# DATA-001 / WORK-013 첫 이관 계약 독립 검수

2026-11-03 · Task `task_f19308ab3f31` · Dispatch `ctx_6351d574f02c`

**계약 폐쇄 판정: FAIL — High 3건, Medium 1건.** 실제 분모·원문 oracle·필드 locator·기존 coverage는 독립 대조를 통과했다. 그러나 현 계약 그대로 구현하면 입력 고정에서 중단되고, design-only ID 불변 반례를 만족할 수 없으며, owner가 없는 안전 claim의 attachment 처리에 구현자의 해석이 필요하다. 이 보고는 구현 전 계약 검수이며 candidate 구현 실패·임상 부정 판정이 아니다. 검수 작업 자체는 완료했다.

## 1. Findings

### CR-H1 — 고정 입력의 `_RESUME.md`가 이미 다른 판이며 reconciliation 실행 계약이 없다

**근거:** [input-manifest](../silver-data-contract-batch1/results/input-manifest.json)의 첫 행은 `_RESUME.md`를 154,536 bytes / `da701b275e2fd2e784d425fdc2d872e9e4f3f81ee600108ef9a6b7fa6e2428ba`로 고정했다. 검수 시 실제 파일은 154,883 bytes / `e58504ab8c322be846115b811a45b2c5287838a3970f0f79d5d354eda6a3bf32`다. 나머지 68파일은 일치했다. 앞 154,536 bytes를 잘라 계산한 hash도 고정 hash와 다르므로 단순 append 이전판이라고 복구할 수 없다.

[WORK-013 §2](../WORK-013.md:35)는 hash 불일치 중단을 요구하고, §1은 구현 worker가 manifest·기존 WORK를 수정하지 못하게 한다. manifest note와 작성 보고는 “명시 reconciliation” 필요성만 말하며, 누가 어떤 고정 원본을 어디에 보관하고 어떤 diff/인용 위치 검토 후 새 판을 승인하는지는 정하지 않았다. 현재판을 조용히 hash 갱신해서 진행하거나 인용만 복사하면 고정된 decision collection의 입력판을 검증한 것이 아니다. 이 현상은 검수 중 보호입력 변조가 아니라 시작 시부터 존재한 불일치다.

**재현:** [results/manifest.json](results/manifest.json)의 `matches=false` 행 또는 `verify.py` 실행. **영향:** P0부터 현 CLI가 정상적으로 실패해야 하며, 현재 계약을 그대로 다음 구현 브리프로 사용할 수 없다.

**최소 수정:** 구현 발주 전에 코디가 역사 원본의 실제 bytes를 별도 immutable artifact로 확보하고 manifest를 그 파일로 고정하거나, 기존 판→현재 판의 diff와 family.name_basis 등 실제 인용 대조를 수행한 reconciliation 기록·승인된 새 manifest판을 제공한다. 이전 hash 증거는 유지한다. 이후 변경되는 운영 로그를 고정 입력으로 직접 읽지 않도록 물리 locator를 분리하고, builder는 승인된 manifest만 받도록 한다. 단순 prefix 절단·자동 재baseline은 금지한다.

### CR-H2 — generated collection의 design 파일 때문에 “design hash만 바뀌면 normalized ID 불변”을 지킬 수 없다

**근거:** [DATA-001 §2](../DATA-001.md:28)는 generated collection 전체 manifest로 snapshot ID를 만들고, 그 snapshot ID를 모든 source occurrence ID에 넣는다. 고정 manifest의 같은 collection에는 `silver-entity-graph-design/design.json`과 `step1-products.json`이 함께 들어 있다. 따라서 design 파일 hash만 바뀌어도 제품의 허가 원문 occurrence ID까지 바뀐다. claim은 source occurrence/source_refs를 payload로 가지며 normalized ID가 그 payload를 hash하므로 이후 claim·mapping·attachment ID에도 전파된다. 이는 DATA-001 §2의 design 감사 hash 비입력 규정 및 [WORK-013 수용기준6](../WORK-013.md:107)의 design-only ID 불변과 모순이다. native product ID 불변만으로 이 normalized ID 요구를 만족시키지 못한다.

