# v2 검증용 계약

이 계약은 단계3 pilot에만 적용하는 제안이다. 임상판정·정본 이관·Gold 활성화 승인이 아니다. v1 42사례, combos146, LOSS16잎, note7과 기존 미정을 보존한다.

## H1 / M2: identity와 판

source domain은 `raw21`, `generated-silver`, `decision-artifact`로 구분한다. collection은 각각 `procedure-hub/raw21`, `procedure-hub/generated-silver`, `procedure-hub/decision-artifact`라는 고정 논리명이다. file key는 collection 루트에 대한 상대 POSIX 경로 전체다. basename-only/content-only 병합은 금지한다. locator는 별도 물리경로다.

collection snapshot ID = `snap:` + SHA256(canonical JSON([domain, collection, 정렬된 [logical_file_key, full SHA256] manifest])). raw21은 실제 원문21 전체를 포함한다. generated/decision은 pilot이 사용하는 파일의 명시 collection이며 원문21의 판과 섞지 않는다. source occurrence ID = `src:` + SHA256([snapshot ID, logical file key, JSON Pointer]). 이동은 ID 불변, file key 변경·다른 domain·행재정렬은 새로운 snapshot/occurrence다. entity ID는 기존 namespace:native_id이며 행재정렬·표시이름 변경에도 유지한다.

normalized record는 immutable source identity와 다른 수명이다. 여기서 revision 대상은 scopes/mappings/claims/relation_claims/notes/decisions/resolutions/attachments다. cases.id는 기존 evidence 행 식별자를 유지하고 legacy_aliases는 namespace+snapshot_ref+alias 자연키의 집합 레지스트리이며 별도 normalized ID를 발급하지 않는다. 이들의 전송 필드 모양은 최상위 schema_version이 갖는다. record ID는 type prefix + SHA256([record schema version, mapping contract revision, id를 제외한 canonical record payload])이며 source/entity ID는 이 공식을 쓰지 않는다. dependency 순서로 ref를 먼저 새 ID에 연결한다. scope→mapping→claim(variant parent 먼저)→relation→note→decision→resolution→attachment 순서다. normalized revision은 schema/rule 판 또는 내용 변경에 바뀐다. record 간 순환은 이 pilot에서 허용하지 않는다. design.json hash는 감사용 basis일 뿐 ID 입력이 아니다. source native_id와 source_kind는 실제 원문과 domain에서 독립 확인한다. validator는 위 알고리즘을 직접 재계산한다.

## H2: typed refs

모든 ref의 type/cardinality는 schema의 필수/nullable/배열 minItems와 `ref-contract.json`에 선언한다. `cases.evidence_refs`는 기존 evidence 행 이름인 원문 literal이며 entity ref가 아니다. expansion.id, note.existing_claim_refs.id는 source native ID이며 source_record_ref에서 확인한다. mapping.rule.id, policy.id, attachment.rule.id는 versioned rule 식별자이며 graph record ref가 아니다. override.override_of는 entity ref다.

축 값은 value_kind로 나눈다. product/family/site/unit_procedure/concern/target은 entity_refs, container는 source_literals, site_relation은 relation_conditions(same_site/different_site), statement_site/patient_conditions는 none이다. included/excluded는 각 축 타입만 수용하며 raw_refs는 source_records다. 임의 축은 거부한다.

claim.override의 claim/scope/decision/source, decision.target_refs(1+ claims)/supersedes(0+ decisions), attachment witness의 mapping/source/relation/component source를 각각 도달·타입 검사한다. witness는 mapping이 source를 포함하고 attachment target을 candidate/selected로 가리켜야 한다. edge/component는 함께 있어야 하며 해당 relation member와 일치해야 한다. 이 pilot의 실제 witness는 []이고 application_state=unknown이다. 근거 없는 witness를 발명하지 않는다. approved_rule은 실제 step9-decisions 원문 정책/날짜/이유/대상과 결합하며 human은 reviewer 없는 승인을 거부한다. 이 pilot에는 실제 human 승인 근거가 없으므로 human 전환 자체를 거부한다.

## H3: 의미

원문 값 보존과 구조화 의미 검사는 별개다. 언어 family=M2, unknown application, statement/patient_explanation predicate 및 동일 source statement variant parent를 독립 확인한다. 모든 combo container는 원문 complaint의 cc/cc_group을 그대로 보존한다. nary direction=unknown이다. interval 수치 정본은 interval이고 field_conditions.days는 독립 원문이 없는 한 null이어야 한다. timing의 same_day/first는 원문의 interval/note로 별도 확인한다. 원문 미기재(not_declared), unknown, null, explicit_no_required_order를 합치지 않는다. 이 fixture는 정본 duration 숫자 interval을 새로 계산하지 않는다.

## M1: identity와 clinical application

exact identity8개(CC4, timing endpoint2, duration2)는 원문 correspondence/attach/from/to와 selected를 대조한다. candidate selected0과 미승인 clinical edge0을 별도 검사한다. rule id/version/code hash는 실제 생성기 파일과 Silver 버전·correspondence에 대조한다. exact를 모두 hold로 내려 통과시킬 수 없다. 조회 projection은 원문 fact·확정 identity·보류 적용을 따로 제공한다. withheld graph는 usable Gold 입증이 아니다.

