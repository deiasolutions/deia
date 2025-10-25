"""
Llama Local Chatbot with Command Execution
FastAPI server with WebSocket support for real-time chat with local Llama model
"""

import asyncio
import json
import os
import sys
import subprocess
from typing import AsyncGenerator
from pathlib import Path
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

# Add parent directory to path for DEIA imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.deia.services.llm_service import OllamaService, ConversationHistory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Llama Local Chatbot")

# Configuration
LLAMA_ENDPOINT = os.getenv("LLAMA_ENDPOINT", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5-coder:7b")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

ALLOWED_COMMANDS = ['ls', 'cat', 'grep', 'find', 'python', 'git', 'pip', 'pytest', 'tree', 'dir', 'cd', 'pwd', 'type', 'findstr', 'echo', 'mkdir', 'rmdir', 'del', 'copy', 'move']
PROJECT_ROOT = Path(__file__).parent

# Initialize LLM service
llm_service = OllamaService(
    model=MODEL_NAME,
    base_url=f"{LLAMA_ENDPOINT}/v1",
    max_tokens=MAX_TOKENS,
    temperature=TEMPERATURE
)

# Track active connections and their conversation histories
active_connections: dict[WebSocket, ConversationHistory] = {}


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: int = 0


class CommandRequest(BaseModel):
    command: str


def is_safe_command(command: str) -> bool:
    base_cmd = command.strip().split()[0]
    if base_cmd not in ALLOWED_COMMANDS:
        return False
    dangerous = ['rm -rf', 'sudo', 'chmod 777', 'dd', '>', '>>', 'curl', 'wget', '&&', '||', ';', '|']
    return not any(pattern in command for pattern in dangerous)


# Removed old call_llama_api function - now using llm_service


@app.on_event("startup")
async def startup():
    logger.info("=" * 60)
    logger.info("LLAMA LOCAL CHATBOT WITH COMMAND EXECUTION")
    logger.info("=" * 60)
    logger.info(f"Model: {MODEL_NAME}")
    logger.info(f"Endpoint: {LLAMA_ENDPOINT}")
    logger.info(f"Temperature: {TEMPERATURE}")
    logger.info(f"Max Tokens: {MAX_TOKENS}")
    logger.info(f"Project Root: {PROJECT_ROOT}")
    logger.info("\nChecking Llama connection...")

    try:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{LLAMA_ENDPOINT}/api/tags", timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    models = await response.json()
                    available_models = [m["name"] for m in models.get("models", [])]
                    logger.info(f"✓ Connected to Ollama")
                    logger.info(f"Available models: {', '.join(available_models)}")

                    if MODEL_NAME not in available_models:
                        logger.warning(f"⚠ Warning: {MODEL_NAME} not found in available models")
                        logger.warning("Update MODEL_NAME environment variable to match your installed model")
                else:
                    logger.warning(f"⚠ Ollama not responding (status: {response.status})")
    except Exception as e:
        logger.error(f"⚠ Could not connect to Ollama: {e}")
        logger.warning("Make sure Ollama is running with: ollama serve")

    logger.info("\n" + "=" * 60)
    logger.info("Server ready!")
    logger.info("Chat available at: http://localhost:8000")
    logger.info("=" * 60 + "\n")


@app.get("/")
async def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Llama Chat with CLI</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .chat-container {
                width: 90%;
                max-width: 800px;
                height: 80vh;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }
            .chat-header h1 { font-size: 24px; margin-bottom: 5px; }
            .chat-header p { opacity: 0.9; font-size: 14px; }
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f8f9fa;
            }
            .message {
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
            }
            .message.user { justify-content: flex-end; }
            .message.assistant { justify-content: flex-start; }
            .message-content {
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 18px;
                word-wrap: break-word;
                white-space: pre-wrap;
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 14px;
            }
            .message.user .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 5px;
            }
            .message.assistant .message-content {
                background: white;
                color: #333;
                border: 1px solid #e1e5e9;
                border-bottom-left-radius: 5px;
            }
            .run-button {
                margin-top: 10px;
                padding: 6px 12px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12px;
                font-weight: 600;
                transition: all 0.2s;
            }
            .run-button:hover { background: #5568d3; transform: translateY(-1px); }
            .run-button:disabled { opacity: 0.6; cursor: not-allowed; }
            .chat-input-container {
                padding: 20px;
                background: white;
                border-top: 1px solid #e1e5e9;
            }
            .chat-input-wrapper { display: flex; gap: 10px; }
            .chat-input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e1e5e9;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            .chat-input:focus { border-color: #667eea; }
            .send-button {
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: transform 0.2s;
            }
            .send-button:hover { transform: translateY(-2px); }
            .send-button:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
            .typing-indicator {
                display: none;
                padding: 12px 16px;
                background: white;
                border: 1px solid #e1e5e9;
                border-radius: 18px;
                border-bottom-left-radius: 5px;
                color: #666;
                font-style: italic;
            }
            .typing-indicator.show { display: block; }
            .status {
                text-align: center;
                padding: 10px;
                font-size: 12px;
                color: #666;
                background: #f8f9fa;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h1>🦙 Llama Chat + CLI</h1>
                <p>Local AI with Command Execution</p>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message assistant">
                    <div class="message-content">Hello! I'm your local Llama assistant with CLI capabilities. I can help you with code and execute commands. Try asking me "How do I list Python files?"</div>
                </div>
            </div>
            <div class="typing-indicator" id="typingIndicator">Llama is thinking...</div>
            <div class="chat-input-container">
                <div class="chat-input-wrapper">
                    <input type="text" id="chatInput" class="chat-input" placeholder="Type your message..." autocomplete="off">
                    <button id="sendButton" class="send-button">Send</button>
                </div>
            </div>
            <div class="status" id="status">Connected</div>
        </div>

        <script>
            const chatMessages = document.getElementById('chatMessages');
            const chatInput = document.getElementById('chatInput');
            const sendButton = document.getElementById('sendButton');
            const typingIndicator = document.getElementById('typingIndicator');
            const status = document.getElementById('status');
            let ws = null;
            let isConnected = false;
            
            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = protocol + '//' + window.location.host + '/ws';
                console.log('[DEBUG] Connecting to WebSocket:', wsUrl);
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function() {
                    console.log('[DEBUG] WebSocket connected');
                    isConnected = true;
                    status.textContent = 'Connected';
                    sendButton.disabled = false;
                };
                
                ws.onmessage = function(event) {
                    console.log('[DEBUG] Received message:', event.data);
                    const data = JSON.parse(event.data);
                    if (data.type === 'response') {
                        console.log('[DEBUG] Response type, content length:', data.content.length);
                        hideTypingIndicator();
                        addMessage('assistant', data.content);
                        sendButton.disabled = false;
                    } else if (data.type === 'error') {
                        console.log('[DEBUG] Error type:', data.message);
                        hideTypingIndicator();
                        addMessage('assistant', 'Error: ' + data.message);
                        sendButton.disabled = false;
                    }
                };
                
                ws.onclose = function() {
                    console.log('[DEBUG] WebSocket closed');
                    isConnected = false;
                    status.textContent = 'Disconnected - Click Send to reconnect';
                    sendButton.disabled = false;
                };
                
                ws.onerror = function(error) {
                    console.error('[DEBUG] WebSocket error:', error);
                    status.textContent = 'Connection error';
                };
            }
            
            function addMessage(role, content) {
                console.log('[DEBUG] Adding message - Role:', role, 'Content length:', content.length);
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ' + role;
                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                contentDiv.textContent = content;
                messageDiv.appendChild(contentDiv);
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                if (role === 'assistant') {
                    console.log('[DEBUG] Enhancing code blocks for assistant message');
                    setTimeout(function() { enhanceCodeBlocks(contentDiv); }, 100);
                }
            }
            
            function enhanceCodeBlocks(messageBlock) {
                const content = messageBlock.textContent;
                if (messageBlock.querySelector('.run-button')) {
                    return;
                }
                const lines = content.split('\\n');
                for (let i = 0; i < lines.length; i++) {
                    const trimmedLine = lines[i].trim();
                    let command = null;
                    const firstChar = trimmedLine.charAt(0);
                    if (firstChar === '$' || firstChar === '#') {
                        command = trimmedLine.substring(1).trim();
                    } else {
                        const cmdRegex = /^(dir|cd|type|findstr|ls|cat|grep|find|python|git|pip|pytest|tree|pwd)\\s+/;
                        if (cmdRegex.test(trimmedLine)) {
                            command = trimmedLine;
                        }
                    }
                    if (command) {
                        console.log('[DEBUG] Detected command:', command);
                        const runBtn = document.createElement('button');
                        runBtn.textContent = '▶ Run';
                        runBtn.className = 'run-button';
                        runBtn.onclick = function() { executeCommand(command, messageBlock); };
                        messageBlock.appendChild(runBtn);
                        break;
                    }
                }
            }
            
            async function executeCommand(command, messageBlock) {
                console.log('[DEBUG] Executing command:', command);
                const runBtn = messageBlock.querySelector('.run-button');
                if (runBtn) {
                    runBtn.disabled = true;
                    runBtn.textContent = '⏳ Running...';
                }
                if (!confirm('Run this command?\\n\\n' + command + '\\n\\nIn: Project directory')) {
                    if (runBtn) {
                        runBtn.disabled = false;
                        runBtn.textContent = '▶ Run';
                    }
                    return;
                }
                try {
                    const response = await fetch('/api/execute', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({command: command})
                    });
                    const result = await response.json();
                    let output = '--- Command Output ---\\n$ ' + command + '\\n\\n';
                    if (result.success) {
                        output += result.stdout || '(no output)';
                    } else {
                        output += 'ERROR: ' + (result.error || result.stderr);
                    }
                    addMessage('assistant', output);
                    if (runBtn) {
                        runBtn.textContent = '✓ Done';
                        runBtn.style.background = '#28a745';
                    }
                } catch (error) {
                    addMessage('assistant', 'Failed to execute: ' + error.message);
                    if (runBtn) {
                        runBtn.disabled = false;
                        runBtn.textContent = '▶ Run';
                    }
                }
            }
            
            function showTypingIndicator() {
                typingIndicator.classList.add('show');
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            function hideTypingIndicator() {
                typingIndicator.classList.remove('show');
            }
            
            function sendMessage() {
                console.log('[DEBUG] sendMessage called');
                const message = chatInput.value.trim();
                console.log('[DEBUG] Message:', message);
                console.log('[DEBUG] isConnected:', isConnected);
                if (!message || !isConnected) {
                    console.log('[DEBUG] Message empty or not connected, reconnecting...');
                    if (!isConnected) {
                        connectWebSocket();
                    }
                    return;
                }
                console.log('[DEBUG] Adding user message and sending to server');
                addMessage('user', message);
                chatInput.value = '';
                
                if (message.startsWith('!')) {
                    console.log('[DEBUG] Direct command detected, showing as system message');
                    showTypingIndicator();
                } else {
                    sendButton.disabled = true;
                    showTypingIndicator();
                }
                
                const payload = JSON.stringify({type: 'message', content: message});
                console.log('[DEBUG] Sending payload:', payload);
                ws.send(payload);
            }
            
            sendButton.addEventListener('click', function() {
                console.log('[DEBUG] Send button clicked');
                sendMessage();
            });
            
            chatInput.addEventListener('keypress', function(e) {
                console.log('[DEBUG] Key pressed:', e.key);
                if (e.key === 'Enter') {
                    console.log('[DEBUG] Enter key detected');
                    sendMessage();
                }
            });
            
            console.log('[DEBUG] Initializing WebSocket connection on page load');
            connectWebSocket();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Create conversation history for this connection
    conversation_history = ConversationHistory(max_messages=20, max_tokens=4000)
    active_connections[websocket] = conversation_history

    logger.info("WebSocket connected")

    # Set system prompt
    system_prompt = "You are a helpful coding assistant running on Windows. When suggesting commands, use Windows commands (dir, type, findstr) not Unix commands (ls, cat, grep). Format commands clearly on their own line starting with $ or just the command itself."
    conversation_history.add_message("system", system_prompt)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data.get("type") == "message":
                user_message = message_data.get("content", "")

                # Check if message starts with ! for direct command execution
                if user_message.startswith("!"):
                    command = user_message[1:].strip()
                    logger.info(f"Direct command execution: {command}")

                    if not is_safe_command(command):
                        await websocket.send_text(
                            json.dumps({"type": "response", "content": f"Command not allowed: {command}"})
                        )
                        continue

                    try:
                        result = subprocess.run(
                            command, shell=True, capture_output=True, text=True, timeout=30, cwd=str(PROJECT_ROOT)
                        )
                        output = f"Command: !{command}\n\nOS responds:\n{result.stdout or '(no output)'}"
                        if result.returncode != 0:
                            output = f"Command: !{command}\n\nERROR (exit code {result.returncode}):\n{result.stderr or result.stdout}"

                        await websocket.send_text(json.dumps({"type": "response", "content": output}))
                    except subprocess.TimeoutExpired:
                        await websocket.send_text(
                            json.dumps({"type": "response", "content": "Command timed out (30s limit)"})
                        )
                    except Exception as e:
                        await websocket.send_text(
                            json.dumps({"type": "response", "content": f"Error: {str(e)}"})
                        )
                    continue

                # Use new streaming service
                try:
                    full_response = ""

                    # Stream response in real-time
                    async for chunk in llm_service.chat_stream(
                        user_message,
                        system_prompt=None,  # Already in conversation history
                        conversation_history=conversation_history.get_messages()[1:]  # Exclude system prompt
                    ):
                        if chunk:
                            full_response += chunk
                            # Send chunks in real-time for better UX
                            await websocket.send_text(
                                json.dumps({"type": "stream", "content": chunk})
                            )

                    # Add to conversation history
                    conversation_history.add_message("user", user_message)
                    conversation_history.add_message("assistant", full_response)

                    # Send completion signal
                    await websocket.send_text(
                        json.dumps({"type": "response", "content": full_response})
                    )

                    logger.info(f"User: {user_message}")
                    logger.info(f"Llama: {full_response[:100]}...")

                except Exception as e:
                    logger.error(f"Chat error: {e}", exc_info=True)
                    await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    finally:
        if websocket in active_connections:
            del active_connections[websocket]


@app.post("/api/execute")
async def execute_command(request: CommandRequest):
    command = request.command
    if not is_safe_command(command):
        return {"success": False, "error": "Command not allowed", "stdout": "", "stderr": ""}
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30, cwd=str(PROJECT_ROOT)
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out (30s limit)", "stdout": "", "stderr": ""}
    except Exception as e:
        return {"success": False, "error": str(e), "stdout": "", "stderr": ""}


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "endpoint": LLAMA_ENDPOINT,
        "active_connections": len(active_connections),
        "service": llm_service.__class__.__name__
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """REST API endpoint for chat (non-WebSocket)."""
    # Build conversation history
    history = [{"role": msg.role, "content": msg.content} for msg in request.history]

    try:
        # Use async chat method
        result = await llm_service.chat_async(
            user_message=request.message,
            system_prompt="You are a helpful AI assistant.",
            conversation_history=history
        )

        if result["success"]:
            return ChatResponse(
                response=result["content"],
                model=result["model"],
                tokens_used=result["tokens_used"]
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error_detail", "Unknown error"))

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting Llama Local Chatbot with CLI...")
    print("Make sure Ollama is running with your model")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", reload=False)
