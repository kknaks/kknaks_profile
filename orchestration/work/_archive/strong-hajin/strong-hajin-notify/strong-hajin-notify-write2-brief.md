# [writer] 알림 2판 — SPEC-011 신설 · SPEC-006/008/009 개정 · WORK-013 신설

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라(앞 판 BASE-009·DEC-010 을 쓴 것이 너일 수도 있지만, 맥락은 파일에서 다시 읽어라):

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 문서 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/project.md` · `P/20-spec/README.md`(SPEC 에 둘 것/두지 않을 것) · `P/30-work/README.md`
- **모양의 본보기**: SPEC = `P/20-spec/spec-010-meeting-ax-enhance.md` · `P/20-spec/spec-008-external-channels.md`(§1 Context ~ §7 Open Questions) · WORK = `P/30-work/work-012-enhance.md`(Meta · 원칙 · Work Summary · Code Surface · Phase 절 · Pre-deploy · Rollback · Done Criteria · Open Issues · Domain/Schema)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga` (코디 워크트리에 직접 탄다)
경로 약어: `P/` = `para/projects/summer-star/strong-hajin/` · `W/` = `orchestration/work/strong-hajin-notify/` · `D/` = `reference/2026-09-10-sc-meeting/package 2/` · 코드 `C/` = `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/`(origin/main `d2a06fa`, **읽기만**)

⚠ **코디와 같은 트리다.** allowed_paths 의 파일만 만든다/고친다.

## 1. SSOT — 계약의 근거 (여기 없는 것은 발명하지 마라)

| 원료 | 경로 |
|---|---|
| **결정 — 정본** | `P/10-decision/decision-010-notifications.md` (D-01~D-35 · 사건 × 관계 표 **사용자 확정 — 전 행** · 열린 OQ 0 · 범위 밖 · WP 묶음 · 실측 필요 · 영향 범위 · 시안 고칠 것) |
| 입력 | `P/00-baseline/baseline-009-notifications.md` |
| 확정 시안 — 화면 정본 | `D/Alerts.html` · `D/handoff/alerts/` · `D/handoff/settings/js/{data.js,settings.v1.jsx}` · `D/handoff/shell/js/nav.js` · 바뀐 기록 `W/design-change-1.md` ~ `design-change-4.md` |
| 현재 코드 — 파일:줄 | `W/be-survey-report.md` · `W/fe-survey-report.md` · 운영 확인 `W/prod-check-1.md` |
| 고칠 기존 계약 | `P/20-spec/spec-006-tauri-wrapper.md`(v0.6.0 · §2.5 · §4 커맨드 표) · `P/20-spec/spec-008-external-channels.md`(v0.6.0 · 사용자 사건 채널 §4.4 · 안 읽음 「내 줄 빼기」) · `P/20-spec/spec-009-mac-kakao-collector.md`(v0.5.1 · 수집기 업로드 모양) |

**기대는 개념** — DEC-010 `up:` 의 개념(server-sent-events · websocket · application-event · per-user-fanout)을 SPEC 의 `up:` 에도 둔다.

## 2. 배경

DEC-010 이 알림의 방향을 정했고 미결도 모두 닫혔다. 이 판은 그것을 **계약(SPEC)과 실행 계획(WORK)** 으로 내린다. 다음은 바로 **구현 발주**다 — WORK 의 Phase 가 그대로 BE·FE 브리프가 된다.

## 3. 만들 것

### 3-1. `P/20-spec/spec-011-notifications.md` 신설 → v0.1.0

