"""
Enhanced BOK Search

Provides advanced search capabilities for the Body of Knowledge (BOK):
- Semantic search using TF-IDF vectorization
- Fuzzy search with typo tolerance
- Related pattern discovery
- Comprehensive search result ranking

This component extends basic BOK search with machine learning-based
relevance scoring and fuzzy matching for improved search accuracy.

Author: Agent BC (implementation) + CLAUDE-CODE-004 (integration)
Date: 2025-10-18
Source: Agent BC Phase 3 Extended
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# Optional dependencies (graceful degradation)
try:
    from rapidfuzz import fuzz
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False
    logging.warning("rapidfuzz not available - fuzzy search disabled")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available - semantic search disabled")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """
    Represents a single search result from BOK search.

    Attributes:
        pattern_id: Unique identifier for the pattern
        title: Pattern title
        path: File path to the pattern
        relevance_score: Relevance score (0.0 to 1.0)
        summary: Brief summary of the pattern
        metadata: Optional additional metadata
    """
    pattern_id: str
    title: str
    path: str
    relevance_score: float
    summary: str
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "pattern_id": self.pattern_id,
            "title": self.title,
            "path": self.path,
            "relevance_score": self.relevance_score,
            "summary": self.summary,
            "metadata": self.metadata or {}
        }


class EnhancedBOKSearch:
    """
    Enhanced search engine for the Body of Knowledge.

    Provides semantic search using TF-IDF vectorization, fuzzy search
    with typo tolerance, and related pattern discovery based on content
    similarity.

    Attributes:
        index_path (Path): Path to BOK index JSON file
        patterns (List[Dict]): Loaded pattern data
        vectorizer (TfidfVectorizer): TF-IDF vectorizer for semantic search
        tfidf_matrix: Pre-computed TF-IDF matrix for all patterns
    """
    def __init__(
        self,
        index_path: str,
        min_df: int = 1,
        max_df: float = 1.0,
        auto_load: bool = True
    ):
        """
        Initialize Enhanced BOK Search.

        Args:
            index_path: Path to BOK index JSON file
            min_df: Minimum document frequency for TF-IDF (default: 1)
            max_df: Maximum document frequency for TF-IDF (default: 1.0)
            auto_load: Whether to load patterns on initialization (default: True)

        Raises:
            FileNotFoundError: If index file doesn't exist
            ValueError: If scikit-learn not available
        """
        self.index_path = Path(index_path)
        self.patterns: List[Dict] = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self.min_df = min_df
        self.max_df = max_df

        if not SKLEARN_AVAILABLE:
            logger.warning(
                "scikit-learn not available - semantic search will be disabled. "
                "Install with: pip install scikit-learn"
            )

        if auto_load:
            self._load_and_index()

    def _load_patterns(self) -> List[Dict]:
        """
        Load patterns from BOK index file.

        Returns:
            List of pattern dictionaries

        Raises:
            FileNotFoundError: If index file doesn't exist
            json.JSONDecodeError: If index file is invalid JSON
        """
        if not self.index_path.exists():
            raise FileNotFoundError(f"BOK index not found: {self.index_path}")

        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                patterns = json.load(f)

            logger.info(f"Loaded {len(patterns)} patterns from {self.index_path}")
            return patterns
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in BOK index: {e}")
            raise

    def _load_and_index(self):
        """Load patterns and build TF-IDF index."""
        self.patterns = self._load_patterns()

        if SKLEARN_AVAILABLE and self.patterns:
            self._build_tfidf_index()

    def _build_tfidf_index(self):
        """Build TF-IDF index for semantic search."""
        if not self.patterns:
            logger.warning("No patterns to index")
            return

        # Extract content for vectorization
        contents = [p.get("content", "") for p in self.patterns]

        # Build TF-IDF matrix
        self.vectorizer = TfidfVectorizer(
            min_df=self.min_df,
            max_df=self.max_df
        )

        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(contents)
            logger.info(f"Built TF-IDF index for {len(self.patterns)} patterns")
        except Exception as e:
            logger.error(f"Failed to build TF-IDF index: {e}")
            self.vectorizer = None
            self.tfidf_matrix = None

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Perform semantic search on BOK using TF-IDF similarity.

        Args:
            query: Search query string
            top_k: Number of top results to return (default: 5)

        Returns:
            List of SearchResult objects, sorted by relevance (highest first)

        Raises:
            ValueError: If semantic search is not available
        """
        if not SKLEARN_AVAILABLE:
            raise ValueError(
                "Semantic search requires scikit-learn. "
                "Install with: pip install scikit-learn"
            )

        if not self.vectorizer or self.tfidf_matrix is None:
            logger.warning("TF-IDF index not built - no results")
            return []

        if not query or not query.strip():
            return []

        # Vectorize query
        query_vector = self.vectorizer.transform([query])

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Get top K indices
        top_indices = similarity_scores.argsort()[::-1][:top_k]

        # Build results
        results = []
        for idx in top_indices:
            if similarity_scores[idx] > 0:  # Only include positive scores
                pattern = self.patterns[idx]
                results.append(SearchResult(
                    pattern_id=pattern.get("id", str(idx)),
                    title=pattern.get("title", "Untitled"),
                    path=pattern.get("path", ""),
                    relevance_score=float(similarity_scores[idx]),
                    summary=pattern.get("summary", ""),
                    metadata=pattern.get("metadata", {})
                ))

        return results

    def fuzzy_search(
        self,
        query: str,
        threshold: float = 0.8,
        max_results: Optional[int] = None
    ) -> List[SearchResult]:
        """
        Perform fuzzy search on pattern titles (typo-tolerant).

        Uses fuzzy string matching to find patterns even with typos
        or minor variations in the query.

        Args:
            query: Search query string
            threshold: Minimum similarity ratio (0.0 to 1.0, default: 0.8)
            max_results: Maximum number of results (None for all matches)

        Returns:
            List of SearchResult objects, sorted by relevance (highest first)

        Raises:
            ValueError: If rapidfuzz is not available
        """
        if not RAPIDFUZZ_AVAILABLE:
            raise ValueError(
                "Fuzzy search requires rapidfuzz. "
                "Install with: pip install rapidfuzz"
            )

        if not query or not query.strip():
            return []

        results = []
        query_lower = query.lower()

        for pattern in self.patterns:
            title = pattern.get("title", "")

            # Calculate fuzzy ratio (0-100)
            ratio = fuzz.ratio(query_lower, title.lower())
            normalized_score = ratio / 100.0

            if normalized_score >= threshold:
                results.append(SearchResult(
                    pattern_id=pattern.get("id", ""),
                    title=title,
                    path=pattern.get("path", ""),
                    relevance_score=normalized_score,
                    summary=pattern.get("summary", ""),
                    metadata=pattern.get("metadata", {})
                ))

        # Sort by relevance (highest first)
        results.sort(key=lambda x: x.relevance_score, reverse=True)

        # Limit results if requested
        if max_results:
            results = results[:max_results]

        return results

    def find_related(
        self,
        pattern_id: str,
        top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Find patterns related to a given pattern based on content similarity.

        Args:
            pattern_id: ID of the pattern to find related patterns for
            top_k: Number of related patterns to return (default: 3)

        Returns:
            List of tuples (pattern_id, similarity_score) for related patterns

        Raises:
            ValueError: If semantic search is not available
        """
        if not SKLEARN_AVAILABLE:
            raise ValueError(
                "Related pattern search requires scikit-learn. "
                "Install with: pip install scikit-learn"
            )

        if not self.tfidf_matrix:
            logger.warning("TF-IDF index not built - no results")
            return []

        # Find pattern index
        pattern_idx = next(
            (i for i, p in enumerate(self.patterns) if p.get("id") == pattern_id),
            None
        )

        if pattern_idx is None:
            logger.warning(f"Pattern not found: {pattern_id}")
            return []

        # Calculate similarity to all other patterns
        similarity_scores = cosine_similarity(
            self.tfidf_matrix[pattern_idx],
            self.tfidf_matrix
        ).flatten()

        # Get top K indices (excluding the pattern itself)
        top_indices = similarity_scores.argsort()[::-1][1:top_k + 1]

        # Build results
        results = []
        for idx in top_indices:
            related_id = self.patterns[idx].get("id", str(idx))
            score = float(similarity_scores[idx])
            results.append((related_id, score))

        return results

    def log_search(self, query: str, results: List[SearchResult]):
        """
        Log search query and results for debugging/monitoring.

        Args:
            query: Search query string
            results: List of search results
        """
        logger.info(f"Search query: '{query}' - {len(results)} results")
        for i, result in enumerate(results, 1):
            logger.info(
                f"  {i}. {result.title} "
                f"(score: {result.relevance_score:.3f}, id: {result.pattern_id})"
            )

    def get_pattern_count(self) -> int:
        """Get total number of indexed patterns."""
        return len(self.patterns)

    def reload_index(self):
        """Reload patterns from index file and rebuild TF-IDF index."""
        logger.info("Reloading BOK index...")
        self._load_and_index()


# Standalone convenience functions

def search_bok(index_path: str, query: str, top_k: int = 5) -> List[SearchResult]:
    """
    Convenience function to perform semantic search.

    Args:
        index_path: Path to BOK index JSON file
        query: Search query
        top_k: Number of results to return

    Returns:
        List of SearchResult objects
    """
    search_engine = EnhancedBOKSearch(index_path)
    return search_engine.search(query, top_k)


def fuzzy_search_bok(
    index_path: str,
    query: str,
    threshold: float = 0.8
) -> List[SearchResult]:
    """
    Convenience function to perform fuzzy search.

    Args:
        index_path: Path to BOK index JSON file
        query: Search query
        threshold: Minimum similarity threshold

    Returns:
        List of SearchResult objects
    """
    search_engine = EnhancedBOKSearch(index_path)
    return search_engine.fuzzy_search(query, threshold)
