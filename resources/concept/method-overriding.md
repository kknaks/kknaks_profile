---
type: concept
id: method-overriding
title: 메서드 오버라이딩 (Method Overriding)
aliases:
  - 메서드 오버라이딩
  - 메소드 오버라이딩
  - 오버라이딩
  - method overriding
  - override
up:
  - 2024-06-24-Day21
  - 2024-06-25-Day22
  - 2024-06-26-Day23
  - 2024-07-01-Day26
  - 2024-07-03-Day28
  - 2024-08-05-Day48
tags:
  - oop
  - java
  - 상속
---

# 메서드 오버라이딩 (Method Overriding)

자식 클래스가 부모에게서 물려받은 메서드를 **같은 선언부로 다시 정의**하는 것. 재정의하면 부모의 것은 가려지고 자식의 것이 실행된다.

## 정의

지켜야 하는 조건이 있는데, **세 가지가 서로 다른 방향으로 묶여 있다.**

| 항목 | 규칙 |
|---|---|
| 이름 · 매개변수 | **완전히 같아야** 한다 — 하나라도 다르면 오버로딩이 된다 |
| 반환 타입 | 같거나 **더 좁은 타입**이어도 된다 (공변 반환 타입) |
| 접근 제어자 | 같거나 **더 넓혀야** 한다 (`public` → `private` 불가) |
| 예외 선언 | 같거나 **더 줄여야** 한다 |

「선언부가 같아야 한다」로 뭉쳐 외우면 뒤의 셋이 왜 한쪽 방향으로만 허용되는지 안 보인다. 기준은 하나다 — **부모 타입으로 부르던 코드가 그대로 돌아가야 한다.** 반환 타입이 좁아지고 접근이 넓어지고 예외가 줄어드는 것은 부르는 쪽이 손해 볼 일이 없는 변화다.

`@Override` 는 컴파일러에게 "재정의 의도" 를 알리는 표시다. 붙이면 오타로 새 메서드를 만드는 실수를 컴파일 시점에 잡는다 → [[annotation]]

가려진 부모 메서드를 굳이 부르려면 `super.메서드()` 를 쓴다.

## 사용 예시

```java
public static class Parent {
    public void method1() { System.out.println("Parent-method1()"); }
    public void method2() { System.out.println("Parent-method2()"); }
}

public static class Child extends Parent {
    @Override
    public void method2() { System.out.println("Child-method2()"); }
    public void method3() { System.out.println("Child-method3()"); }
}
```

`Child` 는 `method2` 만 재정의했다. `method1` 은 부모 것이 그대로 살아 있고, `method3` 은 자식에만 있다.

### 첫 오버라이딩은 상속을 배우기 전에 온다

**일주일 앞선 회차에서 이미 네 개를 재정의한다.** [[object-class]] 를 배우는 자리인데, `extends` 를 쓰지 않은 클래스도 이미 부모가 있으므로 **상속 문법을 하나도 안 쓰고 오버라이딩만 하게 된다** → [[inheritance]]

```java
@Override
public String toString() {                       // 해시값 대신 필드를 찍는다
  return "My [name=" + name + ", age=" + age + "]";
}

@Override
public boolean equals(Object obj) { ... }        // 주소 비교 대신 내용 비교

@Override
public int hashCode() {                          // 인스턴스별 값 대신 내용 기준 값
  return Objects.hash(age, name, working);
}

@Override
public Score clone() throws CloneNotSupportedException {
  return (Score) super.clone();                  // 권한을 열고 타입을 되돌린다
}
```

**네 개가 재정의하는 이유가 다 다르다.** 앞의 셋은 물려받은 구현이 쓸 만하지 않아서 바꾸는 것이고, `clone()` 은 **구현을 바꾸려는 것이 아니다** — `super.clone()` 이 실제 복제를 그대로 하고, 재정의의 목적은 `protected` 를 `public` 으로 넓히는 것과 반환 타입을 `Object` 에서 `Score` 로 좁히는 것뿐이다 → [[object-cloning]] · [[access-modifier]]

