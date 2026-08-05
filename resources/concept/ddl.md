---
type: concept
id: ddl
title: DDL (Data Definition Language)
aliases:
  - DDL
  - 데이터 정의어
  - 데이터 정의 언어
  - data definition language
  - create table
  - alter table
up:
  - 2024-08-06-Day51
  - 2024-08-12-Day54
tags:
  - database
  - SQL
  - MySQL
  - 설계
---

# DDL (Data Definition Language)

**값이 아니라 값이 들어갈 틀을 다루는 SQL 부류.** Day51 의 한 줄이 「데이터베이스 구조를 정의하고 수정」이고, 대상은 데이터가 아니라 **DB 객체**(테이블·뷰·트리거·함수·프로시저·인덱스)다. 지금까지 「어떤 필드를 어떤 타입으로 들 것인가」를 정한 것은 자바의 클래스 선언이었는데, **그 일이 코드 밖으로 나가 서버에 남는 선언이 되는 것**이 이 개념이다 → [[class]]

## 정의

동작은 셋이고 대상은 여럿이다. Day51 이 적은 대상 목록에 「무엇이 들어가는 자리인가」를 채우면 이렇게 된다.

| DB 객체 | 무엇인가 | Day51 이 적은 것 |
|---|---|---|
| 데이터베이스 = 스키마 | 테이블을 담는 이름공간 | `CREATE DATABASE` → [[database-schema]] |
| 테이블 | 컬럼 정의의 묶음. 데이터가 실제로 사는 곳 | `create table` · `desc` · `drop table` |
| 뷰 (view) | **저장해 둔 `select` 문.** 이름을 테이블처럼 쓰면 그 쿼리가 대신 실행된다 — 데이터를 복사해 두는 것이 아니다 | 이름만 |
| 트리거 (trigger) | 입력·변경·삭제 **전/후에 DB 가 자동으로 실행하는 코드 덩어리** | 「특정 조건에서 자동으로 호출되는 함수」·「OOP 의 옵저버」 → [[observer-pattern]] |
| 함수 (function) | 값을 하나 **반환**하는 것. `select` 문 안에서 컬럼처럼 쓸 수 있다 | 이름만 |
| 프로시저 (procedure) | 반환값 없이 **여러 문장을 실행**하는 것. `call` 로 부른다 | 이름만 |
| 인덱스 (index) | 조회를 빠르게 하는 파생 구조 | `fulltext index` → [[database-index]] |

**동작 세 개가 모든 대상에 같은 모양으로 붙는다.**

| 동작 | 하는 일 | Day51 의 예 |
|---|---|---|
| `create` | 없던 객체를 만든다 | `create table test1( ... );` |
| `alter` | 있는 객체의 정의를 바꾼다 | `alter table ... add column` |
| `drop` | 객체를 없앤다 | `drop table 테이블명;` |

테이블을 만드는 골격은 **컬럼 하나가 네 조각**이다.

```sql
create table 테이블명(
컬럼명 타입 NULL여부 옵션,
컬럼명 타입 NULL여부 옵션
);
```

「타입」이 [[sql-data-type]], 「NULL 여부」와 「옵션」이 [[sql-null]] 이고, 컬럼 목록 뒤에 `constraint` 로 [[primary-key]]·[[unique-key]]·[[database-index]] 가 붙는다. **`create table` 한 문장이 Day51 에서 배운 것 전부를 담는 자리**다.

**엿새 뒤 Day54 가 그 `constraint` 목록에 하나를 더한다 — [[foreign-key]]** 다. 앞의 셋은 **한 테이블 안에서 값을 검사**하는데 이것만 **다른 테이블을 본다**. 그래서 DDL 로 만드는 것이 「테이블 정의」에서 「테이블들 사이의 규칙」으로 넓어진다.

만든 뒤 정의를 되읽는 명령이 따로 있다.

```sql
describe 테이블명;
desc 테이블명;
```

### 고친다 — `alter table`

이미 데이터가 든 테이블의 정의를 바꾸는 자리다. Day51 은 세 갈래를 적었다.

```sql
alter table 테이블명
  add column 컬럼명 변수타입;

alter table 테이블명
  add constraint 키이름 primary key(컬럼명),
  add constraint 키이름 unique(컬럼명),
  add fulltext index 인덱스이름(컬럼명);

alter table 테이블명
  modify column 컬럼명 변수명 (not null/null),
  modify column 컬럼명 int not null auto_increment;
```

Day54 가 여기에 네 번째 갈래를 더한다.

```sql
alter table 테이블명
    add constraint 제약조건이름 foreign key (컬럼명) references 테이블명(컬럼명);
```

**`add` 와 `modify` 의 차이가 이 명령의 성격을 가른다.** `add` 는 없던 것을 더하므로 기존 데이터와 부딪히지 않지만, `modify` 는 **이미 들어 있는 값 전부가 새 정의를 만족해야** 성립한다 — NULL 이 든 컬럼에 `not null` 을 걸면 그 자리에서 거절된다.

