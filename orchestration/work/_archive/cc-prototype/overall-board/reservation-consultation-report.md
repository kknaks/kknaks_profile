# 상담 구간 — KOS 에서 실제로 일어나는 순서 (HAR 해석 · 조회)

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-move-cancel-report.md`(`MC§`)에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/상담.har` (gitignore · 항목 58개 · 06:21:08.8Z ~ 06:21:56.7Z)
  - KOS 예약 화면 JS `reservation-client_v0.0.540`
  - 공개 스펙 openapi.yaml 1.0.1
- **KOS 쓰기 0건.** 조회는 데모 테넌트에서만 했다(스크립트 `assert`, 쓰기 허가 목록은 비워 두었다). 운영 키 0건
- 대상 일정: 앞 판 `예약취소/부도.har` 가 다룬 **그 일정**이다. 신규 고객 · 오늘 18:30 KST. HAR 맨 앞 조회에서 `RESERVED` · **`NO_SHOW`** 였다
- 표기
  - **확인**: HAR · 데모 조회로 본 것
  - **JS**: 웹앱 코드
  - **스펙**: openapi.yaml
  - **추정**: 해석
- 리포트에 id · 이름 · 상담 내용은 적지 않았다

---

## 0. 결론

- **KOS 상담 구간은 쓰기 5번이다**(모두 고객 상세 화면)

  | 순서 | 쓰기 | 본문 | 결과 |
  |---|---|---|---|
  | ① | `schedule/v1/commands/recept` | `{scheduleId}` | 접수. **부도(`NO_SHOW`) 일정이었는데도 받았다** → 예약 상태 `IN_PROGRESS` |
  | ② | `schedule/v1/commands/change-flow-step` | `{id, step:"CONSULTATION_WAITING"}` | **상담 대기** |
  | ③ | `schedule/reservation/v2/commands/update-reservation` | `{scheduleId, counselor:{id, name}}` | **예약의 「희망 상담사」(`reservation.counselor`)를 정한다** = 상담사 배정 |
  | ④ | **`consultation/v1/commands/create-consultation`** | `{consultationId(화면이 만든 uuid), visitorId, scheduleId, consultationStartedDateTimeUtc, content{text}, counselorIds[1], doctorIds[1]}` | **상담 기록 1건**(`consultations[]`)이 생긴다. 상담사 · 상담 의사 · 내용이 여기에 남는다 |
  | ⑤ | `schedule/v1/commands/change-flow-step` | `{id, step:"CONSULTATION"}` | **상담 진행** |

- **「상담 완료」라는 상태는 KOS 에 없다**(스펙 · 응답 · JS)
  - flowStep enum 은 `CONSULTATION_WAITING → CONSULTATION → PROCEDURE_WAITING …` 이고 「상담 완료」 단계가 없다
  - 상담 기록에도 종료 시각 · 상태 필드가 없다(`consultationStartedDateTimeUtc` 뿐)
  - 「끝났다」에 가까운 값은 둘이다
    - (a) **다음 단계(`PROCEDURE_WAITING` 등)로 넘어감**
    - (b) 상담 기록의 **`result`(상담 결과 코드)** — 선택 값이다. 데모 코드 8개: 시술 확정 · 당일 시술 · 예약금 결제 · 고민 후 결정 · 재상담 필요 · 가격 문의 · 타원 비교 중 · 시술 보류
  - 이번 HAR 에서는 결과를 넣지 않았다
  - **이번 HAR 은 `CONSULTATION` 에서 끝난다.** 사용자가 말한 「시술 대기로 넘김」 호출은 이 HAR 에 없다
- **상담사 「배정」은 세 곳에 남는다**(데모에서 셋이 같은 계정으로 확인)
  - `reservation.counselor` ← ③
  - `consultations[].counselors[]` ← ④
  - 일정의 요약 `consultation{counselor, doctor, consultationMemo}`
    - `consultationMemo` 는 ④의 상담 내용과 같다
    - `doctor` 는 ④의 상담 의사와 같다(확인)
