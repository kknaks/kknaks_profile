# backend 수정 1판 — code r1 WARN (WP-LIVE 전)

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r1-report.md` — W-1 · W-2 · W-5 · W-6 을 읽어라.

1. **W-1** — ⑤ 에 수납은 있는데 `APPROVED` 후보가 0 이면 「⑤ 에 수납 없음」과 똑같이: `items_here = (이 달 ① APPROVED 행이 있나)` · `unknown = True`(→ `firstApprovedUnknown`). 시험 1
2. **W-2** — 계약은 안 바꾼다. ① 첫 페이지 `totalCount` 를 읽어 받은 행 수와 다르면 `log.warning("sales month=%s totalCount=%d rows=%d", …)`(숫자만 — 이름 · 금액 · id 금지). 같으면 INFO 로 같은 한 줄. 가짜 transport 가 `totalCount` 를 행 수와 다르게 주는 시험 1(경고 로그가 남는지)
3. **W-5** — 수납 통화 판정에서 `None` 은 뺀다. 통화가 하나도 없으면(줄 0 등) `currency` 는 이 달 ① 행 통화 → 그래도 없으면 `"KRW"` 가 아니라 **섞임이 아님**을 front 가 알 수 있게 SPEC §4.2 범위 안에서 처리(예: 줄 0 이면 합계 칸 0 · `currency` = ① 통화). 계약 필드를 새로 만들지 마라. 시험 1
4. **W-6** — README 실행 명령을 `--port ${SALES_BACK_PORT:-8800}` 꼴로
5. W-3 · W-4 · W-7 은 손대지 마라(SPEC 정리 · 실물 확인 몫)

검증: `cd back && uv run ruff check . && uv run pytest -q` · KOS 호출 0. allowed_paths 는 원 브리프 그대로(`back/` · `README.md` 실행 절). 끝나면 원 브리프 §9 두 채널(같은 task/dispatch · subject 「backend 수정 1판 완료」). **코디handle 은 `term_3605662c-607d-4c3e-8480-a4fdce8f45af`**.
