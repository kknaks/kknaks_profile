---
type: concept
id: nested-class
title: 중첩 클래스 (Nested Class)
aliases:
  - 중첩 클래스
  - 중첩클래스
  - 내부 클래스
  - 내부클래스
  - inner class
  - nested class
  - 정적 멤버 클래스
  - 정적멤버클래스
  - static nested class
  - 정적 중첩 클래스
  - 정적 중첩클래스
  - 인스턴스 멤버 클래스
  - 인스턴스 중첩 클래스
  - 인스턴스 중첩클래스
  - non-static nested class
  - 로컬 클래스
  - 로컬클래스
  - local class
  - 바깥 클래스
up:
  - 2024-07-10-Day32
  - 2024-07-11-Day33
  - 2024-07-16-Day36
tags:
  - 자바
  - 클래스설계
  - 문법
  - 캡슐화
---

# 중첩 클래스 (Nested Class)

**클래스 안에 선언한 클래스.** 종류가 넷으로 갈리는데 갈리는 축은 「어디에 썼는가」로 보이고 실제로는 **바깥 인스턴스에 대한 숨은 참조를 갖는가**다. 그 참조가 있으면 바깥의 필드와 메서드를 자기 것처럼 쓸 수 있고, 없으면 필요한 것을 넘겨받아야 한다.

## 정의

| 종류 | 선언 위치 | 바깥 인스턴스 참조 | 바깥 것에 닿는 법 | 밖에서 만드는 법 |
|---|---|---|---|---|
| **정적 멤버 클래스** | 클래스의 멤버 + `static` | **없다** | 생성자·매개변수로 받는다 | `new A.X()` |
| **인스턴스 멤버 클래스** | 클래스의 멤버 | 있다 | `바깥클래스명.this` | `outer.new X()` |
| **로컬 클래스** | 생성자·메서드 안 | 있다(인스턴스 메서드라면) | `바깥클래스명.this` + 그 메서드의 지역변수 | 불가 — 그 메서드 안에서만 |
| **익명 클래스** | 식(`new ...{}`) 안 | 있다 | 같음 → [[anonymous-class]] | 식 자체가 생성이다 |

Day32 의 분류가 앞 두 개를 「멤버클래스」로 묶는다 — 「중첩클래스는 크게 클래스의 멤버로서 선언되는 멤버클래스와 메서드내부에 선언 되는 중첩클래스로 나뉜다 / 멤버클래스는 다시 인스턴스 멤버 클래스와 정적멤버클래스로 나뉜다」. **하루 뒤 회차는 같은 넷을 종류별로 한 장씩 나눠 「개념 → 접근제한자 → 정의와 인스턴스 생성 → 바깥에 접근하기 → 안쪽에 접근하기」의 같은 다섯 항목으로 훑는다** — 분류는 그대로고 각 칸의 문법이 채워진다.

```java
[public] class A{
    [public | private] static class B{      // 정적 멤버 클래스
    }
    [public | private] class B{             // 인스턴스 멤버 클래스
    }
    public void method(){
        class B2{ }                          // 로컬 클래스 — 지정자를 붙일 수 없다
    }
}
```

**멤버 클래스에는 접근 지정자를 붙일 수 있고 로컬 클래스에는 붙일 수 없다.** 멤버는 「누가 볼 수 있나」를 말할 대상이 있지만 로컬은 지역변수와 같아서 그 블록 밖에서는 이름조차 없다 — 하루 뒤 회차가 그 이유를 「**로컬 변수처럼** 로컬클래스에는 접근 제한자를 붙일 수 없다」로 적었다 → [[access-modifier]] · [[variable-scope]]

멤버 클래스에는 **넷이 다 붙는다** — 최상위 클래스가 `public` 과 생략 둘뿐인 것과 다르다. 「클래스의 멤버이기 때문에 필드나 메서드처럼 접근 제한자를 붙일수 있다」가 그 이유다.

```java
public class StaticNestedClass {
    private static class A1 {}
    static class A2 {}          //(package-private)
    protected static class A3 {}
    public static class A4 {}
}
```

그리고 **정적 멤버 클래스 안에는 `static` 멤버와 인스턴스 멤버가 모두 들어간다** — 초기화 블록까지 양쪽 다 된다. `static` 이 붙은 클래스라고 안이 전부 `static` 이 되는 것이 아니다.

```java
class A2 {
    static class X {
        // top level class 처럼 스태틱 멤버 선언 가능
        static int v1;
        static void m1() {}
        static {}

        // top level class 처럼 인스턴스 멤버 선언 가능
        int v2;
        void m2() {}
        {}
    }
}
```

### 인스턴스를 만드는 문법이 종류를 가른다

**`static` 이 붙은 쪽은 `new A.Y()`, 안 붙은 쪽은 `outer.new X()` 다.** 하루 뒤 회차가 두 줄을 나란히 놓고 하나를 주석으로 막아 그 차이를 보였다.

