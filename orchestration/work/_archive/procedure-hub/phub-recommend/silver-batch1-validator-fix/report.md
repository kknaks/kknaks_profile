# P5 BR-H1 / BR-M1 validator 보완 결과

Task `task_b47e5e46c475` · Dispatch `ctx_4d540e974490` · 2026-11-03

**수정 범위 검증 PASS. BR-H1과 BR-M1의 구현·재현 시험을 마쳤으며, P5 독립 재검수는 남아 있다.** 정본 전환이나 임상 적용을 승인하는 보고서는 아니다. 현재 정상 candidate의 payload, manifest, validation을 포함한 모든 파일은 시작·끝 해시가 같다.

## 변경과 finding 폐쇄

**BR-H1:** `migration/validate.py`가 새 `independent_source.py`를 호출한다. helper는 `collections`와 transport의 JSON/hash 함수만 import하며 builder/rules 변환을 oracle로 사용하지 않는다. 고정 84-field contract와 manifest v2는 기존 validator의 hash gate로 유지한다. helper는 manifest membership에서 snapshot/source ID를 독립 계산하고, 실제 step1·step2·step5 및 raw21 taxonomy 원문에서 395 product + 27 family + 580 safety = **1,002 scope**의 기대값을 복원한다. 354 membership은 해당 product의 기대 scope와도 대조한다.

각 scope의 10개 축에 대해 knowledge, value_kind, included, excluded, raw_refs를 객체 전체로 비교한다. statement_qualifiers의 axis/raw/source_ref/state/operator/value를 전체 비교하고 parent, conflicts, application_state와 source_refs도 대조한다. 원천별 scope 전체 목록을 별도로 검사하므로 source_refs를 바꾸거나 다른 정상 scope로 위장해도 누락·중복을 잡는다. 기존 집합 교차·중복·참조 도달성 검사도 유지했다. 미해석 legacy context는 그대로 보존하며 operator/value=null, needs_source, application_state=unknown을 바꾸지 않는다.

**BR-M1:** 395 product 각각의 line_memberships 기대 목록을 원문 row.line.line_row 및 lines.items의 명시 ledger_id/line_row에서 복원한다. 부모가 실제 batch product인지와 자기 자신인지 확인하며 이름이나 허가번호로 추정하지 않는다. 누락·추가·role·parent·decision_ref·reason 전체를 대조한다. 원문에 명시 부모가 없거나 batch에 없는 경우에는 기존 unresolved mapping 전체와 field-state의 source refs, state, raw_state, reason을 함께 대조한다. 새 승인 decision을 만들지 않았다. 나머지 typed 필드에 대한 기존 검사도 모두 유지했다.

## 검증 결과

| 검사 | 결과 | 증거 |
|---|---|---|
| 원 candidate 읽기 전용 evaluate + sidecar | PASS, 실패 0 | [positive-original.json](positive-original.json) |
| 정상 복사본 전체 CLI | exit 0, PASS | [positive-cli.json](positive-cli.json) |
| ID·파생 export·output hash 정합 후 전체 CLI 변조 21건 | 모두 exit 1, 해당 의미 진단 발생, NORMALIZED_ID/OUTPUT_HASH/sidecar/export 불일치 0 | [full-cli-probes.json](full-cli-probes.json) |
| 기존 35 negative + 추가 9 negative / 기존 14 positive | 44 / 14 모두 PASS | [counterexamples.json](positive-copy/counterexamples.json), [로그](regression-stdout.log) |
| 변경 없는 builder 단일 재현본 | 14개 manifest 대상 출력이 원 candidate와 byte 동일, 새 validator와 sidecar PASS | [rebuilt-comparison.json](rebuilt-comparison.json), [rebuilt-validation.json](rebuilt-validation.json) |
| 시작·끝 보호 파일 검사 | 1,665 unique 파일, 허용된 validate.py/test_contract.py만 변경, candidate 변경 0 | [protection-result.json](protection-result.json) |

