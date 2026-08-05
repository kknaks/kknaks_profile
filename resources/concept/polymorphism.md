---
type: concept
id: polymorphism
title: 다형성 (Polymorphism)
aliases:
  - 다형성
  - polymorphism
  - 폴리모피즘
up:
  - 2024-06-25-Day22
  - 2024-06-26-Day23
  - 2024-07-01-Day26
  - 2024-07-03-Day28
  - 2024-07-08-Day30
  - 2024-07-09-Day31
tags:
  - oop
  - java
  - 상속
---

# 다형성 (Polymorphism)

같은 메서드 선언부로 서로 다른 결과를 만들 수 있는 성질. 자동 타입변환과 메서드 오버라이딩이 함께 성립할 때 나온다.

## 정의

두 가지가 갖춰져야 성립한다.

1. **자동 타입변환(업캐스팅)** — 부모 타입 변수가 자식 인스턴스를 가리킬 수 있다.
2. **메서드 오버라이딩** — 자식이 부모 메서드를 재정의한다.

호출 시점에 **변수의 타입이 아니라 실제 인스턴스의 타입**으로 메서드가 결정된다. 일주일 앞선 회차가 그 찾는 순서를 적어 두었다 — **「Object 클래스에 선언된 멤버여도 실제 obj객체가 가리키는 클래스부터 찾아 올라간다」.** 방향이 **아래에서 위로**라는 것이 요점이다. 실제 타입에서 시작해 없으면 부모로 올라가고, 그래서 재정의본이 있으면 반드시 그것이 먼저 걸린다.

```java
타이어 t1 = new 타이어();       // t1.굴린다() → "타이어가 굴러간다"
타이어 t2 = new 한국타이어();    // t2.굴린다() → "한국타이어가 굴러간다"
타이어 t3 = new 금호타이어();    // t3.굴린다() → "금호타이어가 굴러간다"
```

변수 타입은 셋 다 `타이어` 인데 결과가 다르다. 이것이 다형성이다.

## 사용 예시

**매개변수의 다형성** — 메서드가 부모 타입만 받도록 선언해 두는 것.

```java
public class Driver {
    public void drive(Vehicle vehicle) {   // Vehicle 만 안다
        vehicle.run();                      // Bus 가 와도, Taxi 가 와도 동작한다
    }
}

Driver driver = new Driver();
driver.drive(new Bus());    // "버스가 달립니다"
driver.drive(new Taxi());   // "택시가 달립니다"
```

`Driver` 는 `Bus`·`Taxi` 를 **모른다.** 자식이 몇 개가 되든 `drive` 는 안 고친다.

### 이름을 배우기 전에 이미 쓰고 있었다

**일주일 앞선 래퍼 클래스 회차에 오버로딩과 매개변수 다형성이 나란히 놓여 있다.** 기본 타입만으로는 타입마다 메서드를 만들어야 한다.

```java
static void m(long value) { ... }      // byte, short, int, long, char
static void m(double value) { ... }    // float, double
static void m(boolean value) { ... }   // boolean
```

래퍼로 감싸면 하나로 줄어든다.

```java
static void m(Object value) { // 모든 객체를 받을 수 있다.
System.out.printf("wrapper value=%s\n", value);
}
```

**위가 오버로딩이고 아래가 다형성이다.** 위는 컴파일러가 인자 타입을 보고 **셋 중 하나를 고르는** 것이고, 아래는 하나뿐인 메서드가 **무엇이 와도 받는** 것이다. 그래서 위는 새 타입이 생길 때마다 메서드를 하나 더 만들어야 하고 아래는 안 만들어도 된다 — 아래의 `printf("%s")` 가 실제로는 각 래퍼가 재정의한 `toString()` 을 부르므로, **한 메서드 안에서 세 가지 결과가 나온다** → [[method]] · [[wrapper-class]] · [[method-overriding]]

`Vehicle` 예제와 다른 점이 하나 있다. **`Object` 를 매개변수로 쓰면 「모든 객체」가 되므로 자식 목록을 열어 두는 것을 넘어 아무 제약도 없어진다.** 부모 타입을 고르는 것은 「무엇까지 받을까」를 정하는 일이고, `Object` 는 그 선택을 포기한 극단이다 → [[object-class]] · [[type-casting]]

### 부모가 없어도 성립한다 — 인터페이스 쪽

**「다형성」이라는 말이 이 필기에 처음 나오는 것은 상속 수업이 아니라 그보다 닷새 앞선 인터페이스 회차의 1.1 이다.** 세 줄로 그 경로를 적어 두었다 — 「같은 형식으로 선언된 메소드여도 구현객체에 따라 다른 결과 값을 가져온다. 이러한 특징으로 인해 다형성을 구현할 수 있다」.

