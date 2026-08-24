---
type: concept
id: parameterization
title: 매개변수화 (Parameterization)
aliases:
  - 매개변수화
  - 파라미터화
  - parameterize
  - parameterization
  - 매개변수 추출
  - extract parameter
  - 하드코딩 제거
up:
  - 2024-06-13-Day14
  - 2024-06-18-Day17
tags:
  - 리팩터링
  - 설계
  - 메서드
  - 재사용
---

# 매개변수화 (Parameterization)

메서드가 **안에 박아 두었거나 밖에서 직접 읽던 값**을 매개변수로 받게 바꾸는 것. 하는 일은 그대로 두고 **무엇에 대해 하는지를 부르는 쪽이 고르게** 만드는 리팩터링이다.

## 정의

세 단계다.

1. 그 메서드가 무엇에 의존하는지 찾는다 — 리터럴, 클래스 필드, 상수
2. 그 의존을 매개변수로 올린다 → [[parameter-and-argument]]
3. 부르는 쪽이 무엇을 넘길지 고른다

문법적으로는 매개변수 하나를 더하는 것뿐이다.

```java
static String prompt() {                      // 프롬프트가 "> " 로 고정
    System.out.print("> ");
    return keyboardScanner.nextLine();
}

static String prompt(String title) {          // 부르는 쪽이 정한다
    System.out.printf("%s> ", title);
    return keyboardScanner.nextLine();
}
```

**메서드가 하는 일은 바뀌지 않았다** — 한 줄 출력하고 한 줄 읽는다. 바뀐 것은 「무엇을 출력할지 누가 정하는가」다.

## 사용 예시

이 필기의 실습은 메인 메뉴만 있던 프로그램에 서브메뉴를 붙이면서 같은 리팩터링을 두 군데에 했다.

첫째는 프롬프트다. 위치를 보여 주려면 `"메인> "` 과 `"메인/회원> "` 이 둘 다 필요한데, 문자열이 메서드 안에 박혀 있어 하나밖에 만들 수 없었다.

```java
String command = prompt("메인");                    // 메인 루프
String command = prompt("메인/" + menuTitle);       // 서브 루프
```

둘째가 이 필기가 「리팩토링」이라 적은 자리다. 검증과 조회 메서드가 클래스 필드 `menus` 를 직접 읽고 있어서, 서브메뉴 배열로는 부를 수 없었다.

```java
// 변경 전 — 필드 menus 에 묶여 있다
static boolean isValidateMenu(int menuNo) {
    return menuNo >= 1 && menuNo <= menus.length;
}
static String getMenuTitle(int menuNo) {
    return isValidateMenu(menuNo) ? menus[menuNo - 1] : null;
}

// 변경 후 — 어느 배열이든 받는다
static boolean isValidateMenu(int menuNo, String[] menus) {
    return menuNo >= 1 && menuNo <= menus.length;
}
static String getMenuTitle(int menuNo, String[] menus) {
    return isValidateMenu(menuNo, menus) ? menus[menuNo - 1] : null;
}
```

**본문은 한 글자도 바뀌지 않았다.** `menus.length` 도 `menus[menuNo - 1]` 도 그대로인데, `menus` 가 가리키는 것이 필드에서 매개변수로 바뀌었다 → 「경계와 오해」

그 결과 같은 두 메서드가 메인 메뉴와 서브메뉴 양쪽에서 불린다.

```java
String menuTitle = getMenuTitle(menuNo, mainMenus);     // 메인 루프
String subMenuTitle = getMenuTitle(menuNo, menus);      // 서브 루프 — 넘어온 행
```

넘기는 것이 [[multidimensional-array]] 의 행 하나이므로, 이 메서드는 서브메뉴가 2차원 배열에서 왔다는 사실을 알 필요가 없다.

### 다음 회차에서 같은 메서드가 한 칸 더 나아간다

며칠 뒤 실습 프로젝트는 이 `prompt` 를 `util` 패키지의 `Prompt.input` 으로 옮기면서 매개변수를 **형식 문자열과 가변 인수**로 바꿨다 → [[varargs]] · [[package]]

