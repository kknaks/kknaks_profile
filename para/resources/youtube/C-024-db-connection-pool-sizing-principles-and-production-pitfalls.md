---
type: content
id: C-024
date: 2026.07.29
duration: '37:33'
speaker: 코딩하는기술사
kind: study
youtubeId: uhMhv8yGAyM
title:
  en: DB Connection Pool Sizing Principles and Production Pitfalls
  ko: DB 커넥션 풀 사이징 원리와 실무 함정
summary:
  en: Covers connection pool sizing from the cores×2 formula to multi-WAS distribution and long-transaction pitfalls
  ko: 물리 코어×2 공식부터 멀티 WAS 배분, 롱 트랜잭션·타임아웃 미스매치 함정까지 커넥션 풀 사이징의 핵심을 다룬다
tags:
- '#postgresql'
- '#hikaricp'
- '#connection-pool'
- '#database'
- '#backend-architecture'
- '#performance'
- '#usl'
---

## 요지

- 커넥션 수가 일정 임계를 넘으면 컨텍스트 스위칭·락 경쟁·캐시 교체 비용으로 TPS가 오히려 감소한다(USL 법칙).
- 최적 풀 사이즈의 출발점은 'DB 물리 코어 수 × 2 + 유효 스핀들 수'이며, NVMe SSD 환경에서는 사실상 '코어 × 2'다.
- 멀티 WAS 환경에서는 전체 인스턴스의 풀 사이즈 합산이 DB maxConnections를 초과하지 않도록 배분해야 한다.
- 풀 고갈의 주범은 풀 크기 부족이 아니라 트랜잭션 내 외부 호출 등으로 인한 롱 트랜잭션이다.
- HikariCP의 maxLifetime은 PgBouncer·RDS Proxy 등 중간 계층의 idle timeout보다 반드시 짧게 설정해야 한다.
- Little's Law(TPS = 활성 커넥션 ÷ 쿼리 실행 시간)로 풀 부족과 쿼리 느림을 구별하는 진단이 가능하다.

## 개요

DB 커넥션 풀 사이즈는 많은 백엔드 개발자와 아키텍트가 라이브러리 기본값이나 경험적 감으로 설정하는 경우가 많다. 그러나 잘못된 사이즈 설정은 처리량 저하, 커넥션 고갈로 인한 장애, 또는 불필요한 자원 낭비로 이어진다.

이 강의는 PostgreSQL 위키와 HikariCP 공식 문서, Oracle Real-World Performance(RWP) 팀의 권고를 근거로 삼아 커넥션 풀 사이즈를 어떻게 결정해야 하는지 그 원리와 공식을 설명한다. 나아가 멀티 WAS 환경에서의 배분 방법, 타임아웃 미스매치, 롱 트랜잭션 등 실무에서 자주 마주치는 함정과 대응법까지 다룬다. 이 강의에서 다루는 개념은 DB 커넥션 풀에만 국한되지 않으며, 스레드 풀·HTTP 클라이언트 풀 등 모든 종류의 풀 설계에 동일하게 적용된다.

## 배경 / 사전 지식

### DB 커넥션 풀이란?

DB 커넥션을 미리 생성해 두고 요청이 들어올 때마다 빌려쓰고 반납하는 자원 재사용 메커니즘이다. 커넥션을 매 요청마다 새로 만들면 TCP 핸드셰이크, SSL/TLS 협상, 인증, 백엔드 프로세스 할당 등의 비용(수ms~수십ms)이 매번 발생하기 때문에 풀로 미리 생성해 두는 것이다. PostgreSQL은 커넥션당 별도 프로세스가 생성되는 프로세스 기반 구조라 커넥션 수가 늘수록 메모리도 함께 증가한다.

### 주요 용어

| 용어 | 설명 |
|---|---|
| **maximumPoolSize** | 풀이 유지할 수 있는 커넥션 객체의 최대 수. HikariCP 기본값 10 |
| **minimumIdle** | 풀이 유지할 최소 유휴 커넥션 수. minimumIdle = maximumPoolSize로 맞추면 고정 풀 |
| **maxLifetime** | 커넥션이 풀에 존재할 수 있는 최대 수명. HikariCP 기본값 30분 |
| **connectionTimeout** | 풀에서 커넥션을 얻을 때까지 대기하는 최대 시간 |
| **TPS** | 초당 처리되는 트랜잭션 수 |
| **USL** | Universal Scalability Law. 동시 처리 단위 증가 시 처리량이 감소하는 성능 확장 모델 |
| **Little's Law** | TPS = 활성 커넥션 수 ÷ 평균 쿼리 실행 시간. 대기행렬 이론의 관계식 |
| **WAS** | Web Application Server. 여러 대를 운영하는 멀티 WAS 환경이 일반적 |
| **PgBouncer / RDS Proxy** | DB 앞단의 중간 커넥션 풀러. 실제 DB 커넥션 수를 제한하면서 WAS 요청을 처리 |
| **스핀들(Spindle)** | HDD의 물리 디스크 회전축. NVMe SSD 환경에서는 0으로 간주 |

### 선수 지식

- HTTP 요청 처리 흐름 (스레드 → DB 커넥션 → 쿼리 → 응답)
- 기본 SQL 트랜잭션 개념 (BEGIN / COMMIT / ROLLBACK)
- CPU 물리 코어와 하이퍼스레딩 논리 코어의 차이
- 기본 TPS / 응답 시간 개념

### 언어별 커넥션 풀 라이브러리 기본값

| 언어/프레임워크 | 라이브러리 | 기본 최대 풀 사이즈 |
|---|---|---|
| Java (Spring Boot 2.0+) | HikariCP | 10 |
| Node.js | node-postgres (pg) Pool | 10 |
| Python | SQLAlchemy QueuePool | 5 (+ overflow 10 = 최대 15) |
| .NET | ADO.NET 내장 풀 | 100 |

.NET의 100은 SQL Server의 maxConnections가 32,000 수준으로 여유롭고, 여유 있게 시작하는 Microsoft 진영의 철학이 반영된 것이다. 단, Microsoft 공식 가이드도 "기본값을 그대로 쓰지 말고 워크로드에 맞게 조정하라"고 명시한다. 5~15 범위에 수렴하는 다른 라이브러리들의 기본값은 기술적 근거가 있음을 시사한다.

## 핵심 개념

### 커넥션이 많아질수록 느려지는 이유 — USL 법칙

직관적으로는 "일꾼이 많으면 일이 빨리 끝난다"처럼 보이지만, DB에서는 커넥션 수가 일정 임계를 넘으면 처리량(TPS)이 오히려 감소한다. USL(Universal Scalability Law)이 이 현상을 수학적으로 설명한다. Oracle RWP 팀 문서도 *"연결 수를 줄이면 CPU 부하가 줄어 응답 속도가 빨라지고 처리량이 증가한다"*고 명시한다. HikariCP 위키 벤치마크에서는 PostgreSQL 기준 약 50 커넥션 부근부터 TPS가 평탄화된다는 결과를 보여준다.

구체적인 원인은 세 가지다:

**1. 컨텍스트 스위칭 비용 증가**
CPU 코어가 8개인데 동시에 실행 중인 스레드가 200개라면, CPU는 실제 연산 대신 스레드 교체에 시간을 소모한다. 스레드 교체 시 L1/L2 캐시도 무효화되어 메모리 접근이 추가로 발생한다.

**2. 락 경쟁 증가**
같은 테이블·행을 노리는 스레드가 많을수록 락 대기 시간이 늘어난다. 경우에 따라 처리 시간보다 대기 시간이 길어지는 역전 현상이 발생한다.

**3. 캐시 효율 저하**
많은 커넥션이 각자 다른 데이터를 읽으면 DB 버퍼 캐시가 빠르게 교체되어 캐시 미스가 증가하고, 결과적으로 디스크 I/O가 늘어난다.

**핵심 원칙**: 동시에 일하는 커넥션은 CPU가 처리할 수 있는 양만큼만 의미가 있다. 풀을 아무리 키워도 물리 자원의 처리 능력 이상으로는 처리량이 늘지 않는다.

### 풀 사이징 공식 — 코어 × 2 + 스핀들

PostgreSQL 위키에서 출발한 경험칙 공식이다:

```
최적 활성 커넥션 수 = (CPU 물리 코어 수 × 2) + 유효 스핀들 수
```

HikariCP 공식 가이드도 이 값이 다른 데이터베이스에도 대체로 적용 가능하다고 명시하며, 백엔드 진영의 표준 출발점으로 받아들여진다.

**왜 ×2인가?**
DB 쿼리는 CPU 연산과 I/O 대기를 번갈아 수행한다. I/O 대기 동안 코어가 노는 시간을 채우기 위해 커넥션 하나를 추가로 두는 것이다. ×3, ×4로 더 늘리면 컨텍스트 스위칭·캐시 무효화·스레드 내부 락 경쟁 비용이 급격히 커진다.

**왜 하이퍼스레딩(논리 코어)은 제외하는가?**
하이퍼스레딩이 만드는 논리 코어는 실제 연산 자원이 아니다. DB 작업처럼 메모리 접근이 빈번하고 캐시 미스가 많은 워크로드에서는 두 하이퍼스레딩 스레드가 같은 캐시를 두고 경쟁해 오히려 성능이 떨어질 수 있다. 8코어 16스레드 CPU라면 8만 사용한다.

**스핀들 수란?**
HDD 시대의 물리 디스크 회전축 수다. 디스크 I/O 대기 중 비어있는 CPU 자원을 추가 커넥션으로 채우기 위한 항목이다. 2026년 현재 대부분 NVMe SSD를 사용하므로 스핀들 수는 0으로 간주한다. 데이터가 메모리에 모두 캐시된 경우도 마찬가지다.

**→ 현대 환경에서의 공식: `풀 사이즈 = 물리 코어 수 × 2`**

이 값은 최종값이 아니라 **부하 테스트의 시작점**이다. PostgreSQL 위키도 "이 값은 시작값일 뿐, 실제 스위트 스폿은 부하 테스트로 찾아야 한다"고 언급한다.

Oracle RWP 그룹은 코어당 1~10개까지로 가이드하며, 이는 코어 × 2(하한)보다 넓은 범위로 환경별 유연성을 감안한 것이다.

### Little's Law를 활용한 진단

리틀의 법칙을 DB에 적용하면:

```
TPS = 활성 커넥션 수 ÷ 쿼리 실행 시간(초)
```

이 공식은 풀 크기를 정하는 공식이 아니라, **"풀이 부족한 것인지, 쿼리가 느린 것인지"를 구별하는 진단 도구**다.

- 활성 커넥션 수가 DB 코어 × 2에 근접한 상태에서 TPS가 목표에 미달 → 풀을 늘려도 USL에 의해 효과 없음. **쿼리 최적화·인덱스·캐시**가 우선.
- 활성 커넥션 수에 여유가 있고 DB 코어도 여력이 있다 → **풀 사이즈 확장** 검토.

쿼리 실행 시간을 절반으로 줄이면 TPS는 두 배가 된다. 풀 크기를 무작정 늘리기 전에 쿼리 튜닝을 먼저 검토하는 것이 원칙이다.

### 데드락 회피를 위한 최소 커넥션 수 공식

HikariCP 문서에 나오는 별도 공식이다:

```
최소 커넥션 수 = Tn × (Cm - 1) + 1
```

- Tn: 동시 스레드 수
- Cm: 한 스레드가 동시에 점유하는 최대 커넥션 수 (중첩 트랜잭션 패턴)

한 스레드가 첫 번째 커넥션을 보유한 채 두 번째 커넥션을 요청했을 때 풀이 비어있으면 영원히 대기하는 데드락이 발생한다. 이 공식은 스레드 하나라도 완전히 일을 끝낼 수 있도록 최소 한 개의 커넥션 여유를 보장한다.

일반적인 애플리케이션은 Cm=1이므로 결과가 1이 되어 실질적 의미가 없다. **이 공식은 풀 사이즈 설정용이 아니라 데드락 발생 시 진단 도구로 활용한다.**

## 작동 원리

### 커넥션 풀의 기본 동작 순서

1. 애플리케이션 시작 시 풀이 초기화되며 minimumIdle만큼 커넥션 객체를 미리 생성한다.
2. 요청이 들어오면 풀에서 사용 가능한 커넥션 객체를 가져간다(borrow).
3. DB 작업(쿼리/트랜잭션)을 수행한다.
4. 작업 완료 후 커넥션을 풀로 반납(return)한다. 커넥션을 닫는 것이 아니라 풀로 돌아간다.
5. 풀에 사용 가능한 커넥션이 없으면 connectionTimeout 동안 대기하다 타임아웃 예외를 던진다.

### 풀 사이즈 결정 프로세스

1. **시작값 계산**: `물리 코어 수 × 2` (NVMe SSD 환경 기준)
2. **부하 테스트 실행**: Gatling, k6, JMeter 등으로 목표 TPS에 도달하는지 측정
3. **메트릭 모니터링**: `hikaricp.connections.active`, `hikaricp.connections.pending` 지표를 피크 시간대에 수집
4. **스위트 스폿 탐색**: 풀 사이즈를 시작값 ±2 범위에서 단계적으로 조정하며 TPS가 꺾이는 세추레이션 포인트 식별
5. **쿼리 최적화 병행**: 활성 커넥션이 코어 한계에 도달했다면 풀 확장 대신 쿼리 튜닝 먼저

### 멀티 WAS 환경에서의 배분 원리

```
모든 WAS의 풀 사이즈 합계 < DB maxConnections × 0.8
```

DB 맥스 커넥션 100개 기준이면 시스템 예약·관리자 접속을 제외하면 실제 가용 커넥션은 약 90개이고, 여기에 안전 마진 80%를 곱하면 72개 이내로 유지해야 한다. AWS RDS 가이드도 maxConnections=500이면 풀러는 400으로 설정하라고 명시한다.

**배분 방식 선택:**
- **DB 보호 우선**: `각 WAS 풀 사이즈 = (DB 코어 × 2) ÷ WAS 수` — 총량을 엄격히 유지
- **가용성 우선**: 각 WAS에 +1~2개 여유를 두어 한 대 장애 시 나머지가 흡수 — 합산이 안전 마진 이내인지 반드시 확인

### maxLifetime과 중간 계층 idle timeout의 관계

```
HikariCP maxLifetime < 중간 계층 idle timeout - 30초 이상
```

중간 계층(PgBouncer, RDS Proxy, NLB)이 먼저 세션을 끊었는데 HikariCP 풀이 그 사실을 모르면, 이후 쿼리 시도 시 오류가 발생한다. maxLifetime이 중간 계층의 idle timeout보다 짧아야 풀이 먼저 교체하여 오류를 예방할 수 있다.

## 코드 예시

### HikariCP 설정 (Spring Boot)

```yaml
# application.yml — 8코어 DB, PgBouncer 경유 환경 예시
spring:
  datasource:
    hikari:
      maximum-pool-size: 16        # 물리 코어 8개 × 2, 시작값
      minimum-idle: 16             # 고정 풀: minIdle = maxPoolSize
      connection-timeout: 30000    # 30초 (기본값 유지 권장)
      max-lifetime: 570000         # 9분 30초 (PgBouncer 기본 10분 - 30초)
      leak-detection-threshold: 60000  # 60초: 반환 안 된 커넥션 경고 로그
```

