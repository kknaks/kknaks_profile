# 앱 WP-4 관계 어댑터 재검수 v2

2026-11-02 · 읽기 전용 · 앱 HEAD `078ac99` 대비 현재 diff, Hub selected 코어/fixture 및 WORK-011/012, SPEC-006 0.3.10 대조. **판정: FAIL — WP-4 코드 수락 및 기능 활성화 보류.** 수정 보고의 핵심 방향은 반영됐으나 F-1/F-3 음성 경로가 남고 I-08 prior 판정은 Claude까지 전달되지 않는다.

| 항목 | 판정 | 근거·최소 수정 |
|---|---|---|
| F-1 단일 target 자기 쌍 | **FAIL** | `clinic_chat/cases/case3.py:403-404,1891-1896`: `_explicit_self_pair`가 `다시 받`만으로 true다. I-07, resolve가 `이마 보톡스` 한 단위만 확정, 질문 `이마 보톡스 후 다른 시술을 다시 받아도 되나요?`이면 상대가 미확정인데 `(이마 보톡스, 이마 보톡스)`를 조회한다. 단위 재현 `_explicit_self_pair(question) == True`. 자기 재시술 표현을 *확정 단위와 같은 시술*에 연결하고, `다른 시술` 등 미확정 상대가 있으면 `unresolved_pair`로 남겨야 한다. 기존 `test_one_unit_other_procedure_does_not_query_self_pair`는 `다시` 없는 문장만 확인한다. |
| F-2 pair/global 분리 | **PASS** | `case3.py:1927-1946,2020-2038`: scope별 완료와 지원 ID를 따로 계산한다. global 오류/잘림/빌드 불일치 시 global facet은 `blocked`, 전체 `incomplete`다. `tests/phase8/test_relation_adapter.py:283-324`가 세 경로를 확인한다. |
| F-3 global 조건 | **FAIL** | `relation_adapter.py:43-52`의 정확한 조건 비교 자체는 맞다. 다만 `case3.py:420-424`는 질문에 `같은 날`과 `같은 부위`가 모두 있으면 단일 값 대신 `None`을 낸다. `서브시전과 니들RF를 같은 날 같은 부위에 받아도 되나요?`와 Q139 row `condition="같은 날"`의 작은 재현은 `_global_condition=None`, `facts(...)[0].quotable=False`였다. scope가 완료되면 `case3.py:2029-2036`은 실제 적용 가능한 row가 있는데도 global facet을 `unresolved_absence`로 둔다. 질문에서 확정된 조건 집합을 보존해 row별로 일치 여부를 검사하고, 조건 선별 실패를 완료 부재로 바꾸지 말아야 한다. |
| F-4 resolved 값/source ID | **PASS** | `relation_adapter.py:145-155`, `case3.py:2041-2051,2088-2092,2131-2134`: 완료 scope의 `source_fact_ids`가 모두 독립 선택돼야 resolved 값이 들어가며, 분할 payload도 해당 source를 같은 조각에 둘 때만 넣는다. `tests/phase8/test_relation_adapter.py:137-146,194-234`에서 확인. |
| F-5 prior 역방향 | **WARN** | `case3.py:407-417,1917-1926`은 이전 시술 span을 바인딩해 역방향 `prior.procedure`를 보내며, `tests/phase8/test_relation_adapter.py:327-360`가 요청을 확인한다. 그러나 Hub `backend/app/modules/gold/selected.py:281-283`의 `prior:{ok,basis}` 응답은 `relation_adapter.collect`에서 `pages`에만 남고 `case3.py:1939-1942,2051-2055`의 Claude payload 및 relation facet에는 없다. 즉 모델이 질문의 기간·방향에 대한 Hub prior 판정을 근거로 답할 수 없다. 완료된 pair scope의 `prior.ok/basis`를 source가 입증하는 범위와 함께 전달하고 역방향 답 재생을 추가해야 한다. |

## 범위와 관문

- `uv run pytest -q tests/phase8/test_relation_adapter.py`: **26 passed**. `git diff --check 078ac99`: 통과. F-1/F-3 재현은 읽기 전용 `uv run python -c`로 각각 `True`, `None/False` 확인. 서버·DB·평가 실행, 앱 코드 변경 없음.
- 현 시험의 대표 R8 5 ID는 `tests/phase8/test_relation_adapter.py:181-191`에서 동일 가짜 pair/문장으로 순회한다. Q018.1/R8-0163, Q064.1/R8-0075, Q139.1/2/R8-0218/0219+전역 메모, Q173.1/R8-0111의 실제 확정 pair·조건·source·Claude 전달/답 검증은 아직 없다.
- 활성화 전 F-1/F-3을 수정하고 F-5 prior 판정 전달을 결정·검증해야 한다. 이어 사용자 서버 selected/global endpoint와 앱 build hash 일치, 각 QID의 수집→선별→전달→답 재생, WORK-012의 고정 50문항 승격 관문이 필요하다. WORK-011 인계 당시 사용자 서버 경로는 404였으므로 격리 fixture 성공을 실서버 성공으로 간주할 수 없다.
