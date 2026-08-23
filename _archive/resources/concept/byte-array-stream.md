---
type: concept
id: byte-array-stream
title: 바이트 배열 스트림 (ByteArrayStream)
aliases:
  - 바이트 배열 스트림
  - ByteArrayOutputStream
  - ByteArrayInputStream
  - byte array stream
  - 메모리 스트림
  - 메모리 버퍼
up:
  - 2024-07-18-Day38
  - 2024-07-19-Day39
tags:
  - java
  - 입출력
  - 메모리
---

# 바이트 배열 스트림 (ByteArrayStream)

**통로 끝이 파일이나 네트워크가 아니라 메모리의 `byte[]` 인 스트림.** 나가는 바이트를 밖으로 보내지 않고 배열에 모으거나(`ByteArrayOutputStream`), 이미 손에 든 배열을 스트림처럼 읽는다(`ByteArrayInputStream`).

## 정의

Day38 은 「ByteArrayOutputStream 클래스를 이용하여 바이트배열 담을 저장소를 만든다」·「이후 toByteArray()메서드로 통해 바이트 배열을 리턴 할 수 있다」로 두 줄에 정리했다.

| 클래스 | 통로의 끝 | 결과를 꺼내는 법 |
|---|---|---|
| `ByteArrayOutputStream` | 안에서 자라는 `byte[]` | `toByteArray()` |
| `ByteArrayInputStream` | 생성자로 받은 `byte[]` | `read()` · `read(byte[], off, len)` |

**둘 다 같은 `OutputStream`·`InputStream` 을 상속한다.** 그래서 쓰는 코드는 대상이 메모리인지 파일인지 모른다 → [[io-stream]]

```java
  public byte[] getBytes() throws IOException {
    try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
      //객체의 정보들을 byte로 담는다.
      return out.toByteArray();
    }
  }
```

## 사용 예시

Day38 이 이것을 쓰는 자리가 정확히 **「크기를 미리 모르는 바이트 뭉치를 만들어야 하는」** 곳이다.

```java
public byte[] getBytes() throws IOException {
    try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
      out.write(no >> 24);
      /* ... */
      byte[] bytes = name.getBytes(StandardCharsets.UTF_8);
      out.write(bytes.length >> 8);
      out.write(bytes.length);
      out.write(bytes);
      /* email · password · tel */
      return out.toByteArray();
    }
  }
```

**이름이 몇 바이트인지 미리 알 수 없다.** 한글이면 글자당 3바이트, 알파벳이면 1바이트이므로 `new byte[?]` 로 시작할 수 없고, 네 필드가 다 그렇다. `ByteArrayOutputStream` 은 안에서 배열을 늘려 주므로 그냥 쓰기만 하면 된다 → [[dynamic-array]] · [[character-encoding]]

읽는 쪽은 반대로 **이미 완성된 배열**을 스트림으로 감싼다.

```java
public static User valueOf(byte[] bytes) throws IOException {
    try (ByteArrayInputStream in = new ByteArrayInputStream(bytes)) {
      User user = new User();
      user.setNo(in.read() << 24 | in.read() << 16 | in.read() << 8 | in.read());

      byte[] buffer = new byte[10000];
      int len = in.read() << 8 | in.read();
      in.read(buffer, 0, len);
      user.setName(new String(buffer, 0, len, StandardCharsets.UTF_8));
      /* ... */
      return user;
    }
  }
```

**`bytes` 를 인덱스로 직접 훑을 수도 있었다** — `bytes[0] << 24 | bytes[1] << 16 | ...` 로. 그렇게 하지 않은 값은 **「지금 어디까지 읽었나」를 스트림이 대신 세어 주는 것**이다. 필드가 넷이고 각각 길이가 다르므로 손으로 세면 오프셋 변수를 계속 더해야 하고, 그 계산이 곧 형식이 어긋나는 자리가 된다 → [[serialization]]

## 왜 중요한가

**길이를 먼저 적어야 하는 형식의 모순을 이것이 푼다.** 「길이 + 내용」으로 저장하려면 길이를 먼저 써야 하는데, 길이는 내용을 다 만든 뒤에야 안다. 파일 스트림에 바로 쓰면 되돌아가 앞을 고칠 수 없다. **메모리 버퍼로 한 번 받아 두면 `bytes.length` 가 나오고, 그 다음에 파일에 「길이 → 내용」 순서로 쓸 수 있다.** Day38 이 `getBytes()` 를 따로 둔 진짜 이유가 이것이고, `saveUser` 의 세 줄이 그 결과다 → [[length-prefix-framing]]

