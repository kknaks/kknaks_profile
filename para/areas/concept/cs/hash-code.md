---
type: concept
id: hash-code
title: 해시코드 (hashCode)
aliases:
  - 해시코드
  - 해시값
  - 해쉬값
  - hashCode
  - hash code
  - 해시
up:
  - 2024-06-24-Day21
  - 2024-06-25-Day22
tags:
  - java
  - 자료구조
  - 비교
  - 성능
---

# 해시코드 (hashCode)

인스턴스를 **하나의 `int` 로 요약한 값.** 「같은가」를 필드 하나하나 비교하지 않고 숫자 하나로 먼저 걸러 내기 위해 존재하고, 그래서 해시 기반 저장소가 **위치를 계산하는 재료**로 쓴다.

## 정의

[[object-class]] 의 기본 `hashCode()` 는 **인스턴스마다 다른 값**을 준다. 내용은 보지 않는다.

```java
My obj1 = new My();  obj1.name = "홍길동";  obj1.age = 20;
My obj2 = new My();  obj2.name = "홍길동";  obj2.age = 20;

System.out.println(Integer.toHexString(obj1.hashCode())); //7ad041f3
System.out.println(Integer.toHexString(obj2.hashCode())); //251a69d7
```

같은 값을 넣었는데 다른 해시코드다. 이 값이 `toString()` 의 `@` 뒤에 붙는 그 숫자다 — `com.eomcs.basic.ex01.Exam0120$My@7ad041f3` 의 16진수가 곧 해시코드다.

내용 기준으로 바꾸려면 재정의한다. 필기는 두 방식을 차례로 썼다.

```java
@Override
public int hashCode() {
  // String 클래스의 hashCode() 메서드는
  // 같은 문자열에 대해 같은 해시값을 리턴한다.
  String str = String.format("%s,%d", this.name, this.age);
  return str.hashCode();
}
```

```java
@Override
public int hashCode() {
  return Objects.hash(age, name, working);       // 같은 일을 표준 유틸로
}
```

**뒤쪽이 하는 일이 앞쪽과 같다.** 필드들을 하나의 `int` 로 접는 것이고, 앞의 방식은 그 중간에 문자열을 한 개 만들었다 → [[string-comparison]] · [[format-string]]

## 사용 예시

재정의하면 **같은 내용의 두 인스턴스가 같은 해시코드**를 갖는다.

```java
System.out.println(Integer.toHexString(obj1.hashCode())); //994aa0fc
System.out.println(Integer.toHexString(obj2.hashCode())); //994aa0fc
```

이 한 줄의 변화가 컬렉션의 동작을 바꾼다. `HashMap` 실습이 재정의 전의 상태를 그대로 보여 준다.

```java
MyKey k3 = new MyKey("haha");
map.put(k3, new Student("유관순", 17, true));

MyKey k6 = new MyKey("haha");            // 같은 내용으로 새로 만들었다
System.out.println(map.get(k6));         // 엥? 값을 꺼낼 수가 없다.

System.out.println(k3 == k6);            // 인스턴스는 다르다.
System.out.println(k3.hashCode());       // hash code는 다르다.
System.out.println(k6.hashCode());       // hash code는 다르다.
System.out.println(k3.equals(k6));       // equals()의 비교 결과도 다르다.
```

**「내용물이 같은데 못 찾는다」의 원인이 해시코드**다. 넣을 때 계산한 위치와 찾을 때 계산한 위치가 다르니 같은 자리를 보지도 않는다 → [[hash-based-collection]]

## 왜 중요한가

**조회가 훑기에서 계산으로 바뀐다.** Day19 의 `findByNo` 는 앞에서부터 하나씩 비교했지만, 해시코드가 있으면 값에서 **저장할 자리를 바로 계산**한다. 비교 횟수가 개수에 비례하던 것이 상수에 가까워지고, 이것이 해시코드가 존재하는 이유 전부다 → [[linear-search]] · [[search-index]]

**그리고 `equals` 만으로는 그 이득을 못 얻는다.** 내용 비교가 정확해도 전부와 비교하면 여전히 선형이다. 해시코드는 **비교할 후보를 좁히는 값**이고, 정확한 판정은 여전히 `equals` 가 한다. 둘이 역할을 나눠 갖는 구조라 **하나만 재정의하면 반쪽이 된다** → [[object-equality]]

## 경계와 오해

