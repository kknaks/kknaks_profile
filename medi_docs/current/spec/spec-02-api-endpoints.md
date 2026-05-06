---
id: spec-02
type: spec
title: API 엔드포인트 명세 — SLOTS.md 흡수 + 페르소나→JSON 변환 룰
status: draft
created: 2026-05-01
updated: 2026-05-01
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
tags: [spec, api, endpoints, i18n]
---

# API 엔드포인트 명세

## Summary

`claude_design/SLOTS.md` (디자인 v0.5)를 흡수해서 백엔드 엔드포인트 12개 + 응답 스키마를 정의. 페르소나 md(spec-01)를 입력으로, JSON을 출력. i18n 분기(ADR-02)·위키링크 파싱·잔디 격자 변환 룰 포함.

> **⚠ 디자인 동기화**: 본 spec은 `claude_design/SLOTS.md` v0.5 (디자인 v0.5 동결본) 기준. 디자인 변경 시 (1) SLOTS.md 갱신 → (2) 본 spec 동기화 → (3) `frontend/` fetcher 수정. 이 흐름 깨지면 프론트-백 응답 mismatch 발생.

---

## 1. 명명 규칙 (SLOTS.md §1)

| 표현 | 의미 |
|---|---|
| `user.intro` | 단일 필드 |
| `career[].title` | 배열 원소의 필드 (반복 N번) |
| `notes.recent[].path` | 중첩 객체의 배열 |
| `user.stack[]` | 배열 자체 (프론트가 통째로 받아 .map) |
| `[0]`, `[1]` | 명시 인덱스 — 미리보기 등 "처음 N개"만 쓰는 곳 |

---

## 2. 엔드포인트 목록

