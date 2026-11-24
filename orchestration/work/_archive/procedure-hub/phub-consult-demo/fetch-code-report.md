# SPEC-011 0.1.2 구현 리포트 — WP-1 ~ WP-4 + 호출마다 토큰 기록

발주 `task_c0df5e0a0b4d` · `ctx_3f0d2526ebe7`. 앱 워크트리 `A` 만 고쳤다 · 커밋 0 · 서브에이전트 0 · 18222 · 18105 그대로(pid 22755/22758 · 56189/56191 시작과 같음) · 허브는 GET 만 · 키 · 토큰 값 출력 0.
실물 재생은 빈 포트 18231(잘라 내기 끔) · 18232(켬)에 18222 와 같은 env + 따로 `CHAT_DIR`(스크래치)로 띄우고 끝나고 껐다. 재생 장부(명동점 블록 · 가격 포함)는 스크래치에만 있고 이 리포트에는 수 · 답 앞 2 줄만 옮겼다.

## 0. 머리 수

| 완료 조건 | 기준 | 결과 |
|---|---|---|
| WP-2 ① 표본 43 「## 자료」 | −55% 이상 | **−62.6%**(697,892 → 261,317 · 스펙 측정 −62.7%) |
| WP-2 ① 지금 시대 밖 11 | −10% 이상 | **−17.6%**(28,432 → 23,429) |
| WP-2 ② 빠짐 — 표본 · 밖 11 · 11-23 새 턴 | 0 | **0/276 · 0/49 · 0/79**(새 턴 13 · 인용 79) |
| WP-2 ③ 상세 잃음 | ≤ 7 | **7**(lineup 이름만 17 따로) · 새 턴 0(lineup 이름만 3) |
| WP-2 ④ offered(KD11) 전후 | 비교표 | 54 턴 가운데 같음 50 · 달라짐 4(§2-3) |
| WP-2 ⑤ 이름만 → 이름으로 다시 물음 → 같은 번호 상세 | 시험 | `test_v06_fetch_read.py::test_g7_names_then_named_again_same_number_full` 통과 |
| WP-1 JSON 깨짐 | 0 | 표본 · 밖 54 → 첫 실행 2 깨짐(이해 호출이 객체 뒤 「Wait —」 로 객체를 하나 더 냄) → `verify.parse` 고침(맨 끝 완결 객체) 뒤 0 · 새 턴 13 깨짐 0 |
| WP-1 fetch 빠짐 · 고침 | 기록 | 67 호출 모두 fetch 있음 · enum 고침 0 |
| WP-1 장부 `parsed.fetch` · `usage.cache_creation_input_tokens` | 있음 | 새 장부 13 턴 모두 있음 · 이해 캐시 쓰기 합 22,212(옛 장부는 null) |
| WP-3 「정보 없어요」 문장 | 0 | 안 가져온 종류로 인한 것 0 · **73bd T3 · T4 에 「필러 개요 정보는 없어요」 2**(EM `empty[]` — 개요를 읽었는데 허브 행 0 · 옛 답에도 같은 문장 · §6) |
| WP-3 이름만 줄 상세 지어냄 | 0 | 0 — 03b8 T6 은 이름만(branch) 57 이름 가운데 「올리지오, 인모드 같은 장비는 명동점에는 없어요」 로만 말함 |
| WP-4 재생 장부 칸 · cost.py | 다 있음 | `consult.fetch` · `material_size.by_fetch` · `tokens.calls[]` · `tokens.sum` 13/13 · `fetch-plan/cost.py`(사본 실행) 이해 14 호출 `understand_missing` = {} · 캐시 쓰기 22,764 |
| 실물 3 대화 답 입력(전이 있는 턴 합) | — | **1,004,680 → 493,098(−50.9%)** · 「## 자료」 바이트 987,846 → 185,993(−81.2%) · ecc6 T3 414,174 → 62,050 |
| 시험 | — | 관련 시험 전부 통과(새 24 포함) · 마지막 전체 700 통과 · 1 실패(옛 실패 · §5) · 2 건너뜀 |

## 1. WP 별 바뀐 파일:줄

