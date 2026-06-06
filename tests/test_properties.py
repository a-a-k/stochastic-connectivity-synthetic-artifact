from __future__ import annotations

import shutil
import sys
import unittest
from pathlib import Path

import yaml

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from stochconn.boundary import failure_domain_gap, timeout_reference, trace_incompleteness_reference
from stochconn.cli import main
from stochconn.estimators import exact_enumeration, path_closed_form, replicated_edge_bottleneck_availability
from stochconn.experiments import ExperimentRunner
from stochconn.families import async_side_effect_graph, bottleneck_graph, chain_graph


class StochasticConnectivityProperties(unittest.TestCase):
    def test_path_closed_form_includes_edge_rho(self) -> None:
        graph, endpoint, path = chain_graph(1, theta=0.9, rho=0.8)
        self.assertAlmostEqual(path_closed_form(graph, path), 0.9 * 0.9 * 0.8, places=12)
        self.assertAlmostEqual(exact_enumeration(graph, endpoint), path_closed_form(graph, path), places=12)

    def test_monotonicity_in_theta_and_rho(self) -> None:
        low_graph, low_endpoint, _ = chain_graph(2, theta=0.8, rho=0.7)
        high_theta_graph, high_theta_endpoint, _ = chain_graph(2, theta=0.9, rho=0.7)
        high_rho_graph, high_rho_endpoint, _ = chain_graph(2, theta=0.8, rho=0.9)
        low = exact_enumeration(low_graph, low_endpoint)
        self.assertGreaterEqual(exact_enumeration(high_theta_graph, high_theta_endpoint), low)
        self.assertGreaterEqual(exact_enumeration(high_rho_graph, high_rho_endpoint), low)

    def test_replicated_bottleneck_bound(self) -> None:
        rho = 0.82
        for replicas in [1, 2, 5, 12]:
            availability = replicated_edge_bottleneck_availability(1.0, 0.9, replicas, rho)
            self.assertLessEqual(availability, rho)
        graph, endpoint = bottleneck_graph(1.0, 0.9, 3, rho)
        self.assertAlmostEqual(exact_enumeration(graph, endpoint), replicated_edge_bottleneck_availability(1.0, 0.9, 3, rho))

    def test_async_immediate_invariance_and_eventual_contrast(self) -> None:
        graph, immediate, eventual, sync_graph = async_side_effect_graph(theta=0.97, rho_sync=0.96, rho_async=0.85)
        immediate_full = exact_enumeration(graph, immediate)
        immediate_sync_only = exact_enumeration(sync_graph, immediate)
        eventual_value = exact_enumeration(graph, eventual)
        self.assertAlmostEqual(immediate_full, immediate_sync_only, places=12)
        self.assertLess(eventual_value, immediate_full)

    def test_failure_domain_gap_is_positive(self) -> None:
        stats = failure_domain_gap(entry_theta=1.0, replica_theta=0.9, replica_count=3, rho=0.95)
        self.assertGreater(stats["product_baseline"], stats["correlated_reference"])
        self.assertGreater(stats["gap"], 0.0)

    def test_timeout_false_positive_gap(self) -> None:
        no_retry = timeout_reference(theta=0.98, rho=0.97, path_edges=2, on_time_probability=0.55, retry_count=0)
        retry = timeout_reference(theta=0.98, rho=0.97, path_edges=2, on_time_probability=0.55, retry_count=2)
        self.assertGreater(no_retry["false_positive_gap"], 0.0)
        self.assertLess(retry["false_positive_gap"], no_retry["false_positive_gap"])

    def test_trace_incompleteness_biases_both_directions(self) -> None:
        stats = trace_incompleteness_reference(degree=5, theta=0.97, rho=0.95, replica_count=3, omission_rate=0.2)
        self.assertGreater(stats["hidden_dependency_bias"], 0.0)
        self.assertLess(stats["edge_only_bias"], 0.0)
        self.assertLess(stats["replica_omission_bias"], 0.0)

    def test_scale_sanity_layer_has_large_closed_form_and_sentinel_mc(self) -> None:
        config = _smoke_config()
        config["scale_sanity"] = {
            "enabled": True,
            "mc_samples": 200,
            "q_values": [0.995],
            "chain_lengths": [128],
            "fanout_degrees": [64],
            "bottleneck_replicas": [64],
            "bottleneck_entry_theta": 1.0,
            "bottleneck_target_theta": 0.90,
            "bottleneck_rho": 0.95,
            "sentinel_mc": [{"graph_family": "chain", "k_edges": 16, "q": 0.995}],
        }
        bundle = ExperimentRunner(config).run()
        self.assertEqual(len(bundle.summary_rows), 8)
        self.assertEqual(len(bundle.scale_rows), 4)
        self.assertIn("up to 129 services", bundle.context["scale_sanity_paragraph"])
        sentinel_rows = [row for row in bundle.scale_rows if row["metric_kind"] == "scale_sentinel_mc"]
        self.assertEqual(len(sentinel_rows), 1)
        self.assertEqual(sentinel_rows[0]["n_services"], 17)

    def test_cli_smoke_outputs_all_files_without_markers(self) -> None:
        root = Path(__file__).resolve().parents[1]
        tmp = root / ".test-output"
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir()
        config = _smoke_config()
        config_path = tmp / "smoke.yaml"
        config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
        out = tmp / "outputs"
        main(["run", "--config", str(config_path), "--out", str(out)])
        for name in [
            "raw_results.csv",
            "table2_summary.csv",
            "scale_sanity.csv",
            "table2_snippets.md",
            "report.md",
            "fig_synthetic_boundaries.png",
            "fig_synthetic_boundaries_acm.png",
            "manifest.yaml",
        ]:
            self.assertTrue((out / name).exists(), name)
        text = (out / "report.md").read_text(encoding="utf-8") + (out / "table2_snippets.md").read_text(encoding="utf-8")
        self.assertNotIn("TO" + "DO", text)
        self.assertNotIn("PLACE" + "HOLDER", text)
        shutil.rmtree(tmp)


def _smoke_config() -> dict[str, object]:
    return {
        "suite_id": "smoke",
        "seed": 7,
        "mc_samples": 1000,
        "chain": {"lengths": [1], "theta_values": [0.9], "rho_values": [0.8]},
        "fanout": {"degrees": [1, 2], "theta": 0.9, "rho": 0.8},
        "replicated_bottleneck": {"replica_counts": [1, 2], "entry_theta": 1.0, "target_theta": 0.9, "rho": 0.82},
        "sensitivity": {
            "theta_min": 0.5,
            "theta_max": 0.9,
            "theta_steps": 4,
            "rho_min": 0.5,
            "rho_max": 0.9,
            "rho_steps": 4,
            "base_replicas": 1,
            "improved_replicas": 3,
        },
        "async_side_effect": {"theta": 0.97, "rho_sync": 0.96, "rho_async": 0.85},
        "failure_domain": {"entry_theta": 1.0, "replica_theta": 0.9, "replica_count": 3, "rho": 0.95},
        "timeout": {
            "theta": 0.98,
            "rho": 0.97,
            "path_edges": 1,
            "on_time_probabilities": {"50ms": 0.55},
            "retry_counts": [0, 1],
        },
        "trace_incompleteness": {
            "degree": 3,
            "theta": 0.97,
            "rho": 0.95,
            "replica_count": 2,
            "omission_rates": [0.0, 0.2],
        },
    }


if __name__ == "__main__":
    unittest.main()
