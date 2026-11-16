# Hub 선택 관계 3차 코드 검수

**종합 FAIL — 앱 WP-4 인계 불가.** 기준 `2edc190` 대비 현재 미커밋 diff를 읽기 전용으로 검토했다. SPEC-005 0.3.9 §5-5·§6-9, WORK-011, SPEC-006 0.3.10 §3-4-1-5와 대조했다. `/Users/marin/AGENTS.md`는 이 환경에 없어 읽지 못했다. 서버·DB·평가와 코드는 변경하거나 실행하지 않았고, 실물 Gold를 메모리에 만든 `tests.gold_support.real_graph()` 및 격리 단위 시험만 사용했다.

## 항목별 판정

1. **PASS — Q139 인접 pair와 무관 pair 차단.** `backend/app/modules/gold/selected.py:280-312,343-350`은 원문·combo anchor·component를 확인한 뒤 `U5-045/U5-110`(4주 후), `U5-110/U5-020`(동시 도포) 두 관계만 정규화 쌍으로 열거한다. `backend/tests/test_gold_selected.py:141-160`은 양방향, 조합 내부 비지원 쌍 세 개, 무관 쌍, pair 없는 호출의 `quotable=false`를 확인한다. 단위 시험도 통과했다. **최소 수정안:** 없음.

2. **PASS — R8-0144 qualifier의 key/value 결속.** `backend/app/modules/gold/selected.py:156-166,169-184`는 알려진 원천 qualifier를 `{"깊이":"심부 · 페놀"}`로만 묶고, 차원 미확정이면 인용을 막는다. `backend/tests/test_gold_selected.py:163-180`의 올바른 키·잘못된 `세션` 키·미확정 qualifier·역방향 시험이 통과했다. **최소 수정안:** 없음.

3. **PASS — 공유 claim의 다른 owner edge 방어와 선택 쌍 인용 자격.** `backend/app/modules/gold/selected.py:57-89,232-270`은 공유 fact가 원 owner와 선택 edge 양쪽의 `claims`에 명시돼 있고 원천 path가 그 fact를 가리키는 경우에만 허용한다. 실물 `R8-0206`은 owner `E8-0028`, 선택 `E8-0029`로 완료 조회되지만 `direction=related_edge`, claim/resolved source/대안 모두 `quotable=false`다. 같은 fixture에서 owner를 존재하지만 claim을 갖지 않는 `E8-0001`로 바꾸면 `status=error, complete=false`가 된다. `backend/tests/test_gold_selected.py:201-246`도 claim·conditional·resolved·대안의 잘못된 owner와 다른 공유 사례 `R8-0156`을 검사한다. 실물 공유는 30 fact가 62 edge 자리에 나열돼 있으며, 개별 62자리 전수 음성 변이는 하지 않았다. **최소 수정안:** 없음; 전수 변이 시험은 추가하면 좋다.

4. **FAIL — 다른 `source_condition`은 여전히 값만 비교한다(신규).** `backend/app/modules/gold/selected.py:140-148,188-190`은 interval 조건 `같은 부위`를 `sub_condition`의 임의 값과 비교한다. 실물 `R8-0180` (`U5-026/U5-100`)과 `R8-0244` (`U5-022/U5-102`)에서 `{"부위":"같은 부위"}`뿐 아니라 `{"세션":"같은 부위"}`와 `{"깊이":"같은 부위"}`도 claim `quotable=true`로 나왔다. 앱이 잘못된 차원을 맞는 조건으로 받아 의료 관계를 인용할 수 있다. **최소 수정안:** interval 조건의 정본 차원을 원천에 근거해 `(key,value)`로 결속한다. 차원이 확정되지 않으면 `unresolved_condition`과 `quotable=false`를 반환하고 두 fact의 잘못된 key 음성 시험을 추가한다.

5. **FAIL — 일반 claim의 source path가 다른 fact를 가리켜도 인용된다(신규).** `backend/app/modules/gold/selected.py:37-54,57-62`는 일반 owner claim에서 `source.file/path`의 존재만 검사하며, `claims[<fid>]`와 실제 ID의 일치를 확인하는 로직은 공유 claim에만 있다(`:63-70`). 실물 `R8-0111`의 source path를 존재하는 다른 `claims[R8-0144]`로 바꾼 메모리 fixture에서 `U5-023/U5-034`가 `status=found, complete=true`, 해당 claim `quotable=true`였다. 출처가 다른 주장으로 결속된 채 §5-5의 지원 사실로 전달된다. **최소 수정안:** 일반 R8 claim에도 ID와 원천 path의 결속을 확인하고 불일치 시 `error, complete=false`; 이 변이를 음성 시험에 추가한다.

6. **PASS — 전역 550행 페이지 재조립.** `backend/app/modules/gold/selected.py:92-131,315-358`은 build·정규화 요청에 묶인 cursor와 32 KiB 상한으로 이어 읽는다. `backend/tests/test_gold_selected.py:92-114`는 실물 550행을 9페이지 `[85,83,51,52,52,36,48,75,68]`로 회수하고 ID·원문·source file/path의 전량 일치, 각 응답 상한, 최종 `more=0/scope_complete=true`를 확인한다. 해당 시험 포함 21개가 통과했다. **최소 수정안:** 없음.

7. **WARN — §6-9의 기존 페이지 회귀 증거가 아직 부족하다.** `backend/tests/test_gold_selected.py:249-266`은 뒤 페이지 5사례를 현재 `g.section_ids`와 비교하지만, WORK-011:51·SPEC-005 §6-9가 요구한 기존 186 section 첫 페이지의 `2edc190` 대비 ID 순서 비교는 없다. `backend/app/modules/gold/tools.py`는 이번 diff에서 변경되지 않아 회귀 가능성은 낮지만, 코드 무변경만으로 수용 관문의 검증 증거를 대신할 수는 없다. 기존 peek compact byte 차 0, cut 인용 자격, `safety.management`도 이번 재검수에서 실행 확인하지 않았다. **최소 수정안:** HEAD의 첫 페이지 186 ID 목록을 고정해 현재 결과와 비교하고, 기존 해당 회귀 시험 결과를 남긴다.

8. **PASS — REST/MCP 공통 코어.** `backend/app/router/gold.py:80-90`, `backend/app/modules/gold/mcp_server.py:93-102`, `backend/app/modules/gold/service.py:85-89`가 같은 선택 코어를 호출한다. `backend/tests/test_gold_mcp.py:47-55,78-88`은 기본 응답과 전역 둘째 cursor 페이지의 동등성을 검사한다. 이번에는 이 통합 시험을 재실행하지 않았다. **최소 수정안:** 없음.

## 검증과 인계

`cd backend && pytest -q tests/test_gold_selected.py` 결과 **21 passed**. 추가 실물 메모리 음성 호출에서 공유 owner 손상은 오류로 닫혔고, 4·5항의 잘못된 인용을 재현했다. 4·5항을 고친 뒤 해당 음성 시험과 §6-9 첫 페이지·기존 회귀 증거를 확인해야 한다. 현재는 **앱 WP-4 인계 불가**이며, SPEC-006 §3-4-1-5에 따라 응답 상한이나 부분 조회를 탐색 완료·사실 부재의 근거로 사용해서는 안 된다.
