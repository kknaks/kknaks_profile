# DAY ext 「예약 요청」 API — 링키 개발자용 안내서

> 스웨거(`<DAY ext 주소>/api/ext/docs`)와 **같이 읽는** 안내서입니다. 칸 하나하나의 모양은 스웨거가 정본이고, 이 문서는 흐름 · 규칙 · 예시를 모아 둡니다. 둘이 다르면 스웨거(= 코드)가 맞습니다. 스웨거 화면은 별도 로그인(Basic)이 필요하니, 계정은 병원 키와 같은 경로로 받아 주세요.
>
> 이 문서의 주소 · 키 · id 는 모두 자리표시(`<…>`)나 가짜 값입니다.

## 1. 무엇이 생겼나

**예약 요청**은 링키가 요청을 보내면 DAY 에 **스레드**(요청 하나의 대화 묶음)가 생기는 기능입니다. 병원 코디가 DAY 예약 현황판에서 그 스레드를 보고 확인한 뒤 [예약 생성]을 누르면, 그때 KOS 예약이 만들어집니다.

- 스레드 안에는 **버전**(링키가 보낸 요청 완성본 · 번호 1, 2, 3 …)과 **댓글**(링키 · 병원의 글, 병원의 변경 요청, KOS 반영 확인 줄)이 쌓입니다.
- 기존 `POST /reservations` 와 다른 점은 이것 하나입니다. `POST /reservations` 는 **바로 예약**을 넣고(워커가 KOS 에 반영), 예약 요청은 **병원이 확인한 뒤에** 예약이 됩니다. 예약 요청 경로(E1 · E2 · E3 · E6)는 DAY 에만 저장하고 KOS 를 부르지 않습니다. 202 는 "받아 저장함"이지 "예약됨"이 아닙니다.

## 2. 키 · 헤더

| 헤더 | 필수 | 내용 |
|---|---|---|
| `X-Api-Key` | ✓ | **병원당 키 하나**(링키 · 차티 공용). 키가 연결된 병원에만 접근합니다. 값 = `<병원 키>` |
| `X-Day-Client` | 선택 | 보낸 곳 표시. 형식 = 영문 소문자 · 숫자 · `-` 1 ~ 16자(아니면 400 `invalid_request`). E5 버전의 `client` 로 돌아옵니다 |
| `Idempotency-Key` | E1 · E2 · E6 필수 | 재시도 키 1 ~ 128자. 아래 「재시도」 |
| `Content-Type` | 쓰기 | `application/json` |

**키가 바뀌었습니다.** 이제 키는 연동처별이 아니라 병원 단위 하나입니다. 예전에 링키용으로 받은 키는 더 이상 쓰지 않으니, 병원 키를 새로 받아 바꿔 주세요(새 키 값은 문서가 아닌 별도 경로로 전달합니다).

**재시도(`Idempotency-Key`)**

- 같은 키에 같은 본문으로 다시 보내면 새로 만들지 않고, 처음 만든 버전이나 댓글을 돌려줍니다.
- 같은 키에 다른 본문을 보내면 409 `idempotency_conflict` 입니다.
- 키가 묶이는 범위는 병원 단위이고, 표마다 따로입니다. 새 요청(E1)과 새 버전(E2)이 한 범위를 쓰고, 댓글(E6)은 따로 셉니다.
- 재시도 응답은 **처음 응답 그대로**입니다(`requestId` · `version` · `kind` · `status`). 처음 E2 `cancel` 응답이 `canceled` 였다면 재시도 응답도 `canceled` 입니다. 그 뒤 바뀐 지금 상태는 E5 로 확인합니다.

**호출 한도**

- 병원 단위로 분당 60회입니다. 넘으면 429 `too_many_requests` 입니다.
- 같은 IP 에서 인증이 안 된 실패(400 · 401 · 404 · 405)가 분당 10회를 넘어도 429 입니다.
- 검사 순서는 401(키) → 429(한도) → 400(`X-Day-Client` 형식)입니다.

