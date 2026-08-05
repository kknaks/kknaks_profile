---
type: concept
id: object-equality
title: 동일성과 동등성 (equals 재정의)
aliases:
  - 동일성
  - 동등성
  - 동일성과 동등성
  - equals 재정의
  - equals 오버라이딩
  - object equality
  - identity vs equality
up:
  - 2024-06-24-Day21
  - 2024-07-08-Day30
  - 2024-07-15-Day35
tags:
  - java
  - 객체지향
  - 비교
  - 설계
---

# 동일성과 동등성 (equals 재정의)

「같다」에 두 가지 뜻이 있다 — **같은 인스턴스인가**(동일성)와 **내용이 같은가**(동등성). 자바는 앞의 것만 문법으로 주고, 뒤의 것은 **각 클래스가 `equals()` 를 재정의해 스스로 정한다.**

## 정의

| | 묻는 것 | 문법 | 누가 정하나 |
|---|---|---|---|
| 동일성 (identity) | 같은 인스턴스인가 | `==` | 언어 — 바꿀 수 없다 |
| 동등성 (equality) | 내용이 같은가 | `.equals()` | **클래스** — 재정의해야 생긴다 |

[[object-class]] 에서 물려받은 `equals()` 의 기본 구현은 **주소를 비교한다.** 즉 재정의하지 않으면 `equals()` 와 `==` 가 같은 답을 준다.

재정의 골격은 다섯 단계다.

```java
@Override
public boolean equals(Object obj) {
  if (this == obj) {                     // 1. 같은 인스턴스면 볼 것도 없다
    return true;
  }
  if (obj == null) {                     // 2. null 이면 아래에서 터진다
    return false;
  }
  if (getClass() != obj.getClass()) {    // 3. 같은 클래스가 아니면 비교 불가
    return false;
  }
  My other = (My) obj;                   // 4. Object 로 받았으니 되돌린다
  //파라미터가 type이 Object type이기 때문에 형변환을 적용한다.
  return age == other.age && Objects.equals(name, other.name);   // 5. 필드 비교
}
```

**네 번째 줄이 필요한 이유가 매개변수 타입에 있다.** 선언부를 `Object obj` 로 맞춰야 오버라이딩이 되고, 그러면 안에서 다운캐스팅을 해야 필드에 닿는다 → [[method-overriding]] · [[type-casting]]

## 사용 예시

같은 값을 넣은 두 인스턴스로 재정의 전후를 비교한다.

```java
My obj1 = new My();
obj1.name = "홍길동";
obj1.age = 20;

My obj2 = new My();
obj2.name = "홍길동";
obj2.age = 20;
```

재정의하기 전.

```java
System.out.println(obj1 == obj2);        //false
System.out.println(obj1.equals(obj2));   //false
```

재정의한 뒤. **`==` 는 그대로고 `equals` 만 뒤집힌다.**

```java
System.out.println(obj1 == obj2);        //false
System.out.println(obj1.equals(obj2));   //true
```

`==` 가 계속 `false` 인 것이 중요하다 — 인스턴스는 여전히 둘이고, 바뀐 것은 **「같다」를 무엇으로 판정하느냐**뿐이다 → [[object-reference]]

### 필드가 세 개면 조건도 세 개가 된다

같은 회차의 `Student` 는 필드가 셋이라 마지막 줄만 길어진다. 골격은 그대로다.

```java
Student other = (Student) obj;
return age == other.age && Objects.equals(name, other.name) && working == other.working;
```

**어느 필드를 비교에 넣을지가 곧 「같은 학생」의 정의**다. `working` 을 빼면 재직 여부가 달라도 같은 학생이 되고, 이 결정은 문법이 아니라 도메인이 정한다 → [[cohesion]]

`String` 필드에 `Objects.equals` 를 쓰고 `int`·`boolean` 에는 `==` 를 쓴 것도 우연이 아니다 — 참조 타입과 기본 타입에서 `==` 의 뜻이 갈리기 때문이다 → [[string-comparison]] · [[data-type]]

### 21일 뒤, 같은 골격을 짧게 쓰고 다른 결정을 한다

Day35 의 메뉴 트리는 모든 노드의 공통 부모에 `equals`·`hashCode` 를 함께 재정의한다.

```java
import java.util.Objects;

public abstract class AbstractMenu implements Menu {
  protected String title;

  @Override
  public boolean equals(Object object) {
    if (this == object)
      return true;
    if (!(object instanceof AbstractMenu that))
      return false;
    return Objects.equals(title, that.title);
  }

  @Override
  public int hashCode() {
    return Objects.hashCode(title);
  }
}
```

