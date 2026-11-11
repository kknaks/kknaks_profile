# 알림 v8 앱 리뷰 W1 — 설정 칸 차례 정정 — task_b332bdb8f78e / ctx_da4a0edaa3f7

- 범위: `notification-mobile-review.md` W1 만 — 설정 탭 차례를 원형(cc-prototype 77173cf8 `screens/settings_screen.dart:97-128`) · DAY-SPEC-005 §2 와이어프레임대로 **계정 → 「알림」 → [로그아웃]**.
- 결과: **정정 완료 · 관련 시험 PASS · PNG 원형 대조 같음**. commit/push/하위위임 0 · backend/spec · 실키 · 서버 · 시뮬레이터 · 실계정 0.

## 변경 경계 · hash(sha256 앞 16자)

| 파일 | 전 | 후 | 변경 |
|---|---|---|---|
| `app/lib/ui/shell.dart` | `42d0cf939524dcc3` | `5dcb1e8853cb50ff` | `SettingsBody._body` 배치만 — [로그아웃] `MsButton`(같은 key · 글자 · variant · color · expand · onPressed)을 계정 카드 안에서 꺼내 「알림」 칸 **뒤**로. 계정 카드(이름 · 병원) · 알림 칸 · 권한 · 동작 · 글자 무변경(새 글자 · 새 디자인 0) |
| `app/test/ui/notification_ui_test.dart` | `06def2d09abcfa19` | `88e1637a8212f1d2` | 시험 2개 추가 — `phone` · `ipad` 「설정 차례 = 계정 → 「알림」 → [로그아웃]」: 위젯 **위치**(계정 `hospital-name` 아래 < 「원장 호출」 위 · 「원장 호출」 아래 < `logout` 위) + [로그아웃] 누를 수 있음. 구현을 복제하지 않음 |

전체 hash = `notification-mobile-evidence/fix/hash-{before,after}.txt`. `test/capture/notification_capture_test.dart` 는 바꾸지 않았다(기존 설정 장면 그대로 다시 찍음).

## 검증(관련만 · 로그 `notification-mobile-evidence/fix/`)

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues |
| `fvm flutter test test/ui/notification_ui_test.dart test/ui/app_flow_test.dart test/ui/chat_ui_test.dart` | **56 passed** · 실패 0(알림 UI 16 + 셸 app_flow · 채팅 셸 회귀 — 설정 로그아웃 · 권한 없는 직원 설정 포함) — `test-related.txt` |
| `DAY_CAPTURE_DIR=… fvm flutter test test/capture/notification_capture_test.dart --plain-name "설정"` | 4 passed(설정 장면 폰/아이패드 × 스위치 · OS 거부+받는 종류 없음) |

전체 277 · native · build 는 브리프대로 다시 돌리지 않았다(셸 설정 배치 Dart 한 곳 · native/의존 변화 0).

## PNG 원형 대조 — `notification-mobile-evidence/fix/`

- `day/`(새 DAY 4장) · `pairs/`(왼쪽 원형 `proto/` 기존 캡처 | 오른쪽 DAY · 같은 viewport 폰 390×844 · 아이패드 1024×1366 · 같은 픽셀 크기)
- `pairs/phone-07-settings.png` · `ipad-07-settings.png` · `phone-08-settings-denied-empty.png` · `ipad-08-settings-denied-empty.png` 직접 열어 확인: 원형 = 계정 → 알림 → (이 기기 · 앱 정보) → [로그아웃] · DAY = 계정 카드 → 알림 → [로그아웃] — **차례 같음**. 남은 차이(의도 · 리뷰 PASS 항목): DAY 계정 카드 모양(SPEC-003 U-16) · 원형 「이 기기」 · 「앱 정보」 칸 없음(SPEC-005 §1 뺌) · DAY 색 · [로그아웃] 버튼 모양은 DAY 기존 회색 외곽선 그대로.

## 미결

- 없음(W1 범위). 리뷰 「참고 1 — KST 고정 시각」은 결함 아님 기록 그대로.
