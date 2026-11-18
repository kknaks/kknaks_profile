# 코드 검수 — 허브 v05(WORK-005 · SPEC-001 0.5.1 구현분)

- 검수: reviewer_code · 2026-11-16 · read-only(코드 레포 변경 · 커밋 · stash 없음 · `.env` 안 엶)
- 대상: `HUB-WT = ~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev/backend` 미커밋 작업 트리(branch `kknaksss/phub-gold-jev`)
- 계약: `SPEC-001-hub-gold-mcp.md` 0.5.1 · `WORK-005-hub-v05.md` 0.1.0 · `_RESUME.md` §2 맨 위 행(W-1 ~ W-5 · A-1 · KD8) · `review-work-v05.md` · `kd8-jev-check-report.md`
- 외부 호출: 없음(Jev · LLM 안 부름). 18105 · 18106 은 GET 두 번씩(`health` · `coverage`)만 · 띄우거나 내리지 않음
- 이 리포트에는 질문 문장 · 시술 이름 · 답 원문 · gold 값이 없다(코드 · 칸 이름 · 셈 · 문항 id까지만).

## 0. 판정

| 판정 | FAIL | WARN | NOTE |
|---|---:|---:|---:|
| **PASS** | 0 | 0 | 8 |

WP-1 ~ WP-4 의 완료 조건이 전부 코드와 시험에 있고, 전체 시험이 통과한다(**598 passed · 2 skipped** — 기준선 568 · 2 에 30 이 더해짐 · skip 둘은 기준선과 같은 PostgreSQL 시험). 원칙을 어기는 자리(행 빼기 · 상위 N · 점수 · 덮인 후보 빼기 · 안전 강제 첨부)는 0이다. SPEC 에 없는 동작을 지어낸 곳도 없다 — 구현 때 정한 것은 전부 WORK-005 §9 A-1 ~ A-5 · O-22 ① 안에 있다.

유일하게 계약과 수가 다른 자리는 §4-9 상품 셈이다(SPEC 은 계열 15 · 시술 11, 도구는 계열 17 · 시술 0). 하지만 코드는 §4-4 맞춤 규칙을 그대로 따른다. 다른 것은 SPEC 셈의 식이고, WORK-005 §4 완료 조건 3 이 시킨 대로 코드를 수에 맞추지 않고 시험으로 드러냈다(N-1). 그래서 코드 결함이 아니라 SPEC 되적기 대상이다.

## 1. 검증 — 직접 한 번

| 명령 | 결과 |
|---|---|
| `uv run ruff check app tests scripts` | **All checks passed** |
| 데이터 env(WORK-001 §2-3 의 네 경로) + `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q -rs` | **598 passed · 2 skipped · 35.7 s**. skip 두 개 = `test_db_resilience.py:77 · :119`(격리 PostgreSQL URL 필요 — 기준선과 같음). **gold 실물 시험은 skip 0**(전부 돌았다) |
| 실물 build | `gold_hash` 앞 8자 `8accbb21`(시험의 `SPEC_HASH_PREFIX` 와 같음 → 셈 재현 단언이 skip 되지 않고 돌았다) |
| 오래 걸린 gold 시험 | T16 실물 불변식(대상 4표 전 노드 × 14) 0.75 s · T3 실물 0.34 s · T16 셈 재현 0.24 s(검수 N-4 의 「걸리는 시간」 — 문제없음) |
| `coverage` 한 번(실물 · 포트 없이 · 이 검수 셈) | 노드 7 = **4.4 ms** · 64 = **28.3 ms** |
| `resolve` 맞춤 꼴(37 질문 평균) | **0.09 ms/질문** — 서로 다른 `norm` 2,541 을 매번 도는 꼴이지만 느리지 않다 |
| 18105 · 18106 `GET health` · `GET coverage(product:PRD-416)` | 둘 다 새 코드(`integrity` 에 새 칸 · `coverage` 응답) · 셈 = 효과 (0, 4, 19) · 적응 (0, 11, 27) · 원리 (0, 0, 3) · 개요 (1, 1, 3) — WP-4 4 ① 그대로 |

