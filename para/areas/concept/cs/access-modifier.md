---
type: concept
id: access-modifier
title: 접근 지정자 (Access Modifier)
aliases:
  - 접근 지정자
  - 접근지정자
  - 접근 제어자
  - access modifier
  - public
  - protected
  - private
up:
  - 2024-06-17-Day16
  - 2024-06-18-Day17
  - 2024-06-20-Day19
  - 2024-06-24-Day21
  - 2024-07-03-Day28
  - 2024-07-05-Day29
  - 2024-07-11-Day33
tags:
  - java
  - 객체지향
  - 문법
  - 구조화
---

# 접근 지정자 (Access Modifier)

클래스와 멤버를 **어디에서 쓸 수 있는지** 정하는 키워드. 네 등급이 있고, 등급을 가르는 기준은 「같은 클래스인가 · 같은 패키지인가 · 하위 클래스인가」다.

## 정의

이 필기가 정리한 표가 그대로 규칙이다.

| 접근 지정자 | 현재 클래스 내부 | 동일 패키지 내부 | 하위 클래스 내부 | 전체적인 접근 가능 |
|---|---|---|---|---|
| `public` | O | O | O | O |
| `protected` | O | O | O | X |
| (default, 생략) | O | O | X | X |
| `private` | O | X | X | X |

세 번째 열의 「하위 클래스 내부」는 **다른 패키지에 있는 하위 클래스**를 뜻한다. 같은 패키지라면 (default) 로도 이미 보이므로, `protected` 가 (default) 보다 넓은 이유가 그 한 칸이다 → [[inheritance]]

그 한 칸에 **표에 적히지 않은 조건이 하나 더** 붙는다. 자기가 물려받은 멤버여야 하고, **같은 타입이라도 남의 인스턴스의 것은 안 된다.** Day21 의 `clone()` 이 그 자리다.

```java
Score s1 = new Score("홍길동", 100, 100, 100);
Score s3 = s1.clone(); // 컴파일 오류!
// 비록 Object의 서브 클래스라 할지라도 남의 인스턴스로 protected 멤버를 사용할 수 없다.
// 자신이 상속 받은 protected 멤버인 경우에만 접근할 수 있다.
```

**표만 보면 통과해야 하는 코드**다 — `Score` 는 `Object` 의 하위 클래스이고, 「하위 클래스 내부」열이 `O` 다. 갈리는 것은 `this.clone()` 과 `s1.clone()` 이고, 앞의 것만 「자신이 상속 받은 멤버」다 → [[object-cloning]]

**아흐레 뒤 회차가 이 조건을 규칙으로 적어 둔다** — 네 등급 목록 아래에 별표로 한 줄이 붙는다.

```text
*자식 클래스에서 상속 받아 만든 변수가 아니면 부모클래스로 생성해도 protected 접근불가
```

`clone()` 에서 컴파일 오류로 만난 것이 **표의 예외가 아니라 표에 적히지 않은 다섯 번째 조건**이라는 것을 이 줄이 확정한다. 표는 「코드가 어디 있는가」만 담고, 이 줄은 「무엇을 통해 닿는가」를 담는다 → [[inheritance]] · [[this-reference]]

멤버(필드·메서드·생성자)에는 넷 다 붙을 수 있지만, **최상위 클래스에는 `public` 과 생략 둘뿐이다.**

### 「멤버에는 넷 다」는 클래스의 멤버 이야기다

**열여드레 뒤 회차가 세 번째 경우를 더한다.** 인터페이스의 멤버에는 넷이 다 붙지 않고, **생략했을 때의 결과도 반대**다.

| 붙이는 자리 | 쓸 수 있는 것 | 생략하면 |
|---|---|---|
| 최상위 클래스 | `public` · 생략 | (default) |
| 클래스의 멤버 | 넷 다 | (default) |
| **중첩 클래스**(멤버 클래스) | **넷 다** | (default) |
| **로컬 클래스** | **하나도 없다** | (default 상당 — 그 블록 안뿐) |
| 인터페이스의 멤버 | `public` · `private`(몸통이 있을 때) | **`public`** |

