# WORK-013 첫 실버 candidate 구현 보고

Task `task_58b443eb2006` · Dispatch `ctx_5fceae89c5b8` · 2026-11-03

**P0–P4 구현·자체검증 PASS. P5 독립 candidate 검수와 정본전환은 미실행이다.** 새 candidate는 비활성 산출물이며 기존 step1/2/5 정본과 서비스 읽기경로를 바꾸지 않았다. 임상 검토·허가 재인증·제품선택·Gold publication은 0건이다.

## 1. 구현과 고정 입력

새 schema `silver-batch1/1`, attachment 규칙 `batch1-source-preservation/2`를 구현했다. `silver-batch1-migration/`의 build.py·rules.py·transport.py·84필드 type-contract.json이 변환 fingerprint를 구성하고, expected-rules.json의 고정 실제 파일 hash를 독립 validator가 대조한다. validator는 builder/rules의 변환 함수를 import하지 않고 실제 원문과 승인된 계약·고정 oracle를 읽는다. type-contract.json은 중첩 객체/배열/enum/required/null/정수와 bool 구분까지 검사하며 schema.json에 그대로 포함된다.

승인된 manifest v2 69파일(raw21 21, generated18, research11, decision13, audit6)의 full SHA256/bytes를 전부 확인했다. DATA-001/2·WORK-013·field-contract·collections·reconciliation·evidence-manifest·580 locator·1394 field oracle·recount·247 baseline·pilot fixture의 시작판을 expected-inputs.json에 고정했다. 다른 manifest/field-contract나 입력 bytes 변경은 중단하며 재baseline하지 않는다. `_RESUME.md` 현재판은 읽지 않고 승인 frozen snapshot을 원문으로 보존했다. 코디 진행기록은 보호입력 집합에서 분리했고 frozen 파일은 보호했다.

5개 collection은 각자 snapshot을 갖는다. audit 6파일의 snapshot과 audit-sidecar는 데이터 source_refs 및 normalized ID에서 분리했다. 비감사 63파일의 전체 root를 source_record로 보존해 연구/KPIC/허가/결정의 역사적 문자열·JSON·추가 원문을 보존했다. 과거 연구의 명시 ID가 실제 제품 ledger ID와 일치하는 모든 occurrence를 연결하고 이름 first-match는 쓰지 않았다. text/.md는 media_type=text/plain, pointer="", 전체 실제 line 범위 및 bytes hash로 보존하고 UTF-8 왕복을 검증했다. JSON version 정수/문자열/null/missing은 manifest의 파일 meta 그대로 유지하며 collection version/captured_at은 null+근거 미확보 사유다.

pilot 회귀용 regression-inputs.json에는 fixture가 실제 가리키는 원문 13파일의 hash/bytes를 별도로 고정했다. 이들은 회귀 입력이며 69파일 semantic membership이나 신규 이관 실적에 합산하지 않았다.

## 2. 실제 분모

| 대상 | 실제 결과 |
|---|---:|
| product/native identity | 395 (active354 / inactive41) |
| family/native identity | 27 |
| product_family source행 / active ID집합 | 354 / 정확 일치 |
| family null / pending_director | 3 / 3 보존 |
| 계열 밖 source membership | 5 excluded 보존 |
| safety source행 | items521 + taxonomy products59 = 580 |
| safety/aftercare 원문 | 1,394 field / 4,170 scalar leaf |
| override 원문 | units248 + product_links376 = 624 |
| attachment eligible | 1242 field / 동일 owner attachment1개씩 |
| attachment not_created | 152 field / attachment0 |
| 미부착 field 사유 | candidate_only49 / out_of_batch_entity83 / owner_unresolved20 |
| 미부착 행 사유 | candidate_only19 / out_of_batch_entity37 / owner_unresolved6 |
| 후보19 + 원문보관37 | 56행 / 132field claim보존·attachment0 |
| 제한 registry | unit96 / technique17 (전수이관 아님) |
| source-row-index | 1356 source행(395+27+354+580) |
| records | source_record23255, scope1002, mapping2797, claim13399, attachment1242 |
| 새 decision / relation / resolution | 0 / 0 / 0 |

