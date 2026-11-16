# 실물 설계 pilot 검증 결과

Task `task_9a80516d7b7c` · Dispatch `ctx_55cef790e0f9` · 2026-11-03 KST

## 결과와 판정 범위

**pilot 범위의 원문 보존·후보/조건 보존·참조 검증 PASS.** 기존 42개 증거 사례를 실제 snapshot 원문과 현재 실버에서 다시 읽어 별도 pilot records로 구조화했다. 실버 전체 이관이나 임상 정확도 승인이 아니다. 원장 자체의 미정은 미정으로 남겼다.

- 독립 source 대조/참조/구조/투영 검사 **11,923 PASS / 0 FAIL**, 명시 변조 **31/31 거부**. 검사 수에는 ID/ref별 반복 검사가 포함되며 서로 다른 임상 검토 건수가 아니다. 정상본 positive control이 통과해야 변조 시험을 시작한다.
- 안전 alias 충돌 3행의 6개 원래 field-list와 **16잎 전부 보존**: 기존에 남은 common 6잎과 소실된 원문 10잎을 별도 source occurrence로 추적한다. 동일한 common 문장이 세 행에 있어도 claim/source ID를 합치지 않았다. pilot 범위 원문 손실 **0**이다.
- CC 중복키 2개/4행은 occurrence와 명확한 taxonomy entity/그룹으로 분리했다. 튼살 두 행은 **P9-4**, 기존 실버 R8-0366의 P9-3와 R8-0367의 P9-1 연결도 비교 증거로 유지했다. legacy 이름 alias의 단일확정 승격 **0**이다.
- 원문 CC combos **146/146** 전수 구조화: arity **1=21, 2=119, 3=6**. singleton pair 생성 **0**, 새 pair 임상 승인 **0**. n-ary 원문 구성·순서와 기존 R8 전개 rule/lowering/endpoint/arity 및 정확한 실버 ref를 보존했다. 기존 legacy key가 모호하면 source occurrence 후보도 모호하게 둔다.
- note **7/7**은 기존 **R8-0277/0278/0279/0298/0299/0300/0301**과 원문 source_record_ref로 연결했다. 원장에 없는 관계를 새로 만들지 않았다.
- R8-0001의 same_day와 first를 분리하고 same_site→a(M1), different_site→**explicit_no_required_order**를 원문 ref별로 보존했다. 조건 모름의 first는 null, staff_check 유지다. 임상 승인이나 근거 없는 unknown resolution을 만들지 않았다.
- 비교 필러 두 멤버의 8개 후보와 제품 다계열 compatibility는 후보로 보존했다. 후보→선택 승격 **0**이며 팔자 단독 확정 연결 **0**이다. 제품 M4 override의 원문 범위와 override_of/level/priority를 유지했다. K8-0028/29의 이미 존재하는 target/conditions/kind도 보존했다.
- 팔자 container/목주름 statement 충돌, patient_ko의 지연성 한정, duration 원천 2claim/보수 resolution/alternative는 모두 분리돼 역추적된다. 미정 해소나 원장 정정은 하지 않았다.

## 산출물과 재실행

```sh
python3 orchestration/work/phub-recommend/silver-design-pilot/run.py
```

외부 패키지·설치·네트워크·DB·서버·Gold builder 없이 Python 표준 라이브러리만 쓴다. `run.py`는 이 폴더의 build → schema → 검증용 projection → 독립 validator/변조 → report 순서로 실행하며 실패 시 멈춘다. 최초 `inputs-start.json`은 재실행해도 갱신하지 않는다.

