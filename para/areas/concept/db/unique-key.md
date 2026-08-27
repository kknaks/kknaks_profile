---
type: concept
id: unique-key
title: 유니크 키 (Unique Key)
aliases:
  - 유니크 키
  - unique key
  - unique
  - unique 제약
  - unique constraint
  - 유일성 제약
up:
  - 2024-08-06-Day51
tags:
  - database
  - SQL
  - 제약조건
  - MySQL
---

# 유니크 키 (Unique Key)

**기본키는 아니지만 값이 겹치면 안 되는 컬럼에 거는 제약.** Day51 의 두 줄이 이유 전부다 — 「primary key 만 적용하면 다른 칼럼들의 중복을 막을 수 없다」·「primay key는 아니지만 다른 값들이 중복되면 안된느 컬럼을 지정 할 때 사용한다」. 앞 절에서 `no` 만 다른 똑같은 행이 통과한 것을 보고 **바로 이어서 나온 도구**다 → [[primary-key]]

## 정의

컬럼 목록 뒤에 `constraint 이름 unique (컬럼, ...)` 로 적는다. 컬럼이 여럿이면 **각각이 아니라 조합이 유일**하면 된다.

```sql
create table test1(
  no int,
  name varchar(20),
  age int,
  kor int,
  eng int,
  math int,
  constraint primary key(no),
  constraint test1_uk unique (name, age)
  );
```

기본키와 나란히 두고 보면 셋이 다르다.

| | `primary key` | `unique` |
|---|---|---|
| 개수 | 테이블당 하나 | **여러 개** 가능 |
| `NULL` | 허용하지 않는다 (자동 `not null`) | **허용하고, 여러 행이 가질 수 있다** → [[sql-null]] |
| 이름 | 언제나 `PRIMARY` (지어 준 이름을 버린다) | 지어 준 이름을 지킨다 (`test1_uk`) |
| 인덱스 | 만들어진다 (InnoDB 는 데이터 정렬 기준) | 만들어진다 (별도 인덱스) → [[database-index]] |

## 사용 예시

Day51 의 데이터 넷과 거절된 둘을 나란히 읽으면 **복합 unique 의 동작이 그대로 드러난다.**

```sql
insert into test1(no,name,age,kor,eng,math) values(1,'a',10,90,90,90);
insert into test1(no,name,age,kor,eng,math) values(2,'a',11,91,91,91);
insert into test1(no,name,age,kor,eng,math) values(3,'b',11,81,81,81);
insert into test1(no,name,age,kor,eng,math) values(4,'c',20,81,81,81);

/* 번호가 중복되었기 때문에 입력 거절 */
//insert into test1(no,name,age,kor,eng,math) values(4,'d',21,81,81,81);

/* 비록 번호가 중복되지 않더라도 name, age가 unique 컬럼으로 지정되었기
때문에 중복저장될 수 없다.*/
//insert into test1(no,name,age,kor,eng,math) values(5,'c',20,81,81,81);
```

**들어간 넷 중 첫째와 둘째의 `name` 이 둘 다 `'a'` 다.** `unique (name, age)` 인데도 통과하는 이유는 `age` 가 10과 11로 달라 **조합이 다르기** 때문이다. 거절된 마지막 줄은 `no` 가 새 값(5)인데도 `('c', 20)` 이 이미 있어서 막혔다.

**즉 제약 하나가 두 방향으로 답한다** — 앞의 거절은 기본키가, 뒤의 거절은 유니크 키가 냈다. 「번호는 새것인데 왜 거절되나」의 답이 여기 있다.

## 왜 중요한가

**「먼저 조회해서 없으면 넣는다」는 유일성을 보장하지 못한다.** 애플리케이션이 `select` 로 중복을 확인하고 `insert` 하는 사이에 다른 흐름이 같은 값을 넣을 수 있고, **둘 다 「없다」를 보고 둘 다 넣는다.** 이 문제는 전날 배운 쓰레드에서 이미 나왔던 형태다 — 검사와 쓰기가 갈라져 있으면 그 틈이 위험해진다. **유일성은 값을 쓰는 그 순간에 원자적으로 검사되어야 하고, 그렇게 할 수 있는 곳은 값을 소유한 DB 하나**다 → [[thread]]

**그래서 등록 실패가 정상 경로가 된다.** 제약을 DB 에 걸면 중복 등록은 `if` 로 걸러지지 않고 **오류로 돌아온다**(MySQL 1062 `Duplicate entry`). 애플리케이션은 그 오류를 잡아 「이미 사용 중인 이메일입니다」로 바꿔야 하고, **예외 처리가 검증 로직의 일부가 된다** → [[exception-handling]]

**그리고 조회가 함께 빨라진다.** 유니크 제약은 인덱스로 구현되므로 `where email = ?` 이 훑지 않는다. **제약을 걸었더니 성능이 따라온 것**인데, 반대로 「빠르게 하려고」 유니크를 거는 것은 순서가 틀렸다 — 뜻이 유일하지 않은 컬럼에 유니크를 걸면 정상적인 데이터가 거절된다 → [[database-index]]

