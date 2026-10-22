---
type: spec
id: SPEC-001
title: "cc PoC — 데스크 현황판 · 직원 페이지 · 통역 계약"
status: draft
product: cc-prototype
feature: cc
version: 0.3.0
created_at: 2026-10-13
updated_at: 2026-10-13
tags:
  - product/cc-prototype
  - feature/cc
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-002-sts-idea|BASE-002]]"
    - "[[baseline-003-cc-idea|BASE-003]]"
  decisions:
    - "[[decision-001-feature-lab|DEC-001]]"
    - "[[decision-002-cc-poc|DEC-002]]"
  specs: []
  works: []
  releases: []
  related: []
---

# cc PoC — 데스크 현황판 · 직원 페이지 · 통역 계약

`cc/back`(FastAPI) · `cc/front`(Next.js) 가 지킬 계약. **업무 흐름의 정본은 `workflow-v1.md`**(프로필 레포 `reference/2026-10-12-cc-prototype/workflow-v1.md`) — 이 문서는 그 흐름을 화면 · 상태 · API 로 옮긴 것이다. 둘이 다르면 workflow-v1.md 가 이긴다.

## 0-b. 0.3.0 — E2E 2차 반영 (2026-10-13)

근거 · 원문: `orchestration/work/sts-prototype/e2e-feedback-batch-2.md` #1~#26 · workflow-v1.md 「동선이 메인 데이터」 「메모 원칙」. **이 절이 앞 절과 다르면 이 절이 이긴다.**

