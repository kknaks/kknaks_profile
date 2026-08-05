---
type: concept
id: cohesion
title: 응집도 (Cohesion)
aliases:
  - 응집도
  - cohesion
  - high cohesion
  - 책임 배치
  - information expert
up:
  - 2024-06-18-Day17
  - 2024-06-19-Day18
  - 2024-06-20-Day19
  - 2024-07-08-Day30
tags:
  - 설계
  - 객체지향
  - 유지보수
  - 리팩터링
---

# 응집도 (Cohesion)

한 클래스가 **자기가 가진 데이터에 대한 판단과 조작을 자기 안에 두는** 정도. 데이터는 여기 있고 그것을 다루는 코드는 저기 있는 상태를 없애는 일이다.

## 정의

기준은 하나다 — **어떤 필드를 읽어야 하는 코드는 그 필드를 가진 클래스에 둔다.**

| 코드 | 읽어야 하는 필드 | 살아야 하는 곳 |
|---|---|---|
| `contain(User)` 팀원 중복 검사 | `Project.users` · `memberSize` | `Project` |
| `addMember` · `deleteMember` · `getMember` | 같음 | `Project` |
| `findByNo(int)` 회원 조회 | `UserCommand.users` · `userLength` | `UserCommand` |

그래서 밖에서는 **데이터를 달라고 하지 않고 물어본다.**

```java
if (project.contain(user)) { ... }        // 배열을 받아 직접 뒤지지 않는다
project.addMember(user);
```

이것은 [[encapsulation]] 과 축이 다르다. 캡슐화는 **필드를 어떻게 여는가**이고, 응집도는 **그 필드를 쓰는 코드가 어디 사는가**다. `private` 으로 닫아 놓고 `getUsers()` 로 배열을 내주면 캡슐화 문법은 지켰지만 판단은 여전히 밖에 있다.

## 사용 예시

이 필기 안에서 코드가 **한 번 옮겨 간다.** 2.2 의 초안은 `contain` 을 `ProjectCommand` 에 두려 했다.

```java
//ProjectCommand.java
public static boolean contain(User user){
	for (int i = 0; i < memberLength; i++){
    	User member = users[i]
    	if(user.getName().equals(member.getName()){
        	return true;
		}
   	 }
    return false;
}
```

`users` 도 `memberLength` 도 `ProjectCommand` 에는 없는 이름이다 — `Project` 의 필드다. **그 자리에서는 컴파일되지 않는다.** 최종 코드에서 이 메서드는 `Project` 안으로 들어갔다.

```java
public class Project {
  private final User[] users = new User[10];
  private int memberSize;

  public boolean contain(User user) {
    for (int i = 0; i < memberSize; i++) {
      User member = users[i];
      if (user.getName().equals(member.getName())) {
        return true;
      }
    }
    return false;
  }

  public void addMember(User user) { users[memberSize++] = user; }

  public User getMember(int index) { return users[index]; }

  public void deleteMember(int index) { ... }
}
```

그러자 `ProjectCommand` 의 팀원 추가 루프에는 **자기가 모르는 것을 묻는 코드**만 남는다.

```java
static void addMembers(Project project) {
  while (true) {
    int userNo = Prompt.inputInt("추가할 팀원 번호?(종료:0)");
    if (userNo == 0) break;
    User user = UserCommand.findByNo(userNo);          // 회원 배열은 UserCommand 것이다
    if (user == null) {
      System.out.println("없는 팀원입니다.");
      continue;
    }
    if (project.contain(user)) {                      // 팀원 배열은 Project 것이다
      System.out.printf("'%s'은 현재 팀원입니다.", user.getName());
      continue;
    }
    project.addMember(user);
  }
}
```

**`ProjectCommand` 는 배열 두 개를 다루면서 그중 어느 것도 직접 만지지 않는다.** 하는 일은 입력받고 순서를 정하는 것뿐이다.

`findByNo` 가 새로 생긴 것도 같은 이유다. 회원 배열은 `UserCommand` 의 `private static` 필드라 밖에서 볼 수 없으니, **찾는 일을 소유자에게 맡긴다** → [[access-modifier]]

```java
//UserCommand.java
public static User findByNo(int userNo) {
  if (userNo < 1 || userNo > userLength) {
    return null;
  }
  return users[userNo - 1];
}
```

### 다음 회차의 Board 는 다시 데이터만 갖는다

게시판을 만들 때 `Board` 에는 getter/setter 여덟 개 말고 아무 메서드도 없다. 그런데 `viewCount` 를 다루는 판단은 생겼다 — **그 판단이 클래스 밖에 있다.**

