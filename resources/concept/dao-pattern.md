---
type: concept
id: dao-pattern
title: DAO (Data Access Object)
aliases:
  - DAO
  - dao
  - Data Access Object
  - 데이터 접근 객체
  - DAO 패턴
up:
  - 2024-08-16-Day57
  - 2024-08-20-Day59
tags:
  - 설계
  - database
  - java
  - 계층
---

# DAO (Data Access Object)

**저장소에 닿는 코드를 한 클래스에 모으고, 부르는 쪽에는 도메인 타입으로 된 메서드만 보이게 하는 층.** `projectDao.insert(project)` 를 부르는 쪽은 `Connection`·`PreparedStatement`·SQL 을 하나도 모른다. Day57 이 이 클래스를 **코드로만** 보여 주고, 나흘 뒤 Day59 의 「Dao 기능분리」 절이 그 층이 무엇을 맡는지 처음 말로 적었다 → [[jdbc]] · [[crud]]

## 정의

Day59 의 세 줄이 이 패턴의 경계를 세운다.

1. 「기존 Dao 소스는 java상에서 JDBC를 활용하여 쿼리문을 전송하고 결과를 리턴 받는다」 — **DAO 가 맡는 일**
2. 「유지보수 측면에서 Java코드와 SQL쿼리가 혼재되어 불리하다」 — **그 안에 섞여 있는 두 가지**
3. 「Mybatis를 사용해서 JDBC API의 역할을 이전하고 소스에서는 자바코드만 작성한다」 — **떼어 낼 수 있는 쪽**

즉 DAO 안에는 성질이 다른 셋이 있다.

| DAO 안의 것 | 무엇인가 | 떼어 낼 수 있나 |
|---|---|---|
| 메서드 이름과 시그니처 (`Project findBy(int no)`) | **부르는 쪽과의 계약** | 아니다 — 이것이 DAO 다 |
| SQL 문장 | 저장소에 하는 말 | **된다** → 매퍼 XML |
| `PreparedStatement` 준비·바인딩·`ResultSet` 읽기 | JDBC 를 다루는 절차 | **된다** → 세션·프레임워크 |

**Day58·Day59 가 아래 두 줄을 차례로 걷어내는 세 회차 사다리**이고, 첫 줄은 끝까지 남는다 → [[sql-session]] · [[mybatis]]

### 층으로 보면

| 층 | 아는 것 | 모르는 것 | 이 필기에서 |
|---|---|---|---|
| 화면 (Command) | 「프로젝트를 등록한다」 | SQL · 연결 | `ProjectAddCommand` |
| **DAO** | **SQL · 연결 · 커서** | 화면 · 사용자 입력 | `ProjectDao` |
| 저장소 | 테이블 · 제약 | 자바 | MySQL |

**DAO 가 갈라 놓는 것은 「무엇을 원하는가」와 「그것을 어떻게 얻는가」다** → [[cohesion]] · [[coupling]]

## 사용 예시

Day57 §2.1 이 실습 프로젝트의 DAO 를 다섯 메서드로 보였다. **다섯 개의 시그니처가 이 층의 계약 전부다.**

```java
boolean insert(Project project) throws Exception
List<Project> list() throws Exception
Project findBy(int no) throws Exception
boolean update(Project project) throws Exception
boolean delete(int no) throws Exception
```

**반환형에 JDBC 의 낱말이 하나도 없다.** `ResultSet` 이 아니라 `List<Project>` 를 돌려주고, 성공 여부는 `boolean` 이다 — 그 변환이 메서드 안에서 일어난다 → [[result-set]] · [[crud]]

```java
List<Project> list() throws Exception{
  try (Statement stmt = con.createStatement();
          ResultSet rs = stmt.executeQuery(select 쿼리문)) {
    ArrayList<Project> list = new ArrayList<>();
    while (rs.next()) {
      Project project = new Project();
      project.setNo(rs.get(컬럼명));
      list.add(project);
    }
    return list;
  }
}
```

**커서를 다 읽어 담아 돌려주는 것이 이 층의 실제 일이다.** `ResultSet` 을 그대로 밖으로 넘기면 문장이 닫히는 순간 죽으므로, **자원의 수명이 메서드 안에서 끝나야 한다는 것이 반환형을 정한다** → [[try-with-resources]]

### 나흘 뒤 Day59 — 같은 다섯 메서드가 껍데기가 된다

`delete` 하나가 세 회차에서 어떻게 얇아지는지가 이 층의 값을 보인다.

