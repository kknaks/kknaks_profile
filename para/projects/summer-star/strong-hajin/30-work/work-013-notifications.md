---
type: work
id: WORK-013
title: "알림 — 사건 채널(SSE) · 알림 생성과 설정 · 알림 화면 · 셸 시스템 알림 · 카톡 표지"
status: todo
product: strong-hajin
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-10-08
updated_at: 2026-10-08
tags:
  - product/strong-hajin
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-009-notifications|BASE-009]]"
  decisions:
    - "[[decision-010-notifications|DEC-010]]"
  specs:
    - "[[spec-011-notifications|SPEC-011]]"
    - "[[spec-006-tauri-wrapper|SPEC-006]]"
    - "[[spec-008-external-channels|SPEC-008]]"
    - "[[spec-009-mac-kakao-collector|SPEC-009]]"
  works:
    - "[[work-012-enhance|WORK-012]]"
    - "[[work-011-external-channels|WORK-011]]"
  releases: []
  related:
    - "[[runbook-002-production-deploy|RUNBOOK-002]]"
sources:
  - orchestration/work/strong-hajin-notify/_RESUME.md
  - orchestration/work/strong-hajin-notify/be-survey-report.md
  - orchestration/work/strong-hajin-notify/fe-survey-report.md
  - orchestration/work/strong-hajin-notify/prod-check-1.md
---

# 알림 — 사건 채널(SSE) · 알림 생성과 설정 · 알림 화면 · 셸 시스템 알림 · 카톡 표지

DEC-010(accepted · D-01~D-41 · 사건 × 관계 표 사용자 확정 전 행 · 열린 OQ 0)이 정한 알림을 구현한다.
**SPEC-011 v0.2.2**(알림) · **SPEC-006 v0.7.0**(셸) · **SPEC-008 v0.7.0**(메시지함 · 사건 채널 · 안 읽음) · **SPEC-009 v0.6.0**(카톡 수집기 표지)이 계약의 정본이다.

> **초안이다(`status: todo`).** **SPEC 이 정본이다** — 이 WP 와 SPEC 이 다르면 SPEC 이 맞고, 워커는 코디에게 알린다(Open Issues).
> 근거 줄 번호는 조사 시점(코드 origin/main `d2a06fa`) 값이다 — 워커는 **줄이 아니라 심볼로 다시 찾는다**(P-2).
> **Phase 가 그대로 발주 브리프가 된다** — 한 Phase = 한 워커 발주. BE 가 계약을 먼저 고정하고 FE 가 이어받는다.
> SPEC-011 §7 의 미결(OQ-1101 · 1102 · 1104 · 1105 · 1108 · 1109 · 1111)은 **제안대로 구현**하고 사용자 결정이 다르면 2루프에서 고친다. OQ-1103 · 1106 · 1107 · 1110 은 **사용자가 닫았다**(DEC-010 D-36 ~ D-40).
>
> **수정 1(2026-10-08 · 검수 FAIL 3 · WARN 11 + 사용자 결정 넷 — `orchestration/work/strong-hajin-notify/review-spec-work-report.md` · DEC-010 D-36 ~ D-41)** — 무엇이 어디서 닫혔는지는 **부록 3**.

## Meta

- **SPEC (정본)**
  - SPEC-011 **v0.2.2** — §4.1(사건 채널 SSE · v0.2.0 닫힘 처리 · 겹침 창 · v0.2.1 둘째 `ready` = 다시 읽기 · 기준 줄 대체 · 10회 멈춤) · §4.2 · §4.3(사건 × 관계 67행 + M15 · 생성 규칙) · §4.4(설정) · §4.5(알림 API · 대상 · 점 · §4.5-3 메시지함 읽음 → 알림 읽음) · §4.6(셸 커맨드) · §4.7(백필 두 걸음) · §2(화면 · §2.5 OS 알림 줄이기) · AC-01~25 · AC-02b · AC-02c
  - SPEC-006 v0.7.0 — §2.5(칸 열기) · §4 커맨드 여섯 · 「시스템 알림 수용」 절 · AC-T50~52
  - SPEC-008 v0.7.0 — §4.4(v0.7.0) 사건 채널 대체 · 안 읽음 `from_me` · §4.6 `from_me` · §2.7 · AC-35~37
  - SPEC-009 v0.6.0 — §3.1 · §4 업로드 표지 · OQ-K01 · AC-11 · AC-12
- **Decision**: DEC-010 · **Baseline**: BASE-009
- **코드(읽기만 — 조사 기준)**: `Strong_hajin` origin/main `d2a06fa` · 구현 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify`(branch `kknaksss/strong-hajin-notify`)
- **조사**: `orchestration/work/strong-hajin-notify/be-survey-report.md`(BE §n) · `fe-survey-report.md`(FE §n) · `prod-check-1.md`(운영 DB 읽기)
- **확정 시안**: `reference/2026-09-10-sc-meeting/package 2/` — `Alerts.html` · `handoff/alerts/` · `handoff/settings/js/{data.js,settings.v1.jsx}` · `handoff/shell/js/nav.js`
- **운영**: RUNBOOK-002 · origin `https://ax.medisolveai.xyz`(Cloudflare → cloudflared → ingress-nginx) · 데스크톱 앱 medi-ax

**경로 약어** — `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/` · `T/` = `frontend/src-tauri/src/` · `BT/` = `backend/tests/`.
줄 약어는 BE 리포트 그대로(`WT` · `APP` · `REQ` · `ASG` · `BA` · `HIN` · `SS` · `SYNC` · `INB` · `IS`).

## 이 판의 원칙

| # | 원칙 | 근거 |
|---|---|---|
| P-1 | **구현은 두 판이다.** **1루프** = 계약대로 전 Phase 구현 → **사용자 E2E(데스크톱 앱)** → 지적을 **모아서 한 번에** 받아 **2루프**. E2E 도중 단건 발주를 하지 않는다 | `feedback_batch_e2e_feedback` |
| P-2 | **쓰는 곳을 전부 센다.** 아래 Code Surface 의 줄은 출발점 — 같은 심볼·패턴을 **grep 으로 전부** 다시 세고 시작한다. 「고칠 곳 N개」 가 아니라 「그 심볼을 쓰는 곳 전부」. 수가 다르면 코디에게. 빠진 자리가 다음 판 FAIL 이다 | `feedback_brief_enumerate_not_list` |
| P-3 | **완료 = 앱 실물.** 사용자는 **데스크톱 앱만** 쓴다 — 운영 웹에서 된다는 것은 서버 쪽 근거일 뿐이다(DEC-010 D-03) | `feedback_done_on_user_surface` |
| P-4 | **백엔드를 커밋하면 스택을 재시작한다**(`make local-stack` 재기동 · 워커 포함). 옛 코드가 떠 있으면 「프론트가 안 된다」 로 보인다 — **특히 사건 채널 교체(WP1)는 옛 back 이 떠 있으면 SSE 가 404** | `feedback_restart_stack_after_commit` |
| P-5 | **외부 경로는 실물 1회가 완료 조건** — Gmail(메일 수신 → 알림 · From/To/CC 판정) · Slack(DM · 멘션 · 채널 합침 · 내가 보낸 줄) · 카톡 수집기(표지) · **OS 알림(macOS 실기 · 서명 dmg)** · **운영 경로 SSE(Cloudflare → ingress)** | `feedback_real_e2e_before_done` |
| P-6 | **운영과 같은 조건으로 확인한다** — SSE 버퍼링 · 유휴 끊김은 **https 운영 origin** 에서만 드러난다(로컬 vite 프록시는 Cloudflare 를 지나지 않는다) · OS 알림은 **서명 dmg** 에서 | `feedback_verify_prod_scheme` |
| P-7 | **워커는 사용자 포트·프로세스를 건드리지 않는다.** 앱 실물 · 운영 확인 · 운영 SQL 은 코디 몫 | `feedback_real_e2e_before_done` |
| P-8 | **검증은 Phase 마다 관련 시험만 — 전체 스위트 금지, `make verify` 는 마지막에 코디가 한 번.** 백엔드는 **늘 Makefile 타겟으로**(코드 레포 `AGENTS.md` 「백엔드 테스트는 항상 Makefile 타겟으로 — 직접 호출하지 않는다」 · 재검수 R-W2) 범위만 좁힌다: ① **파일 지정(직렬)** `make test-contract-serial FILES="tests/unit/x.py tests/contract/y.py"` — `pytest $(FILES) -n0`(Makefile:86-91)이라 단위 · contract 파일 모두 된다 ② **병렬 + 이름 거르기** `PYTEST_ADDOPTS='-k "<표현>"' make test-contract`(Makefile:76-79 — 직렬 패스가 고를 것이 없으면 5 를 삼킨다) ③ **Postgres** `PYTEST_ADDOPTS='<파일 또는 -k>' POSTGRES_TEST_URL=… make test-postgres`. **`make test-unit` · `make test-contract` · `make test-postgres` 를 거르지 않고 통째로 돌리지 않는다 · `uv run pytest` 직접 호출 금지.** 프론트는 **고른 파일만** `cd frontend && npx vitest run <파일들> --no-file-parallelism`(로컬 스택이 떠 있는 기계 — 병렬 vitest 가 스택을 죽인 전례) · 스택이 없는 워커 기계면 `--no-file-parallelism` 없이 병렬 가능 · 타입은 `make frontend-build`. **셸은 cargo feature 두 벌** — `cd frontend/src-tauri && cargo test`(strong-hajin · feature 없음) **와** `cargo test --features kakao-collector`(medi-ax · 카톡 시험은 이것으로만 돈다 — `kakao/mod.rs:27` · Makefile:151) | `feedback_verify_scope_per_phase` · 검수 W-5 · r2 R-W2 |
| P-9 | **시안 · DS 안에서** — 알림 화면은 시안 CSS(`alerts.css`)를 옮겨 쓰고 DS 부품(Badge · SegmentedControl · Skeleton · StatusNote · Icon)으로. 스위치는 설정 부품에(SPEC-011 §2.3) | WORK-012 P-8 |
| P-10 | **실명 금지** — 카톡 백필의 본인 이름은 **실행 인자**로만. SQL 파일 · 코드 · 문서 · 커밋 · 시험 픽스처에 쓰지 않는다(DEC-010 D-35) | 사용자 지시 |

## Work Summary

**Phase 순서 = DEC-010 WP 묶음 순서**(WP1 → WP2 → WP3 → WP4) 앞에 **Phase 0 조사**. 각 WP 는 **BE → FE**(BE 가 계약을 고정해야 FE 가 붙는다).

| Phase | 워커 | 무엇 | SPEC | 시작 조건 | 병렬 |
|---|---|---|---|---|---|
| **P0** 조사(코드 아님) | 코디 + 사용자 Mac · frontend(셸 문서 읽기) | 카톡 로컬 DB 「내가 보냄」 재료(OQ-K01) · 데스크톱 알림 플러그인의 클릭 콜백 · 권한 · 서명 영향 | S9 OQ-K01 · S11 OQ-1108 · S6 「시스템 알림 수용」 실측 | SPEC 검수 PASS | WP1 과 나란히 |
| **WP1-BE** 사건 채널(서버) | backend | SSE `GET /api/events/stream` · 사건 id · 이어 받기 · `resync` · 하트비트 · 401/403 · 큐 넘침 `resync` · 알림 사건 NOTIFY 페이로드(짧게) · 워커 게시 길(meeting_worker) | S11 §4.1 · S8 §4.4(v0.7.0) | SPEC 검수 PASS | P0 와 |
| **WP1-FE** 사건 채널(화면) | frontend | 앱 전역 EventSource 하나 · `useInboxStream` 을 전역 구독으로 · `resync` 다시 읽기 · **닫힘 처리(CONNECTING 은 브라우저 · CLOSED 는 `GET /api/auth/me` → 401 이면 세션 상실 / 아니면 백오프 새 연결 `?last_event_id=`)** · (id · 순번) 중복 거르기 · WS 연결 코드 걷기 | S11 §4.1-3 · §4.1-6 · S8 AC-35 | WP1-BE 계약 고정 | — |
| **WP2-BE** 알림 생성 + 설정 + 판정 재료 + 백필 | backend | 알림 표 칸 · 생성기 하나 · **사건 자리 전부(68행 — 67 + M15)** · 원칙 셋 + 예외 · 관계 우선 · 슬랙 합침 · 설정 저장·API · `from_me`(저장 때) · 안 읽음 셈 · 카톡 업로드 `from_me` · 알림 API(목록·요약·읽음·모두 읽음·badges·target) · 읽기 인가 변경 · 흡수(WT:2116) · 백필 SQL | S11 §4.2 ~ §4.5 · §4.7 · S8 §4.4 · §4.6 | WP1-BE 머지(알림 사건이 채널에 실린다) | WP1-FE 와 나란히 |
| **WP3-FE** 화면 | frontend | 알림 목록 화면(`surface="notifications"`) · 자동 이어 불러오기 · [모두 읽음] = 전부 · 사이드바 점 둘 · 설정 알림 탭 + Switch · 클릭 이동(target → 포커스) · 문장 함수(labels) | S11 §2.1 ~ §2.3 · §4.5 | WP2-BE 계약 고정 · WP1-FE 머지 | — |
| **WP4-SHELL** 셸 시스템 알림 + 수집기 표지 | frontend(셸) | 알림 플러그인 · 커맨드 둘 · capability · 클릭 사건 · `shell_info.features` · 웹 다리(`F/lib/shell.ts`) · 새 알림 → `notify_show`(**보고 있으면 생략 · 합친 줄은 처음만 · 10초에 넷 이상이면 「새 알림 N건」** — D-39) · `build.rs` ACL 매니페스트 · `Cargo.toml` 의존 · 권한 묻기 · **카톡 수집기 `from_me`**(P0 결과대로) · dmg 1회 | S6 v0.7.0 · S11 §2.5 · §4.6 · S9 v0.6.0 | WP3-FE 머지 · P0 결과 | — |
| **반영** | 코디 | 1루프 E2E(앱) → 2루프 → 운영(SQL · ingress 주석 · 이미지 — **back · front · 워커 다섯(conversation · material · meeting · report · external)** · dmg · 백필 SQL 두 걸음) | — | 전 Phase | — |

