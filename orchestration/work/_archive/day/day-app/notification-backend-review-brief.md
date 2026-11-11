# 알림v8 독립 코드 검수
read-only·직접수정/commit/push/merge/하위위임0. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS.md 및 profile orchestration/roles/day/reviewer 규칙 준수. 시작base3aaa97806684b8cea7f7fb777adbcdcff7ae0de6 위 이번 v8 미커밋변경만을 검수. 승인 request delivery-request-v8-execution.json 및 delivery-v8-approved-result.json, SPEC /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec b0f71ec3의 SPEC005전문+003/004/000/001인접계약, 원형 /Users/kknaks/git/toy_pr2/cc-prototype gitshow77173cf8 read-only. 새문구/수신자/권한정책발명0. 이슈mainbaselinepending/미머지는사용자마지막merge순서, 검수를선merge로막지않음. 사용자실계정/시뮬레이터/Apple키/서명/실서버11040/실env/DB/포트/프로세스변경0. profile보고/증거만생성. API/실키테스트·fixture·실PG/Redis를구분해정직기록. 작성자테스트수치복사만으로PASS금지, 실코드경계·핵심관문집중재현. 통과한전체테스트무의미반복0. 각결함은fileline/실제재현/사용자영향/최소정정, 가정만으로WARN늘리거나범위바깥보완반복0.

## 서버 검수
notification-backend-code-brief.md / notification-backend-code-report.md 먼저 읽고 backend/와추가sharedpush/설정diff소유경계를확인. app은다른writer라미검수.
API4/SSE: 인증·계정/세션병원·오늘KST경계/50밖unread·ordering·unknownkind·빈ids0/idsANDcallId/absent모두읽음전체날짜·동시읽음수·settingdoctorlist같은대상·계정전역defaulttrue/비원장400. 원장목록집계가직무권한기준일관·시스템계정등기존boardlist조건과같음.
기존호출·재호출업무tx/응답변경0·commit후만훅·실패가성공뒤집기0. 병원전체/지정대상·관리자추가/호출자제외0·settingoff알림/pushlog0·키/기기없어도알림행. 실제PG doctor_call행잠금과동시후크(call,account)한번, 새recall새id앞행유지, 중복task푸시한번·발송중세션/직원/setting/토큰변경재검증. APNs기존sharedclient/retry/deadtoken/code복제0·namespace·만료0·CALL board.accept.edit 기기세션별·env/hospital·PushLog기존status/notification_id/token_tail. sharedpushrefactor로채팅수신자/멱등/소프트삭제/만료1일회귀0, log본문/토큰0. DBtx내네트워크기다림0·1세션동시task0·N+1/lockorder/timeout/concurrency·재시도bounded.
SSE구독은머리전확인·채널account+hospital·새알림/실읽음>0커밋후notificationunread·초기replay0·도중sessioninvalid민감데이터0·response/generator취소/실패/연결끊김정리·45초timeout/1시간한도. notifycounts가다른병원로새지않고읽음다른기기동기화. 기존models/migrations무변경/0007singlehead.
실PG/Redis focusednotifications+board+chatshared회귀는작성자종료후네단독주자. 기존DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env source프로그램적주입만, env값모델출력0·day_test/Redis15만. scripts/test.sh경계읽고사용. ruffbackend scripts/architecture관문도관련범위만. live푸시/실키/서버배포미실행정직. 최종notification-backend-review.md+filehash·PASS/WARN/FAIL·명령수치·기기공유/프로토정합·실물사용자확인자리. 새preambleIDs/outcome/reportpath로worker_done1회후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_1d5db035-7383-46d1-97ae-2e65e50e3927 \
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
