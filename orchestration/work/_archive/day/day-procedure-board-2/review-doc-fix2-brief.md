# [reviewer_doc] 리뷰 — SPEC-002 개정 ⑭(고객 검색 바로잡기 · 실물 확인 반영 · OQ 닫기)

너는 day reviewer_doc 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md`(+ 같은 폴더). **읽기만** — 파일 수정 · 커밋 금지 · KOS 호출 금지. 산출물 = 리포트 1개.

대상: `git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec diff`(spec-002 · log.md · 마지막 커밋 24949777 이후). 지시: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/planner-spec-fix2-brief.md`. 정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 결정 표(특히 11-10 고객 검색 바로잡음 · 11-09 데모 실물 확인 · HAR 확인 · 디자인 [재호출] 검정).

## 볼 것
1. 고객 검색: 대상이 「시술 완료」 탭 고객만인가 — 「카드가 생겼던 고객 전부 · 지난 방문 · 최근 방문일 · 결과 줄 · 정렬」 흔적이 **하나도** 안 남았나(`grep` 전수) · 찾는 말 = 이름(발음 · 영문) + 담당 원장 + 관리실 · 누르면 같은 차트
2. KOS 쓰기 표 확인 상태가 사실과 맞나(완료 취소 · 귀가 대기 1 · 2 · 재호출 = 데모 실물 · 원장 바꾸기 = HAR 덮어쓰기 1명) · 닫은 OQ(22 · 23 · 25 · 31)가 근거와 맞나 · 새 OQ-33
3. 결정에 없는 것을 새로 정한 곳 · 반대 문장 · 앞뒤 안 맞는 곳
4. `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-doc-fix2-report.md` · FAIL / WARN / PASS · 지적마다 파일:줄 + 근거.

## 완료 보고 (두 명령 모두)
```bash
orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer_doc 완료: <판정>" --body "<요약>"
orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] reviewer_doc 완료 — <한 줄>. 상세는 인박스." --enter
```
핸들은 dispatch preamble 값이 맞다.
