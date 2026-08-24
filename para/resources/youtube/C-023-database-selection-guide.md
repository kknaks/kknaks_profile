---
type: content
id: C-023
date: 2026.07.29
duration: '6:58'
speaker: 코딩애플
kind: study
youtubeId: ZVuHZ2Fjkl4
title:
  en: 'Database Selection Guide: Types, Features, and When to Use Each'
  ko: '데이터베이스 선택 가이드: 유형별 특징과 사용 시나리오 총정리'
summary:
  en: A practical breakdown of six database types and criteria for choosing the right one for your service.
  ko: Redis·관계형·그래프·도큐먼트 등 6가지 DB 유형의 핵심 특징과 실전 선택 기준을 정리한다.
tags:
- '#database'
- '#redis'
- '#mongodb'
- '#mysql'
- '#elasticsearch'
- '#nosql'
- '#backend'
---

## 요지

- Redis는 데이터를 RAM에 저장해 속도가 빠르며, 메인 DB의 자주 쓰이는 데이터를 캐싱하는 보조 DB로 주로 활용한다.
- 관계형 DB는 정규화와 트랜잭션으로 데이터 정확도를 보장하므로 금융·거래처럼 정확도가 중요한 서비스에 적합하다.
- 도큐먼트 DB는 스키마 없이 JSON 형태로 자유롭게 저장하고 분산 처리가 쉬워 대량 입출력 서비스에 유리하다.
- 그래프 DB는 노드 간 관계와 방향을 직접 저장해 SNS 친구 관계, 추천 서비스, 감염 경로 추적 등에 최적화되어 있다.
- 컬럼 패밀리 DB는 표 형식이지만 정규화 없이 컬럼을 자유롭게 추가할 수 있어 대규모 분산 쓰기에 강하다.
- 검색 인덱스 DB(Elasticsearch)는 역색인을 보관해 빠른 전문 검색·자동완성·오타 교정을 쉽게 구현할 수 있게 한다.

## 개요

데이터베이스는 서비스의 요구사항—데이터 정확도, 입출력 처리량, 관계 표현, 검색 기능—에 따라 적합한 유형이 달라진다. 잘못 선택하면 성능 병목이나 데이터 정합성 문제가 발생하고, 나중에 마이그레이션하는 비용은 훨씬 크다.

이 문서는 키밸류(Redis), 관계형(MySQL/PostgreSQL), 그래프(Neo4j), 도큐먼트(MongoDB), 컬럼 패밀리(Cassandra), 검색 인덱스(Elasticsearch) 여섯 가지 유형을 순서대로 다루며, 각 유형의 저장 방식·장단점·대표 사용 시나리오를 정리한다. 최종 목표는 "일반적인 상황에서 관계형 DB와 도큐먼트 DB 중 무엇을 선택할 것인가"라는 실용적인 기준을 갖추는 것이다.

## 배경 / 사전 지식

### RAM vs 하드디스크
RAM(메모리)은 휘발성이지만 하드디스크보다 수십~수백 배 빠르다. 데이터를 RAM에 저장하면 읽기 속도가 크게 향상되지만, 전원이 꺼지면 데이터가 사라질 수 있다.

### 정규화(Normalization)
관계형 DB에서 데이터 중복을 제거하기 위해 테이블을 여러 개로 분리하는 설계 원칙이다. 예를 들어 주문 테이블에 고객 이름을 반복 저장하는 대신, 고객 테이블을 별도로 만들고 외래 키로 참조한다.

### 트랜잭션(Transaction)
여러 DB 작업을 하나의 논리적 단위로 묶어 전부 성공하거나 전부 실패하도록 보장하는 기능이다. 계좌 이체처럼 "출금과 입금이 동시에 완료되어야 하는" 상황에서 필수적이다.

### 분산 처리(Distributed Processing)
데이터를 여러 서버(노드)에 나눠 저장·처리하는 방식이다. 처리량과 가용성을 높일 수 있지만, 노드 간 데이터 동기화가 완벽하지 않아 일시적으로 데이터가 불일치할 수 있다(정합성↓).

### JSON(JavaScript Object Notation)
키-밸류 쌍으로 데이터를 표현하는 텍스트 형식이다. `{"name": "홍길동", "age": 30}` 형태로, 도큐먼트 DB에서 데이터 저장 단위로 널리 사용된다.

