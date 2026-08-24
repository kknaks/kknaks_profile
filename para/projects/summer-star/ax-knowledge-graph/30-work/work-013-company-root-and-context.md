---
type: work
id: AXKG-WORK-013
title: "WP13: 회사 루트 + context 층 — 회사 앵커·요구/context 분기·up: 회사 루트 수렴"
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
    - "[[decision-009-company-root-and-context|AXKG-DEC-009]]"
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
  specs:
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
  works:
    - "[[work-011-enterprise-project-fanout|AXKG-WORK-011]]"
    - "[[work-012-plan-then-fanout|AXKG-WORK-012]]"
  releases: []
  related: []
---

# WP13: 회사 루트 + context 층

회사 프로젝트에 **회사 루트 문서 `{corp}.md`(회사당 1개 앵커)** 와 **회사 배경지식 `context/` 층**을 도입하고, project 분류를 **요구사항 vs 회사 context 2종으로 하위 분기**하며, **모든 산출을 `up:` 체인으로 회사 루트에 수렴**시킨다(AXKG-DEC-009). 지금까지 요구 docx마다 baseline이 고립돼 안 묶이던 문제를 회사 앵커로 해결한다. **AXKG-SPEC-014의 팬아웃 결과 계약(원본요약 + 기능정의서 N, main+derived, origin·경로)은 유지**하고 그 위에 회사 앵커·context 층을 얹는다. 생성 메커니즘은 AXKG-WORK-012(plan-then-fanout)와 정합한다(요구사항 팬아웃 경로 그대로).

## Meta

- Baseline: AXKG-BL-002
- Covers decision: AXKG-DEC-009(회사 루트·context 층·요구/context 분기·up: 회사 루트 체인)
- Covers spec: AXKG-SPEC-014(확장된 외부 계약 SSOT), AXKG-SPEC-001(분류 파이프라인), AXKG-SPEC-003(intake 메모·성격 힌트), AXKG-SPEC-005(링크/frontmatter 계약)
- Depends on work: AXKG-WORK-011(v1 — corp 바인딩·origin·경로·템플릿·스캐폴드), AXKG-WORK-012(plan-then-fanout 생성)
- External dependency: 없음

## Scope

포함:

- ① 회사 루트 문서 `{corp}.md` — "프로젝트 추가"에 회사 간략정보(회사명·도메인·한 줄 소개) 입력 + 루트 문서 생성.
- ② project 하위 분기 — 요약①/분류가 업로드 docx를 요구사항 vs 회사 context로 판정(메모 성격 힌트 우선).
- ③ context 산출 — 회사 context는 `projects/{corp}/context/{문서}.md` 단일 문서로 생성(팬아웃 없음)·apply.
- ④ up: 회사 루트 배선 — 문서 생성 시 corp 루트 stem 주입 → `up:` frontmatter + 본문 `[[{corp}]]` 자동 생성.
- ⑤ 기존 baseline/spec의 `up:` 회사 루트 체인 정합(spec→원본요약→{corp}).

제외:

- **팬아웃 결과 계약 변경** — 원본요약 + 기능정의서 N·main+derived·origin·경로는 불변(AXKG-SPEC-014 SSOT).
- **생성 메커니즘(plan-then-fanout)** — AXKG-WORK-012 소관(이 WP는 그 위에 앵커·context·up: 만 얹음).
- **회사 루트/context document_type 최종 확정·요구/context 폴백·context dedup** — AXKG-DEC-009 OQ, 구현 시 확정(아래 Open Issues).

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/api/routes/projects.py` · `services/project_scaffold.py` · `schemas/projects.py` | ① 회사 간략정보 입력 + `{corp}.md` 생성, `context/` 스캐폴드 |
| `apps/api/axkg/seeds.py` (분류 프롬프트) | ② project 하위 요구/context 판정 프롬프트·라우팅 |
| `apps/api/axkg/services/document_paths.py` | ③ `projects/{corp}/context/` 경로 매핑, context document_type |
| `apps/api/axkg/services/ai/` (plan_fanout_execution / documentation_gate) | ③ context 단일 문서 산출 경로(요구는 WORK-012 팬아웃) |
| `apps/api/axkg/workers/apply_executor.py` | ④ 생성 문서에 up: 회사 루트 stem 주입 + 본문 `[[{corp}]]` 배선 |
| `apps/web/app/projects/` (프로젝트 추가 폼) | ① 회사 간략정보 입력 UI, ③ context/·루트 트리 렌더 |

## Execution

| Phase | 범위 | 담당 | 관련 spec/decision | 완료조건 | Status |
|---|---|---|---|---|---|
| **P1. "프로젝트 추가" 회사 간략정보 + `{corp}.md`** | "프로젝트 추가" 폼에 회사명·도메인·한 줄 소개 입력 + `projects/{corp}/{corp}.md`(회사 루트, document_type `company` 기본) 생성. `context/` 스캐폴드 추가 | be·fe | DEC-009 D1, SPEC-014 U-1 | 프로젝트 추가 시 회사 간략정보로 `{corp}.md`가 생성되고 `context/`가 스캐폴드된다 | ⬜ todo |
| **P2. 분류 요구/context 분기** | 요약①/분류에 project 하위 sub-type 판정(requirement | context) 추가 — 메모 성격 힌트 우선, 내용 판단 보조. 라우팅(requirement→팬아웃 / context→context 경로) | be | DEC-009 D2, SPEC-001, SPEC-003 | project 업로드가 메모+내용으로 요구/context로 분기되고 각 경로로 라우팅된다 | ⬜ todo |
| **P3. context 산출 경로·apply** | 회사 context를 `projects/{corp}/context/{문서}.md` 단일 문서로 생성(팬아웃 없음)·apply. context document_type·경로 매핑 | be | DEC-009 D2, SPEC-014, SPEC-005 | 회사 context docx가 `context/` 단일 문서로 apply되고 기능정의서로 쪼개지지 않는다 | ⬜ todo |
| **P4. up: 회사 루트 배선** | 문서 생성 시 corp 루트 stem 주입 → `up:` frontmatter + 본문 `[[{corp}]]` 자동 생성(요약/팬아웃/context 생성 경로 공통). `baseline`·`context`→`up:[{corp}]` | be | DEC-009 D3, SPEC-005 | 생성 문서에 up: 회사 루트 + 본문 `[[{corp}]]`가 자동 배선되어 그래프가 회사 루트로 수렴한다 | ⬜ todo |
| **P5. 기존 baseline/spec up: 체인 정합** | spec `up:` = 원본요약(→ 원본요약 `up:` = {corp})으로 2단 체인 정합. 기존 생성분/템플릿과 정합 | be | DEC-009 D3, SPEC-010 | spec→원본요약→{corp} 2단 체인으로 모든 요구 문서가 회사 루트에 수렴한다 | ⬜ todo |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| CompanyRoot 문서(`{corp}.md`) | 신규 — document_type `company`(기본), 회사당 1개 앵커, 그래프 노드. up-target 허브 |
| CompanyContext 문서(`context/{문서}.md`) | 신규 — document_type `context`(기본), 회사 배경지식 단일 문서(팬아웃 없음) |
| `documents` / `document_edges` | 회사 루트·context 노드 추가 + `up:`(본문 `[[{corp}]]`) 기반 회사 루트 수렴 엣지 |
| `ai_tasks` / 분류 | project 하위 sub-type 판정(requirement/context) 라우팅 |

- 상태 / invariant: 팬아웃 결과 계약(원본요약 + 기능정의서 N·main+derived·origin·경로)은 불변(AXKG-SPEC-014). 회사 루트는 그래프 노드(origin과 달리), 요구/context 무관하게 origin raw 보관 공통(AXKG-DEC-009 D4).
- Migration 필요 여부: document_type에 `company`/`context` 추가 여부는 구현 시 확인(AXKG-DEC-009 OQ — 신규 enum vs 기존 타입 재사용).
- SPEC에 환류: AXKG-SPEC-014 확장 완료(회사 루트·context·up: 체인 본문 정합).

## Acceptance

- [ ] 회사 생성(프로젝트 추가) 시 회사 간략정보로 `projects/{corp}/{corp}.md`(회사 루트)가 생성되고 `context/`가 스캐폴드된다.
- [ ] 회사 context docx(메모 "회사 정보야")를 올리면 요구/context 분기에서 **context**로 판정돼 `projects/{corp}/context/{문서}.md` 단일 문서로 생성된다(기능정의서로 쪼개지지 않음).
- [ ] 요구 docx는 기존대로 baseline+spec 팬아웃된다(AXKG-SPEC-014 계약 불변).
- [ ] 생성된 모든 문서(baseline·spec·context)가 `up:` 체인으로 회사 루트 `{corp}.md`에 수렴하고, 본문 `[[{corp}]]` 링크가 자동 생성된다(빈 `[[ ]]` 없음).
- [ ] 그래프에서 한 회사의 origin(비노드)을 제외한 모든 문서가 회사 루트를 통해 회사 단위로 묶인다.

## Rollback

- 작업 레포 커밋 단위 revert. 회사 루트/context 노드·up: 배선 revert 시 v1(WORK-011/012) 팬아웃 경로로 복귀(앵커·context 없음).

## Open Issues

- **회사 루트/context document_type 확정(AXKG-DEC-009 OQ)**: 신규 `company`/`context` enum vs `permanent`/`reference` 재사용 — 그래프 노드 처리·마이그레이션 보고 P1/P3 착수 시 확정.
- **요구/context 판단 모호 시 폴백(AXKG-DEC-009 OQ)**: 메모 힌트 없고 내용도 애매할 때 기본을 요구/context 중 무엇으로 둘지, 사용자 확인 여부 — P2에서 확정.
- **context 문서 dedup(AXKG-DEC-009 OQ)**: 같은 성격 context 재유입 시 기존 문서 통합·보강 vs 별개 문서 — 요구 dedup(AXKG-DEC-007 D4) 정책 적용 여부를 P3에서 확정.
