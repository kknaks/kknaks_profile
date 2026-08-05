---
type: concept
id: decorator-pattern
title: 데코레이터 패턴 (Decorator Pattern)
aliases:
  - 데코레이터 패턴
  - 데코레이터
  - decorator
  - decorator pattern
  - 장식자 패턴
  - 감싸기
up:
  - 2024-07-19-Day39
  - 2024-07-23-Day41
  - 2024-07-24-Day42
tags:
  - 설계
  - 디자인패턴
  - 객체지향
  - 입출력
---

# 데코레이터 패턴 (Decorator Pattern)

**같은 타입의 객체를 하나 품고, 그 앞뒤에 자기 일을 끼워 넣어 내보내는 것.** Day39 의 한 줄이 정의 전부다 — 「객체에 동적으로 새로운 행동(기능)을 추가할 수 있는 패턴이다. 주로 상속 대신 사용되며, 원래 객체를 수정하지 않고도 행동을 확장할 수 있다」. 껍데기가 **안쪽과 같은 타입**이기 때문에 몇 겹을 씌워도 부르는 쪽 코드가 변하지 않는다.

## 정의

역할이 넷이고 Day39 가 그 넷을 그대로 적었다.

| 역할 | Day39 의 설명 | 이 실습에서 |
|---|---|---|
| **Component** | 「구체적인 객체들과 데코레이터들이 구현할 공통 메서드를 정의」 | `interface Printer { void print(String s); }` |
| **ConcreteComponent** | 「실제로 기능을 구현하는 클래스」 | `ContentPrinter` — 내용만 찍는다 |
| **Decorator** | 「컴포넌트 객체를 래핑(wrapping)하여 동적으로 행동을 추가」하는 **추상 클래스** | `PrinterDecorator` — `protected Printer origin` |
| **ConcreteDecorator** | 「추가된 행동을 정의」 | `HeaderPrinter` · `FooterPrinter` · `SignPrinter` |

성립시키는 한 줄은 `PrinterDecorator implements Printer` 이면서 안에 `Printer origin` 을 갖는 것이다. **구현하는 타입과 품는 타입이 같다** — 그래서 데코레이터가 다른 데코레이터를 품을 수 있고 겹이 쌓인다.

```text
Printer (Component)
 ├── ContentPrinter      (ConcreteComponent)  print() → 내용만 찍는다
 └── PrinterDecorator    (Decorator, abstract)  origin: Printer   ← 다시 Component 다
      ├── HeaderPrinter  print() → 머릿말 찍고 origin.print()
      ├── FooterPrinter  print() → origin.print() 하고 꼬릿말
      └── SignPrinter    print() → origin.print() 하고 서명
```

`PrinterDecorator` 는 `Printer` 를 구현한다고 선언하고도 **`print()` 를 구현하지 않는다.** `abstract` 이기 때문에 컴파일되고, 그래서 「필드와 생성자만 물려주고 동작은 자식이 채운다」가 된다 → [[abstract-class]] · [[interface]]

### 상속으로 조합하면 클래스가 폭발한다

Day39 는 패턴을 보여 주기 전에 **패턴이 없을 때의 비용**을 먼저 센다 — 기능 3가지를 상속으로 조합하면 「순서에 상관 없는 경우 8가지」, 「순서가 상관있는 경우 27가지」의 클래스가 필요하고, 「각클래스마다 생성자의 매개변수도 다양해서 일관성도 저해된다」.

핵심은 숫자가 아니라 **곱셈으로 늘어난다**는 것이다. 상속은 조합을 **컴파일 시점에** 고정하므로 「머릿말+꼬릿말」과 「꼬릿말+머릿말」이 각각 클래스여야 하고, 기능이 넷째로 늘면 그 전부에 다시 곱해진다 → [[inheritance]]

## 사용 예시

Component 는 아무것도 모른다 — 자기 일만 한다.

```java
public interface Printer {
  void print(String s);
}

public class ContentPrinter implements Printer {
  @Override
  public void print(String s) {
    System.out.println(s);
  }
}
```

Decorator 는 **같은 타입을 받아 필드에 두는 생성자**가 전부다.

```java
public abstract class PrinterDecorator implements Printer {
  protected Printer origin;

  public PrinterDecorator(Printer printer) {
    this.origin = printer;
  }
}
```

