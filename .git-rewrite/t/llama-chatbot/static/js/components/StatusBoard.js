/**
 * StatusBoard.js - Status Dashboard Component
 * Handles real-time bot status display and updates
 */

class StatusBoard {
  constructor() {
    this.statusList = document.getElementById('statusList');
  }

  /**
   * Start polling for status updates
   */
  startUpdates() {
    if (store.getStatusUpdateInterval()) return;

    const interval = setInterval(async () => {
      try {
        const response = await fetch('/api/bots');
        const data = await response.json();

        this.render(data.bots || {});
      } catch (error) {
        console.error('Status update error:', error);
      }
    }, 3000); // Update every 3 seconds

    store.setStatusUpdateInterval(interval);
  }

  /**
   * Stop polling for status updates
   */
  stopUpdates() {
    const interval = store.getStatusUpdateInterval();
    if (interval) {
      clearInterval(interval);
      store.setStatusUpdateInterval(null);
    }
  }

  /**
   * Render status items to DOM
   */
  render(bots) {
    this.statusList.innerHTML = '';

    for (const [botId, botData] of Object.entries(bots)) {
      const statusDiv = document.createElement('div');
      statusDiv.className = `status-item ${botData.status}`;

      statusDiv.innerHTML = `
        <div class="status-label">${botId}</div>
        <div class="status-value">Status: ${botData.status}</div>
        <div class="status-value">PID: ${botData.pid || 'N/A'}</div>
        <div class="status-value">Port: ${botData.port || 'N/A'}</div>
      `;

      this.statusList.appendChild(statusDiv);
    }
  }

  /**
   * Update status for a single bot
   */
  async updateBotStatus(botId) {
    try {
      const response = await fetch(`/api/bot/${botId}/status`);
      const data = await response.json();

      const activeBots = store.getActiveBots();
      activeBots[botId] = data;
      store.setActiveBots(activeBots);

      this.render(activeBots);
    } catch (error) {
      console.error(`Failed to update status for ${botId}:`, error);
    }
  }

  /**
   * Update all bot statuses
   */
  async updateAllStatuses() {
    try {
      const activeBots = store.getActiveBots();

      for (const botId of Object.keys(activeBots)) {
        const response = await fetch(`/api/bot/${botId}/status`);
        const data = await response.json();
        activeBots[botId] = data;
      }

      store.setActiveBots(activeBots);
      this.render(activeBots);
    } catch (error) {
      console.error('Failed to update statuses:', error);
    }
  }

  /**
   * Clear status display
   */
  clear() {
    this.statusList.innerHTML = '';
  }
}
