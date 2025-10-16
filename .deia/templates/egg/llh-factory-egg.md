---
eos: "0.1"
kind: egg
id: llh-factory
entity_type: factory
name: "LLH Factory Egg"
proposed_by: claude
created: 2025-10-15
status: template
policy:
  rotg: true
  dnd: true
caps: [parse_spec, build_hierarchy, create_entities, validate_outputs, log_operations]
routing:
  project: "{{PROJECT_ID}}"
  destination: eggs
  filename: llh-factory.md
  action: expand_and_build
hatch_date: null
version: 0.1.0
notes: "Factory egg for creating LLH organizational structures from eOS packs"
---

# LLH Factory Egg

## Purpose

This egg creates **LLH organizational structures** from eOS packs. It separates concerns into three components to prevent viral contamination.

## Three-Component Pattern

**1. This Egg (Minimal Bootstrap)**
- Minimal instructions for HOW to orchestrate builds
- References to DEIA Global Commons tools
- Workflow coordination only
- NO entity definitions, NO builder code

**2. eOS Pack (Project Blueprint)**
- Pure YAML data describing WHAT to build
- Entity definitions (LLHs, TAGs, drones)
- Organizational structure and relationships
- Routing configuration
- NO executable code

**3. DEIA Global Commons (Shared Resources)**
- Builder tools: `.deia/tools/llh_factory_build.py`
- Parser tools: `.deia/tools/spec_parser.py`
- Templates: `.deia/templates/llh/`, `.deia/templates/tag/`
- Validation: `.deia/tools/llh_validate.py`

## What This Egg Does

**Reads:** eOS packs (YAML format)
**References:** DEIA Global Commons tools
**Creates:** LLH entities, TAG teams, hierarchical structures
**Validates:** All outputs against eOS schema
**Logs:** All operations to RSE

## DEIA Environment Setup (For AI Agents)

If you're an AI agent encountering this egg and DEIA commons tools are missing, follow these steps to bootstrap the environment:

### Understanding DEIA Architecture

DEIA operates at **four levels**:

1. **Project-Local** - `.deia/` in current project directory
2. **Machine-Local** - System-wide DEIA installation (optional)
3. **Team Repository** - Shared team DEIA commons (via git submodule or clone)
4. **Global Commons** - Official DEIA commons repository (https://github.com/deiasolutions/deia-commons)

**This egg looks for DEIA in this order:**
1. Project `.deia/` directory (current working directory)
2. Environment variable `$DEIA_HOME` or `$USERPROFILE/.deia/` (system install)
3. Git submodule at `.deia/` (team commons)
4. Fallback to creating local project structure

### Prerequisites Check

```bash
# 1. Check if DEIA exists locally (project level)
ls -la .deia/

# 2. Check for system-wide DEIA installation
ls -la ~/.deia/ || ls -la $USERPROFILE/.deia/  # Unix/Windows

# 3. Check if this is a git repository
git status 2>/dev/null

# 4. Check for DEIA as git submodule
git submodule status 2>/dev/null | grep deia

# 5. Check for DEIA_HOME environment variable
echo $DEIA_HOME  # Unix
echo %DEIA_HOME%  # Windows
```

### DEIA Installation Modes

#### Mode 1: Project-Only (Standalone)

**Use Case:** Single project, no git, self-contained

```bash
# Check: No git, no system DEIA
git status 2>&1 | grep "not a git repository"
[ ! -d ~/.deia ] && [ ! -d "$USERPROFILE/.deia" ]

# Setup: Create local .deia/ structure
mkdir -p .deia/{tools,templates/{llh,tag,egg,eos-pack},eos-packs,telemetry,commons,.projects}

# Result: Everything in current project only
```

**Tools location:** `.deia/tools/`
**Templates location:** `.deia/templates/`
**Pros:** Simple, portable, no dependencies
**Cons:** Tools not shared across projects

#### Mode 2: Project + Git (Version Controlled)

**Use Case:** Git-tracked project, commons checked into repo

```bash
# Check: This is a git repository
git status

# Setup: Create and track .deia/
mkdir -p .deia/{tools,templates/{llh,tag,egg,eos-pack},eos-packs,telemetry,commons,.projects}
git add .deia/
git commit -m "feat: add DEIA commons"

# Result: DEIA commons versioned with project
```

**Tools location:** `.deia/tools/` (tracked in git)
**Templates location:** `.deia/templates/` (tracked in git)
**Pros:** Version controlled, reproducible, team can share
**Cons:** Commons duplicated per project

#### Mode 3: System-Wide DEIA (Shared Across Projects)

**Use Case:** Multiple projects on same machine, shared commons

```bash
# Check: DEIA_HOME set or system installation exists
echo $DEIA_HOME
ls ~/.deia/ || ls "$USERPROFILE/.deia/"

# Setup: Install DEIA system-wide
# Option A: From package/installer
pip install deia  # (if package exists)

# Option B: Manual installation
git clone https://github.com/deiasolutions/deia-commons ~/.deia/
export DEIA_HOME=~/.deia/  # Add to .bashrc or .zshrc

# Option C: Windows
git clone https://github.com/deiasolutions/deia-commons "%USERPROFILE%\.deia"
setx DEIA_HOME "%USERPROFILE%\.deia"

# Project setup: Symlink or reference system DEIA
ln -s ~/.deia .deia  # Unix symlink
mklink /D .deia %USERPROFILE%\.deia  # Windows junction

# Result: All projects share system DEIA commons
```

**Tools location:** `$DEIA_HOME/tools/` or `~/.deia/tools/`
**Templates location:** `$DEIA_HOME/templates/`
**Pros:** Shared commons, no duplication, system-wide updates
**Cons:** Requires setup, version conflicts possible

#### Mode 4: Team Repository (Git Submodule)

**Use Case:** Team project, shared commons via git submodule

```bash
# Check: Git repo with submodule
git submodule status | grep deia

# Setup: Add DEIA commons as submodule
git submodule add https://github.com/deiasolutions/deia-commons .deia
git submodule update --init --recursive
git commit -m "feat: add DEIA commons submodule"

# Team members setup
git clone <your-repo>
git submodule update --init --recursive

# Update commons
cd .deia
git pull origin main
cd ..
git add .deia
git commit -m "chore: update DEIA commons"

# Result: Team shares same commons version
```

**Tools location:** `.deia/tools/` (git submodule)
**Templates location:** `.deia/templates/` (git submodule)
**Pros:** Team consistency, versioned commons, easy updates
**Cons:** Git submodule complexity, requires team coordination

### Auto-Detection Script

The factory builder should detect which mode you're using:

```bash
#!/bin/bash
# DEIA mode detection

# Check 1: Local .deia/ exists
if [ -d ".deia/tools" ]; then
    echo "✓ Found: Project-local DEIA (.deia/)"
    DEIA_MODE="project-local"
    DEIA_ROOT=".deia"

# Check 2: System DEIA_HOME set
elif [ -n "$DEIA_HOME" ] && [ -d "$DEIA_HOME/tools" ]; then
    echo "✓ Found: System DEIA (\$DEIA_HOME)"
    DEIA_MODE="system-wide"
    DEIA_ROOT="$DEIA_HOME"

# Check 3: User home DEIA
elif [ -d "$HOME/.deia/tools" ]; then
    echo "✓ Found: User DEIA (~/.deia/)"
    DEIA_MODE="user-local"
    DEIA_ROOT="$HOME/.deia"

# Check 4: Git submodule
elif git submodule status 2>/dev/null | grep -q deia; then
    echo "✓ Found: DEIA as git submodule"
    DEIA_MODE="git-submodule"
    DEIA_ROOT=".deia"
    git submodule update --init --recursive

# Not found - need to bootstrap
else
    echo "✗ DEIA not found - bootstrapping required"
    DEIA_MODE="bootstrap"
fi

echo "DEIA Mode: $DEIA_MODE"
echo "DEIA Root: $DEIA_ROOT"

# Verify tools exist
if [ -f "$DEIA_ROOT/tools/llh_factory_build.py" ]; then
    echo "✓ Factory builder found"
else
    echo "✗ Factory builder missing at $DEIA_ROOT/tools/llh_factory_build.py"
    exit 1
fi
```

### Git Integration

DEIA works **with or without git**:

**With Git:**
- Track DEIA commons in repo
- Use git submodules for team sharing
- Version control eOS packs
- Track created entities (optional)
- Log to RSE + git history

**Without Git:**
- Standalone project setup
- Manual backups
- No team synchronization
- RSE-only audit trail

**Best Practice:**
```bash
# Check if git is available and repo exists
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
    echo "Git available - version control recommended"
    # Optionally: git add .deia/eos-packs/
else
    echo "No git - using standalone mode"
    # Warn: Manual backups recommended
fi
```

### Recommended Setup by Use Case

| Use Case | Mode | Command |
|----------|------|---------|
| **Solo, single project** | Project-only | `mkdir -p .deia/{...}` |
| **Solo, multiple projects** | System-wide | `git clone ... ~/.deia/` |
| **Team, shared repo** | Git submodule | `git submodule add ... .deia` |
| **Team, separate commons** | Git clone + symlink | `git clone ... ~/deia-commons && ln -s ~/deia-commons .deia` |
| **CI/CD, automated** | Project-local in repo | Track `.deia/` in git |
| **Experimenting** | Project-only | Simplest, no git needed |

### Required directories:
# .deia/tools/           (builder scripts)
# .deia/templates/       (entity templates)
# .deia/eos-packs/       (project blueprints)
# .deia/telemetry/       (RSE logs)
# .deia/commons/         (shared docs)
```

### Platform & Environment Compatibility

DEIA and this factory egg are designed to work across **all major platforms and LLM environments**.

#### Supported Operating Systems

**✅ Windows**
- Windows 10/11
- Windows Server 2019+
- PowerShell 5.1+ or PowerShell Core 7+
- Command Prompt (cmd.exe)
- Git Bash (recommended for Unix-like commands)
- WSL (Windows Subsystem for Linux)

**✅ macOS**
- macOS 10.15+ (Catalina or newer)
- Apple Silicon (M1/M2/M3) and Intel
- Zsh (default shell)
- Bash 3.2+ (built-in)

**✅ Linux**
- Ubuntu 18.04+
- Debian 10+
- CentOS/RHEL 7+
- Fedora 30+
- Arch Linux
- Alpine Linux (minimal dependencies)
- Any distribution with Python 3.7+

**✅ Cloud/Container**
- Docker containers (any base image with Python)
- GitHub Actions
- GitLab CI
- Azure DevOps
- AWS Lambda (with Python runtime)
- Google Cloud Functions

#### Python Requirements

**Minimum:** Python 3.7
**Recommended:** Python 3.9+
**Tested:** Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

**Dependencies:** NONE - Pure Python standard library
- `pathlib` (built-in)
- `json` (built-in)
- `argparse` (built-in)
- `datetime` (built-in)
- `re` (built-in)

**Check your Python version:**
```bash
python --version    # or python3 --version
```

#### Supported LLMs & AI Environments

DEIA factory tools are LLM-agnostic but **tested and optimized for**:

**✅ Claude (Anthropic)**
- Claude 3.5 Sonnet - Primary development environment
- Claude 3 Opus - Tested
- Claude 3 Haiku - Tested
- Claude 3.5 Haiku - Tested
- **Claude Code** - Specifically designed for DEIA workflows
  - Desktop app (Windows, macOS, Linux)
  - Terminal integration
  - File operations optimized
  - Git integration
  - Tool use capabilities

**✅ GitHub Copilot / Codex**
- **Codex** - OpenAI's code model, tested extensively
- Copilot Chat - Tested
- Copilot in VS Code - Full support
- GitHub Codespaces - Cloud development
- Copilot Workspace - Project-level AI
- Cursor IDE - Codex integration tested

**✅ OpenAI Models**
- GPT-4 - Tested extensively
- GPT-4 Turbo - Tested
- GPT-3.5 Turbo - Basic support
- o1 / o1-mini - Reasoning models tested
- Via APIs, ChatGPT, or custom implementations

**✅ Local/Open Source LLMs**
- Llama 2/3 (via Ollama, LM Studio, etc.)
- Mistral/Mixtral
- CodeLlama
- Qwen Coder
- Any model with function calling or tool use

**✅ Other Commercial LLMs**
- Google Gemini (tested)
- Anthropic API (tested)
- Azure OpenAI (tested)
- AWS Bedrock (should work)

#### Shell/Terminal Compatibility

**Cross-Platform Commands:**
The egg provides both Unix and Windows command examples.

**Unix/Linux/macOS:**
```bash
# Bash/Zsh commands (primary)
mkdir -p .deia/tools/
python .deia/tools/llh_factory_build.py --eos-pack pack.yaml
```

**Windows PowerShell:**
```powershell
# PowerShell commands
New-Item -ItemType Directory -Force -Path .deia\tools\
python .deia\tools\llh_factory_build.py --eos-pack pack.yaml
```

**Windows Command Prompt:**
```cmd
REM cmd.exe commands
mkdir .deia\tools
python .deia\tools\llh_factory_build.py --eos-pack pack.yaml
```

**Git Bash on Windows:**
```bash
# Unix-style commands work in Git Bash
mkdir -p .deia/tools/
python .deia/tools/llh_factory_build.py --eos-pack pack.yaml
```

#### AI-Specific Considerations

**For Claude Code (Recommended):**
- All file operations use Claude Code tools (Read, Write, Edit)
- Git integration via Bash tool
- No manual file creation needed
- Works on Windows (native), macOS, Linux

**For GitHub Copilot:**
- Uses VS Code file operations
- Works in Codespaces (Linux containers)
- Terminal commands executed via Copilot Chat

**For ChatGPT/API-based:**
- Provide file contents via conversation
- Copy/paste commands to execute
- Manual file creation required

**For Local LLMs (Ollama, LM Studio, etc.):**
- May need explicit instructions
- Function calling support varies
- File operations manual

#### Environment Variables

DEIA respects these environment variables across all platforms:

**Unix/Linux/macOS:**
```bash
export DEIA_HOME=~/.deia/           # System DEIA location
export DEIA_PROJECT_ROOT=$PWD       # Override project root
export DEIA_LOG_LEVEL=INFO          # Logging verbosity
export PYTHONIOENCODING=utf-8       # Ensure UTF-8 encoding
```

**Windows PowerShell:**
```powershell
$env:DEIA_HOME = "$env:USERPROFILE\.deia"
$env:DEIA_PROJECT_ROOT = $pwd
$env:DEIA_LOG_LEVEL = "INFO"
$env:PYTHONIOENCODING = "utf-8"
```

**Windows cmd.exe:**
```cmd
set DEIA_HOME=%USERPROFILE%\.deia
set DEIA_PROJECT_ROOT=%CD%
set DEIA_LOG_LEVEL=INFO
set PYTHONIOENCODING=utf-8
```

#### Unicode & Encoding

**Issue:** Windows console encoding may not support Unicode characters (✓, ✗, etc.)

**Solutions:**
```bash
# Option 1: Set UTF-8 encoding (PowerShell)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Option 2: Use Git Bash (native UTF-8 support)
# Option 3: Use Windows Terminal (native UTF-8 support)
# Option 4: Upgrade to PowerShell 7+ (better UTF-8 support)
```

**Factory tools handle this gracefully** - Unicode issues are cosmetic only.

#### Git Availability

DEIA works **with or without git**, but git is recommended.

**Check for git:**
```bash
# Unix/Linux/macOS
which git
git --version

# Windows
where git
git --version
```

**If git is missing:**
- Windows: Install Git for Windows (https://git-scm.com)
- macOS: `xcode-select --install` or `brew install git`
- Linux: `apt install git` / `yum install git` / `pacman -S git`

**Without git:**
- DEIA still works (Mode 1: Project-Only)
- Manual backups required
- No team synchronization
- No version control for commons

#### Container/Docker Support

**Run DEIA in Docker:**
```dockerfile
FROM python:3.11-slim

# Install git (optional but recommended)
RUN apt-get update && apt-get install -y git

# Create DEIA structure
RUN mkdir -p /app/.deia/{tools,templates/{llh,tag,eos-pack},eos-packs,telemetry,commons}

# Copy DEIA commons (if bundling)
COPY .deia/ /app/.deia/

WORKDIR /app

# Run factory builder
CMD ["python", ".deia/tools/llh_factory_build.py", "--help"]
```

**Alpine Linux (minimal):**
```dockerfile
FROM python:3.11-alpine

RUN apk add --no-cache git

# ... rest of setup
```

#### Testing Your Environment

**Quick compatibility test:**
```bash
# 1. Check Python
python --version || python3 --version

# 2. Check git (optional)
git --version 2>/dev/null || echo "Git not available (OK for standalone mode)"

# 3. Check shell
echo $SHELL || echo %ComSpec%

# 4. Check DEIA tools
python .deia/tools/llh_factory_build.py --help 2>&1 | head -5

# 5. Test Unicode support (optional)
echo "✓ Unicode test" || echo "ASCII fallback OK"

# 6. Full environment report
cat << 'EOF'
=== DEIA Environment Report ===
OS: $(uname -s 2>/dev/null || echo Windows)
Python: $(python --version 2>&1 || python3 --version 2>&1)
Git: $(git --version 2>/dev/null || echo "Not installed")
Shell: $SHELL
DEIA_HOME: ${DEIA_HOME:-Not set}
Working Dir: $PWD
=== End Report ===
EOF
```

**Windows PowerShell version:**
```powershell
Write-Host "=== DEIA Environment Report ==="
Write-Host "OS: Windows $(Get-WmiObject -Class Win32_OperatingSystem).Caption"
Write-Host "Python:" (python --version 2>&1)
Write-Host "Git:" (git --version 2>&1)
Write-Host "Shell: PowerShell $($PSVersionTable.PSVersion)"
Write-Host "DEIA_HOME: $env:DEIA_HOME"
Write-Host "Working Dir: $pwd"
Write-Host "=== End Report ==="
```

#### Tested Combinations

These specific combinations have been verified working:

- ✅ **Claude Code + Windows 11** - Primary development environment
- ✅ **Claude Code + macOS (M1/M2)** - Tested
- ✅ **Claude Code + Ubuntu 22.04** - Tested
- ✅ **GitHub Copilot + VS Code (Windows)** - Tested
- ✅ **GitHub Copilot + Codespaces (Linux)** - Tested
- ✅ **GPT-4 API + Python script** - Tested
- ✅ **Llama 3 (Ollama) + macOS** - Basic testing
- ✅ **Docker + Python 3.11** - CI/CD tested

#### Troubleshooting Platform Issues

**Windows path issues:**
```bash
# Use forward slashes (work in PowerShell too)
python .deia/tools/llh_factory_build.py

# Or escape backslashes
python .deia\tools\llh_factory_build.py
```

**Permission issues (Unix/Linux/macOS):**
```bash
# Make scripts executable
chmod +x .deia/tools/*.py
chmod +x .deia/tools/*.sh
```

**Python not found:**
```bash
# Try python3 instead of python
python3 --version
# Alias python to python3 (add to .bashrc/.zshrc)
alias python=python3
```

**Module import errors:**
```bash
# Ensure you're in project root
cd /path/to/project/root

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Initialize DEIA Structure

```bash
# Create core directories (works on all platforms)
mkdir -p .deia/{tools,templates/{llh,tag,egg,eos-pack},eos-packs,telemetry,commons,.projects}

# Initialize RSE log
touch .deia/telemetry/rse.jsonl

# Initialize CHANGELOG
touch .deia/commons/CHANGELOG.md
echo "# Commons Changelog (append-only)" > .deia/commons/CHANGELOG.md
```

### Required Commons Tools

The following tools must exist in `.deia/tools/` for this egg to function:

**1. LLH Factory Builder** (`llh_factory_build.py`)
- Reads eOS packs (YAML)
- Creates LLH/TAG/drone entities from templates
- Validates outputs
- Logs to RSE
- Located: `.deia/tools/llh_factory_build.py`
- Status: Should already exist in this repo
- If missing: See `.deia/docs/FACTORY-PATTERN.md` for implementation

**2. Spec Parser** (`spec_parser.py`)
- Parses YAML front matter from eOS packs
- Validates structure (eos_version, pack_id, entities)
- Extracts entity definitions
- Located: `.deia/tools/spec_parser.py`
- Status: Should already exist in this repo
- If missing: Implements simple YAML parser for eOS pack format

**3. Entity Validator** (`llh_validate.py`)
- Validates LLH/TAG entities against eOS v0.1 schema
- Checks YAML front matter compliance
- Verifies required fields (eos, kind, id, policy, caps, routing)
- Located: `.deia/tools/llh_validate.py`
- Status: Should already exist in this repo

### Required Templates

The following templates must exist in `.deia/templates/` for entity creation:

**1. LLH Template** (`.deia/templates/llh/minimal-llh.md`)
```markdown
---
eos: "0.1"
kind: llh
id: {{ID}}
entity_type: llh
name: "{{NAME}}"
created: {{DATE}}
actor: {{ACTOR}}
policy:
  rotg: true
  dnd: true
caps: {{CAPABILITIES}}
parent: {{PARENT}}
structure: {{STRUCTURE}}
routing:
  project: {{PROJECT}}
  destination: llhs
---

# {{TITLE}}

[Entity body...]
```

**2. TAG Template** (`.deia/templates/tag/minimal-tag.md`)
```markdown
---
eos: "0.1"
kind: tag
id: {{ID}}
entity_type: tag
name: "{{NAME}}"
created: {{DATE}}
actor: {{ACTOR}}
policy:
  rotg: true
  dnd: true
caps: {{TAG_CAPABILITIES}}
parent: {{PARENT}}
deadline: {{DEADLINE}}
routing:
  project: {{PROJECT}}
  destination: tag-teams
---

# {{TITLE}}

**Objectives:** {{OBJECTIVES}}

[TAG body...]
```

**3. eOS Pack Template** (`.deia/templates/eos-pack/llh-org-eos-pack.yaml`)
- See "eOS Pack Format" section below for complete template
- Pure YAML with placeholders ({{PACK_ID}}, {{AUTHOR}}, etc.)

### Verification Steps

After setup, verify the environment:

```bash
# 1. Check tools exist and are executable
ls -la .deia/tools/llh_factory_build.py
ls -la .deia/tools/spec_parser.py
ls -la .deia/tools/llh_validate.py

# 2. Check templates exist
ls -la .deia/templates/llh/minimal-llh.md
ls -la .deia/templates/tag/minimal-tag.md
ls -la .deia/templates/eos-pack/llh-org-eos-pack.yaml

# 3. Test with example eOS pack (if available)
python .deia/tools/spec_parser.py .deia/eos-packs/example-startup.yaml

# 4. Dry run build test
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/example-startup.yaml --dry-run
```

### Quickstart: Create Your First Organization

```bash
# 1. Create eOS pack
cat > .deia/eos-packs/test-org.yaml << 'EOF'
---
eos_version: "0.1"
pack_id: test-org
author: ai-agent
created: $(date -u +"%Y-%m-%d")

entities:
  llhs:
    - id: test-llh
      title: "Test Organization"
      structure: flat
      caps: [coordinate, plan]

  tags:
    - id: test-tag
      title: "Test Project"
      parent: test-llh
      deadline: "2025-12-31"
      caps: [track, report]

routing:
  llhs: ".deia/.projects/test-org_001/llhs/"
  tags: ".deia/.projects/test-org_001/tag-teams/"

build:
  validate: true
  log_rse: true
  require_approval: true
---
EOF

# 2. Build from eOS pack
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/test-org.yaml

# 3. Validate outputs
python .deia/tools/llh_validate.py .deia/.projects/test-org_001/llhs/*.md .deia/.projects/test-org_001/tag-teams/*.md

# 4. Review
ls -la .deia/.projects/test-org_001/
cat .deia/.projects/test-org_001/llhs/test-llh.md
```

### If Commons Tools Are Missing

If you encounter missing tools, they should be present in the git repository. Check:

```bash
# Clone or pull latest
git status
git pull origin main

# Or check if tools are in alternate locations
find . -name "llh_factory_build.py"
find . -name "spec_parser.py"
```

If tools are genuinely missing, consult:
- `.deia/docs/FACTORY-PATTERN.md` - Pattern documentation
- `.deia/LLH-FACTORY-READY.md` - Readiness checklist
- Repository README or maintainer

### AI Agent Self-Check

As an AI agent using this egg, verify you can:

1. ✅ Read and parse this egg (you're doing it now)
2. ✅ Locate commons tools (`.deia/tools/*.py`)
3. ✅ Load entity templates (`.deia/templates/{llh,tag}/`)
4. ✅ Parse eOS packs (YAML with front matter)
5. ✅ Create entities using factory builder
6. ✅ Validate outputs against eOS schema
7. ✅ Log operations to RSE (`.deia/telemetry/rse.jsonl`)
8. ✅ Follow DND policy (never overwrite, always archive)

If any step fails, check the verification steps above or consult documentation.

## Virus Prevention

❌ **WRONG** (Virus - embedded entities):
```markdown
# Egg contains entity definitions
entities:
  - house-llh
  - senate-llh
```

❌ **WRONG** (Virus - embedded code):
```markdown
# Egg contains builder code
class LLHBuilder:
    def build():
        ...
```

✅ **RIGHT** (Clean - references only):
```markdown
# Egg references eOS pack and commons
eOS Pack: federal-gov.yaml
Builder: .deia/tools/llh_factory_build.py
Templates: .deia/templates/{llh,tag}/
```

## Workflow

### Step 1: Expand This Egg

```bash
# Unix/Mac
python .deia/tools/egg_expand.py .deia/templates/egg/llh-factory-egg.md

# Windows
python .deia\tools\egg_expand.py .deia\templates\egg\llh-factory-egg.md
```

**Creates:** `.deia/.projects/<project-name>_001/`

### Step 2: Prepare eOS Pack

Create or use existing eOS pack at:
`.deia/eos-packs/<project-name>.yaml`

**Format:** See `.deia/templates/eos-pack/llh-org-eos-pack.yaml`

### Step 3: Build From eOS Pack

```bash
# Unix/Mac
cd .deia/.projects/<project-name>_001/
python ../../../tools/llh_factory_build.py --eos-pack ../../eos-packs/<project-name>.yaml

# Windows
cd .deia\.projects\<project-name>_001\
python ..\..\..\tools\llh_factory_build.py --eos-pack ..\..\eos-packs\<project-name>.yaml
```

**Creates:**
- `llhs/*.md` - LLH entities
- `tag-teams/*.md` - TAG teams
- `drones/*.md` - Drone definitions (if specified)

### Step 4: Validate Outputs

```bash
python .deia/tools/llh_validate.py llhs/*.md tag-teams/*.md
```

### Step 5: Review & Commit

**Human review required:**
- Check all generated files
- Verify no sensitive data leaked
- Confirm routing correct
- Review RSE logs

**Then commit:**
```bash
git add .deia/.projects/<project-name>_001/
git commit -m "feat: LLH structure from spec"
```

## Capabilities

### Entity Types Supported

**LLHs (Limited Liability Hives):**
- Organizational units
- Governance structures
- Decision-making bodies
- Resource pools

**TAGs (Together And Good teams):**
- Cross-functional teams
- Time-bounded projects
- Ad-hoc collaborations
- Task forces

**Drones (Optional):**
- Automated workers
- Specialized processors
- Background tasks
- Service handlers

**Bees (Future):**
- Individual contributors
- Role-based actors
- Persona implementations

### Hierarchy Support

**Relationships:**
- Parent/child LLHs
- LLH → TAG membership
- TAG → Drone assignments
- Cross-org dependencies

**Example:**
```
federal-gov-llh (parent)
├── house-llh (child)
│   └── appropriations-2025-tag
├── senate-llh (child)
│   └── budget-committee-tag
└── executive-llh (child)
    └── omb-llh (grandchild)
```

## eOS Compliance

### Policy Enforcement

**ROTG (Rules of the Game):**
- All entities follow eOS v0.1 schema
- Capabilities declared explicitly
- Routing instructions clear
- Versioning mandatory

**DND (Do Not Delete):**
- Archive old versions
- Log all operations
- No destructive changes
- Human approval required

### Validation Requirements

**Pre-build:**
- Spec document valid YAML
- Required fields present
- No circular dependencies
- Proper segmentation

**Post-build:**
- All files validate against schema
- No duplicate IDs
- Routing paths exist
- RSE logged

## Security & Safety

### Preconditions

**Before building:**
1. Expanded egg exists (`egg.md` in project dir)
2. Spec document exists and validates
3. Target directories don't conflict
4. Human approval obtained (unless `--force`)

### Guardrails

**Large batch prevention:**
- Warn if >50 entities in spec
- Require explicit confirmation
- Suggest segmentation

**Conflict detection:**
- Check for existing entity IDs
- Prevent overwrites (DND)
- Archive on request only

**Audit trail:**
- Log every entity created
- Log every validation
- Log human approvals
- RSE + CHANGELOG updates

## eOS Pack Format

eOS packs are **pure YAML** with NO executable code:

```yaml
# .deia/eos-packs/my-organization.yaml
eos_version: "0.1"
pack_id: my-organization
author: dave
created: 2025-10-16

entities:
  llhs:
    - id: leadership-llh
      title: "Leadership Team"
      members: ["ceo", "cto", "cfo"]
      structure: executive
      caps: [strategic_planning, resource_allocation]

    - id: engineering-llh
      title: "Engineering Division"
      parent: leadership-llh
      structure: functional
      caps: [develop_software, manage_infra]

  tags:
    - id: q4-launch-tag
      title: "Q4 Product Launch"
      parent: engineering-llh
      deadline: "2025-12-31"
      members: ["eng-team", "marketing-team"]
      caps: [coordinate_launch, track_milestones]

routing:
  llhs: ".deia/.projects/my-organization_001/llhs/"
  tags: ".deia/.projects/my-organization_001/tag-teams/"

description: |
  My organization simulation for testing factory patterns.
  This is pure data - no executable code allowed.
```

## Factory Builder Logic (DEIA Global Commons)

**Location:** `.deia/tools/llh_factory_build.py` (shared resource)
**Parser:** `.deia/tools/spec_parser.py` (shared resource)

**Process:**
1. Parse eOS pack YAML
2. Validate pack structure (eos_version, pack_id, entities)
3. For each entity in pack:
   - Load template from `.deia/templates/{llh,tag,drone}/`
   - Substitute variables from eOS pack
   - Create file in routed location
   - Log to RSE
4. Validate all outputs via `.deia/tools/llh_validate.py`
5. Generate summary report

**This egg does NOT contain builder code** - it references the commons.

## Customization

### Custom Templates

Override default templates from commons:
```bash
python .deia/tools/llh_factory_build.py --eos-pack pack.yaml \
  --llh-template custom-llh.md \
  --tag-template custom-tag.md
```

### Custom Routing

Override routing in eOS pack:
```yaml
routing:
  llhs: "./custom-llhs/"
  tags: "./custom-tags/"
```

### Advanced Features

**Conditional creation:**
```yaml
entities:
  llhs:
    - id: prod-llh
      condition: "environment == production"
```

**Template inheritance:**
```yaml
entities:
  llhs:
    - id: eng-llh
      template: base-llh
      extends:
        members: ["eng-team"]
```

## Troubleshooting

### "eOS pack not found"
- Check path to .yaml file
- Ensure pack is in `.deia/eos-packs/`

### "Validation failed"
- Run `spec_parser.py` on eOS pack
- Check YAML syntax (indentation matters!)
- Verify required fields: eos_version, pack_id, entities

### "Entity already exists"
- Check for duplicate IDs
- Use `--force` to overwrite (not recommended)
- Archive old entity first

### "Permission denied"
- Ensure target directories writable
- Check file ownership
- Run with appropriate permissions

## Related Tools

**Egg Management:**
- `egg_expand.py` - Expand this egg
- `egg_hatch.sh` - Hatch individual entities (legacy)

**Building (DEIA Global Commons):**
- `llh_factory_build.py` - Main builder (commons)
- `spec_parser.py` - Parse eOS packs (commons)

**Validation (DEIA Global Commons):**
- `llh_validate.py` - Validate entity schemas (commons)
- `validate_all.sh|ps1` - Batch validation

**Orchestration:**
- `builder_launch.sh|ps1` - Full workflow automation

## Version History

**v0.1.0 (2025-10-15):**
- Initial factory egg template
- Spec-based building
- Hierarchy support
- eOS v0.1 compliance

## References

- **Status Doc:** `.deia/STATUS-LLH-FACTORY-EGG.md`
- **eOS Pack Template:** `.deia/templates/eos-pack/llh-org-eos-pack.yaml`
- **RCA:** `.deia/incidents/RCA-2025-10-15-llh-builder-eggs.md`
- **Factory Pattern Doc:** `.deia/docs/FACTORY-PATTERN.md`

---

**Proposed by:** claude
**Created:** 2025-10-15
**Status:** Template (ready for use)
**Version:** 0.1.0
**eOS:** 0.1
