---
id: adr-05
type: adr
title: 콘텐츠 = pending stub + 백엔드 enrich 잡 (수동 작성 금지)
status: accepted
created: 2026-05-02
updated: 2026-05-02
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[adr-04-llm-via-open-kknaks]]"
  - "[[spec-03-activity-scheduler]]"
tags: [adr, content, llm, open-kknaks, scheduler]
---

# 콘텐츠 = pending stub + 백엔드 enrich 잡 — 수동 작성 금지

## Summary

`persona/contents/*.md` 의 작성 모델을 **사용자 수동 작성 → 백엔드 자동 enrich** 로 변경. 사용자는 `youtubeId` + `status: pending` 만 박은 stub 을 push, 백엔드 스케줄러 잡이 yt-dlp 메타 + youtube-transcript-api 자막 + open-kknaks LLM 요약으로 frontmatter + 본문을 채워 `status: published` 로 commit·push 한다.

---

## 1. Context

- `planning-01` §3.2 contents — "매일 스터디 영상 + 교안" 이 차별점 (§4.5 / §5.3). 매일 누적이 핵심.
- 현 `spec-01` §3.5 명세 — 사용자가 모든 frontmatter (title/summary/duration/tags/youtubeId) + 본문 (개념/적용/실수 등) 을 직접 작성.
- 매일 영상마다 frontmatter 채우고 교안 본문 박는 마찰이 큼 → 학습 지속성 차별점인데 입력 마찰이 크면 누락 위험.
- `adr-04` 결정 후 LLM 인프라 (open-kknaks worker + Redis broker) 가 이미 떠있음. 추가 인프라 없이 잡 1개만 더 박으면 됨.
- yt-dlp / youtube-transcript-api 모두 API key 불요 — 외부 시크릿 추가 부담 0.

---

## 2. Decision

### 2.1 작성 흐름

```
사용자 → persona/contents/C-NNN-slug.md 작성
         frontmatter 최소: { id, type: content, youtubeId, status: pending }
         본문: 비워둠
         git push
   ↓
백엔드 스케줄러 주기 폴링 → status: pending MD 발견
   ↓
content enrich 잡 실행:
   ① yt-dlp           → 메타 (title/description/duration/channel/tags/thumbnail)
   ② youtube-transcript-api → 자막 (없으면 설명/태그 fallback)
   ③ open-kknaks       → LLM 요약 (ko/en title·summary, 본문 초안, kind 분류)
   ④ MD 갱신           → frontmatter 보강 + 본문 채움 + status: published
   ⑤ git commit + push → 메모리 reload → 사이트 표시
```

### 2.2 주요 설계 결정

- **입력 SoT** = 사용자가 박은 pending stub. enriched MD 도 git 에 commit (재현성 + 사이트 빌드 단순화 — `planning-01` §3.5 SoT 원칙 그대로 유지).
- **라이브러리** — yt-dlp (메타) + youtube-transcript-api (자막) + open-kknaks (LLM). 모두 API key 0 → 외부 시크릿 추가 없음.
- **트리거** — 별도 endpoint X. APScheduler interval polling (잔디 잡과 동일 패턴, `adr-03` 정합).
- **실패 처리** — `status: error` + `error_reason` frontmatter. 다음 tick 자동 재시도 X. 사용자가 수동으로 `status: pending` 으로 되돌리면 재처리.
- **사용자 검토 흐름** — 잡이 published 박은 후 사용자가 본인 검토 → 직접 수정해서 push. status 가 published 면 잡이 다시 덮어쓰지 않음 (멱등).

상세 잡 명세는 `spec-06`.

---

## 3. Alternatives Considered

### 3.1 수동 작성 (현 `spec-01` 명세)
- **장점**: 단순. 인프라 0 추가
- **단점**: 매일 영상마다 frontmatter + 본문 작성 마찰 큼 → 학습 지속성 차별점 약화
- **기각 이유**: 차별점 (`planning-01` §5.3) 자체가 마찰로 무너지면 의미 없음

