# WORK-003 FE request-material API integration

## Goal

Connect the existing request-creation modal's **자료** tab to the already implemented
request-material REST contract. The backend contract is two-step: create the request first,
then use the returned `request_id`; do not add material fields to the create payload.

## Contract

- `POST /api/work-requests/{request_id}/materials` multipart file upload
- `POST /api/work-requests/{request_id}/materials/links` link creation
- `GET /api/work-requests/{request_id}/materials` list
- `GET /api/work-requests/{request_id}/materials/{material_id}/content` download/open
- `DELETE /api/work-requests/{request_id}/materials/{material_id}` detach

For **내 업무**, preserve the existing task-material flow. For **업무 요청**, after the
request create succeeds, upload selected files and links through the new request endpoints.
Show per-item progress/error and allow retry for failed items; do not silently claim that
request materials are unsaved. If the request create succeeds but an attachment fails,
keep the request and report the failed item clearly.

## Constraints

- Allowed paths: `frontend/src/**` and the smallest relevant frontend tests only.
- Do not touch backend, para, inventory, or unrelated UI.
- No new payload keys such as `material_ids`, `attachments`, or `material_draft_ids`.
- Remove/replace the `REQUEST_MATERIALS_SAVED=false` behavior and stale alert only for the
  request branch. Keep the current tab/frame and both-branch materials UI.
- Add at most 3 focused tests: request file upload, request link upload, and partial-failure
  reporting/retry. Do not run the full frontend suite; run only those focused tests and
  `tsc --noEmit`.
- If an existing API response or upload helper cannot support the contract, stop and report
  the exact blocker instead of inventing a route or fallback.

## Report

Report changed files, exact focused test/tsc results, and any blocker. No commit/push/PR.
