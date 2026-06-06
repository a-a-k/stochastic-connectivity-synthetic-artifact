# Synthetic adequacy report

Suite: `stochastic_connectivity_synthetic`
Seed: `20260605`
Monte Carlo samples per oracle validation cell: `200000`

## Table 2 results

### Synchronous chain

- Varied parameter: Length k, theta, rho
- Adequacy question: Does simulation match the node+edge closed form?
- Result: closed form matched; max MC error 0.0014
- Details: Exact availability ranged from 0.1668 to 0.9703; max 95% CI half-width 0.0022.

### Fan-out

- Varied parameter: Branching degree d, edge reliability rho
- Adequacy question: How quickly do mandatory AND dependencies degrade availability?
- Result: d=1->12 drops 0.894->0.364
- Details: At theta=0.97, rho=0.95, absolute drop was 0.530.

### Replicated bottleneck

- Varied parameter: Replica count R(v), fixed rho_e
- Adequacy question: Does replication help against node failures but saturate at an edge bottleneck?
- Result: R=1->12 rises 0.738->0.820, bounded by rho=0.82
- Details: Remaining distance to edge bound at R=12 was 0.000000.

### Node vs. edge sensitivity

- Varied parameter: Grid over theta and rho
- Adequacy question: When does edge reliability dominate node replication?
- Result: max replication gain 0.373; edge-dominant cells 94%
- Details: Mean gain was 0.155 in edge-dominant cells and 0.319 elsewhere.

### Async side effect

- Varied parameter: Immediate Phi_Imm vs eventual Phi_Evt
- Adequacy question: Are async edges invariant only for immediate response?
- Result: immediate delta 0.000000; eventual lower by 0.289
- Details: Immediate exact availability 0.9033; eventual exact availability 0.6140.

### Failure domain

- Varied parameter: Co-location and domain failure probability
- Adequacy question: What gap appears between product and correlated P?
- Result: product overestimates correlated reference by 0.094
- Details: Product baseline 0.9490; correlated reference 0.8550.

### Timeout/hang

- Varied parameter: Delay, timeout, retry count
- Adequacy question: Where does pure connectivity produce false positives?
- Result: max connectivity false positive 0.399; retries recover 0.318
- Details: Timed reference multiplies connectivity by the probability of at least one on-time attempt.

### Trace incompleteness

- Varied parameter: Edge/instance omission rate
- Adequacy question: What bias follows from partial model discovery?
- Result: max abs bias 0.594; hidden deps overestimate by 0.118
- Details: Edge-only omissions underestimated by 0.594; replica undercount by 0.069.

## Scale sanity extension

As a large-family sanity check, the oracle families were extended beyond the compact Table 2 grid. Synchronous chains reached up to 257 services and 256 required edges, fan-out graphs reached substantially larger mandatory dependency sets, and replicated bottlenecks reached up to 64 target replicas. Closed-form values preserved the same qualitative regimes: long mandatory chains and fan-outs decayed multiplicatively, while replicated bottlenecks saturated at the required edge reliability. The smallest large-family availability was 0.00577. Selected sentinel cells were also checked by Monte Carlo sampling with N=50,000; the maximum absolute error was 0.0020, within the maximum 95% confidence half-width of 0.0044.

Scale rows: `38`

## Interpretation paragraph

The oracle checks support the implementation: the chain max Monte Carlo error is 0.0014 within sampling error, fan-out degrades multiplicatively, and the replicated bottleneck approaches but does not exceed the required edge reliability. The async contrast gives zero immediate-response delta and a 0.289 eventual-completion delta. Correlated domains, timed failures, and trace omissions produce systematic gaps up to 0.594, which identifies the boundary where the baseline product connectivity model needs richer semantics.

## Generated files

- `raw_results.csv`
- `table2_summary.csv`
- `scale_sanity.csv`
- `fig_synthetic_boundaries.png`
- `fig_synthetic_boundaries_acm.png`
- `table2_snippets.md`
- `report.md`
- `manifest.yaml`
