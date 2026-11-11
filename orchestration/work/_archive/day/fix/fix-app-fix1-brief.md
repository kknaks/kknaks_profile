# [mobile] fix 앱 수정 1 — 코드 리뷰 W1 + 참고 R1 ~ R5

너는 **day `mobile` 워커**(WP-APP-1 · APP-2 작성자 · 같은 터미널)다.

- 리뷰 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-report.md` (판정 WARN · FAIL 0)
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` U-1 `:155-159` · C-A19 · U-7 `:221`

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` — `app/lib/` · `app/test/` 만. backend 워커가 같은 워크트리에서 통역을 짓는 중이다(`backend/` 등 건드리지 마라 · `git stash` · `checkout` 금지).

## 고칠 것

1. **W1** — 채팅 403 이 거절 안내로 가지 않는 경로: 새 대화 직원 목록(`chat_new_screen.dart`) · 사진 · 동영상 모아보기(`chat_media_screen.dart`) · 사진 바이트 읽기(`chat_state.dart`). 리뷰의 고칠 방향대로 403 이면 채팅 공통 거절 처리로 넘긴다. **이 셋만 고치지 말고 `app/lib/chat/` 에서 채팅 HTTP 를 부르는 자리를 전부 grep 으로 세어**, 403 이 거절로 가지 않는 자리가 0 인지 표로 보고한다(리뷰가 못 본 자리가 있을 수 있다). 시험: 새 대화 403 · 모아보기 403 각 1건 이상.
2. **R1** — 잠금 키 문자열을 한 곳으로(`homeLockKey`).
3. **R2** — 목록 [귀가 대기] 줄 조건에서 `waitingCalls.isEmpty` 를 빼 「방 상세와 같은 조건」(`canHome` + 판 편집 권한)과 글자 그대로 같게.
4. **R3** — 늦게 온 설정 응답이 새 값을 덮지 않게(요청 순번 · 가장 나중에 **보낸** 요청의 응답만 적용). 시험 1건.
5. **R4** — `_recheck` 가 풀린 뒤 스트림을 열 때 앱이 뒤에 있으면 열지 않는다(또는 바로 pause). 시험 1건.
6. **R5** — 그룹 이름 40자 셈을 스펙대로 「앞뒤 공백 뺀 뒤 40자」. 넘으면 ✓ 꺼짐(새 글자 없음).
7. 「조용히 통과하는 자리」 2 — 「거절 상태에서는 배너 없음」 시험에 같은 시험 안 대조(거절 아님 → 배너 있음)를 넣는다.

새 화면 글자 0 · 새 의존성 0 · 통역 폴더 무변경.

## 검증

`cd app && fvm flutter analyze` · 고친 테스트 파일만 `fvm flutter test <파일들>` · 마지막에 `fvm flutter test` 전체 1회.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-fix1-report.md` — 항목별 고친 자리(`파일:줄`) · 채팅 HTTP 호출 자리 전수 표(자리 · 403 처리) · 시험 이름 · 수치.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "mobile 완료: <한 줄>" \
  --body "항목별 결과 / 채팅 호출 자리 수 · 403 누락 수 / 시험 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] mobile: <질문>" --enter`
