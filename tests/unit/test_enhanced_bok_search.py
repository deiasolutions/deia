"""
Unit tests for Enhanced BOK Search

Tests all search capabilities:
- Semantic search (TF-IDF)
- Fuzzy search (typo-tolerant)
- Related pattern discovery
- Error handling and edge cases

Author: CLAUDE-CODE-004 (Documentation Curator / Master Librarian)
Date: 2025-10-18
Target Coverage: >80%
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.deia.services.enhanced_bok_search import (
    EnhancedBOKSearch,
    SearchResult,
    search_bok,
    fuzzy_search_bok,
    SKLEARN_AVAILABLE,
    RAPIDFUZZ_AVAILABLE
)


# Test fixtures

@pytest.fixture
def sample_bok_data():
    """Sample BOK pattern data for testing."""
    return [
        {
            "id": "pattern-001",
            "title": "Python List Comprehension",
            "content": "A concise way to create lists in Python using a single line of code",
            "summary": "List comprehensions provide a shorter syntax for creating lists.",
            "path": "python/list_comprehension.md",
            "metadata": {"tags": ["python", "basics"], "difficulty": "beginner"}
        },
        {
            "id": "pattern-002",
            "title": "Python Generators",
            "content": "Generators are a simple way to create iterators in Python using yield",
            "summary": "Generators can be created with generator expressions or generator functions.",
            "path": "python/generators.md",
            "metadata": {"tags": ["python", "intermediate"], "difficulty": "intermediate"}
        },
        {
            "id": "pattern-003",
            "title": "Python Decorators",
            "content": "Decorators are a way to modify or enhance functions in Python without changing their code",
            "summary": "Decorators can be used to add functionality to functions.",
            "path": "python/decorators.md",
            "metadata": {"tags": ["python", "advanced"], "difficulty": "advanced"}
        },
        {
            "id": "pattern-004",
            "title": "JavaScript Promises",
            "content": "Promises represent the eventual completion or failure of an asynchronous operation",
            "summary": "Promises are used for asynchronous programming in JavaScript.",
            "path": "javascript/promises.md",
            "metadata": {"tags": ["javascript", "async"], "difficulty": "intermediate"}
        }
    ]


@pytest.fixture
def temp_bok_index(tmp_path, sample_bok_data):
    """Create a temporary BOK index file."""
    index_file = tmp_path / "test_bok_index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(sample_bok_data, f)
    return index_file


@pytest.fixture
def search_engine(temp_bok_index):
    """Create an EnhancedBOKSearch instance with test data."""
    return EnhancedBOKSearch(str(temp_bok_index))


# Tests for SearchResult class

def test_search_result_creation():
    """Test SearchResult dataclass creation."""
    result = SearchResult(
        pattern_id="test-001",
        title="Test Pattern",
        path="test/pattern.md",
        relevance_score=0.95,
        summary="Test summary"
    )

    assert result.pattern_id == "test-001"
    assert result.title == "Test Pattern"
    assert result.path == "test/pattern.md"
    assert result.relevance_score == 0.95
    assert result.summary == "Test summary"
    assert result.metadata is None


def test_search_result_to_dict():
    """Test SearchResult serialization."""
    result = SearchResult(
        pattern_id="test-001",
        title="Test Pattern",
        path="test/pattern.md",
        relevance_score=0.95,
        summary="Test summary",
        metadata={"author": "Test Author"}
    )

    result_dict = result.to_dict()
    assert result_dict["pattern_id"] == "test-001"
    assert result_dict["title"] == "Test Pattern"
    assert result_dict["relevance_score"] == 0.95
    assert result_dict["metadata"]["author"] == "Test Author"


# Tests for initialization

def test_initialization_with_valid_index(temp_bok_index):
    """Test successful initialization with valid index."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index))

    assert search_engine.index_path == Path(temp_bok_index)
    assert len(search_engine.patterns) == 4
    assert search_engine.get_pattern_count() == 4


def test_initialization_with_nonexistent_file(tmp_path):
    """Test initialization with non-existent file raises error."""
    nonexistent = tmp_path / "nonexistent.json"

    with pytest.raises(FileNotFoundError):
        EnhancedBOKSearch(str(nonexistent))


def test_initialization_with_invalid_json(tmp_path):
    """Test initialization with invalid JSON raises error."""
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("not valid json{]")

    with pytest.raises(json.JSONDecodeError):
        EnhancedBOKSearch(str(invalid_json))


