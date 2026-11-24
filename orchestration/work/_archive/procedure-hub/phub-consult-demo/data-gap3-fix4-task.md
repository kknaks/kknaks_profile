# [data · 고침 4] J30 ~ J33 빼기 — 볼 주름 목록 16 → 6 줄어듦 (코디 판단 · 사용자 원칙 「품질 그대로」)

너는 procedure-hub 데이터 워커다(앞 고침 3 을 한 사람). 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · **18105 · 18222 손대지 마라**(GET 만 · 지금 측정이 18105 를 쓰는 중) · 키 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 리포트 `$W/data-gap3-report.md` v1.3(§「바뀐 목록」 볼 주름 16 → 6 · 코디 판단 필요 1).

## 결정(코디 · 다시 묻지 마라)
- **J30 ~ J33(IND-3283 ~ 3286 · M3 × 볼 주름) 4 줄을 이번 묶음에서 뺀다.** 까닭: 직접 줄이 생기면 허브 `concern-candidates`(`upper=auto`)가 상위 고민(주름)으로 올라가지 않아 명동점 볼 주름 목록이 16 → 6 으로 줄고, 새로 더해지는 명동점 진료항목은 0 이다. 데이터를 더해서 상담 목록이 줄면 안 된다(사용자 원칙 「품질 그대로」).
- 나머지(J28 · J29 근거 고침 · J34 · PRP × 볼 꺼짐)는 그대로 둔다.
- J30 ~ J33 은 사람 판단 표에 「보류 — `upper=auto` 규칙(직접 근거가 상위 넓힘을 막음)을 먼저 정해야 함」 으로 남긴다.

## 할 일
1. 4 줄 빼고 묶음 재현 · silver-check · gold-check PASS(작업 사본에서) · gold_hash.
2. **같은 꼴 전수**: 지금 gold 에서 「직접 줄이 있어 상위로 안 올라가는데, 상위로 올라가면 명동점 목록이 더 넓은 고민」 을 센다(고민 × 명동점 묶음 수 직접 vs 상위 · 표). 이번 묶음 · 앞 묶음 9 가 만든 직접 줄 때문에 줄어든 고민이 또 있는지 꼭(입꼬리주름 · 팔자 · 눈가주름 · 미간 …). 반영은 하지 말고 표만.
3. 리포트 판 올림(v1.4) · 목록 전 → 후.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: J30~33 빼기 · upper 전수" --body "gold_hash / 같은 꼴 줄어든 고민 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] J30~33 빼기 완료 — <한 줄>. 상세는 인박스." --enter
```
