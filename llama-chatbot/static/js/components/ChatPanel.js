/**
 * ChatPanel.js - Chat Panel Component
 * Handles message display, history loading, and message rendering
 */

class ChatPanel {
  constructor() {
    this.chatMessages = document.getElementById('chatMessages');
    this.chatInput = document.getElementById('chatInput');
    this.sendButton = document.getElementById('sendButton');
    this.typingIndicator = document.getElementById('typingIndicator');
    this.selectedBotInfo = document.getElementById('selectedBotInfo');
  }

  /**
   * Select a bot and load its chat history
   */
  async selectBot(botId) {
    store.setSelectedBotId(botId);
    this.selectedBotInfo.textContent = `Talking to: ${botId}`;
    this.chatInput.disabled = false;
    this.sendButton.disabled = false;
    this.chatMessages.innerHTML = '';

    // Load history BEFORE adding connection message
    await this.loadHistory();

    // Add connection message after history loads
    this.addMessage(
      'assistant',
      `Connected to ${botId}. Ready for commands.`
    );
  }

  /**
   * Load chat history from server
   */
  async loadHistory() {
    try {
      const selectedBotId = store.getSelectedBotId();
      const response = await fetch(
        `/api/chat/history?limit=100&bot_id=${selectedBotId}`
      );
      const data = await response.json();

      if (data.messages && data.messages.length > 0) {
        // Clear current messages and reload history
        const messageElements = this.chatMessages.querySelectorAll(
          '.message:not(.assistant)'
        );
        messageElements.forEach((el) => el.remove());

        // Load historical messages
        data.messages.forEach((msg) => {
          this.displayHistoryMessage(msg);
        });

        // Show "Load More" button if available
        if (data.has_more) {
          this.addLoadMoreButton(data.total);
        }
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  }

  /**
   * Display a message from history
   */
  displayHistoryMessage(msg) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + (msg.role === 'user' ? 'user' : 'assistant');

    // Add timestamp
    const timestamp = document.createElement('small');
    timestamp.style.color = '#999';
    timestamp.style.display = 'block';
    timestamp.style.fontSize = '11px';
    timestamp.textContent = new Date(msg.timestamp).toLocaleTimeString();

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = msg.content;

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timestamp);
    this.chatMessages.appendChild(messageDiv);
  }

  /**
   * Add a load more button to history
   */
  addLoadMoreButton(total) {
    const btn = document.createElement('button');
    btn.textContent = `Load More History (${total} total messages)`;
    btn.style.cssText =
      'background: #3a3a3a; color: #ccc; border: none; padding: 8px 16px; margin: 10px; cursor: pointer; border-radius: 4px;';

    btn.onclick = async () => {
      const selectedBotId = store.getSelectedBotId();
      const response = await fetch(
        `/api/chat/history?limit=200&bot_id=${selectedBotId}`
      );
      const data = await response.json();
      this.chatMessages.innerHTML = '';
      data.messages.forEach((msg) => this.displayHistoryMessage(msg));
      btn.remove();
    };

    this.chatMessages.insertBefore(btn, this.chatMessages.firstChild);
  }

  /**
   * Send message to bot
   */
  async sendMessage() {
    const selectedBotId = store.getSelectedBotId();
    if (!selectedBotId) {
      alert('Please select a bot first');
      return;
    }

    const message = this.chatInput.value.trim();
    if (!message) return;

    this.addMessage('user', message);
    this.chatInput.value = '';
    this.showTypingIndicator();

    try {
      // Route message to selected bot
      const response = await fetch(`/api/bot/${selectedBotId}/task`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: message }),
      });
      const result = await response.json();
      this.hideTypingIndicator();

      // Clear feedback on command routing
      if (result.success === true || !result.error) {
        // Success case
        this.addMessage('assistant', `✓ ${result.response || 'Command executed'}`);
      } else if (result.error) {
        // Error case
        this.addMessage('assistant', `✗ Error: ${result.error}`);
      } else {
        // Fallback
        this.addMessage(
          'assistant',
          `${selectedBotId}: ${result.response || 'No response'}`
        );
      }
    } catch (error) {
      this.hideTypingIndicator();
      this.addMessage('assistant', `✗ Network Error: ${error.message}`);
    }
  }

  /**
   * Add a message to the chat display
   */
  addMessage(role, content, persist = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + role;

    const selectedBotId = store.getSelectedBotId();
    if (role === 'assistant' && selectedBotId) {
      const botIdDiv = document.createElement('div');
      botIdDiv.className = 'message-bot-id';
      botIdDiv.textContent = selectedBotId;
      messageDiv.appendChild(botIdDiv);
    }

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    // Add timestamp
    const timestamp = document.createElement('small');
    timestamp.style.color = '#999';
    timestamp.style.display = 'block';
    timestamp.style.fontSize = '11px';
    timestamp.textContent = new Date().toLocaleTimeString();

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timestamp);
    this.chatMessages.appendChild(messageDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

    // Save to history only if: persist=true AND selectedBotId is set
    if (persist && selectedBotId) {
      this.saveMessageToHistory(role, content);
    }
  }

  /**
   * Save message to server history
   */
  async saveMessageToHistory(role, content) {
    try {
      const selectedBotId = store.getSelectedBotId();
      await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          role: role,
          content: content,
          bot_id: selectedBotId,
        }),
      });
    } catch (error) {
      console.warn('Failed to save message to history:', error);
    }
  }

  /**
   * Show typing indicator
   */
  showTypingIndicator() {
    this.typingIndicator.classList.add('show');
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  /**
   * Hide typing indicator
   */
  hideTypingIndicator() {
    this.typingIndicator.classList.remove('show');
  }

  /**
   * Reset chat panel
   */
  reset() {
    this.chatMessages.innerHTML = '';
    this.chatInput.value = '';
    this.chatInput.disabled = true;
    this.sendButton.disabled = true;
    this.selectedBotInfo.textContent = 'Select a bot to start';
    store.setSelectedBotId(null);
  }
}
