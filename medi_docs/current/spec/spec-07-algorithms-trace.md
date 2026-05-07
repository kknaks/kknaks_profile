---
id: spec-07
type: spec
title: 알고리즘 (Interview Trace) — md 형식·API·source 정규화 파이프라인
status: draft
created: 2026-05-05
updated: 2026-05-05
sources:
  - "[[planning-03-algorithm-daily-tab]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-02-api-endpoints]]"
  - "[[spec-03-activity-scheduler]]"
  - "[[adr-04-llm-via-open-kknaks]]"
  - "[[adr-08-logic-quiz-format]]"
  - "[[adr-09-trace-yaml-via-settrace]]"
tags: [spec, algorithms, persona, schema, api, pipeline]
---

# 알고리즘 (Interview Trace) — md 형식·API·source 정규화 파이프라인

## Summary

planning-03 (해외 코딩 면접 트레이서) 의 **데이터·API 형식 명세**. 새 카테고리 `persona/algorithms/A-NNN-slug.md` 의 frontmatter, 본문 헤딩 + yaml 블록 (clarifying·approach·logic·trace·solution), API 엔드포인트 (read-only `GET`), source 정규화 파이프라인 (§4.8 매트릭스 → fetch · 캐시 · 정규화 · LLM gap-filler) 까지 한 곳. **per-항목 데이터 SoT = md 파일 자체**, 본 spec 은 형식 명세.

---

## 1. 위치·관계

| 문서 | 역할 |
|---|---|
| spec-01 | 페르소나 공통 컨벤션 (디렉토리·i18n·assets·위키링크). `algorithms/` 는 본 spec 이 신규 슬롯 추가 |
| spec-02 | v1.0 엔드포인트 목록. 알고리즘 API 2개 (§6) → 구현 시 spec-02 §2 표 합류 |
| spec-03 | 활동 잔디 잡 정의. 본 spec §8 의 **`neetcode-canonical` 잡 (매일 23:00 UTC)** 이 spec-03 에 행 추가됨. **잔디 잡과 별도 큐**, 매일 1개 commit 박힘 |
| planning-03 | 무엇을·왜 + 4 섹션 디자인 매핑 + §4.x 블록 정의 |

본 spec = **planning-03 §4 항목 구조 + §4.8 source 매트릭스 + ADR-08·09 결정** 을 형식으로 옮긴 것.

---

## 2. 디렉토리·파일명

```
persona/
├─ algorithms/                  ← 신규 (본 spec)
│  ├─ A-001-two-sum.md
│  ├─ A-002-best-time-buy-sell-stock.md
│  └─ ...
```

| 규칙 | 값 |
|---|---|
| 디렉터리 | `persona/algorithms/` (복수형, spec-01 의 `notes/`·`contents/` 와 동급) |
| 파일명 | `A-<NNN>-<slug>.md` — `NNN` 3자리 zero-pad, `slug` kebab-case 영문 |
| `id` (frontmatter) | `A-NNN` (파일 stem 접두와 일치) — API 의 `{id}` 와 동일 |

`contents/` 의 `C-NNN` 과 접두로 구분. `T-` (Trace) 로 변경 검토는 planning §9 row 5 후속.

---

## 3. frontmatter 스키마

| 키 | 필수 | 타입 | 설명 |
|---|---|---|---|
| `id` | ✅ | string | `A-NNN` (파일 stem 접두와 일치) |
| `type` | ✅ | string | 리터럴 `algorithm` |
| `title` | ✅ | `{ko, en}` | 목록·헤더용 (영문 NeetCode 제목 그대로 KO 같이 박음) |
| `date` | ✅ | string | `YYYY-MM-DD` 박힌 날 (스케쥴러 잡 박는 날, KST 기준) |
| `day` | 권장 | string | `Day NN` 시퀀스 표시 |
| `source` | ✅ | object | 멀티 platform — §3.1 |
| `difficulty` | ✅ | enum | `easy` \| `medium` \| `hard` |
| `tags` | 권장 | string[] | NeetCode 카테고리 (`array`·`hash`·`two-pointer` 등 — adr-08 §1.1 어휘) |
| `today` | 권장 | bool | true 면 목록 페이지 상단 강조 카드. **하루 1개만 true** (어제 항목은 자동 false 갱신 — §8.2) |
| `status` | 권장 | enum | `draft` \| `published` |
| `visible` | 권장 | bool | 사이트 노출 (default true) |
| `created` / `updated` | 권장 | ISO date | spec-01 관례 |

