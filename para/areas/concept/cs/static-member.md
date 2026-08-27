---
type: concept
id: static-member
title: 클래스 멤버와 인스턴스 멤버 (static)
aliases:
  - static
  - 스태틱
  - 클래스 메서드
  - class method
  - 인스턴스 메서드
  - instance method
  - 클래스 변수
  - 정적 메서드
up:
  - 2024-06-11-Day12
  - 2024-06-17-Day16
  - 2024-06-18-Day17
  - 2024-06-20-Day19
  - 2024-07-03-Day28
  - 2024-07-10-Day32
  - 2024-07-11-Day33
tags:
  - java
  - 객체지향
  - 문법
---

# 클래스 멤버와 인스턴스 멤버 (static)

같은 클래스 안의 멤버가 **클래스에 붙는 것**과 **인스턴스에 붙는 것**으로 갈린다. `static` 이 그 표시이고, 갈리는 것은 이름이 아니라 **부르는 방법과 접근할 수 있는 상태**다.

## 정의

| | 클래스 멤버 (`static`) | 인스턴스 멤버 |
|---|---|---|
| 소속 | 클래스 | 인스턴스 하나하나 |
| 호출 | `클래스명.멤버` — **객체 생성 없이** | `레퍼런스.멤버` — [[instance]] 를 먼저 만들어야 |
| 개수 | 하나 | 인스턴스마다 하나씩 |
| 접근 | 클래스 멤버만 | 클래스 멤버 + 자신의 인스턴스 멤버 |

이 필기의 정리는 이렇다.

```text
[클래스 메서드]
객체에 종속되지 않는 기능을 제공한다.
객체의 상태에 영향을 받지 않는 독립적인 작업을 수행한다.
클래스 메서드는 객체의 생성 없이 직접 호출할 수 있다.

[인스턴스 메서드]
특정 객체에 종속된 기능을 제공한다.
객체의 상태를 변경하거나 해당 객체의 속성을 조작하는 작업을 수행한다.
인스턴스를 생성한 후에만 호출할 수 있다.
객체에 종속되기 때문에 인스턴스를 생성하여 레퍼런스를 사용해야한다.
```

## 사용 예시

같은 실습 안에 두 종류가 나란히 있다.

```java
int menuNo = Integer.parseInt(command);              // 클래스 메서드 — Integer 를 만들지 않았다

Scanner keyboard = new Scanner(System.in);           // 인스턴스를 먼저 만들고
String command  = keyboard.nextLine();               // 인스턴스 메서드 — 레퍼런스로 부른다
```

→ [[number-parsing]] · [[standard-input]]

`Integer.parseInt` 는 넘긴 문자열만 보면 답이 나오므로 객체가 필요 없다. `nextLine()` 은 **그 `Scanner` 가 어디까지 읽었는지**를 알아야 하므로 인스턴스에 붙는다. **상태를 들고 있어야 하는가**가 갈림길이다.

그리고 이 실습의 클래스는 전부 `static` 이다.

```java
public class App {
    static String[] menus = new String[]{ "회원", ..., "종료" };
    static Scanner keyboard = new Scanner(System.in);

    public static void main(String[] args) { ... }
    static void printMenu(){ ... }
    static String prompt(){ ... }
}
```

`main` 이 `static` 이라 거기서 부르는 메서드도, 그 메서드들이 쓰는 `menus`·`keyboard` 도 모두 `static` 이 되어야 했다 → [[main-method]]

### 같은 클래스를 두 방식으로 만들어 보면 갈림이 드러난다

며칠 뒤 클래스를 배우는 회차의 `Calculator` 실습이 같은 기능을 두 번 만든다. 먼저 전부 클래스 멤버로.

```java
public class Calculator {
  static int result = 0;
  static void plus(int a) { result += a; }
  ...
}

Calculator.plus(2);
Calculator.plus(3);
System.out.printf("result = %d\n", Calculator.result);
```

객체를 만들지 않아서 편한데, **계산기가 프로그램 전체에 하나뿐이다.** `result` 가 클래스당 하나이므로 두 계산을 따로 굴릴 수 없다.

필드를 인스턴스 멤버로 바꾸면 `new` 한 만큼 생긴다.

```java
public class Calculator {
  int result = 0;
  static void plus(Calculator that, int a) { that.result += a; }
  ...
}

Calculator c1 = new Calculator();
Calculator.plus(c1, 2);                              // 어느 계산기인지 말해 줘야 한다
System.out.printf("result = %d\n", c1.result);
```

