---
type: work
id: KDEV-WORK-017
title: "잔디 커밋 파이프라인 — 레지스트리·로컬 클론·승인 게이트"
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
created_at: 2026-07-31
updated_at: 2026-07-31
tags:
  - product/kknaks-dev
  - doc/work
  - status/todo
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
- Covers spec: SPEC-011·012·013 (신규) + SPEC-010·008 (개정분)
- Depends on work: [[work-016-async-execution-and-progress-ui|KDEV-WORK-016]] — 제출/수확 분리와 드라이버가 전제다. 잔디 파이프라인은 그 위에 정의만 얹는다
- Parallel work: 없음
- Follow-up work: `algorithms`·`content_enrich` 게이트 편입 (후속 baseline)
- External dependency: `GH_TOKEN_COMPANY`(회사 레포 클론) · 디스크 약 321MB · 서버 재배포(compose 볼륨 추가)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | — |
| Blocker | 없음 |
| Next | P1 — 레지스트리 + 클론 + collect |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | todo |
| Design | kknaks | 승인 화면 편집 UX | todo |
| FE | kknaks | 게이트 화면 (줄/문장 단위 편집) | todo |
| BE | kknaks | 레지스트리·클론·스테이지·발행부 | todo |
| QA | kknaks | 검증과 완료 판단 | todo |
| Ops | kknaks | 볼륨·env·배포·첫 클론 | todo |

## Scope

포함:

- 레포 레지스트리 테이블 + 마이그레이션 + `showcase.md` 1회 시드 이관
- bare 클론 볼륨과 fetch 절차, identity drift 알림
- `collect` — 로컬 git 조사(전 브랜치·identity 패턴·tree-hash dedupe·입력 상한·영역 분해)
- `templates/persona/daily.md`·`career.md` 신규 + `agent.md` 등록
- `daily_commit` 파이프라인 정의 + `investigate`(fan-out)·`compose` 스테이지
- `chain.enabled_stages` route 없는 파이프라인 분기
- `apply/` 확장 6종 + `publish_atomic` 전환
- 스케줄러 접수 진입점(백필 포함) + 날짜 축 중복 판정
- 승인 대기 Slack 알림 전환
- 게이트 화면 — 줄 단위 편집 · career 문장 단위 승인

제외:

- `products/*/30-work`·`showcase.md`·`persona/posts/` 목적지 → 후속
- `inbox/` idea 목적지 → 채택하지 않음
- `career.bullets` 자동 갱신 → 영구 제외
- 레지스트리 admin CRUD 화면 → 후속

## Code Surface

- Repo / module: `app/back` (주) · `app/front` (게이트 화면) · 루트(templates·agent.md·compose)

| 경로 후보 | 설명 |
|---|---|
| `core/models.py` | 레지스트리 모델 신설 |
| `alembic/versions/0007_*.py` | 레지스트리 테이블 마이그레이션 |
| `config.py` | 클론 루트 경로 · identity 패턴 · 입력 상한 |
| `service/jobs/repos.py` (신규) | 클론·fetch·identity 조회 |
| `service/pipeline/stages/investigate.py` (신규) | 레포별 조사 fan-out |
| `service/pipeline/stages/compose.py` (신규) | 취합 — daily·career·concept 초안 |
| `service/pipeline/collect_commits.py` (신규) | git 조사 (LLM 없음) |
| `service/pipeline/definitions.py` | `DAILY_COMMIT` 등록 |
| `service/pipeline/chain.py` | `enabled_stages(None)` 분기 |
| `service/pipeline/runtime.py` | 스테이지 등록 |
| `service/apply/plan.py` | allowlist 2개 · `LAYER_PREFIX` · `build_actions` 분기 · `upsert` |
| `service/apply/graph_check.py` | `daily`·`career` 제외 |
| `service/apply/executor.py` | 본인 작성 보호 · 사람 전용 필드 검증 |
| `service/scheduler.py` | 잔디 잡 → 접수 호출로 교체 |
| `service/jobs/main_job.py` · `inputs.py` · `llm.py` · `upsert.py` | 구 잔디 경로 정리 |
| `service/notify.py` 호출부 | 발행 완료 → 승인 대기 알림 |
| `api/routers/queue.py` | 접수 날짜 파라미터(백필) |
| `templates/persona/daily.md` · `career.md` | 형식 SoT (신규) |
| `agent.md` | 별도 계열에 daily·career 등록 |
| `docker-compose.yml` | `repo-cache` 볼륨 · `WORKER_CONCURRENCY` |
| `app/front/.../queue` | 게이트 화면 편집 UI |

