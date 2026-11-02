# [frontend] WORK-008 Phase 1 — 화면 확인에서 나온 것 (fix2)

너는 Phase 1 을 구현한 **strong-hajin `frontend` 워커**다. 같은 워크트리에서 이어서 고친다. 규칙은 `strong-hajin-polish-fe-p1-brief.md` 와 같다.

## 무엇이 보였나 (코디 화면 확인 — 데모 DB, 1920px)

내 업무 › 타임라인을 열면 **업무명 열이 화면에서 사라진다.** 첫 진입 때 오늘이 보이게 가로 스크롤(`(idx-2)*34`)하는데, 업무명 열(`.timeline-label-col` · `.timeline-title`)이 스크롤과 함께 왼쪽으로 밀려 나간다 — 막대만 남고 어느 업무인지 알 수 없다. 머리줄의 「기간」·「업무명」 칸도 같이 사라진다.
원인: `.work-timeline .timeline-scroll{overflow-x:auto}` 안에서 업무명 열이 고정되어 있지 않다(`screens-a.css:475·483`).

## 고칠 것 (이것만)

- 타임라인의 **업무명 열(머리줄의 기간/업무명 칸 포함)을 가로 스크롤에서 왼쪽에 고정**한다. 프로젝트 간트가 이미 하는 「라벨 칸 틀고정」(SPEC-005 D-36, `scax-pj-gantt__name-cell`)과 같은 방식·같은 DS 토큰으로. 고정 칸이 막대 위로 겹칠 때 배경이 비치지 않게
- 오늘 스크롤 계산이 고정 칸 폭을 고려하는지 확인한다 — 오늘 칸이 고정 칸 뒤에 숨지 않아야 한다
- 테스트 1개: 고정 칸 클래스/스타일이 서고, 첫 진입 스크롤 위치가 고정 칸 폭을 뺀 자리
- WP 1-5 의 「업무명 열은 지금 DS 그대로」는 **모양**을 말한다 — 고정은 보이게 하기 위한 것이라 계약 안이다

## 하지 말 것
- 위 밖 금지. 커밋·push 금지. 서버·브라우저 띄우지 마라(코디의 로컬 스택 8001·5176 이 떠 있다 — 건드리지 마라. vite 가 파일 변경을 바로 반영한다)
- 테스트는 직렬·바뀐 파일만. `npx tsc --noEmit` 1회

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 1 fix2" \
  --body "고친 파일:줄 / 테스트 / tsc"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — Phase 1 fix2. 상세는 인박스." --enter
```
