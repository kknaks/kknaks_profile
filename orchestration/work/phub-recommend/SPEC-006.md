---
type: spec
id: SPEC-006
title: "hub-evals 실험 앱 — 원장 MCP vs 골드 MCP vs 골드 + Jev · 로컬 프론트 질문 → 세 갈래 동시 실행 · 속도 · 품질 두 층 · 기록"
status: draft
product: procedure-hub
feature: phub-recommend
version: 0.3.15
created_at: 2026-10-30
updated_at: 2026-11-03
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (10-30 「원장도 MCP 로」 · 「hub-evals 결정」 Q-1~Q-8 · 「최종 목표」 · 「hub-evals 는 골드 완성 뒤」 · DEC-001 D-08 · D-11)"
  sources:
    - "reference/2026-10-30-hub-evals/README.md"
    - "orchestration/work/phub-recommend/jev-research.md"
    - "orchestration/work/phub-recommend/SPEC-005.md §5 · §5-12"
  work:
    - "orchestration/work/phub-recommend/WORK-004.md"
    - "orchestration/work/phub-recommend/WORK-006.md"
    - "orchestration/work/phub-recommend/WORK-009.md"
  evals:
    - "reference/2026-10-30-hub-evals/build-out/fail-triage2.md §2 · §5(case2 잘림 100/614 · intent 2.1%)"
    - "orchestration/work/phub-recommend/cli-research.md · phub-recommend-jev-walk-addendum.md(11-01 사용자 결정)"
    - "reference/2026-10-30-hub-evals/build-out/work006-report.md · verify-b202611011148-c6ed3a.md · rerun-v4-vs-v3.md(rerun-v4 · 182 · 허브 b031371c · 앱 f8533ff)"
    - "orchestration/work/phub-recommend/spec006-v22-count.md · .py(v2.2 · v2.3 근거 셈 · 결정론 · 두 번 같음)"
    - "orchestration/work/phub-recommend/spec006-v23-cover.md · .py(v2.3 셈 E — v2.4 에서 정의가 틀려 대체됨 · 보관)"
    - "orchestration/work/phub-recommend/review-v33-v22-report.md(검수 F-1~F-3 · W-9~W-16)"
    - "orchestration/work/phub-recommend/spec006-v24-recount.md · .py(v2.4 — 받는 자리 정의 하나로 순서 표 · 34 행 다시 · backend venv · 결정론)"
    - "orchestration/work/phub-recommend/review-spec006-v2.3-report.md(재검수 F-1 · F-2 · W-1~W-7)"
---

# SPEC-006 — hub-evals 실험 앱

> **0.3.15 2026-11-03 — active scope 수집·적용 계약(구현 전).** §3-4-1-9가 attachment와 실제 답 scope, 단계별 완료·unknown/hold의 정본이다. Hub SPEC-005 0.3.10 §5-16-1과 짝 의존하며 §3-4-1-8의 의미·필수 coverage·전달 gate는 유지한다. R01/R02/R03 한정 PASS는 전체 context/최종 답 성공이 아니다. 과거 판의 실행 상태를 소급 변경하지 않는다.

> **v2.13 2026-11-02(0.3.13) — TypeSafe 공식 primitive 대조.** 여러 노드의 관련성은 후보마다 독립된 `Noul` 질문을 한 `system_one` 요청에 묶어 평가한다. §3-4-1-7의 동일 후보 집합 `pick_1..pick_k` 반복 Choice는 이 판에서 폐기한다. Jev는 구조화된 관련성·종료 판단을 반환하고 앱이 후보·근거·안전·부재를 검증한다. 근거: TypeSafe 공식 `primitives`, `Noul`, `Speculative fan-out`, `Classifying RAG passages` 문서.

> **v2.12 2026-11-02(0.3.12) — Jev는 노드 갈래와 종료를 고른다.** §3-4-1-7이 현행 탐색 선택·페이지 종료 계약이다. §3-4-1-6의 `매 frontier/page마다 Jev Choice 하나`는 Q002 245 Jev 호출·461 Hub 호출·73초 TTFT를 만든 실패 기록이다. 수집 원장·의료 근거·부재 증명 규칙은 유지한다.

> **v2.11 2026-11-02(0.3.11) — Jev가 매 frontier의 관련성·다음 노드·종료를 선택.** §3-4-1-6이 탐색 선택과 종료의 현행 정본이며, §3-4-1-5의 수집 원장·출처/범위·안전/부재 증명 계약은 유지한다. 이전 판의 Jev 첫 이웃만 선택, 등록된 section/page 전수 완료, 고정 depth/바이트 종료와 충돌하면 §3-4-1-6이 우선한다. Q002 실물 290 Hub 호출 중 `safety.side_effects` 133 page, 7개 직접 후보 전수 펼침과 답변 지연이 근거다.

> **v2.10 2026-11-02(0.3.10) — case3 수집·전달 분리 계약, 현 코드 미구현.** §3-4-1-5가 case3 탐색 종료·근거 선별·전달의 현행 정본이다. §3-4-1~4, §3-4-2, §3-4-3, §3-4-4, §3-4-7, §4-4, §7-8~10에서 충돌하는 4걸음 전체 상한, safety/general/full 8/20/15KB 탐색 장부, 예산 80%·Noul `enough`, 예산 초과 배제·fallback 문구는 **0.3.9 이하의 당시 실행·설계 기록**으로만 읽는다. 해당 절의 Hub API 모양·Jev 역할·원문 인용·관계 적용 범위·평가 이력은 충돌하지 않는 범위에서 유지한다. SPEC-005 0.3.9 §5-5/§5-16과 WORK-011의 Hub 읽기 계약은 변경하지 않는다. 현재 `case3.py`/`config.py`는 section 단위 `taken`, 고정 바이트 장부, 걸음·`enough` 중지를 쓰며 이 판을 구현하지 않았다.

> **v2.9 2026-11-02(0.3.9) — 당시 case3 정보 없음 수집 계약, 현 구현 아님**: §3-4-1-4 대상/페이지/관계 상태 기계, §3-4-2 비용, §3-4-4 trace, §3-4-7 부분 답변, §7-10 관문과 OQ를 추가한다. `info-absence-spec-proposal.md` 및 `review-info-absence-spec-proposal-v2.md` F-1~F-3·W-1~W-4와 ignored audit가 근거다. SPEC-005 0.3.9의 관계 읽기 계약과 짝 의존하며 앱 WORK 구현 전이다. 기존 Jev 노드 선택·4걸음·20/8/15KB·안전 우선·D-13b는 유지한다.

> **0.3.9 당시 계약의 우선순위(0.3.10에서는 §3-4-1-5 우선)**: 아래 v2.8·v2.7·v2.5의 「메모가 정본」은 각 변경 당시의 **걸음 중 최초 수집·안전 우선·Jev 역할**에 관한 결정 기록이다. `phub-recommend-walk-fix3.md`의 「남은 예산 채우기 · 아직 안 받은 섹션 · 1쪽」도 당시 fill 규칙에만 적용된다. 0.3.9 당시 페이지 수신과 후속 fill에는 당시 §3-4-1-4 및 SPEC-005 0.3.9 §5-16이 우선했다. 걸음 중 대상 section의 최초 수집은 page 1 한 쪽이고, 걸음 뒤 fill은 채택 응답의 `more`에 따라 의도 묶음의 `page≥2`를 먼저 수집한 뒤 미수신 section의 page 1을 수집한다. 따라서 옛 메모의 1쪽 문구로 후속 fill의 뒤 페이지를 막지 않는다.

> **v2.8 2026-11-01(0.3.8) — 걷기 고침 4(당시 정본 메모 `phub-recommend-walk-fix4.md` · 11-01 사용자 승인 「1번 넣고 돌리자」)**: §3-4-1-3(새) 안전 예산 따로(`SAFETY_BUDGET` 기본 8KB · 20KB 예산 밖) · 순서(안전 예산 먼저 → 일반 예산) · §3-4-4 `walk.safety_budget` · §7-8 확인(v8a 안전 실패 13 행 재생) · 전체 실행 fullrun-v2 · v8a 결과 한 줄. 허브 계약 변경 없음. 당시 안전 우선 결정에서 메모가 이 판보다 우선했다. 0.3.9 당시 페이지·fill 우선순위는 위 0.3.9 문단을 따랐다. v2.7(0.3.7)은 `SPEC-006.v2.7.md` 보관
> **v2.7 2026-11-01(0.3.7) — 걷기 고침 3(당시 정본 메모 `phub-recommend-walk-fix3.md` · 11-01 사용자 승인 · v8a)**: §3-4-1-2(새) 역할 재정의 — **Jev = 의도 · 시작 노드 · 이웃(어디로 갈지)만 · 섹션 양은 규칙** · 바닥 = 의도 묶음 · Jev 는 이웃만 · 남은 예산 채우기 · 「충분」 은 예산 80% 전엔 무시 · §3-4-4 기록 칸 · §7-8 재측정 rerun-v8a · v7a 결과 한 줄. 허브 계약 변경 없음. 당시 걸음·fill 결정에서 메모가 이 판보다 우선했다. 0.3.9 당시 후속 fill은 위 0.3.9 문단을 따랐다. v2.6(0.3.6)은 `SPEC-006.v2.6.md` 보관
> **v2.6 2026-11-01(0.3.6) — I-04 고정 섹션에 `safety.management`**: SPEC-005 0.3.5 G20 이 합병증 관리 · 예방 54 fact 를 `safety.complications` 밖(새 section `safety.management`)으로 옮겨, v3.4 빌드에서 case3 I-04 가 지금 받던 관리 · 예방을 잃는다(검수 `review-spec005-v34-report.md` F-1). §3-4-1-1 규칙 3 의 I-04 에 `safety.management` 추가 · 바꿀 곳 = 앱 `clinic_chat/config.py:80` `walk_fixed_sections_by_intent`(구현은 rerun-v6b 끝난 뒤 앱 워커) · §7-8 회귀 행. v2.5(0.3.5)는 `SPEC-006.v2.5.md` 보관
> **v2.5 2026-11-01(0.3.5) — 걷기 고침 2(당시 정본 메모 `phub-recommend-walk-fix2.md` · 11-01 사용자 승인 「2회차 멈추고 고치자」)**: §3-4-1-1(새) 필수 묶음 · 「충분」 늦추기(예산 50% 미만이면 무시 · 문턱 0.5 → 0.8) · 의도별 고정 섹션 · §3-4-4 기록 칸 · §7-8 재측정 rerun-v6a · v6b · rerun-v5a 결과 한 줄. 허브 계약 변경 없음. 당시 해당 변경에서 메모가 이 판보다 우선했다. 0.3.9 당시 페이지·fill 우선순위는 위 0.3.9 문단을 따랐다. v2.4(0.3.4)는 `SPEC-006.v2.4.md` 보관
> **v2.4 2026-11-01(0.3.4) — 재검수 반영(`review-spec006-v2.3-report.md` F-1 · F-2 · W-1~W-7) · 마지막 판**: 셈 정의를 **「받는 자리」 하나**로 — fact 를 받는 곳 = 그 걸음의 `expand(n, sections=[s])` 가 실제로 내는 줄(`g.section_ids` · 노드 자신의 줄 · 1쪽 12줄 기준). **F-1** 34 행 덮는 셈을 이 정의로 다시: 걸음 1 선택지에 뜸 **v2.3 「19」 → 같은 정의로 9 · v2.4 규칙 12**(0홉·1쪽 4 + 1홉·1쪽 8 · §3-4-8) — 계열 S 의 펼친 단위 fact 7 은 1홉 `key_family` 로 셈(1쪽 안 3 은 뜸 · 1쪽 밖 4 는 못 닿음) · 계열 · 제품 규칙(단위 이웃 종류 늘 더함 · `by_unit` unit id 로 단위 expand — 허브 계약 변경 없음). **F-2** 순서 표를 같은 정의의 1홉·1쪽 행(461 중 120)으로 다시 셈(§3-4-6 · `order_v24`) · 「이웃 먼저」 근거를 1홉·1쪽 26% > 0홉·1쪽 20% 로 고침 · 걸음 1 섹션 2 의도 I-02 · I-03 · I-04 · I-05. 끝 조건(§7-8)은 고친 셈 그대로: 1홉 몫 ≥ 8 · 0홉 몫 보고(W-4). WARN: W-1 섹션 호출 본문 · W-2 · W-3 SPEC-005 문구는 전달 목록(§7-9 X-14) · W-5 · W-6 · W-7. v2.3(0.3.3)은 `SPEC-006.v2.3.md` 보관
> **v2.3 2026-11-01(0.3.3) — 검수 반영(`review-v33-v22-report.md` F-1~F-3 · W-9~W-16)**: **F-1** 바이트 셈 = 허브와 같은 직렬화(compact · 걸음 경로 허브 호출은 `intent` 안 넘김 → peek `bytes` 와 차 0 · SPEC-005 V-17 닫음 · §3-4-1 「예산 B」 · §3-4-2) · **F-2** 원문 예산 `WALK_FULL_BYTE_BUDGET` 12,000 → **15,000**(SPEC-005 §6-7 (e) cut 받기 응답 p95 14,376 · 근거 표 §3-4-6) · **F-3** 「자료에 없다」 case3 68 중 안 닿은 34 를 걸음 규칙이 덮는 셈 표(§3-4-8 새 · `spec006-v23-cover.md`) + 규칙 보강 — 순서 표를 **edge kind 단위 · 1홉 행 90% 덮기**로(key_technique · treats · child_of 등 실제 답이 산 종류가 들어옴 · W-16 해소) · 앞 4 밖은 `expand(neighbor_kinds)` 목록으로 · 시작 노드 섹션이 1위인 의도(I-03 · I-04)는 걸음 1 섹션 2 → **34 중 걸음 1 선택지에 뜨는 행 16 → 19**(끝 조건 §7-8) · 남은 15 = 어느 노드 섹션에도 없는 fact 8(관계 7 · scope 1 — 허브 쪽 X-10) · 2홉+ 5(대기열로만) · 표 밖 종류 2(X-9). WARN: W-9 이름 나눔(「이웃 fact 도달」) · W-10 선택지 라벨에 `n_facts` · `bytes` · W-11 이웃 slim 실측(중앙 250 · p95 1,014)으로 예산 표 다시 · W-12 · W-15 · W-16 · WORK-009 W-13 · W-14. v2.2(0.3.2)는 `SPEC-006.v2.2.md` 보관
> **v2.2 2026-11-01(0.3.2) — case3 걷기 순서 · stray 원인(발주 `phub-recommend-spec006-v22-brief.md` · 배경 `phub-recommend-walk-fix-context.md`)**: §3-4 걸음 규칙 교체(**첫 걸음 = 이웃 먼저** · 의도별 이웃 종류 순서 표 §3-4-6 · 걸음당 섹션 ≤ 2 · peek 바이트로 미리 거름 · 예산 넘는 섹션은 **건너뛰고 계속** · 「충분」 은 fact 1개 이상 모은 뒤 · 시작 노드로 돌아옴 · 마지막에 모은 줄 중 잘린(`cut`) 것만 `fact_ids` 로 원문) · §3-4-7 Claude 에 넘기는 꼴(fact 원문 + 출처 노드 · 허브 줄 순서 = 「use_first」 순) · §3-3 case2 도구 11 · **§3-8(새) stray 15 원인 · 막는 법** · §3-5-1(새) WP-0 결과 반영(Claude 마커 비움 · 바이트 대조 잘림 판정) · §4-4 걸음 · stray 칸 · **§4-5(새) 비교 규칙**(case1 대비 차 · 결정 전 2회 평균) · **§7-8 v2.2 끝 조건 · §7-9 v2.2 아직 안 정한 것** · §7-7 W-3 · W-5 · W-6 처리. 근거 숫자는 전부 `spec006-v22-count.md`(rerun-v4 기록 재생 · 결정론). 당시 허브 쪽 짧은 fact 꼴의 기준은 **SPEC-005 v3.3(0.3.4 · WORK-008 · 다른 planner)**이었다(이 판 작성 중 나와 §3-4-2 에 칸을 맞춤). 현재 계약은 SPEC-005 0.3.9와 아래 §3-4-2를 따른다. v2.1(0.3.1)은 `SPEC-006.v2.1.md` 보관
> 검수 반영 2026-10-30(F-1 · W-1~W-7) — `review-spec006-report.md` · R-1~R-10 사용자 승인(10-30) · U-1 · U-2 사용자 완료 · 레포 세팅 사실(10-30)
> **v2.1 2026-11-01(0.3.1) — 검수 반영(`review-spec006-v2-report.md` F-1~F-3 · W-1~W-5)**: §3-5 표(50,000 자 → 실물 코드 상수로 특정 · Codex 마커 실물 후보 5 · Claude 변형 3) · 전달 보장 정의(마커 = WP-0 가 고정하는 상수 `TRUNCATION_MARKERS`) · §3-6 `intent_passed` 값 규칙(`none` 처리) · §4-4 · §7-6 C 비율 열 · §7-7 W-1 · W-2(v3.2 발주 보충 2 로 전달 확인) · WORK-006 시험 경로 · 코드 표면 표
> **v2 2026-11-01(0.3.0) — 실험 앱 공정성(B-1) + case3 교체(사용자 결정 11-01)**: §2-5 provider 층(CLI 판 — 「SPEC-006 과 다른 점」 본문 반영) · §3-5 도구 결과 전달 보장 · §3-6 intent 전달 · **§3-4 case3 = Jev 재귀 탐색으로 교체**(보충 `phub-recommend-jev-walk-addendum.md` 우선) · §3-7 공정성 원칙 · §4-2 기록 칸(`delivered_bytes` · `truncated` · `intent_passed` · `walk`) · §4-4 기록 검증 스크립트 · §7-6 v2 끝 조건 · §7-7 아직 안 정한 것. v1(0.2.0)은 `SPEC-006.v1.md` 보관. 근거 = `fail-triage2.md` §2 · §5 · `cli-research.md` · 11-01 실물 조사(§3-5 표)

근거는 아래 정본만이다. 결정은 다시 논의하지 않는다. 이 스펙이 고른 값 R-1~R-10 은 10-30 사용자 승인으로 결정됐다(§7-3). 남은 열린 것은 §7-5 에만 둔다.

| 정본 | 이 스펙에서 |
|---|---|
| `reference/2026-10-30-hub-evals/README.md` | 세 케이스 · 속도 칸 · 품질 두 층 · 화면 와이어 · 기록 꼴 · 열린 것 O-1~O-9 |
| `jev-research.md` | Jev = TypeSafe System One(MCP 없음 · Choice 선택지 255 한도 · confidence · Python SDK) · Claude 로컬 MCP = Anthropic SDK + MCP 클라이언트 |
| `_RESUME.md` §2 10-30 | 원장도 MCP · Q-1~Q-8 · 최종 목표 · 레포 공개 · 데이터 · 키 env |
| `SPEC-005.md` | 허브 골드 도구 9(§5) · 원장 도구 3(§5-12) · 포트 · 경로 — **계약**. 허브는 아직 구현 중이라 실물 대조는 허브 완성 뒤 |
| `quality-eval-set.json` | 나중 회귀용 참고만 — 실험 질문은 사용자가 그때그때 입력(README §1) |

## 0. 요약

- 사용자가 로컬 화면에 질문 하나를 넣으면 case1(원장 MCP + Sonnet) · case2(골드 MCP + Sonnet) · case3(허브 사전 → Jev Choice 슬롯 → 골드 도구 → Sonnet 1회)가 **같은 시각에** 돈다
- 열마다: 속도(ttft · total · 단계별 · LLM 왕복 · 토큰) · 답 스트리밍 · 도구 호출 / Jev 슬롯 / 허브 경로 · ① 단어 검사(원장 대조 결정론) · ② Opus 채점(항목별 통과 · 실패 · 근거 인용 · 가리기) · 사람 확인 표시 · 기록 한 줄(jsonl)
- 앱은 공개 레포 `kknaks/clinic_chat` · 로컬 실행. 허브(SPEC-005)는 따로 떠 있는 서버이고 이 앱은 그 MCP · REST 를 부르기만 한다
- **v2.2**: rerun-v4(182)에서 case3 걸음 수 중앙 1 · 멈춤 64% 가 예산(116/182) · 이웃 peek 에 닿은 판 79/148 — expand 한 섹션이 2.6~55KB(fact 메타 포함)라 첫 걸음에 예산 20KB 를 다 썼고, 예산 멈춤 104 중 94 는 **이웃을 대기열에 넣고도 못 갔다**. 채점 실패 행의 답이 산 곳은 시작 노드 섹션 63/461(14%) · 1홉 이웃 218(47%) · 2홉 151(33%)(owner 정의 — v2.4 받는 자리 정의로는 0홉·1쪽 93(20%) · 1홉·1쪽 120(26%) · §3-4-6) → **첫 걸음은 이웃 먼저**(§3-4-6 표) · 허브 v3.3 fact 한 줄 꼴(섹션 1 중앙 1,902B · p95 2,710B — 허브 측정) 위에서 걸음 4 · 예산 20KB 유지 · stray 15 = Claude CLI 의 「No such tool available」(접두 없는 허브 이름 · 15/15 바이트 대조) → 프롬프트 도구 이름을 provider 실제 이름으로(§3-8)
- **v2**: 실험은 CLI 판(Claude CLI Sonnet · Codex CLI terra · 구독 인증)으로 돈다(§2-5). case2 가 받는 허브 바이트를 허브 응답 전체로 보장(§3-5 — 2차 분류: Claude CLI 가 도구 결과 100/614 를 약 2KB 로 잘라 넘김 · 실패 56/131 이 잘린 문항) · 허브 호출마다 `intent` 를 넘김(§3-6 — 지금 2.1%) · 세 케이스 공정성 원칙 한 조항(§3-7) · **case3 는 Jev 재귀 탐색(peek → Choice → expand · 걸음 4 · 예산 20KB · 되돌아가기 = 의도 묶음 1회)으로 교체**(§3-4 · 11-01 사용자)

| 절 | 내용 |
|---|---|
| §1 | 범위 · 경계 |
| §2 | 구성 · 레포 구조 · env |
| §3 | 세 케이스 흐름 · 같은 조건 · **§3-4 걷기 순서(v2.2 · v2.3) · §3-4-8 안 닿은 34 덮는 셈(v2.3) · §3-8 stray 원인** |
| §4 | 속도 측정 · 기록 꼴 · **§4-5 비교 규칙(v2.2)** |
| §5 | 품질 두 층 |
| §6 | 화면 |
| §7 | 열린 것 처리표(README O-1~O-9 · Jev Q-1~Q-8 · R-1~R-10 결정 · 사용자 몫 · 남은 열린 것 · **§7-6 v2 끝 조건 · §7-7 v2 아직 안 정한 것 · §7-8 v2.2 끝 조건 · §7-9 v2.2 아직 안 정한 것**) |
| §8 | 사용자 실행 절차 |

---

## 1. 범위 · 경계

| 안 | 밖 |
|---|---|
| 실험 앱(서버 + 로컬 화면) · 세 케이스 실행 · 측정 · 채점 · 기록 | 허브 자체(SPEC-005 · 별도 서버) |
| 단건 질문(대화 이어가기 없음) | 여러 턴 · 얼굴 지도 패널 · 병원 상품(KOS) · 운영 지연 예산 판정(README §8) |
| 로컬 실행 | 배포 · 외부 공개 서버 · 허브를 밖으로 노출(jev-research §4 — Messages API MCP connector 안 씀) |

- **LLM 키는 env 로만**(D-11 · 10-30 「Claude 는 API 키 별도」). 문서 · 레포 · 기록 · 로그에 키를 쓰지 않는다
- **공개 레포 규칙**(10-30 「레포 kknaks/clinic_chat 공개 · 데이터 · 키는 env」): 레포에 원장 json · 시맨틱 · 실버 · 골드 파일 · 실행 기록(jsonl) · 허브 응답 캐시 · `.env` 를 넣지 않는다. 경로는 env 로 받는다. `.gitignore` 에 `.env` · `runs/` · `*.jsonl` · 캐시 폴더
- **환자 정보 금지**(10-30): 실험 질문에 환자 정보를 넣지 않는다 — 화면 입력칸 위에 안내 한 줄. Jev(TypeSafe · 미국)로 질문 + 노드 이름이 나간다는 사실도 같은 줄에(jev-research B-4)
- 허브 쪽 계약: 골드 MCP `http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp` · 원장 MCP `…/procedure-hub/raw-mcp/mcp` · REST `…/procedure-hub/gold/*`(SPEC-005 §1-3 · §5-1 · §5-12). 도구 입력 · 출력 스키마는 SPEC-005 §5-2~§5-10 · §5-12 그대로 쓴다

## 2. 구성

### 2-1. 실험 서버

| 항목 | 값 | 근거 |
|---|---|---|
| 언어 | Python 3.12 · `uv` | jev-research §5 · 허브와 같은 도구 |
| Claude | 공식 Anthropic Python SDK(`anthropic[mcp]`) — **직접 루프**(Agent SDK · Messages API MCP connector 안 씀) | 10-30 Q-2 |
| 허브 MCP 연결 | 공식 MCP Python SDK `ClientSession` + Streamable HTTP 클라이언트 transport(정확한 import 경로는 고정한 SDK 버전 문서로 확인 — jev-research §4) · 도구 변환은 `anthropic.lib.tools.mcp.async_mcp_tool` 또는 같은 꼴의 직접 변환 | jev-research §4 · claude-api 스킬 `python/claude-api/tool-use.md` 「MCP Tool Conversion Helpers」 |
| Jev | `typesafe-sdk` `AsyncTypeSafeClient` · 모델 `jev-1.14.0` 고정 | 10-30 Q-6 · jev-research §1 |
| 웹 | FastAPI · uvicorn · SSE(서버 → 화면 스트림) · 127.0.0.1 에만 바인딩 | §7-3 R-1(결정됨) |
| 설정 읽기 | `pydantic-settings` — `config.py` 가 레포 루트 `.env` 를 직접 읽는다(`uv run` 은 `.env` 를 저절로 읽지 않으므로 `--env-file` 대신 이 방식 하나) · 환경 변수가 있으면 그것이 앞섬 | 검수 W-4 |
| 동시 실행 | `asyncio` — 세 케이스를 `gather` 로 같은 `t0` 에서 시작 | README §3 |

### 2-2. 프론트(로컬)

- **결정(R-1): 빌드 없는 정적 페이지 하나**(HTML + 바닐라 JS + `EventSource` · 서버가 정적 파일로 냄)
- 이유: 화면 하나(3열 + 기록 목록)뿐이고 로컬 실험용이다 · Node 빌드 체인이 없으면 실행 명령이 서버 하나로 끝난다 · SSE 는 브라우저 기본 `EventSource` 로 충분하다 · 공개 레포에 의존성이 적다
- 나중에 바꿀 경우(React · Vite 등)도 화면 계약(§6 · SSE 이벤트 §4-3)이 같으면 서버는 그대로

### 2-3. 레포 `kknaks/clinic_chat` 구조

10-30 실물(레포 세팅 끝): GitHub 공개 레포 · main `240c321`(「레포 시작」 — `README.md` · `.gitignore` · `.env.example` 만 있음).

| 자리 | 경로 |
|---|---|
| canonical(main) | `/Users/kknaks/git/clinic_chat` |
| 작업 워크트리 | `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` · 브랜치 `kknaksss/hub-evals`(main `240c321` 에서) |

- main 의 `.gitignore` 는 이미 `.env` · `.env.*`(`!.env.example`) · `runs/` · `data/` · `raw/` · `*.jsonl` · Python 캐시를 막는다 — Phase 1 은 `.cache/` 한 줄만 더한다
- main 의 `.env.example` 은 키 두 개(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) 빈칸뿐 — Phase 1 이 §2-4 나머지 이름을 더한다

```
clinic_chat/
  .env.example            env 이름 · 키 값 빈칸 · 사용자 홈 경로 없음(§2-4)
  .gitignore              (main 에 있음) + .cache/
  pyproject.toml · uv.lock
  README.md               (main 에 있음) + 실행 절차(§8) · 데이터 · 키 규칙
  prompts/                common.md · case1.md · case2.md · case3.md · judge.md · extract.md (판 = 파일 sha 앞 12자)
  clinic_chat/
    config.py             env 읽기(pydantic-settings · 루트 .env)
    clients/anthropic_client.py · jev_client.py · hub_mcp.py(골드 · 원장 ClientSession) · hub_rest.py
    cases/case1.py · case2.py · case3.py · loop.py(case1 · 2 공통 도구 루프) · walk_order.json(v2.2 §3-4-6 표 · 셈 스크립트 결과 그대로)
    timing.py             t0 · stages[] 기록기(perf_counter)
    quality/word_check.py · judge.py · normalize.py(resolve_rules.normalize) · raw_tools.py(채점용 로컬 원장 도구 R1~R3)
    runs.py               jsonl 쓰기 · 읽기 · human_checks
    server.py             FastAPI · SSE · 정적 파일
  web/index.html · app.js · style.css
  tests/                  모의 허브 MCP · 모의 Anthropic 스트림 · 모의 Jev(키 없이 도는 시험)
```

### 2-4. env(`.env` · git 제외 · 예시는 `.env.example`)

`.env.example` 규칙: **키 두 개(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) 값은 빈칸 · 사용자 홈 경로(`/Users/…`)는 쓰지 않음**(사용자 경로 칸은 빈칸). 그 밖의 예시 값(모델 id · 허브 URL · `./runs` · 포트 · 상한 · 문턱)은 적는다. 키는 사용자가 워크트리 `.env` 에 직접 넣는다(U-1 · U-2 완료 10-30).