```java
// Day57 §2.1 — DAO 가 JDBC 를 직접 다룬다
boolean delete(int no) throws Exception{
  try (PreparedStatement stmt = con.prepareStatement(delete 쿼리문)) {
    stmt.setInt(1, no);
    int count = stmt.executeUpdate();
    return count > 0;
  }
}

// Day58 — 절차가 세션으로 빠진다. SQL 은 아직 여기 있다
boolean delete(int no) throws Exception {
  return session.delete("delete from myapp_projects where project_id=?", no) > 0;
}

// Day59 — SQL 도 XML 로 빠진다. 남는 것은 이름과 값
boolean delete(int no) throws Exception {
  return sqlSession.delete("UserDao.delete", no) > 0;
}
```

**세 번 줄어드는 동안 첫 줄(시그니처)이 한 글자도 바뀌지 않았다.** 부르는 화면 코드는 세 회차 내내 같은 것을 부른다 — 그것이 이 층이 실제로 지불받는 값이고, Day59 의 「JDBC API의 역할을 이전」이 화면을 안 건드리고 가능한 이유다 → [[mybatis]] · [[sql-session]]

## 왜 중요한가

**저장소를 다루는 API 를 아는 코드가 한 곳으로 줄어든다.** `Statement`·`ResultSet`·SQL 이라는 낱말이 DAO 안에만 있으면, 드라이버를 바꾸거나 프레임워크를 얹거나 테이블 이름을 고칠 때 **열어야 하는 파일이 하나**다. Day59 가 실제로 그 일을 했다 — JDBC 를 MyBatis 로 바꾸면서 화면 코드를 열지 않았다 → [[coupling]] · [[encapsulation]]

**그리고 화면 코드가 도메인 언어로만 쓰인다.** `projectDao.findBy(no)` 는 「몇 번 프로젝트를 가져와라」로 읽히고, 그 안의 `select`·`where`·`rs.next()` 는 읽는 사람의 머리에 들어오지 않는다. **한 파일이 한 층의 낱말만 쓰게 되는 것**이 층을 나눈 결과다 → [[cohesion]]

**대신 층이 하나 늘어난 만큼 「어디에 쓸지」를 매번 정해야 한다.** 팀원 목록까지 함께 넣는 등록은 DAO 메서드 둘인가 하나인가, 커밋은 어디서 하나, 조회 조건이 화면마다 다르면 메서드를 몇 개 만드나 — **이 질문들이 DAO 를 만들고 나서야 생긴다** → [[transaction]]

## 경계와 오해

