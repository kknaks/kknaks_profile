# WP-11 코드·한국어 평가 라벨 검수

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 WP-11을 읽기 전용 검수. SPEC-006 0.3.14 §3-4-1-8/WORK-012 WP-11, `wp11-implementation-report.md`, 계약 A01~A20/B-01/B-02/재검수 PASS 대조. 코디 신규 answer_contract 67tests PASS, 전체586tests 보고.
- claim_v1 strict structured CLI 연결, 앱 소유 cited/context·manifest/승인집합 커버, 미지원/반대/조건/수치·부재 gate, 활성 unit/태그 우회, bounded 수정·정책 미검증 off, 번호 렌더/trace, final delivery lock·예외/CLI timing 덮어쓰기를 검수한다. fake 전량 supports=1의 의미는 조합 검증뿐이며 실제 모델 효능과 구분한다.
- `tests/fixtures/wp11_korean_labels.json` 17개 초안의 claim↔제공 원문/조건/반대 문맥 관계와 expected label을 독립 대조한다. 임상 사실의 외부 진위를 인증하는 작업이 아니라 **제공 근거가 주장을 지지하는지** 라벨을 검수한다. 잘못된/모호한 라벨은 명시하고 실제 정책 평가 전 수정 필요로 기록한다. 평가 도구가 자기 정답을 모델 응답으로 재사용하거나 sample 누락을 숨기지 않는지 확인한다.
- 실제 API/Hub/provider/judge/batch, 코드/DB/서비스·정본 변경 금지. `reference/2026-10-30-hub-evals/build-out/wp11-code-review.md`에 PASS/WARN/FAIL·P1/P2 재현·라벨 판정·실제 한국어 정책 평가 착수 조건을 기록하고 Orca worker_done 보고.
