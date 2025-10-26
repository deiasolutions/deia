#!/usr/bin/env python3
"""Tests for Service Mesh."""

import pytest
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.service_mesh import (
    ServiceStatus, Service, RoutingRule, NetworkPolicy,
    ServiceRegistry, TrafficManager, NetworkPolicyEngine,
    ServiceMesh, ServiceMeshService
)


class TestServiceRegistry:
    """Test service registry."""

    @pytest.fixture
    def registry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = ServiceRegistry(Path(tmpdir))
            yield registry

    def test_register_service(self, registry):
        """Test registering service."""
        service = registry.register("api", "1.0.0", "localhost", 8080)
        assert service.name == "api"
        assert service.port == 8080

    def test_get_service(self, registry):
        """Test getting service."""
        registry.register("api", "1.0.0", "localhost", 8080)
        service = registry.get_service("api", "1.0.0")
        assert service is not None

    def test_deregister_service(self, registry):
        """Test deregistering service."""
        registry.register("api", "1.0.0", "localhost", 8080)
        success = registry.deregister("api", "1.0.0")
        assert success is True

    def test_list_services(self, registry):
        """Test listing services."""
        registry.register("api", "1.0.0", "localhost", 8080)
        registry.register("db", "2.0.0", "localhost", 5432)
        services = registry.list_services()
        assert len(services) == 2


class TestTrafficManager:
    """Test traffic management."""

    def test_add_routing_rule(self):
        """Test adding routing rule."""
        mgr = TrafficManager()
        rule = RoutingRule(
            name="api-db",
            source_service="api",
            target_service="db"
        )
        mgr.add_routing_rule(rule)
        assert mgr.get_route("api", "db") is not None

    def test_circuit_breaker(self):
        """Test circuit breaker."""
        mgr = TrafficManager()

        # Record failures
        for _ in range(5):
            mgr.record_failure("service")

        # Should open circuit
        allowed = mgr.record_failure("service")
        assert allowed is False

    def test_reset_circuit(self):
        """Test resetting circuit."""
        mgr = TrafficManager()
        mgr.record_failure("service")
        mgr.reset_circuit("service")

        # Should allow again
        allowed = mgr.record_failure("service")
        assert allowed is True


class TestNetworkPolicyEngine:
    """Test network policies."""

    def test_allow_policy(self):
        """Test allow policy."""
        engine = NetworkPolicyEngine()
        policy = NetworkPolicy(
            name="allow-api-db",
            action="allow",
            from_service="api",
            to_service="db"
        )
        engine.add_policy(policy)
        assert engine.is_allowed("api", "db", 5432) is True

    def test_deny_policy(self):
        """Test deny policy."""
        engine = NetworkPolicyEngine()
        policy = NetworkPolicy(
            name="deny-api-cache",
            action="deny",
            from_service="api",
            to_service="cache"
        )
        engine.add_policy(policy)
        assert engine.is_allowed("api", "cache", 6379) is False

    def test_default_allow(self):
        """Test default allow (no policy)."""
        engine = NetworkPolicyEngine()
        # No policy defined
        assert engine.is_allowed("api", "unknown", 80) is True


class TestServiceMesh:
    """Test service mesh."""

    @pytest.fixture
    def mesh(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mesh = ServiceMesh(Path(tmpdir))
            yield mesh

    def test_register_and_get(self, mesh):
        """Test registering and getting service."""
        mesh.register_service("api", "1.0.0", "localhost", 8080)
        service = mesh.get_service("api")
        assert service is not None
        assert service.port == 8080

    def test_routing(self, mesh):
        """Test routing configuration."""
        rule = mesh.add_routing("api", "db", weight=1.0)
        assert rule.source_service == "api"
        assert rule.target_service == "db"

    def test_policies(self, mesh):
        """Test policy configuration."""
        mesh.add_policy("allow", "api", "db")
        assert mesh.can_communicate("api", "db", 5432) is True

    def test_service_graph(self, mesh):
        """Test service graph generation."""
        mesh.register_service("api", "1.0.0", "localhost", 8080)
        mesh.register_service("db", "1.0.0", "localhost", 5432)
        graph = mesh.get_service_graph()
        assert len(graph["nodes"]) == 2


class TestServiceMeshService:
    """Test high-level service mesh API."""

    @pytest.fixture
    def service(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            service = ServiceMeshService(Path(tmpdir))
            yield service

    def test_register(self, service):
        """Test registering via service."""
        svc = service.register("api", "1.0.0", "localhost", 8080)
        assert svc.name == "api"

    def test_communication(self, service):
        """Test checking communication."""
        service.allow("api", "db")
        assert service.can_talk("api", "db", 5432) is True

    def test_graph(self, service):
        """Test getting service graph."""
        service.register("api", "1.0.0", "localhost", 8080)
        graph = service.graph()
        assert "nodes" in graph


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
