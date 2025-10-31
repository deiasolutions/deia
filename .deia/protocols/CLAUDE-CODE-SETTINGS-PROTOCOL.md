# CLAUDE CODE SETTINGS PROTOCOL

**Version:** 1.0
**Created:** 2025-10-31
**Authority:** Q33N (BEE-000)
**Status:** RECOMMENDED PRACTICE for All Hives

---

## Purpose

Establish standardized Claude Code permission settings (`settings.local.json`) for DEIA hives to enable bot instances to work autonomously on routine file operations while maintaining safety guardrails on destructive commands.

---

## Problem Statement

### The Friction Problem
When Claude Code instances (bots) are required to get user approval for every file operation, it creates:
- **Workflow friction** - Constant approval prompts for normal work
- **Context loss** - Interrupts task flow and cognitive load
- **Coordination overhead** - Q33N must respond to every "may I write this file?" request
- **Velocity impact** - Multiple approval prompts add 5-10 seconds per file operation

### The Safety Problem
Giving blanket approval for all operations creates risk:
- **Destructive commands** could run without oversight (rm, git reset --hard)
- **Unusual operations** might bypass review (force push, deleting tracked files)
- **Accidental harm** to working systems

### The Solution
**Tiered permission model:** Auto-approve routine operations, ask for approval on unusual/dangerous ones.

---

## Architecture

### Three Permission Levels

```json
{
  "permissions": {
    "allow": [],      // ✅ Auto-approved (no prompt)
    "ask": [],        // ❓ Requires user approval
    "deny": []        // ❌ Blocked (no execution)
  }
}
```

---

## Configuration (Recommended)

### File Location

- **Project-level:** `.claude/settings.local.json` (checked into repo)
- **User-level:** `~/.claude/settings.json` (global, not in repo)
- **Precedence:** Project settings override user settings

### Recommended Allow List

**File Operations (Auto-Approve):**
```json
"allow": [
  "Write(**/*.md)",           // Markdown documentation
  "Write(**/*.json)",         // JSON configs
  "Write(**/*.ts)",           // TypeScript
  "Write(**/*.tsx)",          // React components
  "Write(**/*.py)",           // Python
  "Write(**/*.yaml)",         // YAML configs
  "Write(**/*.yml)",          // YAML configs
  "Edit(**/*)"                // Edit any file
]
```

**Git Operations (Safe):**
```json
"allow": [
  "Bash(git add:*)",          // Stage changes
  "Bash(git commit:*)",       // Commit changes
  "Bash(git push)",           // Push to remote (non-forced)
  "Bash(git pull:*)",         // Pull changes
  "Bash(git checkout:*)"      // Switch branches
]
```

**Development Commands (Safe):**
```json
"allow": [
  "Bash(python:*)",           // Python execution
  "Bash(pip install:*)",      // Install dependencies
  "Bash(npm:*)",              // Node package manager
  "Bash(npm run build:*)",    // Build commands
  "Bash(pytest:*)",           // Python tests
  "Bash(find:*)",             // File searching
  "Bash(grep:*)",             // Content searching
  "Bash(cat:*)",              // Read files
  "Bash(ls:*)"                // List files
]
```

**Utilities (Safe):**
```json
"allow": [
  "Bash(timeout:*)",          // Timeout wrapper
  "Bash(curl:*)",             // HTTP requests
  "Bash(chmod:*)",            // File permissions
  "Bash(bash:*)",             // Bash scripts
  "Read(//path/to/**)",       // Read files
  "WebSearch",                // Web search
  "WebFetch"                  // Fetch web content
]
```

### Recommended Deny List

**Destructive Operations (Always Blocked):**
```json
"deny": [
  "Bash(rm:*)",               // Delete files (no recovery)
  "Bash(rm -rf:*)",           // Recursive delete
  "Bash(git reset --hard:*)", // Destructive git reset
  "Bash(git rebase:*)",       // Complex git rewriting
  "Bash(git clean:*)"         // Clean untracked files
]
```

**Rationale:** These commands have no safe default and can destroy working systems.

### Recommended Ask List

**Dangerous But Sometimes Legitimate (Requires Approval):**
```json
"ask": [
  "Bash(git push --force:*)", // Force push (rewrites history)
  "Bash(git push -f:*)",      // Force push (alt syntax)
  "Bash(git rm:*)"            // Remove tracked files
]
```

