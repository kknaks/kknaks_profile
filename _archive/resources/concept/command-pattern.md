---
type: concept
id: command-pattern
title: 커맨드 패턴 (Command Pattern)
aliases:
  - 커맨드 패턴
  - 커맨드패턴
  - command pattern
  - 명령 패턴
  - Command 패턴
  - 명령 객체
  - 실행 객체
  - 복제 패턴
up:
  - 2024-07-15-Day35
tags:
  - 설계
  - 디자인패턴
  - 객체지향
  - 응집도
---

# 커맨드 패턴 (Command Pattern)

**할 일 하나를 객체 하나로 만들고, 부르는 쪽에는 `execute()` 하나만 남기는 것.** 「무엇을 할지」가 코드의 위치(분기 안)가 아니라 **값**이 되므로, 담아 두고 나중에 부르거나 다른 것으로 바꿔 끼울 수 있다.

## 정의

두 조각뿐이다.

| 조각 | 이 실습에서 |
|---|---|
| **약속** — 실행한다는 것만 말하는 인터페이스 | `interface Command { void execute(String menuName); }` |
| **구현** — 실제로 할 일 하나 | `UserAddCommand` · `BoardListCommand` … |

「할 일 하나」의 **크기**가 이 패턴의 유일한 눈금이고, 실습 프로젝트가 그 눈금을 세 번 옮겼다.

| 회차 | 한 클래스가 담은 것 | 갈래를 고르는 것 |
|---|---|---|
| 7일 전 | 메뉴 그룹 하나 (회원 관련 다섯 기능 + 루프) | 부모의 루프가 부른 `processMenu` 안의 `switch` |
| 6일 전 | 같음 | `Map<String, Command>` 조회 + 그 안의 `switch` |
| **Day35 앞부분** | 메뉴 그룹 하나 (루프는 빼앗기고 기능 다섯만) | 트리의 `MenuItem` + 그 안의 `switch` |
| **Day35 뒷부분** | **기능 하나** | **없다** — 트리의 잎마다 다른 객체 |

**마지막 칸에서 갈래를 고르는 코드가 사라진다.** 「등록인가 목록인가」를 묻는 자리가 없어지는 것이 아니라, **트리를 조립할 때 이미 답이 정해져** 실행 시점에 물을 것이 남지 않는 것이다 → [[dispatch-table]] · [[composite-pattern]]

## 사용 예시

Day35 앞부분의 커맨드는 여전히 기능 다섯을 들고 `switch` 로 갈랐다. 달라진 것은 **어느 기능인지를 매개변수로 받게 된 것**이다.

```java
public interface Command {

  void execute(String menuName);
}
```

```java
public class BoardCommand implements Command {

  private List<Board> boardList;

  public BoardCommand(List<Board> list) {
    this.boardList = list;
  }

  @Override
  public void execute(String menuName) {
    System.out.printf("[%s]\n", menuName);
    switch (menuName) {
      case "등록":
        this.addBoard();
        break;
      case "조회":
        this.viewBoard();
        break;
      /* 목록·변경·삭제 */
    }
  }
  /* 이하 생략 */
}
```

그리고 트리의 잎 다섯 개가 **같은 인스턴스**를 가리킨다.

```java
MenuGroup userMenu = new MenuGroup("회원");
    userMenu.add(new MenuItem("등록", userCommand));
    userMenu.add(new MenuItem("목록", userCommand));
    userMenu.add(new MenuItem("조회", userCommand));
    userMenu.add(new MenuItem("변경", userCommand));
    userMenu.add(new MenuItem("삭제", userCommand));
```

뒷부분은 그 클래스를 기능 단위로 쪼갠다 — 필기의 표현은 「기존의 메서드들을 각 클래스 파일로 분할 하면 된다」다.

```java
public class UserAddCommand implements Command {
  private List<User> userList;

  public UserCommand(List<User> list) {     // ← 클래스 이름과 어긋난다
    this.userList = list;
  }

  @Override
  public void execute(String menuName) {
    User user = new User();
    user.setName(Prompt.input("이름?"));
    user.setEmail(Prompt.input("이메일?"));
    user.setPassword(Prompt.input("암호?"));
    user.setTel(Prompt.input("연락처?"));
    user.setNo(User.getNextSeqNo());
    userList.add(user);
  }
}
```

조립하는 자리에서 `switch` 가 사라진 것이 보인다.

