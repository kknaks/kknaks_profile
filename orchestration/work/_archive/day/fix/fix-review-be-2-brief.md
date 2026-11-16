# [reviewer] fix 서버 검수 2 — 수정 1(리뷰 W1 · R1 ~ R4 · R6) 재확인 + WP-BE-3 읽음 표시 서버

너는 **day `reviewer` 워커**(앱 · 서버 검수를 한 같은 터미널)다. 작성자가 아니다. read-only.

- 네 서버 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-be-report.md`
- 작성자 보고: `…/work/fix/be-fix1-report.md`(수정 1) · `be-3-report.md`(WP-BE-3) · 브리프 `fix-be-fix1-brief.md` · `fix-be-code-2-brief.md`
- **계약의 SoT**(미커밋 스펙 · 5 · 6판까지 반영 중): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` 개정 ④ + 정정 1 — §3 `Member` · 규칙 「읽음」 「읽음 표시 계약」 · 실시간 `chat_member_read` · C-A11 · C-A24 / 정정 문서 `…/work/fix/correction-read-1.md` · `correction-read-2.md` / 작업 계획 `…/work/fix/wp-plan.md` 「WP-BE-3」 · §3 읽음 계약 표
- 문서 리뷰가 찾은 것: `…/work/fix/review-doc-2-report.md`(F1 · W1 · W4 · W6)

대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 `app/` 밖 — **네 앞 검수 뒤에 바뀐 것**. mobile 워커가 같은 워크트리의 `app/` 을 고치는 중이다(대상 아님 · 읽기만).

## 볼 것

### 수정 1 재확인
1. W1 접근 로그 쿼리 필터: `uvicorn.access` · `uvicorn.error` 둘에 걸렸는지 · uvicorn 이 자기 로깅 설정을 다시 잡아 필터가 날아가는 순서가 없는지(api · worker 진입점) · 쿼리 없는 줄 · 경로가 아닌 인자를 건드리지 않는지 · 다른 로그(예외 추적 · 우리 로거의 URL)에 쿼리가 남는 자리가 더 없는지 grep.
2. R1(두 닫기 독립 · 자리 한 번) · R2(`le=50`) · R3(dtos → services import 없음) · R4(경계 시험) · R6(#22 판정 차례) 각각 풀렸는지.

### WP-BE-3
3. **읽음이 「실제로 올랐을 때만」** — 조건부 `UPDATE … RETURNING` 이 동시 요청에서 한 번만 행을 주는지(같은 seq 동시 N번 · 섞인 seq) · `least(seq, 방 last_seq)` · seq 0 · 나간 멤버 · 다른 병원 · 경계 검증이 먼저인지. `last_viewed_at` 갱신 · `chat_read` · #15 응답 · `unreadRooms` 가 앞과 같은지.
4. **`chat_member_read` 받는 사람** — 지금 멤버 중 읽은 사람 아닌 계정 · 커밋 **뒤** 발행 · 채널(방 병원) · 읽은 본인의 다른 기기에는 무엇이 가는지(스펙과 대조). 작성자 물음 2(비활성 직원 멤버도 받는 사람에 포함)를 판정한다 — 스펙 글자 · 정보 경계 · 스트림이 비활성 연결을 끊는다는 주장.
5. **`Room.members[]` 의 두 칸** — `Room` 을 만드는 자리가 정말 `room_views` 한 곳인지 네가 직접 grep · #3 1:1 열기 응답 · 시험에 #3 이 있는지(문서 리뷰 W4) · 쿼리 수가 늘지 않았는지 · 다른 멤버의 `fromSeq` 를 내보내도 경계 규칙과 안 부딪히는지.
6. **정정 1 전제** — 보내기 · 전달이 `chat_member_read` 를 내지 않고 보낸 사람 `last_read_seq` 를 올리는 것이 시험으로 굳었는지. `chat_room` 이벤트의 `Room` 이 커밋 전에 만들어져 옛 `lastReadSeq` 를 실을 수 있다는 문서 리뷰 W1 이 서버에서 사실인지(앱이 max 로 합치니 서버는 그대로 — 사실 확인만).
7. 작성자 「스펙과 다른 곳」 1(시스템 줄은 누구의 읽은 자리도 올리지 않음 — 그룹을 만든 사람도 0): 앱 셈(정정 1 · 2)과 맞물려 **숫자가 영원히 남는 경우**가 없는지 따진다(예: 방을 만든 직후 첫 메시지 · 초대된 멤버의 `fromSeq`).
8. migration 없음 · 범위(`app/` · 통역 코드 · 배포 설정 무변경) · 조용히 통과하는 자리(infra 시험이 skip 되는 것 포함).

## 돌려 볼 것(각 1회)

```
cd backend && uv run pytest -q -m "not infra"
cd backend && uv run ruff check . ../scripts
```

infra 는 돌리지 않는다(사용자 로컬 스택 · 격리 스택 금지). 작성자 수치(격리 1147 passed)를 못 믿을 근거가 코드에 보이면 지적한다.

## 하지 말 것

파일 수정 · Soniox · KOS · 서버 호출 · 배포 · `git stash` · `checkout` 금지. 키 · 토큰 값을 리포트에 옮기지 않는다.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-be-2-report.md` — 판정 **FAIL / WARN / PASS** · 지적마다 `파일:줄` + 근거 + 고칠 방향 · 작성자 물음 판정 · 조용히 통과하는 자리 · 수치.

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
