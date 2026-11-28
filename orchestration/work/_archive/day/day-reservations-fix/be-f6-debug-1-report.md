# be-f6-debug-1 — F6 [문진 QR] 이 잠깐 떴다 사라짐 · 태블릿에 안 감

**원인(확정)**: [문진 QR] POST 가 커밋 뒤 `display` 신호를 내고 → 웹이 SSE 로 그 신호를 받아 상세 모달을 **`GET /reservations/visits/{id}`** 로 다시 받는데, 이 GET 라우트가 `detail_view(...)` 에 **`origin` 을 안 넘긴다**(`routers/reservation_detail.py:179`). `visit_displays` 는 origin 이 없으면 `qrUrl = None`(`services/displays.py:515`) → 템플릿은 `pending ∧ qrUrl` 일 때만 QR 그림 · [태블릿에 보내기] · 기기 목록 자리를 그린다(`templates/partials/reservations_display.html:55-62`) → **수십 ms 뒤 덮어쓴 모달에서 QR · 보내기 버튼이 빠진다.** 상태는 여전히 `pending` 이라 머리 줄(「대기 · 남은 시간 mm:ss」)만 남고, 10분 뒤 `day.js` 초 세기가 0 이 되면 모달을 다시 받아 「만료 · 시간이 지났어요」가 된다(스크린샷 상태).

- 시한 · 시간대 · DB/앱 시계 · 요청 중복 생성 · 앞 요청 취소는 **원인 아님**(아래 실물 근거 표).
- 버튼이 사라지니 기기 줄을 누를 수 없어 **웹 문진은 기기 있는 요청이 한 번도 안 만들어졌다**(오늘 컨테이너 기동 02:22Z 뒤 웹 문진 행 전부 `device` 없음) → 태블릿에 안 감. 태블릿 받기 경로 자체는 살아 있다(같은 시각대 여권 스캔은 기기로 가서 태블릿이 받고 닫음).

## 1. 코드 경로 (file:line)

| 차례 | 자리 | 내용 |
| --- | --- | --- |
| 1 | `templates/partials/reservations_display.html:20-23` | [문진 QR] = `hx-post /reservations/visits/{v}/display-requests` → `#modal-root` |
| 2 | `routers/reservation_displays.py:116-125` | `displays.create(..., public_origin(request))` → `_modal()` 이 `detail_view(..., public_origin(request))`(`:68-70`) — **이 응답엔 QR 이 있다** |
| 3 | `services/displays.py:317-318` | 커밋 뒤 `signal()` → `board_events.display_changed`(`services/board_events.py:131-137`) — 병원 채널 `{"type":"display","visitId"}` |
| 4 | `static/day.js:2592-2599` | SSE `display` + 열린 모달이 그 방문 → `resOpenDetail(visit)` → `:2482-2490` `htmx.ajax("GET", "/reservations/visits/{v}")` → `#modal-root` 덮어씀 |
| 5 | `routers/reservation_detail.py:179` | `detail_view(session, view.current, visit_id, _now())` — **origin 없음**(`services/reservation_detail.py:134` 기본값 `None`) |
| 6 | `services/displays.py:515` | `url = qr_url_of(row, origin) if origin and status == PENDING else None` → `qrUrl: null` |
| 7 | `templates/partials/reservations_display.html:55-62` | `{% if q.status == "pending" and q.qrUrl %}` 안에 QR(`:56`) · [태블릿에 보내기] / 「{기기}에 표시 중」(`:57-60`) · 기기 목록 자리(`:61`) — 전부 빠짐. 머리 줄 `:48`(남은 시간 span) 은 남음 |
| 8 | `static/day.js:5888-5904` | 남은 시간 0 → `resOpenDetail` → GET → 서버가 읽을 때 시한 판정(`services/displays.py:513-514`) → 「만료 · 시간이 지났어요」(`:51`) |

같은 결함이 있는 다른 모달 다시 그리기(origin 없음): `routers/reservation_detail.py:327`(동행 저장) · `:407`(신분확인) — 열린 QR 이 있을 때 이 쓰기를 하면 QR 이 같은 식으로 사라진다. 앱 JSON `routers/api/reservations.py:104` 도 origin 없음(앱 상세 `displays[].qrUrl` 늘 null — 앱은 QR 을 `createDisplay` 응답의 qrUrl 로 그려서 지금 증상은 없음).

시험 공백: `tests/day/web/test_reservation_detail_display_screen.py` 는 detail 값을 Fake 로 넣어 템플릿만 본다(`:31` qrUrl 직접 넣음) → 「GET 상세 라우트가 열린 문진 QR 을 그리는가」를 실제 service 로 보는 시험이 없어 못 잡았다.

## 2. 실물 근거 (dev · 읽기만)