## 경계와 오해

- **복합 unique ≠ 각 컬럼 unique** — `unique (name, age)` 는 **조합**만 막는다. 「이름도 유일, 나이도 유일」을 원했다면 제약을 두 개 걸어야 한다. Day51 의 데이터에 `'a'` 가 두 번 들어간 것이 이 차이의 증거이고, **필기의 의도(동명이인 구분)와 문법의 동작이 일치한 드문 예**다.
- **컬럼 순서가 뜻은 같고 성능은 다르다** — `unique (name, age)` 와 `unique (age, name)` 은 **막는 조합이 완전히 같다.** 다만 만들어지는 인덱스는 앞 컬럼부터 정렬되므로, `where name = 'a'` 만으로 찾을 때 쓸 수 있는 것은 앞에 `name` 이 있는 쪽뿐이다 → [[database-index]]
- **`NULL` 은 중복으로 보지 않는다** — MySQL 에서 유니크 컬럼에 `NULL` 은 **여러 행이 가질 수 있다.** `NULL` 이 「모른다」이므로 두 `NULL` 이 같은 값인지 알 수 없다는 논리다. 「이메일은 유일해야 한다」에 `unique` 만 걸고 `not null` 을 빼면 **이메일 없는 행이 무한히 들어온다** → [[sql-null]]
- **collation 이 중복 판정을 바꾼다** — Day51 이 데이터베이스를 만들 때 고른 `utf8_general_ci` 는 대소문자를 구분하지 않으므로 `'Kim'` 을 넣은 뒤 `'kim'` 을 넣으면 **중복으로 거절된다.** 문자열의 유일성은 제약이 아니라 **비교 규칙**이 정하고, 그래서 서버 설정이 다르면 같은 `insert` 가 한쪽에서만 통한다. 자바에서 `equals` 와 `equalsIgnoreCase` 를 고르던 결정이 여기서는 **테이블을 만들 때 이미 끝나 있다** → [[database-schema]] · [[string-comparison]]
- **제약 이름을 지어 주는 것이 값을 갖는다** — Day51 은 `test1_uk` 로 이름을 줬다. 생략하면 MySQL 이 컬럼명으로 이름을 만들고, 나중에 지우거나 오류 메시지에서 「어느 제약이 걸렸는지」를 읽을 때 그 이름이 필요하다. **오류 메시지가 사용자에게 보여 줄 문구를 고르는 열쇠가 제약 이름**이 되는 경우가 많다.
- **유니크는 「중복 데이터가 없다」를 뜻하지 않는다** — 지정한 컬럼만 본다. Day51 의 테이블에서 `kor`·`eng`·`math` 가 똑같은 행은 얼마든지 들어가고, 앞 절에서 문제로 적은 「데이터의 중복성」은 **어느 컬럼 조합을 골랐는가만큼만 해결된다.** 무엇이 「같은 데이터」인지를 정하는 일은 여전히 설계자의 몫이다 → [[object-equality]]
- **`alter table ... add constraint unique` 는 기존 데이터에 걸려 실패할 수 있다** — 운영 중인 테이블에 유니크를 더하는 순간 **이미 들어 있는 중복이 드러난다.** 「제약을 나중에 걸면 된다」가 실제로는 「중복을 먼저 청소해야 한다」인 자리다 → [[ddl]]

## 함께 보는 개념

- [[primary-key]] — 이 제약이 보완하는 것
- [[sql-null]] — 유니크가 `NULL` 을 예외로 두는 자리
- [[database-index]] — 유니크 제약의 실제 구현
- [[database-schema]] · [[string-comparison]] — 문자열 중복 판정을 정하는 collation
- [[thread]] — 「검사한 뒤 넣기」가 깨지는 이유
- [[exception-handling]] — 중복 등록이 오류로 돌아오는 자리
- [[object-equality]] — 「같은 데이터」를 무엇으로 정하는가
- [[ddl]] — 제약을 나중에 더하는 명령
- [[crud]] — 등록 화면이 중복 안내를 내보내는 지점

## 출처

- [[2024-08-06-Day51]] — 「primary key 만 적용하면 다른 칼럼들의 중복을 막을 수 없다」를 이유로 `constraint test1_uk unique (name, age)` 를 걸고, 네 행을 넣은 뒤 **번호가 중복된 경우와 번호는 새것인데 `(name, age)` 가 중복된 경우** 두 가지 거절을 주석으로 구분해 남겼다. 들어간 데이터에 `name = 'a'` 가 두 번 있는 것이 복합 유니크가 조합만 본다는 증거다. 제약에 `test1_uk` 라는 이름을 지어 준 형태와, `alter table ... add constraint 키이름 unique(컬럼명)` 로 나중에 더하는 문법도 함께 적었다