## 2. WP 마다 완료 조건 · 계약 대조

### WP-1 — `resolve` 넓은 후보(§4-1 · §5-1 R1 ~ R8 · T15)

| 완료 조건 / 계약 | 코드 · 시험 | 결과 |
|---|---|---|
| R1 `norm` = 공백 제거 + 소문자뿐 | `resolve.py:20-24` | 맞음 |
| R2 · R3 부분 일치 전부 · 조사 목록 폐기 | `resolve.py:68-70`(`entry_norms()` 가운데 `f in q` 전부) · `PARTICLES` · 낱말 이어 붙임은 gold 모듈에 0(grep — 남은 `_KOREAN_PARTICLES` 는 기존 `retrieval` 모듈 · 이번 범위 밖) | 맞음 |
| R7 길이 하한 없음 · 덮인 짧은 조각도 남김 | `resolve.py:70`(빈 문자열만 제외) · `:79-89`(`covered_by` 는 표지만 · 빼지 않음) | 맞음 |
| R8 점수 · 순위 없음 | 정렬 키 = `in_range` → `-len(norm)` → `TABLE_ORDER` → 「이름」 먼저 → `gid`(`:78`) | §4-1 순서 그대로 |
| `matched{span, start, covered_by}` · `particle` 없음 | `:88` · 부록 A 계산 필드 `headers.py:95` · T3 `test_gold_contract.py:65` | 맞음 |
| `covered_by` = 나온 자리가 **전부** 덮일 때만(A-1 · 코디 확인) | `_covered_by` `:55-65` — 모든 자리를 덮는 더 긴 조각이 있어야 하고, 고를 때는 첫 자리를 덮는 것 가운데 가장 긴 것(같으면 앞 자리) | 맞음 · `test_T15_covered_only_when_every_occurrence_covered` |
| 같은 개념은 첫 행 하나(가장 긴 조각의 행) | `:80-86` | §4-1 그대로(N-3 의 좁힘 위험은 아래 셈으로 0) |
| `entry_norms()` = Protocol + CSV 구현 · 적재 때 한 번 | `repository.py:42 · 103-105` · `memory.py:46` | 맞음 · service 는 repository 만 부른다(기존 시험 그대로 통과) |
| T15 합성 — 직접 센 수 = `total` · 옛 조사 밖 꼬리 · 띄어쓰기 · 덮인 조각 남음 · 긴 것 먼저 · `particle` 없음 | `test_gold_tools_synthetic.py:60-84`(가짜 이름 · 꼬리 「조차」 · 「마저」) | 전부 있음 |
| `test_resolve_particle_and_span` 을 지우지 않고 **바꿈** | 옛 이름 없음 → `test_T15_*` 둘로 바뀜 | 맞음 |
| T15 실물 — 37 질문 개념 수 1 ~ 7 · 중앙 3 · 직접 센 집합 = 후보 집합 | `test_gold_coverage.py:372-386`(질문은 로컬 파일에서만 읽음 · 출력 없음) | 통과 |
| `test_resolve_zero_is_200` · `test_resolve_range_never_drops` · `test_T13_*` 그대로 | 그대로 있고 통과 | 맞음 |
| A-5 빈 `norm` | 이 검수 셈: 11-16 gold `g_entry` 에 빈 `norm` 행 **0** · 코드는 빈 문자열을 건너뜀(`memory.py:46`) | 맞음 |
| 도구 설명 — 「부분 일치 전부 · 조사를 떼지 않는다 · `covered_by` 와 함께 남는다 · 고르지 않고 전부」 | MCP `mcp_server.py:34-41` · REST summary `router/gold.py:48` · Swagger `swagger_docs/gold.py:14` · `test_tool_list` 가 낱말을 봄 | 맞음 |

