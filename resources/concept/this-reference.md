---
type: concept
id: this-reference
title: this 레퍼런스
aliases:
  - this
  - this 레퍼런스
  - this 포인터
  - 암시적 매개변수
  - implicit parameter
up:
  - 2024-06-17-Day16
  - 2024-07-10-Day32
  - 2024-07-11-Day33
tags:
  - java
  - 객체지향
  - 메서드
  - 문법
---

# this 레퍼런스

인스턴스 메서드를 호출하면 **컴파일러가 대상 인스턴스의 주소를 숨은 첫 매개변수로 넘긴다.** 그 매개변수의 이름이 `this` 다. 그래서 `this` 는 특별한 마법이 아니라 **직접 넘기던 것을 대신 넘겨 주는 것**이다.

## 정의

같은 일을 손으로 하면 이렇게 된다.

```java
// 대상을 매개변수로 직접 받는다
static void plus(Calculator that, int a) {
  that.result += a;
}
Calculator.plus(c1, 2);

// 인스턴스 메서드 — 컴파일러가 대상을 넘겨 준다
void plus(int a) {
  this.result += a;
}
c1.plus(2);
```

**대상이 인수 목록에서 점 앞으로 옮겨간 것**이 전부다. `this.` 는 생략할 수 있고, 생략하면 컴파일러가 붙여 준다.

| | `static` 메서드 | 인스턴스 메서드 |
|---|---|---|
| 대상 | 매개변수로 받는다 (`Calculator that`) | `this` 로 자동으로 들어온다 |
| 호출 | `Calculator.plus(c1, 2)` | `c1.plus(2)` |
| 대상이 없을 때 | 안 받으면 된다 | 성립하지 않는다 — 그래서 `static` 문맥에는 `this` 가 없다 |

필기의 정리가 이 관계를 그대로 적어 뒀다.

```text
non-static 메서드를 선언하면 컴파일러 내부에서 this 레퍼런스를 생성하여 자동으로 넘긴다.
ex) Cal c1, Cal c2에서 this는 각각 c1,c2의 레퍼런스를 의미 하지만
ex) static은 Cal을 의미하므로 this로 접근 할 수 없다.
```

## 사용 예시

이 필기의 `Calculator` 는 세 단계를 거친다. 하는 일(`result` 에 더하기)은 끝까지 같고, **대상을 누가 어떻게 지정하는가**만 바뀐다.

```java
// 1단계 — 클래스 필드. 계산기가 프로그램 전체에 하나뿐이라 대상을 말할 필요가 없다
static int result = 0;
static void plus(int a) { result += a; }
Calculator.plus(2);
```

```java
// 2단계 — 인스턴스 필드. 대상이 여러 개가 되자 메서드가 그것을 받아야 한다
int result = 0;
static void plus(Calculator that, int a) { that.result += a; }
Calculator.plus(c1, 2);
```

```java
// 3단계 — 인스턴스 메서드. 넘기던 대상이 점 앞으로 간다
int result = 0;
void plus(int a) { this.result += a; }
c1.plus(2);
```

`Score` 에서도 같은 이동이 한 번 더 일어난다.

```java
// Test02 의 static 메서드였다
static void compute(Score s) {
  s.sum = s.kor + s.eng + s.math;
  s.aver = (float) s.sum / 3;
}
compute(s1);
```

```java
// Score 안으로 옮기고 s → this 가 되었다
void compute() {
  this.sum = this.kor + this.eng + this.math;
  this.aver = (float) this.sum / 3;
}
s1.compute();
```

**본문에서 바뀐 것은 `s.` 가 `this.` 로 된 것뿐이다.** 대신 메서드가 사는 곳이 `Test02` 에서 `Score` 로 옮겨졌고, 그래서 `Score` 를 쓰는 누구든 이 계산을 같이 얻는다.

같은 필기가 `printScore(Score s)` 는 옮기지 않았다. `compute` 는 `Score` 의 필드만으로 답이 나오지만 `printScore` 는 출력 대상(`System.out`)에 의존하므로, 옮기면 `Score` 가 화면을 알게 된다.

### `this` 가 둘이 되는 자리

