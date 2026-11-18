# 새 gold × 허브 MCP × Jev × LLM 연결 — 조사 리포트

작성: 2026-11-16 · researcher 워커(read-only) · 브리프 `phub-gold-jev-research-brief.md`
경로 접두어: `P` = 이 워크트리 · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model` · `HUB` = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` · `APP` = `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`

> 공개 레포 규칙: 이 리포트에는 표 · 칸 이름, id(코드), 셈, 질문 id · 범위만 싣는다. 시술 설명 · 원장 문장 · 답 원문 · 가격 값 · 질문 문장은 싣지 않는다.
> 결정하지 않는다 — 추천과 근거만 붙여 「정할 것」으로 모은다. 「확인 안 됨」은 그대로 적는다.

---

## 0. 요약

**Q1 새 gold 구조** — `g_*` 15표 = 속성 12 + 그래프 내보내기 2(`g_node` · `g_edge`) + 근거 참조 1(`g_evidence`). 속성 표 행 24,115 전부가 `g_evidence` 로 silver 행에 되짚히고(빠짐 0), silver `source_ref` 로 원장 포인터까지 간다. 그래프는 노드 1,545(10종) · 엣지 10,389(23종). **부위 · 재료 · 방법 · 해부는 노드가 아니다**(입구 `g_entry` 와 속성 칸에만 있음).
**Q2 옛 허브** — 입력은 실버 · 시맨틱 JSON 13파일(`semantic.json` 해시 가드), 허브 안에서 규칙 G1~G22 로 빌드해 `gold_*` 8테이블에 발행 → 서버 시작 때 메모리 그래프. 도구는 MCP 11(커밋) + 2(미커밋 `selected_pair` · `global_claims`), REST 같은 수 + health. 전부 옛 노드 13종 · fact section 18 · intent 12 체계 위에 있다.
**Q3 대조** — 옛 도구 중 그대로 쓸 수 있는 것은 0. 모양만 살릴 것 7(resolve · recommend · procedure_card · pair_check · check_conditions · combos · neighbors), 필요 없음 6(compare · vocab 대부분 · peek/expand 의 section 체계 · selected_pair · global_claims). 배관은 **MCP 마운트 · lifespan · 발행/해시 · 메모리 색인 · 조사 떼기 목록은 틀만 가져가고, 빌드(build.py 1,415줄) · 사실(fact) 체계 · 봉투(claude_contract · companion · intent)는 버린다.**
**Q4 앱** — Jev 클라이언트 · MCP 클라이언트 · 기록(runs.jsonl) · 시간/비용 셈 · CLI provider 는 가져갈 만하다. 커밋본 걷기(case3)는 「여러 개 고르기를 Choice 로」 하고 있어 llms.txt 와 어긋나고, 미커밋 WP-10 `_frontier_choice` 는 「후보마다 Noul + answer_ready Noul 한 요청」으로 llms.txt §3 과 맞다. 다만 그 걷기 전체가 옛 peek/expand/section 에 묶여 있어 다시 쓴다.
**Q5 질문 37 × 걷기** — 상태 = 답함 34 · 원장 확인 2(Q10 · Q33) · silver 빈칸 1(Q12). 질문 경로의 후보 수는 전부 255 아래(최대 = Q08 상위 고민 → 후보 130 · 시술 50). 255 를 넘는 곳은 **역방향**뿐(부작용 노드 ← 대상 379 · 2노드, 한 계열 노드 전체 이웃 263). 시험 세트는 37 그대로 + 입구 겹침 · 조사 · 역방향 · 같은 날 빈칸 · 충돌 · 해당 없음 묶음을 더하는 것을 추천.
**Q6 연결 설계** — 허브: `release/v1.2.0` 새 브랜치 · 새 모듈 · gold CSV 그대로 적재(+ silver `source_ref`) · 요청은 메모리 색인. MCP 최소 8도구 초안(§6-3). 앱: 범위 Choice 1번 → (허브 후보) → 후보마다 Noul + answer_ready Noul → 앱 hard gate → LLM. 종료 4상태.

### 정할 것 (사용자가 고를 것만 · 각 추천 포함)

| # | 정할 것 | 선택지 | 추천 | 근거 |
|---|---|---|---|---|
| D1 | 허브 코드 자리 | (a) PROCEDURE-HUB `release/v1.2.0` 에서 새 브랜치 · 새 모듈 (b) PR #31 브랜치 위에 이어서 (c) 허브 밖 별도 소형 서비스 | **(a)** | PR #31 의 gold 모듈 전체가 옛 데이터 체계(§2). release/v1.2.0 에는 MCP · graph_main 이 아예 없음(§3-3) — 틀만 다시 옮겨 쓰는 편이 깨끗. 「허브 = 결정론」 원칙은 (c)와 어긋남 |
| D2 | 허브 저장 꼴 | (a) gold 표 1:1 관계형 테이블 + 발행 해시, 요청은 메모리 색인 (b) DB 없이 CSV 를 시작 때 메모리로만 (c) 표마다 JSONB 한 덩이 | **(a)** · 실험 속도가 급하면 (b) 로 시작 | 11-16 결정 「관계형 먼저 + 그래프 내보내기」. (b)는 결정 4의 「DB 적재 = 다음 범위」와도 맞지만 발행 이력 · 해시 대조가 없음 |
| D3 | silver `source_ref` 도 허브에 적재? | (a) 적재(근거 → 원장 포인터까지 허브 응답에) (b) gold 행 → silver 행까지만 | **(a)** | `g_evidence` 는 silver 행을 **가리키기만** 한다(semantic-map §4). 원장 포인터는 `source_ref` 에만 있음. 안 올리면 산출물 추적성이 silver 에서 끊김 |
| D4 | MCP 도구 집합 | §6-3 초안 8도구 그대로 / 줄이기 / 더하기 | **초안 8** | 37문항 경로가 전부 이 8개로 닫힘(§5 표의 「읽을 gold 표」 열) |
| D5 | 앱의 허브 호출 길 | (a) 걷기 = REST · LLM 직접 질의 = MCP(옛 구조) (b) 전부 MCP | **(a)** | 옛 앱이 이미 `hub_rest`(걷기) · `hub_mcp`(case1 · 2) 둘 다 씀. 같은 코어를 두 입구가 부르는 옛 허브 틀(`service.py` → REST/MCP)과 맞음 |
| D6 | Jev 판단 지점 | (a) 범위 Choice 1 + 후보 Noul fan-out + answer_ready Noul (b) (a) + 입구 겹침도 Jev Choice | **(a)** — 입구 겹침은 semantic-map §1 규칙(범위 → 순서)으로 앱이 먼저 · 규칙이 못 가르면만 Choice | llms.txt §2 「하나만 고를 때만 Choice」 · 겹침 99 norm 중 범위 규칙으로 갈리는 것이 대부분(§1-5) |
| D7 | Noul 문턱값 | (a) 옛 값(yes 0.7 · no 0.3 · 그 사이 보류) 임시 + 기록 후 보정 (b) 보정 세트부터 | **(a)** | llms.txt §1 「임계값은 실제 질문 · 위험도별 평가로」. 37문항 1회차 trace 가 보정 재료가 됨 |
| D8 | 답 생성 LLM 경로 | (a) Anthropic SDK(옛 case3 · `anthropic_client.py`) (b) CLI 구독(`claude -p` · `codex exec` — `llm/cli.py`) (c) 둘 다 | **확인 필요 — 추천 보류** | 옛 앱에 둘 다 있음. 어느 쪽이 지금 쓸 수 있는지(키 · 구독)는 이 조사에서 확인하지 않음(.env 금지) |
| D9 | 앱 코드 자리 | (a) clinic_chat 새 브랜치(main 기준) · 새 case 모듈 (b) hub-evals 브랜치 위 | **(a)** | hub-evals 에 미커밋 16파일(WP-8~10)이 얽혀 있고 case3 가 옛 허브 꼴에 묶임(§4). 클라이언트 4개만 옮기면 됨 |
| D10 | Jev instructions 언어 | (a) instructions 영어 · state 는 한국어 이름 + 코드 (b) 전부 한국어 | **(a)** | jev-research §1(영어 주 학습 · CJK 정확도 낮음). 미커밋 WP-10 이 이미 (a) |
| D11 | 시험 세트 | (a) 37 그대로 (b) 37 + 추가 묶음(§5-3 약 12) | **(b)** | 37 은 gold 시범용이라 입구 겹침 · 조사 · 역방향 · 해당 없음 · 충돌을 거의 안 건드림(§5-3) |
| D12 | 255 넘는 역방향(부작용 ← 대상 379) | (a) 범위 밖으로 두고 시험에서 뺌 (b) 종류(계열 · 시술 · 케이스 · 제품 · 패키지)로 먼저 나눠 2단 (c) Noul fan-out 을 32개씩 쪼개 전부 | **(c)** | Noul 은 선택지 한도가 없음 — 255 는 Choice 한도(jev-research §2-3). 미커밋 `_frontier_choice` 가 이미 32개 묶음으로 전부 평가(APP `clinic_chat/cases/case3.py:1730`) |

---

## 1. Q1 — 새 gold 구조

### 1-0. 셈 명령

모든 셈은 scratchpad 의 python(표준 라이브러리 csv 만)으로 했다. 스크립트 전문은 부록 A.

```sh
python3 q1.py  $SM/gold          # 표 행 수 · 노드/엣지 분포 · 근거 · scope · entry 겹침
python3 deg.py $SM/gold          # 노드별 이웃 수(엣지 종류 · 방향별) · 고민 → 후보 수
python3 q5.py  $SM               # 질문 37 걷기 셈(gold-build.py QUESTIONS 를 ast 로 읽음)
cd $SM && python3 gold/gold-check.py   # 판정 인용용
```

