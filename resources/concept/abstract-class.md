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
  - 2024-06-26-Day23
  - 2024-07-01-Day26
  - 2024-07-03-Day28
  - 2024-07-08-Day30
  - 2024-07-24-Day42
  - 2024-08-05-Day48
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

### 문법을 배우기 닷새 전에 실습에서 먼저 썼다

**인터페이스 회차의 실습이 추상 클래스를 먼저 만든다.** 필기는 이름을 「추상화클래스」로만 부르고 `abstract` 가 무엇인지는 설명하지 않는데, 만든 이유는 분명히 적어 두었다 — 「ArrayList와 LinkedList 클래스에는 size가 중복된다」.

```java
public abstract class AbstractList implements List {
  protected int size;

  @Override
  public int size() {
    return size;
  }
}
```

```java
public class ArrayList extends AbstractList { ... }
public class LinkedList extends AbstractList { ... }
```

**`Phone` 과 목적이 반대다.** `Phone` 은 자식에게 `internetSearch()` 를 **강제하려고** 비워 둔 것이고, `AbstractList` 는 두 자식이 똑같이 갖고 있던 `size` 필드와 `size()` 메서드를 **한 곳으로 올리려고** 만든 것이다. 추상 메서드가 하나도 없고 비어 있는 것은 「인터페이스에서 물려받았지만 아직 안 채운 다섯 개」다 → [[interface]]

`protected` 인 것도 결정이다. 자식이 `list[size++]`·`size--` 로 직접 만지므로 `private` 이면 안 되고, `public` 이면 밖에서 개수를 바꿀 수 있다. **「자식에게만 연다」는 접근 범위가 필요해지는 첫 자리다** → [[access-modifier]] · [[encapsulation]]

**단 그것은 Day23 시점의 코드다.** 12일 뒤 같은 클래스를 다시 만들 때 `ArrayList` 가 `private int size = 0` 을, `LinkedList` 가 `int size` 를 각자 다시 선언하고 `size()` 까지 따로 재정의한다. **`protected` 로 열어 두어도 자식이 안 쓸 수 있고**, 그러면 이 중간 층은 아무도 읽지 않는 필드 하나만 든 껍데기가 된다 → [[field-hiding]]

### 만드는 이유가 호출부에서 먼저 드러난다 — 그리고 네 단계로 자란다

**이틀 뒤 회차는 추상 클래스를 클래스 쪽에서 시작하지 않고 「부르는 쪽이 불편하다」에서 시작한다.** 정렬 클래스가 둘 있는데 하는 일이 같은데도 메서드 이름과 매개변수가 달라서, 호출부가 둘로 갈라져 있다.

```java
static void display(BubbleSort sorter, int[] values) {
  sorter.run(values);
}

static void display(QuickSort sorter, int[] values) {
  sorter.start(values, 0, values.length - 1);
}
```

**오버로딩으로 이름만 하나로 맞춘 상태다.** 필기의 진단이 정확하다 — 「2개의 메서드는 기능은 같지만, sorter.run()과 sorter.start()의 메서드명과 매개변수가 다르다」. 정렬 클래스가 하나 늘 때마다 `display` 도 하나 늘고, 그때마다 그 클래스의 메서드 이름을 새로 알아야 한다 → [[method]]

그 다음이 추상 클래스다. **부모가 이름을 정하고 자식이 자기 방식으로 그 이름을 채운다.**

```java
public abstract class Sorter {
  public void sort(int[] values) {};
}

public class QuickSort extends Sorter {
  @Override
  public void sort(int[] values) {
    start(values, 0, values.length - 1);   // 원래 이름은 그대로 두고 sort 안에서 부른다
  }
}
```

```java
Sorter sort = new BubbleSort();
display(sort, values); // OK!

Sorter sort2 = new QuickSort();
display(sor2, values); // OK!
```