## 3. 경로 8개

모든 경로의 앞에는 `<DAY ext 주소>` 가 붙습니다.

| # | 메서드 | 경로 | 하는 일 | 성공 |
|---|---|---|---|---|
| E1 | POST | `/reservation-requests` | 새 요청. 스레드와 v1 `new` 를 만들고 `status=requested` | 202 `ExtRequestAccepted` |
| E2 | POST | `/reservation-requests/{requestId}/versions` | 새 버전. `change`(완성본 전체) 또는 `cancel`(사유 선택) | 202 `ExtRequestAccepted` |
| E3 | POST | `/reservation-requests/{requestId}/withdraw` | 철회. 예약이 없는 스레드를 닫음(본문 · `Idempotency-Key` 없음) | 200 `ExtRequestWithdrawn` |
| E4 | GET | `/reservation-requests?updated_since=&cursor=` | 스레드 목록. 바뀐 것을 폴링 | 200 `ExtRequestList` |
| E5 | GET | `/reservation-requests/{requestId}` | 스레드 상세. 버전 · 댓글 · 상태 | 200 `ExtRequestDetail` |
| E6 | POST | `/reservation-requests/{requestId}/comments` | 링키 댓글(`message` 만) | 201 `ExtCommentCreated` |
| E7 | GET | `/reservation-groups` | 본문 `groupId` 에 넣을 값(예약 현황 열 순서) | 200 `ExtGroupList` |
| E8 | GET | `/funnels` | 본문 `funnelId` 에 넣을 값(닫힌 채널은 빠짐) | 200 `ExtFunnelList` |

요청을 보내기 전에 같이 쓰는 기존 경로도 있습니다.

- `GET /clinics/{clinicId}/staff` 의 `staffId` 를 `doctorStaffId` · `counselorStaffId` 에 넣습니다. `doctorStaffId` 에는 원장 직무인 직원만 넣을 수 있습니다.
- `POST /customers/lookup` 은 `customerId` 를 얻는 길입니다(§9).

응답 모양

- E1 · E2 응답은 `{requestId, version, kind, status}` 입니다.
- E3 응답은 `{requestId, status: "closed"}` 입니다.
- E4 응답은 `{items: [{requestId, status, latestVersion, customerId, reservationId, updatedAt}], nextCursor}` 입니다.
- E6 응답은 `{commentId, createdAt}` 입니다.
- E7 · E8 응답은 `{items: [{groupId|funnelId, name}]}` 입니다.

## 4. 요청 본문

### E1 새 요청 · E2 `change`

E2 `change` 는 아래 칸에 `"kind": "change"` 를 더한 **완성본 전체**입니다. 바뀐 칸만 보내는 방식이 아닙니다.

| 칸 | 필수 | 형식 · 길이 · 값 |
|---|---|---|
| `customer` | ✓ | 아래 고객 표 |
| `start` | ✓ | ISO-8601 일시. 오프셋이 없으면 KST 로 봅니다. 지난 시각이면 400 `request_past_start` |
| `groupId` | ✓ | E7 목록의 값 |
| `funnelId` | ✓ | E8 목록의 값 |
| `doctorStaffId` | | 지정 원장. 직원 목록의 `staffId` 중 원장 직무만 |
| `counselorStaffId` | | 지정 상담사. 직원 목록의 `staffId` |
| `desiredProcedures` | | 희망 시술 글, 500자까지 |
| `interpreterLanguage` | | 통역 언어. `en` · `ja` · `zh` · `zh-Hant` · `th` · `vi` · `yue` 중 하나. null 이면 통역이 필요 없다는 뜻 |
| `memo` | | 예약 메모, 1000자까지. 병원이 고칠 수 있습니다 |

`customer`