- Domain / schema note: **마이그레이션 1건**(레지스트리 테이블). 큐·게이트 테이블은 무변경 — `source_kind`·`stage_name` 에 CHECK 가 없어 새 파이프라인이 스키마를 건드리지 않는다.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `tracked_repos` | 잔디가 추적할 레포. `slug`·`type`·`detail`·`account`·`enabled`·`path_rules`·`last_fetched_at`·`last_error` |

- 상태 / invariant: `slug` 유일. `type=company` 면 `detail` 필수이고 실재하는 career stem 이어야 한다. `type=studio` 면 `detail` 은 비어 있다.
- Migration 필요 여부: **필요**(신규 테이블 1개). 기존 테이블 변경 없음.
- SPEC 환류: 없음 — SPEC-011 이 이미 계약을 담고 있다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| P3 `collect` 스테이지 | P1 의 조사 함수 | 레지스트리·클론이 있어야 조사가 돈다 |
| P3 `compose` 스테이지 | P2 의 템플릿 파일 | 형식 SoT 를 읽어 프롬프트를 만든다 |
| P4 발행부 | P3 의 게이트 산출물 | 승인 payload 형태가 계획 조립 입력이다 |
| P5 실운영 | P1~P4 전부 | — |

## Internal Interface Contract

`collect` 산출물(= `investigate`·`compose` 의 입력)은 SPEC-011 §4 Data Contract 를 따른다. 여기서 다시 적지 않는다.

**스테이지 실행기 계약**은 기존 `StageRunner`(`submit`·`poll`·`parse`) 를 그대로 쓴다 — WORK-016 이 세운 것이다. `investigate` 만 예외적으로 한 스테이지가 N 건을 제출하므로, 그 N 건을 `ItemPreparation` payload 에 누적하는 방식을 P3 에서 고정한다.

## Execution

### Phase 1 — 레지스트리 + bare 클론 + collect (BE/Ops)

- **Status**: TODO
- **설명**: 조사의 원천을 바꾼다. 이 phase 가 끝나면 "그날 커밋을 상세히 아는 함수" 가 생기고, 그때부터 파이프라인을 얹을 수 있다. 가장 무겁고 배포가 필요한 단계다.
- **작업**:
  - [ ] `tracked_repos` 모델 + 마이그레이션 `0007`
  - [ ] `showcase.md` → 레지스트리 1회 시드 스크립트 (`links.repo`→`slug`, `org`→`type`), `detail` 은 company 5건 수동
  - [ ] `docker-compose.yml` — `repo-cache` 볼륨(back rw), `CONCURRENCY` 리터럴을 `${WORKER_CONCURRENCY:-1}` 로 분리
  - [ ] `config.py` — 클론 루트, identity 패턴, 입력 상한(32KB/8KB/30건)
  - [ ] `service/jobs/repos.py` — `clone --bare` · `fetch --all --prune` · `last_fetched_at`/`last_error` 기록
  - [ ] identity 조회 + drift 판정 + Slack 알림
  - [ ] `collect_commits.py` — `git log --all --numstat --author=<패턴>` · KST 경계 · tree-hash dedupe · 영역 분해 · `counts`
  - [ ] 입력 상한 적용 + `truncated` 기록
  - [ ] `inputs.py` 의 GitHub API 커밋 경로(`fetch_repo_commits`·`extract_tracked_repos`) 제거, 죽은 `git_log_today` 정리
  - [ ] 서버에서 13개 최초 클론 (~321MB)
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
- **완료 증거**: 미작성

### Phase 2 — 형식 SoT (문서)

- **Status**: TODO
- **설명**: `compose` 가 읽을 양식을 먼저 만든다. P1 과 **병렬 가능**하고 P3 의 선행 조건이다. 코드가 아니라 문서 작업이다.
- **작업**:
  - [ ] `templates/persona/daily.md` — frontmatter 필드 소유(`counts`=코드), 본문 섹션, 길이 상한 1200자
  - [ ] `templates/persona/career.md` — 섹션 5종(`## 담당 영역` 포함), **append 금지·압축 재서술** 규율, 섹션당 5~7줄 상한, `stack` 판정 근거, 사람 전용 필드 격리
  - [ ] `agent.md` — "별도 계열" 에 daily·career 등록 (교안과 같은 형태)
  - [ ] `llm.py` 의 프롬프트에 박힌 daily 형식 명세 제거 → 템플릿 로드로 전환
