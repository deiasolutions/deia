/**
 * BotList.js - Bot List Component
 * Handles bot list rendering, selection, and control
 */

class BotList {
  constructor(onBotSelect, onBotStop) {
    this.botListElement = document.getElementById('botList');
    this.onBotSelect = onBotSelect;
    this.onBotStop = onBotStop;
  }

  /**
   * Refresh bot list from server
   */
  async refresh() {
    try {
      const response = await fetch('/api/bots');
      const data = await response.json();
      const activeBots = data.bots || {};

      store.setActiveBots(activeBots);
      this.render(activeBots);
    } catch (error) {
      console.error('Failed to refresh bot list:', error);
    }
  }

  /**
   * Render bot list to DOM
   */
  render(activeBots) {
    this.botListElement.innerHTML = '';

    if (Object.keys(activeBots).length === 0) {
      this.botListElement.innerHTML =
        '<div class="bot-item"><div class="bot-id">No bots running</div></div>';
      return;
    }

    const selectedBotId = store.getSelectedBotId();

    for (const [botId, botData] of Object.entries(activeBots)) {
      const botItem = document.createElement('div');
      botItem.className = 'bot-item' + (selectedBotId === botId ? ' active' : '');

      botItem.innerHTML = `
        <div class="bot-id">
          <span class="bot-status status-${botData.status}"></span>${botId}
        </div>
        <div class="bot-status-text">${botData.status}</div>
        <div class="bot-actions">
          <button class="bot-action-btn" data-action="select" data-bot-id="${botId}">Select</button>
          <button class="bot-action-btn" data-action="stop" data-bot-id="${botId}">Stop</button>
        </div>
      `;

      // Add event listeners to action buttons
      botItem.querySelectorAll('[data-action]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const action = btn.getAttribute('data-action');
          const id = btn.getAttribute('data-bot-id');

          if (action === 'select') {
            this.onBotSelect(id);
          } else if (action === 'stop') {
            this.onBotStop(id);
          }
        });
      });

      this.botListElement.appendChild(botItem);
    }
  }

  /**
   * Stop bot with confirmation
   */
  async stopBot(botId) {
    if (!confirm(`Stop ${botId}?`)) return;

    try {
      const response = await fetch(`/api/bot/stop/${botId}`, { method: 'POST' });
      const result = await response.json();

      if (result.success) {
        const selectedBotId = store.getSelectedBotId();
        if (selectedBotId === botId) {
          store.setSelectedBotId(null);
        }
        await this.refresh();
      }
    } catch (error) {
      console.error('Error stopping bot:', error);
    }
  }
}
