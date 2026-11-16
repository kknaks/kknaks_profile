# case3 반복 탐색 3차 FAIL 수정 보고

기준: 앱 HEAD `078ac99`의 기존 미커밋 구현을 이어 수정했다. 실물 Hub 서버, DB, provider 및 50·239×3 평가는 실행하지 않았다. `walk_coverage_mode=False`와 관계 WP-4 미구현 경계를 유지했다.

## 수정

- 질문의 resolve span에서 대상별 clause를 잡아 명시 facet을 연결했다. 대상마다 필요한 section을 열고, 선택에서 빠진 fact도 slim line, 조회된 원문, source, scope 및 제외 이유를 원장에 남긴다.
- 대상/facet/scope에 연결된 원문 텍스트와 ID를 한 줄 단위로 정확히 대조한다. 생성 문장이 원문을 정확히 뒷받침하지 않으면 검증된 원문 인용 답으로 대체하며, 존재하지 않는 ID는 차단한다. 분할 묶음과 합성 결과에 같은 검사를 적용한다.
- 일부 facet 조회가 실패해도 지원된 facet의 원문 인용은 답하고, 미완료 facet만 보류한다. 관계 facet은 WP-4 공개 계약 전 계속 blocked로 기록한다.
- coverage 전용 `walk_input_max_bytes`를 추가했다. 미설정 또는 0이면 provider 모델 호출을 막고 원문 기반의 제한된 답을 낸다. system+user 전체 프롬프트 바이트로 분할을 판단한다. CLI 분할 호출의 비용 추정치를 합산하고 타이머 전체 단계를 최종 timing에 반영한다.
- 이웃 Jev 선택에 coverage deadline의 남은 시간을 적용했다.
- 단위 시험에 미설정 입력 한도, 원문/대상/facet 불일치, 미완료 부분 답, CLI 분할 비용 합산을 추가했다. 기존 복합 대상 시험은 대상별 facet 기대값으로 수정했다. 시험 fixture에만 명시적인 입력 한도를 주었다.

## 검증

- `uv run pytest -q`: 235 passed
- `uv run ruff check .`: passed
- `git diff --check`: passed

## 남은 확인

- 실제 Claude CLI·SDK·Codex CLI 입력 한도와 system/prompt 외 래핑 오버헤드는 확인되지 않았다. 운영 환경의 `walk_input_max_bytes`를 검증된 값으로 설정하기 전 coverage 활성화 금지.
- 120초 deadline의 실물 TTFT p50/p90과 QID 개별/고정 50 재생은 실행하지 않았다. Hub 빈 목록·`more` 생략의 실물 계약 및 다중 페이지 동작도 검증 전이다.
- WP-4 관계 claim/대안 어댑터는 WORK-011 공개 계약·§6-9 PASS 인계가 없어 미구현이다.