| 이름 | 뜻 | 예시 값(.env.example) |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API 키(사용자) | 빈칸 |
| `TYPESAFE_API_KEY` | Jev 키(사용자) | 빈칸 |
| `TYPESAFE_DEFAULT_MODEL` | Jev 모델 | `jev-1.14.0` |
| `ANSWER_MODEL` · `JUDGE_MODEL` · `EXTRACT_MODEL` | 답 · 채점 · 이름 뽑기 모델 | `claude-sonnet-5-5` · `claude-opus-5-5` · `claude-opus-5-5`(R-4) |
| `HUB_GOLD_MCP_URL` · `HUB_RAW_MCP_URL` · `HUB_REST_URL` | 허브 주소 | `http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp` · `…/raw-mcp/mcp` · `…/procedure-hub/gold` |
| `RAW_DIR` | ① 단어 검사 · ② 채점 원장 도구(§5-2)가 읽는 원장 21 폴더(레포 밖) | 빈칸(사용자 경로 — `.env` 에서 `…/PROCEDURE-HUB/phub-stg-2026-10-26` 꼴로 채움) |
| `SEMANTIC_JSON` | ① 정규화 규칙 · 표기 차이 확인용 시맨틱 사전(레포 밖) | 빈칸(사용자 경로 — `…/orchestration/work/phub-recommend/semantic.json` 꼴) |
| `RUNS_DIR` | 기록 폴더(레포 밖 또는 ignore 된 `runs/`) | `./runs` |
| `CLINIC_CHAT_PORT` | 실험 서버 포트 | `18210`(사용자 포트 3700 · 3800 · 8700 · 8800 · 54329 · 허브 18005 와 안 겹침) |
| `CASE_TOOL_LOOP_MAX` | case1 · 2 도구 루프 상한 | `12`(R-2) |
| `JEV_CONFIDENCE_MIN` | 낮은 신뢰 표시 문턱 | `0.3`(10-30 Q-5) |

### 2-5. provider 층 — SDK 판 · CLI 판(v2 · 「SPEC-006 과 다른 점」 본문 반영)

10-30 사용자 결정 「실험은 CLI · 배포는 SDK」 · 「CLI provider 결정」 · 「채점 방식 바꿈」 · 「밤새 일괄 실험」 과 `cli-research.md` §6 · 구현(`clinic_chat/llm/cli.py` · `cli_process.py` · `specs.py` · `batch.py`)을 v2 본문으로 올린다. v1 의 SDK 판 조항(§2-1 · §3-1 · §3-2 R-2 · R-3)은 **SDK 판에만** 남는다.

| 항목 | SDK 판(`provider=sdk`) | CLI 판(`claude-cli` · `codex-cli` — **실험 기본**) | 근거 |
|---|---|---|---|
| LLM 호출 층 | Anthropic SDK 직접 루프(§2-1 · `loop.py`) | `claude -p --output-format stream-json --verbose --include-partial-messages`(stdin 프롬프트) · `codex exec --json` — 앱은 JSONL 이벤트를 `CaseTimer` · 기록 꼴로 옮기기만(`cli.py` `ClaudeIngest` · `CodexIngest`) | cli-research §1 · §6-1 |
| provider 고르기 | 질문마다 화면 옵션(`POST /api/ask {question, provider}`) · 기본 `DEFAULT_PROVIDER=claude-cli` · 세 케이스 모두 같은 provider · 기록 `provider` · `versions.answer_provider` | 10-30 「질문에 옵션으로 클로드 / 코덱스 선택」 |
| 모델 · effort | Sonnet 5.5 · effort `high`(R-3) | Claude `claude-sonnet-5-5` · Codex `gpt-5.6-terra` · **effort `medium` 둘 다**(`--effort` · `-c model_reasoning_effort`) · 세 케이스 같음 | 10-30 CLI provider 결정 |
| thinking | `between_tools`(Q-3) | **CLI 기본값**(끌 수 없음 · 기록 `settings.thinking: "cli-default"` · `thinking_seen` · 바퀴마다 `thinking_ms` 따로) — ttft 는 thinking 제외 첫 글자 | cli-research §3-3 |
| 인증 · 과금 | API 키(env) | **구독만** — 자식 env 에서 `ANTHROPIC_API_KEY` · `ANTHROPIC_AUTH_TOKEN` · `*_BASE_URL` · `CODEX_API_KEY` · `OPENAI_API_KEY` · `TYPESAFE_API_KEY` 를 지움(`child_env`) · 실행 앞 `auth.check`(Claude `apiKeySource` 없음 · Codex 로그인) 아니면 그 열 오류 · 기록 `cost.billed: "subscription"` · `usd_estimate`(CLI 추정 · 청구 아님) | 10-30 「ANTHROPIC_API_KEY 는 .env 에서 뺌」 · cli-research §4-1 |
| 격리 | — | Claude `--setting-sources ""` · `--tools ""` · `--allowedTools mcp__hub` · `--strict-mcp-config` · `--disable-slash-commands` · `--no-session-persistence` · `--system-prompt`(Claude Code 기본 프롬프트 갈아 끼움) · `--permission-mode bypassPermissions` · 임시 cwd(레포 밖) / Codex 전용 `CODEX_HOME`(auth.json 링크만) · `--ignore-user-config` · `--ignore-rules` · `--ephemeral` · `-s read-only` · 셸 · exec · 웹검색 · 플러그인 · 스킬 끔 · `model_instructions_file` · `project_doc_max_bytes=0` · `shell_environment_policy.inherit="none"` | cli-research §5 |
| 도구 루프 상한 | `CASE_TOOL_LOOP_MAX` 12 · 닿으면 `tool_choice none`(R-2) | **없음**(CLI 에 칸 없음 · D-3) — `CLI_TIMEOUT_SEC` 600 · Claude `--max-budget-usd` 1.0 · 도구 호출 수 기록 · `tool_loop_max: null` · `loop_capped` 는 CLI 판에서 늘 false | cli-research B-2 |
| 입력(도구 결과) 상한 | `TOOL_RESULT_MAX_BYTES` 20,000(`cap_text`) | **셋 다 없음**(CLI 가 직접 받음 · case3 도 안 넣음 · 기록 `settings.input_cap_bytes: null`) → v2 §3-7 원칙으로 정리 · **SDK 판도 상한을 없앤다**(v2 — 두 판 같게 · `TOOL_RESULT_MAX_BYTES=0` = 없음) | 10-30 결정 · cli-research B-3 |
| ttft | 첫 `text_delta`(토큰) | Claude = 첫 `text_delta`(토큰) · Codex = 첫 `agent_message` 완료(메시지 단위 · 글자 델타 없음) → 기록 `timing.ttft_kind: "token"\|"message"` · 케이스 사이 비교는 같은 provider 안에서만 | cli-research §2 |
| CLI 단계 정의 | `claude#n` · `tool:<이름>#n` | `cli_boot`(spawn → `system/init`) · `cli_queue`(동시 상한 `CLI_MAX_CONCURRENT` 6 에 막혀 기다린 시간) · Claude `claude#n`(`status:requesting` → 그 바퀴 마지막 이벤트) · Codex `codex#n`(턴을 도구 호출로 나눔) · `tool:<이름>#n` · 「(측정 밖)#k」(어느 단계도 안 덮은 구간 — 덮인 합 + 빈틈 = total) · `thinking_ms` · `ttft_ms_ex_boot` · `total_ms_ex_boot` · `cli_boot_ms` | cli-research §2-1 · 10-30 피드백 |
| 채점(① · ②) | SDK Opus(수동 버튼 `AUTO_QUALITY`) | **Claude CLI Opus 자동** · `JUDGE_PROVIDER=claude-cli` · effort `medium`(① 뽑기 `low`) · `JUDGE_MAX_BUDGET_USD` 3.0 · 채점용 원장 도구 3 은 stdio 로컬 MCP(`quality/raw_mcp.py` · R-10 계약 그대로) | 10-30 「채점은 오퍼스로 자동 · cli 는 부담 없잖아」 |
| 채점 방식 | 세 답 묶어 비교(v1 §5-2 가리기 A · B · C) | **열마다 절대 채점** — 한 열 답이 끝나면 그 열 ① → ② 를 바로(세 열 기다리지 않음) · 답 하나씩 같은 기준 · 가리기 유지(case 이름 · 도구 흔적 · 속도 안 보임) · 기록 `judge.mode: "absolute"` · `judge_order` · `judge_seed` 는 남김(섞기 기록) | 10-30 「채점을 왜 한 번에 · 답변 먼저 나온 거 채점 먼저」 |
| 직렬 처리 | — | **없음** — 채점과 다음 질문이 서로 안 막음(서버 직렬 큐 없음 · CLI 동시 상한만) | 10-30 같은 결정 |
| 한도 | — | Claude `rate_limit_event`(status · rateLimitType · utilization · resetsAt · unifiedWindows) 기록 · rejected 면 그 열 오류 · `api_retry` 기록 / Codex 「usage limit」 문구 판정 | cli-research §4-3 · §6-4 |
| 일괄 실행 | — | `clinic_chat.batch` — 계획 파일 `RUNS_DIR/batches/<batch_id>.json` · 질문 × provider 순차(Q1 claude · Q1 codex · Q2 …) · 간격 `BATCH_GAP_SEC` · 재시도 `BATCH_RETRIES` + `BATCH_RETRY_BACKOFF_SEC` · 한도 `BATCH_LIMIT_WAIT_SEC` · 이어 가기 `--resume` · `--label` · `--questions-file` · 질문 세트 `QUESTION_SET_JSON`(239문항) · 값은 사용자가 정함(10-30 전체 실행: 간격 15초 · 재시도 2) · 기록 `batch_id` · `batch_item` · `question_no` · `src_id` · `topic` · `reference_answer`(기록만 · 채점 기준 아님) | 10-30 「전체 질문 실행」 · 「밤새 일괄 실험」 |
| 기록 위치 | `RUNS_DIR` | `RUNS_DIR` = 프로필 레포 `reference/2026-10-30-hub-evals/runs/`(사용자가 봄 · `.gitignore` · 커밋 안 함) — L-1 닫힘 | 10-30 「실험 기록 저장 위치」 |
| 보고서 | — | `clinic_chat.report`(전체 실행) · `rerun_report`(전후 비교 — 통과율 182 · 239 환산 · 통과 수 · 「정보 없음」류 · 오류 · 시간 · 허브 바이트 · 나빠진 문항) · 출력은 레포 밖 `build-out/` | 10-30 「모아 두기만」 |

- v1 의 `.env.example` 표(§2-4)에 더해진 이름: `DEFAULT_PROVIDER` · `CLAUDE_CLI_BIN` · `CLAUDE_CLI_MODEL` · `CLAUDE_CLI_EFFORT` · `CODEX_CLI_BIN` · `CODEX_CLI_MODEL` · `CODEX_CLI_EFFORT` · `CODEX_SERVICE_TIER` · `CLI_TIMEOUT_SEC` · `CLI_MAX_BUDGET_USD` · `CLI_MAX_CONCURRENT` · `JUDGE_PROVIDER` · `JUDGE_CLI_EFFORT` · `EXTRACT_CLI_EFFORT` · `JUDGE_MAX_BUDGET_USD` · `AUTO_QUALITY` · `BATCH_*` 4 · `QUESTIONS_MD` · `QUESTION_SET_JSON` — 값은 `config.py` 기본값(10-30 결정)과 같다. **v2 가 더하는 이름**: `MCP_RESULT_MAX_CHARS`(§3-5 · 기본 200000) · `WALK_MAX_STEPS`(§3-4 · 4) · `WALK_BYTE_BUDGET`(20000) · `WALK_ENOUGH_MIN`(§3-4 · 0.5 추천 · §7-7 · **v2.5: 0.8**) · `TOOL_RESULT_MAX_BYTES=0`. **v2.2 가 더하는 이름**(§3-4-1): `WALK_SECTIONS_PER_STEP`(2) · `WALK_NEIGHBORS_MAX`(3 · 지금 코드 상수를 설정으로) · `WALK_FIRST_SECTION_MAX`(1) · `WALK_FULL_BYTE_BUDGET`(**v2.3: 15000** · §3-4-6 원문 예산 표) · `WALK_FULL_FACTS_MAX`(64 · 허브 `GOLD_EXPAND_FACT_IDS_MAX` 와 같음) · `WALK_FIRST_SECTION_MAX_BY_INTENT`(v2.4 · 기본 `I-02:2,I-03:2,I-04:2,I-05:2` = `order_v24` 셈 결과) · `WALK_ORDER_TABLE`(§3-4-6 표 파일 경로 · 기본 = 레포 안 `clinic_chat/cases/walk_order.json`)

## 3. 세 케이스 흐름

### 3-1. 같은 조건(세 케이스 공통)

| 항목 | 값 | 근거 |
|---|---|---|
| 답 모델 | `claude-sonnet-5-5` · 세 케이스 같음 | README §1 |
| thinking | **끔** = `thinking: {"type": "between_tools"}`(Sonnet 5.5 에서 `disabled` 는 400 — 가장 낮은 설정이 `between_tools` · 다른 칸 같이 보내면 400) | 10-30 Q-3 · claude-api 스킬(Sonnet 5.5 breaking change 1) |
| effort | `output_config.effort = "high"`(Sonnet 5.5 기본값을 명시 · `between_tools` 는 high 이하만 받음) · 세 케이스 같음 | R-3(결정됨) |
| tool_choice | `auto`(Sonnet 5.5 · Opus 5.5 는 강제 `any` · `tool` 이 400) | claude-api 스킬 |
| 폴백 | 쓰지 않음 — 폴백 모델이 답하면 「세 케이스 같은 모델」이 깨진다. `stop_reason == "refusal"` 이면 그 열에 거절로 기록 | README §1 「세 케이스 같은 모델」 |
| 프롬프트 | 공통부(`prompts/common.md` — 답 문장 지시) 같음 + 케이스별 부분(데이터 · 도구 설명만 다름) | README O-2 선택지 → R-5(결정됨) |
| 시작 | 같은 `t0` 에서 동시 시작 | README §3 |
| 스트리밍 | Sonnet 호출은 전부 `messages.stream` | — |
| 단건 | 대화 이어가기 없음 · 매 질문 새 대화 | README §1 |

### 3-2. case1 — 원장 MCP + Sonnet

- 도구 = 원장 MCP 3(`raw_list` · `raw_get` · `raw_search` — SPEC-005 §5-12) 그대로. 골드 · 시맨틱에 기대지 않음(10-30 「원장도 MCP 로」 · Q-1)
- 루프(`loop.py`): Sonnet 스트림 → `tool_use` 면 MCP 호출(병렬 호출은 모아 한 user 메시지로 결과 반환) → 다시 Sonnet → … `end_turn` 까지. 상한 `CASE_TOOL_LOOP_MAX` 번 Sonnet 호출 — 닿으면 `tool_choice: {"type": "none"}`(강제 금지 대상 아님 — none 은 허용)로 마지막 답 호출 1번 · 기록 `loop_capped: true`
- `trace.context` = 도구 호출 목록(README §6 의 「넣은 자료 설명」 자리)

### 3-3. case2 — 골드 MCP + Sonnet

- 도구 = 골드 MCP 9(SPEC-005 §5-1 T1~T9) 그대로 · 같은 `loop.py` — **v2.2: 골드 MCP 11**(T1~T9 + T10 `peek` · T11 `expand` — SPEC-005 v3.2 §5-16 · WORK-006 WP-2 에서 프롬프트에 한 줄로 이미 들어감 · 코디 답 B). v3.3 이 expand 를 짧은 fact 꼴로 바꾸면 case2 도 같은 꼴을 받는다(허브 계약 하나 · 앱은 프롬프트 한 줄 「expand 는 한 줄 fact · 원문은 `fact_ids` 로」 만 맞춤 — v3.3 인자 이름 확정 뒤)
- **v2.2**: 프롬프트의 도구 이름은 provider 가 노출하는 실제 이름으로 채운다(§3-8 막는 법 1)
- `trace.tool_calls[]{tool, input, output_bytes, node_ids[], ms}` — `node_ids` = 결과 JSON 안의 정본 id(`{kind}:{키}` 꼴) 전부(README §6)
- 골드 응답의 `claude_contract`(SPEC-005 §5-0 · O-3)는 도구 결과에 들어 있는 그대로 Sonnet 에 간다(이 앱이 따로 덧붙이지 않음)
- **v2**: CLI 판은 CLI 가 허브 MCP 를 직접 붙인다(앱 `hub_mcp.py` 를 안 거침 · `--mcp-config {"hub": {"type":"http","url":…}}` / Codex `mcp_servers.hub.url`) — 도구 결과 전달은 §3-5 · `intent` 는 §3-6 · 기록 `tool_calls[]` 칸은 §4-2

### 3-4. case3 — Jev 재귀 탐색(v2 역사; 현행 종료·선별은 §3-4-1-5)

> 보충 `phub-recommend-jev-walk-addendum.md` 가 우선한다. v1 의 「Jev 슬롯 1회 → 허브 경로 1회 → 의도 묶음 · 동봉 전부 → Sonnet」 은 잘못된 설계(허브가 「뭐가 필요할지 몰라 다 주는」 구조 — 2차 분류 case3 허브 결과 중앙 46,539B · p95 170,989B · C 10%)로, **되돌아가기(fallback) 경로로만** 남는다(§3-4-3). 허브 쪽 `peek` · `expand` 응답 꼴은 SPEC-005(v3.2 §5-16 · **v3.3 짧은 fact 꼴** — WORK-008)가 정한다 — 이 스펙은 앱이 그 계약에서 쓰는 칸만 §3-4-2 에 적는다.
>
> **v2.2 가 바꾼 것(rerun-v4 근거 · `spec006-v22-count.md` §A)**: v2 걸음은 첫 걸음에 섹션 원문(섹션 하나 2.6~55KB · 단독 호출 중앙 method 8,117B · safety.side_effects 9,793B · aftercare 39,849B)을 받아 예산 20KB 를 소진했다 — 걸음 판 148 중 예산 멈춤 104(첫 걸음에서 62) · 그중 94 는 첫 걸음에 고른 이웃(중앙 3)을 대기열에 넣고도 peek 하지 못함 · 이웃 peek 도달 79/148 · 첫 걸음 expand 하나가 혼자 예산을 넘어 fact 0 → 되돌아감 10. 그래서 ① 첫 걸음은 **이웃 먼저**(§3-4-6) ② 섹션은 허브 v3.3 fact 한 줄(≤ 40자)로 받고 원문은 **마지막에 잘린 줄만 `fact_ids` 로** ③ 예산 넘는 섹션은 **건너뛰고 계속**(멈추지 않음) ④ 「충분」 은 fact 를 1개 이상 모은 뒤에만.

#### 3-4-1. 당시 흐름(v2.2 · v2.3 보강; 현행 종료·선별은 §3-4-1-5)

```
t0 ─▶ ① hub_resolve: T1 resolve(질문 전체)                                         [허브 REST · 결정론]
      ② jev#0: 의도 Choice 12 + 시작 노드 Choice(① 후보 ≤ 255 · 「해당 없음」)       [Jev 1회]
      ③ 걸음 1(시작 노드 S):
           hub_peek#1: peek(S) — slim 카드 + neighbors_by_kind + sections[]{name, n_facts, bytes(= 실제 expand 바이트 · v3.3)} + 안전 요약
           hub_list#1: (v2.3) 표의 edge kind 중 peek n > 앞 4 인 종류마다 expand(S, neighbor_kinds=[kind]) — 그 종류 이웃 전부(예산 밖 · Sonnet 에 안 감)
           jev#1: Choice「먼저 볼 이웃」(§3-4-6 v2.4 edge kind 표의 종류 + S 가 계열이면 key_family · 제품이면 product_unit · 앞 4 + 목록 · ≤ 255) + 짝 Noul(≤ WALK_NEIGHBORS_MAX=3)
                  + Choice「같이 볼 섹션」(≤ WALK_FIRST_SECTION_MAX=1 · I-02 · I-03 · I-04 · I-05 는 2 · 「없음」 있음) — 한 Jev 요청에 두 질문 · 「충분」 은 묻지 않음
                  · 선택지 라벨(v2.3 · W-10): 이웃 = 이름 — edge · label · fact {n_facts} / 섹션 = 이름 · fact {n_facts} · {bytes}B
           hub_expand#1: expand(S, neighbors=고른 이웃) — 이웃 slim · 그다음 expand(S, sections=[고른 섹션]) — 짧은 fact
      ④ 걸음 k = 2..N(N = WALK_MAX_STEPS=4) — 대기열(걸음 1 이웃 · 고른 순) 앞에서 하나씩, 대기열이 비면 S 로 돌아옴:
           hub_peek#k: peek(노드)                    (S 로 돌아오면 peek 는 걸음 1 것을 다시 씀 · 허브 호출 없음)
           jev#k: Choice「펼칠 것」(섹션 ∪ 이 노드의 이웃 · 남은 예산에 맞는 섹션만 · ≤ 255 · 「없음(충분)」) + 짝 Noul + Noul「충분」
           충분(≥ WALK_ENOUGH_MIN 이고 모은 fact ≥ 1) 이면 멈춤 · 아니면 hub_expand#k: 섹션 하나씩(≤ WALK_SECTIONS_PER_STEP=2) — 짧은 fact
           고른 이웃은 대기열 뒤에 붙음(≤ 3 · 걸음 상한 안에서만 감)
           (v2.4) S 가 계열 · 제품이면 섹션 expand 응답의 by_unit{section: {unit id: n}}(≤ 4) unit 을 「그 section 으로」 대기열 뒤에 — 그 걸음은 Jev 섹션 고름 없이 expand(unit, sections=[section])
      ⑤ hub_full: 모은 줄 중 `cut: true`(40자 넘어 잘린 줄 — 잘리지 않은 줄은 줄 = 원문) 를 우선순위 순(§3-4-7)으로
                  → 출처 노드마다 expand(node, fact_ids=[…]) 1회 — WALK_FULL_BYTE_BUDGET(15,000 · v2.3) · WALK_FULL_FACTS_MAX(64) 안에서
                  · 못 받은 cut 줄은 인용 불가 줄로만 넘김(허브 계약 `allowed: "facts_uncut"`)
      ⑥ claude: Sonnet 1회 — §3-4-7 꼴                                                           [스트리밍]
```

| 단계 | 규칙 | 근거 |
|---|---|---|
| 시작 노드 | ① `candidates` 가 비면 Jev 가 vocab(계열 · 고민 · 부위)에서 시작 노드 하나를 고른다 · 그래도 없으면 §3-4-3 되돌아가기 | Q-4 · 11-01 |
| **걸음 1 = 이웃 먼저**(v2.2 · v2.3 · v2.4 보강) | Jev 선택지 = **§3-4-6 v2.4 표에서 그 의도의 edge kind**(+ S 가 계열이면 `key_family` · 제품이면 `product_unit`) 인 이웃 — peek `neighbors_by_kind[kind].items`(앞 4) + n > 4 인 종류는 `expand(S, neighbor_kinds=[kind])` 목록 전부(v2.3 · F-3 앞 4 밖) · 종류 순 · 섞기는 R-7 그대로. 그 종류에 이웃이 없으면 그 다음 종류(SPEC-005 `GOLD_PEEK_KIND_ORDER` 순)로 채워 선택지가 1개 이상이 되게 · 이웃이 하나도 없으면 걸음 1 은 섹션만. 이웃 slim 을 먼저 받고(expand 1회) 섹션(≤ 1)을 그다음에 받는다(예산을 이웃이 먼저 씀) | `spec006-v24-recount.md` — 받는 자리 정의로 461 행 1홉·1쪽 26% · 0홉·1쪽 20%(v2.2 owner 정의의 47% · 14% 를 고침) · 발주 「이웃 먼저 · 섹션은 그다음」 |
| 걸음 1 에 「충분」 없음 | 걸음 1 Jev 요청엔 「충분」 Noul · 「없음(충분)」 선택지를 넣지 않는다 — 아무것도 모으기 전 | rerun-v4: 걸음 1 「충분」 Noul ≥ 0.5 는 0/171(중앙 0.05) · 걸음 1~2 에서 「없음(충분)」 으로 멈춰 fact 0 → 되돌아감 6 |
| 대기열 · 돌아옴 | 걸음 1 이웃(고른 순 = Choice 1위 → 짝 Noul 높은 순)이 걸음 2~ 의 peek 대상. 대기열이 비면 **S 로 돌아와** 남은 섹션을 고름(peek 다시 안 부름). 걸음 k 에서 고른 이웃은 대기열 뒤(2홉) | 발주 「섹션은 그다음」 · 2홉 33% |
| 섹션 수 · 순서 | 걸음당 섹션 ≤ `WALK_SECTIONS_PER_STEP`(2) — Choice 1위 → 짝 Noul 높은 순. **선택지에 넣기 전에** peek `sections[].bytes`(v3.3 = 실제 expand 바이트) > 남은 예산인 섹션은 뺀다 · expand 뒤 실제 바이트가 남은 예산을 넘으면 그 섹션만 **빼고 다음 섹션으로**(멈추지 않음 · 기록 `excluded`) | 0be5ca6 「섹션 하나씩」 유지 · 「처음 넘는 것에서 budget 멈춤」 은 버림(예산 멈춤 104 중 94 가 이웃 대기 중) |
| 예산 B | `WALK_BYTE_BUDGET` 20,000 = **걸음 중 expand 응답 바이트 합**(짧은 꼴 · 이웃 slim 포함 · peek · resolve · 안전 요약 · ⑤ 원문 · 이웃 목록(`neighbor_kinds`)은 밖). **바이트 셈(v2.3 · F-1 · SPEC-005 V-17)**: 허브 REST 응답 본문과 같은 직렬화 = `json.dumps(응답, ensure_ascii=False, separators=(",", ":"))` 의 UTF-8 바이트(앱 `_hub` 의 지금 셈 = 공백 구분자 · 같은 476 호출에서 2,146 vs 2,014 · +6.6% 를 바꿈) · 걸음 경로 호출엔 `intent` 없음 → **peek `sections[].bytes` == 앱이 센 그 섹션 expand 바이트(차 0)** · 차가 나면 기록 `bytes_mismatch` 로 세고 그 섹션은 실제 바이트로 예산 판단. 남은 예산이 peek 의 가장 작은 섹션 바이트보다 작고 이웃 선택지도 없으면 그때 멈춤 `budget` | 추정(§3-4-6 끝 표): 걸음당 섹션 2 · 4걸음 합 중앙 15,159B · p95 19,310B < 20,000 |
| 멈춤 조건 | ⓐ 걸음 2~ 에서 「충분」 Noul ≥ `WALK_ENOUGH_MIN`(0.5) **그리고** 모은 fact ≥ 1 ⓑ 걸음 N 소진 ⓒ 예산(위 정의) ⓓ 대기열 비고 S 에 남은 섹션 · 이웃 없음 — 기록 `walk.stop: enough\|steps\|budget\|empty` (+ Jev 오류 `error` — WORK-006 구현 그대로 · v2.2 에서 정식 칸) | rerun-v4 걸음 2~4 「충분」 ≥ 0.5 = 11/89 · 4/36 · 1/15 — 0.3 이면 걸음 2 에서 22/89 가 멈춰 「걸음 중앙 ≥ 3」 과 어긋남 → 0.5 유지 |
| 의도 | **v2.3: 걸음 경로 허브 호출(peek · expand)에는 `intent` 를 넘기지 않는다**(허브는 받되 무시 M-3 · 넘기면 응답 `request` 에 실려 ≈ 17B 커져 peek `bytes` 와 어긋남 — F-1) · 의도는 `walk.intent` 로 기록 · **의도 기본 묶음 · 동봉 자동 첨부는 걸음 경로에서 쓰지 않는다** · 되돌아가기 경로만 의도 묶음 · **의도는 §3-4-6 표에서 걸음 1 이웃 종류를 고르는 데 쓴다**(v2.2) | 보충 · v2.2 |
| 안전(G13) | peek 의 안전 요약은 노드마다 한 번 · 걸음이 끝나도 예산 밖에서 늘 포함(허브 결정 10-26 「안전은 늘」) | SPEC-005 G13 |
| Jev 선택지 | 255 넘으면 이웃을 `kind` 로 먼저 고르는 2단(v2 그대로) · 순서 seed 섞기(R-7) · confidence · p_max · 1·2위 비 기록(Q-5) | jev-research §2-3 · R-6 · R-7 |
| Sonnet 입력 | §3-4-7 | v2.2 |

#### 3-4-1-1. 걷기 고침 2(v2.5 · `phub-recommend-walk-fix2.md` 그대로 · 아래가 §3-4-1 의 해당 칸보다 앞선다)

| # | 규칙 | 바뀌는 §3-4-1 칸 |
|---|---|---|
| 1 | **필수 묶음 = 걷기와 별개로 늘 받음**: 답에 나올 시술(걸음에서 모은 단위 시술 · 제품 · 계열 중 rank 상위 3)의 `checks` · `site_caution` 섹션은 Jev 선택과 무관하게 expand 로 받음(**예산 안 · 먼저 차감**). 시작 노드가 시술이면 그 시술도 | 「예산 B」 · 「섹션 수 · 순서」(필수 묶음은 걸음당 섹션 상한 · Jev 고름 밖) |
| 2 | **「충분」 늦추기**: 모은 바이트가 예산의 50% 미만이면 「충분」 멈춤 무시 · 문턱 `WALK_ENOUGH_MIN` 0.5 → **0.8** | 「멈춤 조건」 ⓐ(v2.2 의 0.5 유지 근거는 v2.5 에서 대체) |
| 3 | **의도별 고정 섹션**: I-02 overview · method / I-03 aftercare · recovery / I-04 safety.side_effects · safety.complications · **safety.management**(v2.6 — SPEC-005 0.3.5 G20 이 관리 · 예방 54 를 옮김) / I-05 recovery · timeline / I-07 · I-08 쌍 evidence — 시작 노드(또는 첫 시술 노드)에서 첫 걸음에 고정으로 받음(Jev 선택에 더함) | 「걸음 1」 섹션(§3-4-6 의 걸음 1 섹션 상한은 Jev 가 고르는 몫에만) |
| 3a | (v2.6) **바꿀 곳**: 앱 `clinic_chat/config.py:80` `walk_fixed_sections_by_intent` 의 `I-04:safety.side_effects+safety.complications` → `I-04:safety.side_effects+safety.complications+safety.management` · **구현은 rerun-v6b 끝난 뒤 앱 워커**(v6a · v6b 는 지금 값 그대로 — 같은 판 2회 비교를 깨지 않음) · 허브 v3.4(G20) 빌드와 같이 들어가야 함(앞 빌드엔 `safety.management` 가 없어 받을 줄 0) | 「걸음 1」 섹션 |
| 4 | 기록: 필수 묶음 · 고정 섹션 · 「충분」 무시 횟수를 `trace.walk` 에 칸으로(§3-4-4) | §3-4-4 |

