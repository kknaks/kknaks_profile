# 리뷰 리포트 — day-app 로컬 API 정합(SPEC-003 개정 ② · WP v3) / doc (2026-11-10)

- 대상:
  - 스펙 트리 `day-app-spec` HEAD `1551fa22` 위 미커밋 `products/day/20-spec/spec-003-mobile-app.md`(+42/−27 · `20-spec.md` 무변경)
  - profile `delivery-request-v3.json` · `planner-local-alignment-report.md`
- 원천:
  - `local-alignment-brief.md`(사용자 「응 작업 시작하자 ! 지금 테스트는 로컬 백엔드로 올렷어 !」)
  - SPEC-003 @1551fa22
  - `delivery-request-v2.json` · `delivery235-v2-verified.json`(#235 현재 v2 · plan_digest `7d361ed7…` · pending)
  - 옆 SPEC-002 @`e421b77b4bb836c7c557419dd3fad22db1900862`
  - 옆 코드 @`a1c90b9dc63271dc06023ec0a530c53a216a296c` — `board_rules.py` · `templates/partials/board_parts.html` · `templates/ui.html` · `routers/board.py`
  - 모두 read-only
- 방법: 원문 줄 직접 대조 · `git diff --check` · lint 1회 · JSON schema/model 검증 · v2 ↔ v3 경로 diff. 스펙 · JSON · 코드 · GitHub 수정 없음. 서버 · 로그인 · 실env 접근 없음.

## 판정: WARN (FAIL 0 · WARN 1)

6개 차이 중 소비에 필요한 5개(needs[] · canRecall · 취소 확인 창 · lastSeconds · pickable 준비중만)와 새 오류 코드 2개는 옆 SPEC-002 · 코드 원문과 글자 · 필드까지 일치한다. 앱이 새로 판정하는 곳, 새 문구 · API, 권한 확대, 담당 원장 바꾸기 · 검색 · 차트 같은 기능 추가는 없다. UI 13항목(A-25 ~ A-36은 A-29 · A-31 · A-32의 소비 칸만 바뀜) · 원장 즉시/간호 대리 · TW · 성공 토스트 2.6초 · 토스트 되돌리기 없음 · 4필터 · 4행 · 4메뉴 · 배지 서버 없음은 그대로다. SPEC-001 · D-1 · 세션 · 푸시 · 통역 서버 계약 절에도 무관 변경이 없다. WP v3는 #235 같은 키 · v2 + 1 · L3 · pending · app/만인 정합 갱신이며 범위 확대는 없다. WARN 1건은 새로 소비하는 `home` need가 사용자 확정 「모두 완료」 머리와 겹치는 자리의 표시 규칙이 비어 있다는 것이다.

## FAIL

없음.

## WARN

### W1. `needs[].why = home` 「귀가 대기 전」이 사용자 확정 상세 머리 「시술 모두 완료 · 귀가 대기 전」과 같은 때 같은 자리에 겹치는데, 표시 규칙이 없다
- 위치: `spec-003-mobile-app.md:207`(U-4 머리 — 「확인 필요」 + needs마다 … `home` 「귀가 대기 전」 · 그리고 「모든 시술이 완료된 카드면 머리 상태 글자 = 「시술 모두 완료 · 귀가 대기 전」」) · `:198`(U-3 카드 테두리) · A-33 · A-37 `:696`
- 원천:
  - 옆 SPEC-002 @e421b77b `:251` · 규칙 16 `:711`: `home` = [귀가 대기]가 켜졌는데(카드 시술 전부 완료) 누르지 않음 · **시간 기준 없이 바로**.
  - SPEC-003 U-4 5번 · U-9 · A-33: 사용자 2026-11-10 확정 — 모두 완료면 머리 「시술 모두 완료 · 귀가 대기 전」 + 강조 상자.
- 문제: 모든 시술이 끝나는 순간 서버가 `home` need를 바로 준다. 그래서 개정 ②대로면 상세 머리에 「확인 필요 · 귀가 대기 전」과 「시술 모두 완료 · 귀가 대기 전」이 함께 그려진다. 같은 순간 목록 카드는 테두리가 빨강이 되고 「확인 필요」 칩으로 들어간다(서버 `inbox_section` — 코드 `board_rules.py:466-470`). 업무 판정은 서버 값 그대로라 문제가 없다. 다만 사용자 확정 「모두 완료」 표시와 새 needs 표시가 한 머리에서 어떻게 공존하는지(둘 다 · 한쪽만)를 SPEC이 정하지 않았다. 앱 워커가 추측으로 메워야 하는 빈칸이다(rules.md 「워커가 추측으로 메워야 하는 빈칸」).
- 수정 방향(planner):
  - 새 글자나 판정은 짓지 않는다. OQ-A29(앱 적응 · 리뷰 확인) 기본값에 `home` need와 「시술 모두 완료 · 귀가 대기 전」의 관계를 한 줄 정한다. 예: 「둘 다 서버 · 사용자 원문 그대로 보이되 중복 허용」 또는 「모두 완료 상태 글자가 `home` need 글자를 대신함」 중 하나를 기본으로 두고 사용자 확인으로 남긴다.
  - 같은 순간 카드 테두리 빨강 · 「확인 필요」 칩 이동은 서버 `needs` · `inbox.section` 소비 결과라는 점을 U-3 · OQ-A29에 사실로 적는다.
  - 업무 규칙은 바꾸지 않는다.

## 소비 정합 대조 (원천 실측)

| 항목 | SPEC-003 개정 ② | 원천(read-only 실측) | 판정 |
|---|---|---|---|
| needs[] 5상황 | `:198` 테두리 = `needs[]` 있음 · `:207` 머리 「대기/마취/호출 n분째 · {doctorName} 수락 n분째 · 귀가 대기 전」 · n = since부터 분 · A-37 | `board_parts.html:213-217` 같은 글자 · `:201` 「n = since 부터 지금까지 분」 · `board_rules.py:432-450` `_need` {why, since, limitMin, callId, doctorName} · `:621` 카드에 `needs`만 · `:466-470` inbox `need` = needs 있음 | PASS(W1 표시 겹침만) |
| canRecall | `:212` · A-22 `:681` — `canRecall = true` 줄 + `board` edit · 대상 call · 처음 대상 기본 · API 그대로 · 재계산 없음 | `board_rules.py:180-185` = 귀가 대기 아님 · 줄 `called`(5분 조건 없음) · `:546` · router `recall` 경로 무변경(api/board.py:177) | PASS · 권한 확대 없음 |
| 취소 확인 창 | `:252` · A-31 · 매트릭스 「[닫기] = 요청 없음」 | `board_parts.html:113-117` 제목 「{t.title} 시작을/완료를 취소할까요?」 · 확인 「시작 취소」/「완료 취소」 · `ui.html:319-326` 버튼 「닫기」 · 옆 SPEC-002 U-7 `:208-211` | PASS · 문구 창작 없음 · 폰 시트/아이패드 모달은 기존 앱 적응 패턴 |
| lastSeconds | `:192` · `:258-261` · A-29 — N = `lastSeconds ÷ 60` 내림 · 사용자 확정 「N분」 유지 | 코드 `:607` `lastSeconds` · 옛 dev `lastMinutes = int(minutes(…))`(내림)과 같은 방식 · 업무 판정은 `long`(`:610` `> anes_min`) | PASS · 재계산 없음 |
| 반복 마취 · 귀가 때 닫힘 | `:261-262` [마취 시작] 새 회차 · 「마취 재시작」 글자 제거 | 옆 SPEC-002 U-8 `:216-220` · 규칙 15 · 17 | PASS |
| pickable | `:225` · A-32 서버 값 · 지금 준비중만 | `board_rules.py:173-178` | PASS |
| 새 오류 코드 | `:243` · `:311` · 매트릭스 · A-38 | 옆 SPEC-002 `:551` · `:587` · `:590` · 코드 `routers/board.py:104` · `:107` 같은 글자 · `board_rules.py:206` · `:249` | PASS |
| 새 기능 없음 | §1 「뺌」 `:76` · `:421` · OQ-A30 · A-38 「담당 원장 바꾸기 · 검색 · 차트 API 0건」 | 옆 router `:201` change_doctor 등 존재 — 앱은 부르지 않음 | PASS |
| 서버 의존 | D-6 `:645` — 두 원천 미머지 · dev 91728737은 옛 칸 · 선머지 gate 없음 | `a1c90b9d`는 로컬 origin/dev 조상 아님(앞 리뷰 실측) | PASS |

## UI 13항목 · 기존 계약 보존

- diff hunk가 닿은 곳: frontmatter `sources` · 머리 개정 ② · §1 뺌 · U-3 · U-4 · U-5 · U-6 거절 코드 · U-7 · U-8 · U-11 검색 문장 · U-13 실패 원천 · §3 소비 기준 bullet · 스냅샷 표 2행 · 매트릭스 3행 · 규칙 1 · 차이표 3행 · D-6 · A-22 · A-29 · A-31 · A-32 · A-37 · A-38 · OQ-A29 · A30 · OQ-A12 ⑦.
- 손대지 않은 곳: U-1 · U-2(4메뉴 · 머리 · 4필터) · U-10 · U-12 · U-13 성공 토스트 표 · U-14 · U-15 · U-16 · §3 세션 보관 · 연결 대상 검증 · 푸시 · 통역 · D-1 ~ D-5 · A-1 ~ A-21 · A-23 ~ A-28 · A-30 · A-33 ~ A-36 · OQ-A27/A28.
- 옛 조건(`need.why` · `lastMinutes` · 「확인 창 없이」 · 「마취 재시작」 · E22)은 모두 「대체됨」 설명 · D-6 · OQ-A12 사실 표기에만 남는다(grep). 본문 · 표 · A · OQ 사이 모순은 W1 밖에 없다.
- 4행 카드 · 4필터 · 4메뉴 · 원장 즉시/간호 대리 · TW · 토스트 2.6초/되돌리기 없음 · 배지 서버 없음 문장은 무변경이다. 성공 토스트 「시술 대기로 되돌림」/「시술 중으로 되돌림」은 확인 창 뒤 2xx에 그대로 적용된다.

## WP v3 (`delivery-request-v3.json`)

| 점검 | 결과 |
|---|---|
| JSON 파싱 · schema | `delivery-request.schema.json`(Draft 2020-12 · 같은 폴더 registry) **0 errors** |
| harness 모델 | `DeliveryRequest.model_validate` **OK**(contract_version 3 · L3) |
| 버전 | #235 현재 v2(`delivery235-v2-verified.json` `contract_version=2` · `plan_digest=sha256:7d361ed7…`) + 1 = 3 · scope_delta가 v2 digest `7d361ed7deb8…` 인용(일치) |
| 같은 키 · 범위 | idempotency `day/day-app` · product · root · target_specs · risk L3 · baseline `3f57c1af…` 동일 · code_surface(app/만) 무변경 |
| 경로 diff(v2 → v3) | 바뀐 리프 25개 + 추가 3개(acceptance[26] A26 · target_delta[14] · review_surface[9]). 나머지(완료 기반 v1 · UI 13 매핑 A14 ~ A25 · non_goals 0 ~ 8 · rollback · predeploy)는 동일 |
| 소비 정합 반영 | A2(canRecall) · A16(needs 테두리) · A17(lastSeconds · 회차) · A19(확인 창 · needs 머리) · A20(pickable) · A26(needs 글자 · 새 오류 코드 · 웹 API 0건) — SPEC-003 개정 ②와 일치 · 옛 조건과 새 조건을 동시에 약속한 곳 없음 |
| phase 1 구분 | `execution.phases[1]` · `dependencies[1]` = 대조 완료(개정 ②) · 남은 것 = D-6 머지 · 로컬 day-local 통합 검증(pending 가능 · 사용자 또는 명시 허용 워커) |
| 확대 여부 | non_goals[9] 웹 기능(원장 바꾸기 · 검색 · 차트 · 「마취중 mm:ss」 칩 · 확인 필요 목록 화면) 제외 · backend 수정 없음 · 옛 칸 호환 분기를 새로 정하지 않음(dependencies[2]) · 선머지 gate 없음 |
| 승인 | 승인 receipt 없음 · v2 승인을 v3 승인으로 주장한 곳 없음. L3 새 plan_digest 승인은 코디 몫(사용자 진행 지시와의 결속) |

## 검증 (실결과)

- `git diff --check` → 출력 없음 · exit 0(`spec-003-mobile-app.md` 하나 · `git status` M 1개)
- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분 · 무관)
- v3 JSON: 파싱 OK · schema **0 errors** · model **OK**(v3 · L3)

