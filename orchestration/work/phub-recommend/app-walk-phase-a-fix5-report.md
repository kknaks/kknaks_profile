# case3 분할 part 완료 판정 수정 보고

## 변경

- `clinic_chat/cases/case3.py`: 분할 part의 정상 stop·비어 있지 않은 답도 `_supported_answer`가 ID, owner, target_key, section, 원문을 대조한 뒤에만 `completed`와 `delivery_groups`에 기록한다. 대조 실패는 `answer_evidence_mismatch`로 기록하고 해당 facet을 `blocked`, 전체 coverage를 `incomplete`로 둔다. 다른 part의 검증된 원문 답과 필수 flags는 유지하고 실패 범위만 유보한다.
- 빈 답의 실패 이유를 정상 stop 값인 `end_turn` 대신 `empty_answer`로 기록한다. 입력 한도 실패와 part 처리 실패의 `walk.stop`을 각각 `context_limit`, `tool_error`로 구분한다.
- `tests/phase8/test_case3_walk.py`: 성공 fixture를 유효한 원문 인용으로 바꾸고 SDK 및 Claude CLI part의 잘못된 ID, owner, target_key, 원문, 빈 답 10개 음성 사례를 추가했다. 실패 part 유보, 성공 part 부분 답, 필수 flags, 단일 최종 출력도 확인한다.

## 검증

- `uv run pytest tests/phase8/test_case3_walk.py -q -k 'split_'`: 13 passed.
- `uv run pytest -q`: 250 passed.
- `uv run ruff check .`: 통과.
- `git diff --check 078ac99`: 통과.

## 경계

`walk_coverage_mode` 기본값 False와 WP-4 관계 미지원 경계는 유지했다. 실물 Hub·DB·provider, QID 재생, 50/239×3 평가는 실행하지 않았다. 실제 provider 입력 한도와 Hub page/source/cut 계약 확인 및 평가 관문은 후속 작업이다. 앱 코드는 커밋·push·PR하지 않았다.
