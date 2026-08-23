---
type: work
id: CFO-WORK-004
title: "AI 분류 파이프라인"
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
    - "[[spec-007-ai-classification-pipeline]]"
  works:
    - "[[work-002-organization-tree-catalog]]"
    - "[[work-003-document-record-drive-sync]]"
  releases: []
  related: []
---

# AI 분류 파이프라인

Drive 변경 → `ai_queue_jobs` 원장 → open-kknaks submit(AgentClient) → 결과 schema/fingerprint 검증 → 노드 id resolve → metadata/relation candidate 저장까지의 백그라운드 파이프라인과 ai_worker workspace 프롬프트/가이드를 완성한다. 승인 게이트 UI는 만들지 않는다(WORK-005).

> 1 파일 = 1 work = **빌드 계획**. SPEC 본문은 복제하지 않고 ID/링크로 참조한다. Status Board / Spec Coverage는 `30-work/README.md`가 담당한다.

## Meta

- Baseline: BASE-001, BASE-002 (spec 경유)
- Covers spec: SPEC-007 (AI Classification Pipeline)
- Depends on work: WORK-003 (upsert/fingerprint 훅, 분석 대상 문서), WORK-002 (조직/트리/카탈로그 — input context 조립과 노드 id resolve)
- Parallel work: 없음 (기본 체인)
- Follow-up work: WORK-005 (candidate 승인), WORK-006 (승인 결과 탐색)
- External dependency: open-kknaks Redis broker + ClaudeWorker 실행 환경 (`ai_worker/`), claude CLI credential (worker 측에만 — LLM 실행은 open-kknaks 경유, Anthropic SDK 직접 import 금지). broker namespace/queue는 backend submit env와 ai_worker가 동일 값 공유 (ARCH-001 §10)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker |  |
| Next | WORK-005 착수. open-kknaks 실 실행 검증은 env·claude-tools 투입 후 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | SPEC-007 계약 범위 고정 | done |
| Design | kknaks | 분석 상태 문구 (SPEC-007 U-1/U-2) | done |
| FE | kknaks | 문서별 분석 이력/상태 최소 표시 | done |
| BE | kknaks | job 원장, submit, 검증/resolve/저장 | done |
| QA | kknaks | 멱등/stale/실패 경로 검증 | done |
| Ops | kknaks | `OPEN_KKNAKS_*` env, ai_worker 이미지 | done |

## Scope

포함:

- `ai_queue_jobs` 원장 service/repo: 상태 전이(ARCH-002 state machine), `job_type+document_id+fingerprint+idempotency_key` unique 멱등 enqueue, `attempt_count`/`next_run_at` retry, Redis는 dispatch 전용
- WORK-003 훅 배선: document upsert → `classification` job, fingerprint 변경(stale) → `stale_reanalysis` job 자동 enqueue (DEC-022). `trashed`/`removed`/`out_of_scope` 문서는 자동 재분석 제외
- open-kknaks submit: `app/integrations/open_kknaks/` AgentClient(Redis broker), env 계약(`OPEN_KKNAKS_BROKER_URL`/`PROVIDER`/`MODEL`/`QUEUE`/`TIMEOUT_SEC`), `external_task_id` 저장
- classification input 조립: Drive mirror + `analysis_text`(최소 범위, 장기 저장 금지) + organization/document_tree/document_type/policy/relation_type context. 본문 못 읽으면 `read_capability=metadata_only`
- 결과 처리: valid JSON schema 검증 → fingerprint freshness 검증(다르면 candidate 미저장 + `stale` 종료 + 새 job enqueue) → `owning_department`/`read_policy.department`/`physical_tree_path` 노드 id resolve(실패 값은 admin 보정 대상 표시) → `metadata_candidates` `pending` 저장(문서당 pending 1개, `(document_id, candidate_fingerprint)` 멱등) + `relation_candidates` 저장(target 못 찾으면 `unresolved`)
- 실패 처리: failed/timeout/validation_failed 기록(`CLASSIFICATION_*` error code), 기존 approved metadata 불변
- admin API: `POST /admin/documents/{id}/classify`, `GET /admin/classification-jobs/{id}`, `GET /admin/documents/{id}/classification-jobs` + FE 문서별 분석 이력 최소 표시(상태 문구 — 승인 게이트 통합 표시는 WORK-005)
- ai_worker workspace 완성: `ai_worker/workspace/CLAUDE.md`·`agent.md` 진입 문서 + 루트 `context/classification-guide.md`(출력 JSON schema, 분류 규칙, 민감 preset 판단 가이드 — `context/policy.md` preset 기준) → 이미지 빌드/실행 검증

