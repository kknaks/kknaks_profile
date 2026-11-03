# [reviewer_code] case3 반복 탐색 4차 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v3.md` 전체와 `app-walk-phase-a-fix3-report.md`
- `SPEC-006.md` 0.3.10 §3-4-1-5, `WORK-012.md` WP-1~3/5
- 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff, 기준 HEAD `078ac99`.

## 검수

이전 FAIL/WARN이 실제 실행 경로와 음성 시험에서 닫혔는지 확인한다. 핵심은 (1) 지원된 facet 부분 답변과 미완료만 유보, (2) 답 문장의 주장·대상·facet·scope·안전 근거를 원문 fact와 검증하고 분할/합성에도 적용, (3) provider 한도 미설정 시 fail-closed 및 system/user 전체 바이트 계산, CLI 분할 cost/timing 합산, (4) clause별 대상/facet, 제외 원문 원장, Jev deadline이다. 안전 문구가 사실 인용을 가장한 허위 확신을 내지 않는지 본다. WP-4 미구현 경계와 기본 gate False도 분리해 판정한다. 새 결함도 지적한다.

항목마다 PASS/WARN/FAIL, 파일:줄·근거·최소 수정안, WP-4 발주 가능 여부와 활성화 전 남은 관문을 명시한다.

## 허용 범위

- 읽기 전용. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v4.md`만 생성.
- 코드·서버·DB·평가 수정/실행 금지. 필요한 소수 단위 시험만 격리 실행 가능.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
