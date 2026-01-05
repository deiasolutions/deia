from __future__ import annotations

from pathlib import Path
import subprocess
from shutil import which
from typing import Dict, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from deia_raqcoon.adapters.registry import get_cli_adapter, get_cli_command
from deia_raqcoon.kb.store import list_entities, preview_injection, upsert_entity
from deia_raqcoon.runtime.launcher import preflight_repo_root
from deia_raqcoon.core.task_files import complete_task, latest_response, write_task
from deia_raqcoon.runtime.store import MessageStore
from deia_raqcoon.runtime.flights import FlightStore
from deia_raqcoon.runtime.pty_bridge import PTYBridge


app = FastAPI(title="DEIA RAQCOON")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_message_store = MessageStore()
_flight_store = FlightStore()
_pty_bridge = PTYBridge()
_gates: Dict = {
    "allow_q33n_git": False,
    "pre_sprint_review": False,
    "allow_flight_commits": False,
}


class LaunchRequest(BaseModel):
    tool: str
    cwd: Optional[str] = None
    confirm: bool = False


class PTYStartRequest(BaseModel):
    tool: str
    repo_root: str


class PTYSendRequest(BaseModel):
    session_id: str
    data: str


class PTYStopRequest(BaseModel):
    session_id: str


class MessageRequest(BaseModel):
    channel_id: str
    author: str
    content: str
    lane: Optional[str] = None
    provider: Optional[str] = None
    token_count: Optional[int] = None

class TaskRequest(BaseModel):
    bot_id: str
    task_id: Optional[str] = None
    intent: str = "code"
    title: str
    summary: str
    kb_entities: List[str] = []
    delivery_mode: str = "task_file"
    repo_root: Optional[str] = None


class TaskCompleteRequest(BaseModel):
    path: str
    repo_root: Optional[str] = None
    completion_note: Optional[str] = None


class GitCommitRequest(BaseModel):
    repo_root: Optional[str] = None
    message: str


class GitPushRequest(BaseModel):
    repo_root: Optional[str] = None
    remote: str = "origin"
    branch: Optional[str] = None


class GatesUpdateRequest(BaseModel):
    allow_q33n_git: Optional[bool] = None
    pre_sprint_review: Optional[bool] = None
    allow_flight_commits: Optional[bool] = None


class KBEntityRequest(BaseModel):
    id: str
    type: str
    title: str
    summary: str
    tags: List[str] = []
    delivery_mode: str = "cache_prompt"
    load_mode: str = "situation"
    attachments: Optional[List[str]] = None


class KBPreviewRequest(BaseModel):
    entity_ids: List[str]


class FlightStartRequest(BaseModel):
    flight_id: str
    title: str


class FlightEndRequest(BaseModel):
    flight_id: str


class FlightRecapRequest(BaseModel):
    flight_id: str
    recap_text: str


@app.get("/api/health")
def health() -> Dict:
    return {"status": "ok"}


@app.get("/api/config")
def config() -> Dict:
    cwd = Path.cwd()
    preflight = preflight_repo_root(cwd)
    return {
        "cwd": str(cwd),
        "repo_root": str(preflight.repo_root) if preflight.repo_root else None,
        "repo_status": preflight.status,
    }


@app.post("/api/bees/launch")
def launch_bee(request: LaunchRequest) -> Dict:
    cwd = Path(request.cwd).resolve() if request.cwd else Path.cwd().resolve()
    preflight = preflight_repo_root(cwd)

    if preflight.status == "error":
        return {"success": False, "status": "error", "message": preflight.message}

    if preflight.status == "prompt" and not request.confirm:
        return {
            "success": False,
            "status": "prompt",
            "message": preflight.message,
            "repo_root": str(preflight.repo_root),
            "cwd": str(preflight.cwd),
        }

    repo_root = preflight.repo_root or cwd
    adapter = get_cli_adapter(request.tool)
    result = adapter.launch(repo_root)

    if not result.success:
        return {"success": False, "status": "error", "message": result.error}

    return {
        "success": True,
        "status": "launched",
        "tool": request.tool,
        "repo_root": str(repo_root),
        "pid": result.pid,
    }


