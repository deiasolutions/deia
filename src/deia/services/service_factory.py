"""
Service Factory - Create LLM service instances by type.

Maps bot_type to service class/adapter and handles initialization.
"""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Optional, Union

from deia.services.llm_service import AnthropicService, OpenAIService, OllamaService
from deia.adapters.claude_code_cli_adapter import ClaudeCodeCLIAdapter
from deia.adapters.codex_cli_adapter import CodexCLIAdapter


class BotType(str, Enum):
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    CLAUDE_CODE = "claude-code"
    CODEX = "codex"
    LLAMA = "llama"


ServiceReturnType = Union[
    AnthropicService,
    OpenAIService,
    OllamaService,
    ClaudeCodeCLIAdapter,
    CodexCLIAdapter,
]


class ServiceFactory:
    """Factory for creating bot services/adapters."""

    @staticmethod
    def get_service(
        bot_type: str,
        bot_id: str,
        work_dir: Optional[Path] = None,
    ) -> ServiceReturnType:
        bot_type = bot_type.lower().strip()

        if bot_type == BotType.CLAUDE:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set for claude bot type")
            return AnthropicService(api_key=api_key)

        if bot_type == BotType.CHATGPT:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set for chatgpt bot type")
            return OpenAIService(api_key=api_key)

        if bot_type == BotType.LLAMA:
            return OllamaService(model="qwen2.5-coder:7b")

        if bot_type == BotType.CLAUDE_CODE:
            base_dir = work_dir or Path.cwd()
            return ClaudeCodeCLIAdapter(
                bot_id=bot_id,
                work_dir=base_dir,
                claude_cli_path=os.getenv("CLAUDE_CLI_PATH", "claude"),
            )

        if bot_type == BotType.CODEX:
            base_dir = work_dir or Path.cwd()
            return CodexCLIAdapter(
                bot_id=bot_id,
                work_dir=base_dir,
                codex_cli_path=os.getenv("CODEX_CLI_PATH", "codex"),
            )

        raise ValueError(
            f"Unknown bot_type '{bot_type}'. "
            f"Supported: {', '.join(t.value for t in BotType)}"
        )

    @staticmethod
    def is_cli_service(bot_type: str) -> bool:
        bot_type = bot_type.lower().strip()
        return bot_type in {BotType.CLAUDE_CODE, BotType.CODEX}

    @staticmethod
    def get_supported_types() -> list[str]:
        return [t.value for t in BotType]
