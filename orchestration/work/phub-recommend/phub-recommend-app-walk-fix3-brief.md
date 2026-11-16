# [backend] case3 반복 탐색 3차 검수 FAIL 수정

너는 앱 코드 수정 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 기존 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 미커밋 작업을 이어간다. 기준 HEAD `078ac99`.

## 계약

- `review-app-walk-phase-a-code-v3.md`의 FAIL/WARN을 모두 읽고 실제 코드 경로에서 닫는다.
- `SPEC-006.md` 0.3.10 §3-4-1-5, `WORK-012.md` WP-1~3/5와 맞춘다.
- 가장 중요한 두 FAIL: (1) 지원된 facet은 근거로 부분 답변하고 미완료 facet만 유보한다. (2) 생성된 각 문장과 대상/facet/scope/안전 주장을 해당 원문 fact가 실제 지지하는지 확인한다. 단순 ID/flag 문자열 검사는 부족하다. 분할 묶음과 최종 합성 모두 같은 검증을 거친다.
- CLI/SDK 실제 입력 한도가 확인되지 않으면 임의로 0=무한 입력을 허용하지 않는다. 설정 가능한 provider 한도와 미설정 시 fail-closed 처리를 명확히 하고, CLI 분할의 timing/cost를 합산해 `_finish`에 전달한다.
- facet을 clause/span별 대상에 묶어 불필요한 전체 target 탐색을 피하고, 후보를 제외했다면 원본·source·scope·이유를 원장에 남긴다. Jev 이웃 선택에도 남은 deadline을 적용한다.
- 관계 WP-4 미구현 경계와 `walk_coverage_mode=False` 기본값을 유지한다. 실물 서버/DB/50·239×3 평가는 실행하지 않는다.

## 검증/보고

- 결함을 드러내는 최소 시험을 추가하고 관련 case3 및 전체 기존 시험, ruff, diff check를 실행한다. 실물 provider 한도/TTFT/QID 미확인 항목은 사실대로 보고한다.
- 코드·시험만 수정. 커밋·push·PR 금지. 보고 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/app-walk-phase-a-fix3-report.md`를 작성한다. 완료 시 dispatch preamble대로 `worker_done` 한 번.
