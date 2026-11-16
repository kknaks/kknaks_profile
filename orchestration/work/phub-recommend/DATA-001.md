---
id: DATA-001
title: "실버 데이터 구조와 원천 보존 계약"
status: draft
product: procedure-hub
created_at: 2026-11-03
updated_at: 2026-11-03
---

# DATA-001 — 실버 데이터 구조와 원천 보존 계약

작성일 2026-11-03 · 판 `data-001/2` · 상태: 구현 전 계약, 독립 검수 대기.

## 1. 정본의 권한과 채택 범위

이 문서는 이 작업의 **데이터 구조 계약 정본**이다. 사용자 승인 [작업 방향](../../../reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md)의 단계4를 준비한다. [HTML](silver-entity-graph-design/index.html)·[design.json](silver-entity-graph-design/design.json)은 제안 시점 증거로 보존한다. 기존 SPEC-005/006·WORK-011/012의 API·탐색 계약을 다시 쓰거나 활성 데이터 권한을 바꾸지 않는다.

[폐쇄 검수](silver-pilot-closeout-review/report.md)가 검증한 source/ID/typed refs/scope/rule 계약만 부분 채택한다. pilot의 42사례·entity27개는 전체 이관 실적이 아니다. entity 실물은 product4/family4/unit11/concern7/evidence_statement1이며 `id/type/native_id/source_refs` 네 칸뿐이다. 여기서 제시한 typed 속성은 구현 전이고 clinical 승인도 아니다. site는 schema에 있어도 실물0이다.

전체 기준은 [coverage.json](silver-pilot-closeout-review/coverage.json)의 **25논리타입·247필드**다. pilot검증78/원문raw보존만33/계약만71/미구현62/의미미확정3을 그대로 유지한다. 이 문서와 [필드 계약](silver-data-contract-batch1/field-contract.json)의 planned 상태가 기존 상태를 소급 대체하지 않는다. 새 schema 제약·positive fixture 없는 축, parent 합성, witness 및 임상 적용은 검증됐다고 표시하지 않는다.

계약의 우선순위는 DATA-001 본문 → 필드 계약의 `transform`·명시 예외 → `proposed_contract`(제안 당시 타입/필수/빈값) 순이다. 제안 당시 비nullable이 근거 부족을 표현하지 못하면 null+field_state 허용을 명시한 이번 예외를 적용하며, 다음 구현자는 새 schema판에 그 차이를 선언해야 한다. 기존 pilot schema를 수정해 이 차이를 숨기지 않는다.

## 2. 원천 판·locator와 identity

| 구분 | 계약 |
|---|---|
| domain / collection | `raw21` / `procedure-hub/raw21`(21), `generated-silver` / `procedure-hub/generated-silver`(18), `research-artifact` / `procedure-hub/research-artifact`(11), `decision-artifact` / `procedure-hub/decision-artifact`(13), `audit-artifact` / `procedure-hub/audit-artifact`(6). 각 집합은 [collections.json](silver-data-contract-batch1/contract-fix/collections.json)의 전체 membership이다. |
| logical_file_key | collection 루트 상대 전체 POSIX 경로. basename·내용만으로 병합 금지. 같은 파일명도 domain이 다르면 별개다. |
| file | 물리 locator. 이동으로 바뀌어도 logical key·내용판이 같으면 source ID는 유지한다. |
| manifest | 명시 collection 전체의 `[logical_file_key,full SHA256]`를 key로 정렬한다. bytes·물리경로·source_kind·source_version은 감사 메타다. raw21은 실제21파일 전체이며, 모든 collection은 새 [입력 manifest v2](silver-data-contract-batch1/contract-fix/input-manifest.v2.json)의 전체 집합이다. 이전69파일을 재분류하고 `_RESUME.md` 물리입력만 동결본으로 대체했다. 이전 manifest는 변경하지 않는다. |
| snapshot ID | `snap:` + SHA256(canonical JSON(`[domain,collection,sorted_manifest]`)). JSON canonical은 UTF-8, ensure_ascii=false, sort_keys=true, separators=(comma,colon), NaN 금지로 고정한다. |
| source occurrence | `src:` + SHA256(canonical JSON(`[snapshot_id,logical_file_key,RFC6901_pointer]`)). 행·필드·잎은 각각 occurrence다. raw_value는 해당 pointer 값과 deep equal이어야 한다. |
| native entity | 기존 `namespace:native_id`: product:ledger_id, family:M/N, unit_procedure:U5-ID 등을 유지한다. 표시 이름·배열순서·허가번호로 재발급하지 않는다. source.native_id는 실제 원문행 값이며 ID 모양으로 종류를 추정하지 않는다. |
| 원천 재정렬 | 파일 hash/snapshot/occurrence는 새 판이다. entity native ID는 유지한다. 내용만 같다고 이전 occurrence를 자동 continuity로 연결하지 않는다. |
| normalized revision | scope/mapping/claim/relation/decision/resolution/attachment 등은 `type-prefix:` + SHA256(`[record_schema_version,mapping_rule_revision,id제외 canonical payload]`). source/entity와 수명이 다르다. entity.revision은 내용판1부터 append-only이며 과거 이력을 만들어 넣지 않는다. |

normalized refs를 dependency 순으로 갱신한다. scope→mapping→claim(variant parent 먼저)→relation/note→decision→resolution→attachment가 pilot 검증 범위다. 새 batch에서 entity/mapping을 대상으로 하는 decision이 역참조할 때 순환을 만들지 않는다. 승인근거 원문을 먼저 source_record로 고정한다. 이번 batch의 새 decision target은 stable entity ID로 제한하고, 그 decision을 mapping/claim이 참조하게 한다. mapping/claim 자체에 대한 정규화 decision은 역참조 순환이 없다는 별도 positive가 마련되기 전에는 생성하지 않고 원문/미정으로 보존한다. 순환 content hash를 임의 반복 계산해 수렴시켜서는 안 된다. 정확한 dependency/union은 구현 schema에 선언하고 정·부 반례로 검증한다.

entity의 type/native_id, snapshot의 domain/collection/files[].logical_file_key, source_record.logical_file_key, normalized record의 schema/rule revision은 247 제안필드 밖의 **검증된 core 전송 확장**이다. design.json hash는 감사근거이며 normalized ID 입력은 아니다. schema/rule판 변경은 normalized ID에 반영한다. collection 이동만으로 새 entity/occurrence를 발급하지 않는다.

alias는 `(namespace,snapshot_ref,old_id) → ID 집합`이다. 다수면 ambiguous이고 첫 항목을 택하지 않는다. source parent는 실제 JSON containment, continuity는 증거 있는 이전판 연결, scope parent는 원문 context다. 셋을 혼용하지 않는다.

