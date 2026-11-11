# [reviewer] DAY 앱 UI 교정 + 로컬 API 소비 독립 코드·시각 검수

너는DAY reviewer. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/ 문서와코드AGENTS읽음. 하위워커/내부서브에이전트금지. read-only코드검수, 보고만작성.
대상 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, 시작기준0b776e900cc229f3a447cb0e937400534b6bc709 위app/변경. 기존D1backend는변경대상아님. 기존PR237→dev·merge없음.

## 1. 먼저읽기
스펙 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec/products/day/20-spec/spec-003-mobile-app.md exactcdde456af1e38a988470b5144278cbb04360341f, SPEC001환경·보안. profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/ 안 mobile-ui-code-brief.md(현재계약), mobile-ui-code-report.md, delivery-request-v3.json, review-local-alignment2-report.md, ui-spec-brief.md, research-prototype-toasts.md, 이전mobile-fix1-report.md/review-mobile-code2-report.md. 원본prototype /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app read-only. 실제localAPI source /Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2 @a1c90b9d·옆SPEC002@e421b77b read-only.

## 2. 기능·계약검수
13UI항목전체커버표, 6API소비정합. 원장본인수락=picker안뜨고로그인staff.id, 간호사proxydoctor선택, 3진입점/권한; needs[]서버5상황(앱재계산없음), canRecall노출/권한, lastSeconds→분표시만, pickable서버값/호출시트선택정합/재호출target고정, 취소확인요청없음취소와정확경로, 완료home머리중복없음/서버집계보존, 토스트2xx자기조작/이전세션·떠난화면late결과없음, TW새고객언어초기화와수동변경WS/TTS일치.
D1/API보안·세션race·popup lifetime 회귀중점: shell탭별Navigator/로그아웃시모달제거, 이전세션늦은401새세션삭제없음, 토스트늦은callback·disposednotify없음, route수명/마이크stop, origin/redirect/release규칙유지. debug로컬http가release에열리지않음·http주소소스하드코딩0·ATS예외빌드산출물/ignore로컬뿐. D2/D3/D5서버미구현정직·가짜배지/데모실흐름없음. allowed_pathsapp/만.

## 3. 시각검수 필수
profile ui-reference/*.png원본13장과 mobile-ui-evidence/ 결과PNG를직접열어대조(정적코드추정으로눈검수PASS하지않음). 사용자ASCII가이미지보다우선: 고객카드는방/수납→이름발음→바이탈→상태4행. 나머지둥근카드/진행중강조/완료아래회색/버튼DAY색/세로⋮/원형통역드로어/라운드칩/큰마이크/4탭·종. 원본teal은DAYblue로바뀌는게정상. 원본이미지의내원현황5번째탭은추가하면FAIL. 상태완료정보임의0/2줄추가금지. 목록·상세긴시술명320폭및iPad600·폰599overflow/잘림/시트하단4탭보임정합확인.
fixture렌더PNG는fixture임을표시해야함, 실제local인증/업무쓰기미실행을통합PASS로주장하지않음. 실제Simulator로그인화면증거와위젯상태PNG구분. 픽셀숫자취향은결함과구분하되사용자디자인지시누락은실질결함.

## 4. 검증·보고
mobile보고수치를그대로믿지말고gitdiff·필요핵심테스트직접실행(무관전체backendtest금지, 앱테스트는의미있는회귀/직접probe). 실행이기존모바일워커와겹치지않도록완료후검수. 실제앱/서버/기기UI조작은하지않고증거PNG만읽기. 서버/DB/계정/토큰/포트조작금지. 새테스트probe가필요하면profile임시증거폴더·app파일수정금지.
보고 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-mobile-ui-report.md 한개+read-only검증로그만. PASS/WARN/FAIL, 각지적file:line+spec+재현,13UI/6API표,직접열어본PNG목록·실물에서만날자리·남은통합의존. 별도정책/문구/번역/서버기능발명금지. 수정은mobile에게돌림. livepreambleID우선·마지막메일확인후worker_done한번·idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_1d5db035-7383-46d1-97ae-2e65e50e3927 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

추가 검수 지점(코디 중간 피드백): mobile후속 msg_e7a53096d7c3(run bool오용), msg_85a0f1c0bf92(숨은탭/route late응답), msg_839ac2566c65(숨은드로어 micstop), msg_ecc006fe5ddf(통역드로어하단탭), msg_3e1abad18a7e(호출sheet하단탭/취소footer)의 최종실물 반영 확인. 중간PNG는old일수있으니보고서최종캡처목록/시각도확인.

최종보고후 코디 직접 PNG 재확인: phone-interpret-drawer의4탭은이제보임. phone-doctor-call-sheet-empty는취소footer추가됐으나4탭이여전히안보이는것처럼보임(이미지780x1688). 호출시트·간호수락드로어도원본처럼탭바가보이는지독립적으로확인. 중간판으로오인하지말고실제최종PNG/코드시각대조요망.
