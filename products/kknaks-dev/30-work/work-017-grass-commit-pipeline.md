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
progress: 94
created_at: 2026-07-31
updated_at: 2026-08-03
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
| Progress | 94% (**로컬 하루치를 dry-run 으로 완주했다** (2026-08-02) — 접수부터 발행까지 사람 승인을 포함해 한 바퀴가 실제로 돌았고, 그 과정에서 **결함 9건**을 찾아 고쳤다(⑩은 미수정). 813 passed·FE `tsc` 통과. **남은 6% 는 서버 하나다** — 배포하고 실 push 로 하루치를 완주하는 것. 그 구간이 여전히 미검증인 이유는 토큰·권한·13개 실클론·identity 3종·실비용이 로컬에서 재현되지 않기 때문이다. 이전 서술: **로컬 e2e 로 결함 5건을 찾아 고쳤다** (2026-08-02) — 그중 ①이 `daily` 게이트를 막던 blocker 였다. 798 passed·**전체 green**(⑤가 그 전제를 고쳤다). **눈금이 88 → 90 밖에 안 오른 이유**: 고친 다섯이 전부 "코드가 전부 들어왔다" 던 88% 안에 숨어 있던 것들이라 새 진도가 아니라 **밀린 빚을 갚은 것**이고, 남은 12% 의 정의(배포 + 하루치 실발행)는 그대로다. 다만 그 12% 의 **성격이 나아졌다** — 배포 체크리스트의 미검증 항목 둘(`IDLE_TIMEOUT_SEC`·시드 실행)이 이제 값과 명령까지 확정돼 있다. 이전 서술: **코드가 전부 들어왔다** — P1·P2·P3 done, P4·P5 는 배포에 걸린 검증만 남았다. P5 작업 16 중 14, 786 passed, FE 타입검사·빌드 통과. **남은 12% 가 무엇인지가 이 눈금의 전부다**: 배포와 **하루치 실발행 완주** 하나. WORK-015 의 80%("BE·FE 전부 done, 실전 e2e 만 남음")를 넘어선 근거는 그쪽보다 검증이 촘촘하다는 것이다 — 한 바퀴가 테스트 경로로 완주했고 FE 도 빌드가 섰다. **그럼에도 100 이 아닌 이유는 진짜 GitHub 에서 한 번도 돈 적이 없기 때문이다** — 토큰·권한·13개 실클론·identity 3종·실비용이 전부 미검증이고, WORK-015·016 이 실운영에서 무엇이 더 나왔는지를 기억하면 그 구간을 작게 잡을 수 없다) |
| Branch/PR | `work-017-p2` |
| Blocker | 없음 |
| Next | **커밋 → PR #6 머지 → 배포.** 로컬 완주는 끝났다. 배포 전에 ⑩(career frontmatter 재작성)을 닫을지 정해야 한다 — 서버는 dry-run 이 아니라 그 손실이 `origin/main` 에 커밋된다. 넣을 값은 **넣을 값은 전부 확정돼 있다**(P5 「배포 준비물」) — ① compose 볼륨·env(`REPO_CACHE_DIR`·`GH_TOKEN_COMPANY`, `KNOWN_COMMIT_IDENTITIES` 는 **비운 채로**) ② 마이그레이션 `0007`·`0008` ③ showcase 시드 1회 + company 5개에 `detail=medisolve-ai` ④ 13개 최초 클론(~321MB) ⑤ 하루치 실발행 완주. **⚠ 머지 전까지 `kknaks-back` 재시작 금지** — dev DB 가 `0008` 이라 main 코드로는 부팅이 막힌다 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | doing |
| Design | kknaks | 승인 화면 편집 UX | done — 줄 단위 편집 · **바뀐 줄만 표시 + 기존 본문 접기**로 확정 |
| FE | kknaks | 게이트 화면 (줄/문장 단위 편집) | doing — 작업 전부 들어왔고 **`tsc --noEmit`·`next build` 통과**(`75d2605`). 사람이 눌러 보는 경로만 남았다 |
| BE | kknaks | 준비부 일반화·스테이지·발행부·클론 | **done — 코드 전부.** 남은 것은 배포와 실운영 관측이다 |
| QA | kknaks | 검증과 완료 판단 | doing — 한 바퀴는 테스트 경로로 돌았고 화면 경로가 남았다 |
| Ops | kknaks | 볼륨·env·배포·첫 클론 | todo — **코드 검토 뒤**(사용자 결정 2026-08-01). compose·Dockerfile 은 준비됐다 |

## Scope

포함:

- `templates/persona/daily.md`·`career.md` 신규 + `agent.md` 등록
- **자동 준비부 일반화** — 정의의 `auto` 스테이지를 실제로 읽어 여러 개를 순서대로 돌린다
- `daily_commit` 파이프라인 정의 + `investigate`(fan-out) 자동 스테이지 + `daily` 게이트 작성
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
| `service/pipeline/stages/daily.py` (신규) | **게이트 실행기** — 조사 결과를 daily·career·concept 초안으로 쓴다 — P2. 종전 계획의 `stages/compose.py`(auto)를 대체한다 |
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
| `AITask.kind` 에 새 값(`investigate`·`daily`)을 넣을 수 있다 | `models.py` 가 CHECK 를 안 걸었다. 주석이 그 이유를 밝혀 뒀다 — "스테이지는 정의에서 오므로 CHECK 를 걸지 않는다" |
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
| P2 `daily` 게이트 작성 | P1 의 템플릿 파일 | 형식 SoT 를 읽어 프롬프트를 만든다 |
| P2 나머지 전부 | P2 최선두의 준비부 일반화 | auto 스테이지를 여럿 돌릴 기계가 먼저 있어야 한다 |
| P3 발행부 | P2 의 게이트 산출물 | 승인 payload 형태가 계획 조립 입력이다 |
| P4 완주 | P2+P3 | 더미 한 바퀴는 레일과 발행부가 둘 다 있어야 돈다 |
| P5 진짜 조사 | P2 의 `collect` 자리 | 더미가 계약 전량을 내므로 교체가 그 한 곳에서 끝난다 |

## Internal Interface Contract

`collect` 산출물(= `investigate` 와 `daily` 게이트 작성의 입력)은 SPEC-011 §4 Data Contract 를 따른다. 여기서 다시 적지 않는다.

**스테이지 실행기 계약은 두 갈래다.** 하나로 뭉뚱그리면 auto 스테이지가 승인 리비전을 만들게 된다.

| 갈래 | 해당 스테이지 | 프로토콜 | 산출물 |
|---|---|---|---|
| 게이트 | `daily` | `gates.StageRunner` (`submit`·`poll`·`parse`) 그대로 — WORK-016 이 세운 것이다 | `GateRevision`. `open_gate`/`harvest` 경로를 탄다. **작성이 여기 있다** |
| auto | `collect`·`investigate` | 준비부의 `Summarizer` 계열 (`submit`·`poll`·`parse`·`wait`) | `ItemPreparation` 버전. **`GateRevision` 을 만들지 않는다** |

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
- **설명**: 산출물 작성이 읽을 양식을 먼저 만든다. 코드가 아니라 문서 작업이고, 뒤 Phase 전부의 선행 조건이다. (발주 당시에는 그 읽는 주체를 `compose` auto 스테이지로 적었다 — 지금은 `daily` 게이트다. 아래 Phase 2 참조. **템플릿 자체는 무영향**이다.)
- **작업**:
  - [x] `templates/persona/daily.md` — frontmatter 필드 소유(`counts`=코드), 본문 섹션, 길이 상한 1200자
  - [x] `templates/persona/career.md` — 섹션 5종(`## 담당 영역` 포함), **append 금지·압축 재서술** 규율, 섹션당 5~7줄 상한, `stack` 판정 근거, 사람 전용 필드 격리
  - [x] `agent.md` — "별도 계열" 에 daily·career 등록 (교안과 같은 형태)
- **검증**:
  - [x] 두 템플릿이 존재하고 `agent.md` 에서 도달 가능하다
  - [x] 형식 명세의 SoT 가 템플릿 둘뿐이다 — 작성 스테이지가 여기를 읽는다
  - [x] `bullets` 가 "AI 가 정하지 않는다" 로 명시돼 있다
- **완료 증거**:
  - 커밋 `7155cd2`. `templates/persona/daily.md`·`career.md` 신설, `agent.md` 「별도 계열」에 교안 다음 **셋째 항목**으로 등록.
  - **양식을 상상으로 쓰지 않고 코드에서 읽어 담았다.** 셋을 확인해 템플릿에 넣었다.
  - ① **로더 하드 검증**(`service/persona_loader.py`) — `date` 는 점 표기이고 하이픈으로 바꾼 값이 파일명 stem 과 같아야 한다. `auto: true` 면 `counts` 는 dict, `summary` 는 `null` 이거나 `{ko, en}` 이고 각 값은 `list[str]` 이어야 한다. **어기면 그 파일 하나가 거부되는 데서 끝나지 않는다** — `PersonaError` 가 올라와 persona 로드 **전체**가 실패하고, `reload_data` 가 기존 데이터를 그대로 두므로 사이트는 옛 데이터를 계속 서빙한다. 발행 뒤에야 알게 되는 실패라 나가기 전에 지켜야 한다. 그래서 이 넷을 템플릿에 별도 절로 박았다.
  - ② **5개 섹션은 재직 경력의 양식이다.** `is_current: true` 는 `medisolve-ai` 하나뿐이고, 교육과정 career(`bitcamp`·`likelion`)는 섹션 구조가 아예 다르다(`## 다룬 주제`·`## 프로젝트`). 못박아 두지 않으면 AI 가 남의 문서를 이 양식에 맞추려 든다.
  - ③ **`/api/career` 가 `bullets` 를 내보내지 않는다** — 응답 필드는 `period`·`title`·`org`·`location`·`summary`·`stack`·`is_current`·`body` 여덟이다. "사람 전용" 이 규율일 뿐 아니라 **경력 페이지에 나오지도 않는다**는 사실을 근거로 적었다. 이력서 PDF 전용이라는 것이 코드로 확인된다.

> **`llm.py` 프롬프트 손질을 이 Phase 에서 뺐다.** 발주에는 "프롬프트에 박힌 daily 형식 명세를 템플릿 로드로 전환" 이 있었는데, 그 프롬프트는 구 `main_job` 전용이고 P5 에서 통째로 걷힌다. 곧 지울 코드를 형식에 맞추는 것은 두 번 일하는 것이다. 이중 SoT 는 코드를 고쳐서가 아니라 **구 경로가 사라져서** 해소된다.

### Phase 2 — 파이프라인 레일 + 더미 collect (BE)

- **Status**: DONE
- **설명**: 조사 결과를 게이트에 태운다. 여기서 처음으로 승인 화면에 잔디 항목이 뜬다. **외부 연동은 하나도 하지 않는다** — 조사는 더미가 지어내고, 접수는 기존 `POST /api/admin/queue/items` 를 손으로 부른다. 스케줄러와 Slack 알림 전환은 P5 다. 구 잔디 잡은 그대로 돌게 둔다.

#### 2-A. 자동 준비부 일반화 (**나머지 전부의 선행조건**)

정의에 auto 스테이지를 여럿 적어도 **돌릴 기계가 없었다.** 현행 준비부는 "수집 1회 + 요약 1회" 로 굳어 있다. `definitions.py` 의 `Stage("collect","auto")`·`Stage("summarize","auto")` 가 그 증거다 — 정의는 둘인데 아무도 읽지 않았다.

- **작업**:
  - [x] `driver._finish_preparing` — 수확 뒤 "다음 auto 스테이지가 남았나" 분기. 남으면 제출하고 `preparing` 을 유지한 채 `True` 를 반환한다(기존 `MAX_STEPS` 루프가 다시 돈다). 없으면 `in_review` + 첫 게이트
  - [x] 파이프라인 정의의 `kind="auto"` 스테이지를 실제로 읽는다
  - [x] `runtime.register()` 에 auto 스테이지 실행기를 **이름으로** 등록
  - [x] ~~`prepare.py` — 재료 수집을 스테이지 안으로 넣어 `if item.source_url:` 전제를 푼다~~ → **불필요 판정.** 잔디는 그 전제를 아예 타지 않는다 (아래 「판정 둘」)
  - [x] 첫 게이트 러너 하드코딩 제거 — `driver.py`·`queue.py` **두 곳** 모두 `pipeline.first_gate()` 기반으로
  - [x] `ItemPreparation.payload` 에 어느 auto 스테이지 결과인지 기록 (+ 스테이지 사이 **누적**까지)
  - [x] `investigate` fan-out 저장 — `ai_task_id` 를 비우고 `AITask.item_id` 로 N 건을 찾는다. `_running_preparation_ref` 의 단건 `with_for_update` 를 N 건 대응으로 바꾼다
  - [x] 유튜브 회귀 방지 — 등록된 auto 실행기가 있으면 그쪽이 이기고, 없으면 레거시 준비부가 덮는다. **감싸기 자체는 의도적 보류**다 (아래 「판정 둘」)
- **검증**:
  - [x] 유튜브 준비 흐름에 회귀가 없다
  - [x] `daily_commit` 이 auto 스테이지를 정의 순서대로 지난다 (착수 시점 3개 → 현재 2개, `1f690fb` 이후)
  - [x] 첫 게이트가 정의에서 결정된다 (유튜브=`route`, 잔디=`daily`)

> **fan-out 저장 방식은 Open Issue 가 아니라 여기서 정한다.** `_running_preparation_ref` 와 `harvest_preparation` 이 running 준비 **1건**을 `with_for_update` 로 잡고 있어서, 어느 형태를 고르든 그 두 함수를 고쳐야 한다. 열어 두면 중반에 구조가 흔들린다. 이 결정이 "조사 중 (3/13)" 진행 표시(SPEC-013 U-1)와 부분 실패 처리의 전제이기도 하다.

#### 2-B. 잔디 파이프라인