과거 허가/API/KPIC/웹 조사값은 raw21 원문이라고 부르지 않는다. step1 각 연구 JSON·고정본·apply-log·gate 근거를 실제 file/hash/pointer로 남기고, 그 안의 URL/질의문은 역사적 인용 문자열로 유지한다. artifact가 없으면 `unresolved` 사유와 인용만 보존한다. 새 외부조회나 최신 허가 인증은 하지 않는다. snapshot.captured_at·evidence_source.verified_at은 실제 시각 근거 없으면 null이다.


### 2.1 입력판 보완과 파일 메타

[계약 보완 보고](silver-data-contract-batch1/contract-fix/report.md)와 [reconciliation](silver-data-contract-batch1/contract-fix/reconciliation.json)은 CR-H1~M1의 이번 결정이다. 변경되는 `_RESUME.md`는 builder가 직접 읽지 않는다. 승인된 현재 진행기록 bytes는 `contract-fix/frozen-inputs/coordinator-progress-2026-11-03.md`로 동결했고 decision-artifact의 logical key는 `frozen-inputs/coordinator-progress-2026-11-03.md`다. 코디는 원문·데이터를 바꾸지 않는 이 현재판 입력채택을 브리프에서 승인했다. 이전 expected hash와 manifest는 별도 보존하되 이전 원본 bytes는 미확보이며 이전판 diff/복구를 주장하지 않는다. 이름·임상사실 변경 근거로 로그를 단독 사용하지 않는다. family.name_basis와 실제 원문/현재값/결정 문맥 대조는 reconciliation에 남긴다. 운영 로그의 이후 수정은 frozen 입력에 영향을 주지 않는다.

감사전용 design/coverage와 구현 provenance .py는 audit-artifact로 분리한다. 현재 HTML은 입력 membership 밖이며 향후 채택하면 audit collection에만 추가한다. 각 collection의 snapshot은 위의 같은 공식을 독립 적용한다. audit snapshot/manifest hash는 basis 링크로 보존하되 semantic source snapshot의 membership/hash 및 normalized record payload에는 전파하지 않는다. audit refs는 별도 감사 sidecar에 둔다. 실제 rule fingerprint는 mapping_rule_revision/rule payload에 유지하므로 code/rule 변경을 audit-only 변경이라고 숨기지 않는다. source_refs는 normalized payload에 계속 포함한다. source-data hash 변경 → 해당 snapshot/occurrence와 이를 참조하는 normalized ID 변경; audit-only hash 변경 → audit snapshot만 변경, unchanged-data occurrence와 normalized ID 불변이다.

collection snapshot.source_kind는 collection의 역할 enum(raw_snapshot/generated/research/decision/audit)이다. audit는 제안 당시 enum에 대한 명시 schema 확장이며 proposed_contract 원본은 그대로 보존한다. collection source_version은 별도 선언판이 없으므로 null+source_version_reason이며 임의 멤버 version을 사용하지 않는다. 파일별 실제 원천 종류와 판은 files[].meta에 source_kind, version_state(missing/null/value), source_version_raw, source_version_type, version_pointer, version_reason으로 보존한다. JSON top-level /version의 정수/문자열/null을 변환하지 않으며 missing은 version_state=missing+reason으로 구분한다. source_version_raw=null만으로 missing과 명시 null을 합치지 않는다. text/.py 및 JSON root 배열은 top-level version missing이다. 이 메타는 원본 byte hash 검증으로 보호하며 collection ID의 별도 scalar 입력으로 추가하지 않는다. 파일 원문 version 변경은 파일 hash 변경을 통해 ID에 반영된다.

## 3. typed refs와 상태

모든 ref는 schema와 별도 ref-contract에 source/target union, 필수/nullable, minItems, 중복허용, 도달성을 선언한다. prefix만 맞고 대상이 없거나 타입이 다른 ref는 오류다. mapping.candidates/selected, claim.subject/source/scope/override, entity의 모든 claim/mapping refs, decision.target/supersedes, attachment.target/witness/resolution까지 검사한다. 외부 registry 참조는 파일/hash·native ID 목록이 고정된 제한적 참조로 구분하며 해당 엔터티 전수 이관 실적에 더하지 않는다.

rule.id/version, cases.evidence_refs literal, expansion native ID는 graph record ref가 아니다. source_record.raw_value 안의 기존 ID 문자열도 자동 graph ref로 변환하지 않는다. claim.subject는 이번 entity|null로 제한하고 원문 occurrence는 source_refs로 둔다. 미정 subject=null이면 근거 mapping이 필요하다.

| 상태 축 | 의미 |
|---|---|
| entity.status | active/pending/retired/merged/split은 데이터 수명. 허가 status·recommendable·active 원값은 독립 보존한다. |
| mapping.state | exact/rule_mapped/ambiguous/unresolved/excluded/compatible_candidate/selected는 목적별 대응. membership, unit_compatibility, 실제 제품선택은 별개다. |
| review_state | unreviewed/staff_check/confirmed/source_conflict는 원천 검토. exact identity가 임상 confirmed를 뜻하지 않는다. |
| field_state sidecar | owner_ref/field/state/raw_refs/reason. value, not_declared, unresolved, needs_design, not_applicable을 구분한다. JSON missing/null/[]/false/빈문자열의 원상태도 기록한다. |

`needs_design`은 schema 의미·ID 설계가 아직 없다는 뜻이며 원천 미기재/임상 미정/비적용과 다르다. []는 관측한 명시 빈 목록 또는 계약상 아직 생성하지 않은 결과이고, 전체적용·안전·동치·승인을 뜻하지 않는다. 후자의 경우 상태·사유·raw_refs가 필수다.

## 4. scope 어휘와 표현 한계

본설계 axes는 product/family/subfamily/site/technique/ingredient/purpose/concern/patient/language/route/time이다. pilot은 product/family/site/unit_procedure/concern/target/container/site_relation/statement_site/patient_conditions의10축이다.

