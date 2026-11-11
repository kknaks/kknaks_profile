# 이번 재검수 추가 지시(아래 옛 브리프보다 우선)
독립 재검수. chat-backend-fix-report.md / chat-backend-review.md / delivery-request-v7-execution.json을 먼저 읽어라. 변경 작성자는 모두 작업 완료·코드 수정 중단 상태다. 이전 3 WARN의 실제 해소(특히 Redis SUBSCRIBE 확인이 HTTP 머리 전, 취소 정리, optional secret/금지키, disk 권한·영속)를 재현하고, 첫 검수에서 깊이 읽지 못했던 HTTP20·device·media·idempotency 권한 경계를 직접 읽고 관련 집중 테스트로 확인해라. 기존 전체 765 테스트 반복할 필요 없다. 실제 DB 테스트 주자는 너 하나이며 app 검수와 병렬이다. 최종 보고 chat-backend-rereview.md, 수정 금지. SPEC 현재 b0f71ec3의 /me 실제 사실 정정은 참고하고 새 SPEC005 알림 코드는 범위 밖. 아래 완료 명령에는 --outcome succeeded/failed 와 --report-path 실제 경로를 추가하고 preamble IDs 사용.

# [reviewer] DAY 채팅 backend 독립검수

backend완료뒤발주. read-only·하위위임·commit/push/merge/GitHub0. 보고 profile work/day-app/chat-backend-rereview.md 만. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS·백엔드안전/테스트/role day/reviewer 읽고 chat-backend-code-brief.md/chat-backend-code-report.md, 최종WPv7 request/approved-result/리뷰를검수. SPEC pinned53adbd49 004·000device·003·001(같은spec tree005변경은후속문서라v7검수범위밖). 프로토77173cf8 원천read-only.
수정은backend일체및선택0006의존+0007/deps/config/test만검수, mobile app/는동시진행이라 dirty에있어도본backend검수엔포함하지않음. currentHEADb6c034bf위미커밋경계/서버파일hash를보고서에기록해커밋동일성확인. DB하네스기존로컬승인경로 DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env source만(값모델노출0)·day_test/Redis15만, 운영DB/port/process/restart0. backend작업의전체infra시험과리뷰시험이동시같은schema를쓰지않게완료확인후만실행.
핵심: HTTP20/SSE6/기기2/첨부/APNs·타입·오류·원형행동/권한모든경로, 같은병원활성직원/세션도중권한변화/SSE계정병원필터·재접속since수정삭제/캘린더경계/membershipfrom_seq. 실제PG rowlocks·directunique·seq배정·deleted포함clientId멱등/메시지위조·다른병원클라이언트키충돌·전달부분실패/원자성·삭제/전달/첨부한번붙기·파일참조경합. 단위mock성공을실DB증거로혼동0, N+1/querycount검증, routerDB접근/repository층/ORM외부노출0.
Device oldPUT/DELETE vs새로그인/토큰업데이트·namespace(platform,app_id,push_env,hash)유일·sameinstall다중session·새sessionbinding손실0·암호화·허용app_id/입력한도·토큰메타위조. APNs기기세션정합·activeaccount/member·mute·from_seq·중복job·송신중퇴사/토큰바뀜·410/DEAD400늦은응답이새binding안지움·기존status4값·retry1회범위/timeout/concurrency·키없음skipped성공유지·로그본문/토큰0. commit후전송·파일I/O/네트워크tx안기다림·events실패메우기·작업취소정리.
첨부MIME실체검사·파일크기/메타한도·초대전첨부/탈퇴접근/다른병원/임시파일·파일경로탈출·범위206/416·메모리/디스크무제한0·Blob공개/서명URL권한우회0. SDK공식문서근거/실lock·미설정failclosed·local/server api/worker 설정전달.0006 byte원천불변sha+모델index같음/0007한head/실PGupdown·과거nullable데이터보존/forwardonly운영rollback문서.
각FAIL/WARN에file:line·실제재현/근거·영향·최소정정, 구현직접수정0. 기존기능/로그인/원장호출회귀, 사용자가실물에서볼이상자리도분리. 적절한집중테스트재현·ruff/architecture 등최종변경관련만,이미통과한전체테스트불필요반복0.실키/외부APNsBlob미실행정직. 최종PASS/WARN/FAIL·검증명령수치·파일경계hash·미결. exactpreamblecheckack/outcome/report worker_done1회후idle.

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
