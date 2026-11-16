# [mobile] Android 개발 앱 1판 — app/android · day/session 구현 · push/video 스텁 · 통역 · 로컬 에뮬레이터 (AND-1~4)

너는 **day `mobile` 워커**다. 맥락이 하나도 없다고 가정하라. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 루트 `AGENTS.md` · `app/README.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ 사용자가 다른 워크트리(`CENTURION_DAY/app-review-re1`)에서 예약현황 탭 숨김(`app/lib/ui/shell.dart` · `copy.dart` · `app/README.md` 등)을 하고 있다 — 그 파일의 Dart 를 이 작업에서 고치지 마라. `app/README.md` 는 **Android 절 추가만**(기존 줄 수정 금지 — 나중에 rebase 충돌 최소화).

## 1. SSOT — 먼저 읽을 것

- Delivery Issue: `gh issue view 251 -R MediSolveAIDev/CENTURION_DAY` (v2 · plan-approved · L3) — Target Delta · A 조건 · phases. **이번 판은 AND-1~AND-4 만**.
- 스펙(머지됨 · mediness main `855bab4f` — 읽기: `git -C /Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec show origin/main:<path>`):
  - `products/day/40-architecture/mobile-deployment.md` §7-0(이번 착수 범위 · 채널 3개 표) · §7-2(세션 저장 [제안] Android Keystore 로 보호되는 암호화 저장소) · §3(id)
  - `products/day/20-spec/spec-003-mobile-app.md` §3 「Android 개발 앱 — 네이티브 채널」 · U-15 통역 · **A-48**(완료 조건)
- 범위 원천(사용자 결정): `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/_archive/day/fix-web/android-app-handoff.md` §3~§5 · `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/_RESUME.md` §2

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

DAY 직원 앱(Flutter `app/` · fvm 3.44.8)은 iOS 로만 지어 왔다 — `app/android/` 가 없다. 이번 판은 **개발 앱(`day.medisolveai.dev` · 이름 `DAY Dev`)을 로컬 Android 에뮬레이터에서 띄워 dev 서버에 로그인하고, 시술 현황 · 채팅 목록 · 통역까지 동작**하게 만든다. Play 업로드(업로드 키 · release AAB · API 스크립트)는 **다음 판**(AND-5~7) — 이번엔 하지 마라.

## 3. 계약 — 네이티브 채널 (Dart 쪽 그대로 · Kotlin 이 맞춘다)

착수 전에 `grep -rn "MethodChannel(" app/lib` 로 채널을 **다시 세라**(3개 예상). 각 채널의 메서드 · 인자 · 반환 · 오류는 `app/ios/Runner/AppDelegate.swift` 가 정본이다 — 줄 단위로 대조해 같은 동작을 Kotlin 으로.

| 채널 | Dart | Android |
|---|---|---|
| `day/session` | `app/lib/data/session_store.dart:79` | **구현** — load · save · clear · **clearIf**(token · api_base_url 이 같을 때만 지움 · **직렬 큐 하나로 원자적** — `AppDelegate.swift` `clearIfSame` 과 같게). 저장 = Android Keystore 로 보호되는 암호화 저장소(스펙 §7-2 [제안]을 따른다 · 고른 방식과 이유를 리포트에) |
| `day/push` | `app/lib/data/push_bridge.dart:35` | **스텁** — ready · requestPermission(false) · register(토큰 없음) · installId(설치마다 고정 값) · appId(applicationId) · appName(`DAY Dev`). 역방향 onToken · onTap · onForeground 는 부르지 않는다 |
| `day/video` | `app/lib/chat/video_pick.dart:22` | **스텁** — audioSave · audioFollowSilent · audioRestore · probe · convert. Dart 가 실패를 삼키는지 확인하고, 스텁이 무엇을 돌려줄지 리포트에 |

**Dart 변경은 기본적으로 0.** Android 에서 막을 것은 Kotlin 으로 막는다. Dart 를 고쳐야만 되는 곳이 나오면 **고치기 전에** 코디에게 `[질문]` 으로 묻는다.

## 4. 먼저 읽을 핵심 파일

- `app/ios/Runner/AppDelegate.swift`(채널 3개 전부) · 위 Dart 3파일 · `app/lib/interpret/audio_io.dart`(통역 오디오 — `record` · `audio_session` · `flutter_pcm_sound` · `flutter_tts`) · `app/pubspec.yaml`(권한이 필요한 플러그인: record · image_picker · photo_manager · flutter_tts · url_launcher · 인터넷)
- `app/README.md` 「빌드 설정(`--dart-define`)」 · 「개발 / 정식 빌드」 — iOS 는 id · 이름을 소스 기본값이 아니라 빌드 설정으로 넣는다. Android 에서 id · 이름을 넣는 방식은 스펙이 **정하지 않았다** — iOS 방식과 맞춰 고르고, 고른 방식 · 이유를 리포트에(스펙 반영은 코디가 나중에).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/android/**`(새로 만듦) · `app/.metadata`(flutter create 산물) · `app/.gitignore`(Android 빌드 산물 · 로컬 설정)
- `app/README.md` — Android 실행법 절 **추가만**
- `app/test/` — Android 와 무관한 Dart 테스트는 그대로. 채널 계약 테스트가 필요하면 새 파일만
- `app/ios/**` · `app/lib/**` **수정 금지**(위 Dart 예외는 코디 확인 뒤)

## 6. 구현 단계

