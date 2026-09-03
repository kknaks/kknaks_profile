---
type: concept
id: multipart-form-data
title: multipart/form-data (파일을 포함한 폼 본문)
aliases:
  - multipart/form-data
  - 멀티파트 폼 데이터
  - MultipartConfig
  - Servlet Part
up:
  - 2024-09-04-Day69
  - 2024-09-29-Day84
  - 2024-09-30-Day85
  - 2026-09-03-task-ref-multi-upload
tags:
  - web
  - servlet
  - 폼
  - 파일
---

# multipart/form-data (파일을 포함한 폼 본문)

폼의 각 입력을 경계 문자열로 나눈 HTTP 요청 본문 형식. 파일의 바이트와 일반 문자열을 같은 요청에 실을 때 `application/x-www-form-urlencoded` 대신 쓴다 → [[html-form]] · [[http-message]]

## 정의

일반 폼 인코딩은 `이름=값&이름=값`을 한 문자열로 만들기에 파일 바이트를 안전하게 구획하지 못한다. `multipart/form-data`는 각 입력을 **Part**로 나눠 그 파트마다 헤더와 본문을 둔다.

```http
Content-Type: multipart/form-data; boundary=----boundary

------boundary
Content-Disposition: form-data; name="age"

20
------boundary
Content-Disposition: form-data; name="photo"; filename="cat.png"
Content-Type: image/png

...파일 바이트...
------boundary--
```

서블릿 기본 API에서는 선언과 읽기가 짝이다.

```java
@MultipartConfig(maxFileSize = 1024 * 1024 * 10)
public class UploadServlet extends HttpServlet {
  protected void doPost(HttpServletRequest req, HttpServletResponse res)
      throws ServletException, IOException {
    req.setCharacterEncoding("UTF-8");
    String age = req.getParameter("age");
    Part photo = req.getPart("photo");
    // 검증한 저장 경로 아래에 photo.write(...) 한다.
  }
}
```

`web.xml`의 `<multipart-config>`와 `@MultipartConfig`는 같은 종류의 제한을 서블릿에 등록하는 두 방법이다 → [[web-xml]] · [[annotation]]

## 왜 중요한가

**업로드는 "파일명 하나를 파라미터로 받는 일"이 아니라 본문 스트림과 저장소를 다루는 일이다.** 기본 폼 형식으로 보내면 파일 입력의 이름 또는 문자열 값만 보이고, 바이트는 서버에 오지 않는다. `getPart()`가 필요한 이유가 여기 있다.

크기 제한을 선언해야 요청 하나가 메모리·임시 저장소를 끝없이 점유하는 일을 막는다. 다만 `maxFileSize`는 한 파일의 한도일 뿐이고, 전체 요청 한도·파일 개수·저장 공간·인증은 별도로 정해야 한다.

## 경계와 오해

- **`multipart/form-data` ≠ POST 자체** — 보통 POST와 함께 쓰지만, "POST면 파일이 자동으로 전송된다"는 뜻이 아니다. 브라우저 폼의 `enctype="multipart/form-data"`와 서버의 multipart 처리가 모두 맞아야 한다 → [[html-form]] · [[http-method]]
- **`getParameter()` ≠ 파일 바이트 읽기** — 일반 텍스트 파라미터는 그대로 꺼낼 수 있지만 파일은 `Part`로 받아야 한다. Day69의 "일반 POST면 파일 이름만 넘어온다"는 설명은 브라우저가 제공하는 파일 입력의 이름과 실제 파일 내용을 섞어 읽게 한다.
- **클라이언트 파일명 ≠ 안전한 저장 파일명** — `Part`가 보고한 이름은 경로 조각·중복·제어 문자를 포함할 수 있어 그대로 경로와 이어 붙이면 덮어쓰기나 경로 이탈이 된다. Day69의 Apache 예제처럼 서버가 UUID를 생성하는 방향은 맞지만, 허용 루트를 정규화해 그 아래인지 검사하고 확장자·MIME 타입도 서버에서 검증해야 한다 → [[filesystem-path]]
- **`Part.write("/uploadDir" + filename)` ≠ `/uploadDir` 안에 저장** — 구분자 없이 이어 붙이면 실제 경로는 `/uploadDir<filename>`가 된다. 게다가 Day69의 Servlet API 예시에는 `filename`을 만드는 코드가 없어 그대로는 컴파일되지 않는다. 둘 다 화면이 아니라 저장 시점에 드러나는 버그다.
- **Apache Commons FileUpload ≠ Servlet 기본 API의 단순 별칭** — 둘 다 multipart를 해석하지만 생성·제한·임시 파일·예외 처리 API가 다르다. 같은 요청에서 두 라이브러리가 본문을 각각 소비하도록 섞어 쓰면 안 된다.
- **「여러 파일」 ≠ 「한 요청에 여러 파트」** — 다중 업로드를 여는 방법이 둘이다: (a) 한 요청에 같은 이름의 파트 N개(`form.getlist`), (b) **요청당 파일 1개를 순차 N요청**. (a)는 요청이 한 번이지만 **부분 실패의 응답 형태를 새로 설계**해야 하고(3개 중 2개 성공을 어떻게 말할 것인가), 서버 파싱(`form.get` → `getlist`)까지 계약이 바뀐다. (b)는 요청이 N번이지만 건별 성공/실패가 HTTP 응답 그대로이고, 서버가 「개수 제한 없음」이면 계약 무변경이다 — UI 만 `multiple` 로 열고 클라이언트가 순차 루프를 돌면 백엔드는 그대로다. 프런트 폼의 `multiple` 과 서버의 수신 형태는 독립된 결정이라 짝을 확인해야 한다(Day85 의 `files` 복수 폼 ↔ 단수 `MultipartFile` 어긋남이 같은 자리다).

