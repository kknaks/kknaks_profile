---
type: concept
id: serialization
title: 직렬화 (Serialization)
aliases:
  - 직렬화
  - 역직렬화
  - serialization
  - deserialization
  - marshalling
  - 객체 저장
up:
  - 2024-07-18-Day38
  - 2024-07-19-Day39
  - 2024-07-22-Day40
tags:
  - java
  - 입출력
  - 설계
  - 데이터
---

# 직렬화 (Serialization)

**메모리 안의 객체를 한 줄로 늘어선 바이트로 바꾸는 것.** 되돌리는 쪽을 역직렬화라 한다. 객체는 참조로 이어진 그물인데 파일과 네트워크는 **바이트 한 줄**만 받으므로, 그 사이에 「어떤 순서로 늘어놓을지」를 정하는 일이 반드시 들어간다.

## 정의

Day38 은 그 일을 표준 도구 없이 **메서드 두 개로 손으로** 만든다.

| 방향 | 메서드 | 하는 일 |
|---|---|---|
| 직렬화 | `byte[] getBytes()` | 필드를 정한 순서로 바이트에 쌓는다 |
| 역직렬화 | `static User valueOf(byte[])` | 같은 순서로 떼어 내 객체를 채운다 |

**이 둘은 거울이어야 한다.** 순서·크기·개수 중 한 곳만 어긋나면 그 지점부터 뒤가 전부 밀리고, 밀린 결과는 예외가 아니라 **엉뚱한 값**으로 나타난다.

```text
getBytes()   no(4) | len(2) name | len(2) email | len(2) password | len(2) tel
valueOf()    no(4) | len(2) name | len(2) email | len(2) password | len(2) tel
             └──────────── 이 두 줄이 형식(format)이고, 사양서는 코드뿐이다 ────────────┘
```

### 하루 뒤, 같은 일을 표준 도구로 세 번 다시 한다

Day39 는 이 손코드를 지우고(「user.java에 valueOf, getBytes는 삭제」) 같은 저장·로딩을 **세 가지 방식으로 갈아 끼운다.** 갈리는 축은 「형식을 누가 아는가」다.

| 방식 | 형식을 아는 것 | 파일에 들어가는 것 | 사양서의 위치 |
|---|---|---|---|
| Day38 손코드 | 내가 짠 `getBytes`/`valueOf` | 내가 정한 바이트 배치 | **내 코드 두 개** |
| Data I/O Stream | `writeInt`/`readUTF` 등 표준 메서드 | 타입별 규격 바이트 | **메서드 호출 순서** → [[data-io-stream]] |
| Object I/O Stream | JVM (`Serializable`) | 클래스 이름·필드 이름·값 | **클래스 구조 자체** |
| CSV | `toCsvString`/`valueOf(String)` | 사람이 읽는 텍스트 | **필드 순서** → [[csv]] |
| JSON (Gson) | **라이브러리** (`toJson`/`fromJson`) | 이름과 값이 든 텍스트 | **클래스의 필드 이름** → [[json]] |

**아래로 갈수록 내가 쓰는 코드가 줄고 내가 못 바꾸는 것이 늘어난다.** Object I/O 는 필드 순서를 적을 필요조차 없어지는 대신 **클래스를 고치는 것이 파일 형식을 고치는 일**이 된다.

마지막 줄은 사흘 뒤 Day40 이 더한 것이다 — **형식을 아는 주체가 내 코드 밖으로 완전히 나간다.**

## 사용 예시

내보내는 쪽. 필드마다 「고정 4바이트」또는「길이 2바이트 + 내용」으로 쌓는다.

```java
//유저정보를 바이트배열로 변환 
public byte[] getBytes() throws IOException {
    try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
      //회원번호 넣기
      out.write(no >> 24);
      out.write(no >> 16);
      out.write(no >> 8);
      out.write(no);

      //이름 넣기
      byte[] bytes = name.getBytes(StandardCharsets.UTF_8);
      out.write(bytes.length >> 8);
      out.write(bytes.length);
      out.write(bytes);

      /* email · password · tel 도 같은 세 줄 */

      return out.toByteArray();
    }
  }
```

