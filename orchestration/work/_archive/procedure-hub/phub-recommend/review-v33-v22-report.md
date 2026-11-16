# 함께 검수 보고서 — SPEC-005 v3.3(0.3.4) · WORK-008 + SPEC-006 v2.2(0.3.2) · WORK-009

작성 2026-11-01 · 검수자 reviewer 워커(읽기 전용 · 대상 문서 수정 없음 · 이 보고서만 씀)
대상 `SPEC-005.md`(0.3.4 · 1,227행) · `WORK-008.md`(198행) · `SPEC-006.md`(0.3.2 · 725행) · `WORK-009.md`(219행) · 배경 `phub-recommend-walk-fix-context.md`
대조 = 근거 스크립트 2(사본으로 2회 다시 돌림 · 아래 §2) · 허브 코드 `PROCEDURE-HUB/phub-recommend` **cc637a2**(`git status` 깨끗) · 앱 코드 `clinic_chat/hub-evals` **f8533ff**(깨끗) · `runs.jsonl` rerun-v4 `b202611011148-c6ed3a` 의 `trace.walk` · b031371c 메모리 빌드(스크립트와 같은 방법 · 해시 assert 통과)

## 판정

| 스펙(+ 작업) | 판정 | FAIL | WARN |
|---|---|---|---|
| **SPEC-005 v3.3 · WORK-008** | **PASS** | 0 | 8 |
| **SPEC-006 v2.2 · WORK-009** | **FAIL** | 3 | 8 |

한 줄: 허브 쪽 꼴(T11 `facts[]{id, line, section, owner?, cut?, flags?, gap?}` · 1쪽 12줄 · `more` · `page` · `full` · `fact_ids` · `claude_contract{allowed, must_show_flags}` · peek `bytes` · `n_facts`)은 006 이 이름 · 칸 · 단위 그대로 읽고, 두 스크립트는 결정론이며 숫자가 SPEC 과 맞는다. FAIL 셋은 모두 006 · 009 쪽이다. ① 005 가 WORK-009 에 넘긴 바이트 셈 방법(V-17)이 006 · 009 어디에도 없다 — 「peek `bytes` 를 예산에 그대로 쓴다」는 말과 앱 셈 방법이 서로 다르다. ② 원문 받기 예산 12,000 의 근거(「cut 만이면 여유 큼」)가 005 의 측정(cut 받기 p95 14,376)과 어긋난다. ③ 「자료에 없다」 68 중 안 닿은 34 를 새 걸음 순서 규칙이 얼마나 덮는지 셈한 숫자가 없다.

| 기준 | 005 · 008 | 006 · 009 | 요지 |
|---|---|---|---|
| 1 두 스펙 계약 일치 | PASS | **FAIL(F-1)** | 칸 이름 · 꼴은 1:1(§1 표). 바이트 셈 방법(compact 와 공백 구분자 · `intent` +17B)만 어긋남 |
| 2 숫자 재현 · 결정론 | PASS(W-1 · W-2) | **FAIL(F-2)** · W | 두 스크립트 r1 = r2 = 커밋본(바이트 같음). SPEC 숫자 전부 맞음. 006 원문 예산 근거는 005 측정과 반대 |
| 3 실물 대조 | PASS(W-6) | PASS | 허브 cc637a2 이웃 slim 칸 · peek 칸 · 엣지 종류 31 · 앱 `_hub` 셈 · `trace.walk` 칸이 SPEC 서술과 같음 |
| 4 끝 조건 검증 가능성 · 68/34 덮는 셈 | PASS(W-3) | **FAIL(F-3)** | 005 §6-7 은 (a)~(h) 전부 잴 수 있다. 006 에는 68/34 를 다룬 셈이 없다 |
| 5 결정표 충돌 | PASS | PASS | 허브 LLM 없음 · 결정론(코드 포인트 40자 자르기) · G13 안전 peek · 이웃 slim 유지 · 실버 수정 없음 — 충돌 0 |
| 6 008 ↔ 009 순서 · 표면 grep | PASS(W-7 · W-8) | PASS(W-13 · W-14) | 두 작업 모두 「WP-2 꼴 확정 뒤 009 착수」로 맞음. 표면 grep 을 다시 돌림: 009 는 31/31 이 표 안. 008 은 표 밖 파일이 1개 |
| 7 추측 자리(V-14~18 · X-1~8 밖) | PASS | W-15 | 006 §3-8 사실 4 의 「추정」(S-2)이 §7-9 에 없음 |

