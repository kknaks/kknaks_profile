---
type: spec
id: SPEC-003
title: "명동 PoC v2 — 시술 현황판(procedure) · KOS 데모 지점 실연동 계약"
version: 0.3.0
status: draft
product: cc-prototype
feature: procedure
created_at: 2026-10-21
updated_at: 2026-10-22
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-002-cc-nav-reservation|SPEC-002]]"
  works:
    - "[[work-003-procedure-board|WORK-003]]"
  releases: []
  related: []
---

# 명동 PoC v2 — 시술 현황판 계약

> 0.3.0(2026-10-22): **머지 전 코드 동기화** — 사용자 E2E batch 1(`e2e-feedback-batch-1.md` E2E-1 ~ 12) 처분 · `_RESUME.md` §2 10-21 뒤쪽 줄 ·
> 코드 `kknaksss/cc-prototype` main `329b543`(`procedure/back` · `procedure/front`)을 따른다. §1 · §2.3 · §3.2 · §3.3 · §4.4 · §5.1 · §5.4 · §5.7 · §5.11 ·
> §6 화면 정본 칸 · §6.1 · §6.3 · §7.1 ~ §7.4 · §8 · §9 · §10 · 부록 C(새) · **부록 D(새 — `_RESUME` §2 100줄 · 피드백 · 리뷰 · 처분 · 배포 사실 → 절 전수 대응표)**. 계정 · 권한 · 통역 · 푸시는 SPEC-004 가 정본(이 문서는 가리키기만). 바뀐 줄 끝에 `(0.3.0)`.
> 0.2.1(2026-10-21): 리뷰 r2 — N2 멈춘 op 상태 = `failed`(사유 · `blockedOpIds`) · N1 2xx 비정상 본문 = 동기화 실패(§4.2). 줄 끝 `(r2)`.
> 0.2.0(2026-10-21): 리뷰 r1 S1 ~ S12 · 처분(`orchestration/work/myeongdong-poc-v2/fix-decisions-r1.md`) 반영 —
> §2.1 · §2.2 · §2.3 env 하나 · 빌드 인자 · 개발용 가짜 보드(S6 · S7) / §4.1 시스템 계정 id(S1) / §4.2 서버 시작 조회 · 날짜 바뀜(S10) /
> §4.3 · §4.4 실패 뒤 KOS 값 · 뒤 op 멈춤(S3 · S4) / §4.6 id 모를 때(S12) / §5.1 · §5.10 · §8 같은 단계 flow-step(S2) /
> §6.8 좁은 화면(S8) / §7.2 · §7.5 기준값 · 10초 발행 · 토큰 로그(S5 · S9) / §10 OQ-516(S11). 바뀐 줄 끝에 `(0.2.0)`.

> `procedure/back`(FastAPI) · `procedure/front`(Next.js) 가 지킬 계약. 정책의 원천은 DEC-005(D-01 ~ D-34),
> 화면 정본은 확정 시안 `orchestration/work/myeongdong-poc-v2/design-user-r4/Ceramique 시술현황판 v2.dc.html`
> (읽기 리포트 `design-r3-read-report.md` P1 ~ P19 · `design-r4-read-report.md` Q1 ~ Q4). 시안과 DEC-005 가 다르면
> DEC-005 가 맞다(§6.7). 업무 흐름은 `reference/2026-10-12-cc-prototype/workflow-v2.md`.
>
> 근거 표기: `D-nn` = DEC-005 · `P-nn` / `Q-n` = 시안 읽기 리포트 · `HAR` = `_RESUME.md` §2 「(사실)」 줄 · `API` =
> `kos-demo-api.md` · `기본값` = 결정에 없어 이 문서가 고른 구현값(§10 에 같이 올린다).
> 이 레포는 public — 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · KOS id 값은 쓰지 않는다. env 는 이름만.

## 1. 범위

### 1.1 In

| 무엇 | 근거 |
|---|---|
| 새 기능 폴더 `procedure/`(front Next.js + back FastAPI + 새 SQLite DB). `cc/` 코드 · 시드 · 시나리오 · 동선 로직은 쓰지 않는다 | D-01 · D-15 |
| 테마 · 디자인 시스템은 `cc/` 에서 **복사**(기능끼리 import 금지) — §2.4 | D-02 |
| 시술 현황판 한 화면(간호 스테이션) + 같은 화면 오른쪽 「호출」 탭 = 의국 화면 | D-04 · D-17 · D-27 |
| ~~ccc 로그인 = 관리자 계정 1개(값은 env)~~ → 계정 = 관리자 · 의사 · 간호사 · **아이디 + 비밀번호**(SPEC-004 §3). 웹(간호 스테이션 · 의국)은 관리자 계정으로 쓴다 (0.3.0) | D-05 · `_RESUME` 10-21 OQ-601 닫음 줄 · SPEC-004 A-03 · A-16 |
| KOS 데모 지점 실연동 — 조회(10초 · 1시간) · 쓰기(방 넣기 · 담당자 · 호출 · 수락 · 진행 · 완료 · 작업 취소 · 귀가 대기) (0.3.0) | D-06 ~ D-11 · E2E-1 · E2E-3 |
| 조작 이벤트 로그 · KOS 반영 상태 | D-09 · D-12 · D-13 |
| ~~이번 목표 = 사용자 **로컬 E2E**. 배포(D-03)는 그 뒤 마지막 WP~~ → 로컬 E2E 뒤 **배포 완료**(2026-10-21 · `ccc.medisolveai.xyz` = procedure · WORK-004 WP10) (0.3.0) | D-03 · `_RESUME` 10-21 배포 완료 줄 |

### 1.2 Out

| 무엇 | 근거 |
|---|---|
| 시술실 고객 모니터 | D-34 |
| ~~시술실 태블릿 · 폰(디자인 2단계) · 개인 계정 · 앱 수락~~ → **SPEC-004(시술실 앱 · 계정 · 권한)로 들어갔다** — 이 문서 범위 밖일 뿐 Out 이 아니다 (0.3.0) | `_RESUME` 10-21 「디자인 2단계 = Flutter PoC 앱」 줄 · SPEC-004 A-01 · A-03 |
| 되돌리기(호출 · 수락 · [종료] 실수 포함) — 로그만 쌓는다 | D-28 · D-13 · D-34 |
| 시술 차트(KOS `assigneeMemo` · `doctorMemo` · `memo`) | D-34 |
| 라운지 / 내원현황(방 미리 배정). ~~원장 호출 휴대폰 알림~~ → SPEC-004 §5-1(APNs 푸시)로 들어갔다 (0.3.0) | D-34 · D-22 · SPEC-004 A-14 |
| KOS 「마취용」 계정 배정 · KOS 화면 직접 조작 | D-23 · D-10 |
| 운영 명동점 키 · 운영 지점 | D-06 |
| 연락처 · 생년월일 · 고객 메모 저장 | D-14 |
| 시술 준비(약물 · 장비) 표시 (0.3.0) | `_RESUME` 10-20 「시술 준비는 현황판에 표시하지 않는다」 줄 |

## 2. 폴더 · 실행

### 2.1 폴더 (코드 레포 `kknaksss/cc-prototype`)

```text
procedure/
  docker-compose.yml        # 로컬 한 줄 실행(back + front)
  README.md                 # 실행 · env · E2E 순서
  .env.example              # §2.3 — 이름만 · back + front 공용 하나 (0.2.0)
  back/                     # FastAPI · Python 3.12 · uv
    pyproject.toml · uv.lock · Dockerfile
    app/
      main.py · config.py · container.py
      api/          # router — HTTP 만 안다(§7)
      service/      # 규칙(§5) · 조작 → 이벤트 + KOS 반영 대기열
      domain/       # 상태 계산 · 도메인 예외(HTTP 모름)
      repository/   # SQLite · ORM 은 여기 밖으로 안 나간다
      kos/          # KOS 공개 · 내부 클라이언트 · 토큰 · 조회 루프 · 반영 루프(§4)
      schemas/      # front 계약(§7)
    tests/
  front/                    # Next.js · medikit · Ceramique
    .env.local              # 개별 실행 때만 · gitignore (0.2.0)
    package.json · Dockerfile
    app/ · components/ · lib/
```

- 계층 모양(router → service → repository · 도메인 예외 · 오류 형식 `{error:{code,message}}`)은 `cc/back` 과 같은 규약을 따른다. 코드는 새로 쓴다 — D-01
- 기능끼리 import 금지 — `procedure/` 는 `cc/` 를 참조하지 않는다(D-02)

### 2.2 실행 · 포트

| 무엇 | 값 | 근거 |
|---|---|---|
| 한 줄 실행 | `cd procedure && docker compose up --build` — 루트 `procedure/.env` 하나를 읽어 back 8700 · front 3700 을 띄운다. front 의 `NEXT_PUBLIC_*` 는 compose 가 같은 `.env` 에서 **`build.args`** 로 넘긴다(번들에 박히는 값) (0.2.0) | 브리프 · 처분 S6 |
| 개별 실행 | back `uv run uvicorn app.main:create_app --factory --port 8700`(모듈 import 때 앱을 만들지 않는다 — 시험이 실 env · 실 DB 를 건드리지 않게) · front `npm run dev`(포트 3700, `procedure/front/.env.local` 에 `NEXT_PUBLIC_API_BASE_URL`) — 절차는 README (0.2.0) | 처분 S6 · W12 |
| front 이미지 빌드 인자 기본값 | 비우거나 로컬 주소 — 배포 주소를 기본값으로 두지 않는다 (0.2.0) | 처분 W14 ① |
| 포트 | back **8700** · front **3700** — `cc`(8600 · 3600)와 겹치지 않게 | 기본값 |
| DB | SQLite 파일 하나(`PROC_DB_PATH`). compose 는 볼륨에 둔다 | D-15 |
| 서버 시작 때 | DB 테이블 생성 → KOS 토큰 2종 + 시스템 계정 id(§4.1) → 직원 · 방 조회 1회(**조회 시간과 상관없이**) → 조회 루프 · 반영 루프 · 10초 발행 시작 (0.2.0) | D-07 · D-08 · 처분 W8 |

### 2.3 env (`procedure/.env.example` 하나 — **값 없이 이름만**) (0.2.0)

back 이 읽는 것:

| 이름 | 뜻 | 근거 |
|---|---|---|
| `KOS_OPEN_API_BASE` | 공개 API 호스트(운영 호스트 · 데모 테넌트) | D-06 · API §1.2 |
| `KOS_OPEN_API_KEY` | 데모 지점 공개 API 키(값 원천 = ax-clinic-project `KOS_API_tenent_dev`). **운영 명동점 키 금지** | D-06 · D-07 |
| `KOS_INTERNAL_API_BASE` | 내부 API 호스트 | D-07 · HAR |
| `KOS_TENANT_ID` | 데모 테넌트 id(내부 API 경로 `{tenantId}`) | HAR |
| `KOS_SYSTEM_EMAIL` · `KOS_SYSTEM_PASSWORD` | 시스템 계정(내부 API `sign-in`) | D-07 · D-11 |
| `KOS_ZONE_ID` | 조회 구역 = 「4층」 id | D-08 |
| `KOS_EXCLUDE_ACCOUNT_IDS` | 원장 목록에서 뺄 계정 id(쉼표) — 「마취용」 등. 시스템 계정은 §4.1 의 시스템 계정 id(`get-user-account` `data.id`)로 자동 제외 (0.2.0) | D-11 · S1 |
| `KOS_POLL_SCHEDULE_SEC` | 일정 조회 주기(기본 10) | D-08 |
| `KOS_POLL_MASTER_SEC` | 직원 · 방 조회 주기(기본 3600) | D-08 |
| `KOS_POLL_WINDOW` | 조회 시간(기본 `09:00-21:00`, KST) | D-08 |
| `CCC_ADMIN_ID` · `CCC_ADMIN_PASSWORD` | ccc 관리자 계정 · 비밀번호(서버 시작 때 bcrypt 해시로 DB). 의사 · 간호사 계정 env(`CCC_DOCTOR_*` · `CCC_NURSE_*`) · APNs · 통역 env 는 SPEC-004 §2.3 (0.3.0) | D-05 · SPEC-004 §2.3 · 코드 `config.py` |
| `PROC_SESSION_SECRET` | ccc 로그인 토큰 서명 키 | 기본값 |
| `PROC_SESSION_HOURS` · `PROC_BCRYPT_ROUNDS` | 토큰 만료 시간(기본 12) · 비밀번호 해시 비용(기본 12 · 시험은 낮춘다). **`.env.example` 에는 없다**(코드 기본값으로 돈다) (0.3.0) | 코드 `config.py` |
| `PROC_DB_PATH` | SQLite 경로 | D-15 |
| `PROC_BACK_PORT` · `PROC_FRONT_ORIGIN` | 포트 · CORS 허용 출처 | 기본값 |
| `PROC_FAKE_BOARD` | **개발 전용** — 켜면 KOS 없이 가짜 스냅샷을 보낸다. 켜져 있으면 조작 API(§7.3)는 **403 `fake_board`** 로 막는다. **배포 env 에 넣지 않는다**(README · `.env.example` 주석에도) (0.2.0) | 처분 S7 |

front 가 쓰는 것: `NEXT_PUBLIC_API_BASE_URL`(back 주소) — compose 는 `build.args` 로, 개별 실행은 `procedure/front/.env.local` (0.2.0).

- `.env` · `.env.local` 은 gitignore. `.env.example` 에 값 · 예시 값 넣지 않는다(public)
- 시각은 KOS 와 주고받을 때 UTC, 화면 · 조회 시간 판정은 KST(Asia/Seoul) — API §3.3 필드 이름이 `…Utc`

### 2.4 테마 복사 목록 (D-02 — `cc-prototype` `origin/main` 기준)

| `cc/` 에서 | `procedure/front/` 로 | 어떻게 |
|---|---|---|
| `cc/front/app/styles/ceramique-theme.css` | `app/styles/` | 그대로 |
| `cc/front/app/styles/medikit-patches.css` | `app/styles/` | 그대로 + **시안 쪽 파일에만 있는 `[Button-3]`(`data-compact-buttons` 26px) · `[Badge-1]`(`data-badge-call` 파랑 외곽선) 블록을 더한다** — claude design `dda9a931` 의 `medikit-patches.css` 에서 읽어 온다(r3 리포트 §1 · §5) |
| `cc/front/app/globals.css` | `app/` | 그대로(`cc-btn` · `cc-input` 등 공통) |
| `cc/front/app/layout.tsx` | `app/` | 스타일 import 순서 · `data-product="ceramique"` · 글꼴만 |
| `cc/front/public/ceramique-logo-color.svg` | `public/` | 그대로 |
| `cc/front/{tailwind.config.ts, postcss.config.mjs, next.config.ts, tsconfig.json, eslint.config.mjs, global.d.ts}` | 같은 자리 | 그대로 |
| `cc/front/package.json` 의 의존성(`@medisolve-ai/medikit` 1.4.0 · `pretendard` 1.3.9 · next · react · tailwind 3) | `package.json` | 버전 그대로 · 이름 `procedure-front` · 포트 3700 |
| `cc/front/components/common/AppHeader.tsx` | `components/common/` | **모양만**(높이 57 · 로고 · 메뉴 간격 · 시계 · 로그아웃). 메뉴 = 「시술 현황」 하나(D-17) · 세션 = §7.1 |
| `cc/front/app/(main)/desk/page.tsx` 의 틀(사이드바 `Menu` · main 여백 · 제목 줄 · 토스트) | `app/(main)/procedures/` | **모양만**. 메뉴 항목 = 「시술 현황」 |
| `cc/front/components/desk/Aside.tsx` 의 패널 틀(폭 340 · 반경 12 · 그림자 · 검색 · 탭) | `components/` | **모양만** — 내용은 §6.4 |
| `cc/front/lib/memo.tsx` `MemoCard` · `cc/front/lib/time.ts`(`pad` · `fmtElapsed`) · `cc/front/lib/hooks.ts`(`useNow` · `useWide`) | `lib/` | 그 함수만 복사 |
| `cc/front/Dockerfile` · `.dockerignore` · `.gitignore` | 같은 자리 | 포트 · 이름만 바꿔 복사(배포 WP 에서 쓴다) |