| 본설계 ↔ pilot | 대응과 제한 |
|---|---|
| product/family/site/concern | 같은 이름의 entity_refs 축. 값 종류·원문 문맥 검증을 만족할 때만 재사용한다. site의 실물 entity0을 전체 registry 완료로 읽지 않는다. |
| patient ↔ patient_conditions | 의미 alias 후보일 뿐 자동 치환 불가. pilot 값종류 none·raw 제한이며 환자조건 사전 refs를 이미 지원한다는 뜻이 아니다. |
| subfamily/technique/ingredient/purpose/language/route/time | pilot 직접축 없음. 원문 qualifiers로 보존할 수 있으나 typed 축값으로 바꾸려면 별도 schema/positive 검증 필요하다. language는 claim.language와 혼동하지 않는다. |
| unit_procedure/target | 본설계에 직접축 없음. 원문 소유/대상 refs로 보존하며 product나 purpose로 rename 금지. |
| container | 본설계 container_scope_ref와 동의어 아님. pilot은 cc/cc_group 원문 역할 슬롯 source_literals다. |
| site_relation | same_site/different_site relation_conditions. site entity ID로 치환 금지. |
| statement_site | 값종류 none; raw 문장과 conflict/qualifiers 보존. 확정 부위축으로 승격 금지. |
| declared ↔ explicit | 값·원문근거가 있는 경우만 상태 alias. 선언만 있고 값이 없으면 자동 변환 불가. |
| unresolved ↔ unknown | 원문 해석 미정 의미로 대응 가능하되 후보·근거 유지. 필드의 needs_design과 별개다. |
| not_declared / not_applicable | 어휘는 같으나 실제 검사한 원문/비적용 근거가 필요. missing만 보고 비적용으로 채우지 않는다. |

각 axis는 knowledge/included/excluded/raw_refs/value_kind를 갖는다. explicit은 최소 한 포함/제외값과 원문근거, not_declared/not_applicable은 빈 값과 근거, unknown은 근거 있는 후보값 또는 빈값을 허용한다. 포함·제외의 교집합은 비어야 하며 각각 중복없는 집합이다. container만 원문 [cc,cc_group] 두 역할이 실제로 같고 해당 complaint raw_refs와 정확히 일치할 때 중복3개를 유지한다. 임의 반복 예외는 없다. value_kind=none이면 양쪽은 항상 빈 배열이다.

상충 원문의 포함/제외를 resolved 축에 동시에 넣지 않는다. claim/source별 scope를 분리하고 conflicts+statement_qualifiers에 각각의 원문을 남긴다. 팔자 컨테이너와 목 문장은 원천 충돌 그대로다. unknown이라고 후보를 지우거나, 이미 explicit인 원문축을 unknown으로 낮춰 통과시키지 않는다.

parent는 self/cycle 금지이며 동일 snapshot/logical file/comparison pointer의 procedure 멤버→subtitle context만 검증됐다(실물2개). parent raw_refs와 member raw_refs를 각각 대조한다. 다른 source parent/새 parent/parent를 통한 축 합성은 추가 검토다. 이번 batch는 새 parent 합성을 하지 않는다. pilot의 언어 family=M2·combo cc/cc_group·statement_site unknown 규칙은 해당 source subset의 규칙이며 제품/계열 전체로 복사하지 않는다.

## 5. 원문 claim, override, resolution, attachment

claim은 원문 field/pointer/raw_value를 갖는 원천 주장이다. 정규화 predicate가 같아도 원문 claim ID와 source는 각각 보존한다. normalized_value는 이번 batch null이며 새 임상 normalization·resolution을 만들지 않는다. resolution은 입력 claim 전체/alternatives/scope/policy/output/unknown_branch를 갖는 조회값이고, conservative가 clinical_consensus=true를 뜻하지 않는다.

원문 safety/aftercare를 환자별 적용 승인으로 해석하지 않는다. source_text는 원천필드 claim에서 파생된 조회 호환값이며 유일 정본이 아니다. `source_text → side_effect_override`는 원래 claim_refs/source_refs·raw field와 연결해야 한다. 기존 level, override_of(family ref), priority, source/id/name 및 rule 근거를 보존한다. 제품×계열×키하위 > 제품×계열 > 단위시술 > 단위시술후보 > 계열의 기존 우선순위와 수치 priority를 대조하고 자동 재정렬/새 우선순위를 부여하지 않는다. 후보는 후보이며 안전 claim의 임상 적용은 unknown이다. 합병증 노드를 이 override로 덮지 않는다.

v1/v2 차이는 다음처럼 유지한다.

- **LOSS02는 product가 아니라 unit_procedure:U5-016**이다. 원문 ID가 보톡스처럼 보여도 ID 접두/명칭으로 product를 발명하지 않는다.
- mapping.rule은 nullable이다. null일 때 실제 이유를 `reason`에 필수 보존하고, 존재하면 id/version/code_sha256을 실제 규칙판에 대조한다. 원문이 없다고 규칙을 만들어 채우지 않는다.
- relation.field_conditions.first는 a/b/explicit_no_required_order/not_declared/unknown을 구분한다. v2 schema의 bool|null 허용이 이 의미들을 bool로 축약할 근거는 아니다. 조건별 options는 각각 scope_ref/value/raw_ref를 갖는다. same_day는 다른 조건이며 days의 독립 원문 없으면 null, interval은 수치 정본이다.
- override는 claim/source/scope/decision/override_of 연결을, pair 파생은 원문 parent/relation/source 구성·arity·rule provenance를 보존한다. singleton21에서 pair0, n-ary6을 무조건 한 pair로 만들지 않는다. 기존 note7의 실제 대응 claim은 유지한다.

attachment는 검색 부착 경로이며 소유권·적용승인과 다르다. pilot-preserve-source/1은 subject=target/동일 scope/unknown/빈 witness/실제 duration resolution 한정이다. 그 id/version으로 batch의 새 동작을 주장하지 않는다. 이번 candidate용 `batch1-source-preservation/2`는 검증된 단일 owner=subject=target·unknown·witness=[]·resolution_ref=null일 때만 attachment를 생성한다. 새 witness가 필요하면 mapping/source/relation/member/component 도달성과 target 대응을 별도 positive로 검증한다.


안전 원문 보존 분모는580행/1,394field/4,170scalar잎 전부다. attachment 분모는 별도 eligible claim 집합이다. subject=null, 후보, owner 미확정, 이번 범위 밖 entity이면 claim을 보존하되 attachment는 생성하지 않는다. mapping 및 source-row-index에 source_refs/claim_refs/mapping_refs와 attachment_state=not_created, attachment_reason(owner_unresolved/candidate_only/out_of_batch_entity)을 필수 기록한다. mapping.candidates는 기존 {target_ref,role,basis,exclusion,scope_ref} 객체 배열(0..n)이다. target_ref의 허용 union은 product|family|검증된 제한 unit registry ref|null이며 null이면 candidate.raw_refs와 reason이 필수다. 도달 가능한 entity가 없는 원문후보는 target_ref=null+raw_refs+reason으로 남기거나 candidates=[]+mapping.source_refs+reason으로 원형 보존한다. mapping.selected_refs는 entity/제한 registry ref 배열(0..n)이며 미선택은 []다. 후보를 selected로 올리지 않는다. 새 package/unit owner를 발명하지 않는다.

