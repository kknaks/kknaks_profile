---
id: planning-02
type: planning
title: 이력서·포트폴리오 PDF 자동 생성
status: draft
created: 2026-05-03
updated: 2026-05-03
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-02-api-endpoints]]"
  - "[[spec-06-content-enrich-job]]"
  - "[[adr-02-i18n-strategy]]"
tags: [planning, print, pdf, persona]
---

# 이력서·포트폴리오 PDF 자동 생성

## Summary

`persona/**/*.md` SoT 에서 자동으로 `kknaks-resume.pdf` / `kknaks-portfolio.pdf` 를 생성해 사이트 footer 다운로드 링크에 연결. 디자인 시안 (`claude_design/kknaks_profile_v2.0.0/print/`) 그대로 포팅 + back jobs 패턴 (spec-06) 재사용.

---

## 1. 배경

- 현재 footer (refactor 후) 의 "이력서 (PDF) ↓" / "포트폴리오 (PDF)" 링크가 `href="#"` 로 비어있음
- 디자인 시안 (`claude_design/kknaks_profile_v2.0.0/`) 의 `print/` 안에 React + 자동 페이지 분할 (Pager) 엔진이 완성되어 있음 — 그대로 포팅
- mock 데이터 (`print/data.jsx` 의 `RESUME_DATA`/`PROJECT_DATA`) 는 현재 persona 스키마보다 풍부 → persona 확장 필요

---

## 2. 핵심 결정

### 2.1 PDF 생성 위치 — back jobs (playwright python)

| 옵션 | 평가 |
|---|---|
| Vercel build + puppeteer (Node) | chrome 바이너리 + 빌드 시간 이슈 |
| **back/service/jobs/pdf_generate.py + playwright python** ⭐ | spec-06 패턴 재사용, stack 일치 (back=python), webhook 기 wired |
| 브라우저 print-to-PDF 버튼 | pager 측정 일관성 X, 자동화 X |

