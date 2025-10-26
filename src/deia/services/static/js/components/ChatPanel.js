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
      const botType = store.getSelectedBotType();
      const typeLabel = botType ? ` (${botType})` : '';
      this.selectedBotInfo.textContent = `Talking to: ${botId}${typeLabel}`;
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
        Toast.info('📤 Sending message...');
        ws.send(JSON.stringify({
          type: 'query',
          bot_id: selectedBotId,
          query: message
        }));
      } else {
        // Fallback to REST API
        Toast.info('📤 Sending via API...');
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
          Toast.success('✅ Message sent!');

          // Handle service-specific responses
          const botType = store.getSelectedBotType();
          let responseText = result.response || 'Command executed';

          // For CLI services, show modified files
          if ((botType === 'claude-code' || botType === 'codex') && result.files_modified) {
            if (result.files_modified.length > 0) {
              responseText += `\n\n📝 Modified files:\n${result.files_modified.join('\n')}`;
            }
          }

          this.addMessage('assistant', responseText, false);
        } else {
          Toast.error(`❌ ${result.error || 'Unknown error'}`);
          this.addMessage('assistant', `❌ ${result.error || 'Unknown error'}`, true);
        }
      }
    } catch (error) {
      this.hideTypingIndicator();
      Toast.error(`❌ Error: ${error.message}`);
      this.addMessage('assistant', `❌ Error: ${error.message}`, true);
    }
  }

  addMessage(sender, text, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    if (isError) messageDiv.classList.add('error');

    // Add bot type badge for assistant messages
    if (sender === 'assistant' && !isError) {
      const botType = store.getSelectedBotType();
      if (botType) {
        const badge = document.createElement('span');
        badge.className = 'bot-type-badge';
        badge.textContent = botType;
        badge.style.cssText = `
          display: inline-block;
          background: #007bff;
          color: white;
          padding: 4px 10px;
          border-radius: 3px;
          font-size: 0.85em;
          margin-right: 8px;
          font-weight: bold;
          margin-bottom: 6px;
        `;
        messageDiv.appendChild(badge);

        // Add line break after badge
        const br = document.createElement('br');
        messageDiv.appendChild(br);
      }
    }

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
