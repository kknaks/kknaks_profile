# 실물 pilot v2 독립 재검수

Task `task_a4ce5895c0ff` · Dispatch `ctx_31531eed4ff1` · 2026-11-03 KST

## 판정

**FAIL — 지정 회귀 반례는 해결됐지만, scope 의미와 규칙판 검증의 잔여 결함으로 단계3 전체 수용 및 무조건적인 정본 채택은 보류한다.** 기존 원문이 훼손됐거나 실제 임상 적용이 승인됐다는 뜻은 아니다. 검수 작업은 완료했으며 실제 v2·원장·실버·설계·서비스는 수정하지 않았다.

기존 H1/H2/H3/M1/M2의 구체적 회귀 반례는 모두 닫혔다. 기존31·리뷰24·재해시20 실행은 모두 거부됐고, 정상 검증은 19,563 PASS / 0 FAIL이다. 그러나 독립 추가10개 변조 중 **4개 거부 / 6개 허용**이 재현됐다. 포함한 M2를 동시에 제외하거나 무관한 container를 연결해도 통과하며, resolution policy와 attachment rule의 판을 조작해도 통과한다. 이들은 전수이관 미구현 문제가 아니라 이미 pilot에 존재하는 scope·rule 필드의 검증 누락이다.

## 재현과 분모

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-design-pilot-v2-review/probe.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-design-pilot-v2-review/additional.py
```

`probe.py`는 v2 main을 실행하지 않는다. safe_validate를 import하고, 기존 probe/identity/source-review의 출력을 이 검수 폴더로 돌린다. builder는 common.write를 메모리 sink로 바꿔 실제 코드를 실행한다. identity 시험의 복사본도 이 검수 폴더에만 만들고 삭제한다. `source_review.py`의 원문 독립 대조는 builder/validator를 import하지 않는 원래 코드를 실행하되 결과 저장 위치만 바꿨다. 실행한 원본 코드 SHA256와 출력은 `*.execution.json`에 있다.

| 검사 | 재실행 결과 | 해석 |
|---|---:|---|
| 원천·schema·refs·의미·projection 정상본 | 19,563 PASS / 0 FAIL | [baseline.json](baseline.json), schema.json도 코드 선언과 일치 |
| 기존 변조 | 31/31 거부 | [existing-mutations.json](existing-mutations.json) |
| v1 리뷰 추가 변조 | 24/24 거부 + 정상1 통과 | [additional-probes.json](additional-probes.json) |
| v2 ID 재계산 의미 변조 | 20/20 거부 | [rehashed-semantic-probes.json](rehashed-semantic-probes.json), ID 검사만으로 거부된 것 0 |
| 실제 builder identity 시험 | 24 PASS / 0 FAIL | [identity-tests.json](identity-tests.json) |
| 정상 positive controls | 6 PASS / 0 FAIL | [positive-controls.json](positive-controls.json) |
| 독립 원문 JSON 대조 | 996 PASS / 0 FAIL | [independent-source.json](independent-source.json) |
| 이번 독립 추가 변조 | 10 중4 거부·6 허용 + 정상1 통과 | [independent-additional.json](independent-additional.json) |

31+24+20=75와 이번10은 실행 수다. 서로 중복되는 메커니즘이 있으므로 독립 결함85종으로 세지 않는다. 19,563·996도 반복 기계검사 수이며 임상 검토 건수가 아니다. 이번 추가10은 전부 `identity.revise()`로 normalized revision과 종속 참조를 다시 연결한 뒤 `project()`를 재생성했다. 허용6개에는 실패 check와 normalized ID 실패가 모두 0이고, 구현 예외도 0이다.

## H1~M2 항목별 폐쇄

| 기존 항목 | 직접 확인한 근거 | 판정 |
|---|---|---|
| H1 경로가 occurrence identity에 포함 | actual full builder relocation: collection snapshot/source/entity/normalized ID 동일, 이동본 validator 통과. 동일 bytes 다른 logical key 및 다른 domain은 다른 identity | 기존 반례 폐쇄 PASS |
| H2 refs 타입·도달성·authority | typed ref contract와 axis별 schema, decision target/supersedes, override refs, witness source/target/member 검사. 실제 dangling·wrong-type·가짜 human 변조 거부 | 기존 refs/authority 반례 폐쇄 PASS. 아래 규칙판 잔여 별도 |
| H3 raw와 scope/predicate/variant/기간/방향 | 언어 family 삭제·unknown→explicit·predicate·variant parent, combo container 삭제, numeric interval 발명, nary direction 변경을 재해시해도 관련 의미 진단으로 거부 | 기존 명시 반례 폐쇄 PASS. scope 전반 수용은 R-H1로 FAIL |
| M1 exact identity와 mapping rule | correspondence CC4, from/to2, duration attach2의 selected 보존. exact 삭제/전체 hold, mapping rule id/version/hash, native_id/source_kind 변조 거부 | 기존 반례 폐쇄 PASS |
| M2 source/schema/rule/revision 수명 | raw21 전체 manifest와 generated/decision 분리, normalized payload+schema/rule판 ID 재계산, actual builder schema/rule판 변경 및 무관 design hash 변경 시험 | pilot의 ID 수명 계약 PASS |

### H1/M2: 실제 builder와 판 경계

`identity.py:7`의 SourceRegistry는 domain·collection·정렬된 full logical key/hash manifest로 snapshot을 만들고, snapshot+logical file key+pointer로 source occurrence를 만든다. 물리 file은 locator다. 실제 raw21 전체21, generated7, decision1을 collection3개로 구분한다. source_record792개, entity27개다. 물리 이동에 대한 builder 및 validator positive가 모두 통과한다. 동일 basename/bytes의 `a/same.json`·`b/same.json`도 합쳐지지 않고 domain도 구분된다.

실제 builder에서 원문 행 순서·display label·논리 file key 변경은 새 raw snapshot을 만들며 기존 native entity ID는 유지한다. 시험의 행 재정렬 대상은 `anatomy-danger-zones.json`이고, entity는 기존 실버 namespace:native_id 레지스트리에서 취한다. 따라서 이것을 전체 raw entity 재매핑·전수 continuity 이관 검증으로 확대하지 않는다. parent_ref/continuity_ref는 모두 null이며 새 연속성을 발명하지 않았다.

normalized8그룹은 id를 제외한 payload+record schema+mapping contract판에 결합한다. 내용 변경에는 revision ID가 바뀌고, 기존 ID를 임의 변경하며 참조도 바꾼 변조는 `normalized_revision_id`가 거부한다. schema/rule판을 바꾼 실제 builder에서 source/entity는 유지되고 normalized8그룹은 전부 바뀐다. 이 시험판은 unpublished incompatible fixture이므로 현 고정 schema가 새 판을 수용한다는 증거는 아니다. design hash만 메모리에서 바꾸면 basis는 달라지지만 record ID는 유지한다. source snapshot manifest와 정규화 schema/rule판을 혼동하지 않는다.

### H2/M1: 타입·참조·승인과 규칙 근거

`ref_contract.py`와 `ref-contract.json`은 non-null graph ref의 target type과 schema cardinality를 선언한다. entity 축의 included/excluded는 도달성·namespace를 검사하고, container는 source literal, site_relation은 same_site/different_site enum, statement_site/patient_conditions는 값 없는 축이다. native ID·evidence literal·rule identifier를 entity ref로 오인하지 않는다.

이전 `drop_whole_alias_source_claim`은 이제 `typed_ref`로 거부한다. `override_wrong_scope_type`은 `/claims/157/override/scope_ref`, target=`product:M1-1-3`, target_type=`scopes`, reason=`wrong_type_or_missing`을 남긴다. decision dangling target도 `/decisions/0/target_refs/0`를 남긴다. source pointer 실패는 `source_locator`다. safe_validate는 구현 예외를 RuntimeError로 다시 던져 거부 성공으로 세지 않는다. 이번 실행에서 KeyError fallback에 의존한 거부는 없었다.

approved_rule decision은 실제 step9-decisions의 날짜·reason·target·authority·supersedes에 대조한다. reviewer 없는 human과 발명 reviewer 모두 거부하고, ID를 재계산한 기존 wrong target도 `decision_authority_source`로 거부한다. override의 기존 scope 변경과 witness의 실제 ref이지만 다른 target인 연결도 관련 진단으로 거부된다. 실제 attachment witness는8개 모두 []이며 unknown이다. witness가 존재할 때의 부정 검사는 있으나 **실제 근거 있는 positive witness의 전수 usability를 입증하지는 않았다.** 이 미구현은 가짜 witness로 채우지 않는다.

exact identity8개는 CC correspondence4·timing endpoint2·duration source attach2와 selected를 대조한다. 후보3개 mapping(ambiguous2+compatible_candidate1)은 selected0이고 unresolved277개도 selected0이다. mapping.rule의 id/version/hash는 실제 step5/7/9 생성기와 생성 실버판에 대조한다. 다만 resolution·attachment의 rule판에까지 검증이 완결된 것은 아니다(R-M1).

## 새로 재현한 잔여 결함

### High R-H1. 포함·제외 모순과 원문 밖 scope parent가 통과

원문 언어 근거는 `literature-evidence.json:/categories/M2/adverse_effects/2/{statement,patient_ko,patient_en,patient_zh,patient_ja}`다. 정상 scope는 `scopes[163]`의 family included=[family:M2], excluded=[], knowledge=explicit, container_scope_ref=null, application_state=unknown이다. combo 정상 `scopes[7]`의 container included=['코필러','코'], excluded=[]는 실제 complaint의 cc/cc_group이다. 원문 발췌와 실제 pointer는 independent-source.json에 보존했다.

다음 각 변조는 정상 원문/raw/approval을 유지하고, revision ID와 projection을 재생성해도 모두 PASS한다.

| probe | 조작 | 결과 |
|---|---|---:|
| language_scope_excludes_its_included_M2 | family.excluded=['family:M2']를 추가하여 included와 동일 대상 | 19,565 PASS / 0 FAIL |
| combo_scope_excludes_its_source_container | container.excluded를 included=['코필러','코']와 동일하게 설정 | 19,563 PASS / 0 FAIL |
| language_scope_explicit_to_unknown_axis | family knowledge explicit→unknown, included M2 유지 | 19,563 PASS / 0 FAIL |
| language_scope_adds_unrelated_container | 언어 scope.container_scope_ref를 코필러 combo scope로 연결 | 19,565 PASS / 0 FAIL |

`invariants.py:23`은 included/excluded의 타입·도달성만 검사한다. `:60`의 language_scope_family는 included와 application_state만 보고 excluded/knowledge/container는 보지 않는다. combo 검사 `:89`도 included/knowledge만 본다. schema는 이 네 변조를 수용한다. 이 때문에 원문에는 없는 적용 제외나 무관한 상위 문맥을 정상화된 조회자료로 제공할 수 있다. 현재 clinical_application은 unknown이므로 실제 임상 승인으로 이어졌다는 주장은 하지 않는다.

이전 H3 반례의 삭제·승격·predicate·variant·기간 검증은 실제로 해결됐다. 그러나 포함된 family/컨테이너를 동시에 제외하는 모순을 통과시키는 것은 동일 scope 의미 불변식의 잔여이므로 단순 전수 coverage 미구현으로 분류하지 않는다. 재수용 조건은 축별 included/excluded 충돌 정책과 knowledge 상태, source가 뒷받침하는 parent/axis 범위를 명시하고 관련 오류를 ID 재계산 후에도 거부하는 것이다. 임상값이나 원천 미정을 새로 결정할 필요는 없다.

### Medium R-M1. resolution policy.version과 attachment rule provenance 미검증

- 실제 `step9-decisions.json`의 version은1이며 builder는 `policy.version=str(dec['version'])`를 기록한다. 그런데 `resolutions[0].policy.version='incorrect-version'`으로 바꾸고 revision을 재계산해도 **19,563 PASS / 0 FAIL**이다(`resolution_policy_version_forged`). `validate.py:232`는 policy.id/code hash를 확인하지만 version을 확인하지 않는다.
- 실제 `attachments[0].rule`은 id=`pilot-preserve-source`, version=`1`이다. 이를 id=`invented-rule`, version=`incorrect-version`으로 바꾸고 재해시해도 **19,563 PASS / 0 FAIL**이다(`attachment_rule_id_version_forged`). schema.py:32는 두 임의 문자열을 허용하고 validator는 rule 의미를 대조하지 않는다. attachment rule에는 code hash 필드도 없다.

mapping.rule의 M1 버전 수정은 완료됐다. 위 두 필드를 같은 수준으로 검증했다는 일반화만 성립하지 않는다. resolution의 실제 decision판 연결, attachment 규칙 id/판의 선언 및 판별 가능한 구현/계약 fingerprint를 정하고 source/target/witness 계약과 함께 검증해야 한다. 현재 원문에 새로운 승인·검토자·날짜·resolution을 추가하는 작업은 필요하지 않다.

## 원문 보존·projection과 임상 경계

독립 source review는21 원문파일의 JSON/hash와792 source occurrence의 실제 타입·값을 확인했고996/996 통과했다. 이 분모를21파일 전체 의미검수라고 부르지 않는다. 주요 보존 근거는 다음과 같다.

- LOSS3행·6원문 field·16잎(소실10잎 포함)과 동일 common의 서로 다른 occurrence를 유지한다. LOSS02는 실제 taxonomy와 step5 `/extracted/25`가 가리키는 unit_procedure:U5-016이다.
- 중복 CC2키/4occurrence를 분리하고 튼살 parent=P9-4를 유지한다. 과거 R8-0366/0367의 잘못된 parent는 비교 evidence로 보존한다.
- combos146의 구성/순서·arity1=21/2=119/3=6, singleton pair0, 기존 nary pair expansion은 evidence로만 남고 note7의 R8 lineage를 보존한다.
- R8-0001 same_day와 site별 first branch를 분리하고 scalar first=null·days=null·numeric interval=null·staff_check를 보존한다. explicit_no_required_order는 unknown/not_declared/null과 다르다.
- comparison 고유8개 후보/후보항목16개·선택0, 제품 M4 override metadata·M2 미정, K8 준비/상담의 조건 빈 배열, 팔자/목 conflict, 언어5 variant의 한글 지연성 한정·equivalence unreviewed, duration2+기존 conservative resolution1을 유지한다.

전부 withheld로 바꿔 PASS시킨 정상본은 아니다. claim review_state는 unreviewed165/source_conflict1/staff_check1, scope application_state는 explicit8/conditional3/not_applicable2/unknown152다. graph에는 원문 fact lookup167개와 exact identity lookup8개가 source와 함께 별도로 존재한다. attachment8개 unknown, relation147개 적용 보류, 후보 selected0, 미승인 clinical edge0도 동시에 유지된다. exact를 전부 unresolved로 바꾼 재해시 변조는 거부된다.

조회 가능한 원문 fact·확정 identity와 임상 적용 승인을 분리한 방향은 타당하다. source lookup과 identity lookup은 별도 원천 대조가 있으나 projection 전체 일치 검사는 동일 project 함수를 사용하는 정합 검사이기도 하다. 이 projection을 실제 Gold/API/앱/탐색 사용성 검증으로 해석하지 않는다. unresolved combo member277개 전체가 원천적으로 모호하다는 결론도 내리지 않는다.

## 설계 채택 범위와 다음 단계 인계

v2는 **지정42사례와 combos146 중심의 명시 pilot**이다. 25논리타입·247필드 전체의 이관기가 아니다. schema.entities는6종(product/family/site/unit_procedure/concern/evidence_statement)을 허용하지만 실물에는 **5종27개**만 있다(product4/family4/unit11/concern7/evidence_statement1, site0). entity 행은 id/type/native_id/source_refs만 갖는다. product의 label/license/spec/company/family mapping, unit의 site_basis/attributes/purpose, concern의 parent/related/site 등을 typed entity 필드로 이관하지 않았다. raw_value 안에 보존된 필드를 정규화 타입 coverage 완료로 세지 않는다.

설계의 technique/package/purpose/combo/check_condition/complication/evidence_source는 전용 entity로 구현하지 않았다. subfamily/value_dictionary와 별도 component 레코드도 없다. combo를 relation_claim, K8을 claim으로 표현한 사례가 있어도 해당 논리타입 전체를 이관했다는 뜻은 아니다. snapshot/source/scope/claim/relation/mapping/decision/resolution/attachment의 계약 fixture와 notes/aliases/cases를 제공한다. claim.source_refs는 min1 구조지만 pilot은 정확히1개를 강제하고 normalized_value=null, confirmed 금지, 실제 human 없음 등 fixture 전용 제한이 있다. 이를 전체 실버 스키마에 그대로 복사하면 안 된다.

현 단계에서 **부분 채택 제안으로 가져갈 수 있는 것**은 domain/collection/logical file/locator 분리, 정렬 manifest snapshot, source occurrence와 native entity 및 normalized revision 수명 분리, 축별 entity/literal/condition 타입, ref 도달성 진단, exact identity와 적용 승인 분리다. R-H1/R-M1을 닫기 전에는 이 검수의 전체 PASS나 scope/rule 계약 완결을 근거로 정본을 확정하지 않는다.

다음 설계 정본 반영·실버 이관 계약에는 아래 조건을 구체적으로 넣는다.

1. **25타입/247필드 coverage 표:** 각 필드를 원문 locator·현 실버 필드·제안 typed 경로·missing/null/[]/false 의미·보존/정규화/명시 비적용/미구현 상태와 연결한다. 자동 field-name 일치만으로 승인하지 않는다. 위 pilot 미구현 entity·embedded·component와 schema 차이를 전건 적는다.
2. **판·ID 계약:** raw21과 generated/decision collection membership, logical rename·재정렬·표시이름·분할/병합·schema/rule판의 기대 ID 변화, 검증된 continuity 절차를 명시한다. alternate schema판의 실제 schema/validator 적합성도 별도 시험한다.
3. **scope와 rule 폐쇄:** R-H1 네 변조와 R-M1 두 변조를 정상 positive와 함께 회귀군에 넣는다. 포함/제외·knowledge·parent의 출처 의미 및 policy/attachment 규칙판 fingerprint를 검증한다. refs의 타입/도달성 성공을 source 관계 정합 성공과 혼동하지 않는다.
4. **전체 대상에 맞는 검증:** source-native field·scope·predicate·variant·condition·direction·interval의 독립 oracle을 coverage에 연결한다. 정본에 근거가 있는 identity positive와 아직 승인되지 않은 application negative를 동시에 유지한다. 실제 근거 있는 witness/여러 source/정당한 normalized 값의 positive도 해당 타입을 구현할 때 추가한다.
5. **소비 계약과 미정:** source fact·identity·후보·조건부 사실·보수 view·적용승인의 소비 상태를 별도로 정의하고, 앱/API가 source lookup을 임상 승인으로 승격하지 않는지 후속 단계에서 검증한다. 원천 미정과 구현 누락은 서로 다른 잔여 목록으로 관리한다.

안전580행 전수, semantic-pending1277칸, duration196슬롯/343 alternatives, 전체 concern/combination 의미 이관, 언어 동치, 원문 충돌 해소, 임상·허가·문헌 최신성, usable Gold와 앱 탐색/최종답 성공은 범위 밖이다. 이번 보고서는 임상값·새 근거·새 승인·원천미정 해소를 제안하지 않는다.

## 기준판·보호 경계

기준 pilot.json SHA256는 `cc897e4cca29f0e50bab2605ee3ef06a7ab5fe7942544a2ca00b4b496f45c89f`다. build.py=`6ac8f07c83c4a069f031c7f89788626e01c621cbad13d854e3c62599eb924028`, validate.py=`75a7f4cecefbfbef7d9e4d943c7719ce7fcea6bf98465bdf385b7de68292bd46`, invariants.py=`b1a18db030eb20e3361b2e955ce574649162b2fd21bbe628d311642568ef595d`, identity.py=`dccf33fec8b68da3c72adaeb1addc31214b17cd610d40f10e3f1307bd1729ace`다. 전체 기준코드와 입력 hash는 [review-start.json](review-start.json), 실행 후 코드 hash는 [rerun-integrity.json](rerun-integrity.json)에 있다.

검수 시작/종료 [review-start.json](review-start.json)·[review-end.json](review-end.json)과 [immutability.json](immutability.json)으로 보호입력 및 v2 전체 **243파일 불변**을 확인했다. 기존 v1 WORK 불일치는 v2 immutability의 알려진 코디 진행기록 변경으로 유지하며 v1 baseline을 소급 수정하지 않았다. 검수 중 공유 기준판 변경은 없었고 혼합 판정하지 않았다. 원장·실버·설계/HTML·v1/v2·스펙/WP·앱/Hub·환경·DB·서버를 수정하지 않았다. 결과와 읽기 전용 재현 probe만 이 검수 폴더에 작성했다. 네트워크·모델·설치·하위워커·commit/push/PR 실행은 없었다.
