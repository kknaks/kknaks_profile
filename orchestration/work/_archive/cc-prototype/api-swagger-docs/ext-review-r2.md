# 리뷰 리포트 — WORK-012 외부 연동 API / code 재검수 r2(수정 1) (2026-11-11)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs`(미커밋) · 기준 SPEC-008 **0.2.2** · 지난 리포트 `ext-review-r1.md` · `ext-be-report.md` 「수정 1」
- read-only. KOS 호출 0 · 서버 기동 0 · 사용자 포트 0. 확인은 scratchpad 의 재현 스크립트(`racescript/race_check.py` · `racescript/verify_w.py` — 가짜 KOS · TestClient · ASGITransport)로만 했다.

## 판정: **PASS** (FAIL 0 · 남은 WARN 0 · 새 경미 지적 1)

r1 의 W1 ~ W6 은 모두 닫혔다. 실물 재현 스크립트를 다시 돌려 확인했다. W7 은 SPEC 0.2.2 가 코드에 맞춰졌다. 회귀는 0이다.

### 수치(직접 1회씩)

| | 결과 |
|---|---|
| `uv run pytest -q` | **599 passed**(588 → +11) · 1 warning(httpx 사용 중단 경고) · 66.3s — be 주장과 같음 |
| `uv run ruff check .` | All checks passed |
| 직원 OpenAPI(`openapi-after.json` ↔ 지금) | 직원 경로 차이 **0** · 직원 스키마 차이 **0** · 앱 설명에서 지운 줄 **0** |
| 외부 문서(r1 덤프 ↔ 지금) | 바뀐 operation = 조회 · 예약(오류 표) · Ext 스키마 변화 0 · 앱 설명 +1줄(W2 문장) |
| 기존 시험 · 직원 코드 diff | `test_openapi_docs` · `test_order` · `test_kos_sync` · `reservations.py` · `main.py` 의 diff 줄 수가 r1 과 같다(5 · 4 · 5 · 11 · 5) — 수정 1 이 건드리지 않음 |

## r1 지적별

| # | r1 지적 | 실물 확인(재현) | 판정 |
|---|---|---|---|
| W1 | 이름 검색 2xx 모양 오류 → 0명 | `service/ext.py:172-175` — `data` 가 list 가 아니면 502. 이 판정이 `count` 상한(`:176-178`)보다 먼저 온다. 재현: 조회 `{"count":0}` · `{"data":{"x":1}}` · `{"items":[]}` · `{"data":null,"count":5000}` → **넷 다 502 `kos_unavailable`**. 예약 `{"data":null}` → **502 · `find-duplicated-visitor` · `create-visitor` · `reserve` 모두 0번**. 시험 `test_lookup_search_bad_shape_502`(시술권 0번) · `test_reserve_search_bad_shape_502_no_create` | **닫힘** |
| W2 | 앱 설명 띄어쓰기 문장 | `openapi.json` 앱 설명 외부 절 email 문장 바로 다음 줄에 SPEC 문장 그대로 있다. T29 단언(`test_ext_docs.py:47`) | **닫힘** |
| W3 | 예약 502 · 409 문구 | `api/ext.py` 예약 표 — 409 `kos_rejected` = 「중복 검사 · 고객 만들기 · 예약 쓰기 단계」. 502 = 「… · 이름 검색은 4xx 도 502 · 예약 응답에 일정 id 없음」이고 「다시 읽기」는 뺐다. 코드와 맞는다(`find` 는 모든 예외 → 502 · `kos_write` 는 4xx → 409 · `refresh_schedule` 실패 = None → 200). T29 단언(`:51`) | **닫힘** |
| W4 | 조회 400 줄의 `start` | `LOOKUP_INVALID`(`start` 없음) · `RESERVE_INVALID`(있음)로 나눴다. T29 단언(`:49`) | **닫힘** |
| W5 | 카운터 스레드 경쟁 | `require_ext_key` → `async def`(`api/ext.py:34`). 안에 `await` 가 없어서 키 비교 → 카운터 갱신이 이벤트 루프에서 끊기지 않고 한 번에 돈다. 미들웨어도 같은 스레드다. 재현(150 동시 요청 · `_recent` 에 1ms 지연 주입): r1 은 **150 모두 200** 이었는데 **이제 200 60 · 429 90**. 지연 없이도 60/90. 시험 `test_w5_concurrent_requests_never_exceed_limit`(be: `def` 로 되돌리면 실패 확인) | **닫힘** |
| W6 | 500 에 기록 · no-store 없음 | `api/ext.py` 미들웨어 `try` — 재현: `c.ext.menu` 가 예외 → **500 `{"error":{"code":"internal_error","message":"서버 오류가 났어요"}}` · `no-store` · `ext_call` 1줄 `(linky, GET /api/ext/menu, 500, internal_error)`**. 예외 문구(`secret-detail-xyz`)는 로그 · 본문에 0이다(로그에는 `RuntimeError` 만). 시험 `test_w6_unhandled_error_logged_and_no_store` | **닫힘** |
| W7 | null 칸 SPEC 갱신 | SPEC 0.2.2 §6.3 :342-349 — 옵션 `procedure`, 구성 `count` · `unit` · `listPriceExVat` · `procedure`, 단위 `value` 가 「KOS 가 주지 않으면 null」이다. `schemas/ext.py` 의 `| None` 칸과 하나씩 같다 | **닫힘(SPEC)** |

