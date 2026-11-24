# [spec] SPEC-011 0.1.1 — 검수 지적 고침 (자동 · 11-23)

너는 SPEC-011 을 쓴 스펙 워커다. 앞 발주 `fetch-plan-spec-task.md` 규칙(읽기만 · 18222 · 18105 손대지 마라 · 커밋 0 · 서브에이전트 0 · 키 출력 0) 그대로.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 검수 `$W/review-spec-011.md`(FAIL · P1 4 · P2 9) · 검수 셈 사본 = 리포트 §5 의 `$R`.

## 할 일
- **P1-1 ~ P1-4 · P2-1 ~ P2-9 전부** 검수 리포트의 「고칠 방향」 대로 `$W/SPEC-011-fetch-plan.md` 를 0.1.1 로 · 수치가 바뀌는 곳은 `$W/fetch-plan-report.md` 도.
- P1-3: F20(이해 실패 · 대상 없음) 규칙을 고친 뒤 **실제로 다시 셈** — 표본 43 턴 + 표본 밖 장부 턴 19 개 전부(검수 15 포함) · 빠짐 · 상세 잃음 · lineup 이름만 따로 · 감소(표본 / 밖 나눠). 프롬프트 사본을 고쳐야 하면 고치고 돌린 판을 기록(r4 …). 앱 프롬프트 파일은 고치지 마라.
- P1-1: 「이름만 → 다음 턴 all → 상세 실림」 을 셈 스크립트로 확인할 수 있으면 a578 T5 → T6 · T7 로 보여라(못 하면 WP 시험으로만).
- DQ 는 DQ1 하나만 남긴다(P2-3 · P2-4).
- 끝에 「바뀐 것」 표(지적 ID → 절 · 줄).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-011 0.1.1" --body "지적 처리 수 / 표본 · 밖 빠짐 · 상세 잃음 · 감소"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-011 0.1.1 완료 — <한 줄>. 상세는 인박스." --enter
```
