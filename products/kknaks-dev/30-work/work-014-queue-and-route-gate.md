---
type: work
id: KDEV-WORK-014
title: "승인 큐 + route 게이트 MVP"
status: doing
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
progress: 75
created_at: 2026-07-27
updated_at: 2026-07-28
tags:
  - product/kknaks-dev
  - doc/work
  - status/doing
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
| Status | doing |
| Progress | 75% (Phase 3/4) |
| Branch/PR | — |
| Blocker | 없음 (WORK-012·013 완료) |
| Next | Phase 4 admin 큐 화면 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위·상태기계 확정 | todo |
| Design | kknaks | 큐 화면·게이트 카드 레이아웃 | todo |
| FE | kknaks | admin 큐 화면 | todo |
| BE | kknaks | 스키마·접수·준비·게이트 | done |
| QA | kknaks | 상태 전이·실패 회생 검증 | done (BE 범위) |
| Ops | kknaks | 마이그레이션 적용 | done (로컬 왕복 검증) |

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
- Migration 필요 여부: 필요 (0002·0003·0004)
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

- **Status**: DONE
- **작업**:
  - [x] Alembic 0002 (`queue_items`·`item_preparations`·`ai_tasks`)
  - [x] Alembic 0003 (`gates`·`gate_revisions`·`gate_feedbacks`)
  - [x] ORM 모델 + 제약(승인 버전 partial unique, CHECK 상태값)
- **검증**:
  - [x] upgrade/downgrade 왕복 성공
  - [x] 같은 게이트에 승인 버전 2개를 넣으면 제약 위반이 난다
- **완료 증거**:

`core/models.py` +6 모델, `alembic/versions/0002_create_queue.py`·`0003_create_gates.py`, `tests/test_queue_schema.py` 13건.

**왕복 실측** — 실 Postgres(45433)에 `upgrade head` → `downgrade 0001` → `upgrade head`. 0001 복귀 시점에 남은 테이블은 `users`·`alembic_version` 둘뿐이었고, 재적용 후 6개 테이블이 복원됐다. **`users` 행 수 2건 불변** (Pre-deploy Check 1항 충족).

**순환 FK** — `gates.active_revision_id → gate_revisions`, `gate_revisions.gate_id → gates`, `gate_revisions.feedback_id → gate_feedbacks`, `gate_feedbacks.target_revision_id → gate_revisions`. 테이블을 먼저 만들고 앞을 가리키는 FK 3개를 `create_foreign_key`로 뒤에 붙였다(모델은 `use_alter=True`). downgrade는 역순으로 제약부터 떼야 한다.

**DB가 강제하는 불변식** — 걸어만 두지 않고 발동을 확인했다.

| 제약 | 검증 |
|---|---|
| `uq_gate_revisions_approved` (partial unique) | 승인 버전 2개 → 거부. `superseded`는 무제한 공존 |
| `uq_gate_revisions_version` | 같은 `(gate, version)` 재삽입 → 거부 |
| `uq_gates_live_stage` (partial unique) | 같은 스테이지 2개 → 거부. **`cancelled` 뒤 재오픈은 통과** (D5 역방향 경로) |
| `uq_queue_items_pending_url` (partial unique) | 발행 전 같은 URL → 거부. **발행 후 재정리는 통과**, `null` URL 다건 공존 |
| `CHECK` 상태값 | `queue_items`·`ai_tasks`에 오타 상태 → 거부 |
| `stage_name` 무제약 | 미래 스테이지명 삽입 통과 — 정의가 데이터라 스키마를 안 건드린다(DEC-011 D2) |
| `ON DELETE CASCADE` | 항목 삭제 시 손자(`gate_revisions`)까지 정리 — 고아 행 구조를 두지 않는다 |

**모델↔마이그레이션 드리프트 가드** — 둘은 손으로 쓴 두 벌의 진실이라 갈라질 수 있다. `alembic check`를 테스트로 걸었고(`test_models_and_migrations_agree`), **가드 자체를 역검증**했다: 모델에만 컬럼을 하나 넣자 `AutogenerateDiffsDetected: add_column ... 'drift_probe'`로 정확히 실패했고 원복 후 통과했다. 현재 diff 0.

부수: `alembic.ini`의 `version_path_separator`가 폐기 경고를 내 `path_separator`로 교체.

368 passed (신규 13).

### Phase 2 — 접수와 자동 준비