```java
// Day14 — 문구를 부르는 쪽이 정한다
static String prompt(String title) {
    System.out.printf("%s> ", title);
    return keyboardScanner.nextLine();
}

// Day17 — 문구에 끼워 넣을 값까지 부르는 쪽이 정한다
public static String input(String format, Object... args) {
    System.out.printf(format + " ", args);
    return keyboardScanner.nextLine();
}
```

바뀐 것은 **고정돼 있던 마지막 조각**이다. Day14 의 `prompt` 는 `"%s> "` 라는 모양을 안에 갖고 있어서 `메인/회원> ` 같은 프롬프트만 만들 수 있었다. 형식 자체를 받으면 같은 메서드가 프롬프트도 만들고 현재 값을 보여 주는 질문도 만든다.

```java
Prompt.input("이름?");                                  // 그냥 묻는다
Prompt.input("이름(%s):", user.getName());              // 현재 값을 보여 주며 묻는다
Prompt.input("추가할 팀원 번호?(종료:0)");                // 안내를 붙여 묻는다
```

**의존이 또 한 층 위로 갔다.** `Prompt` 는 이제 회원도 프로젝트도 모르고, 무엇을 물을지는 전부 `command` 쪽이 안다 → [[cohesion]]

## 왜 중요한가

**이것이 없으면 선택은 복사뿐이다.** 서브메뉴용 `getSubMenuTitle` 을 따로 만들면 같은 판정이 두 곳에 살게 되고, `menuNo - 1` 규칙이나 검증 범위를 고칠 때 한쪽만 고치는 날 조용히 어긋난다. [[method]] 로 뽑아 중복을 없앤 것이 여기서 다시 무너지는 셈이다.

두 번째는 **호출부만 읽어도 무엇에 대한 호출인지 안다**는 것이다. `getMenuTitle(menuNo)` 는 어느 목록을 뒤지는지 메서드 안을 봐야 알 수 있지만 `getMenuTitle(menuNo, mainMenus)` 는 한 줄로 드러난다. 매개변수 목록은 **그 메서드가 무엇에 의존하는지의 목록**이고, 필드로 읽는 의존은 그 목록에서 빠져 있다 → [[static-member]]

세 번째는 **재사용 가능성이 이름이 아니라 의존이 정한다**는 것이다. `prompt()` 는 이름만 보면 어디서든 쓸 것 같지만 프롬프트 모양이 박혀 있어 이 프로그램 전용이었다. 밖으로 가져갈 수 있는지는 **같이 가져가야 하는 것이 몇 개인가**로 판정된다.

## 경계와 오해

