# [planner] DAY 알림 Delivery235 v8 입력

이번은005+003연결SPEC독립검수PASS뒤의WP단계, 코드v7는동시에구현/검증중. spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEADb1260dd210bf7bc0d05a49dc4160cd47689e432e, 사용자문서/역할·AGENTS/delivery/document규칙유지. SPEC005+003알림연결,000device/notification설정모델·001/004읽기, 프로필 notification-decisions-20261110.md/005spec보고·리뷰·정정·재검수+003link리뷰/재검수, delivery-request-v7.json/delivery-v7-approved-result.json 및 WP리뷰를먼저읽는다. rootREADME/20-spec/30-work읽기. 코드day-app currentbaseb6c034bf위backend/mobile dirty구현중(읽기만·권한/설정값출력0), 원천프로토77173cf8읽기만.

편집허용profile work/day-app/delivery-request-v8.json/notification-wp-report.md 둘만. 기존JSON/스펙/코드/GitHub/receipt/commit/push/merge/하위위임0. 입력JSON일뿐canonical원장은Issue235. samekeyday/day-app·same235·v7→8정확1·L3·한codePR237/dev·specPR921/main·merge마지막·iOS우선·실키/서명사용자. latest fetchedorigin/main9692 exactbaseline pending정직(현재003004005main없음·000001draft), 새fetch/변화있으면코디보고. 005/003구현원천b1260dd2(005commit0d0ba25f+링크b126), 채팅v7의구현/검증기준53adbd49은회귀원천으로보존. target_specs005추가/기존누적영향ID정직. 계획digest직접생성0/승인대리0. 사용자제품결정원문결속, 최종WP새approval은코디가구체Issue만든뒤받음(너는승인claimX).

결과추가=알림함폰fullscreen·iPad420sheet/종unread99+·0숨김/읽음·모두읽음/설정원장호출스위치·OS권한안내/알림SSE/원장호출·재호출후알림행·APNs. 같은병원현재원장목록전체/지정원장, 관리자추가/호출자제외0. 본인계정+현재병원알림만, 설정은기존accountglobal모델, 상담사호출API/띄우기/AndroidFCM/임의설정다른칸/발행·서명실설정0. 기존chatpush/메뉴badge·배너와종알림중복집계0. commondevice/APNs/retry/deadtoken은v7재사용하고다시만들지않음. 기존3탭제거/시술현황/통역/대리수락·native호출수락회귀.

v7copy후모순전수점검: 전체알림함/원장호출발송non-goal·헤더종배지없음/누름없음·설정계정logout만·D2기기외채팅만·임시API0/호출수신자정책 조건을새v8추가와충돌없게정정. 이전v1~v7기능/AC유지하면서v7이아직진행중인것정직,누적완료수치지어내지않음. title는최종기능간결. scope_delta v7contract/plan digest정확.

실행계획: 현재backend/mobile owners가v7수정·검수/계약정합을닫은뒤각자005를이어구현(같은app/backend동시두writer0). 코드surface새notifications schemas/dtos/query/service/API/전용SSE/notification_settings·공통pushadapter재사용+원장호출서비스/공용router액션커밋후hook(필요최소board.py영향허용,업무규칙/EMR/outbox변경0), public router등록/필요task, 테스트·문서; app notifications UI/controller/API·종배지·settings알림칸·push tapping/read-callId/currenthospital/native category. 쓰일파일현재code읽어정확히하되미완성코드interface는volatile startingpoint·확정은v7owners보고로. schema기본추가0(DoctorCallrow잠금+조회후쓰기동일tx로call/account1회). 새로운색인선택하면SPEC000/migration승인선행이라기본X. 콜본체transaction은불변,실패격리/알림성공과push실패분리,rollback기능만revert/기존0006·0007및model남김, 설정off시행/푸시생성안함source, 임의failopen0. 배포설정실값/프로세스0.

AC/review: 005 N-A1~12매핑·커밋뒤훅중복실행/실제PGcallrow경합·recall새id·원래행유지/권한·비활성·같은계정다병원·다기기API와SSE도중세션죽음·읽음ids[]0/둘다AND/키둘다생략all전체날짜·todayKST50limit외unread·setting_not_allowed/글자출처. APNs키없어도기기없어도이력저장,기존statusskip/no-key화면호출성공보존·retry1회/deadtoken새등록보존·hospitalId/env/native본인수락guards/알림tap없어진룸·권한변경오류원문. 일별자정 unread재동기화·페이지일관은원천계약기준. SSE전용/헤더범위/foreground/resume·stale401가새session안지움·원형phone/iPad시각근거. API4+SSE 실제PG·Redis스크래치E2E·앱tests/analyze/native/unsignedbuild필수, realAPNs/userkeys실기기pending정직. 코드전체가능기능을mock만으로완료금지. 기존tests전체반복은source변경필요검증만.

모든새AC+non-goal/targetdelta/review_surface/code_surface/verification/rollback서로일치. 시술현황can*/순서/수신자업무규칙/웹frontend0변경. 베이스전체diff범위v1∪v7∪v8구분, 이전rollback/migration없음옛문장미한정남기지않음. 문서003연결은이미검수커밋되었고코드착수선행조건충족, main선머지요구0. schema/model최종각1회ERROR0,보고전후변경경로·인수조건매핑·동시구현경계·실제OQ·미실행. 정확preamble/outcome/report worker_done1회/checkack후idle.

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
