---
type: concept
id: observer-pattern
title: 옵저버 패턴 (Observer Pattern)
aliases:
  - 옵저버 패턴
  - 옵저버
  - observer
  - observer pattern
  - 관찰자 패턴
  - 감시자 패턴
up:
  - 2024-07-26-Day44
  - 2024-08-06-Day51
  - 2025-02-19-Day32
tags:
  - 설계
  - 디자인패턴
  - 객체지향
  - 이벤트
---

# 옵저버 패턴 (Observer Pattern)

**상태를 가진 객체 하나가 자기를 보고 있는 객체들의 목록을 들고, 상태가 바뀔 때 그 목록을 돌며 알리는 것.** Day44 의 두 줄이 정의 전부다 — 「한 객체의 상태가 바뀌면 그 객체에 의존하는 다른 객체에게 연락이 가고 자동으로 내용이 갱신되는 방식」·「일대다 의존성(one to many)을 기반으로 주제객체의 상태를 옵저버 객체에게 알린다」. 성립시키는 것은 **알리는 쪽이 받는 쪽의 클래스 이름을 모른다**는 한 가지다.

## 정의

역할이 둘, 그 둘을 잇는 약속이 둘이다. Day44 가 만든 네 타입이 그대로 대응한다.

| 역할 | Day44 의 코드 | 갖는 것 |
|---|---|---|
| Subject (주제) | `interface Subject` | 등록·삭제·알림 세 메서드 선언 |
| ConcreteSubject | `WeatherData` | 상태(`Weather`) + `List<Observer>` |
| Observer | `interface Observer` | `update(Weather)` 하나 |
| ConcreteObserver | `CurrentConditionsDisplay` | 받은 상태로 자기 일을 한다 |

Subject 쪽 약속이 셋인 것이 우연이 아니다 — **목록을 관리하는 일(등록·삭제)과 목록을 쓰는 일(알림)** 이 나뉘어 있다.

```java
public interface Subject {
  public void registerObserver(Observer observer);
  public void removeObserver(Observer observer);
  public void notifyObservers();
}
```

받는 쪽은 메서드 하나다.

```java
public interface Observer {
  public void update(Weather weather);
}
```

**두 약속이 서로를 가리키는 방향이 이 패턴의 전부다.** `Subject` 의 메서드가 `Observer` 를 인자로 받고, `notifyObservers()` 는 그 목록을 돌며 `update()` 를 부른다 — **약속을 쓰는 쪽이 그 약속을 만든 쪽**이다. Day29~32 에서 인터페이스를 「내가 부를 것의 이름을 하나로 줄이는 장치」로 배웠다면 여기서 축이 하나 늘어난다 — 부르는 방향이 뒤집혔다 → [[interface]] · [[polymorphism]]

### 알림의 사슬 — 바깥에서 부르는 것은 첫 줄 하나다

```java
  public void measurementsChanged() {
    notifyObservers();
  }

  public void setMeasurements(Weather weather) {
    this.weather = weather;
    measurementsChanged();
  }
```

`setMeasurements` → `measurementsChanged` → `notifyObservers` → `observer.update(weather)` → `display()`. 다섯 단계인데 `App` 이 부른 것은 첫 줄뿐이고, **「자동으로 내용이 갱신되는」의 실체가 이 사슬**이다.

가운데 `measurementsChanged` 가 낀 것도 자리가 있다 — **「값이 바뀌었다」와 「알려라」를 갈라 놓은 지점**이다. 센서 값이 초당 열 번 들어와도 알림은 한 번만 보내고 싶다면 손댈 곳이 여기 하나다.

### 세 번째 인터페이스는 패턴의 역할이 아니다

```java
public interface DisplyElement {
  public void display();
}
```

Day44 는 이것을 「Subject구현체에서 사용할 display interface」라 적었는데, **`display()` 를 부르는 것은 Subject 가 아니라 옵저버 자신의 `update()` 안**이다.

