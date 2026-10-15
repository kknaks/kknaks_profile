# [backend] WP7c — 고객 이름의 국적 접두(`[TW] ` 등) 떼기

사용자 결정(2026-10-13): 화면에 국적 칩이 따로 있으므로 이름 앞 `[TW] ` · `[HK] ` · `[JP] ` 같은 접두를 뗀다.

- `cc/back` 에서 고객 이름을 내보내는 모든 응답(board · home · patients · 예약 목록 · 로그인 무관)에서 `^\[[A-Z]{2}\]\s*` 를 뗀 이름을 쓴다. 시드 build 에서 한 번 떼어 저장하는 쪽이 간단하면 그렇게
- 국적 값(`nationality`)은 그대로
- 메모 본문은 건드리지 않는다
- 시험 1개 추가 · `uv run pytest` · `uv run ruff check .` 1회 · 끝나면 `seed build` 로 `data/seed.json` 다시(8600 · `data/cc.db` 로 시험 금지는 그대로)
- 리포트: `wp7b-be-report.md` 끝에 「WP7c」 절
- 완료 보고는 WP7b 브리프 §5 두 명령(subject 「backend 완료: WP7c 이름 접두 …」, taskId/dispatchId 는 WP7b 것 task_ecd9746f97f3 / ctx_47048ac349b1)
