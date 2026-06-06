# Reproducibility Protocol

## Environment

Use Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On Unix-like systems:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## Full Run

```powershell
python -m unittest discover -s tests
python -m stochconn run --config configs/stochastic_connectivity_synthetic.yaml --out outputs
python scripts/verify_outputs.py --out outputs
```

The full run is deterministic under the seed in the YAML config. Generated
outputs include raw simulation rows, Table 2 summary rows, scale sanity rows,
table snippets, a Markdown report, two heatmap PNGs, and a manifest.

## Verification Checks

The tests and verifier check:

- closed-form path reliability includes both node and edge probabilities;
- exact enumeration and oracle formulas agree on small families;
- availability is monotone in node and edge live probabilities;
- replicated bottlenecks do not exceed their required edge reliability;
- asynchronous edges do not affect immediate predicates but do affect eventual
  predicates;
- correlated domains, timeouts, and trace omissions produce expected gaps;
- the CLI creates every declared output;
- generated report/snippet files contain no unresolved marker text;
- the manifest config hash matches the current config.

## Expected Runtime

Runtime depends on CPU and installed BLAS, but the full run is designed to be
small enough for artifact review. The configuration uses 200,000 Monte Carlo
samples for compact oracle cells and 50,000 samples for large-family sentinel
checks.