`display` 가 **하나로 줄었다.** `QuickSort` 의 `start(values, 0, values.length - 1)` 처럼 매개변수가 셋이던 것도 `sort(values)` 안으로 들어가서, **호출부가 몰라도 되는 것이 되었다** → [[polymorphism]] · [[method-overriding]]

그런데 여기서 끝나지 않는다. **필기는 이 상태의 구멍을 스스로 찾아낸다.**

```java
public class MergeSort extends Sorter {

  void merge(int arr[], int l, int m, int r)
  { // 생략//
  }
}
```

`MergeSort` 는 `sort` 를 재정의하지 않았는데 **컴파일된다.** 그러면 `display(new MergeSort(), values)` 는 부모의 빈 몸통을 불러 아무 일도 하지 않는다. 필기의 「추상클래스를 사용 안하면, 상속을 받는 의미가 없다」가 그것이고, 답이 `abstract` 를 메서드에 붙이는 것이다.

```java
public abstract class Sorter {

  // 메서드를 추상 메서드로 선언하는 순간
  // => 모든 서브 클래스는 반드시 이 메서드를 구현해야 한다.
  // => 구현하지 않으면 추상 클래스가 될 수 밖에 없다.
  // => 서브 클래스에게 구현을 강제하는 효과가 있다.
  public abstract void sort(int[] values);
}
```

**「구현하지 않으면 추상 클래스가 될 수 밖에 없다」가 이레 전 실습의 `AbstractList` 를 설명한다.** 그때 `implements List` 를 해 놓고 여섯 개 중 `size()` 하나만 채웠는데도 컴파일된 이유가 이 문장이다 — 안 채운 다섯 개가 추상 메서드로 남았고, 그것을 가진 클래스는 추상 클래스일 수밖에 없다. **먼저 코드로 만나고 일주일 뒤에 규칙으로 받은 순서다** → [[interface]]

그리고 마지막 단계에서 클래스가 사라진다. 남은 것이 추상 메서드 하나뿐이니 인터페이스로 갈 수 있다.

```java
public interface Sorter {
  void sort(int[] values);
}
```

**네 단계가 「무엇을 강제할 수 있는가」 순으로 늘어서 있다.**

| 단계 | 자식이 안 채우면 | 부모가 가질 수 있는 것 |
|---|---|---|
| `display` 오버로딩 (추상화 없음) | — (부모가 없다) | — |
| 몸통 있는 메서드 + `abstract` 클래스 | **조용히 통과** | 필드·생성자·구현 |
| 추상 메서드 | 컴파일 에러 | 필드·생성자·구현 |
| 인터페이스 | 컴파일 에러 | 상수만 |

### 두 목적이 한 클래스에서 만나고, 이유가 처음으로 문장이 된다

**닷새 뒤 리팩터링 회차의 `AbstractCommand` 는 위 두 쓰임을 겹쳐 쓴다.** 세 Command 의 공통 `execute()` 를 물려주면서(중복 올리기), `processMenu`·`getMenus()` 를 추상 메서드로 두어 자식에게 강제한다(구현 강제).

| | `AbstractList` (Day23) | `Phone` (Day26) | `AbstractCommand` (Day30) |
|---|---|---|---|
| 추상 메서드 | 없다 | 있다 | **있다** |
| 물려줄 구현 | `size()` 하나 | `turnOn()` 등 | **`execute()` 골격 전체** |
| 만든 목적 | 중복을 올린다 | 구현을 강제한다 | **둘 다** |

그리고 필기가 `abstract` 를 클래스에 붙이는 이유를 처음으로 문장으로 적는다 — 「수퍼클래스를 추상클래스로 설정하여 **직접적인 클래스 사용을 막는다**」. Day26 에서는 「추상 클래스는 `new` 가 안 된다」를 문법으로 배웠고, 여기서는 **왜 막고 싶은가**가 나온다 — `AbstractCommand` 는 메뉴 처리 방법을 모르므로 그것만으로 만들어 놓으면 **아무 일도 못 하는 명령**이 된다 → [[generalization]] · [[template-method-pattern]]

### 열엿새 뒤 — 물려받은 구현을 다시 비울 수 있다

