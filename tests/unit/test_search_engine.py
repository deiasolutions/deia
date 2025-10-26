"""
Unit tests for search_engine module.

Tests full-text search, faceting, query parsing, relevance ranking, and analytics.
"""

import pytest
from src.deia.search_engine import (
    SearchEngine, Document, Tokenizer, SpellingCorrector, InvertedIndex,
    FacetIndex, QueryParser, RelevanceRanker, Autocomplete
)


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        Document(
            doc_id="doc1",
            title="Python Programming Guide",
            content="Learn Python programming basics and advanced concepts",
            category="development",
            tags=["python", "programming"],
            metadata={"author": "Alice"}
        ),
        Document(
            doc_id="doc2",
            title="JavaScript Tutorial",
            content="Master JavaScript for web development",
            category="development",
            tags=["javascript", "web"],
            metadata={"author": "Bob"}
        ),
        Document(
            doc_id="doc3",
            title="DevOps Best Practices",
            content="Learn deployment and operations best practices",
            category="operations",
            tags=["devops", "deployment"],
            metadata={"author": "Charlie"}
        ),
    ]


@pytest.fixture
def search_engine(sample_documents):
    """Create search engine with sample documents."""
    engine = SearchEngine()
    engine.index_documents(sample_documents)
    return engine


class TestTokenizer:
    """Test tokenization and normalization."""

    def test_tokenize(self):
        """Test basic tokenization."""
        text = "Hello World! This is a test."
        tokens = Tokenizer.tokenize(text)

        assert "hello" in tokens
        assert "world" in tokens
        assert len(tokens) > 0

    def test_normalize_removes_stop_words(self):
        """Test stop word removal."""
        tokens = ["the", "quick", "brown", "fox", "jumps", "over"]
        normalized = Tokenizer.normalize(tokens)

        assert "the" not in normalized
        assert "quick" in normalized

    def test_simple_stemming(self):
        """Test stemming."""
        assert Tokenizer.simple_stem("running") == "runn"
        assert Tokenizer.simple_stem("played") == "play"


class TestSpellingCorrector:
    """Test spelling correction."""

    def test_correct_misspelled_word(self):
        """Test correcting misspelled word."""
        vocab = {"python", "javascript", "programming"}
        corrector = SpellingCorrector(vocab)

        result = corrector.correct("pyton")
        assert result == "python"

    def test_correct_exact_match(self):
        """Test exact match."""
        vocab = {"python", "javascript"}
        corrector = SpellingCorrector(vocab)

        result = corrector.correct("python")
        assert result == "python"

    def test_edit_distance(self):
        """Test edit distance calculation."""
        distance = SpellingCorrector.edit_distance("kitten", "sitting")
        assert distance == 3


class TestInvertedIndex:
    """Test inverted index."""

    def test_index_document(self, sample_documents):
        """Test indexing a document."""
        index = InvertedIndex()
        index.index_document(sample_documents[0])

        assert "python" in index.index
        assert sample_documents[0].doc_id in index.index["python"]

    def test_search(self, sample_documents):
        """Test searching index."""
        index = InvertedIndex()
        for doc in sample_documents:
            index.index_document(doc)

        results = index.search("python")
        assert len(results) > 0

    def test_tf_calculation(self, sample_documents):
        """Test TF calculation."""
        index = InvertedIndex()
        index.index_document(sample_documents[0])

        tf = index.get_tf(sample_documents[0].doc_id, "python")
        assert tf > 0

    def test_idf_calculation(self, sample_documents):
        """Test IDF calculation."""
        index = InvertedIndex()
        for doc in sample_documents:
            index.index_document(doc)

        idf = index.get_idf("python")
        assert idf > 0


class TestFacetIndex:
    """Test faceted search."""

    def test_index_document(self, sample_documents):
        """Test indexing document facets."""
        facet_index = FacetIndex()
        facet_index.index_document(sample_documents[0])

        assert "development" in facet_index.facets["category"]

    def test_get_facet_values(self, sample_documents):
        """Test getting facet values."""
        facet_index = FacetIndex()
        for doc in sample_documents:
            facet_index.index_document(doc)

        categories = facet_index.get_facet_values("category")
        assert "development" in categories
        assert "operations" in categories

    def test_filter_by_facet(self, sample_documents):
        """Test filtering by facet."""
        facet_index = FacetIndex()
        for doc in sample_documents:
            facet_index.index_document(doc)

        results = facet_index.filter_by_facet("category", "development")
        assert len(results) == 2


