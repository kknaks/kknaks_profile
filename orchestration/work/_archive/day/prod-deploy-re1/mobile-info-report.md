# prod-deploy-re1 A2 — 설정 탭 「정보」 · 개인정보 처리 안내 링크 결과 보고

## 상태: done (캡처 pending · 빌드 안 함)

## 수행
| 파일 | 내용 |
|---|---|
| `app/lib/ui/shell.dart` | `SettingsBody` 맨 아래(로그아웃 버튼 아래 16px)에 `_InfoSection` 추가 — 제목 「정보」(알림 칸과 같은 caption600 · gray600) + 흰 상자 한 줄 「개인정보 처리 안내」 · 오른쪽 `open_in_new` 아이콘. 누르면 `openInfoLink(Uri.parse(privacyPolicyUrl))`. 상수 `privacyPolicyUrl = 'https://day.medisolveai.com/privacy'`(빌드 환경 무관 고정). `openInfoLink` 기본 = 기존 `chat/chat_link.dart` 의 `openChatLink` → `launchUrl(mode: LaunchMode.externalApplication)` = Safari. 시험이 바꿔 끼운다. 클래스 머리 주석 한 줄 갱신. |
| `app/test/ui/app_flow_test.dart` | 시험 1개 추가 + import 1줄 — 「정보」 · 「개인정보 처리 안내」 글자 · 로그아웃보다 아래 · 탭하면 연 주소 = `https://day.medisolveai.com/privacy` 하나. |

- 기존 계정 · 알림 · 로그아웃: 그대로. 예약현황 「곧 출시 예정」: 그대로. 지원 · 버전 등 다른 글자 없음.
- 키: `settings-info` · `privacy-link`.

## 패키지 · iOS 설정
- **새 패키지 없음** — `url_launcher: ^6.3.3` 이 이미 `pubspec.yaml:24` 에 있다(채팅 링크가 씀). `pubspec` · `pubspec.lock` 변경 없음.
- **iOS 설정 변경 없음** — `https` 를 `launchUrl` 로 여는 데는 `LSApplicationQueriesSchemes` 가 필요 없다(그건 `canLaunchUrl` 로 다른 scheme 을 물을 때만). 코드도 `canLaunchUrl` 을 쓰지 않음. `app/ios` 안 건드림.

## 검증
- `flutter analyze lib/ui/shell.dart test/ui/app_flow_test.dart` → **No issues found**
- `flutter test test/ui/app_flow_test.dart test/ui/notification_ui_test.dart test/ui/chat_ui_test.dart` → **83 passed, 0 failed** (새 시험 포함 · 설정 탭을 보는 기존 시험 포함)
- 시뮬레이터 캡처 · 실제 Safari 열림 확인: **pending**(역할 rules 「시뮬레이터 건드리지 않음」 · 빌드는 리뷰 뒤 따로).

## 계약 대조
- 링크 글자 = app-store-preparation.md :251 「DAY 개인정보 처리 안내」 제목 · :347 「개인정보 처리 안내: https://day.medisolveai.com/privacy」 의 「개인정보 처리 안내」 그대로 · 주소 같음.
- 항목 이름 「정보」 = 사용자 글자 그대로. SPEC-003 U-16(설정 탭)에는 아직 없는 항목 — 스펙 반영은 planner 몫.

## 이슈 · 코디가 확인할 것
1. 오른쪽 아이콘(`open_in_new` · 외부로 열림 표시)은 시안에 없음 — 글자는 아님. 빼라면 한 줄.
2. 커밋 안 함. `app/store/` · `app/tool/store_capture/` 안 건드림. 이전 작업 A1 은 다른 쪽이 이미 커밋함(01bbed49) — 지금 워크트리 변경은 A2 두 파일뿐.
