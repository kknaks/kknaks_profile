
# [planner] WP-126 정정 R2 — 검수 WARN 4건 해소

너는 mediness `planner` 워커다. WP-126(incident 재정비 WP) 검수에서 **WARN(FAIL 0)** — 정정 4건이다.

리뷰 리포트(필독): `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-wp126-report.md`
원 발주 브리프: `.../work/task-redesign/task-redesign-wp2-brief.md` (allowed_paths·완료 보고 동일. taskId/dispatchId 는 이 dispatch preamble)
워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec`

## 고칠 것

**W1 — run 감사 재설계 (사용자 확정 반영).** 실측: `workflow_run_events` 원장이 이미 존재하고 `set_run_status`(runtime.py:363)가 이미 쓴다. payload 컬럼은 **의도적 부재**(models docstring), cause 는 닫힌 4어휘. 사용자 결정 = **payload 요구 폐기**:
- spec-152 §run 감사의 「정리한 Task id 목록을 payload 에」 요구를 정정 — run 원장에는 상태 변경+cause 만, 목록은 각 Task 의 `task_canceled` 이벤트 + execution 사슬 역조회로 충분함을 명시 (**이 문장 정정에 한해 SPEC 본문 수정 허용** — 개정 노트·log 1:1 기록)
- WP-126 P2 를 «신설»이 아니라 «기존 원장 사용»으로 재서술, cause 어휘 확장 필요 여부를 실측 기준으로 확정, **migration 0 확정**, OI-5 닫기
**W2 — 죽은 코드 목록 재실측.** `STATUS_FAILED` 는 살아 있음(incident/const.py:42 → surface.py `_TERMINAL_RUN_STATUSES`) — 목록에서 제외/정정. 고아 pyc 는 현재 0건 — 항목 제거. 나머지 상수 3종(참조 0)은 유지
**W3 — 완료됨(코디 처리).** log.md 에 코디 정정 행이 추가됐다 — 네 log 행의 「SPEC 본문은 고치지 않았다」 서술이 W1 반영 후에도 정확한지 확인하고 필요하면 그 행만 갱신
**W4 — Code Surface 좌표 현행화.** round_complete :340→:321 · set_run_status :220→:363 · on_event :88→:80 · slack/complete :797→HEAD:830(작업본 제거 중이면 그 사실 병기)

## 검증

`python3 scripts/lint-pipeline.py --strict` — mediness ERROR 0. 리포트의 지적 좌표를 스스로 재확인.

## 하지 말 것

- W1 문장 외 SPEC 본문·도메인 문서·WP-125 수정 금지
- 코드 레포 수정 금지(read-only 실측만)

완료 보고 = 원 브리프 §9 2채널 그대로. --from 은 네 새 터미널 handle 로 채워라(아래 dispatch preamble 참조).
