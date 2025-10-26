/**
 * Store.js - Central State Management
 * Manages all application state in a single location
 */

class Store {
  constructor() {
    this.state = {
      // Bot state
      activeBots: {},
      selectedBotId: null,

      // Chat state
      messages: [],
      typingIndicatorVisible: false,

      // Connection state
      ws: null,
      statusUpdateInterval: null,
      botListInterval: null,
    };
  }

  // Bot State Methods
  setActiveBots(bots) {
    this.state.activeBots = bots;
  }

  getActiveBots() {
    return this.state.activeBots;
  }

  setSelectedBotId(botId) {
    this.state.selectedBotId = botId;
  }

  getSelectedBotId() {
    return this.state.selectedBotId;
  }

  // Chat State Methods
  addMessage(role, content, timestamp) {
    this.state.messages.push({
      role,
      content,
      timestamp: timestamp || new Date().toISOString(),
    });
  }

  clearMessages() {
    this.state.messages = [];
  }

  getMessages() {
    return this.state.messages;
  }

  // Typing Indicator
  setTypingIndicatorVisible(visible) {
    this.state.typingIndicatorVisible = visible;
  }

  isTypingIndicatorVisible() {
    return this.state.typingIndicatorVisible;
  }

  // Connection State
  setWebSocket(ws) {
    this.state.ws = ws;
  }

  getWebSocket() {
    return this.state.ws;
  }

  setStatusUpdateInterval(interval) {
    this.state.statusUpdateInterval = interval;
  }

  getStatusUpdateInterval() {
    return this.state.statusUpdateInterval;
  }

  setBotListInterval(interval) {
    this.state.botListInterval = interval;
  }

  getBotListInterval() {
    return this.state.botListInterval;
  }

  // Debug method
  getState() {
    return JSON.parse(JSON.stringify(this.state));
  }
}

// Export singleton instance
const store = new Store();