| 파일 | 역할 |
|---|---|
| [pilot.json](pilot.json) | source occurrence, 기존 entity, claim/scope/mapping/decision/resolution/attachment, 42case records |
| [schema.json](schema.json), [schema.py](schema.py) | 필수 필드/type/enum/additionalProperties와 dependency-free strict validator |
| [build.py](build.py), [common.py](common.py) | 실제 원문과 현재 실버에서 pilot만 재생성 |
| [validate.py](validate.py), [validation.json](validation.json) | 생성기와 별개로 snapshot을 읽는 전수 대조 및 명시 변조 결과 |
| [project.py](project.py), [graph-projection.json](graph-projection.json) | 검증용 logical→Gold projection; 실제 Gold 코드/DB 미실행 |
| [case-traces.json](case-traces.json) | 사례별 원문값·기존 실버값·pilot/graph JSON Pointer 전체 |
| [gaps.md](gaps.md) | 허용된 pilot refinement, 기존안 예시 오류, 원천 미정, 이관 영향 |
| [inputs-start.json](inputs-start.json), [inputs-end.json](inputs-end.json) | 원문21 포함 보호 입력178파일의 시작/종료 full SHA256/bytes |
| [run.py](run.py), [report.py](report.py) | 전체 재실행과 이 보고서/trace 생성 |

원문 occurrence ID는 **snapshot hash+절대파일+JSON Pointer**의 SHA256이며 content-only가 아니다. entity ID는 실제 기존 namespace+ID를 유지한다. source occurrence의 배열 위치는 특정 snapshot의 위치이지 entity ID가 아니다. 기존 엔터티 존재를 검사하므로 이름으로 새 entity를 발급하지 않는다. 원문은 `source_records.raw_value`, 정규화 술어는 `claims.predicate`, 원래 key는 `raw_field`에 분리한다.

이번 pilot에는 13개 실제 사용 파일판 snapshot, 792 source_record, 27 기존 entity, 165 scope, 167 claim, 147 relation_claim, 288 mapping, 1 기존 규칙 decision, 1 conservative resolution, 8 attachment가 있다. 실제 구조화에 사용한 원문은 6/21파일이고 전체 원문21은 hash를 검사했다. snapshot 레코드 수는 원문21의 전체 이관 수가 아니다.

## 계약과 빈값

`schema_version=silver-design-pilot/1`, basis는 원안 `design.json`의 full SHA256 `d742c65d072a48e705a26b9ce6daf23ed23441437f7c7441967b8b8d73f7e382`이다. 본 설계 파일은 수정하지 않았다.

- JSON Schema의 모든 typed record는 required/enum/type을 엄격히 검사하고 추가 필드는 거부한다. `raw_value`는 원문의 임의 JSON을 허용하지만 snapshot의 exact pointer에서 독립 재독한 값·타입과 일치해야 한다. source hash/bytes와 occurrence ID도 검증한다.
- `selected_refs:[]`는 실제 선택이 없음이다. 미정 mapping의 `candidates:[]`는 후보를 아직 정하지 못한 상태이며 아무 대상에나 적용한다는 뜻이 아니다. `rule:null`은 적용한 실제 매핑 규칙 없음이며 reason/state가 필수다. 존재하는 자동 규칙·판정은 정확한 source row와 생산 스크립트의 version/hash로 보존한다.
- `days:null`, `first.value:null`, `normalized_value:null`은 해당 계산/조건이 확정되지 않았음을 뜻한다. `false`와 혼용하지 않는다. `captured_at:null`, reviewer=null은 기록에 없는 날짜·사람을 만들지 않았다는 뜻이다. D9-3의 기존 decided_at만 원래 값으로 인용한다.
- `conditions:[]`인 K8 두 행은 **조건 항목이 아닌 준비/상담**이며 안전 승인이나 위험 부재가 아니다. scope의 patient_conditions=not_applicable에 이 의미를 명시했다.
- 원문 claim은 immutable이고 clinical review와 자동 처리 상태는 별개다. D9-3은 원천 합의가 아니라 기존 보수 출력 정책이다. 대안을 삭제하거나 clinical_consensus=true로 바꾸면 거부한다.

## 논리 타입 → 검증용 graph

