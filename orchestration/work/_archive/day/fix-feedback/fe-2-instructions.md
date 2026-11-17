# [frontend] fe-2 — 2루프: ⋮ 되돌리기 · 간호관리 · 차트 여는 곳 · 알림 늘 · 팝오버 버그 · W2

너는 앞 맥락이 없다. 먼저 읽어라:
1. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-fe-brief.md` — 역할 · allowed_paths · 범위 제약(화면 글자 발명 금지 · 인라인 스크립트 0 · 손 CSS 0) · 검증 · 완료 보고가 그대로 적용(작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` — 1루프 미커밋 위에 이어서).
2. 1루프 결과 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fe-1-report.md` · 코드 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-code-1-report.md`(W2 · W7 · W9).
3. 스펙(미커밋 · 절대경로): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec/products/day/20-spec/spec-002-procedure-board.md` **개정 ㉒**(U-3 :225-229 · U-12 :346 · U-14 :371 · API :578 · 응답 :595 · 스냅샷 :660 · 매트릭스 :740) · `spec-005-notifications.md` 2차 개정(U-5 :157 · S-6 :197 · OQ-N9 :428) · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/e2e-feedback.md`(E2 · E3 · E5 · E6 · F-5) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/_RESUME.md` §2.

⚠ **backend 워커가 같은 워크트리에서 동시에 작업한다** — 서로의 파일을 건드리지 마라.

## 고정 — 사용자 결정

- 호출 취소 **알림 없음**(웹 OS 알림도 `doctor_call` 그대로 — 새 종류 없음).
- 허용 새 글자: 「호출 취소」 · 「간호관리」 · 「차트 작성」(+ 기존 글자).

## be 계약(이대로 부른다)

- `board.cancel_call(session, current, task_id, now=None) -> ActionResult` → 웹 `POST /board/tasks/{task_id}/cancel-call` · 응답 = 다른 줄 조작과 같은 `_after`(카드 조각 + 함께 맞출 조각 · 판 전체 다시 받지 않음 — :595).
- 스냅샷 줄 `systemDoctor: bool`.

## 할 일

1. **F-5 ⋮** — 준비중 줄 ⋮ 없음 · 호출(수락 전) 줄 ⋮ → 「호출 취소」 · 진행중 ⋮ → 시작 취소(그대로) · 완료 ⋮ → 완료 취소(그대로) · 수락 줄 ⋮ 없음. 확인 창 · 성공 토스트 없음 · 거절은 기존 토스트 처리.
2. **E3** — `systemDoctor` 줄의 원장 칸 = 「간호관리」(「간호관리 · 진행 mm:ss」 · 완료 「간호관리 · n분」) · 그 글자에 원장 줄과 **똑같이** 호버 툴팁 「원장 변경」 + 눌러 원장 바꾸기(`board_parts.html` `doctor_pop` 이 `t.doctor` 없으면 안 여는 곳 고침).
3. **E6** — 차트 창은 **시술 이름 글자만** 연다(1루프 줄 전체 `data-day-row-get` 제거 · 판 카드 줄 · 「시술 완료」 탭 줄 모두) · 이름 호버 툴팁 「차트 작성」 · 체크박스 · 버튼 · ⋮ · 시간 칸을 눌러도 안 열림.
4. **E5** — 웹 OS 알림 **늘 띄움**: `day.js` `show` 의 `document.hidden` 조건 제거(권한 granted 만).
5. **W2** — `startNotify`: ① 첫 `prime` 실패 시 다음 신호에서 오늘 것 전부 쏟아내지 않게(그때 받은 목록은 「본 것」으로만 채움) ② `unread` 합 비교(`grew`)로 거르지 말고 신호마다 목록을 받아 `seen` 으로만 거름.
6. **E2 버그** — 의사 호출 팝오버(원장 고르기)에서 기본 선택 원장이 목록 아래쪽이면 팝오버 **위쪽(제목 · 검색 · 추천 · 선택됨)이 잘리고 아래가 빔**(사용자 스크린샷 · `e2e-feedback.md` E2). 원인을 찾아 고쳐라(가설: 선택 줄로 `scrollIntoView` 하며 팝오버 바깥까지 스크롤) — 늘 위부터 다 보이고 목록 안에서만 스크롤. 1루프 전부터 있던 버그인지(dev `4f8316a7` 대조) 리포트에.
7. 화면 테스트 갱신 · 추가(위 각각).

## 검증

- 원 브리프 §8 그대로(pytest 화면 테스트 1회 · CSS 빌드 · node --check · 인라인 스크립트 · style= 0 grep).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fe-2-report.md` — 변경 파일 · E2 원인 · 테스트 수치 · E2E 에서 만날 자리. 완료 보고는 preamble 의 worker_done.