| 칸 | 필수 | 형식 · 길이 · 값 |
|---|---|---|
| `customerId` | | DAY 고객 UUID(`/customers/lookup` 응답 값). 넣으면 재진으로 봅니다(§9) |
| `name` | ✓ | 여권 성명, 100자까지, 빈 값 불가 |
| `birthDate` | ※ | `YYYY-MM-DD` |
| `phone` | ※ | `{dial, number}`. `dial` = 국가번호 숫자 1 ~ 4자. `number` = 숫자만, 앞에 0 없이 4 ~ 15자 |
| `sns` | ※ | `{type, id}`. `type` = `etc` · `kakaotalk` · `line` · `instagram` · `whatsapp` · `wechat` 중 하나. `id` = 1 ~ 100자 |
| `email` | ※ | 254자까지. 새 고객이면 KOS 고객 이메일로 들어갑니다 |
| `phoneticName` | | 한글 발음, 100자까지 |
| `gender` | | `MALE` · `FEMALE` |
| `nationality` | | ISO 3166 대문자 2자 |

※ `birthDate` · `phone` · `sns` · `email` 가운데 **하나 이상은 필수**입니다. 모두 없으면 400 `invalid_request` 입니다.

**공통 규칙**

- 모르는 키를 보내면 400 `invalid_request` 입니다. 버전 번호 칸이나 담당자 칸을 넣어도 막힙니다.
- 길이는 글자 수로 셉니다.
- 오류 `message` 앞에는 칸 이름이 붙습니다.
- `desiredProcedures` · `interpreterLanguage` · `memo` 는 KOS 예약 메모 하나로 합쳐집니다. 합친 형식은 `필드: 내용` 한 줄씩이고, 순서는 희망 시술 → 통역 → 예약 메모, 빈 칸은 뺍니다. 합친 글이 **1000자를 넘으면** 400 `memo_too_long` 입니다. `memo` 하나만 1000자여도 앞에 필드 이름이 붙어 넘을 수 있으니 주의해 주세요.
- 검사 순서는 지난 시각 → `groupId` → `funnelId` → `doctorStaffId` → `counselorStaffId` → 합친 메모 길이 → `customerId` 입니다.

예시(가짜 값)

```json
{
  "customer": {
    "name": "HONG GILDONG",
    "birthDate": "1990-01-01",
    "nationality": "TW",
    "phone": { "dial": "886", "number": "900000000" },
    "sns": { "type": "line", "id": "example.id" }
  },
  "start": "2026-12-01T13:00:00+09:00",
  "groupId": "00000000-0000-0000-0000-0000000000a1",
  "funnelId": "00000000-0000-0000-0000-0000000000b1",
  "doctorStaffId": null,
  "counselorStaffId": null,
  "desiredProcedures": "<희망 시술 글>",
  "interpreterLanguage": "zh-Hant",
  "memo": null
}
```

### E2 `cancel`

```json
{ "kind": "cancel", "reason": "<사유 · 선택 · 500자까지>" }
```

`reason` 은 스레드에만 남고 KOS 에는 싣지 않습니다.

### E6 댓글

```json
{ "type": "message", "body": "<글 1 ~ 1000자>", "authorName": "<글쓴이 · 선택 · 50자까지>" }
```

## 5. 값 사전

**스레드 `status`**

| 값 | 뜻 |
|---|---|
| `requested` | 요청됨. 병원이 답할 버전이 있습니다. 새 요청이나 새 버전(E2)이 받아질 때마다 이 상태가 됩니다 |
| `confirmed` | 확정. 병원 [예약 생성] · [예약 수정]이 KOS 에 반영된 것이 확인됐습니다. 그 사이 새 버전이 오면 `requested` 입니다 |
| `canceled` | 취소됨. 병원 [예약 취소]의 반영이 확인됐거나, 예약이 이미 취소된 스레드에 `cancel` 이 받아졌습니다(E2 · 병원 동기화) |
| `closed` | 닫힘. 예약 없이 끝났습니다. 까닭은 `closedReason` |