## 핵심 개념

### 1. 키밸류 데이터베이스
데이터를 `키 → 값` 쌍으로 저장하는 가장 단순한 형태의 DB다. 구조가 단순해 범용 메인 DB로는 적합하지 않고 보조 용도로 활용한다.

**Redis**는 키밸류 DB 중 가장 널리 쓰이는 구현체다. 일반 키밸류 DB와 달리 데이터를 하드디스크가 아닌 RAM에 우선 저장해 읽기·쓰기 속도가 극히 빠르다. 주로 메인 DB(관계형·도큐먼트)의 자주 조회되는 데이터를 복사해 두는 **캐시(Cache)** 역할을 한다. 데이터가 필요할 때 메인 DB 대신 Redis를 먼저 조회하면 응답 속도가 크게 향상된다. 캐시 외에도 Pub/Sub 메시지 브로커, 세션 저장소 등으로도 활용된다.

### 2. 관계형 데이터베이스 (RDBMS)
데이터를 **행(Row)과 열(Column)로 구성된 테이블**에 저장한다. 엑셀 스프레드시트와 구조가 유사하며, 대량 데이터 관리에는 Oracle, MySQL, PostgreSQL 같은 DBMS를 사용한다.

핵심 특징:
- **정규화**: 데이터 중복을 제거해 저장 공간을 절약하고 업데이트 이상(Anomaly)을 방지한다. 테이블이 여러 개로 나뉘므로 조회 시 JOIN이 필요해 쿼리가 복잡해질 수 있다.
- **트랜잭션**: ACID 속성을 보장해 금융 거래처럼 데이터 정확도가 중요한 작업을 안전하게 처리한다.

"관계형"이라는 이름은 데이터 간 관계를 잘 표현한다는 의미가 아니라, 수학의 관계(Relation, 행렬) 개념에서 유래했다는 점에 주의한다.

### 3. 그래프 데이터베이스
데이터를 **노드(Node)**와 **엣지(Edge, 관계)**로 저장한다. 엣지에는 방향과 속성을 부여할 수 있어 "A가 B를 팔로우한다"처럼 방향성 있는 관계를 직접 표현하기에 최적화되어 있다. 대표 구현체는 Neo4j이며, 데이터 조회에는 Cypher Query Language를 사용한다.

관계형 DB에서도 관계 표현은 가능하지만, 복잡한 다단계 관계를 추적할 때 JOIN이 기하급수적으로 늘어난다. 그래프 DB는 이런 상황에서 훨씬 효율적이다.

### 4. 도큐먼트 데이터베이스
데이터를 **JSON(또는 BSON) 형태의 도큐먼트**로 저장한다. MongoDB, CouchDB, Firebase Firestore가 대표적이다. 도큐먼트들은 컬렉션(폴더) 단위로 관리된다.

핵심 특징:
- **스키마 유연성**: 저장할 필드를 미리 정의하지 않아도 된다. 같은 컬렉션 안에 구조가 서로 다른 도큐먼트가 공존할 수 있다.
- **정규화 없음**: 데이터를 중복 저장하는 대신 관련 데이터를 한 도큐먼트에 내장(embed)해 조회 쿼리를 단순화한다.
- **분산 처리 용이**: 처음부터 분산 환경을 고려해 설계된 경우가 많아 수평 확장이 쉽다.

단점은 분산 환경에서 노드 간 데이터 정합성이 일시적으로 깨질 수 있다는 점이다.

### 5. 컬럼 패밀리 데이터베이스
관계형 DB처럼 테이블과 행을 사용하지만, **각 행마다 자유롭게 열(Column)을 추가**할 수 있다. Cassandra, Google BigTable이 대표적이다. SQL이 아닌 자체 쿼리 언어(Cassandra의 경우 CQL)를 사용한다.

정규화를 하지 않고 분산 처리에 최적화되어 있어, 쓰기 처리량이 매우 높아야 하는 대규모 서비스에 적합하다. 시계열 데이터(IoT 센서, 로그)를 저장하고 분석하는 데도 활용된다.

