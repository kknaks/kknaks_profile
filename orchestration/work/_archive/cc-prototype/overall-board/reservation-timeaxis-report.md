# 스케줄 표 시간축 = 예약 그룹 설정

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 원천
  - `reference/2026-10-23-cc-overall-board/har/예약그룹.har`(214항목 · 10:03:24.8Z ~ 10:03:26.7Z · KOS 웹 `…/{tenantId}/reservation/settings` 화면, gitignore)
  - KOS 예약 화면 JS(`reservation-client_v0.0.540`, 앞 판에서 받은 정적 파일)
  - 앞 판 `reservation-read-report.md`(`R§`) · `reservation-create-report.md`(`C§`)
- **KOS 쓰기 0건.** 데모 조회만 했다(테넌트 · 키 `assert`, 쓰기 허가 목록 비움). 운영 키 0
- 시각은 모두 KST 로 바꿔 적었다(KOS 는 UTC 로 준다)
- 표기
  - **확인**: HAR · 데모로 본 것
  - **JS**: 웹앱 코드
  - **추정**: 해석

---

## 0. 결론

- **데모 13개 그룹의 운영 시간은 모두 같다**: 매일(월~일) 10:00 ~ 20:00, 쉬는 시간 없음. 병원 기본 운영 시간(`get-default-operation-timetable`)과도 같다. 휴무(병원 · 그룹)는 12/31 까지 0건이다
- **다른 것은 간격(`intervalMinutes`)뿐이다** — 「시간축이 시술 때문에 다르다」의 정체

  | 간격 | 그룹 |
  |---|---|
  | 30분 | 국내 · 중화권 · 영미권 · 일본 · 기타(권역 5) · 레이저 · 필러 · 후관리 · 수액/체형 |
  | **60분** | 리프팅 · 스킨부스터 |
  | **15분** | 보톡스 · 제모 |

  - 정원은 모두 「4층」 3명이다(「미사용」 구역 칸은 제모만 켜짐)
  - 슬롯 조회로도 그렇게 나온다(확인): 하루 슬롯 수 30분 그룹 20 · 60분 10 · 15분 40
- **KOS 예약 현황 화면은 칸(그룹)마다 자기 간격으로 줄을 긋는다**(JS)
  - 시간당 높이(`oneHourHeight`)는 모든 칸이 같다. 그래서 60분 칸의 한 줄은 30분 칸 두 줄 높이, 15분 칸은 반 줄 높이다
  - 세로축 시작은 **전역 08:00**(`globalOffsetMinutes: 480`)이다. 각 칸의 첫 줄은 08:00 에서 그 칸의 간격으로 맞춘 자리다
  - 운영 시간 밖 · 쉬는 시간 · 휴무는 칸마다 운영 시간표로 따로 칠한다
- 칸 머리 문구는 `{정원}명 / {간격}분` 이다(JS 번역 `reservation.schedule.dashboard.columns.description`)
- 정할 것은 **6개**다(Q-123 ~ Q-128)

---

## 1. HAR 인벤토리

항목 214 구성

| 출처 | 항목 수 |
|---|---|
| KOS 정적 js(`core-cf`) | 164 — 설정 화면을 처음 열어 묶음을 받았다 |
| Datadog | 21 |
| **KOS POST** | **12** |
| KOS OPTIONS | 4 |
| `api.channel.io` | 9(PATCH 6 · POST 2 · OPTIONS 1) |
| 웹소켓 `front-ws.channel.io` | 1(상담 채팅 위젯) |
| KOS 웹소켓 `schedule-socket` | 1(메시지 3) |
| KOS mp3 | 1 |
| Amplitude | 1 |

