---
type: concept
id: inheritance
title: 상속 (Inheritance)
aliases:
  - 상속
  - inheritance
  - 클래스 상속
  - extends
up:
  - 2024-05-30-Day05
  - 2024-06-24-Day21
  - 2024-07-01-Day26
  - 2024-07-08-Day30
  - 2024-07-19-Day39
tags:
  - oop
  - java
  - 클래스설계
---

# 상속 (Inheritance)

부모 클래스가 가진 필드와 메서드를 자식 클래스에서 그대로 쓸 수 있게 하는 관계. `extends` 로 선언한다.

## 정의

```java
public class Parent {
    필드
    메소드()
}

public class Child extends Parent {
    필드
    메소드()
}
```

자식이 부모를 상속하면 부모의 멤버에 접근할 수 있다. 이때 **자식 객체가 만들어지기 전에 부모 생성자가 먼저 호출된다** — 자식 생성자의 첫 줄에 `super()` 가 암묵적으로 들어간다. 부모에 기본 생성자가 없으면 `super(인자)` 를 직접 써야 한다.

부모의 멤버를 자식에서 가리켜야 할 때는 `super.` 를 쓴다. `this.` 는 자기 자신을 가리킨다.

**`extends` 를 안 써도 부모가 있다.** 모든 클래스는 암묵적으로 `java.lang.Object` 를 상속하며, 이것이 상속 계층의 뿌리다. 컴파일된 `.class` 를 열어 보면 `super_class` 자리에 `java/lang/Object` 를 가리키는 인덱스가 실제로 들어가 있다 → [[class-file-format]]

실행 중에도 같은 것을 확인할 수 있다. 컴파일러가 채워 넣는 부모를 주석으로 적어 두고 `instanceof` 로 물어보는 형태다.

```java
public class Exam0110 /*extends Object*/ {
  static class My /*extends Object*/ {
  }
  ...
  Object obj = new My();                        // 대입이 되는 것 자체가 증거다
  System.out.println(obj instanceof My);        //true
  System.out.println(obj instanceof Object);    //true
}
```

`My` 선언에 `Object` 라는 글자가 없는데 `instanceof Object` 가 `true` 다 → [[instanceof-operator]] · [[object-class]]

**그리고 이 상속에는 딸려 오는 것이 있다.** `toString`·`equals`·`hashCode`·`getClass`·`clone`·`finalize` 여섯 개가 처음부터 들어 있고, 그래서 `extends` 를 한 번도 쓰지 않은 클래스에도 **재정의할 것이 이미 있다** → [[method-overriding]]

## 사용 예시

`Phone` 의 공통 속성을 두고 `SmartPhone` 이 확장한다.

```java
public class SmartPhone extends Phone {
    public SmartPhone(String model, String color) {
        super();                  // 부모 생성자가 먼저 호출된다 (생략해도 암묵 삽입)
        this.model = model;       // model·color 는 Phone 이 가진 필드
        this.color = color;
    }
}
```

`model`·`color` 를 `SmartPhone` 이 다시 선언하지 않았다. `Phone` 의 것을 **쓰는 것**이다.

부모 생성자가 매개변수를 요구하면 `super()` 로는 안 되고 `super(model, color)` 처럼 인자를 넘겨야 한다 — 부모가 초기화를 끝내야 자식이 시작할 수 있기 때문이다.

### 이레 뒤 실습이 상속을 「쓰는 이유」쪽에서 다시 만난다

문법을 배운 이레 뒤 리팩터링 회차에서 `extends` 가 처음으로 **실습 프로젝트의 도구**로 쓰인다. 세 Command 클래스에 같은 `execute()` 가 생겼고, 그것을 `AbstractCommand` 로 올리는 수단이 상속이다.

```java
public class UserCommand extends AbstractCommand {
  public UserCommand(String menuTitle) {
    super(menuTitle);                    // 제목을 부모에게 넘긴다
  }
}
```

**여기서 `super(menuTitle)` 은 문법 연습이 아니라 필드를 옮기는 방법이다.** 자식마다 다른 값을 부모가 갖게 하는 유일한 길이고, 그래서 「부모 생성자가 먼저 호출된다」가 **왜 인자를 받아야 하는가**로 이어진다 → [[constructor]] · [[generalization]]

그리고 상속을 쓰는 이유가 회차마다 다르다는 것이 이 무렵 세 코드로 나란히 드러난다.

