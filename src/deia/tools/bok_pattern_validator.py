import os
import re
import logging
import asyncio
from collections import defaultdict
from typing import List, Dict

import aiohttp
from markdown import markdown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BOKPatternValidator:
    def __init__(self, bok_dir: str):
        self.bok_dir = bok_dir
        self.required_sections = ["Problem", "Solution", "Tags"]

    def validate_patterns(self) -> Dict[str, Dict]:
        patterns = self._get_pattern_files()
        validation_reports = {}

        for pattern_file in patterns:
            logger.info(f"Validating pattern: {pattern_file}")
            try:
                with open(pattern_file, "r", encoding='utf-8') as f:
                    content = f.read()

                report = self._validate_pattern(content)
                report["file"] = pattern_file
                validation_reports[pattern_file] = report
            except Exception as e:
                logger.error(f"Error validating {pattern_file}: {e}")
                validation_reports[pattern_file] = {
                    "file": pattern_file,
                    "error": str(e),
                    "quality_score": 0
                }

        return validation_reports

    def _get_pattern_files(self) -> List[str]:
        patterns = []
        for root, _, files in os.walk(self.bok_dir):
            for file in files:
                if file.endswith(".md"):
                    patterns.append(os.path.join(root, file))
        return patterns

    def _validate_pattern(self, content: str) -> Dict:
        report = defaultdict(list)
        sections = self._parse_sections(content)

        for section in self.required_sections:
            if section not in sections:
                report["missing_sections"].append(section)

        if len(sections.get("Problem", "")) < 50:
            report["issues"].append("Problem section too short")

        if len(sections.get("Solution", "")) < 100:
            report["issues"].append("Solution section too short")

        if "Tags" in sections:
            # FIXED: Allow hyphens in tags
            if not re.match(r"^[\w\s-]+(,\s*[\w\s-]+)*$", sections["Tags"]):
                report["issues"].append("Malformed tags")

        # PERFORMANCE FIX: Use async link checking with timeout
        report["broken_links"] = self._check_broken_links(content)

        score = self._calculate_quality_score(report)
        report["quality_score"] = score

        return report

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown sections (case-insensitive)"""
        sections = {}
        current_section = None

        for line in content.split("\n"):
            if line.startswith("## "):
                # Case-insensitive section matching
                section_name = line[3:].strip()
                # Normalize to title case for consistency
                current_section = section_name.title()
                sections[current_section] = ""
            elif current_section:
                sections[current_section] += line + "\n"

        return sections

    def _check_broken_links(self, content: str) -> List[str]:
        """Check for broken links (synchronous wrapper for async check)"""
        html = markdown(content)
        links = []

        for match in re.finditer(r'<a\s+href="(.+?)"', html):
            link = match.group(1)
            # Only check HTTP/HTTPS links, skip internal links
            if not link.startswith("#") and (link.startswith("http://") or link.startswith("https://")):
                links.append(link)

        if not links:
            return []

        # PERFORMANCE FIX: Use async for parallel checking with timeout
        return asyncio.run(self._check_links_async(links))

    async def _check_links_async(self, links: List[str]) -> List[str]:
        """Check links asynchronously with timeout"""
        broken_links = []

        # TIMEOUT FIX: Set 5 second timeout per request
        timeout = aiohttp.ClientTimeout(total=5)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Check all links in parallel
                tasks = [self._check_single_link(session, link) for link in links]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for link, result in zip(links, results):
                    if result is True:  # Link is broken
                        broken_links.append(link)
        except Exception as e:
            logger.error(f"Error checking links: {e}")

        return broken_links

    async def _check_single_link(self, session: aiohttp.ClientSession, link: str) -> bool:
        """Check a single link. Returns True if broken, False if OK"""
        try:
            async with session.head(link, allow_redirects=True) as response:
                return response.status >= 400
        except asyncio.TimeoutError:
            logger.warning(f"Timeout checking link: {link}")
            return True  # Consider timed-out links as broken
        except Exception as e:
            logger.warning(f"Error checking link {link}: {e}")
            return True  # Consider any error as broken

    def _calculate_quality_score(self, report: Dict) -> int:
        score = 100

        if report["missing_sections"]:
            score -= 20 * len(report["missing_sections"])

        if report["issues"]:
            score -= 10 * len(report["issues"])

        if report["broken_links"]:
            score -= 5 * len(report["broken_links"])

        return max(0, score)

    def generate_report(self, validation_reports: Dict[str, Dict]) -> str:
        """Generate validation report with division by zero protection"""
        report = "BOK Pattern Validation Report\n\n"

        scores = []

        for pattern, result in validation_reports.items():
            report += f"Pattern: {pattern}\n"
            report += f"Quality Score: {result.get('quality_score', 0)}\n"

            if result.get('error'):
                report += f"ERROR: {result['error']}\n"

            if result.get('missing_sections'):
                report += f"Missing Sections: {', '.join(result['missing_sections'])}\n"

            if result.get('issues'):
                report += f"Issues:\n"
                for issue in result['issues']:
                    report += f"- {issue}\n"

            if result.get('broken_links'):
                report += f"Broken Links:\n"
                for link in result['broken_links']:
                    report += f"- {link}\n"

            report += "\n"
            scores.append(result.get('quality_score', 0))

        report += "Summary\n"

        # DIVISION BY ZERO FIX: Check if scores list is empty
        if scores:
            avg_score = sum(scores) / len(scores)
            report += f"Average Quality Score: {avg_score:.2f}\n"

            # Get patterns with lowest scores
            sorted_patterns = sorted(
                validation_reports.keys(),
                key=lambda x: validation_reports[x].get('quality_score', 0)
            )
            lowest = sorted_patterns[:3] if len(sorted_patterns) >= 3 else sorted_patterns
            report += f"Patterns with Lowest Scores: {', '.join(lowest)}\n"
        else:
            report += "No patterns validated.\n"

        return report
