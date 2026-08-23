---
type: concept
id: instanceof-operator
title: instanceof 연산자
aliases:
  - instanceof
  - instanceof 연산자
  - instanceof operator
  - 타입 검사
  - 인스턴스 검사
  - 패턴 변수
  - pattern matching for instanceof
up:
  - 2024-06-24-Day21
  - 2024-07-15-Day35
tags:
  - java
  - 연산자
  - 상속
  - 문법
---

# instanceof 연산자

레퍼런스가 가리키는 인스턴스가 **지정한 클래스의 인스턴스이거나 그 클래스를 조상으로 갖는지** 묻고 `true`/`false` 를 돌려준다. **변수의 선언 타입이 아니라 실제로 들어 있는 것**을 묻는다는 점이 핵심이다.

## 정의

```java
레퍼런스 instanceof 클래스명
```

`true` 가 되는 경우는 둘이다 — 정확히 그 클래스이거나, 그 클래스를 **조상으로** 갖는 경우다. 그래서 한 인스턴스에 대해 여러 클래스가 동시에 `true` 가 될 수 있다.

```java
Object obj = new My();
System.out.println(obj instanceof My);      //true   — 바로 그 클래스
System.out.println(obj instanceof String);  //false  — 관계가 없다
System.out.println(obj instanceof Object);  //true   — 조상이다
```

**세 줄 모두 `obj` 의 선언 타입은 `Object` 인데 답이 갈린다.** 물어보는 대상은 변수가 아니라 그 안의 주소가 가리키는 인스턴스다 → [[object-reference]]

## 사용 예시

필기는 이 연산자를 **상속 관계를 증명하는 도구**로 썼다. `My` 선언에 `extends` 가 없는데도 `Object` 의 서브클래스라는 것을 코드로 확인하는 자리다.

```java
public class Exam0110 /*extends Object*/ {
  static class My /*extends Object*/ {
  }
  public static void main(String[] args) {
    Object obj = new My();
    // Object의 레퍼런스에 My 인스턴스 주소를 저장할 수 있다는 것은
    // My 클래스가 Object 크래스의 서브 클래스임을 증명하는 것이다.
    System.out.println(obj instanceof My);      //true
    System.out.println(obj instanceof String);  //false
    System.out.println(obj instanceof Object);  //true
  }
}
```

증명은 두 단계로 되어 있다. **대입이 되는 것**(`Object obj = new My()`)이 이미 상속의 증거이고, `instanceof` 는 그것을 `true`/`false` 로 **찍어서 보여 준다** → [[object-class]] · [[type-casting]]

다운캐스팅 앞에 두는 것이 원래 쓰임이다.

```java
if (vehicle instanceof Bus) {
    Bus bus = (Bus) vehicle;      // 확인했으니 ClassCastException 이 나지 않는다
    bus.openBackDoor();
}
```

### 21일 뒤, 검사와 캐스팅이 한 줄이 된다

Day35 의 `AbstractMenu.equals` 가 **타입 이름 뒤에 변수 이름을 하나 더 붙인** 표기를 쓴다.

```java
@Override
public boolean equals(Object object) {
  if (this == object)
    return true;
  if (!(object instanceof AbstractMenu that))    // ← 검사하고 동시에 담는다
    return false;
  return Objects.equals(title, that.title);      // ← 캐스팅 없이 필드에 닿는다
}
```

```java
레퍼런스 instanceof 클래스명 변수명
```

`true` 일 때 그 변수에 **캐스팅된 값이 들어간다.** 자바 16에서 정식이 된 표기이고, 같은 클래스가 `StringBuilder.isEmpty()`(자바 15부터)를 쓰고 있으므로 이 코드는 그만한 버전을 전제한다.

**변수가 쓸 수 있는 범위가 「검사가 참인 곳」으로 정해지는 것**이 이 표기의 핵심이고, 위 코드가 그 규칙의 재미있는 경우다. 검사를 `!` 로 뒤집었으므로 **`if` 블록 안이 아니라 그 뒤가** `that` 의 범위다 — `if` 안에서 `return` 해 버리므로 아래로 내려온 실행 흐름에서는 `object` 가 `AbstractMenu` 임이 확정되어 있고, 컴파일러가 그것을 따라간다. 블록이 아니라 **흐름**이 범위를 정하는 것이라 중괄호를 보고 판단하면 틀린다 → [[variable-scope]]

