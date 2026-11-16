---
type: spec
id: SPEC-005
title: "허브 골드 그래프 · 결정론 도구 — 실버 · 시맨틱 → 골드 빌드 · 저장 · REST/MCP 도구 9 · 골드 E2E"
status: draft
product: procedure-hub
feature: phub-recommend
version: 0.3.4
created_at: 2026-10-30
updated_at: 2026-11-01
replaces:
  - "SPEC-004"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (10-26 경계 · 10-27 W-1 · 10-29 reading_contract · 10-30 전 행)"
  sources:
    - "orchestration/work/phub-recommend/semantic.json"
    - "orchestration/work/phub-recommend/step1-products.json ~ step8-relations.json"
    - "orchestration/work/phub-recommend/gold-research.md · gold-research.json"
    - "orchestration/work/phub-recommend/quality-eval.py · quality-eval-set.json · quality-report.md"
  work:
    - "orchestration/work/phub-recommend/WORK-003.md"
    - "orchestration/work/phub-recommend/WORK-005.md"
    - "orchestration/work/phub-recommend/WORK-007.md"
    - "orchestration/work/phub-recommend/WORK-008.md"
  evals:
    - "reference/2026-10-30-hub-evals/build-out/fail-triage.md · fail-triage.json(B 239 · 오류 15 — v3 근거)"
    - "reference/2026-10-30-hub-evals/build-out/fail-triage-scripts/{replay,triage}.py(v3 끝 조건 대조 스크립트의 바탕)"
    - "reference/2026-10-30-hub-evals/build-out/rerun-report.md · fail-triage2.md · fail-triage2.json(rerun-v3 2차 분류 · B 186 · C 18 · 크기 — v3.2 근거)"
    - "reference/2026-10-30-hub-evals/runs/runs.jsonl(batch b202610311552-d39a4d · rerun-v3 실제 호출 676)"
    - "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/work005-report.md(WORK-005 구현 보고 · SPEC 과 다른 곳 14 · 미닫힘 34)"
    - "orchestration/work/phub-recommend/phub-recommend-jev-walk-addendum.md(사용자 결정 11-01 · case3 = Jev 재귀 탐색으로 교체)"
    - "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/work007-report.md(WORK-007 구현 보고 · 코드 cc637a2 · 빌드 b031371c · SPEC 과 다른 곳 D-1~D-13 · 더 줄일 자리 6 — v3.3 근거)"
    - "reference/2026-10-30-hub-evals/runs/runs.jsonl(batch b202611011148-c6ed3a · rerun-v4 · case3 trace.walk) · build-out/work006-report.md · rerun-v4-vs-v3.{md,json} · verify-b202611011148-c6ed3a.{md,json}"
    - "orchestration/work/phub-recommend/phub-recommend-walk-fix-context.md(11-01 사용자 승인 「발주하자」 · case3 걷기 살리기)"
    - "orchestration/work/phub-recommend/spec005-v33-measure.py · spec005-v33-measure.json(v3.3 숫자 근거 — 결정론 · 두 번 같음)"
---

# SPEC-005 — 허브 골드 그래프 · 결정론 도구

> 검수 반영 2026-10-30(F-1 ~ F-5 · W-1 ~ W-9) — `review-spec005-report.md`
> **v3.3 2026-11-01(0.3.4) — expand 를 걷기용으로 · WORK-007 실물 반영(D-1~D-13) · 크기 표를 측정값으로** — 근거 `phub-recommend-walk-fix-context.md`(rerun-v4 case3 걸음 중앙 1 · 예산 멈춤 64% · expand 한 섹션 2.6~55KB) · `work007-report.md` · `spec005-v33-measure.json`. v3.2.1(0.3.3)은 `SPEC-005.v3.2.1.md` 로 보관. 바뀐 조항 = §0 · **§3-0(W7-D1~W7-D13 표)** · §5-0(안전 요약 단위 상한) · §5-0-1(A1-3 · A1-6 · A1-7 · A1-9 표 = 측정값 · case3 경로 행 삭제) · §5-13 C′ 표(기본 응답 = 셈 · C3′ 정렬 · C2′ edges) · §5-14′(`sections_index` 꼴) · **§5-16(T11 expand = fact 한 줄 목록 · `full` · `page` · peek `bytes` = 실제 expand 바이트 · 이웃 `n_facts` · 앞 4)** · §6-4 · §6-5((i) (a)∪(b) · 분모 155 · (iii) 원문 칸 · (v)) · **§6-7(새 · v3.3 끝 조건 · 걸음 재생)** · §7(V-3 · V-13 닫음 · V-14~V-18 · 검수 패치 V-15 · V-17 · V-18 닫음 · V-11 case2 만) · §8(155 · Q003). 실버 · 시맨틱 수정 없음
> **v3.2.1 2026-11-01(0.3.3) — 검수 반영(`review-spec005-v32-report.md` F-1~F-3 · W-1~W-6)** — 바뀐 곳: §5-0-2 M-3 · §5-16(peek · expand 가 `intent?` 를 **받되 무시** · 이웃 꼴 `neighbors_by_kind` 로 통일 + SPEC-006 §3-4-2 최소 칸 대응 · 고정 숫자 → 설정 이름 · V-13) · §6-5 (iii)(C3 = fact 있는 행 3 + 인용 문자열 행 5 · 판정 식 · 셈 5/5 + Q003 2) · §5-0-1 표 「현」 열 출처 = `replay2.json` · §5-16 1-hop 종류별 셈 규칙 · §3-0 미닫힘 표(`not-closed-why.json` 77행 실존) · §4-3 F-D′(실물 = `combos[].consult_copy.patientExplanation` 7 · 가드 7) · WORK-007 의존(WORK-006 WP-0 · WP-3 순서)
> **v3.2 2026-11-01 — 응답 다이어트(A-1) · B 잔여 186 의 조항 대응(A-2) · peek/expand(Jev 재귀 탐색 · 사용자 결정 11-01) · MCP 전달 계약(코디 보충 2 · §5-0-2) · WORK-005 구현 실물 반영** — 근거 `rerun-report.md` · `fail-triage2.md`(정본) · `work005-report.md` · `phub-recommend-jev-walk-addendum.md`. v3.1(0.3.1 · 검수 FAIL 경미 1 → 반영)은 `SPEC-005.v3.1.md` 로 보관. 바뀐 조항 = §0 · §3-0(W5-D1~W5-D14 · 미닫힘 34) · §4-3(F-D′ · F-F) · **§5-0-1(새 · 다이어트 규칙 A1-1~A1-9 · 도구별 상한 표)** · §5-3~§5-9 · §5-13(C1′~C14′) · §5-14(묶음 밖 id 노출) · §5-15 · **§5-16(새 · T10 peek · T11 expand)** · §6-4 · **§6-5(v3.2 끝 조건)** · **§6-6(새 · 걸음 도달)** · §7(V-3 · V-6 · V-7 재정의 · V-8~V-11) · **§8(새 · B 186 ↔ 조항 표)**. 실버 · 시맨틱 수정 없음(A 54 는 9단계)
> 보강 2026-10-30(raw-mcp · O-1~O-4) — `_RESUME.md` §2 10-30 「원장도 MCP 로」 · 「SPEC-005 열린 것 O-1~O-4 추천대로」
> **v3.1 2026-10-31 — 검수 반영(`review-spec005-v3-report.md` F-1~F-8 · W-1~W-8 · 코디 결정 위임)** — 바뀐 곳: §2-2 family_text 문구 · §4-3 F-A ⑤ 연결 키 · F-C treats · F-D pih 칸 · W-7 열거 · §5-13 C2 · C3 종류 이름 · 의도 × 동봉 표(I-06 C7 · C14 · C11 / I-07 · I-09 C12 / I-11 C2) · §5-14 표(근거 열의 section 전부 묶음에) · §5-15 문턱 → V-6 · §6-5(분모 205 · 판정 = 새 export 로 gold_match 재실행 · 셈 규칙 · case3 201 · 「닫지 않는 행」 19 · 목표 = 조항이 닿는 행의 ≥ 90%) · §7 V-1 숫자 · V-6 · V-7
> **v3 2026-10-31 — 허브 응답 설계 수정(전달 문제 B 239건 + 오류 15건)** — `fail-triage.md`(정본) · `_RESUME.md` §2 10-31 「고칠 순서 1 허브 응답 설계」. v2(0.1.0 · 검수 PASS)는 `SPEC-005.v2.md` 로 보관. 바뀐 조항 = §0 · §3-0(v3 행) · §4-3(F-A~F-E) · §5-0 · §5-3~§5-9 · **§5-13 · §5-14 · §5-15(새)** · §6-1 · **§6-5(새)** · §7. A(골드에 없음 61)는 실버 9단계(다음 단계) — 이 스펙 밖

SPEC-004 · WORK-002 를 대체한다. 옛 스펙 · 그래프 v2 와 대조하지 않고 새로 쓴다(_RESUME §2 10-29 「처음부터」).
근거는 아래 정본만이다. 결정을 다시 논의하지 않고, 열린 것은 §7 에만 둔다.

| 정본 | 무엇 | 이 스펙에서 |
|---|---|---|
| `_RESUME.md` §2 | 결정표 | 경계 · 기본 응답 · 충돌 · 품질 목표 · 골드 판단 ①~⑤ · D-01~D-14 |
| `semantic.json` | 노드 13 · 엣지 21 · 사전 2,053 · resolve_rules · id 대응 1,071 · 상속 9 · 표시 12 · gate 3값 | 골드 빌드의 뜻 · id · 읽는 규칙 |
| `step1` ~ `step8` json | 실버 | 골드 빌드 입력(§2) |
| `gold-research.md` · `.json` | 골드 규칙 G1~G17 · 의도 12 · 도구 9 · 경로 11 · 패널 · 속도 장치 | §3 · §5 의 뼈대(정정 3곳 — §3-0) |
| `quality-eval.py` · `quality-eval-set.json` · `quality-report.md` | 품질 3차 · 문항 111 | 골드 E2E 의 정답 세트(§6) |

## 0. 요약

- 허브 = **골드 그래프 + 결정론 조회 도구 9**(REST · MCP 같은 코어). LLM 없음
- 골드 = 실버 · 시맨틱에 규칙 18(gold-research G1~G17 정정 반영 + G18 메뉴 라벨)을 적용해 **빌드 때 단위 시술 수준으로 펼친 그래프**(D-01). 요청 때는 메모리 조회만
- 앱이 읽는 시술 쌍 값 · 확인 조건 등급 · 대기 기간은 8단계 `resolved` 하나뿐(10-30 충돌 하나로). 원문 주장은 근거 · alternatives 로만
- 안전 묶음(부작용 · 합병증 · 확인 조건 · 위험지대 · 금기류 관계 · 피함 · 응급 징후 · 필수 고지 · gap 상태)은 시술이 응답에 나오면 거르기와 무관하게 늘 동봉(10-26)
- 완료 조건: 품질 측정을 **골드 도구 위에서** 다시 돌려 목표 6/6 유지 + 지금 남은 틀림 4문항(Q106 · Q108 · Q109 · Q110)도 맞음 · 로컬 서버 실물 호출 · 속도 측정(§6)
- **v3.3(expand 를 걷기용으로 · 실물 반영 · 측정값 표)**: rerun-v4(182 · 허브 b031371c · 앱 f8533ff)에서 case3 정확성 57→49% · 걸음 수 중앙 1 · 멈춤 = 예산 104/148(걸음 판 · 되돌아감 포함 116/182). 원인 = expand 한 섹션이 fact 메타 · id 5중(`sections[s].facts` · `facts[].id` · `allowed` · `priority` · `use_first`) · `source.meta` 포함 원문 전체라 **섹션당 중앙 6,733B · p95 20,863 · 최대 59,277**(전 6,140 노드 × section · `spec005-v33-measure.json` a) → 20KB 예산을 첫 걸음에 씀 · peek `sections[].bytes` 는 원문 글자 합이라 실제의 중앙 1/10(p95 1/165). 그래서 ① **T11 expand 기본 꼴 = fact 한 줄 목록**(`facts[]{id, line ≤ 40자, section, owner?}` · 1쪽 12줄 · `more` 셈 · 원문은 `full=true` 또는 `fact_ids` 로만 · §5-16) — 섹션당 **중앙 1,902 · p95 2,710**(측정) ② **peek `sections[].bytes` = 그 section 의 실제 expand 기본 응답 바이트**(봉투 포함 · 차 0) ③ peek 이웃 줄에 **`n_facts`**(결정론 셈 · 「답이 많은 곳」 추측 표시 없음) ④ WORK-007 이 SPEC 과 다르게 한 13곳(D-1~D-13 · 코디 11-01 결정)을 본문으로(§3-0 W7-D) ⑤ §5-0-1 크기 표 = **WORK-007 측정값**(이번 판 결정). 걸음 재생(rerun-v4 의 같은 선택 · 새 꼴 · Jev 없이)으로 평균 걸음 1.84 → 3.03 · 이웃 도달 53% → 89% · 「자료에 없다」 case3 68행 중 새 꼴로 새로 닿는 행 5 — 나머지 63 = 새 꼴로도 안 닿음 34(방문 노드인데 Jev 가 그 section 을 안 고름 11 · 그 section 펼침 · 1쪽 밖 2 · 방문 노드에서 1홉 17 · 2홉 2 · 6홉 안 연결 없음 2) · 골드 fact 와 인용이 안 맞음 23 · 되돌아감 6 이라 **허브 꼴로는 더 못 닫는다**(§6-7 (f) 분류 그대로 · §7 V-16)
- **v3.2(다이어트 · 잔여 · 걸음)**: rerun-v3(182문항 · 골드 d3a1abd5)에서 case3 정확성 37→57% 로 올랐지만 허브 결과가 11.9KB→46.5KB(중앙 · p95 171KB · 최대 281KB)로 커졌고 C(허브가 줬는데 놓침)가 1.9%→6.6% · 크기 구간별 0%→10% 로 늘었다(`fail-triage2.md` §2 · §5). 그래서 ① **응답 다이어트(§5-0-1)** — 동봉 · 섹션 원문은 「질문의 부위 · 의도 · 요청 노드」에 맞는 것만, 나머지는 **id 만**(`more_ids` 로 다시 받기) · 도구별 기본 응답 상한을 숫자로(2.5× 폐기) · `claude_contract` 에 우선순위 칸 ② **B 잔여 186 ↔ 조항 1:1**(§8 · 조항 닿는 행 161 · 닫지 않는 행 25) — 이웃 노드 51 은 id 전부 노출 규칙(C2′ · C7′ · C6′ · C3′) · 기본 묶음 밖 섹션 33 + Jev 안 고름 12 + 상위 4 밖 5 는 묶음 밖 id 노출(§5-14′) · 섹션 매핑 밖 24 는 fact id 열거(F-F) · step8 메모 10 · 쌍 evidence 8 · 엣지 속성 6 · 경로 안 닿음 13 은 조항 또는 「닫지 않는 행」 ③ **case3 = Jev 재귀 탐색으로 교체**(사용자 11-01 · 추가 아님) — 허브는 `peek` · `expand` 응답 꼴(§5-16 · 결정론 · LLM 없음)과 끝 조건(peek ≤ 2KB 중앙 · expand 1회 ≤ 8KB 중앙 · 걸음 4 안 도달률 §6-6)을 갖고, 걸음 상한 · 예산 · 되돌아가기 · 기록은 SPEC-006 v2 몫. 의도 묶음 · 동봉 자동 첨부는 case2(Claude MCP) 기본 응답에만 쓰고 case3 경로에선 안 쓴다(선택 가능 유지)
- **v3(응답 설계)**: 도구마다 `intent`(I-01~I-12)를 받아 ① 의도별 **섹션 기본 묶음**(§5-14 · B ① 53) ② 의도별 **고정 동봉**(§5-13 · B ⑤ 90 · ⑦ 20) 을 slim 원칙 안에서 같이 낸다 · 쌍 도구는 evidence 원문을 기본 포함하고 입력 1개 · 계열 · 제품도 받는다(§5-5 · §5-7 · B ④ 27) · full 전용 속성 중 건수 큰 것만 slim 으로(§5-15 · B ⑥ 18) · 어느 노드에도 안 붙던 fact 를 붙이고 섹션 매핑 구멍을 메운다(§4-3 F-A~F-E · B ② 16 · ⑧ 15) · check_conditions 가 계열 · 제품 id 를 받아 펼친다(§5-6 · 오류 15) · 끝 조건 = B 재인용률(분모 = 카드 도구 호출이 있던 B 205 · 조항이 닿는 186 의 ≥ 90%) · 응답 크기 중앙값 ≤ 현 ×2 · 품질 6/6 · 106/106 유지(§6-5)

| 절 | 내용 |
|---|---|
| §1 | 범위 · 경계 |
| §2 | 입력 계약(파일 · 해시 · 칸 경로 — 실물 대조) |
| §3 | 골드 빌드(G1~G18 · G1~G17 정정 반영 · 펼치기 · 거르기 · 안전 동봉 · resolved · gap · 결정론) |
| §4 | 저장(스키마 · 적재 방식) |
| §5 | 도구 9(입력 · 출력 · 후보 여럿 · 응답 크기 · 의도별 경로 ①②③) · §5-12 평가용 원장 도구 3(골드 아님) |
| §5-0-1 | **v3.2** 응답 다이어트 — 규칙 A1-1~A1-9 · 도구별 기본 응답 상한 표(숫자) |
| §5-0-2 | **v3.2** MCP 전달 계약 — 도구 meta `anthropic/maxResultSizeChars` · intent 문구(M-1~M-3) |
| §5-13 · §5-14 · §5-15 | **v3** 의도별 고정 동봉 · 의도 → 섹션 기본 묶음 · full 전용 속성의 slim 승격 — **v3.2** C1′~C14′(id 전부 · 원문 상한) · 묶음 밖 id 노출 |
| §5-16 | **v3.2** T10 peek · T11 expand — Jev 재귀 탐색의 허브 쪽 응답 꼴 · **v3.3** expand = fact 한 줄 목록 · peek bytes = 실제 expand 바이트 |
| §6 | 품질 · E2E · **§6-5 v3.2 끝 조건(재실행 676 recheck · 크기 · C3 8 · 품질 · 결정론)** · **§6-6 걸음 도달 측정** · **§6-7 v3.3 끝 조건(expand 크기 · peek bytes 차 0 · 걸음 재생)** |
| §7 | 열린 것 · 결정된 것(O-1~O-4 · **아직 안 정한 것 V-1~V-18** · v3.3 에서 V-3 · V-13 닫음 · 패치에서 V-15 · V-17 · V-18 닫음(코디 11-01)) |
| §8 | **v3.2** B 186 ↔ 조항 1:1 표(**v3.3** 조항 닿는 행 155 · W7-D12) |

---

## 1. 범위 · 경계

### 1-1. 허브가 하는 것

| # | 하는 것 | 근거 |
|---|---|---|
| B-1 | 실버 8 + 시맨틱 정본을 골드 그래프로 빌드(규칙 적용 · 펼침 · 표시 · 근거) | 10-30 「골드 = 규칙 적용 그래프 + 허브 도구 탐색(카드 묶음 아님)」 |
| B-2 | 골드를 DB 에 빌드 번호로 저장 · 발행 · 서버가 발행본을 메모리에 올려 조회 | gold-research S4 · D-01 |
| B-3 | 결정론 조회 도구 9 를 REST 와 MCP 로 같은 코어에서 냄 | 10-26 경계 「Hub = 데이터 그래프 + 범용 조회 tool(MCP/REST)만」 |
| B-4 | 말 → 노드 후보는 사전 · 규칙(resolve_rules)으로만 — 후보 여럿이면 전부 | 10-26 「노드 검색도 결정론 · 후보만」 · 10-27 W-1 |
| B-5 | Jev 슬롯 선택지 = 노드 목록 · 스키마(vocab) | 10-26 「Jev 선택지는 Hub 가 노드 목록 · 스키마로 제공」 |
| B-6 | **평가용 원장 도구(골드 아님)** — 원장(브론즈 21 파일)을 그대로 읽는 MCP 도구 3. 골드 · 시맨틱 사전 · 규칙에 기대지 않음 · 허브 본 역할(골드 도구 9)과 섞지 않음(§5-12) | 10-30 「원장도 MCP 로 — hub-evals 는 원장 · 골드를 같은 환경으로」 |

### 1-2. 허브 밖(이 스펙에서 만들지 않음)

| 밖 | 누가 | 근거 |
|---|---|---|
| 질의 해석 · 슬롯 추출 · 추천 판단 · 문장 생성 | 외부 LLM(Jev · Claude) | 10-26 · 10-30 「허브에는 LLM 없음」 |
| 병원 상품 · 가격 · KOS 어댑터 · 미라쥬 영역 대응(연결 층) | 앱 | 10-30 「허브 고정 · 병원 무관 · 병원 상품은 표준 꼴 + 소스별 어댑터 → 연결 층」 · 10-30 「KOS 연결 = 기록만」 |
| 허브 호출 주체(U-2) · 시장가 표시(U-3) | 앱 · 화면 설계 | 10-30 「U-2 · U-3 는 데이터 단계 아님」 |
| 허브 평가 실험(원장 vs 골드 vs 골드 + Jev) | 골드 완성 뒤 별도 | 10-30 「hub-evals 는 골드 완성 뒤」 |
| 실버 · 시맨틱 · 브론즈 수정 | — | 이 스펙은 읽기만. 실버에 빈 곳이 보이면 「허브 보강 후보」(§3-6)로 적고 고치지 않는다 |

- 허브는 단위 시술 id · 제품 id 를 **안정 키**로 낸다(G1). 연결 층은 이 키에 붙는다
- 허브에 없는 것(샘플 대조로 드러난 빈칸)은 허브가 채우지 않고 「허브 보강 후보」 목록으로만 남긴다(10-30)

### 1-3. 코드 자리

| 항목 | 값 |
|---|---|
| 레포 | `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` — 로컬 전용 · push 금지 |
| 브랜치 | `kknaksss/phub-recommend`(지금 브랜치 · v1 그래프 파일은 아직 커밋 안 된 상태 — WORK-003 Phase 0 에서 기준점 커밋) |
| 재사용(뼈대만) | `backend/app/graph_main.py`(ASGI 진입점 · `FastAPIBuilder` · lifespan 안 `mcp.session_manager.run()` · `app.mount(MCP)`) · `backend/app/modules/graph/config.py`(env 파일 규칙) · `container.py`(DI 모양) · `backend/graph-local.compose.yml`(postgres 16 · 호스트 55434) · `backend/envs/graph.env.example` · `app/core/tx.db_provider` · alembic 체인 |
| 새로 | 골드 모듈(빌드 · 저장 · 메모리 그래프 · 도구 코어 · REST 라우터 · MCP 서버) · alembic 새 리비전(골드 테이블) · 빌드 · 발행 스크립트 · 시험 · 평가용 원장 모듈 `app/modules/raw/`(§5-12 · 골드와 별도) |
| v1 그래프 모듈 | `app/modules/graph/{application,curation,lowering,domain,sources,validation,resolve,repository}.py` · `app/router/graph.py` 는 골드 앱이 import 하지 않는다(지우지는 않음) |
| 포트 | 앱 `127.0.0.1:18005` · REST 접두 `/procedure-hub/gold` · MCP `/procedure-hub/gold-mcp/mcp`(Streamable HTTP · stateless · JSON) · 평가용 원장 MCP `/procedure-hub/raw-mcp/mcp`(같은 앱 · 별도 마운트 · 같은 전송 — §5-12) · DB `localhost:55434` |
| 사용자 포트 | 3700 · 3800 · 8700 · 8800 · 54329 와 기존 `procedure-*` 컨테이너는 쓰지 않는다(graph-local.compose.yml 머리 주석 그대로) |

---

## 2. 입력 계약 — 실버 · 시맨틱 파일 · 칸 경로(실물 대조 2026-10-30)

입력 폴더 = `orchestration/work/phub-recommend/`(이하 `$W`). 아래 칸 경로는 이 날 실물 파일에서 뽑은 것이다(10-27 SPEC-004 검수 FAIL 「입력 계약이 실물과 다름」 되풀이 방지).

### 2-1. 파일 · 해시 가드

| 파일 | version 칸 | sha256 앞 16자(10-30) | 읽는 이유 |
|---|---|---|---|
| `semantic.json` | `version` = `semantic-v1` | (빌드가 기록) | 노드 · 엣지 종류 · 사전 · resolve_rules · id 대응 · 표시 · 상속 · reading_contract |
| `step1-products.json` | `2` | `41128c7d5bce171b` | 제품 |
| `step2-families.json` | `step2-families v1` | `42eef4dc7dc70b26` | 계열 · 제품 → 계열 |
| `step3-sites.json` | `3.0` | `f92f4a8411c15cd1` | 부위 트리 |
| `step4-techniques.json` | `v1` | `cc6c0291a0b3506a` | 기법 트리 · 계열 기법 · 단위 시술 속성 |
| `step5-units.json` | `step5-units v1` | `38bcc0853547edb7` | 단위 시술 · 제품 연결 · 부작용 덮어쓰기 · PIH · 운영 · 용량 |
| `step6-packages.json` | `step6-packages v1` | `293b50e565ddf61e` | 패키지 |
| `step7-concerns.json` | `step7-concerns v1 (2026-10-29)` | `b2fa90915876de1d` | 고민 · 목적 · 추천 엣지 · 추천 조합 |
| `step8-relations.json` | `step8-v1` | `4f91a2abe7e3aae2` | 관계 · resolved · 확인 조건 · 안전 · 근거 |
| `step7-decisions.json` | `2` | `ae73f09bced8c13b` | 부위 규칙(site_rules) — 질의 때 층 거르기(G6) |
| `step8-decisions.json` | `1` | `2fbeb45c010185e6` | (semantic 입력 · 해시 가드만) |
| `step3-lexicon.json` | `1.1` | `c3b4effa7662af8c` | (semantic 입력 · 해시 가드만) |

- **해시 가드(빌드 실패 조건)**: `semantic.json` `inputs{파일: {version, sha256}}` 11개가 같은 폴더 실물 파일의 sha256 앞 16자와 하나라도 다르면 빌드 실패 — 시맨틱이 실버보다 낡았다는 뜻. 10-30 실물 대조 11/11 같음
- 해시 = `hashlib.sha256(파일 바이트).hexdigest()[:16]`(`semantic-build.py:661` 와 같은 식)
- `semantic.md` 는 읽지 않는다 — 정본은 `semantic.json`
- 브론즈(stg 원본)는 읽지 않는다. 부작용 덮어쓰기 값(G9)과 조합 구성(G17)은 이미 실버에 있다(§2-2 step5 · step7)

### 2-2. 칸 경로

정본 id 는 `semantic.json ids.map[]{canonical, kind, silver_id, name}`(1,071행)로 바꾼다(G1). 실버 안 문자열 꼴(`family:` · `units:` · `bundle:` · `unit:` · `ledger:` · `목적:` · `J{n}-{한글}` · `all`)은 `ids.string_forms[]` · `ids.silver_string_map{}`(41) 규칙대로.

| 파일 | 칸 경로 | 골드에서 | 실물 셈(10-30) |
|---|---|---|---|
| semantic | `node_kinds[]{kind, required, optional, path, count}` · `edge_kinds[]{kind, frm, to, attrs, path, count}` | 종류 목록 · 저장 엣지 셈 가드(S7) | 13 · 21 · 노드 합 1,071 · 저장 엣지 합 3,179 |
| semantic | `dictionary.expressions[]{expr, norm, variants, targets[{id, qualifier, reasons}], sources, collision, mode, ambiguous}` | resolve 사전 | 2,053 |
| semantic | `dictionary.resolve_rules{normalize[], fold{}, strip_chars, split, order[], tails[], prefix_min, prefix_rule}` | resolve 규칙(문서 = 코드) | order 4 · tails 「주사 · 시술」 · prefix_min 2 |
| semantic | `ids.map[]` · `ids.string_forms[]` · `ids.silver_string_map{}` | G1 | 1,071 · 8 · 41 |
| semantic | `reading.reading_contract` · `reading.interval_fields{}` · `reading.flags[]{flag, fields, read}` · `reading.gate_status{values, rule}` · `reading.default_response[]` | 읽는 규칙 · 표시 12 · gate 3값 | flags 12 · gate 3 |
| semantic | `inheritance[]{id, rule, fields}` | I1~I9 | 9 |
| semantic | `statements.table[]{statement, field, class}` | 근거 문장 class(B2) | 119 |
| step1 | `items[]` 중 `active == true` — `ledger_id` · `2_names.display_name` · `2_names.search_names[]` · `1_identity` · `4_license{status, recommendable, licenses[]}` · `5_spec` · `6_companies` · `evidence` · `open` | product 노드 | items 395 · active 354 · recommendable true 236 · false 118 |
| step1 | `lines{라인 이름: {…, items[]}}` | line_item 엣지 · 라인 속성 | 라인 11 · 엣지 5 |
| step2 | `families[]{id, name, name_status, definition, synonyms, sub_families, literature_*}` | family 노드 | 27 |
| step2 | `product_family[]{ledger_id, family, also_families, sub_family, also_sub_families, verdict, evidence_level, conflict, confirm_question, pending_director}` | product_family 엣지 | 354행 → 엣지 370 |
| step3 | `nodes[]{id, name, parent, status, synonyms, anatomical_name, danger_zone}` | site 노드 · 부위 트리 · 최상위 영역 계산 | 53 |
| step4 | `nodes[]{id, name, parent, level, medical_name}` · `family_defaults[]{family, default, also, default_layer}` · `unit_procedure_attrs{safe_layers, target_muscles, landmarks}` | technique 노드 · family_technique 엣지 | 26 · 27 |
| step5 | `units[]{id, key{family, sub_family, ingredient, site, technique}, name, site_basis, synonyms[], candidate_of[], uses_product[], purposes[], route_status, market[], side_effect_override[], pih_not_applicable, ops{}, step4_attrs, dose_range_text, evidence_level, decided_by}` | unit_procedure 노드 · key_* 엣지 · 운영 · 용량 · 시장가 속성 | 162 · side_effect_override 있는 단위 96 |
| step5 | `product_links[]{product, family, sub_family, recommendable, stored_units, inherited_candidates[], technique_excluded, guard, link, side_effect_override[{level, values{common, serious, …}, sub_family, override_of, priority}]}` | I4 assert · 부작용 덮어쓰기(제품 × 계열) | 354 · inherited_candidates 합 1,379 · side_effect_override 있는 제품 316 |
| step5 | `rules.product_link{stored, inherit, guards[], extra_stored[], technique_compat}` | I4 재계산 규칙 | — |
| step5 | `extracted[]{id, keys, attach, product, family, sub_family, source_text{…}}` · `taxonomy_products[]{id, product, attach, keys, source_text}` | 카드 원문 — `source_text` 안 칸은 `aftercare` · `safety.*`(common · serious · note · contraindications · long_term — 부작용 덮어쓰기 원문)뿐(실물: extracted aftercare 521 · safety.common 521 · safety.serious 189 · note 4 · contraindications 4 · long_term 1 / taxonomy_products aftercare 59 · common 59 · serious 31 · note 1 · contraindications 1). `overview` · `mechanism` · `onset_duration` 칸은 0행 | 521 · 59 |
| step5 | `pih[]{attach, target, condition, units}` · `pih_not_applicable_units[]` · `pih_gap_units[]` · `dose_range[]` | PIH · gap 3상태 · 용량 | 26 · 77 · 63 · 11 |
| step6 | `packages[]{id, name, kind, recommendable, synonyms, price, same_day_raw, detail_raw}` · `contains[]` · `slots[]{candidates}` | package 노드 · contains 엣지 | 24(recommendable false 2) · 49 · 8 → 엣지 71 |
| step7 | `concerns.categories[] · subcategories[] · items[] · extra_items[]` · `purposes[]` | concern · purpose 노드 · child_of · concern_related · concern_site | 고민 57 · 목적 13 |
| step7 | `edges[]{source, from, purpose_nodes, to_units, to_family, target_kind, ccs[], cc_named?, layer, site_check, lowering, resolve_flag, concern_region_check, anchor_sites}` | treats 엣지(값 그대로 · 다시 판정 안 함 — G6) | 437 · layer 부위 119 · 상위 35 · null 283 · ccs 있는 엣지 180 |
| step7 | `combos[]{id, kind, source, anchor{concern, concerns, source_label}, name, tier, components[], members[]?, upgrade[]?, schedule[]?, sales_copy{default_response}, concern_regions}` | combo 노드 · anchors_combo · combo_component(구성 칸 이름 그대로) | 79 · 구성 581(components 462 · members 107 · upgrade 12) |
| step7-decisions | `site_rules{lowering, climb, concern_region}` | 질의 때 부위 층 거르기(R21 같은 규칙) | — |
| step8 | `edges[]{id, a, b, endpoints{a,b{kind, id, qualifier, candidates[]}}, self_pair, claims[], conditional_claims, kinds, review_status, review_label, resolved{first, days, open_high, same_day, by_sub_condition, options[], by_direction?, field_status, rules, alternatives[], from_claims, status, inherited_claims, inherited_from_edges}}` | procedure_relation(앱 값 = resolved) | 230 · resolved 230 · by_sub_condition true 32 · by_direction 56 |
| step8 | `resolved_pairs[]{id, a, b, most_specific_edges, applicable_edges, resolved}` | 단위 쌍 값 우선 | 105 |
| step8 | `claims[]{id, kind, text, interval, gate_status, evidence, review_status, …}` | 근거 · alternatives(앱에 바로 안 냄) | 395 |
| step8 | `avoid_edges[]{id, from_concerns, to, qualifier, scope, default_apply}` | concern_avoid | 5(default_apply false 3) |
| step8 | `conditions.nodes[]` · `conditions.claims[]{id, target, target_level, grade3, conditions, scope_conditional, grade3_resolved}` · `conditions.resolved[]{id, target, condition, grade3, status, from, inherited, alternatives}` · `conditions.wait_resolved[]` · `conditions.not_condition[]` | check_condition 노드 · requires_check(등급 = resolved) · 대기 기간 | 53 · 336 · 241(target family 195 · units 20 · all 16 · product 7 · ledger 3) · 1 · 37 |
| step8 | `safety.complications[]{id, family, severity, …, units_inherit}` · `safety.side_effects[]{id, family, …, attach}` · `safety.site_caution[]` · `safety.timelines[]{attach_level, attach, units, phases}` · `safety.pih[]` · `safety.family_text{계열: {칸 이름: 원문}}` · `safety.unit_safety_status[]{unit, fields{…: 값 있음 · 해당 없음(원천) · 정보 없음(gap)}}` · `safety.unit_gaps[]` · `safety.side_effect_gap_families[]` · `safety.complication_gap_families[]` · `safety.complication_mild_only_families` | 안전 묶음 · gap 3상태 | 35 · 72 · 22 · 10 · 26 · 17계열 · 162 · 17 · 10 · 12 |
| step8 | `evidence.statements[]{id, family, field, statement, patient{}, evidence[]}` · `evidence.literature[] · web[] · guides[]` | evidence_statement · evidence_source 노드 · has_statement · cites | 119 · 25 · 29 · 15 |

`safety.family_text` 칸 이름(실물 · 17계열의 합집합 13칸 · 17계열 모두에 있는 칸 9 — 「상담 · 준비 · 고지 · 조건 아닌 문장」 · 「critical_safety_facts」 · 「안전 원문」 은 일부 계열만 · v3.1 W-8): 필수 고지(consent mandatory_disclosures) · 즉시 내원이 필요한 징후(consent emergency_signs) · 환자 설명 가이드(patient-education) · 사후관리 3종(taxonomy modality extracted.aftercare · extracted.json aftercare · procedure-profiles aftercare) · 부작용 문장 common · uncommon · serious(근거 — 합병증 노드 아님) · 상담 · 준비 · 고지 · 조건 아닌 문장(16) · 응급(extracted.json safety.emergency · 2) · critical_safety_facts(anatomy · 1) · 안전 원문(규칙 행 · 쌍 없음 · 1). 카드 칸 대응은 §5-4.

---

## 3. 골드 빌드

### 3-0. gold-research 대비 정정(이 스펙이 정본)

