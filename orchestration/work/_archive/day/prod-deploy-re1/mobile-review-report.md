> 후속 코디 정정: 이 리포트의 통역 동의 관련 보편적 필수/차단 판단은 사용자 지적 이후 철회했다. 실제 개인정보 공유가 있는 경우의 Apple 조건으로 한정하며 별도 팝업을 임의 추가하지 않았다. 코드 관찰 사실(별도 안내 단계 없음)은 유지한다. 최신 정책 원천은 mediness의 app-store-preparation.md다.

# 리뷰 리포트 — prod-deploy-re1 정식 DAY 앱 제출 준비 / code+doc (2026-11-11)

검수 대상은 코디가 정정한 최신본이다(`mobile-submission-draft.md` 88줄 = 이하 초안, `mobile-build-report.md` 177줄 = 이하 빌드 리포트). 이와 함께 코드 `app/`(HEAD `5f7806d3`)와 빌드 산출물 `app/build/ios/iphoneos/Runner.app`을 대조했다.

방법:
- 읽기 전용으로 검수했다. 빌드 · 테스트는 다시 돌리지 않았고, analyze · test 수치는 빌드 리포트를 인용했다.
- 산출물은 `PlistBuddy` · `strings` · `find` · `sips` · `codesign -dv` · `shasum`으로만 확인했다.
- Apple 규정은 공식 URL로 확인했다(아래 「Apple 규정 확인」).
- 이 파일 하나만 썼다. 소스 · 설정 · `_RESUME.md` · ASC는 바꾸지 않았고, 키 · 토큰 · Team ID · 계정 값은 열지 않았다.

## 판정: WARN (FAIL 0 · WARN 8)

- 빌드 리포트가 적은 빌드 사실(번들 ID · 이름 · 버전 · SDK · origin · 아이콘 · manifest 목록 · 소스 변화 0)은 산출물과 전부 일치했다.
- 제출을 막는 항목은 두 문서 모두에 빠짐없이 적혀 있다: 개인정보 링크, 통역 제3자 AI 고지 · 허가, 예약 탭 「곧 출시 예정」, 앱 record, 서명, 서버 준비, ASC 메타데이터.
- 실물 미확인 항목을 통과로 적은 곳은 없다.
- 남은 문제는 사실 오류 1건(W-3 libwebp)과 분류 · 표현 보강(W-1 · W-2 · W-4 · W-6)이다.
- 예약 탭은 첫 검수 때 누락이었지만 코디 정정으로 두 문서에 들어가 FAIL을 해제했다. 다만 차단 목록에는 아직 없다(W-2).

### 제출 차단과 준비 완료 — 한눈에

| 구분 | 상태 |
|---|---|
| 빌드 준비(서명 없는 release · prod 정의 · 정식 identity) | **준비 완료 — 산출물로 확인** |
| 코드 준비(심사 규정) | **미완 — 소스 변경 3건 필요**: 개인정보 링크(5.1.1(i)), 통역 제3자 AI 고지 · 허가(5.1.2(i)), 예약현황 자리표시(2.1(a)) |
| 사용자 결정 | 미완 — 정식 앱 record(생성 여부 미확인), 첫 제출 버전, 서명 M-16, 개인정보 · 지원 URL, App Privacy, 연령 · 가격 · 지역 |
| 서버(다른 코디) | 미완 — prod D-1(데모 → dev 연결), prod APNs, M-20 |
| 실물 | **미확인** — 서명 IPA entitlements, 업로드 검증, 실기기 로그인 · 푸시 · 통역. 두 문서 모두 미확인으로 정확히 적었다 |

→ **지금은 제출할 수 없다.** 준비 문서는 차단 항목을 정확히 드러낸다.

## FAIL

없음.

## WARN

### W-1. 개인정보 링크 · 통역 외부 전달 — 초안 안의 표현이 서로 다름
- 초안 `:75`는 「앱 내부 개인정보 링크와 통역 외부 전달 고지·허가 흐름 **점검/보완**」이라고 써서 아직 확인 전인 것처럼 읽힌다.
- 같은 초안 `:84`는 「단계가 **없다**」고 확정해서 적었다.
- 코드상 사실은 **둘 다 없음**이다. 검수자가 다시 확인한 근거:
  - `lib/`에서 `개인정보|privacy|약관|동의|consent` 검색 결과 0
  - 통역 연결은 세션 주소의 `wss://…/api/interpret`이다(`lib/interpret/interpret_client.dart:2`).
  - 서버가 Soniox로 중계한다(`backend/day/services/interpret/soniox.py`).
  - 마이크 권한 문장 `ios/Runner/Info.plist:58-59`에 외부 전달 언급이 없다.
