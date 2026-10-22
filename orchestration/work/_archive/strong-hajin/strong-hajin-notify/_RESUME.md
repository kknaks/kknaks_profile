# 재개 노트 — strong-hajin-notify (strong-hajin)

**지금**: 운영 반영 2판 — #19 `baf7daf`(「메시지」 세 곳 · 전체화면 빈 공간: WKWebView 요소 전체화면 끔 + 셸 높이 100% 사슬) · 인프라 #15 · Argo Synced/Healthy · 운영 CSS 반영 확인 · medi-ax dmg 공증 Accepted → `~/Downloads/medi-ax_0.0.1_arm64_baf7daf.dmg` · **사용자 앱 확인 대기**(전체화면 왕복 · 「메시지」 · 다른 화면 높이) → 마감(archive-work.sh · 회고 · 개념 · SH-IMP-021 커밋)
**다음**: WP1-BE → reviewer 코드 검수 → 수정 → 코디 검증 → WP1-FE → WP2-BE → WP3-FE → WP4-SHELL(P0 결과로) → **전체 테스트 1회(make verify)** → 사용자 E2E(앱) → 2루프 → 운영(확인 받고)

세팅: `scripts/new-work.sh strong-hajin strong-hajin-notify --workers backend,frontend` · 설정 SSOT `config/projects/strong-hajin.json`
코디handle: `term_aa9fb9af-eed1-45ee-baad-95e52082321d` (2026-10-07 — 한때 `term_3f9a08f5…` 로 바뀌었다가 env 값으로 돌아왔다. `orca terminal list` 에서 beluga 워크트리 · 제목 「Main pull」 · **워커를 띄울 때마다 list 로 확인**)

## 워크트리

