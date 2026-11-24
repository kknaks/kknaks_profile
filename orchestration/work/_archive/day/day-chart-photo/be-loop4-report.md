# be-loop4 결과 보고 — C35 시스템 토큰 Redis 공유 · C36 사진 토스트 글자

## 상태: done (커밋 안 함 · 템플릿 · JS 안 건드림) — SPEC planner-fix-12(DAY-SPEC-001 §3 규칙 9 · DAY-SPEC-002 토스트 표)

## C35 — 시스템 토큰 공유
| 위치 | 내용 |
|---|---|
| 새 `backend/day/emr/kos/token_store.py` | `SystemToken(token, expires_at, staff_external_id)` · `SystemTokenStore` 약속(read · write · 기다리지 않는 lock) · `RedisSystemTokenStore` — 키 `kos:system_token:{병원 id}:{internal\|open}:{자격 표시}`(자격 표시 = 테넌트 · 시스템 계정 · 클라이언트 표시의 sha256 앞 16자 — 연결 설정이 바뀌면 옛 토큰을 안 씀 · 값은 키에 없음) · 값 = `common.crypto.encrypt_value`(ENCRYPTION_KEY · 기존 방식) JSON 암호문 · TTL = KOS 토큰 만료까지(만료를 모르면 6시간 상한) · 잠금 `kos:system_token_lock:…`(SET NX · 60초) |
| `backend/day/emr/kos/client.py` `KosClient(token_store=…)` | `internal_token` · `open_token` → `_shared`: ⓐ 손에 든 사본이 쓸 만하면 그대로(만료 10분 전 기준 그대로) ⓑ 아니면 Redis 를 읽어 쓸 만하면 그것 ⓒ 없음 · 만료 · 401 이면 잠금을 잡은 **한 프로세스만** sign-in → Redis 에 넣음 · 못 잡은 쪽은 0.1초마다 다시 읽으며 최대 20초 기다림 · **401 은 Redis 토큰이 그 401 을 받은 토큰과 같을 때만 새로 받음**(다른 프로세스가 이미 바꿨으면 그것을 씀). 기다림 상한 · Redis · 키 고장 = 지금 방식(혼자 받기 · 경고 로그). 넣기만 실패해도 다시 sign-in 하지 않음. 시스템 계정 직원 id 도 같이 나눠 씀(조회 1회) |
| 〃 해제 규칙 | `SignInLimitExceeded` → 같은 표시 가장 오래된 1개 해제 → 한 번 다시 = `_new_internal_token` 안 그대로 — **새로 받는 그 한 프로세스에서만** 일어남(규칙 9 ⓒ) |
| `backend/day/emr/factory.py` `build_adapter` | KOS 클라이언트에 `RedisSystemTokenStore` 를 붙임. **`adapter_for` 와의 관계**: 클라이언트(HTTP 연결 · 손에 든 토큰 사본)는 프로세스마다 `adapter_for` 캐시 그대로 · 토큰만 Redis 로 공유. 백필 어댑터(`build_backfill_adapter` · 표시 `backfill` · 끝나면 자기 로그인 해제)는 공유하지 않음(지금 그대로) |
| 로그 | 토큰 · 비밀번호 · 키 값 없음 — 종류 · 병원 id · 예외 이름만 |

## C36 — 사진 토스트 글자
- `routers/board_messages.py` `PHOTO_SKIPPED_MESSAGE` = 「올리지 못한 사진이 있습니다 (JPEG · PNG, 5MB 이하만)」(빈 값 대체 — 빠진 장 요약 1장 · KOS 실패 글자와 「 · 」로 이음 · 3루프 그대로)
- 같은 결정의 413 글자 「한 번에 올릴 수 있는 용량(100MB)을 넘었습니다」 = `PHOTO_BODY_TOO_LARGE_MESSAGE` — 서버 쪽 본문 100MiB 413 응답 토스트에 씀(`PhotoError(message_key="photo_body_too_large")` · `web_errors.photo_error_handler`). 한 장 5MB 거절(같은 코드 `photo_too_large`)의 글자는 그대로 빈 값(OQ-88). 앞단 Caddy 413 은 화면(frontend)이 상태 코드로 그린다

## 테스트
- 새 `backend/tests/day/emr/test_kos_shared_token.py`(8): 두 프로세스(클라이언트 둘)가 같은 저장소 → sign-in 1회 · 계정 id 공유 / 동시 첫 호출 4개 잠금 경합 → sign-in 1회 / 401 → 한 번만 다시 받고 다른 프로세스는 새 토큰을 읽음(sign-in 없음) / 401 이 동시에 둘 → 다시 받기 1회 / 만료 10분 전 → 새로 / 저장소 고장 → 혼자 받기 / open 토큰도 공유 / **실제 Redis**: 암호문(토큰 · 계정 id 평문 없음) · TTL · 키에 값 없음
- 고침: `tests/day/board/test_board_loop3.py` — 빠진 장 요약 글자 · 서버 413 글자
- 기존 `test_kos_signin_limit.py`(해제 규칙) · `test_kos_client.py` 그대로 통과

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day` — 2208 passed · 1 failed(`test_role_structure` — 새 필드 이름 `account_id` 는 `AccountId` 타입이어야 한다는 규칙 → `staff_external_id: ExternalStaffId` 로 바꿈) → 고친 뒤 architecture + 토큰 테스트 326 passed
- ruff check · format OK · mypy Success 608 files

## 주의
- 서버 · 개발자 PC 끼리(같은 KOS 시스템 계정 · 같은 표시면)는 Redis 가 달라 여전히 서로 끊을 수 있다(규칙 8 · 실물 몫 — 표시를 환경마다 다르게).
- 잠금을 잡은 프로세스가 20초 넘게 sign-in 하면 기다리던 쪽이 혼자 받는다(sign-in 1회 더 · 드묾).