**같은 파일을 여는 워커를 동시에 태우지 않는다.** BE 는 한 워커가 WP1 → WP2 순서로 간다(`user_event_hub.py` · `http_inbox.py` · `bootstrap/application.py` 를 둘 다 연다).
FE 는 `App.tsx`(WP1-FE 전역 연결 · WP3-FE 화면·점·이동 · WP4 셸 다리) · `labels.ts` · `SettingsPage.tsx` 가 겹친다 — **WP1-FE → WP3-FE → WP4-SHELL 직렬**.

---

## Code Surface — 전수 grep 개수표

코디가 `rg` 로 다시 셌다(2026-10-08 · `d2a06fa` · `node_modules`·lock 제외). **prod** = 제품 코드(줄/파일), **test** = 시험 파일(줄/파일).
워커는 시작할 때 **같은 패턴으로 다시 센다** — 수가 다르면 코디에게.

### WP1 — 사건 채널

| 무엇 | 패턴(rg) · 범위 | prod | test | 바뀌는 자리 / 건드리지 않는 자리 |
|---|---|---|---|---|
| 게시 호출 | `user_events\.publish` · `B/` | **9 / 6** | 1 / 1 | `platform/external_channels_sync_store.py:225,232,255,369` · `platform/external_channels_inbox_store.py:508` · `platform/external_channels.py:154` · `bootstrap/application.py:1796` · `platform/user_event_hub.py:3`(docstring) · **`bootstrap/external_inbox.py:251` 은 워커 깨우기 채널(`SYNC_WAKE_CHANNEL`) — 건드리지 않는다**. 게시 함수(`platform/user_events.py:12-16`)는 그대로 쓰고 **알림 생성기 · meeting_worker 가 새로 부른다** |
| `pg_notify` | `pg_notify` · `B/` | 1 / 1 | 0 | `platform/user_events.py:16` — 그대로 |
| 사건 만들기 | `UserEventType\.` · `B/` | **12 / 6** | 13 / 2 | 정의 밖 생성 11: `modules/external_channels/inbox.py:938,1065` · `application.py:336,652` · `kakao_ingest.py:258,324` · `platform/external_channels_sync_store.py:222,229,251,366` · `bootstrap/application.py:1790` + 묶기 판단 `platform/user_event_hub.py:89`. **사건 이름 · 필드는 바꾸지 않는다**(S8 v0.7.0) — 알림 사건 종류만 `modules/external_channels/events.py`(또는 새 자리)에 더한다 |
| 사건 종류 정의 | `class UserEventType\|MESSAGE_ARRIVED\|REPLY_RESULT\|INTEGRATION_CHANGED\|MESSAGE_UPDATED` · `B/` | 17 / 7 | 13 / 2 | `modules/external_channels/events.py:30-39` — `notification.upserted` · `notification.read` 더함(정의 자리는 구현 — 「메시지함 전용」 이 아님을 docstring 에) |
| 채널 상수 | `USER_EVENTS_CHANNEL` · `B/` | **20 / 7** | 2 / 1 | 정의 `events.py:23` · import·사용 `inbox.py:37,936,1063` · `application.py:43,335,651` · `kakao_ingest.py:33,256,322` · `bootstrap/application.py:225,1796` · `user_event_hub.py:25,137`(LISTEN) · `sync_store.py:18,225,232,255,369` — **값 그대로**(`ax_user_events`) |
| 듣는 쪽 | `UserEventHub\|user_event_hub` · `B/` | 8 / 3 | 8 / 4 | `platform/user_event_hub.py`(전체 — 큐 200 `:28` · 묶기 `:94-116` · 넘침 버림 `:148-154` → **넘침 때 그 연결에 `resync` 표시**) · 조립 `bootstrap/application.py` · `bootstrap/external_inbox.py:144-147`(시험 DB dispatch) |
| WS 라우트 | `@app\.websocket` · `B/` | 2 / 2 | 0 | **`entrypoints/http_inbox.py:338-396`(메시지함 WS) — 화면이 더 쓰지 않는다 · 라우트는 이 판에 남긴다(Rollback)** · `entrypoints/http.py:1245`(회의 WS) — **건드리지 않는다**(D-11) |
| SSE 없음 | `StreamingResponse\|EventSourceResponse\|text/event-stream` · `B/` | **0** | 0 | 새 라우트 `GET /api/events/stream`(`entrypoints/http_inbox.py` 옆 또는 새 파일 — 라우트 등록 시험 `BT/contract/test_production_route_registration.py` 갱신) |
| 같은 출처 · 인증 | `_same_origin\|connection_principal\|CLOSE_UNAUTHORIZED\|CLOSE_FORBIDDEN_ORIGIN` | — | — | `http_inbox.py:346-353` 의 검사를 SSE 로 옮긴다(401 · 403 — 닫힘 코드가 아니라 HTTP 상태) · `entrypoints/http_auth.py:82-101` |
| 화면 연결 | `useInboxStream\(` · `F/` | **3 / 3** | 0 | 정의 `features/inbox/inboxStream.ts:16-69` · 쓰임 `features/inbox/InboxPage.tsx:157` · `features/settings/SettingsPage.tsx:182` → **전역 연결 구독**으로(쓰는 두 화면의 인자 모양은 유지 가능) |
| 소켓 만들기 | `new WebSocket` · `F/` | 2 / 2 | 0 | **`features/inbox/inboxStream.ts:32` → EventSource 로** · `features/meetings/stream.ts:103`(회의) — **건드리지 않는다** |
| 주소 | `inboxStreamUrl` · `F/` | 3 / 2 | 0 | `lib/api.ts:1753-1757` → 사건 채널 주소 함수로(`ws(s)://` 가 아니라 같은 origin `https://…/api/events/stream`) |
| 나눠 주기 | `createInboxEventHub\|hub\.subscribe\|hub\.emit` · `F/` | 8 / 4 | 2 / 1 | `inboxStream.ts:72-88` · `InboxPage.tsx:153` · 듣는 자식 `MailView.tsx:294` · `RoomView.tsx:460,526,646` — 전역 허브로 옮기거나 InboxPage 허브가 전역을 받아 그대로 나눈다(구현 선택 · 자식 넷은 바뀌지 않게) |
| 사건 타입 | `InboxStreamEvent` · `F/` | 9 / 3 | 0 | `lib/viewModels.ts:1688-1699` — 그대로 + 알림 사건 타입 더함 |
| 메시지함 사건 이름 | `inbox\.message_arrived\|inbox\.reply_result\|integration\.changed\|inbox\.message_updated` · `F/` | 14 / 6 | 13 / 2 | 이름 그대로 — 받는 길만 바뀐다 |
| 재연결 다시 읽기 | `onReconnect` | — | — | `inboxStream.ts:37-40` · `InboxPage.tsx:157` · `SettingsPage.tsx:186` → **`resync` 사건**으로 |
| 세션 상실 | `onSessionLost` · 4401 | — | — | 회의 스트림의 4401 처리 `features/meetings/stream.ts:89-92` · `App.tsx:522-526` 와 같은 길로 SSE 401 |
| WS 시험 대역 | `stubGlobal\("WebSocket"` | 0 | **9**(FE N+1) | WS 대역을 쓰는 시험 — `App.test.tsx` · `InboxPage.test.tsx` · `SettingsPage.test.tsx` · `SettingsLanding.test.tsx` · `MeetingLive.test.tsx`(회의 — 그대로) 등. **메시지함·설정 시험은 EventSource 대역으로** 바꾼다 |
| BE 시험 | `inbox/stream\|test_user_event_hub` | — | `BT/contract/test_external_inbox.py`(WS :541·543·559·602·658·661) · `BT/contract/test_kakao_ingest_and_profile.py`(WS :187·200) · `BT/unit/test_user_event_hub.py` · `BT/integration/postgres/test_external_channels_postgres.py` | SSE 시험으로 옮긴다(사건 모양 · 회원 거르기 · 이어 받기 · `resync` · 401/403 · 하트비트) |
| 게시 프로세스 — 새로 | `meeting_worker` · `commit_finalized` · `finalize_failed` | — | — | `bootstrap/meeting_worker.py:1-5`(DB 만 쓴다) → 회의록 완료(`modules/meetings/application.py:886-970`) · 실패(`:972-980`)가 생성기를 부르면 같은 트랜잭션 NOTIFY. **conversation_worker 에서 업무 사건이 나는지**(AX 실행 경로 — `BA:1790` 이 어느 프로세스인지 BE §9 미확인)는 WP2-BE 첫날 확인 |

### WP2 — 알림 생성 · 설정 · 판정 재료 · 백필

| 무엇 | 패턴(rg) · 범위 | prod | test | 자리 |
|---|---|---|---|---|
| 지금 생성 자리 | `\.emit\(` · `B/` | **1 / 1** | 0 | `platform/work_tasks.py:2116`(`append_audit` 안 · 조건 `:2106` · 받는 사람 `:2109`) → **생성기 호출로**(D-30) |
| 알림 저장소·앱 | `SqlAlchemyNotificationRepository\|NotificationRecord\|NotificationApplication` · `B/` | 27 / 6 | 2 / 1 | 모델 `platform/persistence.py:1299-1321` · 저장소 `platform/notifications.py:18-80` · 앱 `modules/notifications.py:30-83` · 조립 `BA:2460-2471` · 정의만 `BA:2473-2492`(`_authorized_notification_view` — 호출 0 · **하나로 정리**) |
| 알림 API · 도구 | `list_notifications\|mark_notification_read\|notification_mark_read\|notification\.mark_read` · `B/` | 23 / 6 | 9 / 2 | HTTP `entrypoints/http.py:1381-1392`(+ 404 매핑 `:528`) · MCP `mcp.py:622-627,1348-1349,1607-1608,1929-1930` · 도구 설명 `modules/ax_execution/tool_catalog.py:57,231-234` · 명령 계약 `command_contracts.py:120` · 실행 `platform/actions.py:832-834,1703-1707` — **응답 모양 갱신 · 새 경로(목록 쿼리 · summary · read-all · badges)** |
| 운영 인벤토리 | `notifications` · `docs/unified-operations-inventory.json` | 16줄 | — | `:650-666` · `:1860-1879` · `:8450-8572` + 새 경로 — drift 시험 `BT/architecture/test_operation_inventory.py` |
| 감사 훅 | `append_audit\(` · `B/` | **37 / 5** | 0 | `modules/meetings/application.py` 21 · `modules/work/requests.py` 12 · `platform/actions.py` 2 · `platform/meetings.py` 1 · `platform/work_tasks.py` 1 — **알림 행은 감사 훅이 아니라 사건 자리에서 부른다**(관련자를 아는 자리) |
| 「알림의 자리」 | `알림의 자리` · `B/` | 2 / 1 | 1 / 1 | **`modules/work/application.py:1581`(선행 해제 — 연다 · W35)** · `:741`(이동 — **그대로 부르지 않는다** · W21) · 시험 `BT/contract/test_task_successors.py:495-515`(「`emit` 0」 기대 → **W35 는 1 로 바뀐다**) |
| 업무 사건 자리 — 요청 | `def (create\|accept\|reject\|negotiate\|amend\|resubmit\|withdraw\|add_comment)` in `modules/work/requests.py` | 8 | — | `:334`(W01·W02~04) · `:486`(W05) · `:509`(W05) · `:534`(W07) · `:564`(W08) · `:650`(W09) · `:702`(W10) · `:1122`(W36 — 독자 `party_of :1183-1197`) |
| 업무 사건 자리 — 담당 | `def (assign\|accept\|cancel)…` in `modules/work/assignments.py` + `WT` | — | — | 직접 배정 `ASG:106`·`WT:2525-2590`(W12) · 넘김·변경 제안 `ASG:188-229`·`WT:2428-2456,2664-2702`(W13·W14) · 수락 `ASG:258-272`·`WT:2707-2793`(W15) · 거절 `ASG:306-322`(W15) · 철회 `ASG:331-347`(W16 — 알림 없음) |
| 업무 사건 자리 — 업무 | `APP` = `modules/work/application.py` | — | — | 수정 `:542-625`(W17~W20 — 기한·시작일만 · `before`/`after`) · 이동 `:666-745`(W21 없음) · 하위 `:524-528`(W22 없음) · 상태 전이 `:2037-2118`(W23 없음 · **취소 W24** `:2120`) · 완료 보고 `:1883-1926`(W25) · 승인 `:1933-1944`(W27 없음) · 보완 `:1946-1964`(W28) · 재개 `:2140-2196`(W29·W30) · 제안 열기 `:2200-2228`(W31·W32) · 응답 `:2230-2283`(W33) · 철회 `:2285-2309`(W34 없음) · 합의 `:2329-2366`(W33) · 선행 해제 `:1565-1619`(W35) · 체크리스트 등 `:2571-2697`(W37 없음) |
| 업무 원장 기록 | `\.record\(` in `modules/work` · `platform/work_tasks.py` | 20 | — | 사건 자리 전수 대조용 — 위 표에 없는 `record` 가 있으면 W 행 중 어디인지 코디에게 |
| 회의 사건 자리 | `modules/meetings/application.py` | 감사 21 | — | 생성 `:302-339`(M01~03) · 수정·참석자 교체 `:481-540`(`replace_attendees :531` — M04~06 · **들어온/빠진 사람 셈이 필요**) · 취소 `:591-603`(M07) · 시작·종료 `:630,644`(M08 없음) · 완료 `:886-970`(M09·M10 — **meeting_worker**) · 실패 `:972-980`(M11) · 공유 **두 길** — `share_many :1112-1133` · **`share :1179-1199`**(감사 `:1198` · 부르는 곳 HTTP `BA:2448` · AX 실행 `BA:4501`)(M12 — 검수 F-2 ①) · 회수 ~~`:1179-1223`~~ → **`revoke_share :1201-1223`**(M13 없음) · **공개 전환 `apply_legacy_visibility :1135-1177`**(`add_legacy_public_share` · 회의 수정 경로 `BA:4320-4336` — **M15 알림 없음** · D-38 · F-2 ②) — 공개 전환 경로가 공유 알림을 부르지 않는 것을 시험으로 고정 |
| 메시지 저장 자리 | `def save_messages\|def handle_slack_event\|def _save_slack\|def slack_fanout_targets` · `B/` | 6 | — | 메일·슬랙 저장 `platform/external_channels_sync_store.py:152-214`(실시간/백필 가르기 — `_announce :204-220`) · 슬랙 팬아웃 `modules/external_channels/sync.py:142,249-284,460-485`(이름 덮기 `:484-485`) · 카톡 `modules/external_channels/kakao_ingest.py:186-269` — **저장 때 `from_me` · 실시간 줄만 알림(OQ-1101)** |
| 끊김 · 접근 잃음 | `mark_disconnected\|_mark_disconnected\|access_lost` · `B/` | 10 + | — | `platform/external_channels_sync_store.py:295-317`(접근 잃음 — X11) · `:349-361`(`mark_disconnected` — X10) · `modules/external_channels/inbox.py:1054-1069`(API · X10) · 카톡 꺼짐 `domain.py:124-148`(X12 — 없음) |
| 안 읽음 「내 줄 빼기」 | `author != ` · 메일 안 읽음 | **1 / 1** + 메일 넷 | 0 | **방**: `platform/external_channels_inbox_store.py:197-199` → `from_me is not true`(슬랙 · 카톡) · **메일(검수 F-2 ③ — 따로 센다)**: `IS:112-118` `mail_page(unread_only)` · `IS:130` 부근 `mail_unread_count` · `modules/external_channels/inbox.py:503`(레일 `counts["mail"]`) · `:525`(줄 `unread`) — **넷 모두 `from_me = true` 메일 제외** · 레일 숫자 · badges 같은 셈 |
| 메시지함 읽음 → 알림 읽음(D-37) | `markInboxMailRead\|markInboxRoomRead\|read-all` · 서버 읽음 라우트 | — | — | 서버: `POST /api/inbox/mail/{id}/read` · `…/rooms/{id}/read` · `/api/inbox/read-all`(`entrypoints/http_inbox.py` · `modules/external_channels/inbox.py` 의 읽음 자리 — 워커가 심볼로 전수) → 같은 트랜잭션에서 메시지 알림 줄 읽음 + `notification.read` · 화면: `F/features/inbox/InboxPage.tsx:180-208` · `F/lib/api.ts:1676,1681` — 읽음 뒤 badges 다시 읽기 |
| 카톡 업로드 모델 | `class KakaoMessageInput` | 1 | — | `modules/external_channels/kakao_ingest.py:69-` — `extra="allow"` 라 지금도 여분 키는 raw 에 남는다 · **`from_me: bool \| None` 을 명시 필드로** · 저장 때 칸으로 · 이미 있는 `logId` 건너뛰기(`:201-208`)는 **그대로** |
| 회원 설정 | `assistant_character_preferences\|AssistantCharacterPreference` · `B/` | 16 / 4 | 5 / 3 | 본보기(회원별 한 벌 · `version`) — 알림 설정 저장은 **새 표**(Schema) |
| 「알림을 내지 않는다」 문구 | `알림을 보내지 않\|회의 공유는 알림` 류 | — | — | `B/modules/ax_execution/tool_catalog.py:446`(회의 공유 도구 설명) · `F/lib/labels.ts:1062` · `F/lib/api.ts:1458` · `F/features/meetings/ShareModal.tsx:22` · 코드 레포 `docs/unified-operations.md:57,85,113` — 이 판으로 고친다(문서는 코디) |
| 시험 — 알림 | `notification` · `BT/` | — | **5 파일** | `BT/contract/test_notifications.py` · `test_personal_command_tools.py` · `test_unified_queries.py:49` · `test_task_successors.py:495` · `BT/architecture/test_local_stack_targets.py:32-33` |