```java
public static void main(String[] args) {
    // 레퍼런스 선언
    A.X obj;
    A.Y obj2;

    // 인스턴스 생성
    obj2 = new A.Y();      // 스태틱 중첩 클래스는 바깥 클래스의 인스턴스가 없어도 생성할 수 있다.
    // obj = new A.X();    // 컴파일 오류! 바깥 클래스의 인스턴스 주소 없이 생성 불가!

    // 1) 바깥 클래스의 인스턴스 준비
    A outer = new A();

    // 2) inner class의 인스턴스를 생성할 때도 바깥 클래스의 인스턴스 주소가 필요하다.
    obj = outer.new X();
    A.X obj3 = new A().new X();
}
```

**`new` 앞에 점이 오는 문법은 이 자리에만 있다.** `outer.new X()` 의 `outer.` 는 「어느 바깥 인스턴스에 붙일 것인가」를 지정하는 자리이고, Day33 이 컴파일 결과를 주석으로 적어 그 실체를 보였다 — 「`obj = new A.X(outer);`」. **인수 목록에 있던 것이 점 앞으로 간 것**이라, 24일 앞선 회차의 `Calculator.plus(c1, 2)` → `c1.plus(2)` 와 같은 이동이다 → [[this-reference]]

바깥 클래스 **안에서** 만들 때는 그 자리에 이미 `this` 가 있어 `this.new X()` 가 되고, 필드나 메서드처럼 `this.` 를 생략할 수 있다.

```java
class C {
    static void m1() {
        // 스태틱 멤버는 인스턴스 멤버를 사용할 수 없다.
        X obj;                    // 레퍼런스 선언은 가능!
        //  obj = this.new X();   // 컴파일 오류! 인스턴스 생성 불가능!
    }

    void m2() {
        X obj = this.new X();     // 인스턴스 메서드에는 this 가 있다
        X obj2 = new X();         // 인스턴스 필드나 메서드와 마찬가지로 this를 생략할 수 있다.
    }

    class X { void test() {} }
}
```

**`static` 메서드에서 레퍼런스 선언은 되고 생성만 막힌다.** 타입 이름을 쓰는 데는 인스턴스가 필요 없고, 만드는 데만 필요하다 — 「이름이 안 보인다」와 「대상이 없다」가 다른 문제라는 것이 이 두 줄에 붙어 있다 → [[static-member]]

### 바깥에 닿는 것과 바깥에서 닿는 것

같은 회차가 방향을 나눠 정리한다. **정적 중첩 클래스에서 바깥으로 가는 길**은 세 경우로 갈린다.

```java
class B2 {
    static int v1;
    static void m1() {}
    int v2;
    void m2() {}

    static class X {
        void test() {
        //Case1
        B2.v1 = 100;
        B2.m1();
        //Case2
        v1 = 200;
        m1();
        //Case3
        // v2 = 100; // 컴파일 오류!
        // m2(); // 컴파일 오류!
        }
    }
}
```

Case1 과 Case2 는 **같은 것을 두 표기로 쓴 것**이다(「클래스 X도 B2의 클래스 멤버이기 때문에 바깥클래스 이름을 생략할 수 있다」). Case3 이 막히는 이유를 Day33 이 정확히 적었다 — 「**바깥 클래스의 인스턴스 주소를 담는 B2.this 라는 인스턴스 멤버가 없다**」. 이름이 안 보이는 것이 아니라 **가리킬 인스턴스가 없다** → [[variable-scope]] · [[static-member]]

인스턴스 중첩 클래스로 바꾸면 Case3 이 열리고, 그때 쓰는 것이 `B2.this` 다. Day33 이 컴파일러가 만드는 것을 주석으로 펼쳐 적었다.

```java
class B2 {
    int v2;
    void m2() { System.out.println("B2.v2 = " + this.v2); }
    class X {
        // 바깥 객체의 주소를 저장할 빌트인 필드
        //    B2 this$0;

        // inner 객체를 생성할 때 바깥 객체의 주소를 받는 생성자
        //    public X(B2 p) {
        //      this.this$0 = p;
        //    }
        void test() {
        System.out.println(B2.this.v2); // ---> this$0.v2
        B2.this.m2();
        }
    }
}
```

**`B2.this` 는 문법이고 `this$0` 은 그것이 컴파일된 결과다.** Day32 가 「컴파일러: 바깥 클래스의 인스턴스 주소를 전달하는 코드로 자동 변환」이라는 한 줄로 넘긴 것을 하루 뒤 회차가 **필드 이름과 생성자 시그니처까지** 적었다 → [[this-reference]]

**반대 방향 — 바깥에서 중첩 클래스를 쓰는 것**은 `static` 여부로 갈린다.

