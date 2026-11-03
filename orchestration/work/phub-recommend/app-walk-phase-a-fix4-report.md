# case3 coverage 분할 FAIL 수정 보고

- 대상: 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`, 기준 HEAD `078ac99`; 기존 미커밋 작업 위에 `clinic_chat/cases/case3.py`, `tests/phase8/test_case3_walk.py`를 수정했다. 커밋·push·PR은 하지 않았다.
- 분할 묶음은 facet의 실제 `support_ids`만 담는다. 같은 대상의 다른 section fact가 앞 묶음에서 소비되지 않으며, 대상별 원문 줄에 `target_key`를 표시하고 ID·owner·section 관계를 검증한다. 반복 target span의 위치와 clause 범위, 전치·공통 facet도 회귀 시험으로 확인했다.
- 각 SDK/CLI part의 예외, error, refusal, 비정상 stop, 빈 답, 입력 상한 초과를 실패로 기록하고 해당 facet을 `blocked/incomplete`로 남긴다. 성공 part만 전달 묶음에 기록하며 최종 답은 성공 facet의 검증된 원문, 미완료 범위 유보, 필수 안전 flags를 함께 합성한다. 분할 입력 바이트와 part 결과를 trace에 남긴다.
- CLI 분할의 합산 비용을 유지하고, 마지막 CLI timing의 보강 필드와 stages를 전체 timer에 보존한다. 기본 `walk_coverage_mode=False`와 관계 WP-4 유보는 유지했다.
- 검증: 관련 87개 시험 통과, 전체 `uv run pytest -q` 240개 통과, `uv run ruff check .` 통과, `git diff --check` 통과.
- 미확인: 실물 Hub page/원문/source 계약, provider별 실제 입력 한도와 CLI 래핑 오버헤드, 50/239×3 재생 및 120초 TTFT p50/p90·오류 분포. 서버·DB·실물 provider·평가는 실행하지 않았다. Coverage 활성화 전 이 운영 관문과 WP-4 선행 계약 검증이 필요하다.
