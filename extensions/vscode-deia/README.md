# DEIA - AI Conversation Logger for VSCode

**Never lose context.** Log AI conversations, recover from crashes, contribute to the knowledge commons.

## Features

### 🔒 Local-First Logging
- Automatically detect DEIA-enabled projects
- Log conversations from any chat extension (Copilot, Continue, Cody, etc.)
- Crash recovery - resume from where you left off
- Privacy-first - all logs stay local

### 📐 SpecKit Integration
- Convert DEIA conversation logs into SpecKit specifications
- Extract requirements, decisions, and architecture from conversations
- Add conversation decisions to SpecKit constitution
- Bridge conversation logging with spec-driven development

### 💬 @deia Chat Participant
Use `@deia` in any chat to:
- `@deia log` - Log the current conversation
- `@deia status` - Check DEIA configuration
- `@deia help` - Get help

### ⌨️ Command Palette
- `DEIA: Log Current Chat` - Save conversation
- `DEIA: View Session Logs` - Browse past sessions
- `DEIA: Read Project Resume` - See latest context
- `DEIA: Check Status` - View configuration
- `DEIA: Toggle Auto-Logging` - Enable/disable auto-log

### 📊 Status Bar
Shows DEIA status at a glance:
- `DEIA: Auto-log ON` - Recording conversations automatically
- `DEIA: Manual` - Manual logging mode

## Requirements

1. **DEIA CLI installed:**
   ```bash
   git clone https://github.com/deiasolutions/deia.git
   cd deia
   pip install -e .
   ```

2. **Initialize DEIA in your project:**
   ```bash
   cd /path/to/your/project
   deia install
   deia init
   ```

## Usage

### Step 1: Initialize Project
Run in your project directory:
```bash
deia init
```

### Step 2: Start Coding
Open your project in VSCode. The DEIA extension will automatically detect the `.deia/` directory.

### Step 3: Log Conversations
**Option A - Use @deia:**
```
@deia log
```

**Option B - Command Palette:**
- Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
- Type "DEIA: Log Current Chat"

**Option C - Auto-logging:**
- Enable auto-logging: `DEIA: Toggle Auto-Logging`
- Conversations are logged automatically

### Step 4: Never Lose Context
If VSCode crashes, your conversations are safe in `.deia/sessions/`. Use `project_resume.md` to see where you left off.

### Step 5: SpecKit Integration (Optional)
If you use GitHub SpecKit for spec-driven development:

1. **Initialize SpecKit in your project:**
   ```bash
   specify init
   ```

2. **Create specs from conversations:**
   - Run `DEIA: Create SpecKit Spec from Conversation`
   - Select a logged conversation
   - Name the spec

3. **Update SpecKit constitution:**
   - Run `DEIA: Add Decisions to SpecKit Constitution`
   - Select a conversation with key decisions
   - Review and add to `.specify/memory/constitution.md`

**Benefits:**
- Conversations become specifications
- Decisions automatically captured in project principles
- Seamless bridge between chat and spec-driven development

## Extension Settings

- `deia.deiaCliPath`: Path to DEIA CLI (default: `deia`)
- `deia.autoDetect`: Auto-detect DEIA projects (default: `true`)
- `deia.showStatusBar`: Show DEIA in status bar (default: `true`)

## How It Works

### Tier 1: Local Logging (No GitHub needed)
- Log conversations locally
- Recover from crashes
- Build personal knowledge base
- **No sign-in required**

### Tier 2: Read Community Patterns (No GitHub needed)
- Browse community-contributed patterns
- Search for solutions
- **No sign-in required**

### Tier 3: Contribute Patterns (GitHub account)
- Submit sanitized patterns to the community
- **Requires GitHub account** (free)

## Privacy

- **Local-first:** All logs stay on your machine
- **Opt-in sharing:** You choose what to contribute
- **Sanitization required:** PII/secrets removed before sharing
- **No telemetry:** Extension doesn't phone home

## Commands

| Command | Description |
|---------|-------------|
| `DEIA: Log Current Chat` | Save current conversation |
| `DEIA: View Session Logs` | Open sessions directory |
| `DEIA: Read Project Resume` | View project context |
| `DEIA: Check Status` | Show configuration |
| `DEIA: Submit Pattern` | Share with community (coming soon) |
| `DEIA: Toggle Auto-Logging` | Enable/disable auto-log |
| `DEIA: Create SpecKit Spec from Conversation` | Generate spec from logged conversation |
| `DEIA: Add Decisions to SpecKit Constitution` | Update SpecKit principles from conversation |

## Troubleshooting

### "DEIA CLI not found"
Install DEIA:
```bash
pip install -e /path/to/deia
```

### "No DEIA-enabled workspace"
Initialize DEIA in your project:
```bash
cd /path/to/your/project
deia init
```

### Check Installation
Run diagnostic:
```bash
deia doctor
```

## Contributing

See [CONTRIBUTING.md](https://github.com/deiasolutions/deia/blob/master/CONTRIBUTING.md)

## License

MIT - See [LICENSE](https://github.com/deiasolutions/deia/blob/master/LICENSE)

## More Information

- [DEIA GitHub](https://github.com/deiasolutions/deia)
- [Documentation](https://github.com/deiasolutions/deia/docs)
- [Report Issues](https://github.com/deiasolutions/deia/issues)
- [Community Patterns](https://github.com/deiasolutions/deia/tree/master/bok)

**Built for humanity. Privacy-first. Community-owned.**
