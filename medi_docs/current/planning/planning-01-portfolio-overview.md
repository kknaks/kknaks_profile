---
id: planning-01
type: planning
title: kknaks.dev 포트폴리오 — 시스템 개요
status: draft
created: 2026-05-01
updated: 2026-05-03
sources: []
tags: [planning, portfolio, persona]
---

# kknaks.dev 포트폴리오 — 시스템 개요

## Summary

1년차 백엔드 엔지니어 이건학(kknaks)의 개인 포트폴리오. 단순 사이트가 아니라 **페르소나 시스템(AI-readable 자기-기록) + 포트폴리오 시스템(외부 표시)** 2-시스템 구조로 설계. 모든 콘텐츠는 md 파일(frontmatter + 본문)이 SoT, DB 없음.

---

## 1. 컨셉 + 톤

- **타겟**: 외부 채용/협업 담당자 + 본인의 학습 기록 보관
- **포지셔닝**: 1년차 백엔드 + AI 회사(Stealth AI Co.) + 홈서버 셀프호스팅 — "엔지니어링 무드"
- **차별 메시지**: 회사 케이스가 적은 1년차 → 매일 쌓이는 학습 노트(Notes/Contents)와 자기-기록 시스템 자체가 작품
- **시각 톤**: 다크 + 모노스페이스. 디자인 v0.5 동결 (`claude_design/` 산출물)
- **언어**: 한/영 토글 (기본 한국어)

---

## 2. 시스템 경계

큰 틀에서 **2개의 시스템**이 한 인터페이스로 연결됨.

```
┌─ 페르소나 시스템 ──────────┐    ┌─ 포트폴리오 시스템 ────────┐
│ 입력 + 가공                 │ →  │ 외부 표시                  │
│ kknaks 본인이 사용           │    │ 사이트 방문자가 사용         │
│   ↑ 사람 편집 (md 직접)     │    │                            │
│   ↓ 기계 쓰기 (LLM 잡 결과) │    │                            │
└─────────────────────────────┘    └────────────────────────────┘
              ↕                                    ↑
              └───── 인터페이스: persona/**/*.md ───┘
                     (md frontmatter + 본문 = SoT)
```

- 두 시스템은 md 파일 형식만 계약으로 공유. 내부 구현은 독립적으로 진화 가능
- 페르소나에 대한 쓰기는 양방향 — 사람이 직접 박는 흐름 + 기계(LLM 잡)가 결과를 commit하는 흐름. 데이터 흐름 디테일은 §3.6
- 페르소나는 포트폴리오 외 다른 활용처도 가능 (이력서 자동 생성, AI 컨텍스트 주입 등 — 본 프로젝트 범위 밖)

---

## 3. 페르소나 시스템

### 3.1 목적

> **"내가 하는 모든 것을 AI가 이해할 수 있도록"**

단순 데이터 입력 공간이 아니라 **AI-readable Self-Documentation Layer**. 본인의 프로젝트·경력·학습·일상 작업을 md로 declarative하게 기록 → 어떤 AI 도구든 이 폴더만 주면 본인을 깊게 이해.

### 3.2 카테고리 (디렉토리 구조 디테일은 spec)

- `profile` — 본인 프로필 (about 입력)
- `career` — 경력 항목별
- `projects` — 프로젝트별
- `notes` — 학습 노트 (옵시디언 스타일 위키링크)
- `contents` — 매일 스터디 영상 + 교안
- `daily` — 일일 작업 로그. **잔디 잡이 자동 작성 (frontmatter `auto: true`)**. 본인이 미리 박은 경우 (`auto: false` 또는 미박음) keep — LLM skip

### 3.3 형식

모든 파일이 **md (frontmatter + 본문)**.

- `frontmatter` — 구조화된 메타데이터 (포트폴리오 시스템이 이걸 파싱해서 표시)
- 본문 — 자유 서술 (AI가 본인을 깊게 이해하는 데 결정적)

데이터성 항목(career, projects)도 yaml 별도 파일이 아니라 md frontmatter에 박음 — yaml 사용 안 함.

### 3.4 가공 (LLM 잡)

스케쥴러가 두 종류의 잡 운영 — 모두 LLM 호출은 `open-kknaks` (ADR-04) 를 통한 Claude Haiku 4.5.

- **잔디 잡** (매일 09:05 KST, spec-03): 어제 데이터 (notes/contents 본문 + GitHub commits) → LLM 이 `persona/daily/{어제}.md` 자동 작성 (frontmatter: counts/summary, 본문: ≤500자 narrative). **`activity.yaml` 폐지** — `/api/activity` 응답은 `daily/*.md` frontmatter 들의 집계 derive (단일 SoT)
- **콘텐츠 enrich 잡** (10분 interval, spec-06, ADR-05): `persona/contents/*.md` 중 `status: pending` 스캔 → yt-dlp 메타 + youtube-transcript-api 자막 + LLM 요약 → frontmatter (title/summary/duration/tags) + 본문 (개념/적용/실수 3-section) 채움 → `status: published` + git commit

