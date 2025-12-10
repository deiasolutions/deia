# DEIA Orchestrator Bot Specification

## Overview

The Orchestrator is an ML-powered bot that learns optimal task routing based on historical performance data. It decides which platform/vendor/model should handle each task based on cost, time, quality, and success patterns.

## Key Principle

> "The prediction should be 'task x, use a claude code cli', not 'bot x' because I want the model to respond to information like... what's the cost and time... what was the vendor and model... what was the quality"
>
> — Dave

The Orchestrator routes tasks to **platforms**, not specific bot IDs. It learns which platform (Claude Code CLI, Claude API, Codex CLI, etc.) performs best for each task type.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestrator Bot                        │
│                                                             │
│  ┌─────────────────┐  ┌────────────────────────────────┐  │
│  │                 │  │                                │  │
│  │  Task Analyzer  │  │  ML Prediction Engine          │  │
│  │                 │  │                                │  │
│  │  • Parse task   │  │  • Load historical data        │  │
│  │  • Extract type │  │  • Feature extraction          │  │
│  │  • Complexity   │  │  • Neural network prediction   │  │
│  │                 │  │  • Output: platform + conf%    │  │
│  └─────────────────┘  └────────────────────────────────┘  │
│           ↓                         ↓                      │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           Router Decision                           │  │
│  │                                                     │  │
│  │  Task: "Fix bug in session_logger.py"             │  │
│  │  Prediction: Claude Code CLI (85% confidence)     │  │
│  │  Reason: Similar tasks avg 120s, $0.03, 9/10 qual │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Task Assignment                                │
│                                                             │
│  .deia/hive/tasks/TASK-fix-session-logger-bug.md           │
│  Platform: claude-code-cli                                 │
│  Assigned to: Next available bot with that platform        │
└─────────────────────────────────────────────────────────────┘
```

## Training Data Sources

### 1. Telemetry Events (`.deia/analytics/staging/events/`)

NDJSON format with bot demographics:
```json
{
  "timestamp": "2025-10-23T19:15:00Z",
  "task_id": "fix-session-logger-bug",
  "platform": "claude-code-cli",
  "vendor": "anthropic",
  "model": "claude-sonnet-4-5",
  "duration_seconds": 120,
  "cost_usd": 0.03,
  "success": true,
  "files_modified": 2,
  "test_results": {"passed": 10, "failed": 0}
}
```

### 2. Violations Log
```json
{
  "timestamp": "2025-10-23T19:20:00Z",
  "task_id": "fix-session-logger-bug",
  "bot_id": "CLAUDE-CODE-002",
  "platform": "claude-code-cli",
  "violation": "scope violation",
  "severity": "major"
}
```

### 3. Task Completion Records
From `.deia/bot-status-board.json` `completed_tasks_today`:
```json
{
  "backlog_id": "BACKLOG-015",
  "title": "Fix Unicode encoding in monitor.py",
  "completed_by": "BOT-00006",
  "completed_at": "2025-10-12T10:30:18",
  "duration_seconds": 300,
  "quality_score": 10,
  "platform": "claude-api",
  "vendor": "anthropic",
  "model": "claude-3-5-sonnet-20241022"
}
```

## ML Model

### Features (Input)
```python
task_features = {
    # Task characteristics
    "task_type": "bug_fix|feature|refactor|test|docs",
    "complexity": 1-10,  # Extracted from task description
    "file_count_estimate": int,
    "requires_testing": bool,
    "requires_external_api": bool,
    "code_language": "python|js|ts|rust|etc",

    # Contextual
    "time_of_day": hour (0-23),
    "current_workload": int,  # Tasks in queue
    "priority": 0-2  # P0=0, P1=1, P2=2
}
```

### Labels (Output)
```python
platform_options = [
    "claude-code-cli",
    "claude-api",
    "codex-cli",
    "llama-local",
    "gemini-api"
]
```

### Training Labels (What We Learn From)
```python
performance_metrics = {
    "duration_seconds": float,
    "cost_usd": float,
    "quality_score": 0-10,  # From test results, code review, human feedback
    "success": bool,
    "violation_count": int
}
```

### Neural Network Architecture
```python
import torch.nn as nn

class TaskRouter(nn.Module):
    def __init__(self, input_dim=20, hidden_dim=64, num_platforms=5):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, num_platforms),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.network(x)  # Returns probabilities per platform
```

### Training Objective
Minimize weighted loss:
```python
loss = (
    0.4 * time_penalty +      # Faster is better
    0.3 * cost_penalty +      # Cheaper is better
    0.3 * quality_reward      # Higher quality is better
)
```

## Orchestrator Bot Workflow

### 1. New Task Arrives
```python
task = {
    "title": "Fix bug in session_logger.py",
    "description": "Unicode error in monitor.py line 45",
    "priority": "P1",
    "files": ["src/deia/services/session_logger.py"]
}
```

### 2. Extract Features
```python
features = orchestrator.extract_features(task)
# {
#   "task_type": "bug_fix",
#   "complexity": 5,
#   "file_count_estimate": 1,
#   "requires_testing": True,
#   "code_language": "python"
# }
```

### 3. Query Model
```python
predictions = orchestrator.predict(features)
# {
#   "claude-code-cli": 0.85,
#   "claude-api": 0.10,
#   "codex-cli": 0.03,
#   "llama-local": 0.02
# }
```

### 4. Make Decision
```python
platform = "claude-code-cli"  # Highest confidence
confidence = 0.85

