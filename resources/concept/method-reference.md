---
type: concept
id: method-reference
title: 메서드 레퍼런스 (Method Reference)
aliases:
  - 메서드 레퍼런스
  - 메서드레퍼런스
  - 메소드 레퍼런스
  - 메서드 참조
  - 메소드 참조
  - method reference
  - 생성자 레퍼런스
  - 생성자 참조
  - constructor reference
  - 이중 콜론 연산자
up:
  - 2024-07-17-Day37
tags:
  - 자바
  - 문법
  - 함수형
  - 컴파일
---

# 메서드 레퍼런스 (Method Reference)

**이미 있는 메서드 하나를 그대로 함수형 인터페이스의 구현으로 쓰는 표기.** `::` 왼쪽에 그 메서드를 가진 것을, 오른쪽에 이름을 적는다. Day37 이 목적을 한 줄로 적었다 — 「메서드를 참조해서 매개변수의 정보 및 리턴 타입을 알아내 람다식을 간소화 하는 것」. **간소화가 이 문법의 전부가 아니다** — 람다는 몸통에 코드를 쓰는 문법이고 메서드 레퍼런스는 코드를 한 줄도 쓰지 않는다. 대신 **두 시그니처를 맞춰 보는 일**이 남는다 → [[lambda-expression]] · [[functional-interface]]

## 정의

```java
클래스::메서드      // 정적 메서드
레퍼런스::메서드    // 인스턴스 메서드 — 객체를 먼저 만든다
클래스::new        // 생성자
```

Day37 이 그 셋을 세 장으로 나눠 배운다. **어느 형태든 왼쪽이 아니라 오른쪽 — 정확히는 「대입받는 타입」 — 이 무엇을 골라 줄지를 정한다.**

| Day37 의 장 | 표기 | 이 코드에서 |
|---|---|---|
| 2. 스태틱 메서드 레퍼런스 | `클래스::정적메서드` | `Cal c4 = My::plus;` |
| 3. 인스턴스 메서드 레퍼런스 | `객체::인스턴스메서드` | `Interest i1 = 보통예금::year;` |
| 4. 생성자 레퍼런스 | `클래스::new` | `Factory1 f1 = Message::new;` |

성립 조건은 **추상메서드 하나와 참조된 메서드 하나의 시그니처를 맞춰 보는 것**이고, Day37 의 「인스턴스 메서드 레퍼런스 구현」 절이 그 규칙 셋을 가장 정확하게 적었다.

| 축 | 규칙 | 방향 |
|---|---|---|
| 개수 | 추상메서드의 매개변수 개수와 같아야 한다 | 같음 |
| 매개변수 타입 | 참조된 메서드 쪽이 **더 넓어도 된다** | 추상메서드 → 참조된 메서드 |
| 반환 타입 | 참조된 메서드 쪽이 **더 좁아야 한다** | 참조된 메서드 → 추상메서드 |

방향이 반대인 것이 헷갈리는 자리인데 이유는 하나다 — **값이 흐르는 방향이 반대**다. 인자는 추상메서드를 통해 들어와 참조된 메서드로 넘어가고(그래서 받는 쪽이 넓어야 한다), 반환값은 참조된 메서드에서 나와 추상메서드의 반환형으로 나간다(그래서 나가는 쪽이 좁아야 한다). Day37 은 이것을 「매개변수 타입보다 큰 범위」·「리턴값보다 작은 범위」로 적었다 → [[type-promotion]] · [[type-casting]]

반환 타입 쪽을 Day37 이 여섯 개 인터페이스로 하나씩 확인해 뒀다. `int plus(int,int)` 를 참조할 때다.

| 추상메서드의 반환형 | 결과 | 무엇이 일어나는가 |
|---|---|---|
| `double` · `float` | OK | 넓히기 변환 |
| `short` | 컴파일 오류 | 좁히기는 자동으로 안 된다 |
| `void` | OK | **변환이 아니다** — 반환값을 버린다 |
| `Object` | OK | 박싱(`int`→`Integer`) 후 참조 넓히기 → [[autoboxing]] · [[wrapper-class]] |
| `String` | 컴파일 오류 | `Integer` 와 상속 관계가 없다 |

