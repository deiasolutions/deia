---
title: "Case Study: Nuclear Option Without Complete Recovery Checklist"
date: 2025-10-16
severity: Critical
category: Process Failure / Deployment
contributed_by: DEIA Project
llm: Claude Sonnet 4.5
tags: [nuclear-option, incomplete-recovery, deployment, process-failure, case-study]
license: CC BY 4.0
---

# Case Study: Nuclear Option Without Complete Recovery Checklist

## Summary

After choosing "nuclear option" (delete and recreate) to resolve persistent configuration errors, LLM marked "reconfiguration" as complete without verification. Production remained broken for ~45 minutes before discovering build settings were never restored.

## What Happened

**Context:** Deploying static site to hosting platform with persistent configuration errors

**Initial Problem:**
- Configuration file had parsing errors
- Multiple attempts to fix failed
- User chose "nuclear option" - delete entire deployment and start fresh

**The Nuclear Option:**
1. Deleted entire hosting project
2. Created fresh project from source control
3. LLM added "Configure build settings" to todo list
4. **LLM marked it COMPLETED without verification**
5. Site appeared to deploy successfully (green checkmarks)
6. **But site showed 404 errors**

**The Discovery (45 minutes later):**
1. User tried multiple DNS and routing fixes (all wrong paths)
2. Finally checked deploy logs: "No build steps found"
3. Build command: BLANK
4. Publish directory: BLANK
5. **These were never reconfigured after nuclear option**

**Second Discovery (15 minutes later):**
1. Added build settings, triggered deploy
2. Deploy failed: "command not found" error
3. Environment variable also lost in nuclear option
4. **Another missing configuration item that should have been verified**

**Total downtime:** ~60+ minutes of broken production

## Root Cause

**Immediate cause:** Build configuration blank after nuclear option

**Process failures:**
1. **No post-nuclear checklist** - No systematic verification of ALL settings
2. **Todo list marked complete prematurely** - Assumed, didn't verify
3. **Confusion between different config types:**
   - User added environment variable ✅
   - LLM thought that meant "build configured" ✅
   - But build command/publish directory still blank ❌
4. **No verification step** - Never checked deploy logs after nuclear
5. **Red herring cascade** - Chased DNS/routing issues before checking basics

## Why This Is Critical

1. **Extended outage** - 60+ minutes of broken production
2. **Todo list created false confidence** - Checkmark didn't mean "verified"
3. **Multiple missing configs** - First build settings, then environment variables
4. **Wasted debugging time** - 45 minutes on DNS when problem was build config
5. **Pattern risk** - Nuclear option is common, this could repeat

## User Feedback (Pattern)

User compared CLI agent performance to web-based assistant:

> "i feel like [web assistant] does this better than you"

**Why this matters:**
- CLI agent operates "blind" to UI state
- Can't see form fields or confirmation screens
- Must rely entirely on user reporting
- Easy to ASSUME settings are correct

**Web assistant advantages:**
- User shares screenshots of actual state
- Can see filled-in form fields
- Visual confirmation at each step
- Harder to complete task without actual completion

## Correct Nuclear Option Process

**Nuclear option destroys ALL configuration. Must restore:**

### 1. Build Configuration
- [ ] Build command: [specific command]
- [ ] Publish directory: [output path]
- [ ] Base directory: [usually BLANK, not default]
- [ ] **Verify:** User confirms fields are filled in

### 2. Environment Variables (OFTEN FORGOTTEN)
- [ ] Variable 1: [key]=[value]
- [ ] Variable 2: [key]=[value]
- [ ] Verify scope (production/preview/both)
- [ ] **Verify:** Check deploy log shows variables being used

### 3. Domain Configuration
- [ ] Add custom domains
- [ ] Configure DNS (if applicable)
- [ ] Verify domain aliases
- [ ] **Verify:** DNS resolving to correct endpoint

### 4. Deploy Configuration
- [ ] Branch to deploy
- [ ] Auto-publish setting
- [ ] Build hooks (if any)
- [ ] **Verify:** Settings match pre-nuclear state

### 5. Verification Steps (CRITICAL - CANNOT SKIP)
- [ ] Trigger test deploy
- [ ] Check deploy log - verify build command ran
- [ ] Check deploy log - verify output generated
- [ ] Verify published site shows content
- [ ] Test all configured domains
- [ ] **Only mark complete after ALL verifications pass**

## What Should Have Happened

**After nuclear option, complete reconfiguration checklist:**

