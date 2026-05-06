---
id: adr-08
type: adr
title: 논리 구조 quiz format = slot (MVP) · ordering · state-first 후속
status: draft
created: 2026-05-05
updated: 2026-05-05
sources:
  - "[[planning-03-algorithm-daily-tab]]"
  - "[[adr-04-llm-via-open-kknaks]]"
tags: [adr, algorithms, quiz, logic-structure, neetcode, format]
---

# 논리 구조 quiz format = slot (MVP) · ordering · state-first 후속

## Summary

planning-03 §4.4 **논리 구조** 블록의 quiz 인터랙션을 패턴별로 3종 (slot · ordering · state-first) 으로 다원화. **MVP 는 `slot` 만** 구현 — NeetCode 150 의 array · hash · two-pointer · sliding window · binary search 패턴 (~70-80% cover). ordering · state-first 는 시퀀스 진행에 따라 후속 추가.

**source-first 적용** — 각 slot 의 *정답 코드 라인* 은 neetcode-gh 솔루션의 core region 에서 **그대로 추출** (LLM 이 짓지 않음). LLM 은 *distractor 변형* + *why 텍스트* + *format 결정* 만 책임. ADR-09 (Trace) 와 동일 패턴 — 데이터는 source, 설명은 LLM.

---

## 1. Context

planning-03 §4.4 (논리 구조) 는 면접 Code 단계 (20–25분) 의 본질을 키보드 X 환경에서 **알고리즘 흐름·자료구조·제어 흐름의 합성** 으로 환원한 quiz. *코드 typing* 이 아니라 *합성 활동* 이므로 인터랙션 형태가 패턴별로 다름:

- **선형 패턴** (array/hash/loop) — 각 단계가 코드 한 줄로 분리 가능 → slot 별 단일 선택
- **재귀·트리 패턴** — 호출 순서가 핵심 → 단계 ordering
- **DP · complex state** — state 정의·transition 식이 핵심 → 단계별 (state → transition → base case)

### 1.1 NeetCode 150 패턴 분포 (대략)

| 패턴군 | 비중 | 적합 format |
|---|---|---|
| Array · Hash | ~25% | slot |
| Two Pointer · Sliding Window | ~15% | slot |
| Binary Search | ~5% | slot |
| Stack · Heap · Linked List | ~15% | slot (linked list 일부 ordering) |
| Tree · Graph (재귀·BFS·DFS) | ~20% | ordering |
| Backtracking | ~5% | ordering |
| DP (1D/2D) | ~10% | state-first |
| Trie · Union-Find | ~5% | slot (메서드별) |

NeetCode 150 시퀀스 시작부 (~50 문제) 는 array · hash · two-pointer 위주 → **slot 단일 format 으로 충분 cover**.

### 1.2 source-first 와 정합

planning-03 §4.8 매트릭스에서 §4.4 의 1차 source = neetcode-gh 솔루션 코드의 core region. **정답 코드 라인은 source 에서 추출** (LLM 이 짓지 않음 — 합성 quiz 의 정답이 §4.6 솔루션과 정합 보장). format 결정·distractor 생성·why 텍스트만 LLM (open-kknaks via adr-04).

---

## 2. Decision

### 2.1 format 3종 정의

#### `slot` (MVP 구현)

- 코드 한 줄 단위 단일 선택. 각 slot 마다 정답 1 + distractor N개.
- **core region 한정** — init·teardown 제외, inner body 만.
- **정답 코드 = neetcode-gh 솔루션의 해당 라인 그대로 추출** (LLM 이 짓지 않음). distractor 만 LLM 이 *정답 라인을 의도적으로 변형* 해서 생성 (off-by-one, 자료구조 오용, 키·값 swap 등).
- 학습자 UI: slot 별 라디오 선택 → "확인" → 정답 공개 → 옵션별 ▾ 이유 펼침 (3 단계).

```yaml
logic:
  format: slot
  slots:
    - label: { ko: 초기화, en: Initialize }
      indent: 0
      options:
        - { code: "seen = {}", type: good, why: { ko: "...", en: "..." } }       # ← neetcode-gh 라인 추출
        - { code: "result = []", type: distractor, why: { ko: "...", en: "..." } }   # ← LLM 변형
```

#### `ordering` (후속)

- 정답 step 들을 *섞어서* 줌 → 학습자가 순서 재배열. 일부 distractor 섞을 수 있음.
- 적합: 재귀 호출 순서, 트리 traverse, backtracking pick/recurse/unpick.
- UI: step 카드 드래그 또는 ↑↓ 버튼.