ConcreteDecorator 는 **`origin.print(s)` 를 어디에 놓는지로 기능이 갈린다.**

```java
public class HeaderPrinter extends PrinterDecorator {
  String header;

  public HeaderPrinter(Printer printer, String header) {
    super(printer);
    this.header = header;
  }

  @Override
  public void print(String s) {
    System.out.println(header);      // 앞에 끼운다
    origin.print(s);
  }
}

public class FooterPrinter extends PrinterDecorator {
  String footer;

  public FooterPrinter(Printer printer, String footer) {
    super(printer);
    this.footer = footer;
  }

  @Override
  public void print(String s) {
    origin.print(s);
    System.out.println(footer);      // 뒤에 끼운다
  }
}
```

**두 클래스의 차이가 두 줄의 순서뿐이다.** 위임 호출 `origin.print(s)` 를 기준으로 앞에 쓰면 머리, 뒤에 쓰면 꼬리가 되고, 양쪽에 쓰면 감싸는 것이 된다 → [[method-overriding]] · [[polymorphism]]

쓰는 쪽은 **필요한 만큼 겹쳐서 만든다.**

```java
    ContentPrinter printer3 = new ContentPrinter();
    HeaderPrinter printer3H = new HeaderPrinter(printer3, "머릿말");
    FooterPrinter printer3F = new FooterPrinter(printer3H, "꼬릿말");
    printer3F.print("안녕하세요");
```

`printer3F.print()` 한 번이 **세 객체를 타고 흐른다** — `FooterPrinter` → `HeaderPrinter` → `ContentPrinter` 로 들어가며 머릿말이 찍히고, 돌아 나오며 꼬릿말이 찍힌다. **들어갈 때 할 일과 나올 때 할 일이 한 메서드 안에서 갈리는 것**이 이 패턴을 읽는 요령이다.

그리고 이 노트의 뒤쪽 절이 **같은 구조를 표준 라이브러리에서 다시 만난다.**

```java
    try (FileInputStream in0 = new FileInputStream("user.data");
        DataInputStream in = new DataInputStream(in0)) {
```

```java
    try (Scanner in = new Scanner(new FileReader("user.csv"))) {
```

Day39 가 「Data I/O Stream처럼 데코레이터 패턴을 통해 File I/O Stream으로 내보낼 수 있다」로 스스로 이어 붙인 자리다. **`FileInputStream` 이 ConcreteComponent, `DataInputStream` 이 Decorator** 이고, 패턴을 배운 값이 「내가 짜는 것」보다 **「Java 입출력이 왜 저렇게 겹쳐 있는지 읽히는 것」**에서 먼저 나온다 → [[data-io-stream]] · [[io-stream]]

### 나흘 뒤 — 같은 겹을 상속으로 읽으면 어떻게 되는지가 나온다

Day41 은 같은 두 껍데기(`DataOutputStream`·`BufferedInputStream`)를 다루면서 관계를 **상속**이라 적는다.

> 「Data I/O stream은 File I/O stream을 상속받아 사용한다」
> 「BufferedFileInputStream의 read() 메서드는 FileInputStream에서 상속 받은 메서드를 이용하여」

**두 문장이 같은 착오를 두 章에서 반복한다.** 그리고 그 모형이 코드의 모양까지 바꿔 놓는다.

| Day39 (감싸기) | Day41 (상속으로 읽은 결과) |
|---|---|
| `new DataOutputStream(out0)` | `new DataFileOutputStream("temp/test4_2.data")` |
| `new BufferedInputStream(in0)` | `new BufferedFileInputStream("temp/jls.pdf")` |

**오른쪽 두 클래스는 존재하지 않는다.** 이름에 `File` 이 들어가고 **생성자가 파일 이름을 받는** 것이 우연이 아니다 — 「`FileOutputStream` 을 상속했다」면 부모의 생성자를 물려받았을 것이고 이름도 그렇게 붙는 것이 자연스럽다. **틀린 관계 모형이 그럴듯한 API 를 상상하게 만든 자리**이고, Day39 에서 이미 옳은 형태를 손으로 써 본 뒤에도 그렇게 됐다.

