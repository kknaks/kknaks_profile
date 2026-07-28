---
type: spec
id: KDEV-SPEC-001
title: "지식그래프 디렉토리 구조"
status: draft
product: kknaks-dev
version: 0.0.4
created_at: 2026-06-29
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-001-products-single-root|KDEV-DEC-001]]"
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
    - "[[decision-008-contents-retention|KDEV-DEC-008]]"
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
  specs:
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
  works: []
  releases: []
  related: []
---

# 지식그래프 디렉토리 구조

레포의 모든 노트가 어느 디렉토리에 사는지, 각 디렉토리가 그래프에서 어떤 **층(layer)**과 노드 타입을 담는지에 대한 계약. 작성자·에이전트·빌더가 이 문서만으로 노트 위치를 판단할 수 있어야 한다.

> v0.0.4 — [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] 반영. 지식 층을 **출처 → 원자 개념 → 종합 판단 → 실행** 4층으로 재편하고 `permanent/concept/`를 신설한다.

## 1. Context

### Meta

- Decision reference: [[decision-001-products-single-root|KDEV-DEC-001]], [[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]], [[decision-008-contents-retention|KDEV-DEC-008]], [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]
- Baseline reference: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]], [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]
- Domain note: 지식 층 = `source`/`concept`/`synthesis`/`execution`. 노드 타입과 `layer` 축의 스키마 상세는 [[spec-002-graph-schema|KDEV-SPEC-002]].
- Open questions: §7

### Business Requirement

흩어진 생각·자료·제품 문서가 일관된 위치 규칙을 가져야, 작성 시 "어디 둘지" 고민이 없고 빌더가 디렉토리로 층과 노드 타입을 결정할 수 있다.

특히 **같은 개념이 여러 자료에 걸쳐 나올 때 합류할 자리**가 있어야 한다. 자료(reference)와 개념은 1:1이 아니다 — 영상 하나에서 개념이 여럿 나오고 개념 하나가 영상 여럿에 걸쳐 나온다. 층을 합치면 자료 기준으로는 개념이 흩어지고 개념 기준으로는 "그 자료가 뭐라 했는지"가 사라진다.

### Scope

In scope:
- 지식 4층과 디렉토리 매핑(`source`/`concept`/`synthesis`/`execution`)
- `permanent/concept/` 신설과 그 작성 규약
- 루트 레벨 지식 파이프라인 층(inbox/reference/permanent)
- products 제품 레이아웃(showcase + 파이프라인)
- persona 재편(posts 신설, projects/notes/contents 이동 결과)

Out of scope:
- 실제 파일 이동·코드 정합(work)
- 노드/엣지 스키마·`layer` 축의 표현 방식([[spec-002-graph-schema|KDEV-SPEC-002]])
- 층별 검증 규칙([[spec-004-graph-validation|KDEV-SPEC-004]])
- 노트가 그 위치에 **도달하는 과정**(승인 게이트 체인) — [[spec-003-knowledge-workflow|KDEV-SPEC-003]]

## 2. UX Contract

해당 없음 (디렉토리 구조 계약, 화면 없음).

## 3. User Scenario

### S-1. 작성자 — 새 노트를 둘 위치 결정

1. 정제 안 된 생각이면 → `inbox/` (type: idea, 휘발).
2. 외부 자료를 읽고 **그 자료가 무엇을 말했는지** 정리한 것이면 → `reference/` (flat) (type: reference, 층 `source`).
3. 자료에서 뽑은 **재사용 가능한 개념 하나**면 → `permanent/concept/` (type: concept, 층 `concept`).
4. 개념들을 엮어 내린 **내 판단·전략**이면 → `permanent/` 루트 (type: permanent, 층 `synthesis`).
5. 제품 스펙감이면 → `products/{제품}/00-baseline` (type: baseline 등, 층 `execution`, 00→20 파이프라인).
6. 발행할 글이면 → `persona/posts/` (type: post).
7. 안 쓰게 된 영구노트·개념은 → `permanent/archive/` (cold).

3과 4를 가르는 기준은 **"사실이냐 판단이냐"**다. "STT는 음성을 텍스트로 바꾸는 기술이고 이런 구조로 동작한다"는 concept이고, "우리 제품에 STT를 붙일지, 붙인다면 어느 지점에"는 synthesis다.

### S-2. 작성자 — 같은 개념이 두 번째 자료에서 또 나온다

