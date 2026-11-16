# 데이터 설계 3단계 — 실제 원문 사례를 새 구조로 표현·검증

## 사용자 승인·목표

사용자는 reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md 계획대로 발주하라고 지시했다. 다음은 §6의 **3. 실물 설계 검증**이다. 기존 데이터/서비스를 바꾸기 전에 실제 원문으로 제안 구조가 손실·오연결·조건 누락을 막는지 검증한다. 설계 문서를 더 늘리는 것으로 끝내지 말고 **기계가 읽고 검사할 수 있는 실제 pilot records와 검증 결과**를 만든다.

## 입력·계약

루트 AGENTS/문서 규약과 이 폴더 silver-origin-structure-audit/{report,issues,inventory,id-design}.json 또는 .md, silver-entity-graph-design/{design.json,index.html,evidence.md}, 위 reference WORK를 읽는다. 원문21과 현재 실버/decisions/생성기/semantic은 읽기 전용이다. path는 inventory에서 확인한다. 현재 신뢰 가능한 엔터티 ID를 재사용하고 원문 occurrence/claim/mapping/scope/decision을 제안 의미에 따라 구분한다.

## 작성할 실물 pilot

허용 작성 경로는 이 폴더 silver-design-pilot/ 하나다. 다음을 실제 원문 locator/hash와 연결하여 pilot.json(또는 명확한 타입별 JSON)으로 만든다.

1. 안전 alias collision 3행의 원래 common 계열 목록을 **각 source field/잎 그대로 보존**한다. 손실10항목과 기존 남은 값 모두를 추적하고 normalized predicate와 raw field를 분리한다. 같은 문장 타출처/타행을 content만으로 합치지 않는다.
2. 중복 CC2키4행을 source occurrence로 구분하고 튼살2행의 올바른 대응 P9-4와 기존 잘못된 연결을 비교한다. 이름 first-match/중복 legacy alias가 단일확정으로 승격되지 않게 한다.
3. CC 원문 combos146개 전체의 arity 분포를 대조하고 singleton21은 pair가 아닌 구조로, n-ary는 원문 구성과 전개근거를 보존한다. 기존 note7을 실제 R8 claim7과 source_record_ref로 연결한다.
4. same_site/different_site에 따라 first가 달라지는 R8-0001을 필드조건별로 표현한다. 원문·staff_check를 유지하고 임상 승인을 만들지 않는다.
5. 비교필러 ambiguous 후보와 제품다계열/override_of=M4를 각각 mapping candidates/selected 및 claim scope로 분리한다. 단독 팔자 확정 연결을 발급하지 않는다. K8-0028/29 기존 명시 metadata도 보존한다.
6. 팔자 container/목주름 statement scope 충돌, patient.ko 한정차이, duration 원천2claim과 보수 resolution/alternatives를 각각 표현한다. 원장미정은 그대로 미정으로 남겨야 통과다.

피상적인 예시 문자열로 대체하지 않는다. 원문 실제 값과 기존42 evidence를 재사용하고 무엇을 직접 구조화했는지 전수/표본 분모를 기록한다. 실버 전체 이관이라고 부르지 않는다.

## 기계 계약과 검증

- pilot 범위의 JSON Schema 또는 동등한 엄격 validator를 만든다. ID/필드 type/required/enum/빈값 의미/참조/원문hash+pointer/후보·확정·조건 불변식을 검사한다. 최상위에 schema_version과 설계 basis hash를 기록한다.
- 이름/배열번호만을 entity ID로 새로 만들지 않는다. snapshot+pointer occurrence와 entity identity는 별개다. legacy alias의 일대다/ambiguity도 표현한다. rule/검토 이력은 실제 근거가 있는 것만 연결하고 가짜 승인자/과거 승인일을 생성하지 않는다.
- 생성 결과와 자신을 대조하는 시험만 쓰지 않는다. **원문 snapshot을 독립적으로 읽어** raw values·구성원·scope근거·역추적을 대조한다. alias 병합·same-name first-match·조건삭제·후보확정·누락 claim ref·잘못된 source hash 등 명시 변조본이 거부되는지 확인한다.
- 제안 필드가 실제 사례를 표현하지 못하면 몰래 schema를 바꾸거나 임상값을 채우지 않는다. gaps.md에 정확한 필드·사례·최소 변경안을 기록한다. 원문 근거로 정할 수 있는 표현상 선택은 근거와 함께 제안으로 분리하고 코디에게 ask한다. 미정은 미정으로 표현 가능한 것이 설계 성공이다.
- 논리 타입→골드 노드/엣지 **검증용 투영**을 제공하여 후보/조건/출처가 남는지 확인할 수 있으나 실제 Gold builder/DB는 수정하거나 실행하지 않는다. 모든 claim을 무조건 노드로 만들지 않고 design.json 대응을 따른다. 잘못된 자동 확정 엣지가 나오면 FAIL이다.

## 산출물·수용 기준

pilot 데이터, schema/validator, 독립 source 대조 및 변조 검증 코드, validation.json, gaps.md, report.md를 허용 폴더 안에 둔다. report에는 사례별 원장→기존실버→pilot→제안graph 추적과 PASS/FAIL/미정, 손실0/후보승격0/조건보존/역추적/ID참조 결과, 실제 검토 분모와 미착수 전체범위를 쓴다. 검증수가 많다는 이유로 임상정확도·전수설계 승인이라 쓰지 않는다. 본인 생성 artifact는 재실행 가능해야 한다.

입력 파일 시작/종료 hash로 원장·기존 실버·HTML설계 불변을 확인한다. 필요하면 HTML에 넣을 사례표를 별도 pilot 폴더에 만들 수 있으나 기존 HTML은 수정하지 않는다. 다음은 코디 검증 및 독립 검수 뒤 설계확정/실버 이관 준비이며 이번 워커는 전체 이관을 착수하지 않는다.

## 금지·보고

원장/실버정본/decisions/apply/스킬/semantic/Gold/앱/Hub/기존설계·스펙/공유env/DB/서버·포트 수정·기동 금지. 외부 모델/네트워크/임의 설치/commit/push/PR/하위 워커 금지. 기존 생성기를 정본 출력으로 돌리지 않는다. 체크포인트 status 및 live preamble의 inbox/heartbeat를 따르고 완료 시 실제 결과·막힌 설계·잔여범위를 세 문장 요약과 report-path/files-modified로 worker_done 한 번 보고하고 멈춘다.
