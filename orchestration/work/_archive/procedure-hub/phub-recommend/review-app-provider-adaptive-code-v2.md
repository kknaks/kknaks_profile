# case3 적응형 입력·관계값 재검수 v2

- 범위: 앱 worktree HEAD `078ac99` 위 현 diff, `walk_coverage_mode=True`. 읽기 전용 코드 검수와 소수 격리 시험만 수행했다.
- 판정: **FAIL 1, WARN 3, PASS 6**. 두 source가 서로 다른 part에 있는 경우의 이전 FAIL은 해소됐으나, 관계 근거가 한 part에 함께 들어간 분할 경로는 정상적인 관계 문장을 거절한다.

| 항목 | 판정 | 근거·재현·최소 수정 |
|---|---|---|
| 단일 호출의 `resolved.value/field_status/by_direction`, `prior.ok/basis` 보존 | PASS | `_relation_lines`가 검증된 값·쌍·방향·조건·모든 source ID를 정본 문장으로 만들고(`case3.py:469-505`), `_source_answer`와 단일 호출 최종 검증·fallback에 들어간다(`:508-535`, `:2423-2456`). 임의 값·ID·방향·조건 문장은 완전 일치 검증에 실패한다. `test_relation_value_lines_require_every_source_and_exact_metadata` PASS. |
| source ID가 서로 다른 part에 분산될 때 전부 성공해야 관계값 노출 | PASS | part별 성공 ID만 `delivery_groups`에 넣고(`case3.py:2351-2354`), 실패 시 facet을 `blocked`/전체를 `incomplete`로 바꾸며(`:2355-2374`), 병합 시 모든 source ID가 전달된 관계만 출력한다(`:2378-2395`). `test_two_source_resolved_survives_separate_provider_parts` 성공·한 source 실패 양쪽 PASS. |
| **한 part가 관계의 모든 source를 가질 때 정상 답 검증** | **FAIL** | part 입력은 해당 `relation_resolved/prior`와 `verified_relation_lines`를 포함하지만(`case3.py:2275-2281`), part 답 검증은 `_supported_answer(answer_part, rows, [part_facet])`로 관계 record를 전달하지 않는다(`:2345`). 따라서 정본 관계 문장만 답하면 `answer_evidence_mismatch`가 된다. 원문 fact 문장과 정본 관계 문장을 함께 답하면 각 source ID가 두 번 인용되어 `answer_id_mismatch`가 된다(`:2334-2343`). 격리 재현: 두 source `R1/R2`의 정본 resolved 문장은 `_supported_answer(line, facts, [facet], [resolved]) == True`, 현 part 호출 형태의 `_supported_answer(line, facts, [facet]) == False`; `_source_answer`의 인용 ID는 `['R1','R2','R1','R2']`. 이는 관계 facet을 `blocked/incomplete`로 잘못 바꾸고 관계값을 유보한다. 최소 수정: part 검증에 그 part의 `relation_resolved/prior`를 전달하고, ID 검사는 중복 횟수가 아니라 허용된 문장별 citation 집합·정본 문장의 완전 일치로 수행한다. 모든 source가 한 part에 있고 다른 facet 때문에 분할된 정상 답, relation-only 답, 원문+relation 답, 위조 값·ID·방향·조건 음성 시험을 추가한다. |
| 기본 cap 미설정 SDK·CLI 호출 및 context 재시도 | PASS | cap 기본값은 `None`(`config.py:74`, `case3.py:434-437`); 완료 시 실제 provider 호출(`case3.py:2182-2218`), SDK count preflight와 CLI context 오류 후 분할 재시도(`:2185-2214`, `:2284-2323`)를 확인했다. 관련 25개 선택 시험 PASS. |
| 단일 fact 초과, part 실패, ID·부분 답·안전 flags | PASS | 단일 fact 제한은 실패 범위로 남기고(`case3.py:2292-2297`), 실패 facet은 blocked, 지원된 facet은 원문 답과 flags를 유지한다(`:2355-2397`). 관계 source 한 part 실패 시험과 기존 음성 시험 PASS. 위 FAIL의 정상 관계 답 거절은 이 항목의 예외다. |
| retrieval cap과 탐색 분리 | PASS | 답변 cap은 수집 이후 `coverage_run`의 payload 생성 시점에만 읽는다(`case3.py:2168`). 생성 입력 제한이 frontier 탐색 종료 조건으로 사용되지 않는다. |
| 비용 합산 | PASS | SDK stage 비용은 반복 `claude`를 합산(`loop.py:209-215`), CLI 실패 전체 호출 및 part 비용은 `cli_parts` 합산(`case3.py:1602-1611`). 선택 시험에서 context 재시도·분할 비용 합산 PASS. |
| 실물 CLI context 오류 문구 | WARN | `_context_failure`는 고정 문구 목록(`case3.py:444-450`). 다른 실물 오류 문구는 재시도 분류에서 빠질 수 있다. 실물 오류 코드/문구 수집 뒤 판별기를 보강한다. |
| CLI 병합 timing 부가 칸 | WARN | 전체 stage/elapsed에 마지막 CLI 호출의 boot/TTFT 부가 칸을 덮어쓴다(`case3.py:1604-1608`). 실물 보고에서 시도별 timing과 최종 case timing을 함께 대조한다. |
| 분할·미완료 답의 `answer_citations` trace | WARN | `answer_citations`는 단일 호출 끝에서만 기록(`case3.py:2459-2464`). 분할과 원문 부분 답은 각각 `:2402`, `:2413`에서 먼저 반환한다. 최종 답 본문에는 ID가 남지만 이 trace 칸은 빠진다. 최소 수정: 최종 답 확정 뒤 모든 반환 경로에서 동일한 citation 작성 함수를 호출하고, 분할 성공·일부 실패·원문 fallback의 최종 답 ID와 trace를 대조한다. |

## 격리 검증

- `uv run pytest tests/phase8/test_relation_adapter.py -q` → **34 passed**.
- `uv run pytest tests/phase8/test_case3_walk.py -q -k 'coverage_unconfigured or coverage_sdk_token_preflight or coverage_cli_single_fact or coverage_split or coverage_input_limit'` → **25 passed, 62 deselected**.
- `uv run python` 소수 단위 재현으로 정상 관계 문장의 split 검증 거절과 원문+관계 문장의 중복 ID 판정을 확인했다. 서버·DB·실물 provider·평가는 실행하지 않았다.

## 활성화 전 실물 관문

위 FAIL을 고치고 한 part 안의 완전 관계·여러 part에 흩어진 관계·한 source 실패를 각각 재검증한다. 앱/Hub 동일 build hash와 WORK-011 공개 계약의 `pair_scope.complete`, claim·대안별 source/`applies_to`, 방향, Q139 `global_claims/scope_complete`를 실물에서 확인한다. CLI 실제 context 오류 문구, SDK count/생성 일치, 단일 fact 거절, 일부 part 실패, 시도별·최종 비용/시간, 안전 flags와 미완료 유보를 고정 50 case3에서 검증한다. 239×3 평가는 고정 50 결과와 사용자 승격 판단 이후 별도 관문이다.