KOS POST 12건 — 모두 조회. `issue-schedule-socket-token` 은 이름만 command 이고 KOS 데이터를 바꾸지 않는다

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 150 | `notification/computer-telephone/v1/queries/find-computer-telephone-settings` | — | 비어 있음(CTI 전화 설정) |
| 155 · 193 | `schedule/zone/v1/queries/get-zones` | — | (2) 「4층」(기본) · 「미사용」 |
| 157 | `role/v2/queries/get-roles` | — | (15) |
| 158 · 179 · 180 · 181 · 182 | `meta/codes/v1/queries/get-codes` | `category:ACCOUNT_STATUS` | (0) |
| 160 | `account/v2/queries/get-accounts-status` | — | (0) |
| 191 | `schedule/socket/v1/commands/issue-schedule-socket-token` | `{}` | `{token}`(앞 판 PC§3) |
| **196** | **`schedule/group/v1/queries/get-reservation-groups`** | `deleted:false · zoneIds[2]` | **(13) — §2** |

합계 12.

---

## 2. 예약 그룹의 시간 필드 (HAR #196, 데모 13개)

그룹 키: `id · title · memo · startDate · intervalMinutes · intervalCapacities[{zoneId, enabled, intervalCapacity}] · isDefault · sameDayCloseBufferMinutes · operationTimetable{monday…sunday{enabled, startTime, endTime, breaktime{startTime, endTime}}} · order`

- 시각 형식: `startTime` · `endTime` 은 **날짜가 붙은 UTC 문자열**이다(예: `2026-08-10T01:00:00Z` = 10:00 KST)
  - 날짜 부분은 그룹을 만든 때의 값이라 뜻이 없다. 시 · 분만 쓴다(JS 도 `getHours · getMinutes` 만 쓴다)
  - 쉬는 시간이 없으면 빈 문자열이다

| order | 그룹 | 간격 | 정원(4층 / 미사용) | 운영(월~일) | 쉬는 시간 | 당일 마감 전 | 시작일 | 기본 |
|---|---|---|---|---|---|---|---|---|
| 1 | 국내 | 30 | 3 / 1(꺼짐) | 10:00–20:00 | 없음 | 30분 | 07-31 | ✔ |
| 2 | 중화권 | 30 | 3 / 3(꺼짐) | 10:00–20:00 | 없음 | 30분 | 08-10 | |
| 3 | 영미권 | 30 | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 4 | 일본 | 30 | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 5 | 기타 | 30 | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 6 | 리프팅 | **60** | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 7 | 레이저 | 30 | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 8 | 필러 | 30 | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 9 | 스킨부스터 | **60** | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 10 | 보톡스 | **15** | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 11 | 제모 | **15** | 3 / **3(켜짐)** | 〃 | 〃 | 30분 | 08-10 | |
| 12 | 후관리 | 30 | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |
| 13 | 수액/체형 | 30 | 3 / 3(꺼짐) | 〃 | 〃 | 30분 | 08-10 | |

- 그룹 응답에는 **휴무 필드가 없다.** 그룹 휴무는 `get-reservation-group-days-offs`(내부, R§2)로 따로 받는다
- **설정 화면이 고를 수 있는 간격**: `15 · 30 · 60 · 90 · 120 · 150` 분, 기본값 30(JS 그룹 설정 폼 `M$`)
- `sameDayCloseBufferMinutes`(당일 마감 전 버퍼)는 모두 30분이다. 당일 예약은 끝나기 30분 전까지로 보인다(추정, 이름 기준)
- `startDate` = 그룹이 쓰이기 시작한 날짜(설정 폼 「오픈일」)

---

## 3. 병원 기본 운영 시간과의 관계 (데모 조회)

| 조회(내부) | 결과 |
|---|---|
| `get-default-operation-timetable` | 월~일 모두 10:00–20:00 · 쉬는 시간 없음 — **그룹과 같다** |
| `get-default-reservation-policy` | `data{}`(비어 있음) |
| `get-default-days-off`(오늘 ~ 12/31) | 0 |
| `get-reservation-group-days-offs`(13개 · 오늘 ~ 12/31) | 0 |
| `get-reservation-rule-summaries` | 2 — 활성 · 기본 1개(C§4: 그룹 「국내」 하나만 가리킨다) |