### 6. 검색 인덱스 데이터베이스
Elasticsearch, Amazon CloudSearch가 대표적이다. 일반 DB로도 사용할 수 있지만 본래 목적은 **검색 인덱스 보관**이다. 메인 DB의 데이터를 동기화하면 텍스트 분석을 통해 역색인(Inverted Index)을 생성·보관한다. 검색 요청이 들어오면 이 인덱스를 활용해 빠른 전문 검색(Full-Text Search)을 수행한다. 실시간 검색어 추천, 자동완성, 오타 교정 같은 부가 기능도 쉽게 구현할 수 있다.

## 작동 원리

### Redis 캐싱 흐름
1. 클라이언트가 데이터를 요청한다.
2. 서버가 Redis(캐시)를 먼저 확인한다.
3. Redis에 데이터가 있으면(Cache Hit) 즉시 반환한다.
4. Redis에 없으면(Cache Miss) 메인 DB에서 조회한 뒤 Redis에 저장하고 반환한다.
5. 이후 동일 요청은 Redis에서 바로 처리된다.

### 관계형 DB 정규화 흐름
1. 설계 단계에서 중복 데이터를 식별한다.
2. 중복되는 데이터를 별도 테이블로 분리하고 기본 키(PK)를 부여한다.
3. 원래 테이블에는 외래 키(FK)만 남긴다.
4. 조회 시 JOIN으로 분리된 테이블의 데이터를 결합한다.

### 도큐먼트 DB 분산 저장 흐름
1. 데이터가 입력되면 샤딩(Sharding) 키를 기준으로 여러 노드에 분산 저장된다.
2. 조회 요청은 해당 샤드로 라우팅된다.
3. 노드 간 복제(Replication)로 가용성을 높인다.
4. 네트워크 분단 등 장애 상황에서는 최신 데이터가 아닐 수 있다(최종 일관성, Eventual Consistency).

### Elasticsearch 검색 인덱싱 흐름
1. 메인 DB(예: MySQL)에 데이터가 저장된다.
2. 동기화 파이프라인이 데이터를 Elasticsearch에 전달한다.
3. Elasticsearch가 텍스트를 분석해 역색인을 생성·저장한다.
4. 검색 요청이 들어오면 역색인을 통해 관련 도큐먼트를 빠르게 반환한다.
5. 오타 교정, 유사어 처리 등 부가 기능이 이 단계에서 적용된다.

## 코드 예시

### Redis 캐싱 (Python, redis-py)

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_user(user_id: int) -> dict:
    cache_key = f"user:{user_id}"

    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    user = fetch_user_from_db(user_id)  # 메인 DB 조회
    r.setex(cache_key, 300, json.dumps(user))  # TTL 300초
    return user
```

`setex`는 키를 설정하면서 만료 시간(초)을 함께 지정한다. TTL이 지나면 캐시가 자동 삭제되어 메인 DB의 최신 값을 다시 조회하게 된다.

### MySQL — 정규화 테이블 설계 및 JOIN 조회

```sql
CREATE TABLE customers (
    id    INT PRIMARY KEY AUTO_INCREMENT,
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL
);

