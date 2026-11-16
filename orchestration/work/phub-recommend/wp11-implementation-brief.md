# WP-11 자연어 claim·번호 출처·최종 전달 계측 구현

## 정본·범위

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 WORK-012 위에서 구현. 정본 프로필 SPEC-006 0.3.14 §3-4-1-8/WORK-012 WP-11, `wp11-answer-quality-proposal.md`와 `reference/2026-10-30-hub-evals/build-out/wp11-contract-review.md` A01~A20/`wp11-contract-rereview.md` PASS. 정본 B-01/B-02 보강이 제안의 cited-only/장기 분할보다 우선한다.
- I-01 coverage CLI만 claim_v1 기능 플래그로 구현하고 **기본 off, 실제 한국어 정책 평가 전 활성화 금지**. 수집/노드 Noul/공개 안전·여섯 보류·다른 의도/provider 계약은 유지. 새 실물/provider/Jev/judge/batch 호출 없이 offline/fake로 구현 검증한다.

## 구현

1. 작은 answer_contract 모듈에서 strict AnswerDraftV1 schema/파싱, 앱 발급 bundle/source/requirement 검증, semantic 질문 생성/판정, 번호 출처 렌더를 만든다. 기존 CLI run(schema=...) 구조화 경로를 연결하고 structured 누락/무효 JSON/refusal/한도는 자유텍스트 대신 보류한다. 최초+수정 최대2회, 같은 bundle만 사용한다.
2. 앱이 cited/context 출처를 각각 발급하고 같은 scope의 조건/상충 원문을 인용 선택으로 숨기지 못하게 한다. 명시 conflict는 모델 점수와 무관하게 차단. 필수 manifest는 검증 section/path/flags/scope와 기존 의무로 결정하며, 원자 필드가 없으면 **전체 원문/모든 조건을 불가분 의무**로 보존한다. source/span/hash/build/scope/필수 이유/manifest hash. 모델 태그로 답 unit/의무를 줄이지 않는다. Q002 ID를 런타임 하드코딩하지 않는다.
3. claim별 supports/contradicts/unsupported Choice와 requirement coverage/scope 질문을 한 system_one에 배치한다. 각 instructions는 정확한 claim/source/context/requirement 인덱스를 지정한다. 승인 claim 집합만의 requirement→source→최종 span 커버를 결합하고 탈락 집합의 커버 판정은 재사용하지 않는다. 오류/누락/불확실/미검증 정책은 승인하지 않는다. 한 요청 한도 초과는 보류, 신규 chunk 시스템은 만들지 않는다. 실제 모델 정책 검증용 한국어 라벨 fixture/오프라인 평가 입력과 실행 도구를 준비하되 이번에 API를 호출하지 않는다.
4. 고정 비임상 제목+검증 claim만 사용자 답으로 렌더하며 내부 ID는 trace에, 화면은 짧은 번호 출처로 표시한다. 모든 필수 위험/고지·조건을 유지하면서 중복 명제를 합칠 수 있어야 한다. 원문 fallback이 21행 dump/정의없는 수치가 되면 품질 PASS 금지, 환자 적합성 확인 불가면 범위 hold.
5. deliver_final에 모든 coverage 최종 반환을 연결하고 callback 전에 attempt lock, 실패/중복/부분출력 후 예외를 기록한다. 같은 clock의 generation_returned/final_validation_completed/final_on_text_started/completed/case_completed, schema_v2/status/hash/시도수를 저장한다. CLI timing 사본/parts/runner except가 final을 덮거나 지우지 않게 한다. structured-only이면 model_first_text null 허용. 기존 TTFT는 유지하고 새 지표를 보고 도구에 구분한다.

## 수용·보고

- A01~A20의 fake fixture, 특히 모든 fake score=1에도 명시 conflict·위조 scope·구조적 manifest/승인span 누락 거부, 정상 의역 통과/반대·조건·수치·의무 삭제 거부의 조합 로직, 다른 intent/provider/off 회귀, 가짜 시계·callback 실패/중복/모든 반환 경로를 시험한다. fake all-green을 의미 효능이라고 주장하지 않는다. 전체 suite/Ruff/diff PASS.
- 코드/관련 테스트·도구만 수정. Hub/DB/사용자 포트·컨테이너·커밋/푸시/PR·실제 API/평가 금지. 결과와 남은 실제 정책 평가 게이트를 `reference/2026-10-30-hub-evals/build-out/wp11-implementation-report.md`에 쓰고 Orca worker_done 보고.