## 3. 데이터 모델 (D-12 ~ D-15)

### 3.1 원칙

- 모든 행 = ccc id(주인, 정수 PK) + `kos_id`(있으면). KOS 에서 오는 행은 `kos_id` 로 맞춰 **덮어쓰고**, ccc 에만 있는 행은 ccc 가 만든다 — D-12
- 필드 이름은 ccc 이름. KOS 이름은 §3.3 대응표에만 — D-12
- 조작은 `event_log` 에 **추가만**(수정 · 삭제 없음). 다른 표의 ccc 열(`started_at` 등)은 그 이벤트의 투영 — D-13
- 개인정보는 화면에 쓰는 것만: 이름 · 읽기 · 국적 · 신규 여부 · 차트번호 — D-14
- SQLite. PoC 뒤 PG + Redis 는 그때 — D-15

### 3.2 테이블

**KOS 원천(조회 때 덮어씀 · D-09)**

| 테이블 | 필드 | 원천 |
|---|---|---|
| `staff` | `id` · `kos_id` · `name` · `role_tags`(json) · `active` · `is_doctor`(목록 포함 여부, §4.6 계산) · `synced_at` | KOS `getAccounts`(1시간) |
| `room` | `id` · `kos_id` · `zone_kos_id` · `title` · `order` · `synced_at` | KOS 내부 `get-rooms`(1시간) |
| `customer` | `id` · `kos_id` · `name` · `phonetic_name` · `nationality` · `is_new` · `chart_number` · `synced_at` | 일정 `visitor`(10초) |
| `visit`(일정 1건 = 카드 1장) | `id` · `kos_id` · `customer_id` · `zone_kos_id` · `flow_step` · `flow_step_at` · `order_memo` · `room_id` · `room_assigned_at` · `kos_updated_at` · `synced_at` · `seen_at`(ccc 가 처음 본 시각) · `present`(마지막 일정 조회에 있었나) · `open_task_seqs`(json — KOS 에서 끝나지 않은 작업 sequence, 종류 무관 · [귀가 대기] 취소 대상 · §5.7) (0.3.0) | 일정(10초) · 코드 `repository/db.py` |
| `procedure`(작업 1개) | `id` · `visit_id` · `kos_sequence`(`kos_id` 역할 — 일정 `kos_id` + sequence) · `kos_order` · `title` · `kos_status` · `payment_required` · `doctor_staff_ids`(json) · `assignee_staff_ids`(json) · `doctor_assigned_at` · `doctor_call_at` · `completed_at` · `synced_at` · `present`(KOS 작업 목록에 있나 · 빠지면 0, 행은 남김) · `room_kos_id`(작업에 들어간 방 — 호출 전 방 넣기 판단 · §5.4) · **`kind`**(`procedure` = KOS `PROCEDURE` · `etc` = `ETCETERA`「방 배정」 등 — 표시만) (0.3.0) | 일정 `tasks[]` type `PROCEDURE` **+ `ETCETERA`**(10초) — E2E-4 (0.3.0) |

**ccc 원천(KOS 에 없음 · D-09 · D-12)**

| 테이블 | 필드 | 근거 |
|---|---|---|
| `procedure` 의 ccc 열 | `started_at`([시작] 시각) · `started_event_id` | D-09 · D-32 |
| `anesthesia`(마취 회차) | `id` · `visit_id` · `started_at` · `ended_at`(null = 진행 중) · `start_event_id` · `end_event_id` | D-23 |
| `doctor_call`(호출) | `id` · `visit_id` · `kind`(`all` \| `one`) · `target_staff_id`(지정 원장 · `one` 일 때) · `created_at` · `event_id` · `reassigned_from_call_id`([다른 원장에게]로 만든 것이면) | D-24 · D-25 · D-27 |
| `doctor_call_item` | `call_id` · `procedure_id` | D-25 |
| `call_accept`(수락) | `id` · `call_id` · `procedure_id` · `doctor_staff_id` · `accepted_at` · `event_id` | D-27 |
| `visit` 의 ccc 열 | `home_requested_at`([귀가 대기] 누른 시각) | D-33 |
| `event_log` | `id` · `at` · `actor`(ccc 로그인 아이디) · `type` · `visit_id` · `payload`(json) | D-13 · D-27 |
| `kos_op`(KOS 반영) | `id` · `event_id` · `visit_id` · `seq`(그 visit 안 순서) · `api`(`open` \| `internal`) · `path` · `body`(json) · `expect`(json — 확인 조건) · `status`(`pending` 대기 · `sent` 보냄 · `confirmed` 확인 · `failed` 실패 — 앞 op 실패로 보내지 않은 op 도 `failed`(사유: 앞 op 실패로 보내지 않음) (0.2.0 · r2)) · `attempts` · `checks`(sent 뒤 `expect` 가 안 맞은 조회 수 · 2 면 재전송) (0.3.0) · `last_error` · `created_at` · `updated_at` | D-09 · D-12 |
| `kos_token` | `kind`(`open` \| `internal`) · `token` · `expires_at` · `account_kos_id`(internal 만) | D-07 |
| `sync_state` | `key`(`schedules` · `master`) · `last_ok_at` · `last_error` | 시안 제목 줄 「마지막 KOS 동기화」 |

`event_log.type`: `anes_start` · `anes_end` · `call_create` · `call_reassign_all` · `call_accept` · `proc_start` · `proc_finish` · `home` · `kos_failed` — D-13 · D-27 「로그에는 수락한 원장 · 시각 · 시술 · 호출 id」.
`call_accept` payload = `{callId, doctorId, procedureIds, byRole, source}`(`source` = `push` \| `app` \| `web` — SPEC-004 §3.5) · `home` payload = `{cancelSequences}`(§5.7) (0.3.0) — 코드 `service/actions.py`.

계정(`account`) · 기기(`device`) · 푸시 내역(`push_log`) 테이블은 SPEC-004 §3.1 · §5-1 (0.3.0).

### 3.3 KOS 필드 대응표

| ccc | KOS | 어디서 | 근거 |
|---|---|---|---|
| `staff.kos_id` · `name` · `role_tags` · `active` | `id` · `name` · `roleTags[]` · `activate` | 공개 `getAccounts` `data[]` | API §3.5 |
| `room.kos_id` · `zone_kos_id` · `title` · `order` | `id` · `zoneId` · `title` · `order` | 내부 `get-rooms` `data[]` | HAR(`시술현황_새로고침.har` 응답 모양) |
| `visit.kos_id` · `flow_step` · `flow_step_at` · `order_memo` · `kos_updated_at` · `zone_kos_id` | `id` · `flowStep` · `flowStepUpdatedDateTimeUtc` · `orderMemo` · `updatedDateTimeUtc` · `zone.id` | 내부 `get-schedules-grouped-by-zone` `data[].schedules[]` | HAR · API §3.3 |
| `visit.room_id` · `room_assigned_at` | `tasks[]` 중 type `ETCETERA` 이고 `room` 있는 작업의 `room.id` · `roomAssignedDateTimeUtc` | 같은 일정 | D-18 · D-22 · HAR(방 배정 작업 · room) |
| `customer.kos_id` · `name` · `phonetic_name` · `nationality` · `is_new` · `chart_number` | `visitor.id` · `name` · `phoneticName` · `nationality` · `isNew` · `chartNumber` | 같은 일정 | D-14 · API §3.3 |
| `procedure.kos_sequence` · `kos_order` · `title` · `kos_status` · `payment_required` | `tasks[].sequence` · `order` · `title` · `status` · `paymentRequired` | type `PROCEDURE` · `ETCETERA` 작업(그 밖 type 은 버림) (0.3.0) | D-22 · API §3.3 · E2E-4 |
| `procedure.kind` · `room_kos_id` | `tasks[].type`(`PROCEDURE` → `procedure` · `ETCETERA` → `etc`) · `tasks[].room.id` | 같은 작업 (0.3.0) | E2E-4 · E2E-1 · 코드 `kos/sync.py` |
| `visit.open_task_seqs` | `tasks[]` 중 `status` 가 `DONE` · `CANCELED` 아닌 작업의 `sequence`(종류 무관) | 같은 일정 (0.3.0) | E2E-3 · 코드 `kos/sync.py` |
| `procedure.doctor_staff_ids` · `doctor_assigned_at` | `tasks[].doctors[].id` · `doctorAssignedDateTimeUtc` | 같은 작업 | D-09(집도의) · HAR(수락 뒤 `doctorAssignedDateTimeUtc`) |
| `procedure.assignee_staff_ids` | `tasks[].assignees[].id` | 같은 작업 | HAR(담당 = 시스템 계정) |
| `procedure.doctor_call_at` | `tasks[].doctorCallDateTime` | 같은 작업 | D-09(호출 여부) · API §3.3 |
| `procedure.completed_at` | `tasks[].completedDateTimeUtc` | 같은 작업 | D-09 · HAR(완료 뒤 `completedDateTimeUtc`) |

저장하지 않는 KOS 필드: `visitor.phone` · `dateOfBirth` · `memo` · `gender` · 작업 메모 3종 · `taskTimers` · 수납 · 시술권 — D-14 · D-34.

## 4. KOS 연동

### 4.1 인증 · 토큰 (D-07)

| 종류 | 받기 | 실을 때 | 근거 |
|---|---|---|---|
| 공개 | `POST {KOS_OPEN_API_BASE}/open/authorization/commands/exchange-token` `{key}` → `{token}` | `Authorization: <token>`(Bearer 없음) | D-07 · API §1.2 |
| 내부 | `POST {KOS_INTERNAL_API_BASE}/common/v1/user/commands/sign-in` `{email, password}` → `{data{id, …, token}, tokenExpiredDateTimeUtc}` · 수명 ≈ 14시간 · refresh 없음 | `Authorization: Bearer <token>` | D-07 · HAR(`로그인.har` · 서버 호출 확인) |

- 토큰은 `kos_token` 에 **만료 시각 기준**으로 보관. 만료 10분 전이면 새로 받는다. 요청이 401 이면 **다시 받기 1회** 후 같은 요청 1회 — D-07
- 공개 토큰의 만료 시각은 응답에 없다 → 401 로만 갱신(만료 시각 칸은 비움) — API §1.2 「응답 키는 `token` 하나」
- **시스템 계정 id** = `sign-in` 직후 내부 `POST {KOS_INTERNAL_API_BASE}/tenants/{tenantId}/v1/account/queries/get-user-account` 의 `data.id`(테넌트 계정 id = `getAccounts` 의 id) → `kos_token.account_kos_id`. 담당자 지정 · 원장 목록 제외에 쓴다. `sign-in` 응답의 `data.id` 는 **사용자 id** 라 쓰지 않는다 — 담당자로 넣으면 KOS 가 200 을 주고 무시한다 (0.2.0) — D-11 · D-24 · S1(워커 실호출 2026-10-21)
- 키 · 비밀번호는 로그 · 오류 메시지 · 응답에 싣지 않는다

### 4.2 조회 (D-08)

| 무엇 | API | 본문 | 주기 | 근거 |
|---|---|---|---|---|
| 일정(시술 현황) | 내부 `POST /tenants/{tenantId}/schedule/v2/queries/get-schedules-grouped-by-zone` | `{zoneIds:[KOS_ZONE_ID], startDateTimeUtc, endDateTimeUtc}` = **오늘 KST 00:00 ~ 24:00** 을 UTC 로 | 10초 | D-08 · HAR |
| 직원 | 공개 `POST /account/open/v1/queries/get-accounts` | `{}` | 1시간 + 서버 시작 | D-08 · API §2 G |
| 방 | 내부 `POST /tenants/{tenantId}/schedule/zone/room/v1/queries/get-rooms` | `{zoneId: KOS_ZONE_ID}` | 1시간 + 서버 시작 | D-08 · HAR |

- **조회 시간 09:00 ~ 21:00 KST** 밖에서는 주기 조회를 하지 않는다(일정 · 직원 · 방 모두) — D-08. 단 **서버 시작 때 직원 · 방 1회는 조회 시간과 상관없이** 한다 (0.2.0) — 처분 W8
- **날짜가 바뀌면(KST 00:00) 전날 카드를 내린다** — 조회가 없어도 back 이 날짜를 보고 전날 일정을 스냅샷에서 뺀다 (0.2.0) — 처분 S10
- 구역은 「4층」 하나(`KOS_ZONE_ID`) — D-08
- 일정 범위 「오늘」 = 기본값(HAR 은 그날 일정 전부를 받았다)
- 조회 결과 반영 순서: ① 직원 · 방 upsert ② 일정 → `customer` · `visit` · `procedure` upsert(§4.3 덮어쓰기 규칙) ③ `kos_op` 확인(§4.4) ④ `sync_state.last_ok_at`
- 조회 실패(네트워크 · 5xx · 401 재시도 뒤 실패 · **그 밖의 예외 전부**)는 `sync_state.last_error` 에 남기고 화면은 마지막 값 그대로. 예외를 삼키지 않는다. 로그에는 예외 종류 · HTTP 상태만(본문 · 토큰 없음) (0.2.0) — 기본값 · 처분 W6
- **2xx 인데 본문이 JSON 이 아니거나 `data` 가 없으면 = 동기화 실패** — 카드는 지우지 않고 그대로 · `sync_state.last_error` 에 남긴다 (r2) — 리뷰 r2 N1 처분

### 4.3 덮어쓰기 · 기준 규칙 (D-09)

| 값 | 기준 | 조회 때 | 근거 |
|---|---|---|---|
| 일정 존재 · 고객 · 오더 메모 | KOS | 덮어씀 | D-09 |
| 시술 목록(작업 추가 · 빠짐) · 제목 · 순서 | KOS | 덮어씀. KOS 에서 빠진 작업은 ccc 에서도 목록에서 뺀다(행 · 이벤트는 남김) | D-09 · D-13 |
| 결제(`payment_required`) | KOS | 덮어씀 | D-09 · D-21 |
| 방 · 방 배정 시각 | KOS | 덮어씀 — KOS 는 완료해도 `room` 을 지우지 않는다 | D-09 · D-33 · HAR(`시술완료_상태.har`) |
| 고객 단계(`flow_step`) | KOS | 덮어씀. **반영 대기 중인 `changeFlowStep` 이 있으면 덮어쓰지 않는다** | D-09 |
| 시술 완료 · 완료 시각 | KOS | 덮어씀. 반영 대기 중인 `change-tasks-complete` 가 있으면 그 작업은 덮어쓰지 않는다 | D-09 |
| 집도의(`doctors`) · 담당자 · 호출 여부(`status` WAITING · `doctorCallDateTime`) | KOS | 덮어씀. 반영 대기 중인 호출 · 수락이 있으면 그 작업은 덮어쓰지 않는다 | D-09 |
| 마취 회차 · [시작] 시각 · 호출 기록 · 지정 원장 · 수락 기록 · [귀가 대기] 누른 시각 | ccc | 조회가 건드리지 않는다 | D-09 · D-12 |

