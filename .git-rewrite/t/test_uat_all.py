"""
UAT Test Suite - Multi-Agent Architecture
Run all tests and report results
"""

from pathlib import Path
import sys
import time

def test_1_service_registry():
    """Test 1: Service Registry"""
    print("\n=== TEST 1: Service Registry ===")

    try:
        from src.deia.services.registry import ServiceRegistry

        registry = ServiceRegistry()
        print("[PASS] ServiceRegistry initialized")

        port = registry.assign_port('deiasolutions-TEST-001')
        assert 8001 <= port <= 8999, f"Port {port} out of range"
        print(f"[PASS] Assigned port: {port}")

        registry.register('deiasolutions-TEST-001', port, repo='deiasolutions')
        print("[PASS] Bot registered")

        bot = registry.get_bot('deiasolutions-TEST-001')
        assert bot is not None, "Bot not found"
        assert bot['port'] == port, "Port mismatch"
        print(f"[PASS] Bot info retrieved")

        url = registry.get_bot_url('deiasolutions-TEST-001')
        assert url == f"http://localhost:{port}", f"URL mismatch: {url}"
        print(f"[PASS] Bot URL: {url}")

        registry_file = Path('.deia/hive/registry.json')
        assert registry_file.exists(), "Registry file not created"
        print("[PASS] Registry file exists")

        print("\nTEST 1: PASSED\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] TEST 1: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_2_bot_service():
    """Test 2: Bot Service HTTP API"""
    print("\n=== TEST 2: Bot Service HTTP API ===")

    try:
        from src.deia.services.bot_service import BotService
        import requests

        service = BotService('deiasolutions-TEST-002', 8051, Path.cwd())
        service.start()
        print("[PASS] Service started on port 8051")

        time.sleep(2)  # Let service start

        # Test health endpoint
        resp = requests.get('http://localhost:8051/health', timeout=5)
        assert resp.status_code == 200, f"Health check failed: {resp.status_code}"
        print(f"[PASS] /health endpoint: {resp.json()}")

        # Test status endpoint
        resp = requests.get('http://localhost:8051/status', timeout=5)
        assert resp.status_code == 200, f"Status check failed: {resp.status_code}"
        data = resp.json()
        assert data['bot_id'] == 'deiasolutions-TEST-002', "Bot ID mismatch"
        print(f"[PASS] /status endpoint: {data['status']}")

        # Test interrupt endpoint
        resp = requests.post('http://localhost:8051/interrupt', timeout=5)
        assert resp.status_code == 200, f"Interrupt failed: {resp.status_code}"
        print("[PASS] /interrupt endpoint")

        service.stop()
        print("[PASS] Service stopped")

        print("\nTEST 2: PASSED\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] TEST 2: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_3_mock_bot():
    """Test 3: Mock Bot with Service Integration"""
    print("\n=== TEST 3: Mock Bot with Service Integration ===")

    try:
        from src.deia.adapters.bot_runner import BotRunner
        from src.deia.services.registry import ServiceRegistry

        work_dir = Path.cwd()
        task_dir = work_dir / '.deia' / 'hive' / 'tasks' / 'deiasolutions-MOCK-001'
        response_dir = work_dir / '.deia' / 'hive' / 'responses'
        task_dir.mkdir(parents=True, exist_ok=True)
        response_dir.mkdir(parents=True, exist_ok=True)
        print("[PASS] Directories created")

        bot = BotRunner(
            bot_id='deiasolutions-MOCK-001',
            work_dir=work_dir,
            task_dir=task_dir,
            response_dir=response_dir,
            adapter_type='mock'
        )
        print("[PASS] BotRunner initialized")

        bot.start()
        print("[PASS] Bot started")

        # Check registry
        registry = ServiceRegistry()
        registered_bot = registry.get_bot('deiasolutions-MOCK-001')
        assert registered_bot is not None, "Bot not in registry"
        print(f"[PASS] Bot registered on port {registered_bot['port']}")

        # Get status
        status = bot.get_status()
        assert status['session_started'], "Session not started"
        print(f"[PASS] Bot status: {status['adapter_type']}")

        bot.stop()
        print("[PASS] Bot stopped")

        print("\nTEST 3: PASSED\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] TEST 3: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_4_claude_sdk_adapter():
    """Test 4: Claude SDK Adapter"""
    print("\n=== TEST 4: Claude SDK Adapter ===")

    try:
        from src.deia.adapters.bot_runner import BotRunner

        work_dir = Path.cwd()
        task_dir = work_dir / '.deia' / 'hive' / 'tasks' / 'deiasolutions-SDK-TEST-001'
        response_dir = work_dir / '.deia' / 'hive' / 'responses'
        task_dir.mkdir(parents=True, exist_ok=True)
        response_dir.mkdir(parents=True, exist_ok=True)
        print("[PASS] Directories created")

        # Try to create SDK adapter bot
        try:
            bot = BotRunner(
                bot_id='deiasolutions-SDK-TEST-001',
                work_dir=work_dir,
                task_dir=task_dir,
                response_dir=response_dir,
                adapter_type='sdk'
            )
            print("[PASS] BotRunner with SDK adapter initialized")
        except ImportError as e:
            print(f"[SKIP] SDK not available: {e}")
            print("\nTEST 4: SKIPPED (SDK not installed)\n")
            return None  # Skip test

        # Start bot
        bot.start()
        print("[PASS] SDK adapter session started")

        # Check session info
        session_info = bot.adapter.get_session_info()
        assert session_info['adapter_type'] == 'claude_sdk', "Wrong adapter type"
        assert session_info['session_active'], "Session not active"
        print(f"[PASS] Session info: {session_info['model']}")

        # Health check
        healthy = bot.adapter.check_health()
        assert healthy, "Health check failed"
        print("[PASS] Health check passed")

        bot.stop()
        print("[PASS] Bot stopped")

        print("\nTEST 4: PASSED\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] TEST 4: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_5_file_based_tasks():
    """Test 5: File-Based Task Assignment"""
    print("\n=== TEST 5: File-Based Task Assignment ===")

    try:
        from src.deia.adapters.bot_runner import BotRunner
        from datetime import datetime

        work_dir = Path.cwd()
        task_dir = work_dir / '.deia' / 'hive' / 'tasks' / 'deiasolutions-TASK-TEST-001'
        response_dir = work_dir / '.deia' / 'hive' / 'responses'
        task_dir.mkdir(parents=True, exist_ok=True)
        response_dir.mkdir(parents=True, exist_ok=True)
        print("[PASS] Directories created")

        # Create mock bot (with cooldown disabled for faster testing)
        bot = BotRunner(
            bot_id='deiasolutions-TASK-TEST-001',
            work_dir=work_dir,
            task_dir=task_dir,
            response_dir=response_dir,
            adapter_type='mock',
            task_cooldown_seconds=0  # Disable cooldown for testing
        )
        bot.start()
        print("[PASS] Mock bot started")

        # Create task file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        task_file = task_dir / f"{timestamp}-P1-test-task.md"
        task_content = f"""---
from: TEST-SCRUM-MASTER
to: deiasolutions-TASK-TEST-001
task_id: test-task-001
priority: P1
created_at: {datetime.now().isoformat()}
---

# Test Task

This is a test task to verify file-based task assignment.
"""
        task_file.write_text(task_content, encoding='utf-8')
        print(f"[PASS] Task file created: {task_file.name}")

        # Run one iteration
        result = bot.run_once()
        assert result['task_found'], "Task not found"
        assert result['task_executed'], "Task not executed"
        assert result['task_id'] == 'test-task-001', "Wrong task ID"
        print("[PASS] Task executed")

        # Check response file created (pattern includes shortened task ID)
        response_files = list(response_dir.glob("*-RESPONSE-*-complete.md"))
        assert len(response_files) > 0, f"Response file not created (found: {list(response_dir.glob('*.md'))})"
        # Verify it's for our test
        response_content = response_files[-1].read_text()  # Get most recent
        assert "test-task-001" in response_content, "Wrong task in response"
        print(f"[PASS] Response file created: {response_files[-1].name}")

        # Verify task tracking works
        assert len(bot.processed_tasks) > 0, "No tasks tracked"
        print(f"[PASS] Task tracking: {len(bot.processed_tasks)} task(s) tracked")

        bot.stop()
        print("[PASS] Bot stopped")

        print("\nTEST 5: PASSED\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] TEST 5: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_6_http_control():
    """Test 6: HTTP Control Endpoints"""
    print("\n=== TEST 6: HTTP Control Endpoints ===")

    try:
        from src.deia.adapters.bot_runner import BotRunner
        import requests

        work_dir = Path.cwd()
        task_dir = work_dir / '.deia' / 'hive' / 'tasks' / 'deiasolutions-HTTP-TEST-001'
        response_dir = work_dir / '.deia' / 'hive' / 'responses'
        task_dir.mkdir(parents=True, exist_ok=True)
        response_dir.mkdir(parents=True, exist_ok=True)
        print("[PASS] Directories created")

        # Start mock bot
        bot = BotRunner(
            bot_id='deiasolutions-HTTP-TEST-001',
            work_dir=work_dir,
            task_dir=task_dir,
            response_dir=response_dir,
            adapter_type='mock'
        )
        bot.start()
        print(f"[PASS] Bot started on port {bot.port}")

        time.sleep(2)  # Let service start

        bot_url = f"http://localhost:{bot.port}"

        # Test direct message endpoint
        resp = requests.post(
            f"{bot_url}/message",
            json={
                "from_bot": "TEST-SCRUM-MASTER",
                "content": "Test message",
                "priority": "P0"
            },
            timeout=5
        )
        assert resp.status_code == 200, f"Message failed: {resp.status_code}"
        print("[PASS] /message endpoint")

        # Test getting messages
        resp = requests.get(f"{bot_url}/messages", timeout=5)
        assert resp.status_code == 200, f"Get messages failed: {resp.status_code}"
        messages = resp.json().get('messages', [])
        assert len(messages) > 0, "No messages received"
        print(f"[PASS] /messages endpoint: {len(messages)} message(s)")

        # Test interrupt (already tested in Test 2, but verify again)
        resp = requests.post(f"{bot_url}/interrupt", timeout=5)
        assert resp.status_code == 200, f"Interrupt failed: {resp.status_code}"
        print("[PASS] /interrupt endpoint verified")

        bot.stop()
        print("[PASS] Bot stopped")

        print("\nTEST 6: PASSED\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] TEST 6: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all UAT tests"""
    print("=" * 60)
    print("MULTI-AGENT ARCHITECTURE - UAT TEST SUITE")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Service Registry", test_1_service_registry()))
    results.append(("Bot Service HTTP API", test_2_bot_service()))
    results.append(("Mock Bot Integration", test_3_mock_bot()))
    results.append(("Claude SDK Adapter", test_4_claude_sdk_adapter()))
    results.append(("File-Based Task Assignment", test_5_file_based_tasks()))
    results.append(("HTTP Control Endpoints", test_6_http_control()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for name, passed in results:
        if passed is None:
            status = "SKIPPED"
        elif passed:
            status = "PASSED"
        else:
            status = "FAILED"
        print(f"{name}: {status}")

    passed_count = sum(1 for _, p in results if p is True)
    failed_count = sum(1 for _, p in results if p is False)
    skipped_count = sum(1 for _, p in results if p is None)
    total_count = len(results)

    print(f"\nTotal: {passed_count} passed, {failed_count} failed, {skipped_count} skipped")

    if failed_count == 0:
        print("\nALL TESTS PASSED (or skipped)")
        return 0
    else:
        print(f"\n{failed_count} TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
