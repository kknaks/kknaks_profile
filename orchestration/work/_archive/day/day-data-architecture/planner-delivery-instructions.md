# [planner] 백엔드 Delivery 시작 — DAY 1차 백엔드 4개(뼈대 · 데이터 모델 · KOS 연동 · 로그인) + PR #909 보정

너는 day planner 워커다. 앞 맥락이 없을 수 있다 — 역할 문서(`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/planner/`)와
1판 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` 의 금지 사항(설계 발명 · 커밋/push 금지)은 그대로다.
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` (브랜치 = PR #909).

**사용자 결정(2026-11-05)**: 백엔드 작업 계획은 mediness 새 규칙대로 **GitHub Delivery Issue** 로 만든다(예전 WP 파일 금지). 디자인은 바뀔 수 있어 **백엔드만**.

## A. PR #909 보정 (products/day 안 · 커밋은 코디)

원천이 바뀌었다 — 반영:
1. **DB 스키마 = env**: `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/README.md` 공통 규칙 「DB」 · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` 결정 7 · 8 — 관리형 PostgreSQL 1대 · DB 1개, 환경은 스키마로(`DB_SCHEMA` = `day_dev` / `day_prod`), 지금은 dev 만.
   SPEC-000 §2 · `40-architecture/system.md` · `code-structure.md` 의 「`day` 스키마」 표기를 이에 맞춘다.
2. **KOS 내부 API 브라우저 헤더 필수**: `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` 「위험 — KOS 내부 API 차단」 — system.md 외부 통합 · 로그인 절에 반영.
lint `--strict` 1회.

## B. start-delivery — Delivery 4개

`.agents/skills/start-delivery/SKILL.md` · `rules/delivery-workflow.md` · `tools/harness/`(README · references/requests.md)를 읽고 그대로 따른다.

| # | Delivery | 결과(완료 뒤 변화) — 근거 |
|---|---|---|
| 1 | 백엔드 뼈대 | CENTURION_DAY `v2-dev` 에 서버가 뜨고 테스트가 돈다: pyproject(Python 3.13 · uv) · `backend/runtime` · `common/db` · 설정(`APP_ENV` · `DB_SCHEMA`) · alembic · 로컬 compose(PostgreSQL · Redis) · 헬스체크 · import 경계 아키텍처 테스트 · taskiq worker/scheduler 자리(Redis 브로커). 근거: 레포 `AGENTS.md`(v2-dev) · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` |
| 2 | 데이터 모델 | DAY-SPEC-000 §3 의 **1차 51 테이블**이 SQLAlchemy 모델 + 첫 alembic migration(`DB_SCHEMA` 스키마)이 된다. 04-1 메뉴(1차 밖)는 제외 |
| 3 | KOS 연동 기반 | `backend/day/emr/`(kos client · mapper) · `external_ref` · `external_outbox` · 10초 일정 폴링 · 1시간 기준 정보(taskiq `interval`) · 병원별 Redis 잠금 · **내부 API 브라우저 헤더**. 데모 지점 데이터가 DAY DB 로 들어온다(`APP_ENV=dev` 는 `is_demo` 연결만) |
| 4 | 로그인 | 우리 로그인 → KOS sign-in → `account` · `staff` · `job_role` · `login_session` · `external_session` 자동 채움(DAY-SPEC-000 §3 04) · 브라우저 헤더 |

- **target SPEC = DAY-SPEC-000**. 지금 `origin/main` 에 없다(PR #909 미머지) → skill 대로 `spec-baseline:pending` 으로 시작한다. 머지 뒤 재결속은 코디가 다시 발주한다.
- **위험 등급** — skill · 가까운 repo 규칙으로 네가 판정하되(뼈대 · migration · 외부 연동이라 L2~L3 로 보인다) 근거를 Issue 에 남긴다.
- 의존: 2 → 1, 3 → 2, 4 → 2 · 3. Non-Goals: 화면(웹 · 앱) · 시술 현황 동작 · 알림 · 채팅 · prod 배포.
- 참고 코드(volatile starting point — 권한 아님): cc-prototype `/Users/kknaks/git/toy_pr2/cc-prototype` `procedure/back/app/kos/`(client · sync · runtime · 쓰기 큐) · centurion `git -C /Users/kknaks/git/centurion show origin/main:backend/common/db/…` · `backend/linky/tasks/broker.py` · `scheduler.py`.
- **멈출 곳**: `review-delivery-plan`(사용자 계약 승인) 또는 `prepare-spec-baseline` 에서 멈추고 보고한다. 구현 · Code PR 은 하지 않는다. human gate 를 대신 통과하지 마라.
- GitHub Issue 생성은 사용자가 허락했다(이 작업 한정). Issue 본문에 KOS 키 · 토큰 · 테넌트 id · 실명 금지.

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery-report.md`: A 고친 곳 · lint / B Issue 4개 링크 · 각 위험 등급과 근거 · 현재 상태 · next_action · 사용자에게 받을 결정. 완료는 preamble 의 worker_done 절차대로.