## 사용 예시

**Day37 의 첫 장은 하루 전 회차의 사다리에 네 번째 칸을 붙인다.** 같은 `Cal` 을 로컬 클래스 → 익명 클래스 → 람다 → 메서드 레퍼런스로 네 번 구현한다.

```java
static class My{
    public static int plus(int a, int b){
        return a + b;
    }
}

interface Cal{
    int compute(int x, int y);
}
```

```java
class CalPlus implements Cal{                    // 1. 일반클래스
    @Override
    public int compute(int x, int y){
        return My.plus(x,y);
    }
}
Cal c1 = new CalPlus();

Cal c2 = new Cal(){                              // 2. 익명클래스
    @Override
    public int compute(int x, int y){
        return My.plus(x,y);
    }
};

Cal c3 = (x, y) -> My.plus(x,y);                 // 3. 람다
Cal c4 = My::plus;                               // 4. 메서드 레퍼런스
```

**네 칸이 지운 것이 차례로 다르다.** 익명 클래스가 클래스 이름을, 람다가 「어느 메서드를 채우는지」를 지웠다면(→ [[anonymous-class]]) 메서드 레퍼런스는 **매개변수 이름과 호출문 자체**를 지운다. `c3` 의 `(x, y)` 는 받아서 그대로 `My.plus` 에 넘기기만 하는 이름이고, 그 껍데기가 없어진 것이 `c4` 다.

**Day37 은 그 껍데기가 없어진 뒤에도 값이 남는 자리를 세 개 만든다.** 셋 다 공통점이 하나 있다 — `My`·`Calculator`·`Message` 중 **어느 것도 인터페이스를 `implements` 하지 않았다.**

정적 메서드 쪽은 계산기 하나를 네 가지 인터페이스 구현으로 만든다.

```java
static class MyCalculator {
  public static int plus(int a, int b) { return a + b; }
  public static int minus(int a, int b) { return a - b; }
  public static int multiple(int a, int b) { return a * b; }
  public static int divide(int a, int b) { return a / b; }
  public static int power(int a) { return a * 2; }
}
interface Calculator {
  int compute(int a, int b);
}

//인터페이스의 매개변수 (int,int)
// -> 메서드 레퍼런스의 매개변수 (int,int)
Calculator c01 = MyCalculator::plus;      //OK
Calculator c02 = MyCalculator::minus;     //OK
Calculator c03 = MyCalculator::multiple;  //OK
Calculator c04 = MyCalculator::divide;    //OK
//Calculator c05 = MyCalculator::power;   //NG
```

**`power` 가 이 예제의 핵심이다** — 하는 일이 이상해서 안 되는 것이 아니라 **매개변수가 하나**라서 안 된다. 나머지 넷과 반환형·접근 지정자·클래스가 모두 같으므로 걸리는 축이 개수 하나로 좁혀진다(Day37 의 원본 코드는 이 다섯 메서드가 모두 중괄호를 잃어 실제로는 실행되지 않는다 — 아래 「경계와 오해」).

인스턴스 쪽은 **하나의 객체에서 세 개의 구현을 꺼낸다.**

```java
static class Calculator {
  double rate;
  public Calculator(double rate) {this.rate = rate;}
  public double year(int money) {return money * rate / 100;}
  public double month(int money) {return money * rate / 100 / 12;}
  public double day(int money) {return money * rate / 100 / 365;}
  public double bonus() {return 100000;}
}

static interface Interest {double compute(int money);}

Calculator 보통예금 = new Calculator(0.5);

// 인터페이스 레퍼런스 = 객체::인스턴스매서드
Interest i1 = 보통예금::year;
// 람다 문법으로 표현하면:
//    Interest i1 = money -> 보통예금.year(money);
System.out.printf("년 이자: %.1f\n", i1.compute(10_0000_0000));

i1 = 보통예금::month;
i1 = 보통예금::day;
```

