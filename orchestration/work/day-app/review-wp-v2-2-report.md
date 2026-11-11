# 리뷰 리포트 — day-app WP v2 W1 + 참고 정정 재검수 / doc (2026-11-10)

- 대상: `delivery-request-v2.json`(planner 제자리 수정) · `planner-wp-v2-fix-report.md`
- 근거: 앞 리뷰 `review-wp-v2-report.md` W1 · 참고 · `wp-v2-fix-brief.md`
- 원천:
  - 옆 코드 `a1c90b9d board_rules.py:621`
  - 옆 `_RESUME.md` §2 :61
  - SPEC-003 @1551fa22 U-3 · U-4 · A-22
  - CENTURION_DAY day-app @0b776e90 `backend/tests/day/auth`
- 방법:
  - 앞 리뷰 때 평탄화해 둔 JSON 사본(scratchpad)과 지금 JSON을 경로 단위로 diff했다.
  - JSON 파싱을 한 번 했다. 전체 schema 검증은 지시대로 반복하지 않았다(planner 0 errors 보고).
  - 입력 JSON · 스펙 · 코드 · GitHub는 수정하지 않았다.

## 판정: PASS (FAIL 0 · WARN 0)

## 변경 범위 (경로 diff 실측)

- 바뀐 경로는 **8개뿐**이다: `$.acceptance[12]` · `[16]` · `[19]` · `$.review_surface[4]` · `[7]` · `$.execution.dependencies[1]` · `[2]` · `$.execution.predeploy[0]`. 나머지 104개 리프는 같다.
- 메타는 그대로다: `contract_version` 2 · `risk_level` L3 · `spec_baseline_revision` `3f57c1af…` · `idempotency_key` `day/day-app` · scope_delta 무변경.
- 항목 수도 그대로다: target_delta 14 · acceptance 26 · non_goals 11 · review_surface 9 · execution(dependencies 7 · phases 8 · verification 5 · predeploy 2 · rollback 4 · open_questions 3).
- 13항목 매핑(A2 · A14 ~ A25) · v1 회귀(A1 ~ A13) · 범위(app/만 · PR #237 하나 · D-2/D-3/D-5 밖) · non_goals는 문구째 같다. 회귀 0이다.

## W1 — 해소

| 확인 | 결과 |
|---|---|
| 「A7 확인 필요」 오기 | 문자열 잔존 0. `dependencies[1]` 영향 = A2(A-22 `need.why` 조건) · A16(U-3 테두리 `anes \| call`) · A19(U-4 머리 「확인 필요」) + A17 · A19 ⋮ · A20 |
| 「키가 없어짐」 사실 | `dependencies[1]` · `[2]` · `review_surface[7]` ③에 「카드 `needs[]`만 · 카드 `need` 키 자체가 없음(a1c90b9d :621)」이라고 적혀 있다. 원천 코드와 일치한다 |
| Acceptance 회귀 조건 | A16에 「확인 필요 카드 테두리 빨강(서버 need.why = anes \| call · SPEC-003 U-3 · 줄 추가 없음)」, A19에 「상세 머리 「수납 필요」 · 「확인 필요」(+ need.why 별 마취/호출 · SPEC-003 U-4)」가 추가됐다. 둘 다 SPEC-003 @1551fa22 기존 계약 문장과 일치하며 새 계약은 없다 |
| 옆 계약 약속 여부 | A16 「옆 5상황 · needs[]는 약속하지 않는다(phase 1 정합 대상)」. 재호출 상시 · 취소 확인 창 · lastSeconds도 Acceptance에 들어가지 않았다 |
| 회귀 연결 | `dependencies[2]` 「A2 · A16 · A17 · A19 회귀 조건으로 잡힘」. 이제 옆 backend가 먼저 머지되면 확인 필요 표시가 Acceptance에 걸린다 |

## 참고 2건 — 해소

| 확인 | 결과 |
|---|---|
| is_demo 사실 | `review_surface[4]` → 「is_demo 동작 분기 제거(crm_connection.is_demo 칸은 유지 · 데모 병원 표시 데이터로만)」. 옆 `_RESUME.md` §2 2026-11-09 행(:61)과 일치한다. 옆 Delivery #234 · #236 추적과 「D-1은 데모 이메일 env로 가르며 is_demo를 쓰지 않음」이 추가됐다(v1 target_delta[6]의 데모 계정 목록 env와 일치). 「is_demo 제거」 잔존 0 |
| A12 ↔ predeploy[0] | 둘이 같은 조건이 됐다: 옛 결과는 실행 기록이고 backend 전체 재발주는 없다. 재실행은 ① PR backend 파일 변경 → v1 A12 backend 명령, ② rebase/merge로 base dev의 auth · 로그인 backend가 바뀜 → D-1 auth pytest. 그 밖은 pending. 명령 경로 `backend/tests/day/auth`는 0b776e90에 실재한다 |

## 참고 (결함 아님 · 선택)

- A12 ②의 명령은 `-m "not infra"`라서 `backend/tests/day/auth`의 infra 표식 테스트(`test_environments_api.py` · `test_auth_api.py` · `test_web_login.py` — 「prod 행 미생성」 등 v1 A3 완료 근거 일부)는 다시 돌지 않는다. base auth가 바뀐 경우 A3의 infra 근거를 어떻게 다룰지 한 줄 덧붙이면 더 정확해진다. 「로컬 DB가 있으면 같은 폴더 infra도 실행, 없으면 그 부분 pending」 정도면 된다. 브리프의 「불필요한 전체 backend 재발주 금지」와 충돌하지 않는 범위다. 차단하지 않는다.
- 앞 리뷰의 나머지 참고(target_delta[11] 약식 표기 · A13 rebase 시 merge-base 확인)는 미수정이다. 이 역시 결함 아님 그대로다.

## 남은 것

- 코디: `start-delivery` plan(origin/main 재 fetch) → L3 새 plan_digest 사람 승인 → #235 apply(v2 미발행 상태). v1 승인 · evidence는 stale.
- SPEC PR #921 머지 전 spec-baseline:pending · 옆 세션 머지 순서 · phase 1 대조.
- 사용자 확인: SPEC-003 OQ-A8 · A21 · A27 · A28.
- 앱 후속 구현은 사용자 지시 대기.
