
# 재개 노트 — day-mobile-v2 (day)

**지금**: 조사 완료(`research-current-state.md` · 정할 것 18) · 통역 범위 결정 · 범위 결정 끝(M-1 ~ M-9 = spec 브리프 결정 표) · planner 발주 · Firebase 사용자 준비 중 · Run `run_fd60deae970e`
**다음**: **사용자 실기기 확인**(DAY Dev 0.2.0 — TestFlight (4) IN_BETA_TESTING · Play internal vc4 completed) → 피드백 모아 한 번에 → prod 서버 배포 → 정식 0.2.0(iOS 3 · Android 4) | 옛: 코드 다 됨(로컬 커밋 · push 전) · 배포 안 함(사용자) · 남은 = 글자 3 사용자 답 · migration 번호 정리(day-cc-mig 머지 뒤) · 로컬 E2E 여부 사용자 · 스펙 정리(planner) · #955 머지 · 재결속 · 승인 · (이전 메모:) backend P1 통역(진행) · designer 없음(사용자) · mobile M1(기존 API 만 쓰는 화면) 발주 · 스펙 PR mediness#955 **머지는 나중**(사용자 — 다른 스펙 작업 동시 진행) · planner 가 #262 · #263 v2 재결속(PR 커밋 7d198317 기준 · 진행)(spec-2/3-report 목록 반영) → plan 승인(사용자) → 코드 워커 P1 통역부터 · designer 시안 병행. PASS 면 스펙 PR → Delivery v2 재결속 · 승인(사용자) → 코드 워커(P1 통역 먼저)

