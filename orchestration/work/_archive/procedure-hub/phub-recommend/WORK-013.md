---
type: work
id: WORK-013
title: "제품·계열 typed candidate와 안전 원문 첫 이관 묶음"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: change
progress: 0
created_at: 2026-11-03
updated_at: 2026-11-03
links:
  data: "DATA-001.md"
---

# WORK-013 — 제품·계열 typed candidate와 안전 원문 첫 이관 묶음

작성일 2026-11-03 · 상태 `todo` · 모든 구현 phase TODO.

## 1. 실행 전제와 소유

이 문서는 [DATA-001](DATA-001.md)이 완성된 뒤 작성한 **구현 발주 계약**이다. 현재 이관기/스키마/candidate는 아직 없다. 다음 코디네이터가 이 문서와 [84필드 계약](silver-data-contract-batch1/field-contract.json)을 브리프에 고정하고 구현→독립 검수 순으로 발주한다. DATA-001의 구조 계약을 바꾸려면 문서 검수에서 먼저 결정하고 구현자가 임의 해소하지 않는다.

코드·출력 모두 같은 slug `orchestration/work/phub-recommend/` 안이다. 기존 step1/2/5 정본은 read-only 입력이며 candidate 검수 전 덮어쓰지 않는다. 사용자서비스·앱·Hub·backend·DB·Gold·semantic·네트워크·모델·설치·서버·스킬·원장/decisions/apply·HTML/design·pilot v1/v2·기존 review·기존 SPEC/WORK는 수정하지 않는다. worker commit/push/PR/하위worker 금지다.

### allowed_paths — 다음 구현 worker

| 경로 | 허용 내용 |
|---|---|
| `orchestration/work/phub-recommend/silver-batch1-migration/**` | 새 표준라이브러리 이관기·schema·ref-contract·고정 규칙 manifest·독립 source validator·positive/negative 테스트·README |
| `orchestration/work/phub-recommend/silver-batch1-candidate/**` | 새 candidate만: 전체 typed records·원문 claims·source/mapping/identity ledger·coverage·검증 결과·input/output manifests |
| `orchestration/work/phub-recommend/silver-batch1-implementation/report.md` | 구현 보고(실제 분모/오류/미정/검증 명령) |

그 외 경로는 쓰지 않는다. DATA-001/WORK-013/이번 field-contract/coverage baseline은 입력이다. 독립 검수 worker는 별도 `silver-batch1-review/**`만 쓰도록 다음 코디가 브리프에 지정한다. 이 문서 자체는 검수·정본전환을 실행할 권한이 아니다.

## 2. 입력판과 분모

