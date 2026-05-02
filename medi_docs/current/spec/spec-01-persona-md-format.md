---
id: spec-01
type: spec
title: 페르소나 md 형식 명세 — 디렉토리·frontmatter·파일명
status: draft
created: 2026-05-01
updated: 2026-05-02
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[adr-05-content-pending-enrich]]"
tags: [spec, persona, md, schema]
---

# 페르소나 md 형식 명세

## Summary

페르소나 시스템(`persona/`)의 md 파일 형식을 정의. 디렉토리 구조, 카테고리별 frontmatter 스키마, 파일명 규칙, i18n 표현(`{ko, en}` 객체), 위키링크 컨벤션, 메타 정의(`_meta.yaml`), 잡 산출물(`activity.yaml`)을 다룸. 백엔드(`back/`)는 부팅 시 이 형식을 메모리 dict로 로드해서 API 응답 소스로 사용.

---

## 1. 디렉토리 구조

```
persona/
├─ profile.md                      ← 단일 (about 페이지 입력)
├─ career/
│  ├─ stealth-ai.md
│  ├─ ssafy.md
│  └─ ...                          ← 정렬은 frontmatter display_order
├─ projects/
│  ├─ homelab-console.md
│  ├─ vault-sync.md
│  └─ ...
├─ notes/
│  ├─ python-asyncio.md
│  ├─ postgres-index.md
│  └─ ...                          ← 옵시디언 스타일 위키링크 [[id]]
├─ contents/
│  ├─ C-001-fastapi-di.md
│  ├─ C-002-gunicorn-vs-uvicorn.md
│  └─ ...                          ← 매일 업로드 스터디 (영상 + 교안)
├─ daily/
│  ├─ 2026-04-30.md
│  ├─ 2026-04-29.md
│  └─ ...                          ← 일일 작업 로그 (잔디 잡 입력 소스)
├─ assets/                         ← 이미지 등 정적 자산 (§2.5)
│  ├─ profile/
│  │  └─ me.png
│  ├─ career/
│  ├─ projects/
│  └─ notes/
├─ activity.yaml                   ← 잡 자동 산출물 (사람 안 만짐)
├─ _meta.yaml                      ← 카테고리·클러스터 enum 정의
└─ _map.md                         ← 자동 생성 인덱스 (옵시디언 진입점, 사람 안 만짐 — spec-04)
```

**원칙**:
- 카테고리 디렉토리 이름은 영문 소문자 + kebab-case. 단/복수는 SLOTS.md mock 표기 따름 (`career`, `daily` 단수 / `projects`, `notes`, `contents` 복수)
- 파일은 카테고리당 N개 (profile만 단일)
- 자동 생성물(`activity.yaml`) + 메타(`_meta.yaml`)는 yaml 허용 (planning-01 §6 예외 조항)

---

## 2. 공통 컨벤션

### 2.1 i18n 표현

다국어 필드는 `{ko, en}` 객체로 표현. 단일 언어 필드(`period`, `email`, `stack[]` 등)는 객체 X.

```yaml
title:    { ko: "Backend Engineer", en: "Backend Engineer" }
summary:  { ko: "...요약 ko...",     en: "...summary en..." }
period:   "2025.06 — present"        # 언어 무관
stack:    ["Python", "FastAPI"]      # 태그는 다국어 X
```

백엔드는 `?lang=ko` 쿼리에 따라 한쪽만 추출해서 응답. 디테일은 ADR-02.

### 2.2 위키링크 (notes 한정)

`notes/*.md` 본문에서 다른 노트 참조 시 `[[id]]` 사용 (옵시디언 컨벤션).

```markdown
> ASGI 서버는 [[gunicorn-vs-uvicorn]] 비교에서...
```

`id`는 frontmatter `id` 필드 = 파일 slug. 백엔드가 본문 파싱 시 `[[…]]` 추출 → 그래프 edge 생성.

