# import-project 룰

## 1. frontmatter 추출

### id
기존 `persona/projects/*.md` 의 frontmatter `id: P-NN` 최댓값 + 1. 첫 프로젝트는 `P-01`.

```bash
grep -h "^id: P-" persona/projects/*.md | sed 's/id: P-//' | sort -n | tail -1
```

### title
우선순위:
1. `README.md` 의 첫 H1 (`^# `)
2. `package.json` `.name` 또는 `pyproject.toml` `[project].name`
3. 디렉토리명 (단어별 첫 글자 대문자, 하이픈 → 공백)

i18n: `{ ko, en }` 둘 다 동일값 박음 (사용자가 정정).

### summary
우선순위:
1. README 첫 단락 첫 문장 (마크다운 헤더·이미지 제거 후)
2. `package.json` `.description`
3. README intro 80자 발췌

**80자 이내** 한 줄. 마침표 제거. i18n 둘 다 동일값.

### date
첫 커밋 월:
```bash
git -C <repo-dir> log --reverse --format="%ad" --date=format:"%Y.%m" | head -1
```

### links.repo
```bash
git -C <repo-dir> remote get-url origin
```

ssh → https 변환:
- `git@github.com:owner/repo.git` → `github.com/owner/repo`
- `https://github.com/owner/repo.git` → `github.com/owner/repo`

### links.live
README 내 `https://...` URL 중 첫 매치. heuristic 우선순위:
1. `kknaks.dev` 도메인
2. `vercel.app`, `netlify.app`, `*.io` 같은 배포 도메인
3. `github.com/<owner>/<repo>` 자체는 제외 (이미 links.repo)

매치 없으면 `links.live` 필드 자체 생략.

---

## 2. stack 추론

### Node 프로젝트 (`package.json`)

`dependencies` + `devDependencies` 키 중 **frameworks / runtimes / 인프라 도구**만:

#### 포함
- 프레임워크: `next`, `react`, `vue`, `svelte`, `nuxt`, `express`, `fastify`, `nestjs`, `astro`
- 모바일: `react-native`, `expo`
- 언어/타입: `typescript` (이게 들어가면 stack 에 `TypeScript` 박음)
- DB/ORM: `prisma`, `drizzle-orm`, `sequelize`, `mongoose`, `typeorm`
- 상태 관리: `redux`, `zustand`, `recoil`, `jotai` (선택 — 핵심 아니면 생략)
- 빌드: `vite`, `webpack` (가시적이면)
- 테스트: `jest`, `vitest`, `playwright`, `cypress` (선택)

#### 제외 (lib 영역)
- `lodash`, `dayjs`, `date-fns`, `axios`, `clsx`, `tailwindcss` (utility lib — 가시적 stack 아님)
- `eslint`, `prettier`, `husky` (도구 — 가시 X)
- `@types/*` (type declarations)

### Python 프로젝트 (`pyproject.toml` / `requirements.txt`)

#### 포함
- 프레임워크: `fastapi`, `django`, `flask`, `starlette`
- ORM: `sqlalchemy`, `tortoise-orm`, `peewee`
- DB driver: `psycopg2`, `asyncpg`, `pymongo` → `Postgres`, `MongoDB` 으로 변환
- 비동기: `celery`, `apscheduler`
- AI/ML: `langchain`, `transformers`, `torch`, `tensorflow`
- 데이터: `pandas`, `numpy`, `polars` (가시적이면)
- 스케쥴러/잡: `airflow`, `prefect`

#### 제외
- `pytest`, `black`, `ruff`, `mypy` (도구)
- `pydantic` (FastAPI에 종속이라 자동)

### Java/Kotlin (`build.gradle` / `pom.xml`)

#### 포함
- `spring-boot`, `spring-webflux`, `spring-cloud`
- `mybatis`, `jpa`, `hibernate`
- `kafka`, `redis`

### 인프라 (Dockerfile, docker-compose.yml, .github/workflows)
- `Dockerfile` 존재 → `Docker`
- `docker-compose.yml` 존재 → `Docker Compose`
- `.github/workflows/*.yml` → `GitHub Actions`
- `kubernetes` manifest (`*.yaml` with `kind:`) → `Kubernetes`
- AWS / Azure / NCP CLI / Terraform 파일 → 각각