**23일 뒤 중첩 클래스 회차가 같은 구조를 한 겹 더 쌓는다.** 인스턴스 멤버 클래스의 인스턴스에는 `this` 외에 **바깥 인스턴스의 주소**도 들어오고, 그것을 넘기는 것도 컴파일러다. 필기가 그것을 주석 한 줄로 적었다.

```java
public abstract class AbstractList implements List {
  // 컴파일러: 바깥 클래스의 인스턴스 주소를 전달하는 코드로 자동 변환
  public Iterator iterator() {
    return new ListIterator();          // 인수가 없는데 바깥 주소가 넘어간다
  }

  public class ListIterator implements Iterator {
    private int cursor;

    @Override
    public boolean hasNext() {
      return cursor < AbstractList.this.size();     // 바깥의 것
    }

    @Override
    public Object next() {
      return get(cursor++);                          // 생략된 AbstractList.this
    }
  }
}
```

**`Calculator that` 이 `this` 가 된 것과 같은 일이 한 층 위에서 반복된다.** 정적 중첩 클래스로 쓰면 `new ListIterator(this)` 로 **손으로 넘겨야** 하고, `static` 을 떼면 그 인수가 사라진다 — Day16 의 2단계와 3단계가 그대로 다시 나온 것이다 → [[nested-class]] · [[static-member]]

`this` 가 둘이므로 이름 붙이는 규칙이 필요하다.

| 쓰는 말 | 가리키는 것 |
|---|---|
| `this` | 중첩 클래스의 인스턴스(`ListIterator`) |
| `바깥클래스명.this` | 바깥 인스턴스(`AbstractList`) |
| 아무것도 안 씀 | 중첩 클래스에 그 이름이 있으면 자기 것, 없으면 바깥 것 |

Day32 가 마지막 줄을 코드 주석으로 적었다 — 「중첩 클래스 안에 해당 필드나 메서드가 없다면 바깥클래스명.this 생략 가능」.

### 하루 뒤 회차가 `this$0` 이라는 이름을 꺼낸다

**Day32 의 「컴파일러가 자동으로 변환한다」가 필드 이름과 생성자 시그니처로 채워진다.**

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

**`B2.this` 는 소스에 쓰는 문법이고 `this$0` 은 그것이 컴파일된 뒤의 모습이다.** Day16 에서 `this` 가 「숨은 첫 매개변수」였던 것과 같은 관계다 — 이번에는 그 숨은 것이 **생성자의 매개변수 하나와 필드 하나**로 두 군데에 자리를 잡는다 → [[nested-class]]

그리고 `this` 가 있는지 없는지가 **인스턴스를 만들 수 있는지**를 정한다. 같은 회차가 그 대비를 주석으로 적어 두었다.

```java
class A {
    static void m1(int a) {
        // static 메서드는 A의 인스턴스를 저장하는 this 라는 변수가 없다.
    }
    void m2(int b) {
        // non-static 메서드는 A의 인스턴스를 저장할 this라는 변수가 있다.
    }
    class X {}
}
```

```java
class C {
    static void m1() {
        X obj;                    // 레퍼런스 선언은 가능!
        //  obj = this.new X();   // 컴파일 오류! 인스턴스 생성 불가능!
    }

    void m2() {
        X obj = this.new X();     // 넘길 this 가 있다
        X obj2 = new X();         // 인스턴스 필드나 메서드와 마찬가지로 this를 생략할 수 있다.
    }

    class X { void test() {} }
}
```

**`this.new X()` 는 `this` 를 인수가 아니라 점 앞에 쓰는 세 번째 자리다.** 메서드 호출의 수신자도 필드 접근의 대상도 아니고 **「어느 바깥 인스턴스에 붙일 객체인가」**를 지정한다. 그래서 `static` 메서드에서 막히는 것은 문법이 아니라 **넘길 것이 없다는 사실**이고, 필기가 「인스턴스 멤버를 사용하기 위해서는 인스턴스를 주소를 담고 있는 this변수가 필요하다」로 그 이유를 적었다 → [[static-member]]

## 왜 중요한가

