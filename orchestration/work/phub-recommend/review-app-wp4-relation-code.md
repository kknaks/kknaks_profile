# 앱 WP-4 관계 어댑터 읽기 전용 코드 검수

2026-11-02 · 앱 HEAD `078ac99` 대비 현 diff · Hub `backend/app/modules/gold/selected.py` 및 `backend/tests/test_gold_selected.py` 대조. 판정: **FAIL — 기능 활성화 보류**. 기존 테스트 18개는 통과하지만 아래 음성 경로와 실제 질문 재생은 증명하지 않는다.

## 항목별 판정

| 항목 | 판정 | 근거 |
|---|---|---|
| 선택 pair/전역 scope 별도 호출, cursor·more·status·build 처리 | PASS | `relation_adapter.py:59-125`, `case3.py:1881-1909`; Hub의 `selected.py:105-129` 페이지 계약과 대조. 오류·잘림은 `complete=false`이며 64/32 KiB를 전체 종료로 쓰지 않는다. |
| claim·resolved source·대안·전역 ID/원문/source/적용 범위 보존 | WARN | `relation_adapter.py:128-151`, `case3.py:1908-1924`. 원장에는 남지만 Claude 입력은 선택 원문 행뿐이며 resolved의 `value`, `field_status`, `by_direction`, `source_fact_ids`는 빠진다. |
| 다른 pair·조건·owner·비인용 근거 차단 | FAIL | pair 조건 및 source 검사 일부는 있음(`relation_adapter.py:15-56`). 전역 `condition`은 무시하고, 단일 관계 facet이 미완료 scope와 섞인다(아래 F-1/F-3). |
| 대표 R8 5개와 Q139 별도 scope | WARN | `tests/phase8/test_relation_adapter.py:148-159`는 5 ID를 같은 가짜 pair/같은 문장으로 확인한다. QID 질문·실물 pair·방향·source·Claude 답 재생이 아니다. Q139 별도 endpoint는 코드에 있다. |
| WP-1~3/5 안전·부분 답·분할 ID 회귀 | WARN | WP-4는 기본 `walk_coverage_mode=False` 경로를 바꾸지 않는다. 기존 274 통과는 구현자 보고이며 이번 검수는 범위상 전체 실행하지 않았다. `case3.py:1955-2012` 관계 facet 계산과 `:2030` 이후 분할의 결합은 아래 결함에 영향받는다. |

## 활성화 차단 결함

### F-1 — FAIL: 한 target I-07을 자기 쌍으로 확정함

`clinic_chat/cases/case3.py:1865-1870`은 질문에서 단위 시술 하나만 확정되면 `(unit,unit)`을 조회한다. SPEC-005 §5-5의 한 입력 모드는 상대 관계 후보를 찾기 위한 것이고, 동일 ID 두 번의 자기 쌍은 명시적 재시술 질문에 한정된다. 따라서 Q018처럼 상대 시술이 미확정인 일반 관계 질문은 다른 시술 관계를 찾지 않고 자기 쌍 완료 응답으로 `unresolved_absence`를 만들 수 있다(`case3.py:1987-1991`). 재현: I-07, 확정 단위 U5-045 하나, 질문 `U5-045와 다른 시술을 함께 해도 되나요?`; 코드상 요청은 `a=b=U5-045`. 최소 수정: 명시적 같은 시술 재시술일 때만 자기 쌍을 만들고, 상대 미확정은 `unresolved_pair`로 유지하며 관계 후보/명시 대상 resolve frontier를 연다.

### F-2 — FAIL: Q139 전역 scope 미완료를 관계 지원 상태가 가림

