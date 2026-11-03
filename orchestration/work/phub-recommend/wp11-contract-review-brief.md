# WP-11 답변 claim·계측 계약 검수

- 읽기 전용으로 SPEC-006 0.3.14 §3-4-1-8, WORK-012 WP-11, `wp11-answer-quality-proposal.md`를 검수한다. 현재 Q002 결과/답의 21줄 원문 덤프·내부ID·여섯 보류·계측 미확인이 문제 근거다. TypeSafe 공식 citation_check/primitives/fan-out과 기존 CLI 구조화 경로를 확인한다.
- Claude 원자 claim+source schema→앱 binding/안전/부재→한 요청 독립 Jev 의미/coverage→번호 출처 렌더→실제 최종 callback 계측이 구현 가능한지, 모델 태그·Choice 결과가 hard gate를 우회하는지, 한국어 의미 검증·필수 고지/조건 커버·실패/최대1회 수정·원문fallback이 구체적인지 PASS/WARN/FAIL한다. 조건부 구문·수치 분모·원문 속 지시·반대 출처·render 추가 문구·CLI timing 덮어쓰기 반례를 본다. 작은 I-01 CLI 범위를 넘어 기능을 넓히지 않는다.
- 구현 차단 결함과 수용 시험을 `reference/2026-10-30-hub-evals/build-out/wp11-contract-review.md`에 기록. 코드·DB·서비스·정본 수정/새 provider·judge·batch 호출 금지. Orca worker_done 보고.
