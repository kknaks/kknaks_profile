# 로컬 서버 즉시 반영·재기동
사용자 최신명시지시: 로컬 day-local 서버를 다시띄우고 현재orca-mobile-iphone 시뮬레이터에서 채팅·알림·푸시를 실제확인하라. 앞단계의 서버/시뮬레이터변경금지를 이번 로컬확인범위에서 해제한다. 원격dev/prod/브랜치merge/서명/TestFlight배포/실KOS쓰기/남의실기기알림/하위위임/commit/push0. 비밀값/사용자세션토큰은프로세스에서만사용·모델/로그출력0. key를cat하지마라. 코드원천 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD f83d7fab, 기존 board소스 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2 HEAD9ba7b79e. 두repo원본편집/checkout/reset/merge0. AGENTS+profile역할규칙먼저읽음. 보고는 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/ 아래. 사용자매우급함. 가장먼저실행가능상태를복구하고정밀후속검증, 불필요테스트재실행0.

네소유는로컬Docker day-local API/worker/scheduler와필요한추가0007migration·scratch빌드문맥. postgres/redis서비스/데이터볼륨삭제·down -v·DB초기화0. 현재day-local컨테이너의compose원천은day-procedure-board-2/deploy/compose.local.yaml,이미지day-backend:local. 백엔드프로필내env는 /Users/kknaks/git/CENTURION_DAY/deploy/local.env 프로그램적source만,값출력0. 현재사용중인최신board업무/웹행동을없애지말고알림/채팅f83코드를합친 **로컬전용scratch문맥**을만들어반영한다. 새Gitworktree/featuremerge0. 같은gitrepo객체에9ba/f83모두있음. 예: scratchpad/day-app-local-runtime 에9ba gitarchive를기반, base91728737..f83의파일patch를3way적용/겹치는변경최소조립(특히services/board.py는현재9ba에커밋뒤notifications.after_call 두군데만, 0006의존byte동일). 버전/파일기록을보고해재현가능하게. 제품소스원본은건드리지말고원본서버를옛board로퇴행시키지말것. migration단일head0007과기존컬럼보존,로컬pg_dump백업을비밀없는보호로컬파일로먼저확보한뒤증분upgrade만. 원본이미지ID/compose태그/롤백정보저장,현재프로젝트day-local/포트11040/PG11042/redis11043 재사용. 최소api/worker/scheduler재생성,DB/Redis기동유지. 빌드명령/composeoverride는scratch파일에(비밀값주입된compose config출력0). 설정은기존local.env유지,새APNs설정은로컬보호override env로만주입가능. credentials ~/.config/day/apple/credentials.local.json 의apns항목을프로그램적으로읽어DAY_APNS_AUTH_KEY/KEY_ID/TEAM_ID/ALLOWED_APP_IDS주입(키값출력0). APNs실수신은별도검증,현재키Production범위일수있고simulator는Sandbox라무조건동작주장0. 실제남의기기로발송0. 기본첨부disk켜고전용영속volume복구부여필요시user로컬설정만.
관문: http127.0.0.1:11040 health200, OpenAPI에/api/chat/rooms,/api/chat/stream,/api/notifications,/api/notifications/stream,/api/devices/{install_id}존재,기존boardAPI/웹 health동작·기존로그인세션보존. 준비되면완료전이라도코디와mobile term_e8a8842c-a789-4862-93a5-7886d6bd1c61에status로APIready알려즉시연결하게. 안전한합성테스트계정2개를같은KOS데모병원에필요시준비가능(기존계정패스워드/직원/방임의변경0),채팅/알림E2E는로그인한현재사용자또는명시테스트계정에만·실KOS/남의푸시0. 없으면새test병원/직원fixture가능하되user세션고객표시보존. 테스트데이터는보고/정리구분.
산출 local-runtime-backend-report.md:실제이미지source/기동/migration/health/API/보존/권한/env이름만·롤백·미결. 필요로그에비밀/고객정보0. 새preamble IDs/outcome/reportpath로worker_done1회후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_bdc96429-0e21-4311-bca9-622e97ece387 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

## 발주 확정(사용자 승인 후)
WP=delivery-request-v7.json, 승인=delivery-v7-approved-result.json 및 delivery-v7-plan-approval.json, 최종WP리뷰=chat-wp-rereview.md. 사용자 「코드 구현 하자」. canonical main baseline pending은사용자마지막merge순서때문이며-reviewed 미머지SPEC53adbd49로지금구현(선merge요구0). 후속알림SPEC은사용자병행요청으로다른planner가005만쓰며003/004/000/001은동결, 코드계약변경없음. 알림함/원장호출발송로직은005후속WP전까지이코드발주범위밖, 그러나공유기기등록/APNs를재사용할수있게구조유지. 코디에게필요공유interface파일/구현선택을보고. 테스트하네스는기존승인된로컬스크래치환경의프로그램적설정주입만사용가능, env/키값모델출력·업무DB변경0.
