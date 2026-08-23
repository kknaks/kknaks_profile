---
type: concept
id: object-cloning
title: 객체 복제 (clone 과 깊은 복사)
aliases:
  - 객체 복제
  - 복제
  - clone
  - Cloneable
  - 깊은 복사
  - deep copy
  - object cloning
up:
  - 2024-06-24-Day21
tags:
  - java
  - 객체지향
  - 메모리
  - 표준라이브러리
---

# 객체 복제 (clone 과 깊은 복사)

같은 내용을 가진 **새 인스턴스**를 만드는 일. [[object-class]] 의 `clone()` 이 필드를 그대로 베껴 주지만, **베끼는 것은 필드에 든 값**이라 참조 필드는 원본과 사본이 같은 것을 가리킨다.

## 정의

`clone()` 을 쓰려면 **두 가지**를 해야 한다. 하나만 해서는 안 된다.

1. `Cloneable` 을 구현한다 — 안 하면 실행 중에 `CloneNotSupportedException`
2. `clone()` 을 재정의해 접근 권한을 `public` 으로 넓힌다 — 물려받은 것은 `protected` 다

```java
static class Score implements Cloneable {
    ...
    @Override
    public Score clone() throws CloneNotSupportedException {
      // 복제를 위한 코드를 따로 작성할 필요가 없다.
      // JVM이 알아서 해준다.
      // 그냥 상속 받은 메서드를 오버라이딩하고, 접근 권한을 public 으로 확대한다.
      // 원래의 clone() 메서드를 실행한 다음에
      // 리턴 타입을 해당 클래스로 형변환 한다.
      return (Score) super.clone();
    }
  }
```

**재정의한 메서드가 복제를 하지 않는다.** 실제 복사는 `super.clone()` 이 하고, 내가 쓴 코드는 **권한을 열고 반환 타입을 되돌리는 것**뿐이다 → [[method-overriding]] · [[access-modifier]]

## 사용 예시

재정의하기 전에는 **컴파일조차 되지 않는다.**

```java
Score s1 = new Score("홍길동", 100, 100, 100);
Score s3 = s1.clone(); // 컴파일 오류!
//
// Object에서 상속 받은 clone()은 protected 이다.
// 따라서 같은 패키지에 소속된 클래스이거나 상속 받은 서브 클래스가 아니면 호출할 수 없다.
// 비록 Object의 서브 클래스라 할지라도 남의 인스턴스로 protected 멤버를 사용할 수 없다.
// 자신이 상속 받은 protected 멤버인 경우에만 접근할 수 있다.
```

`Score` 는 분명히 `Object` 의 서브클래스인데 막힌다. **`protected` 가 여는 것은 「내가 물려받은 것」이고 「남의 인스턴스의 그것」이 아니다** → [[access-modifier]]

### 참조 필드가 있으면 손으로 한 겹 더 들어가야 한다

```java
@Override
public Car clone() throws CloneNotSupportedException {
  // deep copy
  // => 포함하고 있는 객체에 대한 복제를 수행하려면 다음과 같이 
  //    개발자가 직접 포함하는 객체를 복제하는 코드를 작성해야 한다.
  // 
  Car copy = (Car) super.clone();
  copy.engine = this.engine.clone();       // 이 한 줄이 없으면 엔진을 공유한다
  return copy;
}
```

`super.clone()` 만 부르면 `copy.engine` 과 `this.engine` 에 **같은 주소**가 들어간다. 사본의 엔진을 손대면 원본의 엔진도 바뀐다 → [[object-reference]]

| | 필드가 기본 타입 | 필드가 참조 타입 |
|---|---|---|
| `super.clone()` 만 | 값이 복사된다 — 독립 | **주소가 복사된다 — 공유** |
| 원하는 것 | 그대로 충분 | 그 객체도 `clone()` 해야 한다 |

`Score` 예제가 잘 동작한 것은 필드가 `String` 하나를 빼면 전부 기본 타입이었기 때문이다 → [[data-type]]

## 왜 중요한가

**복제 코드를 안 써도 된다.** 필드가 여섯 개인 `Score` 를 손으로 베끼려면 여섯 줄을 쓰고, 필드를 하나 추가할 때 그 줄을 잊으면 조용히 안 복사된다. `super.clone()` 은 **선언된 필드 전부**를 기계적으로 베끼므로 필드가 늘어도 손댈 곳이 없다.

**그리고 「복사했다」가 두 가지 뜻이라는 것이 여기서 드러난다.** Day19 의 `toArray()` 는 배열을 새로 만들었지만 칸에 든 것은 같은 `User` 였다. `clone()` 도 기본 동작은 같은 층에서 멈춘다 — **한 겹만 새것이다.** 어디까지 새것이어야 하는지는 문법이 정해 주지 않고, 「사본을 고쳐도 원본이 안 바뀌어야 한다」를 어느 깊이까지 요구하느냐가 곧 결정이다 → [[defensive-copy]]

## 경계와 오해