| 곳 | gold-research | 이 스펙 | 근거 |
|---|---|---|---|
| G14 · D-08 | 충돌 = 고르지 않고 값 집합 · 양쪽 주장 id | **충돌 = 8단계 `resolved` 하나.** 값 집합 요약 안 만듦 · 원문 주장은 `alternatives` · 근거로만 | 10-30 D-13b 바꿈 · 10-30 골드 판단 「D-08 → 충돌은 resolved 하나만」 |
| G9 · D-07 | 부작용 덮어쓰기 값은 실버에 없음 → 적재가 브론즈 원문을 싣는다 | 값은 실버 `step5 units[].side_effect_override[]` · `product_links[].side_effect_override[]` 에서 읽는다. 브론즈 안 읽음 | 품질 3차 ③(quality-report §0-2) · 실물 96 · 316 |
| G17 · D-04 | combo_component 462 → 581 로 정본 보강 | 7단계 · 시맨틱이 이미 581(components · members · upgrade) — 그대로 읽는다 | 품질 3차 ④ · semantic edge_kinds combo_component 581 |
| G3 | semantic I1 문구 「추천 계열만」을 SPEC-005 에서 뺀다 | treats 「계열만」은 펼치지 않는다(골드 판단 ④ · W2 유지) | 10-30 골드 판단 ④ |
| 골드 판단 ⑤ | 다파장 4(노블린 · 클라리티2 · 아포지 엘리트 플러스 · 디스커버리 피코) KTP 보조 하위 | 실버 `step2 product_family[].also_sub_families` 에 이미 반영(실물 4행 KTP) — G5 가 그 칸을 읽어 단위 시술 연결에 씀. 골드에서 따로 하는 일 없음 | 10-30 골드 판단 ⑤ |
| 판단 ② 범위 | 「메뉴 이름 → 추천 조합(쁘띠시술 등)」 | 메뉴 이름 = 사이트 추천 패키지 메뉴 라벨(`anchor.source_label`) **8개 전부**(G18) — 쁘띠시술만이 아님. 판단 ③ 만으로는 7단계 R12 앵커(「피부결/톤/항노화」 = P4 + P5 + 피부결)로 P5 질의에 P4 패키지가, P4 질의에 하위 P4-1 앵커로 P3 패키지가 섞여 Q109 · Q110 이 틀림(실물 셈) | 코디 답 10-30(이 스펙 작성 중 ask · 「같은 규칙의 일관 적용」) · J5 「사이트 「고민 선택」에는 그대로 뜸(원천 라벨)」 |
| §3 셈 | I4 1,364 · 저장 엣지 3,044 | 고정 숫자를 쓰지 않는다 — **빌드 때 입력 파일에서 센 값과 대조**(지금 실물 I4 1,379 · 저장 엣지 3,179) | 실물 대조 · step2 고정 assert 의 「알려진 한계」(_RESUME 10-28) |

**v3 — 구현이 이미 달라진 점을 본문에 반영(SPEC = 실물 · 2026-10-31)**. 출처 `WORK-003.md` §SPEC 과 다른 점 · 코드 레포 `backend/build-out/work003-report.md` D-1~D-10(코디 ask 합의 10-30). 아래 표의 「본문」 절이 v3 에서 그 값으로 고쳐졌다. (`cli-provider-report.md` 는 이 날 두 워크스페이스에서 찾지 못했다 — 브리프가 든 항목은 D-8~D-10 과 같아 그 셋으로 반영)

| # | v2 문구 | 실물(v3 본문) | 본문 |
|---|---|---|---|
| D-1 | T2 `concerns` 1+ · cc 범위 「같은 원천 문제(P)」 | `cc_roots?: [P{n}]` 선택 입력(고민 노드 없는 대분류 — 쁘띠시술 P1 · 기타 P14) · cc 나 site 가 있으면 concerns 0 허용 · cc_roots 없으면 P = concerns 의 대분류 | §5-3 |
| D-2 | G5 `rules.product_link` 전부 재계산 | 계열(주 · 보조) · 하위 일치 · guards · extra_stored 재계산 · **technique_compat 판정은 실버 `product_links[].technique_excluded` 값** · 제품마다 = inherited_candidates 가드 354/354 | §3-1 G5 |
| D-3 | `$W/quality-eval.py` 에 `--gold` 모드 | `$W` 는 읽기만 — 코드 레포 어댑터 `scripts/gold_quality_eval.py` 가 채점 식을 exec 로 빌림 · 리포트 `backend/build-out/quality-report-gold.*` | §6-1 |
| D-4 | slim 안전 칸 = 상태 · fact id · 짧은 이름 · T3 만 `sections` | **도구 9 모두 `sections`**(이름 = §4-3 fact section + `all` · T3 `full=true` = all) · 짧은 안전 요약 = 금기 조건 id(이름은 응답 머리 `names`) · 그 밖 등급 셈 · 금기류 엣지 id · 피함 고민 · gap 칸 · 원문 셈(`counts`) · 응답 머리 `more`(section 별 안 실은 원문 셈) | §5-0 · §5-4 |
| D-5 | claude_contract allowed = facts id 전부 | 그대로 · 머리 `names` · `emergency_signs`(계열마다 consent 응급 징후 문장)는 facts 밖 이름표 | §5-0 |
| D-6 | 카드 slim 에 쓰는 제품 id · 이름 · 허가 | 짧은 카드 = 쓰는 제품 **셈** · `sections=products` 면 목록 · 추천 조합 앵커는 짧은 카드에서 뺌 → **v3 §5-13 이 의도별로 되살림**(I-01 · I-10 · I-11) | §5-4 · §5-13 |
| D-7 | — | 측정 · E2E · 속도 `--gold inprocess`(TestClient · 포트 안 엶) | §6 |
| D-8 | resolve order 4단계(문서 = 코드) | 낱말 끝 **조사 떼기**(랑 · 이랑 · 하고 · 와 · 과 · 는 · 은 · 이 · 가 · 을 · 를 · 도 · 에 · 에서 · 으로 · 로 — 긴 것 먼저 · 끝 하나만 · 원 낱말 사전 일치 먼저 · 뗀 뒤 완전 일치일 때만 · `particle` 표시) — 질의 쪽만 · 골드 재빌드 없음 | §5-2 |
| D-9 | T4 · T6 · T7 `procedure` = unit_procedure id | **계열 · 제품 id 도 받아 단위 시술로 펼침**(`expanded` · 상한 pair 30쌍 · compare 8 단위 · 짧은 응답은 같은 값 쌍 묶음 `pairs[[a,b]…]`) | §5-5 · §5-7 · §5-8 |
| D-10 | T2 카드 전부 | `limit`(기본 10 · 1~200) · 넘는 카드 `more_cards` · `cards_total` | §5-3 |

**v3.2 — WORK-005 구현이 v3.1 과 다르게 한 곳을 본문에 반영(SPEC = 실물 · 2026-11-01)**. 출처 `backend/build-out/work005-report.md` 「SPEC v3.1 과 다르게 한 곳」 D-1~D-14 · 코디 10-31 범위 한정 한 바퀴 ①~④. 이 스펙 안에서는 WORK-003 의 D-1~D-10 과 번호가 겹치므로 **W5-D1~W5-D14** 로 부른다. 아래 「본문」 절이 그 값으로 고쳐졌다(v3.2 다이어트 §5-0-1 이 다시 바꾼 곳은 「→ v3.2」 로 표시).

| # | v3.1 문구 | 실물(코드 c95b37a) | 본문 |
|---|---|---|---|
| W5-D1 | §5-13 C2 꼴 `{condition, name, grade3, resolved_id, claims}` 전부 | `by_grade{등급: [조건 코드]}`(금기는 안전 요약 `contra` 에 이미 · I-01 은 주의만) + `claims[]`(id 전부 · 원문은 상한) · `claims_text` · 이름은 응답 머리 `names` | §5-13 C2′ → v3.2 는 **전 등급 · 계열 상속 주장 id 전부**(I-01 포함) |
| W5-D2 | §5-13 「시술 노드마다」 동봉 · 섹션 | 쌍 · 비교 · 조합 · 확인 조건은 **입력 노드 단위**(계열 · 제품은 `by_unit`) · combos 는 구성 **계열** 단위 · 같은 값은 `same_as` | §5-0 · §5-13 → v3.2 A1-1 「요청 노드 단위」로 확정 · A1-7 응답 수준 색인 |
| W5-D3 | §5-14 기본 묶음 section 「id 만 + more」 | 기본 묶음 section 도 상한 밖 fact 는 `more_ids` 로 id 전부(코디 10-31 ①) · `total` | §5-14 → v3.2 A1-6 |
| W5-D4 | §5-13 C11 `{timeline, phases[]{name, fact ids}}` | `phases[]{name, facts_n}`(id 는 `sections=timeline`) | §5-13 C11′ |
| W5-D5 | §4-3 F-C 「owner = 엣지 id」(비교 조합 members) | owner = combo 노드 · id `combo:{id}#evidence#members[j].attrs_text.{key}` · `attached_to` = 멤버 단위 시술 + combo | §4-3 F-C |
| W5-D6 | §4-3 F-C clinical_pearls 잎 fact(엣지 owner) | 이미 있던 `{SC}#clinical_pearls[i]`(계열 owner)에 부착만 | §4-3 F-C |
| W5-D7 | §4-3 `family:None` → 제품 정본 id | taxonomy 제품 4개(M1-P-10 · auto-M3 · auto-M9 · auto-M16)는 1단계 제품 노드가 없음 → 계열 코드를 taxonomy id 에서 읽어 `family:M1 · M3 · M9 · M9` | §4-3 |
| W5-D8 | §4-3 F-B 가드 「56행 전부 노드 1+」 | 54 + 2 는 붙일 노드 없음(CC 백반증 · 건선) → 가드 「그 2 외 0」 · `attrs_cc_without_units` | §4-3 F-B |
| W5-D9 | §5-5 C9 쌍당 원문 4 | 기본 3 · I-07/08 은 2 · `evidence` 명시 때는 전부 · `#reason` 은 `reasons[]` 로 따로 | §5-5 · §5-13 C9′ → v3.2 원문 2 · **id 는 claims · reasons 전부** |
| W5-D10 | §5-15 schedule | `schedule[].items[].text · sessions` 만 fact(overview) — 상태 · 근거 칸은 원문 아님(836 잎 → 121) | §5-15 |
| W5-D11 | §5-7 compare rows overview · method | rows 값은 **셈** · 원문 · id 는 입력 노드 `node_sections`(by_unit) | §5-7 |
| W5-D12 | §5-5 | pair_check 에 `family_relations`(입력 계열 사이 엣지 id · 주장 id) · 입력이 전부 한 계열이면 `relations[]` | §5-5 → v3.2 `relations_all` 로 합침 |
| W5-D13 | §5-13 C1 「그 시술 부위에 닿는 SC」 | 단위 시술은 부위(상위 포함) 기준 **계열 무관** · 계열 · 제품은 그 계열 SC 전부 | §5-13 C1′ → **v3.2 가 되돌림: 같은 계열만**(Q003 c2 · c3 C3 — 보톡스 전용 턱 경고가 실리프팅 카드에 붙어 「엉뚱한 연결」로 채점됨 · `rerun-report.md` §3) |
| W5-D14 | §6-5 「재실행 오류 0」 | 42 — 전부 기록 입력이 틀린 호출(없는 id · `check_condition:` id 를 procedures 자리에 · 빈 concerns) · 옛 빌드에서도 같은 오류 · 15건은 0 | §6-5 → v3.2 「기록 입력 오류 호출은 분모 · 오류 셈 밖」 명시 |
| ③ | §5-13 크기 상한 「현 ×2 · recommend 14.4KB」 | 코디 10-31 ③ 2.5×(recommend 18,000 · pair 18,000 · compare 20,000 · 나머지 현 ×2.5) — 측정 compare 25,455 · combos 24,820 초과 | **v3.2 가 2.5× 를 폐기** → §5-0-1 새 표(숫자) |
| ④ | §6-5 닫지 않는 행 19 | 코디 10-31 ④ 로 21행 추가(1-hop 다른 계열 10 · 쌍 양끝 아님 6 · 기록 오류 2 · 기타 3) → 40 | §6-5 → v3.2 는 2차 분류 B 186 기준으로 다시 셈(닫지 않는 행 25 · §8) |

**WORK-005 미닫힘 34(닿는 165 − 닫힘 131) 처분** — `work005-report.md` 「닫지 못한 행 34」. 행 단위 파일 = `reference/2026-10-30-hub-evals/build-out/recheck/not-closed-why.json`(**실존 · 77행** = WORK-005 1차 바퀴 미닫힘 77 — 사유별 24 · 21 · 10 · 7 · 6 · 4 · 3 · 2 · 검수 W-3). 범위 한정 바퀴 뒤 34 는 77 의 부분집합(21행이 「닫지 않는 행」으로 옮겨 가고 22행이 닫힘 — 행 단위 재셈은 WORK-007 WP-0 기준선에서 `recheck2` 가 옛 export 로 한 번 더 낸다). 아래는 34 의 사유별 처분(`work005-report.md` 셈 기준) · 77 의 나머지 43 은 2차 분류에서 닫혔거나 B 186 의 행으로 §8 에 있다:

| 사유(WORK-005) | 행 | v3.2 처분 |
|---|---|---|
| 조합 속성(members attrs_text · effect 가 C7 상한 1 조합 밖 · 비교 멤버 원문은 compare 만) | 21 | **C7′**: 조합 id 전부(≤ 8) + 조합 잎 fact id 전부(`refs` · 응답 수준 색인 A1-7) — 원문은 compare(C10′) · combos 에서만. 2차 분류에서 같은 꼴 40행(§8 C7′)과 같은 조항 |
| step8 메모 6(응답 노드에 안 붙음 — F-A ② 가 CC 의 단위 시술 전부에 붙이지만 응답 카드가 그 단위가 아님) | 6 | **C14′**: 계열 · 제품 카드 · 계열 펼침 응답의 C14 = 그 계열(펼친 단위 시술 전부)에 붙은 메모 · CC 속성 id 전부(상한 10 · 원문 1) |
| 엣지 속성 4(SC key_warning C1 상한 밖 · concern_avoid · product_family basis) | 4 | **C1′** 잎 id 전부(상한은 엣지 수 3 · 잎 id 는 전부) · **C4′** 제품 행에 `basis` fact id · concern_avoid 는 안전 요약 `avoid` + fact id |
| 기본 묶음 밖 2 | 2 | **§5-14′** 묶음 밖 section id 노출 |
| CC 조합 1 | 1 | **C14′** |

**v3.3 — WORK-007 구현이 v3.2.1 과 다르게 한 곳을 본문에 반영(SPEC = 실물 · 2026-11-01)**. 출처 `backend/build-out/work007-report.md` §0(코디 11-01 결정 C + D · ask msg_b52c82bfb858 답 msg_391be6f77522) · §5 D-1~D-13. WORK-003 · WORK-005 번호와 겹치므로 **W7-D1~W7-D13** 으로 부른다. 「본문」 열의 절이 그 값으로 고쳐졌다. 결정 근거(SPEC 글자 그대로 = id 전부 측정): (i) 121/161 · recommend 56KB · 계열 카드 24KB · checks 62KB · compare 67KB · case3 경로 64.6KB(`recheck2-report.spec-default.*`).

| # | v3.2.1 문구 | 실물(코드 cc637a2 · 빌드 b031371c) | 본문 |
|---|---|---|---|
| W7-D1 | A1-6 · C′ 표 「id 전부」(`more_ids` · `refs` · `claims` · 잎 id · `by_unit` id · `sections_index` ids[:4]) | 기본 응답은 **셈(n)** · 명시 `sections` 만 id 전부 · 더 받기 = T11 expand · `sections=` · pair_check | §5-0-1 A1-6 · §5-13 C′ · §5-14′ |
| W7-D2 | §6-5 (i) 닫힘 = 응답 안 id · 인용 | **(a) 응답 원문 · id 안 ∪ (b) 응답에 나온 노드에서 expand/sections 추가 호출 1 로 닿음**(실제로 불러 확인 · 결정론 · 캐시) · (a) 단독 보고 | §6-5 (i) |
| W7-D3 | A1-3 원문 「질문 조건 ≤ 4 · 없으면 금기 ≤ 2」 | 질문 조건 ≤ 4 **+** 금기 앞 2(`compact_safety.contra` + `names` 는 금기 짧은 이름 전부) | §5-0-1 A1-3 · C2′ |
| W7-D4 | §5-16 peek 앞 8 · 상한 2,000/4,000 | 앞 **4** · 상한 중앙 2,500 · p95 8,000(실측 앞 8 = 2,415/9,601) | §5-16 · §5-0-1 표 |
| W7-D5 | §5-16 `sections_bytes` 「빌드 때」 | 메모리 적재 때(`warm_sections` · 0.1s · 발행본 속성 아님 · 해시 영향 없음) — section 매핑 함수가 tools 에 있고 build 는 tools 를 import 못 함(순환) · 「요청 때 계산 없음」(S4)은 지킴 | §5-16 |
| W7-D6 | A1-6 명시 section 원문 ≤ 12 | T5 `sections=checks` · T4 `sections=evidence` 명시는 주장 원문 **전부** — 품질 어댑터(§6-1 · 채점 식 그대로)가 claims 의 facts meta 를 읽음 · 12 로 자르면 I-09 5문항 회귀(Q077 · Q081 · Q082 · Q085 · Q086) · W5-D9 와 같은 예외 | §5-0-1 A1-6 |
| W7-D7 | C3′ 「금기류 먼저」 | **양끝이 입력 안인 엣지 → 금기류 → id** — 계열 수준 관계가 25~63 이라 상한 20 안에 입력 쌍 엣지가 들어오게(C9′ 8/8) | §5-13 C3′ |
| W7-D8 | C2′ `edges[]` | 저장 `requires_check:{K8}:{C}` 만 · 펼친 unit 엣지 id 는 셈(계열 M8 = 31 단위 × 14 조건 엣지 17KB) | §5-13 C2′ |
| W7-D9 | §5-0 「안전 요약은 다이어트 밖」 | 펼친 단위 안전 요약 ≤ 8(`GOLD_SAFETY_UNITS_MAX` · 요청 단위 먼저 · 나머지 `_units_total` · 0 = 전부) — pair M2×M8 56 단위 요약 18.7KB | §5-0 · §5-0-1 |
| W7-D10 | §8 Q003 반대 조건 「보톡스 턱 단위 카드엔 있음」 | 추천 응답엔 M1 카드가 없어(auto-88 · 턱선 treats 에 M1 단위 없음) U5-016 카드(T3 · I-03)에서 확인 | §6-5 (iii) · §8 |
| W7-D11 | §6-5 (iii) 원문 칸 | `names` · `emergency_signs` 도 원문 칸(「켈로이드 체질」 류가 이름으로) | §6-5 (iii) |
| W7-D12 | §8 조항 닿는 행 161 | 데이터상 불가 6(Q007 c2 · c3 · Q018 c3 · Q192 c3 · Q126 c2 · Q169 c3) → 닫지 않는 행(`N-데이터`) · **조항 닿는 행 155 · 닫지 않는 행 31** | §6-5 · §8 |
| W7-D13 | A1-7 · WORK-007 Scope `index{combos, checks, relations, families}` | `index{combos, checks, families}` — relations 는 카드 `relations_all{edges ≤ 20, n, forbid_n, claims_n, global ≤ 4}` 로(id 목록은 셈) | §5-0-1 A1-7 · C3′ |

WORK-007 결과(같은 출처 §1 · 이 판의 출발점): (i) 145/155 = 93.5%(a 58 · b 87 · 161 기준 90.1%) PASS · (ii) 카드 도구 8 이 v3.2 표 초과(→ v3.3 표 = 이 측정값 · §5-0-1) · (iii) 4/5 + Q003 · (iv) 6/6 · 106/106 · 회귀 0 · pytest 853 · (v) peek 2,271/7,248 PASS · expand(가장 큰 section 1) 중앙 7,680 · **p95 18,444 FAIL** · (vi) 155/155 · (vii) meta 14 시험 PASS. 18005 재시작 뒤 `--base-url` 재측정 = in-process 와 바이트 같음.

### 3-1. 규칙 G1~G17

| id | 규칙 | 골드에서 하는 것 | 가드(빌드 실패) |
|---|---|---|---|
| G1 | 정본 id | 모든 노드 · 엣지 끝을 `ids.map` 으로 정본 id(`{kind}:{키}`)로 바꿔 싣는다. 단위 시술 · 제품 id 는 안정 키 | 맵에 없는 실버 id 가 엣지 끝에 있으면 실패 |
| G2 | 계열 → 단위 시술 펼치기(I1) | 관계 · 확인 조건 · 합병증 · 근거 문장 · 부작용 · 위험지대 · 피함의 **계열 끝**을 `key.family` 가 그 계열인 단위 시술 전부로 펼쳐 단위 시술 수준 행으로 싣는다. 행마다 `inherited_from`(계열 정본 id) | 펼친 합병증 행 수 = `safety.complications[].units_inherit` 길이 합(실물 285) |
| G3 | treats 「계열만」은 펼치지 않음 | `step7 edges[] target_kind == 계열만` 은 계열 엣지 그대로 + 표시(site_check · resolve_flag 값 그대로) | — |
| G4 | 하위 계열 · 기법 조건 끝(I2 · I3) | `endpoints.*.qualifier.sub_family` · `.technique` 끝은 같은 하위 · 같은 기법(또는 하위 기법) 단위 시술로. 키에 그 하위 없는 계열은 「candidates」 표시 | — |
| G5 | 제품 → 단위 시술(I4) | `step5 rules.product_link`(같은 계열 주 · 보조 · 하위 일치 · guards · extra_stored)를 다시 계산 · **technique_compat 판정만 실버 `product_links[].technique_excluded` 값을 읽는다**(v3 · D-2 — 4단계 장비 속성 판정 로직 재구현 안 함) | 결과가 `product_links[].inherited_candidates` 와 제품마다 같아야 함 · 저장 `units[].uses_product` 합(실물 44)과 같아야 함 |
| G6 | 부위 — 저장값 그대로 · 질의 때 거르기 | treats 엣지의 부위 판정(R21 · R22 · R23 · R25 · R28 · R32)은 7단계 값 그대로(다시 판정 안 함). 질의에 부위가 오면 `step7-decisions site_rules.climb` 와 같은 층 규칙으로 거른다 · `site_rules.site_free`(「해당 없음」 · 「병변 단위」) 단위 시술은 층 거르기 통과(품질 2차 · quality-report §0-1) · `layer` 「상위」(얼굴 전체 층)도 같이 낸다(골드 U-1 = ②) | — |
| G7 | 끝점 묶음(I6) | `candidates[]` 는 OR — 펼친 행마다 `candidates` 표시. 고르지 않는다 | — |
| G8 | 조건부 제외(I7) | `default_apply false` · `scope_conditional true` 는 펼치되 `conditional` 표시 → 기본 응답 · 기본 탐색 · 값 접기에서 뺀다(`include_conditional` 로만) | — |
| G9 | 부작용 덮어쓰기(I8) | 계열 부작용(`safety.side_effects[] attach family:*`)을 단위 시술로 펼친 뒤, 아래 수준 `side_effect_override[]` 값이 있으면 그 값으로 바꾼다. 우선순위 = `priority` 칸 — **작을수록 먼저**: 0 제품 × 계열 × 키 하위(실물 111) < 1 제품 × 계열(207 · taxonomy products 58) < 2 단위 시술(159) < 3 단위 시술 후보(89) < 계열 값. 덮인 계열 값은 `override_of` 로 근거만 남김. 계열 부작용이 gap 인 계열(`safety.side_effect_gap_families` — N1~N10)을 덮은 행(실물 72 — N1 63 · N4 4 · N5 2 · N2 1 · N6 1 · N7 1)은 아래 수준 값이 유일한 값 — `override_of` 를 남기고 계열 쪽 상태는 「정보 없음(gap)」. **합병증 노드는 덮지 않는다** | `override_of` 가 계열 노드(27)에 없으면 실패 |
| G10 | 해당 없음 ≠ gap(I9) | 안전 칸마다 상태 3값 — `값 있음` · `해당 없음(원천)` · `정보 없음(gap)` — `safety.unit_safety_status[].fields` 그대로. 합병증 원천이 전부 mild 인 계열은 「중대 반응 없음(원천)」 | unit_safety_status 가 단위 시술 162 전부를 덮지 않으면 실패 |
| G11 | 붙는 수준 원문 | 경과 타임라인(`safety.timelines[] attach_level · attach · units`) · PIH(`step5 pih[]` · `step8 safety.pih[]`) · 운영(`units[].ops`) · 계열 원문(`safety.family_text`)은 원천이 가리킨 수준에 붙여 아래로 상속(엣지 아님 · 속성). 하위 계열에 붙은 것은 그 하위 단위 시술만 | — |
| G12 | 기본 응답 거르기 | 뺀다: 제품 `4_license.recommendable false` · 패키지 `recommendable false` · 병원 시그니처 · 영업 문구(`sales_copy.default_response false`) · conditional · 시술 아님 · 못 풂. gate 3값(자동(완전 일치) · 자동(규칙) · 결정)은 전부 통과 — 「미확인」은 상태가 아니라 표시(question · weak · gap)로 값과 같이 낸다(10-27 W-1 · D-05) | — |
| G13 | 안전 정보 늘 동봉 | 시술이 응답에 나오면 거르기와 무관하게: 합병증 · 부작용 · 확인 조건(전 등급) · 위험지대 · 금기류 관계(간격 금기 · 조합 금기 · 같은 날 불가 · 대체(택 1)) · 피함(조건부 아닌 것) · 응급 징후 · 필수 고지 · gap 상태(D-06 · 10-26) | — |
| G14 | 충돌 = resolved 하나(정정) | 시술 쌍 값 = §3-3. 확인 조건 등급 = `conditions.resolved` · 대기 기간 = `conditions.wait_resolved`. 원문 `claims[].interval` 은 근거 · `alternatives` 로만 | 단위 쌍마다 앱 값이 둘 이상이면 실패(§3-3 가드) · 단위 시술 × 조건 등급이 둘 이상이면 실패 |
| G15 | by_sub_condition | 겉 칸이 null 이고 `by_sub_condition true` 면 `options[]` 를 그대로 전달 — 한 값으로 접지 않는다. 조건을 모르면 `sub_condition` 「조건: 모름(전부 접음 — 가장 보수적)」 옵션 | 옵션이 있는 칸의 겉 칸이 채워져 있으면 실패 · 조건 모름 옵션이 칸마다 정확히 1개가 아니면 실패 |
| G15b | by_direction | 같은 날 값이 먼저 하는 쪽에 따라 갈리면 `resolved.by_direction.a\|b.same_day`(a = 엣지 a 끝 먼저 · 겉 same_day null)를 그대로 전달 · 쌍 방향에 맞춰 a/b 를 뒤집어 싣는다 | 겉 same_day 가 채워졌는데 `None` 을 뺀 방향별 same_day 값이 둘 이상이면 실패(`step8-apply.py:2008` 과 같은 식 · 실물 0 — 한쪽 None 인 11건은 통과) |
| G16 | 와일드카드 · 전역은 안 펼침 | 「모든 시술」 끝 관계(`endpoints.*.kind == 모든 시술`)와 `conditions.resolved[] target == all`(16)은 전역 행 하나로 두고 모든 시술 응답에 붙인다 | — |
| G17 | 추천 조합 구성 | `combo_component` = `combos[].components\|members\|upgrade[].units[]`(구성 칸 이름 `field` 그대로 · order · status · flag) | 셈 = semantic combo_component count(실물 581) |
| G18 | 메뉴 라벨(판단 ② · 코디 10-30) | 사이트 추천 화면 라벨 = `step7 combos[] kind == 「고민 패키지(사이트 「추천 패키지」)」` 의 `anchor.source_label`(실물 8 — 주름 4 · 처짐/탄력 4 · 쁘띠시술 3 · 피부결/톤/항노화 3 · 색소/미백 3 · 모공 3 · 흉터 2 · 얼굴윤곽 2). 라벨마다 resolve 사전에 `menu:{라벨}` 대상(kind `menu` — 노드 종류 13 에 안 넣음 · 사전 대상 · T7 입력 값일 뿐)을 더한다 — 같은 norm 행이 있으면 그 match 안에 **별도 후보**로 더하고 기존 고민 대상의 mode(전부 · 하나 · 후보)는 바꾸지 않는다(코디 판단 ① · 10-30 「고민 id 질의는 그대로」) · 없으면 새 행. 실버 · 시맨틱은 안 고침 | 라벨 수 = 실물 셈(8) · 라벨마다 추천 패키지 1+ |

### 3-2. 펼치기 · 거르기 · 안전 동봉 순서(빌드 한 번)

1. 입력 해시 가드(§2-1) → 실패면 멈춤
2. 노드 1,071 을 정본 id 로 싣기(G1) · 표시 12(`reading.flags[].fields` 의 실버 칸에서) · gate 3값(`reading.gate_status.rule` — gate 칸 있으면 그대로 · 없으면 decided_by 가 사용자 결정 id 면 「결정」 · 나머지 「자동(규칙)」)
3. 저장 엣지 21종을 싣기(semantic edge_kinds path 대로) → 저장 엣지 셈 = semantic 셈(S7 · 종류마다)
4. 펼친 엣지 계산: G2 · G4 · G5 · G7 · G9 · G11 · G16 · G17 → 단위 시술 수준 행(행마다 `derived_by`(G 규칙 id) · `inherited_from` · 표시)
5. 시술 쌍 값 · 확인 조건 등급 계산(§3-3)
6. 기본 응답 표시(G8 · G12) — 지우지 않고 `default_out: true` 칸으로(조회 옵션으로 다시 낼 수 있게)
7. 안전 묶음(G13)을 단위 시술 · 제품마다 미리 모아 둔다(카드 응답이 dict 조회 하나로 끝나게 — S4)
8. 카드 원문 facts 만들기(§4-3 · fact id 결정론)
9. 사전 적재 — `dictionary.expressions` + 메뉴 라벨(G18)
10. 빌드 가드 전부(§3-1 가드 열 · §3-3 · §3-5) → 하나라도 실패면 발행 안 함
11. 빌드 해시(§3-5) · 셈 기록 · 발행

### 3-3. 시술 쌍 값(reading_contract 그대로)

| 경우 | 앱 값 |
|---|---|
| 단위 쌍이 `step8 resolved_pairs[]` 에 있음(105) | 그 `resolved` |
| 없음 | 그 쌍에 닿는 엣지 중 **가장 구체적인 엣지**들의 `resolved`(엣지 a 끝이 쌍의 어느 쪽인지에 맞춰 first · by_direction 을 뒤집음). 가장 구체적 = 다른 닿는 엣지의 끝 단위 집합을 자기 끝 집합이 덮지 않는 엣지(`step8-apply.py:1976` 의 `covers` · `:2022-2050` 의 `most_specific` · `two_value` 정의). 위 엣지 주장은 8단계가 상속해 이미 접었다(`resolved.inherited_claims`) |
| 쌍에 닿는 엣지 없음 | 관계 없음(「정보 없음」 · 빈 값) |
| 전역(「모든 시술」) | 모든 쌍 응답에 전역 행을 따로 붙임(G16) |
| 같은 단위 시술끼리(자기 쌍 · 재시술 간격) | 8단계 쌍 셈은 u == v 를 건너뛴다(`step8-apply.py:2028`) — 자기 쌍은 `edges[].self_pair == true` 엣지(실물 4 — E8-0059 M2↔M2 · E8-0214 · E8-0225 · E8-0228)의 `resolved` 만 읽는다. 끝 단위 집합에 그 단위 시술이 든 자기 쌍 엣지 중 가장 구체적인 것 · 없으면 관계 없음 |

- **가드**: 단위 쌍마다 위 규칙의 값이 하나(가장 구체적 엣지들 값이 갈리면 resolved_pairs 에 있어야 함) — 8단계 전수 가드(`two_value`)와 같은 검사를 골드에서 다시 한다. 실물(`UnitSets` 셈): 전역 엣지(G16 · E8-0001 「모든 시술」) 제외 229엣지 → 단위 쌍 4,674 · 엣지 둘 이상 닿는 쌍 2,048 · 그중 resolved_pairs 100 · 나머지는 가장 구체적 엣지 값이 하나 / 전역 엣지 포함 230엣지 → 4,791 · 2,075 · 105 — resolved_pairs 105 중 5 는 전역 엣지 때문에만 생긴 쌍(전역 행으로 따로 붙이므로 G16 과 같이 읽음)
- 확인 조건 등급: 단위 시술 × 조건마다 `conditions.resolved[]` 중 대상 키(units · family · all)가 그 단위 시술을 덮는 가장 구체적인 것(`step8-apply.py:2101` `key_covers`) — 둘 이상이면 가드 실패. 실물 대상 키 = family 195 · units 20 · all 16 · product 7 · ledger 3. **product 7 · ledger 3 은 단위 시술을 하나도 덮지 않는다**(`key_covers` · UnitSets 빈 집합) — product 키 행(product:M1-1-7 4 · product:M9-2-3 3)은 그 제품에만 붙음(T3 제품 카드 · T5 `id=product`) · 단위 시술로 내리지 않음. ledger 키 행(KR8-0212~0214 · `ledger:auto-6-…` 3 — 원장 「넥큐레이션」 · 5단계 행선지 6단계 패키지)은 **`package:P6-03` 에 붙인다**(10-30 O-4 결정 · 대응 = `step6 packages[].ledger_id`) — T5 `id=package` · T7 `packages[]` 의 안전 묶음에 실림 · 단위 시술로 내리지 않음. 가드: ledger 키마다 `ledger_id` 가 같은 패키지가 정확히 1개(아니면 실패)
- 이전 시술 경과 판정(I-08 · D-10): 경과일 ≥ `days[0]`(하한)이면 충족 · 상한 · `open_high` 는 원문 표시만 · `same_day` 는 경과 0 일 때만 · by_sub_condition 이면 옵션별 판정을 다 냄
- 앱 값에 원문 `claims[].interval` 을 섞지 않는다. 쌍 응답의 `claims` 칸은 `{id, kind, text}`(근거) · `alternatives` 는 resolved 칸 그대로

### 3-4. gap 3상태

| 상태 | 뜻 | 실버 칸 | 응답 |
|---|---|---|---|
| `값 있음` | 원천 값 있음 | `unit_safety_status[].fields.*` | 값 + facts |
| `해당 없음(원천)` | 원천이 「해당 없음」이라 함(PIH 해당 없음 계열 등) | `pih_not_applicable_units` · fields | 「해당 없음」 그대로 |
| `정보 없음(gap)` | 원천에 없음 — 「없음 = 안전」 아님 | `pih_gap_units` · `side_effect_gap_families` · `complication_gap_families` · `unit_gaps` | 「정보 없음」 + `gap` 표시(must_show) |
| (보조) `중대 반응 없음(원천)` | 합병증 원천은 있으나 전부 mild | `complication_mild_only_families` | 합병증 칸 상태로 |

### 3-5. 결정론 · 빌드 해시 · 가드

- 같은 입력(해시 11 같음) → 같은 골드. 시각 · 난수 · 순서 미정 dict 순회 · 환경 값이 골드 내용에 들어가지 않는다
- **빌드 해시** = 골드 내용(노드 · 엣지 · facts · 사전 · 전역 행)을 정본 id 순으로 정렬한 canonical JSON(`sort_keys`, `ensure_ascii=False`, 구분자 고정) 의 sha256 앞 16자. 입력 해시 11 과 같이 `gold_build` 에 기록
- 같은 입력으로 두 번 빌드 → 빌드 해시 같음(가드 · 시험)
- 빌드 가드 묶음(S7 확장): 입력 해시 · 저장 엣지 셈(종류마다 = semantic) · 노드 셈(종류마다 = semantic) · G1 · G2 합병증 285(= units_inherit 합) · G5 I4(= product_links 제품마다) · G10 · G14 · G15 · G15b · G17(= 581) · 고정 숫자 대신 입력 파일에서 센 값과 대조
- 펼친 뒤 셈은 빌드가 계산해 `gold_build.counts` 에 기록(gold-research §2-1 의 24,392 는 그때 입력 기준 참고값 — 가드 아님)

### 3-6. 허브 보강 후보

빌드 · 도구가 찾은 「허브에 없는 것」은 고치지 않고 목록으로만(10-30). 출처 2갈래:

- 빌드: resolve 사전에 없어 sample 대조에서 비는 말 등 — gold-research D-18 이 든 3건(쥬비덤 볼루마 품목 · 「Sofwave」 단독 표기 · 소프웨이브 「2주 사우나」(원천 없음))을 첫 행으로
- 빌드: 단위 시술 · 제품마다 따로 쓴 개요 · 기전 · 발현 · 지속 문장 없음(실버 `source_text` 에 그 칸 0행 · 계열 수준 환자 설명 가이드만 — F-1)
- 도구: `resolve` 의 `unmatched` 를 E2E 동안 모은 것

산출 = `gold-hub-gaps.json`(코드 레포 빌드 출력 폴더) · 각 행 `{text, where, kind, first_seen_build}`. 실버 반영은 사용자 결정 몫(이 스펙 밖).

---

## 4. 저장

### 4-1. 적재 방식

1. **적재**(Phase 1): `$W` 의 입력 파일 12(§2-1)를 원문 그대로 `gold_source_snapshot` 에 넣는다(파일 이름 · version · sha16 · 바이트 크기 · JSON 본문). 같은 sha 면 다시 안 넣음
2. **빌드**(Phase 2): 스냅샷 한 벌(파일 12 의 sha 묶음)을 읽어 골드 계산 → `gold_build` 한 행 + 그 빌드의 노드 · 엣지 · facts · 사전을 **한 트랜잭션**으로. 가드 실패면 `status = rejected` 로 기록만(행 안 씀)
3. **발행**: `gold_publication` 의 현재 포인터를 새 빌드로 바꾼다(지난 빌드는 지우지 않음)
4. **서버**: 시작 때 발행된 빌드를 메모리 그래프로 올린다(dict · 인접 목록 · 사전 norm 색인). 요청은 메모리만 읽는다(S4). 발행 바뀌면 재시작으로 반영(이 스펙 범위)

