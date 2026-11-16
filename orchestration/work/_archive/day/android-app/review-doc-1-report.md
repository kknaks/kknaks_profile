# 리뷰 리포트 — android-app / doc (2026-11-12)

검수 대상: mediness 워크트리 `android-app-spec` 미커밋 변경 5파일(`products/day/` — mobile-deployment · spec-003 · spec-004 · 20-spec.md · log.md) + Delivery #251 v1(request · Issue 본문).
기준: 브리프 §1 「사용자 결정」 표 · 인수인계 `fix-web/android-app-handoff.md` §2~§6 · 코드 CENTURION_DAY `android-app` dev `0106654e`(읽기만).
리포 파일 수정 0 — 산출물은 이 리포트 하나.

## 판정: WARN (FAIL 0 · WARN 5 · 참고 6)

결정 표와 어긋난 곳이 없다. [미결]로 남아야 할 것(정식 앱 id · 배포 방식 · keystore · FCM · 세션 저장 위치 · 빌드 주입 방식)이 [확정]으로 올라간 곳도 없다. M-4 · M-17 · M-9 는 정한 만큼만 닫혔다. 코드 사실(채널 3개 · 메서드 목록 · 통역 오디오 정정)도 맞다. lint products/day ERROR 0. WARN 은 문장 하나가 실제보다 많이 말하는 곳과, 직원이 실물에서 보게 될 화면이 스펙에 안 적힌 곳이다.

## 축별 결과

| # | 축 | 결과 |
|---|---|---|
| 1 | 결정 표 일치 | **PASS** — 9행 모두 반영. 표 아래 참조 |
| 2 | 닫힘/남음 분리 | **PASS** — §1 :37 · :46 / §3 :103 · :106-107 / §7 :183 · §7-0 :185-198 / §9 :265-266 / §12 :317 / §13 M-4 :326 · M-9 :331 · M-17 :339 가 모두 같은 말을 한다 |
| 3 | 전수조사 누락 | **PASS(참고 2)** — planner 표 밖에 낡은 줄 없음. 표 밖 「iOS 전용」 표현은 참고에 적음 |
| 4 | 코드 사실 | **PASS** — 아래 「코드 대조」 |
| 5 | A-48 인수 조건 | **WARN** — 범위 안. 다만 한 항목은 에뮬레이터에서 어떻게 확인하는지가 흐리다(W-3) |
| 6 | Delivery | **PASS(WARN 1)** — Target Delta · Non-Goals · L2 · 메모가 스펙과 맞음. 화면 문구 · 키 · 계정 · 서버 값 0. baseline 처리는 사용자가 정할 일(W-5) |
| 7 | lint | **PASS** — `python3 scripts/lint-pipeline.py --strict` exit 0 · `0 error, 263 warning` · products/day 줄 0(WARN 은 전부 다른 제품의 기존 경고라 무관) |

### 결정 표 ↔ 스펙 대조

| 결정 표 행 | 스펙 위치 | 판정 |
|---|---|---|
| 범위 = 로컬 에뮬레이터 · dev 로그인 → 화면 확인 | mobile-deployment :37 · :187 · spec-003 :95 · 20-spec.md :41 | 같음 |
| 개발 앱 id `day.medisolveai.dev` · `DAY Dev` | mobile-deployment :103 · :265 · spec-003 :575 | 같음([확정] · Google 쪽 등록 없음) |
| 정식 앱 id [미결] | mobile-deployment :46 · :104 · :326 | 같음 |
| `day/session` 구현 | mobile-deployment :193 · spec-003 :555 · :569 | 같음 — 저장 위치는 §7-2 **[제안]** 그대로(:197 · spec-003 :555) |
| `day/push` 스텁 | mobile-deployment :194 · spec-003 :570 | 같음 |
| `day/video` 스텁 | mobile-deployment :195 · spec-003 :571 | 같음 + 통역 정정(코드 근거 있음 — 축 4) |
| 알림 [수락] 안 함 | mobile-deployment :194 · :234 · spec-003 :108 | 같음 |
| iOS 무변경 | mobile-deployment :20 · :188 · Delivery Non-Goal | 같음 |
| Play · keystore · 배포 · FCM [미결] | mobile-deployment :198 · :234 · M-3 · M-9 · M-11 | 같음 |
| (브리프 §3) 빌드 주입 방식 미정 | mobile-deployment :107 · :203 · spec-003 :575 | 같음 |

### 코드 대조 (CENTURION_DAY `android-app` `0106654e`)