**재현:** [results/identity-proof.json](results/identity-proof.json). 실제 파일 수정 없이 manifest의 design hash만 메모리에서 바꿔 본문 공식을 재계산했다. snapshot은 `snap:0b56dd43…`→`snap:6256b5f6…`, 변경하지 않은 `step1-products.json#/items/0/4_license` occurrence는 `src:f87003f3…`→`src:a24caef8…`로 바뀐다. 실제 builder가 아직 없으므로 normalized 출력 실행 결과를 주장하지 않는다. source_ref가 변한다는 공식상의 증명이 후속 payload의 불변 조건과 충돌한다.

**최소 수정:** design/coverage 등 감사 전용 artifact를 데이터 source snapshot의 ID 입력 collection과 분리하고, 고정 membership·collection명·감사 링크와 manifest를 명시한다. 또는 ID 불변 요구를 바꾸는 별도 설계 결정을 먼저 한다. 구현자가 임의로 design 항목을 manifest에서 빼거나 source_ref를 payload hash에서 제외해서는 안 된다. 수정 후 실제 source-data 변경에는 source/normalized ID가 바뀌고 design-only 변경에는 바뀌지 않는 positive/negative를 요구한다.

### CR-H3 — owner 미확정 claim은 허용하지만 “원문 claims 전체 attachment”의 예외가 닫히지 않았다

**근거:** DATA-001 §7.2의 `claim.subject_ref`는 owner 미확정이면 null+mapping을 허용한다. 같은 표의 `attachment.claim_refs`는 “원문 claims 전체 대상”, `attachment.target_ref`는 “검증된 owner ref만”이며, §5 새 규칙도 owner 동일만 허용한다. WORK-013은 product/family 이외에 필요한 unit 제한 registry만 허용하고 package/다른 entity의 전수이관은 후속으로 둔다. subject=null·후보 claim에 attachment를 생략할지, 무엇으로 보존 상태를 표시할지, attachment coverage 분모에서 어떻게 제외할지 정한 예외가 없다.

실제580행에는 단위시술 후보19행 및 원문보관37행이 있고, 이56행에 safety/aftercare field132개가 존재한다. 후보19행은 owner 확정19행이라는 뜻이 아니다. 예를 들어 `step5-units.json#/extracted/27`의 `auto-4-1774737181584`는 `원문 보관(6단계 패키지)`이며 safety/aftercare field3개를 갖고 product/unit owner가 없다. claim 전부 부착을 강제하면 package/product를 발명하거나 후보 unit에 적용한 듯 부착할 수 있고, 부착을 생략하면 현재의 전체대상 문구를 위반했다고 판정될 수 있다.

**재현:** [results/safety.json](results/safety.json)의 `ownerless_or_candidate_rows`; 원문 pointer와 source_text는 script가 독립 대조했다. **최소 수정:** 원문 claim580행 전체 보존과 attachment 생성 대상을 분리한다. 검증된 단일 owner가 있는 claim만 새 규칙으로 부착하고, subject=null/후보/후속 entity claim은 mapping·source-row-index·명시 상태/사유로 보존하며 attachment 미생성 수를 별도 집계한다고 정한다. 대상 미확정의 candidate target 표현·nullable/ref union도 새 schema에서 명시하고, 이 정상 사례를 positive에 추가한다. 임상 owner를 새로 판정할 필요는 없다.

### CR-M1 — collection snapshot 하나에 파일별 source_kind/source_version을 담는 규칙이 모호하다

**근거:** DATA-001 §2는 generated-silver 전체를 하나의 고정 collection으로 정하고 research를 그 domain 안에 둔다. 그러나 §7.2/84필드 계약의 `snapshot.source_kind`는 단일 enum이며 “과거조사=research, 실버=generated”, `snapshot.source_version`은 “해당 artifact 실제 version 문자열”이다. 실제 generated collection35파일에는 generated24/research11이 섞이고, version도 정수1/정수2/`step1-C`/`step2-families v1`/`step5-units v1`/design판 등 서로 다르다. 단일 snapshot의 두 scalar를 어느 artifact 기준으로 채울지 규칙이 없다. 파일별 snapshot을 만들면 collection 전체 manifest 공식과도 달라진다.

**재현:** [results/manifest.json](results/manifest.json)의 `generated_source_kinds`와 실제 각 입력파일 version. **최소 수정:** collection-level 값의 의미와 파일별 메타의 위치를 정한다. 예를 들어 collection snapshot은 generated로 두고 실제 research/generated·version은 `files[]`의 감사 메타로 보존하며, collection source_version은 별도 실제 근거 없으면 null+사유로 정할 수 있다. 이는 검토용 수정 제안이며 채택한 schema가 아니다. 결정 후 필드 transform·확장 목록·positive를 함께 맞춘다.

