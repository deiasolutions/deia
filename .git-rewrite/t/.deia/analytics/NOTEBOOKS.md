# DEIA Analytics Notebooks

This directory includes ready‑to‑run Jupyter notebooks for exploring DEIA analytics data produced by the local ETL.

## Notebooks
- `DEIA_Analytics_Explorer_Plotly.ipynb`
  - Plotly + pandas exploration (no matplotlib). Loads NDJSON tables and shows basic charts.
- `DEIA_Analytics_Explorer_Plotly_v2.ipynb`
  - Enhanced version with:
    - Environment check cell (print interpreter and install into THIS kernel)
    - Pareto helper with cumulative % overlay (events by type, tasks by subject)
    - Events per day (by event timestamp)
    - Sessions per day (by ts_start) and most recent ts_ingested
    - Heartbeats last‑seen per bot (bar)
    - TASK→RESPONSE lead‑time histogram (heuristic by subject)

## Before You Start
1) Run the ETL once so staging data exists:
   - CLI: `deia analytics autorun`
   - Or: `python -c "import sys; sys.path.insert(0,'src'); from deia.cli import main; main(['analytics','autorun'])"`
2) (Optional) Enable autorun on session launch:
   - Edit `.deia/analytics/config.json` → set `"autorun_on_launch": true`

## Importing the `deia` Package in Notebooks
Use the bootstrap helper to add `<project_root>/src` to `sys.path` for the current kernel.

In the first cell of your notebook:
```
%run .deia/analytics/notebook_bootstrap.py
configure_deia()       # adds <project_root>/src to sys.path
show_env()             # prints interpreter details
# ensure_packages(['pandas','plotly'])  # optional in‑kernel install
from deia.services.telemetry_etl import autorun
```

## Troubleshooting
- If charts don’t render, ensure `plotly` and `pandas` are available in THIS kernel:
  - Use `ensure_packages(['pandas','plotly'])` from the bootstrap helper.
- If tables are empty, re‑run the ETL and check `.deia/analytics/manifest.json` for written outputs.
- The v2 notebook prints the most recent `ts_ingested` for sessions to help validate freshness.

## Next Steps
- Add Parquet targets in `.deia/analytics/config.json` once `pyarrow` is available: `"targets": ["staging_ndjson","parquet"]`.
- Optionally use DuckDB (installed separately) to query Parquet via `.deia/analytics/warehouse/deia.duckdb`.
