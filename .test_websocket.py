#!/usr/bin/env python3
"""Test WebSocket functionality with the ServiceFactory fix"""

import asyncio
import websockets
import json

async def test_websocket():
    """Test WebSocket message passing"""
    uri = "ws://127.0.0.1:8899/ws?token=dev-token-12345"

    try:
        async with websockets.connect(uri) as websocket:
            print("[WS] Connected!")

            # Test 1: Send a query to a bot (use one that's in the registry)
            message = {
                "type": "query",
                "query": "Hello, can you introduce yourself?",
                "bot_id": "BOT-001"
            }

            print(f"[WS] Sending: {json.dumps(message)}")
            await websocket.send(json.dumps(message))

            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10)
                print(f"[WS] Response: {response}")
                data = json.loads(response)
                print(f"[WS] Parsed: {json.dumps(data, indent=2)}")
            except asyncio.TimeoutError:
                print("[WS] ⚠️ Timeout waiting for response (10 seconds)")
            except Exception as e:
                print(f"[WS] Error receiving: {e}")

    except Exception as e:
        print(f"[WS] Connection error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_websocket())
