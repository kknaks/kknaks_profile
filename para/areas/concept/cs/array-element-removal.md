---
type: concept
id: array-element-removal
title: 배열에서 요소 지우기
aliases:
  - 배열 요소 삭제
  - 배열 삭제
  - 요소 당기기
  - array element removal
  - 순회 중 삭제
up:
  - 2024-06-18-Day17
  - 2024-06-20-Day19
tags:
  - java
  - 자료구조
  - 알고리즘
  - 메모리
---

# 배열에서 요소 지우기

고정 크기 배열에서 중간 요소를 없애는 것. 배열은 칸을 뺄 수 없으므로 **뒤를 앞으로 당기고 · 개수를 줄이고 · 남은 마지막 칸을 비운다.** 세 가지가 다 있어야 끝난다.

## 정의

```java
for (int i = index + 1; i < size; i++) {
  arr[i - 1] = arr[i];          // 1. 뒤를 앞으로 한 칸씩 당긴다
}
arr[--size] = null;             // 2. 개수를 줄이고  3. 그 자리를 비운다
```

세 단계가 각각 다른 일을 한다.

| 단계 | 빠뜨리면 |
|---|---|
| 당기기 | 지운 자리에 옛 값이 남아 목록에 구멍이 생긴다 |
| 개수 줄이기 | 순회가 지운 것을 계속 센다 |
| 마지막 칸 비우기 | 마지막 요소가 두 칸에 남는다 |

**개수만 줄여도 프로그램은 정상으로 보인다** — 순회가 `size` 까지만 도니까. 그래서 `null` 을 넣는 줄이 왜 있는지가 가장 먼저 흐려진다 → 「왜 중요한가」

## 사용 예시

이 필기는 같은 코드를 세 군데에 썼다 — 회원 삭제, 프로젝트 삭제, 팀원 삭제.

```java
// UserCommand.deleteUser — 받는 것이 「번호」다
for (int i = userNo; i < userLength; i++) {
  users[i - 1] = users[i];
}
userLength--;
users[userLength] = null;
```

```java
// Project.deleteMember — 받는 것이 「인덱스」다
public void deleteMember(int index) {
  for (int i = index + 1; i < memberSize; i++) {
    users[i - 1] = users[i];
  }
  users[--memberSize] = null;
}
```

**루프 시작값이 다른 것이 실수가 아니다.** 앞은 1부터 세는 번호를 받고 뒤는 0부터 세는 인덱스를 받으므로 `userNo` 와 `index + 1` 이 같은 칸을 가리킨다 → [[one-based-numbering]]

### 삭제하며 순회하면 역순으로 돈다

팀원 삭제는 하나씩 물어보며 지운다. 순회와 삭제가 같은 루프 안에서 일어난다.

```java
static void deleteMembers(Project project) {
  for (int i = project.getMemberSize() - 1; i >= 0; i--) {
    User user = project.getMember(i);
    String str = Prompt.input("팀원(%s) 삭제?", user.getName());
    if (str.equalsIgnoreCase("y")) {
      project.deleteMember(i);
      System.out.printf("'%s' 팀원을 삭제합니다.", user.getName());
    } else {
      System.out.printf("'%s' 팀원을 유지합니다.", user.getName());
    }
  }
}
```

**`i` 가 거꾸로 내려간다.** 정순으로 돌면 `i` 번을 지운 순간 뒤가 한 칸 당겨져 **다음 요소가 `i` 번으로 올라오는데** 루프는 `i + 1` 로 가므로 한 명을 묻지도 않고 지나친다. 게다가 종료 조건인 `getMemberSize()` 도 같이 줄어든다. 역순으로 돌면 당겨지는 것이 **이미 지나온 뒤쪽**이라 남은 인덱스가 흔들리지 않고, 종료 조건이 `i >= 0` 이라 크기 변화에 영향받지 않는다 → [[for-loop]]

### 시작값을 계산할 수 없게 되면 되찾아 와야 한다

번호가 위치였을 때는 루프 시작값이 그냥 `userNo` 였다. 번호가 데이터의 필드로 옮겨 간 다음 회차에서는 **그 계산이 불가능해진다** → [[surrogate-key]]

```java
// 앞 회차 — 3번 회원은 인덱스 2 에 있고, 당길 것은 인덱스 3 부터다
for (int i = userNo; i < userLength; i++) {
  users[i - 1] = users[i];
}
```