**Day42 의 데코레이터 예제에 이 노트가 아직 안 다룬 문법이 하나 있다.** 부모 `Beverage` 는 `getDescription()` 에 **구현이 있는데**, 중간 층이 그것을 다시 추상으로 선언한다.

```java
public abstract class Beverage{
  protected String description;

  public String getDescription(){    // 구현이 있다
    return description;
  }

  public abstract cost();
}
```

```java
public abstract class Decorator extends Beverage{
  protected Beverage beverage;
  public abstract String getDescription();   // 물려받은 구현을 다시 비운다
}
```

**컴파일된다 — 그리고 효과가 크다.** `Decorator` 를 상속한 모든 조미료는 `getDescription()` 을 **반드시 구현해야 한다.** 그러지 않으면 컴파일이 막히므로, 「빼먹어도 부모 것이 조용히 불린다」가 불가능해진다. Day28 의 `MergeSort` 가 재정의를 빼먹고 통과한 것과 정확히 반대 방향의 장치다.

**왜 이 자리에서 그것이 필요한가**를 보면 Day23·Day26·Day30 의 두 목적에 이어 세 번째 쓰임이 된다. `Decorator` 는 `Beverage` 를 품고 그것에 위임해야 하는데, 부모의 `getDescription()` 은 **자기 `description` 필드**를 돌려준다. `Decorator` 에는 그 필드에 값을 넣는 코드가 없으므로, 자식이 재정의를 빼먹으면 `null` 이 조용히 반환된다. **다시 추상으로 만드는 것이 「이 층에서는 그 구현이 틀렸다」는 선언**이다 → [[method-overriding]] · [[default-initialization]]

| | 물려줄 구현 | 추상 메서드 | 이 층의 뜻 |
|---|---|---|---|
| `AbstractList` (Day23) | `size()` | 없다 | 중복을 올린다 |
| `Phone` (Day26) | `turnOn()` | `internetSearch()` | 구현을 강제한다 |
| `AbstractCommand` (Day30) | `execute()` 골격 | `processMenu`·`getMenus` | 둘 다 |
| `Decorator` (Day42) | `Beverage beverage` 필드·타입 | **`getDescription()` (부모 것을 되돌림)** | **물려받은 구현을 무효화한다** |

### 12일 뒤 Day48 — 남이 만든 추상 클래스에서 이 규칙에 처음 걸린다

지금까지 추상 클래스는 전부 **직접 만든 것**이었다. 쓰레드 회차의 `java.awt.Toolkit` 은 표준 라이브러리의 추상 클래스이고, 필기가 그것을 `new` 로 만들려 한다 → [[thread]]

```java
Toolkit toolkit = Toolkit.getDefaultToolkit();   // 쓰레드를 안 쓴 첫 예제 — 맞다
Toolkit toolkit = new Toolkit();                 // 같은 코드를 run() 안으로 옮긴 뒤 — 컴파일 에러
```

**같은 노트 안에 맞는 형태와 틀린 형태가 나란히 있다.** 순차 판에서 `getDefaultToolkit()` 으로 맞게 받아 놓고, 그 코드를 쓰레드 안으로 옮겨 적으면서 **팩토리 메서드 호출이 생성자 호출로 바뀌었다.** `Toolkit` 이 추상인 이유는 소리를 내는 방법이 운영체제마다 다르기 때문이고, 그래서 자바는 **어느 구현을 줄지 자기가 골라 돌려주는 정적 메서드**만 열어 둔다 → [[platform-dependency]] · [[static-member]]

Day26 이 「추상 클래스는 `new` 가 안 된다」를 문법으로, Day30 이 「직접적인 클래스 사용을 막는다」로 이유까지 배운 규칙인데, **남의 클래스에서 걸릴 때는 「그럼 어떻게 얻나」를 따로 찾아야 한다** — 컴파일러 메시지(`Toolkit is abstract; cannot be instantiated`)는 대안을 알려 주지 않는다. **이것이 「직접 생성 금지」가 실제로 개발자에게 나타나는 모양**이다.

