---
type: content
id: C-018
date: 2026-05-27
duration: '19:31'
speaker: 코딩하는기술사
kind: study
youtubeId: H-jSrhvnaLY
title:
  en: Why Single-Threaded Redis Handles Hundreds of Thousands of QPS
  ko: Redis가 싱글 스레드로도 수십만 QPS를 처리하는 이유
summary:
  en: Why Redis's single-threaded architecture achieves extreme performance through in-memory design, I/O multiplexing, and optimized data structures.
  ko: 싱글 스레드 Redis가 멀티스레드 필요 없이 극단적 성능을 내는 5가지 아키텍처 설계 원리를 분석합니다.
tags:
- '#redis'
- '#architecture'
- '#ioMultiplexing'
- '#performance'
- '#inmemory'
- '#backend'
---

## 요지

- 싱글 스레드는 비효율이 아니라 의도적 설계 — 메모리·네트워크가 병목이지 CPU가 아니기 때문
- In-Memory 기반은 디스크 I/O(ms 단위)를 제거해 메모리 접근(100ns)의 수만 배 성능 향상을 제공
- I/O Multiplexing(epoll)은 단일 스레드에서 수만 클라이언트를 블로킹 없이 동시 처리 — 이벤트 루프가 준비된 소켓만 선별
- O(1) 자료구조 설계와 Skip List 활용으로 각 연산을 상수 시간에 완료 — 데이터 크기와 무관한 성능
- RESP Protocol은 길이 먼저 명시해 파싱 비용을 극소화 — 매번 문자 스캔 불필요
- Pipeline은 네트워크 왕복 시간(RTT)을 압축해 처리량 10배 이상 증가 — 단건 10만 QPS → 배치 180만 QPS

## 개요

Redis는 데이터베이스, 캐시, 메시지 브로커로 널리 사용되는 인메모리 저장소입니다. 특히 "싱글 스레드인데 초당 수십만 건(또는 수백만 건의 파이프라인)을 처리한다"는 사실은 많은 개발자들에게 역설처럼 느껴집니다. 멀티코어 서버에서 하나의 CPU 코어만 사용한다면 나머지 코어는 낭비되지 않을까요?

이 문제의 핵심은 "빠르다 = 더 많은 코어를 사용한다"는 가정이 항상 참이 아니라는 것입니다. Redis는 싱글 스레드 구조에서도 극단적 성능을 낼 수 있도록 다섯 가지 아키텍처 설계 원리를 적용했습니다. 이 교안에서는 각 원리를 깊이 있게 분석하고, 왜 Redis 개발자 안티레즈(Antirez)가 의도적으로 싱글 스레드를 선택했는지, 그리고 멀티코어 환경에서 Redis를 효율적으로 사용하는 방법까지 살펴봅니다.

## 배경 / 사전 지식

### 멀티스레드와 그에 따르는 비용

일반적으로 멀티스레드 환경에서는 여러 스레드가 공유 자원에 접근할 때 **뮤텍스(Lock)**를 사용해 동시성을 제어합니다. 이는 다음과 같은 오버헤드를 초래합니다:

- **락 경쟁(Lock Contention)**: 공유 자원을 획득하려는 스레드들이 대기하면서 처리량 저하
- **컨텍스트 스위칭**: CPU가 스레드 간 전환할 때마다 레지스터, 스택, 캐시를 저장/복원하는 비용 누적
- **캐시 일관성**: 여러 스레드가 다른 CPU 코어에서 실행될 때 L1/L2 캐시를 동기화하는 비용

### 메모리 접근 시간 (Latency) 비교

컴퓨터 시스템에서 데이터에 접근하는 시간은 저장소 위치에 따라 크게 다릅니다:

| 저장소 | 접근 시간 | 상대 속도 |
|--------|---------|---------|
| 메모리(RAM) | 50-100 ns | 1x (기준) |
| NVMe SSD | 20-200 μs | 200-4,000x 느림 |
| SATA SSD | 500 μs | 5,000-10,000x 느림 |
| HDD | 최대 10ms | 100,000x 느림 |

