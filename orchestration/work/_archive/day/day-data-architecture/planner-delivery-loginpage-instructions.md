# [planner] Delivery(WP) 새로 — 로그인 화면(웹) · #229 다음

너는 day planner 다. 앞 Delivery 와 같은 방식(`start-delivery` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/delivery/`). 새 Issue 하나 · **승인 안 함**. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` 파일은 SPEC 에 화면 절이 필요할 때만(아래 3).

## 사용자 결정 (2026-11-06)
- 로그인 화면은 **medikit HTMX 기반(#229)이 끝난 뒤** 따로 한다 — #229 매크로로만 조립.
- 시안이 없다 → **centurion admin 로그인 화면 모양**(`git -C /Users/kknaks/git/centurion show origin/main:backend/admin/templates/<로그인 템플릿>` · `routers/session.py`)을 따른다. 시안이 나오면 그때 맞춘다.

## 계약
1. target: **DAY-SPEC-001**(경로 4 · 오류 매트릭스 · CSRF · 빈 입력) — 화면은 이미 있는 API(#227 · PR #228 `fb2508e4`)를 부른다(웹 = 화면 라우트 HTML 조각 원칙 — SPEC-002 OQ-01 결정과 같은 구조).
2. 범위: 로그인 페이지(이메일 · 비밀번호 · 오류 문구 = SPEC-001 매트릭스 줄마다) · 병원 여럿이면 병원 고르기 · 로그아웃 · 로그인 안 한 요청은 로그인으로 보냄 · 로그인 뒤 갈 곳(1차 = 견본 페이지 또는 빈 홈 — 시술 현황은 #231 뒤).
3. SPEC-001 에 화면 문구 · 흐름이 없으면 그 절을 SPEC-001 에 더하는 것도 계약 phase 로(문구는 매트릭스의 뜻 그대로 · 발명 금지 — 모르는 건 OQ).
4. 의존: #229(매크로 · base.html · CSRF hx-headers) · #227. 하지 않는 것: 시술 현황 · 앱 로그인 · 디자인 새로 만들기.
5. Acceptance: 브라우저 실물 — 데모 지점 계정으로 로그인 → (병원 고르기) → 로그인 뒤 화면 → 로그아웃 · 오류 화면(틀린 비밀번호 · 빈 입력) 스크린샷 · 손 CSS 0 · 인라인 스크립트 0.
6. 담당: frontend(라우트 · 템플릿) — 백엔드 변경이 필요하면 최소로 계약에.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery-loginpage-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
