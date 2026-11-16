# 실물 설계 pilot 독립 검수

Task `task_d0e593063c24` · Dispatch `ctx_30c8283fed89` · 2026-11-03 KST

## 판정

**FAIL — 단계3 전체 수용 및 단계4 정본 이관 착수 조건은 충족하지 못했다.** 실제 pilot의 지정 사례 원문 보존은 확인했으나, 이동에 따른 occurrence ID 변경과 참조·scope·판정 근거 검증의 누락이 재현됐다. 이는 현재 원문이 훼손됐다는 판정이나 임상 판단이 아니다. 수정 없이 읽기 전용 검수했고, 아래 반례와 보고서만 이 디렉터리에 작성했다.

기존 검증 재실행은 **11,922 PASS / 1 FAIL**, 기존 변조 **31/31 거부**다. 유일한 baseline 실패는 `WORK.md`의 pilot 시작 이후 변경이며 코디가 진행기록 갱신임을 확인했다. 이를 숨기거나 baseline을 소급 수정하지 않았다. 이 차이를 제외한 기존 검증은 초록이어도 아래 독립 반례 때문에 전체 판정은 FAIL이다.

## 실행과 증거

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-design-pilot-review/probe.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-design-pilot-review/source_review.py
```

`run.py`, `validate.py`의 CLI main은 pilot 파일을 다시 쓰므로 실행하지 않았다. 대신 기존 `safe_validate`, `mutation_tests`, `structural`, `project`를 직접 실행하고, builder는 `common.write`를 메모리 sink로 바꿔 실행했다. JSON 직렬화 후 재생성 pilot은 기존 `pilot.json`과 정확히 같다. JSON object의 정수 키가 문자열 키로 바뀌는 정상 직렬화 차이도 구분했다. 기존 validator의 main이 수행하는 보호입력178 hash/bytes와 schema 일치 검사도 별도로 그대로 실행했다. 결과는 [existing-rerun.json](existing-rerun.json), [builder-repro.json](builder-repro.json)에 있다.

추가 시험 **25개 = 정상 positive control 1개 + 변조24개**다. 정상본 통과, 변조 **5개 거부 / 19개 허용**이었다. 허용은 검수 성공을 뜻하지 않고 validator가 해당 잘못을 잡지 못했다는 뜻이다. [additional-probes.json](additional-probes.json)에 각 실패 check와 예외를 보존했다. 모든 시험은 실제 기존 값을 삭제·이동·참조 변경하는 방식이며 새로운 임상 원문을 만들지 않았다.

builder/validator를 import하지 않는 [source_review.py](source_review.py)는 원문21파일을 각각 JSON으로 읽고, 지정 사례 및 source_record792개의 실제 파일/pointer/타입/값을 독립 대조했다. **996 PASS / 0 FAIL**이며 결과와 실제 원문 발췌는 [independent-source.json](independent-source.json)에 있다. 996은 반복 기계검사 수이며 임상 검토 건수가 아니다. 21파일 전체의 의미 검수라고 부르지 않는다. 사례 구조화에 직접 사용한 원문은 6파일이고 나머지는 JSON 구조·hash 확인 범위다.

## Severity별 문제와 재현

아래 경로의 기준은 `silver-design-pilot/`이며, JSONpath는 `pilot.json` 기준이다. 검수 스크립트에서 해당 probe 이름으로 재현할 수 있다.

### High H1. 절대경로가 immutable occurrence identity에 섞임

- 위치: `build.py:src`, `validate.py`의 `occurrence_id`, `pilot.json:$.source_records[*].{id,file,snapshot_ref}` 및 `$.snapshots[*]`; `report.md`의 “snapshot hash+절대파일+JSON Pointer” 설명.
- 실제 원문 `problem-packages.json`을 검수 디렉터리 아래에 동일 bytes로 복사해 **실제 builder의 src 함수**를 호출했다. pointer는 `/problems/8/complaints/10`으로 같다. SHA256와 snapshot ID는 양쪽 모두 `e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc`다.
- 원래 occurrence `src:5d930df136433bc73ebc70831c5495f088c3d092de992b44b02e5f439cb5121e`가 복사 위치에서 `src:49862b2b3b6d10aee7150519d457d4dabce73a0b3251d9a8ebde860c3630ec60`으로 바뀐다. 단순 디렉터리 이동만으로 같은 원문/동일 파일판 snapshot/동일 pointer의 ID가 바뀌는 함수임이 재현됐다. 복사본은 시험 후 삭제했다. [relocation.json](relocation.json) 참조.
- 같은 프로세스에서 두 위치를 읽으면 `snap:<file hash>` ID는 같은데 `files`가 다른 snapshot 레코드가 두 개 생긴다(중복1). 현재 pilot13개 snapshot 사이에 충돌이 있다는 뜻은 아니며, 이동·복사 입력을 받는 함수의 결함이다. 원문 루트 밖 복사본은 `source_kind=generated`로 분류하는 경로 의존도 있다.
- 기존 설계 `design.json:$.id_policy` 및 audit `id-design.json`은 원문21의 full snapshot manifest와 `file=problem-packages.json` 같은 이동 독립 file identity를 예시로 사용한다. pilot은 파일 하나의 bytes hash로 snapshot을 만들고 절대경로를 occurrence 입력으로 써 의미를 바꿨다. gaps.md에 이 변경의 합의가 없다.
- 수정방향: source domain/collection·이동 독립 file identity·원문 전체 snapshot·실버 산출물판을 구분해 계약을 합의하고, 물리 locator는 별도 보관한다. 같은 내용을 가진 서로 다른 logical file도 구분해야 한다. 동일 입력의 디렉터리 이동, 동일 bytes 다른 file/domain, 행 재정렬을 서로 다른 시험으로 고정한다. 단순 basename-only/content-only 키로 대체해서도 안 된다.

### High H2. refs의 타입·도달성과 승인 근거를 전수 검증하지 않음

- 위치: `schema.py`의 `REF`, `AXIS`, `OVERRIDE`, `T['decisions']`, `T['attachments']`; `validate.py`의 scope/decision/attachment loop.
- `$.decisions[0].target_refs`를 존재하지 않는 `clm:000…000`으로 바꿔도 통과한다(`decision_dangling_target`). `supersedes`에 존재하지 않는 decision을 넣어도 통과한다. `authority.kind`를 기존 `approved_rule`에서 `human`으로 바꾸고 reviewer=null을 유지해도 통과한다. 실제 decision 원문을 읽지만 status/authority/target 의미까지 묶어 확인하지 않는다.
- `$.claims[157].override.claim_refs`에 존재하지 않는 claim을 넣어도 통과한다(`override_dangling_claim`). override.scope_ref를 entity ID로 바꾸면 거부되지만 명시 타입 검사가 아닌 뒤의 `KeyError`다. 결정·override의 모든 참조를 검증한다는 보장은 없다.
- `$.attachments[0].witness`에 claim ID를 mapping_ref와 source_ref로 쓰고 존재하지 않는 edge_ref/component_ref를 넣어도 통과한다(`attachment_witness_wrong_ref_types`). schema는 문자열 모양만 검사하고 validator는 witness를 검사하지 않는다. 현재 정상본의 witness는 빈 배열이므로 실제 witness→source 역추적 usability도 입증되지 않았다.
- `$.scopes[0].axes.product.included=['product:missing']`가 통과한다(`axis_dangling_entity`). axes는 entity refs와 container 문자열·same_site enum을 같은 string[]로 받아 축별 계약이 없다. 전부 entity로 간주해 검사하는 해결책도 잘못이다.
- 수정방향: ref 필드별 대상 타입·필수 cardinality·source/target 관계를 선언하고 전수 도달 검사한다. 축별 허용 값과 source evidence를 구분한다. decision의 approved_rule/human 근거를 실제 원문에 묶고, witness가 비어 있어도 되는 경우와 필요한 경우를 명시한다.

### High H3. scope와 normalized 의미를 삭제·변경해도 통과

- 위치: `$.scopes[163].axes`(언어 claim의 M2 family), `$.scopes[7].axes`(첫 combo container), `$.claims[160].predicate`, `$.claims[161].variant.of`, `$.relation_claims[146].interval`, `$.relation_claims[86].direction`.
- 언어 scope.axes를 `{}`로 지우거나 application_state를 unknown→explicit으로 바꿔도 통과한다. 한글 qualifier 원문은 유지돼도 적용 family 범위를 잃는다(`scope_family_qualifier_erased_language`, `scope_unknown_to_explicit_language`). 첫 combo container 축 전체 삭제도 통과한다(`combo_scope_container_erased`).
- 언어 statement의 predicate를 safety.common으로 바꾸거나 한글 variant.of를 무관한 기존 safety claim으로 바꿔도 통과한다. raw 값 및 참조 존재만 맞으면 predicate/variant의 의미 오류가 남는다.
- R8-0001의 field_conditions.days는 null이어야 한다는 검사가 있지만, 별도 interval에 min=0/max=0/unit=day를 채우면 통과한다(`timing_interval_changed`). 원문이 말하지 않은 수치 interval을 downstream consumer가 읽을 수 있다. n-ary relation의 direction을 unknown→directed로 바꾸는 것도 통과한다.
- 수정방향: 원문 근거로 확인한 scope/qualifier와 normalized predicate, variant parent, 방향·기간의 변환규칙을 사례에 연결해 독립 확인한다. raw가 정확하다는 사실만으로 구조화 의미가 정확하다고 판정하지 않는다. source에서 확정할 수 없는 필드의 null/unknown을 모든 중복 표현에 일관되게 강제한다.

### Medium M1. 기존 확정 identity mapping과 rule version이 약화돼도 통과

- 위치: `$.mappings[0].selected_refs`, `$.mappings[0].rule.version`, `validate.py:existing_mapping_rule`.
- CC occurrence의 `state=exact`, target 후보 및 실제 correspondence 근거를 두고 selected_refs만 `[]`로 지워도 통과한다(`mapping_drop_exact_selection`). 기존 근거가 있는 identity mapping을 보존해야 한다는 pilot 요구를 검증하지 못한다. 반대로 후보를 selected로 승격하는 명시 변조는 거부되므로 두 방향을 구분해야 한다.
- rule의 hash는 맞지만 version을 틀리게 바꿔도 통과한다(`mapping_rule_wrong_version`). schema의 rule.version은 임의 string이며 실제 파일판과 대조하지 않는다. source native_id나 snapshot source_kind를 바꿔도 통과한다.
- 수정방향: 원문 대응으로 확정된 identity와 임상 적용 승인을 분리한 상태표를 만들고, exact identity의 선택 대상 및 rule id/version/hash를 실제 대응행과 묶어 검증한다. rule=null+reason 허용을 기존 rule 삭제 허용으로 확대하지 않는다.

### Medium M2. schema/rule판과 snapshot/claim ID 수명 구분이 부족

- `build.py`의 claim/mapping/scope ID는 design basis hash와 token 등을 사용하나 schema_version은 입력이 아니다. relation ID는 source만 쓰는 경우도 있다. schema가 바뀌어도 같은 ID가 나올 수 있고 design.json의 다른 변경으로 광범위하게 바뀔 수 있다. 원문 occurrence/실버 파일판/논리 레코드 revision의 수명 계약이 필요하다.
- `$.claims[0].id`를 임의 64자리 hash로 바꾸고 이를 참조하는 필드를 함께 고치면 통과한다(`claim_id_arbitrarily_changed_with_refs`). source ID는 재계산하지만 그 외는 주로 prefix/hash 길이만 검사한다. 이것만으로 ID 안정성 검증 완료라고 할 수 없다. 임의 ID 자체가 모든 설계에서 금지된다는 뜻은 아니다. 현재 생성 알고리즘을 주장한다면 그 결정성과 판 경계를 검증해야 한다.
- 원문과 generated/decision 모두 `snap:<bytes hash>` 한 namespace를 쓰며 현재13개는 서로 다르다. 동일 bytes 다른 domain 충돌을 막는 계약은 없다. source_kind는 보조필드이고 ID에 들어가지 않는다. 원문 전체21 snapshot과 실제 사용13파일의 파일판 snapshot은 같은 분모가 아니다.
- 행 재정렬은 파일 hash와 snapshot이 바뀌어 occurrence가 달라지는 것이 정상이며, 기존 entity namespace+native ID는 유지돼야 한다. parent_ref/continuity_ref가 전부 null인 pilot은 이관 전후 연속성 검증을 아직 수행하지 않았다. 동명이행은 content만으로 합치지 않았고 legacy2키는 집합을 유지했으므로 그 부분은 통과다.

### Low L1. 보고서의 전역 hash PASS는 현재 재실행과 다름

`inputs-start.json`178항목 중177개는 현재도 일치하고, `WORK.md`만 다르다. 이전 SHA256은 `d678b6ff4fe18c227cba93f2ec52b486c911aed62fecbf393593aafdae8fd184`, 현재는 `962fc279da6b64507453a358930d3995431f61d03060203b8719d1dd3ae804a5`다. 코디 메시지 `msg_c342f6be6a7b`가 pilot 종료 후 단계3 진행상태 갱신임을 확인했다. 원문21·실버·schema·design 손상으로 분류하지 않는다. 검수 시작/종료198개 보호파일은 모두 불변이다.

## 실제 사례와 허용 refinement 대조

| 사례·분모 | 독립 확인과 실제 표현 | 판정 범위 |
|---|---|---|
| LOSS 3행/6 field/16잎 | 코어톡스3+2, 턱선보톡스3+2, 에버라인4+2. 기존 common6잎과 잃었던10잎 모두 source occurrence에 존재. 동일 common 문장을 세 출처로 유지 | 현 pilot 원문 보존 PASS |
| LOSS02 entity | 원문 taxonomy `/modality/0/subcategories/2/items/7`은 턱선보톡스. step5 `/extracted/25`의 attach=단위 시술, units=[U5-016] | product 예시 오류 정정은 타당. 기존안은 미수정 |
| CC 2키/4행 | 니들RF·프락셔널레이저 각각 다른 detail/group으로 분리. 튼살 두 taxonomy 행 parent=P9-4, 기존 R8-0366=P9-3/R8-0367=P9-1도 비교 증거에 남음 | 올바른 target과 과거 잘못된 참조를 구분함 |
| combos146 | arity1=21/2=119/3=6, 모든 구성·순서와 전체 원문 reason/evidence 보존 | singleton pair0. n-ary 기존 pair는 evidence로만 보존 |
| note7 | note109/110/111/132/133/134/135 → R8-0277/0278/0279/0298/0299/0300/0301, 실제 reason/원문 parent 대조 | lineage PASS, 새 관계 생성 없음 |
| R8-0001 | “같은 날 가능”과 “동일 부위는 보톡스 먼저…다르면 순서 무관”의 interval/note 분리. same_site→a(M1), different_site→explicit_no_required_order. first scalar=null, days=null, staff_check | options 타입·순서무관 enum 정교화 타당. 미지조건을 승인하지 않음. H3 검증 누락 별도 |
| 비교 필러2멤버 | 각 멤버에 U5-082..089 후보8개씩, selected=[]; subtitle context와 member scope 별도 | 보고서의 “8개 후보”는 고유8개/후보항목16개임. 단독 팔자 적용 승격0 |
| 제품 override1 | 실제 step5 product_links[243]의 priority/level/override_of=M4와 제품 다계열 compatibility 보존, M2 적용 unknown | strict metadata 확장은 타당. 후보=적용 승인 아님 |
| K8-0028/29 | target=family:M2, 준비/상담 kind, 기존 conditions=[] 보존 | 빈 조건을 환자 안전 승인으로 해석하지 않음 |
| 팔자/목 | 팔자 container와 목주름 reason을 source_conflict 및 unknown으로 유지 | 오기·임상 적용 판정 없음 |
| 언어5 claim | statement+patient_ko/en/zh/ja 각각 보존. ko의 “몇 개월 후에 지연성” 한정 존재, equivalence=unreviewed | 원문 차이는 보존. qualifier 승인/동치 판단 없음 |
| duration2+resolution1 | 3-6개월 문장과6-9개월 별도 claim, D9-3 보수선택/alternative/기존 날짜/규칙, clinical_consensus=false | 기존 정책 보존 타당. 임상합의나 새 승인 없음 |

gaps.md의 nullable rule+state/reason, R8 branch 구조와 enum, override의 원래 metadata 및 기존 pair 전개근거를 엄격 필드로 보존한 선택은 실제 사례에 필요하고 근거와 부합한다. 임의 metadata bag이나 가짜 임상 reviewer/date를 정상본에 넣은 흔적은 확인하지 못했다. 허용된 refinement가 validator의 참조 누락과 동의어는 아니다. LOSS02 예시 정정과 이 refinement들을 본 설계에 반영할지는 별도 확정해야 한다.

## 기존 변조31개 평가와 graph usability

기존 validator는 build.py를 import하지 않고 원문을 다시 읽는다. LOSS field/잎, CC taxonomy parent, combos146 구성/순서, 조건분기, 후보 목록, 언어 한정과 duration을 직접 대조하므로 “builder와 같은 출력만 비교하는 시험”으로 전부 폄하할 수 없다. 안전 overwrite, 잘못된 고민 scope, endpoint swap, note wrong R8 등에는 각각 관련 실패 check가 있다. 다만 expected case ID·분모·일부 locator·기대정책은 하드코딩되어 있고, `projection_matches_records`는 동일 project() 구현과 비교하므로 독립 투영 oracle이 아니다.

31개 중 `drop_whole_alias_source_claim`은 broad exception fallback으로 거부됐다. 관련 참조가 실제로 끊긴 것이므로 무관한 원인이라고 단정하지 않지만, 어떤 missing claim인지 모르는 `KeyError` 하나로 종료되어 개별 진단 품질이 낮다. 나머지는 schema 또는 의미에 관련된 check로 거부됐다. 추가 반례의 `override_wrong_scope_type`도 같은 broad exception에 의존한다. positive control이 먼저 통과했으므로 모든 변조가 baseline WORK hash 실패 때문에 거부된 것은 아니다. mutation_tests는 별도 hash 실패 검사를 호출하지 않는다.

graph는 source/snapshot/claims/scopes/mappings/notes/decisions/resolutions를 함께 보관하고, entity27개와 attachment8개를 투영한다. singleton21에 pair를 만들지 않고 n-ary6의 기존 pair 전개근거도 남긴다. 후보→selected 승격0, procedure edges147개 모두 withheld, attachment8개도 모두 application_state=unknown이다. 따라서 자동 임상 확정 edge0은 사실이나 **전부 보류했다는 사실만으로 실제 설계 usability를 입증하지 못한다.**

정상 사례를 보류해도 된다는 이번 안전 경계 안에서는 현재 상태를 허위 임상 승인으로 볼 수 없다. 그러나 원문 trace를 제공하는 검증용 투영과 실제 탐색에서 사용할 수 있는 확정 identity/후보/조건부 fact 계약은 다르다. 정확한 identity mapping8개(CC4/R8 endpoint2/duration2)는 이미 selected를 갖고 있으며 임상 적용과 분리해 유지해야 한다. combo member277개 전체는 후보도 없이 unresolved다. 이를 “모든 조합이 원천적으로 모호하다”는 결론으로 삼아선 안 된다. 원문으로 확정할 수 있는 entity correspondence와 별도 승인이 필요한 적용을 가르는 후속 설계가 필요하다. K8 준비·상담 fact나 기존 D9-3 보수 view를 어떤 상태로 조회할 수 있는지도 별도 소비 계약이 필요하다.

## 단계4 준비 범위와 재수용 조건

현재 가져갈 수 있는 것은 지정42사례의 source evidence, LOSS16잎 보존과 LOSS02 단위시술 분류, 중복 CC occurrence/올바른 P9-4 대응, combos146의 원문 구성과 note7 lineage, 조건분기·후보·override·scope충돌·언어variant·resolution의 **미승인 검증 fixture**다. 본 설계 확정이나 전수 실버 이관 승인으로 가져갈 수 없다.

단계4 착수 전 H1~H3를 고치고 M1/M2의 계약을 합의한 뒤, 동일 raw 원문을 독립 대조하여 추가19개 허용 반례가 관련 check로 거부되는지 재검수해야 한다. ID 경로이동·domain/file namespace·schema/rule revision·재정렬 continuity와 모든 typed ref를 수용조건에 넣는다. metadata-only source mapping과 clinical application을 구분하고 정상 source-confirmed identity가 무조건 hold로 사라지지 않는 positive fixture도 필요하다. pilot refinement와 LOSS02 예시 정정은 정식 설계에 반영할지 결정한다.

이번 검수는 안전580행 전체, 세부 의미 미검토1277칸, duration196슬롯/343 alternatives 전체, 전체 concern/combination의 의미 이관, 임상·허가·문헌 최신성, 활성 DB/publication, 실제 Gold/API/앱/탐색 또는 최종답 성공을 승인하지 않는다. 네트워크·외부모델·설치·하위워커·commit/push/PR·DB/서버 실행은 없었다.

## 보호파일 및 산출물

[review-start.json](review-start.json)과 [review-end.json](review-end.json)은 보호입력178개와 pilot20파일을 합친198개 파일의 full SHA256/bytes다. [immutability.json](immutability.json)의 시작/종료 일치가 true다. 원문21은 pilot baseline 및 검수 시작/종료 모두 일치한다. 원본 pilot/schema/design/HTML/실버/코드/원장·WORK는 수정하지 않았다. 재현 복사본만 검수 폴더에 잠시 만들고 삭제했다.

보고서, probe.py/source_review.py, JSON 결과들만 이 폴더에 작성했다. 실패한 수용 판정은 개선 방향을 전달하는 검수 결과이며 검수 작업 자체는 완료했다.
