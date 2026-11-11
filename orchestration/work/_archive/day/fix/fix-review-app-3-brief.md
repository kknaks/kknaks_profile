# [reviewer] fix 앱 검수 3 — WP-APP-3 채팅 화면(길게 누르기 자리 · 하단 탭 숨김 · 카톡식 읽음 + 정정 1 · 2)

너는 **day `reviewer` 워커**(같은 터미널)다. 작성자가 아니다. read-only.

- **계약의 SoT**(미커밋 스펙 6판): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` 개정 ④ + 정정 1 · 2 — U-2 「하단 4메뉴 숨김」 · 「메시지별 읽음 표시」 · 「멤버 읽은 자리 합치기」 · 「보고 있는 방에서는 내 숫자를 바로 뺀다」 · U-4 「자리가 맞아야 한다」 · §3 `Member` · `chat_member_read` · C-A16 · C-A22 ~ C-A25 · OQ-C16 ~ C18 / `spec-003-mobile-app.md` 개정 ⑩
- 정정 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/correction-read-1.md` · `correction-read-2.md` · 작업 계획 `…/work/fix/wp-plan.md` 「WP-APP-3」 · §3 읽음 계약 표
- 사용자가 본 것: `…/work/fix/e2e-feedback.md` 8 · 9 · 10 · 그림 `e2e-shots/08-app-chat-longpress-floating.png`
- 작성자 브리프 · 리포트: `…/work/fix/fix-app-code-2-brief.md` · `app-3-report.md` · 캡처 `…/work/fix/app-captures/*fix3*`(8장)
- 서버 실제 구현(계약 대조 · 네가 PASS 준 것): `backend/day/queries/chat.py` `room_views` · `services/chat.py` 읽음 · `services/chat_events.py`

대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 `app/` — 네 앞 앱 검수(수정 1 재확인) 뒤에 바뀐 것.

## 볼 것

1. **8번이 풀렸나.** 작성자가 적은 원인(route 가 포커스를 가져가 키보드가 닫히고 `reverse` 목록이 다시 잡힘)이 코드로 맞는지 · `_FollowBubble` 이 다시 재는 조건(키보드 · 회전 · 새 메시지가 와서 목록이 밀릴 때 · 말풍선이 화면 밖으로 나갔을 때 · 그 메시지가 지워졌을 때)과 멈추는 조건 · post-frame 콜백이 dispose 뒤에 도는 길 · 메뉴가 안전 영역 안에 남는지. 시험이 실제로 실패할 수 있는지(작성자의 「끄면 6건 실패」).
2. **9번.** 폰에서 탭이 숨는 화면 · 보이는 화면을 표로(목록 · 대화 · 방 정보 · 모아보기 · 새 대화 · 초대 · 크게 보기 · 채팅 거절 안내 · 다른 메뉴 · 아이패드). 깊이 관찰(`_PageDepth`)이 팝업 · 시트 · 뒤로 제스처 도중 · 푸시/배너로 대화에 바로 들어올 때 · 세션이 바뀔 때 어긋나지 않는지. 「보고 있는 방」 판정 · 탭 배지 · 앱 안 배너가 그대로인지. **아래 안전 영역**: 탭을 숨긴 화면의 입력줄 · 맨 아래 요소가 홈 표시줄과 안 겹치는지 · 탭이 보이는 화면에서 padding 이 두 번 들어가지 않는지 · 키보드가 열릴 때 inset 을 두 번 빼지 않는지.
3. **10번 셈.** 순수 함수 `unreadReaders` 를 스펙 규칙과 줄 단위로 대조하고, 아래를 네가 직접 손으로 따져 코드 결과와 맞는지: 그룹에서 한 명씩 읽음 · 보낸 사람 · 내 메시지 · 초대된 새 멤버(앞 · 뒤 메시지) · 나간 멤버 · 비활성 · 지운 메시지 · 시스템 줄 · 1:1 · **그룹을 만든 직후 첫 메시지**(서버는 시스템 줄로 누구의 읽은 자리도 올리지 않는다 — 만든 사람도 0) · 방을 숨겼다 다시 봄.
4. **정정 1.** `_senderRead` 가 메시지를 받는 **모든** 길에 걸렸는지 네가 직접 grep 으로 세어(실시간 · 보낸 응답 · 전달 · 처음 읽기 · 위로 더 · since 메우기 · 목록 다시 읽기) · `_keepReads` 의 max 합치기와 예외(다시 들어온 멤버 · `fromSeq` 바뀜)가 숫자를 되살리거나 영원히 남기는 경우가 없는지 · 가변 `Member.lastReadSeq` 가 다른 화면(방 정보 · 목록)과 객체를 공유해 생기는 부작용.
5. **정정 2.** 「보고 있는 방이면 그린 메시지까지 나 = 읽음」이 기존 `watching` 판정을 그대로 쓰는지 · 보고 있지 않을 때(앱이 뒤 · 다른 메뉴 · 목록 · 방 정보를 위에 띄움) 뜨는지 · 읽음 요청이 실패했을 때 화면과 서버가 계속 어긋나는지.
6. **서버 계약.** 앱이 읽는 필드(`members[].lastReadSeq` · `fromSeq` · `chat_member_read {roomId, accountId, lastReadSeq}`)가 서버 실제 코드와 필드 · 타입 단위로 같은지 · 없는 칸(옛 서버)일 때 기본값.
7. **표시.** 숫자 자리 · 색(`Ms.primary`) · 0 이면 없음 · 보내는 중 · 실패한 메시지 · 사진 · 동영상 · 「수정됨」 · 길게 누르기 복사본. 캡처 8장을 열어 스펙 와이어와 대조. **새 화면 글자 0**(`git diff` 의 한글 리터럴 전부).
8. 성능 — 메시지마다 멤버를 훑는 셈이 build 마다 도는지 · 읽음 이벤트 하나에 목록 전체를 다시 그리는지(그룹 20명 · 메시지 수백).
9. 시험이 조용히 통과하는 자리 · 수용 항목 C-A16 · C-A22 ~ C-A25 마다 시험 · 범위(`app/lib` · `app/test` · 통역 폴더 · 의존성 무변경).

## 돌려 볼 것(각 1회)

```
cd app && fvm flutter analyze
cd app && fvm flutter test
```

## 하지 말 것

파일 수정 · 서명 · 업로드 · 서버 호출 · 시뮬레이터 · 실기기 · 사용자 로컬 스택 · `git stash` · `checkout` 금지.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-3-report.md` — 판정 **FAIL / WARN / PASS** · 지적마다 `파일:줄` + 근거(스펙 줄 · 서버 코드 줄) + 고칠 방향 · 「탭 보임/숨김 표」 · 「읽음 셈 손 계산 표」 · 「`_senderRead` 걸린 길 표」 · 조용히 통과하는 자리 · 수치.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_4afcc88b-79e9-4f89-82de-783b5f10c7c9 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: <판정 · 한 줄>" \
  --body "판정 / FAIL·WARN 목록(파일:줄) / 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] reviewer 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```
