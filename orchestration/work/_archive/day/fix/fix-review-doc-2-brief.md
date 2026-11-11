# [reviewer_doc] fix 스펙 4판 검수 — 피드백 8 · 9 · 10 (길게 누르기 · 하단 탭 숨김 · 읽음 표시)

너는 **day `reviewer_doc` 워커**(1 · 2판을 검수한 같은 터미널)다. 작성자가 아니다. read-only.

- 사용자 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/e2e-feedback.md` 「버그 기록」 **8 · 9 · 10** · 그림 `e2e-shots/08-app-chat-longpress-floating.png` · 결정 `…/work/fix/_RESUME.md` §2
- 작성자 브리프 · 리포트: `…/work/fix/fix-spec-4-brief.md` · `spec-4-report.md` · 작업 계획 `…/work/fix/wp-plan.md`(WP-BE-3 · WP-APP-3 · §3 읽음 계약 표)
- 코드(읽기 · 「지금 구현」 대조): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`

검수 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` 미커밋 변경 중 **4판분**(SPEC-004 개정 ④ · SPEC-003 개정 ⑩ · SPEC-000 2026-11-11 개정 ② · `log.md`) + `wp-plan.md` 추가분. 1 ~ 3판은 네가 이미 봤다 — 4판이 그것을 깨뜨렸는지만 본다.

**backend · mobile 워커가 이 스펙으로 지금 코드를 짓고 있다.** 계약을 바꿔야 하는 지적(FAIL · 계약에 닿는 WARN)이 나오면 리포트를 다 쓰기 전에 먼저 한 줄로 알려라:
`orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[긴급] reviewer_doc: <문서:줄 · 무엇이 틀렸나>" --enter`

## 볼 것

1. **사용자 확정과 같은가.** 8(버그 — 결과만 · 원인 추측 없음) · 9(폰 대화 화면에서 하단 탭 숨김 · 아이패드 그대로) · 10(카톡식 — 안 읽은 사람 수 · 줄다가 0 이면 사라짐). 코디 · planner 기본값(OQ-C16 ~ C18)이 사용자 확정과 구별돼 있는지.
2. **읽음 계약이 맞게 세어지는가.** 「앱이 센다 · 서버는 멤버의 `lastReadSeq` · `fromSeq` 를 준다」 — 스펙의 셈 규칙으로 아래를 손으로 따져 숫자가 카톡식 기대와 같은지: 그룹 4명에서 한 명씩 읽을 때 · 보낸 사람 자신 · 초대된 새 멤버(앞 메시지) · 나간 멤버 · 비활성 직원 · 내가 방을 숨겼다 다시 봄 · 지운 메시지 · 시스템 줄 · 1:1. 보낸 사람의 `lastReadSeq` 가 자기 메시지 seq 보다 작을 수 있는지(보내기가 읽은 자리를 올리는지 — 서버 코드 `services/chat.py` 확인)와 그때 숫자.
3. **실시간.** `chat_member_read` 를 누가 받나 · 읽은 본인의 다른 기기 · 순서가 뒤바뀌어 온 이벤트(작은 seq 가 나중에) · 끊겼다 다시 붙을 때 메우기 · `chat_room` 이벤트의 `members[]` 와의 충돌(옛 값으로 덮기) · 읽음 폭주. 서버 SSE 구조(`services/chat_events.py` · `routers/api/chat.py` stream)가 스펙이 말한 「받는 사람」을 실제로 지원하는지.
4. **`Member` 칸을 더한 것의 파급.** `Room` 이 나오는 모든 응답 · 이벤트에 일관되게 적혔는지 · 다른 멤버의 `fromSeq` · `lastReadSeq` 를 보여 줘도 되는 정보인지(스펙의 경계 규칙과 부딪히지 않는지) · migration 없음 주장(`models/` 확인).
5. **9번의 파급.** 「보고 있는 방」 판정 · 푸시 탭 이동 · 앱 안 배너 · 탭 배지 · 키보드 열림 때 지금 동작 · SPEC-003 U-2 와의 모순 · 채팅 403 안내 화면(탭이 보여야 다른 메뉴로 갈 수 있다) · 통역 드로어 등 다른 화면과 섞일 때.
6. **옛 문장.** 「하단 4메뉴는 그대로」 · 「탭바 유지」 · 「이벤트 6종」 같은 수 · 「읽음 = 나만」 류가 다른 절에 남았는지 grep.
7. **새 화면 글자 0** — 숫자만. 색 · 자리 토큰이 앱에 실제로 있는 이름인지.
8. **수용 항목 C-A22 ~ C-A25** 가 통과 · 실패를 가르는지 · 조용히 통과하는 자리.
9. `wp-plan.md` WP-BE-3 · WP-APP-3 의 파일 목록이 코드에서 실제로 그 일을 하는 자리와 맞는지(빠진 자리).
10. Delivery #241 v2 에서 Non-Goals 「새 이벤트 종류」를 「`chat_member_read` 하나만 예외」로 좁힌 것이 8 · 9 · 10 범위 안인지.

## 돌려 볼 것

```
python3 scripts/lint-pipeline.py --strict     # products/day/ ERROR 0
```

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-doc-2-report.md` — 판정 **FAIL / WARN / PASS** · 지적마다 `문서:줄` + 근거 + 고칠 방향 한 줄 · 「읽음 셈 손 계산 표」 · 조용히 통과하는 자리 · lint.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_fe17c0ae-13ad-4046-abb8-f9e9280f8932 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer_doc 완료: <판정 · 한 줄>" \
  --body "판정 / FAIL·WARN 목록(문서:줄) / lint"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] reviewer_doc 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```
