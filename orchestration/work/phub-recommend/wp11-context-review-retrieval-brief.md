# WP11 context 수정 읽기 전용 검수 및 누락 수집 경로 확인

## 대상·정본

기존 clinic_chat/hub-evals 미커밋 WP11을 읽기 전용 검수한다. 이 폴더 SPEC-006 §3-4-1-8 B01/B02, WORK-012 WP11과 wp11-context-binding-fix-brief.md가 계약이다. 프로필 reference/2026-10-30-hub-evals/build-out/wp11-context-binding-fix-report.md 및 -trace.json, wp11-claim-q002-experiment-artifacts 원본을 읽는다. 앱 case3.py 변경과 tests/phase8/test_context_binding.py, tests/fixtures/wp11_context_q002.json이 직전 변경이다.

## 해야 할 일

1. 독립 코드 검수: role/family/self/safety/borrowed 구분, 동일 scope 반대 근거 누락 방지, 잘못된 조건 제외, owner/build/source/received_build/cut/full 검증을 확인한다. 테스트가 구현을 그대로 따라가는 데 그치지 않는지 실제 저장 증거와 대조한다. critical/high 결함은 구체적 재현과 함께 FAIL. 코드 수정 금지.
2. 저장 Q002의 포함 36 / 보류 57을 확인하고, 보류 57개를 ID와 유형으로 분류한다. 공개 full API로 원문을 받을 수 있는데 기존 수집이 선택되지 않은 행을 건너뛰는지, full 실패/누락인지, Hub projection 자체 부족인지 추적한다. 앱 Hub client 및 기존 PROCEDURE-HUB/phub-recommend/backend 공개 API 구현과 projection 코드를 읽어 확인한다. 비공개 DB 직접 접근이나 원문 추정으로 증명을 대체하지 않는다.
3. 원문/관계 조회 가능한 기존 공개 endpoint와 요청 인자·응답 증명 필드를 구체적으로 제시한다. 다른 treats actual endpoint, combo applicability, check_condition/scope:all 및 complication family 적용 증명을 각각 확인한다. 코드만으로 불명확하면 unknown이라 적고 최소 확인 요청을 명시한다.
4. 다음 구현 범위를 하나로 정리한다: 기존 수집 단계에서 필요한 context 원문/관계만 추가 수집하고 visited tuple/중복 방지/종료 조건을 보존하는 최소안. blanket fetch 또는 무관 노드 연쇄 탐색을 제안하지 않는다. 답변 직전 make_bundle에서 새 탐색하지 않는다. Hub 수정이 필요하면 앱 수정과 나누어 정확한 필드 계약을 제안한다.

## 경계·수용

앱/Hub/스펙/fixture/정책/prompt/환경/DB/포트/서버 변경 금지. 모델·judge·배치·네트워크 실험 호출 금지. 읽기와 오프라인 테스트만 허용한다. 보고서만 profile build-out/wp11-context-review-retrieval-report.md에 쓴다. 커밋/push/PR/하위 워커 금지. 새 design을 임의 확정하지 않는다.

관련 테스트를 직접 실행하고 diff를 확인하며 PASS/FAIL과 잔여 자료 부족을 구분한다. 원래 잘못된 scope 증명에 합격을 주지 말고, 원문 미수신을 자료 없음으로 단정하지 않는다. 이번 검수 통과도 실제 Q002 답변 성공으로 주장하지 않는다.

완료는 Orca live preamble의 Task/Dispatch/handle을 따라 세 문장 요약과 report-path로 worker_done 한 번 보고한 뒤 멈춘다. 체크포인트에서 inbox 처리한다.
