# Q002 동일 이웃 다중 관계 누락 수정

## 대상·근거

- 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 현재 미커밋 구현을 이어서 수정한다. 기존 변경을 보존한다.
- 정본: 이 작업의 `SPEC-006.md` §3-4-1-5와 `WORK-012.md` WP-7, `reference/2026-10-30-hub-evals/build-out/q002-live-gate-report.md`.
- Q002는 네 역할 fact 중 `treats:0152#evidence#row.evidence.role`만 최종 Claude 입력에서 빠진다. Hub `expand(neighbor_kinds)`가 이웃 ID `U5-082`를 한 번만 내보내면서 `treats:0013`을 대표 edge로 택한 것이 원인이다. `treats:0152`는 Gold에 있고 fact 원문도 이미 수신됐다. 앱의 `branch_relations`에 그 edge ID가 없어서 소유 관계 검증에서 제외됐다.

## 작업

1. Hub 읽기 전용 `recommend`가 Q002 anchor에 대해 `treats:0151~0154` 전부를 `cards[].why[].edge`로 내는지 먼저 실물 또는 동일 Gold fixture로 검증한다. `include_conditional`, site/cc 필터, 카드 `limit=200`과 `more_cards` 경계를 확인한다. 결과를 보고서에 명시한다.
2. 검증되면 앱 I-01 직접 추천 갈래의 관계 수집에 `recommend`의 `why`를 사용해 **같은 unit으로 향하는 모든 직접 treats edge**를 등록한다. 기존 `expand`는 노드/후속 fact 탐색에 유지해도 된다. `why`의 edge/from/role과 anchor·unit·build를 교차 검증한다. `more_cards`가 있으면 완전한 수집으로 간주하지 말고 명시적인 불완전 상태로 처리한다. 단순히 fact 소유 검증을 느슨하게 풀지 않는다.
3. `recommend`가 해당 Q002 관계를 모두 제공하지 못한다면 앱에 추측성 우회 구현을 하지 말고, 필요한 Hub API 계약과 근거를 보고하고 `worker_done`한다. 다른 고민의 edge나 위조 role fact를 현재 anchor에 귀속시키면 안 된다.
4. 다중 edge가 같은 unit에 연결된 fixture, Q002 네 역할 선택, 타 anchor/다른 branch 관계 배제, `more_cards` 처리 테스트를 추가한다. 전체 앱 테스트·Ruff·diff check를 실행한다.

## 경계·보고

- 앱 코드와 직접 관련 테스트만 편집한다. Hub 코드·DB, 사용자 서버/포트/컨테이너는 건드리지 않는다. 커밋/푸시/PR, 50문항 batch 금지.
- 격리 Hub 18015를 사용할 수 있으면 Q002 단독 실문항으로 네 역할이 Claude 입력까지 전달되는지 확인한다. 최종 답이 실패하면 성공이라고 보고하지 말고 정확한 단계와 이유를 기록한다.
- 결과를 `reference/2026-10-30-hub-evals/build-out/q002-multi-edge-report.md`에 기록하고 Orca `worker_done`으로 보고한다.