```java
MenuGroup userMenu = new MenuGroup("회원");
userMenu.add(new MenuItem("등록", new UserAddCommand(userList)));
userMenu.add(new MenuItem("목록", new UserListCommand(userList)));
userMenu.add(new MenuItem("조회", new UserViewCommand(userList)));
userMenu.add(new MenuItem("변경", new UserUpdateCommand(userList)));
userMenu.add(new MenuItem("삭제", new UserDeleteCommand(userList)));
mainMenu.add(userMenu);

MenuGroup projectMenu = new MenuGroup("프로젝트");
ProjectMemberHandler memberHandler = new ProjectMemberHandler(userList);
projectMenu.add(new MenuItem("등록", new ProjectAddCommand(projectList, memberHandler)));
projectMenu.add(new MenuItem("목록", new ProjectListCommand(projectList)));
/* 조회·변경·삭제 */
```

**프로젝트 쪽 두 줄이 쪼갠 값을 가장 잘 보여 준다.** 쪼개기 전 `ProjectCommand(projectList, userList)` 는 다섯 기능 중 **둘**(등록·변경)만 회원 목록을 쓰는데도 회원 목록을 받아야 했다. 쪼갠 뒤에는 `ProjectAddCommand(projectList, memberHandler)` 와 `ProjectListCommand(projectList)` 로 갈리고, **생성자만 읽으면 그 기능이 무엇에 의존하는지 안다** → [[dependency-injection]] · [[interface-segregation-principle]]

## 왜 중요한가

**메뉴 제목이 열쇠에서 라벨로 내려온다.** 쪼개기 전에는 `new MenuItem("등록", userCommand)` 의 `"등록"` 과 `UserCommand` 안의 `case "등록":` 이 **글자까지 같아야** 동작했고, 컴파일러는 그 둘이 짝이라는 것을 모른다. 6일 전 회차에서 표의 키와 명령의 제목이 실제로 어긋났던 것과 같은 종류의 위험이다. 쪼갠 뒤에는 그 문자열을 읽는 코드가 **화면 출력밖에 없다** — 「등록」을 「추가」로 바꿔도 깨지는 것이 없다. **문자열이 동작을 고르는 일에서 손을 떼는 것**이 이 단계에서 실제로 얻는 안전이다 → [[dispatch-table]] · [[literal]]

**기능을 더하는 일이 파일을 만드는 일이 된다.** 필기가 이유로 적은 세 줄 중 맞는 것은 이것이다 — 「MenuItem에 새로운 메뉴가 추가되면 userCommand 전체를 수정해야한다」. 쪼갠 뒤 「회원 검색」을 더하는 일은 `UserSearchCommand` 를 새로 쓰고 트리에 한 줄 넣는 것이고, **기존 클래스는 한 글자도 열지 않는다** → [[open-closed-principle]]

**한 클래스가 다루는 데이터가 좁아진다.** 다섯 기능이 한 클래스에 있으면 필드는 그 다섯의 **합집합**이고, 어느 기능이 어느 필드를 만지는지 읽어 봐야 안다. 하나씩 쪼개면 필드가 그 기능이 쓰는 것만 남는다 → [[cohesion]] · [[coupling]]

**「할 일」이 값이 되면 붙일 수 있는 곳이 늘어난다.** 이 회차는 트리의 잎에 붙였지만 같은 객체를 목록에 쌓으면 실행 내역이 되고, 뒤에서부터 꺼내면 되돌리기가 된다. 6일 전 회차는 그것을 맵의 값으로 담았다 — **담는 통을 바꿔도 커맨드는 그대로**라는 것이 이 패턴이 하는 일이다 → [[stack]] · [[dispatch-table]]

## 경계와 오해

