# 중복 요청에 안전한 API 멱등성 설계

> 출처: https://www.youtube.com/watch?v=NOdZWoJ0xRk · 개발자 팀 · 10:43 · 2026-04-14

## 요지

- 멱등성은 같은 요청을 여러 번 실행해도 서버의 최종 상태가 한 번 실행했을 때와 같도록 보장하는 성질이다.
- 결제·주문 생성처럼 본래 멱등하지 않은 API에는 클라이언트가 생성한 멱등성 키를 요청 헤더에 넣고, 재시도할 때도 같은 키를 사용한다.
- 서버는 키별 처리 상태와 최종 응답을 공유 저장소에 기록하여 중복 요청에는 비즈니스 로직을 다시 실행하지 않고 기존 응답을 반환한다.
- 데이터베이스의 고유 제약 조건은 동시에 도착한 요청이 중복 데이터를 생성하지 못하게 막는 최후의 안전장치다.
- 분산 환경에서는 Redis 같은 공유 저장소와 분산 락을 사용하고, 재시도에는 지수 백오프와 지터를 적용한다.
- 멱등성 데이터의 TTL은 클라이언트가 재시도할 수 있는 최대 시간보다 길어야 한다.

## 개요

클라이언트가 요청을 보낸 뒤 응답을 받지 못했다고 해서 서버가 작업을 수행하지 않은 것은 아니다. 서버가 결제를 정상적으로 저장한 직후 네트워크가 끊기면 클라이언트는 실패로 판단해 같은 요청을 다시 보낼 수 있다. 서버가 두 요청을 구분하지 못하면 결제나 주문이 두 번 생성된다.

멱등성 설계는 이러한 불확실한 전달 환경에서도 하나의 논리적 요청이 부작용을 한 번만 일으키도록 만드는 방법이다. 핵심은 요청에 고유한 키를 부여하고, 서버가 그 키의 처리 상태와 결과를 기억하며, 동시 요청까지 원자적으로 제어하는 데 있다.

## 배경 / 사전 지식

멱등성(idempotency)은 어떤 연산을 한 번 수행한 결과와 여러 번 수행한 결과가 같은 성질이다. 엘리베이터의 5층 버튼을 반복해서 눌러도 목적지는 5층으로 유지되는 동작이 대표적인 예다. 반대로 잔액에 1만 원을 더하는 연산은 실행할 때마다 잔액이 증가하므로 멱등하지 않다.

HTTP 메서드의 멱등성은 응답 코드나 응답 본문이 항상 같다는 뜻이 아니라, 서버에 의도된 최종 효과가 같다는 뜻이다.

| 메서드 | 일반적인 성질 | 설명 |
| --- | --- | --- |
| `GET` | 멱등 | 조회를 반복해도 요청 자체가 리소스 상태를 변경하지 않는다. |
| `PUT` | 멱등 | 같은 표현으로 리소스 전체를 반복 교체하면 최종 상태가 같다. |
| `DELETE` | 멱등 | 최초 요청과 후속 요청의 상태 코드는 달라질 수 있지만 리소스가 없다는 최종 상태는 같다. |
| `POST` | 일반적으로 비멱등 | 호출할 때마다 주문이나 결제 같은 새 리소스가 생길 수 있다. |
| `PATCH` | 연산에 따라 다름 | 값을 특정 값으로 교체하면 멱등할 수 있지만, 현재 값에 금액을 더하는 변경은 멱등하지 않다. |

네트워크 통신에는 타임아웃과 응답 유실이 존재한다. 따라서 클라이언트는 요청의 실제 처리 여부를 알 수 없는 상태에 놓일 수 있으며, 재시도를 안전하게 하려면 애플리케이션 수준의 멱등성 장치가 필요하다.

## 핵심 개념

### 멱등성 키

멱등성 키는 하나의 논리적 작업을 식별하는 고유 값이다. 보통 클라이언트가 UUID를 생성하여 `Idempotency-Key` HTTP 헤더로 전달한다. 같은 작업을 재시도할 때는 반드시 같은 키를 보내야 하며, 새로운 작업에는 새 키를 사용해야 한다.

