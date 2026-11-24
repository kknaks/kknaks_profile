# [reviewer · 읽기만] SPEC-010 0.2.5 재검수 r6 — 0.2.3 ~ 0.2.5 변경분 (11-20)

너는 WP-1 을 검수한 워커다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`. SPEC-010 은 0.2.2 에서 PASS(`$W/review-spec-010-r5.md`) 뒤 세 번 고쳤다: 0.2.3(WP-0 실측 반영 · `$W/spec-010-fix6-task.md` · 실측 `$W/research-v05-facts.md`) · 0.2.4(상담 안의 주제 · `$W/spec-010-fix7-task.md`) · 0.2.5(주제 판단 = 규칙 + 이해 호출 topic 칸 · `$W/spec-010-fix8-task.md`). 결정 표 `$W/_RESUME.md` §2 11-20 행.

`$W/SPEC-010-consult-myeongdong.md` 0.2.5 의 **이 세 고침 변경분**만 본다: 사용자 · 코디 결정과 같은가 · 데이터(JSON v3 `1af2216c` · 허브 18105 gold `caa03560`)로 성립하는가 · 주제 규칙(TP1 ~ TP14)이 서로 모순 없고 시험(T1 ~ T13) 가능한가 · 0.4 이해 호출(`/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/clinic_chat/consult/understand.py` · `prompts/consult.json` pick)에 칸을 더하는 계약이 실제 코드와 맞는가 · WP-2 추가분 · WP 순서. 리포트 1 개만 · 다른 파일 수정 0 · 18222 손대지 마라.

산출 `$W/review-spec-010-r6.md`: 판정 · 지적(P0 / P1 / P2 · 근거 · 고칠 방향).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e9e9922f-2211-43e5-bd97-3403b59f0b99 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-010 r6" --body "판정 / 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review r6 완료 — <한 줄>. 상세는 인박스." --enter
```
