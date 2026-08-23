# persona/posts

**공개 글** — 자료를 읽고 핵심만 가독성 있게 정리한 것. 타입은 둘이다.

| 타입 | 무엇 | 양식 |
|---|---|---|
| `post_article` | **스크랩** — 자료가 말한 요지를 압축 | `templates/persona/post-article.md` |
| `post_note` | **공부** — 내가 이해한 것을 내 언어로 | `templates/persona/post-note.md` |

갈리는 기준은 **누가 말한 것인가**다.

규칙: `rules/persona-artifacts.md`

## source 와의 관계 — 1:1

```
resources/source/{날짜}-{slug}.md   원본 정리 전문   비공개
        ▲ up:
persona/posts/{slug}.md             핵심만 가독성 있게   공개
```

**한 글이 한 자료를 받는다.** `up:` 이 하나라는 것이 그 제약이다. 여러 자료를 묶는 글은 이 계열이 아니다.

겹치는 것을 두려워하지 않는다 — 그쪽은 **전문 기록**이고 여기는 **읽히는 글**이라 목적이 다르다.

## 본문 다섯 절

`주제 · 개념(mermaid) · 사용 예시 · 리스크 · 비슷한 개념`

두 타입이 같은 뼈대를 쓰고 **채우는 결이 다르다.** 상세는 각 템플릿이 갖는다.

## 여기 두지 않는 것

- 자료 원본 정리 → `resources/source/`
- 재사용 가능한 개념 → `resources/concept/` (**개념 상세의 SoT 는 거기 한 곳**이다. 여기서는 요지만 쓰고 `[[]]` 로 위임한다)
- 미정제 생각 → `inbox/`
- 교안 → `persona/contents/`