「반영 대기 중」 = 그 visit 에 `status ∈ {pending, sent}` 인 `kos_op` 이 있고 그 op 이 그 필드를 바꾸는 것. `failed` op 은 대기가 아니다 — **실패 뒤에는 KOS 값을 따른다**(D-09 KOS 기준) (0.2.0) — S3

- 방(room)이 KOS 에서 비면 §5.1 조건 3 에 따라 카드가 사라진다 — 맞는 동작으로 둔다(KOS 는 완료로 room 을 지우지 않는다 — HAR) (0.2.0) — 처분 W9

### 4.4 KOS 반영 — 대기열 · 확인 · 재전송 · 실패 (D-09)

- ccc 조작 1번 = `event_log` 1줄 + `kos_op` 0 ~ 2줄(§8). 조작 응답은 KOS 를 기다리지 않는다 — ccc 상태를 먼저 바꾸고 「KOS 반영 중」 — D-09
- **같은 visit 의 op 은 만든 순서대로** 보낸다. ~~앞 op 이 `confirmed` 또는 `failed` 가 된 뒤 다음~~ → **앞 op 이 2xx(`sent`)면 확인을 기다리지 않고 바로 다음 op** 을 보낸다(방 → 담당자 → 호출 3단계가 조회 주기를 2 ~ 3번 기다려 KOS 에 20 ~ 30초 늦게 뜨던 것). 앞 op 이 오류(`pending` 으로 돌아옴)면 그 visit 은 거기서 멈춘다 (0.3.0) — D-24 · HAR · E2E-6
- 조작 직후 back 이 반영 루프를 깨워 새 op 을 **바로** 보내고, 보낸 것이 있으면 **1.5초 뒤 일정 조회 1회**로 확인을 빨리 찍는다(`QUICK_SYNC_SEC`). 조작 직후 보내기는 재전송 대기(`attempts > 0`) op 을 만나면 그 visit 에서 멈춘다(재전송은 조회 주기 몫) (0.3.0) — E2E-6 · 코드 `kos/runtime.py` · `kos/ops.py`
- 보내기: `pending` → 호출 → HTTP 2xx 면 `sent`. 4xx · 5xx · 네트워크 오류면 `attempts+1` 하고 `pending` 으로 둔다
- 확인: 다음 일정 조회에서 `expect` 가 KOS 값과 맞으면 `confirmed`(§8 「확인」 칸). 보냈다가 거절돼 `pending` 인 op 도 KOS 값이 이미 맞으면 `confirmed`(같은 단계 flow-step 400 — §8)
- **뒤 op 이 같은 값을 다시 바꿨으면 앞 op 은 `confirmed`** 로 본다 — 예: 호출(`WAITING`) 뒤 수락(`READY`) · `PROCEDURE` 뒤 `PROCEDURE_DONE`. 확인을 기다리지 않고 이어 보내므로 앞 op 의 확인 조건이 더는 맞을 수 없어서(재전송하면 KOS 를 되돌린다) (0.3.0) — 코드 `kos/ops.py` `superseded`
- 재전송: `sent` 인데 조회 2번 동안 `expect` 가 안 맞거나, `pending` 으로 돌아온 op 은 다음 조회 주기에 다시 보낸다 — 기본값
- 실패: `attempts` 가 3 에 닿으면 `failed` + `event_log(kos_failed)` — 기본값(횟수) · D-09
- **실패 뒤 같은 visit 의 뒤 op 은 보내지 않고 멈춘다** — 상태 `failed`(사유: 앞 op 실패로 보내지 않음) · 멈춘 op id 는 그 `event_log(kos_failed)` 의 `payload.blockedOpIds` 에 (r2). 담당자 지정이 실패하면 그 뒤 호출을 보내지 않는다(D-24 순서) (0.2.0) — S4
- **실패 뒤 KOS 기준 필드는 KOS 값으로 돌아간다**(다음 조회부터 덮어쓴다 · §4.3). ccc 에만 있는 기록(이벤트 · 호출 · 수락 · [시작] 시각)은 지우지 않는다(되돌리기 없음 — D-28). 카드의 「KOS 반영 실패」는 **그 visit 의 다음 op 이 `confirmed` 될 때까지 남는다** (0.2.0) — S3 · 처분 W1
- 복구 방법은 §10 OQ-509 — D-28
- 조회 시간 밖에도 쓰기는 보낸다(조회만 시간 제한). 확인은 다음 조회 시간에 — 기본값

### 4.5 쓰기 API 표 → §8

### 4.6 원장 목록 (D-11)

- `staff` 중 `role_tags` 에 `DOCTOR` 가 있고 `active = true` 인 계정 — D-11 · API §3.5
- 빼는 것: 시스템 계정(`kos_token.account_kos_id` — §4.1) · `KOS_EXCLUDE_ACCOUNT_IDS`(「마취용」 등) — D-11
- **시스템 계정 id 를 모르면**(`get-user-account` 실패 등) 원장 목록을 **갱신하지 않는다 — 이전 값 유지** (0.2.0) — S12
- 데모에서는 시스템 계정이 KOS 원장 태그를 **가진 채로 둔다**(사용자가 KOS 에서 호출 알림을 직접 보려고) — ccc 원장 목록에서는 계속 계정 id 로 뺀다. 운영에서는 시스템 계정에 원장 태그를 주지 않는다 (0.3.0) — `_RESUME` 10-21 「데모에서는 시스템 계정이 원장 태그를 가진 채로」 줄
- 담당자 · 집도의 표시에서도 같은 계정은 이름을 보이지 않는다(시스템 계정이 담당자로 들어가도 「담당의」가 아니다) — D-11 · D-24
- 「비어 있음」 = ccc 에서 그 원장이 집도의인 **진행 중 시술이 없음** — `_RESUME.md` 10-21 ③ 기본값 줄

## 5. 상태 · 규칙

### 5.1 카드에 나오는 조건 (D-21 · D-22)

다음을 모두 만족하는 일정 = 카드 1장:

1. 구역 = 「4층」, 오늘(KST) 일정. 날짜가 바뀌면(KST 00:00) 전날 카드는 내린다 (0.2.0) — D-08 · S10
2. `flow_step ∈ {PROCEDURE_WAITING, PROCEDURE, PROCEDURE_DONE}` — D-21(시술 대기가 되면 생긴다) · D-33(귀가 대기 카드는 흐리게 맨 뒤). **`PROCEDURE_DONE`(귀가 대기) 카드는 데스크가 귀가(KOS `COMPLETED`) 처리할 때까지 판에 흐리게 남고, `COMPLETED` 가 되면 사라진다** — 데스크 귀가는 지금 KOS 화면 (0.3.0) — E2E-9(E2E-8 되돌림) · `_RESUME` 10-21 「[귀가 대기] = KOS 「방 배정」 등 남은 작업 취소」 줄
3. **방이 있다**(§3.3 `visit.room_id`) — 방 없는 고객 = 라운지 대기 = 안 나온다 — D-22
4. 수납 전(`payment_required` 인 시술이 있음)이어도 띄우고 「수납 필요」 표시 — D-21

- ~~시술 목록 = type `PROCEDURE` 작업만. 「방 배정」 등 ETCETERA 작업은 시술 목록에 안 보인다~~ → **ETCETERA(「방 배정」 등)도 스냅샷에 실린다** — `procedures[].kind = "etc"` · 읽기 전용(제목 + KOS 상태) · 호출 · 시작 · 종료 · 「전부 완료」 · 「수납 필요」 판정에서 빠진다(규칙은 `kind = procedure` 만 본다). KOS `CANCELED` 작업은 목록에서 뺀다(OQ-506) (0.3.0) — E2E-4 · 코드 `domain/rules.py` `items` · `procedures`
- 현황판(웹)이 `etc` 줄을 **그리지 않게** 하는 것은 E2E-10 으로 기록만 됐다 — 코드(웹)는 아직 카드 맨 위에 그린다 · 앱은 그리지 않는다(SPEC-004 §6.0) → §10 OQ-517 (0.3.0)
- 카드가 생기는 때 = 조회 주기만큼 뒤(최대 10초) — D-08 · D-21

### 5.2 고객 상태 (D-32 · D-33)

| ccc 상태 | 화면 | KOS `flowStep` | 바뀌는 때 |
|---|---|---|---|
| `waiting` 대기 | 「시술 대기」 Badge `warning` | `PROCEDURE_WAITING` | 카드가 생길 때 |
| `doing` 진행 | 「시술 진행」 Badge `primary` | `PROCEDURE` | 그 고객의 **첫 [시작]**(ccc 즉시 → KOS `changeFlowStep(PROCEDURE)`) |
| `home` 귀가 대기 | 「귀가 대기」 Badge `neutral` · 카드 흐림 0.55 · 맨 뒤 | `PROCEDURE_DONE` | [귀가 대기](ccc 즉시 → KOS `changeFlowStep(PROCEDURE_DONE)`) |

- 상태 = KOS `flowStep` 에서 읽는다. 반영 대기 중이면 ccc 가 바꾼 값 — D-09
- 마취는 고객 상태가 아니다(§5.3). 「마취 중」은 Badge 자리에 `purple` 로 덮어 보일 뿐 — D-23 · P2
- 「확인 필요」(§5.8)는 Badge 자리를 `danger` 로 덮는다 — 시안 `badgeVariant`

### 5.3 마취 (D-23)

- 고객(visit) 단위 · 시술에 묶지 않음 · 여러 회차 · **동시 진행 1개**
- [마취 시작] · [마취 종료]는 고객 상태 **대기 · 진행 어느 때나** — 시안(시술 대기에서만 · `anesCtl`)을 고친다. 귀가 대기 카드에는 버튼 없음(시안 `hasBtns`)
- KOS 호출 없음 · 「마취용」 배정 안 함 — ccc DB 만
- 표시: 진행 중이면 「마취 · NN분 경과」(`text-purple`, **20분 이상이면 `text-red`**) · 끝난 뒤는 「완료 N분」(**마지막 회차만**) · 한 번도 안 했으면 「안 함」 — P2 · P15 · 시안 `anesSum`

### 5.4 호출 (D-24 ~ D-26)

- 카드에서 **대기 시술**을 체크(줄마다 · 「전체 선택」) → 카드 아래 [의사 호출 · N건] → 팝오버에서 「모든 의사」 또는 원장 한 명 → 보내기 — D-24 · P6 · P7 · Q1 · Q2
- 호출 1번 = `doctor_call` 1행(만든 시각 · `kind` · 지정 원장) + 고른 시술마다 `doctor_call_item`. **쌓기만** 한다(지우거나 고치지 않음) — D-25
- **유효 호출** = 그 시술이 들어간 **가장 최근 호출**. 같은 시술을 다시 호출하면 그 시술은 새 호출로 넘어간다(이미 수락된 시술이어도) — D-25 · `_RESUME.md` 10-21 「새 호출이 생기면」
- 호출 대상 = **대기 시술만**. 진행 · 완료 시술은 체크칸 꺼짐 · 원장을 못 바꾼다 — D-26
- 「지정」 호출도 KOS 요청은 「모든 의사」와 같다(지정 원장은 ccc 만) — OQ-501
- KOS: ① **`change-tasks-room`(카드 방 = 「방 배정」 작업의 방을 고른 시술 작업에 덮어쓴다 — 시술 작업에 다른 방이 있어도)** → ② `change-tasks-assignees`(담당 = 시스템 계정) → ③ `call-tasks-doctors`(고른 시술의 sequences). 고른 작업이 이미 다 그 방이면 ① 은 보내지 않고 `confirmed` 로 쌓는다. 방이 없는 시술 작업을 호출하면 KOS 가 400 `roomId NotFound` 를 준다 (0.3.0) — D-24 · §8 · E2E-1 · `_RESUME` 10-21 「`call-tasks-doctors` 400 = 시술 작업에 방이 없을 때」 줄

### 5.5 수락 · 다른 원장에게 (D-27 · D-28)

- 어디서 = 오른쪽 「호출」 탭(의국 화면) — 원장이 자기를 골라 [수락] — D-27
- **받는 시술** = 그 호출이 **유효 호출인 시술 중 아직 수락 안 된 것만** — 시안 P11(수락 전 호출 전부)을 고친다 — D-27
- 전체 호출: 원장 목록(비어 있는 원장 먼저)에서 고르고 [<원장> 수락] / 지정 호출: [수락](지정 원장으로) — D-27 · P8 · P9
- [다른 원장에게](지정 호출만) = 같은 시술(그 호출에서 아직 받을 것)로 **「전체」 호출을 새로 만든다**. 기존 지정 호출은 그대로 남는다(유효 호출이 새 것으로 넘어간다) — D-27 · D-25
- KOS: `change-tasks-doctors`(받는 sequences · 고른 원장 id). [다른 원장에게]의 KOS 요청 = §5.4 호출과 같다 — D-27 · §8
- [되돌리기] 없음(토스트 · 호출 탭 모두) — D-28
- 호출 탭에 나오는 호출 = **받을 시술이 남은 호출만**(유효 호출이 그것이고 미수락인 시술이 1개 이상) — `_RESUME.md` 10-21 ③④

### 5.6 [시작] · [종료] (D-29 ~ D-32)

- 지금은 현황판 카드의 시술 줄에서 누른다(원칙은 시술실 태블릿 · 폰 — 나중) — D-29 · P3
- **[시작] 켜짐**: 시술이 대기이고 귀가 대기 카드가 아니며
  - 유효 호출이 있으면 → 그 호출에서 **이 시술이 수락됨**
  - 유효 호출이 없으면 → **담당의가 있음**(KOS `doctors` 에 원장 목록 계정이 있음)
  - 새 호출이 생기면 수락 전까지 꺼짐(유효 호출이 바뀌므로 자동) — D-30 · P4
- 순서 · 동시 진행 수는 막지 않는다 — D-30 · P5
- [시작] = ccc `started_at`(지금) · 집도의는 KOS 값 그대로. 그 고객의 첫 [시작]이면 KOS `changeFlowStep(PROCEDURE)` — D-32
- **[종료] 켜짐**: [시작]한 시술(진행)에만 — D-31
- [종료] = KOS `change-tasks-complete`(그 작업 하나) → 완료. 완료 상태만 올린다 — D-32

### 5.7 [귀가 대기] (D-33)

- 시술이 **전부 완료**일 때만 보인다(그 전엔 버튼 자체가 없다 · 같은 자리는 [의사 호출]) — D-33 · Q1 · Q3
- = 방 빼기(라운지로). KOS ① **`cancel-flow-tasks`** — 마지막 조회에서 끝나지 않은 작업(`open_task_seqs`) 중 **시술 작업을 뺀 것**(「방 배정」 등)을 `reason: CANCEL` 로 취소 → ② `changeFlowStep(PROCEDURE_DONE)`. 남은 작업이 없으면 ① 은 만들지 않는다. 방 배정 취소는 시술 현황(ccc)이 한다 — ccc 가 ② 만 보내 KOS 에 「방 배정」이 준비중으로 남고 방이 안 비던 것 (0.3.0) — D-33 · E2E-3 · E2E-9 · 1차 HAR(KOS 화면 귀가 대기 = 같은 두 요청)
- 마지막 시술 완료로 방을 비우지 않는다 — [귀가 대기]까지 그 고객의 방 · 카드 — D-33
- 카드는 흐리게(0.55) 맨 뒤, 「귀가 대기 HH:MM」(`flow_step_at`) — **KOS `COMPLETED`(데스크 귀가)까지 남는다**(§5.1 조건 2) (0.3.0) — D-33 · 시안 `label` · E2E-9

