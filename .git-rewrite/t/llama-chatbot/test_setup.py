#!/usr/bin/env python3
"""
Quick test script for Llama chatbot setup
"""

import asyncio
import aiohttp
import json


async def test_ollama_connection():
    """Test if Ollama is running and has the expected model"""
    endpoint = "http://localhost:11434"

    try:
        async with aiohttp.ClientSession() as session:
            # Test basic connection
            async with session.get(
                f"{endpoint}/api/tags", timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    models = await response.json()
                    available_models = [m["name"] for m in models.get("models", [])]
                    print("✅ Ollama is running!")
                    print(f"Available models: {', '.join(available_models)}")

                    # Check for Llama 34B
                    llama_models = [m for m in available_models if "34b" in m.lower()]
                    if llama_models:
                        print(f"✅ Found Llama 34B models: {', '.join(llama_models)}")
                        return True
                    else:
                        print("⚠️  No Llama 34B models found")
                        print("Available models:", available_models)
                        return False
                else:
                    print(f"❌ Ollama responded with status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Could not connect to Ollama: {e}")
        print("Make sure Ollama is running with: ollama serve")
        return False


async def test_chat_api():
    """Test the chat API with a simple message"""
    endpoint = "http://localhost:11434"
    model_name = "llama3.1:34b"  # Update this to match your model

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello in one word."},
    ]

    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 50},
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{endpoint}/api/chat", json=payload, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    response_text = data["message"]["content"]
                    print(f"✅ Chat API working! Response: {response_text}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Chat API error: {error_text}")
                    return False
    except Exception as e:
        print(f"❌ Chat API test failed: {e}")
        return False


async def main():
    print("🧪 Testing Llama Chatbot Setup")
    print("=" * 40)

    # Test 1: Ollama connection
    print("\n1. Testing Ollama connection...")
    ollama_ok = await test_ollama_connection()

    if not ollama_ok:
        print("\n❌ Setup incomplete. Please:")
        print("   - Start Ollama: ollama serve")
        print("   - Pull Llama 34B: ollama pull llama3.1:34b")
        return

    # Test 2: Chat API
    print("\n2. Testing chat API...")
    chat_ok = await test_chat_api()

    if chat_ok:
        print("\n✅ All tests passed!")
        print("You can now run: python app.py")
        print("Then open: http://localhost:8000")
    else:
        print("\n❌ Chat API test failed")
        print("Check your model name in the script")


if __name__ == "__main__":
    asyncio.run(main())

