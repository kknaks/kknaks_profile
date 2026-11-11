# [mobile] fix 앱 수정 3 — 코드 리뷰 W1 + R1 · R2 (길게 누르기 메뉴)

너는 **day `mobile` 워커**(WP-APP-3 작성자 · 같은 터미널)다.

- 리뷰 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-3-report.md` (판정 WARN · FAIL 0)
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` U-4 「자리가 맞아야 한다」 · C-A22

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` — `app/lib/` · `app/test/` 만. `git stash` · `checkout` 금지.

## 고칠 것

1. **W1** — 길게 누르기 메뉴가 떠 있는 동안 **새 메시지 등으로 목록이 밀려도** 복사본 · 메뉴가 그 말풍선의 실제 자리를 따라간다. 다시 재는 계기를 「화면 크기 · 키보드」뿐 아니라 **말풍선 자리를 바꿀 수 있는 것 전부**로 넓힌다 — 그 방의 메시지가 더해짐 · 지워짐 · 수정됨(높이 바뀜) · 읽음 숫자가 생기거나 사라짐 · 위로 더 불러옴 · 스크롤. 어떤 계기들이 있는지 **코드에서 세어** 보고에 표로(리뷰는 새 메시지만 짚었다 — 목록 밖 계기가 더 있을 수 있다). 시험: 메뉴를 연 채 `chat_message` 가 오면 복사본 rect = 말풍선 rect(다시 재기를 끄면 실패하는지 확인).
2. **R1** — 메뉴를 띄운 그 메시지가 **지워지면**(`chat_message_deleted`) 메뉴를 닫는다. 말풍선이 화면 밖으로 밀려 잴 수 없을 때는 지금처럼 마지막 자리를 둔다(스펙에 정한 것 없음 — 바꾸지 않는다). 새 화면 글자 없음. 시험 1건.
3. **R2** — 다시 재기 체인이 겹쳐 돌지 않게(하나만).

R3 · R4 · R5 는 고치지 않는다.

## 검증

`cd app && fvm flutter analyze` · 고친 테스트 파일만 `fvm flutter test <파일들>` · 마지막에 `fvm flutter test` 전체 1회.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-fix3-report.md` — 항목별 고친 자리(`파일:줄`) · 다시 재는 계기 전수 표 · 시험 이름 · 수치.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "mobile 완료: <한 줄>" \
  --body "항목별 결과 / 계기 수 / 시험 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
