# 처방전 — KOS 에서 출력 · 딥링크 (실제 지점 HAR · 모양만)

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 원천
  - `reference/2026-10-23-cc-overall-board/har/처방전.har`(30항목 · 10:15:39Z ~ 10:17:22Z, gitignore)
  - KOS 처방전 화면 정적 JS(`core-cf.kos-solution.com/prescription/…prescription-client_v0.0.49.js`, 공개 정적 파일 32개)
  - 앞 판의 예약 · 고객 화면 JS
  - 공개 스펙 openapi.yaml 1.0.1
- **⚠ 이 HAR 은 데모가 아니다.** 모든 KOS 요청의 테넌트가 데모 값과 달랐다(스크립트로 비교, 값은 보지 않음)
  - 그 테넌트로는 **아무 호출도 하지 않았다**
  - HAR 에서는 경로 · 본문 키 · 응답 키 구조 · 페이지 주소 꼴만 읽었다(메모리에서 키만 뽑았고 응답을 파일로 덤프하지 않았다)
  - 환자 · 의사 · 의약품 · 기관 값은 이 리포트에 없다
  - 상태 enum 값(`PRINT` · `OUT` 등)만 적었다
- 데모 확인: 데모 테넌트로 **조회만**(쓰기 0 · `print-prescription` 호출 안 함). 운영 키 0
- 표기
  - **확인**: HAR 키 · 데모로 본 것
  - **JS**: 웹앱 코드
  - **추정**: 해석

---

## 0. 결론

- **KOS 처방전 화면 주소**: `https://app.kos-solution.com/{tenantId}/prescription` — **쿼리가 없다**
  - 어느 처방전을 볼지는 주소에 실리지 않는다. 화면 안에서 고른다
  - JS 에 등록된 경로는 `/prescription`(처방전 조회)과 `/prescription/manage`(묶음처방 목록) 둘이다
- **일정 안의 처방전 탭도 있다**(JS): 예약 화면의 일정 상세 Drawer 에 `SchedulePrescriptionTab` 이 들어간다. 이 탭이 일정의 `prescriptionIds` 로 `get-prescriptions-by-ids` 를 부르고, 처방전을 누르면 처방전 창(모달)이 열린다
  - 앞 판들의 딥링크 `tab=` 값(`reservation · consultation · procedure · purchase`)에 처방 탭이 있는지는 HAR 에서 보지 못했다 → Q-129
- **[처방전 출력]** = `print-prescription{id, employeeId}`(내부 쓰기) → 응답 `{}`
  - 처방전의 `status` 가 `PRINT` 가 되고 `printedDateTimeUtc` 가 그때 시각으로 바뀐다(두 번 눌렀을 때 두 번 다 바뀌었다, 키 비교로 확인)
  - **실제 인쇄는 브라우저 인쇄 창**(`window.print()`, JS)이다. PDF 를 서버에서 받는 호출은 없다
  - 즉 `print-prescription` 은 「출력했다」는 **기록**이다
- **공개 API 에는 처방전 조회 · 출력이 없다.** 스펙에 나오는 것은 일정의 `prescriptionIds` 필드뿐이다(grep 2곳)
- **데모에는 처방전이 없다**: 데모 일정 1,144건(08-01 ~ 11-30 · 단계 8개 전부) 모두 `prescriptionIds` 가 비어 있다. 내부 `get-prescriptions` 도 0건이다
- ccc [처방전 출력] 후보
  - (a) 일정 상세 딥링크(`…/reservation/schedule/?visitorId&scheduleId&tab=…`)로 열고 처방전 탭을 사람이 누른다
  - (b) `/prescription` 화면을 열고 사람이 고른다
  - 필요한 값(고객 id · 일정 id · `prescriptionIds`)은 ccc 사본(일정 응답)에 모두 있다
  - 처방전 id 하나로 바로 여는 주소는 확인하지 못했다 → Q-129 · Q-130
- 정할 것은 **6개**다(Q-129 ~ Q-134)

---

## 1. HAR 인벤토리

항목 30 = KOS POST 19 + KOS OPTIONS 2 + Datadog 9.

모든 KOS 요청의 `kos-client-uri` 는 `https://app.kos-solution.com/{tenantId}/prescription`(쿼리 · 해시 없음)이다. `Referer` · `Origin` 은 `https://app.kos-solution.com/`.