알림 자체의 계약:
- **사용자 사건 채널(SSE)** — 하나 · 회원별 · 사건 종류 전부(메시지함 넷 + 알림 + 필요한 것) · 사건 id · 재연결 이어 받기(어디까지 다시 주나 — 알림은 저장되니 다시 준다, 메시지함 신호는 다시 읽기로 메운다는 지금 규칙과의 관계) · 하트비트 · 인증(같은 출처·쿠키) · 프록시 조건(응답 버퍼링 끔 등 — 운영 경로가 nginx + Cloudflare Tunnel 이라는 사실은 `P/70-runbook/runbook-002-production-deploy.md` 에서) · 워커 프로세스 게시 길. **WebSocket `/api/inbox/stream` 은 대체** — SPEC-008 쪽 개정과 짝
- **알림 생성** — DEC-010 사건 × 관계 표를 **조문으로**(사건 · 받는 관계 · 설정 항목 id · 꼬리표 · 문장 모양). 원칙 ①②③ + 예외(D-33) · 관계 우선(담당 > 요청자 > 배정자 > 참조) · 슬랙 채널 합침(방별 · 안 읽은 동안 한 줄 · 멘션·DM 은 안 합침) · 끄면 만들 때 거름 · 지금 알림 생성 1곳 흡수(D-30) · 업무 수신함과 알림은 둘 다, 읽음 따로
- **필요한 판정 재료** — 메일 To/CC 중 나 · 슬랙 멘션 · 「내가 보낸 줄」(슬랙 `raw.user` · 카톡 수집기 표지 · 메일 From = 내 계정) — 저장 칸인가 매번 raw 에서 푸나는 SPEC 이 정한다(근거와 함께)
- **알림 API** — 목록(테마 필터 · 페이지) · 안 읽음 여부(사이드바 점용) · 단건 읽음 · 모두 읽음 · 항목을 누르면 갈 대상(고른 상태까지 — D-31)
- **알림 설정** — 전체 · 테마 셋 · 항목 16(시안 `NOTIFY_GROUPS` id 그대로) · 기본값(시안의 `on`) · 저장 자리 · API
- **화면** — 알림 목록(시안 그대로 · 상태 넷) · 사이드바 점 둘(알림 · 메시지함 — 무엇이 점을 켜고 끄나) · 설정 알림 탭 · 스위치 부품(DS 에 없음 — 어디에 세우나)
- **셸 시스템 알림** — 웹 → 셸 커맨드(이름·인자·origin 허용) · 권한 요청 시점 · 앱이 켜져 있을 때만 · 클릭 → 셸 → 웹 이동 사건(고른 상태까지) · 개인판/medi-ax 판 차이 · 무엇을 시스템 알림으로 띄우나(목록에 쌓이는 것 전부인가 — DEC 에 없으면 OQ)
- **기존 카톡 백필(D-35)** — 일회성 수동 마이그레이션 vs 수집기 재전송 **택일**: `C/` 의 카톡 업로드 경로(`kakao_ingest.py`)가 같은 `logId` 를 다시 받으면 덮어쓰나 버리나를 **읽어서** 근거로 정한다. 사람 이름을 코드·문서에 박지 않는다
- §4 Interface Contract 는 바뀌는/새 API·필드·오류·사건만. 스키마는 WORK 의 Domain/Schema 에

### 3-2. 개정 셋 (지운 문장은 ~~취소선~~ — 지우지 않는다 · 머리 변경 이력에 한 줄)

- `spec-006-tauri-wrapper.md` → **v0.7.0**: §2.5 표의 칸별 — 연다(권한 요청 · 표시 · 이벤트 정의 · 클릭 딥링크) / 그대로(푸시 · 트레이 · 배지) · §4 커맨드 표에 알림 커맨드 · 셸 → 웹 사건에 알림 클릭 → 근거 DEC-010 · SPEC-011
- `spec-008-external-channels.md` → **v0.7.0**: 사용자 사건 채널(§4.4) 을 SPEC-011 의 SSE 로 대체한다는 것 · 메시지함이 그 채널을 받는 모양 · 안 읽음 「내 줄 빼기」 판정을 슬랙 `raw.user`(그리고 카톡 표지)로 — 지금 버그(운영 100% 이름 덮임) 근거
- `spec-009-mac-kakao-collector.md` → **v0.6.0**: 업로드 줄에 「내가 보냄」 표지 · **값의 출처(카톡 로컬 DB 의 무엇인가)는 아직 모른다 — WORK Phase 0 조사로 확정**이라고 적고 OQ 로 둔다(추측 금지) · 백필 방식이 재전송이면 그 절차

### 3-3. `P/30-work/work-013-notifications.md` 신설