## 보호입력과 수정 경계

v1 inputs-start와 v1/review 파일 및 실제 immutable 원장·실버·설계는 시작/종료 SHA256/bytes를 비교한다. WORK와 진행기록은 mutable 별도 manifest에 기록한다. v1 WORK hash 불일치는 알려진 코디 진행 갱신이며 과거 baseline은 수정하지 않는다. 복사·재배열 시험은 이 v2 내부 임시 디렉터리에서만 수행하고 끝나면 삭제한다. 네트워크·설치·모델·하위워커·commit·DB·서버 실행은 없다.

## R-H1: 축 상태와 source context (scope-rule 보완)

모든 축의 included/excluded는 각각 중복 없는 집합이며 교집합은 비어야 한다. 단 container의 [cc, cc_group]은 역할 순서가 있는 원문 literal 두 슬롯이다. 실제 3행은 두 슬롯의 문자열이 같으며, 해당 complaint raw_refs와 두 원문 슬롯이 exact 일치할 때만 이 중복을 보존한다. 임의 반복·excluded 중복은 거부한다. 같은 대상의 포함·제외 동시 표기는 미지원이다. 상충 원문은 conflicts와 source_ref 및 statement_qualifiers로 보존하며 resolved 축 값으로 승격하지 않는다. value_kind=none은 항상 두 값 배열이 비어 있다.

explicit은 최소 한 포함/제외 값과 원문 근거를 요구한다. 근거는 raw_refs 또는 그 scope를 사용하는 claim/mapping의 source_refs로 제공할 수 있다. unknown은 원문 근거가 있는 후보 값을 유지할 수 있으며 빈 값도 허용한다. not_declared는 값이 비어 있고 실제 검사한 원문 근거가 있어야 한다. not_applicable은 값이 비어 있고 비적용을 뒷받침하는 원문 근거가 있어야 한다. 후자의 두 상태는 원문 의미를 읽은 source-specific 검사 없이 서로 바꿀 수 없다. 이번 실물에는 explicit 166축, unknown 149축, not_applicable 2축이며 not_declared 실물은 없다. generic 상태 허용은 새로운 임상 positive의 증거가 아니다.

현재 pilot의 유일한 정당한 parent는 procedure-comparison의 procedures 멤버 → 같은 comparison 원문의 subtitle context다. 멤버 raw_refs는 해당 procedures occurrence, context raw_refs는 그 comparison occurrence이며 parent 자체는 null이다. self/cycle과 다른 comparison·다른 source의 parent를 거부한다. 나머지 모든 scope는 parent=null이다. 실제 claim 계통과 축 raw_refs를 함께 대조하며 source parent/continuity_ref의 null을 임의의 정규화 parent 근거로 쓰지 않는다. parent를 통한 축 합성은 지원하지 않는다.

언어 scope는 원문 categories/M2 계통의 family explicit included=[family:M2], excluded=[], raw_refs=[], parent=null만 허용하며 application=unknown이다. combo scope는 해당 complaint의 cc/cc_group을 순서대로 container explicit included에 보존하고 excluded=[]로 둔다. container raw_refs는 complaint occurrence, statement_site는 unknown·빈 값·해당 combo occurrence를 유지한다. 이 두 source context에는 다른 축·무관 parent를 추가할 수 없다. unknown이라는 이유로 비교 후보·타이밍 조건·팔자/목 conflict·원문 statement를 지우지 않는다.

## R-M1: 선언된 rule 계약

resolution.policy는 D9-3, 실제 decision-artifact step9-decisions.json의 version을 문자열로 변환한 값, 실제 step9-apply.py SHA256, 그리고 그 원문 decision을 가리키는 decision_ref를 모두 exact 검사한다. source판 확인과 기존 conservative output 검사를 함께 적용한다.

attachment.rule의 typed 값은 id=pilot-preserve-source/version=1로 고정한다. ref-contract.json의 attachment_rule 선언은 구현 build.py 및 이 contract.md의 고정 SHA256를 함께 갖는다. validator는 빌더 산출물에서 기대 rule을 추출하지 않고 ref_contract.py의 고정 선언 및 파일 fingerprint를 검증한다. 이 감사 fingerprint는 graph ref나 임상 승인 필드가 아니므로 기존 정상 attachment payload와 revision ID를 바꾸지 않는다. 규칙 의미는 원문 claim의 subject=target, 동일 scope, unknown application, 빈 witness, 실제 duration resolution일 때만 연결 허용이다. subject 없는 claim의 attachment 및 새 witness positive는 이번 규칙에서 지원하지 않는다. 원문 근거 없는 target 변경·추가 승인·무관 resolution 연결은 거부한다.

실물 축의 source-specific knowledge: product/family/unit_procedure/concern/target/container는 explicit, site/statement_site는 unknown, patient_conditions는 not_applicable이다. site_relation의 빈 공통 문맥은 unknown이고 두 원문 분기는 explicit이다. generic unknown 후보 허용을 이 원문 확정 축을 unknown으로 바꾸는 허가로 해석하지 않는다.