---

## 1. 계약 일치 대조(기준 1 · 칸 단위)

| 006 이 읽는 칸(§3-4-2) | 005 정본(§5-16) | 허브 코드 cc637a2(지금) | 판정 |
|---|---|---|---|
| peek `neighbors_by_kind{edge: {n, items[:4]{id, kind, name, label, n_facts}}}` | 같음(`direction` 은 006 이 안 읽음) | `{n, direction, items[:GOLD_PEEK_ITEMS_PER_KIND]{id, kind, name, label}}` — `n_facts` 는 WORK-008 WP-2 가 더함 | ○ |
| peek `sections[]{name, n_facts, bytes}` · `bytes` = expand 기본 꼴 1쪽 REST 본문(봉투 포함 · `intent` 없음) | 같음 | 지금은 원문 바이트 합(`tools.py:2037`) → WP-2 가 바꿈 | ○(꼴) · **단위는 F-1** |
| peek `safety{}` · `claude_contract.rule` | 같음 | 있음(envelope) | ○ |
| expand(neighbors) `neighbors[]{id, kind, name, edge, kind_edge, value?, safety?, sections_n}` | 같음(v3.2 그대로 · `kinds?` 더 있음) | `tools.py` 이웃 행 = 같은 칸 | ○ |
| expand(sections[1]) `facts[]{id, line(≤ 40), section, owner?, cut?, flags?, gap?}` · `more{section: n}` · `claude_contract{allowed: "facts_uncut", must_show_flags}` · `priority` · `use_first` 없음 | 같음 | 지금은 `sections{s:{facts, more_ids}}` · `priority` · `use_first` → WP-1 이 바꿈 | ○ |
| expand(fact_ids[]) → `facts[]` 끝에 `{id, text, section, owner?, source{file, path}}` · ≤ 64 · 그 노드 fact 만 | `full` 행 꼴 · `GOLD_EXPAND_FACT_IDS_MAX` 64 · `_node_fact_ids` | 검증 함수 있음(`tools.py:2174`) | ○ |
| `page` — 걸음에선 1쪽만 · `more` 는 기록 | `page?: 1` · V-18 「허브는 `more` 셈만」 | — | ○ |
| `use_first` 없음 → 앱 `rank` = 걸음 → 호출 → `facts[]` 순 | 「우선순위 = `facts[]` 순서」 | — | ○(W-4: 005 V-11 이 아직 열린 채) |
| `intent?` 받되 무시 | M-3 | 있음 | ○ |

이웃 묶음과 엣지 종류의 대응(006 §3-4-6 · `spec006-v22-count.json order.group_edges`)에 든 엣지 종류 27개가 b031371c 빌드에 **모두 있다**(엣지 종류 31 중 · `concern_related` · `key_technique` · `line_item` 은 「나머지」). peek 키 실물: `unit_procedure:U5-001` → `procedure_relation · requires_check_unit · site_caution_unit · has_complication_unit · combo_component · product_unit · contains · treats · treats_unit · has_statement_unit · key_family · key_site · key_technique · procedure_pair`.

## 2. 숫자 재현(기준 2)

두 스크립트를 scratchpad 사본으로 돌렸다. 출력 경로만 바꿨고, 입력 경로와 셈 코드는 그대로다. 각 2회씩이다. `$W` 의 원본은 덮어쓰지 않았다.

| 스크립트 | r1 = r2 | r1 = 커밋본 | 시간 |
|---|---|---|---|
| `spec005-v33-measure.py`(backend venv · `precompute_bytes_seconds` 빼고) | 같음 | 같음 | 7.2s |
| `spec006-v22-count.py` → `.json` · `.md` | 바이트 같음 | 바이트 같음 | 4.1s |