같은 클래스 가족의 다른 자리는 여전히 옛 표기다.

```java
public void add(Menu child) {
  if (child instanceof MenuGroup) {
    ((MenuGroup) child).setParent(this);      // 검사 따로, 캐스팅 따로
  }
  children.add(child);
}
```

**한 회차의 코드 안에 두 표기가 나란히 있다.** 새 표기를 배운 자리(`equals`)에만 쓰고 다른 자리는 손대지 않은 것이고, 여기서 쓴다면 `if (child instanceof MenuGroup group) group.setParent(this);` 가 된다 → [[type-casting]]

## 왜 중요한가

**컴파일러가 아는 타입과 실행 중에 들어 있는 타입이 다를 수 있다는 것을 코드가 물을 수 있게 된다.** `Object obj` 라고 선언한 변수에 무엇이 들었는지 컴파일 시점에는 알 수 없고, 그것을 알아야 다운캐스팅을 안전하게 할 수 있다. `instanceof` 없이 캐스팅하면 **컴파일은 통과하고 실행 중에 터진다** → [[type-casting]] · [[exception-handling]]

**거꾸로, `instanceof` 가 많이 필요해진다는 것은 신호다.** 타입마다 분기해야 한다는 뜻이고, 그 분기를 각 클래스의 메서드로 옮기면 사라진다. 그래서 이 연산자는 **필요할 때 쓰는 안전장치이면서 설계 냄새의 지표**이기도 하다 → [[polymorphism]]

**Day35 의 메뉴 트리가 그 지표를 실제로 재게 해 준다.** 잎과 가지가 섞인 목록을 돌며 실행하는데 `instanceof` 가 순회 코드에는 하나도 없고, 남은 자리는 **트리를 세우는 `add` 하나**다. 「가지를 넣을 때만 부모를 세운다」는 것은 다형성으로 표현할 수 없는 일이라(잎에는 부모라는 개념이 없다) 그 한 자리는 검사로 남는 것이 맞다. **없애야 하는 검사와 남아야 하는 검사를 가르는 기준이 「그 일이 각 타입의 책임으로 옮겨질 수 있나」**이고, 검사가 하나로 줄면 그 물음을 한 번만 하면 된다 → [[composite-pattern]]

## 경계와 오해

- **`instanceof` ≠ `getClass()` 비교** — `instanceof` 는 **서브클래스도 `true`** 이고, `getClass() != obj.getClass()` 는 **정확히 같은 클래스일 때만** 통과한다. 그래서 `equals()` 를 만들 때 어느 쪽을 쓰는가가 결정이 된다 — 필기의 `equals` 는 `getClass()` 를 골랐고, 그러면 자식 인스턴스는 부모와 절대 같지 않게 된다 → [[object-equality]] · [[class-metadata]]
- **`null instanceof X` 는 `false` 다 — 예외가 아니다** — 그래서 `null` 검사를 겸할 수 있다. Day21 의 `equals` 가 `if (obj == null) return false;` 를 따로 두고 있는데, `getClass()` 를 부르기 전에 막아야 하기 때문이다. `instanceof` 로 썼다면 그 줄이 필요 없었다 — **21일 뒤 Day35 의 `equals` 에 그 줄이 실제로 없다.** 그리고 패턴 변수를 쓰면 「`null` 이면 담기지 않는다」까지 따라오므로, `null` 검사·타입 검사·캐스팅 세 가지가 한 줄에 접힌다 → [[object-reference]] · [[object-equality]]
- **관계가 없는 타입끼리는 컴파일 오류가 난다** — `obj instanceof String` 이 통과한 것은 `obj` 의 선언 타입이 `Object` 라서다. 선언 타입이 `My` 였다면 `My` 와 `String` 은 상속 관계가 없으므로 그 줄 자체가 컴파일되지 않는다. **`false` 가 나오는 것과 못 물어보는 것이 다르다.**
- **`true` 라고 그 타입의 멤버를 쓸 수 있게 되는 것은 아니다 — 패턴 변수를 쓰면 달라진다** — 검사와 캐스팅은 **원래** 별개의 두 줄이다. `if (obj instanceof My)` 블록 안에서도 `obj` 의 타입은 여전히 `Object` 이므로 `My` 의 필드를 쓰려면 `(My) obj` 로 되돌려야 한다. **Day35 가 쓴 `object instanceof AbstractMenu that` 은 그 둘을 한 줄로 묶어** `that` 을 통해 곧바로 필드에 닿는다. 다만 열리는 것은 **새 변수**이고 원래 변수는 그대로다 — 그 코드에서도 `object` 의 타입은 여전히 `Object` 이므로 `object.title` 은 컴파일되지 않는다. **「검사하면 타입이 바뀐다」가 아니라 「검사한 결과를 담은 변수가 하나 생긴다」**로 읽어야 이 차이가 설명된다 → [[variable]]
- **패턴 변수의 범위는 중괄호가 아니라 흐름이 정한다** — `if (obj instanceof My m) { ... }` 는 블록 안이 범위이고, `if (!(obj instanceof My m)) return;` 은 **그 뒤가** 범위다. `&&` 로 이으면 오른쪽에서 쓸 수 있고(`obj instanceof My m && m.age > 20`) `||` 로 이으면 못 쓴다 — 왼쪽이 거짓일 때 오른쪽이 실행되므로 담긴 것이 없다. **컴파일러가 「여기서는 확실히 참이다」를 따라가며 범위를 계산하는 것**이고, 이 규칙을 모르면 되는 자리와 안 되는 자리가 임의로 보인다 → [[variable-scope]] · [[short-circuit-evaluation]]
- **필기의 「super 클래스의 인스턴스 있지 확인하는」은 「있는지」의 오기이고, 「super 클래스」도 좁다** — 직접 부모만이 아니라 **모든 조상**이 `true` 다. 같은 절의 `obj instanceof Object` 가 그 증거인데, `My` 의 직접 부모가 곧 `Object` 여서 이 예제만으로는 둘이 구별되지 않는다 → [[inheritance]]
- **`instanceof` 는 배열과 인터페이스에도 쓴다** — 클래스 전용이 아니다. 필기 예제가 클래스 셋뿐이라 그렇게 읽히기 쉽다.

