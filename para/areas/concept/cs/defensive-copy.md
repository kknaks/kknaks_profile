---
type: concept
id: defensive-copy
title: 방어적 복사 (내부 배열을 그대로 내주지 않기)
aliases:
  - 방어적 복사
  - defensive copy
  - 복사 반환
  - 얕은 복사
  - shallow copy
  - toArray
up:
  - 2024-06-20-Day19
  - 2024-06-25-Day22
tags:
  - 설계
  - java
  - 캡슐화
  - 자료구조
---

# 방어적 복사 (내부 배열을 그대로 내주지 않기)

저장소를 가진 클래스가 그것을 밖에 보여 줄 때 **원본 배열이 아니라 새로 만든 사본을 준다.** 받은 쪽이 사본을 어떻게 만져도 안쪽은 흔들리지 않는다.

## 정의

```java
public static User[] toArray() {
  User[] arr = new User[userLength];        // 든 개수만큼 새 배열을 만들고
  for (int i = 0; i < arr.length; i++) {
    arr[i] = users[i];                     // 하나씩 옮겨 담아
  }
  return arr;                              // 사본을 내준다
}
```

한 줄에서 **두 가지 일**이 일어난다.

| | 원본을 그대로 주면 | 사본을 만들어 주면 |
|---|---|---|
| 구조 변경 | 밖에서 순서를 바꾸고 덮어쓸 수 있다 | 사본만 바뀐다 |
| 길이 | `MAX_SIZE`(10) — 뒤는 `null` | 든 개수 — 빈 칸이 없다 |
| 부르는 쪽이 알아야 하는 것 | 개수 변수를 따로 받아야 한다 | 없다 — `length` 가 답이다 |

**길이를 맞춰 주는 쪽이 실제로 더 크게 바뀌는 부분**이다. 유효한 개수가 사본 안에 들어가서 밖으로 나갈 필요가 없어진다 → [[array]] · [[cohesion]]

## 사용 예시

목록 출력이 **인덱스를 완전히 잃는다.**

```java
private static void listUser() {
  System.out.println("번호 이름 이메일");
  for (User user : UserList.toArray()) {
    System.out.printf("%d %s %s\n", user.getNo(), user.getName(), user.getEmail());
  }
}
```

전날까지는 이랬다.

```java
for (int i = 0; i < userLength; i++) {                     // 개수 변수를 알아야 하고
  User user = users[i];                                     // 배열을 직접 만지고
  System.out.printf("%d %s %s\n", (i + 1), ... );           // 번호를 계산해야 했다
}
```

세 가지가 한꺼번에 사라진 것이고 **셋이 같은 이유로 사라진 것이 아니다.** 개수 변수와 배열 접근은 `toArray()` 가 없애 주었고, 인덱스 자체는 **번호가 데이터 안으로 들어가서** 쓸 일이 없어졌다. 그 둘이 겹쳐서야 `for-each` 로 갈 수 있다 — 한쪽만 됐다면 인덱스가 여전히 필요했다 → [[surrogate-key]] · [[for-loop]]

그리고 전날의 `getUsers()` 와 나란히 놓으면 결정이 갈린다.

```java
public User[] getUsers() { return this.users; }             // 전날 — 원본을 그대로 준다
public static User[] toArray() { ...; return arr; }         // 이 회차 — 사본을 준다
```

앞의 것은 `private final User[] users` 를 밖에서 만질 수 있게 열어 놓았고, 뒤의 것은 `private static final User[] users` 를 끝까지 안에 둔다. **같은 「배열을 보여 주기」인데 하나는 구멍이고 하나는 아니다** → [[encapsulation]] · [[object-reference]]

## 왜 중요한가

**`private` 이 배열에서 새는 것을 막는 유일한 방법이다.** 접근 지정자는 **이름**을 가릴 뿐이라 그 이름이 가리키던 주소를 내주면 아무 효력이 없다. `private` 을 붙였는데 밖에서 내용이 바뀌는 상황이 여기서 끝난다 → [[access-modifier]] · [[call-by-value]]

**저장 방식을 바꿀 여지가 생긴다.** 안에서 배열을 쓰든 리스트를 쓰든 `toArray()` 가 배열을 만들어 주면 부르는 쪽은 한 글자도 안 바뀐다. `UserCommand` 가 `users`·`userLength`·`MAX_SIZE` 를 하나도 모르는 상태가 되었고, **모르는 것은 바뀌어도 영향받지 않는다.**

**그리고 개수 변수가 밖으로 새지 않는다.** 전날의 목록 출력은 `userLength` 를 조건으로 썼기 때문에 그 변수가 같은 클래스 안에 있어야 했다. 사본이 자기 `length` 로 답하면 그 결합이 사라진다 — 클래스를 둘로 쪼갤 수 있게 된 조건 중 하나가 이것이다 → [[cohesion]]

## 경계와 오해

