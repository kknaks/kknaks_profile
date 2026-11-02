# cc 시안 × 운영 데이터 적합성 조사 (2026-10-12)

- 조사자: cc-prototype `researcher` 워커 · 조사일 2026-10-12
- 시안: `/Users/kknaks/git/toy_pr2/cc-prototype/cc/design/` 사본(원본 claude.ai/design 은 열지 않음 — 사본으로 충분했다)
- 데이터: `reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/` (production · 2026-10-01~10-11 KST · 캡처 2026-10-12)
- 모든 수치는 캡처 파일을 읽기 전용으로 직접 세어 얻었다(`python3` 일회성 실행, 결과 파일 없음). 개인 식별 값은 이 문서에 없다 — 필드 경로·건수·코드값만 적었다.
- 판정 정의: **바로 됨** = 필드 하나를 그대로 표시 · **가공** = 여러 필드를 묶거나 시각으로 계산하거나 규칙으로 추정해야 함 · **없음** = 캡처에 대응하는 필드가 없음(또는 전부 비어 있음)

---

## 결론 한 장

| 시안 | 정보 칸 | 바로 됨 | 가공 | 없음 |
|---|---|---|---|---|
| 현황판 v3 (데스크톱) | 63 | 10 | 41 | 12 |
| 의사 모바일 | 24 | 6 | 14 | 4 |

(칸 목록·판정은 §C-6 매핑표. 「현장 접수」·토스트 「되돌리기」·「차트 열기」처럼 화면 조작만 하고 정보를 보여 주지 않는 버튼은 세지 않았다.)

**구현 가능 판단의 근거**

1. **「누가 · 어느 방에서 · 무슨 시술을 · 언제부터」의 뼈대는 데이터에 있다.** `getScheduleDetail` 177건에 고객(visitor) · 예약 시각 · 접수 시각 · 작업(tasks 719건)이 있다. 각 작업에 방(`tasks[].room.title`, 99%) · 담당자(`assignees` 649건) · 의사(`doctors` 557건) · 시각 4종(`ready` 100% · `roomAssigned` 99% · `doctorCall` 67% · `completed` 98%)이 붙어 있다. 그래서 어떤 시각 t 에서 「방마다 고객·직원·현재 시술」은 **시각으로 다시 만들 수 있다**(가공).
2. **다만 상태 변화 이력이 아니라 최종 시각만 있다.** `flowStep` 은 최종값 두 가지(`COMPLETED` 151 · `RESERVED` 26)만 있고 이력 배열은 없다. `taskTimers[]`·`reactions[]` 는 177건 모두 비어 있다. 방을 옮기면 `roomAssignedDateTimeUtc` 가 **덮어써진다** — 원장 상담 작업 135건 중 72건이 ready 보다 5분 넘게 늦게 다시 배정됐다. 그래서 재생은 「근사」다.
3. **시안이 전제하는 운영 모델 일부가 데이터와 다르다.** 시안의 직원 큐 · 라운지/상담실/데스크 같은 비(非)시술 공간 · 수면실 · 고객 주의사항 · 직군 구분은 캡처에 없거나 다른 모양이다. 화면 칸의 약 1/4 이 「없음」인 이유다.

**가장 큰 구멍 3개**

1. **방 배치(도면)가 맞지 않는다.** 데이터 구역은 `4층` 하나뿐이다. 방은 14개(`A_룸1–9` · `A_트윈1-1/1-2` · `A_시술실1–2` · `A_레이저실`)다. 시안은 명동점 1층 33칸(관리실 01–16 · 2인관리실 01–03 · 수면실 01–03 · 라운지 · 상담실 · 데스크 · 인포 1–2)이다. 좌표·정원·방 마스터 API 는 캡처에 없다(`getZones` 는 구역 1건). 라운지·상담실·수면실에 해당하는 방은 데이터에 아예 없다.
2. **직원 큐와 직군이 없다.** 「다음 X」· 「배정 대기 · 앞 순서 N건」(시안의 직원 큐 개념)은 데이터에 없다. 직군도 「어느 필드에 이름이 들어 있나」(doctors/counselors/assignees)로 추정할 수밖에 없다. 직원·직군 마스터 API 는 캡처되지 않았다.
3. **고객 주의사항 · 시술 이력 · 방문 횟수가 없다.** 고객 단위 주의사항 필드가 없다(`medicalServiceConfiguration.caution` 0/574, 자유 메모 `visitor.memo` 12/177 만 있음). 이력은 캡처 기간(11일) 밖이라 없다(재방문 고객 4명). 의사 모바일의 주의사항·시술 이력 카드와 접수 모달의 주의사항이 비게 된다.

---

## A. 시안이 요구하는 정보 (질문 1~2)

### A-1. 현황판 v3 — 영역별 정보 칸

`Ceramique 현황판 v3.dc.html` (이하 `v3:줄`)

| 영역 | 보여 주는 정보 | 근거 |
|---|---|---|
| 헤더 | 지점명 · 로그인 사용자 · 메뉴 | v3:20, 22, 995 |
| 제목 줄 | 「실시간 현황판」 · 지점 · **층** · 안내 | v3:26–27 |
| 범례 | 역할 4종 점 색(고객 gray-800 · 의사 purple · 상담사 yellow · 코디 primary) · 방 상태 3종(대기 · 상담 · 시술) | v3:31–45, 473, 476–480 |
| 도면 그리드 | 8열 × 6줄 + 복도 2줄. 방마다 **이름 · 타이머(상태 진입 후 경과) · 라벨(현재 단계) · 사람(고객/직원 점+이름, 라운지는 고객별 대기 시간) · 큐 대기 직원(「다음 ○」)** · 상태색(빈 방/직원만/대기/상담/시술) · 수면 중 복귀 예정 표시 | v3:54–85, 554–561, 684–711 |
| 동선 화살표 | 직원 탭: 선택한 직원의 큐 순서대로 방 사이 화살표. 고객 탭: 라운지 → 현재 방(→ 수면실 → 복귀) | v3:86–101, 712–728, 924–950 |
| 우측 · 현황 탭 | 요약 숫자 3개(대기 · 상담 · 시술 방 수) · 목록(상태 배지 · 방 · 경과 · 고객 · 라벨 · 직원 「직군 이름」), 경과 긴 순 | v3:199–234, 741–760 |
| 우측 · 예약 탭 | 요약 3개(예정 · 접수 · 노쇼) · 「오늘 예약 N건」 · 행(시각 · 이름 · 지연/곧 도착 힌트 · 시술 · 담당 의사 · 접수 버튼 또는 상태 [방 이름/귀가/노쇼]) · 현장 접수 버튼 | v3:118–150, 791–821 |
| 우측 · 직원 탭 | 행(직군 점 · 이름 · 직군 · 대기 N건[2건↑ 빨강] · 현재 방+업무 · 다음 방 목록) — 의사→상담사→코디 순 | v3:153–172, 762–778 |
| 우측 · 고객 탭 | 행(상태 배지 · 이름 · 현재 위치 · 오더 단계 목록[번호 · 단계명 · 담당 직군 · 지남/지금/남음]) | v3:174–197, 779–790 |
| 접수 모달 | 이름 · 메타(성별 · 나이 · 차트번호 · 신규) · 예약 문구(시각 · 시술 · 담당) · 주의사항 · **보유 시술권(이름 · 잔여/총 회 · 만료일 · 소진)** · 상담 필요 체크 · 오늘 진행 순서 미리보기 | v3:245–306, 822–854 |
| 방 패널 모달 (고객 있는 방) | 방 이름 · 상태 배지 · 타이머 · 고객(이름 · 메타 · 주의 · 단계 목록) · 수면실로 이동(빈 수면실 버튼) · 현재 방 직원(빼기/완료) · 필요 직군 문구 · 배정 대기 큐(앞 순서 N건 · 지금 위치) · 직원 배정(직군 탭 · 직원 풀[비어있음/현재 방+업무/대기 N건] · 배정 상태) | v3:308–413, 868–898 |
| 방 패널 모달 (빈 방) | 넣을 후보(이름 · 라운지 대기 시간 또는 현재 방 · 오더 요약) · 빈 이유 문구(수면 복귀 예정 등) | v3:415–434, 899–911 |
| 방 패널 모달 (라운지) | 대기 고객(이름 · 대기 시간 · 오더 요약) · 배정할 관리실 목록(빈방 / 2인실 n/2명) | v3:436–465, 912–921 |
| 토스트 | 마지막 조작 문구 · 되돌리기 | v3:238–243 |