- 원칙 절에 고정: **구현은 두 판**(1루프 계약대로 → 사용자 E2E(**데스크톱 앱**) → 2루프) · 완료 = 앱 실물 · 백엔드 커밋 뒤 스택 재시작 · 외부 경로(Gmail · Slack · 카톡 수집기 · OS 알림)는 실물 1회가 완료 조건 · **검증은 Phase 마다 관련 시험만, `make verify` 는 마지막에 한 번**
- **Phase 0 조사**(코드 아님): 카톡 로컬 DB 에 「내가 보냄」 값이 있나(수집기 읽기 경로) · 실측 필요 셋(DEC-010 「실측 필요」) 중 코드 전에 갈라야 하는 것
- **Phase = DEC-010 WP 묶음 순서**: WP1 사건 채널(SSE) → WP2 알림 생성 + 설정 저장 + 판정 재료 + 백필 → WP3 화면 → WP4 셸 시스템 알림(+ 수집기 표지 · dmg). WP 마다 BE·FE 로 나누고 **선후(BE 계약 고정 → FE)** 와 병렬 가능 여부
- **Code Surface — 전수**: 각 Phase 가 닿는 파일을 조사 리포트의 파일:줄로 **전부** 센다. 「고칠 곳 N개」 목록이 아니라 **「같은 심볼·패턴을 쓰는 곳 전부」** 를 grep 해 개수와 함께 적어라 — 예: `user_events.publish` 호출 전부 · `UserEventType` 생성 전부 · `useInboxStream` 쓰는 곳 전부 · 사건 × 관계 표의 사건별 발생 자리 전부 · `NotificationRepository.emit` · `SideNav` 항목 정의 · 셸 커맨드 등록 자리. 빠진 자리가 다음 판 FAIL 이다
- Phase 마다 **검증**(Makefile 타겟 — `C/AGENTS.md`) · **Done Criteria**(앱에서 무엇을 보면 끝인가) · 사용자 E2E 체크리스트(앱)
- Domain/Schema 초안: 알림 표 변경 · 알림 설정 저장 · 외부 메시지 판정 칸(쓴다면) · 사건 id · 마이그레이션(수동 SQL 경로 — `C/migrations/manual/` 방식) · 백필
- Pre-deploy · Rollback(SSE → WS 되돌림 가능성) · Open Issues

## 4. 하지 말 것

- 코드를 고치지 마라(읽기는 된다). DEC 를 고치지 마라 — 결정이 부족하면 SPEC §7 / WORK Open Issues 에 OQ 로 올리고 보고에 적어라(**추측으로 메우지 마라**)
- index(`20-spec/README.md` · `30-work/README.md` · `10-decision/README.md` · `00-baseline/README.md`)·`log.md`·`_RESUME.md`·시안 사본을 고치지 마라 — 코디가 한다
- 운영 서버·DB 접속 금지 · 실명·메일·토큰 금지

## 5. allowed_paths

- `P/20-spec/spec-011-notifications.md` (신설)
- `P/20-spec/spec-006-tauri-wrapper.md` · `P/20-spec/spec-008-external-channels.md` · `P/20-spec/spec-009-mac-kakao-collector.md` (개정)
- `P/30-work/work-013-notifications.md` (신설)

커밋·push 금지.

## 6. 검증

- DEC-010 의 D-01~D-35 와 사건 × 관계 표 **전 행**이 SPEC-011·006·008·009 어느 한 곳에 **빠짐없이** 대응한다 — 대응표(결정 → SPEC 절)를 WORK 부록에 두고 개수를 보고에 적어라
- 시안 설정 항목 16개 id 가 SPEC-011 설정 계약에 그대로 있다
- WORK Code Surface 의 grep 개수표가 있다
- `git -C /Users/kknaks/orca/workspaces/kknaks_profile/beluga status --short` 에 위 다섯 파일만 새로 바뀌었다(`orchestration/work/` · 시안 사본 · BASE-009 · DEC-010 은 원래 있던 변경)

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC-011 · SPEC-006/008/009 개정 · WORK-013" \
  --body "파일 경로 / 결정 대응 개수 / Phase 요약 / grep 개수표 요지 / 백필 택일과 근거 / OQ"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] writer SPEC·WORK 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] writer: <질문>" --enter`
