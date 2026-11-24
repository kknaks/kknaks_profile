# [reviewer · 읽기만] SPEC-011 0.1.1 재검수 (자동 · 11-23)

너는 SPEC-011 0.1.0 을 검수한 워커다. 앞 발주 `review-spec-011-task.md` 규칙 그대로(리포트 1 개만 · 수정 0 · 커밋 0 · 18222 · 18105 손대지 마라 · 키 출력 0).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 대상 `$W/SPEC-011-fetch-plan.md` 0.1.1 · `$W/fetch-plan-report.md` · `$W/fetch-plan/` · 고침 지시 `$W/spec-011-fix1-task.md` · 앞 검수 `$W/review-spec-011.md`.

## 볼 것
1. P1-1 ~ P1-4 · P2-1 ~ P2-9 가 각각 고쳐졌나(「바뀐 것」 표 ↔ 실제 절) · 고치면서 새로 생긴 모순.
2. 새 수치 재현(오프라인 · 저장 응답): 표본 −62.1% 빠짐 0 · 표본 밖 19 턴 −13.5% 빠짐 0 · 상세 잃음 7 · lineup 이름만 따로.
3. F20 규칙 고침이 다른 꼴 턴의 빠짐 · 감소를 바꾸지 않았나.
4. 남은 DQ1 하나가 맞나.
5. WP 를 코드 워커가 그대로 할 수 있나(자리 · 완료 조건 · 관련 시험).

## 산출
`$W/review-spec-011-r2.md`: 판정 PASS / FAIL · 지적별 처리 표 · 새 지적(P0 / P1 / P2) · 재현 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-011 0.1.1" --body "판정 / 새 P0 · P1 · P2 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review SPEC-011 0.1.1 완료 — <한 줄>. 상세는 인박스." --enter
```
