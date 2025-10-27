# Bot B1 - Pre-Session Prep Note (LEAD)

**TO:** Bot B1 (Claude Code - LEAD ARCHITECT)
**FROM:** Q33N (oversight)
**DATE:** 2025-10-27 | 07:24 AM Central
**TIME:** Judge controls clock (Dave is timekeeper)

---

## Your Mission

**Lead** a paired effort to train a Flappy Bird AI agent. You architect. B2 supports and validates.

**You are a DEIA bee LEADER. Act accordingly.**

---

## DEIA Protocol Requirements (Non-Negotiable)

### 1. Auto-Logging (Session Tracking)

**Create and maintain:**
```
.deia/sessions/2025-10-27-SIMULATION-BOT-B.md
```

**Log every 15-30 minutes:**
- Timestamp
- Decisions made (you as lead)
- Input from B2 (validation, suggestions)
- What's being implemented
- Blockers or challenges
- Handoff status

**This is your leadership log.**

### 2. Hive Responses (Formal Reports)

**File three reports:**

**Report 1: Pair Acknowledgment (at START)**
```
.deia/hive/responses/deiasolutions/SIMULATION-BOT-B-ACKNOWLEDGED-2025-10-27.md
```
Content: Your approach, team structure, collaboration plan

**Report 2: Mid-Point Status (at 00:30)**
```
.deia/hive/responses/deiasolutions/SIMULATION-BOT-B-MIDPOINT-2025-10-27.md
```
Content: Progress, handoff outcomes, collaboration effectiveness

**Report 3: Completion Report (at STOP)**
```
.deia/hive/responses/deiasolutions/SIMULATION-BOT-B-COMPLETE-2025-10-27.md
```
Content: Final score, methodology, how pair coordination added value

**Emphasize pair effectiveness in all reports.**

### 3. Working Log (Real-Time Notes - SHARED with B2)

**Maintain shared:**
```
.simulations/experiments/sessions/2025-10-27-0724-llm_challenge/Bot_B/WORKING-LOG.md
```

**Sections:**
- **B1 Notes** - Your decisions and leadership
- **B2 Notes** - B2's validation and suggestions  
- **Handoff Log** - Document all B1→B2 and B2→B1 transitions
- **Coordination Notes** - How pair work improved outcomes

Dave watches this in real-time.

---

## Your Role: LEAD ARCHITECT

✅ **You Decide:**
- Which classical RL method (DQN, PPO, NEAT, etc.)
- Overall strategy and approach
- Architecture and design
- Major technical decisions

✅ **B2 Does:**
- Implementation based on your direction
- Validation and testing
- Suggests alternatives (you make final call)
- Executes your vision with quality

❌ **You Don't Do:**
- Work alone (B2 is your support)
- Ignore B2's input (they see things you miss)
- Make decisions without explaining to B2

---

## Bee Rules (From Bootcamp)

1. **Do No Harm** - Don't modify `.sandbox/flappy-bird-ai/` base code
2. **Document Everything** - All decisions, approaches, learnings
3. **Test As You Go** - Validate at each checkpoint
4. **Communicate Clearly** - Especially with B2 (your partner)
5. **Follow DEIA Standards** - Quality, professionalism, discipline

**LEADERSHIP ADDITIONS:**
6. **Lead by Example** - Follow protocols perfectly
7. **Empower Your Partner** - Listen to B2's input
8. **Document Handoffs** - Clear transitions of work
9. **Show Pair Value** - Demonstrate how collaboration helped

---

## Pair Coordination Mechanics

### Handoff Protocol

At logical checkpoints, hand off to B2:

1. **Document state:** What you've decided and created
2. **Explain vision:** What B2 should do next
3. **Pass control:** B2 takes ownership
4. **Log transition:** Record handoff in WORKING-LOG.md

### Your Handoff Checkpoints

**Handoff 1: B1 → B2 (around 00:15)**
- You: Decided method, created architecture, script skeleton
- B2: Implements and tests your design

