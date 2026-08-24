---
type: work
id: CFO-WORK-006
title: "문서 탐색/관계"
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
    - "[[spec-006-document-relations-explorer]]"
  works:
    - "[[work-005-approval-gate]]"
  releases: []
  related: []
---

# 문서 탐색/관계

일반 사용자가 승인된 문서를 탐색하는 최종 표면을 만든다 — 물리 귀속 목록, 관련 문서 영역, 통합 검색 + 출처 badge, 문서 상세 relation, RBAC 숨김 적용, `documents` 화면. 데이터 생산(수집/분류/승인)은 이 WP 범위 밖이다.

> 1 파일 = 1 work = **빌드 계획**. SPEC 본문은 복제하지 않고 ID/링크로 참조한다. Status Board / Spec Coverage는 `30-work/README.md`가 담당한다.

## Meta

- Baseline: BASE-002 (spec 경유)
- Covers spec: SPEC-006 (Document Relations & Explorer) + SPEC-002 문서 목록 API 잔여(`/tree-documents`, `/related-documents`) + SPEC-003 문서 상세 사용자 노출 AC
- Depends on work: WORK-005 (approved metadata·`document_relations`가 데이터 원천), WORK-001 (RBAC 판정 core)
- Parallel work: FE 골격(트리 sidebar/목록 레이아웃)은 WORK-005 진행 중 fixture로 선행 가능
- Follow-up work: 없음 (v1 마지막 WP)
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
| Next | 전 WP 완료. env 투입 후 실연동 검증 → 첫 커밋 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | SPEC-006 계약 범위 고정 | done |
| Design | kknaks | 탐색/검색/상세 UX (SPEC-006 U-1~U-4) | done |
| FE | kknaks | documents 화면 전체 | done |
| BE | kknaks | 목록/관련/검색/relation API + RBAC 필터 | done |
| QA | kknaks | 권한 숨김 매트릭스 검증 | done |
| Ops | kknaks | 없음 (신규 env 없음) | done |

## Scope

포함:

- 물리 귀속 목록: `GET /tree-documents`(path 기준, SPEC-002 계약) — 물리 귀속만, 논리 연결 미혼입, RBAC 필터 적용
- 관련 문서: `GET /documents/{id}/related`, `GET /departments/{id}/related-documents`(+ SPEC-002 `GET /related-documents`) — `related_departments`/`related_products`/승인 `document_relations` 3원천, source label·match_reason
- 문서 상세 relation: `GET /documents/{id}/relations` — approved relation만, target `drive_state` 파생 `broken`/unavailable 숨김
- 통합 검색: `GET /search/documents` — 물리 귀속+관련 문서, `source_badge`(`physical`/`related`), source filter, 실제 path 표시
- `GET /relation-types` — v1 enum 4종
- RBAC 숨김 통합 적용: 목록/트리/검색/관련/상세 relation 전부에서 read policy 불만족·unavailable 문서 숨김(잠금 표시 없음), admin은 전체 열람
- 문서 상세 사용자 노출 완성 (SPEC-003 U-1/U-2): `drive_name` 제목, state badge, `Drive에서 열기`, 승인 metadata 섹션(문서 정보/귀속/권한/요약/Drive 정보), admin 전용 후보/mirror 배지
- FE `app/documents`: 조직 트리 sidebar(SPEC-002 U-1) + breadcrumb + 물리 귀속 목록 + 관련 문서 영역 + 검색 + 문서 상세(relation 섹션 포함)

제외:

- relation 후보 승인/resolve UI → WORK-005 완료분
- relation type 자유 입력, duplicate merge, placeholder document (SPEC-006 Out of scope)
- 조직/트리 설정 화면 → WORK-002 완료분

## Code Surface

