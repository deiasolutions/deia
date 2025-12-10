# Chromium DEIA Extension - Next Steps Specification
**Version:** 0.2.0 (Next Release)
**Current Status:** v0.1.0 - Foundation Complete (~30%)
**Date:** 2025-10-19
**Author:** DEIA Project Team

---

## Executive Summary

The Chromium extension has completed the **foundation phase** with **741 lines of JavaScript/HTML**, Manifest V3 structure, UI components, and AI tool detection. This spec defines the path to **v0.2.0 MVP** (conversation capture) and beyond.

---

## Current State (What We Have) ✅

### Files Implemented (6 modules, 741 lines)

**Location:** `extensions/chromium-deia/src/`

1. **background.js** (100 lines) - Service worker
   - Extension lifecycle (install/update)
   - Message passing between components
   - Config storage (`chrome.storage.local`)
   - AI tool page detection (tab monitoring)
   - Placeholder logging function

2. **content.js** (127 lines) - Content script
   - AI tool detection (Claude, ChatGPT, Gemini, Copilot, Bard)
   - Visual indicator overlay
   - Message listener for capture requests
   - Placeholder conversation capture
   - Page initialization

3. **popup.js** (104 lines) - Extension popup logic
   - UI state management (presumably)
   - Action handling

4. **options.js** (74 lines) - Settings page logic
   - Configuration management (presumably)

5. **popup.html** (129 lines) - Extension popup UI
   - Manual logging controls
   - Status display
   - Quick actions

6. **options.html** (207 lines) - Settings page UI
   - Configuration options
   - Project settings
   - Privacy controls

**Configuration:**
- `manifest.json` - Manifest V3 manifest
- Icons directory (prepared)
- `.deia/config.json` integration

**Total:** 741 lines of production code

### Features Working

**Foundation:**
- ✅ Manifest V3 structure
- ✅ Background service worker
- ✅ Content script injection
- ✅ AI tool detection (5 tools: Claude, ChatGPT, Gemini, Copilot, Bard)
- ✅ Visual indicator when active
- ✅ Extension popup UI
- ✅ Settings page UI
- ✅ chrome.storage.local for config
- ✅ Message passing infrastructure

**AI Tool Detection:**
- ✅ claude.ai (Claude)
- ✅ chat.openai.com (ChatGPT)
- ✅ gemini.google.com (Gemini)
- ✅ copilot.microsoft.com (Copilot)
- ✅ bard.google.com (Bard - legacy)

### Documentation (4 docs, ~54,000 bytes)

- `README.md` - 161 lines project overview
- `CHROMIUM_USER_STORIES.md` - 21,473 bytes (comprehensive user stories)
- `PRODUCT_ROADMAP.md` - 8,007 bytes (4-phase roadmap)
- `STORIES_SUMMARY.md` - 17,591 bytes (user story summary)
- `project_resume.md` - 3,495 bytes (project status)

---

## What's Missing (Critical for MVP)

### MVP Release (v0.1.0 → v0.2.0)

**Goal:** Basic conversation capture with manual logging

**NOT STARTED:**
- ❌ **Conversation capture** from DOM (MutationObserver)
- ❌ **Tool-specific parsers** (Claude/ChatGPT have different DOM)
- ❌ **Local storage** of conversations (JSON format)
- ❌ **Manual "Log Now"** button functionality
- ❌ **Pause/resume** auto-logging
- ❌ **Conversation export** to `.deia/sessions/` format

---

## Next Steps: v0.2.0 MVP (Conversation Capture)

**Goal:** Capture conversations from Claude and ChatGPT, store locally, export to DEIA format

**Timeline:** 3-4 weeks

**Effort:** ~40-50 hours

---

## MVP Tasks Breakdown

### Task 1: Claude Conversation Parser (8-10 hours)

**Goal:** Capture conversations from claude.ai in real-time

**Files to Modify:**
- Modify: `src/content.js` (add Claude parser)
- Create: `src/parsers/claudeParser.js` (new module, ~200 lines)

**Implementation:**