- **그룹이 비면 기본값을 쓰는지**: 데모는 그룹마다 시간표가 다 차 있어서 확인할 수 없다. 그룹 응답에 「기본값 따름」 같은 표시도 없다
- JS 에서 그룹의 그날 요일 시간표가 없을 때(`startTime` 없음) 첫 줄 계산이 기댈 곳은 **전역 08:00**이다. 병원 기본 운영 시간이 아니다(아래 §4) → Q-124
- 공개 `getReservationSlotsByGroupsV2`(2026-10-27) 하루 슬롯: 13개 그룹 모두 10:00 시작 · 20:00 끝. 30분 그룹 20개 · 60분 그룹 10개 · 15분 그룹 40개(확인)
- 공개 `getReservationTimeSlots`(기본 규칙): `timeSlotIntervalMinutes 30` · 10:00 부터(규칙이 가리키는 그룹 「국내」의 간격과 같다)

---

## 4. KOS 예약 현황 화면이 칸마다 다른 간격을 그리는 방법 (JS)

| 무엇 | 코드(요약) | 뜻 |
|---|---|---|
| 칸 정의 | 예약 그룹마다 `{id, name, intervalMinutes, availableZoneIds(정원이 켜진 구역)}` 를 만든다 | 칸 = 그룹 × 구역 |
| 칸 머리 | `"{intervalCapacities}명 / {intervalMinutes}분"`(일어판 `名／分`) | 시안의 「N명 / 30분」과 같은 정보 |
| **첫 줄 시각** | `jr({date, reservationGroup, globalOffsetMinutes: 480})` = `s(그 요일 그룹 운영 시작(분) ?? 480, 480, intervalMinutes)`. `s(e,t,r)` = `e ≤ t` 이면 `e`, 아니면 `e − floor((e−t)/r)·r` | 그룹 운영 시작(10:00 = 600분)을 **08:00(480분) 이후로 간격만큼 되감은 자리** → 30분 · 60분 · 15분 그룹 모두 **08:00 부터** 줄이 시작한다 |
| 줄 수 | `intervalCount = floor((1440 − 첫 줄 분) / intervalMinutes)` | 그 칸의 간격으로 **자정까지** 줄을 긋는다 |
| 높이 | `WU(분, oneHourHeight) = 분 / 60 × oneHourHeight` · 드래그도 `oneHourHeight` 로 계산 | **시간당 높이 하나를 모든 칸이 같이 쓴다** → 60분 줄은 2배, 15분 줄은 0.5배 높이 |
| 운영 밖 표시 | 칸마다 `operationTime{operationTimetable, daysOff, displayedDate}` 로 운영 시작 전 · 끝 뒤 · 쉬는 시간(`breaktime`) · 휴무를 칠한다(`globalStartMinutes` 부터) | 시안의 「지난 시각 회색」과 다른 개념이다(운영 밖 회색) |
| 경고 | 예약이 쉬는 시간에 걸치면 `reservationGroup.breakTime`, 예약 길이가 그룹 간격보다 길면 `reservationGroup.intervalExceeded` | 55분 예약(MC§2.1) 같은 것을 경고한다 |
| 겹침 배치 | 칸 안에서 같은 줄에 겹치는 예약을 왼쪽부터 쌓고(`left`), 줄마다 개수를 센다(`countsInIteration`) → 정원과 비교 | 시안의 「겹치는 최대 카드 수로 칸 폭」(D§3.1)과 같은 생각 |
| 병원 기본 시작(다른 함수) | `W2({date, defaultOperationTimetable, globalOffsetMinutes})` = `s(병원 기본 운영 시작 ?? 480, 480, 15)` | 병원 기본 시간을 15분 단위로 맞춘 전역 시작이다. 어느 화면에서 쓰는지는 이번에 따라가지 않았다 |

→ 「시간축이 다르다」고 보이는 이유: **같은 세로 높이 안에서 60분 칸은 줄이 반, 15분 칸은 줄이 두 배**로 그어진다. 운영 시간 자체는 모든 그룹이 같다.

---

## 5. 스케줄 표 규칙 후보 — KOS 값으로 할 수 있는 것 (결정 아님)