`gold-check.py` 결과(11-16 실행 · 이 워커): A1 · A3 · K1~K7 · M1 · V1 · Q1 · H1 통과 · **구조 문제 0** · gold 해시 `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c`. FAIL 2 = A2(silver-check 끝 줄 FAIL 1) · G1(미추적 `orchestration/work/phub-gold-jev/`) — 브리프가 말한 알려진 것. 실행 전후 gold CSV 해시 같음(`shasum` 묶음 `a378da10…` 전후 동일).

> 참고 차이: `gold-final-notes.md:22` 는 같은 날 「불가 22 · 채움 112」, 지금 gold 는 **불가 25 · 채움 115**(`g_pair.same_day` 셈 · gold-check K6 「같은 날 채움 115」). `_RESUME.md:452-453` 의 11-16 결정(PRL-0884~0886 불가로 채움)이 notes 뒤에 반영된 것 — 데이터가 맞고 notes 숫자가 낡음.

### 1-1. 15표 — 역할 · 키 · 행 수 · 잇는 칸

| 표 | 역할(README `gold/README.md:7-22`) | 키 | 행 | 다른 표와 잇는 칸 | silver 되짚기(`silver_table` 분포) |
|---|---|---|---:|---|---|
| `g_entry` | 입구: 이름 · 별칭 → 개념 | `gid` | 2,642 | `entity_table`+`entity_code` → 노드 · `g_profile.subject_*` | alias 831 · product 315 · concern 260 · adverse 188 · condition 151 · material 143 · … |
| `g_scope` | 물려받기 · 하위 · 경유 펼침 | `gid` | 4,202 | `subject_*` · `holder_*`(→ 모든 속성 표의 `target_*` / `from_*`·`to_*`) · `link`(silver 경로) | procedure_case 1,032 · procedure 985 · case_product 892 · product 739 · package_item 255 · product_procedure 162 |
| `g_profile` | 계열 · 시술 · 케이스 · 제품 한 장 | `gid` (`subject_table`+`subject_code` 유일) | 739 | `modality_code` · `procedure_code` · `mechanism_code` | product 315 · procedure_case 268 · procedure 138 · modality 18 |
| `g_indication` | 적응 × 물은 고민 × 닿은 시술 | `gid` | 4,866 | `asked_concern_code` · `concern_code` · `target_*` · `candidate_*` · `procedure_code` | indication 4,866 |
| `g_outcome` | 효과(시간 3묶음) | `gid` | 1,604 | `target_*` · `effect_code` | outcome |
| `g_adverse` | 부작용 위험 × 빈도 | `gid` | 2,923 | `target_*` · `adverse_code` · `freq_silver_id` | adverse_risk |
| `g_adverse_detail` | 요인 · 대처 · 등급 | `gid` | 3,828 | `adverse_risk_id`(→ `g_adverse.silver_id`) · `target_*` | adverse_guidance 3,061 · adverse_factor 732 · adverse_rating 35 |
| `g_recovery` | 회복(다운타임) | `gid` | 37 | `target_*` | recovery |
| `g_contraindication` | 사람 조건 금기 | `gid` | 350 | `target_*` · `condition_code` | contraindication |
| `g_pair` | 시술 간 관계 | `gid` | 904 | `from_*` · `to_*` · `conflict_id` | procedure_relation |
| `g_package` | 패키지 × 항목 | `gid` | 312 | `package_id` · `concern_code` · `item_*` · `item_procedure_code` | package_item |
| `g_offer` | 상품 × 파는 것 | `gid` | 163 | `offer_id` · `item_*` · `procedure_code` · `modality_code` | offer_item |
| `g_node` | 그래프 노드 `표:코드` | `node_id` | 1,545 | `node_table`+`node_code` | (노드 자신) |
| `g_edge` | 그래프 엣지 → gold 행 | `edge_id` | 10,389 | `src` · `dst`(= `g_node.node_id`) · `gold_table`+`gold_id` | (gold 행으로 되짚음) |
| `g_evidence` | gold 행 → 근거 silver 행 | (`gold_table`,`gold_id`,`silver_table`,`silver_id`) | 27,740 | 전 gold 표의 `gid`/`node_id` | — |
| (`questions.csv`) | 질문 시범 37 | `id` | 37 | `gold_pointers` → gid | — |

행 수는 gold-check 끝 줄 「표 행 수」와 같다. 모든 속성 표 행은 `silver_table` · `silver_id` · `evidence_kind` 를 끝에 갖는다(헤더 `head -1 g_*.csv`).

자주 쓰일 값 분포(필터 · gate 설계에 필요):

- `g_indication.reach`: 제품 경유 2,579 · 시술 직접 571 · 계열 층만 539 · 케이스 직접 509 · 제품 → 시술(product_procedure) 388 · 패키지 — 항목 코드 없음 128 · 패키지 경유 97 · 제품 — 케이스 없음 55 / `concern_match`: 하위 고민 2,498 · 직접 2,305 · 빈칸 63
- `g_pair.question_class`: 재시술 간격 460 · 보완 175 · 순서 120 · 간격 68 · 대안 36 · 회피 21 · 이전 시술 확인 14 · 비교 4 · 관련 기법 4 · 반복 회차 2 / `same_day`: 빈칸 789 · 가능 77 · 불가 25 · 조건부 13 / `conflict_side`: 채택 29 · 진 쪽(근거로 유지) 49
- `g_adverse.polarity`: 발생함 2,893 · 해당 없음 29 · 보고 없음 1 / `g_contraindication.polarity`: 금기 345 · 해당 없음 5
- `g_package.package_kind`: 메뉴 83 · 고민 패키지 63 · 연간 플랜 58 · 고민 단계 조합 56 · 같은 날 조합 26 · 레시피 19 · 병합 기법 5 · 비교표 조합 2 (패키지 119)
- `g_offer.reach`: 케이스 직접 59 · 시술 직접 44 · 제품 경유 29 · 못 닿음 20 · 제품 — 케이스 없음 8 · product_procedure 3 (상품 122)
- `evidence_kind`(gold 행): 원장 전부, 예외 = `g_profile` 원장 + 외부 확인 231 · `g_scope` 314 · `g_entry` 23(+ 외부 확인만 8) · `g_node` 131

### 1-2. `g_node.node_table` 별 노드 수

| node_table | 노드 |
|---|---:|
| product | 315 |
| procedure_case | 268 |
| concern | 242 |
| adverse | 173 |
| procedure | 138 |
| package | 119 |
| condition | 112 |
| offer | 104 |
| effect | 56 |
| modality | 18 |
| **합** | **1,545** |

`g_node` 는 **엣지 끝이 된 것만** 만든다(`gold/gold-build.py:579-607` — `EDGE_SPEC` 을 돌며 끝을 모음). 그래서 `site` · `material` · `method` · `anatomy` · `tissue` · `mechanism` · `organization` 은 노드가 아니다. 부위는 `g_entry`(site 148 행)와 속성 칸(`g_indication.site_name` · `case_site_name` 등 semantic-map §3-4)에만 있다 → **부위로 들어온 질문은 노드 걷기가 아니라 칸 필터**다.

### 1-3. `g_edge.edge_type` 별 엣지 수(src → dst 노드 종류 쌍)

엣지 방향 규칙(`gold-build.py:567-576`): `g_scope` 엣지는 **holder → subject**(이름 = role, 「자기」 제외), `g_pair` 는 from → to(이름 = question_class), 나머지는 대상 → 값(고민 · 효과 · 부작용 · 조건), 패키지 → 항목, 상품 → 파는 것. `g_indication` 은 `concern_match = 직접` 행만.

| edge_type | 합 | (src → dst) 셈 | gold_table |
|---|---:|---|---|
| 부작용 위험 | 2,835 | product→adverse 1,375 · modality 475 · procedure 469 · procedure_case 387 · package 129 | g_adverse |
| 물려받음 | 1,651 | modality→product 336 · procedure_case→product 332 · procedure→product 309 · modality→procedure_case 268 · procedure→procedure_case 268 · modality→procedure 138 | g_scope |
| 적응 | 1,642 | product→concern 784 · procedure 292 · procedure_case 243 · modality 241 · package 82 | g_indication |
| 효과 | 948 | product→effect 482 · procedure 196 · modality 113 · procedure_case 92 · package 65 | g_outcome |
| 하위 제품 | 663 | product→modality 317 · product→procedure 309 · product→product 37 | g_scope |
| 재시술 간격 | 460 | product→product 339 · procedure_case→procedure_case 50 · procedure→procedure 36 · modality→modality 29 · package→package 4 · package→modality 2 | g_pair |
| 금기 | 345 | modality→condition 309 · procedure 21 · product 15 | g_contraindication |
| 제품 경유 | 332 | product→procedure_case 332 | g_scope |
| 하위 케이스 | 268 | procedure_case→procedure 268 | g_scope |
| 패키지 구성 | 265 | package→modality 145 · procedure 62 · procedure_case 58 | g_package |
| 구성 항목 | 255 | modality→package 144 · procedure_case 58 · procedure 53 | g_scope |
| 보완 | 170 | modality→modality 106 · procedure→modality 17 · modality→procedure 16 · (그 밖 9쌍 31) | g_pair |
| 판매 | 143 | offer→procedure_case 59 · procedure 44 · product 40 | g_offer |
| 하위 시술 | 138 | procedure→modality 138 | g_scope |
| 순서 | 96 | modality→modality 67 · (그 밖 8쌍 29) | g_pair |
| 간격 | 66 | modality→modality 39 · procedure→modality 12 · (그 밖 15) | g_pair |
| 상위 제품 | 37 | product→product 37 | g_scope |
| 대안 | 34 | procedure_case→procedure_case 13 · product→product 11 · (그 밖 10) | g_pair |
| 회피 | 18 | modality→modality 7 · modality→procedure 6 · procedure→modality 3 · procedure_case→modality 2 | g_pair |
| 이전 시술 확인 | 13 | modality→modality 12 · modality→procedure 1 | g_pair |
| 비교 · 관련 기법 · 반복 회차 | 4 · 4 · 2 | — | g_pair |
| **합** | **10,389** | | |

