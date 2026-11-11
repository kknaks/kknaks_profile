# [planner] 룸 상세 후속 합의 SPEC·WP v5 최소 정합

너는 planner. 기존 day-app의 후속이고 맥락은 파일로 확인. spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD d6d961e9402dc4dbae69aa1c407b5a37f5571882, 코드 tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD47be2cb0ab22198e1aca27dfcdf7f273adb9adbf 둘다clean에서시작. SPEC003만편집가능(products/day/20-spec/spec-003-mobile-app.md) + profile아래보고/CLI입력. 타SPEC·공통20-spec.md/30-work.md·코드·서버·GitHub쓰기0. 하위위임/내부agent금지. 커밋/push/merge금지.
원천: SPEC003 U4/U6/U7/AC/OQ31, 최신 _RESUME.md 끝 후속UI 합의, delivery-request-v4.json/delivery-v4-approved-result.json, app/lib/ui/room_screen.dart/widgets.dart/format.dart 읽기만. user한국어만·화면문구발명0.

사용자 최신 승인 「ㅇ으 그렇게 해서 이거까지 발주하자」. 그 앞 사용자 「응 호출중도 시작 비활성화 로 두자 / 시술 목록에는 시술경과가 메인이야 / 와이어프레임 수정안 다 그려바」와 코디가 제시한5상태ASCII 전체를 승인. 앞서기록한룸헤더/수락후호출박스도이번묶음에포함. 좁은결과계약:
1) 룸 상세 헤더: 「< 시술현황」 왼쪽, 룸이름은헤더전체폭기준정중앙(왼쪽버튼을뺀영역의가운데아님). 긴이름은안전한폭에서말줄임, 뒤로가기접근/화면들회귀0. 예약/통역등다른헤더변경없음.
2) 룸상세상단호출강조박스는미수락called행이남은호출(oc.waiting)만보임. 전부수락된호출의 「{담당의} 수락」 큰박스숨김. 부분수락/여러호출중미수락이있으면그호출의박스는유지. 목록카드·호출탭·미수락수락버튼·간호대리/원장즉시수락정책·재호출·API·서버권한그대로. 호출박스의기존정보/표시건수새집계정책도추가안함.
3) 시술목록행5상태와버튼순서(사용자확정와이어): 준비중 = 시술명 / 담당의(없으면미정) + [시작](기본비활성). 호출중 = 같은구조 + 회색비활성[시작], 행의[수락]/호출배지/호출대상·호출경과문구제거(상단호출영역에서확인). 수락후 = 시술명 / 담당의 + [시작], 수락배지없음. 진행중 = 연한DAY배경/테두리, 시술명좌/큰mm:ss우, 아래담당의·HH:MM시작 / [종료] [세로⋮], 진행중배지없음. 완료 = 회색톤, 시술명좌/「완료 N분」우(표시, 버튼아님), 아래담당의 / [세로⋮]. 완료소요N분은기존spanMin(startedAt,completedAt)표시변환그대로(새반올림정책없음); 시각누락이면허위N분만들지않고완료만표시. 진행경과는기존elapsedMmss분누적재사용(1초갱신기존Ticking), 새timer없음. 담당의/시술명은그행값만. 순서/시술수·완료수/아래[의사호출]/모두완료귀가박스/통역그대로.
버튼활성은기존서버can*/권한/요청중상태그대로. 호출중은수락전이므로시작비활성. 중요: ready_wait도KOS담당의가있으면현재서버canStart=true가능(start_block). 사용자와이어는기본비활성예시이고마지막문장「실제버튼활성여부와취소가능여부는기존서버권한그대로」까지승인했으므로 ready_wait의서버true시작가능을새로차단하지않음. accepted도canStartfalse면비활성. 진행중⋮는기존canUndoStart일때시작취소, 완료⋮는canUndoFinish일때완료취소, 기존DAY확인창/원문/권한보존. readonly사용자에게새조작노출없음.
이전목록카드2줄/원형4메뉴/DAY색/빠른통역/TW/토스트/세션/환경/API/needs/canRecall/마취는무변경. 상세마취칸mm:ss변경은이번요구아니므로현재그대로, OQ31은룸헤더부분만이번결정으로해소.

산출물: SPEC003관련절·ASCII·AC·OQ 최소정합, profile detail-polish-spec-report.md, delivery-request-v5.json(기존v4기반·same235/idempotency·version5·L3누적·기존pendingmainbaseline·새scope_delta·기존1개PR237/마지막merge보존). v4원본보존, 새WP파일원장만들지않고CLI입력만. 새원천은 d6d961e9+개정④미커밋 정직표기후코디exacthead결속. 좁은회귀AC/검증만추가, API/서버수정0. lint DAYerror0/schema0 각1회, 코드구현은독립문서리뷰후코디가발주. 완료전메일check, livepreamble정확ID/outcome/report-path로worker_done1회후idle.

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
