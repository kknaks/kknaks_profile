# 프로젝트 카드 양식

`para/projects/**/<제품>/showcase.md` 의 형식을 정의한다. **이 파일이 showcase 의 양식 원천이다.**

## 목표

**공개 사이트의 프로젝트 상세 본문**이다. `/projects/{slug}` 상세 페이지가 이 파일을 읽는다.

제품 문서(`00-baseline` ~ `40-architecture`)와 성격이 반대다 — 그쪽은 **내부에서 결정을
쌓는 곳**이고 이 파일은 **밖에 보여주는 한 장**이다. 그래서 여기에 진행 과정을 적지 않고,
결과와 그 결과가 왜 의미 있는지를 적는다.

## frontmatter 를 두지 않는다 — 메타는 DB 가 SoT 다 (2026-08-25)

제목·한 줄 요약·카테고리·상태·스택·공개 여부·시작일·링크·썸네일은 전부 **`project` 표의
컬럼**이고 어드민(`/admin/projects`)에서 관리한다. md 에 같은 값을 두면 원천이 둘이 되어
한쪽만 고쳐지는 날 조용히 어긋난다 — 리뉴얼이 잡은 문제 2 그 자체다.

이 파일은 **`# 개요` 로 시작하는 본문만** 갖는다. 서빙(`read_detail`)은 frontmatter 가
있어도 떼고 내려주지만, 그건 note 처럼 frontmatter 를 쓰는 다른 원장을 위한 방어이지
showcase 에 얹어도 된다는 뜻이 아니다.

| 값 | 소유 |
|---|---|
| slug | **디렉토리명** — `para/projects/summer-star/<slug>/`. 등록 시 실존 검사(케이스 2) |
| title · summary · category · status · stack · started_on · visible · links | DB (`/admin/projects`) |
| thumbnail | DB — para 상대경로. 파일은 아래 `assets/` |
| 본문 | **이 파일** |

## 이미지 — 원장 옆 `assets/`

```text
para/projects/summer-star/<slug>/
├── showcase.md
└── assets/
    └── cover.png        ← DB thumbnail 이 가리키는 파일
```

- DB `thumbnail` 값: `para/projects/summer-star/<slug>/assets/cover.png`
- 본문 안에서는 **상대경로로 참조한다** — `![](assets/스크린샷.png)`. 옵시디언에서도
  사이트에서도 같은 참조가 통한다(사이트는 `GET /api/assets/{path}` 가 풀어 준다)
- 확장자는 이미지만 서빙된다: png · jpg · jpeg · webp · gif · svg

## `category` 의 값

지금 쓰는 값은 아래 일곱이다.

```text
web · frontend · backend · mobile · ai · cli · bot
```

**이 목록을 누가 소유하는지 아직 안 정했다.** `erd.md` 는 `category` 를 `varchar(32)` 로만
두고 있어 DB 가 값을 막지 않는다(_RESUME.md §4).

## `links.repo` 는 표시 전용이다 — 추적 대상이 아니다

카드에 GitHub 링크를 그리는 값일 뿐이고, **잔디가 커밋을 긁을 레포는 `repo` 표가
소유한다.** 둘이 갈라져 있는 것이 정상이다 — 보여주지만 안 긁는 레포, 안 보여주지만 긁는
레포가 모두 정당하다.

## 본문 섹션

필수 셋을 순서대로 둔다. 비어 있어도 헤딩은 남긴다 — 무엇이 빠졌는지 보이는 편이 낫다.

```text
# 개요        무엇을 만들었나. 2~3 문단
# 기술스택    왜 그 선택이었나. 나열이 아니라 근거
# 주요기능    사용자가 무엇을 할 수 있나
```

제품이 깊어지면 아래 넷을 덧붙인다. **필수가 아니다.**

```text
# 아키텍처 · # 핵심 구현 · # 마주친 문제 · # 회고
```

본문은 마크다운 그대로 상세 페이지에 렌더된다. **섹션 이름은 계약이 아니라 관례다** —
API 가 본문을 통째로 넘기므로 헤딩을 바꿔도 깨지지는 않는다. 다만 카드끼리 모양이 갈리면
읽는 사람이 비교를 못 한다.

## 어디에 노출되는가

| 경로 | 무엇이 쓰이나 |
|---|---|
| `/projects` 목록 | DB 메타(`title` · `summary` · `category` · `status` · `startedOn` · `stack` · `thumbnail`) |
| `/projects/{slug}` 상세 | 위 + **이 파일의 본문** + `links` |

둘 다 **`visible = true` 인 행만** 대상이다 — 공개 API 가 걸러서 내려준다(erd §미결 3).

## 최소 예시

```markdown
# 개요

무엇을 만들었나.

![](assets/cover.png)

# 기술스택

# 주요기능
```