- **공개 짝**: ①은 `changeFlowStep(RECEPTION)`(RT§2.3: 결과가 같다) · ② · ⑤는 `changeFlowStep`. ③의 상담사 지정과 ④의 상담 기록 만들기는 **공개 없음**. 공개 상담 쓰기는 `updateScheduleConsultationInfo{scheduleId, consultationMemo}`(상담 메모만) 하나다
- 정할 것은 **10개**다(Q-92 ~ Q-101)

---

## 1. HAR 인벤토리

항목 58개 = KOS API 33 + OPTIONS 9 + Datadog 14 + Amplitude 2.

KOS API 33건은 모두 POST · `api.kos-solution.com/tenants/{tenantId}/…` 다. `kos-client-uri` 는 W1 ~ W4 까지 고객 상세 **예약** 탭(`tab=reservation`), #45 부터 **상담** 탭(`tab=consultation`)이다. 아래는 33건 전부다.

| 단계 | 시각(Z) | # | 경로 | 본문 키 | 응답 모양 | 화면 동작(추정) |
|---|---|---|---|---|---|---|
| P0 | 21:08.8 | 0 | `role/v2/queries/get-roles` | — | (15) | 고객 상세 열림 |
| | | 1 | `schedule/group/v1/queries/get-reservation-group` | `id` | `data{그룹}` | |
| | | 2 | `procedure-menu/visitors/queries/get-visitors` | `sort` | (0) | |
| | | 3 | `schedule/v1/queries/get-schedule-summaries` | `visitorId · sort` | 대상: **`RESERVED` · `NO_SHOW`** · `consultation{}` · `consultations[]` 0 | 상담 전 상태 |
| **W1** | 21:08.9 | **4** | **`schedule/v1/commands/recept`** | `scheduleId` | `{}` | [접수] |
| P1 | 21:09.2 ~ 09.7 | 6 | `meta/codes/v1/queries/get-codes` | `CONSULTATION_RESULT` | (8) | 상담 결과 코드 |
| | | 8 | `account/v2/queries/get-accounts-last-update…` | — | | |
| | | 10 · 12 | `get-reservation-group` | `id` | | |
| **W2** | 21:13.0 | **13** | **`schedule/v1/commands/change-flow-step`** | `id · step:CONSULTATION_WAITING` | `{}` | 단계 → 상담 대기 |
| P2 | 21:13.1 ~ 13.3 | 15 · 18 | `get-reservation-group` | | | |
| | | 16 | `get-accounts-last-update…` | | | |
| P3 | 21:18.2 | 20 | `v1/visitor/queries/get-visitor` | `id` | `data{고객}` | 상담사 고르기 창(추정) |
| | | 22 | `purchase/payment-settings/v1/queries/get-payment-settings` | — | `data{…}` | |
| **W3** | 21:31.4 | **27** | **`schedule/reservation/v2/commands/update-reservation`** | `scheduleId · counselor{id, name}` | `{}` | **상담사 지정** |
| P4 | 21:31.6 ~ 32.2 | 28 · 31 | `get-reservation-group` | | | |
| | | 29 | `get-accounts-last-update…` | | | |
| **W4** | 21:43.9 | **35** | **`consultation/v1/commands/create-consultation`** | §2.4 | `{}` | 상담 기록 저장 |
| P5 | 21:44.2 ~ 44.4 | 37 · 41 | `get-reservation-group` | | | |
| | | 38 | `get-accounts-last-update…` | | | |
| | | 39 | `consultation/v1/queries/get-consultations-by-visitor-id` | `visitorId` | `data[1]{id, visitor{id,name,isNew}, scheduleId, consultationStartedDateTimeUtc, counselors[], consultationDoctors[], consultationProcedures[], content{text}, createdDateTimeUtc, updatedDateTimeUtc}` | 방금 만든 상담 |
| | | 40 | `get-codes` | `CONSULTATION_RESULT` | (8) | |
| P6 | 21:55.0 | 45 | `get-roles` | — | | **상담 탭** 열기 |
| | | 46 | `get-reservation-group` | | | |
| | | 48 | `procedure-menu/visitors/…` | | | |
| | | 49 | `get-schedule-summaries` | | 대상: **`CONSULTATION_WAITING` · `IN_PROGRESS`** · `consultation{counselor, consultationMemo}` · `consultations[1]` | |
| | | 50 | `v1/visitor/queries/get-visitor` | `id` | | |
| **W5** | 21:56.6 | **53** | **`schedule/v1/commands/change-flow-step`** | `id · step:CONSULTATION` | `{}` | 단계 → 상담 진행 |
| P7 | 21:56.7 | 54 | `get-reservation-group` | | | |
| | | 55 | `get-accounts-last-update…` | | | |