작업 cwd는 현재 profile workspace 루트다. [input-manifest.json](silver-data-contract-batch1/contract-fix/input-manifest.v2.json)의 file/logical_file_key/domain/full SHA256/bytes를 입력 기준으로 사용한다. raw21 21/generated18/research11/decision13/audit6의 collection membership도 [collections.json](silver-data-contract-batch1/contract-fix/collections.json) 그대로 고정한다. 이전 manifest는 역사 증거이며 builder 입력이 아니다. `_RESUME.md` 대신 승인된 frozen snapshot만 읽고 [reconciliation](silver-data-contract-batch1/contract-fix/reconciliation.json)을 따른다. collection별 source_kind/버전과 파일별 meta는 DATA-001 §2.1에 따른다. raw21 루트는 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26`이며 파일21개 전체다. locator 루트 재배치 옵션을 제공하되 logical_file_key/domain/collection은 유지한다. 달라진 hash는 조용히 재baseline하지 말고 중단·보고한다.

추가 조사 artifact가 필요한 경우 기존 파일을 참조하되 먼저 명시 manifest에 확정하고 review evidence에 차이를 남긴다. 원문 근거가 없으면 null/미정으로 보존하며 최신 허가를 찾기 위한 네트워크조회는 하지 않는다. JSON 외 역사 .md/.py는 hash/bytes와 실제 인용 line 범위로 evidence locator를 보존한다. 이를 JSON source_record로 취급하려면 새 schema에 media_type/text-root(pointer="") transport를 선언하고 decoded text/bytes 재대조 positive를 추가한다. 이 확장 없이 가짜 JSON Pointer를 만들지 않는다.

| 입력 | 전체 출력 대상·oracle |
|---|---|
| step1-products.json `/items` | 395 typed product identity(고유 ledger_id395); active354/inactive41. 비제품으로 옮겨진 기록도 tombstone/continuity/raw를 남기며 삭제하지 않는다. |
| step2-families.json `/families` | family27(M17+N10); 각 전체 원문과 typed 필드. |
| step2-families.json `/product_family` | 354 mapping source행; ledger_id 집합=active 제품 집합. family null3/pending_director3 유지. mapping record 수가 목적 분리에 따라354보다 늘면 source행별 인덱스/파생사유를 제공한다. |
| taxonomy.json `/modality/*/subcategories/*/items` ↔ step5 `/extracted` | 521 source행 전부, 각 safety.*·aftercare 원문 보존. |
| taxonomy.json `/modality/*/products` ↔ step5 `/taxonomy_products` | 59 source행 전부. 두 집합 합580은 입력행 수이며 안전 field/leaf/clinical claim 수가 아니다. |
| step5 `/product_links`·`/units/*/side_effect_override` | 기존 override624항목(units248/product_links376) inventory 및 source_text/source claim 연결. unit/product compatibility·선택·적용승인을 새로 판정하지 않는다. |
| step4 `/family_defaults`·`/nodes` | 계열 기본기법의 실제 registry ID 도달성만 검사; 외부 참조 보존이며 기법 전수이관 아님. |

[580행 locator](silver-data-contract-batch1/results/safety-origin-locators.json)와 [현재 재집계](silver-data-contract-batch1/results/recount.json)는 구현기 밖의 초기 oracle이다. 재집계는 source가 바뀌면 새 판 승인이 필요하며 이름이나 배열index만으로 임의 연결하지 않는다. step1 연구·고정본·허가/KPIC 근거는 manifest의 실제 artifact에서 source/역사적 주장으로 보존한다.

## 3. candidate 출력 계약

출력은 `silver-batch1-candidate/` 한 경로이며 원본과 혼동할 stepN 정본명으로 외부에 덮어쓰지 않는다. temp 작업도 이 폴더의 명시 `tmp/` 아래에서만 수행하고 검증 후 제거한다.

| 파일 | 필요한 내용 |
|---|---|
| `input-manifest.json` | 원본 manifest 복사·실제 hash/bytes 대조·domain/collection/logical key/locator. hash 미일치면 build 실패. |
| `schema.json`, `ref-contract.json`, `rule-manifest.json` | 새 schema/rule판, union/cardinality/nullability, 구현파일 SHA256, 고정 독립 기대값과 source판. 원래 pilot판을 재사용했다고 위장하지 않는다. |
| `records.json` | snapshots/source_records/products/families/scopes/claims/mappings/decisions/attachments·field_states. 추가 relation/resolution은 이번 신규 생성 없음. entity type/native_id + 실제 typed properties 포함. |
| `source-row-index.json` | product395/family27/product_family354/safety580의 각각 source occurrence와 output refs. source→typed→claim→attachment 역추적, 보존만/미정/미발급 표기. 미부착 claim은 attachment_state=not_created+attachment_reason+mapping/source/claim refs 필수이며 eligible 분모와 별도 집계. |
| `identity-ledger.json` | 기존 ID→새 namespace ID 집합·legacy alias·source 판·line/merge/move 이력·정확/후보/미정·사유. native ID 재발급/이름 first-match 금지. |
| `mapping-ledger.json` | field/source별 identity/membership/normalization/compatibility 목적 분리·후보/선택/제외/판정근거·rule hash. |
| `safety-claims.json` | 580행별 모든 원문 safety.*·aftercare field와 각 raw pointer/value, normalized predicate, source/scope/mapping refs. 충돌은 원천6field/16잎을 별도 유지. `records.json` claims와 중복 저장 시 derived export로 선언하고 deep equal 검사. |
| `override-projection.json` | 기존 대상/level/family/priority/values와 source claim refs·원문 field ref 연결, collision 수정 before/after. 적용상태 unknown. |
| `coverage.json` | 247 proposed 키 일대일 유지 + baseline_status/batch_status/source_count/typed_count/raw_count/empty_count/oracle/result. core 전송 확장은 별도 분모. |
| `validation.json`, `counterexamples.json`, `source-diff.json` | 검사별 분모/실패/스킵/진단 및 입력 원문 직접 대조; 충돌 before/after와 정상 rename 회귀. |
| `output-manifest.json` | deterministic 출력의 hash/bytes·schema/rule판·생성명령·입력 manifest hash. 실행시각은 별도 실행메타이며 deterministic payload ID에 넣지 않는다. |

기존 prototype 네 칸(id/type/native_id/source_refs)은 그대로 유지하며 product14/family11 typed property를 추가한다. source_refs가 있다는 이유로 license/spec/company/line/definition이 typed 완료됐다고 세지 않는다. [필드 계약](silver-data-contract-batch1/field-contract.json)84행 각각을 실행 계약으로 사용한다. 필수/빈값 원규약은 `proposed_contract`, 이번 변환/예외는 `transform` 및 DATA-001 우선순위를 따른다. field별 `oracle`을 독립 source 판독으로 구현한다.

단위 owner 참조는 필요한 unit ID만 원본 step5.units에 도달하는 제한 registry로 보존한다. LOSS02 target은 `unit_procedure:U5-016`이다. 이를 새 unit full typed 이관으로 세지 않는다. 제품·계열을 연관된 모든 임상 fact의 owner로 확장하거나 family membership을 제품안전 적용으로 해석하지 않는다.

family.subfamilies는 원문/legacy 관계를 모두 보존하되 stable key/axis 미발급, typed=[]+field_state=needs_design+raw_refs다. 이 필드는 전체 typed 완료에서 제외한다. purpose.id도 새 발급하지 않는다. technique_defaults는 참조 보존까지며 전체 의미 이관 완료로 세지 않는다. 이러한 예외는 구현 실패를 숨기기 위한 skipped가 아니라 사전에 승인된 범위다.

## 4. 구현 단계와 실행 인터페이스

다음 명령은 **향후 구현자가 제공해야 할 CLI 계약**이다. 현재 존재하거나 실행한 명령으로 보고하지 않는다. Python 표준라이브러리만 사용하며 설치·외부모델 없이 동작해야 한다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/build.py --inputs orchestration/work/phub-recommend/silver-data-contract-batch1/contract-fix/input-manifest.v2.json --field-contract orchestration/work/phub-recommend/silver-data-contract-batch1/field-contract.json --output orchestration/work/phub-recommend/silver-batch1-candidate
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/validate.py --candidate orchestration/work/phub-recommend/silver-batch1-candidate --independent-source
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/test_contract.py --candidate orchestration/work/phub-recommend/silver-batch1-candidate
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/check_reproducible.py --candidate orchestration/work/phub-recommend/silver-batch1-candidate --trials 2 --relocate-inputs
```

