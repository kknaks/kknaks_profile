# Spec Index

규칙: `para/projects/project.md`

> 기능, UX, 정책, acceptance criteria 계약으로 들어가는 map이다. 상세 계약은 `20-spec/` 아래 사용자 기능/정책 묶음 단위의 spec 파일로 둔다.
> 본문은 contract만 다룬다. 구현 진척·work 매핑은 `30-work/README.md`, 결정 로그는 `10-decision/README.md`, 변경 이력은 `log.md`, 리뷰 artifact는 `00-baseline/`, 내부 구조는 `40-architecture/`를 본다.

최종 수정: 2026-07-08

## Scope

### In Scope

- 기존 Mediness user DB seed 기반 User/RBAC
- Google Drive 업로드/변경 이벤트 기반 수집
- AI 메타데이터 후보 생성과 사람 승인
- 자체 DB 기반 Drive 원본 링크 저장
- 부서별 트리/지식그래프 방향은 accepted decision을 기준으로 spec으로 내린다.

### Out Of Scope

- Google Cloud Storage
- 기존 Google Drive 파일 소급 처리
- 운영형 Workspace Events API + Pub/Sub 파이프라인
- 배포/운영 절차는 MVP 아키텍처가 정해진 뒤 작성한다.

## Terms

| 용어 | 의미 |
|---|---|
| 파일 메타데이터 | 파일명, 위치, MIME 타입, 크기, 업로드 시각, 업로더, 콘텐츠 분석 결과 등 파일을 구조화하기 위한 속성 |
| AI 후보 | AI가 생성했지만 아직 사람이 승인하지 않은 메타데이터 |
| 승인 메타데이터 | 사람이 승인/수정해 제품 데이터로 반영된 메타데이터 |
| 트리축 | UI에서 보이는 계층 구조. DEC-004 `회사 > 부서 > 팀/업무 > 문서종류` 기준 |
| 지식그래프축 | 문서 메타데이터와 문서 간 관계를 표현하는 연결 구조. DEC-005/DEC-010/DEC-020 기준 |
| Drive 링크 | 자체 DB row가 원본 Google Drive 파일을 참조하기 위한 `drive_file_id`, 보기 링크 등 |
| Reader profile | 파일 포맷별로 본문/표/이미지/메타데이터를 어떻게 읽을 수 있는지 나타내는 능력 정의 |
| 문서 관계 | 승인된 문서 사이의 `references`, `related`, `supersedes` 같은 연결 |
| User seed | 기존 Mediness `public.users`를 제품 내부 user/RBAC 초기 데이터로 가져오는 것 |
| RBAC | 사용자 role/department/position 기반 읽기 권한 판정 |

## Spec Bundle

| 묶음 | 포함 Spec | 파일 |
|---|---|---|
| User / RBAC | SPEC-001 | [spec-001-user-rbac.md](spec-001-user-rbac.md) |
| Organization / tree | SPEC-002 | [spec-002-organization-tree.md](spec-002-organization-tree.md) |
| Document metadata | SPEC-003 | [spec-003-document-metadata-record.md](spec-003-document-metadata-record.md) |
| Google Drive connector | SPEC-004 | [spec-004-google-drive-connector-sync.md](spec-004-google-drive-connector-sync.md) |
| Approval workflow | SPEC-005 | [spec-005-approval-gate.md](spec-005-approval-gate.md) |
| Document relation / explorer | SPEC-006 | [spec-006-document-relations-explorer.md](spec-006-document-relations-explorer.md) |
| AI classification pipeline | SPEC-007 | [spec-007-ai-classification-pipeline.md](spec-007-ai-classification-pipeline.md) |

## Spec List

spec 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다. work 진행률, owner, blocker, PR은 `30-work/README.md`로 보낸다.

