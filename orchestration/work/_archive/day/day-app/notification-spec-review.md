# 리뷰 리포트 — day-app 알림 SPEC(DAY-SPEC-005 신규 · index/coverage) / doc (2026-11-10)

- 대상: 스펙 트리 `53adbd49` 위 미커밋 — ?? `spec-005-notifications.md`(355줄 · `DAY-DOC-9` · draft) · M `20-spec.md`(Bundle · List 각 1행) · M `30-work.md`(Coverage 1행)
- 원천:
  - `notification-decisions-20261110.md`(사용자 「코드 구현 하자 그리고 알림 페이지 스펙 만들어 동시에 할수 잇지 ? 알림, 푸쉬도 일단 로직 다 만드는거지 ?」)
  - `notification-spec-brief.md` · `notification-spec-report.md`
  - 프로토 `77173cf8` `git show`: `service/notifications.py` · `api/notifications.py` · `repository/repo.py:388-420` · `service/push.py:95-136` · 앱 `notifications_screen.dart` · `settings_screen.dart` · `model/notification.dart`
  - DAY 코드 `backend/day/models/misc.py` · `enums/misc.py`(읽기만)
- 방법:
  - 동결 blob 대조 · 원천 줄 대조 · 모델 대조
  - lint 1회 · `git diff --check`
  - 수정 · 하위 위임 없음

## 판정: WARN (FAIL 0 · WARN 2)

- **동결 확인**: `53adbd49`의 spec-000 · 001 · 002 · 003 · 004 blob과 작업 트리 파일 hash가 **5개 모두 같다**. 편집은 허용 3경로뿐이다.
- **사용자 · 기존 결정 우선**: 원장 호출 받는 사람 = 그 병원 원장 목록 전체 / 지정 원장이다. 프로토의 관리자 추가 · 호출한 의사 제외(B/`service/push.py:117-121`)는 옮기지 않았다. 간호사 대리 수락은 받는 사람과 분리했다.
- **채팅 분리**: 채팅 push · 탭 배지는 종 · 알림함과 따로다.
- **범위 차단**: 상담사 호출 API · Android/FCM · 운영 설정 · 머지는 없다.
- **기기 · APNs 재사용**: 기기 등록 · APNs · 재시도 · 죽은 토큰 · 늦은 세션 보존은 #235 v7 공유로, 중복 API는 0이다.
- **기록과 발송 분리**: 키 없음 `skipped_no_key`와 호출 조작 · 알림 행 저장 성공을 분리했다.
- **원형 대응**: 폰 전체 화면 · 아이패드 420 시트 · 종 99+/0 숨김 · 목록 · 모두 읽음 · 한 건 읽음 · 설정 스위치 · OS 권한 안내가 원문 글자와 맞다.
- **정직 표기**: 서버는 지금 테이블만 있고, 계약은 제안이다.

WARN 2건은 중복 방지와 migration 문장의 모순, 읽음 API 경계(빈 `ids` · 읽음 뒤 실시간)의 원천 차이 미표기다.

## FAIL

없음.

## WARN

### W1. 「(호출, 계정) 하나」 보장과 「migration 필요 없다」가 같이 단정돼 있다
- 위치: `spec-005-notifications.md:185` 「중복 — 같은 호출 id로 두 번 만들지 않는다(재시도 · 중복 실행에도 (호출 id, 계정) 하나) — 방법은 구현」 · `:282` 「기존 테이블로 충분하다 — 새 칸 · 새 테이블 · migration이 필요 없다」 · `:341` OQ-N3 「(호출, 계정) 유일 제약 vs 조회 뒤 쓰기」 · N-A1 「같은 호출 중복 실행에도 (호출, 계정) 하나」
- 근거: DAY `Notification`(misc.py)에는 `doctor_call_id`가 있지만 `(doctor_call_id, account_id)` 유일 색인이 없다(SPEC-000 :982 · 모델 실측). 프로토도 중복 방지가 없다(`repo.py add_notification` = 그냥 insert). planner 보고도 「유일 제약을 고르면 migration 1개 · SPEC-000 개정 대상」이라 적었다.
- 영향: 커밋 뒤 훅의 재시도 · 동시 실행에서 「조회 뒤 쓰기」만으로는 경합이 남는다. 보장하려면 잠금(같은 tx · 호출 단위 advisory/row lock)이나 유일 색인이 필요한데, `:282`가 migration 길을 미리 닫아 OQ-N3과 부딪친다. 동결된 SPEC-000을 건드려야 하는 선택지인지도 SPEC 본문에서 보이지 않는다.
- 최소 정정(새 정책 아님): `:282`를 다음처럼 고치고 OQ-N3 기본값도 같은 문장으로 맞춘다.
  - 「기본 = 기존 테이블 · migration 없이 호출 단위 잠금 안 조회 뒤 쓰기」
  - 「유일 색인을 고르면 SPEC-000 `notification` 색인 개정 + migration이 먼저(SPEC-000 동결 해제 뒤 후속)」