```java
// BoardCommand.viewBoard
Board board = boards[boardNo - 1];
board.setViewCount(board.getViewCount() + 1);      // 조회수를 올리는 규칙이 여기 있다

// BoardCommand.updateBoard
board.setViewCount(board.getViewCount() + 1);      // 같은 한 줄이 한 번 더
```

`viewCount` 를 읽어야 하는 코드가 `viewCount` 를 가진 클래스 밖에 있고, 그래서 **같은 줄이 두 곳에 복사됐다.** 전날 `contain` 을 `Project` 로 옮긴 것과 정확히 반대 방향이다.

```java
// 이 판단이 Board 안에 있었다면
public void increaseViewCount() {
  this.viewCount++;
}
```

이렇게 두면 `setViewCount` 를 닫을 수 있고, 「조회수는 1씩 오른다」·「누구의 조회는 세지 않는다」 같은 규칙이 생길 때 고칠 자리가 하나다 → [[encapsulation]] · [[read-side-effect]]

**전날 얻은 판단이 다음 날 자동으로 적용되지 않았다.** `Project` 는 팀원 배열이라 `private` 이 막아 주며 컴파일 오류로 밀어붙였는데, `viewCount` 는 `int` 이고 setter 가 열려 있어 **밖에서 다루는 코드가 그냥 컴파일된다.** 응집도를 지켜 주던 것이 판단이 아니라 문법의 저항이었다는 것이 여기서 드러난다.

### 그 다음 회차에 이름이 붙고, 이번에는 클래스가 쪼개진다

앞의 두 회차는 **메서드를 어느 클래스에 둘까**였다. 세 번째 회차에서 이 기준에 이름이 생긴다 — GRASP 의 **High Cohesion** 이고, 적용 대상은 메서드 하나가 아니라 **클래스 전체**다 → [[grasp]]

진단이 먼저 나온다 — 「기존 command class의 구조 : 서브메뉴들의 흐름제어 + 데이터보관처리」. 필드 목록과 메서드 목록을 나란히 놓으면 두 무리가 보인다.

```java
public class ProjectCommand {
  //데이터보관 필드
  private static final Project[] projects = new Project[MAX_SIZE];
  private static int projectLength = 0;

  //UI처리 메서드
  private static void addProject() {}
  private static void listProject() {}
  ...
  //데이터처리 메서드
  private static Project findByNo(int projectNo) {}
  private static int indexOf(Project project) {}
}
```

**「데이터처리」로 묶인 둘만 배열을 읽는다.** 나머지는 입력을 받고 화면을 찍는다. 이 기준이 곧 자르는 선이다.

```java
public class UserList {                                    // 배열을 읽는 것만 모았다
  private static final User[] users = new User[MAX_SIZE];
  private static int userLength = 0;

  public static void add(User user)      { users[userLength++] = user; }
  public static User delete(int userNo)  { ... }
  public static User[] toArray()         { ... }
  public static User findByNo(int userNo) { ... }
  public static int indexOf(User user)   { ... }
}
```

```java
public class UserCommand {                                 // 배열 이름이 하나도 없다
  private static void addUser() {
    User user = new User();
    user.setName(Prompt.input("이름?"));
    ...
    user.setNo(User.getNextSeqNo());
    UserList.add(user);                                    // 넣는 일은 소유자에게
  }

  private static void listUser() {
    for (User user : UserList.toArray()) { ... }            // 훑는 일도 소유자에게
  }

  private static void deleteUser() {
    User deletedUser = UserList.delete(userNo);            // 지우는 일도 소유자에게
    if (deletedUser != null) { ... }
  }
}
```

**Day19 시점에 `users`·`userLength`·`MAX_SIZE` 라는 이름이 `UserCommand` 에서 완전히 사라졌다.** 전날 `Project` 에 대해 한 일을 이번에는 회원 목록 자체에 한 것이고, 그래서 이 회차가 앞의 두 회차와 갈리는 지점은 **한 클래스가 아무 데이터도 갖지 않게 되었다**는 것이다.

