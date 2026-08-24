---
type: work
id: CFO-WORK-005
title: "승인 게이트"
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
    - "[[spec-005-approval-gate]]"
  works:
    - "[[work-002-organization-tree-catalog]]"
    - "[[work-004-ai-classification-pipeline]]"
  releases: []
  related: []
---

# 승인 게이트

AI candidate를 admin이 검토·수정·승인·거절하는 게이트를 BE+FE 세로 슬라이스로 만든다 — 후보 큐/상세, stale 차단 + 표시용 재분석 상태, 문서종류 추가, 민감 preset, relation 후보 처리, `admin/approvals` 화면. AI 실행 자체(WORK-004)와 탐색 화면(WORK-006)은 범위 밖이다.

> 1 파일 = 1 work = **빌드 계획**. SPEC 본문은 복제하지 않고 ID/링크로 참조한다. Status Board / Spec Coverage는 `30-work/README.md`가 담당한다.

## Meta

- Baseline: BASE-001, BASE-002 (spec 경유)
- Covers spec: SPEC-005 (Approval Gate)
- Depends on work: WORK-004 (candidate/job 원장·재분석 enqueue), WORK-002 (active path validation·카탈로그)
- Parallel work: 없음 (기본 체인)
- Follow-up work: WORK-006 (approved metadata·relation을 탐색에 노출)
- External dependency: 없음 (내부 API로 완결). 민감 preset 정의 SoT는 전역 `context/policy.md` (DEC-017)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker |  |
| Next | WORK-006 착수 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | SPEC-005 계약 범위 고정 | done |
| Design | kknaks | 승인 게이트 UX (SPEC-005 U-1~U-6) | done |
| FE | kknaks | admin/approvals 화면 전체 | done |
| BE | kknaks | 승인 트랜잭션, validation, relation 처리 | done |
| QA | kknaks | stale 차단·멱등 승인·preset 검증 | done |
| Ops | kknaks | 없음 (신규 env 없음) | done |

## Scope

포함:

- 후보 큐/상세 BE: `GET /admin/approval-candidates`(상태 필터), `GET /admin/approval-candidates/{id}` — `state` 원장 5개 + `reanalysis_status` 파생 계산(`reanalyzing`/`new_candidate_ready`/`reanalysis_failed`, 원장 미저장 — DEC-022), `current_fingerprint` 동봉, `stale_reason`/`blocked_reason`
- 승인: `POST .../approve` — state=`pending`·fingerprint 일치·document `active`·active path·access policy validation 재검사 → `documents` approved 필드 반영(노드 id 저장) + 후보 `approved` 종결, 같은 요청 재시도 멱등 성공
- 거절: `POST .../reject` — `pending`/`stale`에서 가능
- 수동 재분석: `POST .../reanalyze` — WORK-004 `enqueue_reanalysis` 위임
- 문서종류 추가: `GET/POST /admin/document-types` — admin 전용, 정규화 이름 unique, 추가 즉시 현재 form 선택 (SPEC-005 U-4/S-3)
- 민감 preset 검토: AI 추천 preset(`HR_RESTRICTED` 등 — `context/policy.md` SoT) 승인/수정/민감 아님 제거, 승인 시 read policy 필드로 풀어 저장 (DEC-018)
- relation 후보 처리: `POST /admin/relation-candidates/{id}/resolve|hold|remove|rematch` — unresolved 유지(hold), target 지정으로만 확정, rematch는 title/drive_name 재검색 제안, 자동 document 생성 금지 (DEC-021)
- FE `app/admin/approvals`: 후보 큐(필터: 전체/승인 대기/stale/재분석 중/차단됨/본문 분석 없음), 상세(stale/blocked/metadata_only 배너, CTA 활성 규칙), metadata form(문서 정보/귀속/권한/요약, 위치 선택은 active path만), 문서종류 추가 modal, 민감 preset 섹션, relation 섹션

제외:

- classification job 생성/실행 → WORK-004 (이 WP는 소비/위임만)
- 승인된 문서의 일반 사용자 탐색/상세 노출 → WORK-006
- 유사 문서종류 merge, 부서별 shortcut (SPEC-005 Out of scope, v1 제외)

## Code Surface

