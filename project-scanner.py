"""
DEIA Project Scanner
Scans deiasolutions project and outputs comprehensive inventory for AI review

Usage:
    python project_scanner.py

Output:
    deia_project_inventory.md (in current directory)
"""

import os
from pathlib import Path
from datetime import datetime
import json


def scan_directory(root_path, ignore_dirs=None, ignore_files=None):
    """Scan directory tree and collect file information"""
    if ignore_dirs is None:
        ignore_dirs = {
            "node_modules",
            "__pycache__",
            ".git",
            "venv",
            "env",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
            ".next",
        }

    if ignore_files is None:
        ignore_files = {".DS_Store", "Thumbs.db", "*.pyc", "*.pyo", "*.pyd"}

    root = Path(root_path)

    inventory = {
        "directories": [],
        "files_by_type": {},
        "total_files": 0,
        "total_dirs": 0,
        "total_size_bytes": 0,
    }

    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out ignored directories
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        rel_path = Path(dirpath).relative_to(root)

        # Count directory
        inventory["total_dirs"] += 1

        dir_info = {"path": str(rel_path), "files": [], "file_count": 0}

        for filename in filenames:
            # Skip ignored files
            if filename in ignore_files or filename.startswith("."):
                continue

            filepath = Path(dirpath) / filename

            # Get file stats
            try:
                stat = filepath.stat()
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime)
            except:
                continue

            # Get extension
            ext = filepath.suffix.lower() or "no_extension"

            file_info = {
                "name": filename,
                "size": size,
                "modified": modified.isoformat(),
                "extension": ext,
            }

            dir_info["files"].append(file_info)
            dir_info["file_count"] += 1

            inventory["total_files"] += 1
            inventory["total_size_bytes"] += size

            # Group by extension
            if ext not in inventory["files_by_type"]:
                inventory["files_by_type"][ext] = []
            inventory["files_by_type"][ext].append(str(rel_path / filename))

        if dir_info["file_count"] > 0:
            inventory["directories"].append(dir_info)

    return inventory


