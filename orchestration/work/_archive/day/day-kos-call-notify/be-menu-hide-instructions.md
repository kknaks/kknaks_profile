# [backend] 웹 메뉴 — 예약 현황 · 고객 버튼 막기 (menu-hide)

같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify` — **브랜치가 바뀌었다**: `kknaksss/day-menu-hide`(origin/dev `1b5bba22` 위 · 깨끗함). 앞 작업(#285)은 dev 머지 끝.

## 무엇 (사용자 2026-11-25 「예약현황 버튼 비활성화, 사이드 고객 비활성화 · 막는 버튼만 있으면 될듯」 · dev · prod 둘 다)

- `backend/day/menu.py` `HREFS` 에서 `customer` · `reservation` · `reservation_board` 세 키를 뺀다 → 아이콘 줄 「예약」 · 「고객」과 헤더 탭 「예약 현황」이 **링크 없는 글자**로 그려진다(이 파일 머리 주석의 기존 관례 「화면이 아직 없는 메뉴는 href None — 글자만」 그대로).
- 지운 자리에 한 줄 주석: 「2026-11-25 사용자 — 예약 현황 · 고객 메뉴 막음(화면 · 라우트는 그대로 · 다시 열 때 이 줄 복구)」.
- 라우트 · 템플릿 · 서버 API · 설정값은 **건드리지 않는다**(주소 직접 입력은 열림 — 사용자 확인).
- 이 세 href 를 기대하는 시험이 있으면 새 기대(링크 없음)로 고친다. 라우트 자체를 부르는 시험(`/customers` · `/reservations` GET)은 그대로 통과해야 한다.
- 다른 화면이 이 세 링크로 이동시키는 곳(템플릿 · `static/day.js` 의 `/reservations` · `/customers` 하드코딩 링크 · 버튼)이 있는지 grep 해서 **목록만** 보고서에 적어라(고치지 말 것 — 코디 판단).

## 검증
`cd backend && uv run pytest -q <menu · 셸 · 바뀐 시험>` 1회 · ruff · format. 로컬 스택(11140)이 이 워크트리에서 떠 있다 — 재시작 금지 · 리로드되면 `curl -s http://127.0.0.1:11140/login` 200 만 확인. 커밋 · push 금지.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-menu-hide-report.md` · 완료 보고 두 명령(subject 「backend 완료: menu-hide」 · 이번 dispatch 값 · 코디 term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce):

```bash
orca orchestration send --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: menu-hide" --body "<요약>"
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[worker_done] backend 완료 — menu-hide <한 줄>. 상세는 인박스." --enter
```