> **⚠ Architectural seam**: 스케쥴러가 어느 시스템에 속하는지(포트폴리오 인프라 vs 페르소나 gen 레이어)는 ADR-03에서 정의. 가공 결과의 *서버 → 깃* 쓰기는 §3.6 의 ③/④ 채널.

자세한 잡 명세는 spec-* 에서.

### 3.5 SoT 원칙

**md = 진실의 원천**. 그 외의 모든 표현(API 응답, 사이트 HTML, 메모리 dict)은 파생물. md 변경 → git push → 자동 재로드.

### 3.6 데이터 흐름 — 4채널 사이클 (양방향)

페르소나 SoT(`persona/**/*.md`)는 사람과 기계 둘 다 쓰는 공유 자원이라, 변경 채널이 4개로 나뉘고 한 사이클로 닫힘.

```
                            ┌─────────────────────┐
                            │   GitHub (origin)   │
                            └──┬──────────────┬───┘
        로컬 → 서버           │              │           서버 → 깃
        (사람 편집)           ↓              ↑           (기계 쓰기)
   ┌──────────────────────────┤              ├──────────────────────────┐
   │ ① 코드 변경              │              │ ③ 잔디 잡 산출물          │
   │   GitHub Actions         │              │   daily/{date}.md        │
   │   → SSH → git pull       │              │   (auto: true frontmatter│
   │   → docker rebuild       │              │    + ≤500자 narrative)   │
   │   → curl admin/reload    │              │   → git commit + push    │
   │                          │              │                          │
   │ ② 콘텐츠 변경 (md)        │              │ ④ 콘텐츠 enrich 결과     │
   │   GitHub webhook         │              │   md frontmatter + 본문  │
   │   → admin/reload         │              │   → git commit + push    │
   │   → git pull             │              │                          │
   │   → LLM 잡 트리거        │              │   (충돌 회피:            │
   │                          │              │    fetch+rebase+retry,   │
   │                          │              │    git_push.py)          │
   └──────────────────────────┤              ├──────────────────────────┘
                              ↓              ↑
                            ┌─────────────────────┐
                            │  홈서버 백엔드       │
                            │  (back + worker)    │
                            └─────────────────────┘
```

- **① 코드 vs ② 콘텐츠 분리**: 코드는 빌드/이미지 재기동이 필요해 Actions+SSH로 가고, 콘텐츠는 빌드 불필요 → webhook 핸들러가 직접 git pull + LLM 잡 트리거. webhook의 본질이 "콘텐츠 변경 → LLM 돌려라"라 pull은 그 전제조건일 뿐
- **③/④ 서버 → 깃**: LLM 잡이 가공한 결과가 다시 SoT로 박혀야 다음 부팅 때 메모리에 로드됨. `git_push.py` 가 잔디·콘텐츠 공통으로 처리 (paths + message 일반화)
- **사이클 닫힘**: ③/④의 push 가 다시 ②의 webhook 을 발화시킬 수 있음 (콘텐츠 enrich가 자기 자신을 트리거하지 않도록 commit author 또는 path 필터로 차단 — 운영 디테일은 spec-03/spec-06)

### 3.7 자동 인덱스 — `persona/_map.md`

페르소나 폴더에 자동 생성 인덱스(`_map.md`)를 둠. 카테고리별 카운트·파일 리스트(위키링크)·notes 그래프·백링크를 한 페이지에 박아 옵시디언 vault로 페르소나 폴더를 열 때 진입점 역할. 빌드는 git pre-commit hook + 백엔드 부팅 시 둘 다 실행 (멱등). 디테일은 spec-04.

---

## 4. 포트폴리오 시스템

### 4.1 목적

페르소나의 일부를 **외부 방문자가 볼 수 있는 형태**로 표시.

### 4.2 5섹션 구성

| 섹션 | 페르소나 소스 | 비고 |
|---|---|---|
| About | `persona/profile.md` | Hero + 소개 카드 + 활동 잔디 |
| Career | `persona/career/*.md` | 시간순 |
| Projects | `persona/projects/*.md` | 카테고리 필터 |
| Notes | `persona/notes/*.md` | 옵시디언 스타일 포스 그래프 + 위키링크 |
| Contents | `persona/contents/*.md` | 매일 영상 + 교안 |

(Products 섹션은 의도적으로 없음 — 1년차라 회사 케이스보다 학습 노트가 차별점)

### 4.3 데이터 흐름

```
persona/**/*.md  ─→  FastAPI 부팅 시 메모리 dict 로드
                          ↓
                     /api/* (?lang= 분기 응답)
                          ↓
                     Next.js 프론트 fetch
```

