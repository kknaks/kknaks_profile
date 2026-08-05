---
type: concept
id: database-schema
title: 데이터베이스와 스키마 (Database / Schema)
aliases:
  - 스키마
  - schema
  - CREATE DATABASE
  - 데이터베이스 생성
  - collation
  - 콜레이션
  - 정렬 규칙
up:
  - 2024-08-06-Day51
tags:
  - database
  - MySQL
  - 인코딩
  - 설계
---

# 데이터베이스와 스키마 (Database / Schema)

**테이블들을 담는 이름공간 하나.** MySQL 서버 하나 안에 여러 개가 있고, 접속한 뒤 `use` 로 하나를 골라 쓴다. Day51 은 「데이터베이스(database) = 스키마(schema)」로 배웠는데 **그 등호가 성립하는 것은 MySQL 안에서다**(아래 「경계와 오해」).

## 정의

만들 때 **이름 말고 두 가지를 더 정한다.** Day51 의 주석이 그 둘을 정확히 가리킨다.

```sql
CREATE DATABASE studydb /* 인코딩 방식*/
DEFAULT CHARACTER SET utf8 /* 정렬 및 비교 방식*/
DEFAULT COLLATE utf8_general_ci;
```

| 지정 | 정하는 것 | 어긋나면 |
|---|---|---|
| `CHARACTER SET` | 글자를 **몇 바이트로 어떻게** 적을 것인가 | 저장한 글자가 다른 글자로 읽힌다 → [[character-encoding]] |
| `COLLATE` | 그 바이트들을 **어떻게 비교·정렬**할 것인가 | `order by` 순서와 **중복 판정**이 달라진다 |

`DEFAULT` 가 붙은 것이 핵심이다 — **이 두 값은 데이터베이스에 박히는 것이 아니라 그 안에 만들어지는 테이블·컬럼의 기본값으로 내려간다.** 테이블에서, 다시 컬럼에서 덮어쓸 수 있고, 아무것도 안 적으면 위에서 물려받는다.

이름 뒤의 `_ci` 는 **case insensitive**(대소문자 무시)다. `utf8_general_ci` 를 고르면 `'Kim'` 과 `'kim'` 이 **같은 값**이 되어 `where name = 'kim'` 이 둘 다 찾고, `unique` 컬럼이라면 둘 중 하나가 거절된다 → [[unique-key]] · [[string-comparison]]

### 서버 · 데이터베이스 · 테이블의 층

```sql
show databases;        -- 서버가 담고 있는 데이터베이스 목록
use studydb;           -- 앞으로 이름만 쓰면 이 데이터베이스로 해석한다
show tables;           -- 지금 고른 데이터베이스의 테이블 목록
```

`use` 는 **소유가 아니라 생략을 위한 설정**이다. 고르지 않았거나 다른 곳을 볼 때는 `데이터베이스명.테이블명` 으로 온전한 이름을 쓴다 — Day51 의 `select user from mysql.user` 가 그 형태이고, `mysql` 은 **서버가 자기 사용자 정보를 담아 두는 데이터베이스**다 → [[database-user]]

## 사용 예시

권한도 이 단위로 준다. Day51 이 `studydb` 를 만든 직후에 하는 일이 그것이다.

```sql
CREATE DATABASE studydb
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

GRANT ALL ON studydb.* TO 'study'@'localhost';
```

**`studydb.*` 의 `*` 가 「이 데이터베이스의 모든 테이블」**이다. 데이터베이스가 이름공간인 것이 여기서 값을 갖는다 — 프로젝트마다 데이터베이스를 따로 만들면 **권한을 한 줄로 가둘 수 있다.**

## 왜 중요한가

**처음 한 줄이 나중에 고치기 가장 어려운 것을 정한다.** 테이블은 `alter table` 로 컬럼을 더하면 되지만, 데이터가 쌓인 뒤 문자집합을 바꾸는 것은 **모든 행을 다시 쓰는 작업**이고 인덱스 길이 제한에 걸려 실패하기도 한다. Day51 이 별생각 없이 적은 `utf8` 한 낱말이 「이모지를 저장할 수 있는가」를 결정한다 — 아래 「경계와 오해」의 두 번째 항목이 그 이야기다.

**`collate` 는 성능이 아니라 정답을 바꾼다.** 인코딩이 틀리면 글자가 깨져서 바로 보이는데, collation 이 다르면 **결과가 조용히 달라진다** — 같은 `select` 가 다른 행 수를 돌려주고, 같은 `insert` 가 한 서버에서는 통하고 다른 서버에서는 중복으로 거절된다. 「개발에서는 됐는데 운영에서 안 된다」의 흔한 원인이 이 값의 불일치다.

**그리고 나눠 두면 사고가 갇힌다.** 데이터베이스 하나에 전부 몰아 넣으면 권한도 전부 아니면 전무가 되고, 실수로 `drop table` 을 친 손이 남의 테이블에도 닿는다 → [[database-user]]

