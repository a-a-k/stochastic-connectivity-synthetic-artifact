from __future__ import annotations

import math

from .estimators import fanout_closed_form, path_closed_form, replicated_edge_bottleneck_availability, service_live_probability
from .families import chain_graph, fanout_graph


def failure_domain_gap(entry_theta: float, replica_theta: float, replica_count: int, rho: float) -> dict[str, float]:
    independent = replicated_edge_bottleneck_availability(entry_theta, replica_theta, replica_count, rho)
    correlated = entry_theta * replica_theta * rho
    return {
        "product_baseline": independent,
        "correlated_reference": correlated,
        "gap": independent - correlated,
    }


def timeout_reference(
    theta: float,
    rho: float,
    path_edges: int,
    on_time_probability: float,
    retry_count: int,
) -> dict[str, float]:
    graph, _endpoint, path = chain_graph(path_edges, theta, rho)
    connectivity = path_closed_form(graph, path)
    temporal_factor = 1.0 - (1.0 - on_time_probability) ** (retry_count + 1)
    timed = connectivity * temporal_factor
    return {
        "connectivity_availability": connectivity,
        "timed_reference": timed,
        "false_positive_gap": connectivity - timed,
        "temporal_factor": temporal_factor,
    }


def trace_incompleteness_reference(
    degree: int,
    theta: float,
    rho: float,
    replica_count: int,
    omission_rate: float,
) -> dict[str, float]:
    graph, _endpoint, targets = fanout_graph(degree, theta, rho)
    true_availability = fanout_closed_form(graph, "entry", targets)
    retained = 1.0 - omission_rate

    hidden_dependency_estimate = 0.0
    edge_only_estimate = true_availability * (retained ** degree)
    for retained_count in range(degree + 1):
        probability = math.comb(degree, retained_count) * (retained ** retained_count) * (omission_rate ** (degree - retained_count))
        hidden_dependency_estimate += probability * (theta * ((theta * rho) ** retained_count))

    true_replica_live = service_live_probability(theta, replica_count)
    observed_replica_live = 0.0
    for retained_count in range(replica_count + 1):
        probability = (
            math.comb(replica_count, retained_count)
            * (retained ** retained_count)
            * (omission_rate ** (replica_count - retained_count))
        )
        observed_replica_live += probability * service_live_probability(theta, retained_count)
    true_replica_availability = rho * true_replica_live
    observed_replica_availability = rho * observed_replica_live

    return {
        "true_availability": true_availability,
        "hidden_dependency_estimate": hidden_dependency_estimate,
        "hidden_dependency_bias": hidden_dependency_estimate - true_availability,
        "edge_only_estimate": edge_only_estimate,
        "edge_only_bias": edge_only_estimate - true_availability,
        "true_replica_availability": true_replica_availability,
        "observed_replica_availability": observed_replica_availability,
        "replica_omission_bias": observed_replica_availability - true_replica_availability,
    }
