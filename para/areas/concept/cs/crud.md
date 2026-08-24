---
type: concept
id: crud
title: CRUD (등록 · 목록 · 조회 · 변경 · 삭제)
aliases:
  - CRUD
  - 크루드
  - create read update delete
  - 등록 목록 조회 변경 삭제
up:
  - 2024-06-18-Day17
  - 2024-06-19-Day18
  - 2024-06-20-Day19
  - 2024-07-05-Day30
  - 2024-08-07-Day52
  - 2024-08-29-Day66
  - 2024-08-13-Day55
tags:
  - 설계
  - cli
  - 자료구조
  - 유지보수
---

# CRUD (등록 · 목록 · 조회 · 변경 · 삭제)

데이터 한 종류를 다루는 프로그램이 갖게 되는 **연산 묶음.** 만들고(Create) 읽고(Read) 고치고(Update) 지우는(Delete) 네 글자이고, 이 필기는 그것을 「등록 · 목록 · 조회 · 변경 · 삭제」 **다섯 개**로 부른다.

## 정의

Read 가 「전체 목록」과 「하나 조회」로 갈리기 때문에 화면은 다섯 개가 된다.

| 명령 | 영어 | 하는 일 | 입력 |
|---|---|---|---|
| 등록 | Create | 필드를 받아 저장소에 넣는다 | 필드 전부 |
| 목록 | Read (전체) | 전부 훑어 요약을 출력한다 | 없음 |
| 조회 | Read (하나) | 번호로 찾아 전부 출력한다 | 번호 |
| 변경 | Update | 번호로 찾아 필드를 다시 받는다 | 번호 + 필드 |
| 삭제 | Delete | 번호로 찾아 저장소에서 뺀다 | 번호 |

**뒤의 세 개는 같은 앞부분을 갖는다** — 번호를 받고, 범위를 검사하고, 없으면 안내하고 `return` 한다 → [[one-based-numbering]]

명령 문자열을 다섯 갈래로 보내는 것이 진입점이다.

```java
public static void excuteUserCommand(String command) {
  System.out.printf("[%s]\n", command);
  switch (command) {
    case "등록": addUser();    break;
    case "목록": listUser();   break;
    case "조회": viewUser();   break;
    case "변경": updateUser(); break;
    case "삭제": deleteUser(); break;
  }
}
```

→ [[switch-statement]] · [[command-loop]]

## 사용 예시

저장소는 배열 하나와 개수 변수 하나다. 이 셋이 한 세트로 움직인다 → [[array]]

```java
private static final int MAX_SIZE = 10;
private static final User[] users = new User[MAX_SIZE];
private static int userLength = 0;
```

다섯 연산이 그 셋을 서로 다르게 만진다.

```java
private static void addUser() {                       // 등록 — 뒤에 붙이고 개수를 늘린다
  User user = new User();
  user.setName(Prompt.input("이름?"));
  user.setEmail(Prompt.input("이메일?"));
  user.setPassword(Prompt.input("암호?"));
  user.setTel(Prompt.input("연락처?"));
  users[userLength++] = user;
}

private static void listUser() {                      // 목록 — 개수만큼 돌며 요약을 찍는다
  System.out.println("번호 이름 이메일");
  for (int i = 0; i < userLength; i++) {
    User user = users[i];
    System.out.printf("%d %s %s\n", i + 1, user.getName(), user.getEmail());
  }
}

private static void viewUser() {                      // 조회 — 번호 검사 뒤 하나를 다 찍는다
  int userNo = Integer.parseInt(Prompt.input("회원번호?"));
  if (userNo < 1 || userNo > userLength) {
    System.out.println("없는 회원입니다.");
    return;
  }
  User user = users[userNo - 1];
  System.out.printf("이름 : %s\n", user.getName());
  ...
}
```

변경은 조회와 앞부분이 같고, 뒤에서 **현재 값을 프롬프트에 보여 주며 다시 받는다** → [[varargs]]

```java
user.setName(Prompt.input("이름(%s):", user.getName()));
```

삭제는 배열에서 요소를 빼는 일이라 따로 다룰 것이 생긴다 → [[array-element-removal]]

