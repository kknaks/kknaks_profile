# 프로젝트 카드 양식

`products/{제품}/showcase.md` 의 형식을 정의한다. **이 파일이 showcase 형식의 SoT다.**

관리 화면의 제품 등록이 여기를 읽어 카드를 만든다. 형식을 고치려면 **이 파일만** 고친다 —
코드나 프롬프트에 규칙을 복사하지 않는다. 복사하는 순간 SoT 가 둘이 되고 한쪽만 고쳐지는
날 조용히 어긋난다.

> **이 파일은 복사 대상이 아니다.** 같은 디렉토리의 `baseline.md`·`decision.md` 등은 손으로
> 복사해 쓰는 골격이지만, showcase 는 등록 화면이 입력값으로 **렌더**한다. 제품 스캐폴딩의
> 복사 목록에도 들어가지 않는다.

## 목표

**공개 사이트의 프로젝트 카드**다. `/projects` 목록과 상세, 그리고 포트폴리오 PDF 가 이
파일 하나를 읽는다.

제품 문서(`00-baseline` ~ `40-architecture`)와 성격이 반대다 — 그쪽은 **내부에서 결정을
쌓는 곳**이고 이 파일은 **밖에 보여주는 한 장**이다. 그래서 여기에 진행 과정을 적지 않고,
결과와 그 결과가 왜 의미 있는지를 적는다.

## 시스템이 매기는 값 — 사람이 정하지 않는다

| 필드 | 소유 | 규칙 |
|---|---|---|
| `type` | 시스템 | `project` 고정 |
| `id` | **코드** | `P-NN`. 기존 최대값 + 1. **결번을 재사용하지 않는다** |
| `org` | 시스템 | `studio` \| `company`. 레지스트리의 구분에서 온다 |

`id` 는 자산 경로(`/assets/projects/P-NN/`)에 쓰이므로, 지워진 카드의 번호를 다시 쓰면
과거 이미지가 새 프로젝트에 붙는다.

## 사람이 정하는 값

| 필드 | 필수 | 규칙 |
|---|:-:|---|
| `title` | ✓ | `{ko, en}` |
| `summary` | ✓ | `{ko, en}`. 목록 카드에 그대로 실린다 — **한 줄**로 끝낸다 |
| `category` | ✓ | **아래 enum 에서만 고른다** |
| `status` | ✓ | `wip` \| `live` |
| `stack` | ✓ | 문자열 배열. 카드에 뱃지로 실린다 |
| `date` | | `"YYYY.MM"` 착수 시점 |
| `visible` | | `false` 면 사이트·PDF 양쪽에서 빠진다. **기본은 `false`** — 채운 뒤 켠다 |
| `thumbnail` | | `/assets/projects/P-NN/cover.png`. 없으면 카드에 이미지가 없다 |
| `links.repo` | | 카드에 GitHub 링크로 렌더된다 |
| `links.live` | | 배포 주소 |

## `category` 는 이 파일이 아니라 `persona/_meta.yaml` 이 소유한다

```text
web · frontend · backend · mobile · ai · cli · bot
```

**목록 밖의 값을 넣으면 파일 하나가 거부되는 데서 끝나지 않는다.** `validate_persona` 가
`PersonaError` 를 던져 **persona 로드 전체가 실패**하고, `reload_data` 가 기존 데이터를
그대로 두므로 사이트는 **옛 데이터를 계속 서빙한다.** 발행 뒤에야 알게 되는 실패다.

분류를 늘리려면 `persona/_meta.yaml` 의 `projects.categories` 를 먼저 고친다.

## 로더가 강제하는 것 — 어기면 persona 로드 전체가 실패한다

- 필수 필드 7종: `type` · `id` · `title` · `summary` · `category` · `status` · `stack`
- `category` 가 `_meta.yaml` 목록 안에 있을 것
- 파일명은 반드시 `showcase.md` — 제품 디렉토리 깊이 1 (`products/*/showcase.md`)

## `links.repo` 는 표시 전용이다 — 추적 대상이 아니다

카드에 GitHub 링크를 그리는 값일 뿐이고, **잔디가 커밋을 긁을 레포는 DB 레지스트리가
소유한다.** 둘이 갈라져 있는 것이 정상이다 — 보여주지만 안 긁는 레포, 안 보여주지만 긁는
레포가 모두 정당하다.

여기를 고쳐도 추적은 바뀌지 않는다. 추적은 관리 화면에서 바꾼다.

## 포트폴리오 PDF 블록 — 필요할 때 추가한다

아래 다섯은 **이력서 PDF 전용**이고 사이트에는 안 나온다. **비어 있으면 PDF 에 그 항목이
표시되지 않는다.**

```yaml
problem:    { ko: "", en: "" }     # 무엇이 문제였나
approach:   { ko: [], en: [] }     # 어떻게 풀었나
impact:     { ko: [], en: [] }     # 무엇이 달라졌나
learnings:  { ko: [], en: [] }     # 무엇을 배웠나
troubles:   []                     # 마주친 문제
```

**새 카드에는 넣지 않는다.** 케이스 스터디는 제품이 어느 정도 진행된 뒤에 쓰는 것이고,
빈 필드를 미리 깔아 두면 "채워야 할 것" 과 "안 쓰기로 한 것" 이 구분되지 않는다.

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
| `/projects` 목록 | `title` · `summary` · `category` · `status` · `date` · `stack` · `thumbnail` |
| `/projects/{id}` 상세 | 위 + `body` + `links` |
| 포트폴리오 PDF | 위 + `problem` · `approach` · `impact` · `learnings` · `troubles` |

셋 다 **`visible: true` 인 카드만** 대상이다.

## 최소 예시

```yaml
---
type: project
id: P-15
org: studio
title:
  ko: "제품 이름"
  en: "Product Name"
summary:
  ko: "한 줄 설명"
  en: "One-line description"
category: backend
status: wip
date: "2026.08"
stack:
  - FastAPI
  - Postgres
visible: false
thumbnail: ""
links:
  repo: "github.com/kknaks/example"
---

# 개요

# 기술스택

# 주요기능
```
