# 읽기 전용 점검 — 화면 값의 KOS API 원천 (2026-10-13)

- 점검자: cc-prototype `backend` 워커. **코드 수정 없음 · 서버 안 띄움 · KOS 호출 없음.** 사용자 E2E 중인 8600 · `data/cc.db` · `seed.json` 은 건드리지 않았다
- 기준 코드: `cc/back`(WP1 · WP2 · fix1 상태) · 화면이 무엇을 쓰는지는 `cc/front/lib/types.ts` · `lib/board.ts` · `components/desk/*` · `components/staff/*` · `app/login/page.tsx`
- KOS 약어: `SD` = `getScheduleDetail.data` · `T` = `SD.tasks[]` · `SS` = `getScheduleStatistics.data[]` · `PIS` = `getPurchaseItemStatistics.data[]` · `TB` = `getTicketBundlesQuery.data[]` · `PB` = `getVisitorPrepaidCardBalance.data` · `RG` = `getReservationGroups.data[]`
- 판정: **그대로**(형식 변환 · 고객명 치환만) / **가공**(계산 · 자르기, 규칙 한 줄) / **추정**(KOS 에 그 정보가 없는데 다른 필드로 짐작, 이유 한 줄)
- 「현황판 덧씌움」(D-21): 위치 · 단계 · 직원 큐 · since 는 KOS 에 없는 앱 상태다. 시드는 그 **첫 값**을 KOS 시각으로 재구성했고(대부분 추정), 그 뒤는 데스크 조작이 정본이다

---

## 요약

### 추정 22개 (+ ④ 접수 메모 출처 「예약 담당」 1건 — 약한 추정, 표 5)

