---
id: adr-09
type: adr
title: Trace 시각화 = 입력 케이스 리스트 + 예시 1개 (LLM 생성, 단순)
status: draft
created: 2026-05-05
updated: 2026-05-05
sources:
  - "[[planning-03-algorithm-daily-tab]]"
  - "[[adr-04-llm-via-open-kknaks]]"
tags: [adr, algorithms, trace, simple]
---

# Trace 시각화 = 입력 케이스 리스트 + 예시 1개 (LLM 생성)

## Summary

planning-03 §4.5 Trace 의 본질은 **학습자가 머릿속으로 dry-run** 하는 것. UI 가 step-by-step walk-through 해주면 그 행동 자체가 학습 가치를 빼앗음. 그래서 §4.5 UI 는:

- 정답 코드 표시 (read-only)
- 머릿속으로 따라갈 **입력 케이스 N개** (3개 권고)
- 그 중 1개의 **walked-through 예시** (펼침, 답안지)

까지만. step-by-step interactive stepper · 콜스택 시각화 · Predict 마커 · subprocess sandbox · sys.settrace 모두 **폐기**.

---

## 1. Context

이전 검토 (이 ADR 의 초안) 에서 sys.settrace 자동 추출로 100% 정확 trace yaml 생성을 제안. 인프라:

- subprocess sandbox + timeout + RLIMIT_AS + import whitelist
- core region 판별 휴리스틱
- LLM narration · Predict 마커 위치 결정

검토 후 두 가지 이유로 폐기:

1. **학습 가치 위반** — 본 product 의 본질은 *학습자가 머릿속으로 dry-run* 하는 것. UI 가 stepper 로 walk-through 해주면 학습자는 *그냥 보기만* 함. 머릿속 추적 근육이 안 길러짐. 단순 reading 도구로 전락.
2. **인프라 과함** — 본인 사이트 MVP 에 production-level sandbox 는 ROI 부적합. NeetCode 150 well-known 문제라 LLM hallucination 위험 5% 이하, 본인이 보고 fix 가능.

---

## 2. Decision

### 2.1 trace yaml schema (단순)

```yaml
trace:
  code: |
    def two_sum(nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
  cases:
    - { input: "nums=[2,7,11,15], target=9", expected: "[0, 1]" }
    - { input: "nums=[3,2,4], target=6",     expected: "[1, 2]" }
    - { input: "nums=[3,3], target=6",       expected: "[0, 1]" }
  worked_example:
    input: "nums=[2,7,11,15], target=9"
    steps:
      - { ko: "i=0, num=2 → complement=7, seen={} → 7 ∉ seen → seen[2]=0", en: "..." }
      - { ko: "i=1, num=7 → complement=2, seen={2:0} → 2 ∈ seen → return [0, 1]", en: "..." }
    answer: "[0, 1]"
```

step text 는 자유 형식 한 줄 (라인 번호·콜스택 시각화 X — 학습자가 코드 보고 알아서 매칭).

### 2.2 LLM (open-kknaks) 이 한 번에 생성

입력: 솔루션 코드 + LeetCode `exampleTestcases` →
출력: `cases` 배열 + `worked_example` (1개 케이스에 대해 step text + 정답)

cases 의 input 은 LeetCode `exampleTestcases` 활용 (source 가 있으면 source). worked_example step text 는 LLM 전적.

### 2.3 UI 단순화

- 코드 블록 (read-only)
- 케이스 리스트 — 각 행: 입력 + 기대 출력 (학습자가 머릿속 dry-run 대상)
- "예시 walked-through 보기" 버튼 — 펼치면 step text 들 + 정답

step-by-step 인터랙션 X. 콜스택 viz X. Predict 마커 X. 학습자가 막히면 worked_example 펼쳐서 답안지 확인.

---

## 3. Alternatives Considered

### 3.1 step-by-step interactive UI (sys.settrace · sandbox · Predict markers)

- **장점**: 변수값·콜스택 정확도 100%, walking-through assist
- **단점**:
  - **학습 가치 빼앗김** — UI 가 walk-through 해주면 학습자가 굴리지 않음. 본 product 본질 위반
  - subprocess sandbox · timeout · import whitelist = production-level 인프라. 본인 사이트 MVP 에 과함
  - 운영 위험 (외부 lib·import 화이트리스트 관리 등)
- **기각**: 학습 가치 + 인프라 비용 모두 잘못된 방향.

### 3.2 (현 결정) 단순 list + 예시

- **장점**: 학습자가 진짜로 머릿속으로 굴림 (학습 가치). 인프라 0. LLM 자유 형식 text 충분.
- **단점**: worked_example 의 LLM hallucination 가능성 ~5% (NeetCode 150 well-known 문제 한정). 본인 사이트라 보고 fix 가능.
- **수용**: 학습 가치 우선. 정확도 issue 가 매일 누적되면 사후 추가.

---

## 4. Consequences

### 4.1 즉시 효과

- **proto-algorithms.jsx** `TracePanel` — stepper / 콜스택 패널 / 변수표 / Predict 마커 / Solution reveal 통째 제거. 코드 + cases list + worked_example (펼침) 만.
- **spec-07** trace yaml schema — 단순 text 기반 (`code`, `cases`, `worked_example`).
- subprocess sandbox 인프라 **불필요**.

### 4.2 운영 영향

- LLM 호출 1회 (cases + worked_example 같이) — open-kknaks 비용 0.
- 정확도 review 는 본인이 매일 1문제 보고 검수.

### 4.3 향후 확장

- 정확도 issue 가 매일 1문제 누적 후 felt 시 sys.settrace 자동 추출 옵션 부활 검토 — 그때 별도 ADR.
- 또는 LLM 호출 후 worked_example step 을 *간단 검증* (정답 일치 여부만) — overhead 적음.
