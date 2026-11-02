---
type: work
id: WORK-011
title: "외부 채널 연동 · 메시지함 · 프로필 · Mac 카톡 수집"
status: done
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
progress: 5
created_at: 2026-10-06
updated_at: 2026-10-06
tags:
  - product/strong-hajin
  - doc/work
  - status/in_progress
links:
  baselines:
    - "[[baseline-006-external-channels|BASE-006]]"
  decisions:
    - "[[decision-008-external-channels|DEC-008]]"
  specs:
    - "[[spec-008-external-channels|SPEC-008]]"
    - "[[spec-009-mac-kakao-collector|SPEC-009]]"
    - "[[spec-006-tauri-wrapper|SPEC-006]]"
  works:
    - "[[work-006-tauri-wrapper|WORK-006]]"
    - "[[work-010-polish3|WORK-010]]"
  releases: []
  related:
    - "[[runbook-002-production-deploy|RUNBOOK-002]]"
sources:
  - orchestration/work/strong-hajin-inbox/_RESUME.md
  - orchestration/work/strong-hajin-inbox/review-spec-008-009-r2.md
---

# 외부 채널 연동 · 메시지함 · 프로필 · Mac 카톡 수집

메일·슬랙·카카오톡을 **내 메시지함**에 쌓고(조회·읽음·답장), 설정에서 연동·방·프로필을 다루는 1단계(DEC-008)를
구현한다. SPEC-008 v0.5.1(서버·웹)·SPEC-009 v0.5.1(Mac 카톡 수집기)·SPEC-006 v0.6.0(데스크톱 셸 개정)이 정본이다.

> **초안이다(`status: todo`).** **4차 검수(`review-spec-work-r4.md` — 조건부 PASS) 의 ★1~★4·WARN 을 반영했다** — BE-1 은 이미 발주됨. 뒤 검수가 계약을 고치면 그만큼 뒤에 고친다.
> **SPEC 이 정본이다** — 이 WP 와 SPEC 이 다르면 SPEC 이 맞고, 워커는 코디에게 알린다(Open Issues).
> 근거 줄 번호는 조사 시점(코드 `202078b`) 값이다 — 워커는 **줄이 아니라 심볼로 다시 찾는다**(원칙 P-4).
>
> **1 파일 = 1 work.** 이 판은 워커·파일 겹침 기준으로 여러 페이지로 나뉜다. 페이지마다 발주 → 구현 →
> 검수(reviewer) → 재수정 → 코디 커밋. 외부 서비스가 걸린 Phase 는 **실물 호출 1회**가 완료 조건이다.

## Meta

- **SPEC (정본)**
  - SPEC-008 v0.5.1 — §2(UX)·§4(Interface: 연결·방·메시지함·답장·카톡 수신 §4.6·프로필 · 기기 토큰 두 갈래 인증)·§5·§6 AC·§7
  - SPEC-009 v0.5.1 — 수집기(상주·**닫기=웹뷰 파괴**·카톡 실행/계정·기기 토큰 Bearer·방 목록 탐색 로컬·첨부·§3 경계 입출력)
  - SPEC-006 v0.6.0 — 「외부 채널 수집기 수용」 절(**닫기=웹뷰 파괴·프로세스만 메뉴 막대 상주(L-06·S-6·AC-T32 무변경)**·트레이·백그라운드·FDA·**웹 커맨드 정확히 일곱**·판 가르기·OAuth 외부 열기)
- **Decision**: DEC-008(accepted · D-01~D-50) · **Baseline**: BASE-006
- **시안(UX)**: `reference/2026-09-10-sc-meeting/package 2/`(Inbox.html·Settings.html) + `orchestration/work/strong-hajin-inbox/design-change-1~6.md`
- **운영**: RUNBOOK-002 · origin `https://ax.medisolveai.xyz`
- **코드(읽기만)**: `/Users/kknaks/git/toy_pr2/Strong_hajin` origin/main `202078b` · 카톡 DB 모듈 참조 = `~/git/toy_pr2/mykakao`(DEC-001·SPEC-001)

## 이 판의 원칙

| # | 원칙 | 근거 |
|---|---|---|
| P-1 | **SPEC 이 정본, WP 는 실행 계획.** 계약 문장이 갈리면 SPEC 을 따르고 Open Issues 에 올린다 | WORK-010 |
| P-2 | **쓰는 곳을 전부 센다.** 파일:줄은 출발점 — 같은 심볼·패턴을 grep 으로 전부 세고 시작 | 오케스트레이션 규칙 |
| P-3 | **소유 경계가 먼저다.** 연동·방·메시지·첨부·읽음은 연결한 회원 것 — 웹은 세션, 수집기는 기기 토큰. 남의 것 404(SPEC-008 §5 권한) | DEC-008 D-24·D-25 |
| P-4 | **외부 서비스는 실물 1회.** Gmail·슬랙·카톡 각 연결·수신·답장을 실제로 한 번 통과시키는 것이 완료 조건 | `feedback_real_e2e_before_done` |
| P-5 | **디자인 시스템·기존 코드 안에서.** 라우트는 `create_app` 한 자리 · 저장은 `LocalDirectoryMaterialStorage` 계열 · 워커는 `Worker(Settings.from_environment())` 틀 · DS 부품(DropZone·FileList 등) | WORK-008 P-2 · SPEC-008 §1 표 |
| P-6 | **카톡 DB 여는 모듈은 구현 몫.** mykakao 방식(DEC-001·SPEC-001)을 Rust 로 옮긴다 — 절차는 WP 가 적지 않는다. **안전 장치에 막히면 바로 코디에게** | SPEC-009 머리 · Open Issues |

