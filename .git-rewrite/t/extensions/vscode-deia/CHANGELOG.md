# Change Log

All notable changes to the DEIA VSCode extension will be documented in this file.

## [Unreleased]

### Added
- Initial extension scaffold
- DEIA project detection
- Manual conversation logging
- Status bar integration
- `@deia` chat participant
- SpecKit integration (conversation → spec)
- SpecKit constitution updates
- Command palette integration
- Auto-log toggle

### In Progress
- Pattern extraction UI
- PII detection
- GitHub BOK submission
- Auto-logging (file monitoring)

## [0.1.0] - 2025-10-07

### Added
- Initial release
- Core logging functionality
- SpecKit integration
- Chat participant
- Basic commands

### Known Issues
- Auto-logging not yet implemented
- Pattern extraction UI not yet built
- BOK search not available
- No automated tests yet

---

## Release Notes

### 0.1.0

**First Release - Core Logging + SpecKit Integration**

This initial release focuses on manual conversation logging and innovative SpecKit integration.

**Features:**
- ✅ Detect DEIA-enabled projects
- ✅ Manual conversation logging
- ✅ Status bar indicator
- ✅ `@deia` chat commands
- ✅ Create SpecKit specs from conversations
- ✅ Update SpecKit constitution from decisions
- ✅ View session logs
- ✅ Read project resume
- ✅ Toggle auto-log (config only, monitoring not implemented)

**What's Next:**
- Pattern extraction and sharing
- Automatic logging (file monitoring)
- BOK search and discovery
- Automated tests

**Requirements:**
- VSCode 1.85.0 or higher
- DEIA CLI installed (`pip install -e path/to/deia`)
- Project initialized with `deia init`

**Optional:**
- GitHub SpecKit for spec-driven development workflow
