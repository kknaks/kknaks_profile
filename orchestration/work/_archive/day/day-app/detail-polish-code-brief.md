# [mobile] 룸 상세 후속 합의 구현

직접app/만·하위위임/내부agent/commit/push/merge0. /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD47be2cb0ab22198e1aca27dfcdf7f273adb9adbf clean위. rootAGENTS/role읽기. 원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/detail-polish-spec-brief.md(사용자합의전문)/detail-polish-spec-report.md/review-detail-polish-spec-report.md 및spec tree SPEC003개정④최신. WP235v5코디반영후발주됨. 사용자「ㅇ으 그렇게 해서 이거까지 발주하자」승인. 이전190pass/unsigned/native47기반회귀보존.

이번3항목만:
A 룸상세헤더: 왼쪽「< 시술현황」, 룸이름은전체헤더폭정중앙. 긴방이름/320에서도뒤로가기와겹침0·말줄임. 공유DetailHeader변경필요하면room에서만선택사용하도록기본동작보존, 통역/다른화면헤더영향0.
B 룸상세 _body 호출강조박스는 oc.waiting인호출만. 모두수락됐으면큰「원장 수락」박스숨김. 부분수락/복수호출중called남은박스유지. 상단수락버튼직무분기/재호출·목록·호출탭은기존그대로.
C 시술목록카드: 모든상태 공통으로첫줄시술명(시간있으면오른쪽), 둘째줄담당의/시각(왼쪽)+조작(오른쪽)이다. 준비/호출/수락후의[시작]도둘째줄담당의옆에둔다(첫줄제목옆이나전체행세로중앙에두지않음). 시술명/담당의/시술경과/시작·종료중심. 모든행의준비중/호출/수락/진행중 Pill배지제거. 준비중/수락후 [시작]은기존canStart/권한/요청중조건. 호출중은[수락]대신회색비활성[시작](수락전), 행내호출대상/호출경과문구제거·담당의만(없으면미정). 중요ready_wait도KOS담당의가있으면서버canStarttrue가가능하므로그활성동작보존! 진행중=연DAY강조·상단시술명좌/큰mm:ss우, 아래담당의·HH:MM시작 / [종료][세로⋮]순서, 경과분누적elapsedMmss재사용·기존Ticking. 완료=회색·상단시술명좌/「완료 N분」우(표시, 버튼아님), 아래담당의 / [세로⋮]. N은기존spanMin그대로, 시간없으면허위값없이완료만. ⋮는기존doing.canUndoStart/ done.canUndoFinish +boardedit일때만, 기존확인창/API/문구/권한보존. 실제완료/진행없는readonly에도새동작노출0.

시술숫자/완료숫자·서버순서·목록2줄상태박스·호출탭·상단대기호출·모두완료귀가박스·통역/마취영역·세션/API/환경·푸시0변경. 폰/iPad원형DAY스타일, 긴시술명/긴담당의/320/599/600겹침0·시간/더보기잘림0. 아이패드헤더의전체폭은룸화면콘텐츠헤더폭기준(레일제외). 화면새문구/아이콘/패키지발명없음.

허용 app/lib/ui/room_screen.dart, 꼭필요하면ui/widgets.dart/format.dart, 관련ui/capture테스트최소. 먼저git상태/base확인·기존변경있으면덮어쓰기0. 검증 analyze/fullfluttertest/unsignedbuild각1회(코드최종수정뒤)·기존native변경없으면반복0. 테스트는새계약불변식(호출박스전체수락숨김/부분남음/행수락요청0·disabledstart/readyservertrue/role권한/더보기취소/centergeometry)위주만.
시각캡처최종phone+iPad5상태/320긴제목담당의/부분수락·모두수락/헤더중앙과좌뒤로가기. fixtures는실데이터아님명시, 원본재생성불필요장면은반복안함. profile detail-polish-evidence/{screens,logs}/ 및detail-polish-code-report.md에최종검증/변경/남은것.
마지막 표준lib/main.dart 로컬debugbuild (--dart-define=DAY_LOGIN_ENTRY=http://127.0.0.1:11040 --dart-define=DAY_DEV_LOCAL_ORIGIN=http://127.0.0.1:11040 --dart-define=DAY_REQUIRE_ENVIRONMENT=false --dart-define=DAY_APNS_ENV=sandbox) 기존orca-mobile-iphone UDID5C9E05C7-7171-455E-97CE-2AD2EA097F88에덮어설치/install/launch만허용. 사용자로그인/앱데이터보존(uninstall/erase/logout/토큰삭제0), 로그인입력/자격증명검색/업무쓰기/실서버조작0. 현재복원화면·최종PID기록. 새healthprobe/서버재시작0, 서명/TestFlight·다른기기0.
완료전메일check·livepreamble정확ID/outcome/report-path로worker_done1회후idle. 다음review는코디가발주.

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
