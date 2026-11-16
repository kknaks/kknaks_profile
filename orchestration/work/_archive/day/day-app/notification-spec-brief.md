# [planner] DAY 알림 페이지·알림/호출 푸시 SPEC (채팅코드 병행)

## 역할·원천
별도워커·subagent 위임0. 스펙 tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD53adbd49126c12c887b897854107aa7310cc4f75 · AGENTS/context/manifest/index/current-state/document-pipeline/delivery-workflow 및 profile orchestration/roles/day/planner 지침 읽기. products/day README/20-spec/30-work → SPEC000 notification/notification_setting/push_log/device · SPEC001session · SPEC002calls · SPEC003 U14/푸시/셸/설정/D2/D5 · SPEC004chatpush·공유기기등록. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS/관련호출·permission·push앱 read-only. backend/mobile가동시에채팅구현중이므로 현미커밋은현재개발상태이지새계약아님. 읽기계약은53adbd49 gitobject를핀.
profile chat/research-chat-notifications.md가아니라 work/day-app/research-chat-notifications.md + notification-decisions-20261110.md, chat-spec-rereview.md/chat-wp-rereview.md 읽기. 작업목표사용자최신: 「코드 구현 하자 그리고 알림 페이지 스펙 만들어 동시에 할수 잇지 ? 알림, 푸쉬도 일단 로직 다 만드는거지 ?」. 채팅WP235v7은승인돼코드구현중, 이발주는알림SPEC만. 사용자병행지시가동일작업의전단계문서를코드와병렬금지하는일반runbook을후속별도기능005에한해넘어선다. 동일알림기능안에서는SPEC→리뷰→WP→리뷰→코드순서유지.
프로토 read-only /Users/kknaks/git/toy_pr2/cc-prototype pinned77173cf8b62f0b27ec54ec4ee22e9d308b7f701e git show. 로컬checkout낡음. 알림원천 lib/widgets/header.dart · screens/notifications_screen.dart/settings_screen.dart/shell.dart · app_state.dart · model/notification.dart · push/push.dart · ios/Runner/AppDelegate.swift; 서버 notification API/service/repository/push.py/apns.py·시험까지 실제파일확인. 원천SPEC있다고지어내지않음. 기존 UI · 원문글자그대로 DAY색만, 과거시술현황디자인재설계실패반복0.

## 결과
신규 DAY-SPEC-005(번호빈것확인·충돌이면코디질문) 알림페이지+기존원장호출알림생성/목록/읽음/모두읽음·배지·설정·SSE·기기등록재사용/APNs호출푸시/탭·native수락의서버와앱계약을구체화. 아직기존관련테이블만있고API/trigger없다는사실정직, 채팅서버는이번다른워커가만드는것. 채팅푸시가notification행/종배지밖인원천규칙을지키고, 채팅tab badge/배너와중복집계하지않음. 전체알림함의표시종류는현재실제기능원장호출, 상담사호출은향후·kindenum존재와구현범위구분. 사용자가지금상담사호출API제작하라는지시없음.
UI: 종99+ · 0숨김, 각탭머리공통접근, 폰전체/iPad420오른쪽시트, 제목/닫기/모두읽음, 리스트제목/시각/본문/안읽음바탕, 누르면서버읽음→대상room이동, 없음/권한소실/계정변경실패원문처리. 설정안에원천역할해당종류알림스위치·OS권한꺼짐안내·기기이름있는범위를원천과DAY모델대조, 알림과무관한설정재설계0. 원천직무문자열을DAYpermission/tag/activehospital에대응, 새권한키발명0.
확정호출푸시수신자=해당병원의원장목록전체(전체호출) 또는지정원장. 관리자자동추가/호출원장자동제외0. 간호사대리수락기존board경로보존, 알림받는사람정책과수락권한혼동0. 사용자2026-11-09결정우선, prototype관리자추가·호출자제외는이식하지않음. 같은병원/계정소유알림만 · 상태가변해도열람/수락은현재서버can*/권한이정본. 외부KOS쓰기추가0.
API:notification list/unread/read-all/read-one/settings·SSE와호출 생성시notification기록/푸시연결시점, 재호출중복/대상·부분수락/이미수락·취소/만료/같은호출다중기기·계정비활성/멤버십소실/동시읽음/같은seq·타임경계 메우기 계약이실행가능하게. 숫자/문구/정렬/페이지크기는원천에근거, 빈칸은실제OQ로구분하고단순구현선택새질문양산0. 알림기록을남기는것과APNs키없어skip는분리(메시지/호출조작성공과푸시실패별도). 재시도·죽은token·지연결과가새등록안지우는동작은v7계약공유, 중복기기API만들지않음. headerbadge/sseaccountscope/hospital/session/env/로그아웃동시401 격리. 같은계정다병원notification조회/기기세션병원결속 일관. 숨은데이터모델변경 필요하면최소제안만보고하고공유000지금수정금지.
푸시전체준비는현iOS먼저·APNs직접. 토큰/발송/알림tap/네이티브원장수락·실패·권한거부·재등록·로그아웃로직을서버/앱양쪽에서검증가능하게명세. Apple등록/키/Bundle서명·실env·TestFlight·Blob실설정은사용자, 실제수신은그때실기기검증. Android/FCM새앱과SDK통일을자동확대0, 사용자가나중지시하면별도범위. 기존계약은APNs코드공유재사용하는의존으로명시.

## 편집경계·독립병행
허용 products/day/20-spec/spec-005-notifications.md 신규 + 20-spec.md 인덱스최소행 +30-work.md Coverage최소행. 003/004/000/001/002/architecture/코드/GitHub/commit/push/merge 금지(채팅워커동결계약). 기존D5등연결정정필요는보고서에후속패치리스트만. WP JSON 아직없음. 보고 profile work/day-app/notification-spec-report.md 하나. 출처/ref/줄·원형기능매핑·와이어/문구·HTTP/SSE/오류·권한/연결/상태/인수조건·실제OQ 포함. 새schema필요없는지대조, 독립리뷰뒤기존PR921/235에추가예정·1codePR237/dev·머지사용자마지막.
검증lint strict1회DAY ERROR0·무관warning분리, gitdiff--check/편집경계, 기존53adbd49의003/004/000/001/002 blob불변확인. 진짜미실행코드/서버/기기완료로쓰지않음. 정확preambleID/outcome/reportpath1worker_done, 완료전check/ack후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