- **매개변수가 같은 이름의 필드를 가린다** — 변경 후의 `isValidateMenu(int menuNo, String[] menus)` 는 필드 `menus` 가 아직 있는 채로 만들어졌고, 본문의 `menus` 는 그 순간부터 **매개변수**를 뜻한다. 코드가 그대로여서 무엇을 보고 있는지 읽어서는 알 수 없고, 같은 클래스의 다른 메서드는 여전히 필드를 본다 — 같은 이름이 두 곳을 가리키는 상태다. 최종 코드가 필드를 `mainMenus` 로 바꾼 것이 이 모호함을 없앤 조치다 → [[variable]]
- **매개변수화 ≠ 매개변수를 늘리는 것** — 목적은 **감춰진 의존을 드러내는 것**이다. 메서드가 실제로 쓰지 않는 값을 받게 만들면 호출부마다 넘길 것만 늘어난다. 반대로 매개변수가 다섯 개로 늘었다면 대개 **한 덩어리인 개념을 쪼개 넘기고 있다**는 신호이고, 그것을 묶는 것이 클래스가 필요해지는 자리다 → [[instance]]
- **의존은 없어지지 않고 호출부로 옮겨 간다** — `getMenuTitle` 이 `mainMenus` 를 몰라도 되게 된 대신 `main` 이 `mainMenus` 와 `subMenus` 를 둘 다 알아야 한다. 매개변수화는 의존을 **한 층 위로 모으는** 것이고, 그 층이 조립을 담당하게 된다.
- **전부 올리는 것이 답은 아니다** — 이 필기는 `keyboardScanner` 는 필드로 남겼다. 프로그램 전체에 하나뿐이고 다른 것으로 부를 일이 없기 때문이다. 기준은 「밖의 것을 읽는가」가 아니라 **다른 값으로 부를 일이 있는가**다 → [[standard-input]]
- **기존 호출부를 전부 고쳐야 한다** — 매개변수를 더하면 인수 없이 부르던 코드가 컴파일되지 않는다. 이 필기는 `prompt()` 호출을 전부 `prompt("메인")` 으로 고쳤다. 옛 형태를 남기려면 같은 이름의 메서드를 둘 두고 하나가 다른 하나를 부르게 한다(오버로딩) — 그러면 부르는 쪽을 안 고쳐도 되지만 **기본값이 어디 적혀 있는지가 흐려진다** → [[method]]
- **하드코딩된 값이 하나뿐일 때는 매개변수가 아니라 상수가 답일 수 있다** — 여러 곳에서 다른 값이 필요할 때 매개변수가 값을 하고, 한 곳에서 이름만 필요할 때는 변수·상수로 뽑는 것이 맞다 → [[variable]]
- **매개변수화해도 판단은 여전히 한 곳에 있다** — `menuNo - 1` 로 인덱스를 맞추는 규칙과 1부터 시작하는 번호 체계는 `getMenuTitle` 안에 남았다. 매개변수로 올릴 것은 **달라지는 것**이고, 모든 호출에서 같은 것은 안에 두는 것이 맞다 → [[one-based-numbering]]
- **끝까지 올리면 검사가 없어진다** — `prompt(String title)` 은 문구를 받아 `"%s> "` 에 넣기만 하므로 잘못될 것이 없다. 형식 문자열 자체를 받는 `input(String format, Object...)` 은 형식과 인수의 짝을 부르는 쪽이 맞춰야 하고, 안 맞으면 실행 중에 터진다. **매개변수화가 자유를 늘릴 때 그만큼의 책임도 호출부로 옮겨 간다** → [[varargs]]
- **매개변수화와 옮기기는 다른 일이다** — `prompt` 를 `input` 으로 바꾼 것과 그것을 `util.Prompt` 로 옮긴 것은 같은 회차에 일어났지만 별개의 결정이다. 매개변수화가 **옮길 수 있게 만든** 것이고(도메인 의존이 남아 있으면 옮겨도 같이 끌려온다), 옮기는 것은 그 뒤의 선택이다 → [[package]]

## 함께 보는 개념

- [[method]] — 중복을 없애는 앞 단계. 매개변수화는 그것이 다른 맥락에서도 통하게 만든다
- [[parameter-and-argument]] — 값을 받는 자리와 넘기는 값
- [[static-member]] — 필드로 감춰진 의존이 사는 곳
- [[multidimensional-array]] — 넘겨받는 값이 행 하나인 자리
- [[command-loop]] — 같은 메서드가 두 층에서 불리는 구조
- [[call-by-value]] — 넘긴 배열이 어떻게 전달되는가
- [[variable]] — 이름이 무엇을 가리키는지의 문제
- [[varargs]] — 매개변수 개수까지 호출부가 정하게 하는 다음 칸
- [[package]] — 의존이 걷힌 메서드를 옮겨 두는 자리
- [[cohesion]] — 무엇을 물을지 아는 쪽과 묻는 방법만 아는 쪽의 분리
- [[one-based-numbering]] — 올리지 않고 안에 남긴 판단

## 출처

- [[2024-06-13-Day14]] — 서브메뉴를 붙이면서 `prompt()` 에 `title` 을, `isValidateMenu`·`getMenuTitle` 에 `String[] menus` 를 매개변수로 더해 메인 메뉴와 서브메뉴가 같은 메서드를 쓰게 만드는 것을 배웠다. 필기의 주석이 「main 과 sub 둘다 사용 가능」이라고 그 목적을 적어 뒀다
- [[2024-06-18-Day17]] — 같은 메서드가 `Prompt.input(String format, Object... args)` 로 한 칸 더 나아가, 문구뿐 아니라 거기에 끼워 넣을 값까지 부르는 쪽이 정하게 되는 것을 배웠다. 도메인 의존이 남지 않아 `util` 패키지로 옮길 수 있게 된 것도 이 자리다