그래서 이 한 메서드가 위 표의 **아래 세 줄을 한꺼번에** 보여 준다.

| | 부모(`Object`) | 자식(`Score`) | 방향 |
|---|---|---|---|
| 반환 타입 | `Object` | `Score` | 좁혔다 — 허용 |
| 접근 제어자 | `protected` | `public` | 넓혔다 — 허용 |
| 예외 | `throws CloneNotSupportedException` | 그대로 | 줄일 수 있었는데 안 줄였다 |

`super.` 도 여기서 처음 쓰인다 — 「가려진 부모 메서드를 굳이 부르는」 경우가 아니라 **가려 놓고 그것에 일을 맡기는** 형태다.

### 표준 라이브러리가 이미 해 둔 것을 확인하는 자리

바로 다음 회차가 **남이 재정의해 둔 것**을 처음 관찰한다. 직접 재정의하는 것이 아니라 `String` 이 해 둔 결과를 보는 것이다.

```java
Object obj = new String("Hello");
String x1 = (String) obj;
String x2 = obj.toString();
System.out.println(x2);         // Hello    ← 클래스이름@해시값 이 아니다
System.out.println(x1 == x2);   // true
```

필기가 그 이유를 정확히 적었다 — **「String의 toString()이 오버라이딩 되었기 때문에 Hello를 리턴한다」.** 재정의하지 않았다면 `java.lang.String@7ad041f3` 같은 것이 찍혔을 것이고, 문자열을 `println` 에 넣으면 글자가 나오는 그 당연한 동작이 **누가 재정의해 둔 결과**라는 것이 여기서 드러난다 → [[object-class]] · [[string-comparison]]

**그리고 `x1 == x2` 가 `true` 인 것은 재정의의 내용까지 말해 준다.** `String.toString()` 은 새 문자열을 만들지 않고 `this` 를 그대로 돌려준다. **재정의는 「무엇을 돌려줄까」를 고르는 일**이고, 불변 객체에서는 자기 자신이 답이 될 수 있다 → [[immutability]]

### 가릴 것이 없는 재정의 — 인터페이스 구현

**바로 다음 회차의 `@Override` 여섯 개는 가리는 구현이 없다.** 인터페이스의 추상메서드는 몸통이 없으므로 「부모의 것이 가려지고 자식의 것이 실행된다」가 아니라 **비어 있던 자리를 채우는 것**이다.

```java
public class ArrayList extends AbstracList {
  @Override
  public void add(Object obj) { ... }      // List 의 void add(Object obj); 를 채운다
```

세 가지가 앞의 예들과 갈린다.

| | `Object` 재정의 (Day21·Day22) | 인터페이스 구현 (Day23) |
|---|---|---|
| 물려받은 구현 | 있다 (해시값을 찍는 `toString`) | **없다** |
| `super.메서드()` | 부를 수 있다 (`super.clone()`) | 부를 것이 없다 |
| 빠뜨리면 | 컴파일된다 — 부모 것이 조용히 불린다 | **컴파일이 막힌다** |

**그래서 `@Override` 의 값이 반대 방향이다.** `Object` 쪽에서는 「재정의가 아니라 새 메서드를 만들어 버린 실수」를 잡아 주는 장치였는데, 인터페이스 쪽에서는 그 실수가 어차피 「추상메서드를 안 채웠다」로 걸린다. 여기서 `@Override` 는 안전장치가 아니라 **읽는 사람에게 「이건 약속을 채운 것」이라고 알려 주는 표시**다 → [[interface]] · [[annotation]]

**이레 뒤 회차는 이 표의 두 줄을 같은 메서드로 보여 준다.** `Sorter.sort` 가 처음에는 몸통이 있었고,

```java
public abstract class Sorter {
  public void sort(int[] values) {};      // 몸통이 있다 — 안 채우면 이것이 불린다
}
```

```java
public class MergeSort extends Sorter {   // sort 를 재정의하지 않았는데 컴파일된다
  void merge(int arr[], int l, int m, int r) { }
}
```

