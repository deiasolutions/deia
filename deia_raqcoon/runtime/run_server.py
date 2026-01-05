from __future__ import annotations

from pathlib import Path
import sys
import uvicorn


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    uvicorn.run(
        "deia_raqcoon.runtime.server:app",
        host="127.0.0.1",
        port=8010,
        log_level="info",
        reload=False,
    )
