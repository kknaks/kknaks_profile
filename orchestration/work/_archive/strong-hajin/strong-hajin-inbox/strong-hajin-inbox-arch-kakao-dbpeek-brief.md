# [architect] 카톡 Mac DB — 첨부 메시지 필드 확인 (읽기 전용 · 사용자 승인)

너는 strong-hajin `architect` 워커다. 앞 판 `kakao-survey.md` · `kakao-attach-survey.md`(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/`)를 네가 썼다. 미결 AT-1 을 닫는다.

## 1. 승인 범위 (사용자 2026-10-06 「읽기 전용으로 확인」)
- 이 Mac 사용자 **본인의** 카톡 로컬 DB 를 **읽기 전용**으로 열어 확인한다. 키는 kakaocli 방식(기기값 유도). kakaocli 를 scratchpad 에서 빌드해 `query` 로 써도 되고 같은 방식으로 직접 열어도 된다
- **DB 파일은 복사본으로** 연다(원본 WAL 을 건드리지 않게 scratchpad 로 복사 후 그 사본만). 쓰기·스키마 변경 금지. 카톡 앱 조작·발송 금지
- 보는 것: 메시지 테이블 스키마 · 첨부 메시지(type 별: 사진·파일·동영상·이모티콘 각 1건 이내)의 **`attachment`/extra JSON 키 구조**와 URL·썸네일·만료 관련 필드 · 방 테이블에서 1:1/단체방 구분 필드 · 방 이름/참여자 필드
- **개인정보 가리기**: 리포트에 대화 본문·실명·전화번호·실제 URL 을 쓰지 마라. 키 이름 · 값의 모양(예: `https://<host>/<path>?<token>`, 길이, 만료 파라미터 이름) · 호스트 도메인만. 확인한 사본은 끝나면 지운다

## 2. 확인할 것
1. 첨부 메시지의 type 값 목록과 각각의 JSON 키
2. 다운로드 URL 이 어디 있나 · 썸네일 URL 이 따로 있나 · 만료가 URL 파라미터에 보이나(예: expires) · 인증 헤더 없이 받는 URL 모양인가(**실제로 받아 보지는 마라**)
3. 파일 이름·크기·MIME 이 JSON 에 있나
4. 1:1 / 단체방 / 오픈채팅 구분 필드 · 방 이름 없는 1:1 은 무엇으로 표시하나
5. 메시지 고유키(logId 등) · 시각 · 보낸 사람 필드 — 서버 DB 중복 방지 키 후보

## 3. 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/kakao-db-fields.md` — 표 위주 · 결정하지 마라 · 근거(테이블.컬럼)

## 9. 완료 보고 — 문구 변경 금지
> 핸들은 dispatch preamble 의 값을 믿어라.
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_a0ef6537-e532-4b7e-84e5-7e174161f6d8 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 카톡 DB 필드" --body "결론 / 근거 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] architect 완료 — 카톡 DB 첨부 필드 확인. 상세는 kakao-db-fields.md" --enter
```
