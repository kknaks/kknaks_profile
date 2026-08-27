---
type: concept
id: field-hiding
title: 필드 은닉 (Field Hiding)
aliases:
  - 필드 은닉
  - 필드 숨김
  - 필드 섀도잉
  - field hiding
  - field shadowing
  - 변수 은닉
  - variable hiding
up:
  - 2024-07-08-Day30
tags:
  - java
  - 상속
  - 오류
  - 클래스설계
---

# 필드 은닉 (Field Hiding)

**자식 클래스가 부모와 같은 이름의 필드를 다시 선언하면, 그 두 필드가 한 인스턴스 안에 동시에 존재한다.** 메서드처럼 하나로 합쳐지지(재정의되지) 않고 부모 것이 **가려질** 뿐이며, 어느 쪽이 보이는지는 실행 중의 실제 타입이 아니라 **그 코드가 쓰는 변수의 선언 타입**이 정한다.

## 정의

| | 메서드 | 필드 |
|---|---|---|
| 자식이 같은 이름을 선언하면 | **재정의** — 하나만 남는다 | **은닉** — 둘 다 남는다 |
| 무엇이 선택되나 | 실제 인스턴스의 타입 | **변수의 선언 타입** |
| 결정 시점 | 실행 시점 | 컴파일 시점 |
| 부모 것에 닿는 법 | `super.메서드()` | `super.필드` · `((Parent) this).필드` |
| 실수를 잡아 주는 장치 | `@Override` | **없다** |

```java
class Parent { int x = 1; }
class Child extends Parent { int x = 2; }

Parent p = new Child();
System.out.println(p.x);              // 1  ← Parent 의 것
System.out.println(((Child) p).x);    // 2  ← Child 의 것
```

**같은 객체를 두 이름으로 물었는데 답이 다르다.** 필드가 지워지지 않고 둘 다 있기 때문이다 → [[method-overriding]] · [[variable]]

접근 지정자가 `private` 이면 애초에 상속되지 않으므로 「가린다」는 관계조차 성립하지 않는다. 그래도 **결과는 같다** — 이름이 같은 필드가 두 개 존재하고, 부모의 코드는 부모 것을, 자식의 코드는 자기 것을 읽는다 → [[access-modifier]]

## 사용 예시

이 회차는 공통 필드를 부모로 끌어올리는 리팩터링을 두 번 했고, **두 번 다 자식의 선언을 지우지 않았다.**

**하나 — `size`.** `AbstractList` 를 만든 목적이 「ArrayList와 LinkedList 클래스에는 size가 중복된다」였다.

```java
public abstract class AbstractList implements List {
  protected int size = 0;

  @Override
  public int size() {
    return size;
  }
}
```

그런데 두 자식이 그 필드를 다시 선언하고 `size()` 까지 다시 재정의한다.

```java
public class ArrayList extends AbstractList {
  private Object[] list = new Object[MAX_SIZE];
  private int size = 0;              // ← 부모의 protected size 와 별개의 필드

  @Override
  public void add(Object obj) { ... list[size++] = obj; }   // 자기 것을 센다

  @Override
  public int size() { return size; }                        // 자기 것을 돌려준다
}
```

```java
public class LinkedList extends AbstractList {
  Node first;
  Node last;
  int size;                          // ← 여기도

  @Override
  public int size() { return size; }
}
```

**`AbstractList.size` 는 끝까지 `0` 이고 아무도 읽지 않는다.** 자식이 `size()` 를 재정의했으므로 **밖에서 보이는 값은 정확하다** — 그래서 이 실수는 버그로 드러나지 않고, 대신 `AbstractList` 를 만든 이유가 사라진다. 12일 앞선 회차의 `ArrayList` 에는 `size` 선언이 없었고 `size()` 재정의도 없었다. **중복을 없애려고 만든 부모 앞에서 중복이 되돌아온 것**이다 → [[abstract-class]] · [[generalization]]

**둘 — `menuTitle`.** 같은 노트 뒤쪽에서 Command 세 개의 공통 코드를 `AbstractCommand` 로 올릴 때, 제목은 부모 생성자로 넘긴다.

```java
public class UserCommand extends AbstractCommand {

  String menuTitle;                            // ← 지워지지 않은 선언
  String[] menus = {"등록", "목록", "조회", "변경", "삭제"};

  public UserCommand(String menuTitle) {
    super(menuTitle);                          // 값은 부모에게 준다
  }
}
```

**이 필드에는 아무도 값을 넣지 않는다.** 생성자의 매개변수 `menuTitle` 은 `super(...)` 로 흘러가고 `this.menuTitle = ...` 은 없다 — 일반화 전 버전에 있던 그 대입이 지워졌다. 그래서 자식의 `menuTitle` 은 **영원히 `null`** 이다.

여기서도 화면은 정상이다. 제목을 찍는 `printMenus()` 가 부모로 올라가서 **부모의 필드를 읽기 때문**이다. 세 자식 전부(`UserCommand`·`ProjectCommand`·`BoardCommand`) 같은 상태이고, **누군가 자식 안에서 `menuTitle` 을 쓰는 코드를 한 줄 더하는 순간** `null` 이 나온다 → [[template-method-pattern]]

## 왜 중요한가

**컴파일러가 알려 주지 않는 실수 중에서 「고쳐도 아무 일이 안 일어나는」 쪽에 속한다.** 메서드 이름을 잘못 써서 재정의가 안 된 경우는 `@Override` 가 잡아 주는데, **필드에는 그런 표시가 없다.** 이름이 겹치는 것은 합법이고 경고도 없다.