- **Status**: DONE
- **작업**:
  - [x] WORK-012의 sink를 **큐 적재**로 교체 (파일 쓰기·push 제거)
  - [x] 수동 접수 API + 중복 판정(정규화 URL)
  - [x] 자동 준비 스테이지: 수집(yt-dlp·자막) + 요약
  - [x] 준비 실패 시 `prepare_failed` + 메모 보완 재시도 경로
  - [x] Slack 회신을 "접수됨 / 검토 대기"로 변경
- **검증**:
  - [x] Slack에 링크를 던지면 **레포에 파일이 생기지 않고** 큐에 적재된다
  - [x] 준비 완료 후 `in_review`로 전이한다
  - [x] 자막이 없는 영상에서 `prepare_failed` → 메모 추가 → 재시도로 `in_review` 도달
  - [x] 재시도가 기존 실패 기록을 덮어쓰지 않는다
  - [x] 발행 전 같은 URL 재투입 시 기존 항목에 합류한다
- **완료 증거**:

신규 `service/pipeline/`(urls·intake·prepare·summarize·slack_intake·runtime) + `api/routers/queue.py`. 테스트 55건 신규(`test_pipeline_intake` 31 · `test_pipeline_slack` 6 · `test_queue_api` 18). **423 passed.**

**동작이 바뀐 지점** — 이 work의 목적 그 자체다.

```
종전:  Slack → 수집 → AI가 노트 전문 작성 → 렌더 → 파일 쓰기 → origin/main 커밋
현행:  Slack → 큐 적재(received) → 자동준비(수집+요약) → in_review → (route 게이트 대기)
```

노트 전문 작성은 route 승인 뒤로 옮겼다(WORK-015). 목적지를 정하기 전에 본문을 쓰면 **폐기할 자료의 노트까지 쓰게 되고**, 무엇보다 사람이 보기 전에 결과가 확정된다.

**"파일이 안 생긴다"를 사후 확인하지 않는다** — `Path.write_text`·`write_bytes`·`commit_and_push_with_retry`를 **예외를 던지게 만들어 놓고** 전 흐름을 태운다(`no_filesystem_writes` fixture). 밟으면 터진다.

**URL 정규화 (OQ 해소)** — 폭이 곧 정확도다. 좁으면 같은 영상이 두 번 정리되고, **넓으면 다른 자료가 조용히 합쳐진다.** 후자가 더 위험해서(사라진 걸 알아채기 어렵다) 층을 나눴다.

| 대상 | 규칙 | 근거 |
|---|---|---|
| 유튜브 | **영상 ID만** (`youtube:ID`) | ID가 정체성 전부. `t`·`list`·`si`·`shorts`·`embed`·`youtu.be`는 모두 같은 영상 |
| 그 외 | **추적 파라미터만** 제거(utm_*·fbclid·gclid·si·ref…), 나머지 쿼리 보존·정렬 | 어떤 쿼리가 식별자인지 일반적으로 알 수 없다 → 지우는 쪽이 아니라 **남기는 쪽이 기본값** |
| 공통 | host 소문자·`www.` 제거·기본포트 제거·후행 슬래시·fragment 제거 | 문서 내 위치는 정체성이 아니다 |
| 판정 불가 | `None` (중복 검사 제외) | 틀린 키로 서로 다른 자료를 묶는 것보다 낫다 |

**메모가 원문을 대체한다** — 수집이 막혀도(자막 없음·봇 차단) 사람이 한 줄 남기면 준비가 성립한다. Slack 스레드 후속 발언이 그대로 메모로 흘러가고, 항목이 `prepare_failed`면 **거기서 재시도까지 이어진다.** 준비 payload에 `material_source: fetched|note`와 `collect_error`를 남겨 **근거가 원문인지 사람 기억인지** route 판단이 구분할 수 있게 했다.

**재료가 없으면 AI를 부르지 않는다** — 원문도 메모도 없으면 요약 호출 없이 `NO_SOURCE_MATERIAL`로 실패시킨다. 부르면 환각을 근거로 route를 판단하게 된다(`test_no_source_and_no_note_fails_without_calling_ai`가 AI 호출 시 실패하도록 고정).

**재시도는 덮어쓰지 않는다** — 새 `item_preparations` 버전 + 새 `ai_tasks` 행, `retry_of_task_id`로 원 실패를 가리킨다. 실패 v1 + 성공 v2가 함께 남는 것을 검증했다.

**큐 API** — 전 엔드포인트가 `Depends(require_admin)` 뒤에 있고 6개 경로 전부 비인증 401을 확인했다. 발행 재시도는 **만들지 않았다** — Executor가 없는데 자리만 잡아 두지 않는다(WORK-015).

