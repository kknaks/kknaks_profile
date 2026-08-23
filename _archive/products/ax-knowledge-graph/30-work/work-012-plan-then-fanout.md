---
type: work
id: AXKG-WORK-012
title: "WP12: plan-then-fanout — project 문서화 생성 재설계(요약+plan → 기능별 병렬 task → fan-in 조립)"
status: todo
product: ax-knowledge-graph
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-07-21
updated_at: 2026-07-21
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-002-enterprise-requirement-project-destination|AXKG-BL-002]]"
  decisions:
    - "[[decision-008-plan-then-fanout|AXKG-DEC-008]]"
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
  specs:
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works:
    - "[[work-011-enterprise-project-fanout|AXKG-WORK-011]]"
    - "[[work-004-approval-gates|AXKG-WORK-004]]"
  releases: []
  related: []
---

# WP12: plan-then-fanout — project 문서화 생성 재설계

project 문서화 팬아웃의 **생성 메커니즘**을 단일 문서화 task(원본요약 1 + 기능정의서 N을 한 AI 호출로 통째 생성)에서 **plan-then-fanout**으로 교체한다: ① 요약 + plan(기능목록=발주서) → ② plan 각 기능마다 독립 task 병렬 발주(`generate_feature_spec`) → ③ N개 draft를 fan-in해 게이트 revision(main=원본요약, derived=기능 N) 조립 → 승인 → 기존 apply(팬아웃) 재사용. **AXKG-SPEC-014의 외부 계약(원본요약 + 기능정의서 N, main+derived, origin·corp·경로·3층)은 불변**이며, 이 WP는 **생성 방식만** 바꾼다(AXKG-DEC-008). AXKG-WORK-011 v1의 단일-task 생성(Phase 4)을 대체한다.

## Meta

- Baseline: AXKG-BL-002
- Covers decision: AXKG-DEC-008(plan-then-fanout 아키텍처)
- Covers spec: AXKG-SPEC-014(팬아웃 외부 계약 SSOT·불변), AXKG-SPEC-011(AI 실행 파이프라인·3자 조립·task 모델), AXKG-SPEC-004(문서화 게이트·apply·파생지식 모델)
- Depends on work: AXKG-WORK-011(v1 — corp 바인딩·origin·경로 조립·템플릿 2종 재사용), AXKG-WORK-004(WP3 게이트·Apply Executor)
- Supersedes: AXKG-WORK-011 Phase 4(단일 문서화 task 팬아웃 생성 방식) — AXKG-DEC-008
- External dependency: 없음

## 배경 (실측 근거)

2026-07-21 e2e: WORK-011 v1은 문서화 게이트 1개 task로 원본요약 1 + 기능정의서 N을 통째 생성 → The_sc(기능 10개) docx에서 **600초 타임아웃 반복 초과·실패**(1800초로도 느림). 문서 11개를 한 AI 호출로 뽑아 출력이 방대한 게 원인. 생성 방식을 쪼갠다(작은 task·병렬·기능별 재시도). 상세 근거·결정은 AXKG-DEC-008.

## Scope

포함:

- ① **plan 산출** — docx → 원본요약 + 기능목록(plan = `[{seq, 기능명, 요지}]` × N). 요약① 확장 또는 신규 `plan_project` stage.
- ② **fan-out 배선** — plan 각 항목 → `generate_feature_spec` task 병렬 발주. 입력 = docx 원문 + 기능 항목 + `project_feature_spec` 템플릿, 출력 = 기능정의서 1장.
- ③ **fan-in 조립** — N개 기능정의서 draft 취합 → 게이트 revision(main=원본요약, derived=기능 N) 조립. 부분 실패 처리.
- ④ **게이트/UX** — 진행률(N개 중 M 완료) 표시, 게이트 승인 → apply(기존 팬아웃 재사용).
- ⑤ **v1→v2 전환** — WORK-011의 단일 task 경로를 plan-then-fanout으로 교체(또는 project는 v2 경로로 라우팅).

제외:

