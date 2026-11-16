# WP-10 안전 적용 증명과 facet 종료·부분 답 수정

## 대상·근거

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 코드. 기존 SPEC-006 0.3.13의 owner/source/scope·부분 답·필수 안전 계약을 구현한다. `wp10-semantic-state-fix-report.md`, `wp10-semantic-state-q002-result.json`과 과거 `wp8-answer-bundle-report.md`를 읽는다.
- Jev state 누락은 수정됐고 361 tests PASS. Q002 후보 7개 Noul 0.78~0.97, Jev 3회·Hub 219회·574KB. 그러나 14 branch의 site_caution blocked로 Claude 0회, `partial_source_contract`가 네 역할을 나열해 필러 부위 위험 누락으로 안전 FAIL. 과거 같은 Gold에서 필러 `SC-nasolabial-M2`의 공개 적용 경로와 원문은 이미 증명됐으므로 **실제 Gold 누락과 앱 상태 연결 오류를 분리**해야 한다.

## 작업

1. 저장 trace로 safety fact의 received→verified full→public safety proof→facet_state→selection→answer_scope를 각각 대조한다. 필러의 확인된 unit key/추천 카드 family·companion.site_caution/원문 owner/source가 초기 facet 지원 판정에도 쓰이는지 확인한다. owner==unit만 요구해 유효한 family/site 소유 원문을 다시 버리는 회귀, `applies_to` 표현 불일치, treats/treats_unit 중복 상태를 찾아 고친다. 공개 경로가 증명되면 facet을 supported로 닫아 무관한 뒤 page를 취소한다. 조건/부위/계열 불일치는 계속 거부한다.
2. 팔자 보톡스처럼 공개 부위 위험이 실제로 없는 경우에는 범위를 특정해 보류한다. 이를 필러의 유효 위험까지 모두 blocked로 만드는 이유로 사용하지 않는다. Hub 변경이 필요하면 원천/공개 API의 빠진 칸을 증거로 보고하고 앱에 위험 문구/ID를 하드코딩하지 않는다.
3. 안전 미지원 갈래를 `partial_source_contract`에서 추천 역할처럼 나열하는 경로를 막는다. 충분히 지원되고 핵심 안전이 검증된 갈래가 있으면 그 **지원된 범위**로 Claude의 간결한 부분 답을 생성·동일 인용/범위/안전 검증하고 미완료 갈래는 별도로 보류한다. 모든 후보의 모든 section 완료를 지원된 부분 답의 선행 조건으로 요구하지 않는다. 안전 계약을 완화해 통과시키지 않는다.
4. 실제 저장 안전 chain을 재현한 fixture, 타 부위/family/조건 음성, 같은 unit 다중 관계, 지원된 안전 뒤 page 종료, 진짜 공개 공백 보류, supported branch+blocked branch의 환자 답/비추천 보류를 검증한다. 전체 suite/Ruff/diff PASS 후에만 같은 Gold 격리 Q002 한 문항 재검증. 실패하면 반복 batch 금지.

## 경계·보고

- 사용자 Hub 18005·앱 18210·DB/컨테이너 비조작. 본인 격리 Hub 18015만 정리. Hub 코드·DB 수정/커밋·푸시·PR/50문항 금지.
- `reference/2026-10-30-hub-evals/build-out/wp10-safety-state-fix-report.md`에 원인 함수/상태 전이, 필러 vs 보톡스 공개 증거, 실제 답/Claude 호출·안전/관련성·인용, 호출/bytes/TTFT를 쓰고 Orca worker_done 보고.