def test_initialization_without_auto_load(temp_bok_index):
    """Test initialization without auto-loading."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index), auto_load=False)

    assert len(search_engine.patterns) == 0
    assert search_engine.vectorizer is None


def test_initialization_with_custom_tfidf_params(temp_bok_index):
    """Test initialization with custom TF-IDF parameters."""
    search_engine = EnhancedBOKSearch(
        str(temp_bok_index),
        min_df=2,
        max_df=0.9
    )

    assert search_engine.min_df == 2
    assert search_engine.max_df == 0.9


# Tests for semantic search

@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_basic_query(search_engine):
    """Test basic semantic search."""
    results = search_engine.search("Python list", top_k=3)

    assert len(results) > 0
    assert all(isinstance(r, SearchResult) for r in results)
    # First result should be about list comprehension
    assert "list" in results[0].title.lower()


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_returns_top_k_results(search_engine):
    """Test that search returns correct number of results."""
    results = search_engine.search("Python", top_k=2)

    assert len(results) <= 2


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_empty_query(search_engine):
    """Test search with empty query returns no results."""
    results = search_engine.search("")
    assert len(results) == 0

    results = search_engine.search("   ")
    assert len(results) == 0


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_relevance_scores_descending(search_engine):
    """Test that search results are sorted by relevance."""
    results = search_engine.search("Python programming language", top_k=3)

    if len(results) > 1:
        for i in range(len(results) - 1):
            assert results[i].relevance_score >= results[i + 1].relevance_score


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_positive_scores_only(search_engine):
    """Test that only positive relevance scores are returned."""
    results = search_engine.search("completely unrelated query xyz123", top_k=5)

    for result in results:
        assert result.relevance_score > 0


@pytest.mark.skipif(SKLEARN_AVAILABLE, reason="Test for missing scikit-learn")
def test_search_without_sklearn_raises_error(temp_bok_index):
    """Test that search raises error when sklearn not available."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index))

    with pytest.raises(ValueError, match="scikit-learn"):
        search_engine.search("test query")


# Tests for fuzzy search

@pytest.mark.skipif(not RAPIDFUZZ_AVAILABLE, reason="rapidfuzz not installed")
def test_fuzzy_search_exact_match(search_engine):
    """Test fuzzy search with exact title match."""
    results = search_engine.fuzzy_search("Python List Comprehension")

    assert len(results) > 0
    assert results[0].title == "Python List Comprehension"
    assert results[0].relevance_score >= 0.9


@pytest.mark.skipif(not RAPIDFUZZ_AVAILABLE, reason="rapidfuzz not installed")
def test_fuzzy_search_with_typos(search_engine):
    """Test fuzzy search with typos."""
    results = search_engine.fuzzy_search("Pythn List Comprension", threshold=0.7)

    assert len(results) > 0
    # Should still find "Python List Comprehension" despite typos
    assert any("List Comprehension" in r.title for r in results)


@pytest.mark.skipif(not RAPIDFUZZ_AVAILABLE, reason="rapidfuzz not installed")
def test_fuzzy_search_case_insensitive(search_engine):
    """Test fuzzy search is case insensitive."""
    results_lower = search_engine.fuzzy_search("python list comprehension")
    results_upper = search_engine.fuzzy_search("PYTHON LIST COMPREHENSION")

    assert len(results_lower) > 0
    assert len(results_upper) > 0
    assert results_lower[0].pattern_id == results_upper[0].pattern_id


@pytest.mark.skipif(not RAPIDFUZZ_AVAILABLE, reason="rapidfuzz not installed")
def test_fuzzy_search_threshold(search_engine):
    """Test fuzzy search threshold filtering."""
    # High threshold should return fewer results
    results_high = search_engine.fuzzy_search("Python", threshold=0.95)
    results_low = search_engine.fuzzy_search("Python", threshold=0.5)

    assert len(results_high) <= len(results_low)


@pytest.mark.skipif(not RAPIDFUZZ_AVAILABLE, reason="rapidfuzz not installed")
def test_fuzzy_search_max_results(search_engine):
    """Test fuzzy search max_results parameter."""
    results = search_engine.fuzzy_search("Python", threshold=0.5, max_results=2)

    assert len(results) <= 2


@pytest.mark.skipif(not RAPIDFUZZ_AVAILABLE, reason="rapidfuzz not installed")
def test_fuzzy_search_empty_query(search_engine):
    """Test fuzzy search with empty query."""
    results = search_engine.fuzzy_search("")
    assert len(results) == 0


