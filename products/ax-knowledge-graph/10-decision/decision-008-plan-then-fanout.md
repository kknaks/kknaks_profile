---
type: decision
id: AXKG-DEC-008
title: "project 문서화 생성 아키텍처: 단일 task에서 plan-then-fanout으로 전환"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-21
updated_at: 2026-07-21
tags:
  - product/ax-knowledge-graph
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-002-enterprise-requirement-project-destination|AXKG-BL-002]]"
  decisions:
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
  works: []
  releases: []
  related: []
up:
  - divide-and-conquer
  - workflow-orchestration
  - async-io
---

# project 문서화 생성 아키텍처: 단일 task에서 plan-then-fanout으로 전환

project 문서화 팬아웃의 **생성 메커니즘**을 단일 문서화 task(원본요약 1 + 기능정의서 N장을 한 AI 호출로 통째 생성)에서 **plan-then-fanout**(① 요약+plan → ② 기능별 독립 task 병렬 발주 → ③ fan-in 조립)으로 전환한다. **AXKG-SPEC-014의 외부 계약(무엇이 나오나 = 원본요약 + 기능정의서 N, main+derived, origin·corp·경로·3층)은 불변**이며, 이 결정은 그 산출물을 **어떻게 만드느냐**만 바꾼다. AXKG-DEC-007이 확정한 팬아웃 결과 계약을 그대로 유지한 채, AXKG-WORK-011 v1의 단일-task 생성 방식을 대체(supersede)한다.

## Context — 실측 근거

2026-07-21 e2e에서 확인: AXKG-WORK-011 v1은 project 분류 시 **문서화 게이트 1개 task로 원본요약 1 + 기능정의서 N장을 통째 생성**한다. The_sc(기능 10개) docx로 **두 가지 실패 모드**가 실측됐다:

1. **타임아웃**: 단일 task가 **600초를 반복 초과해 실패**. 타임아웃을 1800초로 올리자 완료되긴 했으나(약 8.8분 소요) 여전히 느렸다.
2. **출력 파싱 실패(더 결정적)**: 타임아웃을 넘겨 생성이 끝난 뒤에도(`exit_code=0`), 결과가 `OUTPUT_PARSE_FAILED`("Expecting value: line 1 column 1")로 거부됐다 — **문서 11개를 하나의 거대 structured-output(JSON)으로 뱉으니 출력이 잘리거나 형식이 깨진** 것이다. 즉 타임아웃을 아무리 올려도 **거대 단일 출력 자체가 신뢰 불가**다.

원인은 명확하다 — **문서 11개(원본요약 1 + 기능정의서 10)를 한 AI 호출로 뽑아 출력·컨텍스트가 방대**하다. 한 task의 출력이 커질수록 지연·파싱실패 확률이 비선형으로 커지고, 하나가 삐끗하면 11개를 통째로 재생성해야 한다. 타임아웃 상향으로는 파싱 실패를 못 막으므로, **생성 방식 자체를 기능 단위로 쪼개야 한다**.

> 이 결정은 **생성 메커니즘 재설계**다. 산출물 계약(AXKG-SPEC-014)·팬아웃 결과(AXKG-DEC-007)·apply/파생지식 모델(AXKG-SPEC-004)은 바꾸지 않는다.

## Decision

project 문서화 생성을 **3단계 plan-then-fanout 아키텍처**로 전환한다.

### ① 요약 + Plan (가볍고 빠름)

- **결정**: docx → **원본요약 + 기능목록(plan)** 을 산출한다. plan은 `[{seq, 기능명, 요지}]` × N 형태의 경량 배열이며, **원본요약 수준의 가벼운 산출**(전체 기능정의서를 쓰지 않음)이다. 이 **plan이 곧 fan-out 발주서**가 된다.
- **근거(왜)**: 요약①은 이미 원문 구조를 따르는 적응형 요약이라 docx의 기능 목록 구조를 그대로 뽑는다(AXKG-DEC-007 Decision 5). 여기서 기능목록을 **plan(발주서)** 으로 명시적으로 산출하면, 무거운 본문 생성 없이 "무엇을 몇 장 만들지"만 먼저 확정한다 — 작고 빠르다.
- **영향**: 요약 스테이지의 출력에 plan 배열이 추가되거나(요약① 확장) 신규 `plan_project` stage가 생긴다. plan은 원본요약(baseline)의 `## 기능 목록`과 정합하며(각 seq = 기능정의서 1장), 이후 fan-out의 입력 계약이 된다.

### ② Fan-out (plan에 따라 기능별 독립 task 병렬 발주)

- **결정**: plan의 **각 기능마다 독립 task를 발주**한다(신규 task type `generate_feature_spec`, **병렬**). 각 task의 입력 = **docx 원문 + 그 기능 항목(plan seq) + 기능정의서 템플릿(`project_feature_spec`)**, 출력 = **기능정의서 1장**.
- **근거(왜)**: 한 task가 기능 1개에만 집중하므로 (1) 출력이 작아 **600초로 충분**(타임아웃 해소), (2) worker concurrency로 **병렬 생성**(N개 동시), (3) 실패가 **기능 단위로 격리**되어 그 기능만 재시도(지금은 하나 삐끗하면 11개 통째 재생성), (4) AI가 기능 1개에 집중해 **품질↑**.
- **영향**: `ai_tasks`에 `generate_feature_spec` task type 추가. 입력 조립(docx 원문 + plan 항목 + 템플릿)은 AXKG-SPEC-011의 3자 조립 계약(AXKG-DEC-005)을 재사용한다. 템플릿은 `project_feature_spec`(AXKG-SPEC-010) 고정 동봉.