주의: `g_pair` 904 행 중 엣지는 904 가 아니다 — 한 끝이 빈 행(「to 빈칸 = 같은 날 전체 순서의 한 자리」 · semantic-map §2) 37 은 엣지가 안 된다(`gold-build.py:589` `if not (s_t and s_c and d_t and d_c)`). 걷기에서 `g_pair` 를 엣지로만 보면 이 37 행을 놓친다 → **pair 는 엣지가 아니라 표 조회로**.

### 1-4. 근거 경로와 응답에 실을 최소 칸

경로(semantic-map §4 · `semantic-map.md:110-124`):

```
gold 행(g_*.gid | g_node.node_id)
  → g_evidence(gold_table, gold_id) 1..8 행        [중앙 1 · 최대 8]
      → (silver_table, silver_id, fields)
          → silver source_ref(target_table = silver_table · target_id = silver_id · field ∈ fields)
              → ref(원장 JSON 「파일:포인터」 · 외부 확인 URL · 판정 표 줄)
```

셈: gold 행 24,115(`g_evidence`·`g_edge` 제외) 중 근거 없는 행 **0** · gold 행당 참조 최대 8 · 중앙 1 · 참조 하나당 `source_ref` 행 중앙 1 · **최대 557**(행 전체를 가리키는 참조 — 펼침에 쪽 넘김 필요) · 짝 없는 참조 0. `fields` 값: 빈칸 25,929 · `(행 전체)|name|name_ko` 1,756 · `alias` 55.

응답에 실을 최소 칸(추천):

| 층 | 칸 | 이유 |
|---|---|---|
| 응답 머리 | `build`(gold 해시 + 적재 id) | llms.txt §4 방문 기록 `(build, 노드, 관계, …)` · 재현 |
| 행마다 | `gold_table` · `gid` · `evidence_kind` | 앱이 「원장 / 외부 확인」 구분 · 되짚기 시작점 |
| 행마다(물려받음일 때) | `g_scope.role` · `path` (+ `holder_*`) | 「층」 표시 — semantic-map §5 「하위는 이 대상 이름으로 일반화 안 함」 gate 에 필요 |
| 펼칠 때만 | `g_evidence.silver_table` · `silver_id` · `fields` → `source_ref.field` · `ref` | 인용 · 감사. 매 응답에 싣지 않음(557 행 사례) |

산출물 추적성 기준(`para/areas/concept/cs/artifact-traceability.md` 「공통 식별자 · 관계 · 버전」)에 대응: 식별자 = `gid`/`node_id`, 관계 = `g_evidence` · `g_scope.link`, 버전 = gold 해시. **D3 에서 `source_ref` 를 올리지 않으면 관계가 silver 행에서 끊긴다.**

### 1-5. 입구(`g_entry`) — 조회 규칙의 첫 단

- `g_entry.norm` = 공백 연속 제거 + 소문자(`gold-build.py:126` `norm`). 조사 · 오타 처리는 **없다**.
- norm 2,541 개 중 **99 개가 2개 이상 개념**(최대 3). 겹침 짝: material+procedure 40 · adverse+concern 16 · concern+site 13 · concern+condition 8 · modality+procedure 5 · method+procedure 3 · adverse+condition 3 · material+modality 2 · 같은 표 안(procedure_case 2) · offer+procedure_case 2 …
- 겹침 해소 규칙(semantic-map §1 `semantic-map.md:30`): 질문 **범위가 개념을 고른다**(고민 질문 = 고민 · 부작용 질문 = 부작용), 시술 질문에서는 시술 → 케이스 → 제품 → 계열 순(`gold-build.py:629-641` `lookup` 의 `order`). → 범위가 정해지면 대부분 결정론으로 풀린다. 같은 표 안 겹침(procedure_case 2)만 규칙으로 못 가른다.

### 1-6. 조회 규칙 표(semantic-map §5 · §6 요약)

물려받기(`g_scope` · `semantic-map.md:126-143`):

| 묻는 대상 | 물려받음(위 층 진술 적용 — 답에 그대로) | 하위(「하위」 표시 · 이 이름으로 일반화 금지) | 경유 | 금지 |
|---|---|---|---|---|
| 계열 | — | 하위 시술 · 하위 제품(product_modality) | — | — |
| 시술 | 계열 | 하위 케이스 · 하위 제품(케이스 경유 + product_procedure) | — | — |
| 케이스 | 시술 · 계열 | — | 제품 경유(제품 이름 붙여서만) | — |
| 제품 | 케이스 · 시술 · 계열(case_product) / 시술 · 계열(product_procedure) / 계열(product_modality) | 하위 제품(parent_code) | — | **상위 제품 진술 물려받지 않음**(role 상위 제품 37) |
| 패키지 | — | 구성 항목 | — | — |

`g_scope.role` 셈: 물려받음 1,651 · 자기 858 · 하위 제품 663 · 제품 경유 332 · 하위 케이스 268 · 구성 항목 255 · 하위 시술 138 · 상위 제품 37.

표 ↔ 질문 범위(`semantic-map.md:145-156`) + 추가 규칙:

| 범위 | 시작 | 펼침 | 읽을 표 | 붙는 규칙 |
|---|---|---|---|---|
| 시술 | `g_entry`(시술 순서) | `g_scope` 자기 · 물려받음 | `g_profile` · `g_indication`(직접) · `g_outcome` | 하위는 표시만 |
| 부위 · 고민 | `g_entry`(concern) | 고민 3단 — `asked_concern_code` 로 하위 고민 함께 | `g_indication`(+ `g_package` 고민 패키지) | `reach` 「계열 층만」 따로 · 부위는 칸 필터 |
| 부작용 | `g_entry` → 대상 | 자기 · 물려받음 · 하위 케이스 | `g_adverse` · `g_adverse_detail` · `g_recovery` | polarity 「해당 없음」 섞지 않음 · 빈도 수치 ≠ 서술 등급 · 부작용 지속 ≠ 회복 |
| 시술 조합 | 대상 | 자기 · 물려받음 · 하위 케이스 · 하위 시술 | `g_pair`(보완) · `g_package` | 보완 ≠ 같은 날 가능 |
| 동시 가능 | 두 대상 | 양쪽 펼친 뒤 from/to 맞춤 | `g_pair.same_day` · `g_package`(같은 날 조합 — 두 끝이 한 패키지에) | `same_day` 빈칸 = 원문이 말 안 함(≠ 가능) · 엇갈리면 둘 다 |
| 순서 · 간격 | 대상(들) | 같음 | `g_pair`(순서 · 간격 · 재시술 간격 — `self_pair`) | from → to = 먼저 → 나중 · 충돌은 채택/진 쪽 둘 다 |
| 회피 | 대상 / 사람 조건 | 같음 / 조건 3단 | `g_pair`(회피) · `g_contraindication`(polarity 금기) | 시술 간 회피 ≠ 사람 금기 |
| 상품 | `g_entry`(제품 · 시술 · 상품) | 제품은 하위 제품까지(상품만) | `g_offer` | `price_mid_raw` 계산 · 정렬 금지 · 못 닿음 = 원장 확인 |

---

## 2. Q2 — 옛 허브가 읽는 구조(PR #31 · 커밋본 `HEAD` = `2edc190`)

브랜치 `kknaksss/phub-recommend` · `release/v1.2.0` 대비 커밋 21 · 파일 124(+25,018줄). 작업 트리 미커밋 = 수정 8(`mcp_server.py` · `service.py` · `router/gold.py` · `schema/gold.py` · `swagger_docs/gold.py` · 시험 3) + 미추적 2(`app/modules/gold/selected.py` · `tests/test_gold_selected.py`). **건드리지 않았다**(`git show HEAD:` · `git diff` 로만 읽음).

### 2-1. 입력 · 스키마 · 빌드 · 발행

| 무엇 | 옛 꼴 | 근거 |
|---|---|---|
| 입력(ingest) | 실버 · 시맨틱 **JSON 13파일**(`semantic.json` · `step1-products` ~ `step9-explanations`) → 원문 그대로 `gold_source_snapshot`(file · version · sha16 · size · body JSON). `semantic.json inputs{}` 해시 12 와 실물 sha16 이 다르면 빌드 실패 | `HUB/backend/app/modules/gold/inputs.py:1-78` · `application.py:1-4` |
| DB 스키마 | `gold_source_snapshot` · `gold_build`(started/finished · status · input_hashes · build_hash · counts · guards) · `gold_node`(build_id+id PK · kind · name · attrs JSON · flags · gate_status · default_out · source_refs) · `gold_edge`(build_id+id · kind · from_id · to_id · stored · derived_by · inherited_from · attrs · resolved · flags · gate_status · layer · default_out · evidence) · `gold_global` · `gold_fact`(id · owner_id · section · text · flags · state · source · attached_to) · `gold_dictionary`(norm · expr · variants · targets · mode · ambiguous · collision) · `gold_publication` | `HUB/backend/app/model/gold.py:23-156` · alembic `b202610300001_gold_schema.py`(152줄) · `b202610310001_gold_fact_attached.py`(35줄 — `attached_to`) |
| 빌드 | 허브 안에서 규칙 G1~G22: 노드(13종 · 표시 · gate 3값) → 저장 엣지 21종 → 펼친 엣지 → 시술 쌍 · 확인 조건 등급 → 안전 묶음(G13) → facts(section 18) → 사전 + 메뉴 라벨 → 가드 → 빌드 해시 | `build.py:1-6`(1,415줄) · `pairs.py` · `facts.py` · `ids.py` |
| 발행 단위 | 빌드 1 = 가드 통과 시 한 트랜잭션으로 저장 · `gold_publication` 한 줄. 같은 해시면 unchanged · 가드 실패면 rejected(종료 1). 서버는 **시작 때 발행본을 메모리 그래프(`GoldGraph`)로 한 번** 올림 — 발행이 바뀌면 재시작 | `application.py` · `memory.py:1-3` · `docs/gold-local.md` 「순서」 |
| 실행 | `graph_main.py` FastAPI + 골드 MCP `streamable_http_app(stateless, json_response)` 마운트 + 원장 MCP(raw) 마운트 · lifespan 에서 두 session_manager.run() | `HUB/backend/app/graph_main.py:23-82` · 의존 `mcp>=2.3,<3` · `httpx` 추가(`pyproject.toml` diff) |