메서드는 아직 `static` 인데 필드만 인스턴스 것이 되어서, **대상을 매개변수로 받아야** 한다. 이 중간 단계가 `this` 가 실은 무엇인지 드러나는 자리다 → [[this-reference]] · [[class]]

### 한 프로그램 안에서 두 성격이 갈라진다

바로 다음 회차의 실습 프로젝트는 클래스를 두 갈래로 만든다. **데이터를 담는 쪽은 인스턴스, 명령을 수행하는 쪽은 전부 `static`** 이다 → [[package]]

```java
public class User {                  // vo — new 로 여러 개 만든다
  private String name;
  public String getName() { return name; }
}
```

```java
public class UserCommand {           // command — 인스턴스를 만들 일이 없다
  private static final int MAX_SIZE = 10;
  private static final User[] users = new User[MAX_SIZE];
  private static int userLength = 0;

  public static void excuteUserCommand(String command) { ... }
  private static void addUser() { ... }
}
```

`Prompt` 도 같은 쪽이다 — `static Scanner keyboardScanner` 하나에 `static` 메서드뿐이다 → [[varargs]]

**같은 `class` 문법으로 성격이 정반대인 두 가지를 만든 셈**이고, 그 갈림이 패키지 이름(`vo` / `util` / `command`)으로 표시돼 있다. 앞의 회차들에서 `main` 이 `static` 이라 전부 끌려갔던 것과 달리, 여기서는 **어느 쪽으로 할지 고른 결과**다.

그리고 그 선택의 대가가 바로 드러난다. `users` 가 `static` 이므로 **회원 목록은 프로그램 전체에 한 벌**이다. `ProjectCommand` 가 회원을 찾을 때 인스턴스를 받지 않고 `UserCommand.findByNo(userNo)` 라고 클래스 이름으로 부를 수 있는 것이 그 결과이자 한계다 — 회원 목록이 둘 필요해지는 날 이 호출부터 성립하지 않는다 → [[cohesion]]

### 클래스당 하나뿐인 것을 처음으로 「쓰려고」 고른다

여기까지 `static` 은 대개 **어쩔 수 없이** 붙었다. 그 다음 회차에서 처음으로 **하나뿐이라는 성질 자체가 필요해서** 고른다 — 지금까지 몇 개를 발급했는지 세는 카운터다.

```java
class Counter  {
    static int count = 0;
    Counter() {
        this.count++;
        System.out.println(this.count);
    }
}

Counter c1 = new Counter();          // 1
Counter c2 = new Counter();          // 2
```

인스턴스를 둘 만들었는데 `1`·`2` 가 찍힌다. **필드가 인스턴스 멤버였다면 둘 다 `1`** 이다 — 인스턴스마다 자기 `count` 를 갖고 각자 `0` 에서 시작하니까. 「몇 개 만들어졌나」는 **인스턴스 하나가 알 수 있는 정보가 아니라 클래스가 아는 정보**이고, 그것이 `static` 을 고르는 이유다 → [[instance]] · [[constructor]]

같은 구조가 실습 프로젝트의 식별 번호로 들어간다. 이번에는 **한 클래스 안에 두 성격의 필드가 짝으로** 놓인다.

```java
public class User {
  private static int seqNo;                    // 클래스당 하나 — 발급기
  private int no;                              // 인스턴스마다 하나 — 받은 번호

  public static int getSeqNo() {
    return ++seqNo;
  }
}
```

```java
user.setNo(User.getSeqNo());                   // 클래스 이름으로 부른다
```

`getSeqNo` 가 `static` 인 것이 필수다 — 번호를 받으려는 시점에 대상 인스턴스는 아직 번호가 없고, **누구의 번호도 아닌 값**을 물어보는 것이기 때문이다. `vo` 클래스가 처음으로 클래스 멤버를 갖게 된 자리이고, 그래서 이 클래스는 이제 인스턴스 전용이 아니다 → [[surrogate-key]]

그리고 `static` 저장소가 **자기 클래스를 얻는다.**

```java
public class UserList {
  private static final int MAX_SIZE = 10;
  private static final User[] users = new User[MAX_SIZE];
  private static int userLength = 0;

  public static void add(User user)       { users[userLength++] = user; }
  public static User findByNo(int userNo) { ... }
}
```

