# [planner] SPEC-008 고침 3 — 검수 3차 FAIL 1 · WARN 1

맥락: `review-doc-3-report.md`(M1 · M2 파일:줄). 같은 워크트리. 코디 기본값 11-26:

- **M1** 스레드 묶음의 쓰기 행은 **공용 다시 시도 두 길(`POST /reservations/visits/{visit_id}/retry` · `POST /reservations/retry`)에서 늘 409** — 스레드 [다시 시도]만 연다. 공용 실패 토스트의 「다시 시도」도 스레드 행이면 스레드를 여는 쪽으로(문구 비움 · OQ-Q04). 접을 때 그 행들은 「접힘」 표시(다시 보낼 수 없음). spec-008:415 · spec-000:677 · SPEC-007 고침 6 에 같은 말.
- **M2** E5 `closedReason` 에 `folded` 더함(뜻 = 병원이 처리를 접음).

lint ERROR 0 · 완료 보고 §9 두 명령 · subject `planner 완료: SPEC-008 고침 3`.
