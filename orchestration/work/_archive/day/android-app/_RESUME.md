
# 재개 노트 — android-app (day)

**지금**: 2026-11-15 프로덕션 vc3 심사 중 · PR #253 머지 준비 끝(사용자 머지) — 아래 옛 줄은 이력 참고 · 정식 AAB 완료(~/.config/day/android/out/DAY-0.1.0-1.aab · day.medisolveai · prod · vc1 · 코디 지문 확인) → **사용자 비공개 테스트 손 업로드 대기**
**다음**: #253 머지 → mobile 3판 AND-5(업로드 키 keytool · release AAB 서명) → 사용자 Play Console 손 단계(앱 만들기 · 첫 AAB · 콘텐츠 · 테스터 · 서비스 계정) → AND-7 API 스크립트 · 둘째 빌드 · 실기기 A6(통역 음성 입력 포함)

세팅: `scripts/new-work.sh day android-app` · 설정 SSOT `config/projects/day.json`
코디handle: `term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec` (branch `kknaksss/android-app-spec`, base `origin/main` → PR `main`)
- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app` (branch `kknaksss/android-app`, base `origin/dev` `0106654e` → PR `dev`)
- 인수인계(범위 정본): `orchestration/work/_archive/day/fix-web/android-app-handoff.md`

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] planner — spec-report.md · 스펙 5파일 미커밋 · Delivery #251 v1(digest 2a25e08e · 승인 X) · lint 코디 확인 exit 0
- [~] reviewer_doc — review-doc-1-report.md
- [ ] reviewer_doc → 스펙 PR → Delivery 승인(사용자)
- [ ] AND-7 발주 때 같이: review-code-2 W-1(app/.gitignore 에 *.jks · *.keystore · *.p12 · *.aab · upload-key.properties)
- [ ] mobile — app/android · day/session Kotlin · push/video 스텁 · 권한 · README → reviewer → 에뮬레이터 dev 로그인 실물 e2e
- [ ] 사용자 예약현황 숨김(app-review-re1 · 다른 브랜치)은 **기다리지 않는다**(사용자 11-13). 머지되면 PR 전 rebase(겹침 app/README.md 뿐)
- [!] 워커는 사용자 에뮬레이터 · 프로세스 끄지 않는다 · iOS 무변경(심사 중)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-12 | 범위 = 로컬 에뮬레이터 · dev 로그인 → 화면 확인 · session 구현 · push/video 스텁 · id `day.medisolveai.dev`/`DAY Dev` · iOS 무변경 · FCM/Play 나중 | 인수인계 §2(사용자) |
| 2026-11-12 | 스펙(mobile-deployment 등)에도 반영 — planner → reviewer_doc → 스펙 PR 뒤 코드 | 사용자(이 세션) |
| 2026-11-13 | **Android 통역도 범위 안**(완료 조건) — 마이크 권한 · 녹음 · 결과 · 소리 출력. Dart 변경 필요하면 코디에게 | 사용자 「안드로이드도 통역 넣어야지」 |
| 2026-11-13 | Delivery 승인 경로 (b) 스펙 PR 머지 → v2 재결속(target_specs +SPEC-004) → 승인 · Dart 무변경은 이번 범위 한정(W-2) | 코디 기본값(review-doc-1 U-1 · U-3) |
| 2026-11-13 | **범위 확장: 올릴 수 있으면 Play 에 올린다** · 개발 앱(day.medisolveai.dev)만 Play 내부 테스트 · 정식 앱 id/배포 [미결] · 회사 명의 Play Console 권한 받음 | 사용자 |
| 2026-11-13 | Play 앱 서명 + 업로드 키 로컬(~/.config/day/android/) · 백업 위치 미정 · 업로드 = Play Developer API 서비스 계정(첫 AAB 는 사용자 수동) | 사용자(추천안) · config day.json google_play |
| 2026-11-13 | Play 막혀도 로컬(A1~A5) 끝나면 코드 PR 먼저 머지 · Play 설치 확인 = **실제 Android 폰** · 업로드 키 = 코드 워커가 keytool 로 ~/.config/day/android/(백업은 사용자) · risk L3 | 사용자 · review-doc-3 U-1~U-3 → Delivery v2 에 반영 |
| 2026-11-13 | **예약현황 탭 숨김(앱 · 스펙) = 사용자가 직접**(이 작업 범위 밖 · 코디 손대지 않음). 스펙은 #940 머지 뒤 개정 ⑮ 권장 · 앱 dev 머지 알림 받으면 mobile 발주 전 android-app 워크트리를 최신 dev 로 | 사용자 |
| 2026-11-13 | #940 코디 머지 · Delivery v2 **승인 위임**(「그냥 승인하고 해 같이 해야지」) → planner 가 receipt 적용 | 사용자 |
| 2026-11-13 | dev 데모 테스트 계정 자격 = `~/.config/day/dev-login.local.json`(600 · 값은 레포 · 리포트 금지) — 워커 로그인용 | 사용자 |
| 2026-11-13 | dev 데모 테스트 계정 자격 = `~/.config/day/dev-login.local.json`(600 · 값은 레포 · 리포트 금지) — 워커 로그인용 | 사용자 |
| 2026-11-13 | 통역 **음성 입력**(말하기 → 자막 → 번역 음성)은 에뮬레이터가 아니라 **Play 내부 테스트 실기기(A6)** 에서 확인 — 에뮬레이터는 권한 · 연결 · 듣는 중 · TTS 까지(맥 호스트 마이크 권한 사유). 마감 spec-sync 때 A-48/A-49 반영 | 사용자 |
| 2026-11-13 | 사진 권한(READ_MEDIA_*) 그대로 · Play 업로드 때 막히면 「채팅 최근 사진 줄 = 핵심 기능」 신고 | 사용자(review-code-1 W-2) |
| 2026-11-13 | #253 머지는 나중(사용자) · AND-5~7 은 같은 브랜치에 이어서 · 실기기(Z Fold3) USB 로 release apk(debug 키 서명) 설치해 먼저 확인 — Play 빌드와 서명 달라 나중에 지우고 깔 것 | 사용자 |
| 2026-11-13 | 실기기(Z Fold3) 확인 끝 — 「확인했어」(통역 음성 입력 포함으로 봄) → Play 에 올린다 | 사용자 |
| 2026-11-13 | **정식 Android 앱 = day.medisolveai · DAY · prod · 비공개 테스트**(프로덕션은 나중) · 업로드 키 dev 와 공유 · 사용자가 Play 앱 먼저 만들고 「빌드하고 올리자」 — 스펙(M-4 · M-3 남은 것)은 **뒤따라 반영**(마감 spec-sync 또는 planner) | 사용자 |
| 2026-11-15 | **정식 DAY 프로덕션(공개) 출시 준비 진행** — 「이제 출시 준비도 하면 되나?」 · 빌드 = 비공개 테스트 vc3 승격 · 사용자 Console 손 단계(스크립트는 production 막음 — 의도) · 스펙 M-3 반영은 마감 spec-sync | 사용자 |
| 2026-11-12 | fix-web 마감은 사용자가 다른 세션에서(#130) | 사용자 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58` | `task_50f6c194930e` | `ctx_f9af67fd5e85` | `android-app-spec-brief.md` | 완료 |
| reviewer_doc | `term_ff662177-d76e-437b-af67-574540a68ea3` | `task_ae99419a722b` | `ctx_d4439bc0211c` | `android-app-review-doc-brief.md` | 완료 WARN |
| planner 2 | `term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58` | `task_831a0f2eeb35` | `ctx_3c848e6f4326` | `spec-2-instructions.md` | 완료 |
| reviewer_doc 2 | `term_ff662177-d76e-437b-af67-574540a68ea3` | `task_68714153f7c2` | `ctx_e97098350601` | `review-doc-2-instructions.md` | 완료 PASS |
| planner 3 | `term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58` | `task_5ba5aa89b293` | `ctx_455a64b9a241` | `spec-3-instructions.md` | 완료 |
| reviewer_doc 3 | `term_ff662177-d76e-437b-af67-574540a68ea3` | `task_53ec39aac206` | `ctx_2af725a21ef8` | `review-doc-3-instructions.md` | 완료 WARN 3 |
| planner 4 | `term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58` | `task_53a9bb8a563e` | `ctx_67927add184b` | `spec-4-instructions.md` | 완료 |
| reviewer_doc 4 | `term_ff662177-d76e-437b-af67-574540a68ea3` | — | — | `review-doc-4-instructions.md` | 완료 PASS |
| planner v2 | `term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58` | `task_57257a73c030` | `ctx_db65f4e95646` | `delivery-v2-instructions.md` | 완료(approved) |
| mobile 1 | `term_7110412d-9a63-452f-8dad-75aa43ad8f6e` | `task_ca46b06497f9` | `ctx_37eb0e607479` | `android-app-app-brief.md` | 완료 |
| reviewer 1 | `term_dd8d4e4a-ede4-45b0-bb51-a7ac356c3143` | `task_5729855dd2b3` | `ctx_86dcf3d22d51` | `android-app-review-brief.md` | 완료 WARN |
| mobile 2 | `term_7110412d-9a63-452f-8dad-75aa43ad8f6e` | `task_5d7c8ec71247` | `ctx_9c45dfeeac20` | `app-2-instructions.md` | 완료 |
| mobile 3 | `term_7110412d-9a63-452f-8dad-75aa43ad8f6e` | — | — | `app-3-instructions.md` | 완료 |
| mobile 4 | `term_7110412d-9a63-452f-8dad-75aa43ad8f6e` | — | `ctx_da53a4425b6b` | `app-4-instructions.md` | 완료 |
| reviewer 2 | `term_dd8d4e4a-ede4-45b0-bb51-a7ac356c3143` | — | — | `review-code-2-instructions.md` | 완료 PASS(W-1 낮음 → AND-7 때 app/.gitignore 에 키 · aab 패턴) |
| reviewer 4 | `term_dd8d4e4a-ede4-45b0-bb51-a7ac356c3143` | `task_5bc98134e20b` | `ctx_61ba25c587ee` | `review-code-4-instructions.md` | 완료 PASS |
| planner close 2 | `term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58` | `task_bda159ec9344` | `ctx_a0dbd665c2ba` | `spec-close-2-instructions.md` | 완료 |
| review-doc close | `term_ff662177-d76e-437b-af67-574540a68ea3` | `task_09c4415d6dfb` | `ctx_8d29937814fe` | `review-doc-close-instructions.md` | 완료 WARN 3(W-1 공개 결정 표기 · W-2 업로드 키 주체 · W-3 음성 입력 해석) |
| planner close | `term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58` | `task_9e2c97c5163c` | `ctx_b60d7050eb13` | `spec-close-instructions.md` | 완료(7파일 미커밋 · lint 0 error · #251 conformant) |
| mobile 6 | `term_7110412d-9a63-452f-8dad-75aa43ad8f6e` | `task_59dee9dbe2c7` | `ctx_bb90c45a6766` | `app-6-instructions.md` | 완료(W-1 전수 23 · 4곳 고침 · iOS 픽셀 동일 · W-2/3 · test 355 · DAY Dev internal vc3 출시 · 정식 alpha vc3 dry-run · AAB DAY-0.1.0-3) |
| reviewer 3 | `term_dd8d4e4a-ede4-45b0-bb51-a7ac356c3143` | `task_32ee4c36698e` | `ctx_1e156db1fe3b` | `review-code-3-instructions.md` | 완료 WARN(W-1 중 태블릿 목록 끝 · W-2/W-3 낮음) |
| mobile 5 | `term_7110412d-9a63-452f-8dad-75aa43ad8f6e` | `task_d41afea4fff0` | `ctx_3fc91d28b8e3` | `app-5-instructions.md` | 완료(F1 = 태블릿 채팅 칸 · iOS 픽셀 동일 · play_upload.py · DAY Dev internal vc2 출시 · 정식 alpha dry-run · AAB DAY-0.1.0-2 준비) |

Run: `run_95ce51eb4f07`

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/940
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/253 (AND-1~7 + F1 · 커밋 e13ea876 · fa2f0d9f · 099fe786 · 0120b427)
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-16` review-doc-close WARN 3 → planner close 2 반영 · **mediness#944 squash 머지 `13772db6`** · Delivery #251 마감 댓글 · 닫음 · 다음 = archive-work.sh
- `2026-11-16` 마감 시작(사용자 「아카이브 회고 다 정리 · 문서 · 코드도」) · **#253 squash 머지 `4f8316a7`**(dev) · planner close 발주
- `2026-11-15` 정식 DAY **프로덕션 vc3 심사 제출**(전체 출시 · 대한민국 · 관리형 게시 꺼짐 = 통과 시 자동 공개) · 다음 = 심사 결과 → 마감(PR #253 머지 · spec-sync · archive)
- `2026-11-15` 사용자 실기기 확인 「다 다운 받아서 봤는데 괜찮아서」 — 정식 DAY vc3(비공개 테스트 Play 설치) · F1 해소로 봄 · 테스터 등록 OK · 다음 = 사용자 프로덕션 제출(vc3 승격 · 대한민국)
- `2026-11-15` 정식 DAY alpha vc3 API 업로드 commit ok(사용자 지시 · play_upload.py 첫 정식 사용) · Play 심사 뒤 게시
- `2026-11-15` 코디 커밋 `099fe786`(F1) · `0120b427`(AND-7) · push · PR #253 제목 · 본문 최신화(AND-1~7 + F1) · MERGEABLE/CLEAN · analyze 0 · test 355 · **머지는 사용자** · 정식 alpha vc3 업로드는 Fold 확인 뒤
- `2026-11-14` reviewer 4 PASS · 다음 = 사용자 Fold vc3 확인 → 정식 alpha vc3 실제 업로드 → 코디 커밋 · PR #253 정리
- `2026-11-14` mobile 6 완료 · DAY Dev internal vc3 · reviewer 4 발주 · 사용자 Fold 확인(vc3) 대기
- `2026-11-14` reviewer 3 WARN → mobile 6 발주(정식 alpha 업로드는 vc3 로 · 사용자 Fold 확인도 vc3 로)
- `2026-11-14` mobile 5 완료 · reviewer 3 발주 · 다음 = 사용자 Fold3 에서 DAY Dev vc2 F1 확인 → 정식 alpha vc2 업로드(명령은 app-5-report §C)
- `2026-11-14` mobile 5 발주(F1 + AND-7) · 발주 전 dev 확인 = 움직임 0(ca72fd1d) · 사진 줄 유지 · iOS 재제출 없음 · PR #253 은 전부 끝난 뒤 합침(사용자)
- `2026-11-14` Play API 연결 확인 — 서비스 계정 Play 업로드 전용 서비스 계정 · 키 `~/.config/day/android/play-service-account.json`(600) · 조직 정책 `iam.disableServiceAccountKeyCreation` 을 프로젝트에서 잠깐 재정의해 발급(사용자가 되돌림) · Play 초대(DAY · DAY Dev) · 읽기 시험: DAY alpha vc1 completed · DAY Dev internal vc1 completed · 빌드 2부터 API 업로드 가능(AND-7)
- `2026-11-14` 정식 앱 DAY 비공개 테스트 vc1 **출시됨**(제출 21:43 → 게시 21:52 · 제출 ID 1) · 다음 = 참여 링크로 실기기 설치 · prod 로그인 확인
- `2026-11-14` 정식 앱 DAY 비공개 테스트(Alpha) vc1 **심사 제출**(13 변경 · 관리형 게시 꺼짐 = 통과 시 자동 게시) · 앱 콘텐츠 11/11(로그인=데모 계정 · 광고 없음 · 등급 설문 · 18+ · 데이터 보안(이름·이메일·ID·인앱 메시지·사진·동영상·음성, 공유 없음) · 정부/금융/건강) · 사진·동영상 권한 신고 문구 제출(거절 위험 → 최근 사진 줄 제거) · 스토어 등록정보(iOS 문안 Android 판 · 에셋 `~/.config/day/android/store/` 아이콘 512 · 그래픽 1024×500 · 폰 스샷 4(iOS 스샷 1320×2640 자름 · 알림 화면 제외)) · 카테고리 비즈니스 · 테스터 이메일 목록 medisolveai · 프로덕션 공개 여부 = 사용자 미결(추천: F1 고친 vc2 로)
- `2026-11-13` Play 내부 테스트 실기기 설치 성공(초기 「항목을 찾을 수 없음」 → 반영 지연 · 설치 오류 → 재부팅 뒤 해소)
- `2026-11-13` Play Console 앱 생성(패키지 day.medisolveai.dev · Play 앱 서명 동의) · 내부 테스트 vc1 업로드 · 테스터(사용자) · F1 기록
- `2026-11-13` 실기기 USB 설치(release apk · day.medisolveai.dev)
- `2026-11-13` mobile 2(W-1 · W-4) · 코디 커밋 · rebase ca72fd1d · analyze/test 345/apk · PR #253
- `2026-11-13` mobile 1 완료 · 코디 analyze · 비밀 0 확인 · reviewer 1 발주
- `2026-11-13` Delivery v2 approved · mobile 1판 발주
- `2026-11-13` #940 머지 855bab4f · planner v2 발주
- `2026-11-13` review-doc-4 PASS · #940 커밋 df8a18d9 · PR 본문 갱신
- `2026-11-13` review-doc-3 WARN 3 → planner 4 반영 → review-doc-4 발주 · 사용자 U-1~U-3 결정
- `2026-11-13` planner 3 완료 · review-doc-3 발주
- `2026-11-13` Play 범위 확장 · planner 3 발주 · config google_play 칸
- `2026-11-13` review-doc-2 PASS · 스펙 PR #940
- `2026-11-13` planner 2 완료 · review-doc-2 발주
- `2026-11-13` review-doc-1 WARN 5 · 통역 범위 안 결정 · planner 2회차 발주
- `2026-11-12` planner 완료 · reviewer_doc 발주
- `2026-11-12` 세팅(planner · mobile 워크트리) · planner 브리프

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