| SPEC 숫자 | 출처(재현값) | 판정 |
|---|---|---|
| expand 기본 꼴 section 1: 1,902 / 2,710 / 3,228 · 옛 꼴 6,733 / 20,863 / 59,277 | `a_all_pairs.new/old` | ○ |
| 476 걸음 호출 2,014 / 3,676 / 4,720 · 앱 셈 2,146 · 이웃 없는 231: 1,882 / 2,524 · 기록 재계산 475/476(Q113 33B) | `b_v4_calls` | ○ |
| 481 쌍 1,890 / 2,647 · `full` 2,982 / 4,256 / 5,210 · peek 2,257 / 7,171 / 9,477 | `c_676_touched` · `e_other` | ○(W-2) |
| 걸음 재생 1.84 → **3.03** · 분포 17·28·37·66 · 이웃 79 → 131/148 = **88.5%** · 멈춤 budget 110 → 28 · 새 꼴 steps 58 · frontier_empty 28 · enough 21 · empty 13 · 걸음 바이트 15,877 → 10,087 · 줄 38 · 원문 27.5 · cut 14 · cut 받기 5,389 / 14,376 · 합 16,000 / 32,634 | `d_walk.old_replay/new_replay` | ○ |
| 68 = 닿음 5(원문 2 · cut 3) · 안 닿음 34 · 인용 불일치 23 · 되돌아감 6 · 34 의 사유 11 · 2 · 17 · 2 · 2 | `reach_case3` | ○(W-1 · W-3) |
| grid(8줄 1,439 · id 목록형 2,203 · owner 늘 1,935 · 60자 1,930 · 80자 1,940) | `a_all_pairs.grid` | ○ |
| fact 중앙 11자 · 40자 이하 86.1% · 60자 90.8% · 최대 330 · section fact 중앙 11 / p95 47 / 최대 328 · 12줄 넘는 2,752 · 8줄 넘는 3,654 | **json 에 없음.** 검수자가 같은 그래프로 따로 셈: 86.1 · 90.8 · 93.4% · 11 / 47 / 328 · 2,752 · 3,654 | ○(W-5: 근거 파일에 없음) |
| 006: 461행 · 홉 0:63 · 1:218(47%) · 2:151(33%) · 3:24 · 4+:5 · 의도별 순서 표 11행 | `.md` §B | ○ |
| 006: 걸음 판 148 · 예산 멈춤 104(첫 걸음 62 · 대기 이웃 94) · peek 도달 79 · fact 도달 49 · 되돌아감 34(11 + 23 내역) · 「충분」 0/171 · 11/89 · 4/36 · 1/15 · 섹션 단독 중앙(method 8,117 · side_effects 9,793 · aftercare 39,849) | `.md` §A · §C | ○ |
| 006: 섹션 호출 387 · 2,037 / 2,630(80자 줄 · 앱 셈) · 4걸음 합 15,159 / 19,310 | `.md` §C | ○(W-11) |
| 006 stray 15/15 = 64 + 이름 길이(16 + 31 + 17) · 다음 호출이 같은 이름 13 · 입력 빈 10 · 문자열 배열 3 · 정상 2 | `.md` §D · 글자 수 직접 셈 | ○(W-12) |

## 3. FAIL — SPEC-006 v2.2 · WORK-009

### F-1 · 바이트 셈 방법(SPEC-005 V-17) 미정 — §3-4-1 예산 B · §3-4-2 「`bytes` 를 예산 셈에 그대로」 · WORK-009 WP-1/WP-2(기준 1 · peek bytes 정의)