나머지524행/1262field를 자동 eligible로 삼지 않았다. 제품은 current row의 명시 product와 실제395 제품 ID 도달성을 확인하고, unit은 단일 units 값과 step5.units의 실제 ledger source ID/역할까지 대조했다. 다수 unit owner 등 추가 미확정20field는 owner_unresolved로 보존한다. LOSS02의 owner는 `unit_procedure:U5-016`이며 product를 발명하지 않았다. eligible1,242와 not_created152는 서로소이고 합이 원문1,394다.

단일 owner 확인은 검색 부착 근거다. 모든 attachment는 subject=target, 동일 scope, application_state=unknown, witness=[], resolution_ref=null이다. 안전·사후관리 normalized_value=null이고 검토상태는 unreviewed 또는 원천 충돌 source_conflict다. 임상 confirmed/선택/적용 승인으로 올리지 않았다.

제품·계열의 전체 원문과 직접 필드 claim을 보존했다. license 전체·licenses/history/reference 각 항목·status/reason/recommendable은 별도 원문 claim으로 연결하고 spec JSON은 환산하지 않았다. 업체역할은 각 원래 role/name/original과 claim으로 분리하며 「근거 없음」은 회사로 확정하지 않고 field_state에 남겼다. merge/move/split은 원문 명시 ID/값만 사용했고 absent와 null/default를 구분했다. 라인은 실제 line_row와 ledger_id 연결만 참조로 만들고 이름·허가번호만 있는 parent는 미정 mapping으로 남겼다.

역사적 gate/open/change/name_basis/결정 root와 실제 문맥을 보존했으나 새 approval authority를 충분히 검증한 decision을 생성하지 않았다. decision_refs=[]는 unresolved 사유를 가진다. 따라서 decision8필드는 typed 완료가 아니라 source_preserved_no_approval/typed0이다.

## 3. 손실 복구와 원문 연결

| 원천 충돌 | 이전 leaf | 복구 후 leaf | 복구 leaf |
|---|---:|---:|---:|
| M1-1-3 | 2 | 5 | 3 |
| auto-2-1774737181584 | 2 | 5 | 3 |
| M7-P-1 | 2 | 6 | 4 |

3행의6field를 각각 다른 raw_field/source occurrence/claim으로 남겨6→16leaf, 기존 소실10leaf를 복구했다. 같은 normalized predicate라고 원문 claim을 합치거나 dedup하지 않았다. override-projection은624항목 각각의 기존 target/level/override_of/priority/name/source/value를 `legacy`와 `before`로 보존하고, `after`는 predicate별 원문 field 객체 배열로 만들어 두 common 필드가 덮이지 않게 했다. 관련 충돌3override도 원문 source/claim으로 도달한다. 승인 decision 없는 claim.override는 null이며 역사 override를 projection에 그대로 남긴다.

정상 rename은 common_adverse_effects2/common_side_effects1/serious_adverse_effects2 원천필드를 독립 대조했다. 기존 source_text는 실제 원문의 삽입순서 기반 last-write 결과와 일치하는 역사 before로 검증했고 이를 원문 정본으로 쓰지 않았다. onset_duration.peak_effect→peak 규칙은 고정 source table과 current keys로 회귀 검사했다. 이번1394 안전 field에 onset 필드는 없으므로 신규 안전 이관 건수에 더하지 않았다.

원문 missing/null/[]/false/빈문자열은 보존한다. 원문 census(제품·계열·대응·안전 extracted 전체)는 {"empty_array": 4542, "empty_string": 133, "false": 730, "null": 4889, "scalar_value": 37969} 이며 missing은 별도 field_state로 기록했다. 이 집계는 원문 값 검사 수이며 임상 사실/검토 수가 아니다.

