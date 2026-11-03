# Hub 선택 관계·전역 상태 6차 코드 검수

**코드 범위 PASS, 앱 WP-4 인계는 아직 불가.** Hub worktree의 HEAD `2edc190` 대비 현재 미커밋 diff를 SPEC-005 0.3.9 §5-5·§6-9, WORK-011, 5차 리뷰와 대조했다. 5차 FAIL 두 건은 지정된 음성 시험에서 해소됐다. 빌드·서버·앱의 동일 build hash 관문은 이번 읽기 전용 검수 범위 밖이며 증거를 확인하지 못했다. 브리프가 참조한 `hub-selected-fix5-report.md`는 프로필 저장소에 없어서 그 제출 기록도 대조하지 못했다. `/Users/marin/AGENTS.md` 역시 현재 환경에 없다.

| 항목 | 판정 | 파일:줄 · 근거 · 최소 수정안 |
|---|---|---|
| K8 section 변조 | **PASS** | `backend/app/modules/gold/selected.py:328-337`은 K8의 owner=`scope:all`, section=`checks`, file/path=`step8-relations.json`/`conditions.claims[ID]`를 모두 확인한다. `backend/tests/test_gold_selected.py:95-106`은 `K8-0027`을 존재하는 다른 section `evidence`로 바꿔 9쪽 범위 끝까지 요청하고 `error/scope_complete=false`를 확인한다. 실제 실행 통과. 수정안 없음. |
| Q139 원문 변조 상태·인용 | **PASS** | `selected.py:293-325`의 조합 노드 원문 결속이 깨지면 `selected.py:393-406`에서 `status=error`, `scope_complete=false`, `unresolved_scope=source_text_mismatch`, `quotable=false`가 된다. `backend/tests/test_gold_selected.py:135-142`의 다른 실제 메모 원문 변조와 `backend/tests/test_gold_mcp.py:96-117`의 REST/MCP 동일 응답 시험이 통과했다. 공개 상태는 SPEC-005 §5-5의 네 값 안이다. 수정안 없음. |
| 다른 전역 text 인용 통제 | **PASS(인용), WARN(원문 정본성)** | `selected.py:395-400`은 독립 pair mapping이 없는 전역 행을 인용 불가로 만든다. `backend/tests/test_gold_selected.py:145-168`의 `principles_text_only`, `optimization_principles`, `sequence_rank`, `extracted`, 일반 `step8_notes`, K8 원문 변조가 모두 `quotable=false`로 통과했다. 다만 `selected.py:345-364`는 값 사전 외 일반 전역 fact의 원문을 독립 원천과 대조하지 않으므로 변조된 비인용 `text`가 `found` 응답에 남을 수 있다. **최소 수정:** 앱은 `quotable=false`를 인용·지원 사실로 사용하지 않으며, 향후 인용 범위를 넓힐 때 원문 결속을 추가한다. |
| 선택 쌍·550행 페이지·기존 뒤 페이지 | **PASS(소수 시험)** | `backend/tests/test_gold_selected.py:18-46,186-206,211-232,235-255,346-357,374-385`의 대표 R8 출처·방향/결정론·Q139 정상 쌍·공유 claim·550행 9쪽 전량 회수·뒤 페이지 목표 ID 시험이 통과했다. `selected.py:92-131`의 부분 페이지는 `truncated/complete=false`, 마지막은 `found/complete=true`다. 전체 186 첫 쪽 비교는 이번 범위에서 재실행하지 않았다. 수정안 없음. |
| REST/MCP 경로와 오류 응답 | **PASS(소수 시험), WARN(전체 통합 미실행)** | `backend/app/router/gold.py:80-90`, `backend/app/modules/gold/mcp_server.py:93-102`, `backend/app/modules/gold/service.py:84-89`가 같은 selected 코어를 호출한다. Q139 source path/text 변조의 REST/MCP 동일 JSON 두 사례가 통과했다. DB fixture를 쓰는 전체 통합 시험과 사용자 서버는 실행하지 않았다. 수정안 없음. |

## 실행 근거와 인계

- `backend/.venv/bin/pytest -q backend/tests/test_gold_selected.py -k 'k8_existing_other_section_cannot_complete_last_global_page or q139_other_note_text_cannot_be_quoted_with_valid_source or unbound_global_text_is_never_quotable or k8_text_without_independent_source_is_never_quotable or global_scope_pages_recover_all_source_and_text or pair_pages_recover_resolved_claims_and_alternatives or explicit_shared_claim_keeps_both_edges_without_quoting_other_pair or representative_later_pages'` → **16 passed, 23 deselected**.
- 같은 파일에서 `representative_relations_and_sources or direction_prior_conditional_and_determinism or q139_anchor_scope_both_directions_and_unrelated or interval_condition_requires_source_bound_site_key` → **5 passed, 34 deselected**.
- `backend/.venv/bin/pytest -q backend/tests/test_gold_mcp.py -k 'misbound_global_source_is_incomplete_in_rest_and_mcp'` → **2 passed, 16 deselected**. 인프로세스 메모리 그래프 시험이며 DB·외부 서버를 실행하지 않았다.
- `git diff --check 2edc190` 통과. Hub 코드·DB·서버·평가·커밋은 변경하지 않았다.

**앱 WP-4 인계는 현 시점 불가.** 5차 FAIL 수정의 코드 검수는 통과했지만, WORK-011의 기존 186 첫 쪽·전체 회귀 및 빌드/서버/앱 동일 hash를 코디가 확인해야 한다. 다른 전역 행은 현재 `quotable=false` 정책을 앱에서 유지해야 한다.
