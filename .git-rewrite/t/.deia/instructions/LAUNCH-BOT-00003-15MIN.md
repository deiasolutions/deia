## Drone Launch Script (15 min) — BOT-00003

Follow exactly. Timebox to 15 minutes, then standby.

### 0) Timebox
- Start now. Stop at T+15m.
- At T+10m: send heartbeat “5m remaining”.
- At T+15m: send heartbeat “Standby; awaiting assignment”, then exit.

### 1) Join the Hive as BOT-00003
Run from the repo root directory.

Windows/POSIX (Python import ensures CLI is on path):
```
python -c "import sys; sys.path.insert(0,'src'); from deia.cli import main; main(['hive','join','.deia/hive-recipe.json','--role','BOT-00003'])"
```
Note the printed `Instance ID` and instruction file path.

### 2) Update CLAIMED BY in your instruction file
Edit: `.deia/instructions/BOT-00003-instructions.md`
Replace the CLAIMED BY block with:
```
## CLAIMED BY
**Instance ID:** <paste from join output>
**Claimed at:** <current local time>
**Last check-in:** <current local time>
**Status:** ACTIVE
```

### 3) Send Ready heartbeat
- PowerShell:
```
.\\.deia\\tools\\heartbeat.ps1 -BotId BOT-00003 -Message "Ready"
```
- POSIX:
```
bash ./.deia/tools/heartbeat.sh BOT-00003 "Ready"
```

### 4) Log telemetry (session_start)
- PowerShell:
```
.\\.deia\\tools\\telemetry.ps1 -AgentId BOT-00003 -Role drone -Event session_start -Message "Joined and ready" -DurationMs 0
```
- POSIX:
```
bash ./.deia/tools/telemetry.sh BOT-00003 drone session_start "Joined and ready" 0 0 0
```

### 5) Standby and heartbeat during timebox
- Every ~3–5 minutes, append a short heartbeat, e.g.:
```
.\\.deia\\tools\\heartbeat.ps1 -BotId BOT-00003 -Message "Standing by"
```
- At T+10m:
```
.\\.deia\\tools\\heartbeat.ps1 -BotId BOT-00003 -Message "5m remaining"
```

### 6) Closeout at T+15m
- Send final heartbeat and telemetry end:
```
.\\.deia\\tools\\heartbeat.ps1 -BotId BOT-00003 -Message "Standby; awaiting assignment"
.\\.deia\\tools\\telemetry.ps1 -AgentId BOT-00003 -Role drone -Event session_end -Message "Timebox end" -DurationMs 900000
```
- Leave the terminal open, no further action until assigned.

### Rules
- Do not modify source files or CLI.
- All writes limited to `.deia/`.
- If join fails due to claim, do nothing further and report via heartbeat with message "Join failed; identity claimed".
