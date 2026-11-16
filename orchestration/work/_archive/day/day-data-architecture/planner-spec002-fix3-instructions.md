# [planner] DAY-SPEC-002 fix3 — 재검수 M1 · M2 · M3 + 의사 호출 창 모양

너는 SPEC-002 planner 다. 같은 mediness 워크트리 · 미커밋. 커밋 금지.
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec002-fix2-report.md` M1 ~ M3 · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` 「화면 참고 — 의사 호출 창」(사용자 스크린샷 · 2026-11-06).

1. **M1** — 실패 토스트를 싣는 길: 리뷰어 고칠 방향대로(실패 칸 · 한 번만 뜨는 기준). OQ-01(웹 = 화면 라우트 HTML 조각 · SSE 는 신호) 구조 안에서.
2. **M2** — 실패 뒤 멈춘 op 상태: 리뷰어 방향(cc r2 N2 — `failed` + 막힌 op 표시로 옮김 · 「토큰 없음 `pending`」(규칙 24)과 구분) · 그래야 「KOS 에서 고치면 폴링이 맞춘다」(OQ-07)가 덮어쓰기 보호에 막히지 않는다.
3. **M3** — S2 OQ-11 의 「SPEC-000 변경 없음」 문구 · log 를 맞춘다. SPEC-000 `staff.is_system_account` 설명 고치기는 **다른 지시(planner-spec001-csrf-delivery227-v3)에서 이미 했으니** 그 결과와 문구를 맞추기만.
4. **의사 호출 창(E51)** — 원천 「화면 참고」대로 화면 구성 절에: 모달 · 머리(「의사 호출」 + 방 · 고객) · 왼쪽(검색 · 추천 · 「모든 의사」(설명 「콜 잡은 원장이 집도」) · 원장 줄 = 아바타 · 이름 · 원장 상태) · 오른쪽(선택됨 · 호출할 시술 N개 목록) · 아래 버튼(고르기 전 꺼짐 「의사를 선택하세요」). 재호출도 같은 창 · 기본 = 처음 대상. 시안과 다른 곳이 있으면 원천이 이긴다.
5. SPEC-001 이 이번에 CSRF(403 `csrf_failed`)를 정했으니 S2 의 OQ-16 을 그 줄 참조로 닫는다.
6. log 한 줄 · lint `--strict` 1회.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-fix3-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