전날 `UserCommand` 안에 있던 세 필드가 그대로 옮겨 왔다 — **`static` 성격은 하나도 바뀌지 않았고 사는 집만 바뀌었다.** 필드와 메서드가 전부 `static` 인 클래스는 「인스턴스를 만들 일이 없는 클래스」이고, 이 코드는 `Prompt` 와 같은 부류를 하나 더 만든 것이다 → [[cohesion]] · [[package]]

### `static` 필드가 담는 것이 인스턴스 자신이 되는 자리

**두 주 뒤 회차의 싱글톤은 지금까지와 담는 것이 다르다.** 카운터는 `int` 를 담았고 저장소는 배열을 담았는데, 여기서는 **자기 클래스의 인스턴스**를 담는다.

```java
private static Car instance;

public static Car getInstance() {
  if (instance == null) {
    instance = new Car();
  }
  return instance;
}
```

두 멤버가 `static` 이어야 하는 이유가 각각 다르다. **필드는 「그 하나」를 클래스가 들고 있어야 하니까**이고(인스턴스 필드면 인스턴스마다 자기 것을 갖게 되어 셀 수 없다), **메서드는 부르는 시점에 인스턴스가 아직 없으니까**다 — Day19 의 `getSeqNo()` 가 「누구의 번호도 아닌 값」을 물어보느라 `static` 이어야 했던 것과 같은 이유다 → [[singleton-pattern]] · [[default-initialization]]

**그리고 `UserList` 와의 대비가 여기서 선명해진다.** 둘 다 「프로그램 전체에 하나」를 만드는데, `UserList` 는 인스턴스가 **없고** `Car` 는 **하나 있다.** 그래서 `Car` 는 매개변수로 넘어가고 인터페이스를 구현할 수 있지만 `UserList` 는 못 한다 — **「하나뿐」은 같고 「객체인가」가 갈린다** → [[instance]] · [[polymorphism]]

## 왜 중요한가

**`static` 은 편의 문법이 아니라 "이 코드가 어떤 상태에 닿을 수 있는가"를 정하는 선언이다.** `static` 메서드 안에는 `this` 가 없다. 그래서 인스턴스 필드를 읽을 수도, 인스턴스 메서드를 부를 수도 없고, 그것이 컴파일 단계에서 막힌다.

이 제약이 실습 코드의 모양을 결정했다. `main` 이 `static` 이므로 **메서드를 뽑는 순간 필드도 `static` 으로 올려야** 했고([[method]]), 그 결과 `menus`·`keyboard` 는 프로그램 전체가 공유하는 하나의 상태가 되었다. 나중에 객체지향을 배우며 이 코드를 인스턴스로 다시 쪼개게 되는 이유가 여기 있다 — **`static` 으로 시작하면 상태가 하나뿐이라 같은 프로그램을 두 벌 돌릴 수 없다.**

## 경계와 오해

- **`System.out.println()` 은 클래스 메서드가 아니다** — 이 필기는 "표준입출력은 인스턴스 메서드로 객체에 종속되어 있다"고 적었는데, 문장이 뭉쳐 있어 오해가 되기 쉽다. 정확히는 `System.out` 이 **`System` 의 클래스 변수(static 필드)**이고, `println` 은 그 필드에 담긴 `PrintStream` **인스턴스의 메서드**다. 점이 두 번 찍히는 것이 그 증거이고, `System.println()` 이라 쓸 수 없는 이유다. **클래스 멤버를 거쳐 인스턴스 멤버에 닿는 것**이라, 둘 중 하나로 잘라 말할 수 없다 → [[io-stream]]
- **`static` ≠ 상수** — 하나만 존재한다는 뜻이지 바뀌지 않는다는 뜻이 아니다. `static String[] menus` 는 내용을 고칠 수 있다. 바뀌지 않게 하는 것은 `final` 이고 축이 다르다.
- **클래스 선언에 붙는 `static` 은 다른 축을 말한다** — 일주일 뒤 중첩 클래스 회차에서 `static` 이 **클래스 앞**에 오는데, 그때 뜻은 「클래스당 하나」가 아니라 **「바깥 인스턴스에 대한 숨은 참조가 없다」**다. `public static class Node` 는 하나만 존재하는 것이 아니라 `LinkedList` 가 노드마다 `new` 한다. 같은 키워드가 **개수**를 말하는 자리와 **소속**을 말하는 자리로 갈리는 것이고, 이 노트가 다뤄 온 「몇 개 있나」로 읽으면 그 자리에서 어긋난다.

  다만 뿌리는 같다 — 어느 쪽이든 **인스턴스에 딸려 있지 않다**는 뜻이다. `static` 필드는 인스턴스가 없어도 존재하고, `static` 중첩 클래스는 바깥 인스턴스가 없어도 만들 수 있다. 그래서 정적 중첩 클래스는 바깥의 `static` 멤버만 그냥 쓸 수 있고 인스턴스 멤버가 필요하면 **생성자로 받아야** 하는데, 그 회차의 `new ListIterator(this)` 가 Day16 의 `Calculator.plus(c1, 2)` 와 같은 모양이다 → [[nested-class]] · [[this-reference]]
