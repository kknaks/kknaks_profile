# WORK-010 고객 문진 웹 — frontend · mobile (코디 · 2026-10-28)

계약 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-006-customer-questionnaire-web.md` 0.1.0 · `30-work/work-010-customer-questionnaire-web.md`(내 WP 줄) · DEC-008 · SPEC-004 0.4.2 · SPEC-005 0.4.1 · 결정 `_RESUME` §2 10-28 「고객 문진 웹 OQ 사용자 몫 = 추천대로」(미리 채움 그대로 · QR 만 · 안드로이드 E2E · KOS 없이 원천은 나중).
코드 워크트리 브랜치 `kknaksss/overall-board-6`(origin/main `fad8b56` · 체크아웃됨). backend 가 같은 워크트리에서 먼저 여권 사진 수정 → 그다음 WP-BE 를 한다 — **back 이 아직 없으면 가짜 응답으로 화면부터** · 모양은 SPEC-006 §7 그대로 · 다르면 멈추고 물어라.
- **frontend = WP-FE**(`procedure/front/**` 만) — 고객 페이지 `/q`(로그인 없음 · 직원 세션과 분리) · 데스크 QR 상자 · 검증 `tsc` · `lint` · 스크린샷(아이폰 · 안드로이드 폭) `fe-shots-reservation/q-*.png`
- **mobile = WP-APP**(`procedure/app/**` 만) — 문진 띄우기 = QR 화면 · 앱 문진 화면(APP5) · unlock 제거 · 검증 `flutter analyze` · `flutter test`(`/Users/kknaks/fvm/versions/3.44.8/bin/flutter`)
- 커밋 · push 금지 · 사용자 포트 금지 · 실명 금지 · 보고서(frontend `app-fe-report.md` / mobile `app-mobile-report.md`)에 「WORK-010」 절 + 두 명령(코디 `term_678ac61d-2472-4a9b-ba73-61883337b957`)
