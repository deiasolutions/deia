"""
Advanced Search Engine - Full-text search, faceting, relevance ranking, and analytics.

Enterprise search capabilities for DEIA documents with advanced query parsing,
relevance algorithms, autocomplete, and spelling correction.
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Iterator
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import re
from enum import Enum
import math


# ===== CORE DATA STRUCTURES =====

class QueryOperator(Enum):
    """Query operators for advanced search syntax."""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclass
class Document:
    """Indexed document."""
    doc_id: str
    title: str
    content: str
    category: str
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """Single search result."""
    doc_id: str
    title: str
    relevance_score: float
    snippet: str
    facets: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchQuery:
    """Parsed search query."""
    terms: List[str]
    operators: List[QueryOperator]
    facets: Dict[str, List[str]] = field(default_factory=dict)
    filters: Dict[str, str] = field(default_factory=dict)


# ===== TOKENIZATION & ANALYSIS =====

class Tokenizer:
    """Tokenize and normalize text for indexing."""

    # Common stop words
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "up", "about", "into", "through", "during"
    }

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize text into words."""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation and split
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    @staticmethod
    def normalize(tokens: List[str]) -> List[str]:
        """Remove stop words and apply stemming."""
        # Remove stop words
        normalized = [t for t in tokens if t not in Tokenizer.STOP_WORDS and len(t) > 2]
        # Apply simple stemming (remove common suffixes)
        stemmed = [Tokenizer.simple_stem(t) for t in normalized]
        return stemmed

    @staticmethod
    def simple_stem(word: str) -> str:
        """Simple stemming by removing common suffixes."""
        if word.endswith("ing"):
            return word[:-3]
        elif word.endswith("ed"):
            return word[:-2]
        elif word.endswith("ies"):
            return word[:-3] + "y"
        elif word.endswith("es"):
            return word[:-2]
        elif word.endswith("s"):
            return word[:-1]
        return word


class SpellingCorrector:
    """Simple spelling correction using edit distance."""

    def __init__(self, vocabulary: Set[str]):
        self.vocabulary = vocabulary

    def correct(self, word: str, max_distance: int = 2) -> Optional[str]:
        """Find closest matching word in vocabulary."""
        if word in self.vocabulary:
            return word

        # Find words within edit distance
        candidates = []
        for vocab_word in self.vocabulary:
            distance = self.edit_distance(word, vocab_word)
            if distance <= max_distance:
                candidates.append((vocab_word, distance))

        if candidates:
            # Return closest match
            return min(candidates, key=lambda x: x[1])[0]

        return None

    @staticmethod
    def edit_distance(word1: str, word2: str) -> int:
        """Calculate Levenshtein distance."""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

        return dp[m][n]


# ===== INDEXING =====

class InvertedIndex:
    """Inverted index for full-text search."""

    def __init__(self):
        self.index: Dict[str, Set[str]] = defaultdict(set)  # term -> doc_ids
        self.doc_term_freq: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.documents: Dict[str, Document] = {}

    def index_document(self, doc: Document) -> None:
        """Index a document."""
        self.documents[doc.doc_id] = doc

        # Tokenize and normalize content
        tokens = Tokenizer.tokenize(doc.content + " " + doc.title)
        normalized = Tokenizer.normalize(tokens)

        # Build index
        self.doc_lengths[doc.doc_id] = len(normalized)

        for term in normalized:
            self.index[term].add(doc.doc_id)
            self.doc_term_freq[doc.doc_id][term] += 1

    def search(self, term: str) -> Set[str]:
        """Find documents containing term."""
        return self.index.get(term, set())

    def get_tf(self, doc_id: str, term: str) -> float:
        """Get term frequency for a document."""
        if doc_id not in self.doc_term_freq:
            return 0.0
        return self.doc_term_freq[doc_id].get(term, 0) / max(self.doc_lengths.get(doc_id, 1), 1)

    def get_idf(self, term: str) -> float:
        """Get inverse document frequency."""
        num_docs = len(self.documents)
        doc_count = len(self.index.get(term, set()))
        if doc_count == 0:
            return 0.0
        return math.log(num_docs / doc_count)


