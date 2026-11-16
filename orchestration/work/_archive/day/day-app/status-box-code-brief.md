# [mobile] 목록 상태 박스 2줄·초단위 시간 교정

너는 day-app mobile worker. 앞 대화는 파일로 복원. /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app app/ 기존미커밋 UI위에좁게수정. root AGENTS.md·profile status-box-spec-report.md/review-status-box-spec-report.md·spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec의 SPEC003 최신개정·기존 mobile-ui-fix1-report.md 읽기. WP235v4 코디 반영 후 발주된 태스크다. 사용자 「응 일단 이거 부터 바꾸고 오자」 구현승인. 하위위임/내부agent금지, 직접 app/만, 커밋/push/merge금지.

이번정확범위 = 목록 RoomCard._nowBox 현재상황박스 4상태(시술대기/마취중/마취완료대기/시술중). SPEC의최신정의대로 항상2줄: 첫째줄 상태·시간(좌)/담당의(우), 둘째줄 첫시술명 외N개. 복수의 N은추가건수, 단수면외N개생략, 화살표/펼침없음. 진행중마취/시술 경과 mm:ss 초단위갱신(분60넘어도누적mm), 마취완료 lastSeconds÷60내림 N분. 예 「마취 중 · 12:34」「시술 대기 · 마취 완료 20분」「시술 중 ·05:24」. 스펙의대표시술/시간/담당의선택규칙한묶음지킴. 마취기준/시작시각은기존한줄서새구조로대체되어목록박스에서는그리지않음. 연보라/long빨강·시술중DAY강조·서버값/권한 그대로.
카드밖 방/고객/기타정보/수납필요 구조 그대로. 호출 _callBox·_callLine/수락·귀가·상세시술행·룸헤더·API·세션 무변경. 헤더룸가운데정렬은사용자 「기록해」라한후속이라이번수정금지. 기존미커밋 원형UI/WARN4보완은보존, 대량리팩토링0.

허용 app/lib/ui/board_screen.dart, 표시helper필요시app/lib/ui/format.dart, 해당위젯/fixture/캡처테스트최소. 시간표시변환은업무판정아님. 기존 frame/ticker의now를사용, 새timer중복추가금지. 둘째줄은 긴 시술명 말줄임 시에도 「외 N개」가 남도록 제목과 건수의 폭을 제약한다(화살표없음). 긴이름/320/599/600/iPad에서도2개행블록유지(각행말줄임허용), 담당의가긴경우상태/시간이사라지지않도록제약. 빈시술목록이면임의시술명넣지않고2행높이유지.
검증: analyze/fullfluttertest각1회, 기존캡처가능하니4상태 phone+iPad·320긴상태/이름·시간12:34/마취완료20분·시술중05:24 증거. 새테스트는대표시술집계/초갱신/완료형식 등실제불변식만. 순수디자인복제테스트불필요. 기존fix1회귀(320call버튼/시트고객/호출카운트)는보존.
산출물 profile status-box-code-report.md, status-box-evidence/{logs,screens}/, 기존before-*와manifest보존. fixturePNG는실데이터아님을명시. Flutter3.44.8 FVM사용. 최종 표준lib/main.dart 로컬debugbuild --dart-define=DAY_LOGIN_ENTRY=http://127.0.0.1:11040 --dart-define=DAY_DEV_LOCAL_ORIGIN=http://127.0.0.1:11040 --dart-define=DAY_REQUIRE_ENVIRONMENT=false --dart-define=DAY_APNS_ENV=sandbox. 기존orca-mobile-iphone UDID5C9E05C7-7171-455E-97CE-2AD2EA097F88에만재설치/실행(사용자허용지속), 최종PID와현재화면증거. 기존 사용자 로그인/Keychain/앱데이터는 보존(로그아웃·토큰삭제·simctl erase·uninstall 금지). 로그인 화면이면 그대로, 사용자가 이미 로그인했다면 기존 세션으로 복원된 현황을 그대로 두고 임의 업무조작하지 않는다. 로그인 화면을 만들려고 사용자 세션을 지우지 말 것. 자격증명검색/로그인입력/실데이터쓰기0. 서버/포트/DB/env/네이티브/서명/기타기기0. unsigneddevicebuild최종1회(캐시가능). 마이크/푸시/healthprobe추가실행불필요.
끝에메일check, livepreamble정확task/dispatch·outcome/report-path로worker_done1회후idle. 다음리뷰는코디가발주.

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