### 2.3 본문 컨벤션

- frontmatter 아래 본문은 **자유 서술**
- profile/career/projects의 본문은 사이트엔 안 표시될 수 있으나 **AI 컨텍스트로 가치** (페르소나 사상)
- notes/contents/daily의 본문은 사이트에도 직접 표시
- 마크다운 자유 사용. 코드 블록·인용·링크 OK

### 2.4 파일명 규칙

| 카테고리 | 규칙 | 예 |
|---|---|---|
| profile | 단일 | `profile.md` |
| career | `slug.md` (정렬은 frontmatter `display_order`) | `stealth-ai.md` |
| projects | `slug.md` | `homelab-console.md` |
| notes | `slug.md` (= 위키링크 id) | `python-asyncio.md` |
| contents | `C-NNN-slug.md` | `C-005-postgres-index.md` |
| daily | `YYYY-MM-DD.md` | `2026-04-30.md` |
| activity | 단일 yaml | `activity.yaml` |
| _meta | 단일 yaml | `_meta.yaml` |

slug는 kebab-case (영문 소문자 + 하이픈). 한글 X.

### 2.5 정적 자산 (`assets/`)

이미지 등 정적 파일은 `persona/assets/<category>/...` 에 둔다. md SoT 와 같은 트리 안에 박아 declarative 일관성을 유지 (frontend `public/` 분산 금지).

**디렉토리 컨벤션**:

| 위치 | 용도 | 예 |
|---|---|---|
| `assets/profile/` | profile.md 자산 | `assets/profile/me.png` |
| `assets/career/<slug>/` | 회사별 자산 (로고·스크린샷) | `assets/career/medisolve-ai/logo.png` |
| `assets/projects/<P-NN>/` | 프로젝트별 자산 | `assets/projects/P-01/screenshot.png` |
| `assets/notes/<cluster>/` | 노트 다이어그램·스크린샷 | `assets/notes/py/asyncio-flow.png` |

**참조 경로 (frontmatter URL 필드 / md 본문)**:

`persona/` 루트 기준 절대경로로 `/assets/<category>/<file>` 박는다. 예:

```yaml
avatarUrl: /assets/profile/me.png        # frontmatter URL 필드
```

```markdown
![asyncio flow](/assets/notes/py/asyncio-flow.png)   <!-- md 본문 -->
```

백엔드는 `persona/assets/` 를 `/assets/*` 라우트로 정적 서빙 (spec-02 §2). 프론트는 받은 URL 을 `<API_BASE>/assets/...` 또는 동일 origin 으로 그대로 박음.

> 옵시디언 호환은 본 spec 시점 비-목표. 옵시디언 vault 안에서는 `/assets/...` 절대경로가 못 풀리지만, 사이트 렌더링이 1차 SoT (옵시디언은 작성 도구).

---

## 3. 카테고리별 frontmatter 스키마

### 3.1 `profile.md`

About 페이지 + Hero + Footer 연락처 입력.

```yaml
---
type: profile
handle: kknaks
name: 이건학
role: Backend Engineer
years: "1년차"
location: "Seoul, KR"
focus: "AI · Python · Infra"
email: kknaks@gmail.com
github: github.com/kknaks
linkedin: linkedin/in/kknaks
avatarUrl: /assets/profile/me.png         # §2.5 컨벤션 (persona 루트 기준 절대경로)
tagline:    { ko: "호기심으로 시작해서, 도전으로 만들고, 개발로 풀어냅니다.", en: "..." }
intro:      { ko: "저는 새로운 것을 도전하고...", en: "..." }
intro2:     { ko: "지금은 AI 회사에서...", en: "..." }      # optional
hero:
  headline: { ko: "내 홈서버 위에서\n돌아가는\n제품을 만든다.", en: "..." }
  subline:  { ko: "풀스택 엔지니어. ...", en: "..." }
stack:      ["Python", "FastAPI", "Postgres", "Next.js", "Docker"]
stackShort: "Next.js · Python"
cards:
  - title: { ko: "지금 일하는 곳", en: "Where I work now" }
    body:  { ko: "AI 회사 · ...",  en: "..." }
  - title: { ko: "만들고 있는 것", en: "..." }
    body:  { ko: "...", en: "..." }
  # 카드 4개 권장
---

# (자기소개 자유 서술 — 사이트엔 안 표시되지만 AI 컨텍스트)
```