## Work Summary

| 페이지 | 워커 | 무엇 | SPEC |
|---|---|---|---|
| SHELL-0 카톡 탐침 | frontend(Rust) | **BE-1 과 동시** — mykakao 방식으로 카톡 DB 읽기·방 목록 1회(가장 불확실한 모듈을 앞으로) | SPEC-009 §3 |
| BE-1 기반 | backend | 스키마(연동·고른 방·메시지·첨부 메타·읽음·보낸 답장·프로필 이미지·기기 토큰) · **동기화 상태 칸·NOTIFY 계약·모듈 분할** · 저장(hostPath) · 소유 검사 · 토큰 암호화 · env(Makefile·AX_WEB_ORIGIN) · 운영 인벤토리 · 연결/방/기기토큰 라우트 | §4.1·4.2·4.3·4.7(일부)·§5 |
| BE-2 연동 워커 | backend | 슬랙 Socket Mode · Gmail watch+Pub/Sub pull · 최초 백필 · 재시작 메우기 · 사람별 팬아웃 · 단일 레플리카 | §5 동기화 |
| BE-3 메시지함·답장·프로필·카톡 수신 | backend | 메시지함 목록·본문·읽음 · 첨부 중계 · 이미지 프록시(SSRF) · 사용자 WS + LISTEN/NOTIFY · 답장(슬랙·메일) · 프로필/비밀번호 · 카톡 수신 §4.6 | §4.4·4.6·4.7 |
| FE-a 메시지함 | frontend | 메시지함 surface(2/3열·폭 전체·네 상태) · 메일/슬랙/카톡 본문 · 첨부 · 답장 UI · WS | §2.1·2.2·2.8 |
| FE-b 설정·프로필 | frontend | 설정 세 연동(메일·슬랙·카톡) · 방 고르기 · 프로필 설정(이미지·AX 캐릭터 이동·비밀번호) | §2.3~2.6 |
| SHELL 셸·수집기 | frontend(셸) | SPEC-006 v0.6.0 개정(**닫기=웹뷰 파괴·프로세스 상주**·트레이·판 가르기·카톡 커맨드 셋·OAuth open_external) · Rust 수집기(카톡 DB·폴링·첨부·업로드·**기기 토큰 Bearer·키체인·store 커맨드**) | SPEC-009 · SPEC-006 |
| INFRA 인프라 | infra | 연동 워커 Deployment(replicas 1) · hostPath 마운트 · Secret · Pub/Sub SA 키 파일 마운트 · ingress body size | §5 운영 배치 |

## Code Surface

- **BE**: `backend/src/ax_workspace/` — 신규 모듈 `modules/external_channels/`(제안 · 이름은 구현) · `platform/persistence.py`(스키마) · `bootstrap/settings.py`(env) · `entrypoints/http.py`(라우트) · 신규 `entrypoints/external_worker.py`+`bootstrap/external_worker.py`(연동 워커) · `Makefile`(env 로드·local-stack·워커 타겟) · `migrations/manual/`
- **FE**: `frontend/src/`(features/inbox·settings 신규 · `App.tsx` navigation/surface · `lib/`) + 테스트
- **셸/Rust**: `frontend/src-tauri/`(수집기·셸 개정) + `frontend/src/lib/shell.ts`·`App.tsx`(카톡 커맨드·토큰 수신부) — **frontend 워커 소유**(WORK-006 §Phase 표 — `frontend/` 가 `src-tauri/` 를 덮는다)
- **INFRA**: `MediSolveAIDev/k8s_infra_mac`(차트) — **이 레포는 우리 쓰기 범위 밖**, infra 워커 몫
- **DB 없음인 곳**: FE·SHELL 은 BE 스키마를 만들지 않는다

### 파일 겹침 — 무엇을 나란히 태우나

- **BE-1 → (BE-2 ∥ BE-3)** — **나란히 가는 조건(W4-3)**: BE-1 이 `http.py`·`persistence.py`(**동기화 상태 칸 포함**)·
  `settings.py` 의 기반과 **모듈 골격**(BE-2 `sync_*.py` · BE-3 `inbox_*.py`)·**NOTIFY 계약**을 먼저 놓아야 둘이
  `persistence.py`·같은 모듈을 다시 열지 않는다. 그 조건이 서면 BE-2(신규 워커 파일 · http.py 안 건드림)와 BE-3
  (`http.py` 라우트)이 **파일이 안 겹쳐 나란히**. 조건이 안 서면 직렬
