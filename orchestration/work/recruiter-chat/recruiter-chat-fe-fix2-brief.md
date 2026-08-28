
# [frontend] fix2 — /chat 스크롤: 스레드만 스크롤, 사이드바·네비·컴포저 고정

너는 WORK-024 의 **kknaks-dev `frontend` 워커**다. owner 실사용 피드백이다. 이것만 고친다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`
spec **v0.0.7** U-5 「스크롤 계약」이 신설됐다:
`/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md`

## 증상 (owner 스크린샷 2건)

- `/chat` 에서 문서(body) 전체가 스크롤된다 — 위로 올리면 **네비도 사이드바도 화면에서 사라진다.**
- 답변이 자라거나 도착하면 `chat-view.tsx:240` 의 `scrollIntoView` 가 **사용자 위치와 무관하게** 문서를 끌어내린다 — 위를 읽는 중에 밀린다.

## 수정 (spec U-5 스크롤 계약)

1. `/chat` 을 앱 레이아웃으로: 페이지(body) 스크롤 **없음** — 전체가 뷰포트 높이(네비 제외)에 고정. 네비·사이드바·컴포저는 항상 제자리, **스레드 영역만 `overflow-y: auto`**. (사이드바 대화 목록이 길면 사이드바 내부만 따로 스크롤 — 기존 시안 CSS 의 `.convlist` 패턴)
2. 자동 하단 스크롤을 **스레드 컨테이너 스코프 + bottom-stick** 으로: 사용자가 스레드 하단 근처(예: 80px 이내)에 있을 때만 새 내용·답변 도착 시 하단으로 따라간다. 위로 올려 읽는 중이면 밀지 않는다. `scrollIntoView`(문서 스크롤) 대신 컨테이너 `scrollTop` 제어.
3. 새 질문을 **직접 보낼 때**는 위치와 무관하게 하단으로 이동(자기 행동의 결과는 보여야 한다).
4. 홈(`/`)의 스크롤 동작은 그대로다 — 이 계약은 `/chat` 한정.

## 검증

```
cd app/front && npx tsc --noEmit (만진 파일 0 에러). 검증은 1회만
```
+ dev(:3000)에서 수동 확인 3가지를 보고에 적어라: ① 스크롤해도 사이드바·네비 고정 ② 위를 읽는 중 답변 도착해도 안 밀림 ③ 하단에 있을 때는 따라감.

## 완료 보고 — 2채널, 핸들은 preamble 우선

```bash
orca orchestration send --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> \
  --subject "frontend fix2 완료: <한 줄>" --body "수정 요약 / tsc / 수동 확인 3종"
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] frontend fix2 완료 — <한 줄>. 상세는 인박스." --enter
```
