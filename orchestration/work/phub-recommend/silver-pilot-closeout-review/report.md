# scope·rule pilot 폐쇄 독립 검수 및 단계4 coverage 인계

Task task_bfc71e4a4d06 · Dispatch ctx_1143410c64fa · 2026-11-03

**R-H1 PASS / R-M1 PASS — 지정 결함의 pilot 계약 폐쇄를 확인했다.** 기존 허용6개가 ID 재계산 후 관련 진단으로 모두 거부됐고 정상 원문·후보·identity는 유지됐다. ID·refs·현재 scope·rule판 계약은 후속 설계에 부분 채택할 수 있다. 이 판정은 25타입·247필드의 의미 승인, 전수실버 이관 완료, 단계3의 모든 미래 표현 지원, 임상·Gold·서비스 활성화 승인이 아니다.

## 판단 근거

### R-H1: 축 집합·knowledge·원문 parent

[invariants.py](../silver-design-pilot-v2/invariants.py)의 scope_axis_disjoint(:60), scope_axis_unique(:66), scope_axis_knowledge_values(:67)는 포함/제외 교집합·양쪽 중복과 값/상태/근거 조합을 검사한다. explicit은 값과 근거, not_declared/not_applicable은 빈 값과 근거를 요구한다. raw_refs 또는 해당 scope를 사용하는 claim/mapping의 원문 근거가 필요하다. 현재 source-specific knowledge를 추가 검사하여 실제 explicit 축을 unknown으로 낮추지 못한다. 실물 317축은 explicit166/unknown149/not_applicable2이며 not_declared 실물 positive는 없다.

container의 중복 예외는 complaint 원문의 [cc, cc_group] 두 역할 슬롯과 raw_refs가 정확히 일치할 때만 허용한다. 실제 중복3개를 그대로 유지하고, 임의 반복·excluded 중복·다른 complaint 근거는 거부한다. 일반 축을 모두 비우거나 원문 역할을 deduplicate하여 PASS시킨 결과가 아니다.

scope_parent_acyclic(:35)는 self/cycle을 검사한다. scope_parent_source_context(:73~75)와 comparison_axis_source_state(:74)는 같은 snapshot·logical file·comparison pointer의 subtitle context만 parent로 인정하고 멤버의 원문 raw_refs 및 context의 빈 parent도 대조한다. 실제 comparison parent2개는 보존됐다. 언어의 family 축 전체(:102), combo의 container/statement_site 축 전체(:134)는 원문에서 독립 도출한 값과 비교한다. source parent와 normalized parent는 혼용하지 않는다.

unknown 후보 삭제는 요구하지 않는다. 실제 ambiguous mapping 두 개의 후보는 각각8개, 선택은0개이며, generic inspection만 수행한 합성 site control도 근거 있는 unknown의 후보값을 수용했다. 이 합성 control은 임상 positive나 실제 site 이관 실적으로 세지 않는다. comparison 외의 새 정당한 parent, 다원천 scope 합성, 실제 excluded/witness positive는 후속 표현 계약이며 이번에 발명하지 않았다.

### R-M1: 선언과 실제 source·구현판

resolution_policy_exact_source_version(:163)은 D9-3 id, 실제 step9-decisions.json의 version=1을 문자열로 바꾼 값, 실제 step9-apply.py hash, 실제 decision_ref를 함께 대조한다. 원문 authority/날짜/이유/target와 기존 conservative output 검사도 유지된다.

attachment.rule은 schema에서 pilot-preserve-source/version1을 고정하고, ref_contract.py와 ref-contract.json의 고정 선언을 비교한다. 선언된 build.py·contract.md fingerprint는 실제 파일 bytes에 대조했다. build.py hash는 `6ac8f07c83c4a069f031c7f89788626e01c621cbad13d854e3c62599eb924028`, contract.md hash는 `a191739b17fe4d6b5809aa6d1d565f60c14d1436d2828bb8228d89dae4af47a4`다. 기대 rule을 builder 산출물에서 추출하지 않았다. subject=target·같은 scope·unknown·빈 witness·실제 duration resolution의 연결 정합도 검사한다. 독립 반례의 다른 reachable scope 및 subject 없는 claim도 거부됐다. fingerprint는 감사 선언이며 정상 attachment payload에 새 필드를 쓰지 않는다.

