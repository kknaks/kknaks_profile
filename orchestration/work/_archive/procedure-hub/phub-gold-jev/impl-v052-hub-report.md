# 허브 0.5.2 구현 보고 — WORK-007 WP-1 ~ WP-5 (backend · task_c2e2fd5254c8)

워크트리 `phub-gold-jev` · 커밋 없음 · 18105 손대지 않음 · **18106 띄워 둠**(GOLD_EXPECTED_HASH 줌 · 로그 = 같은 폴더 `hub18106.log`).

## 변경 파일(전부 backend/ · allowed_paths 안)

- 새: `app/modules/gold/closure.py`(하위 닫힘 함수 하나 — scope · facets · pair · coverage 가 함께) · `tests/test_gold_holes.py`(40 시험 — T20 ~ T23 · 보조 ③ · T3 새 줄 · 보고용 셈)
- 고침: `headers.py`(concern_site 칸 · 부록 A 0.5.2 다섯 줄 · AUX_LINES 7 · 계산 필드 상수) · `inputs.py`(concern_site.csv 읽기 · aux 6 파일) · `memory.py` · `repository.py`(`concern_site_by_site` · `sites_of_concern` · LoadRecord.concern_site) · `core.py`(`layer_of` 에 depth · via) · `service.py`(scope 닫힘 · descend · upper 전달 · health.aux.concern_site) · `facets.py` · `pairs.py`(descend · 닫힘) · `coverage.py`(lineup 닫힘 · 고민 indication.inherited) · `concern.py`(HG1 `concern_rows` · HG3 `bound_concerns` · site_match · counts.self_rows · by_site_match · upper) · `kinds.py`(indication 이름 「어디에 쓰나」 — **응답에 나가는 자리 없음**: KIND_NAMES 를 쓰는 코드 0) · `mcp_server.py`(설명 HG2-7 · N-2 · HG1 · HG3 · pair/coverage lower 줄 · 새 입력) · `router/gold.py` · `swagger_docs/gold.py` · `tests/gold_fixture.py`(concern_site.csv · `holes=True` 판) · `tests/gold_support.py`(실물 판정에 concern_site.csv) · `README.md` · `envs/.env.example`
- `pyproject.toml` · `uv.lock` 은 이번에 안 고침(앞 판 변경 그대로)

## 검증

- ruff `app tests scripts` 통과
- 기준선(WP-1 앞): 데이터 env 전체 **598 passed · 2 skipped** → 끝: **638 passed · 2 skipped**(+40 = test_gold_holes) — `--ignore=tests/integration`
- 18106: health gold_hash `8accbb21…` · files 22 · expected_hash_checked true · aux_hash `6435fe41…` · aux.concern_site {95, 85, 51} · REST e2e4 꼴 73 행 · 묶음 16 · by_site_match {column 24, concern_site 54} · Q10 꼴 inherited_from CON-008 steps 1 · 묶음 65 · LCK-010 · Q12 꼴 M2 adverse(하위 셋) total 246 · depth 최대 2 · MCP list_tools 9 · 새 입력 descend(scope · facets · pair) · upper(concern_candidates) · MCP Q10 = REST

## 완료 조건 수치

- WP-1: concern_site 95 행 · gold 해시 그대로 · aux 6 줄 = aux_hash · 0.5.1(5 줄) 값과 다름 · 고민 85 · 부위 51(전부 g_entry site 입구 · 이름 하나) · 옛 cursor_invalid 시험 통과
- WP-2(T21): 계열 18 · depth 2 케이스 합 268(계열별 SPEC 수 그대로) · 한 단 케이스 0 · 전 대상 858 닫힘 holder = 하위 그래프 자손(자손 아닌 0) · 순환 0 · 자기 고리 0 · **그래프 셈 가장 긴 길 4 단(단언)** · **응답 layer.depth 최댓값 = 2(보고만 · H-2)** · Q12 표본 4 가 M2 대상 조회(자기 · 물려받음 · 하위 셋)로 전부 · descend=one 이면 빠짐
- **H-1**: 제품의 하위 제품을 거치는 길 13 건(N-3 의 13 짝) — 그 한 건을 facets profile 응답에서 확인: layer.depth ≥ 2 · layer.via[-1] = 그 제품(holder_table product) · 그 제품의 `하위 제품` 행이 그 holder 를 가리킴(test_T21_real_via_product_path)
- WP-2 완료 조건 6: T16 실물 셈(적응 33·3·1 / 효과 30·3·1 / 부작용 31·3 / 회복 4 / 금기 2 / 상품 제품 7 / inherited 만 수) **HG2 뒤에도 그대로**(기존 시험 손대지 않고 통과) · 상품 17 · 0 · 7 그대로
  - lower 행 합 one → all: 적응 3,590 → 3,886 · 효과 2,321 → 2,556 · 부작용 3,854 → 4,357 · 회복 18 → 27 · 금기 62 → 66 · 상품 293 → 299 · 패키지 120 → 178 · pair(전 갈래) 275 → 377
