# 처방전 상세 — 일정 상세에서 여는 주소 (실제 지점 HAR · 모양만)

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_e6c7f845e581)
- 앞 판: `reservation-prescription-report.md`(Q-129 ~ Q-134). 이 판은 그중 Q-129 · Q-130 의 「일정 상세 처방 탭」 부분을 HAR 로 닫는다
- 원천: `reference/2026-10-23-cc-overall-board/har/처방전상세.har`(92항목 · 10:23:34Z ~ 10:23:52Z, gitignore)
- **⚠ 실제 지점 HAR.** 앞 판 §0 규칙 그대로
  - 그 테넌트로 **호출 0건**(조회 포함) · 데모 호출도 이번엔 0건 · 쓰기 0 · 운영 키 0
  - 스크립트로 메모리 안에서 경로 · 본문 키 · 응답 키 · 주소 꼴만 뽑았다. 응답을 파일로 덤프하지 않았다
  - id 비교는 「같다 / 다르다」만 봤다. 환자 · 처방 · 의사 · 기관 · id 값은 이 리포트에 없다
  - 적은 값은 enum 뿐이다: `tab` · `historyMenu` 값, `status PRINT` · `sideType OUT`
- 표기: **확인** = HAR 에서 본 것 · **추정** = 해석

---

## 0. 결론

