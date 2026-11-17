# Delivery #254 마감 리포트 — v2 재결속 · 승인 receipt · 마감 댓글 · 닫기 (2026-11-17)

mediness 워크트리 `fix-feedback-delivery` = detached origin/main `4443a99ac616cc29bf681cf47a84f719d532fb94`(실행 직전 fetch 값과 같음). 코드 워크트리 `CENTURION_DAY/fix-feedback-delivery` = dev `0c401726`. 두 워크트리 모두 파일 수정 · 커밋 · push 0. CLI = `uv run --project tools/harness mediness …`.

## 결과

| 항목 | 값 |
|---|---|
| Issue | CENTURION_DAY#254 — **CLOSED (completed)** |
| 최종 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` |
| key · version | `day/fix-feedback-2026-11-17` · contract_version **2** · risk L2 |
| baseline | `4443a99ac616cc29bf681cf47a84f719d532fb94`(mediness#945) |
| target_specs | DAY-SPEC-002 · DAY-SPEC-005 · DAY-SPEC-003 |
| contract digest | `sha256:74b446e77b6be700f9274200a8af47a47ebad4b2c50086e7574e62fe4d14a299` |
| plan_digest | `sha256:b39ede6a290592528dda459d19be6925b014ade38975f7de9081f16689c76b9b` — v2 plan · apply · receipt plan · receipt apply 네 번 모두 같음(v1 `06bfccd8…` 에서 바뀜) |
| receipt | `delivery/fb.v2.approval-receipt.json` — approved · human · kknaksss · 위 digest. 근거 = 사용자 2026-11-17 코디 대화 「스펙 묶고 승인하고 이슈 정리하자」(E2E 2회 뒤) |
| plan_review | `approved` |
| 마감 댓글 | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/254#issuecomment-6940495119 (본문 `delivery/fb.close-comment.md`) |

## 명령 · 결과

1. `start-delivery --request fb.v2.request.json --mediness-repo <M> --code-repo <C> --github-repo MediSolveAIDev/CENTURION_DAY --plan --json` → `planned` · next `review-delivery-plan`(human_gate) · plan_review `review-required` → `fb.v2.plan.json`
2. 같은 명령 `--apply` → `scope-delta-recorded`(scope_delta 가 처음부터 있어 conflict 없이 한 번에) · `delivery-plan:review` → `fb.v2.apply.json`
3. `+ --plan-approval-receipt fb.v2.approval-receipt.json --plan` → `planned` · plan_review `approved` · next `implement-and-open-code-pr` → `fb.v2.approve.plan.json`
4. 같은 `--apply` → `execution-updated` · 라벨 `delivery-plan:approved` → `fb.v2.approve.apply.json`
5. closeout 시도: `spec-sync --request fb.closeout.spec-sync.request.json --plan` → rc 2 `conflict`: 「dashboard.content_digest Field required」(→ `fb.closeout.spec-sync.plan.json`). dashboard projection digest 는 mediness sync PR 경로에서만 나오므로 제품 레포 Delivery 에서 못 도는 알려진 제약 #749 그대로 → 댓글 + `gh issue close 254 --reason completed` 로 대신.

## v2 결과 계약 요약 (v1 → v2)

- **target_delta 10**: F-1 · F-2 · F-3 · **F-5(줄 ⋮ 되돌리기 · 호출 취소 DAY 만 · 알림 없음)** · F-4(늘 띄움 · E5) · F-6 · **E6**(시술 이름 글자만 + 호버 「차트 작성」) · **E3**(「간호관리」 · systemDoctor 진행중 · 완료 줄만) · **E2**(팝오버 잘림 버그) · F-7.
- **acceptance A1~A9** — v1 A1~A7 을 머지 코드 · 결정에 맞게 고치고 A4(간호관리) · A5(⋮ 되돌리기) 추가 · A9 앱 코드 변경 0.
- **non_goals**: F-5 보류 삭제 · 호출 취소 알림(enum migration) · 앱 푸시 · KOS 호출 취소 쓰기 추가 · migration · 빈 방 · 웹 푸시 · 앱 변경 · 단건 no_doctor 완화 · 기획안.
- **review_surface 2**: 토스트 글자 3(conflict · task_not_called · visit_not_home) · KOS 기기 제한은 범위 밖 후속.
- **scope_delta**: E2E 2회 · 사용자 2026-11-17 결정 · baseline #945 · execution = #255 기준.
- **execution**: code_surface = #255 diff 19파일 기준 · verification = pytest 1298 · E2E 2회 · dev run 44028948837 · lint · rollback = #255 revert(migration 없음).

## 주의

- apply 결과 `partial: true` — `task_projection` pending(MCP `mediness.task_draft_request` 미호출). android-app 과 같음 · 지시서 범위 밖이라 하지 않음.
- 마지막 apply status 는 `execution-updated`(승인 상태는 plan_review · 라벨로 확인). next_action `implement-and-open-code-pr` 는 이미 머지된 #255 로 충족 — Issue 는 닫힘.
- 비밀값 · 계정 이메일 출력 0.

## 파일 (`delivery/`)

`fb.v2.request.json` · `fb.v2.plan.json` · `fb.v2.apply.json` · `fb.v2.approval-receipt.json` · `fb.v2.approve.plan.json` · `fb.v2.approve.apply.json` · `fb.closeout.spec-sync.request.json` · `fb.closeout.spec-sync.plan.json` · `fb.close-comment.md`