### DB
- `docker-compose.yml` 의 image — `postgres` → `Postgres`, `mysql` → `MySQL`, `redis` → `Redis`
- `.env` / `.env.example` 의 `DATABASE_URL` 패턴

### 표기 일관 (`enrich-note/rules.md` §1.3 와 동일)
- `Spring Boot` (공백, PascalCase 단어)
- `Next.js` (점 포함)
- `JavaScript` / `TypeScript` (한 단어)
- `PostgreSQL` 또는 `Postgres` (프로젝트 일관 — profile.md 가 `Postgres` 쓰면 그대로)
- `React Native`, `MongoDB` (제품명 그대로)

### 갯수
보통 5~10개. 30개 이상이면 핵심만. 빈 list 가능 (분석 실패 시).

---

## 3. category 추론

`_meta.yaml/projects.categories[].id` 안에서 매칭. 7개 enum: `web` / `frontend` / `backend` / `mobile` / `ai` / `cli` / `bot`.

### heuristic

| category | 신호 |
|---|---|
| `mobile` | `react-native`, `expo`, `swift`, iOS/Android 디렉토리 |
| `ai` | `langchain`, `transformers`, `torch`, RAG/embedding 키워드 README |
| `frontend` | `react`/`vue`/`svelte` *only* (백엔드 deps 없음). 또는 SPA 명시 |
| `backend` | `fastapi`/`express`/`nestjs`/`spring-boot` *only* (프론트 deps 없음) |
| `web` | 풀스택 — 프론트 + 백엔드 둘 다. `frontend/` + `back(end)/` 디렉토리 분리 |
| `cli` | `bin/` 디렉토리 + `package.json` `.bin`. 또는 `click`/`typer` (Python) |
| `bot` | `discord.js`, `slack-bolt`, `python-telegram-bot` |

여러 개 매치되면 **상위 우선**: `mobile` > `ai` > `web` > `frontend`/`backend` > `cli` > `bot`.

매치 안 되면 `web` (default).

---

## 4. visible 추론

```bash
git -C <repo-dir> remote get-url origin
```

owner 추출 (`github.com/OWNER/repo`):
- owner == `kknaks` → `visible: true`
- 그 외 (회사 org, fork 등) → `visible: false`

### override
- `--hidden` 인자 → 강제 `visible: false` (heuristic 무시)
- `--public` 인자 → 강제 `visible: true` (heuristic 무시)

### remote 없음 (local-only)
`visible: true` (default — 본인 작업물 가정)

---

## 5. 본문 7섹션 분석

### 5.1 `# 개요`
- README 의 첫 H2 직전까지의 단락 (h1 직후 ~ 첫 H2 직전)
- 길이 200자 이내로 압축
- 마크다운 헤더·이미지·뱃지·링크 제거
- 한국어 README 우선 (`README.md`), 영문만 있으면 영문 그대로

### 5.2 `# 기술스택`
프론트/백엔드/인프라 분리. **선택 이유**까지 박는 게 핵심:

```markdown
# 기술스택

**프론트엔드**
- Next.js 14 (App Router) — SSR + 빠른 페이지 전환
- TypeScript — 타입 안전성

**백엔드**
- FastAPI — async + Pydantic 검증 + 자동 docs
- Postgres + SQLAlchemy

**인프라**
- Docker Compose — 로컬 dev + 홈서버 배포 동일
- GitHub Actions — main push 시 자동 배포
```

선택 이유 추출 — README 의 "Why X" / "기술 선택" 섹션 우선. 없으면 deps 만 list 박고 이유는 `(TBD)` 마커.

### 5.3 `# 주요기능`

소스:
- `app/*` (Next.js App Router) → 페이지 list
- `pages/*` (Next.js Pages Router)
- `routes/*` (Express, etc)
- README features / "주요기능" / "Features" 섹션

