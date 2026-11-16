# WP-10 노드 갈래 선택 계약 검수

- 읽기 전용으로 `orchestration/work/phub-recommend/SPEC-006.md` 0.3.12 §3-4-1-7과 `WORK-012.md` WP-10/우선 계약을 검수한다. 근거는 `reference/2026-10-30-hub-evals/build-out/wp9-jev-frontier-implementation-report.md`: Q002 245 Jev/461 Hub/73초 TTFT, 7 unit 전수, 팔자 보톡스 부위 위험 누락.
- 사용자 예시 `노드→후보1,2,3→Jev→2,3 탐색→다음 후보→Jev→종료`를 정확히 구현할 수 있는지 확인한다. Jev는 노드 후보 묶음 관련성/종료, 앱은 선택된 노드 안의 facet 지원·page 종료/부재 증명이라는 역할이 명확한지, 복수 Choice 슬롯이 실제 SDK와 fake Jev에 맞는지, 미선택 갈래가 필수 target/안전을 가리지 않는지 본다. Gold에 없는 팔자 보톡스 고유 위험을 추측해 답하게 하는 허점도 확인한다.
- PASS/WARN/FAIL과 구현 차단 결함·구체 수용 시험만 `reference/2026-10-30-hub-evals/build-out/wp10-node-choice-review.md`에 적는다. 코드·DB·원본 문서/서비스 변경 금지. Orca `worker_done` 보고.
