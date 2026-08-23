---
type: concept
id: interface
title: 인터페이스 (Interface)
aliases:
  - 인터페이스
  - implements
  - 구현 클래스
  - 구현 객체
tags:
  - oop
  - java
  - 클래스설계
  - 추상화
up:
  - 2024-06-26-Day23
  - 2024-07-03-Day28
  - 2024-07-05-Day29
  - 2024-07-08-Day30
  - 2024-07-09-Day31
  - 2024-07-10-Day32
  - 2024-07-26-Day44
---

# 인터페이스 (Interface)

**「무엇을 할 수 있는지」만 적어 두고 「어떻게 하는지」는 비워 둔 타입.** 부르는 쪽은 인터페이스만 알고, 실제로 실행되는 코드는 그것을 `implements` 한 클래스가 갖는다. 필기가 그 역할을 「서로 다른 두 객체를 연결해주는 것」이라 적었다.

## 정의

인터페이스 안에 둘 수 있는 것이 정해져 있다.

| 멤버 | 형태 | 구현 객체가 있어야 하나 |
|---|---|---|
| 상수필드 | `[public static final] 타입 상수명 = 값;` | 아니다 |
| 추상메서드 | `[public abstract] 리턴타입 메서드명(매개변수);` | **그렇다** (구현 클래스가 채운다) |
| 디폴트메서드 | `[public] default 리턴타입 메서드명(...) {...}` | **그렇다** |
| 정적메서드 | `[public\|private] static 리턴타입 메서드명(...) {...}` | 아니다 (인터페이스 이름으로 부른다) |
| private 메서드 | `private [static] ...` | default/static 이 쓸 공통 코드를 감춘다 |

**`[ ]` 안은 써도 되고 안 써도 되는 것이다.** 안 쓰면 컴파일러가 붙인다 — 상수필드는 `public static final`, 메서드는 `public abstract` 이 자동으로 붙는다. 그래서 인터페이스에는 **감춰진 멤버가 존재할 수 없다.**

구현하는 쪽은 클래스 이름 뒤에 `implements` 를 붙인다.

```java
public class B implements 인터페이스명{}
```

그리고 채워야 한다 — 필기의 표현으로 「인터페이스에서 선언된 추상메소드을 오버라이딩을 통해 구체적인 실행 코드가 들어있다」 → [[method-overriding]]

### 인스턴스 필드가 없다는 것이 나머지를 다 정한다

디폴트 메서드가 「인터페이스내에서 상수필드와 추상메소드를 호출할 수 있다」인 이유가 이것이다. **인터페이스는 상태를 가질 수 없으므로** 실행 코드가 쓸 재료가 상수와 「구현 객체에게 물어본 결과」뿐이다. 필기의 「추상메소드 호출 시, 오버라이딩된 구현객체의 메서드에게 매개변수를 전달한다」가 그 말이다 — 디폴트 메서드는 자기 안에서 일을 끝내지 않고 **아래로 내려보낸다.**

정적메서드가 「상수필드 제외한 메서드들을 호출 할 수 없다」도 같은 뿌리의 반대편이다. `static` 은 구현 객체 없이 불리므로 **추상메서드를 실행해 줄 대상이 없다.** 디폴트 메서드는 `this` 가 있어서 부를 수 있고, 정적메서드는 없어서 못 부른다 → [[static-member]]

### 추상 클래스에서 인터페이스로 넘어갈 수 있는 조건

**일주일 뒤 회차는 추상 클래스를 키우다가 인터페이스에 도착한다.** 정렬 클래스들의 공통 부모를 `abstract class Sorter` 로 만들고 그 메서드를 추상 메서드로 바꾸자, 남은 것이 추상 메서드 하나뿐이 되어 클래스일 이유가 없어진다.

```java
public interface Sorter {
  void sort(int[] values);
}
```

필기가 그 조건을 두 줄로 적었다 — 「추상메서드만 있을 경우, 객체 사용규칙을 정의하는 인터페이스로 전환 가능하다 / 추상클래스 안에 일반 메서드가 있다면, 인터페이스로 전환이 불가능하다」. **일주일 전 실습이 왜 `AbstractList` 를 지우지 못했는지가 이 문장으로 설명된다** — 거기에는 `protected int size` 필드와 그것을 읽는 구현이 있었고, 그래서 인터페이스로 접을 수 없었다 → [[abstract-class]]

다만 이 조건은 Java 7 까지의 형태다. `default` 가 생긴 뒤로는 **일반 메서드가 있어도 옮길 수 있는 경우가 있고**, 진짜 벽은 메서드가 아니라 **상태**다 → 「경계와 오해」

### 생략할 수 있는 자리와 생략하면 막히는 자리

**이틀 뒤 회차가 위 표의 `[ ]` 를 컴파일 오류 목록으로 다시 적는다.** 한 인터페이스 안에 네 가지 표기를 나란히 써 놓고 전부 같은 것임을 보여 준다.

```java
interface MyInterface {
  public abstract void m1();

  abstract void m2(); // public 이 생략된 것이다. (default) 아니다!

  public void m3();   // abstract 를 생략할 수 있다.

  void m4();          // public, abstract 모두 생략할 수 있다.

  // => private, protected, (default)는 없다.
  //  private void m5(); // 컴파일 오류!
  //  protected void m6(); // 컴파일 오류!
}
```

