# [planner] 마감 리포트 — 스펙 사실 반영(spec-sync) + Delivery #251 마감 sync (2026-11-16)

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec`, 브랜치 `kknaksss/android-app-close`. base는 `origin/main` `b051a299`로, #940 `855bab4f`와 #941 개정 ⑮가 이미 들어 있다.
- 미커밋 상태다. 커밋 · push · PR은 하지 않았다.
- 코드 워크트리(`CENTURION_DAY/android-app`)는 읽기만 했다. `4f8316a7` 기준으로 사실을 대조했다.

## 결과 한 줄

스펙 7파일이 바뀌었다(+79 / −57). lint `--strict`는 exit 0이다. products/day 기준 ERROR 0, WARN 0이다.

Delivery #251 판정은 **conformant**다.
- 근거: 코드 PR #253이 머지됐고, A1~A7은 모두 pass다.
- 범위 밖 3건이 같은 PR에 들어갔다. F1 · 정식 앱 · 프로덕션이다. 셋 다 Delivery 승인 뒤 사용자 결정으로 늘어난 것이라 그대로 적었다.

## 변경 파일

| 파일 | 무엇 |
|---|---|
| `products/day/40-architecture/mobile-deployment.md` | 개정 노트 2026-11-16 ④ 한 문단을 더했다. §1 · §1-1 · §3 · §7-0~7-3-2 · §8-1 · §9 · §9-1 · §12 · §13의 사실과 다른 줄을 고쳤다(43곳 + [설정 완료] 1곳) |
| `products/day/20-spec/spec-003-mobile-app.md` | 개정 ⑯ 노트 · §1 범위 표에 행 하나 추가 · 범위 밖 줄 · §2 Placement F1 한 줄 · §3 세션 저장 · 채널 절 3줄 · A-48 · A-49 실물 칸 |
| `products/day/20-spec/spec-004-internal-chat.md` | 「개정 ⑯ 맞춤」 노트 · §1 「뺌」의 Android 줄 · last_updated |
| `products/day/20-spec.md` | 범위 밖 줄에서 「Android 정식 앱 · 출시」를 빼고 「Android 푸시」만 남겼다 · 최종 수정 |
| `products/day/40-architecture/README.md` | mobile-deployment 설명이 「설정은 아직 안 함」이라 틀려서 고쳤다 |
| `products/day/30-work.md` | Spec Coverage의 SPEC-003 · SPEC-004 행에 #251 추가 · Delivery 대시보드에 #251 행 추가 · 최종 수정 |
| `products/day/log.md` | 두 행 추가 — spec-sync(arch-change, spec-change) 한 행, Delivery 마감(wp-status) 한 행 · 최종 수정 |

---

## A. 스펙 사실 반영 — 전수 표

### 전수 범위

브리프 grep으로 222줄 · 20파일이 걸렸다.
- `mobile-deployment` 125 · `spec-003` 21 · `log.md` 16 · `spec-000` 15 · `deployment.md` 11 · `60-release` 8 · `planning/*` 13 · `spec-004` 3 · `spec-002` 3 · `README`/`erd` 4 · `spec-005` 2 · `20-spec.md` 1
- 고치지 않은 줄은 셋 중 하나다. 아래 사실과 이미 맞거나, 이번 사실과 무관하거나, 오탐이다.

| 묶음 | 줄 | 판단 |
|---|---|---|
| `spec-000` 15줄 · `erd.md` 2줄 | `display_request` · `displayName` · `display_channels` | 「play」 부분 일치 오탐 |
| `00-baseline/planning/*` 13줄 | 「CC 미결 N」 | CC 기획안의 미결 번호라 Android와 무관하다. 그리고 baseline이다 |
| `deployment.md` 11줄 · `60-release` 8줄 | `day.medisolveai.com` 도메인 · iOS ASC | 서버 · iOS 사실이라 이번 범위 밖이다 |
| `spec-002` 3줄 · `spec-000:1387` | 「미결」(OQ-54 · KOS 운영 확인) | 무관 |
| `spec-005:68` | 「Android · FCM — mobile-deployment 미결 그대로」 | 사실 그대로다. FCM은 범위 밖 · [미결]이다 |
| `spec-004:454` | 채팅 푸시 「Android 는 넓히지 않」 | 사실 그대로다(FCM 없음) |
| `log.md` 16줄 | 과거 행 | 이력이라 고치지 않는다 |
| `mobile-deployment` 나머지 | §2 그림(Android · FCM 후보) · §4 flavor [제안] 일반 설명 · §7-3 표의 APK · managed Play 후보 · §7-4 개발자 인증 · M-15 · §14 링크 · 2026-11-12 ② / 11-13 ③ 개정 노트(이력) · §7-3-1 「확인 안 됨」 중 문서 근거가 여전히 없는 칸 | 사실과 맞거나 일반 설명 · 이력이다. §7-3-1 칸은 「문서 근거 = 확인 안 됨」을 그대로 두고 실제 결과만 덧붙였다 |

### 고친 줄

- 줄 번호는 `origin/main` 기준이다.
- 「전」은 요지만 적었다. 「후」는 이번에 넣은 사실이다.
- 근거 약어:
  - R = `_RESUME.md` §2(결정) · §5(이력)
  - A1~A6 = `app-1~6-report.md`
  - C = 코드 `4f8316a7` 직접 확인
  - B = 브리프 사실 번호

#### mobile-deployment.md

| 파일:줄 | 전 | 후 | 근거 |
|---|---|---|---|
| :7 | last_updated 2026-11-13 | 2026-11-16 | — |
| :22 뒤(새 줄) | — | 개정 노트 2026-11-16 ④. 아래 줄들을 요약하고 「그대로」 목록(FCM · 알림 [수락] · 동영상 · 백업 · CI · 빌드 번호)을 둔다 | B1~9 |
| :39 §1 | 정식 앱 출시 · 정식 배포 범위 밖 · M-17 [미결] | ~~취소선~~ → [확정] 정식 앱(`DAY` · `day.medisolveai` · prod)도 Play에. 비공개 테스트 → 프로덕션 출시 진행(2026-11-15 심사 제출). M-17 닫음. 푸시는 범위 밖 | R §2 11-13 · 11-15 · B1 |
| :41 §1 | 최종 배포 = 비공개(Unlisted) | 덧붙임: 「이 줄은 iOS다 — Android 정식은 Play 프로덕션(공개) 트랙. 앱 로그인으로 막는 것은 같다」 | R §2 11-15 · B1 |
| :48 §1 | M-1 「Android 방식 §7-3 에 영향」 | 취소선 → Android 방식은 사용자가 정함 | R §2 11-15 |
| :49 §1 | 정식 앱 Android id [미결](M-4) | `day.medisolveai`. M-4 닫음 | R §2 11-13 · B1 |
| :54 §1-1 제목 | 지금 상태 (2026-11-12) | (· Android 2026-11-16) | — |
| :64 §1-1 | 개발 앱 Play 앱 · 첫 업로드 · 업로드 키 · 서비스 계정 「아직 안 함」 | 취소선 → [설정 완료] 4줄을 새로 넣었다. 아래 표 참고 | — |
| :64 §1-1 ① | (새 줄) | Play 앱 둘 · Play 앱 서명 · 업로드 키 하나를 공유 | R §5 11-13 · 11-14 · A4 |
| :64 §1-1 ② | (새 줄) | 트랙 이력: 개발 internal vc1(손) → vc3(API) · 정식 비공개 vc1(손 · 11-14) → vc3(API · 11-15) → 프로덕션 vc3 심사 제출(대한민국 · 관리형 게시 꺼짐) | R §5 · A5 · A6 |
| :64 §1-1 ③ | (새 줄) | 「Play 업로드 전용 서비스 계정 · 키 로컬 · 조직 정책상 키 생성이 막혀 프로젝트 한정 재정의로 한 번 발급」. 이름 · 이메일은 적지 않았다 | R §5 11-14 · B2 |
| :64 §1-1 ④ | (새 줄) | 실기기 Z Fold3 확인 — 통역 음성 입력(11-13) · 정식 vc3 · F1 해소(11-15) | R §2 · §5 · B8 |
| :107 §3 표 dev | Android [확정] · 「올리면 바꿀 수 없음」 | 「Play 내부 테스트 앱 2026-11-13 — 올렸으므로 이제 바꿀 수 없음」 | R §5 11-13 |
| :108 §3 표 prod | Android [미결] | `day.medisolveai`(사용자 2026-11-13 · Play 비공개 테스트 2026-11-14) | R · B1 |
| :110 §3 | 정식 앱 Android id [미결](M-4) | 취소선 → `day.medisolveai` · `DAY`. M-4 닫음 | B1 |
| :111 §3 | 「Android id · 이름 주입 방식 정하지 않았다」 | 취소선 → 3단(`-P` > `identity.local.properties` > `identity.properties` placeholder) · flavor 없음 | A1 · C · B3 |
| :187 §7 | 정식 출시 여부 [미결](M-17) | 취소선 → 비공개 테스트 → 프로덕션 진행. M-17 닫음 | B1 |
| :192 §7-0 | 「정식 앱 · 프로덕션 하지 않는다」 | 취소선 → 「뒤에 늘어난 범위」로 · 푸시는 그대로 안 함 | R §2 |
| :195 §7-0 | Dart 무변경 기본 | 덧붙임: 실제 바꾼 것 = F1 하나(사용자 OK 11-13 · iOS 그대로) | e2e-feedback F1 · B6 |
| :204 §7-0 | 세션 [제안] | 취소선 → 구현됨(§7-2 끝 줄 · 코드 작업이 정함) | A1 · B4 |
| :205 §7-0 | [미결] 목록(M-4 · M-3 · M-11 정식 키 · M-17) | 닫힌 항목은 취소선 · 남은 것 = 백업(M-11) · CI(M-12) · FCM(M-9) | B1 · B2 |
| :205 뒤(새 줄) | — | 「뒤에 늘어난 범위(Delivery #251 승인 뒤 · 사용자 결정)」: 정식 앱 비공개 테스트 → 프로덕션 · 정식 빌드 = prod 진입점 · 허용 prod · dev | R §2 11-13 · 11-15 · B1 |
| :210 §7-1 | 정식 앱 [미결] · flavor [제안](주입 방식 미정) | `day.medisolveai` · flavor 없이 `-P` 3단 | A1 · B3 |
| :210 뒤(새 줄) | — | minSdk 24 · targetSdk · compileSdk 36(M-7의 Android 쪽) | A1 · C(`build.gradle.kts:62-64`) · B5 |
| :215 §7-2 | 개발 앱 Play 앱 서명 | 「· 정식 앱도 같음 — 2026-11-14」 | R §5 |
| :216 §7-2 | 업로드 키 · 서비스 계정 로컬 | 덧붙임: Play 업로드 전용 서비스 계정 · 키 로컬 · 프로젝트 한정 재정의로 한 번 발급 | B2 |
| :217 §7-2 | dev / prod 같은 키? = 정식 앱 때 | 취소선 → [확정] 같은 업로드 키(사용자 2026-11-13). 백업은 [미결] 그대로 | R §2 11-13 · B2 |
| :217 뒤(새 줄) | — | release는 업로드 키로만 서명 · 없으면 빌드가 멈춤(debug 키 길 없음) | A3 · C(`GradleException`) · B3 |
| :219 §7-2 | 세션 [제안] | 취소선 → 구현: Keystore 키 AES-256-GCM · 앱 전용 prefs · 단일 직렬 실행기 · 백업 · 기기 이전 제외 · 복호화 실패 → 로그인 화면 | A1 · B4 |
| :227 뒤 §7-3 표(새 행) | — | 「Google Play 비공개 테스트 → 프로덕션」 = 정식 앱 자리 | R §2 · B1 |
| :230 §7-3 | 정식 앱 배포 방식 [미결](M-3) | 취소선 → [확정] Play 비공개 테스트 → 프로덕션. M-3 닫음 | R §2 11-13 · 11-15 |
| :241 §7-3-1 | 데이터 보안 「확인」 | 덧붙임: 정식 앱은 채웠다 | R §5 11-14 · B9 |
| :242 §7-3-1 | 그 밖 앱 콘텐츠 「확인 안 됨」 | 덧붙임: 정식 앱에서 채웠다 | R §5 11-14 · B9 |
| :247 §7-3-1 | 조직 계정 12명 · 14일 「프로덕션 때 다시 본다」 | 문서 근거는 그대로 확인 안 됨 · 실제로는 조직 계정 프로덕션 제출이 막히지 않았다(11-15) | R §5 11-15 |
| :252 §7-3-2 머리 | 손 단계 안내 | 「1~6은 개발 앱에서 했다(11-13~14) · 정식 앱은 7」 | R §5 |
| :260 뒤 §7-3-2 ① | — | (코드 작업) `play_upload.py` = internal / alpha 두 짝만 · 프로덕션은 스크립트가 막음(의도) · `--dry-run` | A5 · A6 · C(`UPLOAD_TRACKS`) · B7 |
| :260 뒤 §7-3-2 ② | — | 7. 정식 앱 손 단계 「했다」 | R §5 11-14 · B9 |
| :260 뒤 7의 내용 | — | 앱 만들기 · 첫 AAB 손 업로드 · 콘텐츠 선언(데이터 보안 · 사진 / 동영상 권한 「채팅 최근 사진 줄」 신고 통과 · 18+ · 광고 없음 · 앱 접근 = 데모 계정) · 스토어 등록정보 · 테스터 · 서비스 계정 · 프로덕션 제출은 Console 손 | R §5 11-14 · B9 |
| :276 §8-1 | 푸시 안 붙임(로컬 · 내부 테스트) | 범위에 「정식 앱 비공개 테스트 · 프로덕션」 추가 | B · 범위 밖 그대로 |
| :307 §9 | Android id prod [미결] | `day.medisolveai` | B1 |
| :308 §9 | Android prod [미결](M-17 · M-3) | [설정 완료] 비공개 테스트 vc3 → 프로덕션 vc3 심사 중 · dev = 내부 테스트 vc3 | R §5 |
| :309 §9 | Android 서명 prod [미결](M-11) | [확정] 같은 업로드 키 · API는 alpha까지 · 프로덕션 = Console 손 | B2 · B7 |
| :319 §9 | 앱에 든 비밀(암호화 저장소) | 「Android Keystore 키로 암호화한 앱 전용 저장소」 | B4 |
| :324 뒤 §9-1(새 줄) | — | [설정 완료] Android 정식 앱도 같은 규칙으로 빌드(진입점 prod · 허용 prod · dev) · 개발 앱은 dev 하나 | A4 · B1 |
| :360 §12 | 정식 Application ID · 정식 배포 [미결] | 취소선 → 11-13~15 정식 앱 비공개 테스트 → 프로덕션 제출. 백업 · CI는 [미결] | B1 |
| :366 M-1 | 영향: Android 배포 방식 | 취소선(→ Play 프로덕션) | R §2 11-15 |
| :368 M-3 | 정식 앱 배포 방식 남음 | ~~M-3~~ 닫음 | B1 |
| :369 M-4 | 정식 앱 id 남음 | ~~M-4~~ 닫음 `day.medisolveai` | B1 |
| :372 M-7 | 최소 Android 버전 | 취소선(→ minSdk 24 · targetSdk 36) · iOS는 남음 | B5 |
| :374 M-9 | FCM 안 넣음(로컬 · 내부 테스트) | 「· 정식 앱 비공개 테스트 · 프로덕션」 추가 · 미결 그대로 | — |
| :376 M-11 | dev/prod 키 분리 남음 | 취소선(→ 같은 키) · 백업은 남음 | B2 |
| :377 M-12 | 개발 앱 업로드 로컬 | 「Android 업로드(개발 · 정식) 로컬(`play_upload.py`)」 · CI는 남음 | B7 |
| :382 M-17 | 정식 출시 여부 · 시점 남음 | ~~M-17~~ 닫음: 출시한다 · 프로덕션 vc3 심사 제출 11-15 · 통과하면 바로 공개 | R §5 11-15 |

#### spec-003-mobile-app.md

| 파일:줄 | 전 | 후 | 근거 |
|---|---|---|---|
| :8 | last_updated 2026-11-13 | 2026-11-16 | — |
| :66 뒤(새 줄) | — | 개정 ⑯ 노트(①~⑤ · 범위 밖 그대로) | B1~8 |
| :97 뒤(새 행) | — | §1 범위: Android 정식 앱(`DAY` · `day.medisolveai`) · prod 진입점 · 허용 prod · dev · 비공개 테스트 → 프로덕션 · 화면 · 채널 개발 앱과 같음 | B1 |
| :110 | 범위 밖: Android 정식 앱 · 정식 출시 · 정식 배포 · FCM … · M-17 · M-4 · M-3 | 정식 3개는 취소선(→ 개정 ⑯) · FCM · 알림 [수락] · 동영상은 그대로 | B1 · 범위 밖 그대로 |
| :120 뒤(새 줄) | — | §2 Placement: Android 하단 시스템 영역 — 태블릿 채팅 칸 입력줄 · 바닥까지 닿는 목록 끝(판 · 설정 · 폰 차트 시트)을 내비 바 · 태스크바만큼 비움 · iOS 그대로 | e2e F1 · A5 · A6 · C · B6 |
| :557 §3 세션 | Android 저장 위치 [제안] — 확정 아님 | 취소선 → 구현됨: Keystore AES-256-GCM · 앱 전용 저장소 · 단일 직렬 실행기 · 백업 · 기기 이전 제외 · 복호화 실패 → 로그인 화면 | A1 · B4 |
| :567 채널 절 | (개발 앱만) | 「Android 정식 앱 `DAY`도 같은 코드 · 같은 채널 동작 — id · 이름 · 서버만 다름」 · 「실제로 바꾼 Dart = F1 하나」 | B1 · B6 |
| :576 | id · 이름 = 개발만 · 주입 방식은 코드 작업에서 | 개발 · 정식 둘 · 주입 = `-P` 3단 · minSdk 24 · targetSdk 36 | B3 · B5 |
| :577 | Play: 첫 빌드 손 · 그 뒤 API | 업로드 키 개발 · 정식 공유 · API = `app/android/play_upload.py`(internal / alpha만 · 프로덕션 Console 손) | B2 · B7 |
| :924 A-48 | 「말하기(에뮬레이터 호스트 마이크 입력)」 · 실물 「✓ 로컬 에뮬레이터」 | 조건에서 「에뮬레이터 호스트 마이크」를 뺐다. 실물 칸에는 에뮬레이터에서 확인한 범위(권한 · 드로어 · 듣는 중 · 칩 TTS)를 적고, 말하기 → 자막 · 번역 음성은 실기기(Z Fold3 · 11-13)로 적었다 | A1 · R §2 11-13 · B8 |
| :925 A-49 | 실물 「✓ 테스터 기기」 | 덧붙임: 실기기 개발 vc1 Play 설치 11-13 → API vc3 업데이트 · 정식 비공개 vc3 Play 설치 11-15 | R §5 · B8 |

#### 그 밖 4파일

| 파일:줄 | 전 | 후 | 근거 |
|---|---|---|---|
| spec-004 :8 | last_updated 2026-11-13 | 2026-11-16 | — |
| spec-004 :35 뒤(새 줄) | — | 「2026-11-16 — DAY-SPEC-003 개정 ⑯ 맞춤」(Android 줄 · 채팅 동작 · 서버 무변경) | B1 |
| spec-004 :80 | 「Android 는 개발 앱 로컬 실행 · Play 내부 테스트만」 | 「… · 정식 앱 Play 비공개 테스트 → 프로덕션」 · FCM · 동영상 뺌 그대로 | B1 |
| 20-spec.md :9 · :41 | 범위 밖에 「Android 정식 앱 · 출시 · 푸시」 | 「Android 푸시」만 남김(정식 앱 · 프로덕션은 범위 안 · 개정 ⑭ · ⑯) | B1 |
| 40-architecture/README.md :22 | 「dev / prod flavor 제안 · 비공개 배포 후보 · 설정은 아직 안 함」 | 「dev / prod 두 앱 · iOS Unlisted · Android Play 내부 테스트 · 비공개 테스트 → 프로덕션 · 지금 상태는 §1-1」 | 사실 |

### 하지 않은 것

- **값은 0개다.** diff에서 계정 이메일 · 서비스 계정 이름 · 프로젝트 이름 · 정책 이름 · 키 지문 · 비밀번호를 grep했고 0건이었다.
- **화면 문구는 새로 만들지 않았다.** F1 줄은 레이아웃 사실만 적었다.
- **그대로 둔 것:**
  - FCM(M-9) · 동영상 보내기 · 알림 [수락] Android 판 → 범위 밖 · [미결]
  - 업로드 키 백업(M-11) → [미결]
  - CI(M-12) · 빌드 번호 규칙(M-13) → [미결]
  - KOS 세션 14시간 문제 → 손대지 않음(별도 작업)
- **새 [확정]은 사용자 결정만 붙였다.** 세 가지다: 정식 앱 Play 출시 · 같은 업로드 키 · 정식 배포 방식.
  - 구현으로 생긴 사실(세션 저장 · id 주입 · minSdk · `play_upload.py`)은 [확정]으로 올리지 않았다. 「코드 작업이 정함」 / [설정 완료]로 적었다.
- **iOS 줄은 고치지 않았다.** §1-1의 「정식 DAY 0.1.0 (2) 결과 대기」 등이다. 이 일의 범위 밖이고, iOS 재제출 기록은 #941 · 60-release가 갖는다.

---

## B. Delivery #251 마감 sync — review-delivery 대조

### 대상

| 항목 | 값 |
|---|---|
| Delivery | CENTURION_DAY#251 v2 · key `day/android-dev-app-local-run` · risk L3 · OPEN |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` |
| contract | `sha256:d63d70acc0d6c2dc9b435022d237e2b4ec8558cd56bb2ab08b5f8cd7c561ab3e` · plan `sha256:e9664196d73545012edd23174a9ce4cbc0dc6d546c0dc5f0d53f12e67bba9101` |
| baseline | `855bab4f861ef97257621b45b296061c511e1223` |
| 코드 PR | CENTURION_DAY#253 → `dev` · MERGED 2026-11-16T04:56:37Z |
| PR 커밋 | head `0120b427c6485c2015b2aeb540c0fb99ad395465` · squash `4f8316a77dcc33ee8dfd3529accc39c0a1d9733f` · 부모 `ca72fd1d` |
| 바뀐 파일 | 35개 — `app/android/**` · `app/lib` 5 · `app/test` 1 · `.gitignore` 2 · `app/README.md` · `app/.metadata` |

### Target Delta 대조

| # | Target Delta | 결과 | 근거 |
|---|---|---|---|
| 1 | `app/android/` 생성 · 개발 앱 id `day.medisolveai.dev` · `DAY Dev` · 주입 방식은 구현이 정해 PR에 적음 | 지킴 | A1 · `-P` 3단 · aapt / bundletool package · label |
| 2 | `day/session` Kotlin(load · save · clear · clearIf · 직렬 원자) | 지킴 | A1 채널 대조표 · `SessionChannel.kt` · reviewer 1 iOS 대조 |
| 3 | `day/push` 스텁(설정 탭 알림 안내 그대로) | 지킴 | A1 · A1 실물 「알림 꺼짐」 |
| 4 | `day/video` 스텁(새 문구 없음) | 지킴 | A1 · `convert_failed` → 기존 U-6 문구 |
| 5 | 통역 Android(마이크 · 4 플러그인) | 지킴 | A1(권한 · 연결 · TTS) · 실기기 음성 입력(사용자 11-13) |
| 6 | 그 밖 플러그인 권한 · 설정만 | 지킴 | A1 매니페스트 · CAMERA 미선언 · 사진 권한은 Play 신고로 통과 |
| 7 | release AAB · targetSdk 36 · 업로드 키 서명 · 값 저장소 밖 · .gitignore | 지킴 | A3 · C `build.gradle.kts:62-64` · `:92` |
| 8 | 업로드 키 생성(keytool · 600 · 값 출력 금지 · 백업은 사용자) | 지킴 | A3. 백업은 사용자 몫이라 [미결] 그대로 |
| 9 | Play Developer API 업로드 스크립트(내부 테스트 · 둘째 빌드부터 · versionCode 인자) | 지킴 + 넓어짐 | `play_upload.py` `--expect-version-code`(A5) · 정식 → alpha 짝 추가(아래 「범위 밖으로 늘어난 것」) |
| 10 | README Android 절(에뮬레이터 · 호스트 마이크 · AAB · 스크립트) | 지킴 | A1 · A3 · A5 · A6 README 소절(추가만) |

### Acceptance 대조

| A | 조건 | 판정 | 근거 |
|---|---|---|---|
| A1 | 에뮬레이터 DAY Dev dev 로그인 → 시술 현황 · 채팅 목록 | **pass** | 리포트: A1 · `app-1-shots/01~03`. 실물: 에뮬레이터 Android 16 |
| A2 | 재실행 자동 로그인 · 로그아웃 뒤 로그인 화면 · 푸시 없이 오류 없음 | **pass** | 리포트: A1 · shots 05 · 06 · 07. 실물: `day.session` 레코드 0 확인 |
| A3 | iOS `build ios --no-codesign` · `app/ios` 변경 0 · create 산물은 따로 적음 | **pass** | 리포트: A1. 실물: C(`git diff ca72fd1d 4f8316a7 -- app/ios` = 0). PR 본문에 `app/.metadata`를 따로 적음 |
| A4 | Dart 변경 0이 기본 · 바꿨으면 코디 확인 기록 · test · analyze 통과 | **pass**(조건부 갈래) | Dart 5파일은 F1 — 사용자 OK(e2e-feedback F1 · R §2) · iOS 픽셀 동일(A5 · A6) · analyze 0 · test +355(review-code-4) |
| A5 | 통역 — 권한 → 말하기 → 자막 · 번역 음성 · 칩 TTS | **pass** | 에뮬레이터: 권한 · 드로어 · 듣는 중 · 칩 TTS(A1). 말하기 → 자막 · 번역 음성: 사용자 결정 11-13으로 A6 실기기 몫 — 사용자 「확인했어」(2026-11-13 · 통역 음성 입력 포함으로 코디가 봄) · 2026-11-15 정식 vc3 실기기 「다 다운 받아서 봤는데 괜찮아서」(2회차 W-3 문구). DAY-SPEC-003 A-48에 반영 |
| A6 | Play 내부 테스트 → 실제 Android 폰 설치 · dev 로그인 · 둘째 빌드 API 업데이트 | **pass** | 실물: Z Fold3 · vc1 Play 설치 11-13 · API vc2 · vc3 commit ok(A5 · A6) · 사용자 확인 11-13 · 11-15 |
| A7 | 저장소 · 로그 · PR에 키 · 비밀번호 · 서비스 계정 JSON 0 | **pass** | A3 · A5 · A6 비밀 grep 0 · reviewer 1 §7 · C(`git grep` PEM은 서버 테스트의 가짜 값뿐) · `.gitignore` 두 곳 check-ignore |

**판정은 conformant · merged다.** 대상 SPEC 처리는 다음과 같다.
- 계약 자체는 #940으로 이미 main에 있다.
- 구현 사실은 이 PR에서 SPEC-003 개정 ⑯ · SPEC-004 · mobile-deployment ④로 sync했다.
- 그래서 「none」이 아니라 「이 PR」이다.

### Delivery 뒤 사용자 결정으로 늘어난 것

#253에 함께 들어갔다. v2 계약 밖이라 정직하게 적는다.

| 늘어난 것 | v2 계약에서는 | 사용자 결정 | 들어간 곳 |
|---|---|---|---|
| F1 하단 시스템 영역(Dart 5파일 · 테스트 1) | Dart 변경 0이 기본(A4 갈래) | 2026-11-13 「정석 = inset 만큼」 · Dart OK | `099fe786` → #253 · DAY-SPEC-003 §2 Placement |
| 정식 앱 `DAY`(`day.medisolveai` · prod) Play 비공개 테스트 · `play_upload.py` 정식 → alpha 짝 | Non-Goal 「정식 앱(M-4 · M-3)」 | 2026-11-13 「빌드하고 올리자」 · 업로드 키 공유 | `0120b427` → #253 · mobile-deployment ④ |
| 정식 앱 프로덕션 출시 | Non-Goal 「프로덕션 트랙」 | 2026-11-15 「이제 출시 준비도 하면 되나?」 | 코드 변경 없음 — Console 손 단계(스크립트는 프로덕션을 막음) · mobile-deployment §7-3-2 7 |
| 루트 `.gitignore` 비밀 패턴 | code_surface `.gitignore` | (reviewer 참고 · 코디) | #253 |

새 Delivery로 나누지 않은 이유는 두 가지다.
- 코드 변경이 F1 · 스크립트 짝 하나뿐이다.
- 나머지는 Play Console 손 단계다.

사용자가 진행 중에 바로 결정했기 때문이다. 판단이 필요하면 코디가 결정한다. 예를 들어 Issue에 Scope Delta v3를 남길지 여부다. 이번에는 하지 않았다(브리프 범위 밖이고 receipt도 하지 않았다).

### 문서 sync (#936 꼴)

- `30-work.md`
  - Delivery 대시보드에 #251 행을 더했다. 이 PR 머지 뒤 Issue를 닫았을 때의 상태로 적었다: `closed` · `implementation:conformant` · `spec-sync:pending`.
  - Spec Coverage의 DAY-SPEC-003 · DAY-SPEC-004 행에 #251을 더했다. 구현 상태 `in_dev`는 그대로다(다른 Delivery가 열려 있음).
- `log.md`
  - `wp-status` 한 행(#251 마감 sync)을 더했다.
  - spec-sync `arch-change, spec-change` 한 행도 더했다(A).
- `spec-sync` CLI는 돌리지 않았다. #936과 같은 사유다. 원장(CENTURION_DAY)과 문서(mediness)가 다른 레포다(#749).
  - 그래서 Issue의 `spec-sync:pending` 라벨은 닫은 뒤에도 남는다.

### Issue #251 마감 댓글 초안 (게시는 코디)

```markdown
## Delivery 마감 — conformant · merged

- 코드 PR: #253 → `dev` · squash 머지 `4f8316a77dcc33ee8dfd3529accc39c0a1d9733f`(head `0120b427c6485c2015b2aeb540c0fb99ad395465` · 2026-11-16)
- contract v2 `sha256:d63d70acc0d6c2dc9b435022d237e2b4ec8558cd56bb2ab08b5f8cd7c561ab3e` · baseline `855bab4f861ef97257621b45b296061c511e1223`
- 문서 sync: MediSolveAIDev/mediness#<이 PR> (머지 `<SHA>`) — DAY-SPEC-003 개정 ⑯ · DAY-SPEC-004 · mobile-deployment 2026-11-16 ④ · 30-work.md · log.md

### Acceptance
| | 판정 | 근거 |
|---|---|---|
| A1 dev 로그인 → 시술 현황 · 채팅 목록(에뮬레이터) | pass | 구현 워커 실물 |
| A2 자동 로그인 · 로그아웃 뒤 로그인 화면 · 푸시 없이 오류 없음 | pass | 구현 워커 실물 |
| A3 iOS build · `app/ios` 변경 0 | pass | `git diff` 0 · build ios --no-codesign |
| A4 Dart 변경 → 코디 · 사용자 확인 기록 · test · analyze | pass | 하단 시스템 영역 수정(사용자 OK) · iOS 화면 그대로 · test +355 · analyze 0 |
| A5 통역 | pass | 에뮬레이터 권한 · 연결 · TTS · 음성 입력은 사용자 결정대로 실기기 몫 — 사용자 「확인했어」(2026-11-13 · 통역 음성 입력 포함으로 코디가 봄) · 2026-11-15 정식 vc3 실기기 「다 다운 받아서 봤는데 괜찮아서」 |
| A6 Play 내부 테스트 실기기 설치 · API 둘째 빌드 업데이트 | pass | 사용자 실기기 확인 · API vc2 · vc3 |
| A7 저장소 · 로그 · PR 비밀 0 | pass | 값 grep 0 · .gitignore |

### 승인 뒤 사용자 결정으로 늘어난 것(같은 PR)
- 하단 시스템 영역(내비 바 · 태스크바)이 입력칸 · 목록 끝을 가리던 문제 수정 — Dart 변경 · 사용자 OK · iOS 그대로
- 정식 앱 `DAY`(`day.medisolveai` · prod) Play 비공개 테스트 · 업로드 스크립트 정식 → alpha 짝
- 정식 앱 프로덕션 제출(2026-11-15 · Console 손 단계 · 스크립트는 프로덕션을 막음)

### 남은 것(이 Delivery 밖)
- FCM · 알림 [수락] · 동영상 보내기 Android 판 · 업로드 키 백업 위치 · CI 업로드 · 빌드 번호 규칙
- `spec-sync:pending` 라벨은 원장 · 문서 레포가 달라 CLI 가 돌지 않아 남는다(#749 · 손 sync)
```

---

## C. lint

`python3 scripts/lint-pipeline.py --strict`를 레포 루트에서 돌렸다. 결과는 **exit 0 · 0 error · 263 warning**이다.
- `products/day`에 걸린 줄은 0개다. ERROR 0 · WARN 0이다.
- 263개는 다른 제품의 기존 경고다(selly 등).

---

## PR 제목 · 본문 초안 (mediness · 코디가 커밋 · PR)

**제목**: `docs(day): Android 마감 — SPEC-003 개정 ⑯ · SPEC-004 · mobile-deployment ④ · Delivery #251 마감 sync`

```markdown
## 한눈에 보기

- **해결하려는 문제:** #940 머지 뒤 Android 앱이 실제로 많이 진행됐다. 정식 앱 Play 비공개 테스트 → 프로덕션 심사, 업로드 키 공유, 세션 저장 구현, 하단 시스템 영역 수정이다. 그런데 스펙은 여전히 「정식 앱 [미결] · 범위 밖」이었다. Delivery #251도 코드가 머지됐는데 마감 sync가 없었다.
- **이번 PR에서 바뀌는 것:** 스펙을 사실에 맞춘다. 닫힌 [미결]은 M-3 · M-4 · M-17, M-7의 Android 쪽, M-11의 키 분리다. 구현 사실을 [제안] 자리에 적고, Delivery #251을 대시보드 · Spec Coverage · log에 반영한다.
- **이번 PR에서 바뀌지 않는 것:** 서버 · 업무 계약 · 화면 문구. FCM · 알림 [수락] · 동영상 보내기 Android 판 · 업로드 키 백업 · CI는 [미결] / 범위 밖 그대로다. iOS 줄도 그대로다.
- **리뷰 후 다음 단계:** 머지 → `dashboard-sync --view delivery` 확인 → Issue #251 마감 댓글 → 닫기.

## 변경 내용

- `mobile-deployment.md` 2026-11-16 ④
  - 정식 Android 앱 `day.medisolveai` · `DAY` · prod. Play 비공개 테스트 vc1 → vc3, 프로덕션 vc3 심사 중(2026-11-15 제출). iOS 정식과 같은 「정식 빌드 = prod · 데모 계정 → dev」다.
  - 업로드 키는 개발 · 정식 공유다. 백업 위치는 [미결] 그대로다.
  - Play 업로드 전용 서비스 계정 · 키는 로컬이다(값 없음).
  - id · 이름 · 서명 주입은 `-P` 3단이다. release는 업로드 키가 없으면 빌드가 멈춘다.
  - 세션 저장은 Keystore AES-256-GCM이다.
  - minSdk 24 · targetSdk 36.
  - `play_upload.py`는 internal / alpha만 받는다. 프로덕션은 Console 손 단계다.
  - Play 콘텐츠 선언은 「했다」로 적었다.
- `DAY-SPEC-003` 개정 ⑯
  - §1에 Android 정식 앱을 범위 안으로 넣었다.
  - §2 Placement에 Android 하단 시스템 영역 한 줄을 넣었다(iOS 불변).
  - §3 세션 저장 · id 주입 · 업로드 스크립트를 고쳤다.
  - A-48: 음성 입력은 실기기에서 확인했다. A-49에 실물 기록을 넣었다.
- `DAY-SPEC-004`: §1 「뺌」의 Android 줄을 맞췄다.
- `20-spec.md` · `40-architecture/README.md`: 범위 밖 줄과 설명을 고쳤다.
- `30-work.md`
  - Delivery 대시보드에 #251 행을 넣었다(머지 뒤 닫힌 상태로).
  - Spec Coverage SPEC-003 · 004에 #251을 넣었다.
- `log.md`: 두 행.

## 확인 방법과 결과

- **확인한 방법:**
  - 브리프 grep(`android|play|aab|keystore|업로드 키|day.medisolveai|미결`)으로 222줄 전수를 보고 사실과 다른 줄만 고쳤다.
  - 코드 `4f8316a7`을 직접 대조했다: `app/ios` diff 0 · `UPLOAD_TRACKS` · minSdk / targetSdk · 서명 `GradleException`.
  - diff에서 값을 grep했다.
  - `python3 scripts/lint-pipeline.py --strict`를 돌렸다.
- **결과:**
  - lint exit 0 · products/day ERROR 0 · WARN 0.
  - 값(계정 · 키 · 서비스 계정 · 개발자 id) 0.
- **아직 확인하지 못한 것 / 남은 위험:**
  - Play 프로덕션 심사 결과를 기다리는 중이다. 결과가 나오면 §1-1을 한 줄 고쳐야 한다.
  - `spec-sync` CLI는 레포가 달라 돌지 않는다(#749). 손 sync라서 `spec-sync:pending` 라벨이 남는다.

<details>
<summary>문서·운영 체크리스트</summary>

- [x] 신규 delivery의 범위·계획·검증·복구 방법이 Delivery Issue에 있음 — #251 v2 (승인 뒤 늘어난 범위는 Issue 마감 댓글에 적음)
- [x] 사용자 동작·UX·API 계약 변화를 target SPEC에 반영함 — DAY-SPEC-003 개정 ⑯ · DAY-SPEC-004
- [ ] 범위·비용·정책·고객 약속 변화를 `10-decision.md`에 반영함 / 해당 없음 — ESC 없음
- [x] 새 `30-work/work-*.md`를 만들지 않음
- [ ] Legacy WP 변경 / 해당 없음
- [x] `30-work.md` mixed dashboard를 갱신함
- [x] archive 변경 없음
- [ ] 배포·migration·외부 write / 해당 없음(문서만)

</details>

<details>
<summary>Delivery 추적 정보</summary>

- GitHub Delivery Issue: MediSolveAIDev/CENTURION_DAY#251
- Target SPEC: DAY-SPEC-003, DAY-SPEC-004
- SPEC baseline revision: 855bab4f861ef97257621b45b296061c511e1223
- Contract version / digest: v2 / sha256:d63d70acc0d6c2dc9b435022d237e2b4ec8558cd56bb2ab08b5f8cd7c561ab3e
- Code PR head SHA: 0120b427c6485c2015b2aeb540c0fb99ad395465 (squash 4f8316a77dcc33ee8dfd3529accc39c0a1d9733f)
- `review-delivery` evidence: conformant · merged (손 대조 — 이 PR 리포트)
- SPEC sync: 이 PR

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 코디가 정할 것

1. **Scope Delta v3를 남길지.** 승인 뒤 정식 앱 · 프로덕션 · F1이 늘어났다. Issue 마감 댓글에 적는 것으로 갈음할지 정해야 한다. 이번에는 하지 않았다.
2. **프로덕션 심사 결과.** 통과하거나 거절되면 mobile-deployment §1-1 · §9 「심사 중」 두 곳을 고쳐야 한다.

---

## 2회차 — review-doc-close WARN 3 반영 (2026-11-16)

같은 워크트리 · 미커밋에 이어서 고쳤다. 공통 문구 Q = 「사용자 「확인했어」(2026-11-13 · 통역 음성 입력 포함으로 코디가 봄) · 2026-11-15 정식 vc3 실기기 「다 다운 받아서 봤는데 괜찮아서」」.

### 변경 줄

| 지적 | 파일:줄 | 전 | 후 |
|---|---|---|---|
| W-1 | `mobile-deployment.md:43` §1 | 「이 줄은 iOS 다 — Android 정식은 Play 프로덕션(공개)」(11-11 결정을 iOS 한정으로 좁혀 읽음) | 원래 11-11 줄은 그대로 두고 「→ 2026-11-15 Android 정식은 바뀜: Play 프로덕션(공개 — 대한민국 · 검색 가능) · 사유 = 코디가 「프로덕션 = 누구나 검색 · 설치(공개)」 설명 → 사용자 「이제 출시 준비도 하면 되나?」 → 제출 · iOS 는 Unlisted 그대로 · 앱 로그인으로 막는 것은 같다」를 덧붙임 |
| W-1 | `mobile-deployment.md:24` 개정 노트 ④ ① | 「프로덕션 트랙 제출 · 심사 중(… · 대한민국)」 | 「· 공개 — 2026-11-11 「최종 배포는 비공개」를 Android 에서 바꿈 · iOS 는 그대로 · §1」 |
| W-1 | `log.md:18` | (결정 근거 없음) | 「Android 정식 배포 = Play 프로덕션(공개 — 2026-11-15 사용자 결정 · 11-11 「최종 배포는 비공개」를 Android 에서 바꿈 · iOS 는 Unlisted 그대로)」 |
| W-2 | `mobile-deployment.md` §7-3-2 머리말 | 「1 ~ 6 은 개발 앱에서 했다(사용자 2026-11-13 ~ 14)」 | 「1 · 3 ~ 6 은 사용자(2026-11-13 ~ 14) · 2 는 코드 워커(2026-11-13)」 |
| W-2 | `mobile-deployment.md` §7-3-2 · 2 | 「업로드 키를 만들어 … 백업 [미결]」 | 덧붙임: 「이 단계는 코드 워커가 keytool 로 만들었다(2026-11-13 · 백업은 사용자 [미결])」 |
| W-3 | `spec-003:68` 개정 ⑯ ⑤ | 「음성 입력 = 실기기 확인(에뮬레이터는 맥 호스트 마이크를 받지 못함)」 | 「실기기 몫(이번 환경에서는 macOS 가 에뮬레이터에 맥 마이크를 주지 않음) · 확인 근거 = Q」 |
| W-3 | `spec-003:928` A-48 실물 칸 | 「= 실기기(… 사용자 Galaxy Z Fold3 확인 2026-11-13)」 | 「= 실기기 몫(이번 환경 … · Galaxy Z Fold3 — Q)」 |
| W-3 | `mobile-deployment.md:70` §1-1 | 「통역 음성 입력(2026-11-13)」 | 「통역 음성 입력(해석 — Q)」 |
| W-3 | `log.md:17` · `:18` | 「A6 실기기에서 확인」 · 「A-48 음성 입력 = 실기기」 | 「A6 실기기 몫 — Q」 · 「실기기 몫(Q)」 |
| W-3 | 이 리포트 B Acceptance A5 · 댓글 초안 A5 행 | 「실기기에서 확인(사용자 「확인했어」 11-13)」 | 「실기기 몫 — Q」 |

### 참고 R-1 ~ R-5 처분

| | 처분 |
|---|---|
| R-1 log PR 칸 | 그대로 둠 — 코디가 mediness PR 번호를 받으면 같은 커밋에서 `#NNN` 으로 바꾼다(`log.md:17` · `:18` 둘 다) |
| R-2 A4 「코디 확인 기록을 PR 에」 | 그대로 둠 — Issue 마감 댓글 초안 A4 행 「하단 시스템 영역 수정(사용자 OK)」이 기록을 메운다. 게시는 코디 |
| R-3 대시보드 `closed` | 그대로 둠 — #936 꼴(머지 뒤 닫은 상태로 적음). 순서 = 이 PR 머지 → 댓글 → Issue 닫기 |
| R-4 「맥 호스트 마이크」 일반화 | **반영** — 「이번 환경에서는 macOS 가 에뮬레이터에 맥 마이크를 주지 않음」으로 좁힘(spec-003 ⑤ · A-48) |
| R-5 `10-decision.md` 감인지 | 판단: **ESC 감은 아니라고 본다** — 결정권자(사용자)가 직접 정했고 승인 대기가 없다(ESC board = 결정권자 승인 · 판단이 필요한 미완료 항목). 다만 11-11 「비공개 · 병원 직원에게만」 고객 약속을 Android 에서 바꾸는 결정이라 근거는 `log.md` 에 남겼다(W-1 행). 심사 통과(= 대한민국 누구나 검색 · 설치) 전에 사용자에게 한 번 더 확인받을지 · ESC 로 올릴지는 코디가 정한다. 넣지 않았다 |

### lint

`python3 scripts/lint-pipeline.py --strict` → 아래 값.
- exit 0 · `0 error, 263 warning` · `products/day` 걸린 줄 0(ERROR 0 · WARN 0). 263 은 다른 제품의 기존 경고.
- 변경 파일은 1회차와 같은 7개(mobile-deployment +54/−41 · spec-003 +12/−8 · log +3/−1 · 나머지 그대로). 커밋 · push · PR 없음.