원 P5 반례 세 건은 각각 `SCOPE_AXIS_SOURCE`(제외 발명), `SCOPE_QUALIFIER_SOURCE`(qualifier 삭제), `PRODUCT_LINE_SOURCE`(line 삭제)로 거부한다. 추가 CLI 시험은 line role·parent·추가·reason 부분 소실·fieldstate 원천 변경, qualifier raw/source/state/operator/value 변경·추가, 축 raw_refs와 scope source_refs 변경, family/membership/unit scope 제외 발명, product/family qualifier 추가를 포함한다. raw 값 음성 대조는 정합화된 export에서도 `CLAIM_RAW`와 `SAFETY_RAW`로 거부됐다.

raw 대조 첫 실행은 파생 raw export를 맞추지 않아 추가 export 진단을 냈다. harness에 raw export/projection 정합화를 보완했고, schema 안의 claim_ref가 문자열이 아닐 때 발생한 순회 오류도 고친 뒤 해당 한 건만 다시 실행했다. 최종 raw 대조에는 ID/hash/sidecar/export 잡음이 없으며 초기 결과는 [raw-control-initial-harness.json](raw-control-initial-harness.json)에 보존했다. validator 제품 코드는 이 시험 harness 수정 과정에서 바꾸지 않았다.

기존 P5의 두 번 재현·69파일 실제 이동 결과는 그대로 보존했다. 당시 임시 재현 디렉터리는 이미 정리되어 있어 이번에는 builder의 출력 경로 guard만 메모리에서 fix/rebuilt로 돌린 단일 재현을 수행했고, 변환 코드·원본 파일·hash 계산은 그대로 사용했다. 대규모 이동 시험이나 다중 재생성을 반복하지 않았다. [check_rebuilt.py](check_rebuilt.py)에 경로 guard 변경과 실행 방법이 남아 있다.

## 불변 범위와 남은 일

원문·84-field contract·manifest v2·builder/rules/transport/type-contract·원 candidate·기존 P5 증거는 변경하지 않았다. 시작 해시에는 경로 표기 차이로 중복된 행이 있어 종료 비교에서 동일 경로·동일 시작값을 확인한 후 1,665개 unique 경로로 집계했다. [protected-start.json](protected-start.json), [protected-end.json](protected-end.json), [code-hashes.json](code-hashes.json), [independence.json](independence.json)이 원문·코드 경계와 새 validator hash를 남긴다.

152 미부착 필드는 candidate_only 49 / out_of_batch_entity 83 / owner_unresolved 20으로 같다. eligible 1,242 + not_created 152 = 원문 1,394 field, 4,170 leaf이며 raw-only 56행·132 field, collision 복원 3행·16 leaf, 4,576 field locator 검사도 유지했다. 임상 검토는 0건이다. 이 보완은 152 원문 분류나 attachment 결과를 바꾸지 않는다.

남은 일은 별도 P5 독립 재검수에서 두 finding과 추가 회귀 증거를 확인하는 것이다. 정본 전환·임상 판단·새 데이터 설계는 수행하지 않았다.

## 재실행

원 candidate에는 CLI를 실행하지 않는다. 새 목적 폴더를 사용하려면 run_probes.py의 출력 R을 새 fix 하위 폴더로 지정한다. 기존 목적 폴더는 변조 증거이므로 전체 스크립트가 덮어쓰지 않는다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 silver-batch1-validator-fix/run_probes.py
PYTHONDONTWRITEBYTECODE=1 python3 silver-batch1-migration/test_contract.py --candidate silver-batch1-validator-fix/positive-copy
PYTHONDONTWRITEBYTECODE=1 python3 silver-batch1-validator-fix/check_rebuilt.py
python3 silver-batch1-validator-fix/finalize_evidence.py
```

위 경로는 `orchestration/work/phub-recommend/` 기준이다. test_contract.py는 복사본의 counterexamples.json/tmp만 쓰며, validate CLI는 fix 하위 복사본의 validation.json만 썼다.
