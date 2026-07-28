---
type: work
id: KDEV-WORK-014
title: "승인 큐 + route 게이트 MVP"
status: todo
product: kknaks-dev
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
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
  specs:
    - "[[spec-007-approval-queue|KDEV-SPEC-007]]"
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
    - "[[spec-009-gate-feedback|KDEV-SPEC-009]]"
  works:
    - "[[work-012-slack-bridge-absorb|KDEV-WORK-012]]"
    - "[[work-013-concept-layer|KDEV-WORK-013]]"
  releases: []
  related: []
---

# 승인 큐 + route 게이트 MVP

Slack 입력을 **파일이 아니라 DB 큐**로 받고, 자동 준비(수집·요약)를 거쳐 **첫 게이트(route)까지** 동작시킨다. 승인하면 목적지가 확정되고 체인 길이가 정해진다.

> 만들지 않는 것: `source_note`·`concept`·`derived` 게이트와 실제 발행. 이 work의 끝은 **route 승인까지**이며, 발행은 WORK-015다. 즉 이 단계에서는 아직 md가 만들어지지 않는다.

## Meta

- Baseline: KDEV-BL-003
- Covers spec: KDEV-SPEC-007(전부) · KDEV-SPEC-008(route까지) · KDEV-SPEC-009(게이트 공통 계약)
- Depends on work: WORK-012(sink 교체 지점), WORK-013(목적지가 실재해야 route가 의미를 가짐)
- Parallel work: 없음
- Follow-up work: WORK-015
- External dependency: open-kknaks(요약·목적지 제안), yt-dlp·youtube-transcript-api(수집)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | — |
| Blocker | WORK-012·013 선행 |
| Next | Phase 1 스키마 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위·상태기계 확정 | todo |
| Design | kknaks | 큐 화면·게이트 카드 레이아웃 | todo |
| FE | kknaks | admin 큐 화면 | todo |
| BE | kknaks | 스키마·접수·준비·게이트 | todo |
| QA | kknaks | 상태 전이·실패 회생 검증 | todo |
| Ops | kknaks | 마이그레이션 적용 | todo |

## Scope

포함:

- Alembic 리비전 2개 — 큐/준비/실행, 게이트/버전/피드백
- Slack·수동 접수 → `queue_items` 적재 (WORK-012의 sink 교체)
- 자동 준비 스테이지: 수집 + 요약, 실패 시 메모 보완 재시도
- route 게이트 생성·승인·피드백/재생성
- 게이트 공통 계약 구현 (v1 보존 + v2, 세션 resume, 형제 sweep)
- admin 큐 화면 (목록·상세·항목 추가·게이트 카드)

제외:

- `source_note`·`concept`·`derived` 게이트 (WORK-015)
- Apply Executor·발행 (WORK-015)
- 커밋·블로그·스케줄 파이프라인
- 기존 스케줄 잡의 큐 편입

## Code Surface

- Repo / module: `app/back`, `app/front`

| 경로 후보 | 설명 |
|---|---|
| `app/back/alembic/versions/0002_*` | `queue_items`·`item_preparations`·`ai_tasks` |
| `app/back/alembic/versions/0003_*` | `gates`·`gate_revisions`·`gate_feedbacks` |
| `app/back/core/models.py` | ORM 모델 추가 |
| `app/back/api/routers/queue.py` | 큐 API (admin 게이트) |
| `app/back/service/pipeline/` | 파이프라인 정의·스테이지 러너·게이트 서비스 |
| `app/back/service/slack_bridge/runner.py` | sink를 큐 적재로 교체 |
| `app/back/service/jobs/content_enrich.py` | 수집·요약 로직 재사용 (추출) |
| `app/front/app/admin/queue/` | 큐 화면 |
| `app/front/components/admin/` | 게이트 카드·피드백 모달 |

- Domain / schema note: **마이그레이션 2건 필요.** 테이블 구조는 `40-architecture/database/README.md` ERD 참조.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `queue_items` | 입력 접수와 항목 lifecycle |
| `item_preparations` | 자동 준비 산출물 버전 (박제) |
| `ai_tasks` | AI 실행 이력 (실패·재시도 포함) |
| `gates` | 스테이지별 게이트 컨테이너 |
| `gate_revisions` | AI 제안 버전 |
| `gate_feedbacks` | 재생성을 유발한 지시 |

- 상태 / invariant: 게이트당 승인 버전 1개(partial unique) · 게이트당 검토 가능 버전 1개(앱 sweep) · 이력 테이블 불변
- Migration 필요 여부: 필요 (0002·0003)
- SPEC에 환류해야 하는 변경: 상태값이 실제 구현에서 달라지면 SPEC-007/008로 환류

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-015 | `gates` 체인·승인 이벤트 | 뒤 스테이지 게이트가 같은 구조를 재사용한다 |
| WORK-015 | route 승인 결과(목적지·group·파생 on/off) | 체인 길이와 산출물 결정 입력 |

## Internal Interface Contract

파이프라인 정의는 **데이터**로 표현한다(SPEC-008). 이 work에서 유튜브 정의를 등록하되, 저장 위치(코드 상수 vs DB)는 여기서 결정한다.

route 승인 결과의 형태를 고정한다 — WORK-015가 이것만 보고 체인을 만든다.

```text
route_result = {
  destinations: { reference: {enabled, group}, concept: {enabled}, derived: {enabled} },
  exclusive: null | "inbox_hold" | "discard"
}
```

