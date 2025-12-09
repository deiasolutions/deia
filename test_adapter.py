#!/usr/bin/env python3
"""Test adapter initialization directly."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deia.adapters.claude_code_adapter import ClaudeCodeAdapter

API_KEY = "SCRUBBED_USE_ENV_VAR"

print("Testing ClaudeCodeAdapter...")
print(f"API key: {API_KEY[:20]}...")

try:
    adapter = ClaudeCodeAdapter(
        bot_id="TEST-BOT",
        work_dir=Path.cwd(),
        api_key=API_KEY
    )
    print("[OK] Adapter initialized successfully")

    print("Starting session...")
    success = adapter.start_session()
    print(f"[OK] Session started: {success}")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
