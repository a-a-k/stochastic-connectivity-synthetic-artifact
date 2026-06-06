param(
    [string]$Python = "python",
    [string]$Out = "outputs"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $Root
try {
    & $Python -m pip install -r requirements.txt
    & $Python -m unittest discover -s tests
    & $Python -m stochconn run --config configs/stochastic_connectivity_synthetic.yaml --out $Out
    & $Python scripts/verify_outputs.py --out $Out
}
finally {
    Pop-Location
}