부수 정리:
- `_known_stems`·`_allowed_groups`는 소비자 0이 되어 삭제(사용처가 runner 주입뿐이었다). `KnowledgeCaptureRunner`·`FileCaptureStore`는 **남긴다** — Rollback 경로이자 WORK-015가 재사용할 노트 작성 기계다.
- **테스트가 실 Slack에 접속하고 실 AI를 호출하고 있었다.** `.env`를 source한 셸에서 돌리면 `SLACK_CAPTURE_ENABLED=1`이 그대로 들어와 TestClient lifespan이 워크스페이스에 Socket Mode로 붙었다(로그의 `⚡️ Bolt app is running!`, `[youtube] Video unavailable`이 증거). conftest에서 **덮어써서** 강제로 끈다.
- `core/db.py`에 `new_session()` 추가 — `get_db`는 FastAPI 의존성이라 요청 밖(Slack 핸들러)에서 못 쓴다.
- 요약기는 캡처 런타임이 연 broker 연결을 `service/pipeline/runtime.py`로 공유한다. 큐 API가 연결을 두 벌 열지 않는다. 캡처가 꺼져 있으면 재시도는 **503으로 정직하게 거절**한다 — 조용히 대체 경로를 만들지 않는다.

### Phase 3 — route 게이트 + 공통 계약

- **Status**: DONE
- **작업**:
  - [x] 파이프라인 정의 등록(유튜브) + 저장 위치 결정
  - [x] route 게이트 생성 + 목적지 제안 AI 호출
  - [x] 승인 → 목적지 확정 + 체인 길이 확정(뒤 스테이지 게이트 생성은 WORK-015)
  - [x] 피드백 → v2 재생성 (세션 resume, v1 read-only 보존)
  - [x] 형제 검토가능 버전 sweep
  - [x] 실패 → `재시도`(새 실행 행)
- **검증**:
  - [x] 준비 완료 시 route 게이트가 자동 생성된다
  - [x] 피드백 후 v2가 생기고 v1이 read-only로 남는다
  - [x] 재생성을 연속 2회 트리거해도 검토 가능 버전이 1개만 남는다
  - [x] 세션 resume이 동작한다 (원문 재전송 없이 반영)
  - [x] 세션이 없을 때 stateless로 재생성되며 실패하지 않는다
  - [x] 승인된 게이트에 피드백하면 거부된다
  - [x] `폐기` 승인 시 항목이 `discarded`가 되고 파일이 생기지 않는다
- **완료 증거**:

신규 `service/pipeline/{definitions,gates,route,flow}.py` + 큐 API 게이트 5경로. 테스트 39건 신규(`test_pipeline_gates` 31 · `test_queue_api::TestGates` 8). **462 passed.**

**파이프라인 정의 저장 위치 — 코드 상수 (OQ 해소).** DB 테이블로 두면 얻는 것은 "마이그레이션 없이 스테이지 순서 변경"인데 정의를 고치는 사람이 한 명뿐이라 값을 못 한다. 테이블만 둘 는다. **옮길 시점을 미리 박아 뒀다** — 소스 종류가 3개를 넘거나, 화면에서 정의를 편집하고 싶어질 때. 그때도 데이터 마이그레이션은 없다(정의가 코드에만 있다).

**절차와 내용을 분리했다.** `gates.py`는 생성·피드백·재생성·재시도·승인 **절차만** 알고, 무엇을 만들지는 주입된 generator가 안다. WORK-015의 `source_note`·`concept`·`derived` 게이트가 이 파일을 그대로 재사용한다 — 스테이지마다 만드는 건 달라도 절차는 하나다.

**세 상태를 섞지 않는다.**

| 컬럼 | 소유 | 예 |
|---|---|---|
| `gates.status` | 사람이 보는 단계 | `review_pending` |
| `gate_revisions.status` | AI 제안 버전 | `reviewable` |
| `ai_tasks.status` | 실행 | `succeeded` |

셋이 동시에 저 값인 것이 정상이다. 합치면 *"AI가 실패한 것"*과 *"사람이 아직 안 본 것"*이 구분되지 않는다.

**sweep 순서** — 새 버전이 `reviewable`이 되기 **직전**에 형제를 밀어낸다. 반대로 하면 잠시 검토 대상이 0개가 된다. `drafting`(생성 중)은 건드리지 않는다 — 밀어내면 지금 돌고 있는 재생성이 완료 시점에 이미 죽어 있다.

