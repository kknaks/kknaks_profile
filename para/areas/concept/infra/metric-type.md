---
type: concept
id: metric-type
title: 메트릭 타입 (Counter · Gauge · Histogram · Summary)
aliases:
  - 메트릭
  - metric
  - Counter
  - Gauge
  - Histogram
up:
  - 2025-07-21-Prometheus
tags:
  - 모니터링
  - 성능
---

# 메트릭 타입 (Counter · Gauge · Histogram · Summary)

**같은 숫자라도 「어떻게 읽어야 하는 숫자인가」가 타입으로 정해진다.** 타입을 잘못 고르면 그래프가 조용히 거짓을 그린다.

## 정의

| 타입 | 값의 성질 | 어떻게 읽나 | 예 |
|---|---|---|---|
| **Counter** | **늘기만 한다** (0부터 누적) | 값이 아니라 **증가율** | `http_requests_total` · `errors_total` |
| **Gauge** | **오르내린다** (현재 상태) | **지금 값** 그대로 | `cpu_usage_percent` · `active_connections` |
| **Histogram** | 관측값을 **구간(버킷)별로** 센다 | 분포 · 합계 · 개수 | `http_request_duration_seconds` |
| **Summary** | 관측값의 **분위수**를 낸다 | p95 · p99 · 합계 · 개수 | `..._seconds{quantile="0.95"}` |

**앞의 둘은 「하나의 숫자」이고 뒤의 둘은 「숫자들의 모양」이다.** 응답시간처럼 **평균이 거짓말하는** 값은 뒤쪽이 필요하다 → [[performance-testing]]

### 무엇을 기본으로 보는가

필기가 세 층으로 나눠 적어 두었다 — **층이 다르면 보는 사람도 다르다.**

| 층 | 보는 것 |
|---|---|
| **시스템** | `node_cpu_seconds_total` · `node_memory_MemAvailable_bytes` · `node_load1/5/15` · 디스크 여유 |
| **애플리케이션** | `http_requests_total` · `http_request_duration_seconds` · `http_requests_in_flight` |
| **미들웨어** | `mysql_up` · `mysql_global_status_slow_queries` · `jvm_memory_bytes_used` · `jvm_gc_collection_seconds` |

`http_requests_in_flight` 는 **지금 처리 중인 요청 수**라 [[little-law]] 의 「안에 있는 것」에 곧장 대응한다 — 처리량과 응답시간을 곱한 값이 여기 나타난다.

## 왜 중요한가

**타입은 이름표가 아니라 계산 규칙이다.** Counter 를 Gauge 처럼 그리면 **계속 우상향하는 무의미한 선**이 되고, Gauge 를 Counter 처럼 합치면 없는 값이 만들어진다. 「무엇을 재는가」보다 **「어떻게 읽는가」가 먼저 정해진다**는 것이 이 분류의 뜻이다.

**그리고 개선을 숫자로 말하게 한다.** 「빨라진 것 같다」와 「p95 가 800ms → 200ms」는 다른 문장이고, 뒤쪽만 다음 결정의 근거가 된다 → [[performance-testing]] · [[monitoring]]

## 경계와 오해

- **Counter 의 값 자체는 의미가 없다** — 프로세스가 재시작하면 **0 으로 돌아간다.** 「지금까지 몇 건」이 아니라 **「초당 몇 건 늘고 있나」**로 읽는 것이 정상이다
- **Gauge 는 순간값이라 사이를 못 본다** — 수집 주기 사이에 치솟았다 내려온 값은 **없던 일이 된다.** 최댓값이 중요하면 Gauge 로는 부족하다
- **Histogram 과 Summary 는 「분포냐 분위수냐」로만 갈리지 않는다** — 갈리는 진짜 자리는 **여러 인스턴스의 값을 합칠 수 있는가**다. 버킷(Histogram)은 서버에서 더해 전체 분포를 다시 낼 수 있고, 이미 계산돼 온 분위수(Summary)는 **평균 낼 수도 합칠 수도 없다.** 필기는 이 구별까지는 가지 않았다
- **메트릭 이름은 라이브러리마다 다르다** — 같은 JVM 메모리라도 클라이언트에 따라 `jvm_memory_bytes_used` 와 `jvm_memory_used_bytes` 로 갈린다. **대시보드를 옮길 때 이름이 안 맞아 빈 그래프가 나오는** 일이 여기서 생긴다
- **레이블을 늘리면 메트릭이 폭발한다** — 사용자 ID 같은 값을 레이블로 붙이면 조합마다 시계열이 하나씩 생긴다. **저장 비용이 카디널리티에 비례**한다 → [[monitoring]]
- **메트릭은 「무엇이」까지다** — 「왜」는 로그와 추적이 답한다. 수치가 튀는 것을 보고 원인을 아는 것은 다른 도구의 일이다

## 함께 보는 개념

- [[monitoring]] — 이 숫자들을 모아 쓰는 체계
- [[performance-testing]] — 같은 어휘로 개선을 재는 자리
- [[little-law]] — 처리 중인 요청 수가 뜻하는 것
- [[thread-state]] — JVM·스레드 메트릭이 가리키는 실체
- [[async-io]] — 워커 지표가 마르는 이유

## 출처

- [[2025-07-21-Prometheus]] — 네 타입을 **「특징 / 용도 / 예시」 세 줄로 통일해** 정리했다. 특히 Counter 를 「**단조 증가하는 누적 값(0부터 시작하여 증가만 가능)**」으로, Gauge 를 「증가/감소 모두 가능」으로 적어 **읽는 방법이 갈린다는 것**을 처음부터 붙들었다. 인프라·애플리케이션 메트릭을 표로 나눠 둔 것이 이 노트의 절반이고, `node_load1/5/15` 처럼 **같은 값을 시간 창을 달리해 보는** 관행도 함께 남았다
