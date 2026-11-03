# 검수 보고서 — SPEC-005 v3.2(0.3.2) · WORK-007

작성 2026-11-01 · 검수자 reviewer 워커(읽기 전용 · 스펙 · 코드 수정 없음 · 실물 호출 없음) · 발주서 `phub-recommend-review-spec005-v32-brief.md`
대상 `SPEC-005.md`(0.3.2 · 11-01 · 1,142행) · `WORK-007.md` · 보충 `phub-recommend-jev-walk-addendum.md` · 전 판 `SPEC-005.v3.1.md`(diff 로 바뀐 441행 전수) · 대조 = `fail-triage2.md` · `.json`(b_rows 186 · c_rows 18 · meta) · `runs/runs.jsonl`(rerun-v3 182) · `build-out/recheck/replay2.json`(676) · 허브 코드 c95b37a(`tools.py` · `facts.py` · `config.py` · `mcp_server.py` · raw `mcp_server.py` · `schema/gold.py`) · `gold-export.json`(d3a1abd5 · facts 14,891 · edges 13,178) · `mcp` 2.3 `MCPServer.tool` 시그니처 · SPEC-006 v2 §3-4 · `_RESUME.md` §2 11-01

## 판정 — **FAIL** (FAIL 3 · WARN 6)

한 줄: B 186 ↔ §8 표는 행 단위로 1:1 이고(161 닿음 · 25 닫지 않음 · fail-triage2 의 문항 · 케이스 · 항목 · 빠진 칸 전부 일치) 실물 이름 · fact id · meta 시그니처 · 1-hop 중앙 94 도 맞다. FAIL 은 ① peek · expand 의 `intent` 인자가 SPEC-006 v2 와 반대(허브는 「받지 않음」 · 앱은 「넘긴다」) ② 끝 조건 (iii) C3 가 fact 없는 행 5 를 fact 로 재려 하고 셈(6)도 틀림 ③ WORK-007 이 WORK-006 과의 순서 · 계약 의존을 적지 않음 — 세 가지다.

