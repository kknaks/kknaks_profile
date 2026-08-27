---
type: work
id: CFO-WORK-003
title: "문서 record + Drive sync"
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
    - "[[spec-003-document-metadata-record]]"
    - "[[spec-004-google-drive-connector-sync]]"
  works:
    - "[[work-001-foundation-auth-seed]]"
    - "[[work-002-organization-tree-catalog]]"
  releases: []
  related: []
---

# 문서 record + Drive sync

Drive 선택 폴더의 변경이 document record(mirror 멱등 upsert, composite fingerprint, soft delete)로 반영되는 파이프를 만든다 — webhook/`changes.list`, watch 갱신, sync event audit, admin connector 화면까지. AI 분류 실행 자체는 만들지 않는다(WORK-004).

> 1 파일 = 1 work = **빌드 계획**. SPEC 본문은 복제하지 않고 ID/링크로 참조한다. Status Board / Spec Coverage는 `30-work/README.md`가 담당한다.

## Meta

- Baseline: BASE-001 (spec 경유)
- Covers spec: SPEC-003 (Document Metadata Record), SPEC-004 (Google Drive Connector & Sync)
- Depends on work: WORK-001 (migration·auth). WORK-002는 **부분 병렬** — mirror 수집은 트리 없이 가능, 트리는 귀속 승인(WORK-005)부터 필수
- Parallel work: WORK-002와 병렬 가능
- Follow-up work: WORK-004 (upsert/fingerprint 변경 이벤트에서 classification job enqueue)
- External dependency: Google Drive OAuth client/refresh token (`drive.readonly`, env 주입 — SPEC-004 Environment contract), webhook 공개 HTTPS URL (로컬은 tunnel 필요, 폴백으로 수동 sync trigger 사용 가능)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker |  |
| Next | WORK-004 착수. Drive 실연동 검증은 env 입력 후 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | SPEC-003/004 계약 범위 고정 | done |
| Design | kknaks | admin connector 화면 (SPEC-004 U-1~U-3) | done |
| FE | kknaks | connector 상태/sync activity 화면 | done |
| BE | kknaks | mirror upsert, Drive integration, worker | done |
| QA | kknaks | 멱등/soft delete/이어받기 검증 | done |
| Ops | kknaks | Drive env 5종 투입, webhook URL 준비 | done |

## Scope

포함:

- documents mirror 멱등 upsert: `(source_provider, drive_file_id)` 기준, mirror 필드만 갱신(승인 metadata 불가침 — SPEC-004 Implementation Rules)
- composite fingerprint 계산/저장 (DEC-023): `drive_file_id`+`drive_modified_time`+`drive_name`+`mime_type` 필수, 본문 읽은 경우 `content_fingerprint` 포함
- soft delete: 삭제/휴지통/범위 제외 → `drive_state` `trashed`/`removed`/`out_of_scope` 전환, restore 복귀, 일반 UI 숨김 전제
- Drive integration (`app/integrations/google_drive/`): OAuth env client, `changes.list` + page token 저장/이어받기(`drive_sync_state`), `changes.watch` channel 생성/갱신, 선택 폴더 하위 필터
- webhook endpoint `POST /webhooks/google-drive` — trigger로만 사용, 실 변경은 `changes.list`
- worker (`app/workers/`): sync job 소비, 재시작 후 token 이어받기, 멱등 재처리
- sync event audit: `drive_sync_events` 기록 + `GET /admin/drive-sync-events`
- pending candidate **stale 훅**: fingerprint 변경 시 pending candidate를 stale 전환하는 service 훅 자리 (재분석 enqueue 배선은 WORK-004)
- admin API/화면: `GET /admin/drive-connector`, `POST /admin/drive-connector/watch`, `POST /admin/drive-connector/sync/retry` + FE connector 화면(상태/감시 폴더/watch 만료/마지막 sync/재시도)
- 문서 record 조회 최소 표면: `GET /documents/{id}`(mirror+state), `GET /admin/documents`(상태별 감사 목록), `GET /documents/{id}/drive-mirror` — 승인 metadata 표시·RBAC 필터 완성은 WORK-005/006

제외:

- AI classification job 생성/제출 → WORK-004 (이 WP는 훅 인터페이스만 노출)
- metadata candidate 생성/승인 → WORK-004/005
- 문서 탐색 화면·RBAC 목록 필터 → WORK-006
- 기존 파일 backfill, Workspace Events API + Pub/Sub (SPEC-004 Out of scope)

## Code Surface

- Repo / module: `gcs_demo`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `backend/app/integrations/google_drive/` | OAuth client, changes.list/watch wrapper (Drive 호출은 여기만) |
| `backend/app/api/routers/documents.py` · `drive_connector.py` · `webhooks.py` | 문서 조회, connector admin, webhook 수신 |
| `backend/app/services/drive_sync.py` · `services/documents.py` | 변경 적용, upsert orchestration, soft delete 전이, stale 훅 |
| `backend/app/repos/documents.py` · `repos/drive_sync.py` | mirror upsert, sync state/event DB access |
| `backend/app/workers/main.py` · `workers/drive_sync.py` | sync 소비, watch 갱신 job, 이어받기 |
| `backend/app/core/config.py` | `GOOGLE_DRIVE_*` env 5종 typed settings |
| `frontend/app/admin/connector/page.tsx` (신규) | connector 상태/sync activity 화면 — 스캐폴딩에 없어 신규 추가 |
| `frontend/lib/api/` | connector/sync 계약 client |

