"""
ReaderDrone: parses markdown/python files and extracts outlines.
"""
from .base_drone import Drone
from pathlib import Path
from typing import List

class ReaderDrone(Drone):
    def ingest(self, path: str) -> str:
        p = Path(path)
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            text = ""
        self.log(f"ingested {p}")
        return text

    def tag_sections(self, text: str) -> List[str]:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        headers = [ln for ln in lines if ln.startswith('#')]
        self.log(f"found {len(headers)} headers")
        return headers

    def pulse(self, tick: int) -> None:
        if tick % 10 == 0:
            self.log("idle read pulse")