**review-work-v05 N-3 확인(이 검수 셈 · 37 질문)**: 남은 후보 가운데 `covered_by` 가 붙은 것은 19 개다. 그중 같은 개념에 덮이지 않은 다른 이름(별칭)이 문장 안에 있었는데 덮인 행만 남은 개념은 **0** 이다. 그러니 「한 개념당 가장 긴 조각의 행 하나만 남긴다」 규칙이 37 질문에서 폭을 줄인 일은 없다. 자유 질문에서는 생길 수 있으니 1회차 trace 에서 다시 볼 것(N-6).

### WP-2 — `coverage`(도구 9) + 정보 종류 표(§4-0 · §4-9 · §5-8 · T16)

| 완료 조건 / 계약 | 코드 · 시험 | 결과 |
|---|---|---|
| §5-8 표 = 상수 하나 · 순서 = 표의 행 순서(A-4) | `kinds.py:9-48`(14 종류 · 대상 쪽 조회 · 값 · 속성 쪽 `{종류: {표: 조회}}` · 「—」 = 없음) | 표와 한 줄씩 대조해서 **맞음** — `overview` 속성 4표 · `indication` concern/site · `outcome` effect/site · `adverse` adverse/site · `contraindication` condition/site · `offer` offer/material/site · `package` concern/package · 나머지 대상만 |
| 개요 칸 11 · 원리 칸 3 상수 + T3 대조 | `headers.py:80-82 · 90-91` · 부록 A 「(정보 종류 셈)」 넷 · 「(넓은 후보)」 하나 · T3 통과 | 맞음 |
| 세는 길을 따로 짓지 않음 — 「쪽 넘김 앞 행 전부」 안쪽 함수를 **같이** 씀 | `facets.py:158` `facet_rows` · `pairs.py:63` `pair_rows` · `concern.py:67` `asked_rows` 를 `facets()` · `pair()` · `concern_candidates()` 와 `coverage()` 가 함께 부름 | 맞음 — 불변식을 구조로 지킨다 |
| 대상 쪽 셈 — role `자기` · `물려받음` · `하위 *` 로 한 번 얻어 `layer.role` 로 갈라 서로 다른 `gid` | `coverage.py:83-118` · 제품 × `offer` 는 `PRODUCT_OFFER_ROLES` | 맞음 |
| `overview` · `mechanism` = 그 칸에 값이 있는 profile 행만(0.5.1 결정 3 ①) | `coverage.py:115-117` · `:130-131` | 맞음 · 실물 원리 314 / 315 재현 |
| `indication` = `concern_match` 직접(W-5) | `facets.py:204-205` 를 그대로 씀 | 맞음 · 실물 37 / 34 재현 |
| `pair` 넷 = `b` 없이 · `a_layer.role` 로 · `same_day` = 갈래 전부 | `coverage.py:104-109` · `kinds.py:25-26` | 맞음 |
| `lineup` = `self` 0 · `lower` = 「하위 *」 행 수 · `inherited` `null` · `lower_holders` = 서로 다른 holder(A-2) | `coverage.py:100-103` | 맞음 |
| 값 · 속성 쪽 = `hier` 기본 `expand` 행 전부가 `self` · 셋은 `null` · concern `indication` = `counts.rows`(쪽 밖 목록 포함) | `coverage.py:121-132` · `asked_rows` 가 `site` 거르기 앞 전부 | 맞음 |
| 입력 검사 — `nodes` 필수 · 1 ~ 상한(설정 `GOLD_COVERAGE_NODES_MAX` 64) · 넘으면 `invalid_argument`(자르지 않음) · 꼴 · `not_found`(항목을 문구에) · `kinds` 표 밖 = `invalid_argument` · 안 주면 `null` | `coverage.py:29-51` · `config.py:41` · `.env.example` 한 줄 | 맞음 · `test_T16_input_errors` · `test_T16_nodes_max_is_setting` |
| 출력 — `nodes` 순서 그대로(같은 노드 두 번 = 두 번 · A-3) · 「—」 안 실음 · `name` · `total` = items 수 · `next_cursor` `null` · `ledger_check` 없음 | `coverage.py:52-58 · 61-65` | 맞음 · `test_T16_kinds_filter_order_and_duplicates` |
| T16 합성 — 손으로 센 값 · 원리 칸 빈 제품 `mechanism.self` 0 · 값 쪽 `null` | `test_gold_coverage.py:64-125` | 있음 |
| T16 실물 불변식 — **대상 4표 전 노드 × 14 종류**, 공개 도구로 끝까지 넘겨 셈 | `test_T16_real_invariant_all_target_nodes` · `tool_counts` 는 `walk(svc.facets / pair / scope)` 공개 도구만 씀(안쪽 함수 안 씀) | 통과 |
| T16 실물 셈 재현(§4-9 끝 두 불릿) | `test_T16_real_counts_reproduce_spec` — 적응 · 효과 · 부작용 · 회복 · 금기 · `inherited` · 원리 314 · 케이스 3 · 제품 상품 7 = SPEC 수 그대로 | **상품의 계열 · 시술만 다름 → N-1**(코드를 수에 맞추지 않고 따로 시험으로 드러냄 — 완료 조건 3 이 시킨 처리) |
| T7 REST = MCP · 오류 문구 같음 · T6 두 번 같음 | `test_T7_coverage_rest_equals_mcp` | 있음 |
| 기존 `facets` · `pair` · `concern_candidates` 시험이 **안 바뀌고** 통과 | 안쪽 함수 분리 뒤에도 기존 시험 그대로 통과(전체 598) | 맞음 |
| 7 · 64 노드 ms 보고 | `test_coverage_timing_real`(print) · 이 검수 셈 4.4 · 28.3 ms | 맞음 |
| REST `GET /coverage` · MCP `coverage` · 도구 9 | `router/gold.py:132-139` · `mcp_server.py:157-159` · `service.py` 머리글 「도구 9」 | 맞음 |

