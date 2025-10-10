/**
 * DEIA Browser Extension - Background Service Worker
 *
 * Handles background tasks, message passing, and extension lifecycle.
 */

console.log('[DEIA] Background service worker initialized');

// Listen for extension installation or update
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('[DEIA] Extension installed');
    // Set default configuration
    chrome.storage.local.set({
      autoLog: true,
      projectName: 'browser-session',
      initialized: true
    });
  } else if (details.reason === 'update') {
    console.log('[DEIA] Extension updated to version', chrome.runtime.getManifest().version);
  }
});

// Listen for messages from content scripts or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[DEIA] Message received:', request);

  switch (request.action) {
    case 'logConversation':
      handleLogConversation(request.data)
        .then(result => sendResponse({ success: true, result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true; // Keep channel open for async response

    case 'getConfig':
      chrome.storage.local.get(['autoLog', 'projectName'], (config) => {
        sendResponse({ success: true, config });
      });
      return true;

    case 'setConfig':
      chrome.storage.local.set(request.config, () => {
        sendResponse({ success: true });
      });
      return true;

    default:
      sendResponse({ success: false, error: 'Unknown action' });
  }
});

/**
 * Handle conversation logging request
 */
async function handleLogConversation(data) {
  console.log('[DEIA] Logging conversation:', data);

  // TODO: Implement actual logging logic
  // This will need to communicate with the DEIA core library
  // Possibly through a local server or file system API

  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    context: data.context || 'Browser session',
    transcript: data.transcript || '',
    url: data.url || '',
    ...data
  };

  // For now, store in chrome.storage as a placeholder
  const storageKey = `session_${timestamp}`;
  await chrome.storage.local.set({ [storageKey]: logEntry });

  return { logged: true, timestamp };
}

/**
 * Listen for tab updates to detect AI tool pages
 */
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete') {
    // Detect if this is an AI tool page
    const aiToolPatterns = [
      'claude.ai',
      'chat.openai.com',
      'gemini.google.com',
      'copilot.microsoft.com'
    ];

    const isAITool = aiToolPatterns.some(pattern =>
      tab.url && tab.url.includes(pattern)
    );

    if (isAITool) {
      console.log('[DEIA] AI tool page detected:', tab.url);
      // Could inject additional functionality here
    }
  }
});
