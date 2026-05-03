---
id: adr-07
type: adr
title: 이력서·포트폴리오 PDF = back job (playwright python) + KO/EN 합본 + /api/print/* 분리
status: accepted
created: 2026-05-03
updated: 2026-05-03
sources:
  - "[[planning-02-print-pdf]]"
  - "[[adr-02-i18n-strategy]]"
  - "[[adr-05-content-pending-enrich]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-02-api-endpoints]]"
tags: [adr, print, pdf, playwright]
---

# 이력서·포트폴리오 PDF = back job (playwright python) + KO/EN 합본 + /api/print/* 분리

## Summary

PDF 생성을 **back job (playwright python, chromium headless)** 으로 통일하고, 출력은 `frontend/public/{resume,portfolio}.pdf` 에 commit·push (Vercel 정적 호스팅). 합본 정책은 **한 PDF 안에 KO + EN 모두**, API 는 사이트 (`/api/me` 등 i18n 단일 응답) 와 분리해 **`/api/print/*` 신설** (raw `{ko, en}` 응답).

---

## 1. Context

- `planning-02` 가 결정 4개 (생성 위치 / 출력 위치 / 합본 정책 / 라우트 구조) 를 명시했지만 ADR 로 잠그지 않은 상태.
- adr-05 가 "콘텐츠 자동 enrich" 패턴 (`back/service/jobs/content_enrich.py` + `commit_and_push_with_retry`) 박아둠 — 같은 패턴 재사용 가능.
- adr-02 의 i18n 정책 ("`?lang=ko|en` 단일 응답") 은 사이트 기준 — print 합본에는 부적합.
- 외부 채용 담당자가 PDF 1개 받으면 한·영 모두 확인 가능해야 함 (recruiter UX).
- back 은 Python — Node puppeteer 보다 **playwright python** 이 stack 일치.

---

## 2. Decision

### 2.1 생성 위치 — back job (playwright python)

```
back/service/jobs/pdf_generate.py  (adr-05 의 content_enrich 와 동일 패턴)
  → playwright async chromium 실행
  → frontend `/print/*` 라우트 hit
  → page.pdf() 로 frontend/public/*.pdf 출력
  → commit_and_push_with_retry (idempotent — diff 없으면 skip)
```

**대안 비교**:

| 옵션 | 채택? | 이유 |
|---|---|---|
| Vercel build + puppeteer (Node) | X | chromium 바이너리 size + Vercel 빌드 시간 + Node 의존 추가 |
| **back job + playwright python** ✓ | ✓ | stack 일치, jobs 인프라 재사용, webhook 자동화 자연스러움 |
| 브라우저 print-to-PDF 버튼 | X | pager 측정 일관성 X, 자동화 X, recruiter 가 직접 변환해야 함 |

### 2.2 출력 위치 — `frontend/public/{resume,portfolio}.pdf` 커밋

- 잡이 PDF 생성 후 `commit_and_push_with_retry` 로 자동 push → Vercel 정적 호스팅 → footer 다운로드 링크 (`/resume.pdf`, `/portfolio.pdf`).
- 대안 (백엔드 정적 서빙) 거부 — CORS, base URL 분리, 추가 라우터 필요.
- 운영 SoT 일관: 사이트 콘텐츠 (persona/**) 는 git, 자동 생성물 (PDF) 도 git — 외부 의존 없음.

### 2.3 합본 정책 — KO + EN 한 PDF 안에

- `kknaks-resume.pdf` = KO 페이지들 + EN 페이지들 (한 문서).
- `kknaks-portfolio.pdf` = KO cover + KO 프로젝트 + EN cover + EN 프로젝트.
- adr-02 의 단일 lang 응답 정책 예외 — print 만 raw `{ko, en}` 응답.

### 2.4 라우트 + API 분리

```
frontend/app/print/
  resume/page.tsx       # 서버 컴포넌트 — fetch /api/print/resume → <PrintResume>
  portfolio/page.tsx    # 서버 컴포넌트 — fetch /api/print/portfolio → <PrintPortfolio>

frontend/components/print/
  pager.tsx, sheet.tsx  # claude_design/print/*.jsx 포팅 (window 전역 → props)
  resume.tsx            # KO + EN 두 Pager + sentinel [data-print-ready]
  portfolio.tsx         # cover sheet + KO/EN 두 Pager + sentinel
```

API:
- `GET /api/print/resume` — `profile, about, skills, career[], education[], awards[]` (raw `{ko,en}`).
- `GET /api/print/portfolio` — `profile, projects[]` (visible:true 만, raw).
- 사이트 API (`/api/me`, `/api/career`, `/api/projects`) 와 응답 스키마·언어 정책 모두 다름 → 분리 유지가 schema 변경 격리에 유리.

### 2.5 webhook 통합

`back/api/admin/reload.py` 의 push handler 가 `_run_enrich_safe` 와 함께 `_run_pdf_safe` 를 background task 로 큐잉 — 사용자 push → webhook → 자동 PDF 갱신.

idempotency: `commit_and_push_with_retry` 가 diff 없으면 skip (loop 차단).

---

## 3. Consequences

### 3.1 좋아진 점

- 디자인 시안 (`claude_design/.../print/*.jsx`) 의 Pager (자동 페이지 분할) 그대로 활용 — 측정 로직이 jsdom 에서 안 도므로 headless chrome 필수, 이 결정이 그것을 보장.
- persona md 만 채우면 PDF 자동 갱신 — recruiter 가 받는 PDF 가 항상 최신.
- 사이트 API 와 분리 → print schema 변경이 사이트에 영향 없음.

### 3.2 비용·트레이드오프

- back container 에 chromium 바이너리 (~250MB) + system deps 추가 → 이미지 크기 증가. `Dockerfile.back` 에 `playwright install --with-deps chromium` 박음.
- prod 에서 back (홈서버) 이 frontend (Vercel) 를 hit → Vercel 배포 race condition 가능 (아직 빌드 중인 라우트 hit 시 outdated PDF). 운영 관찰 후 필요시 Vercel deploy webhook 으로 동기화.
- PDF 출력 시점에 chromium 의 timestamp 가 달라 byte 가 매번 변할 가능성 — 관찰 후 필요시 metadata 픽싱 옵션 추가 고려.

### 3.3 후속 결정 후보 (현재 sprint 외)

- Vercel deploy 완료 webhook 수신 → 그 후 PDF 잡 — race 해결.
- Cron 으로 정기 PDF 재생성 — webhook 누락 시 backstop.
- PDF 캐시 / hash 기반 skip — playwright 재실행 비용 절감.

---

## 4. Out of scope

- 한·영 외 언어 합본
- PDF 미리보기 페이지 — `/print/*` 라우트 자체가 미리보기 역할
- 별도 어드민 UI (수동 + webhook 충분)
