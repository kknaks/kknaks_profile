# [reviewer] 코드 재검수 r2 — 규칙 하나 · 방 판정 · 되돌리기

너는 **cc-prototype `reviewer` 워커**다. **앞 판의 맥락이 없다.** 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 나머지). 작업 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — **read-only**. 앞 판 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/review-code-r1.md` 먼저 읽어라.

# reviewer r2 — 코드 재검수 (r1 이후 변경 전부)

기준: SPEC-003 **0.5.1** · WORK-006 · `_RESUME.md` §2 10-25 · 10-26 줄 (코디 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/...`).
대상: 코드 워크트리의 **커밋 9a317a2 이후 미커밋 변경 전부**(`git diff` · 새 파일 `test_undo.py` · `UndoConfirm.tsx`) + **9a317a2 안의 r1 이후 변경**(방 판정 type 무관 · 규칙 하나 · isRoomTask — r1 은 이 부분을 못 봤다: `git diff <r1 기준> ...` 대신 `rules.py` · `sync.py` · `actions.py` · front `view.ts` 를 SPEC §5.1 · §5.7 과 직접 대조).

1. 규칙 하나: type 무관 같은 시술 · 예외 「방 배정」(방 붙은 ETCETERA + 호출 이력 없음) · isRoomTask front 숨김 · 귀가 대기 취소 = 방 배정만.
2. 되돌리기: §5.13 표 전부 · 409 네 코드 · canUndo* · 토스트 5초 · 마지막 조작만 · 아이콘 위치(진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 왼쪽 · 대기 줄 없음) · ConfirmModal · KOS op(complete:false · flow-step 뒤로) · superseded/statusNot · **완료 되돌리기 = started_at 유지(경과 시간이 원래 시작부터) · 시작 되돌리기 = started_at 비움** (사용자 확인 10-26).
3. **화면 결함 확인**: `fe-shots/undo-modal-finish.png` 에서 모달 오른쪽 [되돌리기] 버튼이 모달 상자 밖으로 삐져나와 보인다 — 원인(`ConfirmModal` 사용법 · `medikit-patches.css` Button-2 `data-fill-buttons` 등)을 `파일:줄`로. FE 몫 FAIL 후보.
4. 조용히 통과하는 자리 · 사용자가 실물에서 만날 자리(코디 E2E §9 #21 ~ #26 체크리스트).

산출: `review-code-r2.md`. 종합 판정 · FAIL 은 BE/FE 몫 표시. 보고 §9 두 채널.


## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_f2eaa5d5-11f7-447e-ae82-7647fdcf3458 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
