import json
import logging
from pathlib import Path
from typing import List

from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchResult:
    def __init__(self, pattern_id: str, title: str, path: str, relevance_score: float, summary: str):
        self.pattern_id = pattern_id
        self.title = title
        self.path = path
        self.relevance_score = relevance_score
        self.summary = summary

class EnhancedBOKSearch:
    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self.patterns = self._load_patterns()
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform([p["content"] for p in self.patterns])

    def _load_patterns(self) -> List[dict]:
        with open(self.index_path, "r") as f:
            return json.load(f)

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        query_vector = self.vectorizer.transform([query])
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = similarity_scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            pattern = self.patterns[idx]
            results.append(SearchResult(
                pattern_id=pattern["id"],
                title=pattern["title"],
                path=pattern["path"],
                relevance_score=similarity_scores[idx],
                summary=pattern["summary"]
            ))

        return results

    def fuzzy_search(self, query: str, threshold: float = 0.8) -> List[SearchResult]:
        results = []
        for pattern in self.patterns:
            ratio = fuzz.ratio(query.lower(), pattern["title"].lower())
            if ratio >= threshold * 100:
                results.append(SearchResult(
                    pattern_id=pattern["id"],
                    title=pattern["title"],
                    path=pattern["path"],
                    relevance_score=ratio / 100,
                    summary=pattern["summary"]
                ))

        return sorted(results, key=lambda x: x.relevance_score, reverse=True)

    def find_related(self, pattern_id: str, top_k: int = 3) -> List[str]:
        pattern_idx = next((i for i, p in enumerate(self.patterns) if p["id"] == pattern_id), None)
        if pattern_idx is None:
            return []

        similarity_scores = cosine_similarity(self.tfidf_matrix[pattern_idx], self.tfidf_matrix).flatten()
        top_indices = similarity_scores.argsort()[::-1][1:top_k+1]

        return [self.patterns[idx]["id"] for idx in top_indices]

    def log_search(self, query: str, results: List[SearchResult]):
        logger.info(f"Search: {query}")
        for result in results:
            logger.info(f"- {result.title} (score: {result.relevance_score:.2f})")

# Usage example
if __name__ == "__main__":
    bok_search = EnhancedBOKSearch("path/to/bok_index.json")

    query = "python list comprehension"
    results = bok_search.search(query)
    bok_search.log_search(query, results)

    fuzzy_query = "pyhton list comprension"
    fuzzy_results = bok_search.fuzzy_search(fuzzy_query)
    bok_search.log_search(fuzzy_query, fuzzy_results)

    related_patterns = bok_search.find_related(results[0].pattern_id)
    print(f"Related patterns to {results[0].title}: {related_patterns}")