```java
// 이 회차 — 3번 회원이 어디 있는지 모르므로 먼저 찾는다
int index = indexOf(user);
for (int i = index + 1; i < userLength; i++) {
  users[i - 1] = users[i];
}
users[--userLength] = null;
```

**당기기·개수 줄이기·`null` 넣기 세 단계는 한 글자도 바뀌지 않았다.** 바뀐 것은 앞에 한 줄이 붙은 것뿐이고, 그 한 줄이 배열을 한 번 더 훑는다 → [[linear-search]]

필기가 이 변경을 주석으로 남겨 두었다 — 「`userNo`가 아닌 `index+1`로 시작」. `index + 1` 이라는 형태는 전날 `Project.deleteMember(int index)` 에서 이미 쓰던 것이다. **인덱스를 받는 삭제와 번호를 받는 삭제가 따로 있던 것이, 이제 번호를 받아 인덱스로 바꾼 뒤 인덱스 쪽 형태로 도는 하나가 되었다** → [[one-based-numbering]]

그리고 이 코드가 `UserList` 로 옮겨지며 **지운 인스턴스를 돌려주게 된다.**

```java
public static User delete(int userNo) {
  User deleteUser = findByNo(userNo);
  if (deleteUser == null) {
    return null;
  }
  int index = indexOf(deleteUser);
  ...
  return deleteUser;                        // 배열에서 빠진 인스턴스는 아직 살아 있다
}
```

`users[--userLength] = null` 로 배열의 연결은 끊겼지만 지역변수가 그 인스턴스를 잡고 있으므로 **호출한 쪽이 이름을 찍어 볼 수 있다.** 「지웠다」가 곧 「사라졌다」가 아니라는 것이 여기서 코드로 드러난다 → [[object-reference]] · [[garbage-collection]]

## 왜 중요한가

**「지웠다」가 세 가지 상태를 동시에 맞추는 일이라는 것이 드러난다.** 배열은 크기가 고정이라 칸 자체를 없앨 수 없고([[array]]), 실제로 지워지는 것은 값이 아니라 **자리의 의미**다. 개수만 줄이면 순회 결과는 맞지만 마지막 칸의 레퍼런스가 남아 그 인스턴스가 회수되지 않는다 — `null` 대입이 그 줄을 끊는 일이다 → [[garbage-collection]] · [[object-reference]]

**순회 중 삭제가 왜 위험한지가 여기서 설명된다.** 인덱스로 도는 루프는 「지금 몇 번째」를 밖에서 세고 있는데, 삭제는 그 번호가 가리키는 대상을 바꿔 버린다. 컬렉션의 `ConcurrentModificationException` 이 막으려는 것이 정확히 이 상황이고, **배열에서는 아무도 막아 주지 않아 조용히 건너뛴다.**

**그리고 삭제 비용이 위치에 달려 있다는 것을 처음 만난다.** 마지막을 지우면 당길 것이 없고 앞을 지우면 거의 전부를 옮긴다. 배열이 인덱스 접근에는 빠르고 중간 삭제에는 느린 이유가 이 루프 하나에 다 들어 있다.

## 경계와 오해

