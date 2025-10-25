"""
Chat Context Loader - Auto-detect and load DEIA project context.

Loads project README, governance, BOK patterns to inform bot responses.
Makes bots context-aware about the DEIA project.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
import json


@dataclass
class ContextFile:
    """A context file loaded into memory."""
    filename: str
    path: str
    content: str
    size_bytes: int
    type: str  # readme, governance, bok, code, other


class ChatContextLoader:
    """Load and manage DEIA project context for chat."""

    def __init__(self, project_root: Path):
        """Initialize context loader."""
        self.project_root = Path(project_root)
        self.loaded_context: List[ContextFile] = []
        self.context_index: Dict[str, str] = {}  # filename -> content
        self.auto_detect_complete = False

    def auto_detect_context(self) -> List[ContextFile]:
        """Auto-detect and load key DEIA context files."""
        context = []

        # Priority 1: README and project info
        readme_files = [
            "README.md",
            "docs/README.md",
            ".deia/README.md",
            ".deia/project/PROJECT-STATUS.md"
        ]

        for readme in readme_files:
            path = self.project_root / readme
            if path.exists():
                context.append(self._load_file(path, "readme"))
                break  # Only load one README

        # Priority 2: Governance and architecture
        governance_files = [
            ".deia/governance/PROJECT-STATUS-QUEEN-JOURNAL.md",
            ".deia/governance/TEAM-STRUCTURE-POST-FIRE-DRILL.md",
            "docs/architecture.md",
            ".deia/protocols/PROTOCOLS-INDEX.md"
        ]

        for gov_file in governance_files:
            path = self.project_root / gov_file
            if path.exists():
                context.append(self._load_file(path, "governance"))

        # Priority 3: BOK patterns and standards
        bok_files = [
            "src/deia/bok.py",
            "docs/bok/",
            ".deia/bok/",
            "docs/PATTERNS.md"
        ]

        for bok_file in bok_files:
            path = self.project_root / bok_file
            if path.exists():
                if path.is_dir():
                    # Load all .md files from directory
                    for md_file in path.glob("*.md"):
                        context.append(self._load_file(md_file, "bok"))
                else:
                    context.append(self._load_file(path, "bok"))

        # Priority 4: Key integration files
        integration_files = [
            ".deia/protocols/PROTOCOL-agent-instruction-consistency.md",
            "docs/ARCHITECTURE.md",
            ".deia/intake/2025-10-25/architecture/2025-10-25-REQUIREMENT-bee-to-bee-service-architecture.md"
        ]

        for int_file in integration_files:
            path = self.project_root / int_file
            if path.exists():
                context.append(self._load_file(path, "governance"))

        self.loaded_context = context
        self._build_index()
        self.auto_detect_complete = True

        return context

    def add_context_file(self, file_path: str) -> Optional[ContextFile]:
        """Manually add a context file."""
        path = Path(file_path)

        if not path.exists():
            return None

        context_file = self._load_file(path, "other")
        self.loaded_context.append(context_file)
        self._build_index()

        return context_file

    def remove_context_file(self, filename: str) -> bool:
        """Remove a context file."""
        for i, ctx in enumerate(self.loaded_context):
            if ctx.filename == filename:
                self.loaded_context.pop(i)
                self._build_index()
                return True

        return False

    def get_context_summary(self) -> str:
        """Get formatted context summary for display."""
        if not self.loaded_context:
            return "No context loaded. Project context not detected."

        summary = f"Context Loaded: {len(self.loaded_context)} files\n"

        for ctx in self.loaded_context:
            summary += f"  • {ctx.filename} ({ctx.size_bytes} bytes, {ctx.type})\n"

        return summary

    def get_context_for_prompt(self, max_chars: int = 5000) -> str:
        """Get context formatted for inclusion in bot prompts."""
        if not self.loaded_context:
            return ""

        # Sort by priority
        priority_order = {"readme": 0, "governance": 1, "bok": 2, "code": 3, "other": 4}
        sorted_context = sorted(
            self.loaded_context,
            key=lambda x: priority_order.get(x.type, 99)
        )

        prompt = "## PROJECT CONTEXT\n\n"
        chars_used = 0

        for ctx in sorted_context:
            if chars_used >= max_chars:
                break

            # Truncate if needed
            content = ctx.content
            remaining = max_chars - chars_used
            if len(content) > remaining:
                content = content[:remaining] + "..."

            prompt += f"### {ctx.filename}\n{content}\n\n"
            chars_used += len(content)

        return prompt

    def get_loaded_files(self) -> List[Dict[str, Any]]:
        """Get list of loaded context files."""
        return [
            {
                "filename": ctx.filename,
                "path": ctx.path,
                "type": ctx.type,
                "size_bytes": ctx.size_bytes
            }
            for ctx in self.loaded_context
        ]

    def _load_file(self, path: Path, file_type: str) -> ContextFile:
        """Load a single file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            content = f"[Error loading file: {e}]"

        return ContextFile(
            filename=path.name,
            path=str(path),
            content=content,
            size_bytes=len(content),
            type=file_type
        )

    def _build_index(self) -> None:
        """Build searchable index of context."""
        self.context_index = {}
        for ctx in self.loaded_context:
            self.context_index[ctx.filename] = ctx.content

    def search_context(self, query: str) -> List[Dict[str, Any]]:
        """Search context for matching files."""
        results = []
        query_lower = query.lower()

        for ctx in self.loaded_context:
            if query_lower in ctx.filename.lower():
                results.append({
                    "filename": ctx.filename,
                    "type": ctx.type,
                    "match_type": "filename"
                })
            elif query_lower in ctx.content.lower():
                results.append({
                    "filename": ctx.filename,
                    "type": ctx.type,
                    "match_type": "content"
                })

        return results