근거:
- 005 §5-16 은 peek `bytes` 를 이렇게 정한다: 「REST 본문(compact 구분자 `(",", ":")`) · `request{id, sections}` · **`intent` 없이**」. 005 는 「호출 쪽이 `intent` 를 넘기면 ≈ 17B 커진다 — 앱 예산 셈과 맞추는 건 **V-17**」(§5-16 · §5-0-1)이라 하고, V-17 의 「누가」 를 **WORK-009** 로 적었다
- 앱 실물: `clinic_chat/cases/case3.py:531` `b = len(json.dumps(d, ensure_ascii=False).encode("utf-8"))`(공백 구분자). 006 §3-4-1 은 허브 호출마다 `intent` 를 넘긴다. 005 측정에서 같은 476 호출이 compact 2,014 · 앱 셈 2,146(+6.6%)
- 006 §3-4-2 · §3-4-1 「섹션 수 · 순서」 는 peek `bytes`(compact · intent 없음)로 선택지를 미리 거르고, 실제 바이트(앱 셈 · intent 있음)가 넘으면 `excluded` 한다. 두 셈 방법이 달라 「peek bytes = 실제」(005 §6-7 (c) 차 0)가 앱에서는 성립하지 않는다. 그래서 `filtered_by_budget` 과 `excluded` 의 경계가 4~7% 흔들린다
- `grep -n "V-17\|compact\|json.dumps" SPEC-006.md WORK-009.md` 결과는 0건이다. §7-9 X 목록에도 없다

방향: 006 §3-4-1 「예산 B」 에 셈 방법을 한 줄로 정한다. 추천은 「expand 응답의 REST 본문 바이트 = compact 직렬화(`separators=(",", ":")` · `ensure_ascii=False`). peek `bytes` 와 같은 셈이다」. `intent` 처리도 하나로 정한다. 섹션 expand 에 `intent` 를 안 넘기거나, 넘긴다면 「peek `bytes` + `len('"intent":"I-0x",')`」로 비교한다고 적는다. 그다음 WORK-009 WP-1 시험에 「모의 · 실물 허브 peek `bytes` == 앱이 센 그 섹션 expand 바이트(차 0)」, WP-2 에 `hub_rest`/`_hub` 셈 변경(Scope `case3.py` 행)을 넣는다. 005 V-17 은 「006 §3-4-1 로 닫힘」 으로 바꾼다.

### F-2 · 원문 받기 예산 `WALK_FULL_BYTE_BUDGET` 12,000 의 근거가 005 측정과 반대 — §3-4-6 끝 단락(기준 2)

근거:
- 006 §3-4-6: 「rerun-v4 걸음 판이 모은 fact 중앙 14 · p95 26 · 그 원문 바이트(전부 받았을 때) 중앙 2,235B · p95 3,903B … 12,000(p95 의 약 3배 · **cut 만이면 여유 큼**)」. 이 값은 원문 **글자 바이트 합**이고 `expand(fact_ids)` 의 응답 바이트가 아니다. 응답 바이트에는 봉투 · `id` · `section` · `owner` · `source{file, path}` 가 행마다 붙는다
- 005 §6-7 (e) · V-15(같은 새 꼴 · rerun-v4 같은 선택 재생 · 재현함): 걸음당 cut 줄 중앙 14 · p95 35 · **cut 줄 원문 받기 응답 바이트 중앙 5,389 · p95 14,376 · 최대 19,233**. 12,000 을 넘는 걸음이 5% 넘게 나온다
- 검수자 셈(b031371c · 6,140 (노드, section) 의 줄 전부): 줄 기준 cut 비율은 40자에서 **23.4%** 다. 고유 fact 기준 13.9% 보다 크다. 긴 fact 가 여러 노드 · section 에 되풀이되기 때문이다. 「40자 이하 86.1%」 는 고유 fact 기준이라 걸음이 실제로 받는 줄의 cut 비율을 작게 보인다
- v2.2 는 걸음이 길어 줄이 더 많다(006 스스로 「2~3배로 늘 수 있어」). 그러니 재생값(옛 선택 기준)보다 더 커질 쪽이다

방향: §3-4-6 끝 단락의 근거를 005 §6-7 (e) 의 cut 받기 응답 바이트(5,389 / 14,376 / 19,233)로 바꾼다. 12,000 을 유지하면 「p95 걸음에서 뒤쪽 cut 줄은 `quotable: false` 로 남는다(재생 기준 12,000 초과 걸음 수 = n)」를 적는다. 아니면 X-2(T-2)에 「`expand(fact_ids)` 실물 응답 바이트로 `WALK_FULL_BYTE_BUDGET` 을 다시 정함」을 더한다. 숫자를 고르는 일은 사용자 · 코디 몫이다. 이 FAIL 은 「여유 큼」 이라는 서술이 측정과 반대라는 점만 지적한다.