| 부모 | 자식에게 물려주는 것 | 상속을 쓴 이유 |
|---|---|---|
| `Sorter` (Day28) | 없다 (추상 메서드 하나) | 한 타입으로 받으려고 — [[polymorphism]] |
| `AbstractList` (Day23·Day30) | 필드 `size` 와 `size()` | 중복을 없애려고 |
| `AbstractCommand` (Day30) | `execute()` 골격 전체 | 중복을 없애고 **순서를 소유하려고** → [[template-method-pattern]] |

## 왜 중요한가

**공통 코드를 한 곳에 둘 수 있다.** 자식이 늘어도 부모만 고치면 되고, 자식마다 같은 코드를 복사할 이유가 사라진다.

그리고 상속은 그 자체보다 **[[polymorphism]] 의 전제 조건**이라는 점에서 값이 크다. 상속이 없으면 부모 타입 변수가 자식 인스턴스를 가리킬 수 없고, 그러면 다형성도 성립하지 않는다.

## 경계와 오해

- **상속 ≠ 멤버 복사** — 부모의 멤버가 자식에 **복사되지 않는다.** 바이트코드가 복제되는 것이 아니라 부모의 것을 **사용하는 것**뿐이다. 이걸 복사로 이해하면 메모리 모델과 오버라이딩 동작을 계속 잘못 짚게 된다.
- **상속 ≠ 다형성** — 상속은 조건이고 다형성은 그 위에서 나오는 성질이다. 상속만 받고 [[method-overriding]] 을 안 하면 다형성은 발현되지 않는다.
- **`private` 멤버는 상속 대상이 아니다** — 접근 제어자가 상속 범위를 정한다.
- **`protected` 멤버는 상속되지만 마음대로 쓸 수 있는 것은 아니다** — 물려받은 것을 `this` 로 쓰는 것은 되고, **같은 타입인 남의 인스턴스의 것**은 안 된다. `Score` 안에서 `this.clone()` 은 되고 `s1.clone()` 은 컴파일 오류인 자리가 그것이다. 「상속받았으니 내 것이다」로 읽으면 이 구별이 안 보인다 → [[access-modifier]] · [[object-cloning]]
- **상속을 문법으로 배우기 전에 이미 상속을 쓰고 있었다** — `extends`·`super()`·오버라이딩의 조건을 정리한 것은 이 필기의 나중 회차인데, 그보다 앞선 `Object` 회차에서 이미 `toString`·`equals`·`hashCode`·`clone` 네 개를 재정의했다. **`extends` 라는 단어를 한 번도 쓰지 않고 상속의 실습을 다 한 것**이고, 그것이 가능한 이유가 암묵 상속이다. 「상속은 `extends` 를 쓸 때 생기는 관계」로 읽으면 그 회차의 코드가 무엇을 하고 있었는지 설명되지 않는다 → [[object-class]]
- **뿌리가 하나라는 것이 문법이 아니라 설계 결정이다** — 계층이 하나로 모이므로 `Object` 타입 하나가 **무엇이든 받는 자리**가 된다. `HashSet.toArray()` 가 `Object[]` 를 돌려주고 `equals(Object obj)` 가 `Object` 를 받는 것이 다 그 덕분이고, 그 대가로 받는 쪽이 매번 다운캐스팅을 한다 → [[type-casting]] · [[hash-based-collection]]
- **「자식이 부모의 것을 쓴다」에는 자식이 안 쓰는 선택도 들어 있다** — `super(menuTitle)` 로 값을 부모에게 넘긴 세 Command 에 `String menuTitle;` 선언이 그대로 남아 있고, `AbstractList.size` 를 물려받은 두 자식이 같은 이름의 필드를 다시 선언한다. **상속은 이름을 겹치지 못하게 막지 않으므로** 「물려받았다」와 「그것을 쓴다」가 갈릴 수 있다. 그러면 코드는 돌아가면서 상속의 이유만 사라진다 → [[field-hiding]]
- **자식 필드는 `super(...)` 가 끝난 다음에 초기화된다** — `super(menuTitle)` → 자식의 필드 초기자(`String[] menus = {...}`) → 자식 생성자 본문 순서다. 그래서 **부모 생성자에서 자식의 메서드를 부르면 자식 필드가 아직 비어 있다.** 「부모가 먼저 완성된다」를 「부모 안에서는 자식을 다 쓸 수 있다」로 읽으면 원인을 찾기 어려운 `null` 이 나온다 → [[constructor]] · [[template-method-pattern]]
- **기능을 조합하는 수단으로 쓰면 클래스가 곱셈으로 늘어난다** — Day39 가 이 한계를 숫자로 센다. 출력에 붙일 기능이 셋(머릿말·꼬릿말·서명)일 때 상속으로 조합하면 「순서에 상관 없는 경우 8가지」(`2³`), 순서까지 따지면 그보다 더 많은 클래스가 필요하고 「각클래스마다 생성자의 매개변수도 다양해서 일관성도 저해된다」. 핵심은 숫자가 아니라 **상속이 조합을 컴파일 시점에 못 박는다**는 것이다 — 「머릿말+꼬릿말」과 「꼬릿말+머릿말」이 각각 클래스여야 하고 기능이 하나 늘면 그 전부에 다시 곱해진다. **공통 코드를 올리는 데 쓰는 상속과 기능을 더하는 데 쓰는 상속이 갈리는 자리**이고, 뒤쪽의 답은 상속이 아니라 같은 타입을 필드로 품는 것이다 → [[decorator-pattern]]
- **super class ≠ root class** — 옛 필기에 "java 에는 root 에 해당하는 class 를 super class 라고 부른다"고 적어 두었는데, 두 말이 섞인 것이다. **super class 는 어떤 클래스의 직접 부모**를 뜻하고 클래스마다 다르다. 계층 전체의 뿌리인 root class 가 `java.lang.Object` 다. `.class` 파일의 `super_class` 자리에 `java/lang/Object` 가 들어가는 것은 그 클래스가 아무것도 `extends` 하지 않았을 때뿐이다.