**그리고 이 착오가 왜 결과를 바꾸는지가 이 패턴의 논거 그대로다** — 상속이라면 「파일용 Data 스트림」·「소켓용 Data 스트림」·「메모리용 Data 스트림」이 각각 클래스여야 한다. 즉 **Day39 의 「기능 3가지를 상속으로 조합하면 8가지·27가지」와 같은 곱셈**이 표준 라이브러리에서 되살아나는 것이고, 실제 `java.io` 가 `DataOutputStream` **하나**로 끝내는 이유가 감싸기이기 때문이다. **패턴을 잘못 읽으면 라이브러리의 크기까지 다르게 상상하게 된다** → [[inheritance]] · [[buffered-stream]]

### 그 다음 날 — 커피로 다시 만들면서 모형이 제자리로 온다

Day42 는 같은 패턴을 처음부터 다시 만든다. 이번 Component 는 인터페이스가 아니라 **추상 클래스**다.

```java
public abstract class Beverage{
  protected String description;

  public String getDescription(){
    return description;
  }

  public abstract cost();
}
```

```java
public abstract class Decorator extends Beverage{
  protected Beverage beverage;
  public abstract String getDescription();
}
```

**`extends Beverage` 이면서 `Beverage beverage` 를 품는 것** — Day39 의 `PrinterDecorator implements Printer` + `protected Printer origin` 과 정확히 같은 한 줄이다. 상속으로 만들든 인터페이스로 만들든 **성립 조건은 「구현하는 타입 = 품는 타입」 하나**이고, 이 예제가 그것을 두 번째 문법으로 보여 준다 → [[abstract-class]] · [[interface]]

ConcreteDecorator 에서는 두 메서드가 **각자 자기 사슬을 만든다.**

```java
public class Mocha extends Decorator{
  public Mocha(Beverage beverage){
    this.beverage = beverage;
  }

  public String getDescription(){
    return beverage.getDescription + ", Mocha";
  }

  public double cost(){
    return beverage.cost() + 200;
  }

}
```

`getDescription()` 은 문자열을 이어 붙이고 `cost()` 는 숫자를 더한다 — **겹이 하나 늘 때마다 두 사슬이 함께 한 칸 길어진다.** Day39 의 `print()` 는 사슬이 하나였고(출력), 여기서 처음 둘이 된다. 커피 예제가 흔히 쓰이는 이유가 이것이다 — 「이름」과 「가격」이 같은 겹을 타고 따로 흐르는 것이 눈에 보인다.

쓰는 쪽은 변수를 다시 대입한다.

```java
    Beverage cafemocha = new Espresso();
    cafemocha = new Mocha(cafemocha);
```

**이 재대입은 오류가 아니라 이 패턴의 관용구다** — 오른쪽에서 옛 값을 읽어 감싼 뒤 그 결과를 같은 이름에 넣으므로 `Espresso` 는 `Mocha` 안에 살아 있다. 하루 앞 Day41 의 `FileWriter` 재대입은 **닫지도 않은 앞의 스트림을 이름에서 놓아 버려** 빈 파일을 남겼다 — **모양이 같고 결과가 반대**이며, 갈리는 것은 **새 객체가 옛 객체를 인자로 받았는가** 하나다. 같은 문장이 한쪽에서는 조립이고 다른 쪽에서는 유실이다 → [[object-reference]] · [[character-stream]]

그리고 Day42 의 정의 절이 이 패턴의 근거를 세 출처 중 가장 짧게 적는다 — 「상속을 사용하여 객체들을 추가하면 **컴파일 단계에서 결정이 되며** 기능이 추가 될 수록 코드가 복잡해진다」·「상속을 이용한 강결합은 유지보수 측면에서 **OCP 원칙을 위배**한다」. **Day41 이 `java.io` 의 겹을 상속으로 읽은 바로 다음 회차에 「상속은 컴파일 시점에 고정된다」가 문장으로 나온 것**이고, 같은 노트가 「I/O Stream 데코레이터 살펴보기」라는 소제목까지 세운다 → [[open-closed-principle]] · [[coupling]]

#### 비워 둔 소제목의 답

「I/O Stream 데코레이터 살펴보기」에는 **본문이 없다** — 제목만 서 있다. 채우면 이렇게 된다.

