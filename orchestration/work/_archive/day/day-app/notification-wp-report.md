# notification-wp 결과 보고 — Delivery #235 v8 입력(원장 호출 알림)

## 상태: done (입력 JSON · 보고만 · SPEC · 코드 · GitHub · receipt · 커밋 · 하위 위임 0 · 승인 claim 0)

- 새 파일: `delivery-request-v8.json`(v7 사본에서 생성 · 생성 스크립트 scratchpad `gen_v8.py`) · 이 보고. v7 JSON 무변경(approved result 의 contract 와 v7 입력 일치 확인 — 차이 0).
- 유지: idempotency_key `day/day-app` · 같은 #235 · version 7 → **8** · L3 · 코드 PR #237 → dev 하나 · SPEC PR #921 → main · 머지 = 사용자 마지막 지시 · iOS 먼저 · 실키/서명/배포 사용자. canonical 원장은 Issue #235(이 JSON 은 입력).
- baseline: latest origin/main **9692e1fb**(ls-remote 재확인 · 변화 없음) · main 에 DAY-SPEC-003/004/005 없음 · 000/001 draft → **pending 정직**.
- 원천: v8 알림 = SPEC tree **b1260dd2**(005 확정 0d0ba25f + 003 연결 · products/day tree df5277e8) · v7 채팅 구현/회귀 = git **53adbd49** 그대로.
- target_specs += **DAY-SPEC-005** (003 · 001 · 004 · 000 · 005).
- scope_delta: v7 contract `sha256:00d8e577…0700` · plan_digest `sha256:22f86376…248f`(delivery-v7-approved-result.json 실값) → v8 · 사용자 원문 결속. plan digest 직접 생성 · 승인 대리 0 — 최종 승인은 코디가 Issue 갱신 뒤 사용자에게.
- title: 「… · 직원 내부 채팅 · 원장 호출 알림(v8)」.

## 바뀐 key (v7 → v8 실측)
| key | 개수 | 바뀐 기존 항목 | 추가 |
|---|---|---|---|
| target_delta | 20 → 22 | [4] 원장 호출 발송 「범위 밖」 → v8 구현 · [8] 「배지 그리지 않음」 → v7 까지 기준 + v8 서버 값 | [v8 알림 — 앱] · [v8 알림 — 서버] |
| acceptance | 41 → 53 | A0 완료 정의 v8 누적(v7 진행 중 · 수치 지어내지 않음) · A10 원장 호출 발송 = v8 A47 · A12 backend 재실행 v7·v8 · A13 경로 v7·v8 · A15 「배지 없음 · 누름 없음 · 계정/로그아웃만」 = v7 까지 기준 · v8 뒤 A48/A50 | **A41 ~ A52** |
| non_goals | 15 → 17 | [0] 원장 호출 발송 제외 → 상담사/띄우기만 제외 · [4] board 예외 = 커밋 뒤 훅만 · [6] 알림 설정/목록 제거 → 기기 이름 · 앱 정보 등만 · [8] D-5 → 채팅 중복 집계 · 임시 경로 · 밖 설정 칸 · [11] 알림센터 → Android/FCM/kind 확장 | 새 칸/색인/migration 기본 0 · 새 기기 API/두 번째 APNs 0 |
| review_surface | 21 → 26 | [0] baseline(005 포함 · 원천 b1260dd2 + 53adbd49) · [8] D-5 → SPEC-005 서버 값 · [20] 회귀에 대리/native 수락 · v7 채팅 | v7→v8 의미 · 알림 행 정합 · 격리/읽음 · 공유 푸시 · 동시 구현 경계 |
| implementation_constraints | 11 → 14 | [5] 경계 v7·v8 | 받는 사람/원천 · 커밋 뒤 순서 · v7 푸시 재사용 |
| implementation_starting_points | 5 → 7 | — | v8 서버 · 앱(volatile) |
| ex.code_surface | 10 → 13 | [9] 변경 금지에 board 훅 예외 | v8 서버 · 서버 테스트 · 앱 |
| ex.dependencies | 15 → 17 | [3] D-5 = SPEC-005 · [5] 원장 호출 APNs = v8 | v8 SPEC 원천 · v7 → v8 순서 |
| ex.phases | 15 → 20 | — | 15 ~ 19 |
| ex.verification | 9 → 13 | [0] 「머리 배지 없음」 v7 기준 한정 · [2] 누적 경로 v7·v8 · [4] D-5 dev 실물 | v8 서버 · E2E · 앱 · 경계 |
| ex.rollback | 6 → 8 | 「v1 ~ v6 migration 없음」 → v1 ~ v6 · v8(기본) | v8 기능만 revert · 키 비우기 fail-closed |
| ex.open_questions | 6 → 8 | [0] 종 누름(OQ-A19) v8 해소 | SPEC-005 OQ-N1~N3 기본값 · N4 |
| predeploy · domain_candidates | 무변경 | | |