**필수**: `type`, `handle`, `name`, `role`, `email`, `tagline`, `intro`, `stack`
**선택**: `intro2`, `hero`, `cards`, `linkedin`, `avatarUrl`, `stackShort`

### 3.2 `career/slug.md`

> 정렬 SoT는 frontmatter `display_order` 단일. 파일명에 `NN-` prefix 박지 않음 (두 군데 ordering 소스가 drift할 위험 회피).

```yaml
---
type: career
period: "2025.06 — present"
display_order: 1
is_current: true
title:    { ko: "Backend Engineer", en: "Backend Engineer" }
org:      { ko: "Stealth AI Co.",   en: "Stealth AI Co." }
location: { ko: "서울 · 하이브리드", en: "Seoul · Hybrid" }
summary:  { ko: "LLM 기반 B2B 제품 백엔드. ...", en: "..." }
stack:    ["Python", "FastAPI", "Postgres", "Docker"]
links:    { repo: "...", site: "..." }    # optional
---

# 회사 회고 / 기여 / 배운 점 자유 서술 (AI 컨텍스트)
```

**필수**: `type`, `period`, `display_order`, `title`, `org`, `summary`, `stack`
**선택**: `is_current`, `location`, `links`

### 3.3 `projects/slug.md`

```yaml
---
type: project
id: P-01
title:    { ko: "Homelab Console", en: "Homelab Console" }
summary:  { ko: "홈서버 메트릭 대시보드. ...", en: "..." }
category: web                      # _meta.yaml/projects.categories[].id
status: wip                        # live | wip | archived
date: "2026.04"
stack: ["Next.js", "FastAPI", "WebSocket"]
links:
  repo: "github.com/kknaks/homelab-console"
  live: "https://homelab.kknaks.dev"
---

# 프로젝트 포스트모템 — 왜 만들었는지, 어떻게 풀었는지
```

**필수**: `type`, `id`, `title`, `summary`, `category`, `status`, `stack`
**선택**: `date`, `links`

### 3.4 `notes/slug.md`

```yaml
---
type: note
id: python-asyncio                 # 파일 slug과 동일 (위키링크 타깃)
title: { ko: "Python asyncio 기본기", en: "Python asyncio Basics" }
date: "2026.04.10"
tags: ["#python", "#async"]
group: py                          # _meta.yaml/notes.clusters[].id
---

# Python asyncio 기본기

본문 자유 서술. 다른 노트 참조는 [[fastapi-dependency-injection]] 같이.

> 백링크는 백엔드가 자동 추출 — frontmatter에 박지 않음.
```

**필수**: `type`, `id`, `title`, `date`, `group`
**선택**: `tags`

**위키링크**: 본문에 `[[other-note-id]]` 박으면 백엔드가 그래프 edge로 추출. 백링크 응답은 자동 계산.

### 3.5 `contents/C-NNN-slug.md`

**작성 모델**: 사용자가 `youtubeId` + `status: pending` 만 박은 stub 을 push → 백엔드 enrich 잡이 frontmatter (title/summary/duration/tags 등) + 본문을 자동으로 채워 `status: published` 로 commit (`adr-05`, `spec-06`).

#### 사용자가 작성하는 stub (입력)

```yaml
---
type: content
id: C-005
youtubeId: dQw4w9WgXcQ
status: pending
intent: |                # optional — 영상에서 강조하고 싶은 점 한 줄
  Postgres GIN 인덱스의 jsonb 활용 시점이 핵심
---
```