**`closedReason`**(`status=closed` 일 때만 값이 있고, 그 밖은 null, 다시 열리면 null)

| 값 | 뜻 |
|---|---|
| `withdrawn` | 링키가 철회(E3) |
| `expired` | 자동 닫힘. 요청됨이고, 예약이 없고, 확인 대기가 아니고, 마지막 버전 `start` 가 지났을 때. 병원 동기화 때마다 검사하며 `cancel` 버전에는 해당하지 않습니다 |
| `folded` | 병원이 KOS 쓰기 실패를 [접음]. 요청됨이고 마지막 버전이 `cancel` 이고 예약이 없을 때만 닫힙니다. 그 밖에 접으면 요청됨 그대로입니다 |

**버전 `kind`**(기록된 종류)

| 값 | 뜻 |
|---|---|
| `new` | 첫 버전이거나, 예약이 없는 스레드에 온 `change`(생성 전이라 새 요청으로 봄) |
| `change` | 예약이 있는(확인 대기 포함) 스레드에 온 수정 완성본. 병원이 [예약 수정]을 누릅니다 |
| `cancel` | 취소 요청. 병원이 [예약 취소]를 누르고, 예약이 이미 취소됐으면 바로 취소됨이 됩니다 |

**댓글 `type`**

| 값 | 뜻 |
|---|---|
| `message` | 글. 링키(E6)나 병원 직원이 씁니다. 병원이 남기는 「고객 확인 필요」도 이것입니다(§8 ③) |
| `change_request` | 병원의 변경 요청. 제안 일시는 `proposals`, 진행은 `state` |
| `reservation_applied` | 병원 버튼이 KOS 에 반영된 것을 확인한 줄. `action` · `appliedAt` |

**변경 요청 `state`**(`change_request` 만, 그 밖은 null)

| 값 | 뜻 |
|---|---|
| `waiting` | 답변 대기. 링키의 새 버전을 기다립니다(스레드에 하나까지) |
| `superseded` | 대체됨. 그 뒤 새 버전(E2)이 받아졌거나, 스레드가 철회 · 자동 닫힘 · 접음 · 바깥 취소로 끝났습니다 |
| `withdrawn` | 병원이 변경 요청을 거뒀습니다 |

**반영 `action`**(`reservation_applied` 만, 그 밖은 null)

| 값 | 뜻 |
|---|---|
| `create` | [예약 생성] 반영. 이때 `reservationId` · `customerId` 가 채워집니다 |
| `update` | [예약 수정] 반영 |
| `cancel` | [예약 취소] 반영. 또는 예약 현황에서 먼저 취소된 예약에 `cancel` 이 와서 취소됨으로 끝냈을 때(이때 글쓴이 이름은 null) |

**`author.side`**

| 값 | `name` |
|---|---|
| `hospital` | 병원 직원 이름 |
| `partner` | 링키가 E6 에 보낸 `authorName` |
| `system` | DAY 가 남긴 반영 줄(`reservation_applied`). 버튼을 누른 직원 이름이고, 바깥 취소면 null |

**그 밖의 칸**

- `reservationId` 는 만든 DAY 예약 UUID 입니다. 생성이 반영된 뒤 채워지고, 그 예약이 취소돼도 남습니다.
- `customerId` 는 DAY 고객 UUID 입니다. 예약이 없을 때는 버전마다 재진 판정으로 갱신되고, 생성이 반영될 때 확정됩니다.
- `versionNumber`(댓글)는 쓸 때의 마지막 버전 번호입니다. 반영 줄이면 반영한 버전 번호입니다.

## 6. 상태 × 행동

**예약 있음**이란 만든 예약(`reservationId`)이 있고 지금 취소되지 않은 상태를 말합니다. 병원이 버튼을 눌러 KOS 반영을 기다리는 동안(**확인 대기** · 밖에서는 안 보임)도 예약 있음으로 봅니다.

