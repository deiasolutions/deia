# DEIA Project Configuration

**Project:** chromium-deia (Chromium/Chrome browser extension for DEIA)
**Auto-logging:** Enabled
**Mode:** end-user

## What This Project Is

A Chromium/Chrome browser extension that integrates DEIA (Distributed Expertise & Intelligence Archive) into the browser environment. This extension enables conversation logging, pattern capture, and knowledge sharing for browser-based AI interactions.

## Project Structure

```
chromium-deia/
├── .claude/              # Claude Code integration
├── .deia/                # DEIA configuration
│   ├── config.json       # Project settings
│   └── sessions/         # Conversation logs
├── manifest.json         # Chrome extension manifest
├── src/                  # Extension source code
├── icons/                # Extension icons
└── project_resume.md     # Session continuity
```

## Development Preferences

- Follow Chrome Extension Manifest V3 standards
- Use modern JavaScript (ES6+) or TypeScript
- Test in Chrome/Chromium before deploying
- Maintain privacy-first architecture (no external data transmission)
- Log major development decisions to DEIA sessions

## Related Projects

- **vscode-deia**: VS Code extension (sibling project in `../vscode-deia/`)
- **deia-core**: Python CLI and core library (`../../src/deia/`)