- **SHELL-0 ∥ BE-1**: SHELL-0(카톡 DB 탐침)은 스파이크라 다른 Phase 와 안 겹친다 — **지금 BE-1 과 동시**(W4-5)
- **FE-a ∥ FE-b**: feature 디렉터리가 달라 대체로 나란히. 단 `App.tsx`(navigation·surface 둘 추가)는 **공유** —
  한쪽이 먼저 두 surface 자리를 잡고 다른 쪽이 이어받거나, 코디가 App.tsx 조각만 순서를 잡는다(겹치면 코디에게)
- **SHELL**: `frontend/src-tauri/` 는 FE 와 안 겹치나 `lib/shell.ts`·`App.tsx` 수신부는 FE 와 **겹친다** — WORK-010
  Phase 3 처럼 그 두 파일 조각의 순서를 코디가 잡는다
- **동시에 같은 파일을 여는 워커를 둘 태우지 않는다**(WORK-006 원칙)

---

## Phase SHELL-0 — 카톡 DB 탐침 *(BE-1 과 동시 · 가장 먼저)*

- **Status**: TODO · **워커**: frontend(셸/Rust) · **파일**: `frontend/src-tauri/`(탐침 스파이크 · 버려도 되는 코드)
- **무엇이 끝나야 시작하나**: 없음 — **BE-1 과 나란히 지금** (W4-5 — 가장 불확실한 모듈을 앞으로 당긴다)
- **계약**: mykakao 방식(DEC-001·SPEC-001)을 **Rust 로** — 기기값+userId → 키 유도 · userId 복구 · **읽기 전용**으로
  로컬 카톡 DB 열기 · **방 목록 1회 추출**(1:1·단체·오픈채팅 제외). 절차는 구현 몫, 새로 설계하지 않는다
- **완료 조건(실물 · 코디 macOS)**: **방 목록이 나온다**(이름·종류). userId 복구가 이 기기에서 성립
- **막히면(I-1)**: 안전 장치·복호 실패로 막히면 **즉시 코디에게** — 그때 **범위 결정**(카톡만 뒤로 미루고 메일·슬랙만
  먼저 낼지)을 코디가 한다. 늦게(SHELL Phase) 터지면 BE·FE 다 끝난 뒤 카톡만 비므로 **앞으로 당겼다**
- **시험**: `cargo test`(키 유도·복구 단위) · 방 목록 수동 확인

## Phase BE-1 — 기반 (스키마·저장·소유·기기 토큰·env·연결 라우트)

- **Status**: TODO
- **무엇이 끝나야 시작하나**: SPEC-008 4차 검수 조건부 PASS(`review-spec-work-r4.md`) — **이미 발주됨**
- **워커**: backend · **파일**: `persistence.py`·`settings.py`·`http.py`·신규 모듈·`Makefile`·`migrations/manual/`
- **계약**
  - [ ] 스키마(드러나는 것은 SPEC-008 §4.1 · 전문은 여기 Domain/Schema): **연동**(회원 FK·종류 mail/slack/kakao·암호화 토큰·상태 connected/backfilling/disconnected/removed·소프트 딜리트) · **고른 방**(연동 FK·`room_id`(서버 내부)·`external_id`(슬랙 channel/카톡 chatId)·종류·이름·상태·`selected_rooms_version`) · **메시지**(원문 JSON·중복 키 슬랙 `(연동,channel,ts)`·Gmail `(연동,message id)`·카톡 **`(연동,chatId,logId)`**) · **첨부 메타**(이름·크기·MIME·출처 참조/카톡 저장 경로·expired) · **읽음**(사용자별) · **보낸 답장**(우리 기록) · **프로필 이미지 경로** · **기기 토큰**(회원 FK·해시·마지막 사용 시각·철회)
  - [ ] **동기화 상태 칸(W4-3)**: Gmail `historyId`·`watch` 만료시각 · 슬랙 방별 마지막 `ts`·team id · 백필 진행 건수 · 각 방/계정 **「마지막 반영 지점」**. BE-2·BE-3 이 `persistence.py` 를 다시 열지 않게 **BE-1 이 미리 만든다**
  - [ ] **모듈 골격(W4-3)**: `modules/external_channels/` 를 도메인/애플리케이션으로 쪼개 **BE-2 는 `sync_*.py`, BE-3 은 `inbox_*.py`** 처럼 파일이 안 겹치게 둔다
  - [ ] **`LISTEN/NOTIFY` 계약(W4-3)**: 채널 이름·페이로드(예 `{member_id, kind, kind_id}`)를 BE-1 이 정의 — BE-2 가 보내고 BE-3 WS 가 받는다
  - [ ] 저장: 카톡 첨부·프로필 이미지 = `LocalDirectoryMaterialStorage` 계열 hostPath(`platform/materials.py:26`) · DB 는 경로만 · 보존·파기 없음(소프트 딜리트만 · D-49 대체)
  - [ ] 토큰 **암호화 저장**: env 대칭키 하나(`AX_EXTERNAL_TOKEN_ENCRYPTION_KEY` · Fernet 류). 비밀번호 코드(`credentials.py`)는 해시라 전례가 없다 — 가역 암호화 모듈 신설
  - [ ] 소유·인증: 웹 라우트 `current_principal`(`http_auth.py:68`) · **기기 토큰 검증**(수집기용) · 남의 것 404
  - [ ] 연결 라우트: `POST …/{mail|slack}/connect`(`{authorize_url, state}`) · `GET …/callback`(state 로 회원·쿠키 아님·302 쿼리 목적지) · reconnect · disconnect(소프트 딜리트) · `GET /api/integrations` · `GET/POST/DELETE …/{id}/rooms`(슬랙·카톡 공통 · 카톡도 서버 저장) · `POST/GET/DELETE /api/device-tokens`(**세션 발급 · Bearer · 해시만 · §4.6 범위만 · 새 발급이 옛 것 철회**)
  - [ ] env 로딩: `Settings.from_environment()`(`:141`) 에 `GOOGLE_OAUTH_*`·`GMAIL_PUBSUB_*`·`GOOGLE_PUBSUB_SA_KEY_FILE`·`SLACK_CLIENT_*`·`SLACK_APP_TOKEN`·`AX_EXTERNAL_*` 추가 · `Makefile` 이 `~/.config/google/env`·`~/.config/slack/env` 를 `SONIOX_ENV` 방식(`Makefile:2·5`)으로 로드 · **local-stack 이 `AX_WEB_ORIGIN=http://127.0.0.1:5176` 을 넘긴다**(콜백 목적지 · W4-7)
  - [ ] 스키마 반영: 로컬 `schema_sync`(additive) · 운영 `backend/migrations/manual/*.sql`(인덱스 `.concurrent.sql`)
  - [ ] **HTTP 운영 인벤토리 갱신(W4-7)**: 새 라우트 수십 개를 `docs/unified-operations-inventory.json` 에 넣는다 — 없으면 `test_operation_inventory.py:131`(`test_inventory_includes_each_declared_http_operation`)가 `make verify` 에서 깨진다(AGENTS.md drift 규칙). BE-1·BE-3 시험에 포함