| # | 경로 | 본문 키 | 응답 키(값 없음) | 용도(추정) |
|---|---|---|---|---|
| 0 · 13 | `v1/visitor/queries/get-visitor` | `id` | `data{고객 상세 키들}` | 처방 대상 고객 |
| 1 · 14 | `drug_manage/v1/hospital/get` | (본문 없음) | **400** `{code:"HOSPITAL_NOT_FOUND", message, originMessage}` | 약품 관리(병원 설정) — 이 지점에 설정이 없어서 400 |
| 3 · 6 · 7 · 11 · 12 · 16 · 18 · 23 · 25 · 29 | `role/v2/queries/get-roles` | — | `data[{id, name, featureList[], roleTags[int], isDefault}]` | 역할(10회) |
| 8 | `account/v2/queries/get-accounts` | `roleTag(정수) · ids[]` | `data[{id, userId, email, name, roleId, activate, createdAt, **licenseNumber**, roleName, realName, defaultWorkingZoneId, updatedDateTimeUtc, mfaMethods, role}]` | 처방의 목록(면허번호 키가 있다) |
| **19** | **`prescription/v1/commands/print-prescription`** | `id · employeeId` | `{}` | **[처방전 출력] ① — 기록** |
| 21 | `prescription/v1/queries/get-prescription` | `prescriptionId` | §2 | 출력 뒤 다시 읽기 |
| **26** | **`prescription/v1/commands/print-prescription`** | `id · employeeId` | `{}` | **[처방전 출력] ②** |
| 27 | `prescription/v1/queries/get-prescription` | `prescriptionId` | §2 | 다시 읽기 |

합계 19. 쓰기는 2건(같은 처방전에 출력 두 번 — `print-prescription.id` = `get-prescription.prescriptionId`, 비교로 확인).

---

## 2. `get-prescription` 응답 구조 (키만)

```text
data{
  id, status, sideType,                         ← 이번 값: status "PRINT" · sideType "OUT"(원외처방으로 보인다, 추정)
  insuranceType{id, name, etcId, etcText},
  hospital{name, nursingInstitutionNumber, phoneNumber, faxNumber, email},
  visitor{id, name, chartNumber, phoneNumber, registrationType, registrationNumber},
  doctor{id, name, kindOfLicense, licenseNumber},
  dateAndNoIssue{grantNumber, dateTimeUtc},     ← 교부번호 · 교부일
  kcdCode[], periodOfUse{value, date}, isIncludePsychotropicDrugs,
  drug[{id, hiraCode{id, code, name, enteralPath, standard, unit, deleted}, onceDosage, timesPerDay, days, usage}],
  requested{memo, employeeId, dateTimeUtc}, canceled{memo, employeeId, dateTimeUtc},
  createdDateTimeUtc, createdEmployeeId, updatedDateTimeUtc, printedDateTimeUtc
}
```

- **일정 id(`scheduleId`) 키가 없다.** 처방전 → 일정 방향의 연결은 응답에 없다. 일정 → 처방전은 일정의 `prescriptionIds[]` 로 간다
- 상태 값: JS 에서 `REQUEST`(요청) · `PRINT`(출력) 가 보인다. 목록은 「요청 → 출력」 순으로 정렬한다(`SchedulePrescriptionTab`). 취소 상태도 있다(`cancel-prescription` · `canceled{…}`)
- `print-prescription` 두 번 뒤 `printedDateTimeUtc` 가 매번 바뀌었다. 출력 횟수를 세는 칸은 없다

---

## 3. KOS 처방전 쪽 작업 (JS · 이름만)

| 종류 | 경로(`/tenants/{tenantId}/prescription/v1/…`) |
|---|---|
| 조회 | `queries/get-prescription` · `get-prescriptions` · `get-prescriptions-by-ids` · `get-prescription-bundles` |
| 쓰기 | `commands/create-prescription` · `update-prescription` · `update-memo-prescription` · `cancel-prescription` · **`print-prescription`** · `create/update/delete/reorder-prescription-bundle`(묶음처방) |

화면 구성(JS)
- 경로 `/prescription` = 처방전 조회 · `/prescription/manage` = 묶음처방 목록
- 일정 Drawer 안 처방전 탭 `SchedulePrescriptionTab`
  - 일정의 `prescriptionIds` → `get-prescriptions-by-ids`
  - 처방 생성 · 갱신 · 취소 이벤트를 듣고(`usePrescriptionCreationListener` 등) 다시 읽는다
  - 처방전을 누르면 처방전 창(`open: true, dataSource`)이 열린다
- 예약 화면 번역에 「処方せん作成」(일정 행동 메뉴) · 「処方履歴」(고객 이력 탭)이 있다. 일정 · 고객 화면에서 처방을 만들고 이력을 보는 자리가 있다
- 인쇄: 처방전 창에서 `window.print()`(브라우저 인쇄)

