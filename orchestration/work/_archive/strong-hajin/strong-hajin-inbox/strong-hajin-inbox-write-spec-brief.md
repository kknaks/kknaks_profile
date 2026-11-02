# [writer] SPEC-008 · SPEC-009 — 외부 채널 연동 · 메시지함 · 프로필 / Mac 카톡 수집기

너는 strong-hajin `writer` 워커다(BASE-006·DEC-008 을 네가 썼다). 맥락이 없으면: 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/planner/role.md` · 문서 규칙 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/project.md`.
작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진` = 코디 워크트리. §5 파일만 쓴다.

## 1. SSOT
- **`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/decision-008-external-channels.md`** (accepted · D-01~D-50) ← 계약의 SoT. **여기 없는 정책은 발명하지 마라** — 모자라면 SPEC 의 Open Questions 로
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/00-baseline/baseline-006-external-channels.md`
- 확정 시안(UX 정본): 로컬 사본 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` — `Inbox.html`(메시지함) · `Settings.html` + `handoff/inbox/*` · `handoff/settings/*` · 변경 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-1.md`~`-6.md`
- 카톡 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/kakao-survey.md` · `kakao-attach-survey.md` · `kakao-db-fields.md`
- 형식 본보기: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` (frontmatter · 1 Context · 2 UX Contract · 3 User Scenario · 4 Interface Contract · 5 Implementation Rules · 6 Verification · 7 미결) · Tauri 쪽은 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md` · 배포는 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/decision-007-production-deploy.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/70-runbook/runbook-002-production-deploy.md`
- **코드(읽기만)** `/Users/kknaks/git/toy_pr2/Strong_hajin` (origin/main) — 계약은 **지금 코드 구조에 맞춰** 쓴다: 백엔드 모듈 배치(`backend/src/ax_workspace/modules/*`)·인증/세션·사용자(`organization_access`)·마이그레이션 방식·워커 프로세스(`bootstrap/*_worker.py`)·설정(env) 로딩·파일 저장 방식(회의 자료 첨부가 지금 어디 저장되나)·프론트 라우팅·DS·데스크톱 셸(`desktop/` 또는 Tauri 디렉터리). 어긋나면 코드를 근거(파일:줄)로 적는다

## 2. 무엇을 쓰나
**SPEC-008 — 외부 채널 연동 · 메시지함 · 프로필 설정 (서버 · 웹)**
- 데이터: 연동(사용자 FK · 종류 메일/슬랙/카톡 · 암호화한 토큰 · 상태 · 소프트 딜리트) · 고른 방(슬랙·카톡) · 메시지(원문 그대로 JSON · 중복 방지 키 — 슬랙 (channel, ts) · Gmail message id · 카톡 (chatId, logId)) · 첨부 메타(이름·크기·MIME·출처 참조 / 카톡은 저장 경로) · 읽음(사용자별) · 보낸 답장 기록(D-47) · 프로필 이미지
- 동기화: **슬랙 Socket Mode**(앱 토큰 1개 · 연결은 서버 한 곳에서만 — 프로세스 배치 조건 명시) · **Gmail = users.watch + Pub/Sub pull**(watch 7일 → 매일 갱신) · 최초 백필(메일 받은편지함 전체 · 슬랙 허용 끝까지 — 뒤에서 채우며 진행률) · 재시작 메우기(마지막 시점 이후)
- 연결 흐름: Gmail OAuth(웹 클라이언트 · readonly+send 한 번에) · 슬랙 OAuth(사용자 토큰 11권한 — files:write 포함) · 리디렉션 **경로를 여기서 정한다**(로컬·운영)
- 메시지함 API: 목록(출처 필터 · 미읽음) · 본문 · 읽음/모두 읽음 · 첨부 받기(메일·슬랙 = 그 사용자 토큰으로 중계, 저장 안 함 / 카톡 = 저장본) · 슬랙 렌더(blocks 우선·mrkdwn 대체·멘션 이름 풀기)는 프론트 계약
- 답장: 슬랙(채널·스레드 · 내 이름 · 첨부 files:write) · 메일(답장/전체 답장 · 스레드 이어짐 · 첨부 25MB) — 보내는 중/실패
- 설정 API: 연동 목록·연결·해제(소프트 딜리트, D-46 재연결 시 되살림) · 방 고르기 목록(슬랙 = 사용자 토큰으로 조회 / 카톡 = Mac 앱이 올린 목록) · 상태(실시간·채우는 중·끊김) · 실패 배너(D-50)
- 카톡 수신 쪽: Mac 앱 → 서버 **업로드 계약**(방 목록 · 메시지 묶음 · 첨부 파일 · 상태 보고 — 앱/카톡/읽기 불가/계정 바뀜) · 인증(앱이 사용자 세션으로 붙나 — 지금 데스크톱 셸 구조 근거로)
- 첨부 저장: 카톡 첨부·프로필 이미지 = 배포 서버 **hostPath 전용 마운트**, DB 는 경로만(D-29·D-30 등) — 경로 규칙·크기 한도
- 프로필 설정: 프로필 이미지(즉시 저장) · AX 캐릭터 이동(기존 진입점 제거 D-48) · **비밀번호 변경 API 신설** · 이름·직무는 명부 읽기 전용
- 비밀값 env 이름: `GOOGLE_OAUTH_CLIENT_ID/SECRET` · `GMAIL_PUBSUB_TOPIC/SUBSCRIPTION` · `GOOGLE_PUBSUB_SA_KEY_FILE` · `SLACK_CLIENT_ID/SECRET` · `SLACK_APP_TOKEN` + 토큰 암호화 키(이름은 네가 정함) — 값은 쓰지 마라
- UX Contract 는 확정 시안의 화면·상태를 그대로 옮긴다(design-change 판별로 근거)

**SPEC-009 — Mac 카톡 수집기 (Tauri · Rust, 조회만)**
- 백그라운드 상주 · 카톡 실행 여부 · 로그인 계정 = 카톡에 로그인한 계정 · 계정 바뀌면 멈춤(D-45)
- 키: 기기값 + userId → PBKDF2 → SQLCipher, **userId 를 못 찾을 때 복구 방식**(kakao-db-fields DB-1) — **키·DB 경로는 Mac 밖으로 안 나간다**
- 읽기: DB 사본/읽기 전용 열기 원칙 · 방 목록(1:1·단체, 오픈채팅 제외) · 메시지(고른 방만) · 실시간 감지(폴링 간격) · 고른 방 정보는 로컬 저장
- 첨부: 사진·앨범·파일 = 감지 즉시 CDN 에서 받아 서버로 업로드 · 동영상·음성 = 메타만 · 이모티콘 = 표식 · 만료 = 「만료됨」
- 서버 업로드·상태 보고는 SPEC-008 계약을 소비 · 권한(전체 디스크 접근) 안내 · kakaocli 는 **방식만 참고**(Rust 로 직접 — DEC-008 근거), 라이선스 MIT 표기
- Windows 는 범위 밖

## 3. 계약
두 SPEC 사이 계약(업로드·상태)은 SPEC-008 §4 가 정본, SPEC-009 는 참조.

## 4. 먼저 읽을 핵심 파일
§1 순서. 코드는 SPEC-008 §4·§5 를 쓰기 직전에.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` (새로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-009-mac-kakao-collector.md` (새로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/README.md` (표에 두 줄만)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/decision-008-external-channels.md` frontmatter `links.specs` 와 README 의 DEC-008 Spec 칸 **만**
- 그 밖 금지 · 커밋 금지 · 코드 레포 쓰기 금지

## 6. 구현 단계
1. §1 읽기 → 2. 코드 구조 확인(근거 파일:줄 메모) → 3. SPEC-008 → 4. SPEC-009 → 5. 각 SPEC 끝에 「DEC-008 결정 → SPEC 절」 대응표(D-01~D-50 중 이 SPEC 이 받는 것 전부) → 6. README·링크

## 7. 범위 제약
- DEC-008 과 다른 정책 금지 · 2단계(AX 판단)·카톡 발송·알림 메뉴는 Out of Scope 로만
- 실명·실제 URL·토큰 금지 · 운영 도메인은 `ax.medisolveai.xyz` 만(이미 문서에 있음)

## 8. 검증
```
D-01~D-50 이 두 SPEC 대응표 어딘가에 전부(누락 0, 범위 밖은 「해당 없음」으로) · 코드 근거 파일:줄 · 시안 화면·상태가 UX Contract 에 · 열린 것은 SPEC 미결로(번호 OQ-8xx/9xx)
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_3fb95c1b-5d7d-4bcd-8409-b1dba0fbfdea \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