- 채널 = 3개뿐: `grep "MethodChannel(" app/lib` → `session_store.dart:79` · `push_bridge.dart:35` · `video_pick.dart:22`. AppDelegate 의 `FlutterMethodChannel` 도 3개(`AppDelegate.swift:46` · `:50` · `:351`).
- 메서드 목록 일치: session `load` · `save` · `clear` · `clearIf`(`:159-170`) / push `ready` · `requestPermission` · `register` · `installId` · `appId` · `appName`(`:59-88`) / video `audioSave` · `audioFollowSilent` · `audioRestore` · `probe` · `convert`(`:364-397`). Delivery Target Delta 의 video 스텁 메서드 5개와 같다.
- 「`day/video` 오디오 = 채팅 동영상 재생 화면」 정정 **맞음**: `chat_video_screen.dart:45,50,55,90` 이 `VideoChannel` 의 audio* 를 부른다. 통역은 `interpret/audio_io.dart:7` 에서 `audio_session` 플러그인을 쓰고 `day/video` 를 거치지 않는다.
- 스텁이어도 Dart 는 터지지 않는다: `video_pick.dart:26-46` probe · convert 는 예외를 잡아 null 로 바꾸고 → `prepareVideo` 가 `videoFailed`(「동영상을 보내지 못했어요」 `:18` · `:76`)를 낸다. audio* 도 `:50-54` 에서 예외를 삼킨다. push 는 `push_coordinator.dart:70-75` · `:83-89` · `:99-103` · `:110-112` 에서 ready · requestPermission · register 예외를 잡는다. **스텁이 없어도(MissingPluginException) 화면은 같다.** 그래서 스텁 메서드가 무엇을 돌려줄지 스펙이 정하지 않은 것은 문제가 아니다.
- `day/session` 은 예외를 잡지 않는다(`session_store.dart:82-101`) → Android 에서 실제로 구현해야 한다는 판단 맞음(인수인계 §3 「없으면 로그인 직후 터진다」).

## FAIL

없음.

## WARN

### W-1. spec-003 :570 — 「통역은 푸시와 관계없이 쓴다」가 확인 안 된 사실을 단정한다
- 위치: `products/day/20-spec/spec-003-mobile-app.md:570`(`day/push` 행 결과 칸) 「앱 안 기능(판 · SSE · 대리 수락 · 채팅 · **통역**)은 푸시와 관계없이 쓴다」.
- 근거: 같은 절 :573 은 「Android 통역 동작 확인은 이번 완료 조건(A-48) 밖」이라 하고, planner 리포트 미결 1 도 「통역이 Android 에서 실제로 되는지는 확인하지 않았다」고 적었다. 통역은 `record` · `audio_session` · `flutter_pcm_sound` · `flutter_tts` 의 Android 동작에 기대므로 푸시와 별개로 Android 에서 될지 아직 모른다. 결정 표의 `day/video` 행도 사용자는 「통역 오디오 전환이 빠진다」고 알고 있었다.
- 고칠 방향: 이 문장의 뜻은 「푸시와 관계없다」이지 「Android 에서 된다」가 아니다. 괄호에서 「통역」을 빼거나 「(통역은 Android 확인 전 — 아래)」를 붙인다.

### W-2. mobile-deployment :188 — 「Dart 동작 무변경」을 [확정]으로 적었는데, 원천은 「기본」이다
- 위치: `products/day/40-architecture/mobile-deployment.md:188` 「**[확정]** … **Dart 쪽 동작은 바꾸지 않고**」 · 같은 문장이 spec-003 :64 · :565 에도 있다.
- 근거: 인수인계 §5 「Dart 쪽 동작은 바꾸지 않는 게 **기본** — Android 에서 막을 건 Kotlin 스텁으로. Dart 를 고쳐야 하면 **코디에게 묻는다**」. 사용자 결정 표에는 이 행이 없다(브리프 §3 계약 문장). 이 이번 작업 규칙을 아키텍처 문서에 영구 [확정]으로 올리면, 나중에 FCM · video 구현 때 Dart 를 바꿔야 할 경우 스펙과 부딪친다.
- 고칠 방향: 「이번 착수(§7-0)는 Dart 를 바꾸지 않는다 — 바꿔야 하면 코디 · 사용자 확인」처럼 이번 범위에 묶는다. 고치지 않아도 이번 Delivery 에는 영향이 없다(Non-Goal 과 같은 말).

