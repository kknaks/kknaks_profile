---
type: concept
id: change-data-capture
title: CDC (Change Data Capture)
aliases:
  - CDC
  - Change Data Capture
  - binlog
  - 변경 데이터 캡처
up:
  - 2025-11-01-database_migration
tags:
  - database
  - 데이터
  - 동기화
---

# CDC (Change Data Capture)

**DB 가 이미 남기고 있는 변경 기록을 읽어 「무엇이 바뀌었는지」를 따라가는 방식.** 물어보는 것이 아니라 **흘러나오는 것을 받는다.**

## 정의

MySQL 은 복제를 위해 모든 변경을 **바이너리 로그(binlog)** 에 남긴다. CDC 는 그것을 읽는다.

```
[원본 DB]  INSERT / UPDATE / DELETE
              ↓ (binlog 에 기록)
           변경 스트림 ──────▶ [대상]  같은 변경을 적용
```

쓰려면 원본 쪽 설정이 필요하다.

```sql
SHOW VARIABLES LIKE 'log_bin';                                   -- 켜져 있어야 한다
CALL mysql.rds_set_configuration('binlog retention hours', 168);  -- 로그가 남아 있어야 한다
```

### 폴링 방식과 갈리는 지점

| | 주기적 조회 | CDC |
|---|---|---|
| 어떻게 | `SELECT ... WHERE id > 마지막` 을 반복 → [[data-pipeline]] | **로그를 구독** |
| 지연 | 주기만큼 | 거의 즉시 |
| 원본 부하 | 주기마다 질의 | 로그만 읽는다 |
| **삭제** | **못 잡는다** — 지운 행은 조회에 안 나온다 | **잡는다** — DELETE 도 로그에 있다 |
| 수정 | 추적 컬럼이 시각이어야 잡힌다 | 그대로 잡힌다 |

**삭제를 잡을 수 있다는 것이 가장 큰 차이**다 — Day17 의 Logstash 파이프라인이 남긴 구멍이 여기서 메워진다.

## 왜 중요한가

**「원본은 그대로 두고 변경만 흘려보낸다」가 여러 문제를 한꺼번에 푼다.** 애플리케이션 코드를 고치지 않아도 되고(→ [[application-event]] 처럼 발행 코드를 심을 필요가 없다), 원본에 질의를 반복해 부담을 주지도 않는다.

**그리고 쓰이는 곳이 이전만이 아니다.**

- **DB 이전** — 전체 복사 뒤 그 사이 변경을 따라붙인다 → [[database-migration]]
- **검색 색인 동기화** — 원본이 바뀌면 색인도 바뀐다 → [[elasticsearch]] · [[data-pipeline]]
- **이벤트 발행** — 데이터 변경을 메시지로 흘려보낸다 → [[message-broker]]

**셋이 같은 장치의 다른 쓰임**이라는 것을 아는 것이 이 개념의 값이다.

## 경계와 오해

- **로그가 지워지면 따라잡지 못한다** — 보관 기간(`binlog retention hours`)이 짧은데 대상이 느리면 **읽어야 할 로그가 이미 없다.** 필기가 7일로 잡은 것이 그 대비다
- **binlog 가 꺼져 있을 수 있다** — 복제를 안 쓰는 인스턴스는 기본이 꺼짐이다. **켜는 것 자체가 원본에 부하와 디스크를 더한다**
- **스키마 변경은 따로 다뤄야 한다** — 컬럼이 추가·삭제되면 대상 쪽 구조도 함께 바뀌어야 하는데, 변경 스트림만으로는 그 순서를 보장하기 어렵다 → [[database-schema]]
- **순서는 보장되지만 즉시성은 아니다** — 로그를 읽어 적용하는 데 시간이 걸리므로 **잠깐 어긋난 상태**가 정상이다. 두 곳을 동시에 읽는 코드는 그것을 견뎌야 한다 → [[transaction]]
- **원본의 트랜잭션 경계가 그대로 오지는 않는다** — 도구에 따라 변경을 행 단위로 흘려보내므로, **한 트랜잭션의 여러 변경이 나뉘어 도착**할 수 있다 → [[declarative-transaction]]
- **애플리케이션이 모르게 일어난다는 것이 장점이자 위험이다** — 코드 어디에도 「여기서 색인이 갱신된다」가 없으므로, **문제가 났을 때 볼 곳을 모른다** → [[aop]] 와 같은 종류의 대가다

## 함께 보는 개념

- [[database-migration]] — 이 장치가 쓰이는 대표 자리
- [[medallion-architecture]] — 원천의 변경을 브론즈 레이어로 흘려 넣는 자리. 실버의 증분 갱신에도 쓰인다
- [[data-pipeline]] — 주기적으로 물어보는 반대편
- [[elasticsearch]] — 색인을 원본과 맞춰야 하는 쪽
- [[message-broker]] — 변경을 사건으로 흘려보내는 쪽
- [[transaction]] — 두 저장소가 잠깐 어긋나는 이유
- [[caching]] — 사본을 두면 늘 따라오는 문제

## 출처

- [[2025-11-01-database_migration]] — 「CDC(Change Data Capture) 설정 및 동작 원리」 절과 「AWS CDC 설정」이 **실제로 켜는 절차**를 남겼다 — `SHOW VARIABLES LIKE 'log_bin'` 으로 활성화를 확인하고, `mysql.rds_show_configuration` 으로 보관 기간을 본 뒤 **`binlog retention hours` 를 168시간(7일)로** 설정한다. 「binlog retention hours 가 NULL 이 아닌 2일 이상인지 확인」이라는 조건이 **로그가 남아 있어야 따라잡을 수 있다**는 이 방식의 전제를 짚는다. 마이그레이션 단계에서 **Full Load 다음에 CDC 가 오는 순서**로 배치된 것이 이 장치의 역할을 보인다 — 전체를 한 번 복사하고, 그 뒤로는 변경만 따라간다. 다만 스키마 변경·트랜잭션 경계·지연에 대해서는 다루지 않았다
