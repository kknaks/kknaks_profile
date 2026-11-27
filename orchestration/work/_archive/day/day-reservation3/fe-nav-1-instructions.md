# [frontend] 셸 메뉴 정리 — 「홈」→「현황」 · 현황 탭 셋은 현황 아래 · 로그인 뒤 = 예약 현황 (fe-nav-1)

너는 day `frontend` 워커다. 맥락이 없으면 먼저 읽어라: 브리프 `day-reservation3-fe-brief.md`(규칙 · 완료 보고 §9 그대로) · 코드 레포 `AGENTS.md`.

워크트리 그대로: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3` (미커밋 변경 위에 이어서 · 커밋 · push 금지). backend 워커가 같은 워크트리에서 ext 스웨거 설명을 고치는 중이다 — `day/schemas/ext_*` · `day/routers/api/ext*` · `docs/development/deployment.md` 는 건드리지 마라.

## 사용자 결정 (11-27)

- 왼쪽 아이콘 줄 **「홈」 → 「현황」** 으로 이름을 바꾼다.
- 헤더 탭 **예약 현황 · 원내 현황 · 시술 현황** 은 모두 **「현황」 아래** 에 속한다. 지금은 예약 현황 = 「예약」, 시술 현황 = 「시술」 아이콘이 켜진다 → 둘 다 「현황」이 켜져야 한다.
- **로그인 뒤 갈 곳 = 예약 현황**(`/reservations`). 지금은 시술 현황(`/board`, 사용자 2026-11-06 결정을 이번에 바꿈).
- 화면이 있는 메뉴 = **고객 · 현황** 뿐. 「예약」 · 「시술」 · 「매출」 · 「설정」은 화면 없음(링크 없는 글자 — 지금 「홈」 · 「매출」처럼).

## 고칠 곳 — 목록이 아니라 전수조사로

- 출발점: `backend/day/menu.py`(RAIL · TABS · HREFS) · `backend/day/routers/login.py` `after_login()` · `/` 경로 · `active_menu=` 를 넘기는 모든 라우터(`grep -rn "active_menu=" backend/day` — board · kit · kit_board · reservations · customers …).
- **「홈」 · `"home"` · `after_login` · `"/board"` 가 로그인 뒤 기본값으로 쓰이는 곳 · `active_menu="procedure"` · `active_menu="reservation"` 을 전부 grep** 해서 센다(템플릿 · JS · 앱 웹뷰 진입 · 시험 포함). 권한 없음 화면이 「갈 곳」을 가정하는 곳도.
- 화면 문구 시험(`tests/architecture/test_screen_copy.py` 등)에 「홈」이 박혀 있으면 같이.
- 키 이름(`home` → 다른 이름)을 바꿀지는 네가 정하되 리포트에 적는다. 글자는 「현황」.

## 확인할 것 (리포트에)

- 예약 현황 보기 권한이 없는 직무가 로그인하면 무엇이 뜨나(지금 `/board` 일 때와 같은 「권한 없음」 규칙인지). 다르게 할 곳이 보이면 고치지 말고 질문으로.
- 앱(Flutter) · 태블릿이 웹 `/` 나 `/board` 를 기본 진입으로 쓰는지 grep(있으면 고치지 말고 보고).

## 검증

- 관련 시험(로그인 · 셸 메뉴 · board · reservations 페이지 렌더 · screen copy) + `scripts/check.sh --pure` 통과. 마지막에 `scripts/test.sh` 전체 한 번.
- 로컬 스택(11140)은 코디가 띄운 것 — 재시작하지 않는다. 코디가 확인한다.

## 리포트 `fe-nav-1-report.md` (이 폴더)

① 고친 파일:줄 ② grep 으로 센 자리 표(자리 · 고침/그대로 · 이유) ③ 권한 없음 · 앱 진입 확인 결과 ④ 검증 수치 ⑤ 스펙에 고칠 줄(SPEC-001 「로그인 뒤 갈 곳」 등 — 코디가 spec 마감 때 반영).

완료 보고는 브리프 §9 두 명령 그대로 · subject `frontend 완료: 셸 메뉴 현황 · 로그인 뒤 예약 현황`.