- 근거(rerun-v5a `b202611011627-a76c8e` · case3 182 · 앱 0173111 · 허브 2ca8094): 걸음 중앙 4 · 멈춤 enough 82 · steps 87 · 모은 바이트 중앙 6.8KB(예산 20KB 의 1/3) · 실패 192 = 골드에 있는데 못 가져옴 133 · 골드에 없음 27 · 판정 보류 32. 안전 하락 = 예전(의도 묶음)은 금기 · 주의가 늘 따라왔는데 걷기는 Jev 가 고를 때만
- 「필수 묶음」 · 「고정 섹션」 도 바이트 셈 · `intent` 없음 · 1쪽 · 받는 자리 규칙(§3-4-1 · §3-4-2 · §3-4-6)은 그대로

#### 3-4-1-2. 걷기 고침 3(v2.7 · `phub-recommend-walk-fix3.md` 그대로 · 아래가 §3-4-1 · §3-4-1-1 · §3-4-6 의 해당 칸보다 앞선다)

역할 재정의: **Jev = 의도 · 시작 노드 · 이웃(어디로 갈지)만**. 섹션 양은 규칙.

| # | 규칙 | 대체하는 칸 |
|---|---|---|
| 1 | **바닥 = 의도 묶음**: 시작 노드(시술이면 S · 아니면 첫 시술 노드)에서 SPEC-005 §5-14′ 의도 → 섹션 기본 묶음을 expand 로 통째 받음(v3 방식 · 짧은 fact 꼴 · **예산 먼저 차감**) + 필수 묶음(checks · site_caution · I-04 safety.management) 유지 | §3-4-1-1 규칙 3(의도별 고정 섹션)은 이 묶음으로 대체 · 규칙 1(필수 묶음)은 유지 · §3-4-6 걸음 1 섹션 상한 |
| 2 | **Jev 는 이웃만 고름**: 걸음마다 Jev Choice 선택지 = 이웃 노드만(**섹션 선택지 없음**) · 고른 이웃은 그 이웃의 의도 묶음 섹션을 받음(예산 안) | §3-4-1 걸음 1 「같이 볼 섹션」 Choice · 걸음 2~ 「펼칠 것(섹션 ∪ 이웃)」 · 「섹션 수 · 순서」 · S 로 돌아옴의 섹션 고름 · §3-4-6 by_unit 대기열의 섹션(그 단위의 의도 묶음으로) |
| 3 | **남은 예산 채우기(당시 규칙)**: 걸음이 끝나고 예산이 남으면, 방문한 노드들의 섹션 중 의도 순서표(order_v24 · §5-14′) 순으로 아직 안 받은 섹션을 예산이 찰 때까지 받음 · 1쪽 · 결정론. 현재 후속 fill의 뒤 페이지 순서는 §3-4-1-4가 우선한다 | (새 단계 — 걸음 끝 · ⑤ 원문 받기 앞) |
| 4 | **「충분」 멈춤은 예산 80% 전엔 무시**(사실상 예산까지 채움). 걸음 상한 4 · 예산 20KB 유지 | §3-4-1-1 규칙 2(50% · 0.8) |

- 근거: 같은 30문항 case3 정확성 — v3(의도 묶음 통째) 66% vs v6a 38% · v7a 38%. v7a(50): 걸음 중앙 4 · **4걸음 동안 Jev 가 펼친 섹션 합 중앙 3** · 바이트 12.3KB(예산 20KB) · 실버 9단계 데이터가 들어갔는데(I-04 관리·예방 16→62) 정확성 그대로. keycard-measure: 못 가져온 61 중 「방문했는데 Jev 가 그 섹션 안 고름」 29 · 1쪽 밖 4
- 그대로인 것(당시 걸음 기준): 바이트 셈(compact · 걸음 경로 `intent` 없음) · 걸음 중 첫 페이지 1쪽 · 받는 자리 정의 · 이웃 선택지 규칙(§3-4-6 edge kind 표 · 계열 · 제품 단위 규칙 · 앞 4 밖 목록) · 되돌아가기 · ⑤ 원문 받기 · §3-4-7 넘김 꼴. 현재 걸음 뒤 fill은 §3-4-1-4에 따라 뒤 페이지를 받을 수 있다

#### 3-4-1-3. 걷기 고침 4 — 안전 예산 따로(v2.8 · `phub-recommend-walk-fix4.md` 그대로 · 아래가 §3-4-1 · §3-4-1-1 · §3-4-1-2 의 해당 칸보다 앞선다)

| # | 규칙 | 바뀌는 칸 |
|---|---|---|
| 1 | **안전 예산 따로(`SAFETY_BUDGET` · 기본 8KB · 20KB 예산 밖)**: 필수 묶음(checks · site_caution · I-04 safety.management) + 답에 나올 시술 rank 상위 3 의 safety.side_effects · safety.complications 원문 줄은 안전 예산에서 받음 · 일반 예산 20KB 는 의도 묶음 · 이웃 · 남은 예산 채우기 그대로 | §3-4-1-1 규칙 1 「예산 안 · 먼저 차감」 · §3-4-1-2 규칙 1 「필수 묶음 유지」 의 예산 자리(일반 예산 → 안전 예산) |
| 2 | **순서: 안전 예산 먼저 → 일반 예산**. 안전 예산이 넘치면 rank 순으로 자르고 기록 | §3-4-1 흐름의 예산 차감 순서 |
| 3 | 기록: `walk.safety_budget{bytes, sections, cut}`(§3-4-4) | §3-4-4 |

- 근거: rerun-v8a(50 · 앱 106be35) — 정확성 59.2 · 안전 74.0(v6a 84.4) · 답함 90 · 첫 글자 6.9s · 바이트 19.7KB. 실패 대조: 안전 13 = 골드엔 있는데 못 받음 12 · 정확성 20 = 못 받음 16 · 받았는데 안 씀 0. 의도 묶음이 예산 20KB 를 먼저 차지해 금기 · 위험 정보가 밀림
- 그대로인 것(당시 걸음 기준): 바이트 셈(compact · 걸음 경로 `intent` 없음) · 걸음 중 첫 페이지 1쪽 · 받는 자리 정의 · §3-4-1-2(Jev 는 이웃만 · 의도 묶음 · 남은 예산 채우기 · 「충분」 80%) · 걸음 상한 4 · 일반 예산 20KB · 되돌아가기 · §3-4-7 넘김 꼴. 현재 걸음 뒤 fill은 §3-4-1-4에 따라 뒤 페이지를 받을 수 있다
- Sonnet 이 받는 허브 바이트 상한 = 일반 20,000 + 안전 8,000 + ⑤ 원문 15,000(+ 안전 요약) — 공정성 보고(§3-7)에 나란히

#### 3-4-1-4. v2.9 당시 대상·수신 상태와 수집(앱 WORK 전 · 현 구현 아님; 종료·예산은 §3-4-1-5로 대체)

**대상 확정.** Jev 시작 선택 입력/출력에 `question_targets[]{target_key,span,role,candidate_ids[],selected_id?,status,basis,required_sections[],required_facets[]}`를 둔다. `span`은 질문 원문 구간, `role`은 `explicit|comparison_other|synonym_alternative|uncertain`, `basis`는 표현과 resolve 후보·Jev 선택의 연결 근거다. `target_key`는 한 질문 안에서 span 위치와 role로 안정적으로 식별하고 동일 ID의 다른 span도 잃지 않는다. I-06의 명시된 두 대상은 각각 필수이고 같은 span의 경쟁 동의어 후보는 모두 필수가 아니다. 모호한 span/role/선택 ID는 `ambiguous`로 보존하며 임의 후보를 필수 대상으로 확정하지 않는다. Q067.2/Q099.1은 대상 동일성 미확정으로 유지한다. 시작 외 명시 대상의 선택 ID를 질문 순서로 `queue_seed`에 넣는다. queue 항목은 `{node,target_keys[],origin:resolve|neighbor|by_unit,parent?,edge?,state}`이며 동일 node를 합쳐도 target provenance를 합치지 않고 보존한다. 걸음마다 명시 seed를 이웃보다 먼저 처리하되 4걸음 상한은 넘기지 않는다. Jev는 의도·시작 노드·이웃을 고르고 섹션 수집 순서는 아래 앱 규칙이 정한다.

**필수 범위와 상태.** 대상별 `required_sections`는 SPEC-005 §5-14′의 해당 의도 기본 묶음과 기존 필수 안전 섹션이며, `required_facets`는 질문이 명시한 duration/aftercare 등 항목을 해당 대상에 연결한다. I-06은 양쪽 각각 검증한다. I-07/08은 단위 쌍 확정 뒤 그 쌍의 resolved·claims·방향·대안·출처·적용범위와 전역 메모가 요구된 경우 해당 메모를 검증한다. 대상·facet 상태는 `pending|received_supported|unresolved|blocked`, 사유는 `ambiguous|unresolved_pair|unresolved_absence|missing_fact_id|missing_provenance|partial|excluded_budget|error_terminal|deadline|no_progress|steps`로 남긴다. `received_supported`는 필수 section 첫 페이지가 채택되거나 완료 신호가 있는 `empty`이고, **모든 필수 facet**에 적용 범위가 맞는 인용 가능 원문 fact 및 필요한 resolved/대안·방향·출처가 채택됐을 때만 된다. `empty`는 확정 node/section/page 또는 pair 범위의 조회가 완료되고 채택 응답에 fact가 없을 때만 쓰며, 필수 facet의 지원 fact를 대신하지 않는다. `pending/unresolved/blocked` 중 하나라도 있으면 `enough` 금지다. 기존 Noul≥0.8 및 일반 예산 사용 ≥80%도 함께 요구한다. queue 전체 소진은 요구하지 않지만 필수 target의 미방문 seed가 있으면 `enough`가 아니다. 더 진행할 경로가 없으면 `incomplete`로 끝내고, hard stop(steps/budget/error/deadline)은 남은 필수 pending을 사유가 있는 blocked로 바꾼다.

**페이지 수신.** `received[(node,section,page)]={status,accepted_fact_ids[],response_bytes_actual,accepted_budget_bytes,remaining,next_page}`와 `pending_pages[(node,section)]`를 쓴다. `pending → accepted_more|complete|excluded_budget|error_terminal|deadline|no_progress`; `accepted_more`는 다음 page를 pending으로 만들고 현재 tuple을 닫는다. `complete`는 **채택 응답의** `more=0`(칸 생략)에만 붙인다. 제외·오류·deadline은 이번 실행의 terminal이며 section 전체 완료가 아니다. 동일 tuple 자동 재시도는 0회, 다음 사용자 질문은 새 실행이다. 중복 fact ID는 최종 입력에서 한 번만 쓰되 응답 바이트를 환급하지 않는다. page가 증가하고 `more`가 정합하면 기존 ID만 다시 나와도 진전이다. page 정지/반복 또는 remaining 모순은 `no_progress`다. 한 순회에 새 fact·page 진전·target 상태 변화가 모두 없으면 fill을 끝낸다.

**수집 순서.** 안전 8KB의 기존 필수 checks/site_caution·I-04 safety.management·상위 3 시술 안전 **첫 페이지**를 먼저 시도한다. 일반 20KB는 시작/선택 노드의 의도 묶음 첫 페이지부터 받으며, 걸음 중 다음 필수 대상의 첫 페이지가 추가 페이지보다 앞선다. 걸음 뒤 fill은 (1) 방문 노드의 의도 묶음 잔여 페이지를 최초 방문 순→의도 section 순→page 오름차순으로 한 순회에 각각 한 쪽, (2) 의도 묶음에 fact가 있든 없든 **아직 안 받은 section의 첫 페이지**를 기존 의도 순서표로, (3) 예산이 남으면 같은 순서 반복이다. 질문별 정답 ID/키워드로 페이지를 건너뛰지 않는다. 안전 추가 페이지는 기존 안전 rank 절단을 유지하고 안전 예산 안에서만 받는 것을 잠정 규범으로 둔다. 첫 페이지 대상 전부 시도 후 rank 순→section 순→page 순 한 순회 한 쪽씩, 새 상위 3 시술이 나타나면 그 첫 페이지를 추가 페이지보다 먼저 시도한다. 이미 받은 안전 바이트는 rank 하락으로 환급하지 않는다. 안전 추가 페이지 우선순위와 일반 예산 보충 여부는 §7-10 OQ로 사용자 제품 결정 전 WORK 확정 금지다.

**관계 조회.** 확정 단위 쌍의 T4 기본 호출을 general 20KB, `sections=evidence|all` 추가 호출을 full 15KB에 요청 **전** 귀속한다. 현재 T4는 §5-5의 신규 claim/대안별 출처·전역 메모 칸을 보장하지 않으므로 현 응답만으로 필수 관계 facet을 지원 완료 처리하지 않는다. `build+정규화 쌍+prior/sub_condition/include_conditional/sections`가 같은 호출은 중복 제거한다. 호출 전 알려진 응답 크기가 잔여 예산보다 크면 호출하지 않는다. 모르면 잔여 예산을 확인해 호출하고 **전체 compact 응답**이 초과하면 통째로 배제한다. 배제 응답의 resolved·원문·출처·대안 어느 것도 최종 입력이나 인용에 쓰지 않는다. `pairs_more_n`은 개수이므로 확정 단위 쌍은 좁혀 재호출하고 실제 반환 `pairs`를 검사한다. 미확정 쌍은 `unresolved_pair`, 필수 fact가 없으면 `missing_fact_id`, 초과면 `blocked/excluded_budget`다. 64는 node `expand(fact_ids)` 상한이지 T4 상한이 아니다. 005의 선택 관계 API가 구현되면 같은 비용·상태 원칙을 적용한다.

**시간과 예산.** `response_bytes_actual`은 호출별 실제 compact 전체 바이트(초과·중복 응답 포함), `accepted_budget_bytes`는 채택한 전체 응답을 고정된 safety/general/full 한 장부에 차감한 값이다. 혼합 응답도 요청 전에 소유 장부 하나를 정하며 사후 재귀속·부분 채택은 없다. 안전 section을 이미 받았으면 일반 fill은 같은 tuple을 다시 청구하지 않는다. 005의 `peek.sections[].bytes`는 1쪽만의 비용이며 뒤 페이지는 호출 후 전체 바이트로 판정한다. 0.3.9 당시에는 안전 8,000B→일반 20,000B→cut/관계 full 15,000B를 유지하고 배제 응답의 actual 바이트·지연을 기록했다. 0.3.10은 §3-4-1-5로 대체한다. 추가 수집에는 전체 retrieval deadline과 호출별 timeout을 적용한다. 자동 재시도 0회, 시간 소진 시 호출 금지·`deadline` 기록이다. 수치 deadline/timeout은 §7-10 OQ로 남기며 7초 TTFT 목표를 HTTP timeout으로 대체하지 않는다.

#### 3-4-1-5. v2.10 현행 계약 — 탐색 종료와 Claude 입력 선별을 분리(미구현)

**질문 범위.** 시작 전에 질문 원문 span을 `question_targets`에 기록하고 명시 대상마다 필수 facet(기간·회복·관리·비교의 양쪽·관계 방향 등)과 안전 항목(checks, site_caution, I-04 safety.management 및 답에 나올 시술의 관련 위험·금기·고지)을 연결한다. resolve 경쟁 후보는 모두 정답 대상이 아니며 모호하면 `ambiguous`로 남긴다. Jev는 의도·시작·다음 이웃만 고른다. section/page 순서는 의도 묶음·안전 필수 항목·질문의 명시 facet을 기준으로 결정론적으로 정한다. Gold 정답 ID나 평가 키워드를 탐색 경로 점프에 쓰지 않는다. 안전 첫 페이지·명시 대상 seed를 먼저 시도하되 안전의 뒤 페이지와 checks 이웃을 끝까지 추적한다. fullrun-v2 안전 실패 28 중 25가 8KB 절단과 관련된 관측은 이 변경의 근거 일부일 뿐, 회복 수가 아니다.

**Jev 앞단 분류(11-02 사용자 방향).** Hub `resolve`가 질문 원문에서 후보 ID·종류를 내고, Jev가 그 선택지로 의도와 실제 언급된 상품·시술·고민·부위의 역할 및 시작점을 고른다. 서로 다른 종류의 명시 대상이 여럿이면 시작점 하나가 나머지를 지우지 않는다. Jev의 확률 선택은 탐색 경로를 정할 뿐 의료 사실·관계·부재의 증거가 아니며, 선택 ID·종류·원문 span을 Hub 근거와 대조한다.

**동명 anchor와 답변 검증(11-02 실물).** 같은 고민 표현이 둘 이상의 고민 ID로 resolve되어도 시술 대상 하나를 임의로 확정하지 않는다. I-01에서는 그 후보 anchor 각각의 직접 추천 관계와 출처를 확인해 질문 범위의 갈래를 합치고, 서로 다른 조건·적용 범위는 합치지 않는다. Jev 시작 선택은 우선순위 힌트이며 낮은 신뢰도 선택만으로 다른 anchor의 근거를 버리지 않는다. 반면 특정 상품·시술명이 서로 다른 ID로 남는 경우는 대상 모호성을 유지한다. Claude가 정상 반환했는데 검증 실패한 경우에는 원답과 인용·적용범위·필수 안전/flag 등 **실패한 검사 항목**을 평가 trace에 남기고 그 뒤 안전한 fallback을 낸다. 원답이 사라지면 내용 오류와 검증기 오탐을 구별할 수 없다.

**답변 단위 검증 보정(11-02 실물).** 출처 검사는 의료적 사실 주장과 추천한 갈래·시술에 적용하고, 사실을 주장하지 않는 제목·도입/연결 문장에는 인용을 강제하지 않는다. 인용한 문장마다 전달 ID, 원문 내용, owner/`applies_to`를 대조한다. 필수 안전 고지는 실제 추천·언급한 갈래와 관련된 중대 위험·금기·조건을 범위별로 확인한다. 전달했지만 답에서 쓰지 않은 모든 안전 facet을 각각 인용하도록 강제하지 않는다. `정보 없음`의 부정은 **같은 target×section×condition**에 지원 근거가 있을 때만 하며 다른 갈래의 사실로 부재 주장을 뒤집지 않는다. `must_show_flags`는 답에 사용한 인용 사실과 필수 안전 고지에 연결해 검사한다. 이 완화로 근거 없는 효능·관계·제품 추천이나 위험 누락을 통과시키지 않는다.

**추천 역할과 답변 재작성(11-02 실물).** I-01의 직접 `treats`/`treats_unit` 관계가 가리키는 역할 fact가 Gold `evidence` section에 있으면 그 branch의 의도 근거로 원문·출처·범위 확인 뒤 Claude 입력에 포함한다. 그 fact의 `source.file=step7-concerns.json`은 현재 Gold의 인용 가능한 출처이나 원장 `problem-packages`의 정확 배열 path를 대신한다고 주장하지 않는다. 제품 목록·세 조합처럼 현재 Gold가 내지 않는 사실은 추가 원천 투영 전까지 답변 입력과 주장에 넣지 않는다. 모델 원답이 형식·인용·범위/안전 검사에 실패했으나 수집이 완료된 경우, 원답·구체적 실패 사유·동일한 검증 근거를 사용해 재작성을 시도하고 **재작성 결과에도 같은 검사**를 적용한다. 재작성은 검색을 중단하거나 미확인 사실을 보충하는 경로가 아니다. 끝내 실패하면 장문의 근거 원장 전체를 환자용 답으로 덤프하지 말고, 인용 가능한 지원 사실과 미완료 범위를 분리한 간결한 부분 답으로 보류한다. 호출 횟수와 실제 비용·TTFT를 trace/평가에 남긴다.

**관계 소유 fact(11-02 실물).** 직접 추천 관계의 역할 fact는 `owner=applies_to=treats:<id>`처럼 **edge 소유**일 수 있다. node ID와 owner ID가 달라서 배제하지 않는다. `branch_relations`의 anchor→edge→시술 연결, Gold build, fact ID의 edge 접두, 원문·source·`applies_to`가 모두 일치할 때 그 관계에 매인 역할 사실로 인용한다. 같은 단위 시술에 붙은 다른 고민 edge의 fact는 대상 anchor에 속하지 않으므로 제외한다. `treats`의 관계와 파생 `treats_unit`을 각각 추적해 한 역할/시술 갈래가 빠지지 않게 한다.

**실물 범위 보정(11-02).** I-01 추천 질문에서 부위·고민의 일반 표현을 명시된 단위 시술 target으로 승격하지 않는다. 질문의 부위·고민은 anchor이고, 명시 제품·시술명만 시술 target이다. 같은 span의 시술 후보가 여럿인 진짜 모호성은 보존하되, 일반 표현이 여러 시술에 resolve되었다는 이유만으로 답을 차단하지 않는다. anchor의 직접 추천 관계(`treats`, `treats_unit` 등)에서 질문에 맞는 계열·단위 후보 갈래를 만들고, 각 갈래의 해당 부위·조건·의도 facet과 관련 안전 항목만 frontier에 넣는다. 계열·제품의 `units_more_n`은 **그 계열·제품 자체가 답변 대상이거나 해당 단위 갈래가 선택된 경우에만** 전수 조회한다. 선택되지 않은 형제 단위, 타 고민의 모든 overview·부작용, 연결된 모든 확인 조건의 무관 섹션은 `not_required`와 근거를 남기고 열지 않는다. 갈래별 지원 사실·조건·안전 고지의 출처와 적용 범위를 확인하며, 부재를 주장할 때에는 그 갈래의 직접 관계 목록과 필요한 section/page를 실제로 닫는다. Claude에는 갈래별 답변에 필요한 인용 가능 사실을 대표 ID·scope로 묶어 주고, 수집했지만 전달하지 않은 사실은 원장에 남긴다. 전달 ID 전부를 답에 강제 인용해 답변이 근거 덤프가 되게 하지 않는다. 필수 갈래·안전 고지를 조용히 빼는 임의 바이트/걸음 상한은 쓰지 않는다.

**반복 탐색.** frontier는 방문할 node, neighbor 종류/목록의 다음 묶음, `(node,section,page)`, 확정 단위 pair·관계 범위로 나눠 보존한다. 동일 build와 정규화 입력을 키로 중복 enqueue·호출을 막고, 이미 본 node라도 아직 안 받은 section/page/pair는 닫지 않는다. 첫 4걸음은 초기 순회 기본값일 뿐 전체 중단 상한이 아니다. 초기 순회 뒤 미지원 필수 대상/facet 또는 근거를 찾을 수 있는 frontier가 남으면 여러 순회한다. 각 순회에서 명시 대상·안전 → 의도 section의 다음 page → 미수신 section 첫 page → Jev가 선택할 이웃 → 선택 관계·전역 메모 범위를 정해진 순서로 재평가한다. 한 순회에서 각 열린 `(node,section)`의 다음 page는 한 쪽씩 받으며 `more`가 있으면 다음 순회에 넣는다. 응답의 새 fact, 새 page, 새 이웃/section/pair, target/facet 상태 변화를 진전으로 센다. 같은 tuple의 반복, `more`/remaining 모순, 진전 없는 동일 frontier 순회는 `no_progress`로 닫아 무한 루프를 막는다. 단순히 새 fact ID가 없다는 이유로 page 진전을 버리지 않는다. Hub의 page 크기·64 fact_ids 상한·관계 API 상한은 요청 단위 계약이며 전체 탐색 상한이 아니다.

**조회 완료와 종료.** 질문의 각 target/facet은 필요한 인용 가능 원문 fact·출처·적용 범위·관계 방향·대안과 해당 안전 고지를 확인하면 `received_supported`로 닫을 수 있다. 지원 사실을 찾은 뒤 무관한 이웃이나 section의 마지막 page까지 읽을 필요는 없다. 미탐색 frontier가 해당 필수 facet의 지원 판정을 뒤집을 수 있는 필수 범위인 경우에는 열어 두고, 무관해서 더 읽지 않은 범위는 `not_required`와 판단 근거를 trace에 남긴다. **부재를 주장하려는 범위**는 명시된 node/section의 마지막 page `more=0` 또는 완료가 증명된 `empty`, 필요한 이웃·pair·global 범위의 완료 증거가 있어야 `unresolved_absence`로 닫는다. 모호한 대상·쌍은 `ambiguous|unresolved_pair`, 시간/도구/컨텍스트 장애는 `blocked`다. `enough`는 모든 명시 대상·필수 facet·안전 항목이 지원되거나 완료 조회로 정당한 부재 판정을 얻고, 미지원 필수 범위의 frontier가 남지 않았을 때만 가능하다. Jev Noul·바이트 사용률은 참고 trace일 뿐 종료 판정에 넣지 않는다. 후보 경로 소진(`frontier_exhausted`)과 부재 판정에 필요한 범위 조회 완료(`lookup_complete`)를 별도 기록한다. 경로가 소진돼도 조회하지 못한 필수 범위가 있으면 `incomplete`; 완료 조회에서 근거가 없을 때만 해당 범위의 부재를 말한다. 실제 deadline·도구 timeout/오류·모델 컨텍스트 제약으로 중단하면 `blocked/incomplete` 및 미수신 범위를 남기고 사실 부재로 단정하지 않는다. 운영 시간값은 구현 전 설정·가짜 시계 시험으로 정하며 7초 TTFT 목표는 근거 수집을 조용히 자르는 조건이 아니다. safety 8KB/general 20KB/full 15KB 및 예산 80%는 수집 완료·중단·`enough` 조건이 아니고, 카테고리별 고정 장부로 호출을 막지 않는다.

**수집 원장과 전달.** 호출 응답은 compact 실제 바이트·지연·build·요청 tuple·원문 fact ID/본문·source·flags·scope·`more`·오류를 수집 원장에 전부 남긴다. cut 줄은 Hub `expand(fact_ids)`로 원문을 얻기 전에는 인용 불가다. 최종 Claude 입력은 질문 대상·facet에 직접 관련된 인용 가능 fact 원문과 출처, 필수 안전 fact·고지, 적용 범위가 맞는 관계 claim·resolved·대안만 결정론적 순서로 ID와 scope 중복 제거해 구성한다. 인접 시술의 사실을 대상 사실로 옮기지 않는다. 선택에서 빠진 사실도 원장과 `selection_reason`에 남긴다. `retrieval_limits`는 미조회·미확정 범위를 알릴 뿐 의료 근거가 아니다. 관계는 SPEC-005 §5-5/WORK-011의 확정 단위 쌍 `pair_scope.complete`, claim·대안별 source/`applies_to`, 방향, Q139 별도 `global_claims/scope_complete`를 요구한다. 현재 T4 `sections=all`이나 `pairs_more_n`은 충족 근거가 아니다.

**큰 입력.** 전달 크기가 모델 컨텍스트 또는 제공자 제한에 닿으면 관련 근거를 항목별 묶음으로 나눠 각각 출처·ID를 보존해 처리하고, 묶음별 결과를 근거 ID로 대조·병합한다. 일부 묶음을 처리하지 못하면 해당 facet을 `blocked/incomplete`로 표시한다. 입력 cap으로 잘라 놓고 근거 부재라고 답하거나 탈락 사실을 조용히 폐기하지 않는다. 답변은 지원 fact로 확인된 항목만 답하고 안전 고지와 환자별 판단의 한계를 유지한다. 원천/Gold에 없는 사실은 생성하지 않는다. Claude 입력량 제어는 답변 단계의 선별·분할 문제이며 그래프 조회를 막는 별도 바이트 예산이 아니다.

**Q002 실물 후속 — 답변용 근거 묶음(11-02).** 수집 원장 전체와 환자 답을 만들 입력을 분리한다. I-01은 질문 anchor의 검증된 직접 추천 edge를 기준으로 관계 ID와 역할 fact를 각각 보존하되, 같은 unit에 닿는 `treats`·`treats_unit`을 답변 갈래 하나로 합친다. 갈래에 보낼 것은 해당 edge의 역할·시술명/방식의 같은 범위 원문·질문 조건에 적용되는 필수 안전/고지·출처/owner/적용 범위·확인된 gap이다. 단위 시술에 연결됐다는 이유만으로 다른 complaint의 overview나 일반 안전 목록 전체를 보내지 않는다. overview는 질문 고민·부위·조건과 source path가 일치할 때만 채택한다. 적용 범위가 증명되지 않은 사실은 수집 원장에 제외 사유를 남긴다.

**안전 사실의 적용 경로.** 시술 unit을 조회해 받은 family·site_caution·check·disclosure 소유 사실은 `owner != 조회 node`만으로 버리지 않는다. Gold build와 원문 source를 확인하고 해당 unit→family 또는 unit→질문 부위의 공개 관계, fact의 owner·조건·적용 범위를 대조해 갈래에 붙인다. 적용 경로를 증명하지 못하면 그 안전 사실을 임의로 귀속시키지 않고, 필요한 위험 고지가 빠진 갈래는 답변 후보 보류 또는 근거 부족으로 표시한다. Q002의 팔자 필러 갈래는 수신된 안면동맥·괴사·색전 근거가 실제로 적용되는지, 보톡스 갈래는 검증된 제한 효과·비대칭 근거가 적용되는지 확인해야 한다. 의료 문구나 시술 ID를 코드에 하드코딩하지 않는다.