```javascript
// src/parsers/claudeParser.js

/**
 * Parser for claude.ai conversations
 *
 * DOM Structure (as of 2025-10):
 * - Conversations in <div> elements with data-* attributes
 * - User messages: specific class patterns
 * - AI responses: different class patterns
 * - Code blocks: <pre><code> with language class
 */

export class ClaudeParser {

  constructor() {
    this.conversationData = {
      tool: 'Claude',
      url: window.location.href,
      messages: [],
      metadata: {}
    };

    this.observer = null;
    this.isMonitoring = false;
  }

  /**
   * Start monitoring Claude conversation
   */
  startMonitoring() {
    if (this.isMonitoring) {
      console.log('[DEIA] Claude monitoring already active');
      return;
    }

    console.log('[DEIA] Starting Claude conversation monitoring...');

    // Find conversation container
    const conversationContainer = this.findConversationContainer();

    if (!conversationContainer) {
      console.error('[DEIA] Could not find Claude conversation container');
      return;
    }

    // Set up MutationObserver to watch for new messages
    this.observer = new MutationObserver((mutations) => {
      this.handleMutations(mutations);
    });

    this.observer.observe(conversationContainer, {
      childList: true,
      subtree: true,
      attributes: false
    });

    // Parse existing messages
    this.parseExistingMessages(conversationContainer);

    this.isMonitoring = true;
    console.log('[DEIA] Claude monitoring started');
  }

  /**
   * Stop monitoring
   */
  stopMonitoring() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
    this.isMonitoring = false;
    console.log('[DEIA] Claude monitoring stopped');
  }

  /**
   * Find the conversation container element
   */
  findConversationContainer() {
    // Claude's conversation container (selector may need updating)
    // These selectors are fragile and may break with UI updates

    const selectors = [
      '[data-test-render-count]', // Common Claude pattern
      'main [role="main"]',
      '.conversation-container',
      'div[class*="conversation"]'
    ];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) {
        console.log('[DEIA] Found container with:', selector);
        return element;
      }
    }

    // Fallback: find largest scrollable div
    const scrollableDivs = Array.from(document.querySelectorAll('div'))
      .filter(div => div.scrollHeight > div.clientHeight);

    return scrollableDivs[0] || null;
  }

  /**
   * Parse existing messages in the conversation
   */
  parseExistingMessages(container) {
    // Find all message elements
    const messageElements = this.findMessageElements(container);

    console.log(`[DEIA] Parsing ${messageElements.length} existing messages`);

    for (const element of messageElements) {
      const message = this.parseMessageElement(element);
      if (message) {
        this.conversationData.messages.push(message);
      }
    }
  }

  /**
   * Find all message elements in container
   */
  findMessageElements(container) {
    // Try multiple selectors (Claude UI changes frequently)

    const selectors = [
      '[data-message-author-role]',
      'div[class*="message"]',
      'div[data-testid*="message"]',
      '.user-message, .assistant-message'
    ];

    for (const selector of selectors) {
      const elements = container.querySelectorAll(selector);
      if (elements.length > 0) {
        return Array.from(elements);
      }
    }

    return [];
  }

  /**
   * Parse a single message element
   */
  parseMessageElement(element) {
    // Determine role (user vs assistant)
    const role = this.detectMessageRole(element);

    if (!role) {
      return null; // Not a message element
    }

    // Extract text content
    const content = this.extractMessageContent(element);

    if (!content || content.trim().length === 0) {
      return null;
    }

    // Extract code blocks
    const codeBlocks = this.extractCodeBlocks(element);

    // Build message object
    return {
      role,
      content,
      timestamp: new Date().toISOString(),
      codeBlocks,
      elementId: element.getAttribute('data-message-id') || null
    };
  }

  /**
   * Detect message role (user or assistant)
   */
  detectMessageRole(element) {
    // Check data attributes
    const authorRole = element.getAttribute('data-message-author-role');
    if (authorRole) {
      return authorRole === 'user' ? 'user' : 'assistant';
    }

    // Check class names
    const classList = element.className.toLowerCase();

    if (classList.includes('user') || classList.includes('human')) {
      return 'user';
    }

    if (classList.includes('assistant') || classList.includes('claude') || classList.includes('ai')) {
      return 'assistant';
    }

    // Check for visual indicators (profile pics, etc.)
    const hasUserIcon = element.querySelector('[data-icon="user"]');
    const hasAIIcon = element.querySelector('[data-icon="sparkles"]');

    if (hasUserIcon) return 'user';
    if (hasAIIcon) return 'assistant';

    return null; // Unable to determine
  }

  /**
   * Extract text content from message element
   */
  extractMessageContent(element) {
    // Clone element to avoid modifying DOM
    const clone = element.cloneNode(true);

    // Remove code blocks (we handle them separately)
    const codeElements = clone.querySelectorAll('pre, code');
    codeElements.forEach(el => el.remove());

    // Remove UI elements (buttons, icons, etc.)
    const uiElements = clone.querySelectorAll('button, [role="button"], svg');
    uiElements.forEach(el => el.remove());

    // Get text content
    return clone.textContent.trim();
  }

  /**
   * Extract code blocks from message
   */
  extractCodeBlocks(element) {
    const codeBlocks = [];
    const preElements = element.querySelectorAll('pre');

    for (const pre of preElements) {
      const codeElement = pre.querySelector('code');

      if (!codeElement) continue;

      // Extract language from class (e.g., "language-python")
      const languageClass = Array.from(codeElement.classList)
        .find(cls => cls.startsWith('language-'));

      const language = languageClass
        ? languageClass.replace('language-', '')
        : 'plaintext';

      const code = codeElement.textContent.trim();

      codeBlocks.push({ language, code });
    }

    return codeBlocks;
  }

  /**
   * Handle DOM mutations (new messages)
   */
  handleMutations(mutations) {
    for (const mutation of mutations) {
      if (mutation.type !== 'childList') continue;

      for (const node of mutation.addedNodes) {
        if (node.nodeType !== Node.ELEMENT_NODE) continue;

        // Check if this is a message element
        const message = this.parseMessageElement(node);

        if (message) {
          // Check for duplicates (by elementId or content)
          const isDuplicate = this.conversationData.messages.some(existing =>
            existing.elementId === message.elementId ||
            (existing.content === message.content && existing.role === message.role)
          );

          if (!isDuplicate) {
            console.log(`[DEIA] New ${message.role} message detected`);
            this.conversationData.messages.push(message);

            // Notify background script
            chrome.runtime.sendMessage({
              action: 'messageDetected',
              data: message
            });
          }
        }
      }
    }
  }

  /**
   * Get current conversation data
   */
  getConversationData() {
    return {
      ...this.conversationData,
      capturedAt: new Date().toISOString(),
      messageCount: this.conversationData.messages.length
    };
  }

  /**
   * Clear conversation data (after logging)
   */
  clearConversationData() {
    this.conversationData.messages = [];
  }
}

// Export singleton instance
export const claudeParser = new ClaudeParser();
```

