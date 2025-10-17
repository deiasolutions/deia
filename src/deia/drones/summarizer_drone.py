"""
SummarizerDrone: merges outlines into brief summaries.
"""
from .base_drone import Drone

class SummarizerDrone(Drone):
    def summarize(self, sections: list[str]) -> str:
        summary = "; ".join(s.strip('# ').strip() for s in sections[:10])
        self.log(f"summary length={len(summary)}")
        return summary

    def compare(self, a: str, b: str) -> str:
        return a if len(a) >= len(b) else b

    def pulse(self, tick: int) -> None:
        if tick % 12 == 0:
            self.log("idle summarize pulse")
