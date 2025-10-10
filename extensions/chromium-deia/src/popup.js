/**
 * DEIA Browser Extension - Popup Script
 *
 * Handles popup UI interactions.
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Get references to UI elements
  const statusIndicator = document.getElementById('statusIndicator');
  const statusText = document.getElementById('statusText');
  const pageInfo = document.getElementById('pageInfo');
  const logButton = document.getElementById('logButton');
  const optionsButton = document.getElementById('optionsButton');
  const autoLogCheckbox = document.getElementById('autoLogCheckbox');

  // Load configuration
  const config = await getConfig();
  autoLogCheckbox.checked = config.autoLog || false;

  // Get current tab info
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Check if we're on an AI tool page
  const aiToolPatterns = [
    { pattern: 'claude.ai', name: 'Claude' },
    { pattern: 'chat.openai.com', name: 'ChatGPT' },
    { pattern: 'gemini.google.com', name: 'Gemini' },
    { pattern: 'copilot.microsoft.com', name: 'Copilot' }
  ];

  const detectedTool = aiToolPatterns.find(tool =>
    tab.url && tab.url.includes(tool.pattern)
  );

  if (detectedTool) {
    statusIndicator.classList.remove('inactive');
    statusText.textContent = `Active on ${detectedTool.name}`;
    pageInfo.textContent = `Monitoring conversations on this page`;
  } else {
    statusIndicator.classList.add('inactive');
    statusText.textContent = 'No AI tool detected';
    pageInfo.textContent = 'Visit Claude, ChatGPT, or other AI tools';
  }

  // Log button handler
  logButton.addEventListener('click', async () => {
    logButton.textContent = 'Logging...';
    logButton.disabled = true;

    try {
      // Send message to content script to capture conversation
      const response = await chrome.tabs.sendMessage(tab.id, {
        action: 'captureConversation'
      });

      if (response.success) {
        // Send to background for logging
        await chrome.runtime.sendMessage({
          action: 'logConversation',
          data: response.data
        });

        logButton.textContent = '✓ Logged!';
        setTimeout(() => {
          logButton.textContent = 'Log Current Session';
          logButton.disabled = false;
        }, 2000);
      } else {
        throw new Error(response.error);
      }
    } catch (error) {
      console.error('[DEIA Popup] Error logging:', error);
      logButton.textContent = '✗ Error';
      setTimeout(() => {
        logButton.textContent = 'Log Current Session';
        logButton.disabled = false;
      }, 2000);
    }
  });

  // Options button handler
  optionsButton.addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });

  // Auto-log checkbox handler
  autoLogCheckbox.addEventListener('change', async () => {
    await chrome.runtime.sendMessage({
      action: 'setConfig',
      config: { autoLog: autoLogCheckbox.checked }
    });
  });
});

/**
 * Get configuration from storage
 */
async function getConfig() {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ action: 'getConfig' }, (response) => {
      resolve(response.success ? response.config : {});
    });
  });
}