### A-2. 의사 모바일 — 영역별 정보 칸

`Ceramique 의사 모바일.dc.html` (이하 `mob:줄`)

| 영역 | 보여 주는 정보 | 근거 |
|---|---|---|
| 헤더 | 로고 · 지점 · 의사 점 색 · 의사 이름+직함 · 시계 | mob:21–32 |
| 지금 진행 중 카드 | 방 · 고객 이름 · 시술 · 경과 mm:ss | mob:36–47, 215 |
| 오늘 내 일정 | 「n / 전체 완료」 · 행(시각 · 이름 · 방 · 시술 · 상태 배지[완료/진행 중/다음/예정]) | mob:48–63, 162–167, 216–227 |
| 선택 환자 상세 | 라벨(진행 중인/다음/예정/완료한 환자) · 타이머(대기/경과/「HH:MM 예약」) · 이름 · 메타(성별 · 나이 · 차트번호 · 신규) · 방 · 시술 계획 · 주의사항 목록 · 버튼(차트 열기 · 진료 시작/진료 완료) | mob:67–96, 229–237 |
| 오늘 ○님 동선 | 단계 번호 · 방 · 업무 · 지남/지금/남음 | mob:98–106, 239–246 |
| 상담 메모 | 작성자(직군 이름) · 본문 | mob:108–114 |
| 시술 이력 | 방문 n회 · 행(날짜 · 시술 · 시술한 의사) · 「첫 방문 고객」 | mob:116–131 |

### A-3. 시안이 전제하는 도메인 개념과 값

| 개념 | 시안의 값 | 근거 |
|---|---|---|
| 직원 직군 | `의사`(표시는 「원장」) · `상담사` · `코디` — 고객은 별도 점 | v3:473–475 |
| 오더 단계 종류(kind) | `consult` 상담(상담사) · `doctor` 원장 진료(의사) · `treat` 시술(의사 또는 코디) · `sleep` 수면 시술(의사, 수면실) · `calm` 진정 관리(코디) | v3:487–491 |
| 오더 자동 구성 | 상담 필요면 상담 → 시술권 선택 시 원장 진료 + 시술들 + 진정 관리 | v3:594–600, 299 |
| 방 상태 | 빈 방(`EMPTY`) · 직원만(`STAFFED`) · `wait` 대기 · `consult` 상담(상담/원장 진료 중) · `treat` 시술 | v3:476–483, 578–584 |
| 대기 라벨 | 마무리 대기 · 수면실 이동 대기 · 원장 대기 · 상담사 대기 · 「직군 대기 · 단계」 | v3:571–577 |
| 방 종류·정원 | 관리실 `c01–c16`(1명) · 2인관리실 `t01–t03`(2명) · 수면실 `s01–s03`(1명) · 라운지(무제한) · 데스크 · 인포 1/2 · 상담실 · 원장실(`office`, 도면 밖) | v3:552–564 |
| 직원 큐 | 직원마다 방 목록, 첫 번째가 지금 있는 방. 바쁜 직원에게 배정하면 큐 뒤에 쌓임 | v3:526–533, 567–569, 633–638 |
| 직원 쉬는 위치(home) | 의사 → 원장실, 그 외 → 데스크 · 상담실 · 인포 | v3:608 |
| 수면 시술 이동 | 관리실 → 수면실 → (완료 후) 원래 관리실로 복귀 · `prev` 로 기억 | v3:649, 660, 702 |
| 예약 상태 | `booked` 예정 · `checked` 접수 · `noshow` 노쇼 · 지연/곧 도착(현재 시각 기준 15분) | v3:534–548, 793–811 |
| 시술권 | 이름 · 잔여/총 회 · 만료일 · 담당 직군 · 수면 여부 | v3:492, 499–504 |
| 의사 화면 환자 상태 | `done` 완료 · `now` 진행 중 · `next` 다음 · `later` 예정, 진료 시작/완료로 한 칸씩 넘어감 | mob:162–167, 184–196 |
| 대기/경과 시간 | 방·고객별 mm:ss(1시간↑ h:mm:ss), 1초마다 갱신 | v3:611–615, mob:180–183 |

---

## B. 데이터가 가진 정보 (질문 3~5)

### B-3. API 별 내용

| API | 파일 | 건수 | 한 줄 설명 · 핵심 필드 |
|---|---|---|---|
| `getScheduleDetail` | 177 | 일정 177 · 작업 719 | **본체.** 일정(방문) 1건의 고객 · 예약 · 상담 · 작업 · 기타업무. 아래 필드 트리 |
| `getScheduleStatistics` | 1 | 177 | 일정 통계 행. `reservationStatus` · `receptionDateTimeUtc` · **체류 시간 5종**(`receptionDwellTimeMinute` 153 · `consultationWaitingDwellTimeMinute` 130 · `consultationDwellTimeMinute` 141 · `procedureWaitingDwellTimeMinute` 133 · `procedureDoneDwellTimeMinute` 109) · `durationMinute` 151 · `counselorNames[]` · `isFirstProcedureSchedule` · `reservationGroupTitle` |
| `getProcedureTaskStatistics` | 2 | 702 | 완료된 시술 작업 통계 행(= DONE 작업 702와 같은 수). `roomTitle` · `doctorNames[]` · `assigneeNames[]` · `counselorNames[]` · `doctorCallDateTimeUtc` · `doctorAssignedDateTimeUtc` · `completedDateTimeUtc` · `machineNames[]` · `anesthesiaType` |
| `getZones` | 1 | 1 | 구역 마스터: `4층` 한 건(`isDefault`). **방 목록은 없음** |
| `getMachines` | 1 | 306 | 장비 마스터 `id · name` |
| `getProcedures` | 1 | 1,626 | 시술 마스터 `id · name` |
| `getMedicalServices` | 1 | 280 | 진료 서비스 마스터 `title · code · procedure · machines[] · medicines[] · unit` (「수면마취」·「크라이오 진정관리」 서비스가 있다) |
| `getReservationGroups` | 1 | 5 | 예약 그룹(`기타` · `영미권` · `일본` · `중화권` · `국내`) · 30분 간격 · 간격당 정원 7 · 요일별 운영 시간 |
| `getReservationRuleSummaries` | 1 | 1 | 예약 규칙 요약(수정자 이름 포함) |
| `getTicketBundlesQuery` | 173 | 11명만 값 있음 | 고객별 보유 시술권. `ticketSets[].title · medicalService · tickets[].status`(`AVAILABLE` 37 · `USED` 9) · `price` · `createdDateTimeUtc`. **만료일 필드 없음** · 162 파일은 빈 객체 |
| `getVisitorPrepaidCardBalance` | 173 | 173 | 고객별 선불 잔액·포인트 |
| `getPrepaidCardSummaries` · `getPrepaidCardChargingEvents(+Statistics)` | 173+1+1 | 선불카드 1장 | 선불카드 요약·충전 이벤트 |
| `getPurchaseSummaries` · `getPurchaseItemStatistics` · `getTransactionStatistics` | 3·2·1 | 구매 168 · 품목 547 · 결제 173 | 구매·품목·결제(금액 · 결제수단 · 카드 승인번호 등). 현황판 시안에는 쓰는 칸 없음 |
| `getProducts` · `getCategories` · `getMedicines` · `getTargetCountries` | 1씩 | 122 · 16 · 355 · 2 | 상품(옵션 · 가격 · `cautions[]` 66개 상품에 값) · 카테고리 · 약품 · 대상 국가 |
| (제외) | — | — | `getVisitorStatistics` · `getTicketGroupStatistics` 는 캡처에서 제외(`manifest.excludedOperations`). 실패 요청 0 |

#### `getScheduleDetail` 필드 트리 (요약 · `.data.` 생략 · 괄호는 값이 찬 건수)

