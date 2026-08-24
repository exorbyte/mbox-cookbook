# TODO

## `08-production/`

Deferred for now. Not linked from the README until it's built (link is commented out there).

Planned notebooks, when we pick this back up:

1. **Benchmarking match performance at scale** — index build time and query latency as row count grows (1K → 100K+), so someone can size a deployment before committing to it.
2. **Validating match quality against ground truth** — a labeled set of known duplicate/non-duplicate pairs, sweep thresholds, report precision/recall. Turns `05-explainability`'s "why did this score X" into "is X actually the right cutoff."
3. **Index refresh strategy in production** — rebuilding an index when the master table changes without downtime (build new, swap, retire old); every prior notebook builds an index once and never revisits this.

Suggested starting point: #2, since it's the first notebook in the repo that answers "is this working well enough to ship" rather than "how do I call this."
