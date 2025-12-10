# Efemera-Social-Edge-Graft-Outer-Egg-v0.1.md
---

deia_routing:
  project: efemera
  destination: docs/projects/
  filename: Efemera-Social-Edge-Graft-Outer-Egg-v0.1.md
  action: incubate
version: 0.1
last_updated: 2025-10-14
created_by: GPT-5 Thinking (Efemera Eggsmith)
linked_subsystems:
  - DEIA-Orchestrator
  - Observability
  - EdgeGraft-UI
integrity:
  checksum: sha256:pending
repot_pointers:
  index: docs/REPOT.md
  process: docs/process/EFEMERA-DEV-PROCESS.md
  runtime_home: web/efemera-edge-graft/
  eggs_home: docs/projects/
license: MIT
---

# Efemera  Social Edge Graft (Outer Egg v0.1)

## 1) Executive Summary
This Egg hatches a full, local-first **Efemera** development workspace  **server + nodes**  in one command.  
Targets on day one:
- **Server (TypeScript + Fastify + WebSocket + MQTT bridge)**
- **Nodes**: **React Native (Expo) for iOS/Android**, **Alexa Skill scaffold**, and **IoT Mesh (MQTT) bridge** for devices like eero-style sensors.
It sets up **pnpm workspaces**, **Docker (Postgres + Mosquitto)**, **observability (JSONL telemetry + window.EdgeAPI seam)**, and **DEIA session logging hooks**.

> Hatch flow: `bash hatch.sh`  scaffold monorepo  install  start database/broker  run server & mobile & bridges.

---

## 2) Repo Layout (generated)
```

efemera/
 apps/
   server/                 # Fastify REST + WS + MQTT bridge
   mobile/                 # React Native (Expo) app for iOS/Android
   alexa/                  # Alexa Skill (ASK SDK) scaffold
 services/
   edge-bridge/            # MQTT <-> WS bridge & device simulators
 packages/
   edge-api/               # shared client SDK (browser/node/react-native)
   telemetry/              # JSONL logger & schema
 observability/
   telemetry.schema.json
   examples/
 docker/
   docker-compose.yml      # postgres + mosquitto
   initdb/                 # optional SQL init
 scripts/
   dev.sh                  # all-in dev (server, mobile, bridge)
   seed.ts                 # seed demo data
 .env.example
 pnpm-workspace.yaml
 package.json
 turbo.json
 README.md

````

---

## 3) Minimal Domain & APIs (v0.1)
### 3.1 Core objects
- **Edge** (human user devices)  
- **Node** (brand/bot endpoints: server bots, skills, services)  
- **Activity** (posts/requests/signals) with provenance & consent

### 3.2 REST (server)
- `POST /v1/session`  issue dev token
- `GET /v1/health`  health probe
- `POST /v1/activity`  create activity
- `GET /v1/activity/stream` (SSE)  live feed (alt to WS for quick tests)

### 3.3 WebSocket
- `wss://host/ws`  bidirectional activities, presence, consent_change events

### 3.4 MQTT Topics (IoT)
- `efemera/edges/{edgeId}/events`
- `efemera/nodes/{nodeId}/commands`
- `efemera/broadcast`

### 3.5 Observability & AI Test Hooks
- **Telemetry JSONL events:** `session_start`, `activity_post`, `request_sent`, `response_rcvd`, `consent_change`, `moderation_flag`, `error`, `frame`
- **Browser seam:** `window.EdgeAPI`  
  Methods: `setController(fn)`, `clearController()`, `getState()`, `stepOnce()`  
  State snapshot: edges/nodes present, pending activities, consent states
- **Acceptance hook:** CLI key to emit/download `telemetry.jsonl` (server: `/debug/telemetry`)

---

