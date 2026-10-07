# [architect] 메시지함 시안 — 피드백 모음 1 반영 (쓰기 작업)

너는 strong-hajin `architect` 워커다. 맥락: `design-change-1.md` · `design-change-3.md`(답장 판) · `design-feedback-batch-1.md` · `_RESUME.md` §2 — `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/`.

## 1. 고칠 것 (사용자 2026-10-06)
1. **본문 폭 전체 사용** — 메일 본문 720px · 슬랙 대화 880px 제한을 걷는다. 메일 머리 표·HTML 본문·첨부·답장 작성 칸, 슬랙 대화·입력창 모두 남은 폭을 다 쓴다
2. **슬랙 스레드 = 진짜 슬랙처럼 오른쪽 패널, 3열**
   - 평소 2열: `[목록] [내용]` → 「답글 N개」 누르면 3열: `[목록] [내용] [스레드]`
   - 스레드 패널: 머리 「스레드 · #채널명」 + 닫기(×) → 부모 메시지 → 답글들(같은 메시지 모양·묶음·서식·첨부·리액션) → **패널 아래 답글 입력창**(답장 판의 첨부·DropZone 그대로)
   - 지금의 「부모 아래 들여써서 펼침」과 그 아래 작은 입력창은 **없앤다**
   - 패널 폭은 고정(예: 400~440px), 내용 열이 줄어든다. 한 번에 스레드 하나만 열린다
   - 상태 토글에 「스레드 열림」 · 스레드 답글 보내는 중/실패 를 볼 수 있게

대상: `handoff/inbox/js/inbox.v1.jsx` · `handoff/inbox/css/inbox.css` (data.js 는 필요할 때만). DS·다른 화면 금지.

## 2. 끝나면
로컬 사본 갱신(같은 경로·같은 바이트) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-5.md` · 커밋 금지

## 9. 완료 보고 — 문구 변경 금지
> 핸들은 dispatch preamble 의 값을 믿어라.
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_208c9243-9983-47ba-9983-e3aa67ecf049 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 메시지함 폭·스레드 3열" --body "바꾼 파일 / 요약 / 로컬 사본 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] architect 완료 — 메시지함 폭 전체·스레드 3열. 상세는 design-change-5.md" --enter
```