---

## 4. 데모에서 다시 (조회만)

| 조회 | 결과 |
|---|---|
| 공개 `getSchedulesByFlowStep` × 8단계(08-01 ~ 11-30) | 일정 1,144건 · **`prescriptionIds` 가 있는 일정 0건** |
| 내부 `prescription/v1/queries/get-prescriptions`(`{}`) | 200 · `data[]` 0건 |
| `get-prescription` | **부르지 않았다** — 데모에 처방전 id 가 없다 |
| 공개 스펙 | 처방전 작업 **0개**. `prescriptionIds` 필드만 있다 |

→ **「데모에 처방전 없음」.** 데모에서 처방전 화면 · 조회를 다시 확인하려면 데모에 처방전을 하나 만들어야 한다(쓰기 · 이번 범위 밖) → Q-131

---

## 5. ccc [처방전 출력] 후보 (KOS 순서 · 결정 아님)

| 후보 | 주소 | ccc 사본에 있는 값 | 사람이 KOS 에서 할 일 |
|---|---|---|---|
| (a) 일정 상세 처방전 탭 | `https://app.kos-solution.com/{tenantId}/reservation/schedule/?visitorId={visitorId}&scheduleId={scheduleId}&tab=…` | 고객 id · 일정 id ✔ | 처방전 탭을 열고 처방전을 눌러 [처방전 출력]. `tab=` 에 처방 값이 있는지 미확인 |
| (b) 처방전 조회 화면 | `https://app.kos-solution.com/{tenantId}/prescription` | — | 화면 안에서 환자 · 처방전을 찾아 [처방전 출력] |
| (c) 처방전 id 로 바로 | 확인 못 함 | 일정 `prescriptionIds[]` ✔ | — |

- 정산 상자 「처방전 · {요약} 1건 / 오늘 처방전 없음」(시안)
  - 「있음 / 없음 · 건수」는 일정 `prescriptionIds` 개수로 알 수 있다(공개 일정 응답)
  - **내용 요약(약 이름 등)은 내부 `get-prescription(s-by-ids)` 로만** 읽힌다. 의료 정보다 → Q-132
- 「출력됨 / 다시 출력」 표시: 처방전 `status PRINT` · `printedDateTimeUtc`(내부 조회)로 알 수 있다. 공개로는 알 수 없다 → Q-133

---

## 6. 호출 기록 (데모 · 조회만)

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| 공개 | `getSchedulesByFlowStep` | 8 | 200 |
| 내부 | `prescription/v1/queries/get-prescriptions` | 1 | 200 |
| 인증 | 공개 `exchange-token` 1 · 내부 sign-in 1 | 2 | 200 |

- **실제 지점 테넌트 호출 0건** · 쓰기 0건 · 운영 키 0건
- 정적 JS(처방전 화면 `remoteEntry` + 묶음 32개)는 공개 CDN 에서 받았다

---

## 7. 정할 것 (결정하지 않음) — 6개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-129 | [처방전 출력] 딥링크의 모양 | 처방전 화면 주소에는 처방전 id 가 실리지 않는다. 일정 상세(처방 탭) · `/prescription` 조회 화면 중 어디로 보낼지. 일정 상세에 처방 탭 값(`tab=`)이 있는지 KOS 화면에서 한 번 확인할지 | PD Q-103 |
| Q-130 | 처방전 id 하나로 바로 여는 길 | 찾지 못했다. KOS 에 요청할지 · 사람이 한 번 더 누르는 것으로 둘지 | — |
| Q-131 | 데모 처방전 | 데모에 처방전이 하나도 없다. 데모에서 처방전을 만들어(쓰기) 화면 · 딥링크를 확인할지 | — |
| Q-132 | 정산 상자 「처방전」 내용 | 건수는 공개 `prescriptionIds` 로 된다. 약 이름 같은 요약은 내부 조회 · 의료 정보다. ccc 가 읽어 보일지 · 「처방전 N건」만 보일지 | R Q-19 · PD Q-109 |
| Q-133 | 「출력됨」 표시 | 처방전 `status PRINT` · `printedDateTimeUtc` 는 내부 조회로만 보인다. ccc 가 출력 여부를 보일지 | — |
| Q-134 | 처방전 화면을 여는 PC 의 인쇄 | KOS 는 브라우저 인쇄 창을 쓴다. 귀가 데스크 PC 에 프린터 · KOS 로그인이 있다고 가정할지 | PD Q-102 · Q-104 |
