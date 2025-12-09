# TASK: BOT-003 - Service Integration & Response Handling

**Priority:** P1 BLOCKING
**Time Estimate:** 40 minutes
**Start:** When BOT-001 completes and signals
**Blocker:** BOT-001 must finish first
**Depends On:** ServiceFactory from BOT-001

---

## OBJECTIVE

Integrate services into chat panel and handle responses properly. Make API services use FileOperationService for file operations.

---

## PART 1: Update ChatPanel to Handle Service Types

**File:** `src/deia/services/static/js/components/ChatPanel.js`

**Location:** Find `async sendMessage()` method (around line 81)

**Update to show service-specific feedback:**

```javascript
async sendMessage() {
    const selectedBotId = store.getSelectedBotId();
    if (!selectedBotId) {
      Toast.warning('⚠️ Please select a bot first');
      return;
    }

    const message = this.chatInput.value.trim();
    if (!message) return;

    this.addMessage('user', message, false);
    this.chatInput.value = '';
    this.showTypingIndicator();

    try {
      const ws = store.getWebSocket();

      if (ws && ws.readyState === WebSocket.OPEN) {
        // Send via WebSocket
        Toast.info('📤 Sending via WebSocket...');
        ws.send(JSON.stringify({
          type: 'command',
          bot_id: selectedBotId,
          command: message
        }));
      } else {
        // Send via REST API with service routing
        Toast.info('📤 Sending message...');
        const response = await fetch(`/api/bot/${selectedBotId}/task`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ command: message })
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();
        this.hideTypingIndicator();

        if (result.success) {
          // Show bot_type in response
          const botTypeInfo = result.bot_type ? ` (${result.bot_type})` : '';
          Toast.success(`✅ Response received${botTypeInfo}`);

          // Display response
          let responseText = result.response || 'Command executed';

          // For CLI services, show modified files
          if (result.files_modified && result.files_modified.length > 0) {
            responseText += `\n\n📝 Modified files:\n${result.files_modified.join('\n')}`;
          }

          this.addMessage('assistant', responseText, false);
        } else {
          Toast.error(`❌ ${result.error || 'Unknown error'}`);
          this.addMessage('assistant', `❌ Error: ${result.error || 'Unknown error'}`, true);
        }
      }
    } catch (error) {
      this.hideTypingIndicator();
      Toast.error(`❌ Error: ${error.message}`);
      this.addMessage('assistant', `❌ Error: ${error.message}`, true);
    }
  }
```

---

## PART 2: Add Service Integration Methods to API Services

**Files to Update:**
- `src/deia/services/llm_service.py` - Update `AnthropicService`, `OpenAIService`, `OllamaService`

**Add these imports at top:**
```python
from deia.services.file_operation_service import FileOperationService
```

**Add to each API service class (AnthropicService, OpenAIService, OllamaService):**

```python
def process_task_file(self, task_file_path: str) -> dict:
    """
    Process a task file and return result with embedded code.

    For lightweight task file processing (markdown with instructions + embedded code).

    Args:
        task_file_path: Path to task markdown file

    Returns:
        dict: {
            'success': True/False,
            'output': 'Response from LLM',
            'code_blocks': [...],
            'files_to_extract': {...}
        }
    """
    try:
        file_service = FileOperationService()

        # Read and parse task file
        task = file_service.read_task_file(task_file_path)

        # Chat with LLM about the task
        response = self.chat(task.instructions)

        # Extract code blocks from response
        code_blocks = file_service.extract_code_blocks(response)

        # Write result file
        result_path = task_file_path.replace('task-', 'result-')
        file_service.write_result_file(
            result_path,
            title=f"Result: {task.title}",
            summary=response,
            code_blocks=code_blocks
        )

        return {
            'success': True,
            'output': response,
            'code_blocks': code_blocks,
            'result_file': result_path
        }

    except Exception as e:
        logger.error(f"Error processing task file: {e}")
        return {
            'success': False,
            'error': str(e),
            'output': ''
        }
```

---

## PART 3: Create Integration Tests

**File:** `tests/unit/test_service_factory.py`

