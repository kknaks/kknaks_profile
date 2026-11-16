PASS — BR-H1·BR-M1 모두 폐쇄: 원 P5 세 반례는 ID·sidecar·output hash를 정합시킨 전체 CLI에서 각각 원문 의미 진단으로 거부됐으며, 이 판정은 고정 batch의 검증기 보완에 한정하고 원문 의학적 정확성·임상 승인·정본 전환을 승인하지 않는다.

Task `task_c2fda5154f7f` · Dispatch `ctx_560c7d8c80ef` · 2026-11-03

## 폐쇄 근거

[review.py](review.py)는 원 candidate에 CLI를 실행하지 않고 `evaluate`와 `sidecar_checks`만 호출했다. [positive-original.json](positive-original.json)의 원문/계약/파생 export 검사와 sidecar 검사는 모두 PASS다. 이후 모든 CLI 실행은 이 검수 폴더의 별도 복사본을 사용했다.

| 원 P5 반례 | 전체 CLI | 의미 진단 | ID/hash/sidecar/export 불일치 |
| --- | --- | --- | --- |
| 원문 없는 product excluded 추가 | exit 1 | SCOPE_AXIS_SOURCE, MEMBERSHIP_SCOPE_SOURCE | 0 |
| safety statement_qualifiers 전체 삭제 | exit 1 | SCOPE_QUALIFIER_SOURCE | 0 |
| product line_memberships 삭제 | exit 1 | PRODUCT_LINE_SOURCE | 0 |

[full-cli-probes.json](full-cli-probes.json)에 이 세 건과 추가 9건의 입력 변조·정규화 ID 갱신 수·진단을 남겼다. 추가 범위는 knowledge/value_kind/included, parent/conflicts/application, qualifier axis, line reason 부분 소실, unresolved 상태 변조다. [refined-probes.json](refined-probes.json)의 타입에 맞는 product included 교체와 conflicts 추가도 의미 진단으로 거부됐다. [unresolved-erasure.json](unresolved-erasure.json)은 unresolved mapping과 해당 ledger 행을 함께 지워 정합화한 뒤 PRODUCT_LINE_UNRESOLVED만 발생함을 증명한다. 최종 채택한 CLI 반례는 합계 15건이며 모두 ID/hash/sidecar/export 잡음 없이 관련 의미 진단으로 거부됐다. 일부 초기 parent/application/conflicts 반례에는 EXACT_TYPE 등 추가 구조 진단도 있지만 해당 원문 의미 진단이 별도로 있으며, conflicts와 included에는 구조 잡음 없는 보강 시험도 있다.

## 원문 기반 독립성

`independent_source.py`를 직접 읽었다. builder/rules를 import하거나 생성 함수를 호출하지 않고, 고정 manifest의 실제 파일을 읽은 docs와 collections에서 snapshot/source ID를 계산한다. source_refs별 scope 전체 목록을 먼저 대조하므로 scope 삭제·추가·다른 source로 위장하는 경우도 검출한다. 10축의 knowledge/included/excluded/raw_refs/value_kind 객체, qualifier의 axis/raw/source_ref/state/operator/value, parent/conflicts/application/source_refs를 전체 비교한다. membership mapping의 scope도 원문 제품의 기대 scope ID에 묶인다.

변환 로직의 독립성은 단지 import 부재로 판정하지 않았다. builder와 helper의 scope 기본값·소유 판단·line join에는 계약상 같은 분기가 있으며, 특히 line reason과 field-state의 고정 문구는 동일하다. 따라서 별도 구현 자체가 모든 설계 오류를 배제한다고 주장하지 않는다. DATA-001 §2~5, WORK-013과 84-field contract의 실제 transform을 읽어 명시 native ID만 연결, 새 parent 없음, 임상 적용 unknown, legacy context 미해석 보존과 대조했다. helper의 기대값은 candidate의 typed 값을 정답으로 읽지 않는다.