되돌리는 쪽. 같은 순서로 읽어 setter 로 채운다.

```java
// 데이터 배열을 유저 객체로 전환
public static User valueOf(byte[] bytes) throws IOException {
    try (ByteArrayInputStream in = new ByteArrayInputStream(bytes)) {
      User user = new User();
      user.setNo(in.read() << 24 | in.read() << 16 | in.read() << 8 | in.read());

      byte[] buffer = new byte[10000];
      int len = in.read() << 8 | in.read();
      in.read(buffer, 0, len);
      user.setName(new String(buffer, 0, len, StandardCharsets.UTF_8));

      /* email · password · tel 도 같은 네 줄 */
      return user;
    }
  }
```

**`getBytes` 의 세 줄과 `valueOf` 의 네 줄이 필드마다 짝을 이루고 그 짝이 곧 형식이다** → [[length-prefix-framing]] · [[byte-array-stream]]

그리고 객체 하나가 아니라 **목록 전체**를 다루는 층이 하나 더 있다.

```java
private void saveUser() {
    try (FileOutputStream out = new FileOutputStream("user.data")) {
      int userLength = userList.size();
      out.write(userLength >> 8);
      out.write(userLength);

      for (User user : userList) {
        byte[] bytes = user.getBytes();
        out.write(bytes.length >> 8);
        out.write(bytes.length);
        out.write(bytes);
      }
    } catch (IOException e) {
      System.out.println("회원 정보 저장 중 오류 발생" + e.getMessage());
    }
  }
```

**두 층으로 나눈 것이 이 설계의 핵심이다** — `User` 는 자기 필드만 알고, 목록을 몇 개 담을지와 각 레코드가 몇 바이트인지는 밖의 층이 안다. 그래서 `User` 에 필드를 더할 때 `saveUser` 를 손대지 않아도 된다 → [[cohesion]]

읽는 쪽도 같은 두 층이다.

```java
 private void loadUser() {
    try (FileInputStream in = new FileInputStream("user.data")) {
      int userLength = in.read() << 8 | in.read();
      int maxUserNum = 0;
      for (int i = 0; i < userLength; i++) {
        int len = (in.read() << 8) | in.read();
        byte[] bytes = new byte[len];
        in.read(bytes);

        User user = User.valueOf(bytes);
        userList.add(user);

        maxUserNum = Math.max(maxUserNum, user.getNo());
      }
      User.initSeqNo(maxUserNum);
    } catch (IOException e) {
      System.out.println("회원 정보 로딩 중 오류 발생" + e.getMessage());
    }
  }
```

**마지막 줄 `User.initSeqNo(maxUserNum)` 이 이 코드에서 가장 중요한 한 줄이다** — 필드를 다 복원해도 발급기는 복원되지 않기 때문이다(아래 「경계와 오해」) → [[surrogate-key]]

### Day39 — 형식을 짜는 코드가 한 줄로 줄어든다

Day39 §2 는 `User` 에 `implements Serializable` 을 붙이고(「객체가 Serializble 인터페이스를 받아 구현체로 역할을 한다」) 목록 전체를 **한 번의 호출로** 내보낸다.

```java
    private void saveUser() {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("user.data"))) {
        out.writeObject(userList);
        } catch (IOException e) {
        System.out.println("회원 정보 저장 중 오류 발생" + e.getMessage());
        }
    }
```

```java
    private void loadUser() {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("user.data"))) {

        userList = (List<User>) in.readObject();
        int maxUserNum = 0;
        for (User user : userList) {
            maxUserNum = Math.max(maxUserNum, user.getNo());
        }
        User.initSeqNo(maxUserNum);
        } catch (IOException  | ClassNotFoundException e) {
        System.out.println("회원 정보 로딩 중 오류 발생" + e.getMessage());
        userList = new ArrayList<>();
        }
    }
```

