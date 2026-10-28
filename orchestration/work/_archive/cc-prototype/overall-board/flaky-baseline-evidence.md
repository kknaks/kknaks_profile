# flaky 판정 — overall-board (2026-10-23)

- `procedure/front` `npm run build` 첫 실행이 가끔 Next.js 보안 권고 조회(registry.npmjs.org/-/npm/v1/security/advisories/bulk) 실패로 `exitCode: 1` 로 멈춘다. 재실행하면 통과(코디 재현: 1회차 실패 → 2회차 통과 · 라우트 5개 static). 이번 변경과 무관 — 네트워크 조회. `next` ^16.4.0 업그레이드 권유는 범위 밖(사용자 결정 전 안 함).
