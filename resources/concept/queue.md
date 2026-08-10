---
type: concept
id: queue
title: 큐 (Queue)
aliases:
  - queue
  - 큐
  - FIFO
  - 선입선출
  - First In First Out
  - 대기열
  - offer
  - poll
up:
  - 2024-07-09-Day31
  - 2025-02-18-Day31
tags:
  - 자료구조
  - java
  - 알고리즘
  - 설계
---

# 큐 (Queue)

**한쪽 끝으로 넣고 반대쪽 끝으로 빼는 목록.** 필기의 한 줄이 정의 전부다 — 「큐는 FIFO(First In, First Out) 구조를 따르며 처음에 삽입된 요소가 가장 먼저 삭제되는 방식이다. 큐는 마치 줄을 서서 기다리는 형태이다」. [[stack]] 과 갈리는 것은 **넣는 끝과 빼는 끝이 같은가**뿐이고, 그 한 가지가 「최근 것」과 「오래된 것」 중 무엇이 공짜인지를 뒤집는다.

## 정의

| | [[stack]] | 큐 |
|---|---|---|
| 넣는 곳 / 빼는 곳 | 같은 끝 | **반대 끝** |
| 먼저 나오는 것 | 가장 최근 것 | **가장 오래된 것** |
| 쓰이는 데 | 되돌아갈 곳 기억 | 순서대로 처리 · 최근 기록 유지 |
| 이 실습의 이름 | `push` / `pop` | `offer` / `poll` |

```java
public class Queue extends LinkedList {
    //push구현하기
    public void offer(Object obj) {
        add(obj);                    // 꼬리에 붙인다
    }
    //pop구현하기
    public Object poll() {
        return remove(0);            // 머리를 뺀다
    }
    //empty구현하기
    public boolean isEmpty() {
        return size() == 0;
    }
}
```

**두 클래스가 글자 두 군데만 다르다** — `Stack` 의 `pop` 이 `remove(size() - 1)` 이고 여기가 `remove(0)` 이다. 나머지는 같고 주석까지 `//push구현하기`·`//pop구현하기` 로 복사돼 있다. **자료구조를 가르는 것이 저장 방식이 아니라 「어느 자리를 쓰기로 했나」**라는 것이 이보다 선명하게 보이는 자리가 드물다 → [[linked-list]]

## 사용 예시

이 회차의 실습이 큐로 **최근 명령 20개**를 기억한다. 입력을 받는 곳 한 군데에 넣고, 20개를 넘으면 앞에서 버린다.

```java
public static String input(String format, Object... args) {
  String promptTitle = String.format(format + " ", args);
  System.out.print(promptTitle);
  String input = keyboardScanner.nextLine();
  if (promptTitle.endsWith(">")) {
    inputQueue.offer(promptTitle + input);
  }
  if (inputQueue.size() > 20) {
    inputQueue.poll();
  }
  return input;
}
```

**넣을 때마다 하나 버리는 것이 「최근 N개」를 만드는 방법의 전부다.** 큐가 아니면 「가장 오래된 것」을 찾는 일이 따로 필요하다 — 큐는 그것이 머리에 있다는 것을 구조로 보장한다.

읽는 쪽은 들어온 순서대로 찍는다.

```java
public static void printHistory() {
  System.out.println("[명령내역]-----------------------------");
  for (int i = 0; i < inputQueue.size(); i++) {
    System.out.println(inputQueue.get(i));
  }
  System.out.println("-------------------------------------끝");
}
```

그리고 그것을 부르는 명령 하나가 표에 들어간다 → [[dispatch-table]]

```java
public class HistoryCommand implements Command{
  @Override
  public void execute(Stack menuTitle){
    Prompt.printHistory();
  }
}
```

**기록을 남기는 자리가 한 곳이라는 것이 이 설계의 요점**이다. `Prompt.input()` 은 모든 화면이 입력을 받을 때 부르는 정적 메서드이므로, 거기 한 줄을 넣으면 프로그램 전체의 입력이 모인다 → [[static-member]] · [[standard-input]]

## 왜 중요한가

**「순서대로 처리한다」와 「최근 것만 남긴다」가 같은 구조로 풀린다.** 앞의 것은 넣는 만큼 빼는 것이고 뒤의 것은 넘칠 때만 빼는 것이며, 어느 쪽이든 **빼야 할 것이 어디 있는지 찾지 않는다.**

**메모리가 저절로 묶인다.** 상한이 없는 기록은 오래 켜 두면 계속 자라는데, 넣을 때마다 상한을 검사하면 **최대 크기가 코드에 적혀 있는 값으로 고정**된다. 화면 로그·최근 파일 목록·되돌리기 이력이 다 이 모양이다 → [[garbage-collection]]