## 4) Telemetry JSONL (schema excerpt)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Efemera Telemetry",
  "type": "object",
  "required": ["ts","event","ctx"],
  "properties": {
    "ts": {"type":"string","format":"date-time"},
    "event": {"type":"string","enum":[
      "session_start","activity_post","request_sent","response_rcvd",
      "consent_change","moderation_flag","error","frame"
    ]},
    "ctx": {
      "type":"object",
      "properties":{
        "edgeId":{"type":"string"},
        "nodeId":{"type":"string"},
        "sessionId":{"type":"string"},
        "kpi":{"type":"object"}
      }
    },
    "data": {"type":"object"}
  }
}
````

---

## 5) Hatch Scripts (one-shot bootstrap)

> **Run:** `bash hatch.sh` from the directory where you saved this Egg.

```bash
# hatch.sh
set -euo pipefail

# 1) Create repo root
ROOT_DIR="efemera"
mkdir -p "$ROOT_DIR"
cd "$ROOT_DIR"

# 2) Node toolchain
echo '{
  "name": "efemera",
  "private": true,
  "packageManager": "pnpm@9.12.0",
  "scripts": {
    "bootstrap": "pnpm i && pnpm -r build",
    "dev": "bash scripts/dev.sh",
    "server": "pnpm --filter @efemera/server dev",
    "mobile": "pnpm --filter @efemera/mobile start",
    "bridge": "pnpm --filter @efemera/edge-bridge dev",
    "db:up": "docker compose -f docker/docker-compose.yml up -d",
    "db:down": "docker compose -f docker/docker-compose.yml down -v"
  }
}' > package.json

cat > pnpm-workspace.yaml << 'YAML'
packages:
  - "apps/*"
  - "services/*"
  - "packages/*"
YAML

cat > turbo.json << 'JSON'
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": { "outputs": ["dist/**"] },
    "dev": { "cache": false }
  }
}
JSON

mkdir -p apps/server src_tmp apps/mobile apps/alexa services/edge-bridge packages/edge-api packages/telemetry observability/examples docker/initdb scripts

# 3) Env & Docker
cat > .env.example << 'ENV'
POSTGRES_USER=efemera
POSTGRES_PASSWORD=efemera
POSTGRES_DB=efemera
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
MQTT_HOST=localhost
MQTT_PORT=1883
SERVER_PORT=8080
ENV

cat > docker/docker-compose.yml << 'YAML'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: efemera
      POSTGRES_PASSWORD: efemera
      POSTGRES_DB: efemera
    ports: [ "5432:5432" ]
    volumes:
      - dbdata:/var/lib/postgresql/data
      - ./initdb:/docker-entrypoint-initdb.d
  mqtt:
    image: eclipse-mosquitto:2
    ports: [ "1883:1883", "9001:9001" ]
    volumes:
      - mosq:/mosquitto
volumes:
  dbdata:
  mosq:
YAML

# 4) Shared telemetry package
cat > packages/telemetry/package.json << 'JSON'
{
  "name": "@efemera/telemetry",
  "version": "0.0.1",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": { "build": "tsc -p tsconfig.json" },
  "devDependencies": { "typescript": "^5.4.0" }
}
JSON

cat > packages/telemetry/tsconfig.json << 'JSON'
{ "compilerOptions": { "outDir":"dist","declaration":true,"target":"ES2020","module":"CommonJS","strict":true } }
JSON

cat > packages/telemetry/src/index.ts << 'TS'
import { appendFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
type EventName = "session_start"|"activity_post"|"request_sent"|"response_rcvd"|"consent_change"|"moderation_flag"|"error"|"frame";
export function logEvent(path:string, event:EventName, ctx:Record<string,unknown>, data:Record<string,unknown>={}, ts=new Date()){
  const rec = { ts: ts.toISOString(), event, ctx, data };
  mkdirSync(dirname(path), { recursive: true });
  appendFileSync(path, JSON.stringify(rec)+"\n", "utf8");
}
TS

# 5) Shared Edge API (browser/node/rn)
cat > packages/edge-api/package.json << 'JSON'
{
  "name": "@efemera/edge-api",
  "version": "0.0.1",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": { "build": "tsc -p tsconfig.json" },
  "devDependencies": { "typescript": "^5.4.0" }
}
JSON

cat > packages/edge-api/tsconfig.json << 'JSON'
{ "compilerOptions": { "outDir":"dist","declaration":true,"target":"ES2020","module":"CommonJS","strict":true,"lib":["ES2020","DOM"] } }
JSON

cat > packages/edge-api/src/index.ts << 'TS'
export type Controller = (state: any) => void;
let _controller: Controller | null = null;
const _state = { edges:[], nodes:[], pending:[], consent:{} };

export const EdgeAPI = {
  setController(fn: Controller){ _controller = fn; },
  clearController(){ _controller = null; },
  getState(){ return _state; },
  stepOnce(){
    // simple demo tick
    _state.pending.push({ kind:"frame", ts: Date.now() });
    _controller?.(_state);
  }
};
// Browser seam
declare global { interface Window { EdgeAPI?: typeof EdgeAPI } }
if (typeof window !== "undefined") { (window as any).EdgeAPI = EdgeAPI; }
TS

# 6) Server app
cat > apps/server/package.json << 'JSON'
{
  "name": "@efemera/server",
  "version": "0.0.1",
  "type": "module",
  "scripts": { "dev": "tsx src/index.ts", "build": "tsc -p tsconfig.json" },
  "dependencies": {
    "fastify": "^4.27.2",
    "@fastify/websocket": "^8.3.1",
    "mqtt": "^5.7.0",
    "pg": "^8.11.5",
    "dotenv": "^16.4.5",
    "@efemera/telemetry": "workspace:*",
    "@efemera/edge-api": "workspace:*"
  },
  "devDependencies": { "typescript":"^5.4.0","tsx":"^4.7.0","@types/node":"^20.11.30" }
}
JSON

cat > apps/server/tsconfig.json << 'JSON'
{ "compilerOptions": { "outDir":"dist","target":"ES2022","module":"ES2022","moduleResolution":"bundler","strict":true } }
JSON

cat > apps/server/src/index.ts << 'TS'
import Fastify from "fastify";
import websocket from "@fastify/websocket";
import * as dotenv from "dotenv";
import { EdgeAPI } from "@efemera/edge-api";
import { logEvent } from "@efemera/telemetry";
import mqtt from "mqtt";

dotenv.config();
const TELEMETRY_PATH = ".deia/telemetry/telemetry.jsonl";
const app = Fastify({ logger: true });
await app.register(websocket);

app.get("/v1/health", async () => ({ ok: true }));
app.post("/v1/session", async (req, reply) => {
  const token = "dev-" + Math.random().toString(36).slice(2);
  logEvent(TELEMETRY_PATH,"session_start",{ sessionId: token },{});
  return reply.send({ token });
});
app.post("/v1/activity", async (req, reply) => {
  const body = (req.body ?? {}) as any;
  logEvent(TELEMETRY_PATH,"activity_post",{ sessionId: body.sessionId }, body);
  app.websocketServer.clients.forEach((ws:any) => ws.send(JSON.stringify({ type:"activity", data: body })));
  return reply.send({ ok:true });
});

app.get("/v1/activity/stream", { websocket: true }, (conn/*, req*/) => {
  conn.socket.on("message", (msg:Buffer) => {
    const payload = msg.toString();
    logEvent(TELEMETRY_PATH,"response_rcvd",{ },{ payload });
    conn.socket.send(JSON.stringify({ echo: payload }));
  });
});

app.get("/debug/telemetry", async (_req, reply) => {
  reply.header("Content-Type","application/jsonl");
  reply.sendFile?.(TELEMETRY_PATH); // if fastify-static later
  return reply.send("Use local file: .deia/telemetry/telemetry.jsonl");
});

// MQTT bridge
const mHost = process.env.MQTT_HOST ?? "localhost";
const mPort = process.env.MQTT_PORT ?? "1883";
const client = mqtt.connect(`mqtt://${mHost}:${mPort}`);
client.on("connect", () => {
  app.log.info("MQTT connected");
  client.subscribe("efemera/#");
});
client.on("message", (_topic, msg) => {
  logEvent(TELEMETRY_PATH,"frame",{ },{ mqtt: msg.toString() });
});

