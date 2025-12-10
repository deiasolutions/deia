---
title: DEIA Sandbox Structure
version: 0.1.0
date: 2025-10-16
author: Claude (Anthropic)
status: specification
policy: DND
---

# DEIA Sandbox Structure

## Purpose

Separate **production DEIA work** from **experimental/personal projects** to prevent:
- Accidental commits of private content
- PII exposure in public repos
- Mixing experiments with production code
- Cluttering git history with WIP experiments

## Standard DEIA Directory Structure

```
project-root/
├── .deia/                          # DEIA core (PUBLIC, version controlled)
│   ├── tools/                      # Commons tools (committed)
│   ├── templates/                  # Entity templates (committed)
│   ├── eos-packs/                  # Project blueprints (committed, review for PII)
│   ├── .projects/                  # Built organizations (committed after review)
│   ├── telemetry/                  # RSE logs (committed)
│   ├── commons/                    # Shared docs (committed)
│   ├── docs/                       # Documentation (committed)
│   ├── incidents/                  # RCAs (committed)
│   │
│   ├── .sandbox/                   # PRIVATE experiments (.gitignored)
│   ├── .experiments/               # PRIVATE experiments (.gitignored)
│   ├── .private/                   # PRIVATE content (.gitignored)
│   └── .local/                     # Machine-specific (.gitignored)
│
├── .simulations/                   # Official simulations (PUBLIC, committed)
│   ├── federal-gov-2025/          # Production simulation
│   ├── startup-org-simulation/    # Production simulation
│   └── README.md                  # Simulation index
│
└── .sandbox/                       # Top-level sandbox (PRIVATE, .gitignored)
    ├── experiments/               # Personal experiments
    ├── games/                     # Game projects (flappy-bird, etc.)
    ├── prototypes/                # Proof of concepts
    ├── learning/                  # Learning projects
    └── README.md                  # Sandbox usage guide
```

## Directory Purposes

### PUBLIC Directories (Version Controlled)

#### `.deia/tools/`
**Purpose:** DEIA Global Commons builder tools
**Content:** Python scripts for factory, parser, validator
**Commit:** YES, always
**Review:** Check for hardcoded paths with usernames

#### `.deia/templates/`
**Purpose:** Entity templates (LLH, TAG, egg, eOS pack)
**Content:** Markdown and YAML templates
**Commit:** YES, always
**Review:** Check for example data with PII

#### `.deia/eos-packs/`
**Purpose:** Project blueprints for organizations
**Content:** YAML files defining entities
**Commit:** YES, but review first
**Review:** Check for:
- Real person names (use placeholder names)
- Company-specific info
- Sensitive org structures

#### `.deia/.projects/`
**Purpose:** Built organizational entities
**Content:** Generated LLH/TAG markdown files
**Commit:** AFTER REVIEW
**Review:** Check generated content for PII

#### `.deia/telemetry/`
**Purpose:** RSE event logs
**Content:** rse.jsonl (append-only log)
**Commit:** YES, if no PII
**Review:** Check logs for usernames, paths, sensitive events

#### `.deia/commons/`
**Purpose:** Shared documentation, CHANGELOG
**Content:** Documentation files
**Commit:** YES, always
**Review:** Check for PII in CHANGELOG

#### `.simulations/`
**Purpose:** Official, production-ready simulations
**Content:** Completed simulation results, analysis
**Commit:** YES, after completion and review
**Review:** Sanitize any real data

### PRIVATE Directories (NOT Version Controlled)

#### `.deia/.sandbox/`
**Purpose:** Quick experiments within DEIA context
**Content:** Test eOS packs, experimental builds, WIP
**Commit:** NO, .gitignored
**Examples:**
- `.deia/.sandbox/test-idea.yaml`
- `.deia/.sandbox/experiment-llh/`

#### `.deia/.experiments/`
**Purpose:** Longer-running experimental features
**Content:** Feature prototypes, alternative implementations
**Commit:** NO, until ready to promote
**Examples:**
- `.deia/.experiments/new-entity-type/`
- `.deia/.experiments/alternative-parser/`

#### `.deia/.private/`
**Purpose:** Sensitive content, personal notes
**Content:** API keys, credentials, personal docs
**Commit:** NO, never
**Examples:**
- `.deia/.private/api-keys.txt`
- `.deia/.private/meeting-notes.md`

#### `.deia/.local/`
**Purpose:** Machine-specific config, temp files
**Content:** Local overrides, cache, temp data
**Commit:** NO, machine-specific
**Examples:**
- `.deia/.local/cache/`
- `.deia/.local/config-override.yaml`

#### `.sandbox/` (root level)
**Purpose:** Completely separate personal projects
**Content:** Games, learning projects, prototypes
**Commit:** NO, keep in separate repos if needed
**Examples:**
- `.sandbox/flappy-bird-ai/`
- `.sandbox/games/`
- `.sandbox/llama-experiments/`

## Migration Plan

### Step 1: Create Sandbox Structure

```bash
# Create DEIA private directories
mkdir -p .deia/{.sandbox,.experiments,.private,.local}

# Create top-level sandbox
mkdir -p .sandbox/{experiments,games,prototypes,learning}

# Create simulations directory
mkdir -p .simulations
```

