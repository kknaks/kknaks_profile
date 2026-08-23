---
type: concept
id: linear-search
title: 선형 탐색 (앞에서부터 하나씩 비교하기)
aliases:
  - 선형 탐색
  - 순차 탐색
  - linear search
  - sequential search
  - 순차 검색
  - 훑어서 찾기
up:
  - 2024-06-20-Day19
tags:
  - 알고리즘
  - 자료구조
  - java
  - 성능
---

# 선형 탐색 (앞에서부터 하나씩 비교하기)

저장된 것을 **처음부터 하나씩 조건과 맞춰 보고, 맞는 것을 만나면 그 자리에서 멈춘다.** 끝까지 못 만나면 「없다」를 값으로 돌려준다.

## 정의

같은 루프가 **무엇을 돌려주느냐**로 두 형태로 갈린다.

```java
public static User findByNo(int userNo) {        // 찾은 것을 돌려준다
  for (int i = 0; i < userLength; i++) {
    User user = users[i];
    if (user.getNo() == userNo) {
      return user;                               // 만나면 즉시 나간다
    }
  }
  return null;                                   // 끝까지 못 만났다
}

public static int indexOf(User user) {           // 찾은 위치를 돌려준다
  for (int i = 0; i < userLength; i++) {
    if (users[i] == user) {
      return i;
    }
  }
  return -1;                                     // 끝까지 못 만났다
}
```

네 부분으로 되어 있고, 셋은 늘 같고 하나만 바뀐다.

| 부분 | 이 코드 | 바뀌는가 |
|---|---|---|
| 순회 | `for (int i = 0; i < userLength; i++)` | 저장소가 정한다 |
| **비교 조건** | `user.getNo() == userNo` · `users[i] == user` | **여기만 바뀐다** |
| 성공 | `return user` · `return i` | 무엇을 원하는지가 정한다 |
| 실패 | `return null` · `return -1` | 반환 타입이 정한다 |

**「어떻게 찾는가」는 다 같고 「무엇을 같다고 볼 것인가」만 다르다** → [[for-loop]] · [[array]]

## 사용 예시

이 필기는 **직접 접근을 탐색으로 바꾸는 과정**을 그대로 남겼다. 전날의 조회는 계산이었다.

```java
// 전날 — 번호가 위치였으므로 검사하고 계산한다
if (userNo < 1 || userNo > userLength) {
  System.out.println("없는 회원입니다.");
  return;
}
User user = users[userNo - 1];
```

```java
// 이 회차 — 번호가 데이터 안으로 들어가서 훑어야 한다
User user = findByNo(userNo);
if (user == null) {
  System.out.println("없는 회원입니다.");
  return;
}
```

필기가 그 변경을 코드 주석으로 적어 뒀다 — 「`if (범위)` 탐색 -> `for` 문 탐색」. 번호를 위치에서 떼어낸 대가로 **한 번에 닿던 것이 훑는 일이 되었다** → [[surrogate-key]]

바뀐 것은 비용만이 아니다. **검사와 조회가 한 메서드로 합쳐졌다.** 전날에는 `viewUser`·`updateUser`·`deleteUser` 세 곳이 각자 범위 검사를 갖고 있었고 그래서 세 곳이 같이 틀릴 수 있었는데, 이제 그 세 곳이 전부 같은 두 줄이다 → [[one-based-numbering]] · [[conditional-flattening]]

삭제는 두 탐색을 **연달아** 쓴다.

```java
public static User delete(int userNo) {
  User deleteUser = findByNo(userNo);        // 1) 번호로 인스턴스를 찾고
  if (deleteUser == null) {
    return null;
  }
  int index = indexOf(deleteUser);           // 2) 그 인스턴스로 위치를 찾는다
  for (int i = index + 1; i < userLength; i++) {
    users[i - 1] = users[i];
  }
  users[--userLength] = null;
  return deleteUser;
}
```

**두 번 훑는다.** 첫 루프가 이미 `i` 를 알고 있었는데 인스턴스만 돌려주고 위치를 버렸기 때문이다 → [[array-element-removal]]

## 왜 중요한가

**식별자를 위치에서 떼어내면 탐색이 유일한 방법이 된다.** 「3번 회원」이 3번째 칸에 있다는 보장이 사라진 순간, 어디 있는지 아는 방법은 물어보는 것뿐이다. 정렬·이진 탐색·해시·DB 인덱스가 모두 **이 루프를 대신하려는 장치**이고, 그것들이 왜 필요한지는 이 루프를 한 번 써 보면 설명이 끝난다 → [[search-index]]

**비용이 개수에 비례한다는 것이 여기서 처음 문제가 된다.** 10건이면 최대 10번 비교이고 체감이 없다. 10만 건이면 목록 한 번 그리는 동안 10만 번을 돈다. **코드는 한 글자도 안 바뀌는데 데이터만 늘어서 느려지는** 첫 경험이 이 자리다.

