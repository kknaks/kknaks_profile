---
type: concept
id: elasticsearch
title: Elasticsearch (검색 엔진)
aliases:
  - Elasticsearch
  - 엘라스틱서치
  - ELK
  - 샤드
  - shard
  - Logstash
  - Kibana
up:
  - 2025-01-20-Day15
  - 2025-01-21-Day16
tags:
  - search
  - 검색엔진
  - 인프라
---

# Elasticsearch (검색 엔진)

**모든 단어를 미리 색인해 두고 그 색인만 뒤지는 검색 전용 저장소.** 관계형 DB 의 `LIKE` 검색이 느린 이유를 정면으로 푼다.

## 정의

### 검색이 세 세대를 거쳐 왔다

| 세대 | 방법 | 문제 |
|---|---|---|
| 1세대 | `LIKE '%검색어%'` | **모든 행의 모든 값**을 훑는다 → [[sql-like]] |
| 2세대 | 키워드 테이블을 만들어 조인 | 색인할 것을 **사람이 미리 정해야** 한다 (해시태그) |
| 3세대 | **모든 단어를 자동으로 색인** | 저장소가 하나 더 늘어난다 |

```sql
-- 1세대
SELECT * FROM post WHERE subject LIKE '%검색어%' OR content LIKE '%검색어%';

-- 2세대
SELECT P.* FROM postKeyword PK
  JOIN postTag PT ON PK.id = PT.postKeywordId
  JOIN post P ON P.id = PT.postId
 WHERE PK.content = '검색어';
```

**2세대의 브릿지 테이블이 하는 일을 자동화한 것**이 3세대다 → [[search-index]]

### 구조

| 이름 | 관계형 DB 로 치면 |
|---|---|
| **도큐먼트**(document) | 행(row) |
| **인덱스**(index) | 데이터베이스 |
| **샤드**(shard) | 인덱스를 쪼갠 **조각** |

```json
{ "id": "book1", "title": "해리포터와 마법사의 돌", "category": "판타지" }
```

클러스터는 **마스터 노드 하나 + 데이터 노드 여럿**이고, **인덱스는 샤드로 쪼개져 여러 노드에 흩어진다** → [[kubernetes]] 의 클러스터 구성과 같은 모양이다.

특징 넷 — RESTful API · 대용량 처리 · 실시간 검색 · 분산 처리 → [[rest-api]] · [[distributed-processing]]

### ELK 세 조각

- **Elasticsearch** — 저장하고 검색한다
- **Logstash** — 여러 곳(주로 DB)의 데이터를 **가져와 넣는다**
- **Kibana** — 들어 있는 것을 **시각화**한다

## 왜 중요한가

**검색이 저장과 다른 문제라는 것을 인정하는 순간이 이것이다.** 관계형 DB 는 「정확히 이 값인 행」을 빨리 찾도록 만들어져 있고, **문장 안에 그 낱말이 들어 있는가**는 잘하지 못한다 — 인덱스가 앞에서부터 맞는 것만 도우므로 `%검색어%` 는 인덱스를 못 쓴다 → [[database-index]] · [[sql-like]]

**그래서 저장소를 둘로 나눈다.** 원본은 DB 에, 검색용 색인은 검색 엔진에 — 그리고 **둘을 맞춰 주는 일**(Logstash 나 애플리케이션 코드)이 새로 생긴다 → [[persistence-framework]]

## 경계와 오해

- **데이터가 두 곳에 있으면 어긋난다** — DB 에는 지웠는데 색인에는 남는 식이다. **동기화가 이 구조의 항상적인 비용**이고, 「실시간 검색」도 색인이 반영된 뒤의 이야기다 → [[transaction]]
- **인덱스라는 낱말이 세 군데서 다른 뜻이다** — 관계형 DB 의 인덱스(조회 보조 구조), 엘라스틱서치의 인덱스(**데이터베이스에 해당**), 그리고 검색 색인 일반. 필기가 「관계형 DB 의 database 와 같은 개념」이라 적어 둔 것이 그 혼동을 막는다 → [[database-index]] · [[search-index]]
- **샤드 수는 나중에 바꾸기 어렵다** — 인덱스를 만들 때 정해지므로, **처음에 정한 조각 수가 오래 간다.** 나누는 단위를 미리 생각해야 하는 자리다
- **검색 엔진을 DB 로 쓰면 안 된다** — 트랜잭션도, 조인도, 정합성 보장도 그쪽의 강점이 아니다. **원본은 DB 에 두는 것**이 기본 배치다 → [[data-modeling]]
- **RESTful 이라는 것은 편의이자 위험이다** — HTTP 로 무엇이든 되므로 **열려 있으면 누구나 지울 수 있다.** 앞에 접근 제어를 두어야 한다 → [[spring-security]]
- **한국어 검색은 형태소 분석기가 있어야 한다** — 「모든 단어를 색인한다」에서 **「단어」를 무엇으로 볼지**가 언어마다 다르다. 기본 설정으로는 한국어가 제대로 안 쪼개진다

## 함께 보는 개념

- [[search-index]] — 색인이라는 구조 자체
- [[sql-like]] · [[database-index]] — 관계형 DB 로 검색할 때의 한계
- [[distributed-processing]] — 샤드로 흩어 두는 이유
- [[rest-api]] — 이 엔진을 다루는 통로
- [[container]] — docker-compose 로 띄우는 방식
- [[data-modeling]] — 원본을 어디에 둘 것인가
- [[aop]] — 같은 회차에서 응답 처리를 걷어낸 장치

## 출처

- [[2025-01-21-Day16]] — 하루 뒤. **쿼리를 눈으로 보고 코드로 옮기는 순서**가 나온다 — Kibana 를 docker-compose 로 띄우고(`ELASTICSEARCH_HOSTS` 로 엔진을 가리키고 5601 포트) **dev-tools 에서 `GET /app1_posts/_search` 에 `match` 쿼리를 직접 던져 본 뒤**, 스프링의 `PostDocs`·`PostDocRepository` 로 같은 검색을 붙인다. **MySQL 과 Elasticsearch 를 동시에 쓰는 구성**(원본은 JPA, 검색은 문서)이 이 회차에서 실물이 되는데, 둘을 맞추는 문제는 「새로운 Post 도메인을 만든다」로만 적히고 넘어간다
- [[2025-01-20-Day15]] — 「검색 알고리즘」 절이 **세 세대를 SQL 로 나란히 보여** 왜 검색 엔진이 필요한지를 설명한다 — `LIKE '%...%'` 의 전수 조회, 브릿지 테이블(`postKeyword`·`postTag`) 조인, 그리고 「모든 단어를 index 화하여 별도의 테이블에 저장」하는 방식. **2세대의 「중간 테이블을 직접 만들어야 한다」가 3세대의 자동화와 정확히 대비**된다. 구조 쪽은 도큐먼트·인덱스·샤드를 관계형 DB 의 행·데이터베이스와 짝지어 설명했고, 「하나의 인덱스가 여러 노드에 분산저장」된다는 것을 그림으로 남겼다. ELK 세 구성요소의 역할(저장·수집/변환·시각화)도 한 줄씩 갈렸다. 뒤쪽은 `docker-compose.yml` 로 띄우고 Document·Repository·Service 를 만들어 조회까지 가는 실습이다. 다만 DB 와 색인의 동기화 문제, 한국어 분석기는 다루지 않았다