| 바깥의 코드 | 정적 중첩 클래스 | 인스턴스 중첩 클래스 |
|---|---|---|
| `static` 메서드 | `new X()` 도 `X.test2()` 도 된다 | **레퍼런스 선언만** |
| 인스턴스 메서드 | 된다 | 된다 (`this.new X()`) |

`static` 메서드에서 정적 중첩 클래스의 **인스턴스**를 만들 수 있다는 것이 놓치기 쉽다 — 「`static` 문맥에서는 인스턴스 멤버를 못 쓴다」는 규칙과 부딪히는 것처럼 보이지만, 정적 중첩 클래스는 **바깥 인스턴스를 필요로 하지 않으므로** 그냥 `new` 하면 된다.

```java
class C {
    static void m1() {
        // 같은 스태틱 멤버는 사용 가능!
        X obj = new X();
        obj.test();//인스턴스 메서드는 객체생성 후 호출가능
        X.test2(); //static 메서드는 바로 호출 가능
    }
    static class X {
        void test() {}
        static void test2() {}
    }
}
```

## 사용 예시

**같은 `ListIterator` 를 네 방식으로 다시 쓰는 것이 Day32 회차의 전부다.** 줄어드는 것을 보면 축이 드러난다.

정적 멤버 클래스는 **컬렉션을 손으로 받아야 한다.**

```java
public abstract class AbstractList implements List {
  public Iterator iterator() {
    //중첩클래스의 생성자에 넘겨줄 인스턴스가 필요하다.
    return new ListIterator(this);
  }

  static public class ListIterator implements Iterator {
    private List list;
    private int cursor;

    // private List와 바깥 List를 동기화하기 위해
    // 생성자가 필요하다.
    public ListIterator(List list) {
      this.list = list;
    }

    @Override
    public boolean hasNext() { return cursor < list.size(); }
    @Override
    public Object next() { return list.get(cursor++); }
  }
}
```

인스턴스 멤버 클래스로 바꾸면 **필드 하나와 생성자와 대입문이 한꺼번에 사라진다.**

```java
public abstract class AbstractList implements List {
  // 컴파일러: 바깥 클래스의 인스턴스 주소를 전달하는 코드로 자동 변환
  public Iterator iterator() {
    return new ListIterator();
  }

  public class ListIterator implements Iterator {
    private int cursor;

    @Override
    public boolean hasNext() {
      return cursor < AbstractList.this.size();
    }

    @Override
    public Object next() {
      return get(cursor++);
    }
  }
}
```

**`private List list` 가 없어진 것이 이 비교의 결론이다.** Day32 가 정적 버전의 생성자에 「private List와 바깥 List를 동기화하기 위해」라는 주석을 달았는데, 인스턴스 멤버 클래스에서는 **동기화할 두 개가 애초에 없다** — 사본을 받아 두는 것이 아니라 바깥 인스턴스를 그대로 보기 때문이다. 줄어든 세 줄은 편의가 아니라 **어긋날 수 있는 상태가 하나 없어진 것**이다 → [[object-reference]]

그리고 `next()` 에서 `AbstractList.this.` 가 사라졌다. Day32 가 그 규칙을 코드 주석으로 적었다 — 「중첩 클래스 안에 해당 필드나 메서드가 없다면 바깥클래스명.this 생략 가능」 → [[this-reference]]

**로컬 클래스는 그 메서드 안에서만 존재한다** — 선언이 `iterator()` 의 몸통으로 들어간다.

```java
public Iterator iterator() {
  public class ListIterator implements Iterator {   // ← public 때문에 컴파일 오류
    private int cursor;

    @Override
    public boolean hasNext() { return cursor < AbstractList.this.size(); }
    @Override
    public Object next() { return get(cursor++); }
  }
  return new ListIterator();
}
```

**네 버전 중 이것만 돌지 않는다** — 로컬 클래스에는 접근 지정자를 붙일 수 없다(아래 「경계와 오해」). 지정자를 지우면 나머지는 인스턴스 멤버 버전과 같고, 달라지는 것은 **이 클래스를 `iterator()` 밖에서는 아무도 쓸 수 없다**는 것뿐이다.

마지막 버전은 이름까지 지운다 → [[anonymous-class]]

### 로컬 클래스가 바깥 메서드의 변수를 쓰는 코드는 Day36 에서 나온다

**Day36 이 같은 인터페이스를 로컬 클래스로 두 번 구현해 나란히 놓는데, 그 둘의 차이가 포획이다.**

```java
public class Factory {
  // 1.일반 클래스1
  static InterestCalculator create(double rate) {
    class GeneralClass implements InterestCalculator {
      private double rate;

      public GeneralClass(double rate) {
        this.rate = rate;
      }

      @Override
      public double compute(int money) {
        return money * (1 + rate);
      }
    }
    return new GeneralClass(rate);
  }

  // 1.일반 클래스2
  // 로컬 클래스로 선언 할 경우 클래스가 속한 static메서드의
  // 변수값(여기서는rate) 사용할 수 있다.
  static InterestCalculator create(double rate) {
    class GeneralClass2 implements InterestCalculator {
      @Override
      public double compute(int money) {
        return money * (1 + rate);
      }
    }
    return new GeneralClass2();
  }
}
```

