"""
Simple mock bot service that responds to messages.
Used for testing the chat interface without full DEIA bot infrastructure.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI()

class Message(BaseModel):
    content: str

class ChatResponse(BaseModel):
    status: str
    message: str
    timestamp: str

# Simple in-memory message history
messages = []

@app.get("/")
async def root():
    return {"status": "ok", "bot": "mock-bot"}

@app.get("/status")
async def status():
    return {"status": "ready", "current_task": None}

@app.post("/message")
async def send_message(msg: Message):
    """Receive a message and respond"""
    messages.append({"role": "user", "content": msg.content})

    # Simple mock responses
    responses = {
        "hello": "Hello! I'm a mock bot. How can I help?",
        "hi": "Hi there! What can I do for you?",
        "how are you": "I'm doing great! Ready to chat!",
        "test": "Test successful! I'm responding normally.",
        "what is your name": "I'm Mock Bot, here to test the chat interface.",
    }

    # Find matching response
    user_input = msg.content.lower()
    response_text = "I received your message: \"" + msg.content + "\". This is a mock response!"

    for key, value in responses.items():
        if key in user_input:
            response_text = value
            break

    messages.append({"role": "bot", "content": response_text})

    return ChatResponse(
        status="success",
        message=response_text,
        timestamp=datetime.now().isoformat()
    )

@app.get("/messages")
async def get_messages():
    """Get all messages in conversation"""
    return {"messages": messages, "count": len(messages)}

@app.post("/terminate")
async def terminate():
    """Graceful shutdown endpoint"""
    return {"status": "terminating", "message": "Bot shutting down"}

if __name__ == "__main__":
    import uvicorn
    import os

    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8003))

    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
