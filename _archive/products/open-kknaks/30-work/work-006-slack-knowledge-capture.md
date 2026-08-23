---
type: work
id: OKK-WORK-006
title: "Slack Thread 기반 inbox·reference 지식 수집"
status: in_progress
product: open-kknaks
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 90
created_at: 2026-07-02
updated_at: 2026-07-02
tags:
  - product/open-kknaks
  - doc/work
  - status/in-progress
links:
  baselines:
    - "[[OKK-BL-002-slack-idea-knowledge-graph|OKK-BL-002]]"
  decisions: []
  specs:
    - "[[spec-011-slack-knowledge-capture|OKK-SPEC-011]]"
    - "[[spec-003-python-client-and-streaming-api|OKK-SPEC-003]]"
    - "[[spec-008-middleware-and-operational-controls|OKK-SPEC-008]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works: []
  releases: []
  related: []
---

# OKK-WORK-006 Slack Thread 기반 inbox·reference 지식 수집

Slack `app_mention`으로 시작한 thread를 하나의 `open_kknaks` session과 하나의
Markdown 노트에 연결한다. 일반 텍스트는 inbox, 외부 자료 URL은 reference로
구조화하며 같은 thread의 후속 메시지는 같은 노트를 안전하게 갱신한다.

> 비목표: permanent/product/post 자동 승격, slash command, 공개 HTTP Events API,
> Slack 파일 첨부.

## Meta

- Baseline: [[OKK-BL-002-slack-idea-knowledge-graph|OKK-BL-002]]
- Covers spec: [[spec-011-slack-knowledge-capture|OKK-SPEC-011]]
- Depends on work: 없음
- Parallel work: 없음
- Follow-up work: permanent 고도화·연결 승인 워크플로
- External dependency:
  - Slack bot/app token과 Socket Mode 설정
  - Redis
  - `open_kknaks` 2.x `AgentClient`
  - YouTube/웹/논문 원문 접근 가능성
  - 참고 구현 `/Users/kknaks/git/toy_pr2/kknaks_mobile` (읽기 전용)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | in_progress |
| Progress | 90% |
| Branch/PR | `feat/knowledge-graph` |
| Blocker | 없음 |
| Next | 실제 Slack·YouTube/reference smoke와 운영 검증 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | SPEC-011 범위와 비목표 유지 | done |
| Design |  | Slack thread 접수·진행·성공·실패 메시지 | todo |
| FE |  | 해당 없음 | done |
| BE |  | capture core, Slack bridge, session, AgentClient, source extractor | in_progress |
| QA |  | 단위·통합·fixture 기반 E2E 검증 | todo |
| Ops |  | compose service, token/allowlist, feature flag, rollback | todo |

## Scope

포함:

- `.agent/skills/capture-knowledge/`과 고정 structured output 계약
- idea/reference schema validator와 deterministic Markdown renderer
- source type 감지와 YouTube·블로그·논문 extractor
- Slack Bolt Socket Mode bridge
- `app_mention` 신규 session과 활성 thread 후속 message 처리
- Redis idempotency, session TTL, thread별 lock
- `AgentClient` 신규/resume task 실행
- atomic file create/update와 runtime graph reload
- 기존 git push 잡을 재사용한 capture 파일 자동 commit/push
- Slack thread 결과 응답

제외:

- permanent 자동 생성과 inbox 분류 완료 처리
- 자동 wikilink 확정
- Slack 파일 업로드/다운로드
- 다중 workspace 설치/OAuth UI
- URL 뒤 로그인·paywall 우회

## Code Surface

- Repo / module: `/Users/kknaks/git/toy_pr2/kknaks_profile`

| 경로 후보 | 설명 |
|---|---|
| `.agent/skills/capture-knowledge/` | idea/reference 구조화 지침과 schema reference |
| `app/back/service/knowledge_capture/` | domain model, parser, validator, renderer, writer, source extractor |
| `app/back/service/slack_bridge/` | Bolt handler, session/idempotency store, runner |
| `app/back/tests/` | capture/slack/session/source 단위·통합 테스트 |
| `app/slack_bridge/run.py` | Socket Mode 프로세스 entrypoint |
| `app/back/pyproject.toml` | Slack/source parsing 의존성 |
| `docker-compose*.yml` | slack-bridge 서비스와 env/mount |
| `.env.example` | token, allowlist, provider/model, feature flag |

