"""Unified LLM Service for DEIA - Provider-agnostic chat interface.

This module provides a base class and provider-specific implementations
for interacting with various LLM backends (Ollama, DeepSeek, OpenAI, etc.)

Usage:
    from deia.services.llm_service import OllamaService, DeepSeekService

    # Local Ollama
    service = OllamaService(model="qwen2.5-coder:7b")

    # DeepSeek Cloud
    service = DeepSeekService(api_key="your-key", model="deepseek-coder")

    # Simple chat
    response = service.chat("Hello, explain LLHs")

    # Streaming chat
    async for chunk in service.chat_stream("Explain DEIA architecture"):
        print(chunk, end="", flush=True)
"""

import asyncio
import importlib
import logging
import os
import time
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

from openai import AsyncOpenAI, OpenAI
import openai

try:  # Optional dependency; resolved lazily if unavailable
    _ANTHROPIC_MODULE = importlib.import_module("anthropic")  # pragma: no cover
except ImportError:  # pragma: no cover
    _ANTHROPIC_MODULE = None

logger = logging.getLogger(__name__)


def _get_anthropic_module():
    """Return anthropic module if available, attempting lazy import on demand."""
    global _ANTHROPIC_MODULE
    if _ANTHROPIC_MODULE is None:
        try:
            _ANTHROPIC_MODULE = importlib.import_module("anthropic")
        except ImportError:
            return None
    return _ANTHROPIC_MODULE


class ConversationHistory:
    """Manages conversation history with token/token-count heuristics."""

    def __init__(
        self,
        max_messages: int = 20,
        max_tokens: int = 4000,
        tokenizer: Optional[Any] = None,
    ):
        """
        Args:
            max_messages: Maximum message count (excluding system prompts)
            max_tokens: Approximate max tokens (provider-specific heuristics)
            tokenizer: Optional callable returning token count for str content
        """
        self.messages: List[Dict[str, str]] = []
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.tokenizer = tokenizer or _estimate_tokens

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim_if_needed()

    def _trim_if_needed(self):
        system_msgs = [m for m in self.messages if m["role"] == "system"]
        other_msgs = [m for m in self.messages if m["role"] != "system"]

        if len(other_msgs) > self.max_messages:
            other_msgs = other_msgs[-self.max_messages :]

        total_tokens = sum(self.tokenizer(m["content"]) for m in other_msgs)
        while total_tokens > self.max_tokens and len(other_msgs) > 2:
            removed = other_msgs.pop(0)
            total_tokens -= self.tokenizer(removed["content"])

        self.messages = system_msgs + other_msgs

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages.copy()

    def clear(self):
        self.messages.clear()


