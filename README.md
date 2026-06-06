# Stochastic Connectivity Synthetic Experiments Artifact

This repository contains the standalone synthetic experiment artifact for the
stochastic connectivity study on microservice availability.

The artifact is self-contained: it does not import code, configurations, or
results from parent directories. The committed outputs can be regenerated from
the Python package and `configs/stochastic_connectivity_synthetic.yaml`.

## Repository Layout

- `src/stochconn/` - implementation of the stochastic connectivity model,
  oracle formulas, Monte Carlo estimators, synthetic graph families, boundary
  scenarios, plotting, and report generation.
- `stochconn/` and `sitecustomize.py` - local checkout wrappers that allow
  `python -m stochconn` without installation.
- `configs/stochastic_connectivity_synthetic.yaml` - full deterministic experiment
  configuration used for regenerated outputs.
- `outputs/` - generated CSV files, report, snippets, heatmaps, and manifest.
- `tests/` - unit, boundary, CLI smoke, and output-marker tests.
- `scripts/` - one-command reproduction and output verification helpers.
- `docs/` - experiment design, reproducibility protocol, and result summary.

## Quick Start

From this directory:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python -m stochconn run --config configs/stochastic_connectivity_synthetic.yaml --out outputs
python scripts/verify_outputs.py --out outputs
```

Or run the full Windows helper:

```powershell
.\scripts\run_all.ps1
```

The run regenerates:

- `outputs/raw_results.csv`
- `outputs/table2_summary.csv`
- `outputs/scale_sanity.csv`
- `outputs/table2_snippets.md`
- `outputs/report.md`
- `outputs/fig_synthetic_boundaries.png`
- `outputs/fig_synthetic_boundaries_acm.png`
- `outputs/manifest.yaml`

## Output Integration

Use `outputs/table2_summary.csv` for Table 2, `outputs/table2_snippets.md` for
short replacement text, and `outputs/fig_synthetic_boundaries_acm.png` as the
ACM-sized Figure 1 asset.

The manifest records the seed, dependency versions, config hash, and generated
files. A fixed seed makes the Monte Carlo checks deterministic.

## Dependencies

The artifact uses only:

- Python 3.11+
- `numpy`
- `matplotlib`
- `PyYAML`

No `pandas`, `scipy`, external experiment framework, or parent-directory package
is required.

## License

This artifact is released under the MIT License. See `LICENSE`.
