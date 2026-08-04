---
type: concept
id: abstract-class
title: 추상 클래스 (Abstract Class)
aliases:
  - 추상 클래스
  - 추상클래스
  - 추상 메서드
  - 추상메서드
  - abstract class
  - abstract
up:
  - 2024-07-01-Day26
tags:
  - oop
  - java
  - 클래스설계
---

# 추상 클래스 (Abstract Class)

여러 클래스의 공통 멤버를 모아 두되 **그 자체로는 인스턴스를 만들 수 없는** 클래스. `abstract` 로 선언하고, 자식이 상속받아 완성해야 쓸 수 있다.

## 정의

```java
public abstract class Phone {
    String owner;                        // 필드 — 자식이 물려받는다

    Phone(String owner) {                // 생성자 — 자식이 super(owner) 로 부른다
        this.owner = owner;
    }

    void turnOn() {                      // 구현이 있는 메서드 — 그대로 물려받는다
        System.out.println("폰 전원을 켭니다.");
    }

    abstract void internetSearch();      // 추상 메서드 — 자식이 반드시 완성해야 한다
}
```

두 가지가 강제된다.

- **`new Phone()` 이 안 된다** — 추상 클래스는 직접 생성할 수 없다.
- **추상 메서드가 있으면 자식이 구현해야 한다** — 안 하면 컴파일이 막힌다.

생성자·필드·일반 메서드는 보통 클래스와 똑같이 가질 수 있다. "미완성" 인 것은 추상 메서드뿐이다.

## 사용 예시

```java
public class SmartPhone extends Phone {
    SmartPhone(String owner) {
        super(owner);                    // 부모에 기본 생성자가 없으므로 필수다
    }

    @Override
    void internetSearch() {              // 추상 메서드 — 안 쓰면 컴파일 에러
        System.out.println("인터넷 검색을 합니다.");
    }

    @Override
    void turnOff() {                     // 구현이 있는 메서드도 재정의는 자유다
        System.out.println("스마트폰 전원을 끕니다.");
    }
}

SmartPhone smartPhone = new SmartPhone("홍길동");
smartPhone.turnOn();          // "폰 전원을 켭니다."      ← 부모 것
smartPhone.internetSearch();  // "인터넷 검색을 합니다."   ← 자식이 완성한 것
smartPhone.turnOff();         // "스마트폰 전원을 끕니다."  ← 자식이 재정의한 것
```

세 호출이 각각 **물려받은 것 / 완성한 것 / 재정의한 것** 을 보여준다.

## 왜 중요한가

**[[polymorphism]] 을 강제한다.** 부모가 `internetSearch()` 를 추상으로 선언해 두면, 자식은 그 메서드를 반드시 갖는다. 그래서 `Phone` 타입 변수로 받아 놓고 `internetSearch()` 를 불러도 **어떤 자식이 오든 안전하다.**

일반 클래스를 상속시키면 자식이 재정의를 빼먹어도 컴파일이 통과한다 — 부모의 기본 구현이 조용히 불린다. 추상 클래스는 그 실수를 **컴파일 시점에** 막는다. 「해도 되는 것」이 아니라 「안 하면 못 넘어가는 것」으로 바뀐다.

## 경계와 오해

- **추상 클래스 ≠ 전부 추상 메서드** — 구현이 있는 메서드와 없는 메서드를 섞을 수 있다. 공통 구현은 부모가 갖고, 자식마다 달라지는 것만 추상으로 남기는 게 보통이다.
- **`abstract` 키워드를 빠뜨리면 추상 메서드가 아니다** — 본문 없이 `void internetSearch();` 라고만 쓰면 컴파일 에러다. 메서드에도 클래스에도 `abstract` 가 필요하다.
- **인스턴스를 못 만들 뿐 생성자는 있다** — 자식이 `super(...)` 로 부르기 위해 존재한다. 생성자가 없다는 뜻이 아니다.

## 함께 보는 개념

- [[inheritance]] — 추상 클래스는 상속을 전제로만 쓰인다
- [[method-overriding]] — 추상 메서드 구현이 곧 오버라이딩이다
- [[polymorphism]] — 추상 클래스가 강제하려는 것

## 출처

- [[2024-07-01-Day26]] — `Phone`/`SmartPhone` 예제로 추상 클래스의 생성 제한과 자식의 구현 의무를 배웠다
