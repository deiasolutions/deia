"""
Temp staging cleanup utilities for DEIA sync workflows.

Provides helpers that remove (or archive) the temporary staging area created by the
Downloads monitor once work has been committed to git.
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional

from ..config import load_config

logger = logging.getLogger(__name__)


def _default_timestamp() -> datetime:
    return datetime.now()


def cleanup_temp_staging(
    config: Optional[Dict] = None,
    config_path: Optional[Path] = None,
    *,
    source: str = "manual",
    timestamp_fn: Callable[[], datetime] = _default_timestamp,
) -> Dict:
    """
    Remove or archive files from the temp staging directory.

    Args:
        config: Optional pre-loaded DEIA config dict (mainly for tests).
        config_path: Optional explicit path to config JSON.
        source: String describing trigger origin (manual, post-commit, etc.).
        timestamp_fn: Factory for timestamps (injected for deterministic tests).

    Returns:
        Dict with cleanup metadata (counts, archive path, messages).
    """
    if config is None:
        cfg = load_config(config_path)
    else:
        cfg = config

    sync_cfg = cfg.get("sync", cfg)
    processing_cfg = (
        sync_cfg.get("processing", {}) if isinstance(sync_cfg.get("processing"), dict) else {}
    )

    temp_folder_str = sync_cfg.get("temp_staging_folder") or processing_cfg.get(
        "temp_staging_folder"
    )
    use_temp = sync_cfg.get("use_temp_staging")
    if use_temp is None:
        use_temp = processing_cfg.get("use_temp_staging", False)
    use_temp = bool(use_temp)

    archive_folder = sync_cfg.get("archive_folder") or processing_cfg.get("archive_folder")
    archive_folder_path = Path(archive_folder).expanduser() if archive_folder else None

    result = {
        "success": True,
        "deleted_files": 0,
        "archived_files": 0,
        "archive_path": None,
        "temp_folder": temp_folder_str or "",
        "source": source,
        "message": "",
        "commit": _get_last_commit_short_hash(),
    }

    if not use_temp:
        result["message"] = "Temp staging disabled via configuration"
        logger.info(result["message"])
        return result

    if not temp_folder_str:
        result["message"] = "Temp staging folder not configured"
        logger.warning(result["message"])
        return result

    temp_folder = Path(temp_folder_str).expanduser()
    result["temp_folder"] = str(temp_folder)

    if not temp_folder.exists():
        result["message"] = "Temp staging folder does not exist"
        logger.info(result["message"])
        return result

    staged_items = list(temp_folder.iterdir())
    if not staged_items:
        result["message"] = "Temp staging already clean"
        logger.info(result["message"])
        return result

    archive_dest = None
    if archive_folder_path:
        archive_dest = (
            archive_folder_path
            / "temp-staging-backups"
            / timestamp_fn().strftime("%Y%m%d-%H%M%S")
        )
        archive_dest.mkdir(parents=True, exist_ok=True)
        result["archive_path"] = str(archive_dest)

    errors = []

    for item in staged_items:
        try:
            if archive_dest:
                destination = archive_dest / item.name
                destination = _resolve_conflict(destination)
                shutil.move(str(item), destination)
                result["archived_files"] += 1
            else:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                result["deleted_files"] += 1
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Failed cleanup for %s: %s", item, exc)
            errors.append(str(exc))

    if errors:
        result["success"] = False
        result["message"] = f"Cleanup completed with {len(errors)} error(s)"
    else:
        action = (
            f"archived to {archive_dest}"
            if archive_dest
            else "deleted from temp staging"
        )
        result["message"] = f"Cleanup complete: {action}"

    logger.info(
        "Temp staging cleanup result | deleted=%s archived=%s source=%s commit=%s",
        result["deleted_files"],
        result["archived_files"],
        source,
        result["commit"],
    )
    return result


def _resolve_conflict(destination: Path) -> Path:
    """Ensure destination path is unique by appending counters if needed."""
    candidate = destination
    counter = 1
    while candidate.exists():
        candidate = destination.with_name(f"{destination.stem}-{counter}{destination.suffix}")
        counter += 1
    return candidate


def _get_last_commit_short_hash() -> Optional[str]:
    """Return short git hash if available (best-effort)."""
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode == 0:
            return completed.stdout.strip()
    except Exception:
        return None
    return None


def _configure_logging(verbose: bool):
    """Ensure logging is configured for standalone invocation."""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def _parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean DEIA temp staging folder after successful commits."
    )
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        help="Optional path to config.json (defaults to project config).",
    )
    parser.add_argument(
        "--source",
        default="manual",
        help="Source label for logging (e.g., post-commit).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging to stdout.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
    args = _parse_args(argv)
    _configure_logging(args.verbose)

    result = cleanup_temp_staging(config_path=args.config, source=args.source)
    if not result["success"]:
        logger.error(result["message"])
        return 1

    if args.verbose:
        logger.info(result["message"])
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