- Domain / schema note: DB migration 없음. Redis ephemeral record와 Markdown 파일이 SoT다.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `CaptureRequest` | Slack event를 정규화한 한 번의 사용자 입력 |
| `CaptureSession` | `(channel, root_thread_ts)`와 provider session/output path 매핑 |
| `CaptureDocument` | skill이 반환하고 renderer가 소비하는 versioned structured output |
| `CaptureResult` | 저장·reload·Slack 응답 결과 |

- 상태 / invariant:
  - thread 하나당 `kind`, provider session, output path 각각 하나
  - 후속 응답은 patch가 아니라 전체 document snapshot
  - skill/worker는 repository를 직접 쓰지 않음
  - validation 성공 전 기존 파일을 바꾸지 않음
  - 같은 thread 작업은 직렬화
- Migration 필요 여부: 없음
- SPEC 환류: 외부 동작 변경이 발견되면 SPEC-011을 먼저 수정

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| Slack bridge | capture service | 정규화 요청 → task 실행·저장 결과 |
| capture service | `AgentClient` | 신규 task와 provider session resume |
| renderer | `CaptureDocument` | versioned schema → deterministic Markdown |
| writer | loader/reload | 저장 전 검증과 저장 후 runtime reload |

## Internal Interface Contract

```python
async def capture(request: CaptureRequest) -> CaptureResult: ...
async def refine(request: CaptureRequest, session: CaptureSession) -> CaptureResult: ...
def parse_document(raw: str) -> CaptureDocument: ...
def render_document(document: CaptureDocument, context: RenderContext) -> str: ...
```

- `capture()`은 최초 파일을 만들고 session ID/output path를 저장한다.
- `refine()`은 기존 파일과 provider session을 사용해 같은 path를 atomic replace한다.
- 외부 I/O는 adapter에 두고 parser/validator/renderer는 순수 함수로 테스트한다.

## Execution

### Phase 1 — 문서·domain 계약 고정

- **Status**: IN_PROGRESS
- **설명**: SPEC-011을 구현 가능한 work와 내부 경계로 내린다.
- **작업**:
  - [x] WORK-006 생성과 spec coverage 등록
  - [x] `kknaks_mobile`의 thread/session 구현 조사
  - [x] 실제 설치된 `open_kknaks` 2.x API 확인
- **검증**:
  - [x] SPEC-011의 app mention·Socket Mode·thread invariant와 일치
  - [x] 문서 graph 단위 테스트 통과
- **완료 증거**: WORK-006/index 등록, `AgentClient` 신규/resume 계약 확인, graph 테스트 통과

### Phase 2 — Capture core와 skill

- **Status**: DONE
- **설명**: Slack 없이도 입력→검증→Markdown 생성이 결정론적으로 동작하는 기반을 만든다.
- **작업**:
  - [x] `capture-knowledge` skill과 schema reference 작성
  - [x] domain dataclass/model과 JSON parser/validator 구현
  - [x] inbox/reference renderer와 path policy 구현
  - [x] atomic writer와 기존 파일 갱신 guard 구현
  - [x] source type detection과 extractor interface 구현
- **검증**:
  - [x] idea/reference golden fixture가 고정 템플릿과 일치
  - [x] schema/kind/path/group/connection candidate 오류가 저장 전 차단
  - [x] atomic replace 전 실패 시 기존 파일 유지
- **완료 증거**: idea/reference schema·renderer·atomic writer·URL/YouTube extractor 구현, skill validator green

### Phase 3 — Slack thread와 session

- **Status**: DONE
- **설명**: Socket Mode event를 thread 단위 capture session으로 연결한다.
- **작업**:
  - [x] app mention과 활성 thread message handler 구현
  - [x] allowlist fail-closed와 bot/subtype filter 구현
  - [x] Redis session/idempotency/per-thread lock 구현
  - [x] 접수 placeholder와 성공·실패 thread 응답 구현