### 5.8 「확인이 필요」 (D-20)

| 이유 | 기준 | 경과 시작점 | 근거 |
|---|---|---|---|
| 호출 미수락 | **5분** 이상 | 그 카드의 받을 시술이 남은 호출 중 가장 이른 `created_at` | D-20 · 시안 `CALL_LONG` |
| 마취 길어짐 | **20분** 이상 | 진행 중 마취 `started_at` | D-20 · 시안 `ANES_LONG` |
| 시술 모두 완료 · 귀가 대기 전 | 기준 없음(바로) | 마지막 `completed_at` | 시안 `needOf` — DEC 표에는 없음 → OQ-504 |

- 한 카드에 이유가 여럿이면 시안 순서(귀가 대기 전 → 마취 → 호출) 하나만 — 시안 `needOf`
- 목록 = 경과가 긴 순 · 「N분」 크게 · 「+N분 초과 / 기준 도달 / 기준 N분」 · 막대(기준 대비) — D-20 · P13 · P14
- 귀가 대기 카드는 대상 아님 — 시안 `needOf`

### 5.9 시술 상태 · 표시 순서

| ccc 시술 상태 | 조건 | 줄 문구(둘째 줄) | 오른쪽 | 근거 |
|---|---|---|---|---|
| `done` 완료 | KOS `status = DONE` | 「<원장> · HH:MM~HH:MM」 | 「완료」 Badge `neutral` | D-09 · 시안 #10 · #11 |
| `doing` 진행 | ccc `started_at` 있음 · 완료 아님 | 「<원장> · HH:MM 시작」 | [종료] solid blue | D-31 · 시안 |
| `wait` 대기 · 유효 호출 미수락 | | 「전체 호출 · 수락 전」 / 「<원장> 지정 호출 · 수락 전」 | 「호출함」 Badge(파랑 외곽선) + [시작] 꺼짐 | D-30 · 시안 #10 · #11 |
| `wait` · 유효 호출 수락됨 | | 「<원장> 수락 · 시작 가능」(파랑) | [시작] outlined blue | D-30 · 시안 |
| `wait` · 호출 없음 · 담당의 있음 | | 「<원장>」 | [시작] | D-30 |
| `wait` · 호출 없음 · 담당의 없음 | | 「담당의 미정」 | [시작] 꺼짐 | D-30 · 시안 #10 |

- 순서 = 완료(완료 시각 순) → 진행 → 대기(KOS `sequence` 순) — 시안 `procRows` · workflow-v2 §5. `etc` 작업은 그 위에 sequence 순(웹 `orderedProcs`) (0.3.0)
- KOS `status = CANCELED` 작업 → OQ-506
- 「시술 n / m 완료」 줄은 없다 — P16

### 5.10 상태 전이표

| 대상 | 지금 | 조작 / 사건 | 다음 | KOS | 근거 |
|---|---|---|---|---|---|
| 고객 | (없음) | KOS `PROCEDURE_WAITING` + 방 있음 조회 | `waiting` | — | D-21 · D-22 |
| 고객 | `waiting` | 첫 [시작] | `doing` | `changeFlowStep(PROCEDURE)` — 이미 KOS 가 `PROCEDURE` 면 보내지 않음(§8 같은 단계 규칙) (0.2.0) | D-32 · S2 |
| 고객 | `doing` | [귀가 대기](시술 전부 완료) | `home` | `changeFlowStep(PROCEDURE_DONE)` — 같은 규칙 (0.2.0) | D-33 · S2 |
| 고객 | 아무 상태 | KOS `flowStep` 이 다른 값으로 조회됨(반영 대기 없음) | KOS 값을 따른다 · 3 단계 밖이면 카드 사라짐 | — | D-09 · OQ-505 |
| 마취 | 없음 / 끝남 | [마취 시작](`waiting` · `doing`) | 진행 중 | — | D-23 |
| 마취 | 진행 중 | [마취 종료] | 끝남 | — | D-23 |
| 시술 | `wait` | [의사 호출] | `wait` · 유효 호출 = 새 호출(미수락) | assignees → call | D-24 · D-25 |
| 시술 | `wait` · 미수락 | [수락] | `wait` · 수락됨 · 집도의 = 고른 원장 | `change-tasks-doctors` | D-27 |
| 시술 | `wait` · [시작] 켜짐 | [시작] | `doing` | (첫 [시작]이면 flow-step) | D-30 · D-32 |
| 시술 | `doing` | [종료] | `done` | `change-tasks-complete` | D-31 · D-32 |
| 시술 | 아무 상태 | KOS `DONE` 조회 | `done` | — | D-09 |

### 5.11 버튼 활성 조건표

| 버튼 | 보임 | 켜짐 | 근거 |
|---|---|---|---|
| 줄 체크칸 · 「전체 선택」 | 귀가 대기 아닌 카드 | 그 시술이 `wait`(전체 선택 = `wait` 시술이 1개 이상) · 없으면 「호출할 대기 시술 없음」 회색 | D-26 · 시안 r4 #1 |
| 카드 아래 [의사 호출] | 귀가 대기 아님 · **시술이 전부 완료는 아님** | 체크한 `wait` 시술 ≥ 1 — 「의사 호출 · N건」, 없으면 「시술 선택 후 의사 호출」 꺼짐 | Q1 · Q2 · Q4 · D-24 |
| (스냅샷) `canCall` | — | 귀가 대기 아님 · 전부 완료 아님 · **호출할 수 있는(`pickable`) 시술(`kind = procedure`)이 1개 이상**. 시술 0개(「방 배정」 등 `etc` 만)인 카드는 `false` (0.3.0) | T6 · 코드 `service/board_service.py` |
| 팝오버 [<원장> 호출 / 모든 의사 호출] | 팝오버 열림 | 「모든 의사」 또는 원장 한 명을 골랐을 때(기본값 없음 → 「의사를 선택하세요」 꺼짐) | P7 |
| 카드 아래 [귀가 대기] | 귀가 대기 아님 · 시술 전부 완료 | 항상(보이면 켜짐) | D-33 · Q3 |
| [마취 시작] | 귀가 대기 아님 · 진행 중 마취 없음 | 항상 | D-23 |
| [마취 종료] | 진행 중 마취 있음 | 항상 | D-23 |
| 줄 [시작] | 귀가 대기 아님 · `wait` | §5.6 조건 | D-30 |
| 줄 [종료] | `doing` | 항상 | D-31 |
| 호출 탭 [<원장> 수락] | 전체 호출 카드 | 원장을 골랐을 때 | D-27 · 시안 #19 |
| 호출 탭 [수락] · [다른 원장에게] | 지정 호출 카드 | 항상 | D-27 |

조작 버튼은 「KOS 반영 중 · 실패」여도 막지 않는다(§4.4 대기열) — 기본값.

## 6. 화면 (시안 기준)

| 화면 정본 | 값 |
|---|---|
| 확정 시안(정책 기준) | `design-user-r4/Ceramique 시술현황판 v2.dc.html`(r3 · r4 읽기 리포트) |
| **구현 반영 시안 파일 이름**(코드 main `329b543` 화면 = E2E 수정 뒤를 다시 그린 시안) | claude design `dda9a931` 「Ceramique 시술현황판 v2 (구현 v3).dc.html」 — 장면 17(login · login-error · login-locked · board … narrow) · 원본 v2(r4)는 그대로 · 대응표 `orchestration/work/myeongdong-poc-v2/design-sync-frontend-report.md`(아카이브 뒤 같은 slug 로그) (2026-10-22) |

장면 이름은 시안 `scene` 값: `board` · `board-placement` · `memo-expanded` · `call-modal` · `call-modal-specific` · `all-done` · `panel-doctors`(= 호출 탭) · `panel-customers`.

### 6.1 경로

| 경로 | 화면 | 근거 |
|---|---|---|
| `/login` | 로그인 — **아이디 · 비밀번호 폼** · [로그인]. 헤더 없음. ~~계정 카드를 눌러 바로(비밀번호 검증 없음)~~ — 카드 · 계정 목록 없음. 웹은 관리자 계정으로 쓴다(역할 제한은 §10 OQ-518) (0.3.0) | D-05 · `_RESUME` 10-21 OQ-601 닫음 줄 · 코드 `front/app/login/page.tsx` |
| `/procedures/live` | 시술 현황판(시안 사이드바 `current-path`) | 시안 · D-17 |
| `/` · `/procedures` | `/procedures/live` 로 보낸다(로그인 안 했으면 `/login`) | 기본값 |

로그인 화면 모양 = `cc/front/app/login/page.tsx` 의 틀(입력 · 버튼 스타일)만 따른다. 별도 시안 없음 — D-02 · 기본값.

### 6.2 헤더 · 사이드바 · 제목 줄

- 헤더 = `AppHeader` 모양. 메뉴 = **「시술 현황」 하나**(시안은 「현황판 · 시술 현황 · 예약관리」 세 칸 → D-17 이 고친다). 오른쪽 = 시계 · 지점 이름 · 계정 표시 · 로그아웃 — D-17 · 시안 헤더
- 사이드바 = medikit `Menu`, 묶음 · 항목 모두 「시술 현황」 — 시안
- 제목 줄 = 「시술 현황」 + 「명동점 · 마지막 KOS 동기화 HH:MM:SS」(`sync_state.schedules.last_ok_at`) · 범례 Badge sm dot 5개(시술 대기 · 마취 중 · 시술 진행 · 확인 필요 · 귀가 대기) · [입실순 | 배치순] — 시안 · D-18
- 조회 시간 밖이면 동기화 문구 옆 「조회 시간 밖」, 조회 실패면 「동기화 실패」 — 기본값(§4.2)

### 6.3 가운데 — 오더지 카드 (D-17 ~ D-19 · 장면 `board` · `board-placement` · `memo-expanded` · `all-done`)

- 격자 `minmax(300px,1fr)` · 간격 8 · 한 줄 높이 같음 · 카드 흰 바탕 · 확인 필요만 빨간 테두리 — P1 · r3 #2 · #3
- **카드 높이**: 최소 높이 = **가운데 판 보이는 높이의 절반쯤**(판 안에 두 줄 — CSS 비율 계산 · `100cqh` 기준) · 내용이 길면 늘어난다 · **카드 안 스크롤 없음**(내용 다 · 오더 메모는 `MemoCard` 접기) · 아래 큰 버튼은 카드 바닥. **px 상수 금지** (0.3.0) — E2E-5 → E2E-12 · 코드 `front/app/(main)/procedures/live/page.tsx`
- 정렬: **입실순** = `room_assigned_at` 오름차순 · **배치순** = `room.order` 오름차순. 귀가 대기 카드는 그 뒤에(귀가 대기 시각 순) — D-18 · D-33 · 시안 `ordered`
- 카드 안 순서(D-19):
  1. 머리 — 방 이름(`title-lg-600`) · 「입실 HH:MM」 / 상태 Badge + 오른쪽 경과 글자 / 고객 줄(이름 한 줄 줄임 · 국적 칩 · 「첫내원/재내원」) + **「수납 필요」**(§6.7)
  2. 오더 메모 — `MemoCard` 3줄 · 120자 넘으면 접기 [펼치기 · 접기] — P19 · `memo-expanded`
  3. 마취 줄 — §5.3 · [마취 시작/종료] 26px(`data-compact-buttons`)
  4. 선택 줄 — 체크칸(일부면 「–」) · 「전체 선택 / N개 선택됨 / 호출할 대기 시술 없음」. 고르면 `bg-primary-100 border-primary` — r4 #1
  5. 시술 줄 — 줄마다 테두리 상자 · 체크칸 20 · 이름 · 둘째 줄(§5.9) · 오른쪽 버튼(§5.11) — r3 #9 ~ #11. `kind = etc` 작업은 지금 코드에서 **시술 줄 맨 위**에 제목 + KOS 상태 글자만(체크 · 버튼 · 배지 없음) — E2E-4. 빼는 것은 OQ-517 (0.3.0)
  6. 카드 아래 큰 버튼 하나(md · 꽉 찬 폭 · `data-fill-buttons`) — [의사 호출 · N건] 또는 [귀가 대기] — Q1 · Q2 · `all-done`
- 「KOS 반영 중」 / 「KOS 반영 실패」 — 카드 머리 오른쪽 경과 글자 자리 아래 작은 글자(실패 = `text-red`) — D-09 · 자리는 기본값(시안에 없음 · §6.7)
- 토스트: 「A-룸1 3개 시술 · 전체 호출」 · 「… · 최 원장 호출」 · 「방 · 마취 시작/종료」 · 「방 · 이름 · 귀가 대기」 등 시안 문구. **되돌리기 없음** — r3 #25 · D-28

### 6.4 오른쪽 패널 (폭 340 · 검색 + 탭 현황 · 호출 · 고객 — P17)

- 검색 — 이름 · 읽기로 카드 고객 찾기(시안 `hitVals`) · 결과 누르면 그 카드 강조
- **현황** 탭 — 상태 수 6칸 한 줄(전체 · 확인 · 대기 · 마취 · 호출 · 진행) = 카드 필터(고른 칸 파랑 2px). 겹쳐 센다 · 「전체」는 귀가 대기 포함 — D-20 · P12 · r3 §4-2
  - 칸 정의: 확인 = §5.8 대상 · 대기 = `waiting` · 마취 = 진행 중 마취 있음(귀가 대기 제외) · 호출 = 받을 시술이 남은 호출 있음(귀가 대기 제외) · 진행 = `doing` — 시안 `filterFn`
  - 아래 「확인이 필요한 고객」 목록(§5.8) · 빈 문구 「확인이 필요한 고객 없음」 — P13
- **호출** 탭(의국 화면 · `panel-doctors`) — 「수락 대기 N건」 + 호출 카드(호출 오래된 순): 「전체 호출 / 지정 호출」 Badge · 방 · 「호출 N분」(5분 이상 빨강 · 카드 빨간 테두리) · 「기준 5분 / 기준 도달 / +N분 초과」 · 이름 · 국적 · 받을 시술 목록
  - 전체 호출 → 「담당의 선택」 원장 목록(비어 있는 원장 먼저 · 「<방> 시술 중」/「비어있음」) → [<원장> 수락]
  - 지정 호출 → 「지정 <원장> · 상태」 + [다른 원장에게] · [수락]
  - 아래 「최근 수락」 3건 — **[되돌리기] 없음** — D-27 · D-28 · r3 #19
  - 호출 카드 = 고객 1명이 아니라 **호출 1건**(받을 시술이 남은 호출) — D-25 · D-27(시안은 고객 단위로 묶어 보임 → §6.7)
- **고객** 탭(`panel-customers`) — 고객 줄(상태 Badge · 이름 · 방 / 번호 원 시술 줄) · 귀가 대기까지 · 누르면 그 카드만 남기고 흐림 — 시안 r3 §3 「그대로」
- 탭을 옮기면 필터 · 고른 카드 모두 풀림 — r3 #20