### WP-1 이해 계약(JC1 ~ JC6 · LG1 · LG4)
- `prompts/consult.json` pick: 출력 꼴 줄(`fetch` = about · kinds · scope · lineup — **`layers` 칸 없앰**(JC3 추천 · 2차 `sub` 고정) · `site_filter` 없음) · 규칙 `20.` ~ `20-5.`(:335-340 — r4 20-1 · 20-2 · 20-4 · 20-5 그대로 · r4 20-3 layers 와 **20-6 앞 절 「scope = all 일 때만」 은 뺌**(P2-13) · 20-5 = 「부위 필터는 sites · 층은 앱이 정함」) · `pick.version` 0.6.0-draft(:311).
- `consult/verify.py`: `FETCH_ENUMS` · `FETCH_DEFAULT`(:24-28) · `Accepted.fetch`(:53) · `view()` 에 `fetch`(:68) · `parsed_view` 칸 목록에 `fetch`(:120 — LG1) · `fetch_of`(:124 — enum 밖 · 빈 칸 → 기본값 + `fixed[]` · 모르는 kinds 버림 · 없으면 `from = default`) · `verify` 에서 `a.fetch`(:307) · **`parse` 맨 끝 완결 객체 대체**(:83 `last_object` · :99 — 재생에서 찾은 JSON 깨짐 2 의 원인).
- `consult/understand.py:259` — usage 에 `cache_creation_input_tokens`(LG4) · `consult/turn.py:1047-1052` `understand_view.usage` 에 같은 칸 · `models`.
- (잼) **`layers` 칸 없앰**: 0.6.0 출력 중앙 152 토큰(표본) · 139(밖) — r4(`layers` 있음) 158 보다 −6 · 시스템 글 38,422 바이트(r4 38,854 · −432). 2차가 늘 `sub` 라 셈은 같다.
- (잼) **입구 목록 「명동점 없음」 표지**(`replay54.py --mark` · 표지 단 시스템 글 46,003 바이트 · +7,581): FR13b 02af T3 branch → branch · FR14 dc78 T4 branch → branch · 상세 잃음 2 → 2. **효과 0 · 이해 호출마다 +7.6 KB 라 넣지 않음.**

### WP-2 2차 읽기(G1 ~ G7 · 「읽고 잘라 내기」)
- **새 `consult/fetch_read.py`** — `Plan`(:40 — LG2 값 · `brief()` = AR2 줄) · `Line` · `Ctx` · `md_sets`(:89 — 매핑 `by_case` · `by_proc` · `by_product`) · `topic_codes`(:95) · `g2_kinds`(:105 — G2: fetch.kinds ∪ kinds ∪ KS3 · 비면 KS6 · topic 이면 고민 입구 더함 · KD9 없음) · `owner`(:123) · `decide`(:144 — 차례: 종류 없음 → 명시(G3) → 안전(G3 · UD5) → 종류(G2) → 주제(G6) → 층(G4 · `sub` 고정) → 범위 branch 이름만(G4) → lineup names(G5)) · `names_only`(:187) · `app_lines`(:192).
- `consult/kinds_pick.py` — KS5(KD9) 상담 경로에서 끔(:7 · :40 자리) · `STRONG_BY` = yes · entry · fetch(:20) · `decide(..., fetch_kinds)`(:42 — 1차 `fetch.kinds` = by `fetch` · KS8 필수 아님). `walk/front.py` KD9 · `KD9_SET` · `report.py` 경로는 안 건드림.
- `consult/material_read.py:95` — `fetch.kinds` 를 `decide` 에 넘김.
- `consult/material.py:163-238 renumber` — `cut`(뺌 · 이름만) · 이름만 묶음은 갈라 머리 `same` 도 이름 칸만 · 머리 `marks.names_only` = `branch` | `lineup` · `new_lines[].names_only` · `names_why` · `fetch`(까닭) · **G7**: `sent_names` 에 있는 gid 가 전체면 같은 번호로 다시 싣고, 다시 이름만이면 `seen_lines`.
- `consult/ledger.py:49` `Conv.sent_names` · `:242-246` 이름만 gid → `sent_names`(LG6) · 전체로 다시 실으면 `sent` 로 옮김.
- `consult/turn.py:193-204` — 상담 경로 `renumber` 를 **감지(`after_walk`) 뒤**로 옮김(G6 이 이번 턴 주제를 본다) · `cut = cs.fetch_cut(w)` · `sent_names` 넘김 · `:719 fetch_cut`(G1 대상 = 입구 표 · 명시 = accepted targets + follow · 주제 = 감지 뒤 지금 주제의 고민 이름 · 진료항목 허브 코드).
- `config.py:93-94` `CHAT_FETCH_CUT`(on 기본) · `.env.example` 한 줄(값 없음) — off 면 줄은 다 싣고 판단만 `new_lines[].fetch_would`(맞추지 않은 새 턴의 빠짐 셈에 썼다 · 되돌림 손잡이).
- 스펙 자리 가운데 **고치지 않은 것**: `walk/calls.py:137 _site_filters` · `:162 _facets` · `walk/ranges.py:16 ROLES_TARGET` · `walk/material.py:253 to_lines` — 「읽고 잘라 내기」 판이라 허브 호출은 그대로 두고 G4 · G6 은 `fetch_read.decide` 로 잘라 냈다(`walk/material.py` 는 `test_walk_material_and_gate_untouched` 가 HEAD sha 를 지킨다). 「안 읽기」 판에서 그 자리를 고친다.

