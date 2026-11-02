# WORK-003 FE request-material API read-only review

Review the latest FE-only request-material integration in
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`.

- Do not edit code/tests/docs; do not run tests/build/DB/E2E.
- Write only `orchestration/work/strong-hajin-work/review-fe-materials-report.md`.
- Send worker_done to coordinator `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`.

Check file:line evidence for:

1. Request create still sends the existing payload only; returned `request_id` is used for
   file and link uploads through the five backend routes, with no material_ids,
   attachments, or material_draft_ids in create payload.
2. Request file/link success, per-item failure and retry behavior are real; successful items
   are not uploaded twice; existing 내 업무 task-material flow is preserved.
3. `REQUEST_MATERIALS_SAVED=false` and stale request-material warning are removed only for
   the normal request branch. UI does not claim a failed item was saved.
4. Tests are focused and the reported meeting-promotion `request_id` blocker is explicitly
   isolated rather than hidden or bypassed.
5. Allowed paths and no unrelated backend changes in this FE dispatch.

Verdict PASS/WARN/FAIL. Tests are forbidden in this review; treat worker-reported numbers as
unverified and state that clearly.
