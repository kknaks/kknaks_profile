# WP-9 Jev 동적 탐색 계약 검수

- `orchestration/work/phub-recommend/SPEC-006.md` 0.3.11 §3-4-1-6과 `WORK-012.md` WP-9를 읽기 전용 검수한다. 근거는 `reference/2026-10-30-hub-evals/build-out/wp8-answer-gate-repair-report.md`의 Q002 290호출/133 side-effects page 원인과 사용자의 "Jev가 질문↔다음 노드 관련성·종료를 판단" 요구다.
- Jev의 관련성 선택과 앱의 ID/build/owner/scope/필수 안전·부재 검증 경계가 모순 없는지, 매 순회의 후보/선택/종료 payload가 기존 Jev `Choice` API로 구현 가능한지, 지원된 facet의 뒤 page 종료와 나중 page 유일 근거 탐색이 양립하는지, I-01 외 명시 target/관계 의도가 보호되는지 본다. "Jev가 멈춤"만으로 원천 부재가 되는 허점, 정해진 depth/bytes로 조용히 자르는 허점, 같은 요청 반복과 무한 탐색을 지적한다.
- PASS/WARN/FAIL과 구현 전 필수 수정·수용 시험을 `reference/2026-10-30-hub-evals/build-out/wp9-jev-frontier-review.md`에 기록한다. 코드·DB·서비스·원본 문서는 수정하지 않고 Orca `worker_done` 보고한다.
