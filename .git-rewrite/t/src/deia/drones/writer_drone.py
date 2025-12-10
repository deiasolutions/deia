"""
WriterDrone: expands outlines into drafts.
"""
from .base_drone import Drone

class WriterDrone(Drone):
    def compose(self, outline: list[str]) -> str:
        body = "\n\n".join(f"{h}\n\nLorem ipsum..." for h in outline)
        self.log(f"draft length={len(body)}")
        return body

    def call_llm(self, prompt: str) -> str:
        # Placeholder; wired later
        return f"LLM: {prompt[:60]}..."

    def pulse(self, tick: int) -> None:
        if tick % 16 == 0:
            self.log("idle writer pulse")