키 생성 방식에는 범용 UUID, 주문 ID와 사용자 ID를 조합한 비즈니스 키, 요청 내용을 정규화한 뒤 만든 해시가 있다. UUID는 생성이 쉽고 충돌 가능성이 낮으며, 비즈니스 키는 운영 중 요청의 의미를 파악하기 쉽다. 해시 방식은 요청 직렬화 순서나 무관한 필드 때문에 같은 의미의 요청이 다른 키가 되지 않도록 정규화 규칙을 먼저 정해야 한다.

### 처리 상태와 응답 저장

서버는 키마다 최소한 다음 정보를 저장한다.

- 처리 상태: `PROCESSING`, `SUCCEEDED`, 필요하면 `FAILED`
- 요청을 식별할 수 있는 해시
- HTTP 상태 코드와 응답 본문
- 생성 시각과 만료 시각

처리가 끝난 키로 요청이 다시 들어오면 저장한 상태 코드와 응답을 그대로 반환한다. 같은 키에 다른 요청 본문이 들어오면 기존 결과를 돌려주지 말고 충돌로 거부해야 한다. 그렇지 않으면 클라이언트의 키 재사용 오류가 숨겨질 수 있다.

### 데이터베이스 고유 제약

애플리케이션에서 먼저 키 존재 여부를 조회하는 것만으로는 동시 요청을 막을 수 없다. 두 요청이 모두 “키 없음”을 확인한 뒤 각각 삽입할 수 있기 때문이다. `idempotency_key` 열에 고유 제약을 설정하면 오직 한 요청만 레코드 생성에 성공하므로 이러한 경쟁 조건을 데이터베이스 수준에서 차단할 수 있다.

### Redis와 분산 락

서버가 여러 대라면 로컬 메모리에 저장한 키는 다른 서버에서 보이지 않는다. 모든 인스턴스가 접근할 수 있는 Redis나 데이터베이스를 공유 저장소로 사용해야 한다. Redis는 빠른 조회, TTL 기반 자동 만료, 분산 환경의 원자적 명령을 제공한다.

같은 키가 동시에 들어오는 상황에는 키별 락이나 원자적 선점 연산이 필요하다. 락에는 반드시 만료 시간을 설정하고, 락 소유자만 해제하도록 토큰을 검증해야 한다. 락 획득과 결과 저장 사이에 프로세스가 종료되는 경우도 복구할 수 있도록 처리 중 상태의 만료 및 재처리 정책을 함께 설계한다.

### 재시도 전략

일시적인 서버 오류와 타임아웃에는 보통 최대 3~5회의 제한된 재시도를 적용한다. 간격은 1초, 2초, 4초처럼 늘어나는 지수 백오프를 사용하고 무작위 지연인 지터를 더해 다수의 클라이언트가 동시에 재시도하는 현상을 완화한다.

일반적으로 요청 자체가 잘못된 `4xx` 응답은 재시도하지 않고, 일시적 실패일 가능성이 있는 `5xx`, 타임아웃, 연결 오류를 선별해 재시도한다. 단, `408`, `409`, `425`, `429`처럼 정책에 따라 재시도할 수 있는 `4xx`도 있으므로 실제 API 계약과 `Retry-After` 헤더를 기준으로 판단해야 한다.

## 작동 원리

1. 클라이언트가 논리적 작업마다 고유한 멱등성 키를 생성한다.
2. 클라이언트가 요청 본문과 `Idempotency-Key` 헤더를 서버에 전송한다.
3. 서버는 키가 없거나 형식이 잘못되었으면 요청을 거부하거나, API 정책에 따라 비멱등 요청으로 처리한다.
4. 서버는 키와 요청 해시를 공유 저장소에서 조회한다.
5. 완료된 레코드가 있으면 요청 해시가 같은지 확인한 뒤 저장된 응답을 반환한다. 해시가 다르면 동일 키의 잘못된 재사용으로 판단해 충돌 응답을 보낸다.
6. 처리 중인 레코드가 있으면 즉시 “처리 중” 응답을 보내거나, 제한된 시간 동안 기다린 뒤 결과를 다시 조회한다.
7. 키가 없으면 고유 제약이나 Redis의 `SET NX` 같은 원자적 연산으로 처리 권한을 선점한다.
8. 선점한 요청만 결제·주문 생성과 같은 비즈니스 로직을 실행한다.
9. 비즈니스 트랜잭션이 성공하면 상태 코드와 응답 본문을 키에 연결해 저장한다.
10. 서버는 저장된 결과를 클라이언트에 반환한다. 이 응답이 유실되어도 후속 재시도는 같은 결과를 받는다.
11. TTL이 지나면 멱등성 레코드를 정리한다. TTL은 최대 재시도 기간보다 길게 설정한다.