**`out.writeObject(userList)` 한 줄이 Day38 의 두 층(레코드 형식 + 목록 형식)을 전부 대신한다.** 회원 수를 적는 줄도, 레코드 길이를 적는 줄도, 필드를 순서대로 쌓는 줄도 없다 — `List` 안의 `User` 들과 그 안의 문자열까지 **참조를 따라가며 JVM 이 알아서 늘어놓는다.**

그리고 `User.initSeqNo(maxUserNum)` 은 그대로 남아 있다 — **Day38 의 손코드부터 Day40 의 Gson 까지 도구를 네 번 바꿔도 이 줄은 매번 손으로 써야 한다.** 직렬화가 데려가지 않는 상태가 있다는 것이 도구의 문제가 아니라는 증거다 → [[static-member]]

`catch` 에 `ClassNotFoundException` 이 붙은 것이 이 방식의 정체를 알려 준다 — **파일 안에 클래스 이름이 문자열로 들어 있어서** 되읽을 때 그 이름으로 클래스를 찾는다. Day38 의 형식에는 찾을 이름이 없었으므로 이 예외도 없었다 → [[class-metadata]] · [[exception-handling]]

### 사흘 뒤, 형식을 짜는 코드가 아예 없어진다

Day40 은 `getBytes`·`toCsvString` 계열의 메서드를 **하나도 만들지 않는다.** 형식을 만드는 일 전체가 라이브러리 호출 두 개로 들어간다.

```java
        out.write(gson.toJson(boardList));
```

```java
        boardList.addAll(new Gson().fromJson(strBuilder.toString(), new TypeToken<List<Board>>() {
        }));
```

Object I/O 와 겉모습이 비슷한데 **갈리는 것이 「무엇을 형식의 근거로 삼는가」**다. `writeObject` 는 클래스 이름·필드 이름·타입을 다 적어 JVM 이 되돌리므로 그 파일은 **Java 만 읽는다.** Gson 은 필드 이름과 값만 적으므로 다른 언어·다른 도구가 읽고, 대신 **어떤 타입으로 되돌릴지를 읽는 쪽이 알려 줘야 한다**(`TypeToken`) → [[json]] · [[type-erasure]]

| | Object I/O (Day39) | Gson (Day40) |
|---|---|---|
| 파일에 든 것 | 클래스 이름 + 필드 이름 + 값 | **필드 이름 + 값** |
| 되돌릴 타입을 아는 것 | 파일 (그래서 `ClassNotFoundException`) | **부르는 쪽** (`TypeToken`·`Class<E>`) |
| 다른 언어에서 읽기 | 불가능 | 가능 |
| 필드 이름을 바꾸면 | `InvalidClassException` — **터진다** | 그 필드가 `null` — **조용하다** |

**마지막 줄이 이 선택의 값이자 대가다.** 자동화가 깊어질수록 실패가 시끄러워지고, 얕아질수록 조용해진다 → [[exception-handling]]

## 왜 중요한가

**객체가 저장소 밖에서 살아남는다.** Day19 가 만든 「3번 회원」은 배열 없이도 성립하는 이름이었는데, 그 성질을 실제로 쓸 수 있게 되는 것이 여기다 — 프로그램을 끄고 다시 켜도 같은 3번이 돌아온다. 「데이터가 자기를 말할 수 있다」와 「그 말을 파일에 적을 수 있다」는 한 걸음 차이이고 그 걸음이 직렬화다 → [[surrogate-key]] · [[db-normalization]]

**저장·전송·캐시가 한 문제가 된다.** 파일에 적는 것, 소켓으로 보내는 것, 메모리 밖에 넣어 두는 것이 전부 「객체를 바이트로 만들어야 한다」로 같아진다. 통로가 바뀌어도 `getBytes()` 는 그대로다 → [[io-stream]] · [[caching]]

