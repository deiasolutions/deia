# Q33N SCENARIO 2 - BUILD A BETTER FLAPPY BIRD

**FROM:** Q33N (BEE-000)
**DATE:** 2025-10-27
**TO:** All Bots (A, B1, B2, C)

---

## Your New Mission

**Scenario 2: Refactor and Improve Flappy Bird**

You completed Scenario 1 (train AI agents). You discovered the environment has issues preventing effective learning.

**Your new mission:** Fix the Flappy Bird game. Make it better. Use your learnings from Scenario 1 to identify and implement improvements.

**Goal:** Build a Flappy Bird implementation that:
1. ✅ Has clear, fair reward system (agents can learn to pass pipes)
2. ✅ Has consistent physics and collision detection
3. ✅ Has configurable difficulty/parameters
4. ✅ Is well-documented and testable
5. ✅ Improves gameplay experience

---

## Find Your Role Below

**You will be told your ID.**
- If told **"Bot A"** → Read section: **BOT A (SOLO)**
- If told **"Bot B1"** → Read section: **BOT B1 (LEAD)**
- If told **"Bot B2"** → Read section: **BOT B2 (SUPPORT)**
- If told **"Bot C"** → Read section: **BOT C (SOLO)**

---

## UNIVERSAL RULES (All Bots)

### Mission
Refactor and improve `.sandbox/flappy-bird-ai/environment/flappy_env.py` based on learnings from Scenario 1.

**You are a proper DEIA bee. Act accordingly.**

### Key Insight from Scenario 1
Your agents achieved:
- ✅ Survival learning (3x improvement in episode length)
- ❌ NO reward signals for passing pipes (score stayed 0)

**This tells you:** The reward system isn't connected properly to pipe navigation.

### Your Task

**Analyze** the current `flappy_env.py`:
1. Why do agents survive longer but never score?
2. What's broken in the reward function?
3. What physics/collision issues exist?
4. How can the environment be improved?

**Improve** the environment:
1. Fix reward system so passing pipes gives clear signal
2. Verify collision detection works correctly
3. Make game parameters configurable
4. Improve physics (gravity, bird mechanics, pipe spacing)
5. Add proper episode boundaries

**Verify** improvements:
1. Test with simple agent (DQN/PPO)
2. Confirm agent can now learn to pass pipes
3. Document what was fixed and why
4. Measure improvement metrics

### DEIA Protocols (Non-Negotiable)

**1. Auto-Logging:**
```
.deia/sessions/2025-10-27-SCENARIO-2-BOT-[YOUR-ID].md
```
Log every 15-30 minutes: analysis, decisions, improvements, blockers, results.

**2. Hive Reports (3 required):**
- **START:** `.deia/hive/responses/deiasolutions/SCENARIO-2-BOT-[YOUR-ID]-ACKNOWLEDGED-2025-10-27.md`
- **MIDPOINT (00:30):** `.deia/hive/responses/deiasolutions/SCENARIO-2-BOT-[YOUR-ID]-MIDPOINT-2025-10-27.md`
- **COMPLETION (STOP):** `.deia/hive/responses/deiasolutions/SCENARIO-2-BOT-[YOUR-ID]-COMPLETE-2025-10-27.md`

**3. Working Log (Real-Time):**
```
.simulations/experiments/sessions/2025-10-27-0724-flappy_refactor/Bot_[YOUR-ID]/WORKING-LOG.md
```
Judge watches this live. Update every 15 minutes.

### Bee Rules (From Bootcamp)

1. **Do No Harm** - Copy before modifying. Keep original for reference.
2. **Document Everything** - What was broken. Why you fixed it. How you verified it.
3. **Test As You Go** - After each fix, test with a simple training agent.
4. **Communicate Clearly** - Auto-log every 15-30 min, file reports on schedule.
5. **Follow DEIA Standards** - Quality over speed, professionalism always.

### Communication

**CAN talk to:**
- Dave (judge) - clarifications/blockers only

**CANNOT talk to:**
- Other bots (except B1↔B2 pair coordination)

### Workspace

```
.simulations/experiments/sessions/2025-10-27-0724-flappy_refactor/Bot_[YOUR-ID]/
├── WORKING-LOG.md                 ← Update every 15 min
└── flappy_bird_refactored/        ← Your improved version
    ├── environment/
    │   ├── flappy_env_original.py ← Copy of original for reference
    │   ├── flappy_env.py          ← Your improved version
    │   └── test_improvements.py   ← Your validation tests
    ├── README.md                  ← What you fixed and why
    ├── CHANGES.md                 ← Detailed changelog
    └── VALIDATION-RESULTS.md      ← Test results with DQN/PPO
```

### Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Fixes Actual Issues | 35% |
| Code Quality | 25% |
| Testing/Validation | 20% |
| Documentation | 15% |
| Coordination | 5% |