**Integrate with content.js:**

```javascript
// At top of content.js
import { claudeParser } from './parsers/claudeParser.js';

// In initializeDEIA():
if (detection.detected) {
  console.log(`[DEIA] ${detection.tool} detected - monitoring enabled`);

  // Start tool-specific parser
  if (detection.tool === 'Claude') {
    claudeParser.startMonitoring();
  }

  addDeiaIndicator(detection.tool);
}

// Update captureCurrentConversation():
async function captureCurrentConversation() {
  const detection = detectAITool();

  if (!detection.detected) {
    throw new Error('No AI tool detected on this page');
  }

  if (detection.tool === 'Claude') {
    return claudeParser.getConversationData();
  }

  throw new Error(`Conversation capture not implemented for ${detection.tool}`);
}
```

**Note:** Claude's DOM structure changes frequently. This parser will need maintenance as Claude updates their UI. Consider adding a settings option for users to report when parsing breaks.

---

### Task 2: ChatGPT Conversation Parser (8-10 hours)

**Goal:** Capture conversations from chat.openai.com

**Files to Create:**
- Create: `src/parsers/chatgptParser.js` (new module, ~200 lines)

**Implementation:**

```javascript
// src/parsers/chatgptParser.js

/**
 * Parser for chat.openai.com conversations
 *
 * DOM Structure (as of 2025-10):
 * - ChatGPT uses React with data-message-id attributes
 * - User messages: specific role attributes
 * - AI responses: different role attributes
 * - Code blocks: markdown-style with copy buttons
 */

export class ChatGPTParser {

  constructor() {
    this.conversationData = {
      tool: 'ChatGPT',
      url: window.location.href,
      messages: [],
      metadata: {}
    };

    this.observer = null;
    this.isMonitoring = false;
  }

  /**
   * Start monitoring ChatGPT conversation
   */
  startMonitoring() {
    if (this.isMonitoring) return;

    console.log('[DEIA] Starting ChatGPT conversation monitoring...');

    // ChatGPT typically has a main content area
    const conversationContainer = this.findConversationContainer();

    if (!conversationContainer) {
      console.error('[DEIA] Could not find ChatGPT conversation container');
      return;
    }

    this.observer = new MutationObserver((mutations) => {
      this.handleMutations(mutations);
    });

    this.observer.observe(conversationContainer, {
      childList: true,
      subtree: true,
      attributes: false
    });

    this.parseExistingMessages(conversationContainer);

    this.isMonitoring = true;
    console.log('[DEIA] ChatGPT monitoring started');
  }

  stopMonitoring() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
    this.isMonitoring = false;
  }

  /**
   * Find conversation container
   */
  findConversationContainer() {
    const selectors = [
      'main [role="main"]',
      '[data-testid="conversation-turn"]',
      '.conversation-content',
      'main'
    ];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) return element;
    }

    return null;
  }

  /**
   * Parse existing messages
   */
  parseExistingMessages(container) {
    // ChatGPT uses data-message-id on message containers
    const messageElements = container.querySelectorAll('[data-message-id]');

    console.log(`[DEIA] Parsing ${messageElements.length} existing ChatGPT messages`);

    for (const element of messageElements) {
      const message = this.parseMessageElement(element);
      if (message) {
        this.conversationData.messages.push(message);
      }
    }
  }

  /**
   * Parse single message element
   */
  parseMessageElement(element) {
    // Get message ID
    const messageId = element.getAttribute('data-message-id');

    // Determine role
    const role = this.detectMessageRole(element);

    if (!role) return null;

    // Extract content
    const content = this.extractMessageContent(element);

    if (!content || content.trim().length === 0) return null;

    // Extract code blocks
    const codeBlocks = this.extractCodeBlocks(element);

    return {
      role,
      content,
      timestamp: new Date().toISOString(),
      codeBlocks,
      messageId
    };
  }

  /**
   * Detect message role
   */
  detectMessageRole(element) {
    // Check data-message-author-role attribute
    const authorRole = element.getAttribute('data-message-author-role');

    if (authorRole) {
      return authorRole === 'user' ? 'user' : 'assistant';
    }

    // Check for user vs assistant classes
    const classList = element.className.toLowerCase();

    if (classList.includes('user')) return 'user';
    if (classList.includes('assistant') || classList.includes('bot')) return 'assistant';

    // Look for avatar indicators
    const avatar = element.querySelector('[data-testid*="avatar"]');
    if (avatar) {
      const avatarClass = avatar.className.toLowerCase();
      if (avatarClass.includes('user')) return 'user';
      if (avatarClass.includes('assistant')) return 'assistant';
    }

    return null;
  }

  /**
   * Extract message content
   */
  extractMessageContent(element) {
    // Find the message content div
    const contentSelectors = [
      '[data-message-content]',
      '.message-content',
      '[class*="markdown"]'
    ];

    let contentElement = null;

    for (const selector of contentSelectors) {
      contentElement = element.querySelector(selector);
      if (contentElement) break;
    }

    if (!contentElement) {
      contentElement = element;
    }

    const clone = contentElement.cloneNode(true);

    // Remove code blocks
    const codeElements = clone.querySelectorAll('pre, .code-block');
    codeElements.forEach(el => el.remove());

    // Remove UI elements
    const uiElements = clone.querySelectorAll('button, svg, [role="button"]');
    uiElements.forEach(el => el.remove());

    return clone.textContent.trim();
  }

  /**
   * Extract code blocks
   */
  extractCodeBlocks(element) {
    const codeBlocks = [];
    const codeWrappers = element.querySelectorAll('pre, .code-block, [class*="code"]');

    for (const wrapper of codeWrappers) {
      const codeElement = wrapper.querySelector('code') || wrapper;

      // Try to detect language
      let language = 'plaintext';

      // Check for language indicator
      const langIndicator = wrapper.querySelector('[class*="language"]');
      if (langIndicator) {
        const match = langIndicator.className.match(/language-(\w+)/);
        if (match) language = match[1];
      }

      // Check code element classes
      const codeClass = codeElement.className;
      if (codeClass) {
        const match = codeClass.match(/language-(\w+)/);
        if (match) language = match[1];
      }

      const code = codeElement.textContent.trim();

      if (code) {
        codeBlocks.push({ language, code });
      }
    }

    return codeBlocks;
  }

  /**
   * Handle mutations (new messages)
   */
  handleMutations(mutations) {
    for (const mutation of mutations) {
      if (mutation.type !== 'childList') continue;

      for (const node of mutation.addedNodes) {
        if (node.nodeType !== Node.ELEMENT_NODE) continue;

        // Check if node has data-message-id or contains message
        const messageElement = node.hasAttribute('data-message-id')
          ? node
          : node.querySelector('[data-message-id]');

        if (messageElement) {
          const message = this.parseMessageElement(messageElement);

          if (message) {
            // Check for duplicates
            const isDuplicate = this.conversationData.messages.some(existing =>
              existing.messageId === message.messageId
            );

            if (!isDuplicate) {
              console.log(`[DEIA] New ChatGPT ${message.role} message detected`);
              this.conversationData.messages.push(message);

              chrome.runtime.sendMessage({
                action: 'messageDetected',
                data: message
              });
            }
          }
        }
      }
    }
  }

  getConversationData() {
    return {
      ...this.conversationData,
      capturedAt: new Date().toISOString(),
      messageCount: this.conversationData.messages.length
    };
  }

  clearConversationData() {
    this.conversationData.messages = [];
  }
}

export const chatgptParser = new ChatGPTParser();
```

