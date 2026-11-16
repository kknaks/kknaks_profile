# case3 분할 part 6차 코드 검수

**종합 판정: FAIL — coverage 수락·활성화 보류.** 앱 HEAD `078ac99` 대비 현재 미커밋 diff를 SPEC-006 0.3.10 §3-4-1-5와 WORK-012 WP-1~3/5에 대조했다. 5차의 잘못된 ID·owner·target_key·원문을 가진 정상 종료 part가 완료되는 결함은 수정됐으나, **묶음 내 일부 ID를 응답에서 누락해도 완료로 세는 새 결함**을 재현했다. 실물 provider·Hub·QID 재생, 서버·DB·평가는 실행하지 않았다.

| 항목 | 판정 | 파일:줄·근거·최소 수정안 |
|---|---|---|
| 5차 FAIL: 잘못된 ID·owner·target_key·원문 | **PASS** | `clinic_chat/cases/case3.py:2022–2031`에서 `_supported_answer` 실패 시 `answer_evidence_mismatch`와 `failed`로 남기고 성공 집합/전달 묶음에 넣지 않는다. `tests/phase8/test_case3_walk.py:1072–1129`의 SDK·CLI 각 5종 음성 시험 통과. |
| **묶음별 결과 ID 완전성** | **FAIL** | `case3.py:436–456`은 응답에 **등장한** 인용만 검사하며 제공한 모든 `rows`/`support_ids`가 답에 있는지 확인하지 않는다. 직접 재현: 같은 facet의 `F1,F2`를 전달하고 `F1`의 정확한 원문 한 줄만 답하면 `_supported_answer(...) == True`. `case3.py:2022–2031`은 이 part를 `completed`로 세고 두 ID 모두 `delivery_groups`에 기록한다. 최종 답은 `2052–2064`에서 원장 원문으로 다시 합성되어 두 줄을 담을 수 있으므로 허위 문장이 노출되는 형태는 아니지만, Claude가 처리하지 않은 `F2`도 처리 완료로 기록되어 §3-4-1-5의 묶음별 결과 ID 대조·분할 묶음 유실 검증을 충족하지 못한다. 최소 수정: part의 인용 ID 집합을 해당 chunk의 기대 ID 집합과 대조하고 누락·추가 시 실패/blocked/incomplete로 처리하거나, 누락 ID만 별도 재처리해 성공을 확인한다. 두 ID 중 하나만 인용한 SDK·CLI 시험을 추가한다. |
| 실패 part, 성공 part 부분 답·유보·안전 flags | **PASS** | `case3.py:2013–2027,2032–2052`에서 실패 facet은 blocked/incomplete, 성공 facet은 원문 답으로 남는다. `2040,2052`에서 미완료 범위 유보와 전체 `must_show_flags`가 답에 포함된다. `tests/phase8/test_case3_walk.py:1117–1129,1155–1182` 검증 통과. |
| 최종 trace/answer_validation | **WARN** | 잘못된 ID 등은 `split_part_results=failed`, `split_failed`, `stop=tool_error`, `answer_validation=partial_source_contract`로 기록된다(`case3.py:2022–2064`). 다만 ID 일부 누락 경우 `delivery_groups`에 실제 미확인 ID까지 들어가고 `passed_source_contract`가 가능하다. 또한 처리 오류 facet의 `unread`도 `context_limit`으로 고정된다(`2041–2045`); 실패 사유에 맞게 기록하면 trace가 정확해진다. |
| 앞 차수 PASS 회귀 | **PASS(격리 시험), WARN(실문항)** | split 13개, claim/source/repeated/shared 6개 단위 시험과 `git diff --check 078ac99` 통과. 같은 section 두 대상, 반복·전치·공통 facet, CLI 비용/timing의 기존 격리 경로는 유지된다. 실제 QID·provider 한도·Hub source/cut 계약은 미검증이다. |
| 관계·WP-4 | **WARN** | `case3.py:1914–1916`은 관계를 지원 완료로 꾸미지 않고 blocked로 둔다. 프로필 `WORK-011.md:5,23,62`는 아직 todo이고 공개 계약·§6-9 PASS/인계가 없다. **WP-4 발주 불가.** |

**재현·시험:** `uv run pytest tests/phase8/test_case3_walk.py -q -k 'split_'` → 13 passed; `-k 'claim_validator or source_answer or repeated_preposed or shared_trailing'` → 6 passed; `git diff --check 078ac99` → 통과. 직접 호출은 `facts=[F1,F2]`, 단일 `received_supported` facet의 `support_ids=[F1,F2]`, 답 `target:1 node:1 recovery: 첫째 원문 [[F1]]`에 대해 `_supported_answer=True`를 반환했다.

**Coverage 활성화 전 관문:** part 인용 ID 완전성 수정과 SDK·CLI 음성 시험, 실제 provider 입력 한도 설정, Hub page/source/cut 및 WORK-011 관계 공개 계약 확인, 요구 QID 개별·고정 50 재생과 정확성·안전·TTFT p50/p90·blocked 분포 확인. `walk_coverage_mode=False` 기본값은 현 경로 노출을 막지만 수락 근거는 아니다.