명령(코드 레포 `backend/` 에서 · 이름은 WORK-003 이 정함): 적재 `--from-dir $W` · 빌드 · 발행 · 서버 기동. env 는 `envs/.env.gold`(git 제외 · 예시 파일만 커밋 · 비밀값 없음).

### 4-2. 스키마(새 alembic 리비전 · 기존 테이블과 FK 없음)

| 테이블 | 키 | 칸 |
|---|---|---|
| `gold_source_snapshot` | `id` | `file` · `version` · `sha16` · `size` · `body jsonb` · `loaded_at` |
| `gold_build` | `id` | `started_at` · `finished_at` · `status`(published · rejected · unchanged) · `input_hashes jsonb`(파일 12 → sha16) · `build_hash` · `counts jsonb` · `guards jsonb`(가드마다 기대 · 실제 · 통과) |
| `gold_node` | (`build_id`, `id`) | `kind`(13) · `name` · `attrs jsonb`(실버 필수 · 선택 칸 · 운영 · 용량 · 시장가 · PIH · 계열 원문 상속 결과) · `flags jsonb`(표시 12 중 해당) · `gate_status` · `default_out bool` · `source_refs jsonb`(실버 파일 · 경로 · 실버 id) |
| `gold_edge` | (`build_id`, `id`) | `kind`(21 + 펼친 종류) · `from_id` · `to_id` · `stored bool`(저장 엣지 / 펼친 행) · `derived_by`(G id) · `inherited_from` · `attrs jsonb` · `resolved jsonb`(procedure_relation · requires_check 만) · `flags jsonb` · `gate_status` · `layer` · `default_out bool` · `evidence jsonb`(주장 id · 근거 출처 id) |
| `gold_global` | (`build_id`, `id`) | 전역 행(G16) — `kind` · `payload jsonb` |
| `gold_fact` | (`build_id`, `id`) | `owner_id` · `section`(§4-3) · `text`(원문 그대로) · `flags jsonb` · `state`(값 있음 · 해당 없음 · 정보 없음) · `source`(실버 경로 · evidence_source id) |
| `gold_dictionary` | (`build_id`, `norm`) | `expr` · `variants` · `targets jsonb` · `mode` · `ambiguous` · `collision` |
| `gold_publication` | `id`(한 행) | `build_id` · `published_at` |

- 인덱스: `gold_edge(build_id, from_id)` · `(build_id, to_id)` · `(build_id, kind)` · `gold_fact(build_id, owner_id)`. 인덱스 · 제약 이름을 명시(v1 `app/model/graph.py` 머리 주석의 naming 충돌 교훈)
- jsonb 는 postgres · 시험용 sqlite 는 JSON(v1 `_JSON_DOCUMENT` 꼴 재사용)

### 4-3. facts(근거 인용 단위 · S5)

- fact = 응답에 나가는 원문 한 덩이. 원문은 고치지 않는다(번역 · 요약 · 합치기 없음)
- **fact id(결정론)**: 원천에 id 가 있으면 그 id(`ST-…` · `SE-…` · `CX-…` · `K8-…` · `KR8-…` · `WR8-…` · `R8-…` · `SC-…` · 타임라인 `id`) · 없으면 `{owner 정본 id}#{section}#{실버 칸 경로}[{순번}]`(예: `unit_procedure:U5-001#ops#durationMin`)
- 부작용 덮어쓰기 fact 는 `override_of` · `priority` · 덮은 수준(`level`)을 같이 싣는다
- section 값: `overview` · `method` · `recovery` · `aftercare` · `timeline` · `emergency` · `disclosure` · `safety.side_effects` · `safety.complications` · `safety.pih` · `checks` · `site_caution` · `dose` · `products` · `evidence` · `ops` · `market`

**v3 — 붙지 않은 fact · 속성 → fact(F-A ~ F-E)**. 근거 = `fail-triage.md` §3 ⑧ 15 · ② 16 · ⑦ 20 · ⑥ 18(건수) · 부록 fact id. 원칙: 원문은 그대로(복사 · 요약 없음) · fact 는 하나 · **부착은 색인으로**(`gold_fact.attached_to jsonb` = 정본 id 목록 · 메모리 `facts_by_attach[(node, section)]`). owner 는 바꾸지 않는다(원천 수준 기록) · 도구는 owner 와 attached_to 둘 다로 찾는다.

| id | 무엇(실물 셈 · 2026-10-31 gold-export e9d30ace) | 붙이는 규칙(결정론 · 빌드 때) | 가드 |
|---|---|---|---|
| F-A | `step7 step8_notes[]` 245행(지금 owner `scope:all` · section evidence — 도구가 못 꺼냄 · B ⑧ 14건: Q086 · Q115 · Q147 · Q148 · Q159 · Q198 · Q227 → `step8_notes[124 · 138~140 · 190 · 191 · 193 · 229]`) | 행의 `where` 로 앵커를 정한다 — ① `P{n}-{m}`(13) → `combo:RC-PC-P{n}-{m}` ② `P{n} {CC}`(152) → 7단계 treats 엣지 중 `root == P{n}` 이고 `ccs ∋ CC` 인 엣지의 `to_units` 단위 시술 전부(+ 그 CC 가 `anchor` 에 든 추천 조합) ③ `where == combos[].name`(중증도 조합 · 세션 조합 44) → 그 combo ④ 후속 간격 `R{n}`(28) → `combo:RC-RE-R{n}` ⑤ 규칙 8(`combination_rules` 제목) → **연결 키 = `step8_notes[i].text == avoid_edges[j].text` 이고 두 행의 `source` 가 같음**(실물 1건 — `step8_notes[45]` ↔ `AV8-001` · W-2) 인 `concern_avoid` 의 고민 · 대상 단위 시술 · 나머지 7은 `scope:all` 유지(닫히는 B 행 없음 · 추측으로 더 잇지 않음). 단위 시술에 붙는 행은 section `evidence` · meta `{where, kind, cc}` | 245행 전부 앵커 종류가 정해짐(①~⑤ 합 = 13 + 152 + 44 + 28 + 8 = 245 · ⑤ 중 concern_avoid 연결 1 · scope:all 유지 7 · 미해결 0) · ②의 CC 는 7단계 `edges[].ccs` 집합에 있어야 함(실물 152/152) |
| F-B | 8단계 `attrs[]` 56행 중 owner 가 노드가 아닌 것 — `CC P{n}:{CC} 속성(원소 1개 — 쌍 아님)` 21(B ⑧ 1건 Q198 `attrs[25]`) · `7단계 추천 조합(목적 레시피) 후속 일정 원문` 28 · `단위 시술 U5-124,U5-125,U5-126 재시술(터치업) 간격 원문` 4 · `7단계 추천 조합 RC-OP-Hair-* 속성` 2 | `source_index` 로 — `P{n}:{CC}#k` → F-A ② 와 같은 규칙(treats 엣지 to_units) · `R{n}#k` → `combo:RC-RE-R{n}` · `U5-…` 열거 → 그 단위 시술들 · `RC-OP-…` → 그 combo. section `evidence` | 56행 전부 owner 또는 attached_to 가 노드 1+ |
| F-C | 엣지 속성에만 있는 원문(B ⑦ 20건): `site_caution` 엣지 `attrs.row.spec{key_warning, risk, safe_zone, dose_range, target_muscle}` · `vessels[].danger` · `clinical_pearls[]` · `safe_injection_depth`(4건 — Q002 · Q018 · Q036 · Q043) / 비교 조합 `members[].attrs_text{best_for, downtime, duration, limitations, onset, pain, pih_risk, cost_range, mechanism_simple, asian_skin_note(2)}` · `anchor.subtitle`(combo_component 11건 · 열거는 보기 · 규칙은 잎 전부 — W-7) / `product_family` 엣지 `attrs.row.basis`(3건) / treats 엣지 `attrs.row.evidence.role`(1건 Q118 — treats 에 `row.claims` 는 0건 · `R8-0321#reason` 은 이미 procedure_relation evidence fact · F-8) / `concern_avoid` ↔ `step8_notes[45]`(1건 · F-A ⑤) | 잎 값마다 fact 를 만든다 — id `{엣지 id}#{section}#{칸 경로}` · owner = 엣지 id · attached_to = 엣지 양끝 노드(site_caution → 계열 + 부위 + `units_affected` 단위 시술 · 비교 조합 members → 그 멤버 단위 시술(`members[].units`) + combo · product_family → 제품 · treats `evidence.role` → to_units). section: site_caution 칸 → `site_caution` · members attrs_text → `evidence`(downtime · duration · onset 은 `recovery` 로도 색인) · basis → `overview` · treats `evidence.role` → `evidence` | site_caution 22엣지 × spec 잎 전부 fact 있음 · 비교 조합 9 × members attrs_text 잎 전부 |
| F-D | 노드 속성(full 전용)으로만 있던 원문(B ⑥ 18 중 fact 가 없던 것): 단위 시술 `silver.pih[]{attach, condition, fitzpatrick_note, pih_rate, pih_risk, source, target}` 잎(실물 32행 · `prevention` 은 이 칸에 없음 — step8 `safety.pih[]` 의 `pih[k]` fact 본문에 이미 있음 · 9건 중 7 — 지금 `pih[k]` fact 는 묶음 1개) · `sources[].detail`(1) · 조합 `effect{expectedResult, clinicalRationale, riskBenefit}`(목적 레시피는 `effect{expectedResults, repeatCycle}` 7 — W-7) · `price` · `evidence_notes[]` · `caveats[]` · `rationale` · `maintenance` · `sessions` · `subtitle` · `follow_up` · `avoid_text` · `annual_focus`(combo 8 + ⑤ combo 27 의 같은 칸) — **열거는 보기 · 규칙은 「잎 전부」** · 계열 `silver.definition`(1) | 잎 값마다 fact — id `{노드 정본 id}#{section}#{칸 경로}` · owner = 그 노드 · section: pih 잎 → `safety.pih` · sources detail → `overview` · 조합 effect · rationale · caveats · evidence_notes · subtitle → `evidence` · price → `market` · sessions · maintenance · follow_up · annual_focus → `timeline` · avoid_text → `checks` · definition → `overview` | 조합 79 × 위 칸 잎 전부 · 단위 시술 pih 잎 전부 |
| F-E | 섹션 매핑 구멍(B ② 16건 — 부록 fact id): 계열 카드가 **단위 시술 수준 fact 를 못 냄**(Q078 · Q219 `unit_procedure:U5-091#ops#ops.needsAnesthesia` · `…U5-090#ops#ops.prepNotes` · Q110 `pih[1]`(U5-023) · Q136 `fractional-co2#phases[4].normal[3]`(U5-028)) · 계열 카드 `site_caution` 이 SC 엣지 fact 를 안 냄(Q013 `SC-cheek-M1` · Q041 `SC-temple-M1`) · compare 가 `overview` · `method` 를 안 냄(Q015 · Q016 · Q042 · Q057 · Q069 · Q073 · Q209 `family:M*#overview#family_text[환자 설명 가이드…]` · `#method#…how_it_works`) · check_conditions 가 `emergency` 요청을 무시(Q036 `botox#phases[3].emergency[1]`) · recommend 가 `checks` 요청을 무시(Q001 `family:M9#checks#family_text[상담 · 준비 · 고지…][1]` · `K8-0303`) · recommend `overview`(Q103) | 매핑 규칙(§5-4 카드 칸 표 · §5-14): ① 계열 카드 `ops · dose · market · timeline · aftercare · safety.pih · site_caution · products` = 그 계열 단위 시술 facts 를 **단위 시술별로 묶어**(`by_unit{unit: [fact id]}` · 단위 시술 상한 §5-13 표) ② 계열 · 단위 카드 `site_caution` = `facts_by_owner((family, site_caution))` ∪ SC 엣지 fact(F-C · 단위는 부위 일치 · 계열은 전부) ∪ `family_text` critical_safety_facts ③ **`sections` 는 도구 9 공통으로 「응답에 나온 시술 노드(단위 · 제품 · 계열)마다 그 section 의 카드 facts」 를 뜻한다**(T4 · T5 · T6 · T2 · T7 · T8 도 같은 매핑 함수 · 지금은 T3 만 전 section) | §6-5 재실행에서 ② 16건 fact id 가 응답에 있음 |

- 빌드 가드에 더한다: F-A ~ F-D 셈(행 수 · 잎 수)을 `gold_build.counts.v3_facts` 에 기록 · F-A 미해결 0 · F-B owner 없음 0. 빌드 해시가 바뀐다(새 fact) → 발행 · 서버 재시작(WORK-005)
- `family:None` owner fact 40행(실물 — `taxonomy_products[M1-P-10…].source_text.aftercare` 가 계열 코드 없이 들어감)은 빌드 버그 — owner 를 그 taxonomy 제품(`product:` 정본 id)으로 바로잡는다(실버 수정 아님 · 읽는 칸 `step5 taxonomy_products[].product`)

**v3.2 — F-D′(조합 잎 보강 · B 「노드 속성(combo) · 노드에 안 닿음」 Q018 c3)**: 조합 노드 속성 중 fact 가 없던 잎 — 실물(11-01 재대조 · 검수 W-5)은 **`step7 combos[].consult_copy.patientExplanation` 하나**(목적 레시피 RC-RE-R1~R7 · 7건 · 골드 export 에 fact 0) → fact id `combo:RC-RE-R{n}#overview#consult_copy.patientExplanation` · owner 그 combo · section `overview` · **가드 = 7**(`counts.v3_facts.fd2_patient_explanation == 7`). 원장 `treatment-optimization` 의 `severity_levels[].sequence · rationale · contraindicated_combos · expected_sessions` 는 **실버에 칸이 없다**(step7 · step8 · semantic grep 0) → 9단계 몫(V-4 · Q189 는 §8 N-9단계) · `consult_copy` 는 `sales_copy`(G12 영업 문구) 와 다른 칸이라 거르지 않는다. `complications.management` · `prevention` 은 A 그룹(9단계 · V-4) — 여기서 안 만든다.

**v3.2 — F-F(섹션 매핑 밖 24 · B 「섹션 요청했는데도 응답에 없음」 · 2차 분류)**: 아래 fact id 는 전부 골드 export(d3a1abd5)에 **있고**(실물 확인 — 예 `family:M7` 의 `attrs.gold.sections.recovery` 에 downtime · duration_simple 2건) 요청 section 도 §5-4 매핑 안인데 응답에 없었다. 원인은 구현(예산 · by_unit 상한 · 멤버 판정)이지 매핑 규칙이 아니다 — 그래서 **행마다 같은 입력으로 응답 `facts[].id` ∪ `more_ids` ∪ 동봉 id 에 있어야 한다**(§6-4 시험 · §6-5 (iii)). 매핑 열 = 이 id 가 어느 규칙으로 응답 노드에 닿는지.

| 문항 · 케이스 | 호출(도구 · 입력 노드 · section) | fact id | 매핑(v3.2) |
|---|---|---|---|
| Q014 c3 | procedure_card family:M7 · I-05 · recovery | `family:M7#recovery#family_text[환자 설명 가이드(patient-education)][0].downtime` | 계열 owner `recovery` — §5-4 recovery 행 · 묶음 안(I-05) · 원문 상한 4 안 첫 순서(단일 칸 먼저 정렬) |
| Q015 c3 | compare product:M9-1-1 · M9-1-2 · U5-102 · I-06 · overview | `family:M9#overview#family_text[…][0].common_concerns[0].q` | 입력 노드(제품 · 단위)의 계열 overview(`fam_sec`) — compare `node_sections` 에 id · 원문은 상한 안 |
| Q025 c3 | combos 메뉴 쁘띠시술 · I-11 · market | `combo:RC-PC-P1-3#market#price` | 조합 수준 section `market`(combos `combos[].sections`) + C7′ price id |
| Q027 c2 | procedure_card product:M1-2-1 · timeline | `botox#phases[3].normal[1]` | 제품 카드 `timeline` = 쓰는 단위 시술의 타임라인(by_unit) — 제품 by_unit 은 **id 전부**(단위 ≤ 4 · 넘으면 `units_more`) |
| Q057 c3 | compare product:M4-1-1 · U5-018 · I-06 · overview | `family:M4#overview#family_text[…][0].common_concerns[1].a` | Q015 c3 와 같음 |
| Q078 c2 | procedure_card family:M9 · overview | `family:M9#overview#family_text[…][0].pain_level` | 계열 owner overview · 단일 칸 먼저 정렬 → 상한 4 안 |
| Q081 c3 | compare U5-022 · U5-140 · I-06 · evidence | `combo:RC-CP-acne#evidence#members[1].attrs_text.duration` | C10′ — 멤버 `units` ∋ 입력 단위(실물 RC-CP-lifting members[1] = U5-091 · U5-104 꼴 · `combo_component` 엣지 `field == members` 로 찾음) · 비교 대상 멤버 잎 전부 원문 |
| Q095 c2 · c3 | procedure_card family:M11 · aftercare / check_conditions family:M11 · aftercare | `product:auto-M11-1775360637715#aftercare#extracted[…].source_text.aftercare[2]` | 계열 카드 `aftercare` by_unit → 단위 시술의 쓰는 제품 수준 aftercare 는 **id 로**(§5-4 aftercare 행 「붙는 수준 그대로」 · 단위 → 제품 1-hop 은 id 전부 · 원문은 `product=` 지정 때) |
| Q096 c3 | check_conditions family:M11 · I-09 · safety.complications | `CX-M11-03#prevention` | C6′ 합병증 잎 id 전부 · `sections=safety.complications` 면 원문 상한 안 |
| Q103 c2 | recommend concern:P5-1 · overview | `family:M8#overview#family_text[…][0].common_concerns[2].a` | recommend 카드 section 은 요청 section 만 원문(I-01 묶음 없음) · 계열 수준 원문은 응답에 한 번(`facts` id 중복 제거) |
| Q121 c3 | recommend P6 · site.face · I-01 · evidence | `combo:RC-CP-acne#evidence#members[4].attrs_text.best_for` | C7′ refs id(원문은 compare) |
| Q124 c2 | check_conditions family:M8 · safety.side_effects | `product:M8-4-1#safety.side_effects#…safety.common[2]` | 계열 펼침 단위의 쓰는 제품 side_effects **id**(§5-4 safety 행 · 단위 → 제품 1-hop id) |
| Q125 c3 | procedure_card family:M8 · I-04 · aftercare | `product:M8-4-1#aftercare#…aftercare[0]` | Q095 와 같음 |
| Q126 c2 | check_conditions U5-030 · checks | `K8-0230`(C-DERM) | C2′ 주장 id 전부(전 등급) · `sections=checks` 면 원문 |
| Q135 c2 | procedure_card family:M8 · recovery | `family:M8#recovery#family_text[…][0].downtime` | Q014 와 같음 |
| Q136 c3 | procedure_card family:M8 · I-03 · timeline | `fractional-co2#phases[4].normal[3]`(U5-028) | 계열 카드 timeline by_unit **id 전부**(단위 ≤ 4 는 id · 나머지 `units_more` — U5-028 이 4 밖이면 `units_more` 에 단위 id · 타임라인 id 는 `expand`/단위 카드) → **단위가 4 밖이면 닫히지 않는다** · 끝 조건은 「단위 4 안이면 id」 로 재고 그 밖은 §6-6 걸음 |
| Q139 c3 | pair_check U5-045 ×2 · I-07 · evidence | `combo:RC-OP-Acne-중등도#evidence#rationale` | C7′ refs |
| Q140 c3 | procedure_card family:M8 · I-04 · timeline | `fractional-co2#phases[4].normal[1]` | Q136 과 같음 |
| Q150 c2 | check_conditions family:M8 · safety.pih | `unit_procedure:U5-023#safety.pih#pih[3].fitzpatrick_note` | C12′(펼친 단위마다 pih 잎 id) |
| Q165 c3 ×2 | procedure_card family:M15 · I-05 · recovery · timeline | `family:M15#recovery#…downtime` · `chemical-peel-mid#phases[3].normal[0]` | Q014 · Q136 과 같음(코디 10-31 ④ 「범위 밖」이었으나 2차 분류에서 같은 꼴 — v3.2 는 F-F 로 닿게 함) |
| Q191 c3 | compare U5-091 · U5-104 · I-06 · evidence | `combo:RC-CP-lifting#evidence#evidence_notes[2]` | C7′ refs(evidence_notes 잎) |

- 열거 24건 중 2차 분류 「섹션 요청했는데도 응답에 없음」 24 = 위 행(문항 · 케이스 21줄 · 24행) — §8 의 **F-F** 열과 1:1

---

## 5. 도구(REST · MCP 같은 코어 · LLM 없음)

### 5-0. 공통

- 도구 코어 = 순수 함수(메모리 그래프 → 응답 dict). REST 라우터와 MCP tool 은 같은 함수를 부르기만 한다(v1 `mcp_server.py` 머리 원칙과 같음). 입력 이름 · 기본값 · 검증 · 오류 문구가 둘에서 같다
- 모든 응답 머리: `{"build": {"id", "build_hash", "published_at"}, "request": {입력 그대로}, …}`
- 오류: 없는 id · 틀린 종류 · 한도 넘음 = 4xx + 도메인 오류 문구(MCP 는 같은 문구의 tool 오류)
- **후보 여럿 처리**(10-27 W-1 · G7): 말이 여러 노드를 가리키면 고르지 않고 후보 전부 + `candidates` 표시. 도구 입력은 id 만 받는다(말은 resolve 만 받음). 되묻기는 밖(LLM · 앱)
- **표시**: 행마다 표시 12 중 해당하는 것을 그대로(S6). 응답 끝 `must_show_flags` = 응답 안에 실제로 나온 표시 중 conflict · candidates · gap · weak · question · default_value · license_unconfirmed 의 집합
- **Claude 계약 블록**(10-30 O-3 결정 = D-16 추천): 응답마다 `claude_contract{allowed_fact_ids, must_show_flags, rule}` — `allowed_fact_ids` = 이 응답 `facts[].id` 전부 · `must_show_flags` = 위 표시 집합 · `rule` = 고정 문장 「카드 밖 말 금지 — 문장마다 facts id 하나 이상 · 숫자 · 기간 · 금기는 facts 원문 값만 · 시술 쌍 값은 resolved 하나(원문 대안은 alternatives 로만) · gap 은 「정보 없음」 · 후보 여럿이면 되묻기」(gold-research 6-3 문장에서 「충돌은 양쪽」만 10-30 D-13b 「충돌 하나로」에 맞춤). 허브는 블록을 낼 뿐 지키게 하는 건 앱 · Claude 몫
- **기본 응답**: G12 거르기 · G8 조건부 제외 적용. 옵션 `include_conditional`(기본 false) · `include_not_recommended`(기본 false)로만 뺀 것을 다시 냄(뺀 것은 `excluded_counts` 로 셈만 늘 냄)
- **안전 동봉**: 시술(단위 시술 · 제품)이 응답 어디에든 나오면 그 시술의 G13 안전 묶음을 같이 냄 — slim 이어도 안전 칸은 빠지지 않음(상태 · fact id · 짧은 이름. 긴 원문은 full). **v3.3(W7-D9)**: 계열 · 제품을 펼친 단위 시술의 안전 요약은 **≤ 8 단위**(`GOLD_SAFETY_UNITS_MAX=8` · 요청 단위 먼저 · 나머지는 `_units_total` 셈 · 0 = 전부) — 요청 노드 자신의 안전 요약은 그대로 늘
- **응답 크기**(D-14 · S1 · S2 · v3 · **v3.2 §5-0-1**): 카드는 기본 slim · 원문은 `sections`(명시 ∪ **의도 기본 묶음 §5-14**)의 칸만 · 단위 시술 관계 목록은 카드에 싣지 않고 `pair_check` 로만 — 단 **의도별 고정 동봉(§5-13)** 은 요약 꼴(id · 이름 · 등급 · 값 · fact id · 상한 안의 원문)로 늘 같이 낸다. **v3.2**: 원문은 「요청 노드 자체 수준 × 의도 묶음 section」 안에서만 · 그 밖은 id 만(§5-0-1 A1-1~A1-6) · 도구별 상한은 §5-0-1 표
- **facts**: 응답에 나온 원문은 `facts[]{id, text, section, flags, state, source}` 로 모아 내고 카드 · 행은 fact id 로 가리킨다
- **`intent?: I-01 … I-12`(v3 · 도구 9 공통 입력)**: 의도를 받으면 §5-13 동봉 묶음과 §5-14 섹션 기본 묶음을 그 의도로 고른다. **없으면 도구의 기본 의도**(표 §5-1 의도 열의 첫 값 — T2 I-01 · T3 I-02 · T4 I-07 · T5 I-09 · T6 I-06 · T7 I-11 · T1 · T8 · T9 = 없음 → G13 안전 요약만)로 같은 일을 한다 — Jev · Claude 가 안 골라도 기본이 붙는다(B ① 53 · case3 Jev 가 상위 4 밖으로 자르거나(8) 안 고른(10) 건). 모르는 값 = 4xx
- **`sections` 합집합(v3)**: 요청 `sections` 가 오면 **의도 기본 묶음 ∪ 요청** · `sections=none` 은 기본 묶음도 끈다(실험 대조용 · 안전 요약 · 동봉 요약은 그대로) · `sections=all` 은 전부. 응답 머리 `sections_used[]`(실제 적용된 집합) · `intent_used`
- **동봉 · 섹션은 「응답에 나온 시술 노드」 단위**(v3): 단위 시술 · 제품 · 계열이 응답 어디에 나오든(카드 · 쌍 · 비교 · 조합 구성 · 이웃) 그 노드마다 같은 매핑 함수(§5-4 카드 칸 표 + F-E)로 facts 를 찾는다 — 도구마다 따로 매핑하지 않는다(B ② 의 compare · check_conditions · recommend 구멍)

### 5-0-1. 응답 다이어트(v3.2 · A-1 · case2 기본 응답 · case3 는 §5-16)

**왜**: rerun-v3 에서 case3 허브 결과 중앙 46.5KB(p95 171KB · 최대 281KB) · case2 도 27KB 로 커졌고, 크기 구간 0–10KB 에선 C(허브가 줬는데 답이 놓침) 0% · 40–80KB 9% · 80KB+ 10%(`fail-triage2.md` §5). 커진 자리 = 계열 id 카드(case3 procedure_card 78 중 계열 61 · 중앙 59KB · p95 204KB) · check_conditions 계열 펼침(16 중 15 · 중앙 97KB) · 동봉 원문 · 기본 묶음 ∪ Jev section 4 의 원문(`runs.jsonl` rerun-v3 실측). 규칙은 **「원문은 질문이 가리킨 자리에만, 나머지는 id」** 하나다. LLM 없음 · 결정론 유지.

| id | 규칙 | 구체(결정론) |
|---|---|---|
| A1-1 | **응답 노드 = 요청 노드** | 원문 · 동봉은 **요청으로 받은 노드**(T3 `id` · T4 · T6 `procedures` · T5 `id` · T7 `procedure` · T2 는 카드 단위 시술)에만. 계열 · 제품을 펼친 단위 시술(`expanded` · `by_unit`) · 조합 구성 · 이웃은 **id · 이름 · 셈**(W5-D2 확정). 펼친 단위 시술의 section 은 `by_unit{unit: [fact id]}` **id 만**(원문 0) · 단위 ≤ 4(`GOLD_CARD_BY_UNIT_MAX=4`) · 나머지 `units_more[]` · 더 받기 = 그 단위 id 로 T3 또는 T11 |
| A1-2 | **부위 위험(C1′)은 resolve 된 부위 · 같은 계열만** | 질문의 부위 = T2 `site`(resolve 로 잡힌 site) 또는 요청 단위 시술의 `key.site`(부위 트리 체인 포함). SC 엣지는 **그 부위 체인에 닿고 계열이 같은 것**만(W5-D13 「계열 무관」을 되돌림 — Q003 「엉뚱한 연결」). 계열 · 제품 카드는 그 계열 SC 중 요청 부위가 있으면 부위 일치만 · 부위 없으면 전부(엣지 ≤ 3 · 잎 id 전부 · 원문 `key_warning` 1) |
| A1-3 | **확인 조건(C2′) 원문은 질문 조건만** | 원문 = T5 `conditions` 입력 또는 resolve 로 잡힌 `check_condition` 후보(응답 머리 `question_conditions[]`)의 주장(≤ 4) **+ 금기 주장 앞 2**(v3.3 · W7-D3 — 「없으면」 아님 · 늘). 금기 조건의 짧은 이름은 전부(`compact_safety.contra` + `names`). 전 등급 · 계열 상속 주장은 **기본 응답에서 셈**(`claims_n` · `index.checks{cond: {name, claims_n}}` · W7-D1) · id 전부는 `sections=checks` 명시 때 |
| A1-4 | **의도 묶음 밖 section 은 id 만** | `sections` 요청이 의도 묶음 밖이면 그 section 은 **id ≤ 4 + `n`**(원문 0 · `more_ids`) — 원문은 묶음 안 section 에서만. 의도 묶음 밖 section 중 **묻지 않은** section 도 단일 노드 도구(T3 · T4 · T5 · T6 · T7 · T8)에선 `sections_index{section: {n, ids[:4]}}` 로 id 노출(**v3.3 · W7-D1: 기본 응답 꼴은 `{n, units_n}` 셈 — 닫힘은 (b) 추가 호출 1**)(§5-14′ · B 기본 묶음 밖 33 + Jev 안 고름 12 + 상위 4 밖 5 가 id 로 닫힘). T2 recommend 는 카드가 여럿이라 `n` 만(§5-14 I-01) |
| A1-5 | **section 원문 상한** | 묶음 안 section 원문 ≤ **4**/section(`GOLD_SECTION_FACTS_MAX=4` · 단일 칸(pain_level · downtime …) 먼저 · 번역문 `patient.*` 뒤) · 응답 전체 원문 ≤ **24**(`GOLD_RESPONSE_FACTS_MAX=24` · 동봉 원문 먼저) · 의도별 덮어쓰기 `INTENT_CAPS` 는 이 값 이하만(카드 의도 section 12 · 예산 60 폐기) |
| A1-6 | **더 받기(v3.3 · W7-D1)** | **기본 응답**(요청 `sections` 없음)에서 상한 밖 fact 는 **셈만** — 응답 머리 `more{section: n}` · 카드 `by_unit{단위: n}` · `sections_index{s: {n, units_n}}` · 동봉 `facts_n` · `claims_n` · `refs_n`. **명시 `sections`** 의 section 만 `more_ids[]` id 전부 + `total`. 더 받기 = ① 같은 도구에 `sections=<이름>` 명시(원문 ≤ 12 · `GOLD_EXPLICIT_FACTS_MAX=12` — 단 **T5 `sections=checks` · T4 `sections=evidence` 명시는 주장 원문 전부** · W7-D6 · 품질 I-09 5문항) ② T11 `expand(id, sections)`(§5-16 · 한 줄 목록 → `full` · `fact_ids`) ③ pair_check — **fact id 단건 조회 도구는 두지 않는다**(V-8 · `expand.fact_ids` 로 대신). `claude_contract.rule` 에 「`more_ids` 는 더 받을 수 있다는 뜻 — 인용하려면 받아서 원문으로」 한 문장 |
| A1-7 | **응답 수준 색인(중복 제거)** | 같은 조합 · 확인 조건 · 계열 정의가 카드 여럿에 되풀이되지 않게 응답 머리 `index{combos{id: {name, kind, refs_n}}, checks{cond: {name, claims_n}}, families{id: {definition}}}` 를 **한 번** 내고(v3.3 · W7-D13 — relations 는 색인에 없고 카드 `relations_all{edges ≤ 20, n, forbid_n, claims_n, global ≤ 4}` · id 목록은 셈 W7-D1) 카드 동봉은 id 참조(`same_as` 를 일반화 · W5-D2). recommend 10장 × 동봉 ≈ 0.9KB(`work005-report.md`)가 바닥이던 것을 카드당 ≈ 0.3KB 로 |
| A1-8 | **claude_contract 우선순위** | `claude_contract.priority[]` = 이 응답 `allowed_fact_ids` 를 **① 질문 부위 일치(SC · 부위 체인) ② 요청 노드 자체 수준 × 의도 묶음 section ③ 금기 · 금기류 주장 ④ 요청 section(묶음 밖) ⑤ 나머지** 순으로 정렬한 목록 · `use_first[]` = 앞 8개 · 규칙만(LLM 없음 · 결정론 · 같은 입력 같은 순서 · 동순위는 fact id 순). 지키게 하는 건 앱 · Claude 몫(O-3 와 같음) |
| A1-9 | **도구별 기본 응답 상한(숫자 · 2.5× 폐기 · v3.3 = 측정값)** | 아래 표. 「기본 응답」 = 요청 `sections` 없음 · `intent` 있거나 도구 기본 의도. 넘으면 **상한 값(A1-5 · 동봉 상한)을 줄인다** — 동봉 종류 · section 을 빼지 않는다. 값은 설정 `GOLD_SIZE_CAPS`(json) · v3.3 에서 측정값으로 정함(V-3 닫음) |

**v3.3 표(이번 판 결정 · 측정값 기준)** — v3.2 표(recommend 12,000 등)는 WORK-007 이 SPEC 글자 그대로 · 코디 C 둘 다로 쟀을 때 카드 도구 8 전부 넘었다(`work007-report.md` §2). 이 판은 **WORK-007 측정값(676 재실행 · in-process · 발행 b031371c · `build-out/recheck2/sizes.json`)을 위로 올림한 값**을 상한으로 둔다 — 근거: 같은 크기로 돈 rerun-v4 에서 case2 정확성 49 → 58% · C(허브가 줬는데 놓침) 비율 case2 6.6% → 3.8%(`verify-b202611011148-c6ed3a.json c_ratio` 4/106) · 잘림 0(같음 484/484). 상한은 **회귀 경계**다(더 키우지 않음) — 더 줄일 자리 6(`work007-report.md` §2)은 이 판에서 하지 않는다(§7 V-14). case3 는 걸음(§5-16)으로 바뀌었으므로 「case3 경로 합」 행은 지운다 — 걸음 예산은 SPEC-006 · 앱 몫이고 허브는 T10 · T11 한 번의 크기만 진다.

| 도구 | 기본 응답 **중앙 ≤** | **p95 ≤** | 측정(WORK-007 · 기본 n · 중앙 / p95 / 최대) | 근거 · 손잡이 |
|---|---|---|---|---|
| T2 recommend(카드 ≤ 10) | **29,000** | **43,000** | 34 · 28,394 / 42,623 / 48,374 | 카드당 ≈ 3.3KB(C4′ 제품 5행 0.77 · 관계 엣지 id 0.44 · sections_index 0.4 · 안전 0.3) + index.combos 5.8KB · index.checks 2.5 · facts 4.7 · claude_contract 2.0 |
| T3 procedure_card — 단위 시술 · 제품 | **12,000** | **24,000** | 1 · 11,620(기본 응답 표본 1 — 위로 올림만 · p95 는 v3.2 값 유지) | 「sections 있음」 56 · 19,886 / 46,706 은 보고만 |
| T3 procedure_card — 계열 | **11,000** | **13,000** | 5 · 10,961 / 12,687 / 12,687 | by_unit 셈 · 단위 ≤ 4 |
| T4 pair_check | **19,000** | **27,000** | 20 · 18,536 / 26,493 / 27,258 | C9′ 2/쌍 · 쌍 12 · 안전 요약 ≤ 8 단위(W7-D9) |
| T5 check_conditions | **17,000** | **24,000** | 5 · 16,566 / 23,917 / 23,917 | 펼침 8 · C2′ 셈 |
| T6 compare | **33,000** | **43,000** | 10 · 32,893 / 42,808 / 42,808 | C10′ 6/멤버 |
| T7 combos | **22,000** | **26,000** | 2 · 21,300 / 25,891 / 25,891 | 원문 추천 패키지 2 |
| T8 neighbors | **10,000** | **25,000** | 3 · 9,341 / 24,552 / 24,552 | 이웃 동봉 없음 |
| T1 resolve · T9 vocab | 2,000 · 8,000 | 4,000 · 16,000 | 198 · 1,308 / 2,405 · 3 · 5,841 / 6,654 | 변경 없음(v3.2 표 안) |
| **T10 peek**(§5-16) | **2,500** | **8,000** | 1,071 노드(같은 기준 · 이 스펙 측정 e) · v3.2 꼴 2,183 / 6,788 / 8,907 → v3.3 `n_facts` 더해 **2,257 / 7,171 / 9,477**(중앙 +74B) · 참고(다른 기준): WORK-007 보고 2,271 / 7,248 / 9,506 · **보고 칸**: rerun-v4 걸음이 실제로 연 peek 311 = v3.2 꼴 2,845 / 8,408 → v3.3 3,054 / **8,926**(p95 상한 넘음 · peek 는 앱 예산 밖이라 끝 조건 영향 없음 · `b_v4_calls.peek_new`) | 앞 4 · 이름 20자 |
| **T11 expand 기본 꼴 — section 1**(§5-16 v3.3) | **2,000** | **5,000** | 전 6,140 (노드, section) · 1,902 / 2,710 / 3,228 · rerun-v4 걸음 호출 476 재생 2,014 / 3,676 / 4,720(이웃 포함) · 676 재실행이 닿은 481 쌍 1,890 / 2,647(이 스펙 측정 a · b · c) | 한 줄 40자 · 1쪽 12줄 · id 1번 |
| **T11 expand `full=true` — section 1** | **4,000** | **8,000** | 6,140 · 2,982 / 4,256 / 5,210(이 스펙 측정 e) | 원문 · `source{file, path}` |

