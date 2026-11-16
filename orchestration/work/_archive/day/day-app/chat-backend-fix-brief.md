# [backend] 채팅 코드 리뷰 WARN 마감

같은code tree/AGENTS·role·안전/테스트규칙, 기존backend-code-report/review 및review로그읽기. app모바일fix중건드림0. canonicalv7 execution은 delivery-request-v7-execution.json→delivery-v7-execution-result.json으로갱신완료(statusexecution-updated/contract00d8/plan22f그대로approved). 원v7JSON/스펙/승인무변경. code_surface에 scripts/deploy/day_vm.py optionalsecret배선+금지키/테스트·deploy/Dockerfile첨부디렉터리권한·compose로컬영속볼륨이추가됨. 운영값/실Vault/실서버기동/migrate/업무DB/port변경0. 이필수코드마감은이미승인결과를구체화한Execution보완이지새범위승인대기아님.

W1 **구독은HTTP머리전에준비되어야함**: reviewer최소안 'retry바이트전에subscribe'만으론부족할수있음. 실제app/lib/chat/chat_stream.dart:_connect는HTTP200머리를받자마자onConnected→rooms/since메우기, 바디retry수신은기다리지않음. StarletteStreamingResponse는generator시작전http.response.start를보내므로generator안에서subscribe후retryyield만바꿔서는race남음. pubsubsubscribe확정을response.start보다먼저보장하고resource수명을response종료/취소finally까지유지(안전한responsewrapper/context 등선택너의몫). 헤더받자마자publish하면HTTP메우기와SSE사이에메시지가빠지지않는실Redis/ASGI send순서회귀test1건+cancelcleanup. 기존6종/1h/tick/세션검증/backoff/초기데이터재전송0 규칙그대로, 운영기한축소·skip X.
W2/W3 optional 비밀두개 DAY_CHAT_BLOB_CONNECTION_STRING / DAY_APNS_AUTH_KEY→KeyVault naming기존규칙→app.env(Docker env_file), 없어도기존필수secret계약/배포준비성공유지(선택), 있어도일반Git설정에넣으면FORBIDDEN_CONFIG_KEYS거부. realaz/key읽기0, fakeunit/dry-run으로두값전달/생략/금지key/실값로그0·PEMnewline보존검증. name/config예시와문서만, 실제리소스값은사용자.
코디필수disk마감: 현재컨테이너USERday가쓸영속마운트경로를코드/compose로지원해local.env만채우면추가코드수정없이사진동영상가능하도록. Dockerfilemkdir/chown+localcompose API/필요worker namedvolume mount(서버prod는Blob기본방향·여전히사용자설정), 기본storageoff/failclosed유지·컨테이너서비스재시작0. 최소설계와검증가능한config/runtime권한근거를보고, 데이터삭제/기존볼륨변경0. optionalenv값/도메인/계정하드코딩0.

서버심층HTTP/기기/첨부검수는현재리뷰가집중test재실행수준이라고보고했으므로수정뒤독립review추가예정(네가스스로PASS선언으로생략0). 네수정범위는이SSE/배선/해당테스트/문서만, 다른핵심동작임의바꾸지않음. 검증 targeted관련+전체원고변경후최종1회755기준·ruff·아키텍처·한head/스크래치PGRedis필수, 중복pytest프로세스확인. source값출력0. 새report chat-backend-fix-report.md+logs. 원천설정・모든WARN before/after/actual결과·extra미실행정직. 한국어완료요약, 정확preamble/checkack/worker_doneoutcome1회후idle.

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

