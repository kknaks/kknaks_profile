# [data · 고침 5] 허브 검수 r4 P2 3 닫기 (사용자 「추천으로 가라니까 다 끝내」 · 단계 끝 = open 0)

너는 procedure-hub 데이터 워커다(검수 r4 를 한 사람이 그대로 고친다). 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · **18105 · 18222 손대지 마라**(GET 만 · 다른 워커가 18105 로 측정 중) · 키 출력 0 · **검사는 작업 사본에서**(스크래치 180MB 복사본 금지).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 검수 `$W/review-data-gap3-r4.md`(PASS · P2-1 ~ P2-3) · 리포트 `$W/data-gap3-report.md` v1.4 · 앞 지시 `$W/data-gap3-fix3-task.md` · `$W/data-gap3-fix4-task.md`.

## 할 일
1. **P2-1 ~ P2-3 전부** 검수 「고칠 방향」 대로(추천이 있으면 추천대로 · 다시 묻지 않음). P2-1 이 데이터 줄을 바꾸면(근거 제품이 케이스에 안 붙은 것) 근거를 케이스에 붙은 제품 원장으로 좁히거나, 근거가 안 남는 줄은 뺀다 — 지어내기 0.
2. 셈 스크립트(`upper_survey.py`)를 묶음 폴더에 남기고 다시 돌려 표 값 재현.
3. 데이터가 바뀌면 silver-check · gold-check PASS · gold_hash 전(`8f65957f…`) → 후 · 바뀐 목록 전 → 후.
4. 리포트 v1.5.

## 완료 보고 — 2채널(둘 다) · `<내 handle>` 은 네 터미널 handle
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from <내 handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 허브 r4 P2" --body "P2 닫음 / 데이터 바뀜 여부 / gold_hash"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 허브 r4 P2 완료 — <한 줄>. 상세는 인박스." --enter
```
