---
type: project
id: P-02
title:
  ko: "kknaks.dev"
  en: "kknaks.dev"
summary:
  ko: "본 포트폴리오 사이트 — 페르소나 시스템 (md SoT) + 자동 enrich 잡 (open-kknaks dogfooding)."
  en: "This portfolio — persona system (md SoT) + auto-enrich jobs (open-kknaks dogfooding)."
category: web
status: wip
date: "2026.05"
stack:
  - Next.js
  - FastAPI
  - open-kknaks
  - Docker
  - Redis
links:
  repo: "github.com/kknaks/kknaks_profile"
  live: "https://kknaks.dev"
---

# kknaks.dev — 본 포트폴리오

페르소나 시스템 사상 + 잡 인프라 + 자동 enrich 사이클을 한 사이트에 박음.

- 모든 콘텐츠는 `persona/**/*.md` 가 SoT — DB 없음
- 잔디 잡 + 콘텐츠 enrich 잡 모두 본인 OSS `open-kknaks` 활용 (Anthropic SDK 미사용)
- worker 컨테이너 + Redis broker — claude CLI PTY 패턴
- GitHub webhook → reload + enrich → 자동 사이트 갱신

상세: `medi_docs/current/planning/planning-01-portfolio-overview.md`.
