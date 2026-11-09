# 리뷰 리포트 — day-data-architecture / mobile-deployment / doc (2026-11-08)

대상: `products/day/40-architecture/mobile-deployment.md`(신규 293줄) · `README.md` · `system.md` diff. 검수 시점에 코디네이터 커밋 `05b9a195` 로 들어가 있었고, 커밋본과 작업 파일 md5 가 같다(`c32dd4e2…`).
근거: planner brief 「이번 발주의 완결 지시」 · DAY system.md · code-structure.md · DAY-SPEC-000 §3 07 · DAY-SPEC-001 §2/§3 · CENTURION_DAY `AGENTS.md` 「앱 (Flutter)」 · 공식 문서(2026-11-08 직접 확인).

## 판정: WARN

FAIL 은 없다. 사용자 결정과 제안 · 미결을 잘 나눴다. 도메인 소유 · 식별자 등록 · 배포 방식을 확정된 것처럼 쓴 곳도 없다. 기존 auth · DB · 런타임과 부딪히는 곳도 없고, 비밀값도 없다(키 · 비밀번호 · p8 · Team ID 문자열 검색 0건). 아래 WARN 1~3 은 머지 전에 고치기를 권한다. 처음 앱을 만드는 사람이 그대로 따라 하면 잘못 설정할 수 있는 문장이기 때문이다. 나머지는 고치지 않아도 된다.

## FAIL

없음.

## WARN

### 고치기 권장 (사용자가 설정할 때 헷갈릴 문장)

1. **`mobile-deployment.md:65` — 「KOS · APNs · FCM 을 앱이 직접 부르지 않는다」가 지나치게 넓다.** iOS 앱은 OS(`registerForRemoteNotifications`)로 APNs 기기 토큰을 받아야 한다. Android 앱도 FCM 을 쓰면 클라이언트 SDK 로 FCM 에 등록하고 토큰을 받는다. 이때 클라이언트 설정 파일(`google-services.json`)이 필요한데, 서버 키와는 다르다. 앱이 하지 않는 것은 **푸시를 보내는 호출과 보내는 데 쓰는 키를 갖는 것**이다. 권장 문장: 「푸시 *발송* · KOS 호출은 서버만 한다. 앱은 OS · SDK 로 기기 토큰만 받아 DAY 서버에 등록한다」. 같은 오해를 부르는 자리: `:61-62` Mermaid(앱 ↔ APNs 등록 선이 없음), `:222`.
2. **`:36`(앱에 Apple 팀 id 넣지 않음, [확정]) 와 `:117`(Xcode 자동 서명 + 회사 Team 선택)이 어떻게 함께 가는지 설명이 없다.** Xcode 에서 Team 을 고르면 `ios/Runner.xcodeproj/project.pbxproj` 에 `DEVELOPMENT_TEAM` 이 기록된다. 이 파일은 커밋되므로 코드 규칙(CENTURION_DAY `AGENTS.md:98` 「Apple 팀 id · 서명 값 · 키를 넣지 않는다」)과 부딪힌다. Team ID 는 비밀이 아니다. 그래도 규칙이 있으니 이를 지킬 방법을 **[미결]** 로 적어야 한다. 예: 로컬 전용 xcconfig(gitignore) · CI env 로 `DEVELOPMENT_TEAM` 넣기 · 「Dart 코드와 앱 설정값에만 해당」으로 규칙 범위를 좁히기. §13 미결 목록에 한 줄 추가를 권한다.
3. **`:248` §12 3단계에 「Android productFlavors」가 들어 있어 iOS 우선 순서와 어긋난다.** `:148` 「실제 진행은 iOS 다음」, `:254` 「Android 는 1~4 를 뒤따라 한다」와도 맞지 않는다. 3단계는 iOS scheme · configuration 과 `--dart-define` 만 남기고, Android flavor 는 `:254` 쪽으로 옮긴다.

### 고치지 않아도 됨 (표현 · 근거 정밀도)

