/**
 * Toast Notification System
 * Displays temporary user feedback messages with different styles
 */

class Toast {
  static toastContainer = null;

  /**
   * Initialize toast container if not already done
   */
  static initContainer() {
    if (this.toastContainer) return;

    this.toastContainer = document.createElement('div');
    this.toastContainer.id = 'toastContainer';
    this.toastContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10000;
      max-width: 400px;
    `;
    document.body.appendChild(this.toastContainer);

    // Add toast styles if not already in document
    if (!document.getElementById('toastStyles')) {
      const style = document.createElement('style');
      style.id = 'toastStyles';
      style.textContent = `
        .toast {
          background: white;
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 12px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          display: flex;
          align-items: center;
          gap: 12px;
          animation: slideInRight 0.3s ease-out;
          min-width: 300px;
        }

        .toast.success {
          background: #4CAF50;
          color: white;
        }

        .toast.error {
          background: #f44336;
          color: white;
        }

        .toast.warning {
          background: #ff9800;
          color: white;
        }

        .toast.info {
          background: #2196F3;
          color: white;
        }

        .toast-content {
          flex: 1;
          font-size: 14px;
          font-weight: 500;
        }

        .toast-close {
          background: none;
          border: none;
          color: inherit;
          cursor: pointer;
          font-size: 20px;
          padding: 0;
          opacity: 0.8;
          transition: opacity 0.2s;
        }

        .toast-close:hover {
          opacity: 1;
        }

        @keyframes slideInRight {
          from {
            transform: translateX(400px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        @keyframes slideOutRight {
          from {
            transform: translateX(0);
            opacity: 1;
          }
          to {
            transform: translateX(400px);
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  /**
   * Show a toast notification
   * @param {string} message - Message to display
   * @param {string} type - 'success', 'error', 'warning', 'info' (default: 'info')
   * @param {number} duration - How long to show in milliseconds (0 = never auto-hide)
   */
  static show(message, type = 'info', duration = 3000) {
    this.initContainer();

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    // Create content
    const content = document.createElement('div');
    content.className = 'toast-content';
    content.textContent = message;

    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'toast-close';
    closeBtn.innerHTML = '×';
    closeBtn.onclick = () => this.removeToast(toast);

    toast.appendChild(content);
    toast.appendChild(closeBtn);

    // Add to container
    this.toastContainer.insertBefore(toast, this.toastContainer.firstChild);

    // Auto-remove after duration
    if (duration > 0) {
      setTimeout(() => {
        this.removeToast(toast);
      }, duration);
    }

    return toast;
  }

  /**
   * Remove a toast with animation
   */
  static removeToast(toast) {
    toast.style.animation = 'slideOutRight 0.3s ease-out forwards';
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }

  /**
   * Helper methods for common toast types
   */
  static success(message, duration = 3000) {
    return this.show(message, 'success', duration);
  }

  static error(message, duration = 4000) {
    return this.show(message, 'error', duration);
  }

  static warning(message, duration = 3500) {
    return this.show(message, 'warning', duration);
  }

  static info(message, duration = 3000) {
    return this.show(message, 'info', duration);
  }

  /**
   * Show a loading toast that doesn't auto-dismiss
   */
  static loading(message) {
    return this.show(message, 'info', 0);
  }
}

// Export for use in other modules
const showSuccess = (msg) => Toast.success(msg);
const showError = (msg) => Toast.error(msg);
const showWarning = (msg) => Toast.warning(msg);
const showInfo = (msg) => Toast.info(msg);
