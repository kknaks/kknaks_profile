# [frontend] #231 검수 WARN 반영(fix1) — W1 · W2 · W3

너는 #231 frontend 워커다. 같은 워크트리 · 미커밋 · 커밋 금지. **backend 가 #230 fix1 을 동시에 하고 있다 — 백엔드 파일은 건드리지 마라**(조각 계약이 바뀌면 그 워커 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-230-fix1-report.md` 를 보고 맞춘다).
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-231-report.md` W1 ~ W3 · 고칠 방향.
1. **W1** — 시술 줄 시간 칸 「늦음」 빨강을 템플릿이 정하지 않는다: SPEC 규칙(마취 20 · 호출 5)에 있는 것만 · 그 밖은 기본색(리뷰어 방향).
2. **W2** — 권한(edit) 없는 조작 403 이 화면에 안 뜸 → 토스트(권한 없음 문구는 SPEC-001 화면 절 그대로) · 또는 버튼을 처음부터 끔 — 리뷰어 방향대로.
3. **W3** — 미룬 판 다시 받기가 창 닫힐 때만 풀리는 문제(리뷰어 방향).
W4(실물 A4 · A6)는 사용자가 `DAY_ADMIN_EMAILS` 를 넣은 뒤 — 지금은 하지 마라.
검증: `uv run pytest -m "not infra"` · ruff(내 파일) · 브라우저 견본 `/dev/kit/board` 스크린샷 갱신. compose down 금지 · 끝나면 api 만 재빌드.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-231-fix1-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
