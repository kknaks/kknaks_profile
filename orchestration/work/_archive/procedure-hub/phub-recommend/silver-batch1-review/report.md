# WORK-013 P5 독립 candidate 검수

Task `task_6f7a81a87954` · Dispatch `ctx_2feb82da4910` · 2026-11-03

**최종 판정: FAIL — 원문 보존·현재 candidate 분모·기존 회귀는 PASS이나, 독립 source validator가 범위 발명과 typed 관계 소실을 거부하지 못한다.** 정본전환을 승인하지 않는다. 이번 검수는 완료했으며 migration/candidate를 고치지 않았다.

## 1. 발견사항

### BR-H1 · High · scope 원문 의미 검증이 구조 검사에 그친다

`silver-batch1-migration/validate.py`의 scope 검사는 집합 교차/중복, 참조 도달성, explicit 비어있음, qualifier의 operator/value=null을 검사하지만 원문에 의해 허용되는 축별 포함·제외와 qualifier 전체를 복원해 대조하지 않는다. 현재 candidate의 scope 자체가 잘못되었다는 판정이 아니라, 잘못된 candidate도 승인하는 검증 결함이다.

**반례 A:** `step1-products.json#/items/0`의 제품 `product:M1-2-1` scope에 원문에 없는 `excluded=["product:M1-2-3"]`를 넣는다. 대상 scope는 `scp:889c1d46993c0d30a9e4c8515f79c64bc8adfe740483eb16b837ace6e7b26d36`, 원천 sourceID는 `src:6e1013da872e1e9b231cc023c5f4cf0185f9f9db435801ad39908b3965bf4771`이다. 원문에는 이 제품 제외 규칙이 없다. normalized ID 32개를 재계산하고 모든 파생 sidecar 참조와 output-manifest의 hash/bytes도 맞췄다. **전체 validate CLI exit=0, verdict=PASS, failure_count=0**으로 수용했다.

**반례 B:** 안전 원천 `taxonomy.json#/modality/0/subcategories/0/items/0`와 `step5-units.json#/extracted/0`에 연결된 scope의 `statement_qualifiers`를 통째로 삭제한다. 대상 scope는 `scp:cf2f38e50072b9c208f73d6eb62f02ef6fb26a0486d2a8bf8268814135810ff8`이다. 삭제한 원문 context는 `{attach:"제품 × 계열", family:"M1", shown_on:[], sub_family:null}`이며 sourceID는 `src:0a8dc35dd118d219ccd414cb31092179b218a142365407686a7f3b35e7a8d58b`이다. normalized ID 11개와 sidecar/manifest를 정합화하자 **전체 CLI exit=0, PASS, failures=0**이었다. 원문 root 보존만으로 typed scope의 조건 소실을 탐지하지 못한다.

정상 대조는 원 candidate의 `excluded=[]` 및 원문 context qualifier 유지 상태이며 전체 검증 PASS다. safety raw 값을 별도 변조한 음성 대조는 ID 재계산 후 `CLAIM_RAW`와 `SAFETY_RAW`로 거부되었다. ID나 output checksum 검출만을 의미 검증이라고 세지 않았다.

수정 범위: 원문 source와 field-contract로 각 scope 축의 knowledge/value_kind/included/excluded/raw_refs 및 qualifier raw/source/state를 독립 복원해 exact 비교한다. 원천에 없는 제외값과 qualifier 삭제·치환은 관련 의미 진단으로 거부하고, 정상 explicit/unknown/미해석 context는 그대로 허용해야 한다. 임상 해석이나 새 scope 설계는 요구하지 않는다.

### BR-M1 · Medium · 명시적인 product.line_memberships 삭제를 탐지하지 못한다

`validate.py`의 product line 검사는 **존재하는** membership의 부모가 허용된 집합에 속하는지만 확인한다. 원문에서 기대되는 membership 전체 집합과 누락 여부는 검사하지 않는다.

