# [frontend] WORK-012 Phase SHELL — 셸 코드만 (dmg 는 코디)

기존 구현 브리프 규칙 그대로(커밋 금지 · 포트 금지). **이번 판만 allowed_paths 에 `frontend/src-tauri/` 를 연다.** WP1~3 커밋 위 · WP4-FE 변경은 워크트리에 그대로 둔다(건드리지 마라).

- 할 일: `P/30-work/work-012-enhance.md` **「Phase SHELL」** 의 **011** 만 — 이동 허용(`on_navigation`)에서 `about:blank` · `about:srcdoc` 를 허용. 외부 origin 차단 · OS 브라우저 열기 · `/api/` 가로채기는 **그대로**. wry 정책 콜백엔 프레임 구분이 없다(Open Issues I-1 · 네 조사 `W/fe-survey-report.md` §1-2) — 그래서 주 프레임의 `about:blank` 이동도 허용되게 된다: 그것이 안전한지(앱 origin 밖으로 나가지 않는지) 리포트에 판단 근거를 적어라
- **dmg 빌드·서명·공증은 하지 마라** — 코디가 RUNBOOK-002 로 E2E 전에 한 번 만든다
- 013 ②③ GUI 체크리스트는 코디가 dmg 와 함께 사용자에게 전한다(너는 할 일 없음)
- 검증: `cargo test`(판별 시험 `lib.rs` 개정 — about:blank/srcdoc 허용 · 외부 origin 여전히 취소 · /api/ 가로채기 그대로) · `make shell-verify-strict` · `make shell-final-preflight`(서명 없이 되는 것까지). 관련 것만
- 리포트 `W/fe-shell-report.md` · 완료 보고 두 명령(subject 「frontend 완료: SHELL」) · **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