## Execution

### Phase 1 — 스키마

- **Status**: TODO
- **작업**:
  - [ ] Alembic 0002 (`queue_items`·`item_preparations`·`ai_tasks`)
  - [ ] Alembic 0003 (`gates`·`gate_revisions`·`gate_feedbacks`)
  - [ ] ORM 모델 + 제약(승인 버전 partial unique, CHECK 상태값)
- **검증**:
  - [ ] upgrade/downgrade 왕복 성공
  - [ ] 같은 게이트에 승인 버전 2개를 넣으면 제약 위반이 난다
- **완료 증거**: 미작성

### Phase 2 — 접수와 자동 준비

- **Status**: TODO
- **작업**:
  - [ ] WORK-012의 sink를 **큐 적재**로 교체 (파일 쓰기·push 제거)
  - [ ] 수동 접수 API + 중복 판정(정규화 URL)
  - [ ] 자동 준비 스테이지: 수집(yt-dlp·자막) + 요약
  - [ ] 준비 실패 시 `prepare_failed` + 메모 보완 재시도 경로
  - [ ] Slack 회신을 "접수됨 / 검토 대기"로 변경
- **검증**:
  - [ ] Slack에 링크를 던지면 **레포에 파일이 생기지 않고** 큐에 적재된다
  - [ ] 준비 완료 후 `in_review`로 전이한다
  - [ ] 자막이 없는 영상에서 `prepare_failed` → 메모 추가 → 재시도로 `in_review` 도달
  - [ ] 재시도가 기존 실패 기록을 덮어쓰지 않는다
  - [ ] 발행 전 같은 URL 재투입 시 기존 항목에 합류한다
- **완료 증거**: 미작성

### Phase 3 — route 게이트 + 공통 계약

- **Status**: TODO
- **작업**:
  - [ ] 파이프라인 정의 등록(유튜브) + 저장 위치 결정
  - [ ] route 게이트 생성 + 목적지 제안 AI 호출
  - [ ] 승인 → 목적지 확정 + 체인 길이 확정(뒤 스테이지 게이트 생성은 WORK-015)
  - [ ] 피드백 → v2 재생성 (세션 resume, v1 read-only 보존)
  - [ ] 형제 검토가능 버전 sweep
  - [ ] 실패 → `재시도`(새 실행 행)
- **검증**:
  - [ ] 준비 완료 시 route 게이트가 자동 생성된다
  - [ ] 피드백 후 v2가 생기고 v1이 read-only로 남는다
  - [ ] 재생성을 연속 2회 트리거해도 검토 가능 버전이 1개만 남는다
  - [ ] 세션 resume이 동작한다 (원문 재전송 없이 반영)
  - [ ] 세션이 없을 때 stateless로 재생성되며 실패하지 않는다
  - [ ] 승인된 게이트에 피드백하면 거부된다
  - [ ] `폐기` 승인 시 항목이 `discarded`가 되고 파일이 생기지 않는다
- **완료 증거**: 미작성

### Phase 4 — admin 큐 화면

- **Status**: TODO
- **작업**:
  - [ ] 사이드바에 큐 항목 추가 (현재 `ready: false` 상태)
  - [ ] 큐 목록(상태별 묶음, 실패 강조) + 항목 상세
  - [ ] 항목 추가 모달 (URL + 메모)
  - [ ] 게이트 카드 (`피드백`·`승인` 2버튼) + 피드백 모달
  - [ ] route 게이트의 목적지 토글 UI
- **검증**:
  - [ ] 비인증 접근이 차단된다
  - [ ] `publish_failed`·`prepare_failed`가 목록에서 눈에 띈다
  - [ ] 게이트 카드에 인라인 입력창이 없고 두 버튼만 있다
  - [ ] 승인된 게이트가 접히고 현재 검토 대상만 펼쳐진다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 마이그레이션이 기존 `users` 테이블에 영향을 주지 않음
- [ ] sink 교체 후 **기존 캡처 경로로 파일이 더 이상 생기지 않음**을 확인 — 이 시점부터 Slack 캡처는 큐를 거친다
- [ ] 승인 전 초안이 레포에 노출되지 않음
- [ ] 큐 API가 admin 인증 뒤에 있음

## Rollback

- sink를 WORK-012의 파일 sink로 되돌리면 캡처가 이전 동작(즉시 커밋)으로 복귀한다.
- Alembic downgrade로 0003 → 0002 → 0001 복귀. `users`는 영향 없음.
- 큐 화면은 라우트 미등록으로 숨긴다.

## Done Criteria

- [ ] 모든 Phase가 `DONE`이다.
- [ ] Slack 입력이 큐에 쌓이고 route 승인까지 동작한다.
- [ ] 승인 전에는 레포에 파일이 생기지 않는다.
- [ ] 피드백 → v2 재생성이 동작하고 v1이 보존된다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 파이프라인 정의 저장 위치(코드 상수 vs DB) — 이 work에서 결정한다(SPEC-008 §7).
- `normalized_url` 정규화 범위 — 중복 판정 정확도에 직결한다(database README Open).
- **이 work가 끝나면 큐에 항목이 쌓이지만 발행은 안 된다.** WORK-015까지 가야 md가 나온다. 그 사이 기간에 캡처를 계속 쓸지, WORK-015까지 묶어서 배포할지 판단이 필요하다.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 선행 WORK-012·013, 후속 WORK-015