- 측정 열의 T11 은 **옛 expand 와 같은 입력**의 비교값: 옛 꼴 6,140 쌍 중앙 6,733 · p95 20,863 · 최대 59,277 · rerun-v4 걸음 호출 기록 476 중앙 7,987 · p95 13,220 · 최대 60,732(재계산 475/476 이 기록과 바이트 같음 — 1건 33B 차 · 정수/실수 직렬화)

- 바이트 = **허브가 보내는 REST 본문** — 응답 JSON `ensure_ascii=False` · 구분자 `(",", ":")`(FastAPI `JSONResponse` 그대로 · §6-5 셈 규칙과 같음). 중앙 · p95 는 rerun-v3 실제 호출 묶음(676)을 같은 입력으로 재실행한 값(§6-5) · T10 · T11 은 위 측정 열. 앱(clinic_chat f8533ff `case3._hub`)은 `json.dumps(d, ensure_ascii=False)`(공백 있는 구분자)로 세어 같은 응답이 ≈ 4~7% 크게 잡힌다(T11 새 꼴 476 호출 중앙 2,014 → 2,146) — V-17 닫힘(코디 11-01): 앱도 허브와 같은 직렬화로 센다
- 안전 요약(G13 · `compact_safety`) · `claude_contract` · 응답 머리는 다이어트 밖(늘 있음) — 단 펼친 단위 안전 요약은 ≤ 8(W7-D9)
- 다이어트는 **case2(Claude 가 부르는 MCP) 기본 응답**에 그대로 적용된다.

### 5-0-2. MCP 전달 계약(v3.2 · 코디 보충 2 · SPEC-006 v2 §3-5 · §3-6 · W-2 가 허브에 요구하는 두 줄)

| id | 조항 | 실물 근거 |
|---|---|---|
| M-1 | **도구 결과 크기 meta** — 허브 MCP 도구 **전부**(골드 9 + raw 3 = 12 · v3.2 의 T10 · T11 까지 14)에 `meta={"anthropic/maxResultSizeChars": <값>}` 을 단다. 값 = 설정 `GOLD_MCP_RESULT_MAX_CHARS`(기본 **200,000** · SPEC-006 v2 `MCP_RESULT_MAX_CHARS` 와 같은 값 · env 예시 파일에) · raw 는 `RAW_MCP_RESULT_MAX_CHARS`(같은 기본값). 목적 = Claude CLI 가 성공 텍스트 결과 약 50,000자 초과를 파일로 저장하고 모델에 약 2KB 미리보기만 넘기는 잘림(2차 분류 case2 100/614)이 안 나게 — 서버가 도구 정의 `_meta` 로 문턱을 올리면 그 도구는 그 값까지 전달(SPEC-006 v2 §3-5 표 · 공식 문서 · 실측 250,000 자) | `mcp` 2.3.0(pyproject `mcp>=2.3,<3` · 설치본 확인 11-01) `MCPServer.tool(name, title, description, annotations, icons, meta: dict | None, structured_output)` — `meta` 인자 있음 · 지금 코드는 `annotations` 만 씀(`mcp_server.py:57~` · raw `mcp_server.py:34~`) |
| M-2 | **intent 문구** — 도구 9(T2~T7 · T8 · T9 · T1)의 설명 · 입력 스키마 `intent` 설명을 「**반드시 넘긴다** — 의도 표: I-01 고민 → 추천 · I-02 시술 설명 · I-03 주의 · 사후관리 · I-04 부작용 · 합병증 · I-05 회복 · 효과 기간 · I-06 비교 · I-07 같이 · 순서 · 간격 · I-08 이전 시술 뒤 가능? · I-09 나한테 해도 되나(확인 조건) · I-10 용량 · 회차 · 제품 · I-11 추천 조합 · 패키지 구성 · I-12 가격(허브 도구 없음). 없으면 도구 기본 의도(T2 I-01 · T3 I-02 · T4 I-07 · T5 I-09 · T6 I-06 · T7 I-11)」 로 바꾼다(REST query · body · MCP 인자 · 서버 `instructions` 한 줄 같은 문구 — `schema/gold.py INTENT_DESC` 하나에서). 스키마 **required 는 하지 않는다**(선택 유지 · 설명에 필수 명시 — 코디 추천): required 로 하면 `intent` 를 안 넘긴 호출이 4xx 가 되어 case2 가 「응답 없음」으로 더 나빠지고 · 기본 의도 규칙(§5-0 V-2)이 죽는다. 넘긴 비율은 앱 기록(SPEC-006 §4-2 `intent_passed`) | 지금 `INTENT_DESC` = 「의도 코드 I-01~I-12(v3 · 선택) — … 없으면 도구 기본 의도」 · 서버 `instructions` 에 intent 언급 없음 |
| M-3 | T10 peek · T11 expand 는 `intent?` 를 **받되 무시한다**(§5-16 · 검수 F-1 · SPEC-006 v2 §3-4-1 「걸음 중 허브 호출에 intent 를 넘긴다 · 단 의도 묶음 · 동봉은 안 씀」 · 결정표 「허브는 받기만」) — 받으면 `request` 에 그대로 적고 `intent_used: null` · 동봉 · 묶음 0 · 모르는 값만 4xx(도구 9 와 같은 검증) · 설명에 「의도는 기록용 · 동봉 없음 · Jev 걸음용」 한 줄 | — |

- 시험(§6-4): 도구 정의 `list_tools` 에 14 도구 전부 `_meta["anthropic/maxResultSizeChars"] == 설정값` · `intent` 설명이 9 도구 · REST 스키마 · 서버 instructions 에서 같은 문구(상수 하나) · required 아님(`intent` 없는 호출 200)
- 실물 확인(WORK-007 WP-6 · 코디 승인 뒤 1회): Claude CLI 2.1.284 로 허브 MCP 를 붙여 check_conditions 계열 호출(응답 > 50,000 자인 입력 1개 · 예 `family:M8` sections=all)을 1회 — 모델이 받은 결과에 「Output too large」 미리보기가 **없음**. SPEC-006 v2 WP-0 확인 시험과 같은 호출을 써도 된다(앱 쪽이 먼저 하면 그 기록으로 대신)
 case3 는 §5-16 peek/expand 로 Jev 가 크기를 정하므로 의도 묶음 · 동봉 자동 첨부를 **쓰지 않는다**(`intent` 를 안 넘기고 `sections=none` + peek/expand · 선택 가능은 유지)

### 5-1. 도구 목록

| id | 이름 | REST | MCP tool | 의도 | 경로 |
|---|---|---|---|---|---|
| T1 | resolve | `GET /procedure-hub/gold/resolve` | `resolve` | 공통(말 → 후보) | — |
| T2 | recommend | `POST /procedure-hub/gold/recommend` | `recommend` | I-01 | P-01 |
| T3 | procedure_card | `GET /procedure-hub/gold/procedures/{id}` | `procedure_card` | I-02 · I-03 · I-04 · I-05 · I-10 | P-02~P-05 · P-10 |
| T4 | pair_check | `POST /procedure-hub/gold/pairs` | `pair_check` | I-07 · I-08 | P-07 · P-08 |
| T5 | check_conditions | `GET /procedure-hub/gold/procedures/{id}/checks` | `check_conditions` | I-09 | P-09 |
| T6 | compare | `POST /procedure-hub/gold/compare` | `compare` | I-06 | P-06 |
| T7 | combos | `GET /procedure-hub/gold/combos` | `combos` | I-11 | P-11 |
| T8 | neighbors | `GET /procedure-hub/gold/nodes/{id}/neighbors` | `neighbors` | 정해 둔 경로 밖 | — |
| T9 | vocab | `GET /procedure-hub/gold/vocab` | `vocab` | Jev 슬롯 선택지 | — |

- 헬스 `GET /procedure-hub/gold/health` = DB 연결 · 발행 빌드 id · 메모리 적재 셈(도구 셈에 안 넣음)
- I-12 가격은 허브 도구 없음(연결 층) — 허브는 단위 시술 · 제품 id 만
- **v3**: 의도 열의 첫 값이 그 도구의 기본 의도(§5-0 `intent` 없을 때). **I-07 · I-08 경로는 쌍 도구(T4) 필수** — 시술이 하나만 잡혀도 T4 를 부른다(§5-5 「입력 1개」 모드 · B ④ 「pair_check/compare 안 부름」 4건 · 「다른 쌍」 14건 중 한쪽만 잡힌 건). I-06 은 T6 필수 · 둘 다 §5-13 동봉을 낸다

### 5-2. T1 resolve — 사전 검색

| 칸 | 값 |
|---|---|
| 입력 | `text: str`(필수 · 1~200자) · `kinds?: [node kind]`(거르기) · `limit_per_span?: int = 20`(≤ 50) |
| 규칙 | `semantic.json dictionary.resolve_rules` 그대로(문서 = 코드 · 품질 M): 정규화(NFKC → 라틴 악센트 접기 → fold 「쳐짐 → 처짐」 → 공백 제거 → 괄호 지움 → 소문자) → order 4단계: ① 완전 → ② 낱말 나눔(split `[\s/·,()\[\]+]+` 으로 나눠 낱말마다 완전) → ③ 끝말 떼기(tails 「주사 · 시술」) → ④ 접두(질의 2자 이상 · 대상 계열 · 고민 대분류 · 부위 · 목적이 하나로 모일 때만 — 여럿이면 못 찾음). 앞 단계에서 찾으면 다음 단계 안 감(D-11) |
| 출력 | `{"matches": [{"span", "stage": "완전\|낱말\|끝말\|접두", "mode": "하나\|전부\|후보", "ambiguous", "collision", "candidates": [{"id", "kind", "name", "qualifier", "reasons", "flags"}], "menu_candidates": [{"id", "label", "kind"}]}], "unmatched": [str]}` |
| qualifier | 사전 `targets[].qualifier` 그대로 — `{"cc": …}`(CC 고민 앵커 · R28) · `{"taxonomy_entry": "P1"}`(메뉴 · J5) · `{"ledger": …}` 등 |
| 메뉴 후보 | G18 이 더한 `menu:{라벨}` 대상은 같은 match 안의 별도 후보 `menu_candidates[]{id, label, kind: "menu"}` 로 낸다 — 기존 `candidates[]` 와 `mode` 는 사전 그대로(예: 「처짐/탄력」 → `candidates` = P3 · P4-1 · mode 「전부」 그대로 + `menu_candidates` = `menu:처짐/탄력` · 「쁘띠시술」 → `candidates` = `none:고민 노드 아님(트리 항목)` + `menu_candidates` = `menu:쁘띠시술`). 메뉴 후보는 T7 `menu` 입력으로만 이어짐(판단 ②) · 고르지 않음 |
| mode | `하나` = 대상 1 · `전부` = 대상 전부에 적용(묶음 이름 → 고민 여럿 · 갈래 A · I) · `후보` = 고르지 않음(나머지 갈래) |
| 부분 일치 표시 | 접두로 찾은 후보는 `flags` 에 `prefix` |
| unmatched | 끝까지 못 찾은 낱말 — §3-6 보강 후보로 기록(응답에는 그대로) |

### 5-3. T2 recommend — 고민 → 추천(① CC 슬롯)

| 칸 | 값 |
|---|---|
| 입력 | `concerns?: [concern id]`(cc 나 site 가 있으면 0 허용 · D-1) · `site?: site id` · `cc?: str`(원천 CC 이름 · 골드 판단 ① · R28) · `cc_roots?: [P{n}]`(고민 노드 없는 대분류만 — 쁘띠시술 P1 · 기타 P14 · 없으면 P = concerns 의 대분류 · D-1) · `limit?: int = 10`(1~200 · 넘는 카드는 `more_cards` id 목록 + `cards_total` · D-10) · `include_conditional?: false` · `include_not_recommended?: false` · `intent?` · `sections?`(§5-0) |
| 경로 P-01 | ① 고민 + 하위 고민(child_of) — 조상 · 자손이 같이 오면 자손만 · 고민에 부위 1개면 그 부위 · 부위만 오면 그 부위 고민 → ② **cc 가 오면**: 같은 원천 문제(P) 안에서 `ccs[]` 에 그 CC 가 든 treats 엣지만(출발이 고민 · 목적 · 앵커 없음이어도 CC 로 찾음). cc 가 없거나 원천 CC 가 아니면 고민 노드 treats 엣지 전부 → ③ 부위 층 거르기(`site_rules.climb` — 부위 · 하위 → 상위(묶음 통과) → 영역 「전체」 노드 · `site_rules.site_free` 「해당 없음」 · 「병변 단위」 단위 시술은 통과) · `layer` 「상위」(얼굴 전체 층) 엣지도 같이 내되 `layer` 표시(U-1 = ②) → ④ 부위 없이 고민만이면 기본 영역 = 얼굴 + 다른 영역 시술이 있으면 `other_regions` 표시(D-12) → ⑤ 단위 시술마다 G13 안전 묶음 · 쓰는 제품(G5 · recommendable 만) · 추천 조합 앵커 id |
| 출력 | `areas[]{site, name, layer: "부위\|상위\|영역 전체", concerns[], card_ids[]}` · `cards[]`(slim 카드 §5-4 + `why[]{edge, from, source, layer, flags, role?: fact id}` + **I-01 동봉 §5-13**) · `cc_roots_used` · `by_cc` · `more_cards?` · `cards_total?` · `family_only[]{family, reason(site_check · resolve_flag 값), flags}` · `facts[]` · `must_show_flags` · `excluded_counts` · **v3.2** `index{…}`(A1-7) · `why[].role` = treats `row.evidence.role` fact id(F-C · B Q193 c2) · 카드 section 은 요청 section 만 원문(상한 4) · 묶음 밖은 `n` 만(A1-4) |
| 정렬 | 결정론 — `layer`(부위 → 상위) · 엣지 원천 순서 · 단위 시술 id |

### 5-4. T3 procedure_card — 시술 카드

| 칸 | 값 |
|---|---|
| 입력 | `id: unit_procedure\|product\|family id` · `product?: product id`(단위 시술 카드에 특정 제품 원문 · 부작용 덮어쓰기 적용) · `sections?: [§4-3 fact section 이름 · all · none]`(D-4 — `safety` 는 `safety.side_effects` · `safety.complications` · `safety.pih` 셋) · `full?: false`(= `sections=all`) · `intent?`(기본 I-02) |
| slim(기본 · D-4 · D-6) | 이름 · 키(무엇을 · 어디에 · 어떻게) · 표시 · 안전 요약(금기 조건 id · 등급 셈 · 금기류 엣지 id · 피함 · gap · 원문 셈 `counts`) · 쓰는 제품 **셈**(목록은 `sections=products` 또는 §5-13 I-10) · **v3: §5-15 승격 칸**(단위 시술 `pih` 요약 · 계열 `definition` 1문장은 이미 있음) + **§5-13 의도 동봉** |
| sections | 의도 기본 묶음(§5-14) ∪ 요청 칸을 fact 원문으로 · 응답 머리 `more` = 안 실은 section 별 셈 |
| 제품 · 계열 id | 제품 → 그 제품이 쓰이는 단위 시술 id(G5) + 제품 속성 · 원문 · 덮어쓰기 부작용 / 계열 → 정의 · 근거 문장 · 단위 시술 id 목록 · 계열 안전. **v3(F-E ①)**: 계열 · 제품 카드의 단위 시술 수준 section(`ops · dose · market · timeline · aftercare · safety.pih · site_caution · products`)은 `sections[s].by_unit{unit id: [fact id]}` 로 단위 시술별 묶음 · 단위 시술 수 상한 = §5-13 표 「계열 펼침」(넘으면 `truncated` · `units_total`). **v3.2(A1-1)**: `by_unit` 은 **id 만**(원문 0) · 단위 ≤ 4 · 나머지 `units_more[]` · 단위 → 쓰는 제품 수준 원문(aftercare · side_effects)은 단위 id 아래 제품 fact id 로(F-F Q095 · Q124 · Q125) · 계열 수준 section(overview · method · recovery · emergency · disclosure · checks · evidence)만 원문 상한 4 |
| 관계 | 싣지 않음(S2 — pair_check 로) |

카드 칸 ↔ 실버 원문(fact section):

| 칸 | 실버 |
|---|---|
| overview · method | `step8 safety.family_text[계열][「환자 설명 가이드(patient-education)」][]` 의 `simple_explanation` · `how_it_works` · `pain_level` · `common_concerns`(17계열) · `step8 evidence.statements[] field moa · effects`(class 그대로 · `patient{}`) · `units[].ops`. 단위 시술 · 제품마다 따로 쓴 개요 · 기전 문장은 실버에 없다(계열 수준만) → §3-6 보강 후보 |
| recovery | `family_text` 환자 설명 가이드의 `downtime` · `duration_simple` |
| aftercare | `family_text` 사후관리 3종 · `step5 extracted[] · taxonomy_products[] source_text.aftercare`(붙는 수준 그대로 — 제품 × 계열 · 단위 시술) |
| timeline | `safety.timelines[]`(G11 붙는 수준) |
| emergency · disclosure | `family_text` 「즉시 내원이 필요한 징후」 · 「응급(extracted.json safety.emergency)」 / 「필수 고지」 |
| safety | 부작용(G9 덮어쓴 값 + override_of) · 합병증(`safety.complications` 펼친 행) · PIH · 상태(G10) |
| checks | T5 결과 요약(조건 · grade3) |
| site_caution | `safety.site_caution[]` 펼친 행 |
| dose | `units[].dose_range_text` · `step5 dose_range[]` · `step4_attrs` |
| products | G5 결과 · `step1` 제품 이름 · 허가 상태 · 라인 품목 · `5_spec` |
| evidence | 근거 문장 · 출처(`cites`) |
| market | `units[].market[]` 원문(요청 때만 · 화면 표시 여부는 U-3 · 앱 몫) |

### 5-5. T4 pair_check — 같이 · 순서 · 간격 · 이전 시술

| 칸 | 값 |
|---|---|
| 입력 | `procedures: [unit_procedure\|family\|product id]`(**1~6** · v3: 1개 = 「관계 목록」 모드 · 같은 id 두 번 = 자기 쌍(재시술 간격) — §3-3 자기 쌍 규칙 · 계열 · 제품은 단위 시술로 펼침 D-9 · 펼친 쌍 상한 30 `pairs_total` · `truncated`) · `prior?: {procedure: id, elapsed_days: int ≥ 0}` · `sub_condition?: {키: 값}`(예: `{"세션": "같은 날"}`) · `include_conditional?: false` · `intent?`(기본 I-07) · `sections?` |
| 경로 P-07 | 쌍 C(n,2) 마다 §3-3 앱 값 · 금기류(간격 금기 · 조합 금기 · 같은 날 불가 · 대체) 먼저 정렬 · 전역 행. **v3 입력 1개**(B ④ 「다른 쌍」 — 질문의 둘째 시술이 안 잡힌 Q017 · Q018 · Q019 · Q084 · Q112 · Q139 꼴): 그 시술(펼친 단위 시술)에 닿는 `procedure_relation` 전부를 `relations[]{edge, kinds, other{kind, id, name}, value 요약(first · days · same_day · status), claims[] id}` 로 — 금기류 먼저 · 상한 §5-13 · 되묻기 재료(상대 시술 후보 = `other`) |
| 경로 P-08 | (prior, 지금) 쌍의 앱 값으로 D-10 판정 · `C-PRIOR` 확인 조건이 있으면 같이 |
| **같은 계열 자기 쌍(v3)** | 계열 하나가 오거나 두 입력이 같은 계열로 펼쳐져 같은 단위 시술이 만나면 그 쌍은 건너뛴다(지금 규칙) · 대신 **`self_pair[]`** = 그 계열의 `self_pair == true` 엣지(실물 4 — E8-0059 M2↔M2 · E8-0214 · E8-0225 · E8-0228)의 `resolved` 를 한 번 낸다(재시술 간격 질문 · 같은 id 두 번과 같은 값) · 없으면 `self_pair: []` |
| 출력 | `pairs[]{a, b, inputs?, value{first, days, open_high, same_day, by_sub_condition, options[], by_direction?, field_status, status}, prior_ok?: true\|false\|null, prior_basis?, alternatives, claims[]{id, kind, text, flags}, reasons[](fact id · `#reason`), edges[], relation}` · `relations[]?`(입력 1개) · **`relations_all[]`(v3.2 · 입력 노드 — 펼친 단위 포함 — 에 닿는 `procedure_relation` 전부 `{edge, kinds, other, claims[] id}` · 종류 무관 · 금기류 먼저 · 상한 20 · W5-D12 `family_relations` 를 흡수 · B 「다른 쌍」 5 · 「안 부름」 Q004 꼴이 id 로 닫힘)** · `self_pair[]?` · `expanded[]?` · `global[]` · `prior_checks[]` · `safety{}` · `facts[]` · `must_show_flags` · `index{}`(A1-7). **v3 evidence 기본**(B ④ 「쌍 맞음 · evidence 안 요청」 8건 · 「요청했는데도 안 실림」 1건 Q097): 짧은 응답에서도 쌍마다 `claims[]` 는 **원문 포함**(`text` · `kind`) — 금기류 주장 먼저 · 쌍당 상한 §5-13(넘으면 id 만 + `claims_total`) · **v3.2(C9′)**: 원문 ≤ 2/쌍 · **id 는 `claims` · `reasons` 전부**(B 「쌍 맞음 · evidence 안 요청」 8 이 `R8-…#reason` id 로 닫힘) · 펼친 쌍 상한 30 → 12(금기류 쌍 먼저 · 나머지 `pairs_more[[a,b]]` id) · **조건부 주장은 `include_conditional` 과 무관하게 id + `conditional` 표시로 늘 내고** 원문은 상한 안에서 · 같은 값 쌍 묶음(D-9)은 claims 까지 같으면 묶음 |
| sub_condition | 주면 그 조건 옵션만 · 안 주면 옵션 전부(「조건 모름」 포함) — 고르지 않음 |
| 쌍 방향 | `value.first` 의 a · b 는 응답 쌍의 a · b 기준으로 맞춰 냄 |

### 5-6. T5 check_conditions

| 칸 | 값 |
|---|---|
| 입력 | `id: unit_procedure\|product\|package\|**family** id`(package = O-4 ledger 행이 붙은 패키지 · 그 밖 패키지는 빈 결과) · `conditions?: [check_condition id]` · `intent?`(기본 I-09) · `sections?` |
| **계열 · 제품 펼침(v3 · 오류 15)** | 계열 id → 그 계열 단위 시술 전부 · 제품 id → 쓰는 단위 시술(G5 저장 + 상속 후보) — `expand_units` 와 **같은 규칙**(resolve 펼침 · D-9). 지금은 계열이 400(`id: family:M8 는 family — 받는 종류 …` · 15건 = Q008 · Q021 · Q070 · Q074 · Q096 · Q099 · Q108 · Q120 · Q138 · Q141 · Q150 · Q161 · Q168 · Q169 · Q202 · 계열 M8 9 · M15 2 · M4 · M9 · M11 · M12 각 1). 펼친 결과는 **합쳐서** 낸다: 조건마다 가장 엄격한 등급 하나(금기 > 주의 > 확인만 > 확인만(고지)) + `by_unit{condition: {grade3: [unit id]}}`(등급이 단위 시술마다 갈리면 그대로 보임 · 접지 않음) · `expanded{input, kind, units}` · 단위 시술 상한 §5-13 표(넘으면 `truncated`) · 제품 id 일 때 product 키 행(7)은 지금처럼 제품 자체 행으로. **v3.2**: 펼침 단위 20 → **8**(`units_more[]` id · 등급 갈림 `by_unit` 유지) · `checks[]` 행마다 `claims[]` id 전부 + `edges[]`(`requires_check:{K8}:{C}` 엣지 id · B Q021 c2) · 원문은 A1-3(질문 조건 ≤ 4 · 없으면 금기 ≤ 2) · `not_condition` 은 fact id 목록(원문은 `sections=checks`) |
| 경로 P-09 | 단위 시술 × 조건 등급(§3-3 확인 조건) + 전역(target all 16) + 대기 기간(`wait_resolved` · 옵션 그대로) |
| 출력 | `checks[]{condition, name, grade3, scope: "unit\|product\|family\|global", resolved_id, from[], alternatives, facts[], by_unit?}` · `global[]` · `waits[]` · `not_condition`(짧은 응답 = 셈 · `sections=checks` 면 원문) · `claims[]`(그 시술 대상 확인 조건 주장 · 조건부 표시) · `safety{}` · `expanded?` · `facts[]`. **v3**: `sections` 는 §5-0 공통 규칙대로 적용된다(Q036 `emergency` 요청 무시 → 응답에 나온 시술의 emergency facts) |
| 등급 | `grade3` 4값(금기 · 주의 · 확인만 · 확인만(고지)) 그대로 · 거르기 없음(G13 — 전 등급) |

### 5-7. T6 compare

| 칸 | 값 |
|---|---|
| 입력 | `procedures: [unit_procedure\|family\|product id]`(2~4 · 계열 · 제품은 펼침 D-9 · 펼친 단위 시술 상한 8 — 입력마다 돌아가며 · `compared[]` · `truncated`) · `intent?`(기본 I-06) · `sections?` |
| 경로 P-06 | 키 칸 나란히(계열 · 하위 · 부위 · 기법) · ops · 회복 · 지속 fact · 안전 셈 → 같은 단위 시술이 든 비교 combo(`kind == 비교`)의 `members` 원문 → 대체(택 1) 관계 앱 값. **v3**: ① 차이 필드에 `overview` · `method` 를 더한다(B ② compare 7건 — 계열 환자 설명 가이드 `simple_explanation` · `how_it_works` · `common_concerns`) — 기본 묶음 §5-14 I-06 ② `source_comparisons[]` 는 짧은 응답에서도 **비교 대상 멤버의 `attrs_text` 원문**(F-C fact id + text)을 낸다 — 비교 대상이 아닌 멤버는 id · 이름만(B ⑦ 10건 · ⑥ 2건 · ⑤ combo 속성 중 비교 조합 분) ③ 두 시술 사이 `procedure_relation` 이 있으면 종류 무관하게 `relations[]`(값 요약 + claims 원문 상한 §5-13)로 — 대체(택 1)만 내던 것을 넓힘(B ④ 「compare 다른 쌍」 Q134 2건). **v3.2**: `relations_all[]`(§5-5 와 같은 꼴 · 입력 노드의 펼친 단위에 닿는 관계 전부 id · 상한 20 · B Q042 c3 E8-0005 꼴) · C10′ 멤버 판정 = `combo_component` 엣지 `field == members` 의 `units` ∋ 입력(펼친) 단위 · 비교 대상 멤버 잎 원문 ≤ 6/멤버 · 나머지 id · 입력 단위의 treats 엣지 `row.evidence.role` fact id 를 `node_sections[].why_roles[]` 로(B Q198 c3) |
| 출력 | `rows[]{field, values{id: …}}`(field = family · sub_family · site · technique · **overview · method** · ops · recovery · dose · safety_counts) · `source_comparisons[]{combo, name, members[]{unit, text, attrs_text facts}}` · `relations[]`(v3 · 대체 포함) · `alternatives[]` · `expanded?` · `compared?` · 각 시술 안전 묶음 요약 · **§5-13 I-06 동봉** · `facts[]` |

### 5-8. T7 combos — 추천 조합(② 메뉴 → 조합 · ③ 기본 응답 범위)

| 칸 | 값 |
|---|---|
| 입력 | 넷 중 하나 이상: `concern?: concern id` · `purpose?: purpose id` · `procedure?: unit_procedure\|family\|product id`(펼침 D-9) · `menu?: str`(resolve 의 `menu:{라벨}` 후보 · 판단 ② · G18) / `include_sales_copy?: false` · `include_not_recommended?: false` · `intent?`(기본 I-11) · `sections?` |
| ② 메뉴 경로 | `menu` 가 오면 `combos[]` = `kind == 추천 패키지` 이고 `anchor.source_label == menu` 인 조합만(라벨 8 · 근거: 사이트 추천 화면 라벨 = `anchor.source_label` · J5). 고민 앵커로 넓히지 않는다(R12 앵커로 다른 라벨 패키지가 섞이지 않게). 쁘띠시술은 고민 앵커가 없어 이 경로로만 나옴(J5 유지) · 같은 라벨의 나머지 6종 조합은 없음(라벨은 추천 패키지에만 있음 — 실물) |
| 고민 · 목적 · 시술 경로 | 고민 id 로 물으면 지금대로 `anchors_combo`(R12 앵커 전부 · 고민 + 하위) · 목적 · 시술은 combo_component(G17)로 그 시술이 든 조합 · 패키지 `contains`. 이때도 ③ 으로 나눔 |
| ③ 기본 응답 범위 | 응답을 두 묶음으로: `combos[]` = `kind == 「고민 패키지(사이트 「추천 패키지」)」` 만(먼저) · `reference[]` = 나머지 6종(목적 레시피 · 비교 · 세션 조합(순서) · 연간 플랜 · 연령 플랜 · 중증도 조합)에 `role: "참고"` + `kind` 표시. 패키지(step6)는 `packages[]` 로 따로 |
| 칸 | 조합마다 `{id, kind, name, tier, anchor, components[]{field, family, units[], status, flag}, flags, facts}` — 영업 문구(`sales_copy`)는 `include_sales_copy` 때만 · 구성 단위 시술의 안전 묶음 요약 동봉(G13). **v3(§5-15)**: 짧은 조합 카드에 `price`(원문) · `effect{expectedResult, clinicalRationale, riskBenefit}` fact id + 원문 · `evidence_notes` · `caveats` · `rationale` · `sessions` · `maintenance` 는 fact id(원문은 §5-14 I-11 기본 묶음 evidence) · F-A 로 붙은 step8_notes evidence fact id. **v3.2(C7′)**: 조합마다 `refs[]` = 그 조합 owner · attached fact id **전부**(evidence · timeline · checks · overview · market — F-D · F-D′ 잎 · 비교 조합 members 잎 포함) · 원문은 추천 패키지 앞 2 의 price · expectedResult 만 · 구성 계열 동봉은 `index` 참조(A1-7) |
| 정렬 | combos: tier 원천 순서 · 조합 id / reference: kind 고정 순서(위 열거 순) · 조합 id |

### 5-9. T8 neighbors — 범용 이웃 탐색

| 칸 | 값 |
|---|---|
| 입력 | `id: 정본 id` · `edge_kinds?: [kind]` · `direction?: out\|in\|both = both` · `depth?: int = 1` · `limit?: int = 50` · `include_conditional?: false` · `include_derived?: true`(펼친 행 포함) |
| 한도 | `depth ≤ 2` · `limit ≤ 50`(기본 50) · 넘으면 자르고 `truncated: true`(10-30 O-1 결정 = D-15 추천). 값은 설정(`GOLD_NEIGHBORS_MAX_DEPTH=2` · `GOLD_NEIGHBORS_MAX_LIMIT=50`) · 상한 넘는 요청은 4xx |
| 출력 | `nodes[]` · `edges[]`(표시 · 앱 값 포함) · `truncated: bool` · `counts_by_kind{}`(자르기 전 셈) |
| 안전 | 이웃에 시술이 나오면 안전 묶음 요약 동봉(G13) · `intent?` · `sections?`(§5-0 공통 — 이웃 시술 노드에 적용). **v3.2**: 이웃 시술 노드에 동봉 · 기본 묶음 원문을 붙이지 않는다(A1-1 — 이웃은 id · 이름 · 셈 · G13 요약) · 요청 `sections` 는 **요청 노드 `id` 자체**에만 · Jev 걸음은 §5-16 T10 · T11 로(T8 은 범용 유지) |

### 5-10. T9 vocab

| 칸 | 값 |
|---|---|
| 입력 | `kinds?: [concern, site, purpose, check_condition, technique, family, intent, menu]` |
| 출력 | 고민 트리 · 부위 트리 · 목적 · 확인 조건 · 기법 트리 · 계열 · 의도 12 · 메뉴 이름(G18 라벨 8 — `kind == 고민 패키지(사이트 「추천 패키지」)` 의 `anchor.source_label`) · 도구 입력 enum(sections · sub_condition 키) — Jev 슬롯 선택지(10-26) |

### 5-11. 응답 크기 · 속도 장치(D-14 · S1~S7)

| 장치 | 규칙 |
|---|---|
| slim 기본 | 카드 기본 slim · 원문은 sections · full 요청 때만 |
| 관계는 쌍에서만 | 카드 · recommend 에 관계 목록 없음 → pair_check |
| 홉 제한 | 정해 둔 경로(P-01~P-11)는 고정 홉 · neighbors 만 depth · limit · truncated |
| 빌드 때 펼침 | 요청 때 규칙 계산 없음 — 메모리 dict 조회만 |
| 근거 인용 | fact id + 원천(evidence_source) |
| 표시 전달 | 표시 12 를 행마다 그대로 + must_show_flags |
| **원문은 요청 자리에만(v3.2)** | §5-0-1 A1-1~A1-9 · 도구별 상한 표 · 더 받기 = `more_ids` → `sections=` · T11 expand |
| **걸음 탐색(v3.2 · v3.3)** | T10 peek(중앙 ≤ 2.5KB · section 마다 실제 expand 바이트) → Jev 가 고름 → T11 expand(고른 것만 · fact 한 줄 목록 · section 1 중앙 ≤ 2KB · 원문은 `full` · `fact_ids`) — §5-16 |


---

### 5-12. 평가용 원장 도구 3 — raw-mcp(골드 아님)

hub-evals(`reference/2026-10-30-hub-evals/README.md`)가 원장 · 골드를 같은 환경(Claude SDK 에 MCP 도구로)에서 재도록 원장을 그대로 읽는 범용 도구(10-30 「원장도 MCP 로」). **골드 그래프 · 시맨틱 사전 · resolve_rules · 실버 · 골드 규칙에 기대지 않는다.** 골드 도구 9 와 응답 꼴 · 표시 · 안전 동봉 규칙을 나누지 않는다(§5-0 은 적용 안 함).