- **검증**:
  - [x] root `event.thread_ts or event.ts` 규칙
  - [x] 활성 thread만 멘션 없는 후속 message 처리
  - [x] event 재전송과 동시 후속 입력에서 중복·유실 없음
  - [x] TTL 만료 후 후속 입력 무시
- **완료 증거**: `CaptureSessionStore`, Socket Mode handler와 fake Redis/runner 테스트 통과

### Phase 4 — AgentClient·source·reload 통합

- **Status**: DONE
- **설명**: 실제 `open_kknaks` 실행과 원문 수집, 저장·reload를 end-to-end로 연결한다.
- **작업**:
  - [x] `AgentClient` 신규/resume task adapter 구현
  - [x] YouTube transcript·웹 article source adapter 구현
  - [x] paper PDF full text adapter 보강
  - [x] capture result 저장과 runtime reload 연결
  - [x] bridge entrypoint와 compose/env 배선
- **검증**:
  - [x] worker repository write 없이 structured output 반환하도록 경계 분리
  - [x] 같은 thread 두 번째 입력이 같은 provider session과 output path 사용
  - [x] fixture reference 저장 후 reload·inbox 비노드 검증
  - [x] source fetch SSRF/timeout/size/redirect fixture 보강
- **완료 증거**: AgentClient session resume/동일 파일 갱신, reference reload, source security fixture, compose config green

### Phase 5 — QA·운영 검증

- **Status**: IN_PROGRESS
- **설명**: fixture 자동화와 실제 Slack smoke로 배포 가능 상태를 확인한다.
- **작업**:
  - [x] unit/integration test 전체 실행
  - [x] fake Slack/Redis/AgentClient E2E 실행
  - [ ] 실제 Slack mention→thread follow-up smoke
  - [x] 운영 env·로그·feature flag·rollback 정적 확인
  - [ ] WORK/index/log 상태 갱신
- **검증**:
  - [ ] SPEC-011 Acceptance Criteria 전부 충족
  - [ ] 기존 backend/graph/job regression 없음
  - [ ] secret·원문 전문·로컬 절대경로 로그/응답 미노출
- **완료 증거**: backend 전체 303 passed, capture targeted 17 passed, skill/compose/diff validation green

## Pre-deploy Check

- [x] `SLACK_CAPTURE_ENABLED=0` 기본값에서 기존 서비스 무영향
- [x] app/bot token과 allowlist가 secret/env로만 주입됨
- [ ] bot이 지정 channel과 사용자 외 입력을 처리하지 않음
- [ ] worker에 repository write tool이 노출되지 않음
- [x] source fetch SSRF guard가 활성화됨
- [x] Slack 응답에 secret·절대 경로·raw stack trace 없음

## Rollback

- `SLACK_CAPTURE_ENABLED=0`으로 bridge를 중지한다.
- compose의 `slack-bridge` 서비스만 내려 기존 backend/worker/Redis를 유지한다.
- Markdown migration이 없으므로 생성된 노트는 자동 삭제하지 않는다.
- Redis capture namespace는 TTL로 만료시키며 기존 open_kknaks queue namespace와 분리한다.

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] SPEC-011의 Acceptance Criteria가 자동/수동 검증에 매핑됐다.
- [ ] 전체 backend와 graph regression 테스트가 통과했다.
- [ ] 실제 Slack thread 기반 smoke가 통과했다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 실제 Slack credential과 실행 중인 Redis/worker가 필요한 mention→thread smoke가 남아 있다.

## Related

- SPEC: [[spec-011-slack-knowledge-capture|OKK-SPEC-011]]
- Reference implementation:
  - `/Users/kknaks/git/toy_pr2/kknaks_mobile/src/bridge/app.py`
  - `/Users/kknaks/git/toy_pr2/kknaks_mobile/src/bridge/sessions.py`
  - `/Users/kknaks/git/toy_pr2/kknaks_mobile/src/bridge/runner.py`
