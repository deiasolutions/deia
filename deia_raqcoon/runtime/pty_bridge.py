from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

from winpty import PtyProcess


@dataclass
class PTYSession:
    session_id: str
    process: PtyProcess
    buffer: list[str] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)
    alive: bool = True

    def append_output(self, data: str) -> None:
        if not data:
            return
        with self.lock:
            self.buffer.append(data)

    def read_buffer(self, max_chars: int = 4000) -> str:
        with self.lock:
            if not self.buffer:
                return ""
            joined = "".join(self.buffer)
            if len(joined) <= max_chars:
                self.buffer.clear()
                return joined
            chunk = joined[:max_chars]
            remainder = joined[max_chars:]
            self.buffer = [remainder]
            return chunk


class PTYBridge:
    def __init__(self) -> None:
        self.sessions: Dict[str, PTYSession] = {}

    def start(self, command: list[str], cwd: Path, env: Optional[dict] = None) -> PTYSession:
        session_id = str(uuid.uuid4())
        process = PtyProcess.spawn(command, cwd=str(cwd), env=env)
        session = PTYSession(session_id=session_id, process=process)
        self.sessions[session_id] = session
        thread = threading.Thread(target=self._reader_loop, args=(session,), daemon=True)
        thread.start()
        return session

    def _reader_loop(self, session: PTYSession) -> None:
        try:
            while session.process.isalive():
                try:
                    data = session.process.read()
                except EOFError:
                    break
                session.append_output(data)
        finally:
            session.alive = False

    def send(self, session_id: str, data: str) -> bool:
        session = self.sessions.get(session_id)
        if not session or not session.alive:
            return False
        session.process.write(data)
        return True

    def read(self, session_id: str, max_chars: int = 4000) -> str:
        session = self.sessions.get(session_id)
        if not session:
            return ""
        return session.read_buffer(max_chars=max_chars)

    def stop(self, session_id: str) -> bool:
        session = self.sessions.pop(session_id, None)
        if not session:
            return False
        try:
            session.process.terminate(force=True)
        except Exception:
            return False
        session.alive = False
        return True
