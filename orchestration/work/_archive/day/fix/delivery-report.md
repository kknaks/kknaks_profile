# fix Delivery 발행 · 승인 기록 결과

## 상태: done

| 항목 | 값 |
|---|---|
| Issue | **#241** — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/241 (OPEN) |
| 제목 | DAY 직원 앱 실기기 피드백 반영 · 통역 서버 — 시술현황 카드 모두 완료 · [귀가 대기] · 확인 필요 표시 · 채팅 403 · 그룹 이름 바꾸기 · 채팅 전체 알림 · WS /api/interpret (DAY-SPEC-003 · 004 · 005 · 000) |
| idempotency key | `day/fix-device-feedback-interpret` · contract_version 1 |
| 라벨(지금) | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` |
| risk_level | **L3** |
| contract_digest | `sha256:f082f01987f447e1a70272694d96f124d9b48d955e6e16f89f449b1728671e99` |
| plan_digest | `sha256:b3ab2b847d281a909fb5f0536a1bf9178f43355c797fbfca20dc36b464848cf1` |
| baseline | `pending` · revision = mediness `origin/main` `0d69a207c276147b933f6d71ba2043b1433cf9c6` · CLI `missing_target_specs = [DAY-SPEC-000]`(main 에서 draft) |
| 승인 | **적용함** — receipt `{decision: approved, reviewer_type: human, reviewer: kknaksss, plan_digest: sha256:b3ab…48cf1}` · `--plan` 으로 digest 같음 확인 뒤 `--apply` → status `plan-approved` |
| next_action | `prepare-spec-baseline`(human_gate false · when `stable-spec-ready`) — 스펙 PR(`kknaksss/fix-spec`) 머지 뒤 같은 key · version 2 · 새 `origin/main` revision 으로 재결속 |
| task_projection | `pending`(MCP `mediness.task_draft_request` 미호출 — 브리프대로 MCP 승인 카드는 처리하지 않음) · CLI `partial: true` 는 이 Task projection 이 남았다는 뜻 |

## 한 일

1. `start-delivery` Skill · `rules/delivery-workflow.md` · `tools/harness/references/requests.md` 대로 request 작성 → `mediness start-delivery --mediness-repo <fix-spec> --code-repo CENTURION_DAY/fix --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`(#241 생성 · `delivery-plan:review`).
2. 결과 계약 대조: Target Delta 7줄 = `wp-plan.md` WP 4개(BE-1 · BE-2 · APP-1 · APP-2)와 스펙 개정(SPEC-003 ⑧ · ⑨ · SPEC-004 · 005 · 000 2026-11-11)과 같은 범위 — 계획 밖 항목 없음. Non-Goals = 스펙 OQ 기본값(기록 없음 · 병원별 사전 없음 · 재확인 없음 · 수명 상한 없음 · 시스템 줄 없음 · 앱 통역 무수정) · migration 없음 · prod 배포 없음 · 2차 Delivery 손대지 않음 · #240 범위 밖. CLI 가 붙인 추가 조건은 없음(L3 도 담당자 한 명 승인 gate 하나) → 승인 receipt 적용.
3. Acceptance 8줄에 누구 몫인지 표시(A1 ~ A6 구현 워커 · A5 실제 Soniox · A6 로컬 키 비움 · A7 사용자 실기기 · A8 코디).
4. Execution(ready): code surface(WP 별 파일) · dependencies(스펙 PR 머지 · BE-1 → APP-2 로컬 · Soniox dev 키 · TestFlight 다음 빌드) · phases(WP 4개) · verification(pytest · test.sh · ruff · flutter analyze/test · live check · 실기기) · predeploy · rollback(revert · migration 없음 · 선택 비밀 비우면 통역만 꺼짐) · open questions(OQ-A43 · A46 · I-1 ~ I-5).

## risk L3 근거 (Review Surface 에 적음)

새 외부 서비스 연동(Soniox 실시간 STT · TTS — 고객 발화 음성을 외부로 보냄) · 새 선택 비밀 · 새 공개 API 2개(#22 · WS) · 새 의존성 · 깨진 시드 = api 기동 실패. migration 없음. 레포 규칙(`rules/delivery-workflow.md` 「L3 = destructive · production · external write · …」)과 2차 Delivery(#239 L3)와 같은 분류.

## SPEC-000 draft 에 대해

막히지 않았다 — CLI 가 DAY-SPEC-000 을 stable 이 아닌 target 으로 보고(`missing_target_specs`) baseline 을 `pending` 으로 둔다(규칙대로 · 우회 없음). 다만 **재결속(ready)하려면 스펙 PR 머지 때 SPEC-000 이 stable 이어야 할 수 있다** — 2차 Delivery #234 · #239 도 같은 SPEC-000 을 target 으로 pending 이라 함께 정할 일(SPEC-000 `draft → stable` 은 사람 판단).

## 파일

- request: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-spec/61d7eb92-2114-46d5-8714-6da5e5f849de/scratchpad/delivery/fix.v1.request.json`
- 결과: 같은 폴더 `fix.v1.plan.json` · `fix.v1.apply.json` · `fix.v1.approval-receipt.json` · `fix.v1.approve.plan.json` · `fix.v1.approve.apply.json`
- 레포 · 스펙 · 코드 파일 수정 0 · 커밋 · push · PR 0 · 2차 Delivery(#234 · #235 · #236 · #239) 변경 0.
