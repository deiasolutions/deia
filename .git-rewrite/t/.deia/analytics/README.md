# DEIA Analytics (Local ETL) — Quick Guide

This folder contains a local‑first, file‑based analytics pipeline for DEIA logs. It normalizes session markdown, activity JSONL, and heartbeat YAML into analyzable datasets.

What This Produces
- Staging NDJSON (append‑only, date‑partitioned)
  - `.deia/analytics/staging/<table>/dt=YYYY-MM-DD/*.ndjson`
- Warehouse (future phases)
  - Parquet files under `.deia/analytics/warehouse/<table>/...`
  - Optional DuckDB catalog at `.deia/analytics/warehouse/deia.duckdb` (views over Parquet)
- Manifest
  - `.deia/analytics/manifest.json` (per‑run outputs, counts, schema version)

Tables (Phase 1)
- `sessions`: one row per conversation log
- `session_decisions`: bullets under “Key Decisions Made”
- `session_action_items`: bullets under “Action Items”
- `session_files_modified`: bullets under “Files Modified” (repo‑relative flag)
- `events`: rows from `.deia/bot-logs/*.jsonl` (normalized timestamp/type)
- `heartbeats`: rows from `.deia/hive/heartbeats/*.yaml` (timestamp, bot, status, message)

Additional Tables (Phase 2 additions in this repo)
- `hive_tasks`: parsed from `.deia/hive/tasks/*.md` (filename fields: ts, from, to, type, subject, path)
- `hive_responses`: parsed from `.deia/hive/responses/*.md` (same fields as tasks)
- `agents`: derived from events/heartbeats (bot_id, first_seen, last_seen, active)

Sources
- Session logs (Markdown): `.deia/sessions/*.md`
- Bot activity (JSONL): `.deia/bot-logs/*.jsonl`
- Heartbeats (YAML): `.deia/hive/heartbeats/*.yaml`

How To Run (Phase 1)
- Using DEIA CLI (preferred):
  - `deia analytics autorun`
- Or via Python directly (from repo root):
  - `python -c "import sys; sys.path.insert(0,'src'); from deia.cli import main; main(['analytics','autorun'])"`

Autorun Option
- Enable autorun on session launch (e.g., when starting minutes):
  - Edit `.deia/analytics/config.json` → set `"autorun_on_launch": true`
  - Then run: `deia minutes start --topic <name>`

Safety & Refreshing
- Append‑only: each run writes new files under the day’s partition. Safe to refresh regularly.
- Raw sources are never modified.
- Storage growth is linear; we can add compaction/Parquet export in Phase 2.

Config
- File: `.deia/analytics/config.json`
  - `targets`: ["staging_ndjson"] (Phase 1)
  - `transcript_inline`: false (store only transcript file path)
  - `redactions`: [] (regex patterns; reserved)
  - `autorun_on_launch`: false|true
  - `since`: null (reserved for incremental loads)

Schemas (Overview)
- Phase 1 validates shape informally; formal JSON Schemas land in Phase 2 under `.deia/analytics/schemas/`.
- Common fields:
  - `ts` (ISO8601), `bot_id` (string), `event_type` (string), `message` (text), `raw` (original JSON/YAML map)
  - `session_id` (from session filename), `status` (session status), `transcript_path` (path)

 DuckDB (Optional)
 - If `duckdb` is installed, a catalog file `.deia/analytics/warehouse/deia.duckdb` is created with views over Parquet partitions.
 - Parquet writers will be added when `pyarrow` is available; until then, views are placeholders.

Manifest
- `.deia/analytics/manifest.json` keeps a list of runs with:
  - `run_id`, `dt`, `written` (table → file path), `schema_version`, `targets`

Planned Phase 2
- Write Parquet alongside NDJSON
- Create DuckDB views automatically over Parquet
- Add `agents` table (derived from events/heartbeats)
- JSON Schemas + validation + error logs
- Incremental `--since` loads, compaction utilities

Privacy
- By default, transcript content is not inlined (path only). Paths outside the repo can be hashed in Phase 2 redaction hooks.

Troubleshooting
- If no outputs appear, verify sources exist:
  - `.deia/sessions/*.md`, `.deia/bot-logs/*.jsonl`, `.deia/hive/heartbeats/*.yaml`
- Re‑run `deia analytics autorun` and check `manifest.json` for the run entry.

Maintainer Notes
- ETL code: `src/deia/services/telemetry_etl.py`
- CLI entry: `deia analytics autorun` (see `src/deia/cli.py`)

Notebook Bootstrap
- Helper: `.deia/analytics/notebook_bootstrap.py`
- Usage in a Jupyter cell:
  - `%run .deia/analytics/notebook_bootstrap.py`
  - `configure_deia()`  # adds `<project_root>/src` to `sys.path`
  - `show_env()`        # prints interpreter details
  - `# ensure_packages(['pandas','plotly'])`  # optional install into current kernel
  - `from deia.services.telemetry_etl import autorun`

Notebooks
- See `.deia/analytics/NOTEBOOKS.md` for available notebooks:
  - `DEIA_Analytics_Explorer_Plotly.ipynb`
  - `DEIA_Analytics_Explorer_Plotly_v2.ipynb` (recommended)
