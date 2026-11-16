# Hub 전역 출처 결속 수정 보고

## 결과

`backend/app/modules/gold/selected.py`의 `global_claims` 공통 코어에 전역 fact 출처 검증을 추가했다. 전역 fact의 정본 ID와 section/owner를 검사하고, ID에 들어 있는 원천 경로를 실제 `source.file/path`와 대조한다. 대상은 `step8_notes`, `sequence_rank`, `principles_text_only`, `optimization_principles`, `extracted`, 전역 `K8` 주장이다. 값 사전 fact는 대응하는 전역 사전 ID·원문 및 항목 순서의 source path를 함께 검사한다. 불일치는 `malformed_graph` 오류와 `scope_complete=false`, 빈 `global_claims`로 반환한다.

Q139 `scope:all#evidence#step8_notes[26]`을 존재하는 다른 `step8_notes[25]` 경로로 바꾼 경우 이제 `status=error`, `scope_complete=false`다. 원문을 다른 메모로 바꾼 경우에는 기존 조합 시퀀스 결속이 적용 범위를 미확정으로 처리해 `quotable=false`가 된다. 기존 선택 쌍 claim/conditional/resolved/대안 로직은 수정하지 않았다.

## 시험

- `backend/tests/test_gold_selected.py`: 32 passed. 다른 존재 경로(전역 종류별), 다른 file, 다른 owner, 값 사전 원문, Q139 다른 원문을 검사했다.
- `backend/tests/test_gold_mcp.py -k misbound_global_source`: 1 passed. 같은 변조 그래프에서 REST와 MCP가 동일한 미완료 JSON을 반환했다.
- DB를 쓰지 않는 최상위 `backend/tests/test_*.py` 32개 모듈: 504 passed, 14 xfailed. `graph_db`, `db_provider`, `create_async_engine`, `async_sessionmaker`를 사용하는 모듈과 평가 모듈 및 `integration/`은 제외했다.
- 관련 `test_gold_v33_expand.py`, `test_gold_v34_step9.py`, `test_gold_v32_mcp_meta.py`에서 DB fixture 없는 시험: 28 passed, 5 deselected.
- `ruff check backend`: 통과. `git diff --check`: 통과.

서버·DB·평가를 실행하지 않았고 커밋·push·PR을 만들지 않았다. `/Users/marin/AGENTS.md`는 이 환경에 없어 읽지 못했다. 현재 worktree에는 이번 수정 전부터 있던 미커밋 Hub 변경이 있으며, 이 작업에서 직접 수정한 파일은 `selected.py`, `test_gold_selected.py`, `test_gold_mcp.py`다.
