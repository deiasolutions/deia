# TASK: BOT-004 - Service Factory (Cover for BOT-001)

**Priority:** P1 CRITICAL
**Time Estimate:** 45 minutes
**Start:** NOW (BOT-001 unavailable)
**Status:** REASSIGNED from BOT-001

---

## CONTEXT

BOT-001 is out of service for 45 minutes. This is BOT-001's assigned work, now reassigned to BOT-004 to keep progress moving.

**Original Task:** `.deia/hive/tasks/2025-10-26-BOT-001-SERVICE-FACTORY.md`
**Reassigned To:** BOT-004 (this task)
**Will Hand Off To:** BOT-003 continues as planned after this completes

---

## OBJECTIVE

Create ServiceFactory class and update task endpoint to enable all 5 bot types to be called from the chat interface.

---

## PART 1: Create Service Factory

**File:** `src/deia/services/service_factory.py`

```python
"""
Service Factory - Create LLM service instances by type

Maps bot_type to service class and returns configured instance.
Handles initialization with proper parameters.
"""

import os
from pathlib import Path
from typing import Optional, Union
from enum import Enum

from deia.services.llm_service import (
    AnthropicService,
    OpenAIService,
    OllamaService
)
from deia.adapters.claude_code_cli_adapter import ClaudeCodeCLIAdapter
from deia.adapters.codex_cli_adapter import CodexCLIAdapter


class BotType(str, Enum):
    """Supported bot types"""
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    CLAUDE_CODE = "claude-code"
    CODEX = "codex"
    LLAMA = "llama"


class ServiceFactory:
    """
    Factory for creating LLM service instances.

    Maps bot_type to service class and handles initialization.
    """

    @staticmethod
    def get_service(bot_type: str,
                   bot_id: str,
                   work_dir: Optional[Path] = None) -> Union[AnthropicService, OpenAIService, OllamaService, ClaudeCodeCLIAdapter, CodexCLIAdapter]:
        """
        Get service instance for bot type.

        Args:
            bot_type: Type of bot (claude, chatgpt, claude-code, codex, llama)
            bot_id: Bot ID for initialization
            work_dir: Working directory for CLI-based services

        Returns:
            Service instance of appropriate type

        Raises:
            ValueError: If bot_type is invalid
        """
        bot_type = bot_type.lower().strip()

        if bot_type == BotType.CLAUDE:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            return AnthropicService(
                api_key=api_key,
                model="claude-3-5-sonnet-20241022"
            )

        elif bot_type == BotType.CHATGPT:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            return OpenAIService(
                api_key=api_key,
                model="gpt-4"
            )

        elif bot_type == BotType.CLAUDE_CODE:
            if not work_dir:
                work_dir = Path.cwd()
            return ClaudeCodeCLIAdapter(
                bot_id=bot_id,
                work_dir=work_dir,
                claude_cli_path="claude"
            )

        elif bot_type == BotType.CODEX:
            if not work_dir:
                work_dir = Path.cwd()
            return CodexCLIAdapter(
                bot_id=bot_id,
                work_dir=work_dir,
                codex_cli_path="codex"
            )

        elif bot_type == BotType.LLAMA:
            # Ollama defaults to localhost:11434
            return OllamaService(
                model="qwen2.5-coder:7b"
            )

        else:
            raise ValueError(f"Unknown bot_type: {bot_type}. Must be one of: {', '.join([t.value for t in BotType])}")

    @staticmethod
    def get_supported_types():
        """Return list of supported bot types."""
        return [t.value for t in BotType]

    @staticmethod
    def is_cli_service(bot_type: str) -> bool:
        """Check if bot_type is CLI-based (needs subprocess)."""
        bot_type = bot_type.lower().strip()
        return bot_type in [BotType.CLAUDE_CODE, BotType.CODEX]

    @staticmethod
    def is_api_service(bot_type: str) -> bool:
        """Check if bot_type is API-based (uses FileOperationService)."""
        bot_type = bot_type.lower().strip()
        return bot_type in [BotType.CLAUDE, BotType.CHATGPT, BotType.LLAMA]
```

---

## PART 2: Update Task Endpoint