1. 새 자료를 `reference/` (flat)에 정리한다.
2. 그 자료에서 나온 개념이 이미 `permanent/concept/`에 있는지 확인한다 — 파일명 stem과 `aliases`로 찾는다.
3. **있으면 새 파일을 만들지 않고 기존 concept를 보충**한다. 새 자료를 `up:`과 본문 `[[]]`에 추가한다.
4. 없으면 새 concept를 만든다.

같은 개념이 `stt.md`와 `speech-to-text.md`로 갈라지면 SoT가 둘이 된다. `aliases`가 그 갈라짐을 막는 1차 장치다(§5).

## 4. Interface Contract

### API Contract

해당 없음.

### Data Contract — 층 매핑

지식 그래프에 편입되는 4층. 방향은 **출처 → 개념 → 판단 → 실행**이다.

| 층(`layer`) | 디렉토리 | `type` | 답하는 질문 | 단위 | 수명 |
|---|---|---|---|---|---|
| `source` | `reference/` (flat) | `reference` | "이 자료가 뭐라고 했나" | 자료 하나 | 생성 후 고정 |
| `concept` | `permanent/concept/` | `concept` | "이 개념은 뭔가" | 개념 하나 | 출처 합류로 **성장** |
| `synthesis` | `permanent/` 루트 | `permanent` | "내 판단·전략은 뭔가" | 영역 하나 | 개념 유입마다 갱신 |
| `execution` | `products/{제품}/` | `baseline`·`decision`·`spec`·`work`·`release`·`runbook` | "그래서 뭘 만드나" | 프로젝트 문서 | 제품 파이프라인을 따름 |

그래프 밖에 남는 디렉토리:

| 디렉토리 | `type` | 비고 |
|---|---|---|
| `inbox/` | `idea` | 휘발. 노드이되 층에 속하지 않고 `up:` 대상이 될 수 없다 |
| `persona/contents/` | `content` | YouTube 요약 파이프라인. 그래프 비대상([[decision-008-contents-retention|KDEV-DEC-008]]) |
| `persona/algorithms/` | `algorithm` | 개인 배치 산출물. 그래프 비대상 |
| `persona/daily/` · `career/` · `profile.md` · `assets/` | `daily`·`career`·`profile` | 정체성(그래프 주변) |
| `persona/posts/` | `post` | 발행물. **디렉토리 미존재·배선 미완**([[decision-008-contents-retention|KDEV-DEC-008]] Scope Out) |

### Data Contract — 디렉토리 레이아웃

```text
inbox/                 # type: idea (휘발, 미정제)
reference/             # 층: source
└── {group}/           # type: reference — group은 persona/_meta.yaml clusters
permanent/             # 층: synthesis
├── concept/           # 층: concept — type: concept (원자 개념, flat)
├── *.md               # type: permanent (종합 판단)
└── archive/           # 장기기억 (cold) — permanent·concept 공용
products/              # 층: execution
└── {제품}/
    ├── README.md
    ├── showcase.md    # 블로그 카드 (frontmatter: org, category, status …)
    ├── 00-baseline/ … 60-release/   # 개인 제품만 채움
    └── log.md
persona/
├── posts/             # type: post (발행물, 미배선)
├── career/ · profile.md · daily/ · assets/   # 정체성(그래프 주변 노드)
├── algorithms/        # 그래프 무관, 잔류
└── contents/          # type: content — YouTube 요약 파이프라인, 그래프 무관, 잔류 (DEC-008)
```

- `permanent/concept/`는 **flat**이다. 하위 디렉토리를 두지 않는다 — 개념은 분류 트리가 아니라 링크 그래프로 조직된다.
- `permanent/archive/`는 층이 아니라 **상태**다. 안 쓰게 된 `permanent`와 `concept`가 함께 내려간다.
- `products/{제품}/showcase.md` frontmatter: `org: company | studio`, `category`, `status`, `visible`, `thumbnail`.
- 회사 프로젝트 = `showcase.md`만, 개인 제품 = showcase + 파이프라인.

### State / Lifecycle

노트 위치 전이는 [[spec-003-knowledge-workflow|KDEV-SPEC-003]] 참조.

## 5. Implementation Rules

- 노드 타입과 층은 디렉토리가 1차 결정, frontmatter `type`이 명시(불일치 시 검증 ERROR — [[spec-004-graph-validation|KDEV-SPEC-004]]).
- 파일명 stem 전역 유일(식별자 — [[spec-002-graph-schema|KDEV-SPEC-002]]).
- 실제 디렉토리 이동·라우트/로더 코드 정합은 work에 둔다.
- showcase-only 제품(회사/일부 개인, S1)은 stage 디렉토리(00~30) 없이 `showcase.md`만 둔다. product-doc-pipeline은 **showcase.md 有 + stage 디렉토리 無**를 showcase-only로 추론해 stage README 강제를 면제한다(D-001/D-003 파생).

