# [backend] 4루프 — C35 시스템 토큰 Redis 공유 · C36 빠진 장 글자

## 읽을 것
- 결정 파일 C35 · C36
- SPEC 고침 `planner-fix-12-report.md`(mediness #960 최신)
- 로그 근거
  - 워커가 같은 프로세스에서 08:47:29 · 08:49:59 에 재로그인했다
  - API 는 08:58:55 에 로그인했다
  - 둘이 5기기 한도에서 「오래된 같은 표시 세션」을 서로 해제한다(`emr/kos/client.py` sign-in limit 갈래)

## 할 것

### C35 — 시스템 토큰 공유
- KOS 시스템 계정 토큰(내부 토큰 · open 토큰 포함)을 병원마다 Redis 에 1개 둔다. API · 워커가 같이 쓴다.
- 받기: Redis 에 있으면 그대로 쓴다. 없거나 만료 · 401 이면 Redis 잠금을 잡은 한 프로세스만 sign-in 하고, 나머지는 기다렸다 읽는다.
- 토큰 값은 로그에 찍지 않는다.
- Redis 저장 시 암호화한다. 기존 `ENCRYPTION_KEY` 방식을 따르고 TTL 을 둔다.
- 기존 해제 규칙(`SignInLimitExceeded` → 같은 표시 가장 오래된 1개)과 어긋나지 않게 한다.
- 캐시 어댑터(`adapter_for`)와의 관계를 정리한다.
- 테스트
  - 두 「프로세스」(클라이언트 둘)가 같은 Redis 로 → sign-in 1회
  - 401 → 한 번만 다시 받음
  - 잠금 경합

### C36 — 빠진 장 글자
- 빠진 장 요약 토스트 글자 = 「올리지 못한 사진이 있습니다 (JPEG · PNG, 5MB 이하만)」
- `board_messages` 상수 · 빈 값을 대체한다.

## 하지 마라
- 템플릿 · JS
- 커밋

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day`
- ruff

## 보고
- `be-loop4-report.md`
- preamble worker_done 두 채널