```java
List list = new ArrayList();     // 배열로 담는다
List list = new LinkedList();    // 노드 사슬로 담는다
```

`list.add(obj)` 한 줄이 한쪽에서는 배열 칸에 대입하고 다른 쪽에서는 마지막 노드를 잇는다. **여기서 두 구현 클래스는 서로 아무 관계가 없다** — 공통 조상이 아니라 **같은 약속을 지킨다는 것**이 근거이므로, 물려받은 코드가 한 줄도 없어도 한 타입으로 다뤄진다 → [[interface]] · [[dynamic-array]] · [[linked-list]]

그래서 다형성의 두 전제 중 앞의 것(자동 타입변환)이 **상속 관계일 때만 성립하는 것이 아니다.** 「부모 타입 변수가 자식 인스턴스를 가리킨다」는 「**약속을 가리키는 변수가 그것을 지키는 인스턴스를 가리킨다**」의 특수한 경우다.

### 받을 범위를 고르는 자리 — `Object` 와 자기 부모 사이

**래퍼 클래스 회차가 열어 둔 물음이 여드레 뒤 회차에서 답을 받는다.** 그때 `m(Object)` 는 오버로딩 셋을 하나로 줄였지만 「모든 객체」가 되어 **받을 범위를 정하는 일 자체를 포기**했다. 정렬 회차는 같은 문제를 만나고 다른 답을 낸다 — 받을 것들만 묶는 부모를 **직접 만든다.**

```java
static void display(BubbleSort sorter, int[] values) { sorter.run(values); }
static void display(QuickSort sorter, int[] values)  { sorter.start(values, 0, values.length - 1); }
```

```java
static void display(Sorter sorter, int[] values) { sorter.sort(values); }   // 하나로 줄었다
```

```java
Sorter sort = new BubbleSort();
display(sort, values); // OK!

Sorter sort2 = new QuickSort();
display(sor2, values); // OK!
```

**`m(Object)` 와 `display(Sorter)` 는 같은 일을 하고 다른 대가를 치른다.** `Object` 로 받으면 `printf("%s")` 처럼 타입을 안 물어도 되는 일만 할 수 있는데, `Sorter` 로 받으면 **`sort(values)` 를 부를 수 있다** — 아무것도 다운캐스팅하지 않고. 매개변수 타입을 좁힌 만큼 그 안에서 할 수 있는 일이 늘어난 것이다 → [[abstract-class]] · [[type-casting]]

그리고 이 회차의 부모는 **다형성만을 위해 존재한다.** `Sorter` 는 `BubbleSort`·`QuickSort` 에 물려줄 코드가 없다(추상 메서드 하나뿐이다). 상속의 원래 이유였던 코드 재사용이 하나도 없는데 상속을 쓰는 것이고, 그래서 **다형성이 상속의 부산물이 아니라 목적일 수 있다**는 것이 여기서 드러난다 → [[inheritance]]

### 조건이 다 갖춰졌는데 쓰지 않은 자리

**닷새 뒤 리팩터링 회차는 다형성의 두 전제를 다 만들어 놓고 호출부에 `switch` 를 남긴다.** `Command` 인터페이스가 있고(약속), 네 명령이 `AbstractCommand` 를 상속하며 `processMenu` 를 재정의한다(오버라이딩). 그런데 `App` 은 이렇다.

```java
UserCommand userCommand = new UserCommand("회원");
BoardCommand boardCommand = new BoardCommand("게시판");
BoardCommand noticeCommand = new BoardCommand("공지사항");
ProjectCommand projectCommand = new ProjectCommand("프로젝트", userCommand.getUserList());

void processMenu(String menuTitle) {
  switch (menuTitle) {
    case "회원": userCommand.execute(); break;
    case "프로젝트": projectCommand.execute(); break;
    case "게시판": boardCommand.execute(); break;
    case "공지사항": noticeCommand.execute(); break;
    case "도움말": System.out.println("도움말입니다."); break;
    ...
  }
}
```

**네 줄이 하는 일이 같다** — `execute()` 를 부른다. 다른 것은 **어느 변수인가**뿐이고, 그 선택을 문자열 비교로 하고 있다.

### 그리고 다음 날 쓴다

**하루 뒤 회차가 그 `switch` 를 지운다.** 메뉴 이름과 명령을 짝지어 표에 담는 것이 방법이다.

```java
Map<String, Command> commandMap = new HashMap<>();      // 값의 타입이 인터페이스다

void processMenu(String menuTitle) {
  Command command = commandMap.get(menuTitle);
  if (command == null) { ... return; }
  command.execute();                                     // 실제 타입은 모른다
}
```