class FacetIndex:
    """Index for faceted search."""

    def __init__(self):
        self.facets: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))

    def index_document(self, doc: Document) -> None:
        """Index document facets."""
        # Category facet
        self.facets["category"][doc.category].add(doc.doc_id)

        # Tag facets
        for tag in doc.tags:
            self.facets["tags"][tag].add(doc.doc_id)

    def get_facet_values(self, facet_name: str) -> Dict[str, int]:
        """Get all values for a facet with counts."""
        if facet_name not in self.facets:
            return {}

        return {value: len(docs) for value, docs in self.facets[facet_name].items()}

    def filter_by_facet(self, facet_name: str, value: str) -> Set[str]:
        """Get documents matching facet value."""
        return self.facets[facet_name].get(value, set())


# ===== QUERY PARSING =====

class QueryParser:
    """Parse advanced search queries."""

    def parse(self, query_string: str) -> SearchQuery:
        """Parse query string with AND, OR, NOT operators."""
        # Extract facet filters (e.g., category:development)
        facet_pattern = r'(\w+):(\w+)'
        facets = re.findall(facet_pattern, query_string)
        query_string = re.sub(facet_pattern, '', query_string)

        # Split by operators
        terms = []
        operators = []

        # Replace AND, OR, NOT with tokens
        words = query_string.split()

        for word in words:
            upper_word = word.upper()
            if upper_word in ["AND", "OR"]:
                operators.append(QueryOperator[upper_word])
            elif upper_word == "NOT":
                operators.append(QueryOperator.NOT)
            elif word.strip():
                terms.append(word.strip())

        # Build facet dict
        facet_dict = defaultdict(list)
        for facet_name, value in facets:
            facet_dict[facet_name].append(value)

        return SearchQuery(
            terms=terms,
            operators=operators,
            facets=dict(facet_dict)
        )


# ===== RELEVANCE RANKING =====

class RelevanceRanker:
    """Calculate relevance scores using TF-IDF."""

    def __init__(self, inverted_index: InvertedIndex):
        self.index = inverted_index

    def rank(self, terms: List[str], candidates: Set[str]) -> List[Tuple[str, float]]:
        """Rank documents by relevance to query terms."""
        scores: Dict[str, float] = defaultdict(float)

        for doc_id in candidates:
            score = 0.0
            for term in terms:
                tf = self.index.get_tf(doc_id, term)
                idf = self.index.get_idf(term)
                score += tf * idf

            if score > 0:
                scores[doc_id] = score

        # Sort by score descending
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# ===== AUTOCOMPLETE =====

class Autocomplete:
    """Suggest completions for search terms."""

    def __init__(self, terms: List[str]):
        self.terms = terms
        self.trie = self._build_trie(terms)

    def suggest(self, prefix: str, limit: int = 10) -> List[str]:
        """Get suggestions for prefix."""
        prefix = prefix.lower()
        suggestions = []

        # Find all terms starting with prefix
        for term in self.terms:
            if term.startswith(prefix) and len(suggestions) < limit:
                suggestions.append(term)

        return sorted(suggestions)

    def _build_trie(self, terms: List[str]) -> Dict:
        """Build trie structure."""
        trie = {}
        for term in terms:
            node = trie
            for char in term.lower():
                if char not in node:
                    node[char] = {}
                node = node[char]
            node["$"] = True
        return trie


# ===== SEARCH ENGINE =====