- **복사 루프를 손으로 쓸 필요는 없었다** — 닷새 뒤 회차에서 `Arrays.copyOf`·`Arrays.copyOfRange` 를 배운다. `new` + `for` 세 줄이 `return Arrays.copyOf(users, userLength);` 한 줄이 되고, **길이를 든 개수로 맞춰 주는 것까지 그대로 된다.** 다만 얕은 복사라는 성질은 그대로이므로 아래 항목은 표준 메서드로 바꿔도 남는다 → [[array-copy]]
- **복사가 필요한 이유는 배열이 가변이기 때문이다** — 원소가 불변인 `String[]` 이었다면 「밖에서 내용을 고친다」의 절반이 사라진다. 막아야 할 것이 **그릇의 가변성**인지 **원소의 가변성**인지가 갈리고, 이 코드에서는 둘 다 가변이라 둘 다 문제다 → [[immutability]]
- **방어적 복사 ≠ 깊은 복사** — 새로 만든 것은 **배열뿐**이고 칸에 든 것은 같은 `User` 인스턴스의 주소다. `UserList.toArray()[0].setName("x")` 는 원본 회원의 이름을 진짜로 바꾼다. 막은 것은 「목록의 구조를 바꾸는 것」이고 「회원의 내용을 바꾸는 것」은 그대로 열려 있다 → [[object-reference]]
- **사본을 고쳐도 반영되지 않는다** — 막은 것의 뒷면이다. 받은 배열에 `arr[3] = newUser` 를 넣어도 `UserList` 는 모르고, **오류도 나지 않는다.** 「목록을 받아 왔으니 여기에 넣으면 되겠지」가 조용히 실패하므로, 넣는 일은 반드시 `add` 를 거쳐야 한다는 것이 코드에 드러나 있지 않다.
- **복사가 무료가 아니다** — 목록을 찍을 때마다 배열이 하나 새로 생기고 다 쓰면 버려진다. 부를 때마다 O(n) 이고 쓰레기가 쌓인다. 10건짜리 CLI 에서는 안 보이지만 **「읽기만 하는데 왜 메모리를 쓰나」**가 나중에 문제가 되는 자리다 → [[garbage-collection]]
- **빈 목록에는 길이 0 배열이 온다 — `null` 이 아니다** — 그래서 `for-each` 가 0바퀴 돌고 부르는 쪽에 `null` 검사가 필요 없다. 같은 클래스의 `findByNo` 는 못 찾았을 때 `null` 을 준다. **「없음」을 두 방식으로 표현하고 있는 것**이고, 둘 다 맞지만 규칙이 하나가 아니라는 것은 기억해야 한다 → [[linear-search]]
- **루프 조건이 `arr.length` 인 것이 판단으로 남지 않았다** — `i < arr.length` 와 `i < userLength` 는 이 코드에서 값이 같아 둘 다 돌아간다. 사본 기준으로 도는 쪽이 맞지만 **왜 맞는지가 코드에 안 남아** 있어서, 나중에 `arr` 을 크게 잡는 변경이 들어오면 조건이 조용히 어긋난다.
- **`toArray` 라는 이름은 자바 컬렉션의 관례다** — `List.toArray()` 와 같은 이름이라 나중에 안쪽을 `List` 로 바꿔도 이름을 그대로 쓸 수 있다. 「배열로 바꿔 준다」가 아니라 **「내부를 배열 모양으로 내보낸다」**로 읽는 것이 맞다.
- **`static` 이므로 사본도 하나의 저장소에서 나온다** — 회원 목록은 프로그램 전체에 한 벌이고 `toArray()` 는 그 한 벌을 복사한다. 여러 목록을 굴리는 문제와는 아무 상관이 없다 → [[static-member]]

## 함께 보는 개념

- [[encapsulation]] — 배열 getter 가 열어 두었던 구멍
- [[object-reference]] — 사본의 칸에 든 것이 무엇인가
- [[access-modifier]] — 이름만 가리는 장치
- [[call-by-value]] — 주소가 복사되어 넘어가는 구조
- [[array]] — 길이와 든 개수가 다른 저장소
- [[for-loop]] — 사본이 열어 준 `for-each`
- [[surrogate-key]] — 인덱스를 버릴 수 있게 만든 나머지 절반
- [[cohesion]] — 개수 변수를 안에 남기는 것
- [[garbage-collection]] — 버려지는 사본의 운명
- [[static-member]] — 사본이 나오는 저장소의 성격
- [[array-copy]] — 같은 일을 하는 표준 메서드
- [[immutability]] — 복사가 필요 없어지는 조건

## 출처

- [[2024-06-20-Day19]] — 클래스를 쪼개며 `UserList.toArray()` 를 만들어 유효한 개수만큼 새 배열에 옮겨 담아 돌려주고, 그 결과 목록 출력이 `for (User user : UserList.toArray())` 로 바뀌었다. 전날 `Project.getUsers()` 가 원본을 그대로 내주던 것과 같은 자리에서 다른 결정을 한 것이고, `userLength`·`MAX_SIZE` 가 `UserList` 안에만 남게 된 근거도 여기다
- [[2024-06-25-Day22]] — `Arrays.copyOf`·`Arrays.copyOfRange` 를 배우며 이 노트의 복사 루프가 표준 메서드 한 줄로 대체될 수 있다는 것이 드러났다. 같은 회차에서 `String` 이 불변이라 사본을 만들 이유가 없다는 대비까지 나오므로, **방어적 복사가 필요한 조건이 「가변인가」**라는 것이 여기서 정리된다