| 기준 | 판정 | 요지 |
|---|---|---|
| 1 전수 대조(B 186 · C3) | PASS(§8) / **FAIL(C3 → F-2)** | §8 표 186행 = `b_rows` 186 과 (문항 · 케이스 · 항목) 1:1 · 빠진 칸 문자열 186/186 같음 · 조항 열 C7′ 40 · C2′ 32 · §5-14′ 29 · F-F 18 · C3′ 14 · C14′ 11 · C9′ 8 · C6′ 4 · C1′ 3 · C4′ 1 · F-D′ 1 = **161** · X0 16(허브 안 부름 15 + resolve 만 1 — Q176 c3 포함 · 실물 tools_called 빈 행과 같음) · N 9(9단계 3 · 조항 없음 2 · 제품 수준 2 · 다른 계열 2) = **25**. 대응 없는 행 0. C3 8 은 조항(C1′ · C10′ · §5-14′)으로 닿지만 끝 조건 (iii) 의 판정 · 셈이 안 닫힘(F-2) |
| 2 실물 대조 | PASS | 도구 9 시그니처에 `intent` 있음 · `Shape(sections, intent, tool)` · SECTIONS 17 · `INTENT_DESC` 현 문구 = 스펙 인용과 같음 · `mcp` 2.3 `tool(…, meta=…)` 인자 있음(지금 `annotations` 만) · raw 3 도 `annotations` 만 · 단위 시술 1-hop 엣지 중앙 **94**(p95 185 · 최대 275) · F-F 24 fact id(21줄 · 제품 접두 3줄은 prefix 로 5 · 16 · 6건) **전부 export 에 있음** · `attached_to` 칸 있음 · `family:M7 sections.recovery` 2건 실물 · F-D′ 잎(patientExplanation · severity_levels.*) 은 지금 0 → 「새로 만든다」 와 일치 · `scope:all#evidence#sequence_rank[*]` 11 ✓ · 부속 셈 2곳 어긋남은 WARN(W-1 · W-2) |
| 3 보충 대조 | **FAIL(F-1)** | peek ≤ 2KB(중앙 · p95 4KB) · expand ≤ 8KB · 걸음 ≤ 4 BFS(§6-6 d(f) 정의 · 시작 노드 = resolve 후보) · case3 경로 20K/60K · 걸음 · 예산 · 되돌아가기는 앱 몫 — 숫자는 SPEC-006 v2(§3-4 `WALK_MAX_STEPS=4` · `WALK_BYTE_BUDGET=20000` · peek ≤ 2KB) · v32 브리프(20KB/60KB)와 같음. **이름 · 인자는 어긋남**: SPEC-006 §3-4-1 「걸음 중 허브 호출에 `intent` 를 넘긴다」 · §3-4-2 `peek(node, intent?)` · `expand(…, intent?)` ↔ SPEC-005 M-3 「T10 · T11 은 `intent` 를 받지 않는다」 · WORK-007 시험 「peek · expand 인자에 intent 없음」 |
| 4 결정표 충돌 | PASS | LLM 없음(peek · expand · priority 전부 규칙) · 결정론(이웃 순서 고정 · 동순위 id 순 · 두 번 같음) · G13(peek 에 `compact_safety` 그대로 · 다이어트 밖) · slim(원문은 요청 자리만 · id 전부) · 실버 수정 없음(F-D′ 는 빌드 · A 54 는 9단계) · 충돌 하나 유지 — 어긋남 0 |
| 5 끝 조건 검증 가능성 | **FAIL(F-2)** | (i) 676 = `meta.replay_unique` ✓ · 분모 161 = §8 X0 · N 아닌 행 ✓ · 판정 = recheck 식 + 엣지 id + 응답 전체 id 집합(명시) ✓ (ii) 상한은 §5-0-1 표 숫자 · 「sections 없음」 정의 ✓ (iv)(v)(vi) 결정론 · 두 번 ✓ · (iii) 는 F-2 |
| 6 WORK-007 | **FAIL(F-3)** | WP 순서(0 측정 도구 → 1 다이어트 → 2 동봉 → 3 매핑 → 4 peek/expand → 5 meta → 6 측정 → 7 검증) · WP 마다 시험 · 검증 명령 · Done ↔ §6-5 (i)~(vii) 1:1 ✓ · 코드 표면은 「WP-0 grep 전수 → 표에 더함」 규칙 + grep 명령 4 ✓(지금 돌리면 무관 모듈 5 파일 — W-4). **WORK-006 과의 의존 미명시**(F-3) |
| 7 추측 자리(V-3 · V-8~V-12 밖) | WARN | §5-16 의 고정 숫자(이웃 앞 8 · 이름 20자 · `fact_ids ≤ 64` · 종류 순서 표)가 V 밖(W-6) · 나머지는 V-3 · V-8~V-12 안 |

## FAIL

### F-1 · SPEC-005 §5-0-2 M-3 · §5-16 ↔ SPEC-006 v2 §3-4-1 · §3-4-2 — peek · expand `intent` 인자가 두 스펙에서 반대(기준 3)

근거: SPEC-005 M-3 「T10 peek · T11 expand 는 `intent` 를 **받지 않는다**」 · §5-16 입력 칸에 `intent` 없음 · WORK-007 WP-5 시험 「peek · expand 인자에 intent 없음」. SPEC-006 v2 §3-4-1 의도 행 「걸음 중 허브 호출에 `intent`(②)를 넘긴다 — 단 의도 묶음 · 동봉은 쓰지 않는다(`sections=none` 꼴)」 · §3-4-2 `peek(node, intent?)` · `expand(node, sections[] | neighbor_ids[], intent?)` · WORK-006 WP-3 시험 「걸음 판은 `intent` 넘기되 `sections=none` 꼴」. REST GET 은 모르는 쿼리를 버리지만 MCP `tools/call` 은 스키마 밖 인자로 **오류**가 되고, 앱 `hub_rest.py` 가 REST 로 가더라도 두 문서의 계약이 반대라 WORK-006 · WORK-007 시험이 서로 다른 것을 고정한다. 같은 표에서 이웃 꼴도 다르다 — SPEC-006 `neighbors[]{id, kind, edge, label}`(평면) ↔ SPEC-005 `neighbors_by_kind{edge kind: {n, direction, items[:8]{id, kind, name, label}}}`.
방향: 한쪽으로 맞춘다. 추천 = SPEC-005 가 `intent?` 를 **받되 무시**(`intent_used: null` · 동봉 · 묶음 안 붙임 — 「선택 가능 유지」 문구와도 맞음) 하고 §5-16 입력 칸 · M-3 · WORK-007 WP-5 시험을 「받아도 영향 0」 으로 고친다. 이웃 꼴은 SPEC-006 §3-4-2 를 `neighbors_by_kind` 로 바꾸거나 SPEC-005 §5-16 에 「앱이 읽는 최소 칸 대응(평면 = items 펼침 · edge = kind 키)」 한 줄.