## 경계와 오해

- **데이터베이스 ≠ 스키마 — MySQL 에서만 같다** — Day51 의 「데이터베이스 = 스키마」는 MySQL 에서 두 낱말이 실제로 같은 것을 가리키기 때문에(`CREATE SCHEMA` 가 `CREATE DATABASE` 의 동의어다) 맞는 말이지만, **다른 DB 로 옮기면 깨진다.** 표준 SQL 과 PostgreSQL 에서는 데이터베이스 하나가 스키마 여럿을 담고, Oracle 에서는 **스키마가 사용자와 짝**이다(사용자 하나 = 스키마 하나). 「스키마」가 「구조 정의 전체」라는 더 일반적인 뜻으로도 쓰이므로, 이 낱말이 나오면 **어느 제품의 말인지 확인하는 것**이 정확한 습관이다.
- **데이터베이스 ≠ DB 서버** — 「MySQL 을 설치했다」와 「데이터베이스를 만들었다」가 다른 일이다. 설치한 것은 프로세스 하나(서버)이고, 그 안에 이름공간을 여러 개 만드는 것이 `CREATE DATABASE` 다. 접속 주소·포트는 서버의 것이고 `use` 로 고르는 것은 그 안의 것이다 → [[process]] · [[port-number]]
- **MySQL 의 `utf8` ≠ UTF-8** — MySQL 의 `utf8` 은 **한 글자에 최대 3바이트**만 쓰는 반쪽 구현(`utf8mb3`)이라 4바이트가 필요한 문자(이모지, 일부 한자)를 저장할 수 없고 `Incorrect string value` 로 거절한다. 진짜 UTF-8 은 `utf8mb4` 다. Day51 의 「UTF-8로 지정된 경우 `varchar` 의 n 은 최대 21844」라는 숫자가 **바로 그 3바이트에서 나온 것**이라(65535 ÷ 3 ≈ 21845), 이 함정은 필기 안에 이미 흔적을 남기고 있다 → [[sql-data-type]] · [[unicode]]
- **`COLLATE` ≠ `CHARACTER SET`** — 한 문장에 나란히 적혀 있어 하나로 보이지만 축이 다르다. 인코딩은 **글자 → 바이트** 규칙이고 collation 은 **바이트 ↔ 바이트 비교** 규칙이다. 같은 `utf8` 에도 `utf8_general_ci`·`utf8_bin` 등이 여러 개 붙을 수 있고, `_bin` 을 고르면 대소문자를 구분한다. 「인코딩만 맞췄는데 정렬이 이상하다」가 이 구분을 모를 때 나오는 증상이다 → [[character-encoding]]
- **`use` 는 접속의 상태다** — 데이터베이스를 고른 것은 **그 세션에만** 적용되고, 새로 접속하면 다시 골라야 한다. 스크립트를 파일로 실행할 때 `use` 를 빠뜨리면 「테이블이 없다」가 나오는데, 원인은 테이블이 아니라 **어디를 보고 있는지**다.
- **한글 이름과 대소문자** — 데이터베이스 이름은 파일시스템의 디렉토리로 만들어지므로, **테이블·데이터베이스 이름의 대소문자 구분이 운영체제에 따라 다르다**(리눅스는 구분, macOS·윈도우는 대개 구분하지 않는다). 맥에서 만든 스크립트가 리눅스 서버에서 「없는 테이블」이 되는 경로가 여기다 → [[platform-dependency]] · [[filesystem-path]]

## 함께 보는 개념

- [[ddl]] — 이 객체를 만드는 명령의 부류
- [[database-user]] — 권한이 이 단위로 주어지는 상대
- [[character-encoding]] · [[unicode]] — `CHARACTER SET` 이 고르는 규칙
- [[sql-data-type]] — 문자집합이 `varchar(n)` 의 한계를 정하는 자리
- [[unique-key]] · [[string-comparison]] — collation 이 중복·비교 판정을 바꾸는 자리
- [[db-normalization]] — 이 안에서 테이블을 몇 개로 나눌지의 문제
- [[platform-dependency]] — 이름의 대소문자가 운영체제에 딸려 오는 이유

## 출처

- [[2024-08-06-Day51]] — 「데이터베이스(database) = 스키마(schema)」로 적고, `CREATE DATABASE ... DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci` 를 「인코딩 방식」·「정렬 및 비교 방식」 두 주석으로 갈라 적었다. `show databases`·`use studydb`·`show tables` 로 층을 오르내리고, 만든 직후 `GRANT ALL ON studydb.*` 로 권한을 데이터베이스 단위로 준다. `select user from mysql.user` 처럼 `데이터베이스명.테이블명` 을 쓰는 형태도 함께 나온다. `utf8` 을 UTF-8 로 적고 있는데, 같은 노트의 「`varchar` 는 UTF-8 이면 최대 21844」가 그 `utf8` 이 3바이트 구현임을 드러낸다