### F-3 · 「자료에 없다」 case3 68 / 안 닿은 34 를 v2.2 걸음 순서 규칙이 얼마나 덮는지 셈이 없음 — §3-4-6 · §7-8(기준 4)

근거:
- 005 §6-7 (f) · V-16 은 「안 닿은 34 중 32 는 고름 문제 — 고름은 앱(SPEC-006 · WORK-009)」 이라 하며 006 에 넘겼다. 그런데 `grep -n "자료에 없\|68\|안 닿" SPEC-006.md` 결과는 0건이다. 006 의 셈은 461행(채점 실패 · 골드 hit)을 기준으로 하고, 그 안의 `v4_case3_unknown` 23행(`.md` §B)조차 본문에 인용하지 않았다. §7-8 끝 조건에도 「자료에 없다」류는 「정확성 · 안전 · 정보 없음류 Δ 보고」로만 나온다
- 검수자 셈(읽기 · 결정론 · `spec005-v33-measure.json reach_case3.detail` 34행 × rerun-v4 `walk.start_node` · `walk.intent` × `spec006-v22-count.json order` × b031371c `T.peek` · `_neighbor_edges` · fact 의 owner/attached/엣지 양끝을 목표 노드로):

| 34 행의 자리(시작 노드 S 기준) | 행 | v2.2 규칙이 닿게 하나 |
|---|---|---|
| 1홉 · 그 의도 순서 표 위 3 종류 · **peek 앞 4 안**(걸음 1 선택지에 뜸) | **6** | 선택지에 뜬다. 고를지는 Jev 몫(Q020 · Q027 · Q083 · Q102 · Q117 · Q131) |
| 1홉 · 순서 표 종류지만 **앞 4 밖** | 5 | 안 뜬다. 006 은 `expand(neighbor_kinds)` 를 쓰지 않는다(Q106 · Q124 · Q140 · Q169 · Q233) |
| 1홉 · 순서 표 밖 종류(key_technique · treats · concern_avoid · procedure_relation@I-09 · key_family@I-01) | 5 | 안 뜬다(Q070 · Q114 · Q121 · Q136 · Q198) |
| S 자신의 section(0홉) | 10 | 걸음 1 섹션 ≤ 1 · 돌아옴에서 Jev 가 고를 때만 |
| S 에서 2홉 이상 · 연결 없음 | 8 | 대기열 2홉으로만 닿는다(Q099 · Q133 · Q141 · Q185 · Q200 · Q212 · Q215 · Q239) |

  즉 「이웃 먼저」 순서 표가 구조적으로 선택지에 올리는 것은 34 중 **최대 6**이다. 0홉 10 은 Jev 의 섹션 고름에 달려 있다. 이 셈은 검수자의 근사(목표 노드 = owner ∪ attached ∪ 엣지 양끝)라 정본이 아니다. 하지만 스펙에 이런 셈이 하나도 없다는 점은 확인된다
- 006 §3-4-6 은 461행의 「1홉 47% · 2홉 33%」 로 「이웃 먼저」 를 정당화한다. 같은 근거가 「자료에 없다」 행에 대해서는 0홉 10 · 2홉+ 8 로 분포가 다르다. 걸음 1 을 이웃으로 쓰면 0홉 몫이 늦어진다(X-3 과 같은 맥락)

방향: `spec006-v22-count.py` 에 E 셈을 더한다. 005 `reach_case3` 34행 × 순서 표 → 위 표 꼴(앞 4 안 · 밖 · 표 밖 · 0홉 · 2홉+). 그 결과를 §3-4-6 아래 한 단락으로 붙이고 「기대 상한 = n · 끝 조건 아님」을 적는다. 앞 4 밖 5행 때문에 `neighbor_kinds` 를 쓸지는 §7-9 에 X-9 로 연다(추측으로 메우지 않음).

## 4. WARN

### SPEC-005 v3.3 · WORK-008

