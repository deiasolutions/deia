#!/usr/bin/env python3
"""Service Mesh Infrastructure: Service discovery, routing, policies, security."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SERVICE-MESH - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class Service:
    """Registered service."""
    name: str
    version: str
    host: str
    port: int
    status: ServiceStatus = ServiceStatus.HEALTHY
    metadata: Dict = field(default_factory=dict)
    registered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


@dataclass
class RoutingRule:
    """Traffic routing rule."""
    name: str
    source_service: str
    target_service: str
    weight: float = 1.0  # 0-1 for canary
    timeout_ms: int = 5000
    retries: int = 3
    circuit_breaker_threshold: int = 5


@dataclass
class NetworkPolicy:
    """Network access policy."""
    name: str
    action: str  # "allow" or "deny"
    from_service: str
    to_service: str
    ports: List[int] = field(default_factory=list)


@dataclass
class TLSConfig:
    """TLS/mTLS configuration."""
    enabled: bool = True
    mode: str = "STRICT"  # STRICT, PERMISSIVE, DISABLE
    cert_path: Optional[str] = None
    key_path: Optional[str] = None


class ServiceRegistry:
    """Service discovery and registration."""

    def __init__(self, project_root: Path = None):
        """Initialize service registry."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.mesh_dir = project_root / ".deia" / "service-mesh"
        self.mesh_dir.mkdir(parents=True, exist_ok=True)

        self.registry_log = self.mesh_dir / "registry.jsonl"
        self.services: Dict[str, Service] = {}
        self.lock = threading.RLock()

    def register(self, name: str, version: str, host: str, port: int) -> Service:
        """Register a service."""
        with self.lock:
            service = Service(name=name, version=version, host=host, port=port)
            key = f"{name}:{version}"
            self.services[key] = service
            self._persist(service)
            logger.info(f"Service {name}:{version} registered at {host}:{port}")
            return service

    def deregister(self, name: str, version: str) -> bool:
        """Deregister a service."""
        with self.lock:
            key = f"{name}:{version}"
            if key in self.services:
                del self.services[key]
                logger.info(f"Service {name}:{version} deregistered")
                return True
            return False

    def get_service(self, name: str, version: Optional[str] = None) -> Optional[Service]:
        """Get service by name."""
        with self.lock:
            if version:
                key = f"{name}:{version}"
                return self.services.get(key)
            # Get latest version
            matches = [s for k, s in self.services.items() if k.startswith(f"{name}:")]
            return matches[-1] if matches else None

    def get_healthy_services(self, name: str) -> List[Service]:
        """Get healthy services."""
        with self.lock:
            return [s for k, s in self.services.items()
                   if k.startswith(f"{name}:") and s.status == ServiceStatus.HEALTHY]

    def update_status(self, name: str, version: str, status: ServiceStatus):
        """Update service status."""
        with self.lock:
            key = f"{name}:{version}"
            if key in self.services:
                self.services[key].status = status

    def list_services(self) -> List[Service]:
        """List all services."""
        with self.lock:
            return list(self.services.values())

    def _persist(self, service: Service):
        """Persist service registration."""
        try:
            with open(self.registry_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(service)) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist service: {e}")


class TrafficManager:
    """Manages traffic routing and load balancing."""

    def __init__(self):
        """Initialize traffic manager."""
        self.routing_rules: Dict[str, RoutingRule] = {}
        self.circuit_breakers: Dict[str, int] = {}
        self.lock = threading.RLock()

    def add_routing_rule(self, rule: RoutingRule) -> None:
        """Add routing rule."""
        with self.lock:
            self.routing_rules[rule.name] = rule
            logger.info(f"Routing rule '{rule.name}' added")

    def get_route(self, source: str, target: str) -> Optional[RoutingRule]:
        """Get routing rule for source→target."""
        with self.lock:
            for rule in self.routing_rules.values():
                if rule.source_service == source and rule.target_service == target:
                    return rule
            return None

    def record_failure(self, service: str) -> bool:
        """Record service failure for circuit breaker."""
        with self.lock:
            count = self.circuit_breakers.get(service, 0) + 1
            self.circuit_breakers[service] = count
            if count >= 5:
                logger.warning(f"Circuit breaker open for {service}")
                return False
            return True

    def reset_circuit(self, service: str):
        """Reset circuit breaker."""
        with self.lock:
            self.circuit_breakers[service] = 0