## 참고 (결함 아님)

- **원천 커밋 고정**: `review_surface[0]` · scope_delta는 SPEC-003 원천을 「1551fa22 + 개정 ② · 미커밋 — 코디가 커밋하면 그 exact head」로 적었다. CLI plan 전에 커밋해 exact SHA로 바꾸면 결속이 정확해진다(정직하게 표기돼 있어 결함은 아님).
- **실물 검증 칸**: A-31 · A-32(SPEC 실물 칸 「✓ dev」)와 v3 A2 통합 검증 「기존 dev 서버 · day-local」은 D-6 전 dev(91728737)에 `canRecall` · 준비중만 pickable이 없다는 점과 어긋난다. A-22 · A-29 · A-37처럼 「로컬 day-local(D-6 뒤 dev)」로 맞추면 일관된다.
- `acceptance[0]` 머리 「완료 정의(v2)」 · 「v2 완료 근거가 아니다」는 v3에서도 뜻이 통한다. 표기만 v2로 남아 있다.
- U-8 `:258` 「정확히 20분은 초과 아님」: a1c90b9d는 기준 분이 서버 설정(`limits.anesMin` · `:584` · `:610`)이다. 업무 판정은 `long` 소비라 영향은 없다.

## 남은 실제 의존

- planner: W1 OQ-A29 보강(필요 시 참고 2 · 3 표기).
- 코디: 개정 ② 커밋 → v3 plan(origin/main 재 fetch) → L3 새 plan_digest 사람 승인 → #235 apply → mobile 코드 발주.
- D-6: 옆 SPEC PR #920 · backend #236 머지 순서(사용자) · 그 전 dev 서버는 옛 칸.
- 로컬 day-local 통합 검증 · 실기기 · D-1 실물 · D-2 · D-3 · D-5 · 사용자 OQ(A8 · A21 · A27 · A28 · A29 · A30).