- **`null` 대입 ≠ 지우기** — 그 칸만 비고 뒤는 그대로여서 목록 순회에 구멍이 남는다. 당기기와 짝이어야 의미가 있다.
- **개수 줄이기 ≠ 지우기** — 반대쪽 실수다. `size--` 만 하면 순회 결과가 맞아서 **잘 동작하는 것처럼 보인다.** 마지막 값이 배열에 남아 있고 다음 등록이 그 자리를 덮으므로 증상도 안 나타난다. 테스트를 통과하는 미완성이라 발견이 늦다.
- **`arr[--size] = null` 의 순서가 중요하다** — 감소가 먼저다. `size` 가 3이면 `arr[2]` 를 비운다. `arr[size--] = null` 로 쓰면 `arr[3]`(쓰지 않는 칸)을 건드리고 마지막 값은 그대로 남는다. 한 글자 위치가 두 동작을 가른다 → [[increment-operator]]
- **정순으로 지우며 도는 코드는 컴파일된다** — 문법 오류도 예외도 없고 **한 개씩 건너뛴 결과만** 남는다. 「y 를 눌렀는데 안 지워졌다」가 아니라 「묻지도 않고 지나간 팀원이 있다」로 나타나므로 원인을 찾기 어렵다.
- **역순 순회는 삭제 전용 요령이 아니다** — 이유는 「뒤에서 앞으로 가면 남은 인덱스가 안 흔들린다」이고, 그래서 **삽입에도 같은 논리가 적용된다**(삽입은 정순이 안전하다). 「삭제는 역순」으로만 외우면 왜 그런지가 남지 않는다.
- **순서를 지켜야 할 때만 당긴다** — 순서가 상관없으면 마지막 요소를 지운 자리에 옮기는 방법이 있고 그러면 옮기는 것이 한 번이다. 대신 번호가 뒤바뀌므로 목록 번호를 쓰는 이 프로그램에서는 못 쓴다 → [[crud]]
- **삭제가 번호를 다시 매긴다** — 3번을 지운 뒤 다시 3번을 지우면 원래 4번이 사라진다. 목록에서 본 번호를 기억해 연달아 지우는 것이 위험한 이유다. **다시 매겨지는 것은 인덱스이지 데이터가 아니므로**, 번호를 데이터가 들고 있으면 이 위험이 없어진다 → [[one-based-numbering]] · [[surrogate-key]]
- **인덱스를 되찾는 것은 지우기의 일부가 아니다** — `indexOf` 는 「어떻게 지우나」와 아무 상관이 없고, **번호로 위치를 계산할 수 없어서** 붙은 앞단계다. 세 단계에 네 번째를 더한 것으로 세면, 저장소가 위치를 알려 주는 구조로 바뀌었을 때(리스트·맵) 무엇이 사라지는지가 흐려진다 → [[linear-search]]
- **`indexOf` 가 `-1` 을 줄 수 있다는 것을 이 코드는 검사하지 않는다** — `findByNo` 로 찾은 인스턴스를 그대로 넘기므로 항상 찾는다. 안전이 **부르는 순서**에 걸려 있고, `delete` 를 다른 데서 쓰면 `for (int i = 0; ...)` 로 시작해 **첫 요소를 지워 버린다.**
- **지운 인스턴스를 돌려주는 것은 「덜 지운 것」이 아니다** — 배열에서 끊는 것과 인스턴스를 없애는 것은 다른 일이라, 반환값으로 잡고 있는 동안 그것은 정상적으로 살아 있다. `null` 대입이 끊는 것은 **배열 칸에서 시작하는 참조 하나**뿐이다 → [[object-reference]] · [[garbage-collection]]
- **당긴 뒤에도 배열 길이는 그대로다** — `arr.length` 는 `MAX_SIZE` 로 남아 있고 줄어드는 것은 개수 변수뿐이다. `length` 와 「지금 몇 개 들었나」를 같은 것으로 읽으면 삭제가 아무 일도 안 한 것처럼 보인다 → [[default-initialization]]

## 함께 보는 개념

- [[array]] — 크기가 고정이라는 전제
- [[one-based-numbering]] — 번호를 받는 삭제와 인덱스를 받는 삭제
- [[crud]] — 이 코드가 놓이는 자리
- [[object-reference]] — `null` 대입이 끊는 것
- [[garbage-collection]] — 끊긴 인스턴스의 운명
- [[increment-operator]] — `--size` 의 위치가 정하는 것
- [[for-loop]] — 역순 순회의 문법
- [[default-initialization]] — 빈 칸이 `null` 인 이유
- [[surrogate-key]] — 루프 시작값을 계산할 수 없게 만든 변경
- [[linear-search]] — 인덱스를 되찾는 방법
- [[cohesion]] — 이 코드가 옮겨 간 클래스

## 출처

- [[2024-06-18-Day17]] — 회원·프로젝트·팀원 삭제를 만들며 배열에서 뒤 요소를 앞으로 당기고 개수를 줄이고 마지막 칸에 `null` 을 넣는 것을 실습으로 배웠다. 팀원 삭제는 순회 중에 지워야 해서 `getMemberSize() - 1` 부터 역순으로 도는 루프가 되었다
- [[2024-06-20-Day19]] — 번호가 데이터의 필드가 되면서 루프 시작값을 계산할 수 없게 되어, `indexOf` 로 위치를 되찾은 뒤 `index + 1` 부터 당기는 형태가 되었다. 당기기·개수 줄이기·`null` 넣기 세 단계는 그대로이고 앞에 탐색 한 줄이 붙었다. 이 코드가 `UserList.delete` 로 옮겨지며 지운 인스턴스를 반환값으로 돌려주게 된 것도 이 자리다
