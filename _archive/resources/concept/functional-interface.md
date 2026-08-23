---
type: concept
id: functional-interface
title: 함수형 인터페이스 (Functional Interface)
aliases:
  - 함수형 인터페이스
  - 함수형인터페이스
  - functional interface
  - FunctionalInterface
  - 단일 추상 메서드
  - SAM
  - SAM 인터페이스
tags:
  - 자바
  - 문법
  - 함수형
  - 추상화
up:
  - 2024-07-16-Day36
  - 2024-07-17-Day37
  - 2024-08-05-Day48
---

# 함수형 인터페이스 (Functional Interface)

**추상메서드가 정확히 하나뿐인 인터페이스.** 그 하나가 람다식이 채울 자리이고, 하나뿐이라는 조건이 곧 「이 람다가 무엇을 구현하는지」를 컴파일러가 물어볼 필요 없이 알게 되는 근거다. Day36 이 그 순서로 적었다 — 「람다식을 구현하기 위해서는 하나의 추상메서드를 가진 인터페이스가 필요하다 / 이러한 인터페이스를 함수형 인터페이스라고 부르며」 → [[lambda-expression]]

## 정의

두 가지가 별개다.

| | 무엇 | 없으면 |
|---|---|---|
| **조건** | 추상메서드가 하나뿐이다 | 람다를 쓸 수 없다 |
| **표시** | `@FunctionalInterface` | **아무 일도 없다** — 조건만 맞으면 람다는 그대로 된다 |

```java
@FunctionalInterface
interface Player{
    void play();
}
```

세는 것은 **추상메서드**뿐이다. `default`·`static`·`private` 메서드는 몇 개가 있어도 함수형이고, 상수필드도 세지 않는다 → [[default-method]] · [[interface]]

그리고 그 하나의 **시그니처가 계약이다.** 하루 뒤 Day37 이 그것을 명시적인 규칙 셋으로 적는다 — 끼워질 메서드는 **매개변수 개수가 같고**, 매개변수 타입은 **더 넓어도 되고**, 반환 타입은 **더 좁아야** 한다. 「추상메서드가 하나」가 *쓸 수 있는지*를 정하고, 그 하나의 시그니처가 *무엇을 끼울 수 있는지*를 정한다 → [[method-reference]]

## 사용 예시

Day36 이 함수형 인터페이스를 셋 만들고 각각을 람다로 채운다. **셋의 모양이 곧 람다 세 장의 순서다.**

```java
interface Calculable{ void calculate(int x, int y); }   // 매개변수 둘, 반환 없음
interface Player{ void play(); }                        // 매개변수 없음
interface Intro { void introduce(String s); }           // 매개변수 하나
interface InterestCalculator { double compute(int money); }  // 반환값 있음
```

```java
InterestCalculator c6 = Factory.create6(0.025);
System.out.println(c6.compute(10000000));
```

**부르는 쪽은 끝까지 인터페이스 이름만 안다.** `create6` 이 돌려준 것이 로컬 클래스의 인스턴스인지 익명 클래스인지 람다인지 `compute(10000000)` 을 쓰는 자리에서는 구별되지 않는다 — Day36 이 여섯 개를 만들어 여섯 번 `compute` 를 부르는 `Test` 가 그것을 보이려던 코드다 → [[polymorphism]]

**Day37 은 반대쪽에서 같은 것을 시험한다 — 구현을 고정하고 인터페이스를 바꿔 본다.** 추상메서드의 반환형만 다른 함수형 인터페이스 여섯 개를 세우고 같은 `int plus(int,int)` 를 전부에 끼워 본다.

```java
interface Calculator1 {double compute(int a, int b);}
interface Calculator3 {short compute(int a, int b);}
interface Calculator4 {void compute(int a, int b);}
interface Calculator6 {String compute(int a, int b);}

Calculator1 c1 = MyCalculator::plus; // OK!
// Calculator3 c3 = MyCalculator::plus; // 컴파일 오류!
Calculator4 c4 = MyCalculator::plus; // OK!
// Calculator6 c6 = MyCalculator::plus; // 컴파일 오류!
```

