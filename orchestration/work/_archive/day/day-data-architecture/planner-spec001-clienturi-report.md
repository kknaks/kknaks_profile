# planner-spec001-clienturi 결과 보고 — done (미커밋)

- `products/day/20-spec/spec-001-login-session.md` 규칙 10 아래 한 줄: `kos-client-uri` 단계별 모양(근거 HAR `로그인.har` · 값은 옮기지 않음) — sign-in `<web>/auth/sign-in` · get-user-tenants `<web>/hospital/select` · get-user-account `<web>/<tenant>`(고른 병원) · 병원 고르기 전에는 연결 설정 `tenant_id` 에 기대지 않는다.
- `products/day/log.md` 2026-11-06 `spec-change` DAY-SPEC-001 한 줄.
- lint `--strict` → 0 error · products/day 경고 0.
- spec-002 · Issue #227 은 건드리지 않았다 — #227 A10 인용은 PR #909 머지 뒤 v4 에서.
- HAR 직접 대조: 로그인.har 의 sign-in · get-user-tenants · get-user-account 요청 `kos-client-uri` 모양이 위 셋과 같다(값은 보지 않고 호스트 · 테넌트를 치환해 모양만).