- **검증**:
  - [ ] 두 템플릿이 존재하고 `agent.md` 에서 도달 가능하다
  - [ ] 프롬프트 어디에도 daily·career 형식 명세가 복사돼 있지 않다
  - [ ] `bullets` 가 "AI 가 정하지 않는다" 로 명시돼 있다
- **완료 증거**: 미작성

### Phase 3 — daily_commit 파이프라인 (BE)

- **Status**: TODO
- **설명**: 조사 결과를 게이트에 태운다. 여기서 처음으로 승인 화면에 잔디 항목이 뜬다.
- **작업**:
  - [ ] `definitions.py` — `DAILY_COMMIT` 등록 (`collect`·`investigate`·`compose` auto + `daily` gate)
  - [ ] `chain.enabled_stages(None)` → 정의된 게이트 전부 (route 없는 파이프라인 분기)
  - [ ] `investigate` 스테이지 — 레포별 N 건 제출·수확, 결과를 `ItemPreparation` payload 에 누적
  - [ ] 부분 실패 처리 — 일부 실패는 진행, 전부 실패면 스테이지 실패
  - [ ] `compose` 스테이지 — 템플릿 로드 + daily·career·concept 초안, `changed:false` 지원
  - [ ] career 결정적 skip (귀속 커밋 0이면 스테이지 미생성)
  - [ ] `runtime` 등록
  - [ ] `scheduler.py` — 잔디 잡을 **접수 호출**로 교체, `main_job` 구 경로 정리
  - [ ] 접수 진입점 + `normalized_url="daily:{date}"` 합성 키 + 날짜 파라미터(백필)
  - [ ] 활동 0 · `auto:false` 접수 전 차단
  - [ ] Slack 알림 전환 — 발행 완료 → 승인 대기(발동 시 1회, 미승인 2건 이상 재알림)
- **검증**:
  - [ ] 스케줄러 발동으로 항목이 접수되고 요청이 AI 를 기다리지 않는다
  - [ ] `investigate` 가 레포 수만큼 돌고 부분 실패해도 게이트가 열린다
  - [ ] 전 레포 실패 시 스테이지 실패로 닫히고 재시도가 열린다
  - [ ] 게이트가 **하나**만 열린다
  - [ ] `type=studio` 만 커밋한 날은 career 초안이 없다
  - [ ] `is_current` 아닌 career 는 대상에서 빠진다
  - [ ] 같은 날짜로 두 번 접수하면 항목이 하나다
  - [ ] 날짜 지정 백필이 동작한다
  - [ ] **기존 유튜브 파이프라인이 회귀 없이 동작한다** (`chain` 변경 영향)
- **완료 증거**: 미작성

### Phase 4 — 발행부 확장 (BE)

- **Status**: TODO
- **설명**: 승인된 것이 실제로 파일이 되게 한다. P3 와 병렬 착수 가능하지만 e2e 는 P3 완료 후다.
- **작업**:
  - [ ] `plan.py` — `ALLOWED_PREFIXES` 에 `persona/daily/`·`persona/career/`
  - [ ] `LAYER_PREFIX` 에 `daily`·`career`
  - [ ] `build_actions()` 에 daily·career 분기
  - [ ] `upsert` 액션 신설 — 존재 여부 미검사, `stale 대상` 은 유지
  - [ ] `graph_check` — `daily`·`career` 제외 (`concept` 는 유지)
  - [ ] 본인 작성 보호 검증 (`USER_AUTHORED_DAILY`)
  - [ ] 사람 전용 필드 검증 (`PROTECTED_FIELD`)
  - [ ] 잔디 발행을 `publish_atomic` 으로 — `commit_and_push_with_retry` 이탈
- **검증**:
  - [ ] `persona/daily/`·`persona/career/` 가 발행 허용된다
  - [ ] 같은 날 두 번 승인해도 `upsert` 로 통과한다 (`ALREADY_EXISTS` 없음)
  - [ ] daily·career 가 그래프 검증에서 빠지고 concept 는 검증을 받는다
  - [ ] 대상 daily 가 본인 작성이면 거부된다
  - [ ] 계획에 `bullets`·`period` 가 있으면 거부된다
  - [ ] push 실패 시 로컬 커밋이 남지 않는다
  - [ ] 발행 재시도가 AI 를 다시 부르지 않는다
  - [ ] 유튜브 발행이 회귀 없이 동작한다
- **완료 증거**: 미작성

### Phase 5 — 게이트 화면 + 실운영 완주 (FE/QA/Ops)

