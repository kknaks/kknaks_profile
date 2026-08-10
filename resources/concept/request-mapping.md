---
type: concept
id: request-mapping
title: 요청 매핑 (@RequestMapping)
aliases:
  - "@RequestMapping"
  - "@GetMapping"
  - "@PostMapping"
  - 요청 매핑
  - 핸들러 매핑
up:
  - 2024-09-25-Day82
tags:
  - spring
  - web
  - 애노테이션
---

# 요청 매핑 (@RequestMapping)

**URL 과 메서드를 잇는 표식.** 어떤 요청이 왔을 때 어느 메서드를 부를지를 클래스 안에 적어 둔다.

## 정의

| 표식 | 걸리는 요청 |
|---|---|
| `@RequestMapping("/project/view")` | 그 URL 의 **모든 방식** |
| `@GetMapping("/project/list")` | 그 URL 의 GET → [[http-method]] |
| `@PostMapping("/project/add")` | 그 URL 의 POST |

`@GetMapping`·`@PostMapping` 은 `@RequestMapping` 에 방식을 고정해 둔 축약이다.

메서드의 **매개변수**도 함께 선언한다 — 요청 파라미터가 그 자리로 들어온다.

```java
@RequestMapping("/project/view")
public String view(@RequestParam("no") int projectNo, Model model) { ... }
```

`@RequestParam` 은 요청 파라미터 이름과 매개변수를 잇고, 이름이 같으면 생략할 수 있다 → [[request-parameter]]

## 사용 예시

```java
@Controller
public class ProjectController {

  @GetMapping("/project/list")
  public String list(Model model) {
    model.addAttribute("list", projectService.list());
    return "project/list";
  }

  @PostMapping("/project/add")
  public String add(Project project) {
    projectService.add(project);
    return "redirect:list";
  }
}
```

돌려주는 문자열이 **뷰 이름**이고, `redirect:` 접두어를 붙이면 화면을 그리는 대신 [[redirect]] 응답을 보낸다 → [[view-resolver]]

## 왜 중요한가

**URL 과 클래스의 1:1 결합이 끊어진다.** `@WebServlet("/board/list")` 시절에는 URL 하나에 클래스 하나였다. 매핑이 **메서드 단위**가 되면서 관련된 요청들이 한 클래스에 모이고, 그 클래스가 필드로 서비스를 하나 들고 공유한다 → [[cohesion]]

그리고 **분배 코드가 사라진다.** 손으로 만든 프론트 컨트롤러는 경로를 읽어 if-else 나 맵으로 나눠야 했는데, 그 표를 애노테이션이 대신 만든다 → [[dispatch-table]] · [[front-controller]]

## 경계와 오해

- **`@RequestMapping` 만 쓰면 GET 과 POST 가 구별되지 않는다** — 폼을 보여 주는 요청과 제출하는 요청이 같은 메서드로 들어온다. 이 회차의 코드가 `@RequestMapping` 에서 `@PostMapping` 으로 옮겨 가는 것이 그 정리다 → [[http-method]]
- **매핑이 겹치면 시작할 때 터진다** — 같은 URL·같은 방식을 두 메서드가 맡으면 애매해서 컨테이너가 뜨지 않는다. 런타임이 아니라 **기동 시점**에 드러나는 것이 다행인 자리다
- **애노테이션은 문자열이라 컴파일러가 검사하지 않는다** — URL 오타는 404 로만 나타난다. JSP 의 `getAttribute("list")` 와 같은 종류의 계약이다 → [[annotation]]
- **매개변수 이름에 의존하는 자동 매핑은 컴파일 옵션을 탄다** — `@RequestParam` 을 생략하면 스프링이 매개변수 이름을 읽어야 하는데, 그 이름은 `.class` 에 항상 남지 않는다. 필기가 `@RequestParam("no")` 을 쓰다가 생략형(`int no`)으로 넘어가는 자리가 그 위에 서 있다 → [[bytecode]] · [[class-file-format]]
- **반환값 `"project/form3"` 과 `"redirect:list"` 는 성격이 다르다** — 앞은 **뷰 이름**이고 뒤는 **브라우저를 다시 보내라는 지시**다. 접두어 하나로 갈리므로 눈에 잘 안 띈다 → [[redirect]]

## 함께 보는 개념

- [[dispatcher-servlet]] — 이 표식을 읽어 메서드를 고르는 것
- [[stereotype-annotation]] — `@Controller` 와 짝이 되는 표식
- [[request-parameter]] — 매개변수로 들어오는 것
- [[spring-model]] — 결과를 담아 뷰로 넘기는 방법
- [[view-resolver]] — 반환한 이름이 화면이 되는 과정
- [[http-method]] — GET·POST 를 가르는 축
- [[front-controller]] — 이 표식이 대신하는 분배 코드

## 출처

- [[2024-09-25-Day82]] — 「annotation 교체」 절이 `@RequestMapping("URL")` 과 `@GetMapping`·`@PostMapping` 을 한 줄씩 설명하고 **「요청 파라미터와 요청 파라미터 핸들러와 동일하게 사용」**이라 적어, 앞 회차에서 직접 만든 매핑 처리와 같은 것임을 짚었다. 「PageController 클래스 변경」 절의 코드들이 이 표식의 실제 쓰임을 보인다 — `@RequestParam("no") int projectNo` 로 시작해 `int no` 로 생략형이 되고, `@RequestMapping` 이 `@PostMapping` 으로 좁혀지며, 반환값으로 `"/project/view.jsp"` 와 `"redirect:list"` 두 종류가 나온다. 다만 매핑 충돌, 애노테이션 문자열이 검사되지 않는다는 것은 다루지 않았다
