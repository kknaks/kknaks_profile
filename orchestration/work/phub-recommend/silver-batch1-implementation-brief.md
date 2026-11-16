# WORK-013 첫 실버 candidate 이관 구현

## 승인·계약

사용자가 reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md 계획대로 진행하도록 승인했다. 단계3 pilot core 독립검수 PASS 및 첫 이관계약4건 보완을 코디가 직접확인했다. **지금부터 DATA-001/2와 WORK-013 현행판에 따른 실제 candidate 이관기와 결과를 구현한다.** 원본 정본 교체/서비스전환은 아니다.

이 폴더 DATA-001.md, WORK-013.md, silver-data-contract-batch1/field-contract.json, contract-fix/{report.md,input-manifest.v2.json,collections.json,reconciliation.json,evidence-manifest.json}를 순서대로 읽는다. 이전 input-manifest는 history이며 실행입력은 v2다. silver-batch1-contract-review/report.md의 CR4건 수정근거도 확인한다. 코디는69input hash, frozen log/audit source분리, 원문1394field를 직접검증했다. 기존 pilot source/ID/refs/scope/rule 보완은 재사용할 개념 근거이나 코드·schema의42사례전용제약을 전수이관에 그대로 복사하지 않는다.

## 구현범위·순서

WORK-013 §1~7의 P0~P4, allowed_paths·정해진CLI·수용기준을 그대로 수행한다. product395(active354/inactive41)/family27/product_family source354/safety580행의 전체 candidate 및 실제 typed product/family와원문claims·mapping/identity ledger·coverage를 생성한다. safety1394field4170leaf 모두독립원문대조, common3collision의6field16leaf(기존소실10) 복구 및624override의원문연결 before/after를 구현한다. LOSS02는unit U5-016, 후보19+원문보관37행132field는claim보존·attachment미생성이다. 나머지도단일owner가실제검증될때만attachment를생성하고전체eligible+not_created분모를닫는다.

84필드의exact타입/필수·빈값/의미/source/normalization/oracle를구현한다. JSON외research/decision text는계약에명시된media_type/text-root/source lines/hash로보존한다. 허가진위·임상적용·제품선택을새로결정하지않고legacy상태·needs_design을유지한다. subfamily/purpose새ID발급금지, technique/unit은필요한제한registry참조검증이다.

새schema/ref/rule판과source별공통계약, source-domain+collection+logical key와physical locator분리, typed refs/판/normalizedID/모든scope불변식을적용한다. audit-only변화의데이터ID불변과rule실제변화의revision영향을구분한다. frozen입력을직접읽고_RESUME현재판을입력으로읽지않는다. manifest불일치시조용한재baseline금지. 변경이필요하면구체적ask.

독립validator는builder변환함수를정답으로import하지말고실제원문·고정규칙·oracle를읽는다. 명시긍정/변조·전체분모·fieldcoverage·원문loss·정상rename·미정/후보/ownerless·이동·2회재현·룰판·auditID대조를실행한다. ID재계산변조에도관련의미진단을확인한다. inspection counts를임상검토수로부풀리지않는다. 구현자임의로과거source교정/새규칙을추가해PASS시키지않는다.

## 경계·소유

쓰기허용은 WORK-013 그대로 silver-batch1-migration/**, silver-batch1-candidate/**, silver-batch1-implementation/report.md뿐이다. temporary/reprorelocation도candidate/tmp아래에만작성하고cleanup한다. candidate기존존재여부를확인하고다른작업과충돌하면ask한다. source/정본/decisions/apply/스킬/semantic/Gold/HTML/design/pilot/review/스펙·WP/계약manifest/앱·Hub/env/DB/서버/포트/컨테이너 변경금지. 네트워크/모델/설치/하위worker/commit/push/PR금지.

코디진행기록변경은고정frozen source와별개다. immutable입력hash와mutable작업상태를분리하고정본계약은이번시작판으로고정한다. canonical전환옵션은제공하지않는다.

## 보고·완료

초기입력gate와예상output분모를status로보고하고질문은livepreamble ask. P0~P4통과후실제분모/84field별typed/raw/needs_design/제한registry·247전체coverage/안전손실복구/override/미정/반례·재현·이동/보호입력/정본무변경을report.md에쓴다. PASS이어도독립candidate검수P5와정본전환은미실행으로남긴다. live Orca inbox/heartbeat를따르고worker_done한번보고후멈춘다.
