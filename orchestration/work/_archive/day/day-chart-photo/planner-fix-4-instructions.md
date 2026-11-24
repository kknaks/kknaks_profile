# [planner] fix-4 — C21 집도의 「한 명」 기준 문구 바로잡기

결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` C21-기본값이 바뀌었다.
- 앞 판: 매핑 전 KOS 외부 id 개수
- 지금: **DAY · KOS 둘 다 매핑 뒤 DAY 직원 수**
- 이유: DAY 사본 `visit_task_staff` 는 매핑된 집도의만 저장한다(`sync_tasks.py:378-381`). 그래서 매핑 전 개수를 알 수 없고, 새 칸은 migration 이라 범위 밖이다.

네가 fix-3 에서 넣은 문장(규칙 31 · U-14 등)을 이 기준으로 바꾼다. 앞 문장은 취소선 + 날짜 · 사유로 남긴다.

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` — 커밋 `d98c5a28` 위에서 한다. 커밋하지 마라.

검증은 lint `--strict` 로 `products/day` ERROR 0.

보고는 `planner-fix-4-report.md`(같은 work 폴더) + preamble worker_done 두 채널.
