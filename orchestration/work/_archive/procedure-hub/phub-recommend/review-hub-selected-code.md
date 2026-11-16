# Hub 선택 관계·전역 메모 코드 검수

**판정: FAIL — 현재 계약으로 앱 관계 어댑터 발주 불가.** HEAD `2edc190` 위 미커밋 diff와 신규 `selected.py`를 읽기 전용으로 검수했다. 기준은 SPEC-005 0.3.9 §5-5·§5-16·§6-9, WORK-011, SPEC-006 0.3.10 §3-4-1-5다. 실물 Gold 입력은 `tests.gold_support.real_graph()`로 메모리에서 읽었고 build hash는 `567677edfe7123e9`였다. 사용자 서버·포트·DB·컨테이너는 건드리지 않았다.

## FAIL

1. **호출별 상한에 걸리면 해당 범위를 회복할 수 없다.** `backend/app/modules/gold/selected.py:31-45,119-120,154-156`은 64/32 KiB를 넘으면 `resolved`, `claims`, `alternatives`, `global_claims`를 통째로 비우고 `truncated`만 돌려준다. 두 API의 입력에는 page/cursor/offset/fact ID 목록이 없고, 잘린 응답에도 다음 묶음 ID가 없다(`backend/app/schema/gold.py:47-66`, `backend/app/modules/gold/mcp_server.py:93-101`). 실물 `global_claims(scope="scope:all")`은 210,511B라 32 KiB를 넘어 모든 행이 사라진다. 같은 요청을 반복해도 같은 결과다. 현재 선택 pair 4,687개 중 최대 30,354B라는 워커 측정은 현 빌드의 비초과만 입증한다. **최소 수정:** 안정된 정렬의 cursor/page와 `more`/잔여 범위, 혹은 완전한 ID 목록을 먼저 받는 경로를 제공하고 각 페이지에 같은 build·scope를 묶어 검증한다. 초과 호출은 앱 전체 탐색 종료가 아니라 열린 frontier로 남아야 한다.

2. **Q139 전역 메모의 쌍 적용 범위를 판정하지 못한다.** `backend/app/modules/gold/selected.py:146-155`는 `source.meta.pair`만으로 `quotable`을 결정한다. 실물 `scope:all#evidence#step8_notes[26]`의 source는 `step7-concerns.json:step8_notes[26]`, `meta.pair`는 없고 `attached_to=["combo:RC-OP-Acne-중등도"]`다. Q139의 `U5-110/U5-045` 또는 `U5-110/U5-020`을 넘기면 `found`, `scope_complete:true`, `quotable:false`; 쌍을 빼면 동일 원문이 `quotable:true`다. 전자는 필요한 인용을 막고 후자는 쌍 적용 확인 없이 인용을 허용한다. `applies_to.pair:null`인데 완료 표시는 바뀌지 않는다. **최소 수정:** 원천의 `where`/anchor 또는 검증된 관계 매핑으로 Q139 메모의 적용 범위를 명시하고, 그 범위와 요청 쌍의 일치를 확인해야만 인용 가능으로 표시한다. 매핑이 불명확하면 `unresolved_scope`에 해당하는 미지원 상태를 반환한다. 양방향·두 관계와 무관 쌍 시험을 추가한다.

3. **조건부 주장에 기본 적용 가능이라는 잘못된 신호를 준다.** `backend/app/modules/gold/selected.py:21-28,86-109`에서 `include_conditional`은 요청에 기록될 뿐 claim 선별이나 `quotable`에 반영되지 않는다. 실물 `U5-023/U5-034`의 조건부 `R8-0144`는 `include_conditional=false`와 `true` 모두 `conditional:true, quotable:true`이며 `applies_to`에 조건이 없다. 따라서 앱이 `quotable`과 `pair_scope.complete`를 근거로 기본 쌍 사실로 채택할 수 있다. `alternatives`도 `sub_condition`을 적지만 그 조건의 충족 여부를 인용 가능성에 반영하지 않는다(`:110-115`). **최소 수정:** 조건부 사실은 조건과 default 적용 여부를 `applies_to`에 기록하고 기본 호출에서 인용 불가로 하거나 명확히 분리한다. 요청 조건과 실제 조건이 일치할 때만 해당 사실의 지원 판정을 허용하는 시험을 넣는다.