**`rate` 가 어디 사는지가 정적 형태와 갈리는 자리다.** `My::plus` 는 들고 갈 상태가 없지만 `보통예금::year` 는 **`보통예금` 이라는 객체를 함께 잡아서** 나간다 — `i1.compute(...)` 를 부르는 코드는 이율이 0.5 라는 것을 모르고, 그것은 `Interest` 인터페이스에도 적혀 있지 않다. 하루 전 회차의 `Factory.create6(rate)` 가 람다로 `rate` 를 붙잡아 나가던 것과 **같은 일을 객체로 하는 것**이다 → [[variable-scope]] · [[object-reference]]

`bonus()` 는 선언되어 있으나 쓰이지 않는다 — `power` 와 같은 자리의 반례다. `double bonus()` 는 매개변수가 없으므로 `double compute(int)` 를 채울 수 없고, **반환형만 맞는 것으로는 안 된다**는 것을 보이려던 것이다.

생성자 쪽이 Day37 의 결론이다.

```java
static class Message {
  String name;
  public Message() { this.name = "이름없음"; }
  public Message(String name) { this.name = name; }
  public void print() {
    System.out.printf("%s님 반갑습니다!\n", name);
  }
}

static interface Factory1 { Message get(); }
static interface Factory2 { Message get(String name); }

Factory1 f1 = Message::new;
Message m1 = f1.get();
m1.print(); //이름없음님 반갑습니다!

Factory2 f2 = Message::new;
Message m2 = f2.get("홍");
m2.print(); //홍님 반갑습니다!
```

**`Message::new` 라는 똑같은 다섯 글자가 두 번 나오는데 서로 다른 생성자를 부른다.** 오른쪽만 보면 어느 것인지 알 수 없다 — `Factory1` 이냐 `Factory2` 냐가 정한다. Day37 이 이 자리에 빈 항목 두 개를 남기고 설명을 적지 않았는데(원본에 `<li></li>` 가 둘 비어 있다), 채워야 할 내용이 바로 그것이다 → [[constructor]]

## 왜 중요한가

**「이 인터페이스를 구현한다」가 클래스 선언에서 대입문으로 내려온다.** `MyCalculator` 에도 `Calculator`(계산기 클래스) 에도 `Message` 에도 `implements` 가 없다. 그런데 `Cal`·`Interest`·`Factory1`·`Factory2` 의 구현체로 쓰인다. **이미 있는 클래스를, 그 클래스를 손대지 않고, 나중에 만든 인터페이스에 끼워 넣을 수 있게 된다** — 남이 만든 라이브러리에도 통하고, 같은 메서드를 서로 모르는 인터페이스 여럿에 동시에 끼워도 된다. 상속·구현으로는 열리지 않던 문이다 → [[interface]] · [[polymorphism]]

**함수 하나를 만들 때 새 코드가 아니라 이름이 온다.** `(x, y) -> My.plus(x,y)` 에는 `x`·`y` 라는 **새로 지은 이름 두 개**와 호출문 하나가 있다. `My::plus` 에는 없다. 인자를 순서 바꿔 넘기거나(`My.plus(y,x)`) 한쪽을 빼먹는 실수가 **쓸 자리 자체가 없어져** 사라진다 — 짧아진 것보다 이쪽이 크다.

**컴파일러가 검사하는 것이 「몸통」에서 「시그니처 두 개」로 바뀐다.** 그래서 오류가 나는 자리도 바뀐다. 람다는 몸통 안의 문장에서 걸리지만 메서드 레퍼런스는 **대입문 한 줄**에서 걸린다 — `MyCalculator::power` 가 그 예다. 컴파일 오류의 메시지가 「이 메서드는 이 인터페이스에 맞지 않는다」가 되고, 무엇이 안 맞는지는 위의 표 세 줄 안에 반드시 들어 있다 → [[compilation]] · [[parameter-and-argument]]

