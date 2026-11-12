# [mobile-asc] 정식 DAY App Store Connect 등록 리포트 (2026-11-11)

## 상태: 등록 완료 — 메타데이터 · URL · 스크린샷 10장 · 빌드 0.1.0(1) 연결. 심사 제출 안 함(입력 미정 항목 남음)

- 대상: App Store Connect 앱 `DAY`. `bundleId == "day.medisolveai"`로 정확히 비교해 1건 일치했고, resource id는 6833456680이다. DAY Dev는 조회 · 변경하지 않았다.
- 방법: 공식 App Store Connect API(`api.appstoreconnect.apple.com/v1`)만 사용했다. JWT(ES256 · 15분)는 프로세스 안에서만 만들었다. 키 · Issuer · Team ID · 토큰 · 계정 값은 출력 · 기록하지 않았다.
- 작업용 파일: `~/.config/day/apple/` 아래 `asc_day.py` · `asc_upload_shots.py` · `asc-readback.local.txt`. 모두 권한 600이고 레포 밖이다.
- 바꾸지 않은 것: 앱 소스 · backend · env · `_RESUME.md`. 커밋 · push · 빌드 · 서명 · 바이너리 업로드 · 심사 제출도 하지 않았다.

## 등록 전 조회(기존값)

| 항목 | 기존값 |
|---|---|
| 앱 | `DAY` · `day.medisolveai` · primaryLocale `ko` |
| iOS 버전 | 1개, `1.0` · `PREPARE_FOR_SUBMISSION` · releaseType `AFTER_APPROVAL` · copyright 없음 |
| appInfo | `PREPARE_FOR_SUBMISSION` · primaryCategory 없음 |
| appInfoLocalization ko | name `DAY` · subtitle · privacyPolicyUrl · privacyChoicesUrl 모두 없음 |
| appStoreVersionLocalization ko | description · keywords · promotionalText · supportUrl · marketingUrl · whatsNew 모두 없음 |
| 스크린샷 세트 | 0 |

0.1.0 버전은 없었다. 앱 record를 만들 때 자동으로 생긴 편집 가능 버전 `1.0` 하나가 있었다. 새 버전을 만들면 편집 버전이 둘로 중복되므로, 이 버전의 `versionString`을 `0.1.0`으로 바꿔 재사용했다.

## 등록(쓰기) — 각 쓰기 전에 현재값을 재확인했고, 이미 있는 값은 덮어쓰지 않았다

| 리소스 | 필드 | 값 |
|---|---|---|
| appStoreVersions | versionString | `1.0` → `0.1.0` |
| appStoreVersions | releaseType | `AFTER_APPROVAL` → `MANUAL`(자동 공개 방지) |
| appStoreVersionLocalizations(ko) | description | 초안 「설명 초안」 본문. 마크다운 `-` 목록은 `•`로 바꿨다. 초안 안내문 「예약 화면 등 …」 줄은 넣지 않았다. 207자 |
| appStoreVersionLocalizations(ko) | keywords | `병원,직원,시술현황,업무,채팅,알림,통역` |
| appInfoLocalizations(ko) | subtitle | `병원 직원을 위한 업무 앱` |
| appInfos | primaryCategory | 비어 있어서 `BUSINESS`로 설정 |

## API GET 재조회(readback)

| 항목 | 결과 |
|---|---|
| 앱 | `DAY` · `day.medisolveai` · `ko` |
| 버전 | 1개 · `0.1.0` · IOS · `PREPARE_FOR_SUBMISSION` · releaseType `MANUAL` |
| 설명(ko) | 207자 · sha256 앞 8자 `0af2b167` · 「예약」 포함 안 됨 |
| keywords(ko) | `병원,직원,시술현황,업무,채팅,알림,통역` |
| 부제(ko) | `병원 직원을 위한 업무 앱` |
| 카테고리 | primary `BUSINESS` |
| 빌드 연결 | **0.1.0(1) · `VALID`** (build resource `9c4cd151…`) |
| 심사 정보(appStoreReviewDetail) | 없음 |
| 개인정보처리방침 URL(ko) | `https://day.medisolveai.com/privacy`. 등록됨 · 실제 페이지는 502 |
| 지원 URL(ko) | `https://day.medisolveai.com/support`. 등록됨 · 실제 페이지는 502 |
| 앱의 빌드 목록 | 1개(0.1.0(1) · `VALID` · 만료 안 됨) |
| 스크린샷 iPhone `APP_IPHONE_67` | 5장 · 1320×2868 · 전부 `COMPLETE` · MD5가 원본과 일치 · 순서 01-board → 05-interpret |
| 스크린샷 iPad `APP_IPAD_PRO_3GEN_129` | 5장 · 2064×2752 · 전부 `COMPLETE` · MD5가 원본과 일치 · 같은 순서 |

