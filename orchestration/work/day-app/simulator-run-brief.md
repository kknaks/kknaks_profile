# [mobile] iPhone 시뮬레이터에 DAY 앱 실행 — day-dev 연결

너는 DAY mobile 워커다. 앞 맥락이 없다고 보고 이 한 장으로 진행한다. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/mobile/의 role.md·rules.md·skills.md·tools.md·workflow.md와 코드 AGENTS.md, app/README.md를 읽는다.

## 1. 대상·현재 상태
코드 트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, branch kknaksss/day-app, HEAD0b776e900cc229f3a447cb0e937400534b6bc709. 앱+D1 구현과 독립 재검수 PASS, 앱155/Swift47/서버663/analyze0/unsigned device build 성공. 코드 PR #237과 문서 #921은 미머지다. 예전 워커는 종료되어 새 터미널이다. profile 작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/의 mobile-fix1-report.md·review-mobile-code2-report.md 참고.

## 2. 사용자 새 지시
“시뮬레이터로 못띄워 서버는 우리 day-dev 가면 되잖아” → 지금 시뮬레이터 실행/표시가 명시 허용됐다. 기존 브리프의 시뮬레이터 실행 금지는 이번 태스크에 적용하지 않는다. iPhone 시뮬레이터에서 실제 DAY 앱을 띄워 사용자가 로그인할 수 있게 남긴다. 서버 배포/머지/서명/TestFlight/실기기는 여전히 금지.

## 3. 서버·개발 설정
코디가 https://day-dev.medisolveai.com/health/ready HTTP200, database/redis/encryption ok 확인했다. 앱은 서버가 준 상태를 사용한다.
런타임 개발 빌드 값(코드 파일 하드코딩 금지):
- DAY_LOGIN_ENTRY=https://day-dev.medisolveai.com
- DAY_ALLOWED_ORIGINS=https://day-dev.medisolveai.com
- DAY_REQUIRE_ENVIRONMENT=false
- DAY_APNS_ENV=sandbox (시뮬레이터에서 실제 APNs 검증을 주장하지 않음)
이유: D1 환경 연결은 아직 미머지라 dev 로그인은 환경 필드가 없을 수 있다. 기존 개발 전용 fallback을 사용하고 release 규칙을 완화하지 않는다. 앱·서버 env 파일에 주소/계정/키를 기록하지 않는다.

## 4. 시뮬레이터·실행
현재 부팅된 기기 없음. 준비된 자동화용 iPhone:
`orca-mobile-iphone`, UDID `5C9E05C7-7171-455E-97CE-2AD2EA097F88`, iOS26.2, Shutdown.
이 기기를 boot하고 bootstatus 확인, Simulator.app을 해당 기기로 표시한다. 사용자 다른 기기를 종료/초기화/삭제하지 않는다. 기존 시뮬레이터가 재사용 중이면 먼저 상태를 확인하고 그 앱만 설치/실행한다. 대안이 꼭 필요할 때는 임의 기기 대신 코디에게 상태 보고.
FVM Flutter3.44.8/Dart3.12.2 pin 유지, global 설정 변경0. `fvm flutter run -d <UDID> --debug --no-resident --dart-define=...` 또는 build --simulator --debug → simctl install/launch로 실행해도 된다. 서명/Team 불필요. 기존 임시BundleID는 app/ios/Flutter/Identity.xcconfig에 있다(예제 com.example.day.placeholder). 실제 앱화면이 떠 있는지 simctl screenshot으로 확인하고 profile 작업폴더 simulator-evidence/iphone-login.png에 저장한다. 앱 프로세스·Simulator는 사용자 확인용으로 계속 켜 둔다(실행 도구가 내려가며 앱을 끄지 않게 한다).

## 5. 로그인·데이터 경계
계정/비밀번호는 주어지지 않았다. 비밀 env·키체인·다른 앱에서 자격증명을 찾지 말고 로그인 시도/업무쓰기/시드실행을 하지 않는다. 로그인 화면까지 띄워 사용자에게 넘긴다. 실제dev연결은 health/read-only상태+주입빌드값으로 확인, 인증/시술현황통합완료라고 쓰지 않는다. D2/D3 서버는 미구현이며 이번에 구현하지 않는다.

## 6. allowed_paths
원칙 코드변경0, 빌드·설치·시뮬레이터 실행만 한다. 증거/보고는 profile 작업폴더 simulator-evidence/**·simulator-run-report.md. simulator 빌드가 실제 코드/프로젝트 설정 오류로 막히면 app/** 최소 수정은 허용(원인·diff·테스트·sim build를 보고), backend/스펙/서버/실env/서명값 수정금지. 커밋·push·PR은 코디가 한다. 모든 merge금지, 새로운 PR 만들지 않는다. 하위 워커/내부 agent 위임 금지.

## 7. 검증
실제 simulator build 성공, install/launch PID, UDID/기기명, 주입서버 origin, 로그인화면 스크린샷, 프로세스가 남는지 확인한다. 코드수정 없으면 기존 테스트155개/analyze/devicebuild를 반복하지 않는다. 소스수정이 필요했으면 필요한검증과 독립리뷰는 코디에게 넘긴다.

## 8. 완료
simulator-run-report.md에 실제 명령/결과/스크린샷 경로·코드변경 여부·남긴 앱/기기·인증미실행을 한국어로 보고한다. live preamble의 새 id/핸들/worker_done outcome이 아래 예시보다 우선. 마지막 메일 처리 후 정확히 한 번 worker_done을 보내고 idle한다. 앱은 켜 둔다.

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