**답 생성·검증·실패 처리.** Claude에는 위 답변용 묶음만 보내고 같은 묶음의 fact ID·source·scope로 문장별 주장과 임상 효과 제목을 검증한다. 순수 문진 질문·전환·상담 안내는 비임상 문장으로 허용하되 그 안의 효과·위험 주장은 인용한다. 부재 주장은 완료된 target×section×condition 범위에서만 허용한다. 실패 재작성에는 검사 이름과 index뿐 아니라 실제 실패 문장·이유·사용 가능한 근거 또는 불허 이유를 전달하고 같은 작은 묶음만 다시 쓴다. 끝내 실패하면 raw fact 나열을 환자 답으로 반환하지 않는다. 검증된 축약 답이 가능하면 같은 안전·관련성·인용 검사를 통과한 뒤 내고, 아니면 범위를 특정한 보류 답을 낸다. 결과는 전달 ID, 탈락 사유, 답 문장별 지원 ID, 실패 이유 및 호출 bytes/TTFT를 trace에 남긴다.

**WP-8 검수 보강.** 답변용 갈래마다 `required_facets/required_safety`와 모든 명시 target을 `included|justified_not_required|unresolved|blocked`로 대조하고 사유를 기록한다. 작은 입력이라는 이유로 필수 고지·조건부 금기·나중 page의 유일한 지원 fact·명시 비교 상대를 조용히 누락하면 성공 판정 금지다. 안전 fact를 채택할 때는 `build, unit, 공개 관계 kind/id, family 또는 site, 조건, fact id/owner/source, 적용 판정`을 trace에 남긴다. 공개 `peek`/안전 동봉/원문 응답 중 실제 증명에 쓴 것을 특정하고 family·부위 또는 `units_affected`·조건 일치를 확인한다. 연결이 공개 응답으로 증명되지 않으면 `unproven`으로 보류한다. 보톡스의 제한 효과는 효과/적합성 근거로, 비대칭은 안전 근거로 분리한다. overview·이름·방식은 source path가 가리키는 complaint/site/condition 또는 공통 unit/family 범위를 구조적으로 판정하며 source 파일명만으로 동일 범위라고 하지 않는다. 재작성 실패 뒤 축약 답도 안전·관련성·인용·부재 범위 검사를 전부 통과해야 반환한다. 반대 부위/타 family/타 complaint/불일치 조건/owner만 같은 fact, 명시 두 target 중 하나 누락, 조건부 금기와 필수 고지 누락, 임상 제목과 순수 문진을 구분하는 음성·양성 fixture를 둔다. Q002의 특정 ID와 위험 문구는 시험 기대값에만 둔다.

**trace와 검증.** `walk.frontier_rounds[]`에 후보·선택·신규 tuple·진전·잔여·종료 사유를, `walk.received[]`에 `(build,node,section,page)`와 `more`·원문 ID·source·실제 bytes·ms를, `walk.relations[]`에 정규화 pair/범위·완료·claim/대안 scope를, `walk.facets[]`에 상태·지원 ID·미조회 범위를 기록한다. `walk.selection[]`은 수집 fact별 `included|excluded`와 이유·전달 묶음 ID를 담는다. 종료는 `lookup_complete|frontier_exhausted|no_progress|deadline|tool_error|context_limit` 및 `complete|incomplete`를 함께 기록한다. 검증기는 수집 원장↔전달 ID/본문/출처 대조, 필수 안전·지원 facet 누락, cut 미해결 인용, 관계 scope 전이, 미완료 범위의 부재 단정, 중복 호출과 반복 frontier, 분할 묶음 유실을 실패로 센다. 개별 재생과 고정 50의 구체 관문은 §7-10 및 WORK-012를 따른다.

#### 3-4-1-6. 질문 목표에 따른 Jev 선택·동적 깊이·종료(0.3.11)

**누가 관련성을 고르나.** Jev가 매 frontier 순회에서 질문과 다음 후보의 의미상 관련성을 판단한다. 입력은 질문·의도·명시 target, 이미 확인한 facet/지원 ID·범위, 현재 노드의 짧은 머리, 직접 관계 kind·edge/source가 붙은 후보 노드와 다음 page 후보, 아직 미지원인 효과·방식·기간·가격·조건·안전 등 target×facet 상태다. 전체 원문을 선택 프롬프트에 반복해 싣지 않는다. Jev는 실제 후보 ID 중 `expand`할 노드/section/page 하나 또는 `stop_answer|stop_incomplete`를 고른다. 후보가 많으면 기존 2단 선택을 쓴다. 모델이 만든 임의 ID나 관계는 실행하지 않는다.

**Jev `Choice` 프로토콜.** 현 Jev `system_one`은 각 `Choice`가 유한 criteria 중 하나를 반환한다. 매 순회 `action` Choice는 `expand|stop_answer|stop_incomplete`, `candidate` Choice는 앱이 발행한 불변 후보 키 중 하나다. 한 응답에서 여러 노드를 임의 JSON 배열로 받지 않는다. 여러 후보가 필요하면 하나를 실행하고 상태를 갱신한 뒤 다시 Jev에 묻는다. 앱은 후보 키를 `(build, target_key, facet, node, edge/kind, section, page)`의 검증된 tuple에만 매핑하며, Jev가 원문·ID·page를 새로 만들 수 없다. `state`에는 질문, 현재 지원/미지원 목표, 후보의 짧은 설명·관계/source·`more`·방문 상태를 넣는다. 후보 255개 초과는 kind/묶음 2단 선택 뒤 원래 후보 집합에 다시 대조한다. 빈 후보면 앱이 상태로 `absence_proved|incomplete`를 판정한다. 무효/옛 build/방향 불일치 선택, 응답 오류, 반복된 방문 선택은 실행하지 않고 남은 유효 후보로 재선택하거나 `no_progress/incomplete`로 종료한다. 종료 이유와 대상 범위는 Jev의 자유 문장이 아니라 검증된 facet 상태와 유한 사유 코드에서 앱이 기록한다. 후보 키·설명·선택 확률·거부 이유·선택 당시 상태를 trace에 남긴다.

**허용 경로.** 앱은 질문 의도와 확정 anchor에 맞는 방향·관계 종류만 후보로 준다. I-01은 고민/부위 anchor의 직접 추천 관계→후보 시술→그 시술에 적용되는 역할·효과/방식·조건·안전 원문이 기본 경로다. fact는 그 질문 facet의 지원/한계 판단에 쓰는 종착 자료이며, 그 fact를 발판으로 다른 시술·고민으로 옆길을 열지 않는다. 다른 의도는 그 의도의 명시 대상·관계/section 계약을 따른다. 후보가 질문과 관련 있는지, 여러 갈래 중 어느 것을 더 읽을지는 Jev가 고른다. 앱은 관계 ID·build·owner/source/scope·타입·방향·방문 여부를 검증한다. Q002의 직접 역할 edge 네 개는 얕은 단계에서 모두 평가하되, 일곱 unit의 모든 section을 자동 필수로 승격하지 않는다. 같은 역할의 여러 unit은 후보로 묶고, 미선택 이유를 남긴다.

**종료 판정.** 깊이는 고정하지 않는다. 각 target×facet은 `pending → supported | justified_not_required | absence_proved | incomplete`로 전이한다. 인용 가능한 원문과 적용 범위·필수 안전/고지를 확인한 facet은 `supported`로 닫고 그 뒤 page/이웃을 `not_required`로 취소한다. Jev의 `stop_answer`는 모든 명시 대상/필수 facet이 지원되거나 범위 완료에 따른 부재가 증명되고, 실제 말할 갈래의 필수 안전/고지와 근거 ID가 검증된 경우에만 허용한다. 미지원 facet이 있으면 Jev가 관련 후보를 선택해 계속 탐색하거나 그 항목을 명시적으로 보류한다. Jev의 충분하다는 판단만으로 근거 부재를 확정하지 않는다. **부재 주장**은 그 facet의 허용된 관련 frontier와 section/page 끝을 실제로 확인한 `absence_proved`에서만 허용한다. deadline·도구 오류·관계 불명확·Jev 오류·진전 없는 동일 선택은 `incomplete`다. 미완료를 `정보 없음`으로 바꾸지 않는다.

`stop_answer`는 명시 target/필수 facet이 `supported|absence_proved`이고 실제 답에 쓰지 않을 **선택 갈래의 비필수 항목만** 이유 있는 `justified_not_required`일 때 허용한다. `absence_proved`의 문장은 완료된 node/section/조건과 필요한 이웃·pair/global 범위를 특정한다. 명시 대상이나 실제 추천 갈래의 필수 안전·금기·고지를 `justified_not_required`로 면제할 수 없다. `stop_incomplete`는 미지원 필수 범위와 `retrieval_limits`를 남기는 보류이며 원천 부재가 아니다. Jev의 종료 선택이나 후보 소진만으로 `lookup_complete` 또는 `absence_proved`가 되지 않는다. 지원 사실이 있으면 관련 없는 뒤 page는 닫지만, 미지원 facet의 `more>0` 뒤 page는 계속 선택 후보로 남긴다. cut fact는 원문/source/scope 확인 전 지원으로 닫지 않는다.

**페이지 제어·기록.** `get_page`는 `more`가 있다는 이유만으로 다음 page를 무조건 큐에 넣지 않는다. 수신 줄의 fact ID가 cut이면 원문/source/owner/scope를 확인하고, Jev가 그 facet에 대한 뒤 page를 계속 선택할 수 있게 남긴다. 지원이 검증되면 뒤 page를 닫고, 미지원이면 Jev가 다음 page와 다른 허용 이웃 중 선택한다. 앱은 `(build,node,section,page/edge)` 방문 집합으로 중복과 순환을 막고, Jev 선택·제외·종료 이유, target×facet 전이, 열지 않은 후보, 실제 호출/bytes/TTFT를 trace에 남긴다. 고정 총 depth나 바이트 수로 근거를 잘라 내지 않는다. Q002는 현재 290 Hub 호출·133개 부작용 page·1.54MB 수신을 기준선으로, 같은 Gold에서 지원 범위와 의료 안전을 유지하며 불필요한 호출/입력/지연을 줄이는지 단일 실물로 검증한다.

#### 3-4-1-7. 노드 갈래 Jev 선택·facet별 페이지 종료(0.3.12)

**선택 단위.** Jev는 질문과 **다음 그래프 노드 후보 묶음**의 관련성을 판단한다. 예: `팔자주름` anchor의 직접 추천 역할과 후보 시술 머리를 보고 여러 갈래를 선택하거나 종료한다. 새 노드 후보가 열릴 때 다시 묻는다. 같은 노드의 page 2, 3, …마다 Jev를 호출하지 않는다. Jev 입력은 질문·현재 node·typed edge/source가 확인된 다음 노드의 짧은 이름/역할·이미 지원된 target×facet·아직 필요한 정보·선택 가능한 종료만 담는다. 원문과 모든 section/page 목록을 반복하지 않는다. 현재 `Choice` API에서는 `pick_1..pick_k`의 복수 Choice 슬롯(각 후보 키 또는 `none`)과 `action=expand|stop_answer|stop_incomplete`를 한 `system_one` 호출로 묻고, 중복/무효 키를 앱이 제거·거부한다. k는 한 호출의 후보 묶음 크기이며 전체 탐색 depth/후보 수 상한이 아니다. 남은 후보가 있으면 다음 묶음으로 계속 갈 수 있다. >255 후보는 kind/묶음 2단 선택 후 원래 후보 집합에 대조한다. Jev가 고른 갈래 밖의 선택적 unit은 이유 있는 `justified_not_required`로 남기되 명시 target·직접 역할·필수 안전을 조용히 버리지 않는다.

**선택된 노드 안의 자료 읽기.** 앱은 Jev가 선택한 노드의 현재 질문에 필요한 facet만 page 1부터 읽는다. 페이지 수신 직후 cut 원문의 full/source/owner/scope를 필요한 ID에 대해 확인하고 target×facet 지원 여부를 판정한다. 지원과 적용 조건·필수 안전/고지가 검증되면 그 facet의 뒤 page는 `not_required`로 닫는다. 미지원 facet이고 `more>0`이면 해당 section 다음 page만 계속 읽는다. 모든 section을 자동 필수로 만들거나 각 page마다 Jev를 호출하지 않는다. 부재를 말할 facet만 허용된 관련 범위를 마지막 page/이웃/pair/global까지 완료한다. 다른 시술·고민으로의 확장은 **새 노드 후보가 질문에 관련 있는지 Jev가 고른 경우**에만 가능하고, 안전 fact 자체는 다른 갈래를 여는 연결로 쓰지 않는다.

**종료·검증.** Jev가 고른 `stop_answer`는 실제 답의 모든 명시 target/필수 facet/선택 갈래의 주요 위험·금기·고지가 `supported|absence_proved`인지 앱이 검증한 뒤에만 성립한다. 비선택 선택적 후보는 답이 전수 목록처럼 말하지 않는 조건에서만 `justified_not_required`다. 중대한 위험의 Gold 공개 원문/적용 범위가 비어 있으면 그 갈래를 추천 완료로 처리하지 않고 보류하거나 Hub 투영을 보강한다. Jev `stop_incomplete`, 무효/반복 선택, deadline/오류는 미완료 범위를 기록하며 `정보 없음`이 아니다. 방문 tuple은 중복·순환 방지, page `more`는 미지원 facet의 증명용 상태일 뿐 전수 탐색 명령이 아니다. Q002 수용은 Jev 호출 수·Hub 호출/bytes·Claude 입력/TTFT·답의 적용 범위/안전/관련성을 함께 비교한다. 0.3.11의 245 Jev/461 Hub/73초 TTFT는 실패 기준선으로 남기고 합격 근거로 쓰지 않는다.

**복수 Choice 순서.** 한 노드 후보 묶음에서 `k=min(4, 후보 수)`개의 `pick_1..pick_k`를 같은 후보 키와 `none`으로 묻는다. 4는 한 호출의 출력 슬롯 수일 뿐 전체 후보·깊이 상한이 아니다. `action=expand`이면 `none`을 버리고 중복을 첫 등장만 남겨 슬롯 순서로 실행한다. 선택된 노드의 필요한 facet이 닫힌 뒤 남은 후보/새로 발견된 다음 노드를 다시 묶어 Jev에 묻는다. 유효 선택이 0개면 다른 미지원 필수 후보가 있는지 재구성하고, 없으면 상태에 따라 완료/미완료로 닫는다. `stop_answer|stop_incomplete`와 유효 pick 동시 반환은 충돌로 거부하고 한 번 재선택, 계속 충돌하면 `no_progress/incomplete`다. >254 후보와 `none`은 원 후보를 정해진 묶음으로 나누어 2단 kind/묶음 선택을 거치며 미선택 묶음을 버리지 않는다. 무효·옛 build·역방향 키는 Hub 호출 전에 거부한다.

**facet 페이지와 의미 지원.** 선택된 노드에서 직접 역할→질문이 명시한 facet→그 갈래의 주요 위험/조건/고지 순서로 필요한 section 첫 page만 연다. slim의 ID/owner/section/flags/관계 scope로 현재 facet의 후보를 좁힌 뒤, 후보 ID만 원문으로 확장한다(요청당 Hub 상한 준수). 모든 slim fact를 즉시 full로 가져오지 않는다. 원문·source·적용 범위와 질문의 의미가 명확히 맞는 fact만 `supported`다. 의미 지원이 불명확하면 Jev가 해당 page의 **짧은 후보 집합을 한 번** 평가할 수 있으나, 후보가 없는 page/이미 지원된 facet/모든 페이지에 일률 호출하지 않는다. 그 평가도 인용 가능 원문과 적용 범위를 대신하지 못한다. `more>0`에서 일부 fact만 지원되면 미지원 필수 facet의 다음 page만 남긴다. 지원된 facet의 뒤 page/불필요한 full 호출은 trace와 시험에서 실패로 센다. 뒤 page 2~7의 유일 지원 fact는 계속 찾아야 한다.

**갈래 의무와 공개 안전 공백.** I-01의 직접 역할 edge는 얕게 모두 검증·기록한다. 그 edge가 후보로 가리키는 여러 unit을 전부 필수 답 갈래로 승격하지 않는다. Jev가 선택한 unit 또는 최종 답 계획에 들어간 unit을 실제 답 갈래로 확정하고 그 갈래의 필수 위험·금기·고지를 연다. 뒤늦게 답 계획에 갈래가 추가되면 해당 의무를 재개방한다. 명시 target은 Jev 미선택으로 면제할 수 없다. 비선택 선택적 unit은 Jev 관련성 선택과 비전수 답 표현을 근거로 `justified_not_required`로 기록한다. 해당 부위의 site-specific 주요 위험이 Gold 공개 원문·owner/source/scope/관계로 증명되지 않으면 안전 지원도 `absence_proved`도 아니며 그 갈래 추천을 보류한다. 원장 `anatomy-danger-zones.zones[5].botox_specific.risk`를 Gold에 투영할 경우 같은 build의 공개 관계와 원문으로 적용을 증명한 뒤에만 쓴다. 해당 원장 위험 문자열/ID를 앱 일반 로직이나 프롬프트에 하드코딩하지 않는다.

**0.3.13 Jev primitive 정정(이 절의 복수 Choice 문장보다 우선).** TypeSafe `Choice`는 한 질문에서 한 옵션을 고르는 도구이고, 한 요청의 여러 질문은 같은 state를 **독립적으로** 본다. 따라서 동일 후보를 넣은 `pick_1..pick_k`는 다중 선택 계약이 아니다. 다음 노드 후보 각각에 `Noul("이 질문의 아직 미지원인 항목을 채우는 데 이 후보가 관련 있는가?")`를 주고, 별도 `Noul`로 현재 근거만으로 답 준비가 됐는지 묻는다. 이 질문들을 **한 `system_one` 요청**에 묶는다. 후보 ID·짧은 이름·직접 관계/역할·미지원 target×facet을 구조화된 `state`에서 각 질문이 정확히 가리키게 한다. `noul` 값은 해당 yes/no 판단의 확률이며 여러 후보를 동시에 선택할 수 있다. 앱은 위험도와 검증 집합으로 정한 임계값/불확실 구간을 적용하되 고정 임계값만으로 명시 target·필수 안전을 버리지 않는다. 애매한 후보는 짧은 추가 근거를 읽거나 보류하고, `answer_ready` Noul이 높아도 필수 근거/안전/부재 검사를 통과해야 종료한다. 확률은 의료 효능 확률이 아니다. 한 요청의 질문/후보 수가 API 한도에 닿으면 안정된 묶음으로 나눠 전 후보 결과를 합치고 빠진 묶음은 `incomplete`로 기록한다. 후보별 `noul`, 선택/보류 임계값·이유와 앱 검증 결과를 trace에 남긴다. 의미 지원이 불명확한 page의 짧은 fact 후보도 후보별 Noul을 묶어 평가할 수 있으나 원문/source/scope 검증은 앱이 수행한다.

#### 3-4-1-8. 지원된 부분 답의 자연어 주장 검증·표시·전달 계측(0.3.14)

**실제 all-hold 후 후보 보정 실험.** claim-v1-ko-2의 관측된17은 개발 자료로만 사용한다. 새 후보는 `wp11-semantic-calibration-proposal.md`의 lossless 의미 state 투영과 관계/범위/커버 역할 명확화만 적용하고 앱의 provenance·필수 의무·반대문맥·전체 승인 hard gate는 유지한다. `wp11-calibration-review.md` R1은 holdout 양성의 반대 문맥을 조건F로 정정, R2는 명시 일시성↔영속성 contradicts, R3는 각 claim에 방문전/상담 시간한정을 명시해 독립 질문의 상속 모호성을 없앤다. 같은 입력의 상반 정답은 실행 금지다. 합성48은 같은 작성자·유사 템플릿 내부 calibration24/모델결과 미관측 H24이며 외부 의료/독립분포 검증으로 확대하지 않는다.

별도 후보 구현과 라벨/투영 검수 후 사전 동결한 공통 문턱 t={0.50,0.60,0.70,0.80,0.90,0.95} 여섯 tuple만 baseline/candidate에 동일 적용한다. C에서 음성오승인0/severe0 중 양성승인 최대, 동률이면 높은t를 선택한다. candidate C 양성10/12 미달 또는 응답누락이면 H 미실행. 통과한 단일 후보/model/prompt/t를 hash 동결한 뒤 H24 각1회, 음성오승인0/severe0·양성≥10/12·응답누락0을 요구한다. baseline C24+candidate C24+candidate H24 최대72실제시도/retry0/실패재호출 없음, H결과 보고 정책 재선택 금지다. 이 실험 통과는 소규모 개발 관문이며 registry/사용자서버 활성화 또는 의료안전성 인증이 아니다. 다음 Q002 검토는 별도 발주한다.

**WP-11 B-01/B-02 보강.** 앱이 각 claim의 `cited_source_indices`와 별개로 `context_source_indices`를 발급한다. 같은 검증 unit/site/condition/관계 범위의 제한·조건·상충 출처는 모델의 인용 선택으로 줄일 수 없다. 의미 관계 질문은 두 집합 모두를 검사하고 지지/반대 혼합은 차단한다. 명시 conflict metadata가 있으면 모델 supports=1이어도 앱이 거부한다. 다른 조건의 출처는 조건을 구분하며 문맥 적용을 증명하지 못하면 보류한다. 새 검색을 하지 않고 검증 bundle 안에서 문맥을 확정한다.

필수 requirement manifest는 앱 소유다. 검증 bundle의 필수 고지 source section/path·flags·공개 적용 범위와 기존 필수 위험/금기/조건 목록으로 의무 여부를 정한다. 명확한 source proposition/qualifier/span이 있으면 각 원자 명제를 행으로 만들고, 없는 필수 원문은 **전체 원문과 모든 한정 조건을 하나의 불가분 의무**로 보존한다. 의학적 원자화를 임의 regex나 생성 모델에 맡겨 의무를 줄이지 않는다. 각 행은 source ID/text/span/hash, build/unit/site/condition, 필수 판정 이유와 manifest hash를 갖는다. 선택적 제외는 앱의 justified_not_required 이유가 있어야 한다. Q002 ID/위험 문자열을 일반 코드에 하드코딩하지 않는다. manifest 구성 불가면 claim_v1 활성화/semantic PASS 금지다. 실제 답 unit은 앱이 발급한 branch/target/source 관계로 확정하고 모델의 kind/facet/빈 requirement 태그로 줄이지 않는다.

앱은 requirement→후보 claim 집합→승인 claim 집합→최종 렌더 span을 결합한다. 커버 질문은 각 requirement의 전체 원문/조건과 해당 후보 claim 집합을 명시하고 모든 하위 의미 보존을 묻는다. 탈락 claim이 있으면 기존 커버 결과는 무효이며 최대 수정 예산 내 재검증하거나 해당 갈래를 보류한다. 필수 manifest 행·승인 claim·source·span 중 하나가 비면 모델 점수가 모두 1이어도 실패다. 같은 source ID만 붙인 채 HA/비HA·감염 조건·지연 시점·개인차 등을 삭제한 변형은 한국어 의미 평가 음성으로 검증한다.

첫 I-01 CLI 경로는 의미 검증을 한 논리 요청에 맞추며 한도를 넘으면 보류한다. 최초/수정 생성 최대2회, 매 draft 전량 검사, 추가 retrieval 없음이다. 정책 미설정/오류/timeout은 승인하지 않는다. fallback은 원자 완전 원문·필수 커버·환자 적합성이 모두 검증될 때만 사용하고, 기존 21행 dump/정의 없는 숫자를 품질 성공으로 세지 않는다. 충족 불가면 hold다. schema enum/필수nullable/빈값/중복참조/크기 상한을 명시하고 상한 초과는 절단 없이 거부한다. absence의 빈 source_ids는 유효 receipt가 있는 경우만 허용한다. raw JSON 중복 키 검출 가능 여부를 CLI 파싱 경계에서 확인하고 미지원이면 trace에 기록한다.

deliver_final은 callback 이전에 attempt를 잠그고 예외에도 재전달하지 않는다. 시작 시각은 유지, callback 실패 시 완료=null/status=failed/error/hash/시도수를 보존하고 finally에서 case 완료를 기록한다. runner 예외가 trace/timing을 지우지 않게 한다. structured-only 응답에 환자 text delta가 없으면 model_first_text=null이며 JSON/tool delta를 TTFT로 꾸미지 않는다. 물리 SDK 재시도와 논리 의미 요청 수·사용량·deadline은 구분해 기록한다.

I-01 coverage CLI의 `claim_v1` 경로는 검증된 답변 묶음에서 Claude가 원자 claim과 source/requirement ID를 strict schema로 출력하게 한다. 앱은 ID/build/hash/source/owner/적용 unit·site·condition을 대조하고, Jev가 각 claim의 원문 지지/반대/미지원을 서로 다른 Choice로 한 요청에 평가한다. 필수 requirement의 실제 의미 커버도 독립 질문으로 확인한다. 질문 간 결과 의존을 가정하지 않으며 instructions는 정확한 state 인덱스를 지정한다. 모호한 의미·혼합 주장·반대/미지원·누락 결과·오류는 승인하지 않는다. 모델이 붙인 facet/requirement 태그 자체는 증명이 아니다. 부재 claim은 실제 완료 receipt와 범위 검사도 통과해야 한다.

원문 전체 일치 이외의 자연스러운 의역은 이 의미 관문을 통과했을 때만 허용한다. 한국어 정상 의역·부정 반전·조건/수치/위험 누락의 라벨 fixture로 정책/model/임계값을 검증하며, 위험 누락 음성 오승인이 있으면 실물 승격하지 않는다. 필수 안전·금기·고지의 requirement→승인 claim→source→렌더 span 대응표를 보존한다. 중복 위험 설명을 합쳐도 각 필수 명제·조건이 남아야 한다. 짧게 만들기 위해 필수 내용을 잘라 내지 않는다. 실패 재작성은 최대 1회이며 동일 검사를 다시 적용한다. 끝내 실패하면 범위가 검증된 원문 축약 또는 보류로 끝내고 미검증 문장을 내보내지 않는다.

사용자 답은 앱의 고정 비임상 제목·검증 claim만 렌더하고 내부 fact ID 대신 번호 인용/출처 대응표를 표시한다. trace에는 원래 ID/claim/판정/requirement/provenance와 최종 text hash를 보존한다. 보류 여섯 갈래와 전체 incomplete 상태는 유지하며 이 표현 변경으로 Gold 안전 공백을 면제하지 않는다. 처음에는 지원된 필러 부분 답에서 시행하고 다른 의도/provider는 기존 정책을 명시한다. 구체 schema·실패 전이·21행 필수 내용 대응은 `wp11-answer-quality-proposal.md` §3~5를 구현 검토 자료로 사용한다.

검증 전 생성 출력은 buffer에 두고 모든 최종 경로가 단일 deliver_final을 거친다. 같은 단조 clock/t0에서 model_first_text, generation_returned, final_validation_completed, 실제 on_text 시작/완료, case_completed와 emitted/failed 상태를 기록한다. CLI의 오래된 timing 사본으로 후처리 시각을 덮지 않는다. callback 예외/중복 전달도 기록하고 브라우저 화면 표시 시간으로 확대하지 않는다. 기존 TTFT는 모델 첫 텍스트 지표로 유지하며 새 timing_schema_version으로 최종 전달 지표를 구분한다. 최종 코드 Q002→대표4→고정50 순서에서 의료 안전과 실제 읽기 품질·최종 지연을 각각 검증한다.

#### 3-4-1-9. Active scope inventory·적용·필수 문맥 완료(0.3.15 · 구현 전)

근거는 [응답 검수·원천 대조 보고](../../../reference/2026-10-30-hub-evals/build-out/wp11-response-review-scope-contract-report.md) §5~9다. 공개 wire shape·mode·오류·canonical join·metadata hash/cache는 SPEC-005 §5-16-1을 따른다. selected scope metadata는 이미 source에 있는 값을 읽는 통로이며 임상 scope를 새로 채우는 통로가 아니다. 실제9/추가326/전체419는 저장 fixture의 관측 범위다. Q002/QID·fact ID/문구를 런타임 허용목록·임상 규칙으로 사용하지 않는다.

**Attachment와 적용.** 수집 scope는 `(build,branch/unit,site,condition set,relation_scope,target_sections,selected_product)`로 고정한다. source owner·attached_to·후보 membership은 열거 이유이지 현재 주장의 임상 적용 증명이 아니다. Jev는 선택적 갈래/비필수 evidence의 관련성을 판단하고 앱은 exact 공개 receipt·관계·source qualifier로 적용을 증명한다. 낮은 relevance/Noul, 조건을 질문에 말하지 않음, owner 미확인, 원문 미수신만으로 같은 scope의 필수 위험·조건·상충을 제거하지 않는다.

일반 시술 질문에서 제품이 선택되지 않았으면 제품 전용 효과/위험을 시술 일반 사실로 무조건 승격하지 않는다. source가 명시한 제품/조합/쌍 범위와 현재 답 범위가 다른 것이 **검증된** 경우에는 source locator·관계/qualifier witness·현재 답 scope·제외 이유를 남기고 `excluded` 또는 `justified_not_required`로 닫을 수 있다. 모든 attachment를 강제 필수로 만들지 않는다. 다만 범위가 불명확하여 실제 주장/같은 범위 필수 경고·반대 근거에 영향을 줄 수 있으면 unknown을 유지하고 해당 branch를 hold한다. 제품 미선택 자체만으로 모든 product 행을 일괄 제외하지 않는다.

**Source별 적용 검증.**