```text
id · createdDateTimeUtc · updatedDateTimeUtc · deleted(전부 false) · receptionDateTimeUtc(153/177)
flowStep · flowStepUpdatedDateTimeUtc(153/177) · orderMemo(141) · visitorLocation.zoneId(153)
visitor: id · name · phone{countryCode,phoneNumber}(142) · chartNumber · gender · dateOfBirth(175)
         nationality · memo(12) · visitorType{id,name} · isNew · categories[] · snsInfo{snsType,accountId(91)} · phoneticName(140)
reservation: reservationGroupId · startDateTime · endDateTime · status · zoneId
         consultationRequired(전부 false) · sedationRequired(전부 false) · desiredDischargeDateTimeUtc(6)
         doctor{id,name}(0/177 — 비어 있음) · counselor{id,name}(0/177 — 비어 있음) · reservationAssignee{id,name}(175)
         funnel{funnel{…},funnelDetail(10)} · reservationMemo(174) · requestedProcedures[](0/177 — 비어 있음) · connectedChannel
consultation: counselor{id,name}(143) · doctor{id,name}(11) · consultationMemo(143)
consultations[](145): id · visitor{id,name,isNew} · scheduleId · consultationStartedDateTimeUtc · counselors[] · consultationDoctors[](11)
         consultationProcedures[](0) · content.text(143) · created/updatedDateTimeUtc
tasks[](719): type · sequence · order · title · status · paymentRequired(전부 false) · urgencyLevel(전부 UNSPECIFIED) · anesthesiaType
         room{id,zoneId,title,order} · assignees[]{id,name} · doctors[]{id,name} · calledDoctors[]{id,name} · doctorsCalledZone(48)
         readyDateTimeUtc · roomAssignedDateTimeUtc · doctorAssignedDateTimeUtc · doctorCallDateTime · completedDateTimeUtc
         assigneeMemo(237) · doctorMemo(0) · memo(3) · etceteraConfiguration{etceteraTaskId,name}
         procedureConfiguration(574, PROCEDURE 만): medicalServiceConfiguration{title,code,machines[],medicines[],unit,caution(0)}
                                                    productOptionConfiguration{productTitle,optionTitle,procedure,unit} · ticketConfiguration{ticketId,round{current,total}}
         translsMap.title.translation.{ko,en,ja,zh-*,th,…}
etceteraWorks[](141): status · memo · etceteraWorkConfiguration.title · assignees[]{id,name,role{id,name,roleTags[]}}
purchaseIds[](148) · prescriptionIds[] · purchases[](전부 빈 배열) · occupiedResources[](177, 예약 그룹 점유)
taskTimers[](전부 빈 배열) · reactions[](전부 빈 배열) · zone{id,title}
```

#### 열거값 분포

| 필드 | 값 · 건수 |
|---|---|
| `flowStep` (177) | `COMPLETED` 151 · `RESERVED` 26 |
| `reservation.status` (177) | `COMPLETED` 151 · `CANCELED` 19 · `NO_SHOW` 7 |
| `flowStep × reservation.status × 접수 여부 × 작업 유무` | COMPLETED·COMPLETED·접수·작업 있음 145 / COMPLETED·COMPLETED·접수·작업 없음 6 / RESERVED·CANCELED·미접수 17 / RESERVED·NO_SHOW·미접수 7 / RESERVED·CANCELED·접수 2 |
| `tasks[].type` (719) | `PROCEDURE` 574 · `ETCETERA` 145 |
| `tasks[].status` (719) | `DONE` 702 · `CANCELED` 16 · `READY` 1 |
| `type × status` | PROCEDURE·DONE 567 · ETCETERA·DONE 135 · ETCETERA·CANCELED 9 · PROCEDURE·CANCELED 7 · ETCETERA·READY 1 |
| `tasks[].etceteraConfiguration.name` | ETCETERA 145건 전부 `방 점유/원장 상담` · PROCEDURE 는 빈 값 |
| `tasks[].anesthesiaType` | `ANESTHESIA_TYPE_UNSPECIFIED` 591 · `CREAM` 128 |
| `tasks[].urgencyLevel` | `URGENCY_LEVEL_UNSPECIFIED` 719 |
| 일정당 작업 수 | 0개 31 · 1개 7 · 2개 14 · 3개 29 · 4개 25 · 5개 28 · 6개 10 · 7개 6 · 8개 9 · 9개 5 · 10개 7 · 11개 4 · 12개 2 |
| 일정당 ETCETERA 수 | 1개 145 · 0개 32 |
| 일정당 쓴 방 수(작업 있는 146건) | 1개 123 · 2개 22 · 3개 1 |
| `etceteraWorks[].etceteraWorkConfiguration.title` | `문서 발급` 124 · `처방전 발급` 17 (status `COMPLETED` 140 · `CANCELED` 1) |
| `etceteraWorks[].assignees[].role` | name `코디` 140 · roleTags `COUNSELOR`·`CALL_COUNSELOR`·`COORDINATOR` 각 140 |
| `visitor.isNew` | true 159 · false 18 |
| `visitor.gender` | `FEMALE` 140 · `MALE` 36 · `GENDER_UNSPECIFIED` 1 |
| `visitor.nationality` | TW 97 · KR 25 · CN 24 · US 8 · HK 7 · JP 6 · TH 5 · FR 2 · PH 2 · IN 1 |
| `visitor.visitorType.name` | `이벤트가` 174 · 빈 값 3 |
| `visitor.snsInfo.snsType` | etc 87 · line 54 · wechat 20 · instagram 7 · whatsapp 7 · kakaotalk 2 |
| `reservation.connectedChannel` | `Channel_UNSPEICIFED` 174 · `HOMEPAGE` 3 |
| `zone.title` | `4층` 177 |

#### 직원 이름 칸 — 몇 종류, 몇 명(고유 id 수 / 채워진 건수)

| 필드 | 고유 id | 채워진 건수 | 비고 |
|---|---|---|---|
| `tasks[].doctors[]` | 7 | 557 / 719 작업 | 작업당 0–1명 |
| `tasks[].calledDoctors[]` | 6 | 227 | 호출된 의사 |
| `tasks[].assignees[]` | 13 | 649 / 719 작업 | 작업당 0–1명. **직군 표시 없음** |
| `consultations[].counselors[]` (= `consultation.counselor`) | 6 | 143 | 상담사 |
| `consultations[].consultationDoctors[]` (= `consultation.doctor`) | 2 | 11 | 원장 상담 |
| `reservation.reservationAssignee` | 12 | 175 | 예약 담당 |
| `etceteraWorks[].assignees[]` | 6 | 140 | role `코디` |
| `reservation.doctor` · `reservation.counselor` | 0 | 0 / 177 | **비어 있음** |

- 집합 겹침: 의사(doctors ∪ …) 7명 · 담당자(assignees) 13명 · 상담사 6명. 의사∩담당자 1명 · 담당자∩상담사 0 · 의사∩상담사 0. etceteraWorks 담당 6명은 reservationAssignee 와 6명 모두 겹치고 상담사와는 0명 겹친다.
- 같은 id 에 이름이 둘 이상인 경우 0건, 이름이 빈 id 0건 — **id↔이름은 일관된다.**
- 이름 칸이 8곳에 흩어져 있고 직원·직군 마스터는 캡처에 없다. 직군은 「어느 필드에 나왔나」로만 추정된다.

### B-4. 시각 정보

| 필드 | 채움 | 의미(실측으로 읽은 것) |
|---|---|---|
| `reservation.startDateTime` / `endDateTime` | 177 / 177 | 예약 슬롯(30분 단위) |
| `receptionDateTimeUtc` | 153 / 177 (86%) | 접수. 예약 시작 대비 중앙값 +0.1분(사분위 −9.5 ~ +6.2분) |
| `consultations[].consultationStartedDateTimeUtc` | 145 / 145 | 상담 시작(분 단위로 잘림) |
| `flowStepUpdatedDateTimeUtc` | 153 / 177 | 최종 단계(COMPLETED)로 바뀐 시각 ≈ 귀가. 마지막 작업 완료 뒤 중앙값 5.6분, 최대 878분(다음 날 일괄 마감으로 보임) |
| `tasks[].readyDateTimeUtc` | 716 / 719 | 작업 생성(대기 시작). 원장 상담 작업은 접수 직후, 시술 작업은 상담 뒤 **한꺼번에** 생김 |
| `tasks[].roomAssignedDateTimeUtc` | 710 / 719 | 방 배정. 대부분 ready 와 같은 시각(중앙값 0분). 다시 배정하면 **덮어씀**(원장 상담 72/135 · 시술 98/567 건이 ready 보다 5분 넘게 늦음) |
| `tasks[].doctorAssignedDateTimeUtc` | 608 / 719 | 의사 배정 |
| `tasks[].doctorCallDateTime` | 479 / 719 (67%) | 의사 호출. ready 뒤 중앙값 34분 · 완료 전 중앙값 32분 |
| `tasks[].completedDateTimeUtc` | 702 / 719 (DONE 은 100%) | 완료. 작업 2개 이상인 일정 138건 중 52건은 **모든 작업이 같은 분에 완료** — 일괄 처리 버튼 흔적 |
| `getScheduleStatistics` 체류 5종 | 109–153 / 177 | 접수 체류 중앙값 23분 · 상담 대기 4분 · 상담 45분 · 시술 대기 54분 · 시술 후 3분 (서버가 계산한 값) |

