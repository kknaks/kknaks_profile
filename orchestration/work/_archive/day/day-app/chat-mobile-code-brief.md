# [mobile] DAY 내부 채팅 앱 구현

이 문서는 review된 WPv7 CLI결속 뒤에만 발주한다. 발주포인터의 최종 WP/승인결과 파일을 읽고 exact계약 우선. 하위워커/subagent위임·commit/push/PR/merge0.
코드 tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, 착수전 branch/status확인. 루트AGENTS 앱규칙·docs개발지침과 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/mobile/ 지침을 읽는다. 스펙 read-only /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD53adbd49126c12c887b897854107aa7310cc4f75 의 SPEC004 전문+SPEC003 셸/세션/푸시/테마/이전UI수정, SPEC000device, SPEC001auth. profile work/day-app/chat-decisions-20261110.md/research-chat-notifications.md/chat-spec-rereview.md/chat-wp-report.md 및 WP최종리뷰도 읽는다.

목표: 프로토 /Users/kknaks/git/toy_pr2/cc-prototype read-only pinned77173cf8b62f0b27ec54ec4ee22e9d308b7f701e git show 원형으로 내부직원채팅전기능을DAY에 이식. 로컬오래된checkout사용0. lib/chat8개+screens/chat9개/관련셸/네이티브소스/시험파일근거맵. 최대한그대로디자인, 새화면문구0, DAY테마만. 4메뉴유지, 채팅자리활성. 목록/1:1/그룹/초대/탈퇴·숨기기/음소거/읽음/수정삭제/전달/검색/사진·동영상/모아보기/푸시탭진입/앱내배너/탭배지 누락0. phone/iPad 분기 그대로. 서버규칙재구현0, UUID/seq/API는최종SPEC/WP대로.

허용app/만(Flutter UI/data/model/state/native iOS/의존lock/README/test·capturefixture 포함), profile지정 보고 chat-mobile-code-report.md 및 chat-mobile-evidence/ 이미지로그만. backend서버/루트pyproject·uvlock/deploy/스펙/GitHub건드림0. backend워커같은tree서별도backend편집중이니다른dirty정리/stage/reset0, 앱변경만보고. 서버API구현이부족하면어댑터경계에서코디질문, 계약몰래변경·새서버API추측금지. 새SDK/라이브러리/네이티브API버전은공식현행문서만확인·lock정확히, 기존프로토호환선택. 프로토출처파일/ref 기록. 토큰/실키/실사람본문 로그0.

필수격리: session.api_base_url+environment+hospital scope사용. 로그인확정뒤chat controller 시작(보드보기권한과무관), 로그아웃/병원·계정·환경교체시메모리/실패메시지/첨부임시·video dispose/cache/SSE/타이머비움. 이전세션늦은401/2xx/SSE/첨부결과가새세션삭제/섞임/토스트발생0. 기존 세션epoch안전장치재사용, API임의origin/redirect에Bearer유출0. 같은 messageId SSE+foreground APNs배너중복0, muted/openroom/background규칙, 다기기읽음6이벤트+재연결since/tombstones/from_seq범위 준수. 서버unreadRooms가정본. 클릭푸시environment/hospital 검증,없는방오류원문뒤목록.

사진/동영상은원천선택시트/최근사진/카메라/제한접근더고르기/변환/전송진행·취소·재시도/뷰어·Range, 권한문구 SPEC004source그대로(카메라여권부분만삭제), PHPhotoLibraryPreventAutomaticLimitedAccessAlert 포함. 제한값source그대로, 위젯테스트로실기기API성공했다고허위0. 원장호출native액션/기존통역마이크/세션키체인회귀0. Android신설·FCM전환·전체알림센터·예약·채팅외설정범위확대0.

검증: 새규칙·보안·네트워크계약·UI/스크롤·phone/iPad 의미있는단위/위젯테스트, 전체flutter test·analyze·unsignediOS simulator build 각각최종1회. native바뀐부분기존47와새핵심검증 적절히. 사진/동영상플랫폼실물미실행은정직pending. phone/iPad 대표화면 PNG원형대조(목록/대화/새대화/초대/정보/첨부/전달/뷰어/오류·미읽음). 기존시술현황198테스트/세션도회귀. 정확원천기능→구현/검증파일 매핑과미구현0확인. WP검증필수는생략하지않음.

사용자 실제 시뮬레이터 orca-mobile-iphone UDID5C9E05C7-7171-455E-97CE-2AD2EA097F88, bundlecom.example.day.placeholder, 현재PID45830기록(실제착수시확인). 절대uninstall/erase/logout/토큰삭제/실제채팅·업무조작0. 사용자세션보존. 이전처럼같은기기에서최종main디버그를overwrite install+launch가능(11040localdefines DAY_LOGIN_ENTRY/DAY_DEV_LOCAL_ORIGIN=http://127.0.0.1:11040, DAY_REQUIRE_ENVIRONMENT=false, DAY_APNS_ENV=sandbox), 다만fixture캡처가사용자main세션훼손하지않게기존분리harness절차. 서버재시작·env읽거나출력·DB변경0. 계정로그인통합사용자소유. 최종 앱설치가진짜새API미배포서버에붙으면코드완료와활성화전제구분보고.

완료후app변경목록·원천기능매핑·테스트명령실수치·시각근거·제약/실기기pending·서버필요사항을지정report에기록. exactpreamblecheck/ack, worker_done outcome/reportpath1회후idle.

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

## 발주 확정(사용자 승인 후)
WP=delivery-request-v7.json, 승인=delivery-v7-approved-result.json 및 delivery-v7-plan-approval.json, 최종WP리뷰=chat-wp-rereview.md. 사용자 「코드 구현 하자」. canonical main baseline pending은사용자마지막merge순서때문이며-reviewed 미머지SPEC53adbd49로지금구현(선merge요구0). 후속알림SPEC은사용자병행요청으로다른planner가005만쓰며003/004/000/001은동결, 코드계약변경없음. 알림함/원장호출발송로직은005후속WP전까지이코드발주범위밖, 그러나공유기기등록/APNs를재사용할수있게구조유지. 코디에게필요공유interface파일/구현선택을보고. 테스트하네스는기존승인된로컬스크래치환경의프로그램적설정주입만사용가능, env/키값모델출력·업무DB변경0.
