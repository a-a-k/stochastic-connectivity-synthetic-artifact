# Result Summary

The committed outputs were generated from `configs/stochastic_connectivity_synthetic.yaml`.

## Table 2 Values

- Synchronous chain: closed form matched; max MC error 0.0014.
- Fan-out: degree 1 to 12 drops availability from 0.894 to 0.364.
- Replicated bottleneck: target replicas 1 to 12 raise availability from 0.738
  to 0.820, bounded by edge reliability 0.82.
- Node-vs-edge sensitivity: max replication gain 0.373; edge-dominant cells
  94%.
- Async side effect: immediate delta 0; eventual-completion availability is
  lower by 0.289.
- Failure domain: independent product baseline overestimates the correlated
  reference by 0.094.
- Timeout/hang: max connectivity false positive 0.399; retries recover 0.318.
- Trace incompleteness: max absolute bias 0.594; hidden dependencies
  overestimate by 0.118.

## Large-Family Sanity Layer

Synchronous chains reached 257 services and 256 required edges. Fan-out graphs
reached 129 services and 128 required edges. Replicated bottlenecks reached 64
target replicas. The smallest large-family availability was 0.00577. Sentinel
Monte Carlo checks used N=50,000 and produced max absolute error 0.0020.

## Generated Assets

- Table data: `outputs/table2_summary.csv`
- Snippets: `outputs/table2_snippets.md`
- Full report: `outputs/report.md`
- Figure source: `outputs/fig_synthetic_boundaries.png`
- ACM-sized figure: `outputs/fig_synthetic_boundaries_acm.png`