| 지금 스레드 | E2 `change` | E2 `cancel` | E3 철회 | E6 댓글 |
|---|---|---|---|---|
| 요청됨 · 확정 — **예약 있음**(확인 대기 포함) | 202 `kind=change` · `requested` | 202 `kind=cancel` · `requested`(병원이 [예약 취소]) | 409 `request_already_applied` | 201 |
| 요청됨 — 예약 없음 · 만든 예약 없음 | 202 `kind=new` · `requested` | 409 `request_not_applied`(철회 E3 을 쓰라) | 200 `closed`(`withdrawn`) | 201 |
| 요청됨 · 확정 — 만든 예약이 그 뒤 취소됨 | 202 `kind=new` · `requested` | 202 `kind=cancel` · **`canceled`**(+ `reservation_applied` `cancel` · 글쓴이 이름 없음) | 200 `closed`(`withdrawn`) | 201 |
| 취소됨 | 202 `kind=new` · `requested`(다시 열림) | 409 `request_finished`(만든 예약 있었음) · `request_not_applied`(없었음) | 200 `closed`(`withdrawn`) | 409 `request_closed` |
| 닫힘 | 202 `kind=new` · `requested`(다시 열림) | 409 `request_finished`(만든 예약 있었음) · `request_not_applied`(없었음) | 200 `closed`(그대로 · `closedReason` 안 바뀜) | 409 `request_closed` |

- 예약 있음 스레드에 **다른 고객**으로 `change` 를 보내면 400 `customer_changed` 입니다. 다른 `customerId` 를 넣었거나, 판정 결과가 다른 고객 · 초진 · 2명 이상인 경우입니다. 이때는 새 요청(E1)으로 보내 주세요. 예약이 없으면 막지 않습니다.
- `change` 본문 검사(400 · 404 `customer_not_found`)가 위 판정보다 먼저입니다. 없는 스레드는 늘 404 `request_not_found` 이고, 이 검사가 본문 검사보다도 먼저입니다.
- 변경 요청이 `waiting` 인 동안에도 E2 · E3 · E6 은 막히지 않습니다.

상태 그림

```text
            E1
            │
            ▼
   ┌──── requested ◄───────────────────────────────┐
   │        │   ▲                                  │
   │        │   │ 새 버전(E2) 받음                 │ 새 버전(E2) 받음
   │        │   │                                  │ (다시 열림 · closedReason=null)
   │  병원 [예약 생성]·[예약 수정]                 │
   │  KOS 반영 확인                                │
   │        ▼   │                                  │
   │    confirmed ──────────────┐                  │
   │                            │ 병원 [예약 취소] │
   │  병원 [예약 취소]          │ KOS 반영 확인    │
   │  KOS 반영 확인             ▼                  │
   ├───────────────────────► canceled ─────────────┤
   │  (예약이 이미 취소된 스레드에 cancel 받음 ·   │
   │   병원 동기화 때 같은 조건도 여기로)          │
   │                                               │
   │  E3 철회 (withdrawn)                          │
   │  자동 닫힘 (expired)                          │
   │  병원 [접음] (folded)                         │
   └───────────────────────►  closed ──────────────┘
```

## 7. 오류 코드

모든 오류 응답의 모양은 `{"error": {"code": "<code>", "message": "<안내>"}}` 입니다. 분기는 `code` 로 해 주세요. `message` 는 사람이 읽는 안내라서 바뀔 수 있습니다.

**공통**(E1 ~ E8 모두)

