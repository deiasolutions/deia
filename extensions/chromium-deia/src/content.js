/**
 * DEIA Browser Extension - Content Script
 *
 * Runs in the context of web pages to detect and capture AI conversations.
 */

console.log('[DEIA] Content script loaded');

/**
 * Detect if current page is an AI tool
 */
function detectAITool() {
  const url = window.location.href;
  const hostname = window.location.hostname;

  const aiTools = {
    'claude.ai': 'Claude',
    'chat.openai.com': 'ChatGPT',
    'gemini.google.com': 'Gemini',
    'copilot.microsoft.com': 'Copilot',
    'bard.google.com': 'Bard'
  };

  for (const [domain, name] of Object.entries(aiTools)) {
    if (hostname.includes(domain)) {
      return { detected: true, tool: name, domain };
    }
  }

  return { detected: false };
}

/**
 * Initialize DEIA integration
 */
function initializeDEIA() {
  const detection = detectAITool();

  if (detection.detected) {
    console.log(`[DEIA] ${detection.tool} detected - monitoring enabled`);

    // TODO: Implement conversation monitoring
    // This will need to observe DOM changes to capture conversations
    // Each AI tool has a different structure, so we'll need tool-specific handlers

    // Add DEIA indicator to page
    addDeiaIndicator(detection.tool);
  }
}

/**
 * Add visual indicator that DEIA is active
 */
function addDeiaIndicator(toolName) {
  const indicator = document.createElement('div');
  indicator.id = 'deia-indicator';
  indicator.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #4CAF50;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-family: sans-serif;
    z-index: 10000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  `;
  indicator.textContent = `DEIA Active (${toolName})`;

  document.body.appendChild(indicator);

  // Fade out after 3 seconds
  setTimeout(() => {
    indicator.style.transition = 'opacity 0.5s';
    indicator.style.opacity = '0';
    setTimeout(() => indicator.remove(), 500);
  }, 3000);
}

/**
 * Listen for messages from background script
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[DEIA Content] Message received:', request);

  switch (request.action) {
    case 'captureConversation':
      captureCurrentConversation()
        .then(data => sendResponse({ success: true, data }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;

    default:
      sendResponse({ success: false, error: 'Unknown action' });
  }
});

/**
 * Capture current conversation from page
 */
async function captureCurrentConversation() {
  const detection = detectAITool();

  if (!detection.detected) {
    throw new Error('No AI tool detected on this page');
  }

  // TODO: Implement tool-specific conversation capture
  // For now, return a placeholder

  return {
    tool: detection.tool,
    url: window.location.href,
    timestamp: new Date().toISOString(),
    conversationText: 'TODO: Implement conversation capture',
    messages: []
  };
}

// Initialize when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeDEIA);
} else {
  initializeDEIA();
}