## 왜 중요한가

**[[polymorphism]] 을 강제한다.** 부모가 `internetSearch()` 를 추상으로 선언해 두면, 자식은 그 메서드를 반드시 갖는다. 그래서 `Phone` 타입 변수로 받아 놓고 `internetSearch()` 를 불러도 **어떤 자식이 오든 안전하다.**

일반 클래스를 상속시키면 자식이 재정의를 빼먹어도 컴파일이 통과한다 — 부모의 기본 구현이 조용히 불린다. 추상 클래스는 그 실수를 **컴파일 시점에** 막는다. 「해도 되는 것」이 아니라 「안 하면 못 넘어가는 것」으로 바뀐다.

**그리고 인터페이스가 못 하는 일을 대신한다.** 인터페이스는 필드를 물려줄 수 없어서 「둘 다 `size` 를 갖는다」는 약속만 할 수 있고 그 필드 자체를 내려보낼 수는 없다. 중복을 실제로 없애려면 **상태를 가진 중간 층**이 필요하고 그것이 추상 클래스다 — 닷새 앞선 실습이 인터페이스를 만든 다음에 추상 클래스를 하나 더 끼운 이유가 이것이다 → [[interface]]

## 경계와 오해

- **추상 클래스 ≠ 전부 추상 메서드** — 구현이 있는 메서드와 없는 메서드를 섞을 수 있다. 공통 구현은 부모가 갖고, 자식마다 달라지는 것만 추상으로 남기는 게 보통이다.
- **추상 메서드가 하나도 없어도 추상 클래스다** — `AbstractList` 에는 `abstract` 붙은 메서드가 없다. `abstract` 를 클래스에 붙이는 것만으로 「직접 생성 금지」가 되므로, **강제할 것이 없어도 「이것만으로는 쓸 수 없다」를 표시하는 데** 쓸 수 있다. 「추상 메서드를 담는 그릇」으로만 읽으면 이 쓰임이 안 보인다.
- **인터페이스를 다 채우지 않아도 컴파일된다 — 클래스가 `abstract` 일 때만** — `AbstractList implements List` 는 여섯 개 중 `size()` 하나만 구현했다. 남은 다섯은 **추상 메서드로 남은 채 자식에게 넘어가고**, 그것이 허용되는 이유는 이 클래스가 추상이라 인스턴스를 만들 수 없기 때문이다. 「`implements` 하면 전부 구현해야 한다」는 **생성 가능한 클래스**에만 걸리는 규칙이다 → [[interface]]
- **`abstract` 와 `implements` 를 함께 쓰는 것은 둘 중 하나를 고르는 것이 아니다** — 필기의 「추상화 클래스를 생성하여 인터페이스로 받고 이후 상속을 한다」가 그 형태다. 약속은 인터페이스가 갖고, 공통 상태와 공통 구현은 추상 클래스가 갖고, 자식은 다른 것만 채운다. **세 층이 각각 다른 일을 한다** → [[interface]] · [[inheritance]]
- **`abstract` 키워드를 빠뜨리면 추상 메서드가 아니다** — 본문 없이 `void internetSearch();` 라고만 쓰면 컴파일 에러다. 메서드에도 클래스에도 `abstract` 가 필요하다.
- **거꾸로 `abstract` 만 있고 반환 타입이 없어도 컴파일 에러다** — Day42 의 `public abstract cost();` 가 그 형태다. 추상 메서드는 몸통만 없고 **선언은 완전해야** 한다. 이 오타가 그럴듯해 보이는 이유는 **생성자와 모양이 겹쳐서**다 — 생성자만이 반환 타입 없이 선언되지만 그것은 이름이 클래스와 같을 때뿐이고, `cost` 는 `Beverage` 가 아니다. 그리고 이 한 줄은 빠뜨려도 되는 장식이 아니다 — 자식 `Mocha` 가 `beverage.cost() + 200` 으로 **부모 타입을 통해** 안쪽을 부르므로, 선언이 없으면 위임 사슬 전체가 안 선다 → [[method]] · [[constructor]]
- **부모의 구현을 자식에서 다시 `abstract` 로 되돌릴 수 있다** — Day42 의 `Decorator` 가 `Beverage.getDescription()` 을 다시 추상으로 선언한다. 컴파일되고, 그 아래 자식들에게는 **구현이 의무가 된다.** 「추상 → 구체」 한 방향만 있는 것으로 읽으면 이 문법이 안 보이는데, **물려받은 구현이 이 층에서는 틀린 답인 경우**(위임해야 하는데 자기 필드를 돌려주는 경우)에 필요하다. 반대로 인터페이스의 [[default-method]] 를 추상으로 되돌리는 것도 같은 문법이다.
- **다시 추상으로 만드는 것과 `final` 로 막는 것은 반대 방향의 같은 목적이다** — 둘 다 「자식이 부모 구현을 그대로 쓰는 것」을 통제한다. `abstract` 로 되돌리면 **반드시 다시 써야** 하고, `final` 로 막으면 **절대 못 바꾼다.** 그 사이에 있는 보통 메서드가 「써도 되고 안 써도 되는」 상태이며, 실수가 나는 곳도 그 가운데다 → [[template-method-pattern]]
- **`{}` 를 붙인 빈 메서드 ≠ 추상 메서드** — `public void sort(int[] values) {};` 는 **몸통이 있는 보통 메서드**다. 겉보기로는 「비워 뒀으니 자식이 채우겠지」인데, 문법으로는 「아무 일도 하지 않는 구현을 물려준다」다. **이 한 글자 차이가 「강제한다」와 「강제하지 않는다」를 가른다** — `MergeSort` 가 재정의를 빼먹고도 컴파일된 것이 그 결과이고, 필기는 그것을 「추상클래스의 한계」로 적었지만 한계는 추상 클래스에 있는 것이 아니라 **그 메서드를 `abstract` 로 선언하지 않은 데** 있다. 클래스에 붙인 `abstract` 는 생성만 막고 구현은 강제하지 않는다.
- **빈 몸통 뒤의 `;` 는 오류가 아니다** — `... {};` 의 마지막 세미콜론은 클래스 본문에 놓인 **빈 문장**이라 컴파일러가 그냥 넘긴다. 메서드 선언이 세미콜론으로 끝나는 추상 메서드 문법과 모양이 겹쳐서, 이 코드를 추상 메서드로 잘못 읽게 만드는 자리다.
- **추상 클래스가 「강제」하는 것과 인터페이스가 강제하는 것의 차이는 개수가 아니다** — 필기는 「추상클래스를 가지고 메소드사용을 강제하는데 제약이 있어, 인터페이스를 사용하게 된다」로 인터페이스가 더 강한 쪽처럼 적었지만, **추상 메서드로 선언하면 강제력은 완전히 같다.** 갈리는 것은 **부모가 상태와 구현을 가질 수 있는가**이고, 그래서 「제약이 있다」는 진단은 앞 절에서 메서드에 `abstract` 를 안 붙였던 상태에만 맞는다 → [[interface]]
- **인스턴스를 못 만들 뿐 생성자는 있다** — 자식이 `super(...)` 로 부르기 위해 존재한다. 생성자가 없다는 뜻이 아니다.
- **추상 클래스를 「얻는」 통로가 `new` 가 아닐 수 있다 — 그리고 그 통로는 매번 새 인스턴스를 주지 않는다** — `Toolkit.getDefaultToolkit()` 은 플랫폼에 맞는 자식 인스턴스를 돌려주는 정적 팩토리이고, **몇 번 불러도 같은 하나**를 돌려준다. 「`new` 가 막혔으니 만들 수 없다」가 아니라 **「만드는 쪽을 라이브러리가 쥐고 있다」**가 정확한 이해다 — 그래야 어느 구현을 줄지 라이브러리가 고를 수 있고, 그것이 `abstract` 로 생성을 막아서 얻는 것이다. 익명 클래스로 `new 추상클래스(){…}` 를 쓰는 것과는 방향이 반대다 — 그쪽은 **내가** 자식을 그 자리에서 만드는 것이다 → [[singleton-pattern]] · [[anonymous-class]]
- **추상 클래스를 만든 것 ≠ 중복이 없어진 것** — 같은 노트에서 `AbstractList` 는 자식이 `size` 를 다시 선언해 **끌어올린 필드가 죽었고**, `AbstractCommand` 는 자식에 `String menuTitle;` 선언이 남아 그 필드가 `null` 로 남았다. 부모 클래스가 존재하는 것과 자식에서 그 코드가 사라진 것은 별개이고, **확인해야 하는 쪽은 자식이다** → [[field-hiding]] · [[refactoring]]
- **「직접적인 클래스 사용을 막는다」가 규칙 준수까지 막아 주지는 않는다** — 클래스에 붙인 `abstract` 는 `new AbstractCommand()` 만 막는다. 자식이 부모의 `execute()` 를 재정의해 순서를 통째로 바꿔 버리는 것은 아무도 막지 않는다 — 그쪽을 막는 문법은 `final` 이고, 추상 클래스에는 **비워서 강제하는 자리(`abstract`)와 채워서 고정하는 자리(`final`)가 둘 다 필요**하다 → [[template-method-pattern]]
- **생성자를 못 부르게 하는 것과 인스턴스를 못 만들게 하는 것은 다른 장치다** — `abstract` 는 「이 클래스로는 만들 수 없다」이고 생성자를 `private` 으로 닫는 것은 「밖에서는 만들 수 없다」다. 뒤쪽은 자기 안에서는 여전히 `new` 가 되므로 인스턴스가 하나 존재한다. **생성자는 `abstract` 가 될 수 없다** — 몸통 없이 `private Car();` 라고 쓰면 컴파일 에러이고, 두 장치를 같은 문법으로 착각하면 나오는 코드다 → [[singleton-pattern]] · [[constructor]]

