#!/usr/bin/env python3
"""
Quick test of Claude Code Adapter - verifies it's actually calling the API.
"""

from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deia.adapters.claude_code_adapter import ClaudeCodeAdapter

def test_adapter_init():
    """Test that adapter initializes correctly."""
    print("Testing adapter initialization...")

    # Check if API key is set
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("✗ ANTHROPIC_API_KEY not set in environment")
        print("  Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        return False

    try:
        adapter = ClaudeCodeAdapter(
            bot_id="TEST-001",
            work_dir=Path.cwd(),
            model="claude-sonnet-4-20250514"
        )
        print(f"✓ Adapter initialized: bot_id={adapter.bot_id}")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return False

def test_session_start():
    """Test that session can start and communicate with API."""
    print("\nTesting session start (will make real API call)...")

    try:
        adapter = ClaudeCodeAdapter(
            bot_id="TEST-001",
            work_dir=Path.cwd(),
            model="claude-sonnet-4-20250514"
        )

        result = adapter.start_session()

        if result:
            print(f"✓ Session started successfully")
            print(f"  Started at: {adapter.started_at}")
            print(f"  Status: {adapter.get_session_info()['status']}")

            # Clean up
            adapter.stop_session()
            return True
        else:
            print("✗ Session did not start")
            return False

    except Exception as e:
        print(f"✗ Error during session start: {e}")
        return False

def test_send_simple_task():
    """Test sending a simple task to Claude."""
    print("\nTesting simple task execution (will make real API call)...")

    try:
        adapter = ClaudeCodeAdapter(
            bot_id="TEST-001",
            work_dir=Path.cwd(),
            model="claude-sonnet-4-20250514"
        )

        adapter.start_session()

        result = adapter.send_task("Respond with: 'Hello from Claude Code Adapter test!'")

        print(f"\nTask result:")
        print(f"  Success: {result['success']}")
        print(f"  Duration: {result['duration_seconds']}s")
        print(f"  Output: {result['output'][:100]}...")

        if result['error']:
            print(f"  Error: {result['error']}")

        adapter.stop_session()

        return result['success']

    except Exception as e:
        print(f"✗ Error during task execution: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Claude Code Adapter - Quick Test")
    print("=" * 60)

    results = []

    results.append(("Initialization", test_adapter_init()))

    if results[0][1]:  # Only continue if init worked
        results.append(("Session Start", test_session_start()))
        results.append(("Simple Task", test_send_simple_task()))

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    all_passed = all(r[1] for r in results)

    if all_passed:
        print("\n✓ All tests passed! Adapter is working with real API.")
    else:
        print("\n✗ Some tests failed. Check output above.")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