### ③ Fan-in (N개 draft 조립 → 게이트 revision)

- **결정**: N개 기능정의서 draft를 취합해 **문서화 게이트 revision으로 조립**한다 — `main_document` = 원본요약(①의 baseline), `derived_suggestions[]` = 기능정의서 N장(②의 산출). 사용자가 게이트에서 승인하면 **기존 apply(팬아웃)** 가 실행된다.
- **근거(왜)**: 팬아웃 결과(1 원본요약 + N 기능정의서 = main + derived)는 이미 AXKG-DEC-007 Decision 7 / AXKG-SPEC-004의 파생지식 모델과 동형이다. fan-in은 **여러 task 산출을 하나의 게이트 revision으로 모으는 조립 단계**일 뿐, 승인·apply·경로 조립은 그대로 물려받는다.
- **영향**: `apply_executor`(main+derived 팬아웃)와 승인 표면은 **거의 불변**이다 — 바뀌는 것은 revision의 draft가 "한 task의 통째 출력"에서 "N개 task 산출의 조립본"으로 채워진다는 점이다. fan-in 대기·부분 실패 처리·진행률(N개 중 M 완료)이 새로 필요하다(→ Open Questions / AXKG-WORK-012).

## Consequences

- **AXKG-WORK-011 Phase 4의 "단일 문서화 task 팬아웃 생성 방식"을 이 결정이 대체(supersede)한다.** WORK-011 v1이 세운 "게이트 1개 task가 원본요약 + 기능정의서 N을 통째 생성"은 plan-then-fanout(① plan → ② 기능별 task 병렬 → ③ fan-in 조립)으로 교체된다. corp 바인딩·origin 보관·create-only·경로 조립(WORK-011 P2·P3·P5-BE)은 그대로 재사용된다.
- **AXKG-SPEC-014의 외부 계약은 불변**이다 — 원본요약 + 기능정의서 N, main+derived, origin 3층, corp 매칭, 경로 컨벤션은 변하지 않는다. 바뀌는 것은 **생성 메커니즘(1 task → plan + N task + 조립)** 뿐이다. SPEC-014에는 "생성 방식은 AXKG-DEC-008 plan-then-fanout으로 리팩터(외부 계약 불변)"라는 pointer만 추가한다.
- **코드 영향(코드레포 소관)**:
  - `ai_tasks`에 task type 추가 — `plan_project`(① plan 산출), `generate_feature_spec`(② 기능별 생성).
  - 게이트 revision **fan-in 조립** — N개 기능정의서 draft를 취합해 main+derived revision을 구성.
  - **진행률·부분 실패 처리** — N개 중 M개 완료 표시, 일부 기능 task 실패 시 정책(아래 Open Questions).
  - apply_executor(main+derived 팬아웃)·파생지식 apply 규칙은 불변(AXKG-SPEC-004 SSOT).
- **후속 구현은 AXKG-WORK-012**(plan-then-fanout)로 발주한다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[divide-and-conquer]] — **① plan 으로 쪼개고 ② 기능별로 각각 풀고 ③ fan-in 으로 합친다** — 한 번에 통째로 생성하다 타임아웃 나던 것을 쪼개는 쪽으로 뒤집은 것이라, 나누는 방법(plan)과 합치는 방법(조립)을 정한 것이 결정의 내용이다
- [[workflow-orchestration]] — plan 이 곧 **발주서**가 되어 다음 단계의 입력이 된다. 단계 사이로 결과가 넘어가는 구조가 아니면 이 전환이 성립하지 않는다
- [[async-io]] — 기능별 task 를 **병렬로 발주**해 전체 시간을 「합」이 아니라 「가장 긴 하나」로 만든다

## Open Questions

- **fan-in 대기 / 부분 실패 정책**: 일부 기능 task가 실패했을 때 — 성공한 나머지 기능정의서로 게이트를 열어 진행할지(부분 진행), 전체를 보류하고 실패 기능 재시도 후 완주할지(전체 보류). 재시도는 기능 단위로 격리되므로 부분 진행이 유력하나, 게이트 revision의 "완결성" 기준을 후속에서 확정.
- **plan 산출 위치**: plan(기능목록 발주서)을 **요약①에 통합**(요약 출력에 plan 배열 추가)할지, **신규 `plan_project` stage**로 분리할지. 요약과 plan의 결합도·재시도 단위에 따라 결정.
- **진행률 표시 계약**: "N개 중 M개 기능 생성 완료" 진행률을 게이트/인박스 UI에 어떻게 노출할지(상태 enum·폴링 vs 이벤트). 부분 실패 표시와 함께 후속에서 확정.
