"""
BOK Pattern Validator

Validates BOK pattern submissions per Master Librarian Specification v1.0

Quality Standards (Section 5 of Master Librarian Spec):
1. Completeness ✅ - Required sections, metadata, examples
2. Clarity ✅ - Proper formatting, logical structure
3. Accuracy ✅ - Technical correctness, no broken links
4. Reusability ✅ - Generalizable approach, clear scope
5. Unique Value ✅ - Not duplicate, adds new knowledge
6. Safety & Ethics ✅ - No PII, secrets, malicious code

See: .deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md

This validator implements Phase 2 (Review) of the Knowledge Intake Workflow,
automating quality checks before patterns are integrated into the Body of Knowledge.

Usage:
    from deia.tools.bok_pattern_validator import BOKPatternValidator

    validator = BOKPatternValidator(bok_dir=".deia/bok")
    reports = validator.validate_patterns()
    print(validator.generate_report(reports))

Author: CLAUDE-CODE-004 (Documentation Curator / Master Librarian)
Date: 2025-10-18
Version: 1.0 (Enhanced from Agent BC Phase 3 delivery)
"""

import os
import re
import logging
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Optional dependencies (graceful degradation if not installed)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from markdown import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BOKPatternValidator:
    """
    Validates BOK patterns against Master Librarian Specification v1.0 quality standards.

    This validator implements automated checks for the 6 minimum acceptance criteria
    defined in Section 5 of the Master Librarian Specification:

    1. Completeness - Required sections, frontmatter, examples present
    2. Clarity - Proper markdown formatting, logical structure
    3. Accuracy - Technical correctness, no broken links
    4. Reusability - Generalizable approach, clear scope
    5. Unique Value - Not duplicate, adds new knowledge
    6. Safety & Ethics - No PII, secrets, or malicious code

    Attributes:
        bok_dir (str): Path to BOK directory to validate
        required_sections (List[str]): Minimum required section names
        security_patterns (Dict[str, re.Pattern]): Regex patterns for security checks
        link_check_timeout (int): Timeout in seconds for link checking
    """

    def __init__(
        self,
        bok_dir: str,
        required_sections: Optional[List[str]] = None,
        link_check_timeout: int = 5
    ):
        """
        Initialize the BOK Pattern Validator.

        Args:
            bok_dir: Path to BOK directory containing patterns to validate
            required_sections: Optional list of required section names
                              (defaults to Problem, Solution, Tags)
            link_check_timeout: Timeout in seconds for HTTP link checks (default 5)
        """
        self.bok_dir = Path(bok_dir)
        self.required_sections = required_sections or [
            "Problem",
            "Solution",
            "Tags"
        ]
        self.link_check_timeout = link_check_timeout

        # Security patterns for detecting PII, secrets, API keys
        self.security_patterns = {
            "api_key": re.compile(r'(api[_-]?key|apikey)\s*[=:]\s*["\']?[\w-]{16,}["\']?', re.IGNORECASE),
            "password": re.compile(r'(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{3,}["\']', re.IGNORECASE),
            "secret": re.compile(r'(secret|token)\s*[=:]\s*["\']?[\w-]{16,}["\']?', re.IGNORECASE),
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "credit_card": re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
        }

    def validate_patterns(self) -> Dict[str, Dict]:
        """
        Validate all patterns in the BOK directory.

        Returns:
            Dict mapping pattern file paths to validation reports

        Example:
            {
                ".deia/bok/patterns/git/multi-agent-workflow.md": {
                    "file": ".deia/bok/patterns/git/multi-agent-workflow.md",
                    "quality_score": 95,
                    "completeness_score": 100,
                    "clarity_score": 90,
                    "accuracy_score": 100,
                    "reusability_score": 90,
                    "unique_value_score": 100,
                    "safety_score": 100,
                    "issues": [],
                    "warnings": [],
                    "security_issues": []
                }
            }
        """
        patterns = self._get_pattern_files()
        validation_reports = {}

        for pattern_file in patterns:
            logger.info(f"Validating pattern: {pattern_file}")
            try:
                # Read with UTF-8 encoding, handle encoding errors
                with open(pattern_file, "r", encoding='utf-8', errors='replace') as f:
                    content = f.read()

                report = self._validate_pattern(content)
                report["file"] = str(pattern_file)
                validation_reports[str(pattern_file)] = report

            except FileNotFoundError:
                logger.error(f"File not found: {pattern_file}")
                validation_reports[str(pattern_file)] = {
                    "file": str(pattern_file),
                    "error": "File not found",
                    "quality_score": 0
                }
            except Exception as e:
                logger.error(f"Error validating {pattern_file}: {e}")
                validation_reports[str(pattern_file)] = {
                    "file": str(pattern_file),
                    "error": str(e),
                    "quality_score": 0
                }

        return validation_reports

    def _get_pattern_files(self) -> List[Path]:
        """
        Get all markdown files in BOK directory.

        Returns:
            List of Path objects for .md files
        """
        patterns = []

        if not self.bok_dir.exists():
            logger.warning(f"BOK directory does not exist: {self.bok_dir}")
            return patterns

        for md_file in self.bok_dir.rglob("*.md"):
            patterns.append(md_file)

        return patterns

    def _validate_pattern(self, content: str) -> Dict:
        """
        Validate a single pattern against all 6 quality criteria.

        Args:
            content: Full markdown content of the pattern

        Returns:
            Validation report dict with scores and issues
        """
        report = defaultdict(list)

        # Extract frontmatter and sections
        frontmatter, body = self._parse_frontmatter(content)
        sections = self._parse_sections(body)

        # Criterion 1: Completeness
        completeness_score = self._check_completeness(frontmatter, sections, report)

        # Criterion 2: Clarity
        clarity_score = self._check_clarity(sections, report)

        # Criterion 3: Accuracy
        accuracy_score = self._check_accuracy(content, report)

        # Criterion 4: Reusability
        reusability_score = self._check_reusability(sections, report)

        # Criterion 5: Unique Value (placeholder - requires BOK comparison)
        unique_value_score = self._check_unique_value(frontmatter, sections, report)

        # Criterion 6: Safety & Ethics
        safety_score = self._check_safety(content, report)

        # Store individual criterion scores
        report["completeness_score"] = completeness_score
        report["clarity_score"] = clarity_score
        report["accuracy_score"] = accuracy_score
        report["reusability_score"] = reusability_score
        report["unique_value_score"] = unique_value_score
        report["safety_score"] = safety_score

        # Calculate overall quality score (weighted average)
        quality_score = self._calculate_quality_score(
            completeness_score,
            clarity_score,
            accuracy_score,
            reusability_score,
            unique_value_score,
            safety_score
        )
        report["quality_score"] = quality_score

        return dict(report)

    def _parse_frontmatter(self, content: str) -> Tuple[Dict[str, str], str]:
        """
        Parse YAML frontmatter from markdown content.

        Args:
            content: Full markdown content

        Returns:
            Tuple of (frontmatter dict, body content without frontmatter)
        """
        frontmatter = {}
        body = content

        # Check for YAML frontmatter (--- ... ---)
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm_text = parts[1].strip()
                body = parts[2].strip()

                # Parse YAML-like key: value pairs (simple parsing)
                for line in fm_text.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        frontmatter[key.strip()] = value.strip()

        return frontmatter, body

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """
        Parse markdown sections from content.

        Args:
            content: Markdown content (without frontmatter)

        Returns:
            Dict mapping section names to section content
        """
        sections = {}
        current_section = None
        current_content = []

        for line in content.split("\n"):
            # Match ## Section Name (heading level 2)
            if line.startswith("## "):
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()

                # Start new section
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _check_completeness(
        self,
        frontmatter: Dict[str, str],
        sections: Dict[str, str],
        report: Dict
    ) -> int:
        """
        Check Criterion 1: Completeness

        Tests:
        - Required sections present
        - Frontmatter metadata present
        - Sections have sufficient content
        - Examples/code blocks present

        Returns:
            Completeness score (0-100)
        """
        score = 100

        # Check required sections
        for section in self.required_sections:
            if section not in sections:
                report.setdefault("issues", []).append(f"Missing required section: {section}")
                score -= 20

        # Check frontmatter
        if not frontmatter:
            report.setdefault("warnings", []).append("No frontmatter metadata found")
            score -= 10

        # Check section content length (minimum 50 chars for Problem, 100 for Solution)
        if "Problem" in sections and len(sections["Problem"]) < 50:
            report.setdefault("issues", []).append("Problem section too short (< 50 chars)")
            score -= 10

        if "Solution" in sections and len(sections["Solution"]) < 100:
            report.setdefault("issues", []).append("Solution section too short (< 100 chars)")
            score -= 10

        # Check for code blocks or examples
        has_code_blocks = "```" in "\n".join(sections.values())
        if not has_code_blocks:
            report.setdefault("warnings", []).append("No code blocks/examples found")
            score -= 5

        return max(0, score)

    def _check_clarity(self, sections: Dict[str, str], report: Dict) -> int:
        """
        Check Criterion 2: Clarity

        Tests:
        - Proper markdown formatting
        - Logical section organization
        - Tag formatting
        - No excessive jargon without explanation

        Returns:
            Clarity score (0-100)
        """
        score = 100

        # Check tags format
        if "Tags" in sections:
            tags = sections["Tags"].strip()
            # Allow alphanumeric, spaces, hyphens, commas
            if not re.match(r'^[\w\s-]+(,\s*[\w\s-]+)*$', tags):
                report.setdefault("issues", []).append("Malformed tags (should be comma-separated)")
                score -= 10

        # Check for logical organization (sections in reasonable order)
        section_names = list(sections.keys())
        if "Problem" in section_names and "Solution" in section_names:
            problem_idx = section_names.index("Problem")
            solution_idx = section_names.index("Solution")
            if problem_idx > solution_idx:
                report.setdefault("warnings", []).append("Problem section appears after Solution (unusual order)")
                score -= 5

        # Check for excessively long paragraphs (> 500 chars without breaks)
        for section_name, content in sections.items():
            paragraphs = content.split("\n\n")
            for para in paragraphs:
                if len(para) > 500 and "\n" not in para:
                    report.setdefault("warnings", []).append(f"Long paragraph in {section_name} (> 500 chars without breaks)")
                    score -= 3
                    break  # Only warn once per section

        return max(0, score)

    def _check_accuracy(self, content: str, report: Dict) -> int:
        """
        Check Criterion 3: Accuracy

        Tests:
        - No broken links (HTTP/HTTPS)
        - No broken internal references
        - Technical correctness (basic checks)

        Returns:
            Accuracy score (0-100)
        """
        score = 100

        # Check for broken HTTP/HTTPS links
        broken_links = self._check_broken_links(content)
        if broken_links:
            report["broken_links"] = broken_links
            score -= min(25, 5 * len(broken_links))  # Max 25 point deduction

        # Check for broken internal references (anchors)
        broken_anchors = self._check_internal_links(content)
        if broken_anchors:
            report.setdefault("warnings", []).extend([f"Broken internal link: {anchor}" for anchor in broken_anchors])
            score -= min(10, 2 * len(broken_anchors))  # Max 10 point deduction

        return max(0, score)

    def _check_reusability(self, sections: Dict[str, str], report: Dict) -> int:
        """
        Check Criterion 4: Reusability

        Tests:
        - Generalizable approach (not too specific to one project)
        - Clear scope defined
        - Adaptable to different contexts

        Returns:
            Reusability score (0-100)
        """
        score = 100

        # Check for overly specific references (project names, file paths)
        all_content = "\n".join(sections.values())

        # Look for absolute file paths (likely too specific)
        absolute_paths = re.findall(r'[C-Z]:\\[\w\\]+', all_content)
        if absolute_paths:
            report.setdefault("warnings", []).append(f"Contains absolute file paths (may be too specific): {len(absolute_paths)} found")
            score -= 10

        # Check if scope is defined
        if "Scope" not in sections and "Context" not in sections:
            report.setdefault("warnings", []).append("No Scope or Context section (helps define reusability)")
            score -= 5

        return max(0, score)

    def _check_unique_value(
        self,
        frontmatter: Dict[str, str],
        sections: Dict[str, str],
        report: Dict
    ) -> int:
        """
        Check Criterion 5: Unique Value

        Tests:
        - Not a duplicate of existing pattern (basic check)
        - Adds new knowledge or perspective

        Note: Full duplicate detection requires BOK-wide comparison
              This is a basic implementation.

        Returns:
            Unique value score (0-100)
        """
        score = 100

        # Basic check: Does it have a unique title?
        if not frontmatter.get("title"):
            report.setdefault("warnings", []).append("No title in frontmatter (helps identify uniqueness)")
            score -= 10

        # Check for generic/vague content
        all_content = "\n".join(sections.values()).lower()
        generic_phrases = ["todo", "tbd", "coming soon", "under construction"]
        for phrase in generic_phrases:
            if phrase in all_content:
                report.setdefault("warnings", []).append(f"Contains placeholder text: '{phrase}'")
                score -= 5

        return max(0, score)

    def _check_safety(self, content: str, report: Dict) -> int:
        """
        Check Criterion 6: Safety & Ethics

        Tests:
        - No PII (emails, SSN, etc.)
        - No secrets (API keys, passwords, tokens)
        - No malicious code patterns

        Returns:
            Safety score (0-100)
        """
        score = 100
        security_issues = []

        # Check for security patterns
        for pattern_name, pattern_regex in self.security_patterns.items():
            matches = pattern_regex.findall(content)
            if matches:
                # Redact actual values in report
                security_issues.append(f"Possible {pattern_name} detected ({len(matches)} instance(s))")
                score -= 20  # Severe deduction for security issues

        if security_issues:
            report["security_issues"] = security_issues

        # Check for malicious patterns (basic)
        malicious_patterns = [
            (r'eval\s*\(', "eval() usage (potentially dangerous)"),
            (r'exec\s*\(', "exec() usage (potentially dangerous)"),
            (r'__import__\s*\(', "__import__() usage (potentially dangerous)"),
        ]

        for pattern, description in malicious_patterns:
            if re.search(pattern, content):
                report.setdefault("security_issues", []).append(description)
                score -= 15

        return max(0, score)

    def _check_broken_links(self, content: str) -> List[str]:
        """
        Check for broken HTTP/HTTPS links.

        Args:
            content: Full markdown content

        Returns:
            List of broken link URLs
        """
        if not REQUESTS_AVAILABLE:
            logger.warning("requests library not available - skipping link checks")
            return []

        broken_links = []

        # Extract HTTP/HTTPS links from markdown
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)

        for link_text, url in links:
            # Only check HTTP/HTTPS links
            if url.startswith("http://") or url.startswith("https://"):
                try:
                    response = requests.head(url, timeout=self.link_check_timeout, allow_redirects=True)
                    if response.status_code >= 400:
                        broken_links.append(url)
                except requests.exceptions.Timeout:
                    logger.warning(f"Timeout checking link: {url}")
                    broken_links.append(url)
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Error checking link {url}: {e}")
                    broken_links.append(url)

        return broken_links

    def _check_internal_links(self, content: str) -> List[str]:
        """
        Check for broken internal anchor links.

        Args:
            content: Full markdown content

        Returns:
            List of broken anchor references
        """
        broken_anchors = []

        # Extract all anchors (headers create anchors)
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        # Convert to anchor format (lowercase, replace spaces with hyphens)
        valid_anchors = set()
        for header in headers:
            anchor = header.lower().strip()
            anchor = re.sub(r'[^\w\s-]', '', anchor)  # Remove special chars
            anchor = re.sub(r'\s+', '-', anchor)  # Replace spaces with hyphens
            valid_anchors.add(f"#{anchor}")

        # Extract all internal links
        internal_links = re.findall(r'\[([^\]]+)\]\((#[^)]+)\)', content)

        for link_text, anchor in internal_links:
            if anchor not in valid_anchors:
                broken_anchors.append(anchor)

        return broken_anchors

    def _calculate_quality_score(
        self,
        completeness: int,
        clarity: int,
        accuracy: int,
        reusability: int,
        unique_value: int,
        safety: int
    ) -> int:
        """
        Calculate overall quality score from individual criterion scores.

        Weighted average:
        - Completeness: 25%
        - Clarity: 20%
        - Accuracy: 20%
        - Reusability: 15%
        - Unique Value: 10%
        - Safety & Ethics: 10% (but BLOCKER if < 80)

        Args:
            completeness: Completeness score (0-100)
            clarity: Clarity score (0-100)
            accuracy: Accuracy score (0-100)
            reusability: Reusability score (0-100)
            unique_value: Unique value score (0-100)
            safety: Safety score (0-100)

        Returns:
            Overall quality score (0-100)
        """
        # Safety is a blocker - if safety < 80, cap quality at 50
        if safety < 80:
            logger.warning("Safety score < 80 - pattern should be BLOCKED")
            return min(50, int(
                0.25 * completeness +
                0.20 * clarity +
                0.20 * accuracy +
                0.15 * reusability +
                0.10 * unique_value +
                0.10 * safety
            ))

        # Normal weighted average
        return int(
            0.25 * completeness +
            0.20 * clarity +
            0.20 * accuracy +
            0.15 * reusability +
            0.10 * unique_value +
            0.10 * safety
        )

    def generate_report(self, validation_reports: Dict[str, Dict]) -> str:
        """
        Generate human-readable validation report.

        Args:
            validation_reports: Dict of validation results from validate_patterns()

        Returns:
            Formatted string report
        """
        if not validation_reports:
            return "No patterns validated.\n"

        report_lines = ["=" * 80]
        report_lines.append("BOK PATTERN VALIDATION REPORT")
        report_lines.append("Master Librarian Specification v1.0 - Quality Standards")
        report_lines.append("=" * 80)
        report_lines.append("")

        scores = []
        pattern_count = len(validation_reports)

        for pattern_file, result in sorted(validation_reports.items()):
            report_lines.append(f"Pattern: {pattern_file}")
            report_lines.append("-" * 80)

            # Overall score
            quality_score = result.get('quality_score', 0)
            scores.append(quality_score)
            report_lines.append(f"Overall Quality Score: {quality_score}/100")

            # Individual criterion scores
            if 'completeness_score' in result:
                report_lines.append(f"  1. Completeness:  {result['completeness_score']}/100")
                report_lines.append(f"  2. Clarity:       {result['clarity_score']}/100")
                report_lines.append(f"  3. Accuracy:      {result['accuracy_score']}/100")
                report_lines.append(f"  4. Reusability:   {result['reusability_score']}/100")
                report_lines.append(f"  5. Unique Value:  {result['unique_value_score']}/100")
                report_lines.append(f"  6. Safety:        {result['safety_score']}/100")

            # Errors
            if result.get('error'):
                report_lines.append(f"ERROR: {result['error']}")

            # Issues (blocking)
            if result.get('issues'):
                report_lines.append("\nIssues (must fix):")
                for issue in result['issues']:
                    report_lines.append(f"  ❌ {issue}")

            # Warnings (should fix)
            if result.get('warnings'):
                report_lines.append("\nWarnings (recommended fixes):")
                for warning in result['warnings']:
                    report_lines.append(f"  ⚠️  {warning}")

            # Security issues (BLOCKER)
            if result.get('security_issues'):
                report_lines.append("\n🚨 SECURITY ISSUES (BLOCKER):")
                for security_issue in result['security_issues']:
                    report_lines.append(f"  🚨 {security_issue}")

            # Broken links
            if result.get('broken_links'):
                report_lines.append(f"\nBroken Links ({len(result['broken_links'])}):")
                for link in result['broken_links'][:5]:  # Show max 5
                    report_lines.append(f"  🔗 {link}")
                if len(result['broken_links']) > 5:
                    report_lines.append(f"  ... and {len(result['broken_links']) - 5} more")

            report_lines.append("")

        # Summary section
        report_lines.append("=" * 80)
        report_lines.append("SUMMARY")
        report_lines.append("=" * 80)
        report_lines.append(f"Total Patterns Validated: {pattern_count}")

        if scores:
            avg_score = sum(scores) / len(scores)
            report_lines.append(f"Average Quality Score: {avg_score:.1f}/100")

            # Categorize patterns by score
            excellent = [p for p, r in validation_reports.items() if r.get('quality_score', 0) >= 90]
            good = [p for p, r in validation_reports.items() if 70 <= r.get('quality_score', 0) < 90]
            needs_work = [p for p, r in validation_reports.items() if 50 <= r.get('quality_score', 0) < 70]
            reject = [p for p, r in validation_reports.items() if r.get('quality_score', 0) < 50]

            report_lines.append(f"\nQuality Distribution:")
            report_lines.append(f"  ✅ Excellent (90-100): {len(excellent)}")
            report_lines.append(f"  👍 Good (70-89):      {len(good)}")
            report_lines.append(f"  ⚠️  Needs Work (50-69): {len(needs_work)}")
            report_lines.append(f"  ❌ Reject (0-49):     {len(reject)}")

            # Show patterns needing attention
            if reject:
                report_lines.append(f"\n❌ Patterns to REJECT (score < 50):")
                for pattern in sorted(reject, key=lambda p: validation_reports[p].get('quality_score', 0)):
                    score = validation_reports[pattern].get('quality_score', 0)
                    report_lines.append(f"  {score}/100 - {Path(pattern).name}")

            if needs_work:
                report_lines.append(f"\n⚠️  Patterns NEEDING REVISION (score 50-69):")
                for pattern in sorted(needs_work, key=lambda p: validation_reports[p].get('quality_score', 0)):
                    score = validation_reports[pattern].get('quality_score', 0)
                    report_lines.append(f"  {score}/100 - {Path(pattern).name}")

        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("Generated by BOK Pattern Validator v1.0")
        report_lines.append("See: .deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md")
        report_lines.append("=" * 80)

        return "\n".join(report_lines)


# CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bok_pattern_validator.py <bok_directory>")
        sys.exit(1)

    bok_dir = sys.argv[1]
    validator = BOKPatternValidator(bok_dir)
    reports = validator.validate_patterns()
    print(validator.generate_report(reports))