### WP3 — 화면

| 무엇 | 패턴(rg) · 범위 | prod | test | 자리 |
|---|---|---|---|---|
| 알림 API 함수 | `getNotifications\|markNotificationRead` · `F/` | **2 / 1**(정의만) | 0 | `lib/api.ts:726-732` — 쿼리 · summary · read-all · badges 더함 |
| 알림 타입 | `type Notification\b\|Notification\[\]\|<Notification>` · `F/` | 5 / 2 | 0 | `lib/viewModels.ts:1024-1037` → SPEC-011 §4.5-2 모양 |
| 화면 종류 | `type ProductSurface` | 1 | — | `lib/viewModels.ts:1` 에 `"alerts"` · App 조건부 렌더(`surface === "…"` 12줄 · `App.tsx`) |
| 사이드바 | `utilityItems\|visibleNavigation\.map` · `F/` | 8 / 2 | — | `App.tsx:441`(주 메뉴 매핑 — **`dot` 넘김**) · `:447-460`(알림 줄 — `disabled` 걷고 `dot` · `onActivate`) · `shell/SideNav.tsx:25-43,50,73,90-93,103-109,183-184` — 부품은 그대로 · 시험 `shell/AppShell.test.tsx:65-66`(disabled 단언 → 바뀜) |
| 점 | `dot\?:\|scax-nav-item__dot\|\bdot:` · `F/` | 4 / 3 | 0 | `SideNav.tsx` · `styles/shell.css:121-122` — 그대로 |
| 설정 탭 | `notifyOutOfScope\|id: "notify"\|"notify"` · `F/` | 6 / 2 | — | `features/settings/SettingsPage.tsx:31,36,51,62-76` · `lib/labels.ts:1607-1609` · 콜백 쿼리 `App.tsx:73-74` · 시험 `SettingsPage.test.tsx:355-358`(disabled 단언 → 바뀜) · `SettingsLanding.test.tsx` |
| 스위치 | `scax-switch\|role="switch"` · `F/` | **8 / 1**(CSS 만) | 0 | CSS `styles/settings.css:57-65` · 부품 0 → `features/settings/settingsParts.tsx` 에 `Switch` |
| 포커스 이동 | `focusTaskId\|focusWorkRequestId\|focusMeetingId\|focusProjectId\|inboxFocus` · `F/` | **42 / 5** | 6 / 2 | `App.tsx:87-121` — 알림 `target` → 이 상태 · **`onOpenResource`(22 / 4 · `App.tsx:694-754`)와 같은 함수** — 메시지함 포커스 모양(`inboxFocus`)에 `message_id` 강조가 있는지 확인(SPEC-008 §2.9 ④ 출처 링크와 같은 길) |
| 토스트 | `putNotice\(` · `F/` | 5 / 1 | 0 | `App.tsx:137-150` — 「열 수 없는 항목입니다」 · 설정 저장 실패 |
| 메시지함 안 읽음 | `unread_counts\|unread_count` · `F/` | 11 / 3 | 5 / 2 | 셈은 서버 — 화면은 그대로 · 메시지함 점은 badges |
| 시안 옮기기 | `handoff/alerts/{js/alerts.v1.jsx, css/alerts.css}` | — | — | `RELATIONS`(꼬리표 16) · `THEMES` · `EMPTY_BY_FILTER` 문구 · 날짜 구분 |

### WP4 — 셸 · 수집기

| 무엇 | 패턴(rg) · 범위 | prod | test | 자리 |
|---|---|---|---|---|
| 커맨드 등록 | `generate_handler` · `T/` | 2 | — | `lib.rs:687`(medi-ax 7) · `:697`(strong-hajin 4) → **9 · 6** |
| **ACL 매니페스트(검수 F-2 ④)** | `AppManifest::new().commands` · `src-tauri/build.rs` | 1 | — | **`build.rs:138-160`** — 웹에 여는 커맨드 목록(기본 넷 + 카톡 셋)이 `allow-*` 권한을 만든다 → **`notify_permission` · `notify_show` 를 넣지 않으면 capability 의 `allow-notify-*` 가 없는 권한이 되어 빌드가 서지 않는다** · 주석 「기본 넷 … 일곱」 갱신 |
| **의존(검수 F-2 ④)** | `tauri-plugin-*` · `src-tauri/Cargo.toml` | 1(`:35` opener) | — | 알림 플러그인 의존을 `Cargo.toml:35` 옆에(두 판 공통 — feature 아님) · `package.json` 의 `@tauri-apps/*` 는 웹이 플러그인 JS 를 직접 부르지 않으므로(커맨드는 우리 것) **더하지 않는다** |
| 플러그인 | `\.plugin\(` · `T/` | **1** | — | `lib.rs:613`(opener) + 알림 플러그인 |
| capability | `"permissions"` in `flavors/*/capabilities/product-shell.json` | 2 파일 | — | `flavors/medi-ax/…`(7) · `flavors/strong-hajin/…`(4) → `allow-notify-permission` · `allow-notify-show` · 시험 `lib.rs` 「웹에_여는_커맨드가_판에_맞다」 등(`:844-930` 부근) |
| 기능 목록 | `features: \[` · `"features"` · `T/lib.rs:210` | 1 | — | `["wake_guard","open_external"]` + `"notification"` |
| 셸 → 웹 사건 | `window\.eval` · `notify_download` · `T/` | **1** | `download.rs` 「사건_이름이_웹_수신부와_같다」 `:725-731` | `lib.rs:350-362` 와 같은 결로 알림 클릭 사건 + 이름 일치 시험 |
| 창 앞으로 | `show\(\)\|set_focus` · `T/` | `kakao/tray.rs:52-54`(트레이 「열기」) | — | 알림 클릭 때 `main` 창 보이기 · 포커스 |
| 웹 셸 다리 | `invoke\(\|invoke<` · `F/` | **2 / 2** | 2 / 2 | `lib/shell.ts:96-100`(유일한 제품 자리) · `dev/probeShell.ts:37-44`(탐침 — 건드리지 않음) |
| 셸 판별 | `hasShell\(` · `F/` | 12 / 5 | 4 / 3 | `lib/shell.ts:64-72` — 그대로 |
| 사건 수신 본보기 | `onShellDownload\|SHELL_DOWNLOAD_EVENT\|strong-hajin:download` · `F/` | 10 / 3 | 9 / 3 | `lib/shell.ts:216-243` 와 같은 결로 `onShellNotificationClick` |
| Info.plist · Entitlements | `src-tauri/Info.plist` · `Entitlements.plist` | 키 1 · 1 | — | 알림 키 필요 여부는 P0 · WP4 실측 |
| 카톡 수집기 | `T/kakao/{db.rs, client.rs, collector.rs}` | — | `db.rs` 시험 · `client.rs` 시험(`:415,431` — 픽스처 이름은 가상) | 내 userId `db.rs:127-131` · 메시지 조회 `:236-286`(`authorId` 조인 `:245` — 지금은 이름만 뽑는다) · 업로드 모양 `client.rs:15-23,282-284` → **`from_me`**(P0 결과대로 — OQ-K01) · `RawMessage`(`db.rs:52`) |
| 셸 Makefile | `shell-verify\|shell-build\|tauri-local\|shell-final-preflight` | — | — | `Makefile` — dmg(서명) 1회 |

### 개수 요지

| 축 | 값 |
|---|---|
| 사건 × 관계 행 | **67**(W 38 · X 15 · M 14) — 「알림」 행 **40** · 「없음」 행 **27** · *(수정 1)* + **M15**(공개 전환 — 없음 · D-38) = **68** |
| 알림 종류(`kind`) | **19** |
| 설정 항목 | **16**(업무 8 · 메시지 3 · 회의 5) |
| 지금 알림 생성 자리 | **1**(`WT:2116`) |
| 게시 호출 | **9 / 6 파일**(그중 워커 깨우기 1 제외) |
| 운영 워커 · 이미지 | **back + 워커 다섯**(conversation · material · meeting · report · **external** — RUNBOOK-002 :42 · :163-166). 메일 · 슬랙 저장(X01~X06 · X10 · X11)은 **worker-external**(`bootstrap/external_worker.py`) 프로세스에서 알림을 만든다(검수 F-2 ⑤) |
| 사건 만들기 `UserEventType.` | **12 / 6 파일** |
| WS 라우트 | **2**(메시지함 → SSE 대체 · 회의 그대로) |
| SSE · `EventSource` | **0 / 0** |
| 화면 연결 `useInboxStream(` | **3 / 3 파일** · `new WebSocket` **2**(하나만 바뀜) |
| 안 읽음 「내 줄 빼기」 | **1**(`IS:199`) |
| 셸 커맨드 | **4 → 6 · 7 → 9** · 셸 → 웹 사건 **1 → 2** |

---

## Phase P0 — 조사 (코드 아님)

