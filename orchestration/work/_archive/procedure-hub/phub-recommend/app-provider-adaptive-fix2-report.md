# 앱 적응형 분할 관계 검증 fix2 보고

- 기준: 앱 HEAD `078ac99` 위 기존 미커밋 작업을 이어서 수정했다. 수정 파일은 `clinic_chat/cases/case3.py`, `tests/phase8/test_case3_walk.py`, `tests/phase8/test_relation_adapter.py`다. 커밋·push·PR은 하지 않았다.
- 한 분할 part에 관계 source ID가 모두 있을 때 그 part의 `relation_resolved`와 `relation_prior`를 정본 문장 검증에 전달한다(`case3.py:2358-2359`). part ID 완전성은 기대 ID 집합과 인용 ID 집합으로 대조한다. 같은 ID가 원문과 정본 관계 문장에 각각 나와도 허용하며, 동일 문장을 중복 출력하면 거절한다(`case3.py:535-536,2347-2359`). 정본 이외의 값·ID·쌍·방향·조건 문장은 여전히 완전 일치 검증에서 거절한다.
- 최종 답 확정 뒤 호출하는 공통 citation 기록 함수를 추가했다(`case3.py:557-566`). 분할 성공·일부 실패, 원문 fallback, 단일 호출 및 인용 없는 조기 반환 모두 실제 최종 답의 인용 순서와 반복을 `walk.answer_citations`에 기록한다(`case3.py:2166,2179,2415,2426,2475`).
- 격리 시험: 한 part 완전 관계의 원문+관계 및 관계 문장만, 서로 다른 part 성공, 한 part 실패의 `blocked/incomplete`, 위조 값·ID·쌍·방향·조건, citation trace의 분할/일부 실패/fallback/단일 경로를 확인했다. `uv run pytest tests/phase8/test_relation_adapter.py tests/phase8/test_case3_walk.py -q` **128 passed**; `uv run pytest -q` **301 passed**; `uv run ruff check .` 통과; `git diff --check` 통과.
- 기존 cap 미설정 호출, SDK/CLI context 재시도, 비용 합산, 안전 flags·유보, WP-4 관계 출처 검증은 시험 회귀 없이 유지했다. 실물 서버·DB·provider·고정 50·239×3 평가는 실행하지 않았다. CLI 실물 context 오류 문구와 분할 시도별/최종 timing 대조는 여전히 활성화 전 실물 관문이다.