**설정 포인트 해설:**
- `maximum-pool-size 16`: 코어 × 2 시작값. 부하 테스트 후 조정.
- `minimum-idle = maximum-pool-size`: 고정 풀로 운영해 런타임 풀 resize 오버헤드 제거.
- `max-lifetime 570000`: PgBouncer idle timeout(기본 600000ms=10분)보다 30초 짧게 설정. 기본값 1800000ms(30분)를 그대로 쓰면 PgBouncer가 먼저 끊어버린 커넥션을 풀이 재사용해 오류 발생.
- `leak-detection-threshold 60000`: 60초 이상 반납되지 않은 커넥션을 스택 트레이스와 함께 로그로 경고. 롱 트랜잭션·커넥션 누수 진단에 필수.

### Little's Law 진단 계산

```python
# 피크 시간대 측정값 기준 진단
db_cores = 8
pool_size = 16
active_connections = 14      # 피크 시간대 평균 활성 커넥션
query_time_sec = 0.05        # 평균 쿼리 실행 시간 (50ms)
measured_tps = 280           # 실측 TPS

theoretical_tps = active_connections / query_time_sec  # 280.0
utilization = active_connections / pool_size            # 0.875 (87.5%)
cores_limit = db_cores * 2                             # 16

print(f"이론 TPS: {theoretical_tps}")
print(f"풀 사용률: {utilization:.0%}")
print(f"활성 커넥션({active_connections}) vs DB 코어 한계({cores_limit})")

# 풀 사용률 87% + 코어 한계 근접 → 풀 확장보다 쿼리 최적화 우선
# 쿼리 시간 50ms → 25ms로 줄이면 TPS는 280 → 560으로 두 배
```

### 멀티 WAS 풀 배분 검증

```python
db_cores = 8
was_count = 4
db_max_connections = 100

total_ideal = db_cores * 2                                 # 16
safe_limit = (db_max_connections - 10) * 0.8              # 72 (시스템 예약 10개 제외 후 80%)

# DB 보호 우선
per_was_conservative = total_ideal // was_count            # 4
total_conservative = per_was_conservative * was_count      # 16

# 가용성 우선 (한 대 장애 흡수)
per_was_available = per_was_conservative + 2               # 6
total_available = per_was_available * was_count            # 24

print(f"DB 보호 우선: WAS당 {per_was_conservative}개, 합계 {total_conservative} < {safe_limit}: {total_conservative < safe_limit}")
print(f"가용성 우선:  WAS당 {per_was_available}개, 합계 {total_available} < {safe_limit}: {total_available < safe_limit}")
# DB 보호 우선: WAS당 4개, 합계 16 < 72: True
# 가용성 우선:  WAS당 6개, 합계 24 < 72: True
```

### 롱 트랜잭션 리팩토링

```java
// ❌ 잘못된 패턴 — 트랜잭션 안에 외부 호출 포함
@Transactional
public void processOrder(Order order) {
    orderRepo.save(order);
    paymentClient.charge(order);         // 외부 HTTP 호출이 트랜잭션 안에
    notificationService.sendEmail(order); // 이메일 발송도 트랜잭션 안에
    // 커넥션 점유 시간 = DB 저장 + HTTP 응답 대기 + 이메일 발송 시간 합산
}

// ✅ 올바른 패턴 — DB 작업만 트랜잭션으로
public void processOrder(Order order) {
    PaymentResult result = paymentClient.charge(order);  // 트랜잭션 밖에서 먼저
    saveOrderWithPayment(order, result);                 // DB 작업만 트랜잭션
    notificationService.sendEmail(order);                // 트랜잭션 밖에서
}

@Transactional
private void saveOrderWithPayment(Order order, PaymentResult result) {
    orderRepo.save(order);
    paymentRepo.save(result);
    // 커넥션 점유 시간 = DB 저장 시간만
}
```

