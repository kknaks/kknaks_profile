# 허브 구현 보고 — WORK-013 0.2 (SPEC-001 0.7.2 · NM · DP · CS · SP)

- 워크트리 `PROCEDURE-HUB/phub-gold-jev` · HEAD `daa54e3` 위 · `backend/` 만 · **커밋 안 함**
- 시험: **WP 마다 그 WP 파일만** · 전체 pytest 안 돌림 · WP-4 는 B-1 범위(gold 묶음 + `test_medallion_repo.py` + `medallion_fixture.py` 를 고쳐 `test_medallion_load.py`)
- 실물 env 넷 + `GOLD_EXPECTED_HASH`(8accbb21…)를 준 채로 돌림 → skip 0

## 변경 파일(22 — allowed_paths 안)

새 5: `app/modules/gold/descend.py` · `tests/test_gold_v07_{resolve,descend,site,compat}.py`
고침 17: `app/modules/gold/{resolve,concern,memory,repository,headers,service,mcp_server}.py` · `app/router/gold.py` · `app/swagger_docs/gold.py` · `README.md`(gold 절) · `tests/{gold_fixture,medallion_fixture}.py` · `tests/{test_gold_contract,test_gold_holes,test_gold_mcp,test_gold_tools_synthetic,test_medallion_repo}.py`

손대지 않음 확인: `coverage · closure · facets · pairs · inputs · db_inputs · gold_main` diff 0 · `app/main.py` · `app/core` diff 0(origin 대비) · CSV · json · db 파일 0 · 새 파일 포함 비밀값 · 홈 경로 grep 0 · 18107 `lsof` 0.

## WP 별

| WP | 구현 | 돌린 파일 | 결과 |
|---|---|---|---|
| WP-1 NM | `memory.abbr_keys_of`(NM1 — 한 곳) · 색인 `entry_by_abbr` · repo `abbr_keys()` · `entries_by_abbr(key)`(Protocol 29 → **31**) · `resolve._match` 줄임 · `matched.how` 전 후보 · `full` 은 줄임만 · NM4 덮임 · 같은 길이 부분 먼저 · 입력 `abbr` | `test_gold_v07_resolve` · `test_gold_tools_synthetic` · `test_gold_contract` · `test_medallion_repo` · `test_gold_coverage` | **233 passed · 0 skip** |
| WP-2 DP · CS | `descend.py`(DP1 ~ DP9 · repo 만 읽음) · `concern_sites()`(CS1 ~ CS6) · 입력 `to_procedure` · 첫 쪽 `descended[]` · `sites[]` · `counts.descended` · `counts.sites` | `test_gold_v07_descend` · `test_gold_contract` · `test_gold_holes` · `test_gold_tools_synthetic` · `test_gold_coverage` | **210 passed · 0 skip** |
| WP-3 SP | SP1(0.7.2): 물은 부위 코드 ∈ `sites[]` 면 `filter` · 아니면 `prefer`(행 전부 · `site_prefer` · true 행에만 `site_match` · `n_site_prefer` · `counts.site_prefer`) · 입력 `site_mode` · 머리 `site_applied` | `test_gold_v07_site` · `test_gold_tools_synthetic` · `test_gold_holes` · `test_gold_contract` · `test_gold_v07_descend` | **207 passed · 0 skip** · 실물 23,140 짝 시험 **3.9 s** |
| WP-4 | compat · DT10 v07 · SAME/ERRORS · T3 부록 A 여섯 줄 · swagger · README | `tests/test_gold_*.py`(12) + `test_medallion_repo` + `test_medallion_load` | **501 passed · 0 skip** · ruff 통과 |

## 실물 수(전부 WORK 기대와 같음)

