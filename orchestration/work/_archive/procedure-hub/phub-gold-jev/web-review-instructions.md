# [reviewer_code] 시험 화면 검수 (짧게)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-code-app-brief.md`(같은 폴더)의 역할 · 제약(read-only · 공개 레포 · 실호출 금지 · `.env` 열지 마라 · 허브 18105 · 화면 18220 은 코디가 띄워 둠 — 띄우거나 내리지 마라 · GET 은 됨) · 완료 보고 그대로. 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`.

읽을 것: `WORK-003-web.md` · `_RESUME.md` §2 「시험 화면 추가」 행 · 변경 = `clinic_chat/web/**` · `progress.py` · `runner.py` · `llm/cli.py` · `columns/col_b.py` · `runs.py` · `tests/test_web.py` · `pyproject.toml`.

볼 것: ① 화면 전용 걷기 · 답 · 판정 로직 0(runner 그대로) — runner/col_b/cli 고친 곳이 CLI · batch 동작을 바꾸지 않나 ② 127.0.0.1 만 바인딩 · 포트 18220 ③ 지어 넣은 문구(WORK-003 「문구는 지어 넣지 마라」) — 화면 · API 오류 글 전수 ④ 공개 레포 grep ⑤ ruff · pytest 1회 ⑥ 「사용자가 화면에서 만날 자리」(마크다운이 날 글로 보임 · 열이 차례로 스트리밍 등).

산출: `review-code-web.md` 1개 · 판정 PASS/WARN/FAIL.
