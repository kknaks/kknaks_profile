# v2 scope·rule 보완 결과

R-H1/R-M1의 지정 메커니즘 보완을 완료했다. 정상 pilot 값과 ID를 유지하면서 기존 v2 계약·validator·schema를 강화했다. 이 결과는 pilot 범위의 검증이며 본설계 정본 반영, 전체 이관, 임상 승인이나 단계3 전체 수용 판정은 아니다.

## 변경과 근거

| 항목 | 구현·원문 근거 | 검증 |
|---|---|---|
| R-H1 축 상태 | 모든 축의 included/excluded 교집합, 양쪽 중복, knowledge/값/근거 조합을 검사한다. 실제 317축은 explicit166·unknown149·not_applicable2이며 not_declared 실물은 없다. source-specific knowledge도 함께 고정했다. | 언어 M2 포함·제외 동시 표기, explicit→unknown, combo container 제외가 재해시 후 관련 검사로 거부된다. |
| R-H1 source parent | self/cycle 검사와 원문 context 검사를 분리했다. 정당한 parent는 실제 comparison member 두 건에서 같은 comparison subtitle context로 연결되는 경우만 허용한다. source snapshot/file/pointer와 claim 계통 및 축 raw_refs를 대조한다. 나머지 scope parent는 null이다. | 언어·combo의 무관 parent, 다른 comparison parent, parent 삭제·중첩, self/cycle 모두 거부된다. 실제 두 parent는 정상본·이동본 검사에서 유지된다. |
| R-H1 언어·combo | 언어 categories/M2 계통의 family included/excluded/knowledge/raw_refs/parent를 exact 검사한다. combo는 complaint의 cc/cc_group 및 raw_refs, statement_site 미정, parent를 원문에서 독립 도출한다. | 추가10 및 확장38의 관련 scope 변조를 거부한다. 팔자/목 conflicts와 statement evidence를 유지한다. |
| R-M1 policy | D9-3 id, 원문 step9-decisions.json version 문자열, step9-apply.py SHA256, 실제 decision_ref를 함께 exact 검사한다. | policy version/id/hash 변조를 거부한다. 기존 decision authority/source·conservative output 검사도 유지된다. |
| R-M1 attachment | schema에서 id=pilot-preserve-source/version=1을 고정했다. ref_contract.py와 ref-contract.json에 구현 build.py·계약 contract.md의 고정 fingerprint를 선언하고 실제 파일과 대조한다. builder 산출값을 기대값으로 쓰지 않는다. source subject=target·같은 scope·unknown·빈 witness·실제 duration resolution 관계를 검사한다. | 임의 rule id/version, 무관 resolution·target 연결을 거부한다. 실제 attachment8개 payload와 ID는 불변이다. |

container included는 일반 집합과 달리 [cc, cc_group] 두 원문 역할 슬롯이다. 원문 3행은 두 문자열이 같으므로 해당 complaint evidence와 두 슬롯이 exact 일치할 때만 중복을 보존한다. 임의 반복과 excluded 중복은 금지한다. 이 예외 없이 일괄 중복 제거하거나 정상 원문을 변경하지 않았다.

unknown의 후보 값을 일괄 삭제하지 않는다. generic 상태 검사는 원문 근거가 있는 unknown 후보 값을 허용하며, 실제 원문이 확정한 축을 unknown으로 내리는 것은 source-specific 검사에서 거부한다. not_declared/not_applicable의 값은 비어 있어야 하며 근거가 필요하다. 실제 not_declared positive나 새로운 excluded/witness positive는 만들지 않았다.