| 유형 | 승인 가능한 범위와 미확정 경계 |
|---|---|
| K8 | conditions/target_keys/not_condition와 나머지 원천 metadata를 보존하고 unit key_family/target_keys를 exact join한다. 저장 K8-0028/0029의 `conditions=[]`, `scope_conditional=false`, `not_condition=true`, target family:M2는 명시 값이며 준비·상담 context로 검증 가능하다. 부재/null을 []/false로 바꾸지 않는다. canonical path는 `step8-relations.json / conditions.claims[ID]` 그대로다. 이는 fixture 수용 예시이며 두 ID 전용 분기 아님 |
| combo member/anchor | 실제 row/field/member index/관계/units/ambiguity와 anchor raw/resolved scope를 각각 검증한다. source_family=M2·후보 여러 site이면 후보 membership을 exact site 적용으로 바꾸지 않는다. 원천이 명시한 family/비교 조합 수준을 그대로 조건 붙여 설명하고 그 수준의 근거가 검증되면 그 수준의 context로 보존할 수 있다. **단독 unit/site 효능·위험의 proof로는 사용할 수 없다.** 별도 확정 scope 증거가 없으면 unknown/hold다. subtitle 부위 목록을 regex로 임상 subject로 나누지 않는다. 같은 source 범위로 채택한 문장의 limitations/조건/상충을 함께 보존하며 낮은 관련성으로 지우지 않는다 |
| product | gold.products one-hop·product_unit 원천 관계로 attachment만 증명하고 product families, active unit family/subfamily, override_of/level/priority/severity_key/source_id를 별도 대조한다. 다중 family 제품의 이름/ID prefix로 제외 금지. extracted 원문에 없는 override_of를 families로 보완하지 않는다. 기존 override 우선순위는 공개 원천 근거와 함께 유지하며 새 선택 정책을 만들지 않는다. 선택 제품 ID/null은 앱 소유 상태로 기록한다. 명시 타 scope 증명 없이 unknown을 일반위험 승인 또는 일괄 제외로 바꾸지 않는다 |
| global note | source가 `step7-concerns.json`인 note도 있다. where/anchor/cc/kind/source와 root+cc→treats→unit witness를 확인해 CC attachment와 pair 적용을 분리한다. owner=scope:all을 모든 unit에 무조건 적용으로 해석하지 않는다. canonical pair/문장 subject가 없으면 `pair_scope_unknown`; regex/LLM으로 임상 subject나 endpoint를 합성하지 않는다. 텍스트와 attachment 문맥이 어긋나도 그것만으로 다른 pair scope가 증명됐다고 하지 않는다 |
| family/site leaf | patient 언어 잎은 exact 부모 statement/source·key_family를 join하고 의미 동일성·필수 qualifier 보존 증거 없이 번역 중복으로 제외하지 않는다. SE leaf는 exact SE root→leaf와 family/기존 override를 확인한다. SC leaf/vessel은 source SC row·meta.sc/vessel·site_caution 관계·unit family/site·조건/전체 원문을 검증한다. site label이나 owner만 같은 것은 proof가 아니다 |

source_family 수준의 context 보존은 exact-site 주장의 면제가 아니다. 원천의 위험/제한이 더 넓은 family 수준으로 이미 검증됐다면 그 scope를 유지해 필수 후보로 보존한다. 반대로 다른 제품·pair임이 증명됐고 현재 답에 그 범위의 주장이 없으면 non-required/excluded가 가능하다. 이 구분이 증명되지 않으면 보수적 hold로 끝내며 원천의 모호성을 구현 결함과 구분해 보고한다.

**단계별 장부와 완료.** support facet의 앞 page 종료와 active context inventory 종료는 별도다. 모든 graph/section이 active inventory가 되는 것은 아니다. 명시 target·실제 답 갈래의 필요한 section 및 같은 scope 필수 안전/조건/상충 후보를 먼저 정하고 다음 순서로 닫는다.

1. **Active scope inventory:** 해당 section의 slim pages·unique ID·remaining/more·peek/공개 count를 대조해 목록을 닫는다. 다른 scope/비필수 section은 검증된 not-required 이유와 범위를 기록한다. 한 page의 support 만족·후보형 일부 수신을 전체 context 완료로 세지 않는다.
2. **Selected scope metadata:** inventory의 적용 미해결 exact ID만 `fact_projection=scope`로 확인한다. 각 행은 attachment 이유/witness, canonical provenance, metadata 존재/hash/version, 대상 scope와 `applicable|excluded|unknown`을 기록한다. `applicable`과 "필수 원문"은 별개다. mode cache를 분리하며 scope 수신은 original 미수신 상태다.
3. **필요 original:** 같은 scope 제한/조건/상충/필수 안전·실제 주장에 필요한 exact ID만 full 수신·검증한다. scope proof에 필요한 원문이 없으면 full을 추가하되 전체326/section 원문을 일괄 full로 열지 않는다. full receipt의 canonical join과 metadata 충돌·새 inventory 재검증을 통과한 뒤 original=received로 승격한다.
4. **Context/manifest:** enumerated ID마다 verified same-scope context, 증명된 다른 scope 제외, 또는 이유 있는 `justified_not_required`로 귀결시킨다. 후자는 source/관계 witness·답 scope·필수 의무에 영향 없다는 근거를 남긴다. 번역 중복은 의미 동일성과 qualifier 보존 증거가 필요하며 자동 면제하지 않는다. 영향 가능한 unresolved ID가 있으면 context incomplete다. 필수 원자 정보가 없으면 전체 원문+모든 조건을 불가분 requirement로 보존한다. B-01/B-02의 앱 소유 context_source_indices·manifest·coverage hard gate는 그대로다.

필요 inventory·scope·original·manifest가 각각 closed이고 영향 가능한 unknown이 없어야 그 scope의 context 완료다. 원천에 없는 pair/site 등의 영향이 해소되지 않으면 무관 graph를 확대하지 않고 `held`로 종료한다. 이것은 구현 완료와 양립하지만 원천 사실 해소/답 성공은 아니다. branch context 완료만으로 전체 lookup/absence 완료를 만들지 않는다. visited/deadline/no_progress와 오류 hold를 유지하며 고정 budget/전체graph 확장/원문 일괄 full을 도입하지 않는다.

claim·제품 선택·branch/target/site/condition/relation scope가 바뀌면 관련 inventory 판정·적용 proof·필수 목록·context·requirement/coverage를 다시 연다. claim 삭제로 scope를 줄여도 장부/필수 의무를 재산출하고 이전 coverage를 무효화한다. 모델 citation/facet/빈 requirement 태그로 의무를 줄일 수 없다. 수집을 끝낸 검증 bundle에서만 의미 검사를 수행하며 bundle 발급 뒤 새 retrieval를 끼워 넣지 않는다. 기존 미지원 여섯 갈래·빈 registry/기본 off·의미 정책 관문은 유지한다.

#### 3-4-2. 앱이 쓰는 허브 계약(SPEC-005 0.3.10 §5-16/§5-16-1 포함)

| 호출 | 앱이 넘기는 것 | 앱이 읽는 칸(최소) |
|---|---|---|
| `peek(node)` | 정본 id 하나(v2.3 · `intent` 안 넘김 — F-1) | `node{}` · `neighbors_by_kind{edge: {n, items[:4]{id, kind, name, label, n_facts}}}`(v3.3 · 종류별 앞 4 · 이웃 fact 수) · `sections[]{name, n_facts, bytes}` — **v3.3: `bytes` = 그 섹션 하나로 부른 expand 기본 꼴 1쪽 응답 바이트(봉투 포함 · 차 0)**(v3.2 의 원문 합은 실제의 중앙 1/10 이라 못 씀 · WORK-006 보고 7) · `safety{}` · `claude_contract.rule`(걸음 계약 규칙 문장 — 여기 한 번) |
| `expand(node, neighbor_kinds[])`(v2.3) | 걸음 1 · peek n > 앞 4 인 표의 edge kind | `neighbors[]{id, kind, name, edge, …}`(≤ 20) · `neighbors_truncated` · `neighbors_more_ids` — 선택지만 · 예산 밖 · Sonnet 에 안 감 |
| `expand(node, neighbors[])` | 걸음 1 · 고른 이웃 id | `neighbors[]{id, kind, name, edge, kind_edge, value?, safety?, sections_n}` |
| `expand(node, sections[1], page?)` | section 하나. 걸음의 최초 수집은 page 1, v2.9 fill은 기존 `page≥2`를 명시한다. page 1의 요청 본문은 `{"sections":[s]}`만, 뒤쪽은 `{"sections":[s],"page":p}`다. 계열·제품의 `by_unit`·`units_more_n`도 읽음 | **기본 꼴** `facts[]{id,line,section,owner?,cut?,flags?,gap?}` · `more{section:n}`(요청 page 뒤 잔여, 0 생략) · `claude_contract{allowed:"facts_uncut",must_show_flags}`. `priority/use_first` 없음 |
| `expand(node, fact_ids[], fact_projection?)` | exact inventory ID ≤64, 기본 full; scope는 metadata-only 전용(혼용 제한은 Hub §5-16-1) | selected full은 기존 text와 source.meta?/scope_projection 추가; scope는 text/line 없이 같은 canonical provenance·projection, original 미수신 |

- **바이트 셈(v2.3 · F-1)**: 앱이 세는 모든 허브 응답 바이트(예산 · 기록 `bytes` · `peek_bytes` · `list.bytes` · `full.bytes`) = 허브 REST 본문과 같은 직렬화 `json.dumps(응답, ensure_ascii=False, separators=(",", ":"))` UTF-8 · 걸음 경로 호출은 `intent` 없이 → peek `sections[].bytes` 와 차 0(SPEC-005 §5-16 「REST 본문 · compact · `intent` 없이」 · V-17 은 이 줄로 닫힘)
- 칸 이름의 **당시 기준**은 SPEC-005 v3.3(0.3.4) §5-16이었다(그 판 작성 중 15:26에 나와 위 표를 맞췄음). **현행 목표 Hub 응답 계약**은 SPEC-005 0.3.10 §5-16/§5-16-1, 앱 수집·종료는 §3-4-1-5~9를 따른다. 새 projection은 구현 전이며 기존 서버 제공을 가정하지 않는다. Hub 응답 칸이 바뀌면 앱 어댑터에서 맞춘다(§7-9 X-1)
- **0.3.9 당시 비용 장부**: 예산 B는 채택한 일반 `expand` 응답 전체 바이트의 합(이웃 slim·fill 포함)이었다. 안전 8KB, 일반 20KB, cut 원문 및 관계 원문 15KB의 단일 소유 장부는 §3-4-1-5에서 폐기한다. 기존 `walk.bytes_total`은 옛 일반 장부만 뜻한다. 현행은 실제 호출 바이트와 Claude 전달 바이트를 분리 기록한다.

#### 3-4-3. 당시 되돌아가기(fallback) — v1 case3 경로 1회(현행 `blocked/incomplete`는 §3-4-1-5)

Jev 가 시작 노드를 못 고르거나(`no_start`) · 첫 걸음 `peek` 가 실패하거나(`peek_failed`) · 걸음이 끝났는데 모은 fact 가 0 이면(`no_facts`) **의도 기본 묶음 1회** = v1 §3-4 경로(의도 → 도구 표 · SPEC-005 §6-1 · `intent` 포함 · 의도 기본 묶음 · 동봉 그대로)를 한 번 부르고 Sonnet 에 넘긴다. 기록 `walk.fallback: true` · `fallback_reason` · 되돌아간 판은 비교 보고에서 따로 센다. 그 밖(걸음이 돌았고 fact ≥ 1)엔 되돌아가지 않는다 — Jev 가 고른 만큼만 답한다(설계의 뜻).

- **v2.2 재검토(조건은 그대로 · 원인 둘을 없앰)**: rerun-v4 되돌아감 34 = `no_start` 11 · `no_facts` 23(첫 expand 호출 하나가 예산을 넘어 fact 0 = 10 · 「없음(충분)」 으로 fact 0 = 6 · 걸음 3 에서 예산 2 · 고를 것 없음 4 · 걸음 소진 1). v2.2 에서 앞 둘은 규칙으로 사라진다(섹션은 미리 거르고 넘으면 건너뜀 · 걸음 1 에 「충분」 없음). 나머지는 사유를 그대로 기록하고 끝 조건에 「되돌아감 수」 를 보고한다(§7-8)

#### 3-4-4. 기록 · 측정(기존 판 필드; 0.3.10 추가 trace는 §3-4-1-5)

**v2.9 당시 trace 초안(현 구현 아님; 0.3.10 추가 칸·판정은 §3-4-1-5 우선):** `walk.targets[]`에 question_targets·required facet별 상태/근거 ID/사유, `walk.queue_seed[]`, queue의 `target_keys/origin/state`, `walk.coverage_at_stop`, `walk.enough_blocked_reason`를 둔다. `walk.pages[]{node,section,page,status,next_page,remaining,request_bytes,response_bytes_actual,accepted_budget_bytes,budget_owner,accepted,fact_ids[],exclusion_reason,ms}`와 `walk.relations[]{pair,input_ids[],expanded_pairs[],tool,sections,request,resolved,fact_ids[],alternatives_status,provenance_status,response_bytes_actual,accepted_budget_bytes,budget_owner,preflight_bytes?,remaining_before,accepted,status,exclusion_reason,ms}`를 둔다. `base_bundle/required/fill`도 node/section/page를 기록한다. section별 `more` 합계는 참고치이고 완료 판정은 page tuple로만 한다. 단계별 Hub/Jev/원문 시간과 TTFT p50/p90, 실제 호출량·배제량을 함께 보고한다. 검증기는 중복 tuple, 이유 없는 page 누락, 같은 Gold ID의 본문 불일치, compact 실제 bytes 차이, 세 예산 초과, 배제 응답의 최종 입력/인용 유입, 미지원 facet에서 enough 종료, 안전 fact·필수 고지 누락을 실패로 센다.

- `trace.walk{start_node, intent, order_kinds[](§3-4-6 v2.3 표에서 쓴 edge kind · 판 `order_table_sha`), list{kinds[], calls, bytes, ids_n, ms}(v2.3 · v2.4 ms), by_unit_queued[]{unit, section}(v2.4), step1_options[](걸음 1 선택지 id 전부 · v2.3 — §7-8 「34 중 선택지에 뜸」 을 재실행 기록으로 다시 세는 칸), bytes_mismatch(v2.3 · peek bytes ≠ 실제), steps[]{k, node, phase: "first"|"queue"|"return", peek_bytes, peek_ms, peek_reused, jev{picked[], picked_neighbors[], picked_sections[], enough?, confidence, p_max, ratio, ms, usage, options_n, filtered_by_budget[]}, expand{calls[]{sections[], neighbors[], bytes, ms, fact_ids[], excluded?}, bytes, fact_ids[]}}, queue_left[], stop, steps_n, bytes_total, budget_hit, neighbor_reached(이웃 노드에서 fact ≥ 1 받은 걸음 수), full{calls, fact_ids[], cut_unfetched_ids[], bytes}, more{section: n}(걸음에서 안 받은 다음 쪽 줄 수), fallback, fallback_reason, jev_calls, jev_ms_total, hub_calls, hub_ms_total, fact_ids[]}` · `trace.hub` 는 되돌아간 판에만
- **v2.8 칸**(메모 3): `walk.safety_budget{bytes, sections, cut}`(안전 예산에서 받은 바이트 · 섹션 · rank 순으로 잘린 것) · `settings.safety_budget`(기본 8000)
- **v2.7 칸**(메모 5): `walk.base_bundle{node, intent, sections[], calls, bytes, fact_ids[]}`(바닥 의도 묶음) · `walk.fill{sections[]{node, section}, calls, bytes, fact_ids[]}`(남은 예산 채우기 — 받은 섹션 · 바이트) · `steps[].jev.picked_neighbors[]`(Jev 이웃 선택 · 섹션 선택 칸은 비움) · 「충분」 무시 횟수는 `walk.enough_ignored` 그대로(문턱 = 예산 80%)
- **v2.5 칸**(메모 4): `walk.required{nodes[](rank 상위 3 + 시술 시작 노드), sections: ["checks", "site_caution"], calls, bytes, fact_ids[]}` · `walk.fixed{intent, node, sections[], calls, bytes, fact_ids[]}` · `walk.enough_ignored`(예산 50% 미만이라 「충분」 멈춤을 무시한 횟수) · `settings.walk_enough_min = 0.8`
- `stages[]`: `hub_resolve` · `jev#0` · `hub_peek#k` · `jev#k` · `hub_list#1-j`(v2.3) · `hub_expand#k`(-j) · `hub_full#n` · `claude`(되돌아가면 `hub_path`) — 첫 글자(`ttft_ms`)에 걸음이 주는 영향 = `claude` 시작 시각 − `t0`
- 비교 기준(v2.2): §4-5 비교 규칙(같은 배치 case1 대비 차 · 결정 전 2회 평균) · 기준 배치 = rerun-v4 `b202611011148-c6ed3a`

#### 3-4-5. (v1 경로 — 되돌아가기에서만 쓰는 정의)

```
t0 ─▶ ① hub_resolve: T1 resolve(질문 전체)                      [허브 REST · 결정론]
      ② jev: 의도 Choice + 슬롯 Choice(한 요청에 병렬)           [Jev 1회 · 255 넘는 슬롯만 2단]
      ③ hub_path: 의도별 골드 도구 경로 1번                       [허브 REST]
      ④ claude: Sonnet 1회(③ 결과 + 낮은 신뢰 슬롯 표시)         [스트리밍]
```

| 단계 | 규칙 | 근거 |
|---|---|---|
| 시작 때 1회 | T9 vocab(고민 · 부위 · 목적 · 확인 조건 · 기법 · 계열 · 의도 · 메뉴)을 받아 캐시 · 질문당 단계에서 뺌(기록엔 `hub_list: "cache"`) | 10-30 Q-7 · SPEC-005 §5-10 |
| ① 사전 검색 | T1 resolve(질문 전체) → `candidates` · `menu_candidates` · `unmatched`. **질문마다 늘 부른다** — 시술 · 제품 슬롯(255 넘음)은 ① 후보 없이는 Choice 선택지를 만들 수 없고, 질문이 시술 슬롯을 말하는지는 ① 을 해 봐야 안다(Q-4). 255 이하 슬롯만 쓰는 질문에도 부르므로 그 시간은 `stages[]` 의 `hub_resolve` 로 따로 남겨 `jev` · `hub_path` · `claude` 와 나눠 비교한다(검수 W-7) | SPEC-005 §5-2 · 10-30 Q-4 |
| ② 의도 | Choice 하나 — 선택지 = 의도 12(SPEC-005 §5-1 의도 열 · gold-research 의도 I-01~I-12) · `criteria` 설명 = 의도 이름 · 예시 질문 | D-08 · gold-research §3 |
| ② 슬롯 | 슬롯마다 Choice 하나 — 슬롯 = T9 vocab 종류(고민 · 부위 · 목적 · 확인 조건 · 기법 · 계열 · 메뉴) + 시술 · 제품. **중증도 슬롯은 없다** — 허브 vocab(SPEC-005 §5-10)에 중증도 종류가 없고, 7단계가 중증도를 하위 고민으로 옮겼다(R18 · J12 — 주름 초기 · 경미 → P2-3 잔주름 · 중기 · 중등도 · 심화 · 중증 → P2-2 깊은주름 · `step7-concerns.md`) — D-08 의 「중증도」는 고민 슬롯이 덮는다(검수 W-6). 선택지 = vocab 노드(이름 + 동의어 몇 개를 설명으로 · 한국어만). **선택지가 255 를 넘는 슬롯**(시술 · 제품: 단위 시술 162 + 제품 354 + 계열 27)은 ① 의 후보로 줄인 뒤 Choice(10-30 Q-4) · 「해당 없음」 선택지 + 짝 Noul(「질문이 이 슬롯 값을 말하나」) | 10-30 Q-4 · jev-research §2-3 |
| ② 여러 고민 | Choice 는 하나만 고른다 → R-6(① 후보 고민마다 Noul) | jev-research §2-3 |
| ② 선택지 순서 | 섞고 seed 기록(앞쪽 기울기) | jev-research §2-3 「순서 또는 seed 기록」 → R-7 |
| ② 신뢰도 | 슬롯 · 의도마다 `confidence` · `p_max` · 1·2위 비 기록 · `confidence < 0.3` 이면 `low_confidence` 표시 | 10-30 Q-5 · jev-research §2-2 |
| ③ 경로 | **의도 → 도구 = SPEC-005 §6-1 의도 → 도구 대응 그대로**(① T1 은 이미 부름). 이 스펙에 옮겨 적은 꼴: I-01 → T2 recommend(`concerns` · `site` · `cc` — T1 `candidates` 의 concern · site 만) · I-02 · I-03 · I-04 · I-05 · I-10 → T3 procedure_card(의도별 `sections`) · I-06 → T6 compare · I-07 · I-08 → T4 pair_check(**I-07 자기 쌍 = 같은 id 두 번** — SPEC-005 §5-5) · I-09 → T5 check_conditions(**확인 조건 노드가 안 잡히는 질문(「통증 민감」 꼴)은 T3 `sections=overview,ops`**) · I-11 → T7 combos(`menu_candidates` 는 여기만 · 질문 말이 라벨이면 `menu` · 아니면 `concern`) · I-12 가격 → 허브 도구 없음(연결 층 · 이 실험 밖 — Sonnet 에 「가격 정보 없음」만 줌). SPEC-005 §6-1 이 바뀌면 그쪽을 따른다(검수 W-2) | SPEC-005 §6-1 · §5-1 · §5-5 · gold-research §3 |
| ③ 필수 슬롯 없음 | 그 의도의 필수 슬롯(SPEC-005 도구 필수 입력)이 비면 도구를 부르지 않고 「되묻기 필요」로 Sonnet 에 넘김 | D-08 「신뢰도 낮은 슬롯은 되묻기」 |
| ④ Sonnet | 1회 · 도구 없음 · 입력 = 질문 + ③ 결과 JSON + 슬롯 표(낮은 신뢰 표시 포함) | README §2 |

- 기록 `trace.jev{model, intent{choice, confidence, p_max, ratio}, slots{…}, noul{…}, option_order_seed, usage}` · `trace.hub{resolve, path, tool, input, node_ids[]}`
- Jev 실패(401 · 422 · 429/529 재시도 끝 · 시간 초과): 그 열을 오류로 기록하고 다른 두 열은 계속(jev-research §2-4)

#### 3-4-6. 첫 걸음 이웃 순서 표(v2.4 · 「받는 자리」 정의 하나 · edge kind 단위 · 결정론 규칙 · 근거 셈)

**받는 자리(v2.4 · 재검수 F-1 · F-2 — 이 스펙의 당시 걸음 도달 셈이 이 정의 하나를 쓴다)**: fact f 를 걸음이 받는 곳 = (노드 n, section s, 쪽 p) 중 f 가 `g.section_ids[(n, s)]` — **`expand(n, sections=[s])` 가 실제로 줄로 내는 목록**(노드 자신의 줄 · 계열 · 제품의 펼친 단위 fact 는 안 들어감 · 허브 `_node_fact_ids` 는 `fact_ids` 로 받아 줄 수 있는 집합이라 이것과 다름) — 의 i 번째이면 p = i // 12 + 1(1쪽 12줄 · SPEC-005 `GOLD_EXPAND_SECTION_MAX`). 이 표의 **걸음 중 최초 수집**은 1쪽만 센다(§3-4-2). 0.3.9의 **걸음 뒤 fill**도 §3-4-1-4에 따라 `page≥2`를 받을 수 있었고, 0.3.10은 §3-4-1-5에 따라 반복한다. 이 표의 1쪽 도달 수치를 전체 수집 상한으로 읽지 않는다. 행의 자리 = 그 행 골드 fact hit 전부(인용 → `triage2.gold_match` · 앞 몇 개로 자르지 않음) 중 걸음이 받기 쉬운 쪽을 먼저:

| 자리 | 뜻 |
|---|---|
| 0홉·1쪽 | S 자신의 section 줄 1쪽 |
| 1홉·1쪽 | S 줄 1쪽에 없고 · edge kind k 로 이은 이웃 X 의 줄 1쪽에 있음(k 를 기록) |
| 0홉·2쪽+ · 1홉·2쪽+ | S · 이웃 X 의 줄에 있으나 2쪽 이후뿐 |
| 2홉+ | S · 1홉 밖 어느 노드의 줄에 있음 |
| 받을 곳 없음 | 어느 노드의 section 줄에도 없음(관계 엣지 · `scope:` 가 owner 인 fact 등) |
| 이름·속성만 | 인용이 fact 가 아니라 노드 이름 · 속성 · 엣지 속성에만 잡힘 |

**461 행(근거 행은 v2.2 와 같음 — rerun-v4 case2 · case3 + rerun-v3 채점 실패 · valid 근거 · 골드 hit · 시작 노드 S 있음)을 이 정의로 다시 셈**(`spec006-v24-recount.py` · backend venv · b031371c 메모리 빌드 · 두 번 같음):

0홉·1쪽 **93**(20%) · 1홉·1쪽 **120**(26%) · 0홉·2쪽+ 19 · 1홉·2쪽+ 94 · 2홉+ 75 · 받을 곳 없음 33 · 이름·속성만 27

| 의도 | 0홉·1쪽 | 1홉·1쪽 | 0홉·2쪽+ | 1홉·2쪽+ | 2홉+ | 받을 곳 없음 | 이름·속성만 |
|---|---|---|---|---|---|---|---|
| I-01 | 2 | 14 | 1 | 19 | 12 | 2 | 3 |
| I-02 | 9 | 5 | 2 | 6 | 2 | 0 | 2 |
| I-03 | 16 | 2 | 0 | 10 | 2 | 0 | 0 |
| I-04 | 27 | 10 | 2 | 10 | 1 | 0 | 6 |
| I-05 | 21 | 20 | 7 | 16 | 4 | 5 | 0 |
| I-06 | 13 | 30 | 5 | 11 | 27 | 2 | 9 |
| I-07 | 1 | 10 | 0 | 3 | 13 | 22 | 2 |
| I-08 | 0 | 0 | 1 | 0 | 0 | 2 | 0 |
| I-09 | 3 | 15 | 1 | 15 | 9 | 0 | 3 |
| I-10 | 1 | 11 | 0 | 2 | 4 | 0 | 0 |
| I-11 | 0 | 3 | 0 | 2 | 1 | 0 | 2 |

- **「이웃 먼저」 근거 다시(F-2)**: v2.2 의 「1홉 47% · 2홉 33% · S 섹션 14%」 는 owner 정의라 일부가 실제로는 S 섹션 몫이었다. 받는 자리로는 **1홉·1쪽 26% > 0홉·1쪽 20%** — 이웃 먼저는 유지되지만 차가 작다. 그래서 0홉·1쪽이 1위인 의도(**I-02 · I-03 · I-04 · I-05**)는 걸음 1 섹션 2(아래)
- **v2.3 표가 잘못 센 곳(재검수 F-2)**: v2.3 「1홉 185」 은 owner 엣지 종류로 셌다 — 같은 행을 받는 자리로 보면 S 줄에 이미 있음 · 받을 곳 없음(관계 fact) · 이름만이 섞여 있었다(검수자 셈 61 · 16 · 16). v2.4 는 1홉·1쪽 120 행만 표 근거로 쓴다(W-5 — 461 의 나머지 341 행이 빠진 이유 = 위 자리 표)
- 1홉·2쪽+ 94(20%)는 이웃에 가도 1쪽에 없다 — 걸음에서 2쪽을 부를지는 X-12

**v2.4 규칙**: 1홉·1쪽 행의 edge kind 셈 · 의도 행 ≥ 10 이면 그 의도 · 아니면 전체 · 셈 내림차순(동점 = 전체 셈 → 이름)으로 넣어 가며 **그 의도 1홉·1쪽 행의 90% 를 덮으면 멈춤(최소 3)**. 표는 `spec006-v24-recount.json` 의 `order_v24` 이고 앱은 그 커밋본을 그대로 `walk_order.json` 으로 복사한다(손으로 고치지 않음 · 스크립트 재실행 금지 · 판 sha 기록).

| 의도 | 1홉·1쪽 행 | 근거 | 걸음 1 이웃 edge kind(순서) | 덮음 | 걸음 1 섹션 |
|---|---|---|---|---|---|
| I-01 고민 → 추천 | 14 | 의도 | treats → treats_unit → key_family → key_site → site_caution_unit → procedure_relation → requires_check_unit | 13 | 1 |
| I-02 시술 설명 | 5 | 전체 | (전체) | 5 | **2** |
| I-03 주의 · 사후관리 | 2 | 전체 | (전체) | 2 | **2** |
| I-04 부작용 · 합병증 | 10 | 의도 | key_family → product_family → procedure_relation | 9 | **2** |
| I-05 회복 · 효과 기간 | 20 | 의도 | treats → treats_unit → key_technique → product_unit → uses_product → key_family → requires_check → product_family | 18 | **2** |
| I-06 비교 | 30 | 의도 | key_family → treats → treats_unit → procedure_relation → requires_check → product_family → key_technique → product_unit | 29 | 1 |
| I-07 같이 · 순서 · 간격 | 10 | 의도 | treats → treats_unit → requires_check → anchors_combo → key_family | 9 | 1 |
| I-08 이전 시술 뒤 | 0 | 전체 | (전체) | 0 | 1 |
| I-09 해도 되나 | 15 | 의도 | requires_check → key_family → product_family → requires_check_unit → treats → treats_unit → procedure_relation → key_site | 14 | 1 |
| I-10 용량 · 회차 · 제품 | 11 | 의도 | treats → treats_unit → key_technique → key_family → requires_check | 10 | 1 |
| I-11 추천 조합 | 3 | 전체 | (전체) | 3 | 1 |
| I-12 가격 | — | — | 걸음 없음(허브 도구 없음 · v1 과 같게 「가격 정보 없음」) | — | — |

전체 순서: treats → treats_unit → key_family → requires_check → product_family → procedure_relation → key_technique → anchors_combo → key_site(1홉·1쪽 120 중 108 덮음).