### W2. 읽음 API 경계 두 가지가 원천과 다르거나 비어 있는데 「프로토와 다른 곳」에 없다
- 위치: `:198` API #2 「`ids` · `callId` 둘 다 없으면 **모두 읽음**」 · `:218` 실시간 「새 알림 행이 생긴 뒤 · **읽음 · 모두 읽음 뒤**(다른 기기 맞춤) 보낸다」 · `:292-304` 프로토와 다른 곳 표
- 근거:
  - 프로토 `repo.py mark_read`는 `ids is not None`이면 `id IN (...)`이고, 빈 배열이면 `IN (NULL)`이라 **0건**이다. 모두 읽음은 `ids` · `callId`가 **아예 없을 때만**이다. SPEC 문장은 `ids: []`(빈 배열)를 「없음」으로 읽어 **전부 읽음**으로 구현될 여지가 있다(클라이언트 버그 한 번에 알림 전체가 읽힘).
  - 프로토 `service/notifications.py:45-52` `announce`는 **새 행 생성 때만** SSE를 보내고, `read`(:66-69)는 보내지 않는다. 「읽음 뒤 다른 기기 맞춤」은 DAY 추가 동작인데 차이 표에 없다.
- 영향: 빈 `ids` 해석에 따라 데이터 의미가 달라진다(검증 불가). 원천에 없는 SSE 이벤트가 근거 없이 계약에 들어간다(N-A4 · N-A6 판정이 흔들림).
- 최소 정정:
  - #2에 「`ids: []` = 0건(모두 읽음은 `ids` · `callId` 둘 다 칸이 없을 때만 — 프로토 `repo.py mark_read`)」을 한 구절 넣는다.
  - 읽음 뒤 SSE는 다른 기기 종 맞춤을 위한 DAY 적응이라고 차이 표에 한 줄 적는다. 원천대로 빼고 앱이 앞으로 올 때 · 재연결 때 다시 읽기로 맞출 수도 있다. 둘 중 하나를 기본값으로 둔다.

## 원천 · 계약 대조 (실측)