```java
interface MyInterface {
  abstract void m2(); // public 이 생략된 것이다. (default) 아니다!
  //  private void m5(); // 컴파일 오류!
  //  protected void m6(); // 컴파일 오류!
}
```

필기가 「(default) 아니다!」에 느낌표를 붙인 이유가 그것이다. **같은 「아무것도 안 씀」이 한쪽에서는 가장 좁은 쪽 다음이고 다른 쪽에서는 가장 넓은 쪽**이라, 네 등급 표를 자리와 무관한 규칙으로 외우면 여기서 정반대로 읽는다 → [[interface]] · [[default-method]]

### 클래스에도 넷이 다 붙는 자리가 있다 — 그것이 멤버일 때다

**엿새 뒤 중첩 클래스 회차가 네 번째와 다섯 번째 줄을 더한다.** 첫 줄(최상위 클래스는 둘뿐)과 둘째 줄(멤버에는 넷 다)이 부딪히는 것처럼 보이는 자리인데, 중첩 클래스는 **클래스이면서 멤버**라서 둘째 줄을 따른다. 필기가 그 근거를 그대로 적었다 — 「정적 중첩클래스도 **클래스의 멤버이기 때문에** 필드나 메서드처럼 접근 제한자를 붙일수 있다」.

```java
public class StaticNestedClass {
    private static class A1 {}
    static class A2 {}          //(package-private)
    protected static class A3 {}
    public static class A4 {}
}
```

```java
public class NonStaticNestedClass {
    private class A1 {}
    class A2 {}                 //(package-private)
    protected class A3 {}
    public class A4 {}
}
```

로컬 클래스에서는 **넷이 다 막힌다.** 이유가 등급이 아니라 **이름의 유효범위**다 — 그 블록 밖에서는 이름조차 없으니 「누가 볼 수 있나」를 말할 대상이 없다. 필기의 표현이 「**로컬 변수처럼** 로컬클래스에는 접근 제한자를 붙일 수 없다」다 → [[variable-scope]] · [[nested-class]]

```java
public class NonStaticNestedClass {
    static void m1(){
        // private class A1 {}
        class A2 {}
        // protected class A3 {}
        // public class A4 {}
    }
}
```

그리고 같은 회차가 **종류마다 관례가 갈린다**고 적었다.

| 종류 | 필기가 적은 관례 | 이유로 적힌 것 |
|---|---|---|
| 정적 중첩 클래스 | (default) · `public` | 「외부에서 사용되는 경우도 많아」 |
| 인스턴스 중첩 클래스 | `private` | 「바깥 클래스의 객체가 생성되어야 쓸수 있기때문에」 |

## 사용 예시

이 필기는 `Score` 를 하위 패키지로 옮기면서 접근 지정자를 처음 만난다.

```text
기존                          변경
study/oop/clazz/              study/oop/clazz/
  Test02.java                   Test02.java
  Score.java                     vo/
                                  Score.java
```

옮긴 것뿐인데 `Test02` 에서 `Score` 가 보이지 않게 된다. 지정자를 아무것도 쓰지 않았으니 (default) 였고, 패키지가 갈렸기 때문이다.

```java
package study.oop.clazz.vo;

public class Score {          // 클래스가 public 이 아니면 다른 패키지에서 이름조차 못 쓴다
  public String name;         // 필드도 각각 열어야 한다
  public int kor;

  public Score() {}           // 생성자도 열어야 new 할 수 있다
}
```

```java
package study.oop.clazz;

import study.oop.clazz.vo.Score;    // 다른 패키지가 되어 import 가 필요해졌다
```

