---
type: concept
id: encapsulation
title: 캡슐화 (Encapsulation)
aliases:
  - 캡슐화
  - encapsulation
  - 정보 은닉
  - information hiding
  - getter
  - setter
  - 접근자 메서드
up:
  - 2024-06-17-Day16
  - 2024-06-18-Day17
  - 2024-06-19-Day18
  - 2024-06-20-Day19
  - 2024-07-03-Day28
  - 2024-08-19-Day58
tags:
  - java
  - 객체지향
  - 설계
  - 유지보수
---

# 캡슐화 (Encapsulation)

필드를 `private` 으로 닫고 **밖에서는 메서드로만** 읽고 쓰게 하는 것. 문법은 접근 지정자와 메서드 두 개지만, 실제로 하는 일은 **상태를 바꿀 수 있는 자리를 세어 한 곳으로 모으는 것**이다.

## 정의

```java
private int kor;

public int getKor() { return this.kor; }          // 읽기

public void setKor(int kor) {
  this.kor = kor;
  this.compute();                                  // 받은 뒤에 딸린 값을 다시 맞춘다
}
```

- **getter** — 값을 읽어 준다
- **setter** — 값을 받고, **그 값에 딸린 것을 같이 손본다**

setter 의 두 번째 줄이 캡슐화의 몸통이다. 대입만 하고 끝나면 `private` 을 붙인 값이 없다 → [[access-modifier]]

## 사용 예시

`Score` 의 필드 여섯 개가 전부 `private` 이 되고 메서드가 그 앞에 선다.

```java
public class Score {
  private String name;
  private int kor;
  private int eng;
  private int math;
  private int sum;
  private float aver;

  public void setName(String name) { this.name = name; }              // compute 를 부르지 않는다
  public void setKor(int kor)  { this.kor = kor;  this.compute(); }
  public void setEng(int eng)  { this.eng = eng;  this.compute(); }
  public void setMath(int math){ this.math = math; this.compute(); }

  public String getName() { return this.name; }
  public int getKor()  { return this.kor; }
  public int getSum()  { return this.sum; }
  public float getAver() { return this.aver; }

  public void compute() {
    this.sum = this.kor + this.eng + this.math;
    this.aver = (float) this.sum / 3;
  }
}
```

**`setSum`·`setAver` 가 없다.** 필드는 여섯 개인데 입구는 넷뿐이다. `sum`·`aver` 는 다른 필드에서 계산되어 나오는 값이라 밖에서 넣을 것이 아니고, 그래서 **읽기만 열려 있다.** 이 비대칭이 캡슐화가 실제로 한 일이다 — 「전부 닫고 전부 다시 열기」가 아니다.

호출부도 따라 바뀐다.

```java
static void printScore(Score s) {
  System.out.printf("%s: %d, %d, %d, %d, %.1f\n", s.getName(), s.getKor(), s.getEng(),
      s.getMath(), s.getSum(), s.getAver());
}
```

### 필드가 배열이면 예고된 구멍이 실제로 열린다

다음 회차의 `Project` 는 필드에 배열을 갖는다. `private` 이고 `final` 이기까지 한데, getter 하나가 그것을 통째로 내준다.

```java
public class Project {
  private final User[] users = new User[10];      // 닫혀 있고 다시 대입도 못 한다
  private int memberSize;

  public User[] getUsers() {
    return users;                                 // 그런데 주소를 그대로 준다
  }

  public void setMemberSize(int memberSize) {
    this.memberSize = memberSize;                 // 개수를 밖에서 정할 수 있다
  }
}
```

받은 쪽은 `private` 필드의 내용을 마음대로 고칠 수 있다.

```java
User[] members = project.getUsers();
members[0] = null;                  // Project 는 아무것도 모른다
```

**`final` 은 「그 변수가 다른 배열을 가리키지 못한다」는 뜻이고 내용은 계속 바뀐다.** 실제로 `addMember` 가 `users[memberSize++] = user` 로 매번 고친다. `private final` 두 개를 다 붙여도 배열 안쪽은 열려 있는 것이다 → [[object-reference]]

`setMemberSize` 는 더 직접적이다. 개수는 `addMember`·`deleteMember` 가 관리하는 파생값인데 setter 가 따로 열려 있어서, 밖에서 `setMemberSize(9)` 를 부르면 **넣지 않은 칸의 `null` 이 팀원으로 세어진다.** Day16 의 `Score` 가 `setSum` 을 두지 않은 것과 정확히 반대되는 선택이다.