세팅: `scripts/new-work.sh day day-mobile-v2` · 설정 SSOT `config/projects/day.json`
코디handle: `term_5e3720e2-a945-4350-86e9-f3f6bce65ac0`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec` (branch `kknaksss/day-mobile-v2-spec`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

범위(사용자 11-20) — 직원 앱(Flutter) 다음 버전 4건:

1. **KOS 기기 로그인 제한 → 이전 기기 로그아웃** — 웹은 kos-signin-limit(#257)에서 기기 선택(POST /login/device). 앱은 지금 401 `invalid_credentials` 그대로(회고 2026-11-17-kos-signin-limit §7 「앱 기기 선택 화면 · 앱 오류 안내 = 다음 앱 버전」). 화면 기준 = 웹 기기 선택 + KOS 캡처 `~/.config/day/reference/kos-device-limit-2026-11-17.png`(공개 레포 금지)
2. **시술 현황 탭 바뀐 화면** — 바로 시작 · 호출 취소 · 귀가 취소 등(웹은 fix-feedback #255 에서 바뀜). 호출 취소 알림 · 앱 푸시는 「앱 업데이트 뒤」로 미뤄 둔 것(새 notification_kind = enum migration · SPEC-005 OQ-N14)
3. **호출 취소 알림 · 앱 푸시** — 사용자 11-20 「이제 호출 취소 알림도 가야 한다」(fix-feedback 에서 앱 업데이트 뒤로 미룬 것)
4. **통역 = 통키 최신 따라가기** — 원천 kknaksss/interpret-pwa(11-16 tongky-quality-re1 · code #15 `56e43a0` · 시드 `.11`). DAY 통역은 11-11 fix 에서 이식한 옛 판

배경: Google Play 프로덕션 승인 · 배포됨 / Apple 0.1.0 (2) 심사 대기 — 사용자 「다음 버전 가도 될 것 같다」. 다음 빌드 = 정식 iOS 3 · Android versionCode 4(메모리 기준 · 조사에서 확인)

- [x] researcher 현황 조사 완료 — 추천 기본값 = 사용자에게 11-20 보고(버전 0.2.0 · ~~앱 버전 칸으로 옛/새 앱 가르기~~(11-20 뺌 — 옛 앱 사용자 없음) · 웹 기기 선택 재사용 · quick-start/undo-home JSON · can* 서버 계산 · designer 시안 · 시드 로더 넓힘 · Soniox 한도 코디 조회)
- [!] 정정(11-20): 「앱 로그아웃 때 KOS 세션 해제」는 넣지 않는다 — 해제 API 가 비밀번호를 요구해 로그아웃 때 불가(SPEC-001 규칙 15 · kos-signin-limit 결정 유지 · 리포트 B3)
- 웹에 닿는 것 = 호출 취소 알림 하나(웹도 같이 — §2)
- [!] 정정(11-20): 웹에는 알림 목록 · 종 배지가 없다(`static/day.js:1824-1834` — 원장 호출 OS 알림만). 호출 취소도 웹은 OS 알림만(OQ-N19). 앞서 사용자에게 「목록 · 배지에도 뜬다」고 한 것 틀림
- Firebase(11-20): 프로젝트 = 기존 Play 업로드용 GCP 프로젝트에 붙임 · Spark · GA 켜짐(무관) · 앱 2개 등록(`day.medisolveai.dev` · `day.medisolveai`) → `~/.config/day/android/google-services.json`(두 앱 다 · 600) · FCM API(V1) 사용 설정됨 확인
- Firebase 서비스 계정 키 받음(11-20) → `~/.config/day/android/fcm-service-account.dev.json` · `fcm-service-account.prod.json` — 같은 계정 키 2개를 환경별로 나눔(600 · 조직 정책 잠깐 풀어 발급 — 되돌림은 사용자). 서버 반영 = FCM WP(F1) 때 Key Vault(dev 먼저)
- [!] Delivery 재결속 막힘(11-20): 머지 전 PR 커밋 baseline 불가 → #955 머지 시점 사용자 판단 대기(#954 day-cc-mig-spec 이 같은 SPEC-000 을 고치는 중)
- 통역 동시 상한 3 · P1 W-1 시험 → backend P3 에 같이 넣음 · Soniox 한도 상향 = 사용자
- [x] 글자 3 결정(M5 발주) — 옛 메모: ① 드로어 재생 중 안내 「번역 음성이 나오는 동안은 듣지 않아요」(`interpret_widgets.dart:409` · 통키에 같은 뜻 없음 · 지움 제안) ② (선택) 「번역 읽는 중」 → 통키 「〈언어〉로 출력 중」(재생 언어 표시 기능 필요) ③ 대리 수락 창 「호출할 시술 · N개」(`doctor_picker.dart:433`)
- [ ] 실기기 볼 것(P5 검수 INFO): 출력 구간 벽시계 추정 · flush 뒤 녹음 재설정 · 메아리(I-6)
- [ ] P2 검수 WARN 코드 3건 → backend F1 에 같이 넣음 · SPEC-002 :672 canChangeDoctor 문장 ㉕ ③ 과 모순 → planner(스펙 정리 때 · M1 W-1 「복귀하기」와 같이)
- [x] **P3 고칠 것(c22b56bc)**: ⓪ 앱 뒤/꺼짐일 때 원래 원장 호출 푸시가 알림 센터에 남음(M3 이슈 1) → 서버가 원장 호출 · 호출 취소 푸시에 같은 `apns-collapse-id`(= callId) · FCM 은 같은 tag/collapse 로 — 취소 푸시가 원래 푸시를 OS 에서 덮음(코디 기본값 · 사용자에 통보) · ① 취소 뒤 늦게 도는 call_push 가 원래 푸시를 보내거나 닫힌 호출에 안 읽은 행(notifications.py:454-545 · 325-) — 실제 버그 · ③ JS 픽스처 NOTIFY_KIND 문자열이라 취소 닫기 시험 0(controllers.test.mjs:50) · ④ 재호출 뒤 취소 시험. ② 0012 앞 이미지로 롤백하면 알림 목록 500 → 배포 rollback 메모(되돌리기 = migration 도 같이)
- [x] **M2 고칠 것(841454c4 · 남은 범위 밖: 대리 수락 창 U-6 도 「호출할 시술」 칸 — 0.1.0 부터 · M1 캡처 같은 하네스 · 아이패드 원장 변경 두 칸)**: FAIL 원장 변경 창 「호출할 시술 · 1개」 = 웹에 없음 → 지움(`room_screen.dart:528` procs 비움) · WARN 바로 시작 rejected[] 코드마다 토스트 여러 장(웹 board.py:628) · 캡처 하네스 그림자(debugDisableShadows) · 호출 취소 ⋮ 의 state=='called' 덧붙인 조건 → can 만
- [!] **migration 번호 충돌**: 우리 `0012_doctor_call_cancel_kind` · `0013_device_platform_android` vs `day-cc-mig` 의 `0012_kos_keys` — 둘 다 down_revision 0011 → 두 head. 나중에 머지하는 쪽이 번호 · down_revision 을 이어 붙여야 함(우리 둘은 enum 값 추가뿐이라 옮기기 쉬움)
- [ ] M1 모아 둘 것: 검수 W-1(스펙 「복귀」→「복귀하기」 · planner 다음) · W-2(unsetActionCodes 손 복제) · W-3(거절 토스트 단언 약함) · 사용자 화면 확인 4(시트 제목 · ▾ · 띠 모양 · 의사 호출 시트 간호관리)
- [!] 사용자 대기: 조직 정책 되돌림 확인
- [x] planner 2차 완료 — F5 · W17 · A55 · N15 · N16 · N19 반영 · #262 문구 변경은 v2 재결속 때(spec-2-report)
- OQ-N16 닫음({N} 뺌) — planner 2차에 send 로 전달 프로젝트 생성 + google-services.json 2벌 + 서버 발송용 키
- [!] 문서 파이프라인(baseline→decision→spec→work) 닫고 나서 구현 발주

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-20 | 범위 = 위 3건 · Apple 심사 결과 기다리지 않고 다음 앱 버전 진행 | 사용자 |
| 2026-11-20 | 범위에 호출 취소 알림 · 앱 푸시 추가 | 사용자 |
| 2026-11-20 | 통역 엔진 정본 = 통키(interpret-pwa main `56e43a0`) 최신본 — DAY 는 그대로 따라간다(STT v6 · 시드 `.11` · 끊김 D-67 · 세 참여자 D-68~70 · 바로잡기 D-58~66). 통역 기록(records)만 DAY 에 없음 | 사용자 |
| 2026-11-20 | 시술 현황 앱 범위 — 넣음: 바로 시작 · 호출 취소 · 「간호관리」 표시 · 방 옮기기 · 원장 바꾸기 / 뺌: 귀가 대기 취소(앱에 귀가 대기 목록 없음) · 정렬 탭 · 순서 변경 | 사용자 |
| 2026-11-20 | 호출 취소 알림 = 추천대로: 받는 사람 = 그 호출을 받았던 원장(들) · 원래 호출 알림은 닫음. 제목 「호출 취소」 · 본문 ~~「{방} · 시술 {N}건 · 호출 취소」~~ → **「{방} · 호출 취소」**(11-20 사용자 — 줄 단위 취소라 N 이 헷갈려 뺌 · OQ-N16 닫음 · 방 없으면 「방」) | 사용자 |
| 2026-11-20 | Android 푸시(FCM) 이번에 넣음 — Firebase 프로젝트 · 앱 등록은 사용자(회사 Google 계정) | 사용자 |
| 2026-11-20 | 지금 배포된 앱(0.1.0)은 1차라 쓰는 사람 없음 · 이번 버전까지 해서 병원 인계 → **옛 앱 호환 안 챙긴다**(앱 버전 칸으로 옛/새 가르기 뺌 · 서버 응답 · 알림 종류 · 통역 프로토콜은 새 앱 기준으로 바로 바꾼다) | 사용자 |
| 2026-11-20 | 호출 취소 알림은 웹에도 같이 — ~~웹 알림 목록 · 종 배지 ·~~ 웹 OS 알림(원장 호출과 같은 대우 · OQ-N14 ⓔ 닫음) — 11-20 정정: 웹엔 목록 · 종 화면이 없어 OS 알림만(OQ-N19 · 사용자에게 정정 통보) | 사용자 「취소는 같이 가는 게 맞다」 |
| 2026-11-20 | 방 복귀도 앱에 넣는다(OQ-A55 닫음 · 기존 `/api/visits/{id}/room-return`) | 사용자 |
| 2026-11-20 | 새 알림 종류 이름 = `doctor_call_cancel`(OQ-N15 닫음) | 사용자 |
| 2026-11-20 | 호출 취소 알림은 **그 호출이 완전히 닫힐 때만**(남은 줄 0) 한 번 보내고 원래 원장 호출 알림도 그때 닫는다. 일부 줄 취소 = 알림 없음 · 원래 호출 그대로(OQ-N17 · 검수 2차 R-3) | 사용자(추천 A) |
| 2026-11-20 | 스펙 PR #955 머지는 나중 · Delivery 재결속은 PR 커밋 기준으로 먼저 | 사용자 |
| 2026-11-20 | #262 · #263 재결속 검수 PASS 면 **코디가 plan 승인 receipt 적용 → 바로 코드 발주**(사용자 위임 · 이번 두 Issue 한정). 첫 발주 = backend P1 통역 · designer P4 시안 병행 | 사용자 「검수 통과하면 승인하고 작업 바로 들어가」 |
| 2026-11-20 | **머지 · 승인 전에 코드 먼저**(B) — P1 통역 서버 · P4 designer 시안을 PR 브랜치 스펙(7d198317) 기준으로 시작. #955 머지 · 재결속 · 승인은 #954 정리 뒤 | 사용자 「코드부터 해 · 이전 작업도 지금 작업도 내가 하고 있어」 |
| 2026-11-20 | **시안(designer P4) 없이 코드로** — mobile 이 지금 앱 컴포넌트 + DAY 웹 배치 · 글자를 따라 만들고, 시뮬레이터 캡처로 사용자 확인 · 지적은 모아 한 번에(OQ-A52 · A54 = 웹 참고로 닫음) | 사용자 「새로 만드는 건 거의 없잖아 · 웹 참고해도 되고」 |
| 2026-11-20 | **바로 시작(U-18) 화면** = 룸 상세 [의사 호출] 옆에 [바로 시작] · 누르면 의사 호출처럼 드로어(`app/lib/ui/doctor_picker.dart` 시트 — 시술 체크 · [전체 선택] 그대로 · 원장 고르기 단계 없음) → [바로 시작 · N건](웹 액션바 글자) · 체크 가능 줄 = 서버 `canQuickStart` 값(OQ-A54 바로 시작 몫 닫음 · 스펙엔 다음 planner 때 반영) | 사용자 「의사 호출처럼 드로어 열리면 되는 거 아니야」 |
| 2026-11-20 | 통역 동시 상한 **3**(`DAY_INTERPRET_MAX_SESSIONS=3` · dev · prod `deploy/config/<env>.env`) — Soniox 조직 TTS 3 에 맞춤(I-1 닫음). 한도 상향은 사용자가 Soniox 에서 · 늘면 다시 올림 | 사용자 「3개로 해 · 내가 소니옥스 가서 늘려야 해」 |
| 2026-11-20 | `/api/auth/device` 는 client=web 이면 400 `invalid_request`(SPEC-001 §3 「JSON /api/auth/* 앱 전용」) · `taut.toml` 에 `adapters/fcm.py` 한 줄 허용 | 코디(F1 질문) |
| 2026-11-20 | 통역 기능이 바뀐 만큼 **통역 화면 글자도 바꾼다** — 원천 = 통키 56e43a0 화면 글자(같은 뜻) · 원천 없는 건 사용자에게 | 사용자 「문구 같은 거 기능이 좀 바뀌었잖아」 |
| 2026-11-20 | 푸시 묶음 = 새 칸 없음 · iOS `apns-collapse-id`=callId · Android 알림 tag = data.callId | 코디(고침 1 질문) |
| 2026-11-20 | **배포 안 함(지금)** — 다른 세션(`day-cc-mig`)에 DB 마이그레이션이 쌓여 있음. 코드 · 검수까지만 · dev/prod 배포 · 앱 빌드 제출은 그쪽 정리 뒤 | 사용자 「배포는 안 할 거야」 |
| 2026-11-20 | 글자 3: ① 통역 재생 중 안내 「번역 음성이 나오는 동안은 듣지 않아요」 지움 ② 「번역 읽는 중」 그대로 ③ 대리 수락 창 「호출할 시술 · N개」 그대로 | 사용자 「추천으로 가자」 |
| 2026-11-20 | 코드 브랜치 `kknaksss/day-mobile-v2` push OK(별도 브랜치 · PR · 머지 없음) · 로컬 시뮬레이터 시험은 대기 | 사용자 |
| 2026-11-20 | dev 가 움직임(f724b149 · day-cc-mig #265 · 0012_kos_keys) → 우리 브랜치 rebase · migration 0013 · 0014 → **dev 에 스쿼시 머지** → dev 자동 배포(migration 자동) → TestFlight DAY Dev 로 확인 | 사용자 「우리 것도 스쿼시 머지 하자 · dev 에」 |
| 2026-11-22 | 스펙(mediness#955) · 프로필 마감은 **대기** — 다른 세션 작업이 마무리되면 mediness main · profile main 이 움직인다 → 그 뒤 코드처럼 새 main 위로 rebase(#955 는 #954 와 spec-000 · log.md 겹침) → 문장 정리 3 → 머지 → Delivery #262 · #263 재결속 · 승인 → 프로필 아카이브 · 회고 | 사용자 「일단 대기 · 이전 작업 마무리하면 main 들이 움직일 거라서」 |
| 2026-11-20 | 출시 방법 = DAY Dev 앱(dev 서버)으로 먼저 내고 실기기 통과하면 같은 코드를 prod 설정(정식 DAY)으로 빌드해 낸다 | 사용자 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_24f45b68-0ac5-4802-b3e3-f9759c7d1fc9` | `task_997b04d27621` | `ctx_4a9a0f9c21ec` | `day-mobile-v2-spec-brief.md` | 완료(spec-report.md · Delivery #262 · #263) · 터미널 유지(검수 수정용) |
| reviewer_doc | `term_dd83abfd-70f3-4748-8a2b-096d8c135407` | `task_caa2a16818da` | `ctx_2f2bee16e8ce` | `day-mobile-v2-review-doc-brief.md` | 1차 FAIL(F5 · W17) · 터미널 유지(2차 검수용) |
| planner | `term_24f45b68-0ac5-4802-b3e3-f9759c7d1fc9` | `task_aa192895f959` | `ctx_c1a62784e1db` | `spec-2-instructions.md` | 2차 완료(spec-2-report.md) · 터미널 유지 |
| reviewer_doc | `term_dd83abfd-70f3-4748-8a2b-096d8c135407` | `task_eb19ddf308d2` | `ctx_a401af9df0f0` | `review-doc-2-instructions.md` | 2차 WARN(R-1~R-6) · 터미널 유지 |
| planner | `term_24f45b68-0ac5-4802-b3e3-f9759c7d1fc9` | `task_38743a63b8dc` | `ctx_f402edda53a1` | `spec-3-instructions.md` | 3차 완료(spec-3-report.md) · 터미널 유지 |
| reviewer_doc | `term_dd83abfd-70f3-4748-8a2b-096d8c135407` | `task_3e50c4b22d55` | `ctx_5a628b695014` | `review-doc-3-instructions.md` | 3차 WARN(N-1 · N-2 잔재) · 사용자 결정 남은 것 0 |
| planner | `term_24f45b68-0ac5-4802-b3e3-f9759c7d1fc9` | `task_02299a2166bb` | `ctx_ba5e78f1f937` | `spec-4-instructions.md` | 4차 완료 |
| planner | `term_24f45b68-0ac5-4802-b3e3-f9759c7d1fc9` | `task_0ee28fa3f4a7` | `ctx_1bfd49a652b9` | backend | `term_569ff46d-a71f-4df7-af39-cf8bec549a2e` | `task_bbe4221250f9` | `ctx_68995ec16323` | `be-p2-instructions.md`(브리프 day-mobile-v2-be-brief.md) | P1 · P2 · P3 · F1(87cec04d) 완료 · 고침 1 · 고침 2 완료(전체 2076) · 대기 |
| mobile | `term_bf75bf2c-9a7d-4d30-a288-34520744e855` | `task_d7a154294d1f` | `ctx_c7faed6ff069` | `mobile-p5-instructions.md` | M1 · P5 · M2 · M3(ecea81d4) 완료 · M2 고침(841454c4) · M4 · F2(b87925c6) 완료 · 푸시 고침 완료(test 415) · 대기 |
| reviewer | `term_9ee0169f-c92f-48ee-a610-968d9bbb5039` | `task_27fd8daee8c3` | `ctx_730565303878` | `review-code-push-instructions.md` | 앱 푸시 PASS(WARN 6) · release |
| reviewer | `term_569ef5d0-e0ef-4827-932f-463b98314b6f` | `task_94c4f82fc24f` | `ctx_463af92780b5` | `review-code-f1-instructions.md` | F1 조건부 PASS(FAIL 1 비밀 배선 · WARN 3) → 고침 1 에 더함 · release |
| reviewer | `term_a7a61882-2c73-4169-9f84-fdad5886e859` | `task_3b84b0d8ed7c` | `ctx_83726cc19a54` | `review-code-p3-instructions.md` | P3 PASS(WARN 4 · review-code-p3-report) · release |
| reviewer | `term_abc3762b-2dbf-4b6e-94c4-8df26c792ab2` | `task_6a58b1257d37` | `ctx_d395a2fd5a58` | `review-code-m2-instructions.md` | M2 FAIL 1 · WARN 3(review-code-m2-report) · release |
| reviewer | `term_a680049d-f134-4000-ab1d-9b9723544cde` | `task_7d86bce7ac93` | `ctx_21424f5911e1` | `review-code-p2-instructions.md` | P2 PASS(WARN 4 · review-code-p2-report) · release |
| reviewer | `term_49dda010-189b-4822-8c6f-1442e66746b5` | `task_6cc73714f09c` | `ctx_63503b548b9e` | `review-code-p5-instructions.md` | P5 PASS(WARN 1 = 안내 문구 · INFO 3 실기기) · release |
| reviewer | `term_703f01cd-c59e-4d75-b61c-00432e035a39` | `task_6a03f5721cb4` | `ctx_590155637f07` | `review-code-p1-instructions.md` | P1 WARN(FAIL 0 · review-code-p1-report) · release |
| reviewer | `term_d4b68fc2-4069-4438-ad75-6fa2d155033b` | `task_1f970c4aa3ba` | `ctx_b8260448f6d0` | `day-mobile-v2-review-brief.md` | M1 PASS(WARN 4 · review-code-m1-report) · release |
| planner(재결속) | — | `task_0ee28fa3f4a7` | `ctx_1bfd49a652b9` | `spec-5-instructions.md` | 막힘 — harness 가 baseline = origin/main 만 받음(7d198317 거절 · rc=2) · 요청 준비됨(spec-5-report) · 터미널 유지 |
| researcher | (release) | `task_89dac2a586e8` | `ctx_b469d176839c` | `day-mobile-v2-research-brief.md` | 완료 · 터미널 release |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/955 (`7d198317` · OPEN)
- **dev 배포 성공**(run 44708143917 attempt 2 · 1차는 체크 중 취소됨 — 취소 주체 미확인 · 코디 cancel 은 거절돼 실행 안 됨) · alembic `0014_device_platform_android (head)` · api healthy · worker · scheduler up · FCM 키 실림 · 상한 3 · FCM 허용 앱 dev · /login 200
- **DAY Dev 0.2.0 업로드(11-20)**: iOS (4) TestFlight VALID · 내부 테스트 · Android internal vc4 completed · AAB 사본 `~/.config/day/android/out/DAY-Dev-0.2.0-4.aab` · 서버 주소 dev 만 · 정식 앱 0
- dev Key Vault `day-dev-fcm-service-account` 넣음(11-20 · ssh -D day-vm 경유 REST · 200)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/266 → dev **스쿼시 머지 `5ece25ea`**(11-20 · rebase HEAD 8a76c35b · migration 0013 · 0014)
- code(이전): 브랜치 `kknaksss/day-mobile-v2`(로컬 커밋 · push 전) — `e7853088` M1 app · `a7868dc6` P1 통역 · `bb8412de` P5 앱 통역 · `e96b0718` P2 API · `b91d2fca` M2 앱 · `bd93b559` 통역 시험 · 상한 3 · `ecea81d4` M3 앱 알림 · `841454c4` M2 고침 · `d7055af4` M4 캡처 · `c22b56bc` 고침 1 · `b87925c6` F2 Android 푸시 · `999f2377` 고침 2 · `dba35bbd` 푸시 고침 · `921d88cd` M5 안내 줄 지움(끝 · origin/dev 위 16커밋 · **origin 에 push 됨 11-20 · PR 없음**) · `87cec04d` F1 FCM(migration 0013 · Key Vault `DAY_FCM_SERVICE_ACCOUNT` 넣을 것) · `9162ee18` P3 알림(migration 0012 · 새 worker 태스크 call_cancel_push — 배포 때 worker 같이)
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-20` M1(app) · P1(통역) 완료 · 커밋 분리 · P1 검수 · P2 · P5 동시 발주
- `2026-11-20` 스펙 검수 1차 FAIL → 2차 WARN → 3차 WARN → 4차 수정 · 코디 grep 확인 · PR mediness#955
- `2026-11-20` planner 완료(SPEC 000 · 001⑩ · 002㉕ · 003⑲ · 005 · mobile-deployment · Delivery #262 · #263 v1 baseline ccede286) · reviewer_doc 발주
- `2026-11-20` 코드 워크트리 `CENTURION_DAY/day-mobile-v2`(origin/dev 844eace4) · planner 발주
- `2026-11-20` researcher 조사 발주(orca 새 방식 — run-create → worker-start --terminal)
- `2026-11-20` 세팅(new-work.sh · 코드 base origin/dev `844eace4` 확인) · 범위 3건 기록

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