**필드 하나와 생성자와 대입문이 사라진다 — Day32 가 정적 멤버 클래스 → 인스턴스 멤버 클래스에서 보인 것과 똑같은 세 줄이다.** 다만 없어진 이유가 다르다. 거기서는 바깥 **인스턴스**를 숨은 참조로 보게 된 것이고, 여기서는 바깥 **메서드의 지역변수**를 컴파일러가 복사해 넣은 것이다. 그리고 둘 다 `static` 메서드 안에 있으므로 이 로컬 클래스들에는 `Factory.this` 가 없다 — **닿을 수 있는 것은 그 메서드의 변수뿐**이고, Day33 이 「성질은 자기 선언이 아니라 담긴 자리가 정한다」로 적은 것의 실제 코드가 이것이다 → [[static-member]] · [[call-by-value]]

`GeneralClass` 쪽의 `private double rate` 는 매개변수와 이름이 같아 `compute` 안의 `rate` 는 **필드**를 읽는다(포획이 아니다). 두 버전을 갈라 보이려면 그렇게 이름을 겹쳐 쓸 수밖에 없고, 그래서 이 비교는 **같은 이름이 서로 다른 것을 가리키는 두 코드**의 대비가 된다 → [[variable-scope]] · [[field-hiding]]

같은 장이 이 사다리를 익명 클래스와 람다로 두 칸 더 올라간다 → [[anonymous-class]] · [[lambda-expression]]

**14일 전 회차의 `Node` 가 이미 이 문법이었다.** 그때는 `LinkedList` 밖에 홀로 있던 클래스가 안으로 들어갔고, 이번 노트는 그 코드를 「중첩 클래스 예시」로 다시 꺼내 이름을 붙인다.

```java
public class LinkedList extends AbstractList {
  private Node first;
  private Node last;

  public static class Node {
    Object value;
    Node next;

    public Node(Object value) {
      this.value = value;
    }
  }
}
```

**`Node` 는 정적이고 `ListIterator` 는 정적이 아니어도 된다** — 노드는 바깥 리스트의 상태를 하나도 쓰지 않고, 반복자는 바깥 리스트를 계속 물어봐야 한다. 같은 문법의 두 쓰임이 한 프로젝트 안에 나란히 있다 → [[linked-list]]

## 왜 중요한가

**관계가 선언 위치에 나타난다.** `Node` 가 톱레벨 클래스면 「어느 리스트의 노드인가」를 알 방법이 없고 같은 패키지 누구나 `new Node(...)` 를 쓴다. 안으로 넣으면 이름이 `LinkedList.Node` 가 되어 **읽는 사람이 찾을 곳이 한 곳으로 줄어든다.** Day32 가 「특정클래스와만 관계를 맺을 경우 중첩클래스로 선언하는 것이 유지보수에 유리하다」로 적은 것이 이것이다 → [[cohesion]] · [[package]]

**바깥의 `private` 에 닿을 수 있다 — 캡슐화를 깨지 않고 협력자를 만드는 유일한 길이다.** 반복자는 컬렉션의 내부를 훑어야 하므로, 톱레벨 클래스로 두면 컬렉션이 `get`·`size` 를 `public` 으로 열어야 한다(이 실습이 실제로 그렇다). 중첩으로 넣으면 그 메서드들을 좁혀도 반복자는 계속 볼 수 있다. **반복자 패턴이 「내부 구조를 감춘다」를 지키려면 중첩이 필요하다** → [[encapsulation]] · [[iterator-pattern]] · [[access-modifier]]

**`static` 을 붙이느냐가 메모리와 생명주기를 정한다.** 인스턴스 멤버 클래스의 객체는 바깥 인스턴스를 가리키고 있으므로, 그 객체가 살아 있는 동안 **바깥도 회수되지 않는다.** 반복자 하나가 리스트 전체를 붙잡는 것은 순회하는 동안이니 문제가 없지만, 노드 수만큼 만들어지는 `Node` 가 그랬다면 참조 하나씩을 더 들고 다녔을 것이다 → [[garbage-collection]] · [[static-member]]

## 경계와 오해

