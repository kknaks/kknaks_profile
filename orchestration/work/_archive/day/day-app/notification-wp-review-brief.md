# [reviewer_doc] 알림WP235 v8 입력 검수

read-only,하위위임·source/JSON/코드/GitHub/DB0. 보고 profile work/day-app/notification-wp-review.md 하나. spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEADb1260dd2 AGENTS·문서/Delivery규칙/role기존유지, profile notification-wp-brief/report/delivery-request-v8.json을 v7request/approvedresult +notification005/003링크재검수보고·실SPEC b1260dd2(005/N-A1~12·003·000/001/004)에대조. code/원천프로토77173cf8 읽기만, 현재v7미커밋모듈명은volatile interface아직확정주장0.
같은issue235/keyday/day-app·7→8정확1·L3·target+=005/baseline9692pending/mainready위조0·코드PR237/dev한개/머지마지막·iOS우선/실키설정사용자·실서버배포0. 결과=원형종/알림함/읽음/설정/SSE/원장호출발송·기존staff수신자/관리자추가·호출자제외0,chat과종분리·v7device/APNs재사용/AndroidFCM·상담사API·설정밖추가0. 과거v7non-goal/AC/verification/rollback내용(알림센터없음/원장발송밖/설정계정logout만/배지없음/board수정금지)이v8과충돌하지않게범위한정되었는지전수. code_surface/helper실제public/task/API/worker 전달경계·v7owners마감/검수후같은owners이어코드(queue)·수신자/업무/EMR/KOS·웹0변경.
중복callrowlock+queryinsertion같은tx·recall새id·커밋뒤별도알림실패격리·키/기기없음기록·설정off기록없음·전체날짜allread/ids[]0/AND·KST50밖unread·settingsallowedkind·SSE읽음·세션만료다병원/stale401·native CALL/env/hospital/tap/수락servercan*. v7skippednokey/1회retry/deadtoken새등록보존공유·코드APNs실기기pending정직·실PG/RedisE2E필수·appunit/native/analyze/build+phone/iPad원형대조·기존시술현황/chat회귀. schema기본추가0/기존0006/0007rollbackforwardonly보존·v8기능만되돌림·failclosed불변. AC A41~52↔N-A1~12 일치/검증가능.
JSON schema/model최종각1회, 판정FAIL/WARN/PASS·각fileline/jsonpath·근거영향최소정정. 코드직접수정/권한gate추가양산0. 기존head/worktree범위정직. 정확preambleID/outcome/report worker_done1회/checkack후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_4fc8346e-2c4e-4f56-a8a4-96120c073f8c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
