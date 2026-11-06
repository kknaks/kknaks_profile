# 리뷰 리포트 — day-data-architecture / code · #227 fix1 재검수 (2026-11-06)

대상: 같은 워크트리의 미커밋 변경(fix1 반영 뒤). 근거 문서는 `backend-227-fix1-instructions.md` · `backend-227-fix1-report.md`, 앞 리포트는 `review-227-report.md` 다.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. compose 는 11042 · 11043 만 쓰고 끝나고 `down` 했다.

## 판정: PASS (FAIL 0 · WARN 0)

W1 ~ W4 와 낮은 지적은 지적대로 닫혔다. 아래 「참고」 둘은 동작을 막지 않는 작은 것이라 판정에 넣지 않았다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q`(DAY_REQUIRE_INFRA=1) | **273 passed / 20.4s** |
| `uv run pytest -q -m "not infra"` | **182 passed · 91 deselected / 2.6s** |
| `uv run ruff check backend scripts` | All checks passed |
| 시스템 계정 경로 `emr/kos/client.py` diff · migration | 0줄 · `0003` 그대로(새 리비전 없음) |

수정 리포트 수치(273 · 182/91)와 같다.

## W 별 확인

| | 판정 | 근거 |
|---|---|---|
| W1 | **닫힘** | 아래 따로 |
| W2 | **닫힘** | `field(repr=False)` — `emr/normalized.py:241` `NStaffSignIn.token` · `dtos/auth.py` `IssuedSession.token/csrf_token` · `PendingLogin.pending_token` · `CurrentSession.csrf_token`. DB 없는 테스트 `test_auth_rules.py:114-129` 가 네 값의 `repr()` 에 비밀 문자열이 없는지 본다. frozen dataclass 의 `__eq__` · `__hash__` 는 `repr` 과 무관해 동작이 바뀌지 않는다 |
| W3 | **닫힘** | `services/auth.py` 에서 `session.get(CrmConnection)` 과 `system_email` 이 사라졌다(grep 0). 로그인 경로가 연결 설정에 닿는 곳은 후보 거르기 `jsonb_extract_path_text(config, 'tenant_id')`(`:175`) 하나다. 이것은 SQL 식이라 `EncryptedJSONB` 의 결과 처리(복호화)를 타지 않는다. 처음 만드는 직원은 `is_system_account=False`(`:488`). **동기화가 덮는 흐름도 확인했다**: 로그인이 `Refs.link(STAFF, …)` 로 같은 외부 id → 같은 DAY id 를 잇는다. #226 `apply_master` 의 staff upsert 칸에 `is_system_account` 가 있어, 다음 기준 정보 회차(최대 1시간 · 새 병원이면 `needs_master`)에 시스템 계정 id 기준으로 덮인다. 로그인은 있던 직원의 `is_system_account` · `is_active` 를 건드리지 않는다. 테스트 `test_auth_api.py:512-525`(연결의 시스템 이메일과 같아도 false). 늘 참이던 `assert CrmVendor.KOS` 는 없어졌다 |
| W4 | **닫힘** | `test_auth_rules.py` 17개(DB 없이). ② 틀린 비밀번호 · ③ sign-in 단계 KOS 장애 × 3 · 토큰 만료 없음 · 로그인 중 KOS 401 재시도 없음(호출 순서 `sign_in · user_tenants · aclose`). 가짜는 KOS 경계(`FakeAuth`)와 「계정 찾기 한 번」 읽기 세션(`NoAccountSession`)뿐이다. 도메인 규칙은 mock 하지 않았다. API(infra)에는 「행 0」(DB 확인) 대표 줄만 남았다. 2026-11-06 규칙에 맞다 |

### W1 — 원자적 꺼냄 · TTL · 되돌림

- **경합**: `_TAKE_SCRIPT`(`auth.py:98-104`)는 `GET` · `PTTL` · `DEL` 을 Lua 하나로 한다. Redis 는 스크립트를 한 번에 돌리므로 같은 키를 두 요청이 동시에 꺼낼 수 없다. 둘째는 `None` → 401 `session_expired`. infra 테스트 `test_같은_임시_토큰_동시_두_요청은_세션_하나`(`:531-551`)는 진짜 `RedisPendingStore`(`pending_store="redis"`)로 첫 요청이 KOS 를 0.3초 기다리는 동안 둘째를 넣고 → `[200, 401]` · 세션 1개를 확인한다. 「DEL 을 빼면 실패」를 수정 리포트가 직접 확인했다. 테스트 구조상 그 주장이 맞다.
- **TTL**: `put` 은 `EX 300`. 진짜 보관소 테스트(`:573-594`)가 `0 < TTL ≤ 300` · 한 번만 꺼냄 · 되돌린 뒤 `PTTL ≤ 꺼낼 때 남은 시간` · `NX`(있으면 덮지 않음)를 본다. 앞 리뷰의 「`RedisPendingStore` 조용히 통과」가 닫혔다.
- **되돌림**: `choose_hospital`(`:227-238`)은 `ServiceError` 일 때만 `put_back(key, raw, ttl_ms)` 한다(`SET PX NX`, `ttl_ms ≤ 0` 이면 안 함). 후보 밖 · 연결 끊김 · 직원 계정 없음 · 2단계 인증 · staff 비활성 · KOS 장애가 여기에 든다. `_finish` 의 `commit` 뒤에는 `ServiceError` 를 낼 줄이 없다. 그래서 「세션이 만들어졌는데 토큰이 되돌려져 한 번 더 쓰이는」 길이 없다. 「후보 밖 → 다시 고르면 200」은 `test_후보_밖을_고르면_…`(`:553-570`)가 진짜 Redis 로 확인한다.
- **되돌림 실패 경로**: `ServiceError` 가 아닌 예외(DB 오류 · Redis 오류 · 복호화 실패 · 요청 취소)는 되돌리지 않는다. 토큰이 소모돼 로그인부터 다시 해야 한다. 닫힌 쪽으로 실패하는 것이라 받아들인다. `put_back` 자체가 Redis 오류로 실패하면 그 예외가 원래 `ServiceError` 를 가린다(500). 드물고 결과(로그인부터 다시)는 같다.

### 낮은 지적

| 앞 리뷰 지적 | 판정 |
|---|---|
| Redis 임시 값의 이메일 · 이름 평문 | **닫힘** — 값 전체를 `encrypt_value`(`auth.py:302`), 꺼낼 때 `decrypt_value`(`:247`). 안쪽 KOS 토큰은 이제 따로 암호화하지 않는다(겉이 이미 암호문) |
| 동시 첫 로그인 테스트 없음 | **닫힘** — `test_같은_사람의_동시_첫_로그인은_계정_하나`(`:597-614`). 계정 연결 1 · 세션 2. lock 을 지우면 실패를 직접 확인했다(수정 리포트) |
| `"p" not in …split()` | **닫힘** — 긴 고유 비밀번호 · 부분 문자열 검사(`str` · `repr`) |
| `assert CrmVendor.KOS` | **닫힘**(W3 와 같이) |
| A3 로그 검사가 진짜 client 를 안 지남 | 그대로 — 참고 항목이었고 실해 없음(httpx 는 본문을 찍지 않는다 · WARNING 상향) |

## 조용히 통과하는 자리

새로 찾은 것 없음. 이번에 더한 테스트 넷(동시 임시 토큰 · 후보 밖 재시도 · 진짜 Redis 보관소 · 동시 첫 로그인)은 고친 줄을 되돌리면 실패하는 구조다.

## 참고 (판정 밖)

1. **되돌린 토큰의 남은 시간이 처리 시간만큼 늘어난다** — `auth.py:236` `put_back(key, raw, ttl_ms)` 의 `ttl_ms` 는 **꺼낸 순간**의 남은 시간이다. 그 사이 `_choose` 가 KOS get-user-account(최대 15초)를 기다린 시간은 빠지지 않는다. 실패할 때마다 시계가 그만큼 멈추는 셈이다. 실패하는 요청을 연달아 보내면 「5분」이 길어진다. 다만 그 안의 KOS 토큰은 자기 만료가 있고, 세션 만료 = KOS 토큰 만료라 실해는 낮다. 맞추려면 `take` 때 `time.monotonic()` 을 재고 `ttl_ms - 경과 ms` 로 되돌린다(0 이하면 버림).
2. **동시 요청에서 진 쪽은 앞 요청이 실패해 토큰이 되돌려져도 이미 401 `session_expired` 를 받는다.** 화면이 「로그인부터 다시」로 보내지만 토큰은 남은 시간 동안 살아 있다. 더블 클릭 같은 드문 경우이고 안전한 쪽이다. 화면 Delivery 에서 병원 고르기 버튼을 누른 동안 막아 두면 생기지 않는다.
