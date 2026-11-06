# [planner] Delivery(WP) 새로 — DAY 웹 기반 · medikit HTMX 컴포넌트 (시술 현황 화면보다 먼저)

너는 day planner 다. #224 ~ #227 Delivery 를 만든 방식(`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/delivery/*.json` · mediness `start-delivery` 스킬)을 그대로 쓴다. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`(미커밋 SPEC 변경 있음 — 건드리지 마라). 새 Issue 하나(CENTURION_DAY). **승인하지 마라**(사용자 몫).

## 사용자 결정 (2026-11-06)

- 화면 구현 전에 **medikit HTMX 기반부터** 만든다. 시술 현황 화면은 그 매크로만으로 조립한다.
- 새 컴포넌트는 **DAY 레포 안**(`backend/day/templates/ui.html` 매크로 · `backend/day/static/` · `backend/day/styles/`). centurion 키트는 가져다 쓰기만 하고, 새로 만든 건 「키트로 올릴 후보」 목록으로 남긴다.
- CRM 브랜드색 · 고객 상태 팔레트는 **DAY 토큰 파일에서 medikit 토큰을 확장**한다.

## 계약에 넣을 것

- 정본 근거: 레포 `AGENTS.md` 「웹 화면」 · centurion 키트 `git -C /Users/kknaks/git/centurion show origin/main:docs/development/medikit-htmx-kit/README.md`(+ `medikit.css` · `medikit.js` · `example.html`) · `medikit-htmx-design-guide.md` · centurion admin `backend/admin/templates/{base,ui}.html` · `web.py` · DS 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-ds-research-report.md`(HTMX 에 없는 6개 · gap G1 ~ G17 · 토큰 밖 값) · 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`(의사 호출 창 모양 · 「수납 필요」 등) · SPEC-002(미커밋 — 화면 구성 절 · E번호).
- 바뀌는 것: 키트 가져오기(+ htmx 벤더링 · 라이선스) · `base.html`(셸 G1) · `ui.html` 매크로(기존 btn · input · badge · chip · banner · card · table + **HTMX 에 없는 6개**: 툴팁 · 팝오버 · 콤보박스 목록 · 아코디언 · 토스트 · 체크박스 혼합 + **시술 현황에 필요한 gap**: 밀집 카드 · 사각 배지 · 시술 행 · 실시간 경과 · D&D 순서 · 하단 액션 바 · 의사 아바타 · 의사 호출 모달 등 — DS 조사 G 번호로) · DAY 토큰 확장 파일 · (이벤트 위임 + data-* · 인라인 스크립트 금지) · **컴포넌트 견본 페이지**(dev 에서만 열림 · 리뷰 기준).
- 하지 않는 것: 시술 현황 화면 · 업무 라우터 · API · 로그인 화면 · 앱 · centurion 키트 수정.
- 완료 조건 예: 견본 페이지에서 모든 매크로가 상태별로 보인다 · 손 CSS 0(토큰 · 클래스만 — grep 기준) · 인라인 스크립트 0 · 매크로마다 시안 요소 번호 대응표 · 「키트로 올릴 후보」 목록 · 브라우저 실물 확인(스크린샷).
- 의존: CSRF `hx-headers` 연결은 #227(`session.py` · CSRF)이 PR #228 브랜치에 들어온 뒤 — 계약에 순서로 적는다.
- 담당 워커: frontend.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery-webkit-report.md` — Issue 링크 · plan_digest · 계약 요약. 완료는 preamble 의 worker_done 절차대로(둘 다).
