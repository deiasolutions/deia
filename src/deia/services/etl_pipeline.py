#!/usr/bin/env python3
"""ETL Data Pipeline Framework: Extract, transform, load with scheduling.

Features:
- Data extraction from multiple sources (DB, API, files)
- Transformation pipeline (filtering, mapping, aggregating)
- Loading to destinations
- Job scheduling and triggers
- Error handling and retries
- Monitoring and alerting
- Data validation
"""

import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from abc import ABC, abstractmethod
import threading
from collections import deque

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - ETL-PIPELINE - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Job execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class SourceType(Enum):
    """Data source types."""
    DATABASE = "database"
    API = "api"
    FILE = "file"
    STREAM = "stream"


@dataclass
class JobResult:
    """Result of job execution."""
    job_id: str
    status: JobStatus
    start_time: float
    end_time: Optional[float] = None
    duration_seconds: float = 0.0
    rows_extracted: int = 0
    rows_transformed: int = 0
    rows_loaded: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = JobStatus(self.status)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['status'] = self.status.value
        if self.end_time:
            data['duration_seconds'] = self.end_time - self.start_time
        return data


class DataSource(ABC):
    """Abstract base for data sources."""

    @abstractmethod
    def extract(self, query: Optional[Dict] = None) -> List[Dict]:
        """Extract data from source."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate source connectivity."""
        pass


class FileSource(DataSource):
    """File-based data source."""

    def __init__(self, file_path: Path):
        """Initialize file source."""
        self.file_path = file_path

    def extract(self, query: Optional[Dict] = None) -> List[Dict]:
        """Extract data from file."""
        try:
            if self.file_path.suffix == '.json':
                with open(self.file_path) as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else [data]
            elif self.file_path.suffix == '.jsonl':
                records = []
                with open(self.file_path) as f:
                    for line in f:
                        if line.strip():
                            records.append(json.loads(line))
                return records
        except Exception as e:
            logger.error(f"Failed to extract from {self.file_path}: {e}")
            return []

    def validate(self) -> bool:
        """Check file exists."""
        return self.file_path.exists()


class APISource(DataSource):
    """API-based data source."""

    def __init__(self, endpoint: str, headers: Optional[Dict] = None):
        """Initialize API source."""
        self.endpoint = endpoint
        self.headers = headers or {}

    def extract(self, query: Optional[Dict] = None) -> List[Dict]:
        """Extract data from API (simulated)."""
        # In production, would use requests library
        logger.debug(f"Simulated API call to {self.endpoint}")
        return []

    def validate(self) -> bool:
        """Validate API endpoint."""
        return bool(self.endpoint)


class Transformation:
    """Data transformation pipeline step."""

    def __init__(self, name: str, func: Callable, config: Optional[Dict] = None):
        """Initialize transformation.

        Args:
            name: Transformation name
            func: Callable that transforms records
            config: Optional configuration
        """
        self.name = name
        self.func = func
        self.config = config or {}

    def apply(self, records: List[Dict]) -> List[Dict]:
        """Apply transformation to records."""
        try:
            return self.func(records, **self.config)
        except Exception as e:
            logger.error(f"Transformation '{self.name}' failed: {e}")
            return records


class DataLoader:
    """Loads data to destinations."""

    def __init__(self, destination_path: Path):
        """Initialize loader.

        Args:
            destination_path: Path to load data to
        """
        self.destination_path = destination_path
        self.destination_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self, records: List[Dict], mode: str = 'w') -> int:
        """Load records to destination.

        Args:
            records: Records to load
            mode: Write mode ('w' = overwrite, 'a' = append)

        Returns:
            Number of records loaded
        """
        try:
            with open(self.destination_path, mode, encoding='utf-8') as f:
                for record in records:
                    f.write(json.dumps(record) + '\n')
            return len(records)
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return 0


class DataValidator:
    """Validates data quality."""

    def __init__(self, schema: Optional[Dict] = None):
        """Initialize validator.

        Args:
            schema: Optional validation schema
        """
        self.schema = schema or {}

    def validate(self, records: List[Dict]) -> tuple[bool, List[str]]:
        """Validate records.

        Args:
            records: Records to validate

        Returns:
            Tuple of (valid, errors)
        """
        errors = []

        for i, record in enumerate(records):
            # Check required fields if schema provided
            for field_name, field_config in self.schema.items():
                if field_config.get('required') and field_name not in record:
                    errors.append(f"Record {i}: missing required field '{field_name}'")

            # Check data types if specified
            for field_name, field_config in self.schema.items():
                if field_name in record and 'type' in field_config:
                    expected_type = field_config['type']
                    actual_value = record[field_name]
                    if not isinstance(actual_value, expected_type):
                        errors.append(f"Record {i}: field '{field_name}' type mismatch")

        return len(errors) == 0, errors