**형식이 곧 호환성 계약이 된다.** 한번 파일을 쓰기 시작하면 `getBytes()` 를 바꾸는 일이 「내부 구현 변경」이 아니라 **「이미 저장된 파일을 못 읽게 만드는 변경」**이 된다. 클래스의 필드 목록이 캡슐화 뒤에 숨어 있지 않고 파일 형식으로 밖에 노출된 셈이고, 그것이 직렬화가 설계에 남기는 제약이다 → [[encapsulation]]

## 경계와 오해

- **형식을 라이브러리에 맡겨도 형식이 없어지지는 않는다 — 「필드 이름」으로 옮겨 갈 뿐이다** — Day38 은 **필드 순서**가 형식이었고 Day39 의 CSV 도 그랬다. Gson 을 쓰면 순서는 상관없어지는 대신 **필드 이름이 형식**이 된다. `tel` 을 `phone` 으로 고치는 리팩터링이 그 순간 **파일 형식 변경**이 되고, 옛 파일을 읽으면 `phone` 이 `null` 로 남는다 — **컴파일러도 라이브러리도 아무 말을 하지 않는다.** 「내부 이름은 자유롭게 바꿀 수 있다」가 직렬화 대상 클래스에서는 성립하지 않고, Gson 의 `@SerializedName` 처럼 **파일에 나갈 이름을 코드에 못 박는 장치**가 그래서 있다 → [[json]] · [[refactoring]] · [[encapsulation]]
- **순환 참조를 도구마다 다르게 다룬다** — `writeObject` 는 이미 내보낸 객체를 기억하며 참조 그래프를 따라가므로 A→B→A 가 있어도 한 번씩만 적고 되돌릴 때 관계까지 복원한다. Gson 은 **필드를 따라 내려가며 텍스트를 만드는 것뿐**이라 같은 구조에서 무한히 파고들어 `StackOverflowError` 를 낸다. 실습 프로젝트에서 `Project` 가 팀원 `User` 목록을 갖고 `User` 가 참여 프로젝트를 되가리키게 만드는 순간 걸리는 자리이고, **「객체는 참조로 이어진 그물이다」라는 첫 문장이 여기서 다시 청구서로 돌아온다** → [[json]] · [[object-reference]]
- **직렬화 ≠ Java 의 `Serializable` — Day38 에는 `Serializable` 이 아예 없고, Day39 에 와서 둘이 한 노트에 같이 있다** — Day38 은 `implements Serializable` 도 `ObjectOutputStream` 도 쓰지 않는다. 그래서 그 시점에는 「직렬화를 배웠다」가 「`Serializable` 을 배웠다」가 아니었다. **Day39 §2 가 그 표준 쪽을 실제로 쓴다** — `User implements Serializable` 을 붙이고 `writeObject`/`readObject` 로 왕복한다. 두 방식의 차이는 그대로 남는다: 표준 쪽은 클래스 이름·필드 이름·타입까지 함께 적어 자동으로 되돌려 주는 대신 파일이 커지고 클래스 구조가 바뀌면 깨지고, 손으로 쓴 쪽은 **형식이 내 것**이라 작고 규칙이 명확하지만 **대칭을 사람이 지켜야 한다.** 실무에서 JSON·Protobuf 를 쓰는 것은 손으로 형식을 정하는 이쪽 계열이다.
- **`Serializable` 은 구현할 메서드가 없다 — 「인터페이스를 받아 구현체가 된다」의 예외다** — Day39 는 「객체가 Serializble 인터페이스를 받아 구현체로 역할을 한다」로 적었는데, 이 인터페이스에는 **메서드가 하나도 없다.** 구현할 것이 없고 「이 클래스는 내보내도 된다」는 **표시만 하는 마커 인터페이스**다. Day23 부터 배운 인터페이스가 「무엇을 할 수 있는지 약속하는 것」이었던 것과 역할이 다르고, 그래서 `writeObject` 가 하는 일도 그 클래스의 코드가 아니라 **JVM 이 클래스 구조를 들여다보며** 한다 → [[interface]] · [[annotation]]
- **역직렬화는 그 클래스의 생성자를 부르지 않는다 — Day38 의 setter 경로보다 더 깊이 우회한다** — Day38 의 `valueOf` 는 `new User()` 와 setter 를 지나갔으므로 최소한 그 코드가 실행됐다. `readObject` 는 **`User` 의 생성자도 setter 도 부르지 않고** 필드에 값을 직접 꽂는다(부르는 것은 직렬화 대상이 아닌 최상위 부모의 기본 생성자뿐이다). `private` 필드도 그대로 채워지고, 생성자에 넣어 둔 검사(필수값·범위)는 **전부 건너뛰어진다.** 「객체는 생성자를 통해서만 만들어진다」가 깨지는 자리이고, 그래서 신뢰할 수 없는 파일을 `readObject` 로 읽는 것이 보안 취약점으로 취급된다 → [[constructor]] · [[encapsulation]]
- **`serialVersionUID` 를 적지 않으면 클래스를 고치는 순간 옛 파일을 못 읽는다** — 값을 안 적으면 JVM 이 클래스 구조(필드 이름·타입·메서드 시그니처)에서 계산해 파일에 넣는다. 그래서 필드를 하나 더하거나 이름을 바꾸면 계산값이 달라지고, 옛 파일을 읽을 때 `InvalidClassException` 이 난다 — **컴파일러가 경고하지 않고 실행에서만 드러난다.** Day38 의 손코드에 「버전이 파일에 없다」로 남았던 문제가 여기서는 **버전이 있고 대신 너무 엄격한** 쪽으로 뒤집힌 것이다. 필드를 더해도 옛 파일을 읽으려면 상수를 직접 박아 두어야 하고 Day39 의 `User` 에는 그것이 없다.
- **`(List<User>) in.readObject()` 는 컴파일러가 검사하지 못하는 형변환이다** — `readObject()` 의 반환 타입은 `Object` 이고, 제네릭 타입 인자는 실행 시점에 지워져 있어 **「`List` 인지」만 확인되고 「안에 `User` 가 들었는지」는 확인되지 않는다.** 다른 것이 든 파일을 읽어도 이 줄은 통과하고, 나중에 `for (User user : userList)` 에서 `ClassCastException` 이 난다 — **오류가 원인에서 멀어진 자리**에 나타난다. 컴파일 경고(unchecked)가 뜨는데 이 코드는 그것을 그대로 둔다 → [[type-casting]]
- **파일 형식이 `ArrayList` 라는 구현 클래스에 묶인다** — `writeObject(userList)` 는 「목록」이 아니라 **그 순간의 구현 클래스**를 적는다. 나중에 `LinkedList` 로 바꾸면 새 코드는 옛 파일을 읽을 수 있지만(`List` 로 받으므로) **파일에는 여전히 `ArrayList` 가 들어 있고**, 읽어 온 것은 `LinkedList` 가 아니다. `userList = (List<User>) in.readObject()` 가 필드를 **통째로 갈아 끼우기** 때문에, 다른 코드가 옛 리스트 참조를 들고 있었다면 그쪽은 갱신되지 않는다 → [[object-reference]] · [[dynamic-array]]
- **`transient` 가 없으면 모든 필드가 나간다** — 비밀번호처럼 내보내고 싶지 않은 필드도 자동으로 포함된다. 손코드에서는 「쓰지 않으면 안 나간다」였는데 표준 직렬화는 **반대로 「빼겠다고 적어야 안 나간다」**다. 자동화의 방향이 뒤집히는 자리이고, Day39 의 `User` 에는 `transient` 가 없다.
- **Day39 의 `catch` 는 처음으로 상태를 복구한다** — `userList = new ArrayList<>();` 한 줄이 붙었다. Day38 의 `catch` 는 메시지만 찍어 첫 실행(파일 없음)에서 목록이 어떤 상태인지 코드로 보장되지 않았는데, 여기서는 **빈 목록으로 되돌린다.** Day11 의 「어떤 상태를 되돌려야 다시 시도할 수 있는가」에 이 파일 층에서 처음 답한 줄이다. 다만 **정상 상태(첫 실행)가 오류 메시지를 내는 문제는 그대로**고, 깨진 파일과 없는 파일도 여전히 구별되지 않는다 → [[exception-handling]]
- **필드를 복원하는 것과 상태를 복원하는 것이 다르다** — `no`·`name`·`email` 을 다 되돌려도 `User.seqNo` 는 되돌아오지 않는다. **`static` 카운터는 어느 인스턴스의 필드도 아니라서 직렬화 대상에 아예 들어가지 않는다.** `initSeqNo(maxUserNum)` 이 그 구멍을 메우는 줄이고, 이 줄이 없으면 다음 등록이 1번을 다시 발급해 **같은 번호를 가진 회원이 둘** 생기고 `findByNo` 가 앞의 것만 돌려준다 → [[static-member]] · [[surrogate-key]]
- **그 카운터를 파일에서 「세는 것」과 「저장하는 것」은 다르다 — 이 코드는 세고 있어서 지운 번호가 되살아난다** — `maxUserNum` 은 남아 있는 회원들의 최댓값이다. 5번까지 발급한 뒤 5번을 지우고 저장하면 파일의 최댓값은 4가 되고, 다음 실행에서 카운터가 4로 복원되어 **새 회원이 5번을 다시 받는다.** Day19 가 「지운 번호는 다시 나오지 않는다」를 이 번호 체계의 성질로 적었는데, **파일 왕복을 한 번 거치면 그 성질이 깨진다.** 카운터 자체를 파일에 적었다면 유지됐고, 이 코드는 예외도 경고도 없이 조용히 성질을 잃는다 → [[surrogate-key]]
- **역직렬화가 생성자가 아니라 `static` 메서드인 것은 이유가 있다 — 그런데 그 이유가 여기서 반만 살았다** — `valueOf(byte[])` 를 `new User(byte[])` 로도 쓸 수 있는데 정적 팩토리로 갔다. 생성자는 이름이 클래스 이름으로 고정이라 「바이트에서 만든다」와 「필드로 만든다」를 구별할 수 없고, 실패했을 때 `null` 이나 다른 것을 돌려줄 여지도 없다. 다만 이 구현은 안에서 `new User()` 로 빈 객체를 만들고 setter 로 채우므로 **완성되지 않은 `User` 가 실제로 존재하는 순간이 있고**, 중간에 예외가 나면 반쯤 채워진 객체가 만들어지던 중이었다는 사실만 남는다 → [[constructor]] · [[immutability]]
- **잘린 파일을 만나면 예외가 `catch` 를 통과해 프로그램을 죽인다** — `catch (IOException e)` 는 「오류 발생」을 찍고 넘어가도록 쓰였지만, 파일이 중간에서 끊기면 `in.read()` 가 `-1` 을 돌려주고 `len = -1 << 8 | -1` 이 **`-1`** 이 된다. `loadUser` 쪽에서는 `new byte[-1]` 이 `NegativeArraySizeException`, `valueOf` 쪽에서는 `in.read(buffer, 0, -1)` 이 `IndexOutOfBoundsException` 이다. **둘 다 `IOException` 이 아니라 `RuntimeException` 이라 이 `catch` 에 걸리지 않고 밖으로 나간다** — 「읽기 실패는 메시지만 찍고 계속한다」로 짠 코드가 실제 실패에서는 예외를 던지며 멈춘다. 형식이 어긋난 입력을 방어하는 코드가 형식 안에 없기 때문이다 → [[exception-handling]] · [[length-prefix-framing]]
- **저장 실패가 조용하다** — `saveUser` 의 `catch` 는 메시지를 찍고 끝나므로 **부른 쪽은 저장이 됐는지 알 수 없다.** 그리고 `new FileOutputStream("user.data")` 는 여는 순간 기존 파일을 비우므로, 중간에 실패하면 **옛 데이터도 없고 새 데이터도 반쪽인 파일**이 남는다. 다음 실행의 `loadUser` 가 그것을 읽으려 하고 위 항목의 경로로 들어간다. Day11 의 「예외를 잡는 것이 고치는 것은 아니다」가 파일 층에서 반복되는데, 이번에는 되돌릴 상태가 **메모리가 아니라 디스크**라 훨씬 비싸다 → [[exception-handling]] · [[try-with-resources]]
- **첫 실행의 「파일 없음」과 「파일 깨짐」이 구별되지 않는다** — `user.data` 가 없으면 `FileNotFoundException` 이 나고 그것도 `IOException` 이라 같은 `catch` 로 들어와 「회원 정보 로딩 중 오류 발생」을 찍는다. **정상 상태(처음 실행)가 오류 메시지를 내고 있고**, 진짜 오류와 같은 화면을 쓴다.
- **`User.getBytes()` 와 `String.getBytes()` 는 같은 이름의 다른 일이다** — `String.getBytes(charset)` 는 **인코딩 규칙 하나**를 적용해 문자를 바이트로 바꾸고, `User.getBytes()` 는 여러 필드를 순서대로 이어 붙인 **형식**을 만든다. 후자가 전자를 안에서 부르므로 한 메서드 안에 두 층이 같은 이름으로 나타난다. 인자가 있는지 없는지가 구별의 유일한 단서다 → [[character-encoding]] · [[method]]
- **레코드 순서가 형식의 일부인데 아무도 그렇게 취급하지 않는다** — `for (User user : userList)` 가 목록 순서로 쓰고 `userList.add(user)` 가 읽은 순서로 담으므로 순서가 보존된다. 그래서 **목록의 구현을 순서 없는 것으로 바꾸면 저장·로드마다 순서가 흔들린다** — 형식 문서에 적히지 않은 약속이 하나 더 있는 셈이다.
- **버전이 파일에 없다** — `User` 에 필드를 하나 더하면 `getBytes` 는 다섯 벌을 쓰고 `valueOf` 는 다섯 벌을 읽으려 하는데, 네 벌만 든 옛 파일에는 그 표시가 없다. 읽는 쪽은 **형식이 다르다는 것을 알 방법 없이** 위의 잘린 파일 경로로 들어간다. 형식 맨 앞에 버전 번호 한 바이트를 두는 것이 이 문제의 표준 답이고, **손으로 쓴 직렬화가 표준 직렬화보다 먼저 만나는 대가**가 이것이다.