### 4.4 i18n

A안 — 슬롯은 단일 키, 백엔드가 `?lang=ko` / `?lang=en` 쿼리로 분기. 디테일은 ADR-02.

### 4.5 차별점 표현 (사이트 위)

- **Notes 옵시디언 그래프** — force-directed 그래프 + 위키링크 본문 패널
- **Contents 매일 업로드** — 스터디 영상 + 교안 (개념/적용 2단)
- **활동 잔디** — git 커밋 + notes/contents 변경 다채널 집계, AI가 일일 종합 요약

---

## 5. 차별점 (전체)

1. **페르소나-드리븐 사상** — md SoT, 자기 자신을 declarative하게 관리. 1년차에 "시스템 자체가 작품"
2. **Notes 옵시디언 그래프** — 학습 노트를 시각적으로 연결, 위키링크 탐색
3. **Contents 매일 업로드** — 학습 지속성을 시각화
4. **AI 종합 잔디** — GitHub 잔디와 다른, LLM이 일일 활동을 종합 요약하는 커스텀 잔디
5. **셀프호스팅** — 본인 홈서버 운영. 인프라 자체가 작품
6. **OSS dogfooding** — LLM 호출은 본인 OSS 라이브러리 [`open-kknaks`](https://pypi.org/project/open-kknaks/) 사용. "내가 만든 도구로 내 사이트가 돌아간다" — 매일 1회 활동 가공이 본인 라이브러리의 production 사용 사례. ADR-04

---

## 6. 비기능 요구

- **호스팅**: 백엔드 = 본인 홈서버 docker compose (back + redis + worker, NPM = Nginx Proxy Manager 가 SSL/리버스 프록시) / 프론트 = Vercel. 도메인은 백 `profile-api.kknaks.cloud`, 프론트 `profile.kknaks.cloud`. 두 시스템은 같은 SoT(`persona/**/*.md`)를 git 으로만 공유 — 프론트는 백 API만 호출, 페르소나 직접 접근 X
- **콘텐츠 SoT**: md 기본 (frontmatter + 본문). 데이터-only yaml 은 사람이 박는 메타 정의 (`persona/_meta.yaml`) 만. 잡 자동 산출물도 md 로 박음 (잔디 잡 → `persona/daily/{date}.md`, 콘텐츠 enrich → `persona/contents/*.md` 갱신)
- **모노레포 구조**: `persona/` (md SoT — 백엔드의 "DB" 역할) + `back/` (FastAPI) + `frontend/` (Next.js). 통합 디렉토리 트리 SoT는 spec-05
- **DB**: 사용 안 함. 부팅 시 md 메모리 로드. 향후 데이터 만 단위 넘으면 sqlite부터 incremental
- **i18n**: A안 — md frontmatter `{ko, en}` 객체로 양쪽 보관. 백엔드가 `?lang=` 분기해서 응답
- **디자인**: v0.5 동결. 변경 의도 없으면 .jsx/.html 수정 X
- **secret**: env var (`GH_TOKEN`, `REDIS_URL`, `RELOAD_TOKEN` — ADR-04로 ANTHROPIC_API_KEY 불요), `.env`는 `.gitignore`, 운영은 systemd EnvironmentFile + docker-compose env

---

## 7. Out of Scope (이 프로젝트엔 없음)

- 비즈니스 도메인 정책 (예약/결제/시술 등) — `policy/` 폴더 비워둠
- 다인 admin / 권한 관리 — 1인 운영
- 동적 백엔드 기능 (방문자 카운트, 댓글, 좋아요) — 정적 표시만
- 페르소나의 비-포트폴리오 활용 (이력서 자동 생성, 외부 AI 컨텍스트 주입 등) — 같은 SoT에서 파생 가능하지만 별도 프로젝트
- Products 섹션 — 1년차 컨텍스트상 의도적 제외

---

## 다음 단계 (이 planning에서 파생할 문서)

- **ADR-01** — DB 사용 안 함 결정 근거 (대안 비교 + 트리거 조건)
- **ADR-02** — i18n A안 결정 근거 (대안 비교)
- **ADR-03** — AI 잡 위치 (백엔드 내장 vs Actions cron) 결정 근거
- **spec-01** — 페르소나 md 형식 명세 (frontmatter 스키마, 디렉토리 구조)
- **spec-02** — API 엔드포인트 명세 (`claude_design/SLOTS.md` 흡수)
- **spec-03** — 잔디 잡 명세 (notes/contents 본문 + GitHub commits → daily.md 자동 작성; `activity.yaml` 폐지)
- **plan-01** — v1.0-pre 마일스톤 (페르소나 시드 → 백엔드 스켈레톤 → 프론트 fetch → 데이터 주입)
