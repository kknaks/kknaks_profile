# [backend] 시술 현황 1차 기본 권한 채우기

너는 #230 backend 워커다. 같은 워크트리 · 커밋 `e5912d2b` 위 · 커밋 금지 · 템플릿 금지.
정본: 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` 「결정 — 시술 현황 1차 기본 권한」(사용자 2026-11-08 · SPEC-002 반영은 planner 가 동시에).
- 기준 정보 동기화(직무)가 `job_role_permission` 을 이 표대로 채운다 — 태그 매핑 + 표의 이름 줄(경영지원 · 마케팅 = 없음 · 마취과 = 보기 · 수정 · 수락)로 **표와 정확히 같은 결과**. 사람이 바꾼 행이 생길 수 있으니 「동기화가 처음 만든 기본값」과 「사람이 고친 값」을 구분할 방법을 리포트에(지금은 관리 화면 없음 — 덮어쓰기 정책 제안).
- 테스트(DB 없이 매핑 함수): 데모 직무 15개 → 표 그대로. infra 1: 동기화 뒤 행.
- 실물: 데모 지점 기준 정보 회차 뒤 직무별 권한 행 확인(이름 · 키만).
검증 `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff · compose down 금지 · worker/scheduler/api 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-perm-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
