"""Tests for MessageRouter service."""

import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.message_router import MessageRouter


@pytest.fixture
def router():
    """Provide MessageRouter instance."""
    return MessageRouter()


class TestCategoryDetection:
    """Tests for message category detection."""

    def test_detect_dev_category(self, router):
        """Test detection of dev category."""
        decision = router.route_message("Write a Python function to parse JSON files")

        assert decision.detected_category == "dev"
        assert decision.confidence > 0.5

    def test_detect_qa_category(self, router):
        """Test detection of QA category."""
        decision = router.route_message("Create unit tests for the authentication module")

        assert decision.detected_category == "qa"
        assert decision.confidence > 0.5

    def test_detect_docs_category(self, router):
        """Test detection of docs category."""
        decision = router.route_message("Write documentation for the API endpoints")

        assert decision.detected_category == "docs"
        assert decision.confidence > 0.5

    def test_detect_ops_category(self, router):
        """Test detection of ops category."""
        decision = router.route_message("Deploy the application to production infrastructure")

        assert decision.detected_category == "ops"
        assert decision.confidence > 0.5

    def test_detect_analysis_category(self, router):
        """Test detection of analysis category."""
        decision = router.route_message("Analyze the performance metrics and generate a report")

        assert decision.detected_category == "analysis"
        assert decision.confidence > 0.5


class TestBotRecommendation:
    """Tests for bot recommendation."""

    def test_recommend_bot_for_category(self, router):
        """Test bot recommendation matches category."""
        decision = router.route_message("Debug the Python code")

        # Dev category should recommend bot-001
        assert decision.recommended_bot == "bot-001"
        assert decision.final_bot == "bot-001"

    def test_recommend_different_bots(self, router):
        """Test different bots recommended for different categories."""
        dev_decision = router.route_message("Write Python code")
        qa_decision = router.route_message("Create tests")

        assert dev_decision.recommended_bot != qa_decision.recommended_bot


class TestBotOverride:
    """Tests for manual bot override."""

    def test_override_with_at_syntax(self, router):
        """Test @bot-XXX override syntax."""
        decision = router.route_message("@bot-002 Write Python code")

        assert decision.override_bot == "bot-002"
        assert decision.final_bot == "bot-002"

    def test_override_removed_from_message(self, router):
        """Test override syntax removed from message."""
        decision = router.route_message("@bot-003 Debug this code")

        assert "@bot-003" not in decision.message
        assert "Debug this code" in decision.message

    def test_no_override(self, router):
        """Test message without override."""
        decision = router.route_message("Write Python code")

        assert decision.override_bot is None
        assert decision.final_bot == decision.recommended_bot


class TestConfidenceScoring:
    """Tests for confidence scoring."""

    def test_high_confidence_match(self, router):
        """Test high confidence for strong matches."""
        decision = router.route_message("def my_function(): pass  # Python code")

        assert decision.confidence > 0.7

    def test_low_confidence_weak_match(self, router):
        """Test lower confidence for weak matches."""
        decision = router.route_message("hello world")

        assert decision.confidence <= 0.6


class TestCategories:
    """Tests for available categories."""

    def test_get_all_categories(self, router):
        """Test retrieving all available categories."""
        categories = router.get_all_categories()

        assert "dev" in categories
        assert "qa" in categories
        assert "docs" in categories
        assert "ops" in categories
        assert "analysis" in categories

    def test_category_has_bot(self, router):
        """Test each category has assigned bot."""
        categories = router.get_all_categories()

        for category, info in categories.items():
            assert "bot" in info
            assert info["bot"].startswith("bot-")


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_message(self, router):
        """Test handling of empty message."""
        decision = router.route_message("")

        assert decision.final_bot is not None
        assert decision.confidence == 0.5  # Default

    def test_message_with_multiple_categories(self, router):
        """Test message with keywords from multiple categories."""
        decision = router.route_message("Write test code for Python module")

        # Should prioritize based on keyword density
        assert decision.final_bot is not None

    def test_reasoning_generated(self, router):
        """Test reasoning is always generated."""
        decision = router.route_message("Test message")

        assert decision.reasoning is not None
        assert len(decision.reasoning) > 0


# Coverage targets
COVERAGE_TARGETS = {
    "Category Detection": "✅ 5 tests",
    "Bot Recommendation": "✅ 2 tests",
    "Bot Override": "✅ 3 tests",
    "Confidence Scoring": "✅ 2 tests",
    "Categories": "✅ 2 tests",
    "Edge Cases": "✅ 3 tests",
    "Total Tests": "17 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