**네 줄이 전부 `public abstract void` 다.** 필기가 「(default) 아니다!」에 느낌표를 붙인 것이 이 회차에서 가장 값이 큰 한 줄이다 — 클래스에서는 지정자를 안 쓰면 (default) 로 좁아지는데 인터페이스에서는 `public` 으로 넓어진다. **같은 「비어 있음」이 반대 방향을 뜻한다** → [[access-modifier]]

그리고 생략이 자유로운 것은 **선언 쪽뿐**이다. 구현 쪽에서 같은 것을 생략하면 접근 범위를 좁히는 일이 되어 막힌다.

```java
abstract class MyInterfaceImpl implements MyInterface {
  @Override
  //  private void m2() {}  // 컴파일 오류!
  //  protected void m2() {} // 컴파일 오류!
  //  void m2() {} // 컴파일 오류!
  public void m2() {} // OK!
}
```

이 예제가 `abstract class` 로 선언된 것도 우연이 아니다. 필기가 그 이유를 세 줄로 적어 두었다 — 「인터페이스의 모든 메서드를 구현해야 한다 / 한 개라도 빠뜨린다면 concrete 클래스가 될 수 없다 / 추상 클래스로 선언해야 한다」. **아흐레 전 실습의 `AbstractList` 가 왜 추상이어야 했는지가 여기서 규칙 문장이 된다** → [[abstract-class]] · [[method-overriding]]

마지막으로 **타입은 만들 수 있고 인스턴스는 만들 수 없다.**

```java
MyInterface obj = null;              // 인터페이스 레퍼런스 — 선언은 된다
obj = new MyInterfaceImpl2();        // 담기는 것은 구현체다
//  obj = new MyInterface();         // 컴파일 오류!
```

「규칙이기 때문에 구체적인 구현 내용이 없다. 그래서 인스턴스를 생성할 수 없다」가 필기의 이유다 → [[instance]] · [[object-reference]]

### 열엿새 뒤 — 약속을 만든 쪽이 그 약속을 부르는 형태가 나온다

Day23~32 의 인터페이스는 전부 **내가 부를 것**의 이름이었다. `List`·`Command`·`Iterator` 가 다 내 코드에서 `list.add(...)`·`command.execute()`·`it.hasNext()` 로 불리는 대상이고, 얻은 것은 「구현 클래스 이름을 모르게 되는 것」이었다.

Day44 의 `Observer` 는 방향이 반대다.

```java
public interface Observer {
  public void update(Weather weather);
}
```

```java
  @Override
  public void notifyObservers() {
    for (Observer observer : obsevers) {
      observer.update(weather);
    }
  }
```

**`Observer` 를 선언한 것도 `WeatherData` 쪽 사정이고 그것을 부르는 것도 `WeatherData` 다.** 남이 하는 일은 구현뿐이다. 같은 문법이 두 가지 일을 한다.

| | 무엇을 위해 선언하나 | 구현체를 누가 부르나 | 이 필기의 예 |
|---|---|---|---|
| Day23~32 | 여러 구현을 같은 이름으로 부르려고 | **내가** 부른다 | `List`·`Command`·`Iterator` |
| Day44 | 남이 내 안에 끼어들 자리를 열려고 | **내가 남의 것을** 부른다 | `Observer` |

아래쪽이 라이브러리와 프레임워크가 인터페이스를 쓰는 방식이다 — 내 클래스가 남의 인터페이스를 구현하면 **언제 불릴지는 남이 정한다.** 그래서 이쪽 약속은 「무엇을 부를 수 있나」가 아니라 **「무엇이 불려 올 것인가」**를 적은 것이고, 시그니처를 고치는 비용도 반대편에 생긴다 → [[observer-pattern]] · [[polymorphism]]

## 사용 예시

실습에서 `ArrayList` 와 `LinkedList` 를 하나로 묶은 것이 이 인터페이스다.

```java
package bitcamp.myapp2.util;

public interface List {
  void add(Object obj);

  Object remove(int index);

  Object get(int index);

  Object[] toArray();

  int indexOf(Object obj);

  int size();
}
```

**접근 지정자가 한 글자도 없는데 여섯 개 다 `public abstract` 다.** 그리고 `{ }` 가 없다 — 필기가 「추상화메서드로 메서의 원형만 선언해준다」로 적은 그 상태다.

**이 여섯 줄은 없던 것을 만든 게 아니다.** 필기의 순서가 그것을 보여 준다 — 먼저 「두개의 클래스는 동일한 기능을 하는 메서드들이 있다. add(), remove() .... 등」을 관찰하고, 그 다음에 「하나의 인터페이스로 묶어서 관리하는 것이 편리하다」로 간다. **이미 겹쳐 있던 것에 이름을 붙인 것**이고, 그래서 인터페이스를 먼저 설계하지 않아도 나올 수 있었다.

구현 쪽에서는 여섯 개가 전부 `@Override` 를 달고 나타난다.

```java
public class ArrayList extends AbstracList {
  @Override
  public void add(Object obj) { ... }

  @Override
  public Object get(int index) { ... }

  @Override
  public Object remove(int index) { ... }

  ...

  public boolean contain(User user) {      // 인터페이스에 없는 메서드
    return indexOf(user) != -1;
  }
}
```

**`contain` 만 `@Override` 가 없다.** 인터페이스가 정하는 것은 「최소한 이것들은 있어야 한다」이고, 더 갖는 것은 자유다. 대신 그 메서드는 `List` 타입 변수로는 부를 수 없다 → [[polymorphism]]

