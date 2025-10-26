"""
Unit tests for REST API builder service.

Tests API builder functionality including endpoint generation, validation,
rate limiting, authentication hooks, and error handling.
"""

import pytest
import json
import time
from pathlib import Path
from fastapi.testclient import TestClient

from src.deia.rest_api_builder import (
    RESTAPIBuilder, APISchema, EndpointConfig, FieldSchema,
    HTTPMethod, ValidationRule, FieldValidator, RequestTransformer,
    RateLimiter, load_api_config, create_api_builder, build_api, APIResponse
)


# ===== FIXTURES =====

@pytest.fixture
def simple_field():
    """Simple string field."""
    return FieldSchema(
        name="name",
        type="string",
        required=True,
        description="User name"
    )


@pytest.fixture
def email_field():
    """Email field with validation."""
    return FieldSchema(
        name="email",
        type="string",
        required=True,
        validations=[
            ValidationRule(type="email", message="Invalid email address")
        ]
    )


@pytest.fixture
def number_field():
    """Number field with validation."""
    return FieldSchema(
        name="age",
        type="number",
        required=True,
        validations=[
            ValidationRule(type="min_length", value=1)
        ]
    )


@pytest.fixture
def get_endpoint():
    """GET endpoint configuration."""
    return EndpointConfig(
        path="/users/{user_id}",
        method=HTTPMethod.GET,
        name="get_user",
        description="Get a user by ID",
        response_fields=[
            FieldSchema(name="id", type="string"),
            FieldSchema(name="name", type="string")
        ]
    )


@pytest.fixture
def post_endpoint():
    """POST endpoint configuration."""
    return EndpointConfig(
        path="/users",
        method=HTTPMethod.POST,
        name="create_user",
        description="Create a new user",
        request_fields=[
            FieldSchema(name="name", type="string", required=True),
            FieldSchema(name="email", type="string", required=True)
        ],
        response_fields=[
            FieldSchema(name="id", type="string"),
            FieldSchema(name="name", type="string"),
            FieldSchema(name="email", type="string")
        ]
    )


@pytest.fixture
def simple_api_schema(get_endpoint, post_endpoint):
    """Simple API schema with 2 endpoints."""
    return APISchema(
        name="Test API",
        version="1.0.0",
        description="Test API for unit tests",
        base_url="/api/v1",
        endpoints=[get_endpoint, post_endpoint],
        global_rate_limit=100
    )


@pytest.fixture
def api_builder(simple_api_schema):
    """Create API builder."""
    return RESTAPIBuilder(simple_api_schema)


@pytest.fixture
def test_client(api_builder):
    """Create test client for FastAPI app."""
    app = api_builder.build()
    return TestClient(app)


# ===== FIELD VALIDATOR TESTS =====

class TestFieldValidator:
    """Test field validation."""

    def test_validate_required_field(self, simple_field):
        """Test required field validation."""
        valid, msg = FieldValidator.validate_field("John", simple_field)
        assert valid
        assert msg is None

    def test_validate_required_field_missing(self, simple_field):
        """Test required field missing."""
        valid, msg = FieldValidator.validate_field(None, simple_field)
        assert not valid
        assert "required" in msg.lower()

    def test_validate_optional_field(self):
        """Test optional field."""
        field = FieldSchema(name="age", type="number", required=False)
        valid, msg = FieldValidator.validate_field(None, field)
        assert valid

    def test_validate_type_string(self):
        """Test string type validation."""
        field = FieldSchema(name="name", type="string", required=True)
        valid, msg = FieldValidator.validate_field("John", field)
        assert valid

    def test_validate_type_number(self):
        """Test number type validation."""
        field = FieldSchema(name="age", type="number", required=True)
        valid, msg = FieldValidator.validate_field(25, field)
        assert valid

    def test_validate_type_mismatch(self):
        """Test type mismatch."""
        field = FieldSchema(name="age", type="number", required=True)
        valid, msg = FieldValidator.validate_field("not a number", field)
        assert not valid

    def test_validate_email(self, email_field):
        """Test email validation."""
        valid, msg = FieldValidator.validate_field("test@example.com", email_field)
        assert valid

    def test_validate_email_invalid(self, email_field):
        """Test invalid email."""
        valid, msg = FieldValidator.validate_field("invalid-email", email_field)
        assert not valid

    def test_validate_min_length(self):
        """Test minimum length validation."""
        field = FieldSchema(
            name="username",
            type="string",
            required=True,
            validations=[ValidationRule(type="min_length", value=3)]
        )
        valid, msg = FieldValidator.validate_field("ab", field)
        assert not valid

    def test_validate_max_length(self):
        """Test maximum length validation."""
        field = FieldSchema(
            name="username",
            type="string",
            required=True,
            validations=[ValidationRule(type="max_length", value=10)]
        )
        valid, msg = FieldValidator.validate_field("this is a very long string", field)
        assert not valid

    def test_validate_pattern(self):
        """Test pattern validation."""
        field = FieldSchema(
            name="phone",
            type="string",
            required=True,
            validations=[ValidationRule(type="pattern", value=r"^\d{3}-\d{3}-\d{4}$")]
        )
        valid, msg = FieldValidator.validate_field("123-456-7890", field)
        assert valid


