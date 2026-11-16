# 첫 이관 계약 CR-H1/H2/H3/M1 보완

2026-11-03 · Task `task_2914431d1469` · Dispatch `ctx_2dc2d6dd7d82`

**이번 계약 보완 검증 PASS.** DATA-001/2, field-contract/2, WORK-013의 실행 입력을 새 manifest v2로 맞췄다. 이는 구현 전 계약 검증이며 candidate 생성·임상 승인·P1~P5 통과가 아니다. 기존 문서검수 FAIL 보고와 input-manifest/results는 그대로 보존했다.

| finding | 수정 전 → 수정 후 | 폐쇄 근거 |
|---|---|---|
| CR-H1 | 변경되는 `_RESUME.md` 직접 입력 → 승인된 현재 bytes의 frozen 파일 입력 | [이전 manifest](input-manifest.previous.json), [reconciliation](reconciliation.json), [대조 결과](results/reconciliation.json): 현재 source의 로그 인용51곳과 frozen line 문맥, 27계열 이름/근거를 실제 source와 대조했다. M1~M17은 raw 문헌 이름, N1은 step2-research 이름, N2~N10은 step2-step5-decisions의 name/name_basis exact 일치다. M1의 실제 제품 ATC도 별도 대조했다. |
| CR-H2 | design/coverage가 generated 데이터 source snapshot에 혼재 → audit collection 분리 | [membership](collections.json), [ID 메모리 시험](results/identity-proof.json): audit 전체 hash만 바꾸면 audit snapshot만 변하고, unchanged 제품 occurrence와 source_refs를 유지한 normalized claim ID는 같다. 실제 source hash 변경은 occurrence/claim ID를 바꾼다. |
| CR-H3 | 모든 원문 claim 부착 요구 → 전체 claim 보존과 eligible attachment 분모 분리 | [안전 원문 대조](results/safety.json): 580행/1394field/4170잎 exact 보존 oracle, 후보19+보관37행의132field 정상 미부착. mapping/source-row-index에 상태·사유·source/claim/mapping refs 필수, 원문 candidate의 nullable target_ref/raw_refs/reason 및 selected_refs=[] 규칙 명시. |
| CR-M1 | 파일별 heterogeneous 판을 collection scalar로 해석 → collection 역할/판과 파일 메타 분리 | [입력 검증](results/manifest.json): collection.source_kind는 역할, collection.source_version=null+reason. 모든 파일의 meta.source_kind 및 /version 원형 타입·missing/null 구분을 검증했고 정수/문자열/missing/null positive를 별도 확인했다. |

## 입력판과 reconciliation 한계

브리프가 코디의 현재판 진행기록 snapshot 입력채택을 승인했다. 원문·정본·진행기록은 수정하지 않았으며 frozen 파일은 앞으로 변경하지 않는 입력이다. 이전판 원본 bytes는 확보하지 못했으므로 이전판→현재판 byte diff나 과거 승인 원문의 독립 인증을 주장하지 않는다. 이전 expected hash와 현재 hash를 명시하고, 현재값·원문·결정의 대조로 이번 입력채택을 한정했다. 로그만으로 이름/임상사실을 변경하거나 승인하지 않는다.

- 이전 expected: `da701b275e2fd2e784d425fdc2d872e9e4f3f81ee600108ef9a6b7fa6e2428ba` / 154536 bytes.
- 실제 채택 frozen: `c3394f487966cfc061439e5902541555fbc82460fd774e4feb92d6f9125fb974` / 155396 bytes.

새69파일 전체는 raw21 21/generated18/research11/decision13/audit6이다. 이전 membership의69파일 중 68파일은 bytes/hash를 그대로 유지했고, 로그 하나만 frozen locator/logical key로 대체했다. audit6은 design/coverage 및 apply.py4개이며 HTML은 현재 입력 밖이다. rule code의 실제 fingerprint는 별도 rule payload/revision에서 검증하므로 규칙변경을 audit-only로 숨기지 않는다. 감사 basis는 audit sidecar에 보존하고 데이터 source_refs는 normalized ID payload에서 제거하지 않는다. 각 collection은 동일한 독립 snapshot 공식을 쓰며 전체 manifest hash와 고정 증거 hash는 별도로 보존한다.

