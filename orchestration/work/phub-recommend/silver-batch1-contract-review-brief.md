# DATA-001/WORK-013 첫 이관 계약 독립 검수

## 목표

사용자 승인 계획 단계4의 구현 선행검수다. DATA-001.md→WORK-013.md와 silver-data-contract-batch1/field-contract.json(84필드), 원문 oracle/results 및 silver-pilot-closeout-review/report.md·coverage.json을 읽기 전용 검수한다. 문서가 실제분모/필드의미/원문판/변환/필수·빈값/refs·판·scope를 정확하고 구현가능하게 정했는지 확인한다. 원장·실버정본·설계 제안/검증된core/이번신규계약을 구분한다.

## 핵심 검수

- product14/family11/common59 각필드의 실제source/current locator·타입·required/nullable·transform·oracle가 충분한지 대조한다. 이름/fieldmatch만으로 typed완료를 주장하지 않는지, 허가/규격/업체역할 등 실제 다형구조를 문자열·일대일로 임의 압축하지 않는지 확인한다.
- 원문21/역사artifact/generated/decision collection membership와 고정 inputmanifest가 domain/logical key·ID이동/판 규약에 맞는지 검증한다. mutable _RESUME/WORK 기록판의 구현시 reconciliation 절차가 명확한지 확인한다. json외artifact source transport도 결정적/검증가능해야 한다.
- 분모 product395(active354/inactive41)/family27/mapping354/safety580(1394field4170leaf)/override624를 실제파일로 재집계한다. 3collision/16잎과 source_text→override 복구, 정상rename 유지의 수용기준을 원문으로 확인한다. LOSS02 unit U5-016을 product로 발급하지 않는지 확인한다.
- identity_kind/이동·병합·비활성·기존ID 정합, 불완전허가/미정/후보·family=null3·needs_design·제한technique 참조를 무조건값으로 채우지 않는지 검토한다. claim scope·mapping·임상 적용·attachment/decision 규칙의 일반화가 pilot전용제약과 모순되지 않는지 확인한다.
- 84field의 계약과 후보파일/CLI/allowedpaths/독립validator/긍정·변조/재현성·이동·안전필드 원문대조가 구현자 임의발명 없이 닫히는지 확인한다. 247전체 baseline 및 163범위밖 coverage와 미정3을 보존한다.
- candidate vs canonical transition 권한/실행·rollback 분리, 정본 source 생성기/DB/Gold/앱 무변경이 명확한지 검토한다. 실제 이관을 막지 않는 범위 안에서 중대한 모순/모호성만 finding으로 적는다. 임상값을 새로 결정하지 않는다.

## 실행·산출물

작성은 silver-batch1-contract-review/report.md 및 읽기전용검증script/results만 허용. DATA-001/WORK-013/field-contract/oracle/기존pilot/원장/실버/앱·Hub/설계·스펙/환경/DB/서버 수정금지. 네트워크/모델/설치/하위worker/commit/push/PR금지. locator/type/분모와 문서crossref·hash를 독립검증하고 PASS/FAIL·severity별근거/재현·필요최소수정·candidate구현가능범위·미확정을 보고한다. scope를 전체 임상재인증으로 확대하지 않는다.

시작/종료 보호hash를 남기고 live Orca preamble의 inbox/heartbeat/worker_done을 따른다. 완료 뒤 멈춘다.