### WP-3 3차 규칙(AR1 · AR2)
- `prompts/consult.json` kos rules `R14`(:391 — 이름만 줄: branch = 「명동점에는 없고 이런 것이 있다」 까지 · lineup = 이름만 · 상세 지어내지 않음) · `R15`(:392 — 「앱 판정」 의 fetch 밖 종류를 「정보 없음」 으로 말하지 않음) · `kos.version` · 최상위 `version` 0.6.0-draft.
- `consult/turn.py:978-979` — 「앱 판정」 에 `fetch` 한 줄(`Plan.brief()` — about · kinds · scope · lineup · AR2).

### WP-4 장부(LG2 · LG3 · 호출마다 토큰)
- `consult/turn.py:742 fetch_view` → 장부 `consult.fetch`(:1081 — about · kinds · layers · scope · lineup · from · fixed · g2 · 줄 판단 수 · applied) · `:751 fetch_size` → `material_size.by_fetch`(:211-212 — kind · layer · scope(branch · names_only · all) · forced(explicit · safety) 바이트 · `est_tokens`).
- **호출마다 토큰** `consult/turn.py:109-140 call_tokens` → 장부 `tokens`: 옛 평평한 칸(답 호출 usage)은 그대로 둠 + `calls[]` `{role, model, ms, input, output, cache_creation, cache_read, thinking}` + `sum`(네 칸 · 값 없으면 null). 답 호출 값은 `llm/cli.py:266-275` 왕복 합 그대로.
- 옛 칸을 읽는 곳(grep 전수): `token-cause/{common,decompose,cache_split,history_alt,tables}.py` · `fetch-plan/{cost,layers_check,run4,tables,measure}.py` — 모두 `tokens.input_tokens` 등 평평한 칸을 읽어 그대로 돈다(옛 칸을 둠). `speed.py` · `report.py` · `runs.py` · `columns/*` 는 시험 앱 `runs.jsonl` 의 열 `tokens` 라 상담 장부와 무관.

### 상담 경로 LLM 호출 목록(grep `run_cli` · `und.call` · `llm.turn` · `system_one`)
| role | 자리 | 장부 |
|---|---|---|
| understand | `consult/turn.py` `Consult.understand` → `consult/understand.py:222 call` → `run_cli`(:230) | `tokens.calls[0]` · `consult.understand.usage` |
| answer | `consult/turn.py` `run_turn` → `ctx.llm.turn` → `llm/chat_cli.py:159 run_cli`(`--resume`) | `tokens.calls[1]` · 옛 평평한 칸 |
| (상담 밖) | `clients/jev_client.py:79`(끈 가지 `col_b.walk` 만) · `llm/cli.py:318`(시험 앱 열) · `consult/e8.py:100` · `consult/probe.py:72`(실측 스크립트) | 해당 없음 |

턴당 LLM 호출은 이해 1 + 답 1 이다(`talk` 턴도 같음 · 이해 실패 턴은 답 1).

## 2. 완료 조건 수치

### ① ② ③ 표본 43 · 지금 시대 밖 11 — 앱 프롬프트 0.6.0-draft 실제 이해 호출 + 앱 `fetch_read.decide`