- **완료 조건(실물)**: 로컬에서 Gmail `connect`→Google 동의→`callback` 이 **state 로 회원을 찾아** 토큰을 암호화 저장(복호 왕복 1회) · 기기 토큰 발급·철회 왕복 · 남의 연동 404
- **시험**: `make verify`(PG) · 새 계약마다 테스트(state 검증·토큰 암복호·소유 404·소프트 딜리트·기기 토큰)

## Phase BE-2 — 연동 워커 (슬랙·Gmail 수집) *(BE-1 뒤 · BE-3 과 나란히)*

- **Status**: TODO
- **무엇이 끝나야 시작하나**: BE-1(스키마·토큰 저장·연동 레코드)
- **워커**: backend · **파일**: 신규 `entrypoints/external_worker.py`·`bootstrap/external_worker.py`·워커 서비스 모듈(http.py 안 건드림)
- **계약**
  - [ ] **단일 소유·단일 레플리카**: 슬랙 Socket Mode 는 앱 토큰 1개로 **이 워커 한 곳**에서만 연결(`SLACK_APP_TOKEN`). 틀은 `material_worker.py` 의 `Worker(Settings.from_environment())` 단일 루프
  - [ ] 슬랙: 이벤트 수신 → **사람별 팬아웃**(이벤트 1건 → 그 `(team,channel)` 고른 모든 연동에 복제 · 키 `(연동,channel,ts)`) · 최초 백필(API 허용 끝까지) · 재시작 메우기(마지막 지점 이후)
  - [ ] Gmail: `users.watch`(7일 → 매일 갱신) · Pub/Sub **pull** 구독 · history 로 증분 · 최초 백필(받은편지함 전체) · 재시작 메우기
  - [ ] 원문 그대로 저장(D-28) · 중복 키로 버림 · 새 메시지 도착을 **BE-3 의 사용자 WS 로 알림**(Postgres `LISTEN/NOTIFY` 로 back 에 전달)
- **★3 — 슬랙 완료 조건을 로컬에서 재는 법**: 슬랙 연동 레코드는 OAuth 콜백으로만 생기고 그 콜백은 **https 라
  운영에서만** 된다(S8 §4.2 · RES). 그래서 **개발 전용 토큰 주입 make 타겟**을 둔다 — 로컬에서 `~/.slack_test_token`
  (실측 때 받은 사용자 토큰 · RES)을 **「연결된 슬랙 연동」 레코드로 넣는다**. **운영 빌드·프로파일에서는 거절**
  (`X-Demo-Persona` 와 같은 결 · 운영 프로파일에서 거절하는 시험 1개). 이 타겟으로 로컬에서 Socket Mode 수신·팬아웃·
  답장을 잰다. **「슬랙 연결」 OAuth 버튼 흐름 자체는 운영 반영 뒤 확인**(P-6)