- **중첩 클래스의 `static` ≠ 필드·메서드의 `static`** — 필드에서 `static` 은 「클래스당 하나」인데 클래스에서는 **「바깥 인스턴스 참조가 없다」**다. `public static class Node` 는 하나만 존재하는 것이 아니라 `LinkedList` 가 노드마다 `new` 한다. 같은 키워드가 다른 축을 말하므로, 23일에 걸쳐 배운 「몇 개 있나」로 읽으면 이 자리에서 어긋난다 → [[static-member]] · [[instance]]
- **로컬 클래스에 접근 지정자를 붙일 수 없다 — Day32 의 3) 적용 코드가 컴파일되지 않는다** — `iterator()` 안의 `public class ListIterator implements Iterator` 다. 로컬 클래스에 붙일 수 있는 것은 `abstract`·`final`·`strictfp` 뿐이고 `public`·`private`·`protected`·`static` 은 전부 컴파일 오류다. **바로 위의 문법 골격은 `class B1 { }` 로 맞게 적혀 있다** — 앞 두 절의 적용 코드를 복사해 오면서 지정자가 따라 들어온 자리이고, 네 버전 중 이 하나만 돌지 않는다. **하루 뒤 회차가 이 규칙을 별도 항목으로 세우고 네 지정자를 하나씩 주석으로 막아 두었다**(`// private class A1 {}` … `class A2 {}` … `// public class A4 {}`) — 전날 코드가 어긋난 자리를 다음 날 규칙으로 확정한 셈이다 → [[access-modifier]] · [[variable-scope]]
- **`AbstractList.this.size()` 가 필드가 아니라 메서드라서 살아 있다** — 이틀 전 회차에서 `ArrayList`·`LinkedList` 가 부모와 같은 이름의 `size` 를 다시 선언해 `AbstractList.size` 는 끝까지 `0` 이다. 여기서 `AbstractList.this.size` **(필드)** 를 읽었다면 `hasNext()` 가 언제나 `false` 가 되어 목록이 아무것도 찍지 않는다. `size()` **(메서드)** 는 재정의된 자식 것이 불리므로 정확한 값이 온다 — **괄호 두 글자가 죽은 필드를 비켜 간 것**이고, 필드 은닉이 「정상으로 보이는 상태로 남는다」의 실제 사례가 하나 더 늘었다 → [[field-hiding]] · [[method-overriding]] · [[polymorphism]]
- **「바깥클래스를 생성해야만 내부 클래스를 생성할 수 있다」는 Day32 의 코드로는 확인되지 않고, 하루 뒤 회차가 그 문법을 꺼낸다** — 그 규칙이 문법으로 보이는 것은 **밖에서** 만들 때인데, Day32 의 네 버전은 전부 바깥 클래스 **안에서** `new ListIterator()` 로 끝난다(그 자리에 이미 `this` 가 있어 컴파일러가 넘겨 준다). 그래서 그 시점에는 문장이 맞아도 **왜 「생성해야만」인지가 코드에 없었다.** Day33 이 `outer.new X()` · `new A().new X()` · `this.new X()` 세 형태를 놓고 `new A.X()` 를 컴파일 오류로 막아 보이면서 그 빈칸이 채워진다 — **이 개념에서 「밖에서 만드는 법」을 코드로 처음 본 것이 Day33 이다** → [[this-reference]]
- **「바깥 클래스의 객체가 생성된 이후에 인스턴스 중첩클래스를 **선언**해야한다」에서 막히는 것은 선언이 아니라 생성이다** — 바로 아래 코드가 스스로 반증한다. `A.X obj;` 가 `A outer = new A();` **보다 먼저** 쓰여 있고 컴파일된다. 타입 이름을 쓰는 데는 바깥 인스턴스가 필요 없고 `new` 에만 필요하다. 같은 노트의 `static void m1()` 이 `X obj;` 는 두고 `this.new X()` 만 주석으로 막은 것도 같은 구별이다 — **「선언」과 「생성」을 뭉치면 `static` 메서드에서 레퍼런스를 왜 선언할 수 있는지가 설명되지 않는다** → [[variable]]
- **`outer2` 가 선언되지 않아 `B2.this` 데모가 컴파일되지 않는다 — 하필 그 예시의 요점이 사라지는 자리다** — `B2.X inner2 = outer2.new X();` 의 `outer2` 는 어디에도 없다. 이 `main` 이 두 인스턴스를 만들려 한 이유는 **같은 `X` 코드가 각자의 바깥을 본다**는 것, 즉 `this$0` 이 인스턴스마다 다르다는 것을 보이려는 것이었는데(주석에 `--> new X(outer)` · `--> new X(outer2)` 로 짝을 적어 두었다), **두 번째 인스턴스가 없어서 그 대비가 성립하지 않는다.** 그리고 컴파일 오류이므로 `main` 전체가 돌지 않아 `B2.this.v2` 가 `100` 을 찍는 것조차 확인되지 않는다 — **한 줄이 빠진 것이 아니라 그 절이 증명하려던 것 전부가 빠졌다** → [[instance]]
- **로컬 클래스에 `static` 을 붙일 수 없다 — 「Static 로컬 클래스」라는 말은 성립하지 않는다** — Day33 이 「Static 로컬 클래스는 static과 동일한 성질을 같는다 / 인스턴스 로컬 클래스는 static과 동일한 성질을 같는다」라고 두 줄을 적었는데 **같은 말이 두 번**이다(뒷줄은 앞줄을 복사하며 「static」이 남은 것으로 보인다 — 뜻이 통하려면 「인스턴스와 동일한 성질」이어야 한다). 그리고 애초에 클래스에 붙는 키워드로 두 종류가 갈리는 것이 아니다. 갈리는 것은 **그 로컬 클래스가 어느 메서드 안에 있는가**다 — `static` 메서드 안이면 `this` 가 없으니 바깥 인스턴스에 못 닿고(정적 멤버 클래스와 같은 성질), 인스턴스 메서드 안이면 닿는다(인스턴스 멤버 클래스와 같은 성질). **로컬 클래스에는 지정자도 `static` 도 붙일 수 없고, 성질은 자기 선언이 아니라 담긴 자리가 정한다** → [[access-modifier]] · [[static-member]]
- **「top level class와 동일하게 사용된다」가 세 자리에서 다르다** — 정적 멤버 클래스가 톱레벨처럼 쓰인다는 말이 대개 맞지만, ① 이름이 `A2.X` 로 **한정**되어 `import` 나 바깥 이름 없이는 부를 수 없고, ② `private`·`protected` 를 붙일 수 있어 **밖에서 이름조차 못 쓰게** 만들 수 있고(톱레벨은 `public`·생략 둘뿐이다), ③ 파일명이 클래스명과 같아야 하는 규칙을 받지 않는다(`.class` 는 `A2$X.class` 로 따로 나온다). **「동일하게」로 외우면 `private static class` 를 왜 만들 수 있는지가 설명되지 않는다** → [[access-modifier]] · [[java-compilation-unit]] · [[class-file-format]]
- **인스턴스 멤버 클래스가 정적 멤버 클래스보다 항상 낫지 않다** — 필드와 생성자가 없어진 대신 **숨은 필드가 하나 생겼다.** 「세 줄 줄었다」와 「보이지 않는 참조가 붙었다」는 같은 사건의 앞뒤이고, 그래서 바깥의 상태를 안 쓰는 중첩 클래스에는 `static` 을 붙이는 것이 기본이다. Day32 는 네 방식을 나란히 보여 주면서 **어느 것을 고를지의 기준을 적지 않았다** → [[garbage-collection]]
- **중첩 ≠ 상속** — `Node` 가 `LinkedList` 안에 있다고 `LinkedList` 의 필드를 물려받지 않는다. 인스턴스 멤버 클래스조차 바깥 것을 **물어봐야** 닿는다(`AbstractList.this.size()`). 「안에 있다」와 「이다」는 다른 관계이고, 실제로 `ListIterator` 는 `AbstractList` 안에 있으면서 `Iterator` 를 `implements` 한다 → [[inheritance]] · [[interface]]
- **정적 멤버 클래스는 바깥의 `static` 멤버만 그냥 쓸 수 있다** — 인스턴스 멤버는 대상이 없으므로 못 쓴다. 그래서 Day32 의 정적 버전이 `List` 를 생성자로 받아야 했다. 「받아야 한다」가 불편이 아니라 **`static` 을 골랐다는 것의 필연적 결과**다 → [[static-member]]
- **정적 멤버 클래스만 `static` 멤버를 가질 수 있다** — 하루 뒤 회차가 정적 멤버 클래스 안에 `static int v1` · `static void m1()` · `static {}` 과 인스턴스 멤버를 **함께** 선언해 「top level class 처럼」 된다는 것을 보였다. 인스턴스 멤버·로컬·익명 클래스는 상수(`static final`)만 둘 수 있다(Java 16 이전 규칙이다) — 바깥 인스턴스에 얽혀 있는 것에 클래스 단위 저장소를 두면 소속이 모순되기 때문이다. **그래서 「`static` 클래스 안은 전부 `static`」도 「중첩 클래스에는 `static` 멤버를 못 둔다」도 둘 다 틀리고, 갈림은 그 클래스가 `static` 인가에 달려 있다** → [[static-member]]
- **로컬 클래스가 쓰는 지역변수는 사실상 `final` 이어야 한다 — 그 코드는 Day36 에서 처음 나온다** — 메서드가 끝나면 지역변수는 사라지는데 객체는 남을 수 있으므로, 컴파일러가 **값을 복사해 넣는다.** 그래서 나중에 그 변수를 바꾸면 두 값이 갈리게 되고, 그것을 막으려고 변경을 금지한다. Day32·Day33 은 이 형태를 만들지 않아 제약을 만나지 않았고(Day33 의 로컬 클래스 장은 빈 클래스 `class A2 {}` 하나로 끝난다), **닷새 뒤 Day36 이 정확히 그 코드를 쓴다** — 「로컬 클래스로 선언 할 경우 클래스가 속한 static메서드의 변수값(여기서는rate) 사용할 수 있다」는 주석과 함께다(아래 「사용 예시」의 `GeneralClass2`). 그러면서도 **`rate` 를 바꿀 수 없다는 쪽은 여전히 적히지 않았다** — 쓸 수 있다는 것만 확인하고 넘어간 자리다 → [[call-by-value]] · [[variable-scope]] · [[lambda-expression]]
- **로컬 클래스와 익명 클래스의 차이는 「이름」과 「두 번 만들 수 있나」뿐이다** — 로컬은 이름이 있으니 같은 메서드에서 여러 번 `new` 할 수 있고 생성자를 가질 수 있다. Day32 가 네 번째를 「추가)」로 붙인 것은 순서상 맞다 — **익명은 로컬에서 이름을 더 지운 것**이다 → [[anonymous-class]]
- **`static public class` 와 `public static class` 는 같다** — Day32 가 순서를 바꿔 썼다. 지정자 순서는 문법이 아니라 관례이고, 관례는 접근 지정자를 앞에 둔다.
- **소스에서 감춰져도 바이트코드에는 이름이 있다** — 중첩 클래스는 별도의 `.class` 파일이 되어 `LinkedList$Node.class`·`AbstractList$1.class` 로 나온다. 「외부에는 중첩관계를 감춤으로써 코드의 복잡성을 줄일 수 있다」는 **읽는 사람에 대한 이야기**이고, 컴파일 결과물에서 사라지는 것은 아니다 → [[class-file-format]] · [[compilation]]
- **Day36 의 `Factory` 는 컴파일되지 않고, 그 하나의 원인이 실행 코드까지 끌고 간다** — 「일반 클래스1」과 「일반 클래스2」를 나란히 보이려고 **`static InterestCalculator create(double rate)` 를 같은 이름 같은 매개변수로 두 번** 선언했다. 매개변수 목록이 같으면 오버로딩이 아니라 **중복 정의**이므로 `already defined in class Factory` 로 걸린다. 그리고 그 장의 실행 코드는 `Factory.create1(0.025)`·`Factory.create2(0.025)` 를 부르는데 **`create1`·`create2` 라는 메서드는 어디에도 없다** — 익명 클래스 쪽은 `create3`·`create4`, 람다 쪽은 `create5`·`create6` 으로 번호가 붙어 있으니 **1·2 번만 번호를 붙이지 않은 채 남은 것**이다. 두 오류는 같은 원인이고 이름을 `create1`·`create2` 로 고치면 함께 사라진다. 그대로면 `Test.main` 이 컴파일되지 않아 **여섯 방식이 같은 결과를 낸다는 그 장의 결론이 실행으로 확인되지 않는다** → [[method]] · [[compilation]]
- **중첩 인터페이스에는 `static` 을 쓸 필요가 없다 — 언제나 `static` 이다** — Day36 이 `public class Test` 안에 `interface Player{ void play(); }` 를 그냥 선언하는데, 이것은 **정적 멤버**다(중첩 인터페이스와 중첩 enum 은 `static` 이 암묵으로 붙는다). 그래서 `main` 이 `static` 인데도 `Player` 를 타입으로 쓸 수 있다. 클래스는 `static` 을 붙였는가로 성질이 갈리는데(위 첫 항목) **인터페이스는 갈릴 여지가 없다** — 인터페이스에는 인스턴스 상태가 없으니 바깥 인스턴스에 매달 이유도 없다 → [[interface]] · [[static-member]]
- **중첩을 늘리면 파일 하나가 커진다** — 네 버전 모두 `AbstractList` 한 파일 안에 반복자가 들어간다. 반복자가 여럿 필요해지거나 길어지면 그 파일이 두 가지 일을 하게 되고, **「관계를 드러낸다」와 「한 파일이 한 가지를 한다」가 반대 방향으로 당긴다** → [[cohesion]]

