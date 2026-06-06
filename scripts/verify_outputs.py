from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

import yaml


EXPECTED_FILES = [
    "raw_results.csv",
    "table2_summary.csv",
    "scale_sanity.csv",
    "table2_snippets.md",
    "report.md",
    "fig_synthetic_boundaries.png",
    "fig_synthetic_boundaries_acm.png",
    "manifest.yaml",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="outputs")
    parser.add_argument("--config", default="configs/stochastic_connectivity_synthetic.yaml")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    out_dir = (root / args.out).resolve()
    config_path = (root / args.config).resolve()

    errors: list[str] = []
    for name in EXPECTED_FILES:
        path = out_dir / name
        if not path.exists():
            errors.append(f"missing output: {name}")
        elif path.stat().st_size == 0:
            errors.append(f"empty output: {name}")

    if not errors:
        errors.extend(_check_csv(out_dir / "table2_summary.csv", expected_rows=8, label="table2_summary.csv"))
        errors.extend(_check_csv(out_dir / "raw_results.csv", min_rows=50, label="raw_results.csv"))
        errors.extend(_check_csv(out_dir / "scale_sanity.csv", min_rows=1, label="scale_sanity.csv"))
        errors.extend(_check_text(out_dir / "report.md"))
        errors.extend(_check_text(out_dir / "table2_snippets.md"))
        errors.extend(_check_manifest(out_dir / "manifest.yaml", config_path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"verified {len(EXPECTED_FILES)} outputs in {out_dir}")
    return 0


def _check_csv(path: Path, label: str, expected_rows: int | None = None, min_rows: int | None = None) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if expected_rows is not None and len(rows) != expected_rows:
        return [f"{label}: expected {expected_rows} rows, got {len(rows)}"]
    if min_rows is not None and len(rows) < min_rows:
        return [f"{label}: expected at least {min_rows} rows, got {len(rows)}"]
    return []


def _check_text(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    markers = ["TO" + "DO", "T" + "BD", "PLACE" + "HOLDER", "FIX" + "ME", "?" + "?"]
    return [f"{path.name}: contains marker {marker}" for marker in markers if marker in text]


def _check_manifest(path: Path, config_path: Path) -> list[str]:
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    generated = manifest.get("generated_files", [])
    for name in EXPECTED_FILES:
        if name not in generated:
            errors.append(f"manifest missing generated file: {name}")
    actual_hash = hashlib.sha256(config_path.read_bytes()).hexdigest()
    if manifest.get("config_sha256") != actual_hash:
        errors.append("manifest config_sha256 does not match current config")
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