const port = Number(process.env.SERVER_PORT ?? 8080);
app.listen({ port, host: "0.0.0.0" }).then(() => console.log(`Efemera server on :${port}`));
TS

# 7) Mobile app (Expo)
cat > apps/mobile/package.json << 'JSON'
{
  "name": "@efemera/mobile",
  "version": "0.0.1",
  "private": true,
  "main": "index.js",
  "scripts": { "start": "expo start", "android":"expo run:android", "ios":"expo run:ios" },
  "dependencies": {
    "expo": "^51.0.0",
    "react": "18.2.0",
    "react-native": "0.74.0",
    "@efemera/edge-api": "workspace:*"
  },
  "devDependencies": { "@types/react":"^18.2.66","@types/react-native":"^0.73.0" }
}
JSON

cat > apps/mobile/app.json << 'JSON'
{ "expo": { "name":"Efemera","slug":"efemera","scheme":"efemera","web":{"bundler":"metro"} } }
JSON

cat > apps/mobile/index.js << 'JS'
import { registerRootComponent } from 'expo';
import App from './src/App';
registerRootComponent(App);
JS

mkdir -p apps/mobile/src
cat > apps/mobile/src/App.jsx << 'JSX'
import React, { useEffect, useState } from "react";
import { View, Text, Button, SafeAreaView, ScrollView } from "react-native";
import { EdgeAPI } from "@efemera/edge-api";