## 함께 보는 개념

- [[binary-io]] — 바이트로 적는 방식 자체
- [[data-io-stream]] — 타입별 규칙을 표준이 대신 짜는 층
- [[csv]] — 같은 일을 사람이 읽는 텍스트로 하는 형식
- [[json]] — 형식을 짜는 일을 라이브러리에 넘긴 네 번째 방식
- [[type-erasure]] — 되돌릴 타입을 부르는 쪽이 알려 줘야 하는 이유
- [[class-metadata]] — 표준 직렬화가 파일에 함께 적는 것
- [[type-casting]] — `readObject()` 의 결과를 받는 자리
- [[length-prefix-framing]] — 이 형식이 가변 길이를 다루는 방법
- [[byte-array-stream]] — 바이트를 모으고 되읽는 그릇
- [[try-with-resources]] — 통로를 닫는 문법
- [[io-stream]] — 바이트가 나가는 통로
- [[character-encoding]] — 문자열 필드가 바이트가 되는 규칙
- [[surrogate-key]] — 파일에 적히는 식별 번호와 되살려야 하는 발급기
- [[static-member]] — 직렬화가 데려가지 않는 상태가 사는 곳
- [[exception-handling]] — 형식이 어긋났을 때 무엇이 던져지는가
- [[constructor]] — 역직렬화가 객체를 만드는 방법을 고르는 자리
- [[encapsulation]] — 필드 목록이 파일 형식으로 밖에 나가는 문제
- [[caching]] — 같은 변환이 쓰이는 다른 자리
- [[db-normalization]] — 데이터를 밖에 두는 다음 단계