**여섯 개 중 `size()` 만 구현 클래스에 없는데 컴파일된다.** 그것은 중간에 낀 추상 클래스가 대신 채웠기 때문이다 → [[abstract-class]]

```java
public abstract class AbstractList implements List {
  protected int size;

  @Override
  public int size() {
    return size;
  }
}
```

## 왜 중요한가

**부르는 쪽이 구현 클래스의 이름을 모르게 된다.**

```java
List list = new ArrayList();     // 여기 한 줄만 LinkedList 로 바꾸면 된다
```

이 문장이 엿새 전 회차에서 남긴 빚을 갚는 자리다. 그때 `UserCommand` 는 응집도를 올린 대가로 `UserList` 라는 **클래스 이름과 그 메서드 다섯 개를 직접** 알게 되었고, 「그 대가를 치를 만했는가」는 판단되지 않은 채로 남았다. 인터페이스는 **알아야 하는 것을 이름 하나에서 약속 하나로 바꾼다** → [[cohesion]] · [[grasp]]

**그 「알아야 하는 것」에 이름이 붙는 것은 아흐레 뒤 회차다.** 세 노동자 클래스를 각각의 타입으로 받아 `doFight`·`doZingZing`·`doSsingSsing` 을 부르던 코드가 `Worker` 하나와 `execute()` 하나로 줄어드는 예제이고, 거기서 호출하는 쪽과 호출되는 쪽을 「호출자(클라이언트)」·「피호출자(구현체)」로 가른다. **인터페이스가 무엇을 줄이는지가 그 축에서 세어진다** → [[coupling]]

**컴파일러가 「빠뜨림」을 목록으로 확인해 준다.** 인터페이스에 메서드를 하나 더하면 모든 구현 클래스가 그 자리에서 컴파일 에러가 난다. 두 클래스가 「같은 기능을 하는 메서드들」을 우연히 나란히 갖고 있던 상태에서는 한쪽에만 메서드를 추가해도 아무 일이 없었다 — **약속이 문서가 아니라 코드가 되면서 어긋남이 실행 전에 드러난다.**

**그리고 상속을 쓰지 않고 다형성을 얻는 길이 열린다.** `ArrayList` 와 `LinkedList` 는 안이 완전히 다른 구조인데(배열 대 노드 사슬) 밖에서는 같은 것으로 다뤄진다. 「공통 조상이 있다」가 아니라 「같은 약속을 지킨다」가 근거이므로, **관계가 없는 클래스들도 한 타입으로 묶인다** → [[polymorphism]] · [[inheritance]]

## 경계와 오해

- **인터페이스 ≠ 추상 클래스** — 둘 다 「미완성 타입」이라 고르는 문제로 보이지만 이 회차는 **둘을 겹쳐 쓴다**(`AbstractList implements List`). 갈리는 지점은 상태를 가질 수 있는가다.

  | | 인터페이스 | [[abstract-class]] |
  |---|---|---|
  | 인스턴스 필드 | 없다 (상수만) | 있다 (`protected int size`) |
  | 생성자 | 없다 | 있다 |
  | 붙이는 문법 | `implements` — **여러 개** | `extends` — **하나** |
  | 구현 있는 메서드 | `default`·`static` 만 | 자유 |

  그래서 필기 2.2 의 순서가 필연이다. **`size` 중복을 인터페이스로는 없앨 수 없다** — 필드를 둘 수 없으니 「둘 다 `size` 를 갖는다」는 약속만 할 수 있고 그 필드 자체를 물려줄 수는 없다. 추상 클래스가 중간에 끼어야 했던 이유가 그것이고, 「인터페이스로 받고 이후 상속을 한다」는 필기의 한 줄이 그 조합이다.
