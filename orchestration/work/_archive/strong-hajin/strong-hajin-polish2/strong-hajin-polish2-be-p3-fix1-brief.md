# [backend] WORK-009 Phase 3 — 검수 WARN 재수정 (fix1)
앞 판 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-be-p3-brief.md` 규칙 그대로(subject 「backend 완료: WORK-009 Phase 3 fix1」). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-be-p3-report.md` W1~W4 전부 읽어라. 코디 판단: **넷 다 고친다.**

참고 — 코디 실물 1회(로컬, 「디자인 시안 최종 검토 업무 만들어 줘」): 도구 9회(graph_search·my_meeting_list·material_search·list_projects·task_get·graph_neighbors·task_get·task_get·task_create_self), **67초**(제한 90초), 연결 4종 채움·사람·날짜 비움·체크리스트가 읽은 업무를 반영. 여유가 작다.

1. **W1** ID 와 날짜 문장을 나눈다 — **ID** 는 대화·조회 근거(현행), **날짜는 대화가 준 것만**(기록 속 날짜·할 일 마감 후보를 옮기지 않음). `tool_catalog.py:546`·`:648` 의 「IDs and dates come only from the conversation or lookup」과 `codex_cli.py:477-478` 을 이 기준으로. 같은 뜻 문장 전부 grep
2. **W2** 탐색 호출 상한을 문장으로 — 초안 전 탐색의 **검색은 도구마다 한 번**(graph_search·my_meeting_list·material_search 각 1회), **상세는 최대 3건**, 연결 탐색(list_projects·graph_neighbors)은 필요할 때 한 번. material_search 「최대 세 번」(:396-398)이 생성 턴에는 「한 번」으로 읽히게 정리
3. **W3** 예외 꼬리가 **금지 문장까지 풀지 않게** — `:410` 「넓힌 목록으로 내 업무 답하지 않는다」·`:385`·`:395` 의 꼬리를 「무엇이 예외인지」(탐색 호출 자체)만 가리키는 자리로 옮기거나 문장을 「…를 부르지 않는다(업무 초안 준비 턴의 관련 기록 탐색은 예외). 넓힌 목록으로 …답하지 않는다」 처럼 나눈다
4. **W4** `test_ax_work_lookup_policy` 의 brakes 튜플 + `len == 5` 빈 단언·깨진 따옴표 — 각 제동 문장이 실제 정책 문자열에 있고 그 뒤에 예외가 붙었음을 문장별로 단언
검증 test-unit · test-contract · inventory drift(그 항목만).
