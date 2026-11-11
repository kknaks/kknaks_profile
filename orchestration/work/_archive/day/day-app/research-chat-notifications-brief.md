# [mobile 조사만] 기존 알림·푸시 이식 가능 범위 / 채팅 원천 확인

순수read-only 조사, 코드/SPEC/WP/GitHub/서버/env/기기/DB/commit/push/merge쓰기0. 하위위임/내부agent0. 산출물profile지정report1개만. 기존day-app코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEADb6c034bf, spec /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD06239a1c. 새로운구현은아직승인범위정리전이며조사만.
사용자 「내부 채팅 구현 ... 기존 앱에 채팅 그대로 옮기고 알림도 그대로 ... 권한 일부 ... 디자인최대한유지」 + 「아이폰/안드로이드둘다푸시설정토큰받아야하는거아니야?」. 디자인원형유지·DAY권한/병원격리/실제API맞춤필수. 현재확인한프로토 /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app 에 notifications_screen/model/push/settings 구현있고 shell.dart현재4탭(예약/내원/시술/설정), chat 파일이나채팅문구안보임. 코디가사용자에게기존채팅기준레포/경로async질문중. 경로답없으면추측해서다른서비스AI채팅을직원채팅으로간주하지않고미확인으로보고. 프로토git history등필요한읽기로만실제채팅원천유무검증.
조사:
1 프로토알림목록/읽음·모두읽음/배지·역할별알림설정/탭연결/폰전체화면·iPad시트 디자인·앱APNs/Android푸시코드존재 실제파일:줄. 호출/상담호출/띄우기등 종류와DAY이식시권한/대상수정필요. 문구번역새로짓지말것.
2 DAY앱현재 iOS AppDelegate/push_bridge/push_coordinator의권한/APNs토큰등록갱신·해제/네이티브수락/세션origin/기기·사용자연결, Android폴더/FCM존재여부정확히. 현코드iosonly면Android구현안됐다고구분. 계약D2/D5/기기API와서버실구현은구분.
3 gitfetchorigin/dev(안전읽기) exacthead backend/api/services/models/routes에서현재 기기등록/APNs발송/알림목록·미읽음·읽음/설정/실시간/채팅API 존재여부. 최신mainSPEC도fetch해서DAY관련계약유무읽기. 사용자로컬backend옆tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2 는githead/status/소스읽기만(서버재시작/실env/자격증명출력0). backend쓰기절대0.
4 채팅원천못찾아도알림조사는끝내서보고. 그대로가져올디자인/권한·API교체/없는서버기능/추가사용자결정 분리. 앱쪽토큰받기와서버전송/Apple·Firebase등록설정/서명키는다름. FCM으로양쪽통일하거나 iOSAPNs직접+AndroidFCM 선택은아직결정하지않음.
공식참고: https://firebase.google.com/docs/cloud-messaging/flutter/get-started · https://firebase.google.com/docs/cloud-messaging/manage-tokens . 코디최신조회에서FCM은기존등록토큰과새FID방식을함께지원하는전환안내가있음. 버전지정/구현선택은하지말고SDK확정할때현행문서검증필요로기록. iOSFCM도APNs설정필요. 출처텍스트장문인용0. 현DAY는Firebase없는APNs직접구현확인됨.
산출물profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/research-chat-notifications.md. 짧은결론+표/파일줄근거·head/있는것없는것·남은결정, 구현/설계발주로확장하지않음. 고객·직원실명/토큰/설정값보고0. 테스트/빌드/기기조작불필요. preambleID/outcome/report-path worker_done한번후idle.

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