| 모음 | 시대 | 턴 | 「## 자료」 토큰(× k 0.458) | 감소 | 빠짐 / 인용 | 상세 잃음 | lineup 이름만 |
|---|---|---|---|---|---|---|---|
| sample | 전체 | 43 | 697,892 → 261,317 | −62.6% | 0 / 276 | 7 | 17 |
| sample | default | 10 | 444,411 → 60,932 | −86.3% | 0 / 54 | 0 | 0 |
| sample | understand | 33 | 253,481 → 200,385 | −20.9% | 0 / 222 | 7 | 17 |
| outside | 전체 | 11 | 28,432 → 23,429 | −17.6% | 0 / 49 | 0 | 0 |
| outside | default | 2 | 19,588 → 15,422 | −21.3% | 0 / 6 | 0 | 0 |
| outside | understand | 9 | 8,844 → 8,007 | −9.5% | 0 / 43 | 0 | 0 |

- sample: JSON 깨짐 0 · fetch 빠짐 0 · fetch 고침 턴 0 · 이해 출력 중앙 152 토큰 · 이해 ms 중앙 2544.8
- outside: JSON 깨짐 0 · fetch 빠짐 0 · fetch 고침 턴 0 · 이해 출력 중앙 139 토큰 · 이해 ms 중앙 2473.9

상세 잃음 줄:

| 턴 | 줄 | 까닭 | 종류 | 주인 |
|---|---|---|---|---|
| a578 T5 | 136 | branch | indication | 슈링크 |
| a578 T5 | 195 | branch | indication | 올리지오 |
| 5bce T6 | 132 | branch | indication | 나보타 |
| 5bce T6 | 134 | branch | indication | 보툴렉스 |
| 5bce T6 | 338 | branch | indication | 메디톡신 |
| dc78 T4 | 28 | branch | overview+mechanism | PPC 지방분해주사 |
| dc78 T4 | 30 | branch | overview+mechanism | 카복시테라피 |

### ④ offered(KD11) 전후 — 같은 입구 · 옛 = 장부 `trace.front.offered`(KD9 있음) · 새 = 앱 `kinds_pick.decide`(KS5 끔 · fetch.kinds) · 같음 50 · 달라짐 4

| 턴 | 질문 | 옛 kd9 종류 | 옛 offered | 새 offered | 읽는 종류 빠짐(옛−새) | 읽는 종류 더함(새−옛) |
|---|---|---|---|---|---|---|
| 03b8 T5 | 고주파 원리가 머야 ? | - | overview | - | - | overview |
| 03b8 T6 | 응 고주파에 대해서 전반적으로 설명해줘 | indication,lineup,mechanism,outcome | - | - | - | - |
| a7d7 T8 | 볼뉴머가 머야 | indication,lineup,mechanism,outcome | - | - | - | - |
| 5bce T6 | 미간주름에 보톡스만 가능해 ? | - | overview | overview,package | lineup | combo |
| dc78 T4 | 응 어떤 원리인지 어떤 시술인지 궁금해 | indication,lineup,outcome | - | - | indication,lineup,outcome | - |
| dc78 T8 | 응 써마지 몇샷 맞아야해 ? | - | - | overview | - | outcome |
| 02af T3 | 그럼 실 리프팅은 없어 명동점에 ? | - | - | overview | offer | lineup |
| 7897 T2 | 볼뉴머에 대해서 설명해줄래 ? | indication,lineup,mechanism,outcome | - | - | - | - |
| 67bb T6 | 응 팔자주름에는 보톡스에 대해 알려줘 | lineup,mechanism,outcome | - | - | - | - |

(달라진 4 · 읽는 종류만 다른 5 — KS5 끔으로 KD9 종류 대신 1차 `fetch.kinds` 가 같은 다섯을 고른 「전반 설명」 턴(03b8 T6 · a7d7 T8 · 7897 T2)은 읽는 종류가 같다. dc78 T4 「어떤 원리인지 어떤 시술인지」 는 KD9 의 indication · lineup · outcome 을 안 읽게 됐고 인용 빠짐은 0.)

## 3. 실물 3 대화 — 전 → 후(호출별)

### 실물 3 대화 — 전(옛 장부) → 후(이번 앱 · 잘라 내기 켬) · 칸 = input / cache_creation / cache_read / output

