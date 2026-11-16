# WP11 최종 응답 패치 검수와 잔여 적용 범위 계약안

## 정본·대상

기존 clinic_chat/hub-evals 미커밋 WP11을 읽기 전용 검수한다. SPEC-006 §3-4-1-8 B01/B02, WORK-012 WP11, wp11-public-response-fix-brief.md, profile reference/2026-10-30-hub-evals/build-out/wp11-public-response-fix-report.md 및 wp11-context-live-receipt-review-report.md가 입력이다. 실제 응답은 tests/fixtures/wp11_live_public 및 build-out의 live-receipt-review-artifacts에 있다.

## 결과 1: 독립 코드 검수

R01 실제 T8 candidates membership/edge별 incomplete 분리, R02 모든 T11 echo/provenance 검증, R03 검증 전 role cache 중복 우회를 확인한다. 기존 변조 probes를 직접 실행하거나 동등 재현하고 정상 actual57의 included47/held9/excluded1 집합을 검증한다. 실제 Hub public contract와 일치하는지, 테스트 수정이 정상 생성 회귀를 hold로 바꿔 숨기지 않았는지, H01/필수 경고/context 미완료 보류를 유지하는지 확인한다. critical/high/medium마다 구체적 근거와 재현을 적고 PASS/FAIL을 구분한다. 관련 pytest/Ruff/diff를 직접 실행한다. 코드 수정 금지.

## 결과 2: 한 번의 후속 구현으로 닫을 수 있는 최소 계약안

남은 combo7/K8-0028·0029와 추가326의 exact ID/owner 목록을 실제 artifact로 확인한다. PROCEDURE-HUB/phub-recommend/backend의 공개 API/projection 원천 코드를 읽어 앱이 부족한 적용 proof를 정확히 분류한다. 문서·설계 산출물만 만들며 스펙 정본은 고치지 않는다.

- T11 selected fact_ids에 source-specific metadata/provenance/scope를 투영하는 최소 필드 계약을 제시한다. 실제 원천 graph/fact meta에 이미 있는 값인지, 새 추론 없이는 없는 값인지 분리하고 source 코드 위치를 든다. combo source member/anchor 범위와 K8 조건/target_keys는 9개 exact ID로 좁힌다. unknown은 unknown으로 유지한다.
- 추가326은43 known candidate형/283 unknown owner에 대해 공개 원천 관계로 왜 active unit에 붙었는지 확인 가능한 최소 증거를 정리한다. product276의 unit/family/site 연결과 evidence scope:all7의 provenance를 샘플 몇 개로 확인하되 샘플을 전체 승인으로 확대하지 않는다. 각 유형의 검증 규칙과 필요한 필드를 제시하고 전체 graph/원문일괄full/무관 frontier를 해법으로 쓰지 않는다.
- 관련성 판단(Jev)과 구조적 적용 proof를 구분한다. 질문 relevance가 낮다고 같은 범위의 경고·반대 근거를 숨길 수 없고, 모든 첨부 자료가 같은 범위 필수라는 가정도 하지 않는다. 현재 수집/검증 불일치를 반복하지 않도록 어떤 context가 필요하고 언제 그 범위가 완료되는지 명확히 제안한다. 새 확률 threshold나 고정 budget은 정하지 않는다.
- 수정 대상 Hub/app 책임과 필드 shape/불변식/명시 부재 또는 unknown 처리/수용 테스트 및 안전한 격리 확인 순서를 구체적으로 제시한다. 먼저 SSOT/WP 반영 후 구현하는 직렬 절차를 지킨다. 코드가 가진 증거만으로 닫히지 않는 쟁점은 숨기지 않는다.

## 경계·보고

앱/Hub/spec/test/fixture/정책/registry/prompt/threshold/환경/DB/서버 변경·네트워크/모델/배치/하위 워커/커밋/push/PR 금지. 읽기·오프라인 테스트만 허용한다. 시작/종료 핵심 파일 hash를 기록하여 공유 변경 여부를 확인한다. 작성물은 profile build-out/wp11-response-review-scope-contract-report.md 한 개다. 검수 결과와 제안 계약안을 구분하고 전체 context/최종 답 성공을 주장하지 않는다.

Orca live preamble의 Task/Dispatch/handle대로 체크포인트 inbox 처리, 세 문장 요약·report-path로 worker_done 한 번 보낸 뒤 멈춘다.