### 두 번째 데이터 타입에서 구조가 반복된다

필기가 그것을 한 줄로 적어 뒀다 — 「CRUD의 구성은 기존 회원의 구조와 동일 하다」. `ProjectCommand` 는 `UserCommand` 와 같은 다섯 메서드를 갖고, 저장소 선언도 타입만 바뀐다.

```java
private static final Project[] projects = new Project[MAX_SIZE];
private static int projectLength = 0;
```

그리고 **처음에는 껍데기만 만들어 두고 채운다.**

```java
static void addProject()    { System.out.println("프로젝트 등록"); }
static void listProject()   { System.out.println("프로젝트 목록"); }
static void viewProject()   { System.out.println("프로젝트 조회"); }
```

다섯 갈래로 보내는 부분이 먼저 돌아가게 해 놓고 하나씩 실제 코드로 바꾸는 순서다. `viewProject` 의 마지막 줄에 `System.out.println("프로젝트 조회")` 가 그대로 남아 있는 것이 그 흔적이다.

### 구조가 같다고 코드가 같은 것은 아니다

`Project` 에는 `User[]` 필드가 있어서 등록과 변경이 **한 겹 더 생긴다.** 필드를 받은 뒤 팀원 목록을 관리하는 루프가 붙는다.

```java
static void addProject() {
  Project project = new Project();
  project.setTitle(Prompt.input("프로젝트명?"));
  ...
  addMembers(project);              // 회원 CRUD 에는 없던 단계
  projects[projectLength++] = project;
}

static void updateProject() {
  ...
  deleteMembers(project);           // 하나씩 물어보며 뺀다
  addMembers(project);              // 등록과 같은 루프를 다시 쓴다
}
```

`addMembers` 는 종료 값이 올 때까지 도는 무한 루프다 — 필드 입력처럼 「한 번 묻고 끝」이 아니다 → [[break-continue]] · [[cohesion]]

```java
while (true) {
  int userNo = Prompt.inputInt("추가할 팀원 번호?(종료:0)");
  if (userNo == 0) break;
  User user = UserCommand.findByNo(userNo);
  if (user == null)             { System.out.println("없는 팀원입니다."); continue; }
  if (project.contain(user))    { System.out.printf("'%s'은 현재 팀원입니다.", user.getName()); continue; }
  project.addMember(user);
}
```

### 세 번째 타입에서는 등록이 필드를 다 묻지 않는다

게시판까지 오면 골격은 세 번째 반복이라 새로울 것이 없는데, **등록이 달라진다.** `Board` 의 네 필드 중 사용자에게 묻는 것은 둘뿐이다.

```java
private static void addBoard() {
  Board board = new Board();
  board.setTitle(Prompt.input("제목?"));       // 묻는다
  board.setContent(Prompt.input("내용?"));     // 묻는다
  board.setCreatedDate(new Date());           // 프로그램이 정한다 → [[date-time]]
  boards[boardLength++] = board;              // 조회수는 손대지 않는다 → 0 으로 시작
}
```

회원·프로젝트는 필드가 곧 입력 항목이었는데(팀원 배열만 예외), 여기서는 **입력 항목 · 프로그램이 채우는 값 · 안 채우는 값** 셋으로 갈린다. 조회수는 자동 초기화된 `0` 을 그대로 쓴다 → [[default-initialization]]

조회도 달라진다 — 보여 주기만 하지 않고 **조회수를 하나 올린다.** CRUD 의 R 이 W 를 하는 첫 자리다 → [[read-side-effect]]

```java
Board board = boards[boardNo - 1];
board.setViewCount(board.getViewCount() + 1);
```

### 세 번 반복한 뒤에 다섯 개가 두 층으로 갈린다

같은 골격을 세 타입에 만들어 본 다음 회차에서 **다섯 연산이 각자 두 조각으로 쪼개진다.** 데이터를 만지는 쪽과 사람을 상대하는 쪽이다 → [[cohesion]] · [[grasp]]

