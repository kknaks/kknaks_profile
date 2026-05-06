---
id: A-001
type: algorithm
title:
  ko: Two Sum
  en: Two Sum
date: 2026-05-05
day: Day 01
source:
  platform: leetcode
  number: 1
  slug: two-sum
  url: https://leetcode.com/problems/two-sum/
  curated_in: [neetcode150, blind75]
difficulty: easy
tags: [array, hash]
today: true
status: draft
visible: true
created: 2026-05-05
updated: 2026-05-05
---

# Two Sum

## Data

```yaml
problem:
  title:
    ko: Two Sum
    en: Two Sum
  statement:
    ko: 정렬되지 않은 정수 배열 nums 와 정수 target 이 주어질 때, nums[i] + nums[j] == target 인 두 인덱스 [i, j] 를 반환하라. 정답이 정확히 1쌍 존재한다고 가정. 같은 원소를 두 번 사용할 수 없음.
    en: Given an unsorted int array nums and target, return indices [i, j] such that nums[i] + nums[j] == target. Exactly one solution exists. Cannot use the same element twice.
  constraints:
    - "2 ≤ nums.length ≤ 1e4"
    - "−1e9 ≤ nums[i], target ≤ 1e9"
    - "정답이 정확히 1쌍 존재"
  io:
    - { input: "nums = [2, 7, 11, 15]\ntarget = 9", output: "[0, 1]" }
    - { input: "nums = [3, 2, 4]\ntarget = 6",     output: "[1, 2]" }
    - { input: "nums = [3, 3]\ntarget = 6",         output: "[0, 1]" }

clarifying:
  items:
    - q: { ko: "음수 포함 가능?", en: "Can values be negative?" }
      type: good
      why:
        ko: "범위 확인 — hash 키로 음수 처리는 파이썬에선 OK 지만 다른 언어에선 영향"
        en: "Range check — fine in Python hash keys, matters in other langs"
    - q: { ko: "같은 원소를 두 번 사용 가능?", en: "Can we reuse the same element?" }
      type: good
      why:
        ko: "인덱스 i ≠ j 강제 — hash lookup 시 자기 자신 제외 처리"
        en: "Forces i ≠ j — exclude self in hash lookup"
    - q: { ko: "정답이 여러 개일 때 어떻게?", en: "What if multiple answers exist?" }
      type: distractor
      why:
        ko: '문제가 "정확히 1쌍" 명시 — 시간 낭비'
        en: 'Problem states "exactly one solution" — wastes time'
    - q: { ko: "오버플로 처리 필요?", en: "Need overflow handling?" }
      type: distractor
      why:
        ko: "파이썬은 임의 정밀도 — C++/Java 에서나 의미"
        en: "Python has arbitrary precision — only matters in C++/Java"
    - q: { ko: "입력이 정렬되어 있나?", en: "Is the input sorted?" }
      type: good
      why:
        ko: "정렬되어 있으면 two pointers 가 더 효율 — 접근이 바뀜"
        en: "If sorted, two pointers is more efficient — changes approach"
    - q: { ko: "배열 크기 제한?", en: "Array size limit?" }
      type: good
      why:
        ko: "메모리 사용 가능 여부 결정 — 1e4 면 hash 안전"
        en: "Determines memory feasibility — 1e4 is fine for hash"
    - q: { ko: "문자열도 입력으로 들어오나?", en: "Will strings come as input?" }
      type: distractor
      why:
        ko: "문제가 정수 배열 명시 — 무관한 질문"
        en: "Problem specifies int array — unrelated"

approach:
  items:
    - name: { ko: "Brute force (이중 loop)", en: "Brute force (nested loop)" }
      complexity: "O(n²) time / O(1) space"
      type: good
      why:
        ko: "모든 쌍 검사 — 면접에서 baseline 으로 한 번 언급, 실전 풀이는 X"
        en: "Check all pairs — mention as baseline, not the actual answer"
    - name: { ko: "Hash map (one-pass)", en: "Hash map (one-pass)" }
      complexity: "O(n) time / O(n) space"
      type: good
      why:
        ko: "target − nums[i] 를 키로 hash 에 저장. 표준 풀이."
        en: "Store target − nums[i] in hash. Canonical solution."
    - name: { ko: "Sort + two pointers", en: "Sort + two pointers" }
      complexity: "O(n log n)"
      type: distractor
      why:
        ko: "인덱스 반환이라 정렬 후 원본 인덱스 추적 필요 — 비실용적"
        en: "Index return → tracking original indices after sort — impractical"
    - name: { ko: "Binary search", en: "Binary search" }
      complexity: "O(n log n)"
      type: distractor
      why:
        ko: "입력이 정렬 안 되어 있어 적용 불가"
        en: "Input is unsorted — not applicable"
    - name: { ko: "Sliding window", en: "Sliding window" }
      complexity: "O(n)"
      type: distractor
      why:
        ko: "연속 부분 배열 패턴이 아니라 임의 두 원소 — 윈도우 무관"
        en: "Pattern is for contiguous subarrays, not arbitrary pairs"

logic:
  format: slot
  slots:
    - label: { ko: 초기화, en: Initialize }
      indent: 0
      options:
        - code: "seen = {}"
          type: good
          why:
            ko: "인덱스를 값에 매핑하는 빈 dict — O(n) hash 풀이의 핵심"
            en: "empty dict mapping value → index — core of O(n) hash approach"
        - code: "result = []"
          type: distractor
          why:
            ko: "문제는 단일 쌍 반환 — 누적 list 불필요"
            en: "problem returns a single pair — accumulator unnecessary"
        - code: "a = sorted(nums)"
          type: distractor
          why:
            ko: "정렬하면 인덱스 잃음 — 인덱스 반환 문제에 부적합"
            en: "sort loses original indices — unfit for index-return problem"
    - label: { ko: 반복문, en: Loop }
      indent: 0
      options:
        - code: "for num in nums:"
          type: distractor
          why:
            ko: "인덱스 못 잡음 — 결과 [i, j] 형태 반환 불가"
            en: "can't track index — can't return [i, j] form"
        - code: "for i, num in enumerate(nums):"
          type: good
          why:
            ko: "i + num 동시 추적 — canonical"
            en: "tracks both i and num — canonical pythonic form"
        - code: "for i in range(len(nums)):"
          type: distractor
          why:
            ko: "동작은 하지만 num 도 매번 인덱싱 — verbose"
            en: "works but indexes num each time — verbose"
    - label: { ko: 루프 안 — 보조값, en: In loop — helper }
      indent: 1
      options:
        - code: "complement = target - num"
          type: good
          why:
            ko: "필요한 짝꿍 값 — hash 에서 찾을 키"
            en: "the partner needed — key to look up in hash"
        - code: "pair_sum = nums[i] + num"
          type: distractor
          why:
            ko: '같은 인덱스 더하기 — "같은 원소 두 번 사용 금지" 위반'
            en: 'same-index sum — violates "no element twice" rule'
        - code: "mid = (i + len(nums)) // 2"
          type: distractor
          why:
            ko: "바이너리 서치용 mid — 무관한 패턴"
            en: "binary search mid — unrelated pattern"
    - label: { ko: 분기 조건, en: Branch condition }
      indent: 1
      options:
        - code: "if complement in seen:"
          type: good
          why:
            ko: "짝꿍이 이미 봤던 원소 중에 있나 — O(1) 체크"
            en: "has the partner been seen already? — O(1) check"
        - code: "if num == target / 2:"
          type: distractor
          why:
            ko: "특수 케이스만 잡음 — 일반화 X"
            en: "only catches special case — not general"
        - code: "if i + 1 < len(nums):"
          type: distractor
          why:
            ko: "바운드 체크일 뿐 — 답 못 찾음"
            en: "just a bound check — finds no answer"
    - label: { ko: 참일 때 — 결과 반환, en: On true — return }
      indent: 2
      options:
        - code: "return [seen[complement], i]"
          type: good
          why:
            ko: "짝꿍 인덱스 + 현재 인덱스 — 정답 형식"
            en: "partner index + current index — required form"
        - code: "return (complement, num)"
          type: distractor
          why:
            ko: "값 반환 — 문제는 인덱스 요구"
            en: "returns values — problem wants indices"
        - code: "result.append([seen[complement], i])"
          type: distractor
          why:
            ko: "한 쌍만 존재하는데 누적 — 즉시 반환이 정답"
            en: "one pair only — should return immediately, no accumulation"
    - label: { ko: 루프 끝부분 — 갱신, en: Loop tail — update }
      indent: 1
      options:
        - code: "seen[num] = i"
          type: good
          why:
            ko: "값 → 인덱스 — 다음 iter 들이 짝꿍 찾기 위함"
            en: "value → index map — so future iters can find partners"
        - code: "seen[i] = num"
          type: distractor
          why:
            ko: "키·값 뒤바뀜 — `complement in seen` 체크 무용"
            en: "key/value swapped — `complement in seen` check breaks"
        - code: "continue"
          type: distractor
          why:
            ko: "저장 안 함 — 다음 iter 가 짝꿍 못 찾음"
            en: "no store — future iters never find partners"
    - label: { ko: 루프 후 — 폴백 반환, en: After loop — fallback }
      indent: 0
      options:
        - code: "return []"
          type: good
          why:
            ko: "문제가 정답 보장하지만 안전한 default 반환"
            en: "problem guarantees a pair, but safe default return"
        - code: "pass"
          type: distractor
          why:
            ko: "함수가 암묵적 None 반환 — caller 처리 어려움"
            en: "function returns implicit None — hard for caller to handle"
        - code: 'raise ValueError("no pair")'
          type: distractor
          why:
            ko: "문제가 정답 보장 — 예외 불필요"
            en: "problem guarantees a pair — exception unnecessary"

trace:
  code:
    - "def two_sum(nums, target):"
    - "    seen = {}"
    - "    for i, num in enumerate(nums):"
    - "        complement = target - num"
    - "        if complement in seen:"
    - "            return [seen[complement], i]"
    - "        seen[num] = i"
    - "    return []"
  cases:
    - { input: "nums=[2,7,11,15], target=9", expected: "[0, 1]" }
    - { input: "nums=[3,2,4], target=6",     expected: "[1, 2]" }
    - { input: "nums=[3,3], target=6",       expected: "[0, 1]" }
  worked_example:
    input: "nums=[2,7,11,15], target=9"
    steps:
      - ko: "i=0, num=2 → complement=7, seen={} → 7 ∉ seen → seen[2]=0"
        en: "i=0, num=2 → complement=7, seen={} → 7 not in seen → seen[2]=0"
      - ko: "i=1, num=7 → complement=2, seen={2:0} → 2 ∈ seen → return [seen[2], 1] = [0, 1]"
        en: "i=1, num=7 → complement=2, seen={2:0} → 2 in seen → return [seen[2], 1] = [0, 1]"
    answer: "[0, 1]"

solution:
  code: |
    def two_sum(nums, target):
        seen = {}
        for i, num in enumerate(nums):
            c = target - num
            if c in seen:
                return [seen[c], i]
            seen[num] = i
  complexity:
    time: "O(n)"
    space: "O(n)"
  followup:
    - ko: "입력이 정렬되어 있다면? → two pointers 로 O(1) 공간"
      en: "If sorted? → two pointers in O(1) space"
    - ko: '"3 sum" 으로 확장? → outer loop + 2sum 으로 O(n²)'
      en: 'Extend to "3sum"? → outer loop + 2sum gives O(n²)'
    - ko: "여러 정답 가능하다면? → set 으로 모든 쌍 수집"
      en: "If multiple answers? → collect all pairs via set"
```