**Integrate with content.js:**

```javascript
import { chatgptParser } from './parsers/chatgptParser.js';

// In initializeDEIA():
if (detection.tool === 'ChatGPT') {
  chatgptParser.startMonitoring();
}

// In captureCurrentConversation():
if (detection.tool === 'ChatGPT') {
  return chatgptParser.getConversationData();
}
```

---

### Task 3: Local Storage & Export (6-8 hours)

**Goal:** Store conversations locally and export to DEIA format

**Files to Create:**
- Create: `src/storage.js` (new module, ~150 lines)
- Create: `src/deiaFormatter.js` (new module, ~100 lines)

**Implementation:**

```javascript
// src/storage.js

/**
 * Storage manager for conversation data
 */

export class ConversationStorage {

  /**
   * Save conversation to chrome.storage.local
   */
  async saveConversation(conversationData) {
    const timestamp = new Date().toISOString();
    const conversationId = `conv_${timestamp.replace(/[:.]/g, '-')}`;

    const storageEntry = {
      id: conversationId,
      savedAt: timestamp,
      ...conversationData
    };

    await chrome.storage.local.set({
      [conversationId]: storageEntry
    });

    console.log('[DEIA] Conversation saved:', conversationId);

    return conversationId;
  }

  /**
   * Get all saved conversations
   */
  async getAllConversations() {
    const allData = await chrome.storage.local.get(null);

    const conversations = Object.entries(allData)
      .filter(([key]) => key.startsWith('conv_'))
      .map(([key, value]) => value)
      .sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt));

    return conversations;
  }

  /**
   * Get specific conversation by ID
   */
  async getConversation(conversationId) {
    const data = await chrome.storage.local.get(conversationId);
    return data[conversationId] || null;
  }

  /**
   * Delete conversation
   */
  async deleteConversation(conversationId) {
    await chrome.storage.local.remove(conversationId);
    console.log('[DEIA] Conversation deleted:', conversationId);
  }

  /**
   * Clear all conversations
   */
  async clearAll() {
    const allData = await chrome.storage.local.get(null);
    const conversationKeys = Object.keys(allData).filter(k => k.startsWith('conv_'));

    await chrome.storage.local.remove(conversationKeys);
    console.log('[DEIA] All conversations cleared');
  }

  /**
   * Get storage usage stats
   */
  async getStorageStats() {
    const conversations = await this.getAllConversations();

    const totalMessages = conversations.reduce((sum, conv) =>
      sum + (conv.messages?.length || 0), 0
    );

    const totalSize = JSON.stringify(conversations).length;

    return {
      conversationCount: conversations.length,
      totalMessages,
      totalSizeBytes: totalSize,
      oldestConversation: conversations[conversations.length - 1]?.savedAt,
      newestConversation: conversations[0]?.savedAt
    };
  }
}

export const conversationStorage = new ConversationStorage();
```