```java
  @Override
  public void update(Weather weather) {
    this.weather = weather;
    display();
  }
```

즉 「알림을 받는 일」과 「화면에 찍는 일」을 두 메서드로 나눈 것이고, Subject 는 이 타입을 모른다. **패턴의 구성 요소가 아니라 이 예제의 도메인**이다 → [[cohesion]] · [[interface]]

## 사용 예시

ConcreteSubject 는 목록과 상태를 함께 든다.

```java
public class WeatherData implements Subject {
  private List<Observer> obsevers;
  private Weather weather;

  @Override
  public void registerObserver(Observer observer) {
    obsevers.add(observer);
  }

  @Override
  public void notifyObservers() {
    for (Observer observer : obsevers) {
      observer.update(weather);
    }
  }
```

**`List<Observer>` 라는 필드 선언 한 줄이 「일대다」다.** 관계의 수가 클래스 개수나 필드 개수가 아니라 **컬렉션의 길이**로 표현되므로, 화면이 0개든 10개든 `WeatherData` 의 코드는 같다 → [[generics]] · [[polymorphism]]

ConcreteObserver 는 **생성자에서 스스로 등록한다.**

```java
public class CurrentConditionsDisplay implements Observer, DisplyElement {
  private Weather weather;
  private WeatherData weatherData;

  public CurrentConditionsDisplay(WeatherData weatherData) {
    this.weatherData = weatherData;
    weatherData.registerObserver(this);
  }
```

`new` 하는 것만으로 연결이 끝나므로 `App` 에 등록 한 줄이 따로 없다. **편한 만큼 대가가 셋 붙는데** 아래 「경계와 오해」의 구체 타입 의존·`this` 유출·해제 없음이 그것이다 → [[constructor]] · [[this-reference]]

쓰는 쪽은 조립 세 줄과 값 한 줄이다.

```java
    Weather weather = new Weather();
    WeatherData weatherData = new WeatherData(weather);
    CurrentConditionsDisplay currentConditionsDisplay = new CurrentConditionsDisplay(weatherData);

    weatherData.setMeasurements(new Weather(36, 50, 50));
```

**마지막 한 줄만이 실행이고, 화면을 찍으라고 시키는 코드는 없다.** `currentConditionsDisplay` 라는 변수는 만든 뒤 한 번도 쓰이지 않는데 — 참조를 이미 Subject 가 들고 있으므로 — 그것이 이 패턴이 도는 증거다. 다만 **쓰이지 않는 변수가 정상인 코드**라는 것이 나중에 이 줄을 「지워도 되는 줄」로 오해하게 만든다 → [[variable-scope]] · [[object-reference]]

## 왜 중요한가

**화면을 하나 더하는 일이 파일 하나로 끝난다.** 새 옵저버 클래스를 만들고 `new` 하면 되고, `Subject`·`Observer`·`WeatherData`·기존 화면 중 아무것도 열지 않는다. 반대로 `WeatherData` 가 화면들을 직접 알고 있었다면 화면이 늘 때마다 필드와 호출 줄이 늘어 **상태를 가진 클래스를 계속 고치게** 된다 → [[open-closed-principle]] · [[coupling]]

**「누가 언제 물어볼까」가 사라진다.** 옵저버 없이 같은 일을 하려면 화면 쪽이 주기적으로 `weatherData.getWeather()` 를 확인해야 하고, 그러면 간격을 정하는 문제(짧으면 낭비, 길면 늦음)가 생긴다. **값이 바뀐 시점을 아는 쪽은 상태를 가진 객체뿐**이므로 알림을 그쪽에서 시작하는 것이 이 패턴이 고른 방향이다.

