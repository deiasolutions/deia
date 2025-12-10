/**
 * app.js - Main Application Entry Point
 * Initializes all components and wires up event listeners
 */

// Initialize components
const botList = new BotList(
  (botId) => {
    // onBotSelect callback
    chatPanel.selectBot(botId);
    botList.refresh();
  },
  (botId) => {
    // onBotStop callback
    botList.stopBot(botId);
  }
);

const chatPanel = new ChatPanel();
const statusBoard = new StatusBoard();
const botLauncher = new BotLauncher(
  (botId) => {
    // onLaunchSuccess callback
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `✓ Bot ${botId} launched successfully`;
    chatMessages.appendChild(messageDiv);

    botList.refresh();
  },
  (error) => {
    // onLaunchError callback
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `✗ ${error}`;
    chatMessages.appendChild(messageDiv);
  }
);

// WebSocket Management
function initWebSocket() {
  try {
    const ws = new WebSocket(`ws://${window.location.host}/ws`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      chatPanel.addMessage(
        'assistant',
        '✓ Real-time messaging connected',
        false
      );
    };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      chatPanel.addMessage('assistant', msg.response || msg.content);
      chatPanel.hideTypingIndicator();
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      chatPanel.addMessage(
        'assistant',
        'Connection error - using fallback',
        false
      );
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    store.setWebSocket(ws);
  } catch (error) {
    console.error('Failed to connect WebSocket:', error);
  }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  const launchBtn = document.getElementById('launchBtn');
  const sendButton = document.getElementById('sendButton');
  const chatInput = document.getElementById('chatInput');

  // Launch button
  launchBtn.addEventListener('click', () => {
    botLauncher.show();
  });

  // Send button
  sendButton.addEventListener('click', () => {
    chatPanel.sendMessage();
  });

  // Chat input - send on Enter
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      chatPanel.sendMessage();
    }
  });

  // Initialize application state
  chatInput.disabled = true;
  sendButton.disabled = true;
});

// Page Initialization
window.addEventListener('load', () => {
  // Initial setup
  botList.refresh();
  initWebSocket();
  statusBoard.startUpdates();

  // Periodic bot list refresh
  const botListInterval = setInterval(() => {
    botList.refresh();
  }, 2000);

  store.setBotListInterval(botListInterval);
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  const ws = store.getWebSocket();
  if (ws) {
    ws.close();
  }

  const botListInterval = store.getBotListInterval();
  if (botListInterval) {
    clearInterval(botListInterval);
  }

  statusBoard.stopUpdates();
});
