---
type: concept
id: pagination
title: 페이징 (Pagination)
aliases:
  - 페이징
  - pagination
  - 페이지 처리
  - LIMIT
  - OFFSET
up:
  - 2024-10-21-Day98
  - 2024-12-30-Day01
tags:
  - database
  - web
  - 설계
---

# 페이징 (Pagination)

**전체를 한 번에 안 보내고 「몇 번째부터 몇 개」씩 끊어 보내는 것.** DB 가 행 수를 제한할 수 있다는 성질 하나에서 출발한다.

## 정의

```sql
select ...
from   myapp_boards
order  by board_id desc
limit  #{rowNo}, #{length}
```

`limit 시작행, 개수` — **시작 행 번호는 0부터**다.

```
rowNo  = (pageNo - 1) * pageSize     -- 몇 번째 행부터
length = pageSize                    -- 몇 개
```

전체 개수를 알아야 **마지막 페이지 번호**가 나온다.

```java
int length    = boardService.countAll();
int pageCount = length / pageSize;
if (length % pageSize > 0) pageCount++;   // 남는 것이 있으면 한 페이지 더
```

**`order by` 가 없으면 페이징이 성립하지 않는다** — 순서가 정해져 있지 않으면 「5번째부터」가 매번 다른 행을 가리킨다.

### 계층을 지나는 모양

| 계층 | 다루는 것 |
|---|---|
| 클라이언트 | `?pageNo=2&pageSize=10` → [[request-parameter]] |
| 컨트롤러 | **값을 다듬는다** — 1보다 작으면 1로, 마지막보다 크면 마지막으로 |
| 서비스 | 페이지 번호를 **행 번호로 바꾼다** → [[service-layer]] |
| DAO·Mapper | `limit #{rowNo}, #{length}` → [[mybatis]] |

**「페이지 번호」에서 「행 번호」로 바뀌는 지점이 서비스**라는 것이 이 배치의 핵심이다 — 화면은 페이지로 말하고 DB 는 행으로 말한다.

## 왜 중요한가

**목록이 커져도 응답 크기와 시간이 일정해진다.** 만 건을 다 읽어 화면에 뿌리면 DB·네트워크·브라우저 모두가 그 부담을 지고, **데이터가 늘수록 느려진다** → [[little-law]]

그리고 **경계값이 화면 논리로 드러난다.** 「이전/다음이 있는가」·「마지막 페이지는 몇인가」는 `pageCount` 하나에서 나오므로, 그 값을 모델에 함께 담아야 화면이 그릴 수 있다 → [[spring-model]]

## 경계와 오해

- **`order by` 없는 페이징은 틀린다** — 관계형 DB 는 순서를 보장하지 않으므로, 정렬 없이 `limit` 만 쓰면 페이지 사이에 **빠지거나 겹치는 행**이 생긴다. 정렬 컬럼도 **동점이 없어야** 안전하다 → [[dql]] · [[primary-key]]
- **개수 세기와 목록 읽기는 두 번의 질의다** — 그 사이에 데이터가 바뀌면 `pageCount` 와 실제가 어긋난다. 마지막 페이지가 비어 보이는 현상이 여기서 온다
- **OFFSET 이 커지면 느려진다** — `limit 100000, 10` 은 앞의 10만 행을 **읽고 버린다.** 뒤쪽 페이지가 갈수록 느려지는 것이 그 때문이고, 큰 데이터에서는 「마지막 본 키 이후」로 읽는 방식(커서 페이징)으로 바꾼다 → [[database-index]]
- **컨트롤러의 보정이 방어의 전부다** — `pageNo < 1` 과 `pageNo > pageCount` 를 잡지 않으면 음수 OFFSET 이나 빈 화면이 나온다. 필기의 코드가 그 둘을 정확히 잡았지만, **`pageSize` 는 검사하지 않는다** — 클라이언트가 `pageSize=1000000` 을 보내면 그대로 읽는다
- **`limit` 은 표준 SQL 이 아니다** — MySQL·PostgreSQL 의 문법이고, 다른 DB 는 `OFFSET ... FETCH` 나 `ROWNUM` 을 쓴다. **DB 를 바꾸면 이 질의가 안 돈다** → [[persistence-framework]]
- **전체 개수가 필요 없는 화면도 있다** — 「더 보기」 방식은 `pageCount` 를 안 구해도 되므로 `count(*)` 한 번을 아낀다. **페이지 번호를 보여 줄 때만 드는 비용**이다

## 함께 보는 개념

- [[dql]] — `limit` 이 붙는 질의
- [[database-index]] — 정렬과 건너뛰기의 비용
- [[service-layer]] — 페이지 번호를 행 번호로 바꾸는 자리
- [[mybatis]] — 파라미터를 질의에 넣는 통로
- [[spring-model]] — 페이지 정보를 화면에 넘기는 자리
- [[request-parameter]] — 페이지 번호가 들어오는 경로
- [[little-law]] — 응답 크기를 일정하게 두는 이유
- [[polling]] — 같은 커서 방식이 실시간 조회에 쓰이는 자리

## 출처

- [[2024-12-30-Day01]] — 두 달 뒤. **이 노트가 「커서 페이징」으로만 언급하고 넘어간 방식이 실물로 나온다** — 채팅 메시지를 `/chat/messages?fromUuid=D` 로 「D 이후로 발생한 것」만 받는다. 페이지 번호가 아니라 **마지막으로 본 것의 식별자**를 보내는 형태라, 그 사이에 새 메시지가 끼어들어도 어긋나지 않는다 — 목록이 계속 늘어나는 화면에서 번호 방식이 깨지는 이유의 반대편이다 → [[polling]]
- [[2024-10-21-Day98]] — 「페이징 처리 적용하기」 절이 원리 한 줄(**「SQL DataBase 에서 쿼리문을 통해 select 할 수 있는 행의 갯수를 제한할 수 있다」**)에서 시작해 **클라이언트 → 컨트롤러 → 서비스 → DAO → Mapper 다섯 단계를 코드로 관통**한다. `limit 4,4` 가 「5번째(0부터 시작)부터 4개」라는 주석이 시작 행 번호의 기준을 못 박고, 컨트롤러가 `pageNo < 1` 과 `pageNo > pageCount` 를 보정하며 `length % pageSize > 0` 이면 `pageCount++` 하는 계산이 그대로 남아 있다. 서비스가 `(pageNo - 1) * pageSize` 로 **페이지 번호를 행 번호로 바꿔** `Map` 에 담아 넘기는 것이 계층 간 변환의 자리다. 다만 `order by` 가 없으면 안 된다는 것, OFFSET 이 커질 때의 비용, `pageSize` 의 상한은 다루지 않았다