- NM: 열쇠 **2,881**(하한 없이 2,885) · 개념 533 · 37 문항 `abbr` on = off(`how` 빼고) — 새 후보 0
- DP: 묶음 0 → **41 → 41** · `undescended` 합 **0** · 내린 것 있는 고민 **155**(260 전부) / **142**(자기 행 247 기준 — W-1) · 최대 **107** `CON-226`(계열 6 · 자기 행 기준 · 물려받는 `CON-230` 도 107) · `CON-168` → `M18` · `PRC-123`~`128` · path 패키지 → 계열
- CS: `sites[]` 있는 고민 **100**(자기 85) · 최대 23 항목(서로 다른 부위 18) · `CON-168` = `SITE-072`/`CSI-0054`
- SP: `filter` **191**(자기 95 · 하위만 96 · 고민 100) · `prefer` **22,949** · 묶임 없는 160 고민 14,240 짝(filter 로 0 14,008 · 표지 646 / 232 짝) · 밖 부위 8,709 짝(filter 로 0 8,444 · 표지 971 / 265 짝) · 표지 합 1,617 / 497 짝 · auto 0 행 5 짝(전부 filter — 기대 5 짝 그대로) · 물려받는 묶임 없는 9 전부 prefer · 묶임 있는 4(`CON-012 · 136 · 206 · 230`)만 filter 짝 · `CON-048`×`SITE-051` prefer 105/55/표지 0 · `CON-005`×`SITE-051` prefer 54/15/표지 0(filter 0 · unfiltered 54) · `CON-005`×`SITE-014` filter 54/15 · `CON-001`×`SITE-014` filter 73/16(column 24 · concern_site 54) · `CON-001`×`SITE-051` filter 11/3

## §8-1 실물 확인(18107 — CSV 판 → DB 판 · 띄웠다 내림)