`build.py`는 기존 canonical 파일에 대한 쓰기 옵션을 제공하지 않는다. 기존 candidate가 다르면 명시 실패하고, 동일 입력 재생성은 별도 candidate/tmp/run-N으로 수행한다. 이동시험은 input locator 루트만 복사/재배치하며 logical key/collection 불변, manifest bytes 동일을 확인한다. 검증 실패의 exit code는 nonzero이고 모든 진단은 source locator·field·reason을 포함한다. validator가 builder의 transform 결과/기대 fixture를 정답으로 import해서는 안 된다.

| phase | 상태 | 산출·완료 증거 |
|---|---|---|
| P0 입력 고정·독립 census | TODO | manifest 일치·395/354/27/580·모든 safety field/leaf·override 항목·정확 join·null/[]/false/missing census. |
| P1 schema/ID/refs·필드 대응 | TODO | 새 schema/ref/rule판, DATA84행의 실제 타입/nullable/원천대응, metadata 예외 명시, 정·부 fixture. |
| P2 전수 candidate 생성 | TODO | product395/family27/mapping source354/safety580 전체 source-row-index 및 typed/raw 구분. |
| P3 원문/충돌·override·분모 검증 | TODO | 3collision6field16잎과 기존10잎 복구·모든 정상 rename·원문이력·unknown/candidate 유지. |
| P4 재현성·이동·반례·보호입력 | TODO | deterministic 두 실행 동일, 이동 불변, schema/rule/원천변조 탐지, 입력 변경0, report. |
| P5 독립 candidate 검수 | TODO | 별도 read-only reviewer가 원문 직접 대조·PASS/WARN/FAIL. 실패면 candidate 수정/재검수. |

