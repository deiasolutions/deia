#!/usr/bin/env python3
"""Tests for Vector Database."""

import pytest
import tempfile
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.vector_database import (
    SimilarityMetric,
    VectorRecord,
    VectorIndex,
    VectorDatabase,
    VectorDatabaseService
)


class TestVectorRecord:
    """Test vector record."""

    def test_create_record(self):
        """Test creating vector record."""
        embedding = [0.1, 0.2, 0.3]
        record = VectorRecord(embedding=embedding, metadata={"name": "test"})

        assert record.embedding == embedding
        assert record.metadata["name"] == "test"
        assert record.created_at is not None

    def test_record_serialization(self):
        """Test record serialization."""
        record = VectorRecord(
            embedding=[0.1, 0.2],
            metadata={"key": "value"}
        )

        data = record.to_dict()
        assert data["embedding"] == [0.1, 0.2]

        record2 = VectorRecord.from_dict(data)
        assert record2.embedding == record.embedding


class TestVectorIndex:
    """Test vector indexing and search."""

    @pytest.fixture
    def index(self):
        """Create vector index."""
        return VectorIndex(dimension=3, metric=SimilarityMetric.COSINE)

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        index = VectorIndex(2, SimilarityMetric.COSINE)

        # Identical vectors
        sim = index._cosine_similarity([1, 0], [1, 0])
        assert abs(sim - 1.0) < 0.001

        # Orthogonal vectors
        sim = index._cosine_similarity([1, 0], [0, 1])
        assert abs(sim - 0.0) < 0.001

    def test_l2_distance(self):
        """Test L2 distance calculation."""
        index = VectorIndex(2, SimilarityMetric.L2)

        # Same vectors
        dist = index._l2_distance([0, 0], [0, 0])
        assert abs(dist - 0.0) < 0.001

        # Distance of 3-4-5 triangle
        dist = index._l2_distance([0, 0], [3, 4])
        assert abs(dist - 5.0) < 0.001

    def test_add_vector(self, index):
        """Test adding vector."""
        embedding = [0.1, 0.2, 0.3]
        index.add("vec-1", embedding, {"name": "test"})

        assert index.size() == 1

    def test_add_wrong_dimension(self, index):
        """Test adding vector with wrong dimension."""
        with pytest.raises(ValueError):
            index.add("vec-1", [0.1, 0.2])  # Only 2 dims, needs 3

    def test_search_similar(self, index):
        """Test searching for similar vectors."""
        # Add vectors
        index.add("vec-1", [1.0, 0.0, 0.0])
        index.add("vec-2", [0.9, 0.1, 0.0])
        index.add("vec-3", [0.0, 1.0, 0.0])

        # Search with query similar to vec-1
        results = index.search([1.0, 0.0, 0.0], top_k=2)

        assert len(results) == 2
        assert results[0][0] == "vec-1"  # Best match
        assert results[0][1] > results[1][1]  # Similarity decreases

    def test_search_with_metadata_filter(self, index):
        """Test searching with metadata filter."""
        index.add("vec-1", [1.0, 0.0, 0.0], {"type": "A"})
        index.add("vec-2", [0.9, 0.1, 0.0], {"type": "B"})
        index.add("vec-3", [0.8, 0.2, 0.0], {"type": "A"})

        # Search only for type A
        results = index.search([1.0, 0.0, 0.0], top_k=10, metadata_filter={"type": "A"})

        assert len(results) == 2
        for vec_id, _ in results:
            assert vec_id in ["vec-1", "vec-3"]

    def test_delete_vector(self, index):
        """Test deleting vector."""
        index.add("vec-1", [1.0, 0.0, 0.0])
        assert index.size() == 1

        deleted = index.delete("vec-1")
        assert deleted is True
        assert index.size() == 0

    def test_delete_nonexistent(self, index):
        """Test deleting nonexistent vector."""
        deleted = index.delete("nonexistent")
        assert deleted is False