| # | 결과 |
|---|---|
| E1 | 18107(CSV) health `gold_hash` 8accbb21 · `aux_hash` 6435fe41 = 18105 · 열쇠 같음 · `expected_hash_checked` true |
| E2 | 답 키 `calls/` 37 파일 · 55 호출 · 69 쪽(facets 31 · pair 15 · concern_candidates 5 · scope 4) — 새 열쇠 빼고 18105 와 **차이 0**. 다른 것은 둘째 쪽 `request.cursor` 문자열 한 곳(Q08#0)뿐 — 불투명 cursor 서명에 새 입력이 들어가 값이 다를 뿐 내용 아님(SPEC 변경 기록 cursor 줄대로) · `covered_by` 차이 0 |
| E3 | `CON-168` total 0 · `M18` 1 묶음 · 시술 6 · path 패키지 → 계열 · `sites` = `SITE-072` 1 |
| E4 | `CON-048`×`SITE-051` prefer 105 · 55 · 표지 0 / filter → 0 · unfiltered 105 · `CON-001`×`SITE-014` filter 73 · 16 · `CON-005`×`SITE-051` prefer 54 · 15 · 표지 0 · sites = `SITE-014` / filter → 0 · 54 · `CON-005`×`SITE-014` filter 54 · 15 |
| E5 | `M18` 앞 낱말 2 글자 줄임(띄움 · 붙임) → `M18` how 줄임 · `CON-137` covered_by = 줄임 조각 / `abbr=off` → `M18` 없음 |
| E6 | MCP tools 9 · 설명 문장 ①②③ · 스키마 `abbr` · `to_procedure` · `site_mode` · MCP = REST(두 판 모두) |
| E7 | CSV 판 = DB 판: health(loaded_at · load_ms 빼고) 같음 · 요청 66 묶음 차이 **0** · E6 같음 |

- DB 판 첫 시작은 `F1 DB 접속 실패(ConnectionRefusedError)` — 코디 메시지대로 Docker 데몬이 꺼져 18432 가 내려가 있던 탓 · 다시 띄운 뒤 재시도로 통과. 접속 값은 `set -a; . ~/.config/phub/medallion-pg.env; set +a` 로 프로세스 env 에만(찍지 않음). PG 에 쓰기 0.
- 18105 에는 GET 만. 응답 dump 는 세션 scratchpad(레포 밖).

## 고친 기존 시험(전부 §2 ⓐ ~ ⓖ 안)

| 파일:자리 | 까닭 |
|---|---|
| `test_gold_tools_synthetic.py` T15 · T23 `matched` dict 넷 | ⓐ `"how": "부분"` 더함 |
| `test_gold_tools_synthetic.py` `test_concern_candidates_groups` 두 호출 | ⓑ `site_mode="filter"`(기본 판 CON-901 sites = [] → prefer) |
| `test_gold_holes.py` `test_T22_unbound_is_051`(두 짝 · CON-902 × 부위가) · `test_T22_other_site_does_not_pick_bound` | ⓖ `site_mode="filter"` |
| `test_gold_holes.py` `test_T22_with_inherit` · `test_e2e_shapes_052_real` · `test_T22_real` | ⓒ — 손대지 않고 통과 |
| `test_gold_contract.py` matched 꼴 · counts 두 꼴(N-2) · descended/sites/site_prefer 꼴 · ROW_COMPUTED `site_prefer` · v07 응답 · 부록 A 여섯 줄 | ⓓ |
| `test_medallion_repo.py` 색인 목록 + `entry_by_abbr` · v07 DT9 · DT10 v07(길 단언 뒤 대조) · PAGED concern | ⓔ · W-2 · N-3 |
| `test_gold_mcp.py` SAME 셋 · ERRORS 셋 · `SAME_V07`(N-1 — 판마다 따로) | WP-4 표 |

ⓕ 는 일어나지 않음(기본 · holes 판 열쇠 0 — 시험이 단언).

## 구현 때 정한 것(SPEC 되적기 후보 — §10 A)

- A-1 DP 자리 = 새 `descend.py`(repo 만 읽음) · `concern.py` 는 부르기만
- A-2 메서드 `abbr_keys()` · `entries_by_abbr(key)` — **Protocol 29 → 31**(SPEC-003 §5 P1 되적기 후보)
- A-3 목록 꼴 `abbr` = 검사해 `request` 에 싣기만(무시) · 기본 `"on"`
- A-4 `matched` 순서 (`span`, `start`, `covered_by`, `how`) + 줄임만 `full`
- A-5 `site_prefer` = false 행에 `site_match` 없음(N-2)
- A-7 `write_fixture(root, holes=False, v07=False)` — v07 은 holes 개체 위에 얹음
- R1 `norm` 은 `headers.py` 로 옮김(`resolve.norm` 그대로 다시 내보냄) — `resolve.py` 가 `memory` 를 import 하면 기존 경계 시험(`test_service_layer_uses_repository_only`)이 막아서
- NM4 덮임: 문장에 나온 줄임 열쇠는 그 개념이 이미 부분 후보라 다시 내지 않아도 「맞은 조각」 으로 덮임에 넣음(이름 전체 + 줄임 꼴을 함께 말한 문장에서 짧은 조각의 둘째 자리가 덮이게) — 37 문항 차이 0 확인
- `ambiguous`: 줄임 열쇠가 (부분 후보 아닌) 개념 둘 이상에 닿으면 참
- 머리 순서 `… inherited_from · site_applied · counts · groups` · counts 순서 = 0.6 여덟 + `descended` · `sites` · `site_prefer`
- DP: 제품의 「가장 좁은 층」 = 그 층의 holder 전부 · 한 행이 한 계열에 여러 길이면 `path` 의 scope_gid 열이 작은 길 · `procedure_codes` 는 그 계열로 닿은 시술 전부(고른 길이 lands=procedure 일 때)

## 미결 · 주의

- **코디: 18105 를 0.7.2 로 재시작(DB 판) 필요** — 지금 18105 는 0.6 코드.
- SPEC 되적기 후보: SPEC-003 §5 P1 메서드 29 → 31 · SPEC-001 §4-1 목록 꼴 `abbr`(A-3) · `부분` 후보에 `full` 없음(A-4) · §4-5 `site_prefer` = false 행 `site_match` 없음(A-5).
- 실물 시험 시간: T28(23,140 짝 × 거름 대조) 3.9 s · WP-4 묶음 전체 46 s — 줄이지 않음.
