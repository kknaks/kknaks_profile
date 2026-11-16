# [backend] 화면 피드백 1차분 — F8 오더 메모 조사 · 고침

너는 #230 backend 워커다. 같은 워크트리 · 미커밋 · 커밋 금지 · 템플릿 · day.js 금지(frontend 가 동시에). KOS 는 **조회만**(데모 지점 · 값 · 개인정보를 리포트에 남기지 마라).
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md` F8.
- 오늘 방문 오더 메모가 DB `visit.procedure_order_note` 에 비어 있다. 동기화는 일정 응답의 `orderMemo` 를 읽는다. 데모 지점 조회로 **오더 메모가 실제로 어느 칸에 오는지**(일정 · 작업 `memo` · 고객 상세 등) 칸 이름만 확인하고 매핑을 고친다. 응답에 없으면 「없음」으로 보고(추정 금지). SPEC-000 · 002 의 「KOS 칸」 표와 다르면 리포트에 적어라(SPEC 은 planner 가 고침).
- 테스트(DB 없이 mapper) · `uv run pytest -m "not infra"` · ruff · compose down 금지 · worker 만 재빌드.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-feedback-a-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
