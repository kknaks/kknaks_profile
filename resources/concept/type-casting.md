---
type: concept
id: type-casting
title: 타입 변환 (Type Casting)
aliases:
  - 타입 변환
  - 타입변환
  - 형변환
  - 업캐스팅
  - 다운캐스팅
  - upcasting
  - downcasting
  - type casting
up:
  - 2024-06-24-Day21
  - 2024-06-25-Day22
  - 2024-07-01-Day26
tags:
  - oop
  - java
  - 상속
---

# 타입 변환 (Type Casting)

상속 관계에 있는 클래스 사이에서 참조 변수의 타입을 바꾸는 것. 부모 쪽으로 가는 **업캐스팅**과 자식 쪽으로 되돌리는 **다운캐스팅**이 있다.

## 정의

```java
Parent p = new Child();      // 업캐스팅 — 자동. 캐스팅 연산자가 필요 없다
Child  c = (Child) p;        // 다운캐스팅 — 명시적. (Child) 를 직접 써야 한다
```

방향에 따라 규칙이 다르다.

| | 방향 | 문법 | 안전한가 |
|---|---|---|---|
| **업캐스팅** | 자식 → 부모 | 자동 | 항상 안전 |
| **다운캐스팅** | 부모 → 자식 | `(자식타입)` 명시 | **실행 시점에 깨질 수 있다** |

업캐스팅한 변수로는 **부모가 선언한 멤버만** 부를 수 있다. 자식에만 있는 멤버를 쓰려면 다운캐스팅해서 되돌려야 한다.

## 사용 예시

`instanceof` 로 실제 타입을 확인한 뒤 내려간다.

```java
public void handle(Vehicle vehicle) {
    vehicle.run();                       // 부모 멤버 — 업캐스팅 상태로 호출 가능

    if (vehicle instanceof Bus) {
        Bus bus = (Bus) vehicle;         // 확인했으니 안전하게 다운캐스팅
        bus.openBackDoor();              // Bus 에만 있는 멤버
    }
}
```

`instanceof` 없이 `(Bus) vehicle` 을 바로 쓰면, 들어온 게 `Taxi` 일 때 `ClassCastException` 으로 터진다 → [[instanceof-operator]]

### `Object` 가 끼면 캐스팅이 선택이 아니게 된다

[[object-class]] 가 모든 것의 조상이므로 **업캐스팅은 아무 대입에서나 일어난다.**

```java
Object obj = new My();          // (Object) 를 쓰지 않았는데 업캐스팅이다
```

그리고 그 대가를 받는 쪽이 낸다. 같은 회차의 세 자리가 전부 다운캐스팅으로 되돌리고 있다.

```java
// equals — 매개변수가 Object 라서
public boolean equals(Object obj) {
  ...
  My other = (My) obj;
  //파라미터가 type이 Object type이기 때문에 형변환을 적용한다.
  return age == other.age && Objects.equals(name, other.name);
}

// 컬렉션에서 꺼낼 때 — toArray() 가 Object[] 를 주므로
Object[] list = set.toArray();
for (Object obj : list) {
  Student student = (Student) obj;
  ...
}

// clone — super.clone() 의 반환 타입이 Object 라서
return (Score) super.clone();
```

**셋 다 `instanceof` 검사가 없다.** 앞의 것은 바로 위에서 `getClass()` 로 이미 확인했고, 뒤의 둘은 넣은 것이 무엇인지 코드를 쓴 사람이 알고 있다. 「확인하고 내려간다」가 원칙이지만 **실제 코드에서는 확인이 다른 형태로 되어 있거나 아예 없다** → [[object-equality]] · [[hash-based-collection]] · [[object-cloning]]

### 다운캐스팅해야 하는 이유는 「보이는 창」 하나로 설명된다

바로 다음 회차가 그것을 한 문장으로 적는다 — **「원래 타입으로 형변환을 해야 해당 타입의 클래스의 메소드를 호출 할 수 있다」.**

```java
Object obj = new String("Hello"); // 인스턴스 주소가 100이라 가정하자;
String x1 = (String) obj; // x1 <--- 100
System.out.println(obj == x1);    // 같은 인스턴스다
```

