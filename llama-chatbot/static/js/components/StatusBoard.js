/**
 * StatusBoard.js - Status Board Component
 */

class StatusBoard {
  constructor() {
    this.statusContainer = document.getElementById('statusPanel');
  }

  init() {
    if (!this.statusContainer) {
      this.statusContainer = document.createElement('div');
      this.statusContainer.id = 'statusPanel';
      this.statusContainer.style.cssText = 'padding: 15px; background: #1a1a1a; border-radius: 8px; margin: 10px;';
      document.body.appendChild(this.statusContainer);
    }
  }

  updateStatus(bots) {
    if (!this.statusContainer) return;

    this.statusContainer.innerHTML = '<h3 style="margin-top: 0;">Active Bots</h3>';

    if (!bots || bots.length === 0) {
      this.statusContainer.innerHTML += '<p style="color: #999;">No active bots</p>';
      return;
    }

    bots.forEach(bot => {
      const botEl = document.createElement('div');
      botEl.style.cssText = 'padding: 8px; margin: 5px 0; background: #2a2a2a; border-radius: 4px; border-left: 3px solid ' +
                           (bot.running ? '#4CAF50' : '#f44336') + ';';

      const indicator = bot.running ? '🟢' : '🔴';
      botEl.innerHTML = `
        <div><strong>${bot.id}</strong> ${indicator}</div>
        <div style="font-size: 12px; color: #999;">Port: ${bot.port || 'N/A'}</div>
      `;

      this.statusContainer.appendChild(botEl);
    });
  }
}
