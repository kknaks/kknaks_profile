# planner-local-alignment 결과 보고 — 로컬 DAY API 정합 (SPEC-003 개정 ② · WP v3 입력)

## 상태: done (커밋 · push · GitHub · CLI · 서버 · 로그인 · 실env 없음)

## 변경 파일

| 파일 | 변경 |
|---|---|
| `products/day/20-spec/spec-003-mobile-app.md` | +42 / −27 (HEAD `1551fa22` 위 미커밋). `status: stable` · `version: 0.0.1` · `last_updated: 2026-11-10` 유지(같은 날) · `sources` 에 옆 SPEC-002 `e421b77b…` · backend `a1c90b9d…` 추가 · 머리에 「2026-11-10 개정 ② — 로컬 DAY API 정합」 |
| `products/day/20-spec.md` | 변경 없음(SPEC-003 설명 · 날짜가 이미 맞음) |
| profile `delivery-request-v3.json` | v2 에서 최소 변경 · contract_version **3** |
| profile `planner-local-alignment-report.md` | 이 보고서 |

옆 SPEC-002 · SPEC-001 · 30-work · 코드 · 옆 세션은 읽기만.

## 정합표 (옆 원천 → SPEC-003 개정 ②)

원천: 옆 SPEC-002 = `day-procedure-board-2-spec` `e421b77b4bb836c7c557419dd3fad22db1900862`(미머지) · backend = `day-procedure-board-2` `a1c90b9dc63271dc06023ec0a530c53a216a296c`(미머지 · 사용자 로컬 day-local). dev `917287374723871d554f8a094610d46c39450534` 대비 스냅샷 키 diff 실측: **삭제** `need` · `overSec` · `lastMinutes` / **추가** `needs` · `canRecall` · `lastSeconds` · `waitMin` · `acceptMin` · `doctorName`(needs 안) · `visitDate`(chart 응답) · `card`(웹 인박스 내부).