- **`implements` ≠ `extends`** — 필기 2.1 의 코드가 `public class ArrayList extends AbstracList` 로 시작하는데, **`AbstractList` 는 아직 없다.** 다음 절 2.2 에서 만드는 클래스다. 2.1 단계의 코드는 `implements List` 였어야 하고, 완성본을 붙여넣으며 남은 흔적이다(클래스 이름도 `t` 가 빠져 `AbstracList` 다). 「인터페이스를 따르는 클래스에는 implements 인터페이스명 을 붙인다」고 바로 위에 적어 놓고 코드는 `extends` 인 것이 그 증거다.
- **선언할 때 `public` 을 생략할 수 있다 ≠ 구현할 때도 생략할 수 있다** — 인터페이스의 `void add(Object obj);` 는 `public` 이 자동으로 붙지만, 구현 클래스에서 `public` 을 빼면 **접근 범위를 좁히는 것**이 되어 컴파일이 막힌다. 필기가 「오버라이딩(public 타입으로) 을 시행하여야 한다」로 못을 박아 둔 자리이고, **오버라이딩은 접근을 넓힐 수만 있다**는 규칙이 가장 자주 걸리는 곳이다 → [[method-overriding]] · [[access-modifier]]
- **정적메서드는 구현 클래스 이름으로 못 부른다** — 필기가 「메인에서 인터페이스 명으로 호출 가능하다」고 적은 것이 「인터페이스 이름으로**만**」이라는 뜻이다. 인터페이스의 `static` 메서드는 구현 클래스에 상속되지 않으므로 `List.정적메서드()` 는 되고 `ArrayList.정적메서드()` 는 컴파일 에러다. 클래스의 `static` 메서드가 자식 이름으로도 불리는 것과 갈린다 → [[static-member]]
- **필기 1.2 의 「public 메소드」가 가리키는 것은 `public void m3();` 다** — 선언 목록에 `public 상수필드`·`public 추상메소드`·`public 디폴트메소드`·`public 정적메소드` 다음에 `public 메소드` 가 한 줄 더 있어 **몸통 있는 일반 인스턴스 메서드**로 읽히는데, 그런 멤버는 인터페이스에 둘 수 없다. **아흐레 뒤 회차가 그 자리를 채운다** — `public void m3();` 처럼 `abstract` 만 생략한 표기가 실제로 존재하고, 그것이 목록에서 추상메서드와 따로 세어진 것으로 보인다. 어느 쪽이든 **다섯 번째 종류는 아니다.** 몸통을 붙이면 `default` 가 필요하고, 안 붙이면 추상메서드다.
- **`private void m5(); // 컴파일 오류!` 와 `private void x() {}` 가 같은 노트 안에 있다** — 아흐레 뒤 회차의 2.1 은 `private` 을 「없다」로 적고 2.3 은 `private` 메서드를 만든다. 어긋나 보이지만 갈리는 것은 **몸통이다.** 추상메서드는 구현 클래스가 채워야 하므로 `private` 일 수 없고(볼 수 없는 것을 채울 수는 없다), 인터페이스 안에서 끝나는 코드는 `private` 이어도 되지만 **몸통이 필수**다. 2.1 의 그 줄은 「`private` 금지」가 아니라 「몸통 없는 `private` 금지」다 → [[default-method]] · [[access-modifier]]
- **같은 목록의 「private 정적메소드」도 반쪽이다** — 1.2 는 `private 정적메소드` 만 적었는데 1.8 은 「default (non-static, static), static(static) 메소드 호출이 가능하다」로 **non-static private 메서드**까지 말한다. 실제로 둘 다 된다 — 1.2 의 목록이 좁게 적힌 것이다.
- **다섯 종류가 한 번에 생긴 문법이 아니다** — 상수필드와 추상메서드만 처음부터 있었고, `default`·`static` 은 Java 8, `private` 은 Java 9 에서 들어왔다. 필기는 다섯 개를 나란히 놓아 **처음부터 그랬던 것처럼 보이는데**, 「인터페이스에 실행 코드를 둘 수 있다」는 것 자체가 나중에 뒤집힌 규칙이다.
- **디폴트 메서드가 생긴 이유는 편의가 아니다** — 이미 배포된 인터페이스에 메서드를 하나 더하면 그것을 구현한 **세상의 모든 클래스가 깨진다.** 「기본 구현을 같이 주면 안 깨진다」가 `default` 의 목적이고, 그래서 **인터페이스를 나중에 고치는 비용**이 이 문법의 배경이다. 필기는 문법만 배우고 이 이유를 적지 않았다.
- **메서드가 하나도 없는 인터페이스도 쓴다** — `Cloneable` 이 그 예다. 「구현하면 메서드를 채운다」의 예외이고, 하는 일은 **표시**뿐이다 → [[object-cloning]]
- **「인스턴스를 생성할 수 없어서 상수만 둘 수 있다」는 인과가 뒤집혀 있다** — 아흐레 뒤 회차가 인터페이스 필드를 그렇게 설명하는데, **구현체는 인스턴스로 존재한다** — 필드를 둘 자리가 물리적으로 없는 것이 아니다. 상태를 물려주지 못하게 한 것은 결정이고, 그 이유는 `implements` 가 **여러 개** 붙을 수 있다는 데 있다. 두 인터페이스가 같은 필드를 물려주면 한 인스턴스에 그 값이 두 벌 생기고, 클래스 다중 상속을 막은 이유가 인터페이스로 돌아온다. **「상수만」과 「여러 개 붙는다」는 같은 결정의 앞뒷면이다** → [[multiple-inheritance]] · [[static-member]]
- **인터페이스 타입 변수를 만드는 것은 인스턴스를 만드는 것이 아니다** — `MyInterface obj = null;` 은 컴파일되고 `new MyInterface()` 는 막힌다. 「인터페이스는 생성할 수 없다」를 「인터페이스 이름을 타입으로 쓸 수 없다」로 읽으면 정반대가 되는데, **타입으로 쓰는 것이 인터페이스의 목적 전부**다 → [[object-reference]] · [[instance]]
- **인터페이스 상수필드는 설정값을 두는 자리가 아니다** — `public static final` 이 강제되므로 밖에서 다 보이고 바꿀 수 없다. 실습의 `MAX_SIZE` 가 인터페이스가 아니라 `ArrayList` 의 `private static final` 로 남은 것이 그 대비다 — **용량은 구현마다 다른 사정이고 약속이 아니다** → [[static-member]] · [[encapsulation]]
- **`List` 라는 이름이 표준 라이브러리와 겹친다** — 실습은 `bitcamp.myapp2.util.List` 를 만드는데 `java.util.List` 가 이미 있다. 같은 파일이 `java.util.Arrays` 를 import 하고 있어 **`java.util.*` 로 바꾸는 순간 이름이 충돌한다**. 표준 컬렉션과 같은 이름·같은 메서드로 만든 것은 의도된 실습이지만, 그 대가가 이 자리에 있다 → [[package]]
- **「일반 메서드가 있으면 인터페이스로 전환이 불가능하다」는 Java 8 이전의 규칙이다** — `default` 를 붙이면 몸통 있는 메서드도 인터페이스에 들어간다. 그래서 전환을 막는 것은 **일반 메서드가 아니라 인스턴스 필드와 생성자**다. `AbstractList` 를 인터페이스로 접을 수 없는 이유는 `size()` 에 몸통이 있어서가 아니라 **`protected int size` 를 둘 곳이 없어서**이고, 실제로 `size()` 만 있다면 `default int size() { ... }` 로 옮길 수 있는데 그 안에서 읽을 필드가 사라진다. 필기의 규칙을 그대로 외우면 `default` 를 배운 절(1.4~1.5)과 스스로 어긋난다.
- **「추상클래스로 강제하는 데 제약이 있어 인터페이스를 쓴다」는 이 필기의 순서에서만 참이다** — 추상 메서드로 선언한 뒤에는 강제력이 똑같다. 인터페이스가 더 강한 것이 아니라 **부모가 상태와 구현을 못 갖는 것**이 다르다. 「강제 → 더 센 강제」로 읽으면 왜 `AbstractList` 와 `List` 를 **둘 다** 두었는지 설명되지 않는다 → [[abstract-class]]
- **인터페이스를 구현했다고 「할 수 있는 일」이 늘지는 않는다** — `List list = new ArrayList()` 로 받으면 `contain(User)` 를 부를 수 없다. **부를 수 있는 목록은 선언 타입이 정한다**는 것이 인터페이스에서 더 아프게 나타난다 — 구현 클래스에만 있는 메서드를 쓰려면 다시 형변환해야 하고, 그러면 인터페이스로 받은 이유가 사라진다 → [[type-casting]] · [[polymorphism]]
- **그 대가가 12일 뒤 실습에서 실제로 걸린다** — 리팩터링 회차의 `ProjectCommand` 가 `project.getMembers().contains(user)` 를 부른다. `contains` 는 `ArrayList` 에만 있고 `List` 에는 없으므로, **`Project` 는 팀원 목록을 `List` 타입으로 들 수 없다** — `getMembers()` 의 반환 타입이 구현 클래스여야 이 줄이 컴파일된다. 「약속으로 받는다」가 좋은 것이라고 배운 다음, 편의 메서드 하나 때문에 구현 타입으로 되돌아가는 자리다.
- **인터페이스를 만든 것 ≠ 인터페이스로 받은 것 — 그리고 그 사이가 하루였다** — 사흘 뒤 리팩터링 회차(Day30)는 `interface Command { void execute(); }` 를 새로 만들지만, `App` 은 `UserCommand userCommand = new UserCommand("회원")` 처럼 **구현 클래스 넷을 필드로 들고 `switch` 로 갈래를 낸다.** `Command` 타입의 변수도 배열도 없다. 같은 노트의 `List` 도 마찬가지로 `LinkedList userList = new LinkedList();` 다 — **만들어 놓고 어느 것도 타입으로 쓰지 않은 상태**다.

  **다음 날(Day31) 그중 하나가 실제로 타입이 된다.**

  ```java
  Map<String, Command> commandMap = new HashMap<>();

  void processMenu(String menuTitle) {
    Command command = commandMap.get(menuTitle);
    if (command == null) { ... return; }
    command.execute();
  }
  ```

  `processMenu` 에서 구현 클래스 이름이 전부 사라졌고, `App` 의 필드 다섯 개가 표 하나로 줄었다. 즉 **「만든 절」과 「그 타입으로 받는 절」이 하루 차이로 갈려 있고**, 그래서 이 구별은 순서의 문제이지 실력의 문제가 아니다 — 약속을 만드는 일이 먼저 끝나야 그것으로 받을 수 있다 → [[dispatch-table]] · [[dependency-inversion-principle]] · [[coupling]] · [[polymorphism]]

  **`List` 쪽은 하루 뒤에도 그대로다.** Day31 이 목록을 `App` 으로 올려 명령에 넘기면서도 `ArrayList userList` · `LinkedList projectList` 로 **구현 클래스 타입을 그대로 쓴다.** 두 인터페이스가 같은 상태에서 출발했는데 한쪽만 타입으로 승격된 것이고, 갈린 이유는 `Command` 쪽에 **갈래를 없애고 싶은 `switch` 가 있었다**는 것이다 — 인터페이스로 받는 일이 저절로 오지 않고 **그것을 요구하는 문제가 있을 때** 온다 → [[dependency-injection]]

  **그리고 그 다음 날(Day32) `List` 도 타입이 된다 — 요구한 문제는 반복자였다.**

  ```java
  public class ListIterator implements Iterator {
    private List list;                       // ← List 가 처음으로 필드 타입이 된다

    public ListIterator(List list) { this.list = list; }
  }
  ```

  ```java
  public abstract class AbstractList implements List {
    @Override
    public Iterator iterator() {
      return new ListIterator(this);         // this 가 List 로 넘어간다
    }
  }
  ```

  `ListIterator` 는 `ArrayList` 인지 `LinkedList` 인지 알 필요가 없고 `size()`·`get(int)` 만 부른다 — **약속으로 받을 이유가 처음 생긴 자리**다. 명령 클래스들의 `ArrayList userList` 는 그대로 남았으므로, 인터페이스가 타입이 되는 일은 클래스 전체에 한 번에 오지 않고 **그것을 필요로 하는 코드가 생긴 곳에서만** 온다 → [[iterator-pattern]] · [[dependency-inversion-principle]]
