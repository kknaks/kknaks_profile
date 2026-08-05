---
type: concept
id: sql-null
title: SQL 의 NULL 과 DEFAULT (테이블 옵션)
aliases:
  - SQL NULL
  - NOT NULL
  - not null 제약
  - DEFAULT 옵션
  - default 제약
  - 널 허용
  - nullable
  - is null
  - is not null
up:
  - 2024-08-06-Day51
  - 2024-08-07-Day52
tags:
  - database
  - SQL
  - 제약조건
  - MySQL
---

# SQL 의 NULL 과 DEFAULT (테이블 옵션)

**컬럼마다 「값이 없는 것을 허용하는가」와 「값을 안 주면 무엇이 들어가는가」를 따로 정한다.** [[ddl]] 의 컬럼 정의 `컬럼명 타입 NULL여부 옵션` 에서 뒤의 두 자리가 이것이고, Day51 은 이 절을 「테이블 옵션」이라 불렀다. **`NULL` 은 「0」이나 「빈 문자열」이 아니라 「값이 없다」는 표시 자체**다.

## 정의

세 가지 상태가 있고, Day51 이 실험으로 셋을 다 지나간다.

| 적는 것 | 값을 생략하면 | `null` 을 명시하면 |
|---|---|---|
| (아무것도 안 적음) | `NULL` 이 들어간다 | `NULL` 이 들어간다 |
| `not null` | **오류** (기본값이 없으면) | **오류** |
| `default 'noname'` | `'noname'` 이 들어간다 | **`NULL` 이 들어간다** |

**마지막 칸이 이 개념의 핵심이고 Day51 이 직접 확인한 것**이다 — 필기의 문장이 「default 옵션은 입력값을 **생략**하면 자동으로 지정되는 값이다」·「값을 입력시에 null로 입력값을 주면 NULL값이 들어간다」다.

즉 **`DEFAULT` 는 「빈 값을 채워 주는 장치」가 아니라 「생략을 해석하는 규칙」**이다. `null` 을 적어 보낸 것은 생략이 아니라 **「없다고 적은 것」**이라 기본값이 끼어들지 않는다.

## 사용 예시

Day51 은 옵션이 없는 테이블부터 만들어 **무엇이든 들어가는 것**을 확인한다.

```sql
create table test1 (
no int,
name varchar(20)
);

insert into test1(no, name) values(1, 'aaa');
insert into test1(no, name) values(null, 'bbb');
insert into test1(no, name) values(3, null);
insert into test1(no, name) values(null, null);
select * from test1;
```

**네 줄이 다 통과한다** — 번호가 없는 행, 이름이 없는 행, 둘 다 없는 행이 나란히 저장된다. 「번호 없는 회원」이 저장될 수 있다는 것이 다음 절(`not null` → `primary key`)로 가는 이유다.

그다음 셋을 한 테이블에 섞는다.

```sql
create table test1(
no int not null,
name varchar(20) default 'noname',
age int default 20
);

insert into test1(no, name, age) values(1, 'aaa', 30);
-- 컬럼 값을 null로 지정하면 기본 값이 사용되지 않는다.
insert into test1(no, age, name) values(6, null, null);

-- 값을 입력하지 않는 컬럼은 이름과 값 지정을 생략한다.
insert into test1(name, age) values('aaa', 30); /* 오류! no는 not null*/

-- 컬럼에 default 값이 설정된 경우, 컬럼 값의 입력을 생략하면 기본값이 사용된다.
insert into test1(no) values(5);
```

**마지막 줄 하나에 세 규칙이 다 들어 있다** — `no` 는 적었으니 5, `name` 은 생략했으니 `'noname'`, `age` 는 생략했으니 20 이다. 그리고 **두 번째 줄과 마지막 줄이 짝**이다: 같은 컬럼에 `null` 을 적으면 `NULL`, 아예 안 적으면 기본값이다.

### 하루 뒤 — 조회하는 쪽의 문법이 온다

Day51 이 `NULL` 을 **넣는** 규칙이었다면 Day52 는 **찾는** 문법이다. 연산자 절에 별도 항목으로 서 있다 — 「null 조건 검색은 is null/ is not null(not ~ is null)로 지정한다」.

```sql
//is null
select * from 테이블명 where 컬럼명 is null;

//is not null
select * from 테이블명 where 컬럼명 is not null;
select * from 테이블명 where not 컬럼명 is null;
```