- Repo / module: `gcs_demo`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `backend/app/api/routers/approvals.py` · `document_types.py` · `relation_candidates.py` | 승인 게이트 admin endpoint |
| `backend/app/services/approval.py` | 승인 트랜잭션(재검사→반영→종결), 멱등, preset 풀어 저장 |
| `backend/app/services/relation_candidates.py` | resolve/hold/remove/rematch 규칙 |
| `backend/app/repos/candidates.py` · `repos/documents.py` · `repos/document_types.py` · `repos/relation_candidates.py` | DB access (stmt는 여기만) |
| `backend/app/schemas/` · `dtos/` | approval payload/candidate 응답 계약 |
| `frontend/app/admin/approvals/page.tsx` | 승인 게이트 화면 본체 |
| `frontend/components/approval/` · `components/relation/` | 큐/상세/form/preset/relation 섹션 |
| `frontend/lib/api/` · `lib/schemas/` | typed client 확장 |

- Domain / schema note: 신규 테이블 없음 (WORK-001 migration 전제). 승인 반영은 `documents` approved 필드 갱신 — mirror 필드는 불가침. `reanalysis_status`는 저장하지 않고 stale 후보 + `ai_queue_jobs` 상태에서 계산.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `metadata_candidates` | state 전이 본체 (pending→approved/rejected, stale 차단) |
| `documents` | 승인 시 approved 필드(document_type_id, 귀속 노드, path, read policy, sensitivity, preset, summary) 반영 |
| `document_types` | admin 추가 (normalized unique) |
| `relation_candidates` | pending/unresolved/approved/removed 전이 |
| `document_relations` | 승인된 relation 확정 저장 (`(source,target,type)` unique) |

- 상태 / invariant: 후보 원장 state machine SSOT는 SPEC-003/005 (동일 5 enum). 승인은 pending에서만, 거절은 pending/stale에서
- Migration 필요 여부: 없음. 필요 시 컬럼 보강만
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 승인 payload의 부서/트리 값 id resolve 규칙(현재 SPEC-005 payload는 text 표기, ARCH-003은 id 저장) 확정 시 spec 환류

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-006 | `documents` approved 필드 + `document_relations` | 탐색/검색/관련 문서의 데이터 원천 |
| WORK-006 | 승인 완료 문서의 read policy | RBAC 숨김 판정 입력 |

## Internal Interface Contract

- `services/approval.approve(candidate_id, payload, admin) -> ApprovalResult` — 내부에서 WORK-002 `validate_active_path` + WORK-001 admin guard + fingerprint 재검사를 모두 수행. 부분 반영 금지(단일 트랜잭션)
- preset 승인: `policy_preset` 이름 저장 + read policy 필드 풀어 저장을 한 번에 수행 (판정은 풀어 저장된 필드 기준 — SPEC-001)

## Execution

### Phase 1 — 후보 목록/상세 + 승인/거절/재분석 BE

- **Status**: DONE
- **설명**: 게이트의 핵심 트랜잭션. 승인 시점 재검사(state/fingerprint/document state/path/policy)가 계약의 본체다.
- **작업**:
  - [x] 후보 목록(필터)/상세 API — reanalysis_status 파생 계산, current_fingerprint 동봉
  - [x] approve 트랜잭션: 재검사 → documents approved 반영(노드 id) → 후보 종결, 멱등 재시도
  - [x] reject(pending/stale), reanalyze(WORK-004 위임), Case Matrix 에러 코드 전 항목
- **검증**:
  - [x] stale 후보 승인 시 `CANDIDATE_STALE`, unavailable 문서 승인 시 `DOCUMENT_UNAVAILABLE` (SPEC-005 AC)
  - [x] 승인 후 `documents`에 approved 필드 반영·mirror 불변, 동일 요청 재시도 멱등 성공
  - [x] inactive path 승인 거부 (`INVALID_TREE_PATH`)
- **완료 증거**: `services/approval.py`·`api/routers/approvals.py` — 승인 재검사(pending·fingerprint·active·validate_active_path 재사용), documents approved 반영(노드 id)+relation 확정+후보 종결 단일 transaction, 같은 payload 재시도 멱등. fingerprint 불일치는 원장 stale 전이 후 CANDIDATE_STALE, unavailable은 blocked 전이. reanalysis_status 3종 파생(원장 미저장, DEC-022). pytest test_approval_gate 14

### Phase 2 — 문서종류 추가 + 민감 preset + relation 후보 BE

