"""
Base Drone class for DEIA Drone-Lite runtime.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Protocol
import time


class Clock(Protocol):
    def now(self) -> float: ...


@dataclass
class Drone:
    name: str
    role: str
    context: Dict[str, Any] = field(default_factory=dict)
    clock: Optional[Clock] = None

    def pulse(self, tick: int) -> None:
        """Periodic heartbeat; override in subclasses."""
        pass

    def log(self, message: str) -> None:
        ts = self.clock.now() if self.clock else time.time()
        print(f"[{ts:.3f}] [{self.role}] {self.name}: {message}")
