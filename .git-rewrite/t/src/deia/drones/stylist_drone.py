"""
StylistDrone: applies DEIA style and QA checks.
"""
from .base_drone import Drone

class StylistDrone(Drone):
    def format(self, text: str) -> str:
        self.log("formatted text")
        return text.strip() + "\n"

    def check_quality(self, text: str) -> dict:
        q = {"length": len(text), "lines": text.count('\n') + 1}
        self.log(f"quality={q}")
        return q

    def pulse(self, tick: int) -> None:
        if tick % 18 == 0:
            self.log("idle stylist pulse")