- `docs`(코디): `/Users/kknaks/orca/workspaces/kknaks_profile/beluga` (branch `kknaksss/beluga`)
- `code`: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` (branch `kknaksss/strong-hajin-notify`, base `origin/main` `d2a06fa` → PR `main`)

## 1. 지금

- [ ] 사용자 답: 알림 사건 목록 · 메시지 알림 범위 · 시각 기반 · 받는 경로 · 사이드바 클릭 대상 · 수신함과의 관계
- [ ] 답 뒤 BASE-009(writer · 코디 워크트리 탑승) → DEC-010
- [!] 사용자는 **데스크톱 앱만** 쓴다 — 완료 판정은 앱 실물

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-07 | 알림은 **나와 관련된 것만** — 업무 상태 변경 · 메일 · 슬랙 · 카톡 등 | 사용자 |
| 2026-10-07 | 시스템 알림 = **A안**: 앱이 켜져 있을 때만. 웹이 지금 있는 실시간 연결로 받아 Tauri(Rust)에 넘겨 OS 알림. 서버→기기 푸시 없음 | 사용자 |
| 2026-10-07 | **설정 알림 메뉴 · 사이드바 알림** 이번 범위 (DEC-008 D-37 「범위 밖」을 이번 작업이 연다) | 사용자 |
| 2026-10-07 | 조사 먼저 — BE·FE read-only 조사로 지금 알림이 쌓이는 자리·추가할 자리·렌더링·시스템 알림 길을 확정 | 사용자 지시 |
| 2026-10-07 | 알림 사건 네 묶음 다 한다 — 업무 상태 변경 · 메일·슬랙·카톡 수신 · 회의(초대·변경·취소·회의록 완료/실패·공유) · 연동 끊김·수집 실패 | 사용자(조사 표 보고) |
| 2026-10-07 | 사이드바 알림 = **알림 목록**을 보는 자리. **시안 먼저** 만든다 | 사용자 |
| 2026-10-07 | 실시간은 **하나로 모은다 · SSE** — 사용자 사건 채널 하나(지금 inbox WS 대체)에 알림+메시지함 사건. 회의 WS 는 별개 유지(코디 제안) | 사용자 제안 · 코디 동의 |
| 2026-10-07 | 설정 알림 = 테마 **업무 · 메시지 · 회의** · 전체 on/off · 테마별 on/off · 항목 체크박스 | 사용자 |
| 2026-10-07 | 같은 사건이라도 **받는 사람의 관계(To·CC·담당·요청자·멘션 등)에 따라 알림이 다르다** — DEC 에 사건×관계 표로 정한다 · 필요한 칸·게시 길은 새로 낸다 | 사용자 |
| 2026-10-08 | 사이드바 알림 = **점만**(숫자 배지 없음 · design-change-1 미결 1 닫힘) | 사용자 |
| 2026-10-08 | 사이드바 **메시지함도 점**을 켠다 — 알림·메시지함 둘 다 점(숫자 없음). 화면 안 숫자는 지금대로 | 사용자 |
| 2026-10-08 | 기본값(코디 통보 · design-change-1 미결 2~7): 끄면 목록에도 안 쌓임(생성 때 거름) · 관계 둘 이상이면 담당>요청자>참조 하나 · 카톡 설정 항목 하나(꼬리표로만 1:1/단체방) · 연동 끊김 = 메시지 테마·「내 연동」 · 슬랙 채널 새 메시지 = 방별로 안 읽은 동안 한 줄 합침 ~~· 보관 90일~~ (10-08 사용자: 보관 기간 고려 안 함) | 코디 기본값 → 10-08 사용자 확정 |
| 2026-10-08 | 설정 「메시지」 테마 항목 = **메일 · 슬랙 · 카톡 셋만**(받는 사람/참조·DM/멘션/채널로 나누지 않음). 연동 끊김은 그 채널 항목에 딸림(코디 추천) | 사용자 · 코디 추천 |
| 2026-10-08 | **알림 보관 기간은 이번에 고려하지 않는다**(지우는 규칙 없음) | 사용자 |
| 2026-10-08 | 나머지 미결은 **코디 추천안 확정** — 끄면 목록에도 안 쌓임 · 관계 둘 이상이면 담당>요청자>참조 · 슬랙 채널은 방별 합침 · 연동 끊김 꼬리표 「내 연동」 | 사용자 |
| 2026-10-08 | DEC-010 OQ-1001~1015 **코디 추천안 확정**(1010 제외) — 1001 수신함·알림 둘 다(읽음 따로, 기존 2종 흡수) · 1002 CC 는 댓글만(목데이터 a07 고침) · 1003 결재자 안 알림 · 1004 담당 수락·거절→배정자 answer · 밀려난 담당 assign · 제안 철회 없음 · 1005 철회·취소·재개→상대 change · 완료 승인 없음 · 1006 표대로 + 취소 제안 change · 제안 응답→제안자 answer · 1007 기한 변경 담당만 · 이동 없음 · 1008 To/CC 없는 메일도 알림(꼬리표 「메일」) · 1009 그룹 DM=DM · 멘션 따로 한 줄 · DM 안 합침 · 1011 고른 상태까지 이동 · 1012 수집기 꺼짐 안 알림 · 방 접근 잃음 알림 · 1013 새로 든 사람 invite · 빠진 사람 change · 1014 참석자도 받음 · 1015 「공유받음」 꼬리표 | 사용자(「응 가자」) |
| 2026-10-08 | OQ-1010 운영 확인 — 카톡 raw 에 「내가 보낸」 재료 없음 · 슬랙 author 100% 이름 덮임(판정은 raw.user) → 사용자 결정 대기 | `prod-check-1.md` |
| 2026-10-08 | OQ-1010 = **A 수집기를 고친다** — Mac 카톡 수집기가 「내가 보냄」 표지를 올린다(로컬 DB 에 그 값이 있는지 구현 전 조사) · 슬랙은 `raw.user` 로 판정 · 슬랙 안 읽음 「내 줄 빼기」 버그(author 100% 이름 덮임)도 이번에 고친다 | 사용자 · `prod-check-1.md` |
| 2026-10-08 | **기존 카톡 메시지 백필** — 표지 없는 기존 행(운영 116건 · 본인 14건)을 「내가 보냄」 으로 채운다. 방식은 일회성 수동 마이그레이션(본인 이름은 코드·문서에 박지 않고 실행 인자로) — 수집기 재전송으로 메울 수 있으면 그쪽(조사 뒤 SPEC 에서 택일) | 사용자 지시 · 코디 추천 |
| 2026-10-08 | OQ-1016 꼬리표 우선순위 = **담당 > 요청자 > 배정자 > 참조** · D-28 원칙 ① 「내가 한 행동은 나에게 알리지 않는다」 **확정** · 설정 업무 `answer` = 「내가 보낸 요청·배정·제안에 답이 왔을 때」 / 「받는 사람이 수락·거절하거나 제안에 답하면」 | 사용자(추천안) |
| 2026-10-08 | 검수(FAIL 3·WARN 11) 뒤 사용자 결정(추천안): ① 알림 목록 = 스크롤 끝 **자동 이어 불러오기**(단추 없음 · DEC 「더 불러오기 범위 밖」 뒤집음) ② **메시지함에서 읽으면 그 메시지 알림도 읽음** ③ 회의 **공개 전환은 「공유받음」 알림 안 냄**(특정 사람 공유만) ④ OS 알림 줄이기 — 그 화면을 보고 있으면 OS 알림 생략(목록엔 쌓음) · 슬랙 채널 합친 줄은 처음 생길 때만 · 몰리면 「새 알림 N건」 한 번 · [모두 읽음] = 시안대로 전부 | 사용자(「응 추천으로 가자」) · `review-spec-work-report.md` |
| 2026-10-08 | **코드 구현까지 끝까지 간다** — 발주 → 검수 → 수정 루프를 코디가 묻지 않고 돈다. 멈추는 곳: P0 카톡 대조(사용자 Mac 데이터) 결과 · 1루프 E2E(앱) · 운영 반영 직전 | 사용자 |
| 2026-10-08 | **테스트는 Phase 마다 해당 부분만** · 전체 테스트(`make verify`)는 **E2E 직전에 한 번만** | 사용자 |
| 2026-10-08 | 외부 발신자(메일·슬랙·카톡) 이름에는 「님」 을 붙이지 않는다 — 서버가 사람/단체를 가르지 못한다 · 회원만 「이름님」(fe-wp3 §6-4) | 코디 기본값 — E2E 에서 뒤집기 가능 |
| 2026-10-08 | P0 처분(추천안): **OQ-1108 = ④ macOS 는 UNUserNotificationCenter 를 objc2 로 셸이 직접**(클릭 → 기존 셸→웹 사건 · 진짜 권한 프롬프트·거부 판정) · Windows 는 공식 `tauri-plugin-notification`(실기 pending) · **tauri 2.12 로 올림** · OS 알림 실측은 **서명 dmg 만**(dev 는 번들 id 없어 대상 아님) · **OQ-K01 닫힘** = `authorId == NTChatContext.userId`(운영 16=16 · 1:1 로컬 보조 확인) | 사용자(「응 다 구현하라고」) · `p0-report.md` |
| 2026-10-08 | W17·W24·W30(사건×관계 「알림」 행)은 지금 권한상 행위자=받는 사람이라 늘 0줄 — **코드 자리는 남기고 권한은 넓히지 않는다** · `actor_member_id` NOT NULL 은 이번에 풀지 않는다 · 코드 레포 `docs/domain-model.md`·`unified-operations.md` 문구는 다음 backend 손질에 | 코디 판단 — `be-wp2-report.md` §2·§6 |
| 2026-10-08 | 사이드바 머리 `titleEnd` 슬롯 신설 받아들임(SPEC-011 §2.1 「안 읽음 N」) · E2E 체크리스트의 기한 변경(W17)·취소(W24)·재개(W30)은 「지금 권한상 알림 안 섬」 으로 손질 | 코디 판단 — `review-wp2-wp3-report.md` W-6 · §8 ⑦ |
| 2026-10-08 | WP4 검수 처분: W-1 창 없을 때 배너 클릭 = ① 창을 만들고(트레이 「열기」 길) 웹 준비 뒤 사건 · W-3 Windows 컴파일 미확인 → 확인 전 **Windows 배포 막음** · W-4 `target:null` OS 클릭 = 목록 클릭과 같게 · W-2 tauri 2.12 회귀는 dmg 실측(트레이·닫기·내려받기·하위 프레임·외부 링크·절전 방지·마이크) · W-5 권한 묻기 범위 · W-6 앱 origin 아닐 때 클릭 버림 → 2루프 후보 | 코디 판단 — `review-wp4-report.md` |
| 2026-10-10 | **사용자 E2E 통과** — 2루프 지적 없음(슬랙 알림 안 옴 = 내가 보낸 줄 · 정상 확인) | 사용자 |
| 2026-10-10 | ~~화면에 보이는 「메시지함」 을 전부 「메시지」 로~~ → **세 곳만**: 사이드바 항목 · 화면 머리 제목 · 목록 칸 제목. 나머지 문구는 「메시지함」 그대로 | 사용자(최종 선택) |
| 2026-10-10 | **`from_me` 백필은 하지 않는다** — 사용자가 운영 DB 를 다 날릴 예정(셈 apply=0 만 했고 바뀐 것 없음 · 카톡 16/3방 · 슬랙 2097 · 메일 0). DB 를 지우는 일은 사용자가 한다 | 사용자 |
| 2026-10-07 | 기본값(코디 통보): 받는 경로 = 앱만(메일·슬랙 DM 범위 밖) · 기한 하루 전·일일 요약 범위 밖(스케줄러 없음) · 연동 끊김은 「메시지」 테마 · 창 닫으면 끊김(A안 그대로) | 코디 기본값 — 사용자 뒤집기 가능 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_db0bdde7-4ed1-448a-a562-d845c8c32012` | `task_6ed3bf250024` | `ctx_4e312ad0164e` | `strong-hajin-notify-be-brief.md` | 완료 |
| frontend | `term_d858ee9f-73e0-4703-9383-11065edb5fe3` | `task_5d5fdd305638` | `ctx_9fbcb22c9441` | `strong-hajin-notify-fe-brief.md` | 완료 |
| architect | `term_77c4741f-985c-4917-9e9b-60eda18a1b9d` | `task_fdcea1e115a0` | `ctx_a1b9f4724272` | `strong-hajin-notify-arch-design-brief.md` (알림 시안 둘 · 코디 워크트리 탑승) + `design-fix1-instructions.md` · `design-fix2-instructions.md` · `design-fix3-instructions.md` | 완료 — design-change-1~4.md |
| writer | `term_f8edf263-f144-49a1-9adc-25b1d7a4877f` | `task_205352d86c70` | `ctx_2a1a1534c934` | `strong-hajin-notify-write-brief.md` (BASE-009 · DEC-010) + `write-fix1-instructions.md` · `write-fix2-instructions.md` | 완료(수정 2) |
| writer | `term_f8edf263-f144-49a1-9adc-25b1d7a4877f` | `task_b682145e7758` | `ctx_fa770908c723` | `strong-hajin-notify-write2-brief.md` (SPEC-011 · SPEC-006/008/009 개정 · WORK-013) | 완료 |
| backend | `term_db0bdde7-4ed1-448a-a562-d845c8c32012` | `task_c572dfd1af26` | `ctx_fb564a8e5c35` | `strong-hajin-notify-be-impl-brief.md` (WP1-BE) | 완료 — 검수 WARN 4 |
| backend | `term_db0bdde7-4ed1-448a-a562-d845c8c32012` | `task_bb01b35b494b` | `ctx_c0b15977f94f` | `be-wp1fix-wp2-instructions.md` (WP1 손질 + WP2-BE) | 완료 — 검수 중 |
| frontend | `term_d858ee9f-73e0-4703-9383-11065edb5fe3` | `task_3d3ac83c8f56` | `ctx_e22253f41284` | `strong-hajin-notify-p0-brief.md` (P0 조사) | 완료 |
| frontend | `term_d858ee9f-73e0-4703-9383-11065edb5fe3` | `task_a801008c7bf0` | `ctx_f713eb1e9f99` | `strong-hajin-notify-fe-impl-brief.md` (WP1-FE) | 완료 — 검수 PASS |
| frontend | `term_d858ee9f-73e0-4703-9383-11065edb5fe3` | (preamble) | (preamble) | `fe-wp3-instructions.md` (WP3-FE) | 완료 — 검수 FAIL 2 |
| frontend | `term_d858ee9f-73e0-4703-9383-11065edb5fe3` | `task_68d69aab9520` | `ctx_5d9f88d09c44` | `fe-wp4-instructions.md` (WP4-SHELL) | 완료 — 검수 대기 |
| frontend | `term_d858ee9f-73e0-4703-9383-11065edb5fe3` | `task_938d817a3245` | `ctx_74a6287d6f7f` | `fe-wp3fix-instructions.md` | 진행 |
| backend | `term_db0bdde7-4ed1-448a-a562-d845c8c32012` | `task_c44bd3c65d13` | `ctx_24138ad3fab4` | `be-wp2fix-instructions.md` | 진행 |
| reviewer | `term_f53dd780-dc2f-44fa-8ced-c5c9fdf7348c` | `task_532b22ab5c34` | `ctx_bbfde9e783b2` | `strong-hajin-notify-review-brief.md` (SPEC·WORK 검수) | 완료 — FAIL 3 · WARN 11 |

