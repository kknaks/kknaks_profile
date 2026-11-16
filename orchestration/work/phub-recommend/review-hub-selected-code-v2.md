# Hub 선택 관계·전역 메모 코드 재검수

**판정: FAIL — 앱 WP-4 관계 어댑터 인계 보류.** 기준 HEAD `2edc190`의 현재 미커밋 diff, SPEC-005 0.3.9 §5-5·§6-9, WORK-011, SPEC-006 0.3.10 §3-4-1-5. 실물 입력을 `tests.gold_support.real_graph()`로 메모리에만 빌드해 소수 호출을 확인했다. build hash는 `567677edfe7123e9`다. 서버·DB·평가·코드는 변경하거나 실행하지 않았다. 지시된 `/Users/marin/AGENTS.md`는 이 환경에 없어 읽을 수 없었다.

## 기존 FAIL 재판정

1. **PASS — 호출별 초과 복구.** `backend/app/modules/gold/selected.py:23-34,57-96,138-154,237-274`는 정렬된 item에 offset cursor를 사용하고 build hash와 정규화 요청 digest로 이어 읽기를 묶는다. `next_cursor`/`more`/미완료 상태가 있어 64/32 KiB 초과를 다음 호출에서 회수한다. `backend/tests/test_gold_selected.py:92-135`는 전역 source/text 전체와 선택 관계 resolved/claim/대안의 재조립·요청 변경 거부를 검증한다. 실물 `scope:all` 550행을 9페이지 `[85,83,51,52,52,36,48,75,68]`로 회수했고 각 응답 크기는 `[32579,32432,31671,32594,32706,24726,32568,32629,27061]` B였다. 최종 `more=0, scope_complete=true`; 소스 시험의 550행 ID/원문/source 비교와 일치한다. build가 다른 cursor는 prefix 검증에서 거부된다. 남는 제한: 이 검수는 다른 build를 실제 생성해 cursor를 재사용하는 시험은 하지 않았고, 64 KiB 초과 실물 pair 대신 축소 cap 10,000B 시험을 검토했다.

2. **FAIL — Q139 combo anchor의 적용 쌍 과잉 생성.** `backend/app/modules/gold/selected.py:219-234,264-276`은 실물 `scope:all#evidence#step8_notes[26]`의 `attached_to=[combo:RC-OP-Acne-중등도]`, `source.meta.where`, combo 이름, `sequence_text_8` 원문 일치를 확인한다. 이는 anchor 동일성을 뒷받침한다. 그러나 `silver.components` 네 묶음의 모든 교차 쌍 23개를 `pairs`로 생성한다. 원문은 “서브시전 → 4주 후 프락셔널/니들RF → PRP 동시 도포”인데 실제 호출은 서브시전 `U5-045`/PRP `U5-020`도 `quotable=true, scope_complete=true`다. 요구한 `U5-110/U5-045`, `U5-110/U5-020` 양방향은 참이고 무관 `U5-001/U5-082`는 거짓이지만, 시험 `backend/tests/test_gold_selected.py:138-153`은 조합 **안의 무관 쌍**을 놓친다. pair 없는 호출도 `quotable=true`라 확정 쌍 일치 없이 인용할 여지가 있다. **최소 수정:** 원문 순서·동시성 구문과 component 대응으로 지원되는 관계만 명시적으로 매핑하고, 확정 pair 없는 응답은 pair별 인용 불가로 둔다. 조합 내부의 비인접/비지원 쌍을 음성 시험에 추가한다.

3. **FAIL — R8-0144 조건의 키 일치가 검증되지 않는다.** `backend/app/modules/gold/selected.py:116-135,190-209`은 기본 `include_conditional=false`와 조건 없는 `true`에서 인용을 막고, `source_a.qualifier/default_apply`, 방향을 반환한다. 실물 `U5-023/U5-034`에서 `include_conditional=true, sub_condition={"깊이":"심부 · 페놀"}`는 인용 가능하다. 그러나 같은 값의 `{"세션":"심부 · 페놀"}`도 인용 가능하다. `:127,133`이 조건 값을 임의 key의 `.values()`와만 비교하기 때문이다. `backend/tests/test_gold_selected.py:156-173`은 true/false와 실제 키는 검증하지만 틀린 키는 검증하지 않는다. **최소 수정:** 원천 qualifier가 지정하는 조건 차원을 정본 key와 결속하고 `(key,value)` 일치로 판정한다. 차원이 원천에서 확정되지 않으면 `quotable=false`와 미확정 조건을 반환한다.