**클래스에 `public` 을 붙였다고 안이 열리는 것이 아니다** — 멤버는 각자의 지정자를 갖는다. 그래서 3.5 의 `Score` 는 필드마다 `public` 을 다시 붙였고, 3.6 에서 그것을 `private` 으로 되돌리며 getter/setter 를 세웠다 → [[encapsulation]]

### 프로젝트 규모가 되면 지정자가 층마다 다르게 붙는다

다음 회차에서 클래스를 `util`·`vo`·`command` 세 패키지로 가르자 같은 일이 다시 일어난다. 필기가 그 순간을 이렇게 적어 뒀다.

```text
파일을 리팩터링 하면 다음과 같이 에러가 발생 -> 접근지정자의 오류
이전에 default 로 설정이 되어 있어, 다른패키지의 파일을 참고 할 수가 없다
import 문과 public 문 사용
```

이번에는 **같은 클래스 안에서도 지정자가 갈린다.**

```java
public class UserCommand {                                  // App 이 부르므로 열린다
  private static final User[] users = new User[MAX_SIZE];   // 저장소는 닫는다
  private static int userLength = 0;

  public static void excuteUserCommand(String command) { }  // 진입점 — 열린다
  public static User findByNo(int userNo) { }               // ProjectCommand 가 쓴다 — 열린다

  private static void addUser() { }                         // 안에서만 쓴다 — 닫는다
  private static void listUser() { }
}
```

**`private` 이 붙은 것이 「감출 것」이 아니라 「밖에서 부를 일이 없는 것」이다.** `addUser` 를 열어 둘 이유가 없는 것은 `excuteUserCommand` 가 명령을 받아 알아서 고르기 때문이다 → [[crud]]

그리고 `ProjectCommand` 는 이 결정이 실습 중에 바뀐 자리를 그대로 보여 준다. 2.1 의 초안은 (default) 였고,

```java
public class ProjectCommand {
  static void excuteProjectCommand(String command) { ... }     // 지정자 없음
```

최종 코드는 진입점만 `public` 으로 열고 나머지는 (default) 로 남겼다.

```java
public class ProjectCommand {
  public static void excuteProjectCommand(String command) { ... }   // 열렸다
  static void addProject() { ... }                                  // 그대로 (default)
  static void addMembers(Project project) { ... }
}
```

`App` 이 `bitcamp.myapp2` 에, 이 클래스가 `bitcamp.myapp2.command` 에 있으므로 **밖에서 부르는 것 하나만 열면 된다.** 「공개 API 를 정하라」는 요구에 대한 답이 이 한 줄의 차이다.

## 왜 중요한가

**폴더를 옮기는 것이 접근성을 바꾼다.** Day16 까지 지정자 없이도 실습이 잘 돌아간 것은 모든 클래스가 한 패키지에 있었기 때문이다. 역할별로 패키지를 가르는 순간 (default) 로 붙어 있던 것들이 전부 끊기고, 그때 무엇을 열지 결정해야 한다. **패키지 분리는 공짜가 아니라 「공개 API 를 정하라」는 요구**다 → [[package]]

**공개 범위가 곧 고칠 때의 파급 범위다.** `private` 필드의 이름을 바꾸는 것은 그 클래스 안만 보면 되지만, `public` 필드는 어디서 쓰는지 전부 찾아야 하고 남이 쓰는 코드라면 못 바꾼다. 지정자는 접근을 막는 장치라기보다 **나중에 무엇을 자유롭게 고칠 수 있는지 미리 정하는 장치**다.

## 경계와 오해

