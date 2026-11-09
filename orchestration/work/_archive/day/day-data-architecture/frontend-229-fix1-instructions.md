# [frontend] #229 + 웹 로그인 검수 FAIL 반영(fix1) — F1 · F2 · F3 + WARN

너는 #229 frontend 워커다. 같은 워크트리 · 미커밋 그대로 · 커밋 금지. 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-229-report.md` F1 ~ F3 · WARN 전부 · 고칠 방향.
1. **F1** — 견본의 실제 지점 이름 제거: 로그인했으면 세션 병원 이름 · 아니면 「견본 병원」 같은 자리표시. 테스트 「견본 응답에 `명동` 없음」. 시안에서 옮긴 다른 실명 · 실데이터가 없는지 템플릿 · 견본 전수 grep. **스크린샷 34장 다시 찍기**(`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-229-shots/` 덮어쓰기).
2. **F2** — JSON `/api/auth/*` 의 `client` 기본값 = app(또는 칸 · 쿠키 분기 제거 — 웹은 화면 라우트가 쿠키). 테스트 옮기기 · JSON 회귀 1.
3. **F3** — 화면 라우트용 예외 처리: `Forbidden` → 권한 없음 페이지(로그아웃 버튼) · `CsrfFailed` → 토스트 조각 · JSON(`/api/`)과 화면 가르기 · `/logout` 개별 try/except 합치기 · 테스트 2.
4. **WARN** — 리포트 고칠 방향대로(`/dev/kit` 노출 범위 등).
5. **사용자가 지금 http://127.0.0.1:11040/login 을 보고 있다** — compose 를 `down` 하지 마라. 다 고친 뒤 `--profile app up -d --build api` 로 api 만 다시 올려 같은 URL 이 새 코드로 뜨게 한다(재시작 전후 `/login` 200 확인).
검증: `uv run pytest -m "not infra"` · `scripts/test.sh -q`(compose 의 postgres · redis 를 같이 쓴다 — 내리지 말 것) · ruff.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-229-fix1-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