## 함께 보는 개념

- [[anonymous-class]] — 이름까지 지운 네 번째 형태
- [[iterator-pattern]] — Day32 가 중첩으로 감싼 대상
- [[static-member]] — 같은 키워드가 다른 뜻을 갖는 자리
- [[this-reference]] — 바깥 인스턴스를 가리키는 문법
- [[variable-scope]] — 층이 늘어난 뒤 이름이 어디서 풀리는지
- [[java-compilation-unit]] — 톱레벨 클래스와 갈리는 파일명 규칙
- [[linked-list]] — `Node` 를 정적 중첩으로 둔 쪽
- [[field-hiding]] — 괄호 두 글자로 비켜 간 지뢰
- [[access-modifier]] — 로컬 클래스에는 붙일 수 없는 것
- [[encapsulation]] — 중첩이 지켜 주는 것
- [[class]] — 중첩되는 단위
- [[abstract-class]] — 이 실습에서 반복자를 품은 클래스
- [[instance]] — 바깥과 안의 개수 관계
- [[class-file-format]] — 중첩이 컴파일 결과에 남는 모양
- [[garbage-collection]] — 숨은 참조가 만드는 문제
- [[cohesion]] — 중첩을 고르는 근거이자 대가
- [[lambda-expression]] — 로컬 클래스와 같은 포획 제약을 물려받은 다음 문법
- [[functional-interface]] — Day36 이 중첩으로 선언한 인터페이스들의 조건
- [[method]] — Day36 의 `create` 가 두 번 선언돼 걸리는 규칙