## 2. 독립 검증한 분모와 원문

표의 PASS는 증거 대조 결과이며 위 계약 폐쇄 FAIL을 대체하지 않는다.

| 검증 대상 | 독립 결과 | 증거 |
|---|---|---|
| 제품 | 395 unique ledger IDs; active354/inactive41 | [census.json](results/census.json) |
| 계열·대응 | family27; product_family354; active 제품 ID집합과 정확 일치; family=null3/pending_director3 | census.json |
| raw21 membership | 실제 파일21개와 manifest의21개 집합 일치 | manifest.json |
| 전체 고정 입력 | raw21 21/generated35/decision13 =69; 68일치/1불일치 | manifest.json |
| 안전 원문 source행 | taxonomy items521 + taxonomy products59 =580 | [safety.json](results/safety.json) |
| 안전 원문 field/잎 | safety.*·aftercare1,394 field / scalar4,170잎; oracle 전체 exact pointer/value/field/predicate/leaf count 일치 | safety.json |
| 현재 source_text | 580행 전부 raw field의 기존 key_normalize+last-write 결과와 일치 | safety.json |
| collision | 3행/6field; before6잎→원문16잎; 소실10잎 확인; 관련 override3개 확인 | safety.json |
| override inventory | units248 + product_links376 =624; 실제 pointer/value 전부 일치 | safety.json |
| 정상 rename | common_adverse_effects2/common_side_effects1/serious_adverse_effects2; 기존 정상 변환 유지 | safety.json |
| technique 제한 registry | family_defaults27의 default/also가 실제 nodes ID에 도달 | census.json |
| baseline locator | origin/current1,186 + typed evidence199; 전부 실파일 pointer 도달, 선언된 value_type 대조 | [identity-proof.json](results/identity-proof.json) |
| 이번 필드 locator | exact_current_locators4,576개 전부 도달, 실제 값 타입 기록 | [fields.json](results/fields.json) |
| 문서 crossref | DATA-001/WORK-013의 Markdown 로컬 링크 존재 | [links.json](results/links.json) |

LOSS02의 원문 ID `auto-2-1774737181584`는 `/extracted/25`의 단위시술이며 `/units/15`의 `U5-016` sources와 override에 실제 도달한다. product로 발급할 근거가 없고 계약의 명시 예외가 맞다. collision M1-1-3·LOSS02·M7-P-1은 원문별 두 field claim을 각각 유지해야 하며 union/dedup로 대체할 수 없다. 현재 last-write 결과의 재현은 오류 복구 완료가 아니다. 정상 onset→peak 규칙도 현 rules에 존재하고 계약이 보존을 요구하지만, 이번 safety field census에는 onset이 없으므로 위 rename 건수에 억지로 합산하지 않았다.

## 3. 84필드 및 권한 검토

[fields.json](results/fields.json)은 product14/family11/공통59의 각 키에 baseline 상태·planned 상태·제안 타입·required/빈값·실제 locator 타입·변환·oracle을 기록한다. 원래 coverage의 제안 계약과 baseline 상태는84개 모두 동일하고, 나머지163키도 baseline과 일치한다. 전체247의78/33/71/62/3 및 미정 `subfamily.key/subfamily.axis/purpose.id`는 보존돼 있다. fieldname/source_refs만으로 typed 완료됐다고 계산한 신규 실적은 없다.

제품 허가는 `4_license` 전체와 licenses/history/reference 및 status/reason/recommendable을 별도 원문 claim으로 보존한다. 규격은 `5_spec` JSON 전체를 보존하고 환산하지 않는다. 업체역할은 실제 dict 배열이며 manufacturer/importer/seller/license_holder/other 역할을 구분하고 부가키·conflict를 claim에 유지하는 계약이다. “근거 없음”을 업체명으로 확정하지 않는 예외도 있다. 문자열·단일허가·일대일 업체로 압축하라는 계약은 발견하지 않았다. inactive395개 전체 보존·기존ID·merged/moved 판정·line의 명시 ID만 연결·허가 불완전/미정·family=null·후보 미선택·clinical confirmed 금지도 적절히 구분돼 있다.