entity 27개 중 실제 registry에 있는 타입만 node로 투영한다(실제 생성 수는 위 집계/JSON 기준). claim/scope/mapping/decision/source_record는 **노드가 아닌 typed records**로 남긴다. fact_attachment는 원안의 선택 projection을 사용하며 모두 application_state=unknown이다. 기존 concern/combo/Gold 전체 그래프를 재구성하는 구현이 아니다.

그래프에는 facts, relation_records, mapping_records, scope_records, notes, legacy_aliases, decisions, resolutions 및 exact source_records/snapshots가 남아 후보/조건/출처를 확인할 수 있다. 독립적인 적용 판정 없는 procedure_relation/procedure_pair는 모두 withheld에 기록하고 자동 생성하지 않았다. 기존 R8 pair는 relation_records의 기존 근거이며 새 확정 엣지가 아니다. 자동 확정 procedure_pair를 주입한 변조는 FAIL로 검출한다.

## 사례별 원장 → 현재 실버 → pilot → 제안 graph

표의 pilot/graph 경로는 각각 `pilot.json`, `graph-projection.json`의 JSON Pointer다. 원문/실버 파일의 절대경로·full hash·값과 모든 source refs는 `case-traces.json`과 source_records에 있다. 아래 PASS는 **표현과 역추적**의 판정이며 기존 실버 오류를 고쳤다거나 임상 승인했다는 뜻이 아니다.