## 4. 산출물

- 리포트: `be-survey-report.md` · `fe-survey-report.md` (완료 · 코디 표본 확인: WT:2116 · api.ts:726 호출 0 · SideNav disabled · Cargo 알림 의존 0 · 코드 트리 clean)

## 5. 이력 (최신이 위)

- `2026-10-10` 운영 반영 2판 — #19 · 인프라 #15 · dmg baf7daf · 개선 목록 SH-IMP-021(캘린더 공휴일) 추가
- `2026-10-08` 운영 반영 — #18 · #88 · 인프라 #14 머지 · SQL ① · 이미지 · Argo · v2 재실행 · 인덱스 · dmg 공증 · 전체 1회(BE 통과 · FE 날짜 기존 8 · `flaky-baseline-evidence.md`)
- `2026-10-08` 구현: WP1-BE 검수 WARN 4 · WP1-FE 검수 PASS(사람 눈 ① 옛 back 이 떠 있으면 실시간 멈춘 듯 — E2E 전 스택 재시작) · P0 완료
- `2026-10-08` 시안 수정 1(메시지 항목 셋) 완료 · writer BASE-009·DEC-010 발주
- `2026-10-07` 알림 시안 완료 — `Alerts.html`(새) · 설정 알림(받는 경로 걷음·전체/테마 스위치·항목 20) · 미결 8
- `2026-10-07` BE·FE 조사 완료 — 알림 생성 1곳(요청 발송·수락) · 화면 미사용 · 스트림에 업무 사건 없음 · 게시는 API·external_worker 뿐 · Tauri 알림 수단 0
- `2026-10-07` new-work.sh 로 작업 단위 생성 · BE·FE 알림 조사 발주
