# 재개 노트 — strong-hajin-inbox (strong-hajin)

**지금(2026-10-06 오후)**: BE·FE·INFRA 구현+검수 PASS · 코디 로컬 실물 — 슬랙 OK(아래) · Gmail 은 사용자 8001 리디렉션 대기 · 카톡 수집기는 범위 결정 대기
**이전 지금**: 시안 조사 완료(`design-survey.md` §0~§7, 질문 39) · 로컬 사본 `reference/2026-09-10-sc-meeting/package 2/` · 사용자와 정책 논의 중
**다음**: 1단계(슬랙·메일 → 메시지함) 정책 닫힘 → 사용자 「진행」 받으면 writer 에 baseline·decision 발주

세팅: `scripts/new-work.sh strong-hajin strong-hajin-inbox` · 설정 SSOT `config/projects/strong-hajin.json`
코디handle: `term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b` (env `ORCA_TERMINAL_HANDLE` 은 stale `term_87febe39…` — terminal list 제목 「외부 채널 연동 및 수신함 시안」으로 확인)

## 워크트리

- docs: 코디 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진` (architect 는 workspace=coordinator)

## 1. 지금

- [ ] 조사 결과로 정책 논의 → baseline → decision → spec → work 순으로 닫고 나서 구현 발주
- [x] 1단계(쌓기) 정책 닫힘 (2026-10-06)
- [x] writer — BASE-006 · DEC-008 초안(결정 40 · OQ-801~810)
- [x] DEC-008 accepted (2026-10-06, 결정 50 · 미결 0)
- [~] SPEC-008·009 writer 진행 (사용자 승인 2026-10-06 — 끝까지 구현 → 코디 로컬 실물 확인 → 운영 배포 → 사용자 E2E)
- [~] 사용자 콘솔 설정 — `reference/2026-10-06-strong-hajin-inbox/사용자-설정.md` · 비밀값 = 레포 규칙대로 `~/.config/google/env` · `~/.config/slack/env`(Makefile set -a 로드 · 운영은 k8s secretRef)
- [!] writer 가 SPEC-009 의 카톡 DB 여는 부분(키·userId·복호)을 안전 분류기 때문에 못 씀 → (a) 경계 입출력 계약만 쓰고 절차는 kakao-survey/kakao-db-fields 참조로. **구현(Rust 워커)도 같은 지점에서 막힐 수 있음 — 사용자와 처리 방식 정해야**
- [x] writer · WORK-011 초안 — Phase BE-1 · BE-2 · BE-3 · FE-a · FE-b · SHELL · INFRA · 반영
- [!] **SHELL-0(카톡 DB 여는 모듈) 발주서 작성이 코디 쪽에서 안전 장치에 막힘(2026-10-06)** → 제안: DB 모듈은 인터페이스+가짜 구현만 워커, 실제 구현은 사용자(mykakao Mac 코드 이식) — 사용자 답 대기
- [x] medi-ax dmg 빌드·서명 완료(d015091 기준 · `frontend/src-tauri/target/release/bundle/dmg/medi-ax_0.0.1_aarch64.dmg` 7.3MB · Developer ID UYQF47UCVR · codesign verify ok) · 사용자 Apple 계약 동의 → **공증 Accepted**(3414ed2e) · 스테이플 · 전달본 `~/Downloads/medi-ax_0.0.1_arm64-inbox.dmg` — **운영 배포 뒤 설치**
- [ ] **슬랙 available-rooms 첫 쪽 20.6초**(DM 이름 풀이) — 배포 전 캐시/사전 적재로 줄이기 + FE 로딩 확인 (be-fix-123-report.md)
- [x] SHELL 카톡 수집기 완료 — 커밋 **d015091** · 실기 방 426 추출 · 로컬 jiho 에 28건 업로드 · shell-report.md · 미결: 첨부 CDN 실물 1회 · 그룹방 참여자 이름 · GUI 수동 확인 — `term_d1bc29d4-64a6-44b7-8c97-73728de8f837` · task_3767868ebba2 · ctx_ef02de9c5891 · shell-brief.md (Opus 4.8) → 끝나면 dmg 빌드·공증
- [x] (해소) 카톡 수집기 발주서가 코디 쪽에서 막혔던 것 — 사용자에게 ①직접 진행 ②이번 범위 제외(설정 「준비 중」) 질문 · 답 전까지 ②로 진행. 서버 카톡 수신 API 는 완성(가짜 수집기 26/26)
- [x] writer 지시 5
- [ ] SPEC 3차 PASS → WORK-011 → 구현 발주(BE·FE·Rust·infra 각자 워크트리)
- [!] `_ds_bundle.css` 뒤 73KB 원격 비교 불가(DesignSync 256KiB 절단) · `assets/avatar-person.png` 못 받음

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-05 | 순서 = 시안 → 정책 확정 → 구현. 지금은 정책 단계 | 사용자 지시 |
| 2026-10-05 | 채널 착수 순서 Slack → 메일(회사 Google Workspace) → 카카오톡 | 사용자 지시 |
| 2026-10-05 | 카톡은 Tauri 데스크톱 앱(Rust)이 개인 Mac 의 카톡 로컬 DB 를 읽어 가져온다. ~~서버에는 카톡 연결 정보(복호화 키 · 사용자가 저장한 채팅방 ID)를 보관~~ (2026-10-06 정정 → 대화방 정보는 로컬 Rust 에 저장) | 사용자 지시 |
| 2026-10-05 | 수신함 시안 = `Inbox.html` · 시안은 로컬 `reference/2026-09-10-sc-meeting/package 2/` 에 내려받아 보며 논의(TSX 구현은 정책 뒤) | 사용자 지시 |
| 2026-10-05 | 외부 채널 단위: 메일 = 건 · 슬랙(채널)·카톡(대화방) = 흐름 | 사용자 확인 |
| 2026-10-05 | 메시지 도착 = 이벤트 → AX 가 읽고 내 프로젝트·업무를 탐색 → **업무 업데이트 / 업무 생성 / 패스** | 사용자 지시 |
| 2026-10-05 | 시안 `Inbox.html` 화면 이름 = **메시지함**, 역할 = 수집한 메시지 **조회**. AX 의 생성·업데이트 제안을 사람이 판단하는 자리 = 기존 **업무 > 수신함** (C-1 닫힘) | 사용자 지시 |
| 2026-10-05 | 메시지함 = 목록이 쌓이고 **읽음 확인만**. 시안 카드의 업무/참고 배지·`+`·`내 업무로`·`답장`·`확인완료` 는 쓰지 않는다 (AX 가 패스한 것을 사람이 건지는 길은 이번엔 없음) | 사용자 지시 |
| 2026-10-05 | **단계 분리** — 1단계 목표 = 메일·슬랙·카톡이 메시지함에 쌓인다(설정 연동 화면 + 수집 + 메시지함 조회·읽음). 2단계 = AX 판단(생성/업데이트/패스 → 업무>수신함). 흐름의 이벤트 단위는 2단계에서 정한다 | 사용자 지시 |
| 2026-10-05 | Slack 흐름: 설정에서 보고 싶은 **채널·대화방(DM·그룹 DM)** 을 저장 → 서버에 방 정보 저장 → 이벤트가 생길 때마다 메시지함에 **실시간 반영**. 표기 `슬랙 - #채널명` · `슬랙 - 대화방명 or 참여자` (시안의 채널만·수집 주기와 다름) | 사용자 지시 |
| 2026-10-05 | Slack 기본값(코디 통보): DM 을 읽으려면 **사용자 토큰**(본인 권한으로 읽음 — 봇은 남의 DM 불가) · 실시간 = Slack 이벤트 구독 · 방 추가 때 과거 메시지 최근 30일 · 스레드 답글은 같은 방 카드에 「답글」 표시 | 코디 기본값, 사용자 이의 시 변경 |
| 2026-10-06 | 메일 연결은 **사용자 1회 등록**으로 읽기(1단계)와 답장(2단계)을 모두 덮는다 — IMAP 이면 같은 앱 비밀번호로 SMTP, Gmail API 면 연결 때 readonly+send 를 함께 받는다. 방식(IMAP / Gmail API 내부 앱)은 Workspace 관리자 콘솔 접근 여부로 결정 — 미결 | 사용자 지시 |
| 2026-10-06 | Gmail API 실물 시험 **통과** — 회사 GCP 프로젝트 `mediness` 에 데스크톱 클라이언트 `strong-hajin-mail-test` · 동의 1회로 `gmail.readonly`+`gmail.send` 동시 부여 · refresh token 받음 · 받은편지함 5통 읽음. 운영 연동을 어느 GCP 프로젝트에 둘지(회사/개인·이직·상용)는 미결 | 시험 스크립트 결과 |
| 2026-10-06 | 메일 = **Gmail API**, 회사 GCP 프로젝트 `mediness` 에 둔다(①). 연결 1회에 readonly+send. 클라이언트 ID·비밀값은 env 로만 넣어 개인 프로젝트로 옮길 수 있게(이직·상용 때 ③ 정식 심사로 이전, 사용자 재연결 1회) | 사용자 결정 |
| 2026-10-06 | **카카오톡은 뒤로 미룬다** — 지금은 Slack·메일만. 카톡 질문(K-1 동의 문구 · K-2 수집 기기 카드 · K-3 방 목록 고르기)은 열린 채로 둔다 | 사용자 지시 |
| 2026-10-06 | Slack 사용자 토큰 실물 시험 **통과** — 새 앱 `Strong Hajin`(워크스페이스 MediSolve AI) · User Token Scopes 10개(`admin.teams:write` 제외) · 관리자 승인 없이 설치 · 방 목록 채널 52 / 비공개 4 / 그룹DM 35 / DM 53 · 채널·DM 메시지 읽기 ✓. 그룹DM 이름은 `mpdm-…` 라 참여자 실명으로 풀어 보여야 함 · DM 목록에 봇(질문봇 등) 포함 | 시험 스크립트 결과 |
| 2026-10-06 | 슬랙·메일 모두 **실시간 동기화** — 슬랙 이벤트(Socket Mode 또는 Events API) · Gmail Pub/Sub 신호(watch 7일 만료 → 매일 갱신) · 재시작 때 마지막 시점 이후를 훑어 빠진 것 메우기. 시안의 수집 주기 → 「실시간」 | 사용자 결정 |
| 2026-10-06 | 봇 처리 없음 — 채널은 사용자가 고른 것이라 봇 메시지도 그대로 쌓는다. 봇 DM 도 방 목록에 그대로(실측: DM 66 중 봇 26, 채널 56 중 39 에 봇 메시지) | 사용자 지시 |
| 2026-10-06 | 메일은 받은편지함만(스팸·프로모션·보낸 메일 제외) · ~~방/계정 삭제 시 쌓인 메시지도 삭제~~ (2026-10-06 뒤집음 → 소프트 딜리트) · 설정의 계정·알림 메뉴는 이번 범위 밖 | 사용자 결정 |
| 2026-10-06 | 흐름 = 메일/슬랙 수신 → 우리 DB 저장 → 앱에서 **개인별 노출**. 연결·방·메시지는 연결한 사용자 소유, 본인만 본다 | 사용자 지시 |
| 2026-10-06 | 같은 채널·방을 여러 사람이 골라도 **사람마다 따로 저장**(각자 토큰·각자 읽음) | 사용자 결정 |
| 2026-10-06 | **1차 목표 = 연동 + 조회.** 연동 정보는 ~~사용자 테이블에 저장~~ (2026-10-06 정정 → 별도 연동 테이블 + `users` 외부키) · 계정(연동) 삭제는 DB **소프트 딜리트** | 사용자 지시 |
| 2026-10-06 | 최초 1회 연동 때 과거 내용 최대한: **메일 = 받은편지함 전체** · **슬랙 = API 가 허용하는 기간·양 전부**(플랜 열람 한도까지). 시안의 「가져올 범위」 선택 없음 · 앞의 「슬랙 30일 / 메일 90일」 기본값 대체 | 사용자 지시 |
| 2026-10-06 | 연동 정보 = **별도 연동 테이블**, `users` 와 **외부키** 관계. 고른 슬랙 방·메시지도 그 연동에 매달린다 | 사용자 결정 |
| 2026-10-06 | 메시지함 본문 다시 그린다 — 메일: 머리 표(보낸·받는·참조·날짜·계정)·읽기 폭·HTML 틀·첨부 칩 / **슬랙: 진짜 슬랙 대화방처럼**(날짜 구분선·연속 묶음·서식·이미지·리액션·스레드, 입력창·행동 없음). 시안(Claude Design)을 먼저 고친다 | 사용자 승인 |
| 2026-10-06 | 첨부 = **파일은 우리 서버에 저장하지 않는다.** DB 에는 첨부 정보(이름·유형·크기·슬랙 url_private / Gmail 첨부 ID)만. 사용자가 클릭하면 그때 서버가 그 사용자 토큰으로 슬랙·Gmail 에 요청해 받아 넘긴다(중계). URL 미리보기 정보는 메시지와 함께 저장 | 사용자 결정 |
| 2026-10-06 | 메시지 **원문 그대로 저장**(슬랙 text·blocks·files·attachments JSON / 메일 원본) — 가공은 렌더링에서만. 슬랙 렌더 = rich_text blocks 우선, 없으면 mrkdwn text. 멘션·채널 ID 는 이름으로 풀어 그린다. 대화형 요소(버튼 등)는 1단계에서 안 그린다 | 사용자 결정 |
| 2026-10-06 | 설정 시안도 고친다 — 메일: IMAP 폼 → 「Google로 연결」·계정 여러 개·범위 없음·실시간·연결 해제 / 슬랙: 연결 단추·방 고르기 모달(채널·비공개·DM·그룹DM)·실시간. 카톡·계정·알림 메뉴는 그대로 | 사용자 승인 |
| 2026-10-06 | **1단계에 답장 포함** — 메일(답장·전체 답장, 원문 아래 작성 칸) · 슬랙(입력창·스레드 답글, 내 이름으로) · 첨부 보내기(끌어다 놓기 + 첨부 창, 기존 DS `DropZone`·`FileList`). 「1차 목표 = 연동+조회」를 연동+조회+답장으로 넓힘. 슬랙 파일 보내기엔 `files:write` 사용자 권한 추가 필요 | 사용자 지시 |
| 2026-10-06 | 카카오톡은 **Mac 에서만** 지원. 조회+발송 가능성 조사 — mykakao 문서 + 외부 kakaocli(silver-flight-group) | 사용자 지시 |
| 2026-10-06 | 카톡 흐름: Rust 앱이 **백그라운드 실행** · 설정 = 로컬 → Rust 에 **카톡 대화방 정보 저장** · 메시지함 = 로컬 카톡 → Rust → 서버 DB → 렌더링 → **발송**(메시지함 → 서버 → Rust → 카톡). 복호화 키 보관 위치는 미결 | 사용자 지시 |
| 2026-10-06 | 설정 `계정 설정` → **`프로필 설정`**: 프로필 이미지(바꾸기·삭제) · **AX 캐릭터 설정**(지금 앱의 캐릭터 고르기를 이리로) · 비밀번호 변경. **이름·직무는 조직 명부 값이라 여기서 안 고친다**(읽기 전용 표시). 「설정의 계정 메뉴는 범위 밖」을 이 범위만큼 되돌림. 비밀번호 변경 API 는 지금 코드에 없어 새로 필요 | 사용자 지시 |
| 2026-10-06 | 카톡: **Rust 앱이 카카오톡 실행 여부를 확인**해야 한다(꺼져 있으면 수집·발송 불가 상태를 보인다 — K-2 수집 기기 카드와 묶임) | 사용자 메모(워커 터미널 경유) |
| 2026-10-06 | 메시지함 본문 **폭 전체 사용**(읽기 폭 제한 없앰) · 슬랙 스레드는 **오른쪽 패널 3열**(레일 | 대화 | 스레드) | 사용자 피드백 — `design-feedback-batch-1.md` 에 모음 |
| 2026-10-06 | 카톡 이번 범위 = **조회만**(발송 없음) · **사용자가 고른 대화방만** · **첨부도 조회 가능한 구조**. 키는 Mac 안에서만(기기값으로 자동 유도 — 서버 보관 안 함, K-10) · 시안의 참여자 안내·동의 문구는 뺀다(기술 근거 없음, K-2) · 과거 = 이 Mac 로컬에 있는 만큼 | 사용자 지시 · 코디 기본값 |
| 2026-10-06 | 카톡 첨부 = **실시간 수집 순간 CDN 에서 받아 우리 쪽에 저장**(「첨부 저장 안 함」 원칙의 카톡 예외 — CDN URL 이 만료되기 때문). 이미 만료된 옛 첨부는 「만료됨」 표시·복구 안 함 | 사용자 결정 |
| 2026-10-06 | 카톡: **1:1·단체방 모두 사용자가 골라야** 수집 · 카톡은 **조회용**(입력창 없음), 내용은 **DB 저장** · 첨부 파일은 배포 서버 k8s **전용 바인드 마운트(hostPath)** 에 저장하고 DB 에는 **경로만** · 본인 카톡 DB 를 **읽기 전용으로 1회 확인** 승인(사본·개인정보 가림) | 사용자 결정 |
| 2026-10-06 | 카톡 첨부 종류: 사진·앨범·파일 = 수집 즉시 받아 저장 · 동영상·음성 = 표시만 · 이모티콘 = 「(이모티콘)」 · **오픈채팅방 제외** · 계정 = **카카오톡에 로그인한 계정 기준**(고르는 목록 없음) | 사용자 결정 |
| 2026-10-06 | DEC-008 OQ-801~810 전부 닫음 — 801 Gmail 회사 내부 앱 유지(심사는 회사 밖 사용자·개인 프로젝트 이전 때만) · 802 「카카오톡을 읽을 수 없음」 상태 · 803 상태 카드 정보 4개 · 804 **앱 공통 최소 폭 1542px 따름, 좁은 화면 대응 없음**(업무 탭 3열과 같음) · 805 계정 바뀌면 수집 멈춤·Mac 사람당 1대 · 806 재연결 시 되살림+빈 구간 · 807 보낸 답장 = 우리 기록 · 808 캐릭터 기존 진입점 없앰 · 809 보존 기간 미정(소프트 딜리트만) · 810 메시지함 머리 배너 | 사용자 결정 |
| 2026-10-06 | 수신 방식 = **슬랙 Socket Mode · Gmail Pub/Sub pull** — 로컬·운영 모두 공개 수신 주소 없음(터널 불필요). Gmail 서버 연결은 **웹 OAuth 클라이언트** 새로(리디렉션 localhost+운영). 슬랙 OAuth 버튼 흐름은 https 필요 → 운영에서 확인 · 진행 = 코디 구현 / 사용자 콘솔 설정 병행 · 최종 사용자 E2E | 사용자 승인 |
| 2026-10-06 | **보존·파기 없음** — 회사 데이터라 수집한 원문·첨부는 계속 보관(D-49·SPEC OQ-805 닫힘) · **첨부 한도 50MB 통일**(메일 보내기는 Gmail 자체 한도 25MB 와 충돌 — 확인 필요) | 사용자 결정 |
| 2026-10-06 | **카톡 DB 읽기 = mykakao 자체 방식(DEC-001 accepted · SPEC-001 · 로컬 코드 `~/git/toy_pr2/mykakao`)을 Rust 로 옮긴다** — kakaocli 는 참고만(사이드카 안 씀). 앞 조사가 「mykakao = Windows 뿐」이라 한 것은 오판(설정 canonical 경로가 Windows 라서) · **첨부 한도: 메일 보내기 25MB(Gmail 자체 한도) · 그 밖(카톡 수집·슬랙 보내기) 50MB** · SPEC 미결 추천안 채택: 801 env 대칭키(Fernet) · 802 연동 전용 워커 새로(레플리카 1) · 803 pull · 804 회사판만 · 808 사람마다 복제 · 901 같은 데스크톱 앱에 수집 추가(SPEC-006 「파일 권한 없음」 원칙 개정) · 902 폴링 2초 · 903 mykakao 복구 절차 · 904 기존 서명·공증, 자동 업데이트 없음 · 905 「카카오톡을 읽을 수 없습니다 — 버전이 바뀌었을 수 있습니다」 | 사용자 결정 |
| 2026-10-06 | 비밀값 위치 = **레포 규칙 `~/.config/<서비스>/env`** (Google → `~/.config/google/env` + `oauth-web-client.json` · `pubsub-sa.json` / Slack → `~/.config/slack/env`). Makefile 이 soniox·theconnect 처럼 읽게 구현 · 운영은 k8s Secret. 처음 만든 `~/strong-hajin-deploy-data/integrations/` 는 폐기 | 사용자 지적 · 코드 확인 |
| 2026-10-06 | SPEC 검수 FAIL 처리 결정: ① **카톡 방 목록·선택 = Mac 이 정본** — 서버는 웹 방 고르기 창을 위해 **중계만**(저장 안 함 · 앱 꺼지면 「Mac 앱이 켜져 있어야…」) · 서버에 남는 방 = 메시지가 올라온 방뿐 · 서버는 고른 방 메시지만 받는지 검사 ② 카톡 수집은 **회사판 medi-ax** 앱에(개인판은 주소 정해질 때) ③ **SPEC-006 원칙 개정 수용** — 백그라운드 상주 · 메뉴 막대 아이콘 · 전체 디스크 접근 · 관련 AC/셸 시험 | 사용자 결정 |
| 2026-10-06 | 사용자 콘솔 설정 A(Google)·B(Slack) 완료 — 코디 실물 확인: Google OAuth 리디렉션 2개 · Pub/Sub 구독 pull 200 · Slack Socket Mode 연결 주소 발급 · Client ID·Secret 일치 · 사용자 토큰 11권한. 조직 정책 2개(`iam.allowedPolicyMemberDomains` · `iam.disableServiceAccountKeyCreation`)를 mediness 만 잠깐 풀었다 → 되돌리기·관리자 역할 회수 남음 | 사용자 작업 · 코디 확인 |
| 2026-10-06 | **카톡 방 고르기 = 데스크톱 앱(Rust) 로컬에서** — 설정 화면이 데스크톱 앱 웹뷰 안에서 열리면 Tauri 커맨드로 Rust 가 로컬 DB 방 목록을 읽고 선택을 로컬에 저장(서버 중계·명령 대기열 없음). 브라우저에서 열면 카톡 방 고르기 대신 「Mac 앱에서 고르세요」 + 상태·수집된 방만. (R-F1 해소) · OQ-906 **장수명 기기 토큰 채택**(수집기는 창 쿠키에 기대지 않음 — R-F2 쿠키 문제 해소) · OQ-811 「Mac 앱 받기」 = Strong_hajin GitHub Releases | 사용자 지적·결정 |
| 2026-10-06 | **카톡 「고른 방」(설정 정보)은 서버에 저장한다** — 앞 행의 「선택도 Rust 가 로컬에 저장」을 바꾼다. 방 **전체 목록 탐색**은 여전히 데스크톱 앱이 고르기 창을 열 때만 Rust 로컬에서(서버 저장 안 함). 고른 방 = 서버가 정본(웹에서도 보이고 재설치·새 Mac 에서 유지), Rust 는 시작·생존 신호 때 서버에서 받아 로컬 캐시. D-15 「대화방 정보는 로컬」은 **방 목록**으로 좁혀 읽는다 | 사용자 결정 |
| 2026-10-06 | **진행 권한: 「계속 하라 — 코드 구현까지 끝내라」.** SPEC 검수 PASS → WORK-011 → 구현 → 코디 실물 확인 → 운영 배포까지 단계마다 사용자 승인 없이 진행. 최종 E2E 만 사용자 | 사용자 지시 |
| 2026-10-06 | 데스크톱 창 닫기 = **웹뷰 실제 파괴 · 프로세스만 메뉴 막대 상주**(수집기는 기기 토큰) — 「숨기기 + 점유 해제」는 숨은 웹뷰 녹음 문제로 폐기 · 기기 토큰 범위 = 카톡 수집 라우트 + 고른 방 조회만, 해시 보관, 비번 변경·새 발급 시 철회 · 카톡 중복 키에 연동(사용자) 범위 포함 | 코디 결정(진행 권한) · 3차 검수 근거 |
| 2026-10-06 | **코디 로컬 실물(슬랙) 통과** — 스택(ax_demo_inbox · API 8001 · FE 5176 · external-worker) · jiho 에 개발 토큰 연동 · available-rooms 144(채널52·비공개4·그룹DM35·DM53 = 실측과 일치) · 본인 DM 추가 → 백필 51 → live · 답장 202 → **1.1초 뒤 메시지함에 수신**(실시간) · 응답에 users 맵·permalink | 코디 확인 |
| 2026-10-06 | **카톡 수집기(SHELL) = Opus 4.8 워커로 발주, mykakao 기존 코드(`~/git/toy_pr2/mykakao`)를 옮겨 쓴다** — 이후 dmg 빌드(medi-ax)·서명·공증까지 | 사용자 지시 |
| 2026-10-06 | 코디 로컬 실물(Gmail): 8001 리디렉션 등록 확인 → 사용자 동의 OK → **백필 100통 저장** → 곧 `PERMISSION_DENIED` 로 「끊김」(403 을 무조건 토큰 폐기로 분류) · 슬랙 연동도 멀쩡한 토큰인데 3분 뒤 `revoked` 로 조용히 끊김 → **BE 수정 판 4** 발주(be-fix-4-instructions.md) | 코디 확인 |
| 2026-10-06 | 메일 원격 이미지 = **자동 표시**(우리 이미지 프록시 경유만 — Gmail 방식) · 「이미지 보기」 배너 없앰 | 사용자 결정 |
| 2026-10-06 | 수집 실패 알림 모양 = 메시지함 머리 「모두 읽음으로」 옆 **[!] 배지 → 팝오버 경고 목록**(본문 배너 대신 · D-50 의 모양 변경) | 사용자 피드백 — local-feedback-batch-1.md |
| 2026-10-06 | BE 수정 판 4·5 커밋 **2807351** — 403 오분류(Gmail 속도 제한·슬랙 첨부 files:read 없음)로 조용히 끊던 것 수정 · 이미지 프록시 22/22(로컬 CA 에 Sectigo 루트 없던 것 certifi) · 배경/스타일 보존 · 읽음 500(동시 요청) · **슬랙 User Token Scopes 에 `files:read` 추가 필요(12번째)** · 로컬 스택 재시작 | 코디 확인 |
| 2026-10-06 | 슬랙 `files:read` 추가·재설치 확인(13 scopes) → 재연결 → **슬랙 첨부 중계 3/3 200**(image/png, 저장 안 함) · 연동 connected 유지 · 카톡 connected | 코디 확인 |
| 2026-10-06 | 앱 사용자 ↔ 슬랙·메일 계정 매핑 검사(연결된 계정 표시 · 이메일 불일치 거절)는 **보류 — 운영에서 각자 본인 계정으로 연결하면 해결**(로컬은 데모 jiho 에 개발 토큰을 붙인 시험 방식이라 생긴 혼동) · 지금은 **대화방·채팅방 로딩 속도만** | 사용자 결정 |
| 2026-10-06 | **운영 반영 완료** — 코드 PR kknaks/Strong_hajin#12 머지(main 279f94b) · 노드 hostPath(worker-1) · manual SQL 새 표 9 · Secret(앱 키 7 + 운영 전용 암호화 키 · Pub/Sub SA 키 Secret) · 이미지 279f94b-arm64 · 인프라 PR MediSolveAIDev/k8s_infra_mac#10 머지 · Argo sync Synced/Healthy · worker-external 1/1 Recreate · 단일 소유 잠금 · 슬랙 Socket Mode 연결 · SA 키 존재 · 저장소 쓰기 가능 · /health 200. 로컬 스택은 내림(Socket Mode·Pub/Sub 경합 방지) | 코디 반영 |
| 2026-10-06 | 운영 E2E 결함 2 — ① 카톡: 수집기가 https 첫 요청에서 패닉(ureq native-tls provider 미등록 · 로컬은 http 라 안 드러남) → Opus 4.8 워커 수정 · PR kknaks/Strong_hajin#13 머지(main 4e48632) · dmg 재빌드·서명·**공증 Accepted** → `~/Downloads/medi-ax_0.0.1_arm64-inbox-fix1.dmg` ② 슬랙 bad_client_secret — 코드는 표준, 저장 값이 앱의 현재 Client Secret 아님(코디의 가짜 code 검증은 무효였음) → 사용자가 Client Secret 재복사 대기 · 진단 로그는 다음 이미지에 | 코디 반영 |
| 2026-10-06 | **운영 E2E: 메일·슬랙 정상**(사용자 확인) — 슬랙은 Client Secret 재발급(지문 b2aa32d0) → 운영 Secret 교체·back/worker-external 재시작 후 연결 OK · 카톡은 앱 연결·「방 추가」 정상, **단체방 「(이름 없음)」 수정 중**(Opus 4.8) | 사용자 확인 |
| 2026-10-06 | 운영 E2E 결함: 메일 본문이 **medi-ax 앱(WebKit)에서만** 빈 칸(Chrome 정상) → FE 워커 · 카톡 단체방 이름 수정은 PR kknaks/Strong_hajin#14(미머지) — **둘을 한 번에 반영**(PR 머지 → front·back 이미지 + dmg 재빌드·공증) | 사용자 결정 |
| 2026-10-06 | **2차 반영** — PR kknaks/Strong_hajin#14(카톡 단체방 이름)·#15(메일 본문 medi-ax: srcdoc → 첫 문서에 써 넣기) → main f0ad522 · 이미지 f0ad522-arm64 · 인프라 PR MediSolveAIDev/k8s_infra_mac#11 · Argo Synced/Healthy · 9 파드 Running · worker-external 잠금·Socket Mode 연결 · /health 200 · dmg 공증 Accepted → `~/Downloads/medi-ax_0.0.1_arm64-inbox-fix2.dmg` | 코디 반영 |
| 2026-10-07 | 운영 E2E 마감: 메일·슬랙·카톡 연결·수집 OK(사용자) · **남은 것은 개선 목록으로** — BUG-001(reference) → SH-IMP-006 이관 · SH-IMP-007 첨부(카톡 안 받아짐·슬랙/메일 운영 확인) · 008 AX 판단(2단계) · 009 계정 매핑(보류) · 010 설정 숫자 실시간 · 011 셸 하위 프레임 · 012 슬랙 나간 방 분배 · 013 카톡 수집기 남은 확인. 첨부·AX 는 다음 세션 | 사용자 지시 |
| 2026-10-05 | 설정·수신함·외부 연동을 한 slug(`strong-hajin-inbox`)로 | 코디 제안, 사용자 이의 없음 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| architect | `term_208c9243-9983-47ba-9983-e3aa67ecf049` | `task_c0fbdf53f1ba` | `ctx_2428fb711ef8` | `strong-hajin-inbox-arch-design-brief.md` (메시지함 시안 쓰기, +design-instructions-1) | 완료 — 사용자 화면 확인 대기 |
| architect | `term_208c9243-9983-47ba-9983-e3aa67ecf049` | `task_aa9b42321beb` | `ctx_8de4f0c0e371` | `strong-hajin-inbox-arch-settings-brief.md` (설정 시안 쓰기 — 메일·슬랙만) | 완료 — design-change-2.md |
| architect | `term_208c9243-9983-47ba-9983-e3aa67ecf049` | `task_13e47b110461` | `ctx_dfbfe0fd67c6` | `strong-hajin-inbox-arch-reply-brief.md` (메시지함 답장 시안) | 완료 — design-change-3.md |
| architect | `term_208c9243-9983-47ba-9983-e3aa67ecf049` | `task_89c2cec6488b` | `ctx_b89a95e1f294` | `strong-hajin-inbox-arch-profile-brief.md` (프로필 설정 시안) | 완료 — design-change-4.md |
| architect | `term_208c9243-9983-47ba-9983-e3aa67ecf049` | `task_af0f087928ce` | `ctx_783f4a5e0fda` | `strong-hajin-inbox-arch-fb1-brief.md` (피드백 1 — 폭 전체·스레드 3열) | 완료 — design-change-5.md |
| architect | `term_208c9243-9983-47ba-9983-e3aa67ecf049` | `task_9d41687d7a5f` | `ctx_ee70b57e89c6` | `strong-hajin-inbox-arch-kakao-design-brief.md` (카톡 설정·메시지함 시안) | 완료 — design-change-6.md |
| writer | `term_3fb95c1b-5d7d-4bcd-8409-b1dba0fbfdea` | `task_c8e1fb0918e1` | `ctx_c63dfbe7c575` | `strong-hajin-inbox-write-brief.md` (BASE-006 · DEC-008 + instructions-1) | 완료 — DEC-008 accepted(결정 50 · 미결 0) |
| writer | `term_3fb95c1b-5d7d-4bcd-8409-b1dba0fbfdea` | `task_564e70378891` | `ctx_fdbbc9104c1e` | `strong-hajin-inbox-write-spec-brief.md` (SPEC-008 서버·웹 · SPEC-009 Mac 카톡 수집기 + spec-instructions-1) | 완료 — v0.2.0 |
| reviewer | `term_fd936f8b-e332-4fa6-b892-ad24d3e754cd` | `task_963fa618256d` | `ctx_ae1b4deb8155` | `strong-hajin-inbox-review-brief.md` (SPEC-008·009 검수, read-only · 코드 워크트리 Strong_hajin/strong-hajin-inbox) | 1차 FAIL 4 · WARN 17 → writer 수정(S8·S9 v0.3.0 · S6 v0.4.0) → 2차 FAIL(R-F1·R-F2·WARN12) → writer v0.4.0/S6 v0.5.0 → 3차 FAIL(R3-F1 기기 토큰 계약 · R3-F2 숨기기 vs 녹음 → 닫기=웹뷰 파괴·프로세스 상주) · WARN 9 → writer v0.5.0/S6 v0.6.0 → 4차 **조건부 PASS**(FAIL 0 · ★4) → 구현 착수 |
| backend | `term_b638849c-2972-4ae7-abff-a0a37e118c60` | `task_dcbd72328974` | `ctx_2695d151590a` | `strong-hajin-inbox-be-brief.md` (WORK-011 Phase BE-1) | 완료 — 커밋 78f014f(로컬, 미push) · 코드 검수 WARN(FAIL 0 · review-be1.md) — W-6 은 be-coordination-1 로 즉시 조정 · W-2·3·4·5·7·8·9 는 BE-2/3 뒤 BE 수정 판 · **W-1 운영 configmap AX_WEB_ORIGIN 은 INFRA 필수** |
| backend(BE-2) | `term_b638849c-2972-4ae7-abff-a0a37e118c60` | `task_3e295ffdfad7` | `ctx_938e5c685425` | `strong-hajin-inbox-be2-brief.md` (연동 워커 · 슬랙/Gmail · ★3) | 완료 — be2-report.md · 슬랙 실물(백필 48 · 실시간 0.53초 · 재시작 메우기 중복 0) · Gmail 실동의는 코디 확인 대기(8001 리디렉션) · 커밋 db57ba7 |
| backend(BE-3) | `term_4e60d06d-45f3-4a0a-bb72-169d2b5a91d6` | `task_cded83d2822c` | `ctx_2b92e64681f0` | `strong-hajin-inbox-be3-brief.md` (메시지함·답장·프로필·카톡 수신) | 완료 — be3-report.md · 실물 26/26 · 커밋 **db57ba7**(BE-2+BE-3, 로컬 미push) · 메일 카드 from→sender FE 통보 |
| backend(수정 판 1) | `term_b638849c-2972-4ae7-abff-a0a37e118c60` | (메시지 지시) | — | `be-fix-1-instructions.md` (BE-1 WARN W-2~9 + 답장 내구 경로) + `be-fix-2-instructions.md`(BE-2·3 검수 **FAIL 2: 슬랙 방 접근 미검사 누출 · available-rooms 없음** + WARN 12) | 진행 |
| reviewer | `term_fd936f8b-e332-4fa6-b892-ad24d3e754cd` | (메시지 지시) | — | `strong-hajin-inbox-review-instructions-5.md` (BE-2·3 코드 검수 → review-be23.md) | 완료 — FAIL 2 · WARN 12 → BE 수정 판 커밋 **b2ba11a** → **재검수 PASS**(review-be-r2.md · 운영 전 권장 W-N1 나간 방 잔여 팬아웃 창) |
| frontend | `term_e3b0bba1-f7c7-47b9-bdff-111d9894557e` | `task_2411ddbe7504` | `ctx_02e7ea97da77` | `strong-hajin-inbox-fe-brief.md` (FE-a·FE-b) | 완료 — fe-report.md · 커밋 **496fc1e** · 검수 FAIL 1(링크 스킴)·WARN 7(review-fe.md) → fe-fix-1 커밋 **17ea307** → **재검수 PASS**(review-fe-r2.md) |
| infra | `term_92255e52-73b0-43f3-8eee-d733434da316` | `task_507d343dc47b` | `ctx_80215921630b` | `strong-hajin-inbox-infra-brief.md` (연동 워커·hostPath·Secret·SA 키 볼륨·AX_WEB_ORIGIN·ingress · 워크트리 k8s_infra_mac/strong-hajin-inbox-infra) | 완료 — 인프라 커밋(로컬 미push) · AX_WEB_ORIGIN 은 이미 configmap 에 있었음(W-1 확인) · AX_API_ORIGIN 추가 · 반영 명령 infra-deploy-steps.md |
| architect(kakao) | `term_a0ef6537-e532-4b7e-84e5-7e174161f6d8` | `task_c1f9826f6c96` | `ctx_89d477500d99` | `strong-hajin-inbox-arch-kakao-survey-brief.md` (카톡 Mac 조회·발송 조사, read-only) | 완료 — kakao-survey.md |
| architect(kakao) | `term_a0ef6537-e532-4b7e-84e5-7e174161f6d8` | `task_9986ebddefc5` | `ctx_271b35ef4ab8` | `strong-hajin-inbox-arch-kakao-attach-brief.md` (카톡 첨부 조회 구조, read-only) | 완료 — kakao-attach-survey.md |
| architect(kakao) | `term_a0ef6537-e532-4b7e-84e5-7e174161f6d8` | `task_84e26a4460bc` | `ctx_90e1fc8f0b81` | `strong-hajin-inbox-arch-kakao-dbpeek-brief.md` (본인 카톡 DB 사본 읽기 전용 — 첨부 필드) | 완료 — kakao-db-fields.md |