| 항목 | 결과 |
|---|---|
| 목록 | 오늘(KST) · 50(`LIST_MAX`) · `created_at` 내림 · id 내림 · `unread` = 오늘 안 읽은 수 — `service/notifications.py:17 · 32-33 · 54-64` · `repo.py notifications/unread_count`와 일치. DAY는 + 세션 병원 범위(차이 표 「범위 계정 + 세션 병원」) |
| 읽음 | `ids` · `callId` · 전부 · 안 읽은 것만 · `read` = 바꾼 수 — `repo.py mark_read`와 일치(W2 빈 배열 · SSE만 예외) |
| 설정 | 저장 없으면 `true` · 받는 종류만 · `setting_not_allowed` 「이 계정이 받지 않는 알림이에요」 — `:37-38 · 72-81` 일치. 프로토 역할 표(admin · doctor = doctor_call) 대신 「원장 목록이면 doctor_call」 — DAY 받는 사람 정책(관리자 추가 없음)과 맞춘 것으로 차이 표에 있음 |
| 알림 행 | 설정 켠 계정마다 1행 · 끈 계정은 행 · 발송 없음 · 기기 없어도 행 — `push.py:97-103` 일치. 제목 「원장 호출」 · 본문 「{방} · 시술 {N}건 · 전체 호출/지정 호출」(방 없으면 「방」) — `:123-124` 일치 |
| 푸시 | `aps.alert` · `sound default` · `kind doctor_call` · `visitId` · `callId` + DAY `environment` · `hospitalId` · `CALL` = `board.accept` edit 세션만(프로토 「의사만」 `:131` 대신 — DAY-SPEC-003 U-14) · 만료 0 · 재시도 · 죽은 토큰 · `skipped_no_key` = v7 A36 공유 |
| 화면 글자 | 「닫기」 · 「알림」 · 「모두 읽음」(안 읽음 없으면 회색) · 「오늘 받은 알림이 없어요」 · 「알림 꺼짐 · 설정에서 켜기」(빨강) · 「알림 설정」 · 「받는 알림이 없어요」 · 「원장 호출」(`notifKindName`) — 원문 일치 · 새 글자 없음 |
| DAY 모델 | `Notification`(hospital_id · account_id · kind · doctor_call_id · visit_id · title · body · read_at) · `NotificationSetting`(PK account_id × kind · is_enabled) · `NotificationKind` = doctor_call · counselor_call · `PushStatus` 4값 — SPEC 계약에 충분(W1 중복 방지 수단만 예외) · 숨은 schema 변경 없음 |
| 격리 · 세션 | 목록 · 수 · 스트림 · 푸시 = 계정 + 세션 병원 · 다른 병원 세션 기기 · 스트림 제외 · 로그아웃 · 401 · 병원 바꿈 비움 · 늦은 응답 버림 · 푸시 `hospitalId` 다르면 무시 |
| 알림 tap | 카드 없음 = 「호출이 끝났거나 방이 비었어요」 · 이미 수락/닫힘 = 지금 상태 · 버튼은 서버 `can*` · 네이티브 수락은 DAY-SPEC-003 U-14(서버가 판정) — 알림이 권한을 만들지 않음 |
| 재호출 · 상태 변화 | 재호출 = 새 호출 → 새 대상에 새 행 · 앞 행 그대로 · 부분 수락/닫힘/귀가 대기에도 행 무변경 · 비활성/멤버십 소실 = 새 행 없음 |
| 인수 조건 | N-A1 ~ N-A12 서버 더블 · 로컬 스크래치 · 시뮬레이터 · 실기기(N-3 사용자 키) 구분 — 각 검증 가능(W1 · W2 정정 뒤) · 실키/실기기는 pending 정직 |
| OQ | OQ-N1 · N2 · N3 구현 확인 · N4 원천 확인 불가 — 새 사용자 질문을 만들지 않았다 |

## 참고 (결함 아님)

1. **동결된 SPEC-003과의 순서**: SPEC-003 A-26 「D-5 전 배지 없음 · 임시 경로 요청 0건」 · U-2 종 「누르는 동작 없음」 · U-16 「계정 · 로그아웃만」 · D-2 「발송 미구현」은 SPEC-005 구현과 충돌한다. SPEC-005 `:353-355` 후속 패치 목록에 정확히 있다. WP(#235 v8)에서 「SPEC-003 연결 패치 → 리뷰」를 알림 **코드 착수 전 선행 조건**으로 두면 된다.
2. 「모두 읽음」의 날짜 범위: 프로토 `mark_read`는 날짜 조건 없이 안 읽은 전체를 읽는다(목록 · 수는 오늘만). SPEC 「내 안 읽은 행」도 같은 뜻으로 읽힌다(세션 병원 범위 추가). 구현 때 「오늘만」으로 좁히지 않도록 확인하면 된다.
3. `doc_no DAY-DOC-9` — 다른 경로 · remote ref에 중복이 없다(grep 0). 머지 때 재확인한다.
4. 받는 계정 = `doctors[]`와 같은 원장(활성 · 계정 있음) — DAY `board_rules.doctors()`는 `is_doctor`로 거른다. 활성 · 계정 조건은 구현이 받는 사람 계산에서 함께 걸러야 한다(SPEC 문장 그대로 구현하면 됨).

## 검증 (실결과)

- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분)
- `git diff --check` → 출력 없음 · exit 0
- 경계: `git status` = M `20-spec.md` · M `30-work.md` · ?? `spec-005-notifications.md` · spec-000 ~ 004 blob = `53adbd49`와 동일(5/5)

## 남은 것

- planner: W1(`:282` · OQ-N3 문장) · W2(#2 빈 `ids` · 읽음 뒤 SSE 차이 표기) 최소 정정 → 재검수.
- 그 뒤: SPEC-003 연결 패치(동결 해제 뒤) · #235 WP v8 입력 · 리뷰 → 알림 코드(같은 PR #237). 실키 · Apple · 실기기 수신은 사용자 설정 뒤 pending.