### 3.2 로컬 skill (`/content-enrich`)
- **장점**: 서버 인프라 0 추가, push 전 완성
- **단점**: "링크만 던지면 끝" UX 못 만듦 — 매번 수동 실행 필요. open-kknaks LLM 호출하려면 어차피 worker 필요. UX 와 인프라 둘 다 손해
- **기각 이유**: 기존 worker 인프라 재사용 못 하면서 UX 도 떨어짐

### 3.3 GitHub Action
- **장점**: 서버 부담 0
- **단점**: `CLAUDE_CODE_OAUTH_TOKEN` 시크릿을 Action 에 박는 보안 부담. open-kknaks worker 를 Actions 환경에 띄워야 함. 두 번 빌드 비용. dogfooding 패턴 (`adr-04` §4.6) 분리됨
- **기각 이유**: dogfooding 정합성 깨지고 시크릿 관리 부담

### 3.4 (현 결정) 백엔드 스케줄러 + open-kknaks 잡
- **장점**: 기존 worker + Redis 인프라 재사용, dogfooding 강화, "링크만 push" UX, API key 추가 0
- **단점**: 잡 1개 추가 — 단순한 폴링 패턴
- **수용 가능한 이유**: 비용 = 잡 1개. 반대로 차별점·UX·OSS dogfooding = 매우 큼

---

## 4. Consequences

### 4.1 즉시 효과

- `back/pyproject.toml` — `yt-dlp`, `youtube-transcript-api` 추가
- `back/service/jobs/` — `content_enrich.py` 신규 (또는 `main_job.py` 확장)
- `spec-01` §3.5 contents frontmatter 재정의 필요 — 사용자 입력 (필수) vs 잡 출력 (잡이 채움) 분리 + `status` enum 추가
- `spec-06` 신규 — 잡 명세 (입력 스캔 / 처리 단계 / 출력 / 트리거 / 본문 템플릿)

### 4.2 운영 영향

- **사용자 흐름** — `persona/contents/C-NNN-slug.md` 작성 시 `youtubeId` 만 박고 push → 다음 tick (~분 단위) 안에 enriched MD 가 자동 commit 되어 사이트 표시
- **자막 없는 영상** — 본문 품질 저하 (메타+설명만 기반). 향후 fallback 로직 강화 가능
- **LLM 출력 품질** — Pro/Max rate limit 안에서 매일 1~3개 영상 가공 → 비용 0, 품질 충분 (`adr-04` 가정 그대로)

### 4.3 위험 + 완화

| 위험 | 완화 |
|---|---|
| YouTube 자막 차단/없음 | 메타+설명 fallback. `status: published` + frontmatter `transcript: false` 로 표시 (선택적) |
| yt-dlp 봇 감지로 메타 추출 차단 | 거의 발생 X (개인 잡 트래픽). 발생 시 status: error 후 수동 재시도 |
| LLM 할루시네이션 (사실과 다른 본문) | 사용자 검토 흐름 — published 후 본문 수정해서 push. 잡이 published 면 다시 덮어쓰지 않음 (멱등) |
| 잡 무한 폴링 부하 | 폴링 주기 5~15분, pending MD 없으면 즉시 종료 |
| 잡 도중 git commit 충돌 | 사용자가 동시 편집 가능성 낮음 (1인). 충돌 시 잡 실패 → 다음 tick 재시도 안전 |

### 4.4 향후 확장

같은 패턴으로 다른 enrich 잡 추가 가능:
- notes 자동 태깅 (frontmatter `tags` 비어있으면 본문 기반 LLM 태깅)
- 프로젝트 README → `persona/projects/*.md` 요약
- weekly digest

→ Redis broker 1개로 다중 잡 운영. dogfooding 사용 사례가 풍부해짐 (`adr-04` §4.5 정합).

### 4.5 SoT 원칙 정합

`planning-01` §3.5 "md = 진실의 원천" 원칙은 그대로 유지된다:
- 사용자가 박은 pending stub 도 md, 잡이 enrich 한 결과도 md → 둘 다 git 에 commit
- 잡이 박은 frontmatter/본문은 *derived* 지만 git history 로 추적 가능 → 재생성 가능
- 즉 SoT 가 한 단계 layered 되었을 뿐, 단일 SoT 형식 (md) 은 동일
