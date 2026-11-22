# day-mobile-v2 M5 결과 보고 — 통역 재생 중 안내 줄 지우기

## 상태: done (커밋 없음)

base = `dba35bbd`. 사용자 결정(2026-11-20): 재생 중 안내 「번역 음성이 나오는 동안은 듣지 않아요」를 지운다 · 새 글자 없음 · 「번역 읽는 중」 그대로 · 대리 수락 창 「호출할 시술 · N개」 그대로.

## 수행
| 파일 | 변경 |
|---|---|
| `app/lib/ui/interpret_widgets.dart` `_micRow` | 재생 중 안내 줄 = 없음(`hint` null) → 안내 Text 와 그 위 2px 간격을 그리지 않음. 상태 한 줄(「번역 읽는 중」)이 원 옆 가운데에 놓임(Row 세로 가운데 — 캡처로 확인). 듣는 중 · 멈춤 · 연결 중 · 연결 안 됨 안내 줄은 그대로 · 안내 Text 에 key `drawer-hint`(시험용) |
| `app/test/ui/interpret_hint_test.dart`(새) | 실제 앱 트리 + 목 WS: 듣는 중 = 안내 있음 → `audio_start` + PCM = 「번역 읽는 중」 · 안내 없음 · 「듣지 않아요」 글자 없음 → `audio_stop` 뒤 멈춤 = 안내 있음 |

대리 수락 창(`ui/doctor_picker.dart:433`) 무수정.

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+416 ~81 All tests passed**(새 1) |
| `fvm flutter build ios --no-codesign` | ✓ `Runner.app` (20.8MB) |
| 캡처 `DAY_CAPTURE_DIR=… flutter test test/capture/m4_capture_test.dart` | 2/2 — `m4-{phone,ipad}-drawer-playing.png` 다시 찍음(안내 줄 없음 · 상태 한 줄 가운데) · 같은 실행에서 listening · paused 도 다시 찍힘(변화 없음) |
