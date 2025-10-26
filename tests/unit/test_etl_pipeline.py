#!/usr/bin/env python3
"""Tests for ETL Data Pipeline."""

import pytest
import tempfile
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.etl_pipeline import (
    JobStatus,
    SourceType,
    JobResult,
    FileSource,
    APISource,
    Transformation,
    DataLoader,
    DataValidator,
    ETLJob,
    ETLScheduler,
    ETLPipelineService
)


class TestFileSource:
    """Test file data source."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_json_extraction(self, temp_dir):
        """Test extracting from JSON file."""
        data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        json_file = temp_dir / "data.json"
        with open(json_file, 'w') as f:
            json.dump(data, f)

        source = FileSource(json_file)
        records = source.extract()

        assert len(records) == 2
        assert records[0]["name"] == "Alice"

    def test_jsonl_extraction(self, temp_dir):
        """Test extracting from JSONL file."""
        jsonl_file = temp_dir / "data.jsonl"
        with open(jsonl_file, 'w') as f:
            f.write('{"id": 1, "value": "a"}\n')
            f.write('{"id": 2, "value": "b"}\n')

        source = FileSource(jsonl_file)
        records = source.extract()

        assert len(records) == 2
        assert records[1]["id"] == 2

    def test_source_validation(self, temp_dir):
        """Test source validation."""
        json_file = temp_dir / "exists.json"
        json_file.write_text("[]")

        source = FileSource(json_file)
        assert source.validate() is True

        missing_file = temp_dir / "missing.json"
        source_missing = FileSource(missing_file)
        assert source_missing.validate() is False


class TestAPISource:
    """Test API data source."""

    def test_api_source_creation(self):
        """Test creating API source."""
        source = APISource("https://api.example.com/data")
        assert source.endpoint == "https://api.example.com/data"

    def test_api_source_validation(self):
        """Test API source validation."""
        source = APISource("https://api.example.com")
        assert source.validate() is True

        empty_source = APISource("")
        assert empty_source.validate() is False


class TestTransformation:
    """Test data transformations."""

    def test_filter_transformation(self):
        """Test filtering transformation."""
        def filter_func(records, **config):
            min_val = config.get('min_val', 0)
            return [r for r in records if r.get('value', 0) >= min_val]

        transform = Transformation("filter", filter_func, {"min_val": 5})
        records = [{"id": 1, "value": 3}, {"id": 2, "value": 7}]
        result = transform.apply(records)

        assert len(result) == 1
        assert result[0]["value"] == 7

    def test_mapping_transformation(self):
        """Test mapping transformation."""
        def map_func(records, **config):
            return [{"id": r["id"], "name": r["name"].upper()} for r in records]

        transform = Transformation("map", map_func)
        records = [{"id": 1, "name": "alice"}]
        result = transform.apply(records)

        assert result[0]["name"] == "ALICE"

    def test_aggregation_transformation(self):
        """Test aggregation transformation."""
        def agg_func(records, **config):
            return [{
                "count": len(records),
                "total": sum(r.get("value", 0) for r in records)
            }]

        transform = Transformation("aggregate", agg_func)
        records = [{"value": 10}, {"value": 20}, {"value": 30}]
        result = transform.apply(records)

        assert result[0]["count"] == 3
        assert result[0]["total"] == 60


class TestDataLoader:
    """Test data loader."""

    def test_load_records(self):
        """Test loading records."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.jsonl"
            loader = DataLoader(output_file)

            records = [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]
            loaded = loader.load(records)

            assert loaded == 2
            assert output_file.exists()

    def test_append_mode(self):
        """Test append mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.jsonl"
            loader = DataLoader(output_file)

            loader.load([{"id": 1}])
            loader.load([{"id": 2}], mode='a')

            with open(output_file) as f:
                lines = f.readlines()
            assert len(lines) == 2


class TestDataValidator:
    """Test data validation."""

    def test_required_field_validation(self):
        """Test required field validation."""
        schema = {"id": {"required": True}, "name": {"required": True}}
        validator = DataValidator(schema)

        records = [{"id": 1, "name": "Alice"}]
        valid, errors = validator.validate(records)

        assert valid is True
        assert len(errors) == 0

    def test_missing_required_field(self):
        """Test validation with missing field."""
        schema = {"id": {"required": True}}
        validator = DataValidator(schema)

        records = [{"name": "Alice"}]  # Missing id
        valid, errors = validator.validate(records)

        assert valid is False
        assert len(errors) > 0

    def test_type_validation(self):
        """Test type validation."""
        schema = {"id": {"type": int}, "name": {"type": str}}
        validator = DataValidator(schema)

        records = [{"id": 1, "name": "Alice"}]
        valid, errors = validator.validate(records)

        assert valid is True


class TestETLJob:
    """Test ETL job execution."""

    @pytest.fixture
    def job_setup(self):
        """Setup for ETL job tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create source file
            source_file = tmpdir / "source.jsonl"
            with open(source_file, 'w') as f:
                f.write('{"id": 1, "value": 100}\n')
                f.write('{"id": 2, "value": 200}\n')

            source = FileSource(source_file)
            dest_file = tmpdir / "dest.jsonl"
            loader = DataLoader(dest_file)

            yield {
                "source": source,
                "loader": loader,
                "dest_file": dest_file,
                "tmpdir": tmpdir
            }

    def test_job_execution(self, job_setup):
        """Test basic job execution."""
        setup = job_setup
        job = ETLJob(
            "job-1",
            "test_job",
            setup["source"],
            [],
            setup["loader"]
        )

        result = job.execute()

        assert result.status == JobStatus.COMPLETED
        assert result.rows_extracted == 2
        assert result.rows_loaded == 2

    def test_job_with_transformation(self, job_setup):
        """Test job with transformation."""
        setup = job_setup

        def double_values(records, **config):
            return [{"id": r["id"], "value": r["value"] * 2} for r in records]

        transform = Transformation("double", double_values)

        job = ETLJob(
            "job-2",
            "transform_job",
            setup["source"],
            [transform],
            setup["loader"]
        )

        result = job.execute()

        assert result.status == JobStatus.COMPLETED
        assert result.rows_transformed == 2

    def test_job_with_validation(self, job_setup):
        """Test job with validation."""
        setup = job_setup
        schema = {"id": {"required": True}, "value": {"required": True}}
        validator = DataValidator(schema)

        job = ETLJob(
            "job-3",
            "validate_job",
            setup["source"],
            [],
            setup["loader"],
            validator
        )

        result = job.execute()

        assert result.status == JobStatus.COMPLETED


