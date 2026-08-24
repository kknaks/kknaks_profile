# Decision Index

규칙: `para/projects/project.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| DEC-001 | Google Drive 데모 수집/메타데이터 승인 구조 | accepted | BASE-001 | Drive changes.watch + changes.list 기반 intake, AI 제안/사람 승인, DB 링크 저장 | SPEC-004 / SPEC-005 |
| DEC-002 | 문서 메타데이터 기본 정의 | accepted | BASE-001 / BASE-002 | Drive mirror, 물리 귀속, 논리 연결, named access policy, 승인 후보를 DB metadata 기본 축으로 확정 | SPEC-003 / SPEC-007 |
| DEC-003 | Google Drive 문서 SoT와 DB 동기화 기준 | accepted | BASE-001 / BASE-002 | Google Drive가 파일 SoT, DB는 Drive 변경 내역을 반영하는 메타데이터/인덱스 저장소. 동시성은 `drive_file_id` 단위 멱등/버전 검사 | SPEC-003 / SPEC-004 |
| DEC-004 | 부서별 UI 트리와 조직도 DB 관리 | accepted | BASE-002 | UI 트리는 `회사 > 부서 > 팀/업무 > 문서종류`, 조직도는 DB 관리 | SPEC-002 |
| DEC-005 | 문서 귀속: 단일 물리 트리와 다중 논리 연결 | accepted | BASE-002 | 문서는 물리 트리 위치 1개를 갖고, 관련 부서는 지식그래프/메타데이터로 N개 연결 | SPEC-002 |
| DEC-006 | 사용자 속성 기반 문서 읽기 권한 | accepted | BASE-002 | 사용자 DB의 부서/직급/권한으로 문서 읽기 권한 판정. 초기 범위는 read-only | SPEC-001 |
| DEC-007 | 전사 공통 문서종류 카탈로그와 승인 게이트 추가 | accepted | BASE-002 | 문서종류는 전사 공통 DB 카탈로그, 관리자만 승인 게이트에서 추가 가능. merge/shortcut은 v1 제외 | SPEC-002 / SPEC-005 |
| DEC-008 | 민감 문서 정책 컨텍스트와 Claude 진입 흐름 | accepted | BASE-002 | 민감 문서 정책은 `context/policy.md`, Claude/agent가 민감도/권한 판단 시 읽음 | SPEC-007 |
| DEC-009 | Google Drive intake scope | accepted | BASE-001 | v1은 선택 폴더 1개 감시, 읽을 수 없는 파일은 metadata-only 후보로 처리. 기본 scope는 DEC-019로 대체 | SPEC-004 |
| DEC-010 | 문서 relation과 related metadata 승인 기준 | accepted | BASE-002 | UI/AI wikilink 표현은 후보, DB relation이 SoT. related department/product는 승인 필드 | SPEC-006 |
| DEC-011 | Drive sync 상태와 승인 대기 중 변경 처리 | accepted | BASE-001 | Drive 삭제는 soft delete, 기본 제목은 drive_name, 승인 대기 중 변경되면 후보 stale 처리 | SPEC-003 / SPEC-004 / SPEC-005 |
| DEC-012 | 조직도와 문서 트리 설정의 경계 | accepted | BASE-002 | 조직도 DB는 회사/부서/팀, 문서 트리 설정은 업무/문서종류를 관리 | SPEC-002 |
| DEC-013 | 비활성 조직의 기존 문서 노출 기준 | accepted | BASE-002 | 비활성 조직의 기존 문서는 기존 path에 유지하고 표시, 새 귀속 대상으로는 선택 불가 | SPEC-002 |
| DEC-014 | 물리 귀속 목록과 관련 문서 노출 분리 | accepted | BASE-002 | 기본 목록은 물리 귀속 문서만, 논리 연결 문서는 관련 문서 영역/검색에 노출 | SPEC-002 / SPEC-006 |
| DEC-015 | physical_tree_path 변경 이력 보존 | accepted | BASE-002 | 현재 path는 document row, 변경 이력은 append-only audit으로 보존 | SPEC-002 |
| DEC-016 | 읽기 권한 policy와 boolean vector 사용 범위 | accepted | BASE-002 | 원장은 named policy, boolean vector는 판정 결과/log로만 사용 | SPEC-001 / SPEC-003 |
| DEC-017 | 민감 문서 정책의 전역 단일 원장 | accepted | BASE-002 | 전역 `context/policy.md`를 정책 SoT로 유지하고 향후 DB 테이블 승격 가능 | SPEC-001 / SPEC-007 |
| DEC-018 | 민감 문서 preset 추천과 승인 기준 | accepted | BASE-002 | AI는 HR/계약/재무/보안/법무 preset 후보를 추천하고 관리자가 승인 | SPEC-001 / SPEC-003 / SPEC-005 / SPEC-007 |
| DEC-019 | 데모 v1 Google Drive readonly scope | accepted | BASE-001 | 데모 v1은 `drive.readonly`, 선택 폴더 제한, 원문 미저장으로 진행 | SPEC-004 |
| DEC-020 | v1 문서 relation type 기본 목록 | accepted | BASE-002 | relation type은 related/references/supersedes/duplicate_candidate 4개로 시작 | SPEC-006 |
| DEC-021 | target 없는 relation 후보 처리 | accepted | BASE-002 | target 없는 wikilink는 unresolved 후보로 보관하고 새 문서 자동 생성은 하지 않음 | SPEC-005 / SPEC-006 |
| DEC-022 | stale 후보 자동 재분석 | accepted | BASE-001 | Drive 변경으로 후보가 stale되면 자동 재분석하고 실패 시 수동 재분석 제공 | SPEC-004 / SPEC-005 / SPEC-007 |
| DEC-023 | Drive composite fingerprint 기준 | accepted | BASE-001 | stale 판정은 drive_file_id/modified_time/name/mime_type 등 composite fingerprint 기준 | SPEC-003 / SPEC-004 |
| DEC-024 | open-kknaks 기반 AI 문서 분류 파이프라인 | accepted | BASE-001 / BASE-002 | AI 분류/후보 생성은 open-kknaks task로 실행하고 제품 backend가 결과 검증 후 candidate 저장 | SPEC-007 |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-101 | Google Drive OAuth scope는 최소 read-only로 충분한가, 파일 export/content read까지 필요한가? | closed | DEC-009 최소 권한 원칙 → DEC-019: 데모 v1 기본 scope는 `drive.readonly` |
| OQ-102 | 데모에서 감시 대상은 사용자의 전체 My Drive인가, 선택 폴더 1개인가? | closed | DEC-009: 선택 폴더 1개 |
| OQ-103 | AI가 읽을 수 없는 파일 타입은 어떤 최소 메타데이터만 제안하는가? | closed | DEC-009: metadata-only 후보 |
| OQ-211 | `access_roles` enum을 현재 회사 role과 맞출 것인가, 데모 전용 enum으로 둘 것인가? | closed | DEC-006: 사용자 role 기반, enum 세부값은 spec |
| OQ-212 | `owning_department`는 단일값인가, 복수값인가? | closed | DEC-005: 단일값 |
| OQ-213 | UI/AI 링크 표현과 DB relation을 어떻게 변환할지 | closed | DEC-010: wikilink 후보 -> DB relation 승인 |
| OQ-214 | `related_department`, `related_product`는 승인 필드인가 후보 필드인가? | closed | DEC-010: AI 후보, 최종 승인 필드 |
| OQ-301 | Drive에서 파일이 삭제됐을 때 UI에서 숨김 처리만 할지, archive 상태로 노출할지 | closed | DEC-011: soft delete 후 일반 UI 숨김, 관리자/감사 조회 |
| OQ-302 | Drive 파일명이 바뀌면 승인된 `title`도 자동 갱신할지, Drive name과 approved title을 분리할지 | closed | DEC-011: 기본 제목은 `drive_name`, v1 approved title 없음 |
| OQ-303 | Drive parent/folder를 제품 트리축에 얼마나 반영할지 | closed | DEC-011: 수집 힌트로만 사용, 제품 트리 자동 변경 없음 |
| OQ-304 | version 검사를 숫자 version으로 할지, `updated_at`/etag 기반으로 할지 | closed | DEC-011: Drive mirror fingerprint 기반 stale 검사 |
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