- **인터페이스에서 `private` 이 막히는 것은 등급 때문이 아니다** — 열여드레 뒤 회차의 2.1 이 `private void m5();` 를 컴파일 오류로 적어 두고 2.3 은 `private void x() {}` 를 만든다. 갈리는 것은 **몸통**이다. 인터페이스의 몸통 없는 메서드는 구현 클래스가 채워야 하므로 `private` 이면 성립하지 않고(볼 수 없는 것을 채울 수 없다), 인터페이스 안에서 끝나는 코드는 `private` 이어도 된다. **지정자와 「누가 이 코드를 완성하는가」가 묶여 있는 첫 자리**이고, `protected` 가 그쪽에서 아예 쓸 수 없는 것도 물려줄 상태가 없어서다 → [[interface]] · [[default-method]]
- **(default) ≠ `public`** — 아무것도 쓰지 않은 것은 「제한 없음」이 아니라 「같은 패키지에서만」이다. 이름이 없는 등급이라 가장 자주 오해되고, 한 패키지에서 실습하는 동안에는 차이가 드러나지 않아 더 그렇다.
- **`protected` ≠ 상속 전용** — `protected` 는 같은 패키지 전체에도 열려 있다. 표에서 「동일 패키지 내부」가 O 인 것을 같이 읽어야 한다. 「자식만 쓸 수 있게 하려고 `protected`」로 쓰면 같은 패키지의 무관한 클래스에도 열린다.
- **Day16 시점의 표는 접근성을 「누가 보는가」로만 읽게 한다 — 여드레 뒤 회차에서 「무엇을 통해 보는가」가 더 붙는다** — 네 등급 표의 칸은 **코드가 있는 자리**만 따진다. 그런데 `protected` 의 세 번째 칸은 자리만 맞으면 되는 것이 아니라 **접근 경로**까지 본다. `Score` 안에서 `this.clone()` 은 되고 `s1.clone()` 은 안 되는데, 두 줄이 **같은 클래스의 같은 메서드 안에 나란히 있을 수 있다.** 표를 「이 클래스에서 보이나」로 읽으면 이 구별이 아예 표현되지 않는다 → [[object-cloning]] · [[this-reference]]
- **`private` 은 클래스 단위인데 `protected` 는 그렇지 않다** — 같은 클래스의 코드는 다른 인스턴스의 `private` 필드도 읽는다(위의 `that.result`). 그런데 상속으로 받은 `protected` 멤버는 남의 인스턴스로 못 쓴다. **두 등급의 「단위」가 다르다**는 것이고, 등급을 「넓이 순서로 줄 세운 것」으로만 보면 이 차이가 안 보인다.
- **지정자를 넓히는 것이 목적인 코드가 있다** — `clone()` 재정의는 구현을 바꾸려는 것이 아니라 `protected` 를 `public` 으로 여는 것이 전부다(안에서는 `super.clone()` 을 그대로 부른다). 오버라이딩 규칙이 **넓히는 방향만 허용**하는 것이 여기서 제약이 아니라 도구로 쓰인다 → [[method-overriding]]
- **`private` 은 클래스 단위지 인스턴스 단위가 아니다** — 같은 클래스의 코드는 **다른 인스턴스**의 `private` 필드도 읽고 쓴다. 2.3 의 `that.result` 가 그 모양이다(그때는 (default) 였지만 `private` 이어도 똑같이 컴파일된다). 「자기 것만 볼 수 있다」로 외우면 두 인스턴스를 비교하는 메서드를 왜 만들 수 있는지 설명되지 않는다 → [[this-reference]]
- **접근 지정자는 파일 권한이 아니다** — 필기의 「클래스파일에 권한을 설정」은 OS 의 파일 퍼미션과 다른 것이다. 컴파일러가 소스 수준에서 검사하는 규칙이고, `.class` 안에는 지정자가 **정보로 남아 있다.** 값이 물리적으로 감춰지는 것도 아니다 — `private` 필드도 메모리에는 그냥 있다 → [[class-file-format]]
- **`public` 이어도 못 찾을 수 있다** — 지정자는 「보일 자격」만 정하고, 실제로 찾을 수 있는지는 그 클래스가 [[classpath]] 에 있는지가 정한다. 두 가지가 다른 축이라 「public 인데 왜 못 쓰나」의 원인이 갈린다.
- **지정자를 좁히는 쪽이 나중에 어렵다** — 열어 두면 쓰는 코드가 늘어나므로 좁힐 때 전부 고쳐야 한다. 그래서 판단이 안 서면 좁게 두는 것이 안전하다. 이 필기가 3.5 에서 전부 `public` 으로 열었다가 3.6 에서 `private` 으로 되돌릴 수 있었던 것은 쓰는 곳이 `Test02` 하나였기 때문이다.
- **`private` 으로 닫는 것이 곧 「밖에서 하던 일을 대신 해 줄 메서드가 필요해진다」는 뜻이다** — `UserCommand.users` 를 닫자 `ProjectCommand` 가 회원을 찾을 방법이 없어져 `findByNo` 가 생겼다. 지정자는 접근만 막는 것이 아니라 **무엇을 대신 제공해야 하는지를 정한다** → [[cohesion]]
- **클래스를 쪼개면 지정자를 다시 정해야 한다** — Day19 가 `ProjectCommand` 를 `ProjectList` 와 둘로 가를 때 `findByNo`·`indexOf` 를 `private static` 그대로 옮겨 두었는데, **한 클래스 안에서 충분했던 등급이 밖에서 부를 수 없는 코드가 된다.** 최종 코드(`UserList`)에서 `public static` 이 되었다. 지정자는 코드의 성질이 아니라 **경계와의 관계**라서, 경계가 움직이면 같이 움직여야 한다 → [[cohesion]] · [[grasp]]
- **`private` 이 늘어난 것이 아니라 `public` 이 늘었다** — 저장소를 전용 클래스로 옮기면 데이터는 더 잘 감춰지지만 **그 데이터를 다루는 메서드 다섯 개가 `public` 으로 열린다.** 감춘 것과 드러낸 것을 같이 세어야 하고, 드러난 다섯 개가 이제 이 클래스의 **약속**이다 → [[encapsulation]]
- **`private static int seqNo` 는 「전역변수」가 아니다** — 하나뿐이지만 이름이 클래스 밖에서 부를 수 없으므로, 발급 경로가 `getSeqNo()` 하나로 좁혀진다. `static` 과 `private` 을 뭉쳐 「전역」으로 읽으면 이 통제가 안 보인다 → [[static-member]] · [[surrogate-key]]
- **`private` 이 클래스 단위라는 것이 「생성자를 닫는 것」을 성립시킨다** — 생성자를 `private` 으로 만들어 놓고 그 클래스 안에서 `new` 를 부르는 코드는 모순처럼 보이지만, `private` 이 막는 것은 **다른 클래스의 코드**뿐이다. 「자기 것만 볼 수 있다」로 읽으면 `getInstance()` 안의 `new Car()` 가 왜 컴파일되는지 설명되지 않는다. Day28 의 필기도 그 자리에 「private은 같은 class내에서 접근 가능」이라고 주석을 남겼다 → [[singleton-pattern]] · [[constructor]]
- **필기의 「클래스에 소속된 같은 멤버만 접근 가능」은 멤버끼리의 관계가 아니다** — `private` 의 범위는 **같은 클래스에 쓰인 코드 전부**이고, 멤버 하나하나가 서로를 못 본다는 뜻이 아니다. 글자대로 읽으면 `private` 필드를 `private` 메서드가 읽는 흔한 코드가 설명되지 않는다.
- **「바깥 클래스의 객체가 생성되어야 쓸수 있기때문에 일반적으로 private」는 인과가 헐겁다** — 바깥 인스턴스가 필요하다는 것이 **밖에서 못 쓴다는 뜻이 아니다.** 같은 노트가 바로 다음 절에서 `outer.new X()` 로 다른 클래스에서 만드는 문법을 가르친다 — 지정자가 열려 있으면 밖에서도 만들 수 있다. `private` 을 고르는 실제 이유는 접근 방식이 아니라 **그 클래스를 쓰는 코드가 바깥 클래스 안에만 있다**는 것이고, 그 배치가 성립하려면 밖으로 내줄 때 **인터페이스 타입으로** 내줘야 한다(Day32 의 `iterator()` 가 `private` 이어도 되는 `ListIterator` 를 `Iterator` 로 반환하는 것이 그 형태다). **문법 제약과 설계 관례를 하나로 뭉치면 「그럼 정적 중첩 클래스는 왜 `public` 이 많은가」가 설명되지 않는다** → [[nested-class]] · [[interface]] · [[encapsulation]]
- **`private` 중첩 클래스는 밖에서 타입 이름조차 쓸 수 없다** — 그래서 그 타입을 반환값이나 매개변수로 쓰는 `public` 메서드를 만들 수 없다. 최상위 클래스에 `private` 이 없어서 이 문제는 중첩에서 처음 생기고, 답은 **약속 타입을 하나 세워 그것으로 내주는 것**뿐이다. 「감출 수 있다」의 대가로 「밖과 말을 섞으려면 인터페이스가 필요해진다」가 붙는다 → [[interface]] · [[polymorphism]]
- **로컬 클래스에 지정자가 없는 것은 등급이 없는 것이 아니다** — 결과적으로는 (default) 보다도 좁아서 「그 블록 안」이다. 등급 자체를 말할 수 없는 것이라 표의 다른 줄들과 축이 다르고, 그래서 **좁히려고 고른 것이 아니라 스코프가 이미 정해 버린 것**이다 → [[variable-scope]]
- **(default) 로 남겨 둔 것과 (default) 를 고른 것은 구별되지 않는다** — 지정자가 없는 상태는 「아직 안 정했다」와 「같은 패키지에만 열기로 정했다」가 같은 모양이다. `ProjectCommand` 의 `addProject` 가 어느 쪽인지 코드로는 알 수 없고, 그래서 (default) 는 **의도를 기록하지 못하는 등급**이다.