- **작업**:
  - [x] `definitions.py` — `DAILY_COMMIT` 등록 (`collect`·`investigate` auto + `daily` gate)
  - [x] **더미 `collect`** — SPEC-011 §4 계약 전량을 지어낸다 (아래 「더미 경계」)
  - [x] `investigate` 스테이지 — 레포별 N 건 제출·수확, 결과를 `ItemPreparation` payload 에 누적
  - [x] 부분 실패 처리 — 일부 실패는 진행, 전부 실패면 스테이지 실패
  - [x] **`daily` 게이트 작성** — 템플릿 로드 + daily·career·concept 초안, `changed:false` 지원. **종전 계획의 `compose` auto 스테이지를 대체한다** (커밋 `d5bb3cd` 작성 로직 → `1f690fb` 게이트로 이전)
  - [x] career 결정적 skip (귀속 커밋 0이면 스테이지 미생성)
  - [x] `runtime` 등록 — `slack_bridge/bootstrap.py` 가 auto 둘 + 게이트 `daily` 를 실제로 배선한다
  - [x] `intake()` 시그니처 확장 + `normalized_url="daily:{date}"` 합성 키 — **쓰는 쪽까지 닫혔다.** `intake_daily()` 가 키를 만들어 넣고, `collect_dummy.target_date()` 가 그것을 판다
  - [x] `auto:false` 접수 전 차단 — `user_authored()` 가 대상 daily 를 읽고 `auto: true` 가 아니면 접수 자체를 하지 않는다
  - [x] **미래 날짜 접수 전 차단** — 발주 작업 목록에 없던 항목이다. 근거는 SPEC-013 §4 「접수 날짜」가 이미 "미지정이면 어제(KST). **지정 시 미래 날짜 불가**" 로 계약해 두고 있었다는 것이다. 백필이 날짜를 받는 순간 그 계약에 걸리는 입력이 생기므로 진입점과 같은 커밋에 들어가는 것이 맞다. 차단 방식도 나머지 둘과 같다 — 항목을 만들고 실패시키는 게 아니라 **만들지 않는다**
  - [~] 활동 0 접수 전 차단 — **여전히 부분이다.** `collect` 의 `NO_ACTIVITY` 로 접수 **후** 막는다. 근거와 남는 차이는 아래 완료 증거와 Open Issue
- **검증**:
  - [x] 수동 접수로 항목이 들어오고 요청이 AI 를 기다리지 않는다 — 접수는 행 하나를 만들고 끝난다(조사도 AI 호출도 하지 않고 드라이버가 이어 민다)
  - [x] `investigate` 가 레포 수만큼 돌고 부분 실패해도 게이트가 열린다
  - [x] 전 레포 실패 시 스테이지 실패로 닫히고 재시도가 열린다
  - [x] 게이트가 **하나**만 열린다
  - [x] `type=studio` 만 커밋한 날은 career 초안이 없다
  - [x] `is_current` 아닌 career 는 대상에서 빠진다
  - [x] 같은 날짜로 두 번 접수하면 항목이 하나다 — 둘째가 `joined` 로 합류하고 큐 행은 하나다
  - [x] **기존 유튜브 파이프라인이 회귀 없이 동작한다**

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
  - 커밋 `de4d7a3` — **레일이 실제로 돈다.** 637 → **642 passed**(신규 5). 골격 위에 제출·수확·전진을 얹어 잔디 항목이 `collect`→`investigate`→`compose` 를 정의 순서로 지나 `daily` 게이트까지 간다.
    - 분기는 `_finish_preparing` 이 아니라 **`_finish_auto_stage`** 로 들어갔고 **삼값 반환**이다 — "다음이 남았다"·"게이트 차례다" 에 더해 **"내 것이 아니다"(레거시 준비)를 `None` 으로 구분**한다. 두 값으로 두면 레거시 경로를 auto 경로가 삼킨다.
    - 순서에 대한 지식은 `flow.advance_auto_stages` 가 갖는다 — `prepare` 도 `gates` 도 아니다.
    - **auto 레지스트리를 게이트 레지스트리와 나눴다.** 계약이 다르고(auto 는 `GateRevision` 을 만들지 않는다) 이름이 겹칠 수 있다 — 유튜브의 `collect` 와 잔디의 `collect` 는 같은 이름이지만 하는 일이 다르다.
    - payload 는 기록에 더해 **스테이지 사이 누적**까지 넣었다. `latest_preparation` 이 최근 성공분 **하나만** 집으므로, 누적하지 않으면 앞 산출물이 게이트 입력에서 사라진다.
    - fan-out 은 `ai_task_id` 를 비우고 `AITask.item_id`+`kind` 로 되찾는다 — 단일 FK 로는 N 건을 가리킬 수 없다.
    - **앞 커밋의 637 passed 는 증거가 아니었다.** 새 경로를 아무도 밟지 않아 `update` import 누락이 그대로 숨어 있었다. `FakeAutoStage` 로 스테이지 순서·payload 누적·fan-out 3건·부분 실패·전부 실패를 각각 태워서야 드러났다.
  - 커밋 `741d176` — **더미 `collect`.** 642 → **666 passed**(신규 24). `service/pipeline/collect_dummy.py`. SPEC-011 §4 계약 **7키 전부**, 시나리오 **7종**(`normal`·`studio_only`·`career_unchanged`·`partial_failure`·`all_failed`·`truncated`·`empty`)을 메모의 `scenario:<이름>` 으로 고른다 — P2 에는 스케줄러가 없어 접수가 곧 사람의 조작이다.
    - **지어내는 것은 `commits[]` 뿐이다.** 영역 분해·`counts` 산출·career 귀속은 진짜 코드다 → P5 는 "git 을 읽어 `commits[]` 를 만드는" 한 곳만 갈아 끼운다.
    - 한 커밋이 여러 영역에 걸치면 영역마다 계상한다 → `counts["commit"]` 과 영역 합계는 **일치하지 않는다**(테스트가 이 사실을 박아 뒀다). `counts` 는 코드가 센다.
    - career 귀속은 `type=company` 만 간다. 대상이 실재해야 해서 `medisolve-ai` 하나로 모인다(`is_current: true` 가 그것뿐).
    - `collect` 는 제출 0건이라 **`AITask` 가 생기지 않는다** — 조사는 생성이 아니라 읽는 일이고 P5 에서 진짜가 되어도 그 성질은 그대로다. 활동 0(`empty`)은 `NO_ACTIVITY` 로 스테이지를 막는다.
  - 커밋 `b1a2642` — **`investigate` 스테이지 + 수확 계약 정정.** 666 → **678 passed**(신규 12). 레포마다 하나씩 제출한다 — 하루치 diff 를 한 프롬프트에 몰아넣으면 레포 하나가 다른 레포의 서술을 밀어내고, 레포 하나 때문에 그날 조사 **전체**가 날아간다. 여기서 만드는 것은 문서가 아니라 `compose` 가 읽을 **재료**라 `templates/persona/` 를 참조하지 않는다. 회사·개인 레포도 구분하지 않는다 — 조사 깊이는 균일하고 공개 통제는 게이트가 한다. 빠진 레포와 빈 조사문은 `missing` 으로 들고 간다(성공으로 넘기면 `compose` 가 근거 없이 서술한다).
  - 커밋 `d5bb3cd` — **작성 로직.** 678 → **699 passed**(신규 21). 당시에는 `stages/compose.py`(auto)였다 — **이 로직은 `1f690fb` 에서 그대로 `daily` 게이트로 옮겨 갔다**(아래). `service/content_format.py` 로더는 그대로다.
    - **P1 의 형식 SoT 가 여기서 실제로 읽힌다.** `templates/persona/daily.md`·`career.md` 를 실어 프롬프트를 만들고, 테스트가 마커 문자열로 "프롬프트에 **복사돼 있지 않다**"를 검증한다(`test_format_is_loaded_from_templates_not_copied`). **P1 검증 2번("형식 명세의 SoT 가 템플릿 둘뿐이다")이 이제 코드로 증명됐다.** 로더를 교안 모듈(`content_format`)에 얹은 것은 같은 걱정거리이고 같은 캐시를 쓰기 때문이다 — 닮은 모듈을 하나 더 만들 이유가 없다.
    - `counts` 는 **코드가 주입한다** — AI 출력의 숫자는 버린다. 본문 하드 상한 초과는 자르고, 빈 `summary` 줄은 걸러낸다(활동 0 인 카테고리에 빈 줄이 오면 잔디 셀 카드에 그대로 뜬다).
    - career 는 **제출 시점에 대상 목록을 박아** 두고 모델이 대상 밖 career 를 내면 수확이 버린다. **전문 교체**라 기존 본문을 프롬프트에 함께 넣는다 — 안 주면 모델이 append 할 수밖에 없고 career 가 daily 의 복사본이 된다.
    - `summary` 모양(`{ko,en} list[str]`)을 여기서 막는다. 로더가 하드 검증하므로 통과시키면 **발행 뒤 persona 로드 전체**가 실패한다.
  - 커밋 `f36df6d` — **실배선.** 699 passed(신규 0 — 배선만). `slack_bridge/bootstrap.py` 가 `auto_stages={collect, investigate, compose}` 를 등록한다. 그전까지 셋은 존재만 하고 아무도 부르지 않았다. `collect` 는 LLM 을 안 불러 클라이언트조차 없다 — 레지스트리를 나눠 둔 것이 여기서 값을 한다.
  - 커밋 `1f690fb` — **작성 주체를 `daily` 게이트로 옮겼다. 발주 계획의 `compose` auto 스테이지를 없앤다.** 699 → **702 passed**. `stages/compose.py`(278줄) 삭제 → `stages/daily.py`(`DailyStage`), `tests/test_pipeline_compose.py` → `test_pipeline_daily.py`, `definitions.py` 의 `DAILY_COMMIT` auto 가 셋 → 둘, `bootstrap.py` 가 `daily` 를 게이트 실행기로 등록.

    **왜 되돌렸나 — 재생성이 작성 주체를 강제한다.** 발주는 `compose`(auto)가 초안을 만들고 게이트는 보여 주기만 하는 모양이었다. 그런데 SPEC-013 S-3 이 "재생성은 조사를 다시 돌리지 않는다. 원문이 바뀐 게 아니라 서술이 마음에 안 든 것이다" 로 정해 두었다. **즉 재생성이 다시 만드는 것은 서술이고, 그 일을 하는 주체는 게이트일 수밖에 없다.** 게이트가 작성 능력을 갖는 순간 `compose` 의 작성은 **첫 회에만 쓰이고** 재생성마다 게이트가 다시 만드는 중복이 된다 — 매일 LLM 호출 하나를 버리는 셈이다. 세 번째 근거는 대칭이다: 유튜브의 `summarize`(auto)도 route 판단 **재료**만 만들고 노트 작성은 게이트 스테이지(`source_note`·`concept`·`derived`)가 한다. 잔디에서 `compose` 가 작성까지 하면 같은 레일 위에 두 규율이 생긴다.
    - **버려진 코드는 없다.** `d5bb3cd` 가 쓴 작성 로직(형식 SoT 로드·`counts` 코드 주입·`summary` 모양 검증·career 전문 교체)은 그대로 `DailyStage` 로 옮겨 갔다. 바뀐 것은 **어느 프로토콜을 구현하느냐**다 — `AutoStage`(`submit`/`wait`/`parse`, `ItemPreparation` 산출)에서 `AgentStage`(`prompt`/`payload`/`parse`, `GateRevision` 산출)로.
    - **옮기면서 게이트 계약에 맞춰 둘을 고쳤다.** ① **career 대상 목록을 저장하지 않고 제출·수확 양쪽에서 다시 계산한다**(`career_targets()`). 입력이 같으면 결과가 같으므로 저장할 이유가 없고, 제출 시점 값을 붙잡아 두면 back 재시작 뒤 수확이 다른 판단을 한다 — `AgentStage` 가 경고하는 함정이다. ② **`target_path` 를 시스템이 조립해 payload 에 담는다.** 경로를 모델에 맡기면 allowlist 밖으로 쓰는 계획이 나온다. 기존 노트 게이트와 같은 규율이고, **P3 발행부의 입력 형태가 이로써 확정됐다.**
    - **체인 계약은 변하지 않았다.** 게이트는 여전히 `daily` 하나이므로 "승인이 곧 체인 종료이자 발행 트리거"가 그대로다. 준비부 일반화(2-A)도 무영향 — auto 스테이지 개수는 정의에서 읽으므로 셋이 둘이 되어도 코드가 바뀌지 않는다.
    - **SPEC 환류 완료**: SPEC-013 v0.0.2(§1 Meta·§2 Placement/U-1·§3 S-1/S-3·§4 Flow/State·§5·§6). 개정 이유를 스펙 본문 머리에 남겼다. **SPEC-011·012 는 무영향** — `collect`·`investigate` 계약과 문서 형식이 그대로다.

  **판정 둘 — 안 한 것과 그 근거.**

  - **수집 전제 해제(`if item.source_url:`)는 불필요로 판정했다.** 더미 `collect` 가 자기 `AutoStage` 실행기라 `item.source_url` 을 **아예 타지 않는다**. 그 전제는 레거시 유튜브 준비부 안에만 남아 있고(`prepare.py:449`) 유튜브는 그 경로를 계속 쓴다. 목적은 전제를 푸는 것이 아니라 **잔디가 그 전제에 걸리지 않는 것**이었고, 그건 달성됐다.
  - **유튜브 준비부 감싸기는 의도적으로 열어 뒀다.** 레거시 준비부는 `AITask` 를 `summarize.submit` **앞에서** 만든다. 그 순서가 "제출이 터져도 기록이 남는다"는 계약이고 `tests/test_pipeline_intake.py::test_summarize_failure_keeps_task_row` 가 검증한다. 감싸면 그 순서를 깨야 한다 — 새 레일은 실행기가 제출을 내부에서 하므로 **몇 건이 나올지 미리 몰라** 행을 먼저 만들 수 없다. 얻는 것 없이 실패 기록 계약만 흔들린다. 대신 **등록된 auto 실행기가 있으면 그쪽이 이기고 없으면 레거시가 덮는** 구조라 잔디는 막히지 않는다.

  **수확 계약 결함 둘 — 앞선 커밋의 레일에서 찾아 `b1a2642` 에서 고쳤다.** 둘 다 그때까지 테스트가 **통과하고 있었다.**

  1. `parse` 가 성공분만 **순서 있는 리스트**로 받았다. 부분 실패로 한 건이 빠지면 색인이 밀려 **A 레포 조사문이 B 레포 것으로** 읽힌다. `task_ref` 로 키를 잡는 dict 으로 바꿨고, 어느 레포가 빠졌는지는 `submit` 이 남긴 대응표와 맞춰 알아낸다.
  2. 수확이 `payload["failures"]` 에 **실행** 실패를 썼다. 그 키는 SPEC-011 §4 에서 **레포 fetch 실패**의 자리라 `collect` 산출물을 덮는다. `stage_failures` 로 분리했다.

  **왜 안 잡혔나.** 부분 실패 경로에서 결과를 **레포와 대조하는** 단언이 없었다(개수만 셌다). 그리고 `collect` 산출물과 수확 결과가 **같은 payload 에서 만나는 지점**을 아무도 태우지 않았다. 둘 다 이번에 테스트로 덮었다(`test_partial_failure_does_not_shift_results`·`test_results_map_to_the_right_repo`·`test_payload_accumulates_across_stages`). ✅ **SPEC 환류 완료(2026-08-01)** — "결과를 어느 레포에 붙이는가"가 SPEC-013 v0.0.2 §4 「Data Contract — `investigate` 결과 귀속」에 계약으로 들어갔다. Open Issues 참조.

  - 커밋 `dac6ad9` — **접수 진입점. 이것으로 P2 가 닫힌다.** 702 → **717 passed**(신규 15). 신설 `service/pipeline/daily_intake.py`, `intake()` 에 `normalized_key` 인자 하나.
    - **날짜가 항목을 가른다.** 자료를 정리하는 유튜브와 달리 잔디는 하루가 단위라 중복 축이 URL 이 아니라 날짜다. `normalized_url` 에 `daily:{date}` 합성 키를 넣어 **기존 중복 판정을 그대로 쓴다** — 컬럼도 인덱스도 늘지 않는다. 발주서 「`intake()` 는 시그니처가 늘어난다」 절이 예측한 그대로이고, `uq_queue_items_pending_url` 부분 유니크 인덱스가 마이그레이션 없이 하루 한 항목을 **DB 에서** 강제한다. 이미 발행된 날짜를 다시 접수하면 그 인덱스에 안 걸리고 `duplicate_published` 로 떨어지는데, 그것이 SPEC-013 S-7 3항(자동으로 막지 않고 사람에게 물어본다)이 요구하는 동작이다.
    - **막는 것은 항목을 만들고 실패시키지 않는다.** `DailyIntakeResult.outcome` 에 `blocked` 를 따로 둔 이유가 그것이다 — 본인이 쓴 날은 만들지 않는 것이 **정상 동작**이고 미래 날짜는 사람의 오타다. 둘 다 재시도할 것이 없으므로 `prepare_failed` 행을 남기면 큐에 치울 쓰레기만 쌓인다.
    - **`auto: true` 가 아니면 사람 것으로 본다.** `auto` 키가 아예 없는 옛 파일도 사람 소유다. 판정을 뒤집어 "명시적으로 `auto: false` 인 것만 사람 것" 으로 두면 키가 없는 과거 daily 를 잔디가 덮어쓴다. **자동 생성분만 명시적으로 표시되므로** 사람 쪽을 기본값으로 두는 것이 안전하다. 파일을 읽지 못하는 경우도 사람 작성으로 판정한다 — 읽을 수 없는 파일을 덮어쓰는 것보다 하루를 건너뛰는 편이 싸다.
    - **활동 0 은 여기서 막지 않았다 — 의도한 판단이고, 남는 차이가 있다.** 활동 여부는 조사를 해 봐야 알고 조사는 `collect` 의 일이다. 접수 시점에 한 번 더 조사하면 **P5 에서 같은 git 작업을 하루에 두 번** 하게 된다(bare 클론 13개를 두 번 훑는다). 그래서 `collect` 의 `NO_ACTIVITY` 로 준비를 닫는 쪽을 골랐다. 결과적으로 발행되지는 않지만 **항목 행 하나가 남는다** — SPEC-013 §4 Flow 의 "항목 생성(활동 0이면 없음)"·State 의 `received: 접수 (활동>0)` 과 다르다. 스펙을 코드에 맞출지 코드를 스펙에 맞출지는 **Open Issue 로 세우고 P5 착수 전에 못박는다.**
    - **백필 테스트가 `2026-07-29` 를 쓴다 — 지어낸 날짜가 아니다.** 그날이 실제로 비어 있다. 서버가 09:05 발동을 놓쳐 daily 가 만들어지지 않았고, 구 잔디 잡에는 되살릴 경로가 없었다. **이 진입점이 그 첫 사용처다** — 백필을 "있으면 좋은 것" 이 아니라 이미 생긴 구멍을 메우는 기능으로 넣었다.
    - **아직 HTTP 로는 날짜를 지정할 수 없다.** `intake_daily()` 의 호출자는 테스트뿐이고, `POST /api/admin/queue/items` 는 날짜 파라미터를 받지 않는다. 이는 미완이 아니라 **발주서 Code Surface 의 배치 그대로**다 — `api/routers/queue.py` 접수 날짜 파라미터와 `scheduler.py` 접수 호출은 둘 다 P5 다. P2 의 수동 완주는 기존 엔드포인트에 `source_kind=daily_commit` + `note=scenario:<이름>` 으로 넣고 날짜는 기본값(어제 KST)에 맡기는 경로로 돈다.

  **Phase 2 를 `DONE` 으로 올린 근거.** 2-A·2-B 의 작업 항목이 전부 닫혔고, P2 의 검증 방법은 애초에 **수동 접수**다(Phase 설명: "접수는 기존 `POST /api/admin/queue/items` 를 손으로 부른다"). 스케줄러 연결·API 날짜 파라미터는 발주 시점부터 P5 이므로 그것이 없다고 P2 가 열려 있는 것이 아니다. 남은 차이 하나(활동 0 차단 위치)는 **미착수 작업이 아니라 스펙과 구현의 계약 차이**라 Phase 가 아니라 Open Issue 가 들 자리다.

