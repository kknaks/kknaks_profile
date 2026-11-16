# case3 provider 입력 적응형 코드 검수

- 범위: 앱 worktree HEAD `078ac99` 위 현재 diff, `walk_coverage_mode=True` 경로. 읽기 전용 코드 검수와 소수 격리 시험만 수행했다.
- 판정: **FAIL 1, WARN 2, PASS 6**. 관계 `resolved`/`prior` 값의 최종 답변 보존은 활성화 전 수정이 필요하다.

| 항목 | 판정 | 근거 |
|---|---|---|
| cap 미설정 SDK·CLI 최종 호출 | PASS | 완료된 수집에서 SDK는 `count_tokens` 뒤 실제 `_answer`, CLI는 실제 `_answer`를 호출한다 (`case3.py:2135-2173`). 격리 시험 `test_coverage_unconfigured_sdk_counts_and_calls`, `test_coverage_unconfigured_cli_context_retry_keeps_evidence` 통과. 미완료 수집은 원문 부분 답 경로(`2353-2358`)로 모델을 호출하지 않는다. |
| SDK token preflight | PASS | system+user 구조를 `messages.count_tokens`에 전달하고 기본 Sonnet 5.5의 1M 창에서 8K를 남긴다 (`453-464`, `2136-2145`). count 실패 시 생성 호출로 간다. 공식 문서의 [Sonnet 5.5 1M context](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)와 [Messages token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)에 맞는다. |
| CLI 실제 context 오류와 이분 재시도 | PASS | 알려진 context 오류를 감지해 전체 입력 실패 후 facet/ID 묶음으로 재시도하고, part 오류에서 다시 이분한다 (`444-450`, `2163-2170`, `2265-2273`). 단일 fact 거절은 `blocked/incomplete`와 유보로 남긴다 (`2273-2282`, `2305-2331`). 관련 격리 시험 통과. |
| 명시 override·한 fact 초과·일부 part 실패 | PASS | override는 생성 입력에만 쓰며 단일 fact 초과와 part 실패는 `context_limit` 또는 `tool_error`, `blocked/incomplete`로 처리한다 (`2175-2176`, `2235-2247`, `2305-2327`). 지원된 다른 facet의 원문 답과 안전 flags는 유지한다 (`2328-2347`). |
| retrieval frontier와 입력 cap 분리 | PASS | `coverage_run`의 frontier 수집은 `walk_input_max_bytes`를 참조하지 않고 종료 뒤 `2125`에서 생성 cap을 읽는다. page/neighbor 수집은 `1688-1870`에 있다. 따라서 생성 입력 cap 자체가 탐색을 조기 종료하지 않는다. |
| ID/target/facet/source/안전·유보 | PASS | part에 선택 fact 원문과 source/scope, target, facet, 미완료 목록, flags를 넣는다 (`2217-2233`). ID와 원문·target 대조 후 최종 원문 답을 검증한다 (`2284-2304`, `2331-2343`). 관련 음성 시험 25개 통과. |
| 관계 `resolved`/`prior`의 최종 답 보존 | **FAIL** | 관계 값은 payload에 만들어지지만 (`2074-2103`), 분할 시 한 묶음에 모든 `source_fact_ids`가 들어갈 때만 전달한다 (`2191-2195`, `2227-2230`). 두 근거가 다른 묶음으로 갈라지면 어떤 part에도 resolved 값이 없다. 더 직접적으로, 성공한 part의 생성 답은 읽지 않고 `_source_answer`로 다시 만들며 (`2301-2331`), 이 함수는 fact 원문만 출력한다 (`467-488`). 단일 호출에서도 resolved 값을 덧붙인 답은 원문 한 줄과 완전 일치를 요구하는 `_supported_answer`에 거절되어 원문 fallback으로 바뀐다 (`491-511`, `2375-2400`). 최소 재현: fact `R1`의 원문이 `A와 B의 간격 근거`, resolved.value가 `14일`일 때 `_source_answer` 출력에는 `14일`이 없고, 해당 값을 인용해 덧붙인 답은 `_supported_answer`가 `False`다. 실제 격리 명령으로 확인했다. 최소 수정: resolved/prior를 모든 필수 근거 ID와 함께 동일 part에 묶거나 검증된 관계 값의 별도 병합 레코드를 만들고, 최종 답 검증기와 source fallback이 그 값·방향·source ID를 안전하게 표현하도록 한다. 두 source가 분리되는 관계 시험과 단일 호출의 resolved 값 보존 시험을 추가한다. |
| CLI context 오류 문구 확장성 | WARN | `_context_failure`는 고정 문자열 10개에 의존한다 (`444-450`). 다른 실물 오류 문구는 context 거절로 분류되지 않아 이분 재시도에 들어가지 않는다. 현재 알려진 문구 격리 시험만 PASS다. 실물 CLI의 오류 코드/문구를 수집해 판별기를 보강한다. |
| 비용·시간 원장 | WARN | SDK `case_cost`는 반복 `claude` stage를 합산한다 (`loop.py:208-217`). CLI는 실패한 전체 호출과 part 결과를 `cli_parts`로 합산한다 (`case3.py:2165-2166`, `2257-2264`, `1561-1573`). 다만 CLI 병합 timing은 마지막 호출의 boot/TTFT 부가 칸을 쓰고 (`1564-1567`) 전체 합산 stage/elapsed와 의미가 다를 수 있다. 실물 보고에서 각 시도 timing과 최종 case timing을 함께 확인한다. |

## 수행한 격리 검증

`uv run pytest tests/phase8/test_case3_walk.py -q -k 'coverage_unconfigured or coverage_sdk_token_preflight or coverage_cli_single_fact or coverage_split or coverage_input_limit'` → **25 passed, 62 deselected**. 별도 소수 단위 재현에서 `_source_answer`에 `resolved.value=14일`이 나타나지 않았고, resolved 값을 추가한 문장을 `_supported_answer`가 거절했다. 서버·DB·provider 실물 호출과 평가는 수행하지 않았다.

## 활성화 전 실물 관문

관계 값 보존 FAIL을 고치고, 앱/Hub 동일 build hash와 WORK-011 관계 공개 계약의 `pair_scope.complete`, claim·대안별 source/`applies_to`, 방향, Q139 global 범위를 실물로 확인한다. CLI 실제 context 오류 문구, SDK count/생성 일치, 단일 fact 거절, 일부 part 실패, 누적 비용/시간, 안전 flags 및 미완료 유보를 고정 50 case3 한 번에서 확인한다. 239×3 평가는 고정 50 결과와 사용자 승격 판단 이후 별도 관문이다.
