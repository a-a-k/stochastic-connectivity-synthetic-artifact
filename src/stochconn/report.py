from __future__ import annotations

import csv
import hashlib
import platform
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

import matplotlib
import numpy as np
import yaml


RAW_FIELDNAMES = [
    "suite_id",
    "family",
    "scenario_id",
    "metric_kind",
    "n_services",
    "n_edges",
    "n_instances",
    "theta",
    "rho",
    "k_edges",
    "degree",
    "replicas",
    "exact_availability",
    "mc_estimate",
    "mc_abs_error",
    "ci_half_width",
    "baseline_availability",
    "reference_availability",
    "gap",
    "signed_bias",
    "note",
]

SUMMARY_FIELDNAMES = [
    "family",
    "varied_parameter",
    "adequacy_question",
    "result",
    "primary_value",
    "max_mc_abs_error",
    "details",
]

SCALE_FIELDNAMES = [
    "suite_id",
    "graph_family",
    "scenario_id",
    "metric_kind",
    "n_services",
    "n_edges",
    "n_instances",
    "theta",
    "rho",
    "k_edges",
    "degree",
    "replicas",
    "exact_availability",
    "mc_estimate",
    "mc_abs_error",
    "ci_half_width",
    "note",
]


def write_csv(path: str | Path, rows: list[dict[str, object]], fieldnames: list[str]) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(row.get(key, "")) for key in fieldnames})
    return out


def write_report(
    path: str | Path,
    summary_rows: list[dict[str, object]],
    scale_rows: list[dict[str, object]],
    context: dict[str, object],
) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Synthetic adequacy report",
        "",
        f"Suite: `{context['suite_id']}`",
        f"Seed: `{context['seed']}`",
        f"Monte Carlo samples per oracle validation cell: `{context['mc_samples']}`",
        "",
        "## Table 2 results",
        "",
    ]
    for row in summary_rows:
        lines.extend(
            [
                f"### {row['family']}",
                "",
                f"- Varied parameter: {row['varied_parameter']}",
                f"- Adequacy question: {row['adequacy_question']}",
                f"- Result: {row['result']}",
                f"- Details: {row['details']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Scale sanity extension",
            "",
            str(context["scale_sanity_paragraph"]),
            "",
            f"Scale rows: `{len(scale_rows)}`",
            "",
            "## Interpretation paragraph",
            "",
            str(context["interpretation_paragraph"]),
            "",
            "## Generated files",
            "",
        ]
    )
    for file_name in context["generated_files"]:
        lines.append(f"- `{file_name}`")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def write_snippets(
    path: str | Path,
    summary_rows: list[dict[str, object]],
    scale_rows: list[dict[str, object]],
    context: dict[str, object],
) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Reusable snippets",
        "",
        "## Table 2 result cells",
        "",
    ]
    for row in summary_rows:
        lines.append(f"- **{row['family']}**: {row['result']}")
    lines.extend(
        [
            "",
            "## Scale sanity paragraph",
            "",
            str(context["scale_sanity_paragraph"]),
            "",
            "## Interpretation paragraph",
            "",
            str(context["interpretation_paragraph"]),
            "",
            "## Figure caption note",
            "",
            str(context["figure_caption_note"]),
        ]
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def write_manifest(
    path: str | Path,
    *,
    suite_id: str,
    seed: int,
    config_path: str | Path,
    generated_files: Iterable[str],
) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "suite_id": suite_id,
        "seed": seed,
        "created_at": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "platform": f"{platform.system()} {platform.release()}",
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "pyyaml": yaml.__version__,
        "config_path": str(config_path),
        "config_sha256": sha256_file(config_path),
        "generated_files": list(generated_files),
    }
    out.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return out


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def ensure_no_marker_text(paths: Iterable[str | Path]) -> None:
    forbidden = ("TO" + "DO", "T" + "BD", "PLACE" + "HOLDER", "place" + "holder")
    for path in paths:
        text = Path(path).read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                raise ValueError(f"forbidden marker token {token!r} found in {path}")


def _csv_value(value: object) -> object:
    if isinstance(value, float):
        return f"{value:.12g}"
    return value