## 함께 보는 개념

- [[type-casting]] — `instanceof` 로 확인한 뒤 하는 일
- [[object-class]] — 무엇을 물어도 `true` 가 되는 조상
- [[polymorphism]] — `instanceof` 분기를 없애는 방향
- [[object-equality]] — `getClass()` 와 갈리는 결정
- [[class-metadata]] — 실제 타입을 얻는 다른 경로
- [[inheritance]] — `true` 의 범위를 정하는 관계
- [[object-reference]] — 검사 대상이 되는 것
- [[operator]] — 이 연산자가 속한 갈래
- [[if-statement]] — 이 검사가 놓이는 자리
- [[variable-scope]] — 패턴 변수를 쓸 수 있는 범위를 정하는 규칙
- [[short-circuit-evaluation]] — `&&`·`||` 에서 패턴 변수가 갈리는 이유
- [[composite-pattern]] — 검사가 한 자리로 줄어든 구조
- [[variable]] — 패턴 변수가 여는 것

## 출처

- [[2024-06-24-Day21]] — `Object obj = new My()` 로 담고 `obj instanceof My`·`instanceof String`·`instanceof Object` 를 찍어, `extends` 를 쓰지 않은 클래스도 `Object` 의 서브클래스임을 증명하는 도구로 배웠다. 「지정한 클래스의 인스턴스이거나 super 클래스의 인스턴스인지」라는 정의도 이 자리다
- [[2024-07-15-Day35]] — **검사와 캐스팅을 한 줄로 묶는 패턴 변수 표기**(`object instanceof AbstractMenu that`, 자바 16 정식)를 `AbstractMenu.equals` 에서 처음 쓴다. Day21 의 `equals` 골격에서 `null` 검사와 다운캐스팅 두 줄이 사라진 것이 그 결과이고, 검사를 `!` 로 뒤집었으므로 `that` 의 범위가 `if` 블록이 아니라 **그 뒤**라는 흐름 기반 스코프도 여기서 드러난다. 같은 회차의 `MenuGroup.add` 는 `child instanceof MenuGroup` 뒤에 `((MenuGroup) child)` 로 캐스팅하는 옛 표기를 그대로 써서 **한 코드에 두 표기가 나란히 있다.** 그리고 컴포짓 트리에서 순회·실행 코드에는 검사가 하나도 없고 `add` 한 자리에만 남아, 「`instanceof` 가 많으면 설계 냄새」의 반대쪽 — **남는 것이 맞는 검사** — 를 볼 수 있다