class NetworkPolicyEngine:
    """Enforces network policies."""

    def __init__(self):
        """Initialize policy engine."""
        self.policies: Dict[str, NetworkPolicy] = {}
        self.lock = threading.RLock()

    def add_policy(self, policy: NetworkPolicy) -> None:
        """Add network policy."""
        with self.lock:
            self.policies[policy.name] = policy
            logger.info(f"Policy '{policy.name}' added")

    def is_allowed(self, from_service: str, to_service: str, port: int) -> bool:
        """Check if traffic is allowed."""
        with self.lock:
            applicable = [p for p in self.policies.values()
                         if p.from_service == from_service and p.to_service == to_service]

            if not applicable:
                return True  # Default allow if no policy

            for policy in applicable:
                if policy.action == "allow":
                    if not policy.ports or port in policy.ports:
                        return True
                elif policy.action == "deny":
                    if not policy.ports or port in policy.ports:
                        return False

            return False


class ServiceMesh:
    """Main service mesh controller."""

    def __init__(self, project_root: Path = None):
        """Initialize service mesh."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.registry = ServiceRegistry(project_root)
        self.traffic = TrafficManager()
        self.policies = NetworkPolicyEngine()
        self.tls_config = TLSConfig()

    def register_service(self, name: str, version: str, host: str, port: int) -> Service:
        """Register service."""
        return self.registry.register(name, version, host, port)

    def get_service(self, name: str) -> Optional[Service]:
        """Get service."""
        return self.registry.get_service(name)

    def add_routing(self, source: str, target: str, weight: float = 1.0) -> RoutingRule:
        """Add routing rule."""
        rule = RoutingRule(
            name=f"{source}->{target}",
            source_service=source,
            target_service=target,
            weight=weight
        )
        self.traffic.add_routing_rule(rule)
        return rule

    def add_policy(self, action: str, from_service: str, to_service: str) -> NetworkPolicy:
        """Add network policy."""
        policy = NetworkPolicy(
            name=f"{action}-{from_service}-{to_service}",
            action=action,
            from_service=from_service,
            to_service=to_service
        )
        self.policies.add_policy(policy)
        return policy

    def can_communicate(self, from_service: str, to_service: str, port: int) -> bool:
        """Check if services can communicate."""
        return self.policies.is_allowed(from_service, to_service, port)

    def get_service_graph(self) -> Dict:
        """Get service dependency graph."""
        services = self.registry.list_services()
        nodes = [{"id": s.name, "version": s.version, "status": s.status.value} for s in services]
        edges = [{"source": r.source_service, "target": r.target_service}
                for r in self.traffic.routing_rules.values()]
        return {"nodes": nodes, "edges": edges}


class ServiceMeshService:
    """High-level service mesh API."""

    def __init__(self, project_root: Path = None):
        """Initialize service mesh service."""
        self.mesh = ServiceMesh(project_root)

    def register(self, name: str, version: str, host: str, port: int) -> Service:
        """Register service."""
        return self.mesh.register_service(name, version, host, port)

    def get(self, name: str) -> Optional[Service]:
        """Get service."""
        return self.mesh.get_service(name)

    def route(self, source: str, target: str, weight: float = 1.0) -> RoutingRule:
        """Add routing rule."""
        return self.mesh.add_routing(source, target, weight)

    def allow(self, from_service: str, to_service: str) -> NetworkPolicy:
        """Allow traffic."""
        return self.mesh.add_policy("allow", from_service, to_service)

    def deny(self, from_service: str, to_service: str) -> NetworkPolicy:
        """Deny traffic."""
        return self.mesh.add_policy("deny", from_service, to_service)

    def can_talk(self, from_service: str, to_service: str, port: int = 80) -> bool:
        """Check if services can communicate."""
        return self.mesh.can_communicate(from_service, to_service, port)

    def graph(self) -> Dict:
        """Get service graph."""
        return self.mesh.get_service_graph()