- **Day57 은 DAO 를 코드로만 보였다 — 이름이 붙은 것이 코드를 쓴 것보다 늦다** — Day57 §2.1 에서 DAO 에 대한 설명은 「Dao의 Statement의 구조는 다음과 같다」 한 줄뿐이고 그 뒤는 전부 코드다. 즉 **그 클래스가 어느 층을 맡는지는 적히지 않았다.** 나흘 뒤 Day59 의 「Dao 기능분리」 세 줄이 처음 그 경계를 말로 적는데, 그 계기가 **MyBatis 로 옮기려고 「무엇을 이전할 것인가」를 물었기 때문**이다 — **바꿔 보려 할 때 비로소 층의 이름이 필요해지는 자리**다.
- **DAO 가 있다는 것이 저장소를 감췄다는 뜻은 아니다** — Day57 의 다섯 메서드가 전부 `throws Exception` 이고 그 안에는 `SQLException` 이 온다. 부르는 화면이 「SQL 오류인지 연결 오류인지 프로그램 버그인지」를 구별할 수 없는 상태로 예외를 받으므로, **저장소가 DAO 를 통과해 밖으로 새어 나온다.** 감췄는지 판정하는 기준은 「SQL 이 안 보이는가」가 아니라 **「저장소 종류를 짐작할 수 있는 것이 하나라도 넘어오는가」**다 → [[exception-handling]]
- **DAO ≠ VO/DTO** — 이름이 닮아 짝처럼 보이는데 종류가 다르다. DAO 는 **동작**(메서드만 있고 상태는 연결뿐)이고, `bitcamp.myapp.vo.User` 같은 VO 는 **데이터**(필드와 getter/setter 뿐)다. Day59 의 `resultType="bitcamp.myapp.vo.User"` 가 가리키는 것이 후자이고, DAO 가 그것을 만들어 돌려준다 → [[encapsulation]]
- **인터페이스 없는 DAO 는 바꿔 끼울 수 없다 — Day59 의 「이전」은 갈아타기가 아니라 고쳐 쓰기다** — 클래스가 하나뿐이면 JDBC 판을 MyBatis 판으로 바꾸는 일은 **그 파일을 고치는 것**이고, 되돌리려면 다시 고쳐야 하고 둘을 나란히 두고 비교할 수도 없다. 「구현을 바꿔 끼운다」가 성립하려면 `interface ProjectDao` 와 두 구현 클래스가 있고 화면이 인터페이스만 알아야 한다 — 그때 비로소 저장소를 바꾸는 일이 **설정의 문제**가 된다 → [[interface]] · [[dependency-injection]] · [[dependency-inversion-principle]] · [[open-closed-principle]]
- **트랜잭션 경계는 DAO 의 것이 아니다** — Day57 §2.2 가 커밋을 화면 코드에 둔 것이 맞다. DAO 메서드 하나하나에 `commit()` 을 넣으면 **두 메서드를 한 덩어리로 묶을 방법이 없어진다** — 등록이 `insert` + `insertMembers` 둘이므로 앞이 이미 확정되면 뒤가 실패해도 되돌릴 것이 없다. 「DAO 가 DB 를 다 맡는다」로 읽으면 커밋도 그쪽 일로 보이는데, **경계는 「하나의 작업」을 아는 층이 정해야 하고 그것은 화면(또는 그 아래 서비스)이다** → [[transaction]]
- **한 화면이 DAO 메서드 여럿을 부르면 그 조합은 어디에도 살지 않는다** — Day57 의 등록 화면이 `insert` → `insertMembers` 순서와 커밋 경계를 **직접** 들고 있다. 그 순서가 화면 코드에 흩어져 있으므로 다른 화면에서 같은 등록을 하려면 순서를 다시 쓴다. 「DAO 위에 화면」 두 층 사이가 비어 있는 상태이고, 그 자리를 채우는 것이 서비스 층이다 — **이 필기에는 그 층이 없다** → [[cohesion]]
- **「JDBC API의 역할을 이전」해도 DAO 자체는 남는다** — Day59 의 세 번째 줄이 「소스에서는 자바코드만 작성한다」라서 DAO 가 없어지는 것처럼 읽힐 수 있는데, 이전된 것은 **문장 준비·바인딩·커서 읽기**이고 `sqlSession` 을 부르는 클래스는 그대로 DAO 다. MyBatis 에는 DAO 클래스를 인터페이스 하나로 대체하는 길(매퍼 인터페이스)이 실제로 있지만, Day59 의 코드는 그 형태가 아니다 → [[mybatis]]
- **DAO 는 SQL 을 줄이지 않는다 — 화면 수만큼 늘어나기 쉽다** — 조회 조건이 화면마다 다르면 `findByNo`·`findByName`·`findByNameAndDate` … 로 메서드가 불어난다. 그것을 막으려고 조건을 문자열이나 `Map` 으로 받기 시작하면 **다시 SQL 조각이 화면으로 올라간다.** 「메서드가 계약이다」의 대가가 여기 있고, MyBatis 의 동적 SQL(`<if>`·`<where>`)이 그 자리에 대한 답이다 → [[mybatis]] · [[parameterization]]
- **`boolean` 반환은 정보를 접는다** — `count > 0` 형태는 「지웠다/못 지웠다」만 남기므로 조건에 맞는 행이 **여럿 바뀐 경우**를 알 수 없다. `where` 를 빠뜨린 `update` 가 전체 행을 고쳐도 `true` 다. **DAO 의 시그니처가 계약이므로 여기서 접은 정보는 위층에서 되찾을 수 없다** → [[dml]]
- **`con` 을 필드로 들고 있는 DAO 는 여러 화면이 상태를 공유한다** — Day55~58 의 DAO 는 밖에서 만든 `Connection` 을 받아 필드로 쥔다. 그래서 어느 화면이 `setAutoCommit(false)` 를 하고 되돌려 놓지 않으면 **다음 화면이 자기도 모르게 수동 커밋 상태**가 된다. Day59 의 `<dataSource type="POOLED">` 는 그 문제를 프레임워크에 넘긴다 → [[connection-lifetime-mismatch]] · [[transaction]]
- **DAO 와 Repository 는 같은 낱말이 아니다** — DAO 는 **테이블 접근을 감싸는 층**이고, Repository 는 **도메인 객체의 집합처럼 보이게 하는 층**(「조건에 맞는 것들을 달라」)이다. 실무에서 이름만 바꿔 쓰는 경우가 많아 구별이 흐려졌지만, 뒤쪽은 「저장소가 무엇인지」를 도메인이 아예 모르는 것을 목표로 하므로 반환형에 `boolean count > 0` 같은 것이 오지 않는다. 이 필기의 것은 앞쪽이다 → [[interface]]
- **Day57 의 DAO 코드는 그대로 컴파일되지 않는다** — `stmt.set(?,values)`·`rs.get(컬럼명)` 은 존재하지 않는 메서드이고 `insert 쿼리문` 같은 자리 표시가 인수 자리에 그대로 있고 `int count = stmt.executeUpdate()` 에 세미콜론이 없다. **구조를 보이는 스케치**이므로 층의 형태를 읽는 데는 충분하지만, 이 다섯 메서드를 옮겨 쓸 수 있는 것으로 읽으면 안 된다. 그리고 `delete` 의 주석·문자열이 「update 쿼리문」이라 **복사해 만든 흔적**이 남아 있다 → [[prepared-statement]]

