# DEIA Chat Interface

Web-based chat interface for interacting with DEIA projects using local LLMs (Ollama).

## 📊 Current Status

**Phase:** 1 of 4 (Basic Chat) ✅ Complete
**Progress:** 14% by effort, 25% by phase
**Last Updated:** 2025-10-15

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: Basic Chat | ✅ Complete | 100% |
| Phase 2: File Operations | ⏳ Planned | 0% |
| Phase 3: File Modifications | ⏳ Planned | 0% |
| Phase 4: Polish | ⏳ Planned | 0% |

## 🚀 Quick Start

### Prerequisites
```bash
# Install and start Ollama
ollama pull qwen2.5-coder:7b
ollama serve
```

### Run the Chat Interface
```bash
cd llama-chatbot
pip install -r requirements.txt
python app.py
```

Open browser: http://localhost:8000

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 📚 Documentation

**Start Here:**
- **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
- **[STATUS.md](STATUS.md)** - Detailed implementation status and plan

**Deep Dives:**
- **[ROADMAP_SUMMARY.md](ROADMAP_SUMMARY.md)** - Phase overview and timeline
- **[README_SERVICE.md](README_SERVICE.md)** - LLM service API reference
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - What was improved from old service
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** - Service migration details

**Specifications:**
- **[LLH Spec](../.deia/.projects/simulation_004/gpt-llama-bot-eos-companion.md)** - Original specification
- **[Main Roadmap](../ROADMAP.md)** - DEIA project roadmap (Phase 2.5)

## ✨ What Works Now

- ✅ **Chat with local LLM** - Ollama integration with streaming
- ✅ **Multiple providers** - Ollama, DeepSeek, OpenAI support
- ✅ **Real-time streaming** - See responses as they're generated
- ✅ **Conversation history** - Auto-managed with token awareness
- ✅ **Basic commands** - Execute safe shell commands
- ✅ **Retry logic** - Automatic retry with exponential backoff
- ✅ **Error handling** - Comprehensive error categorization

## 🔜 Coming Soon

- ⏳ **DEIA awareness** - Understand .deia project structure
- ⏳ **File operations** - Read files with syntax highlighting
- ⏳ **File browser** - Browse project structure
- ⏳ **File modifications** - Safe file writing with confirmation
- ⏳ **Audit logging** - Track all operations
- ⏳ **Better UI** - Professional styling and UX

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│          Frontend (Browser)              │
│  ┌────────────┐      ┌────────────┐    │
│  │ Chat UI    │      │ WebSocket  │    │
│  └────────────┘      └────────────┘    │
└─────────────────────────────────────────┘
              ↓                ↑
┌─────────────────────────────────────────┐
│         Backend (FastAPI)                │
│  ┌────────────────────────────────────┐ │
│  │  WebSocket Handler                 │ │
│  │  - Streaming chat                  │ │
│  │  - Conversation history            │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  LLM Service (llm_service.py)     │ │
│  │  - OllamaService                   │ │
│  │  - DeepSeekService                 │ │
│  │  - OpenAIService                   │ │
│  │  - Retry logic                     │ │
│  │  - History management              │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
              ↓                ↑