### Phase 3 — 발행부 확장 (BE)

- **Status**: DONE
- **설명**: 승인된 것이 실제로 파일이 되게 한다. P2 와 병렬 착수 가능하지만 e2e 는 P2 완료 후다.
- **작업**:
  - [x] `plan.py` — `ALLOWED_PREFIXES` 에 `persona/daily/`·`persona/career/`
  - [x] `LAYER_PREFIX` 에 `daily`·`career`
  - [x] `build_actions()` 에 daily·career 분기
  - [x] `upsert` 액션 신설 — 존재 검사도 stale 검사도 받지 않는다 (아래 완료 증거 — `stale 대상` 유지는 **career 쪽에서만** 성립한다)
  - [x] `graph_check` — `daily`·`career` 제외 (`concept` 는 유지)
  - [x] 본인 작성 보호 검증 (`USER_AUTHORED_DAILY`)
  - [x] 사람 전용 필드 검증 (`PROTECTED_FIELD`)
  - [x] 잔디 발행을 `publish_atomic` 으로 — **별도 작업이 없었다.** 아래 「자동 달성」
- **검증**:
  - [x] `persona/daily/`·`persona/career/` 가 발행 허용된다
  - [x] 같은 날 두 번 승인해도 `upsert` 로 통과한다 (`ALREADY_EXISTS` 없음)
  - [x] daily·career 가 그래프 검증에서 빠지고 concept 는 검증을 받는다
  - [x] 대상 daily 가 본인 작성이면 거부된다 — `auto: false` 와 **`auto` 키 없음**을 각각 태운다
  - [x] ~~계획에 `bullets`·`period` 가 있으면 거부된다~~ → **검증이 아니라 구조로 막았다.** 갱신안이 본문만 내고 발행부가 기존 frontmatter 를 그대로 이므로 그 필드가 계획에 **들어올 자리가 없다.** 남은 `PROTECTED_FIELD` 검증은 반대 방향을 본다 — 필수 필드(`type`·`period`·`title`·`org`)가 **사라졌으면** 거부한다. 아래 완료 증거
  - [x] push 실패 시 로컬 커밋이 남지 않는다 — `publish_atomic` 계약이고 WORK-015 가 이미 태워 뒀다. 잔디가 그 경로로 들어왔으므로 그대로 상속된다
  - [x] 발행 재시도가 AI 를 다시 부르지 않는다 — 저장된 계획 재사용(DEC-012 D5). 같은 상속
  - [x] 유튜브 발행이 회귀 없이 동작한다 — 발행부 기존 테스트 전량 통과(737 passed)
  - [x] **`dry_run` 이 어디까지 하는지가 테스트로 박혀 있다** — 파일은 써지고 커밋만 생략된다. `apply_item(dry_run=True)` 로 태워 **파일 존재 + HEAD 불변 + `status=published`** 를 함께 단언한다. 계약이 파이프라인과 무관하므로 잔디 산출물로 다시 태울 필요는 없고, 잔디로 실제 관측하는 것은 P4 완주다
- **완료 증거**:
  - 커밋 `2af347f`. 717 → **737 passed**(신규 20). `service/apply/plan.py`(+190) · `graph_check.py` · `executor.py` 한 줄 · `tests/test_apply_grass.py` 신설(266줄).

  - **`publish_atomic` 전환은 자동 달성이다 — 별도 작업이 없었다.** 발주는 이것을 P3 작업 항목으로 잡았지만, `apply_item()` 이 파이프라인을 가리지 않고 `publish_atomic` 하나만 부르는 구조다. 잔디가 apply 경로를 타는 순간 그리로 들어갔다. `commit_and_push_with_retry` 는 예정대로 남아 있고 소비자가 `pdf_generate`·`content_enrich`·`algorithms` 셋이다. **`main_job.py` 의 호출부(구 잔디 잡)는 P5 에서 걷힌다** — 지금 지우면 부팅이 막힌다.

  - **`upsert` 를 신설한 이유는 daily 가 존재 여부로 판단할 수 없는 문서이기 때문이다.** 첫 회 생성과 이후 덮어쓰기가 **둘 다 정상**이라, `create`/`replace` 만으로는 매일 액션 종류가 갈리고 그러면 "오늘은 create 인가 replace 인가" 를 발행부가 미리 알아야 한다. 그래서 `upsert` 는 존재 검사(`ALREADY_EXISTS`·`STEM_TAKEN`)도 stale 검사(`TARGET_MISSING`)도 받지 않는다. 경로 허용·층 정합·본인 작성 보호는 그 앞에서 이미 본다.
    - **career 만 `replace` 로 남겼다.** 같은 잔디 산출물인데 액션이 다른 이유는 성격이 다르기 때문이다 — career 는 **이미 있는 문서를 고치는 것**이라 대상이 사라졌으면 막혀야 한다. 초안 작성과 발행 사이에 파일이 없어졌다면 그건 사람이 지운 것이고, 그 위에 새로 쓰면 사람이 지운 결정을 조용히 되돌린다. `TARGET_MISSING` 이 그 자리다.
    - concept 는 기존 규율 그대로다 — `mode=supplement` 면 `replace`, 아니면 `create`.

  - **frontmatter 를 시스템이 조립한다 — 이 Phase 의 핵심 설계 판단이다.** 다른 노트 스테이지는 AI 가 md **전문**을 낸다. 그것이 규율이었다: 형식 SoT 를 렌더러와 템플릿 **둘로 만들지 않겠다**는 것. daily·career 는 그럴 수 없어서 예외를 냈고, 예외를 낸 자리마다 근거가 다르다.
    - **daily** — `type`·`date`·`auto` 는 시스템 것이고 `counts` 는 **코드가 센 값**이라 AI 출력에 섞이면 안 된다(SPEC-012 §5 「`counts` 는 코드가 센다」). 그래서 `render_daily()` 가 frontmatter 를 짓는다. **형식 SoT 가 둘이 되지는 않는다** — AI 가 내는 `summary` 와 본문은 조립되는 값이 아니라 **그대로 실린다.** 시스템이 정하는 것은 소유가 시스템인 필드뿐이고, 형식이 걸린 부분은 여전히 템플릿 한 곳에서만 온다.
    - **`daily` 의 `date` 는 점 표기다.** 파일명은 하이픈(`2026-08-01.md`)이고 frontmatter 는 `2026.08.01` 이다. `service/persona_loader.py` 가 둘을 대조하며, 어긋나면 **그 파일 하나가 거부되는 데서 끝나지 않는다** — `PersonaError` 가 올라와 persona 로드 **전체**가 실패하고 `reload_data` 가 기존 데이터를 그대로 두므로 사이트는 옛 데이터를 계속 서빙한다. 발행 뒤에야 알게 되는 실패라 렌더러가 표기를 바꾸는 자리에 못박아 뒀고, 테스트도 이 한 가지를 따로 태운다.
    - **career 는 기존 frontmatter 를 그대로 이고 본문만 바꾼다.** 갱신안이 왜 본문만 내는지가 여기서 설명된다 — career frontmatter 는 `bullets`·`period` 처럼 **사람 전용 필드가 대부분**이라, 전문을 받으면 모델이 그것들을 다시 쓰게 된다. 본문만 받아 얹으면 사람 전용 필드는 **건드릴 방법 자체가 없다.** 검증으로 막기 전에 **구조로 막았다는 것이 요점**이고, 그래서 위 검증 항목이 "`bullets` 가 있으면 거부" 에서 "필수 필드가 사라졌으면 거부" 로 뒤집혔다. 남긴 `PROTECTED_FIELD` 검증은 정상 경로에서 걸릴 일이 없지만 **계획 조립 경로가 하나뿐이라고 가정하지 않기 위해** 둔다 — 저장된 계획으로 재시도하는 경로가 있고 그 계획이 다른 코드로 만들어졌을 수 있다. 파일을 쓰기 전이 마지막 기회다. (`repo_root` 없이 계획을 조립하면 기존 본문을 못 읽어 frontmatter 가 통째로 비는데, 이 검증이 그것도 같이 잡는다.)

  - **그래프 검증 제외는 예외 처리가 아니라 사실의 반영이다.** `daily`·`career` 는 **상류 참조가 없어 `up:` 을 갖지 않는다.** 그런 노드를 그래프에 얹으면 L2(고아) 같은 규칙에 걸려 발행이 막힌다 — 즉 얹는 쪽이 사실과 다르고, 빼는 것이 원래 자리다. `OUTSIDE_GRAPH` 를 `plan.py` 에 두고 `graph_check` 가 그것으로 거른 것도 같은 이유다: 층 목록의 SoT 가 `LAYER_PREFIX` 옆에 있어야 새 층을 넣을 때 한 곳만 본다.
    - 같은 발행에 섞인 `concept` 는 **그대로 검증을 받는다.** 잔디가 만든 개념도 유튜브가 만든 것과 같은 계보 규율을 지켜야 한다(SPEC-012 §5). 테스트가 "daily·career 는 가상 노드로 올라가지 않는다" 와 "같은 계획의 concept 는 검증을 받는다" 를 각각 태운다.

  - **보호 검증 둘은 자리가 다르다.**
    - `USER_AUTHORED_DAILY` — **이중이다.** 접수(`intake_daily`)가 한 번 막고 발행이 한 번 더 막는다. 중복이 아니라 **접수와 발행 사이 몇 시간의 경합**을 잡는 자리다. 그 사이에 사람이 그날 daily 를 직접 쓰는 일이 실제로 일어날 수 있고, 접수만으로는 그것을 못 본다. SPEC-012 §5 「본인 작성 보호는 이중이다」가 이로써 코드에 들어왔다.
    - `PROTECTED_FIELD` — 위의 career 절 참조.

