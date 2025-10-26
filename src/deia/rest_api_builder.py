"""
REST API Builder - Auto-generate REST APIs from configuration.

Dynamically generates FastAPI endpoints from configuration schema,
with validation, error handling, rate limiting, and authentication hooks.
"""

from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
from functools import wraps
from pathlib import Path
import logging

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from pydantic import BaseModel, Field, validator
import uvicorn


logger = logging.getLogger(__name__)


# ===== DATA MODELS =====

class HTTPMethod(str, Enum):
    """Supported HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ValidationRule(BaseModel):
    """Validation rule for a field."""
    type: str  # email, number, string, min_length, max_length, pattern, custom
    value: Optional[Any] = None  # validation value
    message: Optional[str] = None  # error message


class FieldSchema(BaseModel):
    """Schema for a request/response field."""
    name: str
    type: str  # string, number, boolean, object, array
    required: bool = True
    default: Optional[Any] = None
    description: Optional[str] = None
    validations: List[ValidationRule] = Field(default_factory=list)
    example: Optional[Any] = None


class EndpointConfig(BaseModel):
    """Configuration for a single endpoint."""
    path: str
    method: HTTPMethod
    name: str
    description: Optional[str] = None
    request_fields: List[FieldSchema] = Field(default_factory=list)
    response_fields: List[FieldSchema] = Field(default_factory=list)
    auth_required: bool = False
    rate_limit: Optional[int] = None  # requests per minute
    tags: List[str] = Field(default_factory=list)
    handler: Optional[Callable] = None  # custom handler function


class APISchema(BaseModel):
    """Complete API schema configuration."""
    name: str
    version: str
    description: Optional[str] = None
    base_url: str = "/api/v1"
    endpoints: List[EndpointConfig]
    global_auth: Optional[str] = None  # authentication type: bearer, api_key, oauth2
    global_rate_limit: Optional[int] = None  # default requests per minute
    cors_enabled: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ===== REQUEST/RESPONSE MODELS =====

class APIRequest(BaseModel):
    """Standard API request model."""
    data: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    request_id: Optional[str] = None


# ===== VALIDATION & TRANSFORMATION =====

class FieldValidator:
    """Validate fields against rules."""

    @staticmethod
    def validate_field(value: Any, field_schema: FieldSchema) -> tuple[bool, Optional[str]]:
        """Validate a field value against schema."""
        # Check required
        if field_schema.required and value is None:
            return False, f"{field_schema.name} is required"

        if value is None:
            return True, None

        # Check type
        if not FieldValidator._check_type(value, field_schema.type):
            return False, f"{field_schema.name} must be of type {field_schema.type}"

        # Check validations
        for validation in field_schema.validations:
            is_valid, message = FieldValidator._apply_validation(value, validation, field_schema)
            if not is_valid:
                return False, message or validation.message or f"Validation failed for {field_schema.name}"

        return True, None

    @staticmethod
    def _check_type(value: Any, expected_type: str) -> bool:
        """Check if value matches expected type."""
        type_map = {
            "string": str,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list
        }

        expected = type_map.get(expected_type)
        if expected is None:
            return True

        return isinstance(value, expected)

    @staticmethod
    def _apply_validation(value: Any, rule: ValidationRule, field_schema: FieldSchema) -> tuple[bool, Optional[str]]:
        """Apply a specific validation rule."""
        try:
            if rule.type == "email":
                import re
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(pattern, str(value)):
                    return False, f"{field_schema.name} must be a valid email"
                return True, None

            elif rule.type == "number":
                try:
                    float(value)
                    return True, None
                except (ValueError, TypeError):
                    return False, f"{field_schema.name} must be a number"

            elif rule.type == "min_length":
                if len(str(value)) < rule.value:
                    return False, f"{field_schema.name} must have minimum length {rule.value}"
                return True, None

            elif rule.type == "max_length":
                if len(str(value)) > rule.value:
                    return False, f"{field_schema.name} must have maximum length {rule.value}"
                return True, None

            elif rule.type == "pattern":
                import re
                if not re.match(rule.value, str(value)):
                    return False, f"{field_schema.name} does not match required pattern"
                return True, None

            else:
                return True, None

        except Exception as e:
            return False, str(e)


class RequestTransformer:
    """Transform request data."""

    @staticmethod
    def transform_request(data: Dict[str, Any], schema: List[FieldSchema]) -> tuple[Dict[str, Any], Optional[str]]:
        """Transform and validate request data against schema."""
        transformed = {}

        for field_schema in schema:
            value = data.get(field_schema.name, field_schema.default)

            # Validate
            is_valid, error_msg = FieldValidator.validate_field(value, field_schema)
            if not is_valid:
                return None, error_msg

            transformed[field_schema.name] = value

        return transformed, None

    @staticmethod
    def transform_response(data: Dict[str, Any], schema: List[FieldSchema]) -> Dict[str, Any]:
        """Transform response data according to schema."""
        response = {}

        for field_schema in schema:
            if field_schema.name in data:
                response[field_schema.name] = data[field_schema.name]
            elif field_schema.default is not None:
                response[field_schema.name] = field_schema.default

        return response


# ===== RATE LIMITING =====

class RateLimiter:
    """Rate limiting for endpoints."""

    def __init__(self, requests_per_minute: int = 60):
        """Initialize rate limiter."""
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed."""
        import time

        current_time = time.time()

        if client_id not in self.requests:
            self.requests[client_id] = []

        # Remove old requests (older than 1 minute)
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 60
        ]

        # Check limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False

        self.requests[client_id].append(current_time)
        return True


