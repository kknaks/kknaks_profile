# [backend] Hub 선택 관계 3차 검수 FAIL 수정

너는 Hub 코드 수정 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 기존 Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`의 미커밋 작업을 이어간다. 기준 HEAD `2edc190`.

## 읽을 것

- 프로필 레포 `orchestration/work/phub-recommend/review-hub-selected-code-v3.md` 전체
- `SPEC-005.md` §5-5·§6-9, `WORK-011.md`, `SPEC-006.md` §3-4-1-5

## 수정

1. `R8-0180`, `R8-0244` 등 interval `source_condition`을 임의 key의 같은 값으로 통과시키지 않는다. 원천에 의해 확인되는 조건 차원 `(key,value)`에만 결속한다. 차원을 확정할 수 없으면 인용 불가와 `unresolved_condition`을 반환한다. 틀린 key 음성 시험을 추가한다.
2. 일반 R8 claim도 source `claims[<fid>]` 경로가 실제 fact ID와 일치해야 한다. 다른 존재 claim path로 바꾼 fixture는 `error, complete=false`여야 한다. 공유 claim 규칙과 resolved/대안 검증도 유지한다.
3. §6-9 수용 관문: HEAD `2edc190`의 186 section 첫 페이지 ID 순서와 현재 결과를 비교하는 재현 가능한 증거를 남기고, 기존 peek compact byte·cut 인용 자격·`safety.management` 회귀를 확인한다. baseline 추출이 불가능하다면 사유와 남은 관문을 보고한다.

## 검증/보고

- 관련 단위 시험, DB 비의존 전체 시험, ruff, diff check. 서버·DB·평가 실행 금지.
- 코드·시험만 수정. 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/hub-selected-fix3-report.md`에 작성한다. 완료 시 dispatch preamble대로 `worker_done` 한 번.