- 한 일정 안 작업들은 ready 순으로 놓으면 562쌍 중 558쌍이 **겹친다**(앞 작업이 끝나기 전에 다음 작업이 ready). 「작업 = 한 번에 하나씩 하는 단계」가 아니라 「오더에 올라간 항목」에 가깝다.
- **「지금 누가 어디 있나」 재구성**: 시각 t 에서 고객의 방 = 그 일정에서 `ready ≤ t < completed` 인 작업의 `room` (원장 상담 작업이 방 점유 구간 역할 — 접수 직후부터 마지막까지 열려 있다). 의사 = `doctorCall ≤ t < completed` 인 작업의 `doctors[]`. 담당자 = 열린 작업의 `assignees[]`. **할 수는 있지만 근사다.** (1) 방 이동 시점은 덮어써져 마지막 배정만 남는다. (2) 직원이 실제로 방에 「들어온」 시각은 없다(의사만 호출 시각이 있다). (3) 완료가 일괄로 찍혀 실제 끝난 시각보다 늦을 수 있다.

### B-5. 방 · 구역 vs BASE-003 도면

| 데이터 방(`tasks[].room.title`) | 작업 수 | BASE-003 도면 / 시안 대응 |
|---|---|---|
| `A_룸1` – `A_룸9` (9개) | 5 · 35 · 93 · 28 · 39 · 61 · 110 · 47 · 82 | 관리실(1인)과 같은 종류로 보인다. 번호 대응 근거 없음 |
| `A_트윈1-1` · `A_트윈1-2` | 69 · 69 | 2인관리실(1실 2자리)로 보인다 — 시안은 방 1개에 정원 2, 데이터는 자리마다 방 1개 |
| `A_시술실1` · `A_시술실2` | 46 · 7 | 도면·시안에 대응 없음 |
| `A_레이저실` | 19 | 도면·시안에 대응 없음 |
| (빈 방) | 9 | 방 미지정 작업 — DONE 8 · CANCELED 1 |

- 구역: `getZones` = `4층` 1건. 모든 일정의 `zone` · `visitorLocation.zoneId` · `doctorsCalledZone` 이 이 구역이다. 시안 제목은 「명동점 · 1층」(v3:27), BASE-003 도면은 관리실 01–16 · 2인관리실 01–03 · 수면시술실 01–03 · 다인상담실 · 라운지 · 인포 1–2.
- **방 마스터 API 가 없다** — 위 14개는 작업에 쓰인 방을 모은 것이라, 열흘 동안 안 쓴 방은 빠졌을 수 있다. `room.order` 는 전부 0 이라 순서 정보도 없다.
- 라운지 · 상담실 · 데스크 · 인포 · 수면실 · 원장실에 해당하는 방은 데이터에 없다. 상담(`consultations[]`)에는 방 필드가 없다.
- 캡처 데이터가 어느 지점인지 알려 주는 필드는 없다(`4층`·`A_` 접두어뿐). 시안의 명동점 1층과 같은 지점인지는 확인할 수 없다.

---

## C. 맞춰 보기 (질문 6~9)

### C-6. 매핑표

약어: `SD` = `getScheduleDetail.data` · `T` = `SD.tasks[]` · 「t」 = 재생 시각.

#### 현황판 v3 (55칸)

