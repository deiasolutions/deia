"""
Tests for temp staging cleanup utilities.
"""

import shutil
from datetime import datetime
from pathlib import Path

import pytest

from deia.tools.temp_staging_cleanup import cleanup_temp_staging


@pytest.fixture
def staging_dir(tmp_path: Path) -> Path:
    d = tmp_path / "staging"
    d.mkdir()
    return d


def test_cleanup_disabled_returns_message(staging_dir: Path):
    config = {
        "sync": {
            "use_temp_staging": False,
            "temp_staging_folder": str(staging_dir),
        }
    }

    result = cleanup_temp_staging(config=config, source="test")

    assert result["message"] == "Temp staging disabled via configuration"
    assert result["deleted_files"] == 0
    assert result["success"] is True


def test_cleanup_deletes_files_when_enabled(staging_dir: Path):
    file_path = staging_dir / "note.md"
    file_path.write_text("hello world", encoding="utf-8")

    config = {
        "sync": {
            "use_temp_staging": True,
            "temp_staging_folder": str(staging_dir),
        }
    }

    result = cleanup_temp_staging(config=config, source="test")

    assert result["success"] is True
    assert result["deleted_files"] == 1
    assert result["archived_files"] == 0
    assert list(staging_dir.iterdir()) == []


def test_cleanup_archives_when_archive_folder_configured(staging_dir: Path, tmp_path: Path):
    file_path = staging_dir / "draft.md"
    file_path.write_text("draft", encoding="utf-8")

    archive_dir = tmp_path / "archive"
    config = {
        "sync": {
            "use_temp_staging": True,
            "temp_staging_folder": str(staging_dir),
            "archive_folder": str(archive_dir),
        }
    }

    fake_ts = datetime(2025, 1, 2, 3, 4, 5)

    result = cleanup_temp_staging(
        config=config,
        source="test",
        timestamp_fn=lambda: fake_ts,
    )

    assert result["success"] is True
    assert result["archived_files"] == 1
    assert result["deleted_files"] == 0
    archive_path = Path(result["archive_path"])
    assert archive_path.exists()
    archived_files = list(archive_path.iterdir())
    assert len(archived_files) == 1
    assert archived_files[0].read_text(encoding="utf-8") == "draft"

    # Clean up archived folder explicitly to keep tmp dir tidy on Windows
    shutil.rmtree(archive_dir, ignore_errors=True)