- **완료 조건(실물)**: (로컬 · 주입 타겟) 슬랙 **메시지 1건 수신→저장→팬아웃** · 답장+파일 전송 1회 / Gmail **받은편지함
  수신 1건 백필+실시간 1건** · 워커 재시작 뒤 빠진 구간 메움 확인 / (운영) 슬랙 OAuth 버튼 연결
- **시험**: 워커 단위 테스트(팬아웃·중복 버림·메우기 경계) · **슬랙 토큰 주입 타겟이 운영 프로파일에서 거절** · `make local-stack` 에 연동 워커 타겟 추가(§INFRA·W4-7)

## Phase BE-3 — 메시지함·답장·프로필·카톡 수신 API *(BE-1 뒤 · BE-2 와 나란히)*

- **Status**: TODO
- **무엇이 끝나야 시작하나**: BE-1(스키마·소유·기기 토큰)
- **워커**: backend · **파일**: `http.py`(BE-1 뒤 이어 씀)·서비스 모듈·WS
- **계약**
  - [ ] 메시지함: `GET /api/inbox/messages`(출처·미읽음·cursor) · `GET …/mail/{id}`(**소독 안전본 HTML**) · `GET …/rooms/{id}/messages`(페이지네이션·thread_ts) · 읽음(`…/read` up_to_ts·`read-all`)
  - [ ] 첨부: `GET …/mail/{id}/attachments/{aid}`·`…/rooms/{id}/attachments/{aid}`(메일·슬랙 = 그 토큰으로 중계·저장 안 함 / 카톡 = 저장본 · 만료 410) · `GET …/mail/{id}/remote-image?u=`(**SSRF: 본문 URL만·http(s)·사설/루프백/메타데이터 거절·이미지 MIME·크기 상한**)
  - [ ] 실시간: **새 사용자 WS `/api/inbox/stream`**(= 사용자 사건 채널 · 회의 WS `http.py:1023` 아님) · 워커→back `LISTEN/NOTIFY`
  - [ ] 답장: 슬랙(`…/rooms/{id}/reply` · 채널·스레드·내 이름·첨부 files:write·`Idempotency-Key`·결과 WS) · 메일(`…/mail/{id}/reply` · 답장/전체 답장·합계 25MB·보낸 답장 기록) · **`202` 뒤 상류 429/5xx 은 실시간 사건으로 실패 통지**(S8 §4.4)
  - [ ] 프로필: `GET /api/organization/me`(+`profile_image_url`) · `GET/PUT/DELETE /api/profile/image`(즉시 저장·1MB) · `PUT …/assistant-character`(기존 재사용) · `POST /api/profile/password`(현재 확인·새 저장·**다른 기기 세션 일괄 revoke** — `auth_sessions.py` 에 회원 단위 revoke 신설)
  - [ ] 카톡 수신(§4.6 · **기기 토큰 Bearer 인증**): handshake(서버 고른 방 `{room_id, external_id=chatId, last_logId}`·`reset_at`·`selected_rooms_version` · **첫 handshake 가 연동 레코드 생성** W4-7) · messages(서버 고른 방 아니면 403·500건 · 중복 키 **`(연동,chatId,logId)`** · `aid`=**SHA-256("{연동}:{chatId}:{logId}:{seq}")**) · attachments(50MB) · status(30초·90초 off 판정 · 응답 `selected_rooms_version`)
  - [ ] **`reset-account` 는 웹 세션 라우트**(§4.3 · ★2 — 기기 토큰 아님) · **`selected_rooms_version` 올리기**(웹에서 방 추가·빼기 때 · W4-7) · **비밀번호 변경·회원 비활성 때 기기 토큰도 철회**(W4-7 · S8 §4.7)
- **완료 조건(실물)**: 메시지함 목록·본문·읽음 · 메일 답장·슬랙 답장+파일 실제 전송 1회 · 첨부 중계·이미지 프록시(사설 IP 거절) · 비밀번호 변경 뒤 다른 세션 로그아웃 · 카톡 업로드가 고른 방 외 403
- **시험**: 라우트별 테스트(소유 404·SSRF 거절·Idempotency·25MB·403·세션 revoke) · WS 연결·사건 수신

## Phase FE-a — 메시지함 *(BE-1·3 계약 고정 뒤)*