**`processMenu` 에 구현 클래스 이름이 한 글자도 없다.** `commandMap` 안에는 `UserCommand`·`BoardCommand`·`ProjectCommand`·`HelpCommand` 가 섞여 들어 있고, `command.execute()` 한 줄이 그 각각의 구현을 실행한다 — 필기가 그것을 「Command는 인터페이스로 다형성을 이용하여 구현체를 대입한다」로 적었다.

여기서 다형성이 **한 변수가 아니라 한 컬렉션**에 걸린다. 앞의 `Sorter sort = new BubbleSort();` 는 변수 하나가 그때그때 다른 것을 가리키는 형태였는데, 표는 **서로 다른 구현들이 동시에 한 통에 담긴** 형태다. 「부모 타입 변수가 자식 인스턴스를 가리킨다」가 「**약속 타입의 자리들이 여러 구현을 동시에 담는다**」로 커진 것이고, 그래서 명령이 몇 개인지도 `processMenu` 가 모르게 된다 → [[dispatch-table]] · [[hash-based-collection]]

**이틀에 걸친 이 대비가 「쓸 수 있는 상태」와 「쓴 상태」의 차이 전부다** — 전날 바뀐 것은 클래스 구조이고 다음 날 바뀐 것은 호출부 한 곳이다. 이득을 만든 쪽은 뒤쪽이다 → [[interface]] · [[grasp]]

`App` 의 `isValidateMenu(int, String[])`·`getMenuTitle(int, String[])` 이 여전히 `String[] menus` 를 받는 것도 같은 자리다. **메뉴가 「이름의 목록」이면 배열이 맞고 「명령의 목록」이면 `Command` 배열이 맞는데**, 이 코드는 이름 배열로 화면을 찍고 이름 문자열로 객체를 고른다 → [[array]]

## 왜 중요한가

**자식이 늘어나도 호출부가 안 바뀐다.** 이게 없으면 종류가 추가될 때마다 호출부에 `if (v instanceof Bus) ... else if (v instanceof Taxi) ...` 분기가 자란다. 새 자식을 넣는 사람이 호출부를 전부 찾아 고쳐야 하고, 하나를 빠뜨리면 런타임에야 드러난다.

다형성은 **변하는 부분(자식의 구현)과 변하지 않는 부분(호출부)을 갈라 놓는** 장치다.

## 경계와 오해

