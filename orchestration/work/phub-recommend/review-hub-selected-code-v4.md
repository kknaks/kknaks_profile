# Hub 선택 관계 4차 코드 검수

**종합 FAIL — 앱 WP-4 인계 보류.** HEAD `2edc190`와 현재 미커밋 변경을 SPEC-005 0.3.9 §5-5·§6-9, WORK-011, 3차 리뷰 및 수정 보고에 대조했다. 코드·서버·DB·평가는 변경/실행하지 않았고, 실물 Gold를 메모리에 적재한 소수 격리 시험만 실행했다. `/Users/marin/AGENTS.md`는 이 환경에 없어 읽을 수 없었다.

| 항목 | 판정 | 근거와 최소 수정안 |
|---|---|---|
| R8-0180/R8-0244 interval의 잘못된 key 차단 | **PASS** | `backend/app/modules/gold/selected.py:149-152,173-177,199-203`은 `L-SAMESITE` 원천 branch와 `같은 부위`를 확인한 후 `부위` key에만 결속한다. `backend/tests/test_gold_selected.py:189-210`은 두 fact의 `세션`/`깊이` 음성과 branch 미확정 시 `quotable=false`를 고정한다. 최소 수정안 없음. |
| 일반 R8 claim의 source path ID 결속 | **PASS** | `selected.py:57-70,245-280`은 일반·공유 claim과 resolved/대안 source 모두 `step8-relations.json`의 `claims[실제 ID]`를 요구한다. `test_gold_selected.py:225-229`의 R8-0111→기존 다른 `claims[R8-0144]` 변이가 `error/complete=false`다. 최소 수정안 없음. |
| 공유 claim·resolved·대안 | **PASS** | `selected.py:64-89,255-283`은 선택·원 owner 양쪽 edge 명시를 확인하고 다른 owner 쌍은 인용을 막는다. `test_gold_selected.py:232-277`은 잘못된 owner 및 R8-0206/R8-0156, resolved·대안을 검사한다. 최소 수정안 없음. |
| 다른 조건 표현의 key 추정 | **PASS(실물 범위)** | 실물 R8 메타 조사에서 `interval.condition`은 R8-0180/R8-0244 두 개뿐이었다. `default_apply=false` qualifier는 R8-0144/R8-0148 두 개이며, `selected.py:160-170,188-195`는 0144의 알려진 `깊이`만 결속하고 0148은 미확정으로 인용을 막는다. 0148은 `all` endpoint여서 선택 단위 쌍 경로에서 직접 시험하지 못했다. 추가 fixture가 생기면 차원 결속을 명시해야 한다. |
| **Q139 전역 메모 source path 결속** | **FAIL (신규)** | `selected.py:37-44,342-364`는 전역 fact의 source `file/path`가 비지 않았는지만 확인한다. 실물 `scope:all#evidence#step8_notes[26]`의 path를 존재하는 다른 `step8_notes[25]`로 바꾼 메모리 음성 사례에서 `global_claims(scope=fid, a=U5-110, b=U5-045)`는 `status=found`, `scope_complete=true`, `quotable=true`를 반환했다. ID·원문과 출처가 다른 행에 연결돼도 Q139 지원 사실로 전달될 수 있다. **최소 수정안:** Q139 fact의 `step7-concerns.json`/`step8_notes[26]` 결속을 확인하고, 불일치면 `error/scope_complete=false` 또는 해당 행 `quotable=false`로 닫는 음성 시험을 추가한다. 다른 전역 fact도 정본 ID에서 source path를 도출할 수 있는 경우 같은 검증을 적용한다. |
| 기존 section·peek/cut/safety 회귀 | **PASS(제출 증거), WARN(독립 재실행 범위)** | `hub-selected-fix3-report.md`는 HEAD와 현재의 전체 6,626 section 첫 페이지 ID 순서 digest 일치·불일치 0, 첫 186 digest 일치(`a85a256c…`)를 기록했다. 현재 diff에서 `backend/app/modules/gold/tools.py`는 무변경이다. 이번 격리 실행은 `test_gold_selected.py`의 뒤 페이지 사례, `test_gold_v33_expand.py`의 40/41자 cut 및 REST peek bytes를 포함한 **13 passed**였다. `test_gold_v34_step9.py:145-172`가 `safety.management`를 고정하며 수정 보고는 전체 suite **917 passed, 14 xfailed**를 제시한다. 이번 워커는 6,626 호출/전체 suite를 독립 재실행하지 않았다. 최소 수정안 없음; 코디는 제출 digest와 실행 환경을 확인해 수용 근거로 사용한다. |
| REST/MCP 공통 코어 | **PASS(코드)** | `backend/app/router/gold.py:80-90`, `backend/app/modules/gold/mcp_server.py:93-102`, `backend/app/modules/gold/service.py:85-89`가 같은 `selected` 함수를 호출한다. 수정 보고의 통합 시험 결과를 확인했고 이번 워커는 통합 시험을 재실행하지 않았다. 최소 수정안 없음. |

## 검증·인계

실행: `backend/.venv/bin/pytest -q backend/tests/test_gold_selected.py backend/tests/test_gold_v33_expand.py -k 'interval or existing_other_claim_source_path or explicit_shared_claim or other_explicit_shared_claim or line_rule_40 or peek_bytes_equal or representative_later_pages or conditional_qualifier'` → **13 passed, 29 deselected**. Q139 path 음성 사례와 실물 조건 메타 조사는 메모리 Gold에서 수행했다. 코드 수정 후 Q139 음성 시험과 REST/MCP 동등성 시험을 확인해야 하며, WORK-011의 build/서버/앱 동일 hash 관문도 코디가 확인해야 한다. 현재 **앱 WP-4 인계 불가**다.
