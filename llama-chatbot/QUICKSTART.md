# DEIA Chat Interface - Quick Start

## Current Status

**Phase 1 (Basic Chat):** ✅ Complete
**Phases 2-4:** ❌ Not started

See `STATUS.md` for detailed implementation status and roadmap.

## What Works Now

- ✅ Chat with local Ollama LLM
- ✅ Real-time streaming responses
- ✅ Basic command execution (`!dir`, `!ls`, etc.)
- ✅ Conversation history
- ✅ Multiple LLM providers (Ollama/DeepSeek/OpenAI)

## What Doesn't Work Yet

- ❌ DEIA project awareness
- ❌ File reading/writing through chat
- ❌ Integration with .deia structure
- ❌ Project file browser
- ❌ Secure file modifications

## Quick Start

### Prerequisites

1. **Install Ollama:**
   ```bash
   # Visit https://ollama.com/
   # Or on Linux/macOS:
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull a model:**
   ```bash
   ollama pull qwen2.5-coder:7b
   ```

3. **Start Ollama:**
   ```bash
   ollama serve
   ```

### Running the Chat Interface

1. **Install dependencies:**
   ```bash
   cd llama-chatbot
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python app.py
   ```

3. **Open browser:**
   ```
   http://localhost:8000
   ```

## Usage

### Basic Chat
Type messages and get responses from the LLM.

### Direct Commands
Prefix commands with `!` to execute them:
```
!dir
!ls -la
!git status
```

**Allowed commands:** ls, cat, grep, find, python, git, pip, pytest, tree, dir, cd, pwd, type, findstr, echo, mkdir, rmdir, del, copy, move

### Environment Variables

- `MODEL_NAME` - Model to use (default: `qwen2.5-coder:7b`)
- `LLAMA_ENDPOINT` - Ollama endpoint (default: `http://localhost:11434`)
- `MAX_TOKENS` - Max response tokens (default: `2048`)
- `TEMPERATURE` - Sampling temperature (default: `0.7`)

**Example:**
```bash
export MODEL_NAME="deepseek-coder-v2:16b"
python app.py
```

## API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Real-time chat with streaming

### REST API
- `GET /` - Web UI
- `GET /api/health` - Health check
- `POST /api/chat` - Non-streaming chat
- `POST /api/execute` - Execute command

## Architecture

```
app.py (FastAPI server)
  ├── WebSocket endpoint (/ws)
  │   └── Streaming chat with LLM
  ├── REST endpoints (/api/*)
  │   ├── /api/chat - Non-streaming
  │   ├── /api/execute - Commands
  │   └── /api/health - Status
  └── LLM Service (llm_service.py)
      ├── OllamaService (local)
      ├── DeepSeekService (cloud)
      └── OpenAIService (cloud)
```

## Documentation

- **STATUS.md** - Detailed implementation status and plan
- **README_SERVICE.md** - LLM service API reference
- **IMPROVEMENTS.md** - Changelog and what was improved
- **MIGRATION_SUMMARY.md** - Migration from old service

## Next Steps (Planned)

**Phase 2:** DEIA Project Awareness (8-10 hours)
- Auto-load .deia context
- File reading capabilities
- Project structure browser

**Phase 3:** File Modifications (12-15 hours)
- Safe file writing with confirmation
- Diff viewer
- Audit logging

**Phase 4:** Polish (6-12 hours)
- Better UI/UX
- Keyboard shortcuts
- Session persistence

See `STATUS.md` for detailed roadmap.

## Troubleshooting

### "Connection error" or "Ollama not responding"
- Make sure Ollama is running: `ollama serve`
- Check the endpoint: `curl http://localhost:11434/api/tags`

### "Model not found"
- Pull the model: `ollama pull qwen2.5-coder:7b`
- List available models: `ollama list`

### WebSocket disconnects
- Check browser console for errors
- Verify firewall isn't blocking localhost:8000
- Try refreshing the page

### Import errors
- Install dependencies: `pip install -r requirements.txt`
- Check you're in the right directory: `cd llama-chatbot`

## Contributing

This project follows the LLH specification in:
`.deia/.projects/simulation_004/gpt-llama-bot-eos-companion.md`

Before contributing:
1. Read the LLH spec
2. Check STATUS.md for current priorities
3. Understand security requirements
4. Follow DEIA principles (DND, ROTG)

## Security

**Current security:**
- Localhost-only by default
- Command whitelist
- Basic path restrictions

**Planned security (Phase 2-3):**
- Project boundary enforcement
- File modification confirmations
- Audit logging
- Directory traversal prevention
- Read-only mode toggle

## License

Same as DEIA project.

---

**Last Updated:** 2025-10-15
**Status:** Phase 1 complete, Phase 2 planned
**Next Review:** 2025-10-16
