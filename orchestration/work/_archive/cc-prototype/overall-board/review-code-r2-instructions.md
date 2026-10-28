# reviewer r2 — 코드 재검수 (r1 이후 변경 전부)

기준: SPEC-003 **0.5.1** · WORK-006 · `_RESUME.md` §2 10-25 · 10-26 줄 (코디 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/...`).
대상: 코드 워크트리의 **커밋 9a317a2 이후 미커밋 변경 전부**(`git diff` · 새 파일 `test_undo.py` · `UndoConfirm.tsx`) + **9a317a2 안의 r1 이후 변경**(방 판정 type 무관 · 규칙 하나 · isRoomTask — r1 은 이 부분을 못 봤다: `git diff <r1 기준> ...` 대신 `rules.py` · `sync.py` · `actions.py` · front `view.ts` 를 SPEC §5.1 · §5.7 과 직접 대조).

1. 규칙 하나: type 무관 같은 시술 · 예외 「방 배정」(방 붙은 ETCETERA + 호출 이력 없음) · isRoomTask front 숨김 · 귀가 대기 취소 = 방 배정만.
2. 되돌리기: §5.13 표 전부 · 409 네 코드 · canUndo* · 토스트 5초 · 마지막 조작만 · 아이콘 위치(진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 왼쪽 · 대기 줄 없음) · ConfirmModal · KOS op(complete:false · flow-step 뒤로) · superseded/statusNot · **완료 되돌리기 = started_at 유지(경과 시간이 원래 시작부터) · 시작 되돌리기 = started_at 비움** (사용자 확인 10-26).
3. **화면 결함 확인**: `fe-shots/undo-modal-finish.png` 에서 모달 오른쪽 [되돌리기] 버튼이 모달 상자 밖으로 삐져나와 보인다 — 원인(`ConfirmModal` 사용법 · `medikit-patches.css` Button-2 `data-fill-buttons` 등)을 `파일:줄`로. FE 몫 FAIL 후보.
4. 조용히 통과하는 자리 · 사용자가 실물에서 만날 자리(코디 E2E §9 #21 ~ #26 체크리스트).

산출: `review-code-r2.md`. 종합 판정 · FAIL 은 BE/FE 몫 표시. 보고 §9 두 채널.