본문은 비워둔다 — 잡이 채움.

**사용자 입력 — 필수**: `type`, `id`, `youtubeId`, `status` (= `"pending"`)
**사용자 입력 — 선택**: `intent`

#### 잡이 enrich 한 결과 (`status: published`)

```yaml
---
type: content
id: C-005
youtubeId: dQw4w9WgXcQ
status: published
intent: |
  Postgres GIN 인덱스의 jsonb 활용 시점이 핵심
date: "2026.05.02"
day: "Day 05"
title:   { ko: "Postgres 인덱스 — B-tree vs GIN", en: "..." }
summary: { ko: "인덱스 종류와 적합한 케이스...", en: "..." }
duration: "18:42"
speaker: kknaks
tags: ["#postgres", "#index", "#jsonb"]
concept:
  - "B-tree 는 범위 쿼리에 강함 — 정렬된 자료구조."
  - "GIN 은 다중 값 컬럼 (jsonb, tsvector) 에 강함."
  - "..."
kind: "study"            # study | talk | tutorial | review
transcript: true         # 자막 가용 여부
enriched_at: "2026-05-02T19:30+09:00"
---

## 개요
주제와 왜 중요한지...

## 배경 / 사전 지식
선수 지식·용어 정의...

## 핵심 개념
B-tree, GIN 정의 + 작동 원리...

## 작동 원리
단계별 설명...

## 코드 예시
```sql
-- ...
```

## 함정·실수
...

## 베스트 프랙티스
...

## 참고
(영상 내 명시 없음)
```

**잡이 채우는 키**: `date`, `day`, `title`, `summary`, `duration`, `speaker`, `tags`, `concept` (시안 02 영역 카드용), `kind`, `transcript`, `enriched_at`, `status` (→ `published`).
**본문**: 8 H2 섹션 (개요 / 배경·사전 지식 / 핵심 개념 / 작동 원리 / 코드 예시 / 함정·실수 / 베스트 프랙티스 / 참고) — 시안 03 영역에 markdown 그대로 렌더 (`adr-05`, `spec-06` §3.3).

#### `status` enum

| 값 | 의미 | 누가 박음 |
|---|---|---|
| `pending` | enrich 대기 | 사용자 |
| `published` | 잡이 enrich 완료 | 잡 |
| `error` | enrich 실패 (재시도 필요) | 잡 |

`error` 일 때 추가로 `error_reason: "..."`, `errored_at: ISO` 박힘. 사용자는 stub 의 `youtubeId` / `intent` 수정 후 `status: pending` 으로 되돌리고 push 하면 다음 잡 tick 에 재처리 (`spec-06` §7).

#### 사용자 검수 흐름 (멱등)

잡이 `published` 박은 후 사용자가 본문 또는 frontmatter 수정해서 push 해도, `status: published` 면 잡이 다시 덮지 않는다 (`spec-06` §8). 즉 잡 출력은 *초안*, 사용자 수정이 *최종*.

#### 사이트 표시

`/api/contents` 응답에 `status: published` 만 노출. `pending`/`error` 는 제외 (`spec-02` 갱신 필요 — 본 spec 시점 별개 task).

상세 잡 명세는 `spec-06`.

### 3.6 `daily/YYYY-MM-DD.md`

잔디 잡(spec-03)의 입력 소스. 자유 서술 → LLM이 종합 요약.

```yaml
---
type: daily
date: "2026.04.30"
---

# 오늘 한 일

- API 캐싱 레이어 추가
- Postgres GIN 인덱스 실험
- spec-01 박음 (이 문서)

(자유 서술 — 잔디 잡이 통째로 LLM에 넘김)
```

**필수**: `type`, `date`
**선택**: 없음 (본문이 곧 데이터)

---

## 4. 잡 산출물 — `activity.yaml`

스케쥴러(spec-03 별도 명세)가 매일 갱신. 사람이 직접 만지지 않음.

