---
type: concept
id: view-resolver
title: ViewResolver
aliases:
  - ViewResolver
  - InternalResourceViewResolver
  - 뷰 리졸버
  - 뷰 이름
up:
  - 2024-09-25-Day82
  - 2024-10-17-Day95
  - 2024-10-18-Day96
  - 2024-10-23-Day100
tags:
  - spring
  - web
  - mvc
---

# ViewResolver

**컨트롤러가 돌려준 「뷰 이름」을 실제 화면 파일로 바꾸는 것.** 이름 앞뒤에 접두사·접미사를 붙여 경로를 만든다.

## 정의

```java
@Bean
public ViewResolver viewResolver() {
  InternalResourceViewResolver vr = new InternalResourceViewResolver();
  vr.setPrefix("/WEB-INF/jsp/");   // 접두사
  vr.setSuffix(".jsp");            // 접미사
  return vr;
}
```

```
컨트롤러 반환값   "project/view"
                    ↓
접두사 + 이름 + 접미사   /WEB-INF/jsp/project/view.jsp
```

그래서 컨트롤러의 반환값이 `"/project/view.jsp"` 에서 `"project/view"` 로 짧아진다 — **경로와 확장자가 설정으로 빠진다.**

## 왜 중요한가

**JSP 를 외부 접근에서 막을 수 있다.** `/WEB-INF/` 아래는 서블릿 컨테이너가 **브라우저에게 직접 내주지 않는 자리**다. 화면 파일을 그리로 옮기면 사용자가 `/project/view.jsp` 를 주소창에 쳐도 못 연다 — **뷰는 반드시 컨트롤러를 거쳐야 한다** → [[front-controller]] · [[web-application-deployment]]

이것이 [[mvc-pattern]] 의 MVC2 를 **문법이 아니라 배치로** 강제하는 유일한 장치다. MVC2 의 정의가 「모든 요청이 컨트롤러를 통과한다」인데, JSP 가 공개 디렉토리에 있으면 그 문장은 규율일 뿐이고 `/WEB-INF/` 아래에 있으면 **구조가 지킨다.**

그리고 **화면 기술을 바꿀 자리가 한 곳이 된다.** 접미사를 `.jsp` 에서 다른 것으로 바꾸면 컨트롤러는 그대로 둔 채 뷰만 갈아 낄 수 있다 → [[template-engine]]

## 경계와 오해

- **접두사/접미사가 붙는 것을 잊으면 경로가 두 번 붙는다** — `"/project/view.jsp"` 를 그대로 돌려주면 `/WEB-INF/jsp//project/view.jsp.jsp` 를 찾는다. 필기의 코드가 `"/project/view.jsp"` 와 `"project/form2"` 를 섞어 쓰고 있어, **뷰 리졸버를 넣은 뒤에 앞쪽 반환값들이 전부 바뀌어야 한다**
- **`redirect:` 접두어는 뷰 리졸버를 타지 않는다** — `"redirect:list"` 는 화면 이름이 아니라 지시라서 접두사·접미사가 붙지 않는다 → [[redirect]]
- **`/WEB-INF/` 는 스프링이 아니라 서블릿 명세가 막는 것이다** — 뷰 리졸버가 보안을 제공하는 게 아니라, **그 디렉토리에 두는 선택**이 제공한다. 접두사를 공개 경로로 두면 그 보호는 없다 → [[servlet-container]]
- **뷰를 못 찾은 것과 매핑을 못 찾은 것은 다른 실패다** — 둘 다 404 로 보일 수 있지만, 앞은 컨트롤러가 이미 돈 뒤이고 뒤는 아예 안 불린 것이다 → [[dispatcher-servlet]]
- **뷰 리졸버는 여럿일 수 있다** — JSP 와 다른 템플릿을 함께 쓰면 순서대로 물어본다. 이 회차는 하나만 등록한다

## 함께 보는 개념

- [[dispatcher-servlet]] — 반환된 이름을 이쪽으로 넘기는 것
- [[spring-model]] — 뷰 이름을 정하는 자리
- [[request-mapping]] — 반환값이 뷰 이름이 되는 메서드
- [[jsp]] — 이 회차가 푸는 뷰
- [[mvc-pattern]] — `/WEB-INF/` 배치가 지키는 원칙
- [[web-application-deployment]] — `/WEB-INF/` 의 성격
- [[handler-interceptor]] — 뷰 실행 전후에 끼어드는 장치
- [[spring-boot]] — 이 설정이 속성 두 줄이 되는 자리
- [[thymeleaf]] — 접미사가 기본값으로 정해져 있는 뷰

## 출처

- [[2024-10-23-Day100]] — 닷새 뒤. **뷰 기술을 바꾸면 이 설정만 바뀐다**는 것이 실물로 확인된다 — `spring.mvc.view.*` 대신 `spring.thymeleaf.prefix=file:src/main/resources/templates/` 를 두고, **접미사는 `.html` 이 기본이라 적을 필요도 없다.** 컨트롤러가 돌려주는 뷰 이름은 그대로다 → [[thymeleaf]]
- [[2024-10-18-Day96]] — 하루 뒤. **빈 등록이 속성 두 줄이 된다** — `spring.mvc.view.prefix=/WEB-INF/jsp/` 와 `spring.mvc.view.suffix=.jsp`. `@Bean public ViewResolver viewResolver()` 메서드가 통째로 사라지지만 **결정한 내용은 똑같다** → [[spring-boot]]
- [[2024-10-17-Day95]] — 삼 주 뒤. **뷰 이름을 안 돌려줘도 된다는 것이 나온다** — 리턴이 `void` 거나 `Map`·`ModelAndView` 에 뷰 이름이 없으면 **요청 핸들러의 URL 자체가 뷰 이름이 된다.** `@GetMapping("h2")` 인 핸들러가 아무것도 안 돌려주면 `/WEB-INF/jsp2/c01_2/h2.jsp` 를 찾는 식이라, 「이름을 안 정하면 규칙이 정한다」는 관례가 성립한다. 실행 과정도 네 걸음으로 정리됐다: 핸들러가 이름을 리턴 → 프론트 컨트롤러가 뷰 리졸버에 전달 → 리졸버가 자기 정책으로 URL 을 만듦 → JSP 를 찾음. 접두사·접미사를 **생성자로 넘기는 표기**(`new InternalResourceViewResolver("/WEB-INF/jsp2/", ".jsp")`)도 이 회차의 것이다
- [[2024-09-25-Day82]] — 「AppConfig 클래스 변경」 절이 `InternalResourceViewResolver` 를 `@Bean` 으로 등록하는 코드와 `setPrefix("/WEB-INF/jsp/")`·`setSuffix(".jsp")` 를 보이고, 그 목적을 **「JSP 외부접근 차단」**이라고 한 줄로 적었다 — 뷰 리졸버를 「경로 짧게 쓰기」가 아니라 **접근 통제**의 관점에서 잡은 것이 정확하다. 같은 절이 `MultipartResolver` 등록도 함께 다룬다(설명 문장은 「`viewResolver` 메서드를 통해」로 적혀 있으나 코드는 `multipartResolver` 다) → [[multipart-form-data]]. 구동원리는 이미지로만 있고, 접두사·접미사가 붙은 뒤 앞선 코드들의 반환값(`"/project/view.jsp"`)이 어떻게 바뀌어야 하는지는 다루지 않았다
