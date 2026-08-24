---
type: concept
id: spring-model
title: Model · ModelAndView
aliases:
  - Model
  - ModelAndView
  - "@ModelAttribute"
  - SessionStatus
up:
  - 2024-09-25-Day82
  - 2024-10-16-Day94
tags:
  - spring
  - web
  - mvc
---

# Model · ModelAndView

**컨트롤러가 뷰에게 값을 넘기는 통로.** 서블릿 시절의 `request.setAttribute()` 자리를 대신하며, 담는 방식이 세 가지다.

## 정의

세 방식이 같은 일을 다르게 적는다.

| 방식 | 값을 담는 곳 | 뷰 이름을 정하는 곳 |
|---|---|---|
| `Map<String, Object>` | 매개변수로 받은 맵 | 반환값(`String`) |
| `Model` | 매개변수로 받은 모델 | 반환값(`String`) |
| `ModelAndView` | 직접 만든 객체 | **같은 객체**(`setViewName`) |

```java
// Map
public String view(@RequestParam("no") int no, Map<String, Object> map) {
  map.put("project", projectService.get(no));
  return "/project/view.jsp";
}

// Model
public String view(int no, Model model) {
  model.addAttribute("project", projectService.get(no));
  return "/project/view.jsp";
}

// ModelAndView
public ModelAndView view(int no) {
  ModelAndView mv = new ModelAndView();
  mv.addObject("project", projectService.get(no));
  mv.setViewName("/project/view.jsp");
  return mv;
}
```

**모델에 담은 것은 요청 보관소로 간다** — 뷰에서는 `${project}` 로 꺼낸다 → [[expression-language]] · [[attribute-scope]]

### 여러 요청에 걸쳐 값을 들고 가기

여러 화면을 거쳐 하나를 완성하는 흐름(form1 → form2 → form3 → add)에서는 요청 하나가 끝나면 값이 사라진다. 해결이 둘이다.

```java
// 세션에 직접 담기
session.setAttribute("project", project);
...
Project project = (Project) session.getAttribute("project");
...
session.removeAttribute("project");
```

```java
// 모델에 담고 @ModelAttribute 로 꺼내기
@PostMapping("/project/form3")
public String form3(int[] memberNos, @ModelAttribute Project project) { ... }

@PostMapping("/project/add")
public String add(@ModelAttribute Project project, SessionStatus sessionStatus) {
  projectService.add(project);
  sessionStatus.setComplete();   // 임시 보관을 끝낸다
  return "redirect:list";
}
```

뒤쪽은 **세션을 직접 만지지 않는다** — 담는 것도 꺼내는 것도 모델이고, 다 쓴 뒤 정리하는 것이 `SessionStatus.setComplete()` 다 → [[http-session]]

## 왜 중요한가

**컨트롤러에서 서블릿 API 가 사라진다.** `HttpServletRequest`·`HttpSession` 을 매개변수에서 걷어내면 그 메서드는 **웹을 모르는 자바 메서드**에 가까워지고, 그만큼 부르기 쉽고 시험하기 쉽다 → [[coupling]] · [[service-layer]]

그리고 **이름 계약이 좁아진다.** `setAttribute("project", ...)` 와 JSP 의 `${project}` 를 잇는 문자열은 여전히 남지만, 담는 코드가 한 줄로 줄어 어디서 담았는지 찾기 쉽다 → [[mvc-pattern]]

## 경계와 오해

- **셋 중 무엇을 써도 결과는 같다 — 고르는 기준은 「뷰 이름을 어디서 정하느냐」다** — 뷰 이름이 분기에 따라 갈리면 `ModelAndView` 가 한 객체에 모아 편하고, 뷰가 고정이면 `Model` + 반환 문자열이 짧다. **성능이나 기능 차이가 아니다**
- **`Map` 을 쓰는 것은 스프링 이전 코드와 이어 붙이기 위한 모양이다** — 필기가 `Map` → `Model` → `ModelAndView` 순으로 옮겨 가는 것이 그 흐름이다. 새로 쓸 때 `Map` 을 고를 이유는 거의 없다
- **`@ModelAttribute` 만으로는 요청을 넘어가지 않는다** — 클래스에 `@SessionAttributes("project")` 가 함께 있어야 그 이름이 세션에 임시 보관된다. 필기의 주석이 「`@SessionAttributes` 에 등록된 이름의 값」이라고 짚은 자리인데, **그 애노테이션 자체는 코드에 안 보인다**
- **`setComplete()` 를 빠뜨리면 값이 세션에 남는다** — 같은 사용자가 다음에 폼을 열면 옛 값이 채워져 있다. 직접 `removeAttribute` 를 부르던 것과 잊기 쉬운 정도가 같다
- **모델에 담는 것과 세션에 담는 것은 수명이 다르다** — 모델은 그 요청 하나, 세션은 사용자의 접속 내내다. 「화면에 넘기려고」 세션을 쓰면 다른 탭·다른 화면까지 그 값을 본다 → [[attribute-scope]]
- **[[redirect]] 하면 모델이 사라진다** — 리다이렉트는 새 요청이라 앞 요청의 모델이 남지 않는다. `"redirect:list"` 뒤에서 값을 보려면 다시 담아야 한다

## 함께 보는 개념

- [[request-mapping]] — 이 값들이 오가는 메서드
- [[view-resolver]] — 뷰 이름이 화면이 되는 과정
- [[attribute-scope]] — 모델이 실제로 담기는 곳
- [[expression-language]] — 뷰에서 꺼내는 표기법
- [[http-session]] — 요청을 넘어 값을 들고 갈 때
- [[mvc-pattern]] — 컨트롤러와 뷰를 잇는 자리
- [[handler-method-argument]] — 모델이 아규먼트로 들어오는 규칙
- [[response-body]] — 모델 대신 본문을 돌려주는 쪽

## 출처

- [[2024-10-16-Day94]] — 삼 주 뒤. 같은 값을 담는 방법이 **넷으로 늘어난다** — `ServletRequest.setAttribute()` · `Map` · `Model` · `ModelAndView`. 그중 `Map` 에 대해 「맵 객체에 값을 담아 놓으면 프론트 컨트롤러가 JSP 를 실행하기 전에 **`ServletRequest` 로 복사한다**」고 적어, **결국 전부 요청 보관소로 간다**는 것을 짚었다 — Day82 가 세 방법만 보이고 넘어간 자리를 채운다 → [[attribute-scope]]
- [[2024-09-25-Day82]] — 「PageController 클래스 변경」 절이 **같은 메서드를 `Map` · `Model` · `ModelAndView` 세 가지로 다시 쓴 코드**를 나란히 실었다 — 이 대비가 이 개념의 몸통이다. 이어서 「Session 대체」가 form2 → form3 → add 흐름을 **`HttpSession` 을 직접 쓰는 버전**과 **`ModelAndView` + `@ModelAttribute` + `SessionStatus.setComplete()` 버전**으로 두 번 보여, 컨트롤러에서 서블릿 API 를 걷어내는 과정을 코드로 남겼다. `setComplete()` 에 붙은 주석이 `@SessionAttributes` 를 언급하지만 **그 애노테이션이 붙은 클래스 선언은 노트에 없어**, 이 코드만 보면 값이 어디에 보관되는지가 설명되지 않는다. 코드에 `model.setAttribute`(실제로는 `addAttribute`)·`mb.setViewName` 오타가 있다