결제 처리와 멱등성 결과 저장이 서로 다른 시스템에서 수행되면 둘 중 하나만 성공하는 구간이 생길 수 있다. 가능한 경우 하나의 데이터베이스 트랜잭션으로 묶고, 외부 결제사 호출처럼 묶을 수 없는 작업은 결제사의 멱등성 키, 상태 조회, 아웃박스나 상태 머신을 조합해 복구 가능하게 만들어야 한다.

## 코드 예시

다음은 Spring Boot와 JPA를 사용한 단순화된 결제 API 예시다. 데이터베이스 고유 제약으로 동시 요청의 승자를 정하고, 완료된 요청에는 저장된 응답을 반환한다.

```java
@RestController
@RequiredArgsConstructor
public class PaymentController {
    private final PaymentService paymentService;

    @PostMapping("/payments")
    public ResponseEntity<PaymentResponse> create(
            @RequestHeader("Idempotency-Key") String idempotencyKey,
            @RequestBody PaymentRequest request) {
        return paymentService.create(idempotencyKey, request);
    }
}

@Service
@RequiredArgsConstructor
public class PaymentService {
    private final IdempotencyRepository idempotencyRepository;
    private final PaymentRepository paymentRepository;
    private final ObjectMapper objectMapper;

    @Transactional
    public ResponseEntity<PaymentResponse> create(
            String key, PaymentRequest request) {
        String requestHash = sha256(canonicalJson(request));

        var existing = idempotencyRepository.findById(key);
        if (existing.isPresent()) {
            return replay(existing.get(), requestHash);
        }

        try {
            idempotencyRepository.saveAndFlush(
                IdempotencyRecord.processing(key, requestHash)
            );
        } catch (DataIntegrityViolationException duplicate) {
            IdempotencyRecord record = idempotencyRepository.findById(key)
                .orElseThrow();
            return replay(record, requestHash);
        }

        Payment payment = paymentRepository.save(
            new Payment(request.orderId(), request.amount())
        );
        PaymentResponse response = new PaymentResponse(
            payment.getId(), "APPROVED"
        );

        IdempotencyRecord record = idempotencyRepository.findById(key)
            .orElseThrow();
        record.complete(201, toJson(response));

        return ResponseEntity.status(201).body(response);
    }

    private ResponseEntity<PaymentResponse> replay(
            IdempotencyRecord record, String requestHash) {
        if (!record.getRequestHash().equals(requestHash)) {
            throw new ResponseStatusException(
                HttpStatus.CONFLICT,
                "Idempotency-Key was reused with a different request"
            );
        }
        if (!record.isCompleted()) {
            throw new ResponseStatusException(
                HttpStatus.CONFLICT, "Request is still processing"
            );
        }
        PaymentResponse body = fromJson(
            record.getResponseBody(), PaymentResponse.class
        );
        return ResponseEntity.status(record.getStatusCode()).body(body);
    }

    // canonicalJson은 필드 순서와 숫자 표현을 고정해야 한다.
    // sha256, toJson, fromJson의 구현은 일반적인 직렬화 코드로 생략했다.
}
```

테이블에는 다음과 같은 고유 제약이 필요하다.

```sql
CREATE TABLE idempotency_record (
    idempotency_key VARCHAR(128) PRIMARY KEY,
    request_hash CHAR(64) NOT NULL,
    status VARCHAR(16) NOT NULL,
    status_code INTEGER,
    response_body TEXT,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL
);
```