# ===== REST API BUILDER =====

class RESTAPIBuilder:
    """Build and serve REST API from configuration."""

    def __init__(self, config: APISchema):
        """Initialize builder with API schema."""
        self.config = config
        self.app = FastAPI(
            title=config.name,
            version=config.version,
            description=config.description
        )
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.request_handlers: Dict[str, Callable] = {}
        self.auth_hooks: Dict[str, Callable] = {}
        self.error_handlers: Dict[int, Callable] = {}
        self.middlewares: List[Callable] = []

    def build(self) -> FastAPI:
        """Build the FastAPI app from config."""
        # Generate endpoints
        for endpoint_config in self.config.endpoints:
            self._generate_endpoint(endpoint_config)

        # Add default error handlers
        self._add_error_handlers()

        logger.info(f"Built API '{self.config.name}' with {len(self.config.endpoints)} endpoints")
        return self.app

    def _generate_endpoint(self, endpoint_config: EndpointConfig) -> None:
        """Generate a single endpoint from config."""
        path = f"{self.config.base_url}{endpoint_config.path}"
        method = endpoint_config.method.value.lower()

        # Create request/response models dynamically
        request_model = self._create_request_model(endpoint_config)
        response_model = APIResponse

        # Create handler function
        async def handler(request_data: request_model):
            return await self._handle_request(endpoint_config, request_data)

        handler.__name__ = endpoint_config.name
        handler.__doc__ = endpoint_config.description or f"{method.upper()} {path}"

        # Add route
        self.app.add_api_route(
            path=path,
            endpoint=handler,
            methods=[endpoint_config.method.value],
            tags=endpoint_config.tags,
            response_model=response_model
        )

        logger.info(f"Generated {endpoint_config.method.value} {path}")

    def _create_request_model(self, endpoint_config: EndpointConfig) -> type:
        """Dynamically create request model from endpoint config."""
        fields = {}

        for field_schema in endpoint_config.request_fields:
            # Determine field type
            python_type = self._get_python_type(field_schema.type)

            # Create field with constraints
            if field_schema.required:
                fields[field_schema.name] = (python_type, ...)
            else:
                fields[field_schema.name] = (python_type, field_schema.default)

        # Create model
        from pydantic import create_model
        model = create_model(
            f"{endpoint_config.name}_Request",
            **fields
        )

        return model

    @staticmethod
    def _get_python_type(field_type: str) -> type:
        """Get Python type from field type string."""
        type_map = {
            "string": str,
            "number": float,
            "boolean": bool,
            "object": dict,
            "array": list
        }
        return type_map.get(field_type, str)

    async def _handle_request(self, endpoint_config: EndpointConfig, request_data: Any) -> APIResponse:
        """Handle a request to an endpoint."""
        try:
            # Extract data
            if hasattr(request_data, 'dict'):
                data = request_data.dict()
            else:
                data = request_data

            # Validate and transform request
            transformed, error = RequestTransformer.transform_request(
                data,
                endpoint_config.request_fields
            )

            if error:
                return APIResponse(
                    success=False,
                    error=error,
                    data=None
                )

            # Check rate limiting
            if endpoint_config.rate_limit:
                if endpoint_config.path not in self.rate_limiters:
                    self.rate_limiters[endpoint_config.path] = RateLimiter(
                        endpoint_config.rate_limit
                    )

                if not self.rate_limiters[endpoint_config.path].is_allowed("global"):
                    return APIResponse(
                        success=False,
                        error="Rate limit exceeded",
                        data=None
                    )

            # Call custom handler if available
            if endpoint_config.handler:
                result = endpoint_config.handler(transformed)
            else:
                # Default handler - echo transformed data
                result = transformed

            # Transform response
            response_data = RequestTransformer.transform_response(
                result if isinstance(result, dict) else {"result": result},
                endpoint_config.response_fields
            )

            return APIResponse(
                success=True,
                data=response_data,
                error=None
            )

        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return APIResponse(
                success=False,
                error=str(e),
                data=None
            )

    def _add_error_handlers(self) -> None:
        """Add default error handlers."""
        @self.app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            return APIResponse(
                success=False,
                error=exc.detail,
                data=None
            )

    def register_handler(self, endpoint_path: str, handler: Callable) -> None:
        """Register a custom handler for an endpoint."""
        self.request_handlers[endpoint_path] = handler

    def register_auth(self, auth_type: str, handler: Callable) -> None:
        """Register an authentication handler."""
        self.auth_hooks[auth_type] = handler

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Run the API server."""
        uvicorn.run(self.app, host=host, port=port)


# ===== FACTORY FUNCTIONS =====

def load_api_config(config_path: Path) -> APISchema:
    """Load API schema from JSON file."""
    with open(config_path, 'r') as f:
        config_dict = json.load(f)

    return APISchema(**config_dict)


def create_api_builder(config: Union[APISchema, Path]) -> RESTAPIBuilder:
    """Create API builder from config."""
    if isinstance(config, Path):
        config = load_api_config(config)

    return RESTAPIBuilder(config)


def build_api(config: Union[APISchema, Path]) -> FastAPI:
    """Build and return FastAPI app from config."""
    builder = create_api_builder(config)
    return builder.build()
