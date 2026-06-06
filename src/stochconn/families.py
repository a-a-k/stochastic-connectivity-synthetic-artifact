from __future__ import annotations

from .model import ASYNC, SYNC, Edge, EndpointPredicate, ServiceGraph, rho_map, theta_map


def chain_graph(k_edges: int, theta: float, rho: float) -> tuple[ServiceGraph, EndpointPredicate, list[str]]:
    if k_edges < 1:
        raise ValueError("k_edges must be positive")
    services = tuple(f"v{index}" for index in range(k_edges + 1))
    edges = tuple(Edge(services[index], services[index + 1], SYNC) for index in range(k_edges))
    replicas = {service: 1 for service in services}
    graph = ServiceGraph(services, edges, replicas, theta_map(services, replicas, theta), rho_map(edges, rho))
    endpoint = EndpointPredicate("chain_last_required", services[0], (services[-1],), "all_of")
    return graph, endpoint, list(services)


def fanout_graph(degree: int, theta: float, rho: float) -> tuple[ServiceGraph, EndpointPredicate, list[str]]:
    if degree < 1:
        raise ValueError("degree must be positive")
    services = ("entry",) + tuple(f"target_{index}" for index in range(degree))
    targets = list(services[1:])
    edges = tuple(Edge("entry", target, SYNC) for target in targets)
    replicas = {service: 1 for service in services}
    graph = ServiceGraph(services, edges, replicas, theta_map(services, replicas, theta), rho_map(edges, rho))
    endpoint = EndpointPredicate("fanout_all_targets", "entry", tuple(targets), "all_of")
    return graph, endpoint, targets


def bottleneck_graph(entry_theta: float, target_theta: float, target_replicas: int, rho: float) -> tuple[ServiceGraph, EndpointPredicate]:
    services = ("entry", "target")
    edges = (Edge("entry", "target", SYNC),)
    replicas = {"entry": 1, "target": target_replicas}
    theta = {"entry": (entry_theta,), "target": tuple(target_theta for _ in range(target_replicas))}
    graph = ServiceGraph(services, edges, replicas, theta, rho_map(edges, rho))
    endpoint = EndpointPredicate("target_required", "entry", ("target",), "all_of")
    return graph, endpoint


def async_side_effect_graph(theta: float, rho_sync: float, rho_async: float) -> tuple[
    ServiceGraph,
    EndpointPredicate,
    EndpointPredicate,
    ServiceGraph,
]:
    services = ("entry", "core", "event_bus", "worker")
    edges = (
        Edge("entry", "core", SYNC),
        Edge("entry", "event_bus", ASYNC),
        Edge("event_bus", "worker", ASYNC),
    )
    replicas = {service: 1 for service in services}
    edge_rho = {
        edges[0].key: rho_sync,
        edges[1].key: rho_async,
        edges[2].key: rho_async,
    }
    graph = ServiceGraph(services, edges, replicas, theta_map(services, replicas, theta), edge_rho)
    immediate = EndpointPredicate("immediate_http", "entry", ("core",), "all_of", success_semantics="immediate_sync")
    eventual = EndpointPredicate(
        "eventual_workflow",
        "entry",
        ("core", "worker"),
        "all_of",
        success_semantics="eventual_async_explicit",
    )
    sync_edges = (edges[0],)
    sync_graph = ServiceGraph(services, sync_edges, replicas, theta_map(services, replicas, theta), {edges[0].key: rho_sync})
    return graph, immediate, eventual, sync_graph
