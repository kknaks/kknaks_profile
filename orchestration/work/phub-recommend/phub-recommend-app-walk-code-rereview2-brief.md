# [reviewer_code] case3 반복 탐색 수정 3차 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- `review-app-walk-phase-a-code-v2.md`의 모든 FAIL/WARN
- `SPEC-006.md` 0.3.10 §3-4-1-5, `WORK-012.md` WP-1~3/5
- 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 현재 diff와 관련 시험. 기준 HEAD `078ac99`.

## 재검수

2차 FAIL인 복합 질문 facet 누락, 교차 target/scope 혼입, 근거 0 답변의 부재 단정, CLI 실제 분할/합성, 이웃 종류와 페이지 완료가 실제 경로와 시험에서 해결됐는지 확인한다. 사실 후보의 조용한 삭제와 safety 과단정, provenance/claim ID 유실도 본다. 기본 gate False와 WP-4 관계 어댑터 미구현을 분리해 판정한다. 새 결함도 지적한다.

각 항목 FAIL/WARN/PASS, 파일:줄·근거·최소 수정안을 보고하고 **WP-4 발주 가능 여부**를 명시한다. 실물 provider의 미확인 한도가 활성화 전 blocker인지도 판단한다.

## 허용 범위

- 읽기 전용. 보고 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-app-walk-phase-a-code-v3.md`만 생성.
- 코드·서버·DB·평가 수정/실행 금지. 필요한 소수 단위 시험만 격리 실행 가능.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