- **해시코드 ≠ 메모리 주소** — `toString()` 이 `@7ad041f3` 처럼 찍어 주므로 주소로 읽히지만, 인스턴스를 구별하기 위한 값이고 실행마다 달라진다. 그래서 **파일이나 DB 에 저장하거나 네트워크로 보내면 안 된다** → [[object-reference]]
- **해시코드가 같다고 같은 객체가 아니다** — `int` 는 약 42억 개뿐인데 인스턴스는 그보다 많이 만들 수 있으므로 **다른 내용이 같은 해시코드를 갖는 일(충돌)이 반드시 생긴다.** 그래서 필기 3.2 의 주석 「해시코드가 같다면 같은 key로 간주한다」는 어긋난다 — `HashMap` 은 해시코드로 자리를 찾고 그 자리에서 `equals` 로 확정한다 → [[hash-based-collection]]
- **「고유번호값」이 아니다** — 필기의 표현인데 유일성이 보장되지 않는다. Day19 의 `seqNo` 는 발급 카운터라 정말 유일했고, 해시코드는 **값에서 계산해 낸 요약**이라 겹칠 수 있다. 둘 다 「식별하는 숫자」로 불리지만 한쪽만 약속이다 → [[surrogate-key]]
- **한 방향만 강제된다** — `equals` 가 `true` 면 해시코드는 **반드시** 같아야 한다. 거꾸로 해시코드가 같은데 `equals` 가 `false` 인 것은 정상(충돌)이다. 「둘이 항상 함께 움직인다」로 읽으면 충돌이 버그로 보인다.
- **가변 필드로 해시코드를 만들면 넣은 뒤에 잃어버린다** — `Objects.hash(age, name, working)` 는 세 필드를 읽는데 `Student` 의 필드는 전부 열려 있다. 컬렉션에 넣고 나서 `age` 를 바꾸면 해시코드가 변해 **넣은 자리를 다시 찾을 수 없다.** 「같은 인스턴스를 들고 있으니 찾을 수 있다」가 여기서 깨진다 → [[encapsulation]]
- **그래서 「재정의하지 않는 것」도 결정이다** — Day21 시점에는 재정의가 기본이고 안 하면 반쪽이라는 방향으로만 배웠는데, 다음 회차의 `StringBuffer` 가 반대쪽 사례다. 내용을 바꿀 수 있는 클래스가 내용 기준으로 해싱하면 **위 항목의 문제를 클래스 차원에서 보장하는 셈**이 되므로, 표준 라이브러리는 재정의하지 않는 쪽을 택했다. 그 결과가 필기의 출력에 그대로 남아 있다 — `Hello` → `Hexxxxo` 로 내용이 바뀌었는데 해시코드가 그대로다. **`String` 은 재정의했고 `StringBuffer` 는 안 했으며, 갈린 기준이 [[immutability]] 다** → [[string-builder]]
- **필기의 `498931366` 이 세 번 다 같은 것은 옮겨 적은 값이다** — `StringBuffer` 와 `StringBuilder` 는 서로 다른 인스턴스이므로 기본 구현에서 같은 값이 나올 이유가 없다. **「변경 전후가 같다」는 요점은 맞고, 「두 클래스가 같은 값을 준다」로 읽으면 틀린다.** 앞 절의 출력을 그대로 옮긴 흔적이 Day21 의 `7ad041f3` 와 같은 종류다
- **필드 하나를 빼먹으면 조용히 느려지고, 넣지 않아야 할 것을 넣으면 조용히 못 찾는다** — 오류가 나지 않는다. `equals` 는 세 필드를 보는데 `hashCode` 는 두 개만 본다면 판정은 맞고 충돌만 늘어난다. **틀린 방향과 느린 방향이 다르다.**
- **`String.format(...).hashCode()` 는 동작하지만 대가가 있다** — 부를 때마다 문자열 인스턴스가 하나 생기고 버려진다. `Objects.hash` 는 그것 없이 같은 일을 하고, 필기 안에서 2.4 → 3.1 로 방식이 바뀐 것이 그 개선이다. 다만 **필기에 바꾼 이유가 적혀 있지 않다** → [[garbage-collection]]
- **필기 2.4 「기본형」의 출력값은 앞 절에서 옮겨 온 것이다** — `7ad041f3`·`251a69d7` 이 2.1 `toString()` 예제의 값과 똑같다. 실행이 다르면 해시코드도 달라지므로 같은 값이 나올 이유가 없다. 값 자체는 「인스턴스마다 다르다」를 보여 주므로 요점은 유지되지만, **실제로 찍어 본 값이 아니다.**
- **`Integer.toHexString` 은 해시코드의 일부가 아니다** — 그냥 16진수로 보기 좋게 찍는 것이다. `toString()` 의 형식과 맞춰 보기 위해 쓴 것이고, `hashCode()` 자체는 10진 `int` 를 돌려준다 → [[number-parsing]]

## 함께 보는 개념

- [[object-equality]] — 해시코드가 좁힌 후보를 확정하는 짝
- [[hash-based-collection]] — 이 값을 위치 계산에 쓰는 곳
- [[object-class]] — 기본 구현이 사는 자리
- [[method-overriding]] — 내용 기준으로 바꾸는 방법
- [[surrogate-key]] — 「식별하는 숫자」의 다른 종류
- [[linear-search]] — 해시코드가 대체하는 조회 방식
- [[search-index]] — 같은 아이디어의 저장소 층
- [[caching]] — 키로 즉시 꺼내는 구조
- [[string-comparison]] — `String` 이 이미 재정의해 둔 해시코드
- [[object-reference]] — 주소와 갈리는 자리
- [[encapsulation]] — 해시코드의 재료를 잠가야 하는 이유
- [[immutability]] — 내용 기준 해싱이 안전해지는 조건
- [[string-builder]] — 일부러 재정의하지 않은 클래스

## 출처

- [[2024-06-24-Day21]] — 「hashCode는 데이터를 구분하기위한 고유번호값」이라는 정의와, 기본 구현은 같은 내용의 두 인스턴스에 다른 값을 준다는 것을 `Integer.toHexString` 으로 확인했다. `String.format(...).hashCode()` 로 재정의해 같은 내용이 같은 값을 갖게 만들고, 이어 `Objects.hash(...)` 로 바꾸는 것까지 한 회차에 나온다. `HashMap` 에서 내용이 같은 키로 값을 못 꺼내는 원인이 이 값이라는 것도 같은 자리다
- [[2024-06-25-Day22]] — `StringBuffer`·`StringBuilder` 의 내용을 `replace()` 로 바꿔도 해시코드가 그대로인 것을 출력으로 확인했다. 재정의를 배우는 것이 아니라 **재정의하지 않은 클래스를 관찰한 것**이고, 가변 객체라 그것이 옳은 선택이라는 대비가 여기서 생긴다