## 빌드 연결 — 완료

- 스크립트: `~/.config/day/apple/asc_link_build.py <build_id>`. 기본은 검사만 하고, `--apply`를 줘야 연결한다.
- 검사 조건: 다음을 모두 만족할 때만 연결한다.
  - 빌드의 앱이 6833456680
  - `processingState == VALID`이고 만료되지 않음
  - preReleaseVersion이 `0.1.0` · `IOS`
  - 앱 버전이 편집 가능한 `0.1.0`
  - 이미 같은 빌드가 연결돼 있으면 건너뛴다.
- 연결 방법: `PATCH /v1/appStoreVersions/{id}/relationships/build`(공식 OpenAPI 4.6) 뒤 GET으로 재확인한다.
- 한계: 빌드가 촬영용 target인지 `lib/main.dart`인지는 API로 구분할 수 없다. 바이너리 task가 `lib/main.dart`로 만들었다고 확인한 build id만 받는다.

## 입력 미정 — 사용자 · 코디 확정 전에는 등록하지 않음

- 개인정보처리방침 URL · 지원 URL: **편집 중 메타데이터에 등록했다.** 근거는 코디 후속 지시(delivery_3d2548002cf3)이며, 앞서 받은 「502라서 대기」 지시(delivery_693a587aa18b)를 이 지시가 대체한다.
  - 등록한 칸: appInfoLocalization ko `privacyPolicyUrl` = `https://day.medisolveai.com/privacy`, appStoreVersionLocalization ko `supportUrl` = `https://day.medisolveai.com/support`. 둘 다 비어 있던 칸이고 GET으로 재확인했다.
  - **페이지는 아직 없다.** 2026-11-11 `curl` 결과 `/privacy` 502 · `/support` 502다. prod 서버가 미배포이고 라우트도 없다.
  - **제출 전 확인(pending):** 두 주소가 200을 돌려주는지, 그리고 문안과 지원 연락처가 실제로 들어 있는지 확인해야 한다. 이 주소가 지금 동작한다는 뜻이 아니다.
- copyright(appStoreVersion `copyright`): 비어 있다.
- 심사 연락처 · 데모 계정 · 심사 메모(appStoreReviewDetail): 없다.
- 빌드: 서명 · 업로드를 별도로 해야 한다.
- 연령 등급, App Privacy 설문, 가격 · 판매 지역, 콘텐츠 권리 선언: 이번 범위 밖이라 건드리지 않았다.

## 스크린샷 준비(업로드 대기)

- 표시 타입은 공식 OpenAPI 4.6(`ScreenshotDisplayType`)으로 확인했다.
  - iPhone 1320×2868 · 1290×2796 → `APP_IPHONE_67`
  - 1284×2778 → `APP_IPHONE_65`
  - 1206×2622 → `APP_IPHONE_61`
  - iPad 2064×2752 · 2048×2732 → `APP_IPAD_PRO_3GEN_129`
- 업로드 절차(공식 스키마 `UploadOperation` · `AppScreenshotUpdateRequest` · `AppMediaAssetState` 기준):
  1. 승인 목록의 sha256, PNG 알파 없음, 규격을 검사한다.
  2. 세트를 조회하고, 없을 때만 만든다.
  3. 같은 파일명 + MD5로 `UPLOAD_COMPLETE` · `COMPLETE`인 자산이 있으면 건너뛴다.
  4. `POST /v1/appScreenshots`로 업로드를 예약한다.
  5. `uploadOperations`에 지정된 method · url · offset · length · requestHeaders 그대로 업로드한다. ASC 토큰은 붙이지 않는다.
  6. `PATCH uploaded=true` · `sourceFileChecksum`(MD5)로 확정한다.
  7. `assetDeliveryState`가 `COMPLETE`가 될 때까지 기다린다.