```java
        byte[] bytes = user.getBytes();     // 다 만들어 두고
        out.write(bytes.length >> 8);       // 길이를 먼저 쓰고
        out.write(bytes.length);
        out.write(bytes);                   // 내용을 쓴다
```

**크기를 계산하는 코드가 사라진다.** 손으로 `byte[]` 를 쓰려면 「4 + 2 + name바이트 + 2 + email바이트 + …」를 미리 합산해야 하고, 그 식은 필드를 하나 더할 때마다 두 곳(계산식과 쓰는 코드)을 같이 고쳐야 한다. 버퍼를 쓰면 고칠 곳이 한 곳이다 → [[dynamic-array]]

### 하루 뒤, 이 버퍼가 사라진다 — 그리고 그 이유가 이 노트의 논거를 확인한다

Day39 는 `User.getBytes()`·`User.valueOf(byte[])` 를 지우고(「user.java에 valueOf, getBytes는 삭제」) `writeUTF`/`readUTF` 로 바꾼다. 그러면서 `ByteArrayOutputStream` 도 함께 없어진다.

**없어진 이유가 위의 「왜 중요한가」 첫 항목 그대로다** — 이 버퍼가 필요했던 것은 「길이를 먼저 써야 하는데 길이는 다 만든 뒤에 안다」는 모순 때문이었다. `writeUTF` 는 문자열을 받아 **자기가 바이트로 바꾸므로 길이를 부르기 전에 이미 안다.** 모순이 생기지 않으니 버퍼가 필요 없다.

즉 **버퍼가 없어진 것은 도구가 좋아진 것이 아니라 「길이를 먼저 쓰는 일」을 표준 층이 안으로 감춘 것**이다. 같은 모순은 `writeUTF` 안에 여전히 있고, 그 안에서도 같은 방식으로 풀린다 → [[data-io-stream]] · [[length-prefix-framing]]

읽는 쪽에서는 `new byte[10000]` 고정 버퍼와 그것이 만든 「저장은 되고 읽지는 못하는 구간(10001~65535)」이 **함께 사라진다.** `readUTF` 는 길이를 읽고 그만큼의 그릇을 스스로 만들기 때문이다 — **손코드의 결함 하나가 코드를 지우는 것으로 없어진 자리**다.

**테스트와 조립이 쉬워진다.** 스트림을 받는 코드에 파일 대신 `ByteArrayInputStream` 을 넘기면 파일 없이 같은 코드를 돌릴 수 있다. 통로를 갈아 끼울 수 있다는 스트림의 성질이 **메모리까지 확장된 것**이고, 그것이 이 클래스가 존재하는 이유의 절반이다 → [[io-stream]]

## 경계와 오해

