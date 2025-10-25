# DEIA Bot Controller - System Architecture

**Version:** 1.0
**Last Updated:** 2025-10-25
**Target Audience:** Architects, DevOps, Senior Engineers

---

## Executive Summary

DEIA Bot Controller is a multi-bot orchestration platform that manages concurrent bot instances with intelligent task routing, state management, and observability. The system is designed for high availability, horizontal scalability, and operational excellence.

**Key Characteristics:**
- Multi-bot orchestration with per-bot lifecycle management
- HTTP/WebSocket-based communication with real-time updates
- Persistent chat history and state management
- Modular architecture with pluggable components
- Production-ready monitoring and observability

---

## System Architecture Overview

### High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                     CLIENT TIER (Port 8000)                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Web UI (HTML/CSS/JavaScript)                              │  │
│  │  - Bot Control Panel                                       │  │
│  │  - Chat Interface                                          │  │
│  │  - Status Dashboard                                        │  │
│  │  - Configuration Management                               │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────┬───────────────────────────────────────────────────────┘
             │ HTTP/WebSocket (Port 8000)
             ▼
┌────────────────────────────────────────────────────────────────────┐
│                   APPLICATION TIER (Llama Chatbot)                 │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Web Server (Express/Node.js)                              │  │
│  │  ├─ Authentication & Authorization                         │  │
│  │  ├─ API Request Routing                                    │  │
│  │  ├─ WebSocket Connection Management                        │  │
│  │  └─ Middleware (CORS, Rate Limiting, Logging)              │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                                      │  │
│  │  ├─ Bot Manager (Launch, Stop, Status)                    │  │
│  │  ├─ Chat History Manager                                  │  │
│  │  ├─ Command Router                                        │  │
│  │  ├─ State Manager                                         │  │
│  │  └─ Event Emitter                                         │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────┬────────────────────────┬─┘
             │ Bot Process Management     │ Database Access        │
             │ (Spawn/Kill)              │                         │
             ▼                           ▼                         ▼
┌────────────────────────────────┐  ┌──────────────────┐  ┌──────────────┐
│  BOT INSTANCES                 │  │  DATABASE TIER   │  │  CACHE TIER  │
│  ┌──────────────────────────┐  │  │  (PostgreSQL)    │  │  (Redis)     │
│  │ BOT-001 (Port 8001)      │  │  │                  │  │              │
│  │ - Ollama Integration     │  │  │ ┌──────────────┐ │  │ ┌──────────┐ │
│  │ - Message Processing     │  │  │ │ chat_messages│ │  │ │ Sessions │ │
│  │ - Context Management     │  │  │ ├──────────────┤ │  │ ├──────────┤ │
│  └──────────────────────────┘  │  │ │ bots         │ │  │ │ Rate Lim │ │
│  ┌──────────────────────────┐  │  │ ├──────────────┤ │  │ ├──────────┤ │
│  │ BOT-002 (Port 8002)      │  │  │ │ bot_status  │ │  │ │ Cache    │ │
│  │ - Ollama Integration     │  │  │ ├──────────────┤ │  │ └──────────┘ │
│  │ - Message Processing     │  │  │ │ audit_logs  │ │  │              │
│  │ - Context Management     │  │  │ └──────────────┘ │  │              │
│  └──────────────────────────┘  │  │                  │  │              │
│  ┌──────────────────────────┐  │  │                  │  │              │
│  │ BOT-N (Port 8000+N)      │  │  │                  │  │              │
│  │ - Ollama Integration     │  │  │                  │  │              │
│  │ - Message Processing     │  │  │                  │  │              │
│  │ - Context Management     │  │  │                  │  │              │
│  └──────────────────────────┘  │  │                  │  │              │
│  (Up to 10 concurrent bots)    │  │                  │  │              │
└────────────────────────────────┘  └──────────────────┘  └──────────────┘
             │
             │ HTTP (Port 11434+)
             ▼