제외:

- 승인/거절/수정 게이트 BE·FE → WORK-005
- reanalysis_status 파생 표시 UI → WORK-005 (job 상태 조회 API는 이 WP가 제공)
- open-kknaks 자체 구현/runner 내부 (SPEC-007 Out of scope)

## Code Surface

- Repo / module: `gcs_demo`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `backend/app/services/ai_jobs.py` · `services/classification.py` | job 원장 전이, input 조립, 결과 검증/resolve/저장 |
| `backend/app/repos/ai_jobs.py` · `repos/candidates.py` · `repos/relation_candidates.py` | job/candidate DB access |
| `backend/app/integrations/open_kknaks/` | AgentClient submit/result (open-kknaks 호출은 여기만) |
| `backend/app/workers/ai_dispatch.py` | queued job 소비, submit, 결과 polling/수신 |
| `backend/app/api/routers/classification.py` | admin classify/조회 3종 |
| `backend/app/core/config.py` | `OPEN_KKNAKS_*` typed settings |
| `ai_worker/run.py` · `ai_worker/Dockerfile` | ClaudeWorker 기동 (스캐폴딩 보강) |
| `ai_worker/workspace/CLAUDE.md` · `agent.md` | claude 진입 문서 |
| `context/classification-guide.md` | 출력 schema/분류 규칙 (빌드 시 workspace/context로 COPY) |
| `frontend/components/approval/` · `lib/api/` | 분석 상태 표시 컴포넌트/클라이언트 (최소) |

- Domain / schema note: `ai_queue_jobs`·`metadata_candidates`·`relation_candidates` 테이블은 WORK-001 migration 완료 전제. task payload에 Drive/DB secret·OAuth token 포함 금지. SQLAlchemy stmt는 repo 전용.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `ai_queue_jobs` | AI job 상태 SoT (queued→…→candidate_saved/stale terminal). FE 폴링 기준 |
| `metadata_candidates` | 결과 저장 대상. `pending` 생성, 문서당 pending 1개 |
| `relation_candidates` | wikilink 후보. target resolve 실패 시 `unresolved` |

- 상태 / invariant: job state machine SSOT는 ARCH-002 §5 (SPEC-007 lifecycle + queued→stale 보강). worker는 submit 전/저장 전 fingerprint 이중 검사
- Migration 필요 여부: 없음. 필요 시 컬럼 보강만
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: open-kknaks 바인딩 세부(namespace/queue 실값), classification output schema 확정본 → 40-architecture/spec 환류

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-005 | `metadata_candidates`/`relation_candidates` row + job 상태 조회 API | 승인 게이트 큐/상세와 reanalysis_status 파생 계산 |
| WORK-005 | `services/ai_jobs.enqueue_reanalysis(document_id)` | 수동 재분석 CTA(`POST /admin/approval-candidates/{id}/reanalyze` 위임) |

## Internal Interface Contract

- `enqueue_classification(document_id, fingerprint, *, requested_by=None) -> AiJob` — 멱등(동일 fingerprint 재호출 시 기존 job 반환)
- classification output JSON schema는 `context/classification-guide.md`와 backend validator가 **동일 schema 정의를 공유**한다 (드리프트 금지 — schema 파일 단일 원천으로 관리)

## Execution

### Phase 1 — ai_queue_jobs 원장 + enqueue 배선

- **Status**: DONE
- **설명**: 관찰 가능/재시도 가능한 job 원장을 먼저 세우고 WORK-003 훅에 연결한다.
- **작업**:
  - [x] job 생성/전이 service·repo (unique 멱등, retry 필드, terminal 규칙)
  - [x] WORK-003 `on_document_upserted`/`mark_candidates_stale` 뒤에 classification/stale_reanalysis enqueue 배선
  - [x] unavailable 문서(trashed/removed/out_of_scope) 자동 재분석 제외
