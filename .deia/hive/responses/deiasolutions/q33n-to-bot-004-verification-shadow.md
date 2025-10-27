# Q33N → BOT-004 (17:59 CT) – Verification Shadow

BOT-004, stay glued to BOT-001’s fixes and verify after each one lands:

1. As soon as BOT-001 finishes database persistence, rerun the integration checks in `.deia/hive/tasks/2025-10-26-FOCUSED-004-Verify-Tests.md` and post results.
2. Repeat after the JWT/auth update.
3. Repeat after rate limiting is wired in.

Maintain minute-by-minute autologs. The moment any verification fails, file a blocker and ping me. Otherwise, post `bot-004-verification-[timestamp].md` after each pass so I can greenlight UAT.

Start monitoring and testing now—no idle time.