@pytest.mark.skipif(RAPIDFUZZ_AVAILABLE, reason="Test for missing rapidfuzz")
def test_fuzzy_search_without_rapidfuzz_raises_error(temp_bok_index):
    """Test that fuzzy search raises error when rapidfuzz not available."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index))

    with pytest.raises(ValueError, match="rapidfuzz"):
        search_engine.fuzzy_search("test query")


# Tests for related pattern finding

@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_find_related_patterns(search_engine):
    """Test finding related patterns."""
    related = search_engine.find_related("pattern-001", top_k=2)

    assert len(related) <= 2
    assert all(isinstance(r, tuple) for r in related)
    assert all(len(r) == 2 for r in related)
    # Check that pattern IDs and scores are returned
    assert all(isinstance(r[0], str) and isinstance(r[1], float) for r in related)


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_find_related_excludes_self(search_engine):
    """Test that find_related excludes the source pattern."""
    related = search_engine.find_related("pattern-001", top_k=5)

    # Should not include the pattern itself
    assert all(pattern_id != "pattern-001" for pattern_id, _ in related)


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_find_related_invalid_id(search_engine):
    """Test find_related with non-existent pattern ID."""
    related = search_engine.find_related("nonexistent-id", top_k=3)

    assert len(related) == 0


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_find_related_similarity_scores_valid(search_engine):
    """Test that similarity scores are valid (0.0 to 1.0)."""
    related = search_engine.find_related("pattern-001", top_k=3)

    for pattern_id, score in related:
        assert 0.0 <= score <= 1.0


@pytest.mark.skipif(SKLEARN_AVAILABLE, reason="Test for missing scikit-learn")
def test_find_related_without_sklearn_raises_error(temp_bok_index):
    """Test that find_related raises error when sklearn not available."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index))

    with pytest.raises(ValueError, match="scikit-learn"):
        search_engine.find_related("pattern-001")


# Tests for logging and utility methods

def test_log_search(search_engine, caplog):
    """Test search logging."""
    import logging

    # Set up logging to capture at INFO level
    caplog.set_level(logging.INFO)

    results = [
        SearchResult("001", "Test Pattern 1", "path1.md", 0.95, "Summary 1"),
        SearchResult("002", "Test Pattern 2", "path2.md", 0.85, "Summary 2")
    ]

    search_engine.log_search("test query", results)

    # Check that log contains key information
    assert len(caplog.records) > 0
    log_text = " ".join([r.message for r in caplog.records])
    assert "test query" in log_text or "2" in log_text


def test_get_pattern_count(search_engine):
    """Test getting pattern count."""
    count = search_engine.get_pattern_count()

    assert count == 4
    assert count == len(search_engine.patterns)


def test_reload_index(temp_bok_index, sample_bok_data):
    """Test reloading index."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index))
    initial_count = search_engine.get_pattern_count()

    # Modify the index file
    new_data = sample_bok_data + [{
        "id": "pattern-005",
        "title": "New Pattern",
        "content": "New content",
        "summary": "New summary",
        "path": "new/pattern.md"
    }]
    with open(temp_bok_index, "w", encoding="utf-8") as f:
        json.dump(new_data, f)

    # Reload
    search_engine.reload_index()

    assert search_engine.get_pattern_count() == initial_count + 1


# Tests for standalone convenience functions

@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_bok_convenience_function(temp_bok_index):
    """Test standalone search_bok function."""
    results = search_bok(str(temp_bok_index), "Python list", top_k=3)

    assert len(results) > 0
    assert all(isinstance(r, SearchResult) for r in results)


@pytest.mark.skipif(not RAPIDFUZZ_AVAILABLE, reason="rapidfuzz not installed")
def test_fuzzy_search_bok_convenience_function(temp_bok_index):
    """Test standalone fuzzy_search_bok function."""
    results = fuzzy_search_bok(str(temp_bok_index), "Python List Comprehension")

    assert len(results) > 0
    assert all(isinstance(r, SearchResult) for r in results)


# Tests for edge cases and error handling

def test_empty_index_file(tmp_path):
    """Test handling of empty index file."""
    empty_index = tmp_path / "empty.json"
    empty_index.write_text("[]")

    search_engine = EnhancedBOKSearch(str(empty_index))

    assert search_engine.get_pattern_count() == 0


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_with_empty_index(tmp_path):
    """Test search with empty pattern list."""
    empty_index = tmp_path / "empty.json"
    empty_index.write_text("[]")

    search_engine = EnhancedBOKSearch(str(empty_index))
    results = search_engine.search("test query")

    assert len(results) == 0


def test_patterns_without_required_fields(tmp_path):
    """Test handling patterns with missing required fields."""
    incomplete_data = [
        {
            "id": "001",
            # Missing title, content, summary
            "path": "test.md"
        }
    ]

    index_file = tmp_path / "incomplete.json"
    with open(index_file, "w") as f:
        json.dump(incomplete_data, f)

    # Should not crash, should handle gracefully
    search_engine = EnhancedBOKSearch(str(index_file))
    assert search_engine.get_pattern_count() == 1


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_result_metadata_preserved(search_engine):
    """Test that metadata is preserved in search results."""
    results = search_engine.search("Python", top_k=1)

    if len(results) > 0:
        assert results[0].metadata is not None
        assert "tags" in results[0].metadata or results[0].metadata == {}


# Tests for loading and indexing

def test_load_patterns_success(temp_bok_index, sample_bok_data):
    """Test successful pattern loading."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index), auto_load=False)
    patterns = search_engine._load_patterns()

    assert len(patterns) == len(sample_bok_data)
    assert patterns[0]["id"] == "pattern-001"