- 대기 이유: 이미지 폴더 `app/store/0.1.0/screenshots/{iphone,ipad}/`가 아직 없다. 코디의 시각 검토 승인도 아직 없다.

## 스크린샷 업로드(완료)

- 승인: 코디 delivery_2e4896cd70bf. 코디가 10장을 직접 열어 실제 UI · 가짜 데이터 · 디버그 배너 없음을 확인했다. allowlist는 `~/.config/day/apple/approved-screenshots.local.json`(600)이다.
- 업로드 직전 검사: 10장 모두 allowlist의 sha256 · width · height · `pngColorType=2`(RGB, 알파 없음)와 일치했다. 불일치가 있었다면 중단했을 것이다.
- 세트: 둘 다 없어서 새로 만들었다(`APP_IPAD_PRO_3GEN_129` · `APP_IPHONE_67`). 기존 이미지 삭제 · 중복은 0이다.
- 업로드 절차: 예약 → `uploadOperations`에 지정된 method · url · offset · requestHeaders 그대로 업로드(ASC 토큰 미첨부) → `uploaded=true` · MD5로 확정 → 10장 모두 `assetDeliveryState=COMPLETE`. 실패나 재시도는 없었다.
- GET 재조회 결과는 위 표와 같다(세트별 5장, 파일명 순서, 처리 완료).

## 남은 일

- **빌드 연결: 완료.** 코디 통지(delivery_e5cc7b44caca)에 따르면 업로드와 IPA 검증이 끝났다. 코디 확인 내용: IPA sha256 `dc96e1f7…`, `day.medisolveai` · `DAY` · 0.1.0 · 1, 암호화 false, 촬영 target · fixture 문자열 0, `aps-environment production`, `get-task-allow false`, `lib/main.dart` target. 그 뒤 ASC가 21:27에 빌드를 `VALID`로 처리했다. `asc_link_build.py`로 먼저 검사(앱 6833456680 · `VALID` · 만료 안 됨 · 0.1.0 · IOS · 연결된 빌드 없음 — 모두 통과)한 뒤 `--apply`로 연결했고, GET으로 `9c4cd151…` · 1 · `VALID`를 확인했다.
- **입력 미정:** 심사 연락처 · 데모 계정 · 심사 메모, copyright, 연령 등급, App Privacy, 가격 · 판매 지역, 콘텐츠 권리 선언.
- **pending:** `/privacy` · `/support`가 200을 돌려주는지 제출 전에 확인해야 한다(현재 502).
- 심사 제출 · 출시 · Unlisted 신청은 하지 않았다.

## 최종 GET 재조회 (빌드 연결 뒤)

| 항목 | 결과 |
|---|---|
| 버전 | 1개 · `0.1.0` · `PREPARE_FOR_SUBMISSION` · releaseType `MANUAL` |
| 빌드 | `1` · `VALID` 연결됨 |
| 설명 | 207자 · sha256 앞 8자 `0af2b167` |
| keywords | `병원,직원,시술현황,업무,채팅,알림,통역` |
| 부제 | `병원 직원을 위한 업무 앱` |
| 카테고리 | `BUSINESS` |
| 개인정보 · 지원 URL | `/privacy` · `/support` 등록됨. 실제 페이지는 502(제출 전 200 확인 pending) |
| 스크린샷 | iPhone 6.7 5장 `COMPLETE` · iPad 13 5장 `COMPLETE` |

### 구분

- **등록 완료:** 위 표의 항목 전부.
- **입력 미정(사용자):** 다음 칸이 남아 있다. 이 칸들이 채워지기 전에는 심사 제출이 막힌다.
  - App Review Information의 연락처 · 데모 계정 · 메모
  - 버전의 copyright
  - 연령 등급 설문
  - App Privacy
  - 가격 · 판매 지역
  - 콘텐츠 권리 선언
  - 추측해서 넣지 않았다.
- **도구 미지원:** 이번 범위에서는 없었다. App Privacy 설문은 공개 App Store Connect API로 쓸 수 없어 ASC 웹의 「App 개인정보 보호」에서 입력해야 한다는 점만 참고로 적는다(이번에 시도하지 않았다).
- **하지 않은 것:** 심사 제출 · 출시 · Unlisted 신청, 다른 앱(DAY Dev) · 계약 · 가격 · 테스터 변경.
