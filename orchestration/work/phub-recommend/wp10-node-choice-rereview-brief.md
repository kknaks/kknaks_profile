# WP-10 노드 갈래 선택 계약 재검수

- 이전 `reference/2026-10-30-hub-evals/build-out/wp10-node-choice-review.md`의 FAIL 다섯 항목을 기준으로 수정된 `orchestration/work/phub-recommend/SPEC-006.md` 0.3.12 §3-4-1-7과 `WORK-012.md` WP-10 검수 차단 해소 문단을 읽기 전용으로 재검수한다.
- 복수 Choice `pick_1..pick_k`/none/중복/stop 충돌/다음 묶음, 선택 노드의 facet page 지원·후속 page·선택 full ID, 직접 역할 edge와 선택 unit의 의무 분리, 미선택 갈래/필수 안전, Gold 안전 공백 보류, 종료/성능 동시 관문이 각각 실행 가능한지 PASS/WARN/FAIL한다. 새 범위를 넓히지 말고 구현을 막는 남은 모순만 지적한다.
- 결과를 `reference/2026-10-30-hub-evals/build-out/wp10-node-choice-rereview.md`에 쓰고 Orca `worker_done` 보고. 코드·DB·원본 문서·서비스 수정 금지.
