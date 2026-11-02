# 작업 요약 — strong-hajin-notify (strong-hajin)

기간: `2026-10-07` ~ `2026-10-10`
결과: 머지·운영 반영·dmg 공증·사용자 E2E 통과·추가 수정 반영까지 완료 (코드 PR #18 `3321504` · #19 `baf7daf` · 문서 #88 · 인프라 MediSolveAIDev/k8s_infra_mac #14 · #15)

## 1. 무엇을 했나

알림이 없었다 — `notifications` 표와 API 는 있었지만 만드는 자리는 업무 요청 두 종류뿐이었고 화면은 그 API 를 한 번도 부르지 않았다. 실시간은 메시지함 WebSocket 이 화면마다 따로 열렸고 업무 사건은 실리지 않았으며, Tauri 셸에는 OS 알림 수단이 없었다. BE·FE 읽기 전용 조사 → 시안 4판(알림 목록 · 설정 알림 · 사이드바 점 둘) → BASE-009 → DEC-010(결정 41 · 사건 × 관계 68행 사용자 확정) → SPEC-011 · SPEC-006/008/009 개정 · WORK-013 로 내리고, P0(카톡 「내가 보냄」 재료 · 알림 플러그인 클릭 콜백 · 권한/서명)를 먼저 가른 뒤 WP1 사건 채널(SSE) → WP2 알림 생성·설정·판정 → WP3 화면 → WP4 셸 OS 알림을 구현·코드 검수·관련 시험으로 쌓았다. E2E 직전 전체 테스트를 한 번 돌리고 운영(SQL 먼저 · 이미지 · 재실행 · 인덱스)에 반영했으며, 사용자 E2E 를 통과한 뒤 「메시지」 세 곳과 전체화면 빈 공간(tauri 2.12 회귀)을 한 번 더 반영했다.

## 2. 적용한 기술·개념

- **사용자 사건 채널을 SSE 하나로** [[server-sent-events]] · [[websocket]] · [[per-user-fanout]] · [[exponential-backoff]] — 메시지함 사건 넷과 알림을 회원별 스트림 하나(`GET /api/events/stream`)에 싣고, 앱이 로그인 동안 `EventSource` 를 **하나만** 연다.
  - 왜 이걸 골랐나: 알림은 서버 → 화면 한 방향이고 지금 WS 도 올라오는 프레임을 읽고 버렸다. 알림은 저장되므로 사건 id 로 **놓친 것을 다시 줄 수 있다**(WS 에는 커서가 없었다). 회의 WS 는 오디오를 올려야 해서 그대로 뒀다
  - 무엇이 어려웠나: 검수가 세 번 같은 자리를 팠다 — ① `EventSource` 는 비-200 이면 **영구히 닫히고** 상태 코드도, 새 인스턴스의 `Last-Event-ID` 도 없다 → 세션 확인(`/api/auth/me`)으로 「로그인 풀림 / 서버 재시작」 을 가르고 화면이 직접 백오프로 새로 연다(`?last_event_id=`) ② 순번 없이 다시 붙으면 다시 읽기가 빠져 **지금 WS 보다 후퇴** → 「둘째 이후 ready = 다시 읽기」 ③ 순번이 커밋 순서와 다를 때 빠짐 → 겹침 창 60초 + 화면이 id 로 거름. 「10회 멈춤」 이 서버 장애에도 걸려 앱이 조용히 멈추는 것도 r3 가 잡았다(인증 200 + 스트림 실패만 센다)
  - 근거: `backend/src/ax_workspace/entrypoints/http_events.py` · `frontend/src/lib/eventStream.ts` · `W/review-spec-work-report.md` F-1 · `W/review-spec-work-r2-report.md` R-F1 · `W/review-spec-work-r3-report.md`
- **같은 트랜잭션 NOTIFY · 짧은 페이로드** [[listen-notify]] · [[application-event]] — 사건은 저장과 같은 트랜잭션에서 `pg_notify` 로 내고, 페이로드는 id 만 싣고 SSE 를 내는 API 프로세스가 DB 에서 항목을 읽는다. 게시 프로세스가 API · external_worker 둘뿐이라 meeting_worker 가 같은 함수로 내게 길을 냈다(회의록 완료 알림).
  - 근거: `platform/user_events.py` · `W/be-survey-report.md` C-2 · `W/be-wp1-report.md`
- **사건 × 관계 생성기 하나** [[relationship-based-notification]] · [[per-user-fanout]] — 같은 사건이라도 받는 사람의 관계(담당 · 요청자 · 배정자 · 참조 · To/CC · DM · 멘션 · 소유자 · 참석자 · 공유받음)로 알림 여부 · 항목 · 꼬리표가 갈린다. 원칙 셋(내 행동은 안 알림 · 설정 항목이 없으면 안 알림 · 관계 없으면 안 알림)과 우선순위(담당 > 요청자 > 배정자 > 참조)로 68행을 한 생성기에 적고, **만들 때 설정으로 거른다**(끄면 목록에도 안 쌓인다).
  - 왜 이걸 골랐나: 사건마다 흩어 쓰면 원칙이 자리마다 달라진다. 행 id 로 시험을 짜 검수가 「표본이 아니라 전수」 로 대조할 수 있었다
  - 무엇이 어려웠나: W17 · W24 · W30 은 표에 「알림」 인데 지금 권한상 **행위자 = 받는 사람**이라 늘 0줄이었다 — 권한을 넓히지 않고 자리만 남기고 E2E 체크리스트를 고쳤다
  - 근거: `modules/notification_events.py` · `BT/contract/test_notification_rows.py` · DEC-010 사건 × 관계 표
- **「내가 보낸 줄」 판정 재료 = 저장 칸 하나(`from_me`)** [[own-message-flag]] — 슬랙 `raw.user` · 메일 From = 연동 계정 · 카톡 수집기 표지(`authorId == NTChatContext.userId`).
  - 무엇이 어려웠나: 운영 DB 를 보니 **슬랙 `author` 4,041건이 100% 표시 이름으로 덮여** 메시지함 안 읽음의 「내 줄 빼기」 가 한 줄도 동작하지 않던 기존 버그였다. 카톡 raw 에는 「내가 보냄」 재료가 아예 없어 P0 에서 사용자 Mac 의 카톡 로컬 DB 를 읽기 전용 사본으로 열어 운영 16건 = 로컬 16건(방마다 일치)을 확인하고서야 수집기를 고쳤다
  - 근거: `W/prod-check-1.md` · `W/p0-report.md` §1
- **데스크톱 OS 알림 — UNUserNotificationCenter 를 셸이 직접** [[desktop-native-notification]] — 웹이 SSE 로 받아 셸 커맨드 둘(`notify_permission` · `notify_show`)로 넘기고, 클릭은 셸 → 웹 사건으로 그 항목을 고른 상태까지 연다. 앱이 켜져 있을 때만(서버 푸시 없음).
  - 왜 이걸 골랐나: 공식 `tauri-plugin-notification` 2.5.1 은 **데스크톱에서 클릭 응답을 버리고 권한을 늘 「허용」 으로 답한다**(P0 — 소스 근거). 폐기 API(NSUserNotification) · 1인 유지 서드파티 플러그인을 빼고 objc2 로 직접 짰다 — 진짜 권한 프롬프트 · 거부 판정 · 클릭. Windows 는 공식 플러그인(클릭 없음 · 실기 pending)
  - 무엇이 어려웠나: delegate 수명 · 번들 id 없는 dev 실행에서 panic 없이 떨어지기 · **창이 없을 때 남은 배너 클릭**(medi-ax 는 트레이 상주) — 클릭 하나를 60초 보관했다가 웹이 준비되면 보내는 중계를 뒀다
  - 근거: `frontend/src-tauri/src/notify.rs` · `W/review-wp4-report.md` · `W/review-wp4-r2-report.md`
- **OS 알림 줄이기** [[notification-coalescing]] — 그 대상 화면을 보고 있으면 생략 · 합친 슬랙 채널 줄은 처음만 · 10초 창에 넷 이상이면 셋 + 「새 알림 N건」 하나.
  - 근거: `frontend/src/lib/osNotifier.ts` · DEC-010 D-39

## 3. 막혔던 것 / 사고

- **의존성 올림이 웹뷰 동작을 바꿨다** [[dependency-upgrade-regression]] — tauri 2.11 → 2.12 는 공식 알림 플러그인이 요구해서 올렸다. 검수가 「65 크레이트가 움직였다 — 시험이 덮지 않는 실행 회귀는 실측으로」 라고 짚었는데, 사용자 앱에서 **전체화면을 나갔다 들어오면 아래 110px 이 비는** 회귀로 나왔다 → wry 0.55 → 0.57 의 macOS 웹뷰 생성 diff 를 전수로 보니 바뀐 것은 `elementFullscreenEnabled` 를 늘 켜는 것(#1779 · #1780) 하나 → 셸에서 끄고 셸 높이도 `100vh` → `100%` 사슬로. 결과적으로 공식 플러그인은 Windows 에만 쓰는데 그 때문에 올린 판이 macOS 를 흔들었다
- **E2E 직전 전체 테스트에서 1건** [[schema-parity-test]] — `from_me` 칸을 모델에 더했는데 처음 까는 DB 용 외부 채널 SQL 에 없어 구조 시험이 걸렸다(운영은 ALTER 로 이미 맞음). 단계마다 관련 시험만 돌린 대가로 마지막 한 번에서 잡혔다 — 그 한 번이 있어서 잡혔다
- **날짜에 묶인 기존 프론트 시험 8개** — 고정 픽스처 마감일이 오늘을 지나 「마감일 초과」 가 붙고, 달력이 9월 날짜 칸을 못 찾았다. 이번 변경과 무관함을 판정해 남겼다(`W/flaky-baseline-evidence.md`)
- **zsh 단어 나누기로 발주 실패** — `for pair in "a b"; set -- $pair` 가 zsh 에서 안 나뉘어 브리프 경로가 통째로 들어갔다. 발주는 변수 없이 한 줄씩
- **코디 핸들이 오갔다** — env 값이 stale 였다가 다시 살아났다(term_3f9a08f5 → term_aa9fb9af). 발주 직전마다 list 로 확인해 브리프 · 워커에 정정
- **운영 백업 스트림이 끊겼다** — `kubectl exec … pg_dump > 파일` 이 도중에 연결 리셋. 파드 안에 먼저 덤프 → 크기 · `pg_restore -l` 확인 → `kubectl cp` · `scp` 로 바꿨다

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-07 | 나와 관련된 것만 · 앱이 켜져 있을 때만(웹이 받아 셸이 띄움) · 설정 알림 · 사이드바 알림 이번 범위 | 사용자 |
| 2026-10-07 | 실시간은 하나로 · SSE · 회의 WS 는 그대로 | 사용자 제안 · 코디 동의 |
| 2026-10-08 | 사이드바는 알림 · 메시지함 둘 다 점(숫자 없음) · 설정 「메시지」 테마는 메일 · 슬랙 · 카톡 셋 | 사용자 |
| 2026-10-08 | DEC-010 OQ 16건 코디 추천안 확정 · 사건 × 관계 68행 확정 | 사용자 |
| 2026-10-08 | 카톡 「내가 보냄」 = 수집기를 고친다(A) | 사용자 · 운영 확인 |
| 2026-10-08 | OS 알림 클릭 = macOS UN 직접(④) · tauri 2.12 · 실측은 서명 dmg 만 | 사용자 · P0 |
| 2026-10-08 | 구현까지 끝까지 · 테스트는 단계마다 관련만 · 전체는 E2E 직전 한 번 | 사용자 |
| 2026-10-10 | ~~`from_me` 백필 apply=1~~ 안 함 — 운영 DB 를 다시 만들 예정 | 사용자 |
| 2026-10-10 | ~~화면의 「메시지함」 전부~~ → 사이드바 · 화면 머리 제목 · 목록 칸 제목 세 곳만 「메시지」 | 사용자 |

## 5. 날짜별 로그

- `2026-10-07` 메인 당김 · 알림 작업 열기 · BE·FE 조사 · 시안 1판
- `2026-10-08` 시안 2~4판 · BASE-009 · DEC-010 · SPEC-011 · WORK-013 · 검수 세 판 · P0 · WP1~WP4 구현·코드 검수 · 전체 테스트 1회 · 운영 반영 · dmg 공증
- `2026-10-10` 사용자 E2E 통과 · 「메시지」 세 곳 · 전체화면 빈 공간(tauri 2.12 회귀) · 운영 반영 2판 · 개선 목록 SH-IMP-021(캘린더 공휴일) · 마감

## 6. 산출물

- 문서 PR: kknaks/kknaks_profile #88(`72de521`) · 마감 문서 PR(이 작업)
- 코드 PR: kknaks/Strong_hajin #18(`3321504` 1루프) · #19(`baf7daf` 「메시지」 · 전체화면)
- 인프라 PR: MediSolveAIDev/k8s_infra_mac #14(`3321504-arm64`) · #15(`baf7daf-arm64`)
- 앱: medi-ax dmg 두 판(공증 Accepted) — `~/Downloads/medi-ax_0.0.1_arm64_notify.dmg` · `…_baf7daf.dmg`
- 리포트: `be-survey-report.md` · `fe-survey-report.md` · `design-change-1~4.md` · `prod-check-1.md` · `p0-report.md` · `review-spec-work(-r2·-r3)-report.md` · `review-wp1-be · wp1-fe · wp2-wp3(-r2) · wp4(-r2)-report.md` · `flaky-baseline-evidence.md` · `fe-fullscreen-report.md`
- 운영 백업: `prod-before-notify-2026-10-08.dump`(파드 /tmp · medi-me /tmp)

## 7. 잔여

- **Windows 빌드** — `cargo check --target x86_64-pc-windows-msvc` 가 이 Mac 에서 안 된다(llvm-rc · openssl-sys) → 확인 전 Windows 배포 막음
- **운영 SSE 1시간 · 배포 중 재연결 실측** — 사용자 앱 사용으로 갈음했다. 따로 재지 않았다
- **2루프 후보** — 권한 묻기 범위(W-5) · 앱 origin 이 아닐 때 클릭 버림(W-6) · 연결 끊김 표시 없음 · 시스템 알림 꺼짐 안내 줄(I-8) · 「새 알림 N건」 창·문턱 실측
- **W17 · W24 · W30** — 권한을 넓히면 그때 알림이 선다(자리만 있음)
- **날짜 고정 프론트 시험 8개** — 상대 날짜로 고친다(별도)
- **main 회의 시험 파일 8개에 실명** — 기존 · 이번 범위 밖
- **SH-IMP-021 캘린더 공휴일** — API 출처 확정부터