export default function App(){
  const [log, setLog] = useState([]);
  useEffect(()=> {
    EdgeAPI.setController((state)=> setLog(l => [...l, `frame#${l.length+1} pending:${state.pending.length}`]));
  },[]);
  return (
    <SafeAreaView>
      <ScrollView style={{ padding:16 }}>
        <Text style={{ fontSize:24, fontWeight:"700" }}>Efemera Mobile Node</Text>
        <Button title="Step Once" onPress={()=> EdgeAPI.stepOnce()} />
        {log.slice(-10).map((line, i)=>(<Text key={i}>{line}</Text>))}
      </ScrollView>
    </SafeAreaView>
  );
}
JSX

# 8) Alexa Skill scaffold
cat > apps/alexa/package.json << 'JSON'
{
  "name": "@efemera/alexa",
  "version": "0.0.1",
  "type": "module",
  "scripts": { "dev": "tsx src/index.ts","build":"tsc -p tsconfig.json" },
  "dependencies": { "ask-sdk-core":"^2.12.1","ask-sdk-model":"^1.77.0" },
  "devDependencies": { "typescript":"^5.4.0","tsx":"^4.7.0","@types/node":"^20.11.30" }
}
JSON

cat > apps/alexa/tsconfig.json << 'JSON'
{ "compilerOptions": { "outDir":"dist","target":"ES2022","module":"ES2022","moduleResolution":"bundler","strict":true } }
JSON

cat > apps/alexa/src/index.ts << 'TS'
import { SkillBuilders } from "ask-sdk-core";
const LaunchRequestHandler = {
  canHandle(handlerInput:any){ return handlerInput.requestEnvelope.request.type === 'LaunchRequest'; },
  handle(handlerInput:any){
    const speakOutput = 'Efemera node online. Say "post hello" to send a test activity."';
    return handlerInput.responseBuilder.speak(speakOutput).getResponse();
  }
};
export const handler = SkillBuilders.custom().addRequestHandlers(LaunchRequestHandler).lambda();
TS

# 9) Edge bridge service
cat > services/edge-bridge/package.json << 'JSON'
{
  "name": "@efemera/edge-bridge",
  "version": "0.0.1",
  "type": "module",
  "scripts": { "dev":"tsx src/index.ts","build":"tsc -p tsconfig.json" },
  "dependencies": { "mqtt":"^5.7.0","ws":"^8.16.0" },
  "devDependencies": { "typescript":"^5.4.0","tsx":"^4.7.0","@types/node":"^20.11.30" }
}
JSON

