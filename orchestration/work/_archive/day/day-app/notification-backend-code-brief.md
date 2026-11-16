# [backend] DAY 알림 v8 서버 구현
작업 tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, branch kknaksss/day-app, 시작 head 3aaa97806684b8cea7f7fb777adbcdcff7ae0de6. 루트 AGENTS.md 및 연결된 규칙, profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/의 해당 역할 문서를 먼저 읽어라. 새 맥락이므로 아래 원천·앞 보고를 먼저 읽는다.
승인 = delivery-v8-plan-approval.json + delivery-v8-approved-result.json(plan-approved·execution ready), 사용자 「응 진행하고 구현하는동안 우리 ios 개발용 푸쉬 알림 받을까 ?」. request는 delivery-request-v8-execution.json(원 delivery-request-v8.json의 계약/digest 완전동일·완료된 과거 실행기록만 정리). 알림 WP 독립 재검수 PASS = chat-permission-spec-wp-rereview.md. 문서 원천 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec exact b0f71ec312548a8dd60c70e51ac68374b84fb906 products/day/20-spec/spec-005-notifications.md 전문, adjacent003/004/000/001. main9692e1fb에는 새SPEC미머지라 baseline pending, 사용자 마지막merge지시로 선merge 요구0. latest fetched code dev91728737, code tree clean. v7채팅 검수/정정/커밋완료, 앞으로 v8만 변경.
프로토 read-only /Users/kknaks/git/toy_pr2/cc-prototype git show 77173cf8b62f0b27ec54ec4ee22e9d308b7f701e:procedure/app 및 back. checkout/pull/원본편집0. 원천화면·문구 유지, DAY결정이 우선. commit/push/PR/merge/하위위임0. 실키/Apple계정/서명/실env/서버재시작·migrate·seed·실계정조작0. profile 보고/증거만 쓴다. 다른 writer영역 dirty 정리/stage/reset0. 기존채팅·로그인·시술현황·통역 회귀0.

읽을 앞 산출: chat-backend-code-report.md / chat-backend-fix-report.md / chat-backend-rereview.md / chat-backend-lint-fix-report.md / chat-mobile-code-report.md(소비 경계만). 네 소유 = backend/ 알림 router/service/queries/dto/schema/errors·public조립·tasks, v7 APNs/기기/푸시 공통화에 필요한 최소부분, services/board.py 및 routers/api/board.py는 호출/재호출 커밋뒤 훅만. 설정명·배선 최소변화시 deploy 예시/scripts/tests 허용하되 실값0. 모델/migration 변경0이 기본. app/·웹·스펙·EMR/KOS·호출/수락 업무규칙·응답·outbox 변경0. migration0006/0007/기존 device원칙 무변경. 새 API권한키나상담사호출/Android/FCM0.
구현관찰: GET notifications(내계정/세션병원/오늘KST 최신50·unread는50밖포함), POST read(ids[]0·ids/callId AND·모두읽음=두칸없음 전체날짜·실변경수·동시읽음원자적), GET/PUT me notification-settings(병원 원장목록에 본인 있으면 doctor_call·비원장빈목록·기본true·계정전역설정·setting_not_allowed). SSE 전용 notifications/stream은 계정+병원, Bearer·세션재검증/기한/1h·notification unread·바뀐읽음>0에도 발행·재연결초기재전송0. Redis SUBSCRIBE 확인은 HTTP머리 전에, close/cancel/no-listener 누수0(v7교훈).
호출/재호출 성공커밋 뒤만 알림처리. 전체는그병원 활성원장목록 계정전부·지정그원장, 관리자추가/호출자제외0. 설정끈계정은 notification/pushlog0. 기기/키없어도 notification 기록. doctor_call 행잠금 안 조회+쓰기 한tx로(call,account)1회(새unique/migration0), 재호출은새callid라앞행보존 새행. 생성/읽음커밋 뒤 unread SSE. 알림실패는 호출응답/판조작성공을 뒤집지 않는다. 네트워크/파일/외부API를 업무tx안에서 기다리지 않는다. 공유push는 v7 apns/devices/retry/deadtoken/logging 재사용, 동일발송코드복제0. 원장payload env/hospital/visit/call, 민감고객이름0, CALL은기기세션 board.accept edit만, 만료0. 죽은토큰늦은결과 새binding안삭제. 기기 세션병원=호출병원·유효세션/활성직원재확인·키없으면 skipped_no_key. 후속작업중복과 호출훅재시도에서 알림행/푸시중복안전 근거 보고.
검증: 기존 DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env 를 scripts/test.sh가프로그램적으로source만, 값모델출력0·day_test/Redis15만. 업무DB/day-local queue·port·process조작0. 실DB주자는이번너혼자, reviewer에넘기기전테스트종료. 두병원/다중병원계정/원장비원장/다기기 합성API·실PG행잠금동시알림생성/동시읽음·Redis계정병원SSE·APNs외부더블(재시도/죽은토큰/CALL) 및 board전체회귀. notinfra/full은변경후최종1회, ruff backend scripts·architecture·migration한head/기존모델diff0. 실Vault/APNs/Blob/사용자계정 통합 미실행 정직. 범위밖계약요구시질문, 임의정책0.
산출 notification-backend-code-report.md 및 notification-backend-evidence/: 변경파일hash·API/계층/원천·테스트수치·committed hooks정확위치·공유push추출경계·앱전달계약차이0·설정이름/실물pending. 새 preamble IDs로 outcome succeeded/failed 및 실제 report-path를 붙여 worker_done1회 후 idle.

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