## 재현·검사 분모

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-design-pilot-v2/scope_rule_probes.py
```

원래 probe 파일은 수정하지 않았다. 신규 runner는 결과만 scope-rule- 접두어 JSON으로 돌리고, source_review.py의 저장문만 메모리에서 redirect한다. 리뷰 additional.py도 원문 코드를 메모리에서 실행하고 저장만 v2 결과 JSON으로 돌린다. identity 시험의 임시 원문 복제는 기존 v2 scratch 아래에서 만들고 삭제했다. 새 v3 복제는 없다.

| 검증 | 결과 | 근거 |
|---|---:|---|
| 정상 source/schema/refs/meaning/projection | 21,337 PASS / 0 FAIL, schema 일치 | scope-rule-baseline.json |
| 기존 31 + 리뷰24 + 재해시20 | 75/75 거부 | scope-rule-existing-mutations.json, scope-rule-additional-probes.json, scope-rule-rehashed-semantic-probes.json |
| 리뷰 독립 추가10 | 10/10 거부, 정상1 통과, 구현 예외0, normalized ID 실패0 | scope-rule-independent-additional.json |
| 다른 축·중복·knowledge·parent·rule 확장 | 38/38 거부, normalized ID 실패0 | scope-rule-extra-probes.json |
| 기존 의미 변조를 다시 재해시·projection 재생성 | 54/54 거부 + 정상1 통과 | scope-rule-historical-rehashed.json |
| 원문 독립 대조 | 996 PASS / 0 FAIL | scope-rule-independent-source.json |
| 실제 builder 이동·판 시험 | 24 PASS / 0 FAIL | scope-rule-identity-tests.json |
| 정상 positive | 6 PASS / 0 FAIL | scope-rule-positive-controls.json |

새 10+38과 기존 의미 변조74개(기존54+이미 재해시하는20)는 normalized ID 재계산 및 projection 재생성 후 검사했다. 나머지 1개 `claim_id_arbitrarily_changed_with_refs`는 순수 ID 위조다. revise가 이를 canonical ID로 복구하므로 payload 의미 변조와 같은 부정 시험으로 세지 않고 원래 normalized_revision_id 검사에서 거부됨을 유지했다. 위조를 복구한 뒤에도 거부돼야 한다고 주장하지 않는다. graph에 직접 임상 edge를 더하는 기존 시험은 graph delta를 유지한 채 검사했다.

기존31+리뷰24는 결과 artifact 복구를 위해 runner 끝에서 한 번 더 실행한다. 따라서 이름이 다른 변조는 123개(75+10+38), 실제 부정 실행은 232회(75+10+38+54+55 반복)다. 중복 메커니즘을 독립 결함 수로 세지 않는다. 21,337·996·24·6도 기계검사 수이며 **새 임상 의미 검토·승인 건수는 0**이다. 원문 scope 형식과 계통을 코드·계약에 대조한 작업을 임상 필드 전수 검토로 바꾸어 세지 않는다.

추가6 허용 반례의 실제 거부 근거는 scope_axis_disjoint, scope_axis_source_knowledge, language_scope_family, combo_scope_source_axes, scope_parent_source_context, resolution_policy_exact_source_version, strict_schema다. self/cycle은 scope_parent_acyclic에서 거부된다. none 축의 값 변조 등 일부 확장 사례는 구조 schema에서 먼저 거부되며 모든 사례가 같은 공통 check에 도달했다고 주장하지 않는다.

정상 source-confirmed identity8(CC4·timing2·duration2), source fact lookup167, LOSS16잎(소실10 포함), combos146, note7, 조건 분기·후보 selected0·원문 conflict·언어 미정·attachment unknown을 동시에 유지했다. pilot/projection이 byte 단위로 불변이며, 독립 원문996과 기존 검증도 이를 재확인했다.

## diff·hash·보호 경계

시작 전 hash·bytes 및 코드/계약 텍스트는 scope-rule-start.json, 정확한 unified patch는 scope-rule-patch.json, 최종 hash와 보호 검사는 scope-rule-integrity.json에 있다. 변경된 기존 파일은 아래 6개뿐이다. 신규 파일은 scope_rule_probes.py, scope-rule- 결과 JSON들과 이 보고서다.

| 기존 파일 | 시작 SHA256 | 종료 SHA256 |
|---|---|---|
| contract.md | `62b2248547bcc3ecfee023b62fadc28b59705cdbd8a2d9d4e8fcccdd5cb80a40` | `a191739b17fe4d6b5809aa6d1d565f60c14d1436d2828bb8228d89dae4af47a4` |
| invariants.py | `b1a18db030eb20e3361b2e955ce574649162b2fd21bbe628d311642568ef595d` | `ce5188297d0a431a91e167e8ce49e00949b50cc5f9788f3f9f048c83a9466232` |
| ref-contract.json | `18a97fc0e5aff54b4c250a0597376ff83c328990b7d2f5f02ac048192f6e6721` | `8afcda20841f3e85c1ab38a2c2f933ebca117da510ca8d3e2997a1d28bc86161` |
| ref_contract.py | `3b6a753edfdac9f7c92469afe48a198b18295f0bbb4d9c23fc8c925f339f4212` | `597fd6ccda4b875e28990c491f6226a7f1b3b3e3410e283b129a928f1343b0f3` |
| schema.json | `763f2730e49235ee836574bd2e9292529f0524ff801541f2e6e4e81dc713c62d` | `a4c762c10372c7dedbaf92f9c7e67aea198dbba35613d263c90dc45f6d250654` |
| schema.py | `a8a0cb51e466773d2c855959ba6ca1f41607d0696548847efee961957d915249` | `121ddca33bf3372c6662e071a3f2dcc9064ca02147705573ea95b883f702cfd9` |

build.py·validate.py·identity.py·run.py와 기존 정상 산출물은 수정하지 않았다. schema.json만 변경한 schema.py 선언에서 다시 출력했다. run.py 실행이나 기존 정상 pilot/projection 재생성은 필요하지 않았다. 신규 probe 코드 SHA256는 `05805decb9b03dd96aa55076bf0d2c428c8045eabe67660cc7f0d0fe01ce9f14`다.

불변 정상 데이터·보호 baseline hash:

- pilot.json: `cc897e4cca29f0e50bab2605ee3ef06a7ab5fe7942544a2ca00b4b496f45c89f`
- graph-projection.json: `9fc347462b83bf675d903de2355e76370ba2d3d190f82f2146d68e756a257a2f`
- protected-start.json: `d9e5f014aeb70f183811610f27eb6ec96d3ed38e24b0cf02a453362a8a03de79`
- protected-end.json: `d9e5f014aeb70f183811610f27eb6ec96d3ed38e24b0cf02a453362a8a03de79`

시작 시 기록한 295파일 중 289파일은 불변이며 6개 변경은 모두 허용된 v2 파일이다. 기존 v2 protected-start.json의 immutable208개는 과거 baseline과도 전부 일치한다. 원문·실버·design/HTML·v1/v1리뷰/v2리뷰·스펙/WP·앱/Hub/환경 파일을 수정하지 않았고 보호 baseline을 소급 갱신하지 않았다.

mutable WORK.md의 과거 baseline hash는 `9bc30bce3ea6c0f1184e135497f3b4118449cdcc138c624ff25f6971525ba68f`, 현재 hash는 `0ed521b6b8d901e60c3b44e73ef8b1dd68c8700b544d931ffc13449e600f8ad2`다. 이 차이는 착수 시 이미 존재했고 이번 착수/종료 사이에는 바뀌지 않았다. 보호입력 변화로 합산하지 않는다. 네트워크·모델·패키지 설치·하위 worker·commit/push/PR·DB·서버 실행은 없었다.

## 남은 coverage

이번 폐쇄는 R-H1/R-M1 지정 scope·rule 메커니즘에 한정한다. generic unknown 후보 보존 규약이 전체 source의 후보 positive를 입증하지는 않는다. 원문 근거 있는 새 parent·excluded·witness, 여러 source의 합성 scope, 새 임상 승인·원천정정은 지원하거나 발명하지 않았다. comparison 두 parent 외의 정당한 parent 모델은 후속 계약 범위다.

25타입·247필드 전수 이관기, 안전580행·semantic-pending1277칸·duration196슬롯/343 alternatives 전수 검수, 임상 최신성, usable Gold/API/앱 탐색은 범위 밖이다. 본설계 정본 반영이나 데이터 이관 완료를 주장하지 않는다.
