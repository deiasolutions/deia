/**
 * app.js - Main Application Entry Point
 */

const botList = new BotList(
  (botId) => {
    chatPanel.selectBot(botId);
    botList.refresh();
  },
  (botId) => {
    botList.stopBot(botId);
  }
);

const chatPanel = new ChatPanel();
const statusBoard = new StatusBoard();
const botLauncher = new BotLauncher(
  (botId) => {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.innerHTML = `✓ Bot ${botId} launched successfully`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    botList.refresh();
  },
  (error) => {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message error';
    messageDiv.innerHTML = `✗ ${error}`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
);

// WebSocket Management
let ws = null;

function initWebSocket() {
  try {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      const statusEl = document.getElementById('connectionStatus');
      if (statusEl) {
        statusEl.textContent = '🟢 Connected';
        statusEl.style.color = '#4CAF50';
      }
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        handleWebSocketMessage(msg);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      const statusEl = document.getElementById('connectionStatus');
      if (statusEl) {
        statusEl.textContent = '🔴 Disconnected';
        statusEl.style.color = '#f44336';
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      const statusEl = document.getElementById('connectionStatus');
      if (statusEl) {
        statusEl.textContent = '🔴 Offline';
        statusEl.style.color = '#f44336';
      }
    };

    store.setWebSocket(ws);
  } catch (error) {
    console.error('Failed to connect WebSocket:', error);
  }
}

function handleWebSocketMessage(msg) {
  const { type, bot_id, content, success, error } = msg;

  if (success === false || error) {
    chatPanel.addMessage(
      'assistant',
      `❌ Error: ${error || 'Command failed'}`,
      true
    );
    chatPanel.hideTypingIndicator();
    return;
  }

  if (type === 'response') {
    chatPanel.addMessage('assistant', content, false);
    chatPanel.hideTypingIndicator();
  } else if (type === 'typing') {
    chatPanel.showTypingIndicator();
  }
}

// Status Polling
let statusPollInterval = null;

function startStatusPolling() {
  statusPollInterval = setInterval(async () => {
    try {
      const response = await fetch('/api/bots/status');
      const bots = await response.json();
      statusBoard.updateStatus(bots);
    } catch (e) {
      console.error('Status poll error:', e);
    }
  }, 5000);
}

function stopStatusPolling() {
  if (statusPollInterval) {
    clearInterval(statusPollInterval);
  }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  const launchBtn = document.getElementById('launchBtn');
  const sendButton = document.getElementById('sendButton');
  const chatInput = document.getElementById('chatInput');

  if (launchBtn) {
    launchBtn.addEventListener('click', () => {
      botLauncher.show();
    });
  }

  if (sendButton) {
    sendButton.addEventListener('click', () => {
      chatPanel.sendMessage();
    });
  }

  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatPanel.sendMessage();
      }
    });
  }

  // Initialize WebSocket and status polling
  initWebSocket();
  startStatusPolling();

  // Load bot list
  botList.refresh();
  statusBoard.init();
});

// Cleanup on unload
window.addEventListener('beforeunload', () => {
  stopStatusPolling();
  if (ws) ws.close();
});