**생성자가 값이 된다.** `Message::new` 는 「메시지를 만드는 방법」을 변수에 담아 넘긴다. 하루 전 회차는 같은 일을 하려고 `class Factory` 를 만들고 `static InterestCalculator create6(double rate)` 를 여섯 번 오버로딩했다 — **팩토리라는 클래스가 필요했던 자리가 표기 하나로 줄어든다.** 그리고 만드는 쪽이 어떤 클래스인지 몰라도 되므로, 「무엇을 만들지」를 밖에서 주입하는 길이 열린다 → [[constructor]] · [[dispatch-table]] · [[singleton-pattern]]

## 경계와 오해

- **메서드 레퍼런스 ≠ 메서드 호출** — `My::plus` 는 `plus` 를 부르지 않는다. **부를 수 있는 객체를 하나 만든다.** `::` 와 `.` 이 나란히 보여서 겹쳐 읽히는데, `My.plus(100,200)` 은 그 자리에서 `300` 이 되고 `My::plus` 는 `Cal` 타입의 인스턴스가 된다. Day37 의 코드가 그 차이를 두 줄로 보여 준다 — `Cal c4 = My::plus;` 다음 줄에야 `c4.compute(100,200)` 이 있다. **인수를 적을 자리가 없다는 것**이 문법으로 드러난 표시다 → [[lambda-expression]] · [[instance]]
- **`::` 오른쪽에는 괄호도 인수도 오지 않는다 — 그래서 오버로딩이 있으면 표기가 같아진다** — `Message::new` 가 두 번 나와 서로 다른 생성자를 부르는 것이 그 결과다. 어느 것인지는 **대입받는 함수형 인터페이스**가 정하고, 후보가 하나로 좁혀지지 않으면 컴파일 오류다(`Factory1`·`Factory2` 를 둘 다 받는 자리에 `Message::new` 를 쓰면 그렇게 된다). 「메서드를 가리킨다」로 읽으면 **하나를 가리키는 게 아니라 후보 집합을 가리키고 왼쪽에서 하나가 고른다**는 것이 안 보인다 → [[constructor]] · [[method]]
- **「추상메서드의 매개변수와 동일해야」와 「추상메서드의 매개변수 타입보다 큰 범위」는 Day37 안에서 서로 어긋난다** — 앞은 스태틱 장(§3 「스태틱 메서드 레퍼런스 특징」), 뒤는 인스턴스 장(「인스턴스 메서드 레퍼런스 구현」)이고 **뒤가 맞다.** 규칙은 형태마다 다르지 않다. 「동일」로 외우면 `void print(Object o)` 를 `interface P { void p(String s); }` 에 끼우는 것(`out::print` 류)이 왜 되는지 설명되지 않는다. 스태틱 장이 「동일」로 적힌 것은 그 장의 예제(`int plus(int,int)` ↔ `int compute(int,int)`)가 마침 정확히 같았기 때문이고, **개수만이 「동일」이어야 하는 축**이다.
- **`int` → `void` 는 변환이 아니다** — 표에서 유일하게 성질이 다른 줄이다. `void compute(int,int)` 에 `int plus(int,int)` 를 끼우면 `300` 은 계산되고 **버려진다.** 그래서 「추상메서드의 반환값을 반환 할 수 있는 메서드만 가능하다」는 Day37 의 문장이 이 줄을 설명하지 못한다 — `void` 로 반환할 수 있는 값은 없다. 그리고 **반대 방향은 절대 안 된다**: 반환형이 있는 추상메서드에 `void` 메서드를 끼우는 것은 언제나 컴파일 오류이고, Day37 의 표는 한쪽 방향만 시험했다. 「값을 버리는 것은 되고 값을 만들어 내는 것은 안 된다」가 이 비대칭의 이유다 → [[expression-vs-statement]]
- **컴파일 결과는 익명 클래스가 아니다 — Day37 의 「원리」 절이 사실과 다르다** — 필기는 「컴파일 단계에서 My::plus는 익명 클래스로 전환된다」로 적고 `class $1 implements Cal { … } Cal c4 = new $1();` 를 그려 뒀다. **실제 `javac` 는 그런 클래스를 만들지 않는다** — `invokedynamic` 한 개를 심고, 구현 클래스는 실행 중에 `LambdaMetafactory` 가 만들어 낸다. 확인은 쉽다: 익명 클래스로 쓰면 `Test$1.class` 파일이 **생기고**, `My::plus` 로 쓰면 **생기지 않는다.** 결과가 셋 갈린다 — ① 클래스 파일 개수가 늘지 않는다, ② `new` 가 없으므로 **매번 새 객체라는 보장이 없다**(상태를 잡지 않는 레퍼런스는 같은 인스턴스가 재사용될 수 있다), ③ 예외가 나면 스택 트레이스가 `$1` 이 아니라 `Test$$Lambda$1`·`lambda$main$0` 류로 찍혀 **소스에 없는 이름**이 나온다. 「익명 클래스로 바뀐다」는 **뜻을 설명하는 모형으로는 맞고 구현으로는 틀리다** — 사다리를 네 칸으로 배웠기 때문에 마지막 칸이 두 번째 칸으로 되돌아가는 것처럼 읽힌 자리다 → [[anonymous-class]] · [[bytecode]] · [[class-file-format]] · [[compilation]]
- **`::` 의 「메서드 레퍼런스」와 상수 풀의 「메서드 참조」는 다른 것이다** — 클래스 파일 안의 `CONSTANT_Methodref`(`0a`)는 **모든** 메서드 호출이 쓰는 항목이고 자바 8 이전부터 있었다. `::` 는 자바 8 문법이다. 한국어로는 둘 다 「메서드 참조」로 번역되어 겹치는데, 이 노트의 것은 **식**이고 그쪽은 **상수 풀 항목**이다 → [[constant-pool]]
- **`객체::메서드` 는 그 객체를 「지금」 잡는다 — 람다로 옮기면 시점이 달라질 수 있다** — Day37 이 `Interest i1 = 보통예금::year;` 옆에 `money -> 보통예금.year(money)` 를 같은 것으로 적어 뒀는데, 지역변수에 대해서는 맞다(포획된 지역변수는 바꿀 수 없으므로 차이가 안 드러난다). **필드나 배열 원소를 왼쪽에 두면 갈린다** — `this.cal::year` 는 그 줄에서 `this.cal` 을 읽어 붙잡고, `money -> this.cal.year(money)` 는 **부를 때마다** 다시 읽는다. 사이에 `cal` 이 다른 객체로 바뀌면 두 코드의 답이 달라진다 → [[object-reference]] · [[immutability]]
- **`null` 이면 만드는 순간 터진다** — 위 항목의 짝이고 실무에서 더 자주 걸린다. `보통예금` 이 `null` 일 때 `보통예금::year` 는 **그 대입문에서** `NullPointerException` 을 낸다. `money -> 보통예금.year(money)` 는 대입은 조용히 통과하고 **`compute()` 를 부를 때** 터진다. 예외가 나는 줄이 다르므로 스택 트레이스를 읽고 찾아가는 자리도 다르다 → [[exception-handling]]
- **Day37 은 네 형태 중 세 개만 다룬다 — 빠진 것이 가장 자주 쓰이는 쪽이다** — 「인스턴스 메서드는 객체를 생성하여 레퍼런스를 만들고」라고 적혀 있어 객체가 반드시 필요한 것처럼 읽히는데, `String::toUpperCase` 처럼 **타입 이름에 인스턴스 메서드를 붙이는 형태**가 따로 있다. 이때는 **첫 번째 인자가 수신자가 되므로 매개변수 개수가 하나 늘어난다** — `Function<String,String>` 의 추상메서드는 인자 하나이고 `toUpperCase()` 는 인자가 없다. Day37 의 「추상매서드의 매개변수의 개수와 인스턴스 매서드의 개수는 동일」은 **객체를 왼쪽에 둔 형태에서만** 맞는 규칙이고, 이 형태에서는 「하나 적다」가 맞다. `super::메서드` 와 `int[]::new` 도 이 회차에 없다.
- **`My::plus` 는 `plus` 가 `static` 이라서 되는 것이 아니라 「왼쪽이 타입인지 객체인지」로 갈린다** — 왼쪽에 타입 이름을 쓸 수 있는 것이 정적 메서드의 성질이지만, 위 항목의 형태 때문에 **`클래스::메서드` 를 보고 정적 메서드라고 단정할 수 없다.** 그리고 같은 클래스에 이름이 같은 정적 메서드와 인스턴스 메서드가 있으면 그 표기 자체가 모호해져 컴파일 오류다 → [[static-member]]
- **원본 코드가 컴파일되지 않는 자리가 넷이고, 그중 두 개는 예제의 논점을 가린다** — ① §3 「특징」의 `MyCalculator` 다섯 메서드가 전부 `public static int plus(int a, int b) return a + b;` 로 **중괄호를 잃었다**(`return` 은 문장이라 몸통 `{}` 없이 놓일 수 없다). 다섯 줄 모두 컴파일 오류이므로 **`c01`~`c04` 가 OK 라는 것도 `c05` 가 NG 라는 것도 확인되지 않는다** — 보이려던 대비 전체가 앞단에서 막힌다. ② 「구현」 절의 익명클래스 판이 `Cal c2 = new Cal{` 로 **괄호를 잃었다** — `new Cal(){` 이어야 한다. 사다리 두 번째 칸이 안 도는 것이고, 하루 전 회차의 익명 클래스 예제가 다른 이유(중복 선언)로 죽어 있던 것에 이어 **같은 칸이 이틀 연속 실행되지 않았다.** ③·④ `Cal c4 = My::plus` 와 `return My.plus(x,y)` 에 세미콜론이 없다 → [[anonymous-class]]
- **「원리」 절의 첫 코드 블록은 `Cal c4 = Plus::Cal` 이다 — 왼쪽과 오른쪽이 둘 다 틀렸다** — 클래스는 `My`, 메서드는 `plus`, 인터페이스는 `Cal` 인데 `Plus` 라는 타입도 `Cal` 이라는 멤버도 없다. 바로 다음 줄의 설명이 「My::plus는 …」이고 그 아래 코드도 `Cal c4 = My::plus` 이므로 **이 한 줄만 어긋난 것**이고, 「인터페이스 이름과 메서드 이름을 `::` 양쪽에 적는 것」이라는 오해가 그 순간 남아 있었을 가능성을 보여 준다. `::` 왼쪽은 **인터페이스가 아니라 구현을 가진 쪽**이다.
- **네 칸 사다리는 「좋아지는 순서」가 아니다** — 메서드 레퍼런스로 쓸 수 있는 것은 **몸통이 딱 한 번의 호출인 경우**뿐이다. `(x, y) -> My.plus(x,y) + 1` 도, 인수 순서를 바꾸는 `(x, y) -> My.plus(y,x)` 도 `::` 로 쓸 수 없다. Day37 의 예제들이 전부 인수를 그대로 넘기기만 하므로 그 제약이 보이지 않고, **네 번째 칸이 항상 도달 가능한 것처럼** 읽힌다. 사다리의 다른 칸들과 다르게 이 칸은 **조건이 붙는다** → [[lambda-expression]]
- **`Cal`·`Calculator`·`Interest`·`Factory1`·`Factory2` 는 전부 함수형 인터페이스인데 `@FunctionalInterface` 가 하나도 없다** — 하루 전 회차에서 `Player` 하나에만 붙였던 것과 같은 상태다. 애노테이션이 조건이 아니라는 것이 다시 확인되고, 동시에 **메서드 레퍼런스도 추상메서드가 하나일 때만 성립한다** — 둘이면 어느 것에 맞춰야 할지 정할 수 없다 → [[functional-interface]] · [[annotation]]

