# Configuration Guide
**Created by:** BOT-001
**Date:** 2025-10-25
**Status:** QUICK REFERENCE

---

## Environment Variables

Create `.env` file in project root with:

```bash
# Application
APP_NAME=DEIA-SOLUTIONS
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# Server
PORT=8000
HOST=0.0.0.0
WORKERS=4

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/deia
DATABASE_POOL_SIZE=20
DATABASE_TIMEOUT=30

# Redis (if using)
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-256-bit-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Bot Service
BOT_SERVICE_PORT=8001
BOT_SERVICE_HOST=localhost

# Monitoring
SENTRY_DSN=https://your-sentry-dsn

# Email (if sending emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=app-specific-password

# File Storage
UPLOAD_DIR=/tmp/uploads
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes

# API Configuration
API_RATE_LIMIT=100
API_RATE_WINDOW=3600

# Logging
LOG_FORMAT=json
LOG_FILE=/var/log/app.log
```

## Configuration by Environment

### Development
```bash
APP_ENV=development
DEBUG=true
LOG_LEVEL=debug
DATABASE_URL=postgresql://dev:dev@localhost:5432/deia_dev
```

### Staging
```bash
APP_ENV=staging
DEBUG=false
LOG_LEVEL=info
DATABASE_URL=postgresql://staging:pass@db.staging.internal:5432/deia
SENTRY_DSN=https://staging-key@sentry.io/project
```

### Production
```bash
APP_ENV=production
DEBUG=false
LOG_LEVEL=warn
DATABASE_URL=postgresql://prod:complex-password@db.prod.internal:5432/deia
SENTRY_DSN=https://prod-key@sentry.io/project
JWT_SECRET=very-long-random-256-bit-secret
```

## Optional Settings

### Enable Redis Caching
```bash
REDIS_ENABLED=true
REDIS_URL=redis://:password@localhost:6379/0
CACHE_TTL=3600
```

### Enable Email Notifications
```bash
EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_USER=alerts@example.com
```

### Enable Monitoring
```bash
MONITORING_ENABLED=true
PROMETHEUS_PORT=9090
DATADOG_API_KEY=your-key
```

## Configuration File (config.yml)

Alternative to environment variables:

```yaml
application:
  name: DEIA-SOLUTIONS
  environment: production
  debug: false

server:
  port: 8000
  host: 0.0.0.0
  workers: 4
  timeout: 30

database:
  url: postgresql://user:pass@localhost:5432/deia
  pool_size: 20
  ssl: true

logging:
  level: info
  format: json
  file: /var/log/app.log
  max_size: 100M
  backup_count: 10
```

## Verification Checklist

- [ ] .env file created and populated
- [ ] Database credentials correct
- [ ] JWT secret set to random 256-bit value
- [ ] LOG_LEVEL appropriate for environment
- [ ] SENTRY_DSN configured (production only)
- [ ] All required vars have values
- [ ] No secrets committed to git

## Common Issues

**Port already in use:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Database connection failed:**
- Check DATABASE_URL is correct
- Verify database is running
- Check network connectivity
- Verify credentials

**Application won't start:**
- Check DEBUG=false (if error output hidden)
- Check LOG_LEVEL to see detailed logs
- Check all required env vars are set

---

## Sign-Off

Configuration guide completed.
Ready for deployment with proper environment setup.