**그런데 `add constraint` 는 「없던 것을 더하는데도」 기존 데이터를 검사한다.** `unique` 는 이미 중복이 있으면 걸 수 없고, `foreign key` 는 참조 대상이 없는 행(고아 행)이 하나라도 있으면 걸 수 없다 — 즉 **가르는 기준은 `add`/`modify` 가 아니라 「그 규칙이 기존 값에도 적용되는가」**다. `add column` 만이 정말로 부딪히지 않는다 → [[foreign-key]]

## 사용 예시

Day51 은 같은 이름 `test1` 로 네 번 테이블을 만들며 옵션을 하나씩 바꿔 실험한다.

```sql
create table test1 (
no int,
name varchar(20)
);
```

```sql
create table test1(
no int not null,
name varchar(20) default 'noname',
age int default 20
);
```

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

**컬럼 정의는 그대로 두고 뒤의 `constraint` 만 늘어나는 것**이 이 회차의 진행 방향이다. 다만 **네 예제를 이어서 실행할 수 없다** — 아래 「경계와 오해」의 첫 항목이 그 이유다.

## 왜 중요한가

**틀을 서버가 검사해 주므로, 검사 코드를 애플리케이션에서 지울 수 있다.** 「번호를 빼먹은 등록」·「같은 이메일이 두 번」은 지금까지 자바 코드가 `if` 로 막아야 했고, 막는 것을 잊으면 그대로 들어갔다. `not null`·`primary key`·`unique` 는 그 검사를 **데이터가 사는 곳 옆으로 옮긴다** — 어느 프로그램이 접속해도, 손으로 `insert` 를 쳐도 같은 규칙이 적용된다 → [[encapsulation]]

**대신 구조 변경이 「배포」가 된다.** 자바에서 필드를 하나 더하는 것은 컴파일하면 끝이지만, 컬럼을 하나 더하는 것은 **이미 쌓인 데이터를 지나가는 작업**이다. 큰 테이블의 `alter table` 이 몇 분씩 걸리고 그 사이 서비스가 멈추는 것이 여기서 시작하는 문제다.

**그리고 되돌릴 수 없다.** 아래에 적은 대로 DDL 은 트랜잭션으로 감싸도 롤백되지 않는다 — `drop table` 을 잘못 치면 「취소」가 없다. 코드는 `git` 이 되돌려 주지만 스키마는 그렇지 않다는 비대칭이 여기 있다 → [[git]]

## 경계와 오해

- **같은 이름으로 `create table` 을 두 번 할 수 없다 — Day51 의 네 예제는 이어서 실행되지 않는다** — 전부 `test1` 이라 두 번째부터 `Table 'test1' already exists` 다. 사이에 `drop table test1;` 이 있어야 하고, 그 명령이 같은 노트의 「테이블 생성」 절에 적혀 있다. **필기가 도구를 먼저 적어 놓고 실험에서 쓰지 않은 형태**이고, 그래서 각 예제의 결과 화면은 이어지는 하나의 세션이 아니라 **매번 지우고 다시 만든 것**이다.
- **DDL ≠ DML** — 구조를 다루는 것과 값을 다루는 것이 다르다. `insert`·`update`·`delete` 는 DML 이고(조회를 따로 세면 `select` 는 DQL 이다), Day51 이 그것을 쓰는 것은 **만든 틀이 실제로 값을 막는지 확인하기 위해서**다. 하루 뒤 Day52 가 그 두 부류를 정면으로 다룬다 → [[dml]] · [[dql]] · [[crud]]
- **`drop` ≠ `delete`** — `delete` 는 행을 지우고 테이블은 남지만, `drop table` 은 **정의와 데이터를 함께 없앤다.** 「데이터를 다 지우고 싶다」로 `drop` 을 고르면 다음 `insert` 가 「없는 테이블」로 거절된다.
- **DDL 은 롤백되지 않는다** — MySQL 에서 `create`·`alter`·`drop` 은 **암시적 커밋**을 일으켜, 트랜잭션 안에서 실행해도 앞의 작업까지 확정되고 되돌릴 수 없다. 「실수하면 `rollback` 하면 된다」는 DML 에서만 통하는 습관이고, 스키마 변경 앞에서 백업을 뜨는 이유가 이것이다 → [[transaction]]
- **SQL 문의 끝은 `;` 이고, 빠뜨리면 오류가 아니라 대기다** — `mysql` 클라이언트는 세미콜론을 볼 때까지 입력을 계속 받는다. Day51 의 코드 화면에 보이는 `->` 는 바로 그 **계속 입력 프롬프트**이고(`mysql>` 가 `->` 로 바뀐다), 필기가 여러 줄 `create table` 을 그대로 복사했기 때문에 남았다. 「암호변경」 절의 `alter user ... identified by '비밀번호'` 처럼 `;` 이 없는 줄은 실행되지 않고 **아무 반응 없이 다음 줄을 기다린다** — 초보가 「멈췄다」로 읽는 자리다 → [[cli]]
- **`->` 는 SQL 문법이 아니다** — 위와 같은 이유로 필기의 `create table` 예제 안에 섞여 있는 `->`·`mysql>` 는 **프롬프트가 함께 복사된 것**이라, 그 코드를 그대로 파일에 붙여 실행하면 문법 오류가 난다. 결과 화면을 그대로 남긴 필기의 장점과 대가가 같은 자리에 있다.
- **트리거는 「함수」가 아니다** — Day51 의 「특정 조건에서 자동으로 호출되는 함수」에서 정확한 부분은 「자동으로」이고 틀린 부분은 「함수」다. 함수·프로시저는 **이름을 불러 실행하는 것**이고, 트리거는 **이름으로 부를 수 없고** DB 가 `insert`/`update`/`delete` 를 처리하는 길목에서 알아서 실행한다. 「부를 수 없다」가 트리거의 편리함이자 위험이다 — 코드를 읽어도 그것이 실행되는 줄이 보이지 않는다 → [[observer-pattern]]
- **뷰는 데이터를 복사해 두는 것이 아니다** — 「테이블처럼 보이는 것」이라 사본으로 오해하기 쉬운데, 뷰를 조회할 때마다 **저장된 `select` 가 실행**된다. 그래서 원본이 바뀌면 뷰도 바뀌고, 느린 쿼리를 뷰로 감싸도 느린 것은 그대로다. 결과를 실제로 복사해 두는 것은 별개의 장치(구체화 뷰·요약 테이블)다 → [[caching]]
- **스키마도 데이터로 저장된다** — Day51 이 사용자 목록을 `select user from mysql.user` 로 조회하는 것이 그 증거다. DDL 로 만든 정의는 특별한 곳이 아니라 **DB 안의 테이블**에 적히고(`mysql`·`information_schema`), 그래서 `desc` 대신 그 테이블을 `select` 해도 같은 답이 나온다 → [[database-schema]]