| # | 시안 칸 | 시안 근거 | 데이터 출처 | 판정 | 근거 · 가공 방법 |
|---|---|---|---|---|---|
| D01 | 지점명 | v3:20 | — | 없음 | 지점 필드 없음. 구역 `4층` 뿐 |
| D02 | 로그인 사용자명 | v3:20 | — | 없음 | 로그인 개념이 캡처에 없음 |
| D03 | 층 | v3:27 | `SD.zone.title` · `getZones` | 바로 됨 | 177/177 = `4층` |
| D04 | 역할 범례(고객 · 의사 · 상담사 · 코디) | v3:31–36, 473 | 필드 위치(`T.doctors` / `consultations[].counselors` / `T.assignees`) | 가공 | 직군 필드 없음. 이름이 나온 필드로 직군을 정하는 규칙 필요. assignees 13명의 직군은 추정 |
| D05 | 상태 범례(대기 · 상담 · 시술) | v3:40–45, 476–480 | — (시안 상수) | 가공 | 아래 D08 규칙으로 3상태를 만든다 |
| D06 | 방 목록 · 방 이름 | v3:61, 554–561 | `T.room.title` | 가공 | 14개를 작업에서 모은다(마스터 없음, `order` 전부 0) |
| D07 | 도면 좌표 · 복도 · 그리드 | v3:54–57, 550–561 | — | 없음 | 좌표 · 배치 데이터 없음 |
| D08 | 방 상태색(빈 방 · 직원만 · 대기 · 상담 · 시술) | v3:59, 578–584, 482–483 | `T.type` · `ready/doctorCall/completed` | 가공 | t 에 열린 작업 있음 → 고객 있음. 원장 상담(ETCETERA)만 열림 → 상담. PROCEDURE 열림 + `doctorCall ≤ t` → 시술. 그 외 → 대기. 「직원만」은 없음(직원 위치 없음) |
| D09 | 방 타이머(상태 진입 후 경과) | v3:62, 696 | `T.ready` · `roomAssigned` · `doctorCall` | 가공 | t − (현재 상태가 시작된 시각). 방 이동 시각은 덮어써짐 |
| D10 | 방 라벨(현재 단계명) | v3:64, 582 | `T.procedureConfiguration.medicalServiceConfiguration.title` · `etceteraConfiguration.name` | 가공 | 열린 작업이 여러 개(겹침 558/562) → 대표 하나를 고르는 규칙 필요 |
| D11 | 방 안 고객 이름 | v3:69, 697 | `SD.visitor.name` | 바로 됨 | 177/177. **개인정보 — §D** |
| D12 | 방 안 직원(점 · 이름) | v3:69, 697 | `T.assignees[]` · `T.doctors[]` | 가공 | 열린 작업에 붙은 사람. 「방에 들어와 있음」 시각은 없음(의사만 `doctorCall`) |
| D13 | 방 큐 대기 직원(「다음 ○」) | v3:74–83, 698 | — | 없음 | 직원 큐 개념 없음 |
| D14 | 빈 방 「비어있음」 | v3:704 | D06 + D08 | 가공 | 열린 작업 없는 방 |
| D15 | 쉬는 직원 위치(데스크 · 인포 · 상담실) | v3:687, 705 | — | 없음 | 직원 위치·쉬는 곳 없음 |
| D16 | 「수면 중 · 복귀 예정」 | v3:702 | `reservation.sedationRequired` | 없음 | 177/177 false. 수면실 방 없음. 「수면마취」 서비스는 마스터에만 있고 기간 내 사용 0 |
| D17 | 라운지 칸(대기 n명 · 고객별 대기 시간) | v3:691–692 | `SD.receptionDateTimeUtc` · 첫 `T.ready` | 가공 | 라운지 방은 없음. 「접수 ≤ t < 첫 방 점유」를 대기로 본다. 원장 상담 작업이 접수 직후 생기는 경우가 많아 대기 구간이 짧게 잡힐 수 있음 |
| D18 | 동선 화살표(직원 탭: 큐 순서) | v3:714–719 | — | 없음 | 직원 큐 없음. 과거 이동 경로(지난 방)라면 `T.assignees`+시각으로 가공 가능 |
| D19 | 동선 화살표(고객 탭: 라운지 → 방 → 수면실 → 복귀) | v3:720–726 | `T.room` 을 `ready` 순으로 | 가공 | 방 2개 이상 쓴 일정 23건. 라운지 · 수면실 칸은 없음 |
| D20 | 현황 요약 숫자(대기 · 상담 · 시술) | v3:200–207, 741–748 | D08 | 가공 | 상태별 방 수 + 라운지 인원 |
| D21 | 현황 목록 · 상태 배지 | v3:214, 750 | D08 | 가공 | `T.type`·시각 4종(ready 716 · doctorCall 479 · completed 702 / 719)로 D08 규칙 적용 |
| D22 | 현황 목록 · 방 이름 | v3:215 | `T.room.title` | 바로 됨 | 99% 채움 |
| D23 | 현황 목록 · 경과 | v3:217, 750 | D09 | 가공 | D09 와 같은 계산 · 시각 필드 채움률 §B-4 |
| D24 | 현황 목록 · 고객 이름 | v3:220 | `SD.visitor.name` | 바로 됨 | 개인정보 |
| D25 | 현황 목록 · 라벨 | v3:221 | D10 | 가공 | D10 과 같음 — 시술 작업 574건에 서비스 title 100% |
| D26 | 현황 목록 · 직원(직군 · 이름) | v3:224–229, 752 | D12 + D04 | 가공 | 열린 작업의 assignees(649/719) · doctors(557/719) + 직군 추정 |
| D27 | 현황 목록 정렬(경과 긴 순) | v3:759 | D09 | 가공 | D09 결과로 정렬 — 추가 필드 불필요 |
| D28 | 예약 요약(예정 · 접수 · 노쇼) | v3:799–803 | `reservation.status` · `receptionDateTimeUtc` | 가공 | 노쇼 = `NO_SHOW` 7. 접수 = `reception ≤ t`. 예정 = 그 외. 취소 `CANCELED` 19 는 시안에 칸 없음 |
| D29 | 「오늘 예약 N건」 | v3:128 | `reservation.startDateTime` 날짜별 개수 | 바로 됨 | 날짜별 6–27건(§C-8) |
| D30 | 예약 행 · 시각 | v3:134 | `reservation.startDateTime` | 바로 됨 | 177/177 (UTC → KST 변환만) |
| D31 | 예약 행 · 이름 | v3:137 | `SD.visitor.name` | 바로 됨 | 개인정보 |
| D32 | 예약 행 · 지연/곧 도착 | v3:138, 806–811 | `startDateTime` − t | 가공 | 미접수일 때만 |
| D33 | 예약 행 · 시술 | v3:140 | `reservation.requestedProcedures`(0/177) → 대체 `T…medicalServiceConfiguration.title` | 가공 | **예약 시점 요청 시술은 비어 있다.** 실제 받은 시술(사후 값)이나 `reservationMemo`(자유 문장)로 대체할 수밖에 없음 |
| D34 | 예약 행 · 담당 의사 | v3:140 | `reservation.doctor`(0/177) → 대체 `T.doctors[]` | 가공 | **예약 담당 의사는 비어 있다.** 사후 값으로 대체. 노쇼·취소 행은 작업이 없어 빈칸 |
| D35 | 예약 행 · 상태(접수 버튼 / 방 이름 / 귀가 / 노쇼) | v3:142–147, 814 | `reception` · D08 · `flowStepUpdatedDateTimeUtc` · `status` | 가공 | 귀가 = `flowStepUpdated ≤ t` |
| D36 | 직원 행 · 이름 | v3:159 | `T.assignees[].name` · `T.doctors[].name` · `consultations[].counselors[].name` | 바로 됨 | 고유 id 기준 의사 7 · 담당 13 · 상담 6. 개인정보(직원) |
| D37 | 직원 행 · 직군 | v3:160 | (필드 위치) · `etceteraWorks[].assignees[].role.name`(6명만) | 가공 | 직군 마스터 없음 — D04 와 같은 추정 |
| D38 | 직원 행 · 현재 방 · 업무 | v3:164–165, 768 | t 에 열린 작업의 `room` · 제목 | 가공 | 한 사람에게 열린 작업이 여러 개면 대표를 골라야 함 |
| D39 | 직원 행 · 다음(방 목록) | v3:166–167, 770 | 그 사람 앞으로 ready 되었지만 아직 시작 안 된 작업 | 가공 | 큐는 없으므로 「배정됐지만 미완료인 작업」으로 근사 |
| D40 | 직원 행 · 대기 N건(2건↑ 빨강) | v3:161, 772–773 | D39 개수 | 가공 | 근사 |
| D41 | 직원 행 · 비어있음 + 쉬는 곳 | v3:768 | — | 없음 | 비어 있음은 가공 가능하지만 쉬는 곳(데스크 · 원장실 등)이 없음 |
| D42 | 고객 행 · 상태 배지 | v3:180, 782 | D08 | 가공 | D08 과 같음 — 고객 단위로 그 고객의 열린 작업 기준 |
| D43 | 고객 행 · 이름 | v3:181 | `SD.visitor.name` | 바로 됨 | 개인정보 |
| D44 | 고객 행 · 현재 위치 | v3:183 | D17 / 열린 작업의 `room` | 가공 | 라운지는 D17 규칙 |
| D45 | 고객 행 · 오더 단계(번호 · 단계명 · 담당 직군 · 지남/지금/남음) | v3:186–192, 785 | `consultations[]` → 상담 · ETCETERA → 원장 상담 · PROCEDURE(sequence 순) → 시술 · 「크라이오 진정관리」 → 진정 | 가공 | 단계 종류 5개 중 `sleep`(수면) 없음. 담당 직군은 D04 추정. 지남/지금은 `completed`·`ready` 비교 |
| D46 | 접수 모달 · 이름 | v3:250 | `SD.visitor.name` | 바로 됨 | 개인정보 |
| D47 | 접수 모달 · 메타(성별 · 나이 · 차트번호 · 신규) | v3:251, 495–504 | `visitor.gender` · `dateOfBirth`(175) → 나이 · `chartNumber` · `isNew` | 가공 | 나이 계산. **차트번호 · 생년월일은 개인정보** |
| D48 | 접수 모달 · 예약 문구(시각 · 시술 · 담당) | v3:253, 834 | D30 · D33 · D34 | 가공 | D33 · D34 와 같은 한계 |
| D49 | 접수 모달 · 주의사항 | v3:255–259 | — | 없음 | 고객 주의 필드 없음. `medicalServiceConfiguration.caution` 0/574. 자유 메모 `visitor.memo` 12/177 · `reservationMemo` 174 · `orderMemo` 141 · `assigneeMemo` 237 은 내용이 주의인지 알 수 없음 |
| D50 | 접수 모달 · 보유 시술권(이름 · 잔여/총 회) | v3:262–271, 839 | `getTicketBundlesQuery.data[].ticketSets[]`(`title` · `tickets[].status`) · `T.procedureConfiguration.ticketConfiguration.round` | 가공 | 잔여 = `AVAILABLE` 수, 총 = 전체 수. 값 있는 고객 11/173. `round` 는 569/574 가 1/1 |
| D51 | 접수 모달 · 시술권 만료일 · 소진 | v3:839 | — | 없음 | 만료일 필드 없음. 소진(잔여 0)은 가공 가능 |
| D52 | 접수 모달 · 상담 필요 체크 | v3:275–281 | `reservation.consultationRequired` | 가공 | 177/177 false 로 정보가 없음 → `consultations[]` 존재 여부(145)나 `isNew` 로 대체 |
| D53 | 접수 모달 · 오늘 진행 순서 미리보기 | v3:284–299 | D45 와 같은 규칙 | 가공 | `T.sequence` 1..n 이 일정마다 연속(예: 1–4 95건) — 순서는 있음, 단계 종류는 D45 규칙 |
| D54 | 방 패널 · 방 이름 · 상태 · 타이머 | v3:312–316 | D06 · D08 · D09 | 가공 | 방 이름 99% 채움 · 상태·타이머는 D08·D09 |
| D55 | 방 패널 · 고객 이름 · 메타 · 주의 · 단계 | v3:325–338 | D11 · D47 · D49 · D45 | 가공 | 주의 부분은 「없음」(D49) |
| D56 | 방 패널 · 수면실로 이동 · 빈 수면실 | v3:340–349 | — | 없음 | 수면실 · 수면 시술 데이터 없음(D16) |
| D57 | 방 패널 · 현재 방 직원(빼기/완료) | v3:355–369 | D12 | 가공 | 「완료」 = `T.completedDateTimeUtc` 대응 |
| D58 | 방 패널 · 필요 직군 문구 | v3:368, 883 | 현재 단계 → 직군(D45 · D04) | 가공 | 열린 단계의 종류 → 직군. 직군 필드 없음(D04) |
| D59 | 방 패널 · 배정 대기 큐(앞 순서 N건 · 지금 위치) | v3:370–382, 885 | — | 없음 | 직원 큐 없음(D13) |
| D60 | 방 패널 · 직원 배정(직군 탭 · 직원 풀 · 상태 · 배정됨) | v3:385–411, 887–897 | D36 · D37 · D38 · D40 | 가공 | 직원 풀 = 그날 데이터에 나온 직원. 근무 명단은 없음 |
| D61 | 빈 방 패널 · 넣을 후보 · 빈 이유 | v3:415–433, 899–911 | D17(라운지 대기) | 가공 | 수면 후보 · 복귀 예정 문구는 없음(D16) |
| D62 | 라운지 패널 · 대기 고객(이름 · 대기 시간 · 오더 요약) | v3:436–450, 913 | D17 · D45 | 가공 | 대기 = reception(153/177) ~ 첫 방 점유 · 오더 = tasks 제목 나열 |
| D63 | 라운지 패널 · 배정할 관리실(빈방 / 2인 n/2) | v3:452–463, 917–920 | D06 · D14 · 정원 | 가공 | 정원 필드 없음 → `트윈` 이름 규칙 또는 트윈 1-1/1-2 를 한 칸으로 묶기 |

