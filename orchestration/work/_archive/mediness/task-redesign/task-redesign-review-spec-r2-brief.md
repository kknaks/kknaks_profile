
# [reviewer_spec] 재검수 R2 — planner 정정분 판정

너는 앞서 task·incident 재정비 스펙을 FAIL 판정한 **mediness `reviewer_spec` 워커**다. planner 가 정정(R2)을 마쳤다 — 재검수하라.

- planner 정정 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/fix-r2-report.md`
- 네 원 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-spec-report.md` — **말미 재검수용 8항목 체크리스트가 이번 판정 기준**이다
- 워크트리·read-only 규칙·완료 보고 방식은 원 브리프(`task-redesign-review-spec-brief.md`)와 동일. taskId/dispatchId 는 이 dispatch 의 preamble 값

## 판정할 것

1. 원 리포트 FAIL V-1~V-6 각각 해소됐는지 (파일:줄 근거)
2. WARN W-1·W-2 해소, W-4 는 코디 지침(A축 폐기 예정 노트만) 대로 처리됐는지
3. 폐기 키워드 grep 스윕 재실행 — 활성 계약 잔존 0 확인 (폐기 표기·개정 이력·A축 폐기 예정 문서·동결 work-074 는 허용)
4. R2 에서 **새로 손댄 파일 6개**(spec-060·113·150·155·230·decision-tracking-engine.md)가 기존 계약을 부수지 않았는지 — 정정 범위 밖 변경이 섞였으면 지적
5. planner 가 스스로 정정한 «write 19→18 오독» 건(전 문서 18→17·57→56 통일) — 근거가 맞는지 spot 확인
6. Spec Coverage 3행(113·155·230) done→in_dev 강등이 derive 규칙상 맞는지
7. lint --strict mediness 범위 ERROR 0

리포트는 원 리포트에 **R2 재검수 절을 append** 하고 최종 판정(PASS/WARN/FAIL)을 내라. 문체 지적으로 FAIL 금지 — 기준은 원 브리프와 동일.

완료 보고는 원 브리프 §9 의 2채널 그대로 (`--from term_8412cd16-b0f5-4f5d-a841-da64055e98ba`).