**끌어올리기의 성공을 「부모에 코드가 생겼나」로 판정하면 안 되는 이유가 이것이다.** 부모에 `size` 가 생겼고 `AbstractList` 도 존재하지만 중복은 그대로다. 확인해야 하는 것은 반대쪽이다 — **자식에서 그 선언이 없어졌는가** → [[refactoring]]

**그리고 값이 맞아 보이는 상태로 남는다.** `size` 쪽은 `size()` 재정의가 덮어 주고 `menuTitle` 쪽은 부모의 것이 화면에 나온다. **두 사례 모두 프로그램이 정상으로 보이므로 발견 계기가 없다** — 나중에 부모의 필드를 믿고 부모에 코드를 한 줄 더하는 사람이 「분명히 세었는데 0 이다」를 만난다.

## 경계와 오해

- **필드 은닉 ≠ 메서드 오버라이딩** — 같은 이름을 다시 쓰는 모양이 똑같아서 「필드도 재정의된다」로 읽히는데, **메서드는 하나로 합쳐지고 필드는 둘 다 남는다.** 그래서 부모 타입 변수로 읽으면 부모 값이 나온다 — 다형성이 필드에는 적용되지 않는다는 말의 실제 내용이 이것이다 → [[method-overriding]] · [[polymorphism]]
- **필드 은닉 ≠ 정보 은닉(information hiding)** — 이름이 닮았지만 완전히 다른 것이다. 정보 은닉은 `private` 으로 **밖에서 못 보게 하는 설계**이고([[encapsulation]]), 필드 은닉은 **상속 관계에서 같은 이름이 겹친 상태**다. 한쪽은 의도이고 한쪽은 대개 사고다.
- **`private` 필드를 「가린다」고 말할 수는 없다** — `private` 은 상속되지 않으므로 `ArrayList.size` 는 부모 필드를 가리는 것이 아니라 **처음부터 다른 필드**다. 그래도 실용적으로 구별할 필요가 없다 — 「한 인스턴스에 같은 이름의 필드가 두 개」라는 결과와 그것이 만드는 문제가 같다. 오히려 `private` 쪽이 더 나쁘다 — `super.size` 로 부모 것에 닿을 수도 없다 → [[access-modifier]]
- **컴파일 에러가 아니다** — 같은 이름을 자식에 다시 선언하는 것은 문법적으로 허용된다. 그리고 **의도적으로 쓰는 경우는 사실상 없다** — 그래서 이 코드를 보면 「무슨 뜻일까」를 찾기보다 **지우고 안 지운 자리인지 먼저 의심**하는 것이 맞다.
- **`static` 메서드에서 같은 일이 일어난다** — 클래스에 묶인 메서드는 재정의가 아니라 은닉이므로, 자식에 같은 시그니처의 `static` 메서드를 두면 필드와 같은 규칙(선언 타입이 고른다)을 따른다 → [[static-member]]
- **부모의 필드를 `protected` 로 열어 둔 것이 원인은 아니다** — `AbstractList.size` 는 자식이 `size++` 로 직접 만지도록 `protected` 로 열려 있었다. 자식은 **그것을 그냥 쓰면 됐다.** 다시 선언한 이유는 접근 문제가 아니라 **부모를 만들면서 자식 코드를 손대지 않았기 때문**이다 → [[generalization]]
- **일반화가 「절반만」 되어 있는 상태를 가리키는 신호다** — 부모가 생겼는데 자식에 같은 선언이 남아 있다면 그 리팩터링은 끝나지 않았다. 이 노트는 같은 자리에서 두 번(필드 `size`, 필드 `menuTitle`) 그렇게 멈췄고, 그것이 **한 번의 부주의가 아니라 절차의 빈칸**임을 보여 준다 → [[refactoring]]

## 함께 보는 개념

- [[method-overriding]] — 필드와 규칙이 반대인 쪽
- [[inheritance]] — 이름이 겹칠 수 있게 되는 관계
- [[generalization]] — 이 실수가 생기는 작업
- [[abstract-class]] — `size` 를 끌어올린 자리
- [[refactoring]] — 「옮기고 안 지웠다」의 한 종류
- [[polymorphism]] — 필드에는 적용되지 않는 성질
- [[encapsulation]] — 이름이 닮은 다른 개념(정보 은닉)
- [[access-modifier]] — 가림 관계가 성립하는지를 정하는 축
- [[static-member]] — 은닉이 일어나는 다른 자리
- [[variable]] — 선언 타입이 이름 해석을 정한다는 규칙
- [[dynamic-array]] — `size` 가 다시 선언된 한쪽
- [[linked-list]] — 다시 선언된 다른 쪽
- [[template-method-pattern]] — `menuTitle` 이 죽은 채로 남은 구조

## 출처

- [[2024-07-08-Day30]] — 공통 필드를 부모로 올리는 리팩터링을 두 번 하면서 **두 번 다 자식의 선언을 남겼다.** `AbstractList` 에 `protected int size = 0` 을 두고도 `ArrayList` 가 `private int size = 0` 을, `LinkedList` 가 `int size` 를 다시 선언하고 `size()` 까지 각자 재정의해 부모 필드가 죽었고, `AbstractCommand` 에 `super(menuTitle)` 로 제목을 넘긴 세 Command 에는 `String menuTitle;` 선언이 남아 그 필드가 영원히 `null` 이다. 두 경우 다 화면에 나오는 값은 정확해서 **정상으로 보이는 것**이 이 실수의 성질을 그대로 보여 준다