# ===== REQUEST TRANSFORMER TESTS =====

class TestRequestTransformer:
    """Test request transformation."""

    def test_transform_simple_request(self, simple_field):
        """Test transforming simple request."""
        data = {"name": "John"}
        result, error = RequestTransformer.transform_request(data, [simple_field])
        assert error is None
        assert result["name"] == "John"

    def test_transform_with_default(self):
        """Test transformation with default value."""
        field = FieldSchema(name="role", type="string", required=False, default="user")
        data = {}
        result, error = RequestTransformer.transform_request(data, [field])
        assert error is None
        assert result["role"] == "user"

    def test_transform_validation_failure(self, email_field):
        """Test transformation with validation failure."""
        data = {"email": "invalid"}
        result, error = RequestTransformer.transform_request(data, [email_field])
        assert error is not None
        assert result is None

    def test_transform_response(self, simple_field):
        """Test response transformation."""
        data = {"name": "John"}
        result = RequestTransformer.transform_response(data, [simple_field])
        assert result["name"] == "John"


# ===== RATE LIMITER TESTS =====

class TestRateLimiter:
    """Test rate limiting."""

    def test_rate_limiter_initialization(self):
        """Test rate limiter creation."""
        limiter = RateLimiter(60)
        assert limiter.requests_per_minute == 60

    def test_rate_limiter_allows_request(self):
        """Test allowing requests within limit."""
        limiter = RateLimiter(10)
        for i in range(10):
            assert limiter.is_allowed("client1")

    def test_rate_limiter_rejects_excess(self):
        """Test rejecting requests over limit."""
        limiter = RateLimiter(5)
        for i in range(5):
            limiter.is_allowed("client1")

        # 6th request should be rejected
        assert not limiter.is_allowed("client1")

    def test_rate_limiter_per_client(self):
        """Test per-client rate limiting."""
        limiter = RateLimiter(5)
        for i in range(5):
            limiter.is_allowed("client1")

        # client2 should still be allowed
        assert limiter.is_allowed("client2")

    def test_rate_limiter_time_window(self):
        """Test rate limit time window (60 seconds)."""
        limiter = RateLimiter(1)
        assert limiter.is_allowed("client1")

        # Second request in same minute should fail
        assert not limiter.is_allowed("client1")


# ===== API BUILDER TESTS =====

class TestAPIBuilder:
    """Test API builder functionality."""

    def test_builder_initialization(self, simple_api_schema):
        """Test builder initialization."""
        builder = RESTAPIBuilder(simple_api_schema)
        assert builder.config.name == "Test API"
        assert len(builder.config.endpoints) == 2

    def test_builder_creates_app(self, api_builder):
        """Test builder creates FastAPI app."""
        app = api_builder.build()
        assert app is not None
        assert hasattr(app, 'routes')

    def test_builder_generates_endpoints(self, api_builder):
        """Test builder generates endpoints."""
        app = api_builder.build()
        # Should have routes for both endpoints
        assert len(app.routes) > 0


# ===== ENDPOINT TESTS =====