**AI에게 규칙을 프롬프트로 주지 않는다.** route 프롬프트는 *"`rules/knowledge-note-pipeline.md`와 `templates/knowledge/`를 읽고 판단하라"*고 지시한다. 4층 모델·개념 입도 기준을 프롬프트에 복사하면 SoT가 둘이 되고 한쪽만 고쳐지는 날 조용히 어긋난다 — WORK-013에서 세운 원칙을 첫 소비자가 실제로 따르는 지점이다.

**사람이 고친 값도 같은 검사를 통과한다.** 승인 시 `payload`를 넘기면 AI 출력과 동일하게 `validate_route_result`를 태운다. 토글을 이상하게 조합한 채로 확정되면 뒤 스테이지가 헛돈다. 검사 항목: group이 `persona/_meta.yaml`의 clusters 값인가 · exclusive와 목적지를 동시에 켜지 않았는가 · 아무것도 안 켰으면 exclusive를 정했는가.

**낙관적 잠금** — `expected_revision_id`. 다른 탭에서 재생성이 돌았는데 옛 화면의 승인 버튼이 먹으면 **사람이 보지 않은 내용을 승인**하게 된다.

**`inbox_hold`는 끝이 아니다.** `discard`만 항목을 `discarded`로 끝낸다. 보류는 `inbox/`에 idea 노트를 남기는 발행이 남아 있어 여전히 발행 대상이다(DEC-011 D1).

**정의 없는 종류에 유튜브 체인을 붙이지 않는다.** 블로그·수동 항목은 게이트 없이 큐에 남고 그 상태가 화면에 보인다 — 조용히 엉뚱한 체인을 태우는 것보다 낫다. 블로그 파이프라인은 해당 work에서 등록한다.

**스키마 결함을 발견하고 고쳤다 (0004).** 항목 hard delete가 **FK 순환으로 실패**했다 — `queue_items → ai_tasks·gates → gate_revisions`가 CASCADE로 지워지는데 `gate_revisions.ai_task_id → ai_tasks` 같은 참조가 그 사이를 가로질러 삭제 순서가 어긋난다.

```
ForeignKeyViolation: update or delete on table "ai_tasks" violates
foreign key constraint "fk_gate_revisions_ai_task" on table "gate_revisions"
```

P1의 CASCADE 테스트는 `ai_task_id`·`active_revision_id`를 **비워 둔 채** 지워서 통과했다. 가로지르는 nullable 참조 8개를 `ON DELETE SET NULL`로 바꾸고(소유 관계 `item_id`·`gate_id`는 CASCADE 유지), 테스트를 **참조를 전부 채운 그래프**로 다시 썼다. CASCADE로 바꾸지 않은 이유는 실행 행 하나가 지워질 때 그걸 참조하던 제안 버전까지 사라져 이력 불변 전제가 깨지기 때문이다.

부수: `retry_prepare`가 `prepare_item`만 불러 **재시도로 살아난 항목엔 게이트가 영영 안 열렸다** → `prepare_and_open_gate`로 교체.

테스트 속도: 큐 API가 매 테스트 TestClient를 띄워 전체 스위트가 101초로 늘었다. 모듈 스코프 + 쿠키만 초기화로 바꿔 **59초**(해당 파일 63초→9초).

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

- ~~파이프라인 정의 저장 위치(코드 상수 vs DB)~~ — **P3에서 해소: 코드 상수.** 옮길 조건은 소스 종류 3개 초과 또는 화면 편집 요구. 근거는 Phase 3 완료 증거.
- ~~`normalized_url` 정규화 범위~~ — **P2에서 해소.** 유튜브=영상 ID만, 그 외=추적 파라미터만 제거(나머지 쿼리 보존). 근거는 Phase 2 완료 증거.
- **이 work가 끝나면 큐에 항목이 쌓이지만 발행은 안 된다.** WORK-015까지 가야 md가 나온다. 그 사이 기간에 캡처를 계속 쓸지, WORK-015까지 묶어서 배포할지 판단이 필요하다.
- **P2 배포 시점부터 Slack 캡처의 산출물이 사라진다.** 지금 배포하면 링크를 던져도 큐에만 쌓이고 노트는 안 나온다(route 게이트가 P3, 발행이 WORK-015). 캡처를 계속 쓰려면 **WORK-015까지 묶어서 배포**하는 편이 맞다.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 선행 WORK-012·013, 후속 WORK-015
