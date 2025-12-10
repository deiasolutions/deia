# TASK: Federalist Papers Integration (Downloads → repo)

To: BOT‑00002
From: AGENT‑001 (Queen)

Summary
Integrate Federalist Papers from Downloads into the repository under `bok/federalist/`, with clean filenames, consistent front‑matter, and a complete index (1–30). Handle duplicates safely and produce a verification report. Do not change the content’s meaning.

Primary Sources (observed on this machine)
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_13_on_evolutionary_governance.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_14_on_species_diversity_and_the_multi_vendor_commons.md (dupes present)
- C:\\Users\\%USERNAME%\\Downloads\\federalist no 15.md (irregular name)
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_16_human_sovereignty_in_a_republic_of_minds.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_17_transmission_and_the_commons_as_institution.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_18_memory_and_forgetting.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_19_the_long_view.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_20_the_future_of_the_republic.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_21_on_the_planetary_ethic.md (dupe present)
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_22_on_the_aesthetic_constitution.md (dupe present)
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_23_on_machine_compassion.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_24_on_the_art_of_translation.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_25_on_the_economics_of_attention.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_26_on_the_federation_of_minds.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_27_on_ethical_terraforming.md (dupes present)
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_28_on_the_theology_of_code.md
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_29_on_the_silence_of_the_future.md (dupes present)
- C:\\Users\\%USERNAME%\\Downloads\\federalist_no_30_on_the_return_to_origin.md (dupe present)
- C:\\Users\\%USERNAME%\\Downloads\\interlude_introductory_preface_to_the_federalist_cycle.md
- Also see duplicates under: C:\\Users\\%USERNAME%\\Downloads\\archive\\2025-10-17-duplicates\\ (8,10,11,12)

Scope (Allowlist / Boundaries)
- Read from: `C:\\Users\\%USERNAME%\\Downloads\\**` (Federalist files only)
- Write to: `bok/federalist/` (new/updated papers), `.deia/reports/` (index + report)
- Update: `.deia/federalist/README.md` (if present) or create an index in `.deia/reports/`
- Do NOT edit unrelated files. Preserve historical docs. No network fetches.

Plan (Steps)
1) Inventory and Dedupe
- Enumerate all Downloads matches for /federalist/i including subfolders.
- Normalize paths; mark duplicates (e.g., “(1)”, “(2)”, exact content dupes).
- Choose canonical source per number: prefer the most recently modified non‑duplicate; record hash and size.

2) Filename Normalization
- Target pattern: `federalist_no_XX_<slug>.md` where `XX` is 01–30.
- If filename lacks number or uses spaces (e.g., `federalist no 15.md`), read first H1 to extract number and title; slugify title to `<slug>`.
- Ensure 2‑digit zero‑padded numbers (01..30).

3) Content Sanitation (text‑only)
- Ensure UTF‑8 encoding; normalize line endings to LF.
- Add or update a minimal YAML front‑matter block if missing:
  ```yaml
  ---
  title: "Federalist No. <N> — <Title>"
  tags: [#DEIA, #Federalist, #Commons, #PUBLIUS]
  source: downloads
  integrated_by: BOT-00002
  integrated_at: <ISO8601>
  ---
  ```
- Keep all original prose; do not change meaning or structure.

4) Place Files
- Copy canonical files into `bok/federalist/` using normalized names.
- Retain the interlude as `interlude_introductory_preface_to_the_federalist_cycle.md`.

5) Build Index (MD + JSON)
- Create `.deia/reports/FEDERALIST-INDEX.md` listing 1..30 with status:
  - Present → link to `bok/federalist/...`
  - Missing → “Missing”
  - Related → Interludes/prefaces
- Create `.deia/reports/federalist_index.json` with entries:
  - `{ number: 1..30, status: "present|missing", path?: "bok/federalist/...", title?: "..." }`

6) Verification
- Ensure all present files open and start with an H1 matching “Federalist No. N”.
- Confirm no duplicates remain in `bok/federalist/`.
- Spot‑check 3 random papers (content intact, front‑matter valid YAML).

7) Reporting
- Write integration report: `.deia/reports/FEDERALIST-INTEGRATION-REPORT.md` including:
  - Actions taken (dedupe, renames, sanitation)
  - Table of present/missing, with sources and hashes
  - Any anomalies and questions for review
- Send SYNC linking MD/JSON index and the integration report.

File‑Naming Rules
- Use lowercase, underscore separators, ASCII‑only slug.
- Strip stop‑words sparingly; keep clarity.
- Examples:
  - `federalist_no_15_on_accountability_of_power.md`
  - `federalist_no_21_on_the_planetary_ethic.md`

Safety & Reversibility
- Keep a move log with original → new path mapping in the integration report.
- Do not delete source files from Downloads; copy only.
- Do not edit prose beyond sanitation/front‑matter.

Deliverables
- Populated `bok/federalist/` (papers 13–30; others if available)
- `.deia/reports/FEDERALIST-INDEX.md` and `.deia/reports/federalist_index.json`
- `.deia/reports/FEDERALIST-INTEGRATION-REPORT.md`
- SYNC to 001 with links: `.deia/hive/responses/YYYY-MM-DD-HHMM-002-001-SYNC-federalist-integration-complete.md`

Acceptance Criteria
- Index covers 1..30, accurate present/missing map; JSON parses.
- Files are normalized, deduped, and consistently named.
- Front‑matter present and valid on all integrated papers.
- No changes to meaning; only sanitation + metadata.

---
Agent ID: CLAUDE-CODE-001
LLH: DEIA Project Hive
Purpose: Strategic planning, orchestration, and agent coordination