**단 이 상태는 18일 뒤에 다시 바뀐다.** 리팩터링 회차의 `UserCommand` 는 `LinkedList userList = new LinkedList();` 를 **자기 필드로 다시 갖는다.** 되돌아간 것처럼 보이지만 옮겨진 것은 소유이고 코드는 아니다 — 그 사이에 범용 자료구조(`ArrayList`·`LinkedList`)가 만들어졌으므로, 목록을 다루는 코드는 여전히 `UserCommand` 밖에 있고 `MAX_SIZE`·개수 변수·배열 당기기도 그쪽에 있다. **`UserList` 라는 도메인에 없는 클래스가 필요했던 이유가 사라진 것**이고, 그래서 Pure Fabrication 이 회수되었다 → [[grasp]] · [[dynamic-array]]

바뀐 것은 위치만이 아니다. `delete` 가 **지운 회원을 돌려준다.**

```java
public static User delete(int userNo) {
  User deleteUser = findByNo(userNo);
  if (deleteUser == null) {
    return null;                                    // 없었다
  }
  ...
  return deleteUser;                                // 지운 것을 알려 준다
}
```

```java
User deletedUser = UserList.delete(userNo);
if (deletedUser != null) {
  System.out.printf("'%s' 회원을 삭제 했습니다.\n", deletedUser.getName());
} else {
  System.out.println("없는 회원입니다.");
}
```

**성공/실패 판정도 소유자가 하고 UI 는 그 결과를 문장으로 바꾸기만 한다.** 전날의 `deleteUser` 는 찾고, 검사하고, 인덱스를 구하고, 당기고, 안내까지 다 했다 — 다섯 단계가 두 클래스로 갈렸다 → [[method]]

그리고 이 분리가 가능해진 조건이 두 개 있는데 둘 다 같은 회차에 생겼다. 목록을 사본으로 내주는 `toArray()` 가 개수 변수를 안에 남겨 주었고([[defensive-copy]]), 번호가 데이터 안으로 들어가서 UI 가 인덱스를 몰라도 되게 되었다([[surrogate-key]]). **응집도만 따로 올릴 수는 없었다.**

### 네 번째 회차는 데이터가 아니라 흐름을 옮긴다

**18일 뒤 리팩터링 회차가 같은 이름(High Cohesion)으로 다른 종류의 것을 옮긴다.** 진단과 처방이 두 줄이다 — 「App에 subMenus에서 수행하는 기능들 혼재」 / 「APP에 있는 subMenus들의 기능을 각 Command 기능으로 옮기기」.

앞 세 회차의 기준은 **「어떤 필드를 읽는가」**였다. 여기서 옮겨진 것은 필드를 읽는 코드가 아니라 **서브메뉴의 흐름 제어 전체**다.

| `App` 에 남은 것 | 각 `Command` 로 간 것 |
|---|---|
| `mainMenus` 배열 | 자기 메뉴 목록 (`menus`) |
| Command 넷을 만드는 일 | 자기 서브메뉴 루프 (`execute()`) |
| 메인 메뉴의 루프와 번호 검증 | 자기 번호 검증과 갈래 (`processMenu`) |

기준을 다시 쓰면 문장 모양은 앞 회차들과 같다 — **「그 메뉴에 대해 아는 것은 그 메뉴의 `Command` 가 갖는다.」** 단위가 「필드」에서 「메뉴」로 옮겨졌을 뿐이고, 그래서 Information Expert 가 데이터에만 걸리는 지침이 아니라는 것이 여기서 드러난다 → [[grasp]] · [[command-loop]]

**그리고 이번에는 대가가 다른 축에서 나온다.** Day19 는 클래스를 둘로 갈라 **결합**이 늘었는데, 이번에는 같은 코드가 **네 벌**이 되었다. 필기가 그것을 바로 다음 절에서 관찰한다 — 「응집력을 높인 결과 각 Command 클래스에 동일한 코드 생성」. 나눈 뒤에 올려야 할 것이 남는 것이고, **응집도 정리는 그 자체로 끝나는 작업이 아니다** → [[generalization]] · [[refactoring]]

## 왜 중요한가

**고칠 때 열어야 하는 파일 수가 달라진다.** 팀원 저장을 배열에서 다른 것으로 바꾸는 일을 생각하면, 지금 구조에서는 `Project` 하나만 고치면 된다. `ProjectCommand` 가 `project.getUsers()` 로 배열을 받아 직접 뒤지고 있었다면 그 코드까지 같이 고쳐야 한다. **저장 방식을 아는 곳의 개수가 곧 변경 비용**이다.

**같은 판단이 여러 곳에 복사되는 것을 막는다.** 「이미 팀원인가」를 `addProject` 와 `updateProject` 가 둘 다 물어야 하는데 `Project.contain` 이 하나 있으면 두 곳이 그것을 부른다. 밖에서 각자 배열을 뒤졌다면 판정 기준(이름으로 비교한다)이 두 벌이 되고, 한쪽만 고치는 날 어긋난다 → [[method]]

