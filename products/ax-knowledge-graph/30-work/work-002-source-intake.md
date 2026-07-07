---
type: work
id: AXKG-WORK-002
title: "WP1: Source Intake — 수신·수집·요약"
status: todo
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
progress: 0
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works:
    - "[[work-001-mvp-pipeline-scaffold|AXKG-WORK-001]]"
  releases: []
  related: []
---

# WP1: Source Intake — 수신·수집·요약

URL이 들어와서(`Slack`/`manual`) 자동으로 원문이 수집·요약되어 `summarized`가 되기까지를 구현한다. WP0의 AI 실행 골격 위에 요약 스테이지(①)를 첫 실사용 스테이지로 배선한다.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-003(Source Inbox), AXKG-SPEC-012(Collection Adapter), AXKG-SPEC-011①(요약 스테이지)
- Depends on work: AXKG-WORK-001(WP0 — 실행 골격·auth·마이그레이션)
- Parallel work: AXKG-WORK-003(WP2)과 병렬 가능
- Follow-up work: AXKG-WORK-004(WP3 — summarized 이후 게이트)
- External dependency: open-kknaks client 실 바인딩 확정(HTTP vs Redis broker AgentClient — WP0 잔여 TODO를 이 WP에서 확정), Slack app(signing secret)

## Scope

포함:

- sources 라우터/서비스/레포지토리: `/sources/manual`, `GET /sources`(status 필터), `GET /sources/{id}`, `queue-collection`(재시도), `GET /sources/{id}/ai-tasks`
- 중복 URL 처리: normalized_url 검사 → metadata.slack_events 누적/duplicate_candidate (SPEC-003 S-2)
- Slack intake: `POST /integrations/slack/sources` + signing secret 검증(토큰 인증 제외 경로)
- Source Collection Adapter (SPEC-012): type detection → youtube(metadata+transcript, description fallback) → static_web → dynamic_web(Playwright) fallback 체인, SourceMaterial 정규화, canonical_url로 normalized_url 갱신·중복 재검사, SSRF 가드
- 요약 스테이지(①): `source_summary` context builder 구현·등록, `received → summarizing → summarized/collection_failed` 자동 전이, summary_payload 저장, chunk 요약 병합, 재시도 배선
- open-kknaks client 실 바인딩 (fake → 실제)
- FE: Source Inbox 화면 — 큐 목록(상태별), 상세(요약 카드·실패 사유·`요약 재시도`), `Inbox에 넣기` 모달. **기준: `21-html/page-approval.html`의 Source Inbox 영역 — 레이아웃·한국어 카피 모두 시안을 따른다**

제외:

- 분류/문서화 게이트 (WP3)
- PDF/RSS adapter, page_kind=list 후속 UX (SPEC-012 OQ)
- 프롬프트 편집 UI (WP5)

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/api/routes/sources.py` · `integrations.py` | sources·Slack 라우터 |
| `apps/api/axkg/services/sources.py` · `repositories/sources.py` | source lifecycle 비즈니스/DB |
| `apps/api/axkg/integrations/source_collection/` | adapter 3종 + selection |
| `apps/api/axkg/integrations/slack.py` | 서명 검증·이벤트 파싱 |
| `apps/api/axkg/services/ai/` | source_summary builder 등록, client 실 바인딩 |
| `apps/web/app/(inbox)/` | Source Inbox 화면 |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `sources` | 전체 lifecycle 구현 (received→summarizing→summarized/collection_failed, ignored/deleted) |
| `ai_tasks` | `collect_source_summary` 실사용 (골격은 WP0) |

- 상태 / invariant: sources.status SSOT는 SPEC-003 상태도. 수집 실패 시 실패 ai_tasks 보존 + collection_failed.
- Migration 필요 여부: 없음(WP0에서 완료). 필요 시 컬럼 보강만.
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: open-kknaks 바인딩 확정 결과를 40-architecture에 반영.

## Execution

### Phase 1 — sources API + Inbox 화면

- **Status**: TODO
- **작업**:
  - [ ] sources 라우터/서비스/레포 (manual 입력, 목록/상세, 중복 처리)
  - [ ] FE Inbox 큐/상세/입력 모달 (SPEC-003 UX Contract)
- **검증**:
  - [ ] SPEC-003 U-1~U-3·S-2·S-3 AC 통과

### Phase 2 — Collection Adapter (SPEC-012)

- **Status**: TODO
- **작업**:
  - [ ] adapter selection + youtube(기존 profile 코드 참고: metadata+transcript, description fallback)
  - [ ] static_web → dynamic_web(Playwright) fallback, 공통 추출·후처리·수집 기준
  - [ ] SSRF 가드, canonical_url→normalized_url 갱신
- **검증**:
  - [ ] SPEC-012 AC 통과 (fixture 2종 포함)

### Phase 3 — 요약 스테이지 배선 (SPEC-011①)

- **Status**: TODO
- **작업**:
  - [ ] open-kknaks client 실 바인딩 확정·구현
  - [ ] source_summary context builder(SourceMaterial + AI 입력 지시 + context/ 문서) + 결과 저장(summary_payload)
  - [ ] received 자동 트리거, 상태 전이, 재시도, chunk 병합
- **검증**:
  - [ ] URL 입력 → summarized까지 end-to-end (라이브)

### Phase 4 — Slack intake

- **Status**: TODO
- **작업**:
  - [ ] `POST /integrations/slack/sources` + signing secret 검증
  - [ ] slack_events metadata 규약 (DB README)
- **검증**:
  - [ ] Slack 서명 검증 통과/실패 케이스, 중복 URL 누적

## Pre-deploy Check

- [ ] 외부 URL 수집 시 비공개 네트워크 접근 차단 (SSRF)
- [ ] transcript/page_text 전문이 application log에 남지 않음
- [ ] Slack 엔드포인트가 서명 검증 없이 열리지 않음

## Rollback

- 작업 레포 커밋 단위 revert. 문서 변경은 별도 커밋.

## Done Criteria

- [ ] 모든 Phase DONE/SUPERSEDED
- [ ] SPEC-003/012 AC + SPEC-011 요약 스테이지 AC 반영
- [ ] product `log.md`·`30-work/README.md` 갱신

## Open Issues

- open-kknaks 실 바인딩 방식(HTTP vs Redis broker AgentClient) — Phase 3 착수 시 확정.
- dynamic adapter 실행 위치(FastAPI 내 vs browser worker 분리) — SPEC-012 OQ.
