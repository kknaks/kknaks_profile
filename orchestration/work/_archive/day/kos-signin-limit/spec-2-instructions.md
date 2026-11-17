# [planner] spec-2 — 사용자 결정 2 · 검수 WARN 6 반영

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-spec-brief.md`(역할 · allowed_paths `products/day/` · 제약 · 검증)를 따른다. 앞 판 `spec-report.md` · 검수 `review-doc-1-report.md`(같은 폴더). 작업 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec`(미커밋 위에). 커밋 · push · Delivery 수정 금지(재결속은 코디가 나중에).

## 사용자 결정(2026-11-17) — 반영
1. **기기 선택 단계는 웹만.** 앱 로그인 API(`/api/auth/login` 등)는 지금처럼 — 기기 제한이면 **오류로** 돌려준다(새 단계 응답 없음). 깔린 앱이 `unexpected_response` 를 보지 않게. 앱 오류 코드: 지금 앱이 아는 코드 중 무엇으로 보낼지 코드 사실(앱 `copy.dart` 등)로 정해 기본값으로 적되, 새 코드면 앱에 어떻게 보이는지 적어라. 앱 기기 선택 화면은 **다음 앱 버전**(사용자). SPEC-003 ⑱ 도 이에 맞춰 고침(W-6 같이 해소).
2. **시스템 계정 = 막혔을 때 같은 환경(UA 정확히 같음) 세션 중 가장 오래된 하나만** 해제 → 재시도 1회. OQ-K1 닫음.

## 검수 WARN — 반영
- W-1 임시 토큰 종류 구분(기기 토큰이 `/login/hospital` 로 오면 500 — `auth.py:82 · :234`) → 종류가 다르면 `session_expired`.
- W-2 「병원 고르기와 같은 처리」 근거 문장을 코드 사실대로.
- W-3 시스템 계정 해제 주체 = worker 병원별 어댑터(api 아님)로 정정 · 위 결정 2.
- W-4 시스템 계정 해제 4xx 처리 = 로그만 남기고 재시도 없이 실패(무한 반복 없음) — 기본값 꼬리표.
- W-5 「처음으로」 = **두지 않음**(KOS 화면에 없음 · 화면 글자 짓지 않음).
- W-6 → 결정 1 로 해소.

`python3 scripts/lint-pipeline.py --strict` products/day ERROR 0. 리포트 `…/kos-signin-limit/spec-2-report.md`. 완료 보고는 preamble 의 worker_done.
