# [architect] 설정 시안 — 「계정 설정」 → 「프로필 설정」 (쓰기 작업)

너는 strong-hajin `architect` 워커다. 맥락: `design-change-2.md`(설정 판) · `_RESUME.md` §2 — `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/`. **답장 시안 작업이 끝난 뒤** 시작한다.

## 1. 결정 (사용자 2026-10-06)
설정의 `계정 설정` 메뉴를 **`프로필 설정`** 으로 바꾸고 구획 셋:
1. **프로필 이미지** — 바꾸기·삭제. 원형 미리보기 · 「이미지 변경」은 기존 DS `DropZone`(끌어다 놓기 + 고르기)로 받아도 된다 · 한도 문구 「정사각형 1MB 이하 PNG · JPG」(시안 문구 유지) · 이미지가 없으면 이니셜 아바타
2. **AX 캐릭터 설정** — 지금 앱에 있는 AX 캐릭터 고르기를 이 자리로 옮긴다. 코드 원본(읽기만): `/Users/kknaks/git/toy_pr2/Strong_hajin/frontend/src/features/assistant/AssistantCharacterPicker.tsx` · `AssistantCharacter.tsx` — 고르는 후보·모양을 그대로 따라 그려라(발명 금지)
3. **비밀번호 변경** — 시안 그대로(현재·새·확인 · 규칙 문구 · 「변경하면 다른 기기의 로그인이 모두 해제된다」)

**이름·직무 입력칸은 없앤다** — 조직 명부에서 오는 값이다(코드 `backend/src/ax_workspace/modules/organization_access/` 직책·직무 = 명부 기준). 프로필 구획 머리에 **읽기 전용**으로 이름 · 소속 · 직책/직무를 보여 주고 「조직 명부에서 관리됩니다」 한 줄. 「프로필 저장」 단추는 이미지 변경 즉시 저장이면 없애도 된다 — 네가 시안에서 하나로 정하고 design-change 에 적어라.

대상: `handoff/settings/js/settings.v1.jsx` · `data.js` · `settings.css`. 메일·슬랙·카톡·알림 메뉴는 건드리지 마라. 메뉴 묶음 이름 「계정」은 그대로 둬도 된다.

## 2. 상태 · 목데이터
이미지 없음/있음 · 업로드 중 · 용량 초과 오류 · 비밀번호 불일치·현재 비밀번호 틀림 · 캐릭터 저장 실패. 가상 인물만.

## 3. 끝나면
로컬 사본 갱신(같은 경로·같은 바이트) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-4.md` · 커밋 금지

## 9. 완료 보고 — 문구 변경 금지
> 핸들은 dispatch preamble 의 값을 믿어라.
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_208c9243-9983-47ba-9983-e3aa67ecf049 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 프로필 설정 시안" --body "바꾼 파일 / 요약 / 로컬 사본 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] architect 완료 — 프로필 설정 시안. 상세는 design-change-4.md" --enter
```