- **`static` 클래스 안이 전부 `static` 이 되는 것은 아니다** — 하루 뒤 회차가 정적 중첩 클래스 안에 `static int v1` · `static void m1()` · `static {}` 과 `int v2` · `void m2()` · `{}` 를 **함께** 선언해 「top level class 처럼」 된다는 것을 보였다. `static` 이 그 클래스에 붙은 것은 **바깥과의 관계**를 정한 것이고, 안에서 멤버를 어느 쪽으로 할지는 **여전히 따로 정하는 결정**이다. 이 구별이 없으면 정적 중첩 클래스의 인스턴스를 `new X()` 로 여러 개 만드는 코드가 모순처럼 보인다 → [[instance]]
- **"객체의 상태에 영향을 받지 않는다" ≠ "상태가 없다"** — 클래스 메서드도 클래스 변수를 읽고 고칠 수 있다. 이 필기의 `printMenu()` 가 `static` 필드 `menus` 를 읽는 것이 그렇다. 인스턴스의 상태에 종속되지 않는다는 뜻일 뿐이므로, `static` 을 "부작용이 없다"로 읽으면 어긋난다.
- **방향이 한쪽이라는 것은 「자기 인스턴스」에 한한 이야기다** — 인스턴스 메서드는 클래스 메서드를 부를 수 있지만 반대는 안 된다. `static` 문맥에는 「누구의」에 해당하는 것이 없기 때문이다. 그런데 **자기가 만든 객체의 인스턴스 메서드는 부를 수 있다.** 하루 뒤 중첩 클래스 회차의 `static void m1()` 이 `X obj = new X(); obj.test();` 로 정적 중첩 클래스의 **인스턴스 메서드**를 부르고 필기가 「인스턴스 메서드는 객체생성 후 호출가능」이라 주석을 달았다. `main` 이 `new Scanner(...)` 를 만들어 `nextLine()` 을 부르는 것과 같은 일이다 — 막히는 것은 「인스턴스 메서드를 부르는 것」이 아니라 **「대상을 말하지 않고 부르는 것」**이고, 그 구분이 없으면 `static` 인 `main` 에서 왜 아무것도 못 할 것 같지 않은지가 설명되지 않는다 → [[this-reference]] · [[instance]]
- **「MethodArea에 있으니 직접 접근 가능」은 이유가 아니고, 시점도 지났다** — 하루 뒤 회차가 정적 중첩 클래스의 접근 규칙에 「Static으로 선언된 멤버는 메모리상에 MethodArea에 생성되여 직접 접근 가능하지만, non-static은 Heap 인스턴스를 받아와야한다」라는 설명을 붙였다. 두 군데가 어긋난다. ① **위치가 그렇지 않다** — Java 7·8 이후 `static` 필드는 Method Area(Metaspace)가 아니라 **힙**에 있는 `Class` 객체 옆에 산다. Metaspace 에 남은 것은 클래스 메타데이터다. ② **위치는 애초에 이유가 아니다** — 인스턴스 필드에 못 닿는 것은 그것이 힙에 있어서가 아니라(`static` 필드도 힙에 있다) **어느 인스턴스인지 말할 방법이 없어서**다. 그리고 **같은 노트가 바로 위 줄에서 정확한 이유를 이미 적었다** — 「바깥 클래스의 인스턴스 주소를 담는 B2.this 라는 인스턴스 멤버가 없다」. 두 설명이 나란히 있고 **나중 것이 앞 것보다 약하다** → [[class-metadata]] · [[garbage-collection]] · [[jvm]]
- **인스턴스 메서드를 부르려면 레퍼런스가 있어야 한다** — 그 레퍼런스가 `null` 이면 `NullPointerException` 이다. 클래스 메서드에는 이 실패가 없다 → [[object-reference]]
- **`static` 으로 다 만들면 컴파일 오류는 사라지지만 설계가 사라진다** — 인스턴스 멤버를 쓰려다 오류가 났을 때 `static` 을 붙여 넘기는 것이 가장 쉬운 해결이고, 그것이 이 실습 코드의 상태다. 오류는 없어졌지만 **상태가 전역이 되어 클래스가 하나의 큰 함수 묶음**이 된다.
- **"클래스 필드는 변수를 1개만 생성할 수 있다" 는 필드 개수 제한이 아니다** — `static` 필드는 여러 개 선언할 수 있다. 하나뿐인 것은 **선언한 필드마다의 저장소**이고, `static int result` 라는 저장소가 클래스당 하나라는 뜻이다. 문장을 글자대로 읽으면 「클래스에 `static` 필드를 하나만 둘 수 있다」가 되어, 위 실습의 `menus`·`keyboard` 두 개와 바로 어긋난다.
- **"한번에 한개의 클래스만 사용 가능하다" 도 클래스 개수 이야기가 아니다** — 클래스 멤버로만 만든 계산기는 상태가 하나뿐이라 **두 계산을 동시에 진행할 수 없다**는 뜻이다. 여러 클래스를 동시에 쓰는 것은 언제나 된다.
- **`static` 을 떼는 것은 두 단계다** — 필드를 non-static 으로 바꾸는 것과 메서드를 non-static 으로 바꾸는 것이 따로 일어난다. 중간 단계(필드는 인스턴스, 메서드는 `static`)도 컴파일되고 돌아가지만, 대상을 매개변수로 손수 넘겨야 한다. 이 단계를 건너뛰면 `this` 가 「자동으로 생기는 것」으로만 남는다 → [[this-reference]]
- **`private static final` 은 세 축이 겹친 것이다** — `private` 은 어디서 보이는가, `static` 은 몇 개 있는가, `final` 은 다시 대입할 수 있는가다. `private static final User[] users` 는 **「밖에서 안 보이는, 클래스당 하나뿐인, 다른 배열로 바꿀 수 없는」 배열**이고 **내용은 얼마든지 바뀐다.** 세 키워드를 「상수」로 뭉쳐 읽으면 그 마지막이 설명되지 않는다 → [[array]]
- **`static` 을 고른 것과 `static` 으로 끌려간 것은 구별되지 않는다** — Day12 의 필드들은 `main` 때문에 어쩔 수 없이 `static` 이 됐고, Day17 의 `command` 클래스는 그렇게 만들기로 고른 것이다. 코드는 같은 모양이라, 나중에 인스턴스로 바꿀 때 **어느 것이 의도였는지 알 방법이 없다.** Day19 의 `seqNo` 는 처음으로 **하나뿐이라는 성질이 목적인** `static` 이라, 나중에 인스턴스로 바꾸면 기능이 깨지는 쪽이다 → [[surrogate-key]]
- **`static` 필드를 `this` 로 읽는 것은 컴파일되지만 오해를 남긴다** — Day19 의 `Counter` 는 `this.count++` 로 클래스 필드를 올린다. 컴파일러가 막지 않고(IDE 가 경고를 띄우는 정도다) 동작도 맞는데, **읽는 사람에게는 인스턴스마다 다른 `count` 가 있는 것처럼 보인다.** 정확히 쓰면 `count++` 나 `Counter.count++` 이고, 그렇게 써야 「이 값은 공유된다」가 코드에 드러난다 → [[this-reference]]
- **`static` 필드 ≠ 전역변수** — 필기가 두 번 같은 말을 했다. Day19 에서 「전역변수와 같은 역할을 하게 된다」였고, 두 주 뒤 싱글톤에서 다시 「하나의 값(전역변수)만을 가지는 인스턴스 선언」이다. 하나뿐이라는 점은 같지만 **이름이 클래스 안에 있고 접근 지정자가 붙는다.** `private static int seqNo` 도 `private static Car instance` 도 그 클래스 밖에서 이름조차 부를 수 없으므로 전역이 아니고, 전역으로 읽으면 **`private` 을 붙이는 이유가 설명되지 않는다.** 다만 **공유 상태라는 성질은 실제로 전역변수와 같다** — 접근 경로가 하나로 좁혀지는 것과 그 하나를 누구나 부를 수 있는 것은 별개다 → [[access-modifier]] · [[singleton-pattern]]
- **「인스턴스 메서드로 선언하는 것이 아닌 클래스 필드를 생성」은 두 가지를 뭉갠 문장이다** — 메서드를 어느 쪽으로 할지와 필드를 어느 쪽으로 할지는 **따로 정하는 두 결정**이다. Day16 의 중간 단계(필드는 인스턴스, 메서드는 `static`)가 그 증거이고, Day19 의 `User` 는 반대 조합(`static` 필드 + `static` 메서드 + 인스턴스 필드 + 인스턴스 메서드)을 한 클래스에 다 갖는다.
- **클래스마다 저장소가 따로다** — `User`·`Board`·`Project` 가 각자 `private static int seqNo` 를 가지므로 카운터가 세 개다. 「`static` 은 하나뿐」을 **프로그램에 하나**로 읽으면 1번 회원과 1번 게시글이 동시에 존재하는 것이 설명되지 않는다. 하나뿐인 범위는 **클래스 하나**다 → [[surrogate-key]]
- **`static` 저장소는 프로그램이 끝나면 사라진다** — `UserList.users` 는 메모리에만 있으므로 다시 켜면 회원 목록도 `seqNo` 도 초기 상태다. 「클래스에 붙어 있다」를 「오래 산다」로 읽기 쉬운데, 사는 기간은 **클래스가 로드된 동안**일 뿐이다 → [[jvm]] · [[read-side-effect]]
- **`static` 클래스를 만들어도 전역 상태는 그대로 하나다** — `UserList` 로 옮겨 응집도는 올랐지만 회원 목록이 여전히 프로그램 전체에 한 벌이다. 클래스를 쪼갠 것과 상태를 인스턴스화한 것은 **다른 일**이고, 「목록이 둘 필요해지는 날」의 문제는 하나도 안 풀렸다 → [[cohesion]] · [[grasp]]

