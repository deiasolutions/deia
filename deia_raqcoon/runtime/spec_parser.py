"""
Spec Parser - Convert markdown specifications to structured JSON.

Parses markdown documents with the following structure:
- # Title -> spec.title
- ## Goals -> spec.goals[]
- ## Constraints -> spec.constraints[]
- ## Acceptance Criteria -> spec.acceptance_criteria[]
- ## Out of Scope -> spec.scope_exclusions[]
- ## Tasks -> spec.tasks[]
  - ### TASK-XXX: Title -> task entry
  - **Intent:** -> task.intent
  - **Depends On:** -> task.depends_on[]
  - **Files:** -> task.files[]
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


def parse_spec_markdown(markdown: str) -> Dict:
    """
    Parse a markdown spec document into structured JSON.

    Args:
        markdown: Raw markdown text

    Returns:
        Dict matching spec.json schema

    Raises:
        ValueError: If markdown cannot be parsed
    """
    spec = {
        "goals": [],
        "constraints": [],
        "acceptance_criteria": [],
        "scope_exclusions": [],
        "tasks": [],
        "context": {}
    }

    lines = markdown.strip().split('\n')
    current_section = None
    current_task = None
    task_description_lines = []

    for line in lines:
        stripped = line.strip()

        # Title (H1)
        if stripped.startswith('# ') and 'spec_id' not in spec:
            title = stripped[2:].strip()
            # Extract spec_id if in format "SPEC-XXX: Title"
            match = re.match(r'(SPEC-[A-Z0-9-]+):\s*(.+)', title)
            if match:
                spec['spec_id'] = match.group(1)
                spec['title'] = match.group(2)
            else:
                spec['spec_id'] = f"SPEC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                spec['title'] = title
            continue

        # Section headers (H2)
        if stripped.startswith('## '):
            # Save previous task if exists
            if current_task and task_description_lines:
                current_task['summary'] = '\n'.join(task_description_lines).strip()
                task_description_lines = []

            section = stripped[3:].strip().lower()
            if 'goal' in section:
                current_section = 'goals'
            elif 'constraint' in section:
                current_section = 'constraints'
            elif 'acceptance' in section or 'criteria' in section:
                current_section = 'acceptance_criteria'
            elif 'scope' in section or 'exclusion' in section or 'out of scope' in section:
                current_section = 'scope_exclusions'
            elif 'task' in section:
                current_section = 'tasks'
            elif 'context' in section:
                current_section = 'context'
            else:
                current_section = None
            current_task = None
            continue

        # Task headers (H3)
        if stripped.startswith('### ') and current_section == 'tasks':
            # Save previous task description
            if current_task and task_description_lines:
                current_task['summary'] = '\n'.join(task_description_lines).strip()
                task_description_lines = []

            task_title = stripped[4:].strip()
            match = re.match(r'(TASK-[A-Z0-9-]+):\s*(.+)', task_title)
            if match:
                task_id = match.group(1)
                title = match.group(2)
            else:
                task_id = f"TASK-{len(spec['tasks']) + 1:03d}"
                title = task_title

            current_task = {
                'task_id': task_id,
                'title': title,
                'intent': 'code',  # default
                'depends_on': [],
                'files': []
            }
            spec['tasks'].append(current_task)
            continue

        # Task metadata
        if current_task:
            if stripped.startswith('**Intent:**'):
                intent = stripped.replace('**Intent:**', '').strip().lower()
                if intent in ('code', 'design', 'planning', 'test', 'docs', 'review'):
                    current_task['intent'] = intent
                continue

            if stripped.startswith('**Depends On:**'):
                deps = stripped.replace('**Depends On:**', '').strip()
                if deps.lower() != 'none':
                    current_task['depends_on'] = [
                        d.strip() for d in re.split(r'[,;]', deps)
                        if d.strip() and d.strip().lower() != 'none'
                    ]
                continue

            if stripped.startswith('**Files:**'):
                files = stripped.replace('**Files:**', '').strip()
                current_task['files'] = [
                    f.strip() for f in re.split(r'[,;]', files)
                    if f.strip()
                ]
                continue

            if stripped.startswith('**Assignee:**'):
                current_task['assignee'] = stripped.replace('**Assignee:**', '').strip()
                continue

            if stripped.startswith('**Priority:**'):
                priority = stripped.replace('**Priority:**', '').strip().upper()
                if priority in ('P0', 'P1', 'P2', 'P3'):
                    current_task['priority'] = priority
                continue

            # Task description (non-metadata lines)
            if stripped and not stripped.startswith('**'):
                task_description_lines.append(stripped)
            continue

        # List items for sections
        if current_section and current_section != 'tasks' and current_section != 'context':
            if stripped.startswith('- '):
                item = stripped[2:].strip()
                # Remove checkbox if present
                item = re.sub(r'^\[[ x]\]\s*', '', item)
                if item:
                    spec[current_section].append(item)

    # Save last task description
    if current_task and task_description_lines:
        current_task['summary'] = '\n'.join(task_description_lines).strip()

    return spec


def parse_spec_file(path: Path) -> Dict:
    """
    Load and parse a markdown spec file.

    Args:
        path: Path to markdown file

    Returns:
        Parsed spec dict

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file cannot be parsed
    """
    if not path.exists():
        raise FileNotFoundError(f"Spec file not found: {path}")

    content = path.read_text(encoding='utf-8')
    return parse_spec_markdown(content)


def validate_spec(spec: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate spec against schema.

    Args:
        spec: Parsed spec dict

    Returns:
        Tuple of (is_valid, error_message)
        error_message is None if valid
    """
    # Check required fields
    required = ['spec_id', 'title', 'goals', 'acceptance_criteria']
    for field in required:
        if field not in spec:
            return False, f"Missing required field: {field}"
        if field in ('goals', 'acceptance_criteria') and not spec[field]:
            return False, f"Field '{field}' cannot be empty"

    # Validate spec_id format
    if not re.match(r'^SPEC-[A-Z0-9-]+$', spec.get('spec_id', '')):
        return False, f"Invalid spec_id format: {spec.get('spec_id')}"

    # Validate tasks if present
    for task in spec.get('tasks', []):
        if 'task_id' not in task:
            return False, "Task missing task_id"
        if 'title' not in task:
            return False, f"Task {task.get('task_id')} missing title"
        if 'intent' not in task:
            return False, f"Task {task.get('task_id')} missing intent"

        valid_intents = ('code', 'design', 'planning', 'test', 'docs', 'review')
        if task.get('intent') not in valid_intents:
            return False, f"Task {task.get('task_id')} has invalid intent: {task.get('intent')}"

        # Check dependency references exist
        task_ids = {t.get('task_id') for t in spec.get('tasks', [])}
        for dep in task.get('depends_on', []):
            if dep not in task_ids:
                return False, f"Task {task.get('task_id')} depends on unknown task: {dep}"

    return True, None


# For testing
if __name__ == "__main__":
    example_md = '''# SPEC-TEST-001: Example Specification

## Goals
- Implement feature X
- Ensure backward compatibility

## Constraints
- Must work offline
- No external dependencies

## Acceptance Criteria
- [ ] Feature X works as expected
- [ ] All tests pass
- [ ] Documentation updated

## Out of Scope
- Feature Y
- Performance optimization

## Tasks

### TASK-001: Create Service
**Intent:** code
**Depends On:** None
**Files:** src/service.py

Implement the core service class.

### TASK-002: Add API Endpoint
**Intent:** code
**Depends On:** TASK-001
**Files:** src/api.py

Create REST endpoint for the service.

### TASK-003: Write Tests
**Intent:** test
**Depends On:** TASK-001, TASK-002
**Files:** tests/test_service.py

Unit and integration tests.
'''

    spec = parse_spec_markdown(example_md)
    print(json.dumps(spec, indent=2))

    valid, error = validate_spec(spec)
    print(f"\nValidation: {'PASS' if valid else 'FAIL'}")
    if error:
        print(f"Error: {error}")
