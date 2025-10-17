"""
Special Instructions:
- Run this script from the root of the DEIA project directory
- The script will scan the `bok/` directory for pattern files and generate the `master-index.yaml` file
- The generated index file will be saved as `.deia/index/master-index.yaml`
- Ensure that the `bok/` directory exists and contains the pattern files in Markdown format
"""

import os
import logging
import yaml
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_metadata(file_path: Path) -> dict:
    """Extract metadata from a BOK pattern file"""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        return None

    metadata = {
        "id": file_path.stem,
        "path": str(file_path.relative_to(Path.cwd())),
    }

    lines = content.split("\n")
    if lines and lines[0].startswith("# "):
        metadata["title"] = lines[0][2:]
    else:
        metadata["title"] = file_path.stem

    try:
        metadata["category"] = str(file_path.parent.relative_to(Path.cwd() / "bok"))
    except ValueError as e:
        logger.warning(f"File {file_path} is outside bok/ directory: {e}")
        metadata["category"] = "uncategorized"

    yaml_lines = []
    yaml_block = False
    for line in lines:
        if line.startswith("---") and not yaml_block:
            yaml_block = True
            continue
        elif line.startswith("---") and yaml_block:
            break
        elif yaml_block:
            yaml_lines.append(line)

    if yaml_lines:
        try:
            yaml_data = yaml.safe_load("\n".join(yaml_lines))
            if yaml_data:
                metadata.update(yaml_data)
        except yaml.YAMLError as e:
            logger.warning(f"Failed to parse YAML frontmatter in {file_path}: {e}")

    if "tags" not in metadata:
        metadata["tags"] = []

    if "summary" not in metadata:
        summary = ""
        for line in lines:
            if line.strip() and not line.startswith("#") and not line.startswith("---"):
                summary = line.strip()
                break
        metadata["summary"] = summary

    return metadata

def generate_bok_index(bok_dir: Path, output_file: Path):
    """Generate BOK index as a dictionary keyed by pattern_id"""
    # FIXED: Changed from array to dict
    index_data = {"patterns": {}}

    pattern_count = 0
    error_count = 0

    for file_path in bok_dir.glob("**/*.md"):
        try:
            metadata = extract_metadata(file_path)
            if metadata:
                pattern_id = metadata["id"]
                # FIXED: Store as dict, not append to array
                index_data["patterns"][pattern_id] = metadata
                pattern_count += 1
                logger.info(f"Processed pattern: {pattern_id}")
            else:
                error_count += 1
        except Exception as e:
            logger.error(f"Unexpected error processing {file_path}: {e}")
            error_count += 1

    try:
        with open(output_file, "w", encoding='utf-8') as f:
            yaml.dump(index_data, f, default_flow_style=False, allow_unicode=True)

        logger.info(f"BOK index generated: {output_file}")
        logger.info(f"Total patterns: {pattern_count}")
        if error_count > 0:
            logger.warning(f"Errors encountered: {error_count}")
    except Exception as e:
        logger.error(f"Failed to write index file {output_file}: {e}")
        raise

if __name__ == "__main__":
    bok_dir = Path.cwd() / "bok"
    output_file = Path.cwd() / ".deia" / "index" / "master-index.yaml"

    if not bok_dir.exists():
        logger.error(f"BOK directory not found: {bok_dir}")
        exit(1)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    generate_bok_index(bok_dir, output_file)
