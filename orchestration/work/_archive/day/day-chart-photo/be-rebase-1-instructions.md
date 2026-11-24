# [backend] rebase 1 — origin/dev(#274) 위로 · migration 번호 다시 잇기

선례(형식 참고): `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/_archive/day/day-reservation/be-rebase-2-instructions.md` · `be-rebase-2-report.md`

## 상태
- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` · 브랜치 `kknaksss/day-chart-photo`
- 우리 커밋 1개: `7e7cb368`(코디가 전부 담음) · 옛 base `4bf0b4a1`
- origin/dev = `fed616a8`(#274 · 고객 목록 · 차트 · KOS 조회 워커 전환)

## 코디가 merge-tree 로 미리 본 충돌 9
- `backend/day/main.py`
- `backend/day/web.py` — 우리 `header_staff` + dev 변경 둘 다 살림
- `backend/day/templates/base.html` — 헤더 「이름 직군」 + dev 메뉴
- `backend/day/templates/partials/board_chart_parts.html`
- `backend/day/static/day.css` — **빌드 산출물 — 손으로 합치지 말고** `styles/app.css` 를 합친 뒤 CSS 를 다시 빌드
- `backend/tests/day/test_column_snapshot.py`
- `backend/tests/day/test_models.py`
- `backend/tests/migrations/test_alembic.py` — HEAD = 새 마지막
- `scripts/frontend/tests/fixtures/reservations-page.html` — 생성물이면 다시 만든다

자동 병합 파일은 둘 다 살아 있는지 확인한다:
- `error_codes.py`(코드 하나 = 예외 하나 · 겹침 없는지)
- `identifiers.py` · `models/__init__.py` · `routers/board.py` · `tasks/__init__.py` · `day.js` · `app.css` · `icons.html`

## migration 번호 겹침
- dev 에 `20261124_0024_customer_memo.py` 가 있다(revision `0024_customer_memo` · down `0023_companion_permission`).
- 우리 `0024_visit_photo` → **`0025_visit_photo`** 로 바꾼다. 바꿀 것: 파일 이름 · revision · down_revision = `0024_customer_memo` · docstring.
- revision 이름을 쓰는 곳은 **전부 grep** 해서 고친다(시험 · `test_visit_photo_migration.py` · 문서).
- 끝나면 `alembic heads` 가 하나인지 확인한다.

## KOS 쪽 확인
- #274 가 「KOS 조회를 Taskiq 워커로」 옮겼다(`services/ext_refresh.py` · `tasks/ext_refresh.py` · `ext_sync.py`).
- 우리 C35(시스템 토큰 Redis 공유 · `emr/kos/token_store.py`) · E3(`adapter_for`)와 겹치는 KOS 클라이언트 생성 경로가 새로 생겼는지 `build_adapter(` 전수 grep → 생겼으면 같은 공유 토큰을 쓰는지 확인 · 보고(고칠 것은 최소 · 보고에 명시).

## 할 일 순서
1. `git rebase origin/dev`
2. 충돌을 푼다
3. 번호를 민다
4. CSS 를 다시 빌드한다
5. **전체 `./scripts/check.sh` 한 번**(마감 전 전체 검증)
6. 커밋은 하나로 둔다(rebase 결과 · `--continue`)

## 금지
- push 금지
- 스택(11040 · docker · .run) 금지
- `deploy/*.env` 금지

## 보고
- 리포트 `be-rebase-1-report.md`(위 폴더): 새 HEAD sha · 충돌 처리 · 새 번호 · KOS 경로 확인 · check.sh 결과 숫자
- preamble 의 worker_done