**그리고 「없다」를 값으로 표현해야 한다.** 인스턴스를 돌려주는 쪽은 `null`, 위치를 돌려주는 쪽은 `-1` 이다. 둘 다 **정상 결과와 같은 타입에 섞여 오므로 부르는 쪽이 반드시 검사해야** 하고, 검사를 잊으면 실패가 그 자리가 아니라 한참 뒤에서 터진다 → [[object-reference]]

## 경계와 오해

- **선형 탐색 ≠ 전체 순회** — 찾으면 `return` 으로 즉시 나가므로 **평균은 절반**이다. 대신 **없는 것을 찾을 때는 항상 전부 본다** — 실패가 가장 비싸다. 「없는 번호를 넣었을 때 제일 오래 걸린다」는 것이 직관과 반대여서 성능을 잴 때 자주 빠진다.
- **`-1` 은 인덱스가 아니라 신호다** — 유효한 인덱스가 `0` 부터라서 남아 있는 값을 「없음」으로 쓴 것이다. 검사 없이 `users[indexOf(x)]` 하면 `ArrayIndexOutOfBoundsException` 이 된다. 팀원 추가 루프가 종료 값으로 `0` 을 쓴 것과 **같은 요령**이다 — 쓰이지 않는 값 하나를 골라 뜻을 얹는다 → [[one-based-numbering]]
- **이 코드의 `indexOf` 는 실패하지 않는다** — `delete` 는 `findByNo` 가 찾아 준 인스턴스를 그대로 넘기므로 배열에 반드시 있다. 그래서 `-1` 검사가 없고 **그 안전은 부르는 순서가 지켜 주는 것**이다. 이 메서드를 다른 곳에서 쓰는 날 그 전제가 조용히 깨진다.
- **`==` 탐색과 값 비교 탐색은 다른 것을 찾는다** — `indexOf` 는 `users[i] == user` 로 **같은 인스턴스**를 찾고, `findByNo` 는 `getNo()` 로 **같은 번호**를 찾고, 전날의 `contain` 은 `equals` 로 **같은 이름**을 찾았다. 세 「같다」가 다 다르므로, 「이름이 같은 다른 인스턴스」를 `indexOf` 에 넘기면 `-1` 이 온다 → [[object-reference]] · [[string-comparison]]
- **첫 번째 하나만 돌려준다** — 조건에 맞는 것이 둘 있어도 앞의 것에서 나간다. 번호가 유일하다는 전제가 깨지면(`setNo` 로 같은 번호를 넣으면) 뒤의 것은 **존재하는데 영원히 조회되지 않는다** → [[surrogate-key]]
- **`userLength` 까지만 돌아야 한다** — `users.length` 는 `MAX_SIZE`(10) 이고 그 뒤 칸은 `null` 이다. 조건을 `users.length` 로 잘못 쓰면 `user.getNo()` 에서 `NullPointerException` 이다. **저장소의 크기와 든 개수가 다르다**는 것이 탐색 조건에서 다시 걸린다 → [[default-initialization]]
- **탐색 메서드를 어디 두느냐가 따로 걸린다** — `findByNo`·`indexOf` 는 배열을 읽어야 하므로 배열을 가진 클래스에 있어야 한다. 필기 「High Cohesion」 절의 `ProjectList` 초안은 이 둘을 `private static` 으로 남겨 두었는데, 그러면 밖에서 부를 수 없어 분리한 의미가 사라진다. 「클래스 분리하기」 절의 `UserList` 에서 `public static` 이 되었다 → [[cohesion]] · [[access-modifier]]
- **한 번의 탐색으로 끝낼 수 있었다** — `findByNo` 가 인덱스를 돌려주면 `delete` 가 두 번 돌지 않는다. 그렇게 하지 않은 것은 **인덱스를 돌려주면 부르는 쪽이 다시 배열을 만져야** 하기 때문이다. 「무엇을 돌려줄까」가 비용과 캡슐화를 동시에 정하는 자리이고, 이 코드는 캡슐화를 골랐다 → [[encapsulation]]

## 함께 보는 개념

- [[surrogate-key]] — 탐색이 필요해진 원인
- [[for-loop]] — 이 순회의 문법
- [[array]] — 탐색 대상이 되는 저장소
- [[one-based-numbering]] — 직접 계산으로 닿던 이전 방식
- [[array-element-removal]] — 위치를 되찾아야 하는 쪽
- [[object-reference]] — `null` 로 「없음」을 알리는 것과 `==` 비교
- [[string-comparison]] — 「같다」의 또 다른 기준
- [[search-index]] — 이 루프를 대신하려는 장치
- [[crud]] — 조회·변경·삭제가 공유하는 앞부분
- [[cohesion]] — 탐색 메서드가 살아야 하는 클래스

## 출처

- [[2024-06-20-Day19]] — 식별 번호를 도입하면서 「`if (범위)` 탐색 -> `for` 문 탐색」으로 조회 방식을 바꾸고, 인스턴스를 돌려주는 `findByNo` 와 위치를 돌려주는 `indexOf` 두 형태를 만들었다. 삭제가 두 탐색을 연달아 부르며 같은 배열을 두 번 훑는 것, 그리고 범위 검사가 `null` 검사로 대체되며 조회·변경·삭제 세 곳이 같은 모양이 된 것도 이 자리다
