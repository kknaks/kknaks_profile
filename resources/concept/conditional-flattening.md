---
type: concept
id: conditional-flattening
title: 중첩 조건문 평탄화
aliases:
  - 조건문 평탄화
  - 중첩 조건문
  - guard clause
  - 가드절
  - early return
  - 조기 반환
up:
  - 2024-06-11-Day12
tags:
  - 리팩터링
  - 제어문
  - 가독성
---

# 중첩 조건문 평탄화

안으로 겹쳐 들어간 `if` 를 **같은 층의 `else if` 사슬로 펴는 것.** 분기의 수를 줄이는 것이 아니라 **읽을 때 쌓아야 하는 층을 없애는 것**이다.

## 정의

이 필기는 목표를 그림으로 먼저 적었다.

```text
if(조건){ 문장;
} else {문장
  if(조건){
    if(조건)
  } else {}
}
구조 단순화 하기
```

두 층으로 겹친 조건을 한 층으로 내린다.

## 사용 예시

메서드로 뽑은 직후의 코드는 아직 겹쳐 있다 → [[method]]

```java
int menuNo = Integer.parseInt(command);
String menuTitle = getMenuTitle(menuNo);
if (isValidateMenu(menuNo)) {
    if (menuTitle.equals("종료")) {
        break;
    }
    System.out.println(menuTitle);
} else {
    System.out.println("유효한 메뉴 번호가 아닙니다.");
}
```

같은 판단을 한 층으로 펴면 이렇게 된다.

```java
int menuNo = Integer.parseInt(command);
String menuTitle = getMenuTitle(menuNo);
if (menuTitle == null) {
    System.out.println("유효한 메뉴 번호가 아닙니다.");
} else if (menuTitle.equals("종료")) {
    break;
} else {
    System.out.println(menuTitle);
}
```

**코드를 옮겨 쓰는 것만으로는 이렇게 되지 않는다.** 앞의 코드는 "유효한가"(`isValidateMenu`)와 "무엇인가"(`getMenuTitle`)를 따로 물어서 층이 두 개였다. 뒤의 코드는 `getMenuTitle` 이 **유효하지 않으면 `null` 을 돌려주기** 때문에 한 번 물어 둘을 다 안다.

```java
static String getMenuTitle(int menuNo){
    return isValidateMenu(menuNo)? menus[menuNo-1] : null;
}
```

→ [[ternary-operator]] · [[object-reference]]

즉 **평탄화의 실제 작업은 조건문을 만지는 것이 아니라 판정과 조회를 한 값으로 합치는 것**이다. 층이 사라지는 것은 그 결과다.

> 위 앞 코드는 필기 원본의 `menuTile` 오타와 `if (isValidateMenu(menuNo) {` 의 닫는 괄호 누락을 고쳐 인용했다. 원본은 [[2024-06-11-Day12]] 에 그대로 있다.

## 왜 중요한가

**겹친 조건은 읽는 사람에게 상태를 쌓게 만든다.** 2층이면 안쪽 문장을 읽을 때 "유효하고 그리고 종료가 아닐 때"를 머리에 들고 있어야 하고, 3층이면 경로가 여덟 갈래로 늘어난다. 평탄화하면 각 가지가 **앞의 조건을 몰라도 읽히는** 문장이 된다 — `menuTitle == null` 가지는 그 한 줄만 봐도 무슨 경우인지 안다.

두 번째로 **비정상 케이스를 위로 올리면 정상 흐름이 마지막에 남는다.** 위 코드에서 "유효하지 않다"가 첫 가지로 올라가고 정상 출력이 맨 아래에 온다. 오류 처리에 파묻힌 정상 경로를 찾는 일이 없어진다.

그리고 이 정리는 **버그를 드러낸다.** 겹쳐 있는 동안은 `menuTitle` 이 `null` 인 경우에 `.equals()` 를 부르게 되는지 아닌지가 층에 가려 보이지 않는다. 펴 놓으면 `null` 검사가 반드시 첫 가지여야 한다는 것이 눈에 들어온다.

## 경계와 오해

- **평탄화 ≠ 조건을 줄이는 것** — 가지의 수는 그대로다(유효하지 않음 / 종료 / 정상). 없애는 것은 **중첩의 깊이**다. 조건이 실제로 줄었다면 그건 판정을 합친 쪽의 공이다.
- **`else if` 사슬은 순서가 곧 의미다** — `null` 검사를 뒤로 미루면 `menuTitle.equals(...)` 에서 `NullPointerException` 이 난다. 중첩은 층으로 순서를 강제했지만 사슬은 **쓴 순서**가 유일한 보장이다. 평탄화는 층 의존을 순서 의존으로 바꾸는 것이다 → [[if-statement]]
- **`null` 을 신호로 쓰는 것에는 대가가 있다** — 부르는 쪽이 검사를 잊으면 실행 시점에 터진다. "없음"을 값으로 표현하는 방법이 `null` 뿐이던 시점의 관용이고, 뒤에 `Optional` 이나 예외로 바꾸게 되는 자리다 → [[object-reference]]
- **`isValidateMenu` 가 사라진 것이 아니다** — 평탄화한 코드에 그 호출이 안 보이지만 `getMenuTitle` 안에서 여전히 불린다. 검증이 없어진 것이 아니라 **한 겹 안으로 들어간 것**이고, 이것이 층을 줄일 수 있었던 이유다.
- **평탄화가 항상 답은 아니다** — 가지마다 앞의 조건이 실제로 필요한 경우(들여쓰기가 의미를 담고 있는 경우)에는 펴면 조건이 중복된다. 겹침이 `A && B` 를 표현하는 것이라면 그것은 겹쳐 있는 것이 맞다 → [[short-circuit-evaluation]]

## 함께 보는 개념

- [[if-statement]] — 사슬의 순서가 실행을 정하는 규칙
- [[method]] — 조건을 이름 있는 판정으로 뽑는 단계
- [[object-reference]] — `null` 을 신호로 쓸 때의 위험
- [[ternary-operator]] — 판정과 조회를 한 값으로 합치는 데 쓴 도구
- [[short-circuit-evaluation]] — 겹친 조건을 하나의 조건식으로 합치는 다른 방법

## 출처

- [[2024-06-11-Day12]] — 겹친 `if` 를 `else if` 사슬로 펴는 실습에서, `getMenuTitle` 이 유효하지 않을 때 `null` 을 돌려주게 만들면 검증과 조회를 한 번에 물을 수 있어 층이 하나 사라진다는 것을 배웠다
