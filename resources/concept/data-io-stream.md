---
type: concept
id: data-io-stream
title: 데이터 입출력 스트림 (Data I/O Stream)
aliases:
  - 데이터 스트림
  - 데이터 입출력 스트림
  - Data I/O Stream
  - DataInputStream
  - DataOutputStream
  - readUTF
  - writeUTF
  - 타입 단위 입출력
up:
  - 2024-07-19-Day39
  - 2024-07-23-Day41
tags:
  - java
  - 입출력
  - 데이터
  - 프로토콜
---

# 데이터 입출력 스트림 (Data I/O Stream)

**바이트 스트림을 감싸서 「바이트 몇 개」가 아니라 「`int` 하나」·「문자열 하나」 단위로 읽고 쓰게 해 주는 층.** Day39 의 한 줄이 쓰임을 그대로 말한다 — 「File I/O Stream을 Dataa I/O Stream에 장착하여 Int,UTF,IEE-754를 읽어온다」. **장착한다**는 말이 정확하다. 이것은 통로가 아니라 통로에 끼우는 껍데기다 → [[decorator-pattern]]

## 정의

`DataOutputStream`·`DataInputStream` 은 타입마다 메서드 한 짝을 준다. **쓰는 메서드와 읽는 메서드가 1:1 로 대응하고, 그 짝이 형식을 정한다.**

| 타입 | 쓰기 | 읽기 | 파일에 남는 것 |
|---|---|---|---|
| `int` | `writeInt` | `readInt` | 4바이트 고정, 상위 바이트 먼저 |
| `double` | `writeDouble` | `readDouble` | 8바이트, IEEE-754 → [[floating-point]] |
| `boolean` | `writeBoolean` | `readBoolean` | 1바이트 (`0` 또는 `1`) |
| `String` | `writeUTF` | `readUTF` | **길이 2바이트 + 수정 UTF-8 바이트** |

**Day38 이 손으로 짠 것이 정확히 이 표다.** 같은 코드를 두 회차가 나란히 적어 놓은 셈이다.

| | Day38 (손으로) | Day39 (표준으로) |
|---|---|---|
| `int` 내보내기 | `out.write(no >> 24)` … 네 줄 | `out.writeInt(no)` |
| `int` 되읽기 | `in.read() << 24 \| in.read() << 16 \| …` | `in.readInt()` |
| 문자열 내보내기 | `getBytes(UTF_8)` + 길이 2바이트 + 내용 | `out.writeUTF(name)` |
| 문자열 되읽기 | 길이 2바이트 읽고 `new String(buffer, 0, len, UTF_8)` | `in.readUTF()` |
| 객체 한 벌 | `User.getBytes()` / `User.valueOf(byte[])` | **삭제** (「user.java에 valueOf, getBytes는 삭제」) |

Day38 의 `getBytes`·`valueOf` 가 지워진 것이 이 회차의 실질이다 — **형식을 만드는 코드가 아니라 형식을 부르는 코드만 남는다** → [[serialization]] · [[length-prefix-framing]]

## 사용 예시

두 자원을 `;` 로 나란히 선언해 **통로와 껍데기를 따로 만든다.**

```java
  private void loadUser() {
    try (FileInputStream in0 = new FileInputStream("user.data");
        DataInputStream in = new DataInputStream(in0)) {
      int userLength = in.readInt();
      int maxUserNum = 0;
      for (int i = 0; i < userLength; i++) {
        User user = new User();
        user.setNo(in.readInt());
        user.setName(in.readUTF());
        user.setEmail(in.readUTF());
        user.setPassword(in.readUTF());
        user.setTel(in.readUTF());
        userList.add(user);

        maxUserNum = Math.max(maxUserNum, user.getNo());
      }
      User.initSeqNo(maxUserNum);
    } catch (IOException e) {
      System.out.println("회원 정보 로딩 중 오류 발생" + e.getMessage());
    }
  }
```

쓰는 쪽이 **거울인 것이 한눈에 보인다** — Day38 에서는 두 메서드를 나란히 놓고 세 줄씩 대조해야 알 수 있던 것이다.

```java
  private void saveUser() {
    try (FileOutputStream out0 = new FileOutputStream("user.data");
        DataOutputStream out = new DataOutputStream(out0)) {

      out.writeInt(userList.size());

      for (User user : userList) {
        out.writeInt(user.getNo());
        out.writeUTF(user.getName());
        out.writeUTF(user.getEmail());
        out.writeUTF(user.getPassword());
        out.writeUTF(user.getTel());
      }
    } catch (IOException e) {
      System.out.println("회원 정보 저장 중 오류 발생" + e.getMessage());
    }
  }
```

