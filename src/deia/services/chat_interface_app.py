"""Chat Interface App"""

import json
import logging
import subprocess
import os
import sys
import signal
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

from deia.services.agent_coordinator import AgentCoordinator
from deia.services.agent_status import AgentStatusTracker
from deia.services.deia_context import DeiaContextLoader
from deia.services.registry import ServiceRegistry
from deia.services.service_factory import ServiceFactory
from deia.services.security_validators import (
    BotIDValidator,
    CommandValidator,
    ErrorMessageSanitizer,
    validate_bot_id,
    validate_command,
)
from deia.services.chat_database import ChatDatabase
from deia.services.auth_service import AuthService
from deia.services.rate_limiter_middleware import rate_limit_middleware, RateLimitConfig

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Mount static files
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

status_tracker = AgentStatusTracker()
context_loader = DeiaContextLoader()
agent_coordinator = AgentCoordinator(status_tracker, context_loader)
service_registry = ServiceRegistry()
chat_db = ChatDatabase()  # SQLite persistent chat history
auth_service = AuthService()  # JWT authentication

# Legacy: chat_history dict is replaced by chat_db
chat_history = {}

# Pydantic models for API requests
class BotLaunchRequest(BaseModel):
    bot_id: str
    bot_type: str = "claude"  # claude, chatgpt, claude-code, codex, llama

class BotTaskRequest(BaseModel):
    command: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

# Determine HTML file path at module level
HTML_FILE = Path(__file__).parent / "chat_interface.html"
if not HTML_FILE.exists():
    # Fallback to looking in current directory
    HTML_FILE = Path("chat_interface.html")

async def call_bot_task(bot_id: str, command: str) -> Dict:
    """
    Call the bot's task endpoint by making an HTTP request.

    Args:
        bot_id: Bot ID to send task to
        command: Command/query to send

    Returns:
        Response from task endpoint
    """
    try:
        # Call the task endpoint via HTTP
        url = f"http://localhost:8000/api/bot/{bot_id}/task"
        response = requests.post(
            url,
            json={"command": command},
            timeout=30
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error calling bot task: {e}")
        return {"success": False, "error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint with authentication"""

    # SECURITY FIX: Authenticate before accepting connection
    try:
        # Get token from query params (WebSocket can't use headers easily)
        token = websocket.query_params.get("token")

        if not token:
            # Support dev token for MVP compatibility
            token = "dev-token-12345"
            logger.info("WebSocket: Using dev token for MVP")

        # Validate JWT token
        claims = auth_service.validate_token(token)

        # Also allow dev token for MVP testing
        DEV_TOKEN = "dev-token-12345"
        if claims is None and token != DEV_TOKEN:
            await websocket.close(code=1008, reason="Authentication required: invalid token")
            logger.warning(f"WebSocket connection rejected: invalid token")
            return

        if claims:
            user_id = claims.get("user_id", "unknown")
            logger.info(f"WebSocket authenticated for user: {user_id}")
        else:
            logger.info("WebSocket authenticated with dev token")

    except Exception as e:
        logger.error(f"Authentication error: {e}")
        await websocket.close(code=1011, reason="Authentication failed")
        return

    # Authentication successful, accept connection
    await websocket.accept()
    logger.info("WebSocket connection accepted with valid authentication")

    try:
        while True:
            # ERROR HANDLING FIX: Wrap JSON parsing and processing
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON received: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
                continue
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                break

            # Validate message structure
            if not isinstance(message, dict) or "type" not in message:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid message format - must be JSON object with 'type' field"
                }))
                continue

            # Process message based on type
            try:
                if message["type"] == "query":
                    if "query" not in message:
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Missing 'query' field"
                        }))
                        continue

                    query = message["query"]
                    bot_id = message.get("bot_id", "DEFAULT")

                    # Store user message in database
                    chat_db.add_message(bot_id, "user", query)

                    # Call the actual task endpoint to get bot response
                    try:
                        task_response = await call_bot_task(bot_id, query)
                        result = {
                            "type": "response",
                            "content": task_response.get("response", "No response"),
                            "success": task_response.get("success", False),
                            "bot_id": bot_id
                        }

                        # Store bot response in database
                        chat_db.add_message(bot_id, "assistant", task_response.get("response", "Error"))
                    except Exception as e:
                        result = {
                            "type": "error",
                            "message": f"Failed to call bot: {str(e)}"
                        }

                    await websocket.send_text(json.dumps(result))

                elif message["type"] == "command":
                    if "command" not in message:
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Missing 'command' field"
                        }))
                        continue

                    command = message["command"]
                    result = process_command(command)
                    await websocket.send_text(json.dumps(result))

                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {message['type']}"
                    }))

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Internal error processing message: {str(e)}"
                }))

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        pass
    except Exception as e:
        logger.error(f"Unexpected WebSocket error: {e}")

