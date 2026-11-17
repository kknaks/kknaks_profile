# [frontend] fe-3 — 정렬 탭 글자 (아주 작은 판)

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-fe-brief.md`(역할 · 검증 · 완료 보고)를 따른다. 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`(미커밋 위 · 혼자). 커밋 금지.

사용자 2026-11-17: `/board` 머리 정렬 탭(`nav.day-seg` · 「시술순」 · 「방별순」 — 임시 이름이었음)을 **「시술대기 순」 · 「방별 순」**(띄어쓰기 그대로)으로 바꾼다. 화면에 보이는 글자 · aria 등 사람에게 읽히는 글자만 — 쿼리 값(`sort=room`) · 내부 이름은 그대로.

- 쓰는 곳을 grep 으로 전부 센다(`시술순` · `방별순` — 템플릿 · 라우터 · 서비스 주석 · CSS 주석 · 화면 글자 근거 표 `tests/architecture/test_screen_copy.py` · 화면 테스트). 화면에 나오는 글자와 그 테스트 단언은 바꾸고, 코드 주석은 「(정렬 탭 1 · 2)」처럼 뜻이 맞게만 정리(선택).
- allowed_paths: `backend/day/templates/` · `backend/day/routers/board.py`(글자만) · `backend/tests/` · 주석만이면 `backend/day/services/` · `backend/day/styles/`(CSS 빌드 불필요하면 안 함).
- 검증: 화면 pytest 1회 · ruff. 리포트 `…/kos-signin-limit/fe-3-report.md`(짧게). 완료 보고는 preamble 의 worker_done.