1. **AND-1** `fvm flutter create --platforms android --org <id 에 맞게> .`(app/ 에서) 또는 동등 — 생성물을 확인하고 불필요한 변경(ios/ · lib/ · test/ 덮어쓰기)이 없게. applicationId `day.medisolveai.dev` · 앱 이름 `DAY Dev` · **targetSdk 36**(Play 요구 — 다음 판에서 필요) · minSdk 는 플러그인 요구에 맞춰 정하고 리포트에(M-7). 앱 아이콘은 `app/assets/brand/app-icon.svg`(iOS 와 같은 아이콘)를 쓸 수 있으면 쓴다.
2. **AND-2** `day/session` Kotlin 구현 · `day/push` · `day/video` 스텁(위 §3).
3. **AND-3** 통역 Android — 매니페스트 권한(인터넷 · 마이크 `RECORD_AUDIO` 등 플러그인이 요구하는 것 · 사진 · 동영상 접근) · 플러그인 Android 설정. 권한 문구는 지어 넣지 마라(Android 는 매니페스트에 사용자 문구가 없다 — 있으면 iOS Info.plist 문구를 그대로).
4. **AND-4** 로컬 에뮬레이터 실물 확인 — 아래 §8.
5. `app/README.md` 에 「Android(개발 앱 · 로컬 에뮬레이터)」 절: 에뮬레이터 실행(`~/Library/Android/sdk/emulator/emulator` 절대경로 · PATH 에 없음) · 실행 명령(dev 서버 `--dart-define` 값 — README 「빌드 설정」 정의를 따름) · 로컬 day-local 에 붙일 땐 `10.0.2.2` + cleartext 는 **저장소에 넣지 않고 개발자 로컬만**(README 원칙 · iOS ATS 와 같음) · 에뮬레이터 호스트 마이크 켜기.

## 7. 범위 제약 — 하지 말 것

- Play 업로드 · 업로드 키 · release 서명 · AAB · API 스크립트(다음 판).
- FCM · `google-services.json` · 알림 [수락] · 동영상 실제 구현.
- iOS · Dart 변경(코디 확인 없이) · 서버 변경 · 커밋 · push · PR.
- **사용자 에뮬레이터 · 프로세스를 끄지 마라.** 이미 떠 있는 에뮬레이터가 있으면 그대로 쓰거나 새로 띄운다(AVD `Medium_Phone_API_36.1` · `mediness_api36`). 끝나고 네가 띄운 것만 정리.
- 로그인 계정 · 토큰 · 비밀번호를 리포트 · 로그에 쓰지 마라. 계정은 dev 데모 테넌트 계정. iOS 시뮬레이터 때 쓴 로컬 로그인 자료가 `~/.config/day/apple/simulator-login.local.json`(600 · 임시 토큰 · 만료 있음 — 값 출력 금지)에 있다. 이걸로 안 되거나 만료됐으면 우회 권한을 만들지 말고 `[질문]` 으로 코디에게 — 사용자가 직접 로그인해 줄 수 있다.

## 8. 검증

```
cd app && flutter analyze · flutter test · flutter build ios --no-codesign — 각 1회(통합은 마지막). 사용자 포트·프로세스·기기를 건드리지 않는다. 서명·TestFlight 는 사용자 몫 — 실행 못 한 검증은 사유와 함께 pending
```

추가(이번 판의 완료 조건 — 스펙 A-48 · Issue A1~A5):
- `fvm flutter build apk --debug`(또는 run) 성공.
- 에뮬레이터에서 **dev 서버 실제 로그인 → 시술 현황 · 채팅 목록이 뜬다**(A1) · 앱을 다시 켜면 자동 로그인 · 로그아웃 뒤 다시 켜면 로그인 화면(A2) · 푸시 없이 오류 화면 없음(설정 탭 「알림 꺼짐」 안내는 정상).
- **통역**(A5): 룸 상세 [통역하기] → 드로어 → 마이크 권한 요청 → 말하기(에뮬레이터 확장 제어 Microphone 「Virtual microphone uses host audio input」 켜기) → 자막 원문 · 번역 → 번역 음성 소리 · 빠른 말하기 칩 TTS(칩 언어 `en` · `ja` · `zh` · `zh-Hant` · `th` 중 하나 이상 소리 · 음성 없는 언어는 U-15 토스트 = 정상). dev 서버 통역(D-3)이 꺼져 있으면 앱 문제로 판정하지 말고 보고.
- iOS: `ios/` 변경 0(`git status`) · `fvm flutter build ios --no-codesign` 통과(A3).
- `app/lib` 변경 0(A4) · 저장소에 키 · 토큰 · 비밀 0(`git diff` grep).
- 각 확인의 **스크린샷**을 `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/app-1-shots/` 에(로그인 화면 · 시술 현황 · 채팅 목록 · 통역 드로어 · 설정 탭). 사람 이름 · 전화번호가 보이면 데모 데이터인지 확인하고 리포트에 적는다.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/app-1-report.md` — 변경 파일 · 채널 대조표(iOS 줄 ↔ Kotlin 줄) · 세션 저장 방식 · id 주입 방식 · minSdk · A1~A5 PASS/FAIL 표 · 「조용히 통과하는 자리」(예: clearIf 원자성 · 스텁이 없어도 화면이 같은 곳) · 정할 것.

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --from term_7110412d-9a63-452f-8dad-75aa43ad8f6e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
