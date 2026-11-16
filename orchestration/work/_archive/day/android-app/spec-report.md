# android-app — 스펙 개정 · Delivery 발행 결과 (planner)

## 상태: done (승인 대기 — receipt 적용 안 함)

| 항목 | 값 |
|---|---|
| Issue | **#251** — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/251 (OPEN) |
| 제목 | DAY 직원 앱 Android 개발 앱(DAY Dev) 로컬 에뮬레이터 실행 — app/android 생성 · day/session 구현 · day/push · day/video 스텁 (DAY-SPEC-003 개정 ⑭) |
| idempotency key | `day/android-dev-app-local-run` · contract_version 1 |
| 라벨 | `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready` |
| risk_level | **L2** — 새 플랫폼(`app/android`) 생성 · 세션 토큰을 보관하는 Android 네이티브 코드 · 빌드 주입 방식 미정. 서버 · 공개 API · migration · 배포 · 외부 쓰기 없음 · iOS 무변경 |
| contract_digest | `sha256:be3ecbd8a4ecdcc49df841acfa3fb2082d0360148504f5e7e5598a570cbcd6f6` |
| plan_digest | `sha256:2a25e08eff36d72208db0542f1c11a372598e7f969a4e861b42d3d9693d582ff` |
| baseline | `ready` · mediness `origin/main` `321a434b628cb7eee16c4a399d4197e060350b8b`(DAY-SPEC-003 이 이미 stable). **주의**: 개정 ⑭ 는 이 워크트리에만 있음(미커밋) — Review Surface[0] 에 「스펙 PR 머지 → 같은 key v2 재결속 → 사용자 승인 · v1 digest 는 승인하지 않는다」 적음 |
| next_action | `review-delivery-plan` · human_gate true — 사용자가 plan_digest 를 승인해야 함(**receipt 적용 안 함**) |
| task_projection | blocked(`delivery-plan-review-required`) · `partial: true` · core healthy |

## 전수조사 — `grep -rn -i "android\|fcm\|application id" products/day/` (시작 시 52줄 · 90-archive 0)