## 함께 보는 개념

- [[database-schema]] — DDL 의 가장 바깥 대상
- [[sql-data-type]] — 컬럼 정의의 「타입」 자리
- [[sql-null]] — 컬럼 정의의 「NULL 여부·옵션」 자리
- [[primary-key]] · [[unique-key]] · [[foreign-key]] — 컬럼 목록 뒤에 붙는 `constraint` 들
- [[database-index]] — 조회를 위해 따로 만드는 객체
- [[database-user]] — 이 명령들을 실행할 권한을 갖는 주체
- [[class]] — 같은 일(필드 이름과 타입 정하기)을 코드 안에서 하던 문법
- [[observer-pattern]] — 트리거가 대응한다고 필기가 적은 패턴
- [[crud]] — 만든 틀 위에서 도는 다섯 연산
- [[db-normalization]] — 테이블을 몇 개로 나눌지 정하는 원칙
- [[dml]] · [[dql]] — 하루 뒤 이 틀에 값을 넣고 꺼내는 부류들
- [[transaction]] — DDL 이 암시적 커밋으로 깨뜨리는 경계

## 출처

- [[2024-08-06-Day51]] — 「데이터베이스 구조를 정의하고 수정」으로 DDL 을 정의하고 대상 객체 일곱(데이터베이스=스키마·테이블·뷰·트리거·함수·프로시저·인덱스)을 나열했다. `create table` 의 컬럼 정의 골격(`컬럼명 타입 NULL여부 옵션`)·`desc`·`drop table` 을 적고, 같은 이름 `test1` 로 테이블을 네 번 만들며 옵션과 제약을 하나씩 더해 실험한 뒤 `alter table` 의 `add column`·`add constraint`·`modify column` 으로 닫는다. 트리거만 세 줄(「자동으로 호출되는 함수」·「SQL 실행 전/후」·「옵저버에 해당」)이 붙고 뷰·함수·프로시저는 이름만 남았다. 예제 네 개가 모두 `test1` 이라 사이에 `drop table` 없이는 이어 실행되지 않으며, 코드에 `mysql>`·`->` 프롬프트가 함께 복사돼 있다
- [[2024-08-12-Day54]] — 엿새 뒤 `alter table ... add constraint 제약조건이름 foreign key (컬럼명) references 테이블명(컬럼명)` 로 **`add constraint` 의 네 번째 갈래**를 더한다. 게시판 첨부파일 구조를 `create table` 로 두 번 세우며(한 테이블에 `filepath1`~`filepath5` → 게시글·첨부 두 테이블) **DDL 이 「어떤 컬럼을 둘까」에서 「테이블을 몇 개로 나눌까」로 넘어가는 자리**를 보여 주고, 두 번째 설계에 대해 스스로 「데이터 무결성 에러」라 적어 제약이 필요한 이유를 만들어 냈다. Day51 과 달리 이 회차의 `create table` 예제에는 프롬프트가 섞여 있지 않고 `;` 도 붙어 있다 → [[foreign-key]]
