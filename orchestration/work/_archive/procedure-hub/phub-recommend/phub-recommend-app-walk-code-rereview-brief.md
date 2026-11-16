# [reviewer_code] case3 반복 탐색 코드 FAIL 재검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-app-walk-phase-a-code.md`의 모든 FAIL/WARN과 `app-walk-phase-a-fix-report.md`
- 같은 디렉터리 SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5
- 현재 앱 worktree의 코드 diff와 관련 시험. HEAD 078ac99.

## 재검수

1차 FAIL(키워드/slim 조기 배제, 안전·이웃·부재 완료, source/scope 대조, 큰 입력 복수 답·CLI 유실, deadline)이 **실제 실행 경로와 시험에서** 닫혔는지 확인한다. 특히 수집한 관련 fact를 Claude 전달에서 조용히 버리지 않는지, `unresolved_absence`의 필수 이웃/page 완료 증거, 보류 답이 사용자 질문에 대해 근거 없는 `정보 없음`을 쓰지 않는지 본다. `walk_coverage_mode=False` 기본값의 안전성과 활성화 전 필요한 실물 관문도 판정한다. 관계 WP-4는 아직 미구현이므로 그 범위를 구분하되 현재 코드가 관계값을 추정하면 FAIL로 센다. 새 결함도 지적한다.

각 항목 FAIL/WARN/PASS, 파일:줄·근거·최소 수정안을 보고하고 **WP-4 어댑터 발주 가능 여부**를 명시한다. 코드/서버/DB/평가 수정·실행 금지, 필요한 소수 단위 시험만 격리 실행 가능.

## 허용 범위

- 읽기 전용. 보고 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-app-walk-phase-a-code-v2.md`만 생성.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