┌────────────────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES (Ollama/LLM Backend)                │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Ollama Service (localhost:11434)                           │  │
│  │  - Model Management (mistral, llama2, etc.)                │  │
│  │  - Inference Engine                                        │  │
│  │  - Context Window Management                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Client Tier

#### Web User Interface (Port 8000)
**Purpose:** User-facing interface for bot control and chat

**Components:**
- **Bot Control Panel**: Launch/stop bots, manage instances
- **Chat Interface**: Real-time message display and input
- **Status Dashboard**: Real-time monitoring of bot states
- **Configuration UI**: Bot parameters, advanced settings

**Technology Stack:**
- HTML5 for markup structure
- CSS3 for responsive styling (mobile-first)
- JavaScript (vanilla or frameworks) for interactivity
- WebSocket API for real-time updates
- Local Storage for session data

**Key Features:**
- Real-time status polling (3-second interval)
- Multi-tab chat history viewing
- Command autocompletion
- Error handling and user feedback
- Accessibility compliance (WCAG AA)

**Data Flow:**
```
User Input (UI) → HTTP Request/WebSocket → Server API
Server Response → WebSocket/HTTP → DOM Update → Visual Feedback
```

---

### 2. Application Tier

#### Web Server (Node.js/Express)

**Purpose:** Core application server handling requests and orchestrating business logic

**Main Responsibilities:**
1. **Request Handling**: HTTP/WebSocket request routing
2. **Authentication**: User session management
3. **Authorization**: Permission checking
4. **Business Logic**: Coordinating bot operations
5. **Data Persistence**: Database interactions
6. **Real-time Communication**: WebSocket broadcasts

**Architecture Pattern:** MVC with Service Layer
```
Client Request → Express Middleware
    ↓
Route Handler (Controller)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Database/Cache
```

#### API Endpoints

**Bot Management:**
```
POST   /api/bot/launch          - Launch new bot instance
GET    /api/bot/:id             - Get bot details
POST   /api/bot/:id/stop        - Stop bot
GET    /api/bots                - List all bots
GET    /api/bot/:id/status      - Get real-time status
```

**Chat Operations:**
```
POST   /api/chat/send           - Send message to bot
GET    /api/chat/:botId         - Get chat history
GET    /api/chat/:botId/:msgId  - Get specific message
POST   /api/chat/:botId/export  - Export chat history
DELETE /api/chat/:botId         - Clear chat history
```

**Health & Monitoring:**
```
GET    /health                  - Application health
GET    /health/db               - Database connectivity
GET    /health/cache            - Cache status
GET    /metrics                 - Prometheus metrics
GET    /logs/tail               - Stream recent logs
```

#### Core Services

**1. Bot Manager Service**
```javascript
// Pseudo-code
class BotManager {
  async launchBot(botId, config) {
    // Spawn child process
    // Configure Ollama connection
    // Initialize state
    // Update database
    // Return bot info
  }

  async stopBot(botId) {
    // Send graceful shutdown signal
    // Wait for cleanup
    // Close connections
    // Update database
  }

  async getBotStatus(botId) {
    // Check process alive
    // Get memory/CPU usage
    // Check Ollama connection
    // Return status
  }
}
```

**2. Chat History Manager Service**
```javascript
class ChatHistoryManager {
  async saveMessage(botId, message, sender) {
    // Validate message
    // Store in database
    // Update indexes
    // Clear expired cache
    // Emit event
  }

  async getHistory(botId, limit, offset) {
    // Check cache first
    // Query database if needed
    // Format response
    // Update cache
    return messages
  }
}
```

**3. Command Router Service**
```javascript
class CommandRouter {
  async routeCommand(botId, command, context) {
    // Validate command syntax
    // Check bot availability
    // Route to correct bot
    // Wait for response
    // Log result
    // Return response
  }
}
```