- **다형성 ≠ 오버로딩** — 오버로딩은 같은 이름 다른 시그니처를 **컴파일 시점**에 고르는 것이고, 다형성은 같은 시그니처를 **실행 시점**에 실제 타입으로 고르는 것이다. **둘이 같은 절에 나란히 놓인 것이 래퍼 클래스 회차의 `m()` 세 개와 `m(Object)` 하나**이고, 거기서 「메서드가 몇 개인가」로 눈에 보이게 갈린다.
- **다형성 ≠ 상속** — 상속은 조건이고 다형성은 그 위에서 나오는 성질이다. 상속만 받고 [[method-overriding]] 을 안 하면 다형성이 발현되지 않는다.
- **필드에는 적용되지 않는다** — 오버라이딩되는 것은 메서드뿐이다. 필드는 변수의 선언 타입을 따른다.
- **부를 수 있는 것과 실행되는 것이 다른 축이다** — 「실제 타입의 것이 실행된다」를 「실제 타입의 메서드를 다 부를 수 있다」로 읽으면 어긋난다. `Object obj = new String("Hello")` 에서 `obj.toString()` 은 `String` 의 것이 실행되지만 `obj.length()` 는 **컴파일이 안 된다.** 부를 수 있는 목록은 **선언 타입**이 정하고, 실행되는 구현은 **실제 타입**이 정한다 → [[type-casting]]
- **`extends` 를 쓰지 않은 클래스에서도 일어난다** — 모든 클래스가 [[object-class]] 를 조상으로 가지므로 **상속 문법을 하나도 쓰지 않은 코드에서도 다형성이 작동하고 있다.** 하루 전 회차의 `String.toString()` 이 그 예다 → [[inheritance]]
- **「부모클래스의 변수명으로 자식클래스 타입을 할당할 수 있다」는 변수 이름 이야기가 아니다** — 이름은 아무 상관이 없고 **변수의 선언 타입**이 부모라는 뜻이다. `Sorter sort = new BubbleSort();` 에서 성립하게 만드는 것은 `sort` 라는 이름이 아니라 왼쪽의 `Sorter` 다. 「변수명」으로 읽으면 「부모와 같은 이름을 써야 하나」로 번지고, 실제로 이 코드의 변수 이름은 부모·자식 어느 클래스 이름과도 다르다 → [[variable]]
- **다형성이 작동하는 것과 올바르게 동작하는 것은 다르다** — 부모 메서드에 몸통이 있으면 자식이 재정의를 빼먹어도 다형성은 성립한다. `MergeSort` 가 `sort` 를 재정의하지 않은 채 `display(sorter, values)` 에 들어가면 **부모의 빈 몸통이 실행되어 정렬되지 않은 배열이 그대로 나온다.** 예외도 경고도 없다 — 「부모 타입으로 받아도 안전하다」는 **추상 메서드가 있을 때만** 참이고, 그 강제가 없으면 다형성은 조용히 아무 일도 하지 않는 쪽으로 열려 있다 → [[abstract-class]] · [[method-overriding]]
- **같은 클래스의 인스턴스 둘은 다형성이 아니다** — 리팩터링 회차의 `App` 은 `BoardCommand` 를 두 번 만들어 「게시판」과 「공지사항」을 처리한다. 동작이 갈리는 근거가 **타입이 아니라 생성자 인자와 각자의 필드**이고, 그래서 재정의도 필요 없다. 「같은 코드로 다르게 동작한다」는 결과가 닮았지만 **인스턴스를 여럿 만드는 것으로 되는 일과 타입을 갈라야 되는 일은 다르다** — 갈릴 것이 값뿐이면 클래스를 늘릴 이유가 없다 → [[instance]]
- **오버라이딩이 있어도 호출부가 `switch` 면 다형성의 이득이 0 이다** — 닷새 뒤 회차(Day30)가 그 형태다. 네 `Command` 가 `processMenu` 를 각자 재정의했으므로 **문법상 다형성은 작동하는데**, `App` 이 문자열로 갈래를 내므로 명령이 하나 늘 때 `App` 을 고쳐야 하는 것은 그대로다. **다형성은 「자식이 재정의했나」가 아니라 「호출부가 타입을 모르나」로 확인해야 한다.** 하루 뒤 회차가 그 `switch` 를 표 조회로 바꾸어 호출부에서 타입을 지운다 → [[coupling]] · [[dispatch-table]]
- **호출부에서 지운 이름이 사라진 것은 아니다** — 표를 쓰는 구조에서도 `new UserCommand(...)` 는 `App` 의 생성자에 남는다. **다형성이 없애는 것은 「부르는 자리」의 타입 의존이고 「만드는 자리」는 그대로**이며, 그 자리를 밖으로 밀어내는 것은 다형성이 아니라 의존성 주입이 하는 일이다 → [[dependency-injection]] · [[dependency-inversion-principle]]
- **표에 담긴 것이 전부 다른 타입일 필요는 없다** — 같은 회차의 `commandMap` 에 `BoardCommand` 두 개가 「게시판」·「공지사항」으로 들어간다. 컬렉션에 담아 한 타입으로 다루는 것과 **그 안이 실제로 여러 타입인 것**은 다른 축이고, 다형성이 주는 이득(호출부가 몰라도 된다)은 안이 한 타입이어도 그대로 있다 → [[instance]]
- **상속 수업에서 배운 개념이 아니다** — 이름이 처음 나오는 것은 인터페이스 회차(1.1)이고 상속 수업은 그보다 닷새 뒤다. 그래서 「다형성은 상속의 응용」으로 순서를 매기면 이 필기의 실제 학습 순서와 어긋난다. **약속을 정해 두고 구현을 갈아 끼우는 쪽을 먼저 보고, 물려받아 재정의하는 쪽을 나중에 봤다** → [[interface]]

## 함께 보는 개념

- [[inheritance]] — 다형성의 전제 조건
- [[method-overriding]] — 다형성을 만드는 두 축 중 하나
- [[type-casting]] — 나머지 한 축
- [[abstract-class]] — 다형성을 강제하는 장치
- [[object-class]] — 상속을 쓰지 않아도 다형성이 성립하는 근거
- [[method]] — 오버로딩과 갈리는 자리
- [[wrapper-class]] — 메서드 셋이 하나로 줄어든 예
- [[interface]] — 상속 없이 다형성을 만드는 길
- [[dynamic-array]] — 같은 약속을 지키는 한쪽
- [[linked-list]] — 같은 약속을 지키는 다른 쪽
- [[grasp]] — 이것을 배치 지침으로 세는 자리
- [[instance]] — 타입을 가르지 않고 값만 다르게 할 때의 선택
- [[template-method-pattern]] — 부모가 자식 구현을 부르는 형태
- [[field-hiding]] — 다형성이 필드에는 적용되지 않는다는 규칙의 실물
- [[dispatch-table]] — 다형성이 호출부에서 실제로 이득을 내는 구조
- [[hash-based-collection]] — 여러 구현을 동시에 담는 통
- [[dependency-injection]] — 「만드는 자리」를 옮기는 다른 축