dev = VM `day-vm` · compose project `day-dev`(`docs/development/deployment.md:11-15 · :58`). `day-dev-api-1` 기동 `2026-11-27T02:22:30Z` · 이미지 revision `65506f35`(= 이 작업 base). prod 로그 · prod DB 는 안 봄. id 는 앞 8자.

### 2.1 서버 로그 — POST 직후 GET 상세(웹 SSE 다시 받기)

| POST `/reservations/visits/4a9e7a98…/display-requests` (UTC) | 이어진 `GET /reservations/visits/4a9e7a98…` | 차이 |
| --- | --- | --- |
| 02:27:14.632 | 02:27:14.685 | 53 ms |
| 03:55:17.559 | 03:55:17.594 | 35 ms |
| 03:55:22.394 | 03:55:22.540 | 146 ms |
| 03:55:24.239 | 03:55:24.271 | 32 ms |
| (마지막 생성 03:55:23.993 + 600 s = 04:05:23.99) | 04:05:25.011 GET | 시한 +1 s — `day.js` 초 세기 0 → 다시 받기 → 「만료」 |

- 03:55:17 → :22 → :24 에 [문진 QR] 을 5 초 안에 3 번 누름 = QR 이 사라져 사용자가 다시 누른 꼴. 그 사이 `display-targets` GET 없음(보내기 버튼이 없어 기기 목록을 못 엶).
- `display signal failed` 로그 없음(오늘). 오류 응답 없음(전부 200).

### 2.2 DB — `day_dev.display_request` 오늘(KST) 행 · `SET TRANSACTION READ ONLY`

DB `now() - clock_timestamp()` = −0.0065 s(쿼리 시점). 시각 값 대신 차이(초)만.

| id | 방문 | kind | 상태 | 기기 | 만든 시각(UTC) | 만료−생성 | 닫힘−생성 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 07d3e411 | 4a9e7a98 | questionnaire | canceled | 없음 | 02:25:27 | 600.0 | 106.9 |
| f5b1d29c · 9e1e71d5 · 91429a3a · d9fa9f69 | 4a9e7a98 | scan | canceled | **있음** | 02:25:22 ~ 02:26:14 | 600.0 | 2.4 ~ 10.4 |
| e44deec3 | 4a9e7a98 | scan | canceled | **있음** | 02:26:43 | 600.0 | 1330.5(웹 취소 02:48:54) |
| 504a4c47 | 4a9e7a98 | questionnaire | expired | 없음 | 02:27:14 | 600.0 | 5282.8(다음 생성 때 `expire_open`) |
| 91d597aa · 19a04727 | 4a9e7a98 | questionnaire | canceled | 없음 | 03:55:17 · :22 | 600.0 | 4.9 · 1.8(다음 클릭이 취소) |
| 283569ff | 4a9e7a98 | questionnaire | pending(행 값 · 읽을 때 만료) | 없음 | 03:55:23 | 600.0 | — |
| 45ce0b8b … 2ea64a95 (14행) | c31be33a | questionnaire | canceled 13 · pending 1 | 3행 있음 · 11행 없음 | 02:16:36 ~ 02:19:49 | 600.0 | 0.7 ~ 85.8 |

읽은 것:
- **만료−생성 = 600.0 s 전부** — `expires_at`(앱 시각 + 10분)과 `created_at`(DB `now()`)이 어긋나지 않음 → 시간대 · naive/aware · 시계 차 원인 아님.
- 웹 문진 요청은 클릭 1 번에 1 행 · 앞 행은 **다음 클릭 때만** 취소(닫힘−생성 = 다음 클릭까지 간격) → 신호로 다시 그릴 때 새 요청이 생기거나 앞 요청이 취소되는 일 없음.
- 기동(02:22Z) 뒤 문진 행은 전부 `device` 없음 · 여권 스캔은 `device` 있음 → **문진만 기기로 못 보냄**(버튼 사라짐), 기기 보내기 자체는 동작.
- c31be33a 의 기기 있는 문진 3행(02:16 ~ 02:18)은 현 컨테이너 기동 전이라 로그가 없어 웹 / 앱 어느 쪽인지 **확인 못 함**.

### 2.3 dev 환경 키(값 출력 안 함)

| 키 | 있음/없음 | 뜻 |
| --- | --- | --- |
| `DAY_PUBLIC_API_BASE` | 있음 | POST 경로 origin 정상 — `origin_of` 가 null 아님. 원인은 GET 이 origin 을 아예 안 넘기는 것 |
| `DAY_DISPLAY_TTL_MINUTES` | 없음 | 기본 10분(`common/config.py:215`) — DB 600 s 와 맞음 |
| `DAY_QWEB_FILL_MINUTES` | 없음 | 기본 60분 |