`obj` 로는 `length()`·`replace()` 를 부를 수 없고 `x1` 로는 부를 수 있다. **인스턴스는 하나뿐인데 부를 수 있는 것이 다르다** — 그것을 정하는 것이 인스턴스가 아니라 변수의 선언 타입이라는 것이 `obj == x1` 한 줄에 들어 있다.

그런데 **부를 수 있는 것 중 하나는 캐스팅 없이도 자식 것이 실행된다.**

```java
String x2 = obj.toString(); // Object 에 선언된 메서드라 obj 로도 부를 수 있다
System.out.println(x2);     // Hello  ← String 이 재정의한 것이 실행됐다
```

**둘의 차이가 「선언이 어디 있나」다.** `toString()` 은 `Object` 에 선언이 있으니 창에 보이고, 실행되는 것은 실제 타입의 재정의본이다. `length()` 는 `Object` 에 선언이 없으니 창에 아예 보이지 않아 캐스팅이 필요하다 → [[method-overriding]] · [[polymorphism]] · [[object-class]]

## 왜 중요한가

**업캐스팅이 [[polymorphism]] 의 두 축 중 하나다.** 부모 타입 변수가 자식 인스턴스를 가리킬 수 있어야 "타입 하나로 여러 구현을 받는" 코드가 성립한다.

다운캐스팅은 반대로 **다형성을 잠깐 포기하는 행위**다. 자식의 고유 기능이 필요해서 내려가는 것인데, 이게 잦아진다는 건 설계가 부모 쪽에 충분한 추상을 못 세웠다는 신호로 읽는 편이 낫다.

**다만 표준 라이브러리 쪽에서는 그 신호가 읽히지 않는다.** `equals(Object)` 와 `toArray()` 는 「무엇이든 받는다」를 택한 대가로 다운캐스팅을 **모든 구현에 강제한다.** 이것은 설계가 부족해서가 아니라 **뿌리가 하나인 계층에서 최상위 타입을 매개변수로 쓰면 필연적으로 생기는 비용**이다. `HashSet<Student>` 라고 타입을 적어 두었는데도 `toArray()` 가 `Object[]` 를 주는 것이 그 비용이 남아 있는 자리다 → [[inheritance]] · [[data-type]]

## 경계와 오해

- **다운캐스팅은 컴파일러가 안 막아 준다** — 문법상 상속 관계이기만 하면 통과하고, 실제 인스턴스가 그 타입이 아니면 **실행 시점에 `ClassCastException`** 이 난다. 컴파일이 됐다는 것이 안전하다는 뜻이 아니다.
- **캐스팅은 객체를 바꾸지 않는다** — 인스턴스는 그대로고 **보는 창(변수 타입)만** 바뀐다. 업캐스팅했다고 자식의 메서드가 사라진 것이 아니라 그 창에서 안 보일 뿐이다. 그래서 [[method-overriding]] 된 메서드는 업캐스팅 상태에서도 자식 것이 실행된다.
- **기본형 형변환과 다른 이야기다** — `int` → `double` 같은 것은 값 자체를 바꾸지만, 참조형 캐스팅은 값을 안 건드린다 → [[type-promotion]]
- **기본 타입은 `Object` 로 업캐스팅할 수 없다** — `Object` 는 참조 타입 계층의 뿌리이고 기본 타입 여덟 개는 그 계층 밖이다. 그래서 `int` 를 `Object` 변수에 담을 수 없고 `int` 에 `getClass()` 를 부를 수도 없다. **「모든 것의 조상」의 「모든 것」이 참조 타입만**이라는 것이 여기서 드러난다 → [[data-type]] · [[class-metadata]]
- **반환 타입을 좁혀 두면 부르는 쪽의 캐스팅이 사라진다** — `Object.clone()` 을 그대로 썼다면 부르는 쪽마다 `(Score)` 를 써야 한다. 재정의에서 반환 타입을 `Score` 로 좁혀 두면 캐스팅이 **메서드 안 한 곳**으로 모인다. 캐스팅은 없애는 것이 아니라 **어디에 둘지 고르는 것**이다 → [[method-overriding]] · [[object-cloning]]
- **캐스팅이 필요한지는 「그 메서드의 선언이 어디 있나」가 정한다** — 「부모 타입으로는 자식 메서드를 못 부른다」로만 외우면 `obj.toString()` 이 `Hello` 를 찍는 것이 반례로 보인다. 기준은 **선언이 부모에 있는가**이고, 있으면 캐스팅 없이 부를 수 있으며 그때 실행되는 것은 자식의 재정의본이다. 캐스팅이 여는 것은 **부모에 선언이 없는 멤버**뿐이다 → [[method-overriding]] · [[object-class]]
- **`Object` 를 「형변환」이라 부르는 것에 두 가지가 섞여 있다** — 이 필기가 같은 회차에서 `(String) obj` 로 참조형 캐스팅을 하고, `Integer obj2 = 100` 으로 기본 타입을 래퍼로 감싸는 것을 배운다. **뒤쪽은 캐스팅이 아니라 인스턴스를 하나 만드는 일**이다. 둘 다 「타입을 맞춘다」로 읽히지만 하나는 창을 바꾸고 하나는 객체를 만든다 → [[autoboxing]] · [[wrapper-class]]
- **`getClass()` 로 확인한 것과 `instanceof` 로 확인한 것은 캐스팅 안전성이 다르다** — 필기의 `equals` 는 `getClass() != obj.getClass()` 로 정확히 같은 클래스만 통과시켰으므로 뒤의 `(My) obj` 가 절대 실패하지 않는다. `instanceof` 로 검사했다면 자식 인스턴스도 통과하고, 그때도 `(My)` 캐스팅은 성공한다 — **두 검사 모두 캐스팅을 안전하게 만들지만 통과 범위가 다르다** → [[object-equality]]

