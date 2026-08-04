---
type: concept
id: javadoc
title: Javadoc
aliases:
  - javadoc
  - 자바독
  - 문서화 주석
up:
  - 2024-05-31-Day06
tags:
  - java
  - 문서화
  - 개발도구
---

# Javadoc

`/** ~ */` 로 붙인 [[comment]] 에서 HTML API 문서를 뽑아내는 도구와 그 주석 문법. 설명을 코드 옆에 두고 문서는 거기서 생성한다.

## 정의

주석을 클래스·변수·메서드 **선언 앞**에 붙이면 그 대상의 설명으로 잡힌다. 태그로 항목을 구분한다.

- `@author` — 작성자
- `@param` — 매개변수 설명

문서를 만드는 명령은 인코딩과 경로를 받는다.

```plaintext
javadoc
  -encoding   [소스 파일의 문자집합]
  -charset    [생성될 HTML 파일의 문자집합]
  -d          [생성된 파일을 놓아둘 디렉토리]
  -sourcepath [자바 소스 경로] [자바 패키지]
```

`-encoding` 과 `-charset` 이 **따로 있다는 것이 핵심**이다. 읽는 쪽과 쓰는 쪽의 [[character-encoding]] 이 다를 수 있어서 각각 지정한다. 대상은 파일이 아니라 [[package]] 단위로 준다.

## 사용 예시

```java
/**
 * 클래스에 대한 설명
 * @author naknak
 *
 */
public class Exam0200 {
  /**
   * 변수에 대한 설명
   * 변수 선언 앞에 설명을 붙여 놓으면 나중에 HTML 문서를 만들 때 추출할 수 있다.
   */
  public static String message = "Hello, world!";

  /**
   * 메서드에 대한 설명
   * @param args 애플리케이션 아규먼트 값을 보관한 배열
   */
  public static void main(String[] args) {
    System.out.println(message);
  }
}
```

## 왜 중요한가

**문서가 코드와 같은 파일에 있으면 함께 고쳐질 확률이 올라간다.** 별도 문서로 두면 코드를 고칠 때 문서를 여는 일이 따로 필요한데, 선언 바로 위에 있으면 눈에 들어온다.

그리고 이것이 **소스 없이 라이브러리를 쓰는 방법**이 된다. 남의 `.jar` 을 쓸 때 우리가 보는 API 문서가 바로 이렇게 생성된 것이고, IDE 가 메서드 위에 띄워 주는 설명도 같은 주석에서 온다.

## 경계와 오해

- **Javadoc 주석도 컴파일에서는 무시된다** — 동작에 영향이 없다는 점은 일반 주석과 같다. 다른 것은 **`javadoc` 이라는 별도 도구가 읽는다**는 것뿐이다. [[annotation]] 처럼 컴파일러가 읽는 것과는 다르다.
- **`/**` 와 `/*` 는 다른 주석이다** — 별 하나 차이로 문서에 들어가는지가 갈린다.
- **선언 앞이 아니면 잡히지 않는다** — 메서드 안에 `/** */` 를 써도 문서에 나오지 않는다. 위치가 대상을 정한다.

## 함께 보는 개념

- [[comment]] — Javadoc 주석이 속한 갈래
- [[character-encoding]] — `-encoding`·`-charset` 을 따로 받는 이유
- [[package]] — 문서 생성의 지정 단위

## 출처

- [[2024-05-31-Day06]] — `/** */` 문법과 `@author`·`@param` 태그, 그리고 `javadoc` 명령의 `-encoding`/`-charset`/`-d`/`-sourcepath` 옵션을 배웠다
