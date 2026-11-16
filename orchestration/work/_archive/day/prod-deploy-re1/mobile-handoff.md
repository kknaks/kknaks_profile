# DAY 정식 앱 준비 전체 인계 — 메인 코디용

작성·확인: 2026-11-12. 아래 내용을 메인 코디가 읽고 앱 준비 작업을 인계받는다.

**현재는 사용자 지시로 대기 중이다.** 마지막 실행 지시는 「실제 환경과 데모 환경 로그인을 모두 확인해야 하니 일단 대기」다. 이 문서는 인계 기록이며 배포·테스트 재개 승인이 아니다. 완료 상태의 원격 검증 시점은 2026-11-11이다. 현재 서버·ASC 상태는 재개 시 다시 확인한다.

## 1. 작업 위치와 소유권

| 구분 | 워크트리 | 마지막 확인 브랜치 |
| --- | --- | --- |
| 프로필·작업 기록 | `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app` | 현재 체크아웃 유지 |
| 코드 | `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` | `kknaksss/prod-deploy-re1` |
| 스펙 | `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec` | `kknaksss/prod-deploy-re1-spec-web` |

- 같은 작업 `prod-deploy-re1`을 이어간다. 새 slug·워크트리·브랜치를 임의로 만들지 않는다.
- 서버·웹·환경 설정과 기존 `_RESUME.md`는 메인 코디 소유다. 앱 세션에서는 수정하지 않았다.
- 같은 코드 워크트리에서 다른 워커가 서버·웹을 수정했다. 전체 `git add -A`·되돌리기 금지. 현재 `git status`와 소유권부터 확인한다.
- 앱 세션에서 회사 레포 commit·push·PR은 하지 않았다. 새 앱 자료·스펙 문서를 보존하고 메인 코디의 기존 PR 절차에 맞춰 검토한다.

## 2. 사용자가 확정한 제품 정체성

DAY는 **기존 병원 EMR의 정보를 조회하고 시술 진행 상태를 변경하는 직원용 앱**이다.

- 기존 EMR이 업무 원장이다. DAY 서버에는 동기화 사본과 상태 변경 등에 필요한 업무 이력이 있다.
- 새로 작성하는 업무 콘텐츠는 주로 직원 채팅·첨부파일이다.
- 로그인 세션·푸시 기기 등록 같은 기술 정보는 업무 원장과 구분한다.
- 신규 진료기록을 수집하는 환자용 앱처럼 설명하지 않는다.
- 조회 중심이라는 이유로 「DAY 서버 저장 데이터가 없다」고 설명하지 않는다.
- 최종 배포 방식은 사용자 결정인 **Unlisted**다.

## 3. App Store Connect 등록 완료

2026-11-11 공식 API GET 확인 결과:

| 항목 | 값 |
| --- | --- |
| 앱 | DAY |
| Bundle ID | `day.medisolveai` |
| ASC app ID | `6833456680` |
| iOS 버전·빌드 | `0.1.0 (1)` |
| build ID | `9c4cd151-eee6-4f50-bcdf-7207d38a50ba` |
| version ID | `e0ae563c-4586-41a3-899e-f4fc1b89deea` |
| processingState | `VALID` |
| usesNonExemptEncryption | `false` |
| expired | `false` |
| 빌드 연결 | 위 빌드를 0.1.0 버전에 연결 완료 |
| 앱 버전 상태 | `PREPARE_FOR_SUBMISSION` |
| releaseType | `MANUAL` |

최초에 존재하던 편집 버전 `1.0`을 `0.1.0`으로 수정해 재사용했다. 중복 버전 생성은 하지 않았다. `DAY Dev`는 변경하지 않았다.

등록한 한국어 메타데이터:

- 최종 설명: **283자**, UTF-8 sha256 앞 8자 **`85ed67f7`**. App Store·TestFlight 양쪽 동일 원천으로 반영·GET 대조.
- 부제: 병원 직원을 위한 업무 앱
- 키워드: 병원,직원,시술현황,업무,채팅,알림,통역
- 카테고리: `BUSINESS`
- 개인정보처리방침: `https://day.medisolveai.com/privacy`
- 지원: `https://day.medisolveai.com/support`

URL은 ASC 편집 메타데이터에 저장했다. 실제 페이지 공개 완료를 뜻하지 않는다.

## 4. 정식 빌드·서명·업로드

실제 출시 진입점 `lib/main.dart`로 정식 IPA를 생성했다.

