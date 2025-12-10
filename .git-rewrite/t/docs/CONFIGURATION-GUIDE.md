# DEIA Configuration Guide

**Version:** 1.0
**Last Updated:** 2025-10-25
**Status:** Complete

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Configuration File Format](#configuration-file-format)
3. [All Configuration Options](#all-configuration-options)
4. [Environment-Specific Configs](#environment-specific-configs)
5. [Default Fallbacks](#default-fallbacks)
6. [Hot Reload](#hot-reload)
7. [Validation](#validation)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Copy template to active config:

```bash
cp .deia/config/production.yaml bot-config.yaml
```

### 2. Customize for your environment:

```yaml
environment: "production"  # or "staging" or "development"
bot_limits:
  min_bots: 2
  max_bots: 10
```

### 3. System loads it automatically:

On startup, DEIA loads `bot-config.yaml` from working directory. If not found, uses production defaults.

---

## Configuration File Format

### Structure

```yaml
# Root level settings
version: "1.0"
environment: "production"
debug: false

# Nested configuration sections
thresholds:
  cpu_warning_percent: 0.80

# Feature flags
feature_flags:
  messaging_enabled: true
```

### File Location

- **Expected location:** `./bot-config.yaml` (project root)
- **Template location:** `.deia/config/production.yaml`
- **Example location:** `.deia/config/bot-config.example.yaml`

### File Format

- **Format:** YAML (`.yaml` or `.yml`)
- **Encoding:** UTF-8
- **Comments:** Use `#` for comments
- **Indentation:** 2 spaces (not tabs)

---

## All Configuration Options

### Root Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `version` | string | "1.0" | Config file format version |
| `environment` | string | "production" | Runtime environment: production, staging, development |
| `debug` | boolean | false | Enable debug logging (verbose output) |
| `log_level` | string | "INFO" | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

### Thresholds (Health Monitoring)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `thresholds.cpu_warning_percent` | float | 0.80 | CPU usage % when WARNING alert triggered (0-1) |
| `thresholds.cpu_critical_percent` | float | 0.95 | CPU usage % when CRITICAL alert triggered (0-1) |
| `thresholds.memory_warning_percent` | float | 0.75 | Memory usage % when WARNING alert triggered (0-1) |
| `thresholds.memory_critical_percent` | float | 0.90 | Memory usage % when CRITICAL alert triggered (0-1) |
| `thresholds.queue_backlog_threshold` | int | 10 | Task queue size when ALERT triggered |
| `thresholds.bot_failure_threshold` | float | 0.30 | Bot success rate when ALERT triggered (0-1) |
| `thresholds.message_failure_threshold` | int | 5 | Failed messages when ALERT triggered |

### Bot Limits

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `bot_limits.min_bots` | int | 1 | Minimum bots to maintain running |
| `bot_limits.max_bots` | int | 10 | Maximum bots to scale up to |
| `bot_limits.max_concurrent_tasks_per_bot` | int | 3 | Max tasks assigned to one bot |
| `bot_limits.port_range_start` | int | 8001 | First port for bot services |
| `bot_limits.port_range_end` | int | 8999 | Last port for bot services |

### Timeouts

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `timeouts.task_timeout_seconds` | int | 3600 | Max seconds per task (1 hour) |
| `timeouts.message_ttl_seconds` | int | 3600 | Message lifetime in seconds (1 hour) |
| `timeouts.bot_health_check_interval_seconds` | int | 30 | Health check frequency (30 sec) |
| `timeouts.scaling_evaluation_interval_seconds` | int | 60 | Scaling check frequency (1 min) |
| `timeouts.config_reload_check_interval_seconds` | int | 300 | Config reload check (5 min) |

### Feature Flags

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `feature_flags.messaging_enabled` | boolean | true | Enable bot-to-bot messaging |
| `feature_flags.adaptive_scheduling_enabled` | boolean | true | Enable ML-based task routing |
| `feature_flags.health_monitoring_enabled` | boolean | true | Enable real-time health dashboard |
| `feature_flags.auto_scaling_enabled` | boolean | true | Enable auto-scale bots up/down |
| `feature_flags.audit_logging_enabled` | boolean | true | Enable immutable audit trail |
| `feature_flags.graceful_degradation_enabled` | boolean | true | Enable graceful failure handling |
| `feature_flags.request_validation_enabled` | boolean | true | Enable request validation/security |
| `feature_flags.performance_profiling_enabled` | boolean | true | Enable performance tracking |

### Adaptive Learning

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `learning.learning_rate` | float | 0.1 | EMA weight for bot performance (0-1) |
| `learning.min_samples_for_recommendation` | int | 3 | Minimum tasks before routing recommendation |
| `learning.min_confidence_threshold` | float | 0.7 | Minimum confidence for recommendation (0-1) |
| `learning.reset_learning_on_major_version_change` | boolean | true | Reset performance history on upgrade |

### Persistence

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `persistence.backup_enabled` | boolean | true | Enable automatic backups |
| `persistence.backup_interval_minutes` | int | 10 | Backup frequency (10 min) |
| `persistence.backup_retention_days` | int | 7 | Keep backups for N days |
| `persistence.state_directory` | string | ".deia/state" | Directory for system state files |
| `persistence.log_directory` | string | ".deia/bot-logs" | Directory for log files |
| `persistence.config_directory` | string | ".deia/config" | Directory for config files |

### Disaster Recovery

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `disaster_recovery.enabled` | boolean | true | Enable disaster recovery |
| `disaster_recovery.recovery_checks_interval_seconds` | int | 60 | Check for recovery issues every 60 sec |
| `disaster_recovery.max_recovery_attempts` | int | 3 | Max recovery attempts per issue |
| `disaster_recovery.recovery_backoff_seconds` | int | 5 | Wait 5 sec between recovery attempts |

### Audit Logging

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `audit.enabled` | boolean | true | Enable audit logging |
| `audit.log_file` | string | ".deia/bot-logs/audit.jsonl" | Audit log file path |
| `audit.retention_days` | int | 90 | Keep audit logs for N days |
| `audit.include_sensitive_data` | boolean | false | Include passwords/tokens in logs (UNSAFE) |

### Custom Settings

Free-form section for application-specific configuration:

```yaml
custom:
  app_name: "DEIA Orchestration System"
  version: "1.0.0"
  slack_webhook: "https://hooks.slack.com/services/..."
  admin_email: "admin@example.com"
```

---

## Environment-Specific Configs

### Production

```yaml
environment: "production"
debug: false
bot_limits:
  min_bots: 2
  max_bots: 10
thresholds:
  cpu_critical_percent: 0.95
```

### Staging

```yaml
environment: "staging"
debug: false
bot_limits:
  min_bots: 1
  max_bots: 5
```

### Development

```yaml
environment: "development"
debug: true
log_level: "DEBUG"
bot_limits:
  min_bots: 1
  max_bots: 3
```

---

## Default Fallbacks

If config option not found or invalid, system uses these defaults:

```yaml
version: "1.0"
environment: "production"
debug: false
log_level: "INFO"

thresholds:
  cpu_warning_percent: 0.80
  cpu_critical_percent: 0.95
  memory_warning_percent: 0.75
  memory_critical_percent: 0.90
  queue_backlog_threshold: 10
  bot_failure_threshold: 0.30
  message_failure_threshold: 5

bot_limits:
  min_bots: 1
  max_bots: 10
  max_concurrent_tasks_per_bot: 3
  port_range_start: 8001
  port_range_end: 8999

timeouts:
  task_timeout_seconds: 3600
  message_ttl_seconds: 3600
  bot_health_check_interval_seconds: 30
  scaling_evaluation_interval_seconds: 60
  config_reload_check_interval_seconds: 300

feature_flags:
  messaging_enabled: true
  adaptive_scheduling_enabled: true
  health_monitoring_enabled: true
  auto_scaling_enabled: true
  audit_logging_enabled: true
  graceful_degradation_enabled: true
  request_validation_enabled: true
  performance_profiling_enabled: true

learning:
  learning_rate: 0.1
  min_samples_for_recommendation: 3
  min_confidence_threshold: 0.7
  reset_learning_on_major_version_change: true

persistence:
  backup_enabled: true
  backup_interval_minutes: 10
  backup_retention_days: 7
  state_directory: ".deia/state"
  log_directory: ".deia/bot-logs"
  config_directory: ".deia/config"

disaster_recovery:
  enabled: true
  recovery_checks_interval_seconds: 60
  max_recovery_attempts: 3
  recovery_backoff_seconds: 5

audit:
  enabled: true
  log_file: ".deia/bot-logs/audit.jsonl"
  retention_days: 90
  include_sensitive_data: false
```

---

## Hot Reload

Configuration reloads automatically every 5 minutes (configurable via `config_reload_check_interval_seconds`).

### To force reload:

1. Modify `bot-config.yaml`
2. Wait up to 5 minutes
3. Check logs for "Config reloaded" message
4. Verify changes applied: `curl http://localhost:8001/status | grep config`

### Safe to change at runtime:

- Feature flags (messaging_enabled, auto_scaling_enabled, etc.)
- Thresholds (cpu_critical_percent, queue_backlog_threshold, etc.)
- Timeouts (task_timeout_seconds, etc.)
- Custom settings

### NOT safe to change (requires restart):

- `port_range_start`/`port_range_end`
- `state_directory`/`log_directory`
- `environment` (production vs development)

---

## Validation

### Validate config before deployment:

```bash
python -c "
from deia.services.config_manager import ConfigManager
cm = ConfigManager('.')
config = cm.load_config('bot-config')
print('Config valid!' if config else 'Config invalid!')
"
```

### Common validation errors:

| Error | Fix |
|-------|-----|
| "Missing 'environment' field" | Add `environment: production` to root |
| "cpu_warning_percent must be 0-1" | Change `0.80` to float between 0 and 1 |
| "min_bots must be <= max_bots" | Ensure `min_bots: 1, max_bots: 10` |
| "Invalid YAML syntax" | Check indentation (2 spaces), no tabs |

---

## Examples

### Minimal Config

```yaml
version: "1.0"
environment: "production"
```

(Uses all defaults)

### High-Performance Config

```yaml
version: "1.0"
environment: "production"
debug: false

bot_limits:
  min_bots: 4
  max_bots: 20
  max_concurrent_tasks_per_bot: 5

timeouts:
  task_timeout_seconds: 7200  # 2 hours

thresholds:
  queue_backlog_threshold: 20

feature_flags:
  auto_scaling_enabled: true
  adaptive_scheduling_enabled: true
```

### Low-Resource Config

```yaml
version: "1.0"
environment: "development"

bot_limits:
  min_bots: 1
  max_bots: 2
  max_concurrent_tasks_per_bot: 1

feature_flags:
  auto_scaling_enabled: false
  health_monitoring_enabled: true

persistence:
  backup_enabled: false
```

### Custom Integration Config

```yaml
version: "1.0"
environment: "production"

custom:
  slack_webhook: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  admin_email: "ops@company.com"
  pagerduty_key: "YOUR_PAGERDUTY_KEY"
  datadog_api_key: "YOUR_DATADOG_KEY"
```

---

## Troubleshooting

### Config not loading

**Symptom:** System starts with defaults, ignores bot-config.yaml

**Solution:**
1. Verify file exists: `ls -la bot-config.yaml`
2. Verify YAML syntax: `python -m yaml bot-config.yaml`
3. Check logs: `tail -f .deia/bot-logs/system.jsonl | grep -i config`
4. Try minimal config to isolate issue

### Invalid threshold values

**Symptom:** Alert "Config validation failed"

**Solution:**
- Ensure thresholds are floats (0-1) for percentages
- Ensure thresholds are integers for queue/failure counts
- Example: `cpu_warning_percent: 0.80` (not `80`)

### Hot reload not working

**Symptom:** Changed config, but system still uses old values

**Solution:**
1. Check reload interval: Should reload within 5 minutes
2. Force restart: `pkill -f "python run_single_bot.py"` then restart
3. Verify file saved: `cat bot-config.yaml | grep setting_you_changed`

### Feature disabled but still active

**Symptom:** Set `messaging_enabled: false` but messaging still works

**Solution:**
1. Verify config reloaded: Check logs for "Config reloaded"
2. Check feature flag name: Exact spelling required
3. Force restart if needed

---

## Best Practices

1. **Version control:** Keep bot-config.yaml in git (don't commit secrets)
2. **Secrets management:** Use environment variables for credentials
3. **Testing:** Test config changes in staging before production
4. **Documentation:** Document your custom settings and why
5. **Monitoring:** Monitor config reload errors in logs
6. **Backup:** Keep backup of working config before making changes

---

**Status:** ✅ PRODUCTION READY

**Last Updated:** 2025-10-25 16:19 CDT
**Updated By:** BOT-001 (Infrastructure Lead)

For deployment help, see DEPLOYMENT-CHECKLIST.md
For troubleshooting, see TROUBLESHOOTING.md
