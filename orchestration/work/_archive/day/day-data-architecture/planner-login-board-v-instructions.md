# [planner] 사용자 결정 반영 — SPEC-001 화면 절 닫기 + #232 contract v2 + #230 contract v3(W6)

너는 day planner 다. mediness 워크트리 · 미커밋 · 커밋 금지 · **Delivery 승인 금지**.
원천(사용자 2026-11-06 · 「추천안으로 가자」): `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md` 「웹 화면 문구 · 흐름」 줄 · `.../screen/procedure-board-decisions.md` 「결정 — #230 계약 검수에서 올라온 것」.

1. **SPEC-001 화면 절 닫기**: 문구 13줄 추천안 확정 · 숨은 폼 칸 · 이메일 유지 · 비밀번호 비움 · 갈 곳 — 「아직 열린 것」에서 걷어 「정함(사용자 2026-11-06)」. 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-screen-report.md` N1 도 이로써 닫힘. log 한 줄 · lint `--strict`.
2. **#232 contract v2**(같은 Issue · key): 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery232-report.md` W1 ~ W5 + `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-screen-report.md` 4절 ① ~ ⑤(웹 화면 라우트 새로 · 쿠키 심기를 웹 라우트로 · JSON `client` 기본값 app · 웹 로그아웃 · CSRF 미적용 주석 · 미로그인/만료/권한/CSRF 를 HTML 로 내는 의존성 · 「백엔드는 라우트 · 리다이렉트만」 문장 고침). target = SPEC-001 화면 절(인용) · phase 1 · A6 · code_surface 의 mediness 줄 삭제.
3. **#230 contract v3**(같은 Issue · key): W6 = 「HAR 확인 안 된 동작(귀가 대기 · 시작 취소 · 완료 취소 · 재호출 재전송)은 KOS 쓰기를 닫는다 · DAY 동작은 함 · 폴링이 되돌릴 수 있음(감수) · HAR 들어오면 확인된 값만」 — Acceptance 를 그 처리로. **W8(데모 원장 계정)은 열린 채**(A8 실물 확인의 수락 단계 = 계정 받은 뒤).
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-login-board-v-report.md` — 바뀐 항목 · plan_digest 둘. 완료는 preamble 의 worker_done 절차대로(둘 다).
