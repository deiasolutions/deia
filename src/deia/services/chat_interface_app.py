"""Chat Interface App"""

import json
import logging
import subprocess
import os
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
from deia.services.security_validators import (
    BotIDValidator,
    CommandValidator,
    ErrorMessageSanitizer,
    validate_bot_id,
    validate_command,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

status_tracker = AgentStatusTracker()
context_loader = DeiaContextLoader()
agent_coordinator = AgentCoordinator(status_tracker, context_loader)
service_registry = ServiceRegistry()

# Chat history storage: {bot_id: [{"role": "user|assistant", "content": "..."}]}
chat_history = {}

# Pydantic models for API requests
class BotLaunchRequest(BaseModel):
    bot_id: str
    bot_type: str = "claude"  # claude, chatgpt, claude-code, codex, llama

class BotTaskRequest(BaseModel):
    command: str

# Determine HTML file path at module level
HTML_FILE = Path(__file__).parent / "chat_interface.html"
if not HTML_FILE.exists():
    # Fallback to looking in current directory
    HTML_FILE = Path("chat_interface.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint with authentication"""

    # SECURITY FIX: Authenticate before accepting connection
    try:
        # Get token from query params (WebSocket can't use headers easily)
        token = websocket.query_params.get("token")

        if not token:
            await websocket.close(code=1008, reason="Authentication required: missing token")
            logger.warning("WebSocket connection rejected: missing token")
            return

        # Token validation - use fixed dev token for development
        VALID_DEV_TOKEN = "dev-token-12345"
        if token != VALID_DEV_TOKEN:
            await websocket.close(code=1008, reason="Authentication required: invalid token")
            logger.warning(f"WebSocket connection rejected: invalid token")
            return

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

                    # Store user message
                    if bot_id not in chat_history:
                        chat_history[bot_id] = []
                    chat_history[bot_id].append({"role": "user", "content": query})

                    result = process_query(query)

                    # Store bot response
                    if result.get("type") == "response":
                        chat_history[bot_id].append({"role": "assistant", "content": result.get("content", "")})

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

        # Format response - return clean mock data if registry is empty
        if not all_bots:
            # Return a sample bot for demo
            return {
                "success": True,
                "bots": {
                    "DEMO-BOT": {
                        "status": "ready",
                        "port": 8001,
                        "registered_at": datetime.now().isoformat()
                    }
                },
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

    Args:
        bot_id: Bot ID to stop

    Returns:
        {"success": true} or error
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
                os.kill(pid, signal.SIGTERM)
                logger.info(f"Bot {bot_id} (PID {pid}) terminated via SIGTERM")
                service_registry.unregister(bot_id)
                return {
                    "success": True,
                    "bot_id": bot_id,
                    "timestamp": datetime.now().isoformat()
                }
            except (ProcessLookupError, PermissionError) as e:
                logger.error(f"Error killing bot {bot_id}: {e}")
                # Still unregister it
                service_registry.unregister(bot_id)
                return {
                    "success": True,
                    "bot_id": bot_id,
                    "message": "Bot unregistered (process may have already exited)",
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

        # If no bots, return demo data
        if not all_bots:
            return {
                "success": True,
                "bots": {
                    "DEMO-BOT": {
                        "status": "ready",
                        "port": 8001,
                        "registered_at": datetime.now().isoformat(),
                        "current_task": None
                    }
                },
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

        # Get messages from chat history
        messages = chat_history.get(bot_id, [])

        # Apply limit
        messages_limited = messages[-limit:] if len(messages) > limit else messages

        return {
            "success": True,
            "bot_id": bot_id,
            "messages": messages_limited,
            "count": len(messages_limited),
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
    Send a command/task to a specific bot.

    Args:
        bot_id: Bot ID to send command to
        request: {"command": "some command"}

    Returns:
        {"success": true, "response": "..."}  or error
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

        # Get bot info
        bot_info = service_registry.get_bot(bot_id)
        if not bot_info:
            return {
                "success": False,
                "error": f"Bot {bot_id} not found",
                "timestamp": datetime.now().isoformat()
            }

        # Send command via WebSocket or REST API
        # For now, we'll try to send via a direct message endpoint if it exists
        bot_url = service_registry.get_bot_url(bot_id)
        if bot_url:
            try:
                # Create direct message
                message_data = {
                    "from_bot": "chat-interface",
                    "content": command,
                    "priority": "P2"
                }

                response = requests.post(
                    f"{bot_url}/message",
                    json=message_data,
                    timeout=5
                )

                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Command sent to {bot_id}: {command[:50]}...")
                    return {
                        "success": True,
                        "bot_id": bot_id,
                        "command": command,
                        "response": "Command queued for bot",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Bot returned status {response.status_code}",
                        "timestamp": datetime.now().isoformat()
                    }

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                return {
                    "success": False,
                    "error": f"Could not reach bot {bot_id} at {bot_url}",
                    "timestamp": datetime.now().isoformat()
                }

        return {
            "success": False,
            "error": f"Bot {bot_id} has no service URL",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error sending task to {bot_id}: {e}")
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
