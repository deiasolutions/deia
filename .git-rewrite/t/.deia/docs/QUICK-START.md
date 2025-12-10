# Quick Start Guide
**Created by:** BOT-001
**Date:** 2025-10-25
**Duration:** 5 minutes

---

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Docker (optional)
- Git

## Setup (5 minutes)

### 1. Clone & Enter (30 seconds)
```bash
git clone https://github.com/deiasolutions/deiasolutions.git
cd deiasolutions
```

### 2. Create Environment (30 seconds)
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### 4. Setup Database (1 minute)
```bash
python -m alembic upgrade head
```

### 5. Run Application (30 seconds)
```bash
python run.py
```

Visit: `http://localhost:8000`

---

## First Commands

Launch a bot:
```bash
curl -X POST http://localhost:8001/api/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "test-bot"}'
```

Check status:
```bash
curl http://localhost:8001/health
```

Send command:
```bash
curl -X POST http://localhost:8001/api/message \
  -H "Content-Type: application/json" \
  -d '{"content": "hello"}'
```

---

## Docker Quick Start

```bash
docker-compose up
```

Runs:
- Application on port 8000
- Bot service on port 8001
- PostgreSQL on port 5432
- Redis on port 6379

---

## Key Files

- `src/deia/services/bot_service.py` - Main API
- `src/deia/adapters/web/app.py` - Web interface
- `requirements.txt` - Dependencies
- `.env` - Configuration
- `Dockerfile` - Container definition

---

## Next Steps

1. Read `CONFIGURATION-GUIDE.md` for detailed setup
2. Read `USER-GUIDE.md` for bot usage
3. Read `API-REFERENCE.md` for API endpoints
4. Check `TROUBLESHOOTING-GUIDE.md` for common issues

---

## Support

- Docs: `deiasolutions/docs/`
- Issues: GitHub Issues
- Logs: `/var/log/app.log`