# Lookup historical stats for explanation
stats = orchestrator.get_stats(platform="claude-code-cli", task_type="bug_fix")
# {
#   "avg_duration_seconds": 120,
#   "avg_cost_usd": 0.03,
#   "avg_quality": 9.2,
#   "success_rate": 0.95
# }
```

### 5. Assign to Platform
```python
orchestrator.assign_task(
    task=task,
    platform="claude-code-cli",
    reason=f"Historical performance: {stats}"
)

# Writes to: .deia/hive/tasks/TASK-fix-session-logger.md
# Metadata includes: platform=claude-code-cli
```

### 6. Bot Picks Up Task
Any bot with `platform=claude-code-cli` can claim it:
- BOT-00002 (Claude Code CLI)
- BOT-00007 (Claude Code CLI)
- etc.

### 7. Track Performance
After completion, log results:
```python
orchestrator.record_outcome(
    task_id="fix-session-logger",
    platform="claude-code-cli",
    duration=115,
    cost=0.028,
    quality=10,
    success=True
)

# Adds to training dataset
# Model retrains nightly
```

## Feedback Loop

```
New Task → Orchestrator Predicts → Bot Executes → Log Results
              ↑                                          ↓
              └──────────── Retrain Model ←─────────────┘
                         (Nightly or after N tasks)
```

## Cold Start Problem

When the Orchestrator has no data:
1. **Round-robin** initial assignments across platforms
2. **Random exploration**: 10% of tasks assigned randomly to gather data
3. **Human override**: You can manually assign and Orchestrator learns from it

## Human Feedback Integration

Via dashboard:
```python
# After task completion, human rates quality
orchestrator.record_human_feedback(
    task_id="fix-session-logger",
    quality_score=9,  # 0-10 scale
    notes="Good fix, but could be more efficient"
)

# This becomes ground truth for training
```

## Implementation Files

```
src/deia/orchestrator.py           # Main Orchestrator class
src/deia/ml/task_router.py         # Neural network model
src/deia/ml/feature_extractor.py   # Feature extraction from tasks
src/deia/ml/trainer.py             # Training pipeline
src/deia/ml/data_loader.py         # Load telemetry for training

models/
├── task_router_v1.pt              # Trained model weights
└── scaler.pkl                     # Feature normalization

.deia/orchestrator/
├── training-data.jsonl            # Aggregated training data
├── model-performance.json         # Model accuracy metrics
└── routing-decisions.jsonl        # Log of all routing decisions
```

## API

```python
from deia.orchestrator import Orchestrator

orch = Orchestrator(work_dir=Path.cwd())

# Predict best platform for task
prediction = orch.predict_platform(task={
    "title": "Add feature X",
    "description": "...",
    "priority": "P1"
})

# prediction = {
#   "platform": "claude-code-cli",
#   "confidence": 0.85,
#   "reasoning": {
#     "avg_duration": 120,
#     "avg_cost": 0.03,
#     "avg_quality": 9.2,
#     "similar_tasks_completed": 45
#   }
# }

# Assign task with platform routing
orch.assign_task(task, platform=prediction["platform"])

# Record outcome after completion
orch.record_outcome(
    task_id="add-feature-x",
    platform="claude-code-cli",
    duration=130,
    cost=0.032,
    quality=9,
    success=True
)

# Retrain model
orch.retrain()
```

## Monitoring Dashboard Integration

Add Orchestrator panel to dashboard:
```
┌─────────────────────────────────────────────────┐
│  Orchestrator Stats                             │
│                                                 │
│  Total Tasks Routed: 1,234                     │
│  Model Accuracy: 87%                           │
│  Avg Confidence: 0.82                          │
│                                                 │
│  Platform Performance:                          │
│  • claude-code-cli: 120s avg, $0.03, 9.2/10   │
│  • claude-api: 90s avg, $0.05, 8.8/10         │
│  • llama-local: 180s avg, $0.00, 7.5/10       │
│                                                 │
│  Recent Predictions:                            │
│  [Table of recent routing decisions]           │
└─────────────────────────────────────────────────┘
```

## Success Metrics

1. **Routing Accuracy**: % of tasks where chosen platform performed best
2. **Cost Savings**: Total $ saved vs worst-case platform choices
3. **Time Savings**: Total time saved vs slowest platform
4. **Quality Improvement**: Avg quality score trend over time

## Initial Implementation Checklist

- [ ] Feature extraction from task markdown
- [ ] Data loader for telemetry NDJSON
- [ ] Neural network model (PyTorch)
- [ ] Training pipeline with validation split
- [ ] Inference API (predict platform)
- [ ] Task assignment with platform metadata
- [ ] Outcome recording to telemetry
- [ ] Nightly retrain job
- [ ] Dashboard integration

---

**Generated by:** CLAUDE-CODE-001
**Date:** 2025-10-23
**Status:** Specification Ready for Implementation
**Priority:** Build tonight alongside dashboard