이 예시에서 `saveAndFlush`는 고유 키 충돌을 비즈니스 로직 실행 전에 확인한다. 실제 구현에서는 트랜잭션이 고유 제약 예외로 실패 상태가 된 뒤 같은 트랜잭션에서 계속 조회하지 않도록, 키 선점 로직을 별도의 `REQUIRES_NEW` 트랜잭션이나 원자적 저장소 연산으로 분리하는 편이 안전하다. 또한 결제 테이블 자체에도 주문 ID 같은 비즈니스 식별자의 고유 제약을 두면 방어 계층이 하나 더 생긴다.

## 함정·실수

- 재시도할 때마다 새 키를 만들면 서버는 매번 새로운 작업으로 인식한다. 하나의 논리적 요청에는 끝까지 같은 키를 사용한다.
- 키 존재 여부를 조회한 뒤 별도로 삽입하는 코드만 사용하면 동시성 경쟁이 발생한다. 고유 제약이나 원자적 선점 연산을 반드시 둔다.
- 같은 키에 다른 요청 본문을 허용하면 잘못된 결과가 반환될 수 있다. 요청 해시를 저장해 키와 요청의 결합을 검증한다.
- 결과를 저장하기 전에 락을 해제하면 다른 요청이 비즈니스 로직을 다시 실행할 수 있다. 처리 완료 기록을 먼저 확정한 뒤 락을 해제한다.
- 락에 만료 시간이 없으면 서버 장애 후 해당 키가 영원히 처리되지 않을 수 있다. 안전한 만료 시간과 복구 정책을 둔다.
- TTL이 재시도 가능 기간보다 짧으면 늦게 도착한 재시도가 새 요청으로 처리된다. 클라이언트의 최대 재시도 창보다 긴 TTL을 사용한다.
- 모든 실패 응답을 장기간 캐시하면 일시적 장애가 복구된 뒤에도 실패만 재생할 수 있다. 성공, 확정적 비즈니스 실패, 일시적 시스템 실패를 구분해 저장 정책을 정한다.
- HTTP 메서드가 본래 멱등하다는 이유만으로 내부 구현도 안전하다고 가정하면 안 된다. 알림 발송이나 감사 로그 같은 부수 효과도 중복될 수 있다.
- Redis만 믿고 영속 결제 데이터의 제약을 생략하면 캐시 유실이나 만료 후 중복 처리가 가능하다. 핵심 비즈니스 데이터에도 고유 제약을 둔다.

## 베스트 프랙티스

- 결제, 주문, 쿠폰 사용, 포인트 지급처럼 중복 실행의 피해가 큰 API부터 멱등성 키를 적용한다.
- 키의 유효 범위, 최대 길이, TTL, 재사용 시 오류, 처리 중 응답 방식을 API 계약에 명시한다.
- 클라이언트 SDK가 키 생성과 보존, 지수 백오프, 지터, 재시도 가능 오류 판별을 담당하도록 공통화한다.
- 서버의 인터셉터나 필터로 키 검증과 응답 재생을 공통화하되, 트랜잭션 경계와 비즈니스별 중복 기준은 서비스 계층에서 명시한다.
- 멱등성 키뿐 아니라 주문 ID나 외부 거래 ID에도 데이터베이스 고유 제약을 두어 다층 방어를 구성한다.
- 저장된 응답에는 상태 코드와 본문을 함께 보관하여 재시도에도 최초 처리와 일관된 결과를 제공한다.
- 키, 요청 해시, 처리 상태, 최초·재시도 여부, 처리 시간을 로그와 메트릭으로 남긴다. 중복 차단 수와 장시간 `PROCESSING` 상태를 모니터링하면 장애를 조기에 찾을 수 있다.
- 외부 결제 API를 호출한다면 내부 요청의 멱등성 키를 외부 API의 멱등성 기능과 연결하고, 호출 결과가 불명확할 때는 무조건 재결제하지 말고 거래 상태를 먼저 조회한다.
- TTL 만료는 저장 공간 관리 수단이지 비즈니스 중복 방지의 유일한 수단이 아니다. 장기적인 중복 방지가 필요하면 영속 비즈니스 키를 별도로 유지한다.

## 참고

- 영상에서 Stripe와 PayPal의 결제 API가 `Idempotency-Key` 계열 패턴을 사용하는 사례로 언급된다.
- 영상 내 별도의 문서 URL이나 도서·논문은 명시되지 않았다.
