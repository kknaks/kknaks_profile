# [frontend · 조사] 시술 현황 시안 — medikit 에 있는 컴포넌트 / 없는 컴포넌트(DS gap) 목록

너는 day frontend 워커다 — 이번은 **읽기 전용 조사**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/frontend/`(role · rules — 웹 = Jinja2 + HTMX · medikit 토큰 · ui.html 매크로).
**코드 · 문서 · 시안 파일을 고치지 마라. 커밋 금지.** 산출물은 리포트 1개뿐이다. 다른 워커(backend)가 CENTURION_DAY 워크트리에서 일하고 있다 — 그 워크트리는 열지 마라.

## 배경 (사용자 2026-11-05)

시술 현황 화면 시안을 아래 파일로 잡는다. 시안은 medikit 을 썼지만 **medikit 에 없는 컴포넌트가 섞여 있다.** 화면을 만들기 전에 무엇이 있고 무엇이 없는지 알아야 한다.

## 읽을 것

1. **시안**: `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` (한 파일 · 이미지는 data URI 로 들어 있음 · 약 3MB). 브라우저로 열 수 없으면 HTML · CSS 구조를 읽어라.
2. **medikit React 라이브러리**(원본): `/Users/kknaks/git/medikit` — `src/` 컴포넌트 목록 · props · 토큰(`tailwind.config.ts`)
3. **DAY 가 실제로 쓸 HTMX 키트**: `git -C /Users/kknaks/git/centurion show origin/main:docs/development/medikit-htmx-kit/README.md` (+ `medikit.css` · `medikit.js` · `example.html`) ·
   `git -C /Users/kknaks/git/centurion show origin/main:docs/development/medikit-htmx-design-guide.md` · centurion admin `backend/admin/templates/ui.html`(매크로)
4. 참고: cc-prototype 시술 현황 화면(`/Users/kknaks/git/toy_pr2/cc-prototype` `procedure/front/`) — 같은 화면의 이전 구현

## 할 일

1. 시안의 화면 구성 요소를 **빠짐없이** 뽑는다(셸 · 헤더 · 필터 · 카드 · 배지 · 칩 · 타이머 · 드래그 영역 · 모달 · 토스트 · 아이콘 …). 화면 위치와 상태(빈 · 선택 · 진행 중 · 경고 등)까지.
2. 요소마다 대응을 적는다:
   - medikit React 컴포넌트(있으면 이름 · props)
   - HTMX 키트 클래스 / admin `ui.html` 매크로(있으면 이름)
   - **판정**: 그대로 있음 / 비슷한 것 있음(무엇이 다른지) / **없음(DS gap)**
3. DS gap 마다: 생김새 · 동작 · 시안에서 쓰는 곳 · medikit 토큰만으로 만들 수 있나(새 색 · 치수가 필요한가) · 비슷한 medikit 컴포넌트 확장으로 될지.
4. 시안이 medikit 토큰 밖의 색 · 글꼴 · 치수를 쓰는 곳.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-ds-research-report.md` — 요약(있음 n · 비슷 n · 없음 n) · 요소별 표 · DS gap 상세 · 토큰 밖 값 · 확인 못 한 것. 근거는 파일:줄(또는 시안 안 위치).
완료는 preamble 의 worker_done 절차대로.