### W-3. spec-003 :920 A-48 — 「로그아웃 뒤 세션 묶음 없음」은 에뮬레이터에서 무엇으로 확인하나
- 위치: `spec-003-mobile-app.md:920` · Delivery A2.
- 판단(축 5): 넓힌 세 항목은 **모두 결정 범위 안**이다. 「재실행 자동 로그인 · 로그아웃 뒤 세션 없음」은 결정 「`day/session` 구현 — iOS 와 같은 동작」을 확인하는 최소 조건이고, 「푸시 없이 오류 화면 없음」은 결정 「`day/push` 스텁」의 결과다. 새 기능을 끌어들인 것은 아니다.
- 확인 가능성: 자동 로그인 · 오류 화면 없음은 에뮬레이터에서 눈으로 바로 본다. 「세션 묶음 없음」은 저장소가 암호화돼 있어(§7-2 [제안]) 직접 볼 수 없다 — 그래서 「로그아웃 → 앱 종료 · 재실행 → 로그인 화면」처럼 **보이는 결과**로 적어야 누가 확인해도 같은 답이 나온다.
- 남는 빈칸: `clearIf`(401 · `session_expired` 때 같은 세션일 때만 지움 · 원자적)는 A-48 이 건드리지 않는다. 에뮬레이터에서 401 을 만들기 어려우니 PR 리뷰 때 iOS `SessionKeychain.clearIfSame` 과 코드로 대조하는 정도로 두면 된다 — 「조용히 통과하는 자리」 S-1 참조.
- 고칠 방향: A-48 「로그아웃 뒤 세션 묶음 없음」 → 「로그아웃 뒤 다시 켜면 로그인 화면」. Delivery v2 A2 도 같게.

### W-4. Android 개발 앱 설정 탭에 「알림 꺼짐 · 설정에서 켜기」(빨강)가 늘 보이는데, 스펙에 그 말이 없다
- 근거(코드): push 스텁 `requestPermission` = false → `push_coordinator.dart:88-89` `osDenied = true` → `app.dart:263` → `shell.dart:229` 설정 탭 → DAY-SPEC-005 :99 · :134 「알림 꺼짐 · 설정에서 켜기」(빨강). 앱이 앞으로 올 때마다 다시 물어도(`:96-108`) 늘 false 라, **OS 설정에서 알림을 켜도 문구가 사라지지 않는다.**
- 스펙: spec-003 :570 은 「U-14 「알림 권한」 거부와 같은 모양」이라고만 적었다. 거부와 달리 **켤 방법이 없다**는 점이 빠졌다. DAY-SPEC-005(알림) :68 「Android · FCM — 미결 그대로」는 손대지 않았다(planner 판단 「사실 변화 없음」 — 사실은 맞다).
- 「오류 화면 없음」(A-48)과 충돌하지는 않는다(오류 화면이 아니라 설정 탭의 안내 칸이다). 새 문구를 지을 필요도 없다 — 이미 있는 문구다.
- 고칠 방향: spec-003 :570 결과 칸에 「설정 탭 「알림」 칸은 늘 OS 알림 꺼짐 안내(DAY-SPEC-005) — Android 에서는 켜도 사라지지 않는다」 한 줄. spec-005 는 그대로 두어도 된다.

### W-5. Delivery v1 — baseline 처리와 target_specs
- 근거: `rules/delivery-workflow.md:29` 「이미 Stable SPEC 이 있는 기능 고도화는 **현재 계약을 baseline 으로 고정하고 목표 변화는 Target Delta 에 둔다**」. 그러니 v1(`spec-baseline:ready` · `321a434b` · 개정 ⑭ 없음 · 바뀌는 내용은 Target Delta)은 **규칙상 유효**하다. 반면 Review Surface[0] · dependencies[0] 는 「스펙 PR 머지 → v2 재결속 → v1 digest 는 승인하지 않는다」고 적어 규칙보다 한 단계를 더 넣었다. 둘 다 말이 되지만, 어느 쪽으로 갈지 정하지 않으면 승인자가 헷갈린다.
- target_specs = `DAY-SPEC-003` 하나. A1 의 「채팅 목록」과 개정 ⑥ 은 DAY-SPEC-004 이다. 개정 ⑥ 은 범위 줄을 좁힌 것뿐이라 빠져도 계약이 틀리지는 않지만, spec-sync 때 004 를 놓칠 수 있다.
- 고칠 방향: 사용자 판단 U-1 참조. v2 를 낸다면 target_specs 에 DAY-SPEC-004 를 더하고 W-3 문구를 함께 반영한다.

## 조용히 통과하는 자리

