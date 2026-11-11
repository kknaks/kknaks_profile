# [reviewer] fix 앱 수정 1 재확인 — 수정분만

너는 **day `reviewer` 워커**(앱 · 서버 검수를 한 같은 터미널)다. read-only.

- 네 앱 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-report.md` (W1 · R1 ~ R5 · 조용히 통과 2)
- 작성자 수정 보고: `…/work/fix/app-fix1-report.md` · 브리프 `…/work/fix/fix-app-fix1-brief.md`
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` U-1 · C-A19 · U-7

대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 `app/` — 네 앞 검수 뒤에 바뀐 것만. backend 워커가 같은 워크트리에서 서버 수정을 하고 있다(`backend/` 는 대상 아님).

## 볼 것

1. W1 · R1 ~ R5 · 조용히 통과 2 가 각각 풀렸는지(`파일:줄`).
2. 작성자의 「채팅 HTTP 호출 자리 26곳 전수 · 403 누락 0」 표를 **네가 직접 grep 으로 다시 세어** 빠진 자리가 없는지. 작성자가 더 찾은 2곳(전달 시트 직원 목록 · 동영상 재생)의 고침이 옳은지 — 특히 재생 실패 때 `refreshRooms` 로 판정하는 방식이 다른 오류(네트워크 끊김)를 거절로 잘못 보내지 않는지 · 전달 시트에서 401 처리가 세션 끝 규칙과 같은지.
3. 공통 `_guard` 가 403 을 처리한 뒤 다시 던지는 오류를 화면이 또 토스트로 내는 자리가 없는지(「조작 중 403 = 본문 안내만 · 토스트 없음」).
4. R3 순번 방식이 설정 화면 PUT → GET 흐름에서 실제로 늦은 응답을 버리는지 · R5 로 포매터를 뺀 뒤 40자 넘는 입력이 저장되지 않는지.
5. 수정이 새 문제를 만들지 않았는지(새 화면 글자 0 · 범위 `app/lib` · `app/test`).

## 돌려 볼 것(각 1회)

```
cd app && fvm flutter analyze
cd app && fvm flutter test
```

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-fix1-report.md` — 판정 **FAIL / WARN / PASS** · 항목별 한 줄 · 네가 센 호출 자리 수 · 수치.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_4afcc88b-79e9-4f89-82de-783b5f10c7c9 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: <판정 · 한 줄>" \
  --body "판정 / 항목별 / 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] reviewer 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```
