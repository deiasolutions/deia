# Handoff: Flight‑2 — CLI/UX Alignment to Season/Flight (Proposed Patches)

Summary
Align user‑visible CLI/help/status strings with Season/Flight vocabulary. These are text‑only changes; no functional code paths are modified. Apply after Flight‑1 docs are accepted to keep terminology consistent.

Files Impacted
- `src/deia/cli.py` — add brief Seasons/Flights mention in top‑level help text
- `src/deia/cli_hive.py` — clarify group help to include Seasons/Flights
- `src/deia/services/messaging.py` — update docstring label from Sprint to Season/Flight

Proposed Diffs (do not apply yet)

---

File: src/deia/cli.py

```diff
@@
-    DEIA - Development Evidence & Insights Automation
-
-    Learn from every AI-assisted development session. Build better with AI.
+    DEIA - Development Evidence & Insights Automation
+
+    Learn from every AI-assisted development session. Build better with AI.
+    Planning cadence uses Seasons (macro) and Flights (execution bursts).
     """
     pass
```

---

File: src/deia/cli_hive.py

```diff
@@
-@cli.group('hive')
-def hive():
-    """Manage DEIA agent coordination"""
+@cli.group('hive')
+def hive():
+    """Manage DEIA agent coordination (Seasons/Flights)"""
     pass
```

Optionally, extend specific help strings later if needed; current subcommands are terminology-neutral.

---

File: src/deia/services/messaging.py

```diff
@@
-Author: Claude (CLAUDE-CODE-001)
-Sprint: Week 1 - Foundation
-Date: 2025-10-17
+Author: Claude (CLAUDE-CODE-001)
+Season: 1 — Flight 1: Foundations
+Date: 2025-10-17
 """
```

Acceptance Criteria
- `deia --help` and `deia hive --help` display Season/Flight terminology where appropriate.
- No logic changes; only string/docstring/help text updated.
- Messaging docstring reflects Season/Flight nomenclature.

Next Steps
- Upon Flight‑1 acceptance, I will apply these diffs and run a quick smoke of `deia --help` and `deia hive --help` to confirm output.

---
Agent ID: CLAUDE-CODE-001
LLH: DEIA Project Hive
Purpose: Strategic planning, orchestration, and agent coordination