**합계**: P0 4 + W1 1 + P1 4 + W2 1 + P2 3 + P3 2 + W3 1 + P4 3 + W4 1 + P5 5 + P6 5 + W5 1 + P7 2 = **33**. 쓰기 5건은 모두 같은 일정에 대한 것이다(확인).

---

## 2. 쓰기 5건 해부

### 2.1 ① `recept` — 부도 일정에서

- 본문 `{scheduleId}` 로, 앞 판(RM§2.1)과 같다
- ⚠ **대상 일정의 예약 상태가 `NO_SHOW` 였는데 200 이었다.** 지금 조회하면 `IN_PROGRESS` 다
- 앞 판 시험(MC§3)에서는 부도를 되돌리는지 확인하지 못했다. 이번 HAR 로 **부도 일정도 접수하면 진행 중이 된다**는 것을 확인했다 → Q-99

### 2.2 ② · ⑤ `change-flow-step`

| | 전 | 뒤 | 화면 |
|---|---|---|---|
| ② #13 | `RECEPTION`(①이 만든 상태, 추정) | `CONSULTATION_WAITING` | 예약 탭 |
| ⑤ #53 | `CONSULTATION_WAITING`(#49 확인) | `CONSULTATION`(지금 조회 확인) | 상담 탭 |

- 공개 스펙에는 「상담 진행 단계로 바꿀 때 상담 담당자가 없으면 `counselor NotFound`」라는 400 예시가 있다
- 이번 ⑤는 ③(상담사 지정) · ④(상담 기록) **뒤**에 보냈으므로 그 조건을 채운 상태였다
- 어느 필드(`reservation.counselor` / 상담 기록의 `counselors`)를 「상담 담당자」로 보는지는 문서에 없다 → Q-94

### 2.3 ③ `update-reservation` — 상담사 지정

- 본문 `{scheduleId, counselor:{id, name}}` 만 보낸다. MC§2.1 의 이동과 같은 작업이고, 다른 필드는 보내지 않는다(부분 수정)
- 바뀐 것: `reservation.counselor`(빈칸 → 그 상담사)
- 그 계정의 `roleTags`(공개 `getAccounts`)에는 `COUNSELOR` 가 들어 있다(확인)
- 같은 묶음 JS 에 **`schedule/flow/v1/commands/change-counselor{scheduleId, counselor}`** 와 `assign-counselor-automatically` 도 있다. 이번 HAR 은 `update-reservation` 을 썼다. 둘의 차이는 미확인이다 → Q-93

### 2.4 ④ `create-consultation` — 상담 기록

```text
{ consultationId,                     ← uuid. 화면이 만든다(JS: e.consultationId 를 그대로 보낸다)
  visitorId, scheduleId,
  consultationStartedDateTimeUtc,     ← "…T09:30:00Z" — 이 HAR 에서는 **예약 시작 시각과 같은 값**이었다(실제 저장 시각 06:21Z 가 아니다)
  content: { text },                  ← 상담 내용(짧은 글)
  counselorIds: [1개],                 ← ③의 상담사와 같은 계정
  doctorIds:    [1개] }                ← 상담 의사(그 계정의 roleTags 에 DOCTOR 포함)
→ {}
```