## 5. 수용 기준과 필수 반례

1. **전수 분모**: product395 unique native IDs·active354/inactive41·family27·product_family source354·safety source580을 source-row-index에서 재구성한다. 누락0/임의 추가0, 원문ID 집합과 일치한다. 비활성·이동·병합은 삭제하지 않는다. raw21 밖 역사 조사 ref도 실제 존재/file hash/인용 위치를 제공한다.
2. **필드 계약**: product14/family11 및 공통59의84키마다 baseline 상태와 실제 batch 상태를 별도로 낸다. needs_design/제한 registry 예외를 typed 전수완료 분모에서 제외한다. 247 baseline 전체를 보존하고163개 범위밖 필드는 변경실적0으로 유지한다. 원문 전체보존과 typed 변환을 따로 검사한다.
3. **원문 deep equal**: 580행 전체의 모든 safety.*·aftercare 원문 field1,394개/scalar잎4,170개를 [field oracle](silver-data-contract-batch1/results/safety-field-oracle.json)의 exact pointer에서 독립 읽는다. missing/null/[]/false/중복/배열순서를 보존한다. normalizer의 before→after는 raw pointer→normalized predicate만이며 원문을 재작성하지 않는다. 아직 해석하지 않은 필드는 explicit unresolved이고 가짜 기본값이 없다.
4. **충돌 정정**: common 충돌3행의6field/16잎이 서로 다른 claim/source로 도달하고 기존 소실10잎이 모두 존재한다. before6잎과 after16잎을 field별 표시한다. LOSS02는 U5-016이다. 기존 정상 serious/onset/common rename과 비충돌 source_text/override는 동일 원문 근거를 유지한다. 전체 override inventory에서 source claim·level/family/priority를 대조하고, collision이 override로 전파된 손실도 복구한다.
5. **임상 경계**: exact identity/계열연결은 유지하되 compatible_candidate/selected/application을 혼동하지 않는다. 원문1394field=eligible+not_created(서로소), 전체580행/4170잎 zero-loss와 attachment eligible coverage를 따로 검사한다. 나머지524행1262field도 owner 검증 없이 자동 eligible로 세지 않는다. attachment는 batch1-source-preservation/2의 단일 owner만 unknown/witness=[]/resolution=null, 새 clinical consensus/승인0. 기존 open·허가확인불가·미허가·후보·conflict·pending_director는 그대로 보존한다.
6. **ID/refs**: 모든 참조 type/도달성/cardinality 검사. 원문파일 이동/label 변경/행재정렬의 수명을 구분한다. 이동은 ID 불변; 행재정렬은 source snapshot/occurrence 변경·entity ID 유지; schema/rule판 변경은 normalized ID 변경; design 감사 hash만 변경해도 normalized ID 불변.
7. **rule 진실성**: 실제 파일 hash·version·원천결정/authority를 고정 선언과 대조한다. forged id/version/hash와 source decision 위조를 ID 재계산 이후에도 의미진단으로 거부한다. 미확정 rule=null+reason을 정상 수용하고 reason 삭제는 거부한다. 과거 source version을 새 batch 승인판으로 위장하지 않는다.
8. **보호**: 입력 manifest 및 기존 정본·pilot·review·design·semantic·스펙/원장을 시작/끝 hash+bytes로 비교해 변경0을 보고한다. 정본전환/Gold/서비스 작업은 실행0이다.

