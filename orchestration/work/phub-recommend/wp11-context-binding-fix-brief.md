# WP11 context relation binding 수정

## 대상·정본

기존 clinic_chat/hub-evals 워크트리의 미커밋 WP11 위에서 작업한다. 정본은 이 폴더 SPEC-006 §3-4-1-8(B01/B02), WORK-012 WP11이며 계약 변경 없이 구현 결함을 고친다. 직전 증거는 프로필 reference/2026-10-30-hub-evals/build-out/wp11-claim-q002-experiment-report.md 및 같은 이름의 -artifacts/source-context-and-scope.json, trace.json이다. 프로필 루트는 이 브리프 경로의 orchestration 상위다.

## 문제와 변경

case3.make_bundle이 active unit에서 수신한 모든 evidence를 direct treats role과 같은 규칙으로 검사하여 family 연구·combo·다른 concern 근거까지 context_relation_unverified로 전체 보류한다. 실제 질문과 동일 범위의 context를 앱이 증명하여 발급하고, 무관한 행은 증거에 따라 제외해야 한다. 해당 범위의 반대 근거나 조건을 선택되지 않았다는 이유로 숨기면 안 된다.

1. 저장된 Q002 증거를 오프라인 재현하여 최초 실패 행과 원인을 특정한다. context 판단별 raw id/node/owner/applies_to/source/build/target/scope 및 포함·제외·보류 사유를 구조화 trace에 남긴다. 비밀·키 기록 금지.
2. direct role, self, public safety 및 기존 공개 relation proof를 구분하여 검증한다. evidence 전부를 role로 승격하지 않는다. 다른 concern/unit/조건에 명백히 해당하는 행은 scope 이유로 제외한다. 같은 범위의 제한·상충 행은 반드시 보존한다. 관련성 또는 출처/적용 범위를 증명하지 못한 필수 행은 여전히 보류한다. 전체 evidence 제외, broad allowlist, 문자열 ID 하드코딩, semantic 모델로 구조 검증 대체 금지. 기존 verified_full/cut/build/owner 불변식 유지.
3. active 필수 facet의 borrowed neighbor receipt도 사라지지 않는지 검사한다. 새 공개 Hub projection이 필요하여 앱만으로 안전한 증명이 불가능하면 우회하지 말고 구체적인 누락 필드·행·최소 수정안을 보고한다.

## 소유·제약

앱 case3.py/answer_contract.py 및 관련 테스트와 이 작업 보고서만 수정한다. 이미 있는 다른 미커밋 변경은 유지한다. Hub/DB/출판 포인터/사용자 서버·포트·컨테이너/.env/정책 registry·threshold·prompt·calibration artifact는 수정하지 않는다. 기능 기본 off 유지. 실제 Claude/Jev/judge/배치 호출·서버 기동 금지. 커밋·push·PR 금지. 구현 워커 혼자 작업하며 별도 하위 워커를 띄우지 않는다.

## 수용 기준

- 실제 저장 Q002의 지원된 필러 branch가 bundle/manifest를 발급할 수 있는지 오프라인 확인한다. 다른 여섯 branch 보류는 유지한다. 발급 불가능하면 정확한 근거 결함을 숨기지 않는다.
- 무관 concern/unit/다른 조건·위조 owner/build/미검증 relation은 거절 또는 증명된 scope 제외, 같은 scope 제한/반대 근거는 미선택 상태여도 포함·명시 conflict 차단하는 회귀 테스트.
- 기존 claim binding/manifest 의무를 약화하지 않고 전체 pytest, Ruff, git diff --check 실행. 적절한 명령은 앱 pyproject/기존 검증 절차를 따른다.
- build-out/wp11-context-binding-fix-report.md에 최초 실패 행, 변경 규칙, 실제 replay 결과, 테스트 수, 변경 파일, 잔여 게이트를 기록한다. 실제 모델 효능을 주장하지 않는다. 구현 뒤 별도 읽기 전용 코드 검수 및 단일 Q002는 코디네이터가 발주한다.

## 완료 보고

Orca live dispatch preamble의 Task/Dispatch/handle이 권위다. 자연스러운 체크포인트와 완료 직전에 inbox를 확인·처리하고, 완료 시 세 문장 요약과 실제 report-path/files-modified로 worker_done을 한 번 보낸 뒤 멈춘다. 막히면 같은 preamble의 ask로 코디네이터에게 구체적으로 질문한다.