**그리고 「밖에서 보이는 순서」와 「자료구조의 순서」가 여기서 처음 일치한다.** [[stack]] 은 쌓은 순서를 읽으려면 제약을 넘어야 했지만, 큐는 **꺼내는 순서가 곧 사용자가 보고 싶은 순서**다. 기록을 오래된 것부터 보여 주는 화면이라면 큐가 자료구조이자 표시 순서다.

## 경계와 오해

- **이 코드는 아무것도 기록하지 않는다** — `promptTitle` 이 `String.format(format + " ", args)` 이므로 **항상 공백으로 끝난다.** 그래서 `promptTitle.endsWith(">")` 는 언제나 `false` 이고 `offer` 는 한 번도 불리지 않는다. `printHistory()` 는 머리글과 꼬리글 사이가 늘 비어 있고, **큐를 만들고 넣고 상한을 두고 화면까지 만든 기능 전체가 동작하지 않는다.** 화면에 프롬프트를 예쁘게 띄우려고 붙인 공백 한 칸이 판정 조건을 무너뜨린 것이고, 검사할 값과 출력할 값을 같은 변수로 쓴 것이 원인이다 — 원본 문자열(`format`)로 판정하거나 공백을 `print` 할 때만 붙이면 살아난다 → [[format-string]] · [[string-comparison]]
- **상한 검사가 넣는 일과 묶여 있지 않다** — `if (inputQueue.size() > 20)` 이 `endsWith` 블록 **밖에** 있어서, 아무것도 넣지 않은 호출에서도 검사가 돈다. 지금은 큐가 늘 비어 있어 무해하지만 **「넣었으니 넘쳤을 수 있다」는 인과가 코드에 표현되지 않은 것**이고, 넣기와 버리기를 한 메서드로 묶어야 하는 자리다.
- **상한이 20 인 것이 코드에 박혀 있다** — `if (inputQueue.size() > 20)` 의 20 은 이름이 없다. 15일 앞 회차의 `MAX_SIZE` 처럼 상수로 두면 「무엇의 20 인가」가 이름으로 남는다 → [[static-member]] · [[literal]]
- **큐를 목록으로 읽고 있다** — `printHistory` 가 `get(i)` 로 훑는다. 큐 연산(`poll`)으로 읽으면 **읽는 것이 곧 지우는 것**이 되어 한 번 본 기록이 사라지므로, 화면에 찍기 위해서는 목록 접근이 필요하다. `Queue extends LinkedList` 라 그것이 그냥 되는데, **가진 것으로 만들었다면 「순회는 되고 지우는 것은 안 되는」 창구를 따로 열어야 했다** — 자료구조의 제약을 정하는 일이 실은 「무엇을 공개할까」의 문제라는 것이 여기서 드러난다 → [[stack]] · [[encapsulation]] · [[interface-segregation-principle]]
- **`get(i)` 로 훑으면 O(n²) 이다** — 단일 연결 리스트의 `get` 은 머리에서부터 `i` 번 걸어간다. 20개면 상관없지만 **같은 코드가 큰 큐에 그대로 쓰이면 순회 한 번이 제곱이 된다.** 커서를 들고 한 번만 도는 방법이 `toArray()` 로 이미 있다 → [[linked-list]] · [[linear-search]]
- **`isEmpty()` 를 만들어 두고 아무 데서도 쓰지 않는다** — `poll()` 이 빈 큐에서 `remove(0)` 을 부르면 `index >= size` 검사에 걸려 `null` 을 돌려준다. 우연히 `java.util.Queue.poll()` 의 규약(비었으면 `null`)과 같아졌지만 **의도해서 맞춘 것이 아니고**, 같은 노트의 `Stack.pop()` 이 `remove(-1)` 로 `null` 을 받는 것과는 경로가 다르다 → [[stack]]
- **`offer` 는 `add` 와 하는 일이 같다** — 상속했으므로 `add` 도 그대로 쓸 수 있고, `offer` 는 이름만 다른 통로다. 표준 라이브러리에서 둘이 갈리는 이유는 **꽉 찼을 때의 행동**이다 — `add` 는 예외를 던지고 `offer` 는 `false` 를 돌려준다. 이 구현의 `offer` 는 `void` 라서 그 구별을 표현할 수 없고, 크기 제한이 자료구조 안이 아니라 부르는 쪽(`if (size() > 20)`)에 있어서 **애초에 「꽉 찬」 상태가 없다** → [[exception-handling]]
- **「검색기록」이 아니다** — 필기는 이 기능을 「검색기록」이라 부르고 출력 머리글은 `[명령내역]` 이다. 실제로 담기는 것은 프롬프트 문자열 + 사용자가 입력한 내용이므로 **명령 내역**이 맞다. 그리고 담는 형태가 `promptTitle + input` 이라 **화면에 보여 주기 위한 문자열**이다 — 다시 실행하거나 되돌리는 데 쓰려면 명령 자체를 담아야 하고, 그러면 큐에 들어갈 것이 문자열이 아니라 객체가 된다 → [[dispatch-table]]
- **이 명령을 부를 길이 노트에 없다** — `HistoryCommand` 를 만들었지만 `commandMap.put(...)` 하는 코드가 없고 `mainMenus` 배열에도 「검색기록」 항목이 없다. 그래서 표에 등록하지 않으면 클래스만 존재하는 상태이고, 하루 전 회차의 `HelpCommand` 가 「아무도 부르지 않는 클래스」였던 것과 같은 형태다 → [[dispatch-table]]
- **큐 ≠ 순환 버퍼** — 「최근 20개」를 유지하는 이 쓰임은 순환 버퍼(ring buffer)와 결과가 같지만, 순환 버퍼는 고정 배열의 자리를 돌려쓰므로 노드를 만들고 버리지 않는다. **같은 화면을 만드는 두 자료구조**이고 이 실습은 노드를 매번 만드는 쪽이다 → [[array]] · [[dynamic-array]]
- **한 줄 넣는 것이 「읽기가 상태를 바꾸는」 구조를 만든다** — `Prompt.input()` 은 값을 받아 돌려주는 메서드인데 이제 기록도 남긴다. 편해서 그렇게 한 것이지만, **입력받는 모든 자리가 기록의 대상이 되어 「기록하지 않을 입력」을 고를 방법이 없어졌다.** 실제로 이 코드가 `endsWith(">")` 로 그것을 고르려 한 것이고 그 판정이 무너져 있다 → [[read-side-effect]]
- **`Queue` 라는 이름이 `java.util.Queue` 와 겹친다** — 그쪽은 인터페이스라서 `new Queue()` 가 안 되는데 여기서는 클래스다. `java.util.*` 를 열면 이름이 부딪히고, 같은 노트가 `Map`·`HashMap` 은 표준 것을 쓰므로 **한 파일에 자작 컬렉션과 표준 컬렉션이 섞인다** → [[package]] · [[hash-based-collection]]

