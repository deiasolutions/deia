---
title: DEIA pip install Design
version: 0.1.0
date: 2025-10-16
author: Claude (Anthropic)
status: proposal
policy: DND
---

# DEIA pip install Design

## Vision

Enable users to install DEIA with:
```bash
pip install deia
```

And immediately use:
```bash
deia init                    # Bootstrap new project
deia build my-org.yaml       # Build from eOS pack
deia validate llhs/*.md      # Validate entities
deia --help                  # Show all commands
```

## Package Structure

### Directory Layout

```
deia/                           # Python package root
├── pyproject.toml             # Modern Python packaging
├── setup.py                   # Backward compatibility
├── README.md                  # PyPI description
├── LICENSE                    # MIT or Apache 2.0
├── MANIFEST.in                # Include non-Python files
│
├── src/                       # Source code
│   └── deia/                  # Main package
│       ├── __init__.py        # Package init
│       ├── __version__.py     # Version string
│       ├── __main__.py        # python -m deia
│       │
│       ├── cli/               # Command-line interface
│       │   ├── __init__.py
│       │   ├── main.py        # CLI entry point
│       │   ├── init.py        # deia init
│       │   ├── build.py       # deia build
│       │   └── validate.py    # deia validate
│       │
│       ├── core/              # Core functionality
│       │   ├── __init__.py
│       │   ├── factory.py     # Factory builder logic
│       │   ├── parser.py      # eOS pack parser
│       │   ├── validator.py   # Entity validator
│       │   └── rse.py         # RSE logging
│       │
│       ├── templates/         # Packaged templates
│       │   ├── __init__.py
│       │   ├── llh.md         # LLH template
│       │   ├── tag.md         # TAG template
│       │   ├── egg.md         # Factory egg
│       │   └── eos-pack.yaml  # eOS pack template
│       │
│       └── utils/             # Utilities
│           ├── __init__.py
│           ├── paths.py       # Path resolution
│           ├── detect.py      # Mode detection
│           └── git.py         # Git integration
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_factory.py
│   ├── test_parser.py
│   ├── test_validator.py
│   └── fixtures/              # Test data
│       └── example-pack.yaml
│
└── docs/                      # Documentation
    ├── quickstart.md
    ├── reference.md
    └── examples/
        └── startup-org.yaml
```

## pyproject.toml

Modern Python packaging configuration:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "deia"
version = "0.1.0"
description = "DEIA - Decentralized Ephemeral Intelligence Architecture"
readme = "README.md"
authors = [
    {name = "DEIA Contributors", email = "hello@example.com"}
]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries",
    "Topic :: System :: Systems Administration",
]
keywords = ["deia", "llh", "organizational-structure", "simulation", "eos"]
requires-python = ">=3.7"
dependencies = []  # Pure standard library!

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
]

[project.urls]
Homepage = "https://github.com/deiasolutions/deia"
Documentation = "https://docs.deiasolutions.com"
Repository = "https://github.com/deiasolutions/deia"
"Bug Tracker" = "https://github.com/deiasolutions/deia/issues"

[project.scripts]
deia = "deia.cli.main:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
deia = ["templates/*.md", "templates/*.yaml"]
```

## CLI Design

### Entry Point: `deia.cli.main`

```python
#!/usr/bin/env python3
"""DEIA CLI - Main entry point"""

