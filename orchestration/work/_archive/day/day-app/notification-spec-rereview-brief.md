# [reviewer_doc] DAY 알림 SPEC 독립검수

read-only, 하위위임/commit/push/GitHub/서버/기기0. 보고하나 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/notification-spec-rereview.md 만. 스펙 tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec 기존HEAD53adbd49 위 신규SPEC005+index/coverage. AGENTS/문서규칙/역할 day/reviewer 읽고 notification-spec-brief.md/notification-decisions-20261110.md/notification-spec-report.md를대조. 코드read-only /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, 프로토read-only /Users/kknaks/git/toy_pr2/cc-prototype ref77173cf8b62f0b27ec54ec4ee22e9d308b7f701e gitshow 원문.
사용자요청=채팅WPv7코드구현과알림페이지SPEC병행, 알림푸시도코드먼저/키설정나중, 기존디자인/문구유지. 후속알림별도기능005이므로003/004/000/001/002동결·표준SPEC→WP→코드순서는005내부유지. 알림전체/기존원장호출푸시까지필요기능을계약화하되상담사호출API·Android/FCM신설·운영설정·머지0. 기존 호출 수신자=해당병원 doctors목록전체/지정원장, 관리자추가·호출원장제외0. nurse대리수락권한과알림수신자혼동0. 채팅push/탭배지는종알림함과별도.
검수: 원형폰fullscreen+iPad420sheet/header99+·0숨김/list-read-all/readone/설정스위치·OS권한·기기표시 원천동작/문구대응 누락·자의변경0, 계약명확·backend서버현재0/미래제안정직. API/알림생성기록트랜잭션/중복·재호출·수락/취소/수신자격리/읽음동시성/목록페이징/SSE누락복구·늦은응답·병원/계정/세션교체, 알림tap대상없음/권한변경/원장본인native수락의현재can*재검증. 키없어skip와호출조작/알림저장성공분리, APNsretry·deadtoken·구응답새등록보존은v7재사용. deviceAPI이중작성0/모델에없는칸으로증명했다고하지않음. 새schema필요시보고하고기존000지금수정0, 실제필요구조보완을자의적별도승인양산으로바꾸지않음. 기존계약동결blob증명, 인수조건각검증가능, 실키/실기기pending정확.
판정PASS/WARN/FAIL, 지적당파일줄+원천근거+영향+최소정정. lint strict1회DAYERROR0/무관분리, gitdiffcheck/경계. 원천매핑전체와핵심코드/규칙대조로사실판단, 코드/문서직접고침0. 정확preamble task/dispatch/outcome/reportpath worker_done1회/checkack후idle.

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

## 이번은 정정 재검수만
notification-spec-fix-brief.md/fix-report.md 현재005문장에W1·W2/원천/AC대조. 고정기존005외003/004/000/001/002 blob5개동일,005stable·index정합확인. readids빈배열0/AND/전체날짜/읽음SSE적응·read>0·dedup기존호출잠금tx기본/migration선택조건·재호출새id 구분. 새정책/권한/문구/API0. 보고 notification-spec-rereview.md 한개, lintstrict최종1회DAY0/diffcheck. 코드다른워커구현중아무변경0, 정확worker_done1회후idle.