class TestVectorDatabase:
    """Test vector database."""

    @pytest.fixture
    def db(self):
        """Create vector database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db = VectorDatabase(Path(tmpdir), dimension=3)
            yield db

    def test_add_vector(self, db):
        """Test adding vector."""
        embedding = [0.1, 0.2, 0.3]
        vector_id = db.add(embedding, {"name": "test"})

        assert vector_id is not None
        assert db.get(vector_id) is not None

    def test_add_wrong_dimension(self, db):
        """Test adding vector with wrong dimension."""
        with pytest.raises(ValueError):
            db.add([0.1, 0.2])  # Only 2 dims

    def test_search(self, db):
        """Test searching vectors."""
        db.add([1.0, 0.0, 0.0], {"label": "A"})
        db.add([0.9, 0.1, 0.0], {"label": "B"})
        db.add([0.0, 1.0, 0.0], {"label": "C"})

        results = db.search([1.0, 0.0, 0.0], top_k=2)

        assert len(results) == 2
        assert results[0]["similarity"] > results[1]["similarity"]

    def test_search_with_filter(self, db):
        """Test searching with metadata filter."""
        db.add([1.0, 0.0, 0.0], {"type": "important"})
        db.add([0.9, 0.1, 0.0], {"type": "other"})

        results = db.search([1.0, 0.0, 0.0], top_k=10, metadata_filter={"type": "important"})

        assert len(results) == 1
        assert results[0]["metadata"]["type"] == "important"

    def test_delete_vector(self, db):
        """Test deleting vector."""
        vid = db.add([0.1, 0.2, 0.3])
        assert db.get(vid) is not None

        deleted = db.delete(vid)
        assert deleted is True
        assert db.get(vid) is None

    def test_batch_add(self, db):
        """Test batch adding vectors."""
        records = [
            ([0.1, 0.2, 0.3], {"id": 1}),
            ([0.4, 0.5, 0.6], {"id": 2}),
            ([0.7, 0.8, 0.9], {"id": 3})
        ]

        vids = db.batch_add(records)

        assert len(vids) == 3
        assert db.get(vids[0]) is not None

    def test_batch_search(self, db):
        """Test batch searching."""
        db.add([1.0, 0.0, 0.0])
        db.add([0.0, 1.0, 0.0])

        queries = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
        ]

        results = db.batch_search(queries, top_k=1)

        assert len(results) == 2
        assert len(results[0]) == 1
        assert len(results[1]) == 1

    def test_get_stats(self, db):
        """Test getting statistics."""
        db.add([0.1, 0.2, 0.3])
        db.add([0.4, 0.5, 0.6])

        stats = db.get_stats()

        assert stats["total_vectors"] == 2
        assert stats["dimension"] == 3
        assert stats["metrics"]["vectors_stored"] == 2

    def test_persistence(self, db):
        """Test vector persistence."""
        db.add([0.1, 0.2, 0.3], {"name": "test"})

        vectors_log = db.vectors_log
        assert vectors_log.exists()


class TestVectorDatabaseService:
    """Test high-level vector database service."""

    @pytest.fixture
    def service(self):
        """Create vector database service."""
        with tempfile.TemporaryDirectory() as tmpdir:
            service = VectorDatabaseService(Path(tmpdir), dimension=2)
            yield service

    def test_store(self, service):
        """Test storing vector."""
        vid = service.store([0.1, 0.2], {"name": "test"})
        assert vid is not None

    def test_search(self, service):
        """Test searching."""
        service.store([1.0, 0.0], {"type": "A"})
        service.store([0.9, 0.1], {"type": "B"})

        results = service.search([1.0, 0.0], top_k=1)

        assert len(results) == 1
        assert results[0]["similarity"] > 0.9

    def test_get(self, service):
        """Test retrieving vector."""
        vid = service.store([0.5, 0.5])
        record = service.get(vid)

        assert record is not None
        assert record.embedding == [0.5, 0.5]

    def test_remove(self, service):
        """Test removing vector."""
        vid = service.store([0.1, 0.2])
        removed = service.remove(vid)

        assert removed is True
        assert service.get(vid) is None

    def test_store_batch(self, service):
        """Test batch storing."""
        vectors = [
            ([0.1, 0.2], {"id": 1}),
            ([0.3, 0.4], {"id": 2})
        ]

        vids = service.store_batch(vectors)
        assert len(vids) == 2

    def test_search_batch(self, service):
        """Test batch searching."""
        service.store([1.0, 0.0])
        service.store([0.0, 1.0])

        queries = [[1.0, 0.0], [0.0, 1.0]]
        results = service.search_batch(queries, top_k=1)

        assert len(results) == 2

    def test_status(self, service):
        """Test getting status."""
        service.store([0.1, 0.2])

        status = service.status()

        assert status["total_vectors"] == 1
        assert status["dimension"] == 2


class TestSimilarityMetrics:
    """Test different similarity metrics."""

    def test_cosine_metric(self):
        """Test cosine similarity metric."""
        index = VectorIndex(2, SimilarityMetric.COSINE)
        index.add("vec-1", [1, 0])
        index.add("vec-2", [0.7, 0.7])

        results = index.search([1, 0], top_k=2)
        assert results[0][0] == "vec-1"  # Exact match first

    def test_l2_metric(self):
        """Test L2 distance metric."""
        index = VectorIndex(2, SimilarityMetric.L2)
        index.add("vec-1", [0, 0])
        index.add("vec-2", [3, 4])

        results = index.search([0, 0], top_k=2)
        assert results[0][0] == "vec-1"  # Closest distance first

    def test_dot_product_metric(self):
        """Test dot product metric."""
        index = VectorIndex(2, SimilarityMetric.DOT_PRODUCT)
        index.add("vec-1", [1, 0])
        index.add("vec-2", [0.5, 0.5])

        results = index.search([1, 0], top_k=2)
        assert results[0][0] == "vec-1"  # Higher dot product first


class TestReranking:
    """Test reranking scenarios."""

    def test_filter_then_search(self):
        """Test searching with filters for reranking."""
        db = VectorDatabase(Path(tempfile.gettempdir()), dimension=2)

        # Add vectors with different categories
        db.add([1.0, 0.0], {"category": "important"})
        db.add([0.95, 0.05], {"category": "normal"})
        db.add([0.9, 0.1], {"category": "important"})

        # Search for important category only
        results = db.search([1.0, 0.0], top_k=10, metadata_filter={"category": "important"})

        assert len(results) == 2
        assert all(r["metadata"]["category"] == "important" for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