### 6.5 의사 호출 팝오버 (`call-modal` · `call-modal-specific`)

- 카드 아래 [의사 호출] 기준 아래로(모자라면 위로) · 560 × 440 · 바깥 누르면 닫힘 · [취소] 없음 — r3 #21 · r4 3-1
- 왼쪽 검색 + 추천: 「모든 의사」(ALL · 「콜 잡은 원장이 집도」) + 원장 목록(§4.6 · 비어 있는 원장 먼저 · 「대기」/「시술 중」) · **하나만 고름 · 다시 누르면 해제** — P7 · P8
- 오른쪽 「선택됨」 + 「호출할 시술 · N개」 목록(바꿀 수 없음 — 카드에서 고른 것) — r3 #22
- 버튼 하나: 「의사를 선택하세요」(꺼짐) / 「<원장> 호출」 / 「모든 의사 호출」 — r3 #24
- 보낸 뒤 카드 체크 비움 — r3 #25

### 6.6 화면 갱신

- **SSE** 로 실시간 갱신 — 현황판 · 호출 탭(의국 화면) 모두 같은 흐름 하나(§7.5). 폴링하지 않는다 — 코디 지시(사용자 2026-10-21)
- 경과 시간은 front 가 1초마다 다시 그린다(`useNow`) · 기준 시각은 스냅샷 `now`(서버 시각)와 front 시계 차이를 보정 — 기본값
- 기준 분(호출 5분 · 마취 20분)은 **스냅샷 `limits` 값만** 쓴다 — front 에 상수를 두지 않는다. 「확인이 필요」 진입 · 빨강 같은 시간 경과로 바뀌는 값은 back 이 **10초마다 발행**하는 스냅샷으로 맞춘다(§7.5) (0.2.0) — S5

### 6.8 좁은 화면 (0.2.0 — S8)

- 폭 **760px 미만 = 가운데 카드만** 보인다(오른쪽 패널 · 호출 탭 없음). 의국 화면(호출 탭)은 **넓은 화면 전제** — 처분 S8 · D-27(의국 PC)
- 760px 이상은 §6.2 ~ §6.5 그대로. 폰 · 태블릿 전용 화면은 범위 밖 — D-34

### 6.7 시안과 다르게 가는 곳

| # | 시안 | 이 계약 | 근거 |
|---|---|---|---|
| 1 | [마취 시작/종료]는 시술 대기 카드에만(`anesCtl`) | 대기 · 진행 어느 때나 | D-23 |
| 2 | 수락 = 그 고객의 수락 전 호출 시술 **전부** | 그 **호출이 유효 호출인 시술 중 미수락만** · 호출 탭 카드 = 호출 1건 | D-27 · D-25 |
| 3 | 「최근 수락」 · 토스트 [되돌리기] | 없음 | D-28 |
| 4 | 시술 줄 「호출함」 Badge 를 누르면 데모 수락 | 누르지 못함(수락은 호출 탭에서만) | D-27 |
| 5 | 헤더 메뉴 세 칸 | 「시술 현황」 하나 | D-17 |
| 6 | 카드 위 주석 「시술 [시작] · [종료]는 태블릿 · 폰 몫(여기 없음)」 | 현황판 카드에 [시작] · [종료] 있음(시안 그림이 맞고 주석이 낡음) | D-29 · P3 |
| 7 | 「수납 필요」 표시 없음(시안 데이터에 결제 없음) | 고객 줄 끝에 작은 칩 「수납 필요」(Badge `warning` sm) — 자리 · 모양은 기본값 | D-21 · OQ-508 |
| 8 | 「KOS 반영 중 · 실패」 표시 없음 | §6.3 의 작은 글자 — 자리는 기본값 | D-09 · OQ-508 |
| 9 | 원장 · 고객 · 방 = 가짜 4명 · seed 6명 | KOS 데모 지점 실데이터 | D-06 · D-11 |
| 10 | 같은 칸을 다시 눌러도 필터가 안 풀림(주석은 「다시 누르면 해제」) | 시안 동작대로 — 「전체」 또는 탭 이동으로 풀림 | 시안 r3 #14 |

## 7. back ↔ front API

공통: 요청 · 응답 JSON · 오류 `{error:{code, message}}` · 로그인 뒤 모든 요청 `Authorization: Bearer <ccc 토큰>`(없거나 틀리면 401 `unauthorized`). 조작 응답은 ccc 상태가 바뀐 뒤 바로 온다(KOS 를 기다리지 않음 — §4.4).

### 7.1 로그인

| 메서드 · 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| `POST /api/auth/login` | `{id, password}`(둘 다 필수) | `{token, expiresAt, id, role, name, staffId}` (0.3.0) | 401 `invalid_credentials` · 429 `too_many_attempts` (0.3.0) |
| `GET /api/auth/me` | — | `{id, role, name, staffId}` (0.3.0) | 401 |

- 정본은 **SPEC-004 §3.3**(비밀번호 bcrypt · 5회 실패 1분 잠금 · 계정 목록 API 없음). 이 절은 웹이 쓰는 모양만 (0.3.0)
- 토큰 = back 이 `PROC_SESSION_SECRET` 로 서명한 값 · 만료 `PROC_SESSION_HOURS`(기본 12시간). front 는 localStorage 에 토큰 · `role` · `name` 을 두고 401 이면 `/login` — D-05 · 기본값 · SPEC-004 §3.6
- ~~직원 개인 계정은 없다~~ → 계정 = 관리자 · 의사 · 간호사(SPEC-004 §3.1) (0.3.0) — SPEC-004 A-03

### 7.2 조회 — 스냅샷 모양

`GET /api/board` → (SSE `board` 이벤트 본문도 이 모양 + `version` — §7.5)

```text
{
  now,                                   // 서버 시각(ISO, KST 오프셋)
  limits: { callMin: 5, anesMin: 20 },   // §5.8 기준 분 — front 는 이 값만 쓴다 (0.2.0 · S5)
  sync: { lastOkAt, lastError, inWindow },
  doctors: [{ id, name, busy, busyRoom }],                  // §4.6
  counts:  { all, need, waiting, anes, call, doing },       // §6.4
  cards: [{
    visitId, room: { id, title, order }, inAt, homeAt,
    customer: { name, phoneticName, nationality, isNew, chartNumber },
    state: "waiting"|"doing"|"home", paymentRequired, orderMemo,
    anesthesia: { runningSince, lastMinutes, long, canStart, canEnd },   // long = 진행 중 마취가 anesMin 이상 (0.2.0)
    procedures: [{ id, kind: "procedure"|"etc", sequence, title, state: "wait"|"doing"|"done",   // kind (0.3.0 · E2E-4)
                   kosStatus,                    // KOS 작업 status 원문(NOT_STARTED · WAITING · READY · DONE · CANCELED) — 반영 대기 중이면 ccc 가 바꾼 값 (0.3.0)
                   startedAt, completedAt, doctor: { id, name }|null,
                   call: { id, kind: "all"|"one", targetDoctorId, createdAt, acceptedBy, acceptedAt }|null,
                   pickable, canStart, canFinish }],
    canCall, canHome,
    need: { why: "home"|"anes"|"call", since, limitMin }|null,
    kos: { status: "ok"|"pending"|"failed", failed: [{ op, error }] }
  }],
  calls: [{ callId, visitId, room, customer: { name, nationality }, kind, targetDoctorId,   // 호출 기준은 limits.callMin 하나로 쓴다 — 호출마다 따로 싣지 않는다 (0.2.0)
            createdAt, procedures: [{ id, title }] }],                         // §5.5 받을 시술 남은 호출만
  recentAccepts: [{ at, room, doctorName, count }]                            // 최근 3건
}
```

- 규칙(§5) 계산은 back 이 한다 — `pickable` · `canStart` · `canFinish` · `canCall` · `canHome` · `need` 를 front 가 다시 계산하지 않는다 — 기본값(규칙 한 곳)
- `kind = etc` 작업은 `state` = KOS `DONE` 이면 `done` · 아니면 `wait`(ccc [시작]이 없으므로) · `pickable` · `canStart` · `canFinish` 는 늘 `false` · 화면 글자는 `kosStatus` — 코드 `domain/rules.py` `proc_state` · `schemas/board.py` (0.3.0)
- 필드 순서는 코드 `schemas/board.py` 의 `BoardSnapshot`(`now` · `sync` · `doctors` · `counts` · `limits` · `cards` · `calls` · `recentAccepts`) — 이름 · null 여부는 코드가 정본 (0.3.0)
- `chartNumber` 는 검색에만 쓰고 화면에 크게 보이지 않는다 — D-14

### 7.3 조작

| 메서드 · 경로 | 요청 | 성공 | 409 코드(도메인 예외) | 근거 |
|---|---|---|---|---|
| `POST /api/visits/{visitId}/anesthesia/start` | — | `{ok:true}` | `visit_home` · `anesthesia_running` | D-23 |
| `POST /api/visits/{visitId}/anesthesia/end` | — | `{ok:true}` | `anesthesia_not_running` | D-23 |
| `POST /api/visits/{visitId}/calls` | `{procedureIds:[…], target:{kind:"all"} \| {kind:"one", doctorId}}` | `{callId}` | `visit_home` · `procedure_not_waiting` · `no_procedures` · `doctor_not_listed` | D-24 ~ D-26 |
| `POST /api/calls/{callId}/accept` | `{doctorId?}` — 관리자 = 필수(없으면 400) · 의사 = 생략하면 자기 원장(SPEC-004 §3.4). 선택 헤더 `X-Accept-Source: push\|app\|web`(없으면 Origin 있음 = `web` · 그 밖 `app`) → `call_accept` payload `source` (0.3.0) | `{acceptedProcedureIds}` | `nothing_to_accept` · `doctor_not_listed` · `doctor_mismatch` | D-27 · SPEC-004 A-07 · A-18 · 코드 `api/actions.py` |
| `POST /api/calls/{callId}/reassign-all` | — | `{callId}`(새 전체 호출) | `not_designated_call` · `nothing_to_accept` | D-27 |
| `POST /api/procedures/{procedureId}/start` | — | `{ok:true, flowStepChanged}` | `visit_home` · `procedure_not_waiting` · `call_not_accepted` · `no_doctor` | D-30 · D-32 |
| `POST /api/procedures/{procedureId}/finish` | — | `{ok:true}` | `procedure_not_started` | D-31 · D-32 |
| `POST /api/visits/{visitId}/home` | — | `{ok:true}` | `procedures_not_done` · `visit_home` | D-33 |

- 없는 id = 404 `not_found` · 형식 오류 = 400 `invalid_request`(cc 와 같은 형식). `etc` 작업 id 로 [시작] · [종료] = 404 (0.3.0 — 코드 `service/actions.py` `_procedure`)
- `PROC_FAKE_BOARD` 가 켜져 있으면 조작 API 전부 403 `fake_board`(§2.3) (0.2.0) — S7
- 역할 403(`role_forbidden` · `doctor_forbidden` · `not_your_call`)과 검사 순서는 SPEC-004 §3.4 (0.3.0)
- 조작마다 `event_log` 1줄(`actor` = 로그인 아이디) — D-13

### 7.4 기타

- `GET /api/health` → `{ok, kos: { open, internal }}`(토큰 보유 여부만 · 값 없음)
- 데모 · 시드 · 리셋 API 없음 — D-01(시드 없음). 데모 고객 준비는 레포 밖 운영 도구(WORK-003 「운영 도구」)가 KOS 에 직접 한다 (0.3.0)
- 그 밖 back API — `WS /api/interpret`(SPEC-004 §4) · `POST /api/devices` · `DELETE /api/devices/{token}`(SPEC-004 §5-1.1) (0.3.0)
- **back 경로 전부(코드 기준 16개 — router 15 + `GET /api/health`)** = §7.1 2 · §7.2 `GET /api/board` · §7.5 `GET /api/board/stream` · §7.3 조작 8 · `GET /api/health` · 통역 WS 1 · 기기 2. `GET /api/auth/accounts` 는 **없다**(0.3.0 에서 제거 — SPEC-004 §3.3) (0.3.0)

### 7.5 실시간 갱신 — SSE (코디 지시 · 사용자 2026-10-21)

| 항목 | 계약 | 이유 |
|---|---|---|
| 경로 | `GET /api/board/stream` · `Content-Type: text/event-stream` | — |
| 인증 | `?token=<ccc 토큰>`(브라우저 `EventSource` 는 헤더를 못 싣는다). 틀리면 401 후 닫음 → front 는 `/login`. **접근 로그에 쿼리 문자열을 남기지 않는다** — uvicorn 접근 로그에서 쿼리를 지우는 필터(또는 `/api/board/stream` 접근 로그 끔). 배포 때 ingress 로그도 같은 기준 (0.2.0) | `EventSource` 제약 · S9 |
| 이벤트 종류 | **`board` 하나** | 화면이 하나 · 상태도 하나 |
| 본문 | **전체 스냅샷** — `GET /api/board`(§7.2)와 **같은 모양 그대로**(+ `version`: 보낼 때마다 1 씩 느는 정수) | 단순한 쪽: ① 한 지점 · 한 구역 · 오늘 일정이라 크기가 작다(HAR 하루 15건 ≈ 32KB, 저장 필드는 그보다 적다) ② front 는 받으면 **통째로 바꾸기만** — 바뀐 것만 보내면 합치기 · 순서 · 빠진 이벤트 복구 로직이 front 에 생긴다 ③ 규칙 계산(`canStart` 등)이 back 한 곳에 남는다(§7.2) |
| 보내는 때 | ① ccc 조작(마취 · 호출 · 다른 원장에게 · 수락 · 시작 · 종료 · 귀가 대기)이 DB 에 들어간 직후 ② KOS 일정 조회(10초)가 끝날 때마다 — 값이 바뀌었거나 `sync`(마지막 동기화 시각 · 오류)가 바뀌었으면 ③ 직원 · 방 조회(1시간) 뒤 ④ `kos_op` 상태가 바뀔 때(반영 중 → 확인 · 실패) ⑤ **조회 시간과 상관없이 10초마다**(시간 경과로 바뀌는 「확인이 필요」 · 마취 `long` · 날짜 바뀜 반영) (0.2.0) | 화면의 값은 이 다섯 중 하나로만 바뀐다 · S5 |
| 첫 접속 | 연결되면 **바로 `board` 1개**(지금 전체). front 는 이것으로 첫 화면을 그린다 — 따로 `GET /api/board` 를 부를 필요 없음(§7.2 는 시험 · 디버그용으로 남긴다) | 첫 로딩과 갱신이 같은 길 |
| 재연결 | 끊기면 `EventSource` 기본 재연결(back 이 `retry: 3000` 을 보낸다). 다시 붙으면 첫 접속처럼 전체 스냅샷을 받는다 — **`Last-Event-ID` 다시 보내기 없음** | 스냅샷이라 놓친 이벤트를 메울 필요가 없다 |
| 연결 유지 | 15초마다 주석 줄 `: ping` | 프록시 · 브라우저 유휴 끊김 방지(기본값) |
| 여러 화면 | 연결마다 같은 스냅샷을 보낸다(간호 스테이션 · 의국 PC 동시) | D-27 의국 화면 |
| 조작 응답과의 관계 | 조작 API(§7.3)는 `{ok…}` 만 돌려준다. 화면은 뒤따르는 `board` 이벤트로 바뀐다 | 갱신 길 하나 |
| 순서 | front 는 지금 가진 `version` 보다 작거나 같은 스냅샷은 버린다 | 재연결 겹침 대비 |

