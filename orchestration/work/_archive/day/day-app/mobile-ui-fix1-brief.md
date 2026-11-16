# [mobile] UI 독립리뷰 WARN1~4 보완 + iOS 로컬 읽기전용 연결 probe

역할/원천/경계는mobile-ui-code-brief.md그대로. 코드트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app 시작0b776e90위UI미커밋. 사용자진행승인유지·app/만. 하위워커/내부agent금지.
읽을것 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-mobile-ui-report.md 전체·mobile-ui-code-report.md·기존브리프. 최종review PASS(WARN4), 184tests/analyze0/native47/빌드OK 재현. 코디도analyze0/native47확인. 새로운독립리뷰에서4탭가시성은최종PNG로확인해해소됨(더고칠것없음).

## 1. WARN1 캡처fixture
카드에열린호출이있으면동일call이calls[]에도있도록실제APIshape정합. 현재인박스「호출0」증거를정상카운트로갱신. 전체캡처fixture/특정called두state 모두. 실제호출목록/완료탭도아래포함.

## 2. WARN2 폰시트머리
SPEC U5정본대로폰도방·고객이름(where)표시. iPad/간호대리시트와일치. 새문구아님(기존서버값), 코드1곳최소수정. 긴이름320폭에서ellipsis/줄바꿈가독성확인, UI새설계금지.

## 3. WARN3/4 시각증거
기존시각캡처테스트에 320긴고객명/긴한글발음/긴시술명 목록+상세, 599/600경계화면, server canStart=true인켜진[시작]카드, 호출탭/시술완료탭 phone+iPad캡처 추가. screenshot은실제backend데이터아닌fixture로분명히표시, server의cards/calls/doneTab정합지킴. Ahem아닌실글꼴. 눈으로잘림/겹침확인. 원형디자인/4행/4탭보존. 코드기능확대없음.

## 4. iOS 로컬network probe — 읽기전용/자격증명없음
호스트curl200만으로앱네트워크확인을대체하지않고, **같은iPhone시뮬레이터의앱프로세스에서 HTTP GET http://127.0.0.1:11040/health/ready**를한번보내200인지확인. 자격증명/Keychain/로그인/업무쓰기/서버재시작0. publichealth만.
권장: profile mobile-ui-evidence/probe/ 안 검증전용Dart entrypoint(코드아닌증거)로같은앱네트워크IoTransport/HttpClient를사용해GET하고상태/건수만출력또는앱sandbox의probe자체파일로기록. fvm flutter run --target=<검증전용entrypoint> --no-resident -d기존UDID로실행가능. 소스의새production debug/demo플래그/화면/route추가금지, app/lib/main.dart수정금지. origin은--dart-define으로. native ATS/Info.plist예외0유지. 완전히분리된검증target이며출력확인후**반드시표준 lib/main.dart 타깃 로컬debug빌드로재설치/실행해실제DAY로그인화면켜둠**, probe UI남기지않음.
GET200이면앱→로컬publichealth실통신검증일뿐로그인/인증통합성공이라고쓰지않음. 네트워크가막히면원인/오류만보고하고release보안을완화하지않음. 새패키지추가없이가능한방법우선. 테스트용파일은profile증거에만, 제품코드엔없음.

## 5. 검증·보고
코드변경은폰where한곳+실제드러난필요수정/테스트fixture에제한. analyze/fluttertest/캡처재생성; iOS소스UI수정있으므로최종unsignedbuild와simlocalbuild(표준main)1회. native변경0이면Swift47재반복불필요. 서버/스펙/실env/서명/계정/포트건드리지않음. 새probe/캡처별출처·실명령·수치·최종실앱PID·스크린샷·로그인미실행을 mobile-ui-fix1-report.md에보고. evidence는기존폴더사용하되최종로그/PNG구분·이전독립리뷰보고서보존. 커밋/push/merge금지.
수정끝에메일읽고livepreamble ID로worker_done한번·idle. 다음재검수는코디가발주.

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