| 명령 | UI 쪽 (`UserCommand`) | 데이터 쪽 (`UserList`) |
|---|---|---|
| 등록 | 필드를 묻고 번호를 붙인다 | `add(User)` |
| 목록 | 형식을 정해 찍는다 | `toArray()` |
| 조회 | 번호를 묻고 결과를 찍는다 | `findByNo(int)` |
| 변경 | 현재 값을 보여 주며 다시 묻는다 | `findByNo(int)` |
| 삭제 | 번호를 묻고 안내를 찍는다 | `delete(int)` |

**조회와 변경이 같은 데이터 연산을 쓴다** — 「번호로 하나 찾기」가 한 곳이 되어, 앞부분이 겹치던 것이 이제 **정말로 같은 코드**다. 전날까지는 세 메서드가 각자 검사 코드를 복사해 갖고 있었다.

데이터 쪽은 다섯이 아니라 **여섯**이 된다.

```java
public static void add(User user)        { users[userLength++] = user; }
public static User delete(int userNo)    { ... }
public static User[] toArray()           { ... }
public static User findByNo(int userNo)  { ... }
public static int indexOf(User user)     { ... }
```

`indexOf` 는 화면에서 부르는 연산이 아니라 `delete` 가 쓰는 것이다 — **CRUD 다섯 개에는 없던 내부용 연산**이 저장소 쪽에 생겼다 → [[linear-search]]

UI 쪽 다섯 개는 이제 **배열 이름을 하나도 모른다.**

```java
private static void deleteUser() {
  int userNo = Prompt.inputInt("회원번호?");
  User deletedUser = UserList.delete(userNo);
  if (deletedUser != null) {
    System.out.printf("'%s' 회원을 삭제 했습니다.\n", deletedUser.getName());
  } else {
    System.out.println("없는 회원입니다.");
  }
}
```

전날의 `deleteUser` 는 찾고·검사하고·인덱스를 구하고·당기고·안내까지 다섯 단계였다. **남은 것은 묻기와 안내뿐**이고, 「지웠나 못 지웠나」의 판정도 `delete` 의 반환값이 알려 준다 → [[defensive-copy]] · [[surrogate-key]]

### 일곱 주 뒤 — 데이터 쪽 다섯 연산이 SQL 네 문장이 된다

Day19 에서 다섯 연산을 「화면 쪽 / 데이터 쪽」 두 층으로 가른 뒤 일곱 주, Day52 가 [[dml]] 과 [[dql]] 을 배우며 **그 데이터 쪽이 SQL 로 대체될 수 있다는 것**이 드러난다. 대응이 1:1 이 아니다.

| 명령 | 데이터 쪽 (`UserList`) | SQL |
|---|---|---|
| 등록 | `add(User)` — 배열 끝에 넣고 개수를 늘린다 | `insert into users(...) values(...)` |
| 목록 | `toArray()` — 전부 복사해 돌려준다 | `select * from users` |
| 조회 | `findByNo(int)` — 훑어서 하나 찾는다 | `select * from users where no=?` |
| 변경 | `findByNo` + setter 넷 | `update users set ... where no=?` |
| 삭제 | `delete(int)` + `indexOf` + 배열 당기기 | `delete from users where no=?` |

**세 가지가 눈에 보이게 사라진다.**

- **목록과 조회가 같은 문장이 된다** — `where` 하나 차이다. 자바에서 두 메서드였던 이유는 「입력이 있는가·출력 형식이 무엇인가」였고 그것은 **화면 쪽 사정**이었다. 데이터 쪽에서 둘은 원래 같은 연산이었다.
- **`indexOf` 와 배열 당기기가 없어진다** — `delete from ... where no=?` 는 뒤의 행을 앞으로 옮기지 않는다. [[array-element-removal]] 이 통째로 사라지고, 그 자리에 [[primary-key]] 와 [[database-index]] 가 온다.
- **`MAX_SIZE` 검사 자리가 사라진다** — 대신 [[sql-null]]·[[unique-key]] 같은 제약이 거절한다. 「등록에만 범위 검사가 없다」는 문제가 **애플리케이션에서 풀리는 것이 아니라 옮겨 간다.**