**다섯 단계가 세 줄로 줄었고, 줄어든 이유가 문법이 아니라 선택에 있다.**

| Day21 의 단계 | Day35 | 왜 |
|---|---|---|
| `this == obj` | 그대로 | 속도용 |
| `obj == null` | **없다** | `null instanceof X` 가 `false` 다 |
| `getClass() != obj.getClass()` | **`instanceof AbstractMenu`** | 자식 종류를 구별하지 않기로 정했다 |
| 다운캐스팅 한 줄 | **없다** | `instanceof AbstractMenu that` 이 겸한다 |
| 필드 비교 | `Objects.equals(title, that.title)` | 그대로 |

두 번째와 네 번째 칸이 사라진 것은 **`instanceof` 로 바꾼 데서 따라오는 결과**다 — `null` 을 걸러 주고 검사와 동시에 변수를 내주므로, Day21 의 골격에서 두 줄을 지울 권한이 생긴다 → [[instanceof-operator]] · [[type-casting]]

그리고 이번에는 `import java.util.Objects;` 가 **적혀 있다.** Day21 의 예제 코드에는 그 줄이 빠져 그대로는 컴파일되지 않았다 → [[object-class]]

## 왜 중요한가

**「같다」의 판정을 남의 코드가 쓴다.** `equals()` 를 재정의하는 것은 내 코드에서 부르기 위해서가 아니다 — `HashSet` 의 중복 검사, `HashMap` 의 키 조회, `List.contains` 가 전부 이 메서드를 부른다. 재정의를 빠뜨리면 **내가 쓰지도 않은 코드가 조용히 틀린 답을 낸다** → [[hash-based-collection]]

**그리고 재정의를 안 해도 컴파일되고 실행된다.** 물려받은 기본 구현이 있으니 오류가 나지 않고, 인스턴스를 하나씩만 다루는 동안은 결과도 맞다. 필기의 `Exam0130` 이 그 상태다 — 내용이 같은 두 인스턴스를 만들어 본 순간에만 드러난다.

**Day19 에서 미뤄 둔 질문의 답이 여기 있다.** 그때 `indexOf` 는 `users[i] == user` 로 회원을 찾았고, 이름·번호가 다 같은 다른 인스턴스를 넘기면 `-1` 이 왔다. 그 자리에서 필요했던 것이 `equals` 재정의였고, **번호로 찾는 `findByNo` 를 따로 만든 것이 그 우회로**였다 → [[linear-search]] · [[surrogate-key]]

### 그리고 그 우회로를 버린 회차가 프로그램의 절반을 잃는다

**18일 뒤 리팩터링 회차는 `findByNo` 를 없애고 정면으로 간다.** 번호만 든 임시 객체를 만들어 목록에 「이것과 같은 것이 몇 번째냐」를 묻는 형태다.

```java
int userNo = Prompt.inputInt("회원번호?");
User user = (User) userList.get(userList.indexOf(new User(userNo)));
if (user == null) {
  System.out.println("없는 회원입니다.");
  return;
}
```

**이 코드는 `equals` 로만 성립한다.** 방금 `new` 한 객체는 목록에 든 어떤 인스턴스와도 주소가 다르므로, 찾는 일이 **내용 비교**여야 한다. 그런데 같은 노트의 `indexOf` 는 이렇다.

```java
// ArrayList
@Override
public int indexOf(Object obj) {
  for (int i = 0; i < size; i++) {
    if (list[i] == obj) {          // Day23 에는 list[i].equals(obj) 였다
      return i;
    }
  }
  return -1;
}
```

```java
// LinkedList
if (cursor.value == value) {
  return currentIndex;
}
```

**`indexOf` 가 항상 `-1` 을 돌려준다.** 그러면 `get(-1)` 이 범위 검사에 걸려 `null` 이 되고, 화면에는 **언제나 「없는 회원입니다」**가 뜬다. 회원·프로젝트·게시글의 **조회·변경·삭제 아홉 개 기능이 모두** 이 두 줄을 쓰므로 전부 같은 결과다. 등록과 목록만 살아 있다.

**`User` 가 `equals` 를 재정의했는지는 상관이 없다** — `==` 는 그 메서드를 부르지 않는다. Day21 에서 배운 「재정의를 빠뜨리면 남의 코드가 조용히 틀린 답을 낸다」의 한 칸 더 나쁜 버전이고, 여기서는 **재정의를 부를 자리 자체가 `==` 로 막혀 있다** → [[method-overriding]] · [[refactoring]]

## 경계와 오해