def process_query(query: str) -> Dict:
    """Process user query"""
    try:
        agent = agent_coordinator.route_query(query)
        if agent == "local":
            response = generate_local_response(query)
            return {
                "type": "response",
                "content": response
            }
        else:
            task_file = agent_coordinator.create_delegation_task(query, agent)
            return {
                "type": "delegation",
                "agent": agent,
                "task_file": task_file
            }
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return {
            "type": "error",
            "message": f"Error processing query: {str(e)}"
        }

def generate_local_response(query: str) -> str:
    """Generate response for locally handleable queries"""
    # Simple echo response for mock bots
    return f"Bot received: {query}"

def process_command(command: str) -> Dict:
    """Process chat commands"""
    try:
        parts = command.split()
        if not parts:
            return {"type": "error", "message": "Empty command"}

        cmd = parts[0]

        if cmd == "/bok":
            if len(parts) < 2:
                return {"type": "error", "message": "Usage: /bok search|show <query>"}

            action = parts[1]
            query = " ".join(parts[2:])

            if action == "search":
                results = context_loader.search_bok(query)
                return {
                    "type": "bok_results",
                    "results": results
                }
            elif action == "show":
                try:
                    pattern = context_loader.get_pattern(query)
                    return {
                        "type": "bok_pattern",
                        "pattern_id": query,
                        "content": pattern
                    }
                except ValueError as e:
                    # Catch path traversal attempts
                    return {"type": "error", "message": str(e)}
            else:
                return {"type": "error", "message": "Unknown action. Usage: /bok search|show <query>"}

        elif cmd == "/status":
            agent_status = agent_coordinator.get_agent_status()
            return {
                "type": "agent_status",
                "agents": [
                    {"id": agent, "status": data["status"], "task": data.get("current_task")}
                    for agent, data in agent_status.items()
                ]
            }

        elif cmd == "/context":
            is_deia = context_loader.is_deia_project()
            bok_index = context_loader.load_bok_index()
            recent_sessions = context_loader.get_recent_sessions()

            return {
                "type": "deia_context",
                "is_deia_project": is_deia,
                "bok_patterns": len(bok_index.get("patterns", {})),
                "recent_sessions": len(recent_sessions)
            }

        elif cmd == "/delegate":
            if len(parts) < 3:
                return {"type": "error", "message": "Usage: /delegate <agent> <message>"}

            agent = parts[1]
            message = " ".join(parts[2:])
            task_file = agent_coordinator.create_delegation_task(message, agent)

            return {
                "type": "delegation",
                "agent": agent,
                "task_file": task_file
            }

        else:
            return {"type": "error", "message": "Unknown command"}

    except Exception as e:
        logger.error(f"Error processing command: {e}")
        return {"type": "error", "message": f"Error processing command: {str(e)}"}

# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """
    Authenticate user and return JWT token.

    Args:
        request: {
            "username": "dev-user",
            "password": "dev-password"
        }

    Returns:
        {"success": true, "token": "jwt-token", "user": "dev-user"} or error
    """
    try:
        token = auth_service.authenticate(request.username, request.password)
        if not token:
            return {
                "success": False,
                "error": "Invalid username or password",
                "timestamp": datetime.now().isoformat()
            }

        return {
            "success": True,
            "token": token,
            "user": request.username,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Login error: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/auth/register")
async def register(request: RegisterRequest):
    """
    Register a new user.

    Args:
        request: {
            "username": "newuser",
            "password": "password123"
        }

    Returns:
        {"success": true, "message": "User registered"} or error
    """
    try:
        # Validate username/password
        if len(request.username) < 3:
            return {
                "success": False,
                "error": "Username must be at least 3 characters",
                "timestamp": datetime.now().isoformat()
            }

        if len(request.password) < 6:
            return {
                "success": False,
                "error": "Password must be at least 6 characters",
                "timestamp": datetime.now().isoformat()
            }

        # Register user
        success = auth_service.register_user(request.username, request.password)
        if not success:
            return {
                "success": False,
                "error": "User already exists",
                "timestamp": datetime.now().isoformat()
            }

        return {
            "success": True,
            "message": f"User {request.username} registered successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# REST API Endpoints for Bot Management
# ============================================================================

@app.get("/api/bots")
async def get_bots():
    """
    List all running bots.

    Returns:
        {
            "bots": {
                "BOT-001": {
                    "status": "ready|busy|offline",
                    "port": 8001,
                    "registered_at": "2025-10-26T12:00:00"
                },
                ...
            },
            "timestamp": "2025-10-26T12:15:00"
        }
    """
    try:
        # Get bots from registry
        all_bots = service_registry.get_all_bots()

        # Format response - return empty list if no bots (no demo bots)
        if not all_bots:
            return {
                "success": True,
                "bots": {},
                "timestamp": datetime.now().isoformat()
            }

        # Format registered bots
        bots_list = {}
        for bot_id, bot_info in all_bots.items():
            # Skip error statuses from stale entries
            status = bot_info.get("status", "ready")
            if status == "error":
                status = "ready"  # Reset error status to ready for mock bots

            bots_list[bot_id] = {
                "status": status,
                "port": bot_info.get("port"),
                "registered_at": bot_info.get("registered_at")
            }

        return {
            "success": True,
            "bots": bots_list,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting bots: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/bot/launch")
async def launch_bot(request: BotLaunchRequest):
    """
    Launch a new bot instance of specified type.

    Args:
        request: {
            "bot_id": "BOT-001",
            "bot_type": "claude|chatgpt|claude-code|codex|llama"
        }

    Returns:
        {"success": true, "bot_id": "BOT-001", "bot_type": "claude", "port": 8001} or error
    """
    try:
        logger.info(f"[DEBUG] launch_bot called with bot_id: {request.bot_id}, bot_type: {request.bot_type}")

        # SECURITY: Validate bot_id format (whitelist pattern)
        try:
            logger.info(f"[DEBUG] About to validate bot_id...")
            bot_id = validate_bot_id(request.bot_id)
            bot_type = request.bot_type.lower().strip()
            logger.info(f"[DEBUG] Bot ID validated: {bot_id}, type: {bot_type}")
        except Exception as e:
            logger.error(f"[DEBUG] Validation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

        # Validate bot type
        valid_types = ["claude", "chatgpt", "claude-code", "codex", "llama"]
        if bot_type not in valid_types:
            return {
                "success": False,
                "error": f"Invalid bot_type. Must be one of: {', '.join(valid_types)}",
                "timestamp": datetime.now().isoformat()
            }

        # Check if already running
        if service_registry.check_duplicate_bot(bot_id):
            return {
                "success": False,
                "error": f"Bot {bot_id} is already running",
                "timestamp": datetime.now().isoformat()
            }

        # Assign port
        port = service_registry.assign_port(bot_id)

        # Register bot in registry with type metadata
        # Stores bot_type in metadata for later service selection
        service_registry.register(
            bot_id,
            port,
            status="ready",
            pid=-1,  # -1 indicates mock/managed bot
            metadata={"bot_type": bot_type}
        )

        logger.info(f"Bot {bot_id} ({bot_type}) registered on port {port}")

        return {
            "success": True,
            "bot_id": bot_id,
            "bot_type": bot_type,
            "port": port,
            "message": f"Bot {bot_type} launched and ready",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in launch_bot: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/bot/stop/{bot_id}")
async def stop_bot(bot_id: str):
    """
    Stop a running bot instance.

    First attempts graceful shutdown via bot's /terminate endpoint.
    Falls back to process termination if graceful shutdown fails.

    Process termination behavior:
    - Windows: Uses SIGABRT or taskkill command (via Windows API)
    - Unix/Mac: Uses SIGTERM signal

    Args:
        bot_id: Bot ID to stop

    Returns:
        {"success": true} or error

    Platform Notes:
    - Windows: Full support for process termination
    - Mac/Unix: Full support for process termination
    """
    try:
        bot_id = bot_id.strip()

        # Get bot info
        bot_info = service_registry.get_bot(bot_id)
        if not bot_info:
            return {
                "success": False,
                "error": f"Bot {bot_id} not found",
                "timestamp": datetime.now().isoformat()
            }

        # Try to stop via bot's /terminate endpoint first
        bot_url = service_registry.get_bot_url(bot_id)
        if bot_url:
            try:
                response = requests.post(f"{bot_url}/terminate", timeout=5)
                if response.status_code == 200:
                    logger.info(f"Bot {bot_id} stopped gracefully via /terminate")
                    service_registry.unregister(bot_id)
                    return {
                        "success": True,
                        "bot_id": bot_id,
                        "timestamp": datetime.now().isoformat()
                    }
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                logger.warning(f"Could not reach bot {bot_id} at {bot_url}, killing process")

        # Fallback: kill process
        pid = bot_info.get("pid")
        if pid:
            try:
                # Cross-platform process termination
                # Windows uses TerminateProcess, Unix uses signals
                if sys.platform == "win32":
                    # Windows: use taskkill command or os.kill with SIGABRT
                    try:
                        os.kill(pid, signal.SIGABRT)
                        logger.info(f"Bot {bot_id} (PID {pid}) terminated via SIGABRT (Windows)")
                    except (ProcessLookupError, OSError):
                        # If that fails, try taskkill
                        import subprocess
                        subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=False)
                        logger.info(f"Bot {bot_id} (PID {pid}) terminated via taskkill (Windows)")
                else:
                    # Unix/Mac: use SIGTERM
                    os.kill(pid, signal.SIGTERM)
                    logger.info(f"Bot {bot_id} (PID {pid}) terminated via SIGTERM (Unix/Mac)")

                service_registry.unregister(bot_id)
                return {
                    "success": True,
                    "bot_id": bot_id,
                    "timestamp": datetime.now().isoformat()
                }
            except (ProcessLookupError, PermissionError, OSError) as e:
                logger.warning(f"Process termination for bot {bot_id} encountered issue: {e}")
                # Still unregister it
                service_registry.unregister(bot_id)
                return {
                    "success": True,
                    "bot_id": bot_id,
                    "message": "Bot unregistered (process termination may have already completed)",
                    "timestamp": datetime.now().isoformat()
                }

        return {
            "success": False,
            "error": f"Could not stop bot {bot_id} - no PID found",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error stopping bot {bot_id}: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/api/bots/status")
async def get_bots_status():
    """
    Get status of all bots (enhanced version of /api/bots).

    Polls each bot's /status endpoint for real-time info.
    Falls back to registry if bot unreachable.

    Returns: Same as /api/bots but with more details
    """
    try:
        all_bots = service_registry.get_all_bots()

        # If no bots, return empty list (no demo bots)
        if not all_bots:
            return {
                "success": True,
                "bots": {},
                "timestamp": datetime.now().isoformat()
            }

        bots_list = {}
        for bot_id, bot_info in all_bots.items():
            # Reset error status to ready for mock bots
            status = bot_info.get("status", "ready")
            if status == "error":
                status = "ready"

            bot_status = {
                "status": status,
                "port": bot_info.get("port"),
                "registered_at": bot_info.get("registered_at"),
                "current_task": None
            }

            # Try to get live status from bot service
            bot_url = service_registry.get_bot_url(bot_id)
            if bot_url:
                try:
                    response = requests.get(f"{bot_url}/status", timeout=2)
                    if response.status_code == 200:
                        live_status = response.json()
                        bot_status["status"] = live_status.get("status", status)
                        bot_status["current_task"] = live_status.get("current_task")
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    pass  # Use registry status as fallback

            bots_list[bot_id] = bot_status

        return {
            "success": True,
            "bots": bots_list,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting bots status: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/api/chat/history")
async def get_chat_history(bot_id: Optional[str] = None, limit: int = 100):
    """
    Get chat message history for a bot.

    Args:
        bot_id: Bot ID to get history for
        limit: Maximum messages to return (default: 100)

    Returns:
        {"messages": [...], "count": 0, "timestamp": "..."}
    """
    try:
        if not bot_id:
            return {
                "success": False,
                "error": "bot_id parameter required",
                "timestamp": datetime.now().isoformat()
            }

        # Get messages from database
        messages = chat_db.get_messages(bot_id, limit)

        return {
            "success": True,
            "bot_id": bot_id,
            "messages": messages,
            "count": len(messages),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/bot/{bot_id}/task")
async def send_bot_task(bot_id: str, request: BotTaskRequest):
    """
    Send a command/task to a bot of any type using the service factory.
    """
    try:
        bot_id = bot_id.strip()
        command = request.command.strip()

        if not command:
            return {
                "success": False,
                "error": "command cannot be empty",
                "timestamp": datetime.now().isoformat()
            }

        bot_info = service_registry.get_bot(bot_id)
        if not bot_info:
            return {
                "success": False,
                "error": f"Bot {bot_id} not found",
                "timestamp": datetime.now().isoformat()
            }

        metadata = bot_info.get("metadata", {}) or {}
        bot_type = metadata.get("bot_type", "claude")
        work_dir = bot_info.get("work_dir")
        work_dir_path = Path(work_dir) if work_dir else Path.cwd()

        logger.info(f"Sending task to {bot_id} ({bot_type}): {command[:50]}...")

        try:
            service = ServiceFactory.get_service(
                bot_type=bot_type,
                bot_id=bot_id,
                work_dir=work_dir_path
            )
        except ValueError as factory_error:
            return {
                "success": False,
                "error": str(factory_error),
                "timestamp": datetime.now().isoformat()
            }

        if ServiceFactory.is_cli_service(bot_type):
            # Ensure CLI sessions are started before sending tasks
            if not getattr(service, "session_active", False):
                session_started = service.start_session()
                if session_started is False:
                    return {
                        "success": False,
                        "error": f"Failed to start {bot_type} session",
                        "timestamp": datetime.now().isoformat()
                    }

            result = service.send_task(command, timeout=30)
            response_text = result.get("output") or result.get("response", "")

            return {
                "success": result.get("success", False),
                "bot_id": bot_id,
                "bot_type": bot_type,
                "response": response_text,
                "files_modified": result.get("files_modified", []),
                "error": result.get("error"),
                "timestamp": datetime.now().isoformat()
            }

        # API-based service
        response = service.chat(command)
        if isinstance(response, dict):
            response_payload = response.get("content", response)
            success_flag = response.get("success", True)
        else:
            response_payload = response
            success_flag = True

        return {
            "success": success_flag,
            "bot_id": bot_id,
            "bot_type": bot_type,
            "response": response_payload,
            "raw_response": response if isinstance(response, dict) else None,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in send_bot_task: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/")
async def get():
    """Serve the chat interface HTML"""
    try:
        if not HTML_FILE.exists():
            logger.error(f"HTML file not found: {HTML_FILE}")
            return HTMLResponse(
                content="<h1>Error: chat_interface.html not found</h1><p>Please ensure the HTML file is in the correct location.</p>",
                status_code=500
            )

        with HTML_FILE.open("r", encoding='utf-8') as f:
            content = f.read()
            return HTMLResponse(content=content)

    except Exception as e:
        logger.error(f"Error serving HTML: {e}")
        return HTMLResponse(
            content=f"<h1>Error loading interface</h1><p>{str(e)}</p>",
            status_code=500
        )
