# Delivery #227 fix1 — 검수 W1 ~ W4 + 낮은 지적 결과 보고

## 상태: done (커밋 안 함 · KOS 실물 호출 없음 · 모델 · migration 변경 없음)

## 검증

| 명령 | #227 뒤 | fix1 뒤 |
|---|---|---|
| `uv run pytest -q -m "not infra"` | 175 passed · 90 deselected | **182 passed · 91 deselected** |
| `scripts/test.sh -q`(compose postgres · redis, `DAY_REQUIRE_INFRA=1`) | 265 passed | **273 passed** (20.7s) |
| `uv run ruff check backend scripts` | pass | All checks passed |

compose `up -d --wait postgres redis` 로 돌리고 `down` 했다.
로그인 테스트 파일: `test_auth_api.py`(infra) 23 → **24** · `test_auth_rules.py`(DB 없이) 10 → **17**.

**고친 줄을 되돌리면 실패하는지 직접 확인**: Lua 꺼내기에서 `DEL` 을 빼면(비원자) → 동시 2요청 테스트 실패 ·
advisory lock 줄을 지우면 → 동시 첫 로그인 테스트 실패. 되돌린 뒤 둘 다 통과.

## W 별 고친 곳

### W1 — 임시 토큰을 원자적으로 꺼낸다
- Redis 버전: 로컬 compose `redis:7-alpine`(GETDEL 6.2+ 가능). 남은 시간까지 같이 꺼내려고 Lua 한 번(`GET` · `PTTL` · `DEL`)으로 했다.
- `backend/day/services/auth.py:84-121` — `PendingStore` = `put` · `take`(원자적 꺼냄 → 값 · 남은 ms) · `put_back`(`SET PX NX` — 남은 시간이 0 이하면
  되돌리지 않음 · 이미 있으면 덮지 않음). `:98` `_TAKE_SCRIPT`.
- `:227-238` `choose_hospital` — 처음에 `take` 로 꺼내고, 세션을 못 만들면(`ServiceError` — 후보 밖 · 연결 끊김 · 직원 계정 없음 · KOS 장애 등)
  남은 시간으로 `put_back` 한 뒤 오류. `:240` `_choose` 가 검증 · 세션 만들기.
- 테스트(infra · 진짜 `RedisPendingStore` · Redis db 15):
  - `test_같은_임시_토큰_동시_두_요청은_세션_하나` — 첫 요청이 get-user-account 를 0.3초 기다리는 동안 둘째 → 200 / 401 `session_expired` · 세션 1개.
  - `test_후보_밖을_고르면_남은_시간_동안_다시_고를_수_있다` — 403 뒤 같은 토큰으로 200(구현 결정 4 유지).
  - `test_진짜_Redis_보관소는_5분으로_넣고_꺼내면_사라진다` — 「조용히 통과」 표 첫 줄: put → TTL ≤ 300 · take 한 번만 · put_back 남은 시간 · NX.

### W2 — 비밀값 dataclass repr
- `backend/day/emr/normalized.py:241` `NStaffSignIn.token` · `backend/day/dtos/auth.py:19-20` `IssuedSession.token` · `csrf_token` ·
  `:34` `PendingLogin.pending_token` · `:50` `CurrentSession.csrf_token` — 전부 `field(repr=False)`.
- 테스트(DB 없이): `test_auth_rules.py::test_토큰을_가진_값의_repr_에_토큰이_없다` — 네 값 모두 repr 에 토큰 문자열 없음.

### W3 — 로그인 경로가 연결 설정을 복호화하지 않는다
- 리뷰어 방향 중 단순한 쪽: 처음 만드는 직원은 `is_system_account = false`(`auth.py:488`), 동기화(sign-in 시스템 계정 id)가 다음 회차에 덮는다.
  `session.get(CrmConnection)` 을 지웠다 — 로그인 경로에서 연결 설정을 읽는 것은 후보 거르기의 `jsonb_extract_path_text(config, 'tenant_id')`
  (평문 칸 · 복호화 없음) 하나뿐이다.
- 테스트: `test_처음_만든_직원은_시스템_계정이_아니다_연결_설정을_풀지_않는다`(연결의 시스템 이메일과 같아도 false · is_active true).
  늘 참이던 `assert CrmVendor.KOS` 는 그 테스트와 함께 없앴다.

### W4 — DB 가 필요 없는 매트릭스 줄을 DB 없는 단위 테스트로
- `test_auth_rules.py` 에 가짜 `StaffAuthenticator` 로 옮겼다(세션 · 엔진 없음):
  - ② `test_틀린_비밀번호는_invalid_credentials`(호출 = sign_in · aclose)
  - ③ sign-in 단계 `test_sign_in_단계_KOS_장애는_kos_unavailable` × 403 Unsupported · 연결 실패 · 시간 초과(오류에 비밀번호 없음)
  - `test_KOS_가_토큰_만료를_안_주면_세션을_만들지_않는다`
  - 「로그인 중 KOS 401 재시도 없음」 `test_로그인_중_KOS_401_은_다시_sign_in_하지_않고_실패`(계정 찾기 한 번만 하는 가짜 세션 · 호출 = sign_in · user_tenants · aclose)
- API(infra)에는 대표만 남겼다: ② `test_틀린_비밀번호_401_아무_행도_없음`(행 0 은 DB 확인이라 유지) · ③ `test_KOS_장애는_503_세션_없음`(get-user-account 단계 1줄).
  옛 API 「KOS 401 재시도 없음」 테스트는 단위로 옮기고 지웠다.

## 낮은 지적

| 지적 | 반영 |
|---|---|
| Redis 임시 값의 이메일 · 이름 평문 | 값 **전체**를 `encrypt_value` 로(`auth.py:302`) — KOS 토큰 · 이메일 · 이름 모두 암호문 |
| 동시 첫 로그인 테스트 없음 | `test_같은_사람의_동시_첫_로그인은_계정_하나`(두 요청 동시 → 둘 다 200 · 계정 연결 1 · 세션 2). lock 을 지우면 실패 확인 |
| `"p" not in …split()` | `test_kos_staff_client.py` — 긴 고유 비밀번호 · 부분 문자열(`str` · `repr` 둘 다) 검사 |
| `assert CrmVendor.KOS` | W3 와 같이 없앰 |
| A3 로그 검사가 진짜 client 를 안 지남 | 참고 항목 — 그대로(httpx 는 본문을 찍지 않고, #226 에서 httpx 로그를 WARNING 으로 올렸다) |

## 남은 것

- 로그인 시도 횟수 제한 · 세션 중 계정/직원 비활성 처리 — 계약 밖(리뷰 「참고」 · 「실물에서 만날 자리」).
- 그 밖 #227 리포트의 「남은 것」 그대로.