- JS 가 보낼 수 있는 필드: 위 + **`result`**(상담 결과 코드 `{id, name, color}`) + **`consultationProcedures[]`**(상담 시술 — 상품 옵션 · 시술권). 이번 HAR 에는 둘 다 없다
- 같은 묶음 JS 의 상담 쓰기
  - `consultation/v1/commands/change-consultation-information{consultationId, consultationStartedDateTimeUtc, content, counselorIds, doctorIds, result}`
  - `change-consultation-procedures{consultationId, procedures[]}`
  - `change-consultation-counselors` · `change-consultation-doctors`
  - `remove-consultation{consultationId}`
- 상담 조회
  - `consultation/v1/queries/get-consultation` · `get-consultation-event-logs` · `get-consultations-by-visitor-id`
  - `consultation/v2/queries/get-consultation-details`
- 이벤트 로그(내부 `get-consultation-event-logs`, 데모 조회): `ConsultationPlanned` · `ConsultationCounselorsAssigned` · `ConsultationDoctorsAssigned` · `ConsultationContentRecorded` — 4건. **「시작 · 종료」 이벤트는 없다.** KOS 는 이 기록을 「상담 계획(Planned)」으로 다룬다
- **오더 메모(`orderMemo`)는 이 작업에 없다.** 일정 필드이고, 이번에는 바뀌지 않았다

---

## 3. 「상담 완료」가 KOS 에 있나

| 어디를 봤나 | 결과 |
|---|---|
| flowStep enum(스펙) | `RESERVED · RECEPTION · CONSULTATION_WAITING · CONSULTATION · PROCEDURE_WAITING · PROCEDURE · PROCEDURE_DONE · COMPLETED` — **상담 완료 단계 없음** |
| 상담 기록 `ConsultationContract`(스펙 · 응답) | `id · visitor · scheduleId · consultationStartedDateTimeUtc · content · counselors · consultationDoctors · consultationProcedures · result · createdDateTimeUtc · updatedDateTimeUtc` — **종료 시각 · 상태 필드 없음** |
| 일정의 `consultation`(스펙 `ScheduleDetailConsultationContract`) | `counselor · doctor · consultationMemo` 뿐 |
| 이벤트 로그 | 계획 · 상담사 · 의사 · 내용만 있다 |
| 통계(`getScheduleStatistics`) | `consultationWaitingDwellTimeMinute` · `consultationDwellTimeMinute`(단계별 체류 분)이 있다. 이 일정은 아직 상담 단계라 값이 비어 있었다. 단계가 바뀐 시각으로 계산하는 것으로 보인다(추정) |

**상담이 끝났다는 것을 알 수 있는 값**
- 다음 단계로 넘어간 것(`flowStep` 이 `PROCEDURE_WAITING` · `PROCEDURE_DONE` 등) + `flowStepUpdatedDateTimeUtc`
- 상담 기록 `result`(선택 값)
- 상담 기록이 생겼는지(`consultations[]` 개수)는 끝을 뜻하지 않는다. 이번 HAR 은 상담 **진행 전**에 기록을 만들었다

참고(데모 지난 일정 조회): `PROCEDURE_WAITING` 일정 6건 중 상담 기록이 있는 2건 모두 `result` 가 비어 있었다. 결과 코드를 늘 쓰지는 않는다.

---

## 4. 전후 상태 (HAR + 지금 조회)