def _estimate_tokens(text: str) -> int:
    """Basic token estimation fallback (approx 4 chars = 1 token)."""
    if not text:
        return 1
    return max(1, len(text) // 4)


class BaseLLMService(ABC):
    """Base class for LLM service implementations."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        timeout: int = 300,
        max_retries: int = 3
    ):
        """Initialize base LLM service.

        Args:
            api_key: API key for the service
            model: Model identifier
            base_url: Base URL for API endpoint
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-2.0)
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
        self.async_client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_retries = max_retries

        logger.info(f"Initialized {self.__class__.__name__} with model={model}, base_url={base_url}")

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a chat message and get response (synchronous).

        Args:
            user_message: User's message/question
            system_prompt: Optional system prompt to set context
            conversation_history: Optional list of previous messages
            **kwargs: Additional parameters to pass to the API

        Returns:
            Dict with response content, tokens, timing, and success status
        """
        start_time = time.time()
        messages = self._build_messages(user_message, system_prompt, conversation_history)

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    **kwargs
                )

                response_time_ms = int((time.time() - start_time) * 1000)
                ai_response = response.choices[0].message.content.strip()
                usage = response.usage

                result = {
                    "content": ai_response,
                    "response_time_ms": response_time_ms,
                    "tokens_used": usage.total_tokens,
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "model": self.model,
                    "success": True,
                    "finish_reason": response.choices[0].finish_reason
                }

                logger.debug(f"Chat completed in {response_time_ms}ms, tokens={usage.total_tokens}")
                return result

            except openai.RateLimitError as e:
                logger.warning(f"Rate limit hit (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return self._error_response("rate_limit", str(e), start_time)

            except openai.APIError as e:
                logger.error(f"API error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                return self._error_response("api_error", str(e), start_time)

            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)
                return self._error_response("unknown_error", str(e), start_time)

        return self._error_response("max_retries_exceeded", "All retry attempts failed", start_time)

    async def chat_async(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a chat message and get response (asynchronous)."""
        start_time = time.time()
        messages = self._build_messages(user_message, system_prompt, conversation_history)

        for attempt in range(self.max_retries):
            try:
                response = await self.async_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    **kwargs
                )

                response_time_ms = int((time.time() - start_time) * 1000)
                ai_response = response.choices[0].message.content.strip()
                usage = response.usage

                return {
                    "content": ai_response,
                    "response_time_ms": response_time_ms,
                    "tokens_used": usage.total_tokens,
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "model": self.model,
                    "success": True,
                    "finish_reason": response.choices[0].finish_reason
                }

            except openai.RateLimitError as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return self._error_response("rate_limit", str(e), start_time)

            except openai.APIError as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                return self._error_response("api_error", str(e), start_time)

            except Exception as e:
                logger.error(f"Async chat error: {e}", exc_info=True)
                return self._error_response("unknown_error", str(e), start_time)

        return self._error_response("max_retries_exceeded", "All retry attempts failed", start_time)

    async def chat_stream(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream chat response in real-time.

        Args:
            user_message: User's message/question
            system_prompt: Optional system prompt
            conversation_history: Optional message history
            **kwargs: Additional API parameters

        Yields:
            Response chunks as they arrive
        """
        messages = self._build_messages(user_message, system_prompt, conversation_history)

        try:
            stream = await self.async_client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True,
                **kwargs
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Streaming error: {e}", exc_info=True)
            yield f"\n\n[Error: {str(e)}]"

    def chat_simple(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """Simplified chat that returns just the response text."""
        result = self.chat(user_message, system_prompt)
        return result.get("content", "")

    def _build_messages(
        self,
        user_message: str,
        system_prompt: Optional[str],
        conversation_history: Optional[List[Dict[str, str]]]
    ) -> List[Dict[str, str]]:
        """Build messages array for API call."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        return messages

    def _error_response(self, error_type: str, error_detail: str, start_time: float) -> Dict[str, Any]:
        """Create standardized error response."""
        return {
            "content": self._get_error_message(error_type),
            "response_time_ms": int((time.time() - start_time) * 1000),
            "error": error_type,
            "error_detail": error_detail,
            "success": False
        }

    @staticmethod
    def _get_error_message(error_type: str) -> str:
        """Get user-friendly error message."""
        messages = {
            "rate_limit": "Rate limit exceeded. Please try again in a moment.",
            "api_error": "API error occurred. Please try again.",
            "timeout": "Request timed out. Please try again.",
            "unknown_error": "Unexpected error occurred.",
            "max_retries_exceeded": "Request failed after multiple attempts.",
            "missing_api_key": "Anthropic API key missing. Set ANTHROPIC_API_KEY and retry.",
            "module_missing": "Anthropic SDK not installed. Run `pip install anthropic`.",
            "invalid_message": "Message invalid. Provide non-empty plain text.",
            "token_limit": "Conversation exceeds allowable token limit. Trim context and retry.",
            "stream_error": "Streaming failed mid-response. Check logs.",
        }
        return messages.get(error_type, "An error occurred.")


class OllamaService(BaseLLMService):
    """Service for local Ollama LLM instances."""

    def __init__(
        self,
        model: str = "qwen2.5-coder:7b",
        base_url: str = "http://localhost:11434/v1",
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ):
        """Initialize Ollama service.

        Args:
            model: Ollama model name (e.g., "qwen2.5-coder:7b", "deepseek-coder-v2:16b")
            base_url: Ollama API endpoint
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            **kwargs: Additional BaseLLMService parameters
        """
        super().__init__(
            api_key="ollama",  # Ollama doesn't require real API key
            model=model,
            base_url=base_url,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )

    def deia_chat(
        self,
        user_message: str,
        context: str = "You are a helpful assistant for the DEIA project."
    ) -> Dict[str, Any]:
        """DEIA-specific chat with default DEIA context."""
        deia_system_prompt = f"""{context}

DEIA is an operating system (eOS) for ephemeral organizational entities:
- Kernel: ROTG (Rules of the Game) + DND (Do Not Delete) policy
- Processes: Eggs (unborn entities), LLHs (Limited Liability Hives), TAGs (Together And Good teams)
- IPC: RSE (Routine State Events) - append-only JSONL coordination
- Filesystem: .deia/ for commons, .deia/projects/<name>/ for segmented workloads

Provide clear, concise, technical guidance following DEIA principles:
- Egg-first architecture (all entities start as eggs)
- Virus prevention (no uncontained instructions)
- DND honored (archive, don't delete)
- ROTG enforcement (policy compliance)
"""
        return self.chat(user_message, system_prompt=deia_system_prompt)


class DeepSeekService(BaseLLMService):
    """Service for DeepSeek cloud API."""

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-coder",
        base_url: str = "https://api.deepseek.com/v1",
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ):
        """Initialize DeepSeek service.

        Args:
            api_key: DeepSeek API key
            model: DeepSeek model name
            base_url: DeepSeek API endpoint
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            **kwargs: Additional BaseLLMService parameters
        """
        super().__init__(
            api_key=api_key,
            model=model,
            base_url=base_url,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )


