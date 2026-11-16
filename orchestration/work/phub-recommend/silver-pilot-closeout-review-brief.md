# 단계3 pilot scope·rule 보완 독립 검수 및 단계4 coverage 인계

## 범위

계획 reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md 단계3 계속. silver-design-pilot-v2-review/report.md R-H1/R-M1과 silver-design-pilot-v2/scope-rule-fix-report.md 및 contract.md가 기준이다. 기존 source/ID/refs 회귀를 보존하며 최신6파일 수정의 계약 충족을 읽기 전용 검수한다. 허용 작성은 silver-pilot-closeout-review/ 아래 report.md/probes/results/coverage.json뿐이다. 원장·실버·v1/v2/기존리뷰/design/HTML/스펙/WP/앱·Hub/환경/서버·DB 무변경. 네트워크/모델/설치/하위worker/commit/push/PR 금지.

## 1. 명시 결함 폐쇄 검수

- R-H1의 included/excluded disjoint, duplicates(원문 container 역할중복 예외 포함), knowledge/근거 조합, parent source context와 self/cycle 검사를 generic/source-specific 수준에서 확인한다. 정상comparison parent2개와 unknown후보보존을 유지하는지 확인한다. 정상값을 모두 비워 PASS시키면 안 된다.
- R-M1 resolution policy id/version/hash/decision판, attachment id/version·구현/contract fingerprint와 source/target/scope/resolution 정합을 확인한다. 자체 산출물을 oracle로 쓰지 않고 선언과 actual source를 대조한다.
- v2리뷰 추가10개 중 과거허용6개를 ID재계산 후 직접 재현하여 관련진단으로 거부되는지 확인한다. scope_rule_probes.py의 확장38과 과거회귀/이동/원문 검증은 결과를 실제 재실행하고 필요범위로 대조한다. 결과 저장은 새 검수폴더로 돌려 원래 artifact 불변 유지.
- 이번 수정 메커니즘에 관련된 독립 반례만 추가한다. 무제한 새 범위를 만들어 반복하지 말고 현재존재 필드의 실질 결함과 향후 미구현 coverage를 구분한다. 검사수 대신 각결함의 폐쇄근거를 보고한다.

## 2. 전체 구조와 pilot coverage 인계

design.json 25논리타입247필드 각 항목을 현행 실버/원문 locator 및 pilot typed schema와 대응한 coverage.json을 작성한다. 이것은 구현/최종의미승인이 아닌 **현재와 미구현 구분표**다. 필드마다 proposed type.field, origin/current path(확인되면), pilot typed path/없음, 상태(pilot검증/원문raw보존만/계약만/미구현/의미미확정), 근거를 포함한다. 단순 fieldname 일치나 raw_value 안의 존재를 typed 이관완료로 세지 않는다. 논리타입과 Gold노드 구분을 유지한다.

PASS시 부분채택 가능한 core계약(ID·refs·scope·rule판)과 전수실버 이관 전 필요한 실제 entity필드·normalization·source coverage를 인계한다. 다음 구현은 source record 원문보존/확인된오류 정정/typed entity 이관을 묶음별로 할 수 있도록 우선범위를 제안하되 정본확정이나 데이터수정은 하지 않는다. 42사례·146combo 밖 의미 검증 미완료를 감추지 않는다. 원천미정은 구현누락과 분리한다.

## 판정·보고

시작/종료보호 hash와 검수기준코드hash를 남긴다. report.md에 R-H1/R-M1 PASS/FAIL·실제반례·정상보존·source/ID회귀 결과, coverage의 타입/필드분모·미확인·단계4전제조건을 기록한다. 전체임상·서비스활성화·이관완료 승인 금지. live Orca preamble의 inbox/heartbeat/worker_done을 따르고 완료 후 멈춘다.
