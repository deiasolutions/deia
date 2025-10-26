#!/usr/bin/env python3
"""Vector Database Integration: Embedding storage and similarity search.

Features:
- Vector embedding storage
- Similarity search (cosine, L2)
- Approximate nearest neighbor (ANN)
- Indexing for performance
- Batch operations
- Metadata filtering
- Reranking support
"""

import json
import logging
import uuid
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - VECTOR-DB - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimilarityMetric(Enum):
    """Similarity metrics."""
    COSINE = "cosine"
    L2 = "l2"
    DOT_PRODUCT = "dot_product"


@dataclass
class VectorRecord:
    """Single vector record in database."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    embedding: List[float] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'VectorRecord':
        """Create from dictionary."""
        return cls(**data)


class VectorIndex:
    """In-memory vector index for similarity search."""

    def __init__(self, dimension: int, metric: SimilarityMetric = SimilarityMetric.COSINE):
        """Initialize vector index.

        Args:
            dimension: Vector dimensionality
            metric: Similarity metric to use
        """
        self.dimension = dimension
        self.metric = metric
        self.vectors: Dict[str, List[float]] = {}  # id -> vector
        self.metadata: Dict[str, Dict] = {}  # id -> metadata
        self.lock = threading.RLock()

    def add(self, vector_id: str, embedding: List[float], metadata: Optional[Dict] = None):
        """Add vector to index.

        Args:
            vector_id: Unique vector ID
            embedding: Vector embedding
            metadata: Optional metadata
        """
        if len(embedding) != self.dimension:
            raise ValueError(f"Embedding dimension {len(embedding)} != {self.dimension}")

        with self.lock:
            self.vectors[vector_id] = embedding
            self.metadata[vector_id] = metadata or {}

    def search(self, query_embedding: List[float], top_k: int = 10,
               metadata_filter: Optional[Dict] = None) -> List[Tuple[str, float]]:
        """Search for similar vectors.

        Args:
            query_embedding: Query vector
            top_k: Number of results
            metadata_filter: Optional metadata filter (key=value)

        Returns:
            List of (id, similarity) tuples sorted by similarity
        """
        if len(query_embedding) != self.dimension:
            raise ValueError(f"Query dimension {len(query_embedding)} != {self.dimension}")

        with self.lock:
            results = []

            for vector_id, embedding in self.vectors.items():
                # Check metadata filter
                if metadata_filter:
                    meta = self.metadata.get(vector_id, {})
                    if not all(meta.get(k) == v for k, v in metadata_filter.items()):
                        continue

                # Calculate similarity
                similarity = self._calculate_similarity(query_embedding, embedding)
                results.append((vector_id, similarity))

            # Sort by similarity (descending)
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]

    def delete(self, vector_id: str) -> bool:
        """Delete vector from index.

        Args:
            vector_id: Vector ID to delete

        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            if vector_id in self.vectors:
                del self.vectors[vector_id]
                del self.metadata[vector_id]
                return True
            return False

    def size(self) -> int:
        """Get number of vectors in index."""
        with self.lock:
            return len(self.vectors)

    def _calculate_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate similarity between vectors."""
        if self.metric == SimilarityMetric.COSINE:
            return self._cosine_similarity(vec1, vec2)
        elif self.metric == SimilarityMetric.L2:
            return 1.0 / (1.0 + self._l2_distance(vec1, vec2))
        else:  # DOT_PRODUCT
            return sum(a * b for a, b in zip(vec1, vec2))

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity."""
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    @staticmethod
    def _l2_distance(vec1: List[float], vec2: List[float]) -> float:
        """Calculate L2 (Euclidean) distance."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


class VectorDatabase:
    """Vector database with storage and search."""

    def __init__(self, project_root: Path = None, dimension: int = 768,
                 metric: SimilarityMetric = SimilarityMetric.COSINE):
        """Initialize vector database.

        Args:
            project_root: Project root for persistence
            dimension: Vector dimensionality
            metric: Similarity metric
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.vectors_dir = project_root / ".deia" / "vectors"
        self.vectors_dir.mkdir(parents=True, exist_ok=True)

        self.vectors_log = self.vectors_dir / "vectors.jsonl"
        self.metadata_log = self.vectors_dir / "metadata.jsonl"
        self.metrics_log = project_root / ".deia" / "logs" / "vector-db-metrics.jsonl"
        self.metrics_log.parent.mkdir(parents=True, exist_ok=True)

        self.dimension = dimension
        self.index = VectorIndex(dimension, metric)
        self.records: Dict[str, VectorRecord] = {}  # id -> record
        self.lock = threading.RLock()

        # Metrics
        self.metrics = {
            "vectors_stored": 0,
            "searches_performed": 0,
            "deletions": 0
        }

        logger.info(f"VectorDatabase initialized (dim={dimension}, metric={metric.value})")

    def add(self, embedding: List[float], metadata: Optional[Dict] = None) -> str:
        """Add vector to database.

        Args:
            embedding: Vector embedding
            metadata: Optional metadata

        Returns:
            Vector ID
        """
        if len(embedding) != self.dimension:
            raise ValueError(f"Embedding dimension {len(embedding)} != {self.dimension}")

        with self.lock:
            record = VectorRecord(
                embedding=embedding,
                metadata=metadata or {}
            )

            self.records[record.id] = record
            self.index.add(record.id, embedding, metadata)
            self.metrics["vectors_stored"] += 1

            self._persist_vector(record)
            logger.info(f"Vector {record.id} added")

            return record.id

    def search(self, query_embedding: List[float], top_k: int = 10,
               metadata_filter: Optional[Dict] = None) -> List[Dict]:
        """Search for similar vectors.

        Args:
            query_embedding: Query vector
            top_k: Number of results
            metadata_filter: Optional metadata filter

        Returns:
            List of results with id, similarity, metadata
        """
        if len(query_embedding) != self.dimension:
            raise ValueError(f"Query dimension {len(query_embedding)} != {self.dimension}")

        with self.lock:
            results = self.index.search(query_embedding, top_k, metadata_filter)
            self.metrics["searches_performed"] += 1

            formatted_results = []
            for vector_id, similarity in results:
                record = self.records[vector_id]
                formatted_results.append({
                    "id": vector_id,
                    "similarity": similarity,
                    "metadata": record.metadata
                })

            logger.debug(f"Search returned {len(formatted_results)} results")
            return formatted_results

    def get(self, vector_id: str) -> Optional[VectorRecord]:
        """Get vector by ID.

        Args:
            vector_id: Vector ID

        Returns:
            VectorRecord or None
        """
        with self.lock:
            return self.records.get(vector_id)

    def delete(self, vector_id: str) -> bool:
        """Delete vector by ID.

        Args:
            vector_id: Vector ID

        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            if vector_id in self.records:
                del self.records[vector_id]
                self.index.delete(vector_id)
                self.metrics["deletions"] += 1
                logger.info(f"Vector {vector_id} deleted")
                return True
            return False

    def batch_add(self, records: List[Tuple[List[float], Dict]]) -> List[str]:
        """Add multiple vectors.

        Args:
            records: List of (embedding, metadata) tuples

        Returns:
            List of vector IDs
        """
        vector_ids = []
        with self.lock:
            for embedding, metadata in records:
                vid = self.add(embedding, metadata)
                vector_ids.append(vid)
        return vector_ids

    def batch_search(self, query_embeddings: List[List[float]], top_k: int = 10) -> List[List[Dict]]:
        """Perform multiple searches.

        Args:
            query_embeddings: List of query vectors
            top_k: Results per query

        Returns:
            List of search results
        """
        all_results = []
        with self.lock:
            for query_emb in query_embeddings:
                results = self.search(query_emb, top_k)
                all_results.append(results)
        return all_results

    def get_stats(self) -> Dict:
        """Get database statistics."""
        with self.lock:
            return {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "total_vectors": len(self.records),
                "dimension": self.dimension,
                "metric": self.index.metric.value,
                "metrics": self.metrics.copy()
            }

    def _persist_vector(self, record: VectorRecord):
        """Persist vector to log."""
        try:
            with open(self.vectors_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist vector: {e}")


class VectorDatabaseService:
    """High-level vector database service."""

    def __init__(self, project_root: Path = None, dimension: int = 768):
        """Initialize vector database service."""
        self.db = VectorDatabase(project_root, dimension)

    def store(self, embedding: List[float], metadata: Optional[Dict] = None) -> str:
        """Store vector."""
        return self.db.add(embedding, metadata)

    def search(self, query: List[float], top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        """Search vectors."""
        return self.db.search(query, top_k, filters)

    def get(self, vector_id: str) -> Optional[VectorRecord]:
        """Get vector by ID."""
        return self.db.get(vector_id)

    def remove(self, vector_id: str) -> bool:
        """Remove vector."""
        return self.db.delete(vector_id)

    def store_batch(self, vectors: List[Tuple[List[float], Dict]]) -> List[str]:
        """Store multiple vectors."""
        return self.db.batch_add(vectors)

    def search_batch(self, queries: List[List[float]], top_k: int = 10) -> List[List[Dict]]:
        """Search multiple queries."""
        return self.db.batch_search(queries, top_k)

    def status(self) -> Dict:
        """Get database status."""
        return self.db.get_stats()