### 과거 허용6 직접 재현

기존 review/additional.py의 코드를 메모리 실행하고 저장만 새 폴더로 돌렸다. 모든 변조는 identity.revise 및 projection 재생성 이후 검사했다. 구현 예외0이며 다음6개는 normalized ID 실패0으로 의미/규칙 진단에서 거부됐다.

| 재현 | 관련 진단 | 결과 |
|---|---|---|
| language_scope_excludes_its_included_M2 | scope_axis_disjoint, language_scope_family | 거부 / ID 실패 0 |
| language_scope_explicit_to_unknown_axis | scope_axis_source_knowledge, language_scope_family | 거부 / ID 실패 0 |
| language_scope_adds_unrelated_container | scope_parent_source_context, language_scope_family | 거부 / ID 실패 0 |
| combo_scope_excludes_its_source_container | scope_axis_disjoint, combo_scope_source_axes | 거부 / ID 실패 0 |
| resolution_policy_version_forged | resolution_policy_exact_source_version | 거부 / ID 실패 0 |
| attachment_rule_id_version_forged | strict_schema | 거부 / ID 실패 0 |

### 이번 독립 반례와 정상 보존

[독립 결과](results/independent.json)에는 comparison context의 excluded 중복, 멤버 raw evidence 변경, context raw evidence 변경, 역할중복 container의 다른 complaint evidence, attachment의 다른 실물 scope, subject 없는 claim 연결, 빈 policy.version의 **7개 반례**를 남겼다. 전부 ID 재계산 후 거부됐고 ID 실패는0이다. 처음4개는 scope_axis_unique/comparison_axis_source_state/scope_parent_source_context/combo_scope_source_axes 등으로, 뒤3개는 attachment_rule_source_application/attachment_rule_resolution/resolution_policy_exact_source_version 등으로 거부된다. 새로운 임상 필드를 임의로 추가해 검사 범위를 늘리지 않았다.

정상본의 exact identity8(CC4·timing2·duration2), source fact167, comparison parent2, 원문 역할중복3, attachment8이 유지됐다. LOSS3행·6field·16잎(소실10 포함), combos146(arity1=21/2=119/3=6), singleton pair0, note7, 튼살 parent=P9-4, same_day와 first 조건 분기, 후보 선택0, M4 override·M2 미정, K8 비환자조건, 팔자/목 conflict, 언어5 variant와 한국어 지연성 한정, duration 대안과 clinical_consensus=false를 보존한다. 정상 pilot/projection을 재생성하거나 바꾸지 않았다.

## 실행 증거와 분모

| 재실행 | 결과 | artifact |
|---|---:|---|
| 정상 schema/source/refs/meaning/projection | 21,337 PASS / 0 FAIL, schema 선언 일치 | results/scope-rule-baseline.json |
| 기존31 + 과거리뷰24 + 의미재해시20 | 75/75 거부 | scope-rule-existing-mutations / additional-probes / rehashed-semantic-probes |
| 과거 독립 추가10 | 10/10 거부 + 정상1 통과, 구현 예외0 | results/scope-rule-independent-additional.json |
| scope·rule 확장38 | 38/38 거부, ID 실패0 | results/scope-rule-extra-probes.json |
| 과거 의미 변조를 다시 재해시 | 54/54 거부 + 정상1 통과 | results/scope-rule-historical-rehashed.json |
| builder·validator를 import하지 않는 원문 대조 | 996 PASS / 0 FAIL | results/scope-rule-independent-source.json |
| 실제 builder 이동·schema/rule판·design판 시험 | 24 PASS / 0 FAIL | results/scope-rule-identity-tests.json |
| 기존 정상 positive | 6 PASS / 0 FAIL | results/scope-rule-positive-controls.json |
| 이번 독립 추가 | 부정7 거부 + 정상 재해시1·generic unknown 후보1 통과 | results/independent.json |