## 함께 보는 개념

- [[package]] — 접근 등급의 기준이 되는 단위
- [[encapsulation]] — 이 문법으로 만드는 설계
- [[class]] — 지정자가 붙는 대상
- [[constructor]] — 열지 않으면 `new` 가 막히는 자리
- [[this-reference]] — `private` 이 클래스 단위임을 보여 주는 예
- [[inheritance]] — 「하위 클래스 내부」열이 뜻하는 관계
- [[classpath]] — 「보이는가」와 다른 축인 「찾는가」
- [[class-file-format]] — 지정자가 컴파일 결과에 남는 곳
- [[java-compilation-unit]] — `public` 클래스와 파일명의 관계
- [[cohesion]] — 닫은 데이터를 대신 다뤄 줄 메서드가 생기는 자리
- [[crud]] — 진입점 하나만 열고 나머지를 닫는 구조
- [[grasp]] — 경계를 다시 그리게 만드는 기준
- [[surrogate-key]] — `private` 이 발급 경로를 하나로 좁히는 예
- [[object-cloning]] — `protected` 의 조건이 드러나는 자리
- [[method-overriding]] — 지정자를 넓히는 쪽만 허용되는 규칙
- [[object-class]] — 상속받은 멤버들의 지정자가 갈리는 곳
- [[singleton-pattern]] — 생성자를 닫는 것이 목적이 되는 자리
- [[interface]] — 생략의 결과가 반대가 되는 자리
- [[default-method]] — `default` 라는 같은 단어의 다른 뜻
- [[nested-class]] — 클래스에 넷이 다 붙는 자리
- [[variable-scope]] — 로컬 클래스에 지정자가 아예 없는 이유

