"""
ScribeDrone: versions, logs, and archives outputs.
"""
from .base_drone import Drone
from pathlib import Path

class ScribeDrone(Drone):
    def commit(self, path: str, content: str) -> str:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        self.log(f"wrote {p}")
        return str(p)

    def archive(self, path: str, archive_dir: str = ".deia/eggs/history") -> str:
        p = Path(path)
        target = Path(archive_dir) / p.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
        self.log(f"archived to {target}")
        return str(target)

    def pulse(self, tick: int) -> None:
        if tick % 20 == 0:
            self.log("idle scribe pulse")
