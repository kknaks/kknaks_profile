이번 reviewer는 backend작성자이나 app작성참여0이다. app 독립리뷰역할이며 backend재수정금지. 기존backend작성편향을공개하고 API대조는SPEC005원천이우선, 테스트더블결과를실통합으로주장0.

# 알림v8 독립 코드 검수
read-only·직접수정/commit/push/merge/하위위임0. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS.md 및 profile orchestration/roles/day/reviewer 규칙 준수. 시작base3aaa97806684b8cea7f7fb777adbcdcff7ae0de6 위 이번 v8 미커밋변경만을 검수. 승인 request delivery-request-v8-execution.json 및 delivery-v8-approved-result.json, SPEC /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec b0f71ec3의 SPEC005전문+003/004/000/001인접계약, 원형 /Users/kknaks/git/toy_pr2/cc-prototype gitshow77173cf8 read-only. 새문구/수신자/권한정책발명0. 이슈mainbaselinepending/미머지는사용자마지막merge순서, 검수를선merge로막지않음. 사용자실계정/시뮬레이터/Apple키/서명/실서버11040/실env/DB/포트/프로세스변경0. profile보고/증거만생성. API/실키테스트·fixture·실PG/Redis를구분해정직기록. 작성자테스트수치복사만으로PASS금지, 실코드경계·핵심관문집중재현. 통과한전체테스트무의미반복0. 각결함은fileline/실제재현/사용자영향/최소정정, 가정만으로WARN늘리거나범위바깥보완반복0.

## 앱 검수
notification-mobile-code-brief.md / notification-mobile-code-report.md 및기존chat후속리뷰먼저읽고 app/변경만검수. backendwriter는병렬이라DB테스트/서버조작0. 알림API는SPEC005고정, 서버미완성시더블계약맞춤으로판정하고실제통합으로주장0.
종모든탭99+/0숨김/accessibility·서버unread값·별도chat배지·notification전용SSE/연결줄없음·login/resume/reconnect/read/foregroundpush시조회·목록열린동안unread변화갱신/동시반복요청무한루프0. 읽음/모두읽음idcallId구분·ids[]와AND전송원천·일전환목록오늘·settingservereligible/default/switchoff실패복원/OSdenied안내원형. 폰전체화면/하단메뉴위·iPad오른쪽420·목록순서·빈/실패/로딩/풀refresh·timestamp·readbg. 원형같은viewport/글자배율PNG직접대조, DAY색/4메뉴/직무차이만·새문구0. 긴제목/본문/가로/스크롤·필수버튼접근/overflow0·셸키보드회귀0.
인증세션·병원/환경guard는kinddoctorcall과chat양쪽·늦은401/200/SSE/read/settings/nativepush/열려있던sheet가새세션종/목록/네비/토스트변경0. 로그아웃종0/caches/streamdispose·no-board활성직원기존셸과알림설정유지하되상세/수락은현재권한·APIcan값·다른병원푸시읽음/이동/native수락0. 푸시tap callId읽음 vs목록ids읽음중복0·이동카드없음기존토스트·기존nativeCALL/category/keychain/기기등록·chatbanner/read/tabs·시술현황/통역회귀0.
독립analyze/notifications+셸/세션/push관련집중테스트·native는변경시에만·build보고실물대조. 실기기/実APNs/서버라이브pending구분, 사용자시뮬레이터조작0. 최종notification-mobile-review.md+변경filehash·PASS/WARN/FAIL·명령수치/PNG·원형문구/디자인동일성·실물확인자리. 새preambleIDs/outcome/reportpath로worker_done1회후idle.

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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

추가실물검수포커스(코드완료후재현해판단): chat_events는tx안에서계정별payload를만든뒤Redis에발행하고chat_stream_events는현재session/staffguard만거치는구조로보임. 발행/수신사이에멤버가나감→재초대from_seq증가한경우 이전room의queued chat_message/edited/deleted/room payload가새경계밖으로흐르지않는지 실제단위/probe로확인. 단순actor생존체크만으로roommembership/from_seq까지검증했다고판정0. 호출순서/이미전송된data와수신전검증의보장범위를분리해실제SPEC004위반여부를근거로판단.

완료보고후추가집중: report의미실행3/4는실키설정이아니라 남은코드연결( scripts/deploy/day_vm.py optional secret whitelist / 로컬disk writable·영속볼륨) 문제일수있다. 사용자「일단로직다/키나중」를만족하려면추가코드작업없도록선택비밀2개지원·예시/테스트·디스크경로/마운트지원이필수인지실물검수해최소정정제안. 실제Vault읽기/배포/DB/서비스시작0. code_surface범위부족은코디가Execution경계만추가할수있으니 '범위밖pending'으로논리누락을닫았다고하지말것. 새required secret로기존배포를깨지않는선택설계필수. source설정/vm.py읽기만가능.