| # | 화면 · 칸 | 왜 추정인가 |
|---|---|---|
| E1 | 환자 상세 ② 오늘 오더 출처 「상담실장 ○○」 (`patient_service.py:82`) | `orderMemo` 에 작성자 칸이 없다. `consultation.counselor` 를 작성자로 짐작 |
| E2 | 환자 상세 ③ 상담 요약 출처 「상담실장 ○○」 (`:86`) | 상담 메모(`consultations[].content.text`)에 작성자 칸이 없다. 그 상담의 담당 상담사를 작성자로 짐작 |
| E3 | 시술 이력 「타 병원」 출처 「상담 메모 · 상담실장 ○○」 (`:156`) | E2 와 같음 |
| E4 | 오늘 고객 동선 첫 줄 「상담 · 상담실장 ○○」 (`:204`) | KOS 작업(`T`)이 아니다. 상담(`consultations[]`)을 동선 한 단계로 끼워 넣었고, 방은 상담에 방 필드가 없어 완료 기록의 방(= 원장 상담 작업의 방)으로 짐작 |
| E5 | 직원 직군(의사 · 상담사 · 코디) — 로그인 목록 · 현황판 직원 탭 · 점 색 · 배정 직군 탭 | 직원 · 직군 마스터가 캡처에 없다. 이름이 나온 칸(`T.doctors` → 의사 · `consultations[].counselors` → 상담사 · `T.assignees` · `etceteraWorks[].assignees` → 코디)으로 짐작(SPEC §4.1-3 규칙). `T.assignees` 에는 직군이 없다 |
| E6 | 직원 쉬는 위치(`staff[].home` — 원장실 / 데스크) · 직원 탭 「비어있음 · 데스크」 | KOS 에 없음. 시안 기본값(의사 office · 그 밖 desk) |
| E7 | 데스크 계정 「데스크」(로그인 카드) | KOS 에 없음. SPEC §6 의 계정 |
| E8 | 고객 오더 단계 — 시술 단계 묶기 · 라벨 「첫 작업 외 n」 · 시술 담당 직군 | KOS 에 「단계」가 없다. PROCEDURE 작업을 방 · 의사 · 담당자가 같으면 한 단계로 묶고, 의사가 있으면 「의사」 없으면 「코디」 직군으로 짐작 |
| E9 | 고객 오더의 「원장 진료」 단계 | ETCETERA 「방 점유/원장 상담」 작업 하나를 원장 진료 단계로 봤다. 이 작업은 실제로는 방 점유 구간(접수~끝)이다 |
| E10 | 고객 현재 단계(시드 14:45) | KOS 에 단계 이력이 없다. 끝 시각을 짐작: 상담 끝 = 첫 시술 작업 `readyDateTimeUtc`, 원장 진료 끝 = 첫 `doctorCallDateTime` |
| E11 | 고객 위치(시드 14:45) — 방 칸 id | 열린 작업의 방은 가공(아래 B)이지만, **KOS 방 → 현황판 칸**은 임시 대응표(D-13, 사람이 정함)다. 열린 작업이 없고 끝난 작업이 있으면 마지막 방에 둔다(짐작) |
| E12 | 경과 타이머 `since`(시드) | 현재 단계 시작 = E10 의 짐작 시각(또는 `doctorCall`). 초기화 때 「지금 − 오프셋」으로 옮긴다 |
| E13 | 직원 큐 · 「방에 있음」 · 「다음 ○」(시드) | KOS 에 큐가 없다. 열린 작업의 담당자 · 호출된 의사를 그 방에 두고, 여러 방이면 최근 시작한 방을 앞에 뒀다. 상담 중 상담사를 그 방에 둔 것은 상담에 방 정보가 없어서 짐작. 호출 전 의사는 뺐다 |
| E14 | 완료 기록(시드 history) → 의사 「완료」 목록 · 동선 시각 | 단계 끝 시각(E10)과 담당자(단계의 첫 의사/담당자/상담사)가 짐작이다 |
| E15 | 예약 탭 「시술」 · 직원 첫 화면 「시술」(`resv.procedure`, `build.py:325`) | `reservation.requestedProcedures` 가 0/177 로 비어 있다. **실제로 받은** 첫 PROCEDURE 작업 제목 「… 외 n」으로 대체(예약 시점 값이 아님). 작업이 없으면 「상담」/「-」 |
| E16 | 예약 탭 「담당 원장」(`resv.doctor`, `:328`) | `reservation.doctor` 가 0/177 로 비어 있다. 실제 작업의 첫 의사(마취용 제외)로 대체, 없으면 「미정」 |
| E17 | 시술권 `role`(= 「의사」) · `sleep`(= false) — 접수 모달의 오더 미리보기 · 단계 직군 | `getTicketBundlesQuery` 에 담당 직군 · 수면 여부가 없다. 고정값 |
| E18 | 접수 모달 오더(시안 buildOrder — 상담 → 원장 진료 → 시술권들 → **진정 관리**) | front 가 시술권으로 오더를 만든다. 10-09 에 시술권 있는 고객 1명, 「진정 관리」는 KOS 작업에 없다. back 의 KOS 재구성 오더(`plannedOrder`)는 front 가 안 쓴다 |
| E19 | 동선 시각(`route[].readyAt` · `completedAt`) · 귀가 시각(`leaveTime`) | KOS 시각이 아니라 **시드 오프셋을 「지금」으로 옮긴 값**(E12 와 같은 방식). 시연 시계 기준이라 실제 10-09 시각과 다르다 |
| E20 | 동선 상태(완료 · 진행 중 · 예정) | KOS 작업 상태(DONE)가 아니라 현황판 단계(E8 · E10)에 작업을 대응시켜 정한다. 시드 14:45 에 KOS 로는 끝난 작업도 「예정」일 수 있다 |
| E21 | 현황판 방 상태 · 라벨 · 대기 라벨 · 요약 수 · 코디 화면 상태 배지 | 시안 규칙(statusOf · waitLabel) 계산 자체는 가공이지만 입력(위치 · 단계 · 큐)이 E10~E13 의 짐작이다 |
| E22 | 시술 이력 「이 병원 · 첫 방문 — 이전 시술 기록 없음」 | `isFirstProcedureSchedule` 플래그만 있다. 「이전 시술 기록 없음」 문장은 플래그에서 짐작(재방문이면 「재방문」만, 이력 조회는 안 함 — D-10) |

### 가공 25개