## 함께 보는 개념

- [[polymorphism]] — 업캐스팅이 만드는 성질
- [[inheritance]] — 캐스팅이 성립하는 전제
- [[method-overriding]] — 업캐스팅해도 자식 구현이 불리는 이유
- [[type-promotion]] — 같은 「형변환」으로 불리는 기본 타입 쪽
- [[object-class]] — 업캐스팅의 목적지가 되는 타입
- [[instanceof-operator]] — 다운캐스팅 앞에 두는 검사
- [[object-equality]] — 다운캐스팅이 필수인 대표 자리
- [[hash-based-collection]] — 꺼낼 때마다 되돌려야 하는 구조
- [[object-cloning]] — 반환 타입을 좁혀 캐스팅을 안으로 모으는 예
- [[data-type]] — 이 계층 밖에 있는 여덟 개
- [[wrapper-class]] — 여덟 개를 이 계층에 들여보내는 방법
- [[autoboxing]] — 「타입을 맞춘다」로 같이 읽히는 다른 일

## 출처

- [[2024-06-24-Day21]] — `Object obj = new My()` 처럼 최상위 타입으로 받는 업캐스팅과, 그것을 되돌리는 다운캐스팅이 `equals` 의 `(My) obj`·`toArray()` 결과의 `(Student) obj`·`(Score) super.clone()` 세 자리에 다 나온다. 「파라미터가 type이 Object type이기 때문에 형변환을 적용한다」가 그 이유이고, 기본 타입은 `Object` 의 서브클래스가 아니라 이 계층에 들어오지 못한다는 것도 같은 회차다
- [[2024-06-25-Day22]] — `Object obj = new String("Hello")` 를 `(String) obj` 로 되돌리며 「원래 타입으로 형변환을 해야 해당 타입의 클래스의 메소드를 호출 할 수 있다」를 배웠다. `obj == x1` 로 인스턴스는 하나뿐임을 확인하고, 같은 `obj` 로 `toString()` 은 캐스팅 없이 불러 `Hello` 를 얻는 것까지 나란히 있어 **캐스팅이 필요한 기준이 「선언이 어디 있나」**라는 것이 이 회차에서 드러난다. 래퍼 클래스를 배우며 `m(Object)` 하나로 세 타입을 받는 것도 같은 자리다
- [[2024-07-01-Day26]] — 자동 타입변환(업캐스팅)과 강제 타입변환(다운캐스팅), `instanceof` 를 배웠다
