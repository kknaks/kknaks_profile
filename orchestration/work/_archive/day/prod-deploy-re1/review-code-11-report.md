# 리뷰 리포트 — prod-deploy-re1 / code 11 · 설정 「정보」 링크 A2 (2026-11-12)

대상: 워크트리 미커밋 `app/lib/ui/shell.dart`(+45 −1) · `app/test/ui/app_flow_test.dart`(+21). `app/store/` · `app/tool/store_capture/` 는 범위 밖이라 보지 않았다.

근거:
- mobile-info-report.md
- 스펙 워크트리 미커밋 SPEC-003 개정 ⑫(`spec-003-mobile-app.md:59` · `:443` · `:228` · `:785`)
- 사용자 결정 「정보」 → 「개인정보 처리 안내」 · `https://day.medisolveai.com/privacy` · 외부 브라우저

## 판정: PASS

FAIL 0 · WARN 0 · 참고 3.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `flutter analyze`(app 전체 · fvm 3.44.8) | No issues found |
| `flutter test test/ui/app_flow_test.dart test/ui/notification_ui_test.dart test/ui/chat_ui_test.dart` | **83 passed** (모두 통과) |

실기기 · 시뮬레이터에서 Safari 로 열리는지는 확인하지 않았다(빌드 안 함 · 앱 세션 몫 · mobile-info-report pending 그대로).

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| 무엇으로 여나 · 외부 브라우저 | PASS | `shell.dart:474` `openInfoLink` 기본 = `openChatLink`(`chat/chat_link.dart:9-11`) = `launchUrl(u, mode: LaunchMode.externalApplication)`. 기기 기본 브라우저(iOS Safari)로 나가고, 앱 안 웹뷰(`inAppBrowserView`)가 아니다. 이미 채팅 링크가 실기기에서 쓰는 같은 함수다. `url_launcher: ^6.3.3` 은 이미 `pubspec.yaml:24` 에 있고, `pubspec.yaml` · `pubspec.lock` · `app/ios` diff 는 없다. 새 패키지가 없다. `https` 를 `launchUrl` 로 여는 데는 `LSApplicationQueriesSchemes` 가 필요 없다(`canLaunchUrl` 을 쓰지 않음) |
| 실패 시 동작 | PASS(+참고 1) | `launchUrl` 이 false 를 돌려주거나 `PlatformException` 을 던지면 값을 보지 않는다. 그래서 화면에 아무 일도 없고 앱은 멈추지 않는다(`onTap` 의 async 예외는 Flutter 오류 로그로만 간다). 채팅 링크와 같은 동작이다. 실패 안내 문구는 결정에 없으므로 넣지 않은 것이 맞다 |
| 글자 · 주소 = 결정 | PASS | 제목 `_infoTitle = '정보'`(사용자 글자) · 링크 `_privacyLabel = '개인정보 처리 안내'`(60-release §6-1 승인 문안 제목) · `privacyPolicyUrl = 'https://day.medisolveai.com/privacy'`(빌드 env 와 무관하게 고정 · 공개 페이지라 맞다). 스펙 :443 과 같다. 그 밖에 보이는 새 글자는 없다(지원 · 버전 없음). `open_in_new` 아이콘은 글자가 아니다(참고 2) |
| 기존 설정 항목 그대로 | PASS | diff 는 `SettingsBody` 끝에 `SizedBox(16)` + `_InfoSection()` 을 더한 것과 클래스 주석 한 줄뿐이다. 계정 · 알림 · 로그아웃 줄과 동작은 바뀌지 않았다. 기존 설정 탭 시험(로그아웃 A-27 · 알림 칸)이 통과한다 |
| 범위 밖 변경 없음 | PASS | `git status` = 두 파일(+ 범위 밖 untracked 둘). 예약현황 「곧 출시 예정」 · 채팅 링크 동작은 바뀌지 않았다. `openInfoLink` 는 부를 때 `openChatLink` 를 읽으므로 채팅 쪽에 영향이 없다 |
| 시험 | PASS | 새 시험(`app_flow_test.dart:647-666`)은 설정 탭으로 들어가 「정보」 · 「개인정보 처리 안내」 글자가 `settings-info` 안에 있는지 확인한다. 로그아웃보다 아래인지(rect), 탭하면 연 주소가 정확히 `[https://day.medisolveai.com/privacy]` 하나인지도 확인한다. opener 는 `addTearDown` 으로 되돌린다. 문자열 리터럴로 단언하므로 상수가 바뀌어도 잡는다 |

## 참고

- 참고 1(검증 공백): 시험은 opener 를 바꿔 끼우므로 `LaunchMode.externalApplication` 자체는 시험이 보지 않는다. 그 줄은 기존 `chat_link.dart` 그대로이고 채팅에서 실기기로 쓰고 있다. 그래도 이 화면에서 Safari 로 열리는지는 빌드 뒤 실기기 한 번으로 닫아야 한다(심사 요건 60-release §7-2 #6 의 근거가 될 캡처와 함께).
- 참고 2: 오른쪽 `Icons.open_in_new_rounded` 는 시안 · 스펙에 없는 표시다. 스펙 :443 은 「칸 모양은 정하지 않았다 — 구현 때 · 리뷰 눈 확인」이라 어긋남은 아니다. 코디나 사용자가 눈으로 확인하면 된다.
- 참고 3: 실패하면 아무 안내가 없다(참고 1의 실패 경로). 공개 https 페이지라 실제로 실패할 일은 드물다. 결정에 문구가 없으므로 지금은 맞다.
