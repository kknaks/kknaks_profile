---
type: spec
id: SPEC-003
title: "명동 PoC v2 — 시술 현황판(procedure) · KOS 데모 지점 실연동 계약"
version: 0.5.1
status: draft
product: cc-prototype
feature: procedure
created_at: 2026-10-21
updated_at: 2026-10-26
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
    - "[[work-005-overall-board-procedure|WORK-005]]"
    - "[[work-006-overall-board-undo|WORK-006]]"
  releases: []
  related: []
---

# 명동 PoC v2 — 시술 현황판 계약

> 0.5.1(2026-10-26 · r6): review-doc r4(`orchestration/work/overall-board/review-doc-r4.md` FAIL 1 · WARN 6) 반영 + **WP-KOS 결과**(`kos-undo-probe-report.md` K1 ~ K4) — OQ-529 · OQ-530 **닫음(받음)** · [종료] 되돌리기 즉시 값 `READY` 확정. 바뀐 절: 머리말(W6) · §5.10 · §5.13 · §8(F1 · W1) · §9 #21 · #22 · 「0.5.0 더함」 · §10 OQ-528 ~ OQ-530 · 부록 I.3(W4) · **부록 J(새 — r4 처분)** · WORK-006(W2 · W3 · W5 · 게이트 통과). 지시 `spec-r6-instructions.md`. 줄 끝 `(r6)`.
> 0.5.0(2026-10-26 · r5): **[시작] · [종료] 되돌리기**(D-28 「되돌리기 없음」을 [시작] · [종료]에 한해 뒤집는다) · **웹 계약이 정본 — 앱(SPEC-004)은 나중에 웹에 맞춘다**. 원천 = `orchestration/work/overall-board/_RESUME.md` §2 2026-10-26 줄 3개(근거 `_RESUME 10-26`) · 지시 `spec-r5-addendum.md` · 코드 `cc-prototype/overall-board/procedure`(PR #6 상태 `9a317a2` — 읽기만) · medikit 1.4.0 `dist/index.d.ts`(`ConfirmModal` · `Tooltip` · `ResetIcon`). 바뀐 절: 머리말 우선순위 · §1.1 · §1.2 · §3.2 · §4.3 · §4.4 · §5.5 · §5.6 · §5.9 · §5.10 · §5.11 · **§5.13(새 — 되돌리기)** · §6.3 · §6.7 #3 · #23 · §7.2 · §7.3 · §7.4 · §7.5 · §8 · §9 #21 ~ #26 · §10(OQ-523 · OQ-526 닫음 · OQ-529 ~ OQ-533 새 · **§10.1 앱 후속(새)**) · 부록 A D-28 · **부록 I(새 — 10-26 반영표)**. 빌드 계획 = WORK-006. 줄 끝 `(r5)`.
> 0.4.3(2026-10-25 · r4): **코드가 먼저 간 10-25 결정을 문서에 맞춘다** — ① 카드 방 = **type 무관** 방 붙은 작업 중 배정 시각 최신 ② **규칙 하나**: KOS 작업은 type 무관 전부 같은 시술 · 예외 「방 배정」 하나(방 붙은 ETCETERA · ccc 호출 이력 없음) — 스냅샷에 싣고 `isRoomTask: true` · front 가 숨김 · 판정 제외 · [귀가 대기] 때 KOS 취소. 0.4.0 의 「기타 작업 읽기 전용 줄」 · 「back 에서 방 배정 거르기」는 뒤집힘. 원천 = `orchestration/work/overall-board/_RESUME.md` §2 2026-10-25 줄(근거 `_RESUME 10-25`) · `room-fix-instructions.md` · `one-rule-instructions.md` · `backend-r1-report.md`(WP-BE3 · 규칙 하나) · `frontend-r1-report.md`(재수정) · 코드 `cc-prototype/overall-board/procedure`(작업 트리 · 시험 162 통과). 바뀐 절: §3.2 · §3.3 · §5.1 · §5.4 · §5.7 · §5.9 · §5.11 · §6.3 · §6.4 · §6.7 · §7.2 · §7.3 · §9 · §10 · 부록 A · 부록 E · **부록 H(새 — 10-25 반영표 · r4 처분)**. 줄 끝 `(r4)`.
> 0.4.2(2026-10-23 · r3): review-doc r2(`orchestration/work/overall-board/review-doc-r2.md` FAIL 1 · WARN 6) 반영 — §5.11 · §5.12(방향 판정 기준 · 경합 ② 비교 · 그사이 귀가 대기) · §6.4 고객 탭 순서 · §7.3 · 부록 E #3 · **부록 G(새 — r2 처분표)** · SPEC-004 0.3.1. 줄 끝 `(r3)`.
> 0.4.1(2026-10-23 · r2): review-doc r1(`orchestration/work/overall-board/review-doc-r1.md` FAIL 2 · WARN 12) 반영 — §3.2 · §5.1 · §5.11 · §5.12 · §6 머리 표 · §6.3 · §6.4 · §6.7 · §7.3 · §9 · §10 · 부록 E(10줄) · **부록 F(새 — r1 처분표)** · 머리말 우선순위 · SPEC-004 §3.4 한 줄. 줄 끝 `(r2)`.
> 0.4.0(2026-10-23): **시술 현황 → 「Ceramique 전체현황판」 시안의 「현황 › 시술 현황」 하위 화면으로 옮긴다** — 원천 = `orchestration/work/overall-board/_RESUME.md` §2 2026-10-23 결정 줄(아래 근거 `_RESUME 10-23`) ·
> 시안 `reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html`(근거 `M:줄`) · 읽기 리포트 `orchestration/work/overall-board/design-analysis-report.md`(근거 `DA §n`) ·
> 지금 코드 인벤토리 `orchestration/work/overall-board/current-board-report.md`(근거 `CB §n`). 바뀐 절: §1 · §2.4 · §3.2 · §5.1 · §5.9 · **§5.12(새 — 카드 순서)** · §6 머리 표 · §6.2 · §6.3 · §6.4 · §6.7 ·
> §7.2 · §7.3 · §7.4 · §7.5 · §9 · §10 · 부록 A · **부록 E(새 — 10-23 결정 줄 → 절 반영표)**. 뒤집힌 줄은 ~~취소선~~ + 「(0.4.0 바뀜)」, 새 줄 끝에 `(0.4.0)`. 예약 현황 · 원내 현황 · 다른 상단 메뉴는 이 문서 범위 밖(§1.2).
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
> DEC-005 가 맞다(§6.7). **0.4.0 부터는 `_RESUME 10-23` 결정 줄 > DEC-005**(D-17 · D-18 · D-22 일부를 뒤집는다 — 부록 A · 부록 E). DEC-005 파일은 개정하지 않는다 (r2) — `_RESUME 10-23` 「review-doc r1 기본값 ①」 줄. **0.5.0 부터 `_RESUME 10-26` > DEC-005 D-28**(되돌리기 — §5.13) (r5).
> **웹 계약(이 문서)이 정본이다 — SPEC-004(시술실 앱)는 따른다.** 웹과 앱의 규칙이 다르면 앱이 틀린 것으로 보고 §10.1 「앱 후속」 목록에 올린다(열린 질문으로 두지 않는다) (r5) — `_RESUME 10-26` 「웹이 정본」 줄. (r6)
> 업무 흐름은 `reference/2026-10-12-cc-prototype/workflow-v2.md`.
>
> 근거 표기: `D-nn` = DEC-005 · `P-nn` / `Q-n` = 시안 읽기 리포트 · `HAR` = `_RESUME.md` §2 「(사실)」 줄 · `API` =
> `kos-demo-api.md` · `기본값` = 결정에 없어 이 문서가 고른 구현값(§10 에 같이 올린다).
> 0.4.3 근거 표기: `_RESUME 10-25` = 같은 파일 §2 2026-10-25 줄 (r4)
> 0.5.0 근거 표기: `_RESUME 10-26` = 같은 파일 §2 2026-10-26 줄(「되돌리기 기능 추가」 · 「아이콘 위치」 · 「웹이 정본」) · `MK` = medikit 1.4.0 `procedure/front/node_modules/@medisolve-ai/medikit/dist/index.d.ts` (r5)
> 0.4.0 근거 표기: `_RESUME 10-23` = `orchestration/work/overall-board/_RESUME.md` §2 2026-10-23 줄 · `M:n` = 전체현황판 시안 줄 · `DA §n` · `CB §n` = 위 두 리포트 절 (0.4.0)
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
| 화면 = 「Ceramique 전체현황판」 시안의 **「현황 › 시술 현황」 하위 화면**(헤더 메뉴 「현황」 하나 · 사이드바 없음 — §6.2) (0.4.0) | `_RESUME 10-23` 목적 · 헤더 줄 · `M:63-92` · `M:777-1153` |
| **카드 드래그 순서** — back DB 저장 · 모든 화면 공유(SSE 스냅샷) · KOS 반영 없음(§5.12) (0.4.0) | `_RESUME 10-23` 드래그 순서 줄 · `M:1425-1430` · `M:1464-1472` |
| **[시작] · [종료] 되돌리기**(웹) — 토스트 [되돌리기] · 시술 줄 되돌리기 아이콘 + 확인 모달 · KOS 반영(§5.13 · §8) (r5) | `_RESUME 10-26` 「되돌리기 기능 추가」 · 「아이콘 위치」 줄 |
| ~~이번 목표 = 사용자 **로컬 E2E**. 배포(D-03)는 그 뒤 마지막 WP~~ → 로컬 E2E 뒤 **배포 완료**(2026-10-21 · `ccc.medisolveai.xyz` = procedure · WORK-004 WP10) (0.3.0) | D-03 · `_RESUME` 10-21 배포 완료 줄 |

### 1.2 Out

| 무엇 | 근거 |
|---|---|
| 시술실 고객 모니터 | D-34 |
| ~~시술실 태블릿 · 폰(디자인 2단계) · 개인 계정 · 앱 수락~~ → **SPEC-004(시술실 앱 · 계정 · 권한)로 들어갔다** — 이 문서 범위 밖일 뿐 Out 이 아니다 (0.3.0) | `_RESUME` 10-21 「디자인 2단계 = Flutter PoC 앱」 줄 · SPEC-004 A-01 · A-03 |
| ~~되돌리기(호출 · 수락 · [종료] 실수 포함) — 로그만 쌓는다~~ (r5 바뀜) → **호출 · 수락 · [다른 원장에게] · [귀가 대기] · 마취 되돌리기** — 로그만 쌓는다. [시작] · [종료] 되돌리기는 In(§5.13) | D-28 · D-13 · D-34 · `_RESUME 10-26`(결정 범위 = [시작] · [종료]) |
| 시술 차트(KOS `assigneeMemo` · `doctorMemo` · `memo`) | D-34 |
| 라운지 / 내원현황(방 미리 배정). ~~원장 호출 휴대폰 알림~~ → SPEC-004 §5-1(APNs 푸시)로 들어갔다 (0.3.0) | D-34 · D-22 · SPEC-004 A-14 |
| KOS 「마취용」 계정 배정 · KOS 화면 직접 조작 | D-23 · D-10 |
| 운영 명동점 키 · 운영 지점 | D-06 |
| 연락처 · 생년월일 · 고객 메모 저장 | D-14 |
| 시술 준비(약물 · 장비) 표시 (0.3.0) | `_RESUME` 10-20 「시술 준비는 현황판에 표시하지 않는다」 줄 |
| 전체현황판의 **예약 현황 · 원내 현황** 하위 화면 · 상단 메뉴 「현황」 밖 5개(고객 · 예약 · 시술 기록 · 매출 · 설정) — 예약 현황은 workflow-v2 예약 구간 → KOS API 조사 뒤 다음 판 (0.4.0) | `_RESUME 10-23` 목적 · 헤더 · 예약 현황 줄 |

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
| `cc/front/components/common/AppHeader.tsx` | `components/common/` | **모양만**(높이 57 · 로고 · 메뉴 간격 · 시계 · 로그아웃). ~~메뉴 = 「시술 현황」 하나(D-17)~~ (0.4.0 바뀜) → 메뉴 = 상단 「현황」 하나 + 호버 드롭다운(§6.2) · 세션 = §7.1 |
| `cc/front/app/(main)/desk/page.tsx` 의 틀(~~사이드바 `Menu`~~ (0.4.0 바뀜 — 사이드바 없음 · §6.2) · main 여백 · 제목 줄 · 토스트) | `app/(main)/procedures/` | **모양만**. ~~메뉴 항목 = 「시술 현황」~~ (0.4.0 바뀜 — 메뉴는 헤더 드롭다운만) |
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
| `visit`(일정 1건 = 카드 1장) | `id` · `kos_id` · `customer_id` · `zone_kos_id` · `flow_step` · `flow_step_at` · `order_memo` · `room_id` · `room_assigned_at` · `kos_updated_at` · `synced_at` · `seen_at`(ccc 가 처음 본 시각) · `present`(마지막 일정 조회에 있었나) · `open_task_seqs`(json — KOS 에서 끝나지 않은 작업 sequence, 종류 무관 · ~~[귀가 대기] 취소 대상 · §5.7~~ (r4 바뀜) → **저장만 · 취소 계산에 쓰지 않는다**(§5.7)) (0.3.0 · r4) | 일정(10초) · 코드 `repository/db.py` |
| `procedure`(작업 1개) | `id` · `visit_id` · `kos_sequence`(`kos_id` 역할 — 일정 `kos_id` + sequence) · `kos_order` · `title` · `kos_status` · `payment_required` · `doctor_staff_ids`(json) · `assignee_staff_ids`(json) · `doctor_assigned_at` · `doctor_call_at` · `completed_at` · `synced_at` · `present`(KOS 작업 목록에 있나 · 빠지면 0, 행은 남김) · `room_kos_id`(작업에 들어간 방 — 호출 전 방 넣기 판단 · §5.4) · **`kind`**(`procedure` = KOS `PROCEDURE` · `etc` = `ETCETERA` **전부 저장** — ~~방 있는 것(「방 배정」)은 스냅샷에서 뺀다 · §5.1 (r2)~~ (r4 바뀜) → **규칙은 type 무관**(§5.1) · 「방 배정」 판정(§5.1)에만 쓴다 (r4)) (0.3.0) | 일정 `tasks[]` type `PROCEDURE` **+ `ETCETERA`**(10초) — E2E-4 (0.3.0) |

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
| `board_order`(카드 드래그 순서 · 하루 1행) (0.4.0) | `day`(KST 날짜 `YYYY-MM-DD` · PK) · `visit_ids`(json — 귀가 대기 아닌 카드의 visit id 를 앞에서부터) · `updated_at` · `updated_by`(로그인 아이디) · `event_id`(그 순서를 만든 `event_log`) | `_RESUME 10-23` 드래그 순서 줄 · §5.12 |

`event_log.type`: `anes_start` · `anes_end` · `call_create` · `call_reassign_all` · `call_accept` · `proc_start` · `proc_finish` · `home` · `kos_failed` · **`board_order`**(0.4.0) · **`proc_undo_start`** · **`proc_undo_finish`**(r5 — §5.13) — D-13 · D-27 「로그에는 수락한 원장 · 시각 · 시술 · 호출 id」.
`board_order` payload = `{day, visitIds}`(저장된 목록 — §5.12 거르기 뒤) · `visit_id` 칸은 비움(카드 여럿) (0.4.0) — D-13(조작은 이벤트 한 줄 · 다른 표는 투영) · `_RESUME 10-23`.

- `board_order` 는 ccc 원천(KOS 에 없음 · `kos_op` 0줄). 새 표라 서버 시작 때 `CREATE TABLE IF NOT EXISTS` 로 생긴다 — 기존 DB 파일에 열 추가(ALTER) 없음(코드 `repository/db.py` `SCHEMA` 방식 그대로) (0.4.0)
`call_accept` payload = `{callId, doctorId, procedureIds, byRole, source}`(`source` = `push` \| `app` \| `web` — SPEC-004 §3.5) · `home` payload = `{cancelSequences}`(§5.7) (0.3.0) — 코드 `service/actions.py`.

`proc_undo_start` payload = `{procedureId, startedAt, startedEventId, flowStepChanged}`(지운 [시작] 시각 · 그 [시작] 이벤트 · 고객 상태를 시술 대기로 돌렸나) · `proc_undo_finish` payload = `{procedureId, completedAt}`(지운 완료 시각). 되돌리기도 **추가만** — 앞 `proc_start` · `proc_finish` 줄은 고치지 · 지우지 않는다(D-13). 새 표 · 새 열 없음 — `procedure.started_at` · `started_event_id` · `completed_at` · `kos_status` 를 바꾸는 투영뿐 (r5) — D-13 · 기본값

계정(`account`) · 기기(`device`) · 푸시 내역(`push_log`) 테이블은 SPEC-004 §3.1 · §5-1 (0.3.0).

### 3.3 KOS 필드 대응표

| ccc | KOS | 어디서 | 근거 |
|---|---|---|---|
| `staff.kos_id` · `name` · `role_tags` · `active` | `id` · `name` · `roleTags[]` · `activate` | 공개 `getAccounts` `data[]` | API §3.5 |
| `room.kos_id` · `zone_kos_id` · `title` · `order` | `id` · `zoneId` · `title` · `order` | 내부 `get-rooms` `data[]` | HAR(`시술현황_새로고침.har` 응답 모양) |
| `visit.kos_id` · `flow_step` · `flow_step_at` · `order_memo` · `kos_updated_at` · `zone_kos_id` | `id` · `flowStep` · `flowStepUpdatedDateTimeUtc` · `orderMemo` · `updatedDateTimeUtc` · `zone.id` | 내부 `get-schedules-grouped-by-zone` `data[].schedules[]` | HAR · API §3.3 |
| `visit.room_id` · `room_assigned_at` | ~~`tasks[]` 중 type `ETCETERA` 이고 `room` 있는 작업의 `room.id` · `roomAssignedDateTimeUtc`~~ (r4 바뀜) → `tasks[]` 중 **type 무관 `room` 있는 작업**(상태 무관 — 취소된 「방 배정」도 후보) 가운데 `roomAssignedDateTimeUtc` **가장 늦은 것**의 `room.id` · `roomAssignedDateTimeUtc`(입실 시각도 같은 작업). 배정 시각이 같거나 없으면 ① ETCETERA 먼저 ② 큰 `sequence`(기본값 — 코드 `kos/sync.py` `_card_room_task`) (r4) | 같은 일정 | D-18 · D-22 · HAR(방 배정 작업 · room) · `_RESUME 10-25` 「카드 방 = KOS 작업 어디든」 줄 |
| `customer.kos_id` · `name` · `phonetic_name` · `nationality` · `is_new` · `chart_number` | `visitor.id` · `name` · `phoneticName` · `nationality` · `isNew` · `chartNumber` | 같은 일정 | D-14 · API §3.3 |
| `procedure.kos_sequence` · `kos_order` · `title` · `kos_status` · `payment_required` | `tasks[].sequence` · `order` · `title` · `status` · `paymentRequired` | type `PROCEDURE` · `ETCETERA` 작업(그 밖 type 은 버림) (0.3.0) | D-22 · API §3.3 · E2E-4 |
| `procedure.kind` · `room_kos_id` | `tasks[].type`(`PROCEDURE` → `procedure` · `ETCETERA` → `etc`) · `tasks[].room.id` | 같은 작업 (0.3.0) | E2E-4 · E2E-1 · 코드 `kos/sync.py` |
| `visit.open_task_seqs` | `tasks[]` 중 `status` 가 `DONE` · `CANCELED` 아닌 작업의 `sequence`(종류 무관) — 저장만 · [귀가 대기] 취소 계산엔 안 씀(§5.7 · r4) | 같은 일정 (0.3.0) | E2E-3 · 코드 `kos/sync.py` |
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
| 시술 완료 · 완료 시각 | KOS | 덮어씀. 반영 대기 중인 `change-tasks-complete` 가 있으면 그 작업은 덮어쓰지 않는다 — [종료] 되돌리기(`complete:false` · §8)도 같은 경로라 같은 보호를 받는다(코드 `kos/sync.py` `guarded` = 대기 op 의 `sequences` · 경로 무관) (r5) | D-09 · §5.13 |
| 집도의(`doctors`) · 담당자 · 호출 여부(`status` WAITING · `doctorCallDateTime`) | KOS | 덮어씀. 반영 대기 중인 호출 · 수락이 있으면 그 작업은 덮어쓰지 않는다 | D-09 |
| 마취 회차 · [시작] 시각 · 호출 기록 · 지정 원장 · 수락 기록 · [귀가 대기] 누른 시각 | ccc | 조회가 건드리지 않는다. [시작] 시각은 [시작] 되돌리기(§5.13)로만 지워진다 (r5) | D-09 · D-12 |

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
- **실패 뒤 KOS 기준 필드는 KOS 값으로 돌아간다**(다음 조회부터 덮어쓴다 · §4.3). ccc 에만 있는 기록(이벤트 · 호출 · 수락 · [시작] 시각)은 지우지 않는다(실패를 되돌리지 않는다 — D-28 · 사용자 [시작] · [종료] 되돌리기(§5.13)와는 다른 이야기 (r5)). **[종료] 되돌리기 op 이 `failed` 면 다음 조회부터 KOS 값(`DONE`)으로 돌아가 그 시술은 다시 완료로 보인다**(§5.13 · OQ-529) (r5). 카드의 「KOS 반영 실패」는 **그 visit 의 다음 op 이 `confirmed` 될 때까지 남는다** (0.2.0) — S3 · 처분 W1
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
3. **방이 있다**(§3.3 `visit.room_id`) — 방 없는 고객 = 라운지 대기 = 안 나온다 — D-22. ~~방 = 「방 배정」(ETCETERA) 작업의 방~~ (r4 바뀜) → 방 = **KOS 작업 어디든(PROCEDURE · ETCETERA) 붙은 방** — 「방 배정」 작업이 없고 시술 작업에만 방이 있어도 카드가 뜬다(데모 10-25 고객 3명이 방은 있는데 카드 0 이던 것) (r4) — `_RESUME 10-25` 「카드 방」 줄
4. 수납 전(`payment_required` 인 시술이 있음)이어도 띄우고 「수납 필요」 표시 — D-21

- ~~시술 목록 = type `PROCEDURE` 작업만. 「방 배정」 등 ETCETERA 작업은 시술 목록에 안 보인다 → **ETCETERA(「방 배정」 등)도 스냅샷에 실린다** (0.4.0 바뀜 — 아래 「방 배정」 줄) → **방 없는 ETCETERA(마취 · 시트팩 등)는 스냅샷에 실린다** (r2) — `procedures[].kind = "etc"` · 읽기 전용(제목 + KOS 상태) · 호출 · 시작 · 종료 · 「전부 완료」 · 「수납 필요」 판정에서 빠진다(규칙은 `kind = procedure` 만 본다). KOS `CANCELED` 작업은 목록에서 뺀다(OQ-506) (0.3.0) — E2E-4 · 코드 `domain/rules.py` `items` · `procedures`~~ (r4 바뀜 — 아래 「규칙 하나」)
- ~~현황판(웹)이 `etc` 줄을 **그리지 않게** 하는 것은 E2E-10 으로 기록만 됐다 — 코드(웹)는 아직 카드 맨 위에 그린다 · 앱은 그리지 않는다(SPEC-004 §6.0) → §10 OQ-517 (0.3.0)~~ (0.4.0 바뀜 — OQ-517 닫음)
- ~~**「방 배정」 작업은 스냅샷 `procedures[]` 에서 뺀다** = `kind = etc` 이고 **작업에 방이 있는 것**(`procedure.room_kos_id` 있음 — KOS ETCETERA 중 `room` 있는 작업 · 카드 방을 고르는 판정과 같은 규칙, 코드 `kos/sync.py:39-40` `_room_task`). 방 있는 ETCETERA 가 여럿이어도(OQ-511 「방 점유/원장 상담」 등) **전부** 뺀다. **그 밖 ETCETERA(마취 · 시트팩 · 관리 마무리 등 — 방 없는 기타 작업)는 남긴다** — 지금처럼 읽기 전용 줄(제목 + KOS 상태 · §6.3) (0.4.0) — `_RESUME 10-23` 「방 배정」 줄 · OQ-517 닫음~~ (r4 바뀜 — 거르지 않고 싣는다 · `isRoomTask`)
  - ~~빼는 자리 = **back**(`domain/rules.py` 「카드에 보이는 작업」 `items` 한 곳). 근거: ① 스냅샷 `procedures[]` 에는 작업 방 필드가 없어 front 는 「방 배정」과 다른 기타 작업을 가를 수 없다 ② 규칙 계산은 back 한 곳(§7.2) ③ 앱도 같은 스냅샷을 쓴다 — 앱은 `etc` 를 그리지 않으므로(SPEC-004 §6.0) 바뀌는 화면이 없다 (0.4.0)~~ (r4 바뀜)
  - ~~[귀가 대기]의 「방 배정」 취소(§5.7)는 그대로 — 취소 대상은 `visit.open_task_seqs`(스냅샷과 무관 · §3.3)에서 고른다. 호출 전 방 넣기(§5.4)의 카드 방도 `visit.room_id` 그대로 (0.4.0) — 코드 `service/actions.py` · `kos/sync.py`~~ (r4 바뀜 — 취소 대상 = 안 끝난 「방 배정」 · §5.7)
- **규칙 하나**(r4): **KOS 작업은 type(PROCEDURE · ETCETERA) 무관 전부 같은 시술** — 표시 · 체크 · 호출 · [시작] · [종료] · 「전부 완료」 · 「수납 필요」 · 고객 상태 · 「확인이 필요」 · 원장 바쁨 판정 모두 같은 규칙. 스냅샷 `procedures[]` = 작업 **전부**(KOS `CANCELED` 만 뺀다 · OQ-506). 마취 · 시트팩 · 관리 마무리 같은 ETCETERA 도 일반 시술 줄이다 — `_RESUME 10-25` 「규칙 하나」 줄 · 코드 `domain/rules.py` `items` · `procedures`
- **예외는 「방 배정」 하나**(r4) = **방 붙은 ETCETERA**(`kind = etc` 이고 그 작업의 `room_kos_id` 있음) **이면서 ccc 가 한 번도 호출하지 않은 작업**(`doctor_call_item` 에 없음). 판정 한 곳 = 코드 `domain/rules.py` `Rules.is_room_task` — `_RESUME 10-25` 「「방 배정」 판정」 줄
  - 호출 이력 조건의 이유: 「방 배정」은 호출 대상이 아니므로 호출된 적이 있으면 「방 배정」일 수 없다. 이 조건이 없으면 시트팩에 [의사 호출]을 하는 순간 호출 전 방 넣기(§5.4 `change-tasks-room`)로 방이 붙어 「방 배정」으로 바뀌어 버린다(backend 재현) — KOS 쓰기는 그대로
  - 「방 배정」은 **스냅샷에 싣는다** — `procedures[].isRoomTask = true`(§7.2). **front 가 숨긴다**(카드 시술 줄 · 고객 탭 번호 원 · 호출 대상 · 개수 어디에도 안 보임 — §6.3 · §6.4)
  - **판정에서 뺀다**: `pickable` · `canStart` · `canFinish` = false · [시작] · [종료] API = 404(§7.3) · 「전부 완료」 · 「수납 필요」 · `canCall` · `need` · 호출 받을 시술 · 원장 바쁨에 안 든다 → 「전부 완료」가 「방 배정」을 기다리지 않는다
  - **[귀가 대기] 때 KOS 에서 취소**(§5.7)
- 「방 배정」 판정과 카드 방 고르기(§3.3 · 조건 3)는 **다른 판정**이다 — 카드 방은 type 무관 · 상태 무관(r4)
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
- KOS: ① **`change-tasks-room`(카드 방(~~= 「방 배정」 작업의 방~~ (r4) → §3.3 type 무관으로 고른 방)을 고른 시술 작업에 덮어쓴다 — 시술 작업에 다른 방이 있어도 · 고른 작업은 type 무관(시트팩도 같다 · r4))** → ② `change-tasks-assignees`(담당 = 시스템 계정) → ③ `call-tasks-doctors`(고른 시술의 sequences). 고른 작업이 이미 다 그 방이면 ① 은 보내지 않고 `confirmed` 로 쌓는다. 방이 없는 시술 작업을 호출하면 KOS 가 400 `roomId NotFound` 를 준다 (0.3.0) — D-24 · §8 · E2E-1 · `_RESUME` 10-21 「`call-tasks-doctors` 400 = 시술 작업에 방이 없을 때」 줄

### 5.5 수락 · 다른 원장에게 (D-27 · D-28)

- 어디서 = 오른쪽 「호출」 탭(의국 화면) — 원장이 자기를 골라 [수락] — D-27
- **받는 시술** = 그 호출이 **유효 호출인 시술 중 아직 수락 안 된 것만** — 시안 P11(수락 전 호출 전부)을 고친다 — D-27
- 전체 호출: 원장 목록(비어 있는 원장 먼저)에서 고르고 [<원장> 수락] / 지정 호출: [수락](지정 원장으로) — D-27 · P8 · P9
- [다른 원장에게](지정 호출만) = 같은 시술(그 호출에서 아직 받을 것)로 **「전체」 호출을 새로 만든다**. 기존 지정 호출은 그대로 남는다(유효 호출이 새 것으로 넘어간다) — D-27 · D-25
- KOS: `change-tasks-doctors`(받는 sequences · 고른 원장 id). [다른 원장에게]의 KOS 요청 = §5.4 호출과 같다 — D-27 · §8
- [되돌리기] 없음(토스트 · 호출 탭 모두) — D-28. 10-26 되돌리기는 **[시작] · [종료]만**이다 — 수락 · 호출 되돌리기는 결정에 없어 그대로 없음 (r5 — 기본값 · `_RESUME 10-26` 결정 범위)
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
- [시작] · [종료]를 잘못 눌렀으면 되돌린다 — §5.13 (r5)

### 5.7 [귀가 대기] (D-33)

- 시술이 **전부 완료**일 때만 보인다(r4 — 「방 배정」을 뺀 작업 전부 · 시트팩 등 ETCETERA 가 안 끝났으면 [귀가 대기] 없음 · API 는 409 `procedures_not_done`)(그 전엔 버튼 자체가 없다 · 같은 자리는 [의사 호출]) — D-33 · Q1 · Q3
- = 방 빼기(라운지로). KOS ① **`cancel-flow-tasks`** — ~~마지막 조회에서 끝나지 않은 작업(`open_task_seqs`) 중 **시술 작업을 뺀 것**(「방 배정」 등)을~~ (r4 바뀜) → **카드 작업 중 아직 안 끝난 「방 배정」(§5.1 `is_room_task`)만** `reason: CANCEL` 로 취소(다른 작업은 전부 완료여야 [귀가 대기]가 되므로 취소할 것이 없다 · PROCEDURE · ETCETERA 밖 type 의 열린 작업은 취소하지 않는다) → ② `changeFlowStep(PROCEDURE_DONE)`. 남은 「방 배정」이 없으면 ① 은 만들지 않는다 (r4 — `_RESUME 10-25` 「규칙 하나」 줄 · 코드 `service/actions.py` `home`). 방 배정 취소는 시술 현황(ccc)이 한다 — ccc 가 ② 만 보내 KOS 에 「방 배정」이 준비중으로 남고 방이 안 비던 것 (0.3.0) — D-33 · E2E-3 · E2E-9 · 1차 HAR(KOS 화면 귀가 대기 = 같은 두 요청)
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
| `done` 완료 | KOS `status = DONE` | 「<원장> · HH:MM~HH:MM」 | (`canUndoFinish` 면 되돌리기 아이콘 →) 「완료」 Badge `neutral` (r5) | D-09 · 시안 #10 · #11 · `_RESUME 10-26` 아이콘 위치 |
| `doing` 진행 | ccc `started_at` 있음 · 완료 아님 | 「<원장> · HH:MM 시작」 | (`canUndoStart` 면 되돌리기 아이콘 →) [종료] solid blue (r5) | D-31 · 시안 · `_RESUME 10-26` 아이콘 위치 |
| `wait` 대기 · 유효 호출 미수락 | | 「전체 호출 · 수락 전」 / 「<원장> 지정 호출 · 수락 전」 | 「호출함」 Badge(파랑 외곽선) + [시작] 꺼짐 | D-30 · 시안 #10 · #11 |
| `wait` · 유효 호출 수락됨 | | 「<원장> 수락 · 시작 가능」(파랑) | [시작] outlined blue | D-30 · 시안 |
| `wait` · 호출 없음 · 담당의 있음 | | 「<원장>」 | [시작] | D-30 |
| `wait` · 호출 없음 · 담당의 없음 | | 「담당의 미정」 | [시작] 꺼짐 | D-30 · 시안 #10 |

- ~~순서 = 완료(완료 시각 순) → 진행 → 대기(KOS `sequence` 순) — 시안 `procRows` · workflow-v2 §5. `etc` 작업은 그 위에 sequence 순(웹 `orderedProcs`) (0.3.0)~~ (0.4.0 바뀜)
- **웹 카드 줄 순서 = 진행 → 대기(KOS `sequence` 순) → 완료(완료 시각 순)** · 완료 묶음 앞에 점선 한 줄(대기 · 진행이 위에 있을 때만). ~~남은 `etc` 작업(방 없는 기타 작업 · §5.1)은 그 위에 sequence 순(지금 자리 그대로)~~ (r4 바뀜) → type 무관 **모든 작업을 한 목록**으로(ETCETERA 를 맨 위에 따로 두지 않는다) · 「방 배정」은 그리지 않는다 (0.4.0 · r4 — 코드 `front/components/procedures/view.ts` `orderedProcs` · `procsOf`) — 시안 `M:1458-1460` · `M:1500-1503` (`[...doing, ...wait, ...done]` · `cut`) · `_RESUME 10-23` 「시안과 코드가 다른데 … 시안대로」
  - 줄 순서는 **웹 front 가 정한다**(지금도 `view.ts` `orderedProcs` 가 다시 정렬 — CB §4). back `procedures[]` 순서(완료 → 진행 → 대기)는 바꾸지 않는다 — 앱이 그 순서를 쓰는지와 무관하게 앱 화면이 바뀌지 않게(이번 판 범위 = 웹) (0.4.0) — 기본값
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
| 시술 | `doing` | [시작] 되돌리기(§5.13) | `wait`(호출 · 수락 · 집도의 그대로) | 없음 · 단 그 고객에 진행 · 완료 시술이 하나도 안 남으면 고객도 ↓ (r5) | `_RESUME 10-26` |
| 고객 | `doing` | 위 [시작] 되돌리기로 진행 · 완료 시술 0 | `waiting` | `changeFlowStep(PROCEDURE_WAITING)` — ~~이미 KOS 가 그 단계면 보내지 않음(§8 같은 단계 규칙)~~ (r6 바뀜) → ccc 고객 상태가 `doing` → `waiting` 이 될 때 **항상 op 1줄**. KOS 가 그 사이 이미 그 단계라 400 이 오면 §8 같은 단계 규칙(다음 조회에서 `confirmed`) (r5 · r6) | `_RESUME 10-26` · §5.13 |
| 시술 | `done`(ccc [시작] 있음) · 귀가 대기 아님 | [종료] 되돌리기(§5.13) | `doing`([시작] 시각 그대로) | `change-tasks-complete {complete:false}` — 고객 상태는 그대로(진행) (r5) | `_RESUME 10-26` · ~~OQ-529~~(닫힘 · 받음 — WP-KOS K2 (r6)) |
| 시술 | 아무 상태 | KOS `DONE` 조회 | `done` | — | D-09 |

### 5.11 버튼 활성 조건표

| 버튼 | 보임 | 켜짐 | 근거 |
|---|---|---|---|
| 줄 체크칸 · 「전체 선택」 | 귀가 대기 아닌 카드 | 그 시술이 `wait`(전체 선택 = `wait` 시술이 1개 이상) · 없으면 「호출할 대기 시술 없음」 회색 | D-26 · 시안 r4 #1 |
| 카드 아래 [의사 호출] | ~~귀가 대기 아님 · **시술이 전부 완료는 아님**~~ (r2 바뀜) → 스냅샷 **`canCall = true`** 일 때만(귀가 대기 아님 · 전부 완료 아님 · 호출할 수 있는 대기 시술 ≥ 1). `canHome` 도 `canCall` 도 아니면(기타 작업만 남은 카드 · 남은 시술이 진행 중뿐인 카드) **카드 아래 버튼 자리 없음** | 체크한 `wait` 시술 ≥ 1 — 「의사 호출 · N건」, 없으면 「시술 선택 후 의사 호출」 꺼짐 | Q1 · Q2 · Q4 · D-24 · 시안 `M:894`(「둘 다 아니면 버튼 없음」) · `M:1518-1519` · 지금 코드(CB §9 #4) (r2) |
| (스냅샷) `canCall` | — | 귀가 대기 아님 · 전부 완료 아님 · **호출할 수 있는(`pickable`) 시술이 1개 이상** — ~~(`kind = procedure`)~~ (r4) type 무관 · 「방 배정」 제외. 「방 배정」만 남은 카드는 `false` (0.3.0 · r4) | T6 · 코드 `service/board_service.py` |
| 팝오버 [<원장> 호출 / 모든 의사 호출] | 팝오버 열림 | 「모든 의사」 또는 원장 한 명을 골랐을 때(기본값 없음 → 「의사를 선택하세요」 꺼짐) | P7 |
| 카드 아래 [귀가 대기] | 귀가 대기 아님 · 시술 전부 완료 | 항상(보이면 켜짐) | D-33 · Q3 |
| [마취 시작] | 귀가 대기 아님 · 진행 중 마취 없음 | 항상 | D-23 |
| [마취 종료] | 진행 중 마취 있음 | 항상 | D-23 |
| 줄 [시작] | 귀가 대기 아님 · `wait` | §5.6 조건 | D-30 |
| 줄 [종료] | `doing` | 항상 | D-31 |
| 줄 되돌리기 아이콘(진행 줄 · [종료] 왼쪽) | 스냅샷 `canUndoStart = true`(§5.13) | 항상(보이면 켜짐) → 누르면 확인 모달 | `_RESUME 10-26` (r5) |
| 줄 되돌리기 아이콘(완료 줄 · 「완료」 왼쪽) | 스냅샷 `canUndoFinish = true`(§5.13) | 항상 → 확인 모달 | `_RESUME 10-26` (r5) |
| 토스트 [되돌리기] | 이 화면에서 [시작] · [종료]가 성공한 직후의 토스트(5초)에만 | 항상 → 모달 없이 바로 되돌리기 API | `_RESUME 10-26` · 기본값(§5.13) (r5) |
| 호출 탭 [<원장> 수락] | 전체 호출 카드 | 원장을 골랐을 때 | D-27 · 시안 #19 |
| 호출 탭 [수락] · [다른 원장에게] | 지정 호출 카드 | 항상 | D-27 |

조작 버튼은 「KOS 반영 중 · 실패」여도 막지 않는다(§4.4 대기열) — 기본값.

### 5.12 카드 순서 — 드래그 (0.4.0)

| 규칙 | 계약 | 근거 |
|---|---|---|
| 무엇 | 현황판 카드를 끌어 다른 카드 위에 놓으면 **방향 따라** 끼운다 — 지금 순서에서 끄는 카드가 대상보다 **앞**에 있었으면(아래 · 뒤로 끔) 대상 **뒤**에, **뒤**에 있었으면(위 · 앞으로 끔) 대상 **앞**에. **앞 · 뒤 판정 = 드래그를 시작할 때의 전체 순서**(놓기 전 화면 순서 — 경합 중이면 그때의 로컬 순서) 기준 — 끄는 동안 미리보기로 바뀐 순서로 다시 판정하지 않는다(같은 대상 위에서 앞 · 뒤가 번갈아 바뀌는 깜빡임 방지 · 기본값 (r3)). 그래서 바로 옆 카드와 자리 바꾸기 · 맨 끝으로 옮기기가 된다(시안 「앞에 끼우기」만으로는 안 됨 · §6.7 #21) (r2). ~~[입실순 \| 배치순] 버튼~~ 은 없다(0.4.0 바뀜) — **정렬 = 드래그 순서** | `_RESUME 10-23` 「review-doc r1 기본값 ②」(방향 따라) · 「입실순/배치순 버튼은 뺀다」 · 드래그 순서 줄 · `M:1464-1472` · DA §11 Q-11 |
| 저장 | **back DB**(`board_order` · §3.2) — ccc 만, **KOS 반영 없음**(`kos_op` 0줄) · 조작 1번 = `event_log(board_order)` 1줄 | `_RESUME 10-23` 드래그 순서 줄 · D-13 |
| 공유 | **모든 화면 공유** — 순서는 SSE 스냅샷 `cards[]` 배열 순서로 실린다(§7.2). 한 화면에서 옮기면 다른 화면(간호 스테이션 · 의국 PC)도 새로고침 없이 같은 순서 | `_RESUME 10-23` 기본값 「모든 화면 공유(SSE 스냅샷에 실음)」 |
| 단위 | **그날(KST) 하나** — `board_order.day` = 오늘 KST. 날짜가 바뀌면(KST 00:00) 새 날은 순서 없음 → 아래 「목록에 없는 카드」 규칙. 전날 행은 지우지 않아도 된다(읽지 않는다) | `_RESUME 10-23` 기본값 「그날 단위」 · §4.2 날짜 바뀜 |
| 스냅샷 정렬 | ① 귀가 대기 아닌 카드 중 **오늘 순서 목록에 있는 카드** = 목록 자리 순 → ② 목록에 **없는** 귀가 대기 아닌 카드(새 카드 등) = **맨 뒤, 그들끼리 입실순**(`room_assigned_at` 오름차순 · 같으면 visit id) → ③ **귀가 대기 카드 = 맨 뒤, 귀가 대기 시각 순**(`flow_step_at` · 지금 규칙 그대로) | `_RESUME 10-23` 기본값 「새 카드는 맨 뒤」 · `M:1425-1430` (`key = i < 0 ? 1000 + inAt : i` · home 은 뒤에 `home` 시각 순) |
| 귀가 대기 카드 | **드래그 제외** — 끌 수 없고(드래그 시작 안 함), 귀가 대기 카드 위에 놓아도 옮기지 않는다. back 도 저장 목록에서 귀가 대기 카드를 뺀다 | `_RESUME 10-23` 기본값 「귀가 대기 카드는 드래그 제외」 · `M:1471`(`ids` = `home == null` 만 · `at < 0` 이면 그만) |
| 귀가 대기가 된 카드 | 목록에 남아 있어도 ③ 으로 간다(목록 자리는 무시). 데스크 귀가(`COMPLETED`)로 사라진 카드는 목록에서 그냥 건너뛴다 | 위 두 줄의 결과 · §5.1 조건 2 |
| 저장 요청 | `PUT /api/board/order` 본문 = **귀가 대기 아닌 카드 전부의 새 순서**(필터로 숨긴 카드 포함 — 화면에 보이는 것만이 아니라 front 가 가진 전체 순서) — §7.3 | 기본값(목록 통째 바꾸기 — 아래 동시 규칙이 단순해진다) |
| 놓은 뒤 화면(경합) (r2) | front 는 놓을 때마다 요청 번호를 하나 올리고 **마지막 요청만** 본다. ① 마지막 PUT 응답이 올 때까지 **로컬 순서 유지** — 그사이 오는 스냅샷은 카드 내용만 바꾸고 순서는 로컬 것(로컬 목록에 없는 새 카드는 스냅샷 순서대로 귀가 대기 아닌 카드들 뒤에 · **로컬 목록 안의 카드가 그사이 귀가 대기가 되면 로컬 순서에서 빼고 귀가 대기 묶음(맨 뒤 · 스냅샷 순서)으로** · 사라진 카드는 뺀다 (r3)) ② 응답(성공) 뒤에는 **「같음」이 성립하는 첫 스냅샷**부터 서버 순서를 따른다 — ~~스냅샷 귀가 대기 아닌 `cards[]` 순서 = 응답 `visitIds`~~ (r3 바뀜) → 비교 = 스냅샷의 귀가 대기 아닌 `cards[]` 에서 **응답 `visitIds` 에 든 카드만 뽑은 차례**가 **응답 `visitIds` 중 그 스냅샷에서 귀가 대기 아닌 카드로 남아 있는 것**의 차례와 같으면 「같음」(그사이 생긴 새 카드 · 그사이 귀가 대기가 되거나 사라진 카드는 비교에서 빠진다) (r3) ③ 응답 뒤 **3초** 안에 그런 스냅샷이 없으면(다른 사람이 그사이 바꿈 등) 그냥 스냅샷을 따른다 ④ 마지막 PUT 실패면 오류 토스트 + 바로 스냅샷 순서. 앞선 요청의 응답 · 실패는 무시 | 기본값(review r1 W5 · r2 R2 — PUT 응답 모양은 그대로 · `version` 안 실음) |
| 목록 거르기 | back 은 받은 목록에서 **지금 카드가 아닌 id**(없는 visit · 이미 사라진 카드 · 다른 날 · 귀가 대기)를 **오류 없이 빼고** 저장한다 — 놓는 사이에 카드가 사라질 수 있어서. 형식 오류(배열 아님 · 정수 아님 · 같은 id 두 번)만 400 | 기본값 |
| 동시에 두 사람 | **마지막 쓰기가 이긴다**(오늘 행을 통째로 바꾼다 · 버전 검사 없음). 앞 사람의 순서는 다음 스냅샷에서 뒤 사람 것으로 바뀐다. 뒤 사람 목록에 없던 카드(그 사이 새로 생긴 카드)는 ② 규칙으로 맨 뒤 | 기본값(PoC 한 지점 · 같은 화면을 보는 사람 수가 적다 — §7.5 「연결 목록은 메모리」와 같은 결) |
| 역할 | 관리자 · 의사 · 간호사 모두(SPEC-004 §3.4 표에 `PUT /api/board/order` 줄 — r2) · `PROC_FAKE_BOARD` 면 403 `fake_board`(§2.3) | SPEC-004 A-08 기본값 · §3.4 · §7.3 |
| 앱 | 앱은 지금 자기 코드로 입실순 정렬(`app/lib/view/view.dart:58`)이라 **이번 판에 바뀌지 않는다**. ~~앱도 같은 순서를 따를지 → §10 OQ-523~~ (r5) → 앱도 같은 순서를 따른다 — **§10.1 앱 후속 1**(웹이 정본) | SPEC-004 §6 「순서 = 입실순」 · 코드 |

### 5.13 [시작] · [종료] 되돌리기 (r5)

원천 = `_RESUME 10-26` 「되돌리기 기능 추가」 · 「아이콘 위치」 줄 — D-28(되돌리기 없음)을 **[시작] · [종료]에 한해** 뒤집는다. 웹만(앱은 §10.1 후속).

| 규칙 | 계약 | 근거 |
|---|---|---|
| 무엇 | **[시작] 되돌리기** = 진행 시술 → **시술 대기** · **[종료] 되돌리기** = 완료 시술 → **시술 중** | `_RESUME 10-26` |
| 들어가는 곳 두 개 | ① [시작] · [종료]가 성공한 직후 토스트 오른쪽 [되돌리기] — **누르면 바로**(확인 모달 없음) ② 시술 줄 되돌리기 아이콘 — 호버 「되돌리기」 툴팁 → 누르면 **확인 모달** → [되돌리기] | `_RESUME 10-26` ① · ② |
| 토스트에 모달이 없는 이유 | 기본값 — 토스트는 방금 내가 누른 조작의 즉시 취소라 대상이 분명하고(그 줄 · 그 시술), 5초 안에 두 번 누르게 하면 시간 안에 못 누른다. 아이콘은 언제 누를지 모르는 다른 사람의 조작도 되돌리므로 모달로 한 번 묻는다 | 기본값 |
| 토스트 시간 | **5초**(기본값) — 지금 토스트 2.6초(§6.3 · 시안 `M:1369`)는 읽기용이라 누르기에 짧다. [되돌리기] 가 있는 토스트만 5초 · 다른 토스트는 2.6초 그대로. 새 토스트가 뜨면 앞 토스트(와 그 [되돌리기])는 사라진다 — 토스트 되돌리기는 **그 화면의 마지막 [시작] · [종료] 하나만** | 기본값 |
| 되돌릴 수 있는 범위 | 토스트 = 마지막 조작만(위). **아이콘 = 아무 때나** — 오늘 카드에 보이는 진행 · 완료 시술이면 누가 언제 눌렀든(다른 화면 · 앱에서 누른 것 포함). 여러 번 되돌리기 · 되돌린 뒤 다시 [시작] · [종료] 모두 된다(횟수 제한 없음) | 기본값 — 아이콘이 줄에 늘 있으므로(`_RESUME 10-26` ②) |
| `canUndoStart` (스냅샷) | 시술이 `doing`(ccc `started_at` 있음 · 완료 아님) · 「방 배정」 아님 · **귀가 대기 카드 아님** | §5.9 · §5.1 |
| `canUndoFinish` (스냅샷) | 시술이 `done` · **ccc `started_at` 있음**(ccc 에서 [시작]한 시술) · 「방 배정」 아님 · **귀가 대기 카드 아님**. KOS 에서만 완료돼 ccc [시작]이 없는 시술은 아이콘 없음 — 「시술 중」 = ccc [시작] 시각이 기준(§5.9)이라 시작 시각 없이 진행으로 돌릴 수 없다 | 기본값 · §5.9 |
| [시작] 되돌리기 뒤 | ccc `started_at` · `started_event_id` 를 비운다 → 시술 `wait`. **호출 · 수락 · 집도의는 그대로** — 수락이 있던 시술은 「<원장> 수락 · 시작 가능」, 호출 없이 담당의로 시작했던 시술은 「<원장>」으로 돌아가 [시작]이 다시 켜진다(§5.6 조건 그대로). KOS 작업 쪽 요청 없음([시작]도 작업에 KOS 요청이 없다 — §8) | §5.6 · §8 · 기본값 |
| 고객 상태(시술 대기로) | [시작] 되돌리기 뒤 그 고객의 시술(「방 배정」 제외 · §5.1 `procedures`) 중 **진행 · 완료가 하나도 없고** 고객이 `doing` 이면 → 고객 `waiting` + KOS `changeFlowStep(PROCEDURE_WAITING)`(§8). 진행 · 완료 시술이 하나라도 남으면 고객은 진행 그대로 · KOS 요청 없음. 첫 [시작]의 거울(§5.2 「그 고객의 첫 [시작]」). KOS 는 뒤로 가기를 **받는다**(WP-KOS K4 — `PROCEDURE` → `PROCEDURE_WAITING` 200 · 작업 값 그대로) (r6) | §5.2 · §5.10 · 기본값 · ~~OQ-530~~(닫힘 · 받음 (r6)) · 리포트 `orchestration/work/overall-board/kos-undo-probe-report.md` |
| [종료] 되돌리기 뒤 | ccc `completed_at` 을 비우고 `kos_status` 를 **`READY`**(즉시 값 — ~~기본값~~ (r6) **확정: 실 KOS 가 `complete:false` 뒤 `DONE` → `READY` 로 간다**(WP-KOS K2 · 완료 시각 지움 · 집도의 · 담당 · 호출 시각 그대로 · 22초 뒤에도 `READY`). 집도의 없는 작업의 값은 보지 않았다 — [시작]이 켜지려면 수락이나 담당의가 있어야 하므로 [종료]된 시술은 집도의가 있다. 확인 뒤엔 KOS 값으로 덮인다)로 → 시술 `doing`(「<원장> · HH:MM 시작」 — 옛 [시작] 시각 그대로) · [종료]가 다시 켜진다. KOS `change-tasks-complete {complete:false}`(§8). 고객 상태는 바뀌지 않는다(완료 시술이 있던 고객은 이미 진행) — 「전부 완료」가 풀리면 카드 아래 [귀가 대기]는 사라지고 스냅샷 규칙대로 [의사 호출] 또는 버튼 없음(§5.11) | §5.9 · §5.11 · ~~OQ-529~~(닫힘 · 받음 (r6)) · 리포트 `orchestration/work/overall-board/kos-undo-probe-report.md` K2 |
| 귀가 대기 카드 | **되돌리기 없음** — 아이콘 없음 · API 409 `visit_home`. 귀가 대기 카드는 다른 조작 버튼도 없고(§5.11), [귀가 대기] 때 취소한 「방 배정」(§5.7)을 되살릴 방법이 정해지지 않았다. 귀가 대기 뒤 [종료] 되돌리기(고객 귀가 대기 → 진행)는 OQ-531 | 기본값 · §5.7 |
| 마취 | 범위 밖 — 마취 시작 · 종료 되돌리기 없음 | 기본값(브리프) |
| 되돌리기 중 KOS | 조작 1번 = `event_log` 1줄 + `kos_op` 0 ~ 1줄(§8) · 응답은 KOS 를 기다리지 않는다(§4.4). 같은 visit 의 op 은 만든 순서대로 — [종료] op 뒤에 되돌리기 op 이 가므로 KOS 에도 그 순서로 닿는다. 확인 · 재전송 · 실패는 §4.4 그대로 | §4.4 |
| 동시성 | **상태로만 검사**(버전 없음): 되돌리기를 누를 때 그 시술이 이미 다른 화면에서 바뀌었으면 409 — [시작] 되돌리기인데 시술이 `doing` 이 아님 = `procedure_not_doing` · [종료] 되돌리기인데 `done` 이 아님 = `procedure_not_done` · 귀가 대기 = `visit_home`. front 는 back `message` 로 오류 토스트(§6.3)를 띄우고 화면은 다음 스냅샷대로. 상태가 같은 채로 다른 사람이 그 사이 되돌리고 다시 누른 경우(A [시작] → B 되돌리기 → C [시작] → A 토스트 [되돌리기])는 C 의 [시작]을 되돌린다 — 막지 않는다(OQ-532) | 기본값(§5.12 「마지막 쓰기가 이긴다」와 같은 결) |
| 역할 | 관리자 · 의사 · 간호사 모두 — [시작] · [종료]와 같다(SPEC-004 §3.4 표 줄) · `PROC_FAKE_BOARD` 면 403 `fake_board` | SPEC-004 §3.4 · §2.3 |
| 앱 | 이번 판 앱 무변경 — 앱은 새 스냅샷 필드(`canUndoStart` · `canUndoFinish`)를 모르고 무시한다. 앱에 되돌리기를 넣는 것은 §10.1 앱 후속 | `_RESUME 10-26` 「웹이 정본」 |
| **KOS 실호출 확인이 구현 완료 조건** | `change-tasks-complete {complete:false}` · `change-flow-step` 뒤로 가기(`PROCEDURE` → `PROCEDURE_WAITING`)는 **실 KOS 에서 본 적이 없다**(HAR 에 `complete:false` 없음 — 「될 것으로 추정」만 · 1차 HAR 조사). WORK-006 **WP-KOS** 가 구현 전에 데모 지점에 1회씩 호출해 응답 · KOS 화면 상태를 리포트로 남긴다. 안 받으면 → OQ-529 · OQ-530. **(r6) 확인됨 — 둘 다 받음**(K2 `complete:false` 200 · `DONE → READY` · K4 flow-step 뒤로 가기 200). KOS **웹 화면** 표시는 워커가 보지 못했다 → §9 #21 · #22 에서 코디 · 사용자가 본다 | `_RESUME 10-26` 「KOS 실호출 확인 필수」 · `spec-r5-addendum.md` ② |

## 6. 화면 (시안 기준)

| 화면 정본 | 값 |
|---|---|
| 확정 시안(정책 기준) | `design-user-r4/Ceramique 시술현황판 v2.dc.html`(r3 · r4 읽기 리포트) |
| **구현 반영 시안 파일 이름**(코드 main `329b543` 화면 = E2E 수정 뒤를 다시 그린 시안) | claude design `dda9a931` 「Ceramique 시술현황판 v2 (구현 v3).dc.html」 — 장면 17(login · login-error · login-locked · board … narrow) · 원본 v2(r4)는 그대로 · 대응표 `orchestration/work/myeongdong-poc-v2/design-sync-frontend-report.md`(아카이브 뒤 같은 slug 로그) (2026-10-22) |
| **전체현황판 시안(0.4.0 화면 정본)** | `reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html`(claude design `dda9a931` 같은 이름 파일 · 「구현 v3」 복사본에서 시작 — `M:17-18`) 의 **헤더 `M:63-92` · 「시술 현황」 하위 화면 `M:777-1098` · 의사 호출 팝오버 `M:1101-1153`**. 읽기 리포트 `orchestration/work/overall-board/design-analysis-report.md` §1 · §2 · §4 · §6 · §8 · §10 · §11. 위 두 시안과 다르면 이 시안이 맞다 — 단 `_RESUME 10-23` 결정이 고친 곳(§6.7)은 결정이 맞다. **public 레포 — 시안 공지 예시 · 직원 이름의 실명은 옮기지 않는다** (0.4.0) |

장면 이름은 시안 `scene` 값: `board` · `board-placement` · `memo-expanded` · `call-modal` · `call-modal-specific` · `all-done` · `panel-doctors`(= 호출 탭) · `panel-customers`.

### 6.1 경로

| 경로 | 화면 | 근거 |
|---|---|---|
| `/login` | 로그인 — **아이디 · 비밀번호 폼** · [로그인]. 헤더 없음. ~~계정 카드를 눌러 바로(비밀번호 검증 없음)~~ — 카드 · 계정 목록 없음. 웹은 관리자 계정으로 쓴다(역할 제한은 §10 OQ-518) (0.3.0) | D-05 · `_RESUME` 10-21 OQ-601 닫음 줄 · 코드 `front/app/login/page.tsx` |
| `/procedures/live` | 시술 현황판(시안 사이드바 `current-path`). 0.4.0 = 헤더 「현황 › 시술 현황」 항목이 가리키는 곳 — **경로는 그대로 둔다**(시안 데모 href `/live/proc` 는 따르지 않음 · 배포 주소 · 북마크 유지 — 기본값 · §10 OQ-524) (0.4.0) | 시안 · D-17 · `M:1215-1222` |
| `/` · `/procedures` | `/procedures/live` 로 보낸다(로그인 안 했으면 `/login`) | 기본값 |

로그인 화면 모양 = `cc/front/app/login/page.tsx` 의 틀(입력 · 버튼 스타일)만 따른다. 별도 시안 없음 — D-02 · 기본값.

### 6.2 헤더 · 사이드바 · 제목 줄

- ~~헤더 = `AppHeader` 모양. 메뉴 = **「시술 현황」 하나**(시안은 「현황판 · 시술 현황 · 예약관리」 세 칸 → D-17 이 고친다). 오른쪽 = 시계 · 지점 이름 · 계정 표시 · 로그아웃 — D-17 · 시안 헤더~~ (0.4.0 바뀜)
- ~~사이드바 = medikit `Menu`, 묶음 · 항목 모두 「시술 현황」 — 시안~~ (0.4.0 바뀜)
- ~~제목 줄 = 「시술 현황」 + 「명동점 · 마지막 KOS 동기화 HH:MM:SS」(`sync_state.schedules.last_ok_at`) · 범례 Badge sm dot 5개(시술 대기 · 마취 중 · 시술 진행 · 확인 필요 · 귀가 대기) · [입실순 | 배치순] — 시안 · D-18~~ (0.4.0 바뀜)

**헤더** (0.4.0) — `M:63-92` · DA §2 · `_RESUME 10-23` 헤더 줄

| 자리 | 계약 | 근거 |
|---|---|---|
| 틀 | 높이 57 · 흰 바탕 · 아래 1px `gray-200` · 좌우 여백 28(좁은 화면 16) · z 30. **사이드바 없음**(medikit `Menu` 를 쓰지 않는다 — 지금 코드의 사이드바를 뺀다) | `M:64-65` · DA §2 · CB §2 |
| 왼쪽 | 로고(높이 22 · 좁은 화면 18) · 간격 48 · 상단 메뉴 **「현황」 하나**(`text-typo-heading-md-500` · 지금 메뉴라 `text-primary`). 나머지 5개(고객 · 예약 · 시술 기록 · 매출 · 설정)는 **그리지 않는다** | `_RESUME 10-23` 헤더 줄 · `M:67-81` · `M:2225` |
| 호버 드롭다운 | 「현황」에 마우스를 올리면 아래로 펼침 — 최소 폭 180 · 반경 10 · 그림자 `0 8px 28px rgba(0,0,0,.12)` · 항목 높이 40. 항목 = **「시술 현황」 하나**(지금 항목이라 `text-typo-body-600 text-primary bg-primary-100`) → `/procedures/live`. 예약 현황 · 원내 현황은 아직 없어 **그리지 않는다**(코디 기본값 · §10 OQ-520). 「현황」 글자를 누르면 그 메뉴 첫 항목(= 시술 현황) | `M:70-78` · `M:2222-2227` · `_RESUME 10-23` |
| 오른쪽 | (넓은 화면만) 시계 HH:MM(tabular · `heading-sm-400 text-ms-black`) · 「세라미크 명동점」(`gray-700`) → 계정 표시(`text-primary`) → [로그아웃](누르면 세션 지우고 `/login`) | `M:83-90` · CB §2 |
| 계정 표시 | 시안 = 「{역할} · {이름}」. 역할 글자는 정한 곳이 없다 → **지금(`name`) 그대로** · §10 OQ-514 | `M:2245` · SPEC-004 §3.6 「헤더 계정 표시 = name」 |
| 하위 화면 탭 | 없음 — 시안이 `subTabs`(개수 뱃지)를 계산만 하고 그리지 않는다. 하위 화면 바꾸기 = 헤더 드롭다운뿐 | `M:2234-2236` · DA §1.2 · Q-3 |

**제목 줄** (0.4.0) — `M:781-800` · DA §4.1

- 왼쪽: 「시술 현황」(`h1` · `text-typo-title-md-600 gray-800`) · 「마지막 KOS 동기화 HH:MM:SS」(`body-400 gray-600` · `sync_state.schedules.last_ok_at`) — ~~「명동점 · 」 앞머리~~ (0.4.0 바뀜 — 시안에 없음) · 「조회 시간 밖」(`caption-md-500 gray-500` · `!sync.inWindow`) · 「동기화 실패」(`caption-md-600 text-red` · title 「KOS 조회 오류」 · `sync.lastError`) — `M:784-791`
- 오른쪽: 범례 Badge sm dot 5개(시술 대기 warning · 마취 중 purple · 시술 진행 primary · 확인 필요 danger · 귀가 대기 neutral) — `M:794-798` · `M:2262-2265`
- **[입실순 | 배치순] 없음**(0.4.0 바뀜) — 정렬 = 드래그 순서(§5.12) — `_RESUME 10-23` · 시안 template 에 버튼 없음(`sortIn` · `sortRoom` 계산만 · `M:2266`)

- 조회 시간 밖이면 동기화 문구 옆 「조회 시간 밖」, 조회 실패면 「동기화 실패」 — 기본값(§4.2)

### 6.3 가운데 — 오더지 카드 (D-17 ~ D-19 · 장면 `board` · `board-placement` · `memo-expanded` · `all-done`)

- 격자 `minmax(300px,1fr)` · 간격 8 · 한 줄 높이 같음 · 카드 흰 바탕 · 확인 필요만 빨간 테두리 — P1 · r3 #2 · #3
- **카드 높이**: 최소 높이 = **가운데 판 보이는 높이의 절반쯤**(판 안에 두 줄 — CSS 비율 계산 · `100cqh` 기준) · 내용이 길면 늘어난다 · **카드 안 스크롤 없음**(내용 다 · 오더 메모는 `MemoCard` 접기) · 아래 큰 버튼은 카드 바닥. **px 상수 금지** (0.3.0) — E2E-5 → E2E-12 · 코드 `front/app/(main)/procedures/live/page.tsx`
- ~~정렬: **입실순** = `room_assigned_at` 오름차순 · **배치순** = `room.order` 오름차순. 귀가 대기 카드는 그 뒤에(귀가 대기 시각 순) — D-18 · D-33 · 시안 `ordered`~~ (0.4.0 바뀜)
- **정렬 = 스냅샷 `cards[]` 순서 그대로**(back 이 §5.12 로 정렬 — 드래그 순서 → 순서 없는 카드는 입실순 → 귀가 대기 맨 뒤 귀가 대기 시각 순). front 는 다시 정렬하지 않는다(지금 `view.ts` `orderedCards` 의 입실순 · 배치순 정렬을 뺀다) (0.4.0) — `_RESUME 10-23` · `M:1425-1430`
- **드래그**(0.4.0) — `M:808` · `M:1464-1472` · `M:2251` · DA §6 시술 줄
  - 귀가 대기 아닌 카드 = 끌 수 있음(`cursor: grab` · HTML5 drag) · 귀가 대기 카드 = 끌 수 없음 · 그 위에 놓아도 안 옮김(§5.12)
  - 끄는 카드 = 불투명도 **0.35** + 테두리 밖 primary 2px 그림자(`box-shadow: 0 0 0 2px var(--ms-primary)`)
  - 끄는 동안 다른 카드 위에 올리면 **그 자리로 미리 옮겨 그린다**(놓기 전 미리보기 — ~~끄는 카드를 그 카드 앞에 끼움~~ (r2 바뀜) → 놓을 때와 같은 **방향 따라** 끼움 · §5.12) · 놓으면 확정 · 끌기를 그만두면(드래그 끝 · 판 밖에 놓음) 원래 순서
  - 놓으면 화면은 **바로 새 순서**(front 가 잠시 들고 있음) → `PUT /api/board/order`(§7.3 · 귀가 대기 아닌 카드 전체 순서) → 뒤따르는 `board` 스냅샷으로 바꾼다(경합 규칙 = §5.12 「놓은 뒤 화면」 (r2)). 실패(4xx · 5xx · 네트워크 — **가짜 보드의 403 `fake_board` 도 같다**, 예외 없음 (r2))면 오류 토스트(back `message`) + 스냅샷 순서로 돌아간다 — 기본값(§6.6 「조작 응답은 `{ok}` · 화면은 SSE」와 같은 길)
  - 필터 · 검색 강조 중에도 끌 수 있다 — 숨긴 카드 자리는 그대로 두고 보이는 카드끼리 자리를 바꾼다(방향 따라 끼우기 · 전체 목록 기준 — 앞 · 뒤는 전체 목록 순서로 판단 (r2)) — 시안 `M:1471`(`ordered()` 전체 목록에서 `ids.splice`)
  - 터치 드래그(태블릿)는 시안에 없다 — 범위 밖(웹 마우스만) — 기본값
- 카드 안 순서(D-19):
  1. ~~머리 — 방 이름(`title-lg-600`) · 「입실 HH:MM」 / 상태 Badge + 오른쪽 경과 글자 / 고객 줄(이름 한 줄 줄임 · 국적 칩 · 「첫내원/재내원」) + **「수납 필요」**(§6.7)~~ (0.4.0 바뀜)
     → 머리 **한 줄** = 왼쪽 방 이름(`title-lg-600 gray-800`) + 상태 Badge(sm dot · §5.2 덮어쓰기 그대로) / 오른쪽 「입실 HH:MM」(`caption-md-400 gray-600`). **경과 글자(「호출 N분 경과」 · 「완료 뒤 N분 경과」 · 「귀가 대기 HH:MM」) 줄 없음 · KOS 반영 줄 없음**. 그 아래 고객 줄(점 7px · 이름 `caption-md-600` 한 줄 줄임 · 국적 칩 `bg-ms-gray-200 caption-md-500 gray-700` · 「첫내원/재내원」 · **「수납 필요」** Badge warning sm) (0.4.0) — `M:810-828` · 시안 `hasLabel` · `hasKos` 는 계산만(`M:1479-1482`) · §6.7 #11 · #12
  2. 오더 메모 — `MemoCard` 3줄 · 120자 넘으면 접기 [펼치기 · 접기] — P19 · `memo-expanded`
  3. 마취 줄 — §5.3 · [마취 시작/종료] 26px(`data-compact-buttons`)
  4. 선택 줄 — 체크칸(일부면 「–」) · 「전체 선택 / N개 선택됨 / 호출할 대기 시술 없음」. 고르면 `bg-primary-100 border-primary` — r4 #1
  5. 시술 줄 — 줄마다 테두리 상자 · 체크칸 20 · 이름 · 둘째 줄(§5.9) · 오른쪽 버튼(§5.11) — r3 #9 ~ #11. ~~`kind = etc` 작업은 지금 코드에서 **시술 줄 맨 위**에 제목 + KOS 상태 글자만(체크 · 버튼 · 배지 없음) — E2E-4. 빼는 것은 OQ-517 (0.3.0)~~ (0.4.0 바뀜)
     → ~~줄 순서 = 진행 → 대기 → 완료 · 완료 묶음 앞 점선(§5.9). **「방 배정」 줄은 없다**(스냅샷에 없음 · §5.1). **방 없는 기타 작업(`kind = etc` — 마취 · 시트팩 · 관리 마무리 등)은 지금처럼 시술 줄 맨 위에 읽기 전용 한 줄**(제목 `body-500 gray-600` + KOS 상태 글자 `caption-md-400 gray-500` — 대기중 · 준비중 · 호출함 · 진행중 · 완료 · 취소 · 체크 · 버튼 · 배지 없음) — 시안에는 이 줄이 없지만 사용자 결정이 이긴다(§6.7 #13) (0.4.0) — `_RESUME 10-23` 「방 배정」 줄 · E2E-4 · CB §4 5a · `M:1232` `KOS_STATUS`~~ (r4 바뀜)
     → 줄 순서 = 진행 → 대기 → 완료 · 완료 묶음 앞 점선(§5.9). **type 무관 모든 작업이 같은 시술 줄**(체크 · [시작]/[종료] · 「호출함」 · 담당 글자 — 시안 시술 줄과 같은 모양 · 읽기 전용 줄 없음). **`isRoomTask` 인 줄(「방 배정」)만 그리지 않는다** — 선택 대상 · 「N개 선택됨」 · [의사 호출 · N건] 개수 · 호출 팝오버 목록에서도 빠진다 (r4) — `_RESUME 10-25` 「규칙 하나」 줄 · 코드 `OrderCard.tsx` · `view.ts` `procsOf` · `CallPopover.tsx` · `live/page.tsx`
     → **되돌리기 아이콘**(r5 — §5.13 · `_RESUME 10-26` 아이콘 위치 줄): 시술 줄 오른쪽 버튼/배지의 **바로 왼쪽** — 진행 줄 = [종료] 왼쪽(`canUndoStart`) · 완료 줄 = 「완료」 Badge 왼쪽(`canUndoFinish`) · 대기 줄 = 없음(되돌릴 것이 없다). 모양(기본값): 아이콘 버튼 26 × 26(줄 버튼 `data-compact-buttons` 26px 높이와 맞춤) · 테두리 없음 · 아이콘 = medikit **`ResetIcon`** `size="sm"`(16px · `MK` — 되돌리기 화살표 모양이 아니면 FE 가 인라인 SVG 되돌리기 화살표로 바꾸고 보고서에 적는다) · 색 `gray-500` → 호버 `text-primary`. **호버 = medikit `Tooltip` · `TooltipTrigger` · `TooltipContent` 「되돌리기」**(`TooltipProvider` 는 페이지에 하나 · `MK`). `aria-label` 「되돌리기」
     → **누르면 확인 모달** = medikit **`ConfirmModal`**(`MK` — `Modal` 위의 확인용 · 좌 · 우 버튼) — `title` 「시술 대기로 되돌리겠습니까?」([시작] 되돌리기) / 「시술 중으로 되돌리겠습니까?」([종료] 되돌리기) · `description` 「<방> · <시술 이름>」(기본값) · `variant` = **`caution`**(기본값 — 상태를 되돌리는 조작이라 주의 · 지우는 조작이 아니라 빨간 `warning` 은 아님) · `leftButton` = 「취소」(닫기만) · `rightButton` = 「되돌리기」(API → 닫기). 바깥 누르면 닫힘(= 취소). API 실패면 모달을 닫고 오류 토스트 (r5)
  6. 카드 아래 큰 버튼 하나(md · 꽉 찬 폭 · `data-fill-buttons`) — [의사 호출 · N건] 또는 [귀가 대기] — Q1 · Q2 · `all-done`
- ~~「KOS 반영 중」 / 「KOS 반영 실패」 — 카드 머리 오른쪽 경과 글자 자리 아래 작은 글자(실패 = `text-red`) — D-09 · 자리는 기본값(시안에 없음 · §6.7)~~ (0.4.0 바뀜)
- **카드에 「KOS 반영 중 · 실패」를 그리지 않는다**(시안대로). 조작 API 실패는 지금 코드의 오류 토스트(back `message`)로만. 스냅샷 `cards[].kos` 필드는 그대로 둔다(앱이 씀 — SPEC-004 §6) · 웹만 안 그린다. **조작 응답 뒤 비동기로 난 KOS 반영 실패(3회 재전송 뒤 `failed`)는 웹 화면에 나타나는 곳이 없다** → §10 OQ-522 (0.4.0) — `_RESUME 10-23` 「KOS 반영 중/실패 표시도 시안대로 뺀다」 · 시안 `hasKos` 계산만(`M:1482`) · CB §5 「조작 호출」
- 카드 불투명도(0.4.0 — 시안 `M:1475`): 끄는 중 **0.35** → 귀가 대기 0.55 → 다른 카드를 골랐을 때(검색 · 필터 강조) 나머지 0.45 → 그 밖 1. 확인 필요 = `border-red` · 그 밖 `border-ms-gray-300` · 고른 카드 = outline 2px primary(지금 그대로)
- 빈 상태: 카드 0 = 「시술 대기 중인 고객 없음」 · 필터 결과 0 = 「조건에 맞는 고객 없음」(지금 그대로) — `M:907-909` · `M:2267`
- 토스트: 「A-룸1 3개 시술 · 전체 호출」 · 「… · 최 원장 호출」 · 「방 · 마취 시작/종료」 · 「방 · 이름 · 귀가 대기」 등 시안 문구. ~~**되돌리기 없음**~~ (r5 바뀜) → 호출 · 수락 · 마취 · 귀가 대기 토스트는 되돌리기 없음 그대로 — r3 #25 · D-28
- **[시작] · [종료] 토스트**(r5 — §5.13): 지금은 [시작] · [종료] 성공에 토스트가 없다(코드 `live/page.tsx` `onStart` · `onFinish` 는 문구 없음 — 실패 토스트만) → 성공하면 「<방> · <시술 이름> 시작」 / 「<방> · <시술 이름> 종료」(기본값 문구) + 오른쪽 글자 버튼 **[되돌리기]**(지금 토스트 틀 · 글자와 간격 16 · `text-typo-body-600` · 진한 토스트 바탕에서 읽히는 밝은 primary 계열 — 토큰은 FE 가 테마에서 고르고 보고서에 적는다 · 기본값) · **5초**. [되돌리기] 를 누르면 토스트를 닫고 바로 되돌리기 API(모달 없음) → 성공 「<방> · <시술 이름> 시술 대기로 되돌림」 / 「… 시술 중으로 되돌림」(2.6초 · [되돌리기] 없음) · 실패(409 등) = back `message` 오류 토스트

### 6.4 오른쪽 패널 (폭 340 · 검색 + 탭 현황 · 호출 · 고객 — P17)

- 검색 — 이름 · 읽기 · 차트번호로 카드 고객 찾기(시안 `hitVals` · `M:1611`) · ~~결과 누르면 그 카드 강조~~ (r2 바뀜) → 결과 누르면 **검색어를 지우고 고객 탭으로 옮겨 그 카드 강조**(필터 = 전체) — 시안 `M:1613` · DA §4.3 E · 지금 코드(CB §9 #8 · #9)와 같음 (r2)
- **현황** 탭 — ~~상태 수 6칸 한 줄(전체 · 확인 · 대기 · 마취 · 호출 · 진행) = 카드 필터(고른 칸 파랑 2px)~~ (0.4.0 바뀜) → 상태 수 6칸 **3칸 × 2줄**(전체 · 확인 · 대기 / 마취 · 호출 · 진행) = 카드 필터. 칸 = 점 6px(전체 `bg-ms-gray-300` · 확인 `bg-red` · 대기 `bg-yellow` · 마취 `bg-purple` · 호출 `bg-primary-500` · 진행 `bg-primary`) · 이름 · 수. 칸 바탕색 · 테두리 상자 없음 — 줄의 2 · 3번째 칸만 왼쪽 1px `gray-300` 구분선. 고른 칸 = `body-600 gray-800` · 나머지 `body-400 gray-500`(지금의 칸 바탕색 · outline 2px 를 뺀다) (0.4.0) — `M:945-955` · `M:1536-1541` · DA §4.3-B. 겹쳐 센다 · 「전체」는 귀가 대기 포함 — D-20 · P12 · r3 §4-2
  - 칸 정의: 확인 = §5.8 대상 · 대기 = `waiting` · 마취 = 진행 중 마취 있음(귀가 대기 제외) · 호출 = 받을 시술이 남은 호출 있음(귀가 대기 제외) · 진행 = `doing` — 시안 `filterFn`
  - 아래 「확인이 필요한 고객」 목록(§5.8) · 빈 문구 「확인이 필요한 고객 없음」 — P13
- **호출** 탭(의국 화면 · `panel-doctors`) — 「수락 대기 N건」 + 호출 카드(호출 오래된 순): 「전체 호출 / 지정 호출」 Badge · 방 · 「호출 N분」(5분 이상 빨강 · 카드 빨간 테두리) · 「기준 5분 / 기준 도달 / +N분 초과」 · 이름 · 국적 · 받을 시술 목록
  - 전체 호출 → 「담당의 선택」 원장 목록(비어 있는 원장 먼저 · 「<방> 시술 중」/「비어있음」) → [<원장> 수락]
  - 지정 호출 → 「지정 <원장> · 상태」 + [다른 원장에게] · [수락]
  - 아래 「최근 수락」 3건 — **[되돌리기] 없음** — D-27 · D-28 · r3 #19
  - 호출 카드 = 고객 1명이 아니라 **호출 1건**(받을 시술이 남은 호출) — D-25 · D-27(시안은 고객 단위로 묶어 보임 → §6.7)
- **고객** 탭(`panel-customers`) — 고객 줄(상태 Badge · 이름 · 방 / 번호 원 시술 줄 — type 무관 · 「방 배정」(`isRoomTask`) 제외 (r4)) · **줄 순서 = 카드판과 같은 카드 순서**(스냅샷 `cards[]` 순서 · 경합 중이면 로컬 순서 — §5.12 · 지금 코드의 `orderedCards(board.cards, sort)` 정렬은 뺀다) (r3) — 시안 `M:1591`(`customerVals` = `this.ordered()`) · 귀가 대기까지 · 누르면 그 카드만 남기고 흐림 — 시안 r3 §3 「그대로」
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
| 3 | 「최근 수락」 · 토스트 [되돌리기] | ~~없음~~ (r5 바뀜) → 「최근 수락」 · 호출 · 수락 토스트 = **없음 그대로**. **[시작] · [종료] 토스트에만 [되돌리기]**(§5.13 · §6.3) | D-28 · `_RESUME 10-26` |
| 4 | 시술 줄 「호출함」 Badge 를 누르면 데모 수락 | 누르지 못함(수락은 호출 탭에서만) | D-27 |
| 5 | ~~헤더 메뉴 세 칸~~ → (0.4.0) 전체현황판 시안: 상단 메뉴 6개(현황 · 고객 · 예약 · 시술 기록 · 매출 · 설정) · 「현황」 드롭다운 3항목(예약 현황 · 원내 현황 · 시술 현황) | ~~「시술 현황」 하나~~ (0.4.0 바뀜) → 상단 메뉴 **「현황」 하나** · 드롭다운 **「시술 현황」 하나**(§6.2) | D-17 · `_RESUME 10-23` 헤더 줄 · 드롭다운은 코디 기본값(OQ-520) |
| 6 | 카드 위 주석 「시술 [시작] · [종료]는 태블릿 · 폰 몫(여기 없음)」 | 현황판 카드에 [시작] · [종료] 있음(시안 그림이 맞고 주석이 낡음) | D-29 · P3 |
| 7 | 「수납 필요」 표시 없음(시안 데이터에 결제 없음) — (0.4.0) 전체현황판 시안에는 **있다**(고객 줄 끝 Badge warning sm · `M:825-827`) → 차이 아님 | 고객 줄 끝에 작은 칩 「수납 필요」(Badge `warning` sm) — ~~자리 · 모양은 기본값~~ (0.4.0) 시안과 같음 | D-21 · ~~OQ-508~~(닫힘) |
| 8 | 「KOS 반영 중 · 실패」 표시 없음 | ~~§6.3 의 작은 글자 — 자리는 기본값~~ (0.4.0 바뀜) → **시안대로 없음**. 조작 실패는 오류 토스트만 · 비동기 KOS 실패의 웹 표시는 OQ-522 | ~~D-09 · OQ-508~~ → `_RESUME 10-23` 「KOS 반영 중/실패 표시도 시안대로 뺀다」 |
| 9 | 원장 · 고객 · 방 = 가짜 4명 · seed 6명 | KOS 데모 지점 실데이터 | D-06 · D-11 |
| 10 | 같은 칸을 다시 눌러도 필터가 안 풀림(주석은 「다시 누르면 해제」) | 시안 동작대로 — 「전체」 또는 탭 이동으로 풀림 | 시안 r3 #14 · 전체현황판 `M:1540`(같음) |
| 11 | (0.4.0) 카드 머리 경과 글자(「호출 N분 경과」 · 「완료 뒤 N분 경과」 · 「귀가 대기 HH:MM」)를 계산만 하고 그리지 않음(`hasLabel` · `M:1479`) | **시안대로 그리지 않는다** — 확인 필요 경과는 오른쪽 현황 탭 · 호출 탭에 남고, 귀가 대기는 Badge · 흐림 · 맨 뒤로 보인다. 되살릴지는 §10 OQ-521 | `_RESUME 10-23` 「시안과 코드가 다른데 … 시안대로」 · CB §4 1b |
| 12 | (0.4.0) 시안 주석은 머리에 「KOS 반영 중 · 실패」 · 기타 작업 줄을 그린다고 적었지만 template 은 그리지 않는다(`M:809` · `M:859` vs `M:1479-1499`) | 「KOS 반영」 = template 대로 없음(#8) · 기타 작업 = #13 | DA §10 「template이 쓰지 않는 계산값」 · Q-10 |
| 13 | (0.4.0) 기타 작업(`etc`) 줄 없음(`etcs` 계산만 · `M:1499`) | ~~**「방 배정」(방 있는 ETCETERA)만 뺀다** · 방 없는 기타 작업(마취 · 시트팩 · 관리 마무리 등)은 **지금처럼 맨 위 읽기 전용 줄로 남긴다**(§5.1 · §6.3)~~ (r4 바뀜) → 기타 작업은 **일반 시술 줄**(시안 시술 줄 모양 그대로 — 따로 줄 없음 = 시안과 같은 결) · 「방 배정」만 안 그림 | ~~`_RESUME 10-23` 「방 배정」 줄(사용자 결정이 시안을 이긴다) · OQ-517 닫음~~ → `_RESUME 10-25` 「규칙 하나」 줄 (r4) |
| 14 | (0.4.0) 사이드바 없음 · 제목 줄 「명동점 · 」 앞머리 없음 · [입실순 \| 배치순] 버튼 없음(주석 `M:781` 엔 있음) | 셋 다 시안대로 없앤다 | `_RESUME 10-23` 헤더 · 버튼 줄 · `M:64` · `M:785` · DA Q-11 |
| 15 | (0.4.0) 시술 줄 순서 진행 → 대기 → 완료 · 완료 앞 점선(주석 `M:859` 은 「완료 → 진행 → 대기」) | **template · 로직대로**(진행 → 대기 → 완료 · 점선) — 주석이 낡았다 | `M:1500-1503` · §5.9 |
| 16 | (0.4.0) 현황 탭 6칸 = 3 × 2 · 점 · 칸 바탕 없음(지금 코드 = 한 줄 6칸 · 칸 바탕색 · outline) | 시안대로(§6.4) | `M:945-955` · CB §3.2 |
| 17 | (0.4.0) 헤더 계정 표시 「{역할} · {이름}」(역할 = 데모 prop) | 지금(`name`) 그대로 — 역할 글자를 정한 곳이 없다 · OQ-514 | `M:2245` · SPEC-004 §3.6 |
| 18 | (0.4.0) 메뉴 href `/live/proc`(데모) | 경로 `/procedures/live` 그대로 · OQ-524 | `M:1215-1222` · §6.1 |
| 19 | (0.4.0) 드래그 순서 = 화면 메모리(`procOrder` · 새로고침 · 다른 화면과 공유 정의 없음) | back DB 저장 · 모든 화면 공유 · 그날 단위(§5.12) | `_RESUME 10-23` 드래그 순서 줄 · DA Q-12 |
| 20 | (0.4.0) 귀가 대기 카드도 `draggable="true"`(놓기만 막힘 · `M:1471`) | 귀가 대기 카드는 **끌기부터 막는다**(§5.12) | `_RESUME 10-23` 기본값 「귀가 대기 카드는 드래그 제외」 |
| 21 | (r2) 놓기 = 「대상 앞에 끼우기」만(`M:1471-1472` `splice(at, 0, from)` · 미리보기 `M:2251` 같음) — 바로 아래 카드 위에 놓으면 안 움직이고 맨 끝 자리로 못 감 | **방향 따라** — 아래로 끌면 대상 뒤 · 위로 끌면 대상 앞(§5.12) | `_RESUME 10-23` 「review-doc r1 기본값 ②」 · review r1 W6 |
| 22 | (r2) 카드 아래 [의사 호출] — 시안 = `canCall` 일 때만(「둘 다 아니면 버튼 없음」 `M:894`) · 0.3.0 SPEC 은 「전부 완료 아님」이면 꺼진 채 보임 | **시안대로**(§5.11 고침 · 지금 코드와 같음) | `_RESUME 10-23` 「시안과 코드가 다른데 … 시안대로」 · review r1 W9 |
| 23 | (r5) 전체현황판 시안 = 토스트 「되돌리기 없음(D-28)」(`M:1089`) · 시술 줄 되돌리기 아이콘 · 확인 모달 없음 | **결정대로 더한다** — [시작] · [종료] 토스트 [되돌리기] · 진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 왼쪽 아이콘 · medikit `ConfirmModal`(§5.13 · §6.3). 시안 그림은 없다 — 모양은 위 기본값 | `_RESUME 10-26` 두 줄(결정이 시안을 이긴다 — 머리말) |

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
                   pickable, canStart, canFinish,
                   canUndoStart, canUndoFinish,  // 되돌리기 아이콘(§5.13) — back 이 계산 (r5)
                   isRoomTask }],                // 「방 배정」(§5.1) — front 는 그리지 않는다 · 판정에서 빠짐 (r4)
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
- ~~`kind = etc` 작업은 `state` = KOS `DONE` 이면 `done` · 아니면 `wait`(ccc [시작]이 없으므로) · `pickable` · `canStart` · `canFinish` 는 늘 `false` · 화면 글자는 `kosStatus` — 코드 `domain/rules.py` `proc_state` · `schemas/board.py` (0.3.0)~~ (r4 바뀜)
- `kind` 는 KOS type 표시만 — **규칙은 type 무관**(§5.1). `state` = KOS `DONE` 이면 `done` · ccc `started_at` 이면 `doing` · 아니면 `wait`(ETCETERA 도 같음). 「방 배정」(`isRoomTask = true`)은 `pickable` · `canStart` · `canFinish` 늘 `false` (r4) — 코드 `service/board_service.py` `_proc` · `schemas/board.py`
- ~~**`procedures[]` 에 「방 배정」(방 있는 `etc`) 작업은 싣지 않는다** — §5.1. 남는 `etc` 는 방 없는 기타 작업뿐. 필드 모양은 그대로(`kind` 값 두 개 유지) (0.4.0) — `_RESUME 10-23`~~ (r4 바뀜)
- **`procedures[]` = KOS 작업 전부**(CANCELED 만 뺌 · 「방 배정」 포함) · 작업마다 **`isRoomTask: bool`**(새 필드 · 그 밖 모양 그대로 · `kind` 유지) (r4) — `_RESUME 10-25` · 코드 `schemas/board.py` `Procedure.isRoomTask`
- **`cards[]` 배열 순서 = 화면 순서**(§5.12 — 드래그 순서 → 순서 없는 카드 입실순 → 귀가 대기 맨 뒤). 순서 전용 필드(`order` 등)는 **두지 않는다**. 근거: ① front 는 받은 스냅샷을 통째로 바꾸기만 한다(§7.5) — 배열 순서면 front 에 정렬 로직이 없다 ② 새 카드 · 귀가 대기 · 날짜 규칙이 back 한 곳에 남는다(이 절 「규칙 계산은 back」) ③ 필드를 더하지 않아 앱 모델(`app/lib/model/board.dart`)이 바뀌지 않는다 — 앱은 자기 입실순 정렬을 그대로 쓴다(§5.12 「앱」) (0.4.0) — 기본값
- `cards[].kos` 는 그대로 싣는다(앱이 그린다 · 웹은 안 그림 — §6.3) (0.4.0)
- **`procedures[].canUndoStart` · `canUndoFinish: bool`**(새 필드 · 그 밖 모양 그대로) — 조건은 §5.13 표. 「방 배정」 · 귀가 대기 카드는 늘 `false`. front 는 이 값으로만 아이콘을 그린다(다시 계산하지 않는다 — 이 절 「규칙 계산은 back」). 앱은 모르는 필드를 무시한다(SPEC-004 §7.2) (r5)
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
| **`POST /api/procedures/{procedureId}/undo-start`** (r5) | — | `{ok:true, flowStepChanged}`(고객을 시술 대기로 돌렸나 · §5.13) | `visit_home` · `procedure_not_doing` | `_RESUME 10-26` · §5.13 |
| **`POST /api/procedures/{procedureId}/undo-finish`** (r5) | — | `{ok:true}` | `visit_home` · `procedure_not_done` · `procedure_not_started`(ccc [시작] 없이 KOS 에서만 완료된 시술) | `_RESUME 10-26` · §5.13 |
| **`PUT /api/board/order`** (0.4.0) | `{visitIds:[int, …]}` — 귀가 대기 아닌 카드의 새 순서(앞이 먼저 · 빈 배열 = 오늘 순서 지움 → 전부 입실순). 그 밖 필드 = 400 | `{ok:true, visitIds:[…]}`(거르기 뒤 저장된 목록) | 없음 — 지금 카드가 아닌 id 는 오류 없이 뺀다(§5.12) | `_RESUME 10-23` 드래그 순서 줄 · §5.12 |

- 없는 id = 404 `not_found` · 형식 오류 = 400 `invalid_request`(cc 와 같은 형식). ~~`etc` 작업 id 로 [시작] · [종료] = 404~~ (r4 바뀜) → **「방 배정」 작업 id** 로 [시작] · [종료] · 호출 = 404(ETCETERA 라도 「방 배정」이 아니면 일반 시술과 같다) (0.3.0 · r4 — 코드 `service/actions.py` `_procedure`)
- `PROC_FAKE_BOARD` 가 켜져 있으면 조작 API 전부 403 `fake_board`(§2.3) (0.2.0) — S7
- 되돌리기 두 API (r5): 경로를 **둘로 나눈다**(하나로 묶고 본문에 종류를 싣지 않는다) — 근거: ① [시작] · [종료]가 이미 경로 둘이라 짝이 맞다 ② 409 코드 · 응답 모양(`flowStepChanged`)이 다르다 ③ 본문 없는 POST 라 형식 오류(400)가 생기지 않는다. 기본값. 409 메시지(기본값): `procedure_not_doing` 「진행 중인 시술이 아니에요」 · `procedure_not_done` 「완료된 시술이 아니에요」 · `procedure_not_started` · `visit_home` 은 지금 문구 그대로. 「방 배정」 작업 id · 없는 id · 카드 아닌 visit = 404(§7.3 위 줄 · [시작] · [종료]와 같은 `_procedure` 검사). 검사 순서 = 401 → 403 `fake_board` → 404 → 409(`visit_home` 먼저 → 시술 상태). 성공하면 `event_log`(`proc_undo_start` · `proc_undo_finish`) 1줄 · `kos_op` 0 ~ 1줄(§8) → SSE `board` 발행(§7.5 ①) — §5.13 · SPEC-004 §3.4
- 역할 403(`role_forbidden` · `doctor_forbidden` · `not_your_call`)과 검사 순서는 SPEC-004 §3.4 (0.3.0)
- 조작마다 `event_log` 1줄(`actor` = 로그인 아이디) — D-13
- `PUT /api/board/order` (0.4.0): `visitIds` = **엄격한 정수 배열(StrictInt — 문자열 `"3"` · 실수 `3.0` · 불리언 `true` 도 400)** (r2). 400 `invalid_request` = 본문이 객체가 아님 · `visitIds` 없음 · 그 밖 필드 · 배열 아님 · 정수 아닌 값 · **같은 id 두 번**. 역할 = admin · doctor · nurse 모두(SPEC-004 0.3.1 §3.4 표 줄) (r2 · r3). 404 없음(없는 visit id 도 거르기만). 성공하면 `board_order` 오늘 행을 **통째로 바꾸고**(마지막 쓰기가 이긴다) `event_log(board_order)` 1줄 · `kos_op` 0줄 → SSE `board` 발행(§7.5 ①). `fake_board` 403 · 인증 401 은 다른 조작과 같다 (r3 — 역할 겹친 말 지움) — §5.12 · SPEC-004 §3.4

### 7.4 기타

- `GET /api/health` → `{ok, kos: { open, internal }}`(토큰 보유 여부만 · 값 없음)
- 데모 · 시드 · 리셋 API 없음 — D-01(시드 없음). 데모 고객 준비는 레포 밖 운영 도구(WORK-003 「운영 도구」)가 KOS 에 직접 한다 (0.3.0)
- 그 밖 back API — `WS /api/interpret`(SPEC-004 §4) · `POST /api/devices` · `DELETE /api/devices/{token}`(SPEC-004 §5-1.1) (0.3.0)
- ~~**back 경로 전부(코드 기준 16개 — router 15 + `GET /api/health`)** = §7.1 2 · §7.2 `GET /api/board` · §7.5 `GET /api/board/stream` · §7.3 조작 8 · `GET /api/health` · 통역 WS 1 · 기기 2.~~ (0.4.0 바뀜) → ~~**back 경로 전부 17개(router 16 + `GET /api/health`)** = §7.1 2 · §7.2 `GET /api/board` · §7.5 `GET /api/board/stream` · §7.3 조작 8 + **순서 1(`PUT /api/board/order`)** · `GET /api/health` · 통역 WS 1 · 기기 2.~~ (r5 바뀜) → **back 경로 전부 19개(router 18 + `GET /api/health`)** = §7.1 2 · §7.2 `GET /api/board` · §7.5 `GET /api/board/stream` · §7.3 조작 8 + 순서 1 + **되돌리기 2(`undo-start` · `undo-finish`)** · `GET /api/health` · 통역 WS 1 · 기기 2. `GET /api/auth/accounts` 는 **없다**(0.3.0 에서 제거 — SPEC-004 §3.3) (0.3.0 · 0.4.0 · r5)

### 7.5 실시간 갱신 — SSE (코디 지시 · 사용자 2026-10-21)

| 항목 | 계약 | 이유 |
|---|---|---|
| 경로 | `GET /api/board/stream` · `Content-Type: text/event-stream` | — |
| 인증 | `?token=<ccc 토큰>`(브라우저 `EventSource` 는 헤더를 못 싣는다). 틀리면 401 후 닫음 → front 는 `/login`. **접근 로그에 쿼리 문자열을 남기지 않는다** — uvicorn 접근 로그에서 쿼리를 지우는 필터(또는 `/api/board/stream` 접근 로그 끔). 배포 때 ingress 로그도 같은 기준 (0.2.0) | `EventSource` 제약 · S9 |
| 이벤트 종류 | **`board` 하나** | 화면이 하나 · 상태도 하나 |
| 본문 | **전체 스냅샷** — `GET /api/board`(§7.2)와 **같은 모양 그대로**(+ `version`: 보낼 때마다 1 씩 느는 정수) | 단순한 쪽: ① 한 지점 · 한 구역 · 오늘 일정이라 크기가 작다(HAR 하루 15건 ≈ 32KB, 저장 필드는 그보다 적다) ② front 는 받으면 **통째로 바꾸기만** — 바뀐 것만 보내면 합치기 · 순서 · 빠진 이벤트 복구 로직이 front 에 생긴다 ③ 규칙 계산(`canStart` 등)이 back 한 곳에 남는다(§7.2) |
| 보내는 때 | ① ccc 조작(마취 · 호출 · 다른 원장에게 · 수락 · 시작 · 종료 · 귀가 대기 · **카드 순서(0.4.0)** · **[시작] · [종료] 되돌리기(r5)**)이 DB 에 들어간 직후 ② KOS 일정 조회(10초)가 끝날 때마다 — 값이 바뀌었거나 `sync`(마지막 동기화 시각 · 오류)가 바뀌었으면 ③ 직원 · 방 조회(1시간) 뒤 ④ `kos_op` 상태가 바뀔 때(반영 중 → 확인 · 실패) ⑤ **조회 시간과 상관없이 10초마다**(시간 경과로 바뀌는 「확인이 필요」 · 마취 `long` · 날짜 바뀜 반영) (0.2.0) | 화면의 값은 이 다섯 중 하나로만 바뀐다 · S5 |
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
| [시작] 되돌리기 — 고객이 시술 대기로 돌아갈 때만(§5.13) (r5) | 1 | 공개 `schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"PROCEDURE_WAITING"}` — ~~이미 KOS 가 그 단계면 보내지 않고 `confirmed`(같은 단계 규칙)~~ (r6 바뀜) → ccc 고객 상태가 `doing` → `waiting` 이 될 때 **항상** 만든다. 그 사이 KOS 가 이미 그 단계라 400 이 오면 아래 같은 단계 규칙(다음 조회에서 `confirmed`) · 앞 `PROCEDURE` op 은 `superseded`(`flowStep` 키 — §4.4 · 코드 `kos/ops.py` `superseded`)로 이미 닫힌다 | 일정 `flowStep = PROCEDURE_WAITING` | `_RESUME 10-26` · ~~미확인~~ **WP-KOS K4 받음(200)** (r6) |
| [시작] 되돌리기 — 고객 진행 그대로 (r5) | — | 없음(ccc 만 — [시작](첫 아님)과 같다) | — | — | §5.13 |
| [종료] 되돌리기 (r5) | 1 | 내부 `schedule/flow/v1/commands/change-tasks-complete` | `{scheduleId, sequences:[그 시술 하나], complete:false}` | 그 작업 `status ≠ DONE`(확인 조건 새 키 `statusNot` — 아래) | `_RESUME 10-26` · 1차 HAR 「`false` 로 완료 취소도 될 것으로 추정 · HAR 에 없음」 · ~~미확인~~ **WP-KOS K2 받음(200 · `DONE → READY`)** (r6) |
| [귀가 대기] | 1 | 내부 `schedule/v1/commands/cancel-flow-tasks` — ~~남은 비시술 작업이 없으면 만들지 않음~~ → **남은 「방 배정」이 없으면 만들지 않음** (r4 · r6 — review-doc r4 F1) | ~~`{scheduleId, sequences:[끝나지 않은 작업 중 시술 작업을 뺀 것], reason:"CANCEL"}`~~ → `{scheduleId, sequences:[안 끝난 「방 배정」(§5.1 is_room_task)], reason:"CANCEL"}` (r4) — §5.7 · 코드 `service/actions.py` `home` | 그 작업들 `status = CANCELED` | E2E-3 · 1차 HAR (0.3.0) · `_RESUME 10-25` 「규칙 하나」 줄 |
| 〃 | 2 | 공개 `schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"PROCEDURE_DONE"}` | 일정 `flowStep = PROCEDURE_DONE` | D-33 · HAR(`시술완료_상태.har`) |

- `scheduleId` = `visit.kos_id` · `sequences` = `procedure.kos_sequence`
- `change-flow-step` 거절(스펙): `ProceduresNotFound` 등 400 → §4.4 재전송 · 실패 규칙 — API §5
- **같은 단계 규칙** (0.2.0 — S2 · 워커 실호출): KOS 는 **지금 단계와 같은 단계로의 `change-flow-step` 을 400 으로 거절**한다. 그래서
  - op 을 만들 때 ~~· 보내기 직전에~~ (r6 — 코드는 보내기 직전에 거르지 않는다 · `kos/ops.py` `send_heads` · review-doc r4 참고) 마지막 조회의 KOS `flowStep` 이 이미 목표 단계면 **보내지 않고 `confirmed`** 로 둔다 — 만들 때의 판단은 ccc 고객 상태(= 마지막 조회 값 · 반영 대기 중이면 ccc 값 · §4.3)로 한다(조회 10초 사이에 KOS 가 먼저 바뀐 경우 — ccc 는 아직 `waiting` 이라도)
  - 보냈는데 400 이 오면 바로 실패로 세지 않고, 다음 조회에서 `flowStep` 이 목표 단계면 `confirmed`(재전송 없음). 아니면 §4.4 재전송 · 실패 규칙
- `call-tasks-doctors` 가 400 을 주는 조건 — 귀가 대기 일정은 400(처분 W10) · **시술 작업에 방이 없으면 400 `errorProperties roomId NotFound`** → 1번 `change-tasks-room` 으로 막는다(E2E-1) (0.3.0). 이미 `WAITING` / `READY` 작업 재호출 · [다른 원장에게]는 미확인 → OQ-516 (0.2.0)
- KOS 작업 칸 「진행중」은 **수락(집도의 지정) 직후** 뜬다(KOS 에 작업별 시작 칸이 없다) — **그대로 둔다**. 시술 진행 · 대기의 기준은 ccc 이고 현장은 KOS 를 보지 않는다. [시작] 때 집도의를 지정하는 방식으로 바꾸지 않는다 (0.3.0) — E2E-2 · `_RESUME` 10-21 「KOS 작업 「진행중」은 수락 시점 그대로」 줄
- **되돌리기 op 의 확인 · 대체 규칙** (r5): ① [종료] 되돌리기의 확인 = 그 작업 `status` 가 `DONE` 이 **아님**(되돌린 뒤 KOS 가 어느 상태 — `READY` · `NOT_STARTED` 등 — 로 가는지 모르므로 「아님」으로 본다 · WP-KOS 가 실제 값을 적는다 → (r6) K2 = `READY`. 확인 조건은 「아님」 그대로 둔다 — 집도의 없는 작업의 값은 보지 않았다) → `expect` 에 `statusNot: "DONE"` 키를 더한다(코드 `kos/ops.py` `expect_met`) ② **같은 작업의 앞 [종료] op(`status = DONE`)은 뒤 되돌리기 op 이 `sent` · `confirmed` 면 `confirmed`** 로 본다 — 지금 `superseded`(§4.4)의 `status` 규칙에 `statusNot` 도 같은 필드로 넣는다. 거꾸로 되돌린 뒤 다시 [종료]하면 앞 되돌리기 op 이 대체된다. 이게 없으면 앞 [종료] op 이 「KOS 값이 바뀌지 않음」으로 재전송돼 KOS 를 다시 완료로 만든다 ③ [시작] 되돌리기의 flow-step op 은 지금 `flowStep` 대체 규칙(앞 `PROCEDURE` op 대체)을 그대로 쓴다
- 「KOS 화면은 마지막 완료 때 방을 비워 보인다」 — ccc 는 그 표시를 따르지 않는다(§5.7) — D-33 · HAR

## 9. 검증 기준 — 로컬 E2E (데모 지점)

준비: `procedure/back/.env` 를 채운다(값 원천 = ax-clinic-project · 사용자) → `docker compose up --build` → `http://localhost:3700` 로그인. KOS 확인은 **데모 KOS 웹 화면** 또는 공개 `getScheduleDetail`(조회만) — 현장 조작 금지(D-10)는 E2E 의 KOS 쪽 **준비**(일정 만들기 · 시술 대기 · 방 배정)에는 해당하지 않는다.

| # | 단계 | ccc 에서 보는 것 | KOS 쪽 확인 | 근거 |
|---|---|---|---|---|
| 0 | 데모 KOS 에서 4층 오늘 일정 1건을 시술 대기 · 방 배정(작업 2개 이상) · **방 없는 ETCETERA(마취 · 시트팩 등) 1개 이상 필수**(r4 — 일반 시술로 다루는지 본다 · #19 · #20) — 데모 환자에 없으면 E2E 전에 KOS 화면에서 붙인다. KOS 에서 만들 수 없으면 그 사실을 기록하고 사용자에게 알린다 (r2) | — | 일정 `PROCEDURE_WAITING` · ETCETERA 작업 `room` | D-21 · D-22 · `_RESUME 10-23` 「방 배정」 줄 · review r1 W10 (r2) |
| 1 | 카드 등장 | 10초 안에 카드 · 「시술 대기」 · 입실 시각 · 오더 메모 · (결제 전이면) 「수납 필요」. 방 없는 일정은 안 나온다 | — | D-08 · D-21 · D-22 |
| 2 | [마취 시작] → 21분 대기 또는 시각 조작 없이 표시만 확인 → [마취 종료] | 「마취 · NN분 경과」 보라 → 20분 이상 빨강 · 「확인」 칸 +1 → 「완료 N분」 | KOS 변화 없음 | D-20 · D-23 |
| 3 | 시술 2개 체크 → [의사 호출 · 2건] → 「모든 의사」 | 「호출함」 · 「전체 호출 · 수락 전」 · [시작] 꺼짐 · 호출 탭 1건 · 5분 뒤 「확인이 필요」 | 두 작업 `room` = 카드 방 · `assignees` = 시스템 계정 · `status = WAITING` — **몇 초 안에**(20 ~ 30초 걸리지 않음) (0.3.0) | D-24 · D-25 · D-30 · E2E-1 · E2E-6 |
| 4 | 호출 탭에서 원장 A 골라 [수락] | 두 시술 「A 수락 · 시작 가능」 · 호출 탭 0건 · 「최근 수락」 1줄 | 두 작업 `doctors` = A · `status = READY` | D-27 |
| 5 | 시술 1 을 다시 체크 → 원장 B 지정 호출 → 호출 탭 [다른 원장에게] → 원장 C [수락] | 시술 1: 지정 호출 → 전체 호출(새 줄) → C 수락. 시술 2 는 A 그대로 | 시술 1 `doctors` = C | D-25 · D-27 · OQ-501 |
| 6 | 시술 1 [시작] | 고객 「시술 진행」 · 시술 1 「C · HH:MM 시작」 · [종료] | 일정 `flowStep = PROCEDURE` | D-30 · D-32 |
| 7 | [마취 시작] (진행 중) | 켜진다 | 변화 없음 | D-23 |
| 8 | 시술 1 [종료] · 시술 2 [시작] → [종료] | 완료 줄이 위로 · 카드 아래가 [귀가 대기] 로 바뀜 | 각 작업 `status = DONE`. KOS 화면은 방을 비워 보일 수 있다 — ccc 카드 · 방은 그대로 | D-31 · D-32 · D-33 |
| 9 | [귀가 대기] | 카드 흐림 · 맨 뒤 · 「귀가 대기 HH:MM」 — 데모 KOS 에서 귀가(`COMPLETED`) 처리하면 10초 안에 카드가 사라진다 (0.3.0) | ~~「방 배정」 등 남은 작업 `CANCELED`~~ (r4) → 안 끝난 **「방 배정」만** `CANCELED` · 일정 `flowStep = PROCEDURE_DONE` · KOS 방이 빈다 (0.3.0) | D-33 · E2E-3 · E2E-9 |
| 10 | 반영 실패 확인(선택) — back 의 내부 API 주소를 틀리게 두고 [종료] | ~~「KOS 반영 중」 → 3회 뒤 「KOS 반영 실패」 · ccc 상태는 완료~~ (0.4.0 바뀜) → 웹 카드에는 표시 없음 · ccc 상태는 완료 · `GET /api/board` 의 그 카드 `kos.status` 가 `pending` → 3회 뒤 `failed`(앱 룸 상세에도 보임) | 변화 없음 | D-09 · `_RESUME 10-23` · OQ-522 |
| 11 | 조회 시간 · 덮어쓰기 | 데모 KOS 에서 오더 메모를 고치면 10초 안에 카드에 반영 | — | D-08 · D-09 |
| 12 | (0.4.0) 헤더 · 제목 줄 | 상단 메뉴 「현황」 하나 · 호버하면 「시술 현황」 한 항목 · 사이드바 없음 · 제목 줄에 [입실순 \| 배치순] 없음 · 「마지막 KOS 동기화 HH:MM:SS」 | — | `_RESUME 10-23` 헤더 · 버튼 줄 · §6.2 |
| 13 | (0.4.0) 「방 배정」 줄 · 기타 작업 | 1 단계 카드에 **「방 배정」 줄이 없다**. ~~0 단계의 **방 없는 기타 작업(마취 · 시트팩 등)은 맨 위 읽기 전용 줄(제목 + KOS 상태)로 반드시 보인다**(필수 확인 · r2).~~ (r4 바뀜) → 0 단계의 기타 작업(마취 · 시트팩 등)은 **일반 시술 줄**(체크 · [시작] · 담당 글자)로 반드시 보인다(필수 확인). [귀가 대기](9 단계) 뒤 KOS 「방 배정」이 `CANCELED` 인 것은 그대로 | 「방 배정」 작업 `CANCELED`(9 단계와 같음) | `_RESUME 10-23` 「방 배정」 줄 · `_RESUME 10-25` 「규칙 하나」 줄 · §5.1 (r4) |
| 14 | (0.4.0) 드래그 순서 · 공유 | 카드 3장 이상에서 ① 첫 카드를 **바로 아래(다음) 카드** 위에 놓으면 둘이 자리를 바꾼다 ② 한 카드를 **마지막 카드** 위에 놓으면 맨 끝으로 간다 ③ 뒤 카드를 앞 카드 위에 놓으면 그 앞으로 — 끄는 동안 같은 자리로 미리 옮겨 보임 (r2). **다른 브라우저(의국 PC 역할)도 새로고침 없이 같은 순서** · 새로고침 · back 재시작 뒤에도 같은 순서. 귀가 대기 카드는 끌리지 않는다 | KOS 변화 없음(데모 KOS 화면 순서 그대로) | `_RESUME 10-23` 드래그 순서 줄 · §5.12 · §7.5 |
| 15 | (0.4.0) 새 카드 · 귀가 대기 | 순서를 정한 뒤 데모 KOS 에서 새 일정을 시술 대기 + 방 배정 → 새 카드가 **귀가 대기 아닌 카드들 맨 뒤**에. 한 카드를 [귀가 대기] → 맨 뒤(귀가 대기 시각 순)로 가고 나머지 순서는 그대로 | — | `_RESUME 10-23` 기본값 · §5.12 |
| 16 | (0.4.0) 동시 저장 | 두 브라우저에서 거의 같이 다른 순서로 놓는다 → 둘 다 **나중에 놓은 쪽 순서**로 맞춰진다(오류 없음) | — | §5.12 「마지막 쓰기가 이긴다」 |
| 17 | (0.4.0) 시안 차이 | 카드 머리 한 줄(방 · Badge / 입실) · 경과 글자 · 「KOS 반영」 글자 없음 · 시술 줄 진행 → 대기 → 완료(점선) · 현황 탭 3 × 2 칸 — 전체현황판 시안 `board` 장면과 나란히 놓고 본다 | — | §6.3 · §6.4 · §6.7 #11 ~ #16 |
| 18 | (r4) 방 배정 작업 없이 카드 | 데모 KOS 에서 「방 배정」 작업 없이 **시술 작업에만 방**을 붙인 일정 → 10초 안에 카드가 뜬다(방 = 그 작업 방 · 입실 = 그 작업 배정 시각). 방이 어디에도 없으면 안 뜬다 | 시술 작업 `room` 만 있음 | `_RESUME 10-25` 「카드 방」 줄 · §3.3 · §5.1 |
| 19 | (r4) 기타 작업 = 일반 시술 | 시트팩(ETCETERA) 줄을 체크 → 호출 · 수락 · [시작] · [종료] 가 일반 시술과 같다. **시트팩이 안 끝났으면 카드 아래에 [귀가 대기]가 없다**(다른 시술이 다 끝나도) · 「수납 필요」도 시트팩 결제를 센다 | 시트팩 작업 `room` = 카드 방 · `WAITING` → `READY` → `DONE`(실 KOS 가 ETCETERA 에 호출 · 완료를 받는지 이 단계에서 처음 본다 — OQ-528) | `_RESUME 10-25` 「규칙 하나」 줄 · §5.1 · §5.7 |
| 20 | (r4) 시트팩 호출 뒤에도 남음 | #19 에서 시트팩을 호출해 KOS 가 시트팩에 방을 붙인 뒤에도 **시트팩 줄이 카드에 남는다**(「방 배정」으로 바뀌어 숨지 않는다). [귀가 대기] 때 취소되는 것은 「방 배정」뿐 | 귀가 대기 뒤 시트팩 `DONE` 그대로 · 「방 배정」만 `CANCELED` | `_RESUME 10-25` 「「방 배정」 판정」 줄 · §5.1 |
| 21 | (r5) 토스트 [되돌리기] — [시작] | 그 고객의 **첫** [시작] → 토스트 「<방> · <시술> 시작」 + [되돌리기] **5초** → 누른다(모달 없음) → 시술 「<원장> 수락 · 시작 가능」(또는 「<원장>」) · [시작] 켜짐 · 고객 「시술 대기」 · 「시술 대기로 되돌림」 토스트. 5초 뒤엔 토스트와 [되돌리기]가 없다 | 일정 `flowStep = PROCEDURE_WAITING`(WP-KOS K4 받음 (r6)) · 작업 상태 변화 없음 · **KOS 웹 화면 표시도 본다**(워커 미관찰 (r6)) | `_RESUME 10-26` · §5.13 · §8 |
| 22 | (r5) 아이콘 — [종료] 되돌리기 | [종료] → 완료 줄 「완료」 **왼쪽** 아이콘 · 호버 「되돌리기」 툴팁 → 누르면 medikit 모달 「시술 중으로 되돌리겠습니까?」 → [취소] = 아무것도 안 바뀜 → 다시 열어 [되돌리기] → 시술 진행 「<원장> · HH:MM 시작」(옛 [시작] 시각) · [종료] 켜짐 · (전부 완료였으면) 카드 아래 [귀가 대기] 사라짐 | 그 작업 `status = READY`(WP-KOS K2 와 같은지 (r6)) · **KOS 웹 화면에서도 완료가 풀렸나**(워커 미관찰) · 30초 뒤에도 다시 `DONE` 으로 안 돌아감 | `_RESUME 10-26` · §5.13 · §8 · ~~OQ-529~~(닫힘 (r6)) |
| 23 | (r5) 아이콘 — [시작] 되돌리기 · 고객 진행 그대로 | 다른 시술이 완료 · 진행인 고객에서 진행 줄 [종료] **왼쪽** 아이콘 → 모달 「시술 대기로 되돌리겠습니까?」 → [되돌리기] → 그 시술만 대기 · 고객 「시술 진행」 그대로. 대기 줄에는 아이콘이 없다 | flowStep 변화 없음 · 작업 변화 없음 | §5.13 |
| 24 | (r5) 다른 화면이 먼저 바꿈 | 브라우저 A [종료] → 브라우저 B 가 아이콘으로 그 시술 되돌리기 → A 가 토스트 [되돌리기] → **오류 토스트 「완료된 시술이 아니에요」**(409) · 두 화면 모두 시술 진행 | — | §5.13 동시성 |
| 25 | (r5) 아이콘 없는 곳 | 귀가 대기 카드의 완료 줄 · KOS 화면에서만 완료한 시술(ccc [시작] 없음) · 「방 배정」 · 대기 줄 — 아이콘 없음 | — | §5.13 `canUndoStart` · `canUndoFinish` |
| 26 | (r5) 되돌린 뒤 다시 [종료] | #22 뒤 같은 시술 [종료] → 완료 · 1분 뒤에도 그대로(앞 op 재전송으로 흔들리지 않음) · `GET /api/board` 그 카드 `kos.status = ok` | 그 작업 `status = DONE` | §8 되돌리기 op 대체 규칙 |

back 단위 시험(pytest, KOS 는 가짜 클라이언트): §5.10 전이 · §5.11 활성 조건 · 유효 호출(D-25) · 수락 범위(D-27) · 덮어쓰기 보호(§4.3) · op 순서 · 재전송 · 실패(§4.4) · 원장 목록 제외(D-11) · 조회 시간(D-08) · SSE(§7.5 — 첫 접속 스냅샷 · 조작 뒤 1개 · 토큰 없으면 401).
0.5.0 더함(r5): `undo-start` — `doing` 만 · 호출 · 수락 · 집도의 남음 · [시작] 다시 켜짐 · 진행 · 완료 0 이면 고객 `waiting` + flow-step op(`PROCEDURE_WAITING`) **항상 1줄** · 남으면 op 0 · ~~이미 KOS 가 그 단계면 op `confirmed`~~ (r6) → 그 op 이 400 을 받은 뒤 다음 조회에서 KOS `flowStep = PROCEDURE_WAITING` 이면 `confirmed`(재전송 없음) · 첫 [시작] 직후 되돌리면 앞 `PROCEDURE` op 은 `superseded` 로 `confirmed` / `undo-finish` — `done` + ccc [시작] 있음만 · `completed_at` 비움 · `kos_status = READY` · `complete:false` op 1줄 · 고객 상태 그대로 · `canHome` 풀림 / 409(`visit_home` · `procedure_not_doing` · `procedure_not_done` · `procedure_not_started`) · 404(「방 배정」 · 없는 id) · 403 `fake_board` · 세 역할 모두 · `event_log` 1줄 · SSE 1개 / 스냅샷 `canUndoStart` · `canUndoFinish`(귀가 대기 · 「방 배정」 false) / `expect_met` `statusNot` · `superseded`([종료] → 되돌리기 → [종료] 순서에서 앞 op 재전송 0) / 경로 수 19.
0.4.3 더함(r4 — 코드 시험 162 통과): 카드 방 type 무관(시술 작업에만 방 · 여러 방 = 가장 늦은 배정 · 동률 = ETCETERA → 큰 sequence · 방 없음 = 카드 없음) · ETCETERA 가 일반 시술처럼 체크 · 호출 · 시작 · 종료 · 전부 완료 · 수납에 든다 · 시트팩 안 끝나면 [귀가 대기] 409 · 「방 배정」 스냅샷에 `isRoomTask=true` · 판정 · 조작에서 빠짐 · [귀가 대기] 취소 = 「방 배정」만 · 호출된 ETCETERA 는 방이 붙어도 「방 배정」 아님. 아래 0.4.0 줄의 「「방 배정」이 `procedures[]` 에 없음 · 방 없는 `etc` 는 있음 · 취소 대상에 「방 배정」 그대로」는 ~~뒤집힘~~ (r4)

0.4.0 더함(r2 — StrictInt: `"3"` · `3.0` · `true` 400 · 옛 스키마 DB 파일로 시작해도 `board_order` 가 생기고 기존 행이 남음): 「방 배정」(방 있는 `etc`)이 `procedures[]` 에 없음 · 방 없는 `etc` 는 있음 · [귀가 대기] 취소 대상에는 「방 배정」 그대로 · `PUT /api/board/order`(저장 · 거르기 — 없는 id · 귀가 대기 · 사라진 카드 · 400 형식 · 같은 id 두 번 · 마지막 쓰기 · `event_log` 1줄 · `kos_op` 0줄 · 저장 뒤 SSE 1개 · 401 · 403 `fake_board`) · 스냅샷 정렬(목록 → 목록 밖 입실순 → 귀가 대기 시각 순 · 날짜 바뀌면 순서 없음) (0.4.0)

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
| OQ-508 | 「수납 필요」 · 「KOS 반영 중 · 실패」 자리 · 모양 — 시안에 없음 | §6.7 #7 · #8. **0.4.0: 「KOS 반영 중 · 실패」 쪽은 닫힘**(웹은 안 그림 · `_RESUME 10-23`) — 「수납 필요」는 전체현황판 시안에 자리가 생겼다(`M:825-827` · 고객 줄 끝 Badge warning sm = 지금 코드와 같음) → 그것도 닫힘 (0.4.0) | 닫힘 (0.4.0) |
| OQ-509 | 「KOS 반영 실패」 뒤 복구 — 다시 보내기 버튼 · 운영 절차 | 버튼 없음 · back 로그 · `event_log(kos_failed)` 로 확인. ~~되돌리기 정책 때 같이~~ (r5) 10-26 되돌리기는 **사용자 조작([시작] · [종료]) 되돌리기**라 이 질문(반영 실패 복구)을 닫지 않는다 — 그대로 열림 | 새로 |
| OQ-510 | 재전송 횟수 · 간격 | 조회 주기마다 · 3회 뒤 실패 | 새로 |
| OQ-511 | ~~한 일정에 방 있는 ETCETERA 작업이 둘 이상이면 어느 방인가~~ (r4) → 한 일정에 **방 있는 작업(type 무관)**이 둘 이상이면 어느 방인가(HAR 에 「방 배정」 외 「방 점유/원장 상담」 작업도 있다 · 데모 10-25 는 시술 작업마다 방) | `roomAssignedDateTimeUtc` 가 가장 늦은 작업의 방 · 동률 · 시각 없음 = ETCETERA 먼저 → 큰 `sequence` — 코드 그대로(`kos/sync.py` `_card_room_task`) · 호출 때 고른 작업에 넣는 방도 이것(§5.4) (r4) | 기본값 구현 (0.3.0 · r4) |
| OQ-512 | KOS 쪽에서 ccc 를 거치지 않은 호출 · 집도의 변경이 조회되면(D-10 은 현장이 안 한다고 정함) | KOS 값을 보여 준다(집도의 · 호출 여부) · ccc 호출 기록은 만들지 않는다 | 새로 |
| OQ-513 | 조회 시간 밖의 조작 | 막지 않는다 · KOS 에 보내고 확인은 다음 조회 시간 | 새로 |
| OQ-514 | 헤더 계정 표시 문구(시안 「데스크」 · 계정은 관리자 1개) | ~~시안 문구 그대로~~ (0.4.0 바뀜) → 전체현황판 시안 = 「{역할} · {이름}」(`M:2245` · 역할은 데모 prop). 역할 글자(관리자 · 의사 · 간호사 등)를 정한 곳이 없어 **지금 `name` 그대로**(SPEC-004 §3.6) | 열림 (0.4.0) |
| OQ-515 | 진행 중 마취가 있는 채로 [귀가 대기] | 막지 않는다 · 귀가 대기 카드엔 마취 버튼 없음 | 새로 |
| OQ-516 | `call-tasks-doctors` 가 400 을 주는 조건 — 이미 `WAITING`/`READY` 작업 재호출(D-25 다시 호출) · [다른 원장에게](D-27) | 확인된 것: 귀가 대기 일정 400 · **시술 작업에 방 없음 400 `roomId NotFound`**(E2E-1 → 방 넣기 op 으로 막음 · §8). 재호출 · [다른 원장에게] 400 여부는 실 데모 기록 없음 — 400 이면 §4.4 실패 규칙 (0.3.0) | 일부 닫힘(방) · 나머지 열림 (0.3.0) |
| ~~OQ-517~~ | 현황판(웹) 카드의 `kind = etc`(「방 배정 · 준비중」) 줄을 빼나 | ~~사용자 「필요하지 않을 거 같아요 · 일단 기록해놔」 — **빼기로 기록만**(다음 수정 batch). 지금 코드(웹)는 그린다 · back · 스냅샷은 그대로(귀가 대기 취소에 씀) · 앱은 안 그림~~ → **닫힘** — ~~**「방 배정」(방 있는 ETCETERA)만 뺀다 · back 스냅샷에서**(§5.1). 다른 기타 작업은 남긴다. 귀가 대기 취소는 `open_task_seqs` 로 그대로 (0.4.0)~~ · (r4) 그 뒤 다시 바뀜 — 「방 배정」은 스냅샷에 싣고 front 가 숨김(`isRoomTask`) · 다른 기타 작업은 일반 시술(§5.1) | 닫힘(`_RESUME 10-23` → `_RESUME 10-25`) (0.4.0 · r4) |
| OQ-518 | 웹 로그인에 역할 제한을 두나 — 결정은 「웹 = 관리자」(SPEC-004 A-03 · §3.6)인데, 정상 로그인 뒤 웹 폼은 **비밀번호가 있는 계정이면 역할과 상관없이** 들어간다(코드 `front/app/login/page.tsx` · back 은 역할로 막지 않음). 조작 권한은 back 이 API 마다 검사(SPEC-004 §3.4) | 코드 그대로(제한 없음) · 결정 필요 | 열림 (0.3.0) |
| OQ-519 | KOS 데모 지점의 데모 표식 계정(`KOS-DEMO` 이름 · 데모 도구가 데모 테넌트 확인에 씀)이 원장 목록에 섞이면 뺄까 — 지금 제외는 시스템 계정 id + `KOS_EXCLUDE_ACCOUNT_IDS` 뿐(§4.6) | 코드 그대로 — 빼려면 `KOS_EXCLUDE_ACCOUNT_IDS` 에 그 계정 id(env · 코드 변경 없음) | 열림 (0.3.0) |
| OQ-520 | 헤더 「현황」 드롭다운에 예약 현황 · 원내 현황 항목을 언제 · 어떤 모양으로 더하나(시안은 3항목 · `M:1215-1222`) | 지금 없는 화면이라 **그리지 않는다** — 「시술 현황」 한 항목만(코디 기본값). 예약 현황 판에서 다시 | 열림 (0.4.0) |
| OQ-521 | 카드 머리 경과 글자(「호출 N분 경과」 · 「완료 뒤 N분 경과」 · 「귀가 대기 HH:MM」)를 되살리나 | 시안대로 **안 그린다**(§6.7 #11). 사용자 E2E 에서 아쉬우면 다음 batch | 열림 (0.4.0) |
| OQ-522 | 조작 응답 뒤 비동기로 난 **KOS 반영 실패**(3회 재전송 뒤 `failed`)를 웹에서 어떻게 알리나 — 결정(`_RESUME 10-23` 「… **오류 토스트로만**(비동기 실패 알림은 OQ-522 열림)」 줄)의 지금 토스트는 조작 API 실패만 띄운다 | **웹엔 표시 없음**(스냅샷 `kos` · `event_log(kos_failed)` · back 로그 · 앱 룸 상세에만). 스냅샷 `kos.status` 가 `failed` 로 바뀔 때 토스트를 띄울지는 정하지 않았다 — OQ-509(복구)와 같이 | 열림 (0.4.0) |
| ~~OQ-523~~ | 시술실 앱도 공유 드래그 순서를 따르나 | **닫힘** — 웹이 정본 · 앱은 웹에 맞춘다 → §10.1 앱 후속 1 (r5) | 닫힘(`_RESUME 10-26` 「웹이 정본」) (0.4.0 · r5) |
| OQ-524 | 전체현황판 경로를 시안 데모 href(`/live/proc` 등)로 바꾸나 | **`/procedures/live` 그대로**(배포 주소 · 북마크 · 앱 무관). 예약 · 원내 현황이 들어올 때 같이 정한다 | 열림 (0.4.0) |
| OQ-525 | 순서 목록을 며칠치 남기나(`board_order` 전날 행) | 지우지 않는다(하루 1행 · 작다 · 읽지 않음). 정리 정책 없음 | 열림 (0.4.0) |
| ~~OQ-526~~ | 시술실 앱(「`etc` 를 그리지 않는다」)과 웹 규칙(type 무관 · 「방 배정」만 숨김)이 갈라졌다 | **닫힘** — 웹 규칙이 맞다 · 앱이 「`isRoomTask` 만 숨김」으로 맞춘다 → §10.1 앱 후속 2 (r5) | 닫힘(`_RESUME 10-26` 「웹이 정본」) (r4 · r5) |
| OQ-527 | ccc [의사 호출]의 방 넣기(`change-tasks-room`)로 KOS 가 그 작업의 `roomAssignedDateTimeUtc` 를 호출 시각으로 새로 찍으면, 「가장 늦은 배정」이 그 작업이 되어 카드 입실 시각(`inAt`) · 목록 밖 카드 입실순이 호출 시각으로 밀린다 | 실 KOS 미확인 — §9 #3 뒤 입실 시각이 그대로인지 본다. 밀리면 「입실 = 같은 방 작업 중 가장 이른 배정」 등 규칙이 필요(정하지 않음) | 열림 (r4 — backend WP-BE3 보고) |
| OQ-528 | 실 KOS 가 ETCETERA 작업에 `call-tasks-doctors` · `change-tasks-complete` 를 받아 주는가 | ccc 는 type 무관 같은 API 로 보낸다(가짜 KOS 시험만). ~~§9 #19 에서 처음 확인~~ (r5) **WORK-006 WP-KOS K5 에서 실호출로 확인**(`spec-r5-addendum.md` ②) — (r6) 되돌리기 게이트와는 **따로**(되돌리기 계약과 무관 · K5 는 사용자가 데모 KOS 에 방 없는 ETCETERA(시트팩)를 붙이면 진행 · WP-E2E 전까지). 「안 받음」이면 §5.1 쪽(WORK-005 · PR #6) 사용자 결정으로 올린다 · §9 #19 는 그 뒤 화면 확인 — 400 이면 §4.4 실패 규칙 | 열림 (r4 — backend 규칙 하나 보고) |
| ~~OQ-529~~ | 실 KOS 가 `change-tasks-complete {complete:false}`(완료 풀기)를 받나 | **닫힘 — 받음**(WP-KOS K2 · 2026-10-26): HTTP 200 · 작업 `DONE → READY` · `completedDateTimeUtc` 지움 · 집도의 · 담당 · 호출 시각 그대로 · 22초 뒤에도 `READY`. §5.13 즉시 값 `READY` 확정. 남은 것: 집도의 없는 작업의 값 · 시술권이 걸린 작업의 차감 되돌림(OQ-502 — 데모 작업은 시술권 없음) · KOS 웹 화면 표시(§9 #22) | 닫힘 (r5 · r6 — 리포트 `orchestration/work/overall-board/kos-undo-probe-report.md`) |
| ~~OQ-530~~ | 실 KOS 가 `change-flow-step` **뒤로 가기**(`PROCEDURE` → `PROCEDURE_WAITING`)를 받나 | **닫힘 — 받음**(WP-KOS K4 · 2026-10-26): HTTP 200 · `flowStep` 바뀜 · 작업 값 그대로. 기준선 K3(`PROCEDURE_WAITING` → `PROCEDURE`)도 200. KOS 웹 화면 표시는 §9 #21 에서 | 닫힘 (r5 · r6 — 리포트 `orchestration/work/overall-board/kos-undo-probe-report.md`) |
| OQ-531 | 귀가 대기 카드에서 [종료] 되돌리기(고객 귀가 대기 → 진행)를 열까 | **막는다**(아이콘 없음 · 409 `visit_home` — §5.13). 열려면 `change-flow-step` `PROCEDURE_DONE` → `PROCEDURE` 와 [귀가 대기] 때 취소한 「방 배정」 되살리기가 필요 — 둘 다 미확인 | 열림 (r5) |
| OQ-532 | 토스트 [되돌리기] 가 그 사이 다른 사람이 같은 상태로 만든 조작을 되돌리는 경우(A [시작] → B 되돌리기 → C [시작] → A 토스트 되돌리기 = C 의 [시작]이 풀림) — 「내 조작만」 되돌리게 이벤트 id 검사를 둘까 | **두지 않는다** — 상태 검사(409)만 · 5초 창이라 드물다(기본값 · §5.13 동시성) | 열림 (r5) |

### 10.1 앱 후속 — 웹 기준으로 맞춘다 (r5)

`_RESUME 10-26` 「웹이 정본 · 앱은 나중에 웹에 맞춘다」 — 웹과 앱이 다른 곳은 질문이 아니라 **앱이 할 일**이다. 앱 판(SPEC-004 개정 · 앱 WORK)에서 아래를 웹 계약대로 맞춘다. 이번 판(WORK-006)은 앱 코드 · 빌드를 건드리지 않는다.

| # | 웹 계약(정본) | 앱 지금 | 앱이 할 일 | 옛 OQ |
|---|---|---|---|---|
| 1 | 카드 순서 = 스냅샷 `cards[]` 배열 순서(드래그 공유 · §5.12) | 자기 입실순 정렬(`app/lib/view/view.dart:58`) | 정렬을 빼고 배열 순서 그대로 | OQ-523 |
| 2 | 작업은 type 무관 같은 시술 · `isRoomTask` 만 숨김(§5.1) | `etc` 를 전부 숨김(SPEC-004 §6.0) | `isRoomTask` 만 숨기고 ETCETERA 를 시술 줄로 | OQ-526 |
| 3 | [시작] · [종료] 되돌리기(§5.13 · `canUndoStart` · `canUndoFinish` · `undo-start` · `undo-finish`) | 없음 | 같은 API · 같은 조건(앱 UI 모양은 앱 판에서) | — (r5 새) |

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
| D-09 | KOS 기준 / ccc 기준 · 반영 중 · 실패(→ 0.4.0 웹 카드 표시 없음 · 스냅샷 `kos` 는 유지) | §3.2 · §4.3 · §4.4 · §5.2 · §6.3 · OQ-522 |
| D-10 | 현장은 KOS 직접 조작 안 함 | §1.2 · §9 · OQ-512 |
| D-11 | 원장 목록 · 시스템 · 마취용 · 비활성 제외 | §2.3 · §4.1 · §4.6 |
| D-12 | ccc DB 가 KOS 를 품음 · `kos_id` · 대응표 | §3.1 · §3.2 · §3.3 |
| D-13 | 이벤트 로그(0.4.0 `board_order` 더함) | §3.1 · §3.2 · §7.3 |
| D-14 | 개인정보 = 화면에 쓰는 것만 | §1.2 · §3.1 · §3.3 · §7.2 |
| D-15 | SQLite · 나중 PG + Redis | §2.2 · §3.1 |
| D-16 | 시안 정본 | 머리말 · §6 |
| D-17 | 구조 · 헤더 메뉴 하나 → (0.4.0) 상단 「현황」 하나 + 드롭다운 「시술 현황」 하나 · 사이드바 없음 | §6.2 · §6.3 · §6.7 #5 · #14 |
| D-18 | 입실순 · 배치순 → (0.4.0) **뒤집힘** — 버튼 없음 · 정렬 = 드래그 순서(`_RESUME 10-23`) · 입실순은 순서 없는 카드에만 | §3.3 · §5.12 · §6.3 |
| D-19 | 카드 구성 | §6.3 |
| D-20 | 현황 · 필터 · 확인이 필요 | §5.8 · §6.4 · OQ-504 |
| D-21 | PROCEDURE_WAITING 이면 카드 · 수납 필요 | §5.1 · §6.7 #7 |
| D-22 | 방 있는 고객만 · ~~ETCETERA 안 보임~~ → 읽기 전용으로 보임(E2E-4) (0.3.0) → ~~(0.4.0) 「방 배정」(방 있는 ETCETERA)만 다시 뺌 · 그 밖은 보임~~ → (r4) 방 = type 무관 · 「방 배정」만 숨김(스냅샷엔 실림) · 그 밖 작업은 일반 시술 | §3.3 · §5.1 · §6.3 · ~~OQ-517~~(닫힘) |
| D-23 | 마취 별개 · 시안 고침 | §5.3 · §5.11 · §6.7 #1 · §8 |
| D-24 | 의사 호출 · KOS 2단계 → 방 넣기 포함 3단계(E2E-1) (0.3.0) | §5.4 · §8 |
| D-25 | 호출 쌓기 · 유효 호출 | §3.2 · §5.4 · §5.5 |
| D-26 | 진행 · 완료 시술은 호출 대상 아님 | §5.4 · §5.11 |
| D-27 | 의국 화면 수락 · 받는 범위 · 다른 원장에게 | §5.5 · §6.4 · §6.7 #2 · #4 · §8 |
| D-28 | 되돌리기 없음 → (r5) **[시작] · [종료]만 되돌리기 생김**(`_RESUME 10-26`) · 호출 · 수락 · 마취 · 귀가 대기는 그대로 없음 | §1.2 · §5.5 · §5.13 · §6.3 · §6.4 · §6.7 #3 · #23 · OQ-509 |
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

## 부록 E. 0.4.0 반영표 — `_RESUME 10-23` 결정 줄 → 절 (0.4.0)

원천 `orchestration/work/overall-board/_RESUME.md` §2 결정 표 2026-10-23 줄 ~~8개~~ → **10개**(r2 — 코디가 7 · 8번째 줄을 더함 · 아래 #7 · #8 · 옛 #7 · #8 은 #9 · #10)(위에서부터). 취소선 부분은 같은 날 뒤집힌 것 — SPEC 은 지금 것만 따른다.

| # | 결정 줄(줄임) | SPEC-003 0.4.0 | WORK-005 |
|---|---|---|---|
| 1 | 목적 = 시술 현황판 → 「Ceramique 전체현황판」 업그레이드 · **현황 탭만**(다른 탭 X) | 머리말 · §1.1(화면 줄) · §1.2(예약 · 원내 현황 · 다른 메뉴 Out) · §6 머리 표 | 머리말 · Meta |
| 2 | 다음 발주 보류 — 먼저 사용자와 계획 | 해당 없음(오케스트레이션 순서 — SPEC 에 닿는 정책 없음) | 해당 없음 |
| 3 | **디자인 시안이 정본** · ~~프론트만 변경~~ → 프론트 + back 소량(KOS 무변경) | 머리말 · §6 머리 표 · §6.7(#11 ~ #22 (r3)) · §5.1 · §5.12(back 소량 = 순서 · ~~「방 배정」 거르기~~ (r4) → `isRoomTask` · 방 판정 type 무관) · §8 변경 없음(KOS 무변경) | WP-BE · WP-FE 범위 |
| 4 | 드래그 순서 = **back DB 저장**(ccc 만 · KOS 반영 없음) · 기본값: 모든 화면 공유(SSE) · 그날 단위 · 새 카드 맨 뒤 · 귀가 대기 드래그 제외 | §1.1 · §3.2 `board_order` · `event_log.type` · §5.12 · §6.3 드래그 · §7.2 배열 순서 · §7.3 `PUT /api/board/order` · §7.4 경로 수 · §7.5 ① · §9 #14 ~ #16 · §6.7 #19 · #20 · OQ-523 · OQ-525 | WP-BE1 · WP-BE2 · WP-FE2 |
| 5 | 헤더 상단 메뉴는 「현황」 하나만(나머지 5개 안 그림) | §2.4 · §6.1 · §6.2 헤더 · §6.7 #5 · #14 · §9 #12 · 부록 A D-17 · OQ-520(드롭다운 항목 — 코디 기본값) | WP-FE1 |
| 6 | ~~기타 작업 줄 전부 뺀다~~ → **「방 배정」 줄만 뺀다**(r4 — 앞 절반은 10-25 로 뒤집힘 · 부록 H)(OQ-517 · room 있는 ETCETERA = `sync.py:39-40`) · 다른 ETCETERA 남김 · **입실순/배치순 버튼 뺀다** · **KOS 반영 중/실패 표시 뺀다** | 「방 배정」: §5.1 · §6.3 #5 · §6.7 #13 · §7.2 · §9 #13 · ~~OQ-517~~ 닫음 · 부록 A D-22 / 버튼: §5.12 · §6.2 제목 줄 · §6.3 정렬 · §6.7 #14 · 부록 A D-18 / KOS 표시: §6.3 · §6.7 #8 · §9 #10 · OQ-508 닫음 · OQ-522 | WP-BE1(「방 배정」) · WP-FE1 · WP-FE2 |
| 7 | (r2 새 줄) 결정 표에 없는 화면 차이는 **시안대로** · KOS 반영 실패는 카드 표시 없이 **오류 토스트로만**(비동기 알림 OQ-522) | §6.3(KOS 표시) · §5.9 · §5.11 · §6.4 · §6.7 #11 · #14 ~ #16 · #22 · OQ-522 근거 칸 | WP-FE1 · WP-FE2 |
| 8 | (r2 새 줄) review r1 기본값 ① DEC-005 개정 안 함 · 머리말 「0.4.0 부터 _RESUME 10-23 > DEC-005」 ② 드래그 놓기 = **방향 따라** | ① 머리말 우선순위 문장 · 부록 A ② §5.12 「무엇」 · §6.3 드래그 · §6.7 #21 · §9 #14 | WP-FE2 · WP-E2E |
| 9 | 예약 현황은 workflow-v2 예약 구간 갱신 → KOS API 조사 순 | §1.2(다음 판 · Out) · OQ-520 | 범위 밖(「하지 않는 것」) |
| 10 | 디자인 원천 = Claude Design p/dda9a931… `Ceramique 전체현황판.dc.html` | §6 머리 표 · 머리말 근거 표기 `M:n` | Meta(시안 경로) |

10줄 · 누락 0 (r2). 결정 표에 없고 **시안을 따른** 화면 차이 = §6.7 #11 · #14 ~ #16 · §5.9 · §6.4(시안 근거) — 판단이 안 선 것은 OQ-514 · OQ-521 · OQ-524 로 열어 두었다.

## 부록 F. review-doc r1 처분 (r2 · 2026-10-23)

원천 `orchestration/work/overall-board/review-doc-r1.md`(FAIL 2 · WARN 12) · 지시 `orchestration/work/overall-board/spec-r2-instructions.md`.

| 항목 | 처분 | 바뀐 곳 |
|---|---|---|
| F1 | §5.1 살아 있는 문장 = 「**방 없는 ETCETERA(마취 · 시트팩 등)는 스냅샷에 실린다**」 | SPEC §5.1 |
| F2 | (c) — FE 는 가짜 보드에서 **미리보기 · 놓은 직후 로컬 순서**까지만 확인. 403 `fake_board` 도 일반 오류(토스트 + 스냅샷 순서 복귀) — 예외 없음. 「놓은 뒤 유지 · 공유」는 WP-E2E(데모 지점) | SPEC §6.3 · WORK-005 고정점 아래 문단 · WP-FE2 완료 조건 · WP-E2E |
| W1 | 근거를 `_RESUME 10-23` 새 줄(「시안과 코드가 다른데 … 시안대로」 · 「오류 토스트로만」)로 | SPEC §5.9 · §6.7 #11 · OQ-522 · 부록 E #7 |
| W2 | DEC-005 개정 안 함 · 머리말에 「0.4.0 부터 `_RESUME 10-23` > DEC-005(D-17 · D-18 · D-22 일부)」 | SPEC 머리말 · 부록 E #8 |
| W3 | SPEC-004 §3.4 표에 `PUT /api/board/order`(세 역할) 한 줄 · SPEC-003 §7.3 에 역할 | SPEC-004 §3.4 · SPEC-003 §5.12 · §7.3 · WORK-005 WP-BE2 |
| W4 | `procedure.kind` = ETCETERA 전부 저장 · 방 있는 것은 스냅샷에서 뺌 | SPEC §3.2 |
| W5 | 경합 규칙 하나 — 마지막 요청만 · 응답까지 로컬 순서 · 응답 뒤 `visitIds` 와 같은 첫 스냅샷부터 서버 순서 · 3초 넘으면 스냅샷 · 실패면 바로 스냅샷(기본값) | SPEC §5.12 「놓은 뒤 화면」 · §6.3 · WORK-005 WP-FE2 |
| W6 | 방향 따라 놓기(아래로 = 대상 뒤 · 위로 = 대상 앞) | SPEC §5.12 · §6.3 · §6.7 #21 · §9 #14 · WORK-005 WP-FE2 |
| W7 | `visitIds` = StrictInt 배열 · 시험 항목 | SPEC §7.3 · §9 끝 · WORK-005 WP-BE2 |
| W8 | 검색 결과 클릭 = 검색어 지우고 고객 탭 + 강조(시안 · 코드와 같음) | SPEC §6.4 |
| W9 | [의사 호출] 보임 = `canCall` 일 때만 · 둘 다 아니면 버튼 없음(시안 · 코드와 같음) | SPEC §5.11 · §6.7 #22 |
| W10 | §9 #0 준비에 방 없는 ETCETERA 필수(없으면 KOS 화면에서 붙임 · 못 만들면 기록 · 사용자 알림) · #13 필수 확인 | SPEC §9 #0 · #13 · WORK-005 WP-E2E |
| W11 | 옛 스키마 DB 시험 이름 · grep 기대 수 · 화면 대조 방법(누가 · 무엇으로) | WORK-005 WP-BE2 · WP-FE1 · WP-FE2 |
| W12 | §6 머리 표 빈 줄 지움 | SPEC §6 |
| 참고 | 앱 정렬 근거 `view.dart:60` → `:58` | SPEC §5.12 · OQ-523 |

FAIL 2 · WARN 12 · 참고 1 — 누락 0.

## 부록 G. review-doc r2 처분 (r3 · 2026-10-23)

원천 `orchestration/work/overall-board/review-doc-r2.md`(FAIL 1 · WARN 6) · 지시 `orchestration/work/overall-board/spec-r3-instructions.md`. 사용자 결정 없음 — 기본값으로 닫음.

| 항목 | 처분 | 바뀐 곳 |
|---|---|---|
| R1(FAIL) | WP-FE1 grep 을 `--include='*.ts' --include='*.tsx'` 로 좁힘 — 복사 테마 CSS(`medikit-patches.css`)의 `[Menu-n]` 주석은 §2.4 「그대로 복사」라 대상 밖 | WORK-005 WP-FE1 |
| R2 | 경합 ② 비교 = 스냅샷 귀가 대기 아닌 `cards[]` 에서 보낸 목록 카드만 뽑은 차례 ↔ 보낸 목록 중 아직 귀가 대기 아닌 카드의 차례(새 카드 · 그사이 귀가 대기 · 사라진 카드 빠짐). ① 에서 그사이 귀가 대기가 된 카드 = 로컬 순서에서 빼고 귀가 대기 묶음으로(기본값) | SPEC §5.12 「놓은 뒤 화면」 · WORK-005 WP-FE2 |
| R3 | 앞 · 뒤 판정 = **드래그 시작 때의 전체 순서**(미리보기 순서 아님 — 깜빡임 방지 · 기본값) | SPEC §5.12 「무엇」 · WORK-005 WP-FE2 |
| R4 | 고객 탭 줄 순서 = 카드 순서(스냅샷 `cards[]` · 경합 중 로컬) — 시안 `M:1591` | SPEC §6.4 · WORK-005 WP-FE1 |
| R5 | 범위 표기 따라잡음 — WP-E2E · WP-FE2 계약 칸 §6.7 #11 ~ #22 · 부록 E #3 · WORK 의 「SPEC-003 0.4.0」 → 0.4.2 | WORK-005 Meta · 병렬 그림 · WP-FE2 · WP-E2E · SPEC 부록 E |
| R6 | SPEC-004 → 0.3.1 · `updated_at` 2026-10-23 · 머리말 한 줄 · 20-spec README | SPEC-004 · README |
| R7 | §5.11 `canCall` 예시 = 방 없는 기타 작업 · §7.3 역할 겹친 말 하나로 | SPEC §5.11 · §7.3 |

FAIL 1 · WARN 6 — 누락 0.

## 부록 H. 10-25 결정 반영 · r4 처분 (r4 · 2026-10-25)

원천 `orchestration/work/overall-board/_RESUME.md` §2 2026-10-25 줄 · 지시 `spec-r4-instructions.md` · `room-fix-instructions.md` · `one-rule-instructions.md` · 보고 `backend-r1-report.md`(WP-BE3 · 규칙 하나) · `frontend-r1-report.md`(추가 수정 · 재수정). 코드가 먼저 갔다 — 문장은 코드(`procedure/back/app/{kos/sync.py,domain/rules.py,service/actions.py,service/board_service.py,schemas/board.py}` · `procedure/front/components/procedures/{view.ts,OrderCard.tsx,Aside.tsx,CallPopover.tsx}`)와 맞춘다.

### H.1 10-25 결정 줄 → 절

| # | 결정 줄(줄임) | SPEC-003 0.4.3 | WORK-005 |
|---|---|---|---|
| 1 | ~~작업 type 구분 없앤다(「방 배정」 포함 전부 같은 시술)~~ — 같은 날 아래 줄로 바로잡힘 | 반영 안 함(뒤집힌 줄) — `frontend-r1-report.md` 「추가 수정」(기타 작업 = 일반 시술 줄)만 다음 줄로 이어짐 | — |
| 2 | **규칙 하나**: type 무관 전부 같은 시술 · 예외 「방 배정」 하나(front 숨김 · back 이 작업마다 값 · 「전부 완료」에서 안 기다림 · [귀가 대기] 때 KOS 취소) · 기타 작업 예외 없음 | §3.2 `kind` · §5.1 「규칙 하나」 · 「예외」 · §5.7 · §5.9 · §5.11 `canCall` · §6.3 #5 · §6.4 고객 탭 · §6.7 #13 · §7.2 `isRoomTask` · §7.3 404 · §9 #13 · #19 · #20 · OQ-517 · OQ-526 · OQ-528 · 부록 A D-22 | WP-BE4 · WP-FE3 |
| 3 | 10-23 「방 배정 줄만 뺀다 · 기타 작업 남김」 줄에 ~~(10-25 뒤집힘)~~ | §5.1 0.4.0 줄들 취소선 · §6.3 #5 · §6.7 #13 · §7.2 · 부록 E #3 · #6 표시 | WP-BE1 「되돌림」 표시 |
| 4 | **카드 방 = KOS 작업 어디든 붙은 방** · 여럿이면 배정 시각 최신 · 「방 배정」 없어도 카드 | §3.3 `visit.room_id` · §5.1 조건 3 · §5.4 ① · §9 #18 · OQ-511 · OQ-527 | WP-BE3 |
| 5 | 「방 배정」 판정 = 방 붙은 ETCETERA **이면서 ccc 호출 이력 없음** · KOS 쓰기 그대로 | §5.1 「예외」 · 호출 이력 이유 · §9 #20 | WP-BE4 |

5줄 · 누락 0. 결정에 없고 코드가 고른 기본값: 카드 방 동률 = ETCETERA 먼저 → 큰 `sequence`(§3.3 · OQ-511) · 카드 방 판정은 작업 상태를 보지 않는다(§3.3) · `open_task_seqs` 는 저장만(§3.2).

### H.2 r4 지시 처분

| 지시 | 처분 | 바뀐 곳 |
|---|---|---|
| 1 카드 방 | type 무관 · 배정 시각 최신 · 동률 규칙 = 코드 `_card_room_task` · 입실도 같은 작업 | §3.3 · §5.1 · §5.4 · OQ-511 |
| 2 규칙 하나 | 위 H.1 #2 · #5 · 0.4.0 줄 취소선 | §5.1 · §5.7 · §5.9 · §5.11 · §6.3 · §6.4 · §6.7 · §7.2 · §7.3 · §9 · §10 · 부록 A · E |
| 3 E2E | #18(방 배정 없이 시술에만 방) · #19(시트팩 = 일반 시술 · 안 끝나면 귀가 대기 불가) · #20(시트팩 호출 뒤에도 남음) · #9 · #13 고침 | §9 |
| 4 SPEC-004 | 앱 무변경 · 갈라진 규칙 = OQ-526 | §10 |
| 5 WORK-005 | WP-BE3 · WP-BE4 · WP-FE3(완료) · 「r4 처분」 | WORK-005 |

## 부록 I. 10-26 결정 반영 (r5 · 2026-10-26)

원천 `orchestration/work/overall-board/_RESUME.md` §2 2026-10-26 줄 3개 · 브리프(planner r5) · 지시 `spec-r5-addendum.md`. 코드(`cc-prototype/overall-board/procedure` · PR #6 상태)는 읽기만 — 이 판의 계약은 코드보다 먼저 간다(구현 = WORK-006).

### I.1 10-26 결정 줄 → 절

| # | 결정 줄(줄임) | SPEC-003 0.5.0 | WORK-006 |
|---|---|---|---|
| 1 | **되돌리기 기능 추가** — [시작] → 시술 대기 · [종료] → 시술 중 · ① 토스트 [되돌리기] ② 시술 줄 아이콘 · 호버 「되돌리기」 · medikit 모달 「시술 대기/시술 중으로 되돌리겠습니까?」 · D-28 뒤집음 | 머리말 · §1.1 · §1.2 · §3.2 · §4.3 · §4.4 · §5.5 · §5.6 · §5.10 · §5.11 · **§5.13** · §6.3(토스트 · 모달) · §6.7 #3 · #23 · §7.2 · §7.3 · §7.4 · §7.5 · §8 · §9 #21 ~ #26 · OQ-529 ~ OQ-532 · 부록 A D-28 | WP-KOS · WP-BE · WP-FE · WP-E2E |
| 2 | **아이콘 위치** = 오른쪽 버튼/배지 왼쪽 — 진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 왼쪽 · 대기 줄 없음 | §5.9 오른쪽 칸 · §5.11 아이콘 두 줄 · §6.3 #5 · §9 #22 · #23 · #25 | WP-FE |
| 3 | **웹이 정본 · 앱은 나중에 웹에 맞춘다** · 되돌리기 KOS 실호출 확인 필수 | 머리말 우선순위 · §5.13 「앱」 · 「KOS 실호출 확인」 · §10 OQ-523 · OQ-526 닫음 · OQ-528 · **§10.1 앱 후속** | 「하지 않는 것」 · **WP-KOS 맨 앞** |

3줄 · 누락 0.

### I.2 브리프 「정할 것」 → 처분

| 정할 것 | 처분 | 절 |
|---|---|---|
| 1 KOS 반영 | [종료] 되돌리기 = `change-tasks-complete {complete:false}`(~~미확인~~ (r6) WP-KOS K2 받음) · [시작] = 지금 KOS 에 보내는 것: 작업 쪽 없음 · 그 고객의 첫 [시작]만 `changeFlowStep(PROCEDURE)`(코드 `service/actions.py` `start`) → [시작] 되돌리기는 고객이 시술 대기로 돌아갈 때만 `changeFlowStep(PROCEDURE_WAITING)`(~~미확인~~ (r6) WP-KOS K4 받음) · 귀가 대기 → 진행은 막음(OQ-531) · 확인 조건 `statusNot` · 대체 규칙 · **WP-KOS 실호출이 완료 조건** · 안 받으면 OQ-529 · OQ-530 | §5.13 · §8 · §10 |
| 2 범위 | 토스트 = 마지막 조작만(5초) · 아이콘 = 아무 때나 · 호출 · 수락 · 담당의 그대로 · 귀가 대기 카드 없음 · ccc [시작] 없는 완료 시술 없음 · 마취 범위 밖 | §5.13 |
| 3 API | `POST /api/procedures/{id}/undo-start` · `/undo-finish`(둘로 나눈 근거) · 409 · 404 · 403 · 역할 세 역할 · `event_log` 두 type · SSE ① · SPEC-004 §3.4 한 줄 | §3.2 · §7.3 · §7.4 · §7.5 · SPEC-004 0.3.2 |
| 4 동시성 | 상태 검사 409(`procedure_not_doing` · `procedure_not_done` · `visit_home`) · 버전 검사 없음(OQ-532) | §5.13 · §9 #24 |
| medikit 모달 | 1.4.0 에 **`ConfirmModal`**(확인 · 좌우 버튼 · `variant`) · `Modal` · `BaseModal` · `Dialog`(Radix) 있음 → `ConfirmModal` 을 쓴다. 툴팁 `Tooltip` · 아이콘 `ResetIcon` 도 있음 — OQ 없음 | §6.3 #5 |
| 토스트 시간 | 5초(기본값 — 되돌리기 토스트만) | §5.13 · §6.3 |

### I.3 기본값 목록(결정에 없어 이 판이 고른 값)

토스트에 모달 없음 · 토스트 5초 · 토스트 문구 · 아이콘 = `ResetIcon` sm · 26px 버튼 · 모달 `variant = caution` · 모달 설명 「<방> · <시술>」 · 아이콘 = 아무 때나 · 귀가 대기 카드 막음 · ccc [시작] 없는 완료 시술 막음 · [종료] 되돌리기 즉시 `kos_status = READY` · 경로 둘 · 버전 검사 없음 · 호출 · 수락 되돌리기 없음 그대로.
(r6 더함 — review-doc r4 W4) · 고객 상태를 시술 대기로 되돌리기(진행 · 완료 0 일 때 · 첫 [시작]의 거울 · §5.13) · 되돌리기 횟수 제한 없음 · 되돌린 뒤 다시 [시작] · [종료] 됨(§5.13) · 새 토스트가 앞 토스트와 그 [되돌리기]를 대체(§5.13) · 마취 되돌리기 범위 밖(§5.13) · 409 새 문구 두 개 「진행 중인 시술이 아니에요」 · 「완료된 시술이 아니에요」(§7.3) · [시작] · [종료] **성공 토스트 신설**과 그 문구(§6.3 — 지금은 성공 토스트가 없다) · 토스트 [되돌리기] 버튼 색 토큰은 FE 가 테마에서 고름(§6.3).
(r6 빠짐) [종료] 되돌리기 즉시 `kos_status = READY` — 기본값이 아니라 WP-KOS K2 로 확정.

## 부록 J. review-doc r4 처분 · WP-KOS 반영 (r6 · 2026-10-26)

원천 `orchestration/work/overall-board/review-doc-r4.md`(FAIL 1 · WARN 6) · `kos-undo-probe-report.md`(K1 ~ K4 끝 · K5 대기) · 지시 `spec-r6-instructions.md`.

| 항목 | 처분 | 바뀐 곳 |
|---|---|---|
| F1 | §8 [귀가 대기] ① = 안 끝난 「방 배정」(`is_room_task`)만 · 「남은 「방 배정」이 없으면 만들지 않음」 · 옛 문장 취소선 · 확인 칸 그대로(코드 `service/actions.py` `home` 과 같음). 코드 `kos_ops.py` `cancel_tasks_op` docstring 낡음은 리뷰가 기록만 — 문서 범위 밖 | SPEC §8 |
| W1 | [시작] 되돌리기 flow-step op = ccc 고객 상태가 `doing` → `waiting` 이 될 때 **항상 1줄** · 400 이면 같은 단계 규칙(다음 조회에서 `confirmed`) · 앞 `PROCEDURE` op 은 `superseded` 로 닫힘 · 시험 줄 고침. 같은 뿌리인 0.2.0 같은 단계 규칙의 「보내기 직전에」도 코드에 맞춰 지움(리뷰 참고) | SPEC §5.10 · §8 · §9 「0.5.0 더함」 · WORK-006 WP-BE |
| W2 | 가짜 보드 `canUndo*` 예시(옛 WP-BE ⑦)를 **WP-FE 로 옮김**(back 파일 `service/fake_board.py` 하나 허용) — FE 가 BE 를 기다리지 않는다 | WORK-006 고정점 아래 문단 · WP-BE · WP-FE · 병렬 |
| W3 | 게이트 = **OQ-529 · OQ-530 만**. OQ-528 은 WP-KOS K5 로 따로(WP-E2E 전까지 · 사용자가 시트팩을 붙이면 진행 · 「안 받음」이면 WORK-005 쪽 사용자 결정) | WORK-006 WP-KOS · 게이트 · 열린 것 · SPEC OQ-528 |
| W4 | I.3 에 빠진 기본값 7개 더함 · `READY` 는 기본값 목록에서 뺌(확정) | SPEC 부록 I.3 |
| W5 | WP-KOS 검증 명령을 실행할 수 있는 grep 으로(UUID · 이메일 · `Bearer` · JWT · 5자리 이상 숫자) · 결과 0 = 완료 조건 | WORK-006 WP-KOS |
| W6 | 머리말 우선순위 줄 끊음 — 「… 「웹이 정본」 줄.」 / 「업무 흐름은 …」 따로 | SPEC 머리말 |
| WP-KOS OQ-529 | **닫음 — 받음**(K2 200 · `DONE → READY` · 22초 뒤에도 `READY`) · §5.13 즉시 값 `READY` 확정 | SPEC §5.10 · §5.13 · §8 · §9 #22 · OQ-529 · I.2 · I.3 |
| WP-KOS OQ-530 | **닫음 — 받음**(K4 200 · `PROCEDURE → PROCEDURE_WAITING`) | SPEC §5.13 · §8 · §9 #21 · OQ-530 · I.2 |
| WP-KOS 화면 | KOS **웹 화면** 표시는 워커가 못 봄 → §9 #21 · #22 KOS 칸에 「웹 화면도 본다」 | SPEC §5.13 · §9 |

FAIL 1 · WARN 6 · WP-KOS 판정 2 — 누락 0. 리뷰 참고의 §6.8 / §6.7 절 순서는 0.2.0 부터의 부채라 이번 판에 옮기지 않는다(한 관심사).
