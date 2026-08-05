---
type: concept
id: dynamic-array
title: 가변 배열 (Dynamic Array)
aliases:
  - 가변 배열
  - 동적 배열
  - dynamic array
  - growable array
  - ArrayList
  - 배열 확장
  - grow
up:
  - 2024-06-25-Day22
  - 2024-06-26-Day23
  - 2024-07-08-Day30
tags:
  - java
  - 자료구조
  - 메모리
  - 성능
---

# 가변 배열 (Dynamic Array)

크기가 고정된 [[array]] 위에 **꽉 차면 더 큰 배열로 옮겨 담는 규칙**을 얹어, 밖에서 보면 무한히 늘어나는 것처럼 보이게 만든 구조. `ArrayList` 가 안에서 하고 있는 일이다.

## 정의

두 부분으로 되어 있다.

1. **배열과 「지금 몇 개 들었나」를 짝으로 들고 다닌다** (`list` · `size`)
2. **`size` 가 `list.length` 에 닿으면 늘린다**

늘리는 쪽이 `grow()` 다.

```java
private void grow() {
    int oldSize = list.length;
    int newSize = oldSize + (oldSize >> 1);
    Object[] arr = new Object[newSize];
    for (int i = 0; i < oldSize; i++) {
      arr[i] = list[i];
    }
    list = arr;
}
```

`oldSize + (oldSize >> 1)` 이 **1.5배**다 — `>> 1` 이 2로 나눈 것이므로 원래 크기에 그 절반을 더한다 → [[bit-shift]]

옮겨 담는 루프는 표준 메서드 한 줄로 대체된다.

```java
list = Arrays.copyOf(list, newSize);
```

→ [[array-copy]]

하루 뒤 회차의 `grow()` 는 **새 배열을 직접 만들고 옮기는 쪽만** 표준 메서드로 바꾼다.

```java
private void grow() {
    int oldSize = list.length;
    int newSize = oldSize + (oldSize >> 1);
    Object[] arr = new Object[newSize];
    System.arraycopy(list, 0, arr, 0, oldSize);   // for 루프가 이 한 줄이 되었다
    list = arr;
}
```

**`Arrays.copyOf` 와 `System.arraycopy` 는 다른 일을 한다** — 앞은 새 배열을 만들어 **돌려주고**, 뒤는 이미 있는 두 배열 사이에서 **옮기기만** 한다. 그래서 `new Object[newSize]` 세 줄이 그대로 남아 있다 → [[array-copy]]

## 사용 예시

넣는 쪽에서 「꽉 찼나」를 먼저 본다.

```java
public void add(Object obj) {
    if (size == list.length) {
      int oldSize = list.length;
      int newSize = oldSize + (oldSize >> 1);
      grow();
    }
    list[size++] = obj;
}
```

**`list[size++] = obj` 는 닷새 전 회차의 `users[userLength++] = user` 와 같은 줄이다.** 달라진 것은 그 앞에 붙은 `if` 하나이고, 그것이 「최대 10건」이라는 제약을 없앤다 → [[array]] · [[crud]]

`Object[]` 로 담는 것도 눈여겨볼 자리다. 무엇이든 넣을 수 있게 되었지만 꺼낼 때는 원래 타입으로 되돌려야 한다 → [[type-casting]] · [[object-class]]

### 하루 뒤, 이 클래스가 약속을 지키는 쪽이 된다

다음 회차에서 `ArrayList` 는 혼자 서 있는 클래스가 아니라 `List` 인터페이스의 구현이 되고, 메서드 여섯 개가 다 채워진다 → [[interface]]

```java
public class ArrayList extends AbstracList {
  private static final int MAX_SIZE = 100;
  private Object[] list = new Object[MAX_SIZE];
  ...
  @Override
  public Object[] toArray() {
    Object[] arr = new Object[size];
    System.arraycopy(list, 0, arr, 0, size);      // list.length 가 아니라 size 만큼
    return arr;
  }

  @Override
  public int indexOf(Object obj) {
    for (int i = 0; i < size; i++) {
      if (list[i].equals(obj)) {
        return i;
      }
    }
    return -1;
  }
}
```