> **`dry_run` 의 사실관계를 여기서 못박는다.** `apply_item(dry_run=True)`·`publish_atomic(dry_run=True)` 는 둘 다 **기본값**이고, dry-run 이어도 `_write_all` 이 먼저 돌아 **파일은 작업트리에 실제로 써진다.** 생략되는 것은 커밋과 push 뿐이다. `item.status` 는 `published` 가 되고 `commit_ref` 는 `None` 이다.
>
> 이 사실이 P4 완주의 관측 방법을 정한다. "발행됐다" 를 커밋 로그로 확인할 수 없고 **작업트리를 봐야 한다.**

### Phase 4 — 게이트 화면 + 더미 한 바퀴 완주 (FE/QA)

- **Status**: IN_PROGRESS — 작업 다섯이 전부 들어왔고 타입·빌드가 섰다. **사람이 눌러 보는 검증 셋만 남았고 그건 배포 뒤(P5)다.**
- **설명**: 사람이 실제로 승인할 수 있어야 한 바퀴다. 배포도 실발행도 하지 않는다 — 그건 P5 다. 여기서 확인하는 것은 **파이프라인이 끝에서 끝까지 돈다**는 것 하나다.

> **「한 바퀴 완주」가 무엇을 뜻하는지를 여기서 못박는다 — 두 갈래였다.** ① **테스트로 완주**(접수부터 발행까지를 한 경로로 태우고 파일이 실제로 써지는 것을 관측) 인지, ② **떠 있는 서버에서 사람이 화면으로 완주**인지. **①은 달성됐고 ②는 P4 에서 달성할 수 없다.** 떠 있는 서버는 origin 미러의 코드를 쓰므로 화면을 띄운 완주는 **배포가 선행돼야 하고 배포는 P5 하나뿐이다**(Execution 머리말 ③ 「배포가 P5 한 번뿐이다」). 즉 ②를 P4 의 완료 조건으로 두면 P4 가 P5 에 의존하게 되어 Phase 순서가 뒤집힌다.
>
> 그래서 **P4 의 완주 조건은 ①로 확정한다.** 사람이 화면으로 도는 완주는 P5 의 「하루치 실발행 완주」가 흡수한다 — 실발행은 어차피 사람이 화면에서 승인해야 일어나므로 별도 항목을 세울 이유가 없다. **다만 이 확정이 화면을 면제해 주지는 않는다** — 화면 코드가 한 번도 돌지 않은 채로 P5 에 넘기면 실발행 당일에 FE 를 디버깅하게 된다. 그것이 아래 Status 가 `DONE` 이 아닌 이유다.

- **작업**:
  - [x] 조사 진행 표시 (`investigate` N건 중 진행 수, 실패 레포, 상한 적중) — `75d2605`. **payload 는 AI 쪽이었고 사람이 보는 것은 `parse()` 결과였다**(아래 완료 증거)
  - [x] daily 요약 **줄 단위** 편집·삭제 — `counts` 는 **표시만** 한다(코드가 센 값이라 고칠 수 있으면 안 된다). 본문도 편집 가능
  - [x] career **줄 단위** 승인·제외 토글 + 기존 문서와의 차이 표시 — 발주의 "문장 단위" 를 **줄 단위**로 확정했다(아래 완료 증거)
  - [x] concept 개별 제외 토글 — 기존 `ConceptList` 를 **그대로** 재사용
  - [x] 더미 조사 → 게이트 → 승인 → 발행까지 **한 바퀴 완주** (dry-run) — **테스트 경로로.** 위 머리말 참조
- **검증**:
  - [x] 요약 줄을 지우고 승인하면 지운 결과가 발행된다 — 한 바퀴 테스트가 승인 payload 를 손으로 고쳐 태우고, 발행된 md 에서 그 줄을 찾는다
  - [~] career 줄을 제외하면 파일에 없다 — **서버 쪽은 성립한다**(전문 교체라 화면이 합쳐 보낸 것이 그대로 나간다). 합치는 주체가 화면이므로 **화면 경로는 미검증**
  - [ ] 회사 레포 서술을 덜어낸 결과가 공개 md 에 반영된다 — 위와 같은 이유로 화면 조작이 필요하다
  - [ ] 승인 안 한 날의 잔디 칸이 비어 있다가 나중 승인 시 채워진다 — 사이트가 떠 있어야 본다. **P5 로 넘긴다**
  - [x] **완주 관측**: `persona/daily/{date}.md` 와 `persona/career/{stem}.md` 가 실제로 생성돼 `git status` 에 뜬다. **커밋은 없다** — dry-run 이 커밋과 push 만 생략하기 때문이다
  - [ ] 시나리오 7종이 각각 화면에서 구분돼 보인다 — **타입·빌드는 통과했으나 렌더는 아직**(`75d2605`). 사람이 조작하는 경로라 배포 뒤다
- **완료 증거**:
  - 커밋 넷. `8c2aa7a`(승인 화면) · `2a2483a`(한 바퀴 완주) · `ead2ceb`(concept 규율 통일) · `75d2605`(조사 진행 표시 + FE 첫 실행). 737 → **774 passed**.

  - **커밋 `8c2aa7a` — 승인 화면.** `app/front/components/admin/queue-gate.tsx`(+280) · `lib/api.ts`(+34) · `service/pipeline/stages/daily.py`(+23) · 회귀 테스트 1건.
    - **기존 분기 옆에 하나를 얹는 모양이다.** 게이트 카드에 `isDaily` 를 신설해 `isNote`·`isConcepts` 와 나란히 뒀다 — **유튜브 경로는 한 줄도 바뀌지 않았다.**
    - **줄 쪼개기를 화면이 한다 — 이 Phase 의 핵심 설계 판단이다.** 서버는 career 를 **본문 전문**으로 내고, 화면이 `splitCareer()` 로 줄을 나눠 보여준 뒤 승인 시 `joinCareer()` 로 남은 줄만 다시 합쳐 보낸다. 쪼개는 것은 **보여주기 위한 일**이라 서버가 알 이유가 없고, 서버는 이미 "본문 전문 교체" 로 서 있다(P3 완료 증거 「career 는 기존 frontmatter 를 그대로 이고 본문만 바꾼다」). **이 선택 덕에 발행부가 한 줄도 바뀌지 않았다** — 서버가 줄을 알게 했다면 계획 조립·`upsert`·보호 검증이 전부 줄 단위 계약을 새로 이고 갔을 것이다.
    - **BE 는 두 곳만 손봤다.** ① career 갱신안에 `previous_content` 를 실었다 — 화면이 "무엇이 바뀌었는지" 를 보이려면 비교 대상이 필요한데 파일을 화면이 직접 읽을 수는 없다. ② **`concept` 의 `mode` 를 `new` → `create` 로 고쳤다.** 유튜브 `concept` 게이트와 FE 타입과 `ConceptList` 가 전부 `create` 를 쓰는데 잔디만 `new` 를 냈다 — **같은 컴포넌트를 재사용하므로 잔디 개념만 잘못 렌더될 참이었고**, 발행부의 `create`/`replace` 분기도 같은 규약 위에 있다. 회귀 테스트(`test_concept_mode_matches_the_youtube_gate`)를 붙였다.
    - ✅ **Open Issue 「career 갱신안의 기존과의 차이 표시 방식」 해소.** 전문 diff 도 섹션별 요약도 아니고 **바뀐 줄에만 표시 + 기존 본문은 접어 두기**를 골랐다. 근거는 career 의 변화량이다 — 매일 갱신하되 **대개 조금씩만 바뀌고 `changed:false` 가 정상**이라(SPEC-012 §5), 좌우 비교 화면은 거의 언제나 같은 것을 두 번 보여준다. 기존 본문은 필요할 때만 펼친다.
    - ⚠ **FE 는 검증하지 못했다.** 이 환경에 **node·npm 이 없어 타입검사도 빌드도 돌리지 못했다.** `mode` 불일치는 코드 대조로 잡은 것이고, **그 외 화면 동작은 전부 미검증이다.** BE 741 passed 는 화면에 대해 아무것도 말하지 않는다.

  - **커밋 `2a2483a` — 한 바퀴 완주.** `tests/test_grass_end_to_end.py` 신설(366줄) + `flow.py` 한 줄. 접수 → `collect` → `investigate` → `daily` 게이트 → 승인 → 발행을 **한 경로로** 태운다. **조사만 더미이고 하류는 전부 진짜 코드다** — `DummyCollect`·`AgentInvestigate`·`DailyStage`·게이트·발행부가 실제로 돌고 AI 호출만 가짜가 답한다. DB 도 실물이고(Postgres 없으면 skip) 파일도 실제로 써진다.
    - **관측 결과**: `persona/daily/2026-07-29.md` 가 생기고 `persona/career/medisolve-ai.md` 본문이 바뀌며 `permanent/concept/` 에 개념이 하나 놓이고 **커밋은 없다**(`git log` 가 init 하나뿐). 사람이 고친 요약 줄이 그대로 발행되고, `counts` 는 코드가 센 값이며, `date` 는 점 표기이고, career 의 `bullets` 는 살아남았다. P3 가 말로 적어 둔 계약들이 여기서 **한 경로 위에서** 관측됐다.
    - **잡은 것 ① — 레일 버그.** `flow.advance_auto_stages` 가 게이트를 **열고 `False` 를 돌려줘** 드라이버가 멈췄다. 게이트가 제출만 되고(`generating`) 수확되지 않아 **사람이 볼 것이 없는 상태로 남는다.** 유튜브 준비부가 `result.ok` 로 `True` 를 돌려주는 것과 같은 이유로 `True` 여야 한다. **단위 테스트는 "게이트가 열렸는가" 만 봤지 "내용이 채워졌는가" 는 보지 않아 놓쳤다.**
    - **잡은 것 ② — 연결부는 여기서만 깨진다는 사실 자체.** 각 조각의 단위 테스트는 **자기 계약만 본다.** `collect` 산출물이 `investigate` 를 지나 게이트 payload 가 되고 그것이 발행 계획으로 조립되는 이음매는 어느 단위 테스트의 관할도 아니다. P2 의 수확 계약 결함 둘(`b1a2642`)도 같은 자리에서 나왔고, 그때는 코드를 읽어 찾았지만 이번에는 **테스트가 잡았다.**
    - ⚠ **이 커밋의 메시지에 오진이 하나 들어 있다** — "잔디가 만든 concept 는 그래프상 부모가 없다". **틀렸고 `ead2ceb` 가 정정했다**(아래). **이 발주서에는 그 서술이 들어오지 않았다** — 당시 갱신은 concept 문제를 「형식 SoT 를 읽지 않는다」 Open Issue 로만 적었고 그 진단은 옳았다. 커밋 로그를 거슬러 읽는 사람을 위해 여기 남긴다.

  - **커밋 `ead2ceb` — concept 규율 통일. 진단이 뒤집힌 자리다.**
    - **틀린 진단**: "잔디 concept 는 상류를 가질 수 없다 — daily 도 career 도 그래프 밖이라 무엇을 걸든 L2(고아)에 걸린다." **테스트 fixture 가 `up:` 을 career 로 걸어 고아가 된 것을 구조적 불가능으로 잘못 읽은 것이다.**
    - **실제 원인은 훨씬 작았다 — `daily` 게이트가 concept 를 대충 다뤘다.** 잔디 concept 도 기존 **개념·종합노트·자료노트**를 얼마든지 상류로 가질 수 있고, **개념이 개념에서 자라는 것이 오히려 정상이다**(`rules/knowledge-note-pipeline.md` 의 개념 성장). 문제는 프롬프트가 `"노트 전문"` 한 줄이 전부라 **모델이 무엇을 `up:` 에 넣을지 알 방법이 없었다**는 것이다. 유튜브 `concept` 게이트는 규칙 문서를 읽히고(`READ_THE_RULES`) 기존 개념 목록을 넣고 `up:` 을 명시 지시하고 `check_note` 로 검증한다 — **한 목적지에 규율이 둘이었다.**
    - **고친 것 넷** — ① `READ_THE_RULES.format(template="concept.md")` 로 **규칙 문서와 템플릿을 읽힌다**(프롬프트에 복사하지 않는다 — SoT 가 둘이 되는 것을 막는 P1 이래의 규율 그대로) ② `build_index()` 로 **기존 개념 목록**(stem·title·aliases)을 넘긴다. 매칭을 AI 에 맡기지 않는 규율은 유튜브와 같다 ③ `up:` 은 **실재하는 stem** 이어야 하고 **daily·career 를 걸면 안 된다**고 명시 — 그 둘은 그래프 밖이라 걸면 고아가 된다(P3 「그래프 검증 제외는 사실의 반영이다」의 대칭) ④ 유튜브와 **같은 검사기**(`check_note`)로 `title`·`aliases`·`up` 을 **게이트에서** 검증한다. 여기서 막지 않으면 발행 직전 그래프 검증에 걸려 **daily 까지 함께 거부된다** — 사람이 화면에서 고칠 수 있는 시점에 거르는 편이 싸다.
    - **덤으로 나온 것 — L3 규칙 누락.** `up:` 에 쓴 stem 은 본문에도 `[[stem]]` 으로 있어야 한다(`up:` 은 본문 링크의 부분집합, KDEV-DEC-004). **유튜브 프롬프트에는 있던 지시인데 잔디로 옮기며 빠졌다.** 규율을 맞추러 들어가지 않았으면 드러나지 않았을 결함이다.
    - `TestConceptGap`(잘못된 진단을 고정해 두었던 테스트)을 지우고 한 바퀴 테스트가 **concept 발행까지** 통과하게 했다. fixture 는 `reference → concept → concept` 로 실제 계보를 세운다 — **진짜 그래프가 그 모양이라**(concept 는 전부 `up:` 을 갖는다) 가짜로 단순화하면 검증이 헐거워진다.
    - ✅ **Open Issue 「잔디가 만드는 concept 는 형식 SoT 를 읽지 않는다」 해소.** **SPEC 환류는 없다** — 그 Open Issue 가 예측한 대로("고치는 쪽이면 `daily.py` 가 유튜브와 같은 로더를 쓰면 되고 **스펙은 그대로다**") SPEC-012 §「형식 SoT」 표는 이미 `templates/knowledge/concept.md` 의 읽는 쪽에 잔디 `daily` 게이트를 적어 두고 있었다. **코드가 스펙을 따라온 것이지 스펙이 바뀐 것이 아니다.**

  - **커밋 `75d2605` — 조사 진행 표시 + FE 첫 실행. 앞선 판단 하나가 뒤집힌 자리다.**
    - **`failed_repos`·`truncated` 는 실려 있었지만 사람에게 가지 않았다.** 그 둘은 `payload()` — **AI 프롬프트 쪽**이다. 승인 화면이 보는 것은 `parse()` 의 산출이고 거기에는 없었다. 앞 갱신이 "게이트 payload 에 실려 오는데 화면이 그리지 않는다" 고 적은 것은 **절반만 맞았다** — 화면이 안 그린 게 아니라 화면까지 오지도 않았다. FE 만 고쳐서는 닫히지 않는 항목이었다.
    - `collection` 블록(`done`·`total`·`missing`·`failed`·`truncated`)을 `parse()` 산출에 더했다. **`counts` 와 같은 규율이다** — 코드가 세고 AI 는 관여하지 않으며 화면은 표시만 한다. AI 가 세면 "조사가 잘 됐다" 는 서술과 실제 상태가 어긋나도 사람이 구분할 수 없다.
    - **`failed` 와 `missing` 을 따로 센다.** 앞은 클론·fetch 에서 빠진 것이고 뒤는 조사까지 갔다가 결과가 안 돌아온 것이다 — **다른 자리의 실패**라 한 숫자로 뭉개면 어디를 고쳐야 하는지가 사라진다. `total` 은 조사를 시도한 수(성공 + 결과 없음)이고 `failed` 는 거기 들지 않는다.
    - 전부 온전하면 「조사 N/N · 빠진 레포 없음」 한 줄로 접힌다. **늘 경고를 띄우면 아무도 안 본다.** `collection` 은 optional 이라 이 커밋 전의 리비전에는 없고, 없으면 그리지 않는다.
    - ✅ **FE 를 처음으로 돌렸다 — 「node·npm 이 없다」는 호스트 기준으로만 맞았다.** 이 환경에 **docker 가 있다.** `node:20-alpine` 에 `app/front` 를 마운트해 `tsc --noEmit` 과 `next build` 를 돌렸고 **둘 다 통과했다**(`/admin/queue` 포함 16 route). BE 테스트도 같은 방법으로 이 워크트리에서 돈다(`kknaks_profile-back` 이미지 + pytest 엔트리포인트). **앞선 세 커밋이 "검증 불가" 로 적어 둔 것은 사실이 아니라 수단을 못 찾은 것이었다.**

  - **그래도 P4 를 `DONE` 으로 올리지 않은 근거.** 남은 것은 성질이 다르다 — **타입·빌드 층은 닫혔고 사람이 조작하는 층이 열려 있다.** 검증 여섯 중 셋(회사 레포 서술 반영 · career 줄 제외의 화면 경로 · 시나리오 7종 구분)이 **떠 있는 화면에서 사람이 눌러 봐야** 확인되고, 하나(잔디 칸)는 성질상 P5 다. 배포가 P5 하나뿐이므로 이 셋은 그때 한꺼번에 갚는다. **P4 가 열린 채로 남는 것이 정확한 표시다** — 화면 코드가 컴파일된다는 것과 사람이 그것으로 승인할 수 있다는 것은 다르다.

