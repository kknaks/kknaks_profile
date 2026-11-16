# WP11 실제 공개 응답 R01/R02/R03 수정

## 범위·정본

기존 clinic_chat/hub-evals 미커밋 WP11 위에서 구현한다. SPEC-006 §3-4-1-8, WORK-012 WP11과 profile reference/2026-10-30-hub-evals/build-out/wp11-context-live-receipt-review-report.md의 R01/R02/R03이 범위다. 같은 이름 -artifacts/의 raw 실제 응답·test_review_probes.py·adapter-proof-observation.json·source snapshot을 읽는다. 기존 스펙 불변식을 유지하는 앱 결함 수정이며 새 정책/Hub schema 설계를 발명하지 않는다.

## 변경

1. R01: 공개 T8 candidates 집합 endpoint의 의미를 Hub 구현에서 확인하여 검증한다. response 수준 build/echo/counts/unique/truncated 검증은 유지하고 edge별 incomplete/irrelevant/valid를 분리한다. 무관한 불완전 edge 하나로 다른 정확한 edge 증거를 폐기하지 않는다. 관련 불완전 edge는 unknown으로 보존한다. 후보 집합은 공개 명시 membership을 exact unit 단위로만 검증하며 부분 문자열/ID prefix 추정 금지. root treats와 derived treats_unit linkage를 이름/순서로 만들지 않는다. 실제 treats:0184의 from purpose:PU-04가 현재 concern anchor와 다른 사실, candidates unit membership을 증명하면 안전한 scope 판정으로 연결하되 명시 endpoint 범위를 넘어 임상 의미를 추정하지 않는다.
2. R02/R03: 모든 T11 진입점(semantic role/section-page/exact full/cache)에 공통 응답 검증을 적용한다. 실제 request echo shape에 맞춰 요청 node/명시 sections/page/exact fact_ids를 검증한다. 기본 echo 필드는 허용하되 전달한 요청 필드 누락/불일치는 실패로 둔다. node/build/exact ID/unique ID/요청 밖 ID/owner/source/cut 검증을 cache 적재 전에 수행하고 cache는 검증된 receipt만 저장한다. role 경로 dict comprehension이 중복 ID를 덮어쓰지 않게 한다. cache 재사용으로 검증이 약화되지 않게 한다.
3. 실제 저장 T8/T11 응답을 읽는 오프라인 replay 회귀를 추가한다. fixture 복사 시 원본 hash/투영 범위를 명시하고 원문/관계 합성 금지. R02/R03 변조 probes가 새 코드에서는 failed/hold로 판정되는지 검증한다. 실제 정상57 receipt와 기존 role 수집이 거짓으로 차단되지 않는지도 확인한다.

## 경계

앱 case3.py와 관련 테스트/fixture 및 보고서만 수정. 다른 미커밋 변경 유지. Hub/스펙/정책/registry/prompt/threshold/환경/DB/서버/컨테이너 수정 금지. 네트워크·모델·judge·배치·서버 기동 금지. 이번은 이미 수신된 실물 replay로만 검증한다. combo7/K8두개/추가326은 증거 미완료 상태를 보존하며 이번 패치로 해결됐다고 쓰지 않는다. 전체graph/section일괄 full/추가 frontier·조건부 경고 제외 금지. 커밋/push/PR/하위 워커 금지.

## 수용·보고

R01 실제 응답에서 정상 exact edge 보존·불완전 edge unknown·candidates exact membership·위조 membership 차단, R02 echo mismatch, R03 중복 role cache 차단, 기존 H01 warning 보존과 context 미완료 hold를 검증한다. 전체 pytest/Ruff/diff check를 실행한다. profile build-out/wp11-public-response-fix-report.md에 변경/실물 replay 결과/잔여 scope 목록/파일 해시/검증 수를 보고한다. 기존 실제 응답57 수신과 전체 context/최종 생성 성공을 구분한다.

Orca live preamble대로 체크포인트 inbox를 처리하고 worker_done을 세 문장 요약·report-path·files-modified로 한 번 보내고 멈춘다.