@app.post("/api/pty/start")
def start_pty(request: PTYStartRequest) -> Dict:
    repo_root = Path(request.repo_root).resolve()
    preflight = preflight_repo_root(repo_root)
    if preflight.status == "error":
        return {"success": False, "error": preflight.message}
    if preflight.status == "prompt":
        return {"success": False, "error": "Repo root required. Provide repo_root."}
    command = get_cli_command(request.tool)
    if not command:
        return {"success": False, "error": "No CLI command configured."}
    executable = command[0]
    resolved = executable
    if not (Path(executable).is_absolute() or Path(executable).exists()):
        resolved = which(executable) or ""
    if not resolved:
        return {"success": False, "error": f"Executable not found: {executable}"}
    command[0] = resolved
    session = _pty_bridge.start(command, repo_root)
    return {"success": True, "session_id": session.session_id}


@app.post("/api/pty/send")
def send_pty(request: PTYSendRequest) -> Dict:
    ok = _pty_bridge.send(request.session_id, request.data)
    return {"success": ok}


@app.get("/api/pty/read")
def read_pty(session_id: str, max_chars: int = 4000) -> Dict:
    output = _pty_bridge.read(session_id, max_chars=max_chars)
    return {"output": output}


@app.post("/api/pty/stop")
def stop_pty(request: PTYStopRequest) -> Dict:
    ok = _pty_bridge.stop(request.session_id)
    return {"success": ok}


@app.post("/api/messages")
def post_message(request: MessageRequest) -> Dict:
    item = _message_store.add_message(
        channel_id=request.channel_id,
        author=request.author,
        content=request.content,
        lane=request.lane,
        provider=request.provider,
        token_count=request.token_count,
    )
    return {"success": True, "message": item}


@app.get("/api/messages")
def get_messages(channel_id: Optional[str] = None) -> Dict:
    return {"messages": _message_store.get_messages(channel_id=channel_id)}


@app.get("/api/summary")
def get_summary() -> Dict:
    return {"summary": _message_store.get_summary()}


@app.get("/api/channels")
def get_channels() -> Dict:
    channels = sorted({m["channel_id"] for m in _message_store.get_messages()})
    return {"channels": channels}


@app.get("/api/kb/entities")
def get_kb_entities() -> Dict:
    return {"entities": list_entities()}


@app.post("/api/kb/entities")
def create_kb_entity(request: KBEntityRequest) -> Dict:
    try:
        entity = upsert_entity(request.dict())
        return {"success": True, "entity": entity}
    except ValueError as exc:
        return {"success": False, "error": str(exc)}


@app.put("/api/kb/entities/{entity_id}")
def update_kb_entity(entity_id: str, request: KBEntityRequest) -> Dict:
    entity = request.dict()
    entity["id"] = entity_id
    try:
        entity = upsert_entity(entity)
        return {"success": True, "entity": entity}
    except ValueError as exc:
        return {"success": False, "error": str(exc)}


@app.post("/api/kb/preview")
def kb_preview(request: KBPreviewRequest) -> Dict:
    return {"preview": preview_injection(request.entity_ids)}


@app.post("/api/tasks")
def create_task(request: TaskRequest) -> Dict:
    repo_root = Path(request.repo_root).resolve() if request.repo_root else Path.cwd().resolve()
    payload = {
        "task_id": request.task_id or "TASK-NEW",
        "intent": request.intent,
        "title": request.title,
        "summary": request.summary,
        "kb_entities": request.kb_entities,
        "delivery": {"mode": request.delivery_mode},
    }
    path = write_task(repo_root, request.bot_id, payload)
    return {"success": True, "path": str(path)}


@app.post("/api/tasks/complete")
def complete_task_endpoint(request: TaskCompleteRequest) -> Dict:
    if not request.repo_root:
        return {"success": False, "path": "", "error": "repo_root required"}
    root = Path(request.repo_root).resolve()
    task_path = Path(request.path).resolve()
    if root not in task_path.parents:
        return {"success": False, "path": "", "error": "task path must be inside repo_root"}
    archived = complete_task(root, task_path, completion_note=request.completion_note)
    if not archived:
        return {"success": False, "path": "", "error": "task not found"}
    return {"success": True, "path": str(archived)}