### Phase 5 — 진짜 git 수집 + 외부 연동 + 실운영 (BE/Ops)

- **Status**: IN_PROGRESS — **코드는 전부 들어왔다.** 작업 16 중 14 가 닫혔고 남은 둘은 배포와 실발행이다. 사용자 지시로 **배포는 코드 검토 뒤**로 미뤘다(2026-08-01).
- **설명**: 더미를 진짜 조사로 갈아 끼우고, 스케줄러·알림·배포를 붙인다. **가장 무겁고 유일하게 배포가 필요한 단계다.** WORK-015·016 과 같이 **실운영 완주를 완료 조건으로** 둔다 — 코드가 도는 것과 하루치가 발행되는 것은 다르다.

> **P4 가 열린 채로 P5 를 시작한 근거.** Phase 순서를 어긴 것이 아니다 — P4 의 잔여는 **사람이 화면을 눌러 보는 것**이고, 레지스트리와 클론 관리는 그 화면을 **한 줄도 지나지 않는다**. 두 갈래가 만나는 곳은 배포 하나뿐이고 그건 P5 의 맨 끝이다. 반대로 P4 잔여는 **떠 있는 서버가 있어야** 갚히는 종류라, 그것을 기다리면 갚을 수 있는 일까지 멈춘다.
>
> **처음 이 문단을 쓸 때의 근거("node 가 없어 지금 갚을 수 없다")는 틀렸다.** 그 빚은 `75d2605` 가 갚았다 — docker 로 타입검사·빌드를 돌릴 수 있었고, 못 한 것이 아니라 **수단을 못 찾은 것이었다.** 문단의 결론은 그대로지만 이유가 바뀌었으므로 고쳐 적는다.

- **작업**:
  - [x] `tracked_repos` 모델 + 마이그레이션 `0007`
  - [x] `showcase.md` → 레지스트리 1회 시드 (`links.repo`→`slug`, `org`→`type`), `detail` 은 company 수동 — **시드가 company 를 건너뛰고 건수를 돌려주는 모양으로 확정**(아래 완료 증거)
  - [x] `docker-compose.yml` — `repo-cache` 볼륨(back rw, 컨테이너 내 **`/var/cache/repos`**), 워커의 `CONCURRENCY` 리터럴을 **`${WORKER_CONCURRENCY:-2}`** 로 분리. **로컬 compose 도 같이 맞췄다** — 둘이 어긋나면 로컬에서만 도는 결함이 생긴다
  - [x] `config.py` — 클론 루트, identity 패턴, 입력 상한(32KB/8KB/30건)
  - [x] `service/jobs/repos.py` — `clone --bare` · `fetch --all --prune` · `last_fetched_at`/`last_error` 기록
  - [x] identity 조회 + drift 판정 + Slack 알림
  - [x] `collect_commits.py` — `git log --all --numstat --author=<패턴>` · **author 날짜** KST 경계 · tree-hash dedupe · 영역 분해 · `counts`
  - [x] 입력 상한 적용 + `truncated` 기록 — **diff 본문을 싣고** 넘치면 본문만 버린다
  - [x] **더미 `collect` 를 진짜 `collect` 로 교체** — 계약이 같으므로 이 스테이지 밖은 손대지 않는다. **테스트가 키 집합 동일성을 직접 본다**
  - [x] `scheduler.py` — 잔디 잡을 **접수 호출**로 교체
  - [x] 접수 날짜 파라미터(백필) — `POST /api/admin/queue/daily`
  - [x] Slack 알림 전환 — 발행 완료 → 승인 대기(발동 시 1회, 미승인 2건 이상 재알림)
  - [x] 구 잔디 경로 제거 — `inputs.py` 의 세 함수 + `main_job.py`·`llm.py`·`upsert.py` **파일째**
  - [x] `tests/test_jobs.py` 정리 — `TestWriteDaily`·`TestLLM*` 계열을 통째로 지웠다
  - [x] **로컬 e2e 에서 드러난 결함 5건 수정** — 발주 시점에 없던 항목이다. 아래 「로컬 e2e 결함」 참조
  - [x] **레지스트리 시드 진입점** — `app/scripts/seed_repo_registry.py`. 발주 목록에 없었다: 시드 **함수**는 있었지만 프로덕션 호출부가 0이었다
  - [ ] 배포 — 볼륨·env 반영, 서버에서 13개 최초 클론 (~321MB). **코드 검토 뒤로 미뤘다.** 절차와 넣을 값은 아래 「배포 준비물」에 확정돼 있다
  - [ ] 하루치 실발행 완주
- **검증**:
  - [~] `enabled=false` 레포가 조사에서 빠진다 — **조회 쪽은 섰다**(`enabled_repos()` 가 켜진 것만 slug 순으로 낸다). 그것을 쓰는 조사가 아직 없어 **관측은 못 했다**
  - [~] `type=company` 인데 `detail` 이 실재 career stem 이 아니면 등록 거부 — **`detail` 이 비면 DB 가 막는다**(CHECK). **실재하는 stem 인지는 아직 아무도 안 본다** — 오타난 stem 은 지금 그대로 들어간다(아래 완료 증거의 남은 구멍)
  - [~] feature 브랜치에만 있는 본인 커밋이 잡힌다 — **동작은 테스트로 고정**(로컬 레포). mediness 기준 +78건은 실데이터라 배포 뒤
  - [~] tree-hash 중복이 제거된다 — **동작은 고정**. 163건 실측은 배포 뒤
  - [~] 세 identity 커밋이 모두 잡힌다 — 패턴 부분매칭이 서 있다. **실제 3종 확인은 배포 뒤**
  - [x] 미등록 identity 발견 시 Slack 알림이 나가고 조사는 계속된다
  - [x] 레포 1개 fetch 실패가 나머지를 막지 않고 `last_error` 가 남는다 — `61b6e40`. 실패 알림도 **한 통으로 묶여** 나간다
  - [x] **클론 뒤에 태어난 브랜치가 다음 fetch 에 딸려 온다** — 발주에 없던 항목이다. 아래 완료 증거의 refspec 결함이 이것을 요구했다
  - [x] 같은 날짜로 두 번 조사해도 결과가 동일하다 — 조사는 읽기 전용이고 fetch 멱등성도 함께 고정했다
  - [x] `counts["commit"]` 과 영역 합계가 다를 수 있음을 테스트가 명시한다 — P2 의 `decompose` 테스트가 그대로 서 있다(공유 모듈로 옮겨도 같은 함수다)
  - [~] 스케줄러 발동으로 항목이 접수된다 — 등록·부팅은 확인. **실제 발동은 떠 있어야 본다**
  - [x] 날짜 지정 백필이 동작한다 — 미래 날짜 거부와 같은 날 중복 합류까지
  - [~] 승인 대기 알림이 오고, 2건 이상일 때 재알림된다 — 코드는 섰고 **실제 Slack 발송은 배포 뒤**
  - [ ] `daily`·`career`·`concept` 가 **한 커밋**으로 나간다
  - [ ] 발행 후 `/api/activity`·`/api/career` 가 갱신된다