같은 클래스가 반대편 답도 갖고 있다. `getMember(int index)` 는 배열이 아니라 **요소 하나**를 돌려주고, `contain(User)` 는 아예 **판정 결과만** 돌려준다.

```java
public User getMember(int index)  { return users[index]; }
public boolean contain(User user) { ... return false; }
```

`viewProject` 가 팀원을 찍을 때 `getUsers()` 대신 `getMemberSize()` + `getMember(i)` 를 쓰는 것이 그 증거다 — **배열을 내줄 필요가 실제로는 없었다.** 열어 둔 통로가 쓰이지 않은 채 남아 있는 상태다 → [[cohesion]]

### 파생값을 밖에서 읽고 더해 다시 넣는다

`Board` 는 필드 넷이 전부 `private` 이고 getter/setter 가 여덟 개 다 열려 있다. IDE 가 만들어 준 모양 그대로다.

```java
public class Board {
  private String title;
  private String content;
  private Date createdDate;
  private int viewCount;
  // getter/setter 여덟 개
}
```

**`setViewCount` 가 Day16 의 `setSum` 자리에 있다.** 조회수는 프로그램이 세는 값이라 밖에서 정할 것이 아닌데 setter 가 열려 있고, 실제로 그 통로로 값이 올라간다.

```java
// BoardCommand.viewBoard — Board 밖에서 읽고, 더하고, 다시 넣는다
board.setViewCount(board.getViewCount() + 1);
```

Day16 의 `Score` 는 `setKor` **안에서** `compute()` 가 파생값을 맞췄다. 여기서는 반대다 — 「조회수를 어떻게 올리나」가 `Board` 가 아니라 부르는 쪽에 있고, `viewBoard` 와 `updateBoard` **두 곳에 같은 한 줄이 복사**돼 있다. `increaseViewCount()` 하나가 있었다면 setter 를 닫을 수 있었고 규칙도 한 곳이었다 → [[cohesion]] · [[read-side-effect]]

그리고 배열 getter 의 구멍이 **다른 타입으로 한 번 더** 나타난다.

```java
public Date getCreatedDate() {
  return createdDate;                 // Date 는 가변 객체다 — 주소가 그대로 나간다
}
```

받은 쪽이 `setTime()` 을 부르면 `private` 필드의 시각이 밖에서 바뀐다. **`Project.getUsers()` 와 같은 문제이고, 필드 타입이 배열이 아니라 라이브러리 클래스라서 더 안 보인다** → [[date-time]] · [[object-reference]]

## 왜 중요한가

**어긋난 상태를 만들 수 없게 된다.** 필드가 `public` 이던 때는 이 한 줄이 통했다.

```java
s1.kor = 50;      // sum 과 aver 는 그대로 → 합계가 거짓이 된다
```

컴파일도 되고 예외도 나지 않는다. **값만 조용히 틀린다.** `setKor` 가 `compute()` 를 부르는 것은 그 창을 닫는 것이고, 그래서 캡슐화는 「감추기」보다 **지켜야 할 관계(`sum == kor + eng + math`)를 지킬 자리를 한 곳으로 모으기**로 읽는 것이 맞다. 필기의 「코드의 기초 데이터를 흔든다」가 그 문제를 가리킨 말이다.

**나중에 고칠 자유가 생긴다.** `sum` 을 필드로 두지 않고 `getSum()` 에서 매번 계산하도록 바꿔도 밖의 코드는 한 줄도 안 바뀐다. 저장 방식이 밖으로 새 나가지 않았기 때문이다. `public` 필드였다면 `s.sum` 을 쓰는 모든 곳을 고쳐야 한다.

**검사를 넣을 자리가 생긴다.** `setKor` 안에 「0 ~ 100 만 받는다」를 넣을 수 있다. 필드 대입에는 그런 것을 끼워 넣을 데가 없다.

## 경계와 오해