- **`clone()` 재정의 ≠ 복제 구현** — 내가 쓴 코드는 권한과 반환 타입만 바꾼다. 「오버라이딩했으니 내가 복제 방식을 정했다」로 읽으면 왜 `super.clone()` 을 빼면 안 되는지 설명되지 않는다. `new Score(...)` 로 바꿔 쓰면 서브클래스에서 잘못된 타입이 나온다.
- **`implements Cloneable` 이 조용히 추가됐다** — 필기 5.1 과 5.2 의 차이는 오버라이딩 하나가 아니라 **둘**이다. `Cloneable` 이 없으면 `super.clone()` 이 `CloneNotSupportedException` 을 던지므로, 5.2 의 첫 줄이 없으면 컴파일은 되고 실행에서 터진다. 필기에 그 이유가 적혀 있지 않다 → [[exception-handling]]
- **`Cloneable` 에는 메서드가 없다** — 「구현하라」고 하는데 구현할 것이 없다. 이 인터페이스가 하는 일은 **`clone()` 을 허락한다는 표시**뿐이고, 실제 복제 코드는 `Object` 에 있다. 「인터페이스를 구현하면 메서드를 채운다」는 규칙의 예외로 보이는 자리다.
- **반환 타입을 `Score` 로 바꾼 것은 오버라이딩이 맞다** — 부모의 `clone()` 은 `Object` 를 돌려주는데 자식은 `Score` 를 돌려준다. 「선언부가 같아야 한다」는 규칙과 어긋나 보이지만, **반환 타입은 좁히는 방향이 허용된다**(공변 반환 타입). 덕분에 부르는 쪽이 `(Score)` 캐스팅을 하지 않아도 된다 → [[method-overriding]] · [[type-casting]]
- **`clone()` 은 생성자를 부르지 않는다** — `Score` 의 `sum`·`aver` 는 생성자에서 계산되는데, 복제는 그 계산을 다시 하지 않고 **이미 들어 있는 값을 베낀다.** 결과는 같아서 문제가 안 보이지만, 생성자에 검증이나 카운터 증가가 있으면 복제가 그것을 전부 건너뛴다. Day19 의 `seqNo` 발급을 생성자에 넣었다면 복제본이 번호를 못 받았을 것이다 → [[constructor]] · [[surrogate-key]]
- **깊은 복사는 자동이 아니고, 한 겹으로 끝나지도 않는다** — `copy.engine = this.engine.clone()` 을 쓰려면 `Engine` 도 `Cloneable` 이어야 하고 `clone()` 을 `public` 으로 열어야 한다. 그 `Engine` 이 또 참조 필드를 가지면 거기서도 같은 일을 해야 한다. **요구가 객체 그래프를 따라 번진다.**
- **`throws CloneNotSupportedException` 이 그대로 남아 있다** — 재정의할 때 지울 수 있었는데(오버라이딩은 예외를 줄일 수 있다) 남겨 두었으므로, **부르는 쪽마다 `try-catch` 를 써야 한다.** 절대 나지 않을 예외를 잡는 코드가 호출부마다 생기는 것이고, 이것이 자바 `clone()` 이 잘 쓰이지 않게 된 이유 중 하나다 → [[exception-handling]]
- **필기 5.3 의 `Car`·`Engine` 은 정의가 없다** — 메서드 조각만 남아 있고 클래스 선언이 잘려 있다. `engine` 필드가 어떤 타입인지, `Engine` 이 `Cloneable` 인지도 확인할 수 없다.
- **`s1.clone()` 을 막은 것이 `private` 이 아니라 `protected` 다** — Day16 의 접근 지정자 표에서 `protected` 의 「하위 클래스 내부」열이 `O` 였으므로 표만 보면 이 코드가 통과해야 한다. 표가 말하지 않은 조건이 하나 더 있었던 자리다 → [[access-modifier]]

## 함께 보는 개념

- [[defensive-copy]] — 배열 한 겹만 새로 만드는 같은 구조
- [[object-class]] — `clone()` 이 사는 곳
- [[method-overriding]] — 권한과 반환 타입을 바꾸는 방법
- [[access-modifier]] — `protected` 가 실제로 여는 범위
- [[object-reference]] — 사본의 필드에 든 것
- [[constructor]] — 복제가 건너뛰는 단계
- [[exception-handling]] — `CloneNotSupportedException` 이 걸리는 자리
- [[instance]] — 복제가 만들어 내는 것
- [[data-type]] — 필드 종류가 복제 깊이를 가르는 기준
- [[type-casting]] — `super.clone()` 의 결과를 되돌리는 일

## 출처

- [[2024-06-24-Day21]] — `Object.clone()` 이 `protected` 라 `s1.clone()` 이 컴파일 오류가 나는 것(「남의 인스턴스로 protected 멤버를 사용할 수 없다」)을 확인하고, `implements Cloneable` 과 `clone()` 오버라이딩으로 권한을 `public` 으로 넓혀 `return (Score) super.clone()` 을 쓰는 것을 배웠다. 포함한 객체까지 복제하려면 `copy.engine = this.engine.clone()` 을 직접 써야 한다는 깊은 복사도 이 자리다