### Step 2: Move Existing Experiments

```bash
# Move games to sandbox
mv flappy-bird-ai/ .sandbox/games/
mv games/ .sandbox/

# Move experiments
mv experiments/ .sandbox/experiments/

# Move private content
mv quantumdocs/ .deia/.private/
mv .davedrop/ .deia/.private/
mv .embargo/ .deia/.private/

# Move services (may contain credentials)
mv services/ .sandbox/experiments/

# Move LLM experiments
mv llama-chatbot/ .sandbox/experiments/
```

### Step 3: Update .gitignore

Add to `.gitignore`:
```gitignore
# DEIA private directories
.deia/.sandbox/
.deia/.experiments/
.deia/.private/
.deia/.local/

# Top-level sandbox
.sandbox/

# Personal experiments (if not moved yet)
/flappy-bird-ai/
/games/
/experiments/
/quantumdocs/

# Private dropboxes
/.davedrop/
/.embargo/

# Services (may contain credentials)
/services/

# LLM experiments
/llama-chatbot/.env
/llama-chatbot/config.ini
/llama-chatbot/credentials/

# Build artifacts
.coverage
*.pyc
__pycache__/
.pytest_cache/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
nul

# Temp
*.tmp
*.log
test_transcript.txt
```

## Sandbox Usage Guidelines

### When to Use .deia/.sandbox/

**Use for:**
- Quick test eOS packs
- Experimenting with entity structures
- Testing factory builder changes
- Trying new workflow ideas

**Example:**
```bash
# Test a crazy idea
cat > .deia/.sandbox/weird-structure.yaml << 'EOF'
---
eos_version: "0.1"
pack_id: crazy-test
entities:
  llhs:
    - id: recursive-llh
      parent: recursive-llh  # Circular reference test!
---
EOF

# Try to build (will fail validation, but safe to test)
python .deia/tools/llh_factory_build.py --eos-pack .deia/.sandbox/weird-structure.yaml --dry-run
```

### When to Use .deia/.experiments/

**Use for:**
- Multi-day experimental features
- Alternative implementations
- Research projects

**Example:**
```bash
# Working on new entity type (Bee)
mkdir .deia/.experiments/bee-entity/
cp .deia/templates/llh/minimal-llh.md .deia/.experiments/bee-entity/bee-template.md
# Modify and test...
```

### When to Use .sandbox/ (root)

**Use for:**
- Completely separate projects
- Learning exercises
- Games, prototypes
- Anything not DEIA-related

**Example:**
```bash
# Flappy bird AI experiment
cd .sandbox/games/flappy-bird-ai/
python main.py
```

### Promoting from Sandbox to Production

When an experiment is ready:

```bash
# 1. Review content thoroughly
cat .deia/.sandbox/new-feature.yaml

# 2. Check for PII
grep -i "dave" .deia/.sandbox/new-feature.yaml
grep -i "api" .deia/.sandbox/new-feature.yaml

# 3. Move to production location
mv .deia/.sandbox/new-feature.yaml .deia/eos-packs/

# 4. Commit
git add .deia/eos-packs/new-feature.yaml
git commit -m "feat: add new feature eOS pack"
```

## Simulation vs Sandbox

### .simulations/ (Production)

**Purpose:** Official simulation runs with results

**Structure:**
```
.simulations/
├── federal-gov-2025/
│   ├── setup/
│   │   ├── scenario.yaml
│   │   └── initial-state.md
│   ├── results/
│   │   ├── run-001-output.md
│   │   └── metrics.json
│   └── analysis/
│       ├── findings.md
│       └── recommendations.md
└── README.md
```

**Commit:** YES, these are valuable results

### .sandbox/ (Experiments)

**Purpose:** Testing, learning, prototyping

**Structure:**
```
.sandbox/
├── experiments/
│   ├── test-simulation-1/    # Quick test
│   └── broken-idea/          # Failed experiment
├── games/
│   └── flappy-bird-ai/       # Personal project
└── learning/
    └── llm-basics/           # Learning exercise
```

**Commit:** NO, these are ephemeral

## Best Practices

### 1. Default to Sandbox
When in doubt, create in sandbox first.

### 2. Promote Deliberately
Move to production only when:
- Tested and working
- Reviewed for PII
- Documented
- Ready to share

### 3. Clean Regularly
```bash
# Review sandbox periodically
ls -la .sandbox/

# Delete failed experiments
rm -rf .sandbox/experiments/bad-idea/

# Promote successful ones
mv .sandbox/experiments/good-idea/ .deia/.projects/
```

### 4. Never Commit Sandbox
Always check `.gitignore` includes sandbox directories.

## Related Documents

- **RCA:** `.deia/incidents/RCA-2025-10-16-commit-process-breakdown.md`
- **Commit Guidelines:** `.deia/docs/COMMIT-GUIDELINES.md` (to be created)
- **Factory Egg:** `.deia/templates/egg/llh-factory-egg.md`

---

**Version:** 0.1.0
**Created:** 2025-10-16
**Author:** Claude (Anthropic, Bee Queen)
**Status:** Specification