옛 노드 종류(`tools.py:33`): product · family · site · technique · unit_procedure · package · concern · purpose · combo · check_condition · complication · evidence_statement · evidence_source. 의도 12(`tools.py:37-42` I-01~I-12). fact section 18(`gold-local.md` v3.4).

### 2-2. 도구 전부

MCP 서버 이름 `procedure-hub-gold` · 전부 `readOnlyHint` · meta `anthropic/maxResultSizeChars`(`mcp_server.py:22-30`). REST prefix `/procedure-hub/gold`(`router/gold.py`).

| 번호 | MCP 이름 | REST | 입력 | 출력 꼴 | 읽는 옛 표 · 칸 |
|---|---|---|---|---|---|
| — | (health) | `GET /health` | — | 발행 빌드 · 메모리 셈 · 적재 시간 · 원장 manifest | gold_build · gold_publication |
| T1 | `resolve` | `GET /resolve` | text · kinds? · limit_per_span(20) · sections? · intent? | candidates[](span별) · menu_candidates · 봉투 | gold_dictionary(norm · targets · ambiguous) · `semantic.json dictionary.resolve_rules`(4단계: 완전 → 낱말 나눔(조사 떼기) → 끝말 떼기 → 접두) · 조사 목록 `resolve.py:19` |
| T2 | `recommend` | `POST /recommend` | concerns[] · site · cc · cc_roots · include_conditional · include_not_recommended · sections · limit(10) · intent | 카드[](layer · family_only · more_cards) + 안전 요약 + companion | concern · unit_procedure 노드 · treats 엣지 · site 층 |
| T3 | `procedure_card` | `GET /procedures/{id}` | id · product? · sections? · full · intent | 시술 카드(slim/sections/full) | unit_procedure/product/family 노드 · gold_fact(section) |
| T4 | `pair_check` | `POST /pairs` | procedures[1~6] · prior{procedure, elapsed_days} · sub_condition · include_conditional · sections · intent | resolved 값(같이 · 순서 · 간격) · claims[] · relations[] · self_pair[] · expanded | gold_edge(resolved · FORBID_KINDS) · pairs.UnitSets |
| T5 | `check_conditions` | `GET /procedures/{id}/checks` | id · conditions[] · sections · intent | 조건마다 등급(금기 · 주의 · 확인만 · 확인만(고지)) · by_unit · 대기 기간 | check_condition 노드 · checks fact · 전역 |
| T6 | `compare` | `POST /compare` | procedures[2~4] · sections · intent | 키 칸 · 개요 · 기전 · 운영 · 회복 · 용량 · 안전 셈 · 비교 조합 · relations[] | 노드 attrs · fact · combo(비교) |
| T7 | `combos` | `GET /combos` | concern · purpose · procedure · menu · include_sales_copy · include_not_recommended · sections · intent | combos[](추천 먼저) · reference[] | combo 노드 · menu_labels |
| T8 | `neighbors` | `GET /nodes/{id}/neighbors` | id · edge_kinds[] · direction(both) · depth(≤2) · limit(≤50) · include_conditional · include_derived · sections · intent | nodes[] · edges[] · truncated · counts_by_kind · safety | gold_node · gold_edge(out/in 인접) |
| T9 | `vocab` | `GET /vocab` | kinds[] · sections · intent | vocab{concern · site · purpose · check_condition · technique · family · intent · menu} + enums | 노드 kind 별 목록 · INTENTS |
| T10 | `peek` | `GET /nodes/{id}/peek` | id · include_conditional · intent(무시) | slim 노드 · neighbors_by_kind{n · direction · items[:4]} · sections[]{name · n_facts · bytes} · 안전 요약 | gold_node · gold_edge · section_ids · sections_bytes |
| T11 | `expand` | `POST /nodes/{id}/expand` | id · sections · neighbors(≤255) · neighbor_kinds · fact_ids(≤64) · full · page · include_conditional · intent | facts[]{id · line(40자 cut) · section · owner} · more · by_unit · global_facts · 이웃 slim | gold_fact · gold_global |
| (미커밋) | `selected_pair` | `POST /pairs/selected` | a · b · prior · sub_condition · include_conditional · sections · cursor | claim/대안별 fact id · 원문 · source · 방향 · pair_scope.complete · next_cursor(64 KiB) | gold_edge · gold_fact |
| (미커밋) | `global_claims` | `POST /global-claims` | scope · a · b · condition · cursor | 전역 fact · scope_complete · next_cursor(32 KiB) | gold_global · gold_fact |

모든 응답은 봉투(`tools.py:225` `envelope`): build · request · intent_used · sections_used · index · facts · more · must_show_flags · `claude_contract`(priority · use_first · 「카드 밖 말 금지」).

---

## 3. Q3 — 옛 ↔ 새 대조

### 3-1. 옛 도구마다

| 옛 도구 | 판정 | 새 gold 로 무엇을 | 근거 |
|---|---|---|---|
| T1 resolve | **바꿔야 함** | `g_entry.norm` 완전 일치 + 조사 떼기(옛 `PARTICLES` 목록만 재사용) → 후보 전부(겹침 99). 범위가 오면 semantic-map §1 순서로 정렬. 옛 4단계 중 「끝말 떼기 · 접두」는 옛 `resolve_rules`(semantic.json) 기반이라 근거 없음 — 새로 넣으려면 결정 필요 | §1-5 · `HUB resolve.py:19-22` |
| T2 recommend | **바꿔야 함** | 고민 코드 → `g_indication`(`asked_concern_code`) · `reach` · `concern_match` · 「계열 층만」 분리 · 부위는 `site_name` / `case_site_name` 필터. 옛 cc · cc_roots · purpose · site 층 체계 없음 | semantic-map §5 · `gold-build.py:694-718` |
| T3 procedure_card | **바꿔야 함** | `g_profile` 한 줄 + `g_scope`(층) + facet 셈. 옛 section 18 · fact 체계 없음 | §1-1 |
| T4 pair_check | **바꿔야 함** | 두 끝 `g_scope` 펼침(자기 · 물려받음 · 하위 케이스 · 하위 시술) → `g_pair` from/to 맞춤 → `same_day` · `conflict_*` · `g_package` 같은 날 조합. 옛 「resolved 하나」(값 갈리면 가드 실패) 개념은 새 규칙 「엇갈리면 둘 다」와 반대 | semantic-map §3-1 · `gold-build.py:769-852` |
| T5 check_conditions | **바꿔야 함** | 조건 코드(+하위) → `g_contraindication`(polarity 금기) · 대상은 `g_scope` 펼침. 옛 4등급은 없음 → `level_text` 원문 그대로 | `gold-build.py:855-870` |
| T6 compare | **필요 없음(이번)** | 비교 gold 표 없음 · `g_pair` 「비교」 4 행뿐. 37문항에 비교 질문 없음. 필요하면 profile 두 장을 앱이 나란히 | questions.csv range 분포 |
| T7 combos | **바꿔야 함** | `g_package`(고민 + 상위 고민 · 항목) · `package_kind` | `gold-build.py:916-935` |
| T8 neighbors | **바꿔야 함 → 걷기 핵심 도구** | `g_edge` + `g_node` — 허용 edge_type · 방향 · 쪽 넘김. 응답에 `gold_table`+`gold_id` 를 실어 속성 행으로 되짚기 | §1-3 |
| T9 vocab | **대부분 필요 없음** | 의도 12 · 메뉴 라벨 · purpose 없음. 남길 것 = 범위 8 · edge_type 23 · facet 이름 · `vocabulary.csv` 고정 값(앱 프롬프트 · 검사용) | `notes/vocabulary.csv` |
| T10 peek | **바꿔야 함(축소)** | 노드 한 장 + edge_type 별 이웃 셈 + facet 별 행 셈. section bytes 없음 | — |
| T11 expand | **바꿔야 함** | facet 행 쪽 넘김 + 근거 펼침으로 쪼갬(§6-3 `facets` · `evidence`). 40자 cut 줄 · fact_ids 체계 없음 | — |
| selected_pair(미커밋) | **필요 없음** | pair 도구가 표 조회로 전부 냄(쌍당 행 최대 = Q19 14 행) | §5 표 |
| global_claims(미커밋) | **필요 없음** | 새 gold 에 「전역 scope fact」 없음 | — |

### 3-2. 37문항에 새로 필요한 도구(옛 것에 없던 것)

1. **scope** — 대상 하나의 holder 목록(role · path). 모든 속성 조회의 첫 단. 옛 허브는 빌드 때 펼친 엣지로 숨겼다.
2. **facets** — (노드, facet ∈ profile · indication · outcome · adverse · adverse_detail · recovery · contraindication · offer · package) 를 scope 로 펼쳐 gold 행으로. 층(role · path) 표시 포함.
3. **허용 관계로 이웃 후보** — 질문 범위별 허용 edge_type(§6-4 표)만, 방향 지정, 쪽 넘김. Jev 후보의 유일한 원천(llms.txt §3-1 「존재하지 않는 노드 ID 를 생성하게 하지 않는다」).
4. **evidence** — gold 행 → `g_evidence` → `source_ref` 쪽 넘김(최대 557 행).
5. **pair(두 끝)** — 위 3-1 T4.
6. **역방향 조회** — 조건 → 금기 대상(Q29 · Q30), 고민 → 후보(Q06~Q10). 엣지 방향이 대상 → 값이라 dst 로 묻는 길이 필요.