**SPEC 0.2.2 ↔ 코드(W1 · W3 · W7)**
- §4.2 「실패」(:245): 「`data` 가 배열 아님(키 없음 포함) = 502 · 예약은 `create-visitor` 0번」 = 코드 · 시험과 같다.
- §6.5 오류 표 409 `kos_rejected`(:426) · 502(:427 — 「다시 읽기 실패는 502 가 아니다 · 200」) = 코드 · Swagger 문구와 같다.
- §6.3 null 칸 = 스키마와 같다.
- 어긋남 0.

## 새 지적(경미 · 머지 막지 않음)

| # | 자리 | 무엇 | 방향 |
|---|---|---|---|
| N1 | `app/api/ext.py` 미들웨어 `except` 갈래 · SPEC §6.2 · §7.4 | W6 수정으로 새 code **`500 internal_error`** 가 생겼다. 그런데 SPEC 0.2.2 공통 오류 표(§6.2)와 Swagger(앱 설명 「공통 오류」 · 세 operation 응답 표 — 500 줄 0)에 없다. 또 이 500 은 `client` 가 null 이어도(예: 의존성 전 예외) IP 카운트에 넣지 않는다. SPEC §3.4 「`client` null 인 **모든** 오류 응답」의 글자와는 조금 다르다(서버 쪽 잘못이라 세지 않는 편이 맞아 보인다) | SPEC §6.2 · §7.4 에 「처리하지 못한 예외 = `500 internal_error` · `ext_call` 1줄 · IP 카운트 안 함」을 적는다(planner). Swagger 앱 설명 공통 오류 줄에 한 마디 더하면 충분하다 |

## 조용히 통과하는 자리(r1 에서 남은 것)

- **중복 검사 흉내**: `fake_kos` `find-duplicated-visitor` 의 이메일 일치는 대소문자까지 같아야 맞는 흉내다. 실물 KOS 의 이메일 비교 방식은 아직 확인하지 않았다. → WP-E2E-LOCAL ④ 에서 대소문자가 다른 같은 이메일로 1번 확인하기를 권한다(r1 그대로).
- W5 시험은 지연을 `_recent` 가 끝난 뒤에 넣는다. 지금 구조(`await` 없는 `async def` · 단일 스레드)에서는 어디에 넣어도 끼어들 수 없으므로 시험은 유효하다. be 는 `def` 로 되돌려 실패를 확인했다고 적었다(이 리뷰는 되돌려 보지 않음 — read-only).