**`toArray()` 가 `size` 만큼만 복사하는 것이 이 구조의 핵심을 그대로 드러낸다.** 안에 있는 배열은 100칸인데 밖에 내주는 것은 든 개수만큼이므로, **밖에서는 「꽉 찬 배열」로만 보인다.** 「용량과 개수가 다르다」는 사실이 이 한 줄로 감춰지는 것이고, 사본을 주므로 안의 배열도 지켜진다 → [[defensive-copy]] · [[array-copy]]

`indexOf` 가 `==` 대신 `equals` 를 쓰는 것도 결정이다. 같은 인스턴스가 아니라 **같은 내용**을 찾겠다는 뜻이고, 담긴 클래스가 `equals` 를 재정의해 두지 않았으면 주소 비교로 되돌아간다 → [[object-equality]] · [[linear-search]]

## 왜 중요한가

**「배열은 크기가 고정이다」가 이 구조 하나로 감춰진다.** 닷새 전 회차에서는 `MAX_SIZE = 10` 을 선언하고 11번째 등록에서 `ArrayIndexOutOfBoundsException` 이 나는 상태였다. 여기서 그 상한이 사라지고, **부르는 쪽 코드는 한 글자도 안 바뀐다** → [[array]]

**늘리는 비율이 성능을 정한다.** 1.5배로 늘리면 복사 횟수가 원소 개수에 비해 훨씬 적어져, `add` 한 번의 비용이 평균적으로 상수에 가까워진다. 만약 `newSize = oldSize + 1` 로 한 칸씩 늘리면 넣을 때마다 전체를 복사하므로 n개를 넣는 데 n² 에 비례하는 일이 든다. **「늘린다」는 결정은 같고 「얼마나」가 전부를 가른다.**

**그리고 이 구조가 배열의 장단점 중 무엇을 남기고 무엇을 포기하는지가 명확하다.** 인덱스 접근 O(1) 과 연속 메모리는 그대로 갖고, 늘어날 때 O(n) 복사가 한 번씩 일어나는 것을 받아들인 것이다. 그 O(n) 마저 없애려고 연속 메모리를 버리는 쪽이 같은 회차의 다음 실습이다 → [[linked-list]]

## 경계와 오해

