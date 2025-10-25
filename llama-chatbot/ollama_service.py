"""Ollama GPT Service for DEIA - Simplified chat interface for LLM interaction.

Adapted from familybondbot chatgpt_service.py with DEIA-specific simplifications.

Usage:
    from deia.services.ollama_service import DeiaGPTService

    service = DeiaGPTService(api_key="your-api-key")
    response = service.chat("Hello, can you help me understand LLHs?")
"""

import time
from typing import Dict, Any, Optional, List
from openai import OpenAI
import openai


class DeiaGPTService:
    """Simplified GPT service for DEIA using Ollama API.

    This service provides basic chat functionality with Ollama's LLM,
    compatible with OpenAI's client library.
    """

    def __init__(
        self,
        api_key: str = "ollama",
        model: str = "qwen2.5-coder:7b",
        base_url: str = "http://localhost:11434/v1",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ):
        """Initialize Ollama GPT service for local LLM.

        Args:
            api_key: API key (default: "ollama" for local Ollama)
            model: Model to use (default: "qwen2.5-coder:7b")
            base_url: Ollama API endpoint (default: http://localhost:11434/v1)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-2.0)
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Send a chat message and get response.

        Args:
            user_message: User's message/question
            system_prompt: Optional system prompt to set context
            conversation_history: Optional list of previous messages
                Format: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

        Returns:
            Dict with response content, tokens, timing, and success status
        """
        start_time = time.time()

        try:
            # Build messages array
            messages = []

            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Call Ollama API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Extract response content
            ai_response = response.choices[0].message.content.strip()

            # Extract token usage
            usage = response.usage
            total_tokens = usage.total_tokens

            return {
                "content": ai_response,
                "response_time_ms": response_time_ms,
                "tokens_used": total_tokens,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "model": self.model,
                "success": True
            }

        except openai.RateLimitError as e:
            return {
                "content": "Rate limit exceeded. Please try again in a moment.",
                "response_time_ms": int((time.time() - start_time) * 1000),
                "error": "rate_limit",
                "error_detail": str(e),
                "success": False
            }

        except openai.APIError as e:
            return {
                "content": "API error occurred. Please try again.",
                "response_time_ms": int((time.time() - start_time) * 1000),
                "error": "api_error",
                "error_detail": str(e),
                "success": False
            }

        except Exception as e:
            return {
                "content": "Unexpected error occurred.",
                "response_time_ms": int((time.time() - start_time) * 1000),
                "error": "unknown_error",
                "error_detail": str(e),
                "success": False
            }

    def chat_simple(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """Simplified chat that returns just the response text.

        Args:
            user_message: User's message/question
            system_prompt: Optional system prompt

        Returns:
            Response text string (or error message if failed)
        """
        result = self.chat(user_message, system_prompt)
        return result.get("content", "")

    def deia_chat(
        self,
        user_message: str,
        context: str = "You are a helpful assistant for the DEIA (Distributed Ephemeral Institutional Architecture) project."
    ) -> Dict[str, Any]:
        """DEIA-specific chat with default DEIA context.

        Args:
            user_message: User's question about DEIA
            context: System context (defaults to DEIA assistant prompt)

        Returns:
            Full response dict with content, tokens, timing
        """
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


# Example usage (can be run as a script)
if __name__ == "__main__":
    import os

    # For Ollama (local), no API key needed
    api_key = os.environ.get("OLLAMA_API_KEY") or "ollama"

    # Initialize service (defaults to local Ollama with qwen2.5-coder:7b)
    service = DeiaGPTService()

    print("Using Ollama locally with qwen2.5-coder:7b")
    print("Make sure Ollama is running: ollama serve\n")

    # Test simple chat
    print("=== Simple Chat Test ===")
    response = service.chat_simple("What is an LLH?")
    print(f"Response: {response}\n")

    # Test DEIA-specific chat
    print("=== DEIA Chat Test ===")
    result = service.deia_chat("Explain the difference between an Egg and an LLH")
    print(f"Response: {result['content']}")
    print(f"Tokens used: {result.get('tokens_used', 'N/A')}")
    print(f"Response time: {result.get('response_time_ms', 'N/A')}ms")