- **S-1 `clearIf` 원자성** — A-48 · Delivery 검증 어디에도 401 · `session_expired` 경로가 없다. Kotlin 구현이 비교 없이 지우거나(`clear` 로 대신) 직렬화를 안 해도 에뮬레이터 확인은 모두 초록이다. code review 에서 `AppDelegate.swift:170` 과 줄 단위로 대조해야 잡힌다.
- **S-2 스텁이 없어도 화면이 같다** — 위 코드 대조대로 push · video 는 Dart 가 예외를 다 삼킨다. 그래서 「스텁을 만들었다」는 화면으로 증명되지 않는다(스텁 없이 MissingPluginException 이어도 A-48 통과). 증명이 필요하면 PR 에 Kotlin 핸들러 코드가 있는지로 본다.
- **S-3 설치 id 유지** — spec-003 :509 「설치 id — Keychain · 로그아웃해도 유지」. Android 스텁 `installId` 는 「값」만 정했고 유지 여부는 정하지 않았다. 지금은 등록이 없어서(로그아웃 때 `DELETE /api/devices/{id}` 가 404 로 끝나고 `push_coordinator.dart:118-122` 가 삼킴) 아무 차이가 없다. FCM 붙일 때 다시 볼 자리.
- **S-4 `appName`** — push 스텁의 `appName` 은 통역 마이크 거부 문구에만 쓰인다(`interpret_controller.dart:144-145,244-249`). null 이면 'DAY' 로 대신하니 깨지지 않는다 — 다만 「DAY Dev」 대신 「DAY」가 뜬다.
- **S-5 iOS 「변경 0」** — Delivery A3 「`ios/` 변경 0」. `flutter create --platforms android` 가 `app/.metadata` 등을 건드릴 수 있다. ios/ 밖이라 조건은 통과하지만, PR diff 에서 따로 본다.

## 직원이 실물에서 만날 자리 (Android 개발 앱)

- 설정 탭 「알림 꺼짐 · 설정에서 켜기」 빨강 — 늘 보임 · 켤 수 없음(W-4).
- 채팅에서 동영상을 고르면 「동영상을 보내지 못했어요」 — 고르는 칸은 그대로 있다(Dart 무변경 · planner 미결 3).
- 받은 동영상 재생 — 재생은 `video_player` 가 하므로 되지만, iOS 처럼 무음 스위치를 따르는 오디오 전환은 없다.
- 통역 — 확인 안 됨(W-1). 마이크 권한 · 소리 출력이 Android 에서 될지 모른다.
- 원장 호출 · 채팅 푸시 · 알림 [수락] 없음(결정대로).

## 사용자 판단이 필요한 것

- **U-1 Delivery 승인 경로** — (a) 규칙대로 v1(`321a434b` 기준 · 개정 ⑭ 는 Target Delta)을 바로 승인한다, 또는 (b) planner 메모대로 스펙 PR 머지 → 같은 key v2 재결속(W-3 문구 · target_specs 에 DAY-SPEC-004 추가) → v2 승인. 지금 Issue 본문은 (b)를 적었다. (a)로 가면 Review Surface[0] 문구를 v2 에서 고치거나 무시해도 된다.
- **U-2 통역** — 사용자는 「통역 오디오 전환이 빠진다」고 알고 있었다. 코드상 통역은 `day/video` 와 무관하다(정정 맞음). 그러면 Android 에서 통역을 **이번 완료 조건에 넣을지**(마이크 권한 · 소리 출력 확인) 아니면 지금처럼 밖에 둘지.
- **U-3 Dart 무변경을 아키텍처 [확정]으로 둘지**(W-2) — 이번 범위에만 묶을지.

## 참고 (기존 부채 · 고치지 않아도 됨)

- `products/day/40-architecture/README.md:22` 「설정은 아직 안 함」 — Android 와 무관하게 이미 낡음(iOS 설정 끝남). planner 도 같은 판단.
- `products/day/20-spec/spec-003-mobile-app.md` frontmatter title 「직원 앱 (iOS · 1차 시술 현황)」 · :24 「iOS 먼저 · iPhone · iPad」 — 틀린 말은 아니다(iOS 먼저). Android 개발 앱이 범위 안에 들어왔으니 다음 개정 때 볼 자리.
- mobile-deployment §1-1 「지금 상태」(:51-59)에 Android 줄이 없다. 지금은 아직 「코드 없음」이니 맞다 — 코드 PR 머지 뒤 spec-sync 때 한 줄.
- spec-005 :68 「Android · FCM — mobile-deployment 미결 그대로」 — 사실 맞음. 그대로.
- spec-004 :452 「Android 는 넓히지 않는다」 — 채팅 푸시 Delivery 문맥이라 맞음. 그대로.
- `products/day/log.md:17` PR 칸 「근거 … (PR 전 · 코디가 PR)」 — 규칙(PR 번호 또는 닿는 링크)과는 다르지만 같은 날 다른 행(:18)도 같은 모양이다. PR 번호가 나오면 바꾼다.
- 모바일 범위 grep 재집계: `grep -rn -i "android\|fcm\|application id\|app/android" products/day/`(90-archive 0) — planner 표의 파일 밖에서 걸리는 것은 20-spec.md:41 · 40-architecture/README.md:22 · spec-004 :38 · :78 · :452 · spec-005 :68 뿐이고 모두 planner 표에 있다.