- **Status**: TODO · **워커**: frontend · **파일**: `features/inbox/`(신규)·`App.tsx`(surface 추가 — FE-b·SHELL 과 조율)
- **계약**
  - [ ] 메시지함 surface(내비 항목) · 출처 전환(전체/메일/슬랙/카톡) · 미읽음 수 · 카드(메일 단건·방 카드) · **읽음만**(업무 행동 없음)
  - [ ] 본문 **폭 전체** · 메일(머리 표·**샌드박스 iframe**(allow-same-origin·allow-popups·allow-scripts 금지)·인용 `<details>`·원격 이미지 차단·첨부) · 슬랙(대화방·날짜·5분 묶음·서식·URL 미리보기·리액션 읽기·**스레드 오른쪽 3열 패널**·슬랙에서 열기) · 카톡(입력창 없는 대화방·첨부 종류·만료)
  - [ ] 답장 UI: 슬랙 입력창·스레드 답글(내 이름·첨부·보내는 중/실패) · 메일 답장/전체 답장(작성 칸·칩·Re:·DropZone 25MB)
  - [ ] 실시간: `/api/inbox/stream` WS 구독 → 새 메시지·답장 결과 갱신 · 네 상태(기본·빈·로딩·오류)
  - [ ] 슬랙 렌더(blocks 우선·mrkdwn 대체·멘션 이름 풀기)는 프론트 책임 · DS 부품 재사용
  - [ ] **iframe 높이 = 부모가 `contentDocument.scrollHeight` · 링크 = 부모가 iframe 클릭 가로채**(웹 새 탭 / 데스크톱 `open_external`) · **아바타는 `GET /api/profile/image`** 로 그린다(SideNav·대화 · W4-7·AC-18b)
- **완료 조건(실물)**: 웹에서 메일·슬랙·카톡 방 열람·읽음 · 답장 전송 · 스레드 3열 · HTML 메일이 iframe 안에서 안전하게(스크립트 안 돎) · 좁은 화면은 공통 최소 폭(1542px)
- **시험**: `make frontend-test`·`tsc`·build · 계약별 테스트

## Phase FE-b — 설정·프로필 *(BE-1·3 계약 고정 뒤 · FE-a 와 나란히)*

- **Status**: TODO · **워커**: frontend · **파일**: `features/settings/`(신규)·`App.tsx`(surface·설정 진입점)·`features/assistant/`(캐릭터 진입점 제거)
- **무엇이 끝나야 시작하나**: BE-1·3 계약 고정 · **카톡 방 추가·「이 Mac 연결」은 SHELL 의 `lib/shell.ts` 바인딩 뒤**(W4-4) — SHELL 이 바인딩 타입 시그니처를 먼저 커밋하면 그만큼 나란히
- **계약**
  - [ ] 설정 surface(모달 아님) · 메일(「Google로 연결」·계정 여럿·실시간·끊김/다시 연결·해제 확인) · 슬랙(연결·방 고르기 모달·그룹 DM 실명·빼기) · **카톡**(상태 카드 · **앱 웹뷰에서만 방 추가 창**(Tauri 커맨드로 목록) · **고른 방 목록·빼기는 웹에서도**(서버 정본) · 못 읽음·계정 바뀜 문구 · 「Mac 앱 받기」=GitHub Releases)
  - [ ] 프로필 설정: 이름·소속·직책·직무 읽기 전용 · 이미지(DropZone·1MB·즉시 저장·삭제) · **AX 캐릭터 이동**(기존 모달 진입점 **둘**(`App.tsx:417` 설정·`:402` 신원 줄) 제거·프로필 설정에서 저장) · 비밀번호 변경(불일치·현재 틀림)
  - [ ] **「이 Mac 연결」 단추 + 기기 토큰 목록·철회 화면**(W4-7 · S8 §4.2) — 단추가 `POST /api/device-tokens` → 곧바로 `kakao_store_device_token` 으로 넘김(화면에 토큰 안 남김 · P-5)
  - [ ] 수집 실패 배너(메시지함 머리) · 알림 메뉴는 범위 밖(그대로)
- **완료 조건(실물)**: 웹에서 메일·슬랙 연결·방 추가·해제 · 프로필 이미지·캐릭터·비밀번호 변경 · 카톡 설정이 앱/브라우저에서 다르게 뜸
- **시험**: `make frontend-test`·`tsc`·build · 계약별 테스트

## Phase SHELL — 데스크톱 셸 개정 · Rust 수집기 *(SPEC-006 검수 뒤 · FE 와 lib/shell·App.tsx 조각 조율)*

- **Status**: TODO · **워커**: frontend(셸) · **파일**: `frontend/src-tauri/` + `frontend/src/lib/shell.ts`·`App.tsx`(수신부)
- **계약(셸 개정 — SPEC-006 v0.6.0)**
  - [ ] medi-ax: **닫기=웹뷰(창) 실제 파괴 · 앱 프로세스만 메뉴 막대 상주**(종료는 트레이 · 「열기」가 창 새로 만듦) — 창이 파괴되므로 **L-06·S-6·AC-T32 무변경**(`lib.rs:615-623` 그대로) · 트레이 아이콘 · 백그라운드
  - [ ] **웹에 여는 커맨드 정확히 일곱**(넷 + `kakao_list_rooms`·`kakao_collector_status`·`kakao_store_device_token`) · strong-hajin 은 넷
  - [ ] **판 가르기** = cargo feature(예 `kakao-collector`) — strong-hajin 판은 수집·트레이·FDA·카톡 커맨드가 **컴파일 안 됨** · 오버레이 키 시험(`lib.rs:841-846`)·`trayIcon` 금지 시험(`:853-855`) 판별 개정
  - [ ] 카톡 웹뷰 커맨드 **정확히 셋**(`kakao_list_rooms`·`kakao_collector_status`·`kakao_store_device_token`) — 고른 방 **저장은 서버 API**(커맨드 아님) · medi-ax 한정·capabilities 판별
  - [ ] OAuth 외부 열기 = `open_external`(기존 커맨드) · 시스템 설정 딥링크는 **네이티브가 직접**(open_external 은 http(s) 전용 `guard.rs:125-135`)
