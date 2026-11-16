# 앱 provider 적응형 관계 답 보존 수정 보고

2026-11-02 · 앱 기준 HEAD `078ac99`와 기존 미커밋 WP-1~5 변경 위에 수정. 커밋·push·PR 없음.

## 수정

- `case3.py`에서 `resolved.value/field_status/by_direction`, `prior.ok/basis`를 쌍·방향·조건(`source_rows[].applies_to`)·모든 `source_fact_ids`와 함께 정본 관계 문장으로 만든다. 문장은 원천 fact ID/원문/source/scope와 지원 관계 facet을 대조한 뒤에만 허용한다. 모델에는 `verified_relation_lines`를 전달하고, 최종 검증기는 그 문장과 원문 fact 문장을 각각 확인한다. 모델이 관계 문장을 생략했으면 검증된 문장을 보태며, 검증에 실패한 원문 fallback에도 관계 문장을 보존한다.
- 분할 병합은 각 part가 검증한 ID의 합집합에 관계의 **모든** source ID가 있고 관계 facet이 성공했을 때만 값을 낸다. 서로 다른 part에 나뉘어도 결합되지만, 한 source part라도 실패하면 관계 값을 유보하고 `blocked/incomplete`를 유지한다. 각 part의 `verified_relation_lines`에는 그 part가 전부 담은 관계만 넣는다. 최종 `answer_citations`는 fallback 뒤 실제 답을 기준으로 기록한다.
- `tests/phase8/test_relation_adapter.py`에 단일 호출 resolved 답, 역방향 prior 값, 두 source의 다른 part 성공/일부 실패, ID·값·facet 음성 검증을 추가했다. 기존 Q139 전역과 R8 관계, 부분 답·안전 flags·ID 시험도 전체 suite에서 재검증했다.

## 검증

`uv run pytest -q`: 294 passed. `uv run ruff check .`: PASS. `git diff --check`: PASS. 서버·DB·실물 provider·고정 50/239×3 평가는 실행하지 않았다.

## 남은 관문

실물 CLI의 context 오류 문구가 현재 `_context_failure` 목록에 포함되는지는 미확인이다. CLI 병합 timing의 boot/TTFT 보조 칸은 마지막 호출 값이라 전체 합산 stage/elapsed와 의미가 다를 수 있다. 두 WARN은 실물 검증 전 추정으로 수정하지 않았다. 기능 활성화 전 WORK-011 인계대로 서버·앱 build hash 일치와 실제 selected/global endpoint, QID 재생 및 WORK-012 고정 평가가 필요하다.
