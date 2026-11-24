# [reviewer · 읽기만] 허브 데이터 구멍 3 재검수 r2 — 고침 1 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · silver · gold · 스크립트 · 허브 · 앱 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(18105 GET 만 · 새 gold 는 허브 코드를 프로세스 안에서 적재해 읽는 것만 허용 · 포트 열지 마라) · 키 값 출력 0 · LLM 호출 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 대상 `$W/data-gap3-report.md` · 묶음 9 `$S/drafts/clinic-supplement/clinic-a-20261119/build_batch9.py` · 기준 사본 `$S/archive/silver-before-clinic-a-20261119-b9/` · 발주서(기준) `$W/data-gap3-task.md` · 앞 방식 `$W/concern-apply-task.md` · 매핑 JSON(읽기만) `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/data/kos/myeongdong-mapping-20261120-v3.json`.

## 볼 것
1. **지어내기 0** — 새 고민 36 · 효과 10 줄마다 source_ref 원장 포인터를 bronze 원문에서 직접 열어, 그 문장이 그 케이스 · 시술과 그 고민 · 효과를 실제로 말하나(표본 15 줄 이상 · 효과 10 은 전부). 「넓은 케이스」 규칙(같은 방법 · 조직 · 재료 + 좁은 케이스 원장 근거)이 너그럽지 않나 — 얼굴 전체 케이스에 붙은 부위 고민이 실제로 그 시술로 하는 것인가.
2. **원칙** — 고민 · 제품은 케이스에만 · 효과는 시술 · 케이스 줄 · 케이스 코드 안 바뀜 · 11-20 「효과 찾기에서 계열 · 제품 줄 뺌」 과 어긋남 없나.
3. **재현** — `build_batch9.py` 다시 돌려 같은 바이트(스크래치로) · silver-check · gold-check 다시 돌림 · gold_hash `(리포트의 새 해시)` 같은가.
4. **전수 셈** — §2 (a) · (b) 표를 다시 세어 같은가 · 「근거 없음」 으로 둔 것 중 원장 근거가 있는데 빠진 것(표본).
5. **사람 판단 32 줄(J1 ~ J26)** — 추천이 원장 근거와 맞나 · 기계가 정할 수 있는데 올린 것.
6. **전 → 후 목록**(§6) — 새 gold 를 프로세스 안에서 적재해 다시 셈.

## 산출
`$W/review-data-gap3-r2.md`: 앞 검수 `$W/review-data-gap3.md` P1 1 · P2 5 가 다 닫혔나(지적마다 닫힘/열림 · 근거) + 새로 생긴 것 · 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 · 고칠 방향) · 원문 대조 표 · 재현 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: 허브 구멍 3 r2" --body "판정 / P0 · P1 · P2 수 / 원문 대조 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review 허브 구멍 3 r2 완료 — <한 줄>. 상세는 인박스." --enter
```

## 주의
- 검사(silver-check · gold-check)는 **스크래치 180MB 복사본에서 돌리지 마라**(지난번 30분 넘게 안 끝남). 데이터 워커가 남긴 검사 출력 · 재현 로그를 읽고, 재현은 `build_batch9.py` 바이트 대조로만.