**같은 메서드가 어떤 인터페이스에는 끼워지고 어떤 인터페이스에는 안 끼워진다.** 통과 여부를 정하는 것이 구현 쪽이 아니라 **선언한 추상메서드의 반환형 하나**이므로, 함수형 인터페이스를 만드는 일이 곧 「무엇을 받아 줄지 정하는 일」이라는 것이 여기서 코드로 보인다.

그리고 매개변수 쪽에서는 **인터페이스가 생성자까지 고른다.**

```java
static interface Factory1 { Message get(); }
static interface Factory2 { Message get(String name); }

Factory1 f1 = Message::new;   // Message() 가 골라진다
Factory2 f2 = Message::new;   // Message(String) 이 골라진다
```

오른쪽 다섯 글자가 같고 **왼쪽 타입만 다른데 실행되는 생성자가 다르다** — 함수형 인터페이스가 「자리」가 아니라 **고르는 주체**로 드러나는 자리다 → [[method-reference]] · [[constructor]]

### 20일 뒤 Day48 — 표준 함수형 인터페이스를 처음 쓴다

아래 「경계와 오해」에 「자바가 이미 만들어 둔 것을 쓰는 편이 흔하다 — 필기는 직접 선언하는 쪽만 다룬다」고 적어 둔 자리에 쓰레드 회차가 첫 반례를 준다. **`Runnable` 이 그것이고, 추상메서드가 `void run()` 하나뿐이라 함수형 인터페이스다** — Day36 이 손으로 만든 `Player{void play()}` 와 모양이 같은 표준 타입이다 → [[thread]]

```java
// Day48 이 쓴 형태 — 익명 클래스
new Thread(new Runnable() {
  @Override
  public void run() { /* 쓰레드가 실행할 코드 */ }
});

// 추상메서드가 하나이므로 그대로 줄어든다
new Thread(() -> { /* 쓰레드가 실행할 코드 */ });
```

**Day48 은 익명 클래스 쪽을 「실무에서는 이 방법이 활용도가 높다」로 적는다.** 20일 전에 로컬 클래스 → 익명 클래스 → 람다 사다리를 세 번 올랐는데, 그 사다리의 마지막 칸이 여기 그대로 적용되는 것을 연결하지 않았다. **함수형 인터페이스를 「내가 선언하는 것」으로만 배우면 남의 인터페이스에 대해 그 조건을 세어 볼 생각이 들지 않고**, 그러면 람다를 쓸 수 있는 자리인지 알 방법이 없다 → [[lambda-expression]] · [[anonymous-class]]

## 왜 중요한가

**「추상메서드가 하나」라는 조건이 람다에서 메서드 이름을 지울 수 있게 해 준다.** `()->{…}` 에는 어느 메서드를 채우는지가 적혀 있지 않다. 채울 자리가 둘이면 그 식이 무엇인지 정할 방법이 없으므로, **하나라는 제약은 문법의 편의가 아니라 성립 조건**이다.

**그 하나가 「무엇을 끼울 수 있나」의 자격 심사표가 된다.** Day37 의 `MyCalculator::power` 는 하는 일이 이상해서 거절되는 것이 아니라 **매개변수가 하나**라서 거절된다 — 나머지 넷과 반환형·접근 지정자·클래스가 전부 같다. 인터페이스를 선언하는 순간 「어떤 모양의 메서드가 여기 들어올 수 있나」가 정해지고, 그 뒤로는 **컴파일러가 대입문 한 줄에서 그것을 검사한다** → [[method-reference]] · [[parameter-and-argument]]

**「이 인터페이스를 구현했나」를 클래스 선언에서 묻지 않게 된다.** Day37 의 `MyCalculator`·`Calculator`·`Message` 에는 `implements` 가 하나도 없는데 `Calculator`·`Interest`·`Factory1`·`Factory2` 의 구현체로 쓰인다. **모양만 맞으면 되므로 이미 있는 클래스를, 손대지 않고, 나중에 만든 함수형 인터페이스에 끼울 수 있다** — 이 타입이 상속 계층과 무관하게 재사용 가능한 이유가 여기다 → [[method-reference]] · [[interface]]