**`static` 메서드에서 인스턴스 필드에 못 닿는 이유가 규칙이 아니라 구조로 설명된다.** `static` 문맥에는 넘어온 대상이 없으므로 「누구의 `result`」인지 쓸 방법이 없다. 그래서 컴파일 오류이고, 그 오류를 피하려고 필드에 `static` 을 붙이는 순간 값이 하나로 합쳐진다 → [[static-member]]

**메서드 코드는 한 벌이고 데이터만 인스턴스마다 있다.** `c1.plus(2)` 와 `c2.plus(2)` 가 서로 다른 `result` 를 고치는 것은 메서드가 인스턴스마다 복사되기 때문이 아니라 **넘어오는 `this` 가 다르기 때문**이다. 인스턴스를 만드는 비용에 메서드가 포함되지 않는 이유도 여기다 → [[instance]]

그리고 **`Calculator.plus(c1, 2)` 와 `c1.plus(2)` 는 동작이 같은데 읽히는 방향이 반대다.** 앞은 「클래스가 데이터를 처리한다」, 뒤는 「데이터가 스스로 한다」다. 이 자리 이동이 나중에 [[polymorphism]] 을 가능하게 한다 — 실제로 실행될 메서드가 대상의 타입에 따라 갈릴 수 있는 것은, 대상이 인수 중 하나가 아니라 **점 앞의 수신자**이기 때문이다.

## 경계와 오해