그 다음 `abstract` 를 붙이자 같은 클래스가 재정의를 강제하게 된다.

```java
public abstract class Sorter {
  public abstract void sort(int[] values);   // 이제 MergeSort 가 컴파일 에러다
}
```

**부모가 `Object` 인지 인터페이스인지가 갈림길이 아니었다.** 갈리는 것은 **물려받은 자리에 실행할 코드가 있는가**이고, 그것이 한 클래스 안에서 키워드 하나로 뒤집히는 것을 이 회차가 보여 준다 → [[abstract-class]]

### 33일 뒤 — 같은 메서드를 한 형태에서는 덮어야 하고 다른 형태에서는 덮으면 안 된다

쓰레드 회차의 `run()` 이 그 자리다. Day48 은 작업 쓰레드를 만드는 두 형태를 나란히 놓는데, **`Runnable` 을 넘기는 쪽은 `Thread.run()` 을 재정의하지 않고** `Thread` 를 상속하는 쪽은 재정의한다 → [[thread]]

```java
// ① 넘긴다 — Thread 의 run() 을 그대로 쓴다
Thread t1 = new Thread(new Task());

// ② 덮는다 — Thread 의 run() 을 가린다
class WorkerThread extends Thread {
  @Override
  public void run() { /* 쓰레드가 실행할 코드 */ }
}
```

`Thread.run()` 은 **몸통이 있는 보통 메서드**이고 그 몸통이 「넘겨받은 `Runnable` 이 있으면 그것을 실행한다」다. 그래서 ① 이 도는 이유가 **부모의 구현이 일부러 남아 있는 것**이고, ② 는 그 구현을 버리는 것이다. **둘을 겹쳐 `new Thread(task){ public void run(){…} }` 로 쓰면 `task` 는 영원히 실행되지 않는다** — 그것을 실행하던 코드를 덮었기 때문이다.

그리고 위 「빠뜨리면」 칸에 세 번째 답이 붙는다.

| | Day28 `Sorter.sort` (빈 몸통) | Day48 `Thread.run()` |
|---|---|---|
| 부모의 구현 | `{}` — 아무 일도 하지 않는다 | 넘겨받은 `Runnable` 을 실행한다 |
| 재정의를 빠뜨리면 | 정렬해 달라고 부른 코드가 **정렬 없이 성공한다** | `new Thread()` 에는 실행할 것이 없어 **쓰레드가 뜨자마자 끝난다** |
| 오류로 드러나는가 | 아니다 | 아니다 — 게다가 **다른 흐름**이라 부른 쪽에는 흔적도 없다 |

**Day28 이 「자기가 만든 부모라 더 위험하다」였던 자리가, 여기서는 「남이 만든 부모인데 더 위험한」 쪽으로 옮겨 간다** — 실패가 다른 실행 흐름 안에서 조용히 끝나므로 호출부의 다음 줄은 정상적으로 계속된다 → [[thread-state]] · [[process]]

## 왜 중요한가

**부모 타입으로 호출해도 자식의 구현이 실행된다.** 이것이 [[polymorphism]] 을 만드는 두 축 중 하나다 — 나머지 한 축은 [[type-casting]] 의 자동 타입변환이다.

오버라이딩이 없으면 상속은 코드 재사용에서 끝나고, 자식마다 다르게 동작시키려면 호출부에서 타입을 분기해야 한다.

**그리고 재정의는 「이름을 고를 자유를 버리는 일」이다.** 인스턴스 내용을 찍는 메서드를 `print()` 라고 이름 붙이면 내 코드에서만 쓸 수 있고, `toString()` 으로 재정의하면 `System.out.println(obj)` 가 그것을 부른다. 중복 판정을 `isSame()` 으로 만들면 아무도 안 부르고, `equals()` 로 만들면 `HashSet` 이 부른다. **남의 코드가 내 클래스를 다루게 되는 대가로 이름을 내주는 것**이고, 이것이 오버라이딩이 다형성과 별개로 갖는 값이다 → [[object-class]] · [[hash-based-collection]]

