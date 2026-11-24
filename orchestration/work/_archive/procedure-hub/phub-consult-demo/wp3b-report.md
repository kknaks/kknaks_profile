# WP-3 고침(D1) + WP-3b 다음 질문 축 리포트 (app 워커 · 2026-11-20)

발주 `task_606c48f51e93` · `ctx_f9d1a2a76628` · SPEC-010 0.2.7 §5-0b · §5-1 ⑥ · §5-4 AX1 ~ AX7 · §13 WP-3b. 기준은 `$J` 1af2216c · 허브 caa03560(GET 만)이다. 커밋 0 · push 0 · 18222 손 안 댐(pid 64439 그대로) · 실물 서버 18297(끝에 내림).

## 1. D1 고침 — 코디 판단 (가)

| 무엇 | 내용 |
|---|---|
| 코드 | `topics.decide` LS 갈래: 막은 칸 값을 **주제 조건 칸에서 뺀다**. 칸 = 막은 칸을 이번 턴 앞 값으로 되돌린 조건(LS2 가 찾은 `trial`)이다. 다 빼도 0(blocked all)이면 이번 턴 조건을 하나도 남기지 않는다(앞 칸 그대로). 막은 값은 장부 `items.blocked{slot, values, without_n}` 에만 남는다. 목록 규칙(LS1 앞 목록 그대로 · LS3 막은 칸 뺀 결과)은 그대로다 |
| **스펙과 다른 점(코디가 스펙에 옮김)** | §5-1 ⑥ LS3 「막은 칸 값은 칸에 남는다」 · C4 「제품 칸 값은 남음」 → **「막은 칸 값은 주제 칸에서 빼고 장부 `blocked` 에만 남긴다(다음 턴 A 셈에 끼지 않음)」**. LS1 에서도 같다(칸에서 빠짐 · 목록은 앞 것 그대로) |
| 시험 | `test_d1_blocked_value_leaves_topic_so_next_turn_narrows`(실물 wp3real000000001 꼴 — 「볼 꺼짐 때문에 필러」 고민 0 → LS3 · 고민 빠짐 · 6 → 「쥬비덤으로」 같은 주제 안 좁힘 1 · A 1) · C4 시험 단언을 고침(제품 칸 빔 · `blocked.values` = 써마지) |
| 실물 확인 | `wp3breal00000001`: 1 턴 「볼 꺼짐 때문에 필러 맞고 싶어요」 → 이해 호출 = 고민 볼 꺼짐(CON-057) · 필러 M2 · 볼 SITE-051 → A = B = 0 → **LS3 · blocked 고민 「볼 꺼짐」 · 주제 t1 = [필러 · 볼] 6**. 2 턴 「쥬비덤으로 할래요」 → **A 1 · rule continue · used continue · t1 = [필러 · 볼 · 쥬비덤] 1**(전에는 자동 새 주제 t2 였음). 덤: `wp3breal00000002` 「팔자주름이 고민이에요」 는 이해 호출이 부위 SITE-046(팔자주름)도 냈다 → 고민 ∩ 부위 0 → LS3 · 부위가 칸에서 빠지고 고민만으로 23 |

## 2. WP-3b — 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/ask_axis.py`(새) | **`pick`(순수)**: AX1(L ≤ `CHAT_ASK_LIST_MIN` 이면 축 0) · AX2(값 있는 칸 · AX6 로 빠진 축 제외 · 회차 `count` · 대상 `target` 축 자리 — 값은 WP-5 장바구니가 넣음) · AX4(점수 = 가장 큰 묶음 · 묶음 < 2 · 「없음」 > L/2 · 가장 큰 묶음 = L(N14) 빼기 · 동점 부위 → 고민 → 효과 → 제품 → 대상 → 회차) · AX5(앞 5 · 동점 = groups 처음 나온 순 · 이름). **`axis_values`**: 부위 = `level2`(얼굴 · 몸 바로 아래 · 얼굴 · 전신 · 몸은 그대로) · 고민 = 케이스 `facets indication` role 「자기」 · reach 「케이스 직접」 · 효과 = 케이스 `facets outcome` 의 `effect_code` 있는 줄만(N3) · 제품 = scope 「상위 제품」 으로 끝까지 올림(N9) · 프로세스 캐시 (gold_hash, 노드, facet) · **AX6**: 고민 · 효과에 새 호출이 40 을 넘으면 두 축을 빼고 `skipped_axes` · **빠지는 턴에도 한도(40)까지 캐시를 채워 다음 턴에 셈** |
| `clinic_chat/consult/turn.py` | `_detect` 끝에 `_axis`(지금 주제 목록 · 지금 주제 칸 = 값 있는 축 · TP9). 축이 있으면 **0.2 빈 칸 질문 대신 축 질문 하나**: `ask = None` · `ask_why = "axis"` · `close.by = "ask"` · LLM 「앱 판정」 의 `ask` = `{slot: "axis:<축>", options: [이름 …]}`(선택지는 이 값만 · 0.2 `ask` 꼴). 장부 `consult.ask_axis{axis, options[{value, name, n}], scores, excluded, skipped_axes, hub_calls}` · 축 셈이 깨지면 0.2 그대로(기록만) |
| `clinic_chat/consult/topics.py` | D1(위) |
| `clinic_chat/consult/items_view.py` | 주제 머리 이름을 한 번씩(실물 LDM 머리가 「LDM · LDM」 이던 것 — 제품 이름 = 이름 일치 이름) |
| `tests/test_v05_ask_axis.py`(새) | 13 시험 |
| `tests/test_v05_detect.py` | D1 시험 · C4 단언 · 머리 이름 한 번 시험(31 → 33) |