## 함께 보는 개념

- [[inheritance]] — 추상 클래스는 상속을 전제로만 쓰인다
- [[method-overriding]] — 추상 메서드 구현이 곧 오버라이딩이다
- [[polymorphism]] — 추상 클래스가 강제하려는 것
- [[interface]] — 약속만 갖는 쪽. 필드를 물려줄 수 없어서 이것이 필요해진다
- [[access-modifier]] — `protected` 로 자식에게만 여는 결정
- [[dynamic-array]] — `AbstractList` 를 상속한 한쪽
- [[linked-list]] — 상속한 다른 쪽
- [[method]] — 추상화 전에 호출부가 오버로딩으로 버티던 자리
- [[singleton-pattern]] — 생성을 막는 다른 장치
- [[generalization]] — 이 클래스를 만들게 되는 작업
- [[template-method-pattern]] — 골격과 빈 칸을 함께 둘 때의 구조
- [[field-hiding]] — 끌어올린 필드를 죽게 만드는 실수
- [[decorator-pattern]] — 물려받은 구현을 다시 비우는 이유가 나온 자리
- [[default-method]] — 인터페이스 쪽에서 같은 「구현을 되돌리기」가 걸리는 곳
- [[thread]] — 표준 라이브러리의 추상 클래스를 `new` 로 만들려 한 자리
- [[platform-dependency]] — `Toolkit` 이 추상 클래스인 이유