- Repo / module: `gcs_demo`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `backend/app/api/routers/documents.py` · `explorer.py` · `search.py` | 목록/관련/검색/relation endpoint |
| `backend/app/services/explorer.py` · `services/search.py` | 3원천 관련 문서 병합, RBAC 필터 orchestration |
| `backend/app/services/rbac.py` | WORK-001 core 소비 (변경 최소) |
| `backend/app/repos/documents.py` · `repos/relations.py` | path/GIN index 조회, relation 조회 (stmt는 여기만) |
| `frontend/app/documents/page.tsx` (+상세 라우트) | 탐색 화면 본체 |
| `frontend/components/document/` · `components/relation/` | 트리 sidebar, 목록, 관련 영역, relation 섹션, 출처 badge |
| `frontend/lib/api/` · `lib/schemas/` | typed client 확장 |

- Domain / schema note: 신규 테이블 없음. 조회 성능은 ARCH-003 index(`organization_path`/`tree_path`/`read_departments` GIN) 활용. SQLAlchemy stmt는 repo 전용.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `documents` | 승인 path/related/read policy 기반 조회 대상 |
| `document_relations` | approved relation 탐색 (unresolved candidate는 미노출) |
| `document_related_departments` | 부서 기준 관련 문서 역방향 조회 |

- 상태 / invariant: `broken`은 저장 없이 target `drive_state`에서 파생 (SPEC-006/ARCH-003). 기본 목록=물리 귀속, 관련 영역=논리 연결 — 혼입 금지 (DEC-014)
- Migration 필요 여부: 없음
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 검색 구현 방식(LIKE/tsvector) 확정 시 architecture 노트 환류

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| (최종 소비자) | 없음 | v1 사용자 표면의 종착 WP |

## Internal Interface Contract

- 해당 없음 — 외부 계약은 SPEC-006, 내부적으로 WORK-001 `evaluate_read`와 WORK-005 산출 데이터를 소비만 한다.

## Execution

### Phase 1 — 물리 귀속 목록 + 관련 문서 + relation BE

- **Status**: DONE
- **설명**: 탐색의 데이터 계약. 물리/논리 경계와 RBAC 필터가 핵심이다.
- **작업**:
  - [x] `GET /tree-documents` — path(노드 id) 기준 물리 귀속 조회 + RBAC/state 필터
  - [x] 관련 문서 3원천 병합(source/match_reason/relation_type) + 권한·unavailable 제거
  - [x] `GET /documents/{id}/relations` — approved만, target 파생 상태 처리, `GET /relation-types`
- **검증**:
  - [x] 물리 귀속 목록에 논리 연결 문서 미혼입 (SPEC-006 AC)
  - [x] unresolved relation candidate가 어떤 응답에도 미노출
  - [x] target trashed/removed/out_of_scope 시 일반 사용자 숨김
- **완료 증거**: `services/explorer.py`·`api/routers/explorer.py` — /tree-documents(GIN contains, 물리 귀속만), 관련 문서 3원천(dedupe 우선순위 relation>부서>제품), /documents/{id}/relations(approved만·target_state 파생·unreadable 숨김), /relation-types. RBAC은 evaluate_read 단독 소비

### Phase 2 — 통합 검색 BE

- **Status**: DONE
- **설명**: 물리 귀속과 관련 문서를 함께 찾되 출처를 흐리지 않는다.
- **작업**:
  - [x] `GET /search/documents` — drive_name/승인 metadata 검색, `source_badge`, source filter(`전체`/`물리 귀속`/`관련 문서`), 실제 `physical_tree_path` 동봉
  - [x] RBAC/state 필터 공통 적용
- **검증**:
  - [x] 결과마다 badge·실제 path 표시, 권한 없는 문서 미포함
  - [x] `SEARCH_EMPTY` 등 Case Matrix 처리
- **완료 증거**: `api/routers/search.py` — drive_name/summary ILIKE, source_badge(physical/related)+필터, 실제 path 동봉. DocumentDetailOut 확장(문서종류/path 표시명 join, admin 전용 pending_candidate). pytest 신규 17

### Phase 3 — FE documents 화면