- **「복제 패턴」이라는 이름이 일어난 일과 반대다** — 필기의 장 제목이 「Command 복제 패턴」이고 절 제목이 「복제패턴의 필요성」·「복제패턴의 구현」인데, **복제(clone)는 이 작업과 아무 관계가 없다.** 객체를 베끼는 패턴은 프로토타입 패턴이고 그것은 `clone()`·복사 생성자의 세계다. 여기서 일어난 것은 **한 클래스를 기능 단위로 쪼갠 것**이고, 쪼개진 것들은 서로 닮은 껍데기를 가졌을 뿐 **내용이 전부 다르다.** 「복제」로 기억하면 「그럼 무엇을 복제했나」에 답할 수 없다 — 정확한 이름은 커맨드 패턴이고, 쪼개는 근거는 단일 책임이다 → [[object-cloning]] · [[solid-principles]]
- **「command의 전체를 호출하는 것은 비 효율적이다」는 사실이 아니다** — 필기가 쪼개는 첫 이유로 적었는데, `userCommand.execute("등록")` 은 **메서드 하나를 부르고 `switch` 가 갈래 하나를 고른다.** 다섯 기능이 함께 실행되는 것도, 안 쓰는 코드가 메모리에 더 올라가는 것도 아니다. 실행 시간으로 재면 쪼개기 전과 후가 같고, `switch` 한 번이 없어진 만큼이 전부다. **문제는 성능이 아니라 변경과 응집이다** — 다섯 기능이 한 파일에 있으면 하나를 고치러 열 때 다섯이 보이고, 필드는 다섯의 합집합이며, 잎 다섯이 같은 인스턴스를 공유한다. 「비효율」로 기억하면 **정말로 느려지는 종류의 문제와 구분되지 않는다** → [[cohesion]]
- **커맨드 패턴 ≠ 분기 테이블** — 6일 전 회차의 노트가 이미 갈라 둔 구분이고 Day35 가 그것을 증명한다. 커맨드는 **할 일을 객체로 만드는 것**이고 표는 **그 객체를 키로 찾는 것**이다. Day35 는 `Map` 을 버렸는데도 커맨드는 그대로 남았고, 오히려 더 잘게 쪼개졌다 — **찾는 방법이 바뀌어도 실행할 것의 모양은 바뀌지 않는다** → [[dispatch-table]]
- **`execute(String menuName)` 의 인자가 쪼갠 뒤 쓸 데가 없어진다** — 그 매개변수는 「어느 기능인가」를 알려 주기 위해 생긴 것이고, 클래스가 곧 기능이 된 뒤에는 갈래를 고를 필요가 없다. `UserAddCommand.execute` 는 인자를 **한 번도 읽지 않는다.** 그런데 약속에 남아 있으므로 구현 전부가 계속 받는다 — 6일 전 `execute(Stack menuPath)` 가 스택을 안 쓰는 형제들에게까지 번졌던 것과 **같은 자리의 반복**이다 → [[interface-segregation-principle]] · [[parameter-and-argument]]
- **그래서 화면의 제목 줄이 조용히 사라진다** — 쪼개기 전 `BoardCommand.execute` 의 첫 줄은 `System.out.printf("[%s]\n", menuName);` 였다. 쪼갠 뒤의 `UserAddCommand.execute` 에는 그 줄이 없다. 인자를 안 쓴다는 것은 **그 인자로 하던 일도 함께 없어졌다**는 뜻이고, 실행하면 `[등록]` 머리말 없이 곧바로 「이름?」이 뜬다. 기능이 깨진 것이 아니라 출력이 한 줄 줄어든 것이라 **테스트도 컴파일러도 잡지 않는다** — 필기에 이 변화가 적혀 있지 않다 → [[format-string]]
- **`UserAddCommand` 는 컴파일되지 않는다 — 생성자 이름이 클래스 이름과 다르다** — `public class UserAddCommand` 안에 `public UserCommand(List<User> list)` 가 있다. 쪼개면서 클래스 이름만 바꾸고 생성자를 안 바꾼 자리다. 자바에서 **클래스 이름과 다른 이름은 생성자가 아니라 메서드**이고, `public UserCommand(...)` 는 반환 타입이 없으므로 「invalid method declaration; return type required」로 걸린다. 설령 반환 타입을 붙여 통과시켜도 그 클래스에는 선언된 생성자가 없어 **기본 생성자만 생기고** `new UserAddCommand(userList)` 가 다시 컴파일 오류다. 어느 길로 가도 `userList` 가 채워지지 않으므로 **동작으로는 `userList.add(user)` 에서 `NullPointerException`** 이 목적지다. 「동일 한 방법으로 클래스를 나눈다」로 열다섯 개를 같은 손놀림으로 만들 참이었으므로 **같은 실수가 열다섯 번 복사될 자리**이기도 하다 → [[constructor]] · [[default-initialization]]
- **클래스가 다섯 배로 늘어나는 것이 이 결정의 대가다** — 도메인 셋 × 기능 다섯 = 열다섯 개에 도움말·명령내역까지 열일곱 개가 되고, 그 전에는 다섯 개였다. **파일을 열어 읽을 때는 좁아지고 전체를 훑을 때는 넓어진다.** 필기는 쪼개는 이유만 적고 이 비용을 적지 않았다. 기능이 두세 줄이고 서로 거의 같다면 쪼개지 않는 편이 낫다는 판단도 가능한 자리다 → [[refactoring]]
- **쪼개도 데이터는 계속 공유된다 — 그게 맞다** — `UserAddCommand` 와 `UserListCommand` 가 **같은 `userList` 참조**를 받는다. 넣는 것과 읽는 것이 다른 목록을 보면 프로그램이 성립하지 않으므로 이것은 쪼개기의 예외가 아니라 전제다. **쪼개진 것은 동작이고 상태는 여전히 하나**이며, 그 하나를 `App` 의 생성자가 만들어 나눠 준다 → [[dependency-injection]] · [[object-reference]]
- **잎마다 인스턴스를 따로 만드는 것이 필수는 아니다** — 쪼갠 커맨드들은 상태를 바꾸지 않으므로 하나씩 만들어 돌려 써도 된다. 쪼개기 전에 잎 다섯이 `userCommand` 하나를 공유한 것도 그래서 문제가 없었다. **인스턴스를 몇 개 만드는가와 클래스를 몇 개 만드는가는 다른 결정**이고, 필기가 「비효율」로 묶어 버린 것 안에 이 두 축이 섞여 있다 → [[instance]] · [[singleton-pattern]]
- **커맨드 패턴은 되돌리기를 공짜로 주지 않는다** — 「할 일이 객체」라는 것이 실행 취소의 전제이긴 하지만, 실제로 되돌리려면 `undo()` 가 약속에 있고 각 커맨드가 **되돌릴 정보를 들고** 있어야 한다. 이 `Command` 에는 `execute` 하나뿐이고 `UserAddCommand` 는 무엇을 넣었는지 기억하지 않는다. **패턴을 썼다고 그 패턴으로 흔히 하는 일이 되는 것은 아니다** → [[immutability]]

