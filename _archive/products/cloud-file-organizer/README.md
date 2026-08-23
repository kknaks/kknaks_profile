# cloud-file-organizer

## 목적

Google Drive 데모를 통해 파일 업로드, AI 메타데이터 후보, 사람 승인 흐름을 검증하는 제품의 SSOT다. 부서별 문서 관리는 트리축(물리 귀속)과 지식그래프축(논리 연결)의 이중 축으로 확정했다(DEC-004/DEC-005).

규칙: `rules/product-doc-pipeline.md`

> ID prefix: frontmatter `id`는 전역 유일성을 위해 `CFO-` prefix를 쓴다 (`CFO-SPEC-001` 등, AXKG/MRT 컨벤션 동일). 본문/표의 `BASE/DEC/SPEC/WORK-###` 표기는 제품 내 축약형이다.

> DEC-001~024 accepted, SPEC-001~007 draft. 다음 단계는 work 분해다.

## 코드 레포

| 항목 | 경로 |
|---|---|
| Remote | `https://github.com/kknaksss/gcs_demo` |
| Local clone | `/Users/kknaks/git/toy_pr2/gcs_demo` |
| 문서 SoT | `/Users/kknaks/git/toy_pr2/kknaks_profile/products/cloud-file-organizer` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | BASE-001 accepted / BASE-002 accepted | - |
| Decision | DEC-001~024 accepted | - |
| Spec | SPEC-001~007 stable | 구현 중 변경은 spec-change로 관리 |
| Work | WORK-001~006 done (코드 구현 완료) | env 투입 후 실연동 검증 → 첫 커밋 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |

> 60-release / 70-runbook 은 필요해질 때 생성한다 (optional).

## 최근 로그

전체 이력은 `log.md`.

