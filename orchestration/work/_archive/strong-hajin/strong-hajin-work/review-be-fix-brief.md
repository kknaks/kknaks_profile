# WORK-003 BE F-1/F-2 read-only re-review

Review only the latest backend fix. Do not edit code, tests, docs, or inventory. Do not run
tests/build/DB/E2E. Write only `orchestration/work/strong-hajin-work/review-be-fix-report.md`
and send worker_done to coordinator `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`.

Check with file:line evidence:

1. F-1: `POST /api/work-requests/{request_id}/materials` is no longer marked verified against
   `file_attachment_request` when that AX intent routes to evidence. Confirm inventory is E2
   excluded with a clear reconsideration note, `operation_inventory.py` has no stale override,
   and no existing evidence intent was broadened.
2. F-2: legacy request-material attachment opening returns the existing client error for link
   sources instead of storage-key 500, while file download remains unchanged. Confirm the new
   focused regression is present and scoped.
3. Allowed paths and test scope: only the brief's two focused regressions plus the inventory
   guard were run; record worker-reported numbers as unverified because this review runs no tests.
4. Record remaining prior risks (four contract failures, checkout incident) without reopening
   unrelated work.

Verdict PASS/WARN/FAIL. If either fix is incomplete, FAIL and stop; do not ask for broad tests.