**4. State Manager Service**
```javascript
class StateManager {
  async getState(botId) {
    // Get from cache (fast path)
    // Fall back to database
    // Return state object
  }

  async updateState(botId, newState) {
    // Validate state
    // Update in-memory cache
    // Persist to database
    // Emit state-change event
  }
}
```

**5. Event Emitter**
```javascript
// Publish-Subscribe pattern for state changes
EventBus.on('bot:launched', (botId) => {
  // Update UI
  // Log event
  // Trigger monitoring
})

EventBus.on('message:received', (botId, message) => {
  // Store in history
  // Broadcast to connected clients
  // Update dashboard
})
```

---

### 3. Bot Instance Tier

#### Individual Bot Process (Port 8001+)

**Purpose:** Isolated subprocess for each bot with independent LLM context

**Architecture:**
```
Bot Instance (Child Process)
├── Ollama Connection Manager
│   └── HTTP client to localhost:11434
├── Message Queue
│   ├── Incoming messages (from parent)
│   └── Outgoing responses (to parent)
├── Context Manager
│   ├── System prompt
│   ├── Conversation history (in-memory)
│   └── Token counting
└── State Storage
    ├── Bot configuration
    ├── Current status
    └── Performance metrics
```

**Bot Process Lifecycle:**
```
1. INIT: Parent spawns child process
2. CONFIG: Load bot parameters and system prompt
3. READY: Connect to Ollama, report status as "ready"
4. ACTIVE: Accept and process messages
5. IDLE: No messages (keep-alive heartbeats)
6. SHUTDOWN: Graceful cleanup of resources
7. TERMINATED: Process exits
```

**Message Processing Flow:**
```
1. Receive message from parent process
2. Add to context manager (maintain conversation history)
3. Prepare prompt with context
4. Send to Ollama (HTTP request)
5. Stream response from Ollama
6. Parse and validate response
7. Send response back to parent
8. Update context and state
```

---

### 4. Data Persistence Tier

#### PostgreSQL Database

**Purpose:** Persistent storage of chat history, bot state, audit logs

**Schema:**

**Table: bots**
```sql
CREATE TABLE bots (
  id VARCHAR(50) PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  config JSONB,
  status VARCHAR(20),
  port INTEGER UNIQUE,
  process_id INTEGER,
  metadata JSONB
);
```

**Table: chat_messages**
```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY,
  bot_id VARCHAR(50) REFERENCES bots(id),
  sender VARCHAR(20), -- 'user' or 'bot'
  content TEXT,
  tokens INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB,

  INDEX idx_bot_created (bot_id, created_at DESC),
  INDEX idx_created (created_at DESC)
);
```

**Table: bot_status**
```sql
CREATE TABLE bot_status (
  bot_id VARCHAR(50) PRIMARY KEY REFERENCES bots(id),
  status VARCHAR(20),
  memory_mb INTEGER,
  cpu_percent FLOAT,
  uptime_seconds INTEGER,
  last_message TIMESTAMP,
  error_count INTEGER,
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Table: audit_logs**
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  bot_id VARCHAR(50) REFERENCES bots(id),
  action VARCHAR(50),
  user_id VARCHAR(50),
  details JSONB,
  created_at TIMESTAMP DEFAULT NOW(),

  INDEX idx_bot_action (bot_id, action, created_at DESC)
);
```

**Data Relationships:**
```
bots (1) ──────── (N) chat_messages
  │
  ├─── bot_status (1:1)
  └─── audit_logs (1:N)
```

**Retention Policies:**
- Chat messages: 90 days (configurable)
- Audit logs: 180 days (compliance requirement)
- Bot status: 7 days (operational data only)

---

### 5. Caching Tier

#### Redis Cache

**Purpose:** High-speed data access for frequently requested items

**Cache Keys & Data Types:**

