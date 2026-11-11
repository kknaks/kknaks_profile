# 알림v8 서버 리뷰 W1 시험 격리만 정정
너는backend작성자이며 방금 app read-only리뷰도완료했다. 새로운task는 backend최소정정이다. notification-backend-review.md W1을읽고 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS준수. 허용파일 backend/tests/day/chat/test_devices_push.py 하나와 profile notification-backend-fix-report.md/필요로그뿐. 276~277 Notification테이블전체비어있음단언을 해당world병원/계정범위로좁힌다. '채팅은알림함에행을안쓴다'원래보장유지·단언삭제/약화0. 제품코드/모델/migration/app/spec/실env/서버기동/키/Apple/commit/push/하위위임0. 역순 notifications 먼저 + chat의 해당파일로회귀재현, ruff해당파일. 전후파일hash·변경1구절·제품코드변경0·테스트수치 보고. 실PG/Redis는기존DAY_ENV_FILE하네스 day_test/Redis15만·값출력0·다른pytest없음을먼저확인(리뷰어이미시험완료). 전체787반복0. 새preambleIDs/outcome/reportpath로완료1회후idle.

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
