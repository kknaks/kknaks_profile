# [planner] Delivery(WP) 새로 — 시술 현황 1차 (DAY-SPEC-002)

너는 day planner 다. 앞 Delivery 와 같은 방식(`start-delivery` 스킬 · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/delivery/`). 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`(SPEC-002 커밋됨 `3c14633b` · PR #909 미머지 → spec-baseline pending). **승인하지 마라.**
target: **DAY-SPEC-002**(+ SPEC-000 · SPEC-001 참조). 정본은 SPEC-002 본문 · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`.

1. **Issue 를 둘로 나눈다** — ① 백엔드: 시술 작업(`visit_task` · `visit_task_staff`) · 상담 동기화 추가분 · 동작 서비스(호출 · 재호출 · 수락 · 시작 · 종료 · 되돌리기 · 마취 · 순서 · 귀가 대기) · 화면 라우트(HTML 조각 — 단 템플릿은 ②) · 앱 JSON · KOS 쓰기(outbox · `SUPPORTED_WRITES` 를 HAR 확인된 것만 열기 · #226 검수 W7 outbox 구멍 닫기 · `(visit_id, seq)` 유일 migration) · SSE · 토스트 신호 ② 화면: 시술 현황 템플릿 · HTMX · `day.js` — **#229 매크로만**으로 조립.
2. 의존: ① ← #226 · #227 / ② ← #229 · ①. 「먼저 계약(라우트 · 조각 이름 · SSE 이벤트) → 화면」 순서를 계약에 적는다.
3. **첫 실제 KOS 쓰기**가 생긴다 — 위험 L3 · 실물 확인은 **데모 지점에만 · 사용자 허락 뒤**로 계약에 적는다(지금까지 KOS 는 조회만 했다).
4. HAR 요청 6개(SPEC-002 §5)는 확인 안 된 쓰기를 열지 않는 근거로 Non-Goal/Review Surface 에.
5. 테스트 규칙(레포 AGENTS.md 「테스트」 2026-11-06) — 도메인 규칙은 DB 없이.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery-board-report.md` — Issue 링크 둘 · plan_digest · 계약 요약. 완료는 preamble 의 worker_done 절차대로(둘 다).