- **Status**: TODO · **누가**: 코디(사용자 Mac · 읽기만) + frontend 워커(셸 플러그인 문서 · 소스 읽기) · **SPEC**: S9 OQ-K01 · S11 OQ-1108 · S6 「시스템 알림 수용」 실측
- **시작 조건**: SPEC 검수 PASS
- **물음**
  - [ ] **P0-1 카톡 「내가 보냄」 재료(OQ-K01)** — 사용자 Mac 의 카톡 로컬 DB 를 **읽기 전용 사본**으로 열어(수집기와 같은 방식 · 키·경로는 Mac 밖으로 내지 않음) **고른 방 3개**에서 `NTChatMessage.authorId` 가 `NTChatContext.userId`(내 id)와 같은 줄 수를 센다 → 운영 백필 기준(**본인 14건 · 방 3개** · `prod-check-1.md`)과 맞는지. 1:1 · 단체방 각각. **결과(맞음 / 다름 / 열 수 없음)만 기록**하고 사람 이름 · 본문은 적지 않는다
  - [ ] **P0-2 알림 플러그인 클릭 콜백(OQ-1108)** — 쓰려는 Tauri 2 데스크톱 알림 플러그인 판이 **macOS 에서 사용자가 알림을 눌렀을 때 앱에 콜백**을 주는가(문서 · 소스 · 이슈). 못 주면 대안(OS 기본 = 앱 활성화 · 웹이 「마지막 알림」 으로 가는 길 등)을 적고 코디가 사용자에게 묻는다
  - [ ] **P0-3 권한 · 서명 영향** — 미서명 `tauri dev` 와 서명 dmg 에서 알림 권한 프롬프트 · 표시가 각각 어떤지(문서 근거 · 실기는 WP4) · Info.plist 키 필요 여부 · Windows 는 pending
- **코드 전에 갈라야 하는 실측은 위 셋뿐이다.** 숨은 · 최소화 웹뷰의 연결 · 타이머(DEC-010 실측 ②)와 창을 닫으면 프로세스가 끝나는가(③)는 **WP1-FE · WP4 의 완료 조건**에서 잰다(코드가 있어야 잴 수 있다)
- **완료**: 결과 한 장(`orchestration/work/strong-hajin-notify/p0-report.md`) · SPEC-009 OQ-K01 · SPEC-011 OQ-1108 처분을 코디가 사용자와 닫는다 → WP4 브리프

## Phase WP1-BE — 사건 채널(서버)

- **Status**: TODO · **워커**: backend · **SPEC**: S11 §4.1 · S8 §4.4(v0.7.0)
- **시작 조건**: SPEC 검수 PASS
- **계약**
  - [ ] **`GET /api/events/stream`** — `text/event-stream` · `Cache-Control: no-cache, no-transform` · `X-Accel-Buffering: no` · 첫 `retry: 3000` + `event: ready` · **20초 `: ping`**
  - [ ] **인증** 세션 쿠키 — 없으면 스트림 없이 `401` JSON · `Origin` 이 있고 web origin 과 다르면 `403`(지금 WS 검사 옮김) · 화면은 상태 코드를 못 보므로 **세션 확인은 기존 `GET /api/auth/me`(`entrypoints/http.py:736`)가 한다** — 그 라우트는 바꾸지 않는다
  - [ ] **사건 종류** — 메시지함 넷은 지금 WS 프레임과 같은 `data`(이름 · 필드 그대로) · `notification.upserted`(id = 사건 순번 · `data` = 알림 항목 — WP2 가 항목 모양을 채운다, WP1 은 순번 · 이어 받기 틀) · `notification.read` · `resync`
  - [ ] **이어 받기** — 마지막 순번 = **`Last-Event-ID` 머리 또는 `?last_event_id=` 쿼리**(둘 다면 머리) → **겹침 창**: 순번 > 마지막 + (순번 ≤ 마지막 이고 `updated_at` ≥ 마지막 순번 알림의 `updated_at` − 60초) 를 순번 순으로(`replayed: true`) (기준 줄이 없으면 **그 순번 이하 가장 큰 순번 줄**의 `updated_at` − 60초 · 그것도 없으면 이어 받기 없이 `resync(reconnected)` — r2 R-W1) → `resync`. 200건 넘으면 `resync(replay_overflow)` 만. **구독을 먼저 걸고 DB 를 읽는다** · 같은 순번은 한 번만(S11 §4.1-3 · 검수 W-2)
  - [ ] **NOTIFY 페이로드** — 알림은 `{v, type, member_id, notification_id, seq, created}` 만 · SSE 를 내는 API 프로세스가 DB 에서 항목을 읽어 보낸다
  - [ ] **큐 넘침** — 버린 사건이 있으면 그 연결에 `resync(dropped)`
  - [ ] **워커 게시 길** — meeting_worker 가 같은 함수로 게시할 수 있게(import 경로 · 세션) — 실제 호출은 WP2 생성기
  - [ ] WS `/api/inbox/stream` 서버 라우트는 **남긴다**(화면은 안 씀 · Rollback) · 회의 WS 는 손대지 않는다
- **완료 조건(실물)**: **운영 origin(Cloudflare → ingress)에서 SSE 연결이 1시간 이상 유지되고 사건이 바로 온다**(검수 W-11 — SPEC · WORK 모두 1시간) — ingress 주석(Pre-deploy)을 먼저 적용해야 한다 · 코디가 운영 반영 뒤 확인(그 전엔 로컬 · 개발 fixture)
- **시험(관련만 — P-8 · Makefile 타겟)**: `make test-contract-serial FILES="tests/unit/test_user_event_hub.py tests/contract/test_external_inbox.py tests/contract/test_kakao_ingest_and_profile.py tests/contract/test_production_route_registration.py <새 SSE 시험 파일>"`(SSE 라우트 · 401/403 · 머리/쿼리 우선 · 겹침 창 · **기준 줄 없음 → 가장 큰 순번 이하 / 없으면 `resync`** · `resync` · 회원 거르기) · `PYTEST_ADDOPTS='tests/integration/postgres/test_external_channels_postgres.py' POSTGRES_TEST_URL=… make test-postgres`(NOTIFY 경유) · **새 시험: 비-200 뒤 회복의 서버 쪽 — 같은 회원이 `?last_event_id=` 로 다시 붙으면 그 사이 알림을 받는다** · **두 트랜잭션 커밋 순서를 바꾼 이어 받기(겹침 창)** · **합쳐져 순번이 바뀐 줄의 옛 순번으로 다시 붙기(기준 줄 대체)**

## Phase WP1-FE — 사건 채널(화면)

- **Status**: TODO · **워커**: frontend · **SPEC**: S11 §4.1-6 · S8 AC-35
- **시작 조건**: WP1-BE 계약 고정
- **계약**
  - [ ] **App 이 로그인한 동안 EventSource 하나** — 화면이 바뀌어도 유지 · 로그아웃 · 세션 상실 때 닫음
  - [ ] `useInboxStream` → 전역 연결 구독(사건 이름으로) · 메시지함(`InboxPage`) · 설정(`SettingsPage`)이 지금과 같이 반응 · 듣는 자식 넷(`MailView` · `RoomView` ×3) 그대로
  - [ ] **`resync` → 지금 `onReconnect` 와 같은 다시 읽기** · **한 연결에서 다시 읽기는 한 번만**(r3 R3-W2): 순번을 실어 다시 붙었으면 `ready` 가 아니라 뒤따르는 `resync` 에서 · **순번 없이 다시 붙었으면 둘째 이후 `ready` 에서** 다시 읽기(r2 R-F1 — 알림을 한 건도 받지 않아 순번이 없는 재연결은 서버가 `resync` 를 못 낸다) · 첫 `ready` → 점 다시 읽기(WP3 가 점을 그린다 — 여기서는 구독 자리만)
  - [ ] **멈춤**(r2 R-W6 · r3 R3-W1) — **`/api/auth/me` 200 인데 스트림만** 연속 10회 실패하면 빠른 재연결을 멈추고 **5분마다 한 번** 느린 재시도 · 화면 활성(`visibilitychange` → `visible`) · 창 포커스 때 즉시 · **`/api/auth/me` 가 실패하는 동안(서버 장애)은 세지 않고 백오프를 이어 간다**
  - [ ] ~~**401 로 닫히면 다시 붙지 않고 세션 상실**~~ → *(수정 1 · F-1)* **닫힘 처리**(S11 §4.1-6): `CONNECTING` 은 브라우저 재연결에 맡김(30초 넘으면 버림) · **`CLOSED` 면 `GET /api/auth/me`(`getSession` `F/lib/api.ts:826`) → `401` 이면 세션 상실(회의 4401 과 같은 길 `App.tsx:522-526`) · 아니면 백오프(1→2→4…최대 30초 · ±20%) 새 `EventSource(…?last_event_id=)`** · 세션 확인도 같은 백오프 · 지금 WS 의 무한 재시도는 없앤다
  - [ ] **받은 (알림 id · 순번) 기억** — 겹침 창으로 다시 온 줄은 끼우지도 OS 알림도 하지 않는다(그 세션 동안)
  - [ ] WS 연결 코드(`new WebSocket` in `inboxStream.ts` · 백오프 2→30s)를 걷는다 · 주소 함수 교체
- **완료 조건(실물 · 앱)**: 앱에서 홈 · 업무 · 메시지함 · 설정을 오가도 연결 하나(셸 로그 · 개발 도구) · 메시지함 새 메시지 · 설정 연동 숫자가 지금처럼 · **노트북 덮었다 열기 · 최소화 10분 뒤** 다시 붙고 메시지함이 다시 읽힌다(실측 — 결과 기록)
- **시험(관련만 — P-8)**: `cd frontend && npx vitest run src/features/inbox/InboxPage.test.tsx src/features/settings/SettingsPage.test.tsx src/SettingsLanding.test.tsx src/App.test.tsx <새 사건 채널 시험> --no-file-parallelism`(WS 대역 → EventSource 대역) · **새 시험: 「비-200 뒤 회복」** — 대역 EventSource 가 CLOSED 로 끝나면 ① `/api/auth/me` 200 → 백오프 뒤 새 인스턴스 · 주소에 `last_event_id` · 로그인 화면 안 감 ② `/api/auth/me` 401 → 세션 상실 · 다시 안 붙음 ③ CONNECTING 오류는 새 인스턴스를 만들지 않음 ④ **알림을 한 건도 받지 않은 채(순번 없음) 끊겼다 붙으면 둘째 `ready` 로 메시지함 · 설정 연동이 다시 읽는다**(r2 R-F1) ⑤ **`/api/auth/me` 200 + 스트림 10회 실패 → 멈춤 → 5분 타이머 · `visibilitychange`/포커스로 다시 · `/api/auth/me` 실패(장애)는 세지 않아 멈추지 않음**(r2 R-W6 · r3 R3-W1) ⑥ **순번을 실은 재연결은 `resync` 에서만 다시 읽기(GET 한 번) · 순번 없는 재연결은 둘째 `ready` 에서 한 번**(r3 R3-W2) · 중복 순번 거름 · `make frontend-build`

## Phase WP2-BE — 알림 생성 · 설정 · 판정 재료 · 백필

- **Status**: TODO · **워커**: backend · **SPEC**: S11 §4.2 ~ §4.5 · §4.7 · S8 §4.4(v0.7.0) · §4.6
- **시작 조건**: WP1-BE 머지
- **계약**
  - [ ] **스키마**(Domain/Schema) — 알림 표 칸 · 사건 순번 · 알림 설정 표 · 외부 메시지 `from_me` · 기존 두 종류 값 바꾸기 · 수동 SQL + 로컬 `schema_sync`
  - [ ] **생성기 하나**(S11 §5) — 사건 자리는 「무슨 일 · 관련자」 만 넘긴다 · 원칙 ① 행위자 · ② 항목 + 설정 거름 · ③ 관계 없음 + **예외 M06** · 관계 우선 **담당 > 요청자 > 배정자 > 참조** · 회의 겹침은 OQ-1104 제안(소유자 > 참석자 > 공유받음) · 같은 트랜잭션 NOTIFY · 멱등 `uq_notification_recipient_source`
  - [ ] **사건 자리 전부 — S11 §4.2 의 68행**(67 + M15 · 부록 2 표가 행 → 자리). 「알림」 40행은 생성기를 부르고, 「없음」 28행(M15 포함)은 **부르지 않는 것을 시험으로 고정**
  - [ ] **흡수(D-30)** — `WT:2116` 의 `emit` 을 생성기 호출로 · 옛 종류 값 마이그레이션
  - [ ] **선행 해제(W35)** — `APP:1581` 「알림의 자리」 를 연다(시험 `test_task_successors.py:495-515` 기대 바뀜) · 이동(`APP:741`)은 그대로
  - [ ] **메시지 저장 때** `from_me`(슬랙 `raw.user` · 메일 From = `account_key`(D-41) · 카톡 업로드 `from_me`) · 메일 To/CC 판정 · 슬랙 멘션(`<@내 id>` · `@here` 류는 아님 — OQ-1105) · **실시간 줄만 알림 — 백필 · 메우기는 아님**(OQ-1101) · **메일 · 슬랙 저장은 worker-external 프로세스**(그 프로세스에서 생성기 · NOTIFY — F-2 ⑤)
  - [ ] **슬랙 채널 합침**(S11 §4.3-4) — 그 방의 안 읽은 채널 줄 고침(count · senders · 새 순번 · `created: false`) · DM · 멘션은 안 합침 · 방 읽음이 그 줄도 읽음(D-37)
  - [ ] **연동 끊김 X10 · 방 접근 잃음 X11** — 항목 = 그 채널 · 꼬리표 `integration` · 카톡 꺼짐 X12 는 없음
  - [ ] **meeting_worker** — 회의록 완료(M09 · M10) · 실패(M11)가 생성기 → 같은 트랜잭션 NOTIFY
  - [ ] **안 읽음 셈** — 방 `IS:197-199` · **메일 넷**(`IS:112-118` · `IS:130` · `INB:503` · `:525`) → `from_me is not true`(슬랙 · 카톡 · 메일 · 검수 F-2 ③)
  - [ ] **메시지함 읽음 → 알림 읽음**(D-37 · S11 §4.5-3 · S8 v0.7.0) — 메일 한 통 · 방 `up_to_ts` · 메시지함 「모두 읽음」 이 같은 트랜잭션에서 메시지 알림 줄을 읽음 + `notification.read` · 연동 끊김 줄 제외 · 반대 방향 없음
  - [ ] **회의 공유 두 길**(`share_many` · `share`) 모두 M12 · **공개 전환(`apply_legacy_visibility`)은 알림 없음**(M15 · D-38)
  - [ ] **카톡 업로드** — `from_me` 명시 필드 · 없으면 `null` · 이미 있는 `logId` 건너뛰기는 그대로
  - [ ] **알림 API**(S11 §4.5) — `GET /api/notifications?theme&cursor&limit` · `summary` · `{id}/read` · `read-all`(본문 없음 · **전부** — D-40) · `GET /api/me/badges` · 항목 모양 · **`target`(고른 상태까지)** · **읽기 인가 변경**(줄은 남고 `target: null` · 저장한 제목 · 행위자 · 값) · 읽음 성공 → `notification.read`
  - [ ] **설정 API**(S11 §4.4) — `GET/PUT /api/me/notification-settings` · 기본값(시안 `on`) · `version` 409 · 항목 16 정확히
  - [ ] **MCP 도구 · 도구 설명 · 운영 인벤토리** 갱신 · 회의 공유 도구 설명(`tool_catalog.py:446`) 「알림을 내지 않는다」 고침
  - [ ] **백필 SQL**(S11 §4.7 · 검수 W-3) — `migrations/manual/2026-10-xx-notification-from-me-backfill.sql` — 인자 `psql -v integration_id=… -v self_name=… -v apply=0|1` · **두 걸음**: `apply=0`(기본) = 셈만 출력(본인 줄 · 방 수 · 전체 · 이름 종류 · 같은 이름이 본인 하나뿐인지) → 코디가 보고 → `apply=1` = 한 트랜잭션 · `from_me IS NULL` 줄만(다시 돌려도 안전) · ~~적용 전 셈 · 맞지 않으면 롤백~~ · 슬랙(`raw.user`) · 메일(From — 어려우면 `null`) · 카톡(이름 인자) · 파일 · 시험 · 커밋에 실명 없음(P-10)