```yaml
logic:
  format: ordering
  steps:
    - { id: 1, code: "if not root: return 0", correct_pos: 1, why: {...} }
    - { id: 2, code: "left = depth(root.left)", correct_pos: 2, why: {...} }
```

#### `state-first` (후속)

- DP state 정의 → transition → base case 단계별 단일 선택. 일종의 *meta slot* (slot 의 의미가 더 큼).
- 적합: DP, complex state 추적.

```yaml
logic:
  format: state-first
  stages:
    - { name: state,      label: "dp[i] 의 의미?",    options: [...] }
    - { name: transition, label: "dp[i] = ?",          options: [...] }
    - { name: base,       label: "초기값?",            options: [...] }
```

### 2.2 생성 파이프라인 — 추출 + LLM 분담

스케쥴러 잡이 §4.4 콘텐츠 생성 시:

1. **neetcode-gh 솔루션 코드 fetch** — 캐시
2. **core region 판별** (§2.4 휴리스틱) — adr-09 와 같은 라인 set 공유
3. **정답 코드 추출** — core region 의 각 라인을 slot 의 `good` 옵션으로 박음 (코드 그대로, 추출이지 생성 아님)
4. **LLM 메타 호출 (open-kknaks)** — 입력: `{ tags, 솔루션 코드, 추출된 정답 라인들 }` / 출력:
   - format 결정 (`slot` | `ordering` | `state-first`)
   - 각 slot 마다 distractor N개 (정답 라인을 의도적으로 변형)
   - 각 옵션 (good + distractor) 의 why 텍스트
   - slot 의 label (`초기화`·`반복문`·`분기 조건` 등)
   - indent 정보 (중첩 깊이)

LLM 호출 1회로 distractor + why + label + indent 한 번에 받음. **정답 코드는 LLM 응답에 포함시키지 않음** — 우리가 추출한 값을 yaml 박을 때 합치기.

프론트는 `logic.format` enum 으로 분기 → 컴포넌트 다른 거 렌더.

### 2.3 MVP scope = `slot` 만

- **`slot` format 만 구현** (`SlotQuiz` 컴포넌트). `ordering` · `state-first` 는 prompt template 만 미리 박아두고 컴포넌트 비활성.
- LLM 프롬프트가 *"현재 slot format 만 지원"* 고지 → ordering/state-first 패턴 문제 만나면 **fallback 으로 slot 시도**. 부자연스러우면 quiz 누락 (md 본문에 `## Logic` 비움).
- 시퀀스 ~50 문제 누적 또는 사용자 본인이 ordering 필요성 felt 시점에 ordering 추가. state-first 는 DP 패턴 도달 시 (대략 100일 차).

### 2.4 core region 판별 휴리스틱

LLM 이 같이 결정. neetcode-gh 솔루션 코드 함수 본체에서:

| 패턴 | core region 후보 |
|---|---|
| 단일 loop | `for ... :` 의 body |
| 중첩 loop | 가장 안쪽 body + 한 단계 위 |
| 재귀 | `def f():` 의 body (base case + recurse 호출) |
| 분기 (early return) | 분기 조건 + branch body |

모호하면 init/teardown 라인만 제외하고 가운데 모두 core 로 fallback.

---

## 3. Alternatives Considered

### 3.0 LLM 이 정답 코드까지 짓기

- LLM 한 번 호출로 slot 정의 + 정답 코드 + distractor + why 다 박음 (현재 ADR 의 추출 단계 빼고).
- **장점**: 파이프라인 단순. 1회 LLM 호출.
- **단점**: 정답 코드 hallucination 위험 — neetcode-gh 의 canonical 코드와 *정확히 일치* 한다는 보장 없음. `seen[num] = i` 를 `seen[num] = i + 1` 같이 미묘하게 변경할 수 있음. **§4.4 의 정답이 §4.5 Trace 의 실행 코드와 어긋나면** 학습자가 §4.4 에서 푼 코드가 §4.5 에서 다른 동작 → 인지 깨짐.
- **기각**: source-first 정신 위반. 정답 hallucination 허용 X.

### 3.1 단일 format (slot) 만 영구

- **장점**: 구현 단순. UI 일관. 1 컴포넌트.
- **단점**: NeetCode 150 의 ~30% (재귀·DP) 가 부자연스러움. 합성 본질이 흐려짐. 면접 prep 의 핵심 패턴 (DP·tree) 에서 도장 가치 떨어짐.
- **기각**: 도장의 폭 좁아짐. 사용자 의도 ("논리 구조가 핵심") 와 충돌.

### 3.2 단일 format (ordering) 만 영구

- **장점**: 모든 패턴에 적용 가능.
- **단점**: 선형 패턴 (Two Sum 등) 에서 *너무 자명* → 학습 가치 낮음. distractor 섞기도 어색.
- **기각**: easy 문제에서 도장 가치 잃음.

