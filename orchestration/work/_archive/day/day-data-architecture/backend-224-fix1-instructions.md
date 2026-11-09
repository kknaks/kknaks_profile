# [backend] #224 검수 WARN 반영 — W1 · W2 · W3 · W4 (+ 같이 고칠 자리)

너는 day backend 워커다. 같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture`(미커밋 변경 그대로 이어서). 역할 문서 · 계약(Issue #224) · allowed_paths 는 앞 브리프(`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-be-brief.md`)와 같다 — **단 §5 의 AGENTS.md 제한은 아래 「AGENTS.md」 항목만큼 넓힌다.**
읽을 것: 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-224-report.md` 의 W1 ~ W4 · W7 · 「조용히 통과하는 자리」 5.

## 고칠 것 (리뷰어 권장 방향대로 — 코디 결정)

1. **W1** — 테스트의 기본 스키마. `conftest.py` 가 어떤 `common` / `day` import 보다 먼저 `DB_SCHEMA=day_test` 를 넣는다. 「기본값은 day_dev」 단언은 `Settings(_env_file=None)` 를 직접 만드는 테스트로 옮긴다. 테스트가 `day_dev` 를 건드리지 않음을 단언하는 시험 한 개.
2. **W2** — `Base` 를 `backend/day/db.py` 로. `common/db/model_base.py` 는 스키마 없는 공통 도구만(`NAMING_CONVENTION` · 필요하면 `make_metadata(schema)`). centurion `backend/crm/db.py` 모양. alembic `env.py` 는 `from day.db import Base`. `common` 이 DAY 스키마 `Base` 를 공개하지 않는다.
3. **W3** — 태스크 등록 = **(a) taskiq CLI 모듈 인자**: `taskiq worker runtime.worker:broker day.tasks` · `taskiq scheduler runtime.scheduler:scheduler day.tasks`. 지금 `day/tasks/` 는 빈 패키지(`__init__.py`)로 만들고 compose `command` 에 반영. runtime 은 `day.tasks` 를 Python import 하지 않는다. 경계 테스트 머리말에 이 방식을 적는다.
4. **W4** — `DAY_REQUIRE_INFRA=1` 이면 infra 테스트를 skip 대신 실패. `scripts/test.sh` 가 켠다.
5. **W7** — migrations 예외를 `migrations/env.py` → `day.db` · `day.models` 로 좁힌다. `importlib.import_module` · `__import__` 문자열 상수 검사 · leak 테스트에 모듈째 재내보내기 금지.
6. 「조용히 통과」 5 — 헬스 probe 실패 시 `logger.warning`(예외 **타입만**, 접속값 · 문구 없음). infra 테스트에 `SHOW search_path` 단언 한 줄.
7. `.dockerignore`(`**/*.env` · `!**/*.env.example` · `.venv` · `.git`) · `.gitignore` 에 `.env.*` + `!*.env.example`.
8. **AGENTS.md** — 「저장소 구조」 트리에 이번에 생긴 자리를 맞춘다(`common/redis.py` · `common/tasks/` · `runtime/health.py · tasks.py · worker.py · scheduler.py` · `day/db.py` 의 Base) · 태스크 등록 방식(CLI 모듈 인자) 한 줄 · 실행 명령에 `DAY_REQUIRE_INFRA`. 다른 문장은 고치지 마라.

## 하지 말 것

- W5 · W6 · W8 · W9(worker 의 migrate 의존 · APP_ENV 필수화) — 다음 Delivery 몫. 손대지 마라.
- 커밋 · push · PR 금지. 포트는 11040 · 11042 · 11043 만, 끝나면 `down`.

## 검증 · 보고

`scripts/test.sh -q` · `uv run ruff check backend` 각 1회 · compose 로 worker · scheduler 가 `day.tasks` 인자로 뜨고 `day.ping` 이 도는지 1회.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-224-fix1-report.md` — W 별 고친 곳(파일:줄) · 수치. 완료는 preamble 의 worker_done 절차대로.