**약속을 깨는 변경이 나는 위치를 옮긴다.** `@FunctionalInterface` 를 붙여 두면 나중에 그 인터페이스에 추상메서드를 하나 더 넣는 순간 **그 인터페이스 파일에서** 컴파일 오류가 난다. 안 붙였으면 인터페이스는 조용히 통과하고 **그것을 람다로 쓴 모든 자리**가 한꺼번에 깨진다. 하나를 고치는 것과 스무 곳이 붉어지는 것의 차이이고, 이것이 이 애노테이션이 실제로 하는 일 전부다 → [[annotation]]

**함수형인지 아닌지가 인터페이스를 설계할 때의 축이 된다.** 메서드를 하나 더 얹으면 그 타입은 람다로 못 쓰이게 된다. 하루 전 회차의 `Command` 가 `execute(String)` 하나를 지켰기 때문에 람다로 쓸 수 있는 상태였고, 엿새 전의 `Iterator` 는 `hasNext`·`next` 둘이라 그 길이 없다 — **인터페이스를 좁게 유지하는 것에 문법적 보상이 붙는 것**이 여기서 처음 생긴다 → [[interface-segregation-principle]] · [[command-pattern]]

## 경계와 오해

- **`@FunctionalInterface` 를 붙여야 람다가 되는 것이 아니다 — Day36 자신이 반증한다** — 필기는 「이러한 인터페이스를 함수형 인터페이스라고 부르며, 어노테이션은 @FunctionalInterface라고 한다」로 애노테이션을 함수형 인터페이스의 일부처럼 적었지만, **정작 `Intro` 와 `InterestCalculator` 에는 붙이지 않고 둘 다 람다로 쓴다.** 붙은 것은 `Player` 하나뿐이다. 애노테이션은 자격증이 아니라 **조건이 유지되는지 컴파일러에게 검사시키는 자물쇠**다. **하루 뒤 Day37 은 함수형 인터페이스를 다섯 개(`Cal`·`Calculator`·`Interest`·`Factory1`·`Factory2`) 와 반환형만 다른 여섯 개(`Calculator1`~`Calculator6`) 를 더 세우면서 애노테이션을 하나도 붙이지 않고 전부 정상 동작시킨다** — 붙은 것은 Day36 의 `Player` 하나로 끝이고, 그 대비가 열한 개로 늘었다 → [[annotation]]
- **추상메서드 하나 ≠ 메서드 하나** — `default` 메서드와 `static` 메서드는 몸통이 있으므로 람다가 채울 것이 없고, 따라서 몇 개든 함수형 인터페이스로 남는다. 표준 라이브러리의 `Comparator` 가 그 예다 — `compare` 하나만 추상이고 `reversed`·`thenComparing` 등이 `default` 로 잔뜩 붙어 있는데도 람다로 쓴다. 「메서드가 하나뿐인 작은 인터페이스」로 외우면 이 자리가 설명되지 않는다 → [[default-method]]
- **`Object` 의 `public` 메서드를 다시 선언해도 세지 않는다** — `equals`·`hashCode`·`toString` 을 추상메서드로 한 번 더 적어도 함수형 인터페이스다. 구현 객체는 어차피 `Object` 로부터 그것을 갖고 있어 **채울 것이 없기 때문**이다 → [[object-class]]
- **인터페이스가 아니면 안 된다** — 추상메서드가 딱 하나인 **추상 클래스**를 만들어도 람다로는 구현할 수 없다. 익명 클래스는 되는데(`new 추상클래스(){…}`) 람다는 안 된다 — 람다는 상속 계층에 끼어드는 것이 아니라 인터페이스 구현체를 만드는 문법이기 때문이다. **엿새 전 회차의 네 방식 중 익명 클래스까지는 추상 클래스에도 통했다는 것**과 갈리는 자리다 → [[abstract-class]] · [[anonymous-class]]
- **`Thread` 는 함수형 인터페이스가 아니다 — Day48 이 두 형태를 나란히 놓아 그 경계를 보여 준다** — 같은 절의 `new Thread(new Runnable(){…})` 는 람다로 줄어들고 `new Thread(){…}` 는 줄어들지 않는다. 뒤쪽은 **클래스를 상속하는 익명 클래스**이고, 덮는 `run()` 은 추상메서드가 아니라 **구현이 있는 메서드**다. 두 코드의 겉모양이 거의 같아서 「익명 클래스는 다 람다로 줄어든다」로 읽기 쉬운데, **갈리는 것은 `new` 뒤에 적힌 것이 인터페이스인가 클래스인가 하나뿐**이다 → [[thread]] · [[method-overriding]]
- **함수형 인터페이스는 애노테이션 이름이 아니라 내가 만든 타입 이름이다** — 필기의 문장이 둘을 나란히 놓아 겹쳐 읽히는데, 함수형 인터페이스는 `Player`·`Intro`·`InterestCalculator` 이고 `@FunctionalInterface` 는 그 선언 위에 붙이는 표시다. **「함수형 인터페이스를 만든다」는 `@FunctionalInterface` 를 쓰는 일이 아니라 추상메서드를 하나만 두는 일**이다.
- **자바가 이미 만들어 둔 것을 쓰는 편이 흔하다 — 필기는 직접 선언하는 쪽만 다룬다** — `Player`(`void play()`)는 `Runnable` 과 모양이 같고, `InterestCalculator`(`double compute(int)`)는 `IntToDoubleFunction` 과 같다. `java.util.function` 의 `Function`·`Supplier`·`Consumer`·`Predicate` 가 그런 자리를 미리 채워 둔 것들이다. **직접 선언하면 이름이 도메인을 말해 주고(그래서 Day36 의 선택이 배우는 데는 낫다), 표준 것을 쓰면 조합용 `default` 메서드가 딸려 온다** → [[default-method]]
- **시그니처가 같아도 같은 타입이 아니다 — 끼워지는 것은 메서드이고 인터페이스끼리는 안 통한다** — Day36 의 `Player{void play()}` 와 표준 `Runnable{void run()}` 은 모양이 같지만 `Runnable r = player;` 는 컴파일되지 않는다. `Interest` 와 `IntToDoubleFunction` 도 그렇다. **모양만 맞으면 되는 것은 `::`·람다로 들어오는 쪽뿐이고**(그래서 `implements` 없는 `MyCalculator` 가 통한다) 이미 만들어진 함수형 인터페이스 인스턴스를 다른 함수형 인터페이스로 넘기려면 `r = player::play` 처럼 **다시 한 번 끼워야** 한다. Day37 이 `Calculator1`~`Calculator6` 을 여섯 개 세우고 그 사이를 서로 대입해 보지 않아서 이 경계가 그 회차에 드러나지 않았다 → [[method-reference]] · [[type-casting]]
- **하나여야 하는 것은 「내가 선언한 것」이 아니라 「상속까지 합친 것」이다** — 인터페이스가 다른 인터페이스를 `extends` 하면 물려받은 추상메서드까지 합쳐 세므로, 자기 몸에 아무것도 안 적었어도 함수형이 아닐 수 있다 → [[multiple-inheritance]] · [[inheritance]]

