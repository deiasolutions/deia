/**
 * DEIA Browser Extension - Options Script
 *
 * Handles settings page interactions.
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Get references to UI elements
  const autoLogCheckbox = document.getElementById('autoLog');
  const projectNameInput = document.getElementById('projectName');
  const saveButton = document.getElementById('saveButton');
  const resetButton = document.getElementById('resetButton');
  const statusMessage = document.getElementById('statusMessage');

  // Load current settings
  await loadSettings();

  // Save button handler
  saveButton.addEventListener('click', async () => {
    const settings = {
      autoLog: autoLogCheckbox.checked,
      projectName: projectNameInput.value || 'browser-session'
    };

    try {
      await chrome.storage.local.set(settings);
      showStatus('Settings saved successfully!', 'success');
    } catch (error) {
      showStatus('Error saving settings: ' + error.message, 'error');
    }
  });

  // Reset button handler
  resetButton.addEventListener('click', async () => {
    if (confirm('Reset all settings to defaults?')) {
      const defaults = {
        autoLog: true,
        projectName: 'browser-session'
      };

      try {
        await chrome.storage.local.set(defaults);
        await loadSettings();
        showStatus('Settings reset to defaults', 'success');
      } catch (error) {
        showStatus('Error resetting settings: ' + error.message, 'error');
      }
    }
  });
});

/**
 * Load settings from storage
 */
async function loadSettings() {
  const settings = await chrome.storage.local.get(['autoLog', 'projectName']);

  document.getElementById('autoLog').checked = settings.autoLog !== false;
  document.getElementById('projectName').value = settings.projectName || 'browser-session';
}

/**
 * Show status message
 */
function showStatus(message, type) {
  const statusMessage = document.getElementById('statusMessage');
  statusMessage.textContent = message;
  statusMessage.className = `status-message ${type}`;
  statusMessage.style.display = 'block';

  setTimeout(() => {
    statusMessage.style.display = 'none';
  }, 3000);
}