### F-2 · SPEC-005 §6-5 (iii) · WORK-007 Done (iii) — C3 끝 조건이 fact 없는 행을 fact 로 재고 셈도 틀림(기준 1 · 5)

근거(`fail-triage2.json c_rows` · `c_sub == C3` 8행): fact id 가 있는 행은 **3** 뿐(Q003 c2 · c3 `SC-jawline-M1#site_caution#spec.key_warning` · Q069 c2 `combo:RC-CP-wrinkle#evidence#members[3].attrs_text.duration`). 나머지 5(Q014 c2 · Q190 c3 · Q221 c3 = `via: 인용 문자열` · Q054 c3 · Q203 c2 = `via: 골드 문장`)는 `fact` · `section` 칸이 비어 있다 — 허브 응답 본문 어딘가의 문자열(노드 이름 · 속성 · facts 본문)이 인용과 맞았을 뿐이다. 스펙 (iii) 「그 fact 가 같은 입력 재실행 응답에서 `sections_used` 안 section 원문 또는 동봉 원문에 있음」 은 이 5행엔 fact 도 section 도 없어 판정이 서지 않는다. 셈도: 8 − Q003 2(반대 조건) − Q203 1(vocab 밖) = **5** 인데 「6/6」 · WORK-007 Goal 「C3 8 중 6」.
방향: (iii) 판정을 「정규화 인용(triage 와 같은 norm)이 재실행 응답의 `facts[].text` ∪ 동봉 원문 칸(`claims_text` · `key_warning` · price · expectedResult · C10′ 멤버 원문) 안에 있음 — 응답 본문 아무 데나는 아님」 으로 적고, 분모 5 · 통과 5/5 + Q003 2 반대 조건으로 고친다. 다이어트 뒤에는 노드 속성 문자열이 응답에서 빠질 수 있으므로 「인용 문자열」 행이 원문 칸으로 닫히는지가 바로 이 조건의 뜻이다.

### F-3 · WORK-007 depends_on · WP-4 · WP-5 — WORK-006 과의 순서 · 계약 의존이 없음(기준 6)

근거: `depends_on` 은 WORK-005 뿐. WORK-006 은 비목표 · WP-6 5 「SPEC-006 v2 WP-0 확인 시험 기록이 먼저 있으면」 · Open Issues 에만 나온다. 실제 의존: WORK-006 WP-0(메타 빌드가 18005 에 있어야 (a) 근거가 섬) ← WORK-007 WP-5 · 발행 / WORK-006 WP-3(peek · expand 모의라도) ← WORK-007 WP-4 응답 꼴 확정 / `intent` 인자 · 이웃 꼴 계약(F-1) ← 두 planner 합의. 발주서(브리프) 기준 6 이 묻는 「meta · intent 문구 · peek/expand 먼저」 가 WORK-007 어디에도 순서로 적혀 있지 않다.
방향: `depends_on` 에 「SPEC-006 v2 §3-4-2 · §3-5 · §3-6(앱 쪽 소비자)」 · WP-4 완료 조건에 「SPEC-006 §3-4-2 최소 칸 대응표(neighbors id · kind · edge · label / sections name · n_facts · bytes / facts id · text · section) + `intent` 인자 처리」 · WP-5 완료 조건에 「WORK-006 WP-0 이 쓸 빌드 → 코디 재시작 요청」 · Related 에 「WORK-006 WP-0 · WP-3 는 이 WP-5 · WP-4 뒤」 한 줄.

## WARN