class SearchEngine:
    """Complete search engine with all features."""

    def __init__(self):
        self.inverted_index = InvertedIndex()
        self.facet_index = FacetIndex()
        self.ranker = RelevanceRanker(self.inverted_index)
        self.query_parser = QueryParser()
        self.spelling_corrector: Optional[SpellingCorrector] = None
        self.autocomplete: Optional[Autocomplete] = None

        # Analytics
        self.search_queries: List[str] = []
        self.query_results: Dict[str, int] = defaultdict(int)

    def index_documents(self, documents: List[Document]) -> None:
        """Index a batch of documents."""
        for doc in documents:
            self.inverted_index.index_document(doc)
            self.facet_index.index_document(doc)

        # Build spelling corrector and autocomplete
        vocabulary = set()
        for tokens in self.inverted_index.index.keys():
            vocabulary.add(tokens)

        self.spelling_corrector = SpellingCorrector(vocabulary)
        self.autocomplete = Autocomplete(list(vocabulary))

    def search(self, query_string: str, limit: int = 10) -> List[SearchResult]:
        """Execute search with all features."""
        # Log query for analytics
        self.search_queries.append(query_string)

        # Parse query
        parsed = self.query_parser.parse(query_string)

        # Apply spelling correction
        corrected_terms = []
        for term in parsed.terms:
            if self.spelling_corrector:
                corrected = self.spelling_corrector.correct(term)
                if corrected:
                    corrected_terms.append(corrected)
            else:
                corrected_terms.append(term)

        # Find matching documents
        candidates = self._find_candidates(corrected_terms, parsed.operators)

        # Apply facet filters
        for facet_name, values in parsed.facets.items():
            facet_candidates = set()
            for value in values:
                facet_candidates.update(self.facet_index.filter_by_facet(facet_name, value))
            candidates = candidates.intersection(facet_candidates) if candidates else facet_candidates

        # Rank results
        ranked = self.ranker.rank(corrected_terms, candidates)

        # Build results
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.inverted_index.documents[doc_id]
            snippet = self._generate_snippet(doc.content, corrected_terms)

            results.append(SearchResult(
                doc_id=doc_id,
                title=doc.title,
                relevance_score=score,
                snippet=snippet,
                facets={
                    "category": [doc.category],
                    "tags": doc.tags
                },
                metadata=doc.metadata
            ))

            self.query_results[query_string] += 1

        return results

    def autocomplete_suggestions(self, prefix: str, limit: int = 10) -> List[str]:
        """Get autocomplete suggestions."""
        if not self.autocomplete:
            return []
        return self.autocomplete.suggest(prefix, limit)

    def get_facets(self, facet_name: str) -> Dict[str, int]:
        """Get all values for a facet."""
        return self.facet_index.get_facet_values(facet_name)

    def get_analytics(self) -> Dict[str, Any]:
        """Get search analytics."""
        return {
            "total_queries": len(self.search_queries),
            "unique_queries": len(set(self.search_queries)),
            "top_queries": Counter(self.search_queries).most_common(10),
            "total_documents": len(self.inverted_index.documents),
            "vocabulary_size": len(self.inverted_index.index)
        }

    def _find_candidates(self, terms: List[str], operators: List[QueryOperator]) -> Set[str]:
        """Find candidate documents matching query terms and operators."""
        if not terms:
            return set(self.inverted_index.documents.keys())

        # Start with first term
        candidates = self.inverted_index.search(terms[0])

        # Apply operators
        for i, operator in enumerate(operators):
            if i + 1 < len(terms):
                next_docs = self.inverted_index.search(terms[i + 1])

                if operator == QueryOperator.AND:
                    candidates = candidates.intersection(next_docs)
                elif operator == QueryOperator.OR:
                    candidates = candidates.union(next_docs)
                elif operator == QueryOperator.NOT:
                    all_docs = set(self.inverted_index.documents.keys())
                    candidates = candidates - next_docs

        return candidates

    def _generate_snippet(self, content: str, terms: List[str], length: int = 150) -> str:
        """Generate snippet around search terms."""
        content_lower = content.lower()

        # Find first occurrence of any search term
        first_pos = len(content)
        for term in terms:
            pos = content_lower.find(term)
            if pos != -1 and pos < first_pos:
                first_pos = pos

        if first_pos == len(content):
            # No terms found, return beginning
            return content[:length] + "..." if len(content) > length else content

        # Extract snippet around first term occurrence
        start = max(0, first_pos - 50)
        end = min(len(content), first_pos + length)

        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."

        return snippet