**화면 쪽 다섯 개는 그대로 남는다.** 번호를 묻고 형식을 정해 찍는 일은 SQL 이 대신하지 않으므로, Day19 의 두 층 가르기가 여기서 값을 낸다 — **바꿔 끼워야 할 것이 한쪽에 모여 있다** → [[cohesion]]

### 엿새 뒤 — 다섯 중 넷이 두 테이블에 걸친다

Day55 가 프로젝트의 팀원 목록을 중간 테이블로 옮기자, **다섯 화면 중 넷에 DAO 호출이 하나씩 더 붙는다.** 필기가 「projectCommand 수정」 절에 그 네 줄을 그대로 적어 두었다 → [[db-normalization]] · [[foreign-key]]

| 화면 | 더해진 한 줄 | 왜 |
|---|---|---|
| 등록 | `projectDao.insertMembers(project.getNo(), project.getMembers())` | 팀원을 다른 테이블에 넣는다 → [[generated-keys]] |
| 조회 | `List<User> members = projectDao.getMembers(projectNo)` | 팀원을 다른 테이블에서 읽는다 → [[sql-join]] |
| 변경 | `deleteMembers(projectNo)` + `insertMembers(...)` | 목록을 통째로 다시 맞춘다 |
| 삭제 | `deleteMembers(projectNo)` | 자식 행을 먼저 치운다 |
| **목록** | (없음) | 목록 화면은 팀원을 보여 주지 않는다 |

**목록만 그대로 남는 것이 우연이 아니다** — 이 화면은 요약만 찍으므로 팀원이 필요 없다. 「구조가 같다」가 또 한 번 갈리는 자리이고, 만약 목록에 팀원 수를 함께 보여 주기로 했다면 다섯 번째 줄이 생겼을 것이다(그리고 프로젝트마다 질의를 하나씩 더 부르는 형태가 됐을 것이다) → [[sql-join]] · [[aggregate-function]]

그리고 **변경이 데이터 쪽에서는 「삭제 + 등록」이라는 것**이 여기서 처음 코드로 드러난다. 자바 배열 시절의 `updateProject` 도 `deleteMembers(project)` → `addMembers(project)` 였지만 그때는 메모리 안의 일이라 중간 상태가 남을 곳이 없었다. 문장 둘로 갈린 뒤에는 **그 사이가 저장된다** → [[transaction]]

## 왜 중요한가

**다섯 개가 다 있어야 프로그램을 쓸 수 있다.** 등록만 있으면 넣은 것을 확인할 수 없고, 삭제가 없으면 잘못 넣은 것이 영구히 남는다. 그래서 CRUD 는 기능 목록이라기보다 **데이터 타입 하나를 「다룰 수 있게」 만드는 최소 집합**이고, 새 데이터 타입이 생길 때 무엇을 만들어야 하는지가 세는 일 없이 정해진다.

**두 번째 타입에서 구조가 반복되는 것을 보면 다음에 할 일이 보인다.** `UserCommand` 와 `ProjectCommand` 는 저장소 타입과 필드 이름만 다르고 골격이 같다. 이 중복이 나중에 상속·추상 클래스·제네릭으로 묶고 싶어지는 동기이고, 반대로 **묶기 전에는 같은 버그가 그대로 복사된다** → [[inheritance]] · [[abstract-class]]

**그리고 어디에 무엇을 둘지가 CRUD 를 만들면서 갈린다.** 다섯 메서드가 다 배열을 직접 만지면 저장 방식이 다섯 곳에 퍼지고, 조회처럼 겹치는 단계를 메서드로 뽑으면 그것이 소유자 클래스로 모인다 — 이 필기의 `findByNo`·`contain`·`addMember` 가 그렇게 생겼다 → [[cohesion]]

### 여덟 주 뒤 — 다섯 연산이 화면 다섯이 된다

콘솔 메뉴였던 것이 URL 다섯 개로 옮겨간다. 갈리는 것은 **화면을 두 번 왕복한다**는 점이다.