- **처방 탭 값은 `tab=etceteraWork` 다**(확인). 일정 상세 딥링크에 그대로 붙는다
  ```text
  https://app.kos-solution.com/{tenantId}/reservation/schedule/?visitorId={visitorId}&scheduleId={scheduleId}&tab=etceteraWork&historyMenu=reservationHistory
  ```
  - 탭 이름이 「처방」이 아니라 **「기타 업무」(`etceteraWork`)** 다. 처방전 목록은 이 탭이 열릴 때 불린다(#80)
  - `historyMenu=reservationHistory` 는 탭과 함께 붙는 둘째 쿼리다(오른쪽 이력 메뉴로 보인다, 추정). 이번 HAR 에서는 값이 이것 하나뿐이었다
- **처방전 id 쿼리는 없다**(확인). `prescriptionId` 같은 쿼리도, 해시도 없다
  - 처방전 창(모달)을 연 뒤 호출(#83 ~ #90)의 주소도 `tab=etceteraWork` 그대로다. 창을 열어도 주소가 바뀌지 않는다
  - 처방전 창은 `get-prescription`(단건)을 부르지 않았다. 탭에서 받은 `get-prescriptions-by-ids` 응답으로 그린다(추정 — 단건 호출이 0건)
- **ccc [처방전 출력] 한 줄 결론**: 일정 상세 딥링크 하나(`tab=etceteraWork`)로 **처방전 목록이 있는 탭까지는 바로 열린다.** 처방전 창은 사람이 한 번 눌러 연다. 필요한 값(`visitorId` · `scheduleId`)은 ccc 사본에 다 있다. `prescriptionIds` 는 주소에 쓰이지 않는다(「처방전 있음」 판단에만 쓴다)
- 정할 것 **3개**(Q-135 ~ Q-137)

---

## 1. 페이지 주소 꼴 (확인)

- HAR `pages` 제목 1건: `/{tenantId}/reservation/settings`(녹화 시작 때 연 화면)
- `Referer` 92건 전부 `https://app.kos-solution.com/` · `Origin` 60건 전부 `https://app.kos-solution.com`(경로 없음 — 주소 꼴은 `kos-client-uri` 헤더에서만 읽힌다)
- KOS 요청의 `kos-client-uri`(43건)

| 건수 | 주소 꼴 | 때 |
|---|---|---|
| 3 | `/{tenantId}/reservation` | 예약 현황 |
| 16 | `/{tenantId}/reservation/schedule/?visitorId={visitorId}&scheduleId={scheduleId}` | 일정 상세가 열린 직후(탭 쿼리 붙기 전) |
| 11 | `…&tab=reservation&historyMenu=reservationHistory` | 예약 탭 |
| 2 | `…&tab=purchase&historyMenu=reservationHistory` | 수납 탭 |
| 1 | `…&tab=procedure&historyMenu=reservationHistory` | 시술 탭 |
| **10** | **`…&tab=etceteraWork&historyMenu=reservationHistory`** | **처방전 탭 · 처방전 창** |

- 탭 값 4개가 나왔다: `reservation` · `purchase` · `procedure` · `etceteraWork`. 앞 판들의 `consultation` 은 이번 HAR 에 없다(누르지 않음)
- Datadog 화면 기록(`view.url`)도 같은 꼴이다. `/{tenantId}/prescription` 은 `view.referrer` 로만 12번 나온다. 앞 판 녹화(처방전 화면)에서 넘어온 것이다. 이번 장면은 처방전 화면을 거치지 않았다

---

## 2. KOS 호출 (43건 · 전부 POST · 쓰기 0)

인벤토리: `api.kos-solution.com` POST 43 · 정적 `core-cf` GET 25 · `image` GET 7 · Datadog 16 · Amplitude 1 = 92.

| # | 경로(`/tenants/{t}/…`) | 본문 키 | 상태 | 탭 |
|---|---|---|---|---|
| 0 | `role/v2/queries/get-roles` | — | 200 | 현황 |
| 1 · 2 | `visitor/v2/queries/get-visitor` | `id` | 200 | 현황 |
| 5 | `visitor/v2/queries/get-visitor` | `id` | 200 | 상세 열림 |
| 6 | `schedule/v1/queries/get-payment-required-tasks` | `visitorId` | 200 | 〃 |
| 7 | `schedule/v1/queries/get-schedule-detail` | `scheduleId` | 200 | 〃 |
| 9 | `consultation/v1/queries/get-consultations-by-visitor-id` | `visitorId` | 200 | 〃 |
| 10 | `ticket/v1/queries/get-ticket-bundles` | `visitorId · sort{by, order}` | 200 | 〃 |
| 11 | `schedule/v1/queries/get-schedule-summaries` | `visitorId · sort{by, order}` | 200 | 〃 |
| 18 | `account/v2/queries/get-accounts-last-update-date-time-utc` | — | 200 | 〃 |
| 19 | `account/v2/queries/get-accounts` | `{}` | 200 | 〃 |
| 20 | `schedule/group/v1/queries/get-reservation-group` | `id` | 200 | 〃 |
| 21 · 22 · 25 | `meta/codes/v1/queries/get-codes` | `category` | 200 | 〃 |
| 23 | `procedure-menu/visitors/queries/get-visitors` | `sort{by, order}` | 200 | 〃 |
| 24 | `procedure-menu/currency-settings/queries/get-currency-settings` | — | 200 | 〃 |
| 40 | `purchase/tax-refund-settings/v1/queries/get-tax-refund-settings` | `{}` | **400** | 〃 |
| 41 | `meta/template/v1/queries/get-hospital-text-snippets` | `{}` | 200 | 〃 |
| 42 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | `visitorId` | 200 | reservation |
| 43 · 44 | `meta/codes/v1/queries/get-codes` | `category` | 200 | reservation |
| 45 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | `visitorId · available` | 200 | reservation |
| 46 | `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | `visitorId` | 200 | reservation |
| 47 · 62 | `procedure-menu/currency-settings/queries/get-currency-settings` | — | 200 | reservation |
| 48 | `procedure-menu/vat-settings/queries/get-vat-settings` | — | 200 | reservation |
| 60 · 64 | `v1/visitor/queries/get-visitor` | `id` | 200 | reservation |
| 61 | `purchase/payment-settings/v1/queries/get-payment-settings` | — | 200 | reservation |
| 63 | `purchase/v1/queries/get-purchase-summaries` | `purchaseIds[] · includeDeleted` | 200 | reservation |
| 68 | `image/visitor-image/v1/queries/get-visitor-images` | `visitorId · scheduleId · deleted` | 200 | purchase |
| 69 | `image/v1/commands/generate-signed-urls-with-param` | `fileNames[] · query{w, h}` | 200 | purchase(이미지 서명 URL — 이름은 command 지만 읽기용) |
| 77 | `purchase/v1/queries/get-purchase-summaries` | 〃 | 200 | procedure |
| **80** | **`prescription/v1/queries/get-prescriptions-by-ids`** | **`prescriptionId[]`** | 200 | **etceteraWork — 탭 열림** |
| 81 · 87 · 89 · 90 | `purchase/v1/queries/get-purchase-summaries` | 〃 | 200 | etceteraWork |
| 83 | `account/v2/queries/get-accounts` | `roleTag · ids[]` | 200 | etceteraWork — **처방전 창 열림**(처방의 계정) |
| 84 | `/common/kcd-codes/v1/queries/get-kcd-codes`(테넌트 밖 공통) | — | 200 | 〃(상병 코드) |
| 85 | `v1/visitor/queries/get-visitor` | `id` | 200 | 〃 |
| 86 | `drug_manage/v1/hospital/get` | — | **400** | 〃(앞 판과 같은 400) |

합계 43 = 표의 행 번호 수 43(0 · 1 · 2 · 5 · 6 · 7 · 9 · 10 · 11 · 18 ~ 25 · 40 ~ 48 · 60 ~ 64 · 68 · 69 · 77 · 80 · 81 · 83 ~ 87 · 89 · 90).

- 처방전 창이 열린 때 = #83 ~ #86 묶음(23:46). 앞 판 처방전 화면에서 창을 열 때와 같은 묶음(계정 · 고객 · 약품 관리 400)이다(추정 — 앞 판 #8 · #13 · #14 와 같은 경로)
- `get-prescription`(단건) · `print-prescription` 은 **0건**. 이번 장면은 「열어 보기」만 했다

---

## 3. `get-prescriptions-by-ids` 키 (값 없음)

요청

```text
{ prescriptionId[] }          ← 키 이름은 단수, 값은 배열
```

- 본문의 id 집합 = #7 `get-schedule-detail` 응답 `data.prescriptionIds[]` 집합(같음 · 1건). 즉 **일정의 `prescriptionIds` 를 그대로 넣는다**
- 응답 `data[].id` 집합 = 요청 집합(같음)

응답

```text
data[{
  id, status, sideType,                          ← 이번 값: status PRINT · sideType OUT
  insuranceType{id, name, etcId, etcText},
  hospital{name, nursingInstitutionNumber, phoneNumber, faxNumber, email},
  visitor{id, name, chartNumber, phoneNumber, registrationType, registrationNumber},
  doctor{id, name, kindOfLicense, licenseNumber},
  dateAndNoIssue{grantNumber, dateTimeUtc},
  kcdCode[], periodOfUse{value, date}, isIncludePsychotropicDrugs,
  drug[{id, hiraCode{id, code, name, enteralPath, standard, unit, deleted}, onceDosage, timesPerDay, days, usage}],
  requested{memo, employeeId, dateTimeUtc}, canceled{memo, employeeId, dateTimeUtc},
  createdDateTimeUtc, createdEmployeeId, updatedDateTimeUtc, printedDateTimeUtc
}]
```

- 앞 판 `get-prescription.data` 와 **키가 같다**(배열로 감쌌을 뿐). 처방전 창에 필요한 내용이 목록 응답에 다 들어 있다 → 단건 호출이 없는 이유로 보인다(추정)
- 여기에도 `scheduleId` 키는 없다(앞 판과 같음)
- `get-schedule-summaries`(#11, 고객 이력) 응답에는 `prescription` 이 들어간 키가 없다. 처방전 연결은 일정 상세(#7)의 `prescriptionIds` 하나뿐이다

---

## 4. ccc [처방전 출력] 에 대입

| 필요한 것 | ccc 사본에 있나 | 근거 |
|---|---|---|
| `tenantId` | ✔(설정) | 앞 판 딥링크 |
| `visitorId` | ✔ 일정 응답 | 앞 판 |
| `scheduleId` | ✔ 일정 응답 | 앞 판 |
| `tab=etceteraWork` | 고정 값 | §1 |
| `historyMenu=reservationHistory` | 고정 값 | §1(붙일지는 Q-136) |
| 처방전 id | 주소에 **안 쓰인다** | §1 · §0 |
| `prescriptionIds[]` | ✔ 일정 응답 | 「처방전 있음 / 없음 · 건수」 판단용 |

- 사람이 KOS 에서 하는 일: 딥링크로 열림 → 기타 업무 탭에 처방전 목록 → **처방전 하나를 눌러 창 열기** → [처방전 출력](→ `print-prescription` 기록 + 브라우저 인쇄 창, 앞 판)
- 처방전이 여러 건인 일정에서는 어느 것을 열지 사람이 고른다. 이번 HAR 은 1건이라 여러 건일 때의 목록 순서는 HAR 로 보지 못했다(앞 판 JS: 「요청 → 출력」 순)
- 앞 판 후보와의 관계: (a) 「일정 상세 처방전 탭」이 `tab=etceteraWork` 로 **확정된 모양**이 됐다. (c) 「처방전 id 로 바로」는 이번에도 길이 없다

---

## 5. 정할 것 (결정하지 않음) — 3개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-135 | [처방전 출력] 딥링크를 `tab=etceteraWork` 로 둘지 | 처방전 목록까지 바로 열린다. 처방전 창은 한 번 더 눌러야 한다. 이 「한 번 더」를 받아들이면 Q-129 의 모양이 닫힌다. 탭 이름이 「기타 업무」라 화면 안내 문구(「기타 업무 탭에서 처방전을 누르세요」 같은 것)가 필요할지 | Q-129 · Q-130 |
| Q-136 | `historyMenu=reservationHistory` 를 딥링크에 붙일지 | 이번 HAR 에서는 탭을 누르면 KOS 가 스스로 붙였다. 빼고 열어도 같은 화면인지는 실물로 확인하지 않았다(실제 지점이라 열어 보지 않음 · 데모에는 처방전이 없음) | — |
| Q-137 | 「처방전 없음」 일정의 [처방전 출력] | 일정 `prescriptionIds` 가 비면 기타 업무 탭은 빈 목록이다. ccc 가 버튼을 숨길지 · 막을지 · 그래도 열지 | Q-132 |

- 앞 판 Q-131(데모 처방전)은 그대로 열려 있다. Q-136 을 데모에서 확인하려면 데모에 처방전이 하나 있어야 한다

---

## 6. 호출 기록

- 실제 지점 테넌트 호출 **0건** · 데모 호출 **0건** · 쓰기 0 · 운영 키 0
- HAR 은 메모리에서만 읽었다. 스크래치에 응답 · 키 덤프 없음

## 7. 빠진 행 점검

- §2 표 행 번호 43 = HAR KOS POST 43 ✔
- 지시 1(주소 꼴) → §1 · 지시 2(요청 · 응답 키) → §3 · 지시 3(결론) → §0 · §4 · 지시 4(Q-135 ~) → §5 ✔