@app.get("/api/tasks/response")
def get_latest_response(task_id: Optional[str] = None, repo_root: Optional[str] = None) -> Dict:
    root = Path(repo_root).resolve() if repo_root else Path.cwd().resolve()
    path = latest_response(root, task_id=task_id)
    return {"path": str(path) if path else None}


@app.get("/api/git/status")
def git_status(repo_root: Optional[str] = None) -> Dict:
    root = Path(repo_root).resolve() if repo_root else Path.cwd().resolve()
    preflight = preflight_repo_root(root)
    if preflight.status == "error":
        return {"status": "", "error": preflight.message}
    if preflight.status == "prompt":
        return {"status": "", "error": "Repo root required. Provide repo_root or confirm."}
    try:
        result = subprocess.run(
            ["git", "status", "-sb"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        return {"status": result.stdout.strip(), "error": result.stderr.strip()}
    except Exception as exc:
        return {"status": "", "error": str(exc)}


@app.get("/api/gates")
def get_gates() -> Dict:
    return {"gates": _gates}


@app.post("/api/gates")
def update_gates(request: GatesUpdateRequest) -> Dict:
    updates = request.dict(exclude_unset=True)
    _gates.update(updates)
    return {"success": True, "gates": _gates}


@app.post("/api/git/commit")
def git_commit(request: GitCommitRequest) -> Dict:
    root = Path(request.repo_root).resolve() if request.repo_root else Path.cwd().resolve()
    preflight = preflight_repo_root(root)
    if preflight.status == "error":
        return {"output": "", "error": preflight.message}
    if preflight.status == "prompt":
        return {"output": "", "error": "Repo root required. Provide repo_root or confirm."}
    if not _gates.get("allow_q33n_git", False):
        return {"output": "", "error": "Git commit blocked: Q33N git not approved."}
    if not _gates.get("pre_sprint_review", False):
        return {"output": "", "error": "Git commit blocked: pre-sprint review not complete."}
    try:
        result = subprocess.run(
            ["git", "commit", "-am", request.message],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        return {"output": result.stdout.strip(), "error": result.stderr.strip()}
    except Exception as exc:
        return {"output": "", "error": str(exc)}


@app.post("/api/git/push")
def git_push(request: GitPushRequest) -> Dict:
    root = Path(request.repo_root).resolve() if request.repo_root else Path.cwd().resolve()
    preflight = preflight_repo_root(root)
    if preflight.status == "error":
        return {"output": "", "error": preflight.message}
    if preflight.status == "prompt":
        return {"output": "", "error": "Repo root required. Provide repo_root or confirm."}
    if not _gates.get("allow_q33n_git", False):
        return {"output": "", "error": "Git push blocked: Q33N git not approved."}
    cmd = ["git", "push", request.remote]
    if request.branch:
        cmd.append(request.branch)
    try:
        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        return {"output": result.stdout.strip(), "error": result.stderr.strip()}
    except Exception as exc:
        return {"output": "", "error": str(exc)}


@app.post("/api/flights/start")
def start_flight(request: FlightStartRequest) -> Dict:
    return {"success": True, "flight": _flight_store.start_flight(request.flight_id, request.title)}


@app.post("/api/flights/end")
def end_flight(request: FlightEndRequest) -> Dict:
    return {"success": True, "flight": _flight_store.end_flight(request.flight_id)}


@app.post("/api/flights/recap")
def add_flight_recap(request: FlightRecapRequest) -> Dict:
    return {"success": True, "recap": _flight_store.add_recap(request.flight_id, request.recap_text)}


@app.get("/api/flights")
def list_flights() -> Dict:
    return {"flights": _flight_store.list_flights()}


@app.get("/api/flights/recaps")
def list_recaps(flight_id: Optional[str] = None) -> Dict:
    return {"recaps": _flight_store.list_recaps(flight_id=flight_id)}


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        return