이 차이는 동일한 연산이라도 저장소 종류에 따라 완전히 다른 성능을 낸다는 의미입니다.

### I/O와 블로킹

일반적인 블로킹 I/O 모델에서 서버가 클라이언트 요청을 처리할 때:
1. 클라이언트 연결을 받음
2. 그 연결을 전담할 스레드를 할당
3. 요청 처리 중 I/O(디스크, 네트워크)가 발생하면 스레드는 대기
4. 다른 클라이언트는 다른 스레드가 처리

이 방식은 클라이언트 수에 비례해 스레드를 생성해야 하므로, 동시 커넥션이 많을수록 메모리 낭비가 심합니다.

### RESP 프로토콜과 텍스트 파싱

프로토콜은 클라이언트와 서버 간의 통신 규약입니다:

- **텍스트 기반 프로토콜** (일반): 구분자(쉼표, 공백 등)가 나올 때까지 문자를 하나씩 스캔해야 하므로 파싱 비용이 높음
- **길이 명시 프로토콜** (RESP): 데이터 길이를 먼저 전달하므로 버퍼를 정확히 할당하고 고정 시간에 읽을 수 있음

## 핵심 개념

### 1. In-Memory (인메모리) 저장소

**정의**: 모든 데이터를 RAM에 저장하고 모든 읽기/쓰기를 메모리에서 직접 수행하는 구조입니다.

**작동 원리**:
- Redis는 디스크 I/O를 아예 배제합니다. 모든 데이터는 메모리에만 존재합니다.
- 데이터 조회 또는 수정은 항상 100ns 단위의 메모리 접근으로 끝납니다.
- 일반 데이터베이스는 버퍼 풀이 있어도 캐시 미스 시 디스크를 읽어야 하므로 지연이 발생합니다.

**성능 영향**:
메모리 접근(100ns)과 SATA SSD(0.5ms = 500,000ns)의 차이는 **5,000배 이상**입니다. 이는 단순히 "빠르다"가 아니라 완전히 다른 차원의 성능을 의미합니다.

**데이터 안정성**:
인메모리만으로는 서버 재시작 시 모든 데이터가 손실되므로, Redis는 다음을 제공합니다:
- **RDB 스냅샷**: 특정 시점의 메모리 데이터를 디스크에 저장
- **AOF(Append-Only File) 로그**: 모든 쓰기 명령어를 디스크에 기록

### 2. I/O Multiplexing (I/O 멀티플렉싱)

**정의**: 커널의 `epoll` (Linux), `kqueue` (BSD), `IOCP` (Windows) 같은 고성능 이벤트 알림 메커니즘을 사용해 수많은 클라이언트 연결을 단일 스레드에서 처리하는 기법입니다.

**작동 원리**:
1. Redis는 모든 클라이언트 소켓을 커널에 등록합니다.
2. 커널은 수많은 소켓을 감시하면서 읽기/쓰기가 가능한 소켓을 추적합니다.
3. Redis의 이벤트 루프는 주기적으로 커널에 "준비된 소켓은 어떤 것들인가?"라고 물어봅니다.
4. 커널이 준비된 소켓 목록을 반환하면, Redis는 **그것들만** 즉시 처리합니다.

**"준비됨"의 의미**:
- **읽기 준비**: 클라이언트가 명령을 보냈으므로 소켓 버퍼에 데이터가 있음. `read()` 호출이 블로킹되지 않음.
- **쓰기 준비**: 소켓 송신 버퍼에 공간이 있으므로 `write()` 호출이 블로킹되지 않음.

**메리트**:
- 싱글 스레드가 수만 개의 동시 연결을 처리 가능
- 스레드 생성/전환 오버헤드 없음
- C10K 문제(1999년 Dan Kegel이 제기한 "10,000개 동시 연결 처리 문제")를 우아하게 해결

### 3. 자료 구조 설계 (O(1) 중심)

**정의**: Redis의 모든 기본 연산을 상수 시간 O(1)에 완료하도록 설계한 것입니다.

