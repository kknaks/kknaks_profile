---
type: work
id: WORK-003
title: "명동 PoC v2 구현 — 시술 현황판(procedure) · KOS 데모 지점 실연동"
status: done
product: cc-prototype
feature: procedure
work_type: new-feature
owner: kknaks
progress: 100
created_at: 2026-10-21
updated_at: 2026-10-22
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-003-procedure-board|SPEC-003]]"
  works:
    - "[[work-002-cc-nav-reservation|WORK-002]]"
  releases: []
  related: []
---

# 명동 PoC v2 구현 — 시술 현황판

SPEC-003 을 **사용자가 로컬에서 E2E 를 할 수 있는 상태**까지 넣는다. 배포(D-03 — 기존 주소 교체 · `cc/` → `_archive/cc/` · Actions · infra)는 로컬 E2E 통과 뒤 마지막 WP 로 따로.

> **2026-10-22 상태(머지 전 동기화)**: WP1 ~ WP6 완료 · E2E batch 1 수정 반영 · WP7 배포는 WORK-004 WP10 과 **한 번에** 끝났다(2026-10-21 · `ccc.medisolveai.xyz` = procedure). 코드 = `kknaksss/cc-prototype` main `329b543`(#3 `0f4634a` → #4). 남은 것은 「열린 것」.

> 1 파일 = 1 work = **빌드 계획**. 계약은 SPEC-003 을 참조만 한다.

## Meta

- Covers spec: SPEC-003
- 코드 레포: `kknaksss/cc-prototype` — 범위 `procedure/`(WP1 ~ WP6) · 배포 WP7 은 `.github/workflows/` · `cc/` 이동 · infra 레포
- slug: `myeongdong-poc-v2` · 워커: backend · frontend · infra
- 순서 원칙: **계약(SPEC-003 §7 API · §7.5 SSE 스냅샷 모양)을 WP1 에서 코드로 고정** → back(WP2 ~ WP4)과 front(WP5)가 병렬 → 합쳐 E2E(WP6) → 배포(WP7)
- 검증은 WP 마다 그 범위만. 전체 검증 · 로컬 E2E 는 WP6 에서 한 번

## Work Packages

| WP | 내용 | 계약 | 워커 | 범위(경로) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| WP1 | **뼈대 + 계약 고정** — `procedure/` 폴더 · back FastAPI 빈 앱(계층 폴더 · 설정 · 오류 형식 · `/api/health`) · `schemas/`에 §7.2 스냅샷 · §7.3 요청/응답 · §7.5 이벤트 모델 · 가짜 스냅샷 반환하는 `GET /api/board` · `GET /api/board/stream`(첫 접속 스냅샷 1개 + ping) · `.env.example`(이름만) · `docker-compose.yml` · README. front 는 아직 없음 | §2.1 ~ §2.3 · §7 | backend | `procedure/back/**` · `procedure/docker-compose.yml` · `procedure/README.md` | 스냅샷 · 조작 스키마가 코드로 있고 `GET /api/board` · `/stream` 이 가짜 값으로 응답 · `.env.example` 에 값 0 | `cd procedure/back && uv run ruff check . && uv run pytest -q` · `curl -N localhost:8700/api/board/stream?token=…` | 완료 — 코드 #3(`0f4634a`) · backend WP1 ~ 4 보고(38 passed) |
| WP2 | **DB · 로그인 · 도메인 규칙** — §3.2 테이블 전부 · repository · 관리자 로그인(§7.1) · 규칙 계산(§5 — 유효 호출 · 수락 범위 · [시작]/[종료] 조건 · 확인이 필요 · 필터 수 · 원장 목록) · 조작 API(§7.3) → `event_log` + `kos_op`(보내지는 않음) · 조작 뒤 SSE `board` 발행 | §3 · §5 · §7.1 · §7.3 · §7.5 | backend | `procedure/back/app/{repository,domain,service,api}/**` · `tests/` | §5.10 전이 · §5.11 활성 조건 · 409 코드 표 · SSE 발행을 pytest 로(KOS 없이 · 행은 테스트가 넣음) | `uv run pytest -q tests/test_rules.py tests/test_actions.py tests/test_stream.py` | 완료 — 같은 보고 · 리뷰 r1 → fix1(50 passed) · r2 WARN 2 → SPEC 0.2.1 |
| WP3 | **KOS 조회** — 토큰 2종(§4.1) · 조회 루프(일정 10초 · 직원/방 1시간 · 09~21 KST · 4층) · 덮어쓰기 규칙(§4.3) · 카드 조건(§5.1) · `sync_state` · 조회 뒤 SSE 발행 | §4.1 ~ §4.3 · §4.6 · §5.1 | backend | `procedure/back/app/kos/**` · 관련 service | 가짜 KOS 응답(HAR 모양 — **값은 만든 가짜**)으로 upsert · 보호 필드 · 조회 시간 시험 통과. 실 데모 지점에서 서버 1회 기동 → 카드 수 로그 확인(조회만) | `uv run pytest -q tests/test_kos_sync.py` · 실 데모 조회 1회 | 완료 — 실 데모 조회(직원 78 · 방 28 · 원장 4) — 리뷰 r2 |
| WP4 | **KOS 반영** — `kos_op` 대기열(같은 visit 순서) · 보내기 · 확인(`expect`) · 재전송 · 3회 실패 · `kos_failed` 이벤트 · 상태 바뀔 때 SSE | §4.4 · §8 | backend | `procedure/back/app/kos/**` · service | 가짜 KOS 로 순서 · 확인 · 실패 시험 통과. **실 데모 지점 쓰기 1회씩**(호출 · 수락 · flow-step · complete — 데모 일정 하나로) 200 + 다음 조회에서 `confirmed` | `uv run pytest -q tests/test_kos_ops.py` · 실 데모 쓰기 4종 1회 | 완료 — 실 데모 쓰기 4종 · E2E-1(방 넣기) · E2E-3(작업 취소) · E2E-6(바로 이어 보내기 · 1.5초 확인 조회) 반영 |
| WP5 | **front** — 테마 복사(§2.4 · 시안 `medikit-patches.css` 의 `[Button-3]` · `[Badge-1]` 블록 포함) · 로그인 · 헤더 · 사이드바 · 카드(§6.3) · 오른쪽 패널 3탭(§6.4) · 호출 팝오버(§6.5) · SSE 연결(§7.5 — 첫 스냅샷 · 재연결 · version 순서) · 조작 API 호출 · 토스트. WP1 의 가짜 스냅샷으로 먼저 그린다 | §2.4 · §6 · §7 | frontend | `procedure/front/**` | 시안 장면 8개(`board` · `board-placement` · `memo-expanded` · `call-modal` · `call-modal-specific` · `all-done` · `panel-doctors` · `panel-customers`)를 가짜 스냅샷으로 재현 · §6.7 차이 반영 · `cc/` import 0 | `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` · `grep -r "cc/" procedure/front --include=*.ts* ` 0 | 완료 — tsc · lint · build 0 · 장면 8 · fix1 · E2E-5 → E2E-12(카드 높이) · E2E-8 → E2E-9 |
| WP6 | **합치기 · 로컬 E2E** — compose 로 back + front · 실 데모 지점 연결 · SPEC-003 §9 0 ~ 11 단계를 코디가 먼저 한 번 → 사용자 E2E | §9 | backend · frontend(수정) · 코디(진행) | `procedure/**` | 사용자 로컬 E2E 통과(사용자 표면 · 브라우저 2개) · 피드백은 모아서 한 번에 수정 발주 | `cd procedure/back && uv run pytest -q` · `cd procedure/front && npm run build` · `docker compose up --build` | 완료 — 사용자 로컬 E2E batch 1(E2E-1 ~ 12) · 수정 반영(E2E-10 만 기록 — 열린 것) |
| WP7 | **배포**(로컬 E2E 통과 뒤) — `cc/` → `_archive/cc/` · Actions(`cc-*-image.yml` → `procedure-*`) · Dockerfile 포트/이름 · infra 차트 · k8s Secret(KOS 키 · 시스템 계정 · 관리자 계정 · 세션 키 — 값은 Secret 에만) · 기존 주소 `ccc.medisolveai.xyz` 교체 · SSE 가 ingress 에서 버퍼링 안 되게 | D-03 · D-05 · §7.5 | infra · backend(이미지) | `.github/workflows/**` · `procedure/*/Dockerfile` · `_archive/cc/` · infra 레포 | 배포 주소에서 로그인 · 카드 · SSE 갱신 확인(사용자 표면) | Actions 빌드 성공 · 배포 주소 E2E 축약(§9 1 · 3 · 4 · 6 · 9) | 완료 — **WORK-004 WP10 으로 수행**(2026-10-21 · infra #22 ~ #24) |

## 병렬

```text
WP1 ──┬─ WP2 ── WP3 ── WP4 ──┐
      └─ WP5 ────────────────┴─ WP6 ── WP7
```

- WP2 ~ WP4 는 같은 back 이라 차례로(한 워커). WP5 는 WP1 이 끝나면 바로 — 스냅샷 모양이 고정돼 있어 back 을 기다리지 않는다
- 스냅샷 모양을 바꿔야 하면 SPEC-003 §7 을 먼저 고친다(코디 → planner) → 양쪽 다시 맞춤

## 주의

- public 레포(코드 · 문서 모두) — KOS 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · KOS id 값을 코드 · 시험 데이터 · 커밋에 넣지 않는다. 시험의 KOS 응답은 모양만 맞춘 가짜 값
- 운영 명동점 키 금지(D-06). 실 쓰기는 데모 지점 · 데모 일정에만
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 사용자 프로세스를 죽이지 않는다
- 백엔드 커밋 뒤 compose 를 다시 올리고 E2E(옛 코드가 떠 있는 채로 확인 금지)

## 운영 도구 (2026-10-22)

- **KOS 데모 고객 채우기** — 코드 레포 스킬 `.claude/skills/kos-demo-patients/` + 스크립트 `procedure/tools/kos_demo_patients.py`(`create` · `list` · `delete --date`) — 데모 테넌트에서만(데모 표식 계정이 없으면 멈춤) · 예약 메모 `[ccc 데모 <날짜>]` 로 만든 것만 보고 지운다 · 가상 이름 · 연락처 없음 · 키/토큰 출력 없음. 한계: 공개 API 로는 **예약까지만**(재내원 · 접수 · 수납 · 시술 작업 · 방 배정은 KOS 화면). **코드 PR #5(OPEN · 2026-10-22 — 스킬 · 스크립트 · `procedure/README.md` · 앱 빌드 번호 3)로 올라가 있다 · main 머지 전**. 검증(PR 본문): `list 2026-10-22` → 190건 · `create --dry-run` · ruff. 실행 기록 = `orchestration/work/myeongdong-poc-v2/demo-patients-2026-10-22.md`(190건)

## 열린 것 (2026-10-22)

| 무엇 | 지금 | 근거 |
|---|---|---|
| 웹 카드 `kind = etc` 줄 숨기기 | 기록만 · 다음 수정 batch | E2E-10 · SPEC-003 OQ-517 |
| 웹 로그인 역할 제한(결정 「웹 = 관리자」 vs 코드 제한 없음) | 결정 필요 | SPEC-003 OQ-518 |
| 데모 표식 계정(`KOS-DEMO`)을 원장 목록에서 뺄지 | 빼려면 `KOS_EXCLUDE_ACCOUNT_IDS`(env) | SPEC-003 OQ-519 |
| 데모 준비 — 공개 API 에 재내원 · 접수 · 수납(시술 작업) · 방 배정 없음 | 카드로 쓸 고객은 KOS 화면에서 접수 → 수납 → 시술 대기 + 방 배정 | `demo-patients-2026-10-22.md` |
| `call-tasks-doctors` 재호출 · [다른 원장에게] 400 여부 | 실 데모 기록 없음 | SPEC-003 OQ-516 |
| DEC-005 OQ-501 ~ 503(지정 호출 KOS 본문 · 시술권 · 내부 API 변경) | 그대로 열림 — 코드는 지정 호출도 「모든 의사」와 같은 요청 | DEC-005 · 코드 `domain/kos_ops.py` |