cat > services/edge-bridge/tsconfig.json << 'JSON'
{ "compilerOptions": { "outDir":"dist","target":"ES2022","module":"ES2022","moduleResolution":"bundler","strict":true } }
JSON

cat > services/edge-bridge/src/index.ts << 'TS'
import mqtt from "mqtt";
import WebSocket from "ws";
const m = mqtt.connect("mqtt://localhost:1883");
const ws = new WebSocket("ws://localhost:8080/v1/activity/stream");

m.on("connect", ()=> m.subscribe("efemera/broadcast"));
m.on("message", (_t, msg)=> ws.readyState===1 && ws.send(msg.toString()));
ws.on("message", (data)=> m.publish("efemera/broadcast", data.toString()));
console.log("edge-bridge running (MQTT <-> WS)");
TS

# 10) Observability schema
cat > observability/telemetry.schema.json << 'JSON'
{ "$ref":"#/definitions/Telemetry", "definitions": { "Telemetry": {
  "type":"object","required":["ts","event","ctx"],
  "properties":{"ts":{"type":"string"},"event":{"type":"string"},"ctx":{"type":"object"},"data":{"type":"object"}}
}}}
JSON

# 11) Dev script
cat > scripts/dev.sh << 'BASH'
#!/usr/bin/env bash
set -e
pnpm db:up
pnpm -r build || true
concurrently \
  "pnpm --filter @efemera/server dev" \
  "pnpm --filter @efemera/edge-bridge dev" \
  "pnpm --filter @efemera/mobile start"
BASH
chmod +x scripts/dev.sh

# 12) README
cat > README.md << 'MD'
# Efemera (dev)
## Quickstart
1) `cp .env.example .env` (optional)
2) `corepack enable && corepack prepare pnpm@9.12.0 --activate`
3) `pnpm i`
4) `pnpm db:up`
5) `pnpm dev`  (server + mobile + bridge)

### Test
- REST: `curl localhost:8080/v1/health`
- WS: use any WS client to `ws://localhost:8080/v1/activity/stream`
- MQTT: publish to `efemera/broadcast` on `localhost:1883`

### Telemetry
Events at `.deia/telemetry/telemetry.jsonl`.

### Mobile
Expo dev server opens; scan QR in iOS/Android.

MD

# 13) Root tool deps
pnpm add -D concurrently turbo typescript tsx
echo "Hatch complete. Next: corepack enable && corepack prepare pnpm@9.12.0 --activate && pnpm i && pnpm db:up && pnpm dev"
```

---

## 6) Acceptance (v0.1)

* **Build**: `pnpm i` completes without error.
* **Infra**: `pnpm db:up` brings up Postgres + Mosquitto.
* **Server**: `GET /v1/health` returns `{ ok: true }`.
* **Nodes**: Mobile app launches via Expo; pressing **Step Once** updates log.
* **Bridge**: MQTT  WS echo roundtrip visible.
* **Telemetry**: `.deia/telemetry/telemetry.jsonl` accumulates events.

## 7) KPIs

* TTI (time-to-interact)  10 minutes from hatch to mobile button press.
* WS echo roundtrip p50 < 150ms (local).
* MQTT publishWS echo success rate  99% (local dev).

## 8) Risks

* Expo native builds require platform SDKs (Xcode/Android Studio).
* Alexa deployment needs ASK console config (scaffold only).

> Note: IoT meshes differ; MQTT is provided as a portable baseline.

---

## 9) Change Requests (CR log)

* CR-20251014-1: Add SSE `/v1/activity/stream` alt for WS tests.
* CR-20251014-2: Provide `edge-bridge` demo to validate mesh scenarios.

---

## 10) DEIA Session Logging (mandatory hatch step)

* Enable CLI/session capture per DEIA; store outputs in `.deia/sessions/`.
* Sanitize before public sharing.

---

```
#note, #log type, #tag type, #tags, #ask
```
