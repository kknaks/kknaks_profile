# notification-spec 결과 보고 — DAY-SPEC-005 알림 페이지 · 원장 호출 알림/푸시 초안

## 상태: done (SPEC 단계만 · WP · 코드 · GitHub · 커밋 · 하위 위임 없음 · 채팅 구현과 독립 병행)

- 스펙 트리 `day-app-spec` HEAD `53adbd49126c12c887b897854107aa7310cc4f75` 위 미커밋 · 원천 cc-prototype `77173cf8b62f0b27ec54ec4ee22e9d308b7f701e`(`git show` 만) · 코드 day-app read-only(채팅 구현 중 미커밋은 계약으로 쓰지 않음 · 읽기 계약 = 53adbd49 git object)
- 사용자 원문: 「코드 구현 하자 그리고 알림 페이지 스펙 만들어 동시에 할수 잇지 ? 알림, 푸쉬도 일단 로직 다 만드는거지 ?」(notification-decisions-20261110.md)

## 변경 (편집 경계 안)

| 파일 | 변경 |
|---|---|
| `products/day/20-spec/spec-005-notifications.md` | **신규** · `DAY-SPEC-005` · `doc_no DAY-DOC-9` · `status: draft` |
| `products/day/20-spec.md` | SPEC Bundle · SPEC List 각 1행 |
| `products/day/30-work.md` | Spec Coverage 1행(미발주 · 리뷰 뒤 #235 갱신 예정 · proposed) |

- 번호: 현재 트리 · 모든 remote ref · 옆 spec 트리에 spec-005 없음 → 사용 · doc_no = 현행 max DOC-8(SPEC-004) + 1(옆 트리 max DOC-6).
- 동결 확인: `53adbd49` 의 spec-000 · 001 · 002 · 003 · 004 blob 과 작업 트리 파일 hash **5개 모두 같음**(무변경).

## SPEC-005 구성
원천 · DAY 결정 우선 · 정직 표기(테이블만 · API/trigger 없음 · 기기/APNs 는 #235 v7 이 구현 중 → 공유) · 범위(넣음/뺌) · Wireframe(종 · 목록 폰/아이패드 · 설정 칸) · U-1 종 · U-2 목록 · U-3 설정 · U-4 눌러 들어가기 · S-1 ~ S-4 · 범위·격리 · 알림 행 만들기(원장 호출 · 재호출 커밋 뒤) · API 4 + 스트림 · 오류 표 · 실시간 · 원장 호출 푸시 발송(공유) · 케이스 매트릭스 · Flow · Frontend/Backend 규칙 · 프로토와 다른 곳 · 서버 의존 N-1 ~ N-3 · 인수 조건 N-A1 ~ N-A12 · OQ.

## 원형 기능 매핑 (프로토 → SPEC-005)

| 프로토(77173cf8) | SPEC-005 |
|---|---|
| 종 + 안 읽은 수 99+ · 0 숨김 · 접근성 「알림 {n}개 안 읽음」(A/widgets/header.dart:107-137 · :118) | U-1 |
| 다시 읽는 때 — SSE 재연결 · 앞으로 옴 · 탭 뒤(A/app_state.dart:178-199 · 466-476) · SSE `notification {unread}`(:102-108) | U-1 · 실시간 |
| 알림 목록 머리 [‹ 닫기] 「알림」 [모두 읽음] · 폰 전체 / 아이패드 시트 420(notifications_screen.dart:74-81 · shell.dart:321-336) | U-2 · Placement |
| 행 점 · 제목 · HH:MM · 본문 · 안 읽음 바탕 · 빈 「오늘 받은 알림이 없어요」 · 당겨 새로 고침(:89-140) | U-2 |
| 누르면 ids 읽음 → 닫기 → 대상(:59-67) · 모두 읽음(:52-57) · 목록 열린 채 새 알림 다시 읽기(:28) | U-2 |
| 설정 「알림」 칸 · OS 거부 「알림 꺼짐 · 설정에서 켜기」 · 받는 종류 스위치 「원장 호출」 · 「받는 알림이 없어요」(settings_screen.dart:102-117 · model/notification.dart:62) | U-3 |
| 원장 호출 탭 → 시술 현황 그 방 · 푸시 탭만 callId 읽음(app_state.dart:201-226) | U-4 |
| 서버 목록 오늘 · 50 · 새것 위 · unread(service/notifications.py:16-66 · repo.py:391-399) | API #1 |
| 읽음 ids/callId/전부(api/notifications.py:23-25 · repo.py:401-) | API #2 |
| 설정 받는 종류만 · setting_not_allowed(service/notifications.py:18-23 · 70-83) | API #3 · #4 |
| 알림 행 = 발송 1회 × 계정 1 · 기기 없어도 · 설정 끔 = 행/푸시 없음(service/notifications.py:3 · push.py:97-103) | 알림 행 만들기 |
| 원장 호출 본문 「{방} · 시술 N건 · 전체/지정 호출」 · 제목 「원장 호출」 · 고객 정보 없음(push.py:7 · 123-136) | 알림 행 · 푸시 본문 |
| 호출 · 재호출 커밋 뒤 트리거(actions.py:152 · 175 · container.py:126) | 알림 행 「언제」 |
| 재시도 · 죽은 토큰(push.py:28-31 · 284-306) · 키 없음 skipped_no_key | 푸시 발송(#235 v7 공유) |

**옮기지 않은 것(근거)**: 관리자 추가 · 호출한 의사 제외(사용자 2026-11-09) · 상담사 호출(기능 없음 · 새 API 지시 없음) · 띄우기 · 이 기기 이름 · 앱 정보(DAY 범위 밖 · 설정 재설계 없음) · 채팅을 알림 목록에(원천 규칙 그대로 밖).

## 사용자 결정 · 범위 준수
- 받는 사람 = 그 병원 원장 목록 전체(전체 호출) / 지정 원장 · 관리자 추가 · 호출자 제외 없음 · 간호사 대리 수락(DAY-SPEC-003 U-6)과 분리.
- 상담사 호출: `counselor_call` enum 은 있으나 기능 · API 없음 → 받는 종류 · 목록에서 뺌(향후 그 SPEC).
- 받는 종류 = 세션 병원 원장 목록에 있으면 `doctor_call` — 새 권한 키 없음 · 프로토 역할 문자열(admin/doctor/counselor) 대신 DAY 원장 목록.
- `CALL` 수락 카테고리 = `board.accept` edit 세션만(DAY-SPEC-003 U-14) · 들어간 뒤 조작은 서버 `can*`.
- 알림 기록과 APNs 발송 분리(키 없음 = skipped_no_key · 호출 성공 그대로) · 기기 등록 · APNs · 재시도 · 죽은 토큰 · 늦은 세션은 #235 v7 공유 — 중복 기기 API 0.
- 계정 + 세션 병원 격리(목록 · 안 읽은 수 · 스트림 · 푸시 hospitalId) · 로그아웃/401/병원 바꿈 비움.
- Android/FCM · KOS 쓰기 · 실키/Apple/서명/TestFlight/Blob 실설정 없음.

## 모델 대조 — 새 schema 필요 없음
- notification(hospital_id · account_id · kind · doctor_call_id · visit_id · title · body · read_at) · notification_setting(account × kind · is_enabled) · push_log(kind doctor_call · notification_id · status 4값) · device(2026-11-10 개정) 로 충분.
- 참고: notification_setting 에 병원 칸이 없어 설정은 계정 단위(여러 병원 같이) — 프로토와 같아 그대로. (호출, 계정) 중복 방지는 구현 선택(OQ-N3 — 유일 제약을 고르면 그때 migration 1개 필요 · SPEC-000 개정 대상).

## 다른 SPEC 후속 패치 목록 (지금 고치지 않음 — 채팅 구현 중 동결)
- DAY-SPEC-003 U-2 종 bullet: 「D-5 · 배지 그리지 않음」→ DAY-SPEC-005 연결 · OQ-A19(종 누름) → SPEC-005 U-2.
- DAY-SPEC-003 §1 뺌 「알림 목록 화면 · 종 배지 서버 쪽」 · 서버 의존 D-5 → SPEC-005 로 이동 표시.
- DAY-SPEC-003 A-26 「D-5 전 배지 없음」 → SPEC-005 구현 뒤 서버 값 배지.
- DAY-SPEC-003 U-16 설정 탭 「계정 · 로그아웃만」 → 「알림」 칸(SPEC-005 U-3) 추가 문장.
- DAY-SPEC-003 D-2 · U-14 「서버 발송 미구현」 → 원장 호출 발송 = SPEC-005(공유 APNs = SPEC-004/#235 v7).
- DAY-SPEC-002 · SPEC-000: 변경 필요 없음(OQ-N3 에서 유일 제약을 고를 때만 SPEC-000 notification 색인 개정).

## 실제 OQ
- 구현 확인(기본값): OQ-N1 전용 알림 스트림 · OQ-N2 「설정에서 켜기」 글자만 · OQ-N3 중복 방지 방법.
- 원천 확인 불가: OQ-N4 프로토 알림 SPEC 원문.
- 사용자 결정이 필요한 새 질문 없음.

## 검증
- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분)
- `git diff --check` 통과 · `git status` = M `20-spec.md` · M `30-work.md` · ?? `spec-005-notifications.md` — 허용 경계 안
- 53adbd49 대비 spec-000 ~ 004 hash 동일(동결 확인)
- 코드 · 서버 · 기기 실행 0 — 계약 초안이며 완료 주장 없음

## 다음
- 독립 리뷰 → 기존 SPEC PR #921 에 추가 · #235 WP 갱신(v8 입력) → 리뷰 → 코드(같은 PR #237 → dev) · 머지는 사용자 마지막 지시.
