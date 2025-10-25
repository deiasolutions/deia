# LLM Service Documentation

## Overview

The improved LLM service provides a unified, provider-agnostic interface for interacting with various language models (Ollama, DeepSeek, OpenAI). It includes advanced features like streaming, retry logic, conversation history management, and comprehensive error handling.

## Key Improvements

### 1. Unified Service Architecture
- **Base Class**: `BaseLLMService` provides common functionality
- **Provider Classes**: `OllamaService`, `DeepSeekService`, `OpenAIService`
- **Factory Function**: `create_llm_service()` for easy instantiation

### 2. Streaming Support
- Real-time response streaming via `chat_stream()`
- Reduces perceived latency for better UX
- Async generator pattern for efficient memory usage

### 3. Conversation History Management
- `ConversationHistory` class with automatic trimming
- Token-aware history retention
- Prevents context window overflow

### 4. Retry Logic & Error Handling
- Exponential backoff for rate limits
- Automatic retry on transient failures
- Detailed error categorization
- Comprehensive logging

### 5. Better Logging
- Structured logging throughout
- Debug information for troubleshooting
- Performance metrics tracking

## Usage Examples

### Basic Usage (Ollama)

```python
from src.deia.services.llm_service import OllamaService

# Initialize service
service = OllamaService(
    model="qwen2.5-coder:7b",
    base_url="http://localhost:11434/v1"
)

# Simple chat
response = service.chat_simple("Explain Python decorators")
print(response)

# Detailed chat with metadata
result = service.chat("What is DEIA?")
print(f"Response: {result['content']}")
print(f"Tokens: {result['tokens_used']}")
print(f"Time: {result['response_time_ms']}ms")
```

### Streaming Response

```python
import asyncio

async def stream_example():
    service = OllamaService()

    print("Streaming response:")
    async for chunk in service.chat_stream("Write a haiku about coding"):
        print(chunk, end="", flush=True)
    print()

asyncio.run(stream_example())
```

### Conversation History

```python
from src.deia.services.llm_service import ConversationHistory

# Create history manager
history = ConversationHistory(max_messages=20, max_tokens=4000)

# Add system prompt
history.add_message("system", "You are a helpful coding assistant.")

# First question
result = service.chat(
    "What is a closure?",
    conversation_history=history.get_messages()
)
history.add_message("user", "What is a closure?")
history.add_message("assistant", result["content"])

# Follow-up question (maintains context)
result = service.chat(
    "Show me an example",
    conversation_history=history.get_messages()
)
history.add_message("user", "Show me an example")
history.add_message("assistant", result["content"])
```

### Using Different Providers

```python
from src.deia.services.llm_service import DeepSeekService, OpenAIService, create_llm_service

# DeepSeek
deepseek = DeepSeekService(
    api_key="sk-...",
    model="deepseek-coder"
)

# OpenAI
openai = OpenAIService(
    api_key="sk-...",
    model="gpt-4"
)

# Factory pattern
service = create_llm_service(
    provider="ollama",
    model="qwen2.5-coder:7b"
)
```

### DEIA-Specific Chat

```python
service = OllamaService()

result = service.deia_chat("What is an LLH?")
print(result["content"])  # Gets DEIA-contextualized response
```

## API Reference

### BaseLLMService

Base class for all LLM services.

**Constructor Parameters:**
- `api_key` (str): API key for the service
- `model` (str): Model identifier
- `base_url` (str): Base URL for API endpoint
- `max_tokens` (int): Maximum tokens in response (default: 2000)
- `temperature` (float): Sampling temperature 0.0-2.0 (default: 0.7)
- `timeout` (int): Request timeout in seconds (default: 300)
- `max_retries` (int): Maximum retry attempts (default: 3)

**Methods:**

#### `chat(user_message, system_prompt=None, conversation_history=None, **kwargs)`
Synchronous chat.

**Returns:** Dict with keys:
- `content` (str): Response text
- `response_time_ms` (int): Response time in milliseconds
- `tokens_used` (int): Total tokens used
- `prompt_tokens` (int): Tokens in prompt
- `completion_tokens` (int): Tokens in completion
- `model` (str): Model used
- `success` (bool): Whether request succeeded
- `finish_reason` (str): Completion reason
- `error` (str, optional): Error type if failed
- `error_detail` (str, optional): Error details if failed

#### `async chat_async(user_message, system_prompt=None, conversation_history=None, **kwargs)`
Asynchronous chat. Same return format as `chat()`.

#### `async chat_stream(user_message, system_prompt=None, conversation_history=None, **kwargs)`
Stream response in real-time.

**Yields:** str chunks as they arrive

#### `chat_simple(user_message, system_prompt=None)`
Simplified chat returning just the response text.

**Returns:** str

### OllamaService