- **`this` ≠ 인스턴스 그 자체** — `this` 에 담긴 것은 인스턴스의 **주소**다. 그래서 `this` 를 다른 메서드에 넘길 수 있고, 넘긴 쪽이 같은 인스턴스를 고치는 것이 보인다 → [[object-reference]] · [[call-by-value]]
- **`this` 는 변수가 아니라 매개변수다** — `this = ...` 는 컴파일 오류다. 「현재 객체를 가리키는 특수 변수」로 외우면 재대입이 안 되는 이유가 설명되지 않는다. 값을 받는 자리라는 것이 실체다 → [[parameter-and-argument]]
- **`this.` 생략은 편의지만 생략할 수 없는 자리가 있다** — 매개변수 이름이 필드와 같을 때다. `this.name = name` 에서 `this.` 를 빼면 `name = name` 이 되어 **컴파일도 되고 실행도 되면서 아무 일도 하지 않는다.** 필드는 그대로 초기값이고 예외도 나지 않는다 → [[constructor]] · [[variable]]
- **"static으로 선언된 필드와 메소드는 … 접근 불가하다" 는 방향이 뒤집혀 있다** — 인스턴스 메서드는 `static` 멤버를 얼마든지 읽는다. 닿지 못하는 것은 그 반대쪽, **`static` 문맥에서 인스턴스 멤버로 가는 길**이다. 바로 다음 줄의 예시(`static은 Cal을 의미하므로 this로 접근 할 수 없다`)는 맞는 이해를 담고 있어서, 앞 문장은 표현이 엉킨 것으로 보인다 → [[static-member]]
- **"static 메서드를 접근 하려면 인스턴스 필드의 레퍼런스를 매개변수로 넘겨야한다" 도 조건이 뒤집혀 있다** — `static` 메서드를 **부르는** 데는 아무것도 필요 없다(`Calculator.plus(2)` 가 그렇다). 레퍼런스를 넘겨야 하는 것은 그 메서드가 **인스턴스의 데이터를 다뤄야 할 때**뿐이다. 이 구분이 흐려지면 2단계에서 `Calculator that` 이 왜 생겼는지 설명되지 않는다.
- **`that` 은 문법이 아니다** — 그냥 매개변수 이름이다. 예약어는 `this` 뿐이고, `that` 은 「`this` 가 될 자리를 손으로 쓴 것」이라는 뜻으로 이 필기가 고른 이름이다.
- **같은 클래스라면 다른 인스턴스의 필드도 만질 수 있다** — `that.result` 가 그 예다. 접근 제한은 **클래스 단위**여서 `private` 이어도 이 코드는 컴파일된다. 「`this` 것만 볼 수 있다」로 외우면 두 인스턴스를 비교하는 메서드를 왜 만들 수 있는지가 설명되지 않는다 → [[access-modifier]]
- **`this` 와 생성자의 `this(...)` 는 다른 것이다** — 뒤쪽은 같은 클래스의 다른 생성자를 부르는 문법이다. 이름만 같다 → [[constructor]]
- **`바깥클래스명.this.멤버` 에서 필드와 메서드가 갈린다** — `AbstractList.this.size()` 는 자식이 재정의한 `size()` 를 부르지만, `AbstractList.this.size` 라고 **필드**를 읽으면 부모의 것을 읽는다. 이틀 앞 회차에서 `ArrayList`·`LinkedList` 가 같은 이름의 필드를 다시 선언해 부모의 `size` 는 끝까지 `0` 이므로, **괄호를 빼는 순간 `hasNext()` 가 언제나 `false`** 가 되어 목록이 아무것도 찍지 않는다. `바깥클래스명.this` 로 지정하는 것이 「부모의 것을 쓴다」는 뜻이 아니라 **「어느 인스턴스인가」만 정하는 것**이고, 그 인스턴스 안에서 무엇이 선택되는지는 필드/메서드의 규칙이 따로 정한다 → [[field-hiding]] · [[method-overriding]]
- **`this.필드` 는 「내 것부터 찾아라」가 아니라 「내 것만 찾아라」다** — 중첩 클래스에서 `this.v3` 는 그 클래스에 `v3` 가 없으면 컴파일 오류인데, 같은 자리의 `v3`(지정 없이)는 바깥 인스턴스의 것을 잘 읽는다. **`this.` 는 이름 탐색을 도와주는 것이 아니라 한 층에 고정하는 것**이고, 그래서 하루 뒤 회차의 다섯 줄이 `v1` · `this.v1` · `B3.this.v1` 로 층마다 다른 값을 찍을 수 있었다 → [[variable-scope]]
- **`this` 는 한 층만 올라간다** — 중첩이 두 겹이면 `this` 로는 바깥의 바깥에 못 닿고 `A.this`·`B.this` 처럼 **층마다 클래스 이름을 써야** 한다. 「`this` 는 현재 객체」로만 기억하면 `B2.this` 라는 표기가 왜 필요한지가 설명되지 않는다.
- **필기의 「예2)」는 실제 컴파일 결과가 아니다** — `this.new X()` 의 변환을 두 가지로 적었는데(`예1) X obj = new X(this);` / `예2) X obj = new X(); obj.this$0 = this;`), **실제로 일어나는 것은 예1 뿐**이다. `this$0` 은 컴파일러가 만든 합성 필드라 소스에서 이름으로 대입할 수 없고, 애초에 생성자로 받는 이유가 예2 를 피하는 것이다 — 만든 다음에 채우면 **생성자가 도는 동안 바깥 참조가 `null` 인 구간**이 생기고, 그 사이에 바깥 필드를 읽는 초기화 코드가 있으면 `NullPointerException` 이 된다. 예2 는 「무슨 일이 일어나는가」의 설명으로는 통하지만 **순서까지 같은 것으로 읽으면 안 된다** → [[constructor]] · [[object-reference]]
- **`바깥클래스명.this` 는 `static` 문맥에서 쓸 수 없다** — 정적 중첩 클래스에는 `B2.this` 라는 것이 없고, 그것이 같은 회차의 Case3(`v2 = 100;` 컴파일 오류)의 이유다. 필기가 그 이유를 정확히 적었다 — 「바깥 클래스의 인스턴스 주소를 담는 B2.this 라는 인스턴스 멤버가 없다」. **이름이 안 보이는 문제가 아니라 대상이 없는 문제**라서, 층을 명시해도(`B2.v2`) 풀리지 않는다 → [[static-member]] · [[nested-class]]
- **익명 클래스의 `this` 도 자기 자신이다 — 람다와 갈리는 자리** — 같은 회차의 익명 구현 객체가 `AbstractList.this.size()` 를 쓰는 이유가 그것이다. 나중에 배우는 람다는 `this` 가 바깥을 가리키므로, **같은 코드를 람다로 옮기면 `this` 의 뜻이 조용히 바뀐다** → [[anonymous-class]]
- **`static` 을 지우는 것만으로 옮기기가 끝나지 않는다** — `compute` 를 `Score` 로 옮기면 호출부도 `compute(s1)` 에서 `s1.compute()` 로 전부 바뀐다. 필기가 「compute(s) -> s.compute();로 변경」이라 적어 둔 자리다 → [[method]]