원문 field마다 eligible 또는 not_created 중 정확히 하나를 기록하고 두 집합은 서로소이며 합집합은 전체1,394field다. eligible의 각 claim은 최소 한 동일 owner attachment로 도달하고 not_created는0개이며, 보존 coverage는 두 집합 모두에서 원문 deep equal이어야 한다. 실제 후보19행+원문보관37행=56행의132field는 정상 미부착 positive다. 나머지524행/1,262field를 자동 eligible로 간주하지 말고 단일 owner 도달성을 검증해 추가 미부착 사유/분모를 보고한다. 단일 owner 확인도 임상 적용승인이 아니다.

규칙 fingerprint는 선언만으로 통과하지 않는다. 독립 고정 기대값과 실제 파일 bytes·source version을 대조한다. pilot resolution D9-3은 step9-decisions.version=1→문자열, 실제 step9-apply.py SHA256, 실제 decision_ref·날짜·사유·대상까지 exact 대조했다. attachment는 ref_contract.py 고정 선언·ref-contract.json·실제 build.py/contract.md fingerprint를 교차검사했다. 새 batch의 규칙 기대 hash도 builder output에서 읽어 자신의 정답으로 쓰지 않는다. design hash 변경만으로 identity를 바꾸지 않는다.

## 6. 전체25타입의 소유와 Gold 대응

13 entity 타입은 Gold 노드 후보이며 나머지는 source/record/embedded 속성이다. 모든 entity를 연관된 임상 fact의 자동 상속 소유자로 확장하지 않는다. 기존 Gold 노드 표면의 common field/own_properties/claim_refs에 연결할 수 있다는 구조 대응이며, 아래 표는 Gold 구현·publication 승인 목록이 아니다.

| 타입 | 소유역할 / Gold 대응 | 필드 수·기존 상태 | 이번 묶음 |
|---|---|---|---|
| product | 허가·업체·규격을 갖는 제품 identity; 계열과 시술은 별개; 독립 Gold 노드 후보 | 14 / {'pilot검증': 2, '계약만': 3, '원문raw보존만': 7, '미구현': 2} | typed 전개 계약(구현 전) |
| family | 무엇을 하는 시술인지 정의하는 27계열; 독립 Gold 노드 후보 | 11 / {'pilot검증': 2, '계약만': 3, '원문raw보존만': 5, '미구현': 1} | typed 전개 계약(구현 전) |
| subfamily | 계열 내부 축의 값; 단독 노드 신설 없이 계열에 내장; 독립 Gold 노드 아님; 참조/속성 | 6 / {'의미미확정': 2, '원문raw보존만': 2, '계약만': 2} | 후속; 기존 원문/관계 보존 |
| site | 몸 겉에서 가리킬 수 있는 자리; 문장 속 scope와 별개; 독립 Gold 노드 후보 | 11 / {'계약만': 4, '미구현': 7} | 후속; 기존 원문/관계 보존 |
| technique | 큰 기법·세부 기법; 층/도구/근육은 속성 값; 독립 Gold 노드 후보 | 12 / {'미구현': 7, '계약만': 5} | 후속; 기존 원문/관계 보존 |
| unit_procedure | 원천에 있는 최소 시술 조합; 전 조합 생성 금지; 독립 Gold 노드 후보 | 13 / {'pilot검증': 2, '계약만': 3, '원문raw보존만': 8} | 후속; 기존 원문/관계 보존 |
| package | 상업 이름 있는 시술 묶음; 추천 조합과 별도 identity; 독립 Gold 노드 후보 | 10 / {'미구현': 6, '계약만': 4} | 후속; 기존 원문/관계 보존 |
| concern | taxonomy 3층 및 결정 노드; 이름이 같아도 원장행은 분리; 독립 Gold 노드 후보 | 12 / {'pilot검증': 2, '계약만': 3, '원문raw보존만': 5, '미구현': 2} | 후속; 기존 원문/관계 보존 |
| purpose | 시술이 하는 일; 고민과 동의면 독립 노드를 만들지 않음; 독립 Gold 노드 후보 | 9 / {'의미미확정': 1, '계약만': 4, '미구현': 4} | 후속; 기존 원문/관계 보존 |
| combo | 79개 원천별 추천 구조; 구성·비교·업그레이드·스케줄 역할 구분; 독립 Gold 노드 후보 | 12 / {'미구현': 6, '계약만': 5, '원문raw보존만': 1} | 후속; 기존 원문/관계 보존 |
| check_condition | 임신·약물·체질 등 조건 사전; 준비/상담은 제외; 독립 Gold 노드 후보 | 9 / {'미구현': 4, '계약만': 5} | 후속; 기존 원문/관계 보존 |
| complication | 현행 CX 원천별 이상결과 노드 유지; 흔한 반응과 구분; 독립 Gold 노드 후보 | 10 / {'미구현': 5, '계약만': 5} | 후속; 기존 원문/관계 보존 |
| evidence_statement | 119 ST 근거 묶음을 검색 가능한 노드로 유지; 독립 Gold 노드 후보 | 13 / {'pilot검증': 2, '계약만': 5, '원문raw보존만': 5, '미구현': 1} | 후속; 기존 원문/관계 보존 |
| evidence_source | 출처 identity와 snapshot metadata; 외부 최신성 조회 안 함; 독립 Gold 노드 후보 | 11 / {'미구현': 4, '계약만': 7} | 후속; 기존 원문/관계 보존 |
| component | n-ary 구성의 역할·선택·수량을 보존; 독립 Gold 노드 아님; 참조/속성 | 11 / {'계약만': 3, '미구현': 8} | 후속; 기존 원문/관계 보존 |
| snapshot | 원문21 및 외부 조사판을 독립 고정; 독립 Gold 노드 아님; 참조/속성 | 5 / {'pilot검증': 3, '계약만': 2} | source 보존 공통 record(구현 전) |
| source_record | 이름 아닌 snapshot+file+pointer로 행/잎을 식별; 독립 Gold 노드 아님; 참조/속성 | 8 / {'pilot검증': 6, '계약만': 2} | source 보존 공통 record(구현 전) |
| scope | 소유·container 범위·문장 조건을 분리; 독립 Gold 노드 아님; 참조/속성 | 6 / {'pilot검증': 6} | source 보존 공통 record(구현 전) |
| claim | 주제-술어-값과 provenance; 노드 자체 속성과 분리; 독립 Gold 노드 아님; 참조/속성 | 14 / {'pilot검증': 13, '계약만': 1} | source 보존 공통 record(구현 전) |
| relation_claim | 쌍/자기쌍/n-ary/단일 속성·조건별 시간 주장; 독립 Gold 노드 아님; 참조/속성 | 10 / {'pilot검증': 8, '계약만': 2} | 후속; 기존 원문/관계 보존 |
| mapping | 표현·제품·계열·unit의 후보와 실제선택을 구분; 독립 Gold 노드 아님; 참조/속성 | 9 / {'pilot검증': 8, '계약만': 1} | source 보존 공통 record(구현 전) |
| decision | 검토·규칙 승인·질문·철회를 append-only로 보존; 독립 Gold 노드 아님; 참조/속성 | 8 / {'pilot검증': 7, '계약만': 1} | source 보존 공통 record(구현 전) |
| resolution | 여러 주장을 정책으로 접은 view; 원문 합의 아님; 독립 Gold 노드 아님; 참조/속성 | 9 / {'pilot검증': 9} | 후속; 기존 원문/관계 보존 |
| attachment | owner와 조회 노드를 분리; 부착은 적용 승인 아님; 독립 Gold 노드 아님; 참조/속성 | 9 / {'pilot검증': 8, '계약만': 1} | source 보존 공통 record(구현 전) |
| value_dictionary | 층·도구·근육·펄스·박피·운영·회복·severity 등의 코드; 노드 증식 방지; 독립 Gold 노드 아님; 참조/속성 | 5 / {'미구현': 5} | 후속; 기존 원문/관계 보존 |


