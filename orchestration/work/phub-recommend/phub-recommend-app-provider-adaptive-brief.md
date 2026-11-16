# [backend] case3 생성 입력 적응형 처리

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 WP-4까지 이어진 미커밋 코드를 수정한다. 기준 HEAD `078ac99`.

## 이유와 정본

프로필 레포 `SPEC-006.md` 0.3.10 §3-4-1-5와 `WORK-012.md` WP-5를 읽는다. 공식 Claude 문서상 현재 기본 `claude-sonnet-5-5`의 context는 1M tokens이고 SDK에는 `messages.count_tokens`가 있다. 현재 설정 기본 provider는 `claude-cli`, API key는 필수가 아니다. 고정 8/20/15KB를 그래프 탐색 종료 조건으로 사용해서는 안 되며, **최종 선별 사실만 모델에 보내야 한다.** 현재 `walk_input_max_bytes=None`에서 모델 호출을 건너뛰는 경로는 활성화 장애다.

공식 근거:
- https://platform.claude.com/docs/en/models/sonnet-5-5/overview
- https://platform.claude.com/docs/en/build-with-claude/context-windows
- https://platform.claude.com/docs/en/build-with-claude/token-counting

## 구현

- 탐색은 지원·부재 완료 상태로 끝내고 생성 입력 한도 때문에 미탐색 사실을 버리지 않는다. `None` 기본 설정은 모델 호출을 허용한다. 먼저 검증된 선별 사실로 한 번 호출한다. `walk_input_max_bytes`가 명시되면 운영자의 입력 제한/분할 override로만 사용한다.
- SDK는 가능하면 `count_tokens`로 실제 system+messages 입력을 재고 모델 context 여유를 확인한다. CLI는 계정/API key를 요구하는 count 호출에 의존하지 말고 실제 CLI의 context 초과 오류·stop을 감지해 선택 사실 묶음으로 재시도한다. CLI 내부 래핑 크기를 임의 고정 byte로 추정해 기본 차단하지 않는다.
- split 시 모든 ID/target/facet/source/안전 고지/미완료 유보를 보존하고 각 part 성공·실패·cost/timing을 정직하게 합산한다. 단일 fact도 provider 입력 한도를 넘으면 원문 기반 부분 답과 해당 범위 incomplete를 낸다. context 오류를 `정보 없음`으로 바꾸지 않는다.
- 기본 gate False, WP-4 관계 상태·출처 검증 유지. 새 모델/큰 context에서도 한 번의 긴 답이 근거를 놓칠 수 있으므로 최종 근거 ID 완전성 검증은 유지한다.

## 검증/보고

- cap 미설정에서 SDK·CLI 모델 호출이 이뤄지는 시험, context 오류 후 분할·재시도, 한 fact 초과·부분 실패, 명시 override, ID/안전/유보 보존 시험. 실물 provider/서버·DB/50·239×3 평가는 실행하지 않는다.
- 관련/전체 pytest, ruff, diff check. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-provider-adaptive-report.md`. 완료 시 `worker_done` 한 번.
