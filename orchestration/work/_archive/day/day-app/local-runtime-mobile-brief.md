# 현재 시뮬레이터 최신 앱 반영·채팅/알림 실연결
사용자 최신명시지시: 로컬 day-local 서버를 다시띄우고 현재orca-mobile-iphone 시뮬레이터에서 채팅·알림·푸시를 실제확인하라. 앞단계의 서버/시뮬레이터변경금지를 이번 로컬확인범위에서 해제한다. 원격dev/prod/브랜치merge/서명/TestFlight배포/실KOS쓰기/남의실기기알림/하위위임/commit/push0. 비밀값/사용자세션토큰은프로세스에서만사용·모델/로그출력0. key를cat하지마라. 코드원천 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD f83d7fab, 기존 board소스 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2 HEAD9ba7b79e. 두repo원본편집/checkout/reset/merge0. AGENTS+profile역할규칙먼저읽음. 보고는 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/ 아래. 사용자매우급함. 가장먼저실행가능상태를복구하고정밀후속검증, 불필요테스트재실행0.

네소유 app빌드/현재부팅시뮬레이터5C9E05C7-7171-455E-97CE-2AD2EA097F88(orca-mobile-iphone,com.example.day.placeholder)이다. backend worker는동시에day-local재빌드중,기존API404원인은확정. 바로f83최신앱을debug simulator localhost11040정의로build/overwriteinstall/relaunch해사용자기존세션보존. uninstall/erase/logout/사용자키체인삭제0. 기존BundleID를바꿔기존앱세션을잃게하지말것. source코드변경필요시코디질문,먼저현재최신빌드만. defines DAY_LOGIN_ENTRY=http://127.0.0.1:11040 DAY_DEV_LOCAL_ORIGIN=동일 DAY_REQUIRE_ENVIRONMENT=false DAY_APNS_ENV=sandbox. 기존Identity.local.xcconfig 실값확인시내용중비밀출력0. backendready는OpenAPI/health로확인,404이면기다리며앱빌드선행.
런타임연결: 서버반영되면채팅spinner/서버연결중이사라지고새대화직원목록/방목록조회성공인지실화면확인. 테스트만그린fixture로실연결이라하지말것. 현재로그인사용자세션을프로그램내에서읽어HTTP/진단에쓸경우토큰절대모델/로그출력0(필요하면DartVM service객체내처리),권한우회0. 채팅송수신확인은본인+명시합성test직원만,실직원에게메시지/푸시보내기0. 알림은현재로그인사용자또는합성test계정에만,실KOS쓰기0. UI조작은programmatic/SIMCLI우선·불가할때skillcomputer-use준수. User는시뮬레이터바로보고있어화면정상화먼저,실제화면스크린샷증거남겨라.
푸시도동시에확인: native토큰등록성공/서버devicebinding확인(토큰값출력0). 현재placeholder번들/unsigned simulator가실APNs대상이되는지·키production vsSandbox조건을구분. simctl push payload주입은수신UI테스트일뿐 실제APNs성공으로주장0. 실제등록가능환경조건이안맞으면정확원인/최소다음설정보고,채팅/알림정상화는그것때문에미루지말것. 필요하면backend worker와테스트fixtureID만교환(비밀메시지X),계정비번/토큰은보호파일프로그램적전달만.
산출 local-runtime-mobile-report.md:설치PID/로그인세션보존/실제HTTP및SSE상태/실화면PNG/송수신·알림목록/푸시단계별결과/미결. 새preamble IDs/outcome/reportpath worker_done1회후idle.

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