## 7. 첫 묶음의 필드별 계약

대상은 product14 + family11 + 이번 사용 공통59 = **84 제안필드**다. 나머지163은 이번 typed 이관 대상이 아니며 기존 coverage 상태를 보존한다. [field-contract.json](silver-data-contract-batch1/field-contract.json)은 각 필드의 제안 type/required/default/empty_unknown·검증된 current/source file+pointer·변환·출처·baseline 상태·oracle을 담는다. concrete current locator는 배열 첫8개의 예시만으로 끝내지 않고 제품/계열 직접필드4,576곳을 추가 열거했다. DERIVED는 원문 칸이 아니라 고정 manifest/변환에서 계산하는 새 메타이며 원천값이라고 주장하지 않는다.

공통 oracle은 원문 pointer deep equality + 아래 변환의 독립 재계산 + 타입/ref 도달성이다. source metadata는 manifest/ID 공식에서 재계산하고, field별 정규화는 원장/source와 직접 대조한다. 구현기가 생성한 typed 출력만 다시 읽는 자가대조는 oracle이 아니다. 필드 계약의 baseline source_refs는 당시 pilot subset 근거이고 `exact_current_locators`는 이번 전체 current field 근거다. raw21 연결을 추가로 확인하지 않은 current 값은 current_silver로 유지한다.

### 7.1 제품·계열의 모든 제안필드

아래 표의 필수/빈값은 제안 계약이며 본문과 transform의 null/needs_design 예외가 우선한다. source row 전체, 원천 추적, typed field를 함께 보존해야 한다. 제안필드에 없는 ledger_name/name_basis, license.status/reason/recommendable, photo_ids, segment, evidence/open/gate/change_vs_draft, dedup/shared_license_with/line_children/recheck/use_mismatch/weak_link 등도 source_record에서 누락하지 않는다. 이 부가 원문을 새 임상 속성으로 확대 해석하지 않는다.