- Domain / schema note: 테이블은 WORK-001 migration 완료 전제(`documents`, `drive_sync_state`, `drive_sync_events`). Drive 원문/본문 컬럼 금지 (DEC-019). SQLAlchemy stmt는 repo 전용 (ARCH-001 §4).

## Domain / Schema

| Entity | 역할 |
|---|---|
| `documents` | mirror 필드 갱신 본체. `(source_provider, drive_file_id)` 멱등 upsert |
| `drive_sync_state` | 단일 row: page token, watch channel, 마지막 sync/오류 |
| `drive_sync_events` | audit: `webhook_received`~`sync_failed` 7종 event_type |
| `metadata_candidates` | stale 전환만 이 WP 훅에서 touch (생성은 WORK-004) |

- 상태 / invariant: document state machine은 SPEC-003 §State/Lifecycle이 SSOT. 같은 change 중복 처리 시 최종 상태 동일(멱등)
- Migration 필요 여부: 없음. 필요 시 컬럼 보강만
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: webhook 검증 방식 확정 결과 (SPEC-004는 "구현 work에서 구체화"로 위임)

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-004 | `on_document_upserted(document_id, fingerprint)` / `on_fingerprint_changed(...)` 훅 | classification/재분석 job enqueue 지점 |
| WORK-005 | 최신 `drive_fingerprint`·`drive_state` 조회 | 승인 시 fingerprint 재검사, blocked 판정 |
| WORK-006 | `documents` mirror + state 필터 repo | 일반 사용자 숨김 상태 처리 |

## Internal Interface Contract

- `services/drive_sync.apply_change(change) -> SyncOutcome(upserted|unavailable|skipped)` — webhook/수동 retry/재시작 이어받기가 모두 이 단일 진입을 사용 (멱등 보장 지점)
- stale 훅: `services/documents.mark_candidates_stale(document_id, new_fingerprint)` — WORK-004가 이 훅 뒤에 재분석 enqueue를 연결

## Execution

### Phase 1 — documents mirror 멱등 upsert + fingerprint

- **Status**: DONE
- **설명**: Drive SoT ↔ DB mirror의 핵심 불변식(멱등 upsert, mirror/approved 분리, fingerprint)을 먼저 굳힌다.
- **작업**:
  - [x] mirror upsert repo/service — mirror 필드만 갱신, 승인 필드 불가침
  - [x] composite fingerprint 조립/비교 유틸 (필수 4요소 + content_fingerprint 옵션)
  - [x] `drive_state` 전이 (active↔trashed/out_of_scope, removed) + 일반 조회 숨김 조건
- **검증**:
  - [x] 같은 change 2회 적용 → row 1개, 최종 상태 동일 (SPEC-004 AC 멱등)
  - [x] fingerprint 구성요소 누락 시 저장 거부, `mime_type`=`drive_mime_type` 일치
  - [x] soft delete가 hard delete 없이 상태 전환만 수행
- **완료 증거**: `repos/documents.py`(upsert_mirror 멱등·mirror만 갱신·set_drive_state), `services/documents.py`(build_fingerprint 필수 4요소, mark_candidates_stale/blocked), `repos/candidates.py`. pytest로 멱등 2회 적용·구성요소 누락 거부·soft delete만 검증

### Phase 2 — Drive integration + webhook/changes.list + 이어받기

- **Status**: DONE
- **설명**: SPEC-004 수집 파이프. notification은 trigger, 원장은 `changes.list`.
- **작업**:
  - [x] Drive OAuth env client (`drive.readonly`), 선택 폴더 하위 필터, 폴더 밖 `out_of_scope`/제외 처리
  - [x] `POST /webhooks/google-drive` 수신 → sync enqueue (검증: channel id/token 확인 — 방식 확정은 이 Phase)
  - [x] `changes.list` + page token 저장, 재시작 후 이어받기, watch channel 생성/갱신 job
- **검증**:
  - [x] 선택 폴더에 새 파일 → document row 생성, 폴더 밖 파일 → 미수집/`out_of_scope`
  - [x] worker 재시작 후 저장 token부터 이어받아 누락 없음 (SPEC-004 S-5)
  - [x] watch 만료 임박 시 갱신 job 동작 (만료 시각 조작 test)
- **완료 증거**: `integrations/google_drive/client.py`(httpx, token refresh 캐시, changes/files/watch — MockTransport 테스트 8), `services/drive_sync.py`(apply_change 멱등, 폴더 조상 walk, 상태 전이+복구, token 이어받기, watch 등록/갱신), `api/routers/webhooks.py`(channel id+HMAC token 검증, 불일치 무시 204). 실 Drive 연동 검증 완료(2026-07-09 — 하단 실연동 검증 노트)