CREATE TABLE orders (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    product     VARCHAR(200) NOT NULL,
    amount      DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 고객 이름과 주문 내역을 함께 조회
SELECT c.name, o.product, o.amount
FROM   orders o
JOIN   customers c ON o.customer_id = c.id
WHERE  c.id = 1;
```

`customer_id` 외래 키로 두 테이블을 연결한다. 고객 이름이 주문마다 중복 저장되지 않아 데이터 정합성을 유지한다.

### MongoDB — 도큐먼트 삽입 및 조회 (PyMongo)

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
users  = client["myapp"]["users"]

# 필드 구조가 달라도 같은 컬렉션에 저장 가능
users.insert_many([
    {"name": "홍길동", "age": 30},
    {"name": "김철수", "age": 25, "phone": "010-1234-5678"},
])

for user in users.find({"age": {"$gte": 25}}):
    print(user["name"])
```

두 번째 도큐먼트에 `phone` 필드가 추가되어 있지만 에러 없이 저장된다. 스키마 유연성의 핵심이다.

### Elasticsearch — 색인 및 전문 검색

```bash
# 도큐먼트 색인
curl -X POST "localhost:9200/products/_doc" \
     -H 'Content-Type: application/json' -d'{
  "name": "무선 블루투스 이어폰",
  "description": "노이즈 캔슬링 기능이 탁월한 프리미엄 이어폰"
}'

# 오타 허용 전문 검색 (fuzziness)
curl -X GET "localhost:9200/products/_search" \
     -H 'Content-Type: application/json' -d'{
  "query": {
    "match": {
      "description": { "query": "노이즈캔슬링", "fuzziness": "AUTO" }
    }
  }
}'
```

`fuzziness: "AUTO"`는 오타를 허용해 "노이즈캔슬링"(띄어쓰기 없음)으로 검색해도 관련 도큐먼트를 찾아준다.

## 함정·실수

### Redis를 메인 DB로 사용
Redis는 기본적으로 RAM 저장이라 서버 재시작 시 데이터가 유실될 수 있다. AOF/RDB 영속성 옵션을 켜도 메인 DB를 대체하도록 설계된 것이 아니다. 항상 메인 DB + 캐시 보조 구조로 사용한다.

### 도큐먼트 DB에서 무한 중첩 내장
스키마 유연성에 취해 관련 데이터를 모두 한 도큐먼트에 내장하면 MongoDB의 경우 도큐먼트 크기 16MB 제한에 걸릴 수 있다. 자주 독립적으로 조회되는 엔티티는 별도 컬렉션으로 분리하고 참조 방식을 사용한다.

### 분산 DB에서 강한 일관성을 기대
도큐먼트 DB나 컬럼 패밀리 DB를 분산 배치하면 CAP 정리에 따라 네트워크 분단 상황에서 일관성 또는 가용성 중 하나를 포기해야 한다. 금융 거래처럼 강한 일관성이 필요한 데이터는 분산 NoSQL이 아닌 관계형 DB를 사용한다.

### 그래프 DB를 범용 DB로 사용
그래프 DB는 관계 탐색에 특화되어 있지만, 단순한 CRUD 작업에는 관계형이나 도큐먼트 DB가 더 효율적이다. 관계 탐색이 핵심이 아닌 서비스에 그래프 DB를 선택하면 불필요한 복잡성만 증가한다.

### 정규화 과잉
정규화를 극단적으로 적용하면 단순 조회에도 수십 개 테이블을 JOIN해야 하는 상황이 생긴다. 읽기 성능에 영향이 크다면 의도적 역정규화(반정규화)를 검토한다.

## 베스트 프랙티스

### 선택 기준 단순화
대부분의 일반적인 서비스는 두 가지 중에서 고른다:
- **데이터 정확도가 중요하다** (금융, 거래, 재고) → 관계형 DB
- **대량 입출력이 중요하다** (소셜 피드, 로그, 실시간 데이터) → 도큐먼트 DB

### 보조 DB 조합
단일 DB로 모든 요구사항을 충족하려 하지 말고 용도에 맞게 조합한다:
- 메인 DB (관계형/도큐먼트) + Redis (캐싱/세션)
- 메인 DB + Elasticsearch (전문 검색)

### 처음부터 올바른 선택
DB 마이그레이션은 비용이 크다. 서비스 초기에 데이터 특성과 트래픽 패턴을 분석해 적합한 DB를 선택한다.

### 분산 DB 도입 전 규모 확인
도큐먼트 DB와 컬럼 패밀리 DB의 분산 처리 능력은 매력적이지만, 작은 규모의 서비스에서는 오히려 운영 복잡도가 증가한다. PostgreSQL + 적절한 인덱싱으로 수백만 건의 데이터를 처리하기에 충분한 경우가 많다.

### Elasticsearch는 보조로
Elasticsearch를 메인 데이터 저장소로 사용하지 않는다. 메인 DB와 동기화 파이프라인을 유지하고 검색 기능에만 활용한다.

## 참고

- Redis 공식 문서 (redis.io/docs) — 영속성 설정(AOF/RDB), 자료구조 유형, 캐싱 패턴 상세
- CAP 정리 (Wikipedia: CAP theorem) — 분산 DB의 일관성·가용성·파티션 내성 트레이드오프 이해
- PostgreSQL 공식 문서 (postgresql.org/docs) — 트랜잭션, 인덱스, 정규화 설계 가이드
- MongoDB 공식 문서 (mongodb.com/docs) — 스키마 설계 패턴, 샤딩, 집계 파이프라인
- Elasticsearch 공식 가이드 (elastic.co/guide) — 인덱싱·검색·집계 기능 상세
- (영상 내 명시된 추가 자료 없음)