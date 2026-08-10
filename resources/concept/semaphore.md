---
type: concept
id: semaphore
title: 세마포어 (동시 실행 수 제한)
aliases:
  - 세마포어
  - Semaphore
  - 동시성 제어
  - 동시 요청 제한
up:
  - 2025-07-21-Sync_Async
tags:
  - 동시성
  - 성능
---

# 세마포어 (동시 실행 수 제한)

**허가증을 N 장만 두고, 받은 것만 들어가게 하는 것.** 병렬로 밀어붙이는 코드에 **상한**을 다시 붙이는 장치다.

## 정의

```python
semaphore = asyncio.Semaphore(10)      # 허가증 10장

async def fetch_company_data(company_code):
    async with semaphore:               # 한 장 받고 들어간다 (없으면 기다린다)
        return await self._fetch_single_company_async(company_code)

tasks = [fetch_company_data(c) for c in companies]
results = await asyncio.gather(*tasks, return_exceptions=True)
```

**작업은 전부 만들되 동시에 실행되는 것만 10 개로 묶는다.** 기업이 100 곳이어도 상대 API 는 열 개씩만 받는다.

```
gather 만 → ██████████████████████████ 100개 동시 발사
+ 세마포어 → ██████████ 10개씩 열 번에 나눠 통과
```

## 왜 중요한가

**병렬화는 상대를 배려하지 않는다.** `asyncio.gather` 는 있는 대로 전부 동시에 보내므로, **내 쪽이 빨라진 만큼 상대가 무너진다** — 상대 서버의 rate limit 에 막히거나, 커넥션이 모자라거나, 차단당한다 → [[async-io]]

**그리고 자원 고갈의 방향이 밖으로 향한다.** 동기 코드에서는 워커가 먼저 말라 스스로 멈췄지만, 비동기로 풀어 주면 **막아 주던 것이 사라진다.** 세마포어는 그 상한을 **일부러 다시 만드는** 것이다 → [[connection-pool-sizing-formula]]

## 경계와 오해

- **동시 개수 제한이지 속도 제한이 아니다** — 각 호출이 짧으면 **초당 요청 수는 여전히 폭발**한다. 「1초에 몇 건」을 제한하려면 다른 장치가 필요하다
- **락과 목적이 다르다** — 허가증이 하나면 결과적으로 상호배제가 되지만, 세마포어의 본래 일은 **여럿을 들여보내되 몇까지만**이다 → [[thread-local]] · [[database-lock]]
- **잡고 놓는 것을 빠뜨리면 샌다** — 예외가 나도 반드시 반납해야 한다. `async with` 를 쓰는 이유가 그것이고, 직접 acquire/release 로 쓰면 **예외 경로에서 허가증이 사라진다** → [[try-with-resources]] 와 같은 문제다
- **숫자를 정하는 근거가 있어야 한다** — 너무 작으면 병렬로 얻은 것이 도로 없어지고, 너무 크면 안 건 것과 같다. **상대의 한도와 내 커넥션 수** 중 작은 쪽이 기준이다 → [[little-law]]
- **밀어붙이는 대신 물러설 줄도 알아야 한다** — 상한을 두는 것과 실패했을 때 간격을 늘려 다시 보내는 것은 다른 장치다. 둘 다 없으면 **재시도가 상대를 더 밀어붙인다** → [[transport-layer]] 의 혼잡제어와 같은 발상이다

## 함께 보는 개념

- [[async-io]] — 이 장치가 필요해지는 이유
- [[io-bound-vs-cpu-bound]] — 무엇을 겹쳐 보낼 수 있는가
- [[connection-pool-sizing-formula]] — 같은 「상한을 정하는」 문제
- [[little-law]] — 상한과 처리량의 관계
- [[thread]] — 동시성 제어가 원래 살던 자리

## 출처

- [[2025-07-21-Sync_Async]] — 「꼭 알아야 할 3가지」의 세 번째로 **`Semaphore`: 동시 실행 수 제한**을 async/await · `asyncio.gather` 와 나란히 놓았다. 재무제표 레포지토리 코드에서 **「동시 요청 수 제한(세마포어)」** 주석과 함께 `asyncio.Semaphore(10)` 을 `async with` 로 감싸 쓰는 형태가 그대로 나오고, 바깥은 `gather(*tasks, return_exceptions=True)` 로 전부 모은다 — **전부 보내되 열 개씩**이라는 이 조합이 이 개념의 실제 쓰임이다