def test_build_tfidf_index_without_sklearn(temp_bok_index, monkeypatch):
    """Test TF-IDF index building when sklearn not available."""
    # Temporarily disable sklearn
    import src.deia.services.enhanced_bok_search as module
    original_available = module.SKLEARN_AVAILABLE
    monkeypatch.setattr(module, "SKLEARN_AVAILABLE", False)

    search_engine = EnhancedBOKSearch(str(temp_bok_index))

    # Should handle gracefully
    assert search_engine.vectorizer is None
    assert search_engine.tfidf_matrix is None

    # Restore
    monkeypatch.setattr(module, "SKLEARN_AVAILABLE", original_available)


def test_load_and_index_empty_patterns(tmp_path):
    """Test loading and indexing with empty pattern list."""
    empty_index = tmp_path / "empty.json"
    empty_index.write_text("[]")

    search_engine = EnhancedBOKSearch(str(empty_index))

    assert search_engine.get_pattern_count() == 0
    # Should not crash when building index with empty patterns


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_build_tfidf_index_with_empty_content(tmp_path):
    """Test TF-IDF index building with empty content."""
    data = [
        {"id": "001", "title": "Test", "content": "", "summary": "", "path": "test.md"}
    ]
    index_file = tmp_path / "test.json"
    with open(index_file, "w") as f:
        json.dump(data, f)

    search_engine = EnhancedBOKSearch(str(index_file))

    # Should handle empty content gracefully
    assert search_engine.get_pattern_count() == 1


# Tests for SearchResult with metadata

def test_search_result_with_none_metadata():
    """Test SearchResult with None metadata."""
    result = SearchResult(
        pattern_id="test",
        title="Test",
        path="test.md",
        relevance_score=0.5,
        summary="Summary",
        metadata=None
    )

    assert result.metadata is None
    dict_result = result.to_dict()
    assert dict_result["metadata"] == {}


def test_search_result_with_empty_metadata():
    """Test SearchResult with empty metadata dict."""
    result = SearchResult(
        pattern_id="test",
        title="Test",
        path="test.md",
        relevance_score=0.5,
        summary="Summary",
        metadata={}
    )

    dict_result = result.to_dict()
    assert dict_result["metadata"] == {}


# Integration tests

@pytest.mark.skipif(not (SKLEARN_AVAILABLE and RAPIDFUZZ_AVAILABLE),
                    reason="Full dependencies not installed")
def test_full_search_workflow(search_engine):
    """Test complete search workflow with all features."""
    # 1. Semantic search
    semantic_results = search_engine.search("Python programming", top_k=3)
    assert len(semantic_results) > 0

    # 2. Fuzzy search
    fuzzy_results = search_engine.fuzzy_search("Pythun programing", threshold=0.7)
    assert len(fuzzy_results) > 0

    # 3. Find related patterns
    if semantic_results:
        related = search_engine.find_related(semantic_results[0].pattern_id, top_k=2)
        assert isinstance(related, list)

    # 4. Log results
    search_engine.log_search("test query", semantic_results)


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not installed")
def test_search_across_different_languages(search_engine):
    """Test searching across patterns in different programming languages."""
    # Should be able to find patterns regardless of language
    python_results = search_engine.search("Python", top_k=5)
    js_results = search_engine.search("JavaScript", top_k=5)

    assert len(python_results) > 0
    assert len(js_results) > 0

    # Verify they're different results
    python_ids = {r.pattern_id for r in python_results}
    js_ids = {r.pattern_id for r in js_results}
    assert python_ids != js_ids


# Tests for initialization edge cases

def test_initialization_preserves_parameters(temp_bok_index):
    """Test that initialization parameters are preserved."""
    search_engine = EnhancedBOKSearch(
        str(temp_bok_index),
        min_df=3,
        max_df=0.7,
        auto_load=True
    )

    assert search_engine.min_df == 3
    assert search_engine.max_df == 0.7
    assert len(search_engine.patterns) > 0


def test_pathlib_path_handling(temp_bok_index):
    """Test that Path objects are handled correctly."""
    search_engine = EnhancedBOKSearch(str(temp_bok_index))

    assert isinstance(search_engine.index_path, Path)
    assert search_engine.index_path == Path(temp_bok_index)
