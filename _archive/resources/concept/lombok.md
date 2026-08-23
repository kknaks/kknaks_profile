---
type: concept
id: lombok
title: Lombok (애노테이션으로 코드 생성하기)
aliases:
  - Lombok
  - 롬복
  - "@Data"
  - "@Builder"
  - "@Slf4j"
  - annotationProcessor
up:
  - 2024-10-21-Day98
tags:
  - java
  - 빌드
  - 애노테이션
---

# Lombok (애노테이션으로 코드 생성하기)

**getter·setter·`toString()` 같은 반복 코드를 컴파일 시점에 만들어 넣어 주는 도구.** 소스에는 애노테이션만 남고 `.class` 에는 메서드가 들어 있다.

## 정의

동작하는 자리가 **컴파일 중간**이다.

```groovy
configurations {
    compileOnly { extendsFrom annotationProcessor }
}

annotationProcessor 'org.projectlombok:lombok'
```

**애노테이션 프로세서**는 컴파일러가 소스를 읽은 뒤 `.class` 를 만들기 전에 끼어드는 규약이고, Lombok 은 그 자리에서 메서드를 붙인다 → [[annotation]] · [[compilation]] · [[bytecode]]

`compileOnly` 인 이유는 **실행할 때는 필요 없기 때문**이다 — 이미 만들어진 클래스 안에 메서드가 들어 있다 → [[gradle]]

### 주요 애노테이션

| 애노테이션 | 만들어 주는 것 |
|---|---|
| `@Getter` · `@Setter` | 필드별 접근자. 클래스·필드 단위로 붙이고 접근 수준도 정한다 |
| `@ToString` | `toString()`. 포함·제외 필드를 고를 수 있다 |
| `@EqualsAndHashCode` | `equals()`·`hashCode()`. `of={...}` 로 **비교에 쓸 필드를 고른다** → [[object-equality]] · [[hash-code]] |
| `@NoArgsConstructor` | 기본 생성자 |
| `@AllArgsConstructor` | 모든 필드를 받는 생성자 |
| `@RequiredArgsConstructor` | `final`·`@NonNull` 필드만 받는 생성자 → [[dependency-injection]] |
| `@Data` | 위의 여럿을 한 번에 (`@Getter`+`@Setter`+`@ToString`+`@EqualsAndHashCode`+`@RequiredArgsConstructor`) |
| `@Value` | `@Data` 와 비슷하되 **모든 필드를 `final`** 로 — 불변 객체 → [[immutability]] |
| `@Builder` | 빌더 패턴 |
| `@SneakyThrows` | 검사 예외를 선언 없이 던지게 한다 → [[exception-handling]] |
| `@NonNull` | `null` 이면 `NullPointerException` 을 던지는 검사를 넣는다 |
| `@Slf4j` | 로깅 객체(`log`) 필드를 만들어 준다 |

## 왜 중요한가

**값 객체(VO·DTO)의 코드가 필드 목록만 남는다.** `User` 에 필드 여섯이면 getter·setter 열둘에 `toString`·`equals`·`hashCode` 까지 스물이 넘는 메서드가 붙는데, 그 전부가 **필드에서 기계적으로 나오는 것**이라 사람이 쓸 이유가 없다 → [[encapsulation]]

**그리고 필드를 고칠 때 따라 고칠 것이 없어진다.** 손으로 쓴 `equals()` 는 필드를 추가해도 조용히 옛날 기준으로 남는다 — **잊혀서 틀리는 종류의 버그**가 사라진다 → [[object-equality]]

## 경계와 오해

- **`@Data` 를 아무 데나 붙이면 안 된다** — `@Setter` 가 함께 붙어 **불변으로 두려던 객체가 열린다.** 값 객체에는 `@Value` 나 `@Getter` + `@Builder` 쪽이 맞다 → [[immutability]]
- **`@EqualsAndHashCode` 의 기본은 모든 필드다** — JPA 엔티티나 컬렉션에 담는 객체에서 이것이 문제가 된다. `of={...}` 로 **식별자만** 고르는 이유가 그것이다 → [[hash-based-collection]]
- **`@SneakyThrows` 는 예외를 없애지 않는다** — 선언만 건너뛰게 할 뿐, 그 예외는 여전히 던져진다. **부르는 쪽이 예상하지 못한 검사 예외를 받게 되므로** 편의로 쓰면 위험하다 → [[exception-handling]]
- **IDE 가 알아야 보인다** — 소스에 없는 메서드를 쓰는 것이라 플러그인이 없으면 편집기가 오류로 표시한다. **빌드는 되는데 편집기만 빨간** 상태가 흔하다
- **생성된 코드는 소스에 안 남는다** — 리뷰에서 `equals` 의 기준을 보려면 애노테이션 옵션을 읽어야 한다. **읽는 사람이 규칙을 알아야 하는 도구**다
- **`@Builder` 와 `@NoArgsConstructor` 를 같이 쓸 때 주의가 필요하다** — 빌더가 전 인자 생성자를 요구하므로 조합에 따라 생성자가 사라져 프레임워크(예: MyBatis 의 객체 생성)가 실패할 수 있다 → [[constructor]] · [[reflective-instantiation]]

## 함께 보는 개념

- [[annotation]] — 이 도구가 얹혀 있는 장치
- [[compilation]] · [[bytecode]] — 코드가 생성되는 시점
- [[gradle]] — 애노테이션 프로세서를 등록하는 자리
- [[object-equality]] · [[hash-code]] — `@EqualsAndHashCode` 가 만드는 것
- [[immutability]] — `@Value` 가 겨냥하는 성질
- [[dependency-injection]] — `@RequiredArgsConstructor` 가 쓰이는 자리
- [[spring-boot]] — 이 의존성이 기본으로 딸려 오는 환경

## 출처

- [[2024-10-21-Day98]] — 「Lombok 적용하기」 절이 **왜 동작하는지를 먼저 적은 것**이 특징이다: 「gradle 의 설정 시 `compileOnly` 에서 `annotationProcessor` 를 추가하여 작업하는 **중간 컴파일 과정**이 있고, 그 과정에서 Lombok 이 메서드들을 추가해 준다」 — 애노테이션이 실행 중에 마법을 부리는 것이 아니라 **컴파일 시점에 코드가 생긴다**는 것을 짚었다. 이어서 주요 애노테이션 열 가지를 각각 두세 줄로 정리했고, `@Data` 가 무엇들의 조합인지, `@Value` 가 `@Data` 와 달리 **모든 필드를 `final`** 로 만든다는 것, `@RequiredArgsConstructor` 가 `final`·`@NonNull` 필드만 받는다는 것까지 구별해 적었다. `@EqualsAndHashCode(of={...})` 로 비교 대상 필드를 고를 수 있다는 것도 나온다. 다만 각 애노테이션을 언제 쓰면 안 되는지는 다루지 않았다