추가로 [source-direct.json](source-direct.json)은 helper/builder/rules 없이 별도 행 순회와 관계 edge 집합으로 현재값을 확인했다. source_record 값의 실제 원문 deep equality는 정상 evaluate가 선행 검증한다. product395+family27+safety580=1,002 scope의 10,020축을 비교했고 application unknown1,002개, raw context+needs_source+operator/value null qualifier580개가 유지됐다. 제품395개 전체에서 원문 row.line과 lines.items의 ledger_id/line_row만으로 만든 관계 edge 집합6개가 일치했다. 이름·허가번호 추정은 없으며 unresolved mapping29개는 미선택·후보[]·rule null+실제 사유를 유지한다. source 범위별 전수 보장은 helper의 source census와 읽기 전용 validator 결과를 함께 근거로 한다.

## 기존 증거 확인과 보호

[reused-evidence.json](reused-evidence.json)은 fix의 코드 hash9개가 현재 파일과 같고, 기존 CLI21건의 materialized 출력 hash/bytes와 validation 진단이 보고값과 일치함을 확인했다. 기존44 negative/14 positive는 저장된 결과 전건 PASS를 확인했고 이번에 다시 실행하지 않았다. line 추가·role/parent·reason 부분 소실·field-state 원천, qualifier raw/source/state/operator/value/추가, 축 raw_refs/source_refs와 family/membership/unit 범위 반례는 이 고정 증거를 재사용한다.

변경 없는 builder의 fix 재현본14파일은 현재 candidate와 실제 byte 비교해 동일했다. 원 P5의 2회 재현·69파일 실제 이동·source 변조/rebaseline 거부 기록은 hash가 fix에서 참조한 판과 같은 것을 확인하고 재사용했다. builder 재생성이나 이동을 이번에 반복하지 않았다.

[protection-result.json](protection-result.json)은 이번 시작·끝 1,846개 보호 파일의 hash/bytes 변경0을 확인한다. 원문69판, candidate 전체, builder/rules/transport, 계약, 원 P5와 fix 증거, cards가 포함된다. fix protected-end의 기존1,665파일도 현재와 차이0이었다. 새 파일은 이 검수 폴더 안에만 작성했다.

## 실행 한계와 초기 하네스 기록

[initial-harness-results.json](initial-harness-results.json)의 초기 line decision_ref 키 삭제는 STRUCTURAL로만 거부되어 의미 검증 증거에서 제외했다. 원문의 정상 null decision_ref 보존은 정상 전수 비교로 확인했으며, 부분 소실 반례는 reason 키 삭제로 별도 실행해 PRODUCT_LINE_SOURCE를 확인했다. 초기 unresolved 상태 변조는 파생 ledger.state를 맞추지 않아 MAPPING_LEDGER_RAW가 함께 났고, 하네스만 고친 [retry.py](retry.py)의 재실행은 PRODUCT_LINE_UNRESOLVED만 냈다. AST로 시험 함수를 재사용하는 보조 스크립트의 초기 import/path 오류는 검증기 실행 전에 발생했고 바로 수정했다.

타입에 맞는 included 교체는 OWNER_SCOPE와 SCOPE_AXIS_SOURCE가 함께 발생했는데 초기 하네스가 진단 한 종류만 허용해 실패로 잘못 집계했다. [refined-initial-harness-results.json](refined-initial-harness-results.json)을 보존하고 실제 저장된 validation에서 두 진단 모두 의미 검사임을 확인해 판정 조건을 고쳤다. 이 건은 validator를 다시 실행했다고 주장하지 않는다. 제품 코드는 일절 수정하지 않았다.

cards v2는 원문 문맥과 복수 연결 규칙을 설명하는 사용자 검토판이다. cards나 미부착152개의 의미/분류를 승인·수정하지 않았고 정상 검증 분모 eligible1,242/not_created152는 유지된다. 신규 데이터 설계, 외부 조회, 임상 검토, 서버/DB/네트워크/모델 API/설치/하위 워커/commit/push/PR/정본 전환은 수행하지 않았다. 두 기존 finding의 폐쇄 외에 전환 권한이나 전체247필드 의미 완성을 주장하지 않는다.

검수 도구는 기존 산출 폴더를 덮어쓰지 않는다. 재실행하려면 도구를 새 검수 목적 폴더로 복사하거나 R을 새 허용 하위 경로로 지정해야 한다. `review.py`, `unresolved_probe.py`, `refined_probes.py`, `retry.py`, `evidence.py`와 JSON 결과/시험 복사본을 이 폴더에 보존한다.
