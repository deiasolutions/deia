/**
 * BotLauncher.js - Bot Launch Modal Component
 * Handles the launch bot dialog, validation, and API calls
 */

class BotLauncher {
  constructor(onLaunchSuccess, onLaunchError) {
    this.onLaunchSuccess = onLaunchSuccess;
    this.onLaunchError = onLaunchError;

    // Available bot types
    this.botTypes = [
      { id: 'claude', label: '🔵 Claude (Anthropic)', icon: '🔵' },
      { id: 'chatgpt', label: '🟢 ChatGPT (OpenAI)', icon: '🟢' },
      { id: 'claude-code', label: '💻 Claude Code (CLI)', icon: '💻' },
      { id: 'codex', label: '⚙️ Codex (CLI)', icon: '⚙️' },
      { id: 'llama', label: '🦙 LLaMA (Ollama)', icon: '🦙' }
    ];

    this.selectedBotType = 'claude'; // Default
  }

  /**
   * Show professional modal dialog for bot launch
   */
  async show() {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.style.cssText =
      'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 10000;';

    // Create dialog box
    const dialog = document.createElement('div');
    dialog.style.cssText =
      'background: #222; border: 1px solid #444; border-radius: 12px; padding: 24px; max-width: 450px; width: 90%; box-shadow: 0 10px 40px rgba(0,0,0,0.5);';

    // Build bot type options
    const typeOptions = this.botTypes.map(type =>
      `<option value="${type.id}">${type.label}</option>`
    ).join('');

    dialog.innerHTML = `
      <h2 style="margin: 0 0 16px 0; color: #e0e0e0; font-size: 20px;">Launch Bot</h2>
      <p style="margin: 0 0 12px 0; color: #999; font-size: 14px;">Select bot type and enter a bot ID</p>

      <label style="display: block; margin-bottom: 8px; color: #ccc; font-size: 13px; font-weight: 500;">Bot Type</label>
      <select
        id="botTypeSelect"
        style="width: 100%; padding: 12px; margin: 0 0 16px 0; background: #2a2a2a; border: 1px solid #333; border-radius: 6px; color: #e0e0e0; box-sizing: border-box; font-size: 16px; cursor: pointer;">
        ${typeOptions}
      </select>

      <label style="display: block; margin-bottom: 8px; color: #ccc; font-size: 13px; font-weight: 500;">Bot ID</label>
      <input
        type="text"
        id="botIdInput"
        placeholder="e.g., BOT-001"
        style="width: 100%; padding: 12px; margin: 0 0 8px 0; background: #2a2a2a; border: 1px solid #333; border-radius: 6px; color: #e0e0e0; box-sizing: border-box; font-size: 16px;">
      <div id="validationMsg" style="margin: 8px 0; font-size: 12px; color: #999; height: 20px;"></div>

      <div style="display: flex; gap: 10px; margin-top: 20px;">
        <button
          id="launchOkBtn"
          style="flex: 1; padding: 12px; background: linear-gradient(135deg, #4a7ff5 0%, #3d5cb7 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
          Launch
        </button>
        <button
          id="launchCancelBtn"
          style="flex: 1; padding: 12px; background: #333; color: #ccc; border: 1px solid #444; border-radius: 6px; cursor: pointer;">
          Cancel
        </button>
      </div>
    `;

    modal.appendChild(dialog);
    document.body.appendChild(modal);

    // Get elements
    const typeSelect = document.getElementById('botTypeSelect');
    const input = document.getElementById('botIdInput');
    const validationMsg = document.getElementById('validationMsg');
    const okBtn = document.getElementById('launchOkBtn');
    const cancelBtn = document.getElementById('launchCancelBtn');

    // Bot type selection
    typeSelect.addEventListener('change', (e) => {
      this.selectedBotType = e.target.value;
      this.validateInput(input, validationMsg, okBtn);
    });

    // Focus input
    input.focus();

    // Real-time validation
    input.addEventListener('input', () => {
      this.validateInput(input, validationMsg, okBtn);
    });

    // Launch button
    okBtn.addEventListener('click', async () => {
      const botId = input.value.trim();
      if (!botId) return;

      modal.remove();
      await this.performLaunch(botId, this.selectedBotType);
    });

    // Cancel button
    cancelBtn.addEventListener('click', () => {
      modal.remove();
    });

    // Close on Escape key
    const closeOnEscape = (e) => {
      if (e.key === 'Escape') {
        modal.remove();
        document.removeEventListener('keydown', closeOnEscape);
      }
    };
    document.addEventListener('keydown', closeOnEscape);
  }

  /**
   * Validate bot ID input
   */
  validateInput(input, validationMsg, okBtn) {
    const botId = input.value.trim().toUpperCase();

    if (!botId) {
      validationMsg.textContent = '';
      okBtn.disabled = true;
      return;
    }

    if (botId.length < 3) {
      validationMsg.innerHTML = '<span style="color: #f44336;">⚠ Too short</span>';
      okBtn.disabled = true;
    } else if (store.getActiveBots()[botId]) {
      validationMsg.innerHTML = '<span style="color: #ff9800;">⚠ Already running</span>';
      okBtn.disabled = false;
    } else {
      validationMsg.innerHTML = '<span style="color: #4caf50;">✓ Valid format</span>';
      okBtn.disabled = false;
    }
  }

  /**
   * Perform the actual bot launch API call
   */
  async performLaunch(botId, botType) {
    try {
      // Show loading toast
      const loadingToast = Toast.loading(`🚀 Launching ${botId} (${botType})...`);

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5s timeout

      const response = await fetch('/api/bot/launch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bot_id: botId,
          bot_type: botType
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      const result = await response.json();

      // Remove loading toast if it exists
      if (loadingToast) {
        try {
          Toast.removeToast(loadingToast);
        } catch (e) {
          console.error('Error removing toast:', e);
        }
      }

      if (result.success) {
        Toast.success(`✅ ${botId} (${botType}) launched successfully!`);
        this.onLaunchSuccess(botId);
      } else {
        Toast.error(`❌ Failed to launch: ${result.error}`);
        this.onLaunchError(`Failed to launch: ${result.error}`);
      }
    } catch (error) {
      Toast.error(`❌ ${error.name === 'AbortError' ? 'Launch timeout' : error.message}`);
      this.onLaunchError(`Error: ${error.message}`);
    }
  }
}
