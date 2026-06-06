#!/usr/bin/env sh
set -eu

PYTHON="${PYTHON:-python3}"
OUT="${OUT:-outputs}"
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

cd "$ROOT"
"$PYTHON" -m pip install -r requirements.txt
"$PYTHON" -m unittest discover -s tests
"$PYTHON" -m stochconn run --config configs/stochastic_connectivity_synthetic.yaml --out "$OUT"
"$PYTHON" scripts/verify_outputs.py --out "$OUT"
