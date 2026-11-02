# WORK-003 BE API gap — reviewer FAIL fixes only

## Context

The implementation worker completed the request-material REST contract. Read-only review
`review-be-api-gap-report.md` found two FAILs. Fix only these two; do not redesign the
payload or add unrelated features.

## Required fixes

### F-1: AX mapping must not misroute request materials

`POST /api/work-requests/{request_id}/materials` is marked `verified` in
`docs/unified-operations-inventory.json` with `target_tools: ["file_attachment_request"]`,
but the current AX intent list has no request-material intent and routes the call to evidence.
Choose the smallest contract-consistent fix:

- mark that HTTP operation `excluded`/E2 with a precise reconsideration note until an AX
  request-material intent exists; or
- implement the complete `request_material` AX intent and route/authorize it to the new
  request-material service, then keep `verified`.

Do not leave a verified row that actually uploads evidence. Do not silently broaden the
existing evidence intent.

### F-2: link material through legacy open path must not 500

`material_bindings()` now exposes request materials to the legacy attachment view. A link
attachment currently reaches `open_attachment` and passes its URL to local storage, causing
`ValueError("invalid material storage key")` and HTTP 500. Add the same non-file guard used
by the new request-material download path, mapped to the existing client error (422), or
otherwise route links through the existing link response. Keep file download behavior
unchanged.

## Constraints

- Allowed paths only: `backend/src/ax_workspace/**`, `backend/tests/contract/**`,
  `backend/tests/unit/**`, `docs/unified-operations-inventory.json`.
- No frontend, para, orchestration report, migration, checkout/reset/stash, commit, push,
  or PR.
- Do not add a broad test matrix. Add at most two focused regression tests: one for the AX
  mapping decision (or inventory assertion) and one for opening a request link material
  through the legacy path. Reuse existing fixtures.
- Run only the two focused tests and report exact results. Do not rerun full unit/contract,
  scale, release, postgres, or verify suites. If a test or code contract is blocked, stop
  and report the blocker immediately instead of inventing a workaround.

## Required report

Report changed files, exact test command/results, and any unresolved issue. Explicitly state
whether the two FAILs are closed. Do not claim the previous four contract failures are fixed.