Service for local Ollama instances.

**Constructor Parameters:**
- `model` (str): Ollama model name (default: "qwen2.5-coder:7b")
- `base_url` (str): Ollama endpoint (default: "http://localhost:11434/v1")
- `max_tokens` (int): Maximum response tokens (default: 2000)
- `temperature` (float): Sampling temperature (default: 0.7)

**Additional Methods:**

#### `deia_chat(user_message, context="...")`
DEIA-specific chat with pre-configured DEIA context.

### DeepSeekService

Service for DeepSeek cloud API.

**Constructor Parameters:**
- `api_key` (str): DeepSeek API key (required)
- `model` (str): Model name (default: "deepseek-coder")
- `base_url` (str): API endpoint (default: "https://api.deepseek.com/v1")
- Other parameters same as BaseLLMService

### OpenAIService

Service for OpenAI API.

**Constructor Parameters:**
- `api_key` (str): OpenAI API key (required)
- `model` (str): Model name (default: "gpt-4")
- Other parameters same as BaseLLMService

### ConversationHistory

Manages conversation history with automatic trimming.

**Constructor Parameters:**
- `max_messages` (int): Maximum messages to retain (default: 20)
- `max_tokens` (int): Approximate token limit (default: 4000)

**Methods:**

#### `add_message(role, content)`
Add a message to history. Automatically trims if needed.

#### `get_messages()`
Get current message list as List[Dict[str, str]].

#### `clear()`
Clear all messages.

### Factory Function

#### `create_llm_service(provider="ollama", api_key=None, model=None, **kwargs)`

Create an LLM service instance based on provider.

**Parameters:**
- `provider` (str): "ollama", "deepseek", or "openai"
- `api_key` (str, optional): API key (required for cloud providers)
- `model` (str, optional): Model name (uses defaults if not specified)
- `**kwargs`: Additional service parameters

**Returns:** BaseLLMService instance

## Integration with FastAPI

The `app.py` has been refactored to use the new service:

### Key Changes:

1. **Service Initialization**:
   ```python
   llm_service = OllamaService(
       model=MODEL_NAME,
       base_url=f"{LLAMA_ENDPOINT}/v1",
       max_tokens=MAX_TOKENS,
       temperature=TEMPERATURE
   )
   ```

2. **Conversation History per Connection**:
   ```python
   active_connections: dict[WebSocket, ConversationHistory] = {}
   ```

3. **Streaming WebSocket Responses**:
   ```python
   async for chunk in llm_service.chat_stream(...):
       full_response += chunk
       await websocket.send_text(
           json.dumps({"type": "stream", "content": chunk})
       )
   ```

4. **REST API with Async**:
   ```python
   result = await llm_service.chat_async(
       user_message=request.message,
       system_prompt="You are a helpful AI assistant.",
       conversation_history=history
   )
   ```

## Configuration

### Environment Variables

- `MODEL_NAME`: Model to use (default: "qwen2.5-coder:7b")
- `LLAMA_ENDPOINT`: Ollama endpoint (default: "http://localhost:11434")
- `MAX_TOKENS`: Maximum response tokens (default: "2048")
- `TEMPERATURE`: Sampling temperature (default: "0.7")

### Logging

Set logging level via:
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # For verbose logs
```

## Error Handling

The service categorizes errors into:

1. **rate_limit**: Rate limiting errors (with automatic retry)
2. **api_error**: API-level errors (with retry)
3. **timeout**: Request timeout
4. **unknown_error**: Unexpected errors
5. **max_retries_exceeded**: All retries exhausted

All errors are logged with full context for debugging.

## Performance Considerations

1. **Streaming**: Use `chat_stream()` for long responses to improve perceived performance
2. **Conversation History**: Trim history to avoid context window issues
3. **Retries**: Exponential backoff prevents overwhelming the API
4. **Async**: Use `chat_async()` in async contexts for better concurrency

## Testing

Run the service module directly to test:

```bash
# Make sure Ollama is running
ollama serve

# Test the service
python src/deia/services/llm_service.py
```

## Migration Guide

### From Old Service to New

**Old code:**
```python
from llama_chatbot.ollama_service import DeiaGPTService

service = DeiaGPTService()
response = service.chat("Hello")
print(response["content"])
```

**New code:**
```python
from src.deia.services.llm_service import OllamaService

service = OllamaService()
response = service.chat("Hello")
print(response["content"])
```

The API is largely compatible, but with added features and better error handling.

## Future Enhancements

Potential improvements:
- [ ] Support for function calling
- [ ] JSON mode for structured outputs
- [ ] Cost tracking for cloud APIs
- [ ] Response caching
- [ ] Multi-model routing
- [ ] A/B testing framework
- [ ] Usage analytics

## License

Same as DEIA project.
