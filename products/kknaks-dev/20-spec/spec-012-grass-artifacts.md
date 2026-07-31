---
type: spec
id: KDEV-SPEC-012
title: "잔디 산출물 — daily·career·concept 계약"
status: draft
product: kknaks-dev
version: 0.0.1
created_at: 2026-07-31
updated_at: 2026-07-31
tags:
  - product/kknaks-dev
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
  decisions:
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
  specs:
    - "[[spec-011-commit-collection|KDEV-SPEC-011]]"
    - "[[spec-013-grass-gate|KDEV-SPEC-013]]"
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works: []
  releases: []
  related: []
---

# 잔디 산출물 — daily·career·concept 계약

커밋 조사 결과가 어떤 문서가 되는지 정한다. 착지는 셋이다 — **`persona/daily/`(그날) · `persona/career/`(누적) · `permanent/concept/`(개념)**.

> 조사 입력은 [[spec-011-commit-collection|KDEV-SPEC-011]], 승인·발행 절차는 [[spec-013-grass-gate|KDEV-SPEC-013]].

## 1. Context

### Meta

- Decision reference: [[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]
- Baseline reference: [[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]
- Domain note: 외부에 드러나는 것은 세 문서의 frontmatter 필드와 본문 섹션 구조다. 형식의 SoT 는 `templates/persona/daily.md`·`templates/persona/career.md`·`templates/knowledge/concept.md` 이며 **이 spec 은 형식을 복사하지 않는다.**
- Open questions: OQ-1 (daily body 길이 적정성 — 운영 후 조정)

### Business Requirement

두 가지 비대칭이 이 계약을 정했다.

1. **daily body 는 사이트에 노출되지 않고 career body 는 렌더된다.** 잔디는 `counts`(색 강도)와 `summary[]`(셀 카드)만 소비한다. 반면 career 본문은 경력 페이지에 마크다운으로 그대로 나간다. 자세히 쓸 가치가 있는 곳은 career 다.
2. **daily 는 누적되지 않는다.** 잔디는 rolling 365일 창이라 그 밖의 daily 는 사이트에서 사라진다. 축적된 것이 어디로도 흐르지 않는다.

career 본문의 `## 무슨 일 하는지`·`## 챌린지`·`## 배운 점` 은 지금 전부 비어 있다(`(TBD — 사용자 채움)`). 채울 재료는 매일 생산되고 있는데 연결이 없었다.

### Scope

In scope:

- 세 목적지의 경로·액션·갱신 조건
- career 갱신 범위와 **압축·재서술 규칙**, 사람 전용 필드
- `company`/`studio` 에 따른 career 귀속
- 형식 SoT 파일의 소유 관계와 진입점 등록
- daily body 길이 상한

Out of scope:

- 조사 입력 → SPEC-011
- 승인 게이트·발행 검증 → SPEC-013
- `products/*/showcase.md` 케이스 스터디, `persona/posts/` 회고 글 — 후속
- `bullets` 자동 갱신 — 영구 제외
- 그래프 정합 — 이 파이프라인 구축 후 별도 범위

## 2. UX Contract

### Placement

이 spec 은 문서 산출물 계약이라 자체 화면이 없다. 승인 화면은 SPEC-013 이 정의한다. 다만 **발행 결과가 두 공개 화면에 나타난다.**

### U-1. 잔디 (활동 그래프)

- **상태**: 발행된 daily 가 있는 날은 셀에 색이 든다. 승인 대기 중인 날은 **빈 칸**이다
- **문구**: 셀 클릭 시 활동 단위별 한 줄 요약(`[repo] ...`·`[notes] ...`·`[study] ...`)
- **CTA**: 없음
- **기대 결과**: `counts` 합이 색 강도를, `summary[]` 가 카드 내용을 정한다. **본문은 노출되지 않는다**

### U-2. 경력 타임라인

- **상태**: `is_current` 인 항목의 본문이 마크다운으로 렌더된다
- **문구**: `## 무슨 일 하는지` · `## 담당 영역` · `## 챌린지` · `## 배운 점` · `## 대표 작업`
- **CTA**: 없음
- **기대 결과**: 승인된 갱신분이 다음 로드부터 반영된다. `bullets` 는 이 화면에 나오지 않는다(이력서 PDF 전용)

## 3. User Scenario

### S-1. System — 그날의 daily 를 만든다

1. 조사 결과의 `counts` 를 그대로 frontmatter 에 박는다. **AI 가 세지 않는다.**
2. 활동 단위별 한 줄 요약을 ko/en 각각 만든다 — 활동이 0인 카테고리는 줄을 만들지 않는다.
3. 본문을 만든다. 사이트에 노출되지 않지만 career·concept 스테이지의 입력이자 git 기록이다.
4. 대상 날짜 파일이 없으면 생성, 있으면 덮어쓴다.
5. 대상 날짜 파일이 **본인 작성**이면 만들지 않는다 — 접수 단계에서 이미 걸러지고(SPEC-011), 발행 검증이 한 번 더 막는다(SPEC-013).

### S-2. System — career 를 갱신한다

1. 조사 결과의 career 귀속을 읽는다. `type=company` 인 레포의 커밋만 대상이다.
2. 대상 career 가 `is_current: true` 가 아니면 건너뛴다 — 끝난 재직 기간을 지금 커밋으로 고치지 않는다.
3. 그 career 에 귀속된 커밋이 0이면 **갱신안을 만들지 않는다.** AI 를 부르지 않는다.
4. 기존 문서 본문을 읽고, 오늘 조사분을 반영한 **갱신안 전문**을 만든다.
5. 더할 것이 없으면 `changed: false` 로 돌아간다 — 매일 갱신하되 대개 변경 없음이 정상이다.
6. 갱신은 **append 가 아니다.** 새 줄을 더하지 않고 기존 줄을 더 정확하게 만든다.
7. 섹션당 줄 수가 상한을 넘으면 합치거나 뺀다.

### S-3. System — 개념을 뽑는다

1. 조사 과정에서 재사용 가능한 개념 후보가 나오면 concept 초안을 만든다.
2. 같은 개념이 이미 있으면 **새 파일을 만들지 않고 기존 concept 를 보충한다.**
3. 개념 후보가 없으면 만들지 않는다. **억지로 만들지 않는다.**
4. 형식·계보 규칙은 지식노트 파이프라인 규칙과 concept 템플릿을 그대로 따른다 — 이 spec 이 다시 적지 않는다.

### S-4. owner — 승인 화면에서 회사 내용을 덜어낸다

1. 조사는 회사·개인 구분 없이 깊게 되어 있다(SPEC-011).
2. 공개될 문서에 남기고 싶지 않은 서술을 승인 화면에서 지운다.
3. 지운 결과가 승인 대상이 된다 — AI 제안 원본이 아니라 **사람이 고친 것**이 발행된다.

### S-5. owner — 본인이 그날 daily 를 직접 썼다

1. `auto: false` 로 daily 를 직접 작성한다.
2. 잔디는 그날 항목을 접수하지 않는다.
3. career·concept 도 만들어지지 않는다 — 그날 산출물 전체가 사람 소유다.

## 4. Interface Contract

### API Contract

이 spec 은 문서 계약이라 자체 엔드포인트가 없다. 발행 결과는 기존 활동·경력 조회 표면에 반영된다.

| Method | Path | 요약 | 권한 |
|---|---|---|---|
| GET | `/api/activity` | daily frontmatter 파생 (기존) | public |
| GET | `/api/career` | career frontmatter + body (기존) | public |

### Data Contract — 목적지

| 경로 | `type` | 액션 | 조건 |
|---|---|---|---|
| `persona/daily/{YYYY-MM-DD}.md` | `daily` | upsert | 활동 > 0 · 기존 파일이 본인 작성이 아님 |
| `persona/career/{stem}.md` | `career` | replace | `type=company` 커밋 있음 · `is_current: true` · `changed: true` |
| `permanent/concept/{slug}.md` | `concept` | upsert | 개념 후보 + 승인 |

### Data Contract — daily

| 필드 | 소유 | 설명 |
|---|---|---|
| `type`·`date` | 시스템 | 고정 |
| `auto` | 시스템 | 자동 생성분은 참 |
| `counts` | **코드** | `{commit, note, study}` — AI 가 세지 않는다 |
| `summary` | AI | `{ko: [], en: []}` — 활동 단위별 1줄, 0인 카테고리는 줄 없음 |
| 본문 | AI | **사이트 미노출.** career·concept 입력 + git 기록 |

본문 길이 상한은 **1200자**(하드 상한 1500자)다. 종전 500/600자는 career 입력으로 쓰기에 재료가 되지 않는다.

### Data Contract — career

| 필드 | 소유 | 갱신 |
|---|---|---|
| `## 무슨 일 하는지` | AI 초안 → 승인 | ○ |
| `## 담당 영역` | AI 초안 → 승인 | ○ (신설) |
| `## 챌린지` | AI 초안 → 승인 | ○ |
| `## 배운 점` | AI 초안 → 승인 | ○ |
| `## 대표 작업` | AI 초안 → 승인 | ○ — work 문서 위키링크 |
| `stack` | AI 초안 → 승인 | ○ (조건부, 아래) |
| `bullets` | **사람 전용** | ✗ — 이력서 PDF 문장 |
| `period`·`is_current`·`display_order`·`title`·`org`·`summary`·`location` | **사람 전용** | ✗ |

**갱신 규율**

| 규칙 | 계약 |
|---|---|
| append 금지 | 새 줄을 더하지 않고 기존 줄을 더 정확하게 만든다. append 하면 daily 의 복사본이 되고 "같은 사실은 한 곳에만" 을 위반한다 |
| 섹션 상한 | `## 챌린지`·`## 배운 점` 각 **5~7줄**. 넘으면 합치거나 뺀다 |
| `## 담당 영역` | 조사의 기술 영역 분해를 **서술로** 적는다. 커밋 수·라인 수 같은 숫자를 쓰지 않는다 |
| `## 대표 작업` | work 문서 위키링크. career 는 그래프 노드가 아니라 dead link 검증 대상이 아니고, Obsidian 탐색은 된다 |
| `stack` 판정 | **의존성 파일 변경이 먼저다.** `pyproject.toml`·`package.json`·`requirements.txt`·`go.mod` 등이 그날 diff 에 있을 때만 후보로 올리고, 추가된 패키지명을 AI 가 읽는다. 순수 AI 판단은 날마다 흔들린다 |
| `changed` | 더할 것이 없으면 거짓. 액션을 만들지 않는다 |

### career 귀속

```text
type=company + detail=<career stem>  →  persona/career/<career stem>.md
type=studio                          →  career 갱신 없음 (daily·concept 만)
```

`career/studio.md` 같은 항목을 만들지 않는다 — 다닌 적 없는 조직을 이력에 넣지 않는다. `studio` 작업의 누적 서술은 후속(showcase 케이스 스터디) 소관이다.

### 형식 SoT

| 파일 | 소유 | 읽는 쪽 |
|---|---|---|
| `templates/persona/daily.md` | **신규** — daily 형식 | 잔디 compose 스테이지 |
| `templates/persona/career.md` | **신규** — career 형식 + 갱신 규율 | 잔디 compose 스테이지 |
| `templates/knowledge/concept.md` + 지식노트 파이프라인 규칙 | 기존 — 재사용 | 잔디 compose · 유튜브 concept 게이트 |
| `agent.md` | 갱신 — "별도 계열" 에 daily·career 등록 | 에이전트 진입점 |

**규칙을 프롬프트에 복사하지 않는다.** 프롬프트는 "무엇을 만들라" 만 지시하고 형식은 레포에서 읽힌다. 복사하는 순간 SoT 가 둘이 되고 한쪽만 고쳐지는 날 조용히 어긋난다.

### State / Lifecycle

문서별 상태 전이는 없다. daily·career 는 파일 존재 여부만 갖고, 승인·발행 상태는 큐 항목이 소유한다(SPEC-013).

## 5. Implementation Rules

- **`counts` 는 코드가 센다.** AI 출력의 숫자를 신뢰하지 않는다.
- **career 는 전문 교체다.** 부분 패치를 하지 않는다 — 승인 화면이 보여준 것과 발행된 것이 같아야 한다.
- **사람 전용 필드는 갱신안에 포함되더라도 발행 시 무시**하는 것이 아니라, **애초에 갱신안이 그 필드를 담지 않는다.** 담기면 검증이 거부한다(SPEC-013).
- **본인 작성 보호는 이중이다** — 접수 단계(SPEC-011)와 발행 검증(SPEC-013).
- **concept 는 기존 규율을 그대로 받는다.** 잔디가 만든 concept 도 유튜브가 만든 것과 같은 형식·계보 검증을 통과해야 한다.
- **daily 본문은 노출되지 않는다는 사실을 형식 결정의 근거로 쓴다** — 읽는 사람을 위한 문서가 아니라 다음 단계의 입력이다.

## 6. Verification

### Acceptance Criteria

- [ ] daily `counts` 가 조사 결과와 정확히 일치한다 (AI 출력이 아님)
- [ ] 활동이 0인 카테고리는 `summary` 에 줄이 생기지 않는다
- [ ] 잔디 셀 카드에 `summary[]` 가 나오고 본문은 어디에도 나오지 않는다
- [ ] `type=studio` 레포만 커밋한 날은 career 갱신안이 만들어지지 않는다
- [ ] `is_current` 가 아닌 career 는 갱신 대상에서 빠진다
- [ ] career 갱신안에 `bullets`·`period`·`is_current` 가 포함되지 않는다
- [ ] 같은 챌린지가 이틀 연속 나와도 줄이 늘지 않고 기존 줄이 정확해진다
- [ ] `## 챌린지`·`## 배운 점` 이 7줄을 넘지 않는다
- [ ] 의존성 파일 변경이 없는 날에는 `stack` 갱신 후보가 오르지 않는다
- [ ] `## 대표 작업` 의 위키링크가 그래프 검증에 걸리지 않는다
- [ ] `auto: false` 인 날은 daily·career·concept 어느 것도 만들어지지 않는다
- [ ] `templates/persona/daily.md`·`career.md` 가 존재하고 `agent.md` 에 등록돼 있다
- [ ] 프롬프트에 daily·career 형식 명세가 복사돼 있지 않다

## 7. Open Questions

| ID | Question | Next |
|---|---|---|
| OQ-1 | daily 본문 1200자가 career 입력으로 충분한지 | 운영 후 조정 |