- **인터페이스에 메서드를 더해도 구현이 깨지지 않는 경우가 있다 — 중간 층이 받으면 된다** — 아래 마지막 항목(「인터페이스를 고치는 순간 구현 전부를 고친다」)이 하루 뒤 Day32 에서는 성립하지 않는다. `List` 에 `Iterator iterator();` 를 더했는데 **`ArrayList` 와 `LinkedList` 는 한 줄도 바뀌지 않았다.** `AbstractList` 가 그 메서드를 구현해 버렸기 때문이다.

  ```java
  public abstract class AbstractList implements List {
    @Override
    public Iterator iterator() { return new ListIterator(this); }
  }
  ```

  **`default` 메서드가 하는 일을 추상 클래스가 대신한 것**이고, 두 장치가 같은 문제(「이미 있는 구현들을 깨지 않고 약속을 늘리기」)에 답한다는 것이 여기서 보인다. 갈리는 것은 위치다 — `default` 는 약속 안에 기본 구현을 두고, 추상 클래스는 약속 밖 한 층 아래에 둔다. 후자는 **그 부모를 상속한 구현에만** 통하므로, `AbstractList` 를 거치지 않고 `implements List` 만 한 클래스가 있었다면 그것은 깨졌을 것이다 → [[default-method]] · [[abstract-class]] · [[open-closed-principle]]
