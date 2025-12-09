# DEIA Services

**Modular services powering the DEIA ecosystem.**

DEIA Services provide the core functionality for knowledge management, document routing, session logging, and multi-agent coordination.

---

## Service Categories

### Core Services (Production-Ready)

| Service | Description | Coverage |
|---------|-------------|----------|
| [Context Loader](CONTEXT-LOADER.md) | Multi-source context assembly | 90% |
| [Session Logger](SESSION-LOGGER.md) | Session tracking and analytics | 86% |
| [Master Librarian](MASTER-LIBRARIAN.md) | Knowledge curation and quality validation | 87% |
| [Enhanced BOK Search](ENHANCED-BOK-SEARCH.md) | TF-IDF + fuzzy pattern search | 48% |
| [Query Router](QUERY-ROUTER.md) | Intelligent query routing | 82% |
| [Project Browser](PROJECT-BROWSER.md) | Project exploration and navigation | 89% |
| [Downloads Monitor](DOWNLOADS-MONITOR.md) | File routing from Downloads | 90% |

### Infrastructure Services

| Service | Description | Status |
|---------|-------------|--------|
| [Health Check System](HEALTH-CHECK-SYSTEM.md) | System monitoring and health | Active |
| [Agent Coordinator](AGENT-COORDINATOR.md) | Multi-agent task coordination | Active |
| Path Validator | Security layer for path validation | 96% |
| File Reader | Safe file reading with encoding detection | 86% |

### Bot Management Services

| Service | File | Description |
|---------|------|-------------|
| Bot Health Monitor | `bot_health_monitor.py` | Monitor bot health metrics |
| Bot Activity Logger | `bot_activity_logger.py` | Log bot activities to JSONL |
| Bot Resource Monitor | `bot_resource_monitor.py` | Track resource usage |
| Bot Circuit Breaker | `bot_circuit_breaker.py` | Prevent cascade failures |
| Bot Load Manager | `bot_load_manager.py` | Distribute workload |
| Bot Auto Scaler | `bot_auto_scaler.py` | Scale bots based on demand |
| Bot Messenger | `bot_messenger.py` | Inter-bot communication |

### Analytics & Observability

| Service | File | Description |
|---------|------|-------------|
| Analytics Collector | `analytics_collector.py` | Collect system analytics |
| Queue Analytics | `queue_analytics.py` | Task queue metrics |
| Anomaly Detector | `anomaly_detector.py` | Detect system anomalies |
| Error Analyzer | `error_analyzer.py` | Analyze error patterns |
| Failure Analyzer | `failure_analyzer.py` | Root cause analysis |
| Heatmap Generator | `heatmap_generator.py` | Visual analytics |
| Performance Profiler | `performance_profiler.py` | Performance metrics |

### Enterprise Features

| Service | File | Description |
|---------|------|-------------|
| Service Factory | `service_factory.py` | Service instantiation |
| Service Mesh | `service_mesh.py` | Service communication |
| Rate Limiter | `rate_limiter.py` | Request throttling |
| Auth Manager | `auth_manager.py` | Authentication |
| Audit Logger | `audit_logger.py` | Audit trail |
| Feature Flags | `feature_flags.py` | Feature toggles |
| Disaster Recovery | `disaster_recovery.py` | Recovery procedures |

---

## Quick Start

### Using Core Services

```python
from deia.services.context_loader import ContextLoader
from deia.services.session_logger import SessionLogger
from deia.services.master_librarian import MasterLibrarian

# Load context from multiple sources
loader = ContextLoader(project_root='/path/to/project')
context = loader.load_context()

# Log session activity
logger = SessionLogger(session_id='session-001')
logger.log_event('task_started', {'task': 'documentation'})

# Query the knowledge base
librarian = MasterLibrarian(bok_path='/path/to/bok')
results = librarian.query('error handling patterns')
```

### Using Downloads Monitor (CLI)

```bash
# Watch Downloads folder interactively
deia sync

# Process existing files once
deia sync --once
```

### Using BOK Search (CLI)

```bash
# Search patterns
deia bok search "testing patterns" --fuzzy

# Query through librarian
deia librarian query "deployment best practices"
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Commands                         │
│  (deia sync, deia bok, deia librarian, deia log)       │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Core Services                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Context    │  │   Session    │  │    Master    │  │
│  │   Loader     │  │   Logger     │  │  Librarian   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Enhanced   │  │    Query     │  │  Downloads   │  │
│  │  BOK Search  │  │   Router     │  │   Monitor    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Infrastructure Services                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    Path      │  │    File      │  │   Health     │  │
│  │  Validator   │  │   Reader     │  │   Check      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                 Storage Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   .deia/     │  │     BOK      │  │   Sessions   │  │
│  │   config     │  │   patterns   │  │    logs      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Service Dependencies

```
Master Librarian
    └── Enhanced BOK Search
    └── Query Router
    └── Path Validator

Downloads Monitor
    └── Path Validator
    └── File Reader

Session Logger
    └── Context Loader
    └── Path Validator

Health Check System
    └── All services (monitors health)
```

---

## Configuration

Services are configured via `~/.deia/config.json`:

```json
{
  "projects": {
    "project-name": "/path/to/project"
  },
  "sync": {
    "downloads_folder": "/Users/you/Downloads",
    "use_temp_staging": true
  },
  "bok": {
    "path": "/path/to/bok",
    "search_fuzzy_threshold": 0.6
  },
  "logging": {
    "sessions_path": ".deia/sessions",
    "auto_log": false
  }
}
```

---

## Test Coverage Summary

| Service | Coverage | Tests |
|---------|----------|-------|
| Path Validator | 96% | P0 |
| Context Loader | 90% | 20+ |
| Downloads Monitor | 90% | 38 |
| Project Browser | 89% | 19 |
| Master Librarian | 87% | 46 |
| Session Logger | 86% | Core |
| File Reader | 86% | Core |
| Query Router | 82% | Core |
| Enhanced BOK Search | 48% | Core |

**Overall test coverage:** 38% (276+ tests passing)

---

## Adding New Services

1. Create service file in `src/deia/services/`
2. Follow existing patterns (class-based, type hints, docstrings)
3. Add tests in `tests/unit/test_<service>.py`
4. Document in `docs/services/<SERVICE>.md`
5. Target >80% test coverage

### Service Template

```python
"""
Service Name - Brief description.

Features:
- Feature 1
- Feature 2
"""

from typing import Dict, List, Optional
from pathlib import Path


class ServiceName:
    """Main service class."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize service.

        Args:
            config_path: Optional path to config file
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration."""
        # Implementation
        pass

    def main_method(self, input_data: str) -> Dict:
        """
        Main service method.

        Args:
            input_data: Input to process

        Returns:
            Processing results
        """
        # Implementation
        pass
```

---

## Related Documentation

- [Installation Guide](../../INSTALLATION.md) - Setup instructions
- [Sync Usage Guide](../guides/SYNC-USAGE-GUIDE.md) - Document routing
- [BOK Usage Guide](../guides/BOK-USAGE-GUIDE.md) - Knowledge search
- [Conversation Logging Guide](../guides/CONVERSATION-LOGGING-GUIDE.md) - Session capture

---

**Last Updated:** 2025-11-26
**Status:** Production-ready core services