| 턴 | 말 | 이해 전 | 이해 후 | 답 전 | 답 후 | 답 입력 합 전 → 후 | 「## 자료」 바이트 전 → 후 | fetch(about/kinds/scope/lineup) | 「정보 없음」 류 문장 |
|---|---|---|---|---|---|---|---|---|---|
| 03b8 T1 | 팔자주름에 대해서 고민이돼 | 2/null/19183/97 | 2/0/21063/139 | 2/11688/5608/280 | 2/17691/0/772 | 17,298 → 17,693 | 1,337 → 1,337 | targets/[]/branch/none | 0 |
| 03b8 T2 | 미간에 주름도 고민이야 | 2/null/19183/117 | 2/1341/20507/159 | 4/5517/16976/317 | 4/5046/17691/643 | 22,497 → 22,741 | 892 → 892 | targets/[]/branch/none | 0 |
| 03b8 T3 | 얼굴에 탄력이 좀 떨어지는거 같은 | 2/null/19183/117 | 2/1883/20507/159 | 4/7744/22493/447 | 4/8110/22737/367 | 30,241 → 30,851 | 2,566 → 2,566 | targets/[]/branch/none | 0 |
| 03b8 T4 | 그중에서 소프웨이브, 써마지, 울 | 2/null/19183/133 | 2/2396/20507/175 | 4/9480/30237/675 | 4/8827/30847/1825 | 39,721 → 39,678 | 13,455 → 13,455 | targets/[]/branch/none | 0 |
| 03b8 T5 | 고주파 원리가 머야 ? | 2/null/19183/98 | 2/3168/20507/151 | 4/9039/39717/282 | 4/12183/39674/1348 | 48,760 → 51,861 | 15,520 → 20,062 | targets/overview,mechanism/branch/none | 0 |
| 03b8 T6 | 응 고주파에 대해서 전반적으로 설 | 2/null/19183/97 | 2/3242/20507/174 | 4/43255/48756/1395 | 4/31234/51857/2991 | 92,015 → 83,095 | 90,211 → 60,856 | targets/overview,mechanism,indication,outcome,lineup/branch/names | 0 |
| ecc6 T1 | 요즘 피부 탄력이 저하 되서 고민 | 2/null/19411/98 | 2/0/21069/133 | 2/0/18358/258 | 2/0/18753/995 | 18,360 → 18,755 | 2,548 → 2,548 | targets/[]/branch/none | 0 |
| ecc6 T2 | 얼굴에 | 2/null/19411/104 | 2/1659/20507/139 | 4/197324/18038/294 | 4/39255/18753/1064 | 215,366 → 58,012 | 433,360 → 79,429 | topic/[]/branch/none | 0 |
| ecc6 T3 | 얼굴에 | 2/null/19411/104 | 2/2656/20507/139 | 4/198808/215362/505 | 4/4038/58008/497 | 414,174 → 62,050 | 423,129 → 20 | topic/[]/branch/none | 0 |
| 73bd T1 | 얼굴에 피부 탄력이 없어져서 걱정 | 2/null/19183/118 | 2/0/21071/160 | 2/12827/5608/1066 | 2/12865/5965/986 | 18,437 → 18,832 | 2,548 → 2,548 | targets/[]/branch/none | 0 |
| 73bd T2 | 아 주름이 눈가 입꼬리에 잇어 | 2/null/19183/533 | 2/1696/20507/557 | 4/7965/18435/788 | 4/7922/18830/633 | 26,404 → 26,756 | 1,379 → 1,379 | targets/[]/branch/none | 0 |
| 73bd T3 | 아 눈가는 볼뉴머 이ㅃ고리는 필러 | 2/null/19183/464 | 2/2174/20507/252 | 4/2147/26400/1900 | 4/3559/26752/1034 | 28,551 → 30,315 | 881 → 881 | targets/[]/branch/none | 1 |
| 73bd T4 | 입꼬리에는 필러를 맞고 싶다니까 | 2/null/19183/116 | 2/1997/20507/158 | 4/4305/28547/1260 | 4/2144/30311/418 | 32,856 → 32,459 | 20 → 20 | targets/[]/branch/none | 0 |

합(전이 있는 턴): 답 입력 1,004,680 → 493,098 · 「## 자료」 바이트 987,846 → 185,993 · 이해 캐시 쓰기(새로 남김) 합 22,212