## 출처

- [[2024-06-26-Day23]] — 인터페이스 실습에서 `abstract` 라는 문법을 배우기 전에 `AbstractList` 를 먼저 만들었다. 「ArrayList와 LinkedList 클래스에는 size가 중복된다」가 만든 이유고, `implements List` 로 약속을 받아 `size()` 하나만 채운 뒤 나머지를 자식에게 넘긴다. 추상 메서드가 하나도 없는 추상 클래스이며 `protected int size` 를 자식이 직접 만진다
- [[2024-07-01-Day26]] — `Phone`/`SmartPhone` 예제로 추상 클래스의 생성 제한과 자식의 구현 의무를 배웠다. 닷새 전 실습의 `AbstractList` 와 목적이 반대다 — 그쪽은 중복을 올리려고 만들었고 이쪽은 구현을 강제하려고 비워 둔다
- [[2024-07-03-Day28]] — 추상 클래스를 **호출부의 불편에서 출발해** 네 단계로 키웠다. `display(BubbleSort)`/`display(QuickSort)` 오버로딩 → 몸통이 빈 `sort` 를 가진 `abstract class Sorter` → 재정의를 빼먹은 `MergeSort` 가 조용히 통과하는 것을 발견 → `public abstract void sort(...)` → 인터페이스. 「구현하지 않으면 추상 클래스가 될 수 밖에 없다」는 주석이 이레 전 `AbstractList` 가 인터페이스를 다 안 채우고도 컴파일된 이유를 뒤늦게 설명해 준다. 「추상클래스의 한계」로 적은 것은 실은 그 메서드에 `abstract` 를 붙이지 않은 결과다
- [[2024-07-08-Day30]] — 추상 클래스를 **하루에 두 개** 만들며 두 쓰임을 겹쳤다. `AbstractList` 는 Day23 것을 다시 만든 것이고, `AbstractCommand` 는 세 Command 의 공통 `execute()` 를 물려주면서 `processMenu`·`getMenus` 를 추상 메서드로 강제한다. 「수퍼클래스를 추상클래스로 설정하여 직접적인 클래스 사용을 막는다」로 **클래스에 `abstract` 를 붙이는 이유가 처음 문장이 된 자리**다. 동시에 두 부모 모두 자식이 같은 이름의 필드를 다시 선언해(`size`·`menuTitle`) **끌어올린 것이 죽었다** — 추상 클래스가 존재하는 것과 중복이 없어진 것이 다르다는 증거다
- [[2024-08-05-Day48]] — 쓰레드 예제에서 `java.awt.Toolkit`(표준 라이브러리의 추상 클래스)을 `new Toolkit()` 으로 만들려 해 컴파일되지 않는다. **지금까지 추상 클래스는 모두 직접 만든 것이었고, 남이 만든 추상 클래스에서 「직접 생성 금지」에 걸린 첫 사례**다. 같은 노트의 쓰레드를 안 쓴 첫 예제는 `Toolkit.getDefaultToolkit()` 으로 맞게 받아 놓았으므로, **그 코드를 `run()` 안으로 옮겨 적으면서 팩토리 호출이 생성자 호출로 바뀐 것**이다. `Toolkit` 이 추상인 이유(소리를 내는 방법이 플랫폼마다 다르다)와 그래서 얻는 통로가 정적 팩토리라는 것은 이 회차에 나오지 않는다
- [[2024-07-24-Day42]] — 데코레이터 예제의 `Beverage`(Component)와 `Decorator`(중간 층)가 **추상 클래스의 세 번째 쓰임**을 보여 준다 — `Decorator extends Beverage` 가 부모에 구현이 있는 `getDescription()` 을 **다시 `abstract` 로 선언해** 자식에게 재구현을 강제한다. 물려받은 구현이 이 층에서는 틀린 답(위임해야 하는데 자기 `description` 필드를 돌려준다)이기 때문이고, 필기는 이 효과를 설명하지 않고 코드로만 남겼다. 같은 코드의 `public abstract cost();` 는 **반환 타입이 빠져 컴파일되지 않으며**(의도는 `double`), 반환 타입 없는 선언이 생성자 문법과 겹쳐 그럴듯해 보이는 자리다. 인터페이스가 아니라 추상 클래스를 Component 로 쓴 덕에 `protected String description` 과 `getDescription()` 의 기본 구현을 물려줄 수 있었다는 점에서 「인터페이스가 못 하는 일」의 예가 하나 더 붙는다