## 경계와 오해

- **오버라이딩 ≠ 오버로딩** — 오버로딩은 **같은 이름, 다른 매개변수**를 한 클래스 안에 여러 개 두는 것이고 **컴파일 시점**에 결정된다. 오버라이딩은 **같은 선언부**를 상속 관계에서 다시 정의하는 것이고 **실행 시점**에 결정된다.
- **둘을 가르는 실수가 실제로 나는 자리가 `equals` 다** — `equals(Object obj)` 대신 `equals(My obj)` 로 쓰면 편해 보이는데, 매개변수가 다르므로 **재정의가 아니라 메서드가 하나 더 생긴다.** `HashSet` 은 `Object` 를 받는 쪽을 부르므로 내가 쓴 코드가 전혀 실행되지 않고, **오류도 나지 않는다.** `@Override` 를 붙였다면 그 자리에서 컴파일이 막힌다 → [[object-equality]] · [[annotation]]
- **반환 타입은 「같아야」가 아니라 「좁혀도 된다」** — Day26 시점에는 조건을 「이름·매개변수·반환타입이 같아야 한다」로 배웠는데, 그보다 앞선 회차의 `clone()` 이 이미 `Object` → `Score` 로 좁혀 놓고 있었다. 규칙을 「전부 같아야 한다」로 외우면 그 코드가 왜 컴파일되는지 설명되지 않는다. **넓히는 것은 안 되고 좁히는 것은 된다**가 정확한 형태다 → [[object-cloning]]
- **「접근 제어자를 좁힐 수 없다」에 가장 자주 걸리는 곳은 인터페이스 구현이다** — 인터페이스의 메서드는 `public` 을 안 써도 `public` 이므로, 구현 클래스에서 `public` 을 빼면 **패키지 전용으로 좁히는 것**이 되어 컴파일 에러다. 인터페이스 회차의 필기가 「구현클래스에서는 추상메서드에 대한 오버라이딩(**public 타입으로**) 을 시행하여야 한다」로 못을 박은 것이 이 규칙이고, 선언 쪽에서 생략할 수 있는 것을 구현 쪽에서도 생략할 수 있다고 읽으면 걸린다 → [[interface]] · [[access-modifier]]
- **「접근 제어자를 좁힐 수 없다」는 클래스를 상속할 때도 똑같이 걸린다 — Day48 의 `void run()`** — 위 항목이 「가장 자주 걸리는 곳은 인터페이스 구현이다」인데, `Thread.run()` 은 `public` 이므로 자식에서 `public` 을 빼면 그 자리에서 컴파일 에러다. 같은 회차가 이름 있는 클래스에서는 세 번 `public void run()` 으로 맞게 쓰고 **익명 클래스 판에서만** 빠뜨렸다 — 중괄호 안이 「그 자리에서만 쓰는 지역」처럼 보여서 생기는 실수이고, **재정의 규칙은 익명 클래스에서도 그대로 적용된다** → [[anonymous-class]] · [[access-modifier]]
- **재정의해야 하는지 아닌지가 「같은 메서드」에서도 뒤집힌다** — `Thread.run()` 은 상속 형태에서는 반드시 덮어야 하고, `Runnable` 을 넘기는 형태에서는 **덮으면 넘긴 것이 실행되지 않는다.** 「부모 메서드는 필요하면 덮는다」로만 알면 이 갈림이 안 보인다 — 부모의 구현이 **자식이 쓸 코드**인 경우가 있고, `Thread.run()` 처럼 **위임 코드가 들어 있는 메서드**가 그 전형이다 → [[thread]]
- **접근 제어자를 넓히는 것이 재정의의 목적이 될 수 있다** — 「좁힐 수 없다」는 제약으로만 읽히지만, `clone()` 재정의는 **넓히는 것 자체가 목적**이다. 제약이 아니라 도구로 쓰이는 자리다 → [[access-modifier]]
- **재정의하지 않아도 컴파일되고 실행된다** — `Object` 에서 물려받은 여섯 개는 언제나 동작하므로, 재정의를 빠뜨린 것이 오류로 드러나지 않는다. `toString()` 이 해시값을 찍고 `equals()` 가 내용을 안 보는 결과만 나온다. **「구현하라」고 강제하는 장치는 따로 있다** → [[abstract-class]] · [[object-class]]
- **내가 만든 부모라고 다르지 않다 — 그리고 이쪽이 더 위험하다** — `MergeSort` 가 `sort` 를 재정의하지 않아도 컴파일되고, `display(sorter, values)` 는 부모의 **빈 몸통**을 불러 아무 일도 하지 않는다. `toString()` 을 안 고친 것은 출력이 못생겨지는 정도지만, 이쪽은 **정렬해 달라고 부른 코드가 정렬 없이 성공으로 끝난다.** 「빈 몸통을 물려주는 것」과 「구현을 강제하는 것」이 `abstract` 한 글자로 갈린다 → [[abstract-class]] · [[polymorphism]]
- **필드는 오버라이딩되지 않는다** — 재정의 대상은 메서드뿐이다. 같은 이름의 필드를 자식에 두면 부모 것을 가릴 뿐(hiding)이고, 접근은 **변수의 선언 타입**을 따른다. 그래서 두 필드가 한 인스턴스 안에 동시에 존재하고, `@Override` 같은 안전장치도 없다 → [[field-hiding]]
- **`static` 메서드는 오버라이딩이 아니다** — 클래스에 묶이므로 재정의가 아니라 은닉이다.
- **재정의는 「하는 것」과 「이미 되어 있는 것」이 반씩이다** — 필기가 재정의를 배우는 자리는 직접 쓰는 쪽인데, 실제로 코드가 의존하는 재정의는 대개 표준 라이브러리가 이미 해 둔 것이다. `String.toString()`·`String.equals()`·`String.hashCode()` 셋이 그렇고, **`StringBuffer` 는 그중 어느 것도 재정의하지 않았다.** 「자바가 알아서 해 준다」가 아니라 **클래스마다 결정이 다르고 그 결정이 코드의 동작을 바꾼다** → [[string-builder]] · [[object-equality]]
- **`final` 이면 재정의할 수 없다** — `Object.getClass()` 가 그 예다. 필기가 여섯 메서드를 나란히 놓았지만 재정의 가능 여부가 갈리고, `getClass()` 가 못 바뀌는 덕분에 `equals` 안에서 그 결과를 믿을 수 있다 → [[class-metadata]]