- **완료 조건(실물)**: 로컬에서 **Gmail 1통**(To · CC · 숨은 참조 각 1회가 꼬리표 셋) · **Slack**(DM 1 · 멘션 1 · 채널 3건 합침 1줄 · 내가 보낸 줄 알림 없음 + 안 읽음에 안 셈) · **업무 요청 → 수락**(두 회원) · **회의 종료 → 회의록 완료 알림이 meeting_worker 에서** SSE 로 옴
- **시험(관련만 — P-8 · Makefile 타겟)**: `make test-contract-serial FILES="tests/unit/<생성기 · 규칙 · 판정 재료 새 시험> tests/contract/test_notifications.py tests/contract/test_task_successors.py tests/contract/test_task_assignments.py tests/contract/test_request_amendment.py tests/contract/test_request_creation_input.py tests/contract/test_meeting_core.py tests/contract/test_meeting_finalize.py tests/contract/test_external_inbox.py tests/contract/test_external_sync.py tests/contract/test_kakao_ingest_and_profile.py tests/contract/test_personal_command_tools.py tests/contract/test_unified_queries.py tests/architecture/test_operation_inventory.py <새 68 행 시험 파일>"`(**행 id 를 시험 이름에** — S11 AC-07 · 공유 두 길 · 공개 전환 없음 · 메일 안 읽음 넷 · 메시지함 읽음 → 알림 읽음 · read-all 전부 · 인벤토리 drift) · 파일이 많아 직렬이 느리면 `PYTEST_ADDOPTS='-k "notification or from_me or inbox_read"' make test-contract` · `PYTEST_ADDOPTS='tests/integration/postgres/test_external_channels_postgres.py <새 알림 표 · 백필 시험>' POSTGRES_TEST_URL=… make test-postgres`(새 표 · 순번 · NOTIFY · 백필 SQL 두 걸음 — 가상 이름)

## Phase WP3-FE — 화면

- **Status**: TODO · **워커**: frontend · **SPEC**: S11 §2.1 ~ §2.3 · §4.5
- **시작 조건**: WP2-BE 계약 고정 · WP1-FE 머지
- **계약**
  - [ ] **알림 목록 화면** `surface="notifications"`(검수 W-10 — 사이드바 id `notifications` 그대로 · 시안 `alert` = 코드 `notifications` · `ProductSurface` 에 더함) — 시안 A 그대로(머리 · 필터 넷 · 탭 수 · 날짜 구분 넷(KST) · 한 줄 · 꼬리표 16 · 실패 표식 · 상태 넷) · **스크롤 끝 자동 이어 불러오기**(D-36 · 실패면 끝에 「더 불러오지 못했습니다 · 다시 시도」) · **[모두 읽음] = 전부 · 비활성은 전체 기준**(D-40)
  - [ ] **문장 함수 하나**(`labels.ts`) — `kind` · `data` → 문장 · 보조 줄 · 가는 곳 — **OS 알림도 이 함수**(WP4)
  - [ ] **실시간** — `notification.upserted` 끼우기/고치기 · `notification.read` 반영 · 요약 다시 읽기
  - [ ] **누르면** — 읽음 + `target` → 포커스 상태(`onOpenResource` 와 같은 함수) · 메시지 줄 강조 · `target: null` 이면 「열 수 없는 항목입니다」
  - [ ] **사이드바 점 둘** — `disabled` 걷기 · `dot` 넘기기 · `GET /api/me/badges` 를 S11 §2.2 의 때마다
  - [ ] **설정 알림 탭** — 시안 B 그대로 · `Switch`(`settingsParts.tsx`) · 바꿀 때마다 저장 · 실패 되돌림 · 409 다시 읽기 · `tab=notify` 콜백 쿼리
- **완료 조건(실물 · 앱)**: 앱에서 WP2 완료 조건의 알림들이 목록에 서고 눌러서 고른 상태로 열림 · 점 둘이 켜지고 꺼짐 · 설정을 꺼서 그 알림이 안 생김
- **시험(관련만 — P-8)**: `cd frontend && npx vitest run src/shell/AppShell.test.tsx src/features/settings/SettingsPage.test.tsx src/SettingsLanding.test.tsx src/App.test.tsx <새 알림 화면 · 설정 탭 · Switch 시험> --no-file-parallelism` — 꼬리표 · 날짜 구분 · 빈/로딩/오류 · 자동 이어 불러오기 · [모두 읽음] 전부 · 이동(target 별) · 점 · 설정 저장/되돌림 · disabled 단언 바뀐 시험 둘 · `make frontend-build`

## Phase WP4-SHELL — 셸 시스템 알림 + 카톡 수집기 표지 *(dmg 는 이 판에 한 번)*

- **Status**: TODO · **워커**: frontend(셸) · **SPEC**: S6 v0.7.0 · S11 §2.5 · §4.6 · S9 v0.6.0
- **시작 조건**: WP3-FE 머지 · **P0 결과**(OQ-K01 · OQ-1108 처분)
- **계약**
  - [ ] 알림 플러그인(`Cargo.toml:35` 옆) · 커맨드 `notify_permission` · `notify_show` · **`build.rs:138-160` ACL 매니페스트에 두 커맨드**(없으면 빌드 실패 — 검수 F-2 ④) · capability 두 판 · `shell_info.features += "notification"` · 셸 시험(커맨드 6 · 9)
  - [ ] **클릭** — 창 보이기 · 포커스 → `strong-hajin:notification-click`(`{notification_id, target}`) · 이름 일치 시험 · (P0 에서 클릭 콜백이 없으면 OQ-1108 처분대로)
  - [ ] **웹 다리**(`F/lib/shell.ts`) — `notifyPermission` · `notifyShow` · `onShellNotificationClick` · `features` 에 `notification` 있을 때만
  - [ ] **새 알림 → OS 알림**(D-39 · S11 §2.5) — `notification.upserted` 가 `created: true` · `replayed: false` 일 때만 · ① **앱이 앞에 있고 그 대상 화면을 보고 있으면 생략**(`visibilityState` · `hasFocus()` · 지금 surface · 포커스 = `target`) ② 합친 줄 갱신(`created: false`)은 없음 ③ **10초 창에 넷 이상이면 셋까지 낱낱이 · 나머지는 창 끝에 「새 알림 N건」 하나**(누르면 알림 목록) — 창 · 문턱은 웹 상수 · 글자는 WP3 의 문장 함수 · 클릭 → WP3 의 이동 함수
  - [ ] **권한 묻기**(OQ-1102 제안) — 로그인 뒤 첫 화면 한 번 · 거부면 다시 묻지 않는다 · ~~설정 탭 안내 한 줄~~(검수 W-9 — 시안에 없어 걷음 · Open Issues I-8)
  - [ ] **카톡 수집기 `from_me`** — P0-1 결과가 「맞음」 이면 `authorId == 내 userId` 로 업로드에 싣는다 · 아니면 **싣지 않는다**(SPEC-009 AC-12)
  - [ ] dmg 빌드 · 서명 · 공증 1회
- **완료 조건(실물 · macOS 서명 dmg)**: 새 알림 OS 표시 · **그 대상 화면을 보고 있으면 안 뜸** · 합친 슬랙 줄은 처음만 · **몰림(재연결 직후 · 최소화 풀림) 때 셋 + 「새 알림 N건」**(창 · 문턱 실측 기록) · 누르면 앱이 앞으로 + 대상 고른 상태 · 권한 거부 시 목록만 · **창 닫으면 OS 알림 없음 · 다시 열면 목록 · 점 맞음** · **최소화 · 가려짐 30분 동안 알림이 제때 뜨는가**(실측 기록) · strong-hajin 판에서 마지막 창을 닫으면 프로세스가 끝나는가(기록) · 카톡: 내가 보낸 줄 `true` · 받은 줄 `false`(실물 1회)
- **시험(관련만 — P-8)**: `make shell-verify`(커맨드 · capability · 사건 이름) · **cargo 두 벌** — `cd frontend/src-tauri && cargo test`(strong-hajin — 커맨드 6) **와** `cargo test --features kakao-collector`(medi-ax — 커맨드 9 · `kakao/db.rs` · `client.rs` 의 `from_me`) · `cd frontend && npx vitest run src/lib/shell.test.ts <새 셸 다리 · OS 알림 생략/묶음 시험> --no-file-parallelism`(셸 대역 `__TAURI_INTERNALS__`) · `make shell-build`(판마다)

## Phase 반영 — 1루프 E2E → 2루프 → 운영

- [ ] 코디 `make local-stack`(**백엔드 커밋마다 재시작** — P-4) + `make tauri-local` 로 1차 확인 → **운영 반영 → 사용자 E2E(앱)** — 아래 체크리스트
- [ ] 사용자 지적을 **모아** 2루프 브리프 한 장(P-1)
- [ ] 마지막에 코디 `make verify` 한 번(P-8)
- [ ] PR(코드) 하나 · 문서 PR 따로
- **운영 반영 순서**
  1. [ ] **manual SQL**(알림 표 칸 · 설정 표 · `from_me` 칸 · 사건 순번 · 옛 종류 값)을 이미지보다 먼저
  2. [ ] **ingress 주석**(인프라 레포 `MediSolveAIDev/k8s_infra_mac` — `/api/events/stream` 버퍼링 끔 · 읽기 제한) — 이미지보다 먼저
  3. [ ] 이미지 태그(back · front · **워커 다섯 — conversation · material · meeting · report · external**(검수 F-2 ⑤ · 메일 · 슬랙 알림은 external 이 만든다 · meeting 은 회의록 알림)) → Argo 수동 sync · **다섯 워커 모두 재시작 확인**(옛 코드가 떠 있으면 알림이 안 선다 — P-4)
  4. [ ] **운영 SSE 실물**(WP1 완료 조건) — Cloudflare 경유 **1시간** · 그 사이 back 을 한 번 재시작해 **비-200 뒤 회복**(로그인 안 튕김 · 이어 받기)
  5. [ ] **medi-ax dmg 전달 · 사용자 앱 업데이트 확인**(새 수집기가 `from_me` 를 싣는다) — *(수정 1 · W-3: 백필보다 먼저)*
  6. [ ] **백필 SQL 두 걸음**(코디 · `psql -v` 인자) — `apply=0` 셈 출력 → 보고 판단 → `apply=1`. dmg **뒤**에 돌려 그 사이 올라온 `null` 줄까지 채운다 · 그 뒤에도 `null` 이 남으면 한 번 더(`null` 줄만 — 안전). **백필 전 · dmg 전 `null` 줄은 「내 것 아님」**(S11 §4.7) — 그동안 내 카톡 줄이 나에게 알림으로 올 수 있다

### 사용자 E2E 체크리스트 (데스크톱 앱)