```yaml
since: "2025.05.01"
until: "2026.05.01"
totalCount: 487
items:
  - date: "2026.04.30"
    count: 5
    kind: "commit"                 # commit | note | study | null
    summary:
      ko: "API 캐싱 레이어 추가 + Postgres GIN 인덱스 실험"
      en: "Added API caching layer + experimented with Postgres GIN index"
  - date: "2026.04.29"
    count: 0
    kind: null
    summary: null
  # ...365개 항목
```

`kind` enum 5종 중 `ship`은 본 spec 시점엔 미사용 (spec-03에서 정의 시 추가).

---

## 5. 메타 정의 — `_meta.yaml`

카테고리·클러스터 enum과 표시 메타(라벨 ko/en, 정렬 순서, 색상)를 한 파일에 박음. frontmatter의 `category`, `group` 필드는 이 파일의 `id`를 참조.

```yaml
projects:
  categories:
    - id: web
      label: { ko: "Web", en: "Web" }
      order: 1
    - id: cli
      label: { ko: "CLI", en: "CLI" }
      order: 2
    - id: bot
      label: { ko: "Bot", en: "Bot" }
      order: 3

notes:
  clusters:
    - id: ai
      label: { ko: "AI",     en: "AI" }
      color: "#7aa2f7"
      order: 1
    - id: py
      label: { ko: "Python", en: "Python" }
      color: "#9ece6a"
      order: 2
    - id: infra
      label: { ko: "Infra",  en: "Infra" }
      color: "#ff9e64"
      order: 3
    - id: cs
      label: { ko: "CS",     en: "CS" }
      color: "#bb9af7"
      order: 4
    - id: misc
      label: { ko: "기타",   en: "Misc" }
      color: "#7dcfff"
      order: 5
```

**참조 규칙**: `notes/*.md`의 `group: py`가 `_meta.yaml/notes.clusters[].id`에 없으면 검증 에러 (백엔드 부팅 시 fail-fast).

---

## 6. 검증 (백엔드 부팅 시)

### 6.1 강제 검증 (위반 시 부팅 fail)

- 모든 md 파일에 frontmatter 존재
- 카테고리별 필수 필드 모두 박힘 (위 §3 표 기준)
- `notes.group` / `projects.category` 가 `_meta.yaml` 의 등록된 id 안에 있음
- `notes/*.md` 의 frontmatter `id` == 파일명 slug
- `contents/*.md` 의 frontmatter `id` (예: `C-005`) == 파일명 prefix (`C-005-...`)
- `daily/*.md` 의 `date` 필드와 파일명(`YYYY-MM-DD`) 일치
- `_meta.yaml` 의 enum id 중복 없음

### 6.2 경고 (로그만 남김)

- i18n 객체에 한쪽 언어 누락 (예: `en`만 있고 `ko` 없음)
- `notes/*.md` 본문의 `[[unknown-id]]` 위키링크 (타깃 노트 미존재)
- `tags`/`stack` 빈 배열
- frontmatter URL 필드 (예: `avatarUrl`) 가 `/assets/...` 컨벤션 밖 (`http://`, `https://`) — 외부 URL 허용은 하되 SoT 기조 깨짐 알림

(부팅 검증 로직 자체는 spec-02 또는 별도 spec에서 명세)

---

## 7. 향후 확장 여지 (이 spec 범위 밖)

- 페르소나 외부 활용처 (이력서 자동 생성, AI 컨텍스트 dump) — 같은 md SoT 재활용
- `daily/` 의 주간/월간 자동 종합 → `weekly/`, `monthly/` 카테고리 추가 가능
- `ship` kind 정의 시 `releases/` 카테고리 신설 옵션
- 검색 인덱스 (memory inverted index) 외에 임베딩 도입 — 데이터 만 단위 넘을 때 검토 (planning-01 §6 incremental 원칙)
