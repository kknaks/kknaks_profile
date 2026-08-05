---
type: concept
id: string-builder
title: 가변 문자열 버퍼 (StringBuffer · StringBuilder)
aliases:
  - StringBuilder
  - StringBuffer
  - string builder
  - string buffer
  - 문자열 버퍼
  - 가변 문자열
up:
  - 2024-06-25-Day22
tags:
  - java
  - 문자열
  - 성능
  - 동기화
---

# 가변 문자열 버퍼 (StringBuffer · StringBuilder)

문자열을 **원본 그대로 고쳐 쓰는** 두 클래스. `String` 이 [[immutability]] 를 택한 대가로 잃은 「그 자리에서 바꾸기」를 돌려받는 자리이고, 둘의 차이는 **여러 스레드가 동시에 만질 때뿐**이다.

## 정의

`String` 과 같은 이름의 메서드를 부르는데 결과가 다르다.

```java
StringBuffer buf = new StringBuffer("Hello");
System.out.println(buf); // Hello
System.out.println(buf.hashCode()); //498931366

buf.replace(2, 4, "xxxx");// 원본을 바꾼다.
System.out.println(buf); //Hexxxxo
System.out.println(buf.hashCode()); //498931366
```

**내용은 `Hello` → `Hexxxxo` 로 바뀌었는데 해시코드는 그대로다.** 인스턴스가 바뀐 것이 아니라 인스턴스 **안의 내용**이 바뀌었다는 증거다. 같은 코드를 `String` 으로 쓰면 반환값이 새 인스턴스라 원본은 `Hello` 로 남는다.

`StringBuilder` 도 같은 코드가 그대로 동작한다. 갈리는 것은 하나다.

| | 동기화 | 쓰는 자리 |
|---|---|---|
| `StringBuffer` | 한다 | 멀티스레드 — 순서를 정해서 인스턴스에 접근 |
| `StringBuilder` | 안 한다 | 단일 스레드 — 순차적으로 접근 |

동기화는 **여러 스레드가 같은 버퍼를 동시에 고치는 것을 막는** 장치다. 막을 일이 없는 곳에서는 그 검사가 순수한 비용이므로, 단일 스레드에서는 `StringBuilder` 를 쓴다.

## 사용 예시

필기의 두 예제는 같은 코드를 클래스 이름만 바꿔 두 번 쓴 것이다.

```java
StringBuilder strBuilder = new StringBuilder("Hello");
strBuilder.replace(2, 4, "xxxx");// 원본을 바꾼다.
System.out.println(strBuilder); // Hexxxxo
```

**바꿔도 코드가 한 글자도 안 달라진다는 것이 이 예제의 요점**이다. 두 클래스는 같은 메서드 집합을 갖고 있어서 서로 갈아 끼울 수 있고, 그래서 「어느 쪽을 쓸까」가 기능이 아니라 **환경**의 문제가 된다.

## 왜 중요한가

**불변의 대가를 치르지 않고 문자열을 만들 수 있다.** `String` 으로 이어 붙이면 중간 결과마다 인스턴스가 하나씩 생겨 버려진다. 버퍼는 하나를 잡아 두고 그 안을 고치므로 인스턴스가 늘지 않는다 → [[immutability]] · [[garbage-collection]]

**그리고 동기화가 무료가 아니라는 것을 처음 만나는 자리다.** `StringBuffer` 가 먼저 있었고 `StringBuilder` 가 나중에 나왔다 — 「안전하게 만들어 두면 좋다」가 아니라 **안전이 필요 없는 곳에서는 비용**이라는 판단이 클래스 두 개로 갈라져 있는 것이다.

## 경계와 오해

- **「비동기화」 ≠ 비동기** — 필기가 `StringBuilder` 를 「비동기화로 단일 스레드 환경에서」라고 적었는데, **동기화를 하지 않는다(unsynchronized)**는 뜻이고 비동기(asynchronous) 실행과는 아무 관계가 없다. 콜백이나 `await` 이야기로 읽으면 완전히 다른 곳으로 간다.
- **`StringBuffer` 를 쓰면 멀티스레드에서 안전한 것이 아니다** — 메서드 하나하나가 안전할 뿐이고, `if (buf.length() > 0) buf.replace(...)` 처럼 **두 번 부르는 사이**는 보호되지 않는다. 「동기화된 클래스를 썼으니 됐다」가 가장 흔한 오해다.
- **해시코드와 `equals` 를 재정의하지 않았다** — 위 예제의 해시코드가 안 바뀐 것은 **내용을 안 보는 기본 구현**이라서다. 그래서 내용이 같은 두 버퍼도 `equals` 가 `false` 이고, 해시 기반 저장소의 키로 쓰면 못 찾는다. **재정의하지 않은 것이 옳은 선택**이다 — 가변인 것을 내용 기준으로 해싱하면 넣은 뒤에 자리를 잃는다. 내용을 비교하려면 `toString()` 으로 `String` 을 얻어 비교한다 → [[hash-code]] · [[object-equality]] · [[hash-based-collection]]
- **필기의 해시코드 값 `498931366` 이 세 번 다 같은 것은 옮겨 적은 것이다** — `buf` 와 `strBuilder` 는 서로 다른 인스턴스이므로 실제로는 다른 값이 나온다. **「변경 전후가 같다」는 요점은 맞고, 「두 클래스가 같다」로 읽으면 틀린다.**
- **가변 ≠ 무한히 자란다** — 안쪽은 결국 고정 크기 배열이고 꽉 차면 더 큰 것으로 옮긴다. 「그 자리에서 바꾼다」가 항상 복사 없이 된다는 뜻은 아니다 → [[dynamic-array]]
- **`replace(2, 4, ...)` 의 범위는 끝을 포함하지 않는다** — `"Hello"` 의 2·3번(`ll`)만 바뀌어 `Hexxxxo` 가 된다. 같은 회차 1.5 의 `Arrays.copyOfRange` 와 같은 규칙이고, 필기는 그쪽에서 범위를 반대로 적었다 → [[array-copy]]
- **`String` 을 쓰지 말라는 뜻이 아니다** — 한 번 만들어 두고 읽기만 하는 값은 불변이 낫다. 버퍼는 **만드는 과정**에 쓰는 도구다.

## 함께 보는 개념

- [[immutability]] — 이 클래스들이 존재하는 이유
- [[string-comparison]] — 불변 쪽이 얻는 공유
- [[hash-code]] — 재정의하지 않은 것이 드러나는 자리
- [[object-equality]] — 내용 비교가 안 되는 이유
- [[hash-based-collection]] — 가변 키가 위험한 구조
- [[dynamic-array]] — 버퍼 안쪽이 크기를 늘리는 방식
- [[array-copy]] — 같은 반개구간 규칙
- [[garbage-collection]] — 중간 인스턴스가 쌓이는 문제

## 출처

- [[2024-06-25-Day22]] — `StringBuffer`·`StringBuilder` 의 `replace()` 가 원본을 바꾸고 해시코드가 변하지 않는 것을 확인했다. 「두 클래스의 차이는 동시성이다 / Buffer은 멀티스레드 환경에서 순서를 정해서 인스턴스에 접근한다 / Builder는 비동기화로 단일 스레드 환경에서 순차적으로 인스턴스에 접근한다」가 두 클래스를 가르는 기준으로 배운 전부다