**두 층이 한 층으로 합쳐졌다.** Day38 은 「객체 하나의 형식」(`User.getBytes`)과 「목록의 형식」(`saveUser`)을 갈라 두었고, 레코드마다 길이 접두사를 하나 더 적었다. 여기서는 필드를 바로 스트림에 쓰므로 **레코드 길이가 사라진다** — 그것을 쓰지 않았기 때문에 잃는 것도 없다 → [[length-prefix-framing]]

### 나흘 뒤 — 같은 층을 실습에서 떼어 최소 형태로 다시 본다

Day41 은 목록도 예외 처리도 없이 **필드 셋을 순서대로 쓰고 순서대로 읽는 것**만 남긴다.

```java
    out.writeUTF(member.name);
    // 2) 나이 출력 (4바이트)
    out.writeInt(member.age);
    // 3) 성별 출력 (1바이트)
    out.writeBoolean(member.gender);
```

```java
    member.name = in.readUTF();
    // 2) 나이(int) 읽기
    member.age = in.readInt();
    // 3) 성별 읽기
    member.gender = in.readBoolean();
```

**두 조각이 거울인 것이 여기서 가장 짧게 보인다** — Day39 에서는 목록 루프와 `catch` 에 묶여 있던 것이다. 주석의 「(4바이트)」·「(1바이트)」가 이 노트의 표를 필기가 스스로 적어 둔 것이고, **개수 접두사가 없는 것**은 저장할 것이 하나여서다 → [[serialization]]

그런데 **이 회차의 필기가 이 층의 구조를 상속으로 설명한다** — 「Data I/O stream은 File I/O stream을 상속받아 사용한다」. 그리고 그 이해가 **코드의 모양으로 그대로 나타난다.**

```java
    DataFileOutputStream out = new DataFileOutputStream("temp/test4_2.data");
```

`DataFileOutputStream` 이라는 클래스는 없고, **파일 이름을 받는 생성자도 없다.** 이 두 가지가 우연이 아니다 — 「`FileOutputStream` 을 상속했다」면 부모의 생성자(파일 이름)를 물려받을 것이고 클래스 이름에 `File` 이 들어가는 것도 자연스럽다. **틀린 모형이 존재하지 않는 API 를 그럴듯하게 만들어 낸 자리**이고, 실제 형태는 Day39 가 이미 쓴 것이다 → [[decorator-pattern]]

```java
    try (FileOutputStream out0 = new FileOutputStream("temp/test4_2.data");
        DataOutputStream out = new DataOutputStream(out0)) {
```

대가는 **`User` 가 자기 형식을 모르게 됐다**는 것이다. Day38 의 `getBytes()` 는 「내 필드를 바이트로 만드는 법」을 `User` 안에 두었는데, 이제 필드를 하나 더하면 `saveUser`·`loadUser` 두 곳을 고쳐야 한다. **표준 도구를 쓰면서 응집이 한 칸 내려간 자리**이고, 필기는 이 교환을 적지 않았다 → [[cohesion]]

## 왜 중요한가

**대칭을 사람이 아니라 클래스가 보증한다.** Day38 의 위험은 「쓰는 쪽과 읽는 쪽이 어긋나면 조용히 밀린다」였고 그 대칭은 두 메서드에 흩어져 있었다. `writeInt`↔`readInt`, `writeUTF`↔`readUTF` 는 **이름이 짝이라 눈으로 대조된다** — 형식이 코드의 순서에서 **메서드 이름의 나열**로 올라온다 → [[serialization]]

**바이트 순서가 명세로 고정된다.** Day38 은 `no >> 24` 를 먼저 쓴 것이 big-endian 이라는 뜻이었고 그 약속은 코드 순서에만 있었다. `DataOutputStream` 은 **상위 바이트 먼저를 규격으로 못 박아** 다른 언어·다른 기계에서 읽을 때도 기준이 문서에 있다 → [[binary-io]] · [[platform-dependency]]

**끝을 값이 아니라 예외로 알려 준다.** `read()` 는 스트림 끝에서 `-1` 을 돌려주므로 Day38 의 `len = in.read() << 8 | in.read()` 가 잘린 파일에서 `-1` 이 되어 `new byte[-1]` 로 죽었다. `readInt` 는 **4바이트를 다 못 채우면 `EOFException`** 을 던진다 — `IOException` 의 하위라 기존 `catch` 에 걸리고, 「값이 이상해져서 뒤가 무너지는」 경로가 **「예외가 나서 멈추는」 경로로 바뀐다.** 다만 그것이 끝이 아니다(아래 「경계와 오해」) → [[exception-handling]]