- **캡슐화 ≠ 모든 필드에 getter/setter 만들기** — 전 필드에 setter 를 붙이면 통로만 길어진 `public` 필드다. 이 실습이 `setSum` 을 만들지 않은 것이 진짜 예다. 물어야 하는 것은 「이 값을 밖에서 정할 수 있어야 하는가」이고, IDE 가 한 번에 생성해 주기 때문에 그 판단이 통째로 건너뛰어진다.
- **캡슐화 ≠ 읽기 금지** — getter 는 열려 있다. 감추는 것은 **저장 방식과 바꾸는 경로**이지 값 자체가 아니다.
- **setter 마다 `compute()` 를 부르는 것이 규칙은 아니다** — 기준은 **바뀐 값이 파생값에 영향을 주는가**다. `setName` 이 `compute()` 를 부르지 않는 것이 맞다. 규칙으로 외우면 상관없는 계산이 늘고, 기준을 모르면 새 setter 에서 잊는다.
- **`compute()` 가 `public` 인 것은 남은 구멍이다** — 부르는 곳은 생성자와 setter 뿐이므로 `private` 이어도 코드가 그대로 돌아간다. `public` 으로 열려 있으면 「밖에서 언제든 다시 계산해도 된다」는 뜻이 되어, **파생값을 setter 가 책임진다는 약속이 흐려진다.**
- **접근 지정자만으로 캡슐화가 완성되지는 않는다** — 필드가 배열이나 객체면 getter 가 돌려주는 것이 **주소**이므로 받은 쪽이 내용을 고칠 수 있다. `private` 인데 밖에서 바뀌는 것이다. 이 `Score` 는 필드가 전부 기본 타입과 `String` 이라 그 문제를 만나지 않았고, 다음 회차의 `Project.getUsers()` 에서 그대로 열렸다 → [[object-reference]] · [[call-by-value]] · 「사용 예시」
- **`private final` 도 내용은 막지 못한다** — `final` 이 고정하는 것은 **레퍼런스가 가리키는 대상**이고 그 안의 원소는 아니다. `private final User[] users` 에 `addMember` 가 계속 값을 넣는 것이 그 증거다. 「두 개나 붙였으니 안전하다」로 읽으면 배열을 내주는 getter 가 왜 구멍인지 설명되지 않는다 → [[array]]
- **파생값에 setter 를 여는 것이 가장 흔한 되돌림이다** — `Project.setMemberSize` 는 `addMember`·`deleteMember` 가 관리하는 개수를 밖에서 정하게 한다. IDE 가 필드마다 setter 를 만들어 주기 때문에, Day16 에서 `setSum` 을 만들지 않으며 얻은 판단이 다음 실습에서 조용히 사라졌다 → [[array-element-removal]]
- **「하나만 주기」와 「전부 주기」는 다른 결정이다** — `getMember(int index)` 는 요소 하나를, `getUsers()` 는 배열 전체를 준다. 둘이 같이 있으면 뒤쪽이 앞쪽을 무의미하게 만든다. 캡슐화의 실제 질문은 「getter 를 둘까」가 아니라 **「무엇을 돌려줄까」**다 → [[cohesion]]
- **setter 를 아예 두지 않는 선택도 있다** — 생성자에서 다 받고 그 뒤로 못 바꾸게 하면 `compute()` 를 다시 부를 일이 없어져 「잊을 수 있는 단계」자체가 사라진다. 이 필기는 setter 를 두는 쪽을 골랐고, 그 대가로 setter 마다 `compute()` 를 챙겨야 한다 → [[constructor]]
- **파생값 setter 는 한 번 더 열린다** — `Board.setViewCount` 가 `Project.setMemberSize` 와 같은 종류다. 세 회차를 나란히 놓으면 `setSum` 을 만들지 않은 판단이 이어지지 않았다는 것이 보인다. **판단은 한 번 내리는 것으로 남지 않고, IDE 가 기본으로 만들어 주는 쪽이 매번 이긴다.**
- **`getViewCount() + 1` 은 캡슐화를 통과한 상태 변경이다** — 문법은 다 지켰다. `private` 필드를 getter 로 읽고 setter 로 썼다. 그런데 「조회수는 1씩 오른다」는 규칙이 `Board` 밖에 있으므로 **필드를 닫아서 얻으려던 것이 얻어지지 않았다.** 캡슐화를 문법으로 채점하면 통과하고 목적으로 채점하면 실패하는 자리다 → [[cohesion]]
- **가변 객체 필드는 배열과 같은 취급을 받아야 한다** — `Date`·`ArrayList` 처럼 내용을 바꿀 수 있는 객체를 getter 로 내주면 `private` 이 무력해진다. 「배열만 조심하면 된다」로 외우면 `getCreatedDate()` 가 왜 같은 구멍인지 설명되지 않는다. 기준은 타입이 아니라 **받은 쪽이 그 안을 바꿀 수 있는가**다 → [[date-time]]
- **배열 getter 의 구멍을 닫는 방법이 다음 회차에 나온다** — Day19 의 `UserList.toArray()` 는 원본을 주지 않고 유효 개수만큼 새 배열에 옮겨 담아 돌려준다. Day16 에서 예고되고 Day17 에서 열린 그 구멍이 여기서 처음 막힌다. 다만 **막힌 것은 배열 구조뿐**이고 칸에 든 인스턴스는 그대로 공유되므로, `toArray()[0].setName(...)` 은 여전히 원본을 바꾼다 → [[defensive-copy]] · [[object-reference]]
- **식별 번호에 setter 를 여는 것은 파생값 setter 보다 무겁다** — Day19 의 `User.setNo` 는 `public` 이라 밖에서 아무 번호나 다시 넣을 수 있고, 그러면 같은 번호를 가진 회원이 둘 생겨 조회가 앞의 것만 찾는다. `setSum`·`setMemberSize`·`setViewCount` 는 값이 틀리는 문제였지만, 이쪽은 **데이터를 구별할 수 없게 되는 문제**다 → [[surrogate-key]]
- **번호를 밖에서 넣는 것 자체가 열린 자리다** — `addUser` 가 `user.setNo(User.getNextSeqNo())` 를 부른다. 그 한 줄을 잊은 등록은 `no` 가 `0` 인 회원을 만들고 이후 아무 명령도 그 회원에 닿지 못한다. **생성자에서 발급했다면 잊을 단계가 없었다** — Day16 의 「setter 를 아예 두지 않는 선택」과 같은 갈림이 다시 나온 것이고, 이번에도 setter 쪽을 골랐다 → [[constructor]] · [[default-initialization]]
- **`getSeqNo()` 는 getter 가 아니다** — 부를 때마다 값이 바뀌고 부른 것 자체가 상태를 바꾼다. `get` 접두사가 관례일 뿐이라는 것이 이 자리에서 드러나고, 필기도 최종 코드에서 `getNextSeqNo()` 로 이름을 고쳤다 → [[read-side-effect]]
- **캡슐화라는 낱말이 두 가지를 가리킨다 — 상태를 닫는 것과 절차를 감추는 것** — 두 달 뒤 Day58 의 제목이 「JDBC 캡슐화」·「sql구문 캡슐화」인데, 거기에는 `private` 필드도 getter/setter 도 없다. 감춘 것은 **값이 아니라 절차**다(`PreparedStatement` 준비 → `?` 바인딩 → 실행 → 닫기 네 단계를 메서드 하나 뒤로 넣었다). 같은 이름을 쓰는 이유는 뿌리가 같기 때문이다 — **밖에서 알아야 할 것을 줄인다.** 그런데 **묻는 질문이 다르다**: 상태 쪽은 「이 값을 밖에서 정할 수 있어야 하는가」이고(그 답이 `setSum` 을 만들지 않은 것), 절차 쪽은 **「이 절차를 아는 코드가 몇 곳인가」**다. 그리고 결정적으로 **강제 장치가 없다** — 필드는 `private` 이 컴파일러로 막아 주지만, 절차는 감싼 메서드를 안 쓰고 그 옆에서 `con.prepareStatement` 를 직접 불러도 아무도 막지 않는다. 그래서 절차 캡슐화는 「감췄다」가 아니라 **「감싸지 못한 것이 무엇인가」의 목록으로 채점**해야 하고, Day58 의 경우 SQL 문자열·커밋 경계·자동 생성 키 셋이 그 목록에 남았다 → [[sql-session]] · [[access-modifier]] · [[coupling]]
- **Day16 시점의 필기는 이유를 유지보수성으로 적었고, 보름 뒤에 값이 어긋나는 쪽으로 다시 적었다** — Day16 의 "코드의 유지 보수성이 좋아진다"는 결과의 절반이라 「고치기 쉬워진다」로만 기억하면 왜 setter 안에서 `compute()` 를 불러야 하는지가 설명되지 않는다. Day28 의 한 줄이 그 빈자리를 채운다 — 「클래스의 필드 값에 직접적인 접근을 하면 **해당 필드값을 참조하는 결과값도 영향을 받는다**」. 이것이 `s1.kor = 50` 이 `sum` 을 거짓으로 만드는 그 문제이고, **네 회차를 실습한 뒤에야 이유가 값의 정합성으로 다시 쓰였다.** 이어지는 「변경에 따른 추가적인 필드 변경 메서드를 추가할 수 있다」도 `setKor` 안의 `compute()` 를 가리킨다 — 문법이 아니라 **그 안에 무엇을 같이 넣을 수 있는가**를 캡슐화의 값으로 본 것이다.

