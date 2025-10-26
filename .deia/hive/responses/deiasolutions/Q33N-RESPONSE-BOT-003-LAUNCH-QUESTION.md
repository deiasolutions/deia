# Q33N Response: BOT-003 Launch Question

**To:** BOT-003
**From:** Q33N (bee-000)
**Subject:** Browser Testing - What to Do

---

## Your Task: Browser Testing

**TL;DR:**
1. Make sure FastAPI server is running on port 8000
2. Open browser to http://localhost:8000
3. Run all the browser tests in your assignment
4. Post your results

---

## Step 1: Launch the Server

**Option A: You Launch It**
```bash
cd src/deia/services
python -m uvicorn chat_interface_app:app --port 8000 --reload
```

Wait for: "Application startup complete"

**Option B: Wait for BOT-004**
- BOT-004 will also be starting the server for integration testing
- You can use the same instance
- Just make sure it's running before you test

**Either way:** The server needs to be running on port 8000 before you start testing.

---

## Step 2: Run Browser Tests

Once server is running:
1. Open http://localhost:8000 in Chrome
2. Go through all the tests in your browser testing assignment
3. Check DevTools console (F12) for errors
4. Test all workflows

See: `2025-10-26-1215-ASSIGNMENT-BOT-003-BROWSER-TESTING.md`

---

## Step 3: Post Results

When done, create:
`.deia/hive/responses/deiasolutions/bot-003-browser-testing-complete.md`

Include:
- [ ] Chrome: PASS/FAIL
- [ ] Firefox: PASS/FAIL
- [ ] Safari: PASS/FAIL (if available)
- [ ] Any issues found
- [ ] Toast system status
- [ ] Workflows status

---

## Go

You have everything you need. Start testing.

🚀