**집계(현황판 v3 · 63칸)** — 이름 칸(D11 · D24 · D31 · D43 · D46)은 같은 필드를 다른 영역에서 다시 쓰는 것이지만 화면 칸이 다르므로 각각 셌다.

| 판정 | 행 번호 | 수 |
|---|---|---|
| 바로 됨 | D03 · D11 · D22 · D24 · D29 · D30 · D31 · D36 · D43 · D46 | 10 |
| 가공 | D04 · D05 · D06 · D08 · D09 · D10 · D12 · D14 · D17 · D19 · D20 · D21 · D23 · D25 · D26 · D27 · D28 · D32 · D33 · D34 · D35 · D37 · D38 · D39 · D40 · D42 · D44 · D45 · D47 · D48 · D50 · D52 · D53 · D54 · D55 · D57 · D58 · D60 · D61 · D62 · D63 | 41 |
| 없음 | D01 · D02 · D07 · D13 · D15 · D16 · D18 · D41 · D49 · D51 · D56 · D59 | 12 |
| 합계 | | 63 |

#### 의사 모바일 (24칸)

| # | 시안 칸 | 시안 근거 | 데이터 출처 | 판정 | 근거 · 가공 방법 |
|---|---|---|---|---|---|
| M01 | 지점명 | mob:25 | — | 없음 | D01 과 같음 |
| M02 | 의사 이름(+직함) · 점 색 | mob:28–29 | `T.doctors[].{id,name}` | 바로 됨 | 의사 7명, id↔이름 일관. 직함(원장)은 없음 — 상수. 개인정보(직원) |
| M03 | 시계 | mob:30, 213 | — (재생 시각 t) | 가공 | 재생하면 가상 시계 |
| M04 | 지금 진행 중 · 방 | mob:43 | `doctorCall ≤ t < completed` 인 작업의 `T.room.title` | 가공 | `doctorCall` 67% — 없는 작업은 `doctorAssigned`(85%)나 ready 로 대체 |
| M05 | 지금 진행 중 · 고객 · 시술 | mob:44 | `SD.visitor.name` + 그 작업의 서비스 title | 가공 | 개인정보 |
| M06 | 지금 진행 중 · 경과 | mob:40 | t − `doctorCall` | 가공 | `doctorCall` 479/719(67%) — 없으면 `doctorAssigned`(608) 대체 |
| M07 | 「n / 전체 완료」 | mob:51 | 그 의사의 일정 수 · 완료 수 | 가공 | 일정 단위로 묶어야 함(의사 1명 하루 1–9명, §C-9) |
| M08 | 일정 행 · 시각 | mob:55 | `reservation.startDateTime` 또는 `doctorCall` | 가공 | 의사 개인 예약 시각은 없음(`reservation.doctor` 비어 있음) — 무엇을 「내 일정 시각」으로 볼지 규칙 필요 |
| M09 | 일정 행 · 고객 이름 · 방 | mob:57 | `visitor.name` · `T.room.title` | 가공 | 이름은 그대로, 방은 그 의사 작업의 방 |
| M10 | 일정 행 · 시술 | mob:58 | 그 의사 작업들의 서비스 title | 가공 | 한 일정에 작업이 여럿(최대 12) → 요약 규칙 |
| M11 | 일정 행 · 상태(완료 · 진행 중 · 다음 · 예정) | mob:60, 162–167 | `completed` · `doctorCall` · ready 순서 | 가공 | 「다음」 = 아직 호출 안 된 것 중 가장 이른 것 |
| M12 | 상세 · 라벨 · 타이머(대기/경과/예약) | mob:69–70, 231 | 대기 = t − ready · 경과 = t − doctorCall | 가공 | ready 716/719 · doctorCall 479/719 · 예약 = `reservation.startDateTime` 177/177 |
| M13 | 상세 · 이름 | mob:74 | `SD.visitor.name` | 바로 됨 | 개인정보 |
| M14 | 상세 · 메타(성별 · 나이 · 차트번호 · 신규) | mob:75 | D47 과 같음 | 가공 | 개인정보 |
| M15 | 상세 · 방 | mob:78 | `T.room.title` | 바로 됨 | 99% 채움(빈 방 9건) · 방 14개 |
| M16 | 상세 · 시술 계획 | mob:79 | `productOptionConfiguration.{productTitle,optionTitle}` · `unit` | 가공 | 작업 여러 개를 한 줄로 |
| M17 | 상세 · 주의사항 | mob:82–89 | — | 없음 | D49 와 같음 |
| M18 | 상세 · 진료 시작/완료 버튼 상태 | mob:90–95, 234–236 | `doctorCall`(시작) · `completed`(완료) | 가공 | 화면 동작의 결과가 두 시각에 대응 |
| M19 | 오늘 ○님 동선(방 · 업무 · 지남/지금/남음) | mob:98–106, 239–246 | 접수 + `T`(sequence 순 · room · title · completed) | 가공 | 「접수」 단계 = `receptionDateTimeUtc`. 라운지 방은 없음 |
| M20 | 상담 메모 · 본문 | mob:113 | `consultations[].content.text` | 바로 됨 | 143/145. **메모 본문 — 개인정보, 시연에 그대로 띄우지 말 것** |
| M21 | 상담 메모 · 작성자 | mob:111 | `consultations[].counselors[].name` | 바로 됨 | 143. 직원 이름 |
| M22 | 시술 이력(날짜 · 시술 · 시술자) | mob:118–127 | — | 없음 | 캡처 기간(11일) 밖. 기간 안 재방문 고객 4명뿐 |
| M23 | 방문 n회 | mob:119 | `visitor.isNew` · `isFirstProcedureSchedule` | 없음 | 횟수 필드 없음(신규 여부만) |
| M24 | 「첫 방문 고객」 | mob:129 | `SD.visitor.isNew` | 바로 됨 | true 159 / false 18 |

**집계(의사 모바일)** — 바로 됨 6(M02 · M13 · M15 · M20 · M21 · M24) · 가공 14(M03–M12 · M14 · M16 · M18 · M19) · 없음 4(M01 · M17 · M22 · M23) = 24

### C-7. 「데이터에 없음」 칸을 메우는 방법 후보 (고르지 않음)

| 칸 | 후보 |
|---|---|
| D01 지점명 · M01 | 설정 상수 · 사람 입력 |
| D02 로그인 사용자 | 시연용 고정값 · 실제 인증 연동 |
| D07 도면 좌표 | 시안 LAYOUT 를 그대로 쓰고 데이터 방 14개를 시안 칸에 대응시키는 표를 사람이 작성 · 데이터 방 14개에 맞춘 새 배치를 사람이 작성 · 실제 지점 도면(BASE-003 「나중에 매칭」)을 받아 그림 |
| D13 · D59 직원 큐 · D18 직원 동선 | 모의값(시안 규칙으로 생성) · 현황판에서 사람이 배정한 것만 큐로(데이터는 초기 상태만) · 「배정됐지만 미완료 작업」 근사(D39 방식)로 대체 |
| D15 · D41 쉬는 직원 위치 | 모의값 · 칸을 빼기 · 사람 입력 |
| D16 · D56 수면실 · 수면 시술 | 모의 수면 단계 추가 · 수면 칸을 시연에서 빼기 · 수면 시술이 있는 다른 기간·지점 추가 캡처(「수면마취」 서비스는 마스터에 있음) |
| D49 · M17 주의사항 | 모의값 · 자유 메모(`visitor.memo` 등)를 사람이 골라 넣기 · 상품 `getProducts.data[].cautions[]`(시술 일반 주의, 66개 상품)로 대체 · 사람 입력 |
| D51 시술권 만료일 | 모의값 · 다른 API(`getTicketGroupStatistics` — 이번 캡처에서 제외됨) 추가 캡처로 만료 필드가 있는지 확인 · 칸 빼기 |
| M22 시술 이력 · M23 방문 횟수 | 캡처 기간을 넓혀 추가 캡처 · 제외된 `getVisitorStatistics` 추가 캡처 · 모의값 · 「첫 방문/재방문」만 표시 |
| (가공 칸 공통) 직군 | 직원·직군 마스터 API 추가 캡처 · 사람이 직원 목록에 직군을 붙인 표 작성 · 필드 위치 추정(D04) |
| (가공 칸 공통) 방 마스터 · 정원 | 방 마스터 API 추가 캡처 · 사람 입력 · 이름 규칙 |

