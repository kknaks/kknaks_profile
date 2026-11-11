# 알림v8 앱 리뷰 W1 설정칸순서 최소정정
너는mobile작성자다. notification-mobile-review.md W1을읽고 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS준수. 허용 app/lib/ui/shell.dart 설정탭조립 및 관련 app/test/ui/notification_ui_test.dart·test/capture/notification_capture_test.dart(필요때만), profile notification-mobile-fix-report.md/PNG. 설정을 SPEC005/프로토77173cf8 원형대로 계정→알림→로그아웃 순서로맞춘다. 기존계정표시/로그아웃모양/권한/동작·새문구/새디자인0, 최소Widget배치만. 순서를보장하는관련시험과폰/iPad설정PNG원형대조로확인. analyze·관련notificationUITest/셸app_flow회귀만, 전체277/native/build무의미반복0. 실제버그범위외제품변경0·backend/spec·실키/Apple/서버/시뮬레이터/실계정·commit/push/하위위임0. 기존테스트없으면위젯위치기반순서단언추가하되구현을복제하지않는다. 전후hash/검증수치/PNG/변경경계notification-mobile-fix-report.md보고. 새preambleIDs/outcome/reportpath로완료1회후idle.

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

