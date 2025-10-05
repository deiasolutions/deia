"""
Core DEIA functionality - project initialization, log creation, sanitization
"""

from pathlib import Path
from datetime import datetime
import shutil
import re


def init_project(target_path: Path, platform: str):
    """
    Initialize DEIA pipeline structure in the target directory

    Args:
        target_path: Where to create the pipeline
        platform: AI coding platform being used
    """

    # Create directory structure
    dirs = [
        '.deia',
        'devlogs/intake',
        'devlogs/raw',
        'devlogs/reviewed',
        'devlogs/logdump',
        'devlogs/bok',
        'devlogs/wisdom',
        'sanitization-workspace',
    ]

    for dir_path in dirs:
        (target_path / dir_path).mkdir(parents=True, exist_ok=True)

    # Create config
    from .config import create_default_config
    create_default_config(target_path, platform)

    # Copy templates
    from .templates import copy_templates
    copy_templates(target_path)

    # Create .gitignore
    gitignore_content = """# DEIA - IP Protection
*[Ii][Pp]*
*_ip_*
*-ip-*
personal/
private/
sanitization-workspace/
*.local.*
.env*
secrets/
credentials/
"""

    gitignore_path = target_path / '.gitignore'
    if gitignore_path.exists():
        # Append to existing
        with open(gitignore_path, 'a') as f:
            f.write(f"\n\n# Added by DEIA\n{gitignore_content}")
    else:
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)

    # Create START_HERE.md
    from .templates import get_start_here_template
    (target_path / 'START_HERE.md').write_text(get_start_here_template(platform))


def create_session_log(topic: str, session_type: str) -> Path:
    """
    Create a new session log from template

    Args:
        topic: Brief topic slug
        session_type: Type of session (feature, bug-fix, etc.)

    Returns:
        Path to created log file
    """

    # Generate filename
    date_str = datetime.now().strftime('%Y-%m-%d')
    safe_topic = re.sub(r'[^\w-]', '-', topic.lower())
    filename = f"session_{date_str}_{safe_topic}.md"

    # Get current project root (where .deia exists)
    project_root = find_project_root()
    log_path = project_root / 'devlogs' / 'intake' / filename

    # Load template
    from .templates import get_session_log_template
    template = get_session_log_template(session_type)

    # Fill in known fields
    content = template.replace('{{DATE}}', date_str)
    content = content.replace('{{TIME}}', datetime.now().strftime('%H:%M'))
    content = content.replace('{{TYPE}}', session_type)
    content = content.replace('{{TOPIC}}', topic)

    # Write file
    log_path.write_text(content)

    return log_path


def sanitize_file(input_path: str, output_path: str = None) -> Path:
    """
    Sanitize a session log for public sharing

    Args:
        input_path: Path to file to sanitize
        output_path: Where to save sanitized file (optional)

    Returns:
        Path to sanitized file
    """

    input_file = Path(input_path)

    if output_path is None:
        output_file = input_file.parent / f"{input_file.stem}_SANITIZED{input_file.suffix}"
    else:
        output_file = Path(output_path)

    content = input_file.read_text(encoding='utf-8')

    # Run sanitization rules
    from .sanitizer import Sanitizer
    sanitizer = Sanitizer()
    sanitized_content, warnings = sanitizer.sanitize(content)

    # Write sanitized content
    output_file.write_text(sanitized_content, encoding='utf-8')

    # Log warnings if any
    if warnings:
        warning_file = output_file.parent / f"{output_file.stem}_WARNINGS.txt"
        warning_file.write_text('\n'.join(warnings), encoding='utf-8')

    return output_file


def validate_file(file_path: str) -> list[str]:
    """
    Validate a sanitized file is ready for submission

    Args:
        file_path: Path to file to validate

    Returns:
        List of validation issues (empty if valid)
    """

    from .validator import Validator
    validator = Validator()
    issues = validator.validate(Path(file_path))

    return issues


def find_project_root() -> Path:
    """Find the DEIA project root (directory containing .deia)"""

    current = Path.cwd()

    while current != current.parent:
        if (current / '.deia').exists():
            return current
        current = current.parent

    raise FileNotFoundError(
        "Not in a DEIA project. Run 'deia init' first."
    )
