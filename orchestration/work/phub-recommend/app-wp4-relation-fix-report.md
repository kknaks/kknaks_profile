# WP-4 relation adapter review fixes

2026-11-02 · app worktree `hub-evals`, base HEAD `078ac99` (existing uncommitted WP-4 work preserved)

## Changes

- F-1: A lone resolved unit in I-07 no longer becomes `(unit, unit)` unless the question explicitly asks for the same procedure again. An unresolved second target stays `unresolved_pair`; no pair absence is inferred.
- F-2: Relation facets are now recorded separately for each selected pair and Q139 global scope. A supported R8 pair cannot mark a failed, truncated, or build-mismatched global scope supported or complete. Selected relation facts retain their scope key.
- F-3: Global `applies_to.condition` is checked against an explicitly established question condition. The adapter fetches the whole global scope without a condition filter so unconditional notes remain available, then gates conditional rows locally using the Hub's exact string condition contract.
- F-4: Complete selected-pair `resolved.value`, `field_status`, `by_direction`, and `source_fact_ids` enter the answer payload only when all source fact IDs were independently selected. The source rows travel with that metadata. Split payloads include the resolved structure only in a part containing all its sources. Unproven policy values remain in the collection trace, not answer evidence.
- F-5: I-08 prior procedure is bound to the resolved span identified by prior wording. If prior identity is unresolved, no directional prior input is sent and the pair facet stays blocked.

## Verification

- Focused relation tests: `uv run pytest -q tests/phase8/test_relation_adapter.py` — 26 passed.
- Full app tests: `uv run pytest -q` — 282 passed.
- `uv run ruff check .` — passed.
- `git diff --check` — passed.
- Mock Hub negative cases cover one target/self-pair prevention, global 404/error/truncation/build mismatch, exact global condition gating, resolved source binding, and reverse prior direction. No real server, database, provider, or evaluation batch was used.

## Remaining gate

Real Hub and app build-hash parity, question replay on the actual Gold graph, and the 50-question promotion gate remain for the coordinator before activation. No commit, push, or PR was made.