class TestETLScheduler:
    """Test ETL scheduler."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scheduler = ETLScheduler(Path(tmpdir))
            yield scheduler

    def test_job_registration(self, scheduler):
        """Test registering jobs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1}\n')

            source = FileSource(source_file)
            loader = DataLoader(tmpdir / "dest.jsonl")

            job = ETLJob("job-1", "test", source, [], loader)
            scheduler.register_job(job)

            assert "job-1" in scheduler.jobs

    def test_job_execution(self, scheduler):
        """Test executing a job."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1}\n{"id": 2}\n')

            source = FileSource(source_file)
            loader = DataLoader(tmpdir / "dest.jsonl")
            job = ETLJob("job-1", "test", source, [], loader)

            scheduler.register_job(job)
            result = scheduler.execute_job("job-1")

            assert result.status == JobStatus.COMPLETED
            assert result.rows_extracted == 2

    def test_execute_all_jobs(self, scheduler):
        """Test executing all jobs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            for i in range(3):
                source_file = tmpdir / f"source-{i}.jsonl"
                source_file.write_text('{"id": 1}\n')
                source = FileSource(source_file)
                loader = DataLoader(tmpdir / f"dest-{i}.jsonl")
                job = ETLJob(f"job-{i}", f"test-{i}", source, [], loader)
                scheduler.register_job(job)

            results = scheduler.execute_all()
            assert len(results) == 3

    def test_job_history(self, scheduler):
        """Test job history tracking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1}\n')

            source = FileSource(source_file)
            loader = DataLoader(tmpdir / "dest.jsonl")
            job = ETLJob("job-1", "test", source, [], loader)

            scheduler.register_job(job)
            scheduler.execute_job("job-1")

            history = scheduler.get_history()
            assert len(history) > 0

    def test_statistics(self, scheduler):
        """Test getting statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1}\n')

            source = FileSource(source_file)
            loader = DataLoader(tmpdir / "dest.jsonl")
            job = ETLJob("job-1", "test", source, [], loader)

            scheduler.register_job(job)
            scheduler.execute_job("job-1")

            stats = scheduler.get_statistics()
            assert stats["total_executions"] > 0
            assert stats["success_rate"] >= 0


class TestETLPipelineService:
    """Test high-level ETL service."""

    def test_create_pipeline(self):
        """Test creating a pipeline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1}\n')

            service = ETLPipelineService(tmpdir)
            source = FileSource(source_file)
            dest = tmpdir / "dest.jsonl"

            job = service.create_pipeline("test", source, [], dest)
            assert job is not None

    def test_run_pipeline(self):
        """Test running a pipeline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1, "value": 100}\n')

            service = ETLPipelineService(tmpdir)
            source = FileSource(source_file)

            def double(records, **config):
                return [{"id": r["id"], "value": r["value"] * 2} for r in records]

            transform = Transformation("double", double)
            dest = tmpdir / "dest.jsonl"

            job = service.create_pipeline("test", source, [transform], dest)
            result = service.run(job.job_id)

            assert result.status == JobStatus.COMPLETED

    def test_service_history(self):
        """Test service history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1}\n')

            service = ETLPipelineService(tmpdir)
            source = FileSource(source_file)
            job = service.create_pipeline("test", source, [], tmpdir / "dest.jsonl")

            service.run(job.job_id)
            history = service.history()

            assert len(history) > 0

    def test_service_stats(self):
        """Test service statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "source.jsonl"
            source_file.write_text('{"id": 1}\n')

            service = ETLPipelineService(tmpdir)
            source = FileSource(source_file)
            job = service.create_pipeline("test", source, [], tmpdir / "dest.jsonl")

            service.run(job.job_id)
            stats = service.stats()

            assert "total_rows_extracted" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