- **`close()` 가 하는 일이 없다 — 그래서 여기서의 `try (...)` 는 습관이다** — `ByteArrayOutputStream.close()` 는 반납할 OS 자원이 없어 사실상 아무 일도 하지 않는다. 그래서 `return out.toByteArray()` 를 `try` 블록 **안에서** 해도 되고, 닫힌 뒤에 불러도 값이 나온다. **`FileOutputStream` 에서는 둘 다 성립하지 않는다.** Day38 의 코드는 같은 문법을 두 종류에 똑같이 쓰고 있어서 **문법만 보면 어느 것이 진짜 반납인지 구별되지 않는다** → [[try-with-resources]]
- **`toByteArray()` 는 내부 배열이 아니라 복사본이다** — 그래서 받은 뒤 스트림에 더 써도 앞서 받은 배열은 변하지 않는다. 대가는 **그 순간 같은 데이터가 메모리에 두 벌 있다**는 것이고, 큰 데이터에서는 이것이 비용이 된다 → [[defensive-copy]] · [[array-copy]]
- **메모리 스트림 ≠ 파일 스트림의 축소판** — 파일 스트림은 바이트를 흘려보내므로 얼마를 쓰든 힙이 늘지 않는데, 이쪽은 **전부 모은다.** `User` 하나는 작아서 이 실습에서는 문제가 없지만, 같은 방식으로 파일 전체를 만들면 파일 크기만큼 힙을 쓴다. 「스트림이니 흘러간다」로 읽으면 이 차이가 안 보인다.
- **`read(byte[], off, len)` 이 요청한 만큼 읽어 주는 것은 이쪽만의 성질이다** — `valueOf` 는 `in.read(buffer, 0, len)` 의 반환값을 무시하는데, 배열이 이미 메모리에 다 있으므로 짧게 읽힐 수가 없어 맞는 코드다. **같은 모양이 `loadUser` 의 `in.read(bytes)`(`FileInputStream`)에서는 위험하다** — 파일 쪽은 요청보다 적게 읽고 돌아올 수 있다. **두 줄이 똑같이 생겼는데 하나는 안전하고 하나는 아니고, 그 이유가 코드에 없다** → [[io-stream]]
- **`buffer = new byte[10000]` 은 스트림의 성질과 무관한 한계다** — 읽는 쪽에는 가변 버퍼를 쓰지 않고 고정 배열을 하나 만들어 재사용한다. 이름·이메일이 각각 10000바이트를 넘으면 `in.read(buffer, 0, len)` 이 `IndexOutOfBoundsException` 을 던진다. 쓰는 쪽은 길이 접두사가 2바이트라 65535까지 허용하므로 **저장은 되고 읽지는 못하는 구간(10001 ~ 65535)이 형식 안에 있다** → [[length-prefix-framing]] · [[array]]
- **하나를 재사용하는 `buffer` 에는 앞 필드의 찌꺼기가 남는다** — 이름을 9바이트 읽은 뒤 이메일을 5바이트 읽으면 6~9번째 바이트는 이름의 것이다. 이 코드가 안전한 이유는 `new String(buffer, 0, len, …)` 이 **읽은 길이만큼만** 잘라 쓰기 때문이고, `new String(buffer, UTF_8)` 로 적었다면 앞 필드의 꼬리가 붙어 나왔다. **길이를 들고 다니는 것이 이 코드에서 세 번째로 하는 일**이다 → [[character-encoding]]

## 함께 보는 개념

- [[io-stream]] — 이 클래스들이 상속한 통로 개념
- [[length-prefix-framing]] — 이 버퍼가 있어야 성립하는 형식
- [[serialization]] — 이 버퍼를 쓰는 작업
- [[binary-io]] — 여기 담기는 것의 정체
- [[try-with-resources]] — 닫는 문법이 여기서는 no-op 인 자리
- [[dynamic-array]] — 안에서 배열이 자라는 원리
- [[defensive-copy]] — `toByteArray()` 가 복사본을 주는 이유
- [[array]] — 고정 버퍼의 한계가 드러나는 자리
- [[character-encoding]] — 길이를 들고 다녀야 하는 이유
- [[data-io-stream]] — 이 버퍼가 하던 일을 안으로 감춘 층

## 출처

- [[2024-07-18-Day38]] — 「byte[] 만들기」 절에서 `ByteArrayOutputStream` 으로 「바이트배열 담을 저장소」를 만들고 `toByteArray()` 로 꺼내는 것을 배웠다. 그것을 `User.getBytes()` 에 써서 길이를 미리 모르는 네 문자열 필드를 쌓고, 되읽는 쪽 `User.valueOf(byte[])` 는 `ByteArrayInputStream` 으로 배열을 감싸 오프셋을 스트림이 세게 한다. **`saveUser` 가 「길이 → 내용」 순서로 쓸 수 있는 것이 이 버퍼 덕분**이고, 같은 `try (...)` 문법이 반납할 것이 없는 메모리 스트림과 진짜 파일 스트림에 똑같이 붙어 있다. 읽는 쪽은 `new byte[10000]` 고정 버퍼를 재사용하며 `in.read(buffer, 0, len)` 의 반환값을 무시한다
- [[2024-07-19-Day39]] — `User.getBytes()`·`User.valueOf(byte[])` 를 삭제하면서 **이 버퍼가 코드에서 사라진다.** `writeUTF` 가 문자열을 받아 자기가 바이트로 바꾸므로 「길이를 먼저 써야 하는데 길이는 나중에 안다」는 모순이 부르는 쪽에 생기지 않고, 그래서 버퍼가 필요 없어진다 — **버퍼가 하던 일이 없어진 것이 아니라 표준 층 안으로 들어간 것**이다. 읽는 쪽의 `new byte[10000]` 고정 버퍼와 그것이 만들던 「저장은 되고 읽지는 못하는 구간」도 함께 없어진다. 필기는 삭제를 주석 한 줄(「user.java에 valueOf, getBytes는 삭제」)로만 적었다
