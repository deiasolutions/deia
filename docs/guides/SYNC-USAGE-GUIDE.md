# Sync Usage Guide

**Route markdown documents from Downloads to project folders automatically.**

The `deia sync` command watches your Downloads folder for markdown files with DEIA routing headers and automatically routes them to the correct project location.

---

## Quick Start

```bash
# Watch Downloads folder interactively (Ctrl+C to stop)
deia sync

# Process existing files once and exit
deia sync --once
```

---

## How It Works

1. You download or save a markdown file to your Downloads folder
2. The file contains a YAML frontmatter with `deia_routing` information
3. DEIA Sync routes the file to the specified project and destination folder
4. The file is copied (not moved) for safety - original stays in temp staging

### Flow Diagram

```
Downloads/my-doc.md
  ↓ (detected)
.deia-staging/my-doc.md  (temp staging)
  ↓ (copy)
project/docs/my-doc.md   (final destination)
```

---

## Document Format

Add YAML frontmatter to your markdown files:

```yaml
---
title: My Document
version: 1.0
deia_routing:
  project: deiasolutions
  destination: docs/guides
---

# My Document Content

Your markdown content here...
```

### Required Fields

| Field | Description |
|-------|-------------|
| `deia_routing.project` | Project name (must match config) |
| `deia_routing.destination` | Target folder within project (optional, defaults to `docs`) |

### Optional Fields

| Field | Description |
|-------|-------------|
| `version` | Semantic version (e.g., `1.0`, `2.1.3`) |
| `replaces` | Version history for tracking |

---

## Configuration

### Project Configuration

Add projects to `~/.deia/config.json`:

```json
{
  "projects": {
    "deiasolutions": "C:/Users/you/GitHub/deiasolutions",
    "myproject": "C:/Users/you/GitHub/myproject"
  },
  "sync": {
    "downloads_folder": "C:/Users/you/Downloads",
    "default_destination": "docs"
  }
}
```

### Sync Settings

```json
{
  "sync": {
    "downloads_folder": "C:/Users/you/Downloads",
    "default_destination": "docs",
    "temp_staging_folder": "C:/Users/you/Downloads/.deia-staging",
    "processing": {
      "use_temp_staging": true,
      "cleanup_policy": "manual"
    }
  }
}
```

---

## Command Options

```bash
deia sync [OPTIONS]

Options:
  --once     Process existing files and exit (one-time scan)
  --daemon   Run as background daemon (coming soon)
  --config   Custom routing config file path
```

### Examples

```bash
# Interactive mode - watches for new files
deia sync

# One-time scan - process existing files then exit
deia sync --once

# Use custom config file
deia sync --config /path/to/custom-config.json
```

---

## Features

### Safe Temp Staging

Files are copied (not moved) when temp staging is enabled:
- Original remains in `.deia-staging/` until manually cleaned
- Easy recovery if routing goes wrong
- No data loss during testing

### Version Tracking

DEIA Sync tracks document versions:

```yaml
---
version: 2.0
replaces:
  - version: 1.0
    status: submitted
---
```

**Gap Detection:** Warns if versions are skipped (e.g., v1.0 → v3.0)

**Draft Tracking:** Tracks unsubmitted drafts:
```yaml
replaces:
  - version: 1.5
    status: unsubmitted-draft
```

### Conflict Resolution

If a file with the same name exists at the destination:
- Timestamp is added automatically (e.g., `doc_20251126_235959.md`)
- Original file preserved
- Warning logged

### State Persistence

DEIA Sync remembers:
- Last run timestamp
- Processed files list
- Error counts

State is stored in `~/.deia/sync/state.json`

---

## Startup Report

When running `deia sync --once`, you'll see a startup report:

```
============================================================
DEIA Sync - Startup Report
============================================================
Last run: 2h 30m ago (2025-11-26 21:00:00 UTC)
Found 3 new .md files in Downloads

Files to process:
  - project-spec-v2.0.md
  - meeting-notes.md
  - api-design.md

All-time stats:
  Processed: 47 files
  Errors: 2 files
============================================================
```

---

## Manual Cleanup

Phase 1 does NOT auto-delete from temp staging. To clean up:

```bash
# Review what's in temp staging
ls ~/Downloads/.deia-staging/

# Verify files are committed to git in projects
cd ~/GitHub/deiasolutions
git status

# If all is well, clean temp staging
deia cleanup-temp-staging

# Or manually delete
rm -rf ~/Downloads/.deia-staging/*
```

---

## Troubleshooting

### File Not Routing

1. **Check frontmatter:** Must have `deia_routing` section
2. **Check project name:** Must match a project in config
3. **Check file extension:** Must be `.md`

### Unknown Project Error

Add the project to `~/.deia/config.json`:

```json
{
  "projects": {
    "your-project": "/path/to/your-project"
  }
}
```

### Version Gap Warning

This is informational - the file still routes. It warns when intermediate versions may be missing.

---

## Best Practices

1. **Use consistent project names** across all documents
2. **Include version numbers** in frontmatter for tracking
3. **Enable temp staging** for safety during development
4. **Review temp folder** before cleanup
5. **Commit routed files to git** before cleaning temp

---

## Next Steps

- [Conversation Logging Guide](CONVERSATION-LOGGING-GUIDE.md) - Log your AI sessions
- [BOK Usage Guide](BOK-USAGE-GUIDE.md) - Search community patterns
- [Pattern Submission Guide](PATTERN-SUBMISSION-GUIDE.md) - Contribute discoveries

---

**Questions?** File an issue at https://github.com/deiasolutions/deia/issues