## 4. 247 coverage와 84필드별 결과

247 제안 키와 baseline_status/proposed_contract를 일대일 그대로 유지했다. 범위 밖163키는 out_of_batch, 신규 typed/raw/source 실적0이다. 이번84는 implemented74, decision 원문보존·무승인8, family.subfamilies needs_design1, family.technique_defaults 제한 registry1이다. 각 field의 제안 type/required/empty/meaning/source/normalization/oracle와 DATA-001 우선 예외는 schema.json·coverage.json에 남겼다. 원문 locator4,576곳은 독립 실제 파일로 검사했다.

아래 typed/raw 수는 원문 행·필드·전송 record별 검사 분모이며 서로 더해 임상 검토수로 해석하면 안 된다. 빌드 export의 result=pending_independent_validation은 builder가 스스로 승인하지 않는 상태이며 실행 판정은 validation.json의 PASS다.

| 제안 필드 | batch 상태 | typed | raw locator | 빈값 |
|---|---|---:|---:|---:|
| product.id | implemented | 395 | 395 | 0 |
| product.revision | implemented | 395 | 0 | 0 |
| product.status | implemented | 395 | 0 | 0 |
| product.label | implemented | 395 | 395 | 0 |
| product.aliases | implemented | 395 | 395 | 120 |
| product.source_refs | implemented | 395 | 395 | 0 |
| product.decision_refs | implemented | 395 | 0 | 395 |
| product.identity_kind | implemented | 395 | 395 | 0 |
| product.license_claim_refs | implemented | 395 | 395 | 0 |
| product.spec_claim_refs | implemented | 395 | 395 | 0 |
| product.company_roles | implemented | 395 | 395 | 95 |
| product.family_mapping_refs | implemented | 395 | 354 | 41 |
| product.line_memberships | implemented | 395 | 36 | 389 |
| product.continuity | implemented | 395 | 756 | 0 |
| family.id | implemented | 27 | 27 | 0 |
| family.revision | implemented | 27 | 0 | 0 |
| family.status | implemented | 27 | 0 | 0 |
| family.label | implemented | 27 | 27 | 0 |
| family.aliases | implemented | 27 | 27 | 3 |
| family.source_refs | implemented | 27 | 27 | 0 |
| family.decision_refs | implemented | 27 | 0 | 27 |
| family.definition_claim_refs | implemented | 27 | 54 | 0 |
| family.subfamilies | needs_design | 0 | 54 | 27 |
| family.technique_defaults | limited_registry | 27 | 27 | 0 |
| family.deferred_refs | implemented | 27 | 27 | 17 |
| snapshot.id | implemented | 5 | 0 | 0 |
| snapshot.source_version | implemented | 5 | 0 | 5 |
| snapshot.files | implemented | 5 | 0 | 0 |
| snapshot.captured_at | implemented | 5 | 0 | 5 |
| snapshot.source_kind | implemented | 5 | 0 | 0 |
| source_record.id | implemented | 23255 | 0 | 0 |
| source_record.snapshot_ref | implemented | 23255 | 0 | 0 |
| source_record.file | implemented | 23255 | 0 | 0 |
| source_record.pointer | implemented | 23255 | 0 | 63 |
| source_record.native_id | implemented | 23255 | 0 | 17773 |
| source_record.raw_value | implemented | 23255 | 0 | 2642 |
| source_record.parent_ref | implemented | 23255 | 0 | 63 |
| source_record.continuity_ref | implemented | 23255 | 0 | 23255 |
| scope.id | implemented | 1002 | 0 | 0 |
| scope.axes | implemented | 1002 | 0 | 0 |
| scope.container_scope_ref | implemented | 1002 | 0 | 1002 |
| scope.statement_qualifiers | implemented | 1002 | 0 | 422 |
| scope.conflicts | implemented | 1002 | 0 | 1002 |
| scope.application_state | implemented | 1002 | 0 | 0 |
| claim.id | implemented | 13399 | 0 | 0 |
| claim.kind | implemented | 13399 | 0 | 0 |
| claim.subject_ref | implemented | 13399 | 0 | 152 |
| claim.predicate | implemented | 13399 | 0 | 0 |
| claim.raw_field | implemented | 13399 | 0 | 0 |
| claim.raw_value | implemented | 13399 | 0 | 2642 |
| claim.normalized_value | implemented | 13399 | 0 | 13399 |
| claim.source_refs | implemented | 13399 | 0 | 0 |
| claim.scope_ref | implemented | 13399 | 0 | 0 |
| claim.mapping_refs | implemented | 13399 | 0 | 0 |
| claim.language | implemented | 13399 | 0 | 13399 |
| claim.variant | implemented | 13399 | 0 | 0 |
| claim.override | implemented | 13399 | 0 | 13399 |
| claim.review_state | implemented | 13399 | 0 | 0 |
| mapping.id | implemented | 2797 | 0 | 0 |
| mapping.source_refs | implemented | 2797 | 0 | 0 |
| mapping.purpose | implemented | 2797 | 0 | 0 |
| mapping.state | implemented | 2797 | 0 | 0 |
| mapping.candidates | implemented | 2797 | 0 | 1486 |
| mapping.selected_refs | implemented | 2797 | 0 | 1517 |
| mapping.rule | implemented | 2797 | 0 | 1403 |
| mapping.scope_ref | implemented | 2797 | 0 | 0 |
| mapping.decision_refs | implemented | 2797 | 0 | 2797 |
| decision.id | source_preserved_no_approval | 0 | 0 | 0 |
| decision.target_refs | source_preserved_no_approval | 0 | 0 | 0 |
| decision.status | source_preserved_no_approval | 0 | 0 | 0 |
| decision.authority | source_preserved_no_approval | 0 | 0 | 0 |
| decision.reason | source_preserved_no_approval | 0 | 0 | 0 |
| decision.source_refs | source_preserved_no_approval | 0 | 0 | 0 |
| decision.decided_at | source_preserved_no_approval | 0 | 0 | 0 |
| decision.supersedes | source_preserved_no_approval | 0 | 0 | 0 |
| attachment.id | implemented | 1242 | 0 | 0 |
| attachment.claim_refs | implemented | 1242 | 0 | 0 |
| attachment.target_ref | implemented | 1242 | 0 | 0 |
| attachment.rule | implemented | 1242 | 0 | 0 |
| attachment.witness | implemented | 1242 | 0 | 1242 |
| attachment.scope_ref | implemented | 1242 | 0 | 0 |
| attachment.application_state | implemented | 1242 | 0 | 0 |
| attachment.resolution_ref | implemented | 1242 | 0 | 1242 |
| attachment.unknown_reasons | implemented | 1242 | 0 | 0 |