- **완료 증거**: 작업 16 중 14. 남은 둘(배포 · 실발행)은 미작성.

  - **커밋 `cf8ac91` — 레포 레지스트리.** `alembic/versions/0007_tracked_repos.py`(신설) · `core/models.py`(+51) · `service/jobs/repo_registry.py`(신설 126줄) · `tests/test_repo_registry.py`(신설 155줄). 741 → **753 passed**(신규 12).
    - **"보여줄 레포" 와 "긁을 레포" 를 가른다.** 종전 추적 대상은 `products/*/showcase.md` 에 묶여 있었는데 그 파일은 **공개 표시용**이라, 사이트에 안 보이지만 커밋은 세고 싶은 레포를 표현할 방법이 없었다. 시드가 `visible` 을 **보지 않는** 것이 이 분리의 전부다 — 표시 여부와 추적 여부는 다른 축이고, 그 둘을 가르려고 테이블을 만들었다.
    - **이 파이프라인에서 유일한 스키마 변경이다.** 큐·게이트 테이블은 손대지 않았다 — `source_kind` 와 `stage_name` 에 CHECK 가 없어 새 파이프라인이 스키마를 건드리지 않는다(「정의는 데이터다」, KDEV-DEC-011 D2). P1 이래 "새 파이프라인은 정의만 얹는다" 고 적어 온 것이 **여기서 마이그레이션 한 장으로 확인됐다.**
    - **career 귀속의 불변을 DB 가 강제한다.** `type=company` 면 `detail` 이 있어야 하고 `studio` 면 없어야 한다는 것을 CHECK 로 걸었다. 앱에만 두면 **조용히 틀린 채로 쌓이고**, 틀린 귀속은 남의 경력 문서를 고친다 — 발행부의 본인작성 보호(P3)가 막아 주는 종류의 사고가 아니다. 그쪽은 "누가 썼는가" 를 보고 이쪽은 "어느 문서인가" 라서 서로를 대신하지 못한다.
    - **시드는 한 번만 긁는다.** 그 뒤로는 레지스트리가 SoT 이고 showcase 는 공개 표시용으로 돌아간다 — 계속 동기화하면 분리한 목적이 사라진다. 다시 돌려도 새 레포만 들어온다(`detail`·`enabled`·`path_rules` 는 사람이 손본 값이라 덮지 않는다). **`company` 는 시드가 건너뛰고 몇 건인지 돌려준다** — showcase 에 career 귀속 정보가 없고 어느 문서로 갈지는 사람이 정할 일이라, 지어내면 조용히 틀린다. 대신 **사람이 채워야 할 것이 몇 개인지는 알려 준다.**
    - **테스트가 박은 함정 둘.** ① `github.com/` 접두를 뗀다 — 안 떼면 클론 URL 이 `github.com/github.com/...` 이 된다 ② **개인 계정이 둘이다**(`kknaks`·`kknaksss`). 하나만 알면 `mykakao` 가 조용히 빠진다 — BL-004 이 identity 3종을 실측하며 드러낸 것과 **같은 종류의 함정**이고, 다음 작업(identity 조회)이 정확히 그 축 위에 있다.
    - ⚠ **남은 구멍 — `detail` 이 실재하는 career stem 인지는 아무도 안 본다.** DB 는 "비었는가" 만 막는다. 오타난 stem 은 그대로 들어가고, 그때 발행부는 **없는 파일을 새로 만든다**(career 는 `upsert` 다). 검증 항목이 요구하는 것은 "실재하는 stem" 이므로 **이 항목은 아직 반만 섰다.** 어디서 막을지는 열려 있다 — 등록 시점(레지스트리)이냐 조사 결과를 career 로 묶는 시점(`investigate`)이냐.
    - ⚠ **시드는 아직 돌려 본 적이 없다.** 함수는 테스트 fixture 위에서 돌았지만 **진짜 `products/*/showcase.md` 13개를 대상으로는 실행하지 않았다.** 실제 시드는 서버 DB 에서 한 번 도는 것이고 그건 배포 항목에 붙는다 — 그때 `needs_detail` 이 몇으로 나오는지가 **company 레포를 손으로 채울 목록**이다.

  - **커밋 `61b6e40` — bare 클론 관리.** `service/jobs/repos.py`(신설 218줄) · `config.py`(+60) · `tests/test_repo_sync.py`(신설 19건) · compose 둘 · `Dockerfile.back`. 753 → **772 passed**.
    - **`git clone --bare` 는 fetch refspec 을 남기지 않는다 — 이 발주에서 가장 조용한 결함이다.** 그대로 두면 이후 `fetch` 가 `FETCH_HEAD` 만 갱신하고 `refs/heads/*` 는 클론 시점에 멈춘다. **에러가 나지 않아 겉으로는 정상인데**, 둘째 날부터 새 브랜치의 커밋이 통째로 빠진다 — **전 브랜치를 보려고 GitHub API 를 버린 이유 그 자체가 조용히 무효가 되는 것이다**(BL-004 실측 17.3%). 클론 직후와 매 fetch 전에 `+refs/heads/*:refs/heads/*` 를 박는다. 이미 있는 클론에도 매번 박는 이유는 **앞선 버전이 refspec 없이 만들어 두었을 수 있고 그 상태가 겉으로 정상이기 때문이다.**
    - **`--mirror` 를 쓰지 않았다.** refspec 이 `+refs/*:refs/*` 라 GitHub 이 광고하는 `refs/pull/*` 까지 받는다. 필요한 것은 브랜치뿐이고 디스크 예산은 321MB 다.
    - **클론 루트가 작업트리 안이면 돌기 전에 멈춘다.** SPEC-011 §5 가 적어 둔 것을 실행 시점 검사로 옮겼다 — 안에 두면 발행 경로의 작업트리 초기화가 클론을 지우고, **조용히 지워지면 다음 조사가 321MB 를 다시 받는다.**
    - **깨진 디렉터리는 보고하고 지우지 않는다.** 조사는 읽기 전용이고(§5 멱등성), 일시적 이상으로 수백 MB 를 날리는 쪽이 사람이 한 번 보는 것보다 비싸다.
    - **토큰이 stderr 를 타고 `last_error`·Slack 으로 새는 것을 저장 직전에 지운다.** 인증은 extraheader 로 넘기므로 URL 에는 없지만 **그것은 우리 쪽 사정이고 git 이 무엇을 출력할지는 우리가 정하지 않는다.**
    - **네트워크 없이 테스트한다.** `GITHUB_CLONE_BASE` 를 `file://` 로 돌려 로컬 레포를 원격처럼 쓴다 — **그 이음매가 없으면 위 refspec 결함을 재현할 방법이 없다.** 클론 뒤에 태어난 브랜치가 다음 fetch 에 딸려 오는지를 직접 관측하고, 지워진 브랜치가 prune 되는지, 두 번 돌려도 같은지(§5 멱등성)를 함께 고정했다.
    - **볼륨 함정 하나.** named volume 이 붙는 `/var/cache/repos` 를 **이미지에 미리 만들지 않으면 볼륨이 `root:root` 로 생겨** 비루트 유저(`1000:1000`)가 못 쓴다. 미리 만들어 두면 fresh volume 이 소유·모드를 물려받는다 — 로컬 compose 가 다른 uid(`501:20`)로 도는 것까지 감안해 `1777` 이다.
    - ⚠ **진짜 GitHub 에 붙여 본 적은 없다.** 토큰 경로·회사 레포 권한·13개 실제 클론(~321MB)은 전부 배포 항목에 붙는다. 여기서 선 것은 **git 이 어떻게 동작하는지**이지 **우리 토큰이 무엇을 받아올 수 있는지**가 아니다.

  - **커밋 `9382d27` — 진짜 커밋 조사 + 구 잔디 경로 제거.** `collect_commits.py`·`collect_git.py`·`collect_common.py`·`review_alert.py`(신설) · `main_job.py`·`llm.py`·`upsert.py`(**삭제**) · `inputs.py`·`scheduler.py`·`driver.py`·`bootstrap.py` · 테스트 둘 신설. 777 → **783 passed**.
    - **셋을 한 커밋에 둔 이유.** `inputs.py` 의 두 함수는 유일한 소비자가 `main_job` 이고, 스케줄러를 안 바꾼 채 먼저 지우면 백엔드 부팅이 통째로 막힌다(아래 머리말). 교체·전환·제거가 한 덩어리다.
    - **계약이 같아서 하류가 한 줄도 안 바뀌었다.** P2 가 「더미가 SPEC-011 §4 를 통째로 낸다」로 그어 둔 경계의 값을 여기서 받는다. 테스트가 **진짜 payload 의 키 집합이 더미와 같은지**를 직접 본다 — 말로 적어 둔 계약은 다음 사람이 줄일 수 있다.
    - **`collect_common.py` 를 새로 뺐다.** P2 는 "지어내는 것은 커밋뿐이고 영역 분해·`counts` 산출은 진짜 코드다" 라고 적었는데, **더미와 진짜가 같은 함수를 부르지 않으면 그 말이 말뿐이다.**
    - **잡은 것 넷.** ① **author 날짜로 센다** — `--since`/`--until` 은 커밋터 날짜로 거르는데 리베이스가 그걸 오늘로 바꾼다. 좁게 자르면 **지난주 작업이 오늘 잔디에 찍힌다.** 창을 ±7일로 넓게 받고 author 날짜로 정확히 거른다 ② **머지 제외** — 남의 작업을 내 것으로 들이고 `--numstat` 이 합쳐진 diff 를 내놓아 증감이 부풀려진다 ③ **중복 제거를 상한보다 먼저** — 순서가 바뀌면 리베이스 163건이 상한 30건을 통째로 잡아먹고 실제 작업이 잘려 나간다 ④ **레코드 구분자로 파싱** — 개행이나 파이프로 나누면 커밋 메시지 본문이 그 자리를 차지한다.
    - **diff 본문을 실어 보낸다.** 상한(레포 32KB·커밋 8KB)이 존재하는 이유가 그것이고, BL-004 이 "병목은 프롬프트가 아니라 **입력**" 이라 한 것도 그 말이다. 넘치면 본문만 버리고 **파일명·증감 라인은 절대 안 버린다** — 무엇을 건드렸는지는 남고 어떻게 고쳤는지만 사라진다. ✅ **SPEC-011 v0.0.2 로 환류했다**(아래).
    - **identity drift 는 알리되 조사를 멈추지 않는다.** 그 커밋들은 이미 패턴에 걸려 결과에 들어 있고, 알림은 "등록하거나 패턴을 좁혀라" 는 요청이지 실패 통지가 아니다. `KNOWN_COMMIT_IDENTITIES` 가 비면 전부 미등록으로 뜨는데 **그게 맞다** — 처음 한 번은 실제 identity 가 몇 종인지 사람이 봐야 한다(BL-004 이 실측으로 3종을 찾은 일을 운영에서 반복하게 두지 않는다).
    - **Slack 알림의 목적이 바뀌었다.** 종전에는 「발행 완료」를 알렸다 — **이미 레포에 쓰인 뒤라 사람이 할 일이 없는 통지**였다. 이제 알리는 것은 "사람이 봐야 할 것이 생겼다" 이고, **이 알림이 안 가면 파이프라인이 조용히 멈춘다.** 자리는 드라이버가 게이트를 채우고 손을 떼는 그 지점이다.
    - **`DummyCollect` 는 남긴다.** 시나리오 일곱(일부 실패·전부 실패·상한 적중·활동 0…)은 진짜 git 으로 재현하기 어렵고 한 바퀴 테스트가 그 분기들을 타고 있다. 걷어낸 것은 **운영 경로**이지 테스트 재료가 아니다.
    - ⚠ **진짜 GitHub 에서 돈 적이 없다.** 여기서 선 것은 로컬 레포 위의 git 동작이다. 13개 실클론·회사 레포 권한·실제 identity 3종·실비용은 전부 배포 뒤다.

  - **SPEC-011 v0.0.2 — 구현이 스펙보다 앞서 있던 자리 셋.** 세 가지 다 **코드가 옳고 스펙이 침묵했던** 경우라, 적어 두지 않으면 다음 구현자가 되돌려도 테스트가 통과한다.
    - **`commits[]` 에 `diff`·`diff_truncated`·`author`·`authored_at` 을 적었다.** 상한(32KB/8KB)이 본문을 전제하는데 계약에는 본문이 없었다 — 그대로 두면 **본문을 빼도 계약상 정상**이고, 그러면 상한 값이 의미를 잃는다.
    - **머지 커밋 제외를 수집 규칙에 넣었다.** 코드가 `--no-merges` 를 쓰는 이유(남의 작업 유입 · 합쳐진 diff 로 증감 부풀림)가 어디에도 없었다.
    - **「시간 경계」를 author 날짜로 못박고 절을 하나 세웠다.** 종전 표현 "KST 00:00~다음날 00:00" 은 **어느 날짜를 말하는지가 비어 있었다.** `git log --since` 의 기본은 커밋터 날짜이므로 순진하게 읽으면 리베이스된 커밋이 엉뚱한 날에 찍힌다. 조회 창을 넓게 잡는 이유와, 창 밖 리베이스를 **알고 놓친다**는 한계까지 계약에 적었다.

  - **커밋 `66f8894` — 백필 진입점.** `POST /api/admin/queue/daily`. **`POST /items` 로는 안 된다** — 그쪽은 일반 `intake()` 라 잔디의 두 방어(미래 날짜·본인 작성)와 `daily:{date}` 합성 키를 지나치고, 그러면 같은 날짜가 두 항목이 되거나 사람이 쓴 daily 를 덮어쓰는 계획이 만들어진다. 스케줄러와 **같은 함수**를 부른다 — 손으로 넣은 날과 자동으로 들어온 날이 다르게 동작하면 백필로 재현한 문제가 실제 상황과 어긋난다. 783 → **786 passed**.

### 로컬 e2e 결함 10건 (2026-08-02~03)

로컬 스택으로 한 바퀴를 돌려 **테스트가 잡지 못한 결함 10건**을 찾았다. 접수 4852(2026-08-01)가 `collect ✓ → investigate ×2 ✓ → daily ✗` 로 멎은 것이 출발점이다.

**공통점이 이것들을 묶는다: fake 를 쓰는 테스트로는 하나도 안 잡힌다.** ①은 실행기를 fake 로 갈면 워커를 안 지나고, ②는 스케줄러 잡을 부르는 테스트가 없었고, ③④는 애초에 호출부가 없어 테스트할 대상이 없었고, ⑤는 테스트 자신의 전제였다. ⑥⑧⑨는 **실 LLM 출력·실 브라우저**가 있어야만 재현된다.

**그리고 셋(⑥⑧⑨)은 앞의 것을 고쳐야 비로소 드러났다.** ①이 30초에 죽는 동안 ⑥은 보이지 않았고, ⑥으로 게이트가 열려야 ⑧에 닿았다. **결함이 줄지어 있었다** — 한 번에 다 보이지 않는다는 것이 이 발주에서 e2e 를 완료 조건에 넣은 값이다.

| | 결함 | 고친 곳 | 어떻게 드러났나 |
|---|---|---|---|
| ① | `daily` 게이트가 안 열린다 — 워커 무출력 상한 30초 | `app/worker/run.py` `apply_idle_timeout()` | 실 워커 |
| ② | 스케줄러가 드라이버를 안 깨운다 | `daily_intake.run_daily_intake_job` | 코드 대조 |
| ③ | `app/scripts/run_daily_activity.py` 가 죽은 import | 삭제 | 코드 대조 |
| ④ | 레지스트리 시드를 돌릴 방법이 없다 | `app/scripts/seed_repo_registry.py` | 호출부 조사 |
| ⑤ | DB 테스트가 빈 테이블을 전제한다 | `tests/conftest.isolate_tables` | e2e 가 DB 를 채우자 12건 실패 |
| ⑥ | 모델이 JSON 앞에 산문을 붙이면 파싱이 죽는다 | `stages/common.extract_json_object` | **실 LLM 출력** |
| ⑦ | 큐 화면 CSS 경고(`border`/`borderLeft` 혼용) | 미수정 — 경미 | 브라우저 콘솔 |
| ⑧ | **승인이 사람의 daily·career 편집을 삼킨다** | `queue-gate.tsx` + `gates.approve` 가드 | **실 브라우저 승인** |
| ⑨ | **큐 화면을 열어 두면 조사 중 항목이 죽는다** | `prepare.harvest_preparation` 가드 | **실 브라우저 폴링** |
| ⑩ | career 발행이 frontmatter 를 통째로 재작성한다 | `apply/plan.render_career` | 발행 산출물 육안 확인 |

**⑥ JSON 머리말.** ①을 고쳐 159초를 완주했는데 그 다음이 `INVALID_DAILY_OUTPUT · char 0` 이었다. 결과 3179자는 멀쩡한 JSON 인데 앞에 설명 두 줄이 붙어 있었다. 프롬프트는 이미 "JSON 하나로 답한다" 였고 모델이 안 지켰다 — **프롬프트를 조이는 것만으로는 안 된다.** 계약 문구를 조이고(`첫 글자가 { 여야 한다`) 파서에 관용성을 넣었다.

같은 로직의 복사본이 셋이었다(`daily._strip_fence`·`common.parse_json_output`·`route._parse`). 전부 펜스만 벗기고 머리말은 못 벗겼다 — **유튜브 게이트도 같은 취약점**이었고 아직 안 터졌을 뿐이다. `extract_json_object()` 하나로 합치고 에러 코드만 스테이지별로 남겼다. 첫 `{` 부터 **괄호 균형**까지 자른다(문자열 안의 괄호·이스케이프는 세지 않는다) — `rfind("}")` 로 자르면 꼬리말 안의 `}` 에 걸린다.

**⑧ 승인이 편집을 삼킨다 — 가장 값비싼 발견이다.** `queue-gate.tsx` 의 타입 가드가 거짓말을 했다.

```ts
function isConcepts(p): p is ConceptPayload { return !!p && "concepts" in p; }
```

**잔디 게이트 payload 는 `{daily, career, concepts, collection}` 이라 `concepts` 를 가진다.** 그래서 concept 로 오판돼 승인이 `{concepts}` 만 보냈고 daily·career 가 버려졌다. 화면에는 「승인됨」이 뜨고 **발행에서 `EMPTY_PLAN` 을 만나서야** 드러난다. 타입 술어가 거짓을 단언하면 `tsc` 는 그대로 믿으므로 **타입검사로는 절대 안 잡힌다.**

BE 에도 가드를 세웠다. `revision.payload = payload_override` 가 통째 교체라 화면이 무엇을 빠뜨리든 받는다 — 화면만 고치면 같은 함정이 다음 게이트에서 다시 열린다(`REQUIRED_PAYLOAD_KEYS`). route 는 `validate_route_result` 가 빈 `rationale` 을 정당하게 떨어뜨려 대상에서 뺐다.

**⑨ 화면을 열어 두면 조사 중 항목이 죽는다.** `_harvest_item()` 이 목록 조회마다 `preparing` 항목에 **무조건 레거시 단건 수확기**를 불렀다. 그 수확기는 실행 1건을 전제해서 fan-out 준비(`ai_task_id` 가 비어 있다)를 만나면 `TASK_REF_MISSING` 으로 닫는다. 드라이버(`_finish_auto_stage`)는 auto/레거시를 갈랐지만 **읽기 경로에는 그 분기가 없었다.**