| 설정 | 값 |
| --- | --- |
| DAY_BUNDLE_ID | `day.medisolveai` |
| DAY_DISPLAY_NAME | `DAY` |
| version / build-number | `0.1.0` / `1` |
| DAY_LOGIN_ENTRY | `https://day.medisolveai.com` |
| DAY_ALLOWED_ORIGINS | `https://day.medisolveai.com,https://day-dev.medisolveai.com` |
| DAY_REQUIRE_ENVIRONMENT | `true` |
| DAY_APNS_ENV | `production` |

서명 절차는 이전 DAY Dev에서 성공한 방식이다: 서명 없는 archive → 산출물 앱에만 entitlements ad-hoc 서명 → `app-store-connect` 자동 export.

확인한 것:

- Apple Distribution 서명·`codesign --verify --deep --strict` 통과
- `aps-environment=production`, `get-task-allow=false`, 정식 앱 App Store 프로파일
- 아이콘·버전·암호화 설정·prod/dev 허용 origin
- 촬영용 target·fixture 문자열 혼입 없음
- altool validate·upload 성공, ASC VALID 처리·버전 연결

IPA: 코드 워크트리 `app/build/store-prod/ipa/DAY.ipa` — 무시 경로이며 커밋하지 않는다.

SHA256: `dc96e1f74779e686311b3606fc4c3ed28533d93448babfb7539e47f203ca75d1`

신규 서명 자산: 정식 App Store 배포 프로파일 1개. 인증서 추가 없음.

최소 iOS 13.0이다. 업로드 경고 90068이 있었지만 업로드·처리는 성공했다. 경고 내용은 2027-04부터 iOS 15.0 이상 대상 필요. 다음 새 업로드는 build-number **2 이상**이다.

**바이너리 업로드와 테스터 배포·심사 제출·공개 출시는 구분한다.** 이미 바이너리는 ASC에 있다. 앱 코드가 바뀌지 않으면 기존 빌드(1)을 사용할 수 있다.

## 5. 실제 시뮬레이터 스크린샷

실제 앱을 시뮬레이터에 재빌드·설치해 촬영했다.

| 기기 | 규격 | 장수 | ASC 세트 |
| --- | --- | --- | --- |
| iPhone 17 Pro Max | 1320×2868 | 5 | `APP_IPHONE_67` |
| iPad Pro 13-inch M5 | 2064×2752 | 5 | `APP_IPAD_PRO_3GEN_129` |

장면은 두 기기 공통이다:

1. `01-board.png` — 시술 현황
2. `02-room.png` — 룸 상세
3. `03-chat.png` — 직원 채팅
4. `04-notifications.png` — 알림
5. `05-interpret.png` — 통역

- 실제 `DayApp` UI + 가짜 fixture를 촬영 전용 진입점으로 실행했다. 실존 직원·고객·계정 정보는 쓰지 않았다.
- 서버 통합 검증 증거가 아니다. 출시 main과 촬영용 main을 분리했다.
- 상태 막대 9:41, debug 배너 없음, 리사이즈·화면 합성 없음.
- 알파를 제거해 RGB로 변환하고 픽셀 동일·원본 규격·SHA manifest를 확인했다.
- 코디가 10장을 직접 열어 시각 검토했다.
- API 업로드 **10/10 COMPLETE**, 원본 MD5 일치, 각 세트 01→05 순서, 중복·기존 이미지 삭제 없음.

코드 레포 산출물:

- `app/tool/store_capture/main.dart`
- `app/store/0.1.0/README.md`
- `app/store/0.1.0/screenshots/iphone/`
- `app/store/0.1.0/screenshots/ipad/`
- `app/store/0.1.0/screenshots/manifest.sha256.txt`

작업용 시뮬레이터·helper는 정리했다. 촬영 후 정식 빌드는 `lib/main.dart`로 다시 생성했다.

## 6. 앱 코드·검증·권한 문구

앱 일반 `lib/`·`ios/`·`pubspec`·기존 테스트 소스는 수정하지 않았다. 새 파일은 촬영 전용 코드·이미지·기록이다.

검증 기록:

- 기존 앱 analyze: 0 issues
- 기존 flutter test: 343 passed, 캡처 전용 73 skip, 실패 0
- 정식 release 빌드 성공
- 촬영 진입점 analyze·simulator 빌드 확인

권한 문구는 기존 한국어 원문 그대로이며 실제 빌드에도 들어 있다:

- 마이크: 「통역할 때 의료진과 고객의 말을 듣기 위해 마이크를 사용합니다.」
- 사진 보관함: 「채팅으로 보낼 사진 · 동영상을 고르고 최근 사진을 보여 주기 위해 사진 보관함을 사용합니다. 고른 것은 줄이거나 바꿔서 보내고 기기에 따로 저장하지 않습니다.」
- 카메라: 「채팅으로 보낼 사진을 찍기 위해 카메라를 사용합니다. 찍은 사진은 사진첩에 저장하지 않습니다.」

