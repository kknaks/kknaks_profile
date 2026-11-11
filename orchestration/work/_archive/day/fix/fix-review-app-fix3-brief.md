# [reviewer] fix 앱 수정 3 재확인 — 길게 누르기 메뉴(W1 · R1 · R2)

너는 **day `reviewer` 워커**(같은 터미널)다. read-only.

- 네 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-3-report.md`(W1 · R1 · R2)
- 작성자 수정 보고: `…/work/fix/app-fix3-report.md` · 브리프 `…/work/fix/fix-app-fix3-brief.md`
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` U-4 · C-A22

대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 `app/` — 네 앞 검수 뒤에 바뀐 것만.

## 볼 것

1. W1 · R1 · R2 가 풀렸는지(`파일:줄`).
2. 작성자의 「다시 재는 계기 12종」 표를 **네가 직접 코드에서 다시 세어** 빠진 계기가 없는지(말풍선 자리를 바꿀 수 있는 것 전부 — 메시지 더해짐 · 지워짐 · 수정 · 읽음 숫자 · 위로 더 불러옴 · 스크롤 · 키보드 · 회전 · 글자 크기 등).
3. 다시 재기가 **매 프레임 도는 무한 고리**가 되거나, 메뉴가 떠 있는 동안 목록 전체를 계속 다시 그리게 만들지 않는지 · dispose 뒤 콜백 · 리스너 해제.
4. R1: 그 메시지가 지워졌을 때 메뉴가 닫히는 길 — 닫힌 뒤 열려 있던 하위 창(삭제 확인 · 선택 복사 · 전달 시트)이 고아로 남지 않는지 · 남의 메시지 삭제 이벤트에는 닫히지 않는지.
5. 새 시험이 실제로 실패할 수 있는지 · 새 화면 글자 0 · 범위.

## 돌려 볼 것(각 1회)

```
cd app && fvm flutter analyze
cd app && fvm flutter test
```

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-fix3-report.md` — 판정 **FAIL / WARN / PASS** · 항목별 한 줄 · 네가 센 계기 수 · 수치.

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
