# 최종 재검수 — 알림 v8 WARN 2건 최소 정정 (2026-11-10)

- 범위: 서버 리뷰 W1(`backend/tests/day/chat/test_devices_push.py` 단언 범위)과 앱 리뷰 W1(`app/lib/ui/shell.dart` 설정 차례 + `app/test/ui/notification_ui_test.dart` 새 단언 2개)만 본다. 새 범위는 추가하지 않았다.
- 방식: read-only. 제품 · 시험 수정 · 커밋 · push · 하위 위임 · 실키 · 시뮬레이터 · 서버 조작 0.
- 기준: 서버는 커밋 `39a3dad8`(코디 커밋 · push 전), 앱은 미커밋 작업 트리.

## 판정: **PASS — WARN 2건 모두 해소 · 정정으로 인한 회귀 0**

## 파일 해시 (sha256 · 작성자 보고와 일치)

| 파일 | sha256 |
|---|---|
| `backend/tests/day/chat/test_devices_push.py` | `2a262e63b46a6444c6482769d9aede842f44b87cb72c338f9f1a92ab60988163`(= `39a3dad8` 커밋본 · 작업 트리 dirty 0) |
| `app/lib/ui/shell.dart` | `5dcb1e8853cb50ff8c9bb50b527e8b91d87ffeac30f6eb8b1e22c00a28c2f120` |
| `app/test/ui/notification_ui_test.dart` | `88e1637a8212f1d2e742571bfda607b69dea5033da4ac6e5a72f4d8a08afd870` |

## 서버 W1 — 해소

- diff(`git show 39a3dad8 -- …test_devices_push.py` 의 :277 한 hunk): `select(Notification)`(테이블 전체) → `select(Notification).where(Notification.hospital_id.in_([world.a, world.b]))` + 주석 2줄.
- `world.a` · `world.b` 는 그 시험이 새로 만드는 두 병원이다(`tests/day/chat/conftest.py:54-57`). 단언 강도(`== []`)는 그대로이고, 대상만 그 시험 범위로 좁혔다. 시험을 약하게 하거나 지운 것이 아니다.
- 이 파일 밖의 서버 diff 는 0이다(제품 변경 0).
- **직접 재현**: 지난 검수에서 실패했던 역순 `scripts/test.sh -q backend/tests/day/notifications backend/tests/day/chat/test_devices_push.py` → **32 passed** · 8.6s(`notification-final-rereview-logs/reverse-order.txt` · day_test · Redis db15 · env 값 출력 0 · 실행 전 다른 pytest 없음).

## 앱 W1 — 해소

- `shell.dart:398-431` `SettingsBody._body` 의 차례가 계정 카드(이름 · 병원) → `SizedBox(16)` → `NotificationSettingsSection` → [로그아웃] 으로 바뀌었다.
  - [로그아웃] 은 계정 카드 밖으로 옮겨졌고, key `logout` · 글자 · `outlined` · `gray` · `expand` · `onPressed`(`loggingOut` 이면 꺼짐)는 그대로다.
  - 알림 칸의 조건부 표시(`notify` · `osDenied` · `toasts` 셋 다 있을 때)도 그대로다. 새 글자 · 동작 0.
- 원형 `settings_screen.dart:97-128` 과 SPEC-005 §2 차례(계정 → 알림 → … → 로그아웃)와 같다.
- 새 시험 `notification_ui_test.dart:250-260`(phone · ipad 2개)은 화면에서의 **실제 위치**로 확인한다.
  - `hospital-name` 의 아래쪽 < 「원장 호출」 의 위쪽, 「원장 호출」 의 아래쪽 < `logout` 의 위쪽.
  - [로그아웃] 을 누를 수 있다(hitTestable).
  - 구현을 복제한 단언이 아니다.

## 직접 실행 (cd app · FVM)

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues · exit 0 |
| `fvm flutter test test/ui/notification_ui_test.dart test/ui/app_flow_test.dart` | **+47 · 0 fail**(새 차례 단언 phone/ipad · 설정 탭 로그아웃 흐름 · 권한 없는 직원 설정 포함) |

## PNG 직접 확인 (`notification-mobile-evidence/fix/pairs/` · 왼쪽 원형 | 오른쪽 DAY · fixture)

- `phone-07-settings`: DAY = 계정 카드(직원 · 데모 병원) → 「알림」 원장 호출 스위치 → [로그아웃]. 원형은 계정 → 알림 → 이 기기 · 앱 정보 → [로그아웃] 이다. 남은 차이는 SPEC 이 뺀 칸뿐이므로 **차례는 같다**.
- `ipad-08-settings-denied-empty`: DAY = 계정 → 「알림 꺼짐 · 설정에서 켜기」 + 「받는 알림이 없어요」 → [로그아웃]. 차례가 같고 4메뉴 레일도 그대로다.
- 차이는 의도된 것이다(지난 리뷰 PASS 항목): DAY 계정 카드 모양 · DAY 색 · 회색 외곽선 [로그아웃] · 「이 기기」 · 「앱 정보」 칸 없음.

## 미실행 (정직)

- 전체 서버 787 · 앱 277 · native · build · 실제 Apple/APNs 키 · 시뮬레이터 · 실계정은 다시 돌리지 않았다(브리프 지시 · 제품 변경은 Dart 배치 한 곳).
- 캡처 PNG 는 작성자가 재촬영한 것을 열어 보기만 했고, 캡처 시험을 다시 돌리지 않았다.