- **검증**:
  - [x] 같은 `document_id+fingerprint` 중복 enqueue 시 row 1개 (ARCH-002 AC)
  - [x] Redis 죽어도 DB row로 상태/재시도 추적 가능
- **완료 증거**: `repos/ai_jobs.py`·`services/ai_jobs.py` — 멱등 enqueue(job_type+doc+fingerprint+key unique), ARCH-002 §5 전이표 강제, retry 게이트(attempt/max/next_run_at). drive_sync 훅 배선(upsert→classification, fingerprint 변경→stale_reanalysis+event)

### Phase 2 — open-kknaks submit + input 조립

- **Status**: DONE
- **설명**: SPEC-007 Task Submit Contract대로 제출하고, AI에는 제한된 context만 넘긴다.
- **작업**:
  - [x] AgentClient(Redis broker) submit — provider/model/queue/timeout env, `external_task_id` 저장
  - [x] classification input 조립: mirror + analysis_text(최소) + org/tree/catalog/policy/relation_type context, `metadata_only` 분기
  - [x] worker 소비 loop: queued → submit 전 fingerprint 검사(다르면 `stale` 종료+재enqueue) → running
- **검증**:
  - [x] payload에 Drive/DB secret·OAuth token 미포함 (SPEC-007 AC)
  - [x] `OPEN_KKNAKS_*` 미설정 시 `OPEN_KKNAKS_NOT_CONFIGURED` 처리
  - [x] metadata_only 문서는 파일명/MIME/수정시각만 전달
- **완료 증거**: `integrations/open_kknaks/client.py`(Protocol+실 client lazy import, env 검증), pyproject에 open-kknaks==2.0.2. `workers/ai_jobs.py` — queued pick→fingerprint 재검사→submit(external_task_id)→result 대기. Input 조립(`services/classification.py`) — secret/web url 미포함, policy_context/카탈로그/relation 4종 포함. 실 broker 왕복 검증 완료(2026-07-09 — 45건 배치)

### Phase 3 — 결과 검증 + 노드 id resolve + candidate 저장

- **Status**: DONE
- **설명**: AI output은 후보일 뿐 — 검증 통과분만 pending candidate로 내려간다.
- **작업**:
  - [x] JSON schema 검증 (`CLASSIFICATION_RESULT_INVALID` → validation_failed → 자동 재분석 queued 복귀)
  - [x] 저장 시점 fingerprint freshness 검증 (`stale` 종료 + 최신 기준 새 job)
  - [x] `owning_department`/`read_policy.department`/`physical_tree_path` 노드 id resolve, 실패 값 admin 보정 표시 플래그
  - [x] `metadata_candidates` pending 저장(멱등) + `relation_candidates` 저장(unresolved 포함), `candidate_id` 역참조
  - [x] failed/timeout 기록, 기존 approved metadata 불변 보장
- **검증**:
  - [x] invalid JSON → candidate 미저장 (SPEC-007 AC)
  - [x] 저장 직전 fingerprint 변경 시 candidate 미저장 + 새 job (ARCH-002 AC)
  - [x] target 없는 wikilink → `unresolved` relation candidate, 새 document row 미생성 (DEC-021)
- **완료 증거**: `ClassificationOutput` pydantic(extra forbid) 단일 validator, fingerprint 재검증→stale+새 job, 이름→노드 id resolve(실패는 unresolved_fields+needs_admin_fix, 신규 문서종류 플래그), pending 1개 규칙(같은 fp 갱신/다른 fp supersede), relation unresolved 저장(자동 문서 생성 없음). Case Matrix 에러 경로 전부 테스트

### Phase 4 — ai_worker workspace 프롬프트/가이드 완성

- **Status**: DONE
- **설명**: claude가 workspace 진입 문서를 스스로 읽고 분류 task를 수행하도록 실행 컨텍스트를 이미지에 고정한다 (ARCH-001 §10).
- **작업**:
  - [x] `classification-guide.md`: 출력 JSON schema(backend validator와 단일 원천), 분류/귀속/권한/민감 preset 판단 규칙, wikilink relation 표기 규칙
  - [x] `CLAUDE.md`/`agent.md` 진입 경로 정리, 이미지 빌드(`docker compose build ai-worker`) 반영 확인
  - [x] ClaudeWorker가 backend submit과 동일 broker namespace/queue 소비 확인