## 경계와 오해

- **`writeUTF` 의 UTF 는 표준 UTF-8 이 아니다 (수정 UTF-8)** — 두 곳이 다르다. 문자 `U+0000` 을 1바이트 `00` 이 아니라 2바이트로 적고, 보조 평면 문자(이모지 등)를 4바이트 하나가 아니라 **서로게이트 쌍을 각각 3바이트씩 6바이트로** 적는다. 그래서 `writeUTF` 로 쓴 바이트를 다른 언어의 UTF-8 디코더에 그대로 넣으면 이모지에서 깨진다. **`readUTF` 로 되읽는 한 문제가 없다** — Java 안에서 왕복하는 형식이라 그렇다. 「UTF 라고 적혀 있으니 UTF-8 이다」가 통하지 않는 대표적인 자리 → [[character-encoding]] · [[unicode]]
- **`writeUTF` 의 한계가 65535 바이트이고, 이번에는 그것이 예외로 드러난다** — 길이 접두사가 2바이트이므로 Day38 의 손코드와 **한계가 똑같다.** 다른 것은 넘겼을 때다 — Day38 은 `out.write(len >> 8)` 이 상위 비트를 말없이 버려 **저장은 되고 못 읽는 파일**이 남았고, `writeUTF` 는 `UTFDataFormatException` 을 던진다. **같은 형식의 같은 한계인데 한쪽은 조용하고 한쪽은 알려 준다** — 표준 도구를 쓰는 값의 절반이 이 「알려 준다」다 → [[length-prefix-framing]] · [[overflow]]
- **개수 접두사가 2바이트에서 4바이트로 올라갔다** — Day38 은 회원 수를 `out.write(userLength >> 8); out.write(userLength);` 로 2바이트에 적어 65536명째부터 조용히 어긋났다. `out.writeInt(userList.size())` 는 4바이트라 그 한계가 사라진다. **고친 것이 아니라 표준 메서드의 크기가 그런 것**이고, 필기에 이 차이는 적혀 있지 않다.
- **`EOFException` 이 잡히는 것이 안전하다는 뜻은 아니다 — 반쪽 목록이 남는다** — 파일이 중간에서 잘리면 `readUTF` 가 `EOFException` 을 던지고 `catch (IOException)` 이 메시지를 찍는다. 그런데 **그 전까지 읽은 회원들은 이미 `userList.add(user)` 로 들어가 있다.** 프로그램은 「일부만 든 목록」으로 계속 돌고, 다음 `saveUser` 가 **그 반쪽을 파일에 확정한다** — 잘린 데이터가 정상 데이터로 승격되는 경로다. Day38 의 `RuntimeException` 은 프로그램을 죽여서 최소한 저장을 못 하게 막았는데, **예외가 잘 잡히게 된 것이 데이터 손실을 조용하게 만든 셈**이다. 되읽기는 임시 목록에 담고 끝까지 성공했을 때만 `userList` 에 넘기는 것이 답이다 → [[exception-handling]] · [[serialization]]
- **`readInt` 가 4바이트를 「부분만」 읽고 예외를 던지면 스트림 위치는 되돌아오지 않는다** — 예외는 「아무 일도 없었다」가 아니라 「여기까지 먹고 실패했다」다. 그래서 잡은 뒤에 이어서 읽는 것은 성립하지 않고, 이 코드처럼 **읽기를 포기하는 것 말고는 답이 없다.**
- **`DataInputStream` 은 버퍼가 아니다** — 감싸면 타입 단위로 읽게 되지만 **시스템 호출 횟수는 줄지 않는다.** `readInt` 하나가 안쪽 `FileInputStream` 의 `read()` 를 네 번 부르는 것에 가깝고, Day38 에 지적된 「버퍼를 감싸지 않으면 `read()` 한 번이 시스템 호출 한 번」이 그대로 남아 있다. 답은 겹을 하나 더 끼우는 것이다 — `new DataInputStream(new BufferedInputStream(new FileInputStream(f)))`. **데코레이터라서 성능 층을 이렇게 나중에 끼울 수 있다** → [[io-stream]] · [[decorator-pattern]]
- **Data I/O ≠ Object I/O** — 이 층은 **타입은 알지만 객체는 모른다.** 필드를 몇 개 어떤 순서로 쓸지는 여전히 사람이 정하고 두 메서드에 흩어져 있다. `ObjectOutputStream` 은 그 순서까지 자동으로 정해 주는 대신 클래스 구조에 묶인다 — 같은 노트의 다음 절이 그쪽으로 간다 → [[serialization]]
- **타입 단위 ≠ 자기 서술적** — 파일에는 `writeInt` 로 적은 4바이트와 `writeUTF` 로 적은 바이트가 구별 없이 이어져 있다. **어느 바이트가 무슨 타입인지 파일에 없고 읽는 순서에만 있다.** 필드 순서를 한 칸 바꿔 읽으면 `readInt` 가 문자열의 앞 4바이트를 정수로 해석하고, 예외 없이 엉뚱한 번호가 들어온다. Day38 에서 지적된 「형식이 곧 계약」이 도구를 바꿔도 그대로다 → [[binary-io]]
- **감싼 껍데기를 닫아야 안쪽이 비워진다** — `DataOutputStream` 을 닫으면 안쪽 `FileOutputStream` 도 닫힌다. 반대로 안쪽만 닫으면 껍데기가 들고 있던 것이 나가지 않을 수 있다. Day39 는 두 자원을 `try (A; B)` 로 선언해 **선언의 역순으로**(껍데기 먼저) 닫히게 했고, 그것이 이 문법이 역순을 택한 이유다 → [[try-with-resources]]
- **`readUTF` 는 `null` 을 왕복시키지 못한다** — `writeUTF(null)` 은 `NullPointerException` 이다. 회원의 전화번호를 입력하지 않아 `null` 인 경우 저장 자체가 실패하고, 이 코드에는 그 검사가 없다. Day38 의 `name.getBytes(...)` 도 같은 문제를 갖고 있었으므로 **도구를 바꿔도 남는 구멍**이다 → [[object-reference]]
- **「File I/O stream을 상속받아 사용한다」는 틀렸다 — 감싸는 것이다 (Day41 필기의 오류)** — `DataOutputStream` 의 부모는 `FilterOutputStream` 이고, `FileOutputStream` 과는 **형제 관계**(둘 다 `OutputStream` 의 자손)다. 관계는 상속이 아니라 **필드로 들고 있는 것**이다. 이 구분이 말장난이 아닌 이유는 **가능한 조합이 달라지기 때문**이다 — 상속이라면 「파일용 Data 스트림」·「소켓용 Data 스트림」·「메모리용 Data 스트림」이 각각 클래스여야 하고, 감싸는 것이라면 `DataOutputStream` **하나**가 그 셋 모두에 씌워진다. Day39 가 `new DataInputStream(in0)` 로 이미 그 형태를 썼는데도 나흘 뒤 필기가 상속이라 적은 것은, **문법(`extends`)이 아니라 「무엇이 무엇을 이용한다」는 느낌으로 관계를 읽었기** 때문이다 → [[decorator-pattern]] · [[inheritance]] · [[composite-pattern]]
- **그 오류가 존재하지 않는 클래스 이름을 만들어 냈다** — 코드의 `DataFileOutputStream`·`DataFileInputStream` 은 JDK 에 없다. 이름에 `File` 이 들어간 것과 **생성자가 파일 이름을 받는 것**이 둘 다 「상속받았다」는 모형의 자연스러운 귀결이다(부모의 생성자를 물려받았을 것이므로). 실제 `DataOutputStream` 의 생성자는 **`OutputStream` 하나만** 받고 파일 이름을 받는 판이 없으며, **그것이 이 클래스가 파일에 묶이지 않은 증거**다. **틀린 모형은 컴파일 오류로 드러나기 전에 「그럴듯한 API」를 상상하게 만든다** — 필기의 두 예제가 그 상태로 남아 있다.
- **`writeboolean`·`readboolean` 이 아니라 `writeBoolean`·`readBoolean` 이다** — 필기의 설명 줄은 소문자로, 바로 아래 코드는 대문자로 적혀 있어 **같은 노트 안에서 갈린다.** 표준 라이브러리는 camelCase 를 지키므로 소문자 판은 존재하지 않는 메서드다.
- **Day41 의 `Member` 는 컴파일되지 않는다 — 이 층과 무관한 두 가지 이유로** — ① 필드 선언이 `public String member;` 인데 코드는 `member.name` 을 읽고 쓴다(선언에 `name` 이 없다). ② `Member` 가 **`static` 없는 내부 클래스**라 `Test` 인스턴스 없이는 만들 수 없는데 `static main` 에서 `new Member()` 를 부른다. **직렬화 대상 클래스를 중첩 클래스로 두면 이 문제가 늘 따라오고**, 그래서 저장할 데이터 클래스는 최상위나 `static` 중첩으로 두는 것이 관례다 → [[nested-class]] · [[static-member]]
- **저장할 것이 하나면 개수 접두사가 필요 없다 — 그리고 그 형식은 늘릴 수 없다** — Day39 는 `writeInt(userList.size())` 로 개수를 먼저 적었고 Day41 은 그것이 없다. 파일에 정확히 한 건만 있으므로 맞는 코드인데, **나중에 두 건을 담으려면 형식 자체를 바꿔야 한다**(개수를 앞에 넣거나 `EOFException` 까지 읽는 루프로). 「필드를 순서대로 쓴다」와 「몇 개가 있는지 적는다」는 다른 층의 결정이고, 최소 예제는 뒤쪽을 생략한 것이다 → [[length-prefix-framing]] · [[serialization]]

