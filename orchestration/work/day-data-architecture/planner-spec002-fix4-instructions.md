# [planner] DAY-SPEC-002 fix4 — 재검수 P1 · P2 · P3

너는 SPEC-002 planner 다. 같은 mediness 워크트리 · 미커밋 · 커밋 금지. 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec002-fix3-report.md` P1 ~ P3.
1. **P1** — 웹 `kos_failed` 신호: **SSE `sse-swap` 으로 토스트 HTML 조각을 직접 보낸다**(HTMX `hx-trigger` 고정 URL 문제를 피함 · `GET /board/toasts/{event_id}` 는 빼거나 앱용으로만 · SSE `id:` 필드는 안 씀을 명시). 리뷰어가 낸 두 길 중 이쪽이 코디 결정.
2. **P2** — 의사 호출 창 「추천」 = **「모든 의사」**(시안 L1064 · 원천 순서) · 기본값 OQ-20 을 이 근거로 닫는다.
3. **P3** — 판 버튼 이름을 원천대로 **「의사 호출 · N건」** 으로 본문 전부 맞춘다(grep 으로 전수).
4. log 한 줄 · lint `--strict` 1회.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-fix4-report.md`(짧게). 완료는 preamble 의 worker_done 절차대로(둘 다).