| 칸 | 값 |
|---|---|
| 마운트 | 같은 허브 앱 `127.0.0.1:18005` 에 별도 마운트 `/procedure-hub/raw-mcp/mcp` — 골드 MCP 와 같은 전송(Streamable HTTP · stateless · JSON 응답) · 별도 MCP 서버 이름(`procedure-hub-raw`) |
| REST | 만들지 않는다(사용자 결정 「REST 출구는 선택」 — hub-evals 는 MCP 만 씀). 필요해지면 같은 코어에 `/procedure-hub/raw/*` 라우터만 더함 |
| 입력 원장 | env `PHUB_RAW_DIR`(로컬 기본값 = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26` — 예시 env 에만) · 파일 21(아래) · DB 안 씀 · 서버 시작 때 메모리에 읽음 |
| 해시 가드 | 시작 때 파일 21 의 sha256 앞 16자를 `raw-manifest.json`(코드 레포 `backend/` · 파일 이름 · 바이트 · sha16 21행 · 비밀값 없음)과 대조 — 파일이 빠지거나 더 있거나 해시가 다르면 원장 MCP 를 마운트하지 않고 헬스에 사유를 냄(골드 도구는 영향 없음). 응답 머리 `raw: {dir_manifest_sha16, files: 21}` |
| 모듈 경계 | `app/modules/raw/` — `app.modules.gold` · 시맨틱 · 실버 파일을 import · 읽기 하지 않는다. 골드 모듈도 raw 를 import 하지 않는다(시험 §6-4 가드) |
| 도구 meta(v3.2 · M-1) | `raw_list` · `raw_get` · `raw_search` 도 `meta={"anthropic/maxResultSizeChars": RAW_MCP_RESULT_MAX_CHARS}`(기본 200,000) — case1 이 case2 와 같은 전달 조건이 되게(SPEC-006 v2 §3-7 공정성) |

원장 파일 21(10-30 실물 · `phub-stg-2026-10-26/` · 합 1,252,346 바이트): anatomy-danger-zones · combo-recipes · complications · consent-checklist · contraindications · extracted · literature-evidence · market-pricing · patient-education · pih-risk · post-procedure-timeline · pre-procedure-checklist · problem-combos · problem-packages · procedure-comparison · procedure-profiles · products · synergy · taxonomy(660,497 바이트 · `modality[17]` · `problem[14]`) · treatment-optimization · treatment-sequence(`.json`)

경로 문법(세 도구 공통): `{파일 이름(.json 뺌)}` 다음에 `.{키}` 또는 `[{번호}]` 또는 `["{키}"]`(키에 `.` · `[` · 공백이 있을 때). 예 `taxonomy.problem[3]` · `extracted.M9` · `products.botulinum_toxin`. 없는 경로 = 4xx(도메인 오류 문구)

| id | 도구 | 입력 | 출력 | 규칙 |
|---|---|---|---|---|
| R1 | `raw_list` | `file?: str`(없으면 21 전부) · `depth?: int = 2`(≤ 3) | `files[]{name, bytes, sha16, structure}` — `structure` = 키 구조 트리(키 · 값 종류 object/array/string/number/bool/null · 배열 길이 · 객체 키 수) depth 까지 · 배열은 첫 원소 구조만 대표로 | 값 본문은 안 냄 |
| R2 | `raw_get` | `path: str`(필수) · `offset?: int = 0`(배열 · 객체 원소 건너뛰기) · `max_bytes?: int`(≤ 설정 상한) | `{path, type, value, bytes_total, truncated, next_offset?}` — 값은 원문 JSON 그대로 | 크기 한도 = 설정 `RAW_GET_MAX_BYTES`(기본 20,000 바이트 — 골드 카드 full 최대 18.4KB 수준). 넘으면 배열 · 객체는 원소 단위로 앞에서부터 한도까지 + `truncated: true` · `next_offset` · 문자열 하나가 넘으면 앞부분 + `truncated` |
| R3 | `raw_search` | `query: str`(필수 · 1~100자) · `files?: [str]` · `limit?: int = 20`(≤ 100) · `snippet_chars?: int = 80`(≤ 200) | `{query_norm, total, truncated, hits[]{file, path, in: "value\|key", snippet}}` | 정규화 = **공백 지우기 · 소문자만**(질의 · 원문 둘 다 · 시맨틱 정규화 · fold · 괄호 지움 · 사전 안 씀). 문자열 값과 객체 키에서 부분 일치 · 순서 = 파일 이름 순 → 문서 순(결정론) · `snippet` = 일치 앞뒤 원문 그대로(정규화 전 글자) · `total` = 자르기 전 셈 |

- LLM 없음 · 결정론(같은 원장 · 같은 입력 → 같은 출력)
- 품질 측정(§6-1)과 완료 조건에 들어가지 않는다 — hub-evals 는 골드 완성 뒤 별도(10-30)

### 5-13. 의도별 고정 동봉(v3 · B ⑤ 90 · ⑦ 20 · ④ 중 「안 부름 · 다른 쌍」)

recommend · procedure_card · resolve 뒤 경로 · pair_check · compare · check_conditions · combos · neighbors 가 돌려주는 **시술 노드(단위 시술 · 제품 · 계열)마다 1-hop 이웃을 의도에 따라 고정으로** 같이 낸다. LLM 이 고르지 않아도 붙는다(결정론 · 빌드 때 모아 둔 dict 조회 · S4). 꼴은 **요약 + id**(slim 원칙) — 원문은 상한 안의 fact 만 `facts[]` 에 싣고 나머지는 fact id 로 가리킨다(`more` 셈). 카드 안 칸 이름 `companion{…}`.

동봉 묶음(요약 꼴 · 상한은 시술 노드 하나 기준):

| id | 묶음 | 꼴(요약) | 상한 | 원문(facts) | 근거(B) |
|---|---|---|---|---|---|
| C1 | 부위 위험(site_caution) | 그 시술 부위(부위 트리 상위 · 계열 SC 의 `units_affected` 포함)에 닿는 `site_caution` 엣지 `{id, site, danger_level, key_warning: fact id, risk: fact id}` · 금기 아님 · 위험 단계 큰 순 | 3 | `spec.key_warning` 1 · `risk` 1(F-C) | ⑦ 4 · ⑤ family site_caution 1 · ① 1 · ② 2 |
| C2 | 확인 조건(checks) | 그 시술의 `requires_check` 전부(단위 수준 펼친 종류 `requires_check_unit` 1,600 · 제품 `requires_check_product` · 전역 포함 — W-1) `{condition, name, grade3, resolved_id, claims: [fact id]}` — 지금은 금기 id + 등급 셈뿐 → **주의 · 확인만 도 이름 · id 로** | 전부(이름) | 금기 · 주의 주장 원문 ≤ 4(금기 먼저) | ⑤ check_condition 25(1-hop 20 · 경로 5) |
| C3 | 금기류 관계(relations) | 그 시술에 닿는 관계(저장 `procedure_relation` 230 을 단위 시술 쌍으로 펼친 `procedure_pair` 4,687 — 단위 시술은 쌍 색인 `g.pair`/UnitSets 로 닿는 것 · W-1) 중 간격 금기 · 조합 금기 · 같은 날 불가 · 대체(택 1) `{edge, kinds, other{id, kind, name}, first, days, same_day, status, claims: [fact id]}` | 6 | 쌍 도구에서만(C9) | ④ 「안 부름」 4 · 「다른 쌍」 14 · ⑦ 1 |
| C4 | 쓰는 제품(products) | `{id, name, license_status, recommendable}`(D-6 가 뺀 목록을 의도별로 되살림) | 10 | 없음(원문은 `sections=products` · I-10) | ⑤ product 10(aftercare 4 · side_effects 4 · products 1 · 속성 1) |
| C5 | 계열(family) | `{id, name, definition: fact id}` + 계열 안전 상태 2 | 1(+ also_families) | `definition` 1(F-D) | ⑤ family 13(1-hop 4 · 경로 9) · ⑥ 1 |
| C6 | 합병증(complications) | `{id, name, severity, fact}` 전부(지금 items 와 같음 · 계열 카드 · compare · pair 에도) | 전부 | 없음(I-04 기본 묶음) | ⑤ complication 4 |
| C7 | 추천 조합(combos) | 그 시술이 구성에 든 조합 `{id, kind, name, tier, price: fact id, effect: {expectedResult, clinicalRationale, riskBenefit}: fact id}` — 추천 패키지 먼저(판단 ③) | 5 | `price` · `effect.expectedResult` ≤ 2 조합(F-D) | ⑤ combo 27 · ⑥ combo 8 |
| C8 | 패키지(packages) | `contains` 로 그 시술이 든 step6 패키지 `{id, name, kind}` · `package_evidence` fact id | 5 | 없음 | ⑤ package 2 |
| C9 | 쌍 근거(pair evidence) | 쌍마다 `claims[]{id, kind, text, flags}` **원문** · 금기류 주장 먼저 | 쌍당 4(넘으면 id + `claims_total`) | 4/쌍 | ④ 「evidence 안 요청」 8 · 「안 실림」 1 |
| C10 | 비교 멤버 원문 | 비교 조합 `members[].attrs_text` 잎 fact(F-C) — 비교 대상 시술이 멤버인 것만 `{unit, field, fact id, text}` | 멤버당 잎 전부(≤ 9) | 전부 | ⑦ 10 · ⑥ 2 · ⑤ 비교 조합 분 |
| C11 | 경과 타임라인 요약 | `{timeline id, phases[]{name, fact ids}}` — 이름만 | 1 타임라인 | 없음(`sections=timeline`) | ⑤ unit timeline 3 · 경로 1 |
| C12 | PIH 요약 | `{pih_risk, pih_rate, fitzpatrick_note: fact id, source: fact id}`(F-D 잎) · 상태 3값 | 1 | `fitzpatrick_note` 1 | ⑥ unit 9 중 7 |
| C13 | 상담 문장(not_condition) | 계열 `family_text` 「상담 · 준비 · 고지 · 조건 아닌 문장」 fact id | 5 | 5(I-09 만) | ② 1(Q001 K8-0303 · M9 checks) |
| C14 | 붙은 근거 메모(evidence refs) | F-A · F-B 로 그 시술 · 조합 · CC 에 붙은 step8_notes · CC 속성 fact id `{id, kind(meta), where}` | 5 | 원문 ≤ 2(「시너지(쌍 주장)」 먼저) | ⑧ 15 |

**v3.2 — C1′~C14′(위 표를 이렇게 바꾼다 · 원칙 = id 는 전부 · 원문은 질문 자리만 · 근거 = 2차 분류 B 186 · §8)** — **v3.3(W7-D1)**: 아래 「id 범위(전부)」 열은 **명시 `sections` · T11 expand 에서의 범위**다. 도구 **기본 응답**에서는 그 id 목록 대신 **셈**(`facts_n` · `claims_n` · `edges_n` · `refs_n` · `evidence_n`)을 낸다 — 닫힘은 (b) 추가 호출 1 로 잰다(§6-5 (i) W7-D2):

| id | v3.2 꼴 | id 범위(전부) | 원문 상한 | 닫는 B(§8 열) |
|---|---|---|---|---|
| C1′ | A1-2 — resolve 된 부위 체인 · **같은 계열** SC 만 `{id, site, danger_level, facts[]}`(기본 응답 = `facts_n`) | 엣지 ≤ 3 · **잎 fact id 전부**(spec.* · vessels[].danger · clinical_pearls · safe_injection_depth) | `key_warning` 1 | C1′ 3 |
| C2′ | A1-3 — `by_grade{등급: [조건]}` **전 등급**(I-01 포함) · `claims[]` · `edges[]`(**저장 `requires_check:{K8}:{C}` 만** · 펼친 unit 엣지는 `edges_n` · W7-D8) | 단위 `requires_check_unit` + 계열 상속(`checks_by_family`) + 전역 주장 id **전부**(기본 응답 = `claims_n`) | 질문 조건 ≤ 4 **+ 금기 앞 2**(W7-D3) | C2′ 32(→ 28 · 데이터 4 W7-D12) |
| C3′ | 그 시술(펼친 단위 포함)에 닿는 `procedure_relation` **저장 엣지 수준**(230 · 단위 쌍 아님) `{edge, kinds, other, claims[]}` 종류 무관 · 정렬 = **양끝이 입력 안인 엣지 → 금기류 → id**(v3.3 · W7-D7 — 계열 수준 관계 25~63 이라 상한 20 안에 입력 쌍이 들어오게) · 카드 칸 이름 `relations_all{edges, n, forbid_n, claims_n, global}`(W7-D13) + `global[]`(G16 전역 메모 · `scope:all#evidence#sequence_rank[*]` id ≤ 4) | 엣지 ≤ 20 · claims · reasons id 전부 | 0(쌍 원문은 T4 C9′) | C3′ 14 |
| C4′ | `{id, name, license_status, recommendable, basis: fact id}`(F-C `product_family` basis) | 10 | 0 | C4′ 1 |
| C5′ | 그대로 | 1 | definition 1 | — |
| C6′ | `{id, name, severity, facts[]}` — **잎 fact id 전부**(`CX-…` 본문 · `#prevention` · `#incidence` · `#risk_factors[i]` …) | 전부 | 0(I-04 묶음 · `sections=safety.complications`) | C6′ 4 |
| C7′ | 조합 id 전부 ≤ 8(추천 패키지 먼저) · 조합마다 `refs[]` = owner · attached fact id **전부**(price · effect.* · rationale · caveats · evidence_notes · sessions · subtitle · members[].attrs_text 잎 · F-D′ 잎) — 응답 수준 `index.combos` 에 한 번(A1-7) · 카드는 id | 8 · refs 전부 | 추천 패키지 1 조합의 price · expectedResult(T7 은 2) | C7′ 40 |
| C8′ | 그대로 + `evidence[]` fact id | 5 | 0 | — |
| C9′ | T4 쌍마다 `claims[]` + `reasons[]` id **전부** · 조건부는 `conditional` 표시 | 전부 | **2/쌍**(금기류 먼저) | C9′ 8 |
| C10′ | T6 에서만 원문(비교 대상 멤버 잎 ≤ 6/멤버) · 다른 도구에선 C7′ refs 로 **id** | — | 6/멤버 | (C7′ 안) |
| C11′ | W5-D4 `{id, name, phases[]{name, facts_n}}` · `sections=timeline` 으로 id | 1 | 0 | — |
| C12′ | 그대로 · 계열 · 제품 펼침 때 단위마다(`by_unit`) pih 잎 id | 단위 ≤ 4 | note 1 | (F-F Q150) |
| C13′ | id 전부(≤ 5) · 원문은 I-09 만 2 | 5 | 2 | — |
| C14′ | 단위 시술은 그대로 · **계열 · 제품 카드 · 펼침 응답은 그 계열(펼친 단위 전부)에 붙은 step8 메모 · CC 속성 id 전부**(상한 10 · 「시너지」 먼저) | 10 | 1 | C14′ 11 |

의도 × 동봉(I-01~I-12):

| 의도 | 도구 | 동봉 묶음(고정 · 순서대로) | 근거 B 건수(⑤ · ⑦ · ④ · ⑥) |
|---|---|---|---|
| I-01 고민 → 추천 | T2 | 카드마다 C1 · C2 · C3 · C4(상한 5) · C7 · C14 | ⑤ 9 · ⑦ 3 · ④ 1 |
| I-02 시술 설명 | T3 | C5 · C4 · C6 · C2 · C11 | ⑤ 7 |
| I-03 주의 · 사후관리 | T3 | C11 · C1 · C2 · C4(aftercare 원문은 §5-14) | ⑤ 8 |
| I-04 부작용 · 합병증 | T3 | C6 · C1 · C12 · C4 · C2 | ⑤ 13(그중 combo 1 · unit market 1 은 닫지 않음 — §6-5 표) |
| I-05 회복 · 효과 기간 | T3 | C11 · C2 · C12 · C7 · C14 | ⑤ 14 |
| I-06 비교 | T6 | 비교 시술마다 C5 · C12 · C6 · C2 · **C7 · C11 · C14**(v3.1 — ⑤/⑥ combo 8 · Q106 timeline 2 · Q198 ⑧ 2) + 응답에 C10 · 쌍마다 C3(종류 무관 · `relations[]`) | ⑤ 12 · ⑥ 10 · ④ 2 · ⑧ 2 |
| I-07 같이 · 순서 · 간격 | T4 | 쌍마다 C9 · 입력 1개면 C3(`relations[]`) · 시술마다 C2(C-PRIOR 포함) · C1 · C7 · **C12**(v3.1 · Q201) | ④ 21 · ⑤ 11 · ⑥ 1 |
| I-08 이전 시술 뒤 가능? | T4 | I-07 과 같음 + `prior_checks` | ④ 1 · ⑤ 1 · ① 1 |
| I-09 확인 조건 | T5 | C2(원문 상한 4) · C13 · C1 · C6 · **C12**(v3.1 · Q150) | ⑤ 11 · ⑦ 4 · ⑥ 1 |
| I-10 용량 · 회차 · 제품 | T3 | C4(상한 10 · `5_spec` 포함) · C7 · C12 · C14 | ⑤ 2 · ⑥ 1 |
| I-11 추천 조합 | T7 | 조합마다 C7 속성(price · effect) · C14 · C8 · 구성 시술마다 C3 · **C2**(v3.1 · Q025 C-NMJ) | ⑤ 2 · ⑥ 3 · ④ 2 |
| I-12 가격 | — | 허브 도구 없음(연결 층) — 동봉 없음 · §7 V-1 | — |
| (의도 없음 · T1 · T8 · T9) | — | G13 안전 요약만(지금과 같음) | — |

- **계열 펼침 상한**(계열 · 제품 id 가 와서 단위 시술로 펼칠 때 · 동봉 · 섹션 `by_unit` 공통): **v3.2** pair_check 12쌍 · compare 8 단위(D-9 그대로) · check_conditions 8 단위 · 계열 카드 `by_unit` 4 단위 — 넘으면 `truncated` · `units_total` · 나머지는 `units_more[]` id 목록. 값은 설정(`GOLD_EXPAND_MAX_UNITS=8` · `GOLD_CARD_BY_UNIT_MAX=4` · `PAIR_EXPAND_MAX=12`)
- **크기 상한(응답 전체 · §6-5 로 잼)**: **v3.2 — §5-0-1 A1-9 표(숫자)** 로 바뀜. 「현 ×2」(v3.1) · 「2.5×」(코디 10-31 ③)는 폐기. 넘으면 동봉 · section 상한 값을 줄인다 — 동봉 종류 · section 을 빼지 않는다
- 동봉은 **의도의 정의**다(gold-research 의도 12 · 경로 P-01~P-11 의 「→ 단위 시술마다 G13 안전 묶음 · 쓰는 제품 · 추천 조합 앵커」를 의도별로 고정한 것). 새 의도를 더하려면 이 표에 행을 더한다 — 코드 상수 `INTENTS` 와 1:1(시험)

### 5-14. 의도 → 섹션 기본 묶음(v3 · B ① 53 · ② 16)

허브가 `intent` 를 받으면(없으면 도구 기본 의도 — §5-0) 아래 section 을 **기본으로** 붙인다. `sections=` 명시가 오면 합집합 · `none` 이면 끔. section 이름은 §4-3. 적용 대상 = 응답에 나온 시술 노드 전부(§5-0 「시술 노드 단위」 · F-E ③).

| 의도 | 기본 section | 근거(B ① + ② 의 빠진 section · 건) |
|---|---|---|
| I-01 | (없음 — 카드 slim + §5-13 동봉) · `site_caution` 은 C1 으로 | ① site_caution 1 · ② checks 1 · overview 1 |
| I-02 | `overview` · `method` · `ops` | ① overview 3 · ops 1 · ② overview 1 · ops 2 |
| I-03 | `aftercare` · `recovery` · `timeline` · `emergency` · `disclosure` · `overview`(v3.1) | ① aftercare 3 · disclosure 2 · overview 1 · ② safety.pih 1 · timeline 1 |
| I-04 | `safety.side_effects` · `safety.complications` · `safety.pih` · `emergency` · `disclosure` · `overview` · `timeline`(v3.1) | ① disclosure 5 · overview 5 · emergency 2 · timeline 1 · side_effects 1 · ② site_caution 1 · emergency 1 (management 는 A 그룹 · §7 V-4) |
| I-05 | `recovery` · `timeline` · `aftercare` · `overview` · `disclosure` · `ops`(v3.1) | ① aftercare 3 · recovery 3 · overview 1 · disclosure 1 · timeline 1 · ops 1 · ② ops 1 |
| I-06 | compare 차이 필드 = `overview` · `method` · `recovery` · `ops` · `dose`(§5-7 rows) · 비교 시술마다 `safety.pih` · `checks` · `disclosure`(v3.1) · `evidence` 는 조합(C14) 범위만 — 단위 시술 evidence 아님 | ① recovery 2 · overview 1 · checks 1 · disclosure 1 · method 1 · pih 1 · ② overview 6 · method 1 · ⑧ 2 |
| I-07 · I-08 | 쌍 `evidence`(C9 원문) · 시술 `checks`(C-PRIOR) · I-08 은 `safety.side_effects`(v3.1 · Q020) | ① checks 1 · side_effects 1 · ② site_caution 1(C1) · ④ evidence 9 |
| I-09 | `checks` · `site_caution` · `aftercare` · `overview`(v3.1 — 확인 조건 노드 없는 질문의 `overview` · `ops` 경로 §6-1 과 겹침) | ① aftercare 2 · overview 2 · ⑤ checks 25 · ⑦ basis→overview 1 |
| I-10 | `dose` · `products` · `market` · `overview` · `disclosure`(v3.1) | ① overview 2 · disclosure 2 · market 1 |
| I-11 | `products` · `market` · 조합 `evidence`(F-A · F-D) | ⑥ 3 · ⑧ 1 |
| I-12 | — | — |

- **v3.2(§5-14′ · 묶음 밖 id 노출 · B 기본 묶음 밖 33 + Jev 안 고름 12 + 상위 4 밖 5 = §8 §5-14′ 29행)**: 단일 노드 도구(T3 · T4 · T5 · T6 · T7 · T8)의 요청 노드마다 `sections_index` 를 **17 section 중 0 아닌 것 전부**에 낸다(**v3.3 · W7-D1: 꼴 = `{section: {n, units_n}}` 셈** — v3.2 의 `ids[:4]` 는 실물에 없음 · 29행 중 28 이 (a) 9 + (b) 19 로 닫힘 · 못 닫음 1 Q198 c3)(묶음 안 section 은 `sections[s]` 에 원문 + `more_ids` 가 있으므로 색인엔 `n` 만) — disclosure(필수 고지 7/계열) · checks(상담 문장) · market · safety.pih · recovery · timeline 이 의도와 어긋난 호출(I-02 카드에 disclosure 질문 등)에서 id 로 닿는다. 묶음 자체는 v3.1 표 그대로(보강 없음 — 보강은 원문을 키움). T2 recommend 는 `n` 만(카드 10장). 의도 밖 명시 `sections` 요청은 A1-4(id ≤ 4 · 원문 0 · V-9)
- 기본 묶음이 커지면 크기 상한(§5-13)이 먼저다 — section 을 빼지 않고 **section 안 fact 수 상한**(`GOLD_SECTION_FACTS_MAX=4` · v3.2 A1-5 · 넘으면 id 만 + `more`)으로 줄인다. 계열 수준 원문(환자 설명 가이드 등)은 응답에 한 번만(같은 계열 카드가 여럿이어도 facts 는 id 로 중복 제거 — 지금 envelope 와 같음)
- Jev · Claude 가 고른 `sections` 는 그대로 더해진다(합집합) — 「Jev 가 상위 4 밖으로 자름」(case3 8건) · 「noul < 0.5 로 안 고름」(10건)은 **18건 모두** 그 의도의 기본 묶음 안에 있다(v3.1 — Q020 · Q040 · Q042 · Q058 · Q098 · Q104 · Q170 이 위 표 보강으로 들어옴). 앱 쪽 규칙(상위 4 · 0.5)은 SPEC-006 몫 · 여기서 바꾸지 않는다(§7 V-5)

### 5-15. full 전용 속성 → slim 승격(v3 · B ⑥ 18)

건수 기준(fail-triage ⑥ + ⑤ 의 같은 칸)으로 정한다 — **5건 이상이면 slim 에 요약 + fact id · 그 미만은 section(원문)으로만**(문턱 5 는 작성자 기준 · 결정표에 없음 → §7 V-6 · W-3).

| 속성(실물 칸) | 건 | 결정 | 어디로 |
|---|---|---|---|
| 조합 `effect{expectedResult, clinicalRationale, riskBenefit}` · `price` · `evidence_notes` · `caveats` · `rationale` · `sessions` · `maintenance` | ⑥ 8 + ⑤ 27 = 35 | **slim 승격**: 짧은 조합 카드(T7 · C7)에 `price` 원문 · `effect.*` fact id(+ expectedResult 원문 ≤ 2 조합) · 나머지 fact id | §5-8 · C7 · F-D |
| 단위 시술 `pih[]{fitzpatrick_note, source, pih_rate, pih_risk, prevention}` | ⑥ 7(+ ② 1) | **slim 승격**: 안전 요약 `pih` 칸을 셈 → `{pih_risk, pih_rate, note: fact id}` 로(C12) · 원문은 `safety.pih` | §5-4 · C12 · F-D |
| 비교 조합 `members[].attrs_text` · `anchor.subtitle` | ⑥ 2 + ⑦ 11 = 13 · 2차 B 16 | **compare 응답에서만 원문**(C10′) — 카드 slim 에는 원문 안 올림(비교 맥락 밖이라) · **v3.2: id 는 어디서나 C7′ refs 로**(v3.1 「닫지 않는 행」 10 이 id 로 닫힘) | §5-7 · F-C · C7′ |
| 계열 `definition`(계열 overview 대용) | ⑥ 1 + ⑤ family overview 4 | 이미 짧은 계열 카드에 있음 → **C5 로 다른 도구 응답에도**(compare · pair · recommend family_only) | C5 · F-D |
| 단위 시술 `sources[].detail` · `schedule` · `members text` | ⑥ 2 | section(`overview`)으로만 | F-D |
| 조합 `sales_copy` | ⑤ 1(Q238) | 바꾸지 않음 — `include_sales_copy` 때만(G12 영업 문구) | — |

### 5-16. T10 peek · T11 expand — Jev 재귀 탐색의 허브 쪽(v3.2 · 사용자 결정 11-01 · v3.3 expand 꼴)

사용자 결정(`phub-recommend-jev-walk-addendum.md`): case3(Jev 슬롯 1회 → 허브 경로 1회 → 의도 묶음 · 동봉 전부 → Claude)를 **Jev 재귀 탐색으로 바꾼다(교체)**. 허브가 「뭐가 필요할지 몰라 다 주는」 구조가 46KB · C 10% 의 원인. 허브 몫 = **peek · expand 응답 꼴과 끝 조건**(결정론 · LLM 없음) · 앱 몫(SPEC-006 v2) = 걸음 상한(기본 4) · 바이트 예산(기본 20KB) · 「충분」 신뢰도 문턱 · 못 찾으면 되돌아가기(의도 기본 묶음 1회 = 지금 case3) · 걸음마다 기록 · 첫 글자 영향 · Jev 호출 수 · 시간.

```text
질문 → Jev(의도 · 시작 노드 후보: T1 resolve)
  → T10 peek(id): slim 노드 + 이웃 목록(종류별 셈 · 앞 4 id · 한 줄 라벨 · 이웃 fact 수) + 섹션 목록(이름 · fact 수 · 실제 expand 바이트) + G13 안전 요약 ≤ 2.5KB(중앙)
  → Jev Choice: 펼칠 것(섹션 · 이웃 id ≤ 255) · 「충분한가」
  → T11 expand(id, sections | neighbors | neighbor_kinds): 고른 것만 — fact 한 줄 목록(v3.3) · 원문은 full · fact_ids
  → … 걸음 상한 N · 바이트 예산 B 안에서 반복(앱)
→ Claude: 모은 fact(id · 원문) + claude_contract(응답마다 · 앱이 합침)
```

**어디에 두나(추천 기본값 · V-8)**: 같은 코어 위의 **새 도구 2(T10 · T11)** — REST `GET /procedure-hub/gold/nodes/{id}/peek` · `POST /procedure-hub/gold/nodes/{id}/expand` · MCP `peek` · `expand`. 모드(T3 `mode=peek` · T8 `mode=expand`)가 아닌 이유: 응답 꼴이 다르고(의도 · 동봉 없음 · 시술 노드 아닌 노드도 받음) · Jev 도구 설명이 짧아야 하며 · 기존 도구 계약(§6-4 공개 계약 시험)을 안 건드린다. 실물 보고 모드로 바꿔도 아래 응답 꼴은 같다.

**v3.3 — expand 를 걷기용으로(11-01 사용자 승인 「발주하자」 · `phub-recommend-walk-fix-context.md`)**. rerun-v4 걸음 기록(`runs.jsonl` b202611011148-c6ed3a · 148 걸음 판)에서 expand 한 호출(section 1)이 중앙 7,987B · 최대 60,732 라 예산 20KB 의 첫 걸음에서 104/148 이 멈췄고, peek `sections[].bytes`(원문 글자 합)는 실제의 중앙 1/10 이라 Jev · 앱이 미리 고를 수 없었다. 옛 꼴의 바이트 구성(전 6,140 (노드, section) 합 · `spec005-v33-measure.json` a): `facts[]` 39% · `sections[s].facts` id 목록 34% · `claude_contract`(id 3중 + 규칙 문장 411B) 21% · 나머지 6% — **같은 fact id 가 다섯 번**, 원문 행마다 `source.meta`. fact 원문 자체는 짧다(공백 접은 글자 수 중앙 11자 · p95 92 · 40자 이하 86.1% · 60자 이하 90.8% · 80자 이하 93.4% · 최대 330 — 14,898 fact · `spec005-v33-measure.json e_other.fact_chars`). 그래서 기본 꼴을 **fact 한 줄 목록**으로 바꾸고, 원문 전체는 고른 것만 받는다.

| 칸 | T10 peek | T11 expand(v3.3) |
|---|---|---|
| 입력 | `id: 정본 id`(13 종류 전부 · 시술 노드 아니어도 됨) · `include_conditional?: false` · `intent?`(**받되 무시** — M-3 · 기록용 · `intent_used: null`) | `id` · `sections?: [section 이름]` · `neighbors?: [정본 id ≤ GOLD_EXPAND_PICK_MAX(255)]`(peek 가 낸 이웃만 — 아니면 4xx) · `neighbor_kinds?: [edge kind]`(그 종류 이웃 **전부**) · `fact_ids?: [id ≤ GOLD_EXPAND_FACT_IDS_MAX(64)]`(**그 노드의 section fact ∪ 계열 · 제품이면 펼친 단위 시술의 section fact**(`_node_fact_ids`) — peek `sections[].n_facts` 는 앞쪽만 센다(단위 수준 section 은 peek 에 없음) · 그 밖 id 는 4xx) · **`full?: false`**(true 면 요청 section 의 줄을 원문 행으로) · **`page?: 1`**(section 마다 1쪽 = `GOLD_EXPAND_SECTION_MAX`(12)줄 · 1부터) · `include_conditional?` · `intent?`(받되 무시 M-3) |
| 출력 | `node{id, kind, name, key?, flags, gate_status, default_out}` · `safety{}`(시술 노드면 G13 `compact_safety` 그대로) · `neighbors_by_kind{edge kind: {n, direction, items[:GOLD_PEEK_ITEMS_PER_KIND(4 · W7-D4)]{id, kind, name(≤ GOLD_PEEK_NAME_CHARS(20)자), label, **n_facts**}}}` — `label` = 엣지 종류 · 값 요약 한 줄(관계면 kinds · first · days · same_day · 확인 조건이면 grade3 · 부위 위험이면 danger) · **`n_facts`(v3.3) = 그 이웃 노드의 17 section fact 수 합**(결정론 셈 · 「답이 많이 사는 곳」 같은 추측 표시는 내지 않음 — 종류별 `n` · 앞 4 라벨 · 이웃마다 `n_facts` 만) · 이웃 꼴은 이 `by_kind` 하나(SPEC-006 v2 §3-4-2 평면 목록은 아래 대응표) · `sections[]{name, n_facts, bytes}`(0 은 생략 · **`bytes`(v3.3) = 그 section 하나로 부른 T11 기본 꼴 1쪽 응답의 REST 본문 바이트**(봉투 · `request{id, sections}` 포함 · `intent` 없이 · §5-0-1 셈 규칙) — 원문 글자 합 아님) · `priority_hint[]`(규칙 — 부위 · 금기 이웃 종류 이름) · `global{n, ids[:4]}` · `build` · `claude_contract`(`allowed_fact_ids` = [] · `rule` 문장 — 걸음의 규칙 문장은 여기 한 번) | **기본 꼴(`full` 없음)**: `build{build_hash}` · `request`(null 아닌 입력만) · `intent_used: null` · `node{id, kind, name}` · **`facts[]{id, line, section, owner?, cut?, flags?, gap?}`** · `more{section: n}`(그 쪽 뒤에 남은 줄 수 · 0 생략) · 계열 · 제품 노드의 단위 시술 수준 section 은 `by_unit{unit id: n}`(≤ GOLD_CARD_BY_UNIT_MAX(4) · 나머지 `units_more_n` · 원문 · id 없음 — 단위 id 로 다시 expand) · `neighbors[]{id, kind, name, edge, kind_edge, kinds?, value?, safety?, sections_n}`(v3.2 꼴 그대로 · ≤ GOLD_EXPAND_NEIGHBORS_MAX(20) · 넘으면 `neighbors_truncated` · `neighbors_more_ids`) · `claude_contract{allowed: "facts_uncut", must_show_flags}`. **`full=true`**: 같은 줄 자리에 `facts[]{id, text, section, owner?, flags?, gap?, source{file, path}}`(원문 · `meta` 없음) · 쪽 · `more` 같음. **`fact_ids`**: 그 id 들을 `full` 행 꼴로 `facts[]` 끝에 붙임(요청 순서) · 같은 id 가 요청 section 의 줄에도 있으면 **줄은 빼고 원문 행 하나만**(fact id 는 응답에 한 번) |
| 줄(line) 규칙(결정론) | — | `line` = fact `text` 의 공백 연속을 한 칸으로 접은 문자열 · 길이(코드 포인트) ≤ `GOLD_EXPAND_LINE_CHARS`(**40**)이면 그대로(= 원문 전체 · `cut` 없음) · 넘으면 앞 39자 + 「…」 · `cut: true`. 요약 · 다시 쓰기 · LLM 없음. `owner` = fact 의 `owner_id` 가 노드 · 엣지 · `scope:` id 면 그 값 · 아니면 `attached_to[0]` — **요청 `id` 와 같으면 생략**. `flags` 는 비지 않을 때만 · `gap: true` 는 `state == 정보 없음(gap)` 일 때만. 줄 순서 = 요청 section 순 → section 안은 peek `n_facts` 와 같은 순서(`warm_sections` · A1-5 정렬) |
| 인용 계약 | — | `allowed: "facts_uncut"` = 이 응답 `facts[]` 중 **`cut` 없는 줄**(줄 = 원문 전체)과 `full` · `fact_ids` 로 받은 원문 행만 인용 가능 · `cut` 줄은 `fact_ids` 로 원문을 받은 뒤 인용. `priority` · `use_first` 는 내지 않는다(우선순위 = `facts[]` 순서 · v3.2 의 id 3중 제거). 앱이 걸음의 계약을 합칠 때 규칙 문장은 peek 의 `claude_contract.rule` 을 쓴다 |
| 상한 | **중앙 ≤ 2,500 · p95 ≤ 8,000**(W7-D4 · §5-0-1 표) — 이웃 종류 ≤ 21 × 앞 4 · 이름 20자 · 실물 단위 시술 1-hop **총** 중앙 94 엣지(p95 185 · 최대 275 · 단위 시술 162 전부) · 종류별은 그 종류 엣지가 1개 이상인 단위 시술만의 중앙 = procedure_pair 69(n 150) · requires_check_unit 12(136) · has_statement_unit 11(113) · product_unit 11(107) · combo_component 7(76)라 **전부 나열 금지** · 측정 1,071 노드 2,257 / 7,171(`n_facts` 포함 · v3.2 꼴 같은 기준 2,183 / 6,788) · 걸음이 연 peek 311 은 3,054 / 8,926(보고) | **기본 꼴 section 1: 중앙 ≤ 2,000 · p95 ≤ 5,000** · `full=true` section 1: 중앙 ≤ 4,000 · p95 ≤ 8,000(§5-0-1 표 · 측정 1,902 / 2,710 · 2,982 / 4,256) · 이웃 20 |
| 결정론 | 이웃 순서 = 종류 고정 순 — 설정 `GOLD_PEEK_KIND_ORDER`(기본 `procedure_relation` → `requires_check` → `site_caution` → `has_complication` → `combo_component` → `uses_product` · `product_unit` → `contains` → `treats` → `concern_avoid` → `has_statement` → 나머지 kind 이름 순 · 펼친 종류는 저장 종류 이름 뒤에) · 종류 안은 금기류 · 등급 · id 순 · `bytes` 는 같은 빌드 · 같은 설정이면 같은 값 | 요청 순서 그대로 · 줄은 위 규칙 · 같은 입력 같은 바이트 |
| 안 하는 것 | 동봉(C1~C14) · 의도 묶음 — **없음**(Jev 가 고른다 · `intent?` 는 받되 무시 M-3) · 「답이 많은 곳」 추측 표시 없음 · LLM 없음 · 노드 밖 추론 없음 | 같음 · 요청 안 한 이웃 · section 은 0 · 요약문 생성 없음 |
| 되돌아가기 | — | 앱이 「못 찾음」이면 기존 경로(T2~T7 + `intent`)를 1회 — 허브 변경 없음(SPEC-006) |

**SPEC-006 v2 §3-4-2 「앱이 읽는 최소 칸」 대응(검수 F-1 · 계약은 이 표가 정본 · 006 은 따름 · v3.3 에서 expand 줄이 바뀜 → WORK-009 앱이 맞춤)**:

| 006 이 읽는 칸 | 005 응답 칸 |
|---|---|
| peek `neighbors[]{id, kind, edge, label}` | `neighbors_by_kind[edge].items[]{id, kind, label, n_facts}` (`edge` = by_kind 키 · 평면 목록 = 종류 순서대로 items 이어 붙인 것 · `n` 이 items 보다 크면 그 종류는 `expand(neighbor_kinds=[edge])` 로 전부) |
| peek `sections[]{name, n_facts, bytes}` | 같음 — **`bytes` = 실제 expand 기본 꼴 바이트**(v3.3 · 예산 셈에 그대로 씀) |
| peek slim 카드 · 안전 요약 | `node{}` · `safety{}` |
| expand `facts[]{id, text, section}` | **v3.3**: 기본 꼴은 `facts[]{id, line, section, owner?, cut?}` — `cut` 없는 줄의 `line` 이 곧 원문 · `cut` 줄 원문은 `expand(id, fact_ids=[…])` 또는 `full=true` 의 `text` · 남은 줄은 `more{section: n}` → `page=2` |
| expand 이웃의 slim 카드 | `neighbors[]{id, kind, name, edge, value?, safety?, sections_n}` |
| expand `claude_contract` | **v3.3**: `{allowed: "facts_uncut", must_show_flags}` — `priority` · `use_first` 없음(줄 순서가 우선순위) · 규칙 문장은 peek 의 것 |
| `peek(node, intent?)` · `expand(…, intent?)` | `intent?` 받되 무시(M-3) |

- 고정 숫자는 전부 설정 이름이 있다(검수 W-6): `GOLD_PEEK_ITEMS_PER_KIND=4`(W7-D4) · `GOLD_PEEK_NAME_CHARS=20` · `GOLD_PEEK_KIND_ORDER` · `GOLD_EXPAND_PICK_MAX=255`(Jev Choice 상한과 같음) · `GOLD_EXPAND_FACT_IDS_MAX=64` · `GOLD_EXPAND_SECTION_MAX=12`(v3.3 = 1쪽 줄 수) · **`GOLD_EXPAND_LINE_CHARS=40`(v3.3)** · `GOLD_EXPAND_NEIGHBORS_MAX=20` · `GOLD_CARD_BY_UNIT_MAX=4`. 값은 이 판에서 측정으로 정함(V-13 닫음 · 근거 아래)
- **값 근거(`spec005-v33-measure.json` a grid · 전 6,140 (노드, section) · 중앙 / p95)**: 줄 40자 · 1쪽 12줄 · owner 생략 · 계약 규칙형 = **1,902 / 2,710** · 12줄 · id 목록형 계약(`allowed_fact_ids` 나열) = 2,203 / 3,579 · 12줄 · owner 늘 = 1,935 / 2,753 · 줄 60자 = 1,930 / 2,830 · 줄 80자 = 1,940 / 2,891 · 8줄 = 1,439 / 2,056. 12줄을 고른 이유: v3.2 `GOLD_EXPAND_SECTION_MAX=12` 와 같은 손잡이 · section fact 수 중앙 11(p95 47 · 최대 328)이라 중앙 section 은 1쪽에 다 들어옴 · 8줄이면 2쪽이 필요한 section 이 2,752 → 3,654(/6,140 · 44.8% → 59.5% · `e_other.sections_over_k` · `sections_over_8`)로 늘고 중앙 이득은 ≈ 460B. section fact 수 = `e_other.facts_per_section`. 40자를 고른 이유: fact 기준 86.1% 가 줄 = 원문(cut 13.9%)이고 60 · 80자로 늘려도 중앙 +28 · +38B · cut 은 9.2% · 6.6% 로 줄 뿐. **줄 기준 cut 비율**(긴 fact 가 걸음이 펼치는 section 에 몰림)은 더 높다 — 6,140 쌍 1쪽 줄 28.5%(`e_other.pairs_page1_cut_line_ratio`) · rerun-v4 걸음 호출 476 재생 줄 3,842 중 1,208 = 31.4%(`b_v4_calls.cut_line_ratio`) · 걸음 재생 판마다 받은 서로 다른 fact 중 37.7%(`d_walk.new_replay.cut_line_ratio`) — cut 줄 원문 받기는 V-15
- 측정은 계열 · 제품의 단위 시술 수준 section `by_unit{unit: n}` 칸(≤ 4 줄 · 단위 id + 셈)을 넣지 않았다 — 그 section 은 peek `sections[]` 에 안 나오고(계열 자신의 fact 0) 걸음 기록 476 호출 중 바이트 차는 이 칸 크기(≈ 40B/단위)뿐
- `peek` 의 `sections[].bytes` 는 메모리 적재 때 노드 × section 마다 **실제로 T11 기본 꼴을 만들어 바이트를 잰다**(W7-D5 와 같은 자리 · 요청 때 계산 없음 · 측정 0.1s / 6,140 쌍). 공식으로 더하지 않는다(봉투 · 이스케이프 차가 생김) — 시험 = 전 노드 × section 에서 `peek.sections[s].bytes == len(expand(id, sections=[s]) REST 본문)` 차 0 · 호출 쪽이 `intent` 를 넘기면 `request` 에 그 값이 실려 ≈ 17B 커진다(`"intent":"I-01"`) — 앱 예산 셈과 맞추는 건 V-17
- 걸음 · 예산 · 신뢰도 · 기록(`walk[]{step, tool, id, chosen, jev_confidence, bytes, ms}`) · `cut` 줄 원문 받기(받되 예산 포함 · V-15 닫힘) · 걸음은 1쪽만(V-18 닫힘)은 앱 trace · 정책(SPEC-006 v2.2 · WORK-009) — 허브는 응답 머리 `build` · 바이트만
- 끝 조건 = §6-5 (v) · §6-6 걸음 도달 측정 · **§6-7(v3.3)**

---

## 6. 품질 · E2E

### 6-1. 골드 위 품질 측정(완료 조건)

- 정답 세트 = `quality-eval-set.json`(문항 111 · 의도 11 · 슬롯 · 정답 · 채점 식) **그대로**. 문항 · 정답 · 채점 식을 고치지 않는다
- 측정 = 코드 레포 어댑터 `scripts/gold_quality_eval.py`(D-3 · `$W/quality-eval.py` 는 읽기만 — 채점 식을 exec 로 빌림) `--gold <base_url>|inprocess`: M1(질문 세트) · M2(말 → 노드)는 **도구 호출**로 답을 얻고, M3(엣지 표본) · M4(원천 안전 원문)는 **발행된 골드 빌드 내용**(`gold-export.json` — 노드 · 엣지 · facts)에서 잰다. 실버 직접 읽기 경로(지금 판)는 그대로 둔다(대조용). **v3**: 어댑터는 문항 의도를 `intent` 로 넘긴다(기본 묶음 · 동봉이 붙은 응답으로 채점 — 회귀 0 확인)
- 의도 → 도구: I-01 → T1 + T2(`cc` 슬롯을 문항 슬롯 `cc` 로 · **T1 결과 중 `candidates` 의 concern · site 만 쓴다 — `menu_candidates` 는 I-11 T7 만**) · I-02 · I-03 · I-04 · I-05 · I-10 → T1 + T3 · I-06 → T6(**필수** · 계열 · 제품도 받음) · I-07 · I-08 → T4(**필수** · 시술이 하나만 잡혀도 부름 — 「관계 목록」 모드 §5-5 · I-07 자기 쌍 문항은 같은 id 두 번 — 예 Q091) · I-09 → T1 + T5(계열 · 제품 id 는 펼침 §5-6) · 확인 조건 노드가 안 잡히는 문항(예 Q101 「통증 민감」 — 원문은 `family_text.M9` 환자 설명 가이드 `pain_level`)은 T3 `sections=overview,ops` 로 · I-11 → T1 + T7 · M2 → T1. 모든 호출에 `intent`(v3)
- I-11 채점은 T7 의 `combos[]`(판단 ③ 「추천 패키지」 먼저 묶음)로 — `reference[]` 는 채점에 안 넣는다(판단 ③ 이 정한 기본 응답 범위가 정답 범위). I-11 경로: 질의 말(문항 `concern_text`)이 라벨이면 T1 `menu_candidates` 의 menu 후보로 T7 `menu`(판단 ② · G18) · 아니면 고민 후보로 T7 `concern`. 실물 셈(이 스펙 작성 때 실버로): 라벨 경로 + 추천 패키지만 채점이면 Q106~Q111 6문항 계열 집합이 정답과 같음
- 목표(10-30 사용자 승인 · 계산 밖 = 의료진 질문 5문항 Q042 · Q075 · Q083 · Q084 · Q102):

| 지표 | 목표 | 지금(실버 · CC 슬롯 판) |
|---|---|---|
| 질문 세트 재현율(전체) | ≥ 0.95 | 0.991 |
| 질문 세트 정밀도(전체) | ≥ 0.95 | 0.984 |
| I-01 재현율 · 정밀도 | ≥ 0.95 · ≥ 0.95 | 1.0 · 1.0 |
| 문항 안전 누락 · 원천 안전 원문 누락(M4) | 0 · 0 | 0 · 0 |
| 말 → 노드 찾기 | ≥ 97% | 98.4% |
| 엣지 표본 오류율 | ≤ 1% | 0.5% |

- **완료 조건**: 골드 모드 6/6 **그리고** 지금 틀린 4문항 Q106 · Q108 · Q109 · Q110 이 「맞음」. 나머지 문항은 실버 판에서 맞던 것이 골드 판에서 틀리면 안 됨(문항별 대조표를 리포트에)
- 리포트 = `quality-report-gold.json` · `.md`(실버 판 리포트는 덮지 않음) · 머리에 빌드 해시 · 입력 해시 · 서버 주소 · 시드
- 결정론: 같은 빌드 · 같은 서버로 두 번 → 리포트 바이트 같음(시간 칸은 §6-3 속도 리포트로 분리)

### 6-2. 실물 호출

- 로컬 서버(`127.0.0.1:18005`) 기동 상태에서 REST 9 도구 각 1회 이상 · MCP 9 tool 각 1회 이상 실제 호출(같은 입력이면 REST 와 MCP 응답 JSON 이 같음 — 머리 `build` 칸 포함)
- 샘플 흐름(gold-research §1 의 3~10단계)을 실제 도구로 한 번 따라간 기록: 이마 주름 → 팔자 → 턱선 처짐 → 소프웨이브 카드(method · aftercare) → 팔자 필러 dose · products → 조합 A 쌍 확인. 원천에 없는 샘플 값(「2주 사우나」 · 볼루마 품목 · 「Sofwave」 단독)은 허브 응답에 안 나와야 하고 §3-6 보강 후보에 있어야 한다
- 원장 MCP(§5-12): `raw_list` · `raw_get`(`taxonomy.problem[3]` · 한도 넘는 경로 하나 → `truncated`) · `raw_search`(원장에 있는 낱말 하나 · 대소문자 · 공백만 다른 질의가 같은 결과) 실제 호출 각 1회 이상 · 헬스에 manifest 21/21
- 백엔드 커밋 뒤 서버 재시작 후 측정(옛 코드가 떠 있는 상태 측정 금지)

### 6-3. 속도 측정

- 측정만 — 통과 기준은 실측 보고 뒤 사용자가 정한다(10-30 O-2 결정): 문항 111 을 도구 호출로 바꾼 요청 묶음을 따뜻한 서버에 3회 → 도구별 p50 · p95 · 최대(ms, 서버 측 처리 시간 + 클라이언트 왕복 둘 다) · 응답 바이트 중앙 · 최대 · 서버 기동 시 메모리 적재 시간
- 산출 `gold-speed.json` · `.md`

### 6-4. 시험(코드 레포)

| 시험 | 무엇 |
|---|---|
| 빌드 가드 | §3-1 가드 열 · §3-3 · §3-5 를 실물 입력으로 · 일부러 깬 고정 입력(fixture)으로 실패하는지 |
| 결정론 | 같은 입력 두 번 빌드 → 빌드 해시 같음 |
| 도구 코어 | 도구마다 정해 둔 입력 → 기대 출력(실물 빌드에서 뽑은 값 · 가상 문장 없음) |
| REST ↔ MCP 같음 | 같은 입력 응답 JSON 같음 |
| 원장 도구 경계 | `app/modules/raw/` 가 `app.modules.gold` 를 import 하지 않음 · 골드 모듈이 raw 를 import 하지 않음(소스 import 검사 시험) · 원장 도구가 `$W`(실버 · 시맨틱) 경로를 열지 않음 |
| 원장 도구 | manifest 대조(빠진 파일 · 다른 해시 → 마운트 안 함) · 경로 문법 · 잘림 · 검색 정규화(공백 · 대소문자만 — 「쳐짐」 · 「처짐」은 다른 말) · 결정론 |
| 안전 동봉 | 시술이 나오는 모든 도구 응답에 안전 묶음 칸이 있음 |
| **v3 동봉 · 섹션**(WORK-005) | `intent` 12 값 × 도구 → §5-13 묶음 칸이 있고 상한을 안 넘음 · `intent` 없음 = 도구 기본 의도 · 모르는 값 4xx · `sections` 합집합 · `none` · `sections_used` · `intent_used` · 도구 9 공통 section 매핑(T4 · T5 · T6 · T7 에 `sections=emergency` 등이 시술 노드마다 적용) · 계열 카드 `by_unit` 상한 · `INTENTS` 상수 = §5-13 표 행 |
| **v3 facts**(F-A~F-E) | step8_notes 245 앵커 ①~⑤ 셈 · 미해결 0 · attrs 56 owner/attached 1+ · site_caution spec 잎 fact 22엣지 · 비교 조합 members 잎 fact 9조합 · 조합 effect/price fact 79 · pih 잎 fact · `family:None` 0 · **F-D′ patientExplanation 7**(v3.2.1) · 빌드 두 번 해시 같음 |
| **v3 쌍 · 펼침** | pair_check 1개 입력 → `relations[]` · 계열 하나 → `self_pair[]` 4엣지 값 · claims 원문 기본(상한 4 · conditional 표시) · compare `overview · method` rows · `source_comparisons[].members[].attrs_text` · check_conditions family id 6종(M8 · M15 · M4 · M9 · M11 · M12) 200 + `by_unit` 등급 갈림 보임 · 제품 id |
| **v3.2 다이어트**(WORK-007) | 도구 9 × 기본 응답 바이트 ≤ §5-0-1 표(실물 입력 — rerun-v3 호출 676 중 도구별 표본) · `by_unit` 원문 0 · 단위 ≤ 4 · `units_more` · C1′ 같은 계열 · 부위 체인(Q003 입력에 SC-jawline-M1 이 실리프팅 카드에 **없음**) · C2′ 전 등급 id · `question_conditions` 원문 · A1-4 묶음 밖 id ≤ 4 원문 0 · `sections_index` 17 · A1-5 4/24 · `more_ids` 전부 · `index{}` 한 번 · `claude_contract.priority` 순서 결정론 · 설정값 = 표 |
| **v3.2 B 186 ↔ 조항**(WORK-007) | §8 표의 조항 닿는 행 161 — 행마다 같은 입력 재실행 응답에 `gold_hits` fact · 엣지 id 중 하나(`facts[].id` ∪ `more_ids` ∪ 동봉 · 색인 id ∪ `relations_all` · `edges` ∪ 본문 인용) · F-F 24 · F-D′ 잎 · C1′ 3 · C2′ 32 · C3′ 14 · C6′ 4 · C7′ 40 · C9′ 8 · C14′ 11 · §5-14′ 29 |
| **v3.2 MCP 전달**(WORK-007) | `list_tools` 14 도구 `_meta["anthropic/maxResultSizeChars"]` = 설정값(골드 · raw) · `intent` 설명 문구 상수 하나 = 9 도구 · REST · instructions · required 아님 · T10 · T11 은 `intent?` 를 받되 `intent_used: null` · 응답 동봉 0 |
| **v3.2 peek · expand**(WORK-007) | 13 종류 노드마다 peek 200 · 바이트 ≤ 8,000(W7-D4) · 이웃 종류 순서 · 앞 4 · `sections[].bytes` = 원문 합(→ v3.3 행이 바꿈) · expand 가 peek 밖 이웃 · 임의 fact id 를 4xx · section 12 · 이웃 20 · `intent` · 동봉 없음 · REST ↔ MCP 같음 · 두 번 같음 |
| **v3.3 expand 걷기 꼴**(WORK-008) | 전 노드 × section(6,140)에서 **`peek.sections[s].bytes == len(expand(id, sections=[s]) REST 본문)` 차 0** · 기본 꼴 칸 = `facts[]{id, line, section, owner?, cut?, flags?, gap?}` · `more` · `claude_contract{allowed, must_show_flags}` · `priority` · `use_first` · `sections{}` · `source.meta` **없음** · fact id 가 응답에 한 번만(`facts[].id`) · 줄 규칙(공백 접기 · ≤ 40 이면 원문 그대로 · 넘으면 39 + 「…」 + `cut`) · `owner` = 요청 id 면 생략 · `gap` · `flags` 는 있을 때만 · `page` 2 = 13~24번째 줄 · `more` = 남은 수 · `full=true` 는 `text` + `source{file, path}` · `fact_ids` 는 그 노드 fact ∪ (계열 · 제품) 펼친 단위 fact 만(아니면 4xx · 65개 4xx) · `sections` 와 `fact_ids` 가 겹치는 id 는 원문 행 하나만(fact id 한 번) · peek items `n_facts` = 그 이웃 17 section 합 · 앞 4 · 6,140 기본 꼴 중앙 ≤ 2,000 · p95 ≤ 5,000 · `full` 중앙 ≤ 4,000 · p95 ≤ 8,000 · REST ↔ MCP 같음 · 두 번 같음 · `intent` 넘겨도 `request` 빼고 같음 |
| **v3 재인용 대조** | `recheck.py` 가 B 239 행 · 실패 174문항분 호출을 읽어 결정론으로 판정 · 두 번 같음 · **판정 규칙 동일성**: recheck 의 `norm` · 포함 · fact id 규칙으로 `fail-triage.json` 320행을 옛 export 로 재분류하면 cls · sub 가 320/320 같음(F-6 · triage.py 는 수정 · import 하지 않음) |

### 6-5. 끝 조건(측정 · 결정론) — v3.2 판(WORK-007 · v3.3 실물 반영) · v3.1 블록은 아래 「이력」 · v3.3 끝 조건은 §6-7

**v3.2 끝 조건(WORK-007 · 결정론 · 산출 = `reference/2026-10-30-hub-evals/build-out/recheck2/recheck2-report.{md,json}` · 스크립트 `fail-triage-scripts/recheck2.py` — recheck.py 와 같은 판정 식을 다시 적음 · import 안 함)**. 재실행 묶음 = **rerun-v3 실제 호출 676**(`runs.jsonl` batch `b202610311552-d39a4d` · case2 `trace.tool_calls[]` 오류 아닌 것 전부 + case3 `trace.hub` 1회 · `fail-triage2.json meta.replay_unique` 676) 을 **같은 입력**(intent · sections 그대로)으로 v3.2 허브에 다시 보낸다. 기록 입력이 틀린 호출(W5-D14 · 없는 id 등)은 분모 · 오류 셈 밖(사유 열거).

| # | 항목 | 재는 법 | 통과 |
|---|---|---|---|
| (i) | **B 186 재인용**(2차 분류 `fail-triage2.json b_rows`) | 행마다 새 export(v3.2 빌드)로 `gold_match` 재실행 → `gold_hits` 갱신 → 그 문항의 재실행 응답(호출 전부) 안에 갱신된 hit 의 **fact id 또는 엣지 id**(`facts[].id` ∪ `more_ids` ∪ 동봉 · `index` · `sections_index` · `relations_all` · `edges` · `claims` · `reasons` · `refs` 의 id) 또는 정규화 인용(**(a)**) · **v3.3(W7-D2)**: 또는 **(b) 응답에 나온 노드(fact owner · attached · 엣지 양끝 · 요청 노드 · 응답 시술 노드 ≤ 8)에서 `expand(n, sections=[그 section])` · 관계 주장은 `pair_check([양끝], sections=[evidence])` 를 실제로 1회 불러 닿음**(결정론 · 캐시 · `recheck2.reach_one_call`) | **조항이 닿는 행 155(§8 · W7-D12 — v3.2 의 161 에서 데이터상 불가 6 을 `N-데이터` 로) 의 ≥ 90% = 140+**((a)+(b) · (a) 단독 보고) · 닫지 않는 행 31(§8 X0 16 · N 9 · N-데이터 6)은 분자 밖 · 161 · 186 기준 비율 보고 · 묶음 · 조항별 표 · WORK-007 결과 145/155(a 58 · b 87) |
| (ii) | **크기** | 재실행 676 중 「기본 응답」(요청 `sections` 없음)을 도구별 바이트 중앙 · p95 · 최대 · 「sections 있음」 따로 · case3 경로(159)는 그 호출 바이트 | **§5-0-1 표(v3.3 = 측정값)** — 도구별 중앙 · p95 전부 안 · case3 경로 행은 v3.3 에서 지움(걸음 교체 · 보고만) |
| (iii) | **C3 8 → 기본 응답 원문 칸 안**(검수 F-2) | `fail-triage2.json c_rows` 중 `c_sub == C3` 8행. **fact id 가 있는 행 3**(Q003 c2 · c3 `SC-jawline-M1#site_caution#spec.key_warning` · Q069 c2 `combo:RC-CP-wrinkle#evidence#members[3].attrs_text.duration`) · **fact 없는 행 5**(Q014 c2 · Q190 c3 · Q221 c3 = `via 인용 문자열` · Q054 c3 · Q203 c2 = `via 골드 문장` — `fact` · `section` 칸 비어 있음 · 응답 본문 어딘가의 문자열이 인용과 맞았을 뿐). 판정 = **정규화 인용(triage 와 같은 norm)이 같은 입력 재실행 응답의 원문 칸 — `facts[].text` ∪ 동봉 원문 칸(`claims_text` · C1′ `key_warning` 원문 · C7′ price · expectedResult 원문 · C9′ claims text · C10′ 멤버 원문) ∪ **`names` · `emergency_signs`(v3.3 · W7-D11)** — 안에 있음**(노드 이름 · 속성 문자열 · 응답 본문 아무 데나는 **아님** — 다이어트 뒤엔 그 문자열이 빠질 수 있으므로 이 조건의 뜻은 「원문 칸으로 닫히나」). 분모 = fact 없는 5 + Q069 1 = **6** 중 Q203 c2 는 vocab 만 호출이라 밖 → **5**(Q014 c2 · Q054 c3 · Q069 c2 · Q190 c3 · Q221 c3). Q003 ×2 는 C1′ 로 **빠져야 맞음**(엉뚱한 연결) — 반대 조건 「SC-jawline-M1 이 실리프팅 카드에 없음 + 보톡스 턱 단위 카드엔 있음」(v3.3 · W7-D10: 추천 응답엔 M1 카드가 없으므로 「있음」은 보톡스 턱선 단위 U5-016 의 T3 `intent=I-03` 카드로 확인) | **5/5** + Q003 2 반대 조건 · WORK-007 결과 4/5(Q054 c3 ✕ — RC-CP-volume `evidence_notes[0]` 은 조합 잎이라 원문 칸 밖 · id 는 `refs_n` · (b) 로 닿음) + Q003 ○ |
| (iv) | **품질 · 회귀 · 결정론 · 시험** | `gold_quality_eval.py --gold inprocess`(intent 포함) · 재실행 두 번 · pytest · ruff | 6/6 · 106/106 · Q106 · Q108~110 · 회귀 0 · 리포트 바이트 같음 · 시험 전부 · ruff |
| (v) | **peek · expand**(§5-16) | 13 종류 노드 전부(1,071) peek 바이트 · rerun-v3 case3 시작 노드(`hub.resolve.candidates` · 159 run)마다 peek 1회 + 그 peek 의 section 전부 expand 1회 | peek 중앙 ≤ 2,500 · p95 ≤ 8,000(W7-D4) · expand(section 1개) 중앙 ≤ 8,000 · p95 ≤ 16,000(v3.2 꼴 · WORK-007 결과 7,680 / **18,444 FAIL**) → **v3.3 은 §6-7 의 새 꼴 상한으로 바꾼다** |
| (vi) | **걸음 도달**(§6-6) | 결정론 BFS — LLM 없음 | 조항 닿는 행 161(→ 155 · W7-D12) 중 **걸음 ≤ 4 도달 ≥ 90%** · 186 기준 보고 · WORK-007 결과 155/155 |
| (vii) | **실패 문항 재실행** | 코디(이 스펙 밖) — v3.2 허브 + SPEC-006 v2 앱(걸음) 182문항 · 같은 채점 | 보고 |

- 분모 셈(결정론): 186 = `b_rows` 전부 · 조항 닿는 행 161 = §8 「v3.2 조항」 열이 X0 · N-* 가 아닌 행 → **v3.3: 155**(`recheck2.NOT_CLOSABLE_DATA` 6 을 뺌 · W7-D12) · 묶음 ①~⑨ · 의도별 · 도구별 표 같이
- 비율 넷(155 · 161 · 186 · 2차 실패 273)을 다 보고한다 — 끝 조건은 155 기준(V-7 재정의 · W7-D12)

**이력(v3 · v3.1 끝 조건 — 1차 분류 B 239 기준 · WORK-005 결과 131/165 = 79.4% · `work005-report.md`)**:

B 239 건은 「골드엔 있는데 허브 응답에 없음」이다 — 끝 조건은 **허브 응답**(LLM 답 아님)에 그 인용이 들어가는지로 잰다. 대조 스크립트는 `fail-triage-scripts/triage.py` 와 **같은 정규화 · 같은 판정**(소문자 · 공백 · 기호 제거 · 골드 쪽 8자 이상 포함 · fact id 일치)을 쓴다. 산출 = `reference/2026-10-30-hub-evals/build-out/recheck/recheck-report.md` · `.json` · 스크립트 `fail-triage-scripts/recheck.py`(WORK-005 WP-0).

| 항목 | 재는 법 | 통과 |
|---|---|---|
| **B 재인용률** | 실패 174문항의 호출을 **같은 입력으로 다시 보낸다**(전체 replay 유일 호출 755 중 실패 174문항분 — case2 는 trace 의 도구 호출 전부 · case3 는 `trace.hub` 경로 1번 · W-6) + 행의 `jev_intent` 를 `intent` 로(「?」면 없이). **판정(v3.1 · F-3)**: recheck 가 **새 gold-export(v3 빌드)** 로 `gold_match`(triage 와 같은 규칙 — 정규화 · 포함 · 8자)를 행마다 다시 돌려 `gold_hits` 를 갱신한 뒤, B 행이 「닫힘」 = 그 문항의 재실행 응답(도구 호출 전부 · `facts[].id` · 동봉의 fact id · 본문 전체) 안에 **갱신된 gold_hits 의 fact id 하나** 또는 정규화 인용이 있음. 옛 export(e9d30ace)와 새 export 의 빌드 해시 둘 다 리포트 머리에 · WP-0 기준선만 옛 export | **분모 = 카드 도구(T2~T8) 호출이 있던 B 행 205**(239 − 허브 안 부름 17 − resolve · vocab 만 17 · 코디 10-31). **목표 = 조항이 닿는 행(186)의 ≥ 90%**(= 168+) · 분모 205 기준 비율(상한 186/205 = 90.7%)과 239 기준 비율은 **보고**(§7 V-7 · 사용자 확인 자리) · 묶음 ①~⑧ · 의도별 표 · 「닫지 않는 행」 19 는 따로 셈 |
| **오류 15** | 같은 재실행에서 `GET /procedures/family:M*/checks` 15건 | 400 → 200 · 재실행 오류 0 |
| **응답 크기** | 재실행 호출 묶음의 **기본 응답**(요청 `sections` 없는 호출)을 도구별 바이트 중앙값으로 · 요청 sections 있는 호출은 따로 | 도구별 중앙값 ≤ 2 × 현 중앙값(아래 표 「case2 오류 제외」 열 — 셈 규칙 아래) · recommend ≤ 14.4KB · p95 는 보고만 |
| **품질 유지** | `gold_quality_eval.py`(intent 포함) | 6/6 · 106/106 · Q106 · Q108~110 맞음 · 회귀 0 |
| **결정론** | 재실행 · 대조 두 번 | 리포트 바이트 같음(시간 칸 분리) |
| **시험** | §6-4 + v3 시험(WORK-005 WP 마다) | 전부 통과 · ruff |

현 중앙값(기준 · `runs/runs.jsonl` 10-30 전체 실행 239문항 · 바이트 · `statistics.median`). **셈 규칙(v3.1 · F-5)**: case2 = `cases.case2.trace.tool_calls[]` 중 `is_error` 가 아닌 것의 `output_bytes`(전부 749 · 오류 87 = check_conditions 58 · procedure_card 15 · recommend 7 · vocab 5 · pair_check 2 → **662**) · case3 = `cases.case3.trace.hub.tool` 이 있는 run 의 `result_bytes`(**201** · 15건 400 포함 · 허브 경로 없는 run 38 제외) · 「sections 없음」 = case2 오류 제외 중 `input.sections` 가 비어 있는 호출(기본 응답 기준):

| 도구 | case2 오류 제외 n / 중앙 | case2 sections 없음 n / 중앙 | case3 n / 중앙 | v3 상한(case2 오류 제외 ×2) |
|---|---|---|---|---|
| recommend | 58 / 7,262 | 47 / 6,567 | 18 / 8,171 | **14,524**(브리프 7.2KB ×2 = 14.4KB) |
| procedure_card | 154 / 17,180(요청 sections 포함) | 16 / 1,447 | 125 / 26,325(Jev sections ≤ 4) | 34,360 — 기본 응답은 「sections 없음」 열(1,447)과 따로 대조 |
| pair_check | 22 / 7,200 | 23 / 7,151 | 29 / 6,882 | 14,400 |
| check_conditions | 28 / 24,206 | 10 / 115(오류 응답 셈) | 5 / 21,977 | 48,412 |
| compare | 14 / 7,997 | 6 / 7,268 | 21 / 6,146 | 15,994 |
| combos | 4 / 9,537 | 4 / 9,537 | 3 / 7,288 | 19,074 |
| neighbors | 9 / 6,544 | 7 / 5,633 | — | 13,088 |
| resolve | 364 / 1,059 | 364 / 1,059 | (경로 안) | 2,118 |
| vocab | 9 / 6,314 | 14 / 5,501(오류 포함) | — | 12,628 |
| 합 | 662 | — | 201 | — |

**닫지 않는 행(v3.1 · 분모 205 안 · 19행 · 이력 — v3.2 는 §8 의 25행이 정본)** — 조항이 닿지 않음을 명시한다(재인용률 분자에 안 들어감 · 리포트에 같은 표로):

| 사유 | 행 | 문항 · 케이스 | 왜 안 닫나 |
|---|---|---|---|
| C10(비교 멤버 원문)은 compare 에서만(§5-15 결정 · W-4) | 10 | Q117 c2 · Q119 c2 · Q121 c2 · Q149 c3 ×2 · Q156 c2 · Q156 c3 ×2 · Q192 c3 · Q234 c3 | 비교 조합 members 원문을 카드 · 쌍 · 추천 slim 에 올리지 않기로 함(비교 맥락 밖) |
| 조항 없음(F-1 (c)) | 3 | Q123 c3(concern:P8-2 이름) · Q228 c2(product `1_identity.basis`) · Q118 c2(treats `evidence.role` — F-C 로 fact 는 생기나 I-06 compare 동봉 밖) | 고민 이름 · 제품 정체 근거는 동봉 대상이 아님 · treats role 은 추천 why 에만 |
| I-04 · I-09 에 C7 없음 | 2 | Q050 c3 · Q138 c2 | 부작용 · 확인 조건 의도에 조합 속성을 붙이지 않음(코디 결정 목록 밖 · 크기) |
| 1-hop 기타(동봉 종류 밖) | 4 | Q068 c2(unit market) · Q070 c2(다른 단위 시술 side_effects) · Q082 c3(package evidence) · Q084 c3(product products) | 시장가 · 다른 시술의 부작용 · 패키지 근거는 어느 의도 동봉에도 없음 |

분모 밖(참고): 허브 안 부름 17(문항 14 · case3 13 + case2 Q205) · resolve · vocab 만 호출 17(case2 Q015 · Q028 · Q082 · Q105 · Q113 ×2 · Q115 · Q122 · Q129 ×2 · Q135 · Q136 · Q162 ×2 · Q192 · Q211 · Q231 — T1 은 G13 요약만 · 동봉 · 섹션이 붙을 시술 노드가 없음).

- 허브 도구를 아예 안 부른 B 17건(문항 14 — case3 Q066 · Q101 · Q118 · Q122 · Q130 · Q164 · Q166 · Q178 · Q193 · Q197 · Q203 · Q204 · Q238 + case2 Q205 · 되묻기 · I-12 가격 · 필수 슬롯 없음)과 resolve · vocab 만 부른 17건은 허브 응답에 시술 노드가 없어 재인용률 분모에서 뺀다(코디 10-31) — 앱(SPEC-006) 몫 · §7 V-1
- A 61 · C 6 · 미분류 14 는 이 끝 조건 밖(A = 실버 9단계 · C = 사용자 10-31 「프롬프트 문제 아님으로 둠」)

### 6-6. 걸음 도달 측정(v3.2 · peek/expand · 결정론 · LLM 없음)

Jev 재귀 탐색이 **걸음 4 안에** B 186 의 fact 에 닿을 수 있는지를 그래프 경로 길이로 센다(Jev 가 고를지는 앱 실험 몫 · 여기선 「닿을 수 있나」만). 산출 `build-out/recheck2/reach-report.{md,json}` · 스크립트 `fail-triage-scripts/reach.py`.

| 항목 | 정의 |
|---|---|
| 시작 노드 S | 행의 문항에서 case3 `trace.hub.resolve.candidates`(rerun-v3 · 159 run) ∪ `menu_candidates` · 허브 안 부른 문항(X0)은 그 문항 질문을 T1 resolve 로 돌린 `candidates`(resolve 는 결정론) |
| 걸음 1 | S 의 노드 n 을 peek → expand(sections = 그 fact 의 section)로 **n 이 owner 또는 attached_to 인 fact** 전부에 닿음(= 1걸음 · section 상한 12 밖이면 `more_ids` → `fact_ids` 로 같은 걸음에 받음 · **v3.3**: 기본 꼴은 `more` 셈 → `page` 2… 로 같은 걸음) |
| 걸음 +1 | expand(neighbors) 로 peek 가 낸 이웃(종류별 앞 4(W7-D4) **또는** `neighbor_kinds` 전부)으로 옮김 — 엣지 = 골드 엣지 전부(저장 + 펼친 · `candidates:` 끝은 후보 전부 · 조건부는 `include_conditional` 없이 제외) · 방향 무관 |
| 도달 걸음 d(f) | min over s ∈ S of (s → owner/attached 노드 최단 홉 + 1) · 엣지 속성 fact(F-C · owner 가 엣지)는 양끝 노드 중 가까운 쪽 · `scope:all` fact 는 attached_to 로 · 전역(G16)은 걸음 1(peek `global`) |
| 통과 | 조항 닿는 행 161 중 **d ≤ 4 인 행 ≥ 90%** · 분포(d = 1 · 2 · 3 · 4 · >4 · 도달 불가)를 묶음 · 케이스별로 · 186 기준도 보고 · 도달 불가 행은 사유(fact 가 어느 노드에도 안 붙음 · S 가 빔) |
| 결정론 | 같은 export · 같은 trace → 같은 리포트 바이트(시간 칸 분리) · 두 번 |

- 이 측정은 **허브 그래프의 속성**이라 WORK-007 에서 닫는다. Jev 가 실제로 그 길을 고르는 비율 · 걸음 수 · 바이트 · 첫 글자는 SPEC-006 v2 재실행(코디)

### 6-7. v3.3 끝 조건 — expand 걷기 꼴(WORK-008 · 결정론 · Jev · LLM 없음)

작성 때 숫자(「설계 측정」 열)는 `spec005-v33-measure.py` 가 **b031371c 와 같은 입력 · 같은 코드로 메모리 빌드한 그래프 위에서 새 꼴을 흉내 내** 잰 값이다(해시 b031371c4c69cea1 확인 · 옛 expand 재계산이 rerun-v4 기록 476 호출 중 475 와 바이트 같음 · 두 번 같음). WORK-008 은 **실물 코드**로 같은 셈을 다시 내고(산출 `backend/build-out/work008-report.md` · `reference/2026-10-30-hub-evals/build-out/walk3/`), 아래 「통과」 열로 판정한다.

| # | 항목 | 재는 법 | 설계 측정 | 통과 |
|---|---|---|---|---|
| (a) | **expand 기본 꼴 크기 · section 1** | 전 노드 × section 6,140 쌍마다 `expand(id, sections=[s])` REST 본문 바이트 · rerun-v4 걸음 호출 476(같은 노드 · 같은 sections · 같은 neighbors) 재생 · 676 재실행이 닿은 (노드, section) 481 | 6,140: 중앙 1,902 · p95 2,710 · 최대 3,228 · 476(이웃 포함): 2,014 / 3,676 / 4,720 · 그중 이웃 없는 231: 1,882 / 2,524 · 481: 1,890 / 2,647 · (옛 꼴 6,733 / 20,863 / 59,277) | 6,140 · 이웃 없는 걸음 호출 둘 다 **중앙 ≤ 2,000 · p95 ≤ 5,000** · 이웃 포함은 보고 |
| (b) | **`full=true` 크기** | 6,140 쌍 `full=true` | 2,982 / 4,256 / 5,210 | 중앙 ≤ 4,000 · p95 ≤ 8,000 |
| (c) | **peek bytes = 실제** | 6,140 쌍 `peek(id).sections[s].bytes` 와 (a) 의 바이트 | (설계상 같음) | **차 0 · 6,140/6,140** |
| (d) | **peek 크기** | 1,071 노드(`n_facts` 포함 · 앞 4) · rerun-v4 걸음이 연 peek 311 | 1,071: 2,257 / 7,171 / 9,477(v3.2 꼴 같은 기준 2,183 / 6,788 / 8,907) · 311: 3,054 / 8,926 / 9,477(v3.2 꼴 2,845 / 8,408) | 1,071 중앙 ≤ 2,500 · p95 ≤ 8,000 · 311 은 보고 |
| (e) | **걸음 재생**(아래 규칙) | rerun-v4 case3 걸음 판 148(되돌아감 34 제외)의 같은 선택을 새 꼴로 · 예산 20,000(rerun-v4 앱이 센 바이트 = `json.dumps(d, ensure_ascii=False)` 로 재생 — V-17 결정 뒤 앱은 허브 직렬화로 세므로 실제는 ≈ 4~7% 여유가 더 남음 · cut 원문 받기는 재생에 안 넣음 · V-15 결정으로 실제 걸음에선 예산에 들어감) · 걸음 상한 4 | (옛 꼴 재생 → 새 꼴 재생 · 옛 꼴 재생 평균은 기록 1.84 와 같음) 평균 걸음 **1.84 → 3.03**(중앙 2 → 3 · 새 분포 1:17 · 2:28 · 3:37 · 4:66) · 이웃 노드 도달 **53.4% → 88.5%**(79 → 131/148) · 멈춤 budget 110 → 28(새 꼴 나머지 = steps 58 · frontier_empty 28 · enough 21 · empty 13) · 걸음 바이트 중앙 15,877 → 10,087 · 줄로 받은 fact 중앙 38 · 그중 원문(cut 없음) 27.5(옛 14) · cut 14(원문 받기 5,389B · V-15) | **평균 걸음 ≥ 3.0 · 이웃 도달 ≥ 85%** · 걸음 바이트 ≤ 20,000(규칙상) · 분포 · 멈춤 사유 보고 |
| (f) | **「자료에 없다」 case3 68행 도달** | rerun-v4 `remaining_failures` 중 case3 · 정확성 · 판정 문장이 `자료에 없\|정보 없음\|없다고\|찾지 못` 인 행(68 · 같은 식 case2 51 — 배경의 48 과 셈 식이 다름) → 행 인용을 b031371c export 로 `gold_match`(recheck2 와 같은 식) → hit fact id 가 (e) 재생에서 줄로 나왔나 | **새로 닿음 5**(줄 · 원문 2 · cut 3) · 옛 판도 받음 0 · 새 꼴로도 안 닿음 34 · 골드 fact 와 인용이 안 맞음 23 · 걸음 없음(되돌아감) 6. 안 닿은 34 의 자리 = 방문 노드인데 Jev 가 그 section 을 안 고름 11 · 방문 노드 · 그 section 펼침 · 1쪽 밖 2 · 방문 노드에서 1홉 17 · 2홉 2 · 6홉 안 연결 없음 2(전역 메모 `scope:all`). **분모 39(= 닿음 5 + 안 닿음 34 · 골드 fact 있고 걸음 있는 행)**: 시작 노드에서 fact 노드까지 0홉 13 · 1홉 18 · 2홉 6 · 없음 2 · 정책 B(같은 방문 노드 · section 전부 · 같은 예산) 닿음 9 · 안 닿음 30 | **≥ 5**(회귀 경계) · 사유 표 · 행 목록 보고 — 나머지는 Jev 선택 · 실버 몫이라 허브 끝 조건 아님(V-16) |
| (g) | **case2 도구 회귀 0** | 676 재실행(WORK-007 `recheck2 rerun --inprocess`) | — | T1~T9 응답 바이트가 WORK-007 `sizes.json` · `rerun-responses.inprocess.json` 과 같음(빌드 해시 · 시간 칸 빼고) · (i) 145/155 이상 — (b) 추가 호출은 새 expand 꼴에서 **쪽 넘김 포함**(`page` 2… · 같은 section 이면 1 추가 호출로 셈) |
| (h) | **품질 · 결정론 · 시험** | `gold_quality_eval.py --gold inprocess` · (a)~(f) 두 번 · pytest · ruff | — | 6/6 · 106/106 · Q106 · Q108~110 · 회귀 0 · 리포트 바이트 같음(시간 칸 분리) · §6-4 v3.3 행 · 전체 시험 · ruff |

**걸음 재생 규칙(결정론 · Jev 다시 안 부름)** — `runs.jsonl` b202611011148-c6ed3a 의 `cases.case3.trace.walk`:
1. 걸음 k 의 노드 = 기록 `steps[k].node` · 고른 것 = 기록 `jev.picked` **전부**(옛 판에서 예산으로 빠진 것 포함 · `section:` 접두 = section · 나머지 = 이웃) — 앱(clinic_chat f8533ff)처럼 **section 하나씩** 호출 · 이웃은 첫 호출에 같이 · 앱이 넘긴 `intent` 를 그대로
2. 예산 = expand 응답 바이트 합(peek 는 안 셈 · 앱과 같음) · 처음 넘는 호출은 통째로 빼고 그 걸음에서 멈춤(budget)
3. 기록 걸음이 끝났는데 기록 `stop == budget` 이면 이어 간다: 다음 노드 = 펼친 이웃 큐(넣은 순서 · 방문 안 한 것 · 없으면 `frontier_empty`) · 고르는 것 = 그 판에서 Jev 가 고른 section 이름 ∩ 그 노드 peek section(peek 순) · 이웃은 안 고름. 기록 `stop` 이 enough · steps · empty 면 같은 자리에서 멈춤(Jev 판단 그대로)
4. 「이웃 노드 도달」 = 방문 노드 2 이상 · 「닿음」 = hit fact id 가 받은 줄의 `id` 에 있음(「원문」 = 그 줄이 cut 아님)
5. 이 재생은 **새 꼴이 예산 안에 몇 걸음을 허락하나**를 잰다 — Jev 가 새 꼴에서 무엇을 고를지는 재지 않는다(그건 WORK-009 뒤 코디 재실행)

- (f) 가 낮은 이유는 허브 꼴이 아니라 **고름**이다: 안 닿은 34 중 32 는 걸음이 그 노드에 갔거나(13 — section 안 고름 11 · 1쪽 밖 2) 1~2홉 옆(19)인데 Jev 가 그 section · 이웃 · 다음 쪽을 고르지 않았다(나머지 2 = 전역 메모). 「자료에 없다」 68 중 23 은 골드 fact 와 인용이 안 맞는다(실버 · 9단계 몫 · A 그룹과 같은 꼴).

---

## 7. 열린 것 · 결정된 것

v2 까지 열린 것: **없음**(O-1 ~ O-4 는 10-30 사용자 결정 「열린 것은 추천으로 가자」로 닫힘 — _RESUME §2 10-30 행).

**v3 아직 안 정한 것**(추측으로 메우지 않음 · 본문은 「추천 기본값」으로 써 두고 여기에 표시):

| id | 무엇 | 추천(본문에 쓴 값) | 누가 |
|---|---|---|---|
| V-1 | 허브를 아예 안 부른 B 17건(문항 14) · resolve · vocab 만 부른 17건은 허브 스펙으로 못 닫는다 — 분모(205)에서 빼고 앱(SPEC-006)으로 넘기는가(코디 10-31 「분모 = 카드 도구 호출이 있던 B」 로 진행) | 분모 205 · 239 기준도 같이 보고(§6-5) · I-12 는 허브 도구 없음 유지 | 사용자 |
| V-2 | `intent` 가 없을 때 — 도구 기본 의도의 묶음을 붙이는가(case2 Claude 호출도 커짐) · 아니면 G13 요약만 | 도구 기본 의도(§5-0) | 사용자 |
| V-3 | 크기 상한의 기준 — **v3.3 에서 닫음**: §5-0-1 표 = WORK-007 측정값을 위로 올림(회귀 경계 · case2 C 3.8% · 잘림 0 근거) · case3 경로 행 삭제(걸음 교체). 더 줄일지는 V-14 | (닫힘) | — |
| V-4 | I-04 「management」(합병증 관리 · 예방 · A 그룹 `complications.management/prevention`)는 지금 골드에 section 이 없다 — 9단계가 section 이름(`safety.management`?)을 정할 때 §4-3 · §5-14 I-04 에 더한다 | v3 에선 안 넣음 | 9단계 스펙 |
| V-5 | 앱(SPEC-006) 쪽 — Jev 가 `intent` 를 허브에 넘길지 · Jev section 상위 4 · noul 0.5 규칙을 그대로 둘지(기본 묶음이 덮으므로 둬도 됨) · 필수 슬롯 없을 때 되묻기 대신 T4 「관계 목록」을 쓸지 | 허브는 받기만 · 앱 변경은 SPEC-006 v2 | 사용자 · SPEC-006 |
| V-6 | §5-15 slim 승격 문턱 「5건 이상」 — **v3.2 에선 뜻이 줄었다**(id 는 어디서나 C7′ refs · 원문 승격은 price · expectedResult 1 조합만) · 문턱 자체는 그대로 | 5건 유지 | 사용자 |
| V-7 | §6-5 재인용률 목표의 분모 — **v3.2 재정의**: 2차 분류 B 186 중 조항 닿는 행 161 의 ≥ 90%(145+) · 186 · 273 기준은 보고. v3.1 의 205/186 은 1차 분류(이력) | 161 기준 | 사용자 |
| V-8 | peek · expand 를 **새 도구 2(T10 · T11)** 로 둘지 T3 · T8 의 모드로 둘지(보충 「실물 보고 정함」) · fact id 단건 조회 도구를 둘지(A1-6 은 안 둠) | 새 도구 2 · 단건 조회 없음(`expand.fact_ids` 로 대신) | 사용자(WORK-007 WP-4 실물 뒤) |
| V-9 | A1-4 「의도 묶음 밖 명시 `sections` 요청은 id 만 · 원문 0」 — case2 에서 Claude 가 의도와 어긋난 section 을 명시해 물으면 원문을 못 받는다(더 받으려면 `intent` 를 맞추거나 `expand`). SPEC-006 v2 가 `intent` 필수로 가면 좁아짐 · recheck 는 id 로 닫히므로 끝 조건엔 영향 없음 | id 만(브리프 지시) · 측정 뒤 「묶음 밖 명시 요청도 원문 ≤ 4」 로 완화 가능 | 사용자 |
| V-10 | case3 걸음 상한(기본 4) · 예산(기본 20KB) · 「충분」 문턱 · 되돌아가기 조건 — 허브 끝 조건 (v) · (vi) 의 「4 걸음 · 20KB」 는 보충의 기본값을 그대로 쓴 것 | 4 · 20KB(SPEC-006 v2 와 같은 값) | SPEC-006 v2 · 사용자 |
| V-12 | M-2 `intent` 를 스키마 required 로 할지 — 추천 = 선택 유지 + 설명 필수(코디 보충 2 추천과 같음). SPEC-006 v2 재실행에서 `intent_passed` 가 95% 에 못 미치면 required 로 바꾸는 선택지가 남는다 | 선택 유지 | 사용자(SPEC-006 재실행 뒤) |
| V-13 | §5-16 손잡이 — **v3.3 에서 닫음**: 앞 4(W7-D4) · 이름 20 · 255 · 64 · 1쪽 12줄 · 줄 40자 · 이웃 20 · 종류 순서 — §5-16 「값 근거」(grid 측정) | (닫힘) | — |
| V-11 | `claude_contract.priority` · `use_first` 를 앱 프롬프트가 쓰는 방식 — **v3.3: case3 는 해당 없음**(T11 이 `priority` · `use_first` 를 안 냄 · SPEC-006 v2.2 §3-4-1) · **case2 만 남음** | 앱이 한 줄 넣음(case2) | SPEC-006 v2 |
| V-14 | case2 기본 응답을 더 줄일지 — 「더 줄일 자리 6」(`work007-report.md` §2: ① `claude_contract` id 3중 ② C4′ 제품 행 필드 ③ 17 section 색인 0 생략 ④ facts 24 → 16 ⑤ 안전 요약 단위 8 → 4 ⑥ compare 멤버 원문 6 → 3). v3.3 은 expand 만 바꾸고 case2 도구는 안 건드림(§6-7 (g) 바이트 같음) | 안 함(측정값 표 유지) · case2 재실행에서 C 비율이 오르면 ① · ③ 부터 | 사용자 |
| V-15 | `cut` 줄(40자 넘는 원문 · 걸음당 중앙 14줄 · 받기 재생 중앙 5,389B · p95 14,376)을 Claude 전에 원문으로 받을지 · 예산에 넣을지 — **닫힘(코디 11-01 결정 · case3 · SPEC-006 §3-4-1 · §3-4-7)**: cut 줄 원문은 `fact_ids` 로 받되 **그 바이트도 걸음 예산에 포함** | (닫힘) | — |
| V-16 | 「자료에 없다」 case3 68 중 새 꼴로 닿는 5 를 넘기려면 — Jev 의 section · 이웃 · 쪽 고름(32행)을 바꿀지(예: peek `n_facts` · `bytes` 를 Choice 입력에 넣기 · 남은 예산 안이면 고른 노드의 section 을 더 펼치기) · 인용이 골드 fact 와 안 맞는 23 은 실버 9단계로 | 허브 꼴은 여기서 멈춤 · 고름은 앱 · 23 은 9단계 | SPEC-006 · WORK-009 · 9단계 스펙 |
| V-17 | 바이트 셈 방법 — **닫힘(코디 11-01 결정)**: 앱 예산 셈도 **허브와 같은 직렬화**(REST 본문 = `ensure_ascii=False` · 구분자 `(",", ":")`) — peek `bytes` 와 앱 셈이 같아짐 | (닫힘) | — |
| V-18 | 쪽 넘김(`page`) — **닫힘(코디 11-01 결정 · case3 · SPEC-006 §3-4-1 · §3-4-7)**: 걸음은 **1쪽만** 받고 `more` 는 기록만 · 허브는 `more` 셈 · `page` 를 낼 뿐(case2 · 시험 · recheck2 (b) 는 `page` 를 씀) | (닫힘) | — |

| id | 무엇 | 결정(10-30) | 본문 |
|---|---|---|---|
| O-1 | neighbors 한도(D-15) | depth ≤ 2 · limit 50 · truncated | §5-9 |
| O-2 | 속도 통과 기준 | 실측 보고 뒤 사용자가 정함 — 이 작업은 측정 · 보고까지 | §6-3 |
| O-3 | Claude 계약 블록(D-16) | 응답에 `claude_contract{allowed_fact_ids, must_show_flags, rule}` 블록을 낸다 | §5-0 |
| O-4 | 확인 조건 ledger 대상 3행(원장 「넥큐레이션」) | 패키지 P6-03 에 붙인다 | §3-3 · §5-6 |

- **v3.3 에서 결정으로 쓴 것**(사용자 11-01 「발주하자」 · 발주서 `phub-recommend-spec005-v33-brief.md`): expand 기본 꼴 = fact 한 줄 목록(원문 앞부분 결정론 자르기 · 요약 생성 없음) · 원문은 `full` · `fact_ids` 로만 · peek `bytes` = 실제 expand 바이트 · peek 이웃은 종류별 셈 · 앞 4 라벨 · `n_facts` 만(「답이 많은 곳」 추측 표시 안 함) · 크기 표 = 측정값 · WORK-007 D-1~D-13 = 본문 · **검수 패치(코디 11-01)**: V-15 cut 원문은 받되 예산 포함 · V-17 앱도 허브와 같은 직렬화 · V-18 걸음은 1쪽 · 허브 LLM 없음 · 결정론 유지 · 실버 · 시맨틱 수정 없음
- **v3.2 에서 결정으로 쓴 것**(사용자 11-01 · 코디 발주서): case3 = Jev 재귀 탐색으로 **교체** · A-1 다이어트는 case2 기본 응답에 그대로 · 2.5× 폐기 · 허브에 LLM 없음 유지(우선순위도 규칙) · 실버 · 시맨틱 · 시맨틱 수정 없음(A 54 는 9단계) · 원장 인용 본문은 스펙 · 시험에 안 옮김(fact id · 경로만)
- v3 에서 **결정으로 쓴 것**(결정표 안 · 브리프 지시): 허브에 LLM 없음 · 결정론 · 병원 독립 · slim 원칙(D-14) 유지 · 안전 늘 동봉(G13) · 충돌 = resolved 하나(T5 펼침의 「가장 엄격 하나 + by_unit」 도 D-13b 와 같은 방향) · 실버 · 시맨틱 수정 없음(F-A~F-E 는 골드 빌드 규칙 · A 그룹은 9단계)
- U-2(허브 호출 주체) · U-3(시장가 표시)는 10-30 결정대로 앱 · 화면 설계 때 — 이 스펙의 열린 것 아님
- D-17(미라쥬 영역 대응 = 연결 층) · D-18(보강 후보 목록)은 10-30 경계 결정(「병원 상품 · 연결 층은 앱」 · 「허브에 없는 건 보강 후보 목록만」)과 같아 열린 것 아님 — §1-2 · §3-6

---

## 8. 부록 — B 186 ↔ v3.2 조항 1:1(2차 분류 `fail-triage2.json b_rows` · rerun-v3 실제 호출 기준)

셈(결정론 · 스크립트로 뽑음): **186 = 조항 닿는 행 161 + 닫지 않는 행 25**(X0 허브 안 부름 · resolve 만 16 · N 9). 조항별: C7′ 40 · C2′ 32 · §5-14′ 29 · F-F 18(2차 「섹션 매핑 밖」 24 중 F-F 표에 열거된 행 · 나머지 6 은 C7′ · C2′ · C6′ · C12′ 로) · C3′ 14 · C14′ 11 · C9′ 8 · C6′ 4 · C1′ 3 · C4′ 1 · F-D′ 1. 케이스별: 닿음 case2 77 · case3 84 / 닫지 않음 case2 4 · case3 21.

**v3.3(W7-D12 · W7-D10)**: 아래 「조항 닿는 행」 중 **데이터상 불가 6** 을 닫지 않는 행 `N-데이터` 로 옮긴다 — Q007 c2 · c3(concern:J10 추천 카드 0) · Q018 c3(K8-0253 은 M2 주장 · 입력 M1) · Q192 c3(K8-0110 은 M14 · 카드 M9) · Q126 c2(K8-0230 은 M15 · 입력 U5-030 은 M8) · Q169 c3(C4′ basis 인데 I-09 에 C4 없음 — 표의 C4′ 1 이 0 이 됨). 그래서 **조항 닿는 행 155 · 닫지 않는 행 31**(25 + 6) · 조항별 C2′ 32 → 28 · C4′ 1 → 0 · F-F 18 → 17. 행 목록 정본 = `recheck2.NOT_CLOSABLE_DATA` · `build-out/recheck2/b186-clauses.json`. Q003 c2 · c3 반대 조건의 「보톡스 턱 단위 카드」 = U5-016 의 T3 `intent=I-03` 카드(추천 응답엔 M1 카드 없음).

**닫지 않는 행 25(사유)**:

| 사유 | 행 | 문항 · 케이스 |
|---|---|---|
| X0 허브 안 부름(앱 · SPEC-006 — 되묻기 · 필수 슬롯 없음 · I-12) · resolve 만 | 16 | Q028 c3 · Q066 c3 ×2 · Q082 c2(resolve 만) · Q101 c3 · Q118 c3 · Q122 c3 · Q164 c3 · Q166 c3 · Q176 c3 · Q197 c3 ×3 · Q204 c3 ×2 · Q238 c3 |
| N-다른계열 — 응답 노드와 다른 계열의 원문(1-hop 아님) | 2 | Q167 c3(M2 카드에 M15 overview) · Q172 c2(M15 checks 에 M11 합병증) |
| N-제품수준 — 계열 카드에서 제품(2-hop) 수준 원문 · §6-6 걸음 측정엔 들어감 | 2 | Q124 c3 ×2 |
| N-9단계 — A 그룹 성격(management · technique 설명 사실 · 골드 fact 없음 · V-4) | 3 | Q189 c2 · c3 · Q106 c3 |
| N-조항없음(v3.1 그대로) | 2 | Q228 c2(product `1_identity.basis`) · Q082 c3(I-07 에 package evidence 없음) |

열 설명: 「빠진 칸(2차)」 = `fail-triage2.md` §3 sub · 「골드 owner · section」 = 2차 gold_owner · 「fact · 엣지 id」 = 2차 `gold_hits` 앞 2(원문 없음 · id 만) · 「실제 호출」 = rerun-v3 trace(case2 = `tool_calls` 중 resolve · vocab · 오류 제외 · case3 = `hub`) · 「v3.2 조항」 = 이 스펙 절 · 「메모」 = 어느 id 로 닫히는지.

| # | 문항 | 케이스 | 항목 | 빠진 칸(2차) | 골드 owner · section | fact · 엣지 id(gold_hits 첫 2) | 실제 호출(도구 · 입력 · intent · sections) | v3.2 조항 | 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Q002 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PRIOR · checks | `K8-0192 · requires_check:K8-0192:C-PRIOR` | recommend(['concern:auto-83-1774737181584'] · — · —) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 2 | Q002 | case3 | 안전 | 엣지 속성 — 양끝 도달 | site_caution:SC-nasolabial-M1 · — | `site_caution:SC-nasolabial-M1#site_caution#vessels[0].danger · site_caution:SC-nasolabial-M2#site_caution#spec.primary_risk` | recommend(['concern:auto-83-1774737181584'], site:site.nasolabial · I-01 · method,checks,recovery,overview) | **C1′** | 부위 위험 잎 fact id 전부(spec · vessels · pearls) · 같은 계열 · 부위 체인 |
| 3 | Q004 | case2 | 불확실 | 쌍 관계 fact — pair_check/compare 안 부 | procedure_relation:E8-0169 · evidence | `R8-0145#reason` | recommend(['concern:P11-2'] · — · —)<br>recommend(['concern:auto-89-1774737181584'] · — · —) | **C3′** | 카드 · checks 응답의 C3′ = 닿는 procedure_relation 엣지 id · claims id 전부(종류 무관) |
| 4 | Q006 | case3 | 질문에 답함 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-RE-R5 · evidence | `combo:RC-RE-R5#evidence#effect.expectedResults` | recommend(['concern:P6-3', 'concern:P6', 'concern:P7'], site:site.face · I-01 · method,safety.pih,recovery,checks) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 5 | Q007 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-ANTICOAG · checks | `K8-0267 · requires_check:K8-0267:C-ANTICOAG` | recommend(['concern:J10'] · — · —) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 6 | Q007 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-ANTICOAG · checks | `K8-0267 · requires_check:K8-0267:C-ANTICOAG` | recommend(['concern:J10'], site:site.full-face · I-01 · method) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 7 | Q008 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | unit_procedure:U5-023 · safety.pih | `pih[0]` | recommend(['concern:P5-1'] · I-01 · —) | **§5-14′** | 묶음 밖 section(safety.pih) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 8 | Q008 | case2 | 안전 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[138] · scope:all#evidence#step8_notes[139]` | recommend(['concern:P5-1'] · I-01 · —) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 9 | Q010 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-INFECT · checks | `K8-0057 · K8-0105` | procedure_card(family:M7 · — · overview,method) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 10 | Q010 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-INFECT · checks | `K8-0057 · K8-0105` | procedure_card(family:M7 · I-02 · method,overview) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 11 | Q014 | case3 | 질문에 답함 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M7 · recovery | `family:M7#recovery#family_text[환자 설명 가이드(patient-education)][0].downtime` | procedure_card(family:M7 · I-05 · recovery,timeline,ops,evidence) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 12 | Q015 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | combo:RC-CP-lifting · evidence | `combo:RC-CP-lifting#evidence#members[1].attrs_text.limitations` | compare(['unit_procedure:U5-102', 'unit_procedure:U5-091'] · — · —) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 13 | Q015 | case2 | 안전 | slim 카드 밖 섹션(section 안 요청) | combo:RC-CP-lifting · evidence | `combo:RC-CP-lifting#evidence#members[1].attrs_text.limitations` | compare(['unit_procedure:U5-102', 'unit_procedure:U5-091'] · — · —) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 14 | Q015 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev n | combo:RC-CP-lifting · evidence | `combo:RC-CP-lifting#evidence#members[1].attrs_text.cost_range` | compare(['product:M9-1-1', 'product:M9-1-2', 'unit_procedure:U5-102', 'unit_pr · I-06 · method,overview,recovery,ops) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 15 | Q015 | case3 | 안전 | slim 카드 밖 섹션(section 안 요청) · Jev n | family:M9 · checks | `K8-0303 · family:M9#checks#family_text[상담 · 준비 · 고지 · 조건 아닌 문장(확인 조건 엣지 아님)][1]` | compare(['product:M9-1-1', 'product:M9-1-2', 'unit_procedure:U5-102', 'unit_pr · I-06 · method,overview,recovery,ops) | **§5-14′** | 묶음 밖 section(checks) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 16 | Q015 | case3 | 질문에 답함 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M9 · overview | `family:M9#overview#family_text[환자 설명 가이드(patient-education)][0].common_concerns[0].q` | compare(['product:M9-1-1', 'product:M9-1-2', 'unit_procedure:U5-102', 'unit_pr · I-06 · method,overview,recovery,ops) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 17 | Q016 | case3 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) · Jev n | combo:RC-CP-volume · evidence | `combo:RC-CP-volume#evidence#evidence_notes[1]` | compare(['product:M3-1-1', 'unit_procedure:U5-090'] · I-06 · overview,method,recovery) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 18 | Q017 | case2 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0077 · evidence | `R8-0154#reason · R8-0166` | pair_check(['unit_procedure:U5-140', 'unit_procedure:U5-082'] · — · —) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 19 | Q017 | case3 | 안전 | 쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍 | procedure_relation:E8-0208 · evidence | `EV-GD-002 · R8-0146#reason` | pair_check(['product:auto-40-1774737181584', 'unit_procedure:U5-140'] · I-07 · checks,evidence,method,safety.side_effects) | **C3′** | 입력 노드(펼친 단위 포함)에 닿는 procedure_relation 전부 id + claims id(relations_all) |
| 20 | Q018 | case3 | 정확성 | 노드 속성(combo) · 노드에 안 닿음 | combo:RC-RE-R6 · — | `(fact 없음)` | pair_check(['product:M1-2-1', 'unit_procedure:U5-001'] · I-07 · checks,site_caution,safety.side_effects,evidence) | **F-D′** | combo `consult_copy.patientExplanation` 잎 fact 추가(7 · RC-RE-R6 포함) → C7′ refs 로 id |
| 21 | Q018 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-KEL · checks | `K8-0253 · K8-0259` | pair_check(['product:M1-2-1', 'unit_procedure:U5-001'] · I-07 · checks,site_caution,safety.side_effects,evidence) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 22 | Q020 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0297 · K8-0311` | pair_check(['product:M1-2-1', 'product:auto-40-1774737181584'] · I-08 · timeline,recovery,evidence,method) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 23 | Q021 | case2 | 정확성 | 엣지 속성 — 양끝 도달 | requires_check:K8-0366:C-ISO · — | `requires_check:K8-0366:C-ISO · requires_check:K8-0366:C-ISO` | check_conditions(family:M8 · — · —)<br>check_conditions(family:M8 · — · none) | **C2′** | requires_check 엣지 id(K8-0366:C-ISO) — check_conditions 계열 펼침 checks[] 에 id |
| 24 | Q025 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | combo:RC-PC-P1-3 · market | `combo:RC-PC-P1-3#market#price · combo:RC-PC-P5-3#market#price` | combos(menu:쁘띠시술 · — · —) | **C7′** | 조합 price fact id(C7′ · 모든 의도) |
| 25 | Q025 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | combo:RC-PC-P1-3 · market | `combo:RC-PC-P1-3#market#price · combo:RC-PC-P5-3#market#price` | combos(쁘띠시술 · I-11 · market,recovery,checks,dose) | **C7′** | 조합 price fact id(C7′ · 모든 의도) |
| 26 | Q025 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-KEL · checks | `K8-0253 · K8-0259` | combos(쁘띠시술 · I-11 · market,recovery,checks,dose) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 27 | Q026 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | combo:RC-PC-P5-1 · market | `combo:RC-PC-P5-1#market#price` | combos(concern:P5, menu:색소/미백 · — · —) | **C7′** | 조합 price fact id(C7′ · 모든 의도) |
| 28 | Q026 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev n | combo:RC-PC-P5-1 · market | `combo:RC-PC-P5-1#market#price` | combos(concern:P5 · I-11 · checks,safety.pih,recovery,evidence) | **C7′** | 조합 price fact id(C7′ · 모든 의도) |
| 29 | Q027 | case2 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M1 · timeline | `botox#phases[3].normal[1]` | procedure_card(product:M1-2-1 · — · timeline,recovery)<br>recommend(['concern:auto-80-1774737181584'] · — · timeline)<br>procedure_card(unit_procedure:U5-001 · I-01 · timeline)<br>procedure_card(unit_procedure:U5-001 · — · recovery,overview)<br>combos(unit_procedure:U5-001 · — · recovery) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 30 | Q028 | case3 | 정확성 | 경로가 그 노드에 안 닿음 | combo:RC-PC-P2-1 · evidence | `combo:RC-PC-P2-1#evidence#effect.clinicalRationale` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 31 | Q031 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | product:M1-2-1 · aftercare | `product:M1-1-1#aftercare#extracted[M1-1-1].source_text.aftercare[5] · product:M1-1-2#aftercare#extracted[M1-1-2].source_text.aftercare[3]` | pair_check(['product:M1-2-1'] · — · —)<br>pair_check(['family:M1'] · — · timeline,recovery) | **§5-14′** | 묶음 밖 section(aftercare) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 32 | Q031 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PRIOR · checks | `K8-0019 · requires_check:K8-0019:C-PRIOR` | pair_check(['product:M1-2-1'] · — · —)<br>pair_check(['family:M1'] · — · timeline,recovery) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 33 | Q039 | case3 | 질문에 답함 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-PC-P7-1 · evidence | `combo:RC-PC-P7-1#evidence#effect.riskBenefit` | compare(['unit_procedure:U5-009', 'product:M1-2-1'] · I-06 · method,overview) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 34 | Q042 | case3 | 정확성 | 쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍 | procedure_relation:E8-0005 · evidence | `R8-0001 · R8-0005` | compare(['product:M1-2-1', 'family:M2'] · I-06 · method,overview,recovery) | **C3′** | 입력 노드(펼친 단위 포함)에 닿는 procedure_relation 전부 id + claims id(relations_all) |
| 35 | Q042 | case3 | 안전 | slim 카드 밖 섹션(section 안 요청) · Jev n | combo:RC-CP-wrinkle · evidence | `combo:RC-CP-wrinkle#evidence#members[1].attrs_text.limitations` | compare(['product:M1-2-1', 'family:M2'] · I-06 · method,overview,recovery) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 36 | Q050 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | family:M2 · disclosure | `family:M2#disclosure#family_text[필수 고지(consent mandatory_disclosures)][2]` | procedure_card(family:M2 · — · —) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 37 | Q054 | case2 | 질문에 답함 | 조합(CC · 레시피) fact — combos 안 부름 | CC P4:바이오스티뮬레이터시술 속성(원소 1개 — 쌍 아님) · evidence | `CC P4:바이오스티뮬레이터시술 속성(원소 1개 — 쌍 아님)#evidence#attrs[11]` | procedure_card(family:M2 · — · timeline,recovery) | **C14′** | CC 속성 attrs[11](F-B) — 계열 카드 C14′ = 단위 시술에 붙은 메모 · CC 속성 id 전부 |
| 38 | Q056 | case2 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0064 · evidence | `R8-0168` | pair_check(['family:M2', 'family:M8'] · — · —) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 39 | Q056 | case3 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0064 · evidence | `R8-0162` | pair_check(['family:M2', 'family:M8'] · I-07 · timeline,aftercare,checks,recovery) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 40 | Q057 | case3 | 안전 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M4 · overview | `family:M4#overview#family_text[환자 설명 가이드(patient-education)][0].common_concerns[1].a` | compare(['product:M4-1-1', 'unit_procedure:U5-018'] · I-06 · overview,method,products) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 41 | Q060 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PREG · checks | `K8-0139 · K8-0145` | procedure_card(family:M4 · I-05 · method,evidence,overview,timeline) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 42 | Q066 | case3 | 안전 | 경로가 그 노드에 안 닿음 | check_condition:C-ALLERGY · checks | `K8-0160 · requires_check:K8-0160:C-ALLERGY` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 43 | Q066 | case3 | 질문에 답함 | 경로가 그 노드에 안 닿음 | family:M4 · overview | `family:M4#overview#family_text[환자 설명 가이드(patient-education)][0].common_concerns[1].a` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 44 | Q067 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | unit_procedure:U5-090 · market | `unit_procedure:U5-090#market#market[3]` | compare(['product:M3-4-1', 'family:M2'] · — · —)<br>procedure_card(product:M3-4-1 · — · overview,method,recovery) | **§5-14′** | 묶음 밖 section(market) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 45 | Q067 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev 상 | combo:RC-CP-rejuvenation · evidence | `combo:RC-CP-rejuvenation#evidence#members[0].attrs_text.duration` | compare(['product:M3-4-1', 'unit_procedure:U5-090'] · I-06 · method,overview,products,recovery) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 46 | Q068 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | family:M4 · timeline | `skin-booster#phases[1].caution[0]` | check_conditions(family:M4 · — · safety.complications,safety.side_effects,emergency,aftercare)<br>procedure_card(family:M4 · — · emergency) | **§5-14′** | 묶음 밖 section(timeline) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 47 | Q069 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-ANTICOAG · checks | `K8-0144 · K8-0150` | compare(['unit_procedure:U5-020', 'product:M4-1-1', 'unit_procedure:U5-018'] · I-06 · overview,method) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 48 | Q070 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev 상 | family:M4 · disclosure | `family:M4#disclosure#family_text[필수 고지(consent mandatory_disclosures)][0]` | check_conditions(family:M4 · I-09 · checks,safety.side_effects,method,overview) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 49 | Q072 | case2 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-PC-P3-1 · evidence | `combo:RC-PC-P3-1#evidence#effect.clinicalRationale` | compare(['product:M9-1-1', 'product:M9-1-3'] · — · overview,method) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 50 | Q072 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-PC-P3-1 · evidence | `combo:RC-PC-P3-1#evidence#effect.clinicalRationale` | compare(['product:M9-1-1', 'product:M9-1-2', 'unit_procedure:U5-102', 'unit_pr · I-06 · method,overview,evidence) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 51 | Q072 | case3 | 안전 | slim 카드 밖 섹션(section 안 요청) · Jev n | family:M9 · checks | `K8-0303 · family:M9#checks#family_text[상담 · 준비 · 고지 · 조건 아닌 문장(확인 조건 엣지 아님)][1]` | compare(['product:M9-1-1', 'product:M9-1-2', 'unit_procedure:U5-102', 'unit_pr · I-06 · method,overview,evidence) | **§5-14′** | 묶음 밖 section(checks) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 52 | Q073 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | combo:RC-CP-lifting · evidence | `combo:RC-CP-lifting#evidence#members[1].attrs_text.limitations` | compare(['product:M9-1-1', 'unit_procedure:U5-091'] · — · —)<br>procedure_card(unit_procedure:U5-091 · — · evidence) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 53 | Q073 | case2 | 안전 | slim 카드 밖 섹션(section 안 요청) | family:M9 · checks | `K8-0303 · family:M9#checks#family_text[상담 · 준비 · 고지 · 조건 아닌 문장(확인 조건 엣지 아님)][1]` | compare(['product:M9-1-1', 'unit_procedure:U5-091'] · — · —)<br>procedure_card(unit_procedure:U5-091 · — · evidence) | **§5-14′** | 묶음 밖 section(checks) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 54 | Q073 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0297 · K8-0311` | compare(['product:M9-1-1', 'product:M9-1-2', 'unit_procedure:U5-102', 'unit_pr · I-06 · method,overview,recovery,ops) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 55 | Q073 | case3 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) · Jev n | combo:RC-CP-lifting · evidence | `combo:RC-CP-lifting#evidence#members[1].attrs_text.mechanism_simple` | compare(['product:M9-1-1', 'product:M9-1-2', 'unit_procedure:U5-102', 'unit_pr · I-06 · method,overview,recovery,ops) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 56 | Q075 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-METAL · checks | `K8-0075 · K8-0081` | procedure_card(family:M9 · — · recovery,timeline,overview) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 57 | Q078 | case2 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M9 · overview | `family:M9#overview#family_text[환자 설명 가이드(patient-education)][0].pain_level` | procedure_card(family:M9 · — · method,recovery,aftercare,overview)<br>procedure_card(family:M9 · — · method) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 58 | Q081 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | combo:RC-CP-lifting · evidence | `combo:RC-CP-acne#evidence#members[1].attrs_text.duration · combo:RC-CP-body_contouring#evidence#members[3].attrs_text.duration` | compare(['unit_procedure:U5-022', 'unit_procedure:U5-140'] · I-06 · method,overview,recovery,evidence) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 59 | Q081 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-ANTICOAG · checks | `K8-0144 · K8-0150` | compare(['unit_procedure:U5-022', 'unit_procedure:U5-140'] · I-06 · method,overview,recovery,evidence) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 60 | Q082 | case2 | 정확성 | 쌍 관계 fact — pair_check/compare 안 부 | procedure_relation:E8-0221 · evidence | `R8-0136#reason` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 61 | Q082 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | package:P6-09 · evidence | `R8-0028 · R8-0058` | pair_check(['unit_procedure:U5-091', 'unit_procedure:U5-104'] · I-07 · dose,checks,recovery,method) | **N-조항없음** | I-07 에 package evidence 없음 — v3.1 그대로 |
| 62 | Q084 | case3 | 정확성 | 쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍 | procedure_relation:E8-0222 · evidence | `R8-0129#reason` | pair_check(['unit_procedure:U5-091', 'unit_procedure:U5-104', 'product:new-DEV-02 · I-07 · checks,method,dose,site_caution) | **C3′** | 입력 노드(펼친 단위 포함)에 닿는 procedure_relation 전부 id + claims id(relations_all) |
| 63 | Q084 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-METAL · checks | `K8-0189 · K8-0205` | pair_check(['unit_procedure:U5-091', 'unit_procedure:U5-104', 'product:new-DEV-02 · I-07 · checks,method,dose,site_caution) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 64 | Q086 | case2 | 정확성 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[124]` | recommend(['concern:P3'], site:site.jawline · — · —) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 65 | Q086 | case3 | 질문에 답함 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[124]` | combos(concern:auto-88-1774737181584 · I-11 · method,checks,site_caution,overview) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 66 | Q087 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0297 · K8-0311` | compare(['product:M11-1-1', 'unit_procedure:U5-110'] · I-06 · method,overview,recovery) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 67 | Q088 | case2 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | complication:CX-M11-01 · safety.complications | `CX-M11-01#prevention` | procedure_card(family:M11 · I-01 · overview,checks,safety.side_effects,recovery)<br>recommend(['concern:P7-2'] · — · —) | **C6′** | 합병증 잎 fact id 전부(prevention · incidence …) |
| 68 | Q088 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0197 · K8-0204` | procedure_card(family:M11 · I-05 · method,evidence,overview,recovery) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 69 | Q089 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | family:M11 · disclosure | `family:M11#disclosure#family_text[필수 고지(consent mandatory_disclosures)][4]` | procedure_card(unit_procedure:U5-110 · — · overview,checks,evidence) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 70 | Q089 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0297 · K8-0311` | procedure_card(unit_procedure:U5-110 · — · overview,checks,evidence) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 71 | Q089 | case2 | 불확실 | slim 카드 밖 섹션(section 안 요청) | complication:CX-M11-02 · safety.complications | `CX-M11-02#incidence` | procedure_card(unit_procedure:U5-110 · — · overview,checks,evidence) | **C6′** | 합병증 잎 fact id 전부 |
| 72 | Q089 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0297 · K8-0311` | recommend(['concern:P9-1', 'concern:P6', 'concern:P9'], site:site.face · I-01 · evidence,method,overview,checks) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 73 | Q094 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | family:M11 · disclosure | `family:M11#disclosure#family_text[필수 고지(consent mandatory_disclosures)][5]` | procedure_card(family:M11 · — · aftercare,recovery) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 74 | Q095 | case2 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | product:auto-M11-1775360637715 · aftercare | `product:auto-M11-1775360637715#aftercare#extracted[auto-M11-1775360637715].source_text.aftercare[2]` | check_conditions(family:M11 · — · aftercare,recovery,checks)<br>procedure_card(family:M11 · — · aftercare) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 75 | Q095 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | product:auto-M11-1775360637715 · aftercare | `product:auto-M11-1775360637715#aftercare#extracted[auto-M11-1775360637715].source_text.aftercare[2]` | procedure_card(family:M11 · I-03 · aftercare,recovery,timeline,disclosure) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 76 | Q096 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | complication:CX-M11-03 · safety.complications | `CX-M11-03#prevention` | check_conditions(family:M11 · I-09 · safety.side_effects,method,evidence,safety.complications) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 77 | Q097 | case2 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0026 · evidence | `R8-0022#reason` | pair_check(['family:M11', 'family:M8'] · — · —) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 78 | Q097 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0297 · K8-0311` | pair_check(['unit_procedure:U5-110', 'unit_procedure:U5-027'] · I-07 · checks,method,dose,timeline) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 79 | Q101 | case3 | 질문에 답함 | 노드 속성(technique) · 노드에 안 닿음 | technique:K10 · — | `(fact 없음)` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 80 | Q102 | case2 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-pigment · evidence | `combo:RC-CP-pigment#evidence#anchor.subtitle · combo:RC-CP-pigment#evidence#members[1].attrs_text.best_for` | recommend(['concern:P5-1'] · — · —) | **C7′** | 비교 조합 anchor.subtitle · members 잎 id — C7′ refs(원문은 compare) |
| 81 | Q102 | case2 | 질문에 답함 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-pigment · evidence | `combo:RC-CP-pigment#evidence#members[1].attrs_text.limitations` | recommend(['concern:P5-1'] · — · —) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 82 | Q102 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-pigment · evidence | `combo:RC-CP-pigment#evidence#members[1].attrs_text.limitations` | pair_check(['unit_procedure:U5-131', 'unit_procedure:U5-131'] · I-07 · method,site_caution,overview,evidence) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 83 | Q102 | case3 | 질문에 답함 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-pigment · evidence | `combo:RC-CP-pigment#evidence#anchor.subtitle` | pair_check(['unit_procedure:U5-131', 'unit_procedure:U5-131'] · I-07 · method,site_caution,overview,evidence) | **C7′** | 비교 조합 anchor.subtitle id — C7′ refs |
| 84 | Q103 | case2 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M8 · overview | `family:M8#overview#family_text[환자 설명 가이드(patient-education)][0].common_concerns[2].a` | recommend(['concern:P5-1'] · — · overview,recovery,checks) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 85 | Q105 | case2 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) | combo:RC-CP-pigment · evidence | `combo:RC-CP-pigment#evidence#members[1].attrs_text.downtime` | recommend(['concern:P5'] · — · recovery,aftercare) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 86 | Q106 | case3 | 정확성 | 노드 속성(technique) · 노드에 안 닿음 | technique:K04a · — | `(fact 없음)` | compare(['unit_procedure:U5-131', 'unit_procedure:U5-023'] · I-06 · method,overview) | **N-9단계** | technique related_techniques — 골드 fact 없음 · 설명 사실(9단계) |
| 87 | Q109 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-SUN · checks | `K8-0065 · requires_check:K8-0065:C-PRIOR` | procedure_card(family:M8 · I-03 · safety.pih,safety.side_effects,recovery,disclosure) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 88 | Q110 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | family:M8 · disclosure | `family:M8#disclosure#family_text[필수 고지(consent mandatory_disclosures)][2] · unit_procedure:U5-034#aftercare#extracted[M15-1-2].source_text.aftercare[0]` | check_conditions(family:M8 · — · aftercare,safety.pih)<br>recommend(['concern:P5-1'] · — · aftercare,safety.pih)<br>procedure_card(family:M8 · — · aftercare) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 89 | Q110 | case2 | 안전 | slim 카드 밖 섹션(section 안 요청) | complication:CX-M8-01 · safety.complications | `CX-M8-01#prevention · unit_procedure:U5-034#aftercare#extracted[M15-1-2].source_text.aftercare[0]` | check_conditions(family:M8 · — · aftercare,safety.pih)<br>recommend(['concern:P5-1'] · — · aftercare,safety.pih)<br>procedure_card(family:M8 · — · aftercare) | **C6′** | 합병증 잎 fact id 전부 |
| 90 | Q110 | case2 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) | family:M8 · disclosure | `family:M8#disclosure#family_text[필수 고지(consent mandatory_disclosures)][2] · unit_procedure:U5-034#aftercare#extracted[M15-1-2].source_text.aftercare[0]` | check_conditions(family:M8 · — · aftercare,safety.pih)<br>recommend(['concern:P5-1'] · — · aftercare,safety.pih)<br>procedure_card(family:M8 · — · aftercare) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 91 | Q112 | case3 | 정확성 | 쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍 | procedure_relation:E8-0085 · evidence | `R8-0014` | pair_check(['product:M4-1-1', 'unit_procedure:U5-018'] · I-07 · timeline,safety.pih,evidence,recovery) | **C3′** | 입력 노드(펼친 단위 포함)에 닿는 procedure_relation 전부 id + claims id(relations_all) |
| 92 | Q113 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | combo:RC-CP-pigment · evidence | `combo:RC-CP-acne#evidence#members[2].attrs_text.cost_range · combo:RC-CP-pigment#evidence#members[3].attrs_text.cost_range` | recommend(['concern:P5-2'] · — · —) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 93 | Q113 | case3 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) · Jev 상 | combo:RC-CP-acne · evidence | `combo:RC-CP-acne#evidence#members[2].attrs_text.cost_range · combo:RC-CP-pigment#evidence#members[3].attrs_text.cost_range` | compare(['unit_procedure:U5-024', 'unit_procedure:U5-023'] · I-06 · method,recovery,checks,overview) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 94 | Q115 | case2 | 정확성 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[138] · scope:all#evidence#step8_notes[139]` | check_conditions(family:M8 · — · safety.side_effects,safety.complications,safety.pih,emergency) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 95 | Q117 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-acne · evidence | `combo:RC-CP-acne#evidence#members[4].attrs_text.limitations` | pair_check(['family:M8', 'family:M8'] · I-07 · method,evidence,overview,checks) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 96 | Q118 | case3 | 질문에 답함 | 노드 속성(concern) · 노드에 안 닿음 | concern:P6-3 · — | `(fact 없음)` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 97 | Q121 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev n | family:M8 · overview | `ST-M8-effects-01#patient.ko` | recommend(['concern:P6'], site:site.face · I-01 · method,evidence,checks,timeline) | **§5-14′** | 묶음 밖 section(overview) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 98 | Q121 | case3 | 질문에 답함 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | combo:RC-CP-acne · evidence | `combo:RC-CP-acne#evidence#members[4].attrs_text.best_for` | recommend(['concern:P6'], site:site.face · I-01 · method,evidence,checks,timeline) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 99 | Q122 | case3 | 질문에 답함 | 노드 속성(concern) · 노드에 안 닿음 | concern:P6-3 · — | `(fact 없음)` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 100 | Q124 | case2 | 질문에 답함 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | product:M8-4-1 · safety.side_effects | `product:M8-4-1#safety.side_effects#extracted[M8-4-1].source_text.safety.common[2] · product:M8-4-1#safety.side_effects#product_links[M8-4-1].side_effect_override[0].values.common[2]` | check_conditions(family:M8 · — · safety.side_effects)<br>recommend(['concern:P8-2'] · — · safety.side_effects) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 101 | Q124 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | product:M8-4-1 · safety.side_effects | `product:M8-4-1#safety.side_effects#extracted[M8-4-1].source_text.safety.common[2] · product:M8-4-1#safety.side_effects#product_links[M8-4-1].side_effect_override[0].values.common[2]` | procedure_card(family:M8 · I-04 · safety.side_effects,recovery,safety.complications,method) | **N-제품수준** | 계열 카드에 제품(M8-4-1) 수준 원문 — 2-hop(걸음 측정 §6-6 에만) |
| 102 | Q124 | case3 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) · Jev n | product:M8-4-1 · aftercare | `product:M8-4-1#aftercare#extracted[M8-4-1].source_text.aftercare[5] · product:M8-4-2#aftercare#extracted[M8-4-2].source_text.aftercare[5]` | procedure_card(family:M8 · I-04 · safety.side_effects,recovery,safety.complications,method) | **N-제품수준** | 계열 카드에 제품(M8-4-1) 수준 원문 — 2-hop |
| 103 | Q125 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | product:M8-4-1 · aftercare | `product:M8-4-1#aftercare#extracted[M8-4-1].source_text.aftercare[0]` | procedure_card(family:M8 · I-04 · recovery,safety.side_effects,timeline,aftercare) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 104 | Q126 | case2 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | check_condition:C-DERM · checks | `K8-0230 · requires_check:K8-0230:C-DERM` | check_conditions(unit_procedure:U5-030 · — · checks) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 105 | Q127 | case2 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-OP-Acne-경미 · timeline | `combo:RC-OP-Acne-경미#timeline#sessions` | recommend(['concern:P6'] · — · timeline,dose) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 106 | Q129 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | family:M8 · disclosure | `family:M8#disclosure#family_text[필수 고지(consent mandatory_disclosures)][2] · unit_procedure:U5-034#aftercare#extracted[M15-1-2].source_text.aftercare[0]` | procedure_card(family:M8 · — · aftercare,recovery)<br>recommend(['concern:P8-2'] · — · aftercare) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 107 | Q132 | case3 | 질문에 답함 | 쌍 관계 fact — pair_check/compare 안 부 | procedure_relation:E8-0195 · evidence | `R8-0338#reason · R8-0339#reason` | procedure_card(family:M8 · I-02 · method,evidence,overview) | **C3′** | 카드 · checks 응답의 C3′ = 닿는 procedure_relation 엣지 id · claims id 전부(종류 무관) |
| 108 | Q134 | case2 | 정확성 | 쌍 관계 fact — pair_check/compare 안 부 | procedure_relation:E8-0081 · evidence | `R8-0013` | procedure_card(family:M8 · — · overview,method) | **C3′** | 카드 · checks 응답의 C3′ = 닿는 procedure_relation 엣지 id · claims id 전부(종류 무관) |
| 109 | Q135 | case2 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M8 · recovery | `family:M8#recovery#family_text[환자 설명 가이드(patient-education)][0].downtime` | procedure_card(family:M8 · — · recovery,aftercare) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 110 | Q135 | case2 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) | family:M8 · evidence | `ST-M8-adverse_effects-01#patient.ko · ST-M8-effects-02#patient.ko` | procedure_card(family:M8 · — · recovery,aftercare) | **§5-14′** | 묶음 밖 section(evidence) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 111 | Q135 | case3 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) · Jev n | combo:RC-PC-P9-1 · evidence | `combo:RC-PC-P9-1#evidence#effect.riskBenefit` | procedure_card(family:M8 · I-05 · recovery,timeline,ops,site_caution) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 112 | Q136 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | unit_procedure:U5-028 · timeline | `chemical-peel-mid#phases[3].normal[2] · fractional-co2#phases[4].normal[3]` | procedure_card(family:M8 · — · aftercare,recovery) | **§5-14′** | 묶음 밖 section(timeline) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 113 | Q136 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | unit_procedure:U5-028 · timeline | `chemical-peel-mid#phases[3].normal[2] · fractional-co2#phases[4].normal[3]` | procedure_card(family:M8 · I-03 · timeline,aftercare,recovery,safety.pih) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 114 | Q138 | case2 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-skin_texture · evidence | `combo:RC-CP-skin_texture#evidence#evidence_notes[1]` | recommend(['concern:P9'] · — · —)<br>recommend(['concern:P7'] · — · —) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 115 | Q138 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-skin_texture · evidence | `combo:RC-CP-skin_texture#evidence#evidence_notes[1]` | check_conditions(family:M8 · I-09 · method,site_caution,evidence,checks) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 116 | Q138 | case3 | 질문에 답함 | 쌍 관계 fact — pair_check/compare 안 부 | procedure_relation:E8-0196 · evidence | `R8-0220 · R8-0221` | check_conditions(family:M8 · I-09 · method,site_caution,evidence,checks) | **C3′** | 카드 · checks 응답의 C3′ = 닿는 procedure_relation 엣지 id · claims id 전부(종류 무관) |
| 117 | Q139 | case3 | 정확성 | 노드 속성(combo · full 카드 전용) | combo:RC-OP-Acne-중등도 · — | `R8-0218 · R8-0219` | pair_check(['unit_procedure:U5-045', 'unit_procedure:U5-045'] · I-07 · method,evidence,dose) | **C3′** | R8-0218 · 0219 = 쌍 claims id 전부 |
| 118 | Q139 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-ACNE · checks | `K8-0001 · scope:all#evidence#step8_notes[25]` | pair_check(['unit_procedure:U5-045', 'unit_procedure:U5-045'] · I-07 · method,evidence,dose) | **C2′** | K8-0001 (C-ACNE) id 전부 |
| 119 | Q139 | case3 | 질문에 답함 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | combo:RC-OP-Acne-중등도 · evidence | `combo:RC-OP-Acne-중등도#evidence#rationale` | pair_check(['unit_procedure:U5-045', 'unit_procedure:U5-045'] · I-07 · method,evidence,dose) | **C7′** | RC-OP 조합 rationale → C7′ refs id |
| 120 | Q140 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | family:M8 · disclosure | `family:M8#disclosure#family_text[필수 고지(consent mandatory_disclosures)][3]` | check_conditions(family:M8 · — · safety.side_effects,safety.pih,aftercare,emergency)<br>recommend(['concern:P9'] · — · safety.side_effects,safety.pih,emergency)<br>procedure_card(family:M8 · — · emergency)<br>procedure_card(family:M8 · I-05 · safety.side_effects,safety.complications,recovery)<br>neighbors(complication:CX-M8-01 · — · safety.pih) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 121 | Q140 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | unit_procedure:U5-028 · timeline | `fractional-co2#phases[4].normal[1]` | procedure_card(family:M8 · I-04 · recovery,safety.side_effects,timeline,method) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 122 | Q141 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev 상 | check_condition:C-KEL · checks | `K8-0291 · requires_check:K8-0291:C-KEL` | check_conditions(family:M8 · I-09 · safety.side_effects,safety.complications,method,evidence) | **C2′** | 확인 조건 주장 id 전부 |
| 123 | Q147 | case2 | 정확성 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[190] · scope:all#evidence#step8_notes[191]` | pair_check(['family:M8'] · — · —)<br>procedure_card(family:M8 · — · timeline,recovery,overview) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 124 | Q147 | case3 | 정확성 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[190] · scope:all#evidence#step8_notes[191]` | procedure_card(family:M8 · I-10 · recovery,dose,method,timeline) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 125 | Q148 | case2 | 정확성 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[190] · scope:all#evidence#step8_notes[191]` | procedure_card(family:M8 · — · overview,evidence,recovery) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 126 | Q148 | case2 | 질문에 답함 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[190] · scope:all#evidence#step8_notes[191]` | procedure_card(family:M8 · — · overview,evidence,recovery) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 127 | Q148 | case3 | 정확성 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[190] · scope:all#evidence#step8_notes[191]` | procedure_card(family:M8 · I-05 · recovery,method,evidence,overview) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 128 | Q149 | case2 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-OP-Hair-경미 · evidence | `combo:RC-OP-Hair-경미#evidence#rationale` | recommend(['concern:P10'] · — · checks,overview) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 129 | Q149 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-FITZ · checks | `K8-0295 · requires_check:K8-0295:C-FITZ` | recommend(['concern:P10'] · — · checks,overview) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 130 | Q149 | case3 | 질문에 답함 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-CP-hair_removal · evidence | `combo:RC-CP-hair_removal#evidence#members[2].attrs_text.limitations` | procedure_card(family:M8 · I-02 · method,evidence,overview) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 131 | Q150 | case2 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | unit_procedure:U5-023 · safety.pih | `unit_procedure:U5-023#safety.pih#pih[3].fitzpatrick_note · unit_procedure:U5-099#safety.pih#pih[2].fitzpatrick_note` | check_conditions(family:M8 · — · checks,site_caution,safety.pih)<br>recommend(['concern:P10'] · — · checks,safety.pih)<br>check_conditions(unit_procedure:U5-100 · — · checks,safety.pih,site_caution) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 132 | Q156 | case2 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0123 · evidence | `R8-0147#reason · R8-0150#reason` | recommend(['concern:P10'] · — · timeline)<br>pair_check(['family:M8'] · — · —) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 133 | Q159 | case3 | 정확성 | step8 메모(step8_notes) fact — 어느 노드 | scope:all · evidence | `scope:all#evidence#step8_notes[190] · scope:all#evidence#step8_notes[191]` | procedure_card(family:M8 · I-10 · dose,site_caution,recovery,method) | **C14′** | 계열 · 제품 카드 C14′ = 그 계열 단위 시술에 붙은 step8 메모 id 전부(F-A ②) |
| 134 | Q162 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-DERM · checks | `K8-0230 · requires_check:K8-0230:C-DERM` | compare(['unit_procedure:U5-034', 'unit_procedure:U5-027'] · I-06 · method,overview,recovery) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 135 | Q163 | case2 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) | family:M15 · disclosure | `family:M15#disclosure#family_text[필수 고지(consent mandatory_disclosures)][0]` | procedure_card(family:M15 · — · recovery,aftercare,safety.side_effects)<br>check_conditions(family:M15 · — · recovery) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 136 | Q164 | case3 | 질문에 답함 | 경로가 그 노드에 안 닿음 | family:M15 · recovery | `family:M15#recovery#family_text[환자 설명 가이드(patient-education)][0].downtime` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 137 | Q165 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | unit_procedure:U5-034 · safety.pih | `unit_procedure:U5-034#safety.pih#pih[2].fitzpatrick_note` | procedure_card(family:M15 · — · recovery,aftercare,overview)<br>neighbors(family:M15 · — · none)<br>recommend(['concern:P6-2'] · — · recovery)<br>procedure_card(unit_procedure:U5-034 · — · recovery,timeline) | **§5-14′** | 묶음 밖 section(safety.pih) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 138 | Q165 | case2 | 안전 | slim 카드 밖 섹션(section 안 요청) | unit_procedure:U5-034 · safety.pih | `unit_procedure:U5-034#safety.pih#pih[1].fitzpatrick_note` | procedure_card(family:M15 · — · recovery,aftercare,overview)<br>neighbors(family:M15 · — · none)<br>recommend(['concern:P6-2'] · — · recovery)<br>procedure_card(unit_procedure:U5-034 · — · recovery,timeline) | **§5-14′** | 묶음 밖 section(safety.pih) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 139 | Q165 | case3 | 정확성 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M15 · timeline | `chemical-peel-mid#phases[3].normal[0]` | procedure_card(family:M15 · I-05 · recovery,timeline,ops,evidence) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 140 | Q165 | case3 | 질문에 답함 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | family:M15 · recovery | `family:M15#recovery#family_text[환자 설명 가이드(patient-education)][0].downtime` | procedure_card(family:M15 · I-05 · recovery,timeline,ops,evidence) | **F-F** | 섹션 매핑 밖 24 — fact id 열거 · 같은 입력으로 응답에 있어야 함 |
| 141 | Q166 | case3 | 질문에 답함 | 경로가 그 노드에 안 닿음 | family:M15 · disclosure | `family:M15#disclosure#family_text[필수 고지(consent mandatory_disclosures)][2]` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 142 | Q167 | case3 | 질문에 답함 | 경로가 그 노드에 안 닿음 | family:M15 · overview | `family:M15#overview#family_text[환자 설명 가이드(patient-education)][0].common_concerns[0].a` | procedure_card(family:M2 · I-03 · method,timeline,overview,safety.pih) | **N-다른계열** | M2 카드에 M15 overview — 응답 노드와 다른 계열 |
| 143 | Q169 | case3 | 정확성 | 엣지 속성 — 양끝 도달 | product_family:000253 · — | `product_family:000253#overview#basis · product_family:000253` | check_conditions(family:M15 · I-09 · checks,safety.side_effects,method,dose) | **C4′** | product_family basis fact id 를 C4 제품 행에 |
| 144 | Q170 | case2 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) | family:M15 · overview | `family:M15#overview#family_text[환자 설명 가이드(patient-education)][0].common_concerns[1].a` | check_conditions(family:M15 · — · safety.side_effects,safety.complications,recovery,checks) | **§5-14′** | 묶음 밖 section(overview) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 145 | Q170 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev 상 | family:M15 · recovery | `family:M15#recovery#family_text[환자 설명 가이드(patient-education)][0].duration_simple` | procedure_card(family:M15 · I-04 · method,safety.side_effects,evidence,dose) | **§5-14′** | 묶음 밖 section(recovery) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 146 | Q172 | case2 | 안전 | 경로가 그 노드에 안 닿음 | complication:CX-M11-01 · safety.complications | `CX-M11-01#prevention` | check_conditions(family:M15 · — · checks) | **N-다른계열** | M15 checks 에 M11 합병증 |
| 147 | Q172 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-ISO · checks | `K8-0232` | pair_check(['unit_procedure:U5-034', 'unit_procedure:U5-034'] · I-07 · checks,evidence,method,dose) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 148 | Q175 | case3 | 안전 | slim 카드 밖 섹션(section 안 요청) · Jev n | family:M15 · disclosure | `family:M15#disclosure#family_text[필수 고지(consent mandatory_disclosures)][1] · unit_procedure:U5-034#safety.pih#pih[1].source` | recommend(['concern:P9'] · I-01 · method,evidence,overview,recovery) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 149 | Q176 | case3 | 정확성 | 경로가 그 노드에 안 닿음 | family:M15 · disclosure | `family:M15#disclosure#family_text[필수 고지(consent mandatory_disclosures)][1] · unit_procedure:U5-034#safety.pih#pih[1].source` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 150 | Q178 | case2 | 안전 | slim 카드 밖 섹션(section 안 요청) | family:M2 · disclosure | `family:M2#disclosure#family_text[필수 고지(consent mandatory_disclosures)][0]` | procedure_card(family:M7 · — · overview,checks)<br>procedure_card(family:M2 · — · overview,checks) | **§5-14′** | 묶음 밖 section(disclosure) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 151 | Q184 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PREG · checks | `K8-0139 · K8-0145` | procedure_card(family:M7 · I-05 · recovery,method,evidence,overview) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 152 | Q185 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | unit_procedure:U5-022 · aftercare | `product:M7-3-1#aftercare#extracted[M7-3-1].source_text.aftercare[3] · product:M7-3-2#aftercare#extracted[M7-3-2].source_text.aftercare[4]` | pair_check(['family:M7'] · — · —) | **§5-14′** | 묶음 밖 section(aftercare) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 153 | Q185 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-RE-R2 · evidence | `combo:RC-RE-R2#evidence#effect.repeatCycle · combo:RC-RE-R6#evidence#effect.repeatCycle` | pair_check(['family:M7', 'family:M7'] · I-07 · method,dose,recovery,checks) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 154 | Q189 | case2 | 정확성 | 노드 속성(combo) · 노드에 안 닿음 | combo:RC-OP-Acne-중등도 · — | `(fact 없음)` | check_conditions(family:M7 · — · safety.side_effects,safety.complications,emergency,aftercare)<br>procedure_card(family:M7 · — · safety.complications)<br>procedure_card(family:M7 · — · safety.side_effects) | **N-9단계** | complications.management — A 그룹 성격(V-4) |
| 155 | Q189 | case3 | 정확성 | 노드 속성(combo) · 노드에 안 닿음 | combo:RC-OP-Acne-중등도 · — | `(fact 없음)` | procedure_card(family:M7 · I-04 · safety.side_effects,safety.complications,timeline,method) | **N-9단계** | complications.management — A 그룹 성격(V-4) |
| 156 | Q191 | case2 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0112 · evidence | `R8-0098` | compare(['family:M7', 'family:M9'] · — · —) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 157 | Q191 | case2 | 질문에 답함 | slim 카드 밖 섹션(section 안 요청) | combo:RC-CP-lifting · evidence | `combo:RC-CP-lifting#evidence#members[2].attrs_text.best_for · thread-lift#phases[0].normal[0]` | compare(['family:M7', 'family:M9'] · — · —) | **C7′** | 비교 조합 members 잎 id — C7′ refs(compare 에선 C10 원문) |
| 158 | Q191 | case3 | 질문에 답함 | 섹션 요청했는데도 응답에 없음(section 매핑 밖) | combo:RC-CP-lifting · evidence | `combo:RC-CP-lifting#evidence#evidence_notes[2]` | compare(['unit_procedure:U5-091', 'unit_procedure:U5-104'] · I-06 · method,overview,recovery,evidence) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 159 | Q192 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | combo:RC-CP-body_contouring · evidence | `combo:RC-CP-body_contouring#evidence#members[3].attrs_text.limitations` | recommend(['concern:P12'], site:site.body · — · —) | **C7′** | 조합 잎 fact id(refs) — 비교 멤버 원문은 compare 만(C10′) |
| 160 | Q192 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-BMI · checks | `K8-0110 · requires_check:K8-0110:C-BMI` | procedure_card(family:M9 · I-05 · evidence,method,overview) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 161 | Q192 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PACE · checks | `K8-0297 · K8-0311` | procedure_card(family:M9 · I-05 · evidence,method,overview) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 162 | Q193 | case2 | 정확성 | 엣지 속성 — 양끝 도달 | treats:0256 · — | `treats:0256#evidence#row.evidence.role · treats:0256` | recommend(['concern:P12-4'] · — · overview,evidence) | **C3′** | treats role fact id 를 recommend why[] 에 |
| 163 | Q197 | case3 | 정확성 | 경로가 그 노드에 안 닿음 | check_condition:C-SURG · checks | `K8-0226 · requires_check:K8-0226:C-SURG` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 164 | Q197 | case3 | 안전 | 경로가 그 노드에 안 닿음 | check_condition:C-METAL · checks | `K8-0196 · K8-0205` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 165 | Q197 | case3 | 질문에 답함 | 경로가 그 노드에 안 닿음 | check_condition:C-PRIOR · checks | `K8-0199 · requires_check:K8-0199:C-PRIOR` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 166 | Q198 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | unit_procedure:U5-153 · overview | `unit_procedure:U5-153#overview#sources[0].detail` | recommend(['concern:P14-3'], site:site.axilla · I-01 · —)<br>compare(['unit_procedure:U5-010', 'unit_procedure:U5-153'] · — · —) | **§5-14′** | unit sources[0].detail(overview) — recommend 카드 묶음 밖 id 노출(I-01 은 n 만) → 같은 문항 compare 호출에서 id |
| 167 | Q198 | case3 | 정확성 | 조합(CC · 레시피) fact — combos 안 부름 | treats:0267 · evidence | `treats:0267#evidence#row.evidence.role · treats:0267` | compare(['unit_procedure:U5-010', 'unit_procedure:U5-011', 'unit_procedure:U5- · I-06 · method,recovery,checks,safety.side_effects) | **C3′** | treats role fact id — compare 입력 단위의 treats 엣지 id(why) · F-C |
| 168 | Q198 | case3 | 질문에 답함 | 이웃 노드(1-hop) — 도구가 안 펼침 | unit_procedure:U5-153 · overview | `unit_procedure:U5-153#overview#sources[0].detail` | compare(['unit_procedure:U5-010', 'unit_procedure:U5-011', 'unit_procedure:U5- · I-06 · method,recovery,checks,safety.side_effects) | **§5-14′** | unit sources[0].detail — compare 입력 노드 overview 는 I-06 묶음 안 · 상한 4 → 원문 또는 more_ids |
| 169 | Q200 | case2 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0077 · evidence | `R8-0154 · R8-0154#reason` | pair_check(['unit_procedure:U5-140', 'family:M2'] · — · —) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 170 | Q200 | case3 | 정확성 | 쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍 | procedure_relation:E8-0077 · evidence | `R8-0154 · R8-0154#reason` | pair_check(['product:auto-40-1774737181584', 'unit_procedure:U5-140'] · I-07 · checks,recovery,evidence,method) | **C3′** | 입력 노드(펼친 단위 포함)에 닿는 procedure_relation 전부 id + claims id(relations_all) |
| 171 | Q201 | case2 | 정확성 | 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요 | procedure_relation:E8-0072 · evidence | `R8-0143#reason` | pair_check(['family:M8', 'family:M2'] · — · —) | **C9′** | 쌍 claims · reasons(#reason) id 전부 |
| 172 | Q204 | case3 | 안전 | 경로가 그 노드에 안 닿음 | complication:CX-M2-06 · safety.complications | `CX-M2-06#prevention · CX-M7-03#risk_factors[1]` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 173 | Q204 | case3 | 질문에 답함 | 경로가 그 노드에 안 닿음 | complication:CX-M11-03 · safety.complications | `CX-M11-03#prevention` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 174 | Q212 | case2 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-PC-P3-1 · evidence | `combo:RC-PC-P3-1#evidence#effect.clinicalRationale` | compare(['product:M9-1-3', 'product:M9-1-1'] · — · overview,recovery,dose,evidence) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 175 | Q212 | case2 | 질문에 답함 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-PC-P3-1 · evidence | `combo:RC-PC-P3-1#evidence#effect.riskBenefit` | compare(['product:M9-1-3', 'product:M9-1-1'] · — · overview,recovery,dose,evidence) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 176 | Q212 | case3 | 정확성 | 이웃 노드(1-hop) — 도구가 안 펼침 | combo:RC-PC-P3-1 · evidence | `combo:RC-PC-P3-1#evidence#effect.riskBenefit` | compare(['product:M9-1-3', 'unit_procedure:U5-102', 'unit_procedure:U5-103'] · I-06 · method,recovery,overview,evidence) | **C7′** | 조합 id 전부 + 잎 fact id(refs) · 응답 색인 |
| 177 | Q215 | case2 | 정확성 | scope(claim) fact · 대상 대상 노드 없음 | scope:all · evidence | `scope:all#evidence#sequence_rank[1]` | procedure_card(unit_procedure:U5-018 · — · timeline,method,ops)<br>procedure_card(product:M4-1-1 · — · timeline,method,ops) | **C3′** | 전역 sequence_rank 메모 id — companion.relations.global |
| 178 | Q215 | case3 | 정확성 | scope(claim) fact · 대상 대상 노드 없음 | scope:all · evidence | `scope:all#evidence#sequence_rank[1]` | procedure_card(product:M4-1-1 · I-05 · ops,method,products,overview) | **C3′** | 전역 sequence_rank 메모 id — companion.relations.global |
| 179 | Q216 | case2 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-DM · checks | `K8-0264 · K8-0345` | procedure_card(family:M4 · — · ops,method,recovery) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 180 | Q216 | case3 | 안전 | 이웃 노드(1-hop) — 도구가 안 펼침 | check_condition:C-PREG · checks | `K8-0139 · K8-0145` | procedure_card(family:M4 · I-05 · ops,method) | **C2′** | 확인 조건 주장 id 전부(전 등급 · 계열 상속 포함) |
| 181 | Q228 | case2 | 정확성 | 노드 속성(product) · 노드에 안 닿음 | product:auto-M15-1775401780659 · — | `(fact 없음)` | recommend(['concern:P10'], site:site.face · — · overview,safety.side_effects,evidence) | **N-조항없음** | product 1_identity.basis — v3.1 그대로 |
| 182 | Q235 | case2 | 정확성 | slim 카드 밖 섹션(section 안 요청) | product:auto-39-1774737181584 · safety.side_effects | `product:auto-39-1774737181584#safety.side_effects#extracted[auto-39-1774737181584].source_text.safety.serious[2] · product:auto-39-1774737181584#safety.side_effects#product_links[auto-39-1774737181584].side_effect_override[0].values.serious[2]` | check_conditions(family:M9 · — · safety.complications,safety.side_effects,aftercare,recovery)<br>check_conditions(unit_procedure:U5-091 · — · safety.complications,safety.side_effects,aftercare)<br>procedure_card(unit_procedure:U5-091 · — · safety.complications) | **§5-14′** | 묶음 밖 section(safety.side_effects) id 노출 ≤ 4 + n(단일 노드 도구) · 계열 · 제품은 by_unit id |
| 183 | Q237 | case3 | 정확성 | 엣지 속성 — 양끝 도달 | site_caution:SC-nasolabial-M1 · — | `site_caution:SC-nasolabial-M1#site_caution#spec.safe_zone · site_caution:SC-nasolabial-M1` | procedure_card(family:M1 · I-02 · method,evidence,site_caution,checks) | **C1′** | 부위 위험 잎 fact id 전부(spec · vessels · pearls) · 같은 계열 · 부위 체인 |
| 184 | Q237 | case3 | 질문에 답함 | 엣지 속성 — 양끝 도달 | site_caution:SC-nasolabial-M1 · — | `site_caution:SC-nasolabial-M1#site_caution#spec.key_warning · site_caution:SC-nasolabial-M1` | procedure_card(family:M1 · I-02 · method,evidence,site_caution,checks) | **C1′** | 부위 위험 잎 fact id 전부(spec · vessels · pearls) · 같은 계열 · 부위 체인 |
| 185 | Q238 | case3 | 질문에 답함 | 노드 속성(combo) · 노드에 안 닿음 | combo:RC-PC-P1-1 · — | `(fact 없음)` | — | **X0** | 허브 안 부름(resolve · vocab 만 포함) — SPEC-006 몫 |
| 186 | Q239 | case3 | 정확성 | slim 카드 밖 섹션(section 안 요청) · Jev n | complication:CX-M1-05 · safety.complications | `CX-M1-05#incidence` | procedure_card(product:M1-2-1 · I-04 · evidence,method,dose) | **C6′** | 합병증 잎 fact id 전부 |
