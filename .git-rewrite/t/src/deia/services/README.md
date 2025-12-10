# DEIA Services

LLM and AI services for DEIA (Distributed Ephemeral Institutional Architecture).

## Unified LLM Service (Recommended) ⭐

**File:** `llm_service.py`

Production-ready, unified LLM service with streaming, retry logic, conversation history management, and support for multiple providers (Ollama, DeepSeek, OpenAI).

**Status:** ✅ Active (2025-10-15)
**Documentation:** See `llama-chatbot/README_SERVICE.md` for complete API reference

### Quick Start

```python
from deia.services.llm_service import OllamaService

# Local Ollama with streaming
service = OllamaService(model="qwen2.5-coder:7b")

# Simple chat
response = service.chat_simple("What is an LLH?")

# Streaming chat
async for chunk in service.chat_stream("Explain DEIA"):
    print(chunk, end="", flush=True)
```

**Features:**
- ✅ Real-time streaming responses
- ✅ Automatic retry with exponential backoff
- ✅ Conversation history with auto-trimming
- ✅ Multiple provider support (Ollama/DeepSeek/OpenAI)
- ✅ Async/sync support
- ✅ Comprehensive logging and error handling
- ✅ DEIA-specific context prompts

---

## DeepSeek Service (Legacy) ⚠️

**File:** `deepseek_service.py`

**Status:** ⚠️ Deprecated - Use `llm_service.py` instead

Simple GPT service for running **local LLMs via Ollama** (default: qwen2.5-coder:7b). Also compatible with cloud APIs (DeepSeek, OpenAI). Adapted from `familybondbot` chatgpt_service.py with DEIA-specific simplifications.

> **Migration:** Replace `DeiaGPTService` with `OllamaService` from `llm_service.py`. API is mostly compatible.

### Features

- ✅ **Local-first:** Uses Ollama by default (no API key needed)
- ✅ Compatible with OpenAI client library
- ✅ Cloud-compatible (DeepSeek, OpenAI endpoints)
- ✅ Conversation history support
- ✅ DEIA-specific context prompts
- ✅ Token usage tracking
- ✅ Error handling (rate limits, API errors)
- ✅ Simple and full response modes

### Setup

1. **Install Ollama (for local LLM):**
   ```bash
   # Visit https://ollama.com/ and install for your OS
   # Or on Linux/macOS:
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull the model:**
   ```bash
   ollama pull qwen2.5-coder:7b
   ```

3. **Start Ollama server:**
   ```bash
   ollama serve
   ```

4. **Install Python dependencies:**
   ```bash
   pip install openai
   ```

**Optional: Cloud API setup**
   - For DeepSeek cloud API, set `DEEPSEEK_API_KEY` environment variable
   - Sign up at https://platform.deepseek.com/

### Usage

#### Simple Chat (Local Ollama)

```python
from deia.services.deepseek_service import DeiaGPTService

# Uses local Ollama by default (qwen2.5-coder:7b)
service = DeiaGPTService()
response = service.chat_simple("What is an LLH?")
print(response)
```

#### Full Response (with metadata)

```python
result = service.chat("Explain eOS architecture")
print(result['content'])
print(f"Tokens: {result['tokens_used']}, Time: {result['response_time_ms']}ms")
```

#### Cloud API (DeepSeek or OpenAI)

```python
# DeepSeek cloud
service = DeiaGPTService(
    api_key="your-deepseek-key",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# OpenAI cloud
service = DeiaGPTService(
    api_key="your-openai-key",
    base_url="https://api.openai.com/v1",
    model="gpt-4"
)
```

#### DEIA-Specific Chat

```python
result = service.deia_chat("How do I prevent viruses in eggs?")
print(result['content'])
```

#### Conversation History

```python
history = [
    {"role": "user", "content": "What is DEIA?"},
    {"role": "assistant", "content": "DEIA is a distributed architecture..."}
]

result = service.chat(
    "Tell me more about LLHs",
    conversation_history=history
)
```

### Models

**Available DeepSeek models:**
- `deepseek-chat` — General purpose (default)
- `deepseek-coder` — Code-focused (better for technical queries)

```python
# Use coder model
service = DeiaGPTService(
    api_key="your-key",
    model="deepseek-coder"
)
```

### Configuration

Pass parameters to constructor:

```python
service = DeiaGPTService(
    api_key="your-key",
    model="deepseek-chat",
    max_tokens=2000,          # Longer responses
    temperature=0.3           # More deterministic (0.0-2.0)
)
```

### Response Format

```python
{
    "content": "Response text...",
    "response_time_ms": 1234,
    "tokens_used": 567,
    "prompt_tokens": 100,
    "completion_tokens": 467,
    "model": "deepseek-chat",
    "success": True
}
```

### Error Handling

Service catches and returns errors gracefully:

```python
result = service.chat("Hello")

if result['success']:
    print(result['content'])
else:
    print(f"Error: {result['error']}")
    print(f"Details: {result.get('error_detail', '')}")
```

**Error types:**
- `rate_limit` — Too many requests
- `api_error` — DeepSeek API issue
- `unknown_error` — Unexpected error

### Run as Script

```bash
# Set environment variable first
export DEEPSEEK_API_KEY="your-key"

# Run test
python src/deia/services/deepseek_service.py
```

### Source

Adapted from `familybondbot/fbb/backend/src/services/chatgpt_service.py`

**Simplifications:**
- ❌ Removed family coaching prompts
- ❌ Removed Bond Barometer crisis detection
- ❌ Removed knowledge base tier system
- ❌ Removed content service dependencies
- ✅ Added DeepSeek endpoint support
- ✅ Added DEIA-specific context
- ✅ Kept conversation history
- ✅ Kept error handling

---

## Migration Guide

### From `deepseek_service.py` to `llm_service.py`

**Old code:**
```python
from deia.services.deepseek_service import DeiaGPTService

service = DeiaGPTService()
response = service.chat("Hello")
print(response["content"])
```

**New code:**
```python
from deia.services.llm_service import OllamaService

service = OllamaService()
response = service.chat("Hello")
print(response["content"])

# Or use streaming for better UX
async for chunk in service.chat_stream("Hello"):
    print(chunk, end="", flush=True)
```

**Benefits of upgrading:**
- Real-time streaming responses
- Automatic retry on failures
- Better error handling
- Conversation history management
- Multiple provider support
- Comprehensive logging

---

**Created:** 2025-10-15
**Last Updated:** 2025-10-15
**Active Service:** `llm_service.py`
**Deprecated Service:** `deepseek_service.py`
**Tags:** `#deia` `#llm` `#services` `#ollama` `#deepseek` `#openai`