## 7. 서류·공개 페이지 문안 원천

스펙 레포의 **`products/day/60-release/app-store-preparation.md`**가 정책·문안 원천이다.

준비한 내용:

- 제출물 원천·산출물·버전 관리 기준
- 스크린샷 규격·장면·가짜 데이터·파일명·hash 기준
- 촬영용 fixture와 출시 앱의 차이
- 기존 권한 문구
- 최종 앱 설명, App Review 메모, Unlisted 신청 사유
- 관리자 테스트 계정과 심사용 데모 계정 구분
- TestFlight 한국어 테스트 안내
- `/privacy` 개인정보 처리 안내 문안
- `/support` 지원 안내 문안
- 실제 공개·심사 전 남은 확인 항목

**별도 서비스 이용약관(Terms of Use)은 만들지 않았다.** 만들어 둔 공개 페이지 문안은 개인정보 처리 안내와 지원 안내다.

서버 코디가 확인한 구현 방향:

- `/privacy`·`/support` 로그인 없는 공개 GET 라우트·템플릿
- 실제 라우트 구현·배포는 서버 코디 소유
- 마지막 확인 당시 prod 서버 자체가 미배포라 502였다. 현재도 502라고 단정하지 말고 재개 시 확인한다.

## 8. 지원·심사 연락처·데모 자격

공개 지원메일은 **dev@medisolveai.com**이다.

사용자가 제공한 심사 담당 이름·메일·휴대전화는 로컬 파일에만 보관한다:

`~/.config/day/apple/store-contact.local.json` — 권한 600.

- App Review·TestFlight Beta Review 연락처 API 반영·GET 확인
- TestFlight 피드백 이메일·한국어 테스트 안내 반영
- 개인 심사 연락처는 공개 페이지·공개 프로필 문서에 복사하지 않음
- 데모 계정·비밀번호는 사용자가 직접 입력. App Review·Beta Review 모두 빈칸 유지

심사 메모는 원천 §5-3의 **블록 A만 ASC에 등록**했다. 블록 B는 사용자가 데모 자격을 입력하고 실제 로그인·데모 데이터·푸시를 확인한 뒤에만 추가한다. 미확인인데 데모 로그인이 성공한다고 완료형으로 제출하지 않는다.

## 9. 개인정보 문안 권장안과 판단 정정

사용자는 운영주체·보관/삭제 기준을 권장안으로 준비하라고 위임했다.

작성 방향:

- 운영사: Medisolve AI Co., Ltd.
- 개인정보 문의·권리행사 창구: DAY 지원팀 / 공개 지원메일
- 병원 EMR 원본 보존 기준은 병원·EMR 기준
- DAY 계정·동기 사본·채팅/첨부는 서비스 제공·연동에 필요한 범위·기간
- 목적 달성·유효한 삭제 요청·이용 관계 종료로 불필요해진 정보 파기, 법령상 보존분 분리
- 화면 삭제/soft delete와 서버 물리 파기 구분
- 첨부는 남은 참조가 없을 때 기존 코드 계약대로 삭제
- 구현되지 않은 자동 파기를 약속하지 않음
- 비밀번호 미저장 문구는 「로그인할 때 입력한 직원 비밀번호」로 범위 한정
- 심사 담당자를 개인정보보호책임자로 임의 지정하지 않음
- 시행 예정일 2026-11-12, 실제 공개일에 맞춰 갱신

공개 전 사실 대조가 남은 것: 서버·DB·Blob 위탁/보관 지역, Soniox 별도 계약·프로젝트 설정, 로그 내용·보관 기간, 백업, soft delete 데이터 등의 실제 물리 파기 절차. 이미 확인된 사실처럼 쓰지 않았다.

초기 「통역 음성에 개인정보가 있다」「별도 동의 팝업이 무조건 필수」라는 단정은 사용자 지적 후 정정했다. 그 판단을 재사용하지 않는다.

현재 정리:

- 단순 통역만으로 개인정보 포함을 단정하지 않음
- 실제 개인정보 제3자 공유가 있을 때 Apple 5.1.2(i) 적용 조건 확인
- 별도 동의 팝업 임의 추가 없음
- DAY 서버는 통역 대화를 기록하지 않는 코드/SPEC
- Soniox 공개 정책상 실시간 콘텐츠는 일시 처리·미저장, 학습·평가·개선 미사용
- 콘텐츠 없는 운영 메타데이터는 별도 보관
- 개별 계약·설정을 검증했다고 주장하지 않음