- **필기의 `add()` 에 죽은 코드가 있다** — `oldSize`·`newSize` 를 계산해 놓고 쓰지 않는다. 실제로 크기를 계산하는 것은 `grow()` 안이고, `add` 의 두 줄은 아무 일도 하지 않는다. **`grow()` 를 만들면서 원래 `add` 안에 있던 계산을 지우는 것을 빠뜨린 흔적**이다.
- **「Arrays메서드 활용」 버전은 두 번 늘린다** — `list = Arrays.copyOf(list, newSize)` 로 이미 1.5배로 늘려 놓고 `grow()` 를 또 부른다. 결과는 1.5배가 두 번 적용된 2.25배이고 복사도 두 번 일어난다. **`Arrays.copyOf` 가 `grow()` 를 대체하려던 것인데 `grow()` 호출을 지우지 않은 것**으로 보인다. 동작은 하고 예외도 안 나므로 오류로 드러나지 않는다 → [[array-copy]]
- **그 두 줄과 이중 확장이 하루 뒤 회차에 그대로 남아 있다** — 인터페이스로 묶고 추상 클래스를 끼우며 `grow()` 안은 `System.arraycopy` 로 고쳤는데, `add()` 의 죽은 계산과 `Arrays.copyOf` + `grow()` 는 손대지 않았다. **구조를 다시 짜는 리팩터링이 그 안의 오류를 발견해 주지는 않는다** — 고친 자리와 남은 자리가 같은 메서드 안에 나란히 있다. **12일 뒤 회차에서는 정리된다** — `grow()` 가 클래스에서 사라지고 `add()` 의 `oldSize`·`newSize` 가 `Arrays.copyOf` 의 인자로 실제로 쓰이게 되어, 죽은 계산과 이중 확장이 한 번에 없어졌다. 대신 그 회차에서 `indexOf` 와 `size` 쪽에 새 문제가 들어왔다(아래) — **정리와 후퇴가 같은 클래스에서 동시에 일어났다.**
- **초기 크기가 0 이나 1 이면 영원히 늘어나지 않는다** — `oldSize >> 1` 이 0 이 되어 `newSize` 가 `oldSize` 와 같아지고, 새 배열도 같은 크기라 `list[size++]` 에서 `ArrayIndexOutOfBoundsException` 이 난다. **늘리는 공식은 「비율」만 정하고 「최소 증가량」을 정하지 않았다.** 실제 `ArrayList` 가 기본 용량을 따로 두는 이유가 이것이다 → [[bit-shift]] · [[exception-handling]]
- **`MAX_SIZE = 100` 은 그 함정을 고친 것이 아니라 안 걸리게 해 둔 것이다** — 하루 뒤 회차의 초기 용량이 100 이므로 `100 >> 1` 이 50 이고 문제가 드러나지 않는다. **공식은 그대로이고 시작값이 커진 것뿐**이라 초기 용량을 1 로 두는 순간 같은 자리에서 멈춘다. 그리고 이름이 `MAX_SIZE`(최대 크기)인데 실제로는 **늘어나는 배열의 초기 크기**라, 늘려 쓰기로 한 순간 이름이 사실과 어긋난다 → [[bit-shift]] · [[variable]]
- **12일 뒤에는 `MAX_SIZE = 3` 이다 — 확장 경로를 실제로 밟게 하는 값이다** — 100 이면 실습에서 회원을 몇 명 넣어 봐도 `if (size == list.length)` 안으로 한 번도 들어가지 않는다. 3 이면 네 번째 등록에서 곧바로 돌고(3 → 4 → 6 → 9), **함정에서 두 칸 떨어진 값**이다(2 도 돌지만 1 은 멈춘다). 확장을 확인하려면 초기 용량을 작게 두어야 하는데 **작게 두면 이 공식의 하한에 가까워진다** — 시험하기 좋은 값과 안전한 값이 반대 방향에 있다 → [[bit-shift]]
- **자료구조가 특정 도메인 클래스를 알고 있다** — `Object` 로 무엇이든 담게 만들어 놓고 `contain(User user)` 하나가 남아 있어서, `util` 패키지의 `ArrayList` 가 `bitcamp.myapp2.vo.User` 를 `import` 한다. **의존 방향이 뒤집힌 자리**다 — 담기는 쪽이 담는 쪽을 알아야 하는데 담는 쪽이 담기는 쪽을 안다. `indexOf(Object)` 가 이미 있으므로 `contain` 은 부르는 쪽에서 `indexOf(user) != -1` 로 쓸 수 있고, 그러면 `import` 가 사라진다 → [[package]] · [[cohesion]]
- **그 의존도 12일 뒤에 끊긴다 — 그리고 다른 것을 잃는다** — `contain(User user)` 이 `contains(Object obj)` 로 바뀌어 `User` 를 `import` 할 이유가 없어졌다. 대신 **아무 타입이나 넘겨도 컴파일된다** — 「무엇이든 담는 자료구조」의 대가를 이 메서드도 같이 치르게 된 것이고, 이 클래스가 도메인을 모르게 만드는 것과 잘못된 인자를 막는 것이 **같은 방향이 아니다** → [[object-class]] · [[object-equality]]
- **자식이 `size` 를 다시 선언해 중간 층이 무의미해졌다** — 12일 뒤 회차의 `ArrayList` 에 `private int size = 0;` 이 있고 `size()` 도 다시 재정의되어 있다. `AbstractList.size` 를 만든 이유가 「두 클래스에 `size` 가 중복된다」였는데 **중복이 되돌아온 것**이고, 값은 맞으므로 아무도 눈치채지 못한다 → [[field-hiding]] · [[abstract-class]]
- **`indexOf` 가 `equals` 에서 `==` 로 후퇴했다** — 하루 뒤 회차의 `list[i].equals(obj)` 가 12일 뒤 `list[i] == obj` 다. 그리고 그 회차의 부르는 쪽은 `indexOf(new User(userNo))` 처럼 **그 자리에서 만든 객체**를 넘기므로 **결코 찾지 못한다.** 자료구조의 한 줄이 프로그램의 조회·수정·삭제를 통째로 무력화한 자리다 → [[object-equality]]
- **`get()` 안에 쓰이지 않는 지역 변수가 하나 늘었다** — `java.util.ArrayList l;` 한 줄이 12일 뒤 회차의 `get()` 안에 들어 있다. 자기 이름과 같은 표준 클래스를 완전 이름으로 적어 둔 것이라 **자동 완성이 남긴 흔적**으로 보이고, 선언만 있어 컴파일에는 영향이 없다. 같은 이름을 가진 클래스를 직접 만드는 실습에서는 이런 줄이 「무엇을 참고하려던 자리」로 오래 남는다 → [[package]] · [[variable]]
- **가변 배열 ≠ 크기 제한이 없다** — 늘릴 때마다 **새 배열과 낡은 배열이 잠깐 동시에 존재**하므로 필요한 메모리는 1.5배가 아니라 2.5배 순간 최대치다. 「메모리가 남아 있으면 늘어난다」가 아니다 → [[garbage-collection]]
- **`size` 와 `list.length` 를 끝까지 구별해야 한다** — 순회는 `size` 까지, 확장 판정은 `list.length` 로 한다. 이 짝이 어긋나면 아직 `null` 인 칸이 목록에 나온다. 닷새 전 회차의 `userLength` 와 `users.length` 가 그대로 이름만 바뀐 것이다 → [[array]] · [[default-initialization]]
- **늘리기만 있고 줄이기는 없다** — 많이 넣었다가 다 지워도 배열은 커진 채로 남는다. 삭제가 용량을 되돌리지 않는다는 것이 이 구조의 성질이다 → [[array-element-removal]]

