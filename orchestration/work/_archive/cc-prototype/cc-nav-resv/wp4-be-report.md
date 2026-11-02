# WP4-BE 결과 보고 — 예약관리 데모 API (SPEC-002 §3.1 · §3.2)
## 상태: done (커밋·push·PR 안 함 — 워크트리에 변경만)

## 수행 — 파일·모듈
- 새 파일: `cc/back/app/api/reservations.py` (router) · `app/service/reservation_service.py` (전이 규칙 `TRANSITIONS` 한 곳 + 조작) · `app/service/resv_demo.py` (가짜 풀 · 수정 시간 · 메모 · snapshot) · `app/repository/reservation_repo.py` · `tests/test_reservations.py` (12개)
- 고친 파일: `app/repository/db.py` (`resv_request` 테이블, `CREATE IF NOT EXISTS` 라 기존 DB 에도 자동 생성) · `app/container.py` (`reservations` 조립) · `app/main.py` (라우터 등록) · `app/schemas/requests.py` (`ChangeRequestBody`) · `app/api/admin.py` (reset → `c.reservations.reset()` = 1차 reset + 예약 줄 비우기) · `app/service/board_service.py` (`lock` 속성만 추가 — 1차 동작 변경 없음)

## 검증
- `uv run pytest` → **65 passed** (기존 53 + 새 12) · `uv run ruff check .` → All checks passed
- 기능 폴더 밖 import 없음(grep 확인). 사용자 포트·프로세스(8610 back) 안 건드림 — 예시 JSON 은 임시 DB + TestClient 로 뽑음

## 계약 대조
| SPEC 항목 | 결과 |
|---|---|
| §3.1 필드(camelCase) 16개 | 같음 — 모든 줄에 키가 항상 있음(해당 없으면 null) |
| GET 줄 전부 + counts + version | 같음. `rows` = 묶음(groupId) 단위 최신 묶음이 위, 묶음 안은 id 오름차순 |
| counts | needCheck = requested+modify_requested · changeRequested = change_requested · confirmed = confirmed+modified · total = 묶음 수(시안 「전체 예약」= chains.length) |
| demo/request | 같음 — 풀 순번 = 지금 묶음 수 % 3 (reset 하면 처음부터) |
| demo/modify 대상 | 같음 — 묶음마다 **마지막 줄**을 봐서 change_requested 중 가장 최근(changeAt), 없으면 confirmed/modified 중 가장 최근(registeredAt). 마지막 줄이 확인중인 묶음은 대상 아님(시안 modTarget 과 같은 기준). 없으면 409 `no_modify_target` |
| register | 같음 — requested→confirmed / modify_requested→modified, registeredAt · snapshot. modify 면 같은 묶음의 superseded 아닌 나머지 줄 전부 → superseded (snapshot 은 그대로 보관) |
| change-request | 같음 — requested/modify_requested 만, 사유 strip 후 비면 400 `empty_reason`, body 에 reason 없으면 400 `invalid_request` |
| 409 형식 | 1차 그대로 `{"error":{"code","message"}}` — code `invalid_status` / `no_modify_target`. 없는 id = 404 `reservation_not_found` |
| version · SSE | 1차와 같은 meta `version` +1 · 같은 EventBus publish. 1차 BoardService 잠금 공유 |
| reset | 1차 reset 후 예약 줄 비움(같은 잠금 안). seed 없으면 1차처럼 404, 예약 줄 그대로 |
| KOS 주석 | register 의 request/modify 갈래에 SPEC-001 §9 형식 2개. 「공식: 예약 생성 / 예약 변경 — operationId 는 1차 HAR 범위 밖, 확인 필요」(sts research-patient-detail-report C-6: 공개 command 에 예약 생성·취소·변경이 있다는 것까지만 확인됨). KOS 호출 코드 0 |

## 정한 규칙 (SPEC 에 값이 없던 것)
- **수정 시간**: 변경 요청 반영(`change_request`) → `14:30`, 고객 시간 변경(`customer`) → `16:30` (시안 MOD_FROM_CHANGE / MOD_FROM_CUSTOMER). 이전 시간과 같으면 이전 + 1시간. 날짜 · 시술 · 통역은 안 바꾼다 → `before` 는 항상 `{"time": 이전}`
- **날짜**: `YYYY-MM-DD`, 받은 날(KST) + 2/3/3일 (시안 기준일 10-14 → 10-16 · 10-17 · 10-17). 시각 `time` = `HH:MM`
- **시각 값**(`receivedAt` · `changeAt` · `registeredAt` · `snapshot.at`) = epoch ms (1차 `receptionAt` 과 같음)
- **id** = 정수 1부터, `groupId` = 첫 요청 줄 id. reset 뒤 1부터 다시
- **snapshot 키**: kind(register/modify) · at · name · reading · chart · nat · natCode · sex · isNew · visitType(신규 환자/재내원) · birth · phone · lastVisit(신규 「없음」/ 재내원 「2026.08.21」 — 시안 값) · source(「본사(링키)」) · date · time · endTime(+30분) · floor · zone · proc · lang · interpret(「<언어> 통역 필요」) · memo
- **memo**: `YY.MM.DD/링키 본사/<시술>/<언어> 통역 필요` (YY.MM.DD = 등록일 KST) + 수정이면 `\n*예약 시간 변경 <이전> → <새>` — 시안 memoOf 형식
- 가짜 풀은 시안 3명 그대로, 추가 인물 안 만듦

## front 에 넘길 것
- 「n 아래 예약으로 바뀜」 시각: superseded 시각 필드는 §3.1 에 없어 안 만들었다 → **같은 묶음 다음 modified 줄의 registeredAt** 을 쓰면 된다(같은 순간)
- 「수정 요청 받음 ↓」: 같은 묶음에 뒤 줄이 있으면 표시(필드 없음, 순서로 판단)
- 버튼 막힘(수정 요청 생성): front 에서 같은 규칙(묶음 마지막 줄)으로 계산하거나 눌러서 409 처리

## 이슈 · 코디가 확인할 것
- 예약 조작도 1차 version 을 올리므로, 데스크 조작 뒤 예약 조작이 끼면 1차 [되돌리기] 는 「마지막 조작 하나뿐」(400)으로 막힌다 — 다른 데스크 조작이 끼었을 때와 같은 동작
- KOS operationId(예약 생성 · 예약 변경) 미확인 — 공개 스펙 대조 필요

## 응답 JSON 예시 (임시 DB, 시계 2분 간격)
```
### POST demo/request → 200
{
 "version": 1
}

### POST 1/register → 200
{
 "version": 2
}

### POST 2/change-request → 200
{
 "version": 4
}

### POST demo/modify → 200
{
 "version": 5
}

### POST 3/register (modify) → 200
{
 "version": 6
}

### POST 3/register again (409) → 409
{
 "error": {
  "code": "invalid_status",
  "message": "이 줄은 지금 상태(modified)에서 할 수 없는 조작이에요"
 }
}

### POST 1/change-request empty (400) → 400
{
 "error": {
  "code": "empty_reason",
  "message": "변경 요청 사유를 적어 주세요"
 }
}

### GET /api/reservations → 200
{
 "rows": [
  {
   "id": 2,
   "groupId": 2,
   "kind": "request",
   "modifyReason": null,
   "receivedAt": 1791943680000,
   "customer": {
    "name": "[JP] TANAKA YUKI",
    "reading": "다나카 유키",
    "chart": "No.9058",
    "nat": "일본",
    "natCode": "JP",
    "sex": "여성",
    "birth": "1988.11.23 (만 37세)",
    "phone": "+81 90 0000 0000",
    "zone": "3층 / 일본",
    "isNew": false
   },
   "date": "2026-10-17",
   "time": "10:00",
   "proc": "리쥬란 힐러 2cc",
   "lang": "일본어",
   "before": null,
   "status": "superseded",
   "changeReason": "10:00 은 원장 상담이 마감됐어요. 같은 날 14:00 이후로 가능해요.",
   "changeAt": 1791943800000,
   "registeredAt": null,
   "snapshot": null
  },
  {
   "id": 3,
   "groupId": 2,
   "kind": "modify",
   "modifyReason": "change_request",
   "receivedAt": 1791943920000,
   "customer": {
    "name": "[JP] TANAKA YUKI",
    "reading": "다나카 유키",
    "chart": "No.9058",
    "nat": "일본",
    "natCode": "JP",
    "sex": "여성",
    "birth": "1988.11.23 (만 37세)",
    "phone": "+81 90 0000 0000",
    "zone": "3층 / 일본",
    "isNew": false
   },
   "date": "2026-10-17",
   "time": "14:30",
   "proc": "리쥬란 힐러 2cc",
   "lang": "일본어",
   "before": {
    "time": "10:00"
   },
   "status": "modified",
   "changeReason": null,
   "changeAt": null,
   "registeredAt": 1791944040000,
   "snapshot": {
    "kind": "modify",
    "at": 1791944040000,
    "name": "[JP] TANAKA YUKI",
    "reading": "다나카 유키",
    "chart": "No.9058",
    "nat": "일본",
    "natCode": "JP",
    "sex": "여성",
    "isNew": false,
    "visitType": "재내원",
    "birth": "1988.11.23 (만 37세)",
    "phone": "+81 90 0000 0000",
    "lastVisit": "2026.08.21",
    "source": "본사(링키)",
    "date": "2026-10-17",
    "time": "14:30",
    "endTime": "15:00",
    "floor": "3층",
    "zone": "3층 / 일본",
    "proc": "리쥬란 힐러 2cc",
    "lang": "일본어",
    "interpret": "일본어 통역 필요",
    "memo": "26.10.14/링키 본사/리쥬란 힐러 2cc/일본어 통역 필요\n*예약 시간 변경 10:00 → 14:30"
   }
  },
  {
   "id": 1,
   "groupId": 1,
   "kind": "request",
   "modifyReason": null,
   "receivedAt": 1791943440000,
   "customer": {
    "name": "[TW] LIN YA CHEN",
    "reading": "린야천",
    "chart": "No.9041",
    "nat": "대만",
    "natCode": "TW",
    "sex": "여성",
    "birth": "1991.03.08 (만 35세)",
    "phone": "+886 900 000 000",
    "zone": "3층 / 중화권",
    "isNew": true
   },
   "date": "2026-10-16",
   "time": "14:00",
   "proc": "울쎄라피 프라임 300shot",
   "lang": "중국어",
   "before": null,
   "status": "confirmed",
   "changeReason": null,
   "changeAt": null,
   "registeredAt": 1791943560000,
   "snapshot": {
    "kind": "register",
    "at": 1791943560000,
    "name": "[TW] LIN YA CHEN",
    "reading": "린야천",
    "chart": "No.9041",
    "nat": "대만",
    "natCode": "TW",
    "sex": "여성",
    "isNew": true,
    "visitType": "신규 환자",
    "birth": "1991.03.08 (만 35세)",
    "phone": "+886 900 000 000",
    "lastVisit": "없음",
    "source": "본사(링키)",
    "date": "2026-10-16",
    "time": "14:00",
    "endTime": "14:30",
    "floor": "3층",
    "zone": "3층 / 중화권",
    "proc": "울쎄라피 프라임 300shot",
    "lang": "중국어",
    "interpret": "중국어 통역 필요",
    "memo": "26.10.14/링키 본사/울쎄라피 프라임 300shot/중국어 통역 필요"
   }
  }
 ],
 "counts": {
  "needCheck": 0,
  "changeRequested": 0,
  "confirmed": 2,
  "total": 2
 },
 "version": 6
}

```
