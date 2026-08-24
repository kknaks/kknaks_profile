---
type: concept
id: immutability
title: 불변 객체 (Immutable Object)
aliases:
  - 불변
  - 불변 객체
  - immutable
  - immutability
  - 가변 객체
  - mutable
up:
  - 2024-06-25-Day22
tags:
  - java
  - 설계
  - 문자열
  - 메모리
---

# 불변 객체 (Immutable Object)

한 번 만들어지면 **내용을 바꿀 수 없는** 인스턴스. 바꾸는 메서드가 없는 것이 아니라, 바꾸는 것처럼 보이는 메서드가 **원본을 놔두고 새 인스턴스를 만들어 돌려준다.**

## 정의

`String` 이 그렇다. 필기가 두 메서드로 확인한다.

```java
String s1 = new String("Hello");

// String 클래스의 메서드는 원본 인스턴스의 데이터를 변경하지 않는다.
// 다만 새로 String 객체를 만들 뿐이다.
String s2 = s1.replace('l', 'x');
System.out.println(s1 == s2); // false
System.out.printf("%s : %s\n", s1, s2); // 원본은 바뀌지 않는다.

String s3 = s1.concat(", world!");
System.out.println(s1 == s3); // false
```

**`==` 가 `false` 인 것이 증거다.** 원본을 고쳤다면 같은 주소를 돌려줄 수 있었을 텐데, 새 주소가 나왔다는 것은 인스턴스가 하나 더 생겼다는 뜻이다 → [[object-reference]] · [[instance]]

반대쪽이 **가변(mutable) 객체**다. 같은 회차에서 `StringBuffer` 로 같은 일을 하면 주소가 그대로다 → [[string-builder]]

| | 바꾸는 메서드를 부르면 | `==` 로 비교하면 |
|---|---|---|
| **불변** (`String`) | 새 인스턴스가 나온다 | 원본과 다르다 |
| **가변** (`StringBuffer`) | 원본이 바뀐다 | 같은 인스턴스다 |

## 사용 예시

불변이라는 성질이 **자기 자신을 그대로 돌려줘도 안전하게** 만든다. 같은 회차 1.2 의 마지막 줄이 그것이다.

```java
Object obj = new String("Hello");
String x1 = (String) obj;
String x2 = obj.toString();
System.out.println(x1 == x2); // true
```

**`toString()` 이 새 문자열을 만들지 않고 `this` 를 돌려주기 때문에 `true` 다.** 필기는 이 줄을 오버라이딩 이야기로 읽었지만, 그 앞의 1.3 이 이유를 준다 — 받은 쪽이 내용을 바꿀 수 없으니 내부를 그대로 내줘도 잃을 것이 없다.

**같은 판단을 가변 객체로는 할 수 없다.** 일주일 전 회차의 `toArray()` 가 배열을 새로 만들어 돌려주던 것이 그 대비다 — 배열은 가변이므로 원본을 내주면 밖에서 고칠 수 있다. 사본을 만드는 비용은 **불변인 쪽에서만** 사라진다 → [[defensive-copy]] · [[array-copy]]

## 왜 중요한가

**공유해도 되는 이유가 불변이다.** 문자열 리터럴은 같은 글자면 인스턴스 하나를 여러 변수가 나눠 쓴다. 만약 `String` 이 가변이었다면 한 곳에서 `"Hello"` 를 고치는 순간 그 리터럴을 쓰는 코드 전부가 함께 바뀐다. **문자열 풀이라는 최적화가 성립하는 전제가 불변성**이다 → [[string-comparison]] · [[constant-pool]]

**그리고 해시 기반 저장소의 키로 안전해진다.** 일주일 전 회차에서 `Objects.hash(age, name, working)` 로 해시코드를 만든 뒤 「넣고 나서 필드를 바꾸면 넣은 자리를 다시 찾을 수 없다」는 문제를 만났다. `String` 을 키로 쓸 때 그 문제가 안 생기는 이유가 여기 있다 — **바꿀 방법 자체가 없어서** 넣은 뒤에 해시코드가 변할 수 없다 → [[hash-code]] · [[hash-based-collection]]