| 사례 | 원장 위치 | 현재 실버 위치 | pilot | graph | 판정 / 미정 |
|---|---|---|---|---|---|
| LOSS-01 | `taxonomy.json:/modality/0/subcategories/1/items/3/extracted/safety/common_adverse_effects`<br>`taxonomy.json:/modality/0/subcategories/1/items/3/extracted/safety/common` | `step5-units.json:/extracted/7/source_text/safety.common` | `/claims/0`<br>`/claims/1`<br>`/scopes/0`<br>`/attachments/0` | `/facts/0`<br>`/facts/1`<br>`/scope_records/0`<br>`/edges/0` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| LOSS-02 | `taxonomy.json:/modality/0/subcategories/2/items/7/extracted/safety/common_adverse_effects`<br>`taxonomy.json:/modality/0/subcategories/2/items/7/extracted/safety/common` | `step5-units.json:/extracted/25/source_text/safety.common` | `/claims/2`<br>`/claims/3`<br>`/scopes/1`<br>`/attachments/1` | `/facts/2`<br>`/facts/3`<br>`/scope_records/1`<br>`/edges/1` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| LOSS-03 | `taxonomy.json:/modality/6/products/1/extracted/safety/common_side_effects`<br>`taxonomy.json:/modality/6/products/1/extracted/safety/common` | `step5-units.json:/taxonomy_products/36/source_text/safety.common` | `/claims/4`<br>`/claims/5`<br>`/scopes/2`<br>`/attachments/2` | `/facts/4`<br>`/facts/5`<br>`/scope_records/2`<br>`/edges/2` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ANCHOR-11 | `problem-packages.json:/problems/8/complaints/11` | `step8-relations.json:/claims/366` | `/claims/6`<br>`/mappings/1`<br>`/scopes/4` | `/facts/6`<br>`/mapping_records/1`<br>`/scope_records/4` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ANCHOR-10 | `problem-packages.json:/problems/8/complaints/10` | `step8-relations.json:/claims/365` | `/claims/7`<br>`/mappings/3`<br>`/scopes/6` | `/facts/7`<br>`/mapping_records/3`<br>`/scope_records/6` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-095 | `problem-packages.json:/problems/0/complaints/13/combos/0` | `step7-concerns.json:/step8_notes/95` | `/claims/21`<br>`/relation_claims/13`<br>`/scopes/20` | `/facts/21`<br>`/relation_records/13`<br>`/scope_records/20` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-097 | `problem-packages.json:/problems/0/complaints/14/combos/0` | `step7-concerns.json:/step8_notes/97` | `/claims/22`<br>`/relation_claims/14`<br>`/scopes/21` | `/facts/22`<br>`/relation_records/14`<br>`/scope_records/21` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-099 | `problem-packages.json:/problems/0/complaints/15/combos/0` | `step7-concerns.json:/step8_notes/99` | `/claims/23`<br>`/relation_claims/15`<br>`/scopes/22` | `/facts/23`<br>`/relation_records/15`<br>`/scope_records/22` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-101 | `problem-packages.json:/problems/0/complaints/16/combos/0` | `step7-concerns.json:/step8_notes/101` | `/claims/24`<br>`/relation_claims/16`<br>`/scopes/23` | `/facts/24`<br>`/relation_records/16`<br>`/scope_records/23` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-130 | `problem-packages.json:/problems/3/complaints/1/combos/0` | `step7-concerns.json:/step8_notes/130` | `/claims/52`<br>`/relation_claims/44`<br>`/scopes/51` | `/facts/52`<br>`/relation_records/44`<br>`/scope_records/51` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-131 | `problem-packages.json:/problems/3/complaints/2/combos/0` | `step7-concerns.json:/step8_notes/131` | `/claims/53`<br>`/relation_claims/45`<br>`/scopes/52` | `/facts/53`<br>`/relation_records/45`<br>`/scope_records/52` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-190 | `problem-packages.json:/problems/9/complaints/0/combos/0` | `step7-concerns.json:/step8_notes/190` | `/claims/112`<br>`/relation_claims/104`<br>`/scopes/111` | `/facts/112`<br>`/relation_records/104`<br>`/scope_records/111` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-191 | `problem-packages.json:/problems/9/complaints/1/combos/0` | `step7-concerns.json:/step8_notes/191` | `/claims/113`<br>`/relation_claims/105`<br>`/scopes/112` | `/facts/113`<br>`/relation_records/105`<br>`/scope_records/112` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-193 | `problem-packages.json:/problems/9/complaints/2/combos/0` | `step7-concerns.json:/step8_notes/193` | `/claims/115`<br>`/relation_claims/107`<br>`/scopes/114` | `/facts/115`<br>`/relation_records/107`<br>`/scope_records/114` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-194 | `problem-packages.json:/problems/9/complaints/3/combos/0` | `step7-concerns.json:/step8_notes/194` | `/claims/116`<br>`/relation_claims/108`<br>`/scopes/115` | `/facts/116`<br>`/relation_records/108`<br>`/scope_records/115` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-200 | `problem-packages.json:/problems/10/complaints/3/combos/1` | `step7-concerns.json:/step8_notes/200` | `/claims/122`<br>`/relation_claims/114`<br>`/scopes/121` | `/facts/122`<br>`/relation_records/114`<br>`/scope_records/121` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-201 | `problem-packages.json:/problems/10/complaints/4/combos/0` | `step7-concerns.json:/step8_notes/201` | `/claims/123`<br>`/relation_claims/115`<br>`/scopes/122` | `/facts/123`<br>`/relation_records/115`<br>`/scope_records/122` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-211 | `problem-packages.json:/problems/11/complaints/7/combos/0` | `step7-concerns.json:/step8_notes/211` | `/claims/133`<br>`/relation_claims/125`<br>`/scopes/132` | `/facts/133`<br>`/relation_records/125`<br>`/scope_records/132` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-212 | `problem-packages.json:/problems/11/complaints/8/combos/0` | `step7-concerns.json:/step8_notes/212` | `/claims/134`<br>`/relation_claims/126`<br>`/scopes/133` | `/facts/134`<br>`/relation_records/126`<br>`/scope_records/133` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-213 | `problem-packages.json:/problems/11/complaints/9/combos/0` | `step7-concerns.json:/step8_notes/213` | `/claims/135`<br>`/relation_claims/127`<br>`/scopes/134` | `/facts/135`<br>`/relation_records/127`<br>`/scope_records/134` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-226 | `problem-packages.json:/problems/13/complaints/0/combos/0` | `step7-concerns.json:/step8_notes/226` | `/claims/148`<br>`/relation_claims/140`<br>`/scopes/147` | `/facts/148`<br>`/relation_records/140`<br>`/scope_records/147` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-227 | `problem-packages.json:/problems/13/complaints/1/combos/0` | `step7-concerns.json:/step8_notes/227` | `/claims/149`<br>`/relation_claims/141`<br>`/scopes/148` | `/facts/149`<br>`/relation_records/141`<br>`/scope_records/148` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-228 | `problem-packages.json:/problems/13/complaints/2/combos/0` | `step7-concerns.json:/step8_notes/228` | `/claims/150`<br>`/relation_claims/142`<br>`/scopes/149` | `/facts/150`<br>`/relation_records/142`<br>`/scope_records/149` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-229 | `problem-packages.json:/problems/13/complaints/4/combos/0` | `step7-concerns.json:/step8_notes/229` | `/claims/151`<br>`/relation_claims/143`<br>`/scopes/150` | `/facts/151`<br>`/relation_records/143`<br>`/scope_records/150` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-230 | `problem-packages.json:/problems/13/complaints/5/combos/0` | `step7-concerns.json:/step8_notes/230` | `/claims/152`<br>`/relation_claims/144`<br>`/scopes/151` | `/facts/152`<br>`/relation_records/144`<br>`/scope_records/151` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ARITY-231 | `problem-packages.json:/problems/13/complaints/6/combos/0` | `step7-concerns.json:/step8_notes/231` | `/claims/153`<br>`/relation_claims/145`<br>`/scopes/152` | `/facts/153`<br>`/relation_records/145`<br>`/scope_records/152` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| NOTE-LINK-109 | `problem-packages.json:/problems/1/complaints/3/combos/0` | `step7-concerns.json:/step8_notes/109` | `/claims/31`<br>`/relation_claims/23`<br>`/scopes/30`<br>`/notes/0` | `/facts/31`<br>`/relation_records/23`<br>`/scope_records/30`<br>`/notes/0` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| NOTE-LINK-110 | `problem-packages.json:/problems/1/complaints/3/combos/1` | `step7-concerns.json:/step8_notes/110` | `/claims/32`<br>`/relation_claims/24`<br>`/scopes/31`<br>`/notes/1` | `/facts/32`<br>`/relation_records/24`<br>`/scope_records/31`<br>`/notes/1` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| NOTE-LINK-111 | `problem-packages.json:/problems/1/complaints/3/combos/2` | `step7-concerns.json:/step8_notes/111` | `/claims/33`<br>`/relation_claims/25`<br>`/scopes/32`<br>`/notes/2` | `/facts/33`<br>`/relation_records/25`<br>`/scope_records/32`<br>`/notes/2` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| NOTE-LINK-132 | `problem-packages.json:/problems/3/complaints/3/combos/0` | `step7-concerns.json:/step8_notes/132` | `/claims/54`<br>`/relation_claims/46`<br>`/scopes/53`<br>`/notes/3` | `/facts/54`<br>`/relation_records/46`<br>`/scope_records/53`<br>`/notes/3` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| NOTE-LINK-133 | `problem-packages.json:/problems/3/complaints/3/combos/1` | `step7-concerns.json:/step8_notes/133` | `/claims/55`<br>`/relation_claims/47`<br>`/scopes/54`<br>`/notes/4` | `/facts/55`<br>`/relation_records/47`<br>`/scope_records/54`<br>`/notes/4` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| NOTE-LINK-134 | `problem-packages.json:/problems/3/complaints/4/combos/0` | `step7-concerns.json:/step8_notes/134` | `/claims/56`<br>`/relation_claims/48`<br>`/scopes/55`<br>`/notes/5` | `/facts/56`<br>`/relation_records/48`<br>`/scope_records/55`<br>`/notes/5` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| NOTE-LINK-135 | `problem-packages.json:/problems/3/complaints/4/combos/1` | `step7-concerns.json:/step8_notes/135` | `/claims/57`<br>`/relation_claims/49`<br>`/scopes/56`<br>`/notes/6` | `/facts/57`<br>`/relation_records/49`<br>`/scope_records/56`<br>`/notes/6` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| ORIGIN-CC-01 | `problem-packages.json:/problems/1/complaints/3` | `step7-concerns.json:/step8_notes/111` | `/claims/33`<br>`/relation_claims/25`<br>`/scopes/32` | `/facts/33`<br>`/relation_records/25`<br>`/scope_records/32` | PASS / 미정 유지 |
| SCOPE-ORDER-01 | `contraindications.json:/rules/0` | `step8-relations.json:/claims/0` | `/claims/154`<br>`/relation_claims/146`<br>`/scopes/153`<br>`/scopes/154`<br>`/scopes/155` | `/facts/154`<br>`/relation_records/146`<br>`/scope_records/153`<br>`/scope_records/154`<br>`/scope_records/155` | PASS / 미정 유지 |
| CAND-volume | `procedure-comparison.json:/comparisons/2` | `step7-concerns.json:/combos/72/members/0` | `/claims/155`<br>`/mappings/283`<br>`/scopes/156`<br>`/scopes/157` | `/facts/155`<br>`/mapping_records/283`<br>`/scope_records/156`<br>`/scope_records/157` | PASS / 미정 유지 |
| CAND-wrinkle | `procedure-comparison.json:/comparisons/1` | `step7-concerns.json:/combos/71/members/1` | `/claims/156`<br>`/mappings/284`<br>`/scopes/158`<br>`/scopes/159` | `/facts/156`<br>`/mapping_records/284`<br>`/scope_records/158`<br>`/scope_records/159` | PASS / 미정 유지 |
| PRODUCT-SCOPE-01 | `taxonomy.json:/modality/3/subcategories/3/items/4` | `step5-units.json:/product_links/243` | `/claims/157`<br>`/mappings/285`<br>`/scopes/160`<br>`/attachments/3` | `/facts/157`<br>`/mapping_records/285`<br>`/scope_records/160`<br>`/edges/3` | PASS / 미정 유지 |
| PROJECTION-K8-0028 | `pre-procedure-checklist.json:/category_specific/1/checks/5/label` | `step8-relations.json:/conditions/not_condition/2` | `/claims/158`<br>`/scopes/161`<br>`/attachments/4` | `/facts/158`<br>`/scope_records/161`<br>`/edges/4` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| PROJECTION-K8-0029 | `pre-procedure-checklist.json:/category_specific/1/checks/6/label` | `step8-relations.json:/conditions/not_condition/3` | `/claims/159`<br>`/scopes/162`<br>`/attachments/5` | `/facts/159`<br>`/scope_records/162`<br>`/edges/5` | PASS / 원문 구조 보존; 임상 재판정 안 함 |
| PATIENT-LANG-01 | `literature-evidence.json:/categories/M2/adverse_effects/2` | `step8-relations.json:/evidence/statements/19` | `/claims/160`<br>`/claims/161`<br>`/claims/162`<br>`/claims/163`<br>`/claims/164`<br>`/scopes/163`<br>`/attachments/6` | `/facts/160`<br>`/facts/161`<br>`/facts/162`<br>`/facts/163`<br>`/facts/164`<br>`/scope_records/163`<br>`/edges/6` | PASS / 미정 유지 |
| RESOLUTION-01 | `taxonomy.json:/modality/9/subcategories/0/items/0/extracted/onset_duration/duration`<br>`taxonomy.json:/modality/9/subcategories/0/items/1/extracted/onset_duration/duration` | `step9-explanations.json:/node_slots/280` | `/claims/165`<br>`/claims/166`<br>`/scopes/164`<br>`/attachments/7` | `/facts/165`<br>`/facts/166`<br>`/scope_records/164`<br>`/edges/7` | PASS / 미정 유지 |