**핵심 자료 구조들**:

- **String**: 문자열은 단순한 메모리 버퍼. 조회, 수정 모두 O(1)
- **Hash**: 내부적으로 해시 테이블 사용. 키로 값을 조회할 때 해시값을 계산하고 해당 슬롯으로 직접 이동 → O(1)
- **List**: 이중 링크드 리스트. 양쪽 끝의 push/pop은 O(1). 중간 인덱스 접근은 O(n)이지만 일반적으로 사용하지 않음
- **Set**: 해시 테이블 기반. 멤버 추가/제거/조회 모두 O(1)
- **Sorted Set (ZSet)**: 내부적으로 **Skip List** 사용
  - Skip List는 정렬된 자료를 O(log n)에 탐색
  - 레디스 개발자는 "성능은 비슷하지만 구현이 더 단순하다"는 이유로 레드-블랙 트리 대신 Skip List 선택
  - 이는 "성능 최적화보다 단순함 우선"이라는 철학을 반영

**의미**: 데이터 크기가 커져도 연산 시간이 거의 증가하지 않습니다. 백만 개 요소든 10억 개 요소든 같은 시간에 처리됩니다.

### 4. RESP 프로토콜 (Redis Serialization Protocol)

**정의**: Redis가 클라이언트와 통신하기 위해 설계한 텍스트 기반 직렬화 프로토콜입니다.

**핵심 설계**:
일반 텍스트 프로토콜은 구분자를 찾기 위해 문자를 하나씩 스캔합니다:
```
GET,user:1,  <- 쉼표가 나올 때까지 모든 문자를 확인해야 함
```

RESP는 길이를 먼저 명시합니다:
```
$3\r\nGET\r\n$6\r\nuser:1\r\n
(3바이트 문자열 "GET", 6바이트 문자열 "user:1")
```

**파싱 효율**:
- 길이를 알면 정확히 그만큼만 읽으면 됨
- 버퍼를 미리 할당할 수 있음
- 문자 스캔 루프가 단순해짐 (매번 조건 확인 불필요)

**성능 임팩트**:
싱글 스레드가 초당 100만 건 명령을 처리하려면 각 명령의 파싱이 나노초 단위로 빨라야 합니다. RESP는 이를 가능하게 합니다.

### 5. Pipeline (파이프라인과 배치 처리)

**정의**: 여러 Redis 명령을 한 묶음으로 전송하는 기법으로, 클라이언트와 서버 간의 네트워크 왕복 시간(RTT)을 압축합니다.

**작동 원리**:
- **일반 방식**: 명령 1 전송 → 응답 1 대기 → 명령 2 전송 → 응답 2 대기 ... (N개 명령 = N번의 RTT)
- **파이프라인**: [명령 1, 명령 2, 명령 3, ...] 한 번에 전송 → 모든 응답을 한 번에 수신 (N개 명령 ≈ 1번의 RTT)

**성능 차이**:
- RTT가 1ms인 환경에서 100개 명령을 개별 전송: 100ms 이상 소요
- 동일 명령을 파이프라인으로 전송: 1ms 이내 소요
- Redis 벤치마크: 파이프라인 없음 ~10만 QPS → 파이프라인 적용 ~180만 QPS (18배 향상)

## 작동 원리

### 단계 1: 클라이언트 연결과 소켓 등록

```
[Client 1] ──┐
[Client 2] ──┤
[Client 3] ──┼─→ Redis Server (Single Thread)
[...]      ──┤
[Client N] ──┘
      ↓
커널의 epoll에 모든 소켓 등록
(커널이 수만 개 소켓 감시)
```

Redis 프로세스 시작 시, 각 클라이언트 연결을 나타내는 파일 디스크립터(FD)를 커널에 등록합니다. 이후 커널이 이 모든 FD를 감시합니다.

### 단계 2: 이벤트 루프 실행

