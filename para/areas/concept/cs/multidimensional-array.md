---
type: concept
id: multidimensional-array
title: 2차원 배열 (Multidimensional Array)
aliases:
  - 2차원 배열
  - 다차원 배열
  - multidimensional array
  - 2d array
  - 배열의 배열
  - array of arrays
  - jagged array
up:
  - 2024-06-13-Day14
tags:
  - java
  - 자료구조
  - 메모리
  - 문법
---

# 2차원 배열 (Multidimensional Array)

원소가 다시 **배열인 배열.** `String[][]` 은 「문자열 2차원 격자」가 아니라 **`String[]` 을 담은 배열**이고, 그래서 `arr[i]` 는 값이 아니라 배열 하나를 준다.

## 정의

[[array]] 의 원소 타입 자리에 다시 배열이 오는 것뿐이다. 대괄호 하나가 「배열」 한 겹을 뜻한다.

| 표기 | 원소 하나가 | 개수를 읽는 법 |
|---|---|---|
| `String[]` | `String` | `arr.length` |
| `String[][]` | `String[]` | `arr.length`(행) · `arr[i].length`(그 행의 길이) |

만드는 방법은 두 갈래다.

```java
String[][] a = new String[4][5];      // 4개의 행을 만들고 각 행에 5칸씩 확보한다
String[][] b = new String[4][];       // 행 자리만 4개. 각 행은 아직 null 이다
b[0] = new String[3];                 // 행마다 길이를 따로 정할 수 있다 (jagged)
```

뒤쪽이 가능한 이유가 곧 이 개념의 정의다 — **행은 각각 독립된 인스턴스**이고, 바깥 배열은 그 [[object-reference]] 를 모아 둔 것이다 → [[instance]] · [[default-initialization]]

선언과 동시에 값을 적으면 중괄호가 겹친다.

```java
static String[][] subMenus = {
    {"등록a", "목록", "조회", "변경", "삭제"},
    {"등록b", "목록", "조회", "변경", "삭제"}
};
```

## 사용 예시

이 필기의 실습에서 2차원 배열이 나온 이유는 **메인 메뉴 번호로 서브메뉴 한 벌을 골라야** 했기 때문이다. 메인 메뉴가 넷이고 각각 서브메뉴 다섯 개를 갖는다.

```java
static String[] mainMenus = new String[] {"회원", "팀", "프로젝트", "게시판", "도움말", "종료"};
static String[][] subMenus = {
    {"등록a", "목록", "조회", "변경", "삭제"},   // 회원
    {"등록b", "목록", "조회", "변경", "삭제"},   // 팀
    {"등록c", "목록", "조회", "변경", "삭제"},   // 프로젝트
    {"등록d", "목록", "조회", "변경", "삭제"}    // 게시판
};
```

고르는 것은 한 줄이다. 메뉴 번호에서 1을 빼면 그것이 행 번호다.

```java
processMenu(menuTitle, subMenus[menuNo - 1]);   // 행 하나를 떼어 넘긴다
```

넘겨받는 쪽은 **2차원이라는 것을 모른다.** `String[]` 만 알면 된다.

```java
static void printSubMenu(String menuTitle, String[] menus) {
    System.out.printf("[%s]\n", menuTitle);
    for (int i = 0; i < menus.length; i++) {
        System.out.printf("%d. %s\n", (i + 1), menus[i]);
    }
    System.out.println("9. 이전");
}
```

**이것이 행이 독립된 배열이라는 사실의 실용적인 값이다** — 서브메뉴를 다루는 코드는 1차원 배열 하나만 받아 동작하고, 메인 메뉴와의 대응은 부르는 쪽이 담당한다 → [[parameterization]]

> 원본 필기의 `subMenus` 선언은 행을 구분하는 콤마가 뒤의 주석(`//회원메뉴,`) 안으로 들어가 있어 그대로는 컴파일되지 않는다. 위에서는 콤마를 살려 인용했다. 원본은 [[2024-06-13-Day14]] 의 1.2 에 그대로 있다.

## 왜 중요한가

**번호와 묶음의 대응을 코드가 아니라 인덱스가 갖게 된다.** 배열 네 개(`memberMenus`·`teamMenus`…)로 뒀다면 번호에서 묶음을 찾는 [[switch-statement]] 가 필요하고, 메뉴가 하나 늘 때마다 `case` 를 더해야 한다. 2차원 배열이면 `subMenus[menuNo - 1]` 한 줄이고 늘어나는 것은 배열 선언뿐이다.

두 번째는 **행 단위로 떼어 넘길 수 있다**는 것이다. 서브메뉴 출력·실행 메서드가 `String[]` 만 받으므로, 메인 메뉴 다섯 개짜리든 다른 곳에서 만든 배열이든 그대로 부를 수 있다. Java 의 2차원 배열이 **격자가 아니라 배열의 배열**인 덕이다 — 진짜 2차원 블록이라면 행만 떼어 넘길 방법이 없다.

