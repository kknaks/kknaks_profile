# [frontend] 디자인 수정 — 확인 창(F1) · 원장 변경 버튼(F5)

같은 워크트리 · 같은 규칙(`fe-236-brief.md` — medikit · DS 토큰 · 손 CSS 0 · 인라인 스크립트 0 · 화면 글자 새로 짓지 않음 · backend 파일 · 커밋 금지).
피드백 원문 · 코디 관찰: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/e2e-feedback.md` F1 · F5. **이번엔 이 둘만**(호출 로직 · 카드 순서 등 나머지 피드백은 손대지 마라).

## F1 시작 취소 · 완료 취소 확인 창 — 사용자 「모달 디자인 이상함」
지금: 창이 판 폭에 가깝게 넓고 · 제목 아래 구분선 뒤 본문 없이 버튼 줄이 붙어 빈 칸처럼 보이고 · [닫기] 회색 글자 + 회색 테두리라 꺼진 버튼처럼 · [완료 취소] 옅은 빨강 테두리 글자라 주 버튼이 약함.
바꿀 것:
- 레포 medikit 의 **표준 확인 창(작은 모달)** 모양을 따른다 — 키트 견본(`/dev/kit` · `templates/kit.html` · `partials/kit_modal.html` · centurion medikit-htmx-kit 가이드)에 있는 확인/위험 동작 모달 패턴을 찾아 그대로 쓴다. 없으면 가장 가까운 것
- 폭은 작게(확인 창 크기) · 제목 「{시술} 시작을 취소할까요?」/「{시술} 완료를 취소할까요?」 그대로(본문 글자 새로 짓지 않음 — 빈 본문 칸 · 어색한 구분선 없애기)
- 버튼: [닫기] = 보조(일반 글자색 · 꺼진 것처럼 보이지 않게) · [시작 취소]/[완료 취소] = **주 버튼 · 위험 색 채움**(DS 의 danger/destructive 변형) · 버튼 배치는 키트 관례(오른쪽 정렬 등)
- 포커스 · Esc · 바깥 클릭 동작은 그대로

## F5 원장 이름 버튼(원장 변경) — 사용자 「이거 지금 디자인 왜 이래?」
지금: 수락 · 진행 중 줄의 원장 이름이 밑줄 링크(hover:underline) 모양 버튼이라 줄 글자와 따로 놀아 보임.
바꿀 것:
- 평소엔 줄의 다른 메타 글자와 **같은 모양**(링크 · 밑줄 없음)
- 누를 수 있다는 표시는 **호버 때만**: DS 의 ghost/텍스트 버튼처럼 옅은 배경 + 툴팁 「원장 변경」(이미 있음) · 커서 pointer. 필요하면 DS 아이콘(편집/바꾸기 계열)을 호버 때 작게 — 키트에 있는 아이콘만
- aria-label 「{원장} 원장 변경」 그대로

## 검증
화면 테스트(바뀐 클래스 · 버튼 변형 단언) · `scripts/build-css.sh` 1회 · `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q` 1회 · 손 CSS · 인라인 스크립트 grep 0. 가능하면 `/dev/kit/board` 견본에 두 모양이 보이게.

## 완료 보고
코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd` — `orca orchestration send … --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "frontend 디자인 F1·F5"` + `orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] frontend 디자인 F1·F5 — <한 줄>" --enter`. 쓴 키트 패턴 이름 · 바뀐 파일 · 테스트 수.
