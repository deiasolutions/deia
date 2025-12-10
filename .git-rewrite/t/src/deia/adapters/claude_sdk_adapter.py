"""
Claude SDK Adapter - Uses Anthropic's claude-agent-sdk for Claude Code integration.

Leverages official SDK for Claude Code communication, adds our multi-agent
orchestration layer on top (HTTP service, file-based tasks, registry).
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import asyncio
import time

try:
    from claude_agent_sdk import query, ClaudeSDKClient
except ImportError:
    raise ImportError(
        "claude-agent-sdk not installed. Install with: pip install claude-agent-sdk"
    )


class ClaudeSDKAdapter:
    """
    Adapter for Claude Code using official Anthropic SDK.

    Provides same interface as other adapters (ClaudeCodeAdapter, MockBotAdapter)
    but uses claude-agent-sdk under the hood for better Claude Code integration.

    Features:
    - Official SDK for Claude Code (no raw subprocess management)
    - Async streaming responses
    - Custom tools via MCP
    - Session management
    - Our multi-agent additions: health checks, status tracking
    """

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        **config
    ):
        """
        Initialize Claude SDK adapter.

        Args:
            bot_id: Unique bot identifier
            work_dir: Working directory for Claude Code
            **config: Additional configuration
                - model: Model to use (default: claude-sonnet-4.5)
                - max_iterations: Max agent loop iterations
                - custom_tools: List of custom MCP tools
        """
        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.config = config

        # SDK client (created on start_session)
        self.client: Optional[ClaudeSDKClient] = None
        self.session_active = False

        # Track last activity for health checks
        self.last_activity = None

        # Configuration
        self.model = config.get("model", "claude-sonnet-4.5")
        self.max_iterations = config.get("max_iterations", 50)
        self.custom_tools = config.get("custom_tools", [])

    def start_session(self) -> bool:
        """
        Start Claude Code session using SDK.

        Returns:
            True if started successfully
        """
        if self.session_active:
            return True

        try:
            # Initialize SDK client
            # Note: ClaudeSDKClient doesn't take cwd/model/max_iterations in __init__
            # These are passed to query() instead
            self.client = ClaudeSDKClient()

            # Register custom tools if provided
            for tool in self.custom_tools:
                # Tools should be registered via MCP server
                # SDK handles this via create_sdk_mcp_server()
                pass

            self.session_active = True
            self.last_activity = datetime.now()

            print(f"[{self.bot_id}] [SDK] Session started (model: {self.model})")
            return True

        except Exception as e:
            print(f"[{self.bot_id}] [SDK] Failed to start session: {e}")
            return False

    def stop_session(self) -> bool:
        """
        Stop Claude Code session.

        Returns:
            True if stopped successfully
        """
        if not self.session_active:
            return True

        try:
            # SDK doesn't have explicit cleanup, but we can close client
            if self.client:
                # Client is context manager, but we're not using 'with'
                # Just mark as inactive
                self.client = None

            self.session_active = False
            print(f"[{self.bot_id}] [SDK] Session stopped")
            return True

        except Exception as e:
            print(f"[{self.bot_id}] [SDK] Error stopping session: {e}")
            return False

    def send_task(self, task_content: str) -> Dict[str, Any]:
        """
        Send task to Claude Code via SDK.

        Args:
            task_content: Task prompt/content

        Returns:
            dict: {
                "success": bool,
                "response": str,
                "error": Optional[str],
                "duration_seconds": float
            }
        """
        if not self.session_active or not self.client:
            return {
                "success": False,
                "response": "",
                "error": "Session not active. Call start_session() first.",
                "duration_seconds": 0
            }

        start_time = time.time()

        try:
            # Use SDK's query with async event loop
            # Note: SDK query() is async, need to run in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            response_text = ""

            async def run_query():
                nonlocal response_text
                # Stream response messages
                async for message in query(
                    task_content,
                    cwd=str(self.work_dir),
                    model=self.model,
                    max_iterations=self.max_iterations
                ):
                    # Accumulate response text
                    if hasattr(message, 'content'):
                        response_text += str(message.content) + "\n"

            # Run async query
            loop.run_until_complete(run_query())
            loop.close()

            duration = time.time() - start_time
            self.last_activity = datetime.now()

            return {
                "success": True,
                "response": response_text.strip(),
                "error": None,
                "duration_seconds": duration
            }

        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)

            print(f"[{self.bot_id}] [SDK] Task execution error: {error_msg}")

            return {
                "success": False,
                "response": "",
                "error": error_msg,
                "duration_seconds": duration
            }

    def check_health(self) -> bool:
        """
        Check if adapter is healthy.

        Returns:
            True if healthy (session active and recent activity)
        """
        if not self.session_active:
            return False

        # Check if activity within last 5 minutes
        if self.last_activity:
            elapsed = (datetime.now() - self.last_activity).total_seconds()
            if elapsed > 300:  # 5 minutes
                print(f"[{self.bot_id}] [SDK] Health check: No activity for {elapsed}s")
                return False

        return True

    def get_session_info(self) -> Dict[str, Any]:
        """
        Get current session information.

        Returns:
            dict: Session metadata
        """
        return {
            "adapter_type": "claude_sdk",
            "session_active": self.session_active,
            "model": self.model,
            "max_iterations": self.max_iterations,
            "work_dir": str(self.work_dir),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }
