# KOS 웹앱 내부 API — HAR 분석 (DEMO, 2026-10-13)

- 조사자: cc-prototype `researcher` 워커. **HAR 파일 읽기만 했다.** 어떤 요청도 다시 보내지 않았고(재전송 · curl · 토큰 사용 0), HAR 를 복사하거나 고치지 않았다. 이 리포트 말고 만든 파일 없음
- HAR: `/Users/kknaks/Downloads/app.kos-solution.com.har` — Chrome DevTools(`WebInspector 537.36`) 저장, 항목 16개, 녹화 시각 2026-10-13 15:20:42 ~ 15:21:37 KST(약 55초)
- 화면: 모든 KOS 요청의 `kos-client-uri` 가 `https://app.kos-solution.com/<tenantId>/reservation/flow?id=<scheduleId>` → **내원 현황의 동선 화면, 일정 1개**(`dd60eae7-…`)에서 한 조작이다
- 비교용 공개 스펙: `https://developers.kos-solution.com/openapi.yaml`(2026-10-13에 받음, `info.version` 1.0.1, 작업 75개). 이 공개 스펙 문서만 받았고 KOS API 는 호출하지 않았다
- 표기: **사실** = HAR · 스펙에 있는 것, **추정** = 해석. 시각은 KST

---

## 결론 한 장

**이 HAR 에 담긴 쓰기 동작은 세 가지뿐이다.** 단계 변경 2회, 그리고 「귀가 대기로 변경 + 일괄 취소」 1회(요청 2개)다. 워크플로 대응표에 있는 **담당자 · 집도의 · 방 · 우선순위 · 시술 완료하기 · 시술 취소하기(단건) · 상담사 지정 · 시술 추가는 HAR 에 없다**(녹화하지 않음). 그 동작들의 내부 API 는 이번 자료로 알 수 없다.

| 화면 동작(추정) | 내부 API(사실) | 요청 본문 | 공개 OpenAPI |
|---|---|---|---|
| 단계 → 시술 대기 | `POST api.kos-solution.com/tenants/{tenantId}/schedule/v1/commands/change-flow-step` | `{id, step:"PROCEDURE_WAITING"}` | **있음** — `changeFlowStep`(필드 이름 `id` ↔ 공개 `scheduleId` 만 다름) |
| 단계 → 시술 | 같은 경로 | `{id, step:"PROCEDURE"}` | 있음 — `changeFlowStep` |
| **귀가 대기로 변경 + 미완료 일괄 취소** | ① `…/schedule/v1/commands/cancel-flow-tasks` → ② `…/change-flow-step` | ① `{scheduleId, sequences:[1,2,3,4], reason:"CANCEL"}` ② `{id, step:"PROCEDURE_DONE"}` | ① **공개 없음** ② 있음 |
| 담당자 · 집도의 · 방 · 우선순위 · 시술 완료하기 · 시술 취소하기(단건) · 상담사 지정 · 시술 추가 | **HAR 에 없음** | — | 공개 스펙에도 없음(작업 이름으로 대조) |

**「귀가 대기 일괄 취소」의 정체(사실):** 요청 **2개**가 순서대로 나간다. 먼저 `cancel-flow-tasks` 가 취소할 시술을 **본문의 `sequences` 배열**(작업 순번 목록)로 한 번에 보내고, 142ms 뒤 `change-flow-step` 이 `PROCEDURE_DONE` 으로 단계를 바꾼다. 일괄 취소는 단계 변경 요청에 묶여 있지 않은 **별도의 작업 취소 명령**이다. 목록을 받는 꼴이라 **단건 「시술 취소하기」도 같은 명령에 순번 1개를 보내는 것으로 추정**한다(HAR 로 확인 안 됨).

---

## 1. 요청 목록 요약

16개 = KOS API 10 · 분석/로그 6(`browser-intake-datadoghq.com` `/api/v2/rum` 5 · `api2.amplitude.com` `/2/httpapi` 1). 정적 파일(JS · CSS · 이미지) 요청은 HAR 에 0개다. 분석 요청 6개는 목록에서 뺐고 내용도 보지 않았다(쿼리에 클라이언트 키가 들어 있을 수 있음).

KOS API 10개(모두 `POST` · 응답 200 · 호스트 `api.kos-solution.com` · 경로 앞부분 `/tenants/<tenantId>`):

