# DAY Dev 0.2.0 빌드 · 업로드 결과 보고 — iOS TestFlight 빌드 4 · Android internal vc4

## 상태: done — 둘 다 올라감 · TestFlight `0.2.0 (4)` VALID · 내부 테스트 `IN_BETA_TESTING` · Play internal `4 (0.2.0)` completed

- 빌드 커밋: `git fetch origin && git checkout --detach origin/dev` = **`5ece25ea`**(PR #266 스쿼시). 트리 `c67d6c71…` = 브랜치 HEAD `8a76c35b` 트리와 **같음** 확인 후 빌드. 소스 수정 0 · 커밋 0.
- 정식 앱(`day.medisolveai`) 빌드 · 업로드 0. 테스터 · 그룹 · 심사 제출 0. 사용자 기기 · 시뮬레이터 무접촉.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰 · 서명 인증서 식별자는 적지 않았다(셸 변수로만 읽음).

## iOS — DAY Dev `day.medisolveai.dev` 0.2.0 (4)

절차 = 지난 업로드(빌드 1 5차 · 빌드 2)와 같음. 임시 파일은 `app/build/tf4/`(무시 폴더).

| 단계 | 결과 |
|---|---|
| config(`flutter build ios --release --config-only --build-name=0.2.0 --build-number=4` + `DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = `https://day-dev.medisolveai.com` · `DAY_APNS_ENV=production`) | OK |
| archive(서명 없이 · `DAY_BUNDLE_ID=day.medisolveai.dev` · `DAY_DISPLAY_NAME=DAY Dev` · `CODE_SIGNING_ALLOWED=NO`) | **ARCHIVE SUCCEEDED** |
| 앱만 `Runner.entitlements` 로 ad-hoc 서명 | OK |
| export(app-store-connect · 자동 서명 · `-allowProvisioningUpdates` · DAY API 키) | **EXPORT SUCCEEDED** · IPA 22,279,042 bytes |
| `altool --validate-app` | **VERIFY SUCCEEDED** · 오류 0 · 경고 2(아래) |
| `altool --upload-app` | **UPLOAD SUCCEEDED** · 22,279,042 bytes · 18:55 KST |
| ASC 처리(19:00 조회) | **VALID** |

### IPA 확인
| 항목 | 값 | 결과 |
|---|---|---|
| `CFBundleIdentifier` · `CFBundleDisplayName` | `day.medisolveai.dev` · `DAY Dev` | OK |
| `CFBundleShortVersionString` · `CFBundleVersion` | `0.2.0` · `4` | OK |
| `ITSAppUsesNonExemptEncryption` | `false` | OK |
| 아이콘 | `AppIcon60x60@2x.png` · `AppIcon76x76@2x~ipad.png` · `CFBundlePrimaryIcon` | OK |
| entitlements | `aps-environment = production` · `beta-reports-active = true` · `get-task-allow = false` · application-identifier · team-identifier | OK |
| 서명 | `Apple Distribution: Medisolve AI Co., Ltd. (<가림>)` · `codesign --verify --deep --strict` 통과 | OK |
| 프로파일 | `iOS Team Store Provisioning Profile: day.medisolveai.dev` | OK |
| 서버 주소(`App.framework`) | `https://day-dev.medisolveai.com` 만(API 대상). 그 밖 `https://day.medisolveai.com/privacy` = 설정 화면 개인정보 처리방침 고정 링크(`lib/ui/shell.dart:464` 상수 · 서버 대상 아님) | OK |

### ASC 빌드 상태(DAY Dev)
| 버전 (빌드) | processingState | usesNonExemptEncryption | 내부 | 외부 |
|---|---|---|---|---|
| **0.2.0 (4)** | **VALID** | false | **IN_BETA_TESTING** | READY_FOR_BETA_SUBMISSION(제출 안 함) |
| 0.1.0 (4) · (3) · (2) · (1) | VALID | false | IN_BETA_TESTING | 〃 |

- 빌드 번호 4 는 0.1.0 에도 있다(ASC 는 버전마다 빌드 번호를 따로 셈 — 0.2.0 의 4 로 받아들여짐).
- 수출 규정 누락 없음(`MISSING_EXPORT_COMPLIANCE` 아님) → 이미 있는 내부 테스터는 바로 받을 수 있다.
- validate · upload 경고 2(막지 않음): **90068** 배포 대상 iOS 13.0 → 2027-04 부터 15.0 이상 · **90725** iOS 26.2 SDK → 2027-04 부터 iOS 27 SDK(Xcode 27) 이상. 소스 · 도구 변경이 필요 — 범위 밖.
- 새 서명 자산: 프로비저닝 프로파일 폴더 새 파일 0(작업 시각 이후) · 기존 클라우드 배포 인증서 · App Store 프로파일 재사용.

## Android — DAY Dev `day.medisolveai.dev` 0.2.0 (versionCode 4)

| 단계 | 결과 |
|---|---|
| `~/.config/day/android/google-services.json` → `app/android/app/google-services.json` 복사(빌드 뒤 지움) | OK |
| `flutter build appbundle --release --build-name 0.2.0 --build-number 4` + `DAY_APPLICATION_ID=day.medisolveai.dev` · `DAY_APP_NAME=DAY Dev` · `DAY_UPLOAD_KEY_PROPERTIES=~/.config/day/android/upload-key.properties` · dev `--dart-define` 2개(`DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = `https://day-dev.medisolveai.com` — 지난 Android dev 빌드와 같음) | ✓ 55.7MB |
| 사본 `~/.config/day/android/out/DAY-Dev-0.2.0-4.aab`(600) | sha256 `67a2deb0df0478c8dc18ccf34fb578faca43f350dc0140a6d7e104eed5091252` |
| `play_upload.py upload … --track internal --expect-version-code 4 --release-name '4 (0.2.0)' --dry-run` | upload vc 4 · tracks.update · **edits.validate ok** · edit 삭제 |
| 같은 명령 실제 | **edits.commit ok** → `internal: name='4 (0.2.0)' versionCodes=['4'] status=completed` · 18:59 KST |

출시 노트(ko-KR · 원천 = PR #266 제목 요약): 「0.2.0 — 기기 선택 · 바로 시작 · 호출 취소 · 원장 바꾸기 · 방 옮기기 · 호출 취소 알림 · Android 푸시 · 통역 개선」.

### AAB 확인
| 항목 | 값 | 결과 |
|---|---|---|
| package | `day.medisolveai.dev` | OK |
| versionCode | 4(`play_upload --expect-version-code 4` 통과) · versionName `0.2.0` | OK |
| Firebase | `google_app_id` 리소스 있음 · **dev 앱의 Firebase app id 있음 · 정식 앱 id 없음**(google-services.json 과 대조 · 값 미출력) | OK |
| 푸시 구성 | `DayMessagingService` · `AcceptReceiver` · `POST_NOTIFICATIONS` 매니페스트에 있음 | OK |
| 서버 주소(`libapp.so`) | `https://day-dev.medisolveai.com` 만(+ 위와 같은 개인정보 처리방침 고정 링크) | OK |
| 서명 | `jar verified` · SHA-256 `92:75:54:AE:…:F9:A9:69:AD` = 업로드 키(지난 빌드와 같음) | OK |

## 정리 · git
- `app/android/app/google-services.json` 지움 · 풀어 본 IPA · AAB 폴더 지움(산출물 · 로그는 `app/build/tf4/` 무시 폴더에 남음).
- 워크트리를 `kknaksss/day-mobile-v2`(`8a76c35b`)로 되돌림:
```
On branch kknaksss/day-mobile-v2
Your branch is up to date with 'origin/kknaksss/day-mobile-v2'.

nothing to commit, working tree clean
```

## 다음
- 실기기 확인(A-50): TestFlight DAY Dev 0.2.0 (4) · Play 내부 테스트 4 (0.2.0).
- 정식 0.2.0 은 prod 서버 배포 뒤(스펙 개정 ⑲ 순서) — 이번 범위 아님.
- 2027-04 전: iOS 배포 대상 15.0 · Xcode 27(경고 90068 · 90725).
