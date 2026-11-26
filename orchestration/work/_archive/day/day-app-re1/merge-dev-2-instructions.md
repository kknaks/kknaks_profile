# [backend] merge-dev-2 — 코드 브랜치 ← origin/dev · 스펙 브랜치 ← origin/main 합치기

너는 day `backend` 워커다. 역할 문서 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/backend/role.md`(+ 같은 폴더 rules · workflow). 이번만 **`app/` 과 스펙 워크트리도 건드린다**(합치기 충돌 풀기 한정).

## 배경

WORK-002(앱 예약현황 탭 · 문진 QR · 여권 스캔 · 태블릿에 보내기)는 dev `55e60aa4` 위에서 만들었다(코드 커밋 `fb08fe4e` · `ab8f6553` · 미push). 그 사이 dev 에 3 커밋(87 파일 · +8081)이, 스펙 main 에 4 커밋이 들어왔다. 둘 다 합친다. **dev · main 쪽 동작은 그대로 살리고 우리 기능을 그 위에 얹는다** — 어느 쪽 기능도 빼지 마라.

- 코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` · HEAD `ab8f6553` · 대상 `origin/dev` `d03baacb`
  - `1b5bba22`(#285 KOS 원장 호출 알림) · `de0d0dab`(#286 웹 메뉴 「예약 현황」 · 「고객」 링크 막음 — **그대로 둔다**, 되살리지 마라) · `d03baacb`(#292 방별 순 · 「방 배정」 자동 완료 · KOS 담당자 = 누른 직원)
  - 충돌 5: `app/lib/ui/theme.dart` · `backend/day/routers/api/board.py` · `backend/day/services/board_events.py` · `backend/day/static/day.css`(생성 파일 — 손으로 풀지 말고 `scripts/build-css.sh` 로 다시 생성) · `backend/tests/architecture/test_api_contracts.py`
  - 자동 합쳐지는 겹침 8: `app/lib/core/copy.dart` · `backend/day/emr/base.py` · `backend/day/emr/kos/__init__.py` · `backend/day/schemas/events.py` · `backend/day/static/day.js` · `backend/day/styles/app.css` · `backend/tests/architecture/test_screen_copy.py` · `scripts/frontend/tests/fixtures/reservations-page.html` — 자동이라도 **뜻이 맞는지 열어 본다**(특히 KOS 쓰기 인터페이스 = 우리 여권 스캔 고객 수정 · 사진 · 문진 제출이 쓰는 곳 · 이벤트 종류 · 화면 글자 레지스트리)
  - migration: dev 새 것 없음 → 우리 `0029` 가 head 로 이어지는지 확인
  - #286 으로 메뉴 링크가 빠져 `reservations-page.html` 픽스처 · 예약 화면 시험이 바뀌었다 — 우리 예약 상세 버튼 시험과 같이 통과해야 한다
- 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` · HEAD `a018f4fa`(PR #964 draft) · 대상 `origin/main` `ae8cec61`(#965 · #966 · #967)
  - 충돌 6: SPEC-002 · 003 · 005 · 007 · `30-work.md` · `log.md`
  - 개정 번호 · 규칙 번호 · OQ 번호가 main 과 겹치면 **main 쪽 번호를 그대로 두고 우리 것을 뒤로 다시 매긴다**(본문 · 다른 문서 · `30-work` · `log` 안 참조까지 grep 으로 전부 따라 바꾼다). 바꾼 번호 대응표를 리포트에
  - log · 30-work 는 두 쪽 행 다 남김(날짜 순)

## 방법

1. 두 워크트리 모두 `git merge --no-commit --no-ff <대상>` — **커밋 · push · rebase · stash · reset 금지**. 충돌을 다 풀고 `git add` 까지(MERGE_HEAD 상태로 둔다 — 커밋은 코디)
2. 코드: `day.css` 재생성 · `uv run alembic heads` 1개 · 앱 `fvm flutter analyze` · `fvm flutter test` · 백 `scripts/check.sh` 1회(전체). 실패는 합치기 때문인지 · 원래 깨진 것인지 갈라서
3. 스펙: 번호 참조 grep 으로 끊긴 것 0 확인

## 하지 말 것

- 로컬 스택(포트 11040) · 시뮬레이터 · 실행 중 프로세스 건드리기(코디가 쓰는 중) · KOS 실물 호출
- 합치기와 무관한 수정 · 새 기능 · 화면 글자 지어 넣기 · #286 메뉴 되살리기

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/merge-dev-2-report.md` — 충돌 파일별 푼 방법 · 자동 합친 겹침 8 확인 결과 · dev 변경이 우리 기능에 주는 영향(있으면 파일:줄) · 스펙 번호 대응표 · 시험 수치 · 남은 위험. 완료 보고 = dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 직접 주입:
`orca terminal send --terminal <preamble 의 코디 핸들> --text "[worker_done] backend 완료: merge-dev-2 — <한 줄>. 상세는 인박스." --enter`
막히면 같은 방식 `[질문] merge-dev-2: …`.