| # | KST | 경로(접두 뒤) | 종류 | 걸린 시간 |
|---|---|---|---|---|
| 0 | 15:20:42.953 | `/schedule/v1/commands/change-flow-step` | **쓰기** | 57ms |
| 2 | 15:20:45.056 | `/account/v2/queries/get-accounts-last-update-date-time-utc` | 조회 | 35ms |
| 3 | 15:20:45.057 | `/schedule/zone/room/v1/queries/get-rooms` | 조회 | 40ms |
| 6 | 15:20:51.089 | `/schedule/v1/commands/change-flow-step` | **쓰기** | 63ms |
| 8 | 15:21:15.611 | `/role/v2/queries/get-roles` | 조회 | 36ms |
| 9 | 15:21:15.612 | `/schedule/zone/room/v1/queries/get-rooms` | 조회 | 38ms |
| 10 | 15:21:33.015 | `/role/v2/queries/get-roles` | 조회 | 38ms |
| 11 | 15:21:33.018 | `/schedule/zone/room/v1/queries/get-rooms` | 조회 | 35ms |
| 13 | 15:21:36.490 | `/schedule/v1/commands/cancel-flow-tasks` | **쓰기** | 91ms |
| 14 | 15:21:36.632 | `/schedule/v1/commands/change-flow-step` | **쓰기** | 59ms |

- **쓰기 요청 = 4개**(`/commands/` · POST). 조회 6개도 POST 다(KOS 는 조회도 POST — 공개 스펙과 같음)
- `get-roles` + `get-rooms` 쌍이 15:21:15 · 15:21:33 에 두 번 나왔다. 둘 뒤에 이어진 쓰기가 없어서 무슨 창을 열었는지는 알 수 없다(추정: 동작 바의 담당자 · 방 선택 창이나 단계 변경 창을 연 것)

---

## 2. 쓰기 요청 상세(동작별)

HAR 쓰기 요청 **4개 = 아래 표 4행.**

| # | 추정 동작 | 판단 근거 | 경로 | 요청 본문(필드 · 값 모양) | 응답 |
|---|---|---|---|---|---|
| 0 | 단계 변경 → **시술 대기** | 경로 `change-flow-step` + `step` 값 | `/tenants/{tenantId}/schedule/v1/commands/change-flow-step` | `id`: 일정 UUID(`dd60eae7-9d0f-4371-b1a4-d265918c7d7d`) · `step`: `"PROCEDURE_WAITING"` | 200 `{}` |
| 6 | 단계 변경 → **시술** | 같음 | 같음 | `id`: 같은 일정 · `step`: `"PROCEDURE"` | 200 `{}` |
| 13 | **미완료 시술 일괄 취소** | 경로 `cancel-flow-tasks`(동선 작업 취소) · 본문 순번 목록 · 바로 뒤 #14 | `/tenants/{tenantId}/schedule/v1/commands/cancel-flow-tasks` | `scheduleId`: 일정 UUID · `sequences`: 정수 배열 `[1,2,3,4]`(작업 `tasks[].sequence` 와 같은 이름 — 추정) · `reason`: 문자열 `"CANCEL"`(다른 값은 HAR 에 없음) | 200 `{}` |
| 14 | 단계 변경 → **귀가 대기** | `step` = `PROCEDURE_DONE`(공개 스펙 뜻 「귀가 대기」) | `…/change-flow-step` | `id`: 같은 일정 · `step`: `"PROCEDURE_DONE"` | 200 `{}` |

- 사실: 내부 `change-flow-step` 은 일정 id 를 **`id`** 로, `cancel-flow-tasks` 는 **`scheduleId`** 로 받는다
- 사실: 응답 4개 모두 본문 `{}`(2바이트). 바뀐 일정을 돌려주지 않는다
- 요청 헤더 `content-type: application/json`. 테넌트 id 는 본문이 아니라 **경로**에 들어간다

---

## 3. 귀가 대기 + 일괄 취소

순서(사실):

```text
15:21:33.015  get-roles          (조회)
15:21:33.018  get-rooms          (조회)
15:21:36.490  cancel-flow-tasks  {scheduleId: dd60eae7-…, sequences: [1,2,3,4], reason: "CANCEL"}  → 200 {}
15:21:36.632  change-flow-step   {id: dd60eae7-…, step: "PROCEDURE_DONE"}                         → 200 {}
```

- **요청 2개**이고, 시술 목록은 첫 요청(`cancel-flow-tasks`) 본문의 `sequences` 에 **순번으로** 담긴다(시술권 id · 작업 id 가 아님)
- 웹앱이 취소를 먼저, 단계 변경을 나중에 보낸다. 두 요청 사이 142ms — 첫 응답(91ms)을 받은 직후 두 번째를 보냈다(추정: 웹앱이 차례로 호출)
- 일정의 작업이 몇 개였는지, 그중 완료된 것이 있었는지는 HAR 에 응답이 없어 알 수 없다. `[1,2,3,4]` 가 「미완료 전부」인지 「전체」인지 확인 불가
- `reason` 이 `"CANCEL"` 하나만 보인다. 공개 스펙의 예약 취소(`CancelReservationCommand.reason`)와 같은 열거형인지는 알 수 없다