- **Status**: TODO
- **설명**: 사람이 실제로 승인할 수 있어야 끝이다. WORK-015·016 과 같이 **실운영 완주를 완료 조건으로** 둔다 — 코드가 도는 것과 하루치가 발행되는 것은 다르다.
- **작업**:
  - [ ] 조사 진행 표시 (`investigate` N건 중 진행 수, 실패 레포, 상한 적중)
  - [ ] daily 요약 **줄 단위** 편집·삭제
  - [ ] career **문장 단위** 승인·제외 토글 + 기존 문서와의 차이 표시
  - [ ] concept 개별 제외 토글 (기존 패턴 재사용)
  - [ ] 배포 — 볼륨·env 반영, 최초 클론 확인
  - [ ] 하루치 실발행 완주
- **검증**:
  - [ ] 요약 줄을 지우고 승인하면 지운 결과가 발행된다
  - [ ] career 문장을 제외하면 파일에 없다
  - [ ] 회사 레포 서술을 덜어낸 결과가 공개 md 에 반영된다
  - [ ] 승인 대기 알림이 오고, 2건 이상일 때 재알림된다
  - [ ] 승인 안 한 날의 잔디 칸이 비어 있다가 나중 승인 시 채워진다
  - [ ] `daily`·`career`·`concept` 가 **한 커밋**으로 나간다
  - [ ] 발행 후 `/api/activity`·`/api/career` 가 갱신된다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] `repo-cache` 볼륨이 레포 작업트리 **밖**이다 — 안에 있으면 `reset --hard`·`clean -fd` 가 클론을 지운다
- [ ] `GH_TOKEN_COMPANY` 가 설정돼 있다 (없으면 회사 레포 5개가 조용히 빠지고 `medisolve-ai` career 가 갱신되지 않는다)
- [ ] 디스크 여유가 321MB 이상이다
- [ ] 워커 `:ro` 마운트가 그대로다 — 클론 볼륨을 워커에 붙이지 않았다
- [ ] `WORKER_CONCURRENCY` 가 실운영 값(1)으로 반영됐다
- [ ] 예산(`worker_budget_usd=5.0` / `global_budget_usd=20.0`) 안에서 하루치가 끝난다
- [ ] 회사 레포 diff 가 프롬프트로 나가는 것을 알고 있다 (조사 균일·공개 통제는 게이트)
- [ ] 구 잔디 잡이 이중 실행되지 않는다 — 스케줄러에 옛 경로가 남아 있지 않다

## Rollback

- **P1**: 마이그레이션 revert(테이블 drop). 클론 볼륨 삭제. `inputs.py` 의 GitHub API 경로를 되살리면 구 잔디가 그대로 돈다
- **P3**: `definitions.py` 에서 `DAILY_COMMIT` 등록 해제 + 스케줄러를 구 `main_job` 으로 되돌린다. 큐에 남은 `daily_commit` 항목은 폐기 처리
- **P4**: `ALLOWED_PREFIXES`·`upsert` 를 되돌리면 잔디 발행만 막히고 유튜브 경로는 무영향
- **chain 일반화**는 되돌리지 않는다 — 되돌리면 route 없는 파이프라인이 다시 조용히 건너뛴다
- 부분 revert 영향: P4 만 되돌리면 게이트는 열리는데 발행이 거부된다. 항목을 폐기하면 정리된다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다
- [ ] SPEC-011·012·013 의 Acceptance Criteria 가 전부 검증됐다
- [ ] SPEC-008·010 개정분(route 없는 체인 · `upsert` · 그래프 밖 산출물)이 코드에 반영됐다
- [ ] 하루치가 승인·발행되어 `daily`·`career`·`concept` 가 한 커밋으로 origin 에 나갔다
- [ ] 구 잔디 경로가 제거되어 이중 실행이 없다
- [ ] 기존 유튜브 파이프라인 회귀 없음
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다

## Open Issues

- `investigate` 결과를 `ItemPreparation` version N 으로 쌓을지 payload 안 배열로 둘지 — P3 착수 시 결정. 버전으로 쌓으면 이력이 남고 payload 면 조회가 단순하다
- career 갱신안의 "기존과의 차이" 표시 방식 — 전문 diff 인지 섹션별 요약인지. P5 에서 판단
- 첫 클론을 잡 밖에서 미리 돌릴지 첫 실행이 겪게 할지 — 후자면 첫날 조사가 오래 걸린다
- SPEC-012 OQ-1(daily body 1200자 충분성)은 P5 이후 운영에서 판단한다

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: [[work-016-async-execution-and-progress-ui|KDEV-WORK-016]] (제출/수확 분리 · 드라이버)
