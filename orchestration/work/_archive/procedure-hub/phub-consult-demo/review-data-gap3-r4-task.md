# [reviewer · 읽기만] 허브 J28 ~ J34 + J30~33 빼기 검수 r4 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · silver · gold · 스크립트 · 허브 · 앱 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(GET 만 · 새 gold 는 허브 코드를 프로세스 안에서 적재해 읽기만 · 포트 열지 마라) · 키 값 출력 0 · LLM 0 · **검사(silver-check · gold-check)를 스크래치 180MB 복사본에서 다시 돌리지 마라**(30 분 넘게 안 끝남) — 데이터 워커가 남긴 검사 출력 · 재현 로그와 묶음 재현 바이트 대조로만.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 리포트 `$W/data-gap3-report.md` v1.4(gold `8f65957f…`) · 지시 `$W/data-gap3-fix3-task.md` · `$W/data-gap3-fix4-task.md` · 앞 검수 `$W/review-data-gap3-r3.md`.

## 볼 것
1. 새 줄 · 근거 고침(J28 · J29 · J34 · PRP × 볼 꺼짐)이 지시 그대로인가 · 원장 포인터 원문 대조 전부.
2. J30 ~ J33 이 정말 빠졌나 · 볼 주름 16 복귀(새 gold 프로세스 안 적재로 셈).
3. 「같은 꼴 전수」(직접 줄 때문에 상위 넓힘이 막혀 줄어든 고민) 표가 맞나 — 셈 다시 · 묶음 9 · 10 때문에 줄어든 고민 0 이 사실인가 · 「명동점 0 72 는 구조」 판단.
4. 지어내기 0 · 원칙(고민 · 제품은 케이스에만 · 케이스 코드 안 바뀜).

## 산출
`$W/review-data-gap3-r4.md`: 판정 PASS / FAIL · 지적 · 원문 대조 표 · 재현 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from <내 handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: 허브 r4" --body "판정 / P1 · P2"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review 허브 r4 완료 — <한 줄>. 상세는 인박스." --enter
```