`step1-products.json#/items/35`의 `ledger_id=auto-M2-1775364775108`은 `line={line_name:"더채움", role:"품목", line_row:"M2-1-2", decision:"D07"}`이다. 현재 candidate는 `parent_product_ref="product:M2-1-2"`, role="품목", decision_ref=null로 정확히 보존한다. 이 제품의 `line_memberships`만 `[]`로 바꾸고 output hash/bytes를 갱신하면 **전체 validate CLI exit=0, PASS, failures=0**이다. native product는 normalized graph-ID 대상이 아니므로 이 경우 재계산으로 바뀐 ID는 0개다. 원문 sourceID는 `src:dedce87d37d1728f5cb075ab64ad31f76fd673180314b6fdd1ae6ae9609b63d5`이며 원문 자체는 그대로 남았다.

현재 올바른 typed 연결과 기존 `invent_line_parent` 부정시험의 거부가 정상 대조다. 없는 부모 발명은 잡지만 있는 부모 삭제는 통과한다. 원문 row.line과 lines.items의 명시 ledger_id/line_row만으로 기대 membership을 복원해 누락·추가·role 변조를 모두 검사해야 한다. 이름 기반 부모 추정이나 승인 decision 발급은 요구하지 않는다.

## 2. 재현 증거와 실행 경계

[full-cli-probes.json](full-cli-probes.json)은 제외값 발명과 line 삭제의 전체 CLI 결과·정상 before·변경내용을, [full-qualifier-probe.json](full-qualifier-probe.json)은 qualifier 소실의 전체 결과를 담는다. 각각 `full_cli_probes.py`, `full_qualifier_probe.py`로 재현한다. 이들은 원 candidate를 복사한 검수 폴더에서만 records와 파생 sidecar를 수정하고 모든 normalized 참조와 output hash를 맞춘 다음, **수정하지 않은 원본 validate.py CLI의 evaluate+sidecar_checks+export/hash 검사를 모두 실행**한다.

[additional-probes.json](additional-probes.json)의 초기 메모리 시험에서 qualifier 삭제는 낡은 sidecar 참조 때문에 FAIL 3건이었다. 관련 원문 의미 진단은 없었고, sidecar를 재연결한 전체 CLI 시험에서는 PASS로 바뀌었다. 따라서 이 초기 FAIL을 의미 검증의 성공으로 해석하지 않는다.

쓰기 sink와 tmp는 모두 `silver-batch1-review/`로 돌렸다. 빌더는 원본 소스를 메모리에서 읽어 `permitted` 출력 경로 guard 한 곳만 검수 복사본으로 바꿨다. `__file__`, HERE, 입력, 코드 hash 계산과 변환은 원본 그대로이므로 deterministic 결과가 원 candidate와 byte 단위로 같다. `sandbox_build.py`와 `sandbox_repro.py`에 이 변경이 명시되어 있다. 검수 wrapper 첫 실행에서 변수 오타로 빌더 실행이 시작되지 않았으며 이를 바로잡고 성공한 전체 2회+이동시험을 다시 수행했다. 해당 실행 오류는 제품 결함으로 세지 않았다.

