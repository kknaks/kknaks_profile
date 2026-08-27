---
type: concept
id: bean-post-processor
title: BeanPostProcessor
aliases:
  - BeanPostProcessor
  - 빈 후처리기
  - AutowiredAnnotationBeanPostProcessor
  - annotation-config
up:
  - 2024-10-04-Day88
tags:
  - spring
  - 프레임워크
  - 확장
---

# BeanPostProcessor

**컨테이너가 빈을 만든 직후에 끼어들어 그 객체에 무언가를 하는 장치.** 스프링의 애노테이션들이 실제로 동작하는 이유가 이것이다.

## 정의

메서드가 둘이고, **초기화 메서드를 기준으로 앞뒤**다.

```java
public class MyBeanPostProcessor implements BeanPostProcessor {

  @Override
  public Object postProcessBeforeInitialization(Object bean, String beanName) {
    // init-method 가 불리기 "전"
    return bean;
  }

  @Override
  public Object postProcessAfterInitialization(Object bean, String beanName) {
    // init-method 가 불린 "후"
    return bean;
  }
}
```

**받은 빈을 그대로 돌려주지 않아도 된다** — 다른 객체를 돌려주면 컨테이너에 그것이 담긴다. 프록시가 끼어드는 자리가 정확히 여기다 → [[dynamic-proxy]]

### 스프링 자신이 이것으로 만들어져 있다

| 후처리기 | 하는 일 |
|---|---|
| `AutowiredAnnotationBeanPostProcessor` | `@Autowired` 를 찾아 주입 → [[autowired]] |
| `ConfigurationClassPostProcessor` | `@Configuration`·`@Bean` 처리 → [[java-config]] |
| `EventListenerMethodProcessor` | 이벤트 리스너 메서드 등록 |
| `CustomEditorConfigurer` | 프로퍼티 변환기 등록 → [[property-editor]] |

XML 에서는 이것들을 하나씩 등록해야 했고, 한 줄로 줄이는 태그가 있다.

```xml
<context:annotation-config/>   <!-- 위 넷을 대신 등록해 준다 -->
```

`<context:component-scan>` 을 쓰면 **이것이 자동으로 포함된다.**

## 왜 중요한가

**애노테이션이 마법이 아니라는 것이 여기서 드러난다.** `@Autowired` 를 붙였는데 아무 일도 안 일어나는 이유는 「스프링이 이상해서」가 아니라 **그것을 읽을 후처리기가 등록되지 않아서**다. 표식과 그 표식을 읽는 자가 **따로 있다**는 구조를 알면 스프링의 대부분이 설명된다 → [[annotation]] · [[reflective-annotation-access]]

**그리고 확장점이 열려 있다.** 「컨테이너가 만든 모든 객체에 무언가 하고 싶다」가 가능해진다 — 로깅, 검증, 감싸기. 프레임워크가 자기 기능을 만든 방법을 사용자에게도 그대로 열어 둔 형태다 → [[open-closed-principle]]

## 경계와 오해

- **`BeanPostProcessor` 자신은 후처리 대상이 아니다** — 다른 빈보다 **먼저** 만들어져야 하므로 컨테이너가 특별 취급한다. 그래서 후처리기 안에 `@Autowired` 를 쓰면 동작하지 않을 수 있다
- **`postProcess...` 가 돌려준 것이 진짜 빈이다** — 원본을 그대로 돌려주는 것이 관례일 뿐, 프록시로 바꿔치기하는 것이 정상 동작이다. `@Transactional` 이 붙은 빈을 `getBean` 하면 **원래 클래스가 아닌 것**이 나오는 이유가 이것이다 → [[declarative-transaction]]
- **`before`/`after` 의 기준은 「초기화 메서드」다** — 생성자가 아니다. 순서는 **생성자 → before → `init-method`/`@PostConstruct` → after** 다
- **`<context:annotation-config/>` 와 `<context:component-scan/>` 은 겹친다** — 뒤엣것이 앞엣것을 포함하므로 둘 다 쓸 필요가 없다. 필기가 그 관계를 정확히 적었다
- **`@Bean` 으로 등록해도 후처리기가 된다** — 인터페이스를 구현하기만 하면 컨테이너가 알아본다. 별도의 등록 방식이 있는 것이 아니다

## 함께 보는 개념

- [[autowired]] — 이 장치가 처리하는 대표 표식
- [[ioc-container]] — 이 장치를 부르는 주체
- [[dynamic-proxy]] — 여기서 빈이 바꿔치기되는 방식
- [[declarative-transaction]] — 프록시가 실제로 끼어드는 자리
- [[property-editor]] — 같은 방식으로 등록되는 변환기
- [[java-config]] — `@Configuration` 을 처리하는 후처리기
- [[annotation]] — 표식과 처리자가 갈리는 구조

## 출처

- [[2024-10-04-Day88]] — 「BeanPostProcessor 구현체」 절이 인터페이스의 두 메서드를 구현한 예제를 싣고, 주석으로 **「XML 설정에서 `init-method` 속성에 지정된 메서드가 호출되기 전에 / 후에」**라고 호출 시점을 못 박았다. 그 앞의 「객체 자동 주입」 절에서 **`AutowiredAnnotationBeanPostProcessor` 를 XML 에 직접 등록하는 코드**가 나오는데, 이것이 이 개념의 값을 만든다 — `@Autowired` 가 동작하려면 그것을 읽는 빈이 먼저 있어야 한다는 것이 코드로 보인다. 「context:annotation-config」 절은 그 태그가 대신 등록해 주는 네 개의 후처리기를 이름까지 나열했다. 다만 후처리기가 **다른 객체를 돌려줄 수 있다**는 것 — 프록시가 끼어드는 원리 — 은 예제가 `return bean` 만 하고 있어 드러나지 않는다