나이 · 국적명(front) · 아웃 시각 · ⚠ 주의(4종 모으기) · ② 오늘 오더 줄 · 마취 줄 · ③ 상담 요약 · ④ 접수 메모(앞뒤 빈 줄 자르기) · 원장 목록(마취용 제외) · 동행 · 보유 시술권 요약 · 시술권 left/total · 오늘 결제 · 서비스(0원) · 타 병원 이력 줄 · 메모 속 이름 · 전화 치환 · 예약 상태 `st` · 예약 시각(KST HH:MM) · 동선 방 이름 · 동선 담당(마취용 제외) · 코디 요약 수 · 코디 목록 정렬 · 의사 현재/다음 · 통역 자막 묶기 · 번체 변환. 규칙은 아래 표

---

## 표 1 — 로그인 (`GET /api/staff` · `POST /api/login`)

| 화면 · 칸 | 응답 필드 | KOS 원천 | 판정 |
|---|---|---|---|
| 직원 이름 | `[].name` | `T.doctors[].name` · `T.assignees[].name` · `etceteraWorks[].assignees[].name`(그날 일정, 「마취용」 제외) | 그대로 |
| 직원 id | `[].staffId` | 같은 칸의 `.id` | 그대로 |
| 역할(의사 · 코디) | `[].role` | 이름이 나온 칸 | **추정 E5** |
| 데스크 카드 | `{staffId:"desk", name:"데스크"}` | 없음 | **추정 E7** |
| 로그인 뒤 이동 | `home` (`/desk` · `/staff`) | 없음(SPEC §6) | (UI 규칙) |

## 표 2 — 데스크 현황판 (`GET /api/board`)

| 화면 · 칸 | 응답 필드 | KOS 원천 | 판정 |
|---|---|---|---|
| 도면 칸 · 방 이름 | `rooms[]` id · name · col · row | 시안 LAYOUT(KOS 방 마스터 없음, `getZones` 는 「4층」 1건) | (시안 상수) · `kosRooms` 는 임시 대응표(D-13) |
| 방 안 고객 이름 · 라운지 고객 | `customers[].name` | `SD.visitor.name` → 가짜 이름 | 그대로(치환) |
| 고객 위치 | `customers[].room` | `T.room.title` + `readyDateTimeUtc ≤ T < completedDateTimeUtc` + 대응표 | 가공 + **추정 E11** |
| 고객 오더 단계 목록(고객 탭 · 방 패널 · 라운지 패널 「→」) | `customers[].order[]` | `consultations[]` 유무 · ETCETERA 작업 · PROCEDURE `T.title` · `sequence` | **추정 E8 · E9** |
| 지남/지금/남음 | `customers[].step` | 단계 끝 시각 짐작 | **추정 E10** |
| 방 타이머 · 라운지 대기 시간 · 진행 목록 경과(정렬) | `customers[].since` | 단계 시작 짐작 → 오프셋 | **추정 E12** |
| 「수면 중 · 복귀 예정」 | `customers[].prev` | 없음(수면 단계 0건) — 시드에서는 늘 null | (앱 상태) |
| 방 상태색 · 상태 배지 · 라벨(원장 대기 · 마무리 대기 …) · 요약 숫자 | front `statusOf` · `waitLabel`(customers · staff 로 계산) | 시안 규칙 | 가공(규칙) · 입력은 **추정 E21** |
| 직원 이름 · 점 색 · 직군 | `staff[].name` · `role` | 표 1 과 같음 | 그대로 / **추정 E5** |
| 방에 있는 직원 · 「다음 ○」 · 직원 탭 현재 방/다음 방 · 대기 N건 | `staff[].queue` | 시드: 열린 작업 `T.assignees` · `doctorCallDateTime ≤ T` 인 `T.doctors` · 진행 중 상담의 `counselors` | **추정 E13** |
| 직원 탭 「비어있음 · 데스크/원장실」 | `staff[].home` | 없음 | **추정 E6** |
| 예약 탭 시각 | `resv[].time` | `SD.reservation.startDateTime` → KST HH:MM | 그대로(형식) |
| 예약 탭 이름 | `resv[].name` | `SD.visitor.name` → 가짜 이름 | 그대로(치환) |
| 예약 탭 시술 | `resv[].procedure` | 실제 PROCEDURE 작업 첫 `T.title` + 「외 n」 | **추정 E15** |
| 예약 탭 담당 원장 | `resv[].doctor` | 실제 작업 첫 `T.doctors[].name`(마취용 제외) / 「미정」 | **추정 E16** |
| 예약 상태(예정 · 접수 · 노쇼 · 취소) · 요약 수 | `resv[].st` | `SD.reservation.status`(CANCELED · NO_SHOW) + `SD.receptionDateTimeUtc ≤ T` → checked, 그 밖 booked | 가공 |
| 예약 행 「방 이름 / 귀가」 | front: `customers` 의 room · done | 위 위치 · `flowStepUpdatedDateTimeUtc ≤ T`(COMPLETED) → 귀가 | 가공 + E11 |
| 예약 행 「n분 지연 · 곧 도착」 | front 가 `resv.time` 과 **지금 시계**로 계산 | — | (front 계산) ⚠ 시드 날 시각과 시연 시계를 비교한다 |
| 현장 접수 행 | `resv[]`(walkin-n) · 「현장 접수 · 미정」 | 없음(앱 입력) | (앱 상태) |