| 파일:줄(수정 전) | 내용 | 처리 |
|---|---|---|
| mobile-deployment.md:4 · :10 | 제목 「(iOS · Android)」 | 그대로 — 문서 범위 이름 |
| mobile-deployment.md:34 | iOS 먼저 · Android 도 적음 | 그대로 — 여전히 사실 |
| mobile-deployment.md:35 | [미결] Android 착수 · 출시 | **고침** → 착수 [확정] 로컬 실행만 · 출시 여부 · 시점 [미결] |
| mobile-deployment.md:43 | 설치 기기(M-1 · §7-3 영향) | 그대로 — 바뀐 사실 없음 |
| mobile-deployment.md:44 | Android Application ID [미결](M-4) | **고침** → 개발 앱 = `day.medisolveai.dev` · 정식 [미결] |
| mobile-deployment.md:69-84 | mermaid 다이어그램(AndDev · AndProd · FCM 후보) | 그대로 — 구조도(후보 표시 그대로) |
| mobile-deployment.md:89-91 | 앱은 발송 API 안 부름 · FCM 설정 파일 설명 | 그대로 — 일반 설명 |
| mobile-deployment.md:97 | 식별자 설명 | 그대로 |
| mobile-deployment.md:101 · :102 | §3 표 dev · prod | **고침** dev Android [확정] `day.medisolveai.dev` · prod [미결] 그대로 |
| mobile-deployment.md:104 | Android id · Google 계정 [미결] | **고침** + 빌드 주입 방식 미정 한 줄 추가 |
| mobile-deployment.md:121 | §4 productFlavors [제안] | 그대로 — 주입 방식 미정(정할 것) |
| mobile-deployment.md:178 · :180 | §7 머리 · 착수 [미결] | **고침** + **§7-0 신설**(이번 착수 범위 · 채널 3개 표 · 세션 보관 [제안] 유지 · 남은 미결) |
| mobile-deployment.md:184 · :185 | §7-1 계정 [미결] · id 후보 | 계정 그대로 · id 후보 줄 **고침** |
| mobile-deployment.md:189 · :191 | keystore · 세션 토큰 [제안] | 그대로 — [제안] 유지(사용자 미결정) |
| mobile-deployment.md:200 · :206 · :207 | 배포 방식 [미결] · 개발자 인증 | 그대로 |
| mobile-deployment.md:215 | §8-1 FCM [제안 · 후보] | 그대로 + **줄 추가**(이번엔 푸시 없음 · 다음 작업 · M-9 미결) |
| mobile-deployment.md:232 | 기기 토큰 구분 향후 계약 | 그대로 |
| mobile-deployment.md:246 | §9 식별자 행 | **고침** + **Android 행 추가** |
| mobile-deployment.md:269 | versionName · versionCode 설명 | 그대로 |
| mobile-deployment.md:297 | §12 끝 Android 순서 · 착수 [미결] | **고침** |
| mobile-deployment.md:303 · :305 | M-1 · M-3 | 그대로 — 바뀐 사실 없음 |
| mobile-deployment.md:306 | M-4 | **고침** — 개발 앱 id 만 닫음 · 정식 남음 |
| mobile-deployment.md:309 | M-7 최소 버전 | 그대로 — 정할 것(minSdk) |
| mobile-deployment.md:311 | M-9 FCM | **고침** — 「이번엔 안 함 · 다음 작업」 사실만 더함 · 미결 그대로 |
| mobile-deployment.md:313 · :317 | M-11 · M-15 | 그대로 |
| mobile-deployment.md:319 | M-17 | **고침** — 착수만 닫음 · 출시 여부 · 시점 남음 |
| mobile-deployment.md:329 · :337 · :338 · :341 | 공식 문서 링크 | 그대로 |
| 20-spec.md:41 | 범위 밖 「Android」 | **고침** → Android 정식 앱 · 출시 · 푸시(개발 앱 로컬 실행만 범위 안) |
| spec-003:105 | 범위 밖 「Android」 | **고침** → 정식 · 출시 · 배포 · FCM · 알림 [수락] · 동영상 보내기 Android 판 |
| spec-004:76 | 「Android 앱 · FCM · `app/android` 없음」 | **고침** — `app/android 없음`이 이번 작업으로 사실이 바뀌고, 채팅 목록 확인이 완료 조건에 들어가므로 좁힘(개정 ⑥) |
| spec-004:450 | 채팅 푸시 Android 넓히지 않음 | 그대로 — 여전히 사실 |
| spec-005:68 | Android · FCM — iOS 먼저 · 미결 그대로 | **그대로** — 알림(푸시)은 Android 에서 여전히 없음 · FCM 미결 사실 변화 없음 |
| 40-architecture/README.md:22 | mobile-deployment 설명 「설정은 아직 안 함」 | **그대로** — Android 와 무관하게 이미 낡은 줄(iOS 설정 완료). 이번 관심사 밖 · 고칠지 코디 판단 |
| log.md:64 | 2026-11-08 기록 | 그대로 — 이력 |

## 스펙 변경 (products/day 만 · 미커밋)

- `40-architecture/mobile-deployment.md`
  - :19-20 개정 메모 「2026-11-12 ② — Android 착수 범위 = 개발 앱 로컬 실행만」
  - :37 §1 착수 [확정] · 출시 [미결]
  - :46 §1 Android id — 개발 앱만 닫음
  - :103 · :106-107 §3 표 dev Android · 설명 줄 · 빌드 주입 방식 미정 줄
  - :183-198 §7 머리 + **§7-0 이번 착수 범위**(목표 · Dart 무변경 · 채널 3개 표 · 세션 보관 [제안] · 남은 미결)
  - :203 §7-1 id 후보 줄
  - :234 §8-1 이번엔 푸시 없음 · FCM 다음 작업 · M-9 미결
  - :265-266 §9 식별자 행 · Android 행
  - :317 §12 끝
  - :326 M-4 · :331 M-9 · :339 M-17
- `20-spec/spec-003-mobile-app.md`
  - :63-64 개정 ⑭ 메모
  - :95 §1 범위 안 표에 Android 개발 앱 행
  - :108 §1 범위 밖 Android 행 좁힘
  - :555 §3 세션 보관 「저장소」 — Android 같은 동작 · 저장 위치 [제안] 확정 아님
  - :563-575 §3 새 절 「Android 개발 앱 — 네이티브 채널」(채널 3개 · 결과 · 통역 오디오 사실 · id 주입 방식 미정)
  - :590-591 §3 푸시 — Android 등록 없음 · `platform` enum `ios` 그대로
  - :920 §4 인수 조건 **A-48**(에뮬레이터 dev 로그인 → 시술 현황 · 채팅 목록 · 자동 로그인 · 로그아웃 · iOS 빌드)