```
while (running) {
    준비된_소켓들 = epoll_wait(...)
    // 커널로부터 읽기/쓰기 가능한 소켓 목록만 받음
    
    for (socket in 준비된_소켓들) {
        if (socket.readable) {
            데이터 = read(socket)
            파싱_및_실행(데이터)
            result = 명령_실행()
        }
        if (socket.writable) {
            write(socket, result)
        }
    }
}
```

Redis의 메인 루프는:
1. `epoll_wait()`을 호출해 준비된 소켓만 가져옴
2. 각 소켓에서 명령을 읽고 즉시 실행
3. 결과를 다시 클라이언트에 전송
4. **블로킹이 없으므로** 다른 클라이언트 처리로 즉시 이동

### 단계 3: RESP 프로토콜 파싱

```
수신 바이트: *3\r\n$3\r\nSET\r\n$4\r\nkey1\r\n$6\r\nvalue1\r\n

파싱 과정:
1. *3 읽음 → 3개 인자 기대
2. $3 읽음 → 다음 문자열은 3바이트
3. "SET" 정확히 3바이트 읽음
4. $4 읽음 → 다음 문자열은 4바이트
5. "key1" 정확히 4바이트 읽음
6. $6 읽음 → 다음 문자열은 6바이트
7. "value1" 정확히 6바이트 읽음

→ 문자 스캔 루프 없이 길이만큼 정확히 이동 (O(1) 파싱)
```

### 단계 4: O(1) 자료 구조로 명령 실행

```
명령: SET key1 value1

실행:
1. "key1"의 해시값 계산
2. 해시 테이블의 해당 슬롯으로 이동
3. 값을 메모리에 저장

모든 과정이 O(1) → 데이터 크기와 무관한 성능
```

### 단계 5: Pipeline 최적화

```
클라이언트 (3개 명령을 한 번에 보냄):
PIPE_START
SET key1 value1
SET key2 value2
GET key1
PIPE_END

Redis (한 번의 네트워크 왕복으로 처리):
1. 3개 명령 모두 수신
2. 순서대로 실행
3. 3개 결과를 한 번에 반환

→ 네트워크 왕복 시간 1/3로 감소
```

## 코드 예시

### 예시 1: Redis 기본 명령어 (한국)

```python
import redis

# Redis 클라이언트 연결
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 1. String 자료구조 (O(1) 조회/저장)
r.set('user:1:name', 'Alice')           # 메모리에 직접 저장
name = r.get('user:1:name')             # 메모리에서 직접 읽음
print(f"User name: {name}")

# 2. Hash 자료구조 (내부적으로 해시 테이블)
r.hset('user:1', mapping={
    'name': 'Alice',
    'email': 'alice@example.com',
    'age': '30'
})
# 해시값 계산 → 슬롯 이동 → 값 저장 (모두 O(1))

user_data = r.hgetall('user:1')
print(f"User data: {user_data}")

# 3. Sorted Set 자료구조 (내부적으로 Skip List)
r.zadd('leaderboard', {'Alice': 1000, 'Bob': 950, 'Charlie': 900})
# Skip List에 정렬된 순서로 저장 (O(log n))

top_players = r.zrevrange('leaderboard', 0, 2, withscores=True)
print(f"Top 3: {top_players}")
```

**의미**:
- `set()`, `get()`: O(1) - 메모리에서 직접 접근
- `hset()`, `hget()`: O(1) - 해시 테이블로 즉시 탐색
- `zadd()`, `zrange()`: O(log n) - Skip List는 O(log n)이지만 여전히 매우 빠름

### 예시 2: Pipeline 사용 (성능 향상)

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# ❌ 비효율적: 개별 명령 (각각 네트워크 왕복)
print("=== 개별 명령 ===")
for i in range(100):
    r.set(f'key:{i}', f'value:{i}')  # 100번의 네트워크 왕복
    # 총 소요 시간: 100 × RTT(1ms) = 100ms

# ✅ 효율적: Pipeline 사용 (한 번의 네트워크 왕복)
print("=== Pipeline 사용 ===")
pipe = r.pipeline()
for i in range(100):
    pipe.set(f'key:{i}', f'value:{i}')  # 메모리에만 축적
