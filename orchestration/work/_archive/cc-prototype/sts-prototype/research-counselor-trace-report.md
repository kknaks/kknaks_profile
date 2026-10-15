# 상담사가 남긴 정보 추적 (2026-10-13)

- 조사자: cc-prototype `researcher` 워커. KOS 호출 0회. 캡처 · 스펙 · 앞 조사 · 직원 목록 저장본만 읽었다. 이 리포트 말고 만든 파일 없음
- 캡처: `reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/`(이하 `CAP/`) — 2026-10-01 ~ 10-11(KST) 11일 · 일정 177 · 상담 기록 145
- 직군: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/kos-staff.json`(`getAccounts` 저장본 88명, `kos-staff-api-report.md`). `roleTags` 에 `COUNSELOR` 가 있는 계정은 **29명**인데, 상담 기록 `counselors[]` 에 실제로 나오는 사람은 **6명**이다 — 설지호 · 류하린 · 문하람 · 오현우 · 민현우 · **윤나연**
  - ⚠ 윤나연(`6a962c31…`)는 `roleTags` = ADMIN · NURSE · SKINCARE · CALL_COUNSELOR · COORDINATOR 로, **COUNSELOR 태그가 없다.** 그래도 상담 1건(`getScheduleDetail/0000088.json`)의 상담사로 들어가 있다. 태그로만 상담사를 고르면 이런 경우를 놓친다
  - COUNSELOR 태그는 코디(곽태린 · 심준서 · 주태윤 · 남준서 · 차예린 · 정재희)와 공용 계정(`세라미크 명동`, `room01~10` 등)에도 붙어 있다
- 스펙: `/Users/kknaks/git/ax-clinic-project/para/archive/inbox_archive/2026-09-18-kos-openapi.yaml`(이하 `SPEC`, 2026-09-18 스냅샷)
- 표기: **사실** = 캡처에 있는 값과 건수. **추정** = 해석. 시각은 KST
- 고객 이름 점검: 캡처 `visitor.name` · `consultations[].visitor.name` 173개 전부와 이 리포트를 대조 — 걸린 문자열은 강도윤 · 차예린 2개인데, 둘 다 **같은 이름의 직원**(간호사 · 코디)을 가리킨 자리다. 고객 이름 0건 · 전화번호 0건

---

## 결론 한 장

**상담사가 KOS 에 남기는 것(사실)**

| # | 어디 | 무엇 | 언제(캡처 시각으로) | 건수 |
|---|---|---|---|---|
| 1 | 일정 `consultations[]`(상담 기록 1개 = 방문 1회) | `counselors[]` 에 자기 이름 · `content.text` 에 상담 메모 | 기록 **생성**: 접수 뒤 중앙값 6분(대개 방에 들어가는 때, ETC 작업 ready 와 중앙값 0.5분 차이) · 최종 **수정**: 생성 뒤 중앙값 77분, **결제 뒤에도** 고친다(138건 중 126건이 첫 구매 생성 뒤에 마지막 수정) | 145 기록 / 상담사 있음 143 |
| 2 | 상담 메모 본문 | `[상담내용]`(고민 · 이력 · 추천) + `------` 아래 **오더지 사본**(`이름 · ROOM NO. · 실장 : <본인> · Dr:` 머리 + `[진단기]` · `OUT TIME` · 번호 매긴 시술 · `[특이사항]` · `[임플란트 여부]`) | 위와 같음 | 오더지 머리 `실장 :` 줄 117건, 그 이름 = 상담사 116건 |
| 3 | 결제(구매) `getPurchaseSummaries.assignees[]` | 구매 담당 = 그 방문의 상담사 | 구매 생성: 상담 기록 생성 뒤 중앙값 38분 | 168 구매 중 **160** 이 상담사와 같음(나머지 2건 다름 · 6건 상담 없음) |
| 4 | 결제 거래 `transactions[].assignee` | 거래 담당(스펙: 「거래 담당자」) | 결제 승인: 상담 기록 생성 뒤 중앙값 74분 | 173 거래 중 157 이 상담사와 같음 |
| 5 | 예약 메모 `reservation.reservationMemo` | 끝에 `/민현우` 처럼 서명한 줄(할인 · 희망 시술 · 다음 방문 지정) | 시각 없음 | 서명 줄이 있는 일정 7건(민현우만) |

**상담사가 남긴다고 데이터로 말할 수 없는 것**

- **오더 메모 `orderMemo` 작성자** — 작성자 · 작성 시각 칸이 없다(데이터에 없음). 다만 `orderMemo` 가 상담 메모 `------` 아래와 공백 제거 후 **통째로 같은 게 87/137건**이고, 3건은 오더 메모 안에 `실장 : <상담사>` 줄까지 들어 있다 → 상담사가 쓴 오더지를 옮겨 붙인 것으로 **추정**
- **상담 시술 `consultationProcedures`** — 스펙에는 있지만(상품 옵션 / 시술권), **145건 전부 빈 배열.** 상담사는 상담 시술을 구조로 남기지 않는다. 무엇을 권했는지는 메모 글로만 있다
- **상담 결과 `result`**(스펙: 상담 결과 이름 · 색상) — 145건 모두 키 자체가 없다
- **희망 상담사 `reservation.counselor`** — 177건 모두 빈 값. 「다음엔 이 상담사」는 예약 메모 글로만 남는다(「다음 내원시 상담 '문하람' 실장님으로 지정」 3건)
- **시술권 생성 · 시술 작업 ready 를 누가 했나** — 담당 칸이 없다. 시각만 보면 **결제 승인 → 시술권 생성(약 1초) → 시술 작업 ready(중앙값 0.2분)** 가 한 번에 일어난다(사실). 결제 담당이 상담사이니 상담사가 결제부터 작업 등록까지 한 화면에서 끝낸다는 것은 **추정**(누른 사람 칸이 없음)

---

## 1. 상담사와 연결된 모든 칸

### 순회 방법

`CAP/raw/` 의 **21개 API 폴더 · 모든 JSON 파일**을 `python3` 로 재귀 순회했다. 배열 첨자는 `[]` 로 접어 경로를 만들고, **모든 문자열 값**을 다음과 대조했다.

1. 값이 `COUNSELOR` 태그 직원 29명 + 윤나연의 **id 와 같다** → id 칸
2. 값이 그 사람들의 **이름과 같다** → 이름 칸(exact)
3. 값 **안에 이름이 들어 있다** → 글 칸(text)

추가로 키 이름에 `counsel · assignee · consult · creat · author · regist · writer · manag · staff · account · doctor · user` 가 들어간 모든 칸을 따로 세서, 값이 비어 있는 상담사 칸(예: `reservation.counselor`)까지 잡았다. 「상담6」 = 실제 상담 기록에 나온 6명, 「기타」 = COUNSELOR 태그가 붙은 코디 · 공용 계정.

### 표 — 상담사가 등장하는 칸

| API | 경로 | 건수(상담6 / 기타) | 뜻(SPEC) | 비고 |
|---|---|---|---|---|
| getScheduleDetail | `data.consultations[].counselors[].id · name` | 143 / 0 | 상담사 목록 (`ConsultationContract`, SPEC:21711) | 상담 기록 145 중 143(빈 2) — 원천 |
| getScheduleDetail | `data.consultation.counselor.id · name` | 143 / 0 | 상담사 (`ScheduleDetailConsultationContract`, SPEC:23789) | 위와 177/177 같음(파생 사본) |
| getScheduleDetail | `data.consultations[].content.text` | 117 / 0 (글) | 상담 내용 텍스트 (SPEC:21684 근처 `ConsultationContent.text`) | 오더지 머리 `실장 : <이름>` 줄 |
| getScheduleDetail | `data.consultation.consultationMemo` | 117 / 0 (글) | 상담 메모 | `content.text` 와 177/177 같음(앞 조사) |
| getScheduleDetail | `data.orderMemo` | 2 / 0 (글) | 오더 메모 (SPEC:23706) | `실장 :` 줄이 오더 메모에 들어온 경우(전체 3건 중 상담6 이름 2) |
| getScheduleDetail | `data.reservation.reservationMemo` | 11 / 0 (글) | 예약 메모 | `/민현우` 서명 · 「상담 '문하람' 실장님으로 지정」 |
| getScheduleDetail | `data.reservation.funnel.funnelDetail` | 1 / 0 | 예약 유입 경로 상세 | 값 `류하린` — 직원 소개 유입으로 보임(추정) |
| getScheduleDetail | `data.reservation.reservationAssignee.id · name` | 5 / 157 | 예약 담당자 | 대부분 코디(곽태린 62 · 주태윤 34 · 남준서 30 …). 상담6 은 5건(오현우 · 설지호) |
| getScheduleDetail | `data.etceteraWorks[].assignees[]` | 0 / 140 | 부가 업무 담당 | 전부 코디(`role.name` = 코디 140). 상담사 없음 |
| getScheduleDetail | `data.tasks[].assignees[]` | 0 / 1 | 작업 담당자 | 남준서 1건. 상담사는 시술 작업 담당에 **0건** |
| getScheduleDetail | `data.reservation.counselor.id · name` | **0** (177 전부 빈 값) | 희망 상담사 (SPEC:23869) | 쓰이지 않음 |
| getScheduleDetail | `data.consultation.doctor` / `consultations[].consultationDoctors[]` | — | 상담 의사 | 11건(심주원 6 · 권태윤 5). 상담사 아님 |
| getScheduleStatistics | `data[].counselorNames[]` | 143 / 0 | 상담사 이름 목록 (SPEC:13441) | 일정의 상담사와 177/177 같음 |
| getScheduleStatistics | `data[].consultationDwellTimeMinute` · `consultationWaitingDwellTimeMinute` | 141 · 130 | 상담 진행 / 상담 대기 단계 체류 시간(분) (SPEC:13433-13440) | 상담사 칸은 아니지만 상담 시간. 중앙값 45분 / 4분 |
| getScheduleStatistics | `data[].reservationAssigneeName` · `reservationMemo` · `reservationFunnelDetail` · `visitorFunnelDetail` | 5/157 · 11 · 1 · 1 | 상세의 사본 | |
| getPurchaseSummaries | `data[].assignees[].id · name` | 162 / 6 | 담당자 목록 (`PurchaseSummary`, SPEC:18645) | 구매 168건 모두 1명 |
| getPurchaseSummaries | `data[].assignee.id · name` | 162 / 6 | 담당자 — **Deprecated** (SPEC:18636) | `assignees[0]` 과 168/168 같음 |
| getPurchaseSummaries | `data[].transactions[].assignee.id · name` | 159 / 14 | 거래 담당자 (`PurchaseSummaryTransaction`, SPEC:18783 근처) | 거래 173 |
| getPurchaseItemStatistics | `data[].assignees[]` | 538 / 9 | 담당자 목록 (SPEC:13019) | 구매 담당과 547/547 같음 |
| getPurchaseItemStatistics | `data[].counselorNames[]` | 531 / 0 | 상담사 이름 목록 (SPEC:13031) | 일정 상담사와 531/531 같음, 16행은 빈 배열(상담 없는 방문) |
| getTransactionStatistics | `data[].assigneeName` | 159 / 14 | 담당자명 (SPEC:13901) | 거래 담당 사본(173/173) |
| getTransactionStatistics | `data[].purchaseAssigneeNames[]` | 163 / 10 | 담당자명 목록 (SPEC:13952) | 구매 담당 사본(173/173) |
| getProcedureTaskStatistics | `data[].counselorNames[]` | 681 / 0 | 상담사 이름 목록 (SPEC:12686) | 일정 상담사와 702/702 같음 |
| getProcedureTaskStatistics | `data[].assigneeNames[]` | 0 / 1 | 작업 담당 | 남준서 1 |
| getProcedureTaskStatistics · getPurchaseItemStatistics · getTransactionStatistics | `visitorFunnelDetail` · `reservationFunnelDetail` | 1~2 | 유입 경로 상세 | 값 `류하린` |
| getPrepaidCardChargingEventStatistics | `data[].assignees[]` | 0 / 1 | 담당자 목록 | 남준서 1 |

- 나머지 API(`getCategories` · `getMachines` · `getMedicalServices` · `getMedicines` · `getPrepaidCardChargingEvents` · `getPrepaidCardSummaries` · `getProcedures` · `getProducts` · `getReservationGroups` · `getReservationRuleSummaries` · `getTargetCountries` · `getTicketBundlesQuery` · `getVisitorPrepaidCardBalance` · `getZones`)에는 상담사 id · 이름이 **0건**
- `getScheduleDetail.data.visitor.name` 에도 직원 이름과 같은 문자열이 2건 걸렸는데, **고객 이름이 우연히 같은 것**이라 표에서 뺐다
- 스펙에만 있고 캡처에 없는 상담사 칸: 만족도 조사 `EvaluationTarget.counselor`(「상담 담당자를 평가 대상으로 하는 경우」, SPEC:22770) — 캡처 범위에 만족도 API 없음

**정리(사실)**: 상담사 원천 칸은 **두 개뿐**이다 — 상담 기록 `consultations[].counselors[]` 과 구매 `assignees[]`(+ 거래 `assignee`). 통계 API 의 `counselorNames` 는 모두 일정의 상담사를 그대로 붙인 사본이다(어긋남 0).

---

## 2. 상담 기록 `consultations[]`

출처: `CAP/raw/getScheduleDetail/*.json` 177개, `data.consultations[]`

| 칸 | 실측 | 건수 |
|---|---|---|
| 개수 | 일정 1개에 0 또는 1개. **2개 이상 0건** | 있음 145 / 없음 32(취소 18 · 노쇼 7 · 완료 7) |
| `id` · `scheduleId` | 상담 id 145개 모두 다름. `scheduleId` = 그 일정 id 145/145 | |
| `visitor.isNew` | 「상담 생성 시점의 신규 내원객 여부」(SPEC:`ConsultationVisitor`). 일정 `visitor.isNew` 와 다름 3건(상담 시 True → 지금 False) | True 140 · False 5 |
| `counselors[]` | 1명 143 · 빈 배열 2 | 설지호 32 · 류하린 31 · 문하람 28 · 오현우 26 · 민현우 25 · 윤나연 1 |
| `consultationDoctors[]` | 0명 134 · 1명 11 | 심주원 6 · 권태윤 5 |
| `consultationProcedures[]` | **145건 전부 빈 배열** | 0 |
| `result`(상담 결과) | **키 없음** 145/145 | 0 |
| `content.text` | 비어 있지 않음 143(빈 2). 길이 45~612자, 중앙값 294 | |
| `consultationStartedDateTimeUtc` | **분 단위 값 92건 = 예약 시작 시각과 정확히 같음** · 초 단위 값 53건 = `createdDateTimeUtc` 와 같은 순간(차 0분) | 145 |
| `createdDateTimeUtc` | 접수 뒤 중앙값 6분(p25 2 · p75 14). 접수보다 앞 4건 | 145 |
| `updatedDateTimeUtc` | 생성 뒤 중앙값 77분(p25 49 · p75 119). **하루 넘게 뒤 9건**(최대 약 5.2일) · 마지막 작업 완료 뒤 수정 30건 | 145 |

→ `consultationStartedDateTimeUtc` 는 **실제 상담 시작을 찍은 값이 아니다**(사실: 예약 시작 또는 기록 생성 순간의 복사). 실제 상담 시간에 가까운 값은 통계의 `consultationDwellTimeMinute`(상담 단계 체류, 141건 중앙값 45분 · 2~151분)와 `consultationWaitingDwellTimeMinute`(130건 중앙값 4분)다 — `getScheduleStatistics`

### `content.text` 양식

머리 태그(143건 중): `[상담내용]` 142 · `[진단기]` 141 · `[특이사항]` 118 · `[임플란트 여부]` 114. `------` 구분선 142. 위쪽 줄머리: `H)`/`h)`(이력) 53 · `N)` 30 · `고민` 6 · `추천` 5.

예시(`getScheduleDetail/0000144.json`, 상담사 문하람, 고객 이름 가림):

```text
[상담내용]
*유학생(한국어 잘하심)
h) 몇년전 물광주사,+피코토닝 /리쥬란 포텐자 보톡스 보고 오심
고민) 딱히 없다고 하심 / 나중에 눈밑지방재배치 하실 예정
추천 : 올리디아 리쥬란 포텐자 턱보톡스
----------------------------------
이름 : <고객> ROOM NO.9
실장 :   문하람      Dr:
[진단기] O
OUT TIME : x
0. 자가세안 O
1. 포텐자모공팁
2. 리쥬란힐러2cc 인젝 양볼위주
3. 턱보톡스100u 하이톡스

[특이사항] x
[임플란트 여부] x
```

- `------` 아래 오더지 머리 `실장 : <이름>` 이 있는 117건 중 **116건이 `counselors[]` 와 같은 이름**. 다른 1건은 `counselors[]` 가 빈 기록(`실장 : 설지호`) — 상담사 칸이 비어도 메모 안에는 이름이 있다
- `ROOM NO.` 값: 7 19 · 3 16 · 6 14 · 9 14 · 8 11 · 트윈 1-1/1-2 계열 26 … — 상담사가 **상담한 방 번호**를 메모에 적는다(사실). 이 값과 작업 `room` 의 관계는 이번에 재지 않았다

### `consultationProcedures` 구조(스펙만 — 캡처 0건)

SPEC:21906 `ConsultationProcedure` — `type` = `OPTION`(상품 옵션) | `TICKET`(시술권)

- `OPTION` → `optionConfiguration`(`ConsultationOptionConfiguration`, SPEC:21758): 상품 옵션 `id` · `title` · `optionType` · `compositions` … → 결제 품목 `items[].optionConfiguration.id` 와 같은 상품 옵션 id 공간으로 **추정**(캡처로 확인 불가)
- `TICKET` → `ticketConfiguration`(SPEC:21983 근처): `ticketId`(시술권 ID) · `ticketTitle` · `optionTitle` · `productTitle` · `medicalService` → 작업 `procedureConfiguration.ticketConfiguration.ticketId` · `getTicketBundlesQuery.ticketSets[].tickets[].id` 와 이어질 것으로 **추정**
- **캡처에서는 145건 모두 비어 있어 어떻게 이어지는지 데이터로 보이지 않는다.** 상담사가 무엇을 권했는지는 `content.text` 아래쪽 번호 목록(글)에만 있다

### 쓰기 API(스펙)

`updateScheduleConsultationInfo`(SPEC:2230, 「스케줄 상담 정보 수정」) 요청 `OpenUpdateScheduleConsultationInfoCommand`(SPEC:14430) 의 칸은 **`scheduleId` · `consultationMemo` 두 개뿐**이다. 2026-09-18 스냅샷 기준으로 **상담사(`counselor`) 를 쓰는 칸은 없다** → `workflow.md` §4 의 「상담사 = `consultation.counselor` — 후보 `updateScheduleConsultationInfo`(필드 확인 필요)」 의 답: 이 작업으로는 상담 메모만 바꿀 수 있다(현재 공개 스펙 75개는 이번에 보지 않음).

---

## 3. 한 방문의 시간 순서

### 예시 1 — `getScheduleDetail/0000069.json` (10-09, 상담사 민현우)

| KST | 사건 | 칸 |
|---|---|---|
| 09:58:34 | 접수 | `receptionDateTimeUtc` |
| 10:00:00 | 예약 시작 | `reservation.startDateTime` |
| 10:00:32 | 상담 기록 생성 (= `consultationStartedDateTimeUtc`) | `consultations[].createdDateTimeUtc` |
| 10:09:37 | ETC 작업 「방 점유/원장 상담」 ready(담당 유채원) | `tasks[].readyDateTimeUtc` |
| 10:32:33 | 구매 생성(담당 **민현우**, 3품목) | `getPurchaseSummaries.createdDateTimeUtc` · `assignees[]` |
| 11:27:23 | ETC 작업 방 배정 | `roomAssignedDateTimeUtc` |
| 11:33:12 | 상담 기록 최종 수정 | `consultations[].updatedDateTimeUtc` |
| 11:39:55 | 결제 승인 CARD(거래 담당 **민현우**) | `transactions[].paymentDateTime.approvedDateTimeUtc` |
| 11:40:05 | 시술 작업 3개(리쥬란) 방 배정 · ready 동시(담당 유채원) | `tasks[]` |
| 12:27:02 | 작업 4개 완료 | `completedDateTimeUtc` |
| 13:05:59 | `flowStep` = COMPLETED | `flowStepUpdatedDateTimeUtc` |

통계: 상담 대기 9분 · 상담 72분(`getScheduleStatistics`)

### 예시 2 — `getScheduleDetail/0000077.json` (10-09, 상담사 오현우)

| KST | 사건 |
|---|---|
| 09:58:01 | 접수 |
| 10:00:56 | 상담 기록 생성 |
| 10:11:45 | ETC 「방 점유/원장 상담」 방 배정 · ready(담당 서가온) |
| 11:26:35 | 구매 생성(담당 **오현우**, 3품목) |
| 11:56:00 | 상담 기록 최종 수정 |
| 11:56:20 | 결제 승인 CARD(거래 담당 **오현우**) |
| 11:57:04 | 시술 작업 3개(라라필 · 포텐자 · 쥬베룩) 방 배정 · ready 동시(담당 서채원 · 강도윤) |
| 12:39~13:02 | 작업 완료 |
| 13:24:38 | COMPLETED |

### 예시 3 — 시술권 생성 시각이 보이는 일정 `db971253…`(10-09 13:00 예약)

상담 기록 생성 13:06:33 → 구매 생성 13:37:56 → **결제 승인 13:59:35.2 → 시술권 생성 13:59:35.9 → 시술 작업 ready 13:59:43.** 시술권 `createdDateTimeUtc` 는 `getTicketBundlesQuery` 에만 있는데, 그 응답은 **조회 당시 남은 시술권**만 준다(`manifest.json scopeNotes`). 그래서 173 고객 중 11명 · 24묶음만 있고, 상담 기록 있는 일정의 시술 작업 566개 중 6개(일정 2개)만 가리키는 시술권의 생성 시각을 찾았다(모두 결제 승인 뒤 1초 안).

### 전체 통계 (상담 기록 145건 기준)

| 구간 | n | 중앙값(분) | p25~p75 | 순서가 거꾸로 |
|---|---|---|---|---|
| 접수 → 상담 기록 생성 | 145 | 6 | 2 ~ 14 | 4 |
| 접수 → ETC 「방 점유/원장 상담」 ready | 143 | 6.5 | 3.8 ~ 12.9 | 4 |
| 상담 기록 생성 ↔ ETC ready | 143 | 0.5 | −0.7 ~ 4.2 | 50(ETC 가 먼저) |
| 상담 기록 생성 → 첫 구매 생성(같은 날) | 138 | 38 | 24 ~ 56 | 2 |
| 상담 기록 생성 → 첫 결제 승인 | 132 | 74 | 50 ~ 95 | 0 |
| 첫 구매 생성 → 상담 기록 최종 수정 | 138 | **+32**(구매 뒤) | +10 ~ +71 | 12(수정이 먼저) |
| 첫 결제 승인 → 첫 시술 작업 ready | 131 | **0.2** | 0.1 ~ 1.0 | 1 · 2분 안 108 |
| 첫 구매 생성 → 첫 시술 작업 ready | 136 | 24 | 11 ~ 43 | 1 |
| 시술 작업 ready 가 첫 구매보다 앞 | 564 작업 | | | 3 |

- ETC 작업은 145건 모두 제목이 「방 점유/원장 상담」이다
- 데이터로 보이는 순서(사실): **접수 → 상담 기록 생성 ≈ 방 점유 ready → 구매 생성 → (상담 메모 계속 수정) → 결제 승인 → 즉시 시술권 생성 · 시술 작업 ready → 시술 → 완료**
- **「상담사가 결제 · 오더를 같이 하나」**
  - 결제: 구매 담당 160/168 · 거래 담당 157/173 이 그 방문의 상담사다(사실). 「담당」이 버튼을 누른 사람인지는 스펙에 없다(추정)
  - 시술 작업 등록(오더): 작업 ready 가 결제 승인 뒤 중앙값 12초(0.2분)라 같은 흐름에서 일어난다(사실). 등록한 사람 칸은 **데이터에 없음**
  - 시술 작업 `tasks[].assignees` 에 상담사는 0건 — 상담사는 시술 담당이 아니다(사실)

---

## 4. 오더 메모와의 관계

출처: `getScheduleDetail.data.orderMemo` · `data.consultations[0].content.text`

| 항목 | 값 |
|---|---|
| `orderMemo` 있음 | 141/177 |
| 둘 다 있음 | 137 |
| 오더 메모 전체가 상담 메모 안에 그대로(공백 제거 후 포함) | **87/137** (앞 조사와 같음) |
| 오더 메모만 있고 상담 기록 없음 | 3 |
| 상담 메모는 있는데 오더 메모 없음 | 6 |
| 오더 메모 안에 `실장 : <이름>` 줄 | 3 (이름이 상담6 인 것 2: 설지호 · 윤나연) |

- **오더 메모를 누가 쓰는지 알려 주는 칸 → 데이터에 없음.** `orderMemo` 는 일정의 문자열 하나다(SPEC:23706 「오더 메모」). 작성자 · 작성 시각 · 수정 시각 칸이 없고, 일정 `updatedDateTimeUtc` 는 일정 전체의 시각이라 구분할 수 없다
- 2026-09-18 스냅샷에 `orderMemo` 를 쓰는 update 작업도 **없다**(`grep orderMemo` = 스키마 1곳뿐)
- 추정: 87건이 통째로 같고 3건은 상담사 이름 머리까지 들어 있으니, 상담사가 상담 메모 아래에 쓴 오더지를 오더 메모로 옮긴 것으로 보인다. 다른 50건은 어느 쪽이 나중에 고쳐졌는지 시각으로 가릴 수 없다
- 예: 일정 `bc43cc75…`(10-06)은 오더 메모 = 상담 메모 사본이고, 같은 고객의 다음 방문 `bb1feab2…`(10-11)은 다르다(§6)

---

## 5. 결제와 상담사

출처: `getPurchaseSummaries`(구매 168 · 거래 173) · `getPurchaseItemStatistics`(품목 547) · `getTransactionStatistics`(거래 173). 일정 `purchaseIds` 247개를 요청했는데 **168개만 돌아왔다**(`manifest.json requests` · 나머지 79개는 응답 없음, 이유는 데이터에 없음).

### 구매 담당 vs 그 방문의 상담사

| 비교 | 건수 |
|---|---|
| 구매 `assignees[0]` = 일정 상담사 | **160 / 168** |
| 일정에 상담 없음(구매 담당: 남준서 3 · 설지호 2 · 세라미크 명동 1) | 6 |
| 다름 | 2 — 남준서(상담사 류하린) · 세라미크 명동(상담사 윤나연) |
| 거래 `assignee` = 일정 상담사 | 157 / 173 |
| 거래 담당 ≠ 구매 담당 | 4 — 남준서 1(구매 담당 류하린, EASY_PAY) · 세라미크 명동 3(구매 담당 문하람, CARD 취소 · CASH 취소 · TRANSFER 승인) |
| 품목 통계 `counselorNames` = 일정 상담사 | 531 / 531(빈 16 = 상담 없는 방문) |
| 품목 통계 `assignees` = 구매 담당 | 547 / 547 |

- 상담사가 아닌 담당은 **남준서**(코디, COUNSELOR 태그 있음)과 **세라미크 명동**(COUNSELOR · NURSE · SKINCARE · COORDINATOR 태그, 공용 계정으로 보임 — 추정)뿐이다

### 상담 시술 vs 결제 품목

- `consultationProcedures` 가 145건 모두 비어 있어 **겹침 = 0, 비교 불가(데이터에 없음).**
- 글로는 이어진다(예시 1건, 전수 측정 안 함): `bb1feab2…` 상담 메모 번호 목록 「포텐자모공팁 · 리쥬란힐러2cc · 턱보톡스100u」 ↔ 구매 품목 「턱 보톡스 50U(국산) · [첫방문] 턱보톡스 50u(국산) · [첫방문] 리쥬란힐러 2cc · [첫방문] 포텐자(모공) 1회」. 글 ↔ 품목 이름을 기계로 맞추는 규칙은 없다

---

## 6. 회차

출처: `getScheduleDetail` 177건을 `visitor.id` 로 묶음

- 고객 173명 중 일정 2개 이상 **4명뿐**이고, 둘 다 상담 기록이 있는 고객은 **1명**이다. 열흘 캡처라 회차 데이터는 아주 적다
- 그 1명(`getScheduleDetail/0000146.json` → `0000144.json`):

| 방문 | 상담사 | 상담 `visitor.isNew` | 상담 기록 | 구매 · 작업 |
|---|---|---|---|---|
| 10-06 `bc43cc75…` | 문하람 | True | 새로 생성(18:30) · 같은 날 19:41 마지막 수정. 456자, 「금일 상담만 진행」 · 3회 추천안, `Dr: 심주원` | 없음 · 작업 0 |
| 10-11 `bb1feab2…` | 문하람 | **False** | **새 기록**(15:22 생성 · 17:19 수정). 310자, 첫 기록의 이력 줄 「h) 몇년전 물광주사,+피코토닝」을 다시 적음 | 구매 1(담당 문하람, 4품목) · 시술 작업 4 |

- 사실: 방문마다 **새 상담 기록**이 생긴다(`consultations[]` 는 그 일정 것만, `scheduleId` = 일정 145/145). 앞 방문 기록은 고쳐지지 않았다(10-06 기록의 수정 시각이 10-06)
- 사실: 같은 상담사가 이어 받았다. 「다음 방문도 이 상담사」 지정은 예약 메모 글에만 있다(「++다음 내원시 상담 '문하람' 실장님으로 지정」 3건 · 「지정/다음에도 상담사(민현우)」 1건). `reservation.counselor`(희망 상담사)는 177건 모두 비어 있다
- 나머지 3명: 취소 + 완료 조합(상담 기록은 완료 방문에만 1개) 2명, 완료(상담 없음) + 취소 1명
- 상담 기록을 고객 단위로 모아 보는 API: 스펙에 `getSchedulesByVisitor`(앞 조사 `research-patient-detail-report.md:280`)가 있으나 이번 캡처에 없다

---

## 정할 것 — 관제 · 차티 경계 판단 재료 (결정하지 않음)

1. **상담사 칸의 원천** — KOS 에서 상담사를 가리키는 원천은 `consultations[].counselors[]`(방문 단위)와 구매 `assignees[]` 둘이다. 관제가 「이 방 상담사」를 보여 줄 때 어느 값을 기준으로 할지(관제가 배정한 값 / 차티 상담 기록 / KOS 상담 기록)
2. **상담사 목록 범위** — `COUNSELOR` 태그(29명, 코디 · 공용 계정 포함)와 실제 상담한 사람(6명, 태그 없는 윤나연 포함)이 다르다. 관제의 상담사 배정 후보를 무엇으로 고를지
3. **상담 시작 · 종료 시각** — KOS `consultationStartedDateTimeUtc` 는 실제 시작이 아니다(예약 시작 복사 92 · 기록 생성 순간 53). 상담 시간에 가까운 값은 통계의 체류 시간뿐이다. 관제의 [시작] · [종료]가 이 빈자리를 채우는지
4. **상담 메모의 두 부분** — 위쪽(상담내용)과 아래쪽(오더지)이 한 글에 섞여 있고, 오더지는 오더 메모와 37%(50/137) 어긋난다. 차티가 둘을 나눠 받을지, 오더지를 구조(시술 · 샷 · 부위)로 받을지
5. **상담 시술을 구조로** — KOS 에 `consultationProcedures`(상품 옵션 / 시술권) 칸이 있지만 현장은 0건 사용. 차티가 이 칸에 해당하는 것을 채울지, 결제 품목과 어떻게 이을지
6. **결제 · 작업 등록은 상담사 몫인가** — 구매 · 거래 담당 95% 가 상담사이고, 결제 → 시술권 → 작업 ready 가 1분 안에 이어진다. 관제의 「데스크가 결제된 시술 중 오늘 할 것 선택 → 배정」(`workflow.md` 큰 흐름)과 실제 KOS 순서(결제 직후 작업이 자동 · 즉시 ready)가 다르다 — 현장 확인 필요
7. **결제 뒤 상담 메모 수정** — 138건 중 126건이 구매 뒤에 마지막으로 고쳐졌다(중앙값 +32분, 하루 넘게 뒤 9건). 차티 기록을 언제 「닫힌」 것으로 볼지
8. **KOS 로 되돌려 쓰기** — 스냅샷 기준 `updateScheduleConsultationInfo` 는 `consultationMemo` 만 쓴다. 상담사 · 오더 메모를 쓰는 update 작업은 스냅샷에 없음 — 현재 공개 스펙(75개)에서 다시 볼지
9. **다음 방문 상담사 지정** — 지금은 예약 메모 글. 차티 · 관제가 구조로 둘지(KOS `reservation.counselor` 「희망 상담사」 칸은 비어 있음)

---

## 출처 목록

캡처(`CAP/` = `reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/`)

- `CAP/manifest.json` — `jobs` · `requests`(getPurchaseSummaries 요청 247 id) · `scopeNotes`(잔여 시술권 = 조회 당시) · `relatedIdCounts`
- `CAP/raw/getScheduleDetail/*.json` 177개 — `data.consultations[]` · `data.consultation` · `data.orderMemo` · `data.reservation.*` · `data.tasks[]` · `data.etceteraWorks[]` · `data.purchaseIds` · `data.receptionDateTimeUtc` · `data.flowStepUpdatedDateTimeUtc`
  - 예시: `0000069.json`(10-09 민현우) · `0000077.json`(10-09 오현우) · `0000088.json`(윤나연 상담) · `0000144.json` · `0000146.json`(회차)
- `CAP/raw/getScheduleStatistics/0000011.json` — `counselorNames` · `consultationDwellTimeMinute` · `consultationWaitingDwellTimeMinute`
- `CAP/raw/getPurchaseSummaries/0000195~0000197.json` — 구매 168 · `assignees[]` · `assignee` · `transactions[].assignee` · `paymentDateTime.approvedDateTimeUtc`
- `CAP/raw/getPurchaseItemStatistics/0000013~0000014.json` — 547 · `assignees` · `counselorNames`
- `CAP/raw/getTransactionStatistics/0000012.json` — 173 · `assigneeName` · `purchaseAssigneeNames`
- `CAP/raw/getProcedureTaskStatistics/0000015~0000016.json` — 702 · `counselorNames` · `assigneeNames`
- `CAP/raw/getTicketBundlesQuery/*.json` 173개(데이터 있는 것 11) — `ticketSets[].tickets[].createdDateTimeUtc`
- `CAP/raw/getPrepaidCardChargingEventStatistics/*` — `assignees`(남준서 1)
- 나머지 API 폴더 — 순회했고 상담사 0건

스펙 `SPEC` = `/Users/kknaks/git/ax-clinic-project/para/archive/inbox_archive/2026-09-18-kos-openapi.yaml`

- `:2230` `updateScheduleConsultationInfo` · `:14430` `OpenUpdateScheduleConsultationInfoCommand`(scheduleId · consultationMemo)
- `:12638` `OpenProcedureTaskStatisticsItem.counselorNames`(:12686) · `:13007` `OpenPurchaseItemStatisticsItem`(assignees :13019 · counselorNames :13031) · `:13416` `OpenScheduleStatisticsItem`(dwell :13433-13440 · counselorNames :13441) · `:13887` `OpenTransactionStatisticsItem`(assigneeName :13901 · purchaseAssigneeNames :13952)
- `:17963` `PurchaseAssignee` · `:18621` `PurchaseSummary`(assignee deprecated · assignees) · `:18752~` `PurchaseSummaryTransaction`(assignee = 거래 담당자)
- `:21684` `ConsultationContract`(counselors · consultationDoctors · consultationProcedures · consultationStartedDateTimeUtc · content · result) · `:21758` `ConsultationOptionConfiguration` · `:21906` `ConsultationProcedure`(OPTION / TICKET) · `ConsultationTicketConfiguration`(:21983 근처) · `ConsultationResult` · `ConsultationVisitor.isNew`
- `:22770` 만족도 `EvaluationTarget.counselor` · `:23706` `orderMemo` · `:23783` `ScheduleDetailConsultationContract` · `:23869` 예약 `counselor`(희망 상담사)

앞 조사 · 기타

- `orchestration/work/sts-prototype/research-patient-detail-report.md` — 메모 다섯 종 · 87/137(:26 · :188)
- `orchestration/work/sts-prototype/kos-staff-api-report.md` — `getAccounts` · roleTags
- `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/kos-staff.json` — 직원 88명(읽기만)
- `reference/2026-10-12-cc-prototype/workflow.md` §4