## 독립 대조와 변조 결과

독립 validator는 build.py를 import하지 않는다. 실제 원문 snapshot에서 안전 alias 6필드/16잎, duplicate CC 4행과 taxonomy parent, CC combos146개의 구성·순서·arity, R8-0001 원문 note/interval, 비교 멤버, 제품 scope, 언어5잎, duration2잎을 직접 읽는다. 기존42증거의 모든 원문/실버 locator/hash/value도 다시 대조한다. 그래프와 pilot의 일치 검사만으로 합격시키지 않는다.

변조 31개는 아래와 같고 모두 거부됐다. 각 실패 check 이름은 validation.json에 기록했다.

- `alias_merge_overwrites_original_list`: 거부
- `drop_whole_alias_source_claim`: 거부
- `same_name_first_match_wrong_scope`: 거부
- `collapse_duplicate_legacy_occurrence`: 거부
- `duplicate_legacy_auto_selection`: 거부
- `singleton_promoted_to_pair`: 거부
- `nary_member_deleted`: 거부
- `note_claim_reference_deleted`: 거부
- `note_wrong_R8`: 거부
- `first_condition_deleted`: 거부
- `first_unconditional_a`: 거부
- `explicit_no_order_conflated_with_not_declared`: 거부
- `same_site_endpoint_swap`: 거부
- `candidate_promoted_to_selected`: 거부
- `product_M4_override_extended_to_M2`: 거부
- `staff_check_promoted_to_confirmed`: 거부
- `palja_neck_conflict_erased`: 거부
- `ko_qualifier_omitted`: 거부
- `duration_alternative_erased`: 거부
- `policy_promoted_to_clinical_consensus`: 거부
- `wrong_source_hash`: 거부
- `wrong_source_pointer`: 거부
- `existing_mapping_rule_dropped`: 거부
- `unknown_extra_field`: 거부
- `invalid_enum`: 거부
- `null_instead_of_empty_selected_list`: 거부
- `missing_required_raw_field`: 거부
- `identity_from_name`: 거부
- `duration_fake_reviewer`: 거부
- `ambiguous_expansion_first_match`: 거부
- `automatic_confirmed_graph_edge`: 거부