- **추상 메서드는 「공통 코드」가 아니다** — 리팩터링 회차의 필기가 「ArrayList와 LinkedList의 공통 코드를 추상 메소드(pulic abstract)로 선언한다」로 적었는데, 인터페이스로 올라간 것은 코드가 아니라 **이름과 시그니처**다. 실제 공통 코드는 그 다음 줄의 `AbstractList` 가 받는다 — 필기 자신이 두 단계로 적어 놓고 첫 단계를 코드 이동으로 불렀다. 이 구별이 흐려지면 「인터페이스로 중복을 없앤다」가 되어 **한 줄도 못 옮기게** 된다 → [[abstract-class]]
- **상속 한 층이 끼면 `implements` 가 선언에서 사라진다** — Day30 에서 `UserCommand implements Command` 가 일반화 후 `UserCommand extends AbstractCommand` 로 바뀐다. `Command` 약속을 계속 지키려면 `AbstractCommand implements Command` 여야 하는데 **그 클래스의 코드는 필기에 없다.** 「이 클래스가 무슨 약속을 지키나」를 선언 한 줄로 알 수 없게 되는 것이 상속과 인터페이스를 겹쳐 쓸 때의 값이다 → [[generalization]]
- **약속을 안 지키는 클래스가 섞여도 눈에 띄지 않는다 — 그것을 드러낸 것은 「한 통에 담는 일」이었다** — Day30 의 `HelpCommand` 는 필기가 「help커맨드는 인터페이스를 사용하여 직접구현」이라 적었는데도 `public class HelpCommand {` 로만 선언되어 `implements` 가 없었고, 메서드 이름만 `execute()` 로 같았다. `App` 이 `case "도움말"` 안에서 직접 출력하고 있었으므로 **아무 문제도 드러나지 않았다.**

  **하루 뒤 Day31 이 명령들을 `Map<String, Command>` 에 담자 그 자리에서 고쳐진다.**

  ```java
  public class HelpCommand implements Command {
    public void execute(Stack menuPath) {
        System.out.println("도움말입니다!");
    }
  }
  ```

  `commandMap.put("도움말", new HelpCommand())` 를 쓰려면 `Command` 여야 하기 때문이다. **「이름이 같은 것과 약속을 지키는 것은 다르다」가 컴파일 오류로 드러나는 시점이 「그 타입으로 담을 때」**이고, 그때까지는 선언 한 줄이 빠져 있어도 프로그램이 돈다. 인터페이스의 강제력이 선언에서 오지 않고 **그것을 타입으로 쓰는 코드에서 온다**는 것이 이 하루 사이에 보인다 → [[dispatch-table]] · [[template-method-pattern]]
- **인터페이스를 선언한 것 ≠ 그 타입으로 받는 코드가 있는 것 — Day44 의 `DisplyElement` 가 그 극단이다** — 그 회차는 인터페이스를 셋 만드는데 `DisplyElement` 는 **어디에서도 타입으로 쓰이지 않는다.** `implements Observer, DisplyElement` 라는 선언 한 줄이 전부이고, `display()` 는 같은 클래스의 `update()` 안에서 불리며 `App` 은 변수를 구현 클래스 이름(`CurrentConditionsDisplay`)으로 받는다. **`DisplyElement d = ...` 가 한 곳도 없으므로 그 파일을 지우고 `implements` 에서 이름을 떼도 프로그램이 그대로 돈다.** Day30 의 「만들어 놓고 어느 것도 타입으로 쓰지 않은 상태」가 반복된 것인데 이번에는 **그것을 요구하는 문제 자체가 없다** — 화면이 여러 종류가 되어 「화면들을 한 통에 담아 전부 다시 그리게」 할 때 비로소 타입이 된다. Day30~32 의 대비(「그것을 필요로 하는 코드가 생긴 곳에서만 온다」)가 여기서 한 번 더 확인된다 → [[observer-pattern]] · [[cohesion]]
- **한 클래스가 인터페이스 둘을 구현하는 첫 실물이 Day44 다 — 그리고 그 둘이 서로를 부른다** — Day29 의 3장에서 다중 구현을 문법으로 배웠고, `CurrentConditionsDisplay implements Observer, DisplyElement` 가 그것이 실제로 쓰인 자리다. 흥미로운 것은 두 약속이 독립이 아니라는 것이다 — `update()`(`Observer` 쪽)의 마지막 줄이 `display()`(`DisplyElement` 쪽)를 부른다. **`extends` 로는 이 조합을 만들 수 없다** — 「알림을 받는 것」과 「화면인 것」은 상속 계층 한 줄에 놓을 수 없는 두 성질이고, 여러 개 붙을 수 있다는 성질이 값을 내는 것이 이런 자리다 → [[multiple-inheritance]] · [[observer-pattern]]
- **인터페이스를 고치는 순간 구현 전부를 고친다** — Day31 이 메뉴 경로를 넘기려고 `void execute();` 를 `void execute(Stack menuPath);` 로 바꾼다. 그 한 줄 때문에 `AbstractCommand`·`HelpCommand`·`HistoryCommand`·`App` 이 같이 바뀌고, **`menuPath` 를 쓰지 않는 명령들까지 그 인자를 받는다.** 「컴파일러가 빠뜨림을 목록으로 확인해 준다」의 반대편 값이다 — 확인해 주는 대신 **전부 고치게 만든다.** 다만 이것이 언제나는 아니다 — 하루 뒤 Day32 가 `List` 에 `iterator()` 를 더하면서 구현을 하나도 고치지 않는데, `AbstractList` 가 그 자리를 받았기 때문이다(위의 「중간 층이 받으면 된다」). **약속과 구현 사이에 층이 있으면 시그니처 변경이 그 층에서 멈춘다** → [[interface-segregation-principle]] · [[open-closed-principle]] · [[default-method]] · [[abstract-class]]