### Phase 3 — sync event audit + stale 훅 + admin retry

- **Status**: DONE
- **설명**: 관리자 감사 가시성과 후속 WP(AI 재분석) 연결 지점을 만든다.
- **작업**:
  - [x] `drive_sync_events` 기록 (7종 event_type, 원문/secret 금지) + `GET /admin/drive-sync-events`
  - [x] fingerprint 변경 시 `mark_candidates_stale` 훅 호출 배선 (`candidate_staled` event 기록, 재분석 enqueue는 WORK-004 TODO 주석)
  - [x] `POST /admin/drive-connector/sync/retry` — 실패 sync 재처리(멱등)
- **검증**:
  - [x] 수집/삭제/실패 각 시나리오에서 대응 event row 생성
  - [x] 파일 수정 → pending candidate가 있으면 stale 전환 (fixture candidate로 검증)
- **완료 증거**: `repos/drive_sync.py`(state 단일 row/events append), fingerprint 변경→candidate stale+event+reason, WORK-004 hook은 no-op TODO. admin API 4종(`drive_connector.py`) + documents API 3종. pytest 97 passed(신규 44)

### Phase 4 — FE admin connector 화면

- **Status**: DONE
- **설명**: SPEC-004 U-1~U-3. connector가 지금 변경을 받을 수 있는지 admin이 한 화면에서 본다. `21-html/page-admin-settings.html` 시안 기준 (Drive 연동/Sync Activity/수집 결과 섹션).
- **작업**:
  - [x] `app/admin/connector`(신규): 상태 배지(연결됨/설정 필요/갱신 필요/오류), scope·감시 폴더·watch 만료 표시, `상태 새로고침`/`watch 갱신` CTA
  - [x] sync activity: 마지막 동기화/변경 토큰/처리 수, 실패 시 `다시 처리` CTA
  - [x] 문서 intake 결과 표시 (새 문서/갱신/숨김 처리 — sync events 기반)
- **검증**:
  - [x] `tsc --noEmit`·`npm run build` 통과
  - [x] env 미설정 상태에서 `DRIVE_CONNECTOR_NOT_CONFIGURED` 안내 표시
- **완료 증거**: `app/admin/connector/page.tsx`(상태 배지/CTA/Sync Activity/수집 결과/이벤트 목록, admin guard), `lib/api/driveConnector.ts`, catalog NAV에 Drive 연동 링크. tsc·build 통과. 실제 파일 투입 시나리오 검증 완료(2026-07-09) — 목표 시나리오: *Drive 선택 폴더에 파일을 넣으면 admin connector 화면에서 새 문서 등록과 sync event를 확인하고, 파일을 휴지통에 넣으면 문서 상태가 `휴지통`으로 바뀌는 것을 확인한다*


> **실연동 검증 완료 (2026-07-09)**: 실제 Drive 폴더(gcd_sync) 연동 — OAuth(drive.readonly)·startPageToken 확보·60s 폴링 수집(단건 + 44건 일괄 무손실), soft delete/fingerprint/stale 훅, connector 화면 실동작 확인. webhook 실검증만 잔여(공개 URL 필요 — 폴링으로 대체 운용).

## Pre-deploy Check

- [ ] `GOOGLE_DRIVE_*` env 5종이 secret flow로만 주입, 값이 log/문서에 안 남음
- [ ] webhook endpoint가 Drive notification 외 요청을 처리하지 않음
- [ ] Drive 원문/본문이 DB 어떤 컬럼에도 저장되지 않음 (audit message 포함)
- [ ] scope가 `drive.readonly`로 제한됨

## Rollback

- worker 중지 + webhook 라우터 미등록으로 수집 중단 가능 (기존 데이터 영향 없음)
- 문서 상태는 soft delete 구조라 데이터 파괴적 rollback 없음. 잘못 수집된 row는 `out_of_scope` 전환으로 숨김

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] SPEC-003 mirror/state/fingerprint AC + SPEC-004 AC가 Phase 검증에 반영됐다 (candidate 관련 AC는 WORK-004/005에서 최종 닫힘).
- [ ] 필요한 테스트/검증이 끝났다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- webhook 검증 방식(Goog-Channel-Id/Token header 검증 수준) — SPEC-004가 구현 work로 위임. Phase 2에서 확정하고 spec 환류
- 로컬 개발에서 공개 HTTPS webhook 대안: tunnel vs 수동 sync trigger(관리자 retry API) — 착수 시 결정
- 본문 읽기(export/content read)와 `content_fingerprint` 생성 시점: 분석 텍스트 추출은 WORK-004 input 조립과 경계 조정 필요 (원문 장기 저장 금지 공통)

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Work: (frontmatter `links.works` 참조)
- Architecture: ARCH-001 §9 Async Job Boundary, ARCH-003 §6 Drive Sync 테이블