**`=` 가 아니라 `is` 인 것이 이 문법의 전부이고, 그것이 우연이 아니다** — `NULL` 은 값이 아니라 「값이 없다」는 표시라서 비교 연산자로 맞출 대상이 없다. Day52 가 `NULL` 검사를 사칙·비교 연산자와 **다른 항목으로 떼어 적은 것**이 그 성격을 반영한다 → [[sql-operator]] · [[dql]]

## 왜 중요한가

**`NULL` 은 비교를 통과하지 못한다.** `where age = null` 은 참이 되지 않고 `where age is null` 을 써야 한다 — 하루 뒤 Day52 가 배우는 문법이 바로 그것이다. `NULL` 이 「모른다」를 뜻하므로 `모른다 = 20` 의 답도 「모른다」이고, 참이 아니면 그 행은 결과에서 빠진다. **`where age <> 20` 으로 「20 아닌 사람」을 찾으면 나이를 모르는 사람은 나오지 않는다** — 조건을 아무리 뒤집어도 `NULL` 행은 양쪽 어디에도 안 걸린다.

**그래서 집계가 조용히 달라진다.** `count(*)` 는 행을 세지만 `count(age)` 는 **`NULL` 을 빼고** 세고, `avg(age)` 의 분모도 그만큼 줄어든다. 「평균 나이」가 실제와 다르게 나오는데 오류는 없다 — **`NULL` 을 허용한 컬럼은 그 뒤 모든 통계에 조건을 하나 붙인다.**

**`not null` 을 걸어 두면 애플리케이션의 `if` 하나가 사라진다.** 자바 쪽에서 「빈 값인지 검사하고 거절」하던 코드가 서버로 옮겨 가고, 어느 프로그램이 접속해도 같은 규칙이 걸린다. 반대로 걸어 두지 않으면 **읽는 쪽 모두가 `null` 검사를 해야 한다** — 한 컬럼의 선택이 그 컬럼을 읽는 모든 코드로 퍼진다 → [[object-reference]]

## 경계와 오해

- **`NULL` ≠ `0` ≠ `''`** — 셋이 다 「비었다」로 읽히지만 저장·비교·집계가 전부 다르다. `0` 과 `''` 는 **값이라서** `= 0`·`= ''` 로 찾히고 `count()` 에 세어지지만 `NULL` 은 아니다. 나이를 「모른다」와 「0살」로 구분해야 하는 순간 이 차이가 데이터의 뜻을 정한다.
- **`where 컬럼명 = null` 은 오류가 아니라 0행이다** — 문법이 맞으니 서버가 받아 주고, 조건이 언제나 `NULL`(참이 아님)이라 **아무 행도 나오지 않는다.** 「결과가 비었다」를 「그런 데이터가 없다」로 읽으면 실제로 `NULL` 행이 있는데도 없다고 판단하게 된다 — **틀린 조건이 빈 결과로만 나타나는 것**이 이 개념에서 가장 조용한 실패다. 값이 `NULL` 일 수도 있는 비교를 그대로 하고 싶으면 NULL 안전 등호 `<=>` 가 있고, `컬럼명 <=> null` 은 `is null` 과 같은 결과다. Day52 가 `NULL` 검사를 비교연산자와 **다른 항목으로 떼어 적은 것**이 이 차이를 반영한다 → [[sql-operator]]
- **Day51 의 「`not null` 이면 insert 시 컬럼을 생략할 수 없다」는 반쪽이다** — 정확히는 **「값이 정해지지 않은 채로 남을 수 없다」**다. `not null default 0` 처럼 기본값을 함께 주면 `not null` 컬럼도 생략할 수 있고 기본값이 채워진다. 두 옵션이 서로 배타적인 것으로 읽히면 `auto_increment` 컬럼(항상 `not null` 이면서 언제나 생략해서 넣는다)이 설명되지 않는다 → [[surrogate-key]]
- **그 「오류!」는 설정에 딸려 있다** — 필기가 `insert into test1(name, age) values('aaa', 30);` 에 「오류! no는 not null」이라 적은 것은 MySQL 이 **엄격 모드**(`STRICT_TRANS_TABLES`, 5.7 부터 기본값)일 때의 동작이다. 엄격 모드가 아니면 같은 문장이 **경고만 내고 `no` 에 `0` 을 넣는다.** 「제약을 걸었으니 안전하다」가 서버 설정 하나에 걸려 있는 자리이고, 옛 서버에서 옮겨 온 데이터에 `0` 이 잔뜩 들어 있는 이유가 이것이다.
- **`DEFAULT` 는 자바 필드의 기본값과 다르다** — 자바는 선언만으로 `int` 가 `0`, 참조가 `null` 이 되고 **적지 않아도 규칙이 있다.** SQL 의 `DEFAULT` 는 **적어 둔 값**이고, 안 적으면 기본값은 `NULL` 이다. 「선언하면 0으로 시작한다」는 감각을 그대로 들고 오면 `int` 컬럼에 `NULL` 이 든 행을 만나게 된다 → [[default-initialization]]
- **`NULL` 은 자바의 `null` 과 이름만 같다** — 자바의 `null` 은 「가리키는 객체가 없다」는 **참조의 상태**이고, 읽으면 `NullPointerException` 으로 즉시 터진다. SQL 의 `NULL` 은 **값 자리에 들어가는 「모른다」 표시**라 터지지 않고 **비교를 조용히 통과하지 못한다.** 하나는 시끄럽게 실패하고 하나는 조용히 빠지므로, 위험한 쪽은 오히려 SQL 이다 → [[object-reference]] · [[exception-handling]]
- **`NULL` 은 유일성 검사에서도 예외다** — `unique` 컬럼에 `NULL` 은 **여러 행이 가질 수 있다.** 「이메일은 유일해야 한다」에 `unique` 만 걸고 `not null` 을 빼면 이메일 없는 행이 무한히 들어온다 → [[unique-key]]
- **기본키에는 `NULL` 을 적을 수 없다** — `primary key` 를 걸면 `not null` 이 **자동으로 함께 걸린다.** 「없는 값으로는 행을 구분할 수 없다」는 것이 이유이고, 그래서 `primary key` 를 쓸 때는 `not null` 을 따로 적지 않아도 된다 → [[primary-key]]
- **`text`·`blob` 은 기본값을 가질 수 없다** — MySQL 에서 이 타입에 `default` 를 붙이면 정의 자체가 거절된다. 「긴 문자열에 기본 안내문을 넣어 두자」가 문법으로 막히는 자리다 → [[sql-data-type]]
- **정렬에서도 `NULL` 은 값이 아닌 자리를 갖는다** — MySQL 의 `order by` 오름차순에서 `NULL` 이 **맨 앞**에 온다. 「가장 작은 값」이 아니라 **정렬 구현이 정한 규약**이며 제품마다 다르다(Oracle 은 기본이 맨 뒤다). 「제일 위에 이상한 행이 있다」의 원인이 여기다.

