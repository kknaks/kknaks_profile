# [mobile] DAY iOS 직원 앱 신규 구현 — 승인 SPEC003 전체

사용자가 방금 「엥 아니 머지는 마지막인데 코드 구현해」라고 명시 지시했다. SPEC PR #921은 OPEN으로 두고, 리뷰 PASS인 spec branch의 exact commit 78f3ee59c8a10e0abb1bde8896302873a46d0732와 이미 승인된 Delivery #235를 구현 기준으로 사용한다. main baseline pending은 그대로 정직하게 기록한다. 사용자 지시가 로컬 skill의 baseline-before-code 절차보다 우선이다. baseline ready로 속이거나 머지하지 않는다. 결과계약·기능범위는 변하지 않는다. 모든 merge·배포·서명·TestFlight는 마지막 사용자 지시까지 금지. 코드 PR 하나→dev, commit/push/PR은 코디만.

기준 문서 경로: /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec/products/day/20-spec/spec-003-mobile-app.md 및 spec-001-login-session.md, 인접 spec-002-procedure-board.md 및 40-architecture/mobile-deployment.md. 모두 전문을 읽는다. profile 작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/의 delivery-request.json(승인된 WP 입력; canonical 이슈 https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235), review-policy-report.md, review-wp2-report.md, review-baseline-report.md, research-prototype-board.md도 읽는다. 최신 main 기획원문과 차이는 보고되어 있으며 이번 사용자가 승인한 직접 결정이 우선이다. 그 범위를 또 미정으로 만들거나 재승인을 요구하지 않는다.

코드 트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, origin/dev=917287374723871d554f8a094610d46c39450534, app/이 아직 없다. 로컬 backend는 사용자 canonical ~/git/CENTURION_DAY(dev)의 day-local, deploy/local.env. 실제 키/비밀번호/env 내용을 출력/복사/기록하지 않는다. 사용자 포트·컨테이너·프로세스·기기 조작 금지. 다른 세션 day-procedure-board-2의 방이동·차트작성·KOS·seed는 건드리지 않는다. 프로토 /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app는 read-only.

고정 정책: UUID ID, can*·pickable·need·inbox.section은 서버값; 통역=해당 고객정보 보기직원(board view/is_admin), 간호사 대리수락 필수, 푸시 대상=기존호출(모든의사→병원원장전체/지정→그원장), 관리자추가·호출자제외 신설 없음. 상담사호출 향후만. D1 로그인 환경연결 backend는 승인예외, D2 APNs발송/기기 서버전체·D3 통역WS/사전 서버전체는 이번구현밖, 앱소비+더블만. OQ-A1/A9/A11은 보류, 문구는 DAY·프로토 원천 그대로만 쓰고 원천없으면 빈칸/오류코드. 원문을 새로 번역하지 않는다.


먼저 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/mobile/의 role.md·rules.md·skills.md·tools.md·workflow.md 및 코드 AGENTS.md 전문을 읽는다. 맥락 없다고 보고 브리프만 따른다. 백엔드 워커가 같은 트리 backend/·deploy 예제·AGENTS 앱주소규칙만 병렬 수정하므로 건드리지 않는다.

## 1. SSOT
위 공통의 전문 SPEC/WP가 정본. 앱 역할의 판단 기준은 서버가 업무규칙을 계산하고 앱은 표시·입력만 맡는 것이다. 별도 개념문서 없음.

## 2. 목표
app/을 새 Flutter iOS 앱으로 세운다. 로그인·병원선택·세션복원·DAY테마·폰/아이패드 시술현황·룸상세·현재 API조작·실시간·네이티브 푸시연결·통역/오디오/빠른말하기 클라이언트를 SPEC003 U1~U16과 A1~A24/A14b/A16b에 맞게 구현한다. 틀/샘플화면만으로 완료처리하지 않는다. 서버가 미구현인 D2/D3도 실제 HTTP/WS·네이티브클라이언트는 만들고 테스트더블로 검증한다.

