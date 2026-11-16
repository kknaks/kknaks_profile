# 리뷰 리포트 — day-app Delivery #235 v8 입력(원장 호출 알림) / doc (2026-11-10)

- 대상: profile `delivery-request-v8.json` · `notification-wp-report.md`
- 대조:
  - `delivery-request-v7.json` · `delivery-v7-approved-result.json`(contract `00d8e577…` · plan `22f86376…`)
  - 스펙 트리 HEAD `b1260dd2`(clean · products/day tree `df5277e8…`): SPEC-005 N-A1 ~ N-A12 · SPEC-003 알림 연결 · 000/001/004
  - 앞 재검수 PASS(`notification-spec-rereview.md` · `notification-link-spec-rereview.md`)
  - 코드 day-app `b6c034bf` + v7 미커밋 작업 트리(읽기만)
- 방법:
  - JSON 파싱 · 실제 schema · harness 모델 각 1회
  - v7 ↔ v8 경로 diff 77키 전수 읽기 · 옛 범위 문장 grep
  - 코드 출발점 줄 실측
  - 수정 · 하위 위임 없음

## 판정: WARN (FAIL 0 · WARN 1)

결속은 모두 맞다:
- 같은 #235 · `day/day-app` · 7 → **8(정확히 1 증분)** · L3 · target_specs += `DAY-SPEC-005` · baseline `9692e1fb` pending.
- 「main에 003/004/005 없음 · 000/001 draft」로 ready 위조가 없다.
- v8 원천 `b1260dd2`(재검수 PASS 본 · 커밋됨) · v7 채팅 회귀 원천 `53adbd49` 분리 · PR #237 → dev 하나 · 머지 사용자 마지막 · iOS 먼저 · 실키/서명/배포 사용자.

결과 계약은 SPEC-005 원형이다:
- 종 99+/0 숨김 · 목록 폰/420 · 읽음 · 모두 읽음 · 설정 칸 · 알림 SSE · 원장 호출 발송.
- 기존 받는 사람(원장 목록 / 지정 · 관리자 추가 · 호출자 제외 0) · 채팅과 종 분리 · v7 기기/APNs 재사용 그대로다.
- Android/FCM · 상담사 API · 설정 밖 칸 추가가 0이다.

과거 v7 non-goal · AC · verification · rollback 문장도 v7까지 기준으로 거의 모두 한정됐다. WARN 1건은 board backend 무변경 문장 하나가 한정되지 않은 것이다.

## FAIL

없음.

## WARN

### W1. `execution.dependencies[2]`의 「board backend를 고치지 않는다」가 v8 훅 예외와 부딪친다
- 위치: `delivery-request-v8.json` `$.execution.dependencies[2]` 「… 이 Delivery에서 **board backend를 고치거나** 옛 칸 호환 분기를 새로 정하지 않는다(머지 순서는 사용자 · v7 채팅 서버 구현과 별개).」(v7 문장 그대로)
- 근거: v8은 `$.execution.code_surface[10]`에서 `services/board.py` · `routers/api/board.py`(호출 · 재호출 커밋 뒤 훅만)를 바꾼다. 다른 자리는 모두 이 예외로 한정됐다: `code_surface[9]` · `non_goals[4]` · A13 · `implementation_constraints[5]` · `review_surface[21]` · `verification[12]`.
- 영향: 같은 입력 안에서 「board backend 수정 금지」와 「board.py 훅 수정 허용」이 함께 있어 경로 검사 · 리뷰 판정이 갈릴 수 있다.
- 최소 정정: 「board backend 업무 규칙 · 스냅샷 · 응답을 고치거나 옛 칸 호환 분기를 새로 정하지 않는다(v8 예외 = 호출 · 재호출 커밋 뒤 알림 훅 최소 연결)」로 한 구절을 한정한다.

## 실측 결속

| 점검 | 결과 |
|---|---|
| JSON · schema · 모델 | 파싱 OK · `delivery-request.schema.json`(Draft 2020-12 · 같은 폴더 registry) **0 errors** · `DeliveryRequest.model_validate` **OK**(v8 · L3 · target `003/001/004/000/005` · baseline `9692e1fb` · `day/day-app`) |
| 버전 · digest | `delivery-v7-approved-result.json` contract `00d8e577…` · plan `22f86376…` = scope_delta 인용값 · 승인 receipt · 대리 승인 주장 없음 |
| SPEC 원천 | `b1260dd2` = `0d0ba25f` + 003/005 알림 연결(17/17줄 · 앞 링크 재검수 PASS 본) · 작업 트리 clean · `b1260dd2:products/day` tree `df5277e8…`(dependencies[15] 값 일치) |
| 바뀐 키 | v7 대비 77개(신규 A41 ~ A52 · target_delta[20][21] · code_surface[10 ~ 12] · deps[15][16] · phases[15 ~ 19] · verification[9 ~ 12] · rollback 재배열 · OQ[6][7] · NG[15][16] · rs[21 ~ 25] + 기존 한정 정정) |

## 옛 v7 문장 → v8 한정 (grep 전수)