- 빌드 리포트 `:135-146` · `:158-159`는 정확하다.
- 권고: 초안 `:75`를 「확인된 차단 · 소스 변경 필요」로 맞춘다.
- 규정: 5.1.1(i)(앱 안 개인정보 링크), 5.1.2(i)("including with third-party AI, and obtain explicit permission").

### W-2. 예약 탭 「곧 출시 예정」 — 기록은 됐지만 차단 목록 밖에 있음
- 코드: `app/lib/ui/shell.dart:212-215`에서 `AppTab.reservations` 본문이 `Text(comingSoon)` 하나뿐이다. 문구는 `app/lib/core/copy.dart:62` `'곧 출시 예정'`이고, 하단 4메뉴 중 하나다(`shell.dart:26`).
- 규정: 2.1(a) "placeholder text, empty websites, and other temporary content should be scrubbed before submission". Unlisted도 "beta or prerelease state"면 거절한다.
- 문서:
  - 초안 `:85`는 「보완 후보」로 적었다. 하지만 「제출 전 남은 일」(`:73-80`) 번호 목록에는 없다.
  - 빌드 리포트 `:152-154`는 별도 절로 적었다. 하지만 「제출을 막는 항목」(`:156-163`) 번호 목록에는 없다.
- 권고: 두 문서 모두 차단 목록 번호 항목으로 올린다. 처리(탭 숨김 또는 기능 완성)는 DAY-SPEC-003 메뉴 개정이 먼저이며 사용자가 결정한다.