| 데코레이터 역할 | `Beverage` 예제 | `java.io` |
|---|---|---|
| Component | `Beverage`(추상) | `InputStream`(추상) |
| ConcreteComponent | `Espresso` | `FileInputStream` — 통로를 여는 것 |
| Decorator | `Decorator extends Beverage` | `FilterInputStream extends InputStream` |
| ConcreteDecorator | `Mocha` | `BufferedInputStream` · `DataInputStream` |

`FilterInputStream` 의 필드가 `protected volatile InputStream in` 이다 — **`Decorator` 의 `protected Beverage beverage` 와 같은 자리**이고, Day41 의 「Data I/O stream은 File I/O stream을 상속받아 사용한다」가 왜 틀렸는지의 답이 그 한 줄에 다 있다. 확인하는 방법도 짧다 — `DataInputStream(InputStream in)` 이라는 생성자가 「감쌀 것을 받는다」고 말하고 있으니, 상속이라면 그 자리에 파일 이름이 있어야 한다. **소제목을 세운 것까지가 「볼 것을 알아본 것」이고, 본문이 비어 있어 대조는 하지 않았다** → [[buffered-stream]] · [[data-io-stream]] · [[io-stream]]

## 왜 중요한가

**기능을 더하는 일이 새 파일 하나로 끝난다.** 「밑줄 찍기」를 더하려면 `PrinterDecorator` 를 상속한 클래스 하나를 만들면 되고, `Printer`·`ContentPrinter`·기존 데코레이터·부르는 쪽 중 아무것도 열지 않는다. 반대로 상속으로 조합했다면 새 기능이 **기존 조합 전부와 다시 곱해진다** → [[open-closed-principle]]

**조합이 실행 시점으로 내려온다.** 어떤 기능을 어떤 순서로 쓸지가 `new` 를 부르는 코드에 있으므로, 사용자 설정이나 입력에 따라 다르게 조립할 수 있다. 클래스 목록으로 미리 만들어 둘 수 없는 조합 — 같은 기능을 두 번 씌우는 것까지 — 이 가능해지는 것이 「동적으로 추가」의 실체다.

**계약이 인터페이스 하나로 유지된다.** 몇 겹을 씌워도 타입은 `Printer` 이므로 받는 쪽 시그니처가 변하지 않는다. 겹을 늘리는 것이 **호출부에 보이지 않는 변경**이 되고, 그것이 `BufferedInputStream` 을 하나 끼워 넣어 성능을 바꿀 수 있는 이유다 → [[interface]] · [[coupling]]

## 경계와 오해