| 연산 | 콘솔(Day17~19) | 웹(Day65~66) |
|---|---|---|
| 목록 | 한 번의 출력 | `/user/list` |
| 조회 | 번호를 물어 출력 | `/user/view?no=1` |
| 등록 | 입력을 순서대로 받음 | `/user/form` → `/user/add` |
| 변경 | 번호를 물어 값을 다시 받음 | `/user/view`(폼) → `/user/update` |
| 삭제 | 번호를 물어 지움 | `/project/delete?no=1` |

**등록과 변경이 두 화면으로 갈린다** — 폼을 그리는 요청과 값을 받는 요청이 별개다. 콘솔에서는 같은 메서드 안에서 물어보고 받았는데, 웹에서는 그 사이에 요청이 끊긴다. 그래서 **「무엇을 고치는 중인가」를 폼에 실어 보내야** 하고, 그것이 `<input readonly name='no' value='%d'>` 의 역할이다 → [[html-form]]

## 경계와 오해

- **CRUD 는 네 글자인데 화면은 다섯 개다** — Read 가 둘로 갈린다. 목록은 입력이 없고 요약만 찍고, 조회는 번호를 받아 전부 찍는다. 필요한 입력도 출력 형식도 다르므로 한 메서드로 합칠 수 없다.
- **「구조가 동일하다」 ≠ 코드가 동일하다** — `addProject` 는 팀원 관리가 붙어 `addUser` 보다 길고, `updateProject` 는 삭제 루프까지 갖는다. 동일하다고 읽고 복사하면 그 차이가 묻힌다.
- **등록에만 범위 검사가 없다** — 조회·변경·삭제는 번호를 검사하는데 `users[userLength++] = user` 는 아무것도 확인하지 않는다. 배열이 `MAX_SIZE`(10) 로 고정이므로 **11번째 등록에서 `ArrayIndexOutOfBoundsException`** 이다. 「검사는 조회 쪽 일」로 굳으면 이 자리가 빈다 → [[array]]
- **변경이 「고칠 것만」 받지 않는다** — 이 필기의 `updateUser` 는 필드 넷을 다시 다 묻는다. 현재 값을 프롬프트에 보여 주는 것으로 불편을 덮었지만, 엔터만 쳐도 빈 문자열이 그대로 들어가 값이 지워진다. **보여 주는 것과 기본값을 주는 것은 다른 일**이다 → [[varargs]]
- **삭제가 번호를 다시 매긴다** — 목록에서 본 3번을 지우면 4번이 3번이 된다. 처음 두 회차의 번호는 저장된 식별자가 아니라 **지금 목록에서 몇 번째인가**일 뿐이었고, 그 다음 회차에서 데이터가 자기 번호를 갖게 되며 이 문제가 없어진다 → [[array-element-removal]] · [[one-based-numbering]] · [[surrogate-key]]
- **등록의 범위 검사는 쪼갠 뒤에도 여전히 없다** — `UserList.add` 는 `users[userLength++] = user` 한 줄이고 `MAX_SIZE` 를 확인하지 않는다. 배열을 소유하게 되었으므로 **이제는 확인할 정보를 다 갖고 있는데도** 안 한다. 클래스를 옮기는 일이 빠진 검사를 채워 주지는 않는다 → [[cohesion]]
- **다섯 연산이 두 층으로 갈린 것과 계층이 생긴 것은 다르다** — `UserCommand` 는 여전히 `UserList` 를 클래스 이름으로 직접 부르고, 둘 다 `command` 패키지에 있다. 이름이 갈렸을 뿐 **바꿔 끼울 수 있는 경계는 아니다** → [[package]] · [[static-member]]
- **`delete` 가 값을 돌려주는 것과 `void` 인 것은 화면을 바꾼다** — 지운 회원을 돌려주니 `'홍길동' 회원을 삭제 했습니다` 라고 이름을 넣어 찍을 수 있다. 전날의 `void` 삭제는 「삭제했습니다」밖에 못 찍었다. **반환값을 무엇으로 정할지가 UI 가 할 수 있는 말의 범위를 정한다** → [[method]]
- **`switch` 에 `default` 가 없다** — 없는 명령이 오면 아무 일도 없이 프롬프트로 돌아간다. 오류가 아니라 **침묵**이라 사용자는 무엇이 잘못됐는지 알 수 없다 → [[switch-statement]]
- **`excuteUserCommand` 는 `execute` 의 오기다** — 그리고 그 오타가 `excuteProjectCommand`·`excuteBoardCommand` 로 세 번 복사됐다. 구조를 복사하는 것이 이름의 실수까지 복사한다는 예다. **컴파일러가 잡아 주지 않는 실수만 이렇게 살아남는다** — 같은 복사에서 온 `import` 실수는 바로 막혀서 최종 코드에서 정리됐다(아래).
- **「등록은 필드를 다 받는다」가 세 번째 타입에서 깨진다** — `Board` 의 작성날짜는 프로그램이 정하고 조회수는 아무도 채우지 않는다. 「필드 = 입력 항목」으로 굳으면 작성 시각을 사용자에게 묻는 화면을 만들게 된다 → [[date-time]]
- **골격을 복사하면 `import` 도 따라온다** — `BoardCommand` 의 초안은 `import bitcamp.myapp2.vo.User` 를 그대로 갖고 있으면서 정작 쓰는 `Board`·`Date` 는 import 하지 않았다. `UserCommand` 에서 복사한 흔적이고, **이쪽은 컴파일이 막히므로 최종 코드에서 고쳐졌다.** 복사가 남기는 것 중 무엇이 살아남는지를 이름 오타와 나란히 놓고 보면 갈리는 기준이 보인다 → [[java-compilation-unit]]
- **출력 형식은 복사에서 빠져도 조용하다** — `listUser` 의 `printf` 에는 `\n` 이 있었는데 `listBoard` 에는 없어서 목록이 한 줄에 붙어 나온다. 오류가 아니라 **읽을 수 없는 화면**으로만 나타난다 → [[format-string]]
- **CRUD ≠ 번호로 고르는 메뉴 묶음** — 보름 뒤 팀 프로젝트의 소개 문서가 자기 메인 화면을 「CURD : 1 ~ 6까지 메뉴 선택 후 결과값 입출력」이라 적었는데, 그 여섯 개는 과업완료하기 · 아이템사용 · 상점가기 · 업적조회 · 일과종료다. **어느 것도 데이터 한 종류를 만들고 읽고 고치고 지우는 연산이 아니고**, 같은 것은 번호를 받아 다섯 갈래로 보내는 골격뿐이다. 세 타입에 다섯 연산을 세 번 반복해 만든 직후라(→ 위 세 출처) 「번호가 붙은 메뉴 = CRUD」로 이름이 굳은 자리다. CRUD 가 세는 것은 **화면 개수가 아니라 한 데이터 타입을 다룰 수 있는지의 완전성**이고, 그 프로젝트에서 정말 CRUD 인 것은 메뉴가 아니라 **할 일 항목의 상태를 켜고 끄는 부분**이다 → [[command-loop]] · [[gamification]]
- **「삭제가 번호를 다시 매긴다」가 DB 에서 끝나는데, 끝나는 이유가 다르다** — Day19 에서는 **데이터가 자기 번호를 갖게 되어** 풀렸다. Day52 의 `delete from users where no=?` 는 그와 별개로 **애초에 행을 옮기지 않기 때문에** 문제가 없다. 앞은 「번호를 저장해서」이고 뒤는 「자리를 당기지 않아서」라, DB 로 옮기면 이 결함은 설계와 상관없이 사라진다 → [[dml]] · [[primary-key]]
- **「지웠나 못 지웠나」의 판정 방식이 다시 바뀐다** — 자바 쪽 `delete` 는 **지운 회원 객체**를 돌려줘서 `'홍길동' 회원을 삭제 했습니다` 를 찍을 수 있었다. SQL 의 `delete` 는 **영향받은 행 수**만 준다(`0 rows affected`). 이름을 넣어 안내하려면 지우기 전에 `select` 를 한 번 더 해야 하고, 그러면 **화면 하나가 문장 두 개**가 된다 — 그 둘이 함께 성립해야 하므로 [[transaction]] 이 필요해지는 첫 자리다 → [[dml]]
- **SQL 을 배웠다고 CRUD 가 DB 로 넘어가는 것은 아니다** — 옮겨 가는 것은 데이터 쪽 여섯 메서드이고, 번호를 묻고 범위를 안내하고 형식을 정해 찍는 일은 그대로 남는다. 「DB 가 CRUD 를 해 준다」로 읽으면 없어지지 않은 절반이 어디에 있는지를 놓친다 → [[dql]]
- **Day55 의 `deleteMembers` 는 언제나 `false` 를 돌려준다** — 반환 타입이 `boolean` 인데 `try` 블록이 끝난 뒤 `return false` 가 있어서, **삭제가 성공해도 실패로 보고한다.** 짝인 `insertMembers` 는 반대로 언제나 `return true` 다 — 즉 **두 메서드의 반환값 어느 쪽에도 정보가 없다**(하나는 늘 참, 하나는 늘 거짓). 위에 적어 둔 「`delete` 가 값을 돌려주는 것과 `void` 인 것은 화면을 바꾼다」의 뒤집힌 사례다: 값을 돌려주는 시그니처를 골라 놓고 그 값을 만들지 않았으므로, 호출하는 화면이 그것으로 안내를 정하면 **성공한 삭제가 「삭제 실패」로 찍힌다.** 실패를 알리는 진짜 경로는 `throws Exception` 이고, 그렇다면 `boolean` 은 애초에 필요하지 않았다 → [[method]] · [[exception-handling]]
- **「CURD」는 CRUD 의 오기다** — `U` 와 `R` 이 뒤집혔다. 네 글자를 「크루드」라는 소리로 외우면 순서가 남지 않아서 생기는 오타이고, 컴파일러도 검색도 잡아 주지 않아 문서에 그대로 남는다. 실제로 그 프로젝트 문서에는 한 번뿐인 그 단어가 뒤집힌 채로 있다.