```
# Session cache (Hash)
session:{sessionId}
├── userId: string
├── loginTime: timestamp
└── expiresAt: timestamp (TTL: 24 hours)

# Bot status (String with TTL)
bot:status:{botId}
└── {"status": "running", "port": 8001, ...} (TTL: 3 seconds)

# Chat history pagination (Sorted Set)
chat:{botId}:messages
├── members: message IDs
├── scores: timestamps
└── (TTL: 24 hours, size-limited to 10K messages)

# Rate limiting (Counter)
ratelimit:{clientIp}
└── counter: integer (TTL: 1 minute)
└── Incremented per request, checked against limit

# Feature flags (Hash)
feature:flags
├── enableAnalytics: boolean
├── enableExperimental: boolean
└── (No TTL, update on deployment)
```

**Cache Invalidation Strategy:**
```
On Message Received:
  1. Invalidate chat history cache
  2. Invalidate bot status cache (3s TTL handles this)
  3. Update message count

On Bot State Change:
  1. Invalidate bot status cache
  2. Invalidate bot list cache
  3. Notify all connected clients

On Configuration Update:
  1. Invalidate feature flags cache
  2. Invalidate settings cache
```

---

## Data Flow Architecture

### Message Flow Diagram

```
USER                           SERVER                         BOT/OLLAMA
  │                              │                               │
  │─── 1. Send Message ─────────>│                               │
  │                              │                               │
  │                              │─ 2. Validate ─────────────────│
  │                              │                               │
  │                              │<─ 3. Send to Ollama ──────────│
  │                              │                               │
  │                              │<─ 4. Stream Response ─────────│
  │                              │                               │
  │<──── 5. Response Update ─────│                               │
  │                              │                               │
  │                              │─ 6. Save to Database ────────│
  │                              │                               │
  │                              │─ 7. Emit Event ─────────────│
  │                              │                               │
  │<──── 8. WebSocket Broadcast ─│                               │
```

### State Transition Diagram

```
┌─────────┐
│  IDLE   │ (Initial state)
└────┬────┘
     │ Launch command
     ▼
┌─────────────┐
│   STARTING  │ (Spawning process)
└────┬────────┘
     │ Process spawned, connect to Ollama
     ▼
┌─────────────┐
│   READY     │ (Connected, waiting for messages)
└────┬────────┘
     │ Message received
     ▼
┌─────────────┐
│  PROCESSING │ (Sending to Ollama, waiting response)
└────┬────────┘
     │ Response received
     ▼
┌─────────────┐
│   ACTIVE    │ (Message processed, ready for more)
└────┬────────┘
     │ No message (timeout) OR Idle time exceeded
     ▼
┌─────────────┐
│    IDLE     │ (Waiting for next message)
└────┬────────┘
     │ Stop command
     ▼
┌──────────────┐
│  STOPPING    │ (Graceful shutdown)
└────┬─────────┘
     │ Cleanup complete
     ▼
┌──────────────┐
│  TERMINATED  │ (Process exited)
└──────────────┘
```

---

## Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Node.js | 16+ | Server runtime |
| **Framework** | Express.js | 4.x | Web server & routing |
| **Database** | PostgreSQL | 12+ | Persistent data storage |
| **Cache** | Redis | 6+ | Session & data cache |
| **Process Management** | Child Process | Built-in | Bot instance management |
| **HTTP Client** | Axios/Fetch | Latest | Ollama API communication |
| **WebSocket** | Socket.IO | 4.x | Real-time client updates |
| **Logging** | Winston | 3.x | Structured logging |
| **Monitoring** | Prometheus | Latest | Metrics collection |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Markup** | HTML5 | Structure |
| **Styling** | CSS3 | Layout & theming |
| **Scripting** | JavaScript (Vanilla) | Interactivity |
| **Real-time** | WebSocket API | Live updates |
| **Storage** | LocalStorage | Client-side state |

### External Services

| Service | Version | Protocol | Purpose |
|---------|---------|----------|---------|
| **Ollama** | 0.1+ | HTTP REST | LLM inference |
| **System** | Linux/macOS/Windows | OS-level | Process management |