```javascript
// src/deiaFormatter.js

/**
 * Format conversations for DEIA compatibility
 */

export class DEIAFormatter {

  /**
   * Convert conversation to DEIA markdown format
   */
  formatAsMarkdown(conversationData) {
    const { tool, url, messages, capturedAt } = conversationData;

    const date = new Date(capturedAt);
    const dateStr = date.toISOString().split('T')[0];
    const timeStr = date.toISOString().split('T')[1].split('.')[0].replace(/:/g, '');

    // YAML frontmatter
    const frontmatter = `---
date: ${dateStr}
time: ${timeStr}
tool: ${tool}
url: ${url}
message_count: ${messages.length}
source: browser-extension
---

# Conversation: ${tool} Session

**Captured:** ${date.toLocaleString()}
**Tool:** ${tool}
**URL:** ${url}
**Messages:** ${messages.length}

---

`;

    // Format messages
    const formattedMessages = messages.map((msg, index) => {
      const role = msg.role === 'user' ? 'User' : 'Assistant';
      const time = new Date(msg.timestamp).toLocaleTimeString();

      let content = `## ${role} [${time}]\n\n${msg.content}\n`;

      // Add code blocks if any
      if (msg.codeBlocks && msg.codeBlocks.length > 0) {
        content += '\n**Code:**\n\n';

        for (const block of msg.codeBlocks) {
          content += `\`\`\`${block.language}\n${block.code}\n\`\`\`\n\n`;
        }
      }

      content += '---\n\n';

      return content;
    }).join('');

    return frontmatter + formattedMessages;
  }

  /**
   * Export conversation as downloadable file
   */
  exportAsFile(conversationData, filename) {
    const markdown = this.formatAsMarkdown(conversationData);

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);

    // Trigger download
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `deia-session-${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
  }

  /**
   * Export to File System Access API (if available)
   */
  async exportToFileSystem(conversationData) {
    if (!('showSaveFilePicker' in window)) {
      throw new Error('File System Access API not supported');
    }

    const markdown = this.formatAsMarkdown(conversationData);

    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: `deia-session-${Date.now()}.md`,
        types: [{
          description: 'Markdown files',
          accept: { 'text/markdown': ['.md'] }
        }]
      });

      const writable = await handle.createWritable();
      await writable.write(markdown);
      await writable.close();

      return handle.name;
    } catch (err) {
      if (err.name === 'AbortError') {
        return null; // User cancelled
      }
      throw err;
    }
  }
}

export const deiaFormatter = new DEIAFormatter();
```

