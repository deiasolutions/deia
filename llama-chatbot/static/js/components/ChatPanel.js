/**
 * ChatPanel.js - Chat Panel Component
 */

class ChatPanel {
  constructor() {
    this.chatMessages = document.getElementById('chatMessages');
    this.chatInput = document.getElementById('chatInput');
    this.sendButton = document.getElementById('sendButton');
    this.typingIndicator = document.getElementById('typingIndicator');
    this.selectedBotInfo = document.getElementById('selectedBotInfo');
  }

  async selectBot(botId) {
    store.setSelectedBotId(botId);

    if (this.selectedBotInfo) {
      this.selectedBotInfo.textContent = `Talking to: ${botId}`;
    }

    if (this.chatInput) {
      this.chatInput.disabled = false;
      this.chatInput.focus();
    }

    if (this.sendButton) {
      this.sendButton.disabled = false;
    }

    if (this.chatMessages) {
      this.chatMessages.innerHTML = '';
    }

    await this.loadHistory();

    this.addMessage(
      'system',
      `✓ Connected to ${botId}. Ready for commands.`,
      false
    );
  }

  async loadHistory() {
    try {
      const selectedBotId = store.getSelectedBotId();
      if (!selectedBotId) return;

      const response = await fetch(
        `/api/chat/history?limit=100&bot_id=${selectedBotId}`
      );
      const data = await response.json();

      if (data.messages && data.messages.length > 0) {
        data.messages.forEach((msg) => {
          this.displayHistoryMessage(msg);
        });
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  }

  displayHistoryMessage(msg) {
    const messageDiv = document.createElement('div');
    const role = msg.role === 'user' ? 'user' : 'assistant';
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = msg.content;

    const timestamp = document.createElement('small');
    timestamp.style.cssText = 'color: #999; display: block; font-size: 11px; margin-top: 4px;';
    timestamp.textContent = new Date(msg.timestamp).toLocaleTimeString();

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timestamp);
    this.chatMessages.appendChild(messageDiv);
  }

  async sendMessage() {
    const selectedBotId = store.getSelectedBotId();
    if (!selectedBotId) {
      alert('Please select a bot first');
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
        ws.send(JSON.stringify({
          type: 'command',
          bot_id: selectedBotId,
          command: message
        }));
      } else {
        // Fallback to REST API
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
          this.addMessage('assistant', result.response || 'Command executed', false);
        } else {
          this.addMessage('assistant', `❌ ${result.error || 'Unknown error'}`, true);
        }
      }
    } catch (error) {
      this.hideTypingIndicator();
      this.addMessage('assistant', `❌ Error: ${error.message}`, true);
    }
  }

  addMessage(sender, text, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    if (isError) messageDiv.classList.add('error');

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    messageDiv.appendChild(contentDiv);
    this.chatMessages.appendChild(messageDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  showTypingIndicator() {
    if (this.typingIndicator) {
      this.typingIndicator.style.display = 'block';
      this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
  }

  hideTypingIndicator() {
    if (this.typingIndicator) {
      this.typingIndicator.style.display = 'none';
    }
  }
}