| # | 곳 | 무엇 | 방향 |
|---|---|---|---|
| W-1 | §0 마지막 문장 | 「새로 닿는 행 5 — 나머지는 Jev 가 안 고름(28) · 인용 안 맞음(23) · 되돌아감(6) · 6홉 밖(2)」 = 64 ≠ 68. 빠진 것 = 1쪽 밖 2 · 2홉 2(§6-7 (f) 는 11 + 2 + 17 + 2 + 2 = 34 로 맞음) | §0 을 §6-7 (f) 분류 그대로 |
| W-2 | §5-0-1 T10 행 | 「W7-D4 2,271 / 7,248 / 9,506 · v3.3 `n_facts` 더해 2,257 / 7,171 / 9,477」 — 두 값의 기준이 다르다. 스크립트의 옛 peek(같은 코드 · in-process)은 **2,183 / 6,788 / 8,907** 이라, 실제로는 `n_facts` 를 더하면 커진다(+74B 중앙). 그런데 표는 줄어드는 것처럼 읽힌다. 실제 걸음이 연 peek 311 은 3,054 / **8,926**(p95 상한 8,000 넘음 · 예산 밖이라 끝 조건 영향 없음 · `b_v4_calls.peek_new`) | 같은 기준(스크립트 옛 값)과 나란히 적고, 걸음 peek 311 을 보고 칸에 |
| W-3 | §6-7 (f) 「안 닿은 34 의 자리」 | 「시작 노드에서 0홉 13 · 1홉 18 · 2홉 6 · 없음 2」(= 39) · 「정책 B 9」(9 + 30 = 39)는 **닿음 5 + 안 닿음 34 = 39** 기준인데, 34 의 하위처럼 쓰여 있다(json `hops_from_start_to_fact_node` · `policy_b_all_sections_same_nodes`) | 분모 39 를 적음 |
| W-4 | §7 V-11 · V-15 · V-18 | 006 v2.2 가 V-15(원문 = cut 줄만 · 별도 예산 12,000) · V-18(걸음은 1쪽만 · `more` 기록)을 정했고 V-11(`use_first`)은 case3 에서 없어졌다. 그런데 005 §7 은 셋 다 열린 채로 둔다 | 「006 §3-4-1 · §3-4-7 로 닫힘(case3)」 · V-11 은 case2 만 남김 |
| W-5 | §5-16 「값 근거」 | fact 글자 수(중앙 11 · 86.1 / 90.8% · 최대 330) · section fact 수(11 / 47 / 328) · 8줄 3,654 는 `spec005-v33-measure.json` 에 없다(검수자 재계산은 일치). 줄 기준 cut 비율(23.4%)도 같이 내야 40자 선택이 실제 걸음에 주는 영향이 보인다(F-2) | 스크립트 출력에 칸 추가 |
| W-6 | §5-16 입력 `fact_ids` · §6-4 v3.3 행 | ① 「그 노드의 section fact = **peek `n_facts` 가 센 집합**」 — 계열 · 제품은 펼친 단위 fact 도 받는다(`_node_fact_ids`). 그런데 peek `sections[].n_facts` 는 그것을 세지 않는다(단위 수준 section 은 peek 에 없음). ② `sections` + `fact_ids` 를 같이 주면 같은 id 가 줄 · 원문 행으로 두 번 나올 수 있다. 이것이 시험 「fact id 가 응답에 한 번만」 과 충돌한다 | ① 「peek sections ∪ 펼친 단위의 section fact」 ② 겹치면 원문 행만(또는 줄만) 한 줄로 정함 |
| W-7 | WORK-008 front matter `depends_on` | 「WORK-009 — 이 작업의 **WP-1** 꼴 확정 뒤」 인데, 본문 순서 표 · heartbeat 는 **WP-1 · WP-2** 뒤이고 009 가 읽는 peek `bytes` · `n_facts` 는 WP-2 다. heartbeat 문구도 008 「expand 꼴 확정 — WORK-009 착수 가능」 과 009 「v3.3 꼴 확정」 으로 서로 다르다 | front matter 를 WP-2 로 · 문구 하나로 |
| W-8 | WORK-008 §Scope | 표면 grep 3줄째에 `tests/test_gold_tools.py`(286행 `GOLD_SIZE_CAPS` 주석 · `size_caps()["recommend"]` · `GOLD_SIZE_GATE=1` 이면 판정 — v3.3 표로 기대값이 바뀜)가 잡히는데 표에 없다. 또 Scope 의 cap 키 이름(`card_unit` · `card_family` · `pair` · `checks`)이 실물 키(`procedure_card:unit` · `procedure_card:family` · `pair_check` · `check_conditions` — `config.py:80` · `envs/gold.env.example:63`)와 다르다 | 표에 한 줄 · 실물 키 이름으로 |