## 4. 산출물

- 문서: `para/projects/summer-star/strong-hajin/00-baseline/baseline-006-external-channels.md` · `10-decision/decision-008-external-channels.md` (미커밋)
- 리포트: `kakao-db-fields.md` — 본인 DB 사본 복호 성공(kakaocli 그대로는 실패 → userId 복구) · 첨부 = talk.kakaocdn.net 서명 URL(사진 TTL ~3일·파일 ~14일) · 방 구분·중복키 (chatId,logId)
- 리포트: `kakao-survey.md` — Mac 조회 가능(키 기기값 유도·앱 꺼져도) · 발송은 접근성 UI 자동화(텍스트만·불안정) · 선택지 A 사이드카/B Rust 포팅/C 하이브리드 · 새 질문 K-9~K-12
- 리포트: `design-change-1.md` — Claude Design 메시지함 시안 쓰기(5파일) + 로컬 사본
- 리포트: `design-survey.md` — 시안 조사(§6 차이 17 · §7 질문 공통16/슬랙7/메일8/카톡8)

## 5. 이력 (최신이 위)

- `2026-10-05` architect 완료 — design-survey.md + Inbox/Settings 로컬 사본(nav.js 덮어씀)
- `2026-10-05` slug 생성 · architect 시안 조사 발주(read-only)