| 메서드 | 경로 | 입력 | 응답 핵심 키 | 페르소나 소스 |
|---|---|---|---|---|
| GET | `/api/site` | `?lang=ko\|en` | `site.*`, `files.*` | `_meta.yaml` (또는 `profile.md` 일부) |
| GET | `/api/me` | `?lang=ko\|en` | `user.*`, `hero.*`, `about.*` | `profile.md` |
| GET | `/api/activity` | `?lang=ko\|en` | `activity.totalCount`, `activity[]` | `activity.yaml` |
| GET | `/api/career` | `?lang=ko\|en` | `career.*`, `career[]` | `career/*.md` (display_order 정렬) |
| GET | `/api/projects` | `?lang=ko\|en` | `projects.*`, `projects[]` | `projects/*.md` + `_meta.yaml/projects.categories` |
| GET | `/api/notes/graph` | (없음) | `notes.totalCount`, `notes.graph.{clusters,nodes,edges}`, `notes.topics[]` | `notes/*.md` + `_meta.yaml/notes.clusters` |
| GET | `/api/notes/recent` | `?lang=ko\|en&limit=5` | `notes.recent[]` | `notes/*.md` (date desc) |
| GET | `/api/notes/{id}` | `?lang=ko\|en` | `notes.detail.{...,backlinks[]}` | `notes/{id}.md` + 위키링크 역추적 |
| GET | `/api/notes/search` | `?q=...&lang=ko\|en` | `notes.recent[]` (동일 형식) | inverted index over `notes/*.md` |
| GET | `/api/contents` | `?lang=ko\|en&limit=5` | `contents.*`, `contents[]` | `contents/*.md` (date desc) |
| GET | `/api/contents/{id}` | `?lang=ko\|en` | `contents.detail.{...,newer,older}` | `contents/{id}.md` + 인접 항목 |
| GET | `/api/algorithms` | `?lang=ko\|en` | `algorithms.*` (subtitle, intro, totalCount, today), `algorithms[]` | `algorithms/*.md` (date desc) — spec-07 |
| GET | `/api/algorithms/{id}` | `?lang=ko\|en` | `algorithms.detail.{...,newer,older}` | `algorithms/{id}-*.md` 본문 `## Data` yaml + 인접 항목 — spec-07 |
| GET | `/api/print/resume` | (없음) | `profile, about, skills, career[], education[], awards[], projects[]` | `profile.md` + `career/*.md` + `projects/*.md` (visible:true 첫 4개, slim id/title/period/summary) — KO+EN 합본 i18n 미적용 |
| GET | `/api/print/portfolio` | (없음) | `profile, projects[]` | `projects/*.md` (visible:true 만, KO+EN 합본) |
| GET | `/assets/{path}` | (없음) | (정적 — image/*) | `persona/assets/{path}` 직접 서빙 (spec-01 §2.5) |

> `/api/print/*` 는 사이트 API 와 분리 (planning-02 §4) — KO+EN 합본 PDF 라 i18n 미적용 raw `{ko, en}` 객체 그대로 응답. `?lang=` 무시.

> `/assets/*` 는 API 라우트가 아니라 FastAPI `StaticFiles` mount. `/api/` prefix 안 붙음 (이유: md frontmatter URL 필드는 `/assets/profile/me.png` 처럼 박혀 사이트 동일 origin 에서 풀려야 함).

---

## 3. 응답 스키마 (각 엔드포인트)

### 3.1 `GET /api/site?lang=ko`

사이트 전역 (footer, version 등). 정적 라벨이 많아 `_meta.yaml` 또는 `profile.md` 일부에서 추출.

```jsonc
{
  "site": {
    "footerTagline": "홈서버에서 직접 호스팅하는 작은 포트폴리오.",
    "location":      "seoul · KST",
    "version":       "0.1.0 · stable",
    "uptime":        "99.4%",
    "year":          "2026"
  },
  "files": {
    "resumeLabel":    "이력서 (PDF)",
    "portfolioLabel": "포트폴리오 (PDF)"
  }
}
```

### 3.2 `GET /api/me?lang=ko`

About + Hero + Footer 연락처. 입력 = `persona/profile.md`.

```jsonc
{
  "user": {
    "handle":     "kknaks",
    "name":       "이건학",                    // lang에 따라 한쪽
    "role":       "백엔드 엔지니어",              // lang에 따라 한쪽
    "years":      "1년차",
    "location":   "서울, 대한민국",                // lang에 따라 한쪽
    "focus":      "AI · Python · Infra",
    "email":      "kknaks@gmail.com",
    "github":     "github.com/kknaks",
    "linkedin":   "linkedin/in/kknaks",
    "avatarUrl":  "/assets/profile/me.png",
    "tagline":    "...lang에 따라 한쪽...",
    "intro":      "...lang에 따라 한쪽...",
    "intro2":     "...optional...",
    "stack":      ["Python", "FastAPI", ...],
    "stackShort": "Next.js · Python",
    "cards": [
      { "title": "...", "body": "..." }
      // 4개
    ]
  },
  "hero":  { "headline": "...\n...\n...", "subline": "..." },
  "about": { "subtitle": "만드는 사람" }
}
```

### 3.3 `GET /api/activity?lang=ko`

About 페이지 잔디. 입력 = `persona/activity.yaml`.

```jsonc
{
  "activity": {
    "totalCount": 487,
    "since":      "2025.05.01",
    "until":      "2026.05.01"
  },
  "activity[]": [
    {
      "date":    "2026.04.30",
      "count":   5,
      "kind":    "commit",       // commit | note | study | null
      "summary": "..."           // lang 분기. summary 외 필드는 정적
    }
    // ...365개
  ]
}
```

### 3.4 `GET /api/career?lang=ko`

```jsonc
{
  "career": {
    "subtitle":   "1년 · 1개 역할",       // _meta.yaml 또는 자동 집계
    "totalYears": "1 yr",
    "totalRoles": "1 role",
    "focus":      "backend · AI\nRAG · infra"
  },
  "career[]": [
    {
      "period":   "2025.06 — present",
      "title":    "...",
      "org":      "...",
      "location": "...",
      "summary":  "...",
      "stack":    ["Python", "FastAPI", ...]
    }
    // display_order 오름차순
  ]
}
```

### 3.5 `GET /api/projects?lang=ko`

> spec-01 §3.3 — `visible: false` 박힌 항목은 응답에서 제외 (사이트 노출 부담 있는 회사 내부 도구 등). `totalCount`, `categories.count` 도 visible 항목 기준.
>
> 잔디 잡 (`spec-03 §2.4`) 의 `extract_tracked_repos` 는 visible 무관 모든 projects 의 `links.repo` 를 추적.

```jsonc
{
  "projects": {
    "subtitle":   "혼자 만든 것들",
    "totalCount": 6,                   // visible: true 만 카운트
    "categories": [
      // _meta.yaml/projects.categories[] 에서 빌드. count는 visible 기준 자동 집계
      { "id": "web", "label": "Web", "count": 3 },
      ...
    ]
  },
  "projects[]": [                      // visible: false 항목 제외
    {
      "id":        "P-01",
      "title":     "Homelab Console",
      "summary":   "...",
      "category":  "web",
      "status":    "wip",
      "date":      "2026.04",
      "stack":     ["Next.js", "FastAPI"],
      "thumbnail": "/assets/projects/P-01/cover.png",  // optional. 미박음 시 null
      "links":     { "repo": "...", "live": "..." }
    }
    // ...
  ]
}
```

### 3.6 `GET /api/notes/graph` (언어 무관)

```jsonc
{
  "notes": {
    "totalCount": 18,
    "edgeCount":  31,
    "graph": {
      "clusters": [
        // _meta.yaml/notes.clusters[]. color는 응답에 포함 (프론트가 사용)
        { "id": "ai", "label": "AI", "color": "#7aa2f7" },
        ...
      ],
      "nodes": [
        { "id": "rag-basics", "title": "...", "group": "ai" }
        // title은 lang 무관 — graph 엔드포인트라 ko 기본값으로 박음 (또는 둘 다)
      ],
      "edges": [
        { "source": "rag-basics", "target": "bge-m3" }
        // notes/*.md 본문의 [[id]] 위키링크 파싱 결과
      ]
    },
    "topics": [{ "tag": "AI", "count": 42 }, ...]   // tags 자동 집계
  }
}
```

> **언어 처리**: graph는 언어 무관 엔드포인트. node `title`은 ko 기본값 1개만 박음 (graph 데이터 크기 줄이기). lang 분기 필요 시 별도 endpoint (`/api/notes/{id}`)로 디테일 조회.

### 3.7 `GET /api/notes/recent?lang=ko&limit=5`

랜딩 04 섹션, About 옆 미리보기.

```jsonc
{
  "notes.recent[]": [
    { "id": "rag-basics", "title": "...", "date": "2026.04.10", "path": "AI/LLM" }
  ]
}
```

`path`는 `_meta.yaml/notes.clusters[].label` 기반 가공 (예: cluster `ai` + tag `#llm` → "AI/LLM").

### 3.8 `GET /api/notes/{id}?lang=ko`

```jsonc
{
  "notes.detail": {
    "id":        "rag-basics",
    "title":     "...",
    "date":      "2026.04.10",
    "tags":      ["#ai", "#rag"],
    "body":      "# 제목\n\n본문 마크다운...",   // 위키링크 [[id]] 그대로 보존 (프론트가 렌더)
    "backlinks": [
      { "id": "daily-2026-04-30", "title": "..." }
      // 다른 노트 본문에서 [[rag-basics]] 참조하는 것들 자동 추출
    ]
  }
}
```

### 3.9 `GET /api/notes/search?q=...&lang=ko`

응답은 `/api/notes/recent` 와 동일 형식. 메모리 inverted index (spec-01 §6 외 별도 명세에서 다룸).

### 3.10 `GET /api/contents?lang=ko&limit=5`

```jsonc
{
  "contents": {
    "subtitle":   "매일 업로드 · 영상 + 교안",
    "intro":      "매일 한 편씩...",
    "totalCount": 47
  },
  "contents[]": [
    {
      "id":        "C-005",
      "date":      "2026.04.30",
      "day":       "Day 05",
      "title":     "...",
      "youtubeId": "...",
      "duration":  "18:42",
      "summary":   "...",
      "tags":      ["#postgres", "#index"]
    }
    // date desc
  ]
}
```

### 3.11 `GET /api/contents/{id}?lang=ko`

```jsonc
{
  "contents.detail": {
    "id":        "C-005",
    "date":      "2026.04.30",
    "day":       "Day 05",
    "title":     "...",
    "summary":   "...",
    "youtubeId": "...",
    "duration":  "18:42",
    "speaker":   "kknaks",
    "tags":      ["#postgres", "#index"],
    "concept":   ["...", "...", ...],   // md 본문의 ## 개념 섹션 파싱
    "example":   ["...", "...", ...],   // md 본문의 ## 적용 예시 섹션 파싱
    "newer":     { "id": "C-006", "title": "..." },   // null 가능
    "older":     { "id": "C-004", "title": "..." }
  }
}
```

> 본문 섹션 파싱 (`## 개념`, `## 적용 예시`) 은 contents 카테고리 컨벤션. spec-01 §3.5 참조.

---

## 4. 페르소나 → API 변환 룰

### 4.1 i18n helper (ADR-02)

```python
def i18n(node, lang: str = "ko"):
    """ {ko: "a", en: "b"} → "a" 또는 "b". scalar/list는 그대로 통과 """
    if isinstance(node, dict) and lang in node:
        return node[lang]
    if isinstance(node, dict) and "ko" in node:
        return node["ko"]   # fallback to 마스터 언어 (ADR-02 §2.4)
    return node
```

응답 dict를 재귀적으로 i18n 적용하는 wrapper도 권장:

```python
def apply_i18n(obj, lang: str):
    if isinstance(obj, dict):
        # {ko, en} 객체면 한쪽 추출, 아니면 재귀
        if obj.keys() == {"ko", "en"} or {"ko"} <= obj.keys() <= {"ko", "en"}:
            return i18n(obj, lang)
        return {k: apply_i18n(v, lang) for k, v in obj.items()}
    if isinstance(obj, list):
        return [apply_i18n(x, lang) for x in obj]
    return obj
```

### 4.2 위키링크 파싱

`notes/*.md` 본문의 `[[other-id]]`를 정규식으로 추출 → 그래프 edge + backlink 인덱스 빌드.

```python
import re
WIKILINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")

def extract_wikilinks(body: str) -> list[str]:
    return WIKILINK_RE.findall(body)

# 부팅 시:
edges = []
backlinks: dict[str, list[str]] = {}
for note_id, note in _data["notes"].items():
    for target_id in extract_wikilinks(note["body"]):
        edges.append({"source": note_id, "target": target_id})
        backlinks.setdefault(target_id, []).append(note_id)
```

`/api/notes/{id}` 응답의 `backlinks[]`는 이 인덱스에서 추출.
`/api/notes/graph` 응답의 `edges[]`는 그대로 노출.

### 4.3 잔디 격자 변환 (선택 — 보통 프론트 책임)

`activity.yaml/items[]` 는 date 기준 sparse 배열. 7×53 격자(년 단위 잔디)에 배치하는 책임은 일반적으로 프론트.

만약 백엔드가 grid로 변환해서 응답하고 싶다면:

```python
def to_grid(items: list, since: date, until: date) -> list[list[dict | None]]:
    by_date = {item["date"]: item for item in items}
    weeks = ...  # 53주 × 7일
    return weeks
```

본 명세 시점엔 sparse 배열로 응답 (프론트 변환). 향후 grid 응답 옵션 필요해지면 추가.

### 4.4 `_meta.yaml` 합성

`/api/projects.categories[]` 의 `count` 같은 필드는 `_meta.yaml/projects.categories[]` 에 `projects/*.md` 의 `category` 필드를 매칭해서 자동 집계:

```python
def build_category_response(meta: dict, items: list, lang: str) -> list[dict]:
    counts = Counter(item["category"] for item in items)
    return [
        {
            "id":    cat["id"],
            "label": i18n(cat["label"], lang),
            "count": counts.get(cat["id"], 0)
        }
        for cat in sorted(meta["categories"], key=lambda c: c["order"])
    ]
```

---

## 5. 빠진 것 (의도적 — SLOTS.md §4)

다음은 응답에 포함하지 않음:

- 랜딩 터미널 출력 (`whoami`, `cat stack.txt` 등) — 프론트에 박음 (데모 연출)
- 정적 라벨 (About / Career / Projects / Notes / Contents 헤더, 카테고리 'All' 등) — 프론트 i18n 리소스
- 푸터 brand-bound 문구 ("built with next.js + python") — 프론트 정적
- 번호 인덱스 (`01`, `02`, `03.01` 등 디스플레이 숫자) — 프론트 자동

---

## 6. 디자인 동기화 정책

본 spec은 `claude_design/SLOTS.md` v0.5 동결본 기준. 디자인 변경 발생 시:

1. 디자인 시안 갱신 (`claude_design/`)
2. SLOTS.md 새 슬롯/제거 슬롯 반영
3. 본 spec (spec-02) 동기화 — 엔드포인트 추가/제거 또는 응답 스키마 수정
4. 영향 받은 프론트 fetcher 수정 (`frontend/`)
5. 백엔드 핸들러 수정 (`back/`)

위 흐름 깨지면 프론트-백 응답 mismatch 발생. plan-01에서 이 흐름의 도구화(예: 슬롯 vs API 응답 키 자동 비교 스크립트) 검토.

---

## 7. 향후 확장 여지 (이 spec 범위 밖)

- 검색 인덱스 빌드 룰 → 별도 spec
- 부팅 시 페르소나 → 메모리 dict 로드 룰 → 별도 spec
- 잔디 잡 (activity.yaml 자동 갱신) → spec-03
- API rate limiting / caching → 동적 기능 도입 시