실증: 접수 몇 초 만에 `prepare_failed` 인데 워커는 조사 2건을 정상 완료했다(`done`, 1153·1712자). **파이프라인이 아니라 조회가 죽인 것이다.** ②를 고쳐 드라이버가 즉시 돌기 시작하자 노출 구간이 넓어져 드러났다.

판별 기준을 새로 만들지 않았다 — `running_preparation` 의 docstring 이 이미 "레거시 준비에는 `stage` 키가 없다" 고 적어 두고 있었다. 그 규약을 **수확기 자체**에 세웠다. 호출부마다 되풀이하면 또 빠뜨린다.

**⑩ career 발행이 frontmatter 를 재작성한다.** 값은 보존되는데 **주석이 사라지고 키가 알파벳순으로 재정렬됐다.** 본문만 바뀌어야 할 발행이 42 insertions / 38 deletions 를 냈고, `# 이력서 PDF — 비면 PDF 미표시` 주석이 없어졌다.

원인은 `render_career` 가 `frontmatter.loads()` → `dumps()` 로 **YAML 을 왕복**한 것이다. 함수의 docstring 은 진작부터 "기존 frontmatter 를 **그대로 이고** 본문만 바꾼다" 고 적고 있었다 — **의도는 맞았고 구현이 그것을 못 지켰다.**

이제 파싱하지 않는다. 여는 `---` 부터 닫는 `---` 까지를 **문자 그대로** 떼어 본문만 이어 붙인다. 종전에 개행 없이 끝나던 것(`\ No newline at end of file`)도 같이 고쳤다 — 매 발행마다 diff 에 남던 잡음이다.

**"사람 전용 필드를 건드리지 않는다" 는 규율은 값이 같으면 되는 것이 아니다.** 사람이 적어 둔 주석과 순서도 그 사람의 것이다. 기존 테스트가 **파싱된 값**만 단언해서 이 결함을 통과시켰다(`meta["bullets"]["ko"] == [...]`) — 새 테스트는 텍스트를 본다.

**배포 전에 닫은 이유**: 로컬은 dry-run 이라 `git checkout` 으로 되돌렸지만, 서버는 첫 발행에 그 손실이 `origin/main` 에 커밋되고 손으로 복구해야 한다(사용자 결정 2026-08-03).

**① 무출력 상한 — open-kknaks 를 고치지 않고 우리 부팅부에서 덮는다.**

`daily` 프롬프트가 investigate 산출물 79KB + 템플릿 9KB 를 물어 첫 토큰까지 30초를 넘겼고, `IdleTimeoutError` 로 재시도 3회를 소진했다. `investigate` 도 실측 25·32초로 **같은 벽 바로 앞**이었다.

open-kknaks 는 timeout 을 둘로 나눠 잰다. 전체 데드라인(`options.timeout_sec`)은 태스크별로 넘길 수 있지만 **무출력 상한은 `executor.IDLE_TIMEOUT` 모듈 상수라 넘길 자리가 없다** — `ClaudeConfig`·`Task` 어디에도 없고 env 도 안 읽는다. `ClaudeWorker` 가 executor 를 인자로 받지 않고 안에서 만들어 인스턴스 교체도 안 된다.

**open-kknaks 를 고치는 대신 부팅 시 모듈 속성을 덮는다**(사용자 결정 2026-08-02). open-kknaks 는 PyPI 로 나가는 별도 제품이라 이 레포의 결함 하나로 릴리스·핀 bump·OKK-SPEC 개정을 끌어오지 않는다. 성립 근거는 executor 가 그 상수를 **루프 안에서 매 회전 다시 읽는다**는 것이다(기본인자 캡처가 아니다).

- back 쪽 `timeout_seconds`(600·900초)는 **무관하다** — 그건 back 이 결과를 기다리는 상한이고 워커가 먼저 죽인다
- `TimeoutMiddleware` 로도 안 된다 — `task.options["timeout_sec"]` 만 만지고 idle 은 못 만진다
- 값은 **180초**. 전체 데드라인(기본 600초)이 뒤에서 받치므로 멈춘 프로세스가 방치되지 않는다
- **입자가 워커 전역이라는 것이 이 방식의 한계다.** 이 워커가 우리 파이프라인만 돌려서 지금은 무해하다. 태스크별 조정이 필요해지면 그때 OKK 에 `options.idle_timeout_sec` 을 내는 것이 정공법이다 — Open Issue 로 세운다
- **조용한 회귀를 둘로 막았다.** 상수가 사라지면 `apply_idle_timeout()` 이 부팅에서 `RuntimeError` 를 던지고, `TestInstalledContract` 가 설치본 소스의 참조를 검사한다. 없으면 다음 버전 bump 가 이 결함을 그대로 되살린다

**② 접수 뒤 `follow()`.** `api/routers/queue.py` 의 수동 접수는 커밋 뒤 `_follow()` 를 부르는데 스케줄러 잡에 그 대칭이 없었다. 실증에서 120초간 `received` 정지 후 목록 API 한 번에 진행했다(조회 시 수확 안전망). **화면을 안 열면 매일 09:05 에 항목만 쌓인다.** `follow()` 실패는 다시 던지지 않는다 — 접수는 이미 커밋됐고, 여기서 던지면 성공한 접수가 잡 실패로 보고된다.

**④ 시드 함수는 있는데 부르는 곳이 없었다.** `seed_from_showcase()` 의 호출부가 테스트 4곳뿐이었다. 배포하면 `tracked_repos` 가 빈 채로 떠서 매일 `NO_ACTIVITY` 로 끝난다 — **실패로 보이지 않는다.** 그리고 company 5건은 함수가 일부러 건너뛰므로 `detail` 을 넣을 경로가 따로 필요했다. `seed_company_from_showcase()` 를 더해 스크립트가 둘을 순서대로 돈다. **admin 엔드포인트가 아니라 스크립트인 이유**는 배포 때 한 번 돌리는 일회성 작업이고, 발주서가 레지스트리 관리 화면을 범위 제외로 두고 있어서다.

여기서 검증 하나가 같이 닫혔다 — **`detail` 이 실재하는 career stem 인지 본다**(`UnknownCareerError`). DB CHECK 는 `detail IS NOT NULL` 만 보므로 오타는 통과하고, 조사까지 정상으로 돌다가 **발행 단계에서** 없는 문서에 쓰려다 그날 career 가 사라진다. P5 검증의 "오타난 stem 은 지금 그대로 들어간다" 구멍이 이것이다.

**⑤ 테스트가 빈 dev DB 에 기대고 있었다.** e2e 로 `tracked_repos` 13행과 큐 항목 하나가 들어오자 **12건이 깨졌다.** 즉 786 passed 는 레지스트리가 빈 상태에서만 참이었고, **레지스트리가 채워진 것이 정상 운영 상태**다 — 배포하면 반드시 만나는 종류다. `isolate_tables()` 가 이미 열려 있는 트랜잭션 안에서 해당 테이블을 비운다. 바깥 트랜잭션이 teardown 에서 롤백되므로 **커밋된 데이터는 안전하다**(수정 후 `tracked_repos=13`·company 5 그대로임을 확인했다).

### 로컬 하루치 완주 (2026-08-02) — **dry-run**

결함 9건을 고친 코드로 **레지스트리를 비운 상태에서** 처음부터 한 바퀴를 돌렸다. 이것이 "하루치 실발행 완주" 의 로컬판이다 — 남은 것은 서버에서 같은 것을 **실 push** 로 하는 일이다.

| 단계 | 결과 |
|---|---|
| 시드 | `tracked_repos` 0 → 스크립트 1회 → **13건**(studio 8 + company 5/`medisolve-ai`). 손으로 넣었던 것과 동일 |
| 접수 | 날짜 미지정 → 어제(KST) `2026-08-01`, 항목 5881 |
| 드라이버 | **무개입 전진** — `collect ✓ → investigate ✓✓ → daily` |
| investigate | 25.9초 / **60.8초**. 어제 25·32초에서 늘었다 — **30초였으면 둘째가 죽었다** |
| daily 게이트 | `review_pending`, 본문 1411자(상한 1500 미만, 잘림 없음) |
| 사람 승인 | 요약 4줄→**3줄**, career 924자→**727자**(문단 하나 제외) |
| 발행 | `apply: succeeded`, `commit_ref: null` |
| 산출물 | `persona/daily/2026-08-01.md` 신규 + `persona/career/medisolve-ai.md` 수정 |
| 되돌림 | `git checkout` + 신규 파일 삭제. **로컬 레포에 커밋하지 않았다** |

**concept 는 0건이었다** — 두 판 모두. 모델이 "`up:` 이 가리킬 stem 이 없어 만들지 않는다" 고 판단했고 이는 설계상 정당하다(억지로 만들지 않는다). **그래서 `permanent/concept/` 목적지의 발행 경로는 이번에 검증되지 않았다.** 서버 완주 때 확인할 것으로 남긴다.

**본문 잘림은 결함이 아니었다.** 첫 판 1738자(잘림), 둘째 판 1411자(정상). 편차이지 계통적 문제가 아니라 현 설계(상한 초과 시 절단)를 그대로 둔다.

**⑨ 검증에는 화면을 열어 둔 것이 필요했다.** 같은 조건에서 이전 항목(5739)은 몇 초 만에 죽었고, 고친 뒤에는 같은 폴링이 도는 동안 investigate 2건이 살아서 완주했다.

### 배포 준비물 — 사람만 아는 값 (2026-08-01 확정)

배포일에 정할 것을 남겨 두지 않는다. **그날 결정하면 그날 틀린다.**

**① `company` 레포 5개의 `detail` — 전부 `medisolve-ai`.** 넣는 방법은 `app/scripts/seed_repo_registry.py --company-detail medisolve-ai` 다(결함 ④). 시드를 실제 `products/*/showcase.md` 에 돌려 본 결과 13개 중 **studio 8개는 자동으로 들어가고 company 5개는 건너뛴다**(`needs_detail=5`). 다섯 다 `MediSolveAIDev` 조직이고 `persona/career/` 에서 `is_current: true` 는 `medisolve-ai` 하나뿐이다 — `career_targets` 가 `is_current` 아닌 문서를 거르므로 다른 stem 을 넣으면 그 레포의 작업이 어디에도 안 실린다.

```
MediSolveAIDev/CENTURION-CHARTY   MediSolveAIDev/centurion_mso
MediSolveAIDev/Linky              MediSolveAIDev/mediness
MediSolveAIDev/NEXUS
```

**② `KNOWN_COMMIT_IDENTITIES` 는 비워 둔다.** 첫 실행에 전부 미등록으로 알림이 뜨는 것이 **의도한 동작이다** — BL-004 이 실측으로 identity 3종을 찾아낸 일을 운영에서 반복하지 않으려면 한 번은 눈으로 봐야 한다. 미리 채우면 오타난 값이 조용히 굳고, 그러면 빠진 커밋을 영영 모른다. 첫 알림을 보고 등록한다.

**③ 공용 dev DB 는 그대로 둔다 — 머지까지 `kknaks-back` 을 재시작하지 않는다.** DB 는 `0008`, main 브랜치 코드는 `0006` 까지라 entrypoint 의 `alembic upgrade head` 가 모르는 리비전을 만나 **부팅이 막힌다.** 되돌리면(`downgrade 0006`) 이 브랜치 테스트를 돌릴 때마다 다시 올려야 한다. ⚠ **`restart: unless-stopped` 라 호스트 재부팅·크래시로도 재시작될 수 있다** — 그때는 머지하거나 임시로 `0008` 까지 올린 코드를 올려야 한다. 이 위험을 알고 받아들인 선택이다.

> **구 경로 제거와 스케줄러 교체는 같은 커밋이다.** 이 Phase 안에서도 순서는 지킨다. `inputs.py` 의 두 함수는 유일한 소비자가 `main_job.py` 이고, 스케줄러를 안 바꾼 채 먼저 지우면 백엔드 부팅이 통째로 막힌다(Execution 머리말 ①). 재배치로 노출 구간이 좁아졌을 뿐 결합 자체는 그대로다.

## Pre-deploy Check (**P5 전용**)

P1~P4 는 배포하지 않으므로 해당 없다.

- [ ] `repo-cache` 볼륨이 레포 작업트리 **밖**이다 — back 은 `.:/repo` 로 작업트리를 물고 `REPO_ROOT=/repo` 이므로 컨테이너 내 마운트를 **`/var/cache/repos`** 로 둬 `reset --hard`·`clean -fd` 사정권을 벗어난다
- [ ] `GH_TOKEN_COMPANY` 가 설정돼 있다 (없으면 회사 레포 5개가 조용히 빠지고 `medisolve-ai` career 가 갱신되지 않는다)
- [ ] 디스크 여유가 321MB 이상이다
- [ ] 워커 `:ro` 마운트가 그대로다 — 클론 볼륨을 워커에 붙이지 않았다
- [ ] **`IDLE_TIMEOUT_SEC` 이 워커에 반영됐다** — compose 기본값 180. **안 들어가면 `daily` 게이트가 열리지 않는다**(결함 ①). 워커 부팅 로그의 `idle_timeout=180s` 로 확인한다
- [ ] **레지스트리 시드를 돌렸다** — `python ../scripts/seed_repo_registry.py --company-detail medisolve-ai`. 안 돌리면 조사 대상이 0건이라 매일 `NO_ACTIVITY` 로 끝난다. **실패로 보이지 않는다**(결함 ④). `--dry-run` 으로 먼저 본다
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
- [~] SPEC-011·012·013 의 Acceptance Criteria 가 전부 검증됐다 — **실데이터를 요구하는 항목만 남았다**(실클론·identity 3종·실측 건수)
- [ ] SPEC-010 개정분(`upsert` · 그래프 밖 산출물 · 본인작성 보호)이 코드에 반영됐다
- [x] **더미로 한 바퀴 완주**(P4) — 접수부터 승인·발행까지 끊김 없이 돌고, dry-run 산출물이 작업트리에 남는다. **테스트 경로로 달성**(`tests/test_grass_end_to_end.py`, 커밋 `2a2483a`) — 「완주」의 뜻은 P4 머리말에서 확정했다
- [ ] **진짜 데이터로 하루치 실발행**(P5) — `daily`·`career`·`concept` 가 한 커밋으로 origin 에 나갔다. **사람이 화면으로 도는 완주가 여기 흡수돼 있다** — 실발행은 승인 화면을 거쳐야 일어나므로 별도 항목을 세우지 않는다
- [x] 구 잔디 경로가 제거되어 이중 실행이 없다 — `main_job.py`·`llm.py`·`upsert.py` 파일째, `inputs.py` 의 세 함수(`9382d27`)
- [~] 기존 유튜브 파이프라인 회귀 없음 — **786 passed** 로 테스트 상 회귀 없음. 실사용 확인은 배포 뒤
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다 — 실발행 완주와 함께