family.subfamilies는 typed=[]+needs_design이며 전체 sub_families/sub_family_handling/deferred legacy 원문을 보존했다. stable subfamily key/axis와 purpose ID를 발급하지 않았다. technique_defaults는 실제 step4.nodes의 기존 ID 도달성 및 default/also/role/layer/basis/decided_by 원문 참조 보존까지다. unit96과 technique17을 전수 typed migration으로 세지 않았다.

## 5. 검증·반례·재현·보호

독립 validator는 1,320,125회 원문/타입/참조/필드/원장 검사를 수행했고 실패0·skip0이다. 이 중 원문 contract locator4,576회와 원문 source/claim/다수 메타 검사는 중복 inspection이며 clinical_reviews=0이다. 구현 이관기는 기대값으로 import하지 않았다. export/ledger의 모든 ID 도달성, source occurrence containment, 전체 mapping-ledger2797과 identity-ledger422, source row index와 override target/family도 독립 확인했다.

명시 positive 14개와 negative 35개가 PASS다. 모든 negative는 normalized ID를 다시 계산한 뒤 지정한 원문/의미 진단을 요구했고 normalized-ID 실패0을 확인했다. 원문 claim 삭제/다대일 덮어쓰기·배열순서/빈값/null/false 변조·정상 serious rename 소실·LOSS02 오분류·merge/line parent 발명·ledger 오조인·후보 선택승격·family null 채우기·clinical confirmed·bool 타입오류·끊긴 ref·scope 교집합/중복/explicit 은폐/무관 parent·null rule 사유삭제·rule id/version/hash 위조·권한/원천결정 위조·design hash의 normalized ID 오염·witness/registry 변조를 탐지했다.