- **외부 계약 변경** — 산출물(원본요약 + 기능정의서 N)·main+derived·origin·corp·경로·3층은 불변(AXKG-SPEC-014 SSOT). 이 WP는 생성 메커니즘만.
- **기능 dedup·map.md 자동 재생성** — v1(WORK-011)과 동일하게 create-only·후속 WP(AXKG-DEC-007 설계 유지, 구현 제외).
- apply_executor(main+derived 팬아웃)·파생지식 apply 규칙 재설계 — 거의 불변(AXKG-SPEC-004 SSOT), 재사용만.

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/services/ai/` (요약 stage / 신규 `plan_project`) | ① plan(기능목록) 산출 stage·출력 스키마 |
| `apps/api/axkg/workers/` (task types) | ② `generate_feature_spec` task 등록·병렬 실행·기능별 재시도 |
| `apps/api/axkg/seeds.py` (prompts) | plan 프롬프트 + `generate_feature_spec` 프롬프트 시드(기능 1개 집중) |
| `apps/api/axkg/services/gates.py` · `services/ai/documentation_gate.py` | ③ fan-in 조립 — N draft → 게이트 revision(main+derived), 부분 실패·진행률 |
| `apps/api/axkg/workers/apply_executor.py` | apply(main+derived 팬아웃) — 재사용(거의 불변) |
| `apps/web/` (게이트/인박스) | ④ 진행률(N 중 M) 표시·부분 실패 표시 |

## Execution

| Phase | 범위 | 담당 | 관련 spec/decision | 완료조건 | Status |
|---|---|---|---|---|---|
| **P1. Plan 단계** | docx → 원본요약 + 기능목록(plan) 산출(요약① 확장 or 신규 `plan_project` stage). 출력 스키마 = plan 항목 배열 `[{seq, 기능명, 요지}]` | be | DEC-008 ①, SPEC-011 | plan이 원본요약과 함께 산출되고, 각 seq가 기능정의서 1장에 대응됨 | ⬜ todo |
| **P2. Fan-out 배선** | plan 각 항목 → `generate_feature_spec` task 병렬 발주. 입력 조립(docx 원문 + 기능 항목 + `project_feature_spec` 템플릿), worker concurrency로 병렬 | be | DEC-008 ②, SPEC-011, SPEC-010 | N개 `generate_feature_spec` task가 병렬 실행되어 각 기능정의서 draft 1장을 산출, task별 재시도 가능 | ⬜ todo |
| **P3. Fan-in 조립** | N task 완료 취합 → 게이트 revision(main=원본요약, derived=기능 N) 조립. 부분 실패 처리(정책 Open Issue) | be | DEC-008 ③, SPEC-004 | N개 draft가 하나의 게이트 revision(main+derived)으로 조립되고, 부분 실패 시 정책대로 처리됨 | ⬜ todo |
| **P4. 게이트/UX(진행률)** | 진행률(N개 중 M 완료) 표시, 게이트 승인 → apply(기존 main+derived 팬아웃 재사용) | be·fe | DEC-008 ③, SPEC-004, SPEC-014 | 게이트/인박스에 N 중 M 진행률이 보이고, 승인 시 origin+baseline 1+spec N 팬아웃이 기존 apply로 적용됨 | ⬜ todo |
| **P5. v1→v2 전환** | WORK-011의 단일 문서화 task 경로를 plan-then-fanout으로 교체(또는 project는 v2 경로로 라우팅). corp 바인딩·origin·경로·템플릿은 v1 재사용 | be | DEC-008, WORK-011 | project 분류가 단일 task가 아니라 plan-then-fanout 경로로 라우팅되고, v1 단일 task 생성은 은퇴/미사용 | ⬜ todo |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `ai_tasks` | task type 추가 — `plan_project`(① plan 산출), `generate_feature_spec`(② 기능별 생성, 병렬·기능별 재시도) |
| `approval_gates` / `approval_gate_revisions` | ③ fan-in — N개 draft를 취합해 main+derived revision 조립. 진행률·부분 실패 상태 |
| `apply_plans` / `documents` / `document_edges` | apply(main+derived 팬아웃) 재사용 — 거의 불변(AXKG-SPEC-004 SSOT) |
| `document_templates` | `project_source_summary`(①)·`project_feature_spec`(② 고정 동봉) — WORK-011 시드 재사용 |

- 상태 / invariant: AI는 DB/Markdown을 직접 쓰지 않는다 — executor만(AXKG-SPEC-004). 외부 계약(산출물·경로·main+derived)은 불변(AXKG-SPEC-014). 생성만 plan-then-fanout으로 교체.
- Migration 필요 여부: `ai_tasks` task type enum 확장 여부는 구현 시 확인(기존 enum이 문자열이면 무변경 가능).
- SPEC에 환류: SPEC-014에 "생성 방식 = AXKG-DEC-008 plan-then-fanout" pointer 추가(외부 계약 본문 불변, 완료).

## Acceptance

- [ ] **10기능 docx가 타임아웃 없이 기능별 병렬 생성→조립→팬아웃된다**(The_sc e2e 회귀: 단일 task 600초 초과 실패가 사라지고 완주).
- [ ] P1: docx → 원본요약 + plan(기능목록 배열)이 산출되고 각 seq가 기능정의서 1장에 대응한다.
- [ ] P2: plan 각 항목이 `generate_feature_spec` task로 병렬 발주되어 기능정의서 draft를 산출하고, 실패는 기능 단위로 격리·재시도된다(11개 통째 재생성 아님).
- [ ] P3: N개 draft가 하나의 게이트 revision(main=원본요약, derived=기능 N)으로 fan-in 조립된다.
- [ ] P4: 진행률(N 중 M 완료)이 표시되고, 게이트 승인 시 origin+baseline 1+spec N 팬아웃이 기존 apply(main+derived)로 적용된다(AXKG-SPEC-014 외부 계약 그대로).
- [ ] P5: project 분류가 plan-then-fanout 경로로 라우팅되고 v1 단일 task 생성은 사용되지 않는다.

## Rollback

- 작업 레포 커밋 단위 revert. task type·게이트 조립 변경 revert 시 v1(WORK-011) 단일 task 경로로 복귀(단, v1은 대용량 docx에서 타임아웃 재현).

## Open Issues

- **부분 실패 정책(AXKG-DEC-008 OQ)**: 일부 `generate_feature_spec` task 실패 시 — 성공분으로 게이트 진행(부분 진행) vs 전체 보류 후 실패 기능 재시도 완주. 게이트 revision "완결성" 기준을 확정해야 한다.
- **진행률 표시 계약(AXKG-DEC-008 OQ)**: N 중 M 완료 진행률의 상태 enum·노출 방식(폴링 vs 이벤트), 부분 실패 표시.
- **plan 산출 위치(AXKG-DEC-008 OQ)**: plan(발주서)을 요약①에 통합할지 신규 `plan_project` stage로 둘지 — P1 착수 시 결정.