## 함께 보는 개념

- [[abstract-class]] — 같은 회차에서 겹쳐 쓰는 짝
- [[coupling]] — 인터페이스가 줄이는 것을 세는 축
- [[default-method]] — 인터페이스에 몸통이 들어오는 문법
- [[multiple-inheritance]] — 인터페이스가 여러 개 붙을 수 있다는 성질
- [[polymorphism]] — 인터페이스가 만들어 내는 성질
- [[method-overriding]] — 추상메서드를 채우는 방법
- [[inheritance]] — `extends` 와 갈리는 축
- [[static-member]] — 상수필드와 정적메서드의 근거
- [[access-modifier]] — `public` 이 강제되는 자리
- [[encapsulation]] — 인터페이스가 감추는 것과 여는 것
- [[dynamic-array]] — 이 인터페이스의 첫 구현
- [[linked-list]] — 같은 약속을 지키는 다른 구조
- [[cohesion]] — 결합을 이름에서 약속으로 바꾸기 전의 상태
- [[grasp]] — Low Coupling 이 이름으로 남아 있던 자리
- [[package]] — 표준 라이브러리와 이름이 겹치는 문제
- [[object-cloning]] — 메서드 없는 인터페이스의 예
- [[annotation]] — `@Override` 가 붙는 문법
- [[class]] — 인터페이스가 아닌 쪽
- [[generalization]] — 약속이 아니라 코드를 위로 올리는 쪽
- [[template-method-pattern]] — 인터페이스가 담을 수 없는 것(순서)을 담는 구조
- [[refactoring]] — 인터페이스를 도입하는 작업의 단위
- [[dispatch-table]] — 이 약속이 실제로 타입이 되는 자리
- [[dependency-inversion-principle]] — 추상 타입으로 받는 것을 원칙으로 세운 이름
- [[interface-segregation-principle]] — 약속의 크기를 재는 원칙
- [[hash-based-collection]] — 구현체들을 한 통에 담는 자료구조
- [[iterator-pattern]] — `List` 가 처음으로 타입이 되는 자리
- [[observer-pattern]] — 약속을 만든 쪽이 그 약속을 부르는 형태
- [[nested-class]] — 구현을 약속 안쪽으로 감추는 방법

## 출처

