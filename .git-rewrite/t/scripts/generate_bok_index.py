"""
BOK Index Generator

Scans the `bok/` directory for pattern files and generates a master index.

Usage:
    python scripts/generate_bok_index.py

Output:
    .deia/index/master-index.yaml
"""

import os
import yaml
from pathlib import Path

def extract_metadata(file_path: Path) -> dict:
    """Extract metadata from a BOK pattern file"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    metadata = {
        "id": file_path.stem,
        "path": str(file_path.relative_to(Path.cwd())),
    }

    lines = content.split("\n")
    if lines[0].startswith("# "):
        metadata["title"] = lines[0][2:]
    else:
        metadata["title"] = file_path.stem

    metadata["category"] = str(file_path.parent.relative_to(Path.cwd() / "bok"))

    # Extract YAML frontmatter if present
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
        yaml_data = yaml.safe_load("\n".join(yaml_lines))
        metadata.update(yaml_data)

    # Add default tags if not present
    if "tags" not in metadata:
        metadata["tags"] = []

    # Extract summary from first paragraph if not present
    if "summary" not in metadata:
        summary = ""
        for line in lines:
            if line.strip() and not line.startswith("#") and not line.startswith("---"):
                summary = line.strip()
                break
        metadata["summary"] = summary

    return metadata

def generate_bok_index(bok_dir: Path, output_file: Path):
    """Generate the BOK master index"""
    index_data = {"patterns": []}

    # Scan for all markdown files in bok/
    for file_path in bok_dir.glob("**/*.md"):
        try:
            metadata = extract_metadata(file_path)
            index_data["patterns"].append(metadata)
        except Exception as e:
            print(f"Warning: Failed to process {file_path}: {e}")
            continue

    # Write index to YAML
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(index_data, f, sort_keys=False, default_flow_style=False)

    print(f"✅ BOK index generated: {output_file}")
    print(f"   Indexed {len(index_data['patterns'])} patterns")

if __name__ == "__main__":
    bok_dir = Path.cwd() / "bok"
    output_file = Path.cwd() / ".deia" / "index" / "master-index.yaml"

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Generate the index
    generate_bok_index(bok_dir, output_file)