## 함정·실수

### 1. 롱 트랜잭션 — 가장 흔한 풀 고갈 원인

트랜잭션 내부에 HTTP 외부 호출, 이메일 발송, 무거운 계산 등을 넣으면 커넥션 점유 시간이 급격히 늘어난다. 풀 사이즈가 공식대로 맞아도 몇 개의 롱 트랜잭션이 풀 전체를 고갈시킬 수 있다.

**대응**: 트랜잭션 범위를 최소화한다. 외부 호출은 트랜잭션 바깥에서 수행하고, 결과를 가지고 들어와서 DB 작업만 트랜잭션으로 묶는다. leakDetectionThreshold를 설정해 60초 이상 반납되지 않는 커넥션을 로그로 추적한다.

### 2. maxLifetime 미스매치 — 중간 계층 도입 시 빈발

HikariCP maxLifetime 기본값(30분)이 중간 계층의 idle timeout보다 길면, 중간 계층이 먼저 세션을 끊은 후 풀이 그 사실을 모르고 "죽은 커넥션"으로 쿼리를 시도해 오류가 발생한다.

| 레이어 | 기본 idle timeout |
|---|---|
| PostgreSQL | 무제한(0) |
| MySQL | 8시간 |
| PgBouncer | **10분** ← HikariCP 기본 30분과 충돌 |
| AWS NLB | 약 350초 |

PostgreSQL과 MySQL만 쓰는 환경에서는 문제가 없지만, PgBouncer나 RDS Proxy, NLB를 도입하는 순간 즉시 점검 필요. HikariCP GitHub README도 명시: *"데이터베이스나 인프라가 부과하는 커넥션 시간 제한보다 몇 초 짧게 설정하세요."*

**규칙**: `maxLifetime < 중간 계층 idle timeout - 30초`

### 3. 멀티 WAS 확장 시 WAS별 풀을 독립적으로 유지

WAS 1대에서 풀 사이즈 16이 적정했다고 해서 WAS를 4대로 늘릴 때 각각 16을 설정하면 총 64개가 되어 DB가 감당할 수 있는 양의 4배가 된다.

- **고정 풀**: 애플리케이션 시작 시 즉시 64개 커넥션을 생성하려다 DB maxConnections 초과로 파드 기동 실패.
- **동적 풀**: 트래픽 폭증 시 커넥션 수가 DB maxConnections를 넘는 순간 장애.

### 4. DB maxConnections를 무작정 올리기

PostgreSQL은 커넥션당 5~10MB 메모리를 사용하고 커넥션 수가 늘수록 컨텍스트 스위칭도 누적된다. maxConnections를 올리는 것보다 PgBouncer 같은 외부 풀러를 도입하는 것이 올바른 해결책이다.

### 5. 운영 중인 시스템의 풀 사이즈를 갑자기 줄이기

측정 없이 풀을 축소하면 트래픽 폭증 시 즉각 장애로 이어진다. 풀을 키우는 것보다 줄이는 것이 더 위험하다.

**안전한 축소 판단 기준** (피크 시간대 평균 활성 커넥션 / 현재 풀 사이즈 기준):
- 25% 이하 → 축소 검토 가능
- 25~65% → 단계적 적용, 즉시 롤백 준비
- 65% 이상 → 현재 설정 유지

### 6. Cm > 1인 코드 패턴 방치

하나의 스레드 안에서 여러 커넥션을 동시에 점유하는 중첩 트랜잭션 패턴이 있다면, 풀 크기를 키우는 것보다 코드 구조를 고치는 것이 우선이다. JTA 분산 트랜잭션이나 트랜잭션 분리로 해결한다.

## 베스트 프랙티스