**연결의 수와 조합이 실행 시점에 정해진다.** 등록·삭제가 메서드이므로 프로그램이 도는 중에 붙였다 뗄 수 있다. 이틀 앞 회차의 데코레이터가 「겹을 실행 시점에 조립」한 것과 같은 종류의 이득이고, 이쪽은 **겹이 아니라 갈래**를 실행 시점에 정한다 → [[decorator-pattern]]

## 경계와 오해

- **DB 트리거는 「옵저버」인가 — 11일 뒤 Day51 이 그렇게 적었다** — MySQL 의 DDL 을 배우면서 트리거를 「특정 조건에서 자동으로 호출되는 함수」·「SQL 실행 전/후」·「OOP 디자인 패턴에서 옵저버에 해당한다」로 적어 두었다. **닮은 것은 방향 하나다** — 값을 바꾼 쪽이 누가 보고 있는지 모르고, 아는 쪽(DB 엔진)이 알린다. **다른 것이 셋인데 그 셋이 이 패턴에서 배운 문제들과 정확히 대응한다.** ① 등록이 코드가 아니라 **스키마에 박혀 있어** `registerObserver(this)` 같은 줄이 어디에도 없다 — 그래서 코드를 읽어도 실행되는 지점이 보이지 않는다(위의 「알림의 사슬」이 소스에서 사라진 형태다). ② Subject 가 애플리케이션 밖이라 **목록을 볼 수도 지울 수도 없다** — `removeObserver` 에 해당하는 것이 DDL(`drop trigger`)이다. ③ 트리거는 **원래 작업과 같은 트랜잭션에서 동기로 실행**되므로, 아래 「한 옵저버가 예외를 던지면」 항목이 여기서는 **`insert` 자체가 롤백되는 것**으로 나타난다 — 화면 하나가 깨진 것이 데이터가 안 들어가는 일이 된다 → [[ddl]] · [[exception-handling]]
- **옵저버 패턴 ≠ 발행-구독(Pub/Sub)** — 둘 다 「일대다 알림」이라 같은 것으로 읽히는데 **가운데에 무엇이 있는지가 다르다.** 옵저버는 Subject 가 목록을 **직접** 들고, 같은 스레드에서 `update()` 를 함수 호출로 부른다 — `notifyObservers()` 가 반환할 때는 모든 옵저버의 `display()` 가 이미 끝나 있다. Pub/Sub 은 브로커(토픽·큐)가 끼어 발행자와 구독자가 서로의 참조를 갖지 않고 대개 비동기다. 구별하는 표시는 **`registerObserver(this)` 처럼 상대를 인자로 넘기는 코드가 있는가**이고, 그것이 있으면 두 객체는 서로를 안다. 그래서 Day44 의 구조에서는 **옵저버 하나가 느리면 `setMeasurements` 를 부른 쪽이 그만큼 느려진다.**
- **「일대다 의존성」의 화살표와 호출의 화살표가 반대다** — 필기가 「그 객체에 **의존하는** 다른 객체에게 연락이 가고」로 적은 것이 정확한데, 그래서 헷갈린다. **의존은 옵저버 → Subject** 방향이고(화면이 기상 데이터를 필요로 한다), **호출은 Subject → 옵저버** 방향이다. 「일대다」의 1은 Subject 지만 의존의 화살표를 세면 다 → 1 이다. 이 두 방향이 어긋나 있는 것이 이 패턴이 사는 이유 그 자체다 — **필요한 쪽이 묻지 않고, 아는 쪽이 알린다** → [[dependency-inversion-principle]] · [[coupling]]
- **`update(Weather)` 는 푸시(push)다 — 그리고 이 선택이 널리 알려진 원형보다 낫다** — 상태를 인자로 밀어 넣는 것이 push, 옵저버가 `weatherData.getTemp()` 로 당겨 오는 것이 pull 이다. 이 예제의 원형(Head First Design Patterns 의 기상 스테이션)은 `update(float temp, float humidity, float pressure)` 로 값을 **낱개로** 밀어서, 측정 항목이 하나 늘면 그 값을 쓰지 않는 옵저버까지 시그니처가 바뀐다 — Day31 이 `execute()` 를 `execute(Stack)` 으로 바꾸며 구현 넷을 다 고친 것과 같은 자리다. Day44 는 `Weather` 객체 하나로 묶어 그 파급을 `Weather` 안에 가둔다. **약속의 크기를 재면 이쪽이 작다** → [[interface-segregation-principle]] · [[parameter-and-argument]]
- **밀어 넣은 `Weather` 하나를 옵저버 전부가 공유한다** — `notifyObservers()` 가 같은 인스턴스의 참조를 반복문마다 넘기고, 각 옵저버가 `this.weather = weather` 로 그것을 보관한다. 화면이 셋이면 세 필드가 **같은 객체**를 가리키므로 하나가 그 안을 바꾸면 나머지 화면의 값도 바뀐다. `Weather` 가 불변이면 문제가 안 되는데 그 클래스의 코드가 필기에 없어 **막는 것이 아무것도 없다.** Day30 이 회원 목록을 `getUserList()` 로 그대로 넘겨 두 명령이 같은 인스턴스를 만지게 된 것과 같은 형태이고, push 모델을 쓰는 대가가 여기 있다 → [[object-reference]] · [[immutability]] · [[defensive-copy]]
- **`WeatherData` 의 생성자가 받은 인자를 버린다 — 원본 코드의 실제 버그다** — `this.weather = new Weather();` 라 적혀 있어 매개변수 `weather` 는 **어디에도 쓰이지 않는다.** `App` 이 `new WeatherData(weather)` 로 넘긴 객체가 사라지는데 **출력은 정상**이다 — 바로 다음 줄의 `setMeasurements(new Weather(36, 50, 50))` 가 그 필드를 덮어쓰기 때문이다. 드러나는 경로가 셋이다. (1) 등록 시점에 현재 상태를 한 번 밀어 주도록 고치면 옵저버 전부가 **빈 `Weather`** 를 받는다. (2) `setMeasurements` 없이 `measurementsChanged()` 만 부르면 같다. (3) 그리고 이 한 줄 때문에 `Weather` 는 **인자 없는 생성자를 손으로 선언해 둬야** 한다 — `new Weather(36, 50, 50)` 가 존재하므로 기본 생성자는 자동으로 만들어지지 않는다. **버린 인자가 없는 생성자를 요구하는** 모양이고, 잘못된 초기값이 우연히 덮여서 안 보인다 → [[constructor]] · [[default-initialization]] · [[parameter-and-argument]]
- **`display()` 는 첫 알림 전에 부르면 `NullPointerException` 이다 — 그리고 위의 버그가 이것을 가리고 있다** — `CurrentConditionsDisplay.weather` 는 생성자에서 초기화되지 않으므로 `null` 이다. `display()` 는 `public` 이고 `DisplyElement` 가 존재하는 이유가 「밖에서 다시 그리게 하는 것」인데, 첫 `update()` 전에 부르면 `weather.getTemp()` 에서 터진다. Day44 의 `App` 은 `setMeasurements` 를 부르기 때문에 우연히 안 걸리고, **두 줄의 순서만 바꾸면 걸린다.** 정석적인 해법은 `registerObserver` 안에서 현재 상태를 한 번 `update` 해 주는 것인데 — **그렇게 고치는 순간 위의 「생성자가 인자를 버린다」가 드러난다.** 두 결함이 서로를 덮고 있어서 어느 하나만 고치면 다른 하나가 나타난다 → [[default-initialization]] · [[exception-handling]]
- **`removeObserver` 를 만들었고 아무도 부르지 않는다 — 옵저버는 Subject 가 사는 동안 죽지 못한다** — `List<Observer>` 가 강한 참조를 들고 있으므로, 화면을 「닫아도」 목록에 남아 계속 `update()` 를 받고 회수 대상도 아니다. **등록을 옵저버 자기 생성자에서 한 것과 짝이 되는 문제다** — 등록은 자동인데 해제는 자동이 아니고, 해제할 책임이 누구인지 코드에 적힌 곳이 없다. 「lapsed listener」라 불리는 누수의 교과서 형태이며, 약속에 `removeObserver` 를 넣어 둔 것이 그 자리를 아는 표시이자 안 쓴 표시다 → [[garbage-collection]] · [[object-reference]]
- **옵저버가 `update()` 안에서 자기를 지우면 `ConcurrentModificationException` 이다** — `for (Observer observer : obsevers)` 는 향상된 for 문이므로 내부적으로 [[iterator-pattern]] 을 쓰고, 순회 중에 `obsevers.remove(...)` 가 일어나면 다음 반복에서 예외가 난다. **`removeObserver` 를 약속에 넣은 순간 이 경로가 생긴다** — 「한 번만 받고 빠지는 옵저버」가 가장 자연스러운 사용법인데 그것이 정확히 이 예외다. 목록의 복사본을 돌거나 알림이 끝난 뒤 지우게 미루면 막힌다 → [[exception-handling]] · [[defensive-copy]]
- **한 옵저버가 예외를 던지면 뒤에 등록된 옵저버는 알림을 놓친다** — `notifyObservers()` 는 `update()` 를 그대로 부르므로 예외가 반복문을 끊고 `setMeasurements` 를 부른 쪽까지 올라간다. 그러면 **화면 하나가 깨진 것이 「상태를 바꾸는 일」의 실패로 나타난다.** 「일대다」에는 순서가 없다고 생각하기 쉬운데 `List` 이므로 **등록 순서가 곧 알림 순서**이고, 예외·성능·출력 순서가 전부 그 순서에 딸려 온다 → [[exception-handling]]
- **`CurrentConditionsDisplay` 는 `WeatherData` 를 안다 — 결합이 한 방향만 풀렸다** — 필드 타입이 `Subject` 가 아니라 구체 클래스 `WeatherData` 다. Subject 는 옵저버의 클래스 이름을 모르게 되었지만(패턴이 산 것) **옵저버는 Subject 의 클래스 이름을 안다.** `Subject weatherData` 로 받았다면 어떤 주제에든 붙는 화면이 되는데, 지금은 기상 데이터 전용이다. Day29 의 「인터페이스를 썼다 ≠ 결합이 낮아졌다」가 **방향만 뒤집혀 되살아난 자리**이고, 인터페이스를 두 개 만들어 놓고 하나를 타입으로 안 쓴 것이라 Day30 의 상태와도 겹친다 → [[coupling]] · [[dependency-inversion-principle]]
- **생성자에서 `registerObserver(this)` 를 부르는 것은 다 만들어지지 않은 객체를 남에게 건네는 일이다** — Day44 의 코드에서는 등록만 하고 끝나므로 무사하지만, `registerObserver` 가 현재 상태를 바로 밀어 주게 바뀌면 **생성자가 끝나기 전에 `update()` → `display()` 가 실행된다.** 이 클래스를 상속한 자식이 있다면 그 자식의 필드는 아직 기본값이다. 「연결이 `new` 한 번으로 끝난다」의 대가이고, 밖에서 `weatherData.registerObserver(display)` 로 한 줄 더 쓰는 형태에는 이 문제가 없다 → [[this-reference]] · [[constructor]] · [[default-initialization]]
- **`measurementsChanged()` 가 `public` 이라 상태가 안 바뀌었는데 알림이 갈 수 있다** — 밖에서 아무 때나 「지금 값으로 다시 알려라」를 시킬 수 있다. 옵저버가 「알림이 왔다 = 값이 바뀌었다」로 믿고 있으면 그 가정이 조용히 깨지고, 값을 비교해 무언가를 세는 옵저버는 같은 값을 두 번 세게 된다. 알림을 시작하는 자리를 **상태를 바꾸는 메서드 안**으로만 두는 것이 이 문제를 없애는 방법이다 → [[access-modifier]] · [[encapsulation]]
- **`obsevers` 와 `DisplyElement` — 같은 종류의 오타인데 비용이 다르다** — 필드 이름 `obsevers` 는 `WeatherData` 안에서만 쓰이므로 고치면 그 파일만 바뀐다. `DisplyElement` 는 **타입 이름**이라 `implements DisplyElement` 를 쓴 모든 클래스, 그 타입으로 받는 모든 코드, import 문에 박힌다. **오타의 비용은 철자가 아니라 그 이름이 몇 파일에 퍼졌는가로 정해지고**, 그래서 타입·인터페이스·패키지 이름은 처음 한 번을 확인할 값이 있다 → [[package]]
- **출력에 개행이 없어서, 화면이 여럿이 되는 순간 한 줄로 붙는다** — `System.out.printf("현재 온도 : %f , 현재 습도 : %f", ...)` 에 `%n` 이 없다. 옵저버가 하나인 지금은 안 보이고 **이 패턴의 목적(여러 화면)을 실현하는 순간** 출력이 뒤엉킨다. `%f` 가 `36.000000` 으로 찍는 것은 이틀 전 Day42 가 가격을 `100.000000원` 으로 찍은 것과 같은 자리다 → [[format-string]] · [[newline-character]]
- **`java.util.Observer`·`Observable` 을 쓰지 않고 손으로 만든 것이 지금 기준으로 맞다** — 표준 라이브러리에 같은 이름이 있었지만 Java 9 에서 deprecated 됐다. `Observable` 이 **인터페이스가 아니라 클래스**라 Subject 가 그것을 상속해야 했고(Java 의 단일 상속을 그 자리에 써 버린다), `setChanged()` 를 부르지 않으면 알림이 조용히 안 가는 함정도 있었다. **패턴의 이름이 표준 API 에 있어도 그것을 쓰는 것이 정답이 아닌 예**이고, Day42 가 `java.io` 에서 데코레이터를 「알아보는」 쪽이었던 것과 반대 방향이다 → [[inheritance]] · [[interface]]
- **옵저버가 여럿일 때 알림 순서에 기대면 안 된다 — 그런데 코드는 기댈 수 있게 생겼다** — `List` 이므로 등록 순서대로 불리는 것이 사실이고, 그래서 「A 화면이 먼저 갱신된 뒤 B 화면이 그 결과를 읽는다」 같은 코드가 실제로 돌아간다. 하지만 그것은 **약속에 없는 성질**이다 — `Subject` 인터페이스는 순서를 말하지 않고, 구현을 `Set` 이나 비동기로 바꾸면 그날 깨진다. [[coupling]] 이 Day29 에서 세운 「이름을 아는 것보다 순서를 아는 것이 더 강한 결합이다」가 이 패턴에서 가장 걸리기 쉬운 형태다 — **문법에 안 드러나고 컴파일러가 검사하지 않는다.**

