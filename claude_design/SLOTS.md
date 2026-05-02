# kknaks.dev — Slot 명세서 (v1.0-pre)

> 모든 mock을 `{{slot}}`으로 교체한 결과. 이 문서가 곧 백엔드 API 명세의 입력.
> i18n 정책 = **A안** — 슬롯에 `.ko/.en` 안 붙임. 서버가 `?lang=` 쿼리로 분기.

---

## 1. 명명 규칙

- `user.intro` — 단일 필드
- `career[].title` — 배열 원소의 필드 (반복 N번)
- `notes.recent[].path` — 중첩 객체의 배열
- `user.stack[]` — 배열 자체 (프론트가 통째로 받아 .map)
- `[0]`, `[1]` 같은 명시 인덱스 — 미리보기 등 "처음 N개"만 쓰는 곳

---

## 2. 엔드포인트별 응답 스키마

### `GET /api/site?lang=ko`
사이트 전역 (footer, version 등).

| slot | 예시 |
|---|---|
| `site.footerTagline` | "홈서버에서 직접 호스팅하는 작은 포트폴리오." |
| `site.location` | "seoul · KST" |
| `site.version` | "0.1.0 · stable" |
| `site.uptime` | "99.4%" |
| `site.year` | "2026" |
| `files.resumeLabel` | "이력서 (PDF)" |
| `files.portfolioLabel` | "포트폴리오 (PDF)" |

### `GET /api/me?lang=ko`
About + Hero + Footer 연락처.

```jsonc
{
  "user": {
    "handle":     "kknaks",
    "name":       "이건학",
    "role":       "Backend Engineer",
    "years":      "1년차",
    "location":   "Seoul, KR",
    "focus":      "AI · Python · Infra",
    "email":      "kknaks@gmail.com",
    "github":     "github.com/kknaks",
    "linkedin":   "linkedin/in/kknaks",
    "avatarUrl":  "https://cdn.kknaks.dev/me.jpg",  // About 페이지 88px 원형 + 추후 다른 곳에서도 사용 가능
    "tagline":    "호기심으로 시작해서, 도전으로 만들고, 개발로 풀어냅니다.",
    "intro":      "저는 새로운 것을 도전하고...",
    "intro2":     "지금은 AI 회사에서...",   // optional
    "stack":      ["Python", "FastAPI", ...],     // user.stack[]
    "stackShort": "Next.js · Python",             // About 사이드바용 짧은 버전
    "cards": [
      { "title": "지금 일하는 곳", "body": "AI 회사 ·..." },
      { "title": "만들고 있는 것", "body": "..." },
      { "title": "관심 있는 기술", "body": "..." },
      { "title": "일하는 방식",    "body": "..." }
    ]
  },
  "hero": {
    "headline":    "내 홈서버 위에서\n돌아가는\n제품을 만든다.",   // 줄바꿈 \n 허용
    "subline":     "풀스택 엔지니어. ..."
    // CTA 라벨은 정적 — 라우팅 액션이라 슬롯 X
  },
  "about":  { "subtitle": "만드는 사람" }
}
```

### `GET /api/activity?lang=ko`
About 페이지 잔디 (AI가 가공한 활동 히트맵).

```jsonc
{
  "activity": {
    "totalCount": 487,            // 지난 1년 활동 합계
    "since":      "2025.05.01",   // 격자 시작일
    "until":      "2026.05.01"    // 격자 끝일 (오늘)
  },
  "activity[]": [
    {
      "date":    "2026.04.30",     // YYYY.MM.DD
      "count":   5,                // 그날 활동 수
      "kind":    "commit",         // commit | note | study | ship | null(=count 0)
      "summary": "RAG 파이프라인 리팩토링 — 임베딩 캐싱 추가"  // AI 가공 요약, 클릭 시 표시
    },
    ...
  ]
}
```

> **언어 처리**: `summary`만 lang 분기. `kind`는 enum이라 정적 라벨로 매핑.
> **격자 구조**: 프론트가 `date` 기준으로 7×53 격자에 배치. 빈 칸은 자동.

### `GET /api/career?lang=ko`
```jsonc
{
  "career": {
    "subtitle":   "1년 · 1개 역할",
    "totalYears": "1 yr",
    "totalRoles": "1 role",
    "focus":      "backend · AI\nRAG · infra"   // \n으로 줄바꿈
  },
  "career[]": [
    {
      "period":   "2025.06 — present",
      "title":    "Backend Engineer",
      "org":      "Stealth AI Co.",
      "location": "서울 · 하이브리드",
      "summary":  "LLM 기반 B2B 제품의 백엔드. ...",
      "stack":    ["Python", "FastAPI", "Postgres", ...]
    },
    ...
  ]
}
```

### `GET /api/projects?lang=ko`
```jsonc
{
  "projects": {
    "subtitle": "혼자 만든 것들",
    "totalCount": 6,
    "categories": [
      // 가변 — DB에서 관리. 'all'은 프론트가 totalCount로 표시.
      { "id": "web", "label": "Web", "count": 3 },
      { "id": "cli", "label": "CLI", "count": 1 },
      { "id": "bot", "label": "Bot", "count": 2 }
    ]
  },
  "projects[]": [
    {
      "id":      "P-01",
      "title":   "Homelab Console",
      "summary": "홈서버 메트릭...",
      "category":"web",   // categories[].id 중 하나
      "status":  "wip",   // 'live' | 'wip' | 'archived'
      "date":    "2026.04",
      "stack":   ["Next.js", "FastAPI", "WebSocket"],
      "links":   { "repo": "github.com/...", "live": "https://..." }
    },
    ...
  ]
}
```

