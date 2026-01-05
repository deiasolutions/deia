from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class AdapterResult:
    success: bool
    output: str
    metadata: Optional[Dict] = None


class BaseAdapter:
    """Common adapter interface for all execution lanes."""

    name = "base"

    def send(self, payload: Dict) -> AdapterResult:
        raise NotImplementedError("Adapters must implement send()")
