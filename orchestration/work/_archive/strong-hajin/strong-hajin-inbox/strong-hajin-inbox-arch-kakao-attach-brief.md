# [architect] 카톡 Mac — 첨부(사진·파일) 조회 구조 조사 (read-only)

너는 strong-hajin `architect` 워커다. 앞 판 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/kakao-survey.md` 를 네가 썼다(맥락이 없으면 그것과 `_RESUME.md` §2 를 읽어라).

## 1. 결정 (사용자 2026-10-06)
이번 카톡 범위 = **조회만**(발송 없음) · **사용자가 고른 대화방만** · **첨부도 조회 가능한 구조**여야 한다.
조회 = Rust 앱이 로컬 DB 를 읽어 서버로 올리고 메시지함이 그린다. 첨부 파일 자체는 서버에 저장하지 않는 원칙(메일·슬랙 = 클릭하면 그때 받아 중계)이다.

## 2. 조사할 것 — Mac 카톡에서 첨부를 어떻게 「볼 수 있게」 하나
1. Mac 카톡 DB 의 메시지 행에서 **첨부(사진·동영상·파일·이모티콘) 메시지를 어떻게 구분**하나(type/attachment 컬럼 등) — kakaocli 소스 · 공개 연구 근거
2. 첨부의 **실체는 어디 있나**: ① 로컬 캐시 파일(컨테이너 안 경로 — `ls` 로 디렉터리 구조만 확인, 파일 열기 금지) ② 카카오 CDN URL(talkmedia 등 — 메시지 메타에 있나, 만료되나, 인증이 필요한가) ③ 둘 다
3. mykakao Windows 판의 사진 수집(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/mykakao/00-baseline/baseline-007-photo-collection.md` · `baseline-008` · `decision-006` · `spec-006`)이 쓴 방식 중 Mac 에 그대로 통하는 것 / 안 통하는 것
4. 그래서 **클릭하면 보이는 길**이 무엇인가: (가) 서버가 CDN URL 로 직접 받아 중계 (나) 서버 → Rust 앱에 요청 → 로컬 파일을 올려 중계 (다) 그 밖 — 각각 조건(카톡 켜짐? 앱 켜짐? 만료?)과 실패 모습
5. 썸네일(사진 미리보기)을 메시지함 목록에 바로 보이게 할 수 있나

## 3. 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/kakao-attach-survey.md` 하나 — §1 결론(가능? 어떤 길?) · §2 근거 · §3 길별 비교 표 · §4 열린 질문. 결정하지 마라.

## 4. 하지 말 것
DB 복호화·열기 · 캐시 파일 열기 · 카톡 조작 · 네트워크로 CDN 받아 보기 금지(ls 로 구조만). 다른 파일 쓰기·커밋 금지.

## 9. 완료 보고 — 문구 변경 금지
> 핸들은 dispatch preamble 의 값을 믿어라.
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_a0ef6537-e532-4b7e-84e5-7e174161f6d8 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 카톡 첨부 조사" --body "결론 / 근거 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] architect 완료 — 카톡 첨부 조회 구조 조사. 상세는 kakao-attach-survey.md" --enter
```