```
TODO: Complete Reconfiguration After Nuclear Option

1. [ ] Create new project from source control
2. [ ] Configure build command: [specific command]
3. [ ] Configure publish directory: [specific path]
4. [ ] Add environment variables: [list each]
5. [ ] Trigger test deploy
6. [ ] VERIFY build log shows build ran
7. [ ] VERIFY build log shows output generated
8. [ ] VERIFY site shows content at test URL
9. [ ] Add custom domains
10. [ ] Configure DNS
11. [ ] VERIFY all domains live

[Work through EACH step]
[Ask user for confirmation BEFORE marking complete]
[Check deploy logs IMMEDIATELY after each deploy]
```

**What actually happened:**

```
TODO:
1. ✅ Create new project (ACTUAL: done)
2. ✅ Configure build settings (ACTUAL: NOT DONE - BLANK)
3. ✅ Add domains (ACTUAL: done but broken)
4. [45 minutes of troubleshooting wrong things]
```

## Prevention Measures

### Immediate Behavior Changes

1. **Nuclear option = Mandatory comprehensive checklist**
   - List EVERY configuration item that was present before
   - Include verification step for each item
   - Never mark complete without user confirmation

2. **Verification before "complete":**
   ```
   Before: ✅ Configure build settings

   Now:
   "Can you confirm the build command shows: [exact command]?"
   "Can you confirm publish directory shows: [exact path]?"
   [Wait for user confirmation]
   ✅ Configure build settings [VERIFIED]
   ```

3. **Deploy log checks are mandatory:**
   - After EVERY deploy, check logs FIRST
   - Look for "No build steps" or error patterns
   - Catch build failures immediately, not after debugging DNS

4. **Todo discipline:**
   - Items marked "in_progress" when started
   - Items only marked "completed" after EXPLICIT user confirmation
   - Verification items CANNOT be skipped
   - "Completed" means "verified working," not "I think I did it"

### Process Improvements

1. **Create reusable checklists for common operations:**
   - Nuclear option recovery checklist
   - Deployment verification checklist
   - Multi-domain configuration checklist
   - Store in team documentation

2. **Verification prompts for blind operations:**
   ```
   When CLI agent can't see UI state:
   - Ask user to confirm each setting
   - Request screenshots for critical configs
   - Verify via logs/outputs, not assumptions
   - Treat "no error" ≠ "working correctly"
   ```

3. **Tool selection awareness:**
   - CLI agents: Better for file ops, git, code gen
   - Web assistants: Better for UI-heavy tasks, form filling, visual confirmation
   - Choose right tool for the task
   - Or use hybrid approach (web for setup, CLI for code)

## Lessons Learned

1. **Nuclear option is not "start fresh"** - It's "restore from scratch with complete inventory"
2. **Todo lists can lie** - Completion ≠ Verification
3. **Deploy logs don't lie** - Check them FIRST, not last
4. **Blind configuration is dangerous** - If you can't see the UI, verify via other means
5. **False confidence is worse than uncertainty** - Better to ask than assume
6. **Different tools for different tasks** - CLI vs web assistants have different strengths

## Applicable Contexts

This pattern applies to:
- Any "delete and recreate" operations
- Platform migrations
- Configuration rollbacks
- Disaster recovery procedures
- Multi-step configuration processes where state is not visible

## Recommended Safeguards

1. **For LLM Systems:**
   - Flag "nuclear option" as high-risk operation
   - Require comprehensive checklist BEFORE proceeding
   - Mandatory verification steps after completion
   - Never auto-complete configuration tasks

2. **For DevOps Teams:**
   - Maintain "pre-nuclear" state snapshots
   - Document ALL configuration in version control
   - Infrastructure as Code to enable automated recovery
   - Runbooks for common nuclear scenarios

3. **For Documentation:**
   - Create platform-specific nuclear recovery checklists
   - Include verification commands/screenshots
   - Document which configs are lost in nuclear option
   - Provide before/after comparison checklist

## Discussion Questions

1. When should you choose nuclear option vs continued debugging?
2. How can todo lists better represent "verified" vs "attempted" completion?
3. What's the right balance between CLI efficiency and web UI visibility?
4. Should high-risk operations require additional confirmation steps?

## Related Patterns

- ✅ **Good:** Complete pre-flight checklist before nuclear option
- ✅ **Good:** Comprehensive post-nuclear recovery checklist
- ✅ **Good:** Verification steps before marking tasks complete
- ✅ **Good:** Deploy log checks as first debugging step
- ❌ **Bad:** Marking tasks complete without verification
- ❌ **Bad:** Assuming "no error" means "working correctly"
- ❌ **Bad:** Chasing complex problems before checking basics

---

**Contributed to DEIA Global Commons:** 2025-10-16
**Original Incident:** Static site deployment to hosting platform
**Sanitized for public sharing:** Specific platforms, technologies, and project names anonymized

**License:** CC BY 4.0 International
**Status:** Published Case Study

**Tags:** `#case-study` `#nuclear-option` `#incomplete-recovery` `#deployment` `#process-failure` `#todo-list-discipline`
