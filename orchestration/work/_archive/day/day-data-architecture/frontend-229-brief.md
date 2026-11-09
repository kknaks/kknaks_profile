# [frontend] Delivery #229 — DAY 웹 기반 · medikit HTMX 컴포넌트(매크로 · 토큰 · 견본 페이지)

너는 day frontend 워커다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/frontend/`. 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — #224 ~ #227 커밋 위에 이어서(PR #228 하나 · 사용자 결정). 다른 워커 없음.

## SSOT

- **계약 = Issue #229 contract v2** `gh issue view 229 -R MediSolveAIDev/CENTURION_DAY` — 바뀌는 것 · 대응표(SPEC-002 1차 화면 요소 전부) · Acceptance · Non-Goals · phase 순서. 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery229-report.md` · `review-delivery229-v2-report.md`(PASS · 「참고」 둘).
- 사용자 결정: 새 컴포넌트는 **DAY 레포 안**(`backend/day/templates/ui.html` 매크로 · `static/` · `styles/`) · centurion 키트는 가져다 쓰기만 · 새로 만든 것은 「키트로 올릴 후보」 목록 · **CRM 브랜드색 · 고객 상태 팔레트 = DAY 토큰 파일에서 medikit 토큰 확장**.
- 레포 `AGENTS.md` 「웹 화면」(HX-Request 조각 · `day.js` 하나 · 이벤트 위임 + data-* · 인라인 스크립트 · eval 금지 · htmx 벤더링 + 라이선스 · medikit 토큰 · ui.html 클래스만 · 빌드된 CSS 커밋).
- 본(모양만 · 고치지 마라): centurion `git -C /Users/kknaks/git/centurion show origin/main:<경로>` — `docs/development/medikit-htmx-kit/{README.md,medikit.css,medikit.js,example.html}` · `docs/development/medikit-htmx-design-guide.md` · `backend/admin/templates/{base,ui}.html` · `backend/admin/{web,main}.py` · `backend/admin/static/` · `backend/admin/styles/`.
- 화면 정본: SPEC-002 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-002-procedure-board.md` 화면 구성(E 번호) · 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html`(생김새) · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`(의사 호출 창 모양 · 「수납 필요」) · DS 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-ds-research-report.md`(HTMX 에 없는 6개 · G1 ~ G17 · 토큰 밖 값).
- **CSRF `hx-headers` 연결**(계약 마지막 phase): #227 이 이미 커밋됨(`fb2508e4` — `backend/day/session.py` · CSRF). `base.html` 한 곳에 centurion admin 처럼.

## 하지 말 것

시술 현황 화면(#231) · 업무 라우터 · API · 로그인 화면 · 앱 · centurion 키트 수정 · 손으로 쓴 색 · 치수(토큰 · 클래스만) · 인라인 스크립트 · `hx-on`. 커밋 금지. 포트 11040 · 11042 · 11043 만, 끝나면 `down`. 사용자 포트 · 브라우저 프로세스 건드리지 마라.

## 검증 · 보고

- 계약 Acceptance 그대로: 견본 페이지(dev 에서만)에서 매크로가 상태별로 다 보임 · 손 CSS grep 0 · 인라인 스크립트 grep 0 · 대응표(E 번호 ↔ 매크로 ↔ 그린 상태) · 「키트로 올릴 후보」 목록 · **브라우저 실물 스크린샷**(견본 페이지 · 주요 컴포넌트 · 리포트 옆에 png 로 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-229-shots/`).
- `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff — 템플릿 렌더 테스트가 있으면 DB 없이.
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-229-report.md`. 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` 둘 다).