## 함께 보는 개념

- [[one-based-numbering]] — 번호를 받는 세 연산이 공유하는 검사와 변환
- [[array-element-removal]] — 삭제가 실제로 하는 일
- [[cohesion]] — 다섯 연산이 배열을 어디까지 직접 만지는가
- [[array]] — 저장소와 개수 변수의 짝
- [[switch-statement]] — 명령을 다섯 갈래로 보내는 문법
- [[command-loop]] — 이 명령들을 부르는 상위 구조
- [[varargs]] — 현재 값을 보여 주며 다시 묻는 프롬프트
- [[encapsulation]] — 필드를 닫고 getter/setter 로 채우는 등록·변경의 전제
- [[break-continue]] — 팀원 추가 루프의 종료와 재시도
- [[read-side-effect]] — 조회가 조회수를 올리며 R 이 W 를 하는 자리
- [[date-time]] — 등록이 사용자에게 묻지 않고 채우는 값
- [[format-string]] — 목록·조회의 출력 형식
- [[surrogate-key]] — 다섯 연산이 받는 번호의 성격이 바뀐 자리
- [[linear-search]] — 조회·변경·삭제가 공유하게 된 데이터 연산
- [[defensive-copy]] — 목록이 저장소를 만지지 않게 되는 방법
- [[grasp]] — 다섯 연산을 두 층으로 가르는 근거
- [[gamification]] — 같은 골격 위에 CRUD 가 아닌 명령들이 올라간 예
- [[dml]] — 등록·변경·삭제가 옮겨 가는 문장들
- [[dql]] — 목록과 조회가 하나로 합쳐지는 문장
- [[transaction]] — 화면 하나가 문장 여럿이 될 때 필요해지는 경계
- [[primary-key]] — 배열 인덱스가 하던 「번호」의 자리
- [[database-index]] — `findByNo` 의 훑기를 대신하는 구조
- [[foreign-key]] · [[db-normalization]] — 화면 넷이 두 테이블에 걸치게 된 이유
- [[sql-join]] — 갈라진 테이블을 조회 화면에서 되붙이는 문법
- [[generated-keys]] — 등록이 두 문장으로 갈릴 때 그 둘을 잇는 값
- [[jdbc]] — 다섯 화면이 부르는 데이터 쪽이 사는 층