## 표 3 — 방 패널 · 접수 모달 (`/api/board` + `GET /api/patients/{id}`)

| 화면 · 칸 | 응답 필드 | KOS 원천 | 판정 |
|---|---|---|---|
| 고객 메타 「여 · 36세 · 첫 방문」 | `sex` · `age` · `firstVisit` | 표 5 와 같음 | 그대로 · 가공 · 그대로 |
| 고객 주의 한 줄 | `cautions[].text` | 표 5 ① | 가공 |
| 필요 직군 「필요: 원장 · 원장 진료」 | `order[step]` | E8 · E9 | **추정** |
| 직원 배정 풀 상태(비어있음 · 지금 방 · 대기 N건) | `staff[].queue` | E13 | **추정** |
| 접수 모달 예약 문구(시각 · 시술 · 담당) | `resv` time · procedure · doctor | 표 2 | 그대로 · **E15** · **E16** |
| 보유 시술권 이름 | `tickets[].name` | `TB[].ticketSets[].title`(없으면 `procedure.name`) | 그대로 |
| 잔여/총 회 | `tickets[].left` · `total` | `ticketSets[].tickets[].status == AVAILABLE` 개수 · 전체 개수 | 가공 |
| 만료일 | `tickets[].expires` | 없음 — 빈 값(front 는 숨김) | (빈 값, 채우지 않음) |
| 시술권 담당 직군 · 수면 | `tickets[].role` · `sleep` | 없음 — 「의사」 · false | **추정 E17** |
| 오늘 진행 순서 미리보기 · 접수 때 보내는 오더 | front `buildOrder` | 시안 규칙 + 시술권 | **추정 E18** |

## 표 4 — 직원 첫 화면 (`GET /api/staff/{id}/home`)

| 화면 · 칸 | 응답 필드 | KOS 원천 | 판정 |
|---|---|---|---|
| 의사 「지금 진행 중」 · 「다음」 | `current` · `next` | `staff.queue[0]` · `[1]` 방의 첫 고객 | 가공(앱 상태) · 입력 **E13** |
| 의사 「완료」 행 | `done[]` | history 중 내 staffId | **추정 E14**(시드분) · 데스크/의사 조작분은 앱 기록 |
| 행 시각 | `time` | `reservation.startDateTime` KST | 그대로(형식) |
| 행 이름 · 국적 | `name` · `nationality` | `visitor.name`(치환) · `visitor.nationality` | 그대로 |
| 행 시술 | `procedure` | = `resv.procedure` | **추정 E15** |
| 행 방 | `room` → 칸 이름 | 고객 위치 | 가공 + **E11** |
| 「n / 전체 완료」 | front: done 수 / 행 수 | — | (front 계산) |
| 코디 목록 상태 배지 · 라벨 · 경과 | `state` · `label` · `since` | 현황판 계산 | 가공 · **E21 · E12** |
| 코디 목록 정렬(경과 긴 순) · 「외국인 n명」 · 요약(대기 · 상담 · 시술) | `since` 순 · `nationality` · `summary` | — | 가공 |

## 표 5 — 환자 상세 (`GET /api/patients/{scheduleId}`)

