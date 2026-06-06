from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from .experiments import ExperimentRunner, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stochconn")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--config", required=True)
    run_parser.add_argument("--out", required=True)
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args(argv)
    args.func(args)
    return 0


def cmd_run(args: argparse.Namespace) -> None:
    config_path = _resolve_input(args.config)
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    runner = ExperimentRunner(config)
    bundle = runner.run()
    out_dir = Path(args.out)
    paths = write_outputs(bundle, out_dir, config_path)
    print(f"wrote {len(paths)} outputs to {out_dir.resolve()}")


def _resolve_input(path: str) -> Path:
    candidate = Path(path)
    if candidate.exists():
        return candidate
    artifact_root = Path(__file__).resolve().parents[2]
    rooted = artifact_root / path
    if rooted.exists():
        return rooted
    raise FileNotFoundError(path)