- back 은 연결 목록을 메모리에 둔다(프로세스 1개 · PoC) — D-15 · 기본값
- 이벤트 형식 예: `event: board` / `id: <version>` / `data: <스냅샷 JSON 한 줄>`

## 8. KOS 반영 표

내부 = `{KOS_INTERNAL_API_BASE}/tenants/{tenantId}/…` · `Authorization: Bearer` / 공개 = `{KOS_OPEN_API_BASE}/…` · `Authorization: <token>`. 경로 · 본문은 HAR 에서 본 그대로(내부는 공식 계약이 아니다 — OQ-503).

| ccc 조작 | 순서 | 종류 · 경로 | 본문 | 확인(다음 조회에서) | 근거 |
|---|---|---|---|---|---|
| [마취 시작] · [마취 종료] | — | 없음 | — | — | D-23 |
| [의사 호출](전체 · 지정) · [다른 원장에게] | 1 | 내부 `schedule/flow/v1/commands/change-tasks-room` | `{scheduleId, sequences:[고른 시술], roomId:<카드 방 KOS id>}` — 고른 작업이 이미 다 그 방이면 보내지 않고 `confirmed` | 그 작업들 `room.id` = 카드 방 | E2E-1 · HAR(`시술현황_방배정.har`) (0.3.0) |
| 〃 | 2 | 내부 `schedule/flow/v1/commands/change-tasks-assignees` | `{scheduleId, sequences:[고른 시술], assigneeIds:[시스템 계정 id]}` | 그 작업들 `assignees` 에 시스템 계정 | D-24 · HAR(`의사호출*.har`) |
| 〃 | 3 | 내부 `schedule/flow/v1/commands/call-tasks-doctors` | `{scheduleId, sequences:[고른 시술]}` | 그 작업들 `status = WAITING` | D-24 · HAR(호출 뒤 WAITING) · OQ-501 |
| [수락](호출 탭 · 앱 · 알림 [수락]) (0.3.0) | 1 | 내부 `schedule/flow/v1/commands/change-tasks-doctors` | `{scheduleId, sequences:[받는 시술], doctorIds:[고른 원장 id]}` | 그 작업들 `doctors` 에 그 원장 · `status = READY` | D-27 · HAR(관리자 계정 대신 수락 200) |
| 첫 [시작] | 1 | 공개 `schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"PROCEDURE"}` | 일정 `flowStep = PROCEDURE` | D-32 · API §2 A |
| [시작](첫 아님) | — | 없음(ccc 만) | — | — | D-32 |
| [종료] | 1 | 내부 `schedule/flow/v1/commands/change-tasks-complete` | `{scheduleId, sequences:[그 시술 하나], complete:true}` | 그 작업 `status = DONE` | D-32 · HAR(`시술완료.har`) |
| [귀가 대기] | 1 | 내부 `schedule/v1/commands/cancel-flow-tasks` — 남은 비시술 작업이 없으면 만들지 않음 | `{scheduleId, sequences:[끝나지 않은 작업 중 시술 작업을 뺀 것], reason:"CANCEL"}` | 그 작업들 `status = CANCELED` | E2E-3 · 1차 HAR (0.3.0) |
| 〃 | 2 | 공개 `schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"PROCEDURE_DONE"}` | 일정 `flowStep = PROCEDURE_DONE` | D-33 · HAR(`시술완료_상태.har`) |

- `scheduleId` = `visit.kos_id` · `sequences` = `procedure.kos_sequence`
- `change-flow-step` 거절(스펙): `ProceduresNotFound` 등 400 → §4.4 재전송 · 실패 규칙 — API §5
- **같은 단계 규칙** (0.2.0 — S2 · 워커 실호출): KOS 는 **지금 단계와 같은 단계로의 `change-flow-step` 을 400 으로 거절**한다. 그래서
  - op 을 만들 때 · 보내기 직전에 마지막 조회의 KOS `flowStep` 이 이미 목표 단계면 **보내지 않고 `confirmed`** 로 둔다(조회 10초 사이에 KOS 가 먼저 바뀐 경우 — ccc 는 아직 `waiting` 이라도)
  - 보냈는데 400 이 오면 바로 실패로 세지 않고, 다음 조회에서 `flowStep` 이 목표 단계면 `confirmed`(재전송 없음). 아니면 §4.4 재전송 · 실패 규칙
- `call-tasks-doctors` 가 400 을 주는 조건 — 귀가 대기 일정은 400(처분 W10) · **시술 작업에 방이 없으면 400 `errorProperties roomId NotFound`** → 1번 `change-tasks-room` 으로 막는다(E2E-1) (0.3.0). 이미 `WAITING` / `READY` 작업 재호출 · [다른 원장에게]는 미확인 → OQ-516 (0.2.0)
- KOS 작업 칸 「진행중」은 **수락(집도의 지정) 직후** 뜬다(KOS 에 작업별 시작 칸이 없다) — **그대로 둔다**. 시술 진행 · 대기의 기준은 ccc 이고 현장은 KOS 를 보지 않는다. [시작] 때 집도의를 지정하는 방식으로 바꾸지 않는다 (0.3.0) — E2E-2 · `_RESUME` 10-21 「KOS 작업 「진행중」은 수락 시점 그대로」 줄
- 「KOS 화면은 마지막 완료 때 방을 비워 보인다」 — ccc 는 그 표시를 따르지 않는다(§5.7) — D-33 · HAR

## 9. 검증 기준 — 로컬 E2E (데모 지점)

준비: `procedure/back/.env` 를 채운다(값 원천 = ax-clinic-project · 사용자) → `docker compose up --build` → `http://localhost:3700` 로그인. KOS 확인은 **데모 KOS 웹 화면** 또는 공개 `getScheduleDetail`(조회만) — 현장 조작 금지(D-10)는 E2E 의 KOS 쪽 **준비**(일정 만들기 · 시술 대기 · 방 배정)에는 해당하지 않는다.

| # | 단계 | ccc 에서 보는 것 | KOS 쪽 확인 | 근거 |
|---|---|---|---|---|
| 0 | 데모 KOS 에서 4층 오늘 일정 1건을 시술 대기 · 방 배정(작업 2개 이상) | — | 일정 `PROCEDURE_WAITING` · ETCETERA 작업 `room` | D-21 · D-22 |
| 1 | 카드 등장 | 10초 안에 카드 · 「시술 대기」 · 입실 시각 · 오더 메모 · (결제 전이면) 「수납 필요」. 방 없는 일정은 안 나온다 | — | D-08 · D-21 · D-22 |
| 2 | [마취 시작] → 21분 대기 또는 시각 조작 없이 표시만 확인 → [마취 종료] | 「마취 · NN분 경과」 보라 → 20분 이상 빨강 · 「확인」 칸 +1 → 「완료 N분」 | KOS 변화 없음 | D-20 · D-23 |
| 3 | 시술 2개 체크 → [의사 호출 · 2건] → 「모든 의사」 | 「호출함」 · 「전체 호출 · 수락 전」 · [시작] 꺼짐 · 호출 탭 1건 · 5분 뒤 「확인이 필요」 | 두 작업 `room` = 카드 방 · `assignees` = 시스템 계정 · `status = WAITING` — **몇 초 안에**(20 ~ 30초 걸리지 않음) (0.3.0) | D-24 · D-25 · D-30 · E2E-1 · E2E-6 |
| 4 | 호출 탭에서 원장 A 골라 [수락] | 두 시술 「A 수락 · 시작 가능」 · 호출 탭 0건 · 「최근 수락」 1줄 | 두 작업 `doctors` = A · `status = READY` | D-27 |
| 5 | 시술 1 을 다시 체크 → 원장 B 지정 호출 → 호출 탭 [다른 원장에게] → 원장 C [수락] | 시술 1: 지정 호출 → 전체 호출(새 줄) → C 수락. 시술 2 는 A 그대로 | 시술 1 `doctors` = C | D-25 · D-27 · OQ-501 |
| 6 | 시술 1 [시작] | 고객 「시술 진행」 · 시술 1 「C · HH:MM 시작」 · [종료] | 일정 `flowStep = PROCEDURE` | D-30 · D-32 |
| 7 | [마취 시작] (진행 중) | 켜진다 | 변화 없음 | D-23 |
| 8 | 시술 1 [종료] · 시술 2 [시작] → [종료] | 완료 줄이 위로 · 카드 아래가 [귀가 대기] 로 바뀜 | 각 작업 `status = DONE`. KOS 화면은 방을 비워 보일 수 있다 — ccc 카드 · 방은 그대로 | D-31 · D-32 · D-33 |
| 9 | [귀가 대기] | 카드 흐림 · 맨 뒤 · 「귀가 대기 HH:MM」 — 데모 KOS 에서 귀가(`COMPLETED`) 처리하면 10초 안에 카드가 사라진다 (0.3.0) | 「방 배정」 등 남은 작업 `CANCELED` · 일정 `flowStep = PROCEDURE_DONE` · KOS 방이 빈다 (0.3.0) | D-33 · E2E-3 · E2E-9 |
| 10 | 반영 실패 확인(선택) — back 의 내부 API 주소를 틀리게 두고 [종료] | 「KOS 반영 중」 → 3회 뒤 「KOS 반영 실패」 · ccc 상태는 완료 | 변화 없음 | D-09 |
| 11 | 조회 시간 · 덮어쓰기 | 데모 KOS 에서 오더 메모를 고치면 10초 안에 카드에 반영 | — | D-08 · D-09 |

back 단위 시험(pytest, KOS 는 가짜 클라이언트): §5.10 전이 · §5.11 활성 조건 · 유효 호출(D-25) · 수락 범위(D-27) · 덮어쓰기 보호(§4.3) · op 순서 · 재전송 · 실패(§4.4) · 원장 목록 제외(D-11) · 조회 시간(D-08) · SSE(§7.5 — 첫 접속 스냅샷 · 조작 뒤 1개 · 토큰 없으면 401).

E2E 공통: 브라우저 두 개(현황판 · 의국 PC 역할)를 열어 두고, 한쪽 조작이 다른 쪽에 새로고침 없이 바로 보이는지 매 단계 본다(§7.5). back 을 재시작하면 화면이 다시 붙고 같은 상태가 보인다.

## 10. 열린 것

| ID | 질문 | 지금(기본값) | 상태 |
|---|---|---|---|
| OQ-501 | 「원장 한 명」 호출이 KOS 요청에 어떻게 실리나(`doctorIds`?) | 「모든 의사」와 같은 요청 · 지정 원장은 ccc 만 | 열림(DEC-005) |
| OQ-502 | 수납 뒤 결제 전 작업이 시술권(`ticketId`)을 받는지 · [종료] 때 시술권 차감 | ccc 는 시술권을 다루지 않는다 | 열림(DEC-005) |
| OQ-503 | 내부 API 가 막히거나 바뀌면 | 일정 조회는 공개 `getSchedulesByFlowStep` 으로 대체 가능 · 쓰기는 공개 API 에 없음 | 열림(DEC-005) |
| OQ-504 | 「확인이 필요」에 시안의 세 번째 이유(시술 모두 완료 · 귀가 대기 전, 기준 없음)를 넣나 — D-20 은 호출 · 마취 둘만 적었다 | 시안대로 넣는다(D-16 「정책은 시안대로」) | 새로 |
| ~~OQ-505~~ | 카드가 사라지는 때 — KOS 가 `COMPLETED`(귀가) 등 세 단계 밖이 되면 | **닫힘** — 귀가 대기 카드는 흐리게 남고 KOS `COMPLETED` 가 되면 사라진다(§5.1 조건 2) | 닫힘(E2E-9 · `_RESUME` 10-21) (0.3.0) |
| OQ-506 | KOS `status = CANCELED` 작업을 시술 목록에 두나 | 목록에서 뺀다 · 「전부 완료」 판정에서도 뺀다 — 코드 그대로(`domain/rules.py` `items`) | 기본값 구현 (0.3.0) |
| OQ-508 | 「수납 필요」 · 「KOS 반영 중 · 실패」 자리 · 모양 — 시안에 없음 | §6.7 #7 · #8 | 새로 |
| OQ-509 | 「KOS 반영 실패」 뒤 복구 — 다시 보내기 버튼 · 운영 절차 | 버튼 없음 · back 로그 · `event_log(kos_failed)` 로 확인. 되돌리기 정책 때 같이 | 새로 |
| OQ-510 | 재전송 횟수 · 간격 | 조회 주기마다 · 3회 뒤 실패 | 새로 |
| OQ-511 | 한 일정에 방 있는 ETCETERA 작업이 둘 이상이면 어느 방인가(HAR 에 「방 배정」 외 「방 점유/원장 상담」 작업도 있다) | `roomAssignedDateTimeUtc` 가 가장 늦은 작업의 방 — 코드 그대로(`kos/sync.py`) · 호출 때 시술 작업에 넣는 방도 이것(§5.4) | 기본값 구현 (0.3.0) |
| OQ-512 | KOS 쪽에서 ccc 를 거치지 않은 호출 · 집도의 변경이 조회되면(D-10 은 현장이 안 한다고 정함) | KOS 값을 보여 준다(집도의 · 호출 여부) · ccc 호출 기록은 만들지 않는다 | 새로 |
| OQ-513 | 조회 시간 밖의 조작 | 막지 않는다 · KOS 에 보내고 확인은 다음 조회 시간 | 새로 |
| OQ-514 | 헤더 계정 표시 문구(시안 「데스크」 · 계정은 관리자 1개) | 시안 문구 그대로 | 새로 |
| OQ-515 | 진행 중 마취가 있는 채로 [귀가 대기] | 막지 않는다 · 귀가 대기 카드엔 마취 버튼 없음 | 새로 |
| OQ-516 | `call-tasks-doctors` 가 400 을 주는 조건 — 이미 `WAITING`/`READY` 작업 재호출(D-25 다시 호출) · [다른 원장에게](D-27) | 확인된 것: 귀가 대기 일정 400 · **시술 작업에 방 없음 400 `roomId NotFound`**(E2E-1 → 방 넣기 op 으로 막음 · §8). 재호출 · [다른 원장에게] 400 여부는 실 데모 기록 없음 — 400 이면 §4.4 실패 규칙 (0.3.0) | 일부 닫힘(방) · 나머지 열림 (0.3.0) |
| OQ-517 | 현황판(웹) 카드의 `kind = etc`(「방 배정 · 준비중」) 줄을 빼나 | 사용자 「필요하지 않을 거 같아요 · 일단 기록해놔」 — **빼기로 기록만**(다음 수정 batch). 지금 코드(웹)는 그린다 · back · 스냅샷은 그대로(귀가 대기 취소에 씀) · 앱은 안 그림 | 열림 — 다음 수정 batch(E2E-10) (0.3.0) |
| OQ-518 | 웹 로그인에 역할 제한을 두나 — 결정은 「웹 = 관리자」(SPEC-004 A-03 · §3.6)인데, 정상 로그인 뒤 웹 폼은 **비밀번호가 있는 계정이면 역할과 상관없이** 들어간다(코드 `front/app/login/page.tsx` · back 은 역할로 막지 않음). 조작 권한은 back 이 API 마다 검사(SPEC-004 §3.4) | 코드 그대로(제한 없음) · 결정 필요 | 열림 (0.3.0) |
| OQ-519 | KOS 데모 지점의 데모 표식 계정(`KOS-DEMO` 이름 · 데모 도구가 데모 테넌트 확인에 씀)이 원장 목록에 섞이면 뺄까 — 지금 제외는 시스템 계정 id + `KOS_EXCLUDE_ACCOUNT_IDS` 뿐(§4.6) | 코드 그대로 — 빼려면 `KOS_EXCLUDE_ACCOUNT_IDS` 에 그 계정 id(env · 코드 변경 없음) | 열림 (0.3.0) |