### 3-3. 배관 재사용 판정

| 배관 | 판정 | 이유 |
|---|---|---|
| 서버 골격(`graph_main.py` FastAPI · lifespan · MCP 마운트 · server-timing 미들웨어) | **틀만 가져간다** | `release/v1.2.0` 에는 `graph_main.py` · MCP 가 없다(`git show release/v1.2.0:backend/app/graph_main.py` → 「not in release/v1.2.0」 · diff 상 `A`). 마운트 · lifespan 패턴(`graph_main.py:29-82`)과 의존(`mcp>=2.3,<3`)은 그대로 쓸 만함 |
| MCP 서버 틀(`mcp_server.py` — `_call` 도메인 예외 → ToolError · READ_ONLY · meta) | **틀만 가져간다** | 도구 정의 문구 · 입력은 전부 옛 체계 |
| REST 라우터 · DI(`container.py` Singleton 상태 + Factory 서비스 · `service.py` 「REST · MCP 공용 코어」) | **틀만 가져간다** | 한 코어를 두 입구가 부르는 구조는 D5 와 맞음 |
| 빌드(`build.py` · `pairs.py` · `facts.py` · `ids.py` · G1~G22 · 가드) | **버린다** | 새 gold 는 이미 `gold-build.py` 가 만들고 `gold-check.py` 가 검사한 CSV. 허브가 다시 빌드할 이유 없음(허브 = 적재만) |
| 적재 · 발행(`inputs.py` sha16 해시 가드 · snapshot · build · publication · 같은 해시 unchanged) | **틀만 가져간다** | 「파일 묶음 해시 → 발행 1 → 서버 시작 시 메모리」 구조 재사용. 입력 목록 · 대조 해시만 새 gold(CSV 15 + source_ref)로 |
| 메모리 그래프(`memory.py` — dict · out/in 인접 · norm 색인) | **틀만 가져간다** | 새 표 색인(scope by subject · edge out/in · entry by norm · evidence by gold 행)으로 다시 씀 |
| resolve(조사 떼기) | **목록만 가져간다** | `PARTICLES`(`resolve.py:19`) 는 데이터 무관. 정규화는 새 gold 의 `norm` 과 **같은 식**이어야 일치(옛 NFKC · 괄호 지움 등은 새 `g_entry.norm` 과 다름) |
| 봉투(envelope · claude_contract · companion · intent · sections · must_show_flags) | **버린다** | 옛 fact/section/intent 에 묶임. 새 응답 머리는 build · request · rows · cursor 정도 |
| 시험 틀(pytest · sqlite 인메모리 · `GOLD_INPUT_DIR` 없으면 건너뜀) | **틀만 가져간다** | 시험 38개 파일은 옛 데이터 기대값 — 버림. 「실물 데이터는 로컬 경로 env 로, 없으면 skip」 규칙은 공개 데이터 금지에 맞음 |
| 스크립트(`gold_ingest` · `gold_build` · `gold_publish` · `gold_export` · `_gold_cli` · `_gold_client`) | **ingest/publish 만 틀** | quality_eval · e2e · speed 는 옛 문항 · 옛 도구에 묶임 |
| 원장 MCP(raw · manifest) | **확인 안 됨(이번 범위 밖)** | 새 설계에서 원장 직접 조회가 필요한지는 이 조사 범위 밖. WORK.md §4 「런타임 임의 대체 조회는 계획에 포함하지 않는다」 |

---

## 4. Q4 — 앱(clinic_chat · hub-evals) 배관

브랜치 `kknaksss/hub-evals` · HEAD `078ac99`. 미커밋 = 수정 16(case3 · loop · hub_rest · config · llm/cli · report · rerun_report · runner · timing · verify_runs · prompts/case3.md · 시험 5) + 미추적(`calibration_prep.py` · `cases/answer_contract.py` · `cases/relation_adapter.py` · `cases/semantic_candidate.py` · `claim_policy_eval.py` · 시험 다수). case3.py 커밋본 1,411줄 → 작업 트리 4,471줄. **건드리지 않았다.**

### 4-1. 구조

| 부분 | 파일 | 무엇 |
|---|---|---|
| Jev 클라이언트 | `clients/jev_client.py`(33줄 · 커밋본) | `typesafe_sdk.AsyncTypeSafeClient` · 모델 고정 · timeout 10초 · `CHOICE_MAX = 255` · `choice_stats`(p_max · 1/2위 비) |
| 허브 클라이언트 | `clients/hub_mcp.py`(MCP Python SDK `ClientSession` + streamable_http · mcp 2.3) · `clients/hub_rest.py` | case1 · 2 는 MCP 도구 루프, case3 걷기는 REST |
| LLM | `clients/anthropic_client.py`(SDK · Sonnet 스트림 · thinking between_tools · effort high · max 8000) · `llm/cli.py`(676줄 · `claude -p` stream-json / `codex exec --json` · 격리 · API 키 지운 자식 env · 구독 확인) | 세 갈래 같은 조건 |
| 도구 루프 | `cases/loop.py` | case1 · 2: Sonnet → tool_use → MCP → … end_turn · 상한 시 tool_choice none |
| 걷기 | `cases/case3.py` | 아래 4-2 |
| 기록 | `runs.py` · `timing.py` · `pricing.py` · `verify_runs.py` · `report.py` | `RUNS_DIR/runs.jsonl` 한 질문 한 줄(고치지 않음) · `human_checks.jsonl` · `quality.jsonl` · 단계별 ms · 토큰 · 비용 · 걷기 trace(jev_calls · hub_calls · …) |
| 평가 | `quality/judge.py`(Opus 채점) · `word_check.py` · `raw_mcp.py` | ① 단어 검사 ② 채점 |

### 4-2. llms.txt 패턴 대조

| llms.txt 요구(`para/resources/note/ai/llms.txt`) | 커밋본(HEAD) | 미커밋(WP-10) |
|---|---|---|
| §2 여러 후보 관련성 = 후보마다 Noul, 한 요청 | **어긋남** — 걷기 `walk_pick` 이 Choice `pick` 하나 + 선택지마다 짝 Noul `also:*` + Noul `enough`(HEAD `case3.py:603-643`). 첫 걸음도 Choice `nb` · `sec` · `kind`(HEAD `:702-747`). 「여러 개 펼치기」를 Choice 로 함 | **맞음** — `_frontier_choice`(작업 트리 `case3.py:1714-1781`): 후보마다 `candidate_{i}` Noul + `answer_ready` Noul 을 같은 `system_one` 에 · 32개 묶음으로 **전부** 평가 |
| §2 Choice 는 하나만 고를 때 | 의도 Choice 12 · 시작 노드 Choice(HEAD `:106-122`) — 하나 고르기라 허용 범위 | 의도 Choice · `question_focus` Choice · `start` Choice(작업 트리 `:2449-2459`) — 같음 |
| §3-1 후보는 허용 관계에서만 · ID 생성 금지 | 후보 = 허브 peek 이웃(허브가 낸 것만) — 맞음 | 후보 검사 `invalid_frontier_candidates`(build · node_kind · name 확인 · `:1721-1723`) — 맞음 |
| §3-2 state 에 question · required · verified · unresolved · candidates | state = 질문 문자열만(HEAD `:296` `state=question`) — **어긋남** | state JSON = question · intent · build · facets · verified · unresolved · candidates(`:1733-1738`) — 맞음 |
| §3-4 answer_ready 는 종료 **제안**, 앱이 검증 | `enough` Noul 로 멈춤(fact ≥ 1 이면 enough) — **어긋남** | `stop_answer` 는 ready ≥ 0.7 이고 보류 후보 없음일 때만, 아니면 `stop_incomplete` · 이후 answer_contract 검사 다수(`_missing_relevant_safety` · `_absence_invalid` · `_coverage_answer_failures` …) — 맞음 |
| §4 명시 대상 · 필수 안전을 낮은 점수로 빼지 않음 | 확인 안 됨(안전 예산 별도 — 커밋 `1d0e4ae` 메시지) | `required` 후보는 Noul 무시하고 selected(`:1760-1762` `app_required_target_overrides_noul`) — 맞음 |
| §4 선택 안 한 후보 · 불확실 · 이유 기록 | 확인 안 됨 | `frontier_choices[].decisions{noul · status · reason · yes_at · no_at}` · `answer_ready_noul` · options(`:1776-1780`) — 맞음 |
| §1 임계값은 평가로 | — | `yes_at 0.7 · no_at 0.3` **하드코딩**(`:1724`) — 보정 전 값. `calibration_prep.py`(미추적)가 보정 준비로 보임(내용 확인 안 함) |
| §4 실제 model id 기록 · 버전 고정 | 모델 고정 설정(`jev_client.py` `typesafe_default_model`) | 같음 · 단계별 토큰 · 비용 기록(`_jev` `:1700-1710`) |
| (기타) | 255 넘으면 Choice 2단(종류 → 안) | 옛 `walk_pick` · `walk_pick_first` 가 작업 트리에 **아직 남아** 있음(`:1794` · `:1893` 호출 `:2509` · `:2581`) — 경로가 둘 |

### 4-3. 새 앱에 가져갈 것 / 버릴 것

| 가져갈 것 | 이유 |
|---|---|
| `jev_client.py` 통째 | 데이터 무관 · 33줄 |
| `hub_mcp.py` · `hub_rest.py` 의 연결 틀 | mcp 2.x import 경로 확인이 이미 끝남(`hub_mcp.py` docstring) · 도구 이름 · 응답 꼴만 바꿈 |
| `anthropic_client.py` · `llm/cli.py`(+`cli_process` · `auth`) | D8 결정 따라 하나 또는 둘 |
| `runs.py` · `timing.py` · `pricing.py` 의 기록 틀 | 「한 질문 한 줄 · 고치지 않음」 · 단계 ms · 비용 |
| `_frontier_choice` 의 **꼴**(Noul fan-out + answer_ready · 묶음 · 결정 기록 · required 우선) | llms.txt §3 과 맞는 유일한 구현. 후보 · facet 꼴은 새 gold 로 다시 씀 |
| 시험 틀(`tests/fake_jev.py` · 모의 허브 · `mock_server`) | 키 · 허브 없이 돌리는 판 |

