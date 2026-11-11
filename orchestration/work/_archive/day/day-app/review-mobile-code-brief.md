# [reviewer] DAY iOS 앱 전체 코드 독립 검수

너는 day reviewer다. 앞맥락없음. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/의 role.md·rules.md·skills.md·tools.md·workflow.md와 코드 AGENTS.md 읽기. 작업트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, origin/dev=91728737기반. backend D1은 별도독립리뷰 PASS(보고서 참고), 이번주대상 app/** 및 D1↔앱계약이다.

## 1. SSOT
문서트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec exact SPEC commit78f3ee59c8a10e0abb1bde8896302873a46d0732의 SPEC003 전문(610줄)·SPEC001 환경연결전문·인접SPEC002 업무규칙. profile 작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/의 day-app-app-brief.md, mobile-code-report.md, delivery-request.json(승인WP), implementation-user-direction.md, review-backend-code2-report.md. 실제프로토 read-only /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app, 실제API backend/day/routers/api·schemas·services 및 DAY웹토큰·문구원천.

## 2. 권한·경계
사용자“머지는마지막인데코드구현해”로미머지SPEC기준구현승인. #235 plan승인유지·SPECbaselinepending그대로·#921OPEN. 이를결함/승인부재로재질문금지. codePR하나→dev, 모든merge/배포/서명/TestFlight금지. D1만backend허용예외; D2/D3서버전체는범위밖이며앱HTTP/WS/native실경로+더블검증만. 방이동/차트작성/seed는옆세션. OQ-A1/A9/A11보류·UI문구창작0.

## 3. 핵심검수
- U1~U16/A1~A24+A14b/A16b의구현·테스트를실제파일로대조. 빈shell/TODO/가짜성공/독립모형테스트만으로PASS처리금지. 실제UI→controller→HTTP·SSE·native·WS/오디오로이어지는지.
- 로그인75초/재전송0/redirect0, release환경두칸필수·httpsorigin/allowlist/정규화엄격. unknownenv/부분필드·staffUUID/expiry누락·깨진Keychain레코드경계도검토. choose_hospital환경+origin일치·/me환경일치전저장0. token/base/env/expiry/staff단일record원자저장, 복원/만료401/SSE만료는전체폐기, 오프라인은유지. 로그아웃중이전비동기요청이새로그인세션을저장/삭제하는경합확인.
- 기존day-local dev응답의환경칸없음/환경만있음은 명시개발fallback으로만소비, release는완화0. buildconfig는주소입력UI없고비밀없음.
- 권한boardview/edit/accept,is_admin,서버 can*/pickable/need/inbox.section/순서 그대로. 대리수락doctorStaffId·본인기본값·재호출needcall+called+edit, 마취/시작종료/취소/귀가/읽기차트현재API. 이중탭1회·409/오류토스트·kos_failed중복0.
- SSE첫board/version/session_expired·UTF8/멀티라인·끊김/백오프재연결/앞뒤전환·자원정리, 오래된subscription이새세션을지우지않는지.
- push기기권한·installUUID·등록/갱신/해제모두세션대상,400/401은푸시만실패,다른env알림무시·탭→룸. 실제Swiftcoldstart/background수락경로·큐/Keychain정합·현재staff본인·토큰보존/401삭제·새세션삭제경합·redirect0·releasehttp금지. 순수Swift테스트가실제경로에서호출되는지도확인.
- 통역boardview면코디상담도가능/권한없으면WS미전송, Bearer/target/7lang/대만홍콩구분·PCM/음성/반이중·에러종료/foregroundbackground·빠른문구원문5언어만/vi,yue없음·사전UI없음. D3서버검증은못함을정확히기록.
- DAY토큰/로그인브랜드/문구원천확인,폰짧은변600경계·iPadgrid/두열/팝오버·좁은폭overflow·클릭시실제action/disabled유무,빈화면문구발명0.기기실행없이widget검증·코드검토. 기본Flutter브랜드/기본demo화면잔재0.

## 4. allowed_paths
코드/스펙모두read-only. profile작업폴더 review-mobile-code-report.md 보고서1개만생성. 수정/commit/push/PR/서버·기기·시뮬레이터실행/실자격증명읽기금지. 의존성의공식문서/패키지실물확인은필요하면가능. 하위워커발주금지.

## 5. 검증
앱워커가실행한analyze/test/unsignedbuild/native검증증거를읽고필요한관문1개는독립실행. 예 fvm flutter test와tool/native_logic_test.sh. 깨끗한검증을근거없이반복/확대하지않는다. 신규결함은파일:줄+SPEC/WP+재현/실제영향. 보안/업무회귀는FAIL, 단순코드선호로범위확장금지.

## 6. 보고
PASS/WARN/FAIL·차단여부·각AC구현/테스트대응누락·직원이실물에서만날문제자리·실서버통합pending을구분. 사용자설정값없음 자체는코드착수/빌드결함아님. 서버미구현을앱완료로속이지않기. 수정은mobile원워커가수행한다.

## 7. 금지
Apple계정/실기기/운영데이터/포트조작0. 서명없는빌드까지이미허용되어있으나리뷰에서재빌드필요하면구체이유먼저판단. 결과계약변경·문구/번역신규작성0.

## 8. 완료통신
보고서는한국어. live preamble task/dispatch/핸들·worker_done outcome이아래legacy블록보다우선. backend결과는이미PASS지만통합계약불일치는보고가능.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_800d77f0-3654-4902-9baa-4f95bdb06d7b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