| id | 조항 | 내용 · 방향 |
|---|---|---|
| W-1 | §5-0-1 A1-9 표 「현(rerun-v3 · case3 중앙 / case2 중앙)」 열 | 출처가 섞여 있다 — case3 중앙(53,175 · 59,350 · 27,784 · 96,886 · 32,405 · 41,342)은 `runs.jsonl` case3 호출 중앙과 **일치** · 「case2 27,216」 은 `rerun-report` 의 문항당 합(per-run)이고 · 나머지 case2 값(15,912 · 15,439 · 39,406 · 25,455 · 24,820 · 7,662 · 1,174 · 6,473)은 WORK-005 측정값. `replay2.json`(676) 의 case2 호출당 전체 바이트 중앙은 recommend 16,826 · card 29,074 · pair 16,397 · checks 78,605 · compare 25,720 · combos 24,929 · neighbors 6,580 · resolve 1,106 · vocab 5,660. 참고 열이라 끝 조건엔 영향 없음 — 출처를 열 머리에 적거나 replay2 값으로 통일 |
| W-2 | §5-16 상한 행 「1-hop 중앙 94(procedure_pair 69 · requires_check 12 · has_statement 11 · product_unit 11 · combo_component 7)」 | 총 중앙 94 는 맞음(p95 185 · 최대 275). 종류별 숫자는 중앙 단위(U5-092: pair 72 · requires_check 9 · treats 4)도, 종류별 중앙(67.5 · 10.5 · 4 · 3 · 0)도, 평균(57.9 · 9.9 · 7.5 · 8.8 · 3.6)도 아님 — 셈 규칙을 적거나 종류별 중앙으로 |
| W-3 | §3-0 「미닫힘 34 … `not-closed-why.json` 이 날 코디 워크스페이스에 없음 — 사유별 셈만 반영」 | 파일은 `reference/2026-10-30-hub-evals/build-out/recheck/not-closed-why.json` 에 있다(77행 — WORK-005 1차 바퀴 미닫힘 77 · 범위 한정 바퀴 34 는 그 부분집합인지 확인 필요) — 행 단위 처분을 §8 과 같은 꼴로 붙일 수 있음(선택) |
| W-4 | WORK-007 WP-0 grep 1 | 지금 레포에 돌리면 무관 모듈 5(`app/model/canonical_publication.py` · `app/modules/retrieval/{application,domain}.py` · `app/schema/knowledge_retrieval.py` · `tests/test_retrieval_domain.py`)와 grep 2 의 v1 `app/modules/graph/mcp_server.py` 6 도구가 잡힌다 — 「골드 앱이 import 하지 않는 모듈은 영향 없음으로 표에 적고 meta 대상 아님」 한 줄(14 도구 셈이 흔들리지 않게) |
| W-5 | §4-3 F-D′ · WORK-007 WP-2 | 더하는 잎(patientExplanation · severity_levels.sequence · rationale · contraindicated_combos · expected_sessions)은 실물 0 → 새 fact 맞음. 가드에 **기대 셈이 없다**(F-D 는 「조합 79 × 잎 전부」) — WP-2 완료 조건에 `counts.v3_facts.fd2_*` 원문 · 중증도 조합 24 × 잎 셈 |
| W-6 | §5-16 고정 숫자 | 이웃 앞 8(`GOLD_PEEK_ITEMS_PER_KIND`) 은 설정이나 **이름 20자** · `fact_ids ≤ 64` · `neighbors ≤ 255` · 종류 고정 순서 표는 본문 상수 — V-3 「손잡이」 목록에 넣거나 설정 이름을 붙임(WORK-007 Meta 「코드 상수로 박지 않는다」 와 맞게) |

## 부록 A — B 186 ↔ §8 대조(기준 1)

| 항목 | 값 |
|---|---|
| §8 행 수 / `b_rows` | 186 / 186 · (문항 · 케이스 · 항목) 키 186 = 186 · 빠진 칸 문자열 불일치 0 |
| 조항 닿음 161 | C7′ 40 · C2′ 32 · §5-14′ 29 · F-F 18 · C3′ 14 · C14′ 11 · C9′ 8 · C6′ 4 · C1′ 3 · C4′ 1 · F-D′ 1(합 161 — WORK-007 Done (i) 의 조항별 셈과 같음) |
| 닫지 않음 25 | X0 16(= `tools_called` 빈 행 15 + resolve 만 Q082 c2 · fail-triage2 의 「허브 안 부름 14」 + Q176 c3(b_kind 는 범위 밖 21 로 적혔으나 호출 0) + resolve 1) · N 9 = 9단계 3(Q106 c3 technique · Q189 c2 · c3 combo severity) · 조항 없음 2(Q082 c3 package evidence · Q228 c2 product basis) · 제품 수준 2(Q124 c3 ×2) · 다른 계열 2(Q167 c3 · Q172 c2) |
| C 18 → C3 8 | 조항 = C1′(Q003 ×2 반대) · C10′(Q069) · §5-14′ / 인용 문자열(5) — 끝 조건 (iii) 는 F-2 |