**설계 판단으로 보면 「막는 것」이 「지키는 것」보다 싸다.** 가변 객체를 안전하게 쓰려면 누가 언제 고치는지를 계속 지켜야 하고, 불변이면 지킬 일이 없어진다 → [[encapsulation]]

## 경계와 오해

- **불변 ≠ 변수를 바꿀 수 없다** — 가장 자주 걸리는 자리다. `s1 = s1.concat("!")` 는 잘 동작한다. 바뀌지 않는 것은 **인스턴스**이고 변수는 새 인스턴스의 주소로 갈아 탈 수 있다. 「String 은 못 바꾼다」로 외우면 이 코드가 왜 되는지 설명되지 않는다 → [[variable]] · [[object-reference]]
- **불변 ≠ `final`** — `final String s` 는 **변수의 재대입**을 막고, 불변은 **인스턴스의 내용**을 막는다. 축이 다르므로 네 조합이 다 존재한다 — `final StringBuffer` 는 재대입은 막히지만 내용은 바뀌고, 그냥 `String` 은 재대입은 되지만 내용은 안 바뀐다.
- **돌려받은 값을 버리면 아무 일도 일어나지 않는다** — `s1.replace('l', 'x');` 만 쓰면 새 문자열이 생겨서 바로 버려지고 `s1` 은 그대로다. **오류도 경고도 나지 않는다.** 필기가 `replace`·`concat` 의 결과를 매번 변수에 받아 두는 것이 우연이 아니라 이 성질 때문이고, 가변 객체(`buf.replace(...)`)에서는 받지 않아도 되므로 **두 스타일이 섞이면 한쪽이 조용히 실패한다** → [[string-builder]]
- **불변이라고 복사가 필요 없는 것은 아니다 — 복사가 무의미한 것이다** — 사본과 원본을 구별할 방법이 없으므로 복사하는 코드가 낭비다. `String.clone()` 이 없는 것도 같은 이유다 → [[object-cloning]]
- **바꿀 때마다 인스턴스가 늘어난다** — 불변의 대가다. 문자열을 반복해서 이어 붙이면 중간 결과가 전부 쓰레기로 남는다. 그것을 피하려고 존재하는 것이 가변 버퍼다 → [[garbage-collection]] · [[string-builder]]
- **원소가 불변이어도 담는 그릇은 가변일 수 있다** — `String[]` 은 칸을 바꿀 수 있는 가변 배열이고 칸에 든 문자열만 불변이다. 「문자열 배열이니 안전하다」가 여기서 깨진다 → [[array]]

## 함께 보는 개념

- [[string-builder]] — 같은 일을 가변으로 하는 쪽
- [[string-comparison]] — 불변이라서 공유할 수 있는 구조
- [[object-reference]] — 새 인스턴스가 나온 것을 확인하는 수단
- [[defensive-copy]] — 가변 객체에서 필요해지는 대비
- [[array-copy]] — 그 사본을 만드는 표준 도구
- [[hash-code]] — 키가 불변이어야 하는 이유
- [[hash-based-collection]] — 그 성질을 요구하는 저장소
- [[object-cloning]] — 복사가 의미를 갖는 조건
- [[garbage-collection]] — 늘어난 인스턴스의 운명
- [[encapsulation]] — 「지키기」와 「막기」가 갈리는 자리

## 출처

- [[2024-06-25-Day22]] — 「String 객체는 immutable로 한번 정해지면 데이터를 변경할 수 없다」를 `replace`·`concat` 의 반환값이 원본과 `==` 로 다르다는 것으로 확인하고, `StringBuffer`·`StringBuilder` 를 가변 객체로 나란히 놓아 대비했다. 같은 회차 1.2 의 `x1 == x2` 가 `true` 인 것도 `String.toString()` 이 불변이라 `this` 를 돌려줄 수 있기 때문이다
