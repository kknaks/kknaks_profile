# [backend] WP10 fix1 — 상담 종료 뒤 「귀가 대기」 오표시

`wp10-be-report.md` 미결 (2): 상담 종료 뒤 후보만 있고 남은 단계가 없으면 방 상태가 「귀가 대기」(need: discharge). 실제로는 데스크가 후보를 보고 시술을 넣어야 하는 상태다.

- **남은 단계가 없어도, 그 고객에게 아직 동선에 안 넣은 오늘 시술 후보(결제분)가 있거나 미결제 금액이 있으면** 상태 = 「다음 단계 대기」(need: next — 화면 「확인 필요」). 「귀가 대기」는 남은 단계도 · 남은 오늘 후보도 · 미결제도 없을 때만
- 보유 시술권(지난 결제분)만 남은 경우는 「귀가 대기」 그대로(오늘 받을지는 데스크 판단)
- 시험 2개 · `uv run pytest` · `uv run ruff check .` 1회 · `wp10-be-report.md` 끝에 「fix1」 절
- 완료 보고는 WP10 브리프 두 명령(subject 「backend 완료: WP10 fix1 …」, taskId/dispatchId 는 WP10 것 task_a14327d8c49b / ctx_3a642dd0476a)