## 부록 A. DEC-005 대응표

| D | 내용(줄임) | SPEC-003 |
|---|---|---|
| D-01 | 새 폴더 `procedure/` · `cc/` 코드 안 씀 | §1.1 · §2.1 · §7.4 |
| D-02 | 테마 · DS 복사 · import 금지 | §1.1 · §2.1 · §2.4 · §6.1 |
| D-03 | 배포 = 기존 주소 교체 · `_archive/cc` | §1.1(로컬 뒤) · WORK-003 마지막 WP |
| D-04 | 범위 = 구현 · 배포까지 | §1.1 · WORK-003 |
| D-05 | 관리자 계정 1개 → 계정 3종 · 정상 로그인(SPEC-004) (0.3.0) | §1.1 · §2.3 · §6.1 · §7.1 · OQ-518 |
| D-06 | KOS 데모 지점 실연동 · 운영 키 금지 | §1.1 · §1.2 · §2.3 · §6.7 #9 |
| D-07 | 공개 · 내부 인증 · 토큰 보관 | §2.3 · §4.1 |
| D-08 | 4층 · 10초 · 1시간 · 09~21 | §2.3 · §4.2 · §5.1 |
| D-09 | KOS 기준 / ccc 기준 · 반영 중 · 실패 | §3.2 · §4.3 · §4.4 · §5.2 · §6.3 |
| D-10 | 현장은 KOS 직접 조작 안 함 | §1.2 · §9 · OQ-512 |
| D-11 | 원장 목록 · 시스템 · 마취용 · 비활성 제외 | §2.3 · §4.1 · §4.6 |
| D-12 | ccc DB 가 KOS 를 품음 · `kos_id` · 대응표 | §3.1 · §3.2 · §3.3 |
| D-13 | 이벤트 로그 | §3.1 · §3.2 · §7.3 |
| D-14 | 개인정보 = 화면에 쓰는 것만 | §1.2 · §3.1 · §3.3 · §7.2 |
| D-15 | SQLite · 나중 PG + Redis | §2.2 · §3.1 |
| D-16 | 시안 정본 | 머리말 · §6 |
| D-17 | 구조 · 헤더 메뉴 하나 | §6.2 · §6.3 · §6.7 #5 |
| D-18 | 입실순 · 배치순 | §3.3 · §6.3 |
| D-19 | 카드 구성 | §6.3 |
| D-20 | 현황 · 필터 · 확인이 필요 | §5.8 · §6.4 · OQ-504 |
| D-21 | PROCEDURE_WAITING 이면 카드 · 수납 필요 | §5.1 · §6.7 #7 |
| D-22 | 방 있는 고객만 · ~~ETCETERA 안 보임~~ → 읽기 전용으로 보임(E2E-4) (0.3.0) | §3.3 · §5.1 · §6.3 · OQ-517 |
| D-23 | 마취 별개 · 시안 고침 | §5.3 · §5.11 · §6.7 #1 · §8 |
| D-24 | 의사 호출 · KOS 2단계 → 방 넣기 포함 3단계(E2E-1) (0.3.0) | §5.4 · §8 |
| D-25 | 호출 쌓기 · 유효 호출 | §3.2 · §5.4 · §5.5 |
| D-26 | 진행 · 완료 시술은 호출 대상 아님 | §5.4 · §5.11 |
| D-27 | 의국 화면 수락 · 받는 범위 · 다른 원장에게 | §5.5 · §6.4 · §6.7 #2 · #4 · §8 |
| D-28 | 되돌리기 없음 | §1.2 · §5.5 · §6.3 · §6.4 · §6.7 #3 |
| D-29 | 지금은 현황판에서 [시작] · [종료] | §5.6 · §6.7 #6 |
| D-30 | [시작] 조건 | §5.6 · §5.9 · §5.11 |
| D-31 | [종료] = 시작한 시술만 | §5.6 · §5.11 |
| D-32 | 첫 [시작] = PROCEDURE · [종료] = complete | §5.2 · §5.6 · §8 |
| D-33 | [귀가 대기] = 방 빼기 · (남은 작업 취소 →) PROCEDURE_DONE (0.3.0) | §5.1 · §5.2 · §5.7 · §8 |
| D-34 | 이번 범위 밖 | §1.2 |

누락 0.

## 부록 B. 리뷰 r1 S1 ~ S12 반영표 (0.2.0)

| S | 처분(`fix-decisions-r1.md`) | SPEC-003 |
|---|---|---|
| S1 | 시스템 계정 id = `get-user-account` `data.id` | §2.3 · §4.1 |
| S2 | 같은 단계 flow-step 400 · KOS 가 먼저 바뀐 경우 | §5.10 · §8 |
| S3 | `failed` 뒤 KOS 값 · 실패 표시는 다음 확인까지 | §3.2 · §4.3 · §4.4 |
| S4 | 실패 뒤 같은 visit 의 뒤 op 멈춤(`failed` · 사유 「앞 op 실패로 보내지 않음」 · `payload.blockedOpIds` — r2) | §3.2 · §4.4 |
| S5 | `limits.callMin` · `limits.anesMin` · 마취 `long` · 10초 발행(호출 기준은 `limits.callMin` 하나) | §6.6 · §7.2 · §7.5 |
| S6 | 루트 `.env` 하나 · `build.args` · `front/.env.local` | §2.1 · §2.2 · §2.3 |
| S7 | `PROC_FAKE_BOARD` 개발 전용 · 조작 403 | §2.3 · §7.3 |
| S8 | 760px 미만 = 카드만 | §6.8 |
| S9 | SSE 토큰 쿼리를 접근 로그에 안 남김 | §7.5 |
| S10 | KST 00:00 에 전날 카드 내림 | §4.2 · §5.1 |
| S11 | call 400 조건 → OQ | §8 · OQ-516 |
| S12 | 시스템 계정 id 모르면 원장 목록 이전 값 유지 | §4.6 |

처분의 W6(예외 삼키지 않음) · W8(시작 조회) · W9(room 비면 카드 사라짐) · W12(앱 팩토리) · W14 ①(빌드 인자 기본값)도 SPEC 에 닿는 곳만 같이 적었다(§2.2 · §4.2 · §4.3).

## 부록 C. 사용자 E2E batch 1 반영표 (0.3.0)

원천 `orchestration/work/myeongdong-poc-v2/e2e-feedback-batch-1.md`(2026-10-21 · 웹 · 데모 지점). 번호 11 은 그 문서에 없다.

| E2E | 처분(그 문서 「고칠 방향」) | 코드(main `329b543`) | SPEC-003 |
|---|---|---|---|
| 1 | 호출 전 「방 배정」 방을 고른 시술 작업에 덮어쓰기 → 담당자 → 호출 | `domain/kos_ops.py` `room_op` · `service/actions.py` `_new_call` | §3.2 · §3.3 · §5.4 · §8 · §9 #3 · OQ-516 |
| 2 | KOS 「진행중」 = 수락 그대로(수정 없음) | 변경 없음 | §8 |
| 3 | [귀가 대기] = ① 남은 비시술 작업 취소 → ② PROCEDURE_DONE | `cancel_tasks_op` · `home` | §3.2 · §3.3 · §5.7 · §8 · §9 #9 |
| 4 | ETCETERA 도 카드에 읽기 전용 한 줄 · `procedures[].kind` | `kos/sync.py` · `rules.py` `items` · `schemas/board.py` | §3.2 · §3.3 · §5.1 · §6.3 · §7.2 · §7.3 |
| 5 | 카드 높이 고정(→ 12 가 고침) | — | §6.3 |
| 6 | op 2xx 면 바로 다음 · 묶음 뒤 1 ~ 2초 조회 1회 | `kos/ops.py` · `kos/runtime.py` `QUICK_SYNC_SEC = 1.5` | §4.4 · §9 #3 |
| 7 | (사용자 취소) | — | — |
| 8 | 귀가 대기 카드 없애기(→ 9 가 되돌림) | — | §5.1 |
| 9 | 귀가 대기 카드는 흐리게 남고 KOS `COMPLETED` 때 사라짐 · E2E-3 유지 | `rules.py` `BOARD_FLOW_STEPS` | §5.1 · §5.7 · §9 #9 · OQ-505 닫힘 |
| 10 | 현황판에서 `etc` 줄 안 그리기 — **기록만** | 웹은 아직 그림 | §5.1 · §6.3 · OQ-517 |
| 12 | 카드 안 스크롤 없음 · 최소 높이 = 판 절반(비율) · px 금지 · 버튼 바닥 | `front/app/(main)/procedures/live/page.tsx` `gridAutoRows` | §6.3 |

앱 실기기 피드백 중 back 에 닿는 것: T6(`canCall` = pickable 시술 ≥ 1) → §5.11. 나머지 T1 ~ T8 · A1 ~ A7 은 SPEC-004.

누락 0.

## 부록 D. 출처 줄 → SPEC · WORK 절 대응표 (0.3.0 · slug 마감 전 전수)

`S3` = 이 문서(SPEC-003) · `S4` = SPEC-004 · `W3` · `W4` = WORK-003 · WORK-004. 「뒤집힘」 = 그 줄의 결정이 뒤 줄로 바뀌어 SPEC 은 뒤 줄을 따른다.

### D.1 `_RESUME.md` §2 결정 표 — 100줄(파일 30 ~ 129행 · 2026-10-22 기준)

