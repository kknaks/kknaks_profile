# [reviewer · 읽기만] 고침 2(내부 note · 목록 속사정) 검수 (자동 · 11-23)

앞 발주 `review-fetch-code-task.md` 규칙 그대로(리포트 1 개만 · 수정 0 · 커밋 0 · 18222 · 18105 손대지 마라 · 실물은 빈 포트 · 키 출력 0). `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`

## 대상
발주 `$W/fetch-fix2-task.md`(사용자 결정: 아는 것만 · 지어내지 않음 · 모르면 돌려서 · 모름 · 앱 사정 말하지 않음) · 리포트 `$W/fetch-fix2-report.md` · `git -C $A diff`(이번 변경).

## 볼 것
0. 앞 검수 `review-fetch-fix1.md` P1-1(kos R3 note 읽어 줌) · P2-2(목록 · 거르기 속사정) · P2-3 이 고쳐졌나 · note 가 답 재료로 가는 자리가 다 막혔나(grep 전수) · 확인 필요 진료항목을 돌려 말하는가.
1. 결정대로인가 — 「없어요 · 정보가 없 · 자료가 없 · 가져온 · 모르」 류 문장이 규칙 · 판정 줄에서 다 막혔나(grep 전수) · 막다가 **지어내게** 되지 않았나.
2. **실물 직접**: 빈 포트에서 73bd · ecc6 · 03b8 + **허브 행이 빈 칸을 묻는 질문 3 개 이상**(예: 필러 개요 · 명동점에 없는 시술 · 자료 없는 부작용 질문 — 장부 · 허브로 빈 칸을 찾아 골라라)을 돌려 답이 돌려 말하는지 · 지어낸 상세 0(자료 줄 대조) · 사람 눈으로 어색하지 않은지.
3. P2-1(parse 꼬리 조각) · P2-4 처리 · 앞 고침(fetch · 토큰 기록 · 화면)이 안 깨졌나 — 관련 시험.

## 산출
`$W/review-fetch-fix2.md`: 판정 PASS / FAIL · 지적 · 실물 표(질문 · 답 앞 2 줄 · 지어냄 · 모름 문장).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: 고침 2" --body "판정 / P 수 / 빈 칸 질문 결과"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review 고침 2 완료 — <한 줄>. 상세는 인박스." --enter
```