class OpenAIService(BaseLLMService):
    """Service for OpenAI API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ):
        """Initialize OpenAI service.

        Args:
            api_key: OpenAI API key
            model: OpenAI model name (e.g., "gpt-4", "gpt-3.5-turbo")
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            **kwargs: Additional BaseLLMService parameters
        """
        super().__init__(
            api_key=api_key,
            model=model,
            base_url="https://api.openai.com/v1",
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )


class AnthropicService(BaseLLMService):
    """Service for Anthropic Claude models."""

    DEFAULT_MODEL = "claude-3-5-sonnet-20240620"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        timeout: int = 120,
        max_retries: int = 3,
        conversation_history: Optional[ConversationHistory] = None,
    ):
        raw_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        module = _get_anthropic_module()

        self.available = raw_key is not None and module is not None
        self.disabled_reason = None
        anthropic_key = raw_key or "anthropic-key-missing"
        if raw_key is None:
            self.disabled_reason = "missing_api_key"
        elif module is None:
            self.disabled_reason = "module_missing"

        super().__init__(
            api_key=anthropic_key,
            model=model,
            base_url="https://api.openai.com/v1",  # unused but required by base
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.history = conversation_history or ConversationHistory(
            max_messages=40,
            max_tokens=max_tokens * 2,
            tokenizer=_estimate_tokens,
        )

        self._timeout = timeout
        self.anthropic_client = None
        self.anthropic_async_client = None

        if self.available:
            self.anthropic_client = module.Anthropic(
                api_key=raw_key,
                timeout=timeout,
                max_retries=max_retries,
            )
            self.anthropic_async_client = module.AsyncAnthropic(
                api_key=raw_key,
                timeout=timeout,
                max_retries=max_retries,
            )

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        start_time = time.time()
        validation_error = self._validate_message(user_message)
        if validation_error:
            return self._error_response(validation_error, "Invalid message", start_time)

        if not self.available:
            return self._error_response(self.disabled_reason or "api_error", "Anthropic unavailable", start_time)

        sys_prompt, messages = self._prepare_messages(user_message, system_prompt, conversation_history)
        if not self._within_token_budget(messages):
            return self._error_response("token_limit", "Conversation exceeds Anthropic token budget", start_time)

        for attempt in range(self.max_retries):
            try:
                response = self.anthropic_client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=sys_prompt,
                    messages=messages,
                    **kwargs,
                )
                result = self._build_success_response(response, start_time)
                if conversation_history is None:
                    self._append_history(user_message, result["content"])
                return result
            except Exception as exc:
                error_type = self._map_anthropic_error(exc)
                logger.error(
                    "Anthropic chat error (%s/%s): %s",
                    attempt + 1,
                    self.max_retries,
                    exc,
                    exc_info=True,
                )
                if error_type == "rate_limit" and attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return self._error_response(error_type, str(exc), start_time)

        return self._error_response("max_retries_exceeded", "All retry attempts failed", start_time)

    async def chat_async(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        start_time = time.time()
        validation_error = self._validate_message(user_message)
        if validation_error:
            return self._error_response(validation_error, "Invalid message", start_time)

        if not self.available:
            return self._error_response(self.disabled_reason or "api_error", "Anthropic unavailable", start_time)

        sys_prompt, messages = self._prepare_messages(user_message, system_prompt, conversation_history)
        if not self._within_token_budget(messages):
            return self._error_response("token_limit", "Conversation exceeds Anthropic token budget", start_time)

        for attempt in range(self.max_retries):
            try:
                response = await self.anthropic_async_client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=sys_prompt,
                    messages=messages,
                    **kwargs,
                )
                result = self._build_success_response(response, start_time)
                if conversation_history is None:
                    self._append_history(user_message, result["content"])
                return result
            except Exception as exc:
                error_type = self._map_anthropic_error(exc)
                if error_type == "rate_limit" and attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return self._error_response(error_type, str(exc), start_time)

        return self._error_response("max_retries_exceeded", "All retry attempts failed", start_time)

    async def chat_stream(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        validation_error = self._validate_message(user_message)
        if validation_error:
            yield f"[Error: {validation_error}]"
            return

        if not self.available:
            yield "[Error: Anthropic unavailable]"
            return

        sys_prompt, messages = self._prepare_messages(user_message, system_prompt, conversation_history)
        if not self._within_token_budget(messages):
            yield "[Error: Conversation exceeds Anthropic token limit]"
            return

        try:
            stream_call = self.anthropic_async_client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=sys_prompt,
                messages=messages,
                **kwargs,
            )
            if hasattr(stream_call, "__aenter__"):
                async with stream_call as stream:
                    async for chunk in self._iterate_stream(stream):
                        yield chunk
            else:
                async for chunk in self._iterate_stream(stream_call):
                    yield chunk
        except Exception as exc:
            logger.error("Anthropic stream error: %s", exc, exc_info=True)
            yield f"[Error: {exc}]"

    async def _iterate_stream(self, stream_obj) -> AsyncGenerator[str, None]:
        async for event in stream_obj:
            text = self._extract_stream_text(event)
            if text:
                yield text

    def _append_history(self, user_message: str, assistant_message: str):
        self.history.add_message("user", user_message)
        self.history.add_message("assistant", assistant_message)

    def _build_success_response(self, response: Any, start_time: float) -> Dict[str, Any]:
        text = self._extract_response_text(response)
        usage = getattr(response, "usage", None)
        input_tokens = getattr(usage, "input_tokens", None) if usage else None
        output_tokens = getattr(usage, "output_tokens", None) if usage else None
        tokens_used = None
        if input_tokens is not None and output_tokens is not None:
            tokens_used = input_tokens + output_tokens

        return {
            "content": text,
            "response_time_ms": int((time.time() - start_time) * 1000),
            "tokens_used": tokens_used,
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "model": self.model,
            "success": True,
            "id": getattr(response, "id", None),
        }

    def _extract_response_text(self, response: Any) -> str:
        content_blocks = getattr(response, "content", [])
        fragments: List[str] = []
        for block in content_blocks:
            if isinstance(block, dict):
                text_val = block.get("text")
            else:
                text_val = getattr(block, "text", None)
            if text_val:
                fragments.append(text_val)
        if not fragments and hasattr(response, "completion"):
            fragments.append(getattr(response, "completion"))
        return "".join(fragments).strip()

    def _extract_stream_text(self, event: Any) -> str:
        if isinstance(event, dict):
            if event.get("type") == "content_block_delta":
                return event.get("delta", {}).get("text", "")
            return event.get("text", "")
        event_type = getattr(event, "type", "")
        if event_type == "content_block_delta":
            delta = getattr(event, "delta", None)
            return getattr(delta, "text", "") if delta else ""
        return getattr(event, "text", "")

    def _validate_message(self, message: str) -> Optional[str]:
        if message is None or not isinstance(message, str) or not message.strip():
            return "invalid_message"
        if len(message) > 50_000:
            return "token_limit"
        return None

    def _prepare_messages(
        self,
        user_message: str,
        system_prompt: Optional[str],
        conversation_history: Optional[List[Dict[str, str]]],
    ) -> Tuple[Optional[str], List[Dict[str, str]]]:
        history = conversation_history if conversation_history is not None else self.history.get_messages()
        sys_prompt = system_prompt
        prepared: List[Dict[str, str]] = []

        for entry in history:
            if entry["role"] == "system" and not sys_prompt:
                sys_prompt = entry["content"]
                continue
            prepared.append({"role": entry["role"], "content": entry["content"]})

        prepared.append({"role": "user", "content": user_message})
        return sys_prompt, prepared

    def _within_token_budget(self, messages: List[Dict[str, str]]) -> bool:
        total = sum(_estimate_tokens(m["content"]) for m in messages if m["role"] != "system")
        return total <= self.history.max_tokens

    def _map_anthropic_error(self, exc: Exception) -> str:
        name = exc.__class__.__name__.lower()
        if "ratelimit" in name or "rate_limit" in name:
            return "rate_limit"
        if "timeout" in name:
            return "timeout"
        if "authentication" in name or "invalidapi" in name:
            return "api_error"
        return "api_error"



# Convenience function to create service from config
def create_llm_service(
    provider: str = "ollama",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> BaseLLMService:
    """Factory function to create LLM service based on provider.

    Args:
        provider: Provider name ("ollama", "deepseek", "openai", "anthropic")
        api_key: API key (required for cloud providers)
        model: Model name (uses provider defaults if not specified)
        **kwargs: Additional service parameters

    Returns:
        Configured LLM service instance

    Example:
        service = create_llm_service("ollama", model="qwen2.5-coder:7b")
        service = create_llm_service("deepseek", api_key="sk-...", model="deepseek-coder")
        service = create_llm_service("anthropic", api_key="sk-ant-...", model="claude-3-5-sonnet-20241022")
    """
    provider = provider.lower()

    if provider == "ollama":
        return OllamaService(model=model or "qwen2.5-coder:7b", **kwargs)
    elif provider == "deepseek":
        if not api_key:
            raise ValueError("api_key required for DeepSeek service")
        return DeepSeekService(api_key=api_key, model=model or "deepseek-coder", **kwargs)
    elif provider == "openai":
        if not api_key:
            raise ValueError("api_key required for OpenAI service")
        return OpenAIService(api_key=api_key, model=model or "gpt-4", **kwargs)
    elif provider == "anthropic":
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        return AnthropicService(api_key=api_key, model=model or "claude-3-5-sonnet-20241022", **kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'ollama', 'deepseek', 'openai', or 'anthropic'")


# Example usage
if __name__ == "__main__":
    import os
    import sys

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Test with Ollama (local)
    print("=== Testing Ollama Service ===")
    service = OllamaService(model="qwen2.5-coder:7b")

    print("\nSimple chat test:")
    response = service.chat_simple("What is Python? Answer in one sentence.")
    print(f"Response: {response}\n")

    print("DEIA chat test:")
    result = service.deia_chat("What is an LLH?")
    print(f"Response: {result['content']}")
    print(f"Tokens: {result.get('tokens_used', 'N/A')}, Time: {result.get('response_time_ms', 'N/A')}ms\n")

    # Test streaming (async)
    async def test_streaming():
        print("=== Testing Streaming ===")
        async for chunk in service.chat_stream("Count from 1 to 5 slowly."):
            print(chunk, end="", flush=True)
        print("\n")

    # Run async test
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_streaming())
