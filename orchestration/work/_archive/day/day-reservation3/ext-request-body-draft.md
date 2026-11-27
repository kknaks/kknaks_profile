# 초안 — 링키가 보내는 예약 요청 본문 (ext)

> 11-26 코디 초안 · 논의용(스펙 아님). 기준 = DAY 필드(웹 예약 등록 `reservation_book.book()` 입력 + 이번에 새로 생기는 칸). 이름 표기 = 기존 ext 처럼 camelCase. KOS 에 어떻게 들어가는지는 뒤에서 정한다.

## 1. 새 스레드 — v1 신규 요청

`POST /api/ext/reservation-requests` · 헤더 `Idempotency-Key`

```json
{
  "customer": {
    "customerId": null,
    "name": "LIN HSIANGYU",
    "phoneticName": null,
    "gender": "FEMALE",
    "nationality": "TW",
    "birthDate": "1981-03-14",
    "email": null,
    "phone": { "dial": "886", "number": "912345678" },
    "sns": { "type": "LINE", "id": "lin.hy" }
  },
  "start": "2026-10-29T13:00:00+09:00",
  "groupId": "<예약 그룹 id>",
  "doctorStaffId": "<직원 목록 staffId>",
  "counselorStaffId": null,
  "desiredProcedures": "써마지 FLX 또는 울쎄라 + 온다 리프팅",
  "interpreterLanguage": "zh",
  "funnelId": "<유입 채널 id>",
  "memo": "원장님 1:1 상담 필요"
}
```

## 2. 같은 스레드에 새 버전 — 수정 · 취소 요청

`POST /api/ext/reservation-requests/{requestId}/versions`

```json
{ "kind": "change", "...": "1 과 같은 칸 전부(완성본)" }
```

```json
{ "kind": "cancel", "reason": "고객 일정 변경" }
```

## 2-1. 버전 번호

- **번호는 서버가 매긴다**(스레드 안 1, 2, 3 …). 링키는 번호를 보내지 않는다 — 응답으로 받는다.
- 응답(202): `{ "requestId": "<스레드 id>", "version": 2, "kind": "change", "status": "requested" }`
- 버전 종류 `kind` = `new` · `change` · `cancel`. v1 은 늘 `new`(첫 POST) · 그 뒤는 `/versions` 에 `change` · `cancel`.
- `baseVersion` 충돌 검사 **없음**(사용자 11-26 확정)

## 3. 칸별

| 칸 | 필수 | DAY 근거 | 비고 |
|---|---|---|---|
| `customer.customerId` | 재진이면 | `book(customer_id)` | DAY 고객 id(UUID) — `/customers/lookup` 응답 값. 있으면 나머지 고객 칸은 「바뀐 값」 비교용 |
| `customer.name` | ○ | 새 고객 `name` | 여권 성명 · 이름 + 생년월일 = KOS 고객 등록 필수(사용자 11-26) |
| `customer.phoneticName` | | `phonetic_name` | |
| `customer.gender` | | `MALE` · `FEMALE` | 없으면 null |
| `customer.nationality` | | ISO 2자 | |
| `customer.birthDate` | ○ | `birth_date` | 웹은 `YYYY.MM.DD` · ext 는 ISO `YYYY-MM-DD` 제안 |
| `customer.email` | | **새 칸** | 새 고객이면 KOS 고객 이메일로 |
| `customer.phone` | | `dial` + `phone` | |
| `customer.sns` | | `sns_type` · `sns_id` | |
| `start` | ○ | `start` | ISO · 끝 = 그룹 간격(웹과 같음) · 지난 시각 400 |
| `groupId` | ○ | `group_id` | 링키가 보냄(결정) |
| `doctorStaffId` | | `doctor_id` | ext 직원 목록 `staffId` |
| `counselorStaffId` | | **새 칸** | 같은 목록 |
| `desiredProcedures` | | **새 칸** · 텍스트 | |
| `interpreterLanguage` | | **새 칸** | 언어 코드 · null = 통역 필요 없음 |
| `funnelId` | ○ | `funnel_id` | KOS 유입 채널 목록(`get-codes FUNNEL`)에서 보내는 쪽이 고름 · ext 목록 새로 |
| `memo` | | `memo` | 병원이 고칠 수 있음 |
| ~~담당자~~ | — | — | 「예약 생성」 누른 로그인 직원(결정) |

## 4. 결정됨 (11-26)

- 예약 그룹 · 유입 채널 목록 = ext 조회 새로
- `funnelId` 필수 · 상세 유입 채널 뺌
- 이메일 = 새 고객 선택 칸
- 통역 = `interpreterLanguage`(null = 필요 없음) · 언어 코드 목록은 스펙에서
- 수정 = 완성본 전체 · 취소 `reason` 선택
- 이름 · 생년월일 필수 · 버전 번호 서버
