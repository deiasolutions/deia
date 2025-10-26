# FOCUSED TASK - BOT-001: Add AnthropicService
**Priority:** P0 BLOCKING
**Time:** 30 minutes
**Start:** NOW
**Blocker:** None - go immediately

---

## EXACTLY what to do:

### 1. Add import at top of `src/deia/services/llm_service.py`:
```python
from anthropic import Anthropic, AsyncAnthropic
```

### 2. Add this class after `OpenAIService` (line ~470):
```python
class AnthropicService(BaseLLMService):
    """Anthropic/Claude LLM service"""

    def __init__(
        self,
        api_key: str = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 2000,
        temperature: float = 0.7,
        timeout: int = 300,
        max_retries: int = 3
    ):
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY", "")

        super().__init__(
            api_key=api_key,
            model=model,
            base_url="https://api.anthropic.com",
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
            max_retries=max_retries
        )
        self.client = Anthropic(api_key=api_key)
        self.async_client = AsyncAnthropic(api_key=api_key)

    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """Send message to Claude, get response"""
        try:
            self.conversation_history.add_message("user", user_message)

            messages = self.conversation_history.get_messages()

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt or "You are a helpful assistant.",
                messages=messages
            )

            assistant_message = response.content[0].text
            self.conversation_history.add_message("assistant", assistant_message)

            return assistant_message
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    async def chat_async(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """Async version of chat"""
        try:
            self.conversation_history.add_message("user", user_message)

            messages = self.conversation_history.get_messages()

            response = await self.async_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt or "You are a helpful assistant.",
                messages=messages
            )

            assistant_message = response.content[0].text
            self.conversation_history.add_message("assistant", assistant_message)

            return assistant_message
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    async def chat_stream(self, user_message: str, system_prompt: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Stream response from Claude"""
        try:
            self.conversation_history.add_message("user", user_message)

            messages = self.conversation_history.get_messages()

            full_response = ""
            with self.async_client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt or "You are a helpful assistant.",
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    yield text

            self.conversation_history.add_message("assistant", full_response)
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
```

### 3. Create `tests/unit/test_anthropic_service.py`:
```python
import pytest
from deia.services.llm_service import AnthropicService

def test_anthropic_service_init():
    """Test AnthropicService initializes"""
    service = AnthropicService(api_key="test-key-12345")
    assert service.model == "claude-3-5-sonnet-20241022"
    assert service.conversation_history is not None

def test_anthropic_service_invalid_key():
    """Test error handling with invalid key"""
    service = AnthropicService(api_key="invalid")
    # Should not raise on init, only on chat attempt
    assert service is not None

def test_anthropic_conversation_history():
    """Test conversation history tracking"""
    service = AnthropicService(api_key="test-key-12345")
    service.conversation_history.add_message("user", "Hello")
    service.conversation_history.add_message("assistant", "Hi there")

    messages = service.conversation_history.get_messages()
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"

def test_anthropic_clear_history():
    """Test conversation history clearing"""
    service = AnthropicService(api_key="test-key-12345")
    service.conversation_history.add_message("user", "Hello")
    service.conversation_history.clear()

    messages = service.conversation_history.get_messages()
    assert len(messages) == 0

def test_anthropic_service_extends_base():
    """Test AnthropicService extends BaseLLMService"""
    from deia.services.llm_service import BaseLLMService
    service = AnthropicService(api_key="test-key-12345")
    assert isinstance(service, BaseLLMService)
```

### 4. Run tests:
```bash
pytest tests/unit/test_anthropic_service.py -v
```

All 5 tests must PASS.

---

## DONE - Report completion:
Create: `.deia/hive/responses/deiasolutions/bot-001-anthropic-service-done.md`

Write:
- Service added successfully
- All 5 tests passing
- Ready for BOT-003

---

## NO OTHER WORK. Just this.