| 필드 | 타입 / 필수 / 빈값 | 정확 current/source 선택규칙 | 변환·검증 oracle | 기존 coverage |
|---|---|---|---|---|
| product.id | string / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.ledger_id | product: + items[i].ledger_id; native_id 원값 병기; rename/reorder 시 동일 ID; oracle=원값/변환/ref 독립 대조 | pilot검증 |
| product.revision | integer>=1 / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | DERIVED: candidate 최초 내용판 1; 과거판이라고 소급하지 않음; 내용 변경시 append-only +1 | candidate 최초 내용판 1; 과거판이라고 소급하지 않음; 내용 변경시 append-only +1; oracle=원값/변환/ref 독립 대조 | 계약만 |
| product.status | active / pending / retired / merged / split / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | DERIVED: merged_into 있으면 merged, moved_to 있으면 retired, 그 외 active=true면 active, 불일치/active=false 사유없음은 pending+진단; 임상 승인과 무관 | merged_into 있으면 merged, moved_to 있으면 retired, 그 외 active=true면 active, 불일치/active=false 사유없음은 pending+진단; 임상 승인과 무관; oracle=원값/변환/ref 독립 대조 | 계약만 |
| product.label | string / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.2_names.display_name | 2_names.display_name 원문 복사; 누락/빈 문자열은 오류; ledger_name을 대체명으로 추정하지 않음; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| product.aliases | array<{text,lang,source_ref,state}> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.2_names.search_names | 2_names.search_names 각 {name,lang}를 {text,lang,source_ref,state=unreviewed}로 변환; 한/영→ko/en 별도 코드표, 원 lang 보존; ledger_name은 별도 source claim, 동치 승인 금지; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| product.source_refs | array<source_record.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.* | items[i] 발생레코드 + 필드별 연구/결정 occurrence 연결; raw21 대응은 실제 ID/locator 일치할 때만 연결; oracle=원값/변환/ref 독립 대조 | pilot검증 |
| product.decision_refs | array<decision.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::basis/ items.*.gate / items.*.open / items.*.change_vs_draft; step1-apply-log.json (decision native alias, actual occurrence required); step2-families.json::decision / families.*.name_basis | items[i] gate/change_vs_draft/open 및 apply-log의 실제 결정근거를 locator로 연결; 텍스트 내 D번호만으로 승인 decision 생성 금지; oracle=원값/변환/ref 독립 대조 | 계약만 |
| product.identity_kind | string / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.1_identity | 1_identity.kind 원문 string 유지; basis/basis_type을 claim/raw source로 보존; 제품·라인·장비·메뉴·확인불가를 임상추정으로 통일하지 않음; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| product.license_claim_refs | array<claim.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.4_license | 4_license 전체(JSON) 및 각 licenses/history/reference 원문 occurrence→kind=license claim; status/reason/recommendable 별도 보존; 현재 유효허가로 재인증하지 않음; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| product.spec_claim_refs | array<claim.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.5_spec | 5_spec 전체(JSON)→operational claim; license/market/market_pricing/note 및 모든 하위 null/빈값 그대로; 용량 환산/새 규격 추정 금지; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| product.company_roles | array<{role,name,original,claim_ref}> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.6_companies | 6_companies의 manufacturer/importer/seller/license_holder/other 배열 각 요소→role=원래 키, name/original 원값, claim_ref; basis/period/role 부가키와 conflicts/company_search_names는 원문 claim으로 보존; 근거 없음은 회사로 확정하지 않고 field_state=not_declared; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| product.family_mapping_refs | array<mapping.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::product_family.* [join ledger_id] | step2 product_family를 ledger_id로 정확 join; family+also_families 후보/선택과 verdict/conflict/evidence_level/pending_director/sub_family_basis 유지; family=null은 unresolved, pending_director는 선택승인 보류; 계열밖5는 excluded 근거 보존; 이름 first-match 금지; oracle=원값/변환/ref 독립 대조 | 미구현 |
| product.line_memberships | array<{parent_product_ref,role,decision_ref}> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.line; step1-products.json::lines | items[i].line 및 lines 전체를 대조; 명시 ledger_id/line_row만 parent_product_ref로 연결; parent_line 문자열/허가번호만 있는 품목은 원문 claim+unresolved mapping; item=미정 보존; decision_ref 없으면 nullable+reason, 가짜 승인 금지; oracle=원값/변환/ref 독립 대조 | 미구현 |
| product.continuity | {merged_from:[],merged_into:null / id,moved_to:null / string,split_from:[]} / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::items.*.active; step1-products.json::items.*.merged_from; step1-products.json::items.*.merged_into; step1-products.json::items.*.moved_to; step1-products.json::items.*.moved_note; step1-products.json::items.*.merged_ledger_ids; step1-products.json::items.*.line_children; step1-products.json::items.*.dedup | merged_from/merged_into/moved_to/split_from 원값→namespace refs(제품 target 존재검사); 없는 배열=[]/없는 target=null에 field_state=not_declared 기록; moved_to는 문자열 유지; active만으로 split/merge 발명 금지; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| family.id | string / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::families.*.id | family: + families[i].id; native_id 원값 유지; oracle=원값/변환/ref 독립 대조 | pilot검증 |
| family.revision | integer>=1 / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | DERIVED: candidate 최초 내용판1; 과거 내용판 아님 | candidate 최초 내용판1; 과거 내용판 아님; oracle=원값/변환/ref 독립 대조 | 계약만 |
| family.status | active / pending / retired / merged / split / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | DERIVED: 초기 pending(이관 신규 등록 상태); 기존 name_status는 별도 보존; clinical 승인으로 active 승격 금지 | 초기 pending(이관 신규 등록 상태); 기존 name_status는 별도 보존; clinical 승인으로 active 승격 금지; oracle=원값/변환/ref 독립 대조 | 계약만 |
| family.label | string / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::families.*.name | families[i].name 원문 복사; literature_name/name_status/name_basis는 별도 claim/raw 보존; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| family.aliases | array<{text,lang,source_ref,state}> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::families.*.synonyms | synonyms 문자열별 text/source_ref, lang=null(추정 금지), state=unreviewed; literature_name은 독립 이름 claim; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| family.source_refs | array<source_record.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::families.* | families[i] 전체 occurrence 및 실제 literature_evidence.path가 도달하는 raw21 field occurrence를 구분 연결; oracle=원값/변환/ref 독립 대조 | pilot검증 |
| family.decision_refs | array<decision.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step1-products.json::basis/ items.*.gate / items.*.open / items.*.change_vs_draft; step1-apply-log.json (decision native alias, actual occurrence required); step2-families.json::decision / families.*.name_basis | name_basis/step2 결정근거 실제 artifact locator로 연결; 규칙승인/인적승인 authority 분리; oracle=원값/변환/ref 독립 대조 | 계약만 |
| family.definition_claim_refs | array<claim.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::families.*.definition; step2-families.json::families.*.literature_evidence | definition/literature_evidence 원문별 kind=definition claim; 동치/임상사실 확정하지 않음; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| family.subfamilies | array<subfamily> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::families.*.sub_families; step2-families.json::families.*.sub_family_handling | sub_families/sub_family_handling 원문 전체 보존; stable key/axis 미발급; typed 배열=[]와 field_state=needs_design+raw_refs(없음 의미가 아님); 기존 legacy 관계는 유지; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |
| family.technique_defaults | array<{technique_ref,role,layer,claim_ref,decision_ref}> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step4-techniques.json::family_defaults.* [join family]; step4-techniques.json::nodes.* [resolve id] | step4 family_defaults를 family ID로 join; default/also 기존 ID를 step4 techniques registry에 대조하는 참조만 보존; default_layer/role/basis/decided_by 원문 유지; registry entity를 새 전수이관했다고 주장하지 않음; oracle=원값/변환/ref 독립 대조 | 미구현 |
| family.deferred_refs | array<mapping.id> / True / null 금지; []는 명시 빈 목록이며 안전·승인을 뜻하지 않음 | step2-families.json::families.*.deferred | deferred[]를 source_refs 기반 purpose=classification mapping, state=unresolved, selected_refs=[]로 보존; deferred_to를 entity ID로 바꾸지 않음; oracle=원값/변환/ref 독립 대조 | 원문raw보존만 |


### 7.2 이번 사용 공통필드

각 행의 타입·필수·빈값·원천 locator와 기존 상태는 필드 계약의 동일한 `proposed` 키가 소유한다. snapshot5/source_record8/scope6/claim14/mapping9/decision8/attachment9의59개를 빠짐없이 아래에 명시한다. resolution/relation_claim은 기존 pilot 회귀 의미만 유지하고 이번 신규 전수 record를 만들지 않는다.