## 출처

- [[2024-06-18-Day17]] — 회원에 대해 등록·목록·조회·변경·삭제 다섯 메서드를 만들고, 같은 구조를 프로젝트에 한 번 더 만들며 「CRUD의 구성은 기존 회원의 구조와 동일 하다」는 것을 실습으로 배웠다. 프로젝트는 팀원 배열 때문에 등록·변경에 한 겹이 더 붙는다는 것도 이 자리에서 나왔다
- [[2024-06-19-Day18]] — 같은 골격을 게시판에 세 번째로 만들며, 반복되는 것과 타입마다 달라지는 것이 갈렸다. 등록이 작성날짜를 스스로 채우고 조회수는 아무도 채우지 않으며 조회가 조회수를 올린다는 것 — 즉 **필드가 곧 입력 항목이 아니라는 것**이 이 자리에서 나왔다
- [[2024-06-20-Day19]] — 세 번 반복한 골격을 두 클래스로 갈라, 다섯 연산이 각자 「데이터 연산 + 화면 처리」로 쪼개졌다. 조회와 변경이 같은 `findByNo` 를 쓰게 되어 겹치던 앞부분이 실제로 한 곳이 되었고, `delete` 가 지운 회원을 돌려주며 UI 가 이름을 넣어 안내할 수 있게 되었다. 화면에서 부르지 않는 `indexOf` 가 저장소 쪽에만 생긴 것도 이 자리다
- [[2024-07-05-Day30]] — 이 개념이 **잘못 적용된 표본**이다. 팀 토이 프로젝트의 메인 화면을 「CURD : 1 ~ 6까지 메뉴 선택 후 결과값 입출력」이라 적었는데 그 여섯 개는 CRUD 연산이 아니라 게임 명령들이고(→ [[gamification]]), 오기까지 함께 남았다. 골격을 세 번 반복한 뒤 **번호 메뉴 전체를 CRUD 라 부르게 된 자리**로 읽는다
- [[2024-08-29-Day66]] — 여덟 주 뒤. 변경·삭제 화면이 서블릿으로 만들어져 **다섯 연산이 URL 다섯 개로 옮겨간다.** 등록·변경이 「폼을 그리는 요청」과 「값을 받는 요청」 둘로 갈리는 것이 콘솔과 갈리는 지점이고, 그래서 고칠 대상의 번호를 폼에 실어 보낸다. 프로젝트 변경은 `update` → `deleteMembers` → `insertMembers` 세 문장이라 **연산 하나가 문장 여럿**이 되는데, 그 묶음이 커밋 하나로 감싸지지 않은 것은 이 회차에도 그대로다 → [[transaction]]
- [[2024-08-07-Day52]] — 다섯 연산의 **데이터 쪽이 SQL 네 문장으로 대응된다**는 것이 드러나는 회차다. `insert`·`update`·`delete`(→ [[dml]])와 `select`(→ [[dql]])를 배우면서 목록과 조회가 `where` 유무만 다른 한 문장이 되고, `indexOf` 와 배열 당기기·`MAX_SIZE` 검사가 자리를 잃는다. 이 회차 자체는 CRUD 를 언급하지 않는다 — 필기는 SQL 문법을 다루고, 다섯 연산과의 대응은 Day17~19 의 코드와 나란히 놓아야 보이는 것이라 여기에 적는다
- [[2024-08-13-Day55]] — **다섯 화면 중 넷이 두 테이블에 걸치게 되는 회차**다. 팀원 목록을 중간 테이블로 옮기고 「projectCommand 수정」 절에 등록·조회·변경·삭제에 더해진 DAO 호출을 한 줄씩 적었는데(`insertMembers`·`getMembers`·`deleteMembers`), **목록 화면만 손대지 않았다** — 요약에는 팀원이 없기 때문이다. 변경이 데이터 쪽에서 「삭제 + 등록」이라는 것도 여기서 코드로 드러난다. 다만 새로 만든 DAO 메서드의 반환값이 짝이 어긋나 있다 — `insertMembers` 는 언제나 `true`, `deleteMembers` 는 `try` 뒤에 `return false` 가 있어 **언제나 `false`** 다
