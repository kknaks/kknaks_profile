---
type: concept
id: database-user
title: 데이터베이스 사용자와 권한 (User / Privilege)
aliases:
  - DB 사용자
  - 데이터베이스 사용자
  - database user
  - MySQL 사용자
  - CREATE USER
  - GRANT
  - 권한 부여
up:
  - 2024-08-06-Day51
tags:
  - database
  - MySQL
  - 보안
  - 네트워크
---

# 데이터베이스 사용자와 권한 (User / Privilege)

**DB 서버에 접속할 자격과, 접속한 뒤 무엇을 할 수 있는지가 따로 정해진다.** 만드는 것(`CREATE USER`)과 할 수 있게 하는 것(`GRANT`)이 두 명령으로 갈려 있고, **사용자의 정체는 이름 하나가 아니라 「이름 + 어디서 접속했는가」 쌍**이다.

## 정의

`CREATE USER` 의 인자가 둘로 보이는 것이 이 개념의 핵심이다.

```sql
CREATE USER '사용자아이디'@'서버주소' IDENTIFIED BY '암호';
```

**`@` 뒤가 「이 사용자가 접속해 올 수 있는 곳」**이고, 그 값까지가 사용자 이름의 일부다.

| Day51 이 만든 것 | `@` 뒤의 뜻 | 결과 |
|---|---|---|
| `'study'@'localhost'` | 서버가 돌고 있는 그 컴퓨터 | 그 기계에서만 접속 |
| `'study'@'%'` | **모든 호스트** (와일드카드) | 어디서든 접속 |

이름이 같아도 `@` 뒤가 다르면 **별개의 사용자**다 — 암호도 따로 갖고 권한도 따로 갖는다. Day51 이 같은 `study` 를 두 번 만든 것은 사용자를 고친 것이 아니라 **둘을 만든 것**이다.

접속하는 쪽도 같은 정보를 준다.

```bash
mysql -u root -p                    # 로컬 — 호스트를 안 적으면 localhost
mysql -h 서버주소 -u root -p         # 원격 — -h 로 서버를 지정한다
```

암호를 바꾸는 것도 **그 쌍을 지목**해서 한다.

```sql
alter user 'root'@'localhost' identified by '비밀번호'
```

### 만든 것만으로는 아무것도 못 한다

`CREATE USER` 는 「들어올 수 있다」까지이고, 데이터를 만지려면 권한을 따로 준다.

```sql
GRANT ALL ON 데이터베이스명.* TO '사용자아이디'@'서버주소';
GRANT ALL ON studydb.* TO 'study'@'localhost';
```

**`ON` 뒤가 범위, `TO` 뒤가 상대**다. `studydb.*` 는 「그 데이터베이스의 모든 테이블」이고 → [[database-schema]], 상대를 적을 때도 **호스트까지** 써야 한다 — `'study'@'localhost'` 에 준 권한은 `'study'@'%'` 에게는 없다.

사용자 목록은 특별한 명령이 아니라 **테이블 조회**로 본다.

```sql
select user from mysql.user;
```

**서버의 계정 정보가 `mysql` 데이터베이스의 `user` 테이블에 들어 있다** — 설정이 설정 파일이 아니라 데이터로 사는 것이고, 그래서 `select` 로 읽힌다 → [[ddl]]

## 사용 예시

Day51 이 세운 순서가 그대로 「DB 를 쓸 수 있게 만드는 절차」다.

```sql
-- 1) root 로 들어가 암호를 바꾼다
alter user 'root'@'localhost' identified by '비밀번호';

-- 2) 작업용 사용자를 만든다
CREATE USER 'study'@'localhost' IDENTIFIED BY '비밀번호';

-- 3) 데이터베이스를 만든다
CREATE DATABASE studydb
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

-- 4) 그 데이터베이스에 대한 권한을 준다
GRANT ALL ON studydb.* TO 'study'@'localhost';
```

그 다음 **사용자를 바꾸는 방법이 「나갔다 다시 들어오는 것」**이다.

```bash
quit                  # 프로그램 종료
mysql -u study -p     # 다시 실행
```

**접속 하나에 사용자 하나가 붙어 있고 도중에 갈 수 없다** — 인증이 접속을 세울 때 한 번 일어나기 때문이다 → [[client-server-model]]

## 왜 중요한가

**사고 범위를 미리 자른다.** 애플리케이션이 `root` 로 접속하면 SQL 하나가 잘못 나갈 때 **서버의 모든 데이터베이스**가 사거리에 들어온다. `GRANT ALL ON studydb.*` 로 묶어 두면 같은 실수가 그 데이터베이스 안에서 끝난다 — 권한은 「할 수 있는 일」의 목록이 아니라 **최악의 경우 잃는 것의 크기**다.

**호스트 제한은 방화벽과 다른 층에서 같은 일을 한다.** `'app'@'10.0.1.%'` 처럼 적어 두면 암호가 새어 나가도 **그 대역 밖에서는 그 계정으로 들어올 수 없다.** 자격 하나가 「무엇을 아는가」와 「어디에 있는가」 두 조건을 함께 요구하게 되는 것이고, 이것이 DB 계정이 일반 로그인과 다른 점이다 → [[ip-address]]

**그리고 「접속이 안 된다」의 원인이 셋으로 갈린다.** 서버까지 못 갔는가(네트워크·포트), 계정이 아닌가(호스트 쌍·암호), 계정은 맞는데 권한이 없는가 — 세 층이 각자 다른 메시지를 준다. 이 구분을 모르면 `Access denied` 하나를 놓고 방화벽을 뒤진다 → [[socket-binding]] · [[port-number]]

