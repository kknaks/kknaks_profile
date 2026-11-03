# WP11 독립 코드 검수와 실제 한정 Hub receipt 확인

## 대상·권한

기존 clinic_chat/hub-evals 미커밋 WP11을 읽기 전용 검수한다. 이 폴더 SPEC-006 §3-4-1-8, WORK-012 WP11, wp11-context-collection-fix-brief.md, profile reference/2026-10-30-hub-evals/build-out/wp11-context-collection-fix-report.md 및 wp11-context-review-retrieval-report.md를 따른다. 이번에는 코디네이터가 **실제 한정 공개 Hub 요청**을 승인한다. Claude/Jev/judge/전체 Q002 생성/배치는 실행하지 않는다.

## 1. 독립 검수

앱 case3.py의 최신 collection/binding/inventory 변경을 읽고 H01/M01/M02의 실제 해소 여부, 반복·중복·무관 확장, 조기 종료와 context 완료 혼동, request echo/build/owner/source/scope 검증을 독립 검수한다. 특히 unknown 조건의 필수 경고 보존과 원문·관계 없을 때 보류, combo membership을 단독 적용으로 승격하지 않는지, 실제 응답 shape와 fixture의 차이를 확인한다. 기존 57개와 그 외 active inventory를 구분한다. 테스트용 synthetic 성공을 실물 성공으로 계산하지 않는다. 관련 테스트와 Ruff/diff를 직접 실행한다. 결함 발견 시 수정하지 말고 위치·재현·심각도를 기록한다.

## 2. 실제 한정 receipt 확인

이전 build-out/wp11-claim-q002-experiment-harness.py의 격리 Hub 실행/health/raw manifest/build 확인 방식을 참고한다. 기존 PROCEDURE-HUB/phub-recommend/backend 코드를 사용하되 사용자 Hub18005·앱18210/DB publication pointer/컨테이너/공유 .env는 변경하지 않는다. 18015가 비어 있을 때 본인 Hub만 띄우고 본인 PID만 종료한다. 이미 점유됐으면 중단하고 ask한다. 기대 Gold hash567677edfe7123e9/publication78e94deb-d4a3-4442-964a-dd5b08ee1cf5/raw21/21을 확인하며 다르면 hold한다.

공개 HTTP API로만 기존 후보를 확인한다. U5-082의 원래 미선택57 fact_ids에 한정한 T11(<=64), 해당 unit T5 checks(conditions 생략/sections=checks), 필요한 inbound treats T8, 이미 노출된 combo 2개의 구성/anchor T8, complication unit/family T8를 요청한다. 추가 후보를 확인할 경우 active unit의 필요한 slim section inventory만 읽는다. 이웃 본문·새 추천 frontier·전체graph/full=true/sections=all 수집 금지. 읽기 전용 요청과 raw response/hash/build/상태를 별도 새 artifacts에 보존하고 이전 Q002/fixture/calibration 증거는 불변으로 둔다. API키/헤더/환경 비밀은 기록하지 않는다.

가능하면 최신 앱 adapter/receipt 검증 함수를 실제 응답에 적용하여 원문 received/missing/cut/error 및 적용 proved/unknown/excluded를 ID별 집계한다. 수신된 원문을 추측으로 scope에 연결하지 않는다. bundle 발급 조건 충족 여부와 미완료 inventory를 구분한다. 기존 57개 receipt 확인이 전체 context 완전성 증명은 아니다. 코드 검수 FAIL이어도 안전한 읽기 전용 receipt 관찰 자체는 진행할 수 있으나 FAIL 코드를 사용해 답변 생성하지 않는다.

## 경계·산출물

앱/Hub/spec/test/fixture/정책/registry/threshold/prompt/환경 변경·커밋/push/PR·하위 워커 금지. profile build-out/wp11-context-live-receipt-review-report.md 및 새 wp11-context-live-receipt-review-artifacts/ 안의 하네스/증거만 작성 가능하다. 서버 종료·port cleanup을 finally에서 보장하고 기존 하네스의 SDK close/aclose 혼동을 반복하지 않는다(SDK 호출 자체 불필요).

보고서는 코드 검수 PASS/FAIL, 실제57 원문 수신수와 적용 검증수, 실제로 빠진 필드/구체적 ID/최소 Hub projection 요청안을 구분한다. 해결 가능하면 다음 앱 수정점만 제시하고 구현하지 않는다. 모든 source/관계/inventory가 닫히기 전 실제 생성 시험 준비 완료라 쓰지 않는다.

Orca live dispatch preamble대로 체크포인트 inbox 처리, 완료 시 세 문장 요약·report-path·실제 files-modified로 worker_done 한 번 보내고 멈춘다.
