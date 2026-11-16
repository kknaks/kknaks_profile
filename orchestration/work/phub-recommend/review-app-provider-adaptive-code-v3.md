# case3 적응형 분할 관계 검증 재검수 v3

- 범위: 앱 worktree HEAD `078ac99` 위 현 diff, `walk_coverage_mode=True`. 읽기 전용 코드 검수와 격리 단위 시험만 수행했다.
- 판정: **FAIL 0, WARN 2, PASS 6**. v2의 한 part 완전 관계 거절과 citation trace 누락은 해소됐다. 새 결함은 재현되지 않았다.

| 항목 | 판정 | 근거·재현·최소 수정 |
|---|---|---|
| 한 part의 완전 관계: 원문+relation 및 relation-only | PASS | part에 완전한 `relation_resolved/prior`와 정본 문장을 싣고(`case3.py:2284-2295`), ID는 집합으로 대조한 뒤 그 part 관계 record로 정확한 문장을 검증한다(`:2345-2360`). `test_two_source_resolved_survives_provider_parts`의 `together` × 두 답 형태에서 정상 성공하며, `_supported_answer` 단위 시험도 양쪽을 허용한다(`tests/phase8/test_relation_adapter.py:154-185,285-353`). 중복된 동일 문장은 거절한다(`case3.py:534-536`). |
| 서로 다른 part 및 단일 호출 관계 | PASS | 관계 문장은 모든 source ID가 최종 성공 `delivery_groups`에 있을 때만 합성한다(`case3.py:2395-2415`). 서로 다른 part의 성공과 단일 호출에서 정본 resolved 문장을 확인했다(`tests/phase8/test_relation_adapter.py:250-283,285-353`). |
| 일부 source 실패의 유보 | PASS | 실패한 part의 facet은 `blocked`, 전체는 `incomplete`가 되고 관계값을 최종 답에서 제외한다(`case3.py:2369-2403`). `separate/together` × 두 답 형태 × source 실패 시험에서 `[14, 28]` 관계값 비노출을 확인했다(`tests/phase8/test_relation_adapter.py:285-353`). |
| 위조 값·ID·쌍·방향·조건 차단 | PASS | 관계 정본은 pair, value, field_status, by_direction, prior ok/basis, 각 source의 applies_to를 포함하고 원문/source와 대조한다(`case3.py:467-505`). `_supported_answer`는 정본 문장 완전 일치만 허용한다(`:527-555`). 값·ID·쌍·방향 음성 시험(`tests/phase8/test_relation_adapter.py:154-190`)과 source 조건의 정본 직렬화/완전 일치 검토에서 우회가 재현되지 않았다. |
| 최종 답 `answer_citations` | PASS | 공통 기록 함수가 최종 답의 실제 인용 순서와 반복을 기록한다(`case3.py:557-566`). 분할 성공·일부 실패(`:2412-2415`), 부분 원문 fallback(`:2418-2426`), 단일 호출 검증/fallback(`:2430-2475`), 인용 없는 조기 반환(`:2164-2179`)을 확인했다. 시험에서 각 최종 `answer`의 인용 ID 배열과 trace 배열이 같다(`tests/phase8/test_case3_walk.py:1081-1094,1120-1173,1210-1229`; `tests/phase8/test_relation_adapter.py:340-353`). |
| cap 기본 미설정 SDK/CLI, context 재시도, 비용, 안전 flags·유보 | PASS | 기본 cap `None`(`config.py:74`), 실제 호출·SDK count·CLI context 분할 재시도(`case3.py:2182-2328`), SDK 반복 stage와 CLI parts 비용 합산(`loop.py:209-215`, `case3.py:1614-1624`), 실패 part의 flags·유보(`case3.py:2369-2415`)를 확인했다. 관련 격리 시험 포함 **128 passed**. |
| 실제 CLI context 오류 문구 | WARN | 판별기가 고정 문자열 목록이다(`case3.py:444-451`). 실물 provider 오류 코드/문구가 아직 관측되지 않아 다른 형식의 거절을 분할 재시도로 분류하는지 미확인이다. 실제 오류를 채집해 판별기와 회귀 fixture를 맞춘다. |
| CLI 병합 timing 부가 칸 | WARN | 전체 stage/elapsed는 timer를 쓰지만 부가 timing 칸은 마지막 CLI part 값을 결합한다(`case3.py:1614-1624`). 실물에서 시도별 timing과 최종 case timing을 대조하고 의미가 다른 부가 칸은 시도별 trace로 분리한다. |

## 검증

- `uv run pytest tests/phase8/test_relation_adapter.py tests/phase8/test_case3_walk.py -q` → **128 passed**.
- `git diff --check` 통과. 코드·서버·DB·평가 변경/실행은 하지 않았다.

## 활성화 전 실물 관문

앱과 Hub의 동일 build hash 및 WORK-011 공개 계약의 `pair_scope.complete`, claim/대안별 source·`applies_to`, 방향, Q139 `global_claims/scope_complete`를 실물에서 확인한다. 실제 SDK count와 생성 입력, CLI context 오류 문구 및 분할 재시도, 단일 fact 제한, 관계 source 성공·일부 실패, 시도별/최종 비용·시간, 안전 flags와 미완료 유보를 고정 50 case3에서 확인한다. 239×3 평가는 고정 50 결과와 사용자 승격 판단 이후 별도 관문이다.
