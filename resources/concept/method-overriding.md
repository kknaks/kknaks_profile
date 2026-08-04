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
  - 2024-07-01-Day26
tags:
  - oop
  - java
  - 상속
---

# 메서드 오버라이딩 (Method Overriding)

자식 클래스가 부모에게서 물려받은 메서드를 **같은 선언부로 다시 정의**하는 것. 재정의하면 부모의 것은 가려지고 자식의 것이 실행된다.

## 정의

지켜야 하는 조건이 있다.

- 부모 메서드와 **선언부가 같아야 한다** — 이름·매개변수·반환타입
- 접근 제어자를 **더 좁힐 수 없다** (`public` → `private` 불가)
- `@Override` 는 컴파일러에게 "재정의 의도" 를 알리는 표시다. 붙이면 오타로 새 메서드를 만드는 실수를 컴파일 시점에 잡는다

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

## 왜 중요한가

**부모 타입으로 호출해도 자식의 구현이 실행된다.** 이것이 [[polymorphism]] 을 만드는 두 축 중 하나다 — 나머지 한 축은 [[type-casting]] 의 자동 타입변환이다.

오버라이딩이 없으면 상속은 코드 재사용에서 끝나고, 자식마다 다르게 동작시키려면 호출부에서 타입을 분기해야 한다.

## 경계와 오해

- **오버라이딩 ≠ 오버로딩** — 오버로딩은 **같은 이름, 다른 매개변수**를 한 클래스 안에 여러 개 두는 것이고 **컴파일 시점**에 결정된다. 오버라이딩은 **같은 선언부**를 상속 관계에서 다시 정의하는 것이고 **실행 시점**에 결정된다.
- **필드는 오버라이딩되지 않는다** — 재정의 대상은 메서드뿐이다. 같은 이름의 필드를 자식에 두면 부모 것을 가릴 뿐(hiding)이고, 접근은 **변수의 선언 타입**을 따른다.
- **`static` 메서드는 오버라이딩이 아니다** — 클래스에 묶이므로 재정의가 아니라 은닉이다.

## 함께 보는 개념

- [[inheritance]] — 오버라이딩의 전제
- [[polymorphism]] — 오버라이딩이 만드는 성질
- [[abstract-class]] — 오버라이딩을 강제하는 장치

## 출처

- [[2024-07-01-Day26]] — 오버라이딩의 조건과 `@Override`, `super.` 로 부모 메서드를 부르는 법을 배웠다