> SPEC-008 개정분의 "route 없는 체인"(`chain.enabled_stages` 일반화)은 **이번 범위 밖**이다. 아래 Open Issue 참조.

## Open Issues

- **워커 무출력 상한이 태스크별이 아니라 프로세스 전역이다.** 결함 ① 을 open-kknaks 를 고치지 않고 `app/worker/run.py` 에서 모듈 상수를 덮어 해결했다(사용자 결정 2026-08-02). 그래서 `daily`(180초가 필요)와 유튜브 요약(30초면 충분)이 **같은 값을 쓴다.**

  **지금은 무해하다.** idle 은 "출력이 멎은 시간" 이라 정상 태스크는 애초에 안 걸리고, 이 워커가 우리 파이프라인만 돌린다. 상한을 늘리는 것은 느려지게 만드는 것이 아니라 **죽이지 않게** 만드는 것이다. 전체 데드라인(600초)이 뒤에서 받쳐 멈춘 프로세스도 방치되지 않는다.

  **닫아야 할 때는 둘이다.** ① 다른 성격의 워크로드가 같은 워커 큐에 들어올 때 ② 어느 스테이지가 180초로도 부족해질 때. 그때의 정공법은 open-kknaks 에 `options.idle_timeout_sec` 을 내는 것이다 — `options.timeout_sec` 이 이미 `task.options` 로 들어가는 경로가 있어 그 패턴을 그대로 베끼면 되고, 우리 쪽은 `AgentStage` 에 스테이지별 값을 두면 된다. **비용은 코드가 아니라 절차다**: PyPI 릴리스 + 핀 bump 2곳(`app/back/pyproject.toml`·`Dockerfile.worker`) + OKK-SPEC-001/004/008 개정.

  ⚠ **덮어쓰기가 조용히 죽는 것이 이 방식의 유일한 실질 위험**이라 가드 둘을 세워 뒀다(부팅 `RuntimeError` + `TestInstalledContract`). open-kknaks 를 올릴 때 그 둘이 울면 여기를 읽는다.

> **spec-코드 차이는 전부 닫혔다 (2026-08-01).** `investigate` 결과 귀속(SPEC-013 v0.0.2 §4) · 잔디 concept 형식 SoT(`ead2ceb`) · career 차이 표시 방식(`8c2aa7a`) · `chain.enabled_stages` 일반화(범위 밖으로 확정) · **활동 0 차단 위치**(SPEC-013 v0.0.3) · **`detail` 실재 stem 검증**(`missing_career`). 마지막 둘은 아래에 결정 근거와 함께 남긴다 — 어느 쪽으로 갈렸는지가 다음 구현자에게 필요하다.

- ~~**활동 0 차단이 스펙과 다른 자리에 있다.**~~ **해소 (2026-08-01) — SPEC-013 v0.0.3 §4. 선택지 ①(스펙을 코드에 맞춘다)로 결정했다.**

  **항목은 남기되 상태로 구분한다.** `no_activity` 를 `ITEM_STATUSES` 에 더하고(마이그레이션 `0008`), `prepare` 가 `NO_ACTIVITY` 를 받으면 `prepare_failed` 대신 그쪽으로 닫는다. 큐의 `HIDDEN_STATUSES` 에 넣어 **기본 목록에서 감추고** 「완료 항목 보기」로만 보이게 했다.

  **②(항목 폐기)를 고르지 않은 이유가 이 결정의 전부다.** 지워 버리면 "조사가 돌았는데 활동이 0" 과 "**스케줄러가 안 돌았다**" 가 구분되지 않는다 — 화면상 둘 다 빈칸인데 후자는 고쳐야 할 장애다. ②가 더 싸고 스펙 원문에도 맞지만, 싼 대신 **관측 가능성을 판다.**

  **준비 상태와 항목 상태를 갈랐다.** `ItemPreparation` 은 `failed` + `error_code=NO_ACTIVITY` 그대로다 — 준비가 산출물 없이 닫힌 것은 사실이다. 바뀐 것은 **항목** 쪽이고, 그 둘은 다른 것을 말한다(모델 주석의 「넷은 서로 다른 상태다」와 같은 규율). 종결 상태라 다시 준비하지 않고 백필은 새 항목으로 들어온다.

  **스펙을 고쳤다** — 접수 시점에 활동 여부를 알려면 조사를 두 번 해야 하고, 미루면 §5 「접수는 요청 안에서 조사를 기다리지 않는다」와 부딪힌다. 원문 진단(아래)이 그 막다른 길을 이미 적어 두었다.

  <details><summary>원문</summary>

  **활동 0 차단이 스펙과 다른 자리에 있다.** SPEC-013 §4 는 Flow 에 "항목 생성(**활동 0이면 없음**)" 을, State 에 `received: 접수 (활동>0)` 을 적어 두었다. 코드는 접수 전이 아니라 `collect` 스테이지의 `NO_ACTIVITY` 로 막는다(`dac6ad9`). **결과적으로 발행되지 않는 것은 같지만 항목 행 하나가 남는다** — 큐 화면에 실패로 닫힌 항목이 활동 없는 날마다 하나씩 쌓인다는 뜻이다.

  구현이 그쪽을 고른 이유는 비용이다. 활동 여부는 조사를 해 봐야 알고, 접수 시점에 한 번 더 조사하면 **P5 에서 bare 클론 13개를 하루에 두 번** 훑는다. 조사를 두 번 하지 않으면서 "활동 0이면 항목 없음" 을 지키는 방법은 접수를 조사 뒤로 미루는 것뿐인데, 그러면 접수가 요청 안에서 조사를 기다리게 되어 SPEC-013 §5 「접수는 요청 안에서 조사·AI 호출을 기다리지 않는다」와 정면으로 부딪힌다.

  **선택지 셋.** ① 스펙을 코드에 맞춘다(활동 0인 날은 `NO_ACTIVITY` 로 닫힌 항목이 남는다고 계약에 적고, 큐 화면에서 그 상태를 어떻게 보일지 U-1 에 더한다) · ② `collect` 가 활동 0을 판정하면 항목을 **폐기(soft delete)** 해 행을 지운다 · ③ 스케줄러가 접수 전에 가벼운 조사(커밋 유무만)를 한 번 더 한다. **①·② 가 유력하고 ③ 은 두 번 조사를 되살린다.** 늦어도 P5 실운영 전에는 닫는다 — 실데이터에서는 활동 0인 날이 드물지 않다.

  ⚠ 원래 "P4 착수 전에 고르는 것이 싸다" 고 적었는데 그러지 못했다. P4 화면(`8c2aa7a`)이 이 상태를 그리지 않은 채로 들어왔고, 결국 화면을 한 번 더 열어 표시를 붙였다.

  </details>

- ~~**`detail` 이 실재하는 career stem 인지 아무도 안 본다.**~~ **해소 (2026-08-01) — 선택지 ②(`investigate` 가 묶을 때)로 결정했다.**

  **판정은 이미 있었고 없던 것은 「사람이 아는 길」이었다.** `career_targets` 는 진작부터 파일 없는 stem 을 건너뛰고 있었다(`logger.info(... DETAIL_NOT_FOUND)`). 즉 **동작은 이미 스펙대로**였고 — 그 레포의 career 귀속만 해제되고 daily·concept 는 그대로 나간다 — 문제는 **그 사실이 로그에만 남는다**는 것이었다. 로그는 아무도 안 본다.

  `missing_career()` 를 더해 `collection.career_missing` 으로 **승인 화면까지** 들고 간다. 승인하는 사람이 **바로 그 자리에서** "이 레포의 오늘 작업은 어느 career 에도 안 실린다" 를 본다. 게이트가 승인 직전이라 고칠 시점으로도 가장 이르다.

  **①(등록 시점)을 고르지 않은 이유 둘** — DB 계층이 레포 파일시스템을 알게 되고, career 파일 이름이 나중에 바뀌면 그 검증이 **무용해진다**. 귀속 시점은 이미 파일을 읽는 층이고 **매번 다시 본다.**

  ⚠ **Slack(`DETAIL_NOT_FOUND`, SPEC-011 Case Matrix)은 아직이다.** `career_map` 을 만드는 곳이 `collect` 라, 알림은 진짜 `collect_commits.py` 가 들어올 때 U-1(클론·fetch 실패)과 **같은 자리에서** 나가는 것이 맞다. 지금 붙이면 게이트 스테이지가 Slack 을 알게 되고, 재생성 때마다 다시 울린다.

  <details><summary>원문</summary>

  `cf8ac91` 의 CHECK 는 `type=company` 면 `detail` 이 **비지 않았음**만 강제한다. 오타난 stem(`medisolve-ai` → `medisolveai`)은 그대로 등록되고, 그 뒤 발행부는 **없는 파일을 새로 만든다** — career 는 `upsert` 라 "그런 문서 없음" 이 에러가 아니다. 본인작성 보호도 안 걸린다(새 파일에는 보호할 사람 글이 없다). 즉 **조용히 유령 career 문서가 하나 생긴다.**

  </details>
- ~~**잔디가 만드는 `concept` 는 형식 SoT 를 읽지 않는다.**~~ **해소 (2026-08-01) — 커밋 `ead2ceb`.** `daily.py` 가 유튜브와 같은 `READ_THE_RULES.format(template="concept.md")` 로더·`build_index()` 기존 개념 목록·`check_note` 검사기를 쓴다. **스펙 환류는 없었다** — 이 항목이 예측한 대로 코드가 스펙을 따라온 것이다. 자세한 내역과, 이 과정에서 뒤집힌 오진(「잔디 concept 는 상류를 가질 수 없다」)은 P4 완료 증거에 있다. (원문 요지: SPEC-012 「형식 SoT」 표와 S-3 4항이 concept 템플릿을 읽으라고 적어 두었는데 `stages/daily.py` 는 프롬프트에 `"노트 전문"` 한 줄이 전부였다 — **같은 목적지에 두 규율**이었고, 발행부 검증이 막아 주기는 하나 승인 화면에 계속 거부당하는 초안이 올라오는 형태로 드러난다.)
- **`chain.enabled_stages` 일반화는 이번에 하지 않는다.** 지금 필요가 없다 — `next_stage` 는 `after` **다음** 게이트만 훑는데 잔디는 게이트가 `daily` 하나뿐이라 `order[1:]` 이 비고, `enabled_stages` 의 결과는 계산되기만 할 뿐 쓰이지 않은 채 `None`(= 발행 차례)이 돌아온다. 첫 게이트도 `open_first_gate` 가 `pipeline.first_gate()` 로 연다. `enabled_stages` 의 소비자는 `next_stage` 하나뿐이다(테스트 제외). 게다가 발주 당시의 제안 형태(route payload 유무로 판정)는 **두 경우를 뭉갠다** — route 스테이지가 있는데 아직 승인 전(유튜브, 켜지면 안 됨)과 route 스테이지가 애초에 없음(잔디, 켜져야 함). **게이트가 2개 이상인 파이프라인이 생길 때** 필요해지고, 그때의 판정 기준은 payload 유무가 아니라 **파이프라인 정의에 route 스테이지가 있는가** 다. 시그니처가 `enabled_stages(pipeline, route_payload)` 로 바뀌고 `tests/test_pipeline_chain.py` 가 동반 수정된다
- ~~**SPEC-013 환류 후보 — 부분 실패 시 "결과를 어느 레포에 붙이는가".**~~ **해소 (2026-08-01) — SPEC-013 v0.0.2 §4 「Data Contract — `investigate` 결과 귀속」.** 대응표(제출 참조 → 레포)·순서 리스트 금지·빈 결과 불인정·`missing` 표시·`stage_failures` 와 `failures` 자리 분리를 표로 박고, §6 에 "부분 실패해도 결과가 원래 레포에 붙는다" 검수 항목을 더했다. **SPEC-011 §4 가 아니라 SPEC-013 에, §5 가 아니라 §4 에 둔 이유**: `failures` 는 SPEC-011 의 조사 산출물 필드지만 **귀속은 조사 산출이 아니라 fan-out 수확의 성질**이고, 그 fan-out 을 소유한 것은 SPEC-013 이다(§1 Scope 「fan-out 배치와 부분 실패 처리」). 그리고 이것은 "어떻게 만드느냐"가 아니라 **관측 가능한 결과의 형태**라 §5 Implementation Rules 가 아니라 §4 Interface Contract 층위에 있어야 한다 — §5 의 「부분 실패는 진행한다」는 이 계약을 가리키도록 문장을 늘렸다. (원문 요지: 코드는 P2 에서 `task_ref` 키로 정했고 순서 있는 리스트는 색인이 밀린다. 스펙이 침묵하는 사이 구현이 먼저 정한 상태라 **다음 구현자가 리스트로 되돌려도 정상 경로 테스트는 통과한다** — 그것이 계약으로 박아야 할 이유였다.)
- `investigate` **순차 13회의 총 소요와 예산 실측** — `worker_budget_usd=5.0` 안에 드는지. 병렬로 돌리는 선택지는 `WORKER_CONCURRENCY` 와 부딪히므로(실운영 1) 실측 전에는 고르지 않는다. P2 에서 더미로 건수만, P5 에서 실비용
- ~~career 갱신안의 "기존과의 차이" 표시 방식 — 전문 diff 인지 섹션별 요약인지~~ **해소 (2026-08-01) — 커밋 `8c2aa7a`.** 둘 다 아니고 **바뀐 줄에만 표시 + 기존 본문은 접어 두기**. 근거는 career 의 변화량이다 — 매일 갱신하되 대개 조금씩만 바뀌고 `changed:false` 가 정상이라(SPEC-012 §5) 좌우 비교는 거의 언제나 같은 것을 두 번 보여준다. **다만 화면이 아직 렌더된 적이 없어 눈으로 확인된 결정은 아니다**
- 첫 클론을 잡 밖에서 미리 돌릴지 첫 실행이 겪게 할지 — 후자면 첫날 조사가 오래 걸린다. P5
- SPEC-012 OQ-1(daily body 1200자 충분성)은 P5 이후 운영에서 판단한다

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: [[work-016-async-execution-and-progress-ui|KDEV-WORK-016]] (제출/수확 분리 · 드라이버)