## 3. 계약
- 고정 로그인 진입점·허용origin목록·환경칸필수·APNs환경만 build define. 데모 로그인은 prod→dev 인증을 서버가 담당한다. 앱은 75초·자동재시도0·redirect로 자격증명 전달0.
- 응답 api_base_url을 https origin으로 정규화, userinfo/non443port/path(root제외)/query/fragment 거부, release 허용목록 밖 거부. choose_hospital 대상 일치와 /me.environment 확인 전 저장0. token/api_base_url/environment/expires_at/staff_id를 Keychain의 단일 레코드로 저장, HTTP/SSE/WS/push accept는 그 대상만. 로컬 http허용은 개발 debug에서 명시 설정된 local origin에만, release에서 절대 완화하지 않는다.
- 현재 backend JSON/API를 읽고 camelCase 업무 payload vs snake_case auth 구분. SSE board/version/session_expired·지수재연결·foreground/background·401폐기. 재호출 노출=need.why call+called task+board edit. 권한은 서버와 /me 그대로.
- 네이티브 알림권한·APNs토큰 갱신·설치UUID·세션대상 등록해제·탭→룸·원장본인 수락·환경불일치무시. 서버 없음은 푸시만 pending, 앱작동 유지.
- 통역 /api/interpret Bearer WS 및 오디오·드로어, interpret-pwa 프로토콜·7언어. 빠른문구는 원천 en/ja/zh/zh-Hant/th만, vi/yue 생성금지. 사전170용어는 서버context라 앱UI/불필요한 중복시드 만들지 않는다.

## 4. 읽을 코드
backend/day/schemas·routers/api/{auth,board,calls,tasks,visits}.py·services/board 관련, backend/day/styles/app.css DAY토큰, templates 로그인·시술현황 문구, prototype lib/·ios/. 통역 프로토콜은 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md. 원본 /Users/kknaks/git/toy_pr2/interpret-pwa는 origin/main ref로만 있을 수 있으니 git show로 읽는다.

## 5. allowed_paths
오직 app/** 신규작성. app/.fvmrc 등 앱내 SDK pin 포함 가능, root설정 수정금지. profile 작업폴더 mobile-code-report.md 1개 및 mobile-evidence/ 검증증거만 작성가능. 앱에 비밀/Apple Team/실계정/하드코딩 배포주소 금지. iOS Bundle ID는 예제/사용자설정 주입가능한 임시식별자 명확히 문서화, 등록·서명값 채우기 금지.

## 6. 단계
1. 현재 FVM cache 확인, Flutter3.44.8/Dart3.12.2 캐시 사용 가능. fvm 글로벌 설정을 바꾸지 않고 앱 내부 SDK pin. iOS scaffold 생성 및 일관된 간결한 서비스/상태/UI 분리.
2. 실제 HTTP/SSE/WS/native 어댑터 및 주입가능 더블, 토큰/대상 저장 일관성부터 세운다.
3. SPEC UI전체와 DAY토큰 구현. iPhone폭에서 overflow 없고 짧은변600 기준 아이패드 격자/룸두열. 가짜 고객정보를 runtime 기본화면에 넣지 않는다.
4. 의미있는 단위·위젯검증: hostile origin/환경누락·병원응답변조·401·/me전저장0·원자레코드·75초재시도0·권한/대리수락/재호출조건·SSE parser순서/재연결·native푸시세션대상·통역7언어/WS더블/빈문구·폰아이패드.
5. app README에 설정키/명령/미구현서버/서명사용자사항 명확히. 실제설정은 나중, 구성값 부재시 오류코드로 안전하게 실패.

## 7. 금지
backend·웹·문서SPEC·옆세션 수정0. 전체복제/ceramique브랜딩/규칙재계산/공허한 TODO버튼/임의문구0. 사용자 앱/시뮬레이터/기기 실행 금지, unsigned build까지 허용. 필요 기술사항은 공식 문서/현재 패키지실물로 확인한다. 하위워커 임의발주금지. 막힘은 live preamble ask로 즉시.

## 8. 검증·보고
앱 생성 전에는 대상Flutter baseline없음을 기록. 완료 후 cd app에서 fvm flutter analyze, fvm flutter test, fvm flutter build ios --no-codesign 각1회(새실패수정시 필요한것만 반복). 실패원인·pending은 숨기지 말고 보고. 화면크기 위젯검증·네이티브 구현 실물 유무 포함, 전체 A조건별 구현파일/검증/실통합pending표를 mobile-code-report.md에 남긴다. 더블PASS는 실제APNs·Soniox·prod통합완료가 아니다. live preamble worker_done outcome필수, §9보다 최신preamble우선.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_aae94499-001a-4959-98e2-fe0f3f02961d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