필수 부정 사례는 원문 claim 한쪽 삭제, normalized predicate 다대일 overwrite, safety 원문 순서/빈값 변조, 정상 serious rename 소실, LOSS02 product 오분류, 근거없는 merged_into/line parent 발명, 잘못된 ledger_id join, 후보 selected 자동승격, family=null 기본값 채우기, clinical confirmed 자동승격, 타입오류/끊긴 ref, scope 포함·제외 교집합/중복, explicit→unknown 은폐, 무관 parent, nullable rule 사유삭제, 위조 rule/version/hash, design hash의 ID 오염이다. normalized ID를 재계산한 변조에도 원문/의미진단이 실패해야 한다. ID 위조 하나만 거부하고 의미검증을 했다고 주장하지 않는다.

정상 positive는 후보19행+원문보관37행의132field 전체 claim 보존/attachment 미생성 및 mapping/source-row-index 사유 유지, 실제 단일 owner 검증 후에만 attachment 생성, collection별 null source_version+reason 및 파일별 정수/문자열/missing/null version 원형 보존, audit-only snapshot 변경에도 source_refs를 포함한 unchanged-data normalized ID 불변과 source-data 변경시 dependent ID 변경, raw16잎/빈값·정상 rename, 기존 exact identity, null rule+실제 reason, 미정 후보 보존, needs_design 원문/legacy 연결 보존, source parent/continuity null, 제한 registry의 실제 target 도달이다. pilot의 42사례·146combo·note7·언어5·duration 대안은 immutable fixture에서 회귀 읽기검사하고 결과를 신규 이관 건수에 더하지 않는다. 원본 pilot runner가 파일을 생성한다면 원본에서 실행하지 말고 candidate/tmp로 저장위치를 돌린 별도 regression harness를 사용한다.

## 6. candidate 검수·정본전환·되돌리기의 분리

**이번 구현 종료점은 candidate PASS와 보고**다. 독립 reviewer의 source oracle·보호입력·coverage·반례 검증 결과를 다음 코디가 직접 재실행한 뒤 사용자에게 candidate 검수 결과를 제시한다. 이것이 자동으로 정본전환 권한을 주지는 않는다.

정본전환은 별도 작업으로 정본 권한/소비자 호환성/읽기경로·schema판·스냅샷 보관·승인자를 먼저 확정한다. 검수된 candidate의 input/output hash를 고정하고 기존 정본 전부의 별도 immutable backup+manifest를 확보한 뒤 명시된 소비자만 새 판으로 전환한다. 경로를 바꾸는지 파일을 교체하는지는 그 전환 계약에서 결정한다. 이 문서에 자동 copy/apply 명령을 포함하지 않는다.

candidate 단계 rollback은 candidate를 활성 입력으로 삼지 않고 이전 정본을 그대로 유지하는 것이다. candidate 결과는 실패 판정/근거와 함께 보존한다. 정본전환 이후 rollback은 별도 승인된 이전 publication/manifest를 기준으로 이전 입력판과 소비자 읽기경로를 복원하고 hash/건수/회귀를 대조하는 절차다. DB·Gold publication을 이번 파일작업과 묶어 바꾸지 않는다.

## 7. 완료보고 항목

실제 채택한 구조/새 schema판, 입력분모와 출력분모,84필드별 typed/raw/needs_design/제한 registry 상태, collision before/after6field16잎, 원문 미정과 임상 미정, 실패/반례/재현성·이동 결과, 보호입력 변경0, 정본전환 미실행을 나눠 보고한다. 구현 전인 이 문서를 완료라고 표시하지 않는다. concern/combo/site/technique/unit/package/condition/literature 전수이관은 후속이며 기존 서비스·Gold 탐색 변경은 발주하지 않는다.