## 함께 보는 개념

- [[application-event]] — 프레임워크가 이 패턴을 기능으로 제공하는 자리

- [[interface]] — 부르는 방향이 뒤집힌 약속이 나오는 자리
- [[coupling]] — Subject 쪽만 풀린 결합을 세는 축
- [[dependency-inversion-principle]] — 옵저버가 구체 Subject 를 아는 것이 걸리는 원칙
- [[open-closed-principle]] — 화면을 더할 때 기존 파일을 열지 않는 이유
- [[polymorphism]] — 목록 하나로 여러 화면을 부르는 근거
- [[interface-segregation-principle]] — `update` 의 인자가 약속의 크기가 되는 자리
- [[iterator-pattern]] — 목록을 돌며 알리는 `for` 문의 정체
- [[command-pattern]] — 나중에 부를 객체를 담아 두는 같은 모양
- [[decorator-pattern]] — 실행 시점에 조립하는 이득이 같은 종류인 패턴
- [[garbage-collection]] — 해제하지 않은 옵저버가 죽지 못하는 이유
- [[object-reference]] — 밀어 넣은 상태 객체를 전부가 공유하는 자리
- [[immutability]] · [[defensive-copy]] — 그 공유를 막는 두 방법
- [[exception-handling]] — 한 옵저버의 실패가 알림을 끊는 자리
- [[constructor]] — 자기 등록과 버려진 인자가 함께 있는 곳
- [[default-initialization]] — `weather` 가 `null` 인 이유
- [[this-reference]] — 다 만들어지지 않은 객체를 넘기는 문법
- [[access-modifier]] — `measurementsChanged` 가 열려 있는 자리
- [[encapsulation]] — 알림을 시작할 권한을 누구에게 줄지의 결정
- [[cohesion]] — `display()` 를 `update()` 에서 떼어 낸 자리
- [[format-string]] — `%f` 로 찍은 출력
- [[generics]] — 「일대다」를 `List<Observer>` 한 줄로 적는 문법
- [[ddl]] — 같은 구조가 DB 트리거로 나타나는 자리

