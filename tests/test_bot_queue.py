"""
Tests for Bot Queue Service

The bot queue manages FIFO bot availability with skill tracking
for optimal bot selection in the DEIA hive system.
"""
import pytest
import json
from pathlib import Path
from datetime import datetime
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from deia.bot_queue import BotQueue


@pytest.fixture
def temp_queue_file(tmp_path):
    """Temporary queue file for testing"""
    return tmp_path / "test-bot-queue.json"


@pytest.fixture
def bot_queue(temp_queue_file):
    """BotQueue instance for testing"""
    return BotQueue(temp_queue_file)


class TestBotQueueBasics:
    """Test basic queue operations"""

    def test_create_empty_queue(self, bot_queue):
        """Should create empty queue"""
        assert bot_queue.list_available_bots() == []

    def test_add_bot_to_queue(self, bot_queue):
        """Should add bot to queue"""
        bot_queue.add_bot(
            bot_id="BOT-00002",
            skills=["testing", "python"],
            context_history=[]
        )
        assert "BOT-00002" in bot_queue.list_available_bots()

    def test_remove_bot_from_queue(self, bot_queue):
        """Should remove bot from queue"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.remove_bot("BOT-00002")
        assert "BOT-00002" not in bot_queue.list_available_bots()

    def test_fifo_order_maintained(self, bot_queue):
        """Should maintain FIFO order"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.add_bot("BOT-00003", ["integration"], [])
        bot_queue.add_bot("BOT-00004", ["docs"], [])

        available = bot_queue.list_available_bots()
        assert available[0] == "BOT-00002"
        assert available[1] == "BOT-00003"
        assert available[2] == "BOT-00004"


class TestBotSelection:
    """Test bot selection logic"""

    def test_get_next_available_no_skills(self, bot_queue):
        """Should return first available bot when no skills required"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.add_bot("BOT-00003", ["integration"], [])

        next_bot = bot_queue.get_next_available()
        assert next_bot == "BOT-00002"

    def test_get_next_available_with_skill_match(self, bot_queue):
        """Should return bot with matching skills"""
        bot_queue.add_bot("BOT-00002", ["testing", "python"], [])
        bot_queue.add_bot("BOT-00003", ["integration", "api"], [])
        bot_queue.add_bot("BOT-00004", ["docs", "markdown"], [])

        next_bot = bot_queue.get_next_available(required_skills=["integration"])
        assert next_bot == "BOT-00003"

    def test_get_next_available_no_match_returns_first(self, bot_queue):
        """Should return first bot if no skill match found"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.add_bot("BOT-00003", ["integration"], [])

        next_bot = bot_queue.get_next_available(required_skills=["blockchain"])
        assert next_bot == "BOT-00002"

    def test_get_next_available_empty_queue(self, bot_queue):
        """Should return None if queue is empty"""
        next_bot = bot_queue.get_next_available()
        assert next_bot is None

    def test_get_next_available_skips_busy_bots(self, bot_queue):
        """Should skip busy bots"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.add_bot("BOT-00003", ["integration"], [])

        bot_queue.mark_busy("BOT-00002", "Running tests")

        next_bot = bot_queue.get_next_available()
        assert next_bot == "BOT-00003"

    def test_best_match_with_context(self, bot_queue):
        """Should prefer bot with relevant context"""
        bot_queue.add_bot("BOT-00002", ["testing"], ["worked on sync"])
        bot_queue.add_bot("BOT-00003", ["testing"], ["worked on legal", "BOK patterns"])

        # Both have "testing" skill, but BOT-00003 has legal context
        next_bot = bot_queue.get_next_available(
            required_skills=["testing"],
            context_keywords=["legal"]
        )
        assert next_bot == "BOT-00003"


class TestBotStatus:
    """Test bot status management"""

    def test_mark_bot_busy(self, bot_queue):
        """Should mark bot as busy"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.mark_busy("BOT-00002", "Running tests")

        profile = bot_queue.get_bot_profile("BOT-00002")
        assert profile["status"] == "busy"
        assert profile["current_task"] == "Running tests"

    def test_mark_bot_available(self, bot_queue):
        """Should mark bot as available"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.mark_busy("BOT-00002", "Running tests")
        bot_queue.mark_available("BOT-00002")

        profile = bot_queue.get_bot_profile("BOT-00002")
        assert profile["status"] == "available"
        assert profile["current_task"] is None

    def test_update_context(self, bot_queue):
        """Should update bot context history"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.update_context("BOT-00002", "Completed sync tests")

        profile = bot_queue.get_bot_profile("BOT-00002")
        assert "Completed sync tests" in profile["context_history"]


class TestIdleManagement:
    """Test idle bot preparation tasks"""

    def test_assign_idle_prep(self, bot_queue):
        """Should assign prep task to idle bot"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.assign_idle_prep("BOT-00002", "Read BOK INDEX for process diagnosis")

        profile = bot_queue.get_bot_profile("BOT-00002")
        assert profile["idle_prep"] == "Read BOK INDEX for process diagnosis"

    def test_idle_bot_not_selected(self, bot_queue):
        """Should not select bot with idle prep task"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.add_bot("BOT-00003", ["testing"], [])
        bot_queue.assign_idle_prep("BOT-00002", "Read BOK")

        next_bot = bot_queue.get_next_available()
        assert next_bot == "BOT-00003"

    def test_clear_idle_prep_when_assigned_task(self, bot_queue):
        """Should clear idle prep when bot gets real task"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        bot_queue.assign_idle_prep("BOT-00002", "Read BOK")
        bot_queue.mark_busy("BOT-00002", "Real task")

        profile = bot_queue.get_bot_profile("BOT-00002")
        assert profile["idle_prep"] is None


class TestPersistence:
    """Test queue persistence"""

    def test_save_queue_to_file(self, temp_queue_file):
        """Should save queue to JSON file"""
        queue1 = BotQueue(temp_queue_file)
        queue1.add_bot("BOT-00002", ["testing"], ["worked on sync"])
        queue1.mark_busy("BOT-00002", "Running tests")

        # Load in new instance
        queue2 = BotQueue(temp_queue_file)
        profile = queue2.get_bot_profile("BOT-00002")

        assert profile["status"] == "busy"
        assert profile["skills"] == ["testing"]
        assert "worked on sync" in profile["context_history"]

    def test_load_empty_queue(self, temp_queue_file):
        """Should handle loading non-existent queue file"""
        queue = BotQueue(temp_queue_file)
        assert queue.list_available_bots() == []


class TestBotProfiles:
    """Test bot profile management"""

    def test_get_bot_profile(self, bot_queue):
        """Should return bot profile"""
        bot_queue.add_bot(
            bot_id="BOT-00002",
            skills=["testing", "python"],
            context_history=["worked on sync", "BOK patterns"]
        )

        profile = bot_queue.get_bot_profile("BOT-00002")
        assert profile["skills"] == ["testing", "python"]
        assert len(profile["context_history"]) == 2
        assert profile["status"] == "available"

    def test_get_nonexistent_bot_profile(self, bot_queue):
        """Should return None for nonexistent bot"""
        profile = bot_queue.get_bot_profile("BOT-99999")
        assert profile is None

    def test_bot_profile_includes_timestamps(self, bot_queue):
        """Should include timestamps in profile"""
        bot_queue.add_bot("BOT-00002", ["testing"], [])
        profile = bot_queue.get_bot_profile("BOT-00002")

        assert "added_at" in profile
        assert "last_updated" in profile