| 버릴 것 | 이유 |
|---|---|
| `case3.py` 걷기 본체(peek · expand · section · intent 12 · 안전 예산 · walk_order.json · walk_cover34.json) | 옛 허브 꼴에 묶임 |
| Choice 반복 걷기(`walk_pick` · `walk_pick_first`) | WP-10 정정으로 폐기된 꼴 |
| `answer_contract.py` 등 미추적 검사기 | 옛 fact id · section · public context 계약에 묶임 — **검사 항목 목록(부재 주장 · 인용 범위 · 안전 누락)은 새 hard gate 설계의 참고로만** |
| case1(원장 MCP) | 이번 범위 아님(확인 안 됨 — 비교 기준선이 필요하면 D 로) |

---

## 5. Q5 — 질문 37 × 걷기

### 5-1. 셈 방법

`q5.py` 가 `gold-build.py` 의 `QUESTIONS`(ast 로 읽음 · 실행 안 함)와 같은 규칙(입구 순서 · `g_scope` role 묶음 · 필터)으로 gold 를 직접 센다. 「입구 겹침」 = 그 입구 낱말 norm 의 개념 수(범위 거르기 전). 「후보」 = Jev 에 넘길 다음 노드 / 행의 서로 다른 수.

### 5-2. 질문마다

범례: **엣지**(새 gold edge_type 또는 표 조회) · **Jev** = 그 질문에서 Jev 가 할 판단 · **gate** = 앱이 점수와 무관하게 막거나 반드시 실을 것.

| id | 범위 | 시작(코드) | 입구 겹침 | 거칠 엣지 · 표 | 읽을 gold 표 | 후보 셈(실제 gold) | Jev 판단 지점 | 앱 hard gate | 상태 |
|---|---|---|---:|---|---|---|---|---|---|
| Q01 | 시술 | procedure:PRC-001 | 3 | scope 물려받음 → 적응 · 효과 | g_entry · g_profile · g_scope · g_indication · g_outcome | holder 2 · 행 67 · 고민 41 · 효과 12 · 하위 43 | 범위 Choice · facet Noul(고민/효과 41+12) | 하위는 일반화 금지 · 층 표시 | 답함 |
| Q02 | 시술 | product:PRD-400 | 1 | scope(제품 → 케이스 · 시술 · 계열) → 적응 · 효과 | 같음 | holder 4 · 행 49 · 고민 22 · 효과 11 | 범위 Choice · facet Noul | 제품 층 진술은 제품 이름 붙여서 | 답함 |
| Q03 | 시술 | procedure_case:CAS-016 | 1 | scope(케이스 → 시술 · 계열) | g_entry · g_profile · g_scope | holder 3 · 행 75 · 고민 45 · 효과 13 | 범위 Choice | 케이스 ≠ 시술 정체 | 답함 |
| Q04 | 시술 | product:PRD-150 | 1 | scope → 적응 · 효과 | 같음 + 성분(`g_profile.materials`) | holder 2 · 행 46 · 고민 35 · 효과 6 · 하위 3 | 범위 Choice · facet Noul | **상위 제품 진술을 하위 제품에 주지 않음**(PRD-150 은 제품 계열) | 답함 |
| Q05 | 시술 | procedure_case:CAS-021 | 2 | scope | g_entry · g_profile · g_scope | holder 3 · 행 72 · 고민 38 · 효과 8 | 입구 겹침(케이스 2) — 범위 규칙으로 해소 · facet Noul | — | 답함 |
| Q06 | 부위·고민 | concern:CON-005 | 1 | 고민 ← 적응(역방향) | g_entry · g_indication | 행 54 · 시술 5 · 후보 19 · 계열 층만 4 | 후보 Noul 19 | 「계열 층만」 을 시술로 쓰지 않음 · 부위 역할 구분 | 답함 |
| Q07 | 부위·고민 | concern:CON-068 | 1 | 같음 | 같음 | 행 77 · 시술 9 · 후보 43 · 계열 층만 4 | 후보 Noul 43 | 사람 조건(`conditions`) 함께 | 답함 |
| Q08 | 부위·고민 | concern:CON-001 | 1 | 같음 + 고민 3단 | 같음 | 행 524 · 시술 50 · **후보 130** · 계열 층만 9 | 후보 Noul 130(묶음 5) | 직접 / 하위 고민 구분 | 답함 |
| Q09 | 부위·고민 | concern:CON-028 | 1 | 같음 | 같음 | 행 7 · 시술 4 · 후보 7 | 후보 Noul 7 | — | 답함 |
| Q10 | 부위·고민 | concern:CON-012 | 1 | 같음 | 같음 | **행 0** | (후보 없음) | 「정보 없음」 아니라 「원천 미확정」(LCK-010) | 원장 확인 |
| Q11 | 부작용 | procedure:PRC-001 | 3 | scope(자기 · 물려받음 · 하위 케이스) → 부작용 위험 | g_entry · g_scope · g_adverse | holder 24 · 행 147 · 사건 54 · 상위 사건 9 · detail 143 | 사건 Noul 54(또는 상위 9 먼저) | 빈도 수치 ≠ 서술 등급 · polarity 해당 없음 분리 | 답함 |
| Q12 | 부작용 | procedure:PRC-100 | 1 | 같음 + 사건 필터 | + g_adverse_detail | holder 17 · 행 4 · 사건 1 · detail 24 | 거의 없음(결정론) | 발현 ≠ 지속 · 원문 없으면 「silver 빈칸」 | silver 빈칸 |
| Q13 | 부작용 | procedure:PRC-001 | 3 | 같음 + 사건 필터 | g_adverse | holder 24 · 행 5 · 사건 1 | 결정론 | 발생 자리 ≠ 시술 자리 | 답함 |
| Q14 | 부작용 | procedure_case:CAS-021 | 2 | 같음 | g_adverse | holder 3 · 행 8 · 사건 1 · detail 36 | 결정론 | 층(케이스 → 시술 → 계열) 표시 | 답함 |
| Q15 | 시술 조합 | procedure:PRC-001 | 3 | scope → 보완 | g_scope · g_pair | holder 24 · 행 33 · 상대 끝 13 · same_day 채움 16 | 상대 끝 Noul 13 | **보완 ≠ 같은 날 가능** | 답함 |
| Q16 | 시술 조합 | product:PRD-400 | 1 | 같음 | 같음 | holder 4 · 행 28 · 상대 끝 12 | 상대 끝 Noul 12 | 같음 | 답함 |
| Q17 | 시술 조합 | concern:CON-068 | 1 | 고민(+상위) → 패키지 | g_entry · g_package | 행 4 · 패키지 2 | 패키지 Noul 2(또는 결정론) | 패키지 ≠ 상품 | 답함 |
| Q18 | 시술 조합 | modality:M4 + procedure:PRC-116 | 1/2 | 두 끝 scope → 보완 | g_pair | holder 11 · 행 2 | 결정론 | 방향 무관 | 답함 |
| Q19 | 동시 가능 | procedure:PRC-001 + modality:M2 | 3/1 | 두 끝 → 간격 · 회피 · 보완 · 순서 + 같은 날 조합 | g_pair · g_package | holder 28 · 행 14 · same_day 6 · **충돌 5** | 결정론(쌍 고정) | same_day 빈칸 ≠ 가능 · 엇갈리면 둘 다 · 충돌 채택/진 쪽 | 답함 |
| Q20 | 동시 가능 | modality:M8 + modality:M2 | 2/1 | 같음(회피 · 간격) | g_pair | holder 11 · 행 7 · same_day 4 · 충돌 2 | 결정론 | 같음 | 답함 |
| Q21 | 동시 가능 | product:PRD-400 + modality:M4 | 1/1 | 같음 + 패키지 | g_pair · g_package | holder 11 · 행 13 · **same_day 0** · 충돌 7 | 결정론 | same_day 0 → 「원문이 말하지 않음」 이어야(가능으로 말하면 안 됨) | 답함 |
| Q22 | 동시 가능 | modality:M7 + procedure:PRC-001 | 1/3 | 같음 | g_pair | holder 36 · 행 3 · same_day 2 | 결정론 | 같음 | 답함 |
| Q23 | 순서·간격 | modality:M2 + procedure:PRC-001 | 1/3 | 순서 | g_pair | holder 28 · 행 3 · 충돌 3 | 결정론 | from → to = 먼저 → 나중 · 충돌 둘 다 | 답함 |
| Q24 | 순서·간격 | procedure:PRC-001 | 3 | 재시술 간격(self) | g_pair | holder 24 · 행 14 · 상대 끝 8 · 충돌 8 | 층 고르기 Noul 8(또는 전부) | 재시술 ≠ 시술 사이 간격 | 답함 |
| Q25 | 순서·간격 | modality:M2 + modality:M8 | 1/2 | 간격 · 회피 | g_pair | holder 11 · 행 7 · 충돌 2 | 결정론 | 충돌 채택 행 우선 표시 | 답함 |
| Q26 | 순서·간격 | product:PRD-416 | 1 | 재시술 간격(self) | g_pair | holder 4 · 행 1 | 결정론 | 제품 층 | 답함 |
| Q27 | 회피 | modality:M8 | 2 | 회피 | g_pair | holder 7 · 행 7 · 상대 끝 5 | 상대 끝 Noul 5 | 회피 ≠ 사람 금기 | 답함 |
| Q28 | 회피 | modality:M7 | 1 | 회피 | g_pair | holder 12 · 행 9 · 상대 끝 3 | 상대 끝 Noul 3 | 같음 | 답함 |
| Q29 | 회피 | condition:CND-002 | 1 | 조건(+하위) ← 금기(역방향) | g_entry · g_contraindication | 행 30 · 대상 23 | 대상 Noul 23(또는 전부 실음) | **금기는 점수로 빼지 않음** — 전부 | 답함 |
| Q30 | 회피 | condition:CND-094 + modality:M8 | 1 | 같음 + 대상 scope | g_entry · g_scope · g_contraindication | 행 1 · 대상 1 | 결정론 | 기간 · 기준 시점(`period_from`) | 답함 |
| Q31 | 상품 | product:PRD-417 | 1 | 판매(역방향) | g_entry · g_offer | 상품 2 | 결정론 | `price_mid_raw` 쓰지 않음 | 답함 |
| Q32 | 상품 | procedure:PRC-001 | 3 | 판매(시술 코드) | g_offer | 상품 10 | 상품 Noul 10(또는 전부) | 같음 | 답함 |
| Q33 | 상품 | offer(이름 부분 일치) | — | 상품 → 파는 것 | g_offer | 상품 1 · 못 닿음 1 | 결정론 | 못 닿음 = 원장 확인(LCK-308) | 원장 확인 |
| Q34 | 상품 | product:PRD-150 | 1 | 판매 + 하위 제품 | g_entry · g_offer | 상품 2 | 결정론 | 상품 질문만 하위 제품 상품 모음 | 답함 |
| Q35 | 부작용 | procedure:PRC-001 | 3 | scope → 회복 + 부작용 지속 | g_scope · g_recovery · g_adverse | holder 2 · 회복 2 · 부작용 지속 13 | 결정론 | **회복 ≠ 부작용 지속** | 답함 |
| Q36 | 동시 가능 | modality:M4 + procedure:PRC-116 | 1/2 | 전 갈래 · same_day 만 | g_scope · g_pair · g_package | holder 11 · 행 2 · same_day 2 | 결정론 | same_day 원문 조각과 함께 | 답함 |
| Q37 | 시술 조합 | product:PRD-002 | 1 | scope(product_procedure) → 보완 | g_entry · g_scope · g_pair | holder 3 · 행 30 · 상대 끝 10 · same_day 13 | 상대 끝 Noul 10 | 보완 ≠ 같은 날 | 답함 |