# 한 번에 전송 (execute)
pipe.execute()  # 총 소요 시간: 1 × RTT(1ms) = 1ms
# → 100배 빠름!

# ✅ Pipeline으로 읽기도 최적화
pipe = r.pipeline()
for i in range(100):
    pipe.get(f'key:{i}')
results = pipe.execute()
print(f"첫 번째 값: {results[0]}")
```

**핵심**:
- 개별 명령: `명령 전송 → 응답 대기 → 다음 명령` (네트워크 대기 시간 누적)
- Pipeline: `명령 모음 전송 → 한 번에 응답` (네트워크 대기 시간 최소화)
- 실제 벤치마크에서 파이프라인 없음 ~10만 QPS → 파이프라인 ~180만 QPS

### 예시 3: I/O Multiplexing 개념 이해

```python
# 이것은 개념 설명입니다. 실제 Redis는 C로 구현되며 epoll을 사용합니다.

import select
import socket

# 단일 이벤트 루프로 여러 클라이언트를 처리
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 6379))
server_socket.listen(5)

ready_sockets = [server_socket]

while True:
    # 커널에 등록된 모든 소켓 중 준비된 것만 반환
    # (epoll_wait와 동일한 개념, select는 더 느림)
    readable, writable, exceptional = select.select(
        ready_sockets, 
        [], 
        ready_sockets,
        timeout=1
    )
    
    for sock in readable:
        if sock is server_socket:
            # 새 클라이언트 연결
            client_socket, addr = server_socket.accept()
            ready_sockets.append(client_socket)
        else:
            # 기존 클라이언트로부터 데이터 읽음
            try:
                data = sock.recv(1024)
                if data:
                    # 명령 처리 (블로킹 없음)
                    result = process_command(data)
                    sock.send(result)
            except:
                ready_sockets.remove(sock)
                sock.close()
```

**핵심 개념**:
- 싱글 스레드가 수만 소켓을 감시
- 커널(epoll)이 "읽을 데이터 있음", "쓸 수 있음" 상태를 알려줌
- 준비된 소켓만 처리하므로 블로킹 없음
- CPU는 계속 일함 (대기 시간 최소)

## 함정·실수

### 함정 1: "싱글 스레드 = 느린 것"이라는 착각

**문제**:
> "Redis는 CPU 코어를 하나만 사용하니까 비효율적이다"

**왜 틀렸는가**:
- 성능 병목은 CPU가 아니라 메모리와 네트워크입니다.
- CPU 코어를 더 추가해도 메모리 대역폭 한계는 변하지 않습니다.
- 멀티스레드의 **락 오버헤드**가 이득보다 클 수 있습니다.
  - 예: 100나노초 Redis 연산 vs 50나노초 뮤텍스 락 오버헤드 (50% 낭비)

**해결책**:
- 멀티코어를 활용하려면 Redis 인스턴스를 여러 개 실행하세요.
- 예: 16코어 서버에 Redis 4개 인스턴스 실행 (각 4코어 할당, 데이터 샤딩)

### 함정 2: 느린 명령으로 인한 전체 시스템 영향

**문제**:
```python
# ❌ 위험: 싱글 스레드인데 오래 걸리는 명령 실행
r.keys('*')           # 모든 키를 스캔 (O(n) - 백만 개 키면 수초 소요)
r.sunion(set1, set2)  # 집합 합집합 (원소 많으면 오래 걸림)
r.lrange(list1, 0, -1) # 리스트 전체 조회 (원소 많으면 오래 걸림)
```

싱글 스레드이므로 이 명령들이 실행되는 동안 **다른 모든 클라이언트 요청이 블로킹**됩니다.

**해결책**:
```python
# ✅ 올바른 방법
# 1. O(n) 스캔은 피하거나 별도로 처리
r.keys('*')  # 대신 SCAN 사용 (카운트 제한)
for cursor, keys in r.scan_iter(match='*', count=100):
    process(keys)

