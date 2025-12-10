# DEIA Bot Controller - User Guide

**Version:** 1.0
**Last Updated:** 2025-10-25
**Application:** Port 8000 Web Interface

---

## Quick Start (5 Minutes)

### Getting Started

1. **Open the Application**
   - Open your browser to: `http://localhost:8000`
   - You'll see the Bot Controller interface with a dark theme

2. **Launch Your First Bot**
   - Click the **"Launch Bot"** button (top-left)
   - Enter a bot ID (e.g., `BOT-001`)
   - Click **"Launch"**
   - Wait for the bot to initialize (usually <5 seconds)

3. **Send Your First Command**
   - Click on the bot name in the left panel to select it
   - Type a command in the input box at the bottom: `help`
   - Press **Enter** or click **Send**
   - You'll see the response in the chat window

4. **You're Ready!**
   - Chat history is automatically saved
   - You can launch multiple bots and switch between them
   - Commands are routed to the selected bot automatically

---

## Core Workflows

### Workflow 1: Launching a Bot

**Step-by-Step:**
1. Click **"Launch Bot"** button in the top-left panel
2. Enter bot ID in the dialog box (format: `BOT-XXX`)
3. Click **"Launch"** button
4. Status appears in the dashboard showing:
   - Bot ID
   - Status (starting → running)
   - PID (process ID)
   - Port number

**What to Look For:**
- ✅ Bot appears in the left panel
- ✅ Status shows "running"
- ✅ Input box becomes enabled (not grayed out)

**If Bot Won't Launch:**
- See Troubleshooting section below

### Workflow 2: Sending Commands

**Basic Command:**
```
Type your command → Press Enter → See response
```

**Example Commands:**
```
help                    # Get help on available commands
status                  # Check bot status
history                 # View command history
clear                   # Clear chat window
quit                    # Stop bot (graceful)
```

**Command Feedback:**
- **Sending...** indicator appears while command is being processed
- ✓ (checkmark) indicates successful execution
- ✗ (X) indicates error
- Command response appears in chat within 2-5 seconds

### Workflow 3: Viewing Chat History

**Auto-Loading:**
- History automatically loads when you select a bot
- Shows last 100 messages in chronological order (oldest at top)

**Navigation:**
- Scroll up to see older messages
- Click **"Load Earlier Messages"** button to load more
- Messages display with:
  - Timestamp
  - Sender (user or bot)
  - Message content

**Example History:**
```
[16:39:22] user: help
[16:39:23] bot: Available commands: help, status, history, ...
[16:40:15] user: status
[16:40:16] bot: Bot BOT-001 is running normally...
```

### Workflow 4: Switching Between Bots

**To Switch Bots:**
1. Click bot name in left panel
2. Chat history automatically switches
3. Input field focuses on new bot
4. Status updates to show new bot's information

**Important:**
- Each bot has separate chat history
- Chat history persists even if bot stops
- Switching bots does NOT affect their state

**Example:**
```
Switch from BOT-001 to BOT-002:
1. Click "BOT-002" in left panel
2. Chat history shows BOT-002's messages
3. Status panel updates with BOT-002's info
4. Next command goes to BOT-002
```

### Workflow 5: Stopping a Bot

**How to Stop:**
1. Click the **"Stop"** button next to bot name (if visible)
2. Or send command: `quit` or `shutdown`
3. Bot gracefully shuts down
4. Status changes to "stopped"
5. Input becomes disabled until bot is relaunched

**Safe Shutdown:**
- Bots complete current task before stopping
- No data loss
- Chat history is preserved
- Bot can be relaunched at any time

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Send current message |
| **Shift+Enter** | New line in message (if multi-line supported) |
| **Ctrl+K** | Clear chat history (current bot) |
| **Ctrl+L** | List all bots |
| **Ctrl+C** | Cancel ongoing operation |
| **Ctrl+W** | Close current bot connection |
| **Tab** | Autocomplete bot ID (if supported) |

**Example Usage:**
```
Type "BOT-" + Tab → Auto-completes to "BOT-001"
Type command + Enter → Sends immediately
Type "clear" + Enter → Clears chat window
```

---

## Troubleshooting

### Issue: "Bot won't launch"

**Symptoms:**
- Dialog closes but bot doesn't appear in list
- Status shows "error"
- Error message: "Failed to launch bot"

**Solutions:**
1. **Check Ollama is running**
   ```bash
   curl http://localhost:11434/api/tags
   ```
   Expected: List of available models

2. **Check port is available**
   ```bash
   netstat -an | grep 8001  # Port 8001 should be free
   ```

3. **Verify bot ID format**
   - Must be alphanumeric: `BOT-001`, `BOT-DEV-1`
   - Don't use special characters

4. **Check system resources**
   - Each bot needs ~100-200MB RAM
   - Make sure you have free memory available
   - Don't launch too many bots simultaneously (max 10 recommended)

### Issue: "No response to commands"

**Symptoms:**
- Send command but get no response
- "Sending..." indicator hangs
- No message appears in chat

**Solutions:**
1. **Verify bot is selected**
   - Make sure bot name is highlighted in left panel
   - Click bot name again if unsure

2. **Check bot status**
   - Look at status dashboard (right panel)
   - Bot should show "running"
   - If "paused", click "Resume"