| HTTP | `code` | 뜻 |
|---|---|---|
| 400 | `invalid_request` | 입력 형식 · 필수 · 길이 · 모르는 키 · 경로 UUID · `X-Day-Client` 형식 |
| 401 | `ext_unauthorized` | `X-Api-Key` 가 없거나 틀림, 또는 키에 연결된 병원이 쓰이지 않음 |
| 405 | `http_error` | 그 경로에 없는 메서드 |
| 429 | `too_many_requests` | 병원 단위 분당 60회 넘음, 또는 같은 IP 에서 인증 안 된 실패가 분당 10회 |
| 500 | `internal_error` | 처리 중 오류 |
| 503 | `ext_unavailable` | 연동 설정 오류(병원당 키가 둘 이상 등), 또는 호출 제한을 확인할 수 없음 |

**경로별**

| 경로 | HTTP | `code` | 뜻 |
|---|---|---|---|
| E1 · E2 `change` | 400 | `invalid_request` | `groupId` · `funnelId` 가 E7 · E8 목록에 없음, `doctorStaffId`(원장 직무) · `counselorStaffId` 가 직원 목록에 없음, 식별값이 하나도 없음 |
| E1 · E2 `change` | 400 | `request_past_start` | `start` 가 지난 시각 |
| E1 · E2 `change` | 400 | `memo_too_long` | 합친 KOS 메모가 1000자 넘음 |
| E1 · E2 `change` | 404 | `customer_not_found` | `customerId` 가 그 병원 고객이 아님 |
| E1 · E2 · E6 | 409 | `idempotency_conflict` | 같은 `Idempotency-Key` 로 다른 본문 |
| E2 | 400 | `customer_changed` | 예약 있음 스레드에 다른 고객 `change`. 새 요청(E1)으로 |
| E2 · E3 · E5 · E6 | 404 | `request_not_found` | 그 병원에 없는 `requestId` |
| E2 | 409 | `request_not_applied` | 예약을 만든 적 없는 스레드에 `cancel`. 철회(E3)를 쓴다 |
| E2 | 409 | `request_finished` | 취소됨 · 닫힘 스레드에 `cancel`(만든 예약이 있었음) |
| E3 | 409 | `request_already_applied` | 예약 있음(확인 대기 포함). 취소는 E2 `cancel` 로 |
| E4 | 400 | `invalid_request` | `cursor` · `updated_since` 형식 |
| E6 | 400 | `invalid_request` | `type` ≠ `message`, 또는 빈 `body` |
| E6 | 409 | `request_closed` | 취소됨 · 닫힘 스레드 |
| E7 · E8 | | 공통만 | |

E1 ~ E8 에서는 502 가 나오지 않습니다.

## 8. 흐름 예시

모든 요청에 `X-Api-Key: <병원 키>` 를 붙입니다. id 는 가짜 값입니다.

### ① 신규 → 병원 변경 요청 → 링키 `change` → 병원 생성

1. 링키가 새 요청을 보냅니다.
   ```http
   POST /reservation-requests
   Idempotency-Key: linky-req-0001
   { …§4 본문… }
   ```
   → 202 `{"requestId":"<R1>","version":1,"kind":"new","status":"requested"}`
2. 병원이 다른 일시를 제안합니다. 링키는 E4 폴링으로 바뀐 것을 알고, E5 로 읽습니다.
   ```http
   GET /reservation-requests/<R1>
   ```
   → `comments` 에 다음 줄이 보입니다.
   ```json
   { "type": "change_request", "author": {"side":"hospital","name":"<직원>"},
     "versionNumber": 1, "proposals": [{"start":"2026-12-01T15:00:00+09:00"}],
     "state": "waiting", "body": null, "action": null, "appliedAt": null, … }
   ```
3. 링키가 고객과 확인한 일시로 완성본을 다시 보냅니다.
   ```http
   POST /reservation-requests/<R1>/versions
   Idempotency-Key: linky-req-0002
   { "kind": "change", …§4 본문 전체(start 만 바꿈)… }
   ```
   → 202 `{"requestId":"<R1>","version":2,"kind":"new","status":"requested"}`
   - 아직 예약이 없어서 `kind` 가 `new` 로 기록됩니다.
   - 변경 요청 `state` 는 `superseded` 가 됩니다.