## 함께 보는 개념

- [[polymorphism]] — 상속 위에서 성립하는 성질
- [[method-overriding]] — 자식이 부모 메서드를 다시 정의하는 것
- [[abstract-class]] — 상속을 강제하는 장치
- [[class-file-format]] — `super_class` 로 부모가 기록되는 자리
- [[object-class]] — 계층의 뿌리
- [[instanceof-operator]] — 상속 관계를 실행 중에 확인하는 도구
- [[access-modifier]] — 상속되는 범위를 정하는 축
- [[generalization]] — 상속을 쓰는 이유 중 하나(공통 코드 올리기)
- [[template-method-pattern]] — 부모가 자식을 부르게 되는 구조
- [[field-hiding]] — 물려받은 이름을 자식이 다시 선언했을 때
- [[constructor]] — `super(...)` 와 초기화 순서
- [[decorator-pattern]] — 기능 조합을 상속 대신 필드로 하는 방법

## 출처

- [[2024-05-30-Day05]] — `.class` 파일의 `super_class` 자리에 `java/lang/Object` 가 들어가는 것을 16진수로 직접 확인했다
- [[2024-06-24-Day21]] — 암묵 상속을 실행 중에 확인했다. `/*extends Object*/` 주석과 `Object obj = new My()` 대입, `obj instanceof Object` 가 `true` 인 것으로 「모든 클래스는 Object 클래스와 링크된다」를 배우고, 그 상속으로 메서드 여섯 개가 딸려 온다는 것과 물려받은 `protected` 멤버를 남의 인스턴스로는 쓸 수 없다는 것도 이 자리에서 나온다
- [[2024-07-01-Day26]] — 상속의 정의, `extends` 문법, 부모 생성자 호출과 `this`/`super` 를 배웠다
- [[2024-07-08-Day30]] — 문법을 배운 이레 뒤, 상속을 **실습 프로젝트의 도구로** 처음 썼다. 세 Command 의 공통 `execute()` 를 `AbstractCommand` 로 올리고 `super(menuTitle)` 로 제목을 부모에게 넘기는데, 그러면서 자식에 남은 `String menuTitle;` 선언과 `AbstractList` 의 `size` 를 자식이 다시 선언한 것이 **「물려받았다」와 「그것을 쓴다」가 갈릴 수 있다**는 것을 보여 준다. 같은 무렵의 `Sorter`(다형성)·`AbstractList`(중복)·`AbstractCommand`(중복+순서)가 상속을 쓰는 이유 세 가지를 나란히 놓아 준다
- [[2024-07-19-Day39]] — 데코레이터 패턴을 배우면서 **상속을 「하지 않는 이유」쪽에서 다시 만난다.** 기능 3가지를 상속으로 조합하면 순서 무관 8가지(순서까지 따지면 더 많다)의 클래스가 필요하고 생성자 매개변수의 일관성도 깨진다고 세어 두고, 그 대안으로 `PrinterDecorator` 가 `Printer` 를 **필드로 품는** 구조를 쓴다. `HeaderPrinter extends PrinterDecorator` 처럼 `extends` 는 여전히 쓰이지만 **필드·생성자를 재사용하기 위해서**이고 기능이 붙는 축은 상속이 아니다 — 상속을 쓰는 이유 목록에 「쓰면 안 되는 자리」가 처음 추가되는 회차다
