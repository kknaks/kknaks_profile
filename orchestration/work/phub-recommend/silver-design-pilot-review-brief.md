# 실물 데이터 설계 pilot 독립 검수

## 목표·정본

사용자 승인 계획 reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md §6 단계3의 독립 검수다. silver-design-pilot-brief.md, silver-entity-graph-design/design.json과 HTML, silver-origin-structure-audit/report.md를 기준으로 silver-design-pilot/의 실제 records/schema/build/validator/project/report/gaps를 읽기 전용 검수한다. 구현자 테스트가 초록이라는 이유만으로 합격시키지 않는다.

## 확인

1. 원문21 snapshot의 실제 원문을 독립적으로 읽어 LOSS3행16잎, CC duplicate2키4행/P9-4, combos146 arity, note7/R8 refs, R8 same_site/different_site 순서, ambiguous 후보, product M4 override, K8 metadata, 팔자/목 scope 충돌, 언어한정·duration resolution을 대조한다. 사례 분모·증거와 실제 표현이 일치하는지 확인한다. 올바른 원문/새 target과 기존 잘못된 실버 참조를 구분한다.
2. ID 계층·정합·안정성을 검수한다. 특히 **report가 occurrence ID를 snapshot hash+절대파일+pointer로 설명**하는 반면 기존 설계는 이동에 독립적인 snapshot+file identity를 제안했다. 실제 구현을 확인하고 단순 디렉터리 이동이 같은 원문/동일 snapshot/occurrence를 바꾸는지 재현한다. 원문 snapshot과 실버 파일판 snapshot namespace, schema/rule판 변경, 행재정렬·동명이행·legacy alias를 구분한다. 수정은 하지 않는다.
3. 엄격 schema의 refs·조건·후보/선택·raw/normalized·mapping rule/null+reason·source evidence·unknown·resolved 상태가 실제 계약에 맞는지 확인한다. 허용된 pilot refinement와 LOSS02 unit 분류 정정이 정확한지 검토한다. 가짜 승인/새 clinical resolution·원문 불명확을 확정하는 필드가 없는지 확인한다.
4. validator가 builder와 같은 가정·하드코딩 기대만 공유하거나, 관련되지 않은 실패로 변조31개를 거부하는지 확인한다. positive control/실제 source 독립 비교·타입 fidelity·원문추적·참조유형·조건/한정 손실·중복 collision에 의미 있는 반례를 추가로 메모리/별도 검수 scratch에서 재현한다. 정상 사례를 과도한 hold로만 통과시킨 것은 아닌지도 구분한다.
5. 검증용 graph의 source/claim/scope 보존과 후보승격0 및 singleton/nary를 확인한다. graph를 전부 withheld로 두는 것만으로 실제 설계 usability가 입증되는 것은 아님을 명시한다. 필요한 확정 mapping과 아직 미승인 적용을 구분하고 단계4 준비 가능한 정확한 범위와 추가 설계 결정을 보고한다.

## 실행·경계

관련 validator를 직접 실행하되 쓰기 범위를 확인한다. 입력·pilot 시작/종료 hash를 기록하고 보호원문/데이터/설계/코드를 변경하지 않는다. 신규 원문/임상문장을 합성하지 않는다. 작성 허용은 silver-design-pilot-review/ 아래 report.md와 필요한 읽기 전용 probe/결과만이다. 기존 pilot/HTML/schema/스펙·WP/원장·실버/Gold/앱/환경/DB/서버 변경, 네트워크/모델/설치/하위워커/commit/push/PR 금지.

## 판정·완료

report.md에 severity별 문제·정확한 파일/JSONpath·근거·재현·수정방향, 기존검증 재실행결과, 추가반례 결과, PASS/FAIL과 단계4준비범위를 쓴다. 검사수와 임상판정을 혼동하지 않는다. 전수실버 이관/최종답 성공을 승인하지 않는다. live Orca preamble대로 inbox/heartbeat 처리, 완료 시 세 문장 요약·report-path로 worker_done 한 번 보고 후 멈춘다.
