"""Render a bounded acceptance report from executed evidence."""
from common import *
p=read(O/'pilot.json');v=read(O/'validation.json');source=read(O/'independent-source.json');probe=read(O/'probe-summary.json');sem=read(O/'rehashed-semantic-probes.json');ident=read(O/'identity-tests.json');protect=read(O/'immutability.json')
assert v['failed']==source['failed']==ident['failed']==0 and probe['existing_rejected']==31 and probe['review_rejected']==24 and sem['rejected']==20 and protect['immutable_unchanged']
lines=f'''# 실물 설계 pilot v2 결과

Task `task_99f21d64d6e3` · Dispatch `ctx_0c0e33f4ef79` · 2026-11-03 KST

**이 브리프의 단계3 명시범위 검사 PASS.** H1~H3/M1~M2 보완을 v2 안에 구현했고 기존 42사례·combos146·LOSS16잎·note7 및 미정 상태를 보존했다. 정본 설계 채택과 독립 재검수는 코디네이터의 다음 판단이며, 전체이관·전수임상·usable Gold·앱 적용 완료를 의미하지 않는다.

## 실행 결과

| 실행 | 결과 | 분모의 뜻 |
|---|---:|---|
| 독립 원천·schema·typed refs·의미 검사 | {v['passed']:,} PASS / {v['failed']} FAIL | 반복 기계검사 수; 임상 검토 건수 아님 |
| builder/validator를 import하지 않는 원문 대조 | {source['passed']} PASS / {source['failed']} FAIL | 원문21 JSON/hash, 사용 occurrence792 및 지정 사례 |
| 기존 변조 | {probe['existing_rejected']}/31 거부 | v1의 동일31개; graph 변조 포함 |
| 리뷰 추가 변조 | {probe['review_rejected']}/24 거부 | 리뷰 동일24개; 정상 positive 별도 통과 |
| ID 재계산 후 의미 변조 | {sem['rejected']}/20 거부 | normalized ID 불일치에 의존하지 않는 추가 실행 |
| 실제 builder ID/이동/판 시험 | {ident['passed']} PASS / {ident['failed']} FAIL | [identity-tests.json](identity-tests.json) |
| 보호입력 | {protect['immutable_files']}개 불변 | 시작/종료 SHA256와 bytes 일치 |

[positive-controls.json](positive-controls.json)의 재해시 정상본·확정 identity8개·후보 선택0·미승인 clinical edge0·별도 lookup 검사6개도 통과했다.

31+24=55는 **실행 수**이며 서로 독립인 결함55종이라는 주장이 아니다. 20개 추가 실행도 언어·기간·identity·승인·참조 변조를 의도적으로 중복해 ID 무결성 검사 우회 후 의미 검증을 확인했다. 합계75개 변조 실행은 모두 거부됐고, 정상본/확정 identity8개를 보존하는 positive controls는 통과했다. source pointer 오류는 `source_locator`로, 참조 오류는 `typed_ref`와 `path/target/target_type/reason`으로 보고하며 broad KeyError를 성공적인 거부로 세지 않는다. validator 내부 구현 예외는 재발생시켜 시험을 실패시킨다.

## H1 / M2 — 경로 독립 identity와 판

[contract.md](contract.md)에 구현 전에 수명을 정했다. `raw21`의 실제21파일 전체 manifest와 `generated-silver`7파일, `decision-artifact`1파일을 별도 domain/collection snapshot3개로 만든다. 원문 자체는21파일이며 generated/decision을 원문 수에 더하지 않는다. 정렬된 전체 logical file key+full SHA256가 snapshot을 결정하며 locator는 ID 입력이 아니다. 같은 basename/bytes라도 full logical file key가 다르면 occurrence가 다르다. domain이 다르면 snapshot/occurrence 모두 다르다. 모호한 중복 physical binding과 중복 logical key는 builder에서 거부한다.

물리경로에 고정된 의미 대조도 domain+logical file key로 바꿨고, 이동된 artifact 자체를 validator가 수용하는 positive를 추가했다. 실제 full builder를 임시 복사본에서 다시 실행해 디렉터리 이동 시 snapshot/occurrence/entity/normalized ID가 유지됨을 확인했다. 실제 source row 재정렬, display name 변경, 논리 file key 변경은 새 snapshot을 만들고 entity ID는 유지한다. source occurrence는 snapshot 판에 결합되므로 기존 source 기록의 continuity를 임의로 발명하지 않는다. source namespace:native_id만 entity identity로 사용한다. 테스트 파일은 끝나면 삭제했고 원문21 hash도 다시 확인했다.

record schema와 mapping contract revision을 바꾼 실제 builder 실행에서 source/entity ID는 유지되고 normalized revision ID는 바뀐다. design hash만 바꾼 메모리 입력에서는 ID가 유지된다. 정본 design은 고치지 않았다. validator는 snapshot/occurrence/normalized revision 공식을 builder import 없이 다시 계산한다. 원문 source identity와 normalized revision은 서로 대체할 수 없다.

## H2 — ref type·도달성·cardinality·승인 근거

[ref-contract.json](ref-contract.json)에 각 ref 경로의 target type과 schema cardinality를 함께 기록했다. entity 축·container 원문 literal·same_site/different_site enum·값 없는 축은 각각 value_kind와 축별 schema를 사용한다. 빈 axes를 허용하더라도 해당 사례의 필수 의미 범위는 원문 의미 검사에서 따로 강제한다. native ID, rule identifier, evidence literal과 graph record ref를 구분했다.

decision target/supersedes, override claim/scope/decision/source/override_of, attachment mapping/source/edge/component refs를 전수 도달 검사한다. witness는 실제 mapping source 및 attachment target과 일치해야 하고, edge/component가 있으면 그 relation member여야 한다. 실제 근거 없는 witness는 []로 남고 attachment8개는 unknown이다. 미지원 witness를 채워 usability를 주장하지 않는다. approved_rule은 기존 decision 원문의 이유/날짜/상태/대상과 묶고, reviewer 없는 human 변경과 발명 reviewer 모두 거부한다. 실제 사람 검토자·새 날짜·새 resolution은 추가하지 않았다.

## H3 — raw 보존과 normalized 의미의 분리

원문 raw/type/value 검사는 별도로 수행한다. language의 M2 family, unknown application, statement/patient_explanation predicate, 실제 source statement variant parent를 검사한다. combo의 원문 cc/cc_group container 및 unknown statement site/application, singleton/nary 방향, comparison subtitle context, 원문 family safety scope, timing conditional scope도 검사한다.

R8-0001의 “같은 날 가능”과 “동일 부위는 보톡스 먼저 / 다르면 순서 무관”을 독립 필드로 유지한다. days=null과 interval 수치 null을 함께 검사하므로 원문 없는0일을 다른 중복 필드로 밀어 넣을 수 없다. interval이 수치 기간의 정본이며 field_conditions.days는 독립 원문 근거 없는 경우 null이다. explicit_no_required_order는 not_declared/unknown/null과 다른 상태다. 팔자 container/목주름 statement 충돌, 한글 지연성 한정, 언어 동치 미검토, staff_check를 유지했다.

## M1 — exact identity8개와 적용 승인 분리

CC4개는 실제 correspondence와 taxonomy detail/parent=P9-4, timing endpoint2개는 from/to, duration2개는 step9 records.attach.nodes와 대조한다. selected 삭제, exact 전부 hold, rule id/version/hash 변경은 실제 생성기와 Silver 판 증거에 대조해 거부한다. source native_id와 snapshot source_kind도 검증한다. 후보 selected0과 identity exact8개가 동시에 유지된다.

검증용 [graph-projection.json](graph-projection.json)은 source_fact_lookup167개와 identity_lookup8개를 별도로 노출한다. 이는 조회 가능한 원문 fact/identity이며 임상 적용 승인과 다르다. 후보 목록, 조건, K8 준비/상담, 기존 D9-3 conservative view도 원문 trace와 함께 조회한다. procedure relation147개는 적용 보류이고 임상 확정 edge0이다. **전부 보류라는 사실은 usable Gold/API/탐색 검증 완료의 근거가 아니다.**

## v1 대응·refinement·LOSS02

[migration-map.json](migration-map.json)은 snapshot13→collection3 대응과 source/entity/normalized/case별 전건 ID 대응을 담는다. 기존 필드 삭제로 원문을 축소하지 않았으며 source occurrence792개, entity27개, scope165개, claim167개, relation147개, mapping288개, decision1개, resolution1개, attachment8개, alias2개, note7개, case42개다.

LOSS는 원문3행/6 field/16잎(기존 소실10잎 포함)을 복원했고, LOSS02는 원문 및 step5가 가리키는 `unit_procedure:U5-016`이다. 잘못된 product 예시는 정본 design에 소급 수정하지 않았다. v1의 nullable rule+reason, 조건 branch/options/enum, override metadata, 기존 R8 pair evidence 보존 refinement를 v2에도 유지했다. 두 comparison member는 고유8개 후보/후보항목16개이며 선택0이다. combo arity1=21/2=119/3=6, singleton pair0, note7 lineage, 올바른 P9-4와 과거 잘못된 R8 evidence, 언어5 claim, duration2+기존 resolution1을 보존했다.

## 보호입력·미정·다음 조건

[protected-start.json](protected-start.json)과 [protected-end.json](protected-end.json)은 immutable 입력과 mutable 진행기록을 분리한다. v1 WORK hash 불일치는 알려진 코디 진행 갱신으로 [immutability.json](immutability.json)에 이전/current hash를 기록했다. v1 baseline을 소급 수정하지 않았다. v1 pilot/review, 원문·실버·design·HTML·decisions·apply·semantic·스킬·WP·Hub·앱·환경·DB·서버는 고치지 않았다.

다음 조건은 독립 재검수, 이 ID/typed ref/의미 계약의 정본 채택 여부 결정, 원문으로 확정 가능한 combo member correspondence의 후속 설계, 조건부 fact/승인상태 소비 계약 결정이다. semantic 미검토1277칸, 안전580행 전수, duration196슬롯/343 alternatives 전수, 임상·허가·문헌 최신성, 전수 이관과 활성 Gold/API/앱/탐색 성공은 이번 검증 밖이다. clinical application, unknown/null/충돌, 언어 동치, 새 승인/새 resolution을 임의로 확정하지 않았다.

재현은 `PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-design-pilot-v2/run.py`다. 오프라인 표준라이브러리만 사용하며 산출물은 이 v2 폴더 안에서만 생성한다. 초기 protected-start baseline은 재생성하지 않는다. 네트워크·외부모델·설치·하위worker·commit/push/PR·DB/서버 실행은 없었다.
'''
(O/'report.md').write_text(lines)
