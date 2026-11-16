# [reviewer] 직원 앱 내부 채팅 — 코드 검수 r4 (모아보기 · 초대 · 들어온 뒤 대화만)

역할 · allowed_paths(read-only · 리포트 1개) · 하지 말 것 · 완료 보고(§9 두 명령)는 **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-review-brief.md` 그대로**다. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-code-r4.md` (subject 「reviewer 코드 r4 완료: …」).

## 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` 브랜치 `kknaksss/internal-chat-invite` 의 **3ed1089 이후 미커밋 변경**(`git diff 3ed1089`) — backend BE5(pytest 532 · route 71) · mobile APP7(test 248). 코디 수치 확인함.

## SSOT
1. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r5-dispositions.md` (SPEC 보다 이김 — 특히 FAIL-1 푸시 · SSE 받는 사람 경계)
2. SPEC-007 0.5.0 `(r5)` §4.6 V1 ~ V12 · #20 · §4.7 · DEC-009 D-67 ~ D-69 · OQ-962 ~ 969
3. `review-doc-r5.md`

## 볼 것
- **D-69 경계가 back 의 모든 읽기 길에 있나**(V 표 + 표 밖 — grep 으로 전수) · 앱이 경계를 넘는 걸 캐시로 보여 주지 않나(메모리 · 모아보기 · 미리보기)
- `from_message_id` 정의(방 만들 때 · 추가 · 다시 초대) · 옛 DB 채우기 · 안 읽음 불변식
- #20 back ↔ app 대조 · 1:1 [초대] 흐름(새 그룹 · 1:1 그대로 · 시스템 줄 1 · 푸시 0)
- 문구 바뀜이 앱 · 서버 전부(grep 「참여자 추가」 · 「초대했어요」)
- 회귀(전달 · 공용 시트 · F10 정렬 · 1판 ~ 3판)
- 「사용자가 실물에서 만날 자리」