---

## 4. 공개 OpenAPI 대조

공개 스펙 75개 작업의 경로 · operationId 와 대조했다. 공개 경로는 `/<서비스>/open/v1/…`, 내부 경로는 `/tenants/{tenantId}/<서비스>/v1/…` 꼴이다.

| 내부 요청 | 공개 같은 작업 | 차이 |
|---|---|---|
| `schedule/v1/commands/change-flow-step` | `changeFlowStep` — `POST /schedule/open/v1/commands/change-flow-step`(「내원흐름단계 변경」) | 본문 `id` ↔ 공개 `scheduleId`(필수 2칸: `scheduleId` · `step`). `step` 값은 공개 열거형(`RESERVED … PROCEDURE_DONE · COMPLETED`)과 같음. 응답 둘 다 비어 있음(`protos.Empty`) |
| `schedule/v1/commands/cancel-flow-tasks` | **공개 없음** | 공개 스펙의 취소는 `cancelReservation`(예약 취소)뿐 — 동선 작업 취소는 없다 |
| `schedule/zone/room/v1/queries/get-rooms` | **공개 없음** | 공개는 `getZones` · `getZone`(구역 `id · title · isDefault · order`만). 방 목록 작업은 없다. 방은 일정 `tasks[].room`(`RoomContract`)으로만 나온다 |
| `role/v2/queries/get-roles` | **공개 없음** | 공개 `getAccounts` 는 직원별 `roleTags`(문자열)만. 역할 목록(이름 · id)은 없다 |
| `account/v2/queries/get-accounts-last-update-date-time-utc` | **공개 없음** | 직원 목록 마지막 갱신 시각 1개를 돌려준다. 캐시 확인용으로 추정 |

**HAR 에 없어서 대조할 수 없는 동작**(공개 스펙에도 해당 이름의 작업이 없다): 담당자 · 집도의 · 방 · 우선순위 · 시술 완료하기 · 시술 취소하기(단건 — `cancel-flow-tasks` 로 추정) · 상담사 지정 · 시술 추가

---

## 5. 인증(헤더 이름만) · 호스트

**이 HAR 에는 인증 정보가 남아 있지 않다(사실).**

- 요청 · 응답 헤더 이름 전체(25종): `accept` · `accept-encoding` · `access-control-allow-credentials` · `access-control-allow-origin` · `content-encoding` · `content-length` · `content-type` · `cross-origin-resource-policy` · `date` · `dd-request-id` · `kos-client-uri` · `referer` · `sec-ch-ua` · `sec-ch-ua-mobile` · `sec-ch-ua-platform` · `strict-transport-security` · `traceparent` · `tracestate` · `user-agent` · `vary` · `x-content-type-options` · `x-datadog-origin` · `x-datadog-parent-id` · `x-datadog-sampling-priority` · `x-datadog-trace-id`
- `Authorization` · `Cookie` · `Set-Cookie` **0개**, HAR `cookies` 배열 0개. Chrome 은 HAR 를 내보낼 때 기본으로 민감한 헤더를 지운다. 그래서 웹앱이 무엇으로 인증하는지는 **이 HAR 로 알 수 없다**
- 단서(추정): 응답에 `access-control-allow-credentials: true` 가 있어 브라우저 쿠키 인증일 가능성이 있다. 공개 OpenAPI 는 `Authorization` 헤더(`exchangeToken` 으로 받은 토큰, `securitySchemes.auth_token`)를 쓴다
- 웹앱 고유 헤더: `kos-client-uri`(지금 보는 웹앱 화면 주소)

**호스트(사실):** 내부 API = **`api.kos-solution.com`**, 공개 OpenAPI = **`open-api.kos-solution.com`**(운영) · `open-api.kos-solution.dev`(개발). **둘은 다른 호스트**다. 내부 경로에는 테넌트 id 가 들어가고(`/tenants/{id}/…`), 공개 경로에는 없다(토큰으로 테넌트를 정함 — 추정).

테넌트: 경로의 `<tenantId>`(DEMO 지점). 운영 캡처(`2026-10-12T161224…`)의 구역 id `6a85064f…`와는 다른 지점이다.

---

## 6. 쓸 만한 조회