### W-3. libwebp를 Apple 「commonly used SDK」 목록 대상이라 쓴 것은 사실 오류(빌드 리포트)
- 빌드 리포트 `:97`은 「libwebp · SDWebImage 계열은 Apple 목록 대상」이라고 적었다.
- Apple 목록(https://developer.apple.com/support/third-party-SDK-requirements/)에는 `SDWebImage`만 있다. **`libwebp` · `SDWebImageWebPCoder`는 없다.** 다만 "SDKs that repackage those on the list" 조항은 있다.
- 산출물 확인(검수자 `find`):
  - `SDWebImage_SDWebImage.bundle/PrivacyInfo.xcprivacy`는 들어 있다.
  - `build/ios/SourcePackages/checkouts/{libwebp-Xcode,SDWebImageWebPCoder}`에는 manifest가 없다.
- 결과: ITMS-91061 위험은 리포트 서술보다 낮다. 「업로드 뒤 Apple 메일 미확인」으로 둔 처리(`:101` · `:168`)와 초안 `:86`(「단정하지 않는다」)은 맞다. `:97` 문구만 고치면 된다.

### W-4. 스크린샷 규격 예시가 iPhone 필수 세트를 보장하지 않음(초안)
- 초안 `:69`는 「iPhone 1206×2622 … 허용 규격의 예」라고 적었다. 1206×2622는 6.3" 규격이다.
- Apple 표에서 6.5" 행은 "Required if app runs on iPhone and screenshots for iPhone with Dynamic Island (large display) aren't provided"다. 따라서 6.9"(1320×2868 · 1290×2796) 또는 6.5" 세트가 필요하다. 출처: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/
- 검수자는 표의 행 원문이 아니라 요약 추출본으로 읽었다. 촬영 전에 ASC 화면에서 필수 칸을 다시 확인해야 한다. 안전한 선택은 6.9" 1320×2868이다.
- iPad 13" 2064×2752는 "Required if app runs on iPad"다. `UIDeviceFamily [1,2]`(산출물 확인)이므로 필수이고, 초안이 맞다.

### W-5. `aps-environment` 실물 미확인 — 정확히 미결로 기록됨
- 소스 `ios/Runner/Runner.entitlements:5-6`의 값은 `development`다.
- 산출물은 서명이 없다(`codesign -dv` = "code object is not signed at all").
- 빌드 리포트 `:69` · `:167`은 「배포 export 때 production으로 바뀜(DAY Dev IPA 근거) · 정식 앱 실물 미확인」이라고 적었다. 정확하다.
- 권고: 서명 단계에서 entitlements가 `production`인지 확인하는 항목을 남긴다. 계약은 APNs production이다.

### W-6. 최소 iOS 13.0 — 빌드 리포트가 지나치게 보수적이고, 초안에는 언급이 없음
- 산출물의 `MinimumOSVersion`은 `13.0`이다.
- Apple 현재 규정은 "Since September 9, 2026: iOS and iPadOS apps … must target iOS 13 or later"다(https://developer.apple.com/news/upcoming-requirements/). 따라서 **규정상 지금 제출 가능**하다.
- 빌드 리포트 `:59`의 「업로드 가능 여부 미확인」은 정식 번들 업로드를 실제로 하지 않았다는 뜻이라 틀리지는 않다. 다만 규정 근거를 같이 적는 편이 정확하다.
- 「2027-04 전 15.0 필요」(`:43` · `:175`)는 altool 경고 90068 인용이다. 현재 Apple 페이지에는 이 일정이 아직 나오지 않으므로 「업로드 경고 기준」이라고 출처를 밝혀 두는 것을 권한다.
- 초안 「제출 전 남은 일」에 M-7 주의 한 줄을 넣을 것을 권한다.

### W-7. 앱 자신의 `PrivacyInfo.xcprivacy` 없음 — 정확히 기록된 미결
- 산출물의 manifest 7개는 모두 Flutter · 플러그인 번들 것이고 Runner 수준 manifest는 없다. 빌드 리포트 `:91` · `:99-101` · `:177`과 일치한다.
- 검수자 확인: manifest가 없는 플러그인(audio_session · flutter_image_compress_common · flutter_tts · flutter_pcm_sound)의 iOS 소스에 UserDefaults · 파일 타임스탬프 · boot time · 디스크 용량 API가 없다.
- W-1을 고칠 때 동의 상태를 UserDefaults에 두면 `CA92.1` 선언이 필요하다. 빌드 리포트 `:144`의 지적이 정확하다.

### W-8. 초안의 추론과 사실 구분 — 대체로 정확함
- 정확한 곳:
  - URL 미정(`:18-19`)
  - 심사 메모는 실물 확인 뒤에만 제출(`:43`)
  - Unlisted 신청서에 기기 · 규모를 추측해 넣지 않음(`:49`)
  - Unlisted는 「심사 제출 상태에서 신청」(`:51`). Apple 원문과 같다.
  - App Privacy를 「수집하지 않음」으로 일괄 선택하지 않음(`:55`)
  - 공급자 재사용 여부는 코드로 확정할 수 없음(`:65`)
  - 스크린샷 미생성(`:71`)
  - 서명 없는 빌드는 업로드용이 아님(`:88`)
- 빌드 리포트의 정정도 맞다:
  - Unlisted는 「심사 제출 뒤 신청 · 통과 대기 불필요」(`:163`). Apple 원문 "submitted to App Review"와 같다.
  - ASC record 「생성 여부 미확인」(`:160`)
  - Soniox 보관 미확인(`:144` · `:169`)
- 보강 권고: 초안 `:39`의 「회원가입 기능 없음」은 사실이다(빌드 리포트 `:122`). 이것이 5.1.1(v) 계정 삭제가 적용되지 않는 근거이므로, 심사 메모에 「계정은 병원이 발급」을 함께 적을지 사용자가 판단한다.

## 빌드 리포트와 산출물 대조 (검수자 재확인 · 재빌드 없음)

| 빌드 리포트 주장 | 산출물 확인 | 결과 |
|---|---|---|
| `CFBundleIdentifier day.medisolveai`, 이름 `DAY` (`:56-57`) | 동일 | 일치 |
| 버전 `0.1.0` · `1` (`:58`) | 동일, `app/pubspec.yaml:5` `0.1.0+1` | 일치 |
| `MinimumOSVersion 13.0`, `UIDeviceFamily [1,2]` | 동일 | 일치 |
| `DTSDKName iphoneos26.2`, `DTXcode 2620` | 동일. 로컬 Xcode 26.2이므로 Apple 「Xcode 26 · iOS 26 SDK」 규정 충족 | 일치 |
| `ITSAppUsesNonExemptEncryption false` | 동일 | 일치 |
| origin: prod 2회 · dev 1회 (`:76-77`) | `strings App` 결과 `day.medisolveai.com` 2회, `day-dev.medisolveai.com` 1회 | 일치 |
| debug 설정 혼입 0 (`:80`) | `127.0.0.1` · `day-local` · `ngrok` 0. release는 로컬 origin을 무시하고 환경 칸 필수를 강제한다(`lib/core/build_config.dart:48-50`) | 일치 |
| `App` sha256 앞 16자 `ea0292c4b83ae20b` (`:48`) | 동일 | 일치 |
| Frameworks `App` · `Flutter` · `flutter_pcm_sound` (`:70`) | 동일 | 일치 |
| manifest 목록 (`:89-97`) | Flutter · photo_manager · SDWebImage · image_picker_ios · record_ios · url_launcher_ios · video_player_avfoundation 7개 | 일치 (`:97` 목록 대상 서술은 W-3) |
| 아이콘 1024 알파 없음 (`:64`) | `sips` 결과 hasAlpha no, 1024×1024 | 일치 |
| 서명 없음 | `codesign -dv` "not signed at all" | 일치 |
| 소스 변화 0, 임시 `Identity.local.xcconfig` 삭제 (`:29` · `:150`) | `git status --short app` 빈 결과, 파일 없음 | 일치 |
| analyze 0, test 343 통과 · 73 skip · 0 실패, build exit 0 (`:16-18`) | 재실행 금지라 로그 경로(`:49`)만 인용 | 미검증(인용) |

계약(브리프 §3) 준수: 빌드 인자(`:22-27`)와 산출물이 일치한다.
- ID `day.medisolveai`, 이름 `DAY`
- 로그인 진입점 prod, 허용 origin prod + dev
- `DAY_APNS_ENV=production`, `DAY_REQUIRE_ENVIRONMENT=true`

실제 APNs 환경은 서명 뒤 확인한다(W-5).

## Apple 규정 확인 (공식 URL · 2026-11-11)

- **Review Guidelines** — https://developer.apple.com/app-store/review/guidelines/
  - 2.1(a) 자리표시 제거, 2.2 데모 · 베타 금지 (원문)
  - 5.1.1(i) 앱 안 개인정보 링크, 5.1.1(v) 계정 생성을 지원할 때만 삭제 기능 필요, 5.1.2(i) 제3자 AI 포함 고지와 명시적 허가 (요약 추출본)
- **Upcoming requirements** — https://developer.apple.com/news/upcoming-requirements/
  - 2026-04-28부터 Xcode 26 · iOS 26 SDK
  - 2026-09-09부터 iOS 13 이상 대상
- **Unlisted** — https://developer.apple.com/support/unlisted-app-distribution/
  - "already be on the App Store or be ready for final distribution and submitted to App Review"
  - 리뷰 노트에 의도를 적은 뒤 신청
  - 베타 · 프리릴리스는 거절
- **Third-party SDK** — https://developer.apple.com/support/third-party-SDK-requirements/
  - 목록 대상: image_picker_ios · url_launcher_ios · video_player_avfoundation · SDWebImage · Flutter. 모두 manifest가 들어 있음을 확인했다.
  - 목록 밖: libwebp · SDWebImageWebPCoder · record · photo_manager · audio_session · flutter_tts · flutter_image_compress
- **Screenshot** — W-4 참조.

## 직원이 실물에서 만날 자리

- 하단 첫 탭 「예약현황」을 누르면 「곧 출시 예정」 한 줄만 보인다. 심사관도 같은 화면을 본다(W-2).
- 통역을 열면 안내 없이 바로 마이크가 켜지고 음성이 외부(Soniox)로 간다(W-1).
- 설정 탭에는 이름 · 병원 · 로그아웃만 있고 개인정보처리방침이 없다(`app/lib/ui/shell.dart:418`).
- 심사용 데모 로그인과 푸시는 prod 서버 D-1과 M-20이 끝나야 동작한다(서버 코디 몫 · 미확인).

## 참고(기존 부채)

- flutter_pcm_sound · flutter_tts SPM 미지원 경고. 앞으로의 Flutter 버전에서 오류가 된다(빌드 리포트 `:35-41`).
- mobile-deployment.md §6 `:169`는 Unlisted를 「App Review 통과 뒤」라고 적었다. Apple 원문은 「심사 제출 뒤」이므로 문서 담당에 전달할 것을 권한다.
- 정식 서명 우회 절차가 저장소 문서에 없다(M-16 · 빌드 리포트 `:161`).

## 코디 후속 반영(검수 종료 뒤 · 재빌드 없음)

W-1: 초안 ‘점검/보완’을 ‘현재 없는 흐름을 추가’로 변경. W-2: 예약 탭을 빌드 리포트 번호 차단 목록 및 초안 제출 전 순서에 추가. W-3: Apple 목록 직접 확인 후 SDWebImage만 명시됨·libwebp/WebPCoder 이름 비명시·재패키징 여부 별도로 정정. W-4: iPhone 촬영 계획을 1320×2868로 변경하고 ASC 필수칸 대조를 남김. W-6: 최소 OS와 종전 업로드 경고를 초안에 추가. W-5·W-7 및 실기기/공급자 보관 검증은 미확인으로 유지. 이는 코디의 문서 수정 기록이며 독립 검수 재실행을 뜻하지 않는다.