## 함께 보는 개념

- [[dispatch-table]] — 커맨드 객체를 키로 찾던 앞 단계
- [[composite-pattern]] — 이 커맨드들이 매달리는 구조
- [[interface]] — `execute()` 하나를 담는 약속
- [[cohesion]] — 쪼개는 근거가 되는 축
- [[coupling]] — 쪼개면서 좁아지는 것
- [[open-closed-principle]] — 기능 추가가 파일 추가가 되는 성질
- [[dependency-injection]] — 쪼갠 뒤 생성자가 드러내는 것
- [[interface-segregation-principle]] — 안 쓰는 인자가 약속에 남은 것을 재는 원칙
- [[template-method-pattern]] — 커맨드가 루프를 물려받던 앞 구조
- [[constructor]] — 쪼개다 어긋난 자리
- [[object-cloning]] — 「복제」라는 이름이 실제로 가리키는 것
- [[solid-principles]] — 단일 책임이 사는 곳
- [[switch-statement]] — 쪼개면서 사라진 문법
- [[instance]] — 클래스 수와 구별해야 하는 축

## 출처

- [[2024-07-15-Day35]] — `Command` 의 `execute()` 가 `execute(String menuName)` 로 바뀌어 「어느 기능인가」를 인자로 받게 되고, 같은 회차 뒷부분에서 「기존의 메서드들을 각 클래스 파일로 분할」해 `UserAddCommand`·`UserListCommand`… 로 **기능 하나 = 클래스 하나**까지 내려간다. 그 결과 커맨드 안의 `switch` 와 메뉴 제목-갈래의 문자열 짝이 사라지고, `ProjectAddCommand(projectList, memberHandler)` 처럼 **생성자가 그 기능의 의존을 그대로 드러낸다.** 6일 전 회차의 `AbstractCommand` 는 「역할은 menu에서 수행 하므로 더이상 추상클래스가 필요없다」로 삭제된다. 필기는 이 장을 「Command 복제 패턴」이라 불렀는데 복제는 일어나지 않았고(프로토타입 패턴의 낱말이다), 쪼개는 첫 이유로 적은 「command의 전체를 호출하는 것은 비 효율적이다」도 사실이 아니다 — 실제 이득은 응집과 변경 파급이다. 쪼갠 커맨드가 `menuName` 을 안 쓰게 되면서 `[등록]` 머리말 출력이 조용히 없어졌고, `UserAddCommand` 의 생성자 이름이 `UserCommand` 로 남아 **그대로는 컴파일되지 않는다**