### WP-3 — 하위 role 설명 · 되적기 확인(§4-4 · §5-3 · T17 ~ T19)

| 완료 조건 | 코드 · 시험 | 결과 |
|---|---|---|
| W-4 문장이 MCP `facets` 설명 · REST `roles` 설명 · Swagger 에 **글자 그대로** | `mcp_server.py:58` · `router/gold.py:85-86` · `swagger_docs/gold.py:15` · `test_tool_list` 가 문장 전체를 봄(`test_gold_mcp.py:36-38`) | 맞음 |
| `pair` 설명에 펴는 role | `mcp_server.py:72` · 시험 `:39` | 맞음 |
| `facets.py` 머리글 — 한 단 한계 · 「제품 경유」 · semantic-map 을 바꿔 읽는 자리는 앱 쪽 | `facets.py:6-8` | 맞음 |
| T19 — 「하위 *」 을 주면 `layer.role` = 그 role · 기본값으로는 안 나옴 · 「상위 제품」 은 명시해야만 | `test_T19_lower_roles_only_when_named`(합성) · `test_T19_Q04_lower_product_rows_real`(실물 — Q04 줄) | 있음 |
| T17 · T18 이 이름이나 주석으로 찾아짐 | `test_gold_real.py:390` 절 머리 「= SPEC-001 §9 T17」 · `test_T18_packages_without_b`(`b` 없음 · `b` 있음 둘 다) | 맞음 |
| `request` 의 `null` 단언 셋 | `test_request_null_means_all` | 맞음 |
| O-22 ① (`subject`, `holder`) 중복 셈 | `memory.py:110-118` → `health.integrity.scope_duplicate_subject_holder_rows`(실물 0) | 맞음 — 이름이 정해짐(SPEC 되적기 후보 · N-8) |

### WP-4 — 시험 마감 · 실물 확인

