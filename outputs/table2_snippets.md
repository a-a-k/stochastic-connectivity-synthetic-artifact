# Reusable snippets

## Table 2 result cells

- **Synchronous chain**: closed form matched; max MC error 0.0014
- **Fan-out**: d=1->12 drops 0.894->0.364
- **Replicated bottleneck**: R=1->12 rises 0.738->0.820, bounded by rho=0.82
- **Node vs. edge sensitivity**: max replication gain 0.373; edge-dominant cells 94%
- **Async side effect**: immediate delta 0.000000; eventual lower by 0.289
- **Failure domain**: product overestimates correlated reference by 0.094
- **Timeout/hang**: max connectivity false positive 0.399; retries recover 0.318
- **Trace incompleteness**: max abs bias 0.594; hidden deps overestimate by 0.118

## Scale sanity paragraph

As a large-family sanity check, the oracle families were extended beyond the compact Table 2 grid. Synchronous chains reached up to 257 services and 256 required edges, fan-out graphs reached substantially larger mandatory dependency sets, and replicated bottlenecks reached up to 64 target replicas. Closed-form values preserved the same qualitative regimes: long mandatory chains and fan-outs decayed multiplicatively, while replicated bottlenecks saturated at the required edge reliability. The smallest large-family availability was 0.00577. Selected sentinel cells were also checked by Monte Carlo sampling with N=50,000; the maximum absolute error was 0.0020, within the maximum 95% confidence half-width of 0.0044.

## Interpretation paragraph

The oracle checks support the implementation: the chain max Monte Carlo error is 0.0014 within sampling error, fan-out degrades multiplicatively, and the replicated bottleneck approaches but does not exceed the required edge reliability. The async contrast gives zero immediate-response delta and a 0.289 eventual-completion delta. Correlated domains, timed failures, and trace omissions produce systematic gaps up to 0.594, which identifies the boundary where the baseline product connectivity model needs richer semantics.

## Figure caption note

Heatmap color is the exact availability gain from increasing the target service from one to three replicas; the white contour marks rho equal to the replicated service live probability.