### Development & DevOps

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **Docker** | Containerization |
| **systemd** | Service management (Linux) |
| **nginx** | Reverse proxy (optional) |
| **ELK Stack** | Centralized logging |
| **Prometheus/Grafana** | Monitoring & visualization |

---

## Scalability & Performance

### Horizontal Scaling

**Current Limits:**
- Max concurrent bots: 10 per server (configurable)
- Bot startup time: 2-5 seconds
- Message latency: 50-500ms (depends on LLM inference)
- Memory per bot: 100-200MB

**Scaling Strategy (Future):**
```
Single Server (Current)
├── App Server (8000)
├── Bots 1-10 (8001-8010)
└── Database (shared)

Multi-Server (Future)
├── Load Balancer
│   ├── App Server 1 (8000)
│   │   └── Bots 1-5
│   ├── App Server 2 (8000)
│   │   └── Bots 6-10
│   └── App Server N
│       └── Bots N*5+1 to (N+1)*5
├── PostgreSQL Cluster (Primary + Replicas)
└── Redis Cluster (Distributed caching)
```

### Performance Characteristics

**Expected Response Times:**
```
Health Check:          <50ms
Message Send:          50-500ms (LLM dependent)
Chat History Load:     <100ms (from cache)
Bot Launch:            2-5 seconds
Status Update:         <100ms
```

**Resource Usage:**
```
Idle State:
- CPU: 5-10%
- Memory: 300-400MB

Active (5 bots):
- CPU: 40-60%
- Memory: 1.2-1.5GB

Peak (10 bots):
- CPU: 80-95%
- Memory: 2.0-2.5GB
```

---

## Security Architecture

### Authentication & Authorization

```
┌──────────────────────────────────────────┐
│ HTTP Request                             │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│ Extract JWT Token from Header            │
│ (Bearer token in Authorization header)   │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│ Verify Token Signature & Expiration       │
│ (Using secret key)                       │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│ Extract User ID & Permissions from Token │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│ Check User Has Permission for Resource   │
│ (Role-based access control)              │
└────────────┬─────────────────────────────┘
             │
             ▼ Authorized / Not Authorized
```

### Data Security

- **In Transit**: TLS/SSL (HTTPS)
- **At Rest**: Database encryption, encrypted backups
- **Secrets**: Stored in vault (AWS Secrets Manager, HashiCorp Vault)
- **API Keys**: Hashed and salted
- **Chat History**: No PII logging

### Network Security

```
┌─────────────────────────────────────────┐
│ Firewall (Inbound Rules)                │
├─────────────────────────────────────────┤
│ Port 80/443 (HTTPS)      │ Allowed      │
│ Port 22 (SSH)            │ Allowed (key)│
│ Port 3306 (MySQL)        │ Denied       │
│ Port 5432 (PostgreSQL)   │ Denied       │
│ Port 6379 (Redis)        │ Denied       │
│ Port 8000-8010           │ Internal     │
│ All other ports          │ Denied       │
└─────────────────────────────────────────┘
```

---

## Monitoring & Observability

### Metrics Collection

**Application Metrics:**
```
# HTTP Request Metrics
http_requests_total{method, status, endpoint}
http_request_duration_seconds{quantile, endpoint}
http_request_size_bytes{quantile, endpoint}

# Bot Metrics
bot_instances_total{status}
bot_startup_duration_seconds{quantile}
bot_message_processing_duration_seconds{quantile}

# Database Metrics
db_connection_pool_size{status}
db_query_duration_seconds{query_type}
db_transaction_errors_total

# Cache Metrics
cache_hits_total
cache_misses_total
cache_evictions_total
```

### Logging Strategy

```
Application Logs
├── Request logs (who, what, when, where)
├── Error logs (stack traces, context)
├── Audit logs (user actions, state changes)
└── Performance logs (slow queries, delays)

Structured Logging Format:
{
  "timestamp": "2025-10-25T18:30:00Z",
  "level": "INFO",
  "service": "bot-controller",
  "botId": "BOT-001",
  "action": "message.processed",
  "duration_ms": 250,
  "tokens": 45,
  "userId": "user123"
}
```