4. **`:30` 「[확정] Android 도 같은 코드로 나중에 낸다」** — 사용자가 확정한 것은 「문서에 Android 도 적어라 · iOS 먼저」다. Android 를 언제 낼지, 내기는 할지는 정하지 않았다. code-structure.md:61 의 앱 범위도 「iOS · 폰 · 아이패드」다. 「Android 출시 여부 · 시점 [미결]」 정도가 정확하다.
5. **`:138` 「Apple 도 무단 사용 방지 장치를 **요구**」** — Apple Unlisted 페이지의 문장은 "Consider implementing a mechanism within your app to prevent unauthorized use"로, 권고다. 「권고」로 쓰는 편이 정확하다. 우리 앱은 로그인이 있으니 결론은 같다.
6. **`:59` · `:219` prod 「[확정] 실제 병원 연결」** — 근거 문서(system.md:182 · SPEC-000 §3 01 · SPEC-001:75)는 「dev 서버는 `is_demo = true` 연결만」이라고만 쓴다. prod 가 데모 연결을 빼는지는 적혀 있지 않다. 「prod = 연결 제한 없음(실제 병원 포함)」이 원문에 맞다.
7. **`:282` Flutter iOS 배포 페이지가 근거라는 「TestFlight 도 심사 지침 대상」** — 그 페이지에는 "Before releasing … App Review Guidelines"만 있다. TestFlight 외부 베타 심사 쪽은 `:293` 의 미검증 목록에 넣는 편이 맞다.
8. **`log.md` 에 이번 변경 행이 없다.** 앞선 40-architecture 변경은 모두 `arch-change` 행을 남겼다(log.md:35 · 40 · 41 · 43). planner 에게 허용된 경로는 40-architecture 뿐이었으므로 planner 가 빠뜨린 것은 아니다. PR 전에 코디네이터가 `| 2026-11-08 | arch-change | — | #… | 40-architecture mobile-deployment.md 신설(초안) … |` 한 행을 넣을지 정한다.

## 공식 출처 대조 (2026-11-08 직접 확인)

| 문서 줄 | 주장 | 결과 |
|---|---|---|
| :138 · :283 | Unlisted: 링크 가진 누구나 · 검색 · 차트 비노출 · 심사 필요 · 베타 거절 | 일치(developer.apple.com/support/unlisted-app-distribution). 무단 사용 방지는 「권고」 → WARN 5 |
| :137 · :284 | Custom(Private) = Apple Business/School Manager 지정 조직 · 승인 후 방식 변경 불가 · 공개↔비공개 = 새 앱 레코드 | 일치(set-distribution-methods). 예외: 공개 → Unlisted 는 바꿀 수 있음(문서 :138 「공개 레코드에서 별도 신청」과 맞음) |
| :139 · :285 | Enterprise: 100명 이상 · 법인 · D-U-N-S · 공개 웹사이트 · 자사 직원 내부용만 · 고객사용 아님 | 일치. Apple 은 고객사용 custom 앱은 일반 Developer Program 을 쓰라고 함. 문서의 「고객 병원 배포에 쓸 수 없다」가 맞다 |
| :140 · :286 | Ad Hoc 기기: 제품군마다 멤버십 1년 100대 · 중간에 지워도 늘지 않음 | 일치(devices-overview — 새 멤버십 해에 초기화) |
| :187 · :287 | APNs sandbox `api.sandbox.push.apple.com` · production `api.push.apple.com` | 일치(문서 JSON 데이터) |
| :189-192 · :288 | `aps-environment` 는 provisioning profile 로 정해짐 | 일치("Xcode sets the value … based on your app's current provisioning profile"). **TestFlight = production 은 확인한 두 페이지에 그대로 쓰여 있지 않다** — 배포 profile → production 으로 미루어 본 것이다(업계에서는 통설). 미확인으로 분리 |
| :195 | APNs topic = Bundle ID | 일치(apns-topic · "per bundle ID") |
| :93 · :280 | `Debug/Profile/Release-<flavor>` 소문자 · `APP_DISPLAY_NAME` · configuration 별 Bundle ID · `appFlavor` = scheme 이름 | 일치(flavors-ios). Podfile 에 configuration 을 추가하는 단계는 문서에 없다 — 설정 단계에서 공식 문서를 따르면 된다 |
| :108 · :226-227 · :282 | Flutter iOS 13 이상 · `version: 1.0.0+1` · 업로드마다 고유 빌드 번호 · 자동 서명 기본 | 일치(deployment/ios) |
| :165 · :289 | 웹 · 메일 APK 배포 · 「알 수 없는 앱 설치」 허용 필요 · 일부 통신사 차단 | 일치(alternative-distribution). 「자동 업데이트 없음」은 그 페이지에 없고 일반 설명이다 |
| :174-176 · :290 | Play 밖 배포 = Android Developer Console · 2026-08 개발자 API · 소규모 배포 계정 · 2026-09-30 브라질 · 인도네시아 · 싱가포르 · 태국(Android 7+ 인증 기기) · 2027 이후 전 세계 · 한국은 언급 없음 | 일치. 문서는 국가 · 시점을 짐작해 쓰지 않았다(M-15) |
| :166 · :291 | managed Google Play 비공개 앱 = 조직 안에서만 | 일치. 덧붙여 확인한 것: 그 조직의 EMM 콘솔 iframe 으로 게시 · 대부분 10분 안에 배포 · 공개 앱으로 전환 불가 · 하루 15개 한도. 고를 때 참고(M-3) |

