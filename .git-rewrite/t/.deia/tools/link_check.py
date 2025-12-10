#!/usr/bin/env python3
"""
DEIA Link Checker - Scans markdown files for broken links

Usage:
    python link_check.py [path] [--format=json|markdown]

Arguments:
    path: Directory or file to scan (default: current directory)
    --format: Output format (default: markdown)
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class LinkChecker:
    """Checks links in markdown files"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.results = {
            "scanned_files": 0,
            "total_links": 0,
            "valid_links": 0,
            "broken_links": 0,
            "files_with_issues": [],
            "link_details": []
        }

    def find_markdown_files(self) -> List[Path]:
        """Find all markdown files in the given path"""
        if self.root_path.is_file():
            return [self.root_path] if self.root_path.suffix == ".md" else []

        md_files = []
        for root, dirs, files in os.walk(self.root_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]

            for file in files:
                if file.endswith('.md'):
                    md_files.append(Path(root) / file)

        return sorted(md_files)

    def extract_links(self, content: str) -> List[Tuple[str, int, str]]:
        """
        Extract markdown links from content
        Returns: List of (link_text, line_number, link_target)
        """
        links = []
        lines = content.split('\n')

        # Match markdown links: [text](target)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

        for line_num, line in enumerate(lines, 1):
            for match in link_pattern.finditer(line):
                text = match.group(1)
                target = match.group(2)
                links.append((text, line_num, target))

        return links

    def check_link(self, link_target: str, source_file: Path) -> Tuple[bool, str]:
        """
        Check if a link target is valid
        Returns: (is_valid, reason)
        """
        # Skip external URLs (we only check local file links)
        if link_target.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
            return (True, "external")

        # Skip anchor-only links
        if link_target.startswith('#'):
            return (True, "anchor")

        # Handle links with anchors
        if '#' in link_target:
            link_target = link_target.split('#')[0]
            if not link_target:  # Just an anchor
                return (True, "anchor")

        # Resolve relative path from source file's directory
        source_dir = source_file.parent
        target_path = (source_dir / link_target).resolve()

        # Check if target exists
        if target_path.exists():
            return (True, "exists")

        return (False, f"not found: {target_path}")

    def scan_file(self, file_path: Path) -> Dict:
        """Scan a single markdown file for links"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "file": str(file_path.relative_to(self.root_path)),
                "error": f"Could not read file: {e}",
                "links": []
            }

        links = self.extract_links(content)
        link_results = []

        for text, line_num, target in links:
            is_valid, reason = self.check_link(target, file_path)

            link_results.append({
                "text": text,
                "target": target,
                "line": line_num,
                "valid": is_valid,
                "reason": reason
            })

            self.results["total_links"] += 1
            if is_valid:
                self.results["valid_links"] += 1
            else:
                self.results["broken_links"] += 1

        file_result = {
            "file": str(file_path.relative_to(self.root_path)),
            "links": link_results,
            "broken_count": sum(1 for l in link_results if not l["valid"])
        }

        if file_result["broken_count"] > 0:
            self.results["files_with_issues"].append(file_result["file"])

        return file_result

    def scan_all(self) -> Dict:
        """Scan all markdown files"""
        md_files = self.find_markdown_files()
        self.results["scanned_files"] = len(md_files)

        for file_path in md_files:
            file_result = self.scan_file(file_path)
            if file_result["broken_count"] > 0 or "error" in file_result:
                self.results["link_details"].append(file_result)

        return self.results

    def format_markdown_report(self) -> str:
        """Format results as markdown"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# Link Check Report

**Generated:** {timestamp}
**Scanned Path:** `{self.root_path}`

---

## Summary

- **Files Scanned:** {self.results['scanned_files']}
- **Total Links:** {self.results['total_links']}
- **Valid Links:** {self.results['valid_links']}
- **Broken Links:** {self.results['broken_links']}
- **Files with Issues:** {len(self.results['files_with_issues'])}

"""

        if self.results['broken_links'] == 0:
            report += "✅ **All links are valid!**\n"
        else:
            report += f"⚠️ **Found {self.results['broken_links']} broken link(s)**\n\n"
            report += "---\n\n## Broken Links\n\n"

            for file_detail in self.results['link_details']:
                if 'error' in file_detail:
                    report += f"### {file_detail['file']}\n\n"
                    report += f"**Error:** {file_detail['error']}\n\n"
                    continue

                report += f"### {file_detail['file']}\n\n"
                report += f"**Broken links:** {file_detail['broken_count']}\n\n"

                for link in file_detail['links']:
                    if not link['valid']:
                        report += f"- **Line {link['line']}:** `[{link['text']}]({link['target']})`\n"
                        report += f"  - Reason: {link['reason']}\n"

                report += "\n"

        report += "---\n\n"
        report += f"*Report generated by DEIA Link Checker v1.0*\n"

        return report

    def format_json_report(self) -> str:
        """Format results as JSON"""
        output = {
            "timestamp": datetime.now().isoformat(),
            "scanned_path": str(self.root_path),
            "summary": {
                "scanned_files": self.results['scanned_files'],
                "total_links": self.results['total_links'],
                "valid_links": self.results['valid_links'],
                "broken_links": self.results['broken_links'],
                "files_with_issues": len(self.results['files_with_issues'])
            },
            "details": self.results['link_details']
        }
        return json.dumps(output, indent=2)


def main():
    """Main entry point"""
    # Parse arguments
    path = "."
    output_format = "markdown"

    for arg in sys.argv[1:]:
        if arg.startswith("--format="):
            output_format = arg.split("=")[1]
        elif not arg.startswith("--"):
            path = arg

    # Run scan
    checker = LinkChecker(path)
    checker.scan_all()

    # Output results with proper encoding
    if output_format == "json":
        output = checker.format_json_report()
    else:
        output = checker.format_markdown_report()

    # Handle Windows encoding issues
    try:
        print(output)
    except UnicodeEncodeError:
        # Fallback to UTF-8 encoding
        sys.stdout.buffer.write(output.encode('utf-8'))
        sys.stdout.buffer.write(b'\n')


if __name__ == "__main__":
    main()
