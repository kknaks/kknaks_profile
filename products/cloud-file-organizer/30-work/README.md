# Work Index

규칙: `rules/product-doc-pipeline.md`

> 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 상세 work 실행 본문은 `30-work/` 아래 1 파일 = 1 work로 둔다.
> `Status Board`는 실행 상태의 owning view다. Spec Coverage는 work frontmatter `links.specs`를 spec 중심으로 펼친 derived view다.

최종 수정: 2026-07-08

Status 값: `todo`, `in_progress`, `blocked`, `review`, `done`

의존 체인: WORK-001 → 002 → 003 → 004 → 005 → 006. 단 **WORK-002와 WORK-003은 부분 병렬 가능** — Drive mirror 수집은 트리 없이 진행되고, 트리가 필수인 지점은 AI input context(WORK-004)와 귀속 승인(WORK-005)부터다.

## Status Board

| Phase | Work | Scope | Status | Owner | 예상 기간 | 목표 완료 | PR/Branch | Blocker | Next |
|---|---|---|---|---|---|---|---|---|---|
| WP1 | WORK-001 | 기반: 마이그레이션 + Auth + Seed | done | kknaks | - | 2026-07-08 | main `a6ac641` | - | 완료 — pytest 33·seed 멱등·auth 스모크 재검증, spec-001 환류 완료 |
| WP2 | WORK-002 | 조직도/문서 트리/문서종류 | done | kknaks | - | 2026-07-08 | main `a6ac641` | - | 완료 — pytest 53·tsc/build 통과. 이관 진입점은 WORK-006에서 교체 |
| WP3 | WORK-003 | 문서 record + Drive sync | done | kknaks | - | 2026-07-08 | main `a6ac641` | - | 완료 + **실연동 검증(07-09)** — 실제 Drive 45건 수집 무손실. webhook만 잔여(폴링 운용) |
| WP4 | WORK-004 | AI 분류 파이프라인 | done | kknaks | - | 2026-07-08 | main `a6ac641` | - | 완료 + **실행 검증(07-09)** — 로컬 claude 45건 분류, 이슈 4건 수정 반영 |
| WP5 | WORK-005 | 승인 게이트 | done | kknaks | - | 2026-07-08 | main `a6ac641` | - | 완료 — pytest 155·tsc/build 통과 |
| WP6 | WORK-006 | 문서 탐색/관계 | done | kknaks | - | 2026-07-09 | main `a6ac641` | - | 완료 — pytest 172·5표면 RBAC e2e. **전 WP 코드 구현 완료**, env 투입 후 실연동 검증 → 첫 커밋 |

## Work List

work 문서를 만들거나 상태, owner, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | File | Covers Spec |
|---|---|---|---|---|---|---|---|
| WORK-001 | 기반: DB 마이그레이션 + Auth + User Seed | new-feature | kknaks | done | 100% | [work-001-foundation-auth-seed.md](work-001-foundation-auth-seed.md) | SPEC-001 |
| WORK-002 | 조직도/문서 트리/문서종류 | new-feature | kknaks | done | 100% | [work-002-organization-tree-catalog.md](work-002-organization-tree-catalog.md) | SPEC-002 |
| WORK-003 | 문서 record + Drive sync | new-feature | kknaks | done | 100% | [work-003-document-record-drive-sync.md](work-003-document-record-drive-sync.md) | SPEC-003, SPEC-004 |
| WORK-004 | AI 분류 파이프라인 | new-feature | kknaks | done | 100% | [work-004-ai-classification-pipeline.md](work-004-ai-classification-pipeline.md) | SPEC-007 |
| WORK-005 | 승인 게이트 | new-feature | kknaks | done | 100% | [work-005-approval-gate.md](work-005-approval-gate.md) | SPEC-005 |
| WORK-006 | 문서 탐색/관계 | new-feature | kknaks | done | 100% | [work-006-document-explorer-relations.md](work-006-document-explorer-relations.md) | SPEC-006 |

## Spec Coverage

각 spec이 어느 work에서 구현되며 현재 진척이 어떤지 한눈에 보는 spec-centric view다. Covering Work의 Status를 종합한 derived view다.

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 User & RBAC | WORK-001 (판정 core·seed·auth), WORK-006 (탐색 표면 숨김 적용) | done |
| SPEC-002 Organization & Tree | WORK-002 (노드 CRUD·카탈로그·이관), WORK-006 (`/tree-documents`·`/related-documents` 목록 API) | done |
| SPEC-003 Document Metadata Record | WORK-003 (mirror·fingerprint·state), WORK-005 (candidate 승인 반영), WORK-006 (사용자 상세 노출) | done |
| SPEC-004 Google Drive Connector & Sync | WORK-003 | done (실연동 검증 완료 — webhook만 잔여) |
| SPEC-005 Approval Gate | WORK-005 | done |
| SPEC-006 Document Relations & Explorer | WORK-006 | done |
| SPEC-007 AI Classification Pipeline | WORK-004 | done (실 실행 검증 완료) |

## Release Gate

### Scope

- [ ] 릴리즈 대상 spec이 정해졌다.
- [ ] 포함/제외 범위가 decision/spec과 맞다.

### Code

- [ ] 연결된 제품 PR이 merge됐다.
- [ ] 필요한 migration/환경변수/외부 설정이 반영됐다.

### Spec

- [ ] 필요한 `20-spec/README.md` / `20-spec/` 변경이 리뷰됐다.
- [ ] blocker open question이 없다.

### Baseline / UX

- [x] 필요한 baseline artifact가 연결됐다.
- [ ] Known UX issue는 Product/Design이 승인했다.

### QA

- [ ] 필요한 QA case가 실행됐다.
- [ ] blocking fail이 없다.

### Approval

- [ ] Product
- [ ] QA
- [ ] Tech Lead
- [ ] 범위, 벤더 경로, 정책, 비용, 일정, 고객 약속이 바뀐 경우 Decision Owner