## 부록 B — 실물 대조(기준 2)

| 스펙 | 실물 | 결과 |
|---|---|---|
| 도구 9 `intent` 입력 · `Shape(sections, intent, tool)` · `TOOL_DEFAULT_INTENT` | `tools.py` 846~1794 전부 · `INTENTS` 12 · `INTENT_IDS` | ○ |
| section 17 · `UNIT_LEVEL_SECTIONS` 8(by_unit) | `facts.SECTIONS` 17 · `tools.py:87` | ○ |
| M-1 `MCPServer.tool(meta=)` · 지금 `annotations` 만 · raw 3 도 | `mcp` 2.3 시그니처에 `meta` · gold 9 + raw 3 전부 `annotations=_READ_ONLY` 만 | ○ |
| M-2 현 `INTENT_DESC` 문구 | `schema/gold.py:12` 「의도 코드 I-01~I-12(v3 · 선택) — … 없으면 도구 기본 의도」 같음 | ○ |
| 손잡이 현값(6 · 36 · 12 · 20 · 3 · 4 · 6 · 10 · 5 · 5 · 5 · 2 · 3) | `config.py` 35~49 · `PAIR_EXPAND_MAX=30` · `COMPARE_UNITS_MAX=8` | ○ |
| F-F 24 fact id | 19 개 완전 id 전부 export 에 있음 · 제품 접두 3(auto-M11 aftercare 5 · M8-4-1 side_effects 16 · aftercare 6) 있음 · owner · section 스펙과 같음 · `attached_to` 는 비교 조합 멤버 2건만 채워짐 | ○ |
| F-D′ 잎 실물 0(새) · `sequence_rank` 11 · combo facts 734(evidence 492 · overview 121 · timeline 88 · market 27 · checks 6) | export | ○ |
| 1-hop 중앙 94 | 재계산 94(p95 185 · 최대 275) | ○(종류별 W-2) |
| 676 · 186 · 18 · case3 중앙 46,539 · p95 170,989 | `meta.replay_unique` 676 · `b_rows` 186 · `c_rows` 18 · `case3_sizes` | ○ |

## 부록 C — 보충 ↔ SPEC-005 v3.2 ↔ SPEC-006 v2 숫자 · 이름(기준 3)

| 항목 | 보충 | SPEC-005 v3.2 | SPEC-006 v2 | 일치 |
|---|---|---|---|---|
| peek 크기 | ≤ 2KB | 중앙 ≤ 2,000 · p95 4,000 | ≤ 2KB 중앙 | ○ |
| expand 1회 | 「크기 추가」 | 중앙 ≤ 8,000 · p95 16,000 | — | ○(허브 몫) |
| 걸음 | N 4 | §6-6 d ≤ 4 · (vi) | `WALK_MAX_STEPS=4` | ○ |
| 예산 | B 20KB | case3 경로 중앙 ≤ 20,000 · p95 60,000 | `WALK_BYTE_BUDGET=20000` | ○(60K 는 v32 브리프) |
| 도달 비율 | B 186 fact 도달 가능 비율 | 161 중 ≥ 90% · 186 보고 | — | ○ |
| peek 출력 | 요약 + 이웃 목록 + 섹션 목록 | `neighbors_by_kind{…items[:8]}` · `sections[]{name,n_facts,bytes}` | `neighbors[]{id,kind,edge,label}` · `sections[]{name,n_facts,bytes}` | △(F-1 이웃 꼴) |
| `intent` | — | 받지 않음(M-3) | 넘김(`intent?`) | **✗(F-1)** |
| 되돌아가기 | 의도 묶음 1회 | 허브 변경 없음 | §3-4-3 | ○ |
