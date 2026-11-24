# WP-3 검수 FAIL 고침 리포트 (app 워커 · 2026-11-20)

발주 `task_817730b96f16` · `ctx_bfe4469b644e` · 검수 `review-wp3.md`(P1 1 · P2 5) · 코디 판단(P1-1 · P2-1 · G1). 커밋 0 · 18222 손 안 댐(pid 64439 그대로) · 서버 띄움 0(실물 확인은 허브 18105 GET 만 · 프로세스 안).

## 1. 지적별 처리

| # | 지적 | 처리 | 시험 |
|---|---|---|---|
| **P1-1** | 허브 오류 하나가 목록 전체를 0 으로 만들고 D1 이 그 조건을 지움 | **코디 판단대로.** ① `detect.py`: 오류 난 **값**은 `None` 을 돌려 그 칸 합집합에서만 빠진다. 칸의 모든 값이 오류면 그 칸을 교집합에서 뺀다. 국가 칸도 같다. `Detector.errors` 에 턴 동안의 오류를 모은다. ② `turn.py` `_detect`: `decide` 뒤 `det.errors` 가 있으면 **그 턴은 주제 · 조건 칸 · 목록을 바꾸지 않는다**(decide 결과를 버림 · D1 거름 · 새 주제 판단 0 · `items` 조각 0). 장부는 `items{codes(앞 그대로), conditions(앞 그대로), hub_error: true, errors[], turn_conditions, name_hits, hub_calls}` · `consult.topic{…, change: false, hub_error: true}` · 주제 목록 · `active_topic` 은 앞 그대로다. 봇은 0.4 오류 처리 그대로다(축도 안 셈 → 0.2 빈 칸 질문) | `test_hub_error_drops_that_basis_only`(고민 오류 → 시술 칸만으로 `ZZ-BTX-A · B` · 교집합에서 그 칸 뺌) · `test_hub_error_one_value_of_slot`(값 하나만 오류 → 나머지 값으로) · **`test_p1_1_hub_error_turn_keeps_topic_conditions_and_list`**(가짜 CLI · 가짜 허브 두 턴: 1 턴 시술 → t1 2 개 · 2 턴 고민 + `concern_candidates` 500 → `items.hub_error` · 주제 · 지금 주제 · 조건 칸(고민 없음) · 목록 그대로 · `items` 이벤트 0) |
| **P2-1** | 주제 수 한도가 화면에만 걸림 | **코디 판단 = 화면 · LLM 블록 · 되돌림 대상 모두 한도 안 주제만**(장부 `consult.topics` 에는 전부 남음). `topics.visible_prev(topics, cur, max_n)`(지금 + 앞 max_n − 1 · 만든 차례 역순) 하나를 화면(`topics_view` 와 같은 자름) · 이해 호출 턴 메시지 주제 블록(`_topic_brief`) · 검증의 앞 주제 id(`_prev_topic_ids` — 한도 밖 `to` 는 null) · `decide` 의 규칙 되돌림 · TP11 같은 조건 찾기가 같이 쓴다 | `test_p2_1_return_targets_only_within_limit`(한도 2 · 앞 주제 t1 은 한도 밖 → LLM `to: t1` 도 대상 아님) |
| **P2-2** | 첫 턴 LS「all」 이면 빈 주제 t1 | 그 턴에 새로 만든 주제의 칸이 막아서 빈 채면 **주제를 만들지 않는다**(TP1 — 지금 주제 없음 · 목록 0 · LS3 · 장부 `blocked`) | `test_p2_2_first_turn_all_blocked_makes_no_topic` |
| **P2-3** | 0.4 T17 이 `modal.py` 한글로 실패 | WP-4 에서 「발생함」 상수를 `\u` 이스케이프로 고쳤다 → **`test_consult_page` 통과**. 이번에 고친 `detect.py` · `topics.py` · `turn.py` 도 코드 한글 0 확인 | `test_consult_page.py::test_t17` 통과 |
| **P2-4** | 국가 조건 첫 턴 허브 호출 상한 없음(최대 62) | 국가 셈을 **다른 칸 교집합 안의 진료항목 제품만** 묻도록 좁혔다(`country(want, among=others)`). 실물(허브 caa03560 · 빈 캐시): **「보톡스 국산으로」(C5) = 진료항목 57(같음) · 허브 호출 63 → 5**. 다른 칸 없이 국가만인 말(「국산으로」 만)은 여전히 제품 62 를 묻는다(첫 턴 · 캐시 뒤 0) | `test_country_asks_only_products_of_other_slots`(시술 칸 + KR → 그 시술 제품 둘만 물음) |
| **P2-5** | 스펙으로 옮길 것 | 코드 그대로 · 코디 몫: §5-1 ⑥ LS3 · C4 = D1 (가) · SF3 몸 조상 = 조상 전부(D2) · CZ1 = 이름 일치 밖 모든 값(D3) · SF1 부위 칸 = 이해 결과 site 대상(D4) · AX6 빠지는 턴도 한도까지 캐시 채움(X1) · 장부 `consult.ask_axis`(X2) · 주제 id `t<n>`(D8) · **새로**: §5-2 허브 오류 = 그 턴 주제 · 조건 · 목록 그대로 + `items.hub_error`(P1-1) · TP11 한도 = 화면 · LLM 블록 · 되돌림 대상(P2-1) · TP1 막혀 빈 첫 주제는 안 만듦(P2-2) · CD6 국가 셈 범위 = 다른 칸 교집합(P2-4) | — |

## 2. 덧붙임 — WP-4 G1(그림 자리) 코디 판단 반영

- `clinic_chat/config.py` `chat_image_dir` **기본 = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images`**(허브 레포 · 원리 55 · 방법 66 · 새 18 포함 · silver sha 121 / 121 같음 — WP-4 확인). 폴더가 없으면 그림 칸 숨김(IM2). 옛 시드 경로는 코드 · 설정 어디에도 없다.
- `.env.example` 설명 줄을 같은 자리로 바꿨다. 시험은 임시 폴더를 넘겨 기본과 무관하다. README 「상담 0.5」 절은 WP-7 에서 이 자리로 적는다. WP-4 리포트 §0 · §3 의 확인 경로가 이 자리다.

## 3. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/detect.py` | P1-1 값 오류 = `None`(칸 합집합에서만 빠짐 · 칸 전부 오류면 교집합에서 뺌 · 국가 칸 같음) · `Detector.errors` · P2-4 `country(…, among=)` |
| `clinic_chat/consult/topics.py` | `decide(…, max_n=)` · `visible_prev` · P2-2 빈 첫 주제 안 만듦 |
| `clinic_chat/consult/turn.py` | P1-1 허브 오류 턴 = 앞 상태 그대로 + `hub_error` · P2-1 `_topic_brief` · `_prev_topic_ids` · decide 에 한도 |
| `clinic_chat/config.py` · `.env.example` | G1 그림 자리 기본 |
| `tests/test_v05_detect.py` | 오류 시험 고침 + 새 6(값 하나 오류 · 국가 범위 · P2-1 · P2-2 · P1-1 끝까지) → **38** |

## 4. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_detect.py` | **38 passed** |
| v05 전부(detect · ask_axis · page · modal · images · kos_map) + 0.4 `test_consult_page`(T17) + WP-3 회귀 목록(`consult_turn` · `v04_list` · `consult_listing` · `consult_carry` · `state_carry` · `v04_prompt` · `v04_ledger` · `v04_verify` · `v04_understand` · `v04_turn` · `answer_key`) + `state_blanks` | **206 passed · 1 skipped** |
| `ruff check` · `ruff format` 손댄 py | 통과 |