- 2026-07-08 제품 문서 스캐폴딩 생성 및 BASE-001 등록
- 2026-07-08 DEC-001 작성 — Google Drive-only 데모, Drive changes.watch 기반 후킹, AI 제안/사람 승인, DB 링크 저장 결정
- 2026-07-08 BASE-002 작성 — 부서별 문서 관리, 트리축과 지식그래프축 분리, 멱등 싱크는 생각 정리 단계로 보관
- 2026-07-08 DEC-002 작성 — 문서 메타데이터 기본 축(Drive mirror, DB relation, 접근권한 policy, 생성부서, 귀속부서) 정리
- 2026-07-08 DEC-003 작성 — Google Drive를 파일 SoT로 두고 DB는 Drive 변경 내역을 반영하는 메타데이터/인덱스 저장소로 결정
- 2026-07-08 DEC-004 작성 — UI 트리 기본 구조를 `회사 > 부서 > 팀/업무 > 문서종류`로 두고 조직도는 DB 관리로 결정
- 2026-07-08 DEC-005 작성 — 문서 귀속은 물리 트리 위치 1개, 관련 부서는 논리 연결 N개로 결정
- 2026-07-08 DEC-006 작성 — 사용자 DB의 부서/직급/권한으로 문서 읽기 권한을 판정하기로 결정
- 2026-07-08 DEC-007 작성 — 문서종류는 전사 공통 DB 카탈로그로 관리하고 관리자만 승인 게이트에서 추가 가능하게 결정. merge/shortcut은 v1 제외
- 2026-07-08 DEC-008 작성 — 민감 문서 정책은 `context/policy.md`에 두고 Claude/agent가 권한 판단 시 읽도록 결정
- 2026-07-08 BASE-002 accepted — 부서별 문서 관리/트리축/지식그래프축 방향을 DEC-002/004/005/006/007/008로 승격 완료
- 2026-07-08 DEC-009 작성 — v1 Google Drive intake는 선택 폴더 1개, 최소 OAuth scope, metadata-only fallback으로 결정
- 2026-07-08 DEC-010 작성 — UI/AI wikilink 후보를 DB relation으로 승인 저장하고 related department/product를 승인 필드로 결정
- 2026-07-08 DEC-011 작성 — Drive 삭제는 soft delete, 기본 제목은 drive_name, 승인 대기 중 Drive 변경 시 후보 stale 처리로 결정
- 2026-07-08 DEC-012 작성 — 조직도 DB는 회사/부서/팀, 문서 트리 설정은 업무/문서종류를 관리하기로 결정
- 2026-07-08 DEC-013 작성 — 비활성 조직의 기존 문서는 기존 path에 유지하고 표시하되 새 귀속 대상으로는 막기로 결정
- 2026-07-08 DEC-014 작성 — 부서 기본 목록은 물리 귀속 문서만, 논리 연결 문서는 관련 문서 영역/검색에 노출하기로 결정
- 2026-07-08 DEC-015 작성 — physical_tree_path 현재값과 변경 이력을 분리하고 append-only audit으로 보존하기로 결정
- 2026-07-08 DEC-016 작성 — 접근권한 원장은 named policy로 두고 boolean vector는 판정 결과/log로만 쓰기로 결정
- 2026-07-08 DEC-017 작성 — 민감 문서 정책은 전역 `context/policy.md`를 단일 원장으로 유지하고 향후 DB 승격 가능하게 결정
- 2026-07-08 DEC-018 작성 — 민감 문서 preset은 AI 추천 후보로 두고 관리자가 승인하기로 결정
- 2026-07-08 DEC-019 작성 — 데모 v1은 `drive.readonly` scope를 기본으로 쓰고 선택 폴더 제한/원문 미저장을 안전 경계로 결정
- 2026-07-08 DEC-020 작성 — v1 문서 relation type은 related/references/supersedes/duplicate_candidate 4개로 결정
- 2026-07-08 DEC-021 작성 — target 없는 wikilink는 unresolved relation candidate로 보관하고 새 문서 자동 생성은 하지 않기로 결정
- 2026-07-08 DEC-022 작성 — stale 후보 발생 시 자동 재분석하고 실패 시 관리자 수동 재분석 버튼을 제공하기로 결정
- 2026-07-08 DEC-023 작성 — Drive stale 판정은 단일 revision이 아니라 composite fingerprint 기준으로 결정
- 2026-07-08 DEC-002 accepted — 문서 metadata 기본 정의를 Drive mirror, 물리 귀속, 논리 연결, named access policy, 승인 후보 기준으로 확정
- 2026-07-08 SPEC-001 작성 — 기존 Mediness `public.users` seed 기반 User & RBAC 계약 작성
- 2026-07-08 SPEC-002 작성 — 조직도와 문서 트리 설정, 비활성 조직, physical_tree_path 이관 계약 작성
- 2026-07-08 SPEC-003 작성 — 문서 record, Drive mirror, 승인 metadata, 후보 상태, composite fingerprint 계약 작성
- 2026-07-08 SPEC-004 작성 — Google Drive connector, 선택 폴더 sync, watch/list, stale 재분석 트리거 계약 작성
- 2026-07-08 SPEC-005 작성 — 관리자 승인 게이트, 문서종류 추가, 민감 preset, stale/unresolved 후보 처리 계약 작성
- 2026-07-08 SPEC-006 작성 — 문서 relation, 관련 문서 영역, 검색 출처 표시, 권한 필터 계약 작성
- 2026-07-08 DEC-024/SPEC-007 작성 — open-kknaks 기반 AI 문서 분류 파이프라인 계약 추가
- 2026-07-08 ARCH-001 작성 — FastAPI/Next.js/PG/Redis/docker 기반 시스템 아키텍처와 레이어 규칙 정의
- 2026-07-08 ARCH-001/002 보강 — 권장 시스템 기본값 채택, AI queue 상태 추적용 PostgreSQL job table 정의
- 2026-07-08 정합성 검증 반영 — OAuth scope(DEC-019 우선), 후보 enum 통일, 조직도 노드 id 매핑, 예시 경로 정정 등 Critical 3건/Warning 8건 해소
- 2026-07-08 ARCH-002 spec 기준 정렬 + 코드 레포(gcs_demo) 확정
- 2026-07-08 ARCH-003 작성 — SPEC-001~007 기준 core domain 테이블/ERD 정의
- 2026-07-08 21-html 화면별 3분할(documents/approvals/admin-settings) + SPEC-001~007 stable 확정 + WORK-001~006 분해
