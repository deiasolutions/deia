"""Chat Interface App"""

import json
import logging
from typing import Dict, List
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse

from deia.services.agent_coordinator import AgentCoordinator
from deia.services.agent_status import AgentStatusTracker
from deia.services.deia_context import DEIAContextLoader

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

status_tracker = AgentStatusTracker()
context_loader = DEIAContextLoader()
agent_coordinator = AgentCoordinator(status_tracker, context_loader)

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

        # Basic token validation (in production, validate against database/JWT/etc)
        if len(token) < 10:
            await websocket.close(code=1008, reason="Authentication required: invalid token")
            logger.warning(f"WebSocket connection rejected: invalid token format")
            return

        # TODO: Add real token validation here
        # For now, accept any token >= 10 chars as valid

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
                    result = process_query(query)
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
    # TODO: Implement local query handling logic
    return "This is a placeholder response for local query handling."

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
