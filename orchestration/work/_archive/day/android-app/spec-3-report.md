# planner 3회차 리포트 — 범위 확장: 개발 앱 Play 내부 테스트 (2026-11-13)

워크트리 `mediness-mediness/android-app-spec` · 커밋 `cb14f570`(PR mediness#940) 위에 **미커밋** · `products/day/` 만 · 커밋 · push · PR · Delivery · receipt 없음.
값(계정 이메일 · 키 · 서비스 계정 이름 · 개발자 계정 id)은 한 군데도 쓰지 않았다 — 경로(`~/.config/day/android/`)와 칸 이름만.

## 1. 변경 파일:줄

| 파일 | 줄 | 바뀐 것 |
|---|---|---|
| `40-architecture/mobile-deployment.md` | :22 | 개정 노트 **2026-11-13 ③** — 결정 ①~⑤ · 닫히는 만큼만(M-3 · M-11 · M-12 · M-17) |
| 〃 | :39 · :40 §1 | 착수 = 로컬 실행 + **개발 앱 Play 내부 테스트** · 정식 출시 [미결] / 새 줄 「[확정] 조직 명의 Play Console 권한 있음 · 값 안 적음」 |
| 〃 | :64 §1-1 | Android: 권한 있음 · 앱 · 첫 업로드 · 업로드 키 · 서비스 계정은 **아직 안 함**(사용자 손 단계 §7-3-2) — 설정되면 [설정 완료] 로 |
| 〃 | :187 §7 머리 | 착수 = §7-0(11-12 · Play 11-13) · 정식 출시 [미결] |
| 〃 | :189-205 §7-0 | 제목 「+ Play 내부 테스트」 · 목표 ① 의 「Google 쪽 등록은 하지 않는다」 취소선 · **목표 ②**(:192) Play 내부 테스트 → 테스터 기기 Play 설치 → dev 로그인 · 마지막 [미결] 줄(:205) 갱신(계정 닫힘 · M-3/M-11 남은 것 · M-12 추가) |
| 〃 | :209 §7-1 | 계정 [미결] → [확정] 조직 Play Console 권한 |
| 〃 | :215-218 §7-2 | [확정] Play 앱 서명(앱 서명 키 = Google · 업로드 키만 우리 · 재설정 요청 가능) · [확정] 업로드 키 · 서비스 계정 키 = 로컬 `~/.config/day/android/` 600 · [미결] 백업 위치 · 담당 · dev/prod 키 분리(정식 앱 때) · 옛 [제안] 줄 취소선 |
| 〃 | :227-230 §7-3 | 표에 「Google Play 내부 테스트」 행 · [확정] 개발 앱 = 내부 테스트 · [미결] 정식 앱 배포 방식(M-3 남은 것) |
| 〃 | :232-248 **§7-3-1 신설** | 공식 문서 확인 조건 표(확인일 2026-11-13) — 아래 §3 |
| 〃 | :250-259 **§7-3-2 신설** | 사용자 Play Console 손 단계 6개 — 아래 §4 |
| 〃 | :275 §8-1 | 「이번 Android 착수(로컬 실행 · Play 내부 테스트)에도 푸시 없음」 · 「회사 Google 계정 생긴 뒤」 → 계정은 생김 · 그래도 다음 작업 |
| 〃 | :307-308 §9 | Android 행 = 로컬 + Play 내부 테스트 · 새 행 「Android 서명 · 업로드」 |
| 〃 | :359 §12 | Android 문단 — 11-13 개발 앱 Play 내부 테스트까지 · 정식 id · 정식 배포 · 백업 · CI [미결] |
| 〃 | :367 · :373 · :375 · :376 · :381 §13 | M-3 · M-9 · M-11 · M-12 · M-17 (§5 표) |
| 〃 | :386 이하 §14 | 제목 「(Google Play 줄 2026-11-13)」 · Play 문서 10줄 추가 |
| `20-spec/spec-003-mobile-app.md` | :64 개정 ⑭ | 「스토어 출시 … 범위 밖 그대로(개발 앱 Play 내부 테스트는 보강 ② 로 범위 안)」 · 끝에 **「2026-11-13 보강 ②」** 문장(Play 내부 테스트 · Play 앱 서명 · 정본 mobile-deployment §7-0 · §7-3 · A-49 · 정식 id · 정식 배포 · FCM 범위 밖) |
| 〃 | :95 §1 범위 표 | 「Play 내부 테스트 트랙 업로드 → 테스터 기기에서 Play 로 설치」 · 근거 칸 |
| 〃 | :108 범위 밖 | 「Android 정식 앱 · 정식 출시 · 정식 배포 · …」 · M-3 추가 · 「로컬 실행 · Play 내부 테스트는 범위 안」 |
| 〃 | :565 · :575 Android 절 | 로컬 · Play 내부 테스트 빌드 = 같은 앱 · 같은 채널 동작 / 새 줄: 서명 · 업로드 경로(정본 mobile-deployment §7-2 · §7-3-1 · §7-3-2) |
| 〃 | :922 **A-49 신설** | Play 내부 테스트 트랙에 개발 앱 빌드 처리 완료 → 내부 테스터 기기(실기기 또는 Play 스토어가 있는 에뮬레이터) 참여 링크 → Play 설치 → dev 로그인 → 시술 현황. 확인 칸 「테스터 기기(사용자 · 첫 빌드 손 업로드 뒤)」. A-48 그대로 |
| `20-spec/spec-004-internal-chat.md` | :8 · :38 · :78 | last_updated 11-13 · 개정 ⑥ 끝에 「(2026-11-13 보강) Play 내부 테스트에도 올린다 — 채팅 쪽 빠지는 것은 같다」 · 「Android 는 개발 앱 로컬 실행 · Play 내부 테스트만」 |
| `20-spec.md` | :41 | 「로컬 에뮬레이터 실행 · Play 내부 테스트만 범위 안」 |
| `log.md` | :17 | 2026-11-13 `arch-change, spec-change` · DAY-SPEC-003, DAY-SPEC-004 행 추가 |

## 2. 전수조사 — `grep -rn -i "android\|play\|fcm\|keystore" products/day/` (display · player 등 제외 · 90-archive 0)

mobile-deployment · spec-003 은 위 §1 에서 전부 다뤘다. 그 밖:

| 위치 | 내용 | 사실이 바뀌었나 | 처리 |
|---|---|---|---|
| `20-spec.md:41` | 「개발 앱 로컬 에뮬레이터 실행만 범위 안」 | 예 | **고침** |
| `spec-004:38` 개정 ⑥ | 「로컬 에뮬레이터 … 채팅 목록 확인까지 범위 안」 | 예(Play 추가) | **고침** — 같은 개정 안 보강 |
| `spec-004:78` 뺌 표 | 「Android 는 개발 앱 로컬 실행만」 | 예 | **고침** |
| `spec-004:452` | 채팅 푸시 「Android 는 넓히지 않는다」 | 아니오(푸시 그대로 없음) | 그대로 |
| `spec-005:68` | 「Android · FCM — iOS 먼저 · mobile-deployment 미결 그대로」 | 아니오(FCM 미결 그대로) | 그대로 |
| `40-architecture/README.md:22` | 「설정은 아직 안 함」 | 이미 낡음(iOS) · 이번 범위 아님 | 그대로(1 · 2회차와 같은 판단) |
| `log.md:66 · :18` | 과거 이력 행 | 이력이라 고치지 않음 | 그대로 |
| spec-003 :24 · title 「iOS」 | Android 가 Play 내부 테스트까지 와도 출시 대상은 iOS 하나 | 아니오 | 그대로(2회차 §5 판단 유지 — 정식 출시 정해질 때) |

## 3. 공식 문서 확인 (2026-11-13 · Google 공식 문서만 · 스펙 §7-3-1 · §14 에 반영)

| 질문 | 답 | 확인 | 링크 |
|---|---|---|---|
| 내부 테스트 첫 출시 심사 | 첫 업로드는 내부 테스터에게 바로 · 표준 검토를 「받지 않을 수 있다(might not)」 — 「심사 없음」 단정 아님 | 확인 | support.google.com/googleplay/android-developer/answer/9845334 |
| targetSdk 최소 | **Android 16(API 36)** · 2026-08-31 부터 새 앱 · 업데이트 · 연장 기한 11-01 지남. 내부 테스트 트랙에도 걸리는지 문서에 없음 | 값 확인 · 트랙 **확인 안 됨** | …/answer/11926878 |
| 데이터 보안 | 내부 테스트에만 있는 앱은 **불필요** | 확인 | …/answer/10787469 |
| 개인정보처리방침 URL · 등급 · 타깃 연령 · 광고 · 앱 접근 | 「게시 전 선언」 · 트랙별 예외 언급 없음 | **확인 안 됨** | …/answer/9859455 |
| AAB 필수 | 새 앱은 AAB(2021-08~) | 확인 | developer.android.com/guide/app-bundle |
| 첫 업로드 수동 | API 는 빌드가 이미 있는 앱만 → 첫 빌드 Play Console 손 | 확인 | developers.google.com/android-publisher/edits |
| 테스터 초대 | 이메일 목록 · 앱당 최대 100 · 게시 뒤 참여 링크. Google 그룹 = 문서에서 못 찾음 | 확인(그룹 확인 안 됨) | …/answer/9845334 |
| Play 앱 서명 | 새 AAB 앱 기본 등록 · 앱 서명 키 Google · 업로드 키 개발자 · 업로드 키 분실 시 재설정 요청 | 확인 | …/answer/9842756 |
| 서비스 계정 | Cloud 프로젝트 → API 켜기 → 서비스 계정 → Play Console 사용자 및 권한 초대. Cloud 프로젝트 연결 단계 폐지. 출시 권한 이름은 문서에 없음 | 확인(권한 이름 확인 안 됨) | developers.google.com/android-publisher/getting_started |
| 12명 · 14일 테스트 | 2023-11-13 뒤 **개인** 계정의 프로덕션 조건 · 내부 테스트엔 조건 없음 · 조직 계정 예외 명시 없음 | 조직 = **확인 안 됨**(이번엔 무관) | …/answer/14151465 |
| 조직 계정 조건 | D-U-N-S · 웹사이트 · 연락처 확인 — 이미 권한 받음 | 확인 | …/answer/13628312 |

## 4. 사용자 Play Console 손 단계 (스펙 §7-3-2 와 같음)

1. 앱 만들기(`DAY Dev` · 패키지는 첫 AAB 의 `day.medisolveai.dev`).
2. 업로드 키 만들기 → `~/.config/day/android/`(600). 백업 위치 · 담당 [미결].
3. 내부 테스트에 첫 AAB 손 업로드 + Play 앱 서명 받아들이기.
4. 게시 전 Play Console 이 요구하는 앱 콘텐츠 선언(데이터 보안은 불필요).
5. 내부 테스터 이메일 목록(≤100) → 게시 → 참여 링크 전달.
6. Cloud 프로젝트 · Play Developer API · 서비스 계정 · 키 JSON(`~/.config/day/android/` 600) → Play Console 에 초대 · 이 앱 출시 권한. 둘째 빌드부터 API.

> 2번(업로드 키 생성)은 코드 워커가 명령(`keytool`)을 안내 · 실행할 수도 있다 — 누가 할지는 코디 판단. 키 파일은 저장소에 들어가면 안 된다.

## 5. 닫은 / 남은 미결

| # | 닫음 | 남음 |
|---|---|---|
| M-3 | 개발 앱 배포 = Play 내부 테스트 · 회사 Google 개발자 계정(권한 있음) | **정식 앱 Android 배포 방식** |
| M-4 | (1회차) 개발 앱 id | 정식 앱 Android id |
| M-9 | — (사실만: 계정은 생겼어도 FCM 은 다음 작업) | FCM 도입 여부 · 방식 |
| M-11 | 키 보관 = Play 앱 서명 · 업로드 키 로컬 | **업로드 키 백업 위치 · 담당** · dev/prod 키 분리(정식 앱 때) |
| M-12 | — (사실만: 업로드 지금 로컬 · 키 2개 로컬) | CI 서명 · 비밀 저장 |
| M-17 | 착수 = 로컬 실행 + Play 내부 테스트 | 정식 출시 여부 · 시점 |
| M-7 | — | 최소 Android 버전(minSdk). targetSdk 는 Play 요구로 API 36 이 사실상 정해짐(스펙 §7-3-1 · 결정 아님) |

## 6. Delivery v2 변경 목록 (2회차 §4 + 리뷰 2 R-1~R-4 + Play 범위 · 이번엔 안 함)

같은 key `day/android-dev-app-local-run`(Play 가 붙어 key 이름이 좁다 — 같은 key 를 쓸지 새 key 로 갈지 코디 판단. 같은 key 권장: v1 을 대체하는 것이므로) · baseline = mediness#940 머지 SHA.

- **target_specs**: `DAY-SPEC-003`, `DAY-SPEC-004`.
- **risk**: **L2 → L3 로 올릴 것을 권장.** `rules/delivery-workflow.md:60` 「`L3` = … production · **external write** · merge/deploy」 — Play 업로드는 외부 쓰기이고, **패키지 이름(`day.medisolveai.dev`)은 Play 에 한 번 올리면 그 계정에서 되돌릴 수 없다**(앱을 지워도 패키지명 재사용 불가 — 일반 지식 · 이번에 공식 문서로 확인 안 함). 내부 테스트라 사용자 노출은 작지만 규칙 문구상 L3. 승인은 사용자 몫 그대로.
- **Target Delta**:
  1. (v1) `app/android/` 생성 · Application ID `day.medisolveai.dev` · 이름 `DAY Dev` · `day/session` Kotlin 구현 · `day/push` · `day/video` 스텁.
  2. (2회차) 통역 Android — 마이크 권한(매니페스트) · 녹음 · 자막 · 번역 음성 · 빠른 말하기 TTS · 통역 플러그인 Android 설정.
  3. (3회차) **release AAB 빌드** · targetSdk 36(Play 요구) · 업로드 키 서명 설정(키 경로 · 비밀번호는 저장소 밖 `~/.config/day/android/` 에서 읽음 · 저장소엔 값 없음 · gitignore) · **Play Developer API 업로드 스크립트**(서비스 계정 키 경로 = 로컬 · 내부 테스트 트랙 · 둘째 빌드부터) · 버전 코드 규칙(빌드 번호 — mobile-deployment §10 · M-13 은 미결이므로 스크립트가 강제하지 않고 인자로).
- **A 조건**:
  - A1 로그인 → 시술 현황 · 채팅 목록(v1).
  - A2 「로그아웃 뒤 앱을 다시 켜면 로그인 화면」(W-3).
  - A3 iOS 변경 0 · `flutter create` 가 건드린 `ios/` 밖 파일은 PR diff 에서 따로(리뷰 1 S-5).
  - A4 「Dart 변경 0 — 바꿨다면 코디 확인 기록」(R-3 ②).
  - A5 통역(스펙 A-48 통역) + 「칩이 있는 언어(`en` · `ja` · `zh` · `zh-Hant` · `th`) 중 하나 이상 소리 · 음성 없는 언어는 U-15 토스트(정상)」(R-2 — 정하는 것은 코디).
  - **A6 Play 내부 테스트(스펙 A-49)**: 내부 테스트 트랙 빌드 처리 완료 → 테스터 기기 Play 설치 → dev 로그인 → 시술 현황. **둘째 빌드가 API 로 올라가 테스터 기기에서 업데이트됨**(업로드 스크립트 증명).
  - 저장소에 키 · 비밀번호 · 서비스 계정 JSON 0(`git grep` · gitignore 확인).
- **Non-Goals**: 정식 앱(id · Play 등록 · 프로덕션 · 비공개 배포) · FCM · 알림 [수락] Android · 동영상 보내기 Android · CI 업로드 · iOS 변경. 「Dart 동작 · 화면 · 문구 변경」은 Non-Goal 에서 빼서 메모로(R-3 ②). **Review Surface[4] 「Android 통역 확인은 완료 조건 밖」 삭제**(R-3 ①).
- **code_surface**: `app/android/**`(Kotlin 채널 · `AndroidManifest.xml` 마이크 권한 · `build.gradle(.kts)` applicationId · targetSdk · 서명 설정 · 이름 리소스) · 업로드 스크립트(위치는 코드 작업 — 예: `app/tool/` 또는 `scripts/`) · `.gitignore`(키 · `key.properties`) · `app/.metadata`(flutter create 산물).
- **phases**: AND-1 Android 스캐폴드 · id · 이름 → AND-2 `day/session` 구현 · push · video 스텁 → AND-3 통역 Android 설정 · 에뮬레이터 확인 → AND-4 로컬 에뮬레이터 A1~A5 → **AND-5 release AAB · 업로드 키 서명 · targetSdk 36** → **AND-6 사용자 손 단계(§7-3-2 1~6) 대기 · 첫 AAB 넘김** → **AND-7 Play API 업로드 스크립트 · 둘째 빌드 업로드 · A6**.
- **verification**: 에뮬레이터 A1~A5(R-1 에뮬레이터 호스트 마이크 켜기 · R-2 TTS 언어) · `flutter build appbundle` 성공 · AAB 서명 확인(`jarsigner -verify` 또는 동등) · 저장소 비밀 0 검사 · 테스터 기기 A6(사용자).
- **dependencies**: ① **사용자 수동 단계** §7-3-2(앱 만들기 · 첫 AAB · 앱 서명 · 테스터 · 서비스 계정 초대) — AND-6 에서 막힘 ② **업로드 키 · 서비스 계정 키 JSON 이 로컬 `~/.config/day/android/` 에 있어야** AND-5 · AND-7 진행 ③ **dev 서버 통역(D-3) 동작**(R-4) — A5 · 꺼져 있으면 앱 문제로 오판 ④ 스펙 PR mediness#940 머지(baseline) ⑤ 테스터 기기(실기기 또는 Play 있는 에뮬레이터 — 정할 것).
- **rollback**: 코드 = PR 되돌림(iOS 영향 0). Play = 내부 테스트 출시 중지 · 이전 빌드로(올라간 버전 코드는 되돌릴 수 없음 · 패키지명 고정 — 위 risk). 업로드 키 유출 시 Play 업로드 키 재설정 요청.

## 7. lint

`python3 scripts/lint-pipeline.py --strict` → exit 0 · `0 error, 263 warning` · products/day 줄 0(경고는 모두 다른 제품의 기존 경고).

## 8. 정할 것 · 주의

- **테스터 기기**: 실기기 유무 모름 — 스펙은 「테스터 기기(실기기 또는 Play 스토어가 있는 에뮬레이터)」로만 적음. Play 스토어가 있는 에뮬레이터 이미지(「Google Play」 시스템 이미지)로 A-49 를 볼지 사용자 확인.
- **업로드 키 백업 위치 · 담당**(M-11) — 사용자.
- **업로드 키 만들기 주체** — 사용자 손 vs 코드 워커가 로컬에서 `keytool` 실행(키는 저장소 밖). 코디 판단.
- **앱 콘텐츠 선언**: 개인정보처리방침 URL 등이 내부 테스트 게시 전에 요구되면 사용자가 채운다 — iOS 쪽 개인정보 처리 안내 링크(spec-003 개정 ⑫ 「정보」)를 쓸지 사용자 확인.
- **targetSdk 36**: Flutter 기본값이 36 이 아닐 수 있다 — 코드 작업에서 맞추고 플러그인(통역 · 세션 저장) 호환을 확인.
- **패키지명 고정**: `day.medisolveai.dev` 를 Play 에 올리면 그 이름은 바꿀 수 없다(일반 지식 · 확인 안 됨) — 개발 앱 id 는 이미 [확정](사용자 2026-11-12)이라 문제는 없지만 v2 승인 때 한 번 더 알린다.
- risk L3 상향 여부 — 코디 · 사용자.