| 화면 · 칸 | 응답 필드 | KOS 원천 | 판정 · 규칙 |
|---|---|---|---|
| 이름 | `name` | `SD.visitor.name` → 가짜 이름 | 그대로(치환) |
| 국적 칩 | `nationality` | `SD.visitor.nationality` | 그대로 (front 가 코드 → 「대만」) |
| 성별 | `sex` | `SD.visitor.gender` FEMALE/MALE → 여/남 | 그대로(형식) |
| 나이 | `age` | `SD.visitor.dateOfBirth` → 시드 날 기준 만 나이(그해 · 미래 생년은 null) | 가공 |
| 첫 방문/재방문 | `firstVisit` | `SS.isFirstProcedureSchedule`(없으면 `visitor.isNew`) | 그대로 |
| 예약 시각 | `reservationTime` | `SD.reservation.startDateTime` KST | 그대로(형식) |
| 상태 · 지금 방 · 라벨 | `board` | 현황판 상태 | 가공 · **E11 · E21** |
| 귀가 시각 | `leaveTime` | `flowStepUpdatedDateTimeUtc` 를 오프셋으로 옮긴 값 / 앱 귀가 시각 | **추정 E19** |
| 아웃 시각 | `outTime` | ① `orderMemo` 의 `OUT TIME :` 값(x · 빈 값 제외) → ② `reservationMemo` 앞줄 중 「n시 … 아웃」류 → ③ `reservation.desiredDischargeDateTimeUtc` | 가공(D-23) |
| 상담실장 | `counselor` | `SD.consultation.counselor.name` | 그대로 |
| 원장 | `doctors` | 취소 아닌 `T.doctors[].name`(「마취용」 제외, 중복 제거) | 가공 |
| ① ⚠ 주의 | `cautions[]` | `visitor.memo`(「고객 메모」) → `orderMemo` · 상담 메모 `------` 아래의 `[특이사항]` · `[임플란트 여부]` 값(x · 빈 값 버림, `o .` 접두 떼기, 같은 문장 합침, 「특이사항 — 값」 꼴) → `orderMemo` · `reservationMemo` 맨 앞 `**` · `★` 줄 | 가공 · 출처 라벨(「오더 메모 · 상담 메모 사본」)은 메모 위치라 그대로 |
| ② 오늘 오더 줄 · 접힘 마취 줄 | `order.lines` · `anesthesia` | `orderMemo` 에서 번호 줄 · `*` 지시 줄 · 「마취」 든 줄 | 가공 |
| ② 출처 「오더 메모 · 상담실장 ○○」 | `order.source` | 작성자 칸 없음 | **추정 E1** |
| ③ 상담 요약 | `consult.lines` | `consultations[0].content.text`(없으면 `consultation.consultationMemo`)의 `------` 위, 「[상담내용]」 · 빈 줄 제외 | 가공 |
| ③ 출처 「상담 메모(구분선 위) · 상담실장 ○○」 | `consult.source` | 작성자 칸 없음 | **추정 E2** |
| ④ 접수 메모 | `reception.lines` | `reservation.reservationMemo` 전체(앞뒤 빈 줄만 자름) | 가공(자르기) |
| ④ 출처 「예약 메모 · 예약 담당 ○○」 | `reception.source` | `reservation.reservationAssignee.name` — **예약 담당자 칸이지 메모 작성자 칸이 아니다**(당일 덧붙인 줄은 다른 사람이 썼을 수 있음, research-patient-detail §A-0) | **추정(약)** — E1 과 같은 성격. 요약 표에는 E1~E3 와 묶어 볼 것 |
| 차트 · 유입 | `chart[유입]` | `reservation.funnel.funnel.name` + `funnelDetail` | 그대로 |
| 차트 · 예약 그룹 | `chart[예약 그룹]` | `reservation.reservationGroupId` → `RG.title`(없으면 `SS.reservationGroupTitle`) | 그대로(조회) |
| 차트 · 동행 | `chart[동행]` | `reservationMemo` 의 「동행 n명 …」 구절(없으면 「동행」 든 짧은 줄) | 가공 |
| 차트 · 보유 시술권 | `chart[보유 시술권]` | `TB` AVAILABLE 수 / 전체 | 가공 |
| 차트 · 선불 잔액 | `chart[선불 잔액]` | `PB.remainingBalance.balance.value`(0 이면 숨김) | 그대로 |
| 차트 · 오늘 결제 · 서비스(0원) | `chart[오늘 결제]` · `chart[서비스(0원)]` | `PIS` 중 같은 `visitorId` · `createdDateTimeUtc` 가 시드 날(KST) · `purchaseStatus == ACCEPTED` 의 `productOptionTitle` + `cost.totalAmount` | 가공 — ⚠ 일정 id 가 아니라 **고객 + 날짜로 묶었다**(같은 날 일정이 둘이면 섞인다) |
| 시술 이력 · 이 병원 | `history[0]` | `isFirstProcedureSchedule` | **추정 E22**(문장) |
| 시술 이력 · 타 병원 | `history[1..]` | 상담 메모 위쪽 `H)` · `받은시술:` 줄(값 있는 것), 없으면 「n월 … 하심/하셨」 문장 | 가공 · 출처 라벨 **추정 E3** |
| 동선 · 방 | `route[].room` | `T.room.title` → 대응표 칸 이름(대응 없으면 KOS 원값) | 가공 + 대응표(D-13) |
| 동선 · 작업 | `route[].task` | `T.title`(없으면 `etceteraConfiguration.name`) | 그대로 · 첫 줄 「상담」은 **추정 E4** |
| 동선 · 담당 | `route[].staff` | 「원장 」+ `T.doctors[].name`(마취용 제외) · `T.assignees[].name` | 가공(형식) |
| 동선 · 상태 | `route[].status` | 취소 = `T.status == CANCELED` 그대로 · 나머지는 현황판 단계 | **추정 E20** |
| 동선 · 시각 | `route[].readyAt` · `completedAt` | 완료 기록(오프셋) · 현재 since | **추정 E19** |
| 동선 · 담당자 메모 | `route[].memo` | `T.assigneeMemo`(끝난 작업만) | 그대로 |
| 메모 속 이름 · 전화 | 모든 메모 칸 | 원문 → 가짜 이름 · `010-****-****` | 가공(D-09) |