## 함께 보는 개념

- [[crud]] — DAO 의 다섯 메서드가 곧 이것
- [[jdbc]] — DAO 안에 감춰지는 API
- [[sql-session]] — 절차를 걷어낸 첫 걸음
- [[mybatis]] — SQL 까지 걷어낸 다음 걸음
- [[persistence-framework]] — 그 두 걸음의 이름
- [[transaction]] — 이 층이 가질 수 없는 경계
- [[result-set]] · [[try-with-resources]] — 반환형을 정하는 자원 수명
- [[prepared-statement]] — Day57 이 이 층 안에서 바꾼 것
- [[generated-keys]] — `insert` 의 반환값이 계약이 되는 자리
- [[interface]] · [[dependency-injection]] · [[dependency-inversion-principle]] · [[open-closed-principle]] — 「바꿔 끼운다」가 성립하는 조건
- [[cohesion]] · [[coupling]] · [[encapsulation]] — 층을 나눈 값을 재는 축
- [[command-pattern]] — 이 층을 부르는 위쪽
- [[connection-lifetime-mismatch]] — 연결을 필드로 공유한 대가
- [[dml]] — `boolean` 으로 접힌 행 수

## 출처

- [[2024-08-16-Day57]] — 실습 프로젝트의 `ProjectDao` 를 다섯 메서드(`insert`·`list`·`findBy`·`update`·`delete`)로 보이고, 같은 다섯 개의 `Statement` 판과 `PreparedStatement` 판을 나란히 놓았다. **반환형에 JDBC 의 낱말이 하나도 없고**(`List<Project>`·`Project`·`boolean`) 커서를 다 읽어 담아 돌려주는 형태가 이 층의 계약을 그대로 보인다. 다만 DAO 에 대한 설명은 「Dao의 Statement의 구조는 다음과 같다」 한 줄뿐이고 **그 클래스가 어느 층을 맡는지는 적히지 않았다.** §2.2 가 커밋 경계를 DAO 밖(등록 화면)에 둔 것도 이 회차의 것이며, 코드는 `stmt.set(?,values)`·`rs.get(컬럼명)` 처럼 실제로 없는 메서드를 쓴 스케치다
- [[2024-08-20-Day59]] — 나흘 뒤. 「Dao 기능분리」 세 줄이 **이 층의 책임 경계를 처음 말로 적는다** — 「기존 Dao 소스는 java상에서 JDBC를 활용하여 쿼리문을 전송하고 결과를 리턴 받는다」(맡는 일)·「유지보수 측면에서 Java코드와 SQL쿼리가 혼재되어 불리하다」(안에 섞인 두 가지)·「Mybatis를 사용해서 JDBC API의 역할을 이전하고 소스에서는 자바코드만 작성한다」(떼어 낼 쪽). 그 말이 필요해진 계기가 **저장소 접근 방식을 바꾸려 한 것**이라, 이 회차에서 다섯 메서드의 시그니처는 그대로 두고 몸통만 `sqlSession.delete("UserDao.delete", no)` 로 줄어든다 — 계약이 남고 구현이 갈리는 것이 코드로 확인되는 자리다. 다만 인터페이스와 구현을 나누지 않아 「이전」이 파일을 고쳐 쓰는 형태이고, DAO 위의 서비스 층·트랜잭션 경계의 소속은 이 회차에도 다루지 않는다
