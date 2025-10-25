"""
DEIA Downloads Monitor Service

Automatically routes markdown files from Downloads to project folders based on YAML
frontmatter routing headers. Features safe temp staging, version tracking, and state
persistence across runs.

This is a refactored service version of the user script for production use.

Example:
    >>> from deia.services.downloads_monitor import DownloadsMonitor, StateManager
    >>> state = StateManager('/path/to/state.json')
    >>> monitor = DownloadsMonitor(config_path='/path/to/config.json', state_manager=state)
    >>> success, msg = monitor.route_file('/path/to/file.md')
"""

import os
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, asdict

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class ProcessingConfig:
    """Configuration for file processing behavior."""
    use_temp_staging: bool = False
    cleanup_policy: str = "manual"
    archive_temp_after_route: bool = False


@dataclass
class MonitorConfig:
    """Configuration for downloads monitor."""
    downloads_folder: str
    projects: Dict[str, str]
    default_destination: str = "docs"
    log_file: Optional[str] = None
    processed_folder: Optional[str] = None
    error_folder: Optional[str] = None
    archive_folder: Optional[str] = None
    temp_staging_folder: Optional[str] = None
    processing: Optional[ProcessingConfig] = None


class StateManager:
    """
    Manages state persistence across monitor runs.

    Tracks processed files, error counts, and last run timestamp to enable
    intelligent startup scanning and avoid reprocessing files.

    Args:
        state_file: Path to JSON state file

    Example:
        >>> state = StateManager('/path/to/state.json')
        >>> state.add_processed_file('example.md')
        >>> state.was_file_processed('example.md')
        True
    """

    def __init__(self, state_file: str):
        """Initialize state manager with path to state file."""
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from file, or create default state."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass  # Fall through to default state

        # Default state
        return {
            "last_run": None,
            "last_processed_files": [],
            "processed_count": 0,
            "errors_count": 0
        }

    def save_state(self) -> None:
        """Persist state to disk."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving state: {e}")

    def update_last_run(self) -> None:
        """Update last run timestamp to current time."""
        self.state['last_run'] = datetime.now(timezone.utc).isoformat()
        self.save_state()

    def add_processed_file(self, filename: str) -> None:
        """
        Record a successfully processed file.

        Args:
            filename: Name of processed file
        """
        if filename not in self.state['last_processed_files']:
            self.state['last_processed_files'].append(filename)
        self.state['processed_count'] += 1
        self.save_state()

    def increment_error_count(self) -> None:
        """Increment error counter."""
        self.state['errors_count'] += 1
        self.save_state()

    def get_last_run_datetime(self) -> Optional[datetime]:
        """
        Get last run as datetime object.

        Returns:
            Last run datetime or None if never run
        """
        if not self.state['last_run']:
            return None
        return datetime.fromisoformat(self.state['last_run'])

    def was_file_processed(self, filename: str) -> bool:
        """
        Check if file was successfully processed before.

        Args:
            filename: Name of file to check

        Returns:
            True if file was processed successfully
        """
        return filename in self.state['last_processed_files']


class DownloadsMonitor:
    """
    Monitors Downloads folder and routes markdown files based on YAML frontmatter.

    Features:
        - YAML frontmatter parsing for routing headers
        - Safe temp staging (optional)
        - Version tracking and provenance
        - Startup scanning with state persistence
        - Error handling with quarantine

    Args:
        config_path: Path to JSON configuration file
        state_manager: StateManager instance for persistence

    Example:
        >>> monitor = DownloadsMonitor('/path/to/config.json', state_manager)
        >>> success, msg = monitor.route_file('/path/to/file.md')
        >>> if success:
        ...     print(f"Routed: {msg}")
    """

    def __init__(self, config_path: str, state_manager: StateManager):
        """Initialize downloads monitor with configuration and state."""
        self.config = self._load_config(config_path)
        self.state_manager = state_manager
        self._setup_logging()
        self._ensure_folders()

    def _load_config(self, config_path: str) -> Dict:
        """
        Load routing configuration from JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid JSON
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

    def _setup_logging(self) -> None:
        """Configure logging to file and console."""
        log_file = self.config.get('log_file')

        handlers = []
        if log_file:
            handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
        handlers.append(logging.StreamHandler())

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)

    def _ensure_folders(self) -> None:
        """Create required folders if they don't exist."""
        folders = [
            self.config.get('processed_folder'),
            self.config.get('error_folder'),
            self.config.get('archive_folder'),
            self.config.get('temp_staging_folder')
        ]
        for folder in folders:
            if folder:
                Path(folder).mkdir(parents=True, exist_ok=True)

    def move_to_temp_staging(self, file_path: str) -> Tuple[bool, str]:
        """
        Move file to temp staging area for safe processing.

        When temp staging is enabled, files are moved to a temporary area before
        routing. This provides a safety net - files remain in temp until manually
        cleaned up (or until git commit confirmed in future versions).

        Args:
            file_path: Path to file to stage

        Returns:
            Tuple of (success: bool, staged_path: str)

        Example:
            >>> success, staged_path = monitor.move_to_temp_staging('/path/to/file.md')
            >>> if success:
            ...     print(f"Staged at: {staged_path}")
        """
        if not self.config.get('processing', {}).get('use_temp_staging', False):
            # Temp staging disabled, return original path
            return True, file_path

        filename = os.path.basename(file_path)
        temp_folder = self.config.get('temp_staging_folder')

        if not temp_folder:
            self.logger.warning("Temp staging enabled but temp_staging_folder not configured")
            return True, file_path

        staged_path = os.path.join(temp_folder, filename)

        # Handle conflicts in temp
        if os.path.exists(staged_path):
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}{ext}"
            staged_path = os.path.join(temp_folder, filename)

        try:
            shutil.move(file_path, staged_path)
            self.logger.info(f"Staged to temp: {filename}")
            return True, staged_path
        except Exception as e:
            self.logger.error(f"Error staging {filename} to temp: {e}")
            return False, file_path

    def parse_frontmatter(self, file_path: str) -> Optional[Dict]:
        """
        Extract YAML frontmatter from markdown file.

        Looks for YAML frontmatter delimited by --- at start of file.

        Args:
            file_path: Path to markdown file

        Returns:
            Parsed frontmatter dict or None if no valid frontmatter

        Raises:
            ImportError: If pyyaml not installed

        Example:
            >>> frontmatter = monitor.parse_frontmatter('file.md')
            >>> if frontmatter and 'deia_routing' in frontmatter:
            ...     project = frontmatter['deia_routing']['project']
        """
        if yaml is None:
            raise ImportError("pyyaml required for frontmatter parsing. Install with: pip install pyyaml")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for YAML frontmatter
            if not content.startswith('---'):
                return None

            # Extract frontmatter (between first and second ---)
            parts = content.split('---', 2)
            if len(parts) < 3:
                return None

            frontmatter_text = parts[1].strip()
            return yaml.safe_load(frontmatter_text)

        except Exception as e:
            self.logger.error(f"Error parsing frontmatter in {file_path}: {e}")
            return None

    def route_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Route file to appropriate project folder based on YAML routing header.

        Parses YAML frontmatter to determine target project and destination folder.
        Handles file conflicts with timestamps. When temp staging is enabled, files
        are copied (not moved) so originals remain in temp for safety.

        Args:
            file_path: Path to file to route

        Returns:
            Tuple of (success: bool, message: str)

        Example:
            >>> success, msg = monitor.route_file('/path/to/doc.md')
            >>> print(msg)
            'Routed (copied) doc.md => myproject/docs (temp copy retained)'
        """
        filename = os.path.basename(file_path)

        # Parse frontmatter
        frontmatter = self.parse_frontmatter(file_path)

        if not frontmatter:
            msg = f"No valid YAML frontmatter in {filename}"
            self.logger.warning(msg)
            return False, msg

        # Check for deia_routing section
        if 'deia_routing' not in frontmatter:
            msg = f"No deia_routing section in {filename}"
            self.logger.warning(msg)
            return False, msg

        routing = frontmatter['deia_routing']

        # Get project and destination
        project = routing.get('project')
        destination = routing.get('destination', self.config.get('default_destination', 'docs'))

        if not project:
            msg = f"No project specified in {filename}"
            self.logger.warning(msg)
            return False, msg

        # Check if project exists in config
        if project not in self.config.get('projects', {}):
            msg = f"Unknown project '{project}' in {filename}"
            self.logger.error(msg)
            return False, msg

        # Build target path
        project_path = self.config['projects'][project]
        target_dir = os.path.join(project_path, destination)
        target_path = os.path.join(target_dir, filename)

        # Ensure target directory exists
        Path(target_dir).mkdir(parents=True, exist_ok=True)

        # Handle conflicts
        if os.path.exists(target_path):
            # Add timestamp to avoid overwrite
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}{ext}"
            target_path = os.path.join(target_dir, filename)
            self.logger.warning(f"File conflict resolved by adding timestamp: {filename}")

        # Copy or move file depending on temp staging config
        use_temp_staging = self.config.get('processing', {}).get('use_temp_staging', False)

        try:
            if use_temp_staging:
                # COPY file (leave in temp for safety)
                shutil.copy2(file_path, target_path)
                msg = f"Routed (copied) {filename} => {project}/{destination} (temp copy retained)"
                self.logger.info(msg)
            else:
                # Original behavior: MOVE file
                shutil.move(file_path, target_path)
                msg = f"Routed {filename} => {project}/{destination}"
                self.logger.info(msg)

            # Record to state
            self.state_manager.add_processed_file(filename)
            self._record_processed(filename, target_path)

            return True, msg

        except Exception as e:
            msg = f"Error routing {filename}: {e}"
            self.logger.error(msg)
            return False, msg

    def _record_processed(self, filename: str, target_path: str) -> None:
        """Record successfully processed file to log."""
        processed_folder = self.config.get('processed_folder')
        if not processed_folder:
            return

        record_file = os.path.join(processed_folder, 'processed.log')
        try:
            with open(record_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().isoformat()
                f.write(f"{timestamp} | {filename} -> {target_path}\n")
        except Exception as e:
            self.logger.error(f"Error recording processed file: {e}")

    def handle_error(self, file_path: str, error_msg: str) -> None:
        """
        Move file to error folder and log the issue.

        Quarantines files that can't be processed due to invalid frontmatter,
        unknown projects, or routing errors.

        Args:
            file_path: Path to problem file
            error_msg: Description of error

        Example:
            >>> monitor.handle_error('/path/to/bad.md', 'No routing header found')
        """
        filename = os.path.basename(file_path)
        error_folder = self.config.get('error_folder')

        if not error_folder:
            self.logger.error(f"Error folder not configured, cannot quarantine {filename}: {error_msg}")
            return

        error_path = os.path.join(error_folder, filename)

        try:
            shutil.move(file_path, error_path)
            self.logger.error(f"Moved {filename} to error folder: {error_msg}")
            self.state_manager.increment_error_count()

            # Create error log
            error_log = os.path.join(error_folder, f"{filename}.error.txt")
            with open(error_log, 'w', encoding='utf-8') as f:
                f.write(f"Error: {error_msg}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")

        except Exception as e:
            self.logger.error(f"Error moving {filename} to error folder: {e}")

    def scan_existing_files(self, downloads_folder: str) -> List[str]:
        """
        Scan Downloads folder for markdown files that need processing.

        Uses state tracking to determine which files are new or modified since
        last run. Processes:
        - All files on first run (no last_run timestamp)
        - Files modified after last run
        - Files not in processed list (may have errored before)

        Args:
            downloads_folder: Path to Downloads folder

        Returns:
            List of file paths that need processing

        Example:
            >>> files = monitor.scan_existing_files('/path/to/Downloads')
            >>> print(f"Found {len(files)} files to process")
        """
        last_run = self.state_manager.get_last_run_datetime()

        # Get all .md files in Downloads
        md_files = []
        try:
            for filename in os.listdir(downloads_folder):
                if not filename.lower().endswith('.md'):
                    continue

                file_path = os.path.join(downloads_folder, filename)

                # Check if it's a file (not directory)
                if not os.path.isfile(file_path):
                    continue

                # Determine if file needs processing
                needs_processing = False

                # Case 1: No last run - process all files
                if last_run is None:
                    needs_processing = True
                else:
                    # Case 2: File modified after last run
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc)
                    if mtime > last_run:
                        needs_processing = True
                    # Case 3: File not in processed list (might have been an error before)
                    elif not self.state_manager.was_file_processed(filename):
                        needs_processing = True

                if needs_processing:
                    md_files.append(file_path)

        except Exception as e:
            self.logger.error(f"Error scanning downloads folder: {e}")

        return md_files

    def process_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Process a single file through full pipeline: stage → route → handle errors.

        Args:
            file_path: Path to file to process

        Returns:
            Tuple of (success: bool, message: str)

        Example:
            >>> success, msg = monitor.process_file('/path/to/file.md')
            >>> if not success:
            ...     print(f"Processing failed: {msg}")
        """
        # Step 1: Move to temp staging if enabled
        staged, staged_path = self.move_to_temp_staging(file_path)

        if not staged:
            msg = f"Failed to stage {os.path.basename(file_path)}"
            self.logger.error(msg)
            return False, msg

        # Step 2: Route file from temp (or original location)
        success, message = self.route_file(staged_path)

        # Step 3: Handle errors (file stays in temp or moves to error folder)
        if not success and os.path.exists(staged_path):
            self.handle_error(staged_path, message)

        return success, message
