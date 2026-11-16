---
type: concept
id: system-bar-inset
title: 시스템 바 inset (edge-to-edge 하단 안전 영역)
aliases:
  - 하단 안전 영역
  - safe area
  - 시스템 바 가림
  - 내비게이션 바 가림
  - 태스크바 가림
  - edge-to-edge
  - viewPadding
  - MediaQuery padding
up:
  - 2026-11-16-android-app
tags:
  - 프론트
  - 모바일
  - Flutter
  - Android
---

# 시스템 바 inset (edge-to-edge 하단 안전 영역)

**앱이 화면 끝까지 그려질 때(edge-to-edge), OS 의 상태 바 · 내비게이션 바 · 태스크바가 덮는 자리만큼 내용을 비워 두는 것.** 비우지 않으면 하단 입력칸 · 목록 끝이 시스템 바 밑에 깔리고, 그 자리 터치는 시스템이 가져간다.

## 정의

- Android 는 targetSdk 35 부터 edge-to-edge 가 **강제**다(끌 수 없음). 앱 창이 시스템 바 밑까지 내려간다.
- 비울 크기는 플랫폼이 inset 으로 알려 준다. Flutter 에서는 `MediaQuery.paddingOf(context).bottom`(키보드가 열리면 0 으로 줄어듦) · `viewPadding`(키보드와 무관) · `viewInsets`(키보드 높이)다.
- **같은 값이어도 뜻이 플랫폼마다 다르다.** iPad 홈 인디케이터는 내용 위에 겹쳐 그려도 되는 자리다. Android 3버튼 내비 · 삼성 태스크바는 내용을 덮고 터치까지 가져간다. 그래서 「iOS 에서 0 으로 둔 자리」가 Android 에서는 버그가 된다.

## 함정

- **Flutter 스크롤 목록에 `padding:` 을 직접 주면 안전 영역이 자동으로 더해지지 않는다.** `BoxScrollView` 는 padding 이 null 일 때만 MediaQuery 안전 영역을 붙인다. `ListView(padding: EdgeInsets.all(16))` 처럼 쓴 목록은 끝까지 내려도 마지막 줄이 바 밑에 남는다.
- 에뮬레이터 기본(제스처 막대)에서는 잘 안 보인다. **3버튼 내비 · 태블릿 폭 태스크바**로 바꿔 봐야 재현된다 — `adb shell cmd overlay enable com.android.internal.systemui.navbar.threebutton`.
- 고칠 자리는 「하단 고정 요소」만이 아니다. **바닥까지 닿는 스크롤 목록 끝**도 센다. DAY android-app 에서 첫 판은 채팅 입력칸만 고쳤다. 리뷰가 판 목록 끝이 잘린 스크린샷을 찾아냈고, 두 번째 판에서 스크롤 목록 25자리를 전수 grep 했다.

## 이렇게 했다 — DAY android-app

- 분기 한 곳: `paneReservesBottomInset = defaultTargetPlatform == android` · `listEndInset = 그 값 ? paddingOf.bottom : 0`. iOS 는 늘 0 이라 iPhone · iPad 화면은 전후 픽셀 동일이었다. 폰 탭 화면은 셸이 padding 을 지워 0 이다.
- 몰입 모드(시스템 바 숨기기)는 쓰지 않았다 — 사용자가 늘 켜 두는 바를 앱이 숨기면 조작이 더 불편하다.
- 시험은 `TargetPlatformVariant{android, iOS}` 로 같은 테스트를 두 번 돈다. `debugDefaultTargetPlatformOverride` 를 `addTearDown` 으로 되돌리면 프레임워크의 debug 변수 검사가 먼저 돌아 실패한다.

## 관련

- [[para/areas/concept/front/viewport-aware-overlay|viewport-aware-overlay]] — 오버레이를 남은 자리 안에 두는 것(같은 「화면 안 영역」 계산)
- [[para/projects/company/day/log/2026-11-16-android-app|android-app 회고]]