## 함께 보는 개념

- [[lambda-expression]] — 사다리의 한 칸 아래, 몸통을 직접 쓰는 쪽
- [[functional-interface]] — 어느 메서드가 끼워질 수 있는지를 정하는 타입
- [[anonymous-class]] — Day37 이 컴파일 결과라고 적은 것, 실제로는 갈리는 쪽
- [[functional-programming]] — 동작을 값으로 넘기는 방향
- [[constructor]] — `::new` 가 가리키는 것
- [[method]] — 오버로딩 후보 중 하나가 골라지는 규칙을 공유하는 쪽
- [[static-member]] — `클래스::메서드` 의 왼쪽에 타입 이름을 쓸 수 있게 하는 성질
- [[type-promotion]] — 매개변수·반환형이 넓어질 수 있는 근거
- [[autoboxing]] — `int` → `Object` 를 통과시키는 단계
- [[compilation]] — 어느 것이 골라지는지가 정해지는 시점
- [[bytecode]] — `invokedynamic` 이 들어가는 곳
- [[constant-pool]] — 같은 한국어로 번역되는 다른 것
- [[exception-handling]] — `null` 수신자가 터지는 시점이 갈리는 자리
- [[object-reference]] — 바운드 레퍼런스가 붙잡는 것
- [[variable-scope]] — 상태를 들고 나가는 성질
- [[dispatch-table]] — 「만드는 방법」을 값으로 등록하게 되는 자리
- [[interface]] — `implements` 없이 구현체가 되는 대상