**Rationale:** These are sometimes needed but represent a breaking change. User should explicitly approve.

---

## Implementation Guide

### Step 1: Create Project-Level Settings

Create `.claude/settings.local.json` in your hive root:

```json
{
  "permissions": {
    "allow": [
      "Write(**/*.md)",
      "Write(**/*.json)",
      "Write(**/*.py)",
      "Write(**/*.yaml)",
      "Edit(**/*)",
      "Bash(python:*)",
      "Bash(pip install:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push)",
      "Bash(git pull:*)",
      "Bash(git checkout:*)",
      "Bash(npm:*)",
      "Bash(pytest:*)",
      "Bash(find:*)",
      "Bash(grep:*)",
      "Bash(cat:*)",
      "Bash(ls:*)",
      "Bash(timeout:*)",
      "Bash(curl:*)",
      "Bash(chmod:*)",
      "Bash(bash:*)",
      "Read(//c/Users/**)",
      "WebSearch",
      "WebFetch"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(rm -rf:*)",
      "Bash(git reset --hard:*)",
      "Bash(git rebase:*)",
      "Bash(git clean:*)"
    ],
    "ask": [
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(git rm:*)"
    ]
  }
}
```

### Step 2: Check Into Repository

```bash
git add .claude/settings.local.json
git commit -m "config: auto-approve normal file operations in Claude Code"
git push
```

**Why check in?** All team members and bot instances get consistent permissions.

### Step 3: Document in Project README

Add to your project README:

```markdown
## Claude Code Configuration

This project uses `.claude/settings.local.json` to auto-approve routine file operations for bot instances while maintaining safety guardrails on destructive commands.

**Auto-approved operations:**
- File writes (markdown, code, configs)
- Git: add, commit, push, pull, checkout
- Development: python, npm, pytest, etc.

**Blocked operations:**
- File deletion (rm, rm -rf)
- Destructive git (reset --hard, rebase, clean)

**Approval required:**
- Force push (git push --force)
- Removing tracked files (git rm)

See `.claude/settings.local.json` for full details.
```

---

## Usage Patterns

### For Individual Contributors

When working in a DEIA hive:
1. Check if `.claude/settings.local.json` exists
2. Read it to understand what's auto-approved
3. Claude Code handles approvals automatically for routine work
4. You only see approval prompts for unusual operations

### For Bot Instances

When launching a bot in a hive:
1. Bot reads `.claude/settings.local.json` from project root
2. Routine operations (file writes, git add/commit) execute automatically
3. Dangerous operations are blocked or ask for approval
4. Bot maintains full autonomy on permitted operations
5. No workflow interruptions for normal file saves

### For Q33N Authority

When supervising bot operations:
1. Monitor `.deia/bot-logs/` for bot activity
2. Review completion reports and heartbeats
3. Trust that bots only perform permitted operations
4. Intervene only on operations requiring approval ("ask" list)

---

## Security Considerations

### Principle: Defense in Depth

```
User Intent
    ↓
Claude Code Settings (first layer: what's allowed)
    ↓
Git Protection (second layer: can't push without commits)
    ↓
Code Review (third layer: PRs require review before merge)
    ↓
Production Deployment (fourth layer: separate approval)
```

### What's Protected

| Layer | Protection | Example |
|-------|-----------|---------|
| **Settings** | Destructive commands blocked | `rm` cannot run |
| **Git** | History protected by git | `git reset --hard` blocked |
| **Review** | Code changes visible | PRs show all changes |
| **Deploy** | Production separate | Prod deployment requires manual approval |

### What's NOT Protected (By Design)

These operations are auto-approved and NOT tracked by Claude Code:
- Committing breaking changes (code review catches this)
- Pushing buggy code (tests should catch this)
- Creating commits with poor messages (style guides catch this)

**Assumption:** Bots follow DEIA standards and processes. Governance comes from:
- Auto-logging every 15-30 minutes (audit trail)
- Heartbeat reports every 30 minutes (status visibility)
- Code review before merge (quality gate)
- Q33N oversight (governance authority)

---

## Anti-Patterns to Avoid

### ❌ DO NOT: Allow wildcard Bash operations
```json
// WRONG - Too permissive
"allow": ["Bash(*)"]
```

**Why:** Enables any shell command, including destructive ones.

### ❌ DO NOT: Deny file writes
```json
// WRONG - Blocks legitimate work
"deny": ["Write(**/*)", "Edit(**/*)", "Write(**/*.md)"]
```

