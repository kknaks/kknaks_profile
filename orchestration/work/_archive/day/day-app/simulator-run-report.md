# day-app 시뮬레이터 실행 결과 보고
## 상태: done

## 수행
- 코드 트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app`, branch `kknaksss/day-app`, HEAD `0b776e900cc229f3a447cb0e937400534b6bc709`.
- **코드 변경 없음**(`git status --short` 빈 결과). env 파일 · 전역 설정 · fvm 전역 변경 없음. FVM Flutter 3.44.8 · Dart 3.12.2(app/.fvmrc).

## 실제 명령과 결과
```sh
xcrun simctl boot 5C9E05C7-7171-455E-97CE-2AD2EA097F88
xcrun simctl bootstatus 5C9E05C7-7171-455E-97CE-2AD2EA097F88 -b      # Finished
open -a Simulator --args -CurrentDeviceUDID 5C9E05C7-7171-455E-97CE-2AD2EA097F88
curl -s -o /dev/null -w '%{http_code}' https://day-dev.medisolveai.com/health/ready   # 200
cd app
fvm flutter build ios --simulator --debug \
  --dart-define=DAY_LOGIN_ENTRY=https://day-dev.medisolveai.com \
  --dart-define=DAY_ALLOWED_ORIGINS=https://day-dev.medisolveai.com \
  --dart-define=DAY_REQUIRE_ENVIRONMENT=false \
  --dart-define=DAY_APNS_ENV=sandbox
# ✓ Built build/ios/iphonesimulator/Runner.app (Xcode build 30.9s)
# 경고만: flutter_pcm_sound · flutter_tts 가 Swift Package Manager 미지원(빌드 영향 없음)
xcrun simctl install 5C9E05C7-7171-455E-97CE-2AD2EA097F88 build/ios/iphonesimulator/Runner.app
xcrun simctl launch 5C9E05C7-7171-455E-97CE-2AD2EA097F88 com.example.day.placeholder   # PID 19220
xcrun simctl io 5C9E05C7-7171-455E-97CE-2AD2EA097F88 screenshot <작업폴더>/simulator-evidence/iphone-login.png
```

## 검증
- 기기: `orca-mobile-iphone` · UDID `5C9E05C7-7171-455E-97CE-2AD2EA097F88` · iOS 26.2 · Booted. 다른 기기는 건드리지 않음(시작 시 부팅된 기기 없음).
- 주입 서버 origin: `https://day-dev.medisolveai.com`(로그인 진입점 = 허용 목록 유일 항목). 빌드 인자로만 넣었고 소스 · env 파일에 기록하지 않음.
- Bundle ID: 임시 `com.example.day.placeholder`(Identity.xcconfig 기본값). 서명 · Team 없음.
- 스크린샷: `simulator-evidence/iphone-login.png` — 「MediSolve AI / DAY」 로그인 카드(이메일 · 비밀번호 · 로그인 버튼). 설정 오류 코드 표시 없음.
- 프로세스: 스크린샷 뒤 `launchctl list` 에 `UIKitApplication:com.example.day.placeholder` PID 19220 확인. Simulator.app(PID 16215) 이 해당 UDID 로 떠 있음. simctl launch 로 띄워 실행 도구 종료와 무관하게 앱은 남는다.
- 기존 테스트 155 · analyze · device build 는 코드 변경이 없어 다시 돌리지 않음.

## 경계
- **로그인 시도 · 업무 쓰기 · 시드 실행 안 함.** 자격증명을 찾지 않음. 인증 · 시술현황 통합은 미확인 — dev 연결은 health/ready 200 과 주입 빌드값으로만 확인.
- `DAY_REQUIRE_ENVIRONMENT=false` 는 debug 전용 fallback(D-1 미머지 대응). release 규칙은 그대로.
- `DAY_APNS_ENV=sandbox` — 시뮬레이터라 실제 APNs 는 검증하지 않음. D-2 · D-3 서버는 미구현(푸시 pending · 통역 연결 오류가 정상).

## 남겨 둔 것 · 코디 확인
- 시뮬레이터 `orca-mobile-iphone` 부팅 상태 + DAY 앱(PID 19220) 로그인 화면 대기 — 사용자가 직접 로그인하면 된다.
- dev 서버 로그인 응답에 `api_base_url` 이 없으면 debug fallback 으로 요청 주소를 쓴다. 응답의 `api_base_url` 이 허용 목록 밖이면 debug 라도 거절된다(그때는 오류 코드만 표시).
- 빌드 산출물 `app/build/` 은 gitignore 대상(워크트리 변경 없음).