**File:** `src/deia/services/chat_interface_app.py`

**Location:** Find `@app.post("/api/bot/{bot_id}/task")` and `async def send_bot_task()` (around line 624)

**Replace the entire function with:**

```python
@app.post("/api/bot/{bot_id}/task")
async def send_bot_task(bot_id: str, request: BotTaskRequest):
    """
    Send a command/task to a bot of any type.

    Routes to appropriate service (Claude, ChatGPT, Claude Code, Codex, LLaMA)
    based on bot_type stored in registry metadata.

    Args:
        bot_id: Bot ID to send command to
        request: {"command": "some command"}

    Returns:
        {"success": true, "response": "...", "bot_type": "claude"}  or error
    """
    try:
        from deia.services.service_factory import ServiceFactory

        bot_id = bot_id.strip()
        command = request.command.strip()

        if not command:
            return {
                "success": False,
                "error": "command cannot be empty",
                "timestamp": datetime.now().isoformat()
            }

        # Get bot info from registry
        bot_info = service_registry.get_bot(bot_id)
        if not bot_info:
            return {
                "success": False,
                "error": f"Bot {bot_id} not found",
                "timestamp": datetime.now().isoformat()
            }

        # Get bot_type from metadata
        metadata = bot_info.get("metadata", {})
        bot_type = metadata.get("bot_type", "claude")  # Default to claude

        logger.info(f"Sending task to {bot_id} ({bot_type}): {command[:50]}...")

        try:
            # Get service instance
            service = ServiceFactory.get_service(
                bot_type=bot_type,
                bot_id=bot_id,
                work_dir=Path.cwd()
            )

            # Call appropriate method based on service type
            if ServiceFactory.is_cli_service(bot_type):
                # CLI services (Claude Code, Codex)
                # Start session if not already started
                if not hasattr(service, 'session_active') or not service.session_active:
                    if not service.start_session():
                        return {
                            "success": False,
                            "error": f"Failed to start {bot_type} session",
                            "timestamp": datetime.now().isoformat()
                        }

                # Send task to CLI service
                result = service.send_task(command, timeout=30)

                return {
                    "success": result.get("success", False),
                    "bot_id": bot_id,
                    "bot_type": bot_type,
                    "response": result.get("output", ""),
                    "files_modified": result.get("files_modified", []),
                    "error": result.get("error"),
                    "timestamp": datetime.now().isoformat()
                }

            else:
                # API services (Claude, ChatGPT, LLaMA)
                response = service.chat(command)

                return {
                    "success": True,
                    "bot_id": bot_id,
                    "bot_type": bot_type,
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as service_error:
            logger.error(f"Service error for {bot_type}: {service_error}")
            return {
                "success": False,
                "error": f"{bot_type} service error: {str(service_error)}",
                "timestamp": datetime.now().isoformat()
            }

    except Exception as e:
        logger.error(f"Error in send_bot_task: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

---

## PART 3: Add Import at Top of File

**Location:** `src/deia/services/chat_interface_app.py` imports section (top)

**Add:**
```python
from pathlib import Path
```

(Should be near other imports like `from datetime import datetime`)

---

## TESTING

**Run these tests to verify:**

```bash
# Test service factory
pytest tests/unit/test_service_factory.py -v

# Test task endpoint with different bot types
pytest tests/unit/test_chat_api_endpoints.py::TestBotTaskEndpoint -v
```

---

## DONE CHECKLIST

- [ ] Create `src/deia/services/service_factory.py` with ServiceFactory class
- [ ] Update `send_bot_task()` function in `chat_interface_app.py`
- [ ] Add Path import to `chat_interface_app.py`
- [ ] Verify imports work (no syntax errors)
- [ ] Tests pass
- [ ] Create completion report

---

## COMPLETION

When finished, create: `.deia/hive/responses/deiasolutions/bot-004-service-factory-cover-done.md`

Write:
- Service factory created successfully
- Task endpoint updated to route by bot_type
- Tests passing
- Ready for BOT-003 (signal for service integration to proceed)

---

## NOTE

This is BOT-001's work being done by BOT-004 due to BOT-001 unavailability.
After completion, BOT-003 will proceed with service integration as originally planned.
