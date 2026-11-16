# [mobile] DAY 알림 v8 앱 구현
작업 tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, branch kknaksss/day-app, 시작 head 3aaa97806684b8cea7f7fb777adbcdcff7ae0de6. 루트 AGENTS.md 및 연결된 규칙, profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/의 해당 역할 문서를 먼저 읽어라. 새 맥락이므로 아래 원천·앞 보고를 먼저 읽는다.
승인 = delivery-v8-plan-approval.json + delivery-v8-approved-result.json(plan-approved·execution ready), 사용자 「응 진행하고 구현하는동안 우리 ios 개발용 푸쉬 알림 받을까 ?」. request는 delivery-request-v8-execution.json(원 delivery-request-v8.json의 계약/digest 완전동일·완료된 과거 실행기록만 정리). 알림 WP 독립 재검수 PASS = chat-permission-spec-wp-rereview.md. 문서 원천 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec exact b0f71ec312548a8dd60c70e51ac68374b84fb906 products/day/20-spec/spec-005-notifications.md 전문, adjacent003/004/000/001. main9692e1fb에는 새SPEC미머지라 baseline pending, 사용자 마지막merge지시로 선merge 요구0. latest fetched code dev91728737, code tree clean. v7채팅 검수/정정/커밋완료, 앞으로 v8만 변경.
프로토 read-only /Users/kknaks/git/toy_pr2/cc-prototype git show 77173cf8b62f0b27ec54ec4ee22e9d308b7f701e:procedure/app 및 back. checkout/pull/원본편집0. 원천화면·문구 유지, DAY결정이 우선. commit/push/PR/merge/하위위임0. 실키/Apple계정/서명/실env/서버재시작·migrate·seed·실계정조작0. profile 보고/증거만 쓴다. 다른 writer영역 dirty 정리/stage/reset0. 기존채팅·로그인·시술현황·통역 회귀0.

읽을 앞 산출: chat-mobile-review.md / chat-mobile-layout-evidence-report.md / chat-mobile-layout-rereview.md / chat-mobile-keyboard-matrix-report.md, notification-spec 최종리뷰/링크스펙리뷰 및 research-chat-notifications.md. 네 소유 app/만. backend·스펙·루트설정파일0. 서버writer가 backend만 병렬작업한다. 실제서버API는현재11040에서아직없음, mock계약과fixture로앱구현가능. 백엔드응답추측금지·SPEC005 §3 고정,차이즉시질문.
원형 procedure/app/lib/widgets/header.dart·screens/notifications_screen.dart·settings_screen.dart·shell.dart·model/notification.dart·app_state.dart/push를 gitshow read-only로 대조한다. 기존DAY4메뉴/색/시술현황디자인/통역/채팅 유지. 종은모든탭공통 서버unread·99+·0숨김·원문접근성. 폰은알림전체화면(하단메뉴위)/iPad오른쪽420시트. 머리닫기·정가운데알림·모두읽음활성조건·행점/시간/본문/읽음배경·원형빈글자·당겨새로고침. 행tap ids읽음 후 닫고서버현황상세,푸시tap만callId읽음(중복0)·카드없음 기존토스트. 설정계정아래알림칸만추가: 서버kind 스위치·OS권한꺼짐원문·빈종류원문·setting_not_allowed복원. 새고안문구/기기명/앱정보/OS설정링크0.
새 notification controller/API/model/전용SSE(기존패턴재사용·board/chat권한과독립)를구현. unread서버값만·로그인/앞전환/재연결/읽음/원장푸시수신때맞춤·목록열린동안unread변화시재조회. 끊김노란줄없음·현재배지유지. no-board직원도기존셸/채팅/알림목록/설정가능, 상세/수락은서버/me권한판단. 401/로그아웃/병원전환종0·목록/stream/cache정리,늦은전세션HTTP/SSE/push가새세션읽음/배지/화면/토스트를바꾸지않음. kindchat은종알림함에합산0. 원장푸시env/hospitalguard·native CALL본인수락·Keychain·기기등록경합보존. OS푸시권한상태는기존등록상태재사용·실제키/Bundle ID확정값하드코딩0.
검증 analyze·추가unit/widget/contract·필요native·unsignedios. 회귀는 변경범위와기존셸/시술현황/통역/채팅·세션포함최종한번. 원형과같은viewport 폰390x844/iPad1024x1366(글자배율도동일)알림목록/0/99+/읽음/빈목록/설정스위치/OS거부/전체화면·오른쪽420 캡처하고PNG직접비교. 가로/긴본문·제목/스크롤/키보드·늦은응답/스위치실패·부재카드·복수병원푸시거절검증. 예외숨김0. 사용자의orca-mobile-iphone PID70352 로그인 세션/업무데이터/route 조작금지. 이번에는테스트fixture·unsignedbuild만, 실서버활성화·재설치/조작필요하면코디질문.
산출 notification-mobile-code-report.md 및 notification-mobile-evidence/: 파일hash·원형매핑/시각PNG·명령수치·서버계약정합·실키/실기기/실송수신pending·사용자후속. 새 preamble IDs로 outcome succeeded/failed 및 실제 report-path를 붙여 worker_done1회 후 idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_e8a8842c-a789-4862-93a5-7886d6bd1c61 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