**1. 시작값은 공식으로, 최적값은 부하 테스트로**
`물리 코어 × 2`를 시작점으로 삼고, 부하 테스트로 TPS가 꺾이는 세추레이션 포인트를 찾는다. 임의의 큰 값(50, 100)으로 시작하지 않는다. 부하 테스트 시 이론 TPS의 약 80%를 실제 달성 목표로 잡는 것이 현실적이다.

**2. 고정 풀로 운영하라**
`minimumIdle = maximumPoolSize`로 설정해 런타임 중 풀 크기 변동 오버헤드를 제거한다. 동적 풀은 풀 shrink/grow 과정에서 추가 비용이 발생한다.

**3. 쿼리 튜닝이 풀 확장보다 먼저다**
TPS를 올리려면 먼저 쿼리 실행 시간을 줄인다. 쿼리 시간이 절반으로 줄면 TPS는 두 배가 된다. 활성 커넥션이 이미 CPU 한계에 도달했다면 풀을 늘려도 효과가 없다.

**4. HikariCP 메트릭을 대시보드로 모니터링하라**
- `hikaricp.connections.active`: 현재 사용 중인 커넥션 수
- `hikaricp.connections.pending`: 커넥션을 대기 중인 스레드 수
- `hikaricp.connections.timeout`: 타임아웃 발생 건수

pending이나 timeout이 발생하면 풀 부족 또는 롱 트랜잭션 신호다.

**5. 대규모 WAS 환경 또는 오토스케일링 환경에서는 PgBouncer 도입을 검토하라**
WAS 인스턴스 수가 동적으로 변하면 매번 풀 사이즈를 수동 조정하기 어렵다. PgBouncer를 두면 WAS가 늘어도 DB 실제 커넥션 수를 제한할 수 있다. 단, 도입 시 maxLifetime 미스매치를 반드시 점검한다.

**6. 신규 시스템 구축 체크리스트**

- [ ] DB 물리 코어 수 확인 (하이퍼스레딩 논리 코어 제외)
- [ ] 스토리지 타입 확인 (NVMe SSD → 스핀들 0)
- [ ] WAS 인스턴스 수 확인 및 풀 배분 계산 (합산 < DB maxConnections × 0.8)
- [ ] maxLifetime vs 중간 계층 idle timeout 검토
- [ ] 트랜잭션 내 외부 호출 코드 검토 (롱 트랜잭션 제거)
- [ ] leakDetectionThreshold 설정 (60000ms 권장)
- [ ] 부하 테스트 계획 수립 (세추레이션 포인트 탐색)

**7. 운영 중 시스템은 측정 후 단계적으로 적용하라**
잘 동작하는 시스템은 건들지 말자는 것이 운영의 황금률이다. 이 가이드를 적용할 곳은 두 가지: 처리량 문제로 트러블슈팅이 필요할 때, 그리고 신규 시스템을 새로 구축할 때.

## 참고

- **PostgreSQL Wiki — Number Of Database Connections**: 풀 사이징 공식 `(cores × 2) + spindles`의 출처. 수년간 벤치마크에서 경험적으로 수렴된 공식임을 명시. (영상 댓글/설명란에 링크 예정)
- **HikariCP GitHub Wiki**: 풀 사이즈 가이드, maxLifetime 설정 권고, 50 커넥션 부근에서 TPS가 평탄화되는 PostgreSQL 벤치마크 그래프 포함. (영상 댓글/설명란에 링크 예정)
- **Oracle Real-World Performance Group 문서 — Connection Strategies for Database Applications**: CPU 코어당 평균 프로세스 수 10개 이하 권고, 연결 수 감소 시 처리량 증가 원리 설명. (영상 댓글/설명란에 링크 예정)
- 선행 강의: TPS 원리 강의 (Little's Law, 세추레이션 포인트 그래프에 대한 상세 설명은 해당 강의 참고)