| # | 옆 원천(file:line) | 2026-11-09/10 판 SPEC-003 | 개정 ② SPEC-003 | 자리 |
|---|---|---|---|---|
| ① | 스냅샷 `needs: [{why, since, limitMin, callId, doctorName}]` 5상황(SPEC-002 :503 · U-10 :235-251 · 규칙 16 :706-712 · 코드 board_rules.py:621 · 웹 원문 board_parts.html:213-217) | 카드 `need.why = anes \| call` | 카드 테두리 · 칩 = `needs[]` 있음 · 상세 머리 = needs 마다 원문 「대기/마취/호출 n분째」 · 「{doctorName} 수락 n분째」 · 「귀가 대기 전」 · 앱 판정 없음 | U-3 · U-4 · A-37 · 규칙 1 · OQ-A29 |
| ② | `tasks[].canRecall`(SPEC-002 :169 · U-5 · 규칙 6 :696 · 코드 :180-185 · :546) | [재호출] = `need.why = call`(5분) · called · edit | `canRecall = true` 줄 + `board` edit · 대상 call · 처음 대상 기본 선택 · API 그대로 · 권한 확대 없음 | U-4 · U-5 · A-22 |
| ③ | 취소 확인 창(SPEC-002 U-7 :208-211 · 웹 board_parts.html:114 · :117) | ⋮ 확인 없이 바로 | ⋮ 유지 → 「{시술} 시작을 취소할까요?」 · [시작 취소] · [닫기] / 「{시술} 완료를 취소할까요?」 · [완료 취소] · [닫기] · 폰 시트 · 아이패드 모달 · 토스트 [되돌리기] 없음 유지 | U-7 · A-31 · 케이스 매트릭스 · 프로토 차이표 |
| ④ | `anesthesia.lastSeconds`(SPEC-002 :503 · U-8 :219 · 코드 :607) · 회차 · 귀가 시 닫음(규칙 15 · 17 :716) | `lastMinutes` · 「마취 재시작」 | N = `lastSeconds ÷ 60` 내림(형식 변환만) · 사용자 확정 「N분」 유지 · 끝난 뒤 [마취 시작] = 새 회차 · 귀가 시 서버 닫음 수용 · `long` · `runningSince` · `limits.anesMin` 그대로 | U-3 · U-8 · A-29 |
| ⑤ | `pickable` = 준비중만(SPEC-002 :167 · 규칙 5 :695 · 코드 :173-178) | pickable 서버 값 | 그대로 소비 · 「지금 준비중만」 명시 · 시트 입력 조건 불변 | U-5 · A-32 |
| ⑥ | 담당 원장 바꾸기 `POST /api/tasks/{id}/doctor`(:443 · :725 · OQ-29 :796 · router :201) | 없음 | 넣지 않음 · 서버 검색 `/api/board/search` · 차트 `/api/visits/{id}/chart` 도 앱 1차 미사용 | §1 「뺌」 · §3 · A-38 · OQ-A30 |
| + | 새 오류 코드 `call_already_accepted` · `task_not_pickable`(SPEC-002 「오류 · 실패 토스트 글자」 :576-600) | 없음 | 그 표 원문 토스트 「다른 원장이 먼저 받았습니다」 · 「호출할 수 없는 시술이 있습니다」 | U-6 · U-13 · 케이스 매트릭스 · A-38 |
| + | 소비 원천 미머지 | — | 서버 의존 **D-6**(옆 SPEC PR #920 · backend #236 머지 전 · dev 서버는 옛 칸) | §4 서버 의존 |

- 경로 · 요청 본문 변경 없음(`/api/visits/{id}/calls` · `recall` · `accept` · `tasks/{id}/{action}` · `anesthesia` · `home` 동일 — router :150-227).
- UI 13항목 회귀 0: 4메뉴 · 머리 종/배지 없음 · 4필터 · 4행 카드 · 마취 한 줄 · 목록 수락 · 원장 즉시/간호 대리 · 상세 · 시트 · 모두 완료 · 통역 · TW · 성공 토스트 2.6초 문장 무변경(A-25 ~ A-36 은 A-29 · A-31 · A-32 만 소비 칸 수정).
- 업무 결정 변경 없음: 옆 SPEC-002 가 이미 정한 규칙 · 원문을 소비만. 새 판정 · 문구 · API 없음. 앱 적응 두 가지(카드 테두리 · 상세 머리 확인 필요, 웹 기능 미도입)는 OQ-A29 · A30 으로 리뷰 확인 대상에 올림.

## WP v3 (`delivery-request-v3.json`)

| 칸 | 값 |
|---|---|
| idempotency · product · root · targets | `day/day-app` · `day` · `products/day` · DAY-SPEC-003/001 (그대로) |
| contract_version · risk | **3**(#235 현재 v2 + 1) · L3 |
| baseline | `3f57c1af09afa7ce185cd754244c714bf1ec11e5`(로컬 origin/main · fetch 안 함 — 코디 plan 때 재확인) · pending |
| scope_delta | v2 plan_digest `sha256:7d361ed7…` → v3: 사용자 최신 지시 원문 · phase 1 대조 결과 ①~⑥ · 원천 sha · 보존 · app/ 만 · backend 수정 없음 |
| 바뀐 곳 | title · scope_delta · target_delta[1](v1 E22 표기 → v3 로 대체 표시) + [v3] 항목 1개 · acceptance A0(완료 정의) · A2 · A16 · A17 · A19 · A20 + **A26 신규** · non_goals[9] · [10] · review_surface[0] · [7] + 1개 · implementation_constraints[-1] · dependencies[1] · [2] · phases[1] · [3] · [4] · verification[0] · [4] · open_questions[0] · [2] |
| phase 1 구분 | 대조 = v3 에서 **완료**(SPEC-003 개정 ②) · 남은 것 = D-6 머지 · 로컬 day-local 연결 확인(통합 검증 · pending 가능 · 사용자 또는 명시 허용 앱 워커) |
| 항목 수 | target_delta 15 · acceptance 27 · non_goals 11 · review_surface 10 |

## 검증

- SPEC: `git diff --check` 통과 · `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` **0건**
- SPEC 잔존 검사: 옛 조건(`need.why` · `lastMinutes` · 「확인 창 없이」 · 「마취 재시작」 · E22) 은 「대체됨」 설명 문장 · D-6 사실 표기에만 남음
- v3 JSON: 파싱 OK · `jsonschema` Draft 2020-12(delivery-request + delivery-issue execution ref) **0 errors** · `mediness_harness.workflow.DeliveryRequest.model_validate` **OK**(v3 · L3)
- full SHA 6개 실제 rev 값(0b776e90 · 1551fa22 · 3f57c1af · 91728737 · a1c90b9d · e421b77b)

## 실물 검증 미실행

- localhost:11040 · day-local · 로그인 · 앱 실행 · 시뮬레이터 조작 없음(브리프 금지). 정합은 소스(SPEC-002 원문 · backend 코드 · 웹 템플릿) 정적 대조만.

## 미결 · 주의

1. SPEC-003 개정 ② 는 미커밋 — v3 원천 표기는 「1551fa22 + 개정 ②」. 코디가 커밋하면 그 exact head 로 PR #921 · v3 결속.
2. OQ-A29(앱 카드 테두리 · 상세 머리 확인 필요 — 웹은 카드 표시 없음)는 브리프 지시대로 기본값 유지 · 리뷰 확인 대상.
3. `lastSeconds` → 분 = 내림(옛 서버 `lastMinutes = int(minutes)` 와 같은 방식). 웹은 mm:ss.
4. dev 서버(91728737)는 옛 칸 — 옆 backend 머지 전 dev 에 붙이면 확인 필요 · 재호출 · 마취 완료가 비어 보일 수 있음(D-6 · 옛 칸 호환 분기는 새로 정하지 않음).
5. 다음: 독립 리뷰 → 코디 plan(L3 새 plan_digest · 사람 승인 — 현재 사용자 진행 지시와 결속은 코디 몫) → mobile 코드 발주.