| 후보 | 필요한 KOS 값 | 가능? | 메모 |
|---|---|---|---|
| 전체 세로축 = 그날 모든 그룹 운영 시간의 합집합 | 그룹 `operationTimetable[요일]` · 그룹 휴무 · 병원 휴무 | 된다 | 데모는 모두 10:00–20:00 → 합집합도 10:00–20:00. 시안은 08:00–20:00, KOS 화면은 08:00 부터 그린다 → Q-123 |
| 줄 = 30분(사용자 결정 「기본 30분」) | — | 된다 | 15분 그룹(보톡스 · 제모)의 :15 · :45 시작 예약은 30분 줄 사이에 놓인다 → Q-125 |
| 칸마다 운영 밖 = 회색 | 그룹 시간표 · 쉬는 시간 · 그룹/병원 휴무 | 된다 | 지금 데모에는 다른 운영 시간 · 쉬는 시간 · 휴무가 없어 화면에서 차이가 나지 않는다 |
| 60분 그룹 칸 | `intervalMinutes 60` · 슬롯 `capacity` | 된다 | (a) 30분 줄 두 칸을 한 칸으로 합쳐 그리기, (b) 30분 줄 그대로 두고 예약 카드만 60분 높이로 그리기. KOS 는 (a) 꼴(그 칸의 간격으로 줄을 긋는다)이다 → Q-126 |
| 칸 머리 「N명 / 30분」 | `intervalCapacities[4층].intervalCapacity` · `intervalMinutes` | 된다 | KOS 와 같은 문구 |
| 칸마다 남은 자리 | 공개 `getReservationSlotsByGroupsV2.slots[]{capacity, reservationCount}` | 된다 | 그룹 간격 단위로 온다(15 · 30 · 60) |
| 「지금 시각」 줄 · 지난 시각 회색(시안) | 현재 시각만 있으면 된다 | 된다 | KOS 값과 상관없다 |

---

## 6. 호출 기록 (조회만)

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| 내부 | `get-default-operation-timetable` · `get-default-reservation-policy` · `get-default-days-off` · `get-reservation-group-days-offs` · `get-reservation-rule-summaries` | 5 | 200 |
| 공개 | `getReservationSlotsByGroupsV2` 2 · `getReservationTimeSlots` 1 | 3 | 200 |
| 인증 | 공개 `exchange-token` 1 · 내부 sign-in 1 | 2 | 200 |

**쓰기 0건** · 운영 키 0건.

---

## 7. 정할 것 (결정하지 않음) — 6개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-123 | 세로축의 시작 · 끝 | 그룹 운영 합집합은 10:00–20:00, 시안은 08:00–20:00, KOS 화면은 08:00 ~ 자정까지 그린다(운영 밖은 칠함). 어느 범위로 그릴지 | R Q-5 |
| Q-124 | 그룹 시간표가 빈 요일 | 데모에는 없다. KOS 화면은 그 경우 전역 08:00 을 쓰고 병원 기본 시간을 쓰지 않는다(JS). ccc 는 병원 기본 시간으로 채울지 · 운영 안 함으로 볼지 | — |
| Q-125 | 15분 그룹(보톡스 · 제모) | 기본 30분 줄에서 :15 · :45 예약을 어떻게 놓을지(줄 안에 위치로 · 반 줄로 · 칸만 15분으로) | — |
| Q-126 | 60분 그룹(리프팅 · 스킨부스터) | 칸의 줄을 60분으로 합칠지(KOS 꼴), 30분 줄을 유지하고 카드 높이만 60분으로 할지. 드래그로 놓을 수 있는 자리(정시만?)와도 이어진다 | MC Q-84 |
| Q-127 | 예약 길이가 그룹 간격과 다를 때 | KOS 는 간격보다 긴 예약을 경고(`intervalExceeded`)만 하고 받는다(55분 예약 사례). ccc 가 카드를 실제 길이로 그릴지 · 간격으로 맞출지 | MC Q-84 |
| Q-128 | 당일 마감 버퍼(`sameDayCloseBufferMinutes` 30) | 오늘 예약을 끝나기 30분 전에 막는지 KOS 문서로 확인하지 못했다. 칸 [+] 을 그 시간 뒤에 막을지 | C Q-55 |