### concept 층 규약

- **한 파일 = 한 개념.** `permanent/concept/{stem}.md`, flat.
- **`aliases` 필수.** 같은 개념의 다른 이름을 모두 적는다(예: `stt` → `[Speech-to-Text, 음성인식, ASR]`). 개념 중복 생성을 막는 1차 장치이며, 빌더의 alias 인덱스가 이를 stem으로 해소한다([[spec-002-graph-schema|KDEV-SPEC-002]]).
- **`up:` 필수.** concept는 자신이 나온 출처(`reference`)를 `up:`으로 가리킨다. 출처 없는 concept는 성립하지 않는다.
- **SoT 위임.** 개념 상세의 SoT는 concept 노트 한 곳이다.
  - `reference`는 개념을 재서술하지 않고 **요지 + `[[concept]]` 링크**로 위임한다.
  - `permanent` 종합 노트도 개념을 재서술하지 않고 **엮은 판단만** 소유하며, 구성 개념은 `[[concept]]`로 참조한다.
  - "재서술하지 않는다"는 **개념의 상세 설명 섹션을 복사하지 않는다**는 뜻이다. 판단 문장 안에 개념 요지가 인용되는 것은 허용하며 필연적이다.
- **개념 성장.** 같은 개념에 두 번째 출처가 오면 새 파일을 만들지 않고 기존 concept를 **보충**한다. 보충 시 새 출처를 `up:`과 본문 `[[]]`에 추가한다.
- 안 쓰게 된 concept는 `permanent/archive/`로 내린다(`permanent`와 동일 규칙).

### 층 간 참조 방향

`up:`은 **상류(출처 방향)** 만 가리킨다. 층 번호가 같거나 낮은 쪽이다.

| 노트 | `up:` 대상 | 의미 |
|---|---|---|
| `concept` | `reference` | 이 개념이 나온 출처 |
| `permanent`(synthesis) | `concept` | 이 판단을 구성하는 개념 |
| `execution` | `concept` · `permanent` | 이 제품 결정의 근거 |
| `idea` | — | `up:` 금지(휘발) |

방향 판정의 구현 규칙은 [[spec-002-graph-schema|KDEV-SPEC-002]]와 [[spec-004-graph-validation|KDEV-SPEC-004]] L4가 소유한다.

## 6. Verification

### Acceptance Criteria

- [ ] inbox/reference/permanent(+archive) 루트 층 존재.
- [ ] `permanent/concept/` 디렉토리가 존재하고 flat이다.
- [ ] products/{제품}/에 showcase.md 규약 적용, org 필드로 회사/개인 구분.
- [ ] persona/posts 신설, projects→products·notes→reference 재편 완료 (contents 잔류 — DEC-008).
- [ ] 각 디렉토리의 노드 타입이 frontmatter `type`과 일치.
- [ ] 4층(`source`/`concept`/`synthesis`/`execution`)이 디렉토리에서 일의적으로 도출된다.
- [ ] concept 노트가 `aliases`와 `up:`을 모두 갖는다.
- [ ] concept의 `up:` 대상이 `reference`이고, `permanent` 종합 노트의 `up:` 대상이 `concept`다.
- [ ] `reference`·`permanent` 본문에 개념 상세 설명 섹션이 복사되지 않고 `[[concept]]` 링크로 위임된다.
- [ ] 같은 개념이 서로 다른 stem으로 중복 생성되지 않는다(`aliases`로 해소).

## 7. Open Questions

- `reference/`의 group 13종을 4층 재편에 맞춰 정리할지 — 현재 `BackendSchool`·`bitcamp` 등 과거 교육과정 잔재가 섞여 있다([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] OQ-1).
- concept의 입도 — "STT" 하나로 둘지 "STT / 스트리밍 ASR / VAD"로 쪼갤지. 너무 잘게 쪼개면 성장이 안 되고 너무 크면 SoT가 흐려진다. 유튜브 파이프라인 첫 실전에서 관찰 후 규칙화한다([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] OQ-2).
- `layer`를 frontmatter에 명시할지 디렉토리에서 도출만 할지 — 표현 방식은 [[spec-002-graph-schema|KDEV-SPEC-002]]가 소유한다([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] OQ-4).
- 그 외 구현 세부는 work.