- **데코레이터 ≠ 상속 — `extends` 를 쓰는데도 그렇다** — `HeaderPrinter extends PrinterDecorator` 라서 상속처럼 보이지만, **기능이 붙는 방향은 상속이 아니라 필드다.** 상속은 「무엇을 물려받았나」를 컴파일 시점에 고정하고, 데코레이터는 「무엇을 품고 있나」를 생성자 인자로 실행 시점에 정한다. 그래서 상속 계층은 조합마다 클래스가 필요하고 데코레이터는 같은 클래스로 조합이 무한하다. **`extends` 는 필드·생성자를 재사용하려고 쓴 것이고 확장의 축이 아니다** → [[inheritance]] · [[object-reference]]
- **그리고 이 구분은 나흘 뒤에 실제로 놓친다 — 패턴을 짜 보는 것과 라이브러리에서 알아보는 것이 다른 능력이다** — Day39 는 `PrinterDecorator` 를 손으로 만들고 「데코레이터 패턴을 통해」라고 표준 입출력에 스스로 이어 붙였다. 그런데 Day41 은 같은 두 껍데기를 「File I/O stream을 상속받아 사용한다」·「FileInputStream에서 상속 받은 메서드를 이용하여」로 적는다. **패턴의 정의(「주로 상속 대신 사용되며」)를 나흘 전에 정확히 옮겨 적은 사람이 같은 구조를 상속으로 읽은 것**이고, 갈리는 것은 **`extends` 가 코드에 보이는가**다 — 자기가 쓴 코드에는 `PrinterDecorator implements Printer` + `protected Printer origin` 이 눈에 있었고, `java.io` 에서는 그 안을 안 열어 보니 「A 가 B 의 기능을 쓴다」는 느낌만 남는다. **관계를 확인하는 방법은 느낌이 아니라 `extends` 절과 생성자 인자 타입**이고, `DataOutputStream(OutputStream out)` 이라는 시그니처 하나가 답을 갖고 있다 → [[inheritance]] · [[data-io-stream]] · [[buffered-stream]]
- **그 상속 모형은 하루만 서 있었다 — Day41 을 「이해가 후퇴한 상태」로 못 박으면 틀린다** — 바로 다음 회차 Day42 가 「상속을 사용하여 객체들을 추가하면 **컴파일 단계에서 결정이 되며**」·「상속을 이용한 강결합은 OCP 원칙을 위배한다」로 시작하고, 「I/O Stream 데코레이터 살펴보기」라는 소제목을 세워 그 겹을 다시 보려 한다. **Day41 의 상속 읽기는 고정된 오해가 아니라 하루짜리 흔들림**이었고, 남은 것은 다른 종류의 미완이다 — **그 소제목의 본문이 비어 있어 자기가 하루 전에 쓴 문장과 대조하지는 않았다.** 개념을 다시 정의하는 것과 전에 쓴 것을 고치는 것이 별개의 일이라는 표시다.
- **「순서가 상관있는 경우 27가지」는 3³ 이고, 실제로 세야 하는 것은 16이다** — 순서 없는 8은 맞다(부분집합 `2³`, 아무 기능도 안 쓰는 경우 포함). 순서를 세면 **서로 다른 기능을 최대 3개까지 늘어놓는 경우**이므로 `1 + 3 + 3·2 + 3·2·1 = 16` 이다. 27 은 「세 자리를 세 기능 중 하나로 채운다」 즉 **같은 기능이 중복돼도 되고 길이가 반드시 3인** 계산이다. 다만 이 착오가 결론을 약하게 만들지 않는다 — **데코레이터는 실제로 같은 기능을 두 번 씌우는 것을 허용하고, 중복을 허용하면 조합의 상한이 아예 없다.** 미리 클래스로 만들 수 없다는 논거는 16보다 이쪽이 강하다.
- **데코레이터 ≠ 컴포짓 — 둘 다 자기 타입을 품는데 품는 개수와 목적이 다르다** — [[composite-pattern]] 의 `MenuGroup` 은 `List<Menu> children` 으로 **여럿**을 품어 「부분-전체」를 만들고 부르는 쪽이 잎과 가지를 구별하지 않게 한다. `PrinterDecorator` 는 `Printer origin` 으로 **하나**를 품어 그 하나의 동작을 바꾼다. Day35 의 트리는 **구조**를 나타내고 Day39 의 겹은 **행동**을 쌓는다. 둘이 헷갈리는 이유는 코드 모양(같은 타입 필드 + 위임 호출)이 거의 같아서인데, **`List` 인지 단일 참조인지가 그 자리에서 갈리는 표시**다.
- **데코레이터 ≠ 프록시** — 모양이 같다(같은 인터페이스, 안쪽 하나를 품고 위임). 갈리는 것은 목적이다 — 프록시는 **접근을 통제하거나 대신 만들어 주려고**(지연 생성·권한·원격 호출) 끼고, 데코레이터는 **동작을 더하려고** 낀다. 코드로는 구별되지 않고 이름과 의도로만 구별되므로, 클래스 이름을 「…Decorator」로 두는 것이 문서 역할을 한다.
- **씌우는 순서가 결과를 바꾼다 — 그래서 순서도 형식의 일부다** — `HeaderPrinter(FooterPrinter(content))` 와 `FooterPrinter(HeaderPrinter(content))` 는 둘 다 컴파일되고 둘 다 머릿말·내용·꼬릿말을 찍는다. 하지만 `SignPrinter` 처럼 **위임 뒤에 찍는 것들끼리는 순서가 출력에 그대로 나타난다** — Day39 의 `printer6` 은 `HeaderPrinter(SignPrinter(content))` 라 「머릿말 → 내용 → by naknak」이 되고, 뒤집으면 서명이 머릿말보다 먼저 나온다. **「필요한 기능을 선택적으로 사용 가능하다」에는 순서를 고르는 것도 들어 있고, 잘못 고른 순서는 예외가 아니라 이상한 출력으로만 나타난다.**
- **`printer6` 은 `printer6` 을 감싸지 않는다 — 원본 코드의 오류다** — `SignPrinter printer6S = new SignPrinter(printer5, "naknak");` 이 `printer6` 대신 **`printer5` 를 감싼다.** 앞 다섯 줄의 형태(`printerN` 을 만들고 그것을 감싼다)와 어긋나고, `ContentPrinter printer6` 은 만들어져서 아무도 쓰지 않는다. **출력은 우연히 맞는다** — `ContentPrinter` 가 상태가 없고 둘 다 `System.out` 에 찍으므로 `printer5` 를 감싸도 결과가 같다. 그래서 실행으로는 절대 드러나지 않고, **감싸는 대상이 파일이나 소켓처럼 상태를 가진 것이었다면 엉뚱한 곳으로 출력된다.** 데코레이터 코드에서 가장 흔한 실수 형태 — 「무엇을 감쌌는지」가 변수 이름에만 있고 타입에는 없다 → [[object-reference]]
- **감싼 뒤에는 원래 구체 타입으로 되돌릴 수 없다** — `printer3F` 의 타입은 `FooterPrinter` 이고, 그 안의 `ContentPrinter` 에만 있는 메서드를 부를 방법이 없다(`origin` 은 `Printer` 타입이고 `protected` 다). **데코레이터는 인터페이스에 선언된 것만 통과시키는 벽**이라, 구현 클래스에 특화된 기능을 쓰던 코드는 겹을 씌우는 순간 끊긴다. `instanceof ContentPrinter` 도 거짓이 된다 → [[instanceof-operator]] · [[interface]]
- **위임을 잊으면 아무 표시 없이 기능이 사라진다** — `PrinterDecorator` 는 `print()` 를 구현하지 않으므로 **자식마다 `origin.print(s)` 를 손으로 적어야 한다.** 한 줄을 빼먹으면 컴파일도 되고 실행도 되며 **안쪽 내용만 안 찍힌다.** 위임 기본 구현(`public void print(String s) { origin.print(s); }`)을 추상 클래스에 두고 자식이 `super.print(s)` 를 부르게 하면 이 실수가 줄어드는데, Day39 의 구조는 그 자리를 비워 두었다 → [[abstract-class]] · [[method-overriding]]
- **기능이 늘면 클래스는 안 늘지만 객체는 늘어난다** — 상속의 조합 폭발을 없앤 대가로 **디버깅할 때 보는 것이 클래스 계층이 아니라 실행 중의 참조 사슬**이 된다. 스택 트레이스에 `print` 가 겹의 수만큼 쌓이고, 「지금 이 객체가 몇 겹으로 감싸져 있나」는 코드를 읽어서는 알 수 없고 조립한 자리를 찾아가야 한다. Java 입출력 오류를 읽기 어려운 이유가 이것이다.
- **`protected Printer origin` 은 캡슐화를 한 칸 연 것이다** — 자식이 `origin` 에 직접 접근하고 다른 것으로 바꿔 넣을 수도 있다. `private` + `getter` 로 두면 그 여지가 없어지는데, 데코레이터에서는 자식이 반드시 위임해야 하므로 관례적으로 `protected` 를 쓴다. **문법이 막아 주는 것과 관례로 지키는 것이 갈리는 자리** → [[access-modifier]] · [[encapsulation]]
- **Day42 의 구조는 Day39 가 비워 둔 「위임 강제」를 닫는다 — 그런데 그것을 의도로 적지는 않았다** — 위의 「위임을 잊으면 아무 표시 없이 기능이 사라진다」가 `PrinterDecorator` 의 구멍이었다. Day42 의 `Decorator` 는 `getDescription()` 을 **부모에 이미 구현이 있는데도 다시 `abstract` 로 선언**하고, `cost()` 는 `Beverage` 에서부터 추상이다. 그래서 **자식이 위임을 빼먹으면 컴파일이 막힌다** — Day39 에서는 통과했던 실수다. 다만 이 형태로 얻은 것이 하나 더 있다 — `Decorator` 가 `getDescription()` 을 추상으로 되돌리지 않았다면 자식이 안 채웠을 때 **부모의 구현이 불려 `description` 필드(`Decorator` 에서는 아무도 넣지 않는다)의 `null` 이 조용히 반환됐을 것**이다. 「비워서 강제한다」가 위임 구조에서 값을 내는 자리 → [[abstract-class]] · [[method-overriding]] · [[default-initialization]]
- **`public abstract cost();` 는 컴파일되지 않는다 — 반환 타입이 없다** — `Espresso` 가 `public double cost()` 로 구현하므로 의도는 `public abstract double cost();` 다. 반환 타입 없는 선언은 **생성자 문법**과 모양이 겹쳐 그럴듯해 보이는데, 생성자는 이름이 클래스와 같아야 하므로 `cost` 는 그것도 아니다. 그리고 이 한 줄이 없으면 **겹 전체가 안 선다** — `Mocha.cost()` 가 `beverage.cost() + 200` 으로 부모 타입의 시그니처를 통해 안쪽을 부르기 때문이다. **데코레이터에서 Component 의 메서드 선언은 「약속」이 아니라 위임의 통로 그 자체**다 → [[abstract-class]] · [[method]]
- **`beverage.getDescription` 은 호출이 아니다 — `()` 가 없고, 더 나쁜 오타가 옆에 있다** — 필드 접근으로 읽히고 `Beverage` 에 그 이름의 필드가 없어 컴파일 에러다. 문제는 **`beverage.description` 이라고 썼다면 컴파일은 됐다**는 것이다(`protected` 이고 같은 계층이다). 그 코드는 안쪽 객체의 **원본 문자열만** 읽으므로, 세 겹을 씌워도 결과가 「Espresso」 하나뿐이고 겹이 사라진다. **위임은 반드시 메서드로 해야 재귀적으로 풀린다** — 필드로 당겨오면 그 자리에서 사슬이 끊기고 예외도 안 난다 → [[access-modifier]] · [[method]]
- **「`getDescription` 이 가격을 더한다」로 적힌 자리 — 두 사슬이 한 줄에 섞였다** — 실행 절차가 「cagemocha.getDescription -> Beverage(Espresso타입).getDescription + 200(모카의 가격)」·「Beverage.getDescription -> 100(에스프레소의 가격)」이다. 문자열을 잇는 것은 `getDescription()` 이고 가격을 더하는 것은 `cost()` 인데, **두 메서드의 위임 구조가 완전히 같아서** 한쪽 이름으로 양쪽을 설명하게 된다. 「겹이 늘면 사슬도 함께 늘어난다」는 요지는 맞지만, **이 겹이 무엇을 더하는가는 메서드마다 따로 세어야 한다** — 이름에는 문구를 붙이고 값은 그대로 통과시키는 데코레이터(예: 「Tall」 사이즈 표기)도 정상이고, 그때 두 사슬의 길이가 달라진다.

