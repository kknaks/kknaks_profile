실행 기준 SPEC exact commit: cdde456af1e38a988470b5144278cbb04360341f / review-local-alignment2-report.md PASS. 사용자 2026-11-10 진행지시 승인 범위의 DAY 로컬 API 소비 정합 완료.

# [mobile] DAY 직원 앱 사용자 UI 교정 + 로컬 API 소비 구현

너는 DAY mobile 워커. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/mobile/ 문서와 코드루트 AGENTS.md 읽는다. 앞맥락은브리프/산출물로복원. 하위워커/내부서브에이전트금지.
코드트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, branch kknaksss/day-app, 시작HEAD0b776e900cc229f3a447cb0e937400534b6bc709, PR237 OPEN→dev. 기존app155tests/native47/analyze0/buildOK·독립PASS. 이전모바일구현자와같은터미널이나옛브리프의금지보다현재지시우선.

## 1. 계약·원천
- 스펙트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec/products/day/20-spec/spec-003-mobile-app.md **로컬API정합 최신리뷰PASS판**(발주시코디가기준commit전달). SPEC001환경·보안, 원본SPEC0031551fa22의UI13항목은보존.
- profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app 안 _RESUME.md, local-alignment-brief.md, planner-local-alignment-report.md, review-local-alignment-report.md, delivery-request-v3.json, ui-spec-brief.md, research-prototype-board.md, research-prototype-toasts.md, mobile-fix1-report.md, review-mobile-code2-report.md.
- **시각원천**: 같은profile ui-reference/*.png 13장 + /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/screens/board_screen.dart·room_screen.dart·widgets/{ui,call_sheet,interpret_bar,interpret_drawer,header,shell}.dart·theme/tokens.dart를read-only로직접확인. 원래디자인을유지하고DAY색/브랜드만바꾼다. 기존새앱의각진기본Material목록을옳은원형으로간주하지않음.
- 실제로컬backend 원천 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2 @a1c90b9dc63271dc06023ec0a530c53a216a296c read-only, SPEC002는옆spec @e421b77b read-only. 로컬day-local11040 ready200, 이브랜치compose실행확인. canonical~/git/CENTURION_DAY는사용자트리·변경금지.

## 2. 사용자승인·범위
「응 작업 시작하자 ! 지금 테스트는 로컬 백엔드로 올렷어 !」. 앱구현/테스트/시뮬레이터실행허용. 이번코드변경app/**만, 백엔드·웹·스펙·배포/실env/서버재시작/시드수행금지. 기존PR237이어감, 커밋/push/PR/merge는코디몫. Apple서명/TestFlight사용자. 자격증명찾기/Keychain읽어서토큰꺼내기/실고객업무조작금지. DB/worker/scheduler/포트건드리지않음.

## 3. 구현할UI·동작(스펙최신판정본)
1. 셸 4메뉴 예약현황/시술현황/채팅/설정, 폰하단탭/iPad레일. 예약은「곧 출시 예정」, 채팅상세후속. 공통헤더DAY/탭제목/종(실알림API없어배지나클릭목록발명금지). 계정/로그아웃설정으로.
2. 필터4개전체/확인필요/시작가능/시술대기, 서버inbox.section 소비.
3. 고객카드4행: 방—수납필요 / 고객명·한글발음 / 나이·국적·제공기타 / 상태상자·담당의. 둥근원형·여백/구획은원본, 사용자ASCII우선. 임의진행0/2줄추가없음.
4. 마취중한줄·연보라·서버long이면빨강. 완료는시술대기-마취완료N분/담당의. lastSeconds시간형식변환만.
5. 호출후목록카드에대상/수락대기/호출시술/경과/건수/수락. 상세도강조박스. **원장본인바로수락, 간호사원장선택드로어대리**, 목록/상세/호출탭공통·서버권한유지. 다른원장지정호출본인수락현서버성공사실그대로, 새차단없음.
6. 상세헤더「< 시술현황    {방}」, 오더메모상단여백축소. 시술카드제목/담당의/상태/버튼, 진행중연한DAY배경·테두리·큰경과/종료버튼, 완료아래회색. 시작/종료DAY주색통일. ⋮세로더보기·서버canUndo*만. 최신DAY취소확인원문모달(토스트되돌리기없음).
7. 상세상시체크박스삭제, [의사호출]→한시트안시술체크/전체선택+대상원장→호출. 마법사두장금지. pickable/canCall서버값. 재호출canRecall서버값·원장고르기유지.
8. 전부완료시강조박스「시술모두완료」·마지막종료시각·귀가대기버튼, 헤더상태표시. canHome/서버카드이탈그대로.
9. 통역원형드로어: 핸들/언어드롭다운·방·경과/종료/중앙자막/둥근빠른말하기칩/큰원형마이크·상태. 칩스피커아이콘·라운드·가로스크롤, 아래통역하기버튼.
10. TW→중국어(번체)zh-Hant초기선택, 고객바뀌면이전en이덮지않음·수동변경동기화. 7언어/기존번역만·vi/yue칩없음·사전은서버. 보기권한통역유지.
11. 성공토스트원본어두운둥근상단·2.6초·덮어쓰기·원문만, 본인조작2xx에만. 이전세션/떠난화면늦은응답/SSE타인조작으로성공토스트없음. 되돌리기버튼없음. 오류는DAY코드문구우선.
12. API정합파서/fixture: need→needs[]5상황, lastMinutes→lastSeconds, canRecall, pickable ready-only. 임계값·권한·순서/need업무판정은서버. 기존필드없다고조용히성공위장금지. 최신API소비면서환경격리/세션race/로그보안/타임아웃/redirect차단 보존. 원장변경API/방이동/차트쓰기신규기능추가없음.

## 4. 로컬빌드·시뮬레이터
기존day-dev가아닌 **http://127.0.0.1:11040**. debug값만:
DAY_LOGIN_ENTRY=http://127.0.0.1:11040
DAY_DEV_LOCAL_ORIGIN=http://127.0.0.1:11040
DAY_REQUIRE_ENVIRONMENT=false
DAY_APNS_ENV=sandbox
DAY_ALLOWED_ORIGINS는로컬용공백가능(existingBuildConfig). 실제URL소스하드코딩금지. releasehttps필수/허용origin/환경필수완화금지.
로컬http ATS가막히면debug전용build산출물/ignorelocal설정으로만해결(전역설정/commitInfo.plist허용http넣지않음), 원인보고. 개발용예외가release에포함되지않는지검증. 기존Simulator기기 orca-mobile-iphone UDID5C9E05C7-7171-455E-97CE-2AD2EA097F88 확인후재사용·다른기기정지/초기화금지. iPad필요하면기존자동화용기기inventory확인후사용, 사용자기기는건드리지않음.
기존저장된day-dev세션을로컬에보내지말것. 토큰추출/계정찾기/비밀env읽기/로그인시도안함, 사용자로그인할수있게로컬진입로그인화면을띄우고남김. authenticated통합은미실행이라고정확히기록. 로컬요청health+401API확인은read-only가능.

## 5. 검증·시각증거
FVM3.44.8고정, 전역설정변경0. 의미있는위젯/계약/세션회귀테스트: 새API실제shapefixture, 원장picker안뜸/간호picker뜸과정확APIbody, 권한/need/recall/취소확인/토스트late응답/TW고객전환/호출시트선택/모달세션정리. 기존155테스트를무작정삭제/완화하지말고계약변경분만정정. 320폭, 폰/iPad, 짧은변599/600 overflow0.
최종수정후 analyze, fluttertest, unsigneddevicebuild 각1회(실패하면해결후재실행),native변경없으면기존47빠른회귀가능. 모든통과후불필요반복하지않음.
**시각검증필수**: waiting/anesthesia/call-wait/doing/done/all-done/doctor-call-sheet/nurseaccept/interpret-drawer/4tabs 화면을폰+iPad에서실제Flutter위젯으로렌더해PNG. 테스트fixture렌더면fixture라고명시, 실제backend데이터로위장금지. widgetgolden캡처/기존테스트하네스이용가능, 새production데모/가짜데이터flow추가금지. 필요검증전용capture테스트는app/test에범위명시. 산출물profile mobile-ui-evidence/에저장하고원본png들과직접눈으로비교·수정. 원본구조무시한새디자인으로완료보고하지말것.
실제iPhoneSimulator에는로컬빌드앱설치/실행·로그인화면screenshot·PID기록, 앱켜둠. unsignedbuild와simulatorbuild는목적달라둘다가능. 실제로그인은사용자, liveAPI정합은소스/fixture대조까지만.

## 6. 산출물·경계
app/** 코드·테스트·README만. profile mobile-ui-code-report.md, mobile-ui-evidence/**, 필요시시각체크리스트만. 기타파일수정금지. 보안/세션기존수정빠뜨리면FAIL. D2/D3/D5실서버pending정직기록.
보고서구현대조표13항목+API6차이·변경파일·실명령/수치·스크린샷목록/fixture구분·로컬연결·로그인미실행·남은실물의존을한국어로. livepreamble우선·마지막메일확인후worker_done한번·idle. 독립reviewer가이후코드+원본/결과PNG비교예정.

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