로컬 pytest 재현은 안 했다(GET 라우트 + 실제 service 를 보는 기존 시험이 없고, infra 시험은 DB 가 필요 — 로컬 스택을 띄우지 말라는 브리프). 로그 + DB + 코드가 같은 말을 해 「확정」으로 둔다.

## 3. 고칠 자리 (고치지 않음)

1. **`services/reservation_detail.py:134`** — `origin: str | None = None` 기본값을 없애 필수로 → mypy 가 origin 없는 호출 4곳을 다 잡는다(재발 방지 = 타입).
2. **`routers/reservation_detail.py:179 · :327 · :407`** — `reservation_displays.public_origin(request)` 과 같은 값(`displays.origin_of(str(request.base_url))`)을 넘긴다. 공용 함수 자리는 `routers/reservation_displays.py:46-47` 을 같이 쓰거나 service 쪽으로.
3. **`routers/api/reservations.py:104`** — 앱 상세도 origin 을 넘길지(앱 상세 `displays[].qrUrl` 계약을 살릴지) 결정. 지금은 늘 null.
4. (선택) `templates/partials/reservations_display.html:57-61` — 「{기기}에 표시 중」 · 기기 목록 자리를 `qrUrl` 조건 밖으로(qrUrl 이 없어도 보냄 상태는 보이게).
5. 시험: GET `/reservations/visits/{v}` 를 실제 service 로 — pending 문진이 있으면 QR(`day-res-dp__qr`) · [태블릿에 보내기] 가 그려지는지(infra · 웹 라우트). 그리고 POST 응답과 GET 응답의 진행 칸이 같은지.

## 4. 새 흐름(기기 팝오버에서 고르면 그때 생성 · 바로 보냄)에도 남는가

**남는다.** 새 흐름도 `displays.create` → `signal`(`services/displays.py:318`) → 웹 SSE → origin 없는 GET 상세로 모달을 덮어쓴다. 그러면
- 「{기기}에 표시 중」(`reservations_display.html:58`)이 `qrUrl` 조건 안이라 사라진다(태블릿엔 감 — `pending()` 은 origin 을 넘김 `routers/api/displays.py:142`).
- [링크 복사] · [링크 열기] · 이 화면 QR 을 진행 칸의 `qrUrl` 로 그리면 같은 식으로 사라진다.
- 팝오버를 모달 안에 두면 SSE GET 이 모달을 통째로 덮어써 팝오버도 닫힐 수 있다(코드상 추정 — 팝오버 자리 설계에 따름).

→ 새 흐름 구현 전에(또는 같이) §3 의 1 · 2 를 넣어야 한다.

## 5. 여권 스캔 · 앱 영향

| 기능 | 닿나 | 근거 |
| --- | --- | --- |
| 웹 [여권 스캔] | **안 닿음** | 스캔은 qrUrl 을 안 쓰고 진행 칸이 `s.status` 만 봄(`reservations_display.html:65-75`). 로그 02:25 ~ 02:26: `display-targets` → POST(기기 있음) → 태블릿 `GET /api/display-requests/pending` → 태블릿 `POST /api/display-requests/{id}/close` — 끝까지 동작 |
| 앱 [문진 QR](이 기기) | 안 닿음 | QR 을 `createDisplay` 응답 qrUrl 로 그림(`routers/api/displays.py:106` origin 넘김) |
| 앱 「태블릿에 보내기」 | 안 닿음 | 앱은 기기를 먼저 고르고 POST 하나로 보냄(`app/lib/ui/display_flows.dart:120-`) — 다시 그린 상세에 기대지 않음. 받는 태블릿 `pending()` 도 origin 넘김 |
| 앱 예약 상세 JSON `displays[].qrUrl` | 늘 null | `routers/api/reservations.py:104` origin 없음 — 지금 앱이 이 값을 QR 에 쓰는 곳은 이번에 확인 못 함 |
| 웹 동행 저장 · 신분확인 | **닿음** | `routers/reservation_detail.py:327 · :407` 도 origin 없음 — 열린 문진 QR 이 이 쓰기 뒤 사라짐(코드 근거 · 실물 확인 못 함) |

## 6. 한 일 · 안 한 일

- 레포 수정 · 커밋 없음. dev 에 쓰기 없음(로그 `docker logs` 읽기 · DB `READ ONLY` 트랜잭션 SELECT 1회 — api 컨테이너 안 파이썬으로, 접속 값 출력 없음). 스크립트 = `/private/tmp/be-f6-debug-1/q.py`.
- prod · `~/.config/day/prod-*` 안 봄. 고객 이름 등 원문 기록 없음(스크린샷의 이름은 시험 데이터로 보이나 옮기지 않음).