## 함께 보는 개념

- [[html-form]] — `enctype`으로 이 형식을 고르는 쪽
- [[http-message]] — Part들이 들어 있는 HTTP 본문 구조
- [[request-parameter]] — 문자열 Part를 읽는 통로와 인코딩
- [[character-encoding]] — 텍스트 Part를 해석할 문자셋
- [[filesystem-path]] — 서버 저장 경로를 검증하는 자리
- [[web-xml]] · [[annotation]] — multipart 설정의 두 등록 방식
- [[ioc-container]] — 프레임워크에서 이 처리를 빈으로 등록하는 자리
- [[object-storage]] — 받은 파일이 서버 디스크 대신 가는 곳
- [[jsp]] — 폼과 화면 양쪽이 이 형식에 맞춰 바뀌는 자리

## 출처

- [[2026-09-03-task-ref-multi-upload]] — mediness 태스크 산출물 첨부를 다중화할 때 (a) 한 요청 N파트(백엔드 `form.getlist` + 부분 실패 응답 신설) 대신 (b) **요청당 1파일 순차 N요청**을 골랐다 — 서버 계약이 「파일당 25MB·개수 제한 없음」이라 (b)는 프런트만 고치면 됐고, 순차 루프 + 건별 실패 수집 선례가 코드베이스에 이미 있었다. 요청 1회라는 (a)의 이득이 부분 실패 설계 비용을 못 넘었다
- [[2024-09-30-Day85]] — 하루 뒤. **폼에서 화면까지 한 벌이 이어진다.** `<form enctype="multipart/form-data">` 와 `<input name="files" type="file" multiple>` 로 시작해, 컨트롤러가 `MultipartFile` 로 받아 `getContentType()`·`getInputStream()` 을 꺼내고, `UUID.randomUUID()` 로 만든 이름을 DB 컬럼에 저장한 뒤, 화면이 그 이름으로 주소를 조립한다. 폼의 `name` 은 복수(`files`)인데 컨트롤러 매개변수는 단수(`MultipartFile file`)라 **이름과 개수가 어긋나 있는 자리**이기도 하다
- [[2024-09-29-Day84]] — 여덟 주 뒤. **받은 파일이 서버 디스크에 안 남는다.** 「클라이언트가 `Multipart/form-data` 형태로 Post요청을 보내면 서버측에서 `MultipartFile[]` 로 받는다」로 스프링 쪽 수신 타입이 나오고, 그 스트림을 그대로 오브젝트 스토리지에 흘려 보낸다 — Day69 의 `Part.write("/uploadDir" + filename)` 이 하던 로컬 저장이 사라지는 것이다. 파일명 충돌을 UUID 로 피하고 원래 이름을 `AttachFile` 에 따로 담는 처리도 이 회차에서 나온다 → [[object-storage]]
- [[2024-09-04-Day69]] — "파일 업로드" 절이 일반 GET·기본 POST는 파일 바이트를 보내지 못하고 `multipart/form-data`가 필요하다고 갈랐다. `<multipart-config>`·`@MultipartConfig`, `getPart()`·`Part.write()`와 Apache Commons FileUpload의 `FileItem` 순회까지 실제 코드로 적었다. 다만 Servlet API 예시의 `filename`은 선언되지 않았고 `"/uploadDir" + filename`에는 경로 구분자가 없으며, 클라이언트 파일명과 저장 경로 검증·크기 제한의 범위는 다루지 않았다.