**Why:** Defeats the purpose of auto-approval for routine work.

### ❌ DO NOT: Ask on every file operation
```json
// WRONG - Creates constant friction
"ask": ["Write(**/*)", "Edit(**/*)", "Bash(git add:*)"]
```

**Why:** Enables friction problem this protocol solves.

### ✅ DO: Use targeted allow rules
```json
// CORRECT - Specific and safe
"allow": [
  "Write(**/*.md)",
  "Write(**/*.json)",
  "Write(**/*.py)",
  "Edit(**/*)"
]
```

### ✅ DO: Maintain a deny list for destructive operations
```json
// CORRECT - Protects against accidents
"deny": [
  "Bash(rm:*)",
  "Bash(rm -rf:*)",
  "Bash(git reset --hard:*)"
]
```

---

## Troubleshooting

### Problem: Bot is getting approval prompts constantly

**Diagnosis:**
- Check `.claude/settings.local.json` exists in project root
- Verify bot has read access to the file
- Confirm operation is in the "allow" list

**Solution:**
1. Verify file is committed to git (`git log .claude/settings.local.json`)
2. Check operation matches a pattern in "allow" list
3. If pattern is missing, add it to "allow" list and commit
4. Restart bot instance to pick up new settings

### Problem: Bot is performing operations that should be blocked

**Diagnosis:**
- Operation is in "deny" list but still executed
- Settings not being read or outdated

**Solution:**
1. Verify bot is using correct settings file
2. Check settings file for syntax errors (`json` validation)
3. Ensure "deny" rule matches the command pattern exactly
4. Test manually: Try running operation, expect rejection
5. Escalate to Q33N if still not blocked

### Problem: Need to add new operations to allow list

**Process:**
1. Request operation addition in Q33N coordination message
2. Q33N reviews security implications
3. Q33N approves and updates settings file
4. Change is committed to git
5. All instances pick up new settings on next session

---

## Precedence & Override Rules

### Permission Hierarchy

```
DENY (highest priority - always blocks)
    ↓
ASK (requires user approval)
    ↓
ALLOW (auto-approved, lowest priority)
```

**Rule:** If operation matches multiple lists, most restrictive wins.

Example:
```json
{
  "allow": ["Bash(git:*)"],         // Allow all git
  "deny": ["Bash(git reset:*)"]     // But block reset
}
// Result: git reset is BLOCKED (deny takes precedence)
```

### File-Level Precedence

If multiple `.claude/settings.json` files exist:

1. `.claude/settings.local.json` (project-specific, highest priority)
2. `.claude/settings.json` (project-shared)
3. `~/.claude/settings.json` (user-global)

**Recommendation:** Use project-level (local.json) for team consistency.

---

## Recommended Process for Hives

### When Starting a New Hive

1. **Create** `.claude/settings.local.json` with recommended configuration (see Implementation Guide)
2. **Commit** to git with explanatory message
3. **Document** in project README (see Usage Patterns)
4. **Notify** all team members of the configuration
5. **Include** in onboarding guides for bot instances

### When Adding New Bot Type

1. **Test** operations locally with Claude Code
2. **Note** which operations are needed
3. **Update** `.claude/settings.local.json` to permit them
4. **Update** deny/ask lists if new dangerous patterns emerge
5. **Commit** and notify team

### When Incident Occurs (Destructive Operation)

1. **Review** what operation ran (check logs)
2. **Analyze** why it wasn't blocked (settings failure? Wrong rule?)
3. **Update** settings to prevent recurrence
4. **Commit** fix
5. **Notify** Q33N with incident report

---

## Examples

### Example 1: Python Development Hive

```json
{
  "allow": [
    "Write(**/*.py)",
    "Write(**/*.md)",
    "Write(**/*.json)",
    "Edit(**/*)",
    "Bash(python:*)",
    "Bash(pip install:*)",
    "Bash(pytest:*)",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git push)",
    "Bash(git pull:*)",
    "Bash(find:*)",
    "Bash(grep:*)"
  ],
  "deny": [
    "Bash(rm:*)",
    "Bash(rm -rf:*)",
    "Bash(git reset --hard:*)"
  ],
  "ask": [
    "Bash(git push --force:*)",
    "Bash(git rm:*)"
  ]
}
```

### Example 2: TypeScript/React Development Hive

