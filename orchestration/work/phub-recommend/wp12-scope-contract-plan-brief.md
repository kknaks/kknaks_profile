# WP12 적용 범위 projection 정본·작업계획 반영

## 대상·입력

이 profile 레포 문서만 수정한다. 이 폴더 SPEC-006 0.3.14 §3-4-1-8, SPEC-005/WORK-011의 기존 Hub 공개 계약, WORK-012 WP11과 reference/2026-10-30-hub-evals/build-out/wp11-response-review-scope-contract-report.md §5~9가 입력이다. AGENTS→para/para.md 및 관련 버킷 규약과 기존 템플릿을 읽고 문서 위치/양식을 유지한다. 기존 WORK 번호/slug/워크트리를 새로 만들지 않는다.

## 목표

코드 검수 R01/R02/R03 PASS 뒤 남은 실제 적용 범위 정보를 기존 Hub/app 계약에 추가한다. 먼저 SPEC 정본의 명확한 추가 절을 완성하고 이어 같은 작업의 WORK 계획에 Hub→app→독립 검수→격리 receipt→실제 Q002 순서를 작성한다. 문서 반영만이며 코드/실험 발주는 코디네이터가 한다. 현황을 성공으로 소급하지 않는다.

## 반영할 계약

1. selected T11 fact_ids의 원천 source.meta 및 source-specific scope projection, metadata-only scope mode와 full 원문을 구분한다. 기존 exact membership/build/node/echo/uniqueID/provenance/R01~03 보호를 유지하고 mode별 cache를 구분한다. 원천에 존재하는 값만 투영하며 누락/null/[]/false를 구분한다. 공개 REST/MCP 동일 계약 및 호환 기본 full을 명시한다. source.file/path canonical join과 metadata의 별도 일치 검증을 정의한다.
2. K8 conditions/target_keys/not_condition, combo member/anchor/source row/ambiguity, product 관계/family override/selection, note CC attachment/pair 미확정 및 family/site leaf를 보고서 근거에 맞춰 구체화한다. Q002 ID를 런타임 허용목록으로 사용하지 않으며 실제9/326은 수용 fixture의 증거로만 쓴다.
3. attachment와 적용을 구분한다. 제품이 선택되지 않은 일반 시술 질문에서 제품 전용 효과/위험을 무조건 시술 일반 사실로 승격하지 않는다. source가 명시한 제품/조합/쌍의 범위와 현재 답의 범위가 다른 것이 증명되면 이유·witness와 함께 non-required/excluded로 기록할 수 있다. 범위 불명확이 실제 주장/동일 범위 필수 경고에 영향을 줄 수 있으면 branch hold한다. unknown을 억지로 해소하거나 모든 attachment를 강제 필수로 취급하지 않는다.
4. ambiguous combo source_family를 exact site 적용으로 만들지 않는다. 승인된 source 범위 수준으로 조건을 붙여 보존할 수 있는 경우와 단독 unit 주장의 증명으로 사용할 수 없는 경우를 구분한다. 관련 제한/상충은 source 범위를 유지하고 누락하지 않는다. pair 없는 note는 pair_scope_unknown이며 임상 subject를 regex/LLM으로 합성하지 않는다. 경고 조건 미언급은 제외 사유가 아니다.
5. active scope inventory→selected scope metadata→필요 original→manifest의 단계별 완료와 justified_not_required 증거를 명시한다. Jev relevance와 앱 구조 proof를 구분하고 낮은 relevance만으로 필수 경고를 삭제하지 않는다. 필요한 범위가 closed일 때 종료, 원천 미확정이면 held 종료이며 무관 graph 확대/원문 일괄full/고정 budget을 도입하지 않는다. claim/제품 선택으로 scope가 바뀌면 관련 장부·의무·coverage를 다시 연다.

## 계획·검증

Hub 변경 파일과 app 변경 파일·필드 shape/에러/unknown reason 및 기존 호환성, 실제 응답 기반 양성·변조·scope 누락·mode cache 검사, 기존700 회귀, 격리 실제 receipt, 실제 답 생성/가독성 수용 조건을 구체적으로 쓴다. 구현 완료와 원천상 미확정 사실 해소를 분리하고 전체419 승인이나 최종 성공을 약속하지 않는다. Hub 원천 graph/DB를 새 사실로 수정할 계획은 넣지 않는다. 새 semantic 정책/임계값은 범위 밖이다.

정본 간 모순/중복이 없도록 근거를 링크하고 버전·수정일·의존을 일치시킨다. 과거 판/실행 기록은 현행 계약과 분리한다. 기존 문서에 열린 쟁점을 결정 없이 완료로 표시하지 않는다. 계약상 선택지가 불가피하면 근거·권고·영향을 별도 표시해 코디네이터에 ask한다.

## 경계·보고

허용은 이 폴더 SPEC-005/006, WORK-011/012의 필요한 정본 부분 및 profile build-out/wp12-scope-contract-plan-report.md뿐이다. 앱/Hub 코드·테스트/fixture/서버/DB/env/정책/모델/네트워크/하위 워커/커밋/push/PR 금지. 기존 다른 내용은 불필요하게 재작성하지 않는다. 완료 시 변경 절/확정 계약/남은 쟁점/교차 검증 결과를 보고한다. live Orca preamble의 worker_done을 한 번 보내고 멈춘다.