**원칙**
- **동선이 메인 데이터.** 화면의 「오늘 오더」 = 동선(시술 · 순서 · 담당 · 상태). 메모는 참고용 원문(#18 #20)
- **메모 양식에 기대지 않는다 — 원문 그대로**(#25). 잘라 읽기 · 뽑기 전부 삭제: ⚠ 주의 뽑기 · 상담/오더 사본 나누기 · 메모 속 아웃 시각 · 예약 메모 희망 시술 칸 · 빈 양식 줄 숨김 · 타 병원 이력 줄. 구조화된 값은 KOS 구조 필드만(아웃 = `desiredDischargeDateTimeUtc`, 예약 시술 = `requestedProcedures` — 비면 안 보임)
- **강조만**(#25 · #11): 원문에서 **위험 단어**(설정 목록 — 기본: 임플란트 · 아스피린 · 수면 · 알레르기 · 켈로이드 · 임신 · 지정 · 거부)와 **오늘 근무 직원 이름**을 강조. 목록은 back 설정(`CC_RISK_WORDS` 또는 설정 파일)
- **메모 공개 = 쓰인 시점**(#15): 과거 방문 메모 · 시술 이력 · 보유 시술권 · 고객 메모 = 언제나 / 오늘 예약 메모 = 예약 때부터 / 오늘 상담 · 오늘 오더 = 오늘 상담 종료 뒤 / 오늘 담당자 메모 = 히스토리에만(#17)
- **화면에 설명 문구 · 내부 용어 없음**(#21 — 「(고르면 …)」 · 「↑↓ 로 …」 · 「KOS 순번」 등)

**데이터 · 동작(back)**
1. **방문 카드**(#4 #26): 고객마다 `visits[]` = 방문(일정) 하나당 카드 — 날짜 · 상담사 · **상담 내용 원문 전체** · 오더 메모 원문 · 그날 시술 · 담당자 메모. 오늘 카드는 공개 시점 적용, 지난 카드는 언제나. 최근이 위
2. **상담 종료 이벤트 = 후보만**(#19 #23): 상담 종료 때 들어온 결제 시술은 동선에 붙이지 않고 **「오늘 시술 후보」**. 미결제 금액 · [결제 완료] 는 그대로. 원장 상담(ETCETERA)은 동선에 이미 원장 상담이 있으면 후보에서 뺀다
3. **시술 후보 = 묶음 단위 n/m**(#1): 보유 시술권 · 오늘 결제분을 시술권 묶음(세트) 한 줄로 — `{name, left, total}`. 고르면 **1회 차감**(그 묶음의 다음 AVAILABLE 1장을 단계에 연결). 같은 묶음을 또 고르면 또 1장
4. **노쇼**(#14): `POST /api/desk/no-show {scheduleId}` — 예약 st `noshow`. 주석 = KOS 공개 없음(예약 상태)
5. **지정 직원**(#11): 고객마다 `mentionedStaffIds[]` = 고객 · 예약 · 오늘/지난 상담 · 오더 메모 원문에 이름이 그대로 나오는 오늘 근무 직원(문자열 일치)
6. 응답에서 빼는 것: `cautions`(뽑기) · 메모에서 뽑은 `outTime` · 예약 행 `procedure`/`doctor`(KOS 칸 비면 빈 값 그대로) · 동선 단계의 담당자 메모

**화면(front · 시안 r5)**
7. **방 패널 2열**(#9 #10 #20 #22): 왼쪽 = **동선 · 작업**(강조된 ⚠/지정 요약 줄 · 단계 줄마다 **셀렉터 `[미배정 ▾]`** — 고르면 배정, 「미배정」 고르면 해제, 지정 직원 맨 위 · [배정]/[해제] 버튼 없음(#12) · ↑↓ · 오늘 시술 후보 칩(묶음 n/m) · 미결제 [결제 완료] · 수면시술실 · 귀가) / 오른쪽 = **메모**(오늘: 접수 메모 · 오늘 상담 내용 · 오늘 오더 원문 / 히스토리: 지난 방문 카드 · 보유 시술권 n/m). 아래로 펼쳐지는 직원 목록 없음(#5)
8. **귀가 = 확인 모달**(#6): 남은 단계 목록을 「진행 안 함」 으로 보여 주기
9. **예약 탭**(#7 #13 #14 #2): 카드 = `시간 · 이름 · [첫 방문/재내원] · [접수]` 한 줄, 지연 표시 없음. 목록 = 접수 전 · 귀가 · 노쇼만(내원 중 고객은 현황 탭). **카드 클릭 = 예약 상세**: 예약 정보 · 예약 메모 · 고객 메모 원문(강조) · 지난 방문 카드 · 보유 시술권 n/m · [접수] · [노쇼]. 오늘 상담 · 오더 칸 없음
10. 범례 「손 필요」 → **「확인 필요」**(#3)
11. 직원 화면: **로그아웃**(#8) · 상담사 화면엔 오늘 오더 없음(#16) · 「상담 요약」 → **「상담 내용」 원문 전체**(#24) · 방문 카드
12. 접수 모달의 시술 후보도 묶음 n/m · 1회(#1)

## 0-a. 0.2.1 덧붙임 (2026-10-13 — WP7 뒤)

- **데이터 = 목데이터 시드 + 고객별 이벤트**(workflow-v1.md 「PoC 범위」). §6 시드 build 는 캡처를 직접 읽는 대신 **시나리오 파일**(`cc/back/data/scenario/`: `seed.json` + `events/<scheduleId>.json`)을 읽는다. 시나리오는 실데이터 대본에서 만든다(researcher)
- **상담 완료 이벤트**: 상담 단계 [종료] 때 그 고객 이벤트의 상담 기록 · 오더 메모 · **상담사가 넣은 시술**(단계로 추가, `paymentRequired=true` · 「수납필요」) · 결제 금액을 넣는다. 데스크는 확인 · 순서 · 배정
- **[결제 완료]**(방 패널, 미결제 금액 옆, 데스크): 수납필요 해제 · 미결제 0 · 시술권(`ticketId`) 연결. 주석 = 「KOS 결제 조회(공식 `getPurchaseSummariesByVisitor` · `getTicketBundlesQuery`)」
- **시술 완료 이벤트**: 시술 [종료] 때 그 작업의 담당자 메모(있으면)
- 차트 「오늘 결제」 = [결제 완료] 뒤에만
- 재내원 시나리오는 시드에 직접 만든다(보유 시술권 · 이전 상담 기록)

## 0. 0.1.0 → 0.2.0 바뀐 것

E2E 피드백(`orchestration/work/sts-prototype/e2e-feedback-batch-1.md` #1~#21)과 워크플로 정리 결과.

| 영역 | 0.1.0 | 0.2.0 |
|---|---|---|
| 배정 모델 | 직원 큐(시안 `queue`) — 배정 = 곧 방에 있음 | **동선 단계 단위 배정.** 배정 = 대기, 시작 · 종료 = 그 직원 본인 화면 |
| 동선 | KOS 작업에서 재구성 · 원장 진료 · 진정 자동 끼움 | **데스크가 넣은 단계만.** 자동 단계 없음 |
| 시드 | 10-09 14:45 재구성(추정) | **개원 전**(아무도 접수 안 함) |
| 직군 | 의사 · 상담사 · 코디(추정) | KOS `getAccounts` 5직군: 의사 · 상담사 · 피부관리사 · 간호사 · 코디 |
| 직원 화면 | 의사 · 코디 | 배정형(의사 · 상담사 · 피부관리사) · 순회형(코디 · 간호사) |
| 방 패널 | 직원 중심 | **고객 중심**(단계마다 [배정] · 순서 바꾸기) |
| 메모 | 처음부터 다 보임 · 작성자 추정 | 진행에 맞춰 공개 · 작성자 이름 없음 |
| KOS | 언급만 | 조작마다 `kos api 연동 필요` 주석(호출 없음) |
| 이름 | 라운지 · 수면실 | **접수대기실 · 수면시술실** |

## 1. 범위

- In: 로그인 · 데스크 페이지(현황판) · 직원 페이지(5직군, 틀 2개) · 환자 상세 · 통역 모달 · 시드 · 초기화 · 「이걸 시드로」
- Out: **KOS 호출(어떤 것도)** · 결제(KOS 에서 함) · 차티 연동 · 배포 · PWA · 비밀번호 검증 · 메모 작성 · 수정 · 코디/간호사 폰에서 배정
- 실행: 로컬만. 노트북 브라우저 `http://localhost:3600`

## 2. 원칙 (workflow-v1.md)

1. **자동은 없다.** 고객 이동 · 단계 추가 · 배정은 사람이 누른다
2. **배정 = 데스크**(현황판). **시작 · 종료 = 그 직원 본인 화면**(의사 · 상담사 · 피부관리사)
3. **KOS 필드 그대로.** 없는 정보는 비운다(「-」 또는 숨김). 다른 필드로 짐작하지 않는다
4. **가짜는 고객 이름뿐**(메모 본문 속 고객 · 동행인 이름 포함, DEC-002 D-09)
5. **동선 정본 = 관제 DB.** 각 단계에 KOS 작업 `sequence` · `ticketId` 를 같이 저장(있을 때)
6. 조작마다 KOS 반영 자리에 주석만(§9)

## 3. 화면

claude design `dda9a931-097f-4780-9301-972d5ac1fc23`. **시안 수정본(r4)이 나오면 그것이 화면 정본**이다. r4 전에는 기존 시안 + 이 절의 변경.

| 경로 | 화면 | 시안 | 0.2.0 변경 |
|---|---|---|---|
| `/login` | 로그인 | `직원 - 로그인` | 계정 = 데스크 + 10-09 직원(5직군) |
| `/desk` | 현황판 | `현황판 v3` | 범례 5직군 · 「라운지」→**접수대기실** · 「수면실」→**수면시술실** · 방 패널 고객 중심(§3.2) · 접수 모달(§3.1) · 예약 탭 첫 방문 배지 · [초기화] |
| `/staff` | 직원 첫 화면 | `직원 - 의사` · `- 코디` | 배정형 / 순회형(§3.3) |
| `/staff/patient/[scheduleId]` | 환자 상세 | 같은 두 파일 | 버튼 · 메모 공개 시점(§3.4) |
| (모달) | 통역 | `직원 - 통역 모달 상태` | 변경 없음(§8) |

### 3.1 접수 모달 (데스크)

- 예약 행 [접수] → 모달. 첫 방문 배지(`visitor.isNew`)
- **동선 단계를 데스크가 고른다** — 자동으로 끼우는 단계 없음
  - 첫 방문: 기본 체크 = 「상담」 하나
  - 재내원: 기본 체크 = 보유 시술권(§5.4 후보) 전부 + 「상담」 · 「원장 상담」은 데스크가 추가
  - 고를 수 있는 것: 상담 · 원장 상담 · 시술 후보(§5.4)
- [접수] → 고객 = **접수대기실**, 단계 전부 「예정」

### 3.2 방 패널 (고객 중심)

방을 누르면:
- 비어 있으면: 접수대기실 고객 목록 → 골라서 이 방에 넣기(시안 동작)
- 고객이 있으면:
  - 머리: 방 이름 · 고객(가짜 이름 · 첫 방문/재내원 · 국적) · 지금 상태 · 경과
  - **동선 단계 목록** — 한 줄 = 단계 하나(시술은 시술권 1장 = 한 줄, 묶지 않음): 번호 · 이름 · 배정 직원 · 상태(예정 · 대기 · 진행 중 · 완료 · 진행 안 함) · 시각
  - 단계마다 **[배정]** → 그 단계에 맞는 직원 목록(상담 → 상담사 · 원장 상담 → 의사 · 시술 → 의사 또는 피부관리사). 목록에 각 직원의 지금 일(방 · 단계) 표시. 배정된 단계는 [해제]
  - **[시술 추가]** → §5.4 후보에서 고르기(뒤에 붙음)
  - **순서 바꾸기** — 진행 중인 단계가 없을 때만(방이 대기 상태) 예정 · 대기 단계의 순서를 위아래로
  - **[수면시술실로 이동]** · 수면시술실에서 **[원래 방으로]**(원래 방은 계속 점유 — 시안 `prev` 동작)
  - **[귀가]** (§5.3 귀가)

### 3.3 직원 첫 화면

| 틀 | 직군 | 보여 주는 것 |
|---|---|---|
| **배정형**(시안 `직원 - 의사`) | 의사 · 상담사 · 피부관리사 | 「지금 진행 중」(내가 진행 중인 단계) · 「다음」(나에게 배정됐고 아직 시작 안 한 단계, 배정 순) · 「완료」(내가 끝낸 단계). **예정 없음** |
| **순회형**(시안 `직원 - 코디`) | 코디 · 간호사 | 지금 내원 고객 목록(접수 후 귀가 전): 위치 · 상태 · 경과 · 국적 · **오늘 시술 목록**(간호사 준비용). **손 필요 표시**: 「다음 단계 대기」(앞 단계 끝, 다음 단계 미배정) · 「귀가 대기」(모든 단계 끝) |

### 3.4 환자 상세

- 구성은 0.1.0 §5.5(안 A) 그대로 + 아래 변경
- **버튼**(배정형만, 나에게 배정된 단계가 있을 때): 그 단계 종류에 따라 [상담 시작]/[상담 종료] · [시술 시작]/[시술 종료]. 순회형은 [통역]만. KR 이면 [통역] 숨김
- **메모 공개 시점**
  - 예약 메모 · 고객 메모: 처음부터
  - 상담 메모(상담 요약) · 오더 메모(오늘 오더) · 거기서 온 ⚠ 주의: **상담 단계 「완료」 뒤.** 상담 단계가 없는 고객(재내원 등)은 처음부터
  - 담당자 메모: 그 시술 단계 「완료」 뒤, 동선의 그 줄에
- **작성자 이름 없음** — 출처는 칸 이름만(「오더 메모」 · 「상담 메모」 · 「예약 메모」)
- 시술 이력: 「첫 방문」(`isNew`) + 상담 메모의 타 병원 이력 줄. 「이전 시술 기록 없음」 문구 없음
- `**…**` 는 굵게 표시(기호 안 보임) · 값 없는 양식 줄(「고민:」 처럼 콜론 뒤가 빈 줄)은 숨김

## 4. 데이터

| 원천 | 쓰임 |
|---|---|
| KOS 캡처 `CC_CAPTURE_DIR`(10-09) | 예약 · 고객 · 메모 · 시술 작업 · 시술권 · 결제 품목 |
| `cc/back/data/kos-staff.json`(KOS `getAccounts` 응답, 2026-10-13 1회 조회 · gitignore) | 직원 · 직군 |
| 방 대응표(`room-map-provisional.md`) | KOS 방 → 현황판 칸(참고용 — 0.2.0 은 동선을 새로 만들므로 시드에선 안 씀) |

- **직군**: `roleTags` → DOCTOR = 의사 · COUNSELOR = 상담사 · SKINCARE = 피부관리사 · NURSE = 간호사 · COORDINATOR = 코디. 태그가 여럿이면 ① 그날 일정에서 그 사람이 나온 칸(작업 의사 → 의사 · 상담 기록 상담사 → 상담사 · 작업 담당 → 그 사람 태그 중 NURSE/SKINCARE · 기타 업무 → 코디) ② 그래도 여럿이면 DOCTOR > COUNSELOR > SKINCARE > NURSE > COORDINATOR. 이름 「마취용」 제외. 직원 목록 = 10-09 일정에 나온 사람
- 응답에 이메일 · 실제 고객 이름 · 전화 · 차트번호 · 생년월일 없음(나이는 계산값)

## 5. 상태 · 동작

### 5.1 상태 모델 (관제 DB — 동선 정본)

```text
customer: { scheduleId, name(가짜), isNew, nationality,
            location: null | "reception"(접수대기실) | roomId, prevRoom: roomId|null(수면시술실 이동 때),
            flowStep: RESERVED|RECEPTION|CONSULTATION_WAITING|CONSULTATION|PROCEDURE_WAITING|PROCEDURE|PROCEDURE_DONE|COMPLETED,
            receptionAt, completedAt }
step:     { stepId, scheduleId, order(관제 순서), kind: consult|doctor_consult|procedure,
            label, kosSequence|null, ticketId|null, assigneeId|null,
            state: planned|assigned|in_progress|done|skipped,
            assignedAt, startedAt, endedAt }
log:      모든 조작 1줄(누가 · 무엇 · 언제) — 「진행 안 함」 근거
version:  int
```

- 방 상태(현황판 칸): 고객 없음 → 빈 방 / 진행 중 단계 있음 → 그 단계 종류(상담 · 시술) / 배정됐고 시작 전 → 「○○ 대기」(배정 직원 이름) / 앞 단계 끝 · 다음 단계 미배정 → **「다음 단계 대기」**(원장 상담 직후 시술이면 「원장 대기 · 세팅 준비」) / 모든 단계 끝 → 「귀가 대기」
- 경과 타이머 = 지금 상태가 시작된 시각부터
- `flowStep`(KOS 단계)은 조작에 따라 바뀐다(§9 표). 화면 표시에 쓰고, KOS 반영 주석의 근거가 된다

### 5.2 읽기 API

| API | 응답 |
|---|---|
| `GET /api/board` | 방 칸(시안 LAYOUT, 이름 변경 반영) · 고객 · 각 고객 단계 · 직원(5직군 · 지금 일) · 예약 목록 · version |
| `GET /api/staff` | 로그인 목록(데스크 + 직원: 이름 · 직군 · 틀) |
| `GET /api/staff/{staffId}/home` | 배정형: current · next[] · done[] / 순회형: 내원 목록(손 필요 표시 · 오늘 시술) |
| `GET /api/patients/{scheduleId}` | 환자 상세(§3.4 — 공개 시점 적용된 메모) |
| `GET /api/patients/{scheduleId}/procedure-candidates` | 시술 후보(§5.4) |
| `GET /api/events` | SSE `state` `{version}` — 받으면 자기 GET 재호출 |

### 5.3 조작 API — `POST`, 응답 `{version}`, 성공 시 SSE · log

| API | 누가 | 동작 | 막는 조건(400) |
|---|---|---|---|
| `/api/desk/check-in` `{scheduleId, steps:[{kind, ticketId?, kosSequence?, label}]}` | 데스크 | 고객 → 접수대기실, 단계 생성(전부 planned), flowStep RECEPTION | 이미 접수 |
| `/api/desk/place` `{scheduleId, room}` | 데스크 | 접수대기실 → 방. flowStep CONSULTATION_WAITING(상담 단계가 있으면) | 방 정원 초과 · 다른 고객 prevRoom 으로 잡힌 방 |
| `/api/desk/move-sleep` `{scheduleId, room}` / `/api/desk/return-room` `{scheduleId}` | 데스크 | 수면시술실 이동(prevRoom 유지) / 원래 방으로 | 수면시술실 아님 · 빈 칸 없음 |
| `/api/desk/assign` `{stepId, staffId}` | 데스크 | 단계에 직원 → assigned | 직군이 단계에 안 맞음 · 이미 진행/완료 |
| `/api/desk/unassign` `{stepId}` | 데스크 | assigned → planned | 진행 중 이후 |
| `/api/desk/add-procedures` `{scheduleId, items:[{ticketId?, kosSequence?, label}]}` | 데스크 | 시술 단계 추가(뒤에) | 같은 ticketId 중복 |
| `/api/desk/reorder` `{scheduleId, stepIds:[...]}` | 데스크 | planned · assigned 단계 순서 바꾸기 | 진행 중인 단계가 있음 · 완료 단계 위치 바뀜 |
| `/api/staff/{staffId}/start` `{stepId}` | 본인 | assigned → in_progress, flowStep CONSULTATION / PROCEDURE | 내 배정 아님 · 같은 고객에 진행 중 단계 있음 |
| `/api/staff/{staffId}/finish` `{stepId}` | 본인 | in_progress → done. 다음 단계 없으면 flowStep PROCEDURE_DONE, 원장 상담 끝이면 PROCEDURE_WAITING | 진행 중 아님 |
| `/api/desk/discharge` `{scheduleId}` | 데스크 | 남은 단계 → **skipped(진행 안 함)**, 방 비움(prevRoom 포함), flowStep COMPLETED | 진행 중 단계 있음 |
| `/api/desk/undo` `{version}` | 데스크 | 마지막 조작 되돌리기 | |
| `/api/admin/reset` | 데스크 | 시드로 | |

간호사는 PoC 에서 순회형 화면만(배정 · 순서 바꾸기는 현황판에서 — 데스크 계정).

### 5.4 시술 후보 (시술 추가 · 재내원 접수)

KOS 캡처에서 그 고객의:
1. 10-09 일정의 **시술 작업**(`tasks[]` PROCEDURE) — `ticketId` · `title` · `sequence` (그날 결제로 생긴 시술권)
2. 10-09 일정의 「방 점유/원장 상담」 작업(ETCETERA) — 원장 상담 단계 후보(`sequence`)
3. **보유 시술권**(`getTicketBundlesQuery` AVAILABLE 장) — 1과 `ticketId` 가 겹치면 하나로

이미 동선에 들어간 `ticketId` 는 빼고 보여 준다. 결제는 관제에서 일어나지 않으므로 후보는 처음부터 보인다.

## 6. 시드 · 초기화

- `uv run python -m app.seed build --date 2026-10-09` → **개원 전 상태**: 그날 예약 전부(booked/canceled), 접수 · 위치 · 단계 · 로그 없음
- `seed save` · `POST /api/admin/reset` 은 0.1.0 과 같음(「이걸 시드로」 = 코디네이터가 save)

## 7. 로그인

0.1.0 §6 그대로. 계정 목록 = 데스크 + 직원(§4). 시연 계정 카드: 데스크 · 의사 · 상담사 · 피부관리사 · 간호사 각 1명.

## 8. 통역

0.1.0 §7 · `interpret-ws-contract.md` 그대로(구현 완료).

## 9. KOS 반영 주석 (호출 없음)

조작 함수마다 아래 꼴의 주석을 넣는다. **호출 코드 없음.** 출처: workflow-v1.md 「KOS 반영 표」 · HAR 리포트.

```text
## ============kos api 연동 필요 ========================
## <공식: operationId> | <비공식: 내부 경로> | <공개 없음 — KOS 요청>
## ======================================================
```

| 조작 | 주석에 적을 것 |
|---|---|
| check-in | 공식 `changeFlowStep`(RECEPTION) |
| place | 공식 `changeFlowStep`(CONSULTATION_WAITING) · 방: 공개 없음 — KOS 요청(KOS 화면 「방」) |
| assign(상담 단계) | 비공식 `consultation/v1/commands/create-consultation`(counselorIds) |
| assign(원장 상담) | 비공식 `consultation/v1/commands/change-consultation-doctors` |
| assign(시술 — 의사) | 비공식 `schedule/flow/v1/commands/change-tasks-doctors` `{scheduleId, sequences[], doctorIds[]}` |
| assign(시술 — 피부관리사) | 비공식 `schedule/flow/v1/commands/change-tasks-assignees` |
| add-procedures | 공개 없음 · 내부 미확인 — KOS 요청(시술 추가) |
| reorder | 공개 없음 · 내부 미확인 — KOS 요청(우선순위) |
| start(상담) / start(시술) | 공식 `changeFlowStep`(CONSULTATION / PROCEDURE) |
| finish(시술) | 비공식 `schedule/flow/v1/commands/change-tasks-complete` `{scheduleId, sequences[], complete:true}` — 시술권 차감 미확인 |
| finish(상담) | 공식 `updateScheduleConsultationInfo`(차티 기록 → 상담 메모) |
| discharge | 비공식 `schedule/v1/commands/cancel-flow-tasks` `{scheduleId, sequences[], reason:"CANCEL"}` → 공식 `changeFlowStep`(PROCEDURE_DONE → COMPLETED) |

## 10. 실행 · 환경

0.1.0 그대로(back 8600 · front 3600 · `.env.example` · CORS). 추가: `CC_KOS_STAFF_PATH=data/kos-staff.json`.

## 11. 수락 기준

1. `seed build --date 2026-10-09` → 현황판에 예약 목록만, 방 · 접수대기실 비어 있음. 응답 어디에도 실제 고객 이름 · 이메일 · 전화 · 차트번호 · 생년월일 없음
2. 첫 방문 고객: 접수(상담 체크) → 접수대기실 → 방에 넣기 → 상담 단계에 상담사 배정 → **상담사 화면 「다음」에 뜸** → 상담 시작 · 종료 → 환자 상세에 상담 · 오더 메모가 이때 열림
3. 시술 추가(후보에서 3개) → 순서 바꾸기 → 시술1 에 의사 A 배정 → 의사 A 시작 · 종료 → 방 「다음 단계 대기」 · 순회형 화면 손 필요 표시 → 시술2 에 피부관리사 배정 → 시작 · 종료
4. 수면시술실 이동 → 원래 방이 다른 고객에게 막힘 → 원래 방으로
5. 중간 귀가 → 남은 단계 「진행 안 함」 · 방 비움 · 로그에 남음
6. 재내원 고객 접수 → 보유 시술권이 기본 체크
7. 5직군 로그인 각각 맞는 틀 · 버튼. 배정 안 된 직원은 시작 버튼 없음
8. 조작 함수마다 §9 주석, KOS 호출 코드 0
9. back `pytest` · `ruff` / front `tsc` · `lint` · `build`