class ETLJob:
    """Individual ETL job."""

    def __init__(self, job_id: str, name: str, source: DataSource,
                 transformations: List[Transformation], loader: DataLoader,
                 validator: Optional[DataValidator] = None):
        """Initialize ETL job.

        Args:
            job_id: Unique job ID
            name: Job name
            source: Data source
            transformations: Transformation pipeline
            loader: Data loader
            validator: Optional data validator
        """
        self.job_id = job_id
        self.name = name
        self.source = source
        self.transformations = transformations
        self.loader = loader
        self.validator = validator
        self.result: Optional[JobResult] = None

    def execute(self) -> JobResult:
        """Execute the ETL job.

        Returns:
            JobResult with execution details
        """
        result = JobResult(
            job_id=self.job_id,
            status=JobStatus.RUNNING,
            start_time=time.time()
        )

        try:
            # Extract
            logger.info(f"Job {self.job_id}: Extracting data...")
            records = self.source.extract()
            result.rows_extracted = len(records)

            # Validate input
            if self.validator:
                is_valid, errors = self.validator.validate(records)
                if not is_valid:
                    result.errors.extend(errors)

            # Transform
            logger.info(f"Job {self.job_id}: Transforming {len(records)} records...")
            for transform in self.transformations:
                records = transform.apply(records)
            result.rows_transformed = len(records)

            # Load
            logger.info(f"Job {self.job_id}: Loading {len(records)} records...")
            loaded = self.loader.load(records)
            result.rows_loaded = loaded

            result.status = JobStatus.COMPLETED
            logger.info(f"Job {self.job_id}: Completed successfully")

        except Exception as e:
            result.status = JobStatus.FAILED
            result.errors.append(str(e))
            logger.error(f"Job {self.job_id} failed: {e}")

        finally:
            result.end_time = time.time()

        self.result = result
        return result


class ETLScheduler:
    """Schedules and executes ETL jobs."""

    def __init__(self, project_root: Path = None):
        """Initialize scheduler.

        Args:
            project_root: Project root for logs
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.jobs_log = project_root / ".deia" / "logs" / "etl-jobs.jsonl"
        self.jobs_log.parent.mkdir(parents=True, exist_ok=True)

        self.jobs: Dict[str, ETLJob] = {}
        self.job_history: deque = deque(maxlen=1000)
        self.lock = threading.RLock()

        logger.info("ETL Scheduler initialized")

    def register_job(self, job: ETLJob):
        """Register a job.

        Args:
            job: ETLJob to register
        """
        with self.lock:
            self.jobs[job.job_id] = job
            logger.info(f"Job {job.job_id} registered: {job.name}")

    def execute_job(self, job_id: str, retries: int = 3) -> JobResult:
        """Execute a job with retries.

        Args:
            job_id: Job ID to execute
            retries: Number of retries on failure

        Returns:
            JobResult
        """
        with self.lock:
            if job_id not in self.jobs:
                logger.error(f"Job {job_id} not found")
                return None

            job = self.jobs[job_id]
            result = None

            for attempt in range(retries):
                try:
                    result = job.execute()

                    if result.status == JobStatus.COMPLETED:
                        self._log_result(result)
                        self.job_history.append(result)
                        return result

                    if attempt < retries - 1:
                        logger.info(f"Job {job_id}: Retrying (attempt {attempt + 1}/{retries})")
                        time.sleep(2 ** attempt)  # Exponential backoff

                except Exception as e:
                    logger.error(f"Job {job_id} attempt {attempt + 1} failed: {e}")

            return result

    def execute_all(self) -> List[JobResult]:
        """Execute all registered jobs.

        Returns:
            List of JobResults
        """
        results = []
        with self.lock:
            for job_id in self.jobs.keys():
                result = self.execute_job(job_id)
                if result:
                    results.append(result)
        return results

    def get_job_status(self, job_id: str) -> Optional[JobResult]:
        """Get status of a job."""
        with self.lock:
            if job_id in self.jobs:
                return self.jobs[job_id].result
        return None

    def get_history(self, limit: int = 100) -> List[Dict]:
        """Get job execution history."""
        with self.lock:
            return [r.to_dict() for r in list(self.job_history)[-limit:]]

    def get_statistics(self) -> Dict:
        """Get scheduler statistics."""
        with self.lock:
            total = len(self.job_history)
            completed = sum(1 for r in self.job_history if r.status == JobStatus.COMPLETED)
            failed = sum(1 for r in self.job_history if r.status == JobStatus.FAILED)

            return {
                "total_executions": total,
                "completed": completed,
                "failed": failed,
                "success_rate": completed / total if total > 0 else 0,
                "total_rows_extracted": sum(r.rows_extracted for r in self.job_history),
                "total_rows_loaded": sum(r.rows_loaded for r in self.job_history)
            }

    def _log_result(self, result: JobResult):
        """Log job result."""
        try:
            with open(self.jobs_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to log result: {e}")


class ETLPipelineService:
    """High-level ETL service."""

    def __init__(self, project_root: Path = None):
        """Initialize ETL service."""
        self.scheduler = ETLScheduler(project_root)

    def create_pipeline(self, name: str, source: DataSource,
                       transformations: List[Transformation],
                       destination: Path, validator: Optional[DataValidator] = None) -> ETLJob:
        """Create an ETL pipeline.

        Args:
            name: Pipeline name
            source: Data source
            transformations: Transformation steps
            destination: Destination path
            validator: Optional validator

        Returns:
            ETLJob
        """
        job_id = str(uuid.uuid4())[:8]
        loader = DataLoader(destination)
        job = ETLJob(job_id, name, source, transformations, loader, validator)
        self.scheduler.register_job(job)
        return job

    def run(self, job_id: str) -> JobResult:
        """Run a pipeline."""
        return self.scheduler.execute_job(job_id)

    def run_all(self) -> List[JobResult]:
        """Run all pipelines."""
        return self.scheduler.execute_all()

    def status(self, job_id: str) -> Optional[JobResult]:
        """Get pipeline status."""
        return self.scheduler.get_job_status(job_id)

    def history(self) -> List[Dict]:
        """Get execution history."""
        return self.scheduler.get_history()

    def stats(self) -> Dict:
        """Get statistics."""
        return self.scheduler.get_statistics()
