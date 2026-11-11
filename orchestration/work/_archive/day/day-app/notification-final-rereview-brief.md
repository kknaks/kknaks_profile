# 알림v8 WARN2 최소정정 최종 재검수
read-onlyReviewer, 하위위임/제품수정/commit/push0. /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS와 profile roles/day/reviewer 준수. 앞 notification-backend-review.md(PASS/W1시험범위), notification-mobile-review.md(PASS/W1설정차례), notification-backend-fix-report.md, notification-mobile-fix-report.md를먼저읽어라. 이번범위는backend/tests/day/chat/test_devices_push.py의world병원범위 단언1곳, app/lib/ui/shell.dart의설정차례, app/test/ui/notification_ui_test.dart의새위치단언2개뿐. 새범위/다른취약점상상추가0, 기존WARN해소·정정회귀만. 제품은원형77173cf8/SPEC005b0f71ec3대로계정→알림→로그아웃. 버튼동작/글자/계정표시동일, phone/iPad PNG4장중대표직접열어확인. 코디가서버23파일hash확인해39a3dad8로commit했으나push아직0, 앱미커밋. 기존backend/app전체검수는이미끝났다.
검증은알림UITest(새순서phone/iPad)+app_flow관련만, 서버는역순 notifications→chat test_devices_push에대한작성자32pass로그와실제diff보장검토(제품변경0라DB재실행필수아님). 원한다면관련단독테스트만 기존DAY_ENV_FILE하네스 day_test/Redis15, 값출력0·실DB/서버/포트조작0. 전체787/277/native/build불필요반복0. 실제Apple/API키/시뮬레이터0.
최종 notification-final-rereview.md에PASS/WARN/FAIL·해소여부·filehash3개·명령수치·미실행정직기록, 새preambleIDs/outcome/reportpath로worker_done1회후idle.

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