- ☐ 앱 사이드바 「알림」 이 열리고 알림 목록 화면(필터 넷 · 날짜 구분 · 꼬리표)
- ☐ 팀원이 나에게 업무 요청 → 알림 점 · OS 알림 · 누르면 그 업무가 열림 · 점 꺼짐
- ☐ 내가 업무를 요청 → 나에게는 알림 없음 · 상대가 수락하면 「수락했습니다」
- ☐ 배정 · 담당 넘김 · 담당 수락(배정자에게 「배정자」 꼬리표) · 기한 변경 · 완료 보고 · 보완 요청 · 재개 · 선행 업무 끝남 — 각 한 번
- ☐ 슬랙 DM · 멘션은 한 줄씩 · 채널 메시지 여럿은 「N건」 한 줄 · 내가 보낸 슬랙 메시지는 알림 없음 · 메시지함 안 읽음에도 안 셈
- ☐ 메일(받는 사람 · 참조 · 메일링) 꼬리표 셋 · 카톡 1:1 · 단체방 · 내가 보낸 카톡은 알림 없음
- ☐ 회의 초대 · 시간 변경 · 취소 · 회의에서 빠짐(「열 수 없는 항목」) · 회의록 완료(참석자도) · 실패 · 공유(「공유받음」)
- ☐ 메일 · 슬랙 연동 끊김 → 붉은 「내 연동」 줄 → 누르면 설정 그 연동
- ☐ 설정 「알림 설정」 — 항목 16 · 테마 끄기 · 전체 끄기 → 그동안 알림이 목록에도 안 생김 · 다시 켜도 안 생김
- ☐ 메시지함 점 — 안 읽은 메시지가 있으면 켜지고 다 읽으면 꺼짐 · **메시지함에서 메시지를 읽으면 그 알림 줄도 읽음 · 알림 점도 맞게 꺼짐**(D-37)
- ☐ 노트북을 덮었다 열기 → 그 사이 알림이 목록에 · OS 알림은 몰아 울리지 않음(몰리면 「새 알림 N건」 하나)
- ☐ 서버 배포 중에도 로그인 화면으로 튕기지 않고 다시 붙음(코디가 반영 때 재현)
- ☐ 메시지함에서 그 DM 방을 열어 둔 채 새 DM → OS 알림 없음 · 목록에는 섬(D-39 ①)
- ☐ 회의를 「공개」 로 바꿈 → 「공유받음」 알림 없음 · 특정 사람 공유는 알림(D-38)
- ☐ 창을 닫았다 다시 열기 → 닫힌 동안 OS 알림 없음 · 목록 · 점은 맞음
- ☐ [모두 읽음] = **어느 탭에서 눌러도 전부**(D-40) · 스크롤 끝 자동 이어 불러오기(D-36)

**확인할 것 — 동작은 정했지만 사람 눈에 이상해 보일 수 있는 자리**(SPEC-011 §7 제안대로 구현 — 사용자 판단을 받는다)

- ☐ **H-1** 메일 연동 직후 받은편지함 백필은 알림이 없다(OQ-1101) — 받아들일 수 있는가
- ☐ **H-2** OS 알림 권한을 첫 화면에서 묻는다(OQ-1102)
- ☐ ~~**H-3** 슬랙 채널 「N건」 줄이 늘 때 OS 알림은 다시 안 운다(OQ-1103)~~ — 사용자 결정(D-39 ②)
- ☐ **H-4** `@here` · `@channel` 은 멘션 줄이 아니라 채널 「N건」 에 든다(OQ-1105)
- ☐ ~~**H-5** 메시지함에서 그 방을 읽어도 알림 줄은 안 읽음으로 남는다(OQ-1110)~~ — 뒤집힘: 함께 읽음(D-37)
- ☐ ~~**H-6** [모두 읽음] 이 지금 탭만 읽는다(OQ-1107)~~ — 시안대로 전부(D-40)
- ☐ **H-7** 업무 요청 하나에 **업무 수신함 카드 + 알림 줄 + OS 알림** — 수신함에서 수락해도 알림 줄은 안 읽음으로 남는다(D-30 「읽음 따로」 · 검수 §10 ①)
- ☐ **H-8** 알림 목록 화면을 보고 있어도 OS 알림이 뜬다(OQ-1111 — 대상 화면이 아니다)
- ☐ **H-9** 철회 · 취소 · 빠짐 알림은 누르면 거의 늘 「열 수 없는 항목입니다」(검수 §10 ⑦) — 가는 곳 글자를 처음부터 숨길지
- ☐ **H-10** 「새 알림 N건」 묶음의 창(10초) · 문턱(셋)이 몰림을 잘 다루는가

## Pre-deploy Check

- [ ] 모든 Phase 검수 처리 · 코디 `make verify` 통과 · 사용자 E2E(앱) 통과
- [ ] **ingress — `/api/events/stream`**: `nginx.ingress.kubernetes.io/proxy-buffering: "off"` · `proxy-read-timeout`(예 3600) — 인프라 레포 PR(차트 소유 밖 — 코디)
- [ ] **Cloudflare** — 프록시가 SSE 를 버퍼링 · 유휴로 끊지 않는지(하트비트 20초) — 운영 실물 1회 · 끊기면 하트비트 간격을 줄인다(코드 상수)
- [ ] **운영 SQL 먼저** — 알림 표 칸 · 설정 표 · `from_me` · 사건 순번(시퀀스) · 옛 종류 값 — additive · 로컬은 `make sync-demo-schema` 뒤 스택 재시작
- [ ] **API 프로세스 수 · 연결 수** — SSE 는 회원마다 연결 하나를 오래 붙든다 — back(uvicorn) 워커 · 연결 한도 · `LISTEN` 연결 하나(프로세스당) 확인(BE §8-6)
- [ ] **워커 다섯의 이미지 · 재시작** — meeting(회의록 알림) · **external(메일 · 슬랙 알림 · 메일 `from_me`)** · conversation(AX 실행 업무 사건 — I-1) · material · report 가 back 과 같은 이미지로 올라갔는지(RUNBOOK-002 :42 · :163-166 · 검수 F-2 ⑤)
- [ ] **백필 SQL** — 인자(본인 카톡 표시 이름)는 코디가 운영 셸에서만 · ~~셈(14 · 방 3)이 맞을 때만 커밋~~ → **`apply=0` 셈 출력을 보고 판단 → `apply=1`**(W-3) · **dmg 뒤**
- [ ] dmg 서명 · 공증 · 알림 표시 실기(P-6)

## Rollback

- 이미지 태그를 직전 값으로(back · front · 워커 함께) → 수동 sync. **옛 front 는 WS `/api/inbox/stream` 을 쓴다 — 그래서 이 판은 WS 서버 라우트를 남긴다**(새 back + 옛 front 도, 옛 back + 옛 front 도 동작). WS 라우트 제거는 운영 반영 1회 뒤 다음 판
- **SQL 은 additive 라 남긴다** — 새 칸 · 새 표는 옛 이미지가 모른 채 돈다. 옛 이미지의 알림 목록 API 는 바뀐 옛 종류 값(`work.request_received` 등)을 모르고 그대로 내보낸다 — 옛 화면은 알림 API 를 부르지 않으므로(FE A-1) 영향 없음
- 백필 SQL(`from_me`) — 옛 이미지는 그 칸을 읽지 않는다 · 되돌릴 필요 없음
- ingress 주석 — 남겨도 무해(버퍼링 끔은 다른 응답에 영향이 작다 — 경로 한정)
- dmg — 직전 dmg 재설치(옛 셸 = `notification` 기능 없음 → 웹이 OS 알림을 부르지 않음 · 목록만)

## Done Criteria

- SPEC-011(v0.2.1) AC-01~25 · AC-02b · AC-02c · SPEC-006 AC-T50~52(+ AC-T23·T47 개수) · SPEC-008 AC-35~38 · SPEC-009 AC-11·12 가 채워지고, 외부 실물 1회 증거(운영 SSE Cloudflare 경유 · Gmail · Slack · 카톡 수집기 · macOS OS 알림)가 있다
- **사건 × 관계 68행 시험**(67 + M15)이 행 id 로 서 있다(S11 AC-07)
- **사용자 E2E 체크리스트(앱)** 통과 · 2루프 지적 처리 · H-1~H-6 사용자 판단 기록
- 운영 반영(SQL · ingress · 이미지 · 백필 · dmg) 뒤 로그 오류 0 · 운영 슬랙 안 읽음에서 내 줄이 빠짐(`prod-check` 다시 — 코디)
- SPEC-009 OQ-K01 · SPEC-011 OQ-1108 처분 기록

## Open Issues

| ID | 무엇 | 다음 |
|---|---|---|
| **I-1** | **AX 실행으로 난 업무 사건이 어느 프로세스에서 나나**(`BA:1790` 의 실행 경로 — BE §9 미확인). conversation_worker 에서 나면 그 워커도 게시한다 | WP2-BE 첫날 확인 — 생성기는 프로세스 무관(DB 세션 + 같은 트랜잭션 NOTIFY)이라 계약은 그대로 |
| **I-2** | **데스크톱 알림 플러그인의 macOS 클릭 콜백** — 없으면 D-31 의 OS 알림 쪽 「고른 상태까지」 를 못 짓는다 | P0-2 → SPEC-011 OQ-1108 · 사용자 |
| **I-3** | **카톡 「내가 보냄」 재료**(OQ-K01) | P0-1 → SPEC-009 OQ-K01 |
| **I-4** | **Cloudflare 프록시의 SSE 처리** — 버퍼링 · 유휴 끊김 · 요금제 한도(장시간 연결) | WP1 운영 실물 · 하트비트 상수 조정 |
| **I-5** | **메일 「내가 보낸 줄」 백필** — Gmail raw 의 From 을 SQL 로 풀기 어려우면 기존 메일은 `null` | WP2-BE 가 SQL 로 풀 수 있는지 보고 · 못 풀면 `null`(받은편지함만 받아 드묾) |
| **I-6** | **회의 「빠진 참석자」 셈** — `replace_attendees`(`:531`)가 바뀌기 전 · 뒤 목록을 생성기에 넘겨야 한다(지금은 통째 교체) | WP2-BE |
| **I-7** | **업무 단독 댓글 · @멘션** 이 코드에 없어 `comment` 가 요청 스레드만 잡는다 | 범위 밖 — 시안 문구와의 폭 차이는 S11 §4.4 에 적음 |
| **I-8** *(수정 1 · 검수 W-9)* | 설정 알림 탭의 「시스템 알림이 꺼져 있습니다 — 시스템 설정에서 허용」 한 줄 — **확정 시안에 없어 걷었다**. 권한을 거절하면 다시 켤 길이 OS 설정뿐이라 안내가 필요할 수 있다(검수 §10 ⑧) | **2루프 후보** — 사용자 E2E 뒤 시안 추가(architect)로 넘길지 코디가 묻는다 |
| **I-9** *(수정 1)* | 「새 알림 N건」 묶음의 창 10초 · 문턱 셋은 SPEC 이 근거와 함께 정한 값이다(S11 §2.5 ③) — 실측 근거는 없다 | WP4 실물에서 몰림(재연결 · 최소화 풀림)을 재고 조정 |
| **SPEC OQ** | SPEC-011 OQ-1101 · 1102 · 1104 · 1105 · 1108 · 1109 · **1111**(수정 1) — **제안대로 구현** · OQ-1103 · 1106 · 1107 · 1110 — **닫힘**(DEC-010 D-39 · D-36 · D-40 · D-37) · SPEC-009 OQ-K01 — P0 | 사용자가 바꾸면 2루프 |

## Domain / Schema (구현 초안 — 전문 SoT 는 코드 · migration)

| 무엇 | 초안 | 마이그레이션 |
|---|---|---|
| **알림 표 `notifications`** — 칸 더하기 | `theme`(work\|message\|meeting) · `item`(항목 id) · `relation`(꼬리표 id) · `failure`(bool) · **`seq`**(bigint · 전역 시퀀스 — 새로 서거나 합쳐질 때마다 `nextval` · 인덱스 `(recipient_member_id, seq)`) · `data`(JSON — kind 별 값 · 합친 `count` · `senders`) · `target`(JSON — 만들 때의 대상 · 읽을 때 인가로 `null` 처리) · `actor_name`(외부 발신자 이름) · `updated_at` · 합침 키(`coalesce_key` — 슬랙 채널이면 `slack-channel:{room_id}` · 그 밖 null) · 지금 칸(`kind` · `resource_*` · `actor_member_id` · `safe_summary` · `read_at` · `uq_notification_recipient_source`) 유지 — `safe_summary` 는 더 쓰지 않는다 | **있음** — `migrations/manual/2026-10-xx-notifications-v2.sql`: 칸 추가(nullable/기본값) · 시퀀스 · 인덱스(`.concurrent.sql` 짝) · **옛 행 채우기**(`work_request.received` → `kind=work.request_received, theme=work, item=request, relation=assignee` · `work_request.accepted` → `work.request_answered, item=answer, relation=requester, data={"answer":"accepted"}` · `seq` 채움). **지금 마이그레이션 파일이 없는 표다**(ORM `create_all` 로만 섬 — BE A-1) → 운영에 표가 있는지 · 행 수를 코디가 먼저 확인(BE §8-1) |
| **알림 설정** | 회원별 한 벌 — `member_id` PK · `settings` JSON(전체 · 테마 셋 · 항목 16) · `version` · `updated_at`. 없으면 기본값(코드 상수 — 시안 `on`) | **있음** — 새 표 |
| **외부 메시지 `from_me`** | `external_messages.from_me` nullable bool — 저장 때 채움(슬랙 `raw.user` · 메일 From · 카톡 업로드) | **있음** — 칸 추가 + **백필 SQL**(별도 파일 · 인자 둘 · 적용 전 셈) |
| **사건 순번** | 위 `seq` — 이어 받기의 `id:` · 회원별 띄엄띄엄 | 시퀀스 |
| **사건 자체** | 저장하지 않는다 — 알림만 저장(이어 받기 대상) · 메시지함 사건은 NOTIFY 신호 그대로 | 없음 |
| **WS 라우트** | 남긴다(Rollback) | 없음 |

---

## 부록 1 — DEC-010 결정 → SPEC 절 → Phase (전수 대응표)

**41건 전부**(D-01~D-41 — 수정 1 의 D-36~D-41 포함). 받는 SPEC: **SPEC-011 이 41건 전부**에 절을 갖고(과정 D-02 는 「해당 없음(과정)」 + 이 WORK 원칙), 짝 개정이 함께 받는 것은 **SPEC-006 5건 · SPEC-008 8건 · SPEC-009 2건**(표 아래 「셈」).