## 출처

- [[2024-07-18-Day38]] — 실습 프로젝트의 회원 정보를 파일로 저장하고 되읽는 코드 전체가 손으로 쓴 직렬화다. `User.getBytes()` 가 `no` 를 4바이트 고정으로, 네 문자열 필드를 「길이 2바이트 + UTF-8 바이트」로 쌓고 `User.valueOf(byte[])` 가 같은 순서로 되돌린다. 목록 층은 `saveUser`/`loadUser` 가 맡아 회원 수와 레코드 길이를 앞에 적는다 — **객체 하나의 형식과 목록의 형식이 두 층으로 갈린 것**이 이 코드의 구조다. 마지막에 `User.initSeqNo(maxUserNum)` 로 발급기를 되살리지만 **남은 회원의 최댓값을 세는 방식**이라 지운 번호가 재발급되고, 형식이 어긋난 파일에서는 `len` 이 `-1` 이 되어 `catch (IOException)` 이 잡지 못하는 예외가 나간다. 파일 형식에 버전 표시가 없고 저장 실패가 부른 쪽에 전달되지 않는다
- [[2024-07-19-Day39]] — 손으로 쓴 `getBytes`·`valueOf(byte[])` 를 **삭제하고** 같은 저장·로딩을 표준 도구로 세 번 다시 짠다 — `DataInputStream`/`DataOutputStream`, `ObjectInputStream`/`ObjectOutputStream`, 그리고 CSV. §2 에서 `User implements Serializable` 을 붙이고 「객체가 Serializble를 구현하면 Object I/O Stream을 통해 인스턴스된 객체를 byte[]로 변환 할 수 있다」로 적었으며, `out.writeObject(userList)` 한 줄이 Day38 의 레코드 형식·목록 형식 두 층을 전부 대신한다. `catch (IOException | ClassNotFoundException)` 이 **파일에 클래스 이름이 들어 있다는 것**을 드러내고, `catch` 에 `userList = new ArrayList<>()` 가 붙어 **처음으로 실패 후 상태를 되돌린다.** 반대로 `serialVersionUID`·`transient` 가 없고 `(List<User>) in.readObject()` 의 검사되지 않는 형변환을 그대로 두며, `User.initSeqNo(maxUserNum)` 을 세는 방식은 세 도구 모두에서 Day38 그대로 남는다
- [[2024-07-22-Day40]] — 네 번째 방식으로 **Gson** 을 쓴다. `gson.toJson(boardList)` 와 `fromJson(문자열, new TypeToken<List<Board>>() {})` 두 호출이 형식을 짜는 코드 전체를 대신하고, **이 회차에는 `getBytes`·`toCsvString` 류의 메서드를 하나도 만들지 않는다.** Object I/O 와 달리 파일에 클래스 이름이 없어 **되돌릴 타입을 부르는 쪽이 알려 줘야 하고**, 그래서 `TypeToken`·`Class<E>` 가 시그니처에 나타난다. 형식의 근거가 「필드 순서」에서 「필드 이름」으로 옮겨 가며 필드 이름을 바꾸는 리팩터링이 파일 형식 변경이 되었고, `Board.initSeqNo(maxBoardNo)` 를 손으로 부르는 줄은 네 번째 도구에서도 그대로 남는다 — 다만 `getInterfaces()` + `getMethod("initSeqNo", int.class)` 로 **부르는 방법만** 일반화됐다