### `GET /api/notes/graph`  *(언어 무관 — 그래프 구조만)*
```jsonc
{
  "notes": {
    "totalCount": 18,
    "edgeCount":  31,
    "graph": {
      "clusters": [
        // 가변 — DB에서 관리. id는 nodes[].group이 참조.
        // color는 프론트가 id로 매핑(서버 응답에 포함 X).
        { "id": "ai",    "label": "AI" },
        { "id": "py",    "label": "Python" },
        { "id": "infra", "label": "Infra" },
        { "id": "cs",    "label": "CS" },
        { "id": "daily", "label": "Daily" }
      ],
      "nodes": [{ "id": "rag-basics", "title": "RAG 기본 구조", "group": "ai", "links": [...] }, ...],
      "edges": [{ "source": "rag-basics", "target": "bge-m3" }, ...]   // links에서 파생 가능
    },
    "topics": [{ "tag": "AI", "count": 42 }, ...]   // notes.topics[]
  }
}
```

> **언어 처리**: 그래프 노드의 `title`만 lang에 따라 다름. 노드 데이터가 크면 제목만 별도 엔드포인트로 분리하는 것도 고려.

### `GET /api/notes/recent?lang=ko&limit=5`
랜딩 04 섹션, About 옆 미리보기, Notes 모바일 리스트.
```jsonc
{
  "notes.recent[]": [
    { "id": "rag-basics", "title": "RAG 기본 구조", "date": "2026.04.10", "path": "AI/LLM" },
    ...
  ]
}
```

### `GET /api/notes/{id}?lang=ko`
노트 상세 (그래프 노드 클릭 시).
```jsonc
{
  "notes.detail": {
    "id":        "rag-basics",
    "title":     "RAG 기본 구조",
    "date":      "2026.04.10",
    "tags":      ["#ai", "#rag", "#embedding"],
    "body":      "# RAG 기본 구조\n\n> Retrieval...",   // 마크다운
    "backlinks": [{ "id": "daily-2026-03", "title": "2026-03 트러블슈팅" }]
  }
}
```

### `GET /api/notes/search?q=...&lang=ko`
검색 결과. 응답은 `notes.recent[]`와 동일 형태.

### `GET /api/contents?lang=ko&limit=5`
리스트 (랜딩 + Contents 페이지).
```jsonc
{
  "contents": {
    "subtitle":   "매일 업로드 · 영상 + 교안",
    "intro":      "매일 한 편씩 — 유튜브 영상을 보고...",
    "totalCount": 47
  },
  "contents[]": [
    {
      "id":        "C-005",
      "date":      "2026.04.30",
      "day":       "Day 05",
      "title":     "Vector DB 기본기 — HNSW가 왜 빠른가",
      "youtubeId": "dQw4w9WgXcQ",
      "duration":  "18:42",
      "summary":   "벡터 검색의 기본...",
      "tags":      ["#AI", "#VectorDB", "#HNSW"]
    },
    ...
  ]
}
```

### `GET /api/contents/{id}?lang=ko`
상세.
```jsonc
{
  "contents.detail": {
    "id":        "C-005",
    "date":      "2026.04.30",
    "day":       "Day 05",
    "title":     "...",
    "summary":   "...",
    "youtubeId": "dQw4w9WgXcQ",
    "duration":  "18:42",
    "speaker":   "kknaks",
    "tags":      ["#AI", "#VectorDB"],
    "concept":   ["HNSW는 다층 그래프...", "...", ...],   // 가변 길이
    "example":   ["사내 RAG에서 ...", ...],               // 가변 길이
    "newer":     { "id": "C-006", "title": "..." },       // null 가능
    "older":     { "id": "C-004", "title": "..." }
  }
}
```

---

## 3. DB 스키마 힌트 (백엔드 작업용)

언어별 컬럼은 같은 테이블에 `_ko`, `_en` 접미사로:

```sql
-- 예: career
CREATE TABLE career (
  id          SERIAL PRIMARY KEY,
  period      TEXT,           -- 언어 무관
  title_ko    TEXT, title_en  TEXT,
  org_ko      TEXT, org_en    TEXT,
  location_ko TEXT, location_en TEXT,
  summary_ko  TEXT, summary_en TEXT,
  stack       TEXT[],         -- 태그는 다국어 X
  display_order INT,
  is_current  BOOLEAN
);
```

API 핸들러:
```python
@router.get("/api/career")
def get_career(lang: str = "ko"):
    rows = db.query(Career).order_by(Career.display_order).all()
    return {
      "career[]": [{
        "period":   r.period,
        "title":    getattr(r, f"title_{lang}"),
        "org":      getattr(r, f"org_{lang}"),
        ...
      } for r in rows]
    }
```

---

## 4. 슬롯에서 빠진 것 (의도적)

- 랜딩 터미널 출력 (`whoami`, `cat stack.txt` 등) — 데모 연출이라 프론트에 박음
- 정적 라벨 (About / Career / Projects / Notes / Contents 헤더, 카테고리 'All/Web/CLI/Bot' 등)
- 푸터의 "built with next.js + python" 같은 brand-bound 문구
- 번호 인덱스 (`01`, `02`, `03.01` 같은 디스플레이 숫자)

---

## 5. 다음 단계

1. ⬜ 위 슬롯 키 이름 사용자 검수 (네이밍 다듬기)
2. ⬜ DB 스키마 확정 + 마이그레이션
3. ⬜ FastAPI 엔드포인트 스켈레톤
4. ⬜ Next.js fetcher 작성 (lang은 URL state로 보존, 헤더 스위치 시 refetch)
5. ⬜ 슬롯 자리에 실 데이터 주입 → 프로토타입에서 production으로 승격
