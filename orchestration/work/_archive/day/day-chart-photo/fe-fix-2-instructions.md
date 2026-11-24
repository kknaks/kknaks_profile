# [frontend] fix-2 — 코드 검수 review-code-1 W3 · W6 반영

읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/review-code-1-report.md` W3 · W6 · 결정 C21-기본값(`…/reference/2026-11-24-day-picture/chart-photo-decisions.md`).

- W3: 저장 요청이 나가 있는 동안 그 탭 글 · 담당자 칸 잠금(readonly · 버튼처럼 응답 뒤 풀림 · 실패 · 타임아웃이면 풀고 바뀐 줄 유지). 화면 테스트 · node 테스트로 「보내는 중 입력 불가 · 응답 뒤 풀림」.
- W6: `.agents/skills/verify-day-web/SKILL.md:130` 자동 저장 문장 → [저장].

검증: 화면 pytest · `npm run -s check` · ruff. backend 가 병렬로 서비스 · policies 를 고친다 — 건드리지 마라. 커밋 금지. 보고 `fe-fix-2-report.md` + preamble worker_done 두 채널.
