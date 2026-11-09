# [backend] #230 검수 FAIL 반영(fix1) — F1 · F2 + W1 ~ W7

너는 #230 backend 워커다. 같은 워크트리 · 미커밋 그대로 · 커밋 금지 · KOS 쓰기 실호출 금지. **frontend 가 같은 워크트리에서 #231(`templates/` · `static/` · `day.js`)을 동시에 만든다 — 그 파일은 건드리지 마라.** 조각 계약(라우트 · 조각 이름 · 넘기는 값 · SSE 이벤트)을 바꾸게 되면 리포트 맨 위에 「#231 영향」으로 적어라.
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-230-report.md` F1 · F2 · W1 ~ W7 · 「조용히 통과」 표 · 고칠 방향.
1. **F1** — 앱 · 웹 SSE 스트림: tick 마다 세션 생존 · 권한 재확인 · 죽으면 끝냄(`session_expired` 이벤트 또는 닫기) · 최대 수명 · infra 테스트(열고 로그아웃 → 다음 tick 에 끝남).
2. **F2** — query-count infra 테스트(방문 1 vs 10 · 같은 쿼리 수) · 독스트링과 맞춤.
3. **W1 ~ W7** — 리뷰어 고칠 방향대로(W1 전체 권한 계정은 권한 검사 한 곳으로 · W4 쓰기 의도가 기록 없이 빠지는 길 막기 등). 「조용히 통과」 표의 테스트 보강.
검증: `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff. **compose down 금지** — 끝나면 `--profile app up -d --build api worker scheduler`.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-230-fix1-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
