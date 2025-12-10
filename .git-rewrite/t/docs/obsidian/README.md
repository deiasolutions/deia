# Obsidian Compatibility (Efemera)

Open this repository as an Obsidian vault (or add `docs/` and `.deia/` as folders in your vault).

What works now:
- Minutes: `.deia/minutes/*.md` — minute-by-minute logs
- One-pager: `docs/obsidian/notes/one-pager.md` — generated from RSE telemetry
- Graph view: tags like `#note`, `#ask`, `#todo` are discoverable; add wikilinks `[[...]]` to strengthen graphs

Generate one-pager:
- `PYTHONPATH=src python -m tools.rse_to_obsidian`

Tips:
- Enable “Markdown links” in Obsidian settings for robust cross-file links
- Consider Dataview and Mermaid plugins for richer visualizations

