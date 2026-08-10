---
type: decision
id: KDEV-DEC-015
title: "잔디 착지 경로 3개와 문서 양식 — daily·career·concept"
status: proposed
product: kknaks-dev
created_at: 2026-07-31
updated_at: 2026-07-31
tags:
  - product/kknaks-dev
  - doc/decision
  - status/proposed
links:
  baselines:
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
  decisions:
    - "[[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]]"
    - "[[decision-016-grass-gate-and-publish|KDEV-DEC-016]]"
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works: []
  releases: []
  related:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
up: []
---

# 잔디 착지 경로 3개와 문서 양식 — daily·career·concept (ADR-015)

커밋 조사 결과는 **`persona/daily/`(그날) · `persona/career/`(누적) · `permanent/concept/`(개념)** 세 곳으로 간다. area 층을 새로 만들지 않고 **기존 career 문서를 갱신**한다.

> 조사 원천은 [[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]], 승인·발행 절차는 [[decision-016-grass-gate-and-publish|KDEV-DEC-016]] 이 다룬다.

## Context

- 관련 baseline: [[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]
- **daily body 는 아무도 읽지 않고 career body 는 렌더된다.** 이 비대칭이 목적지 설계를 갈랐다.

  | | 노출 경로 | body |
  |---|---|---|
  | `persona/daily/*.md` | `_derive_activity()`(`persona_loader.py:423-430`) → `/api/activity` → `contrib-grass.tsx` | **미노출.** `counts`·`summary[]` 만 추출 |
  | `persona/career/*.md` | `/api/career`(`career.py:37`) → `career-timeline.tsx:127-246` | **`ReactMarkdown` 렌더** |
  | `career.bullets` | `print.py:56` → `resume.tsx:518` | PDF 이력서 전용 |

- **daily 가 누적되지 않는다.** 89건(`2026-05-01`~`2026-07-28`, 88건 `auto:true`)이 쌓여 있으나 `_derive_activity` 가 rolling 365일로 자른다(`persona_loader.py:414`). 창을 벗어나면 사이트에서 사라지고 어디로도 흐르지 않는다.
- **career 본문이 비어 있다.** `## 무슨 일 하는지`·`## 챌린지`·`## 배운 점` 3섹션이 전부 `(TBD — 사용자 채움)` 이다. 사이트에 렌더되는 자리다.
- **career 형식 SoT 가 없다.** `persona_loader.py:68 REQUIRED_FIELDS["career"]` 가 필수 frontmatter 만 알고 본문 구조를 정의한 문서가 없다.
- **daily 형식 SoT 는 흩어져 있다.** 섹션은 `llm.py:100-119` 프롬프트, frontmatter 는 `upsert.py:46-51`, 소비 필드는 `_derive_activity`. `derived.py:5-8` 이 교안에서 없앤 이중 SoT 가 잔디에 남아 있다.
- **career 는 조직 단위다.** 5개 — `medisolve-ai`(`is_current: true`) · `quantus` · `likelion` · `dowha-eng` · `bitcamp`. 반면 `showcase.md` 의 `org` 분포는 `company` 5 / `studio` 8 이다.
- **길이 상한.** `llm.py:21 BODY_HARD_LIMIT = 600`, 프롬프트는 `≤500자`.
- **그래프는 이번 범위 밖이다.** owner 결정 — 그래프 정합은 이 파이프라인을 구축한 뒤 별도로 손본다.

## 근거 개념

없음 — 산출물이 어느 경로로 가는지 정한 배치 표다.

## Options

### area 성격의 누적을 어디에 둘 것인가

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | `persona/areas/` 신설 | PARA 의 area 에 대응, 그래프 밖이라 규율 충돌 없음 | 새 `type`·로더 분기·API·프론트 페이지가 전부 딸려온다 |
| B | `permanent/` 재사용 | 4층 모델 안, 수명 특성 동일 | `up:` 필수 + "개념에서 자란다" 계보 규율과 충돌 — 활동은 커밋에서 자란다 |
| **C** | **`persona/career/` 갱신** | **새 층 0.** 이미 로더·API·프론트가 다 있고, 채울 자리(`(TBD)`)가 비어 있다 | career 는 조직 단위라 studio 를 담을 자리가 없다 |

### studio(개인) 커밋의 누적처

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | `career/studio.md` 신설 | 매핑이 완전해진다 | **다닌 적 없는 회사를 만드는 것.** 이력서 문서에 허구가 들어간다 |
| **B** | **career 갱신 없음** | 이력 정합 유지 | 개인 작업의 누적 서술이 남지 않는다(daily·concept 로만) |

## Decision

### D1. 착지 경로는 셋이다

| 경로 | `type` | 액션 | 조건 | 갱신 범위 |
|---|---|---|---|---|
| `persona/daily/{YYYY-MM-DD}.md` | `daily` | upsert | 활동 > 0 · 기존 `auto:false` 아님 | 파일 전체 |
| `persona/career/{stem}.md` | `career` | replace | `type=company` 커밋 있음 · `is_current: true` · `changed: true` | 본문 섹션 + `stack` |
| `permanent/concept/{slug}.md` | `concept` | upsert | 개념 후보 + 승인 | 신규 or 보충 |

셋 다 **일간**이다. 별도 주기의 롤업 파이프라인을 두지 않는다.

### D2. `persona/areas/` 를 신설하지 않는다 — career 가 그 자리다

area 성격(지속되는 책임 영역, 누적 갱신)은 career 가 이미 갖고 있다. 새 층을 만들면 `REQUIRED_FIELDS`·로더 분기·API·프론트 페이지가 전부 딸려오는데, 그 대가로 얻는 것이 **이미 있는 문서의 빈 섹션**과 같다.

`permanent/` 재사용도 기각한다. `up:` 필수와 "개념에서 자란다" 계보 규율(`knowledge-note-pipeline.md:82`, `plan.py:213-219` 가 검증)이 걸리는데 활동 누적은 개념에서 자라지 않는다 — `up:` 을 채울 방법이 억지가 된다.

### D3. career 갱신 범위

**갱신한다**

- `## 무슨 일 하는지` — 담당 제품·서비스 1단락 + products 링크
- `## 담당 영역` — **신설**(D6)
- `## 챌린지` — 마주친 문제
- `## 배운 점`
- `## 대표 작업` — work 문서 링크(문서 자체는 갱신하지 않는다). **`[[work-016-async-execution-and-progress-ui|KDEV-WORK-016]]` 형태의 위키링크로 건다** (OQ-1 해소) — career 는 `_build_graph_nodes(notes, products_dir, permanent_list)` 에 들어가지 않아 **L1 dead link 검증 대상이 아니고**, Obsidian 에서는 그대로 탐색된다. 그래프 재정비를 기다릴 이유가 없다.
- `stack` — 새로 쓴 기술이 있을 때만. **판정은 의존성 파일 변경 감지가 먼저다** (OQ-2 해소) — `pyproject.toml`·`package.json`·`requirements.txt`·`go.mod` 등이 그날 diff 에 있을 때만 후보로 올리고, 거기서 추가된 패키지명을 LLM 이 읽는다. 순수 LLM 판단은 "이번에 Redis 를 썼나" 가 날마다 흔들린다.

**건드리지 않는다**

- `bullets` — 이력서 PDF 에 나가는 문장이다. `content.md:68-76` 이 `id`·`day` 를 격리한 방식으로 "AI 가 정하지 않는다" 에 명시한다.
- `period` · `is_current` · `display_order` · `title` · `org` · `summary` · `location` — 사람만.

`is_current: true` 인 career 만 갱신 대상이다. 끝난 재직 기간의 문서를 지금 커밋으로 고치는 것은 이력을 왜곡한다.

### D4. `type=company` 인 레포만 career 로 간다

[[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]] D2 의 레지스트리 행이 판정한다.

```text
type=company + detail=medisolve-ai  →  persona/career/medisolve-ai.md 갱신
type=studio                          →  career 갱신 없음 (daily·concept 만)
```

`career/studio.md` 는 만들지 않는다. **다닌 적 없는 조직을 이력에 넣지 않는다.** 개인 작업의 누적 서술이 남지 않는 것은 감수한다 — 그 자리는 `products/*/showcase.md` 가 맞고, 그건 이번 범위 밖이다(D8 기각 항목).

### D5. career 는 append 하지 않는다 — 압축·재서술 + 상한

새 줄을 더하는 것이 아니라 **기존 줄을 더 정확하게 만든다.**

```text
기존:  - 승인 게이트 구축 중 상태 관리 문제
+오늘: 비동기 실행으로 전환, 제출/수확 분리
─────────────────────────────────────────
갱신:  - AI 산출물 승인 파이프라인 — 실행이 요청 수명을 넘는 문제를
         제출·수확 분리로 해결 (게이트/버전/실행 상태 3분리)
```

- append 하면 `daily/*.md` 의 복사본이 되어 `knowledge-note-pipeline.md:167-169`("같은 사실은 한 곳에만")를 위반한다.
- 상한은 **섹션당 5~7줄**. 넘으면 합치거나 뺀다. 1년 append 하면 챌린지가 200줄이 되는데 이력서 문서다.
- 이 규칙은 `templates/persona/career.md` 가 소유한다(D7).

### D6. `## 담당 영역` 섹션을 신설한다

`path_rules`(DEC-014 D2)로 분해한 기술 영역을 서술로 적는다.

```text
## 담당 영역
백엔드(FastAPI·Postgres)가 중심이고, 배포·인프라와 프론트를 함께 본다.
```

**숫자를 쓰지 않는다.** 커밋 수·라인 수는 이력서에 들어갈 값이 아니다. `path_rules` 는 서술의 근거일 뿐이고, 이 섹션이 그 컬럼의 유일한 소비처다.

### D7. 형식 SoT 를 `templates/` 로 모은다

| 파일 | Action | 비고 |
|---|---|---|
| `templates/persona/daily.md` | create | 지금 `llm.py:100-119` + `upsert.py:46-51` 이중 SoT |
| `templates/persona/career.md` | create | 지금 SoT 없음. D3·D5·D6 규칙을 소유 |
| `templates/knowledge/concept.md` | **재사용** | 이미 SoT. 새로 만들지 않는다 |
| `agent.md` | update | "별도 계열" 에 daily·career 등록 |

`route.py:118-121` 이 이미 확립한 방식을 따른다 — **프롬프트에 규칙을 복사하지 않고 레포에서 읽힌다.** 복사하는 순간 SoT 가 둘이 되고 한쪽만 고쳐지는 날 조용히 어긋난다.

`agent.md:76-79` 의 "별도 계열 둘" 이 셋 이상이 된다. 교안이 *"승인 게이트의 `derived` 스테이지와 `content_enrich` 잡이 둘 다 이 파일을 읽는다 — 형식을 고치려면 여기만 고친다"* 로 쓴 규약을 daily·career 에도 그대로 적용한다.

### D8. daily body 를 유지하고 길이 상한을 올린다

사이트에 노출되지 않지만 두 군데서 쓰인다 — **career·concept 스테이지의 입력**, 그리고 git 이력(나중 회고·permanent 재료). 없애면 그날의 서술이 `summary[]` 몇 줄로만 남는다.

`BODY_HARD_LIMIT` 을 **600 → 1500** 으로, 프롬프트 지시를 **500자 → 1200자** 로 올린다. career 입력으로 쓸 것이면 지금 길이로는 재료가 되지 않는다.

### 기각

- **`persona/areas/` 신설** — career 가 그 자리다(D2).
- **`permanent/` 재사용** — `up:` 계보 규율과 충돌(D2).
- **`career/studio.md`** — 허구 이력(D4).
- **`bullets` 자동 갱신** — 이력서 PDF 문장(D3).
- **`products/*/30-work/*.md` 갱신** — owner 결정. 커밋 메시지의 `WORK-NNN` 매칭은 `collect` 이 계산하되 `## 대표 작업` 링크에만 쓴다.
- **`products/*/showcase.md`·`persona/posts/*.md`** — 수동 트리거(casestudy) 파이프라인과 함께 이번 범위 밖.
- **`inbox/` idea** — 잔디에서 idea 로 갈 일이 없다.
- **주간·월간 롤업 파이프라인** — career 도 일간으로 돌린다. "매일 갱신하되 대개 변경 없음" 이 정상이고, 그 처리는 [[decision-016-grass-gate-and-publish|KDEV-DEC-016]] D5 가 계약한다.

## Rationale

- **판단 기준** — 어느 문서가 실제로 읽히는가. daily body 는 미노출이고 career body 는 렌더된다는 실측이 "무엇을 자세히 쓸 가치가 있는가" 를 정했다.
- **대안 대비** — `persona/areas/` 는 개념적으로 깔끔하지만 새 `type` 하나가 로더·검증·API·프론트로 번진다. career 는 그 전부가 이미 있고 채울 자리만 비어 있다. **없는 것을 만드는 것보다 비어 있는 것을 채우는 편이 싸다.**
- **리스크**
  - career 는 이력서다. AI 서술이 사실과 어긋나면 대외 문서가 틀린다 → 게이트에서 문장 단위 승인(DEC-016 D6).
  - `type=studio` 커밋의 누적이 남지 않는다 → showcase 케이스 스터디로 후속.
  - daily body 상한을 올리면 토큰이 는다 → DEC-014 D7 의 입력 상한이 앞에서 막는다.
  - 그래프 정합을 이번에 안 본다 → `permanent/concept/` 산출물이 L1~L6 에 걸릴 수 있다. DEC-016 D6 이 daily·career 를 그래프 검증에서 제외하되 concept 는 기존 규율을 그대로 받는다.

## Scope

- **In** — 목적지 3개와 각 갱신 범위, career 섹션 구조(`## 담당 영역` 신설 포함)와 압축·상한 규칙, `templates/persona/daily.md`·`career.md` 신규, `agent.md` 등록, `BODY_HARD_LIMIT` 상향.
- **Out** — 조사 원천(DEC-014), 게이트·발행부(DEC-016), showcase 케이스 스터디·`persona/posts/`, 그래프 재정비.
- **영향을 받는 spec 후보** — `KDEV-SPEC-001`(디렉토리 계약에 daily·career 갱신 주체 추가), 신규 spec(잔디 산출물 계약).

## Open Questions

**둘 다 spec 을 막지 않는다.**

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-3 | daily body 1200자가 career 입력으로 충분한지 | kknaks | 운영 후 조정 |
| OQ-4 | `type=studio` 누적처(showcase 케이스 스터디) 착수 시점 | kknaks | 후속 baseline |

### 해소됨

| ID | Question | 결론 |
|---|---|---|
| ~~OQ-1~~ | `## 대표 작업` 링크 형식 | **위키링크** (D3). career 는 그래프 노드가 아니라 L1 검증 대상이 아니고 Obsidian 탐색은 된다 |
| ~~OQ-2~~ | `stack` 판정 근거 | **의존성 파일 변경 감지 우선, LLM 은 패키지명만** (D3). 순수 LLM 판단은 날마다 흔들린다 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 잔디 산출물 계약 (신규) | create | 목적지 3개 · 각 갱신 범위 · career 압축 규칙 |
| `KDEV-SPEC-001` | update | `persona/daily/`·`persona/career/` 의 자동 갱신 주체 명시 |
