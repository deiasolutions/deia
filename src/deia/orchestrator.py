"""
Drone-Lite Orchestrator: pulses active drones on a clock.
"""
from __future__ import annotations
import time
from typing import Iterable, List

from .drones import Drone
from .clock import MonotonicClock


def run_clock(active_drones: Iterable[Drone], clock_interval: float = 0.2, ticks: int | None = 10) -> None:
    """
    Pulse each drone on a simple clock for a fixed number of ticks.
    If ticks is None, run indefinitely.
    """
    clock = MonotonicClock()
    drones: List[Drone] = list(active_drones)
    tick = 0
    while True:
        for d in drones:
            d.clock = d.clock or clock
            d.pulse(tick)
        tick += 1
        if ticks is not None and tick >= ticks:
            break
        time.sleep(clock_interval)
