# P5 검증기 보완 독립 폐쇄 검수

현재 역할은 독립 리뷰어다. 구현하지 않는다. 앞선 대화 대신 이 브리프와 아래 파일을 읽는다. 목표는 기존 P5의 BR-H1(scope 원문 의미 검증 누락)과 BR-M1(line 관계 삭제 미탐지)의 폐쇄 여부 판정이다. 새 데이터 설계나 임상 판단은 범위 밖이다.

## 읽을 것과 대상

이 브리프가 있는 폴더를 기준으로 한다.
- silver-batch1-review/report.md 및 원 P5 full_cli_probes.py/full_qualifier_probe.py: 최초 finding과 재현법.
- silver-batch1-validator-fix/report.md, full-cli-probes.json, code-hashes.json, independence.json, protection-result.json.
- silver-batch1-migration/validate.py, independent_source.py, test_contract.py.
- DATA-001.md, WORK-013.md, silver-data-contract-batch1/field-contract.json과 contract-fix/input-manifest.v2.json: 고정 계약과 실제 source 위치.
- silver-batch1-candidate/**: 기존 고정 후보판, 읽기 전용.

## 해야 할 것

1. builder/rules를 정답으로 재사용하지 않고 실제 원문으로 1,002 scope의 축·qualifier·parent·conflicts·application/source refs와 395 product line 관계 기대 목록을 검증하는지 읽고 확인한다. 동일 변환을 그대로 복사해 동일한 오답을 정답으로 삼는 위험도 확인한다.
2. 정상 candidate를 쓰기 없는 함수로 검증하고, 원 P5 세 반례(원문 없는 excluded 추가, qualifier 전체 삭제, line_memberships 삭제)를 자신의 별도 복사본에서 재현한다. normalized ID·sidecar·output manifest까지 정합시켜 전체 CLI에서 의미 진단으로 거부되는지 확인한다. 단순 hash/ID/export 불일치로 거부된 것을 폐쇄로 인정하지 않는다.
3. BR-H1의 의미 축/qualifier 필드와 BR-M1의 누락·추가·부분 소실·미정 관계 보존을 겨냥한 회귀 증거를 확인한다. 필요한 새로운 반례만 최소한 추가한다. 정상 원문 scope 미해석 상태와 line unresolved가 유지되는지 확인한다. 변경 없는 builder의 기존 재현/이동 증거는 재사용하고 대규모 재생성 반복은 하지 않는다.
4. candidate·원문·builder·계약·이전 검수 증거가 바뀌지 않았는지 확인한다. cards v2는 원문 문맥/복수 연결 규칙을 설명하는 사용자 검토판이며 임상 승인이나 후보판 변경이 아니다. 이 검수에서 cards나 152개의 데이터 의미를 승인/수정하지 않는다.

## 권한과 산출물

새 silver-batch1-validator-closeout-review/** 안에만 report.md, 재현 도구, 시험용 복사본, 결과/해시를 쓴다. 나머지는 전부 읽기 전용. validate CLI는 validation.json을 쓰므로 원 candidate에 실행하지 않는다. 서버/DB/네트워크/모델 API/설치/하위 워커/commit/push/PR 금지. 범위 밖 필수 변경이 있으면 ask한다.

report.md 첫 문장에 PASS/WARN/FAIL, BR-H1/BR-M1별 폐쇄 여부와 실제 재현 근거, 남은 제한을 적는다. 원문 값의 의학적 정확성이나 정본 전환 완료라고 하지 않는다. 수행하지 않은 시험은 수행했다고 적지 않는다. 완료는 live Orca preamble의 heartbeat/check/worker_done 절차를 따른다. worker_done 한 번 이후 멈춘다.