## 함께 보는 개념

- [[message-broker]] — 이 자료구조가 인프라가 된 것

- [[stack]] — 반대 순서의 짝
- [[linked-list]] — 이 큐가 상속한 구현
- [[dispatch-table]] — 기록 화면을 명령으로 붙이는 자리
- [[static-member]] — 기록 지점이 한 곳으로 모이는 근거
- [[standard-input]] — 기록되는 값이 들어오는 곳
- [[format-string]] — 판정을 무너뜨린 공백이 붙는 자리
- [[read-side-effect]] — 값을 돌려주는 메서드가 상태를 바꾸게 된 문제
- [[linear-search]] — `get(i)` 순회가 무엇이 되는지
- [[encapsulation]] — 제약을 지키려면 필요한 것
- [[interface-segregation-principle]] — 상속으로 만든 대가를 재는 원칙
- [[array]] · [[dynamic-array]] — 같은 화면을 만드는 다른 자료구조
- [[package]] — 표준 라이브러리와 이름이 겹치는 문제

## 출처

- [[2025-02-18-Day31]] — **이 자료구조가 서버 사이의 인프라가 된다.** 카프카의 토픽은 「먼저 넣은 것을 먼저 꺼낸다」는 성질을 **프로세스 밖에, 여러 대에 걸쳐, 보관 기간 동안 남겨 두고** 제공한다 — 「메시지를 버퍼링하고 컨슈머 그룹을 통해 부하를 분산한다」가 그 쓸모다. 메모리 안의 큐가 하던 「생산자와 소비자의 속도 차이를 흡수한다」가 그대로 확대된 형태다 → [[message-broker]]
- [[2024-07-09-Day31]] — 「FIFO(First In, First Out)」와 「줄을 서서 기다리는 형태」로 개념을 배우고, 14일 전에 만든 `LinkedList` 를 상속해 `offer`(= `add`) · `poll`(= `remove(0)`) · `isEmpty` 를 얹어 구현했다. `Stack` 과 코드가 같고 `pop`/`poll` 의 인덱스만 다르다. 실습에서는 `Prompt.input()` 안에 한 줄을 넣어 모든 입력을 큐에 모으고 20개를 넘으면 `poll` 로 버리는 「최근 N개」를 만들고, `printHistory()` 와 `HistoryCommand` 로 화면까지 붙였다. 그런데 `promptTitle` 이 `String.format(format + " ", args)` 로 **항상 공백으로 끝나** `endsWith(">")` 가 영원히 거짓이고, **기능 전체가 아무것도 기록하지 않는다.** 상한 검사가 넣는 블록 밖에 있고, `HistoryCommand` 를 `commandMap` 에 등록하는 코드도 노트에 없다