| D | 무엇 | SPEC · 절 | Phase |
|---|---|---|---|
| D-01 | 나와 관련된 것 · 네 묶음 | S11 §1 BR · §4.2 | WP2-BE |
| D-02 | 순서(조사 → 시안 → BASE·DEC → SPEC·WORK → 구현) | 해당 없음(과정) — 이 WORK 원칙 · Work Summary | 전체 |
| D-03 | 완료 = 앱 실물 | S11 §6 머리 · AC 「(앱)」 · 이 WORK P-3 | 전체 |
| D-04 | 설정 알림 메뉴 · 사이드바 알림 이번 범위 | S11 §2.2 · §2.3 · S8 v0.7.0 §1 Out · §2.7 · DEC-008 표 | WP3-FE |
| D-05 | 관계에 따라 다르다 · 칸 · 게시 길 | S11 §4.2 · §4.3-6 · §4.1-4 | WP2-BE · WP1-BE |
| D-06 | A안 — 앱 켜져 있을 때 OS 알림 | S11 §2.5 · §4.6 · S6 §2.5 · 「시스템 알림 수용」 | WP4 |
| D-07 | 푸시 없음 | S11 §1 Out · S6 §2.5(그대로) | — |
| D-08 | 창 닫으면 끊김 | S11 §2.5 · AC-22 · S6 「시스템 알림 수용」 | WP4 |
| D-09 | 셸이 맡는 것(권한 · 표시 · 클릭) | S11 §4.6 · S6 §4 커맨드 여섯 · §2.5 | WP4 |
| D-10 | SSE 하나 · WS 대체 · 앱 전역 | S11 §4.1 · §4.1-6 · S8 §4.4(v0.7.0) · AC-35 | WP1-BE · WP1-FE |
| D-11 | 회의 WS 유지 | S11 §4.1-1 · §1 Out · AC-06 | WP1(건드리지 않음) |
| D-12 | 놓친 사건 다시 | S11 §4.1-3 · AC-02 · S8 §4.4 「다시 붙을 때」 | WP1-BE · WP1-FE |
| D-13 | 워커 게시 길 | S11 §4.1-4 · AC-05 | WP1-BE · WP2-BE |
| D-14 | 사이드바 → 알림 목록 | S11 §2.1 | WP3-FE |
| D-15 | 점만 | S11 §2.2 · AC-18 | WP3-FE |
| D-16 | 메시지함도 점 | S11 §2.2 · §4.5 badges · S8 §4.4(v0.7.0) 안 읽음 셈 | WP2-BE · WP3-FE |
| D-17 | 시안 A 그대로 | S11 §2.1 · AC-15 | WP3-FE |
| D-18 | 전체 · 테마 · 항목 | S11 §2.3 · §4.4 · AC-19 | WP2-BE · WP3-FE |
| D-19 | 항목 16 · 문구 | S11 §4.4-1 | WP2-BE · WP3-FE |
| D-20 | 메시지 셋 · 끊김은 채널 항목 · 「내 연동」 | S11 §4.4-1 · §4.2-3 X10·X11 · S8 §2.7 | WP2-BE |
| D-21 | 받는 경로 = 앱만 | S11 §1 Out · §2.5 | — |
| D-22 | 끄면 목록에도 안 쌓임 | S11 §4.3-2 · AC-09 | WP2-BE |
| D-23 | 관계 우선 하나(담당 > 요청자 > 배정자 > 참조) | S11 §4.3-3 · AC-10 | WP2-BE |
| D-24 | 카톡 항목 하나 · 꼬리표로 | S11 §4.2-3 X08·X09 · §4.4 | WP2-BE |
| D-25 | 슬랙 채널 합침 | S11 §4.3-4 · AC-11 | WP2-BE |
| D-26 | 보관 고려 안 함 | S11 §1 Out · §4.3-10 | — |
| D-27 | 시각 기반 밖 | S11 §1 Out | — |
| D-28 | 원칙 셋 | S11 §4.3-1 · 2 · 5 · AC-08 | WP2-BE |
| D-29 | 사건 × 관계 표 | S11 §4.2(67행 + D-38 의 M15 = 68) · AC-07 · 부록 2 | WP2-BE |
| D-30 | 둘 다 · 읽음 따로 · 흡수 | S11 §4.3-7 · 9 · §4.2-1 · AC-13 · Schema(옛 종류 값) | WP2-BE |
| D-31 | 고른 상태까지 | S11 §4.5-2-3 · §2.1 · §2.5 · AC-16 · 21 · S6 §2.5 · §4 | WP2-BE · WP3-FE · WP4 |
| D-32 | 카톡 꺼짐 없음 · 접근 잃음 알림 | S11 §4.2-3 X11 · X12 · S8 §2.7 | WP2-BE |
| D-33 | 빠진 참석자(예외) | S11 §4.2-4 M06 · §4.3-5 · §4.5-2-4 · AC-12 | WP2-BE |
| D-34 | 내가 보낸 줄 판정 · 안 읽음 버그 | S11 §4.3-6 · S8 §4.4(v0.7.0) · §4.6 · S9 §3.1 · §4 · OQ-K01 · AC-08 · 24 | P0 · WP2-BE · WP4 |
| D-35 | 카톡 백필(택일 = 수동 SQL) | S11 §4.7 · AC-25 · S9 v0.6.0 머리 · Schema | WP2-BE · 반영 |
| D-36 *(수정 1)* | 자동 이어 불러오기 | S11 §2.1 · §4.5-1 `cursor` · AC-15 | WP3-FE |
| D-37 *(수정 1)* | 메시지함 읽음 → 메시지 알림 읽음 | S11 §4.5-3 · §2.4 · §4.3-4 · AC-11 · AC-18 · S8 v0.7.0 §4.4 · AC-38 | WP2-BE · WP3-FE |
| D-38 *(수정 1)* | 공개 전환 알림 없음 | S11 §4.2-4 M12 · M15 · AC-07 | WP2-BE |
| D-39 *(수정 1)* | OS 알림 줄이기(보고 있으면 생략 · 합친 줄 처음만 · 「새 알림 N건」) | S11 §2.5 ①②③ · AC-21 · S6 「시스템 알림 수용」(묶음도 같은 커맨드) | WP4 |
| D-40 *(수정 1)* | [모두 읽음] = 전부 | S11 §2.1 · §4.5-1 · AC-17 | WP2-BE · WP3-FE |
| D-41 *(수정 1 · 도출)* | 메일 `from_me` = From | S11 §4.3-6 · S8 v0.7.0 §4.4 · AC-08 · AC-24 | WP2-BE |

**셈** — D-01~D-41 **41건 전부 대응**(수정 1 의 D-36~D-41 여섯 포함)(과정 1건 D-02 는 「해당 없음(과정)」 으로 대응). SPEC-006 이 함께 받는 것(5): D-06 · D-07(「그대로」 칸) · D-08 · D-09 · D-31 · SPEC-008(8): D-04 · D-10 · D-12 · D-16 · D-20 · D-32 · D-34 · D-35 · SPEC-009(2): D-34 · D-35. · *(수정 1)* SPEC-006 이 함께 받는 것 + D-39(묶음 클릭) · SPEC-008 + D-37 · D-41.

## 부록 2 — 사건 × 관계 표 67행(+ M15) → SPEC-011 행 → 사건 자리 → Phase

DEC-010 § 사건 × 관계 표의 행 순서 그대로. **알림 40 · 없음 27** + *(수정 1)* **M15**(없음 · D-38) = 68행. 「없음」 행도 시험으로 고정한다(S11 AC-07).

| 행 | DEC-010 표의 행(사건 · 관계) | 알림 | 사건 자리(출발점) | Phase |
|---|---|---|---|---|
| W01 | 업무 요청 발송 · 받는 사람 | ✅ `request` | `REQ:334-484`(→ `WT:2116` 흡수) | WP2-BE |
| W02 | 〃 · 요청자 · 승격자 | — 행위자 | 〃 | WP2-BE |
| W03 | 〃 · CC | — | 〃 | WP2-BE |
| W04 | 〃 · 결재자 | — | 〃 | WP2-BE |
| W05 | 요청 수락 · 거절 · 요청자 | ✅ `answer` | `REQ:486-532` | WP2-BE |
| W06 | 〃 · 받는 사람 | — 행위자 | 〃 | WP2-BE |
| W07 | 요청 협의 · 요청자 | ✅ `answer` | `REQ:534-562` | WP2-BE |
| W08 | 수락 전 수정 · 받는 사람 | ✅ `change` | `REQ:564-616` | WP2-BE |
| W09 | 재상신 · 받는 사람 | ✅ `request` | `REQ:650-684` | WP2-BE |
| W10 | 요청 철회 · 받는 사람 | ✅ `change` | `REQ:702-724` | WP2-BE |
| W11 | 자료 · 목록 정리 · 참고 읽음 · 자동 합류 · 당사자 | — | `REQ:862·954·989` · `WT:1671-1692` · `REQ:1239` · `REQ:475-483` | WP2-BE |
| W12 | 직접 배정 · 새 담당 | ✅ `assign` | `ASG:106-153` · `WT:2525-2590` | WP2-BE |
| W13 | 담당 넘김 · 변경 제안 · 새 담당 | ✅ `assign` | `ASG:188-229` · `WT:2428-2456,2664-2702` | WP2-BE |
| W14 | 〃 · 기존 담당 | ✅ `assign` | 〃 | WP2-BE |
| W15 | 담당 수락 · 거절 · 배정자 | ✅ `answer` | `ASG:258-322` · `WT:2707-2793` | WP2-BE |
| W16 | 담당 제안 철회 · 제안받은 사람 | — | `ASG:331-347` · `WT:2796-2841` | WP2-BE |
| W17 | 업무 수정(기한 · 시작일) · 담당 | ✅ `change` | `APP:542-625` | WP2-BE |
| W18 | 〃 · 요청자 | — | 〃 | WP2-BE |
| W19 | 〃 · 결재자 | — | 〃 | WP2-BE |
| W20 | 업무 수정(제목 · 설명 · 결재자 · 선행) | — | 〃 | WP2-BE |
| W21 | 상위 · 프로젝트 이동 · 자손 담당 | — | `APP:666-745`(「알림의 자리」 `:741` 그대로) | WP2-BE |
| W22 | 하위 추가 · 상위 담당 | — | `APP:524-528` | WP2-BE |
| W23 | 시작 · 보류 · 완료 | — | `APP:2037-2118` | WP2-BE |
| W24 | 업무 취소(요청자가) · 담당 | ✅ `change` | `APP:2037-2120` | WP2-BE |
| W25 | 완료 보고 · 요청자 | ✅ `report` | `APP:1883-1926` | WP2-BE |
| W26 | 〃 · CC | — | 〃 | WP2-BE |
| W27 | 완료 승인 · 보고자 | — | `APP:1933-1944` | WP2-BE |
| W28 | 보완 요청 · 보고자 · 담당 | ✅ `rework` | `APP:1946-1964` | WP2-BE |
| W29 | 재개(요청자가) · 담당 | ✅ `change` | `APP:2140-2196` | WP2-BE |
| W30 | 재개(담당이) · 요청자 | ✅ `change` | 〃 | WP2-BE |
| W31 | 조건 변경 제안 · 담당 | ✅ `change` | `APP:2200-2228` | WP2-BE |
| W32 | 취소 제안 · 담당 | ✅ `change` | 〃 | WP2-BE |
| W33 | 제안 응답 · 합의 취소/변경 · 제안자 | ✅ `answer` | `APP:2230-2283,2329-2366` | WP2-BE |
| W34 | 제안 철회 · 담당 | — | `APP:2285-2309` | WP2-BE |
| W35 | 선행 해제 · 후행 담당 | ✅ `unblock` | `APP:1565-1619`(「알림의 자리」 `:1581` 연다) | WP2-BE |
| W36 | 요청 댓글 · 담당 · 요청자 · CC · 승격자 | ✅ `comment` | `REQ:1122-1148` · 독자 `REQ:1183-1197` | WP2-BE |
| W37 | 체크리스트 · 메모 · 참고 · 자료 · 담당 | — 행위자 | `APP:2571-2697` · `materials.py:169-272` | WP2-BE |
| W38 | AX 판단 승인 · 거절 · 소유자 | — 행위자 | `ACT:478-489` | WP2-BE |
| X01 | 메일 · To 에 나 | ✅ `mail` | `SS:152-214` | WP2-BE |
| X02 | 메일 · CC 에 나 | ✅ `mail` | 〃 | WP2-BE |
| X03 | 메일 · To/CC 에 없음 | ✅ `mail` | 〃 | WP2-BE |
| X04 | 슬랙 DM · 그룹 DM | ✅ `slack` | `SYNC:249-284` · `SS:120-131,152-214` | WP2-BE |
| X05 | 슬랙 채널 멘션 | ✅ `slack` | 〃 | WP2-BE |
| X06 | 슬랙 채널 일반(합침) | ✅ `slack` | 〃 | WP2-BE |
| X07 | 내가 보낸 줄(슬랙 · 메일 · 카톡) | — 행위자 | 저장 자리 셋 · `from_me` | WP2-BE · WP4(카톡) |
| X08 | 카톡 1:1 | ✅ `kakao` | `kakao_ingest.py:186-269` | WP2-BE |
| X09 | 카톡 단체방 | ✅ `kakao` | 〃 | WP2-BE |
| X10 | 연동 끊김(메일 · 슬랙) | ✅ 채널 항목 | `SS:349-361` · `INB:1054-1069` | WP2-BE |
| X11 | 방 접근 잃음 | ✅ 채널 항목 | `SS:295-317` | WP2-BE |
| X12 | 카톡 수집기 꺼짐 | — | `domain.py:124-148` | WP2-BE |
| X13 | 되살림 · 백필 끝 · 수집기 켜짐 | — | `SS:363-369` · `application.py:336,652` · `kakao_ingest.py:311-324` | WP2-BE |
| X14 | 답장 결과 | — 행위자 | `INB:938` | WP2-BE |
| X15 | 메시지로 만든 업무 확정 | — 행위자 | `BA:1773-1800` | WP2-BE |
| M01 | 회의 생성 · 참석자 | ✅ `invite` | `mtg/application.py:302-339` | WP2-BE |
| M02 | 〃 · 소유자 | — 행위자 | 〃 | WP2-BE |
| M03 | 〃 · 외부 참석자 | — 관계 없음 | 〃 | WP2-BE |
| M04 | 회의 정보 수정 · 참석자 | ✅ `change` | `:481-540` | WP2-BE |
| M05 | 참석자 교체 · 새로 든 사람 | ✅ `invite` | `:531` | WP2-BE |
| M06 | 참석자 교체 · 빠진 사람 | ✅ `change`(예외) | `:531` | WP2-BE |
| M07 | 회의 취소 · 참석자 | ✅ `change` | `:591-603` | WP2-BE |
| M08 | 시작 · 종료 | — | `:630,644` | WP2-BE |
| M09 | 회의록 완료 · 소유자 | ✅ `minutes` | `:886-970`(meeting_worker) | WP2-BE |
| M10 | 회의록 완료 · 참석자 | ✅ `minutes` | 〃 | WP2-BE |
| M11 | 회의록 실패 · 소유자 | ✅ `minutes-fail` | `:972-980`(meeting_worker) | WP2-BE |
| M12 | 회의 공유(특정 사람) · 공유 대상 | ✅ `share` | `share_many :1112-1133` · **`share :1179-1199`**(HTTP `BA:2448` · AX `BA:4501`) — 두 길 모두(검수 F-2 ①) | WP2-BE |
| M13 | 공유 회수 | — | ~~`:1179-1223`~~ → `revoke_share :1201-1223` | WP2-BE |
| M14 | 회의 진행 | — | `stream_service.py` · `HTTP:1245` | — |
| M15 *(수정 1)* | 회의 공개 전환(조직 전원) | — **알림 없음**(D-38) | `apply_legacy_visibility :1135-1177` · `BA:4320-4336` — 공유 알림을 부르지 않는 것을 시험으로 | WP2-BE |