## 3. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_ask_axis.py` | **13 passed** — AX1(4 이하 0 · 5 부터) · AX4 빼기 셋(groups_lt2 · none_over_half · all) + 점수 · 동점 순서 · 값 있는 칸 제외 · skipped · AX5 앞 5 · 동점 groups 순 · 이름 · **AX7 표본 셋**(① 팔자주름 23 → 제품 5 · 부위 · 효과 「all」 · 선택지 PRD-435 · 402 · 400 · 150 · 416 ② 보톡스 106 → 부위 21 · 제품 33 · 고민 · 효과 skipped ③ L 3 → 축 0) · `level2` · `axis_values`(자기 · 케이스 직접만 · 빈 경과 줄 뺌 · 상위 제품 · 이름 · 호출 수 · 캐시) · AX6 한도(빠짐 + 캐시 채움 → 다음 턴 셈) · 한 턴(축 → `close.by ask` · `ask_why axis` · 장부) · 목록 작으면 축 0 |
| `tests/test_v05_detect.py` | **33 passed** |
| 위 + WP-3 회귀 목록 · 0.4 화면 · 장부 · 프롬프트(`test_consult_page` T17 포함) | 145 passed + 96 passed(1 skipped) · 마지막 묶음 76 passed |
| `ruff check` · `ruff format` 손댄 파일 | 통과 |

- 걸렸다 고친 것: 0.4 T17(코드 한글 0)이 `ask_axis.py` 상수 셋을 잡음 → `\u` 이스케이프.

## 4. 실물 표(빈 포트 18297 · 실제 이해 호출 · 허브 caa03560)

| 말 | 목록 L | 고른 축 · 점수 | 다른 축 점수 · 빠짐 | 선택지(이름 · 수) | 허브 호출 | 스펙 AX7 |
|---|---|---|---|---|---|---|
| 팔자주름이 고민이에요 | 23 | **제품 · 5** | 부위 23 · 효과 23(둘 다 「all」) · 고민 칸 참 | 소프웨이브 5 · 슈링크 5 · 울쎄라 5 · 리쥬란 4 · 써마지 3 | 24 | 제품 5 ✓(선택지 = PRD-435 · 402 · 400 · 150 · 416 의 이름) |
| 보톡스 받고 싶어요(1 턴) | 106 | **부위 · 21** | 제품 33 · **고민 · 효과 skipped**(AX6) | 턱 21 · 얼굴 16 · 입 12 · 다리 8 · 코 8 | 44(40 은 캐시 채움) | 부위 21 ✓ · 첫 턴 빠짐 표지 ✓ |
| 보톡스 어떤 게 있어요?(같은 대화 2 턴) | 106 | **부위 · 21** | 고민 71 · 효과 106(「all」) · 제품 33 · 빠짐 0 | 같음 | 8 | WP-0 실측 고민 71 · 효과 106 과 같음 |
| LDM 받고 싶어요 | 1 | **축 0**(list_small) | — | — | 0 | 축 0 ✓(L 은 3 이 아니라 1 — 이해 호출이 제품 LDM 을 내고 이름 일치와 교집합) |
| 볼 꺼짐 때문에 필러(D1 대화 1 턴) | 6 | 제품 · 2 | 고민 6 · 효과 6(「all」) | 레스틸렌 2 · 벨로테로 1 · 셀레스텔라 1 · 쥬비덤 1 | 7 | — |

- 축이 있는 턴은 장부 `close.by = ask` · `ask_why = axis` 이다. 봇 답 끝 질문이 그 축 선택지로 나간다(문장은 LLM).

## 5. 스펙과 다른 점 · 남은 것

| # | 무엇 | 제안 |
|---|---|---|
| D1 | 위 §1 — LS 막은 칸 값은 주제 칸에서 뺌(장부 `blocked` 에만) | 스펙 §5-1 ⑥ LS3 · C4 문구 고침(코디) |
| X1 | AX6 — 빠지는 턴에도 한도(40)까지 캐시를 채운다(안 그러면 「보톡스」 는 매 턴 빠짐) | AX6 에 한 줄 |
| X2 | AX5 장부 자리 — 0.4 장부 `consult.ask` 꼴(BK 칸)을 깨지 않으려고 축은 **`consult.ask_axis`** 에 둔다(`consult.ask` 는 축 턴이면 null · `ask_why` = axis) | 스펙 「장부 `ask{axis, …}`」 → `ask_axis` 로 |
| X3 | 회차 · 대상 축 | 자리만(값 = 장바구니 옵션 안 고른 진료항목 — WP-5) |
| X4 | 축 선택지 이름 | 제품 = 허브 이름(`$J` `hub.products[].name` · 상위 제품은 scope `holder_name`) · 부위 = `sites[].name` · 고민 · 효과 = 허브 행 이름 |
| X5 | AX7 ③ 표본 | 실물에서 「LDM」 은 L 1(제품 LDM ∩ 이름 일치)이라 L 3 묶음은 아니지만 결과(축 0)는 같다 |