## 함께 보는 개념

- [[array]] — 고정 크기라는 전제
- [[array-copy]] — 옮겨 담는 표준 도구
- [[bit-shift]] — 1.5배를 계산하는 방법
- [[linked-list]] — 같은 문제를 다른 방식으로 푼 구조
- [[array-element-removal]] — 지우는 쪽의 비용
- [[default-initialization]] — 늘린 칸의 초기 상태
- [[type-casting]] — `Object[]` 에서 꺼낼 때 필요한 것
- [[object-class]] — 무엇이든 담게 해 주는 타입
- [[garbage-collection]] — 버려지는 낡은 배열
- [[crud]] — 이 구조가 저장소로 쓰이는 자리
- [[string-builder]] — 문자열 쪽에서 같은 일을 하는 버퍼
- [[interface]] — 이 클래스가 지키게 되는 약속
- [[abstract-class]] — `size` 를 물려주는 중간 층
- [[defensive-copy]] — `toArray()` 가 사본을 내주는 이유
- [[object-equality]] — `indexOf` 의 판정 기준
- [[linear-search]] — `indexOf` 가 하는 일
- [[field-hiding]] — `size` 가 다시 선언된 자리
- [[refactoring]] — 이 클래스가 정리되고 동시에 후퇴한 작업

## 출처

- [[2024-06-25-Day22]] — 실습프로젝트에서 `grow()` 로 1.5배(`oldSize + (oldSize >> 1)`)씩 늘리는 가변 배열을 직접 만들었고, 옮겨 담는 루프를 `Arrays.copyOf` 로 바꾸는 것까지 나온다. 앞선 3.1 의 배열 장단점 표에서 「고정된 크기」가 장점과 단점 양쪽에 적혀 있던 것이 이 실습의 출발점이다
- [[2024-06-26-Day23]] — 이 클래스가 `List` 인터페이스의 구현이 되고 `remove`·`toArray`·`indexOf` 까지 채워졌다. `grow()` 의 옮겨 담기가 `System.arraycopy` 로, `toArray()` 는 `size` 만큼만 복사해 용량을 감춘다. 초기 용량이 `MAX_SIZE = 100` 으로 박혀 「작은 값에서 안 늘어나는」 함정을 우연히 피하게 되었고, 전날의 이중 확장과 죽은 계산은 그대로 남았다
- [[2024-07-08-Day30]] — 같은 클래스를 리팩터링 회차에 다시 적으면서 **세 가지가 정리되고 세 가지가 새로 생겼다.** 정리된 쪽은 `grow()` 제거로 없어진 이중 확장과 죽은 계산, `contain(User)` → `contains(Object)` 로 끊긴 도메인 의존, 그리고 확장 경로를 실제로 밟게 하는 `MAX_SIZE = 3` 이다. 새로 생긴 쪽은 `private int size = 0` 재선언으로 죽은 `AbstractList.size`, `list[i].equals(obj)` → `list[i] == obj` 후퇴, `get()` 안의 `java.util.ArrayList l;` 다. `toArray()` 의 복사 길이도 `size` 에서 `arr.length` 로 바뀌었는데 두 값이 같아 동작은 그대로다