4. **FAIL — 잘못된 owner edge여도 범위 완료.** 누락 fact/source와 존재하지 않는 edge는 `backend/app/modules/gold/selected.py:37-44,174-186,214-216,237-240`에서 error/미완료가 되고, 관련 시험은 `backend/tests/test_gold_selected.py:60-89,176-185`에 있다. 그러나 edge `claims[]`의 fid를 `_validate_fact(g,fid)`로만 검사해 **그 edge가 fact.owner_id인지** 검사하지 않는다(`:174-181`). 실물 그래프에서 `R8-0144.owner_id`를 다른 존재 edge `procedure_relation:E8-0001`로 바꾼 메모리 fixture는 `pair_scope.status=found, complete=true`로 끝나고 claim은 `related_edge`/인용 불가로 남는다. 이는 손상된 provenance를 완료 범위로 오인한다. **최소 수정:** edge별 claims/conditional IDs와 fact.owner_id의 일치, resolved/대안 fact의 owner 관계를 검증하고 불일치는 `error,complete=false`로 처리한다. 다른 **존재** edge를 가리키는 손상 시험을 추가한다.

## 기존 WARN 및 새 범위

- **PASS — 방향·qualifier 표면과 축소 후 상한.** `selected.py:99-113,190-209`가 claim/대안별 edge, 원천 a/b, qualifier, 요청 방향을 반환하고 `:93-95`에서 축소 후 크기를 다시 확인한다. 역방향과 대안 조건 시험은 `test_gold_selected.py:156-173`에 있다. 다만 조건의 의미 검증은 FAIL 3과 같다.
- **WARN — §6-9 기존 페이지 회귀 증거 부족.** `test_gold_selected.py:188-205`는 뒤 페이지 다섯 사례의 ID와 `more`를 확인하나, 기존 186 section **첫 페이지의 HEAD 대비 ID 순서**를 비교하는 시험은 없다. `backend/app/modules/gold/tools.py`는 이번 diff에서 수정되지 않았고 기존 page/more/cut/peek 및 `safety.management` 시험은 남아 있다. T4는 신규 코어에서 `_pair_value`, `_filter_options`, `_edges_between`을 재사용하며 `test_gold_selected.py:34-46`은 T4 호출 가능성만 확인한다. **최소 수정:** §6-9의 186 첫 페이지 baseline 비교와 필요한 기존 회귀 증거를 남긴다. 이 검수는 전체 suite를 재실행하지 않았다.
- **PASS — REST/MCP 공통 코어.** `backend/app/router/gold.py:80-90`, `backend/app/modules/gold/mcp_server.py:93-102`, `backend/app/modules/gold/service.py:85-89`가 동일 selected 코어를 호출한다. `backend/tests/test_gold_mcp.py:47-55,78-88`은 정상 응답과 전역 두 번째 cursor 페이지의 REST/MCP 동일성을 시험한다. REST는 HTTP 400/404/422, MCP는 ToolError이므로 앱에서 같은 미수신 상태로 정규화해야 한다.

## 인계 조건

FAIL 2~4를 고치고 조합 내부 음성 쌍, 잘못된 조건 key, 존재하지만 다른 owner edge 시험을 통과시킨 뒤 재검수해야 한다. 550행/9페이지 회수는 확인됐으나 Q139 적용과 조건부 claim의 인용 자격이 아직 안전하지 않아 **앱 WP-4 인계 불가**다. Hub 호출별 cap을 SPEC-006의 전체 탐색 종료 근거로 사용해서는 안 된다.