| 내부 조회 | 주는 것(사실) | 관제에 쓸 곳(추정) |
|---|---|---|
| `schedule/zone/room/v1/queries/get-rooms` 요청 `{zoneId}` | 그 구역의 **방 목록** `[{id, zoneId, title, order}]` — DEMO 28개(A-룸1~9 · A-레이저실 · A-트윈 1-1/1-2 · A-시술실1~3 · A-회복실1~3 · B-룸11~16 · B-트윈2-1~3-2), `order` 모두 0 | 현황판의 방 칸 원천. 지금은 공개 API 로 방 목록을 못 받아 일정의 `tasks[].room` 에서 모으는 수밖에 없다(`room-map-provisional.md`) |
| `role/v2/queries/get-roles` 요청 없음 | **역할 15개** `[{id, name, roleTags:[정수], featureList, isDefault}]` — 관리자 · 상담총괄실장 · 원장 · 피부관리 · 간호 · 코디 · 마취과 · CS팀(콜센터) · OWNER · 촬영팀 · 마케팅 · 상담실장 · 경영지원 · ADMIN · 대표원장 | 직원 → 화면 직군 매핑(`kos-staff-api-report.md` 정할 것 1). `roleTags` 가 **숫자**다. 원장 `[2]` · 상담실장 `[3]` · 간호 `[4]` · 피부관리 `[5]` · CS팀 `[6]` · 코디 `[6,3,7]` 으로 보아, 공개 열거형 순서(1 ADMIN · 2 DOCTOR · 3 COUNSELOR · 4 NURSE · 5 SKINCARE · 6 CALL_COUNSELOR · 7 COORDINATOR)와 맞는다(추정, 운영 캡처의 코디 태그 3종과도 일치) |
| `account/v2/queries/get-accounts-last-update-date-time-utc` | `{"data":"2026-10-12T00:41:25.942Z"}` | 직원 목록을 다시 받을지 판단(낮음) |

---

## KOS 요청서 초안 — 「이 동작들을 OpenAPI 로 열어 달라」 (결정은 코디 · 사용자)

**HAR 로 내부 API 가 확인된 것**

1. **동선 작업 취소** — 내부 `POST /tenants/{tenantId}/schedule/v1/commands/cancel-flow-tasks` `{scheduleId, sequences[], reason}`. 관제 「진행 안 함」 · 귀가 때 남은 시술 취소에 쓴다. 공개 `/schedule/open/v1/commands/cancel-flow-tasks` 로 열어 달라. `reason` 의 값 목록도 함께 요청
2. **방 목록 조회** — 내부 `get-rooms {zoneId}`. 공개 `getZone` 응답에 방을 넣거나 `getRooms` 를 열어 달라
3. **역할 목록 조회** — 내부 `get-roles`(역할 이름 · 태그)

**웹앱 화면엔 있는데 이번 HAR 에는 없는 것** — 다음 녹화로 경로를 확인한 뒤 요청에 넣을 것

4. 시술 완료하기(작업 DONE · 시술권 차감) — 워크플로 표의 「요청 1순위」
5. 담당자 · 집도의 지정(작업 `assignees` · `doctors`)
6. 방 지정 · 이동(작업 `room`)
7. 우선순위(작업 순서)
8. 상담사 지정(상담 기록 `counselors`)
9. 시술 추가(시술권으로 작업 생성)

**다음 녹화 제안(사실이 아니라 방법):** DEMO 지점 동선 화면에서 4~9를 한 번씩 누르는 동안 Network 를 녹화하면 된다. 이번처럼 민감 헤더를 지운 HAR 이면 충분하다(인증 값은 필요 없음).

---

## 검증 — 토큰 · 쿠키 값 0건

- **HAR 에서 뽑은 민감 값:** `Authorization` · `Cookie` · `Set-Cookie` 헤더 **0개**, `cookies` 배열 **0개** → 대조할 토큰 · 쿠키 값이 없다. 그래서 리포트에 들어갈 수도 없다
- 추가 대조: HAR 의 **모든 쿼리 문자열 값 35개**(분석 요청 URL — 클라이언트 키가 섞여 있을 수 있음, 8자 이상 20개)와 추적 헤더 값 65개(`x-datadog-*` · `traceparent` · `tracestate` · `dd-request-id`)를 리포트와 문자열 대조 → **0건**(값은 화면에 출력하지 않고 개수만 셈)
- 요청 본문 4개(쓰기) · 3종(조회)에 토큰류 필드 없음(`id` · `step` · `scheduleId` · `sequences` · `reason` · `zoneId`)
- 재전송: **0**(HAR 는 `json.load` 로 읽기만 함, curl 은 공개 스펙 YAML 1회만)
- 쓰기 요청 수: **HAR 4 = 표(§2) 4행**
- 고객 이름: HAR 의 KOS 응답에 고객 이름 칸 없음(방 · 역할 · 시각만). 리포트에 고객 이름 0