- **계약(Rust 수집기 — SPEC-009)**
  - [ ] 상주·카톡 실행 여부·로그인 계정·계정 바뀜 멈춤 · 폴링 2초 · 방 목록(1:1·단체·오픈채팅 제외)·메시지·첨부(사진/앨범/파일 즉시 받아 업로드·동영상/음성 메타·이모티콘·만료)
  - [ ] **기기 토큰 `Authorization: Bearer`** 로 서버 업로드/상태(키체인 보관·창 쿠키 아님) · 발급은 세션 웹 → `kakao_store_device_token` 으로 키체인 · handshake 로 서버 고른 방(`selected_rooms`) 받아 로컬 캐시 · status 응답 `selected_rooms_version` 으로 변경 감지
  - [ ] **FDA = 사용자 TCC 허용**(plist 키 아님) · 못 읽으면 `reason=permission`
  - [ ] ⚠ **카톡 DB 여는 모듈(키·userId·복호)은 구현 몫** — mykakao DEC-001·SPEC-001·`~/git/toy_pr2/mykakao` 를 Rust 로. **절차를 새로 설계하지 말고 그대로 옮긴다.** 막히면 코디에게(Open Issues I-1)
- **완료 조건(실물 · 코디 macOS)**: 앱에서 카톡 방 고르기(로컬 목록)→서버 저장→수집→메시지함 조회 · **창 닫아도(웹뷰 파괴·프로세스 상주) 수집 이어짐** · FDA 없을 때 안내 · 기기 토큰 왕복(발급·store·철회)
- **시험**: `cargo check`·`cargo test`·`cargo clippy -- -D warnings` · 셸 시험 판별 개정 통과 · **판 가르기 검증(W4-6)**: `SHELL_FLAVOR=medi-ax` → `--features kakao-collector` · **`make shell-final-preflight` 가 개인판(strong-hajin) 바이너리에 수집기 심볼·FDA 안내 없음을 확인**

## Phase INFRA — 운영 배치 *(BE 계약 고정 뒤 · 배포 전)*

- **Status**: TODO · **워커**: infra(`roles/strong-hajin/infra`) · **레포**: `MediSolveAIDev/k8s_infra_mac`(우리 쓰기 범위 밖)
- **계약**
  - [ ] **연동 워커 Deployment** 신설 · **kind 별 replicas 고정 1**(Socket Mode 단일 소유) · `values-prod.yaml` `worker.kinds` 에 추가
  - [ ] **hostPath 마운트**(카톡 첨부·프로필 이미지) — `/mnt/mac/strong-hajin/` 아래 외부 채널 디렉터리 · type `Directory` · **back 과 연동 워커 둘 다** 마운트
  - [ ] **Secret**: OAuth client·`AX_EXTERNAL_TOKEN_ENCRYPTION_KEY`·`SLACK_APP_TOKEN` → `secretRef`(`back.yaml:48-50`·`worker.yaml:39-41`) · **`GOOGLE_PUBSUB_SA_KEY_FILE` 은 Secret 볼륨 마운트**(파일이라 envFrom 불가)
  - [ ] **ingress `proxyBodySize`** 를 50MB 보다 크게(예 60m · `values.yaml:23`)
- **완료 조건**: 운영에 연동 워커 1/1 · 마운트·Secret 적용 · 50MB 업로드가 ingress 를 통과
- **시험**: Argo sync Healthy · 파드 상태

## Phase 반영 — 코디 로컬 실물 → 운영 *(전 Phase 뒤)*

- [ ] 코디 `make local-stack`+`make tauri-local` 로 **E2E 전체**(아래 Done Criteria 체크리스트)
- [ ] PR 하나(스쿼시) → main · 문서 PR 따로
- **★4 — 운영 반영 순서(선행 둘이 먼저 · RUNBOOK-002 §2-4 방식)**. hostPath 가 `Directory` 타입이라 디렉터리가
  없으면 **back·워커 전체가 `ContainerCreating` 에 멈춘다**(runbook-002:160-164). 스키마도 이미지보다 먼저 들어가야 한다:
  1. [ ] **노드 `mkdir`**: `/mnt/mac/strong-hajin/` 아래 외부 채널 첨부·프로필 이미지 디렉터리(limactl shell worker-1)
  2. [ ] **manual SQL 적용**(새 표 · 인덱스는 `.concurrent.sql`)을 운영 DB 에 **이미지보다 먼저**
  3. [ ] **Secret patch**(OAuth·앱 토큰·암호화 키 · **SA 키 파일은 Secret 볼륨 마운트**)
  4. [ ] **차트 PR**(hostPath 마운트 · 연동 워커 Deployment replicas 1 · `worker.kinds` · ingress body size)
  5. [ ] **이미지 태그**(back·front·연동 워커) → Argo 수동 sync
  6. [ ] medi-ax 데스크톱(수집기 들어감): **dmg 재빌드·서명·공증**(RUNBOOK-002 데스크톱 절) 후 사용자 전달