| ID | Title | Area | Status | Decision | File |
|---|---|---|---|---|---|
| SPEC-001 | User & RBAC | user/rbac | stable | DEC-006 / DEC-016 / DEC-017 / DEC-018 | [spec-001-user-rbac.md](spec-001-user-rbac.md) |
| SPEC-002 | Organization & Tree | organization/tree | stable | DEC-004 / DEC-005 / DEC-007 / DEC-012 / DEC-013 / DEC-014 / DEC-015 | [spec-002-organization-tree.md](spec-002-organization-tree.md) |
| SPEC-003 | Document Metadata Record | metadata | stable | DEC-002 / DEC-003 / DEC-011 / DEC-016 / DEC-018 / DEC-023 | [spec-003-document-metadata-record.md](spec-003-document-metadata-record.md) |
| SPEC-004 | Google Drive Connector & Sync | intake/sync | stable | DEC-001 / DEC-003 / DEC-009 / DEC-011 / DEC-019 / DEC-022 / DEC-023 | [spec-004-google-drive-connector-sync.md](spec-004-google-drive-connector-sync.md) |
| SPEC-005 | Approval Gate | approval | stable | DEC-001 / DEC-007 / DEC-011 / DEC-018 / DEC-021 / DEC-022 | [spec-005-approval-gate.md](spec-005-approval-gate.md) |
| SPEC-006 | Document Relations & Explorer | relation/explorer | stable | DEC-010 / DEC-014 / DEC-020 / DEC-021 | [spec-006-document-relations-explorer.md](spec-006-document-relations-explorer.md) |
| SPEC-007 | AI Classification Pipeline | ai/pipeline | stable | DEC-024 / DEC-002 / DEC-008 / DEC-017 / DEC-018 / DEC-022 | [spec-007-ai-classification-pipeline.md](spec-007-ai-classification-pipeline.md) |

## Reading Order

