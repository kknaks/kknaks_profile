# 실물 pilot v2 독립 재검수·설계 채택 범위

## 목표

사용자 승인 WORK(reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md) 단계3 재검수다. silver-design-pilot-v2-brief.md/contract.md와 v1 독립검수 silver-design-pilot-review/report.md H1~H3/M1~M2가 수용 기준이다. v2의 record/schema/builder/validator/identity/ref/invariants/projection 및 실제 source를 읽고 보고를 검증한다. 실제 원장/실버/정본 설계/서비스 변경 금지.

## 필수 검수

1. 이전 H1~H3/M1~M2를 항목별로 닫는다. 실제 builder의 물리 이동 ID 불변, logical file/domain 분리, collection manifest/snapshot/source vs schema/rule revision, 재정렬/native entity 보존을 직접 재현한다. normalized revision ID의 content/contract판 경계를 확인한다.
2. typed refs의 타입/도달성/축·literal 구분, decision authority/target/supersedes, override refs, attachment witness 및 rule version/hash를 확인한다. 범용 진단이 기존 KeyError fallback 없이 관련 실패를 표시하는지 확인한다.
3. 원문·raw와 scope/predicate/variant/direction/interval 등의 의미 검증을 구분한다. 원문 independent source review를 재실행하고 기존31/리뷰24/재해시20의 actual 실패원인이 적절한지 확인한다. ID재계산을 해도 scope/기간/refs/승인 조작이 거부되는지 대표 추가 반례를 확인한다. 검증수만으로 임상 승인하지 않는다.
4. 정상 exact identity8개·source lookup167·후보 selected0·미승인 clinical edge0 보존을 검수한다. 모든 사실을 withheld로 바꿔 PASS시키지 않았는지, source evidence 조회와 clinical approval 구분이 명확한지 확인한다. 원천 미정과 아직 구현하지 않은 완전성은 잔여로 분리한다.
5. v2가 설계247필드/전체 entity 전체에 대한 이관기인지 pilot 명시범위인지 정확히 판정한다. PASS하면 채택 가능한 ID/refs/scope 계약과 다음 단계(설계 정본 반영·실버 이관 계약)에서 필요한 필드/타입 coverage 및 검증 조건을 구체적으로 인계한다. 임상값·원천미정 해소를 제안하지 않는다.

## 범위·검증

작성은 silver-design-pilot-v2-review/의 report.md와 읽기 전용 재현 probe/결과만이다. 원문/실버/design/HTML/v1/v2/스펙/WP/앱/Hub/env/DB/서버 무변경. 직접 validator main은 validation.json을 쓰므로 safe_validate/함수 import 또는 별도 결과경로로 검사하고 기존 산출물을 다시 쓰지 않는다. protected 시작/종료hash와 기준코드 hash를 남긴다. 직전 구현 워커 runtime은 user_takeover retained 상태이므로 검수 중 공유 변경이 있으면 기준판을 명시하고 혼합 판정 금지. 네트워크/모델/설치/하위워커/commit/push/PR 금지.

범위를 무제한 확대하지 말고 명시 H1~M2 수정·핵심 불변식에 집중한다. 발견한 추가 결함은 재현·severity·영향을 보고하되 실제 해결된 것과 비구현 후속범위를 구분한다. PASS/FAIL, 항목별 원문/코드/변조 근거, 재실행 수와 잔여를 report.md에 쓴다. 전체 임상/전수이관/usable Gold 승인은 범위 밖이다.

live Orca preamble대로 체크포인트 inbox/heartbeat 처리, 완료 시 세문장 요약·report-path/files-modified로 worker_done 한 번 보고 후 멈춘다.
