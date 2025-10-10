# DEIA Browser Extension (Chromium)

**Distributed Expertise & Intelligence Archive for Chromium-based browsers**

A browser extension that enables conversation logging, pattern capture, and knowledge sharing for browser-based AI interactions.

## Status

**Version:** 0.1.0 (Initial Development)

This is a new project in early development. Core structure is in place but conversation capture functionality is not yet implemented.

## Features (Planned)

- 📝 **Auto-logging**: Automatically capture AI conversations from supported tools
- 🎯 **Multi-tool support**: Works with Claude, ChatGPT, Gemini, and more
- 🔒 **Privacy-first**: All data stored locally, no external servers
- 📊 **Pattern extraction**: Extract reusable patterns from logged conversations
- 🌐 **Cross-browser**: Compatible with Chrome, Edge, Brave, and other Chromium browsers

## Supported AI Tools

- **Claude** (claude.ai)
- **ChatGPT** (chat.openai.com)
- **Gemini** (gemini.google.com)
- **Microsoft Copilot** (copilot.microsoft.com)

## Installation (Development)

1. Clone the DEIA repository:
   ```bash
   git clone https://github.com/deiasolutions/deia.git
   cd deia/extensions/chromium-deia
   ```

2. Load the extension in Chrome:
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `chromium-deia` directory

3. The DEIA icon should appear in your browser toolbar

## Usage

1. **Visit an AI tool** (Claude, ChatGPT, etc.)
2. **Have conversations** with the AI
3. **Click the DEIA icon** to log the current session
4. **View logs** in the extension settings

### Manual Logging

Click the DEIA icon and press "Log Current Session" to manually save a conversation.

### Auto-logging

Enable auto-logging in settings to automatically capture conversations as they happen.

## Project Structure

```
chromium-deia/
├── manifest.json         # Extension manifest (Manifest V3)
├── src/
│   ├── background.js     # Background service worker
│   ├── content.js        # Content script for page monitoring
│   ├── popup.html        # Extension popup UI
│   ├── popup.js          # Popup logic
│   ├── options.html      # Settings page
│   └── options.js        # Settings logic
├── icons/                # Extension icons (TODO)
├── .claude/              # Claude Code integration
│   ├── INSTRUCTIONS.md   # Auto-logging procedures
│   ├── commands/         # Slash commands
│   └── preferences/      # Project preferences
├── .deia/                # DEIA configuration
│   ├── config.json       # Project config
│   └── sessions/         # Conversation logs
└── README.md
```

## Development

### Requirements

- Chromium-based browser (Chrome, Edge, Brave, etc.)
- DEIA core library (in parent repository)
- Basic knowledge of Chrome Extensions Manifest V3

### Testing

1. Make changes to the extension code
2. Go to `chrome://extensions/`
3. Click the refresh icon on the DEIA extension card
4. Test in a supported AI tool page

### Contributing

This project follows DEIA governance and contribution guidelines. See the main repository's `CONTRIBUTING.md` for details.

## Architecture

- **Manifest V3**: Modern Chrome extension standard
- **Service Worker**: Background task handling
- **Content Scripts**: Page-level conversation monitoring
- **Storage API**: Local data persistence
- **Message Passing**: Communication between components

## Privacy & Security

- ✅ No external data transmission
- ✅ All data stored locally in browser
- ✅ User controls all logging
- ✅ No tracking or analytics
- ✅ Open source and auditable

## Roadmap

### Phase 1: Foundation (Current)
- [x] Basic extension structure
- [x] Manifest V3 setup
- [x] UI components (popup, options)
- [ ] Conversation capture implementation
- [ ] Local storage integration

### Phase 2: Integration
- [ ] DEIA core library integration
- [ ] File system access for session logs
- [ ] Pattern extraction
- [ ] Export functionality

### Phase 3: Multi-tool Support
- [ ] Tool-specific conversation parsers
- [ ] Universal conversation format
- [ ] Cross-tool pattern recognition

### Phase 4: Advanced Features
- [ ] Real-time auto-logging
- [ ] Smart pattern suggestions
- [ ] Collaboration features
- [ ] Cloud sync (optional, privacy-first)

## Related Projects

- **deia-core**: Python CLI and core library
- **vscode-deia**: VS Code extension for DEIA

## License

MIT License - see main repository for details

## Support

- **Issues**: https://github.com/deiasolutions/deia/issues
- **Discussions**: https://github.com/deiasolutions/deia/discussions
- **Documentation**: https://github.com/deiasolutions/deia

---

**Built with DEIA governance principles - privacy-first, community-driven, knowledge commons**
