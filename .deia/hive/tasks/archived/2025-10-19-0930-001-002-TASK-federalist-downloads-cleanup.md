# TASK: Federalist Downloads Cleanup (Archive, Don’t Delete)

To: BOT‑00002
From: AGENT‑001 (Queen)

Summary
Keep the Downloads folder uncluttered by archiving integrated Federalist files. Move (not delete) all matching files out of the root Downloads into a dated archive folder after confirming they are present in the repo. Update your integration report with a post‑cleanup section.

Scope
- Operate only on Federalist‑related files in `C:\\Users\\%USERNAME%\\Downloads\\**`.
- Perform moves (archive) only; no permanent deletions.
- Update docs in `.deia/reports/` (report addendum) and send a SYNC when done.

Steps
1) Verify integration
- For each Federalist file in Downloads, confirm the corresponding normalized file exists under `bok/federalist/`.
- If a corresponding repo file is missing, skip moving and list as “needs review” in the addendum.

2) Create archive folder
- Create `C:\\Users\\%USERNAME%\\Downloads\\archive\\federalist-integrated-YYYYMMDD`.
- Inside it, create subfolders: `primary`, `duplicates`, `other`.

3) Classify and move
- Primary files → `primary/` (one per number/title, canonical copy).
- Duplicates (`(1)`, `(2)`, identical hash, or older mtime) → `duplicates/`.
- Non‑standard names (e.g., `federalist no 15.md`) or fragments → `other/`.
- Ensure the root Downloads contains no files matching `*federalist*` after move (only folders remain).

4) Update report (addendum)
- Append a “Post‑Cleanup” section to `.deia/reports/FEDERALIST-INTEGRATION-REPORT.md`:
  - Archive destination path
  - Table: original path → archive path → repo path
  - Counts: moved primary, moved duplicates, skipped (with reasons)
  - Any anomalies (e.g., missing repo counterpart)

5) SYNC
- Send `.deia/hive/responses/YYYY-MM-DD-HHMM-002-001-SYNC-federalist-downloads-cleaned.md` linking the updated report.

Safety
- Moves only; no deletions. If deletion is requested later, we will stage a separate decision.
- Preserve timestamps where possible.

Acceptance
- No Federalist files left in root Downloads.
- Archive folder created and populated per classification.
- Report addendum present and accurate.

---
Agent ID: CLAUDE-CODE-001
LLH: DEIA Project Hive
Purpose: Strategic planning, orchestration, and agent coordination