상태 셈: 답함 34 · 원장 확인 2 · silver 빈칸 1(`questions.csv.status` · gold-check Q1 줄과 같음).

**255 판정**:
- 질문 경로에서 Jev 에 넘길 후보 최대 = Q08 130(고민 → 후보), 그 밖 54 이하. **255 넘는 곳 없음.**
- gold 전체 노드 기준(`deg.py`): 나가는 방향은 전부 ≤ 156(계열 → 물려받음). **들어오는 방향만** 넘음 — `adverse` ← 부작용 위험 최대 379(2 노드 > 255) · 한 계열 노드의 전체 이웃(양방향 · 모든 엣지) 263(1 노드). 고민 → `g_indication` 후보 최대 130(`>255` 0) · 행 최대 524(3 고민이 > 255 행 — 서로 다른 후보는 130 이하).
- → Noul fan-out 은 선택지 한도가 없으므로 255 는 Choice 를 쓸 때만 문제(D12).

**Jev 판단 지점 정리**: 범위(8) Choice 는 37 모두 1번. 후보 Noul fan-out 이 의미 있는 질문 = Q01 · Q02 · Q04~Q09 · Q11 · Q15 · Q16 · Q24 · Q27~Q29 · Q32 · Q37(≈ 18). 나머지 ≈ 19 는 두 끝이 정해진 결정론 조회라 Jev 걸음이 필요 없다(answer_ready 만).

### 5-3. 시험 세트 추천(추천만)

37 은 gold 시범용이라 다음을 거의 안 건드린다. 더할 묶음(각 1~2문항 · 약 12):

| 묶음 | 왜 | gold 에서 셀 근거 |
|---|---|---|
| 조사 붙은 입력 | `g_entry.norm` 에 조사 처리 없음 → resolve 조사 떼기 시험 | §1-5 |
| 띄어쓰기 · 대소문자 변형 | norm 이 처리 — 회귀 확인 | 같음 |
| 오타 | **지금 gold 로 풀 길 없음**(접두 · 편집 거리 없음) → 「입구 없음」 종료 상태 시험 | 같음 |
| 입구 겹침(재료 · 시술 / 고민 · 부작용 / 고민 · 부위) | 99 norm · 범위 규칙 시험 | §1-5 짝 셈 |
| 두 시술 · 세 시술 한 질문 | pair 두 끝 펼침 · 세 끝은 37 에 없음 | — |
| 해당 없음(gold 에 없는 시술 이름) | 「정보 없음」 vs 「입구 없음」 구분 | — |
| 원장 확인 상태(Q10 · Q33 말고 다른 LCK) | 원천 미확정 종료 | `notes/ledger-check-list.csv` |
| 역방향 큰 후보(이 부작용이 나는 시술은?) | 379 후보 fan-out(D12) | §5-2 255 판정 |
| 같은 날 빈칸 쌍(보완만 있고 `same_day` 빈칸) | 「가능」 으로 말하면 FAIL 이어야 | 보완 175 중 빈칸 119(gold-final-notes:22) |
| 같은 쌍 값 엇갈림(가능 · 조건부) | 「둘 다 보여 줌」 시험 | semantic-map §3-1 |
| 하위 제품 상품 · 상위 제품 진술 | 물려받기 금지 시험 | semantic-map §5 · K7 |
| 사람 조건 + 시술 (Q30 꼴 하나 더) | 금기 gate | — |

---

## 6. Q6 — 연결 설계 선택지

### 6-1. 허브 자리(D1)

| 선택지 | 추천 | 근거 | 위험 |
|---|---|---|---|
| (a) `release/v1.2.0` 새 브랜치 · 새 모듈(예: `backend/app/modules/<새 이름>/` · 별도 진입점) | **추천** | release/v1.2.0 에 MCP · graph_main 없음 → PR #31 에서 틀만 옮김(§3-3). 옛 gold 테이블 · 코드와 섞이지 않음 | PR #31 의 공용 파일(`model/__init__.py` · `pyproject.toml` · `.gitignore`)을 다시 손대야 함. 실험용이라 회사 레포 머지 안 함(_RESUME 11-16 「실험용이라 회사 레포에 머지 안 함」 — 이번에도 같은지 확인 필요) |
| (b) PR #31 브랜치 위 | 비추천 | 이어 쓰기 금지(브리프 §1) · 미커밋 8파일 얽힘 | 옛 gold 와 이름 · 테이블 충돌 |
| (c) 허브 밖 소형 서비스 | 비추천 | 「질문 → 허브(결정론)」 런타임 구조와 어긋남 | 두 번 옮김 |

### 6-2. 저장 · 적재 · 버전(D2 · D3)

표 → DB 대응(D2 (a) 일 때 · 칸은 CSV 헤더 그대로 · 모든 표에 `build_id` FK + 원래 키 = PK):

| gold 표 | DB 테이블(이름 예) | PK | 색인(조회 경로) |
|---|---|---|---|
| g_entry | gold2_entry | build_id, gid | norm · (entity_table, entity_code) |
| g_scope | gold2_scope | build_id, gid | (subject_table, subject_code, role) · (holder_table, holder_code) |
| g_profile | gold2_profile | build_id, gid | (subject_table, subject_code) 유일 |
| g_indication | gold2_indication | build_id, gid | asked_concern_code · (target_table, target_code) · procedure_code |
| g_outcome · g_adverse · g_recovery · g_contraindication | 각각 | build_id, gid | (target_table, target_code) · 값 코드(effect · adverse · condition) |
| g_adverse_detail | gold2_adverse_detail | build_id, gid | adverse_risk_id |
| g_pair | gold2_pair | build_id, gid | (from_table, from_code) · (to_table, to_code) · question_class |
| g_package | gold2_package | build_id, gid | package_id · concern_code · (item_table, item_code) |
| g_offer | gold2_offer | build_id, gid | offer_id · (item_table, item_code) · procedure_code |
| g_node · g_edge | gold2_node · gold2_edge | build_id, node_id / edge_id | src · dst · edge_type |
| g_evidence | gold2_evidence | build_id, gold_table, gold_id, silver_table, silver_id | (gold_table, gold_id) |
| silver source_ref(D3) | gold2_source_ref | build_id, 행 순번 | (target_table, target_id) |
| (발행) | gold2_build · gold2_publication | — | 파일별 sha256 · gold 해시(gold-check Q1 줄 값) · 행 수 |

- 적재: **gold CSV 그대로 ingest**(BOM UTF-8 · 칸 텍스트) — 값 변환 없이(gold 값 = silver 값 · K4). 숫자 칸(`*_min` · `price_*`)도 문자열로 두면 「원문 그대로」 보장이 쉬움(정렬 · 계산은 앱 몫이 아님 · semantic-map §3-6).
- 버전/해시: 적재 전 `gold-check.py` PASS 를 조건으로 할지(정할 것 아님 — 추천: 적재 스크립트가 gold 해시를 기록만, 검사는 gold 쪽 책임). 옛 「같은 해시면 unchanged」 그대로.
- `questions.csv` 는 허브에 올리지 않음(앱 시험 세트).
- 데이터는 로컬 전용(kknaks_profile 은 PUBLIC · silver-model gitignore · 허브 레포에도 CSV 커밋 금지 — 경로 env).

### 6-3. MCP 도구 최소 집합 초안(D4)

모든 응답 머리: `build{gold_hash, build_id}` · `request` · `cursor?`. 모든 행: `gold_table` · `gid` · `evidence_kind`(+ 물려받았으면 `layer{role, path, holder}`).

