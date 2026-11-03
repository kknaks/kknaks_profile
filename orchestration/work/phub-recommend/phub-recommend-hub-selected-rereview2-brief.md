# [reviewer_code] Hub 선택 관계 3차 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- `review-hub-selected-code-v2.md`의 FAIL/WARN
- `SPEC-005.md` §5-5·§6-9, `WORK-011.md`, `SPEC-006.md` §3-4-1-5
- Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` 현재 diff, 기준 HEAD `2edc190`.

## 재검수

Q139 인접 pair만 인용, 조합 내부 비지원 쌍과 pair 없는 호출의 차단, R8-0144 조건 key/value 결속, claim/conditional/resolved/대안 owner 검증을 실물 Gold 메모리 fixture와 음성 시험으로 확인한다. 특히 같은 claim이 여러 edge에 명시된 32개 공유 사례의 일반 규칙이 손상된 다른-owner edge를 허용하지 않는지, 원 owner가 선택 pair를 지원하지 않는 텍스트를 잘못 인용하지 않는지 본다. 전역 550행 페이지 재조립과 기존 §6-9 페이지 회귀 증거도 판정한다. 새 결함도 지적한다.

항목마다 PASS/WARN/FAIL, 파일:줄·근거·최소 수정안, **앱 WP-4 인계 가능 여부**를 명시한다.

## 허용 범위

- 읽기 전용. 보고 파일 `orchestration/work/phub-recommend/review-hub-selected-code-v3.md`만 생성.
- 코드·서버·DB·평가 수정/실행 금지. 필요한 소수 단위 시험만 격리 실행 가능.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
