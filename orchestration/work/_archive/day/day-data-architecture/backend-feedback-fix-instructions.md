# [backend] 피드백 묶음 검수 WARN 반영 — W1 ~ W6 (백엔드 몫)

너는 #230 backend 워커다. 같은 워크트리 · 마지막 커밋 `4c2cebab` 위 · 커밋 금지 · 템플릿 · day.js 는 frontend 몫(W4 의 화면 쪽은 frontend). 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-feedback-batch-report.md` W1 ~ W6 · 고칠 방향.
- **W1(머지 전 필수)** 바로 보내기 발행에 시간 상한(`asyncio.timeout` · 설정값 · 넘으면 로그 + 실패 · 응답은 성공) · DB 없는 테스트(멈추는 가짜 broker).
- **W2 · W3 · W5 · W6** 리뷰어 방향대로(백엔드 파일만).
검증 `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff · compose down 금지 · api/worker/scheduler 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-feedback-fix-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
