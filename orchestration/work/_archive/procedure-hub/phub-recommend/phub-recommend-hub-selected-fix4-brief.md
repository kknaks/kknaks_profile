# [backend] Hub 전역 메모 출처 결속 결함 수정

너는 Hub 코드 수정 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`의 기존 미커밋 작업을 이어간다. 기준 HEAD `2edc190`.

프로필 레포 `orchestration/work/phub-recommend/review-hub-selected-code-v4.md`, SPEC-005 §5-5·§6-9, WORK-011을 읽는다.

Q139 `scope:all#evidence#step8_notes[26]`의 원천 file/path를 다른 존재 행으로 바꿔도 `quotable=true`가 되는 FAIL을 고친다. 전역 fact 중 정본 ID로 source path를 도출할 수 있는 모든 종류를 조사해, ID·원문·출처 경로를 결속한다. 불일치 시 `error/scope_complete=false` 또는 해당 행 `quotable=false`와 명시적 미완료를 반환한다. 소수 ID의 하드코딩만으로 끝내지 않는다. claim/conditional/resolved/대안과 REST/MCP 공통 코어 회귀를 유지한다. 다른 존재 path, 다른 file, 다른 owner 등 음성 시험을 넣는다.

관련 시험, DB 비의존 전체 시험, ruff, diff check 실행. 서버·DB·평가 실행 금지. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/hub-selected-fix4-report.md`. 완료 시 `worker_done` 한 번.