- **검증**:
  - [x] 샘플 문서 task로 유효한 output JSON 회신 (schema pass)
  - [x] 가이드 변경 → rebuild로만 반영됨(런타임 마운트 의존 없음)
- **완료 증거**: `context/classification-guide.md` Input/Output 표 전면 보강(backend 모델과 동기, 드리프트 금지 규칙 명시), `ai_worker/workspace/agent.md` 출력 규칙 보강, `docker compose build ai-worker`로 이미지 반영 확인. 실 task 실행 검증 완료(2026-07-09 — 로컬 claude, workspace 자산은 복사 방식)

### Phase 5 — admin 상태 API + 최소 FE 표시

- **Status**: DONE
- **설명**: FE는 Redis가 아니라 DB job 상태를 API 폴링한다 (ARCH-002 §6).
- **작업**:
  - [x] classify/조회 API 3종 (응답 최소 필드: id, job_type, status, document_id, candidate_id, fingerprint, attempt_count, last_error_code)
  - [x] FE 문서별 분석 이력/상태 문구 표시 (`AI 분석 대기 중`~`Drive 변경으로 다시 분석 중`)
- **검증**:
  - [x] 수동 classify → job 생성 → 폴링으로 상태 변화 표시
  - [x] `tsc --noEmit`·`npm run build` 통과
- **완료 증거**: `api/routers/classification.py` 3종(require_admin_only, 202 멱등), `lib/api/classification.ts`+`components/approval/classification-status.tsx`(U-1 문구, 10s 폴링, 재분석 CTA — connector 화면 장착). pytest 134 passed(신규 37)·tsc/build 통과 — 목표 시나리오: *Drive에 파일을 넣으면 job이 queued→running→candidate_saved로 흐르고, admin 화면에서 문서별 분석 이력과 pending candidate 생성을 확인한다*


> **실행 검증 완료 (2026-07-09)**: open-kknaks(Redis)+로컬 네이티브 claude로 45건 배치 분류 — 후보 45/45 생성(자동 재큐·stale 체인 전량 회수), 승인→documents 반영 확인. 발견 이슈 반영: ①재시도 소진 시 수동 재분석 409 버그 수정(신규 manual job 허용), ②fingerprint version 비교 제외(Drive churn), ③workspace 자산 symlink 금지(claude 샌드박스 — 복사 방식, README 문서화), ④FE 분석 패널 전체 표시(limit 200). AI job 소비는 순차 1건 처리로 확정(사용자 결정). 잔여 백로그: 분석 패널 N+1 → 문서 수백 건 이상 시 집계 API 필요.

## Pre-deploy Check

- [ ] `OPEN_KKNAKS_*` env 주입 확인, broker retention 운영 설정 제한
- [ ] task payload/log에 원문 전문·secret 미노출 (`payload_ref`/`result_ref`는 참조만)
- [ ] claude credential은 ai_worker 측에만 존재 (backend에 없음)
- [ ] AI worker 실패가 승인 metadata에 영향 없음 확인

## Rollback

- enqueue 배선 지점(훅 뒤 호출) 제거로 파이프라인 비활성화 — Drive sync는 계속 동작
- 저장된 job/candidate row는 원장 보존(삭제 안 함). 잘못된 candidate는 승인 게이트에서 거절 처리

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] SPEC-007 Acceptance Criteria + ARCH-002 AC가 Phase 검증에 반영됐다.
- [ ] 필요한 테스트/검증이 끝났다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 결과 수신 방식(worker polling vs AgentClient 결과 stream 수신) 세부 — open-kknaks client 실 바인딩 시 확정 (ax-knowledge-graph WP1의 Redis 직결 AgentClient 확정 경험 참고)
- `analysis_text` 추출(파일 타입별 reader/export) 범위: v1 지원 MIME 목록을 이 WP에서 확정하고 metadata_only 경계로 환류
- output schema의 `document_type`이 카탈로그에 없는 신규 후보일 때 표시 방식(SPEC-007 Validation "추가 필요한 후보로 표시") — candidate_metadata 내 플래그로 구현 예정, WORK-005 form과 계약 맞춤

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Work: (frontmatter `links.works` 참조)
- Architecture: ARCH-001 §9~10, ARCH-002 (job 원장 SSOT)