4. **원천 fact 누락을 범위 완료로 표시할 수 있다.** `backend/app/modules/gold/selected.py:21-28,92-120`은 edge의 claim ID가 `g.facts`에 없어도 `{text:null, source:null, quotable:false}`를 만들고 마지막에 무조건 `pair_scope.complete:true,status:found`로 바꾼다. `global_claims`도 임의의 `scope:` 문자열을 받아 일치하는 fact가 없으면 `scope_complete:true,status:empty`를 돌린다(`:128-155`). build 정합성 결함이나 잘못된 정본 ID를 검증된 부재로 오인할 수 있다. **최소 수정:** 참조 ID의 존재·owner·source를 범위 완료 전에 검증하고, 잘못된 정본 범위는 오류/미완료로 둔다. 실제 빈 확정 쌍과 손상된 그래프를 분리해 시험한다.

## WARN

- **출처와 방향 연결이 부족하다.** `backend/app/modules/gold/selected.py:93-115`는 claim마다 첫 edge를 `owners`로 잡고 요청 pair를 `applies_to`에 넣지만, edge의 원래 `a/b` 방향과 원천 `source.meta.a/b`의 qualifier·condition을 적용 판정에 사용하지 않는다. `resolved.source_fact_ids`와 대안 fact ID는 반환하나 `quotable`은 원문·위치·gap만 검사한다. `R8-0163` 같은 원천 방향 설명과 요청 역방향을 별도 시험해 `direction/condition`을 claim·대안마다 명시해야 한다.
- **크기 상한이 최종 응답 상한이라는 보장은 없다.** `selected.py:31-45`는 축소 *전* 크기만 검사하고 `request`를 그대로 남긴 뒤 재측정하지 않는다. 길이 제한 없는 `sub_condition` 값·중복 `sections`가 큰 요청이면 `truncated` 본문도 선언한 64 KiB를 넘을 수 있다. 요청 길이 제한 또는 축소 후 재측정이 필요하다.
- **§6-9 회귀 증거가 부분적이다.** 신규 `backend/tests/test_gold_selected.py:18-31,91-107`은 대표 ID 다섯 개, 뒤 페이지 다섯 사례를 확인하지만 186개 기존 section의 첫 페이지 ID를 `2edc190`과 비교하지 않는다. Q139의 `a,b` 지정, 조건부 `include_conditional=false`, 글로벌 초과 후 복구도 시험하지 않는다. 기존 `test_gold_v33_expand.py`에는 page/more/cut/peek 바이트, `test_gold_v34_step9.py`에는 `safety.management` 시험이 있고 이번 diff에서 해당 코어는 수정되지 않았다. 워커의 전체 unit 902 passed/14 xfailed 및 Ruff 통과는 전달받은 결과이며 이 검수에서 재실행하지 않았다.

## PASS / 범위 확인

- REST `/pairs/selected`, `/global-claims`와 MCP `selected_pair`, `global_claims`는 모두 `GoldToolService`를 통해 같은 `selected.py` 코어를 호출한다(`backend/app/router/gold.py:77-90`, `backend/app/modules/gold/mcp_server.py:93-101`, `backend/app/modules/gold/service.py:85-89`). 정상 입력의 핵심 schema·상태는 공유한다. REST는 `JSONResponse`, MCP는 structured tool 결과이며 잘못된 요청의 전송 오류 형태는 REST 400/404/422와 MCP `ToolError`로 다르다. 앱은 이를 같은 미수신 상태로 정규화해야 한다.
- 확정 단위 쌍을 직접 조회해 T4의 묶인 `pairs`/`pairs_more_n`에 의존하지 않는다. `_pair_value`/`orient`, `_filter_options`, `_prior_judge`, `_edges_between`을 T4와 공유하고, 대표 R8 다섯 개의 fact ID·원문·source path가 실물과 일치한다. `selected.py:69-84,104-118` 및 `test_gold_selected.py:18-45`가 근거다. 자기 쌍과 유효한 빈 쌍도 별도 처리한다.
- Q139 메모를 R8 edge owner와 별도 `scope:all` fact 경로에서 읽는 구조 자체는 맞다. 다만 위 FAIL 2 때문에 쌍별 인용 가능성은 미충족이다.

## 인계

**앱 관계 어댑터 발주는 보류한다.** 먼저 FAIL 1~4의 코어·계약을 수정하고, REST/MCP 동일 정상 결과와 오류 정규화, Q139 쌍별 적용, 조건부 및 대안 인용 자격, 64/32 KiB 초과 뒤 여러 호출로 전 범위를 회수하는 시험을 통과시켜야 한다. 특히 Hub 호출별 제한을 SPEC-006의 전체 그래프 탐색 중단으로 전파해서는 안 된다.