**그리고 컴파일러가 이 규칙을 어느 정도 강제한다.** 이 필기의 초안이 그 증거다 — `contain` 을 남의 클래스에 두려 하자 이름이 해석되지 않았다. 필드를 `private` 으로 닫아 두면 「그 데이터를 쓰는 코드가 어디 있어야 하는가」가 **오류로 드러난다.** 설계 감각으로 고르는 것이 아니라 코드가 먼저 알려 주는 것이다.

## 경계와 오해

- **응집도 ≠ 캡슐화** — 캡슐화는 필드에 `private` 을 붙이고 메서드로 여는 문법이고, 응집도는 **메서드를 어느 클래스에 두는가**다. 이 `Project` 는 필드가 `private` 인데 `getUsers()` 로 배열 전체를 내주므로 캡슐화 쪽에 구멍이 남아 있다 → [[encapsulation]]
- **한 클래스에 다 넣는 것이 높은 응집도가 아니다** — 기준은 크기가 아니라 **읽는 데이터가 같은가**다. `Project` 에 화면 출력과 입력까지 넣으면 필드와 무관한 코드가 들어와 응집도가 오히려 떨어진다. 이 필기가 `Prompt` 를 `util` 패키지에 따로 둔 것이 그 선이다 → [[package]]
- **`ProjectCommand` 는 Day17 시점에 응집도가 높은 클래스가 아니었다** — 프로젝트 배열을 갖고 있으면서 입력·출력·흐름 제어까지 했다. 그때 정리된 것은 데이터를 가진 `vo` 쪽뿐이고 `command` 쪽은 그대로였는데, **이틀 뒤 회차에서 그쪽이 쪼개진다.** 「한 번의 리팩터링이 모든 클래스를 정리하지는 않는다」가 맞고, 남은 것을 정리하려면 **기준에 이름이 붙어야** 했다 → [[static-member]] · [[grasp]]
- **클래스를 쪼개는 것과 메서드를 옮기는 것은 규모만 다른 것이 아니다** — 메서드 이동은 컴파일러가 「그 이름이 여기 없다」로 밀어 주지만, 두 역할이 한 클래스에 **문법적으로 아무 문제 없이** 같이 살 수 있다. `ProjectCommand` 는 배열과 화면 코드를 함께 가져도 끝까지 컴파일된다. 그래서 이 판단은 **오류가 알려 주지 않고 목록을 보고 세어야** 나온다.
- **쪼갠 뒤에는 `private` 의 뜻이 바뀐다** — 필기 「High Cohesion」 절의 `ProjectList` 초안은 `findByNo`·`indexOf` 를 `private static` 으로 그대로 옮겼는데, 한 클래스 안에서 충분했던 것이 밖에서 부를 수 없는 코드가 된다. 「클래스 분리하기」 절의 `UserList` 에서 `public static` 이 되었다. **응집도를 올리면 캡슐화 경계를 다시 그려야 한다** → [[access-modifier]]
- **`UserList` 는 도메인에 없는 클래스다** — 회원·프로젝트·게시글은 현실에 대응물이 있지만 「회원목록」은 설계 문제를 풀려고 만든 것이다. 응집도를 올리는 일이 **새 클래스를 만들어 내는 것**으로 끝날 수 있다는 것이고, 「기존 클래스 중 어디에 둘까」만 물으면 이 답이 나오지 않는다 → [[grasp]]
- **`UserList` 가 `command` 패키지에 있다** — 역할을 갈라 클래스를 둘로 만들었는데 패키지는 그대로다. 데이터 보관 클래스가 `command` 아래 있으면 **디렉토리를 보고는 갈라진 것을 알 수 없다.** 응집도 정리와 패키지 정리가 따로 일어난 자리다 → [[package]]
- **결합은 줄지 않고 늘었다** — `UserCommand` 가 이제 `UserList` 라는 이름과 그 메서드 다섯 개를 안다. GRASP 목록의 Low Coupling 과 반대 방향이고, **응집도를 올린 대가**다. 「응집도가 높아졌으니 좋아졌다」로만 읽으면 이 대가가 세어지지 않는다. **그 대가를 세는 법과 줄이는 법은 보름 뒤 인터페이스 회차에서 온다** — 아는 대상을 클래스 이름에서 약속으로 바꾸는 것이고, 그때까지 이 축은 이름만 있는 상태다 → [[grasp]] · [[coupling]]
- **필기의 `contain` 초안은 그 자리에서 컴파일되지 않는다** — `//ProjectCommand.java` 라고 적혀 있지만 `users`·`memberLength` 는 `Project` 의 필드다. `memberLength` 라는 이름은 어디에도 없고 실제 필드는 `memberSize` 다. 최종 코드에서 `Project` 로 옮겨지며 둘 다 맞춰졌다.
- **`findByNo(userNo)` 초안은 매개변수 타입이 빠져 있다** — `public static User findByNo(userNo)` 로 적혀 있는데 Java 는 타입을 생략할 수 없다. `getMember` 의 `return users[inx];` 도 `index` 의 오기다.
- **`getMember(index)` 와 `getUsers()` 는 다른 결정이다** — 앞은 「하나 달라」이고 뒤는 「배열을 줘」다. 뒤가 있으면 앞을 만든 이유가 없어진다. 둘이 같이 있는 것은 앞 단계 코드가 남은 것이다 → [[object-reference]]
- **로직을 옮기는 것은 책임을 옮기는 것이다** — 「같은 팀원인지 이름으로 판정한다」가 `Project` 안으로 들어갔다. 그 규칙이 틀리면(동명이인) 틀린 자리도 `Project` 다. 그래서 어디로 옮길지 고르는 일이 곧 설계이고, 옮기고 나면 **그 클래스가 도메인 규칙의 소유자**가 된다 → [[string-comparison]]
- **컴파일러의 강제는 필드 타입에 달려 있다** — `private` 이 막아 주는 것은 **이름이 해석되지 않을 때**뿐이다. `Board.viewCount` 처럼 setter 가 열린 기본 타입 필드는 밖에서 읽고 더해 다시 넣는 코드가 오류 없이 컴파일된다. 「컴파일러가 알려 준다」를 규칙으로 삼으면 **막아 주지 않는 경우를 못 본다** → [[access-modifier]]
- **메서드가 getter/setter 뿐인 클래스는 응집도 판정이 유보된 상태다** — 「데이터만 담는 클래스니 옳다」가 아니라, 그 데이터를 다루는 판단이 아직 없거나 밖에 있다는 뜻이다. `Board` 는 두 번째다 — 조회수를 올리는 판단이 `BoardCommand` 에 두 번 복사돼 있다.
- **응집도를 올려서 늘어나는 것이 결합만은 아니다** — Day19 는 한 클래스를 데이터/UI 로 갈라 **결합**이 늘었고, 18일 뒤 회차는 흐름 제어를 메뉴별로 갈라 **중복**이 늘었다. 나누는 기준이 「역할이 둘」이면 갈린 둘이 서로를 부르게 되고, 「대상이 넷」이면 같은 코드가 넷이 된다. **무엇을 기준으로 나누는가가 어떤 대가를 치를지까지 정한다** → [[coupling]] · [[generalization]]
- **필기의 정의는 실제로 쓴 기준보다 느슨하다** — 리팩터링 회차는 High Cohesion 을 「내부 요소들이 얼마나 밀접하게 관련되어 있는지를 나타내는 개념」·「관련성 높은 기능들의 집합」으로 적었는데, **그 문장으로는 어디를 자를지 나오지 않는다.** 실제로 선을 준 것은 Day19 의 「무엇을 읽는가」와 이번의 「어느 메뉴의 것인가」다. 교과서 정의는 결과를 설명하는 말이고, **판단에 쓰이는 것은 매번 다시 정하는 세는 기준**이다.
- **데이터를 다시 갖는 것이 후퇴는 아니다** — 18일 뒤 `UserCommand` 는 `LinkedList userList` 를 필드로 갖는다. 그런데 그 목록을 **다루는** 코드는 없다 — `add`·`toArray`·`indexOf` 를 부를 뿐이다. Day19 가 없애려 한 것은 데이터를 갖는 것이 아니라 **데이터를 다루는 코드가 화면 코드와 섞여 있는 것**이었고, 「데이터를 갖지 않는 클래스」를 목표로 외우면 이 코드가 뒤로 간 것으로 보인다 → [[linked-list]]
- **흐름을 다 넘긴 것이 아니다** — 18일 뒤 `App` 은 서브메뉴만 넘겼고 「도움말」은 자기 `switch` 안에서 직접 출력한다. `HelpCommand` 클래스가 따로 있는데도 그렇다. **서브메뉴가 없는 메뉴는 옮길 것이 없어서 예외가 되고**, 그 예외 하나 때문에 「모든 메뉴는 Command 가 처리한다」가 깨진다 → [[template-method-pattern]]
- **응집도가 높아지면 클래스 사이 호출이 늘어난다** — 배열을 직접 만지지 않으니 `contain`·`addMember`·`getMember` 처럼 작은 메서드가 여럿 생긴다. 「메서드가 늘었으니 복잡해졌다」로 보이지만, 늘어난 것은 **드러난 약속의 개수**이고 감춰졌던 의존이 이름을 얻은 것이다 → [[method]]

