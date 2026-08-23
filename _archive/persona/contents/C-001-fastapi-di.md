---
type: content
id: C-001
date: "2026.05.01"
day: "Day 01"
title:
  ko: "FastAPI Dependency Injection — 진짜 쓸 수 있게"
  en: "FastAPI Dependency Injection — making it usable"
summary:
  ko: "FastAPI의 Depends가 단순 import 대체가 아닌 이유와, 비동기·세션·인증을 한 번에 처리하는 패턴."
  en: "Why FastAPI's Depends is not just import-replacement, and patterns for handling async/session/auth in one flow."
youtubeId: dQw4w9WgXcQ
duration: "18:42"
speaker: kknaks
tags:
  - "#fastapi"
  - "#di"
  - "#python"
---

## 개념

FastAPI의 `Depends`는 단순 의존성 주입이 아니라 **요청-스코프 객체 lifecycle 관리**까지 포함합니다.

- 요청 시작 시 의존성 그래프 해석
- 같은 요청 안에서 같은 의존성은 한 번만 호출 (use_cache=True 기본)
- async 의존성과 sync 의존성 자동 처리

```python
async def get_db():
    async with AsyncSession(engine) as session:
        yield session
        # 응답 후 자동 close

@router.get("/items")
async def list_items(db: AsyncSession = Depends(get_db)):
    return await db.execute(select(Item))
```

## 적용 예시

- **DB 세션** — 요청마다 새 세션, 응답 후 자동 close. 트랜잭션 경계도 같이.
- **인증 토큰 검증** — `Depends(verify_token)` 한 줄로 모든 보호 라우트
- **rate limiting** — `Depends(rate_limit_check)` 으로 요청 단위 카운트
- **테스트 시 override** — `app.dependency_overrides[get_db] = lambda: mock_session` — 테스트 환경 격리

## 실수했던 것

- `Depends` 안에서 동기 함수에 `await` 박음 — TypeError. 의존성도 async/sync 일관성 필요
- `use_cache=False` 안 박고 매번 새 객체 기대 — 같은 요청 안에선 캐시됨

다른 노트로: [[python-asyncio]] 에서 async 기본기 먼저 보면 도움 됩니다.