- **주의(검수 P2-4)**: cache_creation 과 cache_read 는 캐시 상태(앞 실행이 같은 시스템 글 · 세션을 데웠나)에 따라 서로 옮겨 간다 — 03b8 T1 「후」 의 cache_creation 17,691 이 다른 실행에서는 cache_read 17,691 로 나온다. 턴 사이 · 실행 사이 비교는 네 칸 하나하나가 아니라 **입력 합(input + cache_creation + cache_read)** 으로 본다.
- 전 = 옛 장부(03b8 · 73bd 는 `runs/consult/turns.jsonl` · ecc6 는 테스트 고침 E 재생 장부) · 후 = 18232(잘라 내기 켬) 새 장부.
- 이해 「전」 의 cache_creation 은 옛 앱이 버린 칸이라 null(LG4 로 이번부터 남음).
- 03b8 T5 는 1차가 「원리」 꼴로 overview 를 더해 자료가 늘었다(15,520 → 20,062 바이트 · FR6 규칙대로).
- ecc6 T3 후 「## 자료」 20 바이트 = 같은 말을 되풀이해 새 줄 0(앞 턴 줄은 `seen_lines`).

### 맞추지 않은 새 턴(11-23 · 잘라 내기 끔으로 다 실은 답의 인용 줄 ↔ 2차 판단)

| 턴 | 이해 JSON | fetch | 인용 줄 | 빠짐(뺌) | 상세 잃음(이름만) | lineup 이름만 | 「## 자료」 바이트(끔) | 판단 수 |
|---|---|---|---|---|---|---|---|---|
| 03b8 T1 | ok | 있음 | 7 | 0 | 0 | 0 | 1,337 | {} |
| 03b8 T2 | ok | 있음 | 5 | 0 | 0 | 0 | 892 | {} |
| 03b8 T3 | ok | 있음 | 6 | 0 | 0 | 0 | 2,566 | {} |
| 03b8 T4 | ok | 있음 | 20 | 0 | 0 | 0 | 13,455 | {'full': 12} |
| 03b8 T5 | ok | 있음 | 9 | 0 | 0 | 0 | 30,650 | {'full': 15, 'names': 26} |
| 03b8 T6 | ok | 있음 | 13 | 0 | 0 | 3 | 90,211 | {'full': 177, 'names': 185} |
| ecc6 T1 | ok | 있음 | 3 | 0 | 0 | 0 | 2,548 | {} |
| ecc6 T2 | ok | 있음 | 3 | 0 | 0 | 0 | 432,209 | {'drop': 1474, 'full': 104} |
| ecc6 T3 | ok | 있음 | 2 | 0 | 0 | 0 | 420,558 | {'drop': 1704, 'full': 125} |
| 73bd T1 | ok | 있음 | 4 | 0 | 0 | 0 | 2,548 | {} |
| 73bd T2 | ok | 있음 | 6 | 0 | 0 | 0 | 1,379 | {} |
| 73bd T3 | ok | 있음 | 1 | 0 | 0 | 0 | 881 | {'full': 1} |
| 73bd T4 | ok | 있음 | 0 | 0 | 0 | 0 | 20 | {} |

- 18231(잘라 내기 끔 · 줄은 다 실음 · 판단만 기록)에서 같은 3 대화를 돌려, 답이 인용한 줄 가운데 2차가 뺐을 줄(빠짐) · 이름만으로 줄였을 줄(상세 잃음)을 셌다 — 13 턴 · 인용 79 · **빠짐 0 · 상세 잃음 0** · lineup 이름만 3(03b8 T6).
- ecc6 T2 · T3(끔)은 432 · 421 KB 를 싣고 그중 1,474 · 1,704 줄을 2차가 뺀다 — 뺀 줄 인용 0.

### 답 앞 2 줄(잘라 내기 켬)

