"""
File Operation Service - Generic file I/O for LLM services

Handles reading task files, writing result files, parsing/extracting code blocks.
Works with any LLM API service (Anthropic, OpenAI, Ollama, etc.)

Architecture:
- Read task files: task-001.md → parse instructions + embedded code
- Write result files: process output → result-001.md
- Extract code: Parse markdown code blocks → actual files
- Agnostic to service type: Works with any LLM provider
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class CodeBlock:
    """Parsed code block from markdown"""
    language: str
    content: str
    filepath: Optional[str] = None
    start_line: int = 0
    end_line: int = 0


@dataclass
class TaskContent:
    """Parsed task file content"""
    title: str
    instructions: str
    code_blocks: List[CodeBlock]
    metadata: Dict[str, Any]
    raw_content: str


@dataclass
class ResultContent:
    """Result file content"""
    title: str
    summary: str
    code_blocks: List[CodeBlock]
    embedded_files: Dict[str, str]  # filepath -> content
    metadata: Dict[str, Any]
    raw_markdown: str


class FileOperationService:
    """
    Generic file operations for LLM services.

    Handles markdown file parsing, code extraction, and file management.
    Service-agnostic: works with any LLM provider.
    """

    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize FileOperationService.

        Args:
            base_dir: Base directory for file operations (default: current directory)
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"FileOperationService initialized with base_dir: {self.base_dir}")

    # ==================== READ OPERATIONS ====================

    def read_task_file(self, task_file_path: str) -> TaskContent:
        """
        Read and parse task file.

        Args:
            task_file_path: Path to task markdown file

        Returns:
            TaskContent: Parsed task with instructions and embedded code

        Raises:
            FileNotFoundError: If task file doesn't exist
            ValueError: If task file format is invalid
        """
        file_path = self.base_dir / task_file_path

        if not file_path.exists():
            raise FileNotFoundError(f"Task file not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading task file {file_path}: {e}")
            raise

        # Parse task content
        task = self._parse_task_markdown(content, task_file_path)
        logger.info(f"Parsed task file: {task_file_path} ({len(task.code_blocks)} code blocks)")

        return task

    def _parse_task_markdown(self, content: str, source_path: str) -> TaskContent:
        """Parse markdown task file."""

        # Extract title (first H1)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled Task"

        # Extract code blocks
        code_blocks = self._extract_code_blocks(content)

        # Extract metadata (YAML front matter if present)
        metadata = self._extract_metadata(content)

        # Instructions are everything except code blocks and metadata
        instructions = self._extract_instructions(content)

        return TaskContent(
            title=title,
            instructions=instructions,
            code_blocks=code_blocks,
            metadata=metadata,
            raw_content=content
        )

    def _extract_code_blocks(self, content: str) -> List[CodeBlock]:
        """Extract all code blocks from markdown."""
        blocks = []

        # Pattern: ```language\n...content...\n```
        pattern = r'```(\w+)?\n(.*?)\n```'

        for match in re.finditer(pattern, content, re.DOTALL):
            language = match.group(1) or 'text'
            code_content = match.group(2)

            block = CodeBlock(
                language=language,
                content=code_content,
                start_line=content[:match.start()].count('\n'),
                end_line=content[:match.end()].count('\n')
            )
            blocks.append(block)

        return blocks

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract YAML metadata from front matter."""
        metadata = {}

        # Simple YAML front matter extraction
        if content.startswith('---'):
            # Find closing ---
            end_match = re.search(r'^---$', content[3:], re.MULTILINE)
            if end_match:
                yaml_section = content[3:3 + end_match.start()]
                for line in yaml_section.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()

        return metadata

    def _extract_instructions(self, content: str) -> str:
        """Extract instructions (non-code content)."""
        # Remove code blocks
        instructions = re.sub(r'```\w*\n.*?\n```', '', content, flags=re.DOTALL)
        # Remove YAML front matter
        instructions = re.sub(r'^---.*?^---\n', '', instructions, flags=re.MULTILINE | re.DOTALL)
        return instructions.strip()

    # ==================== WRITE OPERATIONS ====================

    def write_result_file(self,
                         output_file_path: str,
                         title: str,
                         summary: str,
                         code_blocks: Optional[List[CodeBlock]] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Write result file in markdown format.

        Args:
            output_file_path: Where to save result file
            title: Result title
            summary: Summary/response from LLM
            code_blocks: Optional code blocks to embed
            metadata: Optional metadata to include

        Returns:
            str: Full path to written file
        """
        file_path = self.base_dir / output_file_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Build markdown content
        lines = []

        # Add metadata if present
        if metadata:
            lines.append('---')
            for key, value in metadata.items():
                lines.append(f'{key}: {value}')
            lines.append('---\n')

        # Add title
        lines.append(f'# {title}\n')

        # Add timestamp
        lines.append(f'**Generated:** {datetime.now().isoformat()}\n')

        # Add summary
        lines.append(f'## Summary\n')
        lines.append(f'{summary}\n')

        # Add code blocks if present
        if code_blocks:
            lines.append('## Embedded Code\n')
            for block in code_blocks:
                if block.filepath:
                    lines.append(f'### {block.filepath}\n')
                lines.append(f'```{block.language}')
                lines.append(block.content)
                lines.append('```\n')

        # Write file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            logger.info(f"Wrote result file: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Error writing result file {file_path}: {e}")
            raise

    # ==================== CODE EXTRACTION ====================

    def extract_code_blocks(self, content: str) -> List[CodeBlock]:
        """Extract all code blocks from text content."""
        return self._extract_code_blocks(content)

    def extract_and_save_files(self,
                              code_blocks: List[CodeBlock],
                              target_dir: Optional[str] = None) -> Dict[str, str]:
        """
        Extract code blocks from result and save as actual files.

        Args:
            code_blocks: List of code blocks to save
            target_dir: Target directory (default: base_dir)

        Returns:
            Dict: Mapping of filepath -> full_path_written

        Notes:
            - Looks for filepath in code block filepath attribute
            - If no filepath, uses language.{extension} format
            - Creates directories as needed
        """
        saved_files = {}
        target_path = Path(target_dir) if target_dir else self.base_dir
        target_path.mkdir(parents=True, exist_ok=True)

        for i, block in enumerate(code_blocks):
            if not block.content.strip():
                continue

            # Determine filename
            if block.filepath:
                filename = block.filepath
            else:
                # Use language as fallback
                ext = self._language_to_extension(block.language)
                filename = f'code_{i}.{ext}'

            file_path = target_path / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(block.content)
                saved_files[filename] = str(file_path)
                logger.info(f"Saved code block to: {file_path}")
            except Exception as e:
                logger.error(f"Error saving code block to {file_path}: {e}")

        return saved_files

    @staticmethod
    def _language_to_extension(language: str) -> str:
        """Map language name to file extension."""
        mapping = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'bash': 'sh',
            'shell': 'sh',
            'json': 'json',
            'yaml': 'yaml',
            'yml': 'yml',
            'markdown': 'md',
            'html': 'html',
            'css': 'css',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'rust': 'rs',
            'go': 'go',
        }
        return mapping.get(language.lower(), 'txt')

    # ==================== UTILITY ====================

    def list_tasks(self, pattern: str = "task-*.md") -> List[Path]:
        """List available task files."""
        return list(self.base_dir.glob(pattern))

    def list_results(self, pattern: str = "result-*.md") -> List[Path]:
        """List available result files."""
        return list(self.base_dir.glob(pattern))

    def get_file_stats(self, file_path: str) -> Dict[str, Any]:
        """Get file statistics."""
        path = self.base_dir / file_path

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        stat = path.stat()
        return {
            'path': str(path),
            'size_bytes': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
        }