검사 수는 독립 임상 결함 수나 임상 검토 건수가 아니다. 기존75·추가10·확장38은 이름이 다른123개이고, runner는 과거54 재해시와 마지막55 반복까지 부정232회를 실행한다. 같은 메커니즘을 반복 합산하여 새로운 결함 종류로 세지 않는다. 순수 ID 위조1개는 원본 normalized_revision_id 검사에서만 거부를 요구한다. revise가 그 위조를 복구한 뒤의 거부를 주장하지 않는다. 새 임상 의미 승인0이다.

실행 명령:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-pilot-closeout-review/probes/rerun.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-pilot-closeout-review/probes/independent.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-pilot-closeout-review/probes/coverage.py
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-pilot-closeout-review/probes/verify.py
```

rerun.py는 원래 scope_rule_probes.py를 실제 실행하며 결과 sink와 identity 임시복제 위치만 바꾼다. 변경한 실행문/원본 hash는 runner-adaptation.json에 있다. 기존 source_review의 저장문만 redirect하는 원래 방식도 유지한다. 임시 원문은 이번 results 아래에서 생성·삭제했다. 각 *.execution.json은 실제 원본 코드 hash와 stdout을 담는다.

## 25논리타입·247필드 coverage

[coverage.json](coverage.json)은 design.json types의25개·247개 필드를 빠짐없이 한 번씩 담았다. Gold node13종은 별도 분모다. 모든 필드에 proposed type.field, 현행 실버/원문 또는 provenance context의 검증된 file/pointer, pilot typed path 또는 null, 상태, 원래 제안 계약·근거 ID·제약을 기록했다. 자동 fieldname 일치를 이관 근거로 쓰지 않았다. concrete locator 1,385개를 실제 JSON에서 재확인했다.

| 상태 | 필드 |
|---|---:|
| pilot검증 | 78 |
| 원문raw보존만 | 33 |
| 계약만 | 71 |
| 미구현 | 62 |
| 의미미확정 | 3 |
| 합계 | 247 |

pilot검증은 해당 subset의 typed 필드 실물·계약 검증이다. 해당 설계 필드의 모든 임상 의미가 승인됐다는 뜻이 아니다. typed path90개 중12개는 null/빈 배열 또는 population0의 계약만이다. raw보존33개는 source_record.raw_value의 보존 실물이며 entity typed 이관 완료가 아니다. source locator가 확인된 현행 칸이어도 pilot 대응이 없으면 미구현62개로 남겼다.

원천 경로 미확인87개는 새 revision/status/decision_refs 계약이나 derived record처럼 현행 동등 칸이 없는 항목도 포함한다. 이를 원문87개 소실이나 원천87개 오류로 해석하지 않는다. 현행 실버 locator를 확인했더라도 원장까지 독립 추적하지 않은 경우 current_silver로 표시하며 원장 확인으로 포장하지 않았다. 타입당 광범위 source_refs를 필드별 변환 완료로 승격하지 않는다. schema의 site는 허용되지만 실물0이고, 전체 entity는5종27개(product4/family4/unit11/concern7/evidence_statement1)다. 그 행에는 id/type/native_id/source_refs만 있다.

subfamily stable key·axis와 purpose stable id3개는 의미/ID 결정 필요로 별도 표시했다. verified_at은 실제 확인시각 근거가 없다는 계약만이며 timestamp 의미 자체가 미정인 것으로 세지 않았다. 팔자/목 범위, 비교후보 선택·부위, M4→M2 확대 근거, 언어 동치, 보수정책 승인, 정본 권한 등 원천 질문은 coverage의 source_questions_separate_from_implementation에 보존했다. 기존 질문을 구현누락으로 바꾸거나 임의 해소하지 않았다.

### 단계4에 넘길 조건과 우선 묶음

부분 채택 가능한 core는 collection/domain/logical key와 물리 locator 분리, 정렬 manifest snapshot, source occurrence/native entity/normalized revision 수명 분리, typed ref·도달성 진단, explicit·unknown·비적용과 parent 출처, resolution/attachment rule판의 실제 근거 대조다. 이 core를 전체 entity의 완료된 스키마로 복사해서는 안 된다.

먼저 설계판 호환성을 정해야 한다. pilot scope는10축과 explicit/unknown 등의 어휘를 쓰며 본설계의 subfamily/technique/ingredient/purpose/patient/language/route/time 및 declared/unresolved와 그대로 같지 않다. source_record의 상대 파일 키는 logical_file_key이고 file은 물리 locator다. claim.subject는 entity/null만, source_refs는 실물검사상1개만, normalized_value는 null만 허용한다. 여러 source·실제 normalization·실제 witness·새 parent·continuity와 대체 schema판은 각 묶음을 구현할 때 근거 positive와 부정회귀를 추가해야 한다.

다음 구현은 각 묶음에서 **source record 원문보존 + 이미 확인된 오류 정정 + 실제 typed entity 필드**를 함께 구현하고, 그 묶음의 입력/출력 분모와 별도 원장 대조를 통과시키도록 권고한다.

1. 제품·계열·안전 충돌 묶음: native ID를 유지하면서 display/search label, identity_kind, 허가/규격/업체역할·계열 mapping·line/continuity를 typed화한다. 확인된 common 덮어쓰기는 원래6field/16잎 및 두 원천 claim을 남기는 방식으로 정정하고 승인·최신성은 새로 만들어 넣지 않는다.
2. 고민·CC·조합 묶음: 같은 이름4occurrence와 정확 correspondence·튼살 parent 정정 이력을 유지하고 concern parent/related/site/source_kind를 typed화한다. combos146의 전체 원문·note7을 함께 보존하며 combo/component 전용 계약·순서/역할/phase와 후보집합을 구현한다. 팔자/목과 comparison은 원천 확인 전 미정이다.
3. 부위·기법·단위시술·패키지 묶음: site/technique의 전체 레지스트리, subfamily 축·key 결정, unit key/site_basis·attrs·product/purpose/candidate mapping, package contains/slots를 대응한다. 현재 site0이나 inline relation.members를 해당 entity/component 이관 실적으로 세지 않는다.
4. 안전·조건·문헌·설명 전수 묶음: 안전580행, semantic-pending1277칸, duration196슬롯/343 alternatives에 실제 필드별 normalization·빈값 의미·scope·policy와 별도 source oracle을 붙인다. language variant·출처 서지·실제 verification 시각 및 기존 보수 resolution을 원문 claim과 구별한다.

이 순서는 구현 발주 제안이며 정본 확정·원천 수정 명령이 아니다. 42사례·146combo 밖의 의미 검증, 전수 임상/허가/문헌 최신성, usable Gold/API/앱 탐색·최종답은 미완료다. 단계4 수용 시에는 이 coverage를 묶음별 실제 구현 상태로 갱신하고, 원문 미정은 구현 진척과 분리한 채 유지해야 한다.

## 기준판·보호 경계

검수 시작/종료 [start.json](results/start.json)·[end.json](results/end.json)의286파일 hash/bytes를 비교해 변경0을 확인했다. baseline manifest와 v1/v2·기존review·원문/실버·design/HTML·관련 스펙/WP/앱·Hub/환경 보호입력을 포함한다. 기존 manifest를 소급 갱신하지 않았다. WORK의 현재판은 시작과 종료에 동일하다. 네트워크·모델·설치·하위worker·commit/push/PR·DB·서버 실행은 없었다.

pilot.json hash는 `cc897e4cca29f0e50bab2605ee3ef06a7ab5fe7942544a2ca00b4b496f45c89f`, projection은 `9fc347462b83bf675d903de2355e76370ba2d3d190f82f2146d68e756a257a2f`다. 검수기준 코드hash 전부는 start.json.code_hashes, 이번 probe hash는 verification.json.review_code_hashes, 시작/종료 보호행 canonical hash는 verification.json의 start/end_protected_rows_sha256에 있다. 검수 중 수정은 이 폴더 report.md/probes/results/coverage.json에 한정했다.