## 표 6 — 통역 모달 (`WS /api/interpret`, WP2)

| 화면 · 칸 | 메시지 필드 | 원천 | 판정 |
|---|---|---|---|
| 말풍선 원문 · 번역 | `caption.original` · `translation` | Soniox STT 토큰(`text` · `translation_status`) — KOS 아님 | 가공(`<end>` 까지 묶기 · zh/ja/th 빈칸 제거 · TW/HK 번체 변환) |
| 왼쪽/오른쪽 | `caption.side` | Soniox 토큰 `language`(원문 ko → me) | 가공 |
| 기본 언어 | front `NAT_LANG` | `visitor.nationality` → 언어(SPEC §7.2 표) | (SPEC 규칙) |

---

## 코디가 볼 것

1. **E1 · E2 · E3(+ ④ 예약 담당)** — 출처 줄의 사람 이름이 「작성자」로 읽힌다. KOS 에 작성자 칸이 없으니 사용자 원칙대로라면 **출처는 메모 종류만**(「오더 메모」 · 「상담 메모(구분선 위)」 · 「예약 메모」) 두고, 사람 이름은 빼거나 실제 칸 이름대로(「상담 담당 ○○」 · 「예약 담당 ○○」) 붙이는 게 맞다. 고칠지 결정 필요(이번엔 읽기만)
2. **E15 · E16** — 예약 탭의 시술 · 원장은 예약값이 아니라 **사후 실적값**이다. 칸 이름을 바꾸거나(「받은 시술」) 비워 두는 선택지가 있다
3. **E17 · E18** — 접수 모달 오더는 front 의 시안 규칙(진정 관리 포함)으로 만들어진다. 시드의 KOS 재구성 오더(`plannedOrder`)와 다를 수 있다
4. **E19** — 동선 · 귀가 시각은 시연 시계로 옮긴 값이다. 실제 KOS 시각을 보이려면 KOS `T.readyDateTimeUtc` · `completedDateTimeUtc` 를 그대로 쓰는 쪽(대신 현황판 시각과 안 맞음)
5. **오늘 결제** — 일정이 아니라 고객 + 날짜 기준. 10-09 에 한 고객 두 일정은 없어 지금은 문제없다
6. 예약 행 「n분 지연」은 front 가 시드 날 예약 시각을 **지금 시계**와 비교한다(시연 시각에 따라 전부 지연/예정으로 보일 수 있음)