# 2. 느린 연산은 백그라운드 스레드로 처리
from threading import Thread
def slow_operation():
    # Redis가 아닌 외부 작업
    pass
thread = Thread(target=slow_operation, daemon=True)
thread.start()

# 3. Redis 7.0+: IO 스레드 활성화
# redis.conf에서 io-threads 4 설정
# (명령 실행은 여전히 싱글 스레드지만, I/O는 병렬화)
```

### 함정 3: Pipeline 없이 대량 삽입

**문제**:
```python
# ❌ 느림: 1000개 삽입에 1000번 네트워크 왕복
for i in range(1000):
    r.set(f'key:{i}', f'value:{i}')
    # 각각 RTT 소요
```

**해결책**:
```python
# ✅ 빠름: 1번의 네트워크 왕복
pipe = r.pipeline(transaction=False)
for i in range(1000):
    pipe.set(f'key:{i}', f'value:{i}')
pipe.execute()
```

### 함정 4: RESP 프로토콜을 무시한 커스텀 클라이언트

**문제**:
텍스트 기반 프로토콜을 직접 구현하면서 구분자 스캔을 하는 경우:
```python
# ❌ 비효율: 매번 문자 스캔
response = "name,alice,age,30"
parts = response.split(',')  # 각 쉼표까지 전체 문자 스캔
```

**해결책**:
공식 Redis 클라이언트 라이브러리를 사용하세요. 이들은 RESP 프로토콜을 최적화해 구현했습니다.

### 함정 5: 무분별한 데이터 유형 선택

**문제**:
```python
# ❌ 비효율: Sorted Set을 인덱스 없이 사용
r.zadd('user_ids', {user_id: user_id for user_id in range(1000000)})
# 조회: O(log n)이지만, 실제로는 Hash의 O(1)이 훨씬 낫다
```

**해결책**:
```python
# ✅ 효율: 목적에 맞는 자료구조 선택
# 단순 조회: String 또는 Hash (O(1))
r.set(f'user:{user_id}:name', name)

# 순서가 필요: Sorted Set (O(log n))
r.zadd('leaderboard', {name: score})

# 멤버 여부 확인: Set (O(1))
r.sadd('active_users', user_id)
```

## 베스트 프랙티스

### 1. 멀티코어 활용: 수평 확장

**패턴**: Redis 인스턴스 여러 개 실행 + 데이터 샤딩

```python
import redis
from consistent_hash import ConsistentHashRing

# 4개 Redis 인스턴스 (8코어 서버에서 각각 다른 포트)
servers = {
    'node1': redis.Redis(host='localhost', port=6379),
    'node2': redis.Redis(host='localhost', port=6380),
    'node3': redis.Redis(host='localhost', port=6381),
    'node4': redis.Redis(host='localhost', port=6382),
}

# Consistent Hashing으로 키를 노드에 배분
ring = ConsistentHashRing(servers.keys())

def get_redis_client(key):
    """키를 기준으로 적절한 Redis 인스턴스 선택"""
    node = ring.get_node(key)
    return servers[node]

# 사용
r = get_redis_client('user:1')
r.set('user:1:name', 'Alice')

r = get_redis_client('user:2')
r.set('user:2:name', 'Bob')
```

**효과**:
- 16코어 서버 + Redis 4개 인스턴스 = 모든 코어 활용
- 처리량 선형 증가 (인스턴스당 10만 QPS × 4 = 40만 QPS)

### 2. Pipeline을 기본으로

**패턴**: 대량 작업이 필요하면 항상 Pipeline 사용

```python
def batch_write(data_dict):
    """여러 키-값 쌍을 한 번에 저장"""
    pipe = r.pipeline(transaction=False)
    for key, value in data_dict.items():
        pipe.set(key, value)
    return pipe.execute()

# 사용
batch_write({
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3',
})
```

### 3. O(n) 명령어는 주기적 백그라운드 작업으로

**패턴**: `KEYS`, `SCAN`, 집합/리스트 전체 조회는 별도 스레드/프로세스에서

```python
from threading import Thread
import time