## 함께 보는 개념

- [[method]] — 두 종류로 갈리는 대상
- [[main-method]] — `static` 이어야 하는 이유가 가장 분명한 자리
- [[instance]] — 인스턴스 멤버가 붙는 곳
- [[object-reference]] — 인스턴스 메서드를 부르는 데 필요한 것
- [[standard-input]] — `Scanner` 인스턴스가 상태를 들고 있는 예
- [[number-parsing]] — 상태가 없어 클래스 메서드로 충분한 예
- [[this-reference]] — 인스턴스 메서드에만 넘어오는 것
- [[class]] — 두 종류의 멤버가 함께 사는 단위
- [[encapsulation]] — 인스턴스 필드를 닫고 메서드로 여는 다음 단계
- [[package]] — 두 성격의 클래스를 갈라 두는 단위
- [[cohesion]] — `static` 저장소를 소유한 클래스가 조회를 대신 해 주는 자리
- [[varargs]] — `static` 유틸리티 클래스의 예
- [[surrogate-key]] — 하나뿐이라는 성질이 목적이 되는 첫 자리
- [[constructor]] — 카운터를 올리는 자리
- [[grasp]] — `static` 저장소가 자기 클래스를 얻는 근거
- [[singleton-pattern]] — `static` 필드가 자기 클래스의 인스턴스를 담는 쪽
- [[default-initialization]] — `null` 로 시작하는 것이 쓰임이 되는 자리
- [[nested-class]] — 같은 키워드가 소속을 말하는 자리
- [[garbage-collection]] — 바깥 참조를 안 갖는 것의 실익
- [[class-metadata]] — `static` 필드가 실제로 어디 사는지
- [[variable-scope]] — `static` 문맥에서 인스턴스 층이 사라지는 것