### 3.1 `source` 객체

```yaml
source:
  platform: leetcode          # enum: 현재 leetcode 만
  number: 1                   # 플랫폼별 번호
  slug: two-sum               # URL slug
  url: https://leetcode.com/problems/two-sum/
  curated_in: [neetcode150, blind75]   # 큐레이션 리스트
```

`platform` enum: `leetcode` 만. HackerRank·Codeforces 등 추가 시 enum 확장 (frontmatter 호환 유지).

### 3.2 보류 필드 (다음 버전)

- `promoted_to: string | null` — 노트 승격 backref. MVP 미사용 (planning §5).
- `related_notes: string[]` — 관련 노트 slug. MVP 미사용.

---

## 4. 본문 구조 — 단일 yaml 블록

본문 = **`## Data` 헤딩 하나 + fenced ` ```yaml ` 블록 1개** (전체 데이터 트리).

````md
## Data

```yaml
problem:     { ... }
clarifying:  { items: [ ... ] }
approach:    { items: [ ... ] }
logic:       { format: slot, slots: [ ... ] }
trace:       { code: [ ... ], cases: [ ... ], worked_example: { ... } }
solution:    { code: "...", complexity: { ... }, followup: [ ... ] }
```
````

**파싱**: frontmatter parser + `yaml.load(body 의 ## Data fenced block)` 1회. 헤딩별 분리 없음.

**다음 버전 Notes 블록**: 같은 yaml 트리에 `notes:` 키 추가 또는 별도 `## Notes` 헤딩 — 결정은 그때.

**미래 pure yaml 마이그레이션**: 본 구조는 frontmatter + body yaml 통합이 자명 → `algorithms/A-NNN-slug.yaml` 로 전환 시 frontmatter 키 + body yaml 키 합쳐 단일 yaml 트리. 결정·구현 비용 모두 적음.

---

## 5. yaml 트리 스키마

본문 `## Data` 아래 단일 yaml 트리. 6 최상위 키 — 각 §5.x 가 한 키씩 명세.

### 5.1 `problem`

```yaml
title: { ko: ..., en: ... }    # 짧은 제목 (frontmatter title 과 동일 가능)
statement: { ko: ..., en: ... }   # 한 줄 요약 (LeetCode content 첫 문단 trim, paraphrased)
constraints:                      # source = LeetCode constraints
  - "2 ≤ nums.length ≤ 1e4"
io:                               # source = LeetCode exampleTestcases (입출력 예시 1–2개)
  - { input: "...", output: "..." }
```

지문 전체 복사 X (저작권). 한 줄 요약만.

### 5.2 `clarifying`

```yaml
items:
  - q: { ko: ..., en: ... }
    type: good                  # good | distractor
    why: { ko: ..., en: ... }
```

- `items[]` 길이 **5–8** 권고 (good 3+ / distractor 2–3)
- `q` 한 줄 (max ~80자)
- `why` 한–두 문장

### 5.3 `approach`

```yaml
items:
  - name: { ko: ..., en: ... }
    complexity: "O(n) time / O(n) space"
    type: good                  # good | distractor
    why: { ko: ..., en: ... }
```

- `items[]` 길이 **3–5** 권고
- distractor 도 `complexity` 표시 (학습자가 잘못 떠올릴 만한 후보)

### 5.4 `logic`

```yaml
format: slot                    # 'slot' (MVP) | 'ordering' (후속) | 'state-first' (후속)
slots:
  - label: { ko: ..., en: ... }
    indent: 0                   # 0 기본, 1·2·3 으로 중첩
    options:
      - code: "seen = {}"
        type: good              # good = neetcode-gh 코드의 해당 라인 그대로 추출
        why: { ko: ..., en: ... }
      - code: "result = []"
        type: distractor        # LLM 변형 (off-by-one·자료구조 오용 등)
        why: { ko: ..., en: ... }
```

- `slots[]` 길이 **4–7** (core region 한정 — init·teardown 빼면 자연스러움)
- `options[]` per slot: 정답 1 + distractor 2–3
- **정답 코드는 source-extracted** (LLM 안 짓음 — adr-08 §2.2)
- `format=ordering`·`state-first` 의 schema 는 후속 ADR 에서 (current MVP enum validation 은 `slot` 만 통과)

### 5.5 `trace`

```yaml
code:                           # 솔루션 코드 (line-by-line array — UI 라인 번호 표시 편의)
  - "def two_sum(nums, target):"
  - "    seen = {}"
  - "    ..."
cases:                          # 머릿속 dry-run 케이스. 3개 권고
  - { input: "nums=[2,7,11,15], target=9", expected: "[0, 1]" }
  - { input: "nums=[3,2,4], target=6",     expected: "[1, 2]" }
worked_example:                 # 답안지 (1개 케이스)
  input: "nums=[2,7,11,15], target=9"
  steps:                        # 자유 형식 한 줄, 2–4 권고
    - { ko: "i=0, num=2 → ...", en: "..." }
  answer: "[0, 1]"
```

- step text 자유 형식 (라인 번호·콜스택 시각화 X — adr-09)
- step-by-step UI 없음. 사용자가 코드 보고 머릿속으로 따라가며 막히면 worked_example 펼침

### 5.6 `solution`

```yaml
code: |                         # neetcode-gh source 그대로 (multi-line string OK)
  def two_sum(nums, target):
      ...
complexity:
  time: "O(n)"
  space: "O(n)"
followup:                       # 1–3개, LLM 전적
  - { ko: "정렬되어 있다면? two pointers 로 O(1) 공간", en: "..." }
```

---

## 6. API 엔드포인트

i18n 쿼리 spec-02 동일 (`?lang=ko|en`).

| 메서드 | 경로 | 응답 핵심 |
|---|---|---|
| `GET` | `/api/algorithms?lang=ko` | `algorithms.{subtitle, intro, totalCount}`, `algorithms[]` (목록 행), `algorithms.today` |
| `GET` | `/api/algorithms/{id}?lang=ko` | 디테일 — frontmatter + 본문 yaml 파싱 결과 (problem·clarifying·approach·logic·trace·solution) + `newer`·`older` 인접 id |

**write API 없음**. 학습자 풀이는 클라이언트 세션 메모리만 (planning §6).

### 6.1 `GET /api/algorithms` 응답 예시

```jsonc
{
  "algorithms": {
    "subtitle":   "neetcode 150 · 키보드 없는 코딩 면접 도장",
    "intro":      "...",
    "totalCount": 7,
    "today": { "id": "A-007", "title": "Two Sum", "date": "2026-05-05" }
  },
  "algorithms[]": [
    {
      "id":         "A-001",
      "date":       "2026-05-05",
      "day":        "Day 01",
      "title":      "Two Sum",
      "summary":    "정렬되지 않은 정수 배열에서 합이 target 인 두 인덱스 — hash map 으로 O(n)",
      "difficulty": "easy",
      "source":     { "platform": "leetcode", "number": 1, "slug": "two-sum", "url": "..." },
      "tags":       ["array", "hash"]
    }
  ]
}
```

### 6.2 `GET /api/algorithms/{id}` 응답 예시

```jsonc
{
  "algorithms.detail": {
    "id":      "A-001",
    "title":   "Two Sum",
    "source":  { ... },
    "problem":     { "statement": "...", "constraints": [ ... ], "io": [ ... ] },
    "clarifying":  [ ... ],
    "approach":    [ ... ],
    "logic":       { "format": "slot", "slots": [ ... ] },
    "trace":       { "code": [ ... ], "cases": [ ... ], "worked_example": { ... } },
    "solution":    { "code": "...", "complexity": { ... }, "followup": [ ... ] },
    "newer":       null,
    "older":       { "id": "A-002", "title": "..." }
  }
}
```

`{ko,en}` 객체 필드는 백엔드가 `?lang` 에 맞춰 한 쪽 string 으로 평탄화해서 응답.

### 6.3 spec-02 합류

spec-02 §2 표에 위 2 행 추가 — 구현 시점 PR 1개로.

---

## 7. Source 정규화 파이프라인 (§4.8 매트릭스 이행)

스케쥴러 잡 (`neetcode-canonical`) 이 1회 실행하는 **5 단계**.

### 7.1 단계

```
input: NeetCode 150 시퀀스의 다음 slug (잡 상태에서 읽음)

(a) source fetch
    - LeetCode GraphQL → questionFrontendId · title · content (HTML) · exampleTestcases (raw)
                       · difficulty · topicTags · hints · metaData (JSON 문자열)
    - neetcode-gh raw.githubusercontent.com/neetcode-gh/leetcode/main/python/{NNNN}-{slug}.py
                       → 솔루션 코드 (class Solution 패턴 일관)

(b) 캐시 (idempotent)
    - 같은 slug 재호출 시 외부 API 안 때림 — local 캐시 (file 또는 redis)

(c) 미니멀 정규화 (deterministic, LLM 호출 X)
    - metaData JSON.loads → params count 결정 (= exampleTestcases 분할 단위)
    - exampleTestcases newline-split → params count 줄씩 grouping → cases 배열 (input 만)
    - difficulty `.lower()` (Easy → easy)
    - topicTags slug 그대로 (`hash-table`·`dynamic-programming` 등 NeetCode 어휘)
    - core region 라인 set 판별 (adr-08 §2.4 휴리스틱)
      → 솔루션 코드의 `class Solution: def methodName(self, ...)` 본체 inner 라인들

(d) LLM 통째 — open-kknaks 1회 호출 (adr-04)
    - **입력**: raw HTML content · 정규화 결과 (cases input 등) · 솔루션 코드 · 추출된 core region 라인 set · tags
    - **출력 (spec-07 yaml 6 키)**:
      - problem.{title, statement, constraints, io}
        ← raw HTML → paraphrase + 추출 (statement 한 줄 / constraints list / io.output)
      - clarifying.items / approach.items
      - logic.{format=slot, slots[].label/indent/options}
        ← 정답 옵션의 code 는 §c 의 추출 라인 그대로, distractor·why 만 LLM 생성
      - trace.{cases, worked_example}
        ← cases input 은 §c 그대로, expected (output) 와 worked_example 은 LLM
      - solution.{code, complexity, followup}
        ← code 는 source 그대로, complexity 와 followup 만 LLM
    - **HTML 파싱 위임 이유**: LeetCode `content` 의 example 포맷이 두 종류 (옛 `<pre>` / 새 `<div class="example-block">`) + 트리 문제는 `<img>` 섞임. 정형 파서가 깨끗하게 안 잡힘 → LLM 이 robust.
    - **source-first 정신 유지**: 정답 코드 라인 + cases input 은 §c 의 추출값 그대로, LLM 이 *발명* 하는 부분 = HTML 가공 + distractor + narrative 영역만.

(e) md 박음
    - frontmatter + 본문 `## Data` yaml 블록 조립 (spec §4)
    - 파일명: A-NNN-slug.md (NNN = 다음 시퀀스 번호)
    - `today` 필드 mutation (이전 today=true 항목들 → false, spec-03 §11.5)
    - git commit + push (spec-03 §5 의 `commit_and_push_with_retry` 재사용)
```

### 7.2 source 매트릭스 → 단계 매핑

| 필드 | source (raw) | LLM 가공 영역 | 단계 |
|---|---|---|---|
| Problem statement (한 줄) | LeetCode `content` (HTML) | HTML → 한 줄 paraphrase | (a) (d) |
| Problem constraints | LeetCode `content` (HTML — `<strong>Constraints:</strong>` 다음) | HTML → list[str] 추출 | (a) (d) |
| Problem io.input | LeetCode `exampleTestcases` (newline-delimited) | — (`metaData.params.length` 줄씩 split) | (a) (c) |
| Problem io.output | LeetCode `content` (HTML — `Output:` 라벨 추출) | HTML → 추출 (LLM 위임) | (a) (d) |
| Problem tags | LeetCode `topicTags[].slug` | — (그대로 사용) | (a) (c) |
| Problem difficulty | LeetCode `difficulty` | `.lower()` | (a) (c) |
| Clarifying items | — | 전적 LLM (면접관 시뮬레이션) | (d) |
| Approach items | neetcode-gh 패턴 (코드 보고 추론 가능) | distractor·trade-off·why·complexity 모두 | (a) + (d) |
| Logic 정답 코드 | neetcode-gh code 의 core region 라인 | — (§c 추출 그대로) | (a) (c) |
| Logic distractor + label·indent·format | — | 전적 LLM | (d) |
| Trace cases input | LeetCode `exampleTestcases` | — | (a) (c) |
| Trace cases expected | LeetCode `content` (HTML) | HTML → 추출 또는 LLM 시뮬레이션 | (d) |
| Trace worked_example | — | 전적 LLM (단일 케이스 step text) | (d) |
| Solution code | neetcode-gh repo | — (그대로) | (a) |
| Solution complexity | — (neetcode-gh 주석 없음 가정) | LLM (코드 보고 추론) | (d) |
| Solution followup | — | 전적 LLM | (d) |

**(c) 단계 deterministic 작업** — 매우 좁음:
- `metaData` JSON.loads
- `exampleTestcases` newline split
- `difficulty` lower
- core region 라인 식별 (정규식 또는 AST 분석)

**(d) 단계 LLM 책임** — input HTML + raw code → 6 yaml 키 통째 출력. HTML 파싱은 LLM 이 robust 하게.

### 7.3 실패 처리

| 실패 | 처리 |
|---|---|
| LeetCode GraphQL down | 잡 실패 → 다음 날 재시도. 해당 일자 빈 칸 (`today: false`) |
| neetcode-gh 솔루션 누락 (slug 미존재) | LLM fallback — `solution.code` LLM 생성, frontmatter 에 `solution_source: 'llm-fallback'` 마킹 |
| LLM 응답 파싱 실패 | 잡 실패 → 다음 날 재시도 |
| 외부 lib 의존 솔루션 | 그대로 진행 — Trace 는 어차피 LLM 자유 텍스트 (adr-09 단순화 후 sandbox 부담 없음) |

---

## 8. 잡 인터페이스 (spec-03 갱신 입력)

본 spec 의 `neetcode-canonical` 잡은 **잔디 잡과 별도 큐** 로 등록.

| 속성 | 값 |
|---|---|
| 잡 이름 | `neetcode-canonical` |
| 큐 | `algorithm` (잔디 잡은 `daily`) |
| 스케줄 | 매일 23:00 UTC (= KST 다음날 08:00) |
| 트리거 | APScheduler `cron(hour=23, minute=0)` |
| 실행자 | back 컨테이너 → open-kknaks 워커 (adr-04 와 동일 redis broker) |
| 산출물 | `persona/algorithms/A-NNN-slug.md` 1개 + git commit/push |
| 잔디 영향 | 별도 — 본 잡의 commit 도 daily commit 기록에 자연스럽게 반영 (잔디 잡이 git log 보고 카운트 — spec-03) |
| 실패 시 | 다음 날 재시도. 해당 날짜 빈 칸 |

### 8.1 잡 사이드 이펙트 — `today` 필드 갱신

매 잡 실행 시:

1. 새 항목 생성 → `today: true` 박힘
2. **이전 `today: true` 항목들** → `today: false` 로 갱신 (frontmatter mutation 1회)
3. commit 메시지에 두 변경 포함

이게 잡의 *유일한 frontmatter mutation*. 학습자 인터랙션은 절대 frontmatter 안 건드림 (planning §6).

### 8.2 NeetCode 150 시퀀스 진행도

잡 상태 (어디까지 갔는지) 는 **redis** 에 박힘 (spec-03 §11.4):

```
key: kknaks-portfolio:neetcode:next_index → "8"
key: kknaks-portfolio:neetcode:last_run   → "2026-05-05T23:00:00Z"
```

NeetCode 150 의 slug 시퀀스는 잡 코드에 하드코드 (또는 별도 yaml). `_meta.yaml` 은 spec-01 의 *사람이 박는 enum 정의* 전용 — 잡 자동 갱신 상태는 redis 가 정합.

---

## 9. 미정·후속

- 라우트 prefix `A-` → `T-` 변경 — planning §9 row 5 후속.
- `logic.format` 의 `ordering`·`state-first` 추가 — adr-08 후속 (~Day 50, ~Day 100).
- spec-03 갱신 본문 — 본 spec 박힌 후 별도 PR (§8 인터페이스를 spec-03 잡 라인업에 흡수).
- spec-02 §2 엔드포인트 목록 합류 — 구현 시점.
- `solution_source` enum (`neetcode-gh` | `llm-fallback`) frontmatter 추가 검토 — 누락 통계용.