4. 병원이 [예약 생성]을 누르고 KOS 반영이 확인되면, E5 에 다음이 보입니다.
   - `status` = `confirmed`
   - `reservationId` · `customerId` 가 채워짐
   - 댓글 `{"type":"reservation_applied","author":{"side":"system","name":"<직원>"},"action":"create","versionNumber":2,"appliedAt":"…"}`

### ② 확정 뒤 취소

1. ①이 끝나 `confirmed` 인 스레드에 취소를 보냅니다.
   ```http
   POST /reservation-requests/<R1>/versions
   Idempotency-Key: linky-req-0003
   { "kind": "cancel", "reason": "<사유>" }
   ```
   → 202 `{"requestId":"<R1>","version":3,"kind":"cancel","status":"requested"}`
2. 병원이 [예약 취소]를 누르고 반영이 확인되면 `status` = `canceled` 이고, 댓글 `reservation_applied` `action=cancel` 이 붙습니다.
- 병원이 예약 현황에서 **먼저** 예약을 취소해 둔 뒤라면, 1의 응답이 바로 `"status":"canceled"` 입니다. 이때 반영 줄(`action=cancel`)이 붙고, 글쓴이 이름은 null 입니다.
- 이미 `canceled` · `closed` 인 스레드에 `cancel` 을 보내면 409 `request_finished` 입니다.

### ③ 같은 고객이 여럿 → 「고객 확인 필요」 → `customerId` 넣은 `change`

1. `customerId` 없이 E1 을 보냅니다. 판정에서 같은 고객이 2명 이상이 나와도 202 로 받습니다.
2. 병원이 [예약 생성]을 누르면 DAY 가 막고, `message` 댓글 「고객 확인 필요」를 남깁니다(E5 에서 보임). 초진으로 판정됐더라도 생성 때 KOS 에서 같은 고객을 찾으면 같은 댓글로 막습니다.
3. 링키가 `/customers/lookup` 으로 맞는 고객의 `customerId` 를 얻습니다(§9).
4. 그 `customerId` 를 넣은 완성본으로 E2 `change` 를 보냅니다.
   ```http
   POST /reservation-requests/<R2>/versions
   Idempotency-Key: linky-req-0004
   { "kind": "change", "customer": { "customerId": "<C1>", "name": "…", … }, … }
   ```
   → 202 `kind=new`(예약 없음) · `requested`. 이제 병원이 다시 생성을 누를 수 있습니다.

## 9. 초진 · 재진 판정과 `customerId`

판정은 버전을 받을 때 합니다.

- `customer.customerId` 가 **있으면** 재진입니다. 그 병원에 없는 고객이면 404 `customer_not_found` 입니다.
- **없으면** DAY 고객 가운데 다음 조건을 모두 맞는 고객을 셉니다.
  1. **이름이 같다** — 대소문자와 띄어쓰기는 무시합니다.
  2. **보낸 식별값 중 하나 이상이 정확히 같다** — 생년월일 · 연락처 · SNS · 이메일.
  3. **국적은 양쪽 다 있을 때만 같아야 한다.**
- 센 결과는 셋 중 하나입니다.
  - 1명이면 재진입니다.
  - 0명이면 초진입니다.
  - 2명 이상이면 병원이 생성을 누를 때 막히고 「고객 확인 필요」가 붙습니다(§8 ③).

**`customerId` 얻는 길 — `POST /customers/lookup`**

- 본문은 `{"name": "<이름>", "email": "<이메일>"}` 이거나 `{"customerId": "<UUID>"}` 입니다. 둘을 섞지 않습니다.
- 이름은 **KOS 에 등록된 띄어쓰기 그대로** 보내야 합니다. 앞뒤 공백만 지웁니다.
- 이메일은 앞뒤 공백을 지우고 소문자로 바꿔, 정확히 같은지만 봅니다.
- 응답 `customer.customerId` 를 요청 본문 `customer.customerId` 에 넣습니다.
- 못 찾으면 404 `customer_not_found` 입니다. 같은 이름 · 이메일 고객이 여럿이면 409 `customer_ambiguous` 입니다. 이 경로는 KOS 를 부르므로, KOS 를 읽지 못하면 502 `kos_unavailable` 이 날 수 있습니다.

