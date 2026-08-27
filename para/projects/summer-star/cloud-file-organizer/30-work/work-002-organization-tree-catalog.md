---
type: work
id: CFO-WORK-002
title: "조직도/문서 트리/문서종류"
status: done
product: cloud-file-organizer
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/work
  - status/done
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-002-organization-tree]]"
  works:
    - "[[work-001-foundation-auth-seed]]"
  releases: []
  related: []
---

# 조직도/문서 트리/문서종류

조직(회사/부서/팀)·문서 트리(업무/문서종류) 노드 CRUD, 전사 공통 문서종류 카탈로그, 문서 이관 + path history, admin 설정 화면을 만든다. 문서 목록/탐색 화면(`/tree-documents` 소비 UI)은 만들지 않는다(WORK-006).

> 1 파일 = 1 work = **빌드 계획**. SPEC 본문은 복제하지 않고 ID/링크로 참조한다. Status Board / Spec Coverage는 `30-work/README.md`가 담당한다.

## Meta

- Baseline: BASE-002 (spec 경유)
- Covers spec: SPEC-002 (Organization & Tree)
- Depends on work: WORK-001 (migration·auth·기본 조직도 seed)
- Parallel work: **WORK-003과 부분 병렬 가능** — Drive mirror 수집(WORK-003)은 트리 없이 진행 가능하다. 트리가 실제로 필요한 지점은 귀속 승인(WORK-005)과 AI input context(WORK-004)부터다
- Follow-up work: WORK-004 (트리/카탈로그를 AI input context로 소비), WORK-005 (active path 승인), WORK-006 (트리 기반 탐색)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker |  |
| Next | WORK-003 착수 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | SPEC-002 계약 범위 고정 | done |
| Design | kknaks | admin 설정 화면 UX (SPEC-002 U-4/U-5) | done |
| FE | kknaks | admin/catalog 설정 화면, 이관 modal | done |
| BE | kknaks | 노드 CRUD, validation, 이관/history | done |
| QA | kknaks | 계층 validation·inactive 규칙 검증 | done |
| Ops | kknaks | 없음 (신규 env 없음) | done |

## Scope

포함:

- 조직 노드 CRUD: `GET /organization-tree`, `POST /organization-nodes`, `PATCH /organization-nodes/{id}` — 계층 validation(company root 1개, department는 company 하위, team은 department 하위), inactive 전환(hard delete 금지)
- 문서 트리 노드 CRUD: `GET /document-tree-config`, `POST /document-tree-nodes`, `PATCH /document-tree-nodes/{id}` — `work`/`document_type` type, `document_type` 노드는 카탈로그 stable id 참조
- 문서종류 카탈로그: `GET /document-types` — 조회 계약 (추가 API/모달은 승인 게이트 소관이므로 WORK-005, 단 카탈로그 테이블·정규화 unique 규칙은 여기서 확정)
- 문서 이관: `POST /documents/{id}/reassign`(active path validation + 변경 사유 필수) + `GET /documents/{id}/path-history` — `document_path_histories` append-only
- SPEC-002 Case Matrix 에러 코드 (`ORG_NODE_INACTIVE`, `INVALID_TREE_DEPTH`, `REASSIGN_REASON_REQUIRED` 등)
- FE admin 설정 화면: 조직도 / 문서 트리 설정 / 문서종류 섹션 (`app/admin/catalog`), 문서 이관 modal 컴포넌트

제외:

- `GET /tree-documents`·`GET /related-documents` 문서 목록 API와 탐색 화면 → WORK-006 (documents 데이터·RBAC 필터 필요)
- 문서종류 **추가** API/모달 (`POST /admin/document-types`) → WORK-005 (SPEC-005 U-4 승인 게이트 흐름)
- 조직 트리 sidebar의 문서 탐색 배선 → WORK-006

## Code Surface

- Repo / module: `gcs_demo`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `backend/app/api/routers/organization.py` · `document_tree.py` | 조직/트리/카탈로그/이관 endpoint |
| `backend/app/schemas/` · `dtos/` | 노드·path·history 계약 |
| `backend/app/services/organization.py` · `services/document_tree.py` | 계층 validation, inactive 규칙, 이관 트랜잭션 |
| `backend/app/repos/organization.py` · `repos/document_tree.py` · `repos/document_types.py` · `repos/path_history.py` | DB access (stmt는 여기만) |
| `frontend/app/admin/catalog/page.tsx` | 조직도/문서 트리/문서종류 admin 설정 화면 |
| `frontend/components/document/` | 이관 modal, path 표시 컴포넌트 |
| `frontend/lib/api/` · `lib/schemas/` | typed client 확장 |

- Domain / schema note: 테이블은 WORK-001 migration으로 이미 존재. 이 WP는 데이터 흐름/validation만. path array는 노드 **id** 저장(name 아님) — rename 시 path 갱신 없이 최신 표시명 반영 (SPEC-002 Implementation Rules).

## Domain / Schema

| Entity | 역할 |
|---|---|
| `organization_nodes` | 회사/부서/팀. inactive 전환만, hard delete 금지 |
| `document_tree_nodes` | 업무/문서종류 탐색 분류. 조직 노드에 부착 |
| `document_types` | 전사 공통 카탈로그. `normalized_name` unique |
| `document_path_histories` | 이관 이력 append-only (이전/새 path, 변경자, 사유, 시각) |