| 공통필드 | 원천 또는 생성 규칙 / oracle | 기존 coverage |
|---|---|---|
| snapshot.id | contract-fix/collections.json의 fixed membership별 domain/collection/정렬 [logical_file_key,sha256]로 DATA-001 §2 공식 계산; audit collection은 별도 ID이며 semantic source에 합치지 않는다; oracle=독립 원문·새 manifest·collection·zero-loss 분모 재계산 | pilot검증 |
| snapshot.source_version | 별도 collection 선언판이 없으므로 null+source_version_reason 필수; 개별 파일 version을 collection 판으로 선택하지 않는다; oracle=독립 원문·새 manifest·collection·zero-loss 분모 재계산 | 계약만 |
| snapshot.files | contract-fix/input-manifest.v2.json의 fixed membership 전체 logical_file_key/file/sha256/bytes/meta; 파일별 meta.source_kind/version_state/source_version_raw/source_version_type/version_pointer/version_reason 원형 보존; missing/null/type 구분; raw21 21개; oracle=독립 원문·새 manifest·collection·zero-loss 분모 재계산 | pilot검증 |
| snapshot.captured_at | 실제 수집시각 근거 없으면 null; 파일 mtime/generated_at을 수집시각으로 전용 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | 계약만 |
| snapshot.source_kind | collection 역할 enum: raw21=raw_snapshot/generated-silver=generated/research-artifact=research/decision-artifact=decision/audit-artifact=audit; heterogeneous 파일 종류는 files[].meta.source_kind 원형 보존; oracle=독립 원문·새 manifest·collection·zero-loss 분모 재계산 | pilot검증 |
| source_record.id | snap ID+logical_file_key+JSON Pointer로 src SHA256; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| source_record.snapshot_ref | 해당 물리 파일의 domain collection snapshot ref; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| source_record.file | 명시 input-manifest 물리 locator; logical_file_key 별도 필수 확장; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| source_record.pointer | 실제 RFC6901 pointer; leaf/field/row 보존; 내용이나 ID 검색결과로 임의 유일화 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| source_record.native_id | 실제 원문행 id/ledger_id; 없으면 null; prefix로 종류 추정 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| source_record.raw_value | pointer의 JSON deep equal 원값; missing은 record를 발명하지 않고 field_state에 기록; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| source_record.parent_ref | 실제 JSON containment parent만; normalized scope parent와 별개; 없으면 null; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | 계약만 |
| source_record.continuity_ref | 실제 이전판 대응근거 없으면 null; 이름/content 같음으로 연결 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | 계약만 |
| scope.id | 정규화 scope payload+schema/rule revision hash; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| scope.axes | 원문 소유 product/family/unit와 적용 후보를 구분; DATA-001 §4 축 사전/knowledge/evidence 강제; 안전 문장을 적용 승인으로 확장 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| scope.container_scope_ref | 이번 batch 새 parent 합성 없음=null; pilot comparison 원문 parent는 회귀에서 보존; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| scope.statement_qualifiers | 원문 조건은 raw 문자열+source_ref로 보존; 미해석이면 operator/value=null+needs_source; default 조건 발명 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| scope.conflicts | 원문 container/statement 충돌은 각각 source_ref와 함께 보존; resolved 축으로 합치지 않음; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| scope.application_state | source 보존 scope는 unknown; 명시 소유 identity와 clinical 적용상태 별개; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.id | 원문 field occurrence 포함 immutable normalized payload hash; 같은 predicate 다른 raw_field는 별도 claim; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.kind | 안전=safety, aftercare=preparation, 허가=license, 계열정의=definition, 규격/업체=operational; 분류판 기록; 나머지는 원문보존+미정 진단; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.subject_ref | 검증된 단일 owner entity/제한 unit registry ref|null; 미확정/단위 시술 후보/범위밖 owner=null+mapping 필수; mapping.candidates의 target_ref는 product|family|제한 unit registry|null이며 null은 raw_refs+reason 필수; LOSS02 unit_procedure:U5-016; 임상승인과 별개; oracle=독립 원문·candidate union·미부착 분모 | pilot검증 |
| claim.predicate | 원문 dotted path를 key_normalize 표로 변환; 다대일은 predicate만 공유, raw claim 병합 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.raw_field | 원문 extracted 기준 safety.common_adverse_effects 등 정확 경로 문자열; normalized_key로 덮지 않음; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.raw_value | 원문 field JSON 그대로; 배열 순서/중복/null/[]/false/문자열 유지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.normalized_value | 이번 batch null; source 원문보존에 normalization 완료를 주장하지 않음; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | 계약만 |
| claim.source_refs | 필드 source_record 필수1+; row claim과 field claim은 구분; 다원천 합성 claim 생성 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.scope_ref | 소유/후보/문장 제한을 담은 scope에 연결; 도달성/축값 검증; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.mapping_refs | identity/membership/normalization 용도별 근거 mapping refs; 미확정 owner이면 최소1; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.language | 원문 명시 lang만 코드화; 없으면 null, 문자열만 보고 자동 언어 동치추정 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.variant | 이번 신규 claim of=null/equivalence=unreviewed; 기존 언어 variant 구조는 후속 대상/회귀보존; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.override | step5 override 실제 source id/level/override_of/priority를 원문 safety field claim에 연결; claim_refs/scope/decision/source refs 보존; 결정승인 locator 없으면 null+미정근거 sidecar, 기존 override raw삭제 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| claim.review_state | 신규 unreviewed; 실제 원천 충돌이면 source_conflict; identity exact로 confirmed 승격 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| mapping.id | purpose/source/candidates/scope/rule 포함 payload hash; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| mapping.source_refs | 실제 product_family/line/deferred/override source occurrences; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| mapping.purpose | 계열=membership, 원문 owner=identity, deferred=classification, predicate=normalization; compatibility/selected와 분리; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| mapping.state | 명시 단일 identity exact, 명시 규칙대응 rule_mapped, 후보 다수 ambiguous, 대상미상 unresolved, 제외근거 excluded; compatible_candidate를 selected로 올리지 않음; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| mapping.candidates | 기존 {target_ref,role,basis,exclusion,scope_ref} 객체 배열; target_ref union=product|family|검증된 제한 unit registry|null; null이면 raw_refs+reason 필수. 대상미발급 원문은 null candidate 또는 []+mapping.source_refs+reason으로 보존; 후보를 선택/owner로 승격 금지; oracle=독립 원문·candidate union·미부착 분모 | pilot검증 |
| mapping.selected_refs | 확정 identity/계열 연결만 entity/제한 registry ref 배열; 미선택=[]; 후보/owner미확정은 [] 유지; pending_director/conflict 원래값과 근거 보존; oracle=독립 원문·candidate union·미부착 분모 | pilot검증 |
| mapping.rule | 실제 버전 규칙이면 {id,version,code_sha256}; 비규칙/근거부족은 null+reason 필수; 원본파일 actual hash와 고정 기대값 대조; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| mapping.scope_ref | 해당 source의 소유/후보 scope ref; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| mapping.decision_refs | 실제 승인근거 decision만 연결; 미확정은 []+reason; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | 계약만 |
| decision.id | 원본 namespace/native decision 이름은 legacy alias; normalized payload hash로 record판 식별; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| decision.target_refs | 이번 batch 새 decision은 stable entity target만 허용하고 역참조 순환을 거부; 기존 pilot claims-only 결정은 회귀보존; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| decision.status | 증명된 기존 승인만 approved; 확인요구 needs_source/needs_staff; artifact 존재만으로 approved 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| decision.authority | 실제 reviewer human 또는 고정 policy approved_rule; 증거 없으면 승인 record 미생성+legacy source 보존; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| decision.reason | 실제 원문 사유 복사; 가짜 사유/기본 승인 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| decision.source_refs | 원본 결정 artifact occurrence 1+; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| decision.decided_at | 실제 decided_at만; 없으면 null; 이관시각 대체 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| decision.supersedes | 실제 이전결정 대응만; 없으면 []; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | 계약만 |
| attachment.id | claim+target+scope+rule+witness payload hash; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| attachment.claim_refs | 검증된 단일 owner가 있는 eligible 원문 claims만 대상; 원문1394field 보존 분모와 분리; excluded claim은 mapping/source-row-index의 attachment_state=not_created+reason+source/claim refs 필수; 충돌6field도 원문claim 각각 보존; oracle=독립 원문·새 manifest·collection·zero-loss 분모 재계산 | pilot검증 |
| attachment.target_ref | 검증된 단일 owner와 subject 동일일 때만 발급; subject=null/후보/범위밖 entity는 attachment 자체 미생성; 새 package/unit/제품 적용 발명 금지; oracle=독립 원문·새 manifest·collection·zero-loss 분모 재계산 | pilot검증 |
| attachment.rule | batch1-source-preservation/2: verified single owner only; unknown/witness=[]/resolution_ref=null; 미발급 상태는 mapping/source-row-index로 보존; 실제 구현 fingerprint 별도 고정; oracle=독립 원문·새 manifest·collection·zero-loss 분모 재계산 | pilot검증 |
| attachment.witness | 이번 [] 유지; compatibility로 적용 witness 발명 금지; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | 계약만 |
| attachment.scope_ref | claim과 같은 source scope만; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| attachment.application_state | unknown; source identity exact와 임상 적용승인 분리; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| attachment.resolution_ref | null; 신규 임상 resolution 생성 없음; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |
| attachment.unknown_reasons | source_preservation_only 및 실제 미정사유 비어있지 않게 기록; oracle=independent pointer JSON equality + transform-specific rule + typed ref reachability; generated metadata recompute from fixed input-manifest | pilot검증 |


