# [data · 고침 2] 허브 구멍 3 — 사람 판단 J 반영 + 재검수 P2 5 (사용자 승인 11-23 「응 추천대로」)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · **18105 · 18222 손대지 마라**(GET 만 · 재기동은 코디) · 키 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 리포트 `$W/data-gap3-report.md`(고침 1 판 · gold `ab5eebc9…` · §4 J 표) · 재검수 `$W/review-data-gap3-r2.md`(PASS · P2-1 ~ P2-5) · 방식 = 묶음 9 `$S/drafts/clinic-supplement/clinic-a-20261119/build_batch9.py`(같은 묶음에 이어 붙이거나 묶음 10 — 앞 방식대로 재현 가능하게).

## 사용자 결정 — 리포트 §4 「사람 판단」 J 표의 **추천 칸 그대로**(다시 묻지 마라)
- 이음: J6 ~ J15 중 **처짐 4**(볼처짐 · 볼살 처짐 · 턱선무너짐 · 불독살) · J17(온다 전신 × 목주름) · J21(HIFU 얼굴 × 턱선무너짐) · J22(고주파 얼굴 × 볼처짐 · 볼살 처짐 · 불독살) · J24(니들RF × 리프팅 · 타이트닝 · 처짐 개선 — 계열 시술 하나 = 시술 줄 예외로 적음).
- 안 이음: J6 ~ J15 의 주름 5 · 눈꺼풀 처짐 · J1 · J2 · J16 · J23 · J27 · 규칙으로 정한 12 줄.
- 보류: J25 · J26(근거가 판매 문장뿐 — 반영 안 함 · 리포트에 보류로).
- 위와 리포트 표 칸이 다르면 **리포트 추천 칸**이 기준(위는 요약).

## 할 일
1. J 반영(근거 = 리포트 J 표의 원장 포인터 · source_ref · 근거 종류).
2. 재검수 P2-1 ~ P2-5 「고칠 방향」 대로(묶음 상품 문장 단독 근거 2 줄 처분 · 분류 표 · 다른 계열 포인터 · 셈 스크립트 정렬 · 「근거 없음」 에서 계열 원장이 고민을 직접 적은 5 쌍).
3. silver-check · gold-check PASS(**작업 사본에서** — 스크래치 180MB 복사본에서 돌리지 마라) · gold_hash 전 → 후 · 재현.
4. 리포트 판 올림 · §6 목록 전 → 후(입꼬리주름 · 팔자 · 타이트닝 · 볼처짐 · 턱선 · 목주름).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 허브 구멍 3 고침 2" --body "J 반영 줄 / P2 닫음 / gold_hash"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 허브 구멍 3 고침 2 완료 — <한 줄>. 상세는 인박스." --enter
```