## 함께 보는 개념

- [[encapsulation]] — 같은 방향의 다른 축(필드를 어떻게 여는가)
- [[class]] — 데이터와 기능이 함께 사는 단위
- [[method]] — 옮겨지는 대상
- [[access-modifier]] — 남의 데이터에 못 닿게 만드는 문법
- [[package]] — 역할이 갈린 클래스를 묶는 상위 단위
- [[this-reference]] — 기능을 데이터 옆으로 옮기던 첫 단계
- [[crud]] — 이 배치가 필요해진 규모
- [[string-comparison]] — `Project` 가 갖게 된 도메인 규칙
- [[object-reference]] — `getUsers()` 가 내주는 것
- [[read-side-effect]] — 조회수를 올리는 판단이 밖에 남은 자리
- [[grasp]] — 이 기준에 이름을 붙여 주는 지침 묶음
- [[defensive-copy]] — 저장소를 안에 남길 수 있게 해 준 장치
- [[surrogate-key]] — UI 가 인덱스를 몰라도 되게 만든 조건
- [[linear-search]] — 소유자가 대신 해 주는 조회의 내용
- [[access-modifier]] — 쪼갠 뒤 다시 그려야 하는 경계
- [[generalization]] — 응집도 정리가 만든 중복을 되감는 다음 단계
- [[refactoring]] — 이 정리가 놓인 작업의 단위
- [[command-loop]] — 흐름 제어가 옮겨 간 내용
- [[template-method-pattern]] — 네 벌이 된 흐름이 도착한 구조

