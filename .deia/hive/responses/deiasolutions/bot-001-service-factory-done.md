# BOT-001 – Service Factory & Task Endpoint Integration
**Date:** 2025-10-26 16:55 CDT  
**Status:** COMPLETE  
**Duration:** ~45 minutes

---

## Deliverables
1. **Service Factory module** – `src/deia/services/service_factory.py` now exports a `BotType` enum and `ServiceFactory` capable of instantiating Anthropic/OpenAI/Ollama services or CLI adapters (Claude Code, Codex) with env-driven config.
2. **Registry metadata support** – `ServiceRegistry.register` accepts a `metadata` dict so bot launches persist their `bot_type`; HTTP APIs can look up bot-capabilities later.
3. **Task endpoint routing** – `/api/bot/{bot_id}/task` now reads the stored `bot_type`, asks `ServiceFactory` for the right adapter/service, starts CLI sessions when needed, and returns consistent responses (including files modified for CLI bots).
4. **Unit tests** – `tests/unit/test_chat_api_endpoints.py` updated for metadata + CLI handling, and new suite `tests/unit/test_service_factory.py` covers API vs CLI instantiation, env-var errors, and helper methods. Registry interactions in tests now use an isolated tmp file fixture.

---

## Tests
```
python -m pytest tests/unit/test_chat_api_endpoints.py -v
python -m pytest tests/unit/test_service_factory.py -v
```
All tests passing (coverage warning only references legacy `src/deia/admin.py` parser issue).

---

## Notes / Follow-ups
- Bot metadata currently stores only `bot_type`; extendable for future capabilities if needed.
- ServiceFactory raises clear `ValueError` when API keys missing, so frontend will propagate actionable errors.
- CLI adapters still use dev defaults (`claude`, `codex` in PATH); set `CLAUDE_CLI_PATH` / `CODEX_CLI_PATH` env vars in prod.
- Registry persistence is now exercised in tests via dedicated fixture to avoid leakage.

---

**Ready for BOT‑003** (frontend integration) and BOT‑004 (E2E verification). Let me know when to assist further.