- **동일성 ≠ 동등성** — 같은 인스턴스면 내용도 같지만, 내용이 같아도 인스턴스는 다를 수 있다. 한 방향만 성립한다. 그래서 `equals` 를 재정의한 뒤에도 `==` 는 여전히 `false` 이고, **둘 다 필요하다.**
- **「기본적으로 두 인스턴스를 비교하면 false」가 아니다** — 필기의 표현인데, 기본 구현은 **주소를 비교**하므로 같은 인스턴스를 두 번 가리키면 `true` 다(`obj1.equals(obj1)`). 「항상 false」로 외우면 재정의 골격의 첫 줄(`this == obj` 면 `true`)이 왜 있는지 설명되지 않는다.
- **`equals(My obj)` 는 오버라이딩이 아니다** — 매개변수 타입을 편하게 바꾸면 선언부가 달라져 **같은 이름의 새 메서드**가 하나 더 생긴다(오버로딩). `set.add()` 는 `Object` 를 받는 쪽을 부르므로 재정의한 줄 알았던 코드가 전혀 불리지 않는다. `@Override` 를 붙였다면 그 자리에서 컴파일 오류로 잡힌다 → [[method-overriding]] · [[annotation]]
- **`equals` 만 재정의하면 반쪽이다** — 해시 기반 컬렉션은 `hashCode()` 로 자리를 먼저 찾으므로, `equals` 가 `true` 여도 해시코드가 다르면 만나지도 못한다. 필기가 2.3 에서 `equals` 만, 2.4 에서 `hashCode` 만 따로 재정의했다가 **3장에서 둘을 함께 재정의하게 되는 것**이 그 발견이다 → [[hash-code]]
- **`getClass()` 비교와 `instanceof` 는 다른 결정이다 — 21일 뒤에 반대쪽을 고르고 그 대가를 받는다** — `getClass()` 는 정확히 같은 클래스만 통과시키므로 자식 인스턴스는 부모와 절대 같지 않다. `instanceof` 로 쓰면 자식도 통과하는데, 이번엔 「부모.equals(자식)」과 「자식.equals(부모)」의 답이 달라질 수 있다. **어느 쪽도 공짜가 아니고**, Day21 은 `getClass()` 를 골랐다. **Day35 의 `AbstractMenu` 는 `instanceof AbstractMenu` 를 고르고, 그러면 서로 다른 종류가 같아진다** — 제목이 같은 `MenuGroup` 과 `MenuItem` 이 `equals` 로 참이 된다. 「회원」이라는 이름의 서브메뉴와 「회원」이라는 이름의 실행 항목이 **같은 메뉴로 취급되는 것**이고, 트리에서는 가지와 잎을 구별하지 않는 것이 목적이므로 **의도로 볼 수도 있는 자리다.** 다만 필기가 그것을 결정으로 적지 않았으므로 왜 `getClass()` 를 안 썼는지는 남는다 → [[instanceof-operator]] · [[class-metadata]] · [[composite-pattern]]
- **「부모노드의 객체와 같은지 확인」하는 코드는 없다 — `equals` 를 실제로 부르는 것은 목록이다** — Day35 필기가 이유를 「트리노드에서 부모노드의 객체와 같은 확인하는 메서드 equals()와 hash()가 필요하다」로 적었는데, `MenuGroup` 어디에도 자기와 부모를 비교하는 줄이 없다. `equals` 를 부를 수 있는 자리는 `remove(Menu child)` 안의 **`children.remove(child)`** 하나이고(`List.remove(Object)` 는 `equals` 로 찾는다), 그것이 Day21 에서 배운 「내가 쓰지도 않은 코드가 이 메서드를 부른다」의 또 한 예다. **이유를 잘못 짚어도 필요한 메서드가 만들어진 것**이라 코드로는 티가 안 난다 → [[hash-based-collection]] · [[linear-search]]
- **그런데 그 `remove` 를 아무도 부르지 않는다 — `hashCode` 도 쓰이지 않는다** — 메뉴 트리는 `App` 의 생성자에서 조립된 뒤 항목이 빠지지 않는다. `children` 은 `ArrayList` 이므로 해시도 쓰지 않는다. 즉 Day35 의 `equals`·`hashCode` 는 **현재 한 번도 불리지 않는 쌍**이다. Day21 의 교훈은 「빠뜨리면 남의 코드가 조용히 틀린 답을 낸다」였고 이쪽은 그 반대 방향의 짝이다 — **규약을 먼저 갖춰 두는 것이 손해는 아니지만, 갖췄다고 검증된 것도 아니다.** 제목이 같은 항목이 한 그룹에 둘 있을 때 `remove` 가 앞의 것을 지우는지는 부르는 코드가 생기는 날 처음 드러난다.
- **두 번째와 세 번째 줄의 순서를 바꿀 수 없다 — 그리고 `instanceof` 로 쓰면 두 줄이 한 줄이 된다** — `obj` 가 `null` 인 채로 `obj.getClass()` 를 부르면 `NullPointerException` 이다. 이 순서는 취향이 아니라 조건이다. Day35 의 `equals` 에 `null` 검사가 아예 없는 것이 그 조건에서 벗어난 결과다 — `null instanceof AbstractMenu` 가 `false` 이므로 **타입 검사가 `null` 검사를 흡수한다.** 「줄이 빠졌다」가 아니라 「빠질 수 있는 형태로 바꿨다」이고, `getClass()` 로 되돌리는 순간 그 줄이 다시 필요해진다 → [[object-reference]] · [[instanceof-operator]]
- **`this == obj` 는 정확성이 아니라 속도를 위한 줄이다** — 지워도 답은 같다(아래에서 필드끼리 비교해도 `true` 가 나온다). 「없으면 틀리는 줄」과 「있으면 빠른 줄」이 나란히 있는 것이라 골격을 통째로 외우면 구별되지 않는다.
- **`Objects.equals(a, b)` 는 `a.equals(b)` 와 다르다** — 양쪽이 `null` 이어도 터지지 않고 `true` 를 준다. Day11 에서 배운 `"종료".equals(menu)` 뒤집기 관용구가 하던 일을 표준 유틸이 대신하는 것이고, **필드가 `null` 일 수 있는 클래스에서는 이쪽이 유일하게 맞는 선택**이다 → [[string-comparison]]
- **`Objects` 는 `Object` 가 아니다** — 이름이 `s` 하나 차이인데 하나는 모든 클래스의 조상이고 하나는 `java.util` 의 정적 유틸 클래스다. Day21 의 필기 코드에는 `import java.util.Objects;` 가 빠져 있어서 그대로는 컴파일되지 않고, **Day35 의 `AbstractMenu` 에는 그 줄이 있다** → [[object-class]]
- **`hashCode()` 를 `title.hashCode()` 로 쓰면 안 된다** — Day35 는 `Objects.hashCode(title)` 을 썼다. 필드가 `null` 일 때 `title.hashCode()` 는 `NullPointerException` 이고 `Objects.hashCode(null)` 은 `0` 이다. **`equals` 에서 `Objects.equals` 를 쓴 것과 같은 이유가 `hashCode` 에도 그대로 적용되는 것**이고, 둘 중 한쪽만 `null` 안전하게 쓰면 「같다고 판정되는 두 객체가 해시를 물을 때만 터진다」가 된다 → [[hash-code]]
- **`==` 로 쓴 `indexOf` 는 「틀린 답」이 아니라 「아무것도 못 찾는 함수」다** — 내용이 같은 것을 놓치는 정도가 아니다. **찾는 열쇠를 그 자리에서 `new` 로 만드는 코드와 짝이 되면 성공하는 경우가 하나도 없다.** 그래서 이 종류의 버그는 「가끔 이상하다」가 아니라 「그 기능이 통째로 안 된다」로 나타나고, 그럼에도 예외도 오류 메시지도 없이 **「없는 회원입니다」라는 그럴듯한 안내**로 끝난다 → [[linear-search]]
- **`equals` 를 쓰기로 정하면 「무엇이 같은가」를 번호로 좁혀야 한다** — `new User(userNo)` 는 번호만 채운 껍데기다. 그것이 목록의 회원과 같다고 판정되려면 `User.equals` 가 **번호만** 비교해야 하고, 이름·이메일까지 비교하면 여전히 못 찾는다. 즉 이 호출 형태를 고르는 순간 **동등성의 정의가 「같은 사람인가」에서 「같은 번호인가」로 정해진다** — 조회용 열쇠 객체를 쓰는 코드는 `equals` 의 내용까지 지정하는 것이다 → [[surrogate-key]]
- **`contain(User)` 이 `contains(Object)` 로 넓어지면 실수를 잡아 줄 것이 없어진다** — 리팩터링 회차의 `ArrayList` 는 매개변수를 `Object` 로 바꿨다. 편해 보이지만 **엉뚱한 타입을 넘겨도 컴파일된다** — `equals` 가 `Object` 를 받아야 하는 것과 같은 대가이고, 그쪽은 오버라이딩 때문에 어쩔 수 없었던 것인데 이쪽은 선택이다 → [[type-casting]]
- **필기 3.2 의 `MyKey2 other = (MyKey2) obj;` 는 클래스 이름이 어긋난다** — 그 절의 클래스는 `MyKey` 이고 `MyKey2` 는 어디에도 정의되지 않았다. 앞뒤 예제를 옮겨 붙이며 이름만 남은 자리다.