## 보호 입력·남은 범위

시작/종료 manifest **178/178** 파일의 SHA256/bytes가 일치했다. 원문21, 기존 실버/decisions/생성기/semantic/소비 코드 및 기존 HTML/design/audit 입력은 불변이다. 현재 활성 DB publication 판은 조회하지 않았다. 작성 경로는 `silver-design-pilot/` 하나이며 하위워커·외부모델·네트워크·설치·commit/push/PR을 사용하지 않았다.

실제 검토 분모는 기존42사례, 안전3충돌행/6field/16잎, duplicate CC2키/4행, CC combos146전수, note7, R8조건1행, 비교멤버2개, 제품 override1행, K8두행, 언어5claim, duration2claim/1resolution이다. 이 범위를 제외한 실버1~9 전체의 의미 이관/전수 임상 검토는 미착수다. 선행9785비교나 HTML1600검사를 이번 새 검토 수로 합산하지 않았다.

특히 원안의 세부 의미 미검토1277칸, 전체 안전580행, 전체 concern/combination 이관, duration②196슬롯/343 alternatives의 전수 이관, 임상·허가·문헌 최신성, 실제 Gold/API/DB/서비스/탐색 구현은 완료하지 않았다. 다음은 코디 검증과 독립 검수이며, [gaps.md](gaps.md)의 pilot refinement와 LOSS-02 예시 오류를 함께 검토한 뒤 본 설계 확정/정본 이관 준비로 넘어간다.
