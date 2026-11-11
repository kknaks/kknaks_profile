# 재검수 리포트 — 채팅 앱 W1 후속(키보드 · 가로 · 긴 글자) / code + 시각 (2026-11-10)

- 대상: `chat-mobile-layout-evidence-report.md` 의 새 변경만 본다.
  - 제품: `app/lib/ui/shell.dart`(키보드 viewInsets) · `app/lib/chat/screens/chat_room_screen.dart`(1:1 머리 Badge `Flexible`).
  - 시험: `app/test/capture/chat_capture_test.dart` `layout()` 그룹.
  - 기존 전체 앱 검수(`chat-mobile-review.md` PASS/WARN1)와 서버 검수는 다시 하지 않았다.
- 원천: SPEC `b0f71ec3` 003/004 · 원형 cc-prototype `77173cf8` `procedure/app/lib/screens/shell.dart`(`git show`, read-only).
- 방식: read-only. app 수정 · 커밋 · 하위 위임 · 시뮬레이터 · 실계정 · 서버 · DB 조작 0.
- 파일 해시: `chat-mobile-layout-rereview-logs/file-hashes.txt` 에 3파일 sha256. 수정 시각은 shell · room 19:19:05, 캡처 시험 19:19:19 이고, 작성자 로그(analyze 19:19:54 · 시험 19:20:05 · build 19:20:51)는 모두 그 뒤다.

## 판정: **PASS (WARN 1)**

## 코드 대조

| 변경 | 원형 / 근거 | 판정 |
|---|---|---|
| 폰: 셸 Scaffold(기본 resize)가 이미 키보드를 뺀 본문에 `mq.removePadding(removeBottom).removeViewInsets(removeBottom)` 를 넘기고, 키보드가 열리면 탭바를 숨김(`shell.dart:248-258`) | 원형 `shell.dart:136-147` 과 **식 · 주석 의도가 같음**. 이식 때 빠졌던 `removeViewInsets` 를 되살린 것 | PASS |
| iPad: `resizeToAvoidBottomInset: false` · 레일은 전체 높이 · 오른쪽 본문만 `Padding(bottom: viewInsets)` + `removeViewInsets`(`shell.dart:225-241`) | 원형 `shell.dart:115-133` 과 같음 | PASS |
| 1:1 머리 역할 Badge 를 `Flexible`(`chat_room_screen.dart:199-201`) | 원형은 Badge 고정 폭(다섯 역할 2–3자). DAY 직무명은 자유 글자(SPEC-004 OQ-C3)라 넘칠 때만 줄인다. 색 · 글자 · 배치 그대로 | PASS |
| 예외 숨김 | `lib/chat` · `shell.dart` 에 `FlutterError.onError` · 디버그 무시 · `e = null` 류 0. `= null` 은 상태 초기화(배너 · 메시지)뿐이다. 시험 `noOverflow` = `takeException() isNull`(예외를 먹지 않고 실패시킴) · `reachable` = hitTestable + 키보드 위 화면 안 | PASS |

셸 변경은 시술현황 탭 시트 · 모달에도 같은 MediaQuery 를 준다. 이전에는 키보드를 두 번 빼던 것이 한 번이 되므로 회귀 방향이 아니다. 시술현황 · 룸 상세 · 통역 · 세션 위젯 시험 115개도 통과했다(아래).

## 직접 실행

| 명령(cd app · FVM) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues · exit 0 |
| `fvm flutter test test/capture/chat_capture_test.dart --plain-name "레이아웃"` | **+5 · 0 fail** |
| `fvm flutter test test/ui test/chat` | **+115 · 0 fail**(셸을 쓰는 시술현황 · 룸 상세 · 통역 · 세션 · 채팅) |

보고만 확인한 것: release unsigned build 20.6MB. 전체 245 · native · 시뮬레이터 빌드는 다시 돌리지 않았다(브리프 지시 · native 변경 0).

「수정 전에는 이 시험이 실패했다」(25px · 16px overflow)는 작성자 보고로만 확인했다. 제품 코드를 되돌려 돌리는 일은 수정 금지라 하지 않았다.