| 항목 | 결과 |
|---|---|
| 1 T3 새 줄 다섯 + 계산 필드 · `particle` 빠짐 | 맞음(`headers.py:90-97` · T3 합성 · 실물 통과) |
| 2 `test_tool_list` 도구 9 | `TOOLS` 9 개 집합으로 봄 |
| 3 Q04 줄 | `test_T19_Q04_lower_product_rows_real` |
| 4 e2e 두 꼴 — ① `product:PRD-416` 셈 ② 이름 + 옛 조사 밖 꼬리 → 후보 0 아님(이름은 `g_entry` 에서 읽음) | `test_e2e_shapes_at_tool_level` · 18105 / 18106 GET 으로도 ① 같은 값 |
| 5 README 「검증」 전체 한 번 | 이 검수가 직접 돌림: 598 · 2(§1) |
| 6 README 도구 목록에 `coverage` | `README.md:101` |
| 7 18106 확인 | 코디가 띄워 둔 상태(`app-hub18106-ready-note.md`) — GET 으로 확인만 |
| 8 커밋 후보 grep | §4 |

## 3. 원칙 · 안전 · 지어낸 동작

| 볼 것 | 결과 |
|---|---|
| 대상 × 필요한 정보 안에서 빠짐없이 | `resolve` 는 문장 안 입구 이름을 **전부** 낸다(T15 실물이 「직접 센 집합 = 후보 집합」 을 37 질문 모두에서 단언). `coverage` 는 셈만 내고 행을 빼지 않으며, 셈이 0 인 노드도 그대로 낸다. 상한 64 를 넘기면 오류를 내고 잘라 내지 않는다 |
| 행 안 뺌 | 새 코드 어디에도 상위 N · 점수 · 잘라 내기가 없다(grep `[:` · `sorted(...)[` · `limit` 은 쪽 크기뿐). `covered_by` 는 표지일 뿐이다. 개념당 행 하나로 줄이는 것은 §4-1 계약이고, 37 질문에서 그 때문에 줄어든 개념은 0 이다(§2 WP-1) |
| LLM 에는 필요한 칸만 | 허브는 LLM 에 아무것도 넘기지 않는다(앱 몫 · 이번 범위 밖). `coverage` 에 행 본문이 없는 것이 이 원칙에 맞는다 |
| 안전 강제 첨부 0 | 허브 코드에 「묻지 않아도 금기 · 부작용을 붙이는」 자리가 없다. `coverage` 는 종류 14 를 다 **세지만** 행을 내지 않는다. 고르는 것은 앱(`kinds` 입력)이다 |
| 지어낸 동작 0 | SPEC · WORK 밖의 동작이 없다. 구현 때 정한 것 = A-1(나온 자리 전부) · A-2(`lower_holders` = holder 수) · A-3(두 번 = 두 번) · A-4(§5-8 순서) · A-5(빈 `norm` 건너뜀 · 실물 0) · O-22 ① 이름 · 제품 × `offer` 의 `inherited` = **0**(N-2) — 전부 WORK-005 §9 · 코드 머리글에 드러나 있다 |
| 고르지 않음 | `coverage` · `resolve` 둘 다 정렬은 결정론 키뿐이다. 「가장 그럴듯한 후보」 가 없다 |

## 4. 커밋 후보 grep(공개 레포)

커밋될 파일 = `git status --porcelain` 의 수정 4 + 미추적 31(파일 단위 · `__pycache__` 제외 · `uv.lock` 은 의존 목록이라 뺌) = 35 파일. 무시되는 것 = `.venv` · `__pycache__` · `.pytest_cache` · `.ruff_cache` 뿐이다.

