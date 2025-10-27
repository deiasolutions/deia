# Q33N – Bot Launch Fix Notes (2025-10-26 19:47 CT)

**Root issue:** `/api/bot/launch` only registers metadata; it never spawns `run_single_bot.py`. Registry shows a port, but no process listens, so `/api/bot/{id}/task` hits a dead socket and the UI throws “Operation was aborted”.

**What needs to change:**
1. **Cross-platform process spawn**
   - After validation/registry, call a helper to `subprocess.Popen(["python", "run_single_bot.py", bot_id, "--adapter-type", bot_type], ...)`.
   - Pass `creationflags=subprocess.CREATE_NEW_PROCESS_GROUP` on Windows; use plain Popen on Unix/macOS.
   - Store the PID back into the registry entry so `/api/bot/stop/{id}` can kill it later.
2. **Failure handling**
   - Wrap spawn in try/except; if Popen fails, free the port and remove registry entry, then return a 500 with the stderr so the frontend stops spinning.
   - Optionally poll `/health` for a couple seconds to confirm the bot answers before reporting success.
3. **Stop support**
   - Ensure `stop_bot` uses the stored PID for Windows `os.kill(..., SIGABRT)`/`taskkill` and Unix `SIGTERM`.
4. **Verify with Claude Code**
   - Launch a Claude Code bot on Windows, confirm the Python runner starts and `/api/bot/{id}/task` returns the adapter’s response instead of the placeholder `[Offline] …`.

**Next steps:** Implement the spawn helper, update the endpoint, then re-run hive testing and UAT once Claude Code proves out.