| 시점 | 근거 | `flowStep` | 예약 상태 | `reservation.counselor` | `consultation`(요약) | `consultations[]` | `tasks[]` |
|---|---|---|---|---|---|---|---|
| 상담 전 | #3 | `RESERVED` | `NO_SHOW` | 없음 | `{}` | 0 | 0 |
| ① ~ ④ 뒤 | #49 | `CONSULTATION_WAITING` | `IN_PROGRESS` | 있음 | `counselor` · `consultationMemo` 있음 | 1 | 0 |
| **지금**(⑤ 뒤) | 공개 `getScheduleDetail` · 내부 `get-consultation` | `CONSULTATION` | `IN_PROGRESS` | 있음 | `counselor` = 상담 기록의 상담사 · `doctor` = 상담 기록의 의사 · `consultationMemo` = 상담 내용(셋 다 같은 값 확인) | 1(상담사 1 · 의사 1 · 결과 없음 · 시술 0) | **0** |

- `consultationRequired` 는 `false` 그대로다. 상담을 했는데도 「상담 필요」 표시는 바뀌지 않는다
- `receptionDateTimeUtc` 있음 · `flowStepUpdatedDateTimeUtc` = ⑤ 시각

---

## 5. 공개 짝

| KOS 쓰기 | 공개 |
|---|---|
| ① 접수 | `changeFlowStep(RECEPTION)` — 결과가 같다(RT§2.3) |
| ② · ⑤ 단계 변경 | `changeFlowStep`. 상담 진행으로 바꿀 때 상담 담당자가 없으면 400(스펙) |
| ③ 상담사 지정(`reservation.counselor`) | **공개 없음.** 공개 `updateReservationV2` 에 `counselor` 칸이 없다(C§5). deprecated v1 `updateReservation` 에는 `counselor` 가 있다 |
| ④ 상담 기록 만들기 · 고치기 · 지우기 | **공개 없음** |
| (상담 메모) | **`updateScheduleConsultationInfo{scheduleId*, consultationMemo}`** — 「전달하지 않으면 변경되지 않음」. 400: `scheduleId NotFound`. 일정 요약의 `consultationMemo` 만 바꾸는 것으로 보인다. 상담 기록 `content` 까지 바뀌는지는 미확인 → Q-96 |
| (조회) | 공개 일정 응답의 `consultation` · `consultations[]`(기록 전체). 상담 기록만 따로 조회하는 공개 작업은 없다 |

---

## 6. 시안과 비교 (D§3.4 「내원 현황」 2 · 상담 카드)

| 시안 | KOS | 메모 |
|---|---|---|
| 상담 카드 상태 「상담 대기 / 진행 중 / 완료」 | 대기 = `CONSULTATION_WAITING`, 진행 중 = `CONSULTATION`, **완료 = KOS 에 단계 없음** | 다음 단계로 넘어감 · `result` 중 무엇을 「완료」로 볼지 → Q-92 |
| 상담사를 안 정했으면 노랑 카드 | 상담사 = `reservation.counselor`(③) 또는 상담 기록 `counselors`(④) | → Q-93 |
| [상담사 선택/변경] 팝오버 · 실장 4명 | 목록 = 공개 `getAccounts(roleTag COUNSELOR)`(`_RESUME` 정해짐). 지정 = 내부 `update-reservation{counselor}` 또는 `flow/change-counselor` | 공개로 지정하는 길은 없다 |
| **[○○ 실장 호출]** | **KOS 에 상담사 「호출」 개념이 없다.** 시술의 `call-tasks-doctors`(의사 호출) 같은 상담 쪽 작업은 JS · 스펙 어디에도 없다 | ccc 만의 기능이 된다 → Q-97 |
| 상담사의 지금 상태(「A-룸2 상담 중」 · 「비어있음」) | KOS 값으로는 계산해야 한다: 그날 일정 중 `flowStep CONSULTATION` 이고 상담사가 그 사람인 일정 + 그 일정의 방(작업 `room`). 상담사 상태 필드는 없다 | R Q-14 → Q-98 |
| [+ 상담 추가](경로를 「상담 필요」로 되돌림) | KOS 는 한 일정에 상담 기록을 **여러 개** 만들 수 있는 구조다(`consultations[]` 배열 · `create-consultation` 은 매번 새 id). 단계는 `change-flow-step` 으로 다시 `CONSULTATION_WAITING` 에 보낸다(거꾸로 가는 변경도 받는다, RM§2.5) | 두 번째 상담을 만들어 보지는 않았다(쓰기 0) → Q-95 |
| 상담 메모 | 상담 기록 `content.text` = 일정 `consultation.consultationMemo`(같은 값) | 공개 쓰기는 메모만 → Q-96 |
| 원장 상담 | 상담 기록 `doctorIds`(상담 의사) · 일정 `consultation.doctor`. 앞 판 「당일 지정 의사」(`occupiedResources.doctors`)와는 다른 필드다 | C Q-58 → Q-100 |

