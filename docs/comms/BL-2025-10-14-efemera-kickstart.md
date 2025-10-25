# Comms Brief — Efemera Social Edge Graft Kickstart (2025‑10‑14)

Purpose
- Restart logging, run identity dev service, validate signed activity flow, generate the timeline one‑pager, and capture links for context (including this session’s DEIA log).

Context & Links
- Repot index: docs/REPOT.md
- RSE standard: docs/observability/RSE-0.1.md
- System architecture: docs/efemera/EFEMERA-SYSTEM-ARCHITECTURE-v0.1.md
- Social Edge Graft egg: docs/projects/Efemera-Social-Edge-Graft-Outer-Egg-v0.1.md
- Build Spec v2.0: docs/specs/Efemera-Build-Spec-v2.0.md
- Minutes one‑pager: docs/obsidian/notes/one-pager.md
- DEIA session (this chat’s context): .deia/sessions/20251014-165703690465-conversation.md

Plan (restart + test)
1) Start Minutes Bot (looped)
   - python -m deia.cli minutes start --topic "social-edge-graft" --interval 60 --loop
   - (optional) One‑off tick/write/stop: minutes start → minutes write "Kickoff" → minutes tick → minutes stop

2) Identity Dev Service (FastAPI)
   - pip install fastapi uvicorn pydantic
   - run_identity_dev.bat
   - Health: curl http://localhost:8088/v1/health

3) Bind → Sign → Post (dev‑mode)
   - Bind:
     - curl -X POST http://localhost:8088/v1/identity/bind -H "Content-Type: application/json" -d "{\"actorId\":\"edge-001\",\"role\":\"Edge\"}"
     - Capture devToken and keyId from response
   - Prepare payload (example):
     - actorId=edge-001, role=Edge, type=note, payload={"msg":"hello efemera"}
   - Sign (HMAC with devToken): canonicalize JSON {actorId,role,type,payload}, hex(hmac_sha256(token, canonical_json))
     - Use a short Python one‑liner or your preferred tool
   - Post signed activity:
     - curl -X POST http://localhost:8088/v1/activity/signed -H "Content-Type: application/json" -d "{… fields above …, \"signature\":\"<hex>\" }"
   - Expected:
     - HTTP 200 {"ok":true}
     - RSE events appended: identity_bind, activity_post at .deia/telemetry/rse.jsonl

4) Generate One‑Pager (Obsidian)
   - PYTHONPATH=src python -m tools.rse_to_obsidian
   - Open docs/obsidian/notes/one-pager.md

5) Tag Audit (optional)
   - PYTHONPATH=src python -m tools.tags_audit
   - Open docs/tags/TAGS-INDEX.md

Outcomes
- Minutes: minute_start/minute_tick/minute_stop events in RSE; .deia/minutes/* created
- Identity: dev bind + signed activity recorded; RSE shows identity_bind + activity_post
- One‑pager: updated swimlanes for quick review

Next (immediate)
- Add /v1/rsm/send (dev echo) and emit rsm_packet_send/recv
- Add graph/survey endpoints and RSE events (graph_follow/survey_submit)
- Draft QR schema spec and stubs for /v1/qr/issue|verify

Owner & Review
- Owner: Efemera build lead
- Reviewers: Dave (5‑pip), Governance/Commons maintainers
