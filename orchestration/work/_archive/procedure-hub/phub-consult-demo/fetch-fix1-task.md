# [code] SPEC-011 구현 고침 1 — 검수 P2 4 (사용자 승인 11-23)

앞 발주 `fetch-plan-code-task.md` 규칙 그대로(앱 워크트리만 · 커밋 0 · 18222 · 18105 손대지 마라 · 실물은 빈 포트 · 키 출력 0 · 관련 시험만 · 전체는 마지막 한 번). 검수 `$W/review-fetch-code.md` §5 P2-1 ~ P2-4. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`

## 사용자 결정(다시 묻지 마라) — 답 말투
**아는 것만 말한다 · 지어내지 않는다 · 모르는 것은 돌려서 말한다.** 「개요 정보는 없어요」 · 「정보가 없어요」 · 「새로 가져온 자료가 없어서」 처럼 **모른다 · 자료가 없다 · 앱 사정**을 손님에게 직접 말하지 않는다(신뢰가 떨어짐). 대신 가진 자료로 답할 수 있는 것(그 시술의 다른 칸 · 명동점 진료항목 · 상담 때 확인)을 자연스럽게 이어 말한다. 모르는 것을 아는 척 채우지 않는다.

## 할 일
1. **P2-2 · P2-3 · 위 결정**: 답 규칙(`prompts/consult.json` kos rules R15 근처 · `system_v3` · 「앱 판정」 의 EM `empty[]` 를 답에 넘기는 자리 — grep 으로 「없어요」 를 부르는 규칙 · 판정 줄을 전수)을 고친다. `empty[]` 는 「그 칸 말하지 않기」 표지로 쓰고 「없음」 문장 재료로 쓰지 않는다. 새 줄 0 · `seen_lines` 만 있는 턴은 앞 자료로 답하고 가져왔는지 여부는 말하지 않는다.
2. **P2-1**: `verify.parse` 맨 끝 객체는 `targets` 또는 `kind` 칸이 있는 것만 · 시험 「꼬리 조각 객체」.
3. **P2-4**: `$W/fetch-code-report.md` 에 「캐시 상태에 따라 creation ↔ read 가 옮겨 감 · 합으로 볼 것」 주석.
4. **실물**: 빈 포트에서 73bd · ecc6 · 03b8 다시 돌림 + **장부 전체 답에서 「없어요 · 없습니다 · 정보가 없 · 자료가 없 · 가져온」 꼴 문장 grep 표(전 → 후)**. 후 = 0 · 대신 무엇을 말했나 앞 2 줄 · 지어낸 상세 0(자료 줄과 대조).

## 산출
`$W/fetch-fix1-report.md`: 바뀐 파일:줄 · grep 전 → 후 표 · 실물 3 대화 답 앞 2 줄 · 시험.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: 고침 1(P2 4)" --body "「없어요」 문장 전 → 후 / 지어냄 / 시험"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 고침 1 완료 — <한 줄>. 상세는 인박스." --enter
```