┌─────────────────────────────────────────┐
│           Ollama (Local LLM)             │
│         http://localhost:11434           │
└─────────────────────────────────────────┘
```

## 🛡️ Security

**Current:**
- ✅ Localhost-only by default
- ✅ Command whitelist
- ✅ Basic path restrictions

**Planned (Phase 2-3):**
- ⏳ Project boundary enforcement
- ⏳ File modification confirmations
- ⏳ Audit logging
- ⏳ Directory traversal prevention
- ⏳ Read-only mode toggle

## 🎯 Goals (from LLH Spec)

Create a secure, user-friendly web interface that enables:
- Full file system operations within DEIA project boundaries
- Real-time chat with local LLM (Ollama)
- File modification capabilities with confirmation workflows
- Integration with DEIA project structure and specifications

## 📋 Success Criteria

### Functional Requirements
- ✅ Basic chat interface operational
- ⏳ File reading capabilities implemented
- ⏳ File modification with confirmation workflow
- ⏳ Project structure integration
- ✅ Real-time streaming responses

### Security Requirements
- ⏳ Project directory boundary enforcement
- ⏳ File modification confirmation system
- ⏳ Audit logging implementation
- ✅ Localhost-only access by default
- ✅ Session management

### Performance Requirements
- ⏳ Sub-second response times for file operations
- ✅ Smooth streaming chat experience
- ✅ Efficient memory usage
- ✅ Reliable WebSocket connections

**Score:** 5/14 criteria met (36%)

## 🔧 API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Real-time chat with streaming

### REST API
- `GET /` - Web UI
- `GET /api/health` - Health check
- `POST /api/chat` - Non-streaming chat
- `POST /api/execute` - Execute command

**Planned (Phase 2-3):**
- `POST /api/files/read` - Read file
- `POST /api/files/write` - Write file
- `GET /api/files/tree` - Project structure
- `POST /api/files/diff` - Generate diff

## 🚧 Development Roadmap

### Phase 1: Basic Chat ✅ (COMPLETED 2025-10-15)
FastAPI + Ollama + WebSocket + Streaming
**Effort:** 6 hours

### Phase 2: File Operations ⏳ (4-6 weeks)
DEIA awareness + File reading + Project browser
**Effort:** 8-10 hours

### Phase 3: File Modifications ⏳ (6-8 weeks)
File writing + Confirmation + Audit logging
**Effort:** 12-15 hours

### Phase 4: Polish ⏳ (Ongoing)
Enhanced UI + Keyboard shortcuts + Session persistence
**Effort:** 6-12 hours

**Total Estimated:** 30-43 hours (14% complete)

See [ROADMAP_SUMMARY.md](ROADMAP_SUMMARY.md) for detailed timeline.

## 🤝 Contributing

This project follows the LLH specification:
`.deia/.projects/simulation_004/gpt-llama-bot-eos-companion.md`

**Before contributing:**
1. Read [STATUS.md](STATUS.md) for current priorities
2. Review the LLH spec for requirements
3. Understand security constraints
4. Follow DEIA principles (DND, ROTG)

## 📝 Files

**Core:**
- `app.py` (635 lines) - Main FastAPI application
- `requirements.txt` - Python dependencies

**LLM Service:**
- `../src/deia/services/llm_service.py` (650 lines) - Unified LLM service
- `../src/deia/services/deepseek_service.py` (deprecated)

**Documentation:**
- `README.md` (this file) - Project overview
- `STATUS.md` - Detailed implementation status
- `QUICKSTART.md` - Getting started guide
- `ROADMAP_SUMMARY.md` - Phase overview
- `README_SERVICE.md` - Service API reference
- `IMPROVEMENTS.md` - Changelog
- `MIGRATION_SUMMARY.md` - Migration guide

## 🐛 Troubleshooting

**Ollama not responding:**
```bash
# Check Ollama is running
ollama serve

# Test API
curl http://localhost:11434/api/tags
```

**Model not found:**
```bash
# List models
ollama list

# Pull model
ollama pull qwen2.5-coder:7b
```

**WebSocket errors:**
- Check browser console
- Verify port 8000 is free
- Try refreshing the page

See [QUICKSTART.md](QUICKSTART.md#troubleshooting) for more.

## 📊 Metrics

**Code:**
- Total lines: ~1,300 (app.py + llm_service.py)
- Documentation: ~2,000 lines
- Tests: Not yet implemented

**Features:**
- Completed: 5/14 success criteria (36%)
- Phase completion: 1/4 (25%)
- Effort completion: 6/43 hours (14%)

## 🔗 Links

**Project:**
- [Main DEIA Repo](https://github.com/deiasolutions/deia)
- [Main Roadmap](../ROADMAP.md)
- [LLH Specification](../.deia/.projects/simulation_004/gpt-llama-bot-eos-companion.md)

**External:**
- [Ollama](https://ollama.com/) - Local LLM runtime
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Qwen 2.5 Coder](https://ollama.com/library/qwen2.5-coder) - Default model

## 📄 License

Same as DEIA project.

---

**Last Updated:** 2025-10-15
**Phase:** 1 of 4 complete
**Next Review:** 2025-10-16
**Status:** Production-ready for Phase 1, Phases 2-4 planned
