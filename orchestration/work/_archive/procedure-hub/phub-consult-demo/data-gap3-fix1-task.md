# [data · 고침 1] 허브 구멍 3 — 검수 FAIL 반영 (사용자 승인 11-23 「응 추천대로해」 범위)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · **18105 · 18222 손대지 마라**(GET 만 · 재기동은 코디) · 키 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 앞 발주 `$W/data-gap3-task.md` · 앞 리포트 `$W/data-gap3-report.md` · **검수 `$W/review-data-gap3.md`(FAIL · P1 1 · P2 5)**.

## 할 일
1. **P1 · P2 전부** 검수 「고칠 방향」 대로(OUT-1622 — 제품 한 개 문장을 시술 줄로 올려 티타늄 · 포트라가 근거 없이 들어간 것 · 빠진 「풀페이스필러 × 눈 꺼짐」 등). 같은 꼴(제품 문장 → 시술 줄)이 효과 10 · 고민 36 에 또 있는지 전수.
2. **사람 판단 J1 ~ J26 은 반영하지 마라**(사용자 답 대기).
3. 묶음 9 재현 · silver-check · gold-check PASS · gold_hash 전 → 후. **검사는 작업 사본에서 앞과 같은 방식으로**(스크래치 180MB 복사본에서 돌리면 30분 넘게 안 끝났다 — 피하라).
4. 리포트 `$W/data-gap3-report.md` 판 올림 · §6 셋 전 → 후 목록 다시.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 허브 구멍 3 고침 1" --body "P1 · P2 닫음 / gold_hash / 타이트닝 · 팔자 · 입꼬리 목록 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 허브 구멍 3 고침 1 완료 — <한 줄>. 상세는 인박스." --enter
```