| 찾은 것 | 방법 | 결과 |
|---|---|---|
| 홈 절대 경로 · 사용자 이름 · 회사 도메인 | `grep -nE "/Users/|~/orca|kknaks|marin|medisolve"` | **0** |
| 키 · 비밀번호 | `sk-…` · `api_key=` · `password=` | **0** |
| 외부 URL | `https?://` 중 127.0.0.1 · localhost 밖 | **0** |
| 시술 · 제품 · 케이스 · 계열 · 상품 · 패키지 · 고민 · 효과 · 부작용 · 조건 이름(`g_entry.text` 한글 3자 이상) | 실물 `g_entry` 를 읽어 35 파일 본문과 대조 | **0** |
| 실제 `gid` | `[A-Z]{2,4}-\d{3,6}` 를 실물 15표 키(gid · edge_id · node_id)와 대조 | **0** |
| 질문 문장 | `questions.csv` 질문 앞 12자를 대조 | **0** |
| 실제 **엔티티 코드** | 같은 꼴을 `g_entry.entity_code` 와 대조 | **4 종** — `PRD-416`(새 · `test_gold_coverage.py:363-368` · WP-4 4 가 지정한 노드) · `PRC-001` · `CND-002` · `CON-001`(`test_gold_real.py:201-203 · 301-302` · 앞 판부터 있음). 이름 · 값 없이 코드만이고 실물 시험 안에만 있다 → N-7 |

합성 fixture(`gold_fixture.py`)의 코드 · 이름은 전부 `*-90x` · 「제품가」 같은 가짜다. T15 의 꼬리 「조차」 · 「마저」 · 「께서」 도 가짜 이름이나 실물에서 읽은 이름에 붙인 것이다(코드에 이름 글자 없음).

## 5. 지적 표

### NOTE(코드를 막지 않음)