| # | 이름 | 입력 | 출력 | 읽는 표 | 근거 실림 |
|---|---|---|---|---|---|
| 1 | `resolve` | text · range?(8 범위) | candidates[]{entity_table · entity_code · name · name_kind · matched(norm · 조사 뗌 여부)} · ambiguous | g_entry | gid · evidence_kind |
| 2 | `scope` | table · code · roles? | holders[]{holder_table · holder_code · holder_name · role · path} | g_scope | gid |
| 3 | `neighbors` | node_id · edge_types[] · direction(out/in) · cursor · limit | items[]{node_id · label · node_table · edge_type · gold_table · gold_id} · counts_by_type · truncated | g_edge · g_node | gold_id(속성 행으로) |
| 4 | `facets` | node_id(table:code) · facet · roles?(기본 = 범위별 §1-6) · filters?(adverse_code · site · polarity …) · cursor | rows[](그 gold 표 행 그대로) · counts | g_profile · g_indication · g_outcome · g_adverse · g_adverse_detail · g_recovery · g_contraindication · g_offer · g_package + g_scope | 행마다 gid · layer |
| 5 | `concern_candidates` | concern_code · site? · cursor | groups[]{candidate_table · candidate_code · procedure_code · reach[] · concern_match · rows(gid)} · modality_only[] | g_indication | gid |
| 6 | `pair` | a(node) · b?(node) · classes[] · same_day_only? | rows[](g_pair 그대로 · conflict) · same_day_packages[] | g_scope · g_pair · g_package | gid |
| 7 | `evidence` | gold_table · gold_id · cursor | refs[]{silver_table · silver_id · fields · evidence_kind · source_refs[]{field · ref}} | g_evidence · source_ref | (이게 근거) |
| 8 | `health` | — | build · 행 수 · 적재 시각 | 발행 | — |

역방향(조건 → 금기 대상 · 상품 → 파는 것)은 `neighbors(direction=in)` 또는 `facets` 의 필터로 닫힌다. 37문항 × 「읽을 gold 표」 열이 전부 위 8개 안에 있음(§5-2).

### 6-4. 앱 — Jev + LLM 걷기 루프 초안(llms.txt §3 그대로)

```
0  질문 → resolve(입구 후보 · 겹침)                            [허브]
1  Jev system_one: range Choice(8) + (겹침이 규칙으로 안 풀릴 때만) entity Choice   [하나 고르기]
2  앱: 범위 → 시작 노드 · 필수 facet(required) · 허용 edge_type · 허용 scope role 확정
       (아래 표) — Jev 가 바꾸지 못함
3  허브: scope + facets/pair/concern_candidates 로 1홉 후보 · facet 행
4  Jev system_one: 후보마다 Noul(「unresolved 의 어느 항목을 채우나」) + answer_ready Noul
       — 같은 요청 · 32개 묶음 · 후보 = 3 에서 받은 것만 · state = {question, range, required, verified, unresolved, candidates}
5  앱: noul ≥ yes → 펼침 · ≤ no → 기록하고 보류 · 사이 → 보류(불확실) · required/gate 대상은 점수 무시하고 포함
6  앱: 펼친 노드의 facet 행 읽기 → verified 갱신(gid · evidence_kind · layer) · 방문 장부 (build, 노드, edge_type, facet, cursor)
7  answer_ready 가 yes 이고 보류 0 이면 종료 제안 → 앱 hard gate 검사 → 통과면 종료
8  LLM: verified 행만 넣고 답 생성 · 인용은 gid → (요청 시) evidence 펼침
```

범위별 허용(앱 고정 · Jev 는 이 안에서만 판단):

| 범위 | 시작 | 허용 edge_type / 표 | scope role | 필수 facet(예) |
|---|---|---|---|---|
| 시술 | 시술 · 케이스 · 제품 · 계열 | 적응 · 효과(out) · 하위 *(표시만) | 자기 · 물려받음 | profile · indication · outcome |
| 부위·고민 | 고민 | 적응(in) · 패키지 구성 | — | indication(reach) |
| 부작용 | 대상 | 부작용 위험 · (회복 표) | 자기 · 물려받음 · 하위 케이스 | adverse(+detail) · polarity |
| 시술 조합 | 대상 / 고민 | 보완 · 패키지 구성 | + 하위 시술 | pair(보완) |
| 동시 가능 | 두 대상 | g_pair 전 갈래 · 패키지(같은 날 조합) | + 하위 시술 | pair.same_day |
| 순서·간격 | 대상(들) | 순서 · 간격 · 재시술 간격 | 같음 | pair |
| 회피 | 대상 / 조건 | 회피 · 금기(in) | 같음 | pair(회피) · contraindication |
| 상품 | 제품 · 시술 · 상품 | 판매 · 하위 제품(상품만) | — | offer |

앱 hard gate(점수로 빼면 안 되는 것 — semantic-map §3 · §5 에서):
1. 금기(`g_contraindication` polarity 금기) · 회피(`g_pair` 회피) 행은 그 범위에서 닿으면 전부 실음.
2. `same_day` 빈칸을 「가능」 으로 말하지 않음 · 보완 ≠ 같은 날.
3. 같은 쌍 엇갈림 · 충돌(`conflict_side` 진 쪽 포함)은 둘 다.
4. 하위(role 하위 *)를 이 대상 이름으로 일반화하지 않음 · 상위 제품 진술 물려받지 않음.
5. `polarity` 해당 없음 · 보고 없음을 부작용 목록에 섞지 않음 · 빈도 수치 ≠ 서술 등급 · 부작용 지속 ≠ 회복.
6. `price_mid_raw` 계산 · 정렬 금지.
7. 명시 대상(질문이 이름 댄 노드)은 Noul 과 무관하게 포함(WP-10 `required` 와 같음).
8. 임상 진술은 「원장 진술」(semantic-map §3-5 — 검증 안 됨) 표시를 답이 지움 없이.

### 6-5. 종료 상태 · 기록

| 종료 | 조건(앱이 판정) | 답 |
|---|---|---|
| 근거 충족 | required facet 전부 verified · gate 통과 · answer_ready yes · 보류 0 | 답 생성 |
| 후보 소진 | 허용 관계의 미방문 후보 0 · required 일부 미충족 | 지원된 범위만 답 + 미충족 명시 |
| 원천 미확정 | 입구는 있으나 행 0 이고 LCK 가 있음(Q10 · Q33) 또는 silver 빈칸(Q12) | 「원장 확인 필요」 · 「원문 없음」 — 「정보 없음」 과 구분 |
| 실행 중단 | Jev/허브 오류 · 시간 초과 · build 불일치 | 미완료 — 답 없음 또는 부분 + 사유 |
| (입구 없음) | resolve 후보 0 | 되묻기 — 5-3 오타 · 해당 없음 시험 |

기록(질문 한 줄 · 옛 `runs.jsonl` 틀): build(gold 해시) · Jev model id · 범위 Choice 확률 전부 · 걸음마다 후보 목록(노드 · edge_type · 순서/seed) · 후보별 noul · 결정(selected / not_required / uncertain / gate_forced)과 이유 · answer_ready 값 · 방문 장부 · verified gid 목록 · gate 결과 · 종료 상태 · LLM 입력 바이트 · 답의 인용 gid · 단계 ms · 토큰 · 비용.

---

## 부록 A. 셈 스크립트(scratchpad · 읽기만)

```python
# q1.py — 표 행 수 · 노드 · 엣지 · 근거 · scope · entry (발췌)
import csv,collections,glob,os,sys; G=sys.argv[1]
rd=lambda n: list(csv.DictReader(open(os.path.join(G,n),encoding='utf-8-sig')))
n=rd('g_node.csv'); nt={x['node_id']:x['node_table'] for x in n}
print(collections.Counter(x['node_table'] for x in n))
e=rd('g_edge.csv'); print(collections.Counter((x['edge_type'],nt[x['src']],nt[x['dst']]) for x in e))
en=rd('g_entry.csv'); nm=collections.defaultdict(set)
for x in en: nm[x['norm']].add((x['entity_table'],x['entity_code']))
print(len(nm), sum(len(v)>1 for v in nm.values()))
```

```python
# deg.py — 노드별 이웃 수(엣지 종류 · 방향) (발췌)
out=collections.defaultdict(set); inn=collections.defaultdict(set)
for x in E: out[(x['src'],x['edge_type'])].add(x['dst']); inn[(x['dst'],x['edge_type'])].add(x['src'])
# (node_table, edge_type) 별 max · median · p90 · >255 셈
```

```python
# q5.py — 질문 37 걷기 셈 (발췌)
tree=ast.parse(open(G+'/gold-build.py').read())          # 실행하지 않고 QUESTIONS 만 읽음
QN=[n.value for n in tree.body if isinstance(n,ast.Assign) and n.targets[0].id=='QUESTIONS'][0]
Q=[{k.arg:ast.literal_eval(k.value) for k in c.keywords} for c in QN.elts]
# lookup = g_entry.norm + gold-build 순서 · holders = g_scope role 묶음 · 표 필터는 gold-build ans_* 와 같은 규칙
```

```python
# 근거 셈
per=Counter((e['gold_table'],e['gold_id']) for e in g_evidence)           # 24,115 행 · 최대 8 · 중앙 1
srk=Counter((s['target_table'],s['target_id']) for s in source_ref)       # 참조당 source_ref 최대 557 · 중앙 1 · 0 없음
```

## 부록 B. 확인 안 됨

- 앱 미추적 파일(`calibration_prep.py` · `claim_policy_eval.py` · `semantic_candidate.py` · `relation_adapter.py`)의 내용 — 이름과 위치만 봄.
- 옛 원장 MCP(raw)를 새 설계에서 쓸지.
- LLM 경로(SDK 키 · CLI 구독)가 지금 쓸 수 있는지(.env 열지 않음).
- 이번 허브 브랜치도 「실험용 · 회사 레포 머지 안 함」 인지(11-16 phub-ledger-redesign 때의 사용자 말 — 이번 작업에 같은지 확인 필요).
- `drafts/silver-check/silver-check.py` 의 남은 FAIL 1 의 내용(브리프가 알려진 것으로 둠 — 열지 않음).
