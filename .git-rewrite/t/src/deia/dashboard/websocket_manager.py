"""
WebSocket Connection Manager

Manages WebSocket connections and broadcasts hive events to all connected clients.
"""

from fastapi import WebSocket
from typing import List, Dict, Any
import json


class ConnectionManager:
    """Manage WebSocket connections and broadcast events."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[OK] WebSocket connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"[OK] WebSocket disconnected: {websocket.client}")

    async def broadcast(self, event: Dict[str, Any]):
        """
        Broadcast event to all connected clients.

        Args:
            event: Event dictionary to send
        """
        if not self.active_connections:
            return

        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(event)
            except Exception as e:
                print(f"Failed to send to {connection.client}: {e}")
                disconnected.append(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """
        Send message to specific client.

        Args:
            message: Message dictionary
            websocket: Target WebSocket
        """
        await websocket.send_json(message)