## 함께 보는 개념

- [[inheritance]] — 오버라이딩의 전제
- [[polymorphism]] — 오버라이딩이 만드는 성질
- [[abstract-class]] — 오버라이딩을 강제하는 장치
- [[annotation]] — `@Override` 가 속한 문법
- [[object-class]] — 재정의 대상 여섯 개가 사는 곳
- [[object-equality]] — 매개변수 타입을 틀리기 쉬운 자리
- [[hash-code]] — `equals` 와 짝으로 재정의하는 것
- [[object-cloning]] — 반환 타입과 접근 권한을 바꾸는 재정의
- [[access-modifier]] — 넓히는 방향만 허용되는 축
- [[class-metadata]] — 재정의할 수 없는 메서드의 예
- [[string-builder]] — 일부러 재정의하지 않은 클래스
- [[immutability]] — `this` 를 돌려줄 수 있게 하는 성질
- [[interface]] — 가릴 구현이 없는 재정의가 나오는 자리
- [[thread]] — 재정의 여부가 형태에 따라 뒤집히는 `run()` 이 있는 곳
- [[anonymous-class]] — 접근 지정자를 빠뜨리기 쉬운 자리

## 출처

- [[2024-06-24-Day21]] — 상속 문법을 배우기 전에 `Object` 의 `toString`·`equals`·`hashCode`·`clone` 을 재정의하는 것으로 오버라이딩을 먼저 만났다. `clone()` 재정의가 반환 타입을 `Object` → `Score` 로 좁히고 접근 권한을 `protected` → `public` 으로 넓히며, `super.clone()` 에 실제 일을 맡기는 형태라 「선언부가 같아야 한다」는 규칙의 실제 모양이 여기서 드러난다. 「override를 한다고 컴파일러에게 알려주면 오타로 인한 버그를 줄일수 있다」도 이 자리다
- [[2024-06-25-Day22]] — 직접 재정의하는 것이 아니라 **`String` 이 이미 해 둔 재정의를 관찰**했다. 「String의 toString()이 오버라이딩 되었기 때문에 Hello를 리턴한다」가 그것이고, `x1 == x2` 가 `true` 인 것으로 그 재정의가 `this` 를 돌려준다는 것까지 드러난다. 같은 회차의 `StringBuffer` 가 `hashCode()` 를 재정의하지 않아 내용이 바뀌어도 값이 그대로인 것이 나란히 놓인 대비다
- [[2024-06-26-Day23]] — 인터페이스의 추상메서드를 채우는 것도 오버라이딩이라는 것을 배웠다. 「구현 객체는 인터페이스에서 선언된 추상메소드을 오버라이딩을 통해 구체적인 실행 코드가 들어있다」이고, 그때 **`public` 을 반드시 붙여야 한다**(「오버라이딩(public 타입으로)」)는 것이 「접근 제어자를 좁힐 수 없다」의 실제 걸림이다. 실습의 `@Override` 여섯 개는 **가려지는 부모 구현이 없는** 재정의라 앞선 회차들과 성격이 갈린다
- [[2024-07-01-Day26]] — 오버라이딩의 조건과 `@Override`, `super.` 로 부모 메서드를 부르는 법을 배웠다. 조건을 「이름·매개변수·반환타입이 같아야 한다」로 정리했는데, 일주일 전 `clone()` 이 이미 반환 타입을 좁혀 놓았으므로 **반환 타입만은 한 방향으로 열려 있다**는 것이 두 회차를 나란히 놓아야 보인다
- [[2024-08-05-Day48]] — `Thread.run()` 을 **덮는 형태와 덮지 않는 형태를 한 절에 나란히** 놓는다(`Thread` 상속 / `Runnable` 을 넘기기). 부모의 구현이 「넘겨받은 `Runnable` 을 실행한다」라서 **재정의를 빠뜨리면 쓰레드가 뜨자마자 아무 일도 없이 끝나고**, 그 실패가 다른 실행 흐름 안에 있어 부른 쪽에는 흔적도 남지 않는다 — Day28 의 「빈 몸통을 물려받아 조용히 통과하는」 형태가 한 단계 더 조용해진 자리다. 그리고 익명 클래스 판의 `void run()` 이 **접근을 좁힌 재정의**라 컴파일되지 않는데, 같은 회차의 이름 있는 클래스 셋은 `public void run()` 으로 맞게 썼다 — 「좁힐 수 없다」가 인터페이스 구현뿐 아니라 클래스 상속에서도 걸린다는 것이 여기서 드러난다. 필기는 「Override를 구현 후 직접 start()를 호출하여 사용한다」로 형태만 적고 **부모의 `run()` 에 무엇이 들어 있는지**는 다루지 않았다
- [[2024-07-03-Day28]] — 같은 메서드(`Sorter.sort`)를 **몸통 있는 상태와 추상 메서드 상태로 차례로** 만들어 보며, 재정의를 빠뜨렸을 때 조용히 통과하는 쪽과 컴파일이 막히는 쪽을 한 클래스 안에서 확인했다. `MergeSort` 가 `sort` 를 재정의하지 않고도 컴파일되어 빈 몸통이 불리는 것이 「재정의하지 않아도 컴파일된다」의 가장 아픈 형태다 — 표준 라이브러리가 아니라 **자기가 만든 부모**이고, 결과가 「출력이 이상하다」가 아니라 「정렬이 안 된다」다