- **Status**: DONE
- **설명**: SPEC-002 U-1~U-3 + SPEC-003 U-1/U-2 + SPEC-006 U-1~U-4를 하나의 탐색 화면으로 조립한다. `21-html/page-documents.html` 시안 기준 (트리 사이드바, 물리 귀속/관련 문서/검색 섹션 구분, 출처 badge, 상세/이관 modal 포함).
- **작업**:
  - [x] 조직 트리 sidebar(active/inactive `비활성` suffix, 빈 상태 CTA) + breadcrumb + 물리 귀속 목록(`물리 귀속` label, 빈 상태 문구)
  - [x] 관련 문서 영역(`관련 부서`/`관련 제품`/`문서 관계` source label, relation label 관련/참조/대체/중복 후보, type filter)
  - [x] 검색 UI(badge, source filter) + 문서 상세(제목=`drive_name`, state badge, `Drive에서 열기`, metadata 섹션, relation 섹션)
- **검증**:
  - [x] inactive 조직 클릭 시 기존 문서 표시 + `비활성 조직` badge (DEC-013)
  - [x] `tsc --noEmit`·`npm run build` 통과
- **완료 증거**: `app/documents/page.tsx` 전면 구현 — 시안 ①~⑥ 섹션/카피 그대로(트리 사이드바+비활성 suffix, 물리 목록, 관련 문서 3원천+관계 필터, 검색 badge/필터, 상세 metadata 섹션, 문서 연결). 이관 진입점을 reassign-modal 재사용으로 교체(카탈로그 임시 UI 제거), member는 admin CTA/NAV 미렌더. tsc·build 통과

### Phase 4 — RBAC 숨김 통합 검증 (e2e 시나리오)

- **Status**: DONE
- **설명**: SPEC-001/006의 숨김 계약을 표면 전체에서 교차 검증한다. v1 데모의 완료 판정 Phase.
- **작업**:
  - [x] 권한 매트릭스 시나리오: admin/member(부서 A)/member(부서 B)/`department_node_id` null 사용자 × 일반/민감(PRESET) 문서
  - [x] 목록·트리·검색·관련·상세 relation 5개 표면에서 숨김 동작 확인 (잠금 표시 없음)
- **검증**:
  - [x] 권한 없는 문서가 5개 표면 모두에서 미노출, 직접 URL 접근 시 `DOCUMENT_NOT_READABLE`(문서를 찾을 수 없습니다)
  - [x] admin은 민감 문서 포함 전체 열람 (SPEC-001 AC)
- **완료 증거**: `test_rbac_hidden_across_five_surfaces` — seed 계정(admin/fe/hr/미매핑)×민감 PRESET 문서로 목록/관련/검색/relation/직접 접근 5표면 교차 검증, 직접 접근 404 DOCUMENT_NOT_READABLE. pytest 총 172 passed — 목표 시나리오: *Drive에 넣은 파일이 승인 후 member의 부서 트리에 물리 귀속으로 나타나고, 다른 부서 member에게는 보이지 않는다. 검색에서 관련 문서는 `관련 문서` badge로 구분되고, 문서 상세에서 승인된 relation을 따라 이동할 수 있다*

## Pre-deploy Check

- [ ] 권한 없는 문서가 응답 payload에도 포함되지 않음 (FE 필터가 아니라 BE 제거)
- [ ] 상세 응답에서 mirror/approved 구분 유지, 후보값이 확정값처럼 노출 안 됨
- [ ] 검색 응답에 PII/비공개 필드 없음

## Rollback

- 탐색 라우터/화면 비활성화 가능 — 데이터 생산 파이프(수집/분류/승인)는 독립 동작
- 데이터 변경 없음(조회 전용 WP)이라 데이터 rollback 불필요

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] SPEC-006 AC 전 항목 + SPEC-002 문서 목록 AC 잔여 + SPEC-001 숨김 AC가 Phase 검증에 반영됐다.
- [ ] 필요한 테스트/검증이 끝났다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 검색 구현 방식(단순 ILIKE vs PostgreSQL full-text) — v1 데모 규모면 ILIKE로 충분할 가능성. 구현 시 확정
- 문서 상세 라우트 구조(`app/documents/[id]` 신설) — 스캐폴딩에 목록 page만 있어 상세 라우트 추가 필요

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Work: (frontmatter `links.works` 참조)