### SPEC-006 v2.2 · WORK-009

| # | 곳 | 무엇 | 방향 |
|---|---|---|---|
| W-9 | §7-8 「이웃 도달」 · 005 §6-7 (e) | 같은 이름에 정의가 둘이다. 005 = 방문 노드 ≥ 2(peek 도달 · 88.5% · 통과 ≥ 85%), 006 = 이웃 노드 걸음에서 fact ≥ 1(전 33% · 통과 ≥ 80%). 006 §3-4-6 의 「(그쪽 정의)」 한 마디로는 보고서에서 섞이기 쉽다 | 006 은 「이웃 fact 도달」, 005 는 「이웃 peek 도달」 로 이름을 나눔 |
| W-10 | §3-4-1 · WORK-009 Scope | 005 V-16 이 제안한 「peek `n_facts` · `bytes` 를 Choice 입력에」 를 006 이 받지도 버리지도 않았다(앱이 `n_facts` 를 읽기만 함) | §7-9 에 한 줄(채택 안 함 · 이유) |
| W-11 | §3-4-6 예산 표 | 「이웃 slim 1장 300B 가정」(X-2)과 실측이 다르다. rerun-v4 걸음 선택 그대로 b031371c 이웃 행 570장의 크기는 중앙 **250** · p95 **1,014** · 최대 1,178 이다. 걸음 1 이웃 배열(151 호출 · 중앙 3장)은 중앙 752 · p95 2,306 으로, 표의 900 을 쓰면 p95 합 19,310 이 ≈ 20,700 이 된다. 또 표는 걸음 2~4 에서 고른 이웃 expand 를 빼고 셌다 | T-2 에서 위 값과 걸음 2~ 이웃을 같이 다시 셈(X-2 안) |
| W-12 | §3-8 사실 5 | 「첫 도구 호출(resolve) 바로 뒤가 10/15」 — 직전이 resolve 인 것이 10 이고, 2번째 차례인 것은 **7**(Q031 · Q109 · Q115 · Q125 · Q164 · Q235 · Q239)이다. Q066 5/6 · Q167 3/4 · Q172 4/7 은 resolve 를 다시 부른 뒤다 | 「직전 도구 = resolve 10/15 · 2번째 차례 7/15」 |
| W-13 | WORK-009 §순서 의존 | 「WP-0 · WP-4 · **WP-5** 먼저 해도 됨」 이라 했는데, WP-5 는 전체 시험 · 표면 grep 재확인 · case3 걸음 열(WP-2 trace 칸에 의존)이고 발주 순서도 「WP-0~5」 다. 「먼저」 는 WP-5 1(비교 규칙)뿐이다 | WP-5 를 「1 만 먼저 · 2~3 은 끝」 으로 |
| W-14 | WORK-009 WP-0 2 · Scope 끝 | ① `spec006-v22-count.py` 를 「돌려」 표를 옮기라 하는데, 이 스크립트는 **자기 옆(`$W`)에 출력을 덮어쓴다**. 앱 워커가 프로필 레포를 쓰게 된다(결정론이라 바이트는 같다). ② 「grep 31 + grep 밖 5」 인데, 표에는 grep 에 안 걸리는 `README.md` 까지 6개다(grep 재실행 31/31 · 누락 0 은 확인) | ① 커밋된 `spec006-v22-count.json order` 를 그대로 복사, 또는 출력 경로를 레포 밖으로 ② 6 |
| W-15 | §3-8 사실 4 · §7-9 | 「알려진 도구는 CLI 가 스키마로 바로잡는다」 를 **추정**(S-2)이라 하면서 §7-9 X 목록에는 없다(X-7 은 S-1 만) | X-7 에 S-2 를 같이 적음 |
| W-16 | §3-4-6 묶음 대응 | 「계열」 에 `child_of` 를 넣었다. `child_of` 는 고민 · 부위 · 기법 트리 엣지이고 계열 엣지가 아니다. 결정론 표라 동작에는 문제가 없지만, 순서 표가 계열을 고를 때 트리 부모도 같이 뜬다 | 묶음 이름을 「계열 · 상위」 로 하거나 분리 |