- **계열 · 제품 S 의 단위 fact(F-1 · 허브 계약 변경 없음 — 코디 11-01 참고 · WORK-008 실물 꼴)**: 계열 · 제품 노드의 section 줄에는 펼친 단위 시술의 fact 가 없다. 그 fact 는 단위 노드의 줄에 있다(위 정의로는 「1홉 · edge kind `key_family`(계열) · `product_unit`(제품)」). 규칙 둘: ① S 가 계열이면 `key_family` · 제품이면 `product_unit` 을 걸음 1 이웃 edge kind 에 **늘 더한다**(표에 없을 때) ② S 가 계열 · 제품이고 고른 섹션 expand 응답에 `by_unit{section: {unit id: n}}`(≤ 4 · `units_more_n`)이 있으면 그 unit id 들을 **같은 section 이름과 함께** 대기열 후보로 둔다 — 그 단위로 걸음이 가면 `expand(unit, sections=[그 section])` 을 Jev 섹션 고름 없이 부른다(대기열 뒤 · 걸음 상한 안 · 예산 안). 지금 셈에서 ①이 표에 더하는 덮음은 461 · 34 모두 **0**(그 행들의 의도 표에 `key_family` 가 이미 있음) — 표가 바뀔 때를 위한 구조 규칙이다. ②의 몫은 by_unit 이 어느 단위를 앞 4 로 고르는지(허브 정렬)에 달려 이 셈에서 세지 않았다(X-13)
- **걸음 1 섹션 상한**: `WALK_FIRST_SECTION_MAX` = 1 · 0홉·1쪽이 그 의도 자리 1위인 의도(**I-02 9/26 · I-03 16/30 · I-04 27/56 · I-05 21/73**)는 2(`WALK_FIRST_SECTION_MAX_BY_INTENT` = `order_v24.first_section_max_2`). 섹션은 걸음 1 섹션 선택지에 늘 전부 뜬다 — 상한은 받는 개수만
- **앞 4 밖**: 표의 edge kind 중 peek `neighbors_by_kind[kind].n` > 앞 4 인 종류는 Jev 요청 전에 `expand(S, neighbor_kinds=[kind])` 로 그 종류 이웃 전부를 선택지에 넣는다(예산 밖 · Sonnet 에 안 감 · `walk.list` · v2.3 그대로). 표가 9 종류인 의도(전체 표)는 목록 호출이 최대 9번 생길 수 있다 — 호출 수 · ms · 첫 글자 영향은 X-2(T-2)에서 잰다(W-6)
- 「전역 scope」 · 「다른 시술」 은 peek 이웃 종류가 아니다 — 표에 없다. 2홉+ 는 대기열로만 닿는다
- 표는 461행에서 셌고 §3-4-8 의 34 행과 겹친다(표본 안) — 재실행 기록이 쌓이면 같은 스크립트로 다시 센다(판 sha 바뀜 · 자동 갱신 안 함 · X-8)

**예산 · 걸음 상한 근거**: ① 허브 측정(SPEC-005 v3.3 §5-16 · `spec005-v33-measure.json` — 전 6,140 (노드, section) · 줄 40자 · 1쪽 12줄) 섹션 1 기본 꼴 **중앙 1,902B · p95 2,710B** ② 이 스펙의 재생(rerun-v4 걸음 기록의 섹션 호출 387 을 같은 fact 로 `{id, line(앞 80자), section, owner}` 로 다시 셈 · `spec006-v22-count.md` §C) 중앙 2,037B · p95 2,630B — ② 로 표를 짠다(보수적). ③ **이웃 slim(검수 W-11 실측 · b031371c · rerun-v4 걸음 선택 그대로)**: 1장 중앙 250B · p95 1,014B · 최대 1,178B · 걸음 1 이웃 배열(151 호출 · 중앙 3장) 중앙 752B · p95 2,306B. 걸음 2~ 에서 이웃을 고르면 그 slim 도 예산 안(v2.2 표가 빠뜨림):

| 걸음당 섹션 | 걸음 1(이웃 배열 + 섹션 1) | 걸음 2~4 각(이웃 안 고름 / 고름) | 4걸음 합 중앙(안 / 고름) | 4걸음 합 p95(안 / 고름) | 20,000 안? |
|---|---|---|---|---|---|
| 1 | 2,789 | 2,037 / 2,789 | 8,900 / 11,156 | 12,826 / 19,744 | ○ |
| **2(채택)** | 2,789 | 4,074 / 4,826 | **15,011 / 17,267** | **20,716 / 27,634** | 중앙 ○ · p95 ✗ |
| 3 | 2,789 | 6,111 / 6,863 | 21,122 / 23,378 | 28,606 / 35,524 | ✗ |

(p95 열 = 걸음 1 p95 4,936 + 걸음 2~4 각 p95 · I-02 · I-03 · I-04 · I-05 의 걸음 1 섹션 2 는 + 2,037 / 2,630 — 그 의도는 4걸음 합 중앙 17,048(이웃 안 고름) · p95 23,346 · v2.4)
→ `WALK_BYTE_BUDGET` 20,000 · `WALK_MAX_STEPS` 4 · `WALK_SECTIONS_PER_STEP` 2 · `WALK_NEIGHBORS_MAX` 3 유지. p95 걸음은 예산을 넘지만 v2.2 규칙에서 넘는 섹션은 **건너뛰고 계속**하고 `budget` 멈춤은 「남은 예산 < 가장 작은 섹션 · 이웃 선택지 없음」 일 때만이라 마지막 걸음의 섹션 하나가 빠지는 꼴이다. 「예산 멈춤 ≤ 30%」(§7-8)가 이 표로 서는지는 추정이라 WORK-009 T-2 가 v3.3 실물로 잰다(X-2)

**원문 예산(v2.3 · F-2)**: v2.2 의 근거(모은 fact 원문 **글자** 합 중앙 2,235B · p95 3,903B · 「cut 만이면 여유 큼」)는 `expand(fact_ids)` **응답** 바이트가 아니어서(행마다 봉투 · `id` · `section` · `owner` · `source{file, path}`) 틀렸다. 측정으로 바꾼다:

| 근거 | 값 | 출처 |
|---|---|---|
| 걸음당 cut 줄 수(중앙 / p95 / 최대) | 14 / 35 / 49 | SPEC-005 §6-7 (e) · `spec005-v33-measure.json d_walk.new_replay.cut_n`(rerun-v4 같은 선택 · 새 꼴 재생 · 148 걸음) |
| **cut 줄 원문 받기 응답 바이트(중앙 / p95 / 최대)** | **5,389 / 14,376 / 19,233** | 같은 곳 `cut_fetch_bytes` |
| 걸음 + cut 받기 합(중앙 / p95 / 최대) | 16,000 / 32,634 / 37,406 | 같은 곳 `bytes_plus_cut_fetch` |
| 줄 기준 cut 비율 | 전 (노드, section) 줄 23.4%(검수자 셈) · 재생 걸음이 받은 줄 37.7%(`cut_line_ratio`) — 고유 fact 기준 13.9% 보다 큼(긴 fact 가 여러 자리에 되풀이) | 검수 F-2 · `spec005-v33-measure.json` |

→ **`WALK_FULL_BYTE_BUDGET` = 15,000**(재생 p95 14,376 위 · 148 걸음 중 넘는 걸음 ≤ 7 — p95 자리 정의) · `WALK_FULL_FACTS_MAX` 64(허브 `GOLD_EXPAND_FACT_IDS_MAX`). 넘는 걸음의 뒤쪽 cut 줄은 `quotable: false`(§3-4-7). v2.3 걸음은 재생보다 길어(이웃 먼저 · 목록 · 걸음 1 섹션 2) cut 줄이 늘 수 있다 — WORK-009 T-2 가 `expand(fact_ids)` 실물 응답 바이트로 다시 재고, p95 가 15,000 을 넘으면 보고(값 바꿈은 코디 · 사용자 · X-2). Sonnet 이 받는 허브 바이트 상한 = 걸음 20,000 + 원문 15,000(+ 안전 요약) — 공정성 보고에 case1 · 2 받은 바이트(rerun-v4 중앙 14,071 · 29,606)와 나란히(§3-7)

#### 3-4-7. Claude 에 넘기는 당시 꼴(v2.2; 현행 선별·분할은 §3-4-1-5)

**v2.9 당시 부분 답변 계약(현 구현 아님; 전달 선별·큰 입력은 §3-4-1-5 우선).** 최종 입력에 `retrieval_limits[]{target_key,facet?,section?,pair?,reason,stop}`를 더한다. 이는 의료 사실이 아니라 이번 수집의 한계이며 인용 근거로 쓰지 않는다. 질문의 항목마다 **채택했고 적용 범위가 맞는 인용 가능 fact**로 확인된 부분을 먼저 답하고, 미수신·미확정·차단된 항목만 유보한다. 전체 조회 미완료를 원장 전체 부재라고 단정하지 않는다. 인접 시술/다른 제품/응급 프로토콜을 질문 대상의 직접 근거로 전이하지 않는다(Q017 RF/HIFU→소프웨이브, Q050 응급→통상 용해, Q147 토닝 owner→제모 PIH). 환자별 적합성은 일반 사실과 분리하고 안전 요약·필수 고지·금기·gap·충돌 표시를 유지한다. 관계 응답이 예산 초과로 통째 배제되면 그 안의 resolved/claims/대안은 말하지 않고 별도 채택한 사실에 한해 답한다. 필수 관계만 질문 전부라면 값을 추정하지 않는다. 검수는 지원 사실 사용, 유보 범위, 대상·원천 적합성, 안전 누락을 각각 판정한다.

```json
{
  "intent": {"choice": "I-04", "confidence": 0.9},
  "facts": [
    {"id": "<fact id>", "text": "<원문 — 잘리지 않은 줄(= 원문) 또는 ⑤ 로 받은 원문>", "section": "checks", "source": {"id": "check_condition:C-…", "kind": "check_condition", "name": "…", "edge": "requires_check_unit"}, "step": 2, "rank": 1},
    {"id": "<fact id>", "line": "<앞 39자…>", "section": "recovery", "source": {"…": "…"}, "step": 3, "rank": 7, "cut": true, "quotable": false}
  ],
  "neighbors": [{"id": "…", "kind": "…", "name": "…", "edge": "…", "value": "…"}],
  "safety": {"<노드 id>": {"…": "…"}},
  "claude_contract": {"rule": "<peek 의 claude_contract.rule>", "allowed_fact_ids": ["<인용 가능한 id — 잘리지 않은 줄 + ⑤ 원문>"], "must_show_flags": ["…"]}
}
```

- **「use_first」 순 = 허브 줄 순서**: v3.3 expand 는 `priority` · `use_first` 칸을 내지 않고 **`facts[]` 줄 순서가 우선순위**다(SPEC-005 v3.3 §5-16 인용 계약). 앱은 걸음 순 → 그 걸음 expand 호출 순 → 응답 `facts[]` 순으로 이어 붙이고(중복 제거) 그 순서를 넘김 순서로 쓰며 `rank`(1부터)로 적는다 — 앱이 따로 「먼저 쓸 것」 개수를 정하지 않는다(새 숫자 없음). 허브가 `use_first` 칸을 다시 내면 그 id 를 맨 앞으로(§7-9 X-1)
- ⑤ 원문은 이 순서대로 `cut` 줄만 예산이 찰 때까지 · 못 받은 `cut` 줄은 `line` + `cut: true` + `quotable: false` — 허브 계약 `allowed: "facts_uncut"`(cut 줄은 원문을 받은 뒤에만 인용) 을 그대로. 프롬프트 한 줄(`prompts/case3.md`: 「`quotable: false` 줄은 근거로 인용하지 않는다 — 그 말이 필요하면 『자세한 내용은 확인 필요』 로 말한다」)
- `source` = 그 fact 를 받은 걸음의 노드(시작 노드 섹션이면 S · 이웃이면 그 이웃 · `edge` = 걸음 1 에서 그 이웃을 고른 edge kind) — 「출처 노드」(발주 3)
- `allowed_fact_ids` = 인용 가능한 id(잘리지 않은 줄 + ⑤ 원문) · `must_show_flags` 합집합 · `rule` = peek 의 규칙 문장(걸음당 한 번이 아니라 판에 한 번)
- **당시 규칙**: 걸음에서 안 받은 것은 넣지 않았다. 0.3.10에서는 §3-4-1-5의 반복 탐색과 `retrieval_limits`가 우선한다. 안전 요약은 관련 대상과 출처가 맞으면 전달한다.

#### 3-4-8. 「자료에 없다」 case3 68 · 안 닿은 34 를 걸음 규칙이 덮는 셈(v2.4 · 받는 자리 정의)

SPEC-005 §6-7 (f) · V-16: rerun-v4 case3 「자료에 없다」 류 정확성 실패 68 = 새 꼴로 닿음 5 · **새 꼴로도 안 닿음 34** · 골드 fact 와 인용 불일치 23 · 되돌아감 6. 그 34 행을 §3-4-6 의 **받는 자리 정의**로 다시 놓고, 걸음 1 규칙이 그 자리를 **선택지에 올리는가**를 센다(`spec006-v24-recount.py` · 34 행 목록 = 005 `reach_case3.detail` · 목표 fact = 그 행 인용의 골드 hit **전부**(v2.3 은 앞 6 — W-7) · S = rerun-v4 case3 시작 노드 · 결정론 · 두 번 같음 · Jev 없음).

**「선택지에 뜸」**: 0홉·1쪽 → 그 section 이 걸음 1 섹션 선택지에 뜨고 1쪽에 목표가 있음 · 1홉·1쪽 → 목표를 1쪽에 가진 이웃 X 의 edge kind 가 그 판 규칙의 걸음 1 이웃 종류 안(v2.2 = 묶음 위 3 · peek 앞 4 안 / v2.3 = `order_v23` 종류 · 목록 전부 / v2.4 = `order_v24` 종류 + 계열 · 제품 단위 규칙 · 목록 전부). 그 밖 자리는 걸음 1 선택지로 받을 수 없다.

| 34 행의 자리 | 행 | v2.2 | v2.3 | **v2.4** | 문항 |
|---|---|---|---|---|---|
| 0홉·1쪽 | 4 | 4 | 4 | **4**(그중 섹션 2 의도 3) | Q055 · Q078 · Q098 · Q239 |
| 1홉·1쪽 | 8 | 0 | 5 | **8** | Q106 · Q114 · Q121 · Q124 · Q131 · Q161 · Q169 · Q198 |
| 0홉·2쪽+ | 1 | 0 | 0 | 0 | Q027 |
| 1홉·2쪽+ | 8 | 0 | 0 | 0 | Q070 · Q083 · Q102 · Q117 · Q136 · Q140 · Q141 · Q233 |
| 2홉+ | 5 | 0 | 0 | 0 | Q064 · Q099 · Q133 · Q185 · Q212 |
| 받을 곳 없음 | 8 | 0 | 0 | 0 — 관계 fact 7(`procedure_relation`) · scope 1 | Q020 · Q056 · Q097 · Q112 · Q186 · Q200 · Q201 · Q215 |
| 이름·속성만 | 0 | — | — | — | |
| **합** | **34** | **4** | **9** | **12** | |

- **v2.4 가 34 중 걸음 1 선택지에 올리는 행 = 12**(0홉·1쪽 4 + 1홉·1쪽 8). 같은 정의로 v2.2 규칙은 4 · v2.3 규칙은 9(검수자 셈 「1쪽 기준 9」 와 같음). v2.3 판의 「19」 는 `_node_fact_ids`(계열의 펼친 단위 fact 포함 · 쪽 무시)로 세어 부풀었던 값이다(재검수 F-1)
- 계열 S 의 펼친 단위에만 있던 7 행(v2.3 의 「0홉」 Q083 · Q102 · Q106 · Q121 · Q124 · Q140 · Q233)은 이 정의로 **1홉 · `key_family`** 가 된다 — 그중 1쪽 안 3(Q106 · Q121 · Q124)은 v2.4 표(I-06 · I-01 · I-04 모두 `key_family` 포함)로 뜨고, 1쪽 밖 4(Q083 · Q102 · Q140 · Q233)는 못 닿음으로 센다
- 남은 22 = 1홉·2쪽+ 8 · 0홉·2쪽+ 1(2쪽 — X-12) · 2홉+ 5(대기열로만) · 받을 곳 없음 8(허브 계약 밖 — X-10 · SPEC-005 0.3.4 고정이라 이 판에서 안 바꿈)
- **표본 안**: 34 행 문항은 표 근거 461 행과 겹친다 — 12 는 규칙이 구조적으로 올리는 상한 참고. 실제로 고르는지(Jev) · 받는지는 재실행에서 잰다(§7-8)

### 3-5. 도구 결과 전달 보장(v2 · B-1)

**문제(2차 분류 `fail-triage2.md` §5)**: case2(Claude CLI) 200 응답 614 중 100 호출이 모델에겐 전체보다 작게 전달됐다 — 기록 `output_bytes` 중앙 1,815B vs 허브 전체 중앙 88,671B · 도구별 check_conditions 47 · procedure_card 23 · pair_check 17 · compare 7 · recommend 6 · 잘린 호출이 든 case2 실패 행 56/131(B 35 · C 7). rerun-v3 기록(182문항 · 672 호출)에서 `output_bytes` 1,700~2,300B 가 93건(1,774B 19건 · 1,795B 8건 …)으로 뭉친다 = CLI 가 넘긴 **미리보기** 크기.

**실물 조사(11-01 · 설정까지 · 호출은 WORK-006 WP-0 확인 시험)**:

| 쪽 | 자르는 규칙(실물 · 문서) | 올리는 설정 | 출처 |
|---|---|---|---|
| Claude CLI 2.1.284 | ① MCP 도구 결과 10,000 토큰 넘으면 경고 · **25,000 토큰 기본 상한**(`MAX_MCP_OUTPUT_TOKENS`) ② 그와 **별개로 성공 텍스트 결과가 저장 문턱(글자 수)을 넘으면 파일로 저장**하고 모델에는 약 2KB 미리보기만 — 바이너리(2.1.284)에서 확인된 것: env `MAX_MCP_OUTPUT_TOKENS` · 기본 상수 `P=25000` · 도구 `_meta` 키 `anthropic/maxResultSizeChars` · `persistenceThresholdCeiling` 칸 · 저장 경로 `tool-results/mcp-<name>-blob-…` · 마커 「Output too large (」 · 「). Full output saved to:」 · 「exceeds maximum allowed tokens. Output has been saved to」 · 「Preview (first」 + 변형 3 「Output truncated (… KB total). The full output could not all be saved to」 · 「(… KB total): later output was discarded because this session writes no files」(**`--no-session-persistence` 일 때 — 저장 자체가 안 됨**) · 「Output exceeded the persist limit; only the first … were saved to」. 문턱 「약 50,000 자」 · 「250,000 자까지」 는 공식 문서 · #97622 인용값이고 바이너리에서 숫자를 특정하지 못함 → **WP-0 실측 표 「문턱 실측값」 열로 닫는다**(W-3) · 글자 수 기준 · `MAX_MCP_OUTPUT_TOKENS` 로 안 올라감(문서) ③ **서버가 도구 정의 `_meta["anthropic/maxResultSizeChars"]` 를 주면 그 도구의 저장 문턱이 그 값으로 올라감**(250,000 자까지 실측 보고) | ①: 자식 env `MAX_MCP_OUTPUT_TOKENS` · ③: 허브 MCP 도구 meta(서버 쪽 · `mcp` 2.3 `MCPServer.tool(meta=…)` 지원 확인 11-01) | 공식 문서(code.claude.com/docs/en/mcp 「Unless the server raises a tool's own limit, successful text results longer than 50,000 characters are saved to a file regardless of this variable」) · anthropics/claude-code #97622(2.1.283 실측) · #45770 |
| Codex CLI 0.166.0 | 도구 결과를 **토큰 예산**으로 자른다(바이너리에 `tool_output_token_limit` · `output_token_limit` 키 있음). 잘림 표시 **실물 후보 5(0.166 바이너리 문자열)**: 「Warning: truncated output (original token count:」 · 「<truncated omitted_approx_tokens=」 · 「omitted_due_to_size_limit (overage_bytes=」 · 「 bytes omitted ...」 · 「 tokens truncated」 + 구조 칸 `_codex_executed_tool_call_truncated{original_bytes, max_bytes, omitted_calls}`. 옛 이슈의 「[... output truncated to fit」 · 「[... omitted k of n lines」 는 0.166 에 **없음**(쓰지 않는다). 어느 것이 실제로 나오는지는 WP-0 에서 한도를 일부러 작게 한 호출로 받아 고정 | `-c tool_output_token_limit=<n>`(전체) · `-c mcp_servers.hub.tools.<도구>.output_token_limit=<n>`(도구별 · 20% 직렬화 여유 앞 값 · 0.152+) | 공식 config 참조(learn.chatgpt.com config-reference) · openai/codex #5913 · #14206 |
| 앱(관찰) | rerun-v3 case2 에 `bash` 호출 10건(Q078 · Q105 · Q150 · Q161 · Q165 · Q166 · Q170 · Q171 · Q174 · Q202 — 전부 저장된 `tool-results` 파일을 `grep` · `jq` · `cd` 로 읽으려 함 · 전부 `is_error` · 68B) — `--tools ""` 로 Bash 가 꺼져 있어도 모델이 미리보기의 파일 경로를 보고 시도했다. 공정성 · 격리 둘 다에 흔적을 남긴다 | §4-2 `stray_tool` 기록 · 끝 조건 0 | rerun-v3 기록 |

**결정 — (a) 설정으로 한도를 올려 허브 응답 전체를 모델에 그대로 넘긴다.** 세 후보 중 하나:

| 후보 | 판정 | 근거 |
|---|---|---|
| **(a) CLI · 도구 한도 설정** | **채택** | 모델이 받는 바이트 = 허브 응답 전체(10-30 결정 「입력 상한 셋 다 없음」과 같은 뜻) · 두 CLI 모두 공식 설정이 있다(Claude = 도구 meta + env · Codex = config 키) · 앱에 새 부품 없음 · case3 가 프롬프트로 전체를 받는 것과 같은 조건. 조건: 허브 MCP 도구 12(골드 9 · 원장 3)에 `_meta["anthropic/maxResultSizeChars"] = MCP_RESULT_MAX_CHARS`(SPEC-005 §5-0 · §5-12 한 줄 — v3.2 planner 에 전달 · §7-7 W-2) · 자식 env `MAX_MCP_OUTPUT_TOKENS`(같은 값을 토큰으로 — 200,000) · Codex `tool_output_token_limit`(200,000) · **WP-0 확인 시험**(실물 호출 1회씩 · 코디 승인)에서 잘림 0 이어야 채택이 선다 — FAIL 이면 escalation(자동으로 (b) 로 가지 않음) |
| (b) 앱 쪽 MCP 프록시가 결과를 나눠 `page=` 로 이어 주기 | 닫음 | 모델이 다음 페이지를 **부를지 말지 고르게** 된다 → 「전체를 받는다」 보장이 모델 행동에 기댐 · 왕복 · 비용 증가 · case3(프롬프트로 한 번에) 와 조건이 달라짐 · 새 부품(프록시 · 캐시) · 페이지마다 50,000 자 · 25,000 토큰 둘 다 아래여야 해 한국어 JSON 이면 페이지 수가 큼. (a) 가 확인 시험에서 서면 필요 없다 |
| (c) 모델에 Read 도구 허용(저장 파일 경로) | 닫음 | Claude 전용(Codex 에 같은 경로 없음 → 두 provider 조건 불일치) · 모델이 읽을지 말지 고름 · 파일 도구 = 격리 깨짐(위 `bash` 10건이 바로 이 길) · `--no-session-persistence` 때 저장 경로 보장 없음 |

- **전달 보장 정의**: 허브 호출마다 `delivered_bytes`(모델이 받은 도구 결과 바이트 = 지금 `output_bytes` 의 뜻을 이 이름으로 명확히 · `output_bytes` 는 호환 칸으로 같은 값) = `hub_bytes`(같은 입력으로 허브가 돌려준 전체 바이트 — §4-4 검증 스크립트가 재호출로 셈 · 결정론) 이고 `truncated: false`. `truncated` 판정은 **마커 목록 = 설정 상수 `TRUNCATION_MARKERS`**(provider 별 문자열 목록 · 위 표의 Claude 4 + 변형 3 을 넣고 시작 · Codex 는 실물 후보 5 를 넣고 시작 · **WP-0 확인 시험이 실제로 나온 문자열로 고정** — 상수는 `config.py` · 기록 `settings.truncation_markers_sha`)로 앱이 결정론으로 매긴다 · 판정 뒤 `delivered_bytes < hub_bytes` 인데 마커가 없으면 `truncated: "unknown"`(끝 조건에선 잘림으로 셈)
- 원장 MCP 3(case1)도 같은 meta · 같은 env — `raw_get` 의 `max_bytes` 20,000(SPEC-005 §5-12) 은 허브 쪽 응답 규칙이라 그대로(모델이 더 읽으려면 offset 으로 — 그건 「자른 것」이 아니라 「도구 계약」)
- SDK 판: `TOOL_RESULT_MAX_BYTES=0`(없음)으로 두 판을 같게(§2-5)

#### 3-5-1. WP-0 결과 반영(v2.2 · `work006-report.md`)

- **Claude `TRUNCATION_MARKERS` = 비움**(실물 2회 · 허브 meta 200,000 + `MAX_MCP_OUTPUT_TOKENS` 200,000 · 1,000 둘 다 마커 없이 100,901B 그대로 전달 · F-3 · 코디 결정 A). 위 표의 Claude 4 + 변형 3 은 상수에 넣지 않는다(없는 문자열로 판정하지 않음). Codex 는 바이너리 시작값 5 그대로 · **실물 미확인**(§7-9 X-5) · SDK 는 앱 `cap_text` 표시
- **잘림 판정 = 바이트 대조**(마커가 없으므로 이것이 본 판정): `verify_runs` 가 같은 입력으로 허브 REST 를 다시 불러 `hub_bytes` 를 세고, **JSON 값 정규화 뒤**(정수 값 실수 `14.0` → `14` — MCP 가 정수로 씀 · f8533ff) `delivered_bytes < hub_bytes − 8` 이면 잘림(fail-triage2 와 같은 여유) · `0 < hub − delivered ≤ 8` 은 「근소 차이」 · 그때 `is_error` 면 「기록 오류」 · 빌드 해시가 다르면 「대조 불가」 — 셋 다 따로 센다. 끝 조건의 「잘린 호출」 = 잘림 + unknown(근소 차이 · 기록 오류 · 대조 불가는 별도 보고 · 대조 불가 0 은 그대로 조건)
- rerun-v4: case2 잘림 0/484 · case1 0/1023 · unknown 0 · 대조 불가 0 → §7-6 「잘린 호출 0」 통과 · v2.2 는 이 판정을 유지한다

### 3-6. intent 전달(v2 · B-1)

- 2차 분류: case2 허브 호출 662 중 Claude 가 `intent` 를 넘긴 호출 **14(2.1%)** · case3 는 앱이 전부(159/159). 허브 v3 는 `intent` 가 없으면 도구 기본 의도로 묶음 · 동봉을 붙이므로(SPEC-005 §5-0) case2 는 질문 의도와 다른 묶음을 받고 있었다
- **규칙**: ① `prompts/case2.md` 에 한 줄 — 「허브 도구를 부를 때마다 `intent` 를 반드시 넘긴다 · 의도 표: I-01 고민 → 추천 · I-02 시술 설명 · I-03 주의 · 사후관리 · I-04 부작용 · 합병증 · I-05 회복 · 효과 기간 · I-06 비교 · I-07 같이 · 순서 · 간격 · I-08 이전 시술 뒤 가능? · I-09 나한테 해도 되나(확인 조건) · I-10 용량 · 회차 · 제품 · I-11 추천 조합 · I-12 가격」(SPEC-005 §5-1 의도 열 그대로 · 프롬프트 판 sha 바뀜 → `versions.prompts.case2`) ② 허브 MCP 도구 설명 · 스키마의 `intent` 를 「선택」에서 「반드시 넘김 · 의도 표」로(스키마 자체는 허브 — SPEC-005 §5-0 · v3.2 planner 에 전달 · §7-7 W-2 · 필수(required)로 만들지는 허브가 정함 — 앱 끝 조건은 비율로) ③ case1 원장 도구 3 은 `intent` 가 없다(해당 없음) ④ Codex 판도 같은 프롬프트 줄
- **기록**: `tool_calls[].intent_passed: true|false|null` — 스키마에 `intent` 가 있는 도구만 true/false · 없으면 null · **true 는 값이 I-01~I-12 에 들 때만**(`"none"` · 빈 값 · 그 밖 문자열은 false — rerun-v3 의 14 중 2 가 `"none"` 이었고 허브는 모르는 값을 4xx 로 냄 · W-5) · 틀린 값은 `intent_values{}` 에 그대로 셈 · 판마다 `trace.intent_ratio = passed / 해당 호출` · `intent_values{}` · 보고서(`report` · `rerun_report`)에 「intent 전달 비율」 열(케이스 · provider 별)
- **v2.3**: case3 의 intent 비율은 **되돌아가기 경로 호출**(`trace.hub`)과 `walk.intent` 가 I-01~I-12 인 판의 비율로 센다(걸음 경로 peek · expand 는 `intent` 를 안 넘기는 것이 규칙 — §3-4-1 · 그 호출은 분모에 넣지 않음) · rerun-v4 의 case3 182/182 는 옛 셈(걸음 호출에도 넘김)

### 3-7. 공정성 원칙(v2)

세 케이스 · 두 CLI · SDK 판이 **모델에 주는 허브 자료의 양과 전달**을 같은 규칙으로 한다. 10-30 「입력 상한 CLI 판 셋 다 없음」 을 이 조항으로 정리한다.

| 원칙 | 값 | 어디서 |
|---|---|---|
| 허브 바이트 상한 | **없음**(세 케이스 · 두 판 같음) — 양은 허브 응답 규칙(SPEC-005 slim · sections · 상한)과 모델의 선택(case1 · 2 도구 호출 · case3 Jev 걸음)이 정한다 · 앱은 자르지 않는다 | §2-5 · `TOOL_RESULT_MAX_BYTES=0` · `input_cap_bytes: null` |
| 전달 보장 | 허브가 돌려준 바이트 = 모델이 받은 바이트(§3-5) · 세 케이스 · 두 CLI · SDK 판 전부 | §3-5 설정 · §4-4 검증 |
| intent | 허브 호출마다 의도를 넘긴다 — case2 는 모델이(프롬프트) · case3 는 앱이(Jev 의도 — **v2.3: 되돌아가기 경로 호출만** · 걸음 경로는 허브가 무시하고 바이트 셈만 어긋나서 안 넘김 · 의도는 `walk.intent` 기록 · §3-4-1) · case1 해당 없음 | §3-6 |
| 모델 · effort · thinking · 프롬프트 공통부 · 시작 `t0` | 같음(§3-1 · §2-5) | — |
| 걸음 예산(case3 걸음) | B 는 **Jev 가 고르는 양의 상한**이지 잘라 내는 상한이 아니다 — expand 를 통째로 넣거나 뺀다(§3-4-1) · 비교 보고에 `bytes_total` 을 case1 · 2 도구 결과 합과 나란히 | §3-4 |
| 격리 | 모델이 세션 도구 목록 밖 이름을 부른 호출(`stray_tool`)은 0 이어야 함 · v2.2: `stray_kind` 로 나눔 — `foreign`(내장 · 다른 서버 · 지어낸 이름) 이면 그 판 「격리 깨짐」 · `bare_hub`(접두만 빠진 허브 도구 이름 — CLI 가 「No such tool available」 로 막음 · 허브 호출 없음) 이면 「이름 틀림」 · 끝 조건 0 은 둘의 합 | §3-8 · §4-2 · §7-8 |

### 3-8. stray 15 — 원인 · 막는 법(v2.2 · 읽기 · 결정론 조사)

**무엇**: rerun-v4 case2(claude-cli 2.1.284 · 프롬프트 case2 `7f4810a3bab1` · 앱 0be5ca6)에서 `mcp__hub__` 접두 없는 허브 도구 이름 호출 15건(호출 521 중 · 15 문항 · 문항당 1). rerun-v3 의 `bash` 10건은 `--disallowedTools` 로 0(같은 배치 내장 도구 0).

| 문항 | 차례 | 부른 이름 | 오류 B | 직전 도구 | 바로 다음 호출 | 입력 꼴 |
|---|---|---|---|---|---|---|
| Q031 | 2/3 | procedure_card | 78 | resolve | `mcp__hub__procedure_card` 같은 입력 · 성공 | 정상 |
| Q066 | 5/6 | check_conditions_placeholder | 92 | resolve | check_conditions · 성공 | 빈 `{}` |
| Q089 | 3/4 | expand | 70 | procedure_card | expand(배열로) · 성공 | 배열이 문자열 |
| Q109 | 2/3 | check_conditions | 80 | resolve | check_conditions · 성공 | 빈 |
| Q115 | 2/3 | check_conditions | 80 | resolve | procedure_card · 성공 | 빈 |
| Q125 | 2/4 | procedure_card | 78 | resolve | procedure_card(다른 id) · 오류 | 정상 |
| Q149 | 3/4 | procedure_card | 78 | recommend | procedure_card · 성공 | 빈 |
| Q164 | 2/3 | procedure_card | 78 | resolve | procedure_card(배열로) · 성공 | 배열이 문자열 |
| Q167 | 3/4 | procedure_card | 78 | resolve | procedure_card · 성공 | 빈 |
| Q172 | 4/7 | neighbors | 73 | resolve | neighbors · 성공 | 빈 |
| Q175 | 4/5 | combos | 70 | procedure_card | combos · 성공 | 빈 |
| Q197 | 3/7 | peek | 68 | check_conditions(오류) | peek · 성공 | 빈 |
| Q234 | 4/5 | expand | 70 | procedure_card | expand · 성공 | 빈 |
| Q235 | 2/3 | check_conditions | 80 | resolve | procedure_card · 성공 | 빈 |
| Q239 | 2/3 | procedure_card | 78 | resolve | procedure_card(배열로) · 성공 | 배열이 문자열 |

**사실(결정론 · `spec006-v22-count.md` §D)**:
1. 오류 바이트 = **64 + 이름 길이** 가 15/15 — CLI 2.1.284 바이너리에 있는 문구 `<tool_use_error>Error: No such tool available: {이름}</tool_use_error>`(16 + 31 + 17 = 64 글자) 와 정확히 맞는다(바이너리 문자열 확인 · CLI 실행 없음). 허브는 이 호출을 받지 않았다(CLI 가 자기 도구 목록에서 못 찾아 바로 오류)
2. `system/init.tools`(= 기록 `trace.cli.session_tools`)은 `mcp__hub__` 11 개뿐 · 내장 0 — **CLI 가 접두 없는 이름을 노출한 것이 아니다**
3. 바로 다음 호출이 같은 도구의 접두 이름 13/15(나머지 2 는 다른 허브 도구) — 모델이 오류를 보고 곧바로 고쳐 부름 · 답에는 영향 거의 없음(턴 1 회 · 70~92B)
4. 입력 꼴: 빈 `{}` 10 · 배열이 문자열(`"sections": "[\"recovery\",…]"`) 3 · 정상 2 — 앱 ingest 는 CLI `assistant` 이벤트의 `tool_use.input` 을 그대로 적는다(`cli.py` `_assistant`). 접두 이름 호출(성공)에서는 배열이 문자열인 경우가 0 → 알려진 도구는 CLI 가 스키마로 바로잡고, 모르는 이름은 스키마가 없어 모델이 낸 그대로 남은 것으로 읽힌다(**추정** — 확인 시험 S-2)
5. 차례: 직전 도구가 resolve 인 것 10/15 · 2번째 차례(첫 호출 resolve 바로 다음)는 7/15(Q031 · Q109 · Q115 · Q125 · Q164 · Q235 · Q239 — 나머지 3 은 resolve 를 다시 부른 뒤 · 검수 W-12) · 이름 표기는 모델이 보는 글 곳곳이 접두 없음 — `prompts/case2.md` 「도구 11개(resolve · recommend · procedure_card …)」 · 허브 MCP 서버 `instructions`(「resolve 로 후보 id」) · 도구 설명(「combos(menu=…) 입력으로만」 · 「pair_check」) · 허브 응답 문구(「sections=<이름> · expand 로 받음」)

**원인(판정)**: 모델이 글에 적힌 **짧은 이름**(접두 없음)으로 도구를 부른 것이 원인이고(사실 1 · 2 · 3), CLI 는 목록에 없는 이름이라 「No such tool available」 로 돌려줬다. 「왜 이 15 번만」 인지는 기록으로 가를 수 없다 — 프롬프트의 짧은 이름 목록이 가장 가까운 후보지만 **추정**이라 확인 시험(WORK-009 S-1)으로 닫는다. CLI 버전 동작(2.1.284 가 MCP 도구를 `mcp__<서버>__<도구>` 로만 노출하고 짧은 이름 별칭을 두지 않음)은 사실 1 · 2 로 확인된다.

**막는 법(v2.2 규칙)**:
1. **프롬프트의 도구 이름 = provider 가 실제로 노출하는 이름**: `prompts/case2.md` 의 도구 목록 · 예시를 자리표 `{tool:resolve}` 로 쓰고, 앱이 provider 별로 채운다 — claude-cli `mcp__hub__resolve` · codex-cli 는 Codex 가 노출하는 이름(**실물 미확인** — WORK-009 S-3 에서 `codex` 세션 도구 목록 기록으로 확정 · 그 전엔 codex 판 프롬프트는 지금 그대로) · sdk 는 짧은 이름(앱이 준 도구 이름 그대로). 한 줄 더: 「도구 설명 · 응답에 나오는 짧은 이름(resolve · expand 등)은 위 이름의 도구를 가리킨다」. 프롬프트 판 sha 는 **채운 뒤 글**로 셈(provider 마다 다름 · `versions.prompts.case2`)
2. **기록 나눔**: `tool_calls[].stray_kind: "bare_hub"`(접두만 빠진 허브 도구 이름 — 허브 도구 11 의 짧은 이름이거나 그것으로 시작) `| "foreign"`(그 밖 — 내장 · 다른 서버 · 지어낸 이름) · `stray_fixed_next: bool`(바로 다음 호출이 같은 도구 접두 이름) · 판 `trace.stray_tools` 는 둘의 합(끝 조건 0 은 합으로) · `foreign` ≥ 1 이면 「격리 깨짐」 표시 · `bare_hub` 만이면 「이름 틀림」 표시(§3-7)
3. 허브 쪽 글(서버 instructions · 도구 설명 · 응답 문구)의 짧은 이름은 **고치지 않는다** — 접두는 클라이언트(CLI)가 붙이는 것이라 허브가 알 수 없고, 같은 허브를 SDK 판 · Codex 가 다른 이름으로 본다. 앱 프롬프트 한 줄(1의 둘째 문장)로 잇는다
4. 화면 · 보고서: stray 열을 `bare_hub` · `foreign` 둘로

## 4. 속도 측정 · 기록 꼴

### 4-1. 속도 칸

| 칸 | 정의 |
|---|---|
| `t0` | 서버가 질문을 받은 시각(세 케이스 같은 값 · `perf_counter` 기준) |
| `ttft_ms` | `t0` → 그 케이스 Sonnet 스트림의 **첫 `text_delta`** 도착(thinking 델타 제외 · 어느 바퀴든 처음 나온 글자) — 10-30 Q-3 |
| `ttft_answer_ms` | `t0` → 마지막 Sonnet 호출(답 바퀴)의 첫 `text_delta` — case2 는 도구 바퀴 앞 글이 있을 수 있어 같이 남김 |
| `total_ms` | `t0` → 답 스트림 끝 |
| `stages[]` | `{name, start_ms, end_ms, tokens?}` — case1 · 2: `claude#n` · `tool:<이름>#n` / case3: `hub_resolve` · `jev` · `hub_path` · `claude` (`start_ms` · `end_ms` 는 `t0` 기준) |
| `llm_round_trips` | Sonnet 호출 수(+ case3 는 `jev_calls` 따로) |
| `tokens` | 단계별 Anthropic `usage`(input · output · cache_creation · cache_read) · Jev `usage.input_tokens` |

- 단건 값은 편차가 크다 — 결론은 쌓인 기록의 경향으로 본다(README §3). 「같은 질문 다시」 버튼(§6 · R-8)

### 4-2. 기록 꼴(한 질문 = `runs/runs.jsonl` 한 줄)

README §6 꼴에 아래를 더한다.

```json
{
  "run_id": "…", "asked_at": "…", "question": "…",
  "versions": {
    "answer_model": "claude-sonnet-5-5", "judge_model": "claude-opus-5-5", "extract_model": "…",
    "jev_model": "jev-1.14.0",
    "prompts": {"common": "<sha12>", "case1": "…", "case2": "…", "case3": "…", "judge": "…", "extract": "…"},
    "gold_build_hash": "<골드 응답 머리 build.build_hash>",
    "raw_manifest_sha16": "<원장 MCP 응답 머리 raw.dir_manifest_sha16>",
    "app_commit": "<clinic_chat git sha>"
  },
  "settings": {"thinking": "between_tools", "effort": "high", "tool_loop_max": 12, "jev_confidence_min": 0.3, "jev_option_order_seed": 0},
  "cases": {"case1": {"answer": "…", "stop_reason": "…", "loop_capped": false, "error": null,
                      "timing": {"ttft_ms": 0, "ttft_answer_ms": 0, "total_ms": 0, "stages": [], "llm_round_trips": 0},
                      "tokens": {}, "trace": {}, "word_check": {}, "judge": {}}, "case2": {}, "case3": {}},
  "judge_order": ["case2", "case1", "case3"], "judge_seed": 0
}
```

- **v2 칸**: `provider` · `versions.answer_provider · answer_effort · cli_version · auth_kind · judge_provider` · `settings{thinking, effort, tool_loop_max, max_budget_usd, service_tier, timeout_sec, input_cap_bytes: null, mcp_result_max_chars, walk_max_steps, walk_byte_budget, walk_enough_min}` · case1 · 2 `trace.tool_calls[]{tool, input, delivered_bytes, output_bytes(같은 값 · 호환), hub_bytes?(§4-4 가 채움), truncated: false|true|"unknown", intent_passed, ms, is_error, node_ids[], stray: bool}` · `trace.intent_ratio` · `trace.stray_tools: int` · `trace.cli{…}`(§2-5 · `rate_limits` · `api_retries` · `session_tools` · `mcp_servers` · `observed_model` · `api_key_source` · `num_turns` · `cli_ttft_ms`) · case3 `trace.walk{…}`(§3-4-4) · `timing.ttft_kind · cli_boot_ms · thinking_ms · ttft_ms_ex_boot · total_ms_ex_boot` · `cost{usd, usd_estimate, billed}` · `judge.mode: "absolute"` · 배치 칸(§2-5)
- **v2.2 칸**: `settings{walk_sections_per_step, walk_neighbors_max, walk_first_section_max, walk_full_byte_budget, walk_full_facts_max, order_table_sha}` · case3 `trace.walk` 새 칸(§3-4-4 — `order_kinds` · `steps[].phase` · `peek_reused` · `jev.filtered_by_budget` · `expand.calls[].excluded` · `queue_left` · `neighbor_reached` · `full{…}`) · case1 · 2 `tool_calls[].stray_kind · stray_fixed_next`(§3-8) · `trace.stray_by_kind{bare_hub, foreign}` · `versions.prompts.case2` = provider 별로 채운 글의 sha(§3-8)
- 사람 확인은 `runs/human_checks.jsonl` 에 따로 덧붙임(`{run_id, case, verdict: "맞음|틀림", item?, note, at}`) — 기록 줄은 고치지 않는다
- 기록에 키 · 환경 변수 값을 넣지 않는다

### 4-3. 서버 ↔ 화면 계약(SSE)

`POST /api/ask {question}` → `{run_id}` · `GET /api/runs/{run_id}/events`(SSE) 이벤트: `stage{case, name, start_ms, end_ms}` · `text{case, delta}` · `trace{case, …}` · `case_done{case, timing, tokens}` · `word_check{case, …}` · `judge{cases…}` · `run_done{run_id}` · `error{case?, message}` / `GET /api/runs?limit=` 기록 목록 · `POST /api/runs/{run_id}/human_check` · `POST /api/runs/{run_id}/rerun`

### 4-4. 기록 검증 스크립트(v2 · 결정론)

`clinic_chat/verify_runs.py`(레포 안 · 출력은 레포 밖 `build-out/verify-<batch>.{md,json}`): 배치 하나(또는 run_id 목록)를 읽어 **판단 없이** 센다 · 두 번 돌리면 바이트 같음(시간 칸은 머리 하나).

**0.3.10 현행 추가 검증:** 아래 표의 case3 예산·걸음 관련 행은 과거 배치 재생 지표다. 새 판은 §3-4-1-5의 수집 원장↔Claude 전달 ID·원문·source·scope 대조, 필수 안전/고지 전달, 대상/facet 지원 상태, 분할 묶음 누락, 미완료 범위의 사실 부재 단정, 중복 frontier 호출을 검증한다. 실제 호출 바이트·최종 전달 바이트·모델 컨텍스트 한계를 별도 기록하고, 카테고리 장부 초과를 실패로 세지 않는다.

| 항목 | 셈 | 끝 조건에 쓰는 값 |
|---|---|---|
| 잘림 | case1 · 2 `tool_calls[]` 마다 `truncated`(마커) · `hub_bytes` = **같은 입력으로 허브 재호출**(REST · `intent` 포함 · 결정론 · 허브 빌드 해시가 기록과 같을 때만 · 다르면 「대조 불가」) · `delivered_bytes ≠ hub_bytes` 셈 | 잘린 호출 수 · 대조 불가 수 |
| intent | 스키마에 `intent` 있는 도구 호출 중 `intent_passed` 비율(케이스 · provider · 도구별) | ≥ 95% |
| 격리 | `stray_tools` 합 · 허브 MCP 밖 도구 이름 목록 | 0 |
| case3 걸음 | `walk.steps_n` · `bytes_total` · `stop` 분포 · `fallback` 수 · Jev 호출 수 · ms 합 · peek 바이트 중앙 | 보고 · 되돌아간 판 수 |
| 공정성 | 케이스별 모델이 받은 허브 바이트 합(case1 · 2 `delivered_bytes` 합 · case3 `bytes_total` + peek 합) 중앙값 나란히 | 보고 |
| 잘림(v2.2) | §3-5-1 바이트 대조 — 잘림 · 근소 차이 · 기록 오류 · 대조 불가 따로 · JSON 정수 값 정규화 뒤 | 잘림 + unknown 수 · 대조 불가 수 |
| 격리(v2.2) | `stray_kind` 별 수 · 이름 목록 · `stray_fixed_next` 비율 · 문항 목록 | 합 0 |
| case3 걸음(v2.2 · v2.3) | `steps_n` 중앙(전 판 182 기준 · 되돌아간 판 0 걸음 포함) · `stop` 비율(182 기준) · **이웃 fact 도달**(v2.3 이름 · W-9 — SPEC-005 §6-7 (e) 의 「이웃 peek 도달」 = 방문 노드 ≥ 2 와 다른 칸) = 걸음 판 중 이웃 노드 걸음에서 fact ≥ 1 받은 판 비율 · 이웃 peek 도달(같이 보고) · **34 행 선택지에 뜸**(v2.4 정의 — 커밋본 `spec006-v24-recount.json cover34.rows` 의 34 행 · 「받는 자리」(§3-4-6 · 1쪽) 노드 · 섹션이 그 판 `walk.step1_options` 에 있는 행 수를 0홉 몫 · 1홉 몫으로 나눠 · S 가 rerun-v4 와 같은 행만 문턱 · 다른 행은 보고 · 실제로 고른 행 · 받은 행 수) · `list.bytes` · `bytes_mismatch` 수 · 2홉 도달(보고) · `bytes_total` · `full.bytes` 중앙 · p95 · `excluded` 수 · `filtered_by_budget` 수 · 되돌아감 사유별 · peek 재사용 수 | §7-8 |
| case1 대비 차(v2.2) | §4-5 — 배치 하나면 Δ · 둘이면 Δ 평균 · 두 회 차 · case1 뒤집힘 | 보고 |
| C 비율 | 채점 실패 행마다 fail-triage2 §2 와 같은 셈 — 그 문항의 허브 응답(도구 결과 · 걸음 fact) `facts[].text` 정규화 문자열 ∋ 인용 → C · 케이스 · provider 별 C 건수 · 비율(실패 행 대비) | 보고(교체 동기 「C 10%」 대조 · W-2) |

### 4-5. 비교 규칙(v2.2)

rerun-v3 → v4 에서 case1(바뀐 것 없음)의 정확성이 87 → 83% 로 움직였다 — 같은 문항 판정이 회당 15~20% 뒤집힌다(채점 흔들림 · `_RESUME.md` 11-01). 그래서 판 사이 숫자를 그대로 빼서 결론 내지 않는다.

| 규칙 | 값 |
|---|---|
| 판 안 지표 | **case1 대비 차** Δ = 통과율(caseN) − 통과율(case1) — 같은 배치 · 같은 채점 · 같은 문항(항목별: 정확성 · 안전 · 평균 통과 수 · 「정보 없음」류) |
| 판 사이 비교 | Δ 끼리 비교(전 Δ → 후 Δ) · 통과율 원값은 같이 적되 결론은 Δ 로 |
| 결정 전 2회 평균 | 설정값 바꿈 · 채택 · 되돌림을 정하기 전엔 **같은 앱 커밋 · 허브 빌드 · 프롬프트 판으로 2회**(배치 둘) 돌려 Δ 평균 · 두 회 차이 · **case1 뒤집힘 비율**(두 회 사이 같은 문항 · 같은 항목 판정이 바뀐 비율)을 같이 낸다 — 한 회 결과로는 결정하지 않는다 |
| 누가 | 재실행 · 2회 발주는 코디(구독 사용량) · 앱은 `rerun_report` 에 「case1 대비 차」 · 「2회 평균」(`--batches a,b`) · 「case1 뒤집힘」 열 |
| 기준 배치 | v2.2 전 = rerun-v4 `b202611011148-c6ed3a`(1회뿐 — 보고에 「전 1회」 표시) · v2.2 후 = 같은 판 2회 평균. 「전」 도 2회로 맞출지(옛 앱 판을 한 번 더 돌림)는 코디 · 사용자(§7-9 X-6) |

## 5. 품질 두 층

세 열이 모두 끝나면 ① → ② 순서로 자동(README §5).

### 5-1. ① 단어 검사(결정론 판정)

| 단계 | 규칙 | 근거 |
|---|---|---|
| 이름 뽑기 | LLM 추출(R-4 — `claude-opus-5-5` · effort `low` · 구조화 출력 `output_config.format` 으로 `{names: [{text, kind: 시술\|제품\|장비\|부위\|성분}]}`) · 답 원문만 입력 · **시맨틱 사전 · 원장을 주지 않음**(지어낸 이름을 놓치지 않게) | README §4 ① 1 · O-4 |
| 정규화 | **`semantic.json` `dictionary.resolve_rules.normalize` 그대로** — NFKC → 라틴 악센트 접기(NFKD 결합 부호 제거 · NFC) → 입력 접기 `fold`(「쳐짐」 → 「처짐」) → 공백 제거 → 괄호 `strip_chars`(`()[]`) 지움(안 글자는 남김) → **전부 소문자**. 답에서 뽑은 이름 · 원장 문자열 · 사전 `expr` · `variants` 에 **같은 함수 하나**를 쓴다(`fold` · `strip_chars` 는 `SEMANTIC_JSON` 에서 읽음 — 문서 = 코드). 「영문으로 시작하면 소문자」(README §4 ① 2 · 3단계 lexicon 문구)는 쓰지 않는다 — 한글로 시작하고 영문 대문자가 섞인 원장 문자열(실물 290개 · 예 「필러(HA/CaHA)」 · 「…Nd:YAG)」)이 소문자로 안 바뀌어 거짓 「없는 이름」이 나기 때문(검수 F-1) | `semantic.json` `dictionary.resolve_rules`(note: 사전은 이 규칙 하나) · `semantic.md` §4 · `semantic-build.py:55-63` |
| 대조 | 원장 21 파일의 모든 문자열 값(정규화 뒤)에 그 이름이 부분 문자열로 있나 → 없으면 시맨틱 사전 `dictionary.expressions[].expr · variants[]`(정규화 뒤)와 같은가 | README §4 ① 3 |
| 출력 | 이름마다 `{name, norm, found, where[] (원장 파일 · 경로 · 최대 3), via: "원장\|사전"}` · 열마다 `not_found` 수 | README §4 ① 4 |
| 결정론 | 대조는 결정론 · 뽑기 결과(LLM)는 기록에 그대로 남겨 다시 대조 가능 | — |

- 2자 미만 이름은 대조에서 뺌(부분 일치 거짓 「있음」 방지) — R-4
- 원장은 `RAW_DIR` 로컬 파일을 직접 읽는다(허브 원장 MCP 를 부르지 않음 — 채점 경로가 실험 대상 서버에 기대지 않게) · 시작 때 21 파일 해시를 기록 `raw_manifest_sha16` 과 같은 식으로 셈

### 5-2. ② Opus 채점

| 항목 | 묻는 것 | 값 |
|---|---|---|
| 정확성(관계 · 숫자) | 시술 ↔ 부위 ↔ 고민 관계 · 간격 · 용량 숫자가 원천과 맞나 | 통과 · 실패 · 해당 없음 |
| 안전 정보 | 추천한 시술의 금기 · 주의를 같이 말했나(10-26) | 〃 |
| 후보 처리 | 뜻이 갈리는 말을 단정하지 않고 고르거나 되물었나(10-27) | 〃 |
| 불확실 표시 | 근거 약 · 정보 없음을 「안전함」 · 「확실함」처럼 말하지 않았나 | 〃 |
| 질문에 답함 | 물은 것에 답했나 · 새지 않았나 | 〃 |

- 항목 = README §4 ② 5개 그대로(O-5 → R-9 「5개 그대로 시작」). 「지어낸 말」은 ① 몫
- **가리기**: 세 답을 seed 로 섞어 A · B · C 로만 보여 줌 · case 이름 · 도구 흔적 · 속도 안 보임 · `judge_order` · `judge_seed` 기록
- **기준 자료(O-3 → R-10 = B 원장)**: Opus 에 원장 도구 3(`raw_list` · `raw_get` · `raw_search`)을 준다 — 원장 전체를 넣지 않고 필요한 곳만 찾아 읽음(README 의 B 「크기 문제」를 도구로 풂) · 골드 결과는 주지 않음(C 는 case2 · 3 에 유리)
- **원장 도구는 앱 안 로컬 구현**(`quality/raw_tools.py`): SPEC-005 §5-12 R1~R3 과 같은 이름 · 입력 · 출력 계약 · `RAW_DIR` 로컬 원장 파일을 읽는다 · 허브 원장 MCP 를 부르지 않는다 — ① 과 같은 이유(채점 경로가 실험 대상 서버에 기대지 않게 · 기준 하나 · 검수 W-3). case1 이 쓰는 허브 원장 MCP 와 계약이 같은지는 WORK-004 Phase 7 실물 대조에서 확인
- **근거 인용 필수**: 실패마다 `{item, answer: A|B|C, claim, evidence: {file, path, quote}}`. 앱이 `quote` 가 그 경로 원문에 실제로 있는지 원장 로컬 파일로 확인 → 없으면 그 실패는 `invalid`(무효 · 화면에 회색)
- 호출: `claude-opus-5-5` · thinking 기본(Opus 5.5 는 못 끔) · effort `medium` 명시(기본값) · `tool_choice: auto` · 도구 루프(상한 `CASE_TOOL_LOOP_MAX`) 뒤 마지막 응답을 구조화 출력(`output_config.format`)으로 받음
- **사람 확인**: 열마다 「맞음 · 틀림」 + 메모(README §4 「처음 몇 건은 사용자가 채점관 검수」) — §4-2 `human_checks.jsonl`

## 6. 화면

README §5 와이어 그대로 + 질문 기록 목록.

```
┌────────────────────────────────────────────────────────────┐
│ ⚠ 환자 정보 넣지 말 것 · 질문과 노드 이름이 Jev(미국)로 나감   │
│ 질문 [                                          ] [보내기] │
├──────────────────┬──────────────────┬──────────────────────┤
│ case1 원장 MCP   │ case2 골드 MCP   │ case3 골드 + Jev     │
│ ⏱ 첫 글자 / 전체 │ ⏱ 첫 글자 / 전체 │ ⏱ 첫 글자 / 전체     │
│ ▓▓ ▓ ▓▓ 왕복     │ ▓▓ ▓ ▓▓ ▓▓ 왕복  │ ▏hub ▓ jev ▏hub ▓▓ claude │
├──────────────────┼──────────────────┼──────────────────────┤
│ [답변 스트리밍]  │ [답변 스트리밍]  │ [답변 스트리밍]      │
├──────────────────┼──────────────────┼──────────────────────┤
│ ▸ 원장 도구 N    │ ▸ 도구 호출 N    │ ▸ Jev 의도 · 슬롯    │
│   입력 · 결과    │   입력 · 결과    │   confidence(낮음 ⚠) │
│   토큰 수        │   쓴 노드 id     │ ▸ 허브 경로 · 노드 id│
├──────────────────┼──────────────────┼──────────────────────┤
│ ① 없는 이름 N    │ ① 없는 이름 N    │ ① 없는 이름 N        │
│ ② 항목별 ●/✕     │ ② 항목별 ●/✕     │ ② 항목별 ●/✕         │
│   (실패 근거)    │                  │                      │
│ [사람 확인 ✓✗]   │ [사람 확인 ✓✗]   │ [사람 확인 ✓✗]       │
└──────────────────┴──────────────────┴──────────────────────┘
  [같은 질문 다시 ×3]
  ↓ 질문 기록 — 한 줄씩: 시각 · 질문 · 열별 total_ms · 없는 이름 수 · ② 통과 수 · 사람 확인 · 판(골드 해시 앞 8자)
```

- 단계 막대 = `stages[]` 를 `t0` 기준 가로 시간축으로(열마다 같은 눈금)
- 기록 줄을 누르면 그 질문의 3열을 기록에서 다시 그림(다시 호출 안 함)
- 얼굴 지도 패널 없음(README §5)

## 7. 열린 것 처리표

### 7-1. README 열린 것 O-1~O-9

| # | 무엇 | 처리 | 근거 · 값 |
|---|---|---|---|
| O-1 | case1 원장 넣는 방식 | **결정됨** — 원장 MCP 도구 3 | 10-30 Q-1 · 「원장도 MCP 로」 |
| O-2 | 세 케이스 시스템 프롬프트 | **결정됨** — R-5 | README 선택지 「답 문장 지시는 같게 · 데이터 · 도구 설명만 다르게」 |
| O-3 | Opus 기준 자료 | **결정됨** — R-10(B 원장 — 앱 안 로컬 원장 도구로) | README 「논의에선 B 기본」 |
| O-4 | ① 이름 뽑기 방법 | **결정됨** — R-4(LLM 추출 · Opus 5.5) | README 선택지 |
| O-5 | 품질 항목 최종 목록 | **결정됨** — R-9(5개 그대로) | README §4 ② |
| O-6 | Jev 호출 꼴 | **결정됨** — 이 스펙 §3-4(의도 12 · 슬롯 = SPEC-005 vocab · 도구 입력) · 세부 값 R-6 · R-7 | SPEC-005 §5 · Q-4 · Q-5 · Q-7 |
| O-7 | 허브 도구 목록 · 의도별 경로 | **결정됨** — SPEC-005 §5(도구 9 · 경로) · §5-12(원장 3) | SPEC-005 |
| O-8 | 화면 · 실행 위치 | **결정됨** — 레포 `kknaks/clinic_chat`(공개 · §2-3 경로) · 스택 R-1 | 10-30 |
| O-9 | 모델 키 | **결정됨** — 사용자 보유 · env 로만 · Claude 는 API 키 별도 | D-11 · 10-30 |

### 7-2. Jev 조사 Q-1~Q-8(10-30 사용자 「응」 — 전부 결정됨)

| # | 결정 | 이 스펙 |
|---|---|---|
| Q-1 | case1 = 원장 MCP | §3-2 |
| Q-2 | Anthropic Python SDK + MCP 클라이언트 직접 루프 | §2-1 |
| Q-3 | ttft = 첫 텍스트 델타 · thinking 끔(세 케이스 같게) | §3-1 · §4-1 |
| Q-4 | 255 넘으면 허브 사전 검색으로 후보 줄인 뒤 Choice | §3-4 |
| Q-5 | 되묻기 문턱 0.3 시작 · 기록 보고 조정 | §3-4 · env `JEV_CONFIDENCE_MIN` |
| Q-6 | `jev-1.14.0` 고정 | §2-1 · env |
| Q-7 | 노드 목록 앱 시작 1회 캐시 | §3-4 |
| Q-8 | 영어 병기 안 함(처음) | §3-4 슬롯 설명 한국어만 |

### 7-3. R-1~R-10 — 결정됨(10-30 사용자 승인)

이 스펙이 추천한 값을 사용자가 10-30 한 번에 승인했다. 다시 논의하지 않는다(값 조정은 기록을 보고 사용자가 정함).

| # | 무엇 | 결정 | 이유 |
|---|---|---|---|
| R-1 | 서버 · 화면 스택 | FastAPI + SSE + 빌드 없는 정적 페이지 | 화면 하나 · 로컬 · 실행 명령 하나 · 의존성 적음 |
| R-2 | case1 · 2 도구 루프 상한 | Sonnet 호출 12번 · 닿으면 `tool_choice none` 으로 마지막 답 1번 + `loop_capped` | 무한 루프 · 비용 막기 · 셈은 기록으로 조정 |
| R-3 | Sonnet effort | `high`(모델 기본값 명시) · 세 케이스 같음 | `between_tools` 가 high 이하만 받음 · 기본값이면 따로 고른 것이 없음 |
| R-4 | ① 이름 뽑기 | `claude-opus-5-5` · effort low · 구조화 출력 · 2자 미만 제외 | 이미 정해진 채점 모델 — 새 모델을 들이지 않음 · 답 모델(Sonnet)과 달라 자기 답 편들기 없음 |
| R-5 | 프롬프트 | 공통부 같음 + 케이스별 데이터 · 도구 설명만 | README O-2 선택지 |
| R-6 | 여러 고민 슬롯 | 고민 Choice 1 + ① 후보 고민마다 Noul(0.5 이상이면 더함) | Choice 는 하나만 고름(jev-research §2-3 문서 패턴) |
| R-7 | Jev 선택지 순서 | seed 로 섞고 기록 | 앞쪽 기울기(jev-research §2-3) |
| R-8 | 같은 질문 다시 | 버튼 · 3회 · 중간값 표시 | README §3 「필요하면 재실행 버튼(중간값)」 |
| R-9 | 품질 항목 | README 5개 그대로 시작 | O-5 |
| R-10 | Opus 기준 자료 | B 원장 — 원장 도구 3 을 Opus 에 줌 · **도구는 앱 안 로컬 구현**(SPEC-005 §5-12 R1~R3 과 같은 계약 · `RAW_DIR` 로컬 원장 파일 · 허브 원장 MCP 안 부름) | README 「B 기본」 · 크기 문제를 도구 조회로 풂 · C 는 골드 쪽에 유리 · ① 과 같이 채점이 실험 대상 서버에 기대지 않게(검수 W-3 · 코디 판단) |

### 7-4. 사용자 몫

| # | 무엇 | 왜 사용자만 |
|---|---|---|
| U-1 | Jev 콘솔 접근 · 키 발급(`console.typesafe.ai`) · 조직 rate limit 확인 | **완료(10-30)** — 키 받음 · 사용자가 워크트리 `.env` 에 직접 넣음 |
| U-2 | Anthropic API 키를 `.env` 에 넣기(충전된 API 키 · 구독 아님) | **완료(10-30)** — 키 받음 · 사용자가 워크트리 `.env` 에 직접 넣음 |
| U-3 | R-1~R-10 승인 · 바꿈 | **완료(10-30)** — 승인(§7-3) |
| U-4 | 실험 중 사람 확인 표시 · 문턱(0.3) 조정 판단 | README §4 · 10-30 Q-5 「기록 보고 조정」 — 실험하면서 |

### 7-5. 남은 열린 것

0.3.15의 원천상 미확정 사항은 §3-4-1-9의 combo exact site·note pair/subject·product 선택/override·patient 언어 qualifier 보존이다. 해당 절의 scope 보존/영향 branch hold 기본은 확정됐지만 원천 정보 자체는 해소되지 않았다. 기존 열린 결정과 구분해 유지한다.

| # | 무엇 | 선택지 | 지금 |
|---|---|---|---|
| L-1 | 실험 기록(`runs.jsonl` · `human_checks.jsonl`) 저장 위치 | (가) 레포 안 `runs/` 폴더 · 커밋 안 함 / (나) 레포에 커밋 | **닫힘(10-30 사용자)** — `RUNS_DIR` = 프로필 레포 `reference/2026-10-30-hub-evals/runs/`(사용자가 봄 · 프로필 `.gitignore` 에 `runs/` · 커밋 안 함) · 앱 레포에도 안 들어감(§2-5) |

### 7-6. v2 끝 조건(측정)

| 항목 | 재는 법 | 통과 |
|---|---|---|
| **잘린 호출 0** | WP-0 확인 시험(Claude · Codex 각 실물 1회 · 큰 결과 도구 — check_conditions 계열 · procedure_card `sections=all`) 뒤, **case2 182문항 재실행**(rerun-v3 와 같은 문항 · 같은 채점 · 코디 발주)의 §4-4 검증 | `truncated` true · unknown 합 **0** · 대조 불가 0 |
| **intent 전달 ≥ 95%** | 같은 재실행 · §4-4 | 스키마에 `intent` 있는 호출 중 ≥ 95%(케이스 · provider 별 각각) |
| **격리** | §4-4 `stray_tools` | 0 |
| **case3 교체 비교** | case3 걸음 판 182문항 재실행(SPEC-005 v3.2 peek/expand 완성 뒤 · 코디 발주) → `rerun_report` 전후(rerun-v3 case3 기준) | 보고(통과율 · 「정보 없음」류 · **C 건수 · 비율**(§4-4 · 전 10%) · 첫 글자 · `bytes_total` 중앙 · 되돌아간 판 수 · Jev 호출 수 · 시간) — 통과 기준은 사용자가 보고 뒤 정함(§7-7 W-4) |
| **기록 검증 결정론** | `verify_runs.py` 두 번 | 바이트 같음 |
| **기존 시험 전부** | `uv run pytest -q` · ruff · 레포 규칙 시험(`test_repo_rules.py`) | 통과 · 회귀 0 |

### 7-7. v2 아직 안 정한 것(추측으로 메우지 않음)

| id | 무엇 | 추천(본문에 쓴 값) | 누가 |
|---|---|---|---|
| W-1 | `peek` · `expand` 의 정확한 응답 꼴 · 새 도구인지 기존 도구 모드인지 — **SPEC-005 v3.2 §(peek · expand) 의존**(코디가 v3.2 발주 보충 2 로 전달 · 11-01 확인) | 앱은 §3-4-2 최소 칸만 기대 · `hub_rest.py` 두 함수로 감쌈 | SPEC-005 v3.2 planner |
| W-2 | 허브 쪽 두 줄 — MCP 도구 12 의 `_meta["anthropic/maxResultSizeChars"]` · `intent` 설명 「반드시 넘김 · 의도 표」(required 여부) — **SPEC-005 v3.2 §5-0 · §5-12 의존**(보충 2 로 전달 · 확인) | required 는 허브 판단 · 앱 끝 조건은 비율 | SPEC-005 v3.2 planner |
| W-3 | `WALK_ENOUGH_MIN`(「충분」 Noul 문턱) · 걸음당 이웃 수 3 · 2단 Choice 꼴 | 0.5(R-6 과 같은 값) · 3 · kind → id — **v2.2: rerun-v4 근거로 0.5 · 3 유지 + 걸음 1 에 「충분」 없음 · 걸음당 섹션 2(§3-4-1 표)** | 사용자(기록 보고 조정 · Q-5 와 같은 방식) |
| W-4 | **11-01 사용자 수락으로 닫힘**: case3 제품 목표는 182문항×2회 평균 정확성 ≥58%, 안전 ≥90%, 첫 글자 ≤7초(`_RESUME.md` 11-01 기록). 11-02 fullrun-v2 239×3은 정확성 67.5·첫 글자 6.2초이나 안전 87.5%로 목표 미달(`_RESUME.md` 11-02). v2.9 고정 50×1은 진단 관문이며 이 기준을 그대로 최종 합격으로 대입하지 않는다 | 182×2 목표 확정; 50→239×3 승격의 개선량·TTFT 악화 허용치는 별도 OQ | 사용자 |
| W-5 | `MCP_RESULT_MAX_CHARS` 200,000 · `MAX_MCP_OUTPUT_TOKENS` 200,000 · Codex `tool_output_token_limit` 200,000 — 허브 최대 응답(2차 분류 p95 171KB · 최대 281KB)을 덮는 값. Codex 0.166 실물 마커 · 한도 동작은 WP-0 에서 확인 | 200,000 · WP-0 뒤 조정 — **v2.2: WP-0 에서 잘림 0 · 그대로**(§3-5-1) · Codex 는 X-5 | WP-0 결과 · 코디 |
| W-6 | `bash` 10건의 원인(`--tools ""` 인데 모델이 Bash 를 냄 — 모델 환각인지 CLI 가 내장 도구를 남기는지) | WP-0 에서 `system/init.tools` 로 확인 · `--disallowedTools Bash,Read,Grep,Glob,Edit,Write` 를 더해 둘 다 막음 — **v2.2: 닫힘**(내장 0 · bash 0) · 대신 생긴 접두 없는 이름 15 는 §3-8 | WP-0 |


### 7-8. v2.2 · v2.3 · v2.4 당시 끝 조건(0.3.10 수용 기준 아님)

| 항목 | 재는 법 | 통과 | rerun-v4(전) |
|---|---|---|---|
| **case3 걸음 중앙 ≥ 3** | §4-4 `steps_n` 중앙 · 182 기준(되돌아간 판 포함) · 2회 각각 | 두 회 모두 ≥ 3 | 1 |
| **예산 멈춤 ≤ 30%** | `stop == budget` / 182 | 두 회 모두 ≤ 30% | 116/182 = 64% |
| **이웃 fact 도달**(v2.3 이름 · W-9) | 걸음 판 중 이웃 노드 걸음에서 fact ≥ 1 받은 판 비율(SPEC-005 §6-7 (e) 「이웃 peek 도달」 과 다른 칸 · 둘 다 보고) | **≥ 80%**(추천 — §7-9 X-4) | 49/148 = 33%(이웃 peek 도달 79/148) |
| **34 행 · 1홉 몫**(v2.4 · 받는 자리 정의 · W-4) | §3-4-8 의 1홉·1쪽 8 행(Q106 · Q114 · Q121 · Q124 · Q131 · Q161 · Q169 · Q198) 중 **그 판 시작 노드가 rerun-v4 와 같은 행**(분모) × 그 판 `walk.step1_options` — 목표를 1쪽에 가진 이웃 X 가 걸음 1 이웃 선택지에 있는가 · 2회 각각 | **분모 행 전부 뜸**(셈 값 8/8 — 규칙이 바꾸는 몫) · 분모 크기 · S 가 바뀐 행은 보고 | 0/8(v2.2 규칙 · 같은 정의) |
| 34 행 · 0홉 몫 · 합(v2.4) | 0홉·1쪽 4 행(Q055 · Q078 · Q098 · Q239) — S 같으면 섹션 목록으로 늘 뜸(규칙과 무관 · Jev 의 시작 노드 고름을 잼) · 합 = 0홉 + 1홉 | 보고(셈 값 4 · 합 12) · 실제로 고른 행 · 받은 행 수 | 4 · 합 4(v2.2) |
| 바이트 셈 일치(v2.3 · F-1) | `walk.bytes_mismatch` 합 | 0 | — |
| **stray 0** | §4-4 `stray_by_kind` 합(case1 · case2 · provider 별) | 0 | 15(bare_hub 15 · foreign 0) |
| 되돌아감 | `fallback` 수 · 사유별 | 보고(첫 expand 초과 · 「없음(충분)」 사유는 0 이어야 함 — 규칙으로 없어짐) | 34(no_start 11 · no_facts 23) |
| 예산 안 크기 | `bytes_total` 중앙 · p95 · `full.bytes` 중앙 · p95(원문 예산 15,000 넘은 판 수) · `list.bytes` · `excluded` · `filtered_by_budget` 수 | 보고 · §3-4-6 추정표와 대조(다르면 표 고침) | 13,951(중앙) |
| 정확성 · 안전 | §4-5 case1 대비 차(2회 평균 · 두 회 차 · case1 뒤집힘) | 기준은 사용자(W-4) | case3 Δ 정확성 −34%p · 안전 −26%p(1회) |
| 잘린 호출 · intent · 결정론 · 기존 시험 | §7-6 그대로 | §7-6 그대로 | 통과 |

- 「rerun-v4(전)」 Δ 는 `rerun-v4-vs-v3.md` 의 case1 83% · 89% 대비 case3 49% · 63%
- 재실행 전 허브는 SPEC-005 v3.3(WORK-008) 빌드로 코디가 재시작 · 앱은 WORK-009

- **v2.5 재측정(메모 5)**: case3 만 182 × 2회(**rerun-v6a · v6b**) · 통과 기준 W-4 그대로(사용자) · 위 표의 걸음 · 예산 · 이웃 · 34 행 칸은 같은 셈으로 보고 · 새 칸(필수 묶음 · 고정 섹션 · 「충분」 무시 횟수) 보고
- **회귀(v2.6 · 검수 F-1)**: 허브 v3.4(G20) + 앱 I-04 `safety.management` 반영 뒤 재실행에서 case3 I-04 판이 받은 줄 중 관리 · 예방 fact(`CX-…#management` · `#prevention` · `SE-…#management` · `#prevention`) 수가 **v3.4 전(같은 54 가 `safety.complications` 에 있던 rerun-v6a/b) 이상** · I-04 안전 · 정확성은 §4-5 case1 대비 차로 보고 — 0 이면 고정 섹션 누락 회귀
- **v2.8 확인(메모 4)**: 실물 1문항 + **v8a 안전 실패 13 행 문항만 재생(채점 없이 걷기 · 결정론)으로 그 인용이 받는 줄에 들어오는지 셈** → 수 보고
- **v2.8 전체 실행(메모 5)**: 그다음 **239문항(question-set.json 전체) × case1 · case2 · case3 · claude-cli Sonnet · Opus 열마다 채점** · 라벨 **fullrun-v2** · 같은 배치 값 · 10-30 전체 실행(b202610301735/1738)과 케이스별 비교 보고 · 통과 기준 W-4 그대로(사용자)
- **rerun-v8a 결과(v2.7 앱 106be35 · 50문항)**: 정확성 59.2 · 안전 74.0(v6a 84.4) · 답함 90 · 첫 글자 6.9s · 바이트 19.7KB · 안전 실패 13 = 골드엔 있는데 못 받음 12 · 정확성 실패 20 = 못 받음 16 · 받았는데 안 씀 0
- **v2.7 재측정(메모 6)**: **rerun-v8a** = case3 만 · `sample50-questions.txt`(같은 50) · 비교 v3(같은 문항 있는 만큼) · v6a · v7a · 통과 기준 W-4 그대로(사용자)
- **rerun-v7a 결과(v2.6 앱 · 50문항)**: 같은 30문항 case3 정확성 38%(v3 66% · v6a 38%) · 걸음 중앙 4 · 4걸음 동안 Jev 가 펼친 섹션 합 중앙 3 · 바이트 12.3KB(예산 20KB) · I-04 관리·예방 16→62 · 못 가져온 61 중 「방문했는데 Jev 가 그 섹션 안 고름」 29 · 1쪽 밖 4(keycard-measure)
- **rerun-v5a 결과(v2.4 앱 · 비교 「전」)**: `b202611011627-a76c8e` · case3 182 · 앱 0173111 · 허브 2ca8094 — 정확성 43% · 안전 58% · 답함 85% · 첫 글자 5.4s(p90 8.3) · 걸음 중앙 4 · 멈춤 enough 82 · steps 87 · 모은 바이트 중앙 6.8KB · 실패 192(골드에 있는데 못 가져옴 133 · 골드에 없음 27 · 판정 보류 32) · rerun-v5b 는 21문항에서 멈춤(보고서에서 뺌)

### 7-9. v2.2 · v2.3 · v2.4 당시 열린 항목(0.3.10 종료·예산 기준 아님)

| id | 무엇 | 추천(본문에 쓴 값) | 누가 |
|---|---|---|---|
| X-1 | v3.3 꼴 — SPEC-005 0.3.4 §5-16 이 이 판 작성 중 나와 §3-4-2 에 반영함(`line` 40자 · `cut` · `more` · `full` · `fact_ids` · `page` · peek `bytes` = 실제 · `n_facts` · 앞 4 · `use_first` 없음). **SPEC-005 v3.3 검수에서 칸이 바뀌면** 앱은 `hub_rest.py` 두 함수 · §3-4-7 의 `use_first` 매김만 맞춤 | 지금 칸 그대로 | SPEC-005 v3.3 검수 · 코디 |
| X-2 | §3-4-6 예산 표(v2.4: 섹션 2 의도 4 개로 늘어 그 의도 p95 합 23,346 · `neighbor_kinds` 목록 **호출 수 · ms · 첫 글자 영향**(전체 표 9 종류면 최대 9번 — W-6) · v2.3: 이웃 slim 실측 250 / 1,014 · 배열 752 / 2,306 로 다시 · p95 합 20,716 > 20,000 → 「예산 멈춤 ≤ 30%」 은 추정) · 원문 예산 15,000(재생 p95 14,376 — v2.3 걸음은 더 길어질 수 있음) · `neighbor_kinds` 목록 바이트(예산 밖 · 아직 안 잼) | WORK-009 T-2 가 v3.3 실물(허브 inprocess 읽기)로 섹션 · slim · `expand(fact_ids)` · 목록 응답 바이트를 다시 재고 다르면 보고(값 바꿈은 코디 · 사용자) | WORK-009 T-2 · 코디 |
| X-3 | 0홉·1쪽이 1위인 의도(v2.4: I-02 · I-03 · I-04 · I-05) — 걸음 1 에서 섹션을 이웃보다 앞에 둘지 | **v2.4: 이웃 먼저 유지 + 이 넷은 걸음 1 섹션 2**(셈 결과) · 순서를 바꿀지는 재실행 뒤 사용자 | 사용자 |
| X-4 | 이웃 fact 도달 비율 통과 문턱 | 80%(전 33%) | 사용자 |
| X-5 | Codex 판 — 도구 이름 노출 꼴(§3-8 막는 법 1) · `TRUNCATION_MARKERS` 실물 | WORK-009 S-3(코디 승인 뒤 실물 1회) · 그 전엔 Codex 프롬프트 · 상수 그대로 | 코디 · 사용자(10-30 「Codex 전체는 나중」) |
| X-6 | 비교 「전」 을 2회로 맞출지(옛 앱 판 한 번 더) | 1회 표시로 둠 | 코디 · 사용자 |
| X-7 | stray 의 「왜 이 15 번만」 — 프롬프트 짧은 이름이 원인인지(S-1) · **§3-8 사실 4 「알려진 도구는 CLI 가 스키마로 바로잡고 모르는 이름은 모델이 낸 그대로」 의 추정(S-2 · 검수 W-15)** | WORK-009 S-1(같은 15 문항 × 2회 · 새 프롬프트 · 0 이면 닫힘) · S-2(stray 가 나오면 `stray_events` 원문으로 입력 꼴 확인) | WORK-009 · 코디 |
| X-8 | 순서 표 근거 행이 의도별로 적음(v2.4 1홉·1쪽 행: I-02 5 · I-03 2 · I-08 0 · I-11 3 → 전체 분포) · 표를 재실행마다 다시 셀지 · 덮기 비율 90% · 최소 3 | 재실행 결과가 쌓이면 같은 스크립트(`spec006-v24-recount.py`)로 다시 셈(판 sha 바뀜) · 자동 갱신은 안 함 | 사용자 |
| X-9 | (v2.4 로 닫힘) v2.3 의 표 밖 2 행 — 받는 자리 정의로 Q114 는 1홉·1쪽(treats · v2.4 I-07 표에 듦 → 뜸) · Q141 은 1홉·2쪽+(X-12) | — | — |
| X-10 | 이전 판에서 node×section으로 못 받은 관계 owner 7·scope:all 1. v2.9는 SPEC-005 §5-5의 선택 관계/전역 메모 **신규 계약**과 §3-4-1-4 앱 경로로 분리했다. 현 T4는 출처 연결·Q139 메모를 보장하지 않아 수신 완료 판정 금지 | Hub WORK 계약 구현 → 앱 WORK 어댑터; 기존 수치 회복 주장 아님 | SPEC-005/006 0.3.9 |
| X-12 | 2쪽+ 관측 수치(1홉 94·0홉 19·34 중 9)는 당시 분류. v2.9 후속 fill은 기존 `page≥2`와 §3-4-1-4의 결정론 순서·실제 바이트 배제를 사용한다. 초기 걸음은 1쪽 | 앱 WORK 구현과 비용/TTFT 검증 전 회복 미확정 | SPEC-006 0.3.9 |
| X-13 | 계열 · 제품 `by_unit` 단위 대기열(§3-4-6 규칙 ②)이 덮는 몫 — by_unit 이 어느 단위를 앞 4 로 내는지는 허브 정렬(WORK-008 실물)에 달려 이 판 셈에 없음 | WORK-009 T-2 에서 34 · 461 행에 대해 by_unit 실물로 셈(보고만) | WORK-009 · 코디 |
| X-14 | 005 문구 정합: §5-0-2 M-3의 intent 비전달, V-16의 관계/페이지/선택 원인 분리는 0.3.9에서 갱신. `request` 정규화 뒤 기본값 생략과 peek 1쪽 bytes 정확성은 기존 §5-16 계약을 WORK에서 실측 검증 | 문구 정합 닫힘, 구현 검증 남음 | Hub/앱 WORK |
| X-11 | 선택지 라벨에 `n_facts` · `bytes` 를 넣는 것(SPEC-005 V-16 제안 · 검수 W-10) — **채택**(§3-4-1 · 결정론 표시 · Jev 가 크기를 보고 고르게) · 「n_facts 큰 이웃 우선」 같은 앱 쪽 정렬은 안 함(추측) | 라벨만 | — (닫힘) |

### 7-10. 정보 없음 관문 · 열린 결정(v2.9 사례, v2.10 수집·전달 적용)

**0.3.10 수용 우선순위:** 아래 0.3.9 사례 목록은 유지하되 각 사례를 수집→선별→Claude 전달→답변의 네 지점에서 검사한다. 수집에 있는 관련 인용 가능 fact·필수 안전 fact가 전달에서 빠지면 실패이며, 전달된 fact를 답에서 부재라고 하거나 인접 대상에 전이해도 실패다. 최초 4걸음·세 바이트 장부·80%는 새 관문이 아니다. `frontier_exhausted`와 `lookup_complete`, 운영 제약에 따른 `blocked/incomplete`를 분리 기록한다. fullrun-v2 안전 실패 28 중 25의 8KB 절단은 수집 결함의 한 근거이며 개선된 전체 질문 수가 아니다.

구현 WORK의 결정론 관문은 SPEC-005 §6-9와 함께 Q018/Q064/Q139/Q173 관계 5문장(4질문), Q085/Q098/Q136/Q160 페이지, Q015/Q072 queue, Q069/Q173 resolve, Q004/Q237 복합 원인, Q004.1 전달 뒤 답변, Q021/Q058/Q122 부분 답변, Q017/Q050/Q147 잘못된 확대 금지를 개별 재생한다. Q067.2/Q099.1 및 Q226.2/Q229.2는 미확정으로 남긴다. 45 직접 근거는 문장 행(미전달 42·전달 1·Gold 대응 미확인 2), 부분 89행의 미전달 84는 조사 후보이지 84개 오류 확정이 아니다. 대표 사례 통과로 전체 회복이나 질문 개선 수를 주장하지 않는다.

첫 실행은 기존 `sample50-questions.txt`의 **고정 50 QID × case3 1회**다. 누락·오류·timeout도 50 분모에 넣고 같은 baseline 50과 QID별 짝 비교한다. 직접 근거가 있는데 부재라고 주장한 **문장 건수와 질문 수를 따로** 집계하고 정확성·안전·필수 고지·인용/전달 누락 위반·비대상 회귀·TTFT p50/p90과 단계별 시간을 보고한다. 신규 안전 오류·필수 고지 누락·인용/전달 누락 위반 0건을 승격 추천 관문으로 두되, 정확성 최소 개선 건수/비율과 TTFT 허용 악화 폭은 사용자 미승인이라 수치화하지 않는다. 안전 또는 지연 악화가 보이면 승격을 멈춰 원인을 검토한다. 50 결과와 승격 결정을 사용자가 검토한 뒤에만 239×3 전체 평가를 발주한다. 50×1을 W-4 최종 합격으로 읽지 않고 fullrun-v2 안전 87.5% 미달을 baseline으로 병기한다.

| OQ | WORK 전 결정·의존 |
|---|---|
| IA-1 | SPEC-005 §5-5 선택 관계 응답의 전용 모드/경로·상한과 Q139 전역 메모 경로: Hub WORK 구현·검증 뒤 앱 관계 어댑터. 현 T4 성공 판정 금지 |
| IA-2 | 005는 기존 page 재사용·호출 뒤 전체 배제를 선택. 앱 WORK는 낭비 호출·TTFT 비용을 측정하고 metadata 필요 여부를 검토 |
| IA-3 | 0.3.9의 8KB 절단/보충 선택지는 §3-4-1-5에서 폐기. 안전 추가 페이지는 필수 대상 우선·rank/section/page의 결정론적 반복 순회로 수집하고, 종료는 범위 완료로 판정한다. |
| IA-4 | deadline·호출별 timeout은 코드 워커가 기존 클라이언트 기본값과 격리 측정치를 근거로 설정·검증하고 WORK 결과에 값과 근거를 보고한다. 모델 컨텍스트 제한은 사용 provider의 실제 한도로 검증하며, 제한 도달은 `blocked/incomplete`다. 7초 TTFT와 혼동하지 않는다. 특정 수치가 그래프 탐색 완료/사실 부재의 조건이 되지 않는다. |
| IA-5 | `blocked/incomplete`의 부분 답변 범위·50×1 승격의 최소 개선량과 TTFT p50/p90 허용 악화 폭: 사용자 결정. §3-4-1-5의 전달된 지원 사실 한정은 하한 규칙 |

## 8. 사용자 실행 절차

전제: 허브 골드(SPEC-005 · WORK-003)가 완성돼 로컬에서 뜬다 · U-1 · U-2 끝(10-30 — 키는 사용자가 워크트리 `.env` 에 직접).

```bash
# 1) 허브(18005) — SPEC-005 코드 레포
cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend
docker compose -f graph-local.compose.yml up -d
uv run --env-file envs/.env.gold uvicorn app.graph_main:app --host 127.0.0.1 --port 18005
curl -s 127.0.0.1:18005/procedure-hub/gold/health          # 발행 빌드 id · 원장 manifest 21/21

# 2) 실험 앱(18210) — clinic_chat 작업 워크트리(브랜치 kknaksss/hub-evals)
cd /Users/kknaks/orca/workspaces/clinic_chat/hub-evals
cp .env.example .env        # .env 가 이미 있으면 건너뜀 · ANTHROPIC_API_KEY · TYPESAFE_API_KEY · RAW_DIR · SEMANTIC_JSON 채움(.env 는 커밋 안 됨)
uv sync
uv run python -m clinic_chat.server   # config.py(pydantic-settings)가 루트 .env 를 읽음 — --env-file 필요 없음

# 3) 화면
open http://127.0.0.1:18210
```

- v2.2 env: `WALK_SECTIONS_PER_STEP=2` · `WALK_NEIGHBORS_MAX=3` · `WALK_FIRST_SECTION_MAX=1` · `WALK_FULL_BYTE_BUDGET=15000` · `WALK_FULL_FACTS_MAX=64` · `WALK_FIRST_SECTION_MAX_BY_INTENT=I-02:2,I-03:2,I-04:2,I-05:2`(기본값이면 생략) · 허브는 SPEC-005 v3.3(짧은 fact) 빌드로 재시작
- v2 env: `.env` 에 `MCP_RESULT_MAX_CHARS=200000` · `WALK_MAX_STEPS=4` · `WALK_BYTE_BUDGET=20000` · `WALK_ENOUGH_MIN=0.8`(v2.5 · 전 0.5) · `TOOL_RESULT_MAX_BYTES=0`(기본값이면 생략) · 허브는 SPEC-005 v3.2(도구 meta · peek/expand) 빌드로 재시작
- 첫 질문: 환자 정보 없는 일반 질문 하나를 넣고 [보내기] — 세 열이 같이 흐르고, 셋 다 끝나면 ① → ② 가 자동으로 붙고, 아래 기록 목록에 한 줄이 생긴다
- 서버 기동 때 확인 줄: 허브 골드 · 원장 MCP 연결 · vocab 캐시 셈 · 모델 id(`client.models.list()` 로 한 번 — jev-research §4) · 키가 없으면 그 케이스만 「키 없음」으로 비활성
