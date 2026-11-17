# [planner] spec-3 — OQ-K17 한 건 (작은 판)

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-spec-brief.md`(역할 · allowed_paths · 검증)를 따른다. 앞 판 `spec-2-report.md`(같은 폴더). 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec`(미커밋 위에). 커밋 금지.

사용자 결정 A 의 뜻 = **「심사 중 앱 화면은 지금과 같음」**(사용자 2026-11-17 — 앱은 다음 버전에서 같이 고침). 그래서 OQ-K17 을 닫는다:
- 앱 JSON 로그인(`/api/auth/login` 등)은 기기 제한이어도 **지금과 똑같이 401 `invalid_credentials`** 를 돌려준다(새 코드 `kos_signin_limit` 쓰지 않음 · 깔린 앱이 코드 글자를 보지 않게). 원인 오안내는 알고 감수 · 다음 앱 버전 때 앱 전용 처리. 서버 로그에는 기기 제한임을 남긴다(이메일 · 비밀번호 없이).
- 웹(`/login`)만 기기 선택 단계.
- SPEC-001 · SPEC-003 ⑱ · 케이스 매트릭스 · OQ-K17 행을 이에 맞춰 고친다.

lint --strict products/day ERROR 0. 리포트 `…/kos-signin-limit/spec-3-report.md`(짧게). 완료 보고는 preamble 의 worker_done.
