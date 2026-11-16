# [mobile] DAY iOS 앱 독립리뷰 F1·W1~W9 수정

너는 원 mobile 워커다. 앞 맥락이 없다고 보고 아래 브리프·현재 파일로 진행한다. 코드 트리와 역할/계약은 뒤에 포함한 원브리프 그대로다. 새 Task/Dispatch는 live preamble만 사용한다. 기존 구현은 끝났지만 독립리뷰가 FAIL이므로 수정과 재검수까지 진행한다.

## 먼저 읽기
profile 작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/의 review-mobile-code-report.md 전문, mobile-code-report.md, 현재 app/**. 원 SPEC/WP·사용자 “머지는 마지막인데 코드 구현해” 지시 유지. backend D1은 6c6b9d13으로 커밋/독립검수 PASS이며 수정 금지. 앱은 아직 untracked다. 새 기능·문구·번역·서버 변경을 추가하지 않는다.

## 수정할 것 — 전부 실제 동작과 회귀 테스트로 확인

F1. 이전 세션의 늦은 응답이 새 세션을 지우는 두 재현을 막는다. PushCoordinator·BoardController·SessionController와 app.dart 배선을 같이 맞춘다. 세션 끝 콜백은 요청한 세션에 결속하고 현재 세션이 같을 때만 저장소/화면을 지운다. 성공 경로뿐 아니라 catch/마지막 상태 갱신도 동일성을 확인한다. dispose 이후 board.run의 알림/콜백을 무시하여 disposed ChangeNotifier 오류를 막는다. 늦은 로그아웃/복원 결과도 새 로그인을 덮어쓰지 않는지 확인한다. 재현 두 건과 늦은 성공·오류·중복 종료를 실제 클래스+app.dart 배선 위젯/통합 더블로 검증한다.

W1. 등록 401은 동일 세션 /me로 확인한다. /me가 유효하면 앱은 유지하고 푸시만 pending, /me도401이면 그 세션만 기존 U12 종료. /me 네트워크/5xx는 세션을 지우지 않는다. 모든 await 뒤 세션 동일성 검사. 이 방식은 기존 SPEC §3의401세션처리와 A24/WP A10의푸시만실패 의도를 함께 만족하는 기술 처리다. 사용자 정책을 다시 묻거나 SPEC/승인계약을 바꾸지 않는다. README/보고에 구분을 적고 테스트한다.

W2. Keychain 저장 예외(PlatformException 등)는 로그인/병원선택에서 처리하여 busy를 반드시 풀고 저장된 세션을 부분 성공으로 다루지 않는다. 원천 문구가 없으므로 keychain_save_failed 같은 실제 오류 코드만 사용한다. store.save 실패 더블로 /me뒤 저장실패·재시도가능·비밀노출0 검증.

W3. 로그인 send+전체본문 수신을 하나의 75초 전체 제한으로 감싼다. 헤더74초+본문지연에서도 총75초에 끝남·요청1회·세션저장0을 fake clock/slow stream으로 검증한다. 일반HTTP 제한/재시도0/redirect0 유지.

W4. environment는 dev/prod 외 값 거절. 명시 개발 legacy에서만 null 허용, release에서 누락/unknown 거절. /me staff_id는 UUID여야 하며 빈값/형식불량이면 저장/알림수락0. Swift parse의 staff_id도 같은 검증. 세션 레코드 필수 칸(특히 expires_at)의 누락/깨짐은 거절하고, 정상서버 응답 형태/개발fallback 유지. 테스트 fixture의 staff ID는 유효 UUID를 사용하되 관계없는 fixture전체를 불필요하게 갈아엎지 않는다.

W5. 통역 WS error/close/1008/연결종료 뒤 마이크/구독을 즉시 멈추고 녹음 표시가 남지 않게 한다. 새 오류 문구를 짓지 않는다.
W6. mic.start await 도중 닫기/언어변경/restart가 겹쳐도 오래된 녹음이 남거나 PCM이 전송되지 않게 start/stop/dispose 순서를 보장한다. AudioRecorder를 restart마다 누수시키지 않는다. 느린 start 더블·오류 더블로 stop/dispose 호출 및 실제 상태를 확인한다. 기존 sink/WS 반이중·종료 정리도 유지.
W7. WebSocket.connect handshake 실패를 예외 문자열로만 판별하지 않는다. 현재 Dart SDK/공식 문서에서 WebSocketException의 구조화된 HTTP 상태(예: httpStatusCode) 지원을 확인하고 실제 타입으로 처리한다. 없으면 최소한의 주입 가능한 handshake adapter로 정확한 상태를 전달한다. 새 서버 API를 만들지 않으며 실제 서버없음은 pending. 기존 Bearer/세션대상/redirect금지 원칙 유지, 테스트도 임의문자열에만 기대지 않는다.

W8. 의미있는 회귀 검증을 보강한다. 서버 카드 순서 fixture를 시간/id 정렬과 다르게 만들고 UI순서를 확인. 수락·재호출 UI는 body만 보지 말고 정확한 path/메서드/요청성공까지 확인해 404로도 초록이 되는 테스트를 고친다. recall/accept/finish/undo-start/undo-finish/anesthesia-end 경로 및 실제 화면의 시작·종료·더보기·마취·귀가 핵심 동작을 시험한다. 599/600 경계·320폭 고르기창의 재호출/수락 상자 overflow도 검증. F1/W2 회귀는 위 항목으로 충분하고 구현을 그대로 베낀 불필요한 테스트는 만들지 않는다.
W9. 지정 호출 원장이 현재 doctors 목록에 없으면 기본 선택하지 않는다. 유효한 목록 의사를 고르기 전 수락을 켜지 않으며 의사를 임의 대체하지 않는다. 위젯 회귀 검증.

## 범위·완료
allowed_paths: app/** 및 profile 작업폴더 mobile-fix1-report.md, mobile-evidence/fix1-*만. 원본 프로토/스펙/backend/실env/기기/시뮬레이터 수정·실행 금지. 하위 워커·내부 background agent 위임 금지. 본인이 수행한다. 필요하면 기존 코디에 질문하되 새 UI정책 질문을 만들지 않는다.

원천과 같은 빠른 TTS 반이중 부재 등 비차단 참고는 범위를 넓혀 고치지 않는다. 누락코드·세션경합·녹음정리를 우선하고, 기존 모든 테스트 통과 후 fvm flutter analyze·flutter test·tool/native_logic_test.sh·unsigned iOS build를 수정본 기준으로 검증한다. 새 변경이 없는 성공 검증은 반복하지 않는다. F1/W1~W9별 변경/실제테스트/한계/명령·수치를 mobile-fix1-report.md에 남긴다. 원래 mobile-code-report.md는 이전판 증거로 보존한다. worker_done 전에 새 코디메일을 읽고 ack, live preamble outcome 포함해 정확히 한 번 보고한다.

---
원브리프(이번 수정 지시와 충돌하면 위가 우선):
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
