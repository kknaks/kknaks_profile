# v2 pilot 잔여 scope·rule 검증 보완

사용자 승인 데이터설계 단계3 계속. silver-design-pilot-v2-review/report.md의 R-H1/R-M1 두 메커니즘과 추가10변조가 범위다. 앞서 닫힌 ID/typed refs 보완은 유지한다. 전체25타입247필드 이관기는 이번 범위가 아니다. v3 전체 복제는 만들지 말고 **기존 v2의 계약/validator와 필요한 schema·builder만 최소 수정**한다. v2 원문 pilot 값이 근거 없이 달라져서는 안 된다. 변경 전 코드/contract/data hash와 patch 차이를 보고한다.

## 계약 먼저 보완한 뒤 구현

1. scope 모든 축의 included/excluded 교집합·중복·knowledge와 값의 조합을 명시하고 검사한다. 같은 대상을 동시에 포함·제외하는 미지원 표현을 거부한다. 상충 원문은 conflicts+source evidence로 별도 보존해야 하며 무조건 포함/제외로 승격하지 않는다. explicit/unknown/not_declared/not_applicable별 허용 원문근거/값 상태를 정의하되 unknown이라는 이유로 후보 정보를 전부 지우지 않는다. 실제 pilot에서 허용한 각각의 축 상태를 조사하여 안전한 일반 불변식과 source-specific 정합을 함께 적용한다.
2. container_scope_ref는 타입/도달성만 맞으면 끝이 아니다. self/cycle·무관 source parent·원문이 뒷받침하지 않는 scope 합성을 거부한다. source_record/claim 계통과 현재 실제 context를 대조한다. 언어 family와 조합 container의 source-constrained included/excluded/knowledge/parent를 재해시 후에도 검사한다. 현재 null인 parent를 무관 existing scope로 바꿀 수 없어야 한다. 정당한 parent를 지원하는 범위를 계약에 명시하고 증거 없는 positive를 만들지 않는다.
3. resolution policy.id/version/code hash를 기존 decision source판과 함께 exact 검증한다. attachment rule의 id/version 및 선언된 구현·계약 fingerprint를 typed contract로 고정하고 빌더가 생성한 임의 값 자체를 oracle로 쓰지 않는다. 실제 선언 rule과 의미/source/target/application 관계를 검사한다. 새 임상 승인/원천정정은 없다.

## 검증

리뷰 additional.py/independent-additional.json의6허용변조를 v2 회귀에 포함하고 전10개 및 이전75개 모두 관련 check로 거부되는지 확인한다. normalized ID 재계산 및 projection 재생성 후 검증해야 한다. 범용 scope 교집합/knowledge/parent 검사에 대한 다른 축·self/cycle·rule버전 변형도 명시 범위 안에서 점검한다. 정상 source-confirmed identity8개·source lookup167·원문LOSS16·combos146·조건/후보미정 보존을 동시에 확인한다. 검사수와 의미검토수를 구분한다.

원문 독립대조996·ID이동/판24·positive6을 필요한 회귀로 한 번 재실행한다. 원문·실버·기존 HTML/design·v1/v1리뷰/v2리뷰·스펙/WP/앱/Hub/env/DB/서버 무변경. v2 보호입력baseline을 소급 갱신하지 않는다. mutable 진행기록 hash 차이는 따로 보고한다. 원문 domain/locator/ID 알고리즘을 다시 바꾸지 않는다.

작성 허용 v2/{contract.md,invariants.py,validate.py,ref_contract.py,ref-contract.json,schema.py,schema.json,build.py,probes.py,semantic_probes.py,positive_controls.py} 중 필요한 파일과 신규 scope_rule_probes.py·결과JSON·scope-rule-fix-report.md. run.py·기존 정상 산출물 재생성은 기존의존 변화에 필요한 경우에만 하고 기록한다. 다른 파일 필요시 ask. 수정결과 각 R-H1/R-M1 근거·정상/변조결과·diff·코드hash·잔여coverage를 scope-rule-fix-report.md에 쓴다.

네트워크/모델/패키지설치/하위worker/commit/push/PR 금지. 데이터 이관/본설계 정본 반영/전체 필드검수 완료를 주장하지 않는다. live Orca preamble대로 inbox·heartbeat를 처리하고 완료시 세문장 요약·report-path/files-modified로 worker_done 한 번 후 멈춘다.
