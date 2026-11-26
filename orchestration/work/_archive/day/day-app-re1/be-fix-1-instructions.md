# [backend] be-fix-1 — review-code-1 W5 · W6 · W7

너는 day `backend` 워커다. 역할 · allowed_paths · 검증 · 완료 보고는 같은 폴더 `day-app-re1-be-brief.md` 를 그대로 따른다(먼저 읽어라). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` — 커밋 `43ba40a3` 위. **mobile 워커가 같은 시각 `app/` 을 고친다 — 건드리지 마라.** 코디의 로컬 스택(.run/ · :11040 · deploy/*.env)도 건드리지 마라.

읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/review-code-1-report.md` §W5 · §W6 · §W7.

할 것(리포트 고칠 방향대로 · 동작 변경 없음):
1. W5 — 앱 라우터가 웹 라우터의 비공개 함수(`_form` · `_photo_id`)를 import 하지 않게 공개 이름 / 공용 모듈로 올린다(아키텍처 · Taut 규칙에 맞는 자리)
2. W6 — `ChartConflict` docstring 을 C2 `details.conflicts[]` 모양으로
3. W7 — 웹 사진 파일 GET 의 Bearer 거절 단언을 `required_web_view` 실제 결과로 좁힌다

검증: 브리프 §8 + 만진 파일 관련 테스트 · ruff · `scripts/check.sh` 중 Python 게이트(프론트 단계는 npm 이 이제 설치돼 있으니 돌려 보고 결과를 적는다). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/be-fix-1-report.md`. 커밋 · push 금지.
완료 보고: dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입.
