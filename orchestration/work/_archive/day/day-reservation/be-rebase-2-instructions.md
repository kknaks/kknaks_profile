# [backend] rebase 2 — origin/dev 최신(#271 · #273) 위로 · migration 번호 다시 잇기
너는 맥락이 없다(새 터미널). 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-rebase-1-report.md`(지난 rebase 방식)와 워크트리 `AGENTS.md` 를 읽어라.
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation` · 브랜치 `kknaksss/day-reservation` · 커밋 둘(`431c081b` 1차 · `68a37b87` 2차) · 옛 base `a03b83a4`. origin/dev = `b2f28990`(#271 · #273).
코디가 merge-tree 로 미리 본 것:
- 충돌 3: `backend/day/emr/kos/__init__.py`(KosAdapter 상속 — dev `KosExtReads, KosExtWrites` + 우리 `KosNotices` 둘 다 살림) · `backend/day/services/emr_sync.py`(import — dev `ext_delivery` + 우리 `reservation_companions` 둘 다) · `backend/tests/migrations/test_alembic.py`(HEAD).
- **migration 번호 겹침**: dev 가 `20261123_0017_ext_catalog.py`(revision `0017_ext_catalog` · down `0016_ticket_bundle_unknown_price`)를 넣었다. 우리 0017 ~ 0022 를 **0018 ~ 0023** 으로 밀고(파일 이름 · revision · down_revision · docstring) 첫 것의 down = `0017_ext_catalog`. revision 이름 쓰는 곳 **전부 grep**(시험 · 서비스 docstring · test_alembic HEAD = 새 마지막). revision 32자 제한 시험 지킴. `alembic heads` 하나.
- 자동 병합되지만 둘 다 고친 파일: `common/config.py` · `common/error_codes.py`(오류 코드 하나 = 예외 하나 taut 규칙 — 겹치는 코드 없는지) · `day/emr/base.py` · `day/identifiers.py` · `day/models/__init__.py` · `day/emr/sync_references.py` — 합친 결과가 둘 다 살아 있는지 확인.
할 일: `git rebase origin/dev` → 충돌 해결 → 번호 밀기 → **전체 `./scripts/check.sh` 한 번**(이번이 마감 전 전체 검증) → 커밋은 두 개 그대로(번호 밀기는 2차 커밋에 담거나 1차 · 2차 각자 맞게 — 1차의 0017 은 1차 커밋 안에서 0018 로). push 금지 · 스택(11040 · docker · .run) 금지 · deploy/*.env 금지.
리포트 `be-rebase-2-report.md`(위 폴더) — 새 HEAD sha 둘 · 충돌 처리 · 새 번호 표 · check.sh 결과 숫자. preamble 의 worker_done.