### 3.3 단일 format (skeleton-fill — 의사코드 빈칸 채우기) 만 영구

- **장점**: 모든 패턴에 적용 가능, 합성 단계 명료.
- **단점**: 의사코드 합의된 형식이 없음 — 솔루션 마다 어색. 결국 slot 의 변형이라 정합 안 잡힘.
- **기각**: slot 과 본질 차이 없음 + 어색.

### 3.4 (현 결정) 3종 다원화 + MVP slot only

- **장점**: 각 패턴에 자연스러운 인터랙션. 점진 추가 가능. MVP 부담 1 컴포넌트.
- **단점**: 구현 비용 ↑ (장기). LLM format 결정 정확해야 함.
- **수용**: MVP scope 가 slot 으로 충분 cover. 다원화는 *데이터 모델·prompt template* 에 미리 박고 컴포넌트는 점진 추가 — 가장 적은 비용으로 미래 옵션 보존.

---

## 4. Consequences

### 4.1 즉시 효과

- **spec-07** frontmatter 에 `logic.format` enum 필드 추가 (`slot` | `ordering` | `state-first`). MVP 는 `slot` 만 valid.
- **proto-algorithms.jsx** 의 `LogicPanel` — 현재 slot 가정으로 박혀있음. 후속 추가 시 분기 컴포넌트 패턴.
- **LLM 프롬프트 template** — slot format 출력 강제. format 결정 메타 prompt 는 후속 추가.

### 4.2 코드 영향

```jsx
// proto-algorithms.jsx (또는 추후 분리)
function LogicPanel({ item, lang }) {
  const format = item.logic?.format || 'slot';
  if (format === 'slot') return <SlotQuiz item={item} lang={lang} />;
  // 후속:
  // if (format === 'ordering') return <OrderingQuiz ... />;
  // if (format === 'state-first') return <StateFirstQuiz ... />;
  return <UnsupportedFormat format={format} />;
}
```

### 4.3 운영 영향

- LLM 프롬프트 비용 — 논리 구조 quiz 1개 = 추가 1 호출 (Pre-solve · Trace narration · follow-up 과 별개). 매일 1문제 → 매일 +1 호출. open-kknaks 라 비용 0.
- 콘텐츠 생성 실패 시 §4.4 자리 누락 — 프론트는 `LogicPanel` 빈 안내 박음. Pre-solve · Trace 는 정상 작동.

### 4.4 위험 + 완화

| 위험 | 완화 |
|---|---|
| LLM 이 format 잘못 선택 (예: DP 문제에 slot) | quiz 자체는 작동, 학습 효과만 어색. 이상하면 수동 재생성 트리거 |
| slot 으로 cover 안 되는 패턴 (재귀) 의 §4.4 누락 | Pre-solve · Trace 는 정상. §4.4 자리에 "이 패턴은 후속 format 지원" 안내 |
| MVP 시퀀스 (~50 문제) 가 ordering·state-first 가 필요한 패턴에 도달 | NeetCode 150 시퀀스 시작부는 array/hash 위주 → 50일 안에 ordering 구현 가능 |
| LLM 이 정답 코드를 자체 생성 (hallucination) | **§2.2 의 추출 단계** — 정답 라인은 neetcode-gh 코드에서 *그대로* 박힘. LLM 응답에서 정답 코드를 받지 않음 (distractor 만) |
| LLM 의 distractor 가 우연히 정답과 동일 | 추출 단계 후 dedup — distractor 가 정답 라인과 일치하면 LLM 재요청 또는 buckle (slot 의 옵션 수가 부족하면 그대로 진행) |

### 4.5 향후 확장 일정 (대략)

| 시점 | format 추가 |
|---|---|
| MVP 출시 | `slot` 만 |
| ~Day 50 (tree·graph 진입 직전) | `ordering` 추가 |
| ~Day 100 (DP 진입) | `state-first` 추가 |

format 추가 시 작업: (1) prompt template, (2) 컴포넌트 신설, (3) spec-07 enum 확장, (4) 매트릭스 row 보강.

### 4.6 spec-07 영향

```yaml
# spec-07 schema (논리 구조 부분)
logic:
  format: !enum [slot, ordering, state-first]  # MVP: slot만
  # format=slot 일 때:
  slots: [{ label, indent, options: [{ code, type, why }] }]
  # format=ordering 일 때:
  steps: [{ id, code, correct_pos, why }]
  # format=state-first 일 때:
  stages: [{ name, label, options: [{ code, type, why }] }]
```

기존 항목들 yaml 은 그대로 호환 (format 필드 보고 분기).