## 함께 보는 개념

- [[interface]] — 겹과 안쪽이 같은 타입이게 만드는 것
- [[abstract-class]] — 필드·생성자만 물려주고 동작을 비워 두는 자리
- [[inheritance]] — 이 패턴이 대신하는 확장 방법
- [[polymorphism]] — 겹을 몇 개 씌워도 호출이 같은 이유
- [[method-overriding]] — 위임 앞뒤에 자기 일을 끼우는 문법
- [[composite-pattern]] — 같은 모양으로 여럿을 품는 쪽
- [[template-method-pattern]] — 골격을 물려주고 일부만 채우게 하는 다른 방향
- [[open-closed-principle]] — 이 패턴이 지키는 원칙
- [[coupling]] — 겹을 늘려도 호출부가 모르는 이유
- [[io-stream]] — 이 패턴으로 조립되어 있는 표준 라이브러리
- [[data-io-stream]] — 실제로 감싸는 데코레이터의 예
- [[character-stream]] — `Scanner(new FileReader(...))` 로 겹치는 쪽
- [[access-modifier]] — `protected origin` 이 여는 틈
- [[instanceof-operator]] — 겹을 씌우면 거짓이 되는 검사
- [[buffered-stream]] — 성능을 위해 나중에 끼우는 겹
- [[default-initialization]] — 위임을 안 채운 겹이 `null` 을 내보내는 이유