## 함께 보는 개념

- [[io-stream]] — 이 껍데기가 끼워지는 통로
- [[decorator-pattern]] — 껍데기로 끼우는 구조 자체
- [[binary-io]] — 이 층이 만들어 내는 형식의 성격
- [[length-prefix-framing]] — `writeUTF` 가 안에서 쓰는 규칙
- [[serialization]] — 이 층으로 객체를 저장하는 작업
- [[character-encoding]] — 수정 UTF-8 이 표준과 갈리는 자리
- [[floating-point]] — `writeDouble` 이 쓰는 규칙
- [[exception-handling]] — 스트림 끝을 예외로 알리는 쪽
- [[try-with-resources]] — 겹쳐 만든 자원을 닫는 순서
- [[cohesion]] — 형식을 아는 코드가 `User` 밖으로 나간 자리
- [[overflow]] — 접두사 한계를 넘길 때의 두 가지 결말
- [[inheritance]] — 이 층의 관계로 잘못 읽히는 쪽
- [[buffered-stream]] — 같은 자리에 함께 끼우는 성능 층
- [[nested-class]] — 저장할 클래스를 중첩으로 두면 걸리는 것

## 출처

- [[2024-07-19-Day39]] — 「File I/O Stream을 Dataa I/O Stream에 장착하여 Int,UTF,IEE-754를 읽어온다」로 이 층의 쓰임을 적고, `loadUser`/`saveUser` 를 `readInt`·`readUTF`/`writeInt`·`writeUTF` 로 다시 썼다. **Day38 이 손으로 짠 `User.getBytes()`·`User.valueOf(byte[])` 는 이 회차에 삭제된다**(「user.java에 valueOf, getBytes는 삭제」) — 비트 시프트로 `int` 를 쪼개던 코드와 레코드 길이 접두사가 함께 사라진다. `try (FileInputStream in0 = …; DataInputStream in = new DataInputStream(in0))` 로 통로와 껍데기를 나란히 선언하는 형태가 나오고, 회원 수 접두사가 2바이트에서 `writeInt` 의 4바이트로 바뀐다. **수정 UTF-8·65535 한계·`EOFException` 이후에 반쪽 목록이 남는 문제는 필기에 없다**
- [[2024-07-23-Day41]] — 실습에서 떼어 낸 **최소 형태**로 이 층을 다시 본다 — 목록·예외 처리 없이 `writeUTF`/`writeInt`/`writeBoolean` 셋과 그 거울인 `readUTF`/`readInt`/`readBoolean` 셋만 남겨, 두 조각이 대칭이라는 것이 가장 짧게 보인다. 주석의 「(4바이트)」·「(1바이트)」가 타입별 크기를 필기가 직접 적어 둔 것이다. 다만 이 층의 구조를 **「Data I/O stream은 File I/O stream을 상속받아 사용한다」로 잘못 적었고**, 그 모형이 코드의 모양으로 그대로 나타난다 — 존재하지 않는 `DataFileOutputStream`·`DataFileInputStream` 에 **파일 이름을 넘기는** 형태다(실제 생성자는 `OutputStream` 하나만 받는다). Day39 가 이미 `new DataInputStream(in0)` 로 쓴 형태인데도 관계를 상속으로 읽은 자리다. 설명 줄의 `writeboolean`·`readboolean` 은 소문자라 존재하지 않는 메서드이고, `Member` 클래스는 필드 이름(`member` 선언 / `.name` 사용)과 `static` 없는 내부 클래스라는 두 가지 이유로 컴파일되지 않는다. 개수 접두사·`EOFException`·버퍼 겹은 이 회차에도 다루지 않았다
