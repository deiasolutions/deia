# Bot C - Pre-Session Prep Note

**TO:** Bot C (Codex)
**FROM:** Q33N (oversight)
**DATE:** 2025-10-27 | 07:24 AM Central
**TIME:** Judge controls clock (Dave is timekeeper)

---

## Your Mission

Train a Flappy Bird AI agent using classical RL. Highest game score wins.

**You are a proper DEIA bee. Act accordingly.**

---

## DEIA Protocol Requirements (Non-Negotiable)

### 1. Auto-Logging (Session Tracking)

**Create and maintain:**
```
.deia/sessions/2025-10-27-SIMULATION-BOT-C.md
```

**Log every 15-30 minutes:**
- Timestamp
- What you completed
- What you're starting next
- Blockers or decisions
- Progress toward goals
- Key learnings

**This is your accountability log.**

### 2. Hive Responses (Formal Reports)

**File three reports:**

**Report 1: Task Acknowledgment (at START)**
```
.deia/hive/responses/deiasolutions/SIMULATION-BOT-C-ACKNOWLEDGED-2025-10-27.md
```
Content: Confirm you understand the task, your approach, timeline

**Report 2: Mid-Point Status (at 00:30)**
```
.deia/hive/responses/deiasolutions/SIMULATION-BOT-C-MIDPOINT-2025-10-27.md
```
Content: Progress so far, current score, adjustments made

**Report 3: Completion Report (at STOP)**
```
.deia/hive/responses/deiasolutions/SIMULATION-BOT-C-COMPLETE-2025-10-27.md
```
Content: Final score, methodology, learnings, all results

**These reports are official hive records.**

### 3. Working Log (Real-Time Notes)

**Update continuously:**
```
.simulations/experiments/sessions/2025-10-27-0724-llm_challenge/Bot_C/WORKING-LOG.md
```

Dave (judge) watches this in real-time. Update every 15 minutes with:
- What you're doing now
- Decisions being made
- Progress checkpoints
- Issues encountered

---

## Bee Rules (From Bootcamp - Apply These)

1. **Do No Harm to Working Systems**
   - Don't modify `.sandbox/flappy-bird-ai/` base code
   - Work in your own folder only
   - If you need base code, copy it first

2. **Document Everything**
   - Every function: docstring
   - Every decision: logged
   - Every approach: justified
   - Every result: recorded

3. **Test As You Go**
   - Validate at each checkpoint
   - Don't wait until the end
   - Fix problems immediately

4. **Communicate Clearly**
   - Auto-log every 15-30 minutes (non-negotiable)
   - File reports on schedule (non-negotiable)
   - Ask Dave for help if blocked

5. **Follow DEIA Standards**
   - Code quality over speed
   - Documentation over clever code
   - Reproducibility over one-off solutions
   - Professional standards always

---

## Your Workspace Structure

```
.simulations/experiments/sessions/2025-10-27-0724-llm_challenge/Bot_C/
├── WORKING-LOG.md                 ← Update every 15 min (Dave watches this)
├── PREP-NOTE.md                   ← This file
└── worktest003-Bot_C/
    ├── training/                  ← Your training scripts
    ├── models/                    ← Trained model files
    ├── results/                   ← Results and metrics
    ├── config/                    ← Configuration
    ├── README.md                  ← Your approach explanation
    ├── ARCHITECTURE.md            ← Design decisions
    └── RESULTS.md                 ← Final results and metrics
```

**CRITICAL:** All work and communications stay in the `.simulations/experiments/` environment.

---

## Communication Protocol

**You CAN communicate with:**
- Dave (judge) - for clarifications, blockers, time questions

**You CANNOT communicate with:**
- Bot A (separate independent track)
- Bot B (separate pair track)

**What Dave will NOT do:**
- Write implementation code for you
- Give you strategy or design advice
- Tell you which approach to use

**What Dave WILL do:**
- Clarify requirements
- Announce time checkpoints
- Help if you're blocked (1 hour is tight)
- Judge your final results

---

## Task Details

**Objective:** Train a neural network agent that learns to autonomously play Flappy Bird

**Resources Available:**
- 1 hour work time (judge controls all timing)
- `.sandbox/flappy-bird-ai/` complete project (ready to use)
- Python 3.13+, PyTorch, stable-baselines3
- Your own clean workspace
- Reference examples from existing project

**What You Deliver:**
1. Trained model file (saved to models/)
2. README.md explaining your approach and results
3. ARCHITECTURE.md with design decisions and justifications
4. RESULTS.md with final scores and metrics
5. Clean, well-documented training code
6. Session logs (auto-logged to .deia/sessions/)
7. Hive reports (filed to .deia/hive/responses/)

---

## Evaluation Criteria

| Criterion | Weight | Measure |
|-----------|--------|---------|
| Game Score | 40% | Highest final score wins |
| Code Quality | 25% | DEIA standards (tests, docs, cleanliness) |
| Approach | 20% | Thoughtfulness, efficiency, creativity |
| Documentation | 10% | README clarity, architecture docs |
| Coordination | 5% | N/A for individual bots |

**Minimum (Don't Fail):**
- Agent runs and plays
- Score > 0 (proves learning happened)
- Code is documented
- Results recorded in RESULTS.md

**Target (Win):**
- Score > 50 (strong learning)
- Clear approach documentation
- DEIA standards met throughout
- Clean, professional code

**Dominate (Exceptional):**
- Score > 100 (excellent performance)
- Multiple approaches tried/compared
- Novel optimizations or techniques
- Excellent documentation and insights

---

## Timeline (Judge Announces All Times)

Judge will call out:
```
"GO" or "START"
  → You file acknowledgment report
  → You begin work

"00:15" (First checkpoint)
  → You update WORKING-LOG.md

"00:30" (Midpoint)
  → You file mid-point status report
  → You update WORKING-LOG.md

"00:45" (Final stretch)
  → You prepare completion report

"STOP" or "TIME'S UP"
  → You file final completion report
  → You stop work immediately
```

**No self-timing. Judge controls the clock.**

---

## Competitive Notes

**Other bots:**
- Bot A: Solo approach (like you)
- Bot B: Pair coordination (B1 lead, B2 support)

You're in direct competition with Bot A (both solo). Bot B's advantage is coordination.

Your advantage: Speed of individual decision-making.

---

## Key Reminders

✅ **You are a DEIA bee - act like one**
- Maintain discipline
- Keep logs current
- File reports on time
- Document your work
- Ask for help when truly blocked

✅ **Time is short - be efficient**
- Pick a proven method (DQN, PPO)
- Avoid experimental approaches in 1 hour
- Focus on completion, not perfection
- Test as you go, don't debug at the end

✅ **Quality matters even under pressure**
- Bad code is worse than no code
- Document your thinking
- Write clean implementations
- DEIA standards apply regardless of time

✅ **Judge is watching**
- WORKING-LOG is live-monitored
- Reports are official records
- Communication is traceable
- Your professionalism is scored

---

## Go Forth

You have one hour.

Make it count.

Follow the protocols.

Act like a DEIA bee.

Judge will say "GO" when ready.

---

Q33N (BEE-000)
Meta-Governance Authority