- **Status**: DONE
- **설명**: 승인 form을 완결시키는 3개 보조 계약.
- **작업**:
  - [x] `POST /admin/document-types` — 정규화 unique, `DOCUMENT_TYPE_DUPLICATE`
  - [x] 민감 preset 승인/수정/제거 — preset 이름 + 풀어 저장 read policy, `context/policy.md` preset 목록과 정합
  - [x] relation 후보 resolve/hold/remove/rematch — unresolved는 확정 graph 미반영, resolve+승인 시 `document_relations` 저장
- **검증**:
  - [x] 중복 문서종류 거절, 추가분이 카탈로그 조회에 반영
  - [x] preset 승인 후 RBAC 판정(WORK-001 core)이 풀어 저장된 필드로 동작
  - [x] unresolved 후보로 document row가 생성되지 않음 (DEC-021)
- **완료 증거**: `core/policy_presets.py`(DEC-017 SoT 주석)+PRESET 풀어 저장(DEC-018) 후 evaluate_read 판정 테스트, `document_types.py` 추가 API(NFKC 정규화 unique·DOCUMENT_TYPE_DUPLICATE), relation resolve/hold/remove/rematch(제안만, 확정은 resolve — DEC-021). unresolved는 graph 미반영·문서 미생성

### Phase 3 — FE admin/approvals 화면

- **Status**: DONE
- **설명**: SPEC-005 U-1~U-6 전체. `21-html/page-approvals.html` 시안 기준 (원장 5개+표시용 재분석 상태 2축 badge, spec 필터 문구, form 섹션 구성 포함).
- **작업**:
  - [x] 후보 큐: 상태 필터 6종, 빈 상태 `승인할 후보가 없습니다.`, 비admin 차단
  - [x] 상세: stale/blocked/metadata_only 배너 문구(SPEC-005 U-2), CTA 활성 규칙(승인=pending만, 거절=pending/stale, 재분석=실패 시), reanalysis_status 표시
  - [x] metadata form(초기값=AI 후보), 위치 선택(active path만), 문서종류 추가 modal, 민감 preset 섹션(승인/수정/민감 아님), relation 섹션(대상 선택/보류/제거/재매칭)
- **검증**:
  - [x] stale 후보에서 승인 버튼 비활성 + stale 메시지 표시
  - [x] metadata_only 후보에 `본문 분석 없이 Drive 정보만으로 생성된 후보입니다.` 표시
  - [x] `tsc --noEmit`·`npm run build` 통과
- **완료 증거**: `app/admin/approvals` — 필터 6종, 원장+파생 2축 badge, spec 문구 배너, CTA 활성 규칙, metadata form(active path 위치 선택·귀속 자동 파생·문서종류 추가 modal·needs_admin_fix 보정 배너·민감 preset 섹션), relation 섹션(대상 선택/보류/제거/재매칭). 10s 폴링, admin guard. tsc·build 통과. pytest 155 passed(신규 21) — 목표 시나리오: *Drive에 파일을 넣으면 승인 게이트 큐에 후보가 뜨고, admin이 form을 수정·승인하면 문서에 approved metadata가 반영된다. 승인 대기 중 Drive 파일을 수정하면 후보가 stale로 바뀌어 승인이 차단되고 재분석 중 상태가 표시된다*

## Pre-deploy Check

- [ ] 승인 게이트 전 API에 admin guard — 비admin 접근 403
- [ ] 일반 사용자 응답에 승인 전 후보가 확정값처럼 노출되지 않음
- [ ] candidate_metadata/사유 필드에 원문 전문·secret 미포함

## Rollback

- 라우터 미등록으로 게이트 비활성화 — 파이프라인(WORK-004)은 후보 적재만 계속
- 잘못 승인된 metadata는 새 후보 승인 또는 admin 수정으로 덮음(후보 이력은 원장 보존)

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] SPEC-005 Acceptance Criteria 전 항목이 Phase 검증에 반영됐다.
- [ ] 필요한 테스트/검증이 끝났다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- SPEC-005 approval payload의 `owning_department` 등이 text 표기인데 저장은 노드 id (ARCH-003) — FE form은 id 선택, 응답은 최신 표시명으로 구현하고 spec 표기 정합은 구현 후 환류
- 후보 큐 목록의 페이징/정렬 기준 미정 — 구현 시 확정 (spec은 목록 계약만)

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Work: (frontmatter `links.works` 참조)
- Policy: `context/policy.md` (민감 preset SoT, DEC-017)