## 10. 병원 처리 알기 — E4 폴링 → E5

병원이 처리한 것은 링키가 E4 를 폴링해서 알아냅니다.

1. `GET /reservation-requests?updated_since=<시각>` 을 부릅니다.
   - 결과는 `(updatedAt, requestId)` 오름차순이고, 한 번에 최대 100개입니다.
   - `nextCursor` 가 있으면 `cursor=<nextCursor>` 로 이어 읽습니다.
2. `updatedAt` 은 버전 · 댓글(링키 · 병원) · 상태가 마지막으로 바뀐 때입니다.
3. 다음 `updated_since` 는 받은 것 중 가장 늦은 `updatedAt` 에서 **5분 앞으로** 잡아 겹쳐 읽습니다. 커밋 시각이 `updatedAt` 보다 늦을 수 있어서입니다.
   - 겹친 항목은 `requestId` 와 `latestVersion` 으로 거릅니다.
   - 댓글만 바뀌면 `latestVersion` 이 그대로이니, `updatedAt` 도 함께 비교해 주세요.
4. 바뀐 스레드는 E5 로 읽어 `status` · `comments`(`change_request` `state` · `reservation_applied` `action`)를 반영합니다.

## 11. 알아 둘 것

- **생성 전 `change` 는 `new` 로 기록됩니다.** 예약이 없는(또는 만든 예약이 취소된) 스레드에 `change` 를 보내면 응답과 E5 의 `kind` 가 `new` 입니다. 병원은 이것을 [예약 생성]으로 처리합니다.
- **버전 번호는 서버가 매깁니다.** 1부터 시작하고, 본문에 번호 칸을 넣으면 400(모르는 키)입니다. 번호는 응답 `version` 으로 받습니다.
- **예약 있는 스레드에 다른 고객으로 `change` 를 보내면 400 `customer_changed`** 입니다. 고객이 바뀌면 새 요청(E1)을 보냅니다.
- **자동 처리**는 병원 동기화 때마다 일어나고, 링키 호출 없이 상태가 바뀝니다.
  - 요청됨이고, 예약이 없고, 확인 대기가 아니고, 마지막 버전 `start` 가 지났으면 `closed`(`expired`)가 됩니다.
  - 마지막 버전이 `cancel` 인데 예약이 이미 없으면(예약 현황에서 먼저 취소) `canceled` 가 되고, `reservation_applied` `cancel` 이 붙습니다.
- **닫힘 · 취소됨도 다시 열 수 있습니다.** `change` 를 보내면 `requested` 로 돌아가고 `closedReason` 은 null 이 됩니다.
- 철회(E3)는 멱등입니다. 이미 닫힌 스레드에 보내도 같은 200 응답이 오고, `closedReason` 은 바뀌지 않습니다.
- 요청 본문의 고객 정보는 E5 버전 `customer` 에 받은 그대로 남습니다.

## 12. 아직 정하지 않은 것

- **합친 메모의 필드 이름 · 통역 언어 표기** — KOS 메모에 들어가는 글자(「희망 시술」 · 「통역」 · 「예약 메모」, 언어 이름)는 임시이고 기획 확인 중입니다. 1000자 한도와 줄 형식은 정해졌습니다.
- **병원 화면 문구** — 버튼 이름과 안내 글은 임시입니다. 링키는 `code` · enum 값으로만 분기해 주세요. 「고객 확인 필요」 댓글 `body` 도 글자로 분기하지 마세요.
- **에이전시 페이지** 등 링키 화면 쪽 설계는 이 문서 범위 밖입니다.