## 출처

- [[2024-06-17-Day16]] — `Score` 를 `vo` 하위 패키지로 옮기자 `Test02` 에서 접근이 끊겨 `public` 을 붙여야 했던 것과, `public`·`protected`·(default)·`private` 네 등급이 「현재 클래스 / 동일 패키지 / 하위 클래스 / 전체」로 갈리는 표를 배웠다
- [[2024-06-18-Day17]] — 실습 프로젝트를 세 패키지로 가르면서 (default) 였던 `vo` 클래스들이 안 보여 `public` 을 붙이고, `command` 클래스는 진입점과 밖에서 쓰는 메서드만 열고 저장소 필드와 내부 메서드는 `private`·(default) 로 닫는 것을 배웠다. `excuteProjectCommand` 가 초안의 (default) 에서 `public` 으로 바뀐 것도 이 자리다
- [[2024-06-20-Day19]] — 클래스를 데이터 쪽과 UI 쪽으로 가르며 `private static` 이던 `findByNo`·`indexOf` 가 `public static` 으로 열려야 했다. 저장소 필드는 더 깊이 감춰지는 대신 그것을 다루는 메서드 다섯 개가 밖으로 드러나는 교환이고, 발급 카운터를 `private static` 으로 닫아 번호를 얻는 경로를 메서드 하나로 좁힌 것도 이 자리다
- [[2024-06-24-Day21]] — `Object.clone()` 이 `protected` 라 `s1.clone()` 이 컴파일 오류가 나는 것을 만나며, 「하위 클래스 내부」칸에 **자기가 상속받은 멤버여야 한다**는 조건이 더 붙는다는 것을 배웠다(「비록 Object의 서브 클래스라 할지라도 남의 인스턴스로 protected 멤버를 사용할 수 없다」). 해결책이 `clone()` 을 오버라이딩해 `public` 으로 **넓히는 것**이라, 지정자를 여는 일이 목적이 되는 첫 코드이기도 하다
- [[2024-07-03-Day28]] — 캡슐화 장에서 네 등급을 다시 정리하며 **Day21 에 컴파일 오류로 만났던 조건을 규칙으로 적었다** — 「자식 클래스에서 상속 받아 만든 변수가 아니면 부모클래스로 생성해도 protected 접근불가」. 같은 장의 싱글톤 예제는 반대 방향으로 지정자를 쓰는 첫 코드다 — 감추기 위해서가 아니라 **생성 자체를 막기 위해** 생성자를 `private` 으로 닫고, 「private은 같은 class내에서 접근 가능」이라 주석을 달아 그 안에서는 `new` 가 되는 이유까지 남겼다
- [[2024-07-05-Day29]] — 인터페이스 회차가 **지정자를 붙이는 세 번째 자리**를 더했다. 인터페이스의 멤버는 생략하면 (default) 가 아니라 `public` 이 되고(「public 이 생략된 것이다. (default) 아니다!」), `protected` 는 쓸 수 없으며 `private` 은 몸통이 있을 때만 된다. 구현 클래스에서 `public` 을 생략하면 접근 범위를 좁히는 것이 되어 막히는 것도 같은 회차에서 컴파일 오류 목록으로 적혔다
- [[2024-07-11-Day33]] — 중첩 클래스 회차가 **지정자를 붙이는 네 번째·다섯 번째 자리**를 더했다. 멤버 클래스에는 넷이 다 붙고(`private static class A1` ~ `public static class A4`, 인스턴스 쪽도 같다) 그 근거를 「클래스의 멤버이기 때문에 필드나 메서드처럼」으로 적어 **최상위 클래스가 둘뿐인 것과 갈리는 이유**를 명시한다. 로컬 클래스에는 넷 다 못 붙는데 이유가 등급이 아니라 스코프이고, 필기가 「로컬 변수처럼」이라 적어 그 축을 짚었다. 그리고 종류마다 관례를 갈라 적었다 — 정적 중첩은 「외부에서 사용되는 경우도 많아 default나 public」, 인스턴스 중첩은 「바깥 클래스의 객체가 생성되어야 쓸수 있기때문에 일반적으로 private」. 뒤쪽 이유는 헐겁다 — 같은 노트가 다음 절에서 `outer.new X()` 로 밖에서 만드는 문법을 가르치기 때문이다
