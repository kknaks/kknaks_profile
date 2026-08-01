---
type: work
id: KDEV-WORK-017
title: "잔디 커밋 파이프라인 — 레지스트리·로컬 클론·승인 게이트"
status: in_progress
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
progress: 25
created_at: 2026-07-31
updated_at: 2026-08-01
tags:
  - product/kknaks-dev
  - doc/work
  - status/in_progress
links:
  baselines:
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
  decisions:
    - "[[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]]"
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
    - "[[decision-016-grass-gate-and-publish|KDEV-DEC-016]]"
  specs:
    - "[[spec-011-commit-collection|KDEV-SPEC-011]]"
    - "[[spec-012-grass-artifacts|KDEV-SPEC-012]]"
    - "[[spec-013-grass-gate|KDEV-SPEC-013]]"
    - "[[spec-010-apply-executor|KDEV-SPEC-010]]"
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
  works:
    - "[[work-016-async-execution-and-progress-ui|KDEV-WORK-016]]"
  releases: []
  related:
    - "[[work-015-youtube-chain-and-executor|KDEV-WORK-015]]"
---

# 잔디 커밋 파이프라인 — 레지스트리·로컬 클론·승인 게이트

잔디 잡을 **승인 게이트 위로 올린다.** 커밋 조사를 GitHub API 에서 로컬 bare 클론으로 바꾸고, 산출물을 `daily` 한 장에서 `daily`·`career`·`concept` 셋으로 늘린다.

**만들지 않는 것**: `algorithms`·`content_enrich` 잡의 게이트 편입, showcase 케이스 스터디, 레지스트리 관리 화면, 그래프 재정비.

## Meta

