# [planner] 시술현황 상단 인박스 탭 제거 SPEC/WPv6

기존day-app후속. spec /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD4a5d4a4705b07fd66272867d85115376b1289400, code /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD4ee33f959dd561496bb8fac6db83a829d5fffb48, clean기준. 코드/worktree루트AGENTS/역할읽기. 편집허용 SPEC003 한파일(products/day/20-spec/spec-003-mobile-app.md) +profile 산출물뿐. 다른SPEC·20-spec.md·30-work.md·코드·서버/GitHub쓰기·commit/push/merge0. 하위위임0.
읽기원천 SPEC003 U2/U10/U11/수락진입점/ASCII/AC, 기존delivery-request-v5.json 및delivery-v5-approved-result.json, app/lib/ui/board_screen.dart, 최신_RESUME.
사용자: 상단「현황 / 호출7 / 시술완료2」캡처를보고「이거아직도있는데?」→코디가이3탭도없애자는뜻인지확인→사용자「응 시술현황은 카드만 보여주면 된느거 아니야?」. 코디확정안내=3개상단탭제거·기존4필터바로아래카드만/하단4메뉴유지. 이지시를실행승인으로결속, 추가질문없이좁게반영.

결과계약: 시술현황본문은연결상태줄(기존) + 「전체/확인필요/시작가능/시술대기」4개필터 +서버cards[] 카드목록만. 현황/호출n/시술완료n 인박스탭/선택상태/탭본문별도노출없음. 호출탭/시술완료탭의별도목록·완료검색UI도노출안함(다른메뉴/숨은라우트로옮기지않음). 카드격자/1열/서버순서/inbox.section4필터/2줄상태박스/카드직접수락/상세에서수락·호출·조작/푸시진입/홈4메뉴·DAY머리종/룸상세개정④ 모두유지. 수락경로는목록카드호출줄+상세상단호출박스+푸시원장본인으로남음, 직무분기/API권한0변경.
서버API·snapshot calls/doneTab 수신계약·집계/needs/can*/귀가처리0변경. 새통합목록/새정렬/완료카드를cards[]에추가안함. 기존처럼귀가대기로넘긴방문은서버cards[]에서빠지고별도완료탭을앱에서노출하지않는것뿐. 완료목록/검색재배치·새화면추가·backend변경없음. 이전v5누적성과보존, 삭제기능의옛AC·수락진입점·문서인박스대응/하단메뉴와중복설명은현재계약에맞게최소정정. U10/U11은별도탭1차범위에서빠졌음을명확히하고서버계약정의는그SPEC소유라손대지않음.
산출물: SPEC003개정⑤관련절/ASCII/AC/OQ최소일치, tabs-removal-spec-report.md, delivery-request-v6.json(v5원본보존·same235/key·version6·L3누적/pendingmainbaseline·1코드PR237/머지마지막/app만유지·현재사용자지시결속). 신규WP원장없이CLI입력만. 원천4a5d4a47+개정⑤미커밋정직표기후코디커밋결속. lintDAY0/schema0각1회. 새feature0·코드없음. livepreamble정확ID/outcome/report-path로worker_done한번후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