- WP-2 완료 조건 7(O-26): M2 adverse_detail total 276 → 464(+188 = SPEC Q12 줄) · 0.6 ms / M15 adverse_detail 287 → 416 · 0.7 ms / pair M2 68 → 72 · pair M15 49 → 58(전부 한 쪽) · coverage 64 노드 49.5 ms(0.5.1 같은 자리 값은 따로 못 잼 — 기존 test_coverage_timing_real 단언 5 s 안 통과)
- WP-3(T20): 행 0 고민 13(SPEC 목록 그대로) · 전부 steps 1 · 행 합 1,033 · CON-012 → CON-008 묶음 65 · 행 181 · LCK-010 · 13 의 coverage indication.inherited = counts.rows · 자기 행 1 이상 고민 전부 inherited 0 · steps 2 는 합성으로만(N-4)
- WP-4(T22): 97 짝 · 글자 일치 0 인 40 짝 중 37 이 ≥ 1 · 남는 3 짝 = CON-200×SITE-084 · CON-226×SITE-019 · CON-277×SITE-084 · 묶인 고민 자신(자기 행 ≥ 1 인 91 짝) 0 없음 · 겹치는 4 짝: CSI-0079 · 0083 = 0 행 + unfiltered_rows(36 · 56) · CSI-0007 · 0047 = 7 행씩 · 넷 다 inherited_from 있음 · 97 짝 전부 0.5.1 집합 ⊂ 0.5.2 · 낸 행 = 직접 센 것 · CON-001×SITE-014 = 73 행 · 묶음 16 · 겹침 5 · csi_ids CSI-0001
- **W-2 다시 센 수(보고만)**: 케이스 끝 g_pair — 서로 다른 gid **100** · 계열마다 더한 값 **104**(SPEC 129 와 다름) / 97 짝 행 합 — 글자 일치만 **289** · HG3 **1,722**(SPEC 1,700 과 다름 · 검수 셈과 같음)

## 고친 기존 시험(계약이 바뀐 자리)

1. `test_gold_load.py::test_hash_formula_and_record_synthetic` — files 21 → 22(보조 ③ · §2-3 4)
2. `test_gold_load.py::test_T1_real_load_counts_and_hash` — 21 → 22 · 경로 표에 concern_site.csv · aux 6 줄 단언 더함
3. `test_gold_tools_synthetic.py::test_health` — 21 → 22
4. `test_gold_rest.py::test_health_and_tools` — 21 → 22
5. `test_gold_coverage.py::test_T16_modality_lower_holders` — 합성 계열 adverse (1,3,2,0) → (1,4,3,0) · lineup (0,2,2) → (0,3,3)(HG2 — 하위 시술 아래 케이스)
6. `test_gold_coverage.py::test_T16_value_and_attr_nodes` — 고민 노드 indication.inherited None → 0(HG1-6)
7. `test_gold_coverage.py::tool_counts`(T16 불변식 헬퍼) — 고민 indication 을 self_rows · 물려받은 응답의 counts.rows 로(HG1-6)
8. `test_gold_contract.py`(`ROW_COMPUTED` · `_rows_ok` · `check_response`) — layer 에 depth · via · scope 행 depth · via · site_match · inherited_from · counts 꼴(부록 A 0.5.2 계산 필드)
9. `test_gold_real.py::test_T4_Q10_empty_pointers_is_zero_with_ledger` — upper=none 이면 total 0 + LCK-010 · 기본값은 윗고민 묶음 + LCK-010(T20 Q10 줄)
- 주석만: T23 표지(test_T15_covered… · test_integrity_synthetic · test_real_integrity…) · item_* 15·11 = HG2 앞 수(test_T16_real_offer_spec_numbers_are_item_based)
- test_T11_presence_* 는 손대지 않고 통과(윗고민도 없는 값)

## 구현 때 정한 것(SPEC 되적기 후보)

- A-1 닫힘 = 요청 때 따라감(scope_by_subject 색인 하나)
- A-2 `health.aux.concern_site{rows, concerns, sites}` 더함
- A-3 descend=one = 0.5.1 과 같은 행 · 순서 · total · counts + depth 1 · via [] · request.descend
- A-4 `counts.unfiltered_rows` = site 를 안 걸었을 때 이 응답이 낼 행 수(물려받았으면 윗고민의 행 수)
- A-5 `site_match[]` = `[{"by":"column"}, {"by":"concern_site","csi_ids":[…]}]`
- A-7 대상 쪽 holder 순서 (depth, scope_gid) → 행 gid
- A-8 scope roles 없음 = 하위 셋 전부로 따라감
- HG2-3 같은 depth 의 동점 = **마지막 단 g_scope 행의 gid 가 작은 길**(너비 우선 · 단마다 후보를 gid 순)
- depth 1 행은 0.5.1 처럼 전부(같은 holder 가 role 둘이어도 — integrity 넷째 0)
- 닫힘의 방문 집합에 대상 자신 포함(대상으로 돌아오는 고리에서 끝남)
- concern_candidates 응답 머리 순서: build · request · total · next_cursor · inherited_from · counts · groups(+ 첫 쪽 modality_only · unreached · ledger_check)

## 미결 · 주의

- SPEC 수 둘(케이스 끝 g_pair 129 · 97 짝 1,700)은 다시 나오지 않음 — 위 100 · 104 · 1,722 로 되적기 필요
- 18106 은 띄워 둔 채(코디가 내리거나 18105 를 새 코드로 다시 띄울 때 함께)