## 5. 기준별 확인 메모

- **기준 3 실물**: 허브 cc637a2 `tools.py:2134 peek` · `:2184 expand` · `:2027 warm_sections`(지금 = 원문 합 — SPEC 서술 「실제의 중앙 1/10」 과 맞음: `ratio_old_over_peekbytes` 중앙 10 · p95 165) · 이웃 행 칸 · `_node_fact_ids`. 앱 f8533ff `hub_rest.py:54 peek(node, intent, include_conditional)` · `:59 expand(… fact_ids, intent)`(`full` · `page` 없음 → WORK-009 WP-1) · `case3.py:531` 셈 · `:648/721` 이 `priority` 를 아직 읽음(WP-3 범위). rerun-v4 `trace.walk` 칸 = `start_node · steps[]{k, node, peek_bytes, peek_ms, jev{picked, choice, confidence, enough, …}, expand{sections, neighbors, bytes, ms, fact_ids, calls, excluded}} · stop · bytes_total · fact_ids · jev_calls · fallback · fallback_reason · intent`. 005 §6-7 재생 규칙이 쓰는 `steps[k].node` · `jev.picked` · `stop` 과 006 §3-4-4 의 옛 칸이 일치한다(006 의 새 칸 `phase` · `peek_reused` · `calls[].excluded` 등은 새로 만든다)
- **기준 4 005 끝 조건**: (a)~(h) 모두 산출물 · 통과 값 · 재는 법이 있다. (e) 통과 85% 와 설계 88.5% 의 여유는 3.5%p, (f) 통과 ≥ 5 는 설계 값과 같다(회귀 경계라고 명시). 006 §7-8 도 잴 수 있다(칸이 §3-4-4 에 있음). F-3 은 「셈이 있는가」 에서만 FAIL
- **기준 5**: 006 의 ⑤ 원문 받기는 허브 계약 `allowed: "facts_uncut"` 을 그대로 지킨다(못 받은 cut 줄은 `quotable: false`). 안전 요약은 peek 에서 예산 밖에 늘 들어가고, 이웃 slim 의 `safety` 는 예산 안에 든다. G13 「늘 동봉」 과 충돌하지 않는다
- **기준 6 표면**: 008 grep 4줄을 다시 돌리면 13 · 8 · 8 · 2 파일이다. Scope 표 밖은 `tests/test_gold_tools.py` 1개(W-8). 009 grep 은 31 = 표 안 31(W-14 ②). 넓은 grep(`hub_peek|stages|bytes_total`)에 `clinic_chat/timing.py` 가 잡히지만 기록기일 뿐이라 바꿀 곳이 아니다

## 6. 검수자가 쓴 셈(재현용 · scratchpad · 대상 레포에 안 넣음)

- 두 스크립트 사본: 입력 경로는 원본 그대로 · 출력만 scratchpad · 각 2회 diff
- F-2 · W-5: b031371c 그래프로 fact 글자 수 · 줄 기준 cut 비율 · section fact 수
- F-3: `reach_case3.detail` 34행 × v4 `walk.start_node/intent` × `order.table/group_edges` × `T.peek` items · `_neighbor_edges`(목표 노드 = fact owner ∪ attached_to ∪ owner 엣지 양끝 · 근사)
- W-11: v4 걸음의 `jev.picked` 이웃으로 `T.expand(node, neighbors=…)` 이웃 행 바이트(compact)