def read_file_content(filepath, max_lines=50):
    """Read first N lines of file for preview"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    lines.append(f"... (truncated, {max_lines}+ lines)")
                    break
                lines.append(line.rstrip())
            return "\n".join(lines)
    except:
        return "[Binary file or read error]"


def find_key_files(root_path):
    """Find important project files"""
    root = Path(root_path)

    key_files = {"manifests": [], "configs": [], "readmes": [], "packages": [], "entry_points": []}

    patterns = {
        "manifests": ["manifest.json", "package.json", "pyproject.toml", "setup.py"],
        "configs": [
            "*.config.js",
            "*.config.ts",
            "tsconfig.json",
            ".eslintrc*",
            "webpack.config.js",
        ],
        "readmes": ["README.md", "README.txt", "CONTRIBUTING.md"],
        "packages": ["requirements.txt", "package-lock.json", "yarn.lock", "Pipfile"],
        "entry_points": ["main.py", "app.py", "index.js", "index.ts", "index.html"],
    }

    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            if "*" in pattern:
                # Wildcard search
                for match in root.rglob(pattern):
                    if ".git" not in str(match) and "node_modules" not in str(match):
                        key_files[category].append(str(match.relative_to(root)))
            else:
                # Exact name search
                for match in root.rglob(pattern):
                    if ".git" not in str(match) and "node_modules" not in str(match):
                        key_files[category].append(str(match.relative_to(root)))

    return key_files


def generate_markdown_report(root_path, inventory, key_files):
    """Generate markdown report"""

    lines = []

    # Header
    lines.append("# DEIA Project Inventory Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().isoformat()}")
    lines.append(f"**Root Path:** {root_path}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total Directories:** {inventory['total_dirs']}")
    lines.append(f"- **Total Files:** {inventory['total_files']}")
    lines.append(f"- **Total Size:** {inventory['total_size_bytes'] / 1024 / 1024:.2f} MB")
    lines.append("")

    # Files by Type
    lines.append("## Files by Type")
    lines.append("")
    lines.append("| Extension | Count | Example Files |")
    lines.append("|-----------|-------|---------------|")

    for ext in sorted(inventory["files_by_type"].keys()):
        files = inventory["files_by_type"][ext]
        count = len(files)
        examples = ", ".join(files[:3])
        if len(files) > 3:
            examples += f" ... (+{len(files)-3} more)"
        lines.append(f"| `{ext}` | {count} | {examples} |")

    lines.append("")

    # Key Files
    lines.append("## Key Project Files")
    lines.append("")

    for category, files in key_files.items():
        if files:
            lines.append(f"### {category.title()}")
            lines.append("")
            for f in files:
                lines.append(f"- `{f}`")
            lines.append("")

    # Directory Structure
    lines.append("## Directory Structure")
    lines.append("")
    lines.append("```")
    for dir_info in sorted(inventory["directories"], key=lambda x: x["path"]):
        path = dir_info["path"]
        count = dir_info["file_count"]
        lines.append(f"{path}/ ({count} files)")
    lines.append("```")
    lines.append("")

    # Important File Contents
    lines.append("## Important File Contents")
    lines.append("")

    # Read key files
    root = Path(root_path)

    for category, files in key_files.items():
        if category in ["manifests", "readmes", "packages"]:
            for f in files[:5]:  # Limit to first 5 per category
                filepath = root / f
                if filepath.exists():
                    lines.append(f"### {f}")
                    lines.append("")
                    lines.append("```")
                    content = read_file_content(filepath, max_lines=100)
                    lines.append(content)
                    lines.append("```")
                    lines.append("")

    # Extension-Specific Sections
    lines.append("## Chrome Extension Files")
    lines.append("")

    extension_files = []
    for ext, files in inventory["files_by_type"].items():
        if ext in [".html", ".js", ".css", ".json"]:
            extension_files.extend(files)

    if extension_files:
        lines.append("Found potential extension files:")
        lines.append("")
        for f in sorted(extension_files):
            if any(
                keyword in f.lower()
                for keyword in ["extension", "popup", "background", "content", "manifest"]
            ):
                lines.append(f"- `{f}`")
                # Read content if it looks like extension file
                filepath = root / f
                if filepath.exists() and filepath.stat().st_size < 50000:  # < 50KB
                    lines.append("")
                    lines.append(f"**Content of {f}:**")
                    lines.append("```")
                    lines.append(read_file_content(filepath))
                    lines.append("```")
                    lines.append("")
    else:
        lines.append("No extension files found yet.")

    lines.append("")

    # Python Project Structure
    lines.append("## Python Project Structure")
    lines.append("")

    python_files = inventory["files_by_type"].get(".py", [])
    if python_files:
        lines.append(f"Found {len(python_files)} Python files:")
        lines.append("")

        # Group by directory
        py_by_dir = {}
        for f in python_files:
            dir_name = str(Path(f).parent)
            if dir_name not in py_by_dir:
                py_by_dir[dir_name] = []
            py_by_dir[dir_name].append(Path(f).name)

        for dir_name in sorted(py_by_dir.keys()):
            lines.append(f"### {dir_name}/")
            lines.append("")
            for filename in sorted(py_by_dir[dir_name]):
                lines.append(f"- {filename}")
            lines.append("")

    lines.append("")

    # Documentation
    lines.append("## Documentation Files")
    lines.append("")

    md_files = inventory["files_by_type"].get(".md", [])
    if md_files:
        lines.append(f"Found {len(md_files)} Markdown files:")
        lines.append("")
        for f in sorted(md_files):
            lines.append(f"- `{f}`")
        lines.append("")

    lines.append("")
    lines.append("---")
    lines.append("**END OF REPORT**")

    return "\n".join(lines)


def main():
    """Main scanner function"""

    # Detect project root (look for common markers)
    current = Path.cwd()

    # Try to find project root
    root_markers = ["package.json", "pyproject.toml", ".git", "manifest.json"]
    project_root = current

    for marker in root_markers:
        if (current / marker).exists():
            project_root = current
            break
        elif (current.parent / marker).exists():
            project_root = current.parent
            break

    print(f"Scanning project at: {project_root}")
    print("This may take a moment...")

    # Scan
    inventory = scan_directory(project_root)
    key_files = find_key_files(project_root)

    # Generate report
    report = generate_markdown_report(project_root, inventory, key_files)

    # Write output
    output_file = current / "deia_project_inventory.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report generated: {output_file}")
    print(f"   Total files scanned: {inventory['total_files']}")
    print(f"   Total directories: {inventory['total_dirs']}")
    print(f"   Report size: {len(report) / 1024:.1f} KB")
    print("\nYou can now upload this file to Claude.ai for review.")


if __name__ == "__main__":
    main()