### C-8. 시연 재생 가능성

**상태 변화 이력은 없다 — 최종 상태와 「단계별 마지막 시각」만 있다.**
- `flowStep` 은 최종값 하나, `taskTimers[]` · `reactions[]` 는 177건 모두 빈 배열이다.
- 작업마다 시각 4–5개(ready · roomAssigned · doctorAssigned · doctorCall · completed)가 있어 **시각 순으로 펼치면 하루를 다시 그릴 수 있다.** 그래서 「실시간처럼」 움직이게 하는 것은 **가능하지만 근사**다.
  - 방 이동: 마지막 배정 시각만 남는다(덮어씀 — 원장 상담 72/135 · 시술 98/567).
  - 완료: 일괄로 찍힌 경우가 많다(작업 2개↑ 일정 138건 중 52건이 같은 분에 전부 완료). 실제보다 「한꺼번에 끝나는」 모양이 된다.
  - 직원 동선: 의사는 호출 시각이 있지만(67%), 담당자(assignees)는 방에 들어온 시각이 없다.

**날짜별 충실도** (예약 시작 날짜 KST · 동시 체류 = 접수~귀가 구간이 겹친 최대 인원 · 동시 사용 방 = 원장 상담 작업 열린 방 최대 수, 5분 간격 측정)

| 날짜 | 요일 | 일정 | 완료 | 취소 | 노쇼 | 작업 | 접수율 | 의사 | 담당자 | 동시 체류 최대 | 동시 사용 방 최대 | 예약 시각 범위 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10-01 | 목 | 21 | 12 | 7 | 2 | 83 | 57% | 4 | 5 | 5 | 5 | 10:00–18:30 |
| 10-02 | 금 | 12 | 9 | 3 | 0 | 53 | 75% | 3 | 6 | 6 | 6 | 10:00–17:30 |
| 10-03 | 토 | 6 | 6 | 0 | 0 | 22 | 100% | 3 | 6 | 4 | 3 | 10:00–16:30 |
| 10-04 | 일 | 25 | 22 | 3 | 0 | 103 | 88% | 3 | 6 | 10 | 9 | 10:00–17:30 |
| 10-05 | 월 | 20 | 18 | 0 | 2 | 79 | 90% | 3 | 8 | 8 | 7 | 10:00–17:30 |
| 10-06 | 화 | 10 | 10 | 0 | 0 | 39 | 100% | 4 | 6 | 5 | 4 | 12:00–18:30 |
| 10-07 | 수 | 12 | 12 | 0 | 0 | 34 | 100% | 5 | 5 | 5 | 5 | 10:30–20:00 |
| 10-08 | 목 | 12 | 10 | 0 | 2 | 49 | 83% | 3 | 7 | 3 | 3 | 10:00–18:00 |
| **10-09** | **금** | **27** | **26** | **1** | **0** | **126** | **100%** | **5** | **7** | **16** | **9** | 10:00–17:30 |
| 10-10 | 토 | 15 | 13 | 1 | 1 | 69 | 87% | 4 | 5 | 7 | 5 | 10:00–17:30 |
| 10-11 | 일 | 17 | 13 | 4 | 0 | 62 | 82% | 3 | 7 | 7 | 7 | 10:00–15:00 |

- **건수·필드 충실도로는 10-09(금)가 가장 좋다.** 일정 27(최다) · 작업 126(최다) · 접수율 100% · 의사 5명 · 동시 체류 최대 16명 · 방 14개 모두 사용. 정시 체류 인원은 10시 6 → 13시 8 → 16시 11 → **17시 16** → 18시 12 → 19시 5 명이다. 오후 늦게 몰리는 모양이다.
  - 단점: 노쇼가 0 이라 시안 예약 탭의 「노쇼」 칸이 0 으로 보인다.
- 차선은 10-04(일) — 일정 25 · 작업 103 · 동시 체류 10 · 방 9. 취소는 3건, 노쇼는 0건이다.
- 노쇼까지 보이려면 10-05(월 · 노쇼 2 · 동시 체류 8)나 10-01(목 · 노쇼 2, 단 접수율 57%)이 있다.
- 주의: 10-09 의 최종 마감(`flowStepUpdated`) 일부는 다음 날 오전에 찍혀 있다. 귀가 시각을 이 필드로 잡으면 밤까지 「체류 중」으로 남는 고객이 생긴다(20–21시 1명).

### C-9. 의사 모바일 — 「의사 한 명」으로 자르기

- **의사 식별은 일관된다.** `T.doctors[].id` 7개. 같은 id 에 다른 이름 0건. `calledDoctors` · `consultationDoctors` 도 같은 id 체계다(이름 칸 전체에서 id↔이름 불일치 0).
- 자르는 기준은 `T.doctors[].id` 밖에 없다. `reservation.doctor` 는 0/177 로 비어 있어 **「예약상 내 환자」 목록은 만들 수 없다.** 「실제로 내가 시술한 작업」 기준이다 → 아직 의사가 배정 안 된 미래 환자(시안의 「예정」)는 재생 시점 이전에 `doctorAssigned` 가 찍혀야 나타난다.
- 작업 중 의사 없는 것: PROCEDURE 128/574 · ETCETERA 34/145. 이 작업은 어느 의사 화면에도 안 나온다.
- 하루 의사 1명당 담당 환자 수(일정 수): 10-09 = 8 · 6 · 6 · 5 · 4명. 10-04 = 9 · 8 · 3명. 시안의 5명 리스트와 규모가 비슷하다.
- 판정: **의사 한 명으로 잘라 시안 칸을 채울 수 있다**(주의사항 · 시술 이력 · 방문 횟수 제외).

---

## D. 개인정보 · 데이터 품질 (질문 10~11)

### D-10. 개인정보 필드 — 시연 화면에 그대로 띄우면 안 되는 것 (값은 적지 않음)

| 구분 | 필드 경로 |
|---|---|
| 고객 이름 | `SD.visitor.name` · `SD.visitor.phoneticName` · `SD.consultations[].visitor.name` |
| 연락처 | `SD.visitor.phone.countryCode` · `SD.visitor.phone.phoneNumber` |
| 생년월일 · 나이 | `SD.visitor.dateOfBirth` (나이로 바꿔도 이름과 함께 쓰면 식별 위험) |
| 차트번호 | `SD.visitor.chartNumber` · `getScheduleStatistics/getProcedureTaskStatistics/getTransactionStatistics/getPurchaseItemStatistics .data[].visitorChartNumber` |
| 국적 · 성별 | `SD.visitor.nationality` · `SD.visitor.gender` · 각 통계 API `visitorNationality` · `visitorGender` (단독은 약하지만 조합하면 식별) |
| SNS | `SD.visitor.snsInfo.accountId` (+ `snsType`) |
| 자유 메모(본문) | `SD.visitor.memo` · `SD.reservation.reservationMemo` · `SD.consultation.consultationMemo` · `SD.consultations[].content.text` · `SD.orderMemo` · `T.assigneeMemo` · `T.memo` · `SD.etceteraWorks[].memo` · `getScheduleStatistics .visitorMemo/.reservationMemo` · `getTransactionStatistics .purchaseMemo` |
| 유입 상세 | `SD.reservation.funnel.funnelDetail` · 통계 API `visitorFunnelDetail` |
| 결제 | `getTransactionStatistics .cardApprovalNumber · .cardCompanyName · .incomeTaxDeductionNumber · .easyPayApprovalNumber` · 금액 필드 전반 |
| 직원 이름 | `T.assignees[].name` · `T.doctors[].name` · `T.calledDoctors[].name` · `consultations[].counselors[].name` · `consultationDoctors[].name` · `reservation.reservationAssignee.name` · `etceteraWorks[].assignees[].name` · 통계 API `*Names[]` · `getReservationRuleSummaries .lastModifiedBy.account.name` |
| 식별자 | `SD.visitor.id` · `SD.id` · 각 `*.id` (내부 id — 화면에 보일 이유 없음) |