## 함께 보는 개념

- [[access-modifier]] — 캡슐화를 만드는 문법
- [[class]] — 데이터와 기능을 한 이름 안에 두는 단위
- [[constructor]] — 필드를 닫을 수 있게 해 주는 전제
- [[this-reference]] — 매개변수와 필드를 가려 쓰는 자리
- [[method]] — 필드 앞에 서는 것
- [[object-reference]] — getter 가 주소를 돌려줄 때 새는 자리
- [[package]] — 이 실습이 캡슐화를 만난 계기
- [[array]] — `final` 이 내용을 막지 못하는 필드 타입
- [[cohesion]] — 배열을 내주지 않고 물어보게 만드는 다음 단계
- [[crud]] — getter/setter 가 실제로 쓰이는 자리
- [[date-time]] — 가변 객체를 필드로 갖는 쪽
- [[read-side-effect]] — 파생값이 밖에서 올라가는 자리
- [[defensive-copy]] — 배열 getter 의 구멍을 닫는 방법
- [[surrogate-key]] — setter 를 열면 데이터를 구별할 수 없게 되는 필드
- [[singleton-pattern]] — 필드가 아니라 생성 자체를 감추는 쪽
- [[sql-session]] — 같은 낱말이 절차를 감추는 쪽에 쓰인 자리
- [[coupling]] — 절차 캡슐화를 채점하는 축