| 옛 내용 | v8 처리 | 결과 |
|---|---|---|
| 알림센터 · 알림 목록 · 설정 알림 non-goal | NG[6] 「계정 · 「알림」 칸 밖 상세(기기 이름 · 앱 정보 등)」 · NG[8] 채팅 중복 집계 · 오늘 밖 기록 · SPEC-005 밖 칸 · 가짜 배지 · NG[11] Android/FCM/kind 확장 | PASS |
| 원장 호출 발송 밖 | NG[0] 상담사 · 띄우기만 제외 · A10 · deps[5] · target_delta[4] 「v8 구현」 | PASS |
| 배지 없음 · 누름 없음 · 계정/로그아웃만 | A15 · target_delta[8] · verification[0] · rs[8] 「v7까지(SPEC-005 구현 전) 기준 · v8 뒤 A48 · A50」 · scope_delta는 대체 서술 | PASS |
| board 수정 금지 | code_surface[9] · NG[4] · A13 · constraints[5] · rs[21] · verification[12] 예외 한정 | **deps[2]만 미한정(W1)** |
| rollback | rollback[0] v8 기능만 revert(종만 · v7 상태 · 알림 행 지우지 않음 · migration 0 · 0006/0007 forward-only 유지) · [1] 키 비우기 fail-closed(skipped_no_key · 행 유지) · v7 채팅 줄 · 데모 이메일 비우기 금지 줄 보존 · [7] 「v1 ~ v6 · v8(기본) migration 없음 · v7 0006/0007」 | PASS |

## 안전 항목 ↔ AC (SPEC-005 N-A ↔ v8)

| N-A | v8 | 확인 |
|---|---|---|
| N-A1 | A41 | 커밋 뒤만 · 원장 목록(활성 · 계정) · 관리자 추가/호출자 제외 0 · 재호출 = 새 call id 새 행 · 앞 행 유지 · (호출 id, 계정) 한 번 = doctor_call 행 잠금 안 조회 뒤 쓰기 · 같은 tx · 새 색인/migration 0 · 실제 PostgreSQL 경합 테스트 |
| N-A2 | A42 | 설정 끔 = 행/푸시/push_log 0 · 기기/권한/키 없음 = 행 · 실시간 유지 · skipped_no_key(기존 4값) · 호출 응답 · 판 신호 · KOS outbox 불변(constraints[12] 순서 = 호출 tx 커밋 → 알림 행 → SSE → APNs task) |
| N-A3 | A43 | 계정 + 세션 병원 · KST 오늘 · 50 · unread 50 밖 포함 · 자정 · 다병원 분리 |
| N-A4 | A44 | ids [] 0건 · AND · 두 칸 없음 = 전체 날짜 · 동시 한 번 · 남의/다른 병원/없는 id 무시 |
| N-A5 | A45 | 원장 목록이면 doctor_call · enabled true 기본 · setting_not_allowed 원문 · 계정 단위 |
| N-A6 | A46 | 새 행 + read > 0일 때만(DAY 적응) · 계정 그 병원 세션만 · Redis 다중 프로세스 · session_expired · 재연결 #1 · chat/board 스트림 무변경 |
| N-A7 | A47 | 세션 병원 = 호출 병원 기기 · CALL = board.accept 세션 · env/hospitalId · 만료 0 · 1회 재시도 · 죽은 토큰(보낸 시점 결속 같을 때만 해제 · 새 등록 보존) · v7 공유(새 기기 API · 두 번째 APNs 0) · 실 APNs/실기기 pending |
| N-A8 | A48 | 종 · 목록 폰/420 · 빈/오류 · 행 탭 ids → 룸 상세 · 카드 없음 원문 · 서버 can* · 프로토 77173cf8 시각 증거 |
| N-A9 | A49 | 푸시 탭 callId · 목록 탭 ids(중복 0) · 다른 병원/환경 무시 · 네이티브 수락 SPEC-003 U-14 회귀 |
| N-A10 | A50 | 설정 「알림」 칸 · OQ-N2 글자만 · 다른 칸 0 |
| N-A11 | A51 | 채팅 종/목록 제외 · 따로 셈 |
| N-A12 | A52 | 로그아웃/401/병원 바꿈 · stale 401 · 시술현황/대리 · 네이티브 수락/통역/로그인/v7 채팅 회귀 · 새 글자 0 |

- 검증 계획: verification[9] 서버 pytest + 스크래치 PG/Redis 경합 · [10] E2E(두 병원 · 다병원 계정 · 원장/비원장 · 활성/비활성 · 여러 기기 · 미실행 pending) · [11] 앱 analyze/test/native/unsigned build + 폰/아이패드 시각 증거 · [12] 경계(board.py는 훅만 · 모델/migration diff 0 · 비밀/로그 본문 0). mock만 완료 금지(A0). v7은 「구현 · 검증 중 · 수치 지어내지 않음」으로 정직하다.
- 실행 경계: deps[16] · phase 15 · rs[25] — v7 owner가 수정 · 검수 · 정합을 닫은 뒤 같은 owner가 v8을 잇는다(같은 경로 두 writer 0). starting_points[5][6]은 「volatile · 확정은 v7 owner 보고」로 표기돼 있고, 인용 줄은 지금 작업 트리에서 실측 일치한다: `board.py:332-336 _finish`(commit → board_changed → outbox kick) · `:486 call` · `:540 recall` · `board_rules.py:164 doctors` · `misc.py:93 Notification` · `:119 PushLog` · `routers/api/board.py:139` · v7 미커밋 `services/{apns,chat_push,devices}.py` · `tasks/chat.py`. 확정 interface라 주장하지 않는다.
- schema: 기본 추가 0(NG[15]) · 유일 색인은 SPEC-000 개정 + migration 승인 선행(OQ[6]) — SPEC-005와 일치.

## 남은 것

- planner: W1(deps[2] 한 구절) → 좁은 재검수.
- 코디: CLI plan(origin/main · origin/dev 재 fetch) → #235 v8 갱신 → 새 plan_digest 사용자 승인 → v7 owner 마감 뒤 v8 이어 구현.
- 코드 · 서버 · 앱 · E2E · 시각 증거 · 실 APNs/실기기는 모두 미실행(pending)이다.