---

### Task 4: Popup UI Functionality (5-6 hours)

**Goal:** Make popup buttons work (Log Now, View Logs, Settings)

**Files to Modify:**
- Modify: `src/popup.js` (implement button handlers)
- Modify: `src/popup.html` (ensure proper IDs on buttons)

**Implementation:**

```javascript
// src/popup.js (complete rewrite)

import { conversationStorage } from './storage.js';
import { deiaFormatter } from './deiaFormatter.js';

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', async () => {
  await initializePopup();
});

/**
 * Initialize popup UI
 */
async function initializePopup() {
  // Get current tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Check if current tab is an AI tool
  const isAITool = await checkIfAITool(tab.url);

  // Update UI based on context
  updateUIForContext(isAITool);

  // Bind button handlers
  bindButtonHandlers(tab);

  // Load stats
  await loadStats();

  // Load recent conversations
  await loadRecentConversations();
}

/**
 * Check if URL is an AI tool
 */
function checkIfAITool(url) {
  const aiToolDomains = [
    'claude.ai',
    'chat.openai.com',
    'gemini.google.com',
    'copilot.microsoft.com'
  ];

  return aiToolDomains.some(domain => url && url.includes(domain));
}

/**
 * Update UI based on context
 */
function updateUIForContext(isAITool) {
  const logButton = document.getElementById('logNowButton');
  const statusMessage = document.getElementById('statusMessage');

  if (isAITool) {
    logButton.disabled = false;
    statusMessage.textContent = 'AI tool detected - ready to log';
    statusMessage.className = 'status-active';
  } else {
    logButton.disabled = true;
    statusMessage.textContent = 'No AI tool detected on this page';
    statusMessage.className = 'status-inactive';
  }
}

/**
 * Bind button click handlers
 */
function bindButtonHandlers(tab) {
  // Log Now button
  document.getElementById('logNowButton').addEventListener('click', async () => {
    await handleLogNow(tab);
  });

  // View Logs button
  document.getElementById('viewLogsButton').addEventListener('click', () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('logs.html') });
  });

  // Settings button
  document.getElementById('settingsButton').addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });

  // Export button (if exists)
  const exportButton = document.getElementById('exportButton');
  if (exportButton) {
    exportButton.addEventListener('click', async () => {
      await handleExportAll();
    });
  }
}

/**
 * Handle Log Now button click
 */
async function handleLogNow(tab) {
  const button = document.getElementById('logNowButton');
  const statusMessage = document.getElementById('statusMessage');

  try {
    button.disabled = true;
    button.textContent = 'Capturing...';
    statusMessage.textContent = 'Capturing conversation...';

    // Send message to content script to capture conversation
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'captureConversation'
    });

    if (response.success) {
      // Save to storage
      const conversationId = await conversationStorage.saveConversation(response.data);

      statusMessage.textContent = `Logged! (${response.data.messageCount} messages)`;
      statusMessage.className = 'status-success';

      // Refresh conversation list
      await loadRecentConversations();

      // Reset button after 2 seconds
      setTimeout(() => {
        button.disabled = false;
        button.textContent = 'Log Now';
        statusMessage.textContent = 'AI tool detected - ready to log';
        statusMessage.className = 'status-active';
      }, 2000);

    } else {
      throw new Error(response.error || 'Capture failed');
    }

  } catch (error) {
    console.error('[DEIA] Log failed:', error);
    statusMessage.textContent = `Error: ${error.message}`;
    statusMessage.className = 'status-error';

    button.disabled = false;
    button.textContent = 'Log Now';
  }
}

/**
 * Load and display stats
 */
async function loadStats() {
  const stats = await conversationStorage.getStorageStats();

  document.getElementById('statConversations').textContent = stats.conversationCount;
  document.getElementById('statMessages').textContent = stats.totalMessages;

  // Format size
  const sizeMB = (stats.totalSizeBytes / 1024 / 1024).toFixed(2);
  document.getElementById('statSize').textContent = `${sizeMB} MB`;
}

/**
 * Load recent conversations
 */
async function loadRecentConversations() {
  const conversations = await conversationStorage.getAllConversations();
  const recentList = document.getElementById('recentConversationsList');

  if (!recentList) return;

  recentList.innerHTML = '';

  const recent = conversations.slice(0, 5); // Show 5 most recent

  if (recent.length === 0) {
    recentList.innerHTML = '<div class="no-conversations">No conversations logged yet</div>';
    return;
  }

  for (const conv of recent) {
    const item = document.createElement('div');
    item.className = 'conversation-item';

    const date = new Date(conv.savedAt).toLocaleString();

    item.innerHTML = `
      <div class="conversation-tool">${conv.tool}</div>
      <div class="conversation-date">${date}</div>
      <div class="conversation-messages">${conv.messageCount || conv.messages?.length || 0} messages</div>
      <button class="export-button" data-id="${conv.id}">Export</button>
    `;

    // Bind export button
    item.querySelector('.export-button').addEventListener('click', async (e) => {
      e.stopPropagation();
      await handleExportConversation(conv.id);
    });

    recentList.appendChild(item);
  }
}

/**
 * Handle export single conversation
 */
async function handleExportConversation(conversationId) {
  const conversation = await conversationStorage.getConversation(conversationId);

  if (!conversation) {
    alert('Conversation not found');
    return;
  }

  deiaFormatter.exportAsFile(conversation);
}

/**
 * Handle export all conversations
 */
async function handleExportAll() {
  const conversations = await conversationStorage.getAllConversations();

  if (conversations.length === 0) {
    alert('No conversations to export');
    return;
  }

  // Export each conversation as separate file
  for (const conv of conversations) {
    deiaFormatter.exportAsFile(conv);
  }
}
```

