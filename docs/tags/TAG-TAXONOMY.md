# Efemera Tag Taxonomy (v0.1)

Use these inline tags consistently in Markdown docs and session logs:

- #todo — actionable work items
- #note — notable info, decisions, NB (Note Bee)
- #ask — open questions / need input
- #log — general event log, optionally refine with:
  - #log_idea — ideas worth exploring
  - #log_win — achievements
  - #log_blocker — blockers/impediments
  - #log_type — freeform classification when needed
- #tags / #tag_type — meta-tags to categorize other tags or sections

Tools:
- Run tag audit: `PYTHONPATH=src python -m tools.tags_audit` → writes `docs/tags/TAGS-INDEX.md`