def periodic_cleanup():
    """매 분마다 만료된 키 정리 (O(n) 작업)"""
    while True:
        time.sleep(60)
        # Redis가 아닌 곳에서 실행
        # 또는 Redis SCAN으로 분할 처리
        for cursor, keys in r.scan_iter(match='session:*', count=1000):
            # 배치 단위로 처리
            pass

thread = Thread(target=periodic_cleanup, daemon=True)
thread.start()
```

### 4. RESP Protocol의 특성을 이해하고 최적화

**최적화**:
```python
# ❌ 너무 큰 배열 파이프라인 (메모리 낭비)
pipe = r.pipeline()
for i in range(100000):  # 너무 많음
    pipe.set(f'key:{i}', f'value:{i}')
pipe.execute()

# ✅ 배치 단위로 나누기
batch_size = 1000
for batch_start in range(0, 100000, batch_size):
    pipe = r.pipeline()
    for i in range(batch_start, min(batch_start + batch_size, 100000)):
        pipe.set(f'key:{i}', f'value:{i}')
    pipe.execute()
```

### 5. Redis 7.0+: IO 스레드 활용

Redis 7.0부터 순수 I/O는 별도 스레드에서 처리 가능합니다 (명령 실행은 여전히 싱글 스레드):

```bash
# redis.conf
io-threads 4          # I/O 스레드 4개 (읽기/쓰기 병렬화)
io-threads-do-reads yes  # 읽기도 멀티스레드화
```

**효과**:
- 네트워크 I/O 대기 시간 감소
- 파싱 병렬화
- 명령 실행은 여전히 싱글 스레드 (데이터 일관성 보장)

### 6. 모니터링과 성능 측정

```python
import redis
from redis.client import RESP3

# INFO 명령으로 성능 통계 확인
info = r.info('stats')
print(f"명령/초: {info['instantaneous_ops_per_sec']}")
print(f"연결 수: {info['connected_clients']}")
print(f"메모리 사용: {info['used_memory_human']}")

# Latency Monitoring (Redis 2.8.13+)
r.config_set('latency-monitor-threshold', 10)  # 10ms 이상 명령 추적
latency = r.latency_latest()
print(f"최근 지연: {latency}")
```

## 참고

### 공식 자료
- **Redis 공식 벤치마크**: Redis는 공식적으로 초당 7만~180만 건의 처리를 선언합니다.
  - 랜덤 키 SET: 약 7만 QPS
  - 단순 키 SET: 약 18만 QPS
  - GET (파이프라인): 약 180만 QPS
  - ([redis.io/docs/about/benchmarks](https://redis.io/docs/about/benchmarks/))

- **Redis FAQ - 싱글 스레드 설계**: Antirez(Redis 개발자)가 직접 싱글 스레드 선택 이유를 설명합니다.
  - ([redis.io/docs/management/optimization/](https://redis.io/docs/management/optimization/))

### 관련 개념
- **epoll / kqueue / IOCP**: 운영체제의 고성능 이벤트 알림 메커니즘
  - Linux: epoll (매우 효율적, O(1) 성능)
  - macOS/BSD: kqueue
  - Windows: IOCP

- **Skip List**: Sorted Set 내부 구현
  - 논문: "Skip Lists: A Probabilistic Alternative to Balanced Trees" by William Pugh (1990)

- **C10K 문제**: Dan Kegel, "The C10K Problem" (1999)
  - 하나의 서버로 10,000개 동시 연결 처리의 역사와 해결책

### 실제 적용 사례
- **Node.js**: libuv + epoll을 사용한 이벤트 루프
- **Nginx**: epoll 기반의 고성능 웹 서버
- **FastAPI**: asyncio (Python의 이벤트 루프) 기반

---

**이 교안을 통해 Redis의 싱글 스레드 설계가 비효율이 아니라 **의도적이고 계산된 아키텍처 선택**임을 이해할 수 있습니다. 성능은 코어 수가 아니라 설계 철학, 자료구조 최적화, 그리고 네트워크 효율성으로 결정됩니다.**