3. **Try a simple command**
   ```
   help
   ```
   If this works, previous commands may have timed out

4. **Check connection**
   - Look at browser console (F12 → Console)
   - Any red errors? Check WebSocket is connected
   - Try refreshing page (Ctrl+R)

5. **Bot might be overloaded**
   - If bot is processing multiple tasks, response may be slow
   - Wait 30 seconds and try again

### Issue: "Can't see old messages"

**Symptoms:**
- Chat history appears empty
- New messages work but history doesn't load
- "Load Earlier Messages" button doesn't work

**Solutions:**
1. **Refresh page**
   - Press Ctrl+R (Windows) or Cmd+R (Mac)
   - History should reload

2. **Check database connection**
   - Server logs should show database connected
   - If disconnected, restart server

3. **Select bot again**
   - Click bot name again to reload history
   - Wait 2-3 seconds for history to load

4. **Clear browser cache**
   - Press Ctrl+Shift+Delete
   - Clear cookies and cached data
   - Reload page

### Issue: "Connection lost"

**Symptoms:**
- Sudden disconnection mid-chat
- WebSocket error in browser console
- Can't send new messages
- Status shows "disconnected"

**Recovery Steps:**
1. **Don't panic!** Your data is safe
2. **Refresh page:** Ctrl+R
3. **Reconnect:** Click bot name again
4. **Try again:** Send command should work

**Prevention:**
- Keep browser tab active (don't minimize)
- Don't close browser tab during active session
- Check network connection (wifi/ethernet)

---

## FAQ

### Q: Can I run multiple bots at the same time?

**A:** Yes! You can launch and run 1-10 bots simultaneously. Each bot:
- Runs independently
- Has separate chat history
- Gets its own port (8001, 8002, etc.)
- Can be paused/stopped individually

**Recommended:** 2-4 bots for best performance

### Q: How long do conversations persist?

**A:** Chat history is stored in the database and persists:
- ✅ After bot restarts
- ✅ After page refresh
- ✅ After browser closes (restart)
- ✅ For 90 days by default (then auto-deleted)

**To preserve longer:** Export chat before deletion

### Q: Can I export chat history?

**A:** Yes, click **"Export"** button (if visible):
- Exports as: `.txt` (plain text) or `.json` (structured)
- Includes: All messages, timestamps, metadata
- Can reimport to another bot

**How to Export:**
1. Select bot with history you want
2. Click "Export Chat" button
3. Choose format (TXT or JSON)
4. Save file to your computer

### Q: What if a bot gets stuck?

**A:** If bot seems frozen:
1. **Wait 30 seconds** - It may still be processing
2. **Check status** - Should show "busy" or "processing"
3. **Send interrupt** - Type `Ctrl+C` or click "Interrupt"
4. **Force restart** - Click "Stop" then "Launch" again

**Last resort:** Restart application server

### Q: How do I know if my command succeeded?

**A:** Look for indicators:
- ✓ **Checkmark** = Command executed successfully
- ✗ **X** = Command failed with error
- **Response** = Bot replied with result
- **Timestamp** = Shows when command was sent

**Example:**
```
user: help
✓ Available commands: help, status, history
```

### Q: Can multiple people use this at the same time?

**A:** Currently:
- ❌ NOT designed for multi-user concurrent access
- ✅ Single user per session recommended
- ⚠️ Multiple simultaneous users may cause conflicts

**For team use:** Implement authentication/sessions (future feature)

### Q: What's the max number of messages in chat history?

**A:** Unlimited! But for performance:
- History auto-loads last 100 messages
- Click "Load Earlier" to load older messages
- Export if you need to preserve large histories (1000+ messages)

### Q: How do I backup my chat history?

**A:** Three ways:
1. **Export:** Click "Export Chat" button
2. **Database backup:** Administrator backs up database
3. **Browser localStorage:** Automatically synced

**Recommendation:** Export important conversations weekly

---

## Getting Help

### Troubleshooting Checklist

Before asking for help, try:
- [ ] Refresh page (Ctrl+R)
- [ ] Check system has free memory
- [ ] Verify Ollama is running
- [ ] Check browser console for errors (F12)
- [ ] Try with a different browser
- [ ] Restart the application server

### Where to Report Issues

If you've tried troubleshooting and still have problems:

1. **Check logs:** `.deia/bot-logs/` for error messages
2. **Report issue** with:
   - What you were doing
   - Exact error message
   - Browser (Chrome, Firefox, Safari)
   - System (Windows, Mac, Linux)
   - Logs from the server

---

## Tips & Best Practices

### Performance Tips
1. **Limit active bots:** Run 2-4 at a time, not 10
2. **Clear history:** Export old chats, then clear to free memory
3. **Refresh periodically:** Keeps application fresh and responsive

### Security Tips
1. **Don't share bot IDs** publicly (if using authentication)
2. **Keep credentials secure** (don't type in chat)
3. **Review chat history** before exporting (may contain sensitive info)

### Productivity Tips
1. **Use keyboard shortcuts** - Faster than mouse clicking
2. **Keep similar tasks together** - One bot for coding, one for analysis
3. **Export important results** - Don't rely on history alone

---

**Need more help?** Check the Troubleshooting section or contact support.

**Last Updated:** 2025-10-25
**Version:** 1.0