## 경계와 오해

- **2차원 배열 ≠ 격자(matrix)** — 행마다 길이가 달라도 된다(jagged). 그래서 「가로 세로」가 아니라 「배열의 배열」로 읽어야 한다. 실무에서 갈리는 지점은 **길이를 어디서 읽는가**다. `subMenus[0].length` 가 5라고 다른 행도 5인 보장은 없으므로, 루프는 반드시 `menus.length`(그 행의 길이)를 봐야 한다.
- **`arr.length` 는 전체 원소 개수가 아니다** — `subMenus.length` 는 4(행 개수)이고 전체 문자열은 20개다. 전체를 세려면 각 행 길이를 더해야 한다.
- **`arr[i]` 는 원소가 아니라 배열이다** — 그래서 `System.out.println(subMenus[0])` 은 내용이 아니라 주소 표기가 찍힌다. 값을 얻으려면 대괄호가 두 번 필요하다(`subMenus[0][0]`).
- **행을 넘기는 것은 복사가 아니다** — `subMenus[menuNo - 1]` 은 행의 주소를 넘긴다. 받은 쪽에서 `menus[0] = "x"` 를 하면 `subMenus` 가 바뀐다. 이 필기의 `printSubMenu`·`processMenu` 는 읽기만 해서 드러나지 않았다 → [[call-by-value]] · [[object-reference]]
- **`new String[4][]` 의 행은 `null` 이다** — 크기를 나중에 정하려고 이렇게 두면 `arr[0].length` 에서 `NullPointerException` 이 난다. 원소가 빈 문자열이 아니라 **행 자체가 없는** 상태다 → [[default-initialization]]
- **두 배열의 순서가 맞아야 한다는 규칙은 코드에 없다** — `subMenus` 의 행 순서가 `mainMenus` 의 앞 네 개와 같아야 하는데, 그 약속은 배열 두 개로 흩어져 있고 컴파일러가 검사하지 않는다. **메인 메뉴 순서를 바꾸면 「팀」에 들어가서 프로젝트 서브메뉴가 뜨는데 오류는 나지 않는다.** 이 필기가 서브메뉴 첫 항목을 `등록a`·`등록b`·`등록c`·`등록d` 로 다르게 적어 둔 덕에 어느 행이 떠 있는지가 화면에서 구별된다. 이름과 항목을 한 덩어리로 묶어야 어긋나지 않게 되는 자리이고, 그것이 클래스가 필요해지는 이유로 이어진다 → [[instance]]
- **서브메뉴가 있는지 판단할 때 `4` 를 박으면 앞서 배운 것이 되돌아간다** — 최종 코드는 `if (menuNo >= 1 && menuNo <= 4)` 로 행 개수를 상수로 적었다. [[array]] 에서 `menus.length` 를 쓰기로 한 이유가 그대로 적용되는 자리이므로 `menuNo <= subMenus.length` 여야 하고, 그러면 서브메뉴 묶음을 하나 더해도 이 조건을 고칠 일이 없다. **숫자 `4` 는 「서브메뉴 묶음이 넷」과 「서브메뉴를 가진 항목이 메인 메뉴의 앞쪽 넷」이라는 두 가지를 동시에 뜻하고 있어서, 어느 쪽이 바뀌어도 같은 자리를 고쳐야 한다.**
- **표시되는 번호와 인덱스는 다른 체계다** — 화면의 `1.`~`5.` 는 `i + 1` 로 만든 것이고, `9. 이전` 은 배열에 아예 없는 항목이다. 항목이 아홉 개를 넘기면 이 번호가 충돌한다 → [[command-loop]]

## 함께 보는 개념

- [[array]] — 한 겹 배열. 이 개념의 원소가 그것이다
- [[object-reference]] — 바깥 배열이 담고 있는 것
- [[instance]] — 행마다 따로 만들어지는 것
- [[default-initialization]] — 행 자리가 `null` 로 채워지는 규칙
- [[call-by-value]] — 행을 넘겼을 때 원본이 바뀌는 이유
- [[parameterization]] — 행을 떼어 넘겨 1차원만 아는 메서드를 만드는 것
- [[command-loop]] — 이 배열이 쓰인 자리
- [[for-loop]] — 행을 도는 짝

## 출처

- [[2024-06-13-Day14]] — 메인 메뉴 네 개에 각각 서브메뉴 다섯 개를 붙이려고 `String[][] subMenus` 를 만들고, `subMenus[menuNo - 1]` 로 행 하나를 떼어 `String[]` 매개변수에 넘기는 것을 실습으로 배웠다