- 롤백은 **역순** — 이미지만 되돌리고 **SQL 은 additive 라 남긴다**(아래 Rollback)

## Pre-deploy Check

- [ ] 모든 Phase 검수 처리 · 코디 `make verify` 통과 · 사용자 E2E(웹 + macOS 앱)
- [ ] 비밀값: 운영 Secret 에 OAuth·앱 토큰·암호화 키·SA 키 파일 · 로컬 `~/.config/{google,slack}/env`
- [ ] 슬랙 앱 사용자 토큰 **11권한**(실측 10 + `files:write`) · Gmail OAuth 동의 화면(회사 GCP 내부 앱) · Pub/Sub 토픽·구독
- [ ] 외부 서비스 실물 1회씩: Gmail 연결·수신·답장 / 슬랙 연결·수신·스레드·답장·파일 / 카톡 수집·첨부
- [ ] 운영 origin redirect_uri 등록(슬랙은 운영만 · 메일은 운영+로컬 Google)

## 반영

- (운영 반영 때 적는다 — PR·이미지 태그·Argo sync·dmg)

## Rollback

- `values-prod.yaml` 태그를 직전 값으로 되돌려 머지 → 수동 sync. **단 BE 스키마가 늘었으므로** 데이터 되돌림은
  신중히 — 소프트 딜리트만 쓰고 물리 삭제가 없어(D-49 대체) 롤백은 이미지 레벨이고 데이터는 남긴다. 연동 워커
  Deployment 는 replicas 0 으로 내리면 수집만 멈추고 저장분은 보존
- 데스크톱: 직전 dmg 재설치
- 카톡 수집기는 **기기 토큰 철회**로 개별 중단 가능
- **외부 쪽 잔여(W4-9)**: 이미지를 되돌려도 Gmail `users.watch` 가 최대 7일 Pub/Sub 에 계속 쌓이고 슬랙 Socket Mode
  가 끊긴 채 남는다(해롭지 않음). **재반영 시 pull 구독 잔여는 history 메우기가 흡수한다**(중복 키로 버림)

## Done Criteria

- SPEC-008·009·006 의 AC 가 채워지고, 외부 서비스 실물 1회 증거가 있다(Gmail·슬랙·카톡)
- 사용자 E2E 체크리스트 통과 — `reference/2026-10-06-strong-hajin-inbox/사용자-설정.md`(설정 흐름) + 메시지함·답장·프로필 항목
- 운영에 반영됐고(web·워커·dmg) 로그 오류 0

## Open Issues

| ID | 무엇 | 다음 |
|---|---|---|
| **I-1** | **카톡 DB 여는 모듈이 안전 장치에 막힐 수 있다** — 키 유도·userId 복구·SQLCipher 복호는 mykakao 방식을 Rust 로 옮기는 구현 몫(SPEC-009 머리). 워커가 막히면 **절차를 새로 설계하지 말고 즉시 코디에게** | 코디가 mykakao 경로를 다시 지정하거나 범위를 조정 |
| **I-2** | 토큰 **가역 암호화**가 기존 코드에 전례 없음(`credentials.py` 는 해시) — 모듈 신설(`AX_EXTERNAL_TOKEN_ENCRYPTION_KEY`) | BE-1 에서 구현 · 방식은 SPEC-008 OQ-801(대칭키 하나) |
| **I-3** | 인프라 레포(`k8s_infra_mac`)는 **우리 쓰기 범위 밖** — 차트·Secret·ingress 는 infra 워커·운영 | INFRA Phase |
| **I-4** | `App.tsx`·`lib/shell.ts` 를 FE-a·FE-b·SHELL 셋이 건드린다 — 조각 순서를 코디가 잡는다(겹치면 직렬) | 발주 때 조정 |
| — | (진행 중 생기면 적는다) | — |

## Domain / Schema (구현 초안 — 전문 SoT 는 코드·migration)

- aggregate: **연동**(회원 소유 · 그 아래 고른 방·메시지·첨부·읽음 매달림, D-26) · **기기 토큰**(회원 소유)
- 중복 방지 키(전부 연동 범위 · D-25): 슬랙 `(연동, channel, ts)` · Gmail `(연동, message id)` · 카톡 `(연동, chatId, logId)` · `aid`=SHA-256(`{연동}:{chatId}:{logId}:{seq}`)
- 저장소 밖(hostPath): 카톡 첨부·프로필 이미지 바이트 · DB 는 경로만
- 마이그레이션: 새 표 다수 → 운영은 `backend/migrations/manual/`(인덱스 `.concurrent.sql`) · 로컬 `schema_sync`

## Related

- `_RESUME.md` §2 — 결정 원장 · `review-spec-008-009-r2.md` — 재검수 · `design-change-1~6.md` — 시안 변경