## 경계와 오해

- **`'study'@'%'` 는 「원격에서만」이 아니다 — Day51 의 오류다** — 필기는 「원격에서만 접속할 수 있는 사용자를 만들기」로 적었지만 `%` 는 **모든 호스트를 뜻하는 와일드카드**이므로 로컬 접속도 여기에 걸린다(도커의 MySQL 이 `root'@'%'` 하나로 컨테이너 안에서도 접속되는 것이 그 예다). 「원격만」을 정말 원하면 대역을 적어야 한다(`'study'@'192.168.0.%'`). 그리고 `'study'@'localhost'` 와 `'study'@'%'` 를 **둘 다 만들면** MySQL 은 **호스트가 더 구체적인 쪽을 먼저 골라** 인증하므로, 로컬 접속은 `localhost` 항목의 암호를 요구한다 — Day51 처럼 두 계정의 암호를 다르게 준 상태(`'비밀번호'` 와 `'1111'`)에서 「원격 계정 암호로 로컬 로그인이 안 되는」 현상이 정확히 이것이다. **「%는 원격 전용」으로 외우면 이 동작을 설명할 수 없다.**
- **MySQL 에서 `localhost` ≠ `127.0.0.1`** — 같은 기계를 가리키는 두 표기인데 MySQL 은 **접속 방식으로 구분**한다. `-h localhost` 는 유닉스 소켓(파일)으로 붙고 `-h 127.0.0.1` 은 TCP 로 붙으므로, `'study'@'127.0.0.1'` 만 만들어 두고 `mysql -u study` 로 접속하면 거절된다. 「같은 컴퓨터인데 왜 안 되나」의 답이 여기 있다 → [[socket]] · [[ip-address]]
- **사용자 ≠ 스키마** — Oracle 에서는 사용자를 만들면 그의 스키마가 생기지만, MySQL 에서 사용자와 데이터베이스는 **아무 관계가 없다.** `study` 를 만들어도 `study` 라는 데이터베이스가 생기지 않고, `GRANT` 로 연결을 손으로 만들어야 한다 → [[database-schema]]
- **`GRANT ALL` 은 서버 전체 권한이 아니다** — `ALL` 이 무서워 보이지만 `ON studydb.*` 가 범위를 자른다. 진짜 위험한 형태는 `ON *.*` 이고, 여기에 `WITH GRANT OPTION` 이 붙으면 **권한을 남에게 나눠 줄 권한**까지 준 것이다.
- **암호를 명령줄에 적지 않는다** — `mysql -u study -p` 는 `-p` 뒤에 값을 비워 두어 **프롬프트로 받는다.** `-p비밀번호` 로 붙여 쓰면 실행되지만 그 줄이 셸 히스토리와 프로세스 목록(`ps`)에 남는다. Day51 이 적은 형태가 안전한 쪽이다 → [[cli]] · [[command-line-arguments]]
- **권한은 접속 중에 바로 바뀌지 않을 수 있다** — 서버가 권한 표를 메모리에 들고 있어서, `GRANT` 를 직접 쓰는 대신 `mysql.user` 테이블을 `update` 로 고치면 `FLUSH PRIVILEGES` 까지 해야 반영된다. **「설정이 데이터로 보인다」는 것이 「데이터를 고치면 설정이 바뀐다」는 뜻은 아니다** → [[caching]]
- **`root` 는 운영체제의 root 와 다른 계정이다** — 이름만 같다. MySQL 의 `root` 는 그 서버 안에서만 뜻이 있고 암호도 따로다. 「같은 암호일 것」이라는 가정이 초기 설정에서 자주 어긋난다.

## 함께 보는 개념

- [[database-schema]] — 권한을 주는 단위
- [[ddl]] — 계정 정보조차 테이블로 사는 자리
- [[client-server-model]] — 접속마다 사용자가 붙는 구조
- [[socket]] · [[socket-binding]] — `localhost` 와 `127.0.0.1` 이 갈리는 층
- [[ip-address]] — `@` 뒤에 대역을 적는 문법의 근거
- [[port-number]] — 「접속이 안 된다」의 다른 원인
- [[cli]] · [[command-line-arguments]] — `-u`·`-p`·`-h` 를 주는 자리
- [[encapsulation]] — 할 수 있는 일을 밖에서 잘라 주는 같은 발상

## 출처

- [[2024-08-06-Day51]] — `mysql -u root -p`·`mysql -h 서버주소 -u root -p` 로 로컬·원격 접속을 가르고, `alter user 'root'@'localhost' identified by` 로 암호를 바꾼 뒤 `CREATE USER '아이디'@'서버주소' IDENTIFIED BY` 로 사용자를 만든다. `'study'@'localhost'` 와 `'study'@'%'` 를 나란히 만들며 `@` 뒤가 접속 위치임을 보여 주고, `select user from mysql.user` 로 목록을 조회하고 `GRANT ALL ON studydb.* TO 'study'@'localhost'` 로 데이터베이스 단위 권한을 준다. 사용자를 바꾸려면 `quit` 후 다시 접속한다는 것까지 적었다. 다만 `'study'@'%'` 를 「원격에서만 접속 가능」으로 적은 것은 `%` 가 모든 호스트라는 뜻이므로 틀렸다