- Baseline: [[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]
- Covers spec: SPEC-011·012·013 (신규) + SPEC-010 (개정분)
- Depends on work: [[work-016-async-execution-and-progress-ui|KDEV-WORK-016]] — 제출/수확 분리와 드라이버가 전제다. 잔디 파이프라인은 그 위에 정의만 얹는다
- Parallel work: 없음
- Follow-up work: `algorithms`·`content_enrich` 게이트 편입 (후속 baseline)
- External dependency: **P5 에만 있다** — `GH_TOKEN_COMPANY`(회사 레포 클론) · 디스크 약 321MB · 서버 재배포(compose 볼륨 추가). **P1~P4 는 외부 의존이 없다.** 더미 조사로 파이프라인 한 바퀴를 먼저 완주시키기 때문이다(아래 Execution 머리말)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | in_progress |
| Progress | 25% (P1 done · P2 진행 중) |
| Branch/PR | `work-017-p2` |
| Blocker | 없음 |
| Next | P2 잔여 — auto 스테이지 루프·이름별 등록·수집 전제 해제·fan-out 저장·더미 `collect`·`investigate`·`compose`·합성 키 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | doing |
| Design | kknaks | 승인 화면 편집 UX | todo |
| FE | kknaks | 게이트 화면 (줄/문장 단위 편집) | todo |
| BE | kknaks | 준비부 일반화·스테이지·발행부·클론 | doing |
| QA | kknaks | 검증과 완료 판단 | todo |
| Ops | kknaks | 볼륨·env·배포·첫 클론 | todo |

## Scope

포함:

- `templates/persona/daily.md`·`career.md` 신규 + `agent.md` 등록
- **자동 준비부 일반화** — 정의의 `auto` 스테이지를 실제로 읽어 여러 개를 순서대로 돌린다
- `daily_commit` 파이프라인 정의 + `investigate`(fan-out)·`compose` 스테이지
- **더미 `collect`** — SPEC-011 §4 계약 전량을 코드가 지어내 P1~P4 를 외부 연동 없이 돌린다
- `apply/` 확장 6종 + `publish_atomic` 전환
- 게이트 화면 — 줄 단위 편집 · career 문장 단위 승인
- 레포 레지스트리 테이블 + 마이그레이션 + `showcase.md` 1회 시드 이관
- bare 클론 볼륨과 fetch 절차, identity drift 알림
- 진짜 `collect` — 로컬 git 조사(전 브랜치·identity 패턴·tree-hash dedupe·입력 상한·영역 분해)
- 스케줄러 접수 진입점(백필 포함) + 날짜 축 중복 판정
- 승인 대기 Slack 알림 전환

제외:

- `products/*/30-work`·`showcase.md`·`persona/posts/` 목적지 → 후속
- `inbox/` idea 목적지 → 채택하지 않음
- `career.bullets` 자동 갱신 → 영구 제외
- 레지스트리 admin CRUD 화면 → 후속

## Code Surface

- Repo / module: `app/back` (주) · `app/front` (게이트 화면) · 루트(templates·agent.md·compose)

| 경로 후보 | 설명 |
|---|---|
| `templates/persona/daily.md` · `career.md` | 형식 SoT (신규) — P1 |
| `agent.md` | 별도 계열에 daily·career 등록 — P1 |
| `service/pipeline/definitions.py` | `DAILY_COMMIT` 등록 · `auto_stages()` — P2 |
| `service/pipeline/prepare.py` | `AutoStage` 계약 · 수확 후 다음 auto 판정 · **`if item.source_url:` 수집 전제 해제** — P2 |
| `service/pipeline/flow.py` | 첫 게이트를 파이프라인 정의에서 고른다 — P2 |
| `service/pipeline/driver.py` | `_finish_preparing` 에 "다음 auto 가 남았나" 분기 · fan-out N 건 대응 — P2 |
| `service/pipeline/runtime.py` | auto 스테이지 실행기를 **이름으로** 등록 — P2 |
| `service/pipeline/intake.py` | **`intake()` 시그니처 확장** — 합성 키를 받는 자리 — P2 |
| `service/pipeline/collect_dummy.py` (신규) | 더미 조사 — SPEC-011 §4 계약 전량, 시나리오 7종 — P2 |
| `service/pipeline/stages/investigate.py` (신규) | 레포별 조사 fan-out — P2 |
| `service/pipeline/stages/compose.py` (신규) | 취합 — daily·career·concept 초안 — P2 |
| `service/apply/plan.py` | allowlist 2개 · `LAYER_PREFIX` · `build_actions` 분기 · `upsert` — P3 |
| `service/apply/graph_check.py` | `daily`·`career` 제외 — P3 |
| `service/apply/executor.py` | 본인 작성 보호 · 사람 전용 필드 검증 — P3 |
| `app/front/.../queue` | 게이트 화면 편집 UI — P4 |
| `core/models.py` | 레지스트리 모델 신설 — P5 |
| `alembic/versions/0007_*.py` | 레지스트리 테이블 마이그레이션 — P5 |
| `config.py` | 클론 루트 경로 · identity 패턴 · 입력 상한 — P5 |
| `service/jobs/repos.py` (신규) | 클론·fetch·identity 조회 — P5 |
| `service/pipeline/collect_commits.py` (신규) | 진짜 git 조사 (LLM 없음) — 더미를 **이 자리에서만** 갈아 끼운다 — P5 |
| `service/scheduler.py` | 잔디 잡 → 접수 호출로 교체 — P5 |
| `service/jobs/main_job.py` · `inputs.py` · `llm.py` · `upsert.py` | 구 잔디 경로 정리 — P5, **스케줄러 교체와 같은 커밋** |
| `service/notify.py` 호출부 | 발행 완료 → 승인 대기 알림 — P5 |
| `api/routers/queue.py` | 접수 날짜 파라미터(백필) — P5 |
| `docker-compose.yml` | `repo-cache` 볼륨 · `WORKER_CONCURRENCY` — P5 |
| `tests/test_jobs.py` | 구 잔디 경로를 붙들고 있는 테스트 정리 — P5, 같은 커밋 |

- Domain / schema note: **마이그레이션 1건**(레지스트리 테이블, P5). 큐·게이트 테이블은 무변경 — `source_kind`·`stage_name` 에 CHECK 가 없어 새 파이프라인이 스키마를 건드리지 않는다.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `tracked_repos` | 잔디가 추적할 레포. `slug`·`type`·`detail`·`account`·`enabled`·`path_rules`·`last_fetched_at`·`last_error` |

- 상태 / invariant: `slug` 유일. `type=company` 면 `detail` 필수이고 실재하는 career stem 이어야 한다. `type=studio` 면 `detail` 은 비어 있다.
- Migration 필요 여부: **필요**(신규 테이블 1개, P5). 기존 테이블 변경 없음.

### 자동 준비부 일반화는 마이그레이션이 **0건**이다

WORK-016 스키마가 이미 받아 준다. 확인한 근거 넷:

| 확인한 것 | 근거 |
|---|---|
| `AITask.kind` 에 새 값(`investigate`·`compose`)을 넣을 수 있다 | `models.py` 가 CHECK 를 안 걸었다. 주석이 그 이유를 밝혀 뒀다 — "스테이지는 정의에서 오므로 CHECK 를 걸지 않는다" |
| fan-out N 건을 항목으로 되찾을 수 있다 | `ix_ai_tasks_item_id` 인덱스가 있다 |
| 준비 버전이 실행 1건에 묶이지 않아도 된다 | `ItemPreparation.ai_task_id` 가 nullable 이다 |
| 스테이지별 결과를 버전 안에 쌓을 수 있다 | `ItemPreparation.payload` 가 JSONB 다 |

### `intake()` 는 시그니처가 늘어난다 — DB 는 이미 맞다

지금 `intake()` 는 `normalized_url` 을 `normalize_url(source_url)` 로만 채운다. 잔디는 URL 이 없고 날짜가 키라서 `daily:{date}` 합성 키를 밖에서 받을 자리가 필요하다. **코드만 늘고 스키마는 그대로다.**

- 부분 유니크 인덱스 `uq_queue_items_pending_url` 이 pending 상태에서 날짜 유일을 마이그레이션 없이 강제한다 — 같은 날짜로 두 번 접수하면 두 번째는 `joined` 로 합류한다
- 이미 발행된 날짜를 다시 접수하면 그 인덱스에 안 걸리고 `duplicate_published` 로 떨어진다. 이것이 SPEC-013 S-7 3항(사람 확인)과 정확히 같은 동작이다 — 자동으로 막지 않고 물어본다

- SPEC 환류: 없음 — SPEC-011 이 이미 계약을 담고 있다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| P2 `compose` 스테이지 | P1 의 템플릿 파일 | 형식 SoT 를 읽어 프롬프트를 만든다 |
| P2 나머지 전부 | P2 최선두의 준비부 일반화 | auto 스테이지를 여럿 돌릴 기계가 먼저 있어야 한다 |
| P3 발행부 | P2 의 게이트 산출물 | 승인 payload 형태가 계획 조립 입력이다 |
| P4 완주 | P2+P3 | 더미 한 바퀴는 레일과 발행부가 둘 다 있어야 돈다 |
| P5 진짜 조사 | P2 의 `collect` 자리 | 더미가 계약 전량을 내므로 교체가 그 한 곳에서 끝난다 |

## Internal Interface Contract

`collect` 산출물(= `investigate`·`compose` 의 입력)은 SPEC-011 §4 Data Contract 를 따른다. 여기서 다시 적지 않는다.

**스테이지 실행기 계약은 두 갈래다.** 하나로 뭉뚱그리면 auto 스테이지가 승인 리비전을 만들게 된다.

| 갈래 | 해당 스테이지 | 프로토콜 | 산출물 |
|---|---|---|---|
| 게이트 | `daily` | `gates.StageRunner` (`submit`·`poll`·`parse`) 그대로 — WORK-016 이 세운 것이다 | `GateRevision`. `open_gate`/`harvest` 경로를 탄다 |
| auto | `collect`·`investigate`·`compose` | 준비부의 `Summarizer` 계열 (`submit`·`poll`·`parse`·`wait`) | `ItemPreparation` 버전. **`GateRevision` 을 만들지 않는다** |

`investigate` 만 한 스테이지가 N 건을 제출한다. 그 N 건을 어떻게 저장하는지는 아래 P2 의 선결 항목이다 — 열어 두면 중반에 구조가 흔들린다.

## Execution

> **Phase 순서를 walking skeleton 으로 뒤집었다.** 발주 시점의 순서는 제일 무거운 것(bare 클론 321MB·볼륨·토큰·배포)을 맨 앞에 두고 있었다. 그러면 파이프라인이 한 번도 안 돌아 본 채로 인프라 작업을 하게 된다.
>
> **깃은 더미로 가져오고 파이프라인 전체 한 바퀴를 먼저 돌린다. 외부 연동은 뒤로.** 진짜 git 수집은 마지막에 `collect` 한 곳을 갈아 끼우는 일이 된다.
>
> 이 재배치가 해소하는 것 셋.
>
> ① **구 경로 제거의 순서 위험이 구조적으로 사라진다.** `inputs.py` 의 `fetch_repo_commits`·`extract_tracked_repos` 는 유일한 소비자가 `main_job.py` 인데, 스케줄러를 안 바꾼 채 먼저 지우면 **백엔드가 부팅되지 않는다** — `main.py` 의 `lifespan` 이 `service.scheduler` 를 임포트하고 그것이 `main_job` → `inputs.py` 로 이어지는데, 그 임포트만 실패를 삼키는 자리가 없다(같은 `lifespan` 의 `seed_admin` 과 Slack 캡처는 "부팅 비차단"이라고 주석에 못박혀 있다). 잔디만 멎는 게 아니라 사이트 조회 API·승인 큐·유튜브 파이프라인·Slack 캡처가 같이 멈춘다. 이제 그 제거가 P5 한 곳에만 있다. **다만 P5 안에서 "스케줄러 교체와 같은 커밋" 규율은 그대로 유지한다** — 이유가 사라진 게 아니라 노출 구간이 좁아졌을 뿐이다.
> ② **P1~P4 내내 구 잔디 잡이 정상 동작한다.** 잔디에 구멍이 나지 않는다.
> ③ **배포가 P5 한 번뿐이다.** P1~P4 는 로컬에서 끝난다.

### Phase 1 — 형식 SoT (문서)

- **Status**: DONE
- **설명**: `compose` 가 읽을 양식을 먼저 만든다. 코드가 아니라 문서 작업이고, 뒤 Phase 전부의 선행 조건이다.
- **작업**:
  - [x] `templates/persona/daily.md` — frontmatter 필드 소유(`counts`=코드), 본문 섹션, 길이 상한 1200자
  - [x] `templates/persona/career.md` — 섹션 5종(`## 담당 영역` 포함), **append 금지·압축 재서술** 규율, 섹션당 5~7줄 상한, `stack` 판정 근거, 사람 전용 필드 격리
  - [x] `agent.md` — "별도 계열" 에 daily·career 등록 (교안과 같은 형태)
- **검증**:
  - [x] 두 템플릿이 존재하고 `agent.md` 에서 도달 가능하다
  - [x] 형식 명세의 SoT 가 템플릿 둘뿐이다 — 새 `compose` 는 여기를 읽는다
  - [x] `bullets` 가 "AI 가 정하지 않는다" 로 명시돼 있다
- **완료 증거**:
  - 커밋 `7155cd2`. `templates/persona/daily.md`·`career.md` 신설, `agent.md` 「별도 계열」에 교안 다음 **셋째 항목**으로 등록.
  - **양식을 상상으로 쓰지 않고 코드에서 읽어 담았다.** 셋을 확인해 템플릿에 넣었다.
  - ① **로더 하드 검증**(`service/persona_loader.py`) — `date` 는 점 표기이고 하이픈으로 바꾼 값이 파일명 stem 과 같아야 한다. `auto: true` 면 `counts` 는 dict, `summary` 는 `null` 이거나 `{ko, en}` 이고 각 값은 `list[str]` 이어야 한다. **어기면 그 파일 하나가 거부되는 데서 끝나지 않는다** — `PersonaError` 가 올라와 persona 로드 **전체**가 실패하고, `reload_data` 가 기존 데이터를 그대로 두므로 사이트는 옛 데이터를 계속 서빙한다. 발행 뒤에야 알게 되는 실패라 나가기 전에 지켜야 한다. 그래서 이 넷을 템플릿에 별도 절로 박았다.
  - ② **5개 섹션은 재직 경력의 양식이다.** `is_current: true` 는 `medisolve-ai` 하나뿐이고, 교육과정 career(`bitcamp`·`likelion`)는 섹션 구조가 아예 다르다(`## 다룬 주제`·`## 프로젝트`). 못박아 두지 않으면 AI 가 남의 문서를 이 양식에 맞추려 든다.
  - ③ **`/api/career` 가 `bullets` 를 내보내지 않는다** — 응답 필드는 `period`·`title`·`org`·`location`·`summary`·`stack`·`is_current`·`body` 여덟이다. "사람 전용" 이 규율일 뿐 아니라 **경력 페이지에 나오지도 않는다**는 사실을 근거로 적었다. 이력서 PDF 전용이라는 것이 코드로 확인된다.

> **`llm.py` 프롬프트 손질을 이 Phase 에서 뺐다.** 발주에는 "프롬프트에 박힌 daily 형식 명세를 템플릿 로드로 전환" 이 있었는데, 그 프롬프트는 구 `main_job` 전용이고 P5 에서 통째로 걷힌다. 곧 지울 코드를 형식에 맞추는 것은 두 번 일하는 것이다. 이중 SoT 는 코드를 고쳐서가 아니라 **구 경로가 사라져서** 해소된다.

### Phase 2 — 파이프라인 레일 + 더미 collect (BE)

- **Status**: IN_PROGRESS
- **설명**: 조사 결과를 게이트에 태운다. 여기서 처음으로 승인 화면에 잔디 항목이 뜬다. **외부 연동은 하나도 하지 않는다** — 조사는 더미가 지어내고, 접수는 기존 `POST /api/admin/queue/items` 를 손으로 부른다. 스케줄러와 Slack 알림 전환은 P5 다. 구 잔디 잡은 그대로 돌게 둔다.

#### 2-A. 자동 준비부 일반화 (**나머지 전부의 선행조건**)

정의에 auto 스테이지를 셋 적어도 **돌릴 기계가 없었다.** 현행 준비부는 "수집 1회 + 요약 1회" 로 굳어 있다. `definitions.py` 의 `Stage("collect","auto")`·`Stage("summarize","auto")` 가 그 증거다 — 정의는 둘인데 아무도 읽지 않았다.

- **작업**:
  - [ ] `driver._finish_preparing` — 수확 뒤 "다음 auto 스테이지가 남았나" 분기. 남으면 제출하고 `preparing` 을 유지한 채 `True` 를 반환한다(기존 `MAX_STEPS` 루프가 다시 돈다). 없으면 `in_review` + 첫 게이트
  - [x] 파이프라인 정의의 `kind="auto"` 스테이지를 실제로 읽는다
  - [ ] `runtime.register()` 에 auto 스테이지 실행기를 **이름으로** 등록
  - [ ] `prepare.py` — 재료 수집을 스테이지 안으로 넣어 `if item.source_url:` 전제를 푼다. 지금은 URL 없는 잔디 항목이 `NO_SOURCE_MATERIAL` 로 준비 단계에서 죽는다
  - [x] 첫 게이트 러너 하드코딩 제거 — `driver.py`·`queue.py` **두 곳** 모두 `pipeline.first_gate()` 기반으로
  - [ ] `ItemPreparation.payload` 에 어느 auto 스테이지 결과인지 기록 (유튜브분은 들어갔고 일반화가 남음)
  - [ ] `investigate` fan-out 저장 — `ai_task_id` 를 비우고 `AITask.item_id` 로 N 건을 찾는다. `_running_preparation_ref` 의 단건 `with_for_update` 를 N 건 대응으로 바꾼다
  - [x] 유튜브 회귀 방지 — 기존 `submit_preparation` 본문을 유튜브 준비 실행기 하나로 감싸면 1:1 로 같다
- **검증**:
  - [x] 유튜브 준비 흐름에 회귀가 없다
  - [ ] `daily_commit` 이 auto 3개를 정의 순서대로 지난다
  - [x] 첫 게이트가 정의에서 결정된다 (유튜브=`route`, 잔디=`daily`)

> **fan-out 저장 방식은 Open Issue 가 아니라 여기서 정한다.** `_running_preparation_ref` 와 `harvest_preparation` 이 running 준비 **1건**을 `with_for_update` 로 잡고 있어서, 어느 형태를 고르든 그 두 함수를 고쳐야 한다. 열어 두면 중반에 구조가 흔들린다. 이 결정이 "조사 중 (3/13)" 진행 표시(SPEC-013 U-1)와 부분 실패 처리의 전제이기도 하다.

#### 2-B. 잔디 파이프라인

- **작업**:
  - [x] `definitions.py` — `DAILY_COMMIT` 등록 (`collect`·`investigate`·`compose` auto + `daily` gate)
  - [ ] **더미 `collect`** — SPEC-011 §4 계약 전량을 지어낸다 (아래 「더미 경계」)
  - [ ] `investigate` 스테이지 — 레포별 N 건 제출·수확, 결과를 `ItemPreparation` payload 에 누적
  - [ ] 부분 실패 처리 — 일부 실패는 진행, 전부 실패면 스테이지 실패
  - [ ] `compose` 스테이지 — 템플릿 로드 + daily·career·concept 초안, `changed:false` 지원
  - [ ] career 결정적 skip (귀속 커밋 0이면 스테이지 미생성)
  - [ ] `runtime` 등록
  - [ ] `intake()` 시그니처 확장 + `normalized_url="daily:{date}"` 합성 키
  - [ ] 활동 0 · `auto:false` 접수 전 차단
- **검증**:
  - [ ] 수동 접수로 항목이 들어오고 요청이 AI 를 기다리지 않는다
  - [ ] `investigate` 가 레포 수만큼 돌고 부분 실패해도 게이트가 열린다
  - [ ] 전 레포 실패 시 스테이지 실패로 닫히고 재시도가 열린다
  - [ ] 게이트가 **하나**만 열린다
  - [ ] `type=studio` 만 커밋한 날은 career 초안이 없다
  - [ ] `is_current` 아닌 career 는 대상에서 빠진다
  - [ ] 같은 날짜로 두 번 접수하면 항목이 하나다
  - [ ] **기존 유튜브 파이프라인이 회귀 없이 동작한다**

> **더미 경계.** 레지스트리 테이블을 만들지 않는다(마이그레이션 `0007` 은 P5 다). 대상 레포 목록은 코드 안에 하드코딩한다.
>
> **더미는 SPEC-011 §4 조사 산출물 계약을 통째로 낸다** — `commits[]`·`areas`·`career_map`·`counts`·`truncated`·`failures[]`·`identities` 전부. **이것이 P5 교체 비용을 `collect` 한 곳에 가두는 근거다.** 계약을 줄이면 그 보장이 깨지고, `investigate`·`compose`·게이트 화면·발행부가 P5 에서 같이 흔들린다.
>
> 시나리오 7종을 낸다: 정상(company+studio 혼합) · `studio` 만 · `changed:false` · 일부 레포 실패 · 전 레포 실패 · 상한 적중 · 활동 0.

- **완료 증거**:
  - 커밋 `0ee2ace` — 준비부 일반화의 **앞부분**이 들어갔다. 테스트 **637 passed**(베이스라인과 동일 — 이 커밋은 기존 경로를 한 줄도 바꾸지 않았다).
  - 들어간 것: `Pipeline.auto_stages()` 신설 · `harvest_preparation` 이 실행기 **묶음**을 받아 `pipeline.first_gate()` 로 고르게 됨(`driver.py`·`queue.py` 두 호출부의 `"route"` 하드코딩 제거) · `DAILY_COMMIT` 등록.
  - 신설된 계약: **`AutoStage` 프로토콜 + `StageSubmission`** — 제출 건수를 0·1·N 으로 **함께** 다룬다. `collect` 는 LLM 을 안 부르니 0 이고, `investigate` 는 레포마다 하나씩 내니 N 이다. 종전 준비부는 1 만 가정했다. 이어서 `completed_auto_stages()`·`next_auto_stage()`, 그리고 `Summarizer` 프로토콜에 `wait` 선언을 채웠다 — **드라이버가 계속 부르고 있었는데 선언만 빠져 있었다.**
  - **설계 판단 하나를 남긴다: 실행기 하나가 정의상 스테이지 여럿을 덮을 수 있게 했다.** 유튜브 준비는 `payload["stages"]=["collect","summarize"]` 를 적어 한 번에 둘을 닫는다. 그래서 `next_auto_stage` 가 곧바로 `None`(= 게이트 차례)을 돌려주고 **기존 코드 경로는 한 줄도 바뀌지 않았다.** 정의(둘)와 코드(한 덩어리)가 어긋난 것을 굳이 쪼개면, 얻는 것 없이 회귀면만 넓어진다. 잔디는 셋을 각각 따로 덮는다.
  - **미완**: auto 루프 분기(`_finish_preparing`) · `runtime` 이름별 등록 · 수집 전제 해제 · payload 스테이지 기록 일반화 · fan-out 저장 · 더미 `collect` · `investigate`·`compose` · `intake()` 합성 키.

### Phase 3 — 발행부 확장 (BE)

- **Status**: TODO
- **설명**: 승인된 것이 실제로 파일이 되게 한다. P2 와 병렬 착수 가능하지만 e2e 는 P2 완료 후다.
- **작업**:
  - [ ] `plan.py` — `ALLOWED_PREFIXES` 에 `persona/daily/`·`persona/career/`
  - [ ] `LAYER_PREFIX` 에 `daily`·`career`
  - [ ] `build_actions()` 에 daily·career 분기
  - [ ] `upsert` 액션 신설 — 존재 여부 미검사, `stale 대상` 은 유지
  - [ ] `graph_check` — `daily`·`career` 제외 (`concept` 는 유지)
  - [ ] 본인 작성 보호 검증 (`USER_AUTHORED_DAILY`)
  - [ ] 사람 전용 필드 검증 (`PROTECTED_FIELD`)
  - [ ] 잔디 발행을 `publish_atomic` 으로 — **잔디 경로**가 `commit_and_push_with_retry` 에서 이탈한다. 함수 자체는 남는다 (`pdf_generate`·`content_enrich`·`algorithms` 가 계속 쓴다)
- **검증**:
  - [ ] `persona/daily/`·`persona/career/` 가 발행 허용된다
  - [ ] 같은 날 두 번 승인해도 `upsert` 로 통과한다 (`ALREADY_EXISTS` 없음)
  - [ ] daily·career 가 그래프 검증에서 빠지고 concept 는 검증을 받는다
  - [ ] 대상 daily 가 본인 작성이면 거부된다
  - [ ] 계획에 `bullets`·`period` 가 있으면 거부된다
  - [ ] push 실패 시 로컬 커밋이 남지 않는다
  - [ ] 발행 재시도가 AI 를 다시 부르지 않는다
  - [ ] 유튜브 발행이 회귀 없이 동작한다
  - [ ] **`dry_run` 이 어디까지 하는지가 테스트로 박혀 있다** — 파일은 써지고 커밋만 생략된다 (아래)
- **완료 증거**: 미작성

> **`dry_run` 의 사실관계를 여기서 못박는다.** `apply_item(dry_run=True)`·`publish_atomic(dry_run=True)` 는 둘 다 **기본값**이고, dry-run 이어도 `_write_all` 이 먼저 돌아 **파일은 작업트리에 실제로 써진다.** 생략되는 것은 커밋과 push 뿐이다. `item.status` 는 `published` 가 되고 `commit_ref` 는 `None` 이다.
>
> 이 사실이 P4 완주의 관측 방법을 정한다. "발행됐다" 를 커밋 로그로 확인할 수 없고 **작업트리를 봐야 한다.**

### Phase 4 — 게이트 화면 + 더미 한 바퀴 완주 (FE/QA)

- **Status**: TODO
- **설명**: 사람이 실제로 승인할 수 있어야 한 바퀴다. 배포도 실발행도 하지 않는다 — 그건 P5 다. 여기서 확인하는 것은 **파이프라인이 끝에서 끝까지 돈다**는 것 하나다.
- **작업**:
  - [ ] 조사 진행 표시 (`investigate` N건 중 진행 수, 실패 레포, 상한 적중)
  - [ ] daily 요약 **줄 단위** 편집·삭제
  - [ ] career **문장 단위** 승인·제외 토글 + 기존 문서와의 차이 표시
  - [ ] concept 개별 제외 토글 (기존 패턴 재사용)
  - [ ] 더미 조사 → 게이트 → 승인 → 발행까지 **한 바퀴 완주** (dry-run)
- **검증**:
  - [ ] 요약 줄을 지우고 승인하면 지운 결과가 발행된다
  - [ ] career 문장을 제외하면 파일에 없다
  - [ ] 회사 레포 서술을 덜어낸 결과가 공개 md 에 반영된다
  - [ ] 승인 안 한 날의 잔디 칸이 비어 있다가 나중 승인 시 채워진다
  - [ ] **완주 관측**: `persona/daily/{date}.md` 와 `persona/career/{stem}.md` 가 실제로 생성돼 `git status` 에 뜬다. **커밋은 없다** — dry-run 이 커밋과 push 만 생략하기 때문이다
  - [ ] 시나리오 7종이 각각 화면에서 구분돼 보인다
- **완료 증거**: 미작성

### Phase 5 — 진짜 git 수집 + 외부 연동 + 실운영 (BE/Ops)

- **Status**: TODO
- **설명**: 더미를 진짜 조사로 갈아 끼우고, 스케줄러·알림·배포를 붙인다. **가장 무겁고 유일하게 배포가 필요한 단계다.** WORK-015·016 과 같이 **실운영 완주를 완료 조건으로** 둔다 — 코드가 도는 것과 하루치가 발행되는 것은 다르다.
- **작업**:
  - [ ] `tracked_repos` 모델 + 마이그레이션 `0007`
  - [ ] `showcase.md` → 레지스트리 1회 시드 스크립트 (`links.repo`→`slug`, `org`→`type`), `detail` 은 company 5건 수동
  - [ ] `docker-compose.yml` — `repo-cache` 볼륨(back rw, 컨테이너 내 **`/var/cache/repos`**), 워커의 `CONCURRENCY` 리터럴을 **`${WORKER_CONCURRENCY:-2}`** 로 분리
  - [ ] `config.py` — 클론 루트, identity 패턴, 입력 상한(32KB/8KB/30건)
  - [ ] `service/jobs/repos.py` — `clone --bare` · `fetch --all --prune` · `last_fetched_at`/`last_error` 기록
  - [ ] identity 조회 + drift 판정 + Slack 알림
  - [ ] `collect_commits.py` — `git log --all --numstat --author=<패턴>` · KST 경계 · tree-hash dedupe · 영역 분해 · `counts`
  - [ ] 입력 상한 적용 + `truncated` 기록
  - [ ] **더미 `collect` 를 진짜 `collect` 로 교체** — 계약이 같으므로 이 스테이지 밖은 손대지 않는다
  - [ ] `scheduler.py` — 잔디 잡을 **접수 호출**로 교체
  - [ ] 접수 날짜 파라미터(백필)
  - [ ] Slack 알림 전환 — 발행 완료 → 승인 대기(발동 시 1회, 미승인 2건 이상 재알림)
  - [ ] 구 잔디 경로 제거 — `inputs.py` 의 `fetch_repo_commits`·`extract_tracked_repos`, 죽은 `git_log_today`(참조 0건), `main_job.py`·`llm.py`·`upsert.py` 잔여
  - [ ] `tests/test_jobs.py` 정리 — `write_daily` 6곳 + `summarize_daily` 4곳이 걷히는 코드를 붙들고 있다. `TestWriteDaily`·`TestLLM*` 계열이 통째로 대상이다
  - [ ] 배포 — 볼륨·env 반영, 서버에서 13개 최초 클론 (~321MB)
  - [ ] 하루치 실발행 완주
- **검증**:
  - [ ] `enabled=false` 레포가 조사에서 빠진다
  - [ ] `type=company` 인데 `detail` 이 실재 career stem 이 아니면 등록 거부
  - [ ] feature 브랜치에만 있는 본인 커밋이 잡힌다 (mediness 기준 +78건)
  - [ ] tree-hash 중복이 제거된다 (mediness 기준 163건)
  - [ ] 세 identity(`kknaks@medisolveai.com`·`benesia93@naver.com`·`*@*.local`) 커밋이 모두 잡힌다
  - [ ] 미등록 identity 발견 시 Slack 알림이 나가고 조사는 계속된다
  - [ ] 레포 1개 fetch 실패가 나머지를 막지 않고 `last_error` 가 남는다
  - [ ] 같은 날짜로 두 번 조사해도 결과가 동일하다
  - [ ] `counts["commit"]` 과 영역 합계가 다를 수 있음을 테스트가 명시한다
  - [ ] 스케줄러 발동으로 항목이 접수된다
  - [ ] 날짜 지정 백필이 동작한다
  - [ ] 승인 대기 알림이 오고, 2건 이상일 때 재알림된다
  - [ ] `daily`·`career`·`concept` 가 **한 커밋**으로 나간다
  - [ ] 발행 후 `/api/activity`·`/api/career` 가 갱신된다
- **완료 증거**: 미작성

> **구 경로 제거와 스케줄러 교체는 같은 커밋이다.** 이 Phase 안에서도 순서는 지킨다. `inputs.py` 의 두 함수는 유일한 소비자가 `main_job.py` 이고, 스케줄러를 안 바꾼 채 먼저 지우면 백엔드 부팅이 통째로 막힌다(Execution 머리말 ①). 재배치로 노출 구간이 좁아졌을 뿐 결합 자체는 그대로다.

## Pre-deploy Check (**P5 전용**)

P1~P4 는 배포하지 않으므로 해당 없다.

- [ ] `repo-cache` 볼륨이 레포 작업트리 **밖**이다 — back 은 `.:/repo` 로 작업트리를 물고 `REPO_ROOT=/repo` 이므로 컨테이너 내 마운트를 **`/var/cache/repos`** 로 둬 `reset --hard`·`clean -fd` 사정권을 벗어난다
- [ ] `GH_TOKEN_COMPANY` 가 설정돼 있다 (없으면 회사 레포 5개가 조용히 빠지고 `medisolve-ai` career 가 갱신되지 않는다)
- [ ] 디스크 여유가 321MB 이상이다
- [ ] 워커 `:ro` 마운트가 그대로다 — 클론 볼륨을 워커에 붙이지 않았다
- [ ] `WORKER_CONCURRENCY` 가 실운영 값(1)으로 반영됐다 — **기본값은 2 다.** `CONCURRENCY: "2"` 는 워커 서비스 env 이고 유튜브 캡처가 쓰는 값이라, `${WORKER_CONCURRENCY:-2}` 로 두고 서버 `.env` 에서만 1로 내린다. 기본값을 1로 바꾸면 기존 동작이 바뀐다
- [ ] 예산(`worker_budget_usd=5.0` / `global_budget_usd=20.0`) 안에서 하루치가 끝난다
- [ ] 회사 레포 diff 가 프롬프트로 나가는 것을 알고 있다 (조사 균일·공개 통제는 게이트)
- [ ] 구 잔디 잡이 이중 실행되지 않는다 — 스케줄러에 옛 경로가 남아 있지 않다
- [ ] 구 잔디 경로 제거와 스케줄러 교체가 **같은 배포**에 들어 있다

## Rollback

**P1~P4 는 배포되지 않는다.** 되돌릴 것이 코드뿐이고, 그 구간 내내 구 잔디 잡이 그대로 돈다 — 잔디에 구멍이 나지 않는다. 실질적인 롤백 대상은 P5 하나다.

- **P1**: 템플릿 두 장과 `agent.md` 항목을 되돌린다. 코드 영향 0
- **P2**: `definitions.py` 에서 `DAILY_COMMIT` 등록을 해제한다. 준비부 일반화는 유튜브 경로를 1:1 로 감싼 것이라 되돌릴 이유가 없다 — 되돌리면 정의와 코드가 다시 어긋난다. 큐에 남은 `daily_commit` 항목은 폐기 처리
- **P3**: `ALLOWED_PREFIXES`·`upsert` 를 되돌리면 잔디 발행만 막히고 유튜브 경로는 무영향
- **P4**: 화면만 되돌린다. 서버 상태에 영향 없다
- **P5**: 마이그레이션 revert(테이블 drop). 클론 볼륨 삭제. `inputs.py` 의 GitHub API 경로와 스케줄러를 **함께** 되살린다 — 한쪽만 되돌리면 부팅이 막힌다
- 부분 revert 영향: P3 만 되돌리면 게이트는 열리는데 발행이 거부된다. 항목을 폐기하면 정리된다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다
- [ ] SPEC-011·012·013 의 Acceptance Criteria 가 전부 검증됐다
- [ ] SPEC-010 개정분(`upsert` · 그래프 밖 산출물 · 본인작성 보호)이 코드에 반영됐다
- [ ] **더미로 한 바퀴 완주**(P4) — 접수부터 승인·발행까지 끊김 없이 돌고, dry-run 산출물이 작업트리에 남는다
- [ ] **진짜 데이터로 하루치 실발행**(P5) — `daily`·`career`·`concept` 가 한 커밋으로 origin 에 나갔다
- [ ] 구 잔디 경로가 제거되어 이중 실행이 없다
- [ ] 기존 유튜브 파이프라인 회귀 없음
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다

> SPEC-008 개정분의 "route 없는 체인"(`chain.enabled_stages` 일반화)은 **이번 범위 밖**이다. 아래 Open Issue 참조.

## Open Issues

- **`chain.enabled_stages` 일반화는 이번에 하지 않는다.** 지금 필요가 없다 — `next_stage` 는 `after` **다음** 게이트만 훑는데 잔디는 게이트가 `daily` 하나뿐이라 `order[1:]` 이 비고, `enabled_stages` 의 결과는 계산되기만 할 뿐 쓰이지 않은 채 `None`(= 발행 차례)이 돌아온다. 첫 게이트도 `open_first_gate` 가 `pipeline.first_gate()` 로 연다. `enabled_stages` 의 소비자는 `next_stage` 하나뿐이다(테스트 제외). 게다가 발주 당시의 제안 형태(route payload 유무로 판정)는 **두 경우를 뭉갠다** — route 스테이지가 있는데 아직 승인 전(유튜브, 켜지면 안 됨)과 route 스테이지가 애초에 없음(잔디, 켜져야 함). **게이트가 2개 이상인 파이프라인이 생길 때** 필요해지고, 그때의 판정 기준은 payload 유무가 아니라 **파이프라인 정의에 route 스테이지가 있는가** 다. 시그니처가 `enabled_stages(pipeline, route_payload)` 로 바뀌고 `tests/test_pipeline_chain.py` 가 동반 수정된다
- `investigate` **순차 13회의 총 소요와 예산 실측** — `worker_budget_usd=5.0` 안에 드는지. 병렬로 돌리는 선택지는 `WORKER_CONCURRENCY` 와 부딪히므로(실운영 1) 실측 전에는 고르지 않는다. P2 에서 더미로 건수만, P5 에서 실비용
- career 갱신안의 "기존과의 차이" 표시 방식 — 전문 diff 인지 섹션별 요약인지. P4 에서 판단
- 첫 클론을 잡 밖에서 미리 돌릴지 첫 실행이 겪게 할지 — 후자면 첫날 조사가 오래 걸린다. P5
- SPEC-012 OQ-1(daily body 1200자 충분성)은 P5 이후 운영에서 판단한다

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: [[work-016-async-execution-and-progress-ui|KDEV-WORK-016]] (제출/수확 분리 · 드라이버)
