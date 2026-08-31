
# [reviewer_code] WP-126 코드 검수 — 미커밋 delta (BE 26 + FE 3 + 0135 backfill)

너는 **mediness `reviewer_code` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign` — **read-only.** 코드 수정·테스트 실행 금지.
검수 범위 = **현재 미커밋 delta**(`git status` + `git diff` + untracked). 직전 커밋(62e2400c, WP-125)은 이미 검수·확정됐다 — 다시 보지 마라. delta 구성: BE 26파일(WP-126) + front BFF 3건 삭제(WP-126 P6) + `0135_*.py` backfill 수정(코디가 넣은 WP-125 OI-6 해소 — 사용자 확정·로컬 검증됨).

## 판정 기준 (SoT)

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/30-work/work-126-incident-workflow-realign.md`
- `.../products/mediness/20-spec/spec-152-incident-response-workflow.md` (cc 는 2026-08-31 정정본 — AI 초대 후보)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2
- 발주 브리프: `.../task-redesign-wp126-be-brief.md` · `.../task-redesign-wp126-fe-brief.md`

## 체크리스트

1. **판정 1벌**: `round_rule.active_round_complete` 가 유일 정본이고 4벌 잔존 0 인지. `factory.has_open_in_run_chain` 의 «종결 사전조건» 역할 분리가 계약과 맞는지. 부수 버그 수정(eval_statuses CANCELED 누락)이 판정 의미를 바꾸지 않는지 — 이건 «취소도 terminal» 계약의 착지인지 확인
2. **run 감사**: 세 종결 경로가 전부 `set_run_status` 경유(우회 0), payload 미사용, cause=human_approval, migration 0. 추적 Task 정리 훅(task_canceled cause=run_closed)이 §종결 시 태스크 정리와 일치
3. **fail-loud**: `ERR_SLACK_NOT_CONFIGURED` 503 + `ExecutionUnavailable` seam — 일반 DomainError 삼킴 경로가 회귀 안 했는지, 실패 원장 커밋 후 재-raise 순서가 안전한지
4. **RegenGate 이벤트 이름 가드** — 소비자 5자리 전수 선언·행위 동형 주장 검증
5. **cc (B) 유지** — 삭제·확대 0, 사유 주석만
6. **죽은코드 13종** — per-symbol grep 재확인, STATUS_FAILED 존치, W6(patch_task 죽은 인자) 처리
7. **0135 backfill** — 소급 insert 가 append-only 원장 계약을 지키는지(과거 행 무수정), 가드가 뒤에 남아 있는지
8. allowed_paths: BE=back/, FE=front/ 3건 삭제만, 그 외 침범 0
9. 워커 미결 5건 처리 적정성 — 특히 ② resolver 실효 3단(4단째 approve actor 가 lead 와 중복) 이 배선 확장 없이 보고로 남긴 판단

## 산출물

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-code-wp126-report.md` — 판정(PASS/WARN/FAIL) + 위반(파일:줄). 문체 지적 FAIL 금지.

## 완료 보고 — 문구 변경 금지

> ⚠ 핸들은 dispatch preamble 값을 믿어라. **커밋·push·PR 금지.**

```bash
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_9a7b4cdc-3b5c-4a87-aff8-5f378f7ceb30 \
  --type worker_done \
  --task-id <dispatch preamble 의 taskId> \
  --dispatch-id <dispatch preamble 의 dispatchId> \
  --subject "reviewer_code(WP-126) 완료: <판정 한 줄>" \
  --body "판정 / 항목별 결과 / 위반 목록(파일:줄) / 미결"

orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] reviewer_code(WP-126) 완료 — <판정 한 줄>. 상세는 인박스." --enter
```
