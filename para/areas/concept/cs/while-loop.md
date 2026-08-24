---
type: concept
id: while-loop
title: while 문
aliases:
  - while
  - while 문
  - 반복문
  - 무한 루프
  - while true
up:
  - 2024-06-11-Day11
tags:
  - java
  - 제어문
  - 문법
---

# while 문

조건이 참인 동안 문장을 반복하는 제어문. **조건을 먼저 보고** 실행하므로, 처음부터 거짓이면 한 번도 실행되지 않는다.

## 정의

```java
문법1:
while (조건) 문장;
=> 조건이 참인 동안 문장을 계속 실행한다.
```

반복을 끊거나 건너뛰는 것은 [[break-continue]] 가 맡는다.

```java
while (조건)
	문장;
   if (조건) break;      // 조건이 참이면 반복문을 종료한다

while (조건)
	문장1;
   if (조건) continue;   // 조건이 참이면 문장2를 건너뛰고 while 조건으로 돌아간다
	문장2
```

조건식 자리에 `true` 를 두면 **종료 판단을 조건식이 아니라 본문에서** 하게 된다.

```java
while (true) {
    // ... 종료 시점에 break
}
```

## 사용 예시

메뉴 번호를 받아 처리하는 루프다. 유효 범위를 검사하고, 종료 메뉴를 고르면 `break` 로 나간다.

```java
int menuNo;
while (true) {
    System.out.print("> ");
    menuNo = keyboardScanner.nextInt();

    if (menuNo >= 1 && menuNo <= menus.length) {
        if (menus[menuNo - 1] == "종료") {
            break;
        }
        System.out.println(menus[menuNo - 1]);
    } else {
        System.out.println("메뉴 번호가 옳지 않습니다.");
    }
}
```

이 필기는 같은 메뉴 루프를 [[do-while-loop]] 로 먼저 썼다가 `while (true)` 로 바꿨다. 종료 조건이 "6번을 입력했나"에서 **"고른 메뉴가 종료인가"**로 바뀌면서, 값을 뽑아 배열과 견주기 전에는 판단할 수 없게 됐기 때문이다 — 조건식 한 줄에 담을 수 없는 판단이 되면 `while (true)` + `break` 로 간다.

## 왜 중요한가

**`for` 는 횟수를, `while` 은 조건을 적는다.** 몇 번 도는지 모르는 반복 — 입력을 받을 때까지, 파일이 끝날 때까지, 조건이 만족될 때까지 — 가 `while` 의 자리다. 이때 반복을 끝내는 책임이 조건식이나 `break` 어느 한쪽에 있으므로, **루프 안에서 조건에 쓰이는 값을 바꾸지 않으면 무한 루프가 된다.** `for` 는 증감문이 그 자리를 강제하지만 `while` 은 강제하지 않는다.

`while (true)` 는 게으른 코드가 아니다. **종료 조건이 여러 개거나, 값을 얻은 뒤에야 판단할 수 있을 때** 쓰는 형태다. 조건식에 억지로 담으면 같은 코드를 루프 앞에 한 번 더 쓰거나 플래그 변수를 만들게 된다.

## 경계와 오해

- **`while` ≠ `do~while`** — 조건이 처음부터 거짓이면 `while` 은 0번, `do~while` 은 1번 실행한다. "0번 이상 반복이면 `while`, 한 번 이상 반복이면 `do~while`" 이 선택 기준이다 → [[do-while-loop]]
- **`while (true)` 는 무한 루프가 아니다** — 종료 조건이 조건식에서 본문의 `break` 로 옮겨 간 것이다. 진짜 무한 루프는 `break` 가 닿지 않는 경우다.
- **`continue` 가 무한 루프를 만들 수 있다** — 증감·갱신 코드를 본문 끝에 두면 `continue` 가 그것을 건너뛴다. `for` 는 증감문이 조건 검사 앞에 있어 건너뛰어지지 않는다 → [[break-continue]]
- **`while` 뒤에 세미콜론을 찍으면 본문이 사라진다** — `while (조건);` 은 빈 문장을 반복하는 문법상 올바른 코드다. `do~while` 이 세미콜론을 요구하는 것과 헷갈리기 쉽다.
- **반복문과 조건문은 다른 갈래다** — 이 필기는 [[switch-statement]] 를 「반복문」 절 아래에 뒀는데, `switch` 는 값으로 갈리는 조건문이다. 반복을 만드는 것은 `while`·`do~while`·`for` 뿐이다.

## 함께 보는 개념

- [[do-while-loop]] — 조건을 뒤에서 보는 형태. 실행 횟수가 갈린다
- [[for-loop]] — 횟수가 정해진 반복
- [[break-continue]] — 반복을 끊고 건너뛰는 문법
- [[if-statement]] — 루프 안에서 갈리는 판단
- [[standard-input]] — `while` 이 잘 맞는 입력 반복
- [[exception-handling]] — 잘못된 입력을 잡고 루프를 계속 돌리는 짝
- [[command-loop]] — 이 루프가 프로그램의 골격이 되는 형태

## 출처

- [[2024-06-11-Day11]] — `while (조건) 문장;` 의 기본 형태와 `break`·`continue` 로 반복을 제어하는 것, 그리고 메뉴 루프를 `do~while` 에서 `while (true)` + `break` 로 바꿔 쓰는 것을 배웠다