| # | 파일:줄 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| N-1 | `tests/test_gold_coverage.py:324-354` · `facets.py:206-215` | **§4-9 상품 셈이 SPEC 수와 다르다** — `self` 0 · `lower` ≥ 1: SPEC 은 계열 15 · 시술 11 · 제품 7, 도구는 계열 17 · 시술 0 · 제품 7. 시험이 SPEC 수가 **`offer.item_*` = holder 식**에서 나왔다는 것을 직접 다시 세어 보인다(15 · 11 · 7). 그런데 도구는 §4-4 맞춤 규칙(procedure → `procedure_code` · 케이스 → 그 케이스의 `procedure_code` · product → `item_*`)을 따른다. 코드가 계약(§4-4)에 맞고, SPEC §4-9 셈만 다른 식으로 센 것이다. WORK-005 §4 완료 조건 3 대로 코드를 수에 맞추지 않았다 | SPEC-001 §4-4 offer 행 · §4-9 끝 불릿 · §9 T16 · `app-hub18106-ready-note.md` 「허브 쪽 미결」 | 코디가 SPEC 되적기에서 §4-9 상품 수를 도구 식(17 · 0 · 7)으로 바꾸거나, §4-4 를 item 식으로 바꿀지 정한다. 뒤쪽이면 계약이 바뀌는 것이므로 사용자 확인이 필요하다. 앱 RQ1 에는 영향이 작다 — 시술은 `self` 가 늘 크게 잡혀서 하위로 내려가는 판정이 안 걸릴 뿐 행은 다 읽힌다 |
| N-2 | `coverage.py:6 · 112` | 제품 × `offer` 의 `inherited` = **0**(`null` 아님)으로 정했다. 실물에서도 0 이다. review-work-v05 N-2 가 「WORK 응답 꼴에 정해 적으라」 고 한 자리인데, WORK-005 §4 응답 꼴 · §9 A 목록에는 아직 없고 코드 머리글에만 있다. 앱 모의(`fake_hub`)가 `null` 을 내면 실물과 갈린다 | review-work-v05 N-2 · SPEC-001 §4-9 셈 표 | SPEC 되적기 때 「제품 × offer 의 `inherited` = 0(그 role 로 부르지 않음)」 한 줄. 앱 `--ping` 키 대조(W-5)는 키만 보므로 이 값 차이를 못 잡는다 — 앱 검수 쪽에 알릴 것 |
| N-3 | `facets.py:211-214` · `coverage.py:98-118` | 시술 × `offer` 에서 「하위 케이스」 holder 의 자기 행 = 그 케이스의 `procedure_code`(= 부모 시술)의 상품이라, `lower` 가 **`self` 와 같은 gid** 를 다시 센다(이 검수 셈: 하위 케이스 상품 행이 전부 자기 행과 같은 시술 **34**). 셈 정의(층마다 서로 다른 gid)와 불변식은 지키지만, 「하위에 N 행」 이 새 정보가 아닌 경우가 생긴다 | SPEC-001 §4-4 offer 행(0.4.1 계약) · §4-9 `lower` 정의 | 동작은 그대로 둔다. Jev 후보 설명에 `lower` 를 「하위에 따로 있는 정보」 로 쓰면 과장될 수 있다는 점을 SPEC-002 · 앱 쪽에 한 줄. 허브에서 고친다면 계약 변경이다 |
| N-4 | `app/modules/gold/__init__.py:1` · `swagger_docs/gold.py:23` | 머리글 「결정론 도구 8」 이 그대로 있다(`service.py` · `mcp_server.py` · Swagger 본문 `:11` 은 「도구 9」). Swagger 태그 「gold 도구 8(…coverage)」 은 REST 경로 8(`health` 뺌)을 센 것이라 틀리진 않지만, 같은 페이지 `:11` 의 「도구 9」 와 헷갈린다 | WORK-005 §1 「머리글 도구 9」 | 「도구 9」 로 · 태그는 「REST 도구 8 + health」 처럼 (문구만) |
| N-5 | `mcp_server.py:81-87`(coverage 설명) | 설명에 「lower = 하위 시술 · 하위 케이스 · 하위 제품 holder 의 자기 행」 이라고 적혀 있다. 그런데 `pair` 로 세는 넷(avoid · combo · same_day · order_interval)은 `pair` 의 펴는 role(하위 제품 없음)을 따르고, 제품 × `offer` 는 `inherited` 0 이다. 둘 다 계약대로 맞는 동작인데 설명에는 없다. C 열처럼 도구를 스스로 고르는 쪽이 설명만 보고 「하위 제품의 회피 0」 을 「없음」 으로 읽을 수 있다 | SPEC-001 §4-6 규칙 1 · §5-8 · §4-9 | 설명에 「pair 종류의 lower 는 하위 시술 · 하위 케이스만 · 제품의 offer 는 물려받음을 세지 않음(0)」 한 줄 |
| N-6 | `resolve.py:80-86` | review-work-v05 N-3(개념당 가장 긴 조각의 행 하나만 → 덮인 행만 남을 수 있음)은 37 질문에서 **0** 이다(§2). 자유 질문 · 추가 묶음에서는 생길 수 있다 | SPEC-001 §4-1 「같은 (`entity_table`, `entity_code`) 는 한 번만」 | 1회차 trace 에서 「`covered_by` 가 붙은 후보 가운데 같은 개념의 덮이지 않은 별칭이 문장에 있던 수」 를 세어 본다. 0 이 아니면 「덮이지 않은 조각이 하나라도 있으면 그 행」 으로 SPEC 되적기 |
| N-7 | `tests/test_gold_coverage.py:363-368` · `tests/test_gold_real.py:201-203 · 301-302` | 실제 엔티티 **코드** 4 종이 실물 시험에 글자로 있다(`PRD-416` 은 이번 판에 새로 들어옴). 이름 · 값 · gid · 질문은 없다. 공개 레포에서 코드만으로 뜻을 알 수는 없다 | WORK-005 §6 8(「실제 gid · 시술 이름 0」 — 코드는 금지 목록 밖) | 커밋 전에 코디가 정한다 — 그대로 두거나, `review-spec-v051.md` §2 의 대상을 「`g_scope` 에서 하위 제품을 가진 상위 제품 · 자기 효과 0」 조건으로 찾게 바꾼다(T19 Q04 시험이 이미 그렇게 찾는다) |
| N-8 | `memory.py:110-118` | O-22 ① 의 셈 이름이 `health.integrity.scope_duplicate_subject_holder_rows` 로 정해졌다(실물 0). SPEC §4-8 `integrity{…}` 꼴은 아직 세 칸뿐이다 | SPEC-001 §4-8 · O-22 ① | SPEC 되적기 후보 목록에 이름 한 줄(O-22 ① 를 「결정됨」 으로) |