| Area | Spec |
|---|---|
| Product baseline | [BASE-001](../00-baseline/baseline-001-cloud-file-metadata-structuring.md) |
| Product baseline | [BASE-002](../00-baseline/baseline-002-department-document-management-direction.md) |
| Product decision | [DEC-001](../10-decision/decision-001-google-drive-demo-intake.md) |
| Product spec | [SPEC-001](spec-001-user-rbac.md) |
| Product spec | [SPEC-002](spec-002-organization-tree.md) |
| Product spec | [SPEC-003](spec-003-document-metadata-record.md) |
| Product spec | [SPEC-004](spec-004-google-drive-connector-sync.md) |
| Product spec | [SPEC-005](spec-005-approval-gate.md) |
| Product spec | [SPEC-006](spec-006-document-relations-explorer.md) |
| Product spec | [SPEC-007](spec-007-ai-classification-pipeline.md) |

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-101 | Google Drive OAuth scope는 최소 read-only로 충분한가, 파일 export/content read까지 필요한가? | closed | DEC-009 최소 권한 원칙 → DEC-019: 데모 v1 기본 scope는 `drive.readonly` |
| OQ-102 | 데모에서 감시 대상은 사용자의 전체 My Drive인가, 선택 폴더 1개인가? | closed | DEC-009: 선택 폴더 1개 |
| OQ-103 | AI가 읽을 수 없는 파일 타입은 어떤 최소 메타데이터만 제안하는가? | closed | DEC-009: metadata-only 후보 |
| OQ-213 | UI/AI 링크 표현과 DB relation을 어떻게 변환할지 | closed | DEC-010: wikilink 후보 -> DB relation 승인 |
| OQ-214 | `related_department`, `related_product`는 승인 필드인가 후보 필드인가? | closed | DEC-010: AI 후보, 최종 승인 필드 |
| OQ-301 | Drive에서 파일이 삭제됐을 때 UI에서 숨김 처리만 할지, archive 상태로 노출할지 | closed | DEC-011: soft delete 후 일반 UI 숨김, 관리자/감사 조회 |
| OQ-302 | Drive 파일명이 바뀌면 승인된 `title`도 자동 갱신할지, Drive name과 approved title을 분리할지 | closed | DEC-011: 기본 제목은 `drive_name`, v1 approved title 없음 |
| OQ-303 | Drive parent/folder를 제품 트리축에 얼마나 반영할지 | closed | DEC-011: 수집 힌트로만 사용, 제품 트리 자동 변경 없음 |
| OQ-304 | version 검사를 숫자 version으로 할지, `updated_at`/etag 기반으로 할지 | closed | DEC-011: Drive mirror fingerprint 기반 stale 검사 |
| OQ-201 | 샘플 데이터의 첫 부서/팀/문서 종류는 무엇으로 둘 것인가? | closed | DEC-004: 기본 트리 `회사 > 부서 > 팀/업무 > 문서종류` |
| OQ-211 | `access_roles` enum을 현재 회사 role과 맞출 것인가, 데모 전용 enum으로 둘 것인가? | closed | DEC-006: 사용자 role 기반, enum 세부값은 spec |
| OQ-212 | `owning_department`는 단일값인가, 복수값인가? | closed | DEC-005: 단일값 |
| OQ-401 | 팀/업무 단위를 조직도에 둘지, 문서 트리 설정에 둘지 | closed | DEC-012: 팀은 조직도 DB, 업무는 문서 트리 설정 |
| OQ-402 | 조직도 변경으로 비활성화된 부서의 기존 문서는 어디에 보일지 | closed | DEC-013: 기존 path 유지, 일반 탐색 표시, 새 귀속 불가 |
| OQ-403 | 문서종류는 전사 공통 enum인지 부서별 enum인지 | closed | DEC-007: 전사 공통 DB 카탈로그 |
| OQ-501 | 논리 연결 문서는 부서 목록에서 기본 노출할지, "관련 문서" 탭에만 노출할지 | closed | DEC-014: 기본 목록은 물리 귀속, 논리 연결은 관련 문서 영역 |
| OQ-502 | related department가 있어도 접근권한이 없으면 목록에서 숨길지, 잠금 표시할지 | closed | DEC-006: 숨김 |
| OQ-503 | physical_tree_path 변경 이력을 보존할지 | closed | DEC-015: append-only history/audit 구조로 보존 |
| OQ-601 | 목록 노출은 읽기 권한이 없을 때 숨김인가, 잠금 표시인가? | closed | DEC-006: 숨김 |
| OQ-602 | `role`, `department`, `position` 중 충돌 시 우선순위는 어떻게 둘 것인가? | closed | DEC-016: 일반 문서는 ANY, 민감 문서는 PRESET/ALL 가능 |
| OQ-603 | 민감 문서의 기본 policy는 무엇인가? | closed | DEC-008: `context/policy.md` |
| OQ-701 | 새 문서종류 추가 권한은 모든 승인자에게 줄지 관리자에게만 줄지 | closed | DEC-007: 관리자만 |
| OQ-702 | 유사 문서종류 merge는 누가 승인할지 | closed | DEC-007: v1 제외 |
| OQ-703 | 부서별 자주 쓰는 문서종류 shortcut을 둘지 | closed | DEC-007: v1 제외 |
| OQ-801 | `context/policy.md`를 제품별로 분리할지, 전역 정책으로 유지할지 | closed | DEC-017: 전역 `context/policy.md` 단일 원장 |
| OQ-802 | 민감 문서 후보별 기본 role/department preset을 어디까지 고정할지 | closed | DEC-018: AI 추천 후보 + 관리자 승인 |
| OQ-901 | 선택 폴더를 바꾸면 기존 DB 문서는 유지할지 제외 표시할지 | closed | DEC-011: `out_of_scope`로 유지하고 일반 UI 숨김 |
| OQ-902 | `drive.readonly`를 v1 기본으로 받을지, metadata-only에서 단계적으로 요청할지 | closed | DEC-019: 데모 v1은 `drive.readonly`, 선택 폴더 제한과 원문 미저장 |
| OQ-1001 | v1 relation_type 기본 목록은 무엇으로 둘 것인가? | closed | DEC-020: related/references/supersedes/duplicate_candidate |
| OQ-1002 | target 문서가 없는 wikilink 후보를 새 문서 생성 후보로 연결할지 | closed | DEC-021: unresolved relation candidate로 보관, 자동 생성 없음 |
| OQ-1101 | stale 후보 발생 시 자동 재분석할지, 관리자 버튼으로 재분석할지 | closed | DEC-022: 자동 재분석, 실패 시 수동 재분석 버튼 |
| OQ-1102 | Google Drive API에서 파일 타입별로 어떤 version/revision 필드를 안정적으로 쓸 수 있는지 | closed | DEC-023: composite fingerprint 사용, 타입별 매핑은 spec 검증 |