## 8. 첫 묶음 분모와 알려진 오류의 수용형태

[독립 재집계](silver-data-contract-batch1/results/recount.json): step1.items395(유일 native ID395), active354/inactive41; step2.product_family354(대상 ID집합은 active 제품과 일치), families27. family=null3/pending_director3을 임의 확정하지 않는다. 안전 원문 보존의 분모는 taxonomy modality subcategory items의 extracted521 + modality products59 = **580 source 행**이다. [독립 field oracle](silver-data-contract-batch1/results/safety-field-oracle.json)에서 safety/aftercare 원문 field1,394개·scalar잎4,170개를 고정했다. [override inventory](silver-data-contract-batch1/results/override-inventory.json)는624항목(units248/product_links376)이다. 이 수치는 원문 보존·조회연결 분모이며 임상 사실/승인 건수가 아니다. 이는 안전문장580개나 유효한 환자 안전승인580건이 아니다. safety 미기재 행도 전체 source 행 보존에 포함한다.

[safety-origin-locators](silver-data-contract-batch1/results/safety-origin-locators.json)는580행 각각의 raw taxonomy pointer와 current step5 pointer, raw safety/aftercare 값을 기록한다. 이번에는 521/59의 인덱스와 native ID가 전부 일치함을 직접 확인했다. 다음 구현도 원문 ID/locator를 검증해야 하며 재정렬 뒤 같은 index를 재사용해서는 안 된다.

| collision | raw taxonomy extracted 경로 | current step5 source_text | 반드시 보존할 common field/잎 |
|---|---|---|---|
| M1-1-3 | /modality/0/subcategories/1/items/3/extracted | /extracted/7/source_text | common_adverse_effects3 + common2 |
| auto-2-1774737181584 (LOSS02) | /modality/0/subcategories/2/items/7/extracted | /extracted/25/source_text | common_adverse_effects3 + common2; unit U5-016 |
| M7-P-1 | /modality/6/products/1/extracted | /taxonomy_products/36/source_text | common_side_effects4 + common2 |

기존 common2씩만 남았던 before(총6잎)에 원천별 두 field claim씩을 보존하는 after(6field/16잎, 기존 소실10잎 복구)를 요구한다. 한 normalized predicate의 배열 union으로 원문을 대체하거나 중복 문자열을 삭제하지 않는다. 전체 safety.*와 aftercare의 원문 키/타입/목록 순서/빈값도 보존한다. 정상 `serious_adverse_effects→serious`, `common_*→common`, `onset_duration.peak_effect→peak` rename은 source field를 남긴 채 predicate 변환으로 유지한다. rename 자체를 오류라고 되돌리지 않는다.

side_effect_override는 product_links/units의 기존 대상·source/id/level/family/priority/values를 전부 inventory한 뒤 원문 field claim과 연결한다. 3collision의 override 조회값도 before/after를 별도로 낸다. 중복 predicate를 한 JSON key로 내보내야 하는 호환 조회에서는 원문별 source_value 목록/claim_refs를 별도로 제공하고 원문 정본을 overwrite하지 않는다. 현재 실버 호환성 보장을 위해 기존 출력형식을 몰래 바꾸지 않는다. candidate 전용 다대일 표현을 schema에 명시한다.

## 9. 미정과 후속 경계

코디네이터 ask 응답(이번 Dispatch)은 subfamily.key/axis·purpose.id의 새 stable key 발명을 금지하고 원문/legacy ID·관계를 보존하며 field_state=needs_design으로 유지하는 범위를 확인했다. family.subfamilies의 typed 배열 미발급을 원문에 하위계열이 없다는 뜻으로 쓰지 않는다. 후보 의미는 sub_families의 HA/비HA 등 계열 내부 구분과 sub_family_handling의 제품속성/시술넘김 역할이 섞여 있다는 점이다. 사용위치는 family 내장값·product_family.sub_family·unit key·scope이며 key/axis를 정하면 mapping·refs·revision에 영향이 있다. purpose는 concern과 동의인지 독립 목적 entity인지 경계 및 legacy 사용위치부터 확인해야 한다. 이번 batch는 purpose typed ID를 생성하지 않는다.

technique_defaults는 step4 family_defaults와 nodes의 기존 ID 도달성만 검증하는 제한적 참조 보존이다. 기법 의미 재판정/전수이관은 아니다. typed unresolved 표현은 원문 값과 legacy 관계를 끊지 않게 sidecar로 남긴다.

후속은 concern/CC/combo → site/technique/unit/package → 조건·안전 의미 normalization·문헌·설명 전수 묶음이다. 이번580행 원문보존을 조건/안전 임상 의미 전수승인으로 바꾸지 않는다. 팔자/목, 비교후보, M4→M2 확대, 언어 동치, 실제 verification시각, 보수정책 승인·정본전환 권한은 실제 근거가 확보되기 전까지 유지한다. usable Gold/API/서비스는 이 계약의 산출물이 아니다.