snapshot = `snap:` + SHA256(canonical(`[domain,collection,sorted([[logical_file_key,sha256],...])]`)); occurrence = `src:` + SHA256(canonical(`[snapshot_id,logical_file_key,pointer]`)); normalized = prefix + SHA256(canonical(`[record_schema_version,mapping_rule_revision,payload_without_id]`)). canonical은 UTF-8/ensure_ascii=false/sort_keys=true/compact separators/NaN 금지다. 감사 sidecar 외 의미 payload는 source_refs를 포함한다.

## 검증과 다음 worker

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-data-contract-batch1/contract-fix/verify.py
```

표준라이브러리만 사용하는 [독립 검증기](verify.py)는 기존 builder/validator/이전 verifier를 import·실행하지 않고 원문을 직접 읽어 이 폴더 results에만 쓴다. [verification.json](results/verification.json)에 모든 결과와 보호대상 대조를 기록한다. 입력69개 실제 hash/bytes와 fixed membership, raw21 전체집합, product395/active354/inactive41/family27/product_family354의 ID집합, 안전 원문 field/leaf, 4576 current locator, 84 proposed_contract·247 baseline 상태 보존, 문서·machine transform 일치를 확인했다. 범위밖163필드의 신규 구현 실적은0이다. field-contract의 제안 당시 타입/빈값은 보존하고 audit enum/파일 meta/미부착 예외는 새 transform과 DATA-001에 명시했다.

보호대상1592개 고유파일을 시작/끝 hash+bytes로 대조했다. 허용된 DATA-001/WORK-013/field-contract의3개 변경 외에는0이며, 기존 원문/원장/decisions/apply/실버/HTML/design/pilot/review/semantic은 변경하지 않았다. [시작](results/protected-start.json)·[종료](results/protected-end.json)가 근거다. 이번 신규 산출물은 contract-fix 아래에만 있다.

다음 worker는 WORK-013 CLI의 새 `--inputs .../contract-fix/input-manifest.v2.json`을 사용할 수 있고 현재 P0 hash/membership gate는 통과한다. 이관기·schema·candidate는 이번에 만들지 않았으므로 P0의 실제 이관기 전체 실행과 P1~P5는 별도 작업이다. 단일 owner 검증이 필요한 나머지524행/1262field는 자동 attachment eligible이 아니며, 전체1394 = eligible + not_created의 서로소 분모와 원문 zero-loss를 구현 후 검사해야 한다. 임상 application unknown, 신규 임상 승인0, subfamily needs_design 및 후속 타입의 범위는 유지했다.

네트워크/모델/설치/DB/서버/앱·Hub/하위worker/commit/push/PR/정본전환은 실행하지 않았다. 기존 보고의 판정을 새 PASS로 소급 변경하지 않았다.

## 고정 hash

- `input-manifest.previous.json`: `369700df5eca039f2b4e2add159c8ee258ea409d660e0fb9e76714a4c38f27df`
- `input-manifest.v2.json`: `ff8a74cdea25353c219df4d5dd5f145a6fe3573c9d4d1adef023ac4c7756ea04`
- `collections.json`: `99e2ab99b30c5d120bd6d36cee05ed9592b19e207bcd4fe28955e3d0c3ae135f`
- `reconciliation.json`: `07785836d9c3d3bb56160d043aad1bcbb7fdc665509b157fd514daf501995d36`
- `evidence-manifest.json`: `f2351a4cfaa9a45675ec2d11f354217c1055652c101336bbda751ee3d8f9b77e`
- `verify.py`: `01c9e003c7222239bd098df57704472353b1b1ee286d7b4820cdd5e60e3a696e`