## 함께 보는 개념

- [[ddl]] — 이 옵션을 적는 컬럼 정의 자리
- [[sql-data-type]] — 옵션 앞에 오는 타입
- [[primary-key]] — `not null` 을 강제하는 제약
- [[unique-key]] — `NULL` 을 중복으로 보지 않는 제약
- [[default-initialization]] — 자바 쪽의 「적지 않아도 정해지는 값」
- [[object-reference]] — 같은 이름의 자바 `null`
- [[surrogate-key]] — `not null` 과 생략이 함께 성립하는 컬럼
- [[crud]] — 등록 화면이 「입력하지 않음」을 어떻게 보낼지의 문제
- [[sql-operator]] — `is null` 이 다른 비교 연산자와 갈리는 자리
- [[dql]] — `NULL` 행을 잡거나 놓치는 조회
- [[dml]] — 값을 넣을 때 `NULL` 과 생략이 갈리는 자리
- [[sql-like]] — 어떤 패턴에도 걸리지 않는 값

## 출처

- [[2024-08-06-Day51]] — 「테이블 옵션」 절에서 옵션 없는 테이블에 `null` 을 네 조합으로 넣어 전부 저장되는 것을 확인하고, `not null`·`default` 를 섞은 테이블로 네 가지 `insert` 를 시험했다. **「`default` 는 입력값을 생략하면 지정되는 값이고, `null` 을 명시하면 `NULL` 이 들어간다」는 구분**을 코드와 주석으로 정확히 남긴 회차다. 「`not null` 이면 해당 컬럼을 생략할 수 없다」는 문장은 기본값이 함께 있는 경우를 포함하지 않고, 「오류!」로 적은 동작은 MySQL 의 엄격 모드에 딸려 있다
- [[2024-08-07-Day52]] — 하루 뒤, **찾는 쪽의 문법**이 온다. 연산자 절에 「null 조건 검색은 is null/ is not null(not ~ is null)로 지정한다」를 별도 항목으로 두고 세 형태를 적었다 — `NULL` 검사를 사칙·비교 연산자와 나란히 두지 않고 떼어 놓은 것이 `NULL` 이 값이 아니라는 성질과 맞는다. `where 컬럼명 = null` 이 왜 안 되는지, `count`·`avg` 가 `NULL` 을 어떻게 세는지는 다루지 않았다