family.subfamilies의 typed=[]는 needs_design+raw_refs와 함께 내고 typed 전수완료에서 제외한다. technique_defaults는 제한 registry 참조 보존이며 기법 의미/전수이관 완료로 계산하지 않는다. purpose ID를 발명하지 않는다. 승인 decision의 target을 stable entity로 제한하고 source부터 고정하는 DAG 경계, rule=null+reason, source parent와 scope parent/continuity 분리, schema/rule revision과 native ID의 수명 차이는 명시돼 있다. scope의 새 축/parent/witness를 pilot의 검증 실적으로 포장하지 않으며, 환자 적용·언어 동치·임상 normalization·새 resolution은 미정으로 유지한다.

JSON 외 `.md/.py`는 WORK-013 §2가 실제 hash/bytes·line 인용을 요구하고, JSON source_record로 다루려면 media_type/text-root·decoded text/bytes positive를 새 schema에 선언하도록 한다. transport 확장 자체를 이미 검증된 JSON 전송이라고 주장하지 않는다. 구현 전 계약으로 수용 가능한 경계이며, CR-H1의 역사 로그판 확보가 별도로 필요하다.

## 4. 구현 가능한 범위와 종료 조건

수정 전에도 read-only census·raw claim 원문 보존·제품/계열의 직접 필드 변환 설계는 진행할 수 있다. **현 고정 입력/ID/attachment 계약 그대로 P0~P5 완료 또는 candidate PASS를 요구하는 발주는 불가**하다. CR-H1/H2/H3를 먼저 정하고 CR-M1 메타 규칙까지 schema 입력으로 확정하면 임상값을 결정하지 않고 현재 범위의 candidate를 구현할 수 있다.

WORK-013의 코드/출력/보고 allowed_paths, 표준라이브러리 CLI, 독립 validator의 원문 직접 판독·builder 기대값 import 금지, 정/부 fixture, ID 재계산 후 의미검증, 전수분모·정상 rename·collision/override·재현성·이동 시험 요구는 구현 검증 범위를 충분히 지정한다. builder/schema를 지금 만들어서 계약 검수의 증거로 쓰지 않았다. 실제 후보 schema/ref union·cardinality·fingerprint·positive/변조 거부·재현성은 구현 후 P1~P5에서 다시 검증해야 한다. pilot42사례·146combo·note7·언어5·duration은 기존 회귀이며 새 이관 분모가 아니다.

candidate PASS 이후 정본 권한/전환 승인·소비자 호환·backup/manifest·별도 전환·rollback을 나누고, 이번 구현 종료점을 candidate 보고로 둔 것은 명확하다. 원장·실버 source 생성기·DB·Gold·앱·Hub의 변경 권한은 없다. CR-H1 정정을 위한 입력판 관리도 해당 코디의 별도 계약 수정이며 구현자에게 정본 쓰기 권한을 주지 않는다.

## 5. 재현과 보호

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-contract-review/verify.py
```

표준라이브러리만 사용하고 기존 builder/validator/runner를 import하거나 실행하지 않는다. [verify.py](verify.py)는 입력을 읽어 검수폴더 results에만 쓴다. assert PASS는 raw/census/locator 증거의 정확성이며 계약 PASS exit code로 오인하지 않도록 `verification.json.contract_verdict`에 FAIL을 명시했다. field 계약4,576 locator는 중복 검사 수이고 임상 사실 수가 아니다.

[시작 보호 manifest](results/protected-start.json)의3,112파일을 종료 시 SHA256/bytes 재대조하여 변경0을 확인했다([verification.json](results/verification.json)). 기존 보호목록과 현 phub 작업폴더의 파일을 포함하며, 검수 산출물은 제외한다. 시작 hash는 초기 문서 독해 뒤 쓰기 작업 전에 채집했다. 보호대상 파일의 전체 시작값을 저장하고 종료 재계산 결과를 기록했으며, 저장된 `start_manifest_sha256`으로 그 목록 자체도 식별한다. `_RESUME.md`의 입력계약 불일치는 이전 작성판과의 차이이며 이번 시작/종료 변화가 아니다.

수정은 이 `report.md`·읽기전용검증 script·results뿐이다. 원장/기존 문서·설계/pilot/실버/앱/환경 쓰기, DB/서버, 네트워크/모델/설치, 하위worker, commit/push/PR은 실행하지 않았다. 남은 일은 코디가 네 finding의 최소 계약수정을 반영하고 독립 재검수한 뒤 별도 candidate 구현을 발주하는 것이다.
