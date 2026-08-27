---
type: concept
id: if-statement
title: if 문
aliases:
  - if
  - if 문
  - 조건문
  - else if
  - dangling else
  - 매달린 else
up:
  - 2024-06-11-Day11
tags:
  - java
  - 제어문
  - 문법
---

# if 문

조건이 참일 때만 문장을 실행하는 제어문. 조건을 **하나씩 순서대로** 따져 첫 번째로 참인 곳만 실행한다.

## 정의

세 형태가 있다.

```java
문법1:
  if (조건) 문장1;
  => 조건이 참일 때 문장1을 수행한다.

문법2:
  if (조건) 문장1; else 문장2;
  => 조건이 참일 때 문장1을 수행하고, 거짓이면 문장2를 수행한다.

문법3:
  if (조건1) 문장1;
  else if (조건2) 문장2;
  else if (조건3) 문장3;
  else 문장4;
  => 조건1~3을 순차적으로 수행하고, 모두 거짓이면 문장4를 수행한다.
```

중괄호를 쓰지 않으면 `if` 는 **바로 뒤의 한 문장만** 지배한다. 여러 문장을 묶으려면 `{}` 가 필요하고, 이 규칙이 `else` 의 짝을 정하는 문제로 이어진다.

## 사용 예시

메뉴 배열을 출력하면서 종료 항목만 색을 다르게 준다.

```java
for (int i = 0; i < menus.length; i++) {
    if (menus[i] == "종료") {
        System.out.printf("%s%d. %s%s\n", (boldAnsi + redAnsi), (i + 1), menus[i], resetAnsi);
    } else {
        System.out.printf("%d. %s\n", (i + 1), menus[i]);
    }
}
```

입력 검증에도 쓰인다. 범위를 먼저 보고, 그 안에서 다시 종료인지 본다.

```java
if (menuNo >= 1 && menuNo <= menus.length) {
    if (menus[menuNo - 1] == "종료") {
        break;
    }
    System.out.println(menus[menuNo - 1]);
} else {
    System.out.println("메뉴 번호가 옳지 않습니다.");
}
```

여기서 `==` 로 문자열을 비교한 것은 이 필기가 뒤에 `.equals()` 로 고친 부분이다 → [[string-comparison]]

## 왜 중요한가

**`else if` 사슬은 조건 목록이 아니라 순서다.** 앞 조건이 참이면 뒤는 아예 평가되지 않으므로, 조건을 겹치게 써도 앞에 있는 것이 이긴다. 그래서 `if (score > 60) ... else if (score > 90) ...` 처럼 넓은 조건을 먼저 두면 뒤 가지에 절대 닿지 않는다. **버그가 조건식이 아니라 조건의 순서에 있는** 종류의 오류가 여기서 나온다.

그리고 [[switch-statement]] 와 갈리는 기준이 여기 있다. `if` 는 **조건식**으로 갈리고 `switch` 는 **값**으로 갈린다. 범위 비교(`>= 1 && <= length`)는 `case` 로 쓸 수 없으니 `if` 가 맡는다.

## 경계와 오해

- **`else` 는 들여쓰기가 아니라 가장 가까운 `if` 와 짝을 이룬다 (dangling else)** — 아래 코드에서 `else` 는 겉보기와 달리 `age >= 70` 의 짝이다. 그래서 나이가 30 이면 성년인데도 "미성년입니다"가 출력된다. **문법상 짝이 맞는 것과 의미가 맞는 것은 다르고, 컴파일러는 앞쪽만 검사한다.**

    ```java
    if (age >= 19) {
      if (age >= 70)
        System.out.println("지하철 무임승차 가능합니다.");
      else
        System.out.println("미성년입니다.");   // age >= 70 의 else 다
    }
    ```

    짝을 바꾸려면 안쪽 `if` 를 `{}` 로 닫아 `else` 가 붙을 곳을 없앤다. **중괄호는 스타일이 아니라 짝을 정하는 문법이다** — 그래서 한 문장이어도 `{}` 를 쓰는 관례가 생겼다.
- **조건에는 `boolean` 만 온다** — C 계열처럼 `if (1)` 이나 `if (menuNo)` 를 쓸 수 없다. 0 이 아니면 참이라는 규칙이 Java 에는 없다 → [[operator]]
- **`if` 여러 개와 `else if` 사슬은 다르다** — 독립된 `if` 를 나열하면 조건이 여럿 참일 때 여럿 실행된다. `else if` 는 하나만 실행된다.
- **`=` 와 `==` 를 헷갈려도 대개 컴파일에서 막힌다** — `if (a = 1)` 은 결과가 `int` 라서 오류다. 단 `boolean` 변수라면 `if (flag = true)` 가 통과한다.
- **`if` 는 값을 돌려주지 않는다** — 값이 필요하면 [[ternary-operator]] 다. `String s = if (...) ...` 은 성립하지 않는다 → [[expression-vs-statement]]

## 함께 보는 개념

- [[switch-statement]] — 값 하나로 갈리는 쪽. 범위·조건식은 `if` 가 맡는다
- [[ternary-operator]] — 값을 돌려주는 조건 분기
- [[short-circuit-evaluation]] — 조건식 안에서 뒤쪽을 건너뛰는 규칙
- [[expression-vs-statement]] — `if` 가 문장인 이유
- [[string-comparison]] — 조건식에서 문자열을 비교할 때 갈리는 자리
- [[while-loop]] — 같은 조건 판단을 반복에 쓰는 것

## 출처

- [[2024-06-11-Day11]] — `if` / `if-else` / `else if` 사슬 세 형태와, 중괄호를 쓰지 않으면 `else` 가 가장 가까운 `if` 와 짝을 이룬다는 것(dangling else)을 배웠다
