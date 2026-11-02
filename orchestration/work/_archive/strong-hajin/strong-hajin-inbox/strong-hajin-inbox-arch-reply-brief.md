# [architect] 메시지함 시안 — 답장 넣기 (메일·슬랙 · 첨부 포함) (쓰기 작업)

너는 strong-hajin `architect` 워커다. 맥락: `design-change-1.md`(메시지함 판) · `design-change-2.md`(설정 판) · `_RESUME.md` §2 — 전부 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/`.
**설정 시안 작업이 끝난 뒤** 시작한다.

## 1. 결정 (사용자 2026-10-06)
1단계에 **답장**이 들어온다 — 메일 답장 · 슬랙 메시지/스레드 답글 · **첨부 파일 보내기(끌어다 놓기 + 첨부 창 열기)**. 앞 판에서 「조회 전용이라 입력창·답장 없음」으로 걷은 것을 이 범위만큼 되돌린다. 나머지(업무로 옮기기 · 확인완료 · 업무/참고 배지 · 리액션 추가 · hover 행동 막대)는 여전히 없다.

대상 파일: `handoff/inbox/js/inbox.v1.jsx` · `handoff/inbox/js/data.js` · `handoff/inbox/css/inbox.css`. DS·다른 화면 금지.

## 2. 첨부는 기존 DS 부품을 쓴다 — 새로 만들지 마라
- `DropZone`(`.scax-dropzone` / `--over`, 머리 한 줄 = 안내 + 오른쪽 고르기 단추, 고른 목록은 칸 안에 `children`) · `FileList`(종류 글리프 · 이름 · 크기 · 못 붙은 이유 · 빼기). Claude Design 프로젝트 `components/ds/` 와 `_ds_bundle` 에 있다. 코드 원본(읽기만): `/Users/kknaks/git/toy_pr2/Strong_hajin/frontend/src/ds/DropZone.tsx` · `FileList.tsx`, 쓰는 예 `frontend/src/features/meetings/AttachModal.tsx` · `frontend/src/features/work/WorkModals.tsx`
- 입력창 위로 파일을 끌어오면 **창 전체가 DropZone `--over` 모양**이 되는 것도 그린다

## 3. 슬랙
- 본문 맨 아래 **입력창**(진짜 슬랙처럼): 「#채널명에 메시지 보내기」 placeholder · 서식 막대는 최소(굵게·기울임·링크·목록·코드) · 왼쪽 「+」= 첨부 창 열기 · 오른쪽 보내기 · 첨부를 고르면 입력창 안에 FileList 칩
- **스레드 답글**: 「답글 N개」를 펼치면 그 아래 작은 입력창(「답글 달기…」) — 같은 첨부 방식
- 보낸 메시지는 **내 이름으로** 대화에 그대로 선다(사용자 토큰). 보내는 중 · 보내기 실패(다시 보내기) 상태

## 4. 메일
- 원문 머리 오른쪽 `답장` · `전체 답장` 두 단추 (`전달`·새 메일 쓰기는 이번에 없음)
- 누르면 **원문 아래에 답장 작성 칸**이 펼쳐진다(모달 아님): 받는 사람·참조(칩, 전체 답장이면 채워짐, 고칠 수 있음) · 제목 `Re: …` 고정 · 본문 · 원문 인용 접힘(「··· 이전 내용」) · **DropZone + FileList** · `보내기` / `취소`
- 보내는 중 · 보냈음(작성 칸 닫히고 원문 아래에 「보낸 답장」 한 덩어리) · 실패
- 한도 문구는 hint 에 「한 번에 25MB까지」(Gmail 한도 — 계약 사실)

## 5. 네 상태 · 목데이터
- 앞 판 StateSwitch 에 답장 상태(작성 중 · 보내는 중 · 실패)를 볼 수 있게
- 가상 인물·가상 파일만

## 6. 끝나면
로컬 사본 갱신(같은 경로·같은 바이트) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-3.md` · 커밋 금지

## 9. 완료 보고 — 문구 변경 금지
> 핸들은 dispatch preamble 의 값을 믿어라.
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_208c9243-9983-47ba-9983-e3aa67ecf049 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 메시지함 답장 시안" --body "바꾼 파일 / 요약 / 로컬 사본 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] architect 완료 — 메시지함 답장 시안. 상세는 design-change-3.md" --enter
```