## 모순 전수 점검 (정규식: 배지 없음 · 배지를 그리지 · 로그아웃만 · 원장 호출 발송 밖/미구현 · 원장 호출 APNs 발송 · 알림센터 · 알림 목록 화면 · D-5 계약 전 · 계약: 없음 · 누름 없음 · app/ 만)
- 남은 출현은 모두 한정됨: A15(v7 까지 기준) · rs[8] · dep[5](v8 구현) · vf[0](v7 기준) · scope_delta(대체 서술) · app/ 만 = v2 ~ v6 역사 기록.
- 받는 사람 정책 · 관리자 추가/호출자 제외 0 · CALL = board.accept · 수락/can*/순서/웹 frontend 무변경 문장 유지.

## SPEC-005 N-A → v8 AC 매핑
N-A1 → A41 · N-A2 → A42 · N-A3 → A43 · N-A4 → A44 · N-A5 → A45 · N-A6 → A46 · N-A7 → A47 · N-A8 → A48 · N-A9 → A49 · N-A10 → A50(+ A15 한정) · N-A11 → A51 · N-A12 → A52.
브리프 검증 항목 매핑: 커밋 뒤 훅 중복/실제 PG 경합 · recall 새 id · 앞 행 유지 = A41 · 권한/비활성/다병원 = A41 · A43 · 다기기 · SSE 도중 세션 죽음 = A46 · ids [] / AND / 모두 읽음 전체 날짜 = A44 · 오늘 KST 50 밖 unread = A43 · setting_not_allowed = A45 · A50 · 키/기기 없음 · skipped_no_key · 호출 성공 보존 = A42 · 재시도 1회 · 죽은 토큰 새 등록 보존 · CALL · hospitalId/env = A47 · A49 · 사라진 방 = A48 · 자정 = A43 · stale 401 = A52 · 시각 근거 = A48.

## 동시 구현 경계
- v7 backend · mobile owner 가 v7 수정 · 검수 · 계약 정합을 닫은 뒤 같은 owner 가 v8 을 이어 구현(같은 app/ · backend/ 동시 두 writer 0) — dep[16] · phase 15 · rs[25].
- code starting points 는 b6c034bf 커밋 + v7 미커밋 구현(read-only 확인: board.py `_finish` :331-337 · call :486 · recall :540 · board_rules doctors :164 · models/misc.py Notification :93 · PushLog :119 · v7 apns/chat_push/devices/tasks/chat.py) = **volatile** · 확정은 v7 owner 보고.
- schema 기본 추가 0 · (호출, 계정) = doctor_call 행 잠금 + 같은 tx 조회 뒤 쓰기 · 유일 색인은 SPEC-000/migration 승인 선행(기본 아님).

## 검증
- JSON parse OK · jsonschema(delivery-request.schema.json + 참조 schema registry) **0 errors** · `DeliveryRequest.model_validate` **OK**(v8 · L3 · target 5) — 각 최종 1회(수정 뒤 재실행 포함).
- SPEC tree `git status` clean(b1260dd2) · 코드 day-app 읽기만(권한 · 설정값 출력 0).
- 미실행: 코드 · 서버 · 앱 · 시뮬레이터 · 실기기 · Issue 갱신 · plan/approval.

## 실제 OQ
- 새 사용자 질문 0. SPEC-005 OQ-N1~N3(기본값) · N4(원문 미확인) 만 승계.

## 다음 (코디)
v8 입력 독립 리뷰 → CLI plan(origin/main · dev 재 fetch) → #235 갱신 → 새 plan_digest 사용자 승인 → v7 owner 마감 뒤 v8 이어 구현.
