# [backend] Hub 전역 K8·공개 상태 수정

너는 Hub 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` 기존 미커밋 작업을 이어간다. 기준 HEAD `2edc190`.

프로필 레포 `orchestration/work/phub-recommend/review-hub-selected-code-v5.md`, SPEC-005 §5-5·§6-9, WORK-011을 읽는다.

1. 전역 K8의 정본 section=`checks`를 검증한다. K8-0027의 다른 존재 section 변조가 9쪽 끝에서 `found/complete=true`가 되지 않도록 하고 음성 시험을 추가한다.
2. Q139 원문이 다른 실제 메모로 변조된 경우 공개 status 열거 `found|empty|truncated|error` 중 `error`를 사용하고, 별도 `unresolved_scope` 사유와 `scope_complete=false`, `quotable=false`를 유지한다. REST/MCP 동일 계약 시험도 고친다.
3. 다른 전역 종류의 원문 검증 한계를 조사한다. 정본 원문과 안전하게 결속할 수 있는 유형은 검사하고, 불가능한 유형은 `quotable=false`를 보장하고 보고서에 한계를 명시한다. 모든 종류를 묶어 대규모 변경하지 말고 이번 인계 안전에 필요한 범위를 닫는다.

관련 시험, DB 비의존 전체 시험, ruff, diff check. 서버·DB·평가 실행 금지. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/hub-selected-fix5-report.md`. 완료 시 `worker_done` 한 번.