- `20-spec/spec-004-internal-chat.md` — :8 last_updated · :37-38 개정 ⑥ 메모 · :78 뺌 줄 좁힘
- `20-spec.md` — :9 최종 수정 · :41 범위 밖 줄
- `log.md` — :17 `arch-change, spec-change` 한 행(DAY-SPEC-003, DAY-SPEC-004)
- 새 화면 문구 없음 · 기획안(`00-baseline/planning/`) 무수정 · 키 · 계정 · 서버 값 없음

## 닫은 미결 / 남은 미결

| # | 닫은 것 | 남은 것 |
|---|---|---|
| M-17 | 착수 = 개발 앱 로컬 에뮬레이터 실행만(2026-11-12) | 출시 여부와 시점 |
| M-4 | Android 개발 앱 id = `day.medisolveai.dev` | 정식 앱 Android id |
| M-9 | (닫지 않음) 「이번엔 안 함 · 다음 작업」 사실만 더함 | FCM 도입 여부 · 방식 |
| M-3 · M-11 · M-7 · M-6 · M-8 | — | 그대로(배포 방식 · keystore · 최소 버전 · 로컬 접속 방식 · 권한) |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning, 그중 `products/day/` **0**(나머지는 다른 제품에 원래 있던 WARN — 무관)
- 근거 없는 정책 0 — 세션 저장 위치 · 빌드 주입 방식 · 정식 id · 배포 · keystore · FCM 은 [제안] / [미결] 그대로

## 미결 · 주의점

1. **브리프 사실 정정 — 「통역 오디오 전환」**: 코드상 `day/video` 의 `audioSave` · `audioFollowSilent` · `audioRestore` 는 **채팅 동영상 재생 화면**의 오디오 세션(iOS 무음 스위치 따름)이다(`app/lib/chat/screens/chat_video_screen.dart:50,55,90`). 통역 오디오는 `app/lib/interpret/audio_io.dart` 가 `audio_session` 플러그인으로 하며 `day/video` 를 거치지 않는다. 그래서 스펙에는 「Android 에서 빠지는 것 = 채팅 동영상 보내기 · 동영상 재생 화면 오디오 전환」으로 적고, 「통역은 `day/video` 를 거치지 않음 · Android 통역 확인은 이번 완료 조건 밖」으로 적었다. 통역이 Android 에서 실제로 되는지는 확인하지 않았다.
2. **A-48 을 조금 넓힘**: 브리프 완료 조건(로그인 → 시술 현황 · 채팅 목록 · iOS 빌드)에 `day/session` 구현 확인용으로 「재실행 자동 로그인 · 로그아웃 뒤 세션 없음 · 푸시 없이 오류 화면 없음」을 더했다(Issue A2). 빼길 원하면 v2 에서 뺀다.
3. **동영상 스텁의 화면 결과**: Dart 는 probe · convert 실패를 null 로 받아 지금 문구 「동영상을 보내지 못했어요」(DAY-SPEC-004 U-6)를 낸다 — 새 문구 없음. 동영상 고르기 칸 자체를 Android 에서 숨기려면 Dart 변경이라 Non-Goal.
4. **로그아웃 때 기기 해제 `DELETE /api/devices/{install_id}`** 는 Dart 가 그대로 부른다(등록이 없었으니 서버가 없음으로 답함 · 「실패해도 계속」 계약 그대로). 서버 변경 없음.
5. **baseline**: 개정 ⑭ 가 main 에 없는 상태의 v1 이다 — 스펙 PR 머지 뒤 같은 key · version 2 로 재결속하고 그 digest 를 사용자가 승인해야 한다(Review Surface[0]).
6. `40-architecture/README.md:22` 「설정은 아직 안 함」은 Android 와 무관하게 낡은 줄 — 손대지 않음.
7. 하네스 실행으로 `tools/harness/.venv` 생김(gitignore 대상 · git status 에 안 보임).

## 정할 것 (구현 · 코디 · 사용자)

- Application ID · 앱 이름을 Android 빌드에 넣는 방식(`productFlavors` · 명령줄 빌드 값 등) — 구현에서 정해지면 mobile-deployment §3 끝 줄 · §7-1 에 반영
- Android 세션 저장 위치 — §7-2 [제안] 을 따르되 [확정] 은 사용자 몫
- minSdk(플러그인 요구 · M-7)
- 다음 작업(범위 밖): FCM · 알림 [수락] Android 판 · `day/video` Kotlin 구현 · Play Console · keystore

## 파일

- request · 결과: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-android-app-spec/d24f9428-a925-449b-83a1-643e88d80e35/scratchpad/delivery/android.v1.request.json` · `android.v1.plan.json` · `android.v1.apply.json`
- 코드 워크트리 수정 0 · 커밋 · push · PR 0