## 출처

- [[2024-06-11-Day12]] — 클래스 메서드는 객체 생성 없이 부를 수 있고 인스턴스 메서드는 레퍼런스가 필요하다는 구분, 그리고 `main` 이 `static` 이라 실습의 메서드와 필드가 모두 `static` 으로 끌려간 것을 배웠다
- [[2024-06-17-Day16]] — 같은 `Calculator` 를 클래스 필드로 한 번, 인스턴스 필드로 한 번 만들어 보며 클래스 필드는 클래스당 하나이고 인스턴스 필드는 `new` 한 만큼 생긴다는 것, 그리고 `static` 메서드가 인스턴스 필드를 다루려면 대상을 매개변수로 받아야 한다는 것을 배웠다
- [[2024-06-18-Day17]] — 실습 프로젝트에서 `vo` 클래스는 인스턴스로, `util`·`command` 클래스는 필드와 메서드를 전부 `static` 으로 만들어 성격을 갈랐다. 저장소가 `private static final` 배열이라 회원 목록이 프로그램 전체에 한 벌이고, 그래서 `UserCommand.findByNo(userNo)` 처럼 클래스 이름으로 조회할 수 있게 된 것도 이 자리다
- [[2024-06-20-Day19]] — `static int count` 를 생성자에서 올리는 `Counter` 로 「클래스당 하나」를 처음 목적으로 삼아 쓰고, 같은 구조를 `private static int seqNo` 로 데이터 클래스에 넣어 식별 번호를 발급했다. `vo` 클래스가 클래스 멤버를 갖게 된 자리이고, 전날 `UserCommand` 안에 있던 `static` 저장소 세 필드가 `UserList` 라는 전부 `static` 인 클래스로 옮겨 간 것도 이 회차다. 필기가 `this.count++` 로 클래스 필드를 읽고 `static` 필드를 「전역변수와 같은 역할」로 적은 것도 여기서 나왔다
- [[2024-07-03-Day28]] — 싱글톤 패턴에서 `private static Car instance` 가 **자기 클래스의 인스턴스**를 담는다. 필드가 `static` 인 이유(「그 하나」를 클래스가 들고 있어야 한다)와 `getInstance()` 가 `static` 인 이유(부르는 시점에 인스턴스가 없다)가 갈리는 자리이고, 전부 `static` 인 `UserList` 와 나란히 놓으면 「하나뿐」은 같고 「객체로 존재하는가」가 다르다는 것이 보인다. `static` 필드를 「전역변수」로 부른 두 번째 기록이기도 하다
- [[2024-07-10-Day32]] — `static` 이 **클래스 선언 앞**에 오는 것을 처음 배운다. 중첩 클래스에서 이 키워드는 「클래스당 하나」가 아니라 「바깥 인스턴스 참조가 없다」는 뜻이고, `public static class Node` 는 노드마다 새로 만들어진다 — **개수 축과 소속 축이 갈리는 자리**다. 같은 `ListIterator` 를 정적 중첩과 인스턴스 중첩으로 두 번 만들어, 정적 쪽은 `new ListIterator(this)` 로 바깥을 손으로 넘기고 인스턴스 쪽은 그 인수가 사라지는 것을 보여 준다 — Day16 의 `Calculator.plus(c1, 2)` → `c1.plus(2)` 와 같은 이동이 한 층 위에서 반복된 것이다. 필기는 `static public class` 로 지정자 순서를 바꿔 썼고, 넷 중 무엇을 고를지의 기준은 적지 않았다
- [[2024-07-11-Day33]] — **`static` 이 클래스에 붙었을 때 안쪽까지 정하지 않는다**는 것이 여기서 드러난다. 정적 중첩 클래스 안에 `static int v1`·`static void m1()`·`static {}` 과 인스턴스 멤버를 함께 선언해 「top level class 처럼」 된다는 것을 보이고, `static void m1()` 안에서 `X obj = new X(); obj.test();` 로 그 인스턴스 메서드까지 부른다 — **`static` 문맥이 막는 것은 「인스턴스 메서드 호출」이 아니라 「대상을 말하지 않는 호출」**임을 보여 주는 코드다. 반대로 인스턴스 중첩 클래스는 `static` 메서드에서 `X obj;` 선언까지만 되고 `this.new X()` 가 컴파일 오류다. 다만 정적 중첩 클래스가 바깥의 인스턴스 멤버에 못 닿는 이유를 「Static으로 선언된 멤버는 메모리상에 MethodArea에 생성되여 직접 접근 가능하지만, non-static은 Heap 인스턴스를 받아와야한다」로 적어 **위치를 이유로 삼았고**(위치도 지금은 다르다), 정작 정확한 이유는 그 바로 위 줄의 「B2.this 라는 인스턴스 멤버가 없다」에 이미 적혀 있다