import sys
import argparse
from pathlib import Path
from deia.__version__ import __version__
from deia.cli import init, build, validate

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='deia',
        description='DEIA - Decentralized Ephemeral Intelligence Architecture',
        epilog='See "deia <command> --help" for more information on a specific command.'
    )

    parser.add_argument('--version', action='version', version=f'deia {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # deia init
    init_parser = subparsers.add_parser('init', help='Initialize DEIA in current project')
    init_parser.add_argument('--mode', choices=['project', 'system', 'submodule'],
                            default='project', help='Installation mode')
    init_parser.set_defaults(func=init.run)

    # deia build
    build_parser = subparsers.add_parser('build', help='Build from eOS pack')
    build_parser.add_argument('eos_pack', help='Path to eOS pack YAML')
    build_parser.add_argument('--dry-run', action='store_true', help='Validate but don\'t create')
    build_parser.add_argument('--force', action='store_true', help='Skip approval')
    build_parser.add_argument('--quiet', action='store_true', help='Minimal output')
    build_parser.set_defaults(func=build.run)

    # deia validate
    validate_parser = subparsers.add_parser('validate', help='Validate entities')
    validate_parser.add_argument('files', nargs='+', help='Entity files to validate')
    validate_parser.set_defaults(func=validate.run)

    # Parse and execute
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Command: `deia init`

```python
"""deia init - Initialize DEIA structure"""

from pathlib import Path
import sys

def run(args):
    """Initialize DEIA in current project"""
    mode = args.mode

    print(f"Initializing DEIA (mode: {mode})...")

    if mode == 'project':
        # Create .deia/ structure locally
        create_project_structure()
    elif mode == 'system':
        # Install to ~/.deia/ or %USERPROFILE%\.deia
        create_system_structure()
    elif mode == 'submodule':
        # Add as git submodule
        create_submodule()

    print("✓ DEIA initialized successfully")
    print("\nNext steps:")
    print("  1. Create eOS pack: deia init --template my-org")
    print("  2. Build: deia build .deia/eos-packs/my-org.yaml")
    print("  3. Validate: deia validate .deia/.projects/my-org_001/llhs/*.md")

    return 0

def create_project_structure():
    """Create local .deia/ structure"""
    dirs = [
        '.deia/tools',
        '.deia/templates/llh',
        '.deia/templates/tag',
        '.deia/templates/egg',
        '.deia/templates/eos-pack',
        '.deia/eos-packs',
        '.deia/telemetry',
        '.deia/commons',
        '.deia/.projects',
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    # Initialize files
    Path('.deia/telemetry/rse.jsonl').touch()
    Path('.deia/commons/CHANGELOG.md').write_text('# Commons Changelog (append-only)\n')

    # Copy templates from package
    copy_packaged_templates()

def copy_packaged_templates():
    """Copy templates from installed package"""
    import pkg_resources
    from deia import templates

    # Templates are bundled in package
    template_files = {
        'llh.md': '.deia/templates/llh/minimal-llh.md',
        'tag.md': '.deia/templates/tag/minimal-tag.md',
        'egg.md': '.deia/templates/egg/llh-factory-egg.md',
        'eos-pack.yaml': '.deia/templates/eos-pack/llh-org-eos-pack.yaml',
    }

    for src, dst in template_files.items():
        content = pkg_resources.resource_string('deia.templates', src).decode('utf-8')
        Path(dst).write_text(content)
```

### Command: `deia build`

```python
"""deia build - Build from eOS pack"""

from pathlib import Path
from deia.core.factory import FactoryBuilder

def run(args):
    """Build entities from eOS pack"""
    eos_pack = Path(args.eos_pack)

    if not eos_pack.exists():
        print(f"Error: eOS pack not found: {eos_pack}", file=sys.stderr)
        return 1

    builder = FactoryBuilder(
        eos_pack=eos_pack,
        dry_run=args.dry_run,
        force=args.force,
        quiet=args.quiet
    )

    return builder.build()
```

### Command: `deia validate`

```python
"""deia validate - Validate entities"""

from pathlib import Path
from deia.core.validator import EntityValidator

def run(args):
    """Validate entity files"""
    validator = EntityValidator()

    all_valid = True
    for file_path in args.files:
        path = Path(file_path)
        if not path.exists():
            print(f"✗ Not found: {file_path}")
            all_valid = False
            continue

        errors = validator.validate(path)
        if errors:
            print(f"✗ {file_path}")
            for error in errors:
                print(f"  - {error}")
            all_valid = False
        else:
            print(f"✓ {file_path}")

    return 0 if all_valid else 1
```

## Core Module: `deia.core.factory`

Refactor existing `llh_factory_build.py` into class:

```python
"""DEIA Factory Builder - Core functionality"""

from pathlib import Path
from deia.core.parser import SpecParser
from deia.core.rse import emit_rse
from deia.utils.paths import find_template

class FactoryBuilder:
    """Build entities from eOS packs"""

    def __init__(self, eos_pack: Path, dry_run=False, force=False, quiet=False):
        self.eos_pack = eos_pack
        self.dry_run = dry_run
        self.force = force
        self.quiet = quiet
        self.created_files = []

    def build(self) -> int:
        """Main build process"""
        # Parse eOS pack
        parser = SpecParser(self.eos_pack)
        spec = parser.parse()

        # Validate
        if not self._validate(spec):
            return 1

        # Get approval
        if not self.force and not self.dry_run:
            if not self._get_approval(spec):
                return 2

        # Build entities
        self._build_entities(spec)

        # Validate outputs
        self._validate_outputs()

        # Log to RSE
        emit_rse({
            'type': 'factory_build_complete',
            'eos_pack': str(self.eos_pack),
            'files_created': len(self.created_files)
        })

        return 0

    # ... rest of implementation
```

## Installation & Usage

### For Users

```bash
# Install DEIA
pip install deia

# Initialize new project
cd my-project/
deia init

# Create eOS pack (manual or from template)
cp .deia/templates/eos-pack/llh-org-eos-pack.yaml .deia/eos-packs/my-org.yaml
# Edit my-org.yaml with your entities

# Build from eOS pack
deia build .deia/eos-packs/my-org.yaml

# Validate outputs
deia validate .deia/.projects/my-org_001/llhs/*.md
```

### For Developers

```bash
# Clone repo
git clone https://github.com/deiasolutions/deia
cd deia

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Type check
mypy src/
```

### System-Wide vs Virtual Environment

**Virtual Environment (Recommended for projects):**
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install deia
```

**System-Wide (For personal use across projects):**
```bash
pip install --user deia
# or
sudo pip install deia
```

**User home installation:**
```bash
pip install --user deia
# Installs to ~/.local/lib/python3.x/site-packages/
# CLI available at ~/.local/bin/deia
```

## Path Resolution Strategy

The package needs to find DEIA resources (templates, tools). Priority:

```python
def find_deia_root():
    """Find DEIA installation"""
    # 1. Project-local .deia/
    if Path('.deia/tools').exists():
        return Path('.deia')

    # 2. Environment variable
    if 'DEIA_HOME' in os.environ:
        return Path(os.environ['DEIA_HOME'])

    # 3. User home
    user_deia = Path.home() / '.deia'
    if user_deia.exists():
        return user_deia

    # 4. Package installation (templates only)
    import pkg_resources
    return Path(pkg_resources.resource_filename('deia', 'templates'))
```

## Backward Compatibility

### Keep Existing Tools Working

The standalone `.deia/tools/*.py` scripts should continue to work:

```python
# Existing standalone script
python .deia/tools/llh_factory_build.py --eos-pack pack.yaml

# New package CLI
deia build pack.yaml

# Both work! Package wraps the same core logic
```

### Migration Path

1. **Phase 1 (Current):** Standalone scripts in `.deia/tools/`
2. **Phase 2 (Package):** `pip install deia` wraps existing logic
3. **Phase 3 (Future):** Deprecate standalone scripts (but keep for compatibility)

## Publishing to PyPI

### Initial Release

```bash
# Build package
python -m build

# Test on TestPyPI first
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ deia

# If all good, publish to real PyPI
python -m twine upload dist/*
```

### Version Management

Use semantic versioning:
- `0.1.0` - Initial beta release
- `0.2.0` - New features
- `0.2.1` - Bug fixes
- `1.0.0` - Stable release

## Benefits of pip install

### For Users
- ✅ One command to install: `pip install deia`
- ✅ Simple CLI: `deia init`, `deia build`
- ✅ Works in virtual environments
- ✅ Easy updates: `pip install --upgrade deia`
- ✅ No manual path management

### For Developers
- ✅ Standard Python packaging
- ✅ Test suite integration
- ✅ CI/CD friendly
- ✅ Version management
- ✅ Dependency declaration

### For Teams
- ✅ Consistent versions: `pip install deia==0.2.0`
- ✅ Requirements.txt: Add `deia>=0.1.0`
- ✅ Docker: `RUN pip install deia`
- ✅ CI/CD: No git submodule complexity

## Implementation Checklist

- [ ] Create `pyproject.toml` with package metadata
- [ ] Restructure code into `src/deia/` package layout
- [ ] Move `llh_factory_build.py` → `deia.core.factory`
- [ ] Move `spec_parser.py` → `deia.core.parser`
- [ ] Move `llh_validate.py` → `deia.core.validator`
- [ ] Create CLI entry points (`deia.cli.main`)
- [ ] Bundle templates as package data
- [ ] Write comprehensive README.md for PyPI
- [ ] Add test suite (`tests/`)
- [ ] Set up CI/CD (GitHub Actions)
- [ ] Publish to TestPyPI
- [ ] Test installation from TestPyPI
- [ ] Publish to production PyPI
- [ ] Update egg documentation with pip install instructions

## Coexistence: Package + Standalone

Both approaches can coexist:

**Standalone Mode (Current):**
```bash
# Clone repo or have .deia/ locally
python .deia/tools/llh_factory_build.py --eos-pack pack.yaml
```

**Package Mode (Future):**
```bash
# Install from PyPI
pip install deia
deia build pack.yaml
```

**Hybrid Mode:**
```bash
# Install package for CLI
pip install deia

# But project has local .deia/ with custom tools
# Package respects local .deia/ when present
```

## Related Documentation

- **Factory Egg:** `.deia/templates/egg/llh-factory-egg.md`
- **Current Tools:** `.deia/tools/` (standalone scripts)
- **Package Structure:** This document
- **PyPI Page:** https://pypi.org/project/deia/ (once published)

---

**Status:** Proposal
**Version:** 0.1.0
**Created:** 2025-10-16
**Author:** Claude (Anthropic, Bee Queen)
**Next Steps:** Implement package structure and publish to TestPyPI