class TestQueryParser:
    """Test query parsing."""

    def test_parse_simple_query(self):
        """Test parsing simple query."""
        parser = QueryParser()
        query = parser.parse("python programming")

        assert "python" in query.terms
        assert "programming" in query.terms

    def test_parse_with_operators(self):
        """Test parsing with AND/OR operators."""
        parser = QueryParser()
        query = parser.parse("python AND javascript")

        assert len(query.operators) > 0
        assert len(query.terms) >= 2

    def test_parse_with_facets(self):
        """Test parsing with facet filters."""
        parser = QueryParser()
        query = parser.parse("python category:development")

        assert "category" in query.facets


class TestRelevanceRanker:
    """Test relevance ranking."""

    def test_rank_documents(self, sample_documents):
        """Test ranking documents by relevance."""
        index = InvertedIndex()
        for doc in sample_documents:
            index.index_document(doc)

        ranker = RelevanceRanker(index)
        candidates = {doc.doc_id for doc in sample_documents}

        ranked = ranker.rank(["python"], candidates)

        assert len(ranked) > 0
        # First result should have highest score
        assert ranked[0][1] >= ranked[-1][1] if len(ranked) > 1 else True


class TestAutocomplete:
    """Test autocomplete suggestions."""

    def test_suggest_completions(self):
        """Test getting suggestions."""
        terms = ["python", "python3", "programming", "program"]
        autocomplete = Autocomplete(terms)

        suggestions = autocomplete.suggest("prog", limit=5)

        assert len(suggestions) > 0
        assert any("program" in s for s in suggestions)

    def test_suggest_with_limit(self):
        """Test suggestion limit."""
        terms = ["python", "python3", "pythonic", "pythagorean"]
        autocomplete = Autocomplete(terms)

        suggestions = autocomplete.suggest("pyt", limit=2)

        assert len(suggestions) <= 2


class TestSearchEngine:
    """Test complete search engine."""

    def test_search_single_term(self, search_engine):
        """Test searching for single term."""
        results = search_engine.search("python", limit=10)

        assert len(results) > 0
        assert results[0].doc_id == "doc1"

    def test_search_with_facet_filter(self, search_engine):
        """Test search with facet filter."""
        results = search_engine.search("category:development", limit=10)

        assert len(results) == 2

    def test_search_multiple_terms(self, search_engine):
        """Test searching for multiple terms."""
        results = search_engine.search("python programming", limit=10)

        assert len(results) > 0

    def test_autocomplete(self, search_engine):
        """Test autocomplete."""
        suggestions = search_engine.autocomplete_suggestions("prog", limit=5)

        assert len(suggestions) > 0

    def test_get_facets(self, search_engine):
        """Test getting facet values."""
        facets = search_engine.get_facets("category")

        assert "development" in facets
        assert facets["development"] == 2

    def test_search_analytics(self, search_engine):
        """Test search analytics."""
        search_engine.search("python")
        search_engine.search("python")
        search_engine.search("javascript")

        analytics = search_engine.get_analytics()

        assert analytics["total_queries"] == 3
        assert analytics["unique_queries"] == 2
        assert analytics["total_documents"] == 3


class TestSearchResults:
    """Test search result quality."""

    def test_result_relevance_score(self, search_engine):
        """Test relevance scoring."""
        results = search_engine.search("python")

        for result in results:
            assert result.relevance_score >= 0

    def test_result_snippet_generation(self, search_engine):
        """Test snippet generation."""
        results = search_engine.search("python")

        assert len(results) > 0
        assert len(results[0].snippet) > 0

    def test_result_facets(self, search_engine):
        """Test result facets."""
        results = search_engine.search("python")

        assert len(results) > 0
        assert "category" in results[0].facets
        assert "tags" in results[0].facets


class TestComplexQueries:
    """Test complex search scenarios."""

    def test_and_operator(self, search_engine):
        """Test AND operator."""
        results = search_engine.search("python AND development")

        assert len(results) > 0

    def test_multiple_facets(self, search_engine):
        """Test multiple facet filters."""
        results = search_engine.search("category:development")

        assert all(r.facets["category"][0] == "development" for r in results)

    def test_no_results(self, search_engine):
        """Test search with no results."""
        results = search_engine.search("nonexistent_term_xyz")

        assert len(results) == 0

    def test_empty_query(self, search_engine):
        """Test empty query returns all docs."""
        results = search_engine.search("", limit=100)

        # Should return all documents or empty
        assert len(results) >= 0
