# [mobile] 시술현황은 필터+카드목록만
app/만직접수정·하위위임/commit/push/merge0. code /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD4ee33f959dd561496bb8fac6db83a829d5fffb48 clean. rootAGENTS/역할읽기. 원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/tabs-removal-spec-brief.md/tabs-removal-spec-report.md/tabs-removal-spec-fix-report.md/review-tabs-removal-spec2-report.md(최신PASS) 및 spec tree SPEC003개정⑤최신. 코디WP235v6현재사용자지시승인결속후발주. 사용자「응 시술현황은 카드만 보여주면 된느거 아니야?」=상단3탭제거승인.

범위: BoardScreen상단「현황/호출n/시술완료n」3탭제거, 선택상태와3본문용IndexedStack/호출탭/완료탭별도목록·검색UI/미사용화면코드정리. 본문은기존연결상태줄+4필터(전체/확인필요/시작가능/시술대기)+서버cards[]카드목록만. 기존폰1열/iPad격자/서버순서·inbox.section필터/카드2줄상태/목록직접수락·상세진입·pushroute·room상세개정④/4개하단메뉴·DAY/종모두유지. 숨은대체탭/새메뉴/완료카드합치기/정렬규칙/새문구0. 호출수락경로는목록카드+상세상단+푸시원장유지, 직무별수락/권한/서버can*/needs그대로. 서버API·BoardSnapshot.calls/doneTab계약수신/모델/통신·귀가처리0변경. 상세/마취/통역/세션/푸시/native/backend/env0변경.
허용 app/lib/ui/board_screen.dart·관련ui/capture테스트최소·app/README.md의이번UI서술만필요시정정. public모델unused필드삭제등범위확대0. 테스트는옛탭전용기대만정정하고기능회귀는카드/상세진입으로검증. 화면제거를이유로직무별수락/세션race/푸시/환경관련회귀테스트삭제하지않음. 캡처옛호출/완료tab진입시나리오는대체루트발명하지말고제거/의미맞는카드장면으로정정, docs도범위에맞춤.
검증 analyze/fullfluttertest/unsignediosbuild최종수정뒤각1회. 새복제테스트불필요, 필터/카드수락/상세/메뉴보존관문·시각으로증명. phone+iPad+320상단3탭없고4필터바로카드, 빈판/읽기권한/수락권한카드/상세개정④회귀보존. fixture출처명시·원본프로토실파일읽기전용. profile tabs-removal-evidence/{screens,logs}/·tabs-removal-code-report.md에변경/명령수치/미결.
마지막표준lib/main.dart로컬debugbuild --dart-define=DAY_LOGIN_ENTRY=http://127.0.0.1:11040 --dart-define=DAY_DEV_LOCAL_ORIGIN=http://127.0.0.1:11040 --dart-define=DAY_REQUIRE_ENVIRONMENT=false --dart-define=DAY_APNS_ENV=sandbox, 기존orca-mobile-iphone UDID5C9E05C7-7171-455E-97CE-2AD2EA097F88에install덮어쓰기/launch만허용. 사용자로그인/데이터보존(uninstall/erase/logout/토큰삭제0), 로그인입력/자격증명검색/업무쓰기/다른기기/서버·포트·DB·env·서명/TestFlight0. 최종PID·현재화면캡처·실행인자로그보존(비밀없음), 실데이터고객/직원실명보고본문에복사안함. native변경없으면Swift47반복0, healthprobe불필요.
완료전메일check, livepreambleID/outcome/report-path로worker_done한번후idle. 코디가독립리뷰발주.

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