## 출처

- [[2024-07-17-Day37]] — 「메서드를 참조해서 매개변수의 정보 및 리턴 타입을 알아내 람다식을 간소화」로 목적을 세우고 **스태틱 · 인스턴스 · 생성자** 세 형태를 각각 한 장으로 배웠다. 하루 전 회차의 로컬 클래스 → 익명 클래스 → 람다 사다리에 **네 번째 칸**을 붙여 `Cal c4 = My::plus` 로 닫고, `MyCalculator` 의 다섯 메서드로 **매개변수 개수**가 걸리는 축임을(`power` 만 NG) 보이고, 여섯 개 인터페이스로 **반환형 호환**을 하나씩 시험했다(`double`·`float`·`void`·`Object` OK / `short`·`String` 오류). 인스턴스 장은 `보통예금::year`·`::month`·`::day` 로 **한 객체에서 세 구현을 꺼내고** 시그니처 규칙 셋(개수 동일 · 매개변수는 넓게 · 반환은 좁게)을 가장 정확하게 적었는데, **스태틱 장의 「매개변수와 동일해야」와 어긋난다.** 「컴파일 단계에서 My::plus는 익명 클래스로 전환된다 / `class $1 implements Cal`」는 **뜻의 모형으로는 맞고 구현으로는 틀리다**(실제는 `invokedynamic` + `LambdaMetafactory`). 원본 코드는 넷이 컴파일되지 않는다 — 「특징」 절의 `MyCalculator` 다섯 메서드가 중괄호를 잃어 **OK/NG 대비 전체가 확인되지 않고**, 익명클래스 판이 `new Cal{` 로 괄호를 잃었고, 세미콜론이 두 곳 없으며, 「원리」 절 첫 블록은 `Cal c4 = Plus::Cal` 로 양쪽이 다 어긋나 있다. 생성자 장은 **`Factory1 f1 = Message::new` 와 `Factory2 f2 = Message::new` 로 같은 표기가 다른 생성자를 고르는 것**을 코드로 보여 주면서 설명 자리를 빈 항목 둘로 남겨 두었고, `bonus()` 와 `power()` 는 선언만 되고 왜 못 끼워지는지 적히지 않았다. `타입::인스턴스메서드`(수신자가 첫 인자가 되는 형태) · `super::메서드` · `int[]::new` 와 `@FunctionalInterface` 는 이 회차에 없다