| 턴 | 답 앞 2 줄 |
|---|---|
| 03b8 T1 | 팔자주름이 신경 쓰이시는군요. / 팔자주름에는 꺼진 곳을 채우는 쪽, 콜라겐 생성을 자극하는 쪽, 당기거나 열로 탄력을 주는 쪽처럼 접근이 여러 갈래예요. |
| 03b8 T2 | 미간주름 이야기로 바뀌었어요. 앞에서 보시던 팔자주름 목록은 아래에 그대로 남아 있어요. / 미간주름에는 근육의 움직임을 줄이는 쪽, 주름을 채우는 쪽, 콜라겐 생성을 자극하거나 열로 탄력을 주는 쪽이 있어요. |
| 03b8 T3 | 피부 탄력 이야기로 바뀌었어요. 앞의 팔자주름과 미간주름 목록은 아래에 남아 있어요. / 탄력 저하에는 열로 조직을 가열하는 쪽, 콜라겐 생성을 자극하는 쪽, 피부 속을 채우고 보충하는 쪽처럼 접근이 꽤 다양해요. |
| 03b8 T4 | 세 가지 모두 에너지를 피부에 전달하는 기기 리프팅 계열이에요. / 소프웨이브는 1.5mm 깊이에 집속초음파를 보내는 장비예요. |
| 03b8 T5 | 고주파는 고주파 에너지를 피부 깊은 층까지 보내 열을 내는 방식이에요. / 그 열로 콜라겐이 수축하고, 새 콜라겐이 만들어지도록 이끌어요. |
| 03b8 T6 | 고주파는 고주파 에너지로 피부 깊은 층에 열을 내서, 콜라겐을 수축시키고 새로 만들어지게 하는 비침습 리프팅이에요. / 얼굴에서는 모노폴라가 근막층이나 피하지방층까지, 바이폴라는 표피를 보호하면서 진피층까지 전달하는 식으로 나뉘어요. |
| ecc6 T1 | 요즘 탄력이 떨어져서 신경 쓰이시겠어요. / 탄력 고민에는 열로 조직을 데워 응고시키는 기기 리프팅, 실로 당겨 올리는 실리프팅, 속을 채우고 수분을 붙들어 주는 스킨부스터 같은 계열이 있어요. |
| ecc6 T2 | 얼굴 쪽 탄력이 고민이시군요. / 이 고민에는 온다나 슈링크 유니버스 같은 시술도 올라와 있어요. |
| ecc6 T3 | 얼굴 쪽 탄력 고민으로 보고 있어요. / 혹시 마음에 두신 시술이 있으세요? 예를 들면 온다, 슈링크, 올리디아 같은 것들이요. |
| 73bd T1 | 얼굴 탄력이 떨어져서 걱정되시겠어요. 피부 탄력 저하에는 열로 조직을 가열해 끌어올리는 기기 리프팅, 실로 당겨 주는 실리프팅, 콜라겐 생성을 자극하는 방식 등이 있어요. / 혹시 온다, 슈링크, 울쎄라 같은 시술 중에 마음이 가는 게 있으세요? |
| 73bd T2 | 주제가 눈가주름과 입꼬리주름으로 바뀌었어요. 탄력 저하 때 보던 목록은 아래에 남아 있어요. / 눈가주름에는 근육 움직임을 줄여 주는 보톡스나 주름을 채우는 필러, 열로 조직을 가열하는 기기 리프팅 같은 방식이 있어요. 입꼬리주름은 채우는 방식의 필러 계열이 있어요. |
| 73bd T3 | 눈가는 볼뉴머, 입꼬리는 필러로 나눠 볼게요. 이번에는 입꼬리주름과 필러 조건으로 봤고, 눈가 볼뉴머는 앞 목록에 남아 있어요. / 필러 개요 정보는 없어요. 입꼬리주름에는 주름을 채우는 방식이 맞고, 명동점에는 얼굴필러 진료항목이 있어요. |
| 73bd T4 | 네, 입꼬리에는 필러로 보고 있어요. 말씀을 제대로 못 알아들어서 죄송해요. / 필러 개요 정보는 지금 없어요. 명동점에는 얼굴필러 진료항목이 여섯 가지 있어요. |

## 4. 화면

`e2e-shots/fetchplan-*.png`(새 브라우저 프로필 · Playwright chromium · 18232):
- `fetchplan-03b8-final.png` · `fetchplan-ecc6-final.png` · `fetchplan-73bd-final.png` — 재생 마지막 화면(주제 머리 · 얼굴 점 · 진료항목 목록 · 답).
- `fetchplan-73bd-modal.png` — 목록 「시술설명」 모달(탭 · 원리 그림).
- `fetchplan-spinner.png` — 새 대화 첫 턴 「질문을 이해하고 있어요」 스피너 · `fetchplan-spinner-done.png` — 그 턴 끝.
- 페이지 오류 0. (`fullPage` 찍기는 고정 배치에서 빈 화면이 찍혀 보이는 창으로 찍었다.)

## 5. 시험