## 출처

- [[2024-07-19-Day39]] — 「객체에 동적으로 새로운 행동(기능)을 추가할 수 있는 패턴」으로 정의하고 Component·ConcreteComponent·Decorator·ConcreteDecorator 네 역할을 나열했다. 「사용 전」 절에서 상속으로 기능 3가지를 조합하면 순서 무관 8가지·순서 유관 27가지 클래스가 필요하고 생성자 매개변수의 일관성도 깨진다는 것을 세고(뒤쪽 숫자는 3³ 이라 어긋난다), 「사용 후」에서 `Printer` 인터페이스 · `ContentPrinter` · `PrinterDecorator`(추상, `protected Printer origin`) · `HeaderPrinter`·`FooterPrinter`·`SignPrinter` 로 구현한다. `Test01` 이 여섯 조합을 만들어 보는데 마지막 것이 `printer6` 대신 `printer5` 를 감싸는 오류가 있고 **출력이 같아 드러나지 않는다.** 같은 노트의 뒤쪽에서 `new DataInputStream(new FileInputStream(...))`·`new Scanner(new FileReader(...))` 를 쓰며 「Data I/O Stream처럼 데코레이터 패턴을 통해」로 표준 라이브러리와 스스로 이어 붙인다
- [[2024-07-23-Day41]] — 같은 두 껍데기(`DataOutputStream`·`BufferedInputStream`)를 다루면서 관계를 **상속으로 적는다** — 「Data I/O stream은 File I/O stream을 상속받아 사용한다」·「BufferedFileInputStream의 read() 메서드는 FileInputStream에서 상속 받은 메서드를 이용하여」. 나흘 전에 이 패턴의 정의(「주로 상속 대신 사용되며」)를 정확히 옮겨 적고 표준 입출력에 스스로 이어 붙였던 것과 어긋나는 자리다. 그 모형이 코드의 모양까지 바꿔 **존재하지 않는 `DataFileOutputStream`·`BufferedFileInputStream` 에 파일 이름을 넘기는** 형태가 되고(실제 생성자는 감쌀 스트림을 받는다), 그렇게 되면 「통로 종류 × 형식 종류」마다 클래스가 필요해져 **Day39 가 센 조합 폭발이 표준 라이브러리에서 되살아난다.** 자기가 짠 코드에서는 `implements` + `protected Printer origin` 이 눈에 있었고 라이브러리에서는 그것을 열어 보지 않은 차이다
- [[2024-07-24-Day42]] — 같은 패턴을 **커피 메뉴판으로 처음부터 다시 만들며 하루 만에 모형을 되돌린다.** 「객체에 추가 요소를 동적으로 더하는 기능」으로 정의하고 근거를 두 줄로 압축한다 — 「상속을 사용하여 객체들을 추가하면 컴파일 단계에서 결정이 되며 기능이 추가 될 수록 코드가 복잡해진다」·「상속을 이용한 강결합은 유지보수 측면에서 OCP 원칙을 위배한다」. 이번 Component 는 인터페이스가 아니라 추상 클래스(`Beverage`)이고 `Decorator extends Beverage` 가 `protected Beverage beverage` 를 품어 **Day39 의 `implements` + 필드와 같은 형태를 두 번째 문법으로** 보여 준다. `getDescription()`(문자열 잇기)과 `cost()`(가격 더하기)로 **사슬이 처음 둘이 되고**, `cafemocha = new Mocha(cafemocha)` 재대입이 하루 전 `FileWriter` 재대입과 모양이 같고 결과가 반대다. 코드에는 컴파일되지 않는 두 곳이 있다 — `public abstract cost();`(반환 타입 없음)와 `beverage.getDescription`(`()` 없음). 실행 절차 설명은 `getDescription` 이 가격을 더한다고 적어 두 사슬을 한 줄에 섞었고, `%f` 로 찍어 「100.000000원」이 되는 것과 구성요소 목록에 ConcreteDecorator 가 빠진 것은 짚지 않았다. **「I/O Stream 데코레이터 살펴보기」라는 소제목을 세워 놓고 본문을 비워 둔 것**이 이 회차의 미완이며, Day41 이 상속으로 읽은 그 겹을 다시 볼 자리였다
