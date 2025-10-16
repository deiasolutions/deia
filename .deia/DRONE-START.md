# DRONE START (Read First)

Single-file boot guide for any new drone (Claude, Codex, or other).

## 1) Join the Hive as a Drone

Pick a bot ID listed in `.deia/hive-recipe.json` (e.g., `BOT-00002` or `BOT-00003`).

Windows/POSIX (via Python import to ensure `src` on sys.path):

```
python -c "import sys; sys.path.insert(0,'src'); from deia.cli import main; main(['hive','join','.deia/hive-recipe.json','--role','BOT-00002'])"
```

Notes
- The output shows your `Instance ID` and the path to your instruction file.
- If a bot is already claimed, try a different bot ID.

## 2) Update Your Instruction File

Open the file shown in the join output, e.g. `.deia/instructions/BOT-00002-instructions.md`.
Under the `CLAIMED BY` section, fill in your instance and set ACTIVE:

```
## CLAIMED BY
**Instance ID:** <your-instance-id>
**Claimed at:** <YYYY-MM-DD HH:MM:SS>
**Last check-in:** <YYYY-MM-DD HH:MM:SS>
**Status:** ACTIVE
```

## 3) Send Initial Heartbeat

Use the helper scripts to append a heartbeat line to your instruction file:

- Windows PowerShell:
  ```
  .\\.deia\\tools\\heartbeat.ps1 -BotId BOT-00002 -Message "Ready"
  ```
- POSIX shells:
  ```
  bash ./.deia/tools/heartbeat.sh BOT-00002 "Ready"
  ```

Heartbeat format (LLM‑agnostic):

```
- 2025-10-13T10:32:00 [BOT-00002] Ready
```

## 4) Follow Your Current Task

In your instruction file, go to `## Current Task`.
- If it is `OPEN`, keep sending periodic heartbeats with a short status (e.g., "Standing by").
- If a task is assigned, execute and report progress with heartbeats.

## 5) Handoff When Done

Create a handoff doc and link it in your instruction file:

- Path: `.deia/handoffs/<task-slug>.md`
- Include: Work Done, Files Modified, Decisions, Next Steps.

## Optional: Conversation Logging

Save your chat transcript for continuity:

```
deia log --from-file <transcript.txt>
```

Logs are saved under `.deia/sessions/`.

## Troubleshooting

- Ensure Python can import the CLI: `python -c "import sys; sys.path.insert(0,'src'); from deia.cli import main; main(['--help'])"`
- If `.deia/hive-recipe.json` was created on Windows, ensure it’s UTF‑8 without BOM to avoid JSON errors.
- If join reports already claimed, pick another bot ID listed in `.deia/hive-recipe.json`.