## 함께 보는 개념

- [[static-member]] — `this` 가 있는 쪽과 없는 쪽을 가르는 선
- [[instance]] — `this` 가 가리키는 대상
- [[object-reference]] — `this` 에 담긴 것이 주소라는 것
- [[class]] — 기능을 데이터 옆으로 옮기는 단위
- [[constructor]] — `this.` 를 생략할 수 없는 대표적인 자리
- [[encapsulation]] — 옮겨 온 메서드가 필드를 지키게 되는 다음 단계
- [[method]] — 클래스 메서드와 인스턴스 메서드로 갈리는 대상
- [[parameter-and-argument]] — `this` 가 실은 그 자리라는 것
- [[polymorphism]] — 수신자 자리가 있어야 성립하는 것
- [[nested-class]] — `this` 가 둘이 되는 자리
- [[anonymous-class]] — `this` 의 뜻이 람다와 갈리는 자리
- [[field-hiding]] — `바깥클래스명.this` 뒤에 무엇을 쓰는지가 갈리는 이유
- [[variable-scope]] — `this.` 가 이름 탐색을 한 층에 고정한다는 것

## 출처

- [[2024-06-17-Day16]] — `static` 메서드에 `Calculator that` 을 매개변수로 넘겨 인스턴스의 필드를 고치던 코드를 인스턴스 메서드로 바꾸면서, 컴파일러가 `this` 레퍼런스를 만들어 자동으로 넘겨 준다는 것을 배웠다. `Score` 의 `compute(Score s)` 를 `Score` 안의 `compute()` 로 옮긴 것도 같은 이동이다
- [[2024-07-10-Day32]] — 중첩 클래스에서 **같은 구조가 한 층 위에서 반복된다.** 인스턴스 멤버 클래스로 만든 `ListIterator` 에는 자기 `this` 말고 바깥 `AbstractList` 의 주소도 들어오고, 필기가 그것을 「컴파일러: 바깥 클래스의 인스턴스 주소를 전달하는 코드로 자동 변환」이라는 주석으로 적었다 — Day16 의 `Calculator that` → `this` 이동이 `new ListIterator(this)` → `new ListIterator()` 로 다시 일어난 것이다. `바깥클래스명.this` 라는 표기와 「중첩 클래스 안에 해당 필드나 메서드가 없다면 생략 가능」이라는 규칙도 이 회차에서 나왔고, `AbstractList.this.size()` 가 괄호를 빼면 죽은 부모 필드를 읽게 되는 것이 이 표기의 함정이다
- [[2024-07-11-Day33]] — 하루 뒤 회차가 **그 「자동 변환」의 내용물을 적었다** — 「바깥 객체의 주소를 저장할 빌트인 필드 `B2 this$0;`」와 「inner 객체를 생성할 때 바깥 객체의 주소를 받는 생성자 `public X(B2 p) { this.this$0 = p; }`」이고, `B2.this.v2` 옆에 `// ---> this$0.v2` 라고 대응을 달았다. 그리고 `this` 의 유무가 **인스턴스를 만들 수 있는지**를 정하는 것을 보인다 — `static` 메서드에서는 `X obj;` 는 되고 `this.new X()` 는 컴파일 오류이며, 인스턴스 메서드에서는 `this.new X()` 와 `new X()` 가 같다. 다만 `this.new X()` 의 변환을 「예1) `new X(this)`」와 「예2) `new X(); obj.this$0 = this;`」 두 가지로 적어 두었는데 실제 결과는 예1 뿐이고, `B3` 예시의 `v1` · `this.v1` · `B3.this.v1` 세 줄은 **`this.` 가 이름 탐색을 한 층에 고정한다**는 것을 보여 준다
