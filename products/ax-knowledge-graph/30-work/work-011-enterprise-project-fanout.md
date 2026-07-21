---
type: work
id: AXKG-WORK-011
title: "WP11: 기업 프로젝트 팬아웃 — docx→회사별 origin/baseline/spec 문서화·기능 dedup"
status: in-progress
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
progress: 20
created_at: 2026-07-21
updated_at: 2026-07-21
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/in-progress
links:
  baselines:
    - "[[baseline-002-enterprise-requirement-project-destination|AXKG-BL-002]]"
  decisions:
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
  works:
    - "[[work-004-approval-gates|AXKG-WORK-004]]"
    - "[[work-002-source-intake|AXKG-WORK-002]]"
  releases: []
  related: []
---

# WP11: 기업 프로젝트 팬아웃 — docx→회사별 origin/baseline/spec 문서화·기능 dedup

기업 AX 요구사항 docx가 `project`로 분류되면 flat 한 장이 아니라 **회사 프로젝트 `projects/{corp}/`의 origin(첨부 원본)·baseline(원본요약)·spec(기능정의서) 3층으로 팬아웃**되게 한다. intake는 **탭형 `[url | md | docx]` + 메모(항상 존재)**이며, corp는 사용자가 "프로젝트 추가"로 **수동·독립 스캐폴딩**해 둔 `projects/{corp}/`에 **메모의 회사명**이 분류 `project` 확정 시 매칭돼 정해진다(업로드/분류가 프로젝트를 자동 생성하지 않음). **이번 WP(v1) 구현은 기능정의서를 항상 `create_feature_spec`로 신규 생성(create-only)** 하며, 같은 기능 dedup(통합·보강)과 폴더별 `map.md` 자동 재생성은 **후속 WP로 분리**한다(SPEC-014 설계 계약은 유지). **WP3(문서화 승인 게이트, AXKG-WORK-004)의 파생지식 모델(`main_document`+`derived_suggestions[]`)을 재사용해 확장**하며, WP1(수집·요약, AXKG-WORK-002) 위에 얹는다.

## Meta

- Baseline: AXKG-BL-002
- Covers spec: AXKG-SPEC-014(팬아웃 외부 계약 SSOT), AXKG-SPEC-004(문서화 게이트 apply 확장), AXKG-SPEC-010(원본요약·기능정의서 템플릿 2종), AXKG-SPEC-012(docx 텍스트 추출 어댑터), AXKG-SPEC-011①(요약 적응형)
- Decision: AXKG-DEC-007(팬아웃·기능 dedup·origin·map.md), AXKG-DEC-005(파생지식 main+derived·연결 후보 컨텍스트)
- Depends on work: AXKG-WORK-004(WP3 문서화 게이트·Apply Executor), AXKG-WORK-002(WP1 수집·요약)
- Parallel work: 없음
- Follow-up work: 없음
- External dependency: 없음

## Scope

포함:

- project destination 문서화 게이트 apply를 origin 보관 + `main_document`(원본요약→`baseline/`) + `derived_suggestions[]`(기능정의서→`spec/`, **`create_feature_spec` 신규만**) 팬아웃으로 확장. **v1은 기능정의서를 항상 신규 생성(create-only)** 한다
- docx 텍스트 추출 어댑터(`docx_text`) — 본문 텍스트만, 구조화는 요약①
- 원본요약·기능정의서 템플릿 2종(`project_source_summary`·`project_feature_spec`) DB 시드
- **origin(첨부 docx 원본) 바인드 마운트 raw 저장** — `{AXKG_MARKDOWN_ROOT}/projects/{corp}/origin/{원본파일}.docx`(markdown과 같은 바인드 마운트, **그래프 노드 아님** — `documents` 테이블/인덱스 미편입)
- "프로젝트 추가" 스캐폴드 — **수동·독립 디렉토리 생성**(업로드/분류와 별개, AI 자동 생성 아님): 회사명 slugify + 충돌 분기 API + `projects/{corp}/{origin,baseline,spec}/` 동적 생성
- corp 바인딩 — 분류 `project` 확정 시 intake 메모(항상 요약 컨텍스트, SPEC-003)의 회사명을 기존 `projects/{corp}/`에 매칭(매칭 프로젝트 없으면 이번 범위 밖 — 프로젝트 선행 생성 전제)
- FE: 프로젝트 추가 UI(수동 스캐폴딩)·slug 미리보기·충돌 모달·corp 트리 뷰·게이트 팬아웃 표시(AXKG-SPEC-014 §2 U-1~U-5)

제외:

- **기능 dedup(같은 corp 기존 기능정의서 매칭·`supplement_existing_feature` 보강) — 후속 WP** (v1은 항상 `create_feature_spec` 신규 생성). SPEC-014 설계 계약은 유지, 구현만 이번 라운드 제외
- **폴더별 `map.md`(MOC) 자동 재생성 — 후속 WP**. SPEC-014 설계 계약은 유지, 구현만 이번 라운드 제외
- 회사 넘는 전역 capability 레지스터(도입 안 함, AXKG-DEC-007 D4)
- 요약①·분류②·게이트 공통 규칙 자체(WP1/WP3·SPEC-011/001/002/004 SSOT)

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/worker/workspace/context/` (para-classification·documentation-guide·document-link-rules) | project 판정·원본요약/기능정의서 산출 규칙·연결 링크 규칙 |
| `apps/api/axkg/seeds.py` | documentation_gate project 분기 + TEMPLATE_SEEDS 2종 시드 |
| `apps/api/axkg/services/source_collection/` (또는 어댑터 모듈) | `docx_text` 어댑터 추가(본문 텍스트만) |
| `apps/api/axkg/services/document_paths.py` | destination→디렉토리 매핑 `projects/{corp}/{origin,baseline,spec}/` |
| `apps/api/axkg/services/ai/documentation_gate.py` | `DESTINATION_TEMPLATE_KEY` project→`project_source_summary` + `project_feature_spec` 고정 동봉 |
| `apps/api/axkg/workers/apply_executor.py` | 팬아웃 apply(origin raw 보관·main+derived **create-only**; dedup·map.md 재생성은 후속 WP) |
| `{AXKG_MARKDOWN_ROOT}/projects/{corp}/origin/` (바인드 마운트) | 첨부 docx 원본 raw 저장 — markdown과 같은 마운트(`AXKG_WORKSPACE_HOST_PATH` 기본 `./data/documents`), **그래프 노드 아님**(`documents` 테이블/인덱스 미편입) |
| `apps/api/axkg/api/routes/projects.py` | "프로젝트 추가"(수동·독립 스캐폴딩) slugify·충돌 분기·트리 조회 |
| `apps/web/app/projects/` | 프로젝트 추가 UI(수동)·트리 뷰·게이트 팬아웃 표시 |
| Source Inbox intake 모달 (AXKG-SPEC-003 U-3 표면) | 탭형 `[url \| md \| docx]` + 메모(항상 존재·요약 컨텍스트) 확장 |

## Execution

| Phase | 범위 | 담당 | 관련 spec | 완료조건 | Status |
|---|---|---|---|---|---|
| **1. 가이드·프롬프트·템플릿** | `context/`(para-classification·documentation-guide·document-link-rules) 갱신 + `seeds.py` documentation_gate project 분기 + TEMPLATE_SEEDS 2종(`project_source_summary`·`project_feature_spec`) | be | SPEC-010, SPEC-014 | project 분류 시 원본요약+기능정의서 팬아웃 초안 프롬프트/템플릿이 준비됨 | ✅ **done** (코드repo 반영·미커밋) |
| **2. docx 텍스트 추출 어댑터** | source 수집 어댑터에 `docx_text` 추가 — 본문 텍스트만 추출(표/이미지 파싱 계약 없음), 구조화는 요약①. intake 메모(회사명 등)는 탭과 무관하게 항상 요약 컨텍스트로 동반(SPEC-003) | be | SPEC-012, SPEC-003 | `.docx` 업로드가 `adapter=docx_text`·`content_format=doc_text`로 정규화되고 메모가 요약 컨텍스트로 함께 넘어감 | ⬜ todo |
| **3. 경로·템플릿 배선** | `document_paths.py` destination→`projects/{corp}/{origin,baseline,spec}/` 매핑, `documentation_gate.py` `DESTINATION_TEMPLATE_KEY` project→`project_source_summary` + `project_feature_spec` 고정 동봉 | be | SPEC-004, SPEC-010, SPEC-014 | project 초안이 원본요약(main)+기능정의서(derived) 템플릿으로 조립되고 경로가 3층으로 매핑됨 | ⬜ todo |
| **4. 게이트 팬아웃 실행 로직(create-only) + corp 매칭 + origin 보관** | 분류 `project` 확정 시 intake 메모 회사명 → 기존 `projects/{corp}/` 매칭(corp 바인딩). 문서화 게이트 apply를 origin raw 보관(바인드 마운트) + `main_document`(원본요약) + `derived_suggestions[]`(기능별 **`create_feature_spec` 신규만**) 팬아웃으로 확장. **dedup 매칭·`supplement_existing_feature`·map.md 재생성 훅은 이 Phase에서 제외(후속 WP)** | be | SPEC-014, SPEC-004 | 메모 회사명이 기존 corp에 매칭되고, 승인 1회로 origin raw 보관 + baseline 1 + spec N(전부 신규 생성)이 같은 승인 단위에서 적용됨 | ⬜ todo |
| **5. "프로젝트 추가" 수동 스캐폴드 + FE** | BE(**수동·독립** 프로젝트 추가 = 회사명 slugify + 충돌 분기 API, `projects/{corp}/{origin,baseline,spec}/` 동적 생성 — 업로드/분류와 별개, 자동 생성 아님), FE(`apps/web` 프로젝트 추가 UI·slug 미리보기·충돌 모달·corp 트리 뷰·게이트 팬아웃 표시 U-1~U-5) | be·fe | SPEC-014 §2 | 프로젝트 추가(수동)→스캐폴드 생성; 별도로 메모에 회사명 적은 docx 업로드→분류 project→corp 매칭→팬아웃 결과가 corp 트리에 가시화됨 | ⬜ todo |

> Phase 1은 코드repo에 반영됐으나 미커밋 상태다(설계 확정 반영분). Phase 2~5는 미착수.

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `documents` / `document_edges` | project 팬아웃 문서(원본요약 `baseline`·기능정의서 `feature_spec`) 쓰기 경로(executor 경유) + 원본요약↔기능정의서 엣지 |
| origin raw 파일(바인드 마운트, **non-node**) | `{AXKG_MARKDOWN_ROOT}/projects/{corp}/origin/{원본파일}.docx` — 첨부 docx 원본. `documents` 테이블/인덱스에 편입 안 함(바이너리) |
| `approval_gates` / `approval_gate_revisions` / `apply_plans` | project destination의 main+derived 팬아웃 apply_plan |
| `document_templates` | `project_source_summary`·`project_feature_spec` 2종 시드(WP5 Templates API 재사용) |

- 상태 / invariant: AI는 DB/Markdown을 직접 쓰지 않는다 — executor만. 경로 디렉토리는 시스템이 조립(AI는 파일명/stem만, SPEC-004 §4). **v1은 기능정의서를 항상 create-only(신규 생성)** — dedup(`{corp}` 경계 매칭·보강)은 후속 WP. origin은 그래프 노드가 아니라 바인드 마운트 raw 파일이다.
- Migration 필요 여부: 신규 컬럼 없음 전제(문서 타입·경로 확장은 코드 매핑). 세부는 구현 시 확정.
- SPEC에 환류: 없음 예상(SPEC-014가 SSOT).

## Acceptance

- [ ] AXKG-SPEC-014 Acceptance Criteria 중 **이번 WP 범위 항목** 충족(스캐폴드·docx 텍스트추출·팬아웃 main+derived **create-only**·origin raw 보관·연결 링크·3층 트리). **기능 dedup·map.md 재생성 AC는 후속 WP**
- [ ] Phase 1: project 분류 초안이 원본요약+기능정의서 팬아웃 형태로 산출된다(템플릿 2종 시드 반영)
- [ ] Phase 2: `.docx` 업로드가 본문 텍스트만 추출돼 요약①로 넘어가고, intake 메모(회사명 등)가 탭과 무관하게 항상 요약 컨텍스트로 동반된다(파싱 계약 없음)
- [ ] Phase 3: destination→`projects/{corp}/{origin,baseline,spec}/` 매핑 + project 템플릿 조립이 동작한다
- [ ] Phase 4: 분류 `project` 확정 시 메모 회사명이 기존 `projects/{corp}/`에 매칭되고, 게이트 승인 1회로 origin raw 보관(바인드 마운트) + baseline 1 + spec N(전부 `create_feature_spec` 신규 생성) 팬아웃이 같은 승인 단위에서 적용된다(dedup·map.md 제외)
- [ ] Phase 5: "프로젝트 추가"는 수동·독립 스캐폴딩이며 업로드/분류가 프로젝트를 자동 생성하지 않는다 — 수동 생성 후 메모에 회사명 적은 docx 업로드→corp 매칭→팬아웃 결과가 corp 트리에 가시화된다(U-1~U-5)

## Rollback

- 작업 레포 커밋 단위 revert. 적용된 Markdown은 git으로 revert.

## Open Issues

- **기능 dedup(corp 스코핑 retriever 매칭·`supplement_existing_feature` 보강)·폴더별 `map.md` 자동 재생성은 후속 WP로 분리한다** — v1은 기능정의서를 항상 `create_feature_spec` 신규 생성. SPEC-014 설계 계약(dedup·map.md)은 유지되며 구현만 이번 라운드에서 제외한다.
- Phase 1 note: `seeds.py` documentation_gate 프롬프트에 이미 `supplement_existing_feature` 분기가 있으나, v1은 게이트에 기존 기능 컨텍스트를 주입하지 않아(dedup 미배선) 자연히 항상 신규 생성된다 — 프롬프트 재작성은 불필요.
- 기능 dedup 매칭 임계값(같은 기능 판정 기준)은 후속 dedup WP의 튜닝 대상 — SPEC-014 Open Questions(구현 세부 후속).
- Migration 필요 여부(문서 타입 `feature_spec`·경로 확장)는 Phase 3 착수 시 코드 확인.
