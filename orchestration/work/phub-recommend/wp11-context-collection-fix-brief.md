# WP11 원문·관계 수집 누락 및 H01 수정

## 대상과 계약

기존 clinic_chat/hub-evals 미커밋 WP11 위에서 구현한다. 정본은 이 폴더 SPEC-006 §3-4-1-8 B01/B02, WORK-012 WP11이다. 직전 독립 검수 profile reference/2026-10-30-hub-evals/build-out/wp11-context-review-retrieval-report.md의 H01/M01/M02와 endpoint별 설명을 먼저 읽는다. 보고서는 제안이며 정본의 무관 그래프 확장 금지·같은 적용 범위 문맥 보존·app 구조검증을 우선한다.

## 수정 결과

1. H01: 질문에서 조건을 언급하지 않거나 다른 조건을 언급했다는 이유로 경고를 제외하지 않는다. 검증된 동일 unit/site의 조건부 경고는 조건을 붙인 전체 원문으로 보존하고 manifest 의무로 전달한다. 적용 관계가 불명확하면 보류한다. 제외는 명시적으로 증명된 범위 불일치에만 허용한다. 기존 test_other_condition...의 잘못된 기대도 바로잡는다. 알레르기 미언급/임신만 언급/conditional+conflict 미선택 경고의 재현을 회귀 시험으로 만든다.
2. M01: 기존 collection 단계에서 active branch/필요 section의 context 후보 원문을 기존 T11 fact_ids로 수집한다. 기존 support selection과 독립시키고 full_cache(node,id)/검증/build/cut/중복 방지를 재사용한다. 저장 Q002의 보류57은 요청 실패가 아니라 미선택이므로 해당 유형들을 빠뜨리지 않는다. 현재 raw line을 원문으로 승격하지 않는다.
3. 관계 proof는 기존 공개 API에서 후보 owner에 필요한 것만 받는다. 다른 treats inbound T8 exact edge endpoints, 이미 노출된 combo 구성/anchor 및 source member 범위, unit T5 checks의 ID별 conditions/target scope/not_condition, complication unit/family T8를 활용한다. 공개 response의 실제 shape를 Hub 코드에서 확인하고 exact ID/build/owner/source/endpoint를 join한다. 앱이 넣은 applies_to=owner를 독립 관계 증명으로 쓰지 않는다. 알려진 field가 부족하면 unknown/hold와 정확한 Hub 필드 요청안을 보고하고 추정으로 메우지 않는다.
4. M02: support 충족과 필요한 context inventory 완료를 구분하여 장부에 기록한다. active unit/required section의 필요한 slim inventory와 확인된 scope만 다루며 무관 이웃 본문이나 그 이웃에서 새로운 frontier를 만들지 않는다. support 발견만으로 context 완전성을 선언하지 않는다. 공개 summary/관계로 범위를 닫을 수 없는 잔여는 unresolved로 표시하고 bundle을 승인하지 않는다. 전체 graph/full=true/sections=all 일괄 수집이나 고정 depth/고정 호출 예산으로 근거 없음 처리 금지. 기존 Jev 노드 relevance/stop 및 visited/request tuple·deadline/no_progress·build mismatch 경계를 유지한다. 계약을 바꿔야만 해결된다면 코드로 발명하지 말고 ask한다.
5. make_bundle은 완성된 collection ledger를 읽기만 하며 새 호출을 넣지 않는다. same-scope 미선택 제한/상충/필수 source와 borrowed receipt를 보존한다. context 누락을 unresolved_absence로 덮지 않는다. 각 후보의 requested/received/missing/failed/scope_unknown/proved_excluded를 trace에서 구별한다.

## 범위·금지

앱 case3.py, hub_rest adapter 필요 부분, 관련 tests/fixtures만 편집한다. 기존 다른 미커밋 변경을 유지한다. Hub 코드는 읽기만 허용하고 수정 금지. 정책/registry/threshold/prompt/calibration artifact/.env/DB/publication pointer/사용자 서버·컨테이너 변경 금지. 실제 네트워크/Claude/Jev/judge/배치 호출 및 서버 기동 금지: 이번은 공개 응답 계약에 맞춘 offline/fake 구현과 검증이다. 커밋/push/PR/하위 워커 금지. 실제 API의 성공을 fake로 주장하지 않는다.

## 수용·검증

- 기존 저장 fixture는 원문 미수신이므로 그대로 보존하며 성공했다고 주장하지 않는다. 별도 공개 response 모양 fixture로 context candidate→targeted full/relations→same-scope receipt/manifest 경로와 실패 경로를 검증한다. 원문을 합성한 성공을 실제 Q002 성공으로 기록하지 않는다.
- H01 오류 차단, family 연구/체크·global 조건/합병증/조합/다른 concern의 정확한 적용 검증, source/build/owner 위조·cut·full 누락·관계 truncated 차단, 중복 요청 없음, context 미완료가 facet supported로 감춰지지 않음, 여섯 branch 보류 유지.
- 전체 pytest/Ruff/diff check. 결과·변경 파일·실제 수집 미선택57 해소 경로·아직 unknown인 공개 필드·다음 한정 API 확인 절차를 profile build-out/wp11-context-collection-fix-report.md에 작성한다. 구현 후 독립 검수 및 실제 한정 API receipt 검증을 코디네이터가 별도 진행한다.

## 보고

Orca live preamble의 Task/Dispatch/handle을 따라 체크포인트마다 inbox를 처리하고 완료 시 worker_done을 한 번 보낸 뒤 멈춘다. 세 문장 요약·report-path·files-modified를 포함한다. 막히면 구체적 행/필드와 최소 대안을 ask한다.