**Handoff 2: B2 → B1 (around 00:30)**
- B2: Shows progress, suggests improvements
- You: Review, make adjustments, continue

**Pattern:** Alternate every 15 minutes

---

## Your Timeline

**00:00 - START**
- You choose method
- You design architecture  
- You explain to B2
- You create script skeleton
- B2 reviews and confirms understanding

**00:15 - HAND TO B2**
- B2 takes over: "I understand, I'll implement X"
- B2 begins implementation
- You monitor/support

**00:30 - B2 HANDS BACK**
- B2: "Here's the progress, I found this issue, suggest we do Y"
- You: Review, decide, continue work

**00:45 - FINAL COORDINATION**
- Both working together
- You both preparing results

**01:00 - STOP**
- File completion report (joint effort)

---

## Evaluation (Pair Wins If...)

1. **Game Score** (40%) - Highest score
2. **Code Quality** (25%) - DEIA standards
3. **Approach** (20%) - Thoughtfulness
4. **Documentation** (10%) - Clarity
5. **Coordination** (5%) - ← **THIS IS YOUR ADVANTAGE**

Your pair coordination is worth extra points. Show:
- How B2's validation improved design
- How handoffs created better solutions
- How pair work beat individual approaches
- Professional leadership and collaboration

---

## Workspace Structure

```
.simulations/experiments/sessions/2025-10-27-0724-llm_challenge/Bot_B/
├── WORKING-LOG.md                 ← Shared, both log here
├── PREP-NOTE-B1.md                ← This file
├── PREP-NOTE-B2.md                ← B2's instructions
└── worktest002-Bot_B/
    ├── training/                  ← Joint training scripts
    ├── models/                    ← Trained model
    ├── results/                   ← Results and metrics
    ├── config/                    ← Configuration
    ├── README.md                  ← Joint approach explanation
    ├── ARCHITECTURE.md            ← Design (you led)
    └── RESULTS.md                 ← Final results
```

**All work and communications in `.simulations/` environment.**

---

## Communication Protocol

**You CAN communicate with:**
- B2 (your partner) - continuous coordination required
- Dave (judge) - clarifications/blockers only

**You CANNOT communicate with:**
- Bot A (separate track)
- Bot C (separate track)

**What Dave will NOT do:**
- Write code
- Give strategy advice
- Tell you which approach to use

**What Dave WILL do:**
- Clarify requirements
- Announce time checkpoints
- Help if you're blocked
- Judge your results

---

## Task Details

**Objective:** Train neural network agent for Flappy Bird

**Available:**
- 1 hour work time (judge controls clock)
- `.sandbox/flappy-bird-ai/` project
- Python 3.13+, PyTorch, stable-baselines3
- Clean workspace for pair work

**Deliverables:**
1. Trained model with score
2. Code with DEIA standards
3. README explaining approach
4. ARCHITECTURE documenting design
5. RESULTS with metrics
6. Session logs
7. Hive reports showing pair effectiveness

---

## Evaluation Criteria

| Criterion | Weight | Measure |
|-----------|--------|---------|
| Game Score | 40% | Highest score |
| Code Quality | 25% | DEIA standards |
| Approach | 20% | Thoughtfulness |
| Documentation | 10% | Clarity |
| Coordination | 5% | **Pair collaboration value** |

---

## Key Leadership Principles

✅ **Decide clearly** - Pick method fast, explain thoroughly
✅ **Listen to B2** - They see implementation challenges
✅ **Document handoffs** - Clear transitions prevent rework
✅ **Lead by example** - Follow all protocols perfectly
✅ **Show pair value** - Make collaboration visible
✅ **Protect time** - Don't get stuck in analysis

---

## Go Forth

You are a leader.

Lead with clarity and professionalism.

Let B2 support you.

Make the pair work shine.

Judge will say "GO" when ready.

---

Q33N (BEE-000)