**결정**: back job. 트리거는 webhook (persona/** push 시) + 수동 스크립트 (`scripts/run_pdf_generate.py`).

### 2.2 출력 위치 — `frontend/public/{resume,portfolio}.pdf` 커밋

- 잡이 PDF 떨군 후 `commit_and_push_with_retry` (spec-06 §5 의 `service.jobs.git_push` 재사용) 으로 자동 push
- Vercel 정적 호스팅에서 그대로 서빙 → footer href `/resume.pdf`, `/portfolio.pdf`
- 대안 (백엔드 정적 서빙): CORS·base URL 복잡 → 비채택

### 2.3 합본 정책 — 한 PDF 안에 KO + EN 모두

- `kknaks-resume.pdf` = KO 페이지들 + EN 페이지들 (한 문서)
- `kknaks-portfolio.pdf` = cover + KO 프로젝트들 + EN 프로젝트들
- adr-02 의 `?lang=ko|en` 단일 응답 정책에서 print 만 예외 — `?lang=both` 모드 추가
- 채용 담당자가 한 파일 받으면 KO/EN 동시 확인 가능

### 2.4 라우트 구조 — Next.js `/print/*` 라우트

```
frontend/app/print/
  resume/page.tsx       # KO+EN 합본 (Pager 자동 분할)
  portfolio/page.tsx    # cover + KO+EN 프로젝트들
```

- print 컴포넌트 (`pager.tsx`, `sheet.tsx`, `monogram.tsx`, `arch-box.tsx`) → `frontend/components/print/` 로 포팅
- `print.css` 토큰 → `frontend/app/print/print.css` (라이트 톤 + 같은 그린)
- `"use client"` — `useLayoutEffect` 측정 필수 (pager.jsx)

---

## 3. persona schema 확장 (spec-01 갱신 필요)

### 3.1 profile.md — skills tiers + education + awards 추가

```yaml
# 기존 stack: [...] 은 단순 표시용 — 유지
skills:
  primary:   { ko: "주력",        en: "Primary",   list: [Python, FastAPI, ...] }
  secondary: { ko: "익숙",        en: "Working",   list: [Next.js, ...] }
  learning:  { ko: "관심·학습 중", en: "Learning",  list: [Kubernetes, ...] }

education:
  - period: "2018.03 — 2024.06"
    degree: { ko: "...", en: "..." }
    org:    { ko: "...", en: "..." }
    loc:    { ko: "서울", en: "Seoul" }
    note:   { ko: "...", en: "..." }

awards:
  - period: "2025.05"
    title: { ko: "...", en: "..." }
    note:  { ko: "...", en: "..." }
```

### 3.2 career/*.md — bullets 추가

```yaml
bullets:
  ko: ["...", "...", "..."]   # 3~4개
  en: ["...", "...", "..."]
```

### 3.3 projects/*.md — 케이스 스터디 구조화

본문 마크다운 (`# 마주친 문제`, `# 회고`) 은 유지하되 print 용 압축본을 frontmatter 에 추가.

```yaml
problem:   { ko: "...", en: "..." }
approach:  { ko: ["...", "..."], en: ["...", "..."] }
impact:    { ko: ["..."], en: ["..."] }
learnings: { ko: ["..."], en: ["..."] }
troubles:
  - when:  "2026.04.18"
    title: { ko: "...", en: "..." }
    cause: { ko: "...", en: "..." }
    fix:   { ko: "...", en: "..." }
```

빈 필드는 print 가 atom 스킵 → pager 가 알아서 페이지 채움.

---

## 4. API 변경 (spec-02 갱신 필요)

### 4.1 옵션 — `?lang=both` 모드 vs 신설 엔드포인트

**채택**: 신설 엔드포인트 — `/api/print/resume`, `/api/print/portfolio`

이유:
- 기존 `/api/me` 등은 사이트용 — 단일 lang 응답 (adr-02)
- print 는 KO+EN + 추가 필드 (skills tiers, education, awards, project 케이스 스터디) 필요 → 응답 형태가 본질적으로 다름
- 분리하면 사이트 API 가 print schema 변경에 영향 안 받음

### 4.2 응답 스키마 (대략)

```json
GET /api/print/resume
{
  "profile":   { ko: {...}, en: {...} },
  "about":     { ko: [...], en: [...] },
  "career":    [{ period, role: {ko, en}, ..., bullets: {ko: [], en: []} }, ...],
  "education": [...],
  "skills":    { primary: {...}, secondary: {...}, learning: {...} },
  "awards":    [...]
}

GET /api/print/portfolio
{
  "profile": { ... },
  "projects": [{ id, code, title, status, period, summary, role, stack, problem, approach, impact, learnings, troubles, ... }, ...]
}
```

---

## 5. 데이터 흐름

```
persona/**/*.md (SoT)
    ↓ persona_loader (back/service/persona_loader.py)
    ↓
back FastAPI (/api/print/resume, /api/print/portfolio)
    ↓ (HTTP)
frontend Next.js (/print/resume, /print/portfolio 라우트)
    ↓ (DOM 렌더 + Pager 측정)
playwright python (back/service/jobs/pdf_generate.py)
    ↓ headless chrome → PDF 출력
frontend/public/{resume,portfolio}.pdf
    ↓ commit_and_push_with_retry (spec-06 §5)
GitHub → Vercel 정적 호스팅
    ↓
footer 다운로드 링크: `/resume.pdf`, `/portfolio.pdf`
```

webhook 트리거 — `persona/**/*.md` push 시 자동 (이미 wired). 수동 스크립트 — `scripts/run_pdf_generate.py` (spec-06 의 `run_content_enrich.py` 와 같은 패턴).

---

## 6. Sprint breakdown

순서:

1. **D — persona schema 확장** (spec-01 갱신 + persona_loader REQUIRED_FIELDS 갱신)
   - profile.md 에 skills/education/awards 추가
   - career/*.md 에 bullets 추가
   - projects/*.md 에 problem/approach/impact/learnings/troubles 추가
   - 검증: 기존 사이트 API (`/api/me` 등) 영향 없음 확인
2. **API — print 엔드포인트 신설** (spec-02 갱신)
   - `back/api/routers/print.py` 신규
   - `lang=both` 응답 형식
3. **Frontend — print 라우트 + 컴포넌트 포팅**
   - `print/*.jsx` (window 전역) → `frontend/components/print/*.tsx` (props)
   - `app/print/resume/page.tsx`, `app/print/portfolio/page.tsx`
   - 브라우저에서 직접 보기 OK 확인
4. **Back job — pdf_generate**
   - `back/service/jobs/pdf_generate.py` (playwright python)
   - 두 라우트 hit → `frontend/public/*.pdf` 떨굼
   - `commit_and_push_with_retry` 재사용
   - `scripts/run_pdf_generate.py` (수동 dev 스크립트)
5. **Webhook 통합** — persona/** push 시 잡 자동 트리거 (기존 webhook 라우터 갱신)
6. **Footer 연결** — `href="#"` → `/resume.pdf`, `/portfolio.pdf`
7. **(선택) ADR** — 새 결정사항 박제: PDF 생성을 back job 으로, KO+EN 합본, /api/print/* 분리 → `adr-NN-print-pdf-generation.md`

---

## 7. 미정·후속 결정

- **playwright python vs node puppeteer** — back 이 python 이므로 playwright python 1순위. 만약 back deps 무거워지면 별도 Docker 서비스 분리 고려.
- **education / awards 실데이터** — 현재 mock 은 SSAFY 우수상 등이 박혀있는데, 실제 과거 (도화/비트캠프/멋쟁이사자처럼/퀀터스/메디솔브) 어떻게 표기할지 본인 판단 필요.
- **project 케이스 스터디 채우기** — 8 프로젝트 모두 problem/approach/impact/learnings/troubles 채우는 건 큰 작업. 단계적으로: live (Wine.Log, open-kknaks) → wip 순서 추천.
- **자동 트리거 vs 수동 only** — 초기는 수동 (`scripts/run_pdf_generate.py`) 으로 검증 후 webhook 연결.
- **PDF 사이즈 / 품질** — A4 portrait (resume) / A4 landscape (portfolio) — 핸드오프 §8 명시.

---

## 8. Out of scope

- 한/영 외 추가 언어
- PDF 인쇄 시점에 LLM enrich (spec-06 의 content enrich 와 별개)
- 별도 어드민 UI 로 PDF 트리거 (수동 + webhook 으로 충분)
- PDF 미리보기 페이지 — `/print/*` 라우트 자체가 미리보기 역할
