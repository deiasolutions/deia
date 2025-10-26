"""
Service Factory - Creates appropriate service instances based on bot type

This factory handles creating LLM services (API-based) and CLI adapters based on the
specified bot_type. It centralizes service creation logic.
"""

import logging
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


class ServiceFactory:
    """Factory for creating LLM services and CLI adapters."""

    # CLI service types
    CLI_SERVICES = {'claude-code', 'codex'}
    
    # API service types
    API_SERVICES = {'claude', 'chatgpt', 'llama', 'deepseek', 'ollama'}
    
    ALL_SERVICES = CLI_SERVICES | API_SERVICES

    @staticmethod
    def get_supported_types():
        """Get list of supported bot types."""
        return sorted(list(ServiceFactory.ALL_SERVICES))

    @staticmethod
    def is_cli_service(bot_type: str) -> bool:
        """Check if bot type is a CLI service."""
        return bot_type in ServiceFactory.CLI_SERVICES

    @staticmethod
    def is_api_service(bot_type: str) -> bool:
        """Check if bot type is an API service."""
        return bot_type in ServiceFactory.API_SERVICES

    @staticmethod
    def get_service(bot_type: str, bot_id: str, work_dir: Optional[Union[str, Path]] = None):
        """
        Create and return appropriate service for bot type.
        
        Args:
            bot_type: Type of bot ('claude', 'chatgpt', 'claude-code', 'codex', 'llama')
            bot_id: ID of the bot instance
            work_dir: Working directory (required for CLI services)
            
        Returns:
            Service instance (LLM service or CLI adapter)
            
        Raises:
            ValueError: If bot_type is not supported
        """
        if bot_type not in ServiceFactory.ALL_SERVICES:
            raise ValueError(f"Unsupported bot type: {bot_type}")

        # CLI Services
        if bot_type == 'claude-code':
            from deia.adapters.claude_code_cli_adapter import ClaudeCodeCLIAdapter
            if work_dir is None:
                work_dir = Path.cwd()
            return ClaudeCodeCLIAdapter(bot_id=bot_id, work_dir=Path(work_dir))
        
        elif bot_type == 'codex':
            from deia.adapters.codex_cli_adapter import CodexCLIAdapter
            if work_dir is None:
                work_dir = Path.cwd()
            return CodexCLIAdapter(bot_id=bot_id, work_dir=Path(work_dir))
        
        # API Services
        elif bot_type == 'claude':
            from deia.services.llm_service import AnthropicService
            return AnthropicService()
        
        elif bot_type == 'chatgpt':
            from deia.services.llm_service import OpenAIService
            return OpenAIService()
        
        elif bot_type in ('llama', 'ollama'):
            from deia.services.llm_service import OllamaService
            return OllamaService()
        
        elif bot_type == 'deepseek':
            from deia.services.llm_service import DeepSeekService
            return DeepSeekService()
        
        else:
            raise ValueError(f"No implementation for bot type: {bot_type}")