- 상태 / invariant: `active`/`inactive` — inactive는 새 귀속/이관 대상 선택 불가, 기존 문서 조회는 유지 (DEC-013)
- Migration 필요 여부: 없음 (WORK-001 완료 전제). 필요 시 컬럼 보강만
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 없음 예정

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-004 | 조직/트리/카탈로그 조회 repo | AI classification input의 `organization_context`/`document_tree_context`/`document_type_catalog` 조립 |
| WORK-005 | active path validation service | 승인 payload `physical_tree_path` 검증 재사용 |
| WORK-006 | 트리 조회 API + path 표시 계약 | 탐색 sidebar/heading |

## Internal Interface Contract

- `services/document_tree.validate_active_path(organization_path, tree_path) -> ValidatedPath | error` — 승인(WORK-005)·이관이 같은 함수를 사용한다. `ORG_NODE_INACTIVE`/`INVALID_TREE_PATH` 규칙 단일화

## Execution

### Phase 1 — 조직/트리/카탈로그 BE CRUD

- **Status**: DONE
- **설명**: 조직도와 문서 트리 설정의 계약 표면을 만든다.
- **작업**:
  - [x] 조직 노드 조회/생성/수정 + 계층·root validation + inactive 전환
  - [x] 문서 트리 노드 조회/생성/수정 + `document_type` 노드의 카탈로그 id 참조
  - [x] `GET /document-types` 조회, admin guard 적용(쓰기 계열)
- **검증**:
  - [x] SPEC-002 Validation 표 전 항목 (허용 계층, inactive 선택 불가) service/API test
  - [x] rename 후 path 표시가 최신 이름으로 계산됨 (id 저장 확인)
- **완료 증거**: `api/routers/organization.py`·`document_tree.py`, `services/organization.py`·`document_tree.py`, repos 4종. 계층 validation·inactive soft 전환·hard delete 경로 없음. pytest 신규 20 중 계층/트리/카탈로그 12 (총 53 passed)

### Phase 2 — 문서 이관 + path history

- **Status**: DONE
- **설명**: `physical_tree_path` 변경은 명시적 이관 action으로만 발생하고, 이력은 append-only로 남는다 (DEC-015).
- **작업**:
  - [x] `POST /documents/{id}/reassign` — active path validation + `changed_reason` 필수 + 현재 path 갱신 + history append (단일 트랜잭션)
  - [x] `GET /documents/{id}/path-history` (admin)
- **검증**:
  - [x] inactive path 선택 시 `ORG_NODE_INACTIVE`, 사유 누락 시 `REASSIGN_REASON_REQUIRED`
  - [x] 이관 후 이전/새 path·변경자·사유·시각이 history에 남고 UPDATE/DELETE 없음
  - [x] 통합 검증은 문서 record 존재 전제 — WORK-003 완료 후 실데이터 재검증 항목으로 남김 (여기서는 test fixture 문서로 검증)
- **완료 증거**: `DocumentTreeService.reassign()` 단일 transaction(사유 필수→active path 검증→path/owning 갱신+history append), `validate_active_path()` public 재사용 계약, `PathHistoryRepository`는 INSERT/SELECT만(append-only). 이관/이력 pytest 7 — inactive 거부·사유 필수·append 누적·rename 후 최신 표시명(id 저장) 커버

### Phase 3 — FE admin 설정 화면

- **Status**: DONE
- **설명**: SPEC-002 U-4/U-5 관리자 설정 화면. `21-html/page-admin-settings.html` 시안 기준 (조직도/문서 트리 설정/문서종류 섹션).
- **작업**:
  - [x] `app/admin/catalog`: 조직도 섹션(이름 변경/비활성화), 문서 트리 설정 섹션(업무 추가/수정, 문서종류 연결), 문서종류 목록
  - [x] 문서 이관 modal (현재 path 표시, active path 선택, 변경 사유 입력, `이관 저장` 활성 조건)
  - [x] admin이 아니면 접근 차단 (`FORBIDDEN_ADMIN_ONLY`)
- **검증**:
  - [x] admin 화면에서 업무 노드 추가 → 트리 설정 조회에 즉시 반영
  - [x] 비활성화한 조직이 이관 modal 선택지에서 disabled/제외 처리
  - [x] `tsc --noEmit`·`npm run build` 통과
- **완료 증거**: `app/admin/catalog` 구현(조직도 inline rename/비활성화, 업무 추가, 문서종류 연결, 카탈로그 목록, 이관 modal — active path만 선택·사유 필수). admin 아니면 렌더 차단, 미인증 /login redirect. `tsc --noEmit`·`npm run build` 통과. 목표 시나리오는 BE fixture 테스트로 검증(문서 목록 진입점은 WORK-006에서 교체)

## Pre-deploy Check

- [ ] 조직/트리 쓰기 API 전체에 admin guard 적용 확인
- [ ] hard delete 경로가 코드에 존재하지 않음 (inactive 전환만)
- [ ] 신규 env 없음 확인

## Rollback

- 라우터 미등록으로 기능 비활성화 가능. 데이터는 노드 inactive 전환으로 되돌림(삭제 없음)
- path history는 append-only라 rollback 대상 아님

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] SPEC-002 Acceptance Criteria가 Phase 검증에 반영됐다 (문서 목록 노출 항목은 WORK-006에서 최종 검증).
- [ ] 필요한 테스트/검증이 끝났다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- SPEC-002 API contract의 `GET /tree-documents`·`GET /related-documents`는 이 WP가 아니라 WORK-006에서 구현한다 — Spec Coverage상 SPEC-002의 문서 목록 AC 2건은 WORK-006 완료 시 닫힌다
- 문서 이관 실사용 검증은 승인된 문서가 생기는 WORK-005 이후에 가능 — 그 전까지 fixture 기반

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Work: (frontmatter `links.works` 참조)