## 출처

- [[2025-02-19-Day32]] — **이 패턴이 프레임워크 기능으로 나온다.** 스프링의 `ApplicationEventPublisher`(주제)와 `@EventListener`(관찰자)가 그것인데, 손으로 만들 때 필요했던 **등록 목록·통지 루프가 없다** — 컨테이너가 리스너를 모아 두고 부른다. 그래서 **발행하는 쪽은 구독자 목록조차 들고 있지 않고**, 관찰자를 더하는 것이 클래스 하나를 추가하는 일이 된다 → [[application-event]]
- [[2024-07-26-Day44]] — 「한 객체의 상태가 바뀌면 그 객체에 의존하는 다른 객체에게 연락이 가고 자동으로 내용이 갱신되는 방식」·「일대다 의존성(one to many)을 기반으로」로 정의하고, `Subject`(등록·삭제·알림)·`Observer`(`update(Weather)`)·`DisplyElement`(`display()`) 세 인터페이스와 `WeatherData`·`CurrentConditionsDisplay` 구현체를 직접 만들었다. 상태 변경 한 줄(`setMeasurements`)이 `measurementsChanged` → `notifyObservers` → `update` → `display` 로 이어지는 사슬을 코드로 확인한 회차다. 다만 `WeatherData` 의 생성자가 받은 `weather` 를 버리고 `new Weather()` 를 넣는 버그가 있고(다음 줄의 `setMeasurements` 가 덮어써서 드러나지 않는다), 옵저버의 `weather` 필드는 첫 알림 전까지 `null` 이라 `display()` 를 먼저 부르면 `NullPointerException` 이다. `removeObserver` 는 만들어 놓고 부르는 곳이 없고, 옵저버가 `WeatherData` 를 구체 타입으로 들고 있어 **결합이 Subject 쪽에서만 풀렸다.** 인터페이스 이름의 오타(`DisplyElement`)와 필드 오타(`obsevers`), `%n` 없는 `printf` 도 그대로 남아 있다
- [[2024-08-06-Day51]] — 이 패턴을 **DB 쪽에서 다시 만난다.** MySQL 의 DDL 대상 객체를 늘어놓으며 「트리거(trigger=listener)」를 「특정 조건에서 자동으로 호출되는 함수」·「특정 조건? SQL 실행 전/후 등」·「OOP 디자인 패턴에서 옵저버에 해당한다」 세 줄로 적었다. 이 대응을 스스로 적어 둔 것이 값이고, 트리거의 실제 문법(`create trigger`)이나 예제는 나오지 않아 **이름과 대응만 남은 상태**다