## 함께 보는 개념

- [[hash-code]] — 함께 재정의해야 하는 짝
- [[hash-based-collection]] — 이 판정을 실제로 쓰는 곳
- [[string-comparison]] — 같은 구분을 문자열에서 만나는 자리
- [[method-overriding]] — 재정의의 규칙
- [[object-class]] — 기본 구현이 사는 곳
- [[object-reference]] — `==` 가 비교하는 것
- [[type-casting]] — `Object` 로 받은 것을 되돌리는 일
- [[instanceof-operator]] — `getClass()` 와 갈리는 선택지
- [[class-metadata]] — 「같은 클래스인가」의 판정 도구
- [[cohesion]] — 동일성 규칙을 어느 클래스가 갖는가
- [[annotation]] — 오버로딩 사고를 막아 주는 표시
- [[linear-search]] — 「같은 것 찾기」가 이 판정을 부르는 자리
- [[surrogate-key]] — 번호만 든 열쇠 객체로 찾을 때의 전제
- [[dynamic-array]] — `indexOf` 가 `==` 로 후퇴한 한쪽
- [[linked-list]] — 같은 비교를 쓰는 다른 쪽
- [[refactoring]] — 이 후퇴가 들어온 작업
- [[composite-pattern]] — 가지와 잎을 같게 판정하기로 정한 자리
- [[abstract-class]] — 판정 규칙을 모든 노드에 한 벌로 주는 그릇

