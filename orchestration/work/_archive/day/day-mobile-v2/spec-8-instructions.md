# [planner] Delivery #262 · #263 v2 재결속 — 머지된 스펙 기준

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec`. 스펙 PR #955 가 **스쿼시 머지됨 = origin/main `3ae2317e`**. `git fetch origin && git checkout --detach origin/main` 위에서 재결속(브랜치 HEAD 246ccaf0 과 트리가 같은지 먼저 확인 · 다르면 멈추고 보고).

- 준비해 둔 요청: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-5-report.md` 의 경로 · 내용 + `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-6-report.md` 의 「v2 재결속 때 넣을 문구 갱신」(구현 사실 · 닫힌 OQ · migration 0013 · 0014 · 코드 PR CENTURION_DAY#266 = dev `5ece25ea` · dev 배포 성공 · DAY Dev 0.2.0 TestFlight (4) · Play internal vc4 업로드).
- `mediness start-delivery --mediness-repo <이 워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2 --github-repo MediSolveAIDev/CENTURION_DAY` 로 #262 · #263 같은 key contract_version 2 — `--plan` → `--apply`. baseline = `3ae2317e`.
- 상태 기록: 구현 = dev 머지 · dev 배포 완료 / 남은 것 = 실기기 확인(A-50 · I-6 · F3) · prod 서버 배포 · 정식 0.2.0 앱 — Issue 의 실행 단계 · 인수 조건에 그대로(완료로 쓰지 마라).
- **승인 receipt 는 적용하지 마라**(코디가 검수 뒤). 문서 수정 · 커밋 금지.
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-8-report.md`: 두 Issue 새 digest · baseline · 반영 항목 체크 · 승인 명령(적용 안 함).
- 끝나면 워크트리를 `git checkout kknaksss/day-mobile-v2-spec` 로 되돌린다. 완료 보고는 dispatch preamble 의 worker_done 그대로.