```python
"""Tests for ServiceFactory"""

import pytest
from pathlib import Path
from deia.services.service_factory import ServiceFactory, BotType


def test_service_factory_supported_types():
    """Test supported types are listed"""
    types = ServiceFactory.get_supported_types()
    assert 'claude' in types
    assert 'chatgpt' in types
    assert 'claude-code' in types
    assert 'codex' in types
    assert 'llama' in types


def test_service_factory_create_anthropic():
    """Test creating AnthropicService"""
    import os
    if not os.getenv('ANTHROPIC_API_KEY'):
        pytest.skip("ANTHROPIC_API_KEY not set")

    service = ServiceFactory.get_service('claude', 'TEST-BOT')
    assert service is not None
    assert hasattr(service, 'chat')


def test_service_factory_create_openai():
    """Test creating OpenAIService"""
    import os
    if not os.getenv('OPENAI_API_KEY'):
        pytest.skip("OPENAI_API_KEY not set")

    service = ServiceFactory.get_service('chatgpt', 'TEST-BOT')
    assert service is not None
    assert hasattr(service, 'chat')


def test_service_factory_create_llama():
    """Test creating OllamaService"""
    service = ServiceFactory.get_service('llama', 'TEST-BOT')
    assert service is not None
    assert hasattr(service, 'chat')


def test_service_factory_create_claude_code():
    """Test creating ClaudeCodeCLIAdapter"""
    service = ServiceFactory.get_service('claude-code', 'CLAUDE-CODE-BOT', Path.cwd())
    assert service is not None
    assert hasattr(service, 'start_session')


def test_service_factory_create_codex():
    """Test creating CodexCLIAdapter"""
    service = ServiceFactory.get_service('codex', 'CODEX-BOT', Path.cwd())
    assert service is not None
    assert hasattr(service, 'start_session')


def test_service_factory_is_cli_service():
    """Test CLI service detection"""
    assert ServiceFactory.is_cli_service('claude-code') == True
    assert ServiceFactory.is_cli_service('codex') == True
    assert ServiceFactory.is_cli_service('claude') == False


def test_service_factory_is_api_service():
    """Test API service detection"""
    assert ServiceFactory.is_api_service('claude') == True
    assert ServiceFactory.is_api_service('chatgpt') == True
    assert ServiceFactory.is_api_service('llama') == True
    assert ServiceFactory.is_api_service('claude-code') == False


def test_service_factory_invalid_type():
    """Test invalid bot type raises error"""
    with pytest.raises(ValueError):
        ServiceFactory.get_service('invalid-type', 'BOT')
```

---

## PART 4: Update Status Board to Show Bot Type

**File:** `src/deia/services/static/js/components/StatusBoard.js` (or update BotList.js)

**When displaying bot info, show bot_type:**

```javascript
// In bot list rendering, add bot type to display
const botTypeLabel = {
  'claude': '🔵 Claude',
  'chatgpt': '🟢 ChatGPT',
  'claude-code': '💻 Claude Code',
  'codex': '⚙️ Codex',
  'llama': '🦙 LLaMA'
};

// Display in bot item
botItem.innerHTML = `
  <div class="bot-id">
    <span class="bot-status status-${botData.status}"></span>${botId}
  </div>
  <div class="bot-type">${botTypeLabel[botData.bot_type] || botData.bot_type}</div>
  <div class="bot-status-text">${botData.status}</div>
  ...
`;
```

---

## TESTING

**Run these tests:**

```bash
# Test ServiceFactory
pytest tests/unit/test_service_factory.py -v

# Test updated task endpoint
pytest tests/unit/test_chat_api_endpoints.py::TestBotTaskEndpoint -v

# Integration test
pytest tests/integration/test_chat_complete.py -v
```

---

## DONE CHECKLIST

- [ ] Update ChatPanel.js sendMessage() method
- [ ] Add `process_task_file()` to AnthropicService
- [ ] Add `process_task_file()` to OpenAIService
- [ ] Add `process_task_file()` to OllamaService
- [ ] Create `tests/unit/test_service_factory.py` with all tests
- [ ] Tests passing
- [ ] Update bot list/status board to show bot_type (optional but nice)
- [ ] Create completion report

---

## COMPLETION

When finished, create: `.deia/hive/responses/deiasolutions/bot-003-service-integration-done.md`

Write:
- ChatPanel updated for service routing
- API services integrated with FileOperationService
- Tests passing
- All services callable from chat interface
- Ready for end-to-end testing

Signal when complete.