## 직접 연 PNG (`chat-mobile-evidence/layout/` · fixture 렌더 · 실데이터 아님)

| PNG | 확인 |
|---|---|
| `kb-01-chat-input` | 키보드 열림(아래 빈 영역 = 가상 키보드) · 탭바 숨김 · 입력줄이 키보드 바로 위 · 6줄 입력은 5줄 높이 안에서 스크롤 · [+] · [보내기] 보임 |
| `kb-02-message-menu` | 키보드 열린 채 말풍선 메뉴(복사 · 선택 복사 · 공유)가 키보드 위에 다 보임 |
| `land-02-chat` | 가로 844×390 · 머리(‹채팅 · 이름 · 원장 · ⓘ) · 메시지 · 입력줄 · 4탭이 한 화면 |
| `land-long-04-forward` | 가로 전달 시트 · [X] · 「공유」 · [전송] · 검색 보임 · 긴 이름 · 직무 · 그룹 제목 행 전체 표시 · 목록은 시트 안 스크롤 |
| `phone-long-03-direct` | 1:1 머리 「가나다라…」 + 「피부관리 …」 둘 다 말줄임 · ⓘ 유지 · 긴 말풍선 줄바꿈 · 입력줄 · 4탭 |
| `ipad-long-03-direct` | 레일 4메뉴 · 2단(목록 / 대화) · 머리 이름 · 직무 말줄임 · 입력줄 |

## WARN

### W1. iPad 키보드 · 폰 가로 + 키보드를 단언하는 시험이 없다(iPad 셸 분기 코드가 바뀌었는데)

- 위치: `test/capture/chat_capture_test.dart` `layout()` 의 키보드 시험은 `phone`(390×844) 하나뿐이다. 아이패드 · 가로 장면은 키보드가 닫힌 상태다.
- 근거: 이번 수정은 iPad 분기(`shell.dart:225-241` — `resizeToAvoidBottomInset: false` + 본문 Padding)도 바꿨다. 브리프 확인 항목에 「iPad 키보드」가 있다. 작성자 보고 §7 은 아이패드 가로만 범위 밖이라고 적었고, **아이패드 세로 키보드도 증거가 없다**.
  - 폰 가로(390 높이)에서 키보드(약 200pt)가 열리면 머리 + 입력줄이 남는 높이가 가장 빡빡하다. 이 조합도 시험되지 않았다.
- 영향: 코드가 원형 줄과 같아서 결함 가능성은 낮다. 다만 「원형 그대로」 외에 이 앱 화면(2단 · 오른쪽 시트)에서 키보드가 열렸을 때 overflow 0 · 입력줄이 키보드 위에 있다는 실행 증거가 없다.
- 최소 정정(시험만): 같은 그룹에 `ipad` 키보드(viewInsets 예 400)와 `landscape` 키보드(예 200) 장면을 하나씩 더해 `noOverflow` + `reachable(chat-input/send)` 를 단언한다. 제품 코드 변경은 필요 없다.

## 참고 (결함 아님 · 이번 변경 밖)

- 목록 행(폰 · 아이패드)에서는 직무 Badge 가 고정 폭이라, 긴 직무일 때 직원 이름이 「가나다…」 3자까지 줄어든다(`ipad-long-03-direct` 왼쪽 목록). 이름과 직무 중 무엇을 우선할지는 디자인 결정이고, 넘침은 없다.
- 1:1 머리는 이름 · Badge 가 같은 비율(Flexible 1:1)로 줄어든다. 보통 이름(2–4자)은 다 보인다.

## 실기기 · 라이브 pending

- 실제 iOS 키보드 높이 · 예측 막대 · 아이패드 하드웨어 · 분할 키보드 · 회전 중 키보드는 위젯 viewInsets 고정값으로 대신했다(실기기 미확인).
- 로컬 11040 채팅 API 실물 · 실계정 대화는 미실행이다(이전 보고와 같음).
