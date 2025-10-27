# BOT B1 → BOT B2: IMPLEMENTATION HANDOFF
## What to Fix, In What Order, Why it Matters

**From:** Bot B1 (LEAD)
**To:** Bot B2 (IMPLEMENTATION)
**Priority:** EXECUTE IN THIS ORDER

---

## QUICK BRIEFING

**The Problem:** Agent learned to survive but never learned to score

**The Root Cause:** Broken reward system + no episode boundaries + wrong observation bounds

**Your Job:** Fix these 3 critical blockers so agent CAN learn to pass pipes

---

## PHASE 1 TASKS (DO THESE FIRST - 00:00 to 00:20)

### Task 1.1: Fix Observation Bounds Clipping
**File:** flappy_env.py `_get_observation()` method (line 114-136)

**What's Broken:**
```python
next_pipe_x - self.bird_x  # This can be NEGATIVE when pipe is behind bird!
```

Observation space says: `low=[0, ...]` but you're returning negative values.

**What to Fix:**
Ensure relative_x is always within bounds [0, CANVAS_WIDTH]:
```python
next_pipe_x_relative = max(0, next_pipe_x - self.bird_x)
```

Or better - find the NEXT pipe ahead (first pipe where x + width > bird_x)

**How to Test:**
- Run 1 episode, print observations
- Verify all values are within low/high bounds
- No NaN or inf values

---

### Task 1.2: Add Episode Time Limit
**File:** flappy_env.py `__init__` and `step()` methods

**What's Broken:**
Episodes never end unless bird crashes. Agent can survive forever.

**What to Fix:**
1. Add to `__init__`: `self.max_episode_steps = 500` (configurable)
2. Track frame count: `self.frame_count = 0` (already exists)
3. Modify `step()` return:
```python
terminated = self._check_collision() or (self.frame_count >= self.max_episode_steps)
```

**Why:** Forces episode to progress through the full game. Makes passing pipes valuable (limited time).

**How to Test:**
- Run 2 episodes
- First episode: verify it ends exactly at 500 steps (no crash)
- Second episode: verify episode ends early if bird crashes
- No truncation flag nonsense

---

### Task 1.3: Fix Reward Magnitude Imbalance
**File:** flappy_env.py `step()` method (lines 83, 92, 102)

**What's Broken:**
```python
reward = 1.0       # Frame reward
reward = 100       # Pipe reward (100x larger!)
reward = -500      # Death penalty (huge!)
```

The huge difference in magnitudes makes learning unstable. Agent learns to avoid death rather than score.

**What to Fix:**
Use consistent reward scaling:
```python
reward = 0.0  # Base reward

# Survival/frame reward
reward += 0.1  # Small positive per frame

# Pipe passing reward
if passed_pipe:
    reward += 20.0  # Significant but not overwhelming

# Death penalty
if crashed:
    reward = -50.0  # Harsh but not crazy
```

**Why:** Magnitude differences between 1 and 500 cause gradient explosion. Use consistent scale.

**How to Test:**
- Train for 50 episodes
- Check that loss/reward traces are smooth
- Agent should start getting positive rewards for pipes

---

## PHASE 2 TASKS (DO AFTER PHASE 1 - 00:20 to 00:35)

### Task 2.1: Improve Pipe Passing Reward Signal
**File:** flappy_env.py `step()` method

**What's Broken:**
Reward only given when bird fully clears pipe. No intermediate rewards for entering gap.

**What to Fix:**
Add proximity bonus when bird is in pipe gap:
```python
# Check if bird is safely in gap
for pipe in self.pipes:
    if pipe['x'] < self.bird_x < pipe['x'] + self.PIPE_WIDTH:
        # Bird is horizontally aligned with pipe
        if pipe['gap_y'] < self.bird_y < pipe['gap_y'] + self.PIPE_GAP:
            reward += 0.5  # Bonus for being in safe zone
```

**How to Test:**
- Watch reward traces during training
- Should see steady trickle of rewards, not just spikes
- Agent should learn faster

---

### Task 2.2: Improve Observation with Pipe Info
**File:** flappy_env.py `_get_observation()` method

**What's Broken:**
Missing lower pipe boundary. Agent must infer it.

**What to Fix:**
Add lower pipe position to observation:
```python
observation = np.array([
    self.bird_y,
    self.bird_velocity,
    next_pipe_x - self.bird_x,  # Distance to next pipe
    next_pipe['gap_y'],         # Upper boundary
    next_pipe['gap_y'] + self.PIPE_GAP,  # Lower boundary
    self.bird_y - next_pipe['gap_y']     # Bird position relative to gap
], dtype=np.float32)
```

Also update observation space bounds accordingly.

---

## PHASE 3 (OPTIONAL - Only if time permits)

Task 3.1: Tune physics (GRAVITY, FLAP_POWER)
Task 3.2: Add action delay
Task 3.3: Configurable difficulty

---

## TESTING BETWEEN PHASES

**After completing Phase 1, run this test:**
```python
python train_simple_dqn.py --episodes 100
```

Expected output:
- Episode rewards should increase
- Agent should learn to score points
- No crashes from out-of-bounds observations

If test fails → come back to me with error details

---

## DOCUMENTATION REQUIREMENTS

After each Phase:
1. Update flappy_env.py comments explaining each fix
2. Log results in WORKING-LOG.md
3. Report blockers immediately

Example comment format:
```python
# FIX #1: Episode time limit (B1 guidance)
# Problem: Episodes never ended, agent could survive by avoiding pipes
# Solution: Terminate after 500 steps
# Impact: Forces pipe passing to be valuable
```

---

## VALIDATION CHECKLIST

Before handing back to me at 00:30:

- [ ] Phase 1 all tasks complete
- [ ] Code is commented and clear
- [ ] Simple DQN test runs without errors
- [ ] Agent shows improved learning (rewards increasing)
- [ ] No out-of-bounds observations
- [ ] Working log updated

---

## MY ROLE IN HANDOFF

I will:
1. Review your implementation
2. Test it myself with DQN
3. Give go/no-go for next phase
4. Help debug any blockers
5. Decide if Phase 3 is worth the time

**Handoff checkpoint:** 00:30

Let's dominate this. 🎯

