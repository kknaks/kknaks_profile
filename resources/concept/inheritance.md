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
  - 2024-07-01-Day26
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

## 왜 중요한가

**공통 코드를 한 곳에 둘 수 있다.** 자식이 늘어도 부모만 고치면 되고, 자식마다 같은 코드를 복사할 이유가 사라진다.

그리고 상속은 그 자체보다 **[[polymorphism]] 의 전제 조건**이라는 점에서 값이 크다. 상속이 없으면 부모 타입 변수가 자식 인스턴스를 가리킬 수 없고, 그러면 다형성도 성립하지 않는다.

## 경계와 오해

- **상속 ≠ 멤버 복사** — 부모의 멤버가 자식에 **복사되지 않는다.** 바이트코드가 복제되는 것이 아니라 부모의 것을 **사용하는 것**뿐이다. 이걸 복사로 이해하면 메모리 모델과 오버라이딩 동작을 계속 잘못 짚게 된다.
- **상속 ≠ 다형성** — 상속은 조건이고 다형성은 그 위에서 나오는 성질이다. 상속만 받고 [[method-overriding]] 을 안 하면 다형성은 발현되지 않는다.
- **`private` 멤버는 상속 대상이 아니다** — 접근 제어자가 상속 범위를 정한다.
- **super class ≠ root class** — 옛 필기에 "java 에는 root 에 해당하는 class 를 super class 라고 부른다"고 적어 두었는데, 두 말이 섞인 것이다. **super class 는 어떤 클래스의 직접 부모**를 뜻하고 클래스마다 다르다. 계층 전체의 뿌리인 root class 가 `java.lang.Object` 다. `.class` 파일의 `super_class` 자리에 `java/lang/Object` 가 들어가는 것은 그 클래스가 아무것도 `extends` 하지 않았을 때뿐이다.

## 함께 보는 개념

- [[polymorphism]] — 상속 위에서 성립하는 성질
- [[method-overriding]] — 자식이 부모 메서드를 다시 정의하는 것
- [[abstract-class]] — 상속을 강제하는 장치
- [[class-file-format]] — `super_class` 로 부모가 기록되는 자리

## 출처

- [[2024-05-30-Day05]] — `.class` 파일의 `super_class` 자리에 `java/lang/Object` 가 들어가는 것을 16진수로 직접 확인했다
- [[2024-07-01-Day26]] — 상속의 정의, `extends` 문법, 부모 생성자 호출과 `this`/`super` 를 배웠다