```json
{
  "allow": [
    "Write(**/*.ts)",
    "Write(**/*.tsx)",
    "Write(**/*.md)",
    "Write(**/*.json)",
    "Edit(**/*)",
    "Bash(npm:*)",
    "Bash(npm run build:*)",
    "Bash(npm run test:*)",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git push)",
    "Bash(git pull:*)",
    "Bash(find:*)",
    "Bash(grep:*)"
  ],
  "deny": [
    "Bash(rm:*)",
    "Bash(rm -rf:*)",
    "Bash(git reset --hard:*)"
  ],
  "ask": [
    "Bash(git push --force:*)",
    "Bash(git rm:*)"
  ]
}
```

### Example 3: Mixed Language Hive (DEIA Core)

```json
{
  "allow": [
    "Write(**/*.md)",
    "Write(**/*.json)",
    "Write(**/*.py)",
    "Write(**/*.ts)",
    "Write(**/*.yaml)",
    "Write(**/*.yml)",
    "Edit(**/*)",
    "Bash(python:*)",
    "Bash(pip install:*)",
    "Bash(pytest:*)",
    "Bash(npm:*)",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git push)",
    "Bash(git pull:*)",
    "Bash(git tag:*)",
    "Bash(git checkout:*)",
    "Bash(find:*)",
    "Bash(grep:*)",
    "Bash(timeout:*)",
    "Bash(curl:*)"
  ],
  "deny": [
    "Bash(rm:*)",
    "Bash(rm -rf:*)",
    "Bash(git reset --hard:*)",
    "Bash(git rebase:*)",
    "Bash(git clean:*)"
  ],
  "ask": [
    "Bash(git push --force:*)",
    "Bash(git push -f:*)",
    "Bash(git rm:*)"
  ]
}
```

---

## Related Protocols

- **BEE-000-Q33N-BOOT-PROTOCOL.md** - Q33N authority and bot roles
- **AGENT-COMMUNICATION-CADENCE-v1.0.md** - How bots report and coordinate
- **PROTOCOL-agent-instruction-consistency.md** - How to handle instruction conflicts

---

## Future Enhancements

### Possible Additions

1. **Hooks for conditional approval** - Run custom script before operation (see Claude Code docs)
2. **Bot-specific permissions** - Different settings for different bot tiers
3. **Time-based permissions** - Different rules during business hours vs. off-hours
4. **Audit hooks** - Log all operations to centralized audit trail
5. **Integration with monitoring** - Alert on operations outside normal patterns

### Not Recommended (Too Complex)

- Per-command cost limits (not supported by Claude Code)
- Machine learning-based anomaly detection (overkill for current scale)
- Multi-tier approval workflows (handled by git review instead)

---

## FAQ

**Q: What if a bot needs to do something that's blocked?**
A: Update the settings file in the "allow" list, commit to git, and inform Q33N. Bot will pick up new settings on next session.

**Q: Why not just allow everything?**
A: Destructive commands like `rm -rf` and `git reset --hard` can destroy working systems with no recovery. The deny list prevents accidental harm.

**Q: Why require approval for force push?**
A: Force push rewrites history and can break team collaboration. It should be intentional and visible, not automatic.

**Q: Can I use different settings for different bots?**
A: Not natively with Claude Code settings. Use bot-level logic or environment variables if needed, escalate to Q33N for guidance.

**Q: How do I test if settings are working?**
A: Try running an operation and observe:
- **Allow list:** Operation completes without prompt
- **Deny list:** Operation fails/is blocked
- **Ask list:** Operation prompts for approval

**Q: Should I commit settings.local.json to git?**
A: Yes. This ensures:
- All team members have consistent permissions
- All bot instances get the same rules
- Changes are tracked in git history
- New developers automatically get correct settings

---

## Maintenance

**Last Updated:** 2025-10-31
**Maintained By:** Q33N (BEE-000)
**Review Cycle:** Quarterly (or when new patterns emerge)
**Next Review:** 2026-01-31

### Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2025-10-31 | Created protocol based on FBB and DEIA implementation | Q33N |

---

## Approval

**✅ APPROVED for DEIA-wide adoption**

Status: RECOMMENDED PRACTICE
- All new hives should use this configuration
- Existing hives should migrate within 30 days
- Q33N will enforce during oversight cycles

**Endorsement:** This protocol has been successfully tested on:
- familybondbot (FBB) - TypeScript/React development
- deiasolutions - Multi-language Python/bot coordination

---

**End of Protocol**
