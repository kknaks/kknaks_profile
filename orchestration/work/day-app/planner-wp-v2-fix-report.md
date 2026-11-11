# planner-wp-v2-fix 결과 보고 — 리뷰 W1 + 참고 2건 최소 정정

## 상태: done (v2 미발행 · 새 계약/버전 3/승인 receipt/스펙/코드/GitHub 변경 없음)

- 수정 파일: `delivery-request-v2.json` 하나(제자리 수정 · contract_version 2 · 키 구조 · 항목 수 그대로 — acceptance 26 · review_surface 9 · dependencies 7). `planner-wp-v2-report.md` 는 옛판 보존(무수정).
- 수정 전 사본: scratchpad `v2-before-fix.json`(로컬 비교용).

## 수정 위치

| 지적 | JSON 경로 | 고친 것 |
|---|---|---|
| W1 | `$.execution.dependencies[1]` | 「A7 확인 필요 표시」 오기 삭제 → 영향 = A2(SPEC-003 A-22 need.why 조건) · A16(U-3 확인 필요 테두리 need.why = anes \| call) · A19(U-4 상세 머리 「확인 필요」) + A17 · A19 ⋮ · A20 그대로. 「옆 코드 카드엔 `needs[]` 만 · 카드 `need` 키 자체가 없음(a1c90b9d board_rules.py:621) — 배열로 바뀐 게 아니라 키가 사라짐」 명시 |
| W1 | `$.execution.dependencies[2]` | 회귀 칸을 「카드 need 키 없음 · needs[] 만 · lastMinutes 없음」으로 정확히 · 회귀가 걸리는 Acceptance = A2 · A16 · A17 · A19 |
| W1 | `$.review_surface[7]` ③ | 「need → needs[] 배열」 → 「needs[] 만 · 카드 need 키 없음」 · SPEC-003 쪽 사용처 = U-3 테두리(A16) · U-4 머리(A19) · A-22(A2) |
| W1 | `$.acceptance[16]` A16 | 회귀 조건 추가: 확인 필요 카드 테두리 빨강(서버 need.why = anes \| call · SPEC-003 U-3 · 줄 추가 없음). 옆 5상황 · needs[] 는 약속하지 않음(phase 1 정합 대상) |
| W1 | `$.acceptance[19]` A19 | 회귀 조건 추가: 상세 머리 「수납 필요」 · 「확인 필요」(+ need.why 별 마취/호출 · SPEC-003 U-4) |
| 참고1 | `$.review_surface[4]` | 「is_demo 제거」 → 「is_demo 동작 분기 제거(crm_connection.is_demo 칸은 유지 · 데모 병원 표시 데이터)」(옆 `_RESUME.md` §2 2026-11-09 행 :61) · 옆 Delivery #234 · #236 겹침 추적 · 이 앱 D-1 은 데모 이메일 목록 env 로 가르며 is_demo 를 쓰지 않음 |
| 참고2 | `$.acceptance[12]` A12 · `$.execution.predeploy[0]` | 둘을 같은 조건으로 맞춤: backend 전체 테스트 재발주 없음 · 옛 결과는 실행 기록. 재실행은 ① PR #237 backend 파일 변경 → v1 A12 backend 명령 ② rebase/merge 로 base dev 의 auth · 로그인 backend 가 바뀜(예 옆 세션 머지) → D-1 auth pytest 만. 그 밖 새 실행 없음 · 미실행 통합 검증 pending |

옆 계약(확인 필요 5상황 · needs[] · lastSeconds · 재호출 상시 · 취소 확인 창)은 새로 약속하지 않았다 — phase 1 정합 dependency 그대로.

## 검증 (1회)

- JSON 파싱 OK
- `jsonschema` Draft 2020-12 · `delivery-request.schema.json`(+ `delivery-issue.schema.json` execution ref) → **0 errors**
- `mediness_harness.workflow.DeliveryRequest.model_validate` → **OK**(contract_version 2 · L3 · acceptance 26)
- 「A7 확인 필요」 문구 잔존 0

## 남은 것

- 리뷰 참고 중 미수정(결함 아님 · 브리프 범위 밖): target_delta[11] 「< 시술현황 · {방}」 약식 표기(A19 가 정본) · A13 `0b776e90..HEAD` 는 rebase 시 merge-base 확인.
- 코디: plan(origin/main 재 fetch) → L3 새 plan_digest 사람 승인 → #235 apply. 앱 후속 구현은 사용자 지시 대기.