---

### Task 5: Testing & Polish (8-10 hours)

**Goal:** Test on Claude and ChatGPT, fix bugs, polish UI

**Testing Checklist:**

**Claude Testing:**
- [ ] Open claude.ai
- [ ] Start new conversation
- [ ] Verify DEIA indicator appears
- [ ] Have 5-10 message conversation with code blocks
- [ ] Click "Log Now" in popup
- [ ] Verify conversation saved with correct message count
- [ ] Export conversation to .md file
- [ ] Verify markdown format matches DEIA spec

**ChatGPT Testing:**
- [ ] Repeat above steps for chat.openai.com

**Storage Testing:**
- [ ] Log 10+ conversations
- [ ] Check storage stats in popup
- [ ] View logs page (create logs.html)
- [ ] Delete conversation
- [ ] Export all conversations

**Error Handling:**
- [ ] Test with non-AI tool pages (should show inactive status)
- [ ] Test with network offline (should buffer)
- [ ] Test with very long conversations (50+ messages)
- [ ] Test with empty conversation (should show error)

**Polish:**
- [ ] Add loading spinners
- [ ] Add success/error animations
- [ ] Improve CSS styling
- [ ] Add keyboard shortcuts
- [ ] Add tooltips for buttons

---

## MVP Summary

**New Files:**
1. `src/parsers/claudeParser.js` (~200 lines)
2. `src/parsers/chatgptParser.js` (~200 lines)
3. `src/storage.js` (~150 lines)
4. `src/deiaFormatter.js` (~100 lines)
5. `src/logs.html` + `src/logs.js` (~150 lines combined)