immutable pilot 회귀는42사례·146combo(단일21/쌍119/3항6)·note7·언어claim5·duration원문2대안을 직접 읽어 검사했다. 원본 runner를 실행하거나 원본 산출물을 만들지 않았다. 이 수는 이번 이관 분모에 합산하지 않았다.

실제 builder를 새 tmp output에서2회 실행해 deterministic export13개와 output-manifest의 SHA256/bytes가 기존 candidate와 같음을 확인했다. 69입력을 candidate/tmp의 domain/logical-key 경로로 물리 복사하고 같은 manifest bytes와 --locator-root로 실제 재독해한 결과도 동일하다. 실제69개 read locator는 run-metadata에 남겼다. 이동 후 source tamper와 새 manifest rebaseline은 각각 nonzero로 거부했다. 기존 candidate를 다르게 덮어쓰는 CLI는 제공하지 않는다.

audit-only/source-data/schema/rule/label/행재정렬의 수명 시험6개도 PASS다. audit/source hash 및 schema/rule lifetime 시험은 source 파일을 바꾸거나 새 판을 승인하지 않고 실제 candidate graph와 manifest를 메모리에서 교란·ID재계산한 probe다. audit hash만 바뀌면 audit snapshot만 바뀌고 데이터 source_refs/normalized ID는 불변이며, semantic source hash/판 변경은 관련 normalized ID를 바꾼다. 행순서·label 변화는 native entity ID를 바꾸지 않고 source/내용 revision의 수명과 구분한다. 실제 입력 이동 불변은 별도의 실빌드로 증명했다.

보호 대상 1607파일을 시작/끝 SHA256+bytes로 대조해 변경0이다. 원본 정본·기존 pilot/review/design/semantic/스펙/원장/manifest는 그대로다. 코디 mutable 진행로그는 별도 운영 상태이며 builder 입력이 아니다. 모든 tmp 결과는 지웠다. 네트워크/모델/설치/DB/서버/앱·Hub/env/컨테이너/하위worker/commit/push/PR/Gold/정본전환은 실행하지 않았다.

재실행 명령은 [migration README](../silver-batch1-migration/README.md)에 원문 그대로 있다. 기존 candidate가 있으므로 첫 build 명령의 명시 거부가 정상이며, 재생성은 check_reproducible.py가 fresh candidate/tmp/run-N에서 수행한다. validator/test/repro CLI는 실패 시 nonzero다.

## 6. 남은 단계

**P5 별도 독립 reviewer의 source-direct candidate 검수는 TODO다.** 이번 validator는 builder와 코드·원문 oracle를 분리한 구현자 검증이며 별도 reviewer의 독립 검수를 대체하지 않는다. 정본전환/소비자 호환성/backup·승인자/서비스 활성화·Gold publication은 별도 권한과 계약이 필요하며 실행하지 않았다. concern/combo/site/technique/unit/package/condition/literature 전체 의미 이관, 허가 최신성 및 임상 적용/제품선택 판단, subfamily/purpose 설계는 후속이다.

이 candidate를 활성 입력으로 사용하지 않으면 이전 정본이 그대로 유지되는 것이 현재 단계의 되돌리기다. 자동 copy/apply/canonical 전환 옵션은 없다.