## 6. 「사용자가 실물에서 만날 자리」

| # | 자리 | 무엇을 보게 되나 | 판단 |
|---|---|---|---|
| U-1 | 18105 이미 새 허브 | 이 검수 때 18105 · 18106 둘 다 `coverage` 를 내고 `integrity` 에 새 칸이 있다(같은 `gold_hash` `8accbb21`). 그러니 18105 는 **이미 새 코드로 다시 떠 있다**. 옛 앱(`matched.particle` 을 읽음 — WORK-005 §7)이 18105 를 보고 있으면 맞춤 꼴에서 `KeyError` 류로 깨진다 | 코디: 18220 화면이 새 앱 코드로 함께 다시 떴는지 확인(WORK-005 §7 「함께 바꿔 끼우기」) |
| U-2 | 속도 | `resolve` 0.09 ms · `coverage` 64 노드 28 ms — 사용자가 느끼는 속도에 허브 몫은 거의 없다 | 문제없음 |
| U-3 | 상품 질문 · 시술 노드 | 시술의 `offer` 는 `self` 가 하위 제품 상품까지 품어 크게 잡히고(N-1), 하위 케이스 셈은 같은 행을 다시 센다(N-3). 「시술 X 상품」 질문에서 답이 「직접」 층으로 말하는 상품 가운데 실제로는 제품 항목(`item_*` = product)인 것이 섞여 보일 수 있다 — 행의 `item_table` · `item_code` 로는 갈린다 | 앱이 층을 밝힐 때 `layer.role` 만 보면 「시술 자기」 로 말한다. e2e 피드백에 그런 지적이 오면 원인이 여기다 |
| U-4 | 짧은 이름 후보 | 부분 일치라 문장 안에 우연히 든 한 글자 · 두 글자 이름(부위 등)도 후보로 나온다(R7 · R8 — 계약). 37 질문 개념 수 최대 7 | 앱 Jev 대상 판단 trace 에서 「쓸데없는 후보」 로 보이는 것은 정상 동작이다 |
| U-5 | README | 「gold 로컬 실행 · 검증」 절이 18105 로 띄우라고 적혀 있다(코디 포트). 시험 명령은 그대로 따라 하면 돌아간다(이 검수가 같은 꼴로 돌림) | 따라 할 수 있음. 워커가 README 대로 18105 를 띄우면 코디 서버와 부딪히므로 브리프의 「18105 는 코디 것」 이 계속 필요하다 |

## 7. 검수 범위 · 하지 않은 것

- 읽은 것: 허브 gold 모듈 중 이번 판에 바뀐 곳(`resolve.py` · `kinds.py` · `coverage.py` · `facets.py` · `pairs.py` · `concern.py` · `memory.py` · `repository.py` · `headers.py` · `config.py` · `mcp_server.py` · `router/gold.py` · `swagger_docs/gold.py`) · 시험 `test_gold_coverage.py` · `test_gold_tools_synthetic.py` 의 T15 · `test_gold_mcp.py` 의 도구 목록. 0.4.1 에서 그대로인 `inputs.py` · `cursor.py` · `core.py` · `neighbors` · `evidence` 는 다시 읽지 않았다(시험 통과로 확인).
- 미커밋 untracked 파일이라 0.4.1 판과 줄 단위 diff 는 낼 수 없었다. WORK-005 §1 의 「지금」 칸을 기준으로 바뀐 자리를 대조했다.
- 실호출(Jev · LLM) · 서버 띄우기 · 내리기 · 코드 레포 변경은 하지 않았다. 18105 · 18106 에는 GET 4 번만 보냈다. 쓴 파일은 이 리포트 하나다(검수용 셈 스크립트는 세션 scratchpad 에만 있다).
