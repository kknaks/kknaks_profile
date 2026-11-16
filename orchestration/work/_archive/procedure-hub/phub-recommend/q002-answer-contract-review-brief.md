# Q002 답변용 근거 계약 검수

## 대상

- 프로필 `orchestration/work/phub-recommend/SPEC-006.md`의 `Q002 실물 후속 — 답변용 근거 묶음`, `안전 사실의 적용 경로`, `답 생성·검증·실패 처리`와 `WORK-012.md` WP-8.
- 근거 `reference/2026-10-30-hub-evals/build-out/q002-answer-root-cause-report.md`, `q002-after-multi-edge-live-report.md`.

## 검수

- 읽기 전용으로 사실→계약→수용 조건이 이어지는지 PASS/WARN/FAIL 판정한다. 특히 Gold가 실제로 제공하는 unit→family/site 관계로 owner 적용을 증명할 수 있는지, 부위 위험/보톡스 제한 근거를 임의 전이하지 않는지, 답변용 입력 축소가 필수 안전이나 다른 명시 target을 버리지 않는지, 재작성·부분 답 검증이 실행 가능한지를 본다.
- 걸음 수집 완료와 답변 구성의 판정은 분리하고, 특정 Q002 ID를 일반 로직에 하드코딩하는 요구가 없는지 확인한다. 구현자가 답을 꾸밀 수 있는 빈틈과 수용 시험 부족만 구체적으로 지적한다.
- 코드·DB·서비스·문서 원본은 수정하지 않는다. 결과를 `reference/2026-10-30-hub-evals/build-out/q002-answer-contract-review.md`에 쓰고 Orca `worker_done`으로 보고한다.
