# 앱 case3 provider 입력 적응형 처리 보고

- 기준: 앱 HEAD `078ac99`, 기존 WP-1~4 미커밋 작업 위에 수정. `walk_coverage_mode=False` 기본 gate 유지.
- 변경: `walk_input_max_bytes=None`에서도 선별된 원문 사실을 SDK/CLI에 먼저 전달한다. 명시 값은 생성 입력 분할 override로만 사용한다. SDK는 가능하면 `messages.count_tokens`로 실제 system+user 입력을 세고 기본 `claude-sonnet-5-5`의 1M context에서 8,000 출력 토큰을 남긴다. count 호출 실패나 미지원은 생성 호출로 진행한다. CLI는 API key가 필요한 count에 의존하지 않고 실제 context 오류를 감지해 facet/ID 묶음을 이분 재시도한다. 한 fact도 수용되지 않으면 해당 facet을 `blocked/incomplete`로 표시하고 원문 기반 부분 답과 유보를 낸다.
- 전달 보존: 각 part에 관련 target, facet, ID, 원문, source/scope, 관계 메타데이터, 필수 안전 고지, 미완료 범위를 싣는다. part별 실제 호출 상태·timing·cost를 `walk.provider_attempts`에 남기고 CLI 실패 호출도 합산한다. 반복된 SDK `claude` 단계 비용을 합산하도록 `case_cost`를 수정했다. 최종 단일 답도 모든 선택 근거 ID를 인용했는지 검사한다. 수집용 고정 byte 장부는 이 단계에서 새로 도입하지 않았다.
- 격리 검증: cap 미설정 SDK count/생성, cap 미설정 CLI context 실패 후 분할, SDK token preflight, 명시 override, 단일 fact context 실패의 부분 답·유보, 기존 ID/출처·안전·관계 검증을 시험했다. `uv run pytest tests/phase8/test_case3_walk.py tests/phase8/test_verify_runs.py tests/phase4/test_timing_runs.py tests/cli/test_rerun_report.py -q` 107 passed; `uv run pytest -q` 291 passed; `uv run ruff check .` 통과; `git diff --check` 통과.
- 남은 관문: 실물 provider/서버/DB 및 고정 50·239×3 평가는 실행하지 않았다. 다른 모델의 context 크기는 미리 가정하지 않고 실제 provider 오류를 통해 분할한다. CLI context 오류 판별은 현재 알려진 오류 문자열에 기반하므로 새로운 오류 문구는 실물 검증 때 추가 확인이 필요하다. 커밋·push·PR 없음.

공식 근거: [Sonnet 5.5 개요](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting).
