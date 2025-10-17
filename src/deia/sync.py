"""
DEIA Sync - Automatic document routing from Downloads to projects.

Watches Downloads folder for markdown files with YAML frontmatter and
routes them to appropriate project folders based on routing headers.

Features:
- Version tracking with gap detection
- Unsubmitted draft provenance
- Safe temp staging (copies, not moves)
- State persistence across runs
"""

import os
import sys
import json
import time
import shutil
import logging
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, List

try:
    import yaml
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Install with: pip install pyyaml watchdog")
    sys.exit(1)

from .sync_state import StateManager
from .sync_provenance import ProvenanceTracker


class DownloadsSyncer(FileSystemEventHandler):
    """Routes markdown documents from Downloads to project folders."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize syncer.

        Args:
            config_path: Path to routing config file. If None, uses ~/.deia/config.json
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._ensure_folders()

        # Initialize state manager
        state_file = self.config.get('state_file', os.path.join(
            os.path.expanduser("~"),
            ".deia",
            "sync",
            "state.json"
        ))
        self.state_manager = StateManager(state_file)

        # Initialize provenance tracker
        self.provenance_tracker = ProvenanceTracker(self.config)

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """
        Load routing configuration from JSON file.

        Supports both old format (routing-config.json) and new format
        (integrated into main deia config).

        Args:
            config_path: Path to config file

        Returns:
            Config dictionary
        """
        if config_path is None:
            # Try new format first (~/.deia/config.json)
            new_config_path = os.path.join(
                os.path.expanduser("~"),
                ".deia",
                "config.json"
            )

            # Fall back to old format if new doesn't exist
            if not os.path.exists(new_config_path):
                config_path = os.path.join(
                    os.path.expanduser("~"),
                    ".deia",
                    "downloads-monitor",
                    "routing-config.json"
                )
            else:
                config_path = new_config_path

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                full_config = json.load(f)

            # Check if this is new format (has 'sync' section)
            if 'sync' in full_config:
                sync_config = full_config['sync']
                # Merge with projects from main config
                sync_config['projects'] = full_config.get('projects', {})
                config = sync_config
            else:
                # Old format - use as-is
                config = full_config

            # Set defaults for optional fields
            config.setdefault('default_destination', 'docs')
            config.setdefault('log_file', os.path.join(
                os.path.expanduser("~"),
                ".deia",
                "sync",
                "sync.log"
            ))
            config.setdefault('processed_folder', os.path.join(
                os.path.expanduser("~"),
                ".deia",
                "sync",
                "processed"
            ))
            config.setdefault('error_folder', os.path.join(
                os.path.expanduser("~"),
                ".deia",
                "sync",
                "errors"
            ))
            config.setdefault('archive_folder', None)
            config.setdefault('temp_staging_folder', os.path.join(
                config.get('downloads_folder', os.path.join(os.path.expanduser("~"), "Downloads")),
                ".deia-staging"
            ))
            config.setdefault('processing', {
                'use_temp_staging': True,
                'cleanup_policy': 'manual'
            })

            return config

        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Configure logging to file and console."""
        log_file = self.config['log_file']

        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _ensure_folders(self):
        """Create processed, error, archive, and temp staging folders if they don't exist."""
        folders = [
            self.config['processed_folder'],
            self.config['error_folder'],
            self.config.get('archive_folder'),
            self.config.get('temp_staging_folder')
        ]
        for folder in folders:
            if folder:
                Path(folder).mkdir(parents=True, exist_ok=True)

    def move_to_temp_staging(self, file_path: str) -> Tuple[bool, str]:
        """
        Move file to temp staging area for safe processing.

        Returns:
            (success: bool, staged_path: str)
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
        """Extract YAML frontmatter from markdown file."""
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

    def _parse_semver(self, version_str: str) -> Tuple[int, int, int]:
        """Parse semantic version string into (major, minor, patch)."""
        try:
            # Handle 'vX.Y.Z' or 'X.Y.Z' format
            version_str = version_str.lstrip('v')
            parts = version_str.split('.')
            major = int(parts[0]) if len(parts) > 0 else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return (major, minor, patch)
        except (ValueError, AttributeError):
            return (0, 0, 0)

    def _extract_version_from_filename(self, filename: str) -> Optional[str]:
        """Extract version number from filename (e.g., 'doc-v1.2.md' -> '1.2')."""
        match = re.search(r'-v?(\d+\.\d+(?:\.\d+)?)', filename)
        return match.group(1) if match else None

    def _check_version_gap(self, current_version: str, replaced_version: str) -> bool:
        """Detect if there's a version jump (e.g., v2.0 -> v4.0)."""
        curr = self._parse_semver(current_version)
        repl = self._parse_semver(replaced_version)

        # Check for major version gap
        if curr[0] - repl[0] > 1:
            return True

        # Check for minor version gap (within same major)
        if curr[0] == repl[0] and curr[1] - repl[1] > 1:
            return True

        return False

    def route_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Route file to appropriate project folder based on DEIA routing header.
        Includes version tracking and provenance.

        Returns:
            (success: bool, message: str)
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
        destination = routing.get('destination', self.config['default_destination'])

        if not project:
            msg = f"No project specified in {filename}"
            self.logger.warning(msg)
            return False, msg

        # Check if project exists in config
        if project not in self.config['projects']:
            msg = f"Unknown project '{project}' in {filename}"
            self.logger.error(msg)
            return False, msg

        # Build target path
        project_path = self.config['projects'][project]
        target_dir = os.path.join(project_path, destination)
        target_path = os.path.join(target_dir, filename)

        # Ensure target directory exists
        Path(target_dir).mkdir(parents=True, exist_ok=True)

        # Version tracking: Check for replaces field
        if 'replaces' in frontmatter:
            replaces_list = frontmatter['replaces']
            if not isinstance(replaces_list, list):
                replaces_list = [replaces_list]

            current_version = frontmatter.get('version') or self._extract_version_from_filename(filename)

            for replace_info in replaces_list:
                replaced_version = replace_info.get('version', '')
                status = replace_info.get('status', 'submitted')

                # Check for version gap
                if current_version and replaced_version:
                    if self._check_version_gap(current_version, replaced_version):
                        self.logger.warning(
                            f"VERSION GAP DETECTED: {filename} v{current_version} -> v{replaced_version} "
                            f"(skipped intermediate versions)"
                        )

                # Track unsubmitted drafts
                if status == 'unsubmitted-draft':
                    self.logger.warning(
                        f"UNSUBMITTED DRAFT: {filename} replaces v{replaced_version} "
                        f"which was never submitted"
                    )
                    self.provenance_tracker.track_unsubmitted_draft(replace_info, project_path, filename)

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
                # Phase 1: COPY file (leave in temp for safety)
                shutil.copy2(file_path, target_path)
                msg = f"Routed (copied) {filename} -> {project}/{destination} (temp copy retained)"
                self.logger.info(msg)
            else:
                # Original behavior: MOVE file
                shutil.move(file_path, target_path)
                msg = f"Routed {filename} -> {project}/{destination}"
                self.logger.info(msg)

            # Record to state
            self.state_manager.add_processed_file(filename)
            self._record_processed(filename, target_path)

            return True, msg

        except Exception as e:
            msg = f"Error routing {filename}: {e}"
            self.logger.error(msg)
            return False, msg

    def _record_processed(self, filename: str, target_path: str):
        """Record successfully processed file."""
        record_file = os.path.join(self.config['processed_folder'], 'processed.log')
        with open(record_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp} | {filename} -> {target_path}\n")

    def handle_error(self, file_path: str, error_msg: str):
        """Move file to error folder and log the issue."""
        filename = os.path.basename(file_path)
        error_path = os.path.join(self.config['error_folder'], filename)

        try:
            shutil.move(file_path, error_path)
            self.logger.error(f"Moved {filename} to error folder: {error_msg}")
            self.state_manager.increment_error_count()

            # Create error log
            error_log = os.path.join(self.config['error_folder'], f"{filename}.error.txt")
            with open(error_log, 'w', encoding='utf-8') as f:
                f.write(f"Error: {error_msg}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")

        except Exception as e:
            self.logger.error(f"Error moving {filename} to error folder: {e}")

    def scan_existing_files(self, downloads_folder: str) -> List[str]:
        """
        Scan Downloads folder for .md files that need processing.

        Returns list of file paths to process.
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

    def process_file(self, file_path: str):
        """Process a single file (stage -> route -> handle errors)."""
        # Step 1: Move to temp staging if enabled
        staged, staged_path = self.move_to_temp_staging(file_path)

        if not staged:
            self.logger.error(f"Failed to stage {os.path.basename(file_path)}")
            return

        # Step 2: Route file from temp (or original location)
        success, message = self.route_file(staged_path)

        # Step 3: Handle errors (file stays in temp or moves to error folder)
        if not success and os.path.exists(staged_path):
            self.handle_error(staged_path, message)

    def process_existing_files(self) -> None:
        """One-time scan and process existing files."""
        downloads_folder = self.config.get('downloads_folder', os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        ))

        if not os.path.exists(downloads_folder):
            self.logger.error(f"Downloads folder not found: {downloads_folder}")
            return

        # Startup scan: Process existing files
        files_to_process = self.scan_existing_files(downloads_folder)

        # Display report
        self._print_startup_report(files_to_process)

        # Process files found during scan
        if files_to_process:
            self.logger.info(f"Processing {len(files_to_process)} files...")
            for file_path in files_to_process:
                filename = os.path.basename(file_path)
                self.logger.info(f"Processing: {filename}")
                self.process_file(file_path)
            self.logger.info(f"Startup scan complete.")

        # Update last run timestamp
        self.state_manager.update_last_run()

    def _print_startup_report(self, files_to_process: List[str]):
        """Display startup report showing what was found."""
        print("\n" + "="*60)
        print("DEIA Sync - Startup Report")
        print("="*60)

        # Last run info
        last_run = self.state_manager.get_last_run_datetime()
        if last_run:
            time_diff = datetime.now(timezone.utc) - last_run
            hours = int(time_diff.total_seconds() / 3600)
            minutes = int((time_diff.total_seconds() % 3600) / 60)
            print(f"Last run: {hours}h {minutes}m ago ({last_run.strftime('%Y-%m-%d %H:%M:%S UTC')})")
        else:
            print("Last run: Never (first run)")

        # File scan results
        print(f"Found {len(files_to_process)} new .md files in Downloads")

        if files_to_process:
            print("\nFiles to process:")
            for file_path in files_to_process[:10]:  # Show first 10
                print(f"  - {os.path.basename(file_path)}")
            if len(files_to_process) > 10:
                print(f"  ... and {len(files_to_process) - 10} more")

        # Stats
        print(f"\nAll-time stats:")
        print(f"  Processed: {self.state_manager.state['processed_count']} files")
        print(f"  Errors: {self.state_manager.state['errors_count']} files")

        print("="*60 + "\n")

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        file_path = event.src_path

        # Only process .md files
        if not file_path.lower().endswith('.md'):
            return

        # Give the file time to finish writing
        time.sleep(0.5)

        # Process the file
        self.logger.info(f"Detected new file: {os.path.basename(file_path)}")
        self.process_file(file_path)

    def run_interactive(self) -> None:
        """Watch Downloads folder interactively (foreground)."""
        downloads_folder = self.config.get('downloads_folder', os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        ))

        if not os.path.exists(downloads_folder):
            self.logger.error(f"Downloads folder not found: {downloads_folder}")
            sys.exit(1)

        # Start watching for new files
        observer = Observer()
        observer.schedule(self, downloads_folder, recursive=False)
        observer.start()

        print(f"DEIA Sync now watching: {downloads_folder}")
        print(f"Press Ctrl+C to stop\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\nSync stopped")

        observer.join()

    def run_daemon(self) -> None:
        """Run as background daemon (future Phase 2)."""
        raise NotImplementedError("Daemon mode not yet implemented")
