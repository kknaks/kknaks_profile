# 앱 WP-4 관계 어댑터 3차 코드 검수

2026-11-02 · 읽기 전용 · 앱 HEAD `078ac99` 대비 현재 미커밋 diff와 Hub selected 코어, WORK-011 공개 계약 인계, WORK-012, SPEC-006 0.3.10 §3-4-1-5 대조. **판정: PASS — WP-4 관계 어댑터 코드는 수락 가능. 기능 활성화와 실물 평가 관문은 미완료.** 이번 검수에서 재현 가능한 새 결함은 찾지 못했다.

| 항목 | 판정 | 근거·재현·최소 수정안 |
|---|---|---|
| F-1 자기 쌍 오판 | **PASS** | `clinic_chat/cases/case3.py:399-408,1900-1904`는 `다시 받` 단독 및 `다른/타/별도 시술` 상대를 자기 쌍으로 만들지 않는다. `tests/phase8/test_relation_adapter.py:152-163,260-292`는 `이마 보톡스 후 다른 시술을 다시 받아도 되나요?`에서 selected pair 호출 0회, `unresolved_pair/incomplete`를 확인한다. 추가 수정 없음. |
| F-2 pair/global 분리 | **PASS** | `case3.py:1935-1954,2034-2049`는 pair와 global scope별 완료·지원 ID·facet 상태를 분리한다. `test_relation_adapter.py:295-336`의 전역 오류/잘림/build 불일치에서 pair 지원은 유지하고 global은 `blocked/incomplete`다. 추가 수정 없음. |
| F-3 복수 전역 조건 | **PASS** | `case3.py:420-427,1941-1945`는 `같은 날`과 `같은 부위`를 함께 보존하고, `relation_adapter.py:43-52`는 row의 조건을 확정 집합과 대조한다. `case3.py:2037-2049`는 선별 실패 row만 있으면 완료 scope라도 `blocked`로 둔다. `test_relation_adapter.py:126-137,339-392`의 Q139형 문장에서 `같은 날` row가 포함되고 Claude 전달 ID에 남으며, `unresolved_condition`이면 `blocked/incomplete`다. 추가 수정 없음. |
| F-4 resolved/source ID 결속 | **PASS** | `relation_adapter.py:156-166`, `case3.py:2057-2062,2114-2118,2165-2169`는 완료 scope의 source fact ID 전체가 선택된 경우에만 resolved를 전달한다. 분할 payload에서도 같은 source ID가 있는 조각에만 넣는다. `test_relation_adapter.py:140-149,201-241` 확인. 추가 수정 없음. |
| F-5 역방향 prior | **PASS** | `case3.py:407-417,1925-1934`가 이전 시술 span을 묶어 두 번째 target을 `prior.procedure`로 요청한다. Hub `backend/app/modules/gold/selected.py:284-286`의 `prior.ok/basis`는 `relation_adapter.py:108-117,169-186`에서 페이지 간 일치와 완료·source ID 조건을 거쳐 `case3.py:2063-2080`의 `relation_prior`/facet에 들어간다. 분할 입력은 `case3.py:2133-2142,2162-2169`에서 같은 source ID의 조각에만 포함한다. `test_relation_adapter.py:395-452`는 두 번째 target의 14일 역방향 요청, `ok=False`, source ID, Claude payload를 확인한다. 추가 수정 없음. |

## 범위와 남은 관문

- 실행한 소수 단위 시험: `uv run pytest -q tests/phase8/test_relation_adapter.py -k 'one_unit_other_procedure or q139_multiple_conditions or prior_request_uses_second_target or prior_requires_complete_source_bound_resolved or global_failure_stays_separate'` → **10 passed**. `git diff --check 078ac99` → PASS. 서버·DB·평가·전체 테스트는 실행하지 않았다.
- F-5 시험은 fake Claude의 입력과 결과의 ID 보존을 확인한다. `tests/phase8/test_relation_adapter.py:188-198`의 대표 R8 5 ID 시험은 동일 가짜 pair/문장을 순회하므로 실제 Q018.1/R8-0163, Q064.1/R8-0075, Q139.1/2/R8-0218/0219 및 전역 메모, Q173.1/R8-0111의 개별 의미·답변 정확성 증거는 아니다. 이 한계는 코드 FAIL이 아니라 활성화 전 재생 관문이다.
- 기능 활성화 전에 WORK-011 인계의 실제 selected/global endpoint와 앱 Gold build hash 일치를 확인하고, 위 실제 QID별 수집→선별→Claude 전달→답 재생을 검증해야 한다. 이어 WORK-012의 고정 50문항×1 평가와 사용자 승격 판단이 필요하다. 인계 당시 사용자 서버 새 경로는 404였으므로 fixture 통과를 실물 서버 성공으로 읽지 않는다.