- 시안이 이름 · 메타(성별 · 나이 · 차트번호) · 상담 메모 본문을 **화면 전면에** 띄운다(v3:69, 251 · mob:74–75, 113). 실데이터를 그대로 쓰면 이 칸들이 전부 개인정보가 된다.

### D-11. 데이터 품질 — 구현에 걸릴 것

| # | 문제 | 수치 · 경로 |
|---|---|---|
| Q1 | 예약 시점 의사 · 상담사 · 요청 시술이 비어 있음 | `reservation.doctor` 0/177 · `reservation.counselor` 0/177 · `reservation.requestedProcedures` 0/177 · `getScheduleStatistics.requested*[]` 0 · `consultations[].consultationProcedures` 0/145 |
| Q2 | 정보 없는 플래그 | `consultationRequired` · `sedationRequired` · `paymentRequired` 전부 false · `urgencyLevel` 전부 UNSPECIFIED |
| Q3 | 이력 대신 덮어쓰기 | `roomAssignedDateTimeUtc` 재배정 시 덮어씀(§B-4) · `flowStep` 최종값만 · `taskTimers[]`·`reactions[]` 전부 빈 배열 |
| Q4 | 일괄 완료 | 작업 2개↑ 일정 138건 중 52건이 모든 작업을 같은 분에 완료 |
| Q5 | 늦은 마감 | `flowStepUpdated − 마지막 작업 완료` 최대 878분(다음 날 마감). `getScheduleStatistics.procedureDoneDwellTimeMinute` 최대 878 · `durationMinute` 최대 1104 |
| Q6 | 방 미지정 작업 | `T.room.title` 빈 값 9건(DONE 8 · CANCELED 1) · `room.order` 전부 0 |
| Q7 | 작업 없는 완료 일정 | `flowStep=COMPLETED` 인데 `tasks[]` 빈 일정 6건 |
| Q8 | 취소인데 접수된 일정 | `reservation.status=CANCELED` 이면서 `receptionDateTimeUtc` 있음 2건(그중 1건은 작업도 있음) |
| Q9 | 테스트로 보이는 행 | 고객 이름에 「테스트/test」류 문자열 2건(10-07 COMPLETED 작업 0개 · 10-09 CANCELED 작업 0개) — 값은 적지 않음 |
| Q10 | 생년월일 이상값 | `visitor.dateOfBirth` 가 2026년인 행 3건(NO_SHOW · COMPLETED · CANCELED 각 1) · 빈 값 2건 — 기본값으로 들어간 것으로 보임 |
| Q11 | 의사·담당자 없는 작업 | `T.doctors[]` 빈 작업 162 · `T.assignees[]` 빈 작업 70 · `doctorCall` 빈 DONE 작업 223 |
| Q12 | 지점 · 층 불일치 | 데이터 `4층`·`A_` 방 14개 vs 시안 명동점 1층 33칸. 같은 지점인지 데이터로 확인 불가 |
| Q13 | 직군 미상 · 이름 칸 8곳 | 직원·직군 마스터 없음. 의사∩담당자 1명 겹침(한 사람이 두 역할) |
| Q14 | 다국어 · 외국인 비중 | 국적 KR 25/177 — 고객 상당수가 외국인. 메모 본문 언어는 확인하지 않음(값 열람 최소화) · 시술명 `translsMap` 은 17개 언어 |
| Q15 | 시술권 희소 | 보유 시술권이 있는 고객 11/173. `ticketConfiguration.round` 569/574 가 1/1 |

---

## 정할 것 — 코디 · 사용자가 결정할 항목 (결정하지 않음)

1. **방 배치 원천** — 시안 LAYOUT(명동점 1층 33칸) / 데이터 방 14개(4층) / 실제 지점 도면 중 무엇으로 시연하나. 데이터 방을 시안 칸에 대응시킬지.
2. **시연 데이터 원천** — 캡처 재생 / 모의값 / 섞기. 섞는다면 「없음」 칸(§C-7) 각각을 무엇으로 채우나.
3. **재생 날짜** — 10-09(최다 · 노쇼 0) / 10-04 / 노쇼가 있는 10-05 등.
4. **재생 규칙** — 「지금 어디 있나」를 어느 시각 필드로 정할지(§B-4 규칙의 대표 작업 고르기 · 일괄 완료 처리 · 늦은 마감 자르기). 재생 속도(실시간 / 배속).
5. **직군 판정** — 필드 위치 추정을 그대로 쓰나, 직원 목록에 사람이 직군을 붙이나. assignees 13명을 「코디」로 볼지.
6. **직원 큐 · 쉬는 위치 · 수면실** — 시안에서 빼나, 모의로 보여 주나, 현황판에서 사람이 조작한 것만 반영하나.
7. **개인정보 처리** — 이름 · 메타 · 메모를 가명 · 마스킹 · 모의 이름 중 무엇으로. 상담 메모 카드를 실데이터로 보여 줄지. 데이터 파일을 시연 장비 · 앱 레포에 둘지(지금은 프로필 레포 `reference/` 에 있음).
8. **주의사항 · 시술 이력 · 방문 횟수 · 시술권 만료** — 칸을 빼나, 모의로 채우나, 추가 캡처(제외된 `getVisitorStatistics` · `getTicketGroupStatistics`, 더 긴 기간)를 하나.
9. **예약 탭의 시술 · 담당 의사** — 비어 있는 예약값 대신 사후 값(실제 받은 시술 · 실제 의사)을 보여 줘도 되나.
10. **취소(CANCELED 19) 표시** — 시안에 칸이 없다. 숨기나, 칸을 더하나.
11. **테스트 행 · 이상값(Q7–Q10) 처리** — 재생에서 거를지.
12. **OQ-004 연계** — 통역(sts)을 넣을 화면이 의사 모바일인지(외국인 고객 비중이 높다는 사실 — 국적 KR 25/177 — 은 판단 재료).

---

## 출처 목록

**시안** (`/Users/kknaks/git/toy_pr2/cc-prototype/cc/design/`)
- `README.md` — 사본 경위 · 샘플 데이터 고지
- `Ceramique 현황판 v3.dc.html` — 마크업 19–470 · 상수 473–561(직군 · 상태 · 단계 · 샘플 고객/직원/예약 · LAYOUT) · 계산 566–600 · 동작/뷰 602–999
- `Ceramique 의사 모바일.dc.html` — 마크업 19–135 · 상수 138–167 · 뷰 170–250

**데이터** (`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/`)
- `manifest.json` — environment · 기간 · groups · jobs · `scopeNotes` · `excludedOperations` · `relatedIdCounts`
- `raw/getScheduleDetail/*.json` (177) — 필드 트리 · 열거값 · 시각 · 직원 id · 방 · 재생 분석
- `raw/getScheduleStatistics/*.json` (1) — 체류 시간 5종 · 예약 상태
- `raw/getProcedureTaskStatistics/*.json` (2) — 완료 시술 작업 702
- `raw/getZones/*.json` · `raw/getReservationGroups/*.json` · `raw/getReservationRuleSummaries/*.json`
- `raw/getMachines` · `getProcedures` · `getMedicalServices` · `getMedicines` · `getProducts` · `getCategories` · `getTargetCountries`
- `raw/getTicketBundlesQuery/*.json` (173) — 시술권 상태
- `raw/getVisitorPrepaidCardBalance` · `getPrepaidCardSummaries` · `getPrepaidCardChargingEvents(+Statistics)` · `getPurchaseSummaries` · `getPurchaseItemStatistics` · `getTransactionStatistics` — 구조만 확인(현황판 칸과 무관)

**제품 맥락**
- `para/projects/summer-star/cc-prototype/00-baseline/baseline-003-cc-idea.md` — 도면 구역표 · 열린 질문
- `para/projects/summer-star/cc-prototype/10-decision/decision-001-feature-lab.md` — D-04 스택 · D-06 sts→cc · OQ-004
