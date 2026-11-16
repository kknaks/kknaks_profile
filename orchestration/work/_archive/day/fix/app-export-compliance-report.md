# [mobile] 수출 규정(암호화) 자동 답 결과 보고

## 상태: done

워크트리 `CENTURION_DAY/fix` (`kknaksss/fix`). 커밋 · push · PR · 재빌드 · 재업로드 0. 비밀값(Key ID · Issuer ID · Team ID · 키 · 토큰) 미기재 — ASC 호출은 `credentials.local.json` 의 `app_store_connect.private_key_path` 로만.

## 1. 확인 — 면제 범위만 쓰는가: **예**

| 어디 | 무엇 | 판단 |
|---|---|---|
| `pubspec.yaml` 직접 의존 | http · crypto · flutter_tts · record · audio_session · flutter_pcm_sound · image_picker · flutter_image_compress · photo_manager · video_player · url_launcher | 암호화 라이브러리는 `crypto` 하나(해시 전용 패키지) |
| `lib/interpret/interpret_client.dart:14,82` | `package:crypto` 의 `sha1` — 통역 WS 핸드셰이크 `Sec-WebSocket-Accept` 검증(RFC 6455) | 해시 · 인증 — 데이터 암호화 아님 |
| `lib` 전체 | `pointycastle` · AES · RSA · encrypt/decrypt · 자체 cipher 없음. 통신은 https/wss(`lib/core/origin.dart` 가 https 만 허용) | TLS — 면제 |
| `ios/Runner/AppDelegate.swift` | Keychain `SecItemAdd/Update/CopyMatching/Delete` · `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` — 세션 묶음 저장 | OS 제공 — 면제 |
| 플러그인 네이티브 | photo_manager `PMHashUtils.m` CommonCrypto `CC_SHA256`(다이제스트) · SDWebImage `SDDiskCache.m` `CC_MD5`(캐시 파일 이름) | OS 해시 — 면제. `CCCrypt` · CryptoKit · SecKey · OpenSSL 사용 0 |
| `pubspec.lock` 전이 의존 | 암호화 패키지 없음 | — |

참고: Flutter 엔진 dart:io 의 TLS 는 엔진에 든 BoringSSL 로 한다 — 표준 TLS(HTTPS) 용도라 면제 범주로 봤다. 자체 · 비표준 암호화 구현은 없어 멈출 사유 없음.

## 2 · 4. 변경 파일(이번 판)

| 파일 | 변경 |
|---|---|
| `app/ios/Runner/Info.plist` | `ITSAppUsesNonExemptEncryption` = `<false/>` 한 키(+2줄) |
| `app/README.md` | 「수출 규정(암호화)」 절 — 키 뜻 · `false` 근거(위 1) |

- `plutil -lint app/ios/Runner/Info.plist` → OK
- `git diff --stat` → `Info.plist | 2 +` · `README.md` · 그리고 앞 판(아이콘)의 미커밋 `Contents.json`(이번 판 변경 아님). 아이콘 PNG · `assets/brand/` 는 앞 판 그대로(untracked).

## 3. 빌드 1 에 답 넣기 — ASC API

- 대상: 앱 `day.medisolveai.dev` · 빌드 번호 1 (조회 결과 정확히 1개)
- `PATCH /v1/builds/{id}` `usesNonExemptEncryption: false` → **200**
- 재조회:

| 항목 | 전 | 후 |
|---|---|---|
| 버전 · 빌드 | 0.1.0 · 1 | 0.1.0 · 1 |
| processingState | VALID | VALID |
| usesNonExemptEncryption | null | **false** |
| buildBetaDetail internal | MISSING_EXPORT_COMPLIANCE | **READY_FOR_BETA_TESTING** |
| buildBetaDetail external | MISSING_EXPORT_COMPLIANCE | **READY_FOR_BETA_SUBMISSION** |

정식 앱 `day.medisolveai` · 테스터 · 그룹 · 베타 심사 손대지 않음.

## 미결

- 다음 빌드(2 이상)부터 Info.plist 키로 자동 답이 된다 — 다음 업로드 때 `usesNonExemptEncryption=false` 로 바로 서는지 확인.
- 내부 테스터 추가(사용자) 뒤 실기기 설치 가능.
- 이 변경은 미커밋(코디가 PR).
