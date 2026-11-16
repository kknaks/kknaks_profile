# [backend] F16 — KOS 쓰기 바로 보내기

너는 #230 backend 워커다. 같은 워크트리 · 미커밋 · 커밋 금지 · 템플릿 · day.js 금지(frontend 가 동시에). 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md` F16.
- outbox 에 op 을 넣는 조작이 commit 된 뒤 그 병원의 쓰기 큐 발송 태스크를 **바로 발행**(taskiq kiq · 병원별 잠금 · 억제 그대로 — 중복 발행은 잠금이 막음). 10초 주기는 재전송용으로 남김. 발행 실패해도 조작 응답은 성공(주기가 메움).
- 테스트(DB 없이 — 가짜 broker): 조작 뒤 발행 1번 · 발행 실패해도 응답 200.
- 실물: 데모 카드로 버튼 한 번 → 몇 초 안에 sent/confirmed(상태 · 시각만).
검증 `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff · compose down 금지 · api/worker/scheduler 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-feedback-c-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