```markdown
# 주요기능

- **랜딩** (`/`) — Hero + 5섹션 미리보기
- **About** (`/about`) — 자기소개 + 잔디 + Career timeline
- **Notes 그래프** (`/notes`) — force-directed 노트 그래프
- **CLI 명령** (`build`, `deploy`) — homelab 배포 자동화
```

각 항목 1줄 — 경로/명령 + 한 줄 설명.

### 5.4 `# 아키텍처`

소스:
- 최상위 디렉토리 트리 (`tree -L 2 -d`)
- 핵심 디렉토리 책임 (frontend/, backend/, scripts/, etc)
- DB 스키마 (migration / models 디렉토리)
- 외부 서비스 (Redis, S3, OpenAI 등)

```markdown
# 아키텍처

```
foo-app/
├─ frontend/   ← Next.js (App Router)
├─ back/       ← FastAPI + Postgres
├─ scripts/    ← 배포 자동화
└─ docker-compose.yml
```

**데이터 흐름**: 사용자 → frontend (Next.js SSR) → `/api/*` (FastAPI) → Postgres + Redis 캐시.

**외부 의존**: OpenAI API (embeddings), GitHub API (활동 추적).
```

### 5.5 `# 핵심 구현`

소스:
- API 라우터 — FastAPI `@router.get/post`, Express `app.get/post`, Spring `@GetMapping/@PostMapping`
- 주요 React/Vue 컴포넌트 (큰 컴포넌트 또는 핵심 hook)
- 알고리즘이나 자동화 스크립트

```markdown
# 핵심 구현

**API 5개** (FastAPI):
- `GET /api/me` — profile.md → JSON 변환
- `GET /api/career` — display_order 정렬
- ...

**주요 컴포넌트**:
- `<NotesGraph>` — react-force-graph wrapping
- `<TerminalHero>` — 타이핑 애니메이션
```

코드 스니펫은 5~10줄 이내. 핵심 1~2개만.

### 5.6 `# 마주친 문제`

소스:
- `git log --grep="fix\|bug\|issue\|문제\|버그"` 매치 커밋
- README 의 "Troubleshooting" / "문제" 섹션
- TODO / FIXME 주석 분석

```markdown
# 마주친 문제

- **(자동 추론)** WebSocket reconnect 처리 — `git log` 에 reconnect 관련 커밋 3개. 핸드셰이크 timeout 후 backoff 추가.
- **(자동 추론)** Docker 빌드 캐시 무효화 — Dockerfile 의 deps 단계 분리.

> 자동 추론 결과 — 사용자 검토 필수.
```

각 항목 끝에 `(자동 추론)` 마커. 빈 channel 가능.

### 5.7 `# 회고`

소스:
- README "회고" / "Lessons learned" 섹션 (있으면 그대로)
- commit msg 빈도 분석으로 narrative 추론 (refactor 빈도 → "리팩토링 많이 했다" 등)

```markdown
# 회고

> 자동 추론 결과 — 사용자 검토 필수.

- **(자동 추론)** 초기 설계 vs 실제 — refactor 커밋 12개. 초기 monolith → 모듈 분리 과정.
- **(자동 추론)** 다음에 시도하면 — ...
```

거의 항상 `(자동 추론)` 마커. 사용자 회고로 교체 권장.

---

## 6. 출력 형식

### 성공
```
✓ persona/projects/<slug>.md (P-NN)
  title:    <title>
  category: <cat>
  status:   <status>
  visible:  <bool> (owner: <owner>)
  stack:    [<tech>, ...]
  본문 7섹션 자동 채움 (검토 필수):
    1. 개요         ← <소스>
    2. 기술스택     ← <소스>
    ...
```

### 에러
```
× <reason>. abort.
○ <reason>. partial fill.
```

---

## 7. 안전 룰셋 (재확인)

- 단일 디렉토리. 일괄은 외부 loop.
- 기존 파일 존재 시 abort (overwrite X).
- 외부 레포 read-only.
- 7섹션 순서·제목 고정 (spec-01 §3.3 SoT).
- 자동 추론 결과는 *초안* — 사용자 검토 필수, 특히 §5.6 / §5.7.
- `visible: false` 강제 시 사용자가 `--hidden` 명시.
- assets 복사는 본 skill 범위 밖.
