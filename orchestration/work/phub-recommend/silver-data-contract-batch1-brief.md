# 데이터 정본 계약 채택·첫 이관 묶음 준비

## 단계와 근거

사용자 승인 reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md의 단계3 명시pilot 결함 폐쇄를 silver-pilot-closeout-review/report.md에서 PASS로 확인했다. 단계4를 준비한다. **이번은 구현 전 데이터 계약·작업계획 문서 작업**이다. core source/ID/refs/scope/rule판은 명시 검증범위만 부분채택하며 pilot schema의 모든 제한을 전체스키마로 복사하지 않는다. coverage.json 25타입247필드(검증78/raw보존33/계약71/미구현62/의미미확정3)를 근거로 한다.

## 산출물과 순서

이 폴더 DATA-001.md를 데이터 구조 정본으로 작성하고, 완성 후 WORK-013.md에 첫 이관 묶음의 실행계약을 작성한다. 기존 SPEC-005/006/WORK-011/012 전체를 다시 쓰지 않는다. HTML 설계는 제안시점 증거로 보존하고 새 정본에서 참조한다. 문서만 작성, 코드/원장/데이터/서비스 수정은 하지 않는다.

DATA-001에는 검증된 core계약의 의미·source manifest/domain/logical key/locator·ID/revision·typed refs·scope 상태·서로모순되는 포함/제외·knowledge/parent·원문claims vs resolution·규칙 fingerprint/판 검증을 명시한다. 기존 v1/v2 차이(LOSS02 unit, rule nullable+reason, 조건first enum/options, override/pair provenance)를 반영한다. 전체 25타입의 소유역할·골드 노드/속성 대응과 아직제안/미구현인 상태를 명확히 쓴다. scope의 본설계어휘와 pilot어휘를 대응하고 aliases/변환불가/추가검토를 명시한다. 원천 없는 해석으로 미정3필드(subfamily/purpose ID 등)를 확정하지 않는다. identity확정과 clinical승인을 분리한다.

## 첫 이관 묶음 — 제품·계열·안전 원문 보존

다음 구현자가 이름만 맞춰 필드를 옮기지 않도록 product/family의 모든 제안필드와 이번 공통타입 사용필드 각각에 정확한 원천/현재 실버 path·변환규칙·타입·필수·빈값·출처·status·검증oracle을 적는다. prototype의 entity id/type/native_id/source_refs4칸에서 나머지 typed field로 어떻게 확장하는지 명확히 한다.

기존 step1제품395/active354·step2제품계열354/계열27·step5 extracted521+taxonomy_products59의 실제분모를 다시읽어 확정한다. 첫 묶음은 제품·계열 typed records 및 기존580안전행의 **source 원문보존과 알려진3collision 정정**을 대상으로 한다. 모든 임상안전문장의 적용승인을 새로 판정하는 작업은 아니다. identity_kind/label/이름/허가·규격·업체역할·계열mapping·기존native ID·리니지·충돌/후보/미정·이력은 실제원천에 있는 값과 정규화규칙을 분리한다. 원문 없는값은 명시미기재/미정이며 임상추정/최신허가인증 금지. raw21 밖 과거허가조사근거는 실제아티팩트ref를 보존하되 원문snapshot과 구분한다.

known common 충돌3행6원문field16잎을 보존하고 normalized predicate 다대일이 원문claim을 덮지 않게 한다. 기존 다른정상 safety rename도 유지한다. source_text→override의 원문/provenance 연결과 level/family/priority 보존, 제품 compatibility·실제선택·claim적용을 구분한다. LOSS02는 unit U5-016이지 product 아님을 명시한다.

## WORK-013 구현 발주 계약

기존 실버정본을 바로 덮지 않고 별도 candidate output에 전체분모를 재현하는 이관기/스키마·typed records·원천claim·mapping/identity ledger·coverage·검증을 만든다. 입력정본 불변·명시path/hash·재현 가능한 출력·기존ID유지·이동독립·typed refs·원문대조·모든안전field보존·오류수정의 before/after·unknown보존·반례를 수용기준으로 적는다. candidate검수→정본전환과 되돌리기 절차를 분리하고 사용자서비스/DB/Gold는 건드리지 않는 경계를 둔다. 구현코드위치와 출력위치는 같은 slug 안에 정하고 다음 코디가 그대로 발주할 수 있게 allowed_paths·필드계약·명령/증거를 구체화한다.

각필드 coverage는 기존247표와 연결하고 pilot검증을 전수이관이라고 소급표시하지 않는다. 첫묶음밖 concern/combo/site/technique/unit/package/condition/literature 전수이관은 후속계획으로만 남긴다. entity전체를 연관피상속 모든임상fact로 확장하지 않는다.

## 검증·보고·경계

DATA-001→WORK-013 작성 순서 및 문서간 일치, source/현재필드 locator실재·집계분모·coverage필드매칭·링크/표/코드펜스·기존설계와의 차이를 확인한다. 산출물은 DATA-001.md/WORK-013.md 및 silver-data-contract-batch1/report.md와 필요한 field-contract.json/읽기전용검사결과만 허용한다. 원장/실버/decisions/apply/스킬/semantic/HTML/design/v1/v2/review/기존스펙·WP/앱·Hub/env/DB/서버/네트워크/모델/설치/하위worker/commit/push/PR 금지. 필드의미를 근거로정할수없으면 범위/권고를 ask하고 정본에가짜값을넣지않는다.

완료보고는 실제 채택계약·첫묶음대상분모·필드coverage·아직미정·구현전제조건을 구분한다. live Orca preamble대로 inbox/heartbeat 처리·worker_done 한 번 후 멈춘다.