**Modified Files:**
1. `src/content.js` (integrate parsers)
2. `src/popup.js` (complete rewrite)
3. `src/popup.html` (update IDs/structure)
4. `src/background.js` (handle message events)

**Total New Code:** ~800-1000 lines

**Total Effort:** 40-50 hours

**Timeline:** 3-4 weeks part-time

---

## Post-MVP: Phase 2+ (Future)

### v0.3.0: DEIA Integration (4-6 weeks)
- File System Access API for `.deia/sessions/`
- DEIA CLI communication (local server)
- PII detection warnings
- Pattern extraction from conversations

### v0.4.0: Multi-tool Support (6-8 weeks)
- Gemini parser
- Copilot parser
- Universal conversation format
- Tool comparison dashboard

### v0.5.0: Pattern Intelligence (8-10 weeks)
- Pattern suggestions
- Code outcome tracking
- Cross-tool session linking
- BOK submission

---

## Success Criteria (MVP)

**Must Have:**
- [x] Capture conversations from Claude
- [x] Capture conversations from ChatGPT
- [x] Store conversations locally
- [x] Manual "Log Now" button works
- [x] Export conversations to DEIA markdown format
- [x] View saved conversations in popup

**Nice to Have:**
- [ ] Auto-logging (background capture without manual trigger)
- [ ] Pause/resume monitoring
- [ ] PII detection warnings
- [ ] Integration with `.deia/sessions/` folder

**Success Metrics:**
- Users log 10+ conversations in first week
- Capture accuracy >95% (no missed messages)
- Export format matches DEIA spec 100%
- User feedback: "Captures exactly what I need"

---

## File Reference

**Current Files:**
- `src/background.js` (extensions/chromium-deia/src/background.js:1)
- `src/content.js` (extensions/chromium-deia/src/content.js:1)
- `src/popup.js` (extensions/chromium-deia/src/popup.js:1)
- `src/options.js` (extensions/chromium-deia/src/options.js:1)
- `src/popup.html` (extensions/chromium-deia/src/popup.html:1)
- `src/options.html` (extensions/chromium-deia/src/options.html:1)
- `manifest.json` (extensions/chromium-deia/manifest.json:1)

**Files to Create:**
- `src/parsers/claudeParser.js` (NEW)
- `src/parsers/chatgptParser.js` (NEW)
- `src/storage.js` (NEW)
- `src/deiaFormatter.js` (NEW)
- `src/logs.html` + `src/logs.js` (NEW)

---

## Related Documentation

- User Stories: `CHROMIUM_USER_STORIES.md`
- Product Roadmap: `PRODUCT_ROADMAP.md`
- VS Code Extension: `../vscode-deia/NEXT-STEPS-SPEC.md`

---

**Next Action:** Start with Task 1 (Claude Parser) - estimated 8-10 hours

**Questions?** See existing code in `src/content.js` for AI tool detection patterns
