
# [backend] Delivery #224 — DAY v2 백엔드 뼈대(서버가 뜨고 테스트가 돈다)

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture`
base 브랜치: `origin/v2-dev` → 최종 PR 대상 `v2-dev` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 아래 「읽을 것」 순서대로 읽고 시작해라. 이 워크트리는 `v2-dev` 기준 빈 레포(AGENTS.md · CLAUDE.md 만)다. 다른 워커는 없다.

## 1. SSOT — 먼저 읽을 것

- **계약 = GitHub Delivery Issue #224** — `gh issue view 224 -R MediSolveAIDev/CENTURION_DAY` (「바뀌는 것」 · 「이번에 하지 않는 것」 · 「완료 조건」 A1 ~ A5 · 「실행 정보」). **여기 없는 건 발명하지 마라.** 사용자가 2026-11-05 이 계약으로 구현을 지시했다.
- 레포 규칙 = `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture/AGENTS.md` — 저장소 구조 · 계층 · 백엔드 안전 · 테스트. 구조는 이대로 만든다.
- 시스템 결정 = `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` — api / worker / scheduler · taskiq + **Redis 브로커(taskiq-redis, RabbitMQ 없음)** · 10초 `interval` · DB 1개 · **`DB_SCHEMA` 로 환경 분리(dev `day_dev`)** · 지금은 dev 만.
- 데이터 · 아키텍처 문서(참고 · 읽기만) — `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/system.md` · `code-structure.md` · `20-spec/spec-000-data-model.md` §2(공통 규칙만 — 업무 테이블은 이번 범위 밖)

## 2. 배경 / 무엇을 바꾸나

DAY CRM v2 를 빈 브랜치 `v2-dev` 에서 처음부터 짓는다. 이번은 그 첫 단계 — 업무 기능 없이 **서버 · 설정 · DB 연결 · migration 체인 · 백그라운드 자리 · 경계 테스트**만 세운다.
다음 Delivery(#225 데이터 모델 · #226 KOS 연동 · #227 로그인)가 이 위에 쌓인다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 헬스체크 경로가 처음 생기는 외부 계약이다. 이름은 centurion 선례를 따르고 리포트에 적어라.

## 4. 먼저 읽을 핵심 파일 (본 — 권한 아님, 베끼지 말고 모양만)

- centurion(같은 회사 · 통합 대상 — 모양을 맞춘다): `git -C /Users/kknaks/git/centurion show origin/main:<경로>`
  - `pyproject.toml`(Python 3.13 · 의존성 축) · `backend/runtime/main.py` · `dispatcher.py` · `composition.py` — 앱 조립
  - `backend/common/config.py` · `errors.py` · `db/session.py` · `db/model_base.py` · `db/config.py`
  - `backend/linky/tasks/broker.py` · `scheduler.py` — taskiq broker · scheduler 진입점(우리는 RabbitMQ 대신 Redis 브로커)
  - `backend/crm/db.py` — `MetaData(schema=…)` 모양 · `backend/migrations/centurion/env.py` — alembic env
  - `deploy/compose.yaml` · `compose.local.yaml` · `compose.test.yaml` — 로컬 · 테스트 compose 모양
  - `docs/development/backend-reliability.md` · `testing-strategy.md`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `pyproject.toml` · `uv.lock` · `.python-version` · `.gitignore`
- `backend/runtime/` · `backend/common/` · `backend/day/`(빈 패키지 · `public.py`) · `backend/migrations/` · `backend/tests/`
- `deploy/`(로컬 · 테스트 compose) · `*.env.example` · `scripts/`(로컬 실행 · migrate · test 스크립트가 필요하면)
- `AGENTS.md` — **딱 한 곳**: 「테이블은 `day` 스키마」 · `schema="day"` 같은 표기를 `DB_SCHEMA`(env) 로 고친다. 그리고 「테스트」 절의 「실행 명령은 첫 코드가 들어올 때 여기에 적는다」 자리에 실제 명령을 적는다. 그 밖 문장은 고치지 마라.

## 6. 구현 단계 — Issue 「실행 정보」 1 ~ 6 순서

1. 프로젝트 · 설정 — uv · Python 3.13 · `APP_ENV`(dev/prod) · `DB_SCHEMA`(dev `day_dev`) · Redis · DB URL 을 env 로(pydantic-settings).
2. runtime · 헬스체크 — FastAPI 앱 조립 · 헬스체크 경로(DB · Redis 확인 포함 여부는 centurion 선례대로).
3. common/db · alembic — async 엔진 · 세션 · `model_base`(`MetaData(schema=DB_SCHEMA)`) · alembic env(`version_table_schema` · `search_path` = `DB_SCHEMA`) · 빈 첫 revision.
4. 로컬 compose — PostgreSQL · Redis(· api · worker · scheduler). **포트는 사용자 것과 겹치지 않게**(기본 5432 · 6379 를 쓰지 말고 DAY 전용 포트) — 띄우기 전에 `lsof -i :<포트>` 로 확인.
5. taskiq worker · scheduler 자리 — taskiq-redis 브로커 · 샘플 태스크 1개(예: 헬스 핑) · scheduler 진입점(`LabelScheduleSource`).
6. 아키텍처 테스트 — `day` → `common` 단방향 · 다른 패키지는 `day.public` 만 · `common` 은 `day` 를 import 하지 않음.

각 단계 끝에 그 단계 테스트만 돌린다. 전체 검증은 마지막에 한 번.

## 7. 범위 제약 — 하지 말 것

- Issue 「이번에 하지 않는 것」 전부 — 업무 테이블 · 모델 · KOS 연동 · 로그인 · 화면 · 시술 현황 · 알림 · 채팅 · prod 배포.
- 실제 비밀값 커밋 금지 — `*.env.example` 만. 공유 STG · PROD DB 금지 — 로컬 compose 만.
- 사용자 포트 · 프로세스 · 컨테이너를 죽이거나 바꾸지 마라. 네가 띄운 컨테이너는 끝나면 내려라(볼륨은 남겨도 된다).
- 커밋 · push · PR 금지.

## 8. 검증

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-224-report.md` — 완료 조건 A1 ~ A5 각각의 증거(명령 · 결과 수치) · 만든 파일 · 정한 이름(헬스체크 경로 · 포트 · 태스크 이름) · 남은 것.

```
(레포 루트에서 — pyproject 는 루트) uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --from term_a35ac44d-5a0f-4901-9681-51c4c9b6de8f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: #224 백엔드 뼈대" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 \
  --text "[worker_done] backend 완료 — #224 백엔드 뼈대. 리포트 work/day-data-architecture/backend-224-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
