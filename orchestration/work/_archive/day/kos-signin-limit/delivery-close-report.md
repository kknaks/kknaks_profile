# Delivery #256 마감 리포트 — v2 재결속 · 승인 receipt · 마감 댓글 · 닫기 (2026-11-17)

mediness 워크트리 `kos-signin-limit-delivery` = detached origin/main `51f85837c11a4c9904a04d6f27da4dc129fe844b`(실행 직전 fetch 값과 같음). 코드 워크트리 `CENTURION_DAY/kos-signin-limit-delivery` = dev `a6aa4ba5`. 두 워크트리 모두 파일 수정 · 커밋 · push 0(git status clean · uv 가 gitignore 된 `tools/harness/.venv` 만 만듦). CLI = `uv run --project tools/harness mediness start-delivery …`.

## 결과

| 항목 | 값 |
|---|---|
| Issue | CENTURION_DAY#256 — **CLOSED (completed)** |
| 최종 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` |
| key · version | `day/kos-signin-limit-2026-11-17` · contract_version **2** · risk L3 |
| baseline | `51f85837c11a4c9904a04d6f27da4dc129fe844b`(mediness#946) |
| target_specs | DAY-SPEC-001 · DAY-SPEC-003 · DAY-SPEC-000 · **DAY-SPEC-002**(v2 추가) |
| contract digest | `sha256:29597c5791f7704daf9d2e1ea4541c843e8e7f3d4b16799c3f4a4a064578467e` |
| plan_digest | `sha256:9db0b7aa001862acaa45c83b93a337616cbe41fa698488bdd97a138934240fa5` — v2 plan · apply · receipt plan · receipt apply 네 번 모두 같음(v1 `38a941dd…` 에서 바뀜) |
| receipt | `delivery/ksl.v2.approval-receipt.json` — approved · human · kknaksss · 위 digest. 근거 = 사용자 2026-11-17 코디 대화 「회고 개념 정리 다 정리하고 스쿼시 머지 하자」(로컬 직접 확인 뒤) |
| plan_review | `approved` |
| 마감 댓글 | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/256#issuecomment-6945296877 (본문 `delivery/ksl.close-comment.md`) |

## 명령 · 결과

1. `--request ksl.v2.request.json --plan --json` → `planned` · next `review-delivery-plan`(human_gate) · plan_review `review-required` → `ksl.v2.plan.json`
2. 같은 `--apply` → `scope-delta-recorded` · `delivery-plan:review` → `ksl.v2.apply.json`
3. `+ --plan-approval-receipt ksl.v2.approval-receipt.json --plan` → `planned` · plan_review `approved` · next `implement-and-open-code-pr` → `ksl.v2.approve.plan.json`
4. 같은 `--apply` → `execution-updated` · 라벨 `delivery-plan:approved` → `ksl.v2.approve.apply.json`
5. 마감: spec-sync closeout 은 #749 제약(지시서대로 시도 안 함) → 댓글 + `gh issue close 256 --reason completed`.

## v2 결과 계약 요약 (v1 → v2)

- **target_delta 7**: K-1 판정 · K-2 시스템 계정(가장 오래된 1개 · 해제 4xx = 실패) · K-3 직원 **웹만** 기기 선택(「처음으로」 없음) + 앱 JSON = 지금과 같은 401 `invalid_credentials`(choose_device · /api/auth/device · 데모 넘김 삭제) · 보안(암호문 · 종류 · 되돌리지 않음) · 오류(잘못된 device_id = session_expired) · K-4 · K-5 · **SPEC-002 ㉓**(차트 영역 · 탭 글자).
- **acceptance A1~A8** — 앱 401 유지(A4) · 화면 ㉓(A7) 반영.
- **non_goals**: 앱 기기 선택 · 로그아웃 해제 · prod 배포와 옛 세션 정리 · OQ-K16 원인 · 목록 표시 구분 · migration · 기획안. (KOS_CLIENT_TAG 값은 Code PR 이 deploy/config 에 넣어 non_goal 에서 뺌)
- **review_surface 2**: 열린 OQ-K6 · K11 · K16 · 운영(prod 값 · 옛 세션 정리).
- **scope_delta**: baseline #946 · 사용자 결정(웹만 · 앱 401 · 가장 오래된 1개 · 처음으로 없음) · ㉓ 추가 · execution = #257 기준.
- **execution**: code_surface = #257 diff 31파일 기준 · verification = 전체 1359 passed · 검수 PASS · 로컬 확인 · dev run 44062996534 · lint · rollback = #257 revert(migration 없음).

## 주의

- apply 결과 `partial: true` — `task_projection` pending(MCP task_draft 미호출) · 앞 사례와 같음 · 범위 밖.
- 마지막 apply status `execution-updated` · next_action `implement-and-open-code-pr` 는 머지된 #257 로 충족 — Issue 는 닫힘.
- 비밀값 · 이메일 · IP 출력 0.

## 파일 (`delivery/`)

`ksl.v2.request.json` · `ksl.v2.plan.json` · `ksl.v2.apply.json` · `ksl.v2.approval-receipt.json` · `ksl.v2.approve.plan.json` · `ksl.v2.approve.apply.json` · `ksl.close-comment.md`