## 출처

- [[2024-06-24-Day21]] — `Object.equals` 의 기본 구현이 주소 비교라 내용이 같은 두 인스턴스도 `false` 라는 것을 확인한 뒤, `this == obj` → `obj == null` → `getClass()` 비교 → 다운캐스팅 → 필드 비교의 다섯 단계 골격으로 재정의해 `equals` 만 `true` 로 뒤집는 것을 배웠다. 「같은 클래스를 확인하기 위해 getClass()를 사용한다」와 「대표적으로 String.equals()가 Override를 활용한 경우이다」도 이 자리다
- [[2024-07-08-Day30]] — 이 판정이 **없어서 프로그램의 절반이 죽은 코드**가 남았다. 리팩터링 회차의 Command 들이 `userList.get(userList.indexOf(new User(userNo)))` 로 조회하는데, 같은 노트의 `ArrayList.indexOf` 는 Day23 의 `list[i].equals(obj)` 에서 `list[i] == obj` 로 바뀌었고 `LinkedList.indexOf` 도 `cursor.value == value` 다. 방금 `new` 한 열쇠 객체는 주소가 절대 같지 않으므로 `indexOf` 가 항상 `-1` 이고, **회원·프로젝트·게시글의 조회·변경·삭제 아홉 기능이 모두 「없는 회원입니다」로 끝난다.** Day19 의 `findByNo` 우회로를 버리고 정면으로 갔는데 정면에 필요한 것이 빠진 형태이며, 필기에는 이 사실이 적혀 있지 않다
- [[2024-07-15-Day35]] — 메뉴 트리의 공통 부모 `AbstractMenu` 가 `equals`·`hashCode` 를 **처음부터 함께** 재정의한다(Day21 은 따로 만들었다가 합쳤다). Day21 의 다섯 단계가 세 줄로 줄고 그 줄어든 자리가 전부 **`getClass()` 대신 `instanceof AbstractMenu that` 을 고른 결과**다 — `null` 검사와 다운캐스팅 줄이 그 한 줄에 흡수된다. 대가는 제목이 같은 `MenuGroup` 과 `MenuItem` 이 같다고 판정되는 것이고, 가지와 잎을 구별하지 않는 것이 목적인 구조에서는 의도로 볼 수 있으나 필기는 그것을 결정으로 적지 않았다. **필기가 적은 이유(「트리노드에서 부모노드의 객체와 같은 확인하는」)에 해당하는 코드는 없고**, 실제로 `equals` 를 부를 수 있는 자리는 `children.remove(child)` 하나인데 **그 `remove` 를 호출하는 코드도 없다** — 규약을 먼저 갖췄지만 한 번도 불리지 않는 쌍이다. `Objects.equals`·`Objects.hashCode` 로 `null` 을 양쪽 다 막았고 `import java.util.Objects;` 도 이번엔 빠지지 않았다
