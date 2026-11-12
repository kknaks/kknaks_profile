# [mobile] 정식 DAY 시뮬레이터 스크린샷 결과 보고

## 상태: done — iPhone 5장 · iPad 5장 · RGB · manifest · README 완료 · 앱 일반 소스 변화 0

- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` · `kknaksss/prod-deploy-re1` · HEAD `5f7806d3`. 커밋 · push · PR · 서명 · ASC 0.
- 코디 시각 검토(msg: 「10장 모두 코디 시각 검토 완료」) 뒤 재촬영 없음. RGB 변환은 픽셀 동일 확인 후에만.

## 수행 — 파일

| 경로 | 무엇 |
|---|---|
| `app/tool/store_capture/main.dart`(새 파일) | 촬영 전용 진입점. 실제 `DayApp` + `test/support` 의 기존 더블(FakeServer · FakeSse · FakeChat · FakeNotify · InterpDouble · FakePushBridge · MemorySessionStore) + 지어낸 fixture. 새 화면을 그리지 않음. `lib/main.dart` 는 이 파일을 import 하지 않음 |
| `app/store/0.1.0/screenshots/iphone/01-board · 02-room · 03-chat · 04-notifications · 05-interpret.png` | 1320×2868 |
| `app/store/0.1.0/screenshots/ipad/` 같은 5장 | 2064×2752 세로 |
| `app/store/0.1.0/screenshots/manifest.sha256.txt` | sha256 · 크기 · 바이트 10줄 |
| `app/store/0.1.0/README.md` | 기준 · 장면 · 데이터 출처 · 출시와 차이 · 재현 |

`git status --short app` = `?? app/store/` · `?? app/tool/store_capture/` 뿐. `git diff --stat -- app` = 빈 결과(기존 추적 파일 변경 0 — lib/ · ios/ · pubspec · test/ 그대로).

## 검증

| 항목 | 결과 |
|---|---|
| `fvm flutter analyze tool/store_capture` | No issues found(2회 — 수정 전후) |
| `fvm flutter build ios --simulator --debug --target=tool/store_capture/main.dart` | ✓ Built(2회 — 첫 빌드는 `_shift` 의 Map 타입 캐스트 버그로 판이 비어 「서버에 연결 중…」 → 진입점만 고쳐 재빌드). 기존 테스트 반복 안 함(앱 동작 변경 없음) |
| 빌드 Info.plist | `day.medisolveai` · `DAY` · 0.1.0 · 1 |
| `Identity.local.xcconfig` | 시작 때 없음 확인 → 빌드마다 한시 생성 → 삭제(현재 없음) |
| 기기 | iPhone 17 Pro Max(4D3C…) · iPad Pro 13-inch (M5)(85C4…) · iOS 26.2. 시작 때 부팅 기기 0 · 두 기기 모두 Shutdown · 우리 앱 미설치 확인 |
| 실제 크기 | `simctl io screenshot` 원본 1320×2868 · 2064×2752 — 리사이즈 없음 |
| 알파 | 원본 RGBA · A 채널 (255,255) → RGB 로 변환 · 픽셀 비교 assert 통과 |
| 메타데이터 | 원본 eXIf = ExifIFD 포인터만(값 없음 · 기기/위치 없음) → 변환 뒤 없음. 청크 IHDR · sRGB · IDAT · IEND |
| 상태 막대 | 9:41 · 배터리 100% 충전 · Wi-Fi(iPhone 셀룰러 4). iPad 날짜 「11월 11일 수요일」은 실제 날짜(덮어쓰기 칸 없음) |
| debug 배너 | 없음(앱 `debugShowCheckedModeBanner: false`). 런타임 = 시뮬레이터 debug(README 기록) |
| 개인정보 | 10장 모두 직접 열어 확인 — 고객 이름 지어낸 이름 · 직원 가간호/나의사 등 · 원장은 직함 · 이메일 · 전화 · 실제 계정 0. 사진은 그린 색 띠(실제 사진 아님) |

## 장면 · 출처

| 장면 | 조작 | 데이터 |
|---|---|---|
| 01 시술 현황 | 첫 화면 | fixture 카드 7장(대기 · 마취 중 · 마취 초과 · 마취 완료 · 전체 호출 · 진행 · 모두 완료) |
| 02 룸 상세 | C-룸2 카드 | 수락 대기 · 진행 · 수락됨 · 호출 · 완료 줄 |
| 03 채팅 | 채팅 → 나의사 | FakeChat · 어제/오늘 메시지 · 사진 1 |
| 04 알림 | 시술현황 목록 → 종 | FakeNotify 3건(안 읽음 2) |
| 05 통역 | A-룸1(TW) → [통역하기] | InterpDouble · ready + 지어낸 자막 4개(한국어 ↔ 중국어 번체) |

제외: 로그인 · 빈 화면 · 예약현황(「곧 출시 예정」). 탭 막대의 「예약현황」 이름은 실제 UI 그대로 보인다.

## 정리

- `orca emulator kill`(두 기기) · 상태 막대 `clear` · 앱 `uninstall`(우리가 설치한 것만 — 시작 때 없었음) · 두 기기 `shutdown`(시작 상태와 같음). 현재 부팅 기기 0 · 헬퍼 0.
- 남은 생성물: `app/build/ios/iphonesimulator/Runner.app`(무시 경로) · `ios/Flutter/Generated.xcconfig`(무시 파일 — 지금 `FLUTTER_TARGET=tool/store_capture/main.dart` · 시뮬레이터 debug 값. **다음 정식 `flutter build ios --release` 가 다시 쓴다** — 정식 빌드에서 `--target` 을 생략하면 기본 `lib/main.dart` 로 돌아옴 · archive 전에 `flutter build ios --config-only` 를 먼저 돌리는 기존 절차면 문제 없음).
- 추가 시뮬레이터 빌드 필요 없음.

## 이슈 · 코디가 확인할 것

1. iPad 오른쪽 아래 곡선 = iPadOS 26 창 크기 조절 손잡이(시스템 UI). 앱 요소 아님 — 그대로 둠.
2. 「만 36세」는 fixture 기본 생일(1990-01-01) 값 — 모든 고객이 같은 나이로 보인다(지어낸 값이라 그대로).
3. 스크린샷은 서버 통합 증거가 아니다(README 명시). 실제 데모 계정 화면과 같을지는 실물 로그인 뒤 확인.
