# enrich-note 예제

## 예제 1 — Spring Boot 노트 (links + stack 추론)

### Before

`persona/notes/SpringBoot/2025-01-03-chapter1.md`:

```yaml
---
title: "(점프 투 스프링부트) 1장 스프링부트 개발준비하기"
date: "2025.01.03"
tags: [스프링부트, 독학]
links: []
---

## 1.1 스프링부트란
- 스프링 부트(Spring Boot) 는 웹 프로그램(웹 애플리케이션)을 쉽고 빠르게 만들 수 있도록 도와주는 자바의 웹 프레임워크이다.
...
## 1.2 개발환경 준비하기(IntelliJ IDEA)
- IntelliJ IDEA에서 스프링 부트 프로젝트 만들기
...
```

같은 group (`SpringBoot/`) 안 다른 노트들:
- `2025-01-04-chapter2_1.md` — chapter 2 (앞)
- `2025-01-05-chapter2_2.md`
- `2025-01-05-chapter3.md`

### After (enrich-note 적용)

```yaml
---
title: "(점프 투 스프링부트) 1장 스프링부트 개발준비하기"
date: "2025.01.03"
tags: [스프링부트, 독학]
stack: [Java, Spring Boot, IntelliJ IDEA]
links: [2025-01-04-chapter2_1]
---

## 1.1 스프링부트란
... (body 그대로 보존)
```

추론 근거:
- `stack`: 본문에 `Spring Boot`, `자바` (Java), `IntelliJ IDEA` 등장 — 명시적 기술 스택만.
- `links`: chapter1 → chapter2 시리즈 패턴, 시간순 인접 (`2025-01-04`).

---

## 예제 2 — Polling/SSE 노트 (개념 위주, stack 빈 list, links 약간)

### Before

`persona/notes/BackendSchool/2024-12-31-Day02.md`:

```yaml
---
title:  Day02_Polling, SSE통신방식, webSocket
date: "2024.12.30"
tags: [멋쟁이사자처럼, 채팅]
links: []
---

## Polling, SSE 기반 통신
- HTTP 통신 기반 : 무상태, 요청/응답 방식

### Polling 방식으로 채팅 구성하기
1. controller 구현
```java
...
```
```

같은 group 다른 노트:
- `2025-01-02-Day03.md`, `2025-01-03-Day04.md` (시리즈)

### After

```yaml
---
title:  Day02_Polling, SSE통신방식, webSocket
date: "2024.12.30"
tags: [멋쟁이사자처럼, 채팅]
stack: [Java]
links: [2025-01-02-Day03]
---
```

추론 근거:
- `stack`: 본문 코드블록에 `java`. `Polling` / `SSE` / `WebSocket` 은 통신 패턴 (개념) 이라 stack 아님 → tags 영역.
- `links`: Day02 → Day03 시리즈 인접.

---

## 예제 3 — 빈약 본문 (skip)

### Before

`persona/notes/ai_skills/2026-03-11-LangGraph.md`:

```yaml
---
title:  LangGraph의 이해
date: "2026.03.11"
tags: [랭그래프]
links: []
---

#



```

### After

```
○ persona/notes/ai_skills/2026-03-11-LangGraph.md — body 빈약, skip
```

frontmatter 안 건드림. 사용자가 본문 채우면 다시 trigger.

---

## 예제 4 — 자기 link 방지

### Before

`persona/notes/bitcamp/jpa-basics.md` 본문에 "JPA 기본기 정리"가 등장.

### 잘못된 추론 (피해야 함)
```yaml
links: [jpa-basics]   # 자기 자신 — 박지 말 것
```

### 올바른 추론
- 같은 폴더 다른 JPA 관련 노트 (`jpa-relationships.md`, `jpa-query.md`) 찾아서 박음
- 자기 자신은 제외