## 출처

- [[2024-06-25-Day22]] — 「Object 클래스에 선언된 멤버여도 실제 obj객체가 가리키는 클래스부터 찾아 올라간다」로 메서드를 찾는 방향(아래에서 위로)을 배웠고, `Object obj = new String("Hello")` 의 `toString()` 이 `String` 의 재정의본을 부르는 것으로 확인했다. 같은 회차 2.1 에서 `m(long)`·`m(double)`·`m(boolean)` 세 개가 `m(Object)` 하나로 줄어드는 것이 오버로딩과 다형성을 나란히 놓아 준다 — **이름을 배우는 것보다 한 주 먼저 쓰고 있었다**
- [[2024-06-26-Day23]] — **「다형성」이라는 말이 이 필기에 처음 나오는 자리다.** 인터페이스의 개념을 「같은 형식으로 선언된 메소드여도 구현객체에 따라 다른 결과 값을 가져온다 → 이러한 특징으로 인해 다형성을 구현할 수 있다」로 적었고, 실습에서 `ArrayList` 와 `LinkedList` 를 `List` 인터페이스로 묶어 **서로 관계없는 두 클래스가 한 타입으로 다뤄지는** 형태를 만들었다
- [[2024-07-01-Day26]] — 상속 수업에서 다형성의 두 전제(자동 타입변환·오버라이딩)와 타이어 비유로 배웠다. 닷새 전 인터페이스 회차에서 이미 이름과 쓰임을 봤으므로, 여기서 더해진 것은 「상속 관계에서도 같은 일이 일어난다」는 쪽이다
- [[2024-07-03-Day28]] — 「여기에 다형성 개념을 대입하면」으로 추상 클래스에 다형성을 얹어 `display` 오버로딩 두 개를 하나로 줄였다. **매개변수 타입을 `Object` 가 아니라 직접 만든 부모로 고른 첫 자리**이고, 그래서 매개변수 안에서 `sort(values)` 를 바로 부를 수 있다 — 여드레 전 `m(Object)` 가 포기했던 「받을 범위 고르기」의 반대편 답이다. 물려줄 구현이 하나도 없는 부모라서 상속이 코드 재사용이 아니라 다형성만을 위해 쓰인 예이기도 하다
- [[2024-07-08-Day30]] — **두 전제를 다 갖춰 놓고 쓰지 않은 회차다.** `Command` 인터페이스와 `AbstractCommand` 를 만들어 네 명령이 한 타입으로 다뤄질 수 있는 상태를 만들었는데, `App` 은 구현 클래스 넷을 각각 필드로 들고 문자열 `switch` 로 `execute()` 를 부른다 — 네 `case` 가 하는 일이 같고 다른 것은 변수뿐이다. GRASP 목록의 Polymorphism 이 말하는 「타입에 따라 갈리는 분기를 각 타입에게 넘기라」가 정확히 이 자리이고, 넘길 대상(`processMenu`)은 이미 각 Command 안에 있었다. 「게시판」과 「공지사항」을 `BoardCommand` 인스턴스 두 개로 처리한 것은 다형성이 아니라 **값만 다른 인스턴스**의 예로 나란히 놓인다
- [[2024-07-09-Day31]] — **전날 갖춰 놓고 쓰지 않은 것을 쓰는 회차다.** `App` 의 구현 클래스 필드 넷과 문자열 `switch` 가 `Map<String, Command> commandMap` 과 `commandMap.get(menuTitle).execute()` 로 바뀌어 **호출부에서 구현 클래스 이름이 전부 사라진다** — 필기의 「Command는 인터페이스로 다형성을 이용하여 구현체를 대입한다」가 그 한 줄이다. 여기서 다형성이 변수 하나가 아니라 **컬렉션 전체**에 걸린다는 것이 새로 더해진 형태이고, 그래서 `processMenu` 는 명령의 타입도 개수도 모른다. 램프/스위치 예제 2단계에서도 「Lamp의 다형성을 활용하여 모두 제어 가능하다」로 같은 것을 상속 쪽에서 쓴다. 다만 `new UserCommand(...)` 는 `App` 의 생성자에 남아 **「부르는 자리」만 타입을 잊었고 「만드는 자리」는 그대로**이며, `BoardCommand` 를 두 항목으로 담는 것도 전날과 같다