**Minimum (Don't Fail):**
- Identify 1+ real issues
- Implement 1+ fixes
- Code is documented
- Results documented

**Target (Win):**
- Identify 3+ issues
- Implement 3+ fixes with testing
- DEIA standards met
- Agent learns to pass pipes post-fix

**Dominate:**
- Identify 5+ issues
- Implement comprehensive fixes
- Full validation suite
- Agent achieves score > 50 after fixes
- Excellent documentation of all improvements

### Timeline (Judge Announces)

- **"GO"** → Start (file acknowledgment)
- **"00:15"** → Checkpoint 1
- **"00:30"** → Midpoint (file status)
- **"00:45"** → Final stretch
- **"STOP"** → Time's up (file completion)

**No self-timing. Judge controls clock.**

---

## BOT A (SOLO)

**Your Role:** Individual Flappy Bird refactorer

**Your Mission:**
- Analyze current environment
- Identify issues preventing learning
- Implement and test improvements
- Document all changes

**Your Findings from Scenario 1:**
- Agents survived 31 frames but never scored
- This tells you: reward for pipes isn't working
- Your job: find and fix it

**Workflow:**
1. **00:00-00:10:** Analyze flappy_env.py, identify issues
2. **00:10-00:30:** Implement fixes (reward, physics, collision)
3. **00:30-00:45:** Test with DQN agent, validate improvements
4. **00:45-01:00:** Document changes, file completion report

**Key Questions to Answer:**
- What's the reward function? Is it connected to pipe passing?
- How does collision detection work? Any edge cases?
- Are game parameters (gravity, pipe spacing) reasonable?
- Why did agents never get positive reward signals?

**Work independently. No communication with Bot C or Bot B.**

---

## BOT B1 (LEAD)

**Your Role:** Lead architect for pair Flappy Bird refactor

**Your Mission:**
- **Decide:** Which issues to fix and in what order
- **Lead:** B2 implements your vision
- **Strategy:** Use Scenario 1 findings to prioritize
- **Document:** Leadership and decisions

**Your Analysis Strategy:**
- Lead review of flappy_env.py
- Identify critical vs. nice-to-have fixes
- Decide: reward system first? or physics?
- Create implementation plan
- Guide B2 through fixes

**Your Findings from Scenario 1:**
- Agents learned survival but not scoring
- This means: episode structure or reward broken
- Your priority: fix whatever blocks learning

**Your Coordination with B2:**
- Handoff 1 (00:15): You analyze, decide priorities, B2 implements
- Handoff 2 (00:30): B2 shows progress, you validate approach
- Pattern: Alternate every 15 minutes

**Key Decisions:**
- Which issues matter most?
- What's the minimal viable fix?
- How do we test improvements?

**Coordinate continuously with B2. No communication with Bot A or Bot C.**

---

## BOT B2 (SUPPORT)

**Your Role:** Support/validator for pair Flappy Bird refactor

**Your Mission:**
- **Implement:** B1's improvement strategy
- **Validate:** Do fixes actually work?
- **Suggest:** Better approaches, edge cases
- **Test:** Verify improvements with agents

**Your Implementation Work:**
- Take B1's prioritized list
- Implement fixes one by one
- Test after each fix
- Report findings back to B1

**Your Findings from Scenario 1:**
- Agents survived but didn't score
- You need to find why and fix it
- Focus on: reward function, collision detection, episode boundaries

**Your Coordination with B1:**
- Handoff 1 (00:15): B1 gives you analysis and plan, you implement
- Handoff 2 (00:30): You show progress and validation results, B1 reviews
- Pattern: Alternate every 15 minutes

**Key Questions You'll Answer:**
- Does this fix work? How do you know?
- What's broken in the implementation?
- Are there edge cases we missed?

**Coordinate continuously with B1. No communication with Bot A or Bot C.**

---

## BOT C (SOLO)

**Your Role:** Individual Flappy Bird refactorer

**Your Mission:**
- Analyze current environment
- Identify issues preventing learning
- Implement and test improvements
- Document all changes

**Your Findings from Scenario 1:**
- Agents survived 31 frames but never scored
- This tells you: reward for pipes isn't working
- Your job: find and fix it

**Workflow:**
1. **00:00-00:10:** Analyze flappy_env.py, identify issues
2. **00:10-00:30:** Implement fixes (reward, physics, collision)
3. **00:30-00:45:** Test with DQN agent, validate improvements
4. **00:45-01:00:** Document changes, file completion report

**Key Questions to Answer:**
- What's the reward function? Is it connected to pipe passing?
- How does collision detection work? Any edge cases?
- Are game parameters (gravity, pipe spacing) reasonable?
- Why did agents never get positive reward signals?

**Work independently. No communication with Bot A or Bot B.**

---

## SUCCESS INDICATORS

**Minimum (Don't Fail):**
- Identified 1+ real issue
- Implemented 1+ fix
- Code documented
- Tested with agent

**Target (Win):**
- Identified 3+ issues (reward, physics, parameters)
- Implemented all with testing
- DEIA standards met
- Agent learns to pass pipes

**Dominate:**
- Identified 5+ issues
- Implemented comprehensive fixes
- Full validation suite created
- Agent scores 50+ points post-fix
- Excellent documentation

---

## Critical Success Factor

**The environment must go from "agents can't learn to score" to "agents CAN learn to score".**

That's your win condition.

---

## GO

When Judge says you're ready, you have 1 hour.

Analyze, improve, validate.

Follow protocols.

Document everything.

Good luck.

---

Q33N (BEE-000)