| 행 | 날짜 | 줄(줄임) | SPEC · WORK |
|---|---|---|---|
| 30 | 10-20 | v2 = cc-prototype 다음 차수 · 시술 현황판 | S3 머리말 · §1.1 |
| 31 | 10-20 | workflow v1 / v2 나눔 | workflow-v2 머리말(SPEC 밖 — 업무 흐름 원천) |
| 32 | 10-20 | KOS 데모 지점 실연동 · 운영 명동점 키 금지 | S3 §1.1 · §1.2 · §2.3(D-06) |
| 33 | 10-20 | KOS 키 값 · 사용법 참고처 = ax-clinic-project(옮기지 않음) | S3 §2.3(값 원천) · §9 준비 |
| 34 | 10-20 | 데모 접속 · API = `kos-demo-api.md` | S3 머리말 근거 표기 `API` |
| 35 | 10-20 | `cc-prototype.json` `repos.reference` | SPEC 밖(오케스트레이션 설정) — 해당 없음 |
| 36 | 10-20 | 시작 상태 = 수납 끝난 일정(시술 대기) | S3 §5.1 · §5.2 · workflow-v2 §1 |
| 37 | 10-20 | 현황판 = 방 · 고객 · 시술 · 메모 | S3 §6.3 |
| 38 | 10-20 | 마취 타이머 · 고객 단위 · 여러 회차 · 동시 1 · ccc DB | S3 §3.2 `anesthesia` · §5.3(D-23) |
| 39 | 10-20 | `마취용` 계정 표시 제외 | S3 §4.6(D-11) |
| 40 | 10-20 | 시술 준비(약물 · 장비) 표시 안 함 | S3 §1.2 (0.3.0) |
| 41 | 10-20 | 원장 호출 = [전체] · [특정 의사] | S3 §5.4 · §6.5(D-24) |
| 42 | 10-20 | ~~콜 승인 = 진행~~ → 첫 [시작] = 시술 진행 | S3 §5.2 · §5.6(D-32) |
| 43 | 10-20 | `/staff` 「들어온 콜」 칸 — 행 69 가 대체(의국 화면) | S3 §5.5(D-27) — 뒤집힘 |
| 44 | 10-20 | 시술 중 화면 조작 안 함 — 행 71 이 대체 | S3 §5.6(D-29) — 뒤집힘 |
| 45 | 10-20 | ~~수락 때 KOS 두 층~~ → flow-step 은 첫 [시작] | S3 §8 첫 [시작] 줄 |
| 46 | 10-20 | 상태 두 층(일정 진행 · 시술마다 진행/대기/완료) | S3 §5.2 · §5.9 |
| 47 | 10-20 | 고객 중심 · 시술마다 [시작] · [종료] · 순서 자유 | S3 §5.6 · §5.10(D-30) |
| 48 | 10-20 | 화면 분할(스테이션 = 시작 전 · 귀가만) — 행 71 이 고침 | S3 §5.6 · §6.7 #6 — 일부 뒤집힘 |
| 49 | 10-20 | KOS ↔ ccc 계속 동기화 | S3 §4 |
| 50 | 10-20 | 화면 3개(고객 모니터 다음 · 태블릿/폰 · 현황) | S3 §1.2 · S4 §1.1 |
| 51 | 10-20 | 태블릿 · 폰 = 개인 계정 로그인 | S4 §3.1 · §3.3(A-03) |
| 52 | 10-20 | 태블릿 · 폰 목록 = 전체 고객 | S4 §6.2 |
| 53 | 10-20 | KOS 시스템 계정 1개 · 담당자 = 시스템 계정 | S3 §4.1 · §4.6 · §8(D-11 · D-24) |
| 54 | 10-20 | (사실) 내부 `sign-in` 모양 · 수명 ≈ 14시간 | S3 §4.1 |
| 55 | 10-20 | 토큰 = 만료 시각 기준 · 10분 전 · 401 1회 · SQLite → PG+Redis | S3 §4.1 · §2.2 · §3.1(D-07 · D-15) |
| 56 | 10-20 | 데이터 원천 = 데모 실연동 · ~~v1 시드 주석~~(행 111 새 폴더로 대체) | S3 §1.1 · §7.4(D-01 · D-06) |
| 57 | 10-21 | 시안 확정(r3) · P1 ~ P19 | S3 머리말 · §6 · §6.7(D-16) |
| 58 | 10-21 | 플로우 ① PROCEDURE_WAITING 이면 카드 · 수납 필요 | S3 §5.1 · §6.7 #7(D-21) |
| 59 | 10-21 | (사실) 「방 배정」 ETCETERA · 방 없음 = 라운지 | S3 §3.3 · §5.1(D-22) |
| 60 | 10-21 | 방 있는 고객만 · ~~방 배정 안 보임~~(E2E-4 뒤집음) | S3 §5.1 · §6.3 (0.3.0) |
| 61 | 10-21 | 플로우 ② 마취 = 진행과 별개 | S3 §5.3 · §6.7 #1(D-23) |
| 62 | 10-21 | 마취 확인 필요 = 20분 | S3 §5.8 · §7.2 `limits.anesMin`(D-20) |
| 63 | 10-21 | KOS 「마취용」 배정 안 함 | S3 §5.3 · §1.2(D-23) |
| 64 | 10-21 | 플로우 ③④ 호출 쌓기 · 유효 호출 · 받는 범위 | S3 §3.2 · §5.4 · §5.5 · §6.7 #2(D-25 · D-27) |
| 65 | 10-21 | [시작] 조건 — 수락 전 꺼짐 · 담당의 | S3 §5.6 · §5.9(D-30) |
| 66 | 10-21 | 새 호출이면 [시작] 꺼짐 | S3 §5.4 · §5.6 |
| 67 | 10-21 | 진행 · 완료 시술 원장 못 바꿈 · ③ 기본값(지정 = 같은 요청 · 원장 목록 · 비어 있음) | S3 §5.4 · §4.6 · OQ-501(D-26) |
| 68 | 10-21 | [되돌리기] 뺌 · [다른 원장에게] = 새 전체 호출 | S3 §5.5 · §6.7 #3(D-27 · D-28) |
| 69 | 10-21 | 수락 = 의국 화면(호출 탭) · 앱 수락은 나중(→ S4) | S3 §5.5 · §6.4 · S4 §3.4 |
| 70 | 10-21 | 되돌리기 정책 안 정함 · 현장은 KOS 직접 조작 안 함 | S3 §1.2 · §4.4 · OQ-509(D-10 · D-28) |
| 71 | 10-21 | 플로우 ⑤ 지금은 현황판에서 [시작] · [종료] | S3 §5.6 · §6.7 #6(D-29) · S4(앱) |
| 72 | 10-21 | [종료] = 시작한 시술만 | S3 §5.6 · §5.11(D-31) |
| 73 | 10-21 | 시안 r4 — 카드 아래 큰 버튼 하나 | S3 §5.11 · §6.3(Q1 ~ Q4) |
| 74 | 10-21 | 플로우 ⑥ [귀가 대기] = 방 빼기 | S3 §5.7(D-33) |
| 75 | 10-21 | (사실) KOS 는 완료해도 `room` 안 지움 | S3 §4.3 |
| 76 | 10-21 | (사실) KOS 화면은 마지막 완료 때 방을 비워 보임 | S3 §5.7 · §8 마지막 줄 |
| 77 | 10-21 | ccc 는 시술 완료로 방 안 비움 | S3 §5.7(D-33) |
| 78 | 10-21 | 플로우 ⑦ KOS 기준 / ccc 기준 · 반영 중 · 재전송 | S3 §4.3 · §4.4(D-09) |
| 79 | 10-21 | 장기: KOS 점진 교체 · ccc DB 에 저장 | S3 §3.1(D-12) |
| 80 | 10-21 | (사실) `get-schedules-grouped-by-zone` | S3 §4.2 |
| 81 | 10-21 | 데이터 모델 원칙(ccc id + kos_id · 이벤트 로그) | S3 §3.1 · §3.2(D-12 · D-13) |
| 82 | 10-21 | 조회 구역 = 4층 | S3 §2.3 · §4.2(D-08) |
| 83 | 10-21 | 직원 · 방 = 1시간 + 서버 시작 | S3 §4.2 · §4.6(D-08) |
| 84 | 10-21 | 조회 시간 09:00 ~ 21:00 KST | S3 §4.2(D-08) |
| 85 | 10-21 | 시스템 계정 = 사용자 개인 계정 · 관리자 · 원장 목록에서 id 로 뺌 | S3 §4.1 · §4.6 |
| 86 | 10-21 | 데모는 시스템 계정 원장 태그 유지 · 운영은 의사만 | S3 §4.6 (0.3.0) |
| 87 | 10-21 | KOS 「진행중」 = 수락 그대로(E2E-2) | S3 §8 (0.3.0) |
| 88 | 10-21 | [귀가 대기] = 남은 작업 취소 → PROCEDURE_DONE · 카드 흐리게 남음 → COMPLETED 때 사라짐 | S3 §5.1 · §5.7 · §8 · §9 #9 (0.3.0) |
| 89 | 10-21 | 디자인 2단계 = Flutter 앱 | S4 A-01 · §1.1 |
| 90 | 10-21 | 앱 로직 정본 = 코드 스냅샷 | S4 A-02 · §6.0 |
| 91 | 10-21 | 계정 = 어드민 · 의사 · 간호사 · 사람마다 | S4 A-03 · §3.1 |
| 92 | 10-21 | 통역 = 이전 PoC 복사 · 언어 8 | S4 A-04 · §4 |
| 93 | 10-21 | 앱에서 뺀 것(동의서 · 메모 · 다시 알림 · 간호사 요청 · 빈 방) | S4 A-06 · §1.2 |
| 94 | 10-21 | 의사 = 자기 자신으로 수락 | S4 A-07 · §3.4 |
| 95 | 10-21 | 권한 = back 조작 API 마다 | S4 A-08 · §3.4 · §8.1 |
| 96 | 10-21 | 앱 E2E = 로컬 + 아이폰 + 아이패드 · TestFlight | S4 A-09 · §2.4 · §8.4 |
| 97 | 10-21 | ~~앱 E2E 뒤 최종 배포 · 주소 기본 맥 IP~~ — 행 104 가 뒤집음 | S4 A-12 · A-20 — 뒤집힘 |
| 98 | 10-21 | 원장 호출 푸시(APNs 직접) | S4 A-14 · §5-1 · S3 §1.2 (0.3.0) |
| 99 | 10-21 | 관리자도 모든 호출 푸시 · 앱 관리자 수락 = 원장 고름 | S4 A-15 · §5-1.2 · §6.3 #2 |
| 100 | 10-21 | 알림에서 바로 [수락] · `CALL` · 워치 | S4 A-17 · §5-1.2 · §5-1.3 · §8.4 D7 · OQ-616 (0.3.0) |
| 101 | 10-21 | `push_log` · `X-Accept-Source` | S4 A-18 · §3.5 · §5-1.2 · S3 §7.3 (0.3.0) |
| 102 | 10-21 | Apple 번들 id 등록 · 팀 id 레포 밖 | S4 A-19 · §2.4 (0.3.0 · 값은 적지 않음) |
| 103 | 10-21 | App Store Connect 레코드 · 액세스 전체 · APNs 키 | S4 A-19 · OQ-613 닫힘 (0.3.0) |
| 104 | 10-21 | 배포 먼저 · 앱 = 배포 주소 TestFlight | S4 A-20 · §2.2 · §2.4 · §8.4 · W4 WP10 (0.3.0) |
| 105 | 10-21 | 코드 #3 · 이미지 sha · Secret · infra #22 · ArgoCD sync | W4 「배포 기록」 (0.3.0) |
| 106 | 10-21 | 배포 완료 확인 · infra #23 · Cloudflare UA · 빌드 1 업로드 | S4 §8.5 · §2.4 빌드 기록 · W4 「배포 기록」 (0.3.0) |
| 107 | 10-21 | OQ-601 닫음 — 정상 로그인 | S4 A-16 · §3.3 · S3 §6.1 · §7.1 (0.3.0) |
| 108 | 10-21 | 기기 back = 맥 IP — 행 104 · T8 이 고침(debug 만) | S4 A-11 · §2.2 — 뒤집힘 (0.3.0) |
| 109 | 10-21 | (사실) 관리자 권한 쓰기 4종 200 · 대신 수락 | S4 A-13 · S3 §8 수락 줄 |
| 110 | 10-21 | 시술현황 새로 만듦 · 테마 유지 | S3 §1.1 · §2.4(D-01 · D-02) |
| 111 | 10-21 | 새 폴더 `procedure/` · 복사 · 기존 주소 교체 · `_archive/cc` · 메뉴 하나 | S3 §2.1 · §2.4 · §6.2 · W4 「배포 기록」(D-02 · D-03 · D-17) |
| 112 | 10-21 | ~~ccc 로그인 = 관리자 1개~~ — 행 91 · 107 이 고침 | S3 §1.1 · §7.1 · S4 §3 — 뒤집힘 (0.3.0) |
| 113 | 10-21 | ~~카드 로그인~~ — 행 107 이 뒤집음 | S3 §6.1 · §7.1 · S4 §3.3 — 뒤집힘 (0.3.0) |
| 114 | 10-21 | 범위 = 코드 구현 · 배포까지 | S3 §1.1(D-04) · W3 · W4 |
| 115 | 10-21 | 화면 갱신 = SSE | S3 §6.6 · §7.5 |
| 116 | 10-21 | 검증 = 단계별 · 통합은 마지막 한 번 | W3 Meta · W4 Meta |
| 117 | 10-21 | (사실) 시스템 계정 id = `get-user-account` · 같은 단계 flow-step 400 | S3 §4.1 · §8(S1 · S2) |
| 118 | 10-21 | (사실) `call-tasks-doctors` 400 = 시술 작업에 방 없음 | S3 §5.4 · §8 · OQ-516 (0.3.0) |
| 119 | 10-20 | (사실) 내부 API `Authorization: Bearer` · 조회 14/15 | S3 §4.1 |
| 120 | 10-20 | (사실) 내부 쓰기 4종 200 · 작업 하나씩 가능 | S3 §8 · workflow-v2 「KOS 반영 표」 |
| 121 | 10-20 | 한 방 = 원장 한 명 · 예외는 시술 골라 지정 | S3 §5.4 |
| 122 | 10-20 | 오더지 카드 나열 · [입실순 / 배치순] | S3 §6.3(D-17 · D-18) |
| 123 | 10-20 | ~~귀가 대기 흐리게 맨 뒤~~ → (E2E-8) 사라짐 — **E2E-9 가 다시 되돌림**(흐리게 남음 · 행 88) | S3 §5.1 · §5.7 (0.3.0) — 이 줄의 「사라짐」은 낡았다 |
| 124 | 10-20 | 카드 안 = 오더 메모 → 시술 · 메모 접기 · 펴기 | S3 §6.3(D-19) · E2E-12(카드 안 스크롤 없음) |
| 125 | 10-20 | ~~시술 목록 = 체크박스(완료)~~ → 체크 = 호출 고르기(시안) · 정렬 완료 → 진행 → 대기 | S3 §5.9 · §6.3 |
| 126 | 10-20 | (사실) 내부 순서 담당자 → 호출 → 수락 → 진행 | S3 §8 |
| 127 | 10-20 | (사실) `change-tasks-complete` · 공개 API 없음 | S3 §8 [종료] 줄 |
| 128 | 10-20 | (사실) KOS 상태 두 층(작업 칸 · flowStep) | S3 §5.2 · §8 · workflow-v2 §4 |
| 129 | 10-20 | ~~원장 쪽 모바일 앱~~ → 나중 — 행 89 가 다시 넣음 | S4 A-01 — 뒤집힘 |

100줄 · 누락 0. `_RESUME` §2 에 2026-10-22 날짜 줄은 없다 — 10-22 사실(코드 PR #5 · 데모 환자 190건 · 빌드 3)은 D.3.

### D.2 피드백 · 리뷰 · 처분 파일

| 파일 | 줄 | SPEC · WORK |
|---|---|---|
| `design-feedback-batch-1.md`(시안 v1 반려 · 10-20) | #1 구조 · 테마 = 배포 현황판 | S3 §2.4 · §6.2 · §6.4(시안 r3 으로 반영 · D-02 · D-17) |
| 〃 | #2 글자 · 컴포넌트 = 배포 코드 기준 | S3 §2.4(테마 복사) · 머리말(시안 정본) |
| 〃 | #3 카드 = 기존 카드 · 띠 없음 · 컴팩트 | S3 §6.3(P1 · r3 #2 · #3) |
| 〃 | #4 오른쪽 패널 = `Aside` · 탭(→ r3 에서 현황 · 호출 · 고객) | S3 §6.4(P17) |
| `e2e-feedback-batch-1.md`(웹) | E2E-1 ~ 10 · 12(11 번호 없음) | S3 부록 C(줄마다) |
| `e2e-app-feedback-batch-1.md`(앱 시뮬레이터) | A1 ~ A7 | S4 부록 B(줄마다) |
| `e2e-device-feedback-batch-1.md`(실기기 빌드 1 ~ 2) | T1 ~ T8 | S4 부록 B(줄마다 · T6 → S3 §5.11) |
| `review-wp1-5-report.md`(리뷰 r1) | F1 · F2 · F3 · W1 ~ W14 | 아래 `fix-decisions-r1.md` 처분 줄로 |
| 〃 | S1 ~ S12(SPEC 정정 제안) | S3 부록 B(줄마다) |
| `fix-decisions-r1.md` | F1 · F2 · S6(루트 `.env` 하나 · `build.args` · `front/.env.local`) | S3 §2.1 · §2.2 · §2.3 |
| 〃 | F3 · S9(SSE `?token` 접근 로그 지움) | S3 §7.5 |
| 〃 | W1 · S3(failed 뒤 KOS 값 · 실패 표시 유지) | S3 §4.3 · §4.4 |
| 〃 | W2 · S4(실패 뒤 뒤 op 멈춤) | S3 §3.2 · §4.4 |
| 〃 | W3 · W4 · W5 · S5(`limits` · 마취 `long` · 10초 발행) | S3 §6.6 · §7.2 · §7.5 |
| 〃 | W6(예외 삼키지 않음) | S3 §4.2 |
| 〃 | W7 · S12(시스템 id 모르면 원장 목록 유지) | S3 §4.6 |
| 〃 | W8(서버 시작 직원 · 방 1회) | S3 §2.2 · §4.2 |
| 〃 | W9(room 보호 안 함 · 비면 카드 사라짐) | S3 §4.3 |
| 〃 | W10 · S11(가짜 KOS 400 흉내 · OQ) | S3 §8 · OQ-516 |
| 〃 | W11 · S10(KST 00:00 전날 카드 내림) | S3 §4.2 · §5.1 |
| 〃 | W12(팩토리 · `--factory`) | S3 §2.2 |
| 〃 | W13 · S7(`PROC_FAKE_BOARD` 개발 전용 · 403) | S3 §2.3 · §7.3 |
| 〃 | W14 ①(빌드 인자 기본값) · ②(760px 미만 카드만 · S8) | S3 §2.2 · §6.8 |
| `review-r2-report.md`(리뷰 r2) | r1 F1 ~ W14 모두 PASS | 위 처분 줄 그대로 |
| 〃 | N1(2xx 비정상 본문 = 동기화 실패) | S3 §4.2 (r2) |
| 〃 | N2(멈춘 op 상태 = `failed` · `blockedOpIds`) | S3 §3.2 · §4.4 (r2) |

### D.3 배포 · 코드 사실

| 출처 | SPEC · WORK |
|---|---|
| 코드 PR #3(`0f4634a`) · #4(`329b543`) · #5(OPEN — 데모 환자 스킬 · 빌드 3 번호) | W4 「배포 기록」 · W3 「운영 도구」 · S4 §2.4 빌드 기록 |
| infra #22(교체 · Ingress SSE/WS · PVC · Secret · 옛 cc-db keep) | W4 「배포 기록」 · 「열린 것」 |
| infra #23(APNs `/etc/apns` · SA 토큰 끔) | S4 §2.3 `APNS_KEY_PATH` · W4 「배포 기록」 |
| infra #24(이미지 329b543 · Secret 예시 비밀번호 이름) | S4 §2.3 · W4 「배포 기록」 |
| ArgoCD 수동 sync(`cc-prototype-prod`) | W4 「배포 기록」 |
| TestFlight 빌드 1 · 2 · 3 | S4 §2.4 · §8.4 · OQ-618 · W4 WP9 · 「배포 기록」 |
| 데모 환자 190건(10-22) | W3 「운영 도구」 · S4 OQ-604 닫힘 |

누락 0.