## 출처

- [[2024-06-18-Day17]] — 팀원 중복 검사 `contain` 을 `ProjectCommand` 에 두려던 초안이 `Project` 안으로 옮겨지고, `addMember`·`deleteMember`·`getMember` 도 `Project` 가 갖게 되며 `ProjectCommand` 는 배열을 직접 만지지 않게 되는 것을 실습으로 배웠다. 회원 배열이 `private static` 이라 `UserCommand.findByNo` 를 만들어 소유자에게 조회를 맡긴 것도 이 자리다
- [[2024-06-19-Day18]] — `Board` 는 getter/setter 만 갖고, 조회수를 올리는 판단은 `BoardCommand` 의 `viewBoard`·`updateBoard` 두 곳에 복사되었다. 전날 `Project` 에서 얻은 배치가 다음 실습에 이어지지 않은 자리이고, **`private` 이 막아 주는 범위가 필드 타입에 달려 있다는 것**이 그 차이로 드러났다
- [[2024-06-20-Day19]] — GRASP 의 High Cohesion 으로 이 기준에 이름이 붙고, 적용 대상이 메서드에서 **클래스 전체**로 올라갔다. `UserCommand` 가 갖고 있던 배열·개수 변수와 데이터 처리 메서드가 `UserList` 로 나가면서 `users`·`userLength`·`MAX_SIZE` 라는 이름이 UI 쪽에서 사라지고, `delete` 가 지운 회원을 돌려주며 성공/실패 판정까지 소유자가 갖게 되었다. 그 대가로 결합이 늘었고, `private` 이던 탐색 메서드를 `public` 으로 열어야 했다
- [[2024-07-08-Day30]] — High Cohesion 을 **데이터가 아니라 흐름 제어에** 적용했다. 「App에 subMenus에서 수행하는 기능들 혼재」를 진단하고 서브메뉴 루프·번호 검증·갈래 처리를 각 `Command` 로 옮겨, 단위가 「어떤 필드를 읽는가」에서 「어느 메뉴의 것인가」로 올라간다. 그 대가는 결합이 아니라 **중복**이었고(「응집력을 높인 결과 각 Command 클래스에 동일한 코드 생성」) 같은 노트의 다음 절이 그것을 일반화로 되감는다. Day19 가 만든 `UserList` 는 사라지고 목록이 `LinkedList userList` 로 `UserCommand` 의 필드로 돌아오는데, 목록을 **다루는** 코드는 여전히 밖에 있다