### Alerting Rules

```
CRITICAL:
- Service down (no response for 1 min)
- Database unreachable
- Disk space < 5%

WARNING:
- CPU > 80% for 5 min
- Memory > 85%
- Error rate > 1%
- Response time > 2 sec

INFO:
- Bot launched/stopped
- High memory usage (normal during inference)
- Deployment events
```

---

## Deployment Architecture

### Environment Separation

```
Development
├── Feature branches (git)
├── Local database (SQLite/Docker)
├── Max 2 concurrent bots
└── Full logging & debugging

Staging
├── Main branch (git)
├── Staging database (PostgreSQL)
├── Full bot capabilities
└── Performance testing allowed

Production
├── Tagged releases (git tags)
├── Production database (PostgreSQL cluster)
├── Full bot capabilities
├── Zero-downtime deployments
└── Audit logging enabled
```

### CI/CD Pipeline

```
Code Push → Git Hook
    ↓
GitHub Actions
    ├─ Run Tests
    ├─ Run Linter
    ├─ Build
    ├─ Security Scan
    └─ Deploy to Staging

Staging Validation
    ├─ Integration Tests
    ├─ Performance Tests
    ├─ Security Tests
    └─ Manual QA Sign-off

Deploy to Production
    ├─ Create Backup
    ├─ Blue-Green Deployment
    ├─ Health Checks
    ├─ Smoke Tests
    └─ Monitor (1 hour)
```

---

## Reliability & Disaster Recovery

### Failure Scenarios & Handling

| Scenario | Impact | Recovery Time | Action |
|----------|--------|---|--------|
| Bot Process Crash | Single bot down | 2-5s | Auto-restart |
| Database Connection Lost | All operations fail | 10-30s | Reconnect with retry |
| Ollama Service Down | LLM inference fails | 5-30s | Queue messages, retry |
| Memory Leak | Server degrades | 5-10 min | Auto-restart service |
| Disk Full | No new logs, errors | <5 min | Archive logs, alert |
| Network Partition | Client disconnects | <5 min | Auto-reconnect |

### Backup Strategy

```
Hourly Backups
├── Database snapshots (keep 24)
└── Incremental WAL logs

Daily Backups
├── Full database dump
├── Application config
└── Audit logs

Weekly Backups
├── Full system snapshot
└── Off-site copy (AWS S3)

Retention
├── Hourly: 24 hours
├── Daily: 30 days
├── Weekly: 52 weeks
└── Yearly: Indefinite (compliance)
```

---

## Future Architecture Enhancements

### Phase 2: Multi-Server

```
Load Balancer (Nginx)
├── App Server 1 (Primary)
├── App Server 2 (Secondary)
└── Database Cluster (PostgreSQL)

Features:
- Session replication
- Shared cache (Redis cluster)
- Database replication
- Load balancing strategies
```

### Phase 3: Advanced Features

```
Message Queue (RabbitMQ/Kafka)
├── Async message processing
├── Dead letter queue
└── Message replay capability

Service Mesh (Istio)
├── Circuit breaker
├── Rate limiting
├── Distributed tracing
└── Service-to-service auth

API Gateway
├── Rate limiting per user
├── Request validation
├── Response transformation
└── API versioning
```

---

## Summary

**Architecture Type:** Modular, Service-Oriented
**Scalability:** Horizontal (future), Vertical (current)
**Reliability:** 99.5% uptime target
**Technology:** Node.js + PostgreSQL + Redis + Ollama
**Deployment:** Docker + systemd + CI/CD Pipeline

The DEIA Bot Controller is built on proven technologies and architectural patterns designed for reliability, observability, and future scalability. All components are documented and monitored for operational excellence.

---

**Last Updated:** 2025-10-25
**Architecture Status:** ✅ Production-Ready