- [[2024-06-26-Day23]] — 인터페이스의 개념(「서로 다른 두 객체를 연결해주는 역할」)부터 상수필드·추상메서드·디폴트메서드·정적메서드·private 메서드까지 다섯 종류의 멤버를 한 회차에 정리했다. 실습에서는 `ArrayList` 와 `LinkedList` 가 이미 갖고 있던 같은 이름의 메서드들을 `List` 인터페이스 여섯 줄로 묶고, 중복되는 `size` 를 `AbstractList` 로 올려 「인터페이스로 받고 이후 상속을 한다」는 조합을 만들었다. 2.1 의 코드가 아직 없는 `AbstracList` 를 `extends` 하고 있는 것과, 선언 목록에 인터페이스에 둘 수 없는 「public 메소드」가 들어 있는 것이 이 필기의 오류다
- [[2024-07-03-Day28]] — 추상 클래스를 키우다가 인터페이스에 도착하는 경로를 배웠다. 「추상메서드만 있을 경우, 객체 사용규칙을 정의하는 인터페이스로 전환 가능하다 / 추상클래스 안에 일반 메서드가 있다면, 인터페이스로 전환이 불가능하다」가 그 조건이고, `abstract class Sorter` 가 `interface Sorter` 로 줄어드는 것으로 확인했다. 뒤쪽 조건은 `default` 메서드가 생긴 뒤로는 반쪽이 되었으며, 실제로 전환을 막는 것은 인스턴스 필드다
- [[2024-07-05-Day29]] — 인터페이스만으로 한 회차를 채워 **선언 규칙을 컴파일 오류 목록으로** 정리했다. `public abstract void m1();`·`abstract void m2();`·`public void m3();`·`void m4();` 네 표기가 전부 같은 것이고 「(default) 아니다!」라는 것, `private`·`protected` 는 몸통 없이 쓸 수 없다는 것, 구현 쪽에서는 `public` 을 생략하면 막힌다는 것, 다 채우지 못한 클래스는 `abstract` 로 선언해야 한다는 것, `MyInterface obj = null` 은 되고 `new MyInterface()` 는 안 된다는 것이 여기서 규칙 문장이 된다. 1장은 세 노동자 클래스로 결합도의 앞뒤를 보여 주고(→ [[coupling]]), 2.2~2.3 은 디폴트 메서드와 private 메서드를(→ [[default-method]]), 3장은 인터페이스의 다중 상속·다중 구현을(→ [[multiple-inheritance]]) 다룬다. 필드를 「인스턴스를 생성할 수 없기 때문에 상수만」이라 설명한 것은 인과가 뒤집힌 자리다
- [[2024-07-08-Day30]] — 인터페이스를 **두 개 만들고 어느 것도 타입으로 쓰지 않은** 회차다. 앞 절은 Day23 의 `List`/`AbstractList` 를 다시 만들면서 「공통 코드를 추상 메소드로 선언한다」로 적어 약속과 코드를 한 단계로 뭉갰고, 뒤 절은 `interface Command { void execute(); }` 를 새로 만들지만 `App` 은 구현 클래스 넷을 필드로 들고 `switch` 로 갈래를 낸다. 일반화 단계에서 자식의 `implements Command` 가 `extends AbstractCommand` 로 바뀌어 **약속이 선언에서 사라지고**, 「인터페이스를 사용하여 직접구현」이라 적힌 `HelpCommand` 에는 `implements` 가 아예 없다. `contains` 가 `ArrayList` 에만 있어 팀원 목록을 약속 타입으로 들 수 없게 된 것도 이 회차다
- [[2024-07-09-Day31]] — **전날 만들어 두고 쓰지 않던 `Command` 가 하루 만에 타입이 되는 회차다.** `App` 이 구현 클래스 넷을 필드로 들고 `switch` 로 갈래를 내던 것이 `Map<String, Command> commandMap` 과 `commandMap.get(menuTitle).execute()` 로 바뀌어, `processMenu` 에서 구현 클래스 이름이 전부 사라진다. 그 통에 담기려면 `Command` 여야 하므로 전날 `implements` 가 없던 `HelpCommand` 가 여기서 `implements Command` 를 얻는다 — **약속을 안 지킨 것이 드러나는 시점이 「그 타입으로 담을 때」**라는 것이 하루 사이의 대비로 남는다. 반대로 `List` 는 그대로 방치되어, 목록을 `App` 이 만들어 명령에 넘기면서도 타입이 `ArrayList`·`LinkedList` 구현 클래스다. 그리고 `void execute()` 를 `void execute(Stack menuPath)` 로 바꾸느라 구현 전부와 `App` 을 같이 고쳤고, `menuPath` 를 쓰지 않는 `HelpCommand`·`HistoryCommand` 도 그 인자를 받게 되었다. SOLID 다섯 원칙을 같은 노트 앞쪽에서 배우면서 그 중 ISP 에 걸린 것이다
- [[2024-07-10-Day32]] — **`List` 가 처음으로 타입이 되는 회차다.** `Iterator` 약속을 새로 만들고 그것을 구현하는 `ListIterator` 가 `private List list` 를 필드로 들며, `AbstractList.iterator()` 가 `new ListIterator(this)` 로 자신을 `List` 로 넘긴다 — 반복자는 배열인지 노드 사슬인지 알 필요가 없고 `size()`·`get(int)` 만 부르므로 **약속으로 받을 이유가 처음 생겼다.** 전날까지 「만들어 놓고 타입으로 쓰지 않은」 상태였던 이유가 그것을 요구하는 코드가 없었기 때문이라는 것이 이 대비로 확인된다. 동시에 `List` 에 `Iterator iterator();` 를 더했는데도 `ArrayList`·`LinkedList` 가 한 줄도 바뀌지 않아 — `AbstractList` 가 구현을 받았다 — **약속을 늘리는 비용이 중간 층에서 멈추는 경우**가 처음 나온다. 다만 `toArray()` 를 지우지 않아 순회 경로가 둘인 약속이 되었다
- [[2024-07-26-Day44]] — 인터페이스를 셋 만들면서 **부르는 방향이 뒤집힌 첫 약속**이 나온다. `Observer` 는 `WeatherData` 쪽에서 선언하고 `WeatherData` 가 `notifyObservers()` 안에서 부르는 것이라, Day23~32 의 「내가 부를 것의 이름」과 용법이 반대다 — 구현만 남의 코드이고 호출 시점은 선언한 쪽이 정한다. `Subject` 는 인터페이스로 만들어 놓고 옵저버가 구체 클래스 `WeatherData` 를 필드로 들어 **타입으로 쓰이지 않았고**, `DisplyElement` 는 한술 더 떠 **어디에서도 타입으로 쓰이지 않는다** — `implements` 선언과 `update()` 안의 `display()` 호출뿐이라 지워도 프로그램이 돈다. 반대로 `implements Observer, DisplyElement` 는 Day29 3장에서 문법으로만 배운 다중 구현이 실제로 쓰인 첫 자리이며, 두 약속이 독립이 아니라 한쪽 메서드가 다른 쪽 메서드를 부른다