## 출처

- [[2024-06-17-Day16]] — `Score` 의 필드를 전부 `private` 으로 닫고 getter/setter 로만 접근하게 바꾸면서, setter 에서 값을 다시 받으면 합계·평균을 `compute()` 로 다시 계산해야 한다는 것을 실습으로 배웠다. `sum`·`aver` 에는 setter 를 두지 않은 것도 이 실습이다
- [[2024-06-18-Day17]] — `User`·`Project` 의 필드를 전부 `private` 으로 닫고 getter/setter 를 세워 CRUD 가 그것만으로 동작하게 만들었다. 동시에 `Project` 는 `private final User[] users` 를 `getUsers()` 로 통째로 내주고 파생값인 개수에 `setMemberSize` 를 열어, Day16 에서 예고된 배열 getter 의 구멍이 실제로 열린 자리가 되었다
- [[2024-06-19-Day18]] — `Board` 의 네 필드를 닫고 getter/setter 여덟 개를 다 열면서, 파생값인 조회수에도 setter 가 열려 `BoardCommand` 가 `setViewCount(getViewCount() + 1)` 로 밖에서 값을 올리게 되었다. 가변 객체인 `Date` 를 `getCreatedDate()` 로 내주는 것이 배열 getter 와 같은 구멍이라는 것도 이 자리다
- [[2024-06-20-Day19]] — `UserList.toArray()` 가 원본 배열 대신 사본을 돌려주며 세 회차에 걸쳐 열려 있던 배열 getter 의 구멍이 처음 닫혔다. 동시에 식별 번호 `no` 에 `public` setter 가 열리고 번호 발급을 `addUser` 가 밖에서 챙기게 되어, 「닫을 것을 열어 두는」 패턴이 파생값에서 식별자로 옮겨 간 자리가 되었다
- [[2024-07-03-Day28]] — 네 회차의 실습을 거친 뒤 캡슐화의 이유를 **원칙으로 다시 적은** 자리다. 「클래스의 필드 값에 직접적인 접근을 하면 해당 필드값을 참조하는 결과값도 영향을 받는다」가 Day16 의 `sum`·`aver` 문제를 일반화한 문장이고, 「변경에 따른 추가적인 필드 변경 메서드를 추가할 수 있다」가 setter 안의 `compute()` 를 가리킨다. Day16 이 이유를 유지보수성으로 적었던 것과 강조점이 갈린다. 같은 장의 싱글톤 패턴은 감추는 대상을 필드에서 **생성**으로 옮긴 첫 코드다
- [[2024-08-19-Day58]] — 두 달 뒤. 이 낱말이 **상태가 아니라 절차**에 쓰인 첫 자리다. 제목이 「JDBC 캡슐화」이고 요약이 「sql구문 캡슐화 하기」인데 코드에는 `private` 필드도 접근자도 없고, `PreparedStatement` 를 준비하고 `?` 를 채우고 실행하고 닫는 네 단계를 `insert(String sql, Object... values)` 하나 뒤로 넣은 것이 전부다. Day16~28 이 「이 값을 밖에서 정할 수 있어야 하는가」를 물었던 자리에서 이 회차는 「이 절차를 아는 코드가 몇 곳인가」를 묻는다. 필기는 두 뜻을 가르지 않았고 무엇이 감싸지지 않았는지도 적지 않았다 — 절차 쪽에는 `private` 같은 강제 장치가 없어 감싼 메서드를 우회할 수 있다는 것, 그래서 SQL 문자열·커밋 경계·자동 생성 키가 밖에 남았다는 것은 이 노트와 [[sql-session]] 이 채운다
