# [data · 고침 3] 허브 J28 ~ J34 추천대로 반영 (사용자 11-23 「추천으로 가라니까」)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · **18105 · 18222 손대지 마라**(GET 만 · 재기동은 코디 — 지금 다른 측정이 18105 를 쓰는 중이니 18105 는 절대 건드리지 마라) · 키 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 리포트 `$W/data-gap3-report.md`(J28 ~ J34 표 · 추천 칸) · 마지막 검수 `$W/review-data-gap3-r3.md`(PASS · P2-1 CAS-1056 PRP × 볼 꺼짐 · P2-2 J34 는 기계로 정할 수 있음) · 방식 = 앞 묶음(`build_batch9.py` 이어서 · 재현 가능).

## 결정(다시 묻지 마라) — 리포트 J28 ~ J34 **추천 칸 그대로** + 검수 r3 P2-1 · P2-2
- J28 이음(제품 원장 여럿 근거 예외로 적음) · J29 IND-2946 근거를 M9 「턱선 리프팅」 으로 바꿈 · 2948 · 2949 는 J28 과 같게 · J30 ~ J33 이음 · J34 이음(팔자 ⊂ 볼 부위 — 기계 판정) · CAS-1056 PRP × 볼 꺼짐(별칭 「꺼진 볼」) 이음.

## 할 일
1. 반영 · source_ref · 근거 종류.
2. silver-check · gold-check PASS(**작업 사본에서** · 스크래치 180MB 복사본 금지) · gold_hash 전(`e8f02287…`) → 후.
3. 리포트 판 올림 · 바뀐 목록 전 → 후(볼 주름 · 목 처짐 · 팔자 · 턱선 처짐).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: J28~J34" --body "반영 줄 / gold_hash"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] J28~J34 완료 — <한 줄>. 상세는 인박스." --enter
```
