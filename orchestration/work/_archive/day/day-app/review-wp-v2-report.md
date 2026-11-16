# 리뷰 리포트 — day-app WP v2(Delivery #235 갱신 입력) / doc (2026-11-10)

- 대상: `delivery-request-v2.json`(planner 작성 · CLI 입력) · `planner-wp-v2-report.md`
- 대조 원천:
  - `wp-v2-brief.md`(현재 계약)
  - `delivery-request.json`(v1)
  - `delivery235-current.json`(현재 #235 · v1)
  - `_RESUME.md` §2
  - `review-ui-spec2-report.md`
  - SPEC-003 exact `1551fa22dfe23f36d6c3ebe443337225fc6277f1`(스펙 트리 HEAD · clean)
  - SPEC-001
  - latest `origin/main` `3f57c1af09afa7ce185cd754244c714bf1ec11e5`(로컬 ref)
  - 옆 세션 `day-procedure-board-2/_RESUME.md` · 옆 SPEC-002 @`e421b77b4bb836c7c557419dd3fad22db1900862` · 옆 코드 @`a1c90b9dc63271dc06023ec0a530c53a216a296c`(모두 read-only)
- 방법: JSON 파싱, 실제 schema 검증, harness 모델 검증, 원천 줄 대조. 코드 테스트 · 빌드 · lint는 반복하지 않았다. 입력 JSON · 스펙 · 코드 · GitHub는 수정하지 않았다. CLI plan · apply와 승인 receipt도 만들지 않았다.

## 판정: WARN (FAIL 0 · WARN 1)

WP v2는 #235의 누적 계약 version 2로 올바르게 짜여 있다. 사용자 UI 교정 13항목은 모두 Acceptance에 매핑됐다(A2 · A14 ~ A25). v1 로그인 · 세션 · SSE · 푸시 · 통역 클라이언트 계약은 회귀 대상으로 보존됐다. 옛 수치(155 · 47 · 663)는 「옛 head 실행 기록」으로만 적혀 있고 새 UI 완료로 쓰지 않았다(`$.acceptance[0]` · `[12]`). 이번 후속 변경은 app/만이고 코드 PR #237 하나 · 사용자 지시 머지 원칙이 유지된다. D-2 · D-3 · D-5는 범위 밖이다. 새 문구 · 번역 · API 발명은 없다. 옆 세션 차이는 숨기지 않았고 phase 1 대조로 남겼으며, 업무 동작을 WP에서 덮어쓰지 않았다. WARN 1건은 옆 코드 실물이 카드 `need`를 **없애는** 영향 범위를 dependency가 일부 잘못 짚은 것이다.

## FAIL

없음.

## WARN

### W1. 옆 세션 「need → needs[]」 영향 범위를 잘못 짚었고, 「확인 필요」 표시가 Acceptance에 매달리지 않는다
- 위치: `$.execution.dependencies[1]` 영향 목록(「… A7 확인 필요 표시 …」) · `$.review_surface[7]` ③ · `$.acceptance[16]`(A16) · `$.acceptance[19]`(A19)
- 근거:
  - **옆 코드 사실**: `a1c90b9d backend/day/services/board_rules.py:621`은 카드에 `"needs": [...]`만 싣는다. 카드 단위 `need` 키는 card_view에서 사라졌다(`origin/dev 91728737`의 `need` · `need.overSec`는 a1c90b9d 키 목록에 없음). 그래서 「배열로 바뀜」이 아니라 「앱이 읽는 `need`가 없어짐」이다.
  - **SPEC-003 @1551fa22가 `need`를 쓰는 자리**: U-3 「확인 필요 카드 테두리 빨강 · `need.why = anes | call`」 · U-4 머리 「확인 필요(+ `need.why` 별 마취 / 호출)」 · A-22 [재호출] 조건.
  - **WP 쪽 문제**: dependency는 이 영향을 「A7 확인 필요 표시」로 적었다. 그런데 v2 A7(`$.acceptance[7]`)은 SSE · 오프라인 · 이중 탭 · KOS 반영 조건이고 「확인 필요」 표시가 없다. A16(카드 4행) · A19(룸 상세)에도 확인 필요 테두리 · 머리 표시가 없다. 그래서 옆 backend가 dev에 먼저 머지돼 이 표시가 깨져도 걸어 줄 Acceptance ID가 없다(A2의 재호출만 걸림).
- 수정 방향(planner):
  1. dependencies[1] · review_surface[7] ③에 영향 자리를 정확히 적는다 — SPEC-003 U-3 확인 필요 테두리 · U-4 머리 「확인 필요」 · A2(A-22 재호출) · 「`need` 키 부재(a1c90b9d :621)」. 「A7」 표기는 고친다.
  2. 확인 필요 테두리 · 머리 표시는 새 계약이 아니라 SPEC-003 U-3 · U-4 기존 계약이다. A16 · A19의 회귀 문구에 「확인 필요 테두리(`need.why` anes|call) · 상세 머리 확인 필요 표시 유지(SPEC-003 U-3 · U-4)」를 붙이거나, v1 회귀 항목으로 명시한다.
  - 옆 동작(5상황 · needs)을 Acceptance로 약속하지는 않는다(지금 WP 원칙 유지).

## 13항목 커버 표 (SPEC-003 @1551fa22 Acceptance ID 대조 · 모두 실재)

| # | 사용자 확정 | v2 Acceptance(JSON 경로) | SPEC-003 | 판정 |
|---|---|---|---|---|
| 1 | 하단 4메뉴 · 「곧 출시 예정」 · 5번째 탭 없음 · 인박스 탭 구분 | A14 `$.acceptance[14]` · A8 `[8]` | A-25 · A-13 | PASS |
| 2 | 머리 DAY · 종 · 배지 D-5 전 없음 · 설정 = 계정 | A15 `[15]` · non_goals[8] | A-26 · A-27 · OQ-A19 | PASS |
| 3 | 필터 4개 · `inbox.section` | A14 `[14]` | U-2 · OQ-A2 | PASS |
| 4 | 4행 카드(기타 = gender 기본 · isNew 없음) | A16 `[16]` | A-28 · OQ-A27 | PASS(W1 보완) |
| 5 | 마취 한 줄 · `long` 빨강 · 마취 완료 {N}분 | A17 `[17]` | A-29 | PASS |
| 6 | 목록 카드 호출 상태 · 카드에서 수락 · 상세 강조 상자 | A18 `[18]` · A19 `[19]` | A-30 · A-31 | PASS |
| 7 | 원장 즉시 본인 · 간호 등 드로어 대리 · 3곳 공통 · 다른 원장 지정 호출 = 현 서버 성공 · 새 차단 없음 | A2 `[2]` · non_goals[5] | A-2 · OQ-A28 | PASS |
| 8 | 상세 머리 · 메모 여백 · 시술 카드 · 완료 아래 회색 · 세로 ⋮ 확인 없음 | A19 `[19]` | A-31 · U-7 | PASS |
| 9 | 상시 체크박스 없음 · 시트(시술 + 원장) · 마법사 없음 · 재호출 A-22 | A20 `[20]` · A2 | A-32 · A-22 | PASS |
| 10 | 모두 완료 상자 · 마지막 종료 · canHome · 표시 ≠ 업무 상태 | A21 `[21]` | A-33 | PASS |
| 11 | 원형 통역 드로어 · 둥근 칩 · 4메뉴 유지 | A22 `[22]` | A-36 | PASS |
| 12 | TW → zh-Hant 「중국어(번체)」 · 같은 언어 · 덮지 않음 · HK/VN 미확정 en · vi/yue 칩 없음 | A23 `[23]` · non_goals[5] | A-35 · OQ-A9 · OQ-A26 | PASS |
| 13 | 성공 토스트 원문 · 2.6초 · 덮어쓰기 · 되돌리기 없음 · 본인 조작만 · 재호출 토스트 없음 · 실패 DAY 글자 | A24 `[24]` | A-34 · OQ-A25 | PASS |
| — | 시각 검수(원본 프로토 read-only) | A25 `[25]` | — | PASS(리뷰어 기기 조작 없음 명시) |

## 계약 · 메타 점검

| 점검 | 결과 |
|---|---|
| JSON 파싱 | OK(최상위 15키 · target_delta 14 · acceptance 26 · non_goals 11 · review_surface 9 · execution 8칸) |
| 실제 schema | `tools/harness/src/mediness_harness/schemas/delivery-request.schema.json`(`mediness://delivery-request/v2` · Draft 2020-12 · 같은 폴더 schema 전체를 registry로) → **0 errors** |
| harness 모델 | `mediness_harness.workflow.DeliveryRequest.model_validate` → **OK**(contract_version 2 · L3) |
| idempotency · 제품 · root · target_specs | v1과 같음(`day/day-app` · `day` · `products/day` · `DAY-SPEC-003`/`DAY-SPEC-001`) |
| contract_version | 2 = 현재 #235 hidden meta `contract_version=1` + 1(harness `workflow.py` 「Scope Delta must increment … by exactly one」 충족) |
| scope_delta | 있음 · v1 plan_digest `c4f70ae3…` · contract digest `f3d03f99…`는 #235 스냅샷과 일치 · 바뀐 계약 · 보존 계약 · app/만 · L3 · pending 명시 |
| spec_baseline_revision | `3f57c1af…` = 로컬 `origin/main`(harness: 계약이 바뀌면 fetch한 origin/main과 같아야 함 — 코디 plan 때 fetch로 재확인). main에는 SPEC-003이 없고 SPEC-001은 `status: draft`(git show 확인) → pending 정직. 1551fa22를 ready로 위장한 곳 없음 |
| risk | L3 유지(D-1 누적 근거 · `$.scope_delta`) |
| full SHA | 0b776e90 · 1551fa22 · 3f57c1af · 91728737 · a1c90b9d · e421b77b — 40자 값 모두 실제 rev와 일치 |
| 승인 | 승인 receipt · 「승인됨」 주장 없음. `$.review_surface[5]`가 v1 승인 · evidence가 v2 digest에 대해 stale임을 명시. 현재 #235 라벨 `delivery-plan:approved`는 v1 것이다 — apply 뒤 L3 새 plan_digest에는 사람 승인이 필요하다(코디 몫) |
| 범위 | 후속 변경 app/만(`$.execution.code_surface` · A13 · non_goals[4]) · D-1 재작업 없음 · 새 backend/웹/배포 수정 없음 · PR #237 하나 · 머지는 사용자 지시(constraints[4]) · 문서 선머지 게이트 없음(dependencies[0]) |
| 범위 밖 | D-2 · D-3 · D-5 · Apple/서명/키 · 옆 세션 기능(non_goals 0 · 1 · 2 · 8 · 9) |
| OQ 보류 | UI 기본값 진행(A8 · A18 ~ A28)과 정책/문구 보류(A1 · A9 남은 것 · A11 · 문구 OQ)를 구분해 SPEC 구분과 일치(`$.execution.open_questions`). 새 질문 · 승인 단계 없음 |
| 과도한 gate | 없음 — phase 1 대조는 업무 동작 항목 앞에만 있고, 순수 UI는 기다리지 않는다(`$.execution.phases[1]`) |

## 기존(v1) 회귀 보존

- v1 target_delta 8개는 「[v1 · 완료된 기반 · 회귀 대상 — PR #237 head 0b776e90]」로 보존됐다(`$.target_delta[0..7]`).
- v1 A1 · A3 ~ A7 · A9 ~ A11은 원문 유지, A2 · A8 · A12 · A13은 개정이다. v1 acceptance 14개 → v2 26개(완료 정의 + A1 ~ A25).
- 환경 연결 · 정규화 · 세션 묶음 · SSE · 푸시 등록 · 통역 WS 클라이언트 · 비밀 검사(A3 ~ A11)는 SPEC-003 A-3 ~ A-24와 대응하며 v1과 같은 뜻이다.
- non_goals v1 8개 중 v2와 충돌하던 3개(국적 자동 언어 · 예약/설정 탭 · backend 변경)를 v2 확정분과 맞게 좁혔다. Acceptance와 충돌 0건(직접 대조).

## 옆 세션 정합 의존 목록 (원천 줄 직접 확인 · 판단은 하지 않음)

| # | 옆 SPEC-002 @e421b77b / 코드 @a1c90b9d | SPEC-003 @1551fa22 | WP 처리 | 확인 |
|---|---|---|---|---|
| ① | [재호출] 호출 줄에 늘(SPEC :169) · `canRecall`(코드 :180 · :546) | A-22 `need.why = call` 조건 | A2는 A-22만 약속 · phase 1 | 줄 일치 |
| ② | 시작/완료 취소 확인 창(:208 · :319-320 · :735) | U-7 확인 없이 | A19는 확인 없음만 약속 · phase 1 | 줄 일치 |
| ③ | 확인 필요 5상황(:235 · :251 · :710-711) · 카드 `needs[]`만(코드 :621 · `need` 키 없음) | `need.why` anes/call | phase 1 · dependency[2] | 줄 일치 · **영향 범위 W1** |
| ④ | 「마취 완료 mm:ss」(:219) · `lastSeconds`(SPEC :503 · 코드 :607 · `lastMinutes` 없음) | A-29 {N}분 · `lastMinutes` | A17 SPEC-003 기준만 · dependency[2] | 줄 일치 |
| ⑤ | pickable = 준비중만(:167 · 코드 :173-178) | pickable 서버 값 | A20 서버 값 소비 | 줄 일치 |
| ⑥ | 담당 원장 바꾸기 API · 알림(:443 · :725 · OQ-29 :796 · router :201) | 없음 | non_goals[9] | 줄 일치 |

- 추가로 관찰한 키 차이(참고 · WP 수정 필수 아님): 옆 코드 `limits`에 `waitMin` · `acceptMin` 추가, `anes_min`이 설정값(:584 · :610)이다. 앱은 `limits.anesMin` · `long`을 소비하므로 SPEC-003 계약상 영향은 없다.
- 옆 코드 `a1c90b9d`는 로컬 `origin/dev`(91728737)의 조상이 아니다(미머지). 머지 상태 · 순서는 추측하지 않는다(WP dependencies[2]와 같은 입장).

## 참고 (결함 아님)

- `$.review_surface[4]` 「is_demo 제거」는 옆 세션 2026-11-09 결정(「`crm_connection.is_demo` 칸은 지우지 않는다 · 동작 분기만 제거」, 옆 `_RESUME.md` §2)과 표현이 어긋난다. 「is_demo 동작 분기 제거(칸은 유지)」로 다듬으면 정확하다. 옆 Delivery #234 · #236(approved · #920 머지 뒤 재결속)도 같이 적으면 겹침 추적이 쉬워진다.
- `$.execution.predeploy[0]` 「머지 전 D-1 pytest로 확인」과 A12 「backend 변경 없으면 새 실행 대상 아님」 사이에 긴장이 있다. backend 파일이 같으면 옛 결과로 갈음된다는 뜻으로 읽힌다. 다만 dev 기준이 옆 backend 머지로 바뀌면 다시 돌려야 한다는 조건을 한 줄 붙이면 명확해진다.
- `$.target_delta[11]` 「< 시술현황 · {방}」은 SPEC U-4(왼쪽 뒤로 · 오른쪽 방 이름) · A19 표기와 모양이 다르다(SPEC S-7과 같은 약식). Acceptance A19가 정본 표기라 문제는 없다.
- A13 경로 검사 `0b776e90..HEAD`는 PR을 rebase하면 범위가 깨질 수 있다. 실행 때 merge-base를 확인한다.

## 남은 실제 의존

- 코디: `start-delivery` plan(origin/main 재 fetch) → L3 새 plan_digest 사람 승인 → #235 apply. v1 승인 · evidence는 stale.
- SPEC PR #921(1551fa22) main 머지 전까지 spec-baseline:pending · 머지 뒤 재결속.
- 옆 세션 SPEC-002/backend 머지 순서(사용자) · phase 1 대조.
- D-1 실물(prod 배포 · env) · D-2 · D-3 · D-5 서버 · Apple/서명/키(사용자).
- 사용자 확인 대상: SPEC-003 OQ-A8 · A21 · A27 · A28.
- 앱 후속 구현 착수는 이번 범위가 아니다(사용자 지시 대기).