## 출처

- [[2024-07-10-Day32]] — 「클래스 내부에 선언한 클래스」에서 시작해 정적 멤버·인스턴스 멤버·로컬 클래스와 익명 구현 객체까지 네 종류를 정리하고, **같은 `ListIterator` 를 네 방식으로 다시 쓰며** 차이를 보였다. 정적 버전은 `private List list` 와 생성자가 필요하고 인스턴스 버전은 그 셋이 사라지며 `AbstractList.this.size()` 로 바깥을 물어본다 — 「컴파일러: 바깥 클래스의 인스턴스 주소를 전달하는 코드로 자동 변환」이라는 주석이 그 차이의 실체를 적은 한 줄이다. 로컬 클래스 적용 코드에 `public` 이 붙어 **그 버전만 컴파일되지 않고**, 네 방식 중 무엇을 고를지의 기준은 적히지 않았다. 14일 전 회차에 이미 `public static class Node` 로 써 두었던 문법이 여기서 이름을 얻는다
- [[2024-07-11-Day33]] — **하루 뒤 회차가 같은 넷을 종류마다 한 장씩 다시 훑으며 문법을 채운다.** 접근 지정자가 멤버 클래스에는 넷 다 붙고(`private static class A1` ~ `public static class A4`) 로컬 클래스에는 「로컬 변수처럼」 하나도 못 붙는다는 것, 정적 멤버 클래스 안에는 `static` 멤버와 인스턴스 멤버가 함께 들어간다는 것, 그리고 **인스턴스를 만드는 문법**(`new A.Y()` 는 되고 `new A.X()` 는 컴파일 오류, `outer.new X()` · `new A().new X()` · `this.new X()`)이 여기서 처음 코드로 나온다. 바깥에 닿는 길은 Case1/2/3 으로 갈라 정적 중첩 클래스가 인스턴스 멤버에 못 닿는 이유를 「바깥 클래스의 인스턴스 주소를 담는 B2.this 라는 인스턴스 멤버가 없다」로 적고, 반대로 `static` 메서드에서는 정적 중첩 클래스는 `new` 할 수 있고 인스턴스 중첩 클래스는 **레퍼런스 선언만** 된다는 것을 보였다. `B2.this` 의 컴파일 결과를 `B2 this$0;` 필드와 `public X(B2 p)` 생성자로 펼쳐 적은 것이 Day32 의 주석 한 줄을 이어받은 자리다. 다만 그 데모의 `main` 에 `outer2` 가 선언되지 않아 **컴파일되지 않고**, 로컬 클래스 장은 「Static 로컬 클래스 / 인스턴스 로컬 클래스」 두 줄이 같은 말이며, 익명 클래스 장은 두 줄만 남고 잘려 있다
- [[2024-07-16-Day36]] — 람다식을 배우는 회차인데 그 사다리의 **첫 칸이 로컬 클래스**여서 이 개념이 다시 쓰인다. Day32·Day33 에 없던 코드가 여기서 처음 나온다 — **로컬 클래스가 자기를 감싼 `static` 메서드의 지역변수를 쓰는 것**(`GeneralClass2` 가 `create(double rate)` 의 `rate` 를 읽는다)이고, 필기가 그것을 「로컬 클래스로 선언 할 경우 클래스가 속한 static메서드의 변수값(여기서는rate) 사용할 수 있다」로 적었다. 바로 위의 `GeneralClass` 는 같은 값을 `private double rate` 필드 + 생성자로 받으므로 두 버전의 차이가 **필드·생성자·대입문 세 줄**이 되고, Day32 가 정적↔인스턴스 멤버 클래스로 보인 것과 같은 모양이 로컬 클래스에서는 포획으로 일어난다. 붙잡은 변수를 바꿀 수 없다는 제약은 적히지 않았다. 그 `Factory` 는 **`create` 를 같은 시그니처로 두 번 선언해 컴파일되지 않고**, 실행 코드가 부르는 `create1`·`create2` 는 존재하지 않는다. 인터페이스를 클래스 안에 선언하는 형태(`class Test` 안의 `interface Player`)도 이 회차에서 처음 쓰인다