**셈** — W 38(알림 21 · 없음 17) · X 15(알림 10 · 없음 5) · M 14(알림 9 · 없음 5) = **67행 · 알림 40 · 없음 27** · *(수정 1)* + M15(없음) = **68행 · 알림 40 · 없음 28**.

## 부록 3 — 검수(FAIL 3 · WARN 11 · 사람 눈 ⑫) → 닫힌 자리 *(수정 1)*

검수 `orchestration/work/strong-hajin-notify/review-spec-work-report.md` §11 의 행 전부 · §10 의 「사람 눈」 열둘.

| # | 무엇 | 닫힌 자리 |
|---|---|---|
| **F-1** | SSE 재연결이 `EventSource` 동작과 안 맞음 | S11 v0.2.0 §4.1-1(인증 · 경로 쿼리 · `retry`) · §4.1-3 ②(머리 · 쿼리 · 우선) · §4.1-6(닫힘 처리 — `GET /api/auth/me` · 백오프 새 연결) · Case Matrix(네트워크 / 비-200 / 세션 상실) · AC-02b · AC-04 · S-6b · 이 WORK WP1-BE(이어 받기 · 시험) · WP1-FE(닫힘 처리 · 「비-200 뒤 회복」 시험) · 반영 4(재시작 회복) |
| **F-2 ①** | 회의 공유 두 길 · M13 범위 | S11 M12 · M13 · AC-07 · 이 WORK Code Surface 회의 줄 · 부록 2 M12 · M13 |
| **F-2 ②** | `apply_legacy_visibility` | DEC-010 **D-38** · S11 **M15**(알림 없음) · Case Matrix · 이 WORK Code Surface · WP2-BE · 부록 2 M15 |
| **F-2 ③** | 메일 안 읽음 `IS:112-130` · `INB:503,525` | S8 v0.7.0 §4.4 「셈이 있는 자리 전부」 · AC-36 · S11 AC-24 · 이 WORK Code Surface 안 읽음 줄 · WP2-BE |
| **F-2 ④** | `build.rs:138-160` · `Cargo.toml` | 이 WORK Code Surface WP4 두 줄(ACL 매니페스트 · 의존) · WP4 계약 |
| **F-2 ⑤** | worker-external(이미지 · 재시작) | 이 WORK 개수 요지 「운영 워커」 · WP2-BE(저장 프로세스) · 반영 3 · Pre-deploy · Work Summary 반영 줄 |
| **F-3** | [모두 읽음] = 지금 필터 | DEC-010 **D-40** · S11 §2.1 · §4.5-1 `read-all`(본문 없음 · 전부) · OQ-1107 닫힘 · AC-17 · 이 WORK WP2-BE · WP3-FE · H-6 취소선 |
| **W-1** | 무한 스크롤 vs DEC 범위 밖 | DEC-010 **D-36** · 범위 밖 「더 불러오기」 취소선 · S11 §2.1 · OQ-1106 닫힘 · AC-15 · WP3-FE |
| **W-2** | 순번 ≠ 커밋 순서 | S11 §4.1-3 3-1 **겹침 창 60초 + 화면 (id · 순번) 거르기** — 근거: 겹침 창이 늦은 커밋을 다시 주고, 창 밖은 `resync` 목록 다시 읽기가 메워 잃는 것은 OS 알림뿐 · AC-02c · WP1-BE · WP1-FE |
| **W-3** | 백필 셈 · 순서 · `null` 규칙 | S11 §4.7 두 걸음 · `null` = 「내 것 아님」 · dmg 먼저 · AC-25 · 이 WORK WP2-BE · 반영 5 · 6 · Pre-deploy |
| **W-4** | 메일 `from_me` 근거 | DEC-010 **D-41**(도출) · S11 §4.3-6 · S8 v0.7.0 §4.4 |
| **W-5** | 검증이 전체 스위트 · FE 병렬 · cargo feature | 이 WORK **P-8** 다시 씀 · 각 Phase 「시험(관련만)」 — 파일 · 직렬/병렬 · cargo 두 벌 |
| **W-6** | OS 알림 상한 · 생략 | DEC-010 **D-39** ①③ · S11 §2.5(보고 있으면 생략 · 10초 셋 묶음 + 근거) · AC-21 · WP4 · I-9 · H-10 |
| **W-7** | 메시지함 읽음 ≠ 알림 읽음 | DEC-010 **D-37** · S11 §4.5-3 · §2.2 · §2.4 · OQ-1110 닫힘 · S8 v0.7.0 · AC-38 · WP2-BE |
| **W-8** | 합친 줄 OS 재알림 없음 | DEC-010 **D-39** ② · S11 §2.5 · OQ-1103 닫힘 |
| **W-9** | 설정 탭 「시스템 알림 꺼짐」 줄 | S11 §2.5 권한 줄 취소선 · 이 WORK WP4 · **I-8**(2루프 후보) |
| **W-10** | 사이드바 id 셋 · `:457` | S11 §2.1(`surface = "notifications"` · 시안 `alert` 대응) · §2.2(`:456`) · AC-15 · WP3-FE |
| **W-11** | 실측 30분 vs 1시간 | S11 §4.1-5 · AC-03 · 이 WORK WP1-BE 완료 조건 · 반영 4 — **1시간** |
| §10 ① | 수신함 + 알림 + OS 알림 | D-30 그대로 · H-7(사용자 판단) |
| §10 ② · ③ | 메시지함 읽음 vs 알림 점 · 합친 줄 둘 | D-37 — 방 읽음이 합친 줄도 읽음(S11 §4.3-4 · §4.5-3) |
| §10 ④ | 보고 있는데 OS 알림 | D-39 ① · 알림 목록 화면은 OQ-1111 · H-8 |
| §10 ⑤ | 시끄러운 채널이 OS 에서 조용 | D-39 ② — 사용자 결정(처음만) |
| §10 ⑥ | 최소화 뒤 몰림 | D-39 ③ — 10초 셋 묶음 |
| §10 ⑦ | 「열 수 없는 항목」 | 계약대로 · H-9(가는 곳 글자 숨김은 WP3 에서 정함) |
| §10 ⑧ | 권한 거절 뒤 길 | W-9 · I-8 |
| §10 ⑨ | 앱 origin 아닐 때 클릭 | SPEC-006 「시스템 알림 수용」 한 줄(창은 앞으로 · 셸 로그) |
| §10 ⑩ | 공개 전환 전원 알림 | D-38 · M15 |
| §10 ⑪ | 백필 · dmg 사이 내 카톡 알림 | W-3 — dmg 먼저 · `null` 규칙 · 다시 돌리기 |
| §10 ⑫ | 웹 탭 + 앱 | 이상 없음(검수) |

### 재검수 r2(FAIL 1 · WARN 6) → 닫힌 자리 *(수정 2)*

`orchestration/work/strong-hajin-notify/review-spec-work-r2-report.md` §7 · 코디 택일 `write2-fix2-instructions.md`.

| # | 무엇 | 닫힌 자리 |
|---|---|---|
| **R-F1** | 순번 없이 다시 붙으면 `resync` 가 없어 메시지함 · 설정 연동이 다시 읽지 않음 | 권장안 (a) — S11 v0.2.1 §4.1-2 `ready` 행(**둘째 이후 `ready` = 다시 읽기**) · `resync` 행 · §4.1-3 ⑤ · §4.1-6 2(쿼리 없이도) · AC-02 · AC-02b · S8 v0.7.0 §4.4 「다시 붙을 때」 · AC-35 · 이 WORK WP1-FE 계약 · 시험 ④ |
| **R-W1** | 겹침 창 기준 줄이 없음 | S11 §4.1-3 3-1(그 순번 이하 가장 큰 순번 줄 · 없으면 `resync`) · WP1-BE 계약 · 시험 |
| **R-W2** | 시험 직접 호출(AGENTS.md) | 이 WORK **P-8**(Makefile 타겟만 — `test-contract-serial FILES` · `PYTEST_ADDOPTS … make test-contract` · `PYTEST_ADDOPTS … make test-postgres`) · WP1-BE · WP2-BE 시험 줄 |
| **R-W3** | 남은 수 · 판 | 이 WORK 머리(SPEC-011 v0.2.1) · Meta · Work Summary WP2(68행) · WP2-BE 계약(68 · 없음 28) · Done(68행) · S11 머리(D-01~D-41) · DEC-010 머리 「2판 수정 1 · 2」 |
| **R-W4** | OQ-1102 제안의 걷은 줄 | S11 §7 OQ-1102(다시 묻지 않는다 · 안내 줄은 I-8) |
| **R-W5** | 「새 알림 N건」 셸 계약 | S11 §4.6 `notify_show`(`notification_id: null`) · §4.5-2-3 target 표 · §2.5 누르면(읽음 없이 목록만) · S6 「시스템 알림 수용」 |
| **R-W6** | `403` 무한 재연결 | S11 §4.1-6 4(연속 10회 → 멈춤 → 화면 활성 · 포커스 때 다시) · AC-02b · WP1-FE 계약 · 시험 ⑤ |
| 참고 | §4.5-3 이 §4.5-2 앞 | S11 — §4.5-3 을 §4.5-2 뒤로 옮김(번호 그대로) |


### 재검수 r3(WARN 3) → 닫힌 자리 *(수정 3)*

`orchestration/work/strong-hajin-notify/review-spec-work-r3-report.md` · 코디 택일 `write2-fix3-instructions.md`.

| # | 무엇 | 닫힌 자리 |
|---|---|---|
| **R3-W1** | 10회 멈춤이 서버 장애에도 걸림 | 택일 ① + ② — S11 v0.2.2 §4.1-6 4(`/api/auth/me` 200 + 스트림 실패만 셈 · 장애 중엔 세지 않음 · 멈춘 뒤 5분마다 + 활성 · 포커스 즉시) · AC-02b · 이 WORK WP1-FE 계약(멈춤) · 시험 ⑤ |
| **R3-W2** | 한 재연결에 다시 읽기 두 번 | S11 §4.1-2 `ready` 행 · §4.1-3 ⑤(한 연결 한 번 — 순번 있으면 `resync` 에서, 없으면 둘째 `ready` 에서 · 순서 이어 받기 → `resync` → 다시 읽기) · AC-02b · S8 §4.4 「다시 붙을 때」 · 이 WORK WP1-FE 계약 · 시험 ⑥ |
| **R3-W3** | 남은 수 | 이 WORK 머리 「D-01~D-41」 · 부록 1 머리 「41건 전부」 · SPEC-011 판 v0.2.2 |


**DEC-010 새 결정 → SPEC**: D-36 → S11 §2.1 · D-37 → S11 §4.5-3 · S8 v0.7.0 · D-38 → S11 M15 · D-39 → S11 §2.5 · S6 · D-40 → S11 §4.5-1 · D-41 → S11 §4.3-6 · S8 — 여섯 모두 대응(부록 1).


## Related

- `orchestration/work/strong-hajin-notify/_RESUME.md` §2 — 결정 원장 · `be-survey-report.md` · `fe-survey-report.md` · `prod-check-1.md`
- WORK-012 — 앞 판(메시지함 → AX · `inbox.message_updated` 사건) · WORK-011 — 외부 채널 · 사용자 사건 채널(WS)의 출처 · WORK-010 — 셸 다운로드 사건(셸 → 웹 사건의 본보기)