`case3.py:1902-1907`은 전역 scope를 별도로 모으지만 `:1987-1991`은 모든 pair/global scope의 완료 여부와 관계없이 **선택된 관계 행이 하나라도 있으면** 단일 `relation` facet을 `received_supported`로 둔다. 예: pair가 R8-0218을 반환하고 Q139 global이 404, error, truncated 또는 build mismatch이면 `relation_complete=false`와 retrieval limit가 기록돼도 facet은 지원 완료가 된다. 전체 `completion`은 일부 경로에서 incomplete로 남지만 facet·Claude payload의 `support_ids`는 전역 메모 누락을 드러내지 못한다. 최소 수정: pair별·Q139 global별 facet을 분리하고 각 scope의 `complete/status`를 지원 판정에 결합한다. Q139 전체 답은 R8 두 행과 별도 전역 fact의 수신·전달을 각각 검증한다.

### F-3 — FAIL: 전역 조건을 검사하지 않음

`relation_adapter.py:43-56`의 `_global_ok`는 `applies_to.scope`와 pair만 비교하고 `applies_to.condition`을 읽지 않는다. `case3.py:1903-1905`도 `global_claims`에 `condition`을 보내지 않는다. 작은 음성 재현: Q139 ID·정상 source·pair·`quotable=true`에 `applies_to.condition="같은 날"`을 넣고 조건 없는 질문으로 `facts(...)`를 호출하면 `quotable=True`가 나온다(`uv run python`으로 확인). Hub 현 Q139 fixture의 condition은 비어 있을 수 있으나 공개 계약은 조건 행을 허용하므로 범용 어댑터가 조건부 사실을 무조건 전달한다. 최소 수정: 전역 조건을 질문에서 확정된 조건과 대조하고, 확인되지 않은 조건 행은 원장에만 남긴다. 조건 인자의 문자열 의미를 Hub 계약과 맞춘 작은 음성 시험을 추가한다.

### F-4 — WARN: resolved 정책값이 Claude 근거로 전달되지 않음

Hub `selected.py:267-277`은 `resolved.value/field_status/by_direction/source_fact_ids`와 연결 source를 별도 낸다. 앱 `relation_adapter.py:128-151`은 source fact만 선택 행으로 바꾸며, `case3.py:1923-1924,2001-2004`의 Claude payload에 resolved 정책값과 source ID의 연결이 없다. 원문 claim으로 답 가능한 경우도 있지만 순서·기간·방향의 resolved 판정 및 대안 구분을 모델이 확인할 수 없다. 최소 수정: 완료된 scope의 resolved 구조를 source ID와 함께 별도 전달하고 원문 fact의 scope를 유지한다. 근거 원문이 없는 값은 의료 사실로 생성하지 않는다.

### F-5 — WARN: prior 방향을 질문에서 판별하지 않음

`case3.py:1887-1896`은 I-08의 `prior.procedure`를 항상 pair 첫 ID `a`로 보낸다. 질문에서 이전 시술이 두 번째 명시 target인 경우 Hub `selected.py:281-283`의 `prior.ok`는 반대 방향으로 계산된다. 최소 수정: prior span을 resolve된 target에 연결하여 해당 ID를 보내고, 불확실하면 prior 판정을 보류한다. 역순 질문 시험이 필요하다.

## 검증과 관문

- 읽기 전용 소수 시험 `uv run pytest -q tests/phase8/test_relation_adapter.py`: **18 passed**. 위 F-3 음성 재현은 현재 `True`를 출력했다. 코드·서버·DB·평가·커밋은 변경하지 않았다.
- 활성화 전 F-1~F-3을 수정하고 F-4/F-5의 범위·방향을 보강한 뒤, 대표 Q018.1/R8-0163, Q064.1/R8-0075, Q139.1/2/R8-0218/0219+전역 메모, Q173.1/R8-0111을 **각 질문의 실제 확정 pair/조건/source/Claude 전달**로 개별 재생해야 한다. 다른 pair·조건·owner, `quotable=false`, global 404/잘림/빌드 불일치에서 부재·지원 완료가 없는지도 확인한다.
- 실제 사용자 서버의 selected/global endpoint와 앱이 같은 build hash인지 확인하고, WORK-012/SPEC-006의 고정 질문·50문항 승격 관문을 별도로 통과해야 한다. 이 검수는 활성화 승인이나 전체 회복 판정이 아니다.