재실행은 레포 루트에서 다음 순서로 한다. 검수 완료 후 대용량 실행 복사본과 변조 tmp는 제거했고 결과 JSON과 harness를 남겼다. 재실행 시 이미 생성된 검수 복사본/cli 폴더가 있으면 wrapper는 교체하지 않고 실패한다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-review/prepare_execution.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/validate.py --candidate orchestration/work/phub-recommend/silver-batch1-review/execution-copy --independent-source
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/test_contract.py --candidate orchestration/work/phub-recommend/silver-batch1-review/execution-copy
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-review/sandbox_repro.py --candidate orchestration/work/phub-recommend/silver-batch1-review/execution-copy --trials 2 --relocate-inputs
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-review/independent_review.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-review/full_cli_probes.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-review/full_qualifier_probe.py
```

## 3. 독립 확인한 정상 범위

원문을 직접 읽은 별도 [source-direct.json](source-direct.json), 실행한 원 검증기의 [validation.json](validation.json), [counterexamples.json](counterexamples.json), [reproducibility.json](reproducibility.json)을 근거로 한다. 기존 validator의 1,320,125 checks/실패0/skip0은 개별 사실이나 임상 검토 수가 아니다.

| 대상 | 실제 확인 | 판정 |
|---|---|---|
| 승인 입력 | v2 69파일의 full SHA256/bytes, raw21 21/generated18/research11/decision13/audit6 | PASS |
| 원문 전체 | 비감사 63파일 root 전체 raw deep equal, source_record 23,255개의 실제 pointer 값 대조 | PASS |
| 제품·계열 | product395, active354/inactive41, family27, membership354의 ledger ID집합=active집합 | PASS |
| 미정 연결 | family null3/pending_director3 및 계열 밖5 유지, 임의 기본 family 없음 | PASS |
| source row | 395+27+354+580=1,356행 | PASS |
| 안전 원문 | items521/products59=580행, 1,394field, 4,170scalar leaf, 각 field별 source occurrence와 claim 1개, 값·순서·빈값 보존 | PASS |
| 충돌 복구 | 3행 6field의 before6leaf→after16leaf, 소실10복구, 다대일 predicate여도 raw claim 별도 | PASS |
| 정상 rename | common_adverse_effects2/common_side_effects1/serious_adverse_effects2, onset의 고정 규칙·기존 keys 회귀 | PASS |
| override | units248+product_links376=624, metadata/legacy/before와 field별 after 원문 claim 연결 | PASS |
| attachment | eligible1,242/not_created152 서로소·합1,394, owner와 target·scope 일치, unknown/witness=[]/resolution=null | PASS |
| 미부착 | candidate_only49/out_of_batch_entity83/owner_unresolved20, 전체 raw claim 유지, attachment0 | PASS |
| 임상 경계 | 새 decision/relation/resolution0, normalized_value=null, review unreviewed/source_conflict 유지 | PASS |
| 제품 typed | 허가·spec·업체 role별 원문 claim, continuity 명시 source, 라인 명시 ledger_id 관계 현재값 | PASS, 누락 탐지 BR-M1 별도 |
| scope 현재값 | explicit owner/family, 미해석 context·unknown 적용 유지 | 현재값 PASS, 검사 완결성 BR-H1 FAIL |
| 84/247 coverage | implemented74, decision 원문보존 typed0 8, subfamilies needs_design1, technique 제한 registry1, 범위 밖163 변화실적0 | PASS |
| registry | unit96/technique17의 실제 ID·source 도달성만, 전수 typed로 세지 않음 | PASS |
| ID/판 | source/normalized/native ID 수명, ID refs/cardinality/type, collection null+reason와 파일별 version 원형 | PASS, 의미 게이트 BR-H1/BR-M1 별도 |
| 감사 분리 | audit6은 별도 snapshot/sidecar, semantic source_refs와 normalized payload에서 분리 | PASS |
| 구현검사 독립성 | validate는 builder/rules 변환을 import하지 않고 transport만 공유, 실제 원문·고정 oracle와 rule hash/authority 대조 | PASS, 검증 누락 별도 |
| 기존 시험 | negative35/35, positive14/14 모두 재실행 PASS, 부정값은 지정 의미진단/normalized ID 실패0 | PASS |
| 실제 재현 | 새 tmp 2회 생성, deterministic export13개+output-manifest가 원 candidate와 byte/hash 동일 | PASS |
| 실제 이동 | 69파일 domain/logical key로 물리 복사, 동일 manifest bytes, relocated input 실제 read69, 출력 동일 | PASS |
| fail-closed 입력 | 이동된 taxonomy bytes 변조와 새 manifest rebaseline 각각 nonzero 거부 | PASS |
| ID 수명 probe | audit/source/schema/rule/label/행재정렬 6개, 실제 이동 외 수명 probe는 메모리 변조임을 구분 | PASS |
| 기존 pilot 회귀 | 42사례/146combo(21/119/6)/note7/언어5/duration2대안, 참조원문13파일 고정·실제 occurrence582 | PASS, 신규 실적0 |

84개 키의 타입은 required 및 nested type 검사로 확인했고, source_refs 존재나 raw root 보존을 typed 완료로 대체하지 않았다. decision8은 typed 미구현·승인 미발급, subfamilies는 typed=[]+needs_design, technique_defaults는 기존 ID/role/layer/basis 원문을 둔 제한 참조다. raw16잎의 복구를 안전 의미 normalization이나 임상 승인으로 올리지 않는다.

## 4. 미부착 152필드의 owner·사유 확인

[not-created-source-review.json](not-created-source-review.json)에 원천62행의 native ID/raw pointer/claim/source refs와 사유를 남겼다. candidate19행49field, 원문보관37행83field, owner_unresolved6행20field다. 후보19+원문보관37의56행132field만을 미부착 전체라고 쓰지 않는다.

owner_unresolved는 다음과 같으며 이름이나 ID 모양으로 owner를 추정하지 않았다.

| source native ID | field수 | 단일 owner 미확정 이유 |
|---|---:|---|
| M1-3-1 | 4 | units 5개 |
| M1-3-7 | 4 | units 3개 |
| M1-3-8 | 3 | units 3개 |
| auto-3-1774737181584 | 4 | units U5-016/U5-017 둘 |
| M4-P-3 | 3 | current units=[U5-009]지만 실제 U5-009.sources는 M1-3-5만 지칭, M4-P-3 명시 ledger 근거 없음 |
| auto-M16-1775403176937 | 2 | units 3개 |

LOSS02 `auto-2-1774737181584`는 단일 unit `unit_procedure:U5-016`으로 정상 부착되며 위의 서로 다른 `auto-3` 미부착 행과 혼동하지 않는다. 현재 미부착 분류의 오분류는 발견하지 않았다. 따라서 카드 worker에게 변경할 claim/sourceID 분류 정정은 없다. scope·line 검증 결함을 미부착 오분류라고 보고하지 않는다.

## 5. 판 고정·무변경·전환 전제

[review-input-output-manifest.json](review-input-output-manifest.json)은 DATA-001/2·WORK-013·84필드계약·승인 v2·collections/reconciliation 및 candidate input/output/rule/verification manifest의 full hash/bytes를 고정한다. candidate output-manifest SHA256은 `fb3a0e58493189e508764ebebd947b7e0920a948b4fdb3af8b0cdfe8685eebe1`이다. input manifest는 승인 v2와 일치하며 deterministic 13개 파일의 hash/bytes가 모두 맞았다.

검수 시작/끝 [protected-start.json](protected-start.json)·[protected-end.json](protected-end.json)의 **1,640파일 변경0**을 확인했다. 입력·정본·migration 전체·candidate 전체·구현 보고·계약·기존 pilot/review/design/semantic/스펙/원장이 포함된다. 공유 변경이 없어 판을 혼합하지 않았다. 구현 당시 protected-start를 그대로 현재 baseline으로 쓰면 이미 과거에 바뀐 reference WORK.md 한 파일을 변경으로 보므로, 이번 검수는 이번 시작판을 따로 고정했고 그 차이를 이번 작업 변경으로 오인하지 않았다.

검수 폴더 외 쓰기0, 원 candidate·정본 변경0, 정본전환0, 네트워크/모델/설치/하위worker/commit/push/PR/앱·Hub/env/DB/서버 실행0이다. 원천 69판의 역사적 허가 문자열을 보존했을 뿐 허가 최신성·임상 적용·전체247필드 완료를 승인하지 않는다.

BR-H1/BR-M1을 원 구현 worker가 수정한 뒤, 원문 기반 정확한 정상 대조와 이번 3개 추가 반례를 모두 의미진단으로 거부하는 독립 재검수가 필요하다. 고정 manifest·정본 무변경·기존35/14·2회 재현·실제 이동도 수정판에서 다시 확인해야 한다. 그 후에도 정본전환은 별도 계약으로 소비자 호환성/읽기경로·schema판/백업·승인자/rollback을 확정하고 명시 권한을 받아야 한다. 현재 비활성 candidate를 소비자 입력으로 삼지 않는 상태가 유지된다.