공식 근거: [Soniox Privacy Policy](https://soniox.com/policies/privacy-policy), [Security and privacy](https://docs.soniox.com/security-and-privacy).

## 10. 서류 검수

독립 검수 WARN(FAIL 0). 다음 3건을 원 작성자가 수정하고 코디가 확인했다:

1. 비밀번호 미저장 문구를 직원 로그인 입력값으로 한정
2. 앱 설명의 불필요한 부정 대비문 제거
3. 미확인 데모 완료형 문단을 조건부 블록으로 분리

문서 lint 오류 0, 개인 심사 연락처·데모 자격 공개 문서 혼입 0, 최종 설명 원천·txt·API GET 일치 확인.

## 11. 미실행·미완 항목

**실행하지 않은 것:** TestFlight 테스터 추가/그룹 배포, App Store 심사 제출, Unlisted 신청, 공개 출시, 실제 환경 로그인, 정식 앱의 데모 환경 로그인 넘김 실물 확인, 실제 푸시·채팅/첨부·통역 통합 확인, 페이지 공개 접근 200 확인.

**심사 전 남은 것:**

- prod 서버·데모 연결·푸시 M-20 및 두 로그인 실물 검증
- `/privacy`·`/support` 구현·공개·서버 설정과 문안 대조
- 앱 내부 개인정보 페이지 링크
- 예약현황 「곧 출시 예정」 처리 결정
- App Privacy·연령 등급·가격/판매 지역·저작권·콘텐츠 권리 등 미완 칸
- 심사 데모 자격 입력·검증 후 메모 블록 B 추가

등록 완료를 전체 심사 준비 완료라고 표시하지 않는다. 사용자 마지막 서류 후속 작업에서는 추가 빌드·업로드·테스터 배포·심사 제출·출시·자동 스케줄 생성 없음.

## 12. 재개 순서

사용자가 재개를 지시하면:

1. 현재 prod/dev 서버·ASC 상태를 다시 확인한다.
2. 사용자 준비 관리자 계정으로 **같은 정식 앱 → 실제 환경(prod)** 로그인·병원·권한을 확인한다.
3. 사용자 준비 데모 계정으로 **같은 정식 앱 → 데모 환경(dev)** 로그인 넘김을 확인한다.
4. `environment`·`api_base_url`·세션·기기 등록이 올바른 환경에 묶이는지 확인한다.
5. 두 로그인 결과를 각각 기록한다.
6. 지정 테스트 대상에서 조회·상태 변경·채팅·첨부·푸시·통역을 확인한다.

관리자 테스트 계정과 심사 데모 계정은 구분한다. 상태 변경은 실제 병원 EMR에 반영되므로 사용자 승인 범위·지정 테스트 대상에서만 실행한다.

앱 수정이 없으면 기존 빌드(1)을 사용하고, 앱 변경이 있으면 빌드2 이상으로 새로 생성한다.

## 13. 먼저 읽을 결과 문서

이 인계문과 같은 프로필 작업 폴더(`orchestration/work/prod-deploy-re1/`) 기준이다.

| 파일 | 역할 |
| --- | --- |
| [mobile-status.md](mobile-status.md) | 최신 재개점·사용자 대기 지시 |
| [mobile-paperwork-registration.md](mobile-paperwork-registration.md) | 최신 서류·연락처·TestFlight 메타데이터 반영 |
| [mobile-registration-report.md](mobile-registration-report.md) | 최초 ASC 등록 요약. 설명207자는 당시 값, 최종283자 |
| [mobile-asc-report.md](mobile-asc-report.md) | ASC 메타데이터·이미지·빌드 연결 |
| [mobile-prod-upload-report.md](mobile-prod-upload-report.md) | 정식 IPA 서명·검증·업로드 |
| [mobile-screenshot-report.md](mobile-screenshot-report.md) | 촬영·가짜 데이터·이미지 검증 |
| [mobile-paperwork-report.md](mobile-paperwork-report.md) | 문안 작성·검수 보완 |
| [mobile-paperwork-review.md](mobile-paperwork-review.md) | 독립 서류 검수 |
| [mobile-description-final.txt](mobile-description-final.txt) | 최종 설명283자 / 85ed67f7 |

Apple 키·Team·Issuer·토큰은 출력하지 않는다. 위치는 `orchestration/config/projects/day.json`의 `apple` 섹션을 따르고 실제 값은 `~/.config/day/apple/credentials.local.json`에 있다. 키를 파일명으로 추측하지 않는다. 시뮬레이터용 임시 토큰을 심사·실기기 계정으로 사용하지 않는다.

앱 세션 발주는 전부 결과 수신·검증·release 요청 완료, 활성 발주 없음. 서버·웹 진행 상황과 기존 `_RESUME.md`는 메인 코디가 계속 관리한다.
