# case3 분할 part 인용 ID 완전성 수정 보고

## 결과

앱 worktree의 기존 미커밋 변경(기준 HEAD `078ac99`)에 분할 part 검증을 추가했다. 각 part에 실제 전달하는 `facts`와 `support_ids`를 같은 ID 목록으로 맞추고, 모델 답의 인용 ID를 제공 ID와 비교한다. 누락·추가·중복 ID가 있으면 `answer_id_mismatch`로 실패 처리하며, 해당 part를 완료 또는 `delivery_groups`에 기록하지 않는다. 성공한 다른 part의 검증된 ID만 전달 묶음에 남는다.

실패 facet은 `blocked/incomplete`로 남고 `unread`에는 해당 part의 실제 실패 사유가 기록된다. 전체 `stop`은 context 제한 또는 도구 오류에 따라 기록한다. 성공 facet의 원문 부분 답, 미완료 범위 유보, 필수 안전 flags를 유지했다.

## 검증

- SDK·CLI 양쪽에서 F1/F2 중 F1만 답하는 경우와 ID 추가·중복을 포함한 분할 음성 시험: `19 passed`.
- 관련 시험: `103 passed`.
- 전체 시험: `256 passed`.
- `uv run ruff check .`: 통과.
- `git diff --check 078ac99`: 통과.

실물 서버·DB·provider와 50/239×3 평가는 실행하지 않았다. 기본 coverage gate는 `False`이고 WORK-012 WP-4 관계 지원 완료 경계는 그대로다. 커밋·push·PR은 만들지 않았다.