미확인(이번에 공식 문서로 확인하지 못함, 문서도 :293 에 미검증으로 표시): TestFlight 시험자 종류 · 빌드 유효 기간 · 외부 베타 심사, Android 서명 키를 잃었을 때의 업데이트 불가 · Play App Signing 같은 대안, iOS Keychain 권장, 「TestFlight 빌드 = production APNs」를 그대로 적은 문장.

## 체크리스트 결과

- 사용자 결정 / 제안 / 미결 구분 — PASS. 4종 표시와 「[설정 완료] 해당 없음」(`:25`), 「어느 단계도 시작하지 않았다」(`:244`). WARN 4 만 예외.
- 도메인 소유 · 앱 ID 등록 완료를 잘못 쓴 곳 — PASS(`:38` · `:75-78` · `:214` 모두 후보 · 미등록).
- Apple Team — PASS. 「사용 가능」은 사용자 답변 기준으로 적었고, 역할 · 멤버십은 미결이다(`:32` · `:105`).
- 기존 DAY auth · emr · DB · 런타임과 모순 — PASS. Bearer `/api/auth/*` 와 같은 service(SPEC-001:193 · 209), `APP_ENV` · `day_dev/day_prod`(system.md:73 · 182), APNs 직접 · SSE(system.md:126 · 129), `device` 칸(SPEC-000:945-954)은 바꾸지 않고 「향후 계약」으로만 적었다. WARN 6 은 표현 정밀도 문제다.
- iOS private · Unlisted · Enterprise · Ad Hoc 자격 · 범위 · 심사 — PASS(공식 출처와 일치, WARN 5).
- Android 직접 APK · managed Play · 업데이트 · 키 관리 — PASS. 「Play 등록 필수 아님」(`:165`), 서명 keystore 와 Android Keystore 시스템을 구분함(`:159`).
- APNs 환경이 flavor · backend 와 별개 축 — PASS(`:185-195`).
- FCM 미확정 — PASS(`:183` · M-9). WARN 1 만 고친다.
- 비밀정보 — PASS.
- 링크 — PASS. 상대 링크 3개 파일 모두 존재하고, 외부 12개 중 11개를 직접 열었다(aps-environment 는 JSON 데이터로 확인).
- 처음 만드는 사람이 이해할 수 있는가 — PASS. 서명 · flavor/build mode 구분 설명이 좋다. WARN 1 · 2 · 3 은 따라 하다가 막힐 자리다.
- 과잉 기능 · 업무 스펙 추가 — PASS. 기능 · 권한은 스펙으로 넘겼다(`:123`). 테이블 변경 없음(`:201`). release 안내는 체크리스트가 아니라고 밝혔다(`:232`).
- allowed_paths — PASS. planner 는 40-architecture 3개 파일만 바꿨다.

## 검증

- `python3 scripts/lint-pipeline.py --strict` — exit 0 · 0 error · 263 warning. `products/day/` 범위 출력 0건. warning 263건은 모두 다른 제품(selly 등)의 기존분으로, 이번 변경과 무관하다.
- `git diff --check`(검수 시작 시 작업 트리) — 통과. 신규 파일 줄끝 공백 0.

## 직원이 실물에서 만날 자리 (사용자가 실제로 설정할 때 알아야 할 미결)

- **M-1 설치 대상**(회사 직원 / 고객 병원 직원, 개인 폰 / 관리 기기) — 이게 정해져야 iOS(Custom · Unlisted · Enterprise)와 Android(APK · managed Play)를 고를 수 있다. 고객 병원 직원이면 Enterprise 는 빠진다.
- **Team ID 를 어디에 둘지**(WARN 2) — Xcode 에서 처음 Team 을 고르는 순간 정해야 한다.
- **식별자는 등록 후 못 바꾼다** — 도메인 소유(M-4)를 확인하기 전에는 Bundle ID 를 등록하지 않는다.
- **dev 앱을 TestFlight 로 받으면 APNs 는 production** — 서버는 토큰마다 푸시 환경을 알아야 한다. 푸시를 붙일 때 SPEC-000 `device` 개정(M-10)이 필요하다.
- **Android 키** — 보관 담당 · 백업(M-11). 직접 APK 로 간다면 착수 전에 개발자 인증 적용 국가를 다시 확인한다(M-15).
- **심사용 시험 계정**(M-14) — Unlisted · Custom 모두 App Review 를 거친다. KOS 데모 연결 계정을 써도 되는지 확인해야 한다.

## 참고(기존 부채)

- 다른 제품의 lint warning 263건(기존, 무관).