## 함께 보는 개념

- [[lambda-expression]] — 이 인터페이스의 추상메서드 하나를 채우는 식
- [[method-reference]] — 이미 있는 메서드를 그 자리에 끼우는 표기
- [[constructor]] — 함수형 인터페이스가 어느 것을 고를지 정하는 대상
- [[interface]] — 함수형 인터페이스가 특수한 경우인 상위 문법
- [[annotation]] — `@FunctionalInterface` 가 하는 검사
- [[default-method]] — 추상메서드 수에 세지 않는 멤버
- [[anonymous-class]] — 같은 인터페이스를 채우는 다른 방법
- [[abstract-class]] — 람다로는 갈 수 없는 쪽
- [[interface-segregation-principle]] — 인터페이스를 좁게 두는 것에 보상이 붙는 자리
- [[object-class]] — 다시 선언해도 세지 않는 메서드들의 출처
- [[functional-programming]] — 이 타입이 존재하는 이유
- [[polymorphism]] — 구현이 무엇이든 같은 이름으로 부르게 하는 성질
- [[thread]] — 표준 함수형 인터페이스(`Runnable`)를 처음 쓰는 자리

## 출처

- [[2024-07-16-Day36]] — 람다식을 설명하는 도중에 「람다식을 구현하기 위해서는 하나의 추상메서드를 가진 인터페이스가 필요하다」로 이 조건을 세우고 이름과 애노테이션을 붙였다. 실제로 `Calculable`·`Player`·`Intro`·`InterestCalculator` 넷을 선언해 매개변수 없음 · 하나 · 둘 · 반환값 있음을 각각 담았는데, **`@FunctionalInterface` 는 `Player` 에만 붙어 있고 나머지도 람다로 잘 쓰인다** — 애노테이션이 조건이 아니라 검사 장치라는 것이 그 대비로 드러난다. 「어노테이션은 @FunctionalInterface라고 한다」는 문장은 타입 이름과 애노테이션 이름을 겹쳐 읽게 만들고, `default`·`static` 메서드는 세지 않는다는 것, 추상 클래스에는 쓸 수 없다는 것, `java.util.function` 의 기성 인터페이스들은 Day36 에 나오지 않는다
- [[2024-08-05-Day48]] — **표준 함수형 인터페이스를 처음 쓴다** — `Runnable` 은 추상메서드가 `void run()` 하나뿐이라 이 조건을 만족하고, Day36 이 손으로 만든 `Player{void play()}` 와 모양이 같다. 다만 채우는 방법으로 **람다가 아니라 익명 클래스**를 골라 「실무에서는 이 방법이 활용도가 높다」로 적었고, 20일 전 사다리의 마지막 칸이 여기 그대로 쓰일 수 있다는 것은 연결되지 않았다. 같은 절에 `new Thread(){…}`(클래스 상속) 형태가 나란히 있어 **한쪽만 람다로 줄어드는 경계**가 우연히 함께 놓였는데, 필기는 두 형태를 「Runnable 구현 / Thread 상속」의 차이로만 다루고 람다 가능성으로는 보지 않았다
- [[2024-07-17-Day37]] — 하루 뒤 회차가 **시험 방향을 뒤집는다** — 구현을 `int plus(int,int)` 하나로 고정하고 **인터페이스를 바꿔 가며** 통과 여부를 본다. 반환형만 다른 `Calculator1`~`Calculator6` 여섯 개로 `double`·`float`·`void`·`Object` 는 되고 `short`·`String` 은 안 되는 것을 확인하고, `MyCalculator::power` 하나만 거절되는 것으로 **매개변수 개수**가 걸리는 축임을 보인다. 그래서 추상메서드 하나가 *채울 자리*이기만 한 것이 아니라 **끼울 수 있는 것을 고르는 시그니처 계약**이라는 것이 이 회차에서 드러나고, 규칙 셋(개수 동일 · 매개변수는 넓게 · 반환은 좁게)이 「인스턴스 메서드 레퍼런스 구현」 절에 적힌다(같은 노트의 스태틱 장은 「매개변수와 동일해야」로 어긋나게 적혀 있다). `Factory1 get()` 과 `Factory2 get(String)` 은 **똑같은 `Message::new` 로 서로 다른 생성자를 고르게** 해서 인터페이스가 고르는 주체임을 보여 준다. 이 회차의 함수형 인터페이스 열한 개에 **`@FunctionalInterface` 가 하나도 없고** 전부 정상 동작한다. 시그니처가 같은 함수형 인터페이스끼리는 서로 대입되지 않는다는 것과 `implements` 없는 클래스가 구현체가 되는 것이 무엇을 여는지는 적히지 않았다 → [[method-reference]]