- 관련(스펙 목록 + 고친 시험): `test_v04_understand` · `test_v04_prompt` · `test_v03_prompt` · `test_v04_material` · `test_v06_material` · `test_consult_material` · `test_walk_front` · `test_walk_core` · `test_v06_groups` · `test_v04_ledger` · `test_v05_llm_block` · `test_v04_turn` · `test_v04_verify` → 통과.
- 새 `tests/test_v06_fetch_contract.py`(8 — fetch 기본 · enum 고침 · parsed/accepted · 규칙 20 · LG4 · 호출마다 토큰 · null · 두 객체 parse) · `tests/test_v06_fetch_read.py`(16 — FR1 · FR4 · FR5 · FR6 · FR8 · FR10 · FR13b · FR15 · G3 명시 · G4 자기/물려받음 · 후보 줄 · FR3 G6 · FR17 · renumber 이름만 묶음 · **G7 a578 T5 → T7 꼴** · 끔 그대로).
- 고친 옛 시험: `test_v04_material`(KS5 끔 — overview yes 갈래 · kd9 없음 · fetch 종류) · `test_v05_llm_block`(kos 규칙 수 15 → 17 · 판 0.6.0) · `test_v03_prompt` · `test_v04_prompt` · `test_v04_ledger`(판 · usage 칸 · `models`).
- **마지막 전체 한 번: 700 통과 · 2 건너뜀 · 1 실패** — `test_state_object.py::test_s5_t18_terminal_turn_updates_but_no_list_then_catches_up`: 둘째 턴(대상 0 · 거둠만 · out)이 `verify` 의 옛 규칙 「검수 L-1 대상 없이 거둠만 = talk」(`verify.py` 끝 · 이번 작업 전부터 있음)으로 `talk` 가 되어 `end_state` None — 이번 변경이 닿지 않는 갈래(디버그로 `turn_kind = {talk, withdraw_only}` 확인). 고치지 않았다.

## 6. 남은 것

1. **「정보 없어요」 문장 2(73bd T3 · T4 「필러 개요 정보는 없어요」)** — 2차가 안 가져온 종류가 아니라 개요를 읽었는데 허브 행이 0 인 EM `empty[]` 를 답이 그대로 말한 것(옛 답 T3 · T4 에도 같은 문장). SPEC-010 검수 P2-2 몫 — EM 빈 칸 문장 규칙을 정할 것(코디 결정).
2. FR13b · FR14 오답(1차가 `branch`)은 그대로 — 「명동점 없음」 표지 효과 0(§1 WP-1). dc78 T4 상세 잃음 2 는 남는다.
3. 「안 읽기」 판(허브 호출 줄임 · `walk/calls.py` · `walk/ranges.py` 자리)은 다음 판.
4. `verify.parse` 맨 끝 객체 대체는 스펙 밖의 작은 고침(재생 JSON 깨짐 2 의 원인) — 검수에서 보아 줄 것.
5. 장바구니 R5(FR9 `fetch.kinds ∋ offer`)는 이 작업 밖 — `Accepted.fetch` 로 읽을 수 있다.
6. 실물 「후」 답 출력 토큰이 몇 턴 늘었다(03b8 T4 675 → 1,825 등) — 같은 앱이라도 답 길이는 호출마다 다르다 · UD4 대로 기록만.

## 7. 산출 · 다시 돌리기

- 스크립트 `fetch-code/`: `replay54.py`(표본 · 밖 재생 · `--offline` · `--mark`) · `redo.py`(깨짐 턴만 다시) · `bad_raw.py`(원문 보기) · `live3.py`(실물 3 대화 HTTP) · `tables.py`(표) · `final.cjs` · `modal.cjs` · `shots.cjs`(화면).
- 출력 `fetch-code/out/`: `understand_{sample,outside}.jsonl`(JSON · usage — 원문은 깨짐 턴 바이트 수만) · `redo_*.jsonl` · `replay54.json` · `mark_check.json` · `live_{on,off}.json`(대화 id) · `tables.md`.
- 재생 장부(가격 포함)는 스크래치 `…/scratchpad/fc/live_{on,off}/turns.jsonl` 에만.

```bash
A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo; W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo
cd $A && PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python $W/fetch-code/replay54.py --offline
uv run --no-sync python -m pytest -q tests/test_v06_fetch_contract.py tests/test_v06_fetch_read.py
```