class TestEndpoints:
    """Test generated endpoints."""

    def test_post_endpoint_creates_resource(self, test_client):
        """Test POST endpoint creates resource."""
        response = test_client.post(
            "/api/v1/users",
            json={"name": "John", "email": "john@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"]
        assert data["data"]["name"] == "John"

    def test_post_endpoint_validation_fails(self, test_client):
        """Test POST endpoint with invalid data."""
        response = test_client.post(
            "/api/v1/users",
            json={"name": "John"}  # missing email
        )
        # FastAPI returns 422 for validation failures (missing required field)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data  # FastAPI validation error format

    def test_get_endpoint_retrieves_resource(self, test_client):
        """Test GET endpoint retrieves resource."""
        response = test_client.get("/api/v1/users/123")
        assert response.status_code == 200
        data = response.json()
        assert data["success"]

    def test_response_format(self, test_client):
        """Test response format."""
        response = test_client.post(
            "/api/v1/users",
            json={"name": "Jane", "email": "jane@example.com"}
        )
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert "error" in data
        assert "timestamp" in data


# ===== PERFORMANCE TESTS =====

class TestPerformance:
    """Test performance requirements."""

    def test_request_performance(self, test_client):
        """Test request completes in <100ms."""
        start = time.time()
        response = test_client.post(
            "/api/v1/users",
            json={"name": "Perf Test", "email": "perf@test.com"}
        )
        elapsed_ms = (time.time() - start) * 1000

        assert response.status_code == 200
        assert elapsed_ms < 100, f"Request took {elapsed_ms}ms, expected <100ms"

    def test_multiple_requests_performance(self, test_client):
        """Test multiple requests performance."""
        times = []
        for i in range(10):
            start = time.time()
            test_client.post(
                "/api/v1/users",
                json={"name": f"User{i}", "email": f"user{i}@test.com"}
            )
            elapsed_ms = (time.time() - start) * 1000
            times.append(elapsed_ms)

        avg_time = sum(times) / len(times)
        assert avg_time < 100, f"Average request time {avg_time}ms, expected <100ms"


# ===== INTEGRATION TESTS =====

class TestIntegration:
    """Test full integration scenarios."""

    def test_full_crud_workflow(self, test_client):
        """Test complete CRUD workflow."""
        # Create
        create_response = test_client.post(
            "/api/v1/users",
            json={"name": "Alice", "email": "alice@example.com"}
        )
        assert create_response.json()["success"]

        # Read
        read_response = test_client.get("/api/v1/users/123")
        assert read_response.json()["success"]

    def test_schema_with_multiple_validations(self):
        """Test endpoint with multiple validation rules."""
        endpoint = EndpointConfig(
            path="/register",
            method=HTTPMethod.POST,
            name="register",
            request_fields=[
                FieldSchema(
                    name="email",
                    type="string",
                    required=True,
                    validations=[
                        ValidationRule(type="email")
                    ]
                ),
                FieldSchema(
                    name="password",
                    type="string",
                    required=True,
                    validations=[
                        ValidationRule(type="min_length", value=8)
                    ]
                )
            ]
        )

        schema = APISchema(
            name="Auth API",
            version="1.0.0",
            endpoints=[endpoint]
        )

        builder = RESTAPIBuilder(schema)
        app = builder.build()
        client = TestClient(app)

        # Valid request
        response = client.post(
            "/api/v1/register",
            json={"email": "user@example.com", "password": "securepass123"}
        )
        assert response.json()["success"]

        # Invalid email
        response = client.post(
            "/api/v1/register",
            json={"email": "invalid", "password": "securepass123"}
        )
        assert not response.json()["success"]

    def test_api_from_config_dict(self):
        """Test creating API from configuration dictionary."""
        config_dict = {
            "name": "Test API",
            "version": "1.0.0",
            "base_url": "/api",
            "endpoints": [
                {
                    "path": "/test",
                    "method": "GET",
                    "name": "test_endpoint",
                    "response_fields": []
                }
            ]
        }

        schema = APISchema(**config_dict)
        builder = RESTAPIBuilder(schema)
        app = builder.build()

        assert app is not None
        assert builder.config.name == "Test API"
