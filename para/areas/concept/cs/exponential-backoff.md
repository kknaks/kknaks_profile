---
type: concept
id: exponential-backoff
title: 지수 백오프 (Exponential Backoff)
aliases:
  - 지수 백오프
  - 지수 백오프 재시도
  - 지수형 백오프
  - 백오프
  - jitter
  - 지터
up:
  - C-030-idempotency-patterns-for-safe-api-retries
tags:
  - 재시도
  - 네트워크
  - 신뢰성
  - 분산시스템
---

# 지수 백오프 (Exponential Backoff)

실패한 작업을 즉시 같은 간격으로 반복하지 않고, 시도할 때마다 대기 시간을 지수적으로 늘리는 재시도 전략이다. 무작위 지연인 지터를 함께 사용해 여러 클라이언트의 재시도 시점이 다시 겹치는 것을 막는다.

## 정의

기본 대기 시간이 `b`이고 재시도 횟수가 `n`이면 대기 시간은 보통 `b × 2ⁿ` 형태로 증가한다. 예를 들어 기본값이 1초라면 1초, 2초, 4초 순으로 기다린다.

실제 시스템에서는 대기 시간이 끝없이 커지지 않도록 상한을 두고, 전체 재시도 횟수나 총 소요 시간에도 한도를 둔다. 여기에 지터를 적용하면 계산된 범위 안에서 실제 대기 시간을 무작위로 선택한다.

```text
delay = min(maxDelay, baseDelay × 2^attempt)
actualDelay = random(0, delay)
```

재시도 여부는 횟수뿐 아니라 실패의 종류로도 제한한다. 타임아웃, 연결 오류, 일시적인 `5xx`, 정책상 재시도할 수 있는 `408`·`425`·`429` 등이 후보이며, 요청 형식이나 권한처럼 다시 보내도 바뀌지 않는 오류는 제외한다. 서버가 `Retry-After`를 주면 임의 계산보다 그 지시를 우선한다.

## 사용 예시

```java
Duration base = Duration.ofSeconds(1);
Duration cap = Duration.ofSeconds(30);
int maxRetries = 5;

for (int attempt = 0; attempt <= maxRetries; attempt++) {
    try {
        sendPaymentRequest(idempotencyKey, request);
        break;
    } catch (TransientException e) {
        if (attempt == maxRetries) throw e;

        long exponential = base.toMillis() * (1L << attempt);
        long upperBound = Math.min(exponential, cap.toMillis());
        long delay = ThreadLocalRandom.current().nextLong(upperBound + 1);
        Thread.sleep(delay);
    }
}
```

결제처럼 부작용이 있는 요청은 재시도마다 같은 멱등성 키를 사용해야 한다. 백오프는 요청이 몰리는 속도를 줄일 뿐, 작업의 중복 실행 자체를 막지는 않는다 → [[idempotency]]

## 왜 중요한가

서버가 과부하나 일시적 장애로 응답하지 못할 때 모든 클라이언트가 즉시 재시도하면 원래 요청보다 더 큰 부하가 생긴다. 고정 간격만 사용해도 같은 시점에 실패한 클라이언트가 이후에도 같은 시점에 깨어나는 동기화가 유지된다.

지수 백오프는 서버가 회복할 시간을 점차 늘리고, 지터는 클라이언트의 재시도 시점을 시간축에 흩뜨린다. 둘을 함께 사용해야 일시적 장애가 재시도 폭풍으로 확대되는 것을 줄일 수 있다.

## 경계와 오해

- **지수 백오프 ≠ 무제한 재시도** — 대기 시간을 늘려도 횟수와 총 시간을 제한하지 않으면 실패한 작업이 자원과 큐를 계속 점유한다.
- **백오프 ≠ 멱등성** — 기다렸다 다시 보내도 같은 작업이 두 번 실행될 수 있다. 부작용이 있는 요청에는 [[idempotency]]가 별도로 필요하다.
- **모든 오류가 재시도 대상은 아니다** — 입력 오류나 인증 실패처럼 같은 요청으로 회복되지 않는 실패를 반복하면 부하만 증가한다.
- **지터 없는 백오프는 동기화를 남긴다** — 동시에 실패한 클라이언트가 모두 1초, 2초, 4초 뒤에 다시 몰릴 수 있다.
- **비트 시프트를 그대로 쓰면 오버플로할 수 있다** — 큰 횟수로 지수 값을 계산하기 전에 재시도 횟수와 최대 지연을 제한한다.

## 함께 보는 개념

- [[idempotency]] — 같은 논리적 요청을 안전하게 다시 보내기 위한 조건
- [[async-io]] — 재시도 대기 동안 실행 자원을 붙잡지 않게 만드는 방식
- [[queue]] — 실패한 작업의 재예약과 지연 실행이 일어나는 자리

## 출처

- [[C-030-idempotency-patterns-for-safe-api-retries]] — 재시도를 보통 3~5회로 제한하고 1초, 2초, 4초로 간격을 늘리며 지터로 다수 클라이언트의 재시도 시점을 분산하는 전략을 설명한다.
