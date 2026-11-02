# WORK-003 backend contract failure audit (read-only)

Investigate, do not fix, the four unresolved contract failures from the prior backend run:

- `tests/contract/test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result`
- `tests/contract/test_material_worker_recovery.py::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it`
- `tests/contract/test_material_search.py::test_naming_the_work_still_scopes_the_search_to_it`
- `tests/contract/test_material_search.py::test_search_returns_bounded_excerpts_only_for_authorized_live_bindings`

## Rules

- Read-only investigation: no source, tests, inventory, docs, checkout, reset, stash, commit,
  or push.
- Run only these four tests, one file/test at a time and then (if useful) the two test files
  sequentially. Do not run full unit/contract/verify suites.
- Capture exact failure output, first failing assertion/exception, and whether it reproduces
  sequentially. Trace whether the new request-material changes can reach the failing setup;
  if not, say why with file:line evidence. Do not call them flaky without evidence.
- If the environment prevents a meaningful reproduction, report that blocker instead of
  inventing a baseline.

Write only `orchestration/work/strong-hajin-work/be-contract-failure-audit.md` and send
worker_done to coordinator `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`. Keep the report concise.