---

## 7. 호출 기록 (조회만)

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| 공개 | `getScheduleDetail` 2 · `getAccounts` 1 · `getScheduleStatistics` 1 · `getSchedulesByFlowStep` 1 | 5 | 200 |
| 내부 | `consultation/v1/queries/get-consultation` 1 · `get-consultation-event-logs` 1 | 2 | 200 |
| 인증 | 공개 `exchange-token` 2 · 내부 sign-in 1 | 3 | 200 |

**쓰기 0건** · 운영 키 0건(스크립트가 쓰기 허가 목록을 비워 두었다).

---

## 8. 정할 것 (결정하지 않음) — 10개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-92 | 상담 「완료」를 무엇으로 볼지 | KOS 에는 단계도 필드도 없다. 다음 단계(시술 대기 · 귀가 대기)로 넘어감 · 상담 결과 코드 · ccc 자체 상태 중 무엇으로 할지 | R Q-1 |
| Q-93 | 상담사 배정을 어디에 쓸지 | `reservation.counselor`(HAR: `update-reservation`) · `flow/change-counselor` · 상담 기록 `counselorIds` 세 길이 있다. 셋 다 쓸지, 하나만 쓸지 | — |
| Q-94 | 상담 진행으로 바꿀 때 필요한 「상담 담당자」 | 공개 스펙은 담당자가 없으면 거절한다. 어느 필드가 그 담당자인지 데모 시험이 필요하다(쓰기) | — |
| Q-95 | [+ 상담 추가] | 한 일정에 상담 기록을 둘 이상 만들지, 하나를 고칠지(`change-consultation-information`). 단계를 상담 대기로 되돌릴지 | — |
| Q-96 | 상담 메모 쓰기 | 공개 `updateScheduleConsultationInfo` 는 일정 요약 메모만 바꾸는 것으로 보인다. 상담 기록 내용까지 바뀌는지 시험할지 | — |
| Q-97 | [실장 호출] | KOS 에 상담사 호출이 없다. ccc 만의 알림으로 둘지 | — |
| Q-98 | 상담사 「지금 상태」 | KOS 에 필드가 없다. 그날 `CONSULTATION` 일정 + 상담사 + 방으로 계산할지 | R Q-14 |
| Q-99 | 부도 일정의 접수 | KOS 는 `NO_SHOW` 일정도 `recept` 를 받아 `IN_PROGRESS` 로 바꾼다. ccc 가 부도 카드에서 [접수] 를 막을지 | MC Q-87 |
| Q-100 | 「원장 상담」의 원천 | 상담 기록의 상담 의사(`doctorIds`) · 일정 `consultation.doctor` · 예약 당일 지정 의사 중 무엇을 원장 상담으로 볼지 | C Q-58 |
| Q-101 | 상담 시작 시각 | HAR 의 `consultationStartedDateTimeUtc` 는 실제 저장 시각이 아니라 예약 시작 시각이었다. ccc 가 「진행 중 · {시각}」을 보일 때 이 값을 쓸지, 단계가 바뀐 시각(`flowStepUpdatedDateTimeUtc`)을 쓸지 | — |
