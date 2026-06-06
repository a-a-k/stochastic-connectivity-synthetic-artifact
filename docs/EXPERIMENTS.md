# Experiment Design

The artifact implements the synthetic adequacy study for the stochastic
connectivity model. A model instance consists of service types, synchronous and
asynchronous dependency edges, replica counts, node live probabilities, edge
live probabilities, a probability measure, and endpoint predicates.

## Oracle Families

1. Synchronous chain
   - Varies chain length, node live probability, and edge live probability.
   - Compares Monte Carlo estimates against the exact node-and-edge path
     product formula.

2. Fan-out
   - Varies mandatory branch degree.
   - Demonstrates multiplicative degradation under AND dependencies.

3. Replicated bottleneck
   - Varies target replica count with a fixed required edge reliability.
   - Demonstrates that replication improves node liveness but saturates at the
     logical edge bottleneck.

4. Node-vs-edge sensitivity
   - Sweeps node live probability and edge live probability.
   - Generates the heatmap of availability gain from increasing the target from
     one to three replicas.

## Boundary Families

1. Async side effect
   - Compares immediate-response and eventual-completion predicates.
   - Confirms that asynchronous edges are invariant only for the immediate
     predicate when the async work is not required for HTTP success.

2. Failure domain
   - Compares the independent product baseline with a same-marginal correlated
     failure-domain reference.

3. Timeout/hang
   - Compares pure connectivity with timed success under delay, timeout, and
     retries.

4. Trace incompleteness
   - Omits edges or replicas and measures signed and absolute availability bias.

## Scale Sanity Layer

The large-family extension increases oracle graph sizes beyond the compact Table
2 grid. It checks chains up to 257 services, fan-out graphs up to 129 services,
and replicated bottlenecks up to 64 target replicas. Closed-form values are
computed for all large cells; selected sentinel cells also receive Monte Carlo
checks.
