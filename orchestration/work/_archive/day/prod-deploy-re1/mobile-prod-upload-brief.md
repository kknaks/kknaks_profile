# [mobile] 정식 DAY 배포 빌드·App Store Connect 업로드

같은 코드 워크트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/mobile/*.md를 따른다. 사용자 이번 명시 지시 “지금 다 준비하고 App Store Connect API에 너가 등록”. **이번 task에 한해 정식 앱 서명·export·업로드 허용**. 심사 제출·공개 출시·테스터 변경은 금지.

## 1. SSOT
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-build-report.md 및 mobile-asc-report.md (정식 record id 6833456680, bundle day.medisolveai)
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/_archive/day/fix/app-testflight-upload-report.md (성공한 최종 5차 절차)
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/_archive/day/fix/app-testflight-upload-2-report.md
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/config/projects/day.json apple. 자격은 ~/.config/day/apple/credentials.local.json. ~/.appstoreconnect/private_keys의 키는 DAY 키가 아니므로 쓰지 말 것.

## 2. 작업
현재 실제 출시 진입점 lib/main.dart로 정식 production IPA를 생성·검증·업로드하고 ASC 처리 VALID 및 0.1.0 version의 build 연결까지 준비한다. 코디/ASC 워커가 연결할 수 있도록 build resource id 보고. 촬영용 fixture·main이 바이너리에 섞이면 업로드 금지.

## 3. 빌드 계약
- target를 반드시 **lib/main.dart**로 명시. 직전 시뮬레이터 촬영 Generated.xcconfig가 tool/store_capture를 가리킬 수 있으므로 덮어씀.
- DAY_BUNDLE_ID=day.medisolveai, DAY_DISPLAY_NAME=DAY
- --build-name=0.1.0, build-number는 prod ASC builds 조회하여 아직 없는 가장 작은 자연수(기존 있으면 다음)
- DAY_LOGIN_ENTRY=https://day.medisolveai.com
- DAY_ALLOWED_ORIGINS=https://day.medisolveai.com,https://day-dev.medisolveai.com
- DAY_REQUIRE_ENVIRONMENT=true, DAY_APNS_ENV=production
- 수출규정 Info.plist false 기존 유지, 소스 변경 금지

## 4. 단계
1. branch/app 상태 확인. app/store와 tool/store_capture 변경은 사진 task 소유, 되돌리거나 삭제하지 않음. 다른 워커 backend 변경도 건드리지 않음.
2. prod ASC build 목록 read-only 조회. DAY Dev와 혼동 금지. build-number 기록.
3. Flutter config-only release를 --target=lib/main.dart 및 계약 define로 재생성. 서명 없는 archive → 산출물 앱에만 Runner.entitlements ad-hoc → app-store-connect 자동 export. 과거 성공 최종 절차만 사용하고 실패한 1~4차 재시도 금지. 팀/키 ID는 credentials 읽어 변수로 쓰되 출력 금지. 신규 배포 프로파일 필요시 정식 App ID에 자동 생성 허용, 인증서/기기 삭제 및 기존 자산 변경 금지.
4. IPA: bundle/name/version/build/icon/production aps/암호화 false/provisioning/id, codesign verify deep strict. 바이너리에 캡처 target 및 fixture 고유 문자열 포함 0 확인. App.framework prod+dev origin만. 서명/Team 값은 리포트 마스킹.
5. altool validate → upload. API_PRIVATE_KEYS_DIR는 credentials의 private_key_path 부모 디렉토리. 전체 로그에 키 값 노출이 있으면 로그는 app/build/ 무시 디렉토리에만, 콘솔에는 요약만.
6. ASC 처리 최대20분을 제한된 간격으로 확인, VALID 및 usesNonExemptEncryption=false, build id 확인. 단순 조회 기다림은 60초 이하 단위. 오류 발생시 정확 원인·Apple 메시지 식별만 보고.
7. /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-prod-upload-report.md에 산출물경로/hash·빌드 값·서명 검증·validate/upload·processingState·앱 버전 연결 가능 여부·신규 서명 자산 종류/개수·실물 pending 기록.

## 5. allowed_paths
app/build/store-prod/ 아래 생성물·로그 및 기존 생성 무시파일만 쓰기. 레포 영구 문서 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-prod-upload-report.md만. app/ 소스·backend·env·_RESUME 수정 금지, 커밋·push·PR 금지.

## 6. 주의
prod 서버는 아직 미배포(502)이며 정책 링크/지원 연락처/심사 데모 로그인/실물은 미완이다. 바이너리 등록은 심사 제출·승인을 뜻하지 않는다. 예약 placeholder 소스는 변경하지 않는다. 키·토큰·계정·Team ID 출력 금지. 생성한 .xcarchive/ipa에 서명값이 들어 있는 것은 정상이나 공개 repo로 커밋하지 않는다.

## 7. 수용
정식 앱 IPA의 배포 서명 확인, altool validate/upload 성공, ASC VALID. 실패면 실제 실패 보고, 성공으로 추정하지 않는다. 심사제출·출시0.

## 8. 보고
한국어. 기존 source 변경 없음을 app/ diff에서 새 capture 자료와 분리 확인. 새 프로파일/인증서는 종류만 보고.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2b709186-d9f1-4811-8538-95544d6d21b8 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
