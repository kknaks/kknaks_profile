---
created: '2026-07-17'
date: '2026-07-17'
day: Day 65
difficulty: easy
id: A-065
source:
  curated_in:
  - neetcode150
  number: 1046
  platform: leetcode
  slug: last-stone-weight
  url: https://leetcode.com/problems/last-stone-weight/
status: draft
tags:
- array
- heap-priority-queue
title:
  en: Last Stone Weight
  ko: 마지막 돌의 무게
today: true
type: algorithm
updated: '2026-07-17'
visible: true
---

# 마지막 돌의 무게

## Data

```yaml
problem:
  title:
    ko: 마지막 돌의 무게
    en: Last Stone Weight
  statement:
    ko: '정수 배열 stones가 주어지며, stones[i]는 i번째 돌의 무게입니다.


      돌들로 게임을 합니다. 매 차례마다 가장 무거운 두 돌을 선택하여 함께 부습니다. 가장 무거운 두 돌의 무게를 x와 y라 하고 x ≤ y라고 가정합니다. 부딪침의 결과는:


      x == y이면 두 돌 모두 파괴됩니다.

      x != y이면 무게 x인 돌은 파괴되고, 무게 y인 돌의 새로운 무게는 y - x가 됩니다.


      게임이 끝날 때 최대 한 개의 돌이 남습니다.


      마지막에 남은 돌의 무게를 반환하세요. 남은 돌이 없으면 0을 반환하세요.'
    en: 'You are given an array of integers stones where stones[i] is the weight of the i-th stone.


      We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x ≤ y. The result of this smash is:


      If x == y, both stones are destroyed.

      If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.


      At the end of the game, there is at most one stone left.


      Return the weight of the last remaining stone. If there are no stones left, return 0.'
  constraints:
  - 1 ≤ stones.length ≤ 30
  - 1 ≤ stones[i] ≤ 1000
  io:
  - input: '[2,7,4,1,8,1]'
    output: '1'
  - input: '[1]'
    output: '1'
clarifying:
  items:
  - q:
      ko: 가장 무거운 두 돌이 같은 무게라면?
      en: What happens if the two heaviest stones have equal weight?
    type: good
    why:
      ko: 두 돌이 같은 무게면 둘 다 파괴되어 배열에서 제거되므로, 종료 조건을 이해하는 데 중요합니다.
      en: Understanding this edge case clarifies the termination condition and helps design the algorithm correctly.
  - q:
      ko: 배열을 원본 그대로 수정해야 하나요, 아니면 복사본을 만들어야 하나요?
      en: Do we need to preserve the original array, or can we modify it?
    type: good
    why:
      ko: 문제에서 명시되지 않았으므로, 구현 자유도를 이해하는 데 필요합니다. 보통은 수정해도 괜찮습니다.
      en: This affects whether we need to create a copy; typically modifying the input is acceptable unless specified otherwise.
  - q:
      ko: 돌이 1개만 있으면 어떻게 되나요?
      en: What is the expected output if there is only one stone?
    type: good
    why:
      ko: edge case 처리를 확인하고 루프 조건을 올바르게 설계하는 데 필수적입니다.
      en: This edge case is critical for validating loop conditions and boundary handling.
  - q:
      ko: 가장 무거운 두 돌을 매번 찾을 때, 최대 얼마나 효율적으로 할 수 있을까요?
      en: What is the most efficient way to repeatedly find the two heaviest stones?
    type: good
    why:
      ko: 최대 힙(또는 우선순위 큐)을 사용하면 O(log n)에 가능하므로, 최적의 알고리즘 구조를 이끌어냅니다.
      en: This guides the interviewer to the heap/priority queue approach, which is O(log n) per operation.
  - q:
      ko: 파괴되는 돌들이 무엇인지 추적해야 하나요?
      en: Do we need to track which specific stones are destroyed?
    type: distractor
    why:
      ko: 문제는 오직 마지막 돌의 무게만 요구하므로, 돌의 정체성은 중요하지 않습니다.
      en: The problem only asks for the final weight, not the identity of stones, so this tracking is unnecessary.
  - q:
      ko: 돌을 부스르는 순서가 다르면 최종 결과가 달라질까요?
      en: Does the order in which we smash the stones affect the final result?
    type: distractor
    why:
      ko: 최종 결과는 항상 같습니다. 우리는 반드시 가장 무거운 두 돌을 선택해야 하므로, 순서는 알고리즘적 이유일 뿐 결과에는 영향을 주지 않습니다.
      en: The final result is always the same regardless of order; the algorithm's correctness depends on always picking the two heaviest.
approach:
  items:
  - name:
      ko: 최대 힙 (음수 저장)
      en: Max Heap (Using Negation)
    complexity: O(n log n) time / O(n) space
    type: good
    why:
      ko: Python의 heapq는 최소 힙이므로, 모든 값을 음수로 변환하면 최대 힙처럼 동작합니다. 매 반복마다 O(log n)에 두 돌을 추출하고 삽입할 수 있습니다.
      en: Python's heapq is a min-heap; negating values simulates a max-heap. Extraction and insertion are O(log n) per iteration.
  - name:
      ko: 정렬 시뮬레이션
      en: Sorting Simulation
    complexity: O(n² log n) time / O(n) space
    type: good
    why:
      ko: 매 차례마다 배열을 정렬하고 마지막 두 요소를 사용합니다. 동작하지만 매번 O(n log n) 정렬로 인해 느립니다.
      en: Sort the array each turn and take the two largest. Correct but inefficient due to repeated O(n log n) sorts.
  - name:
      ko: 그리디 + 두 포인터
      en: Greedy Two-Pointer
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 포인터로 가장 무거운 두 돌을 찾으려고 하면, 매번 선형 스캔이 필요하고 정렬 상태를 유지하기 어렵습니다.
      en: Linear scan to find max values each turn doesn't guarantee we always pick the correct two heaviest after modifications.
  - name:
      ko: 동적 프로그래밍 (가능한 모든 결과)
      en: Dynamic Programming (All Outcomes)
    complexity: O(2^n) time / O(n) space
    type: distractor
    why:
      ko: 이 문제는 시뮬레이션 문제이지, 부분 문제 최적 부분 구조를 가지지 않습니다. DP는 오버헤드만 늘립니다.
      en: This is a simulation problem with no optimal substructure; DP would be unnecessary overhead.
logic:
  format: slot
  slots:
  - label:
      ko: 모든 돌을 음수로 변환
      en: Negate all stones for max-heap simulation
    indent: 0
    options:
    - code: stones = [-s for s in stones]
      type: good
      why:
        ko: Python의 최소 힙을 최대 힙처럼 사용하기 위해 모든 값을 음수로 변환합니다.
        en: Convert to negative values so Python's min-heap behaves like a max-heap.
    - code: stones.sort(reverse=True)
      type: distractor
      why:
        ko: 정렬은 작동하지만, 매 반복마다 다시 정렬해야 해서 비효율적입니다.
        en: Sorting works but must be repeated each iteration; heap is more efficient.
    - code: stones = [s for s in stones]
      type: distractor
      why:
        ko: 변환이 없으므로 최소 힙이 최대 힙처럼 동작하지 않습니다.
        en: Without negation, the min-heap won't simulate a max-heap correctly.
  - label:
      ko: 배열을 힙 구조로 정렬
      en: Heapify the array
    indent: 0
    options:
    - code: heapq.heapify(stones)
      type: good
      why:
        ko: O(n) 시간에 배열을 힙 구조로 변환하여, 이후 추출과 삽입을 O(log n)으로 수행할 수 있게 합니다.
        en: Build heap structure in O(n) to enable O(log n) extractions and insertions.
    - code: 'heapq.heapify(stones, key=lambda x: x)'
      type: distractor
      why:
        ko: heapq.heapify는 key 인자를 지원하지 않습니다.
        en: heapq.heapify() does not accept a key parameter.
    - code: stones = sorted(stones)
      type: distractor
      why:
        ko: 정렬은 O(n log n)이고 매번 다시 해야 해서 비효율적입니다.
        en: Sorting is O(n log n) and must be repeated each turn.
  - label:
      ko: 두 개 이상의 돌이 남은 동안 반복
      en: Continue loop while 2+ stones remain
    indent: 0
    options:
    - code: 'while len(stones) > 1:'
      type: good
      why:
        ko: 2개 이상일 때만 쌍을 만들 수 있으므로, 1개 이하 남으면 루프를 종료해야 합니다.
        en: Can only smash two stones if 2+ remain; stop when 1 or 0 stones left.
    - code: 'while len(stones) > 0:'
      type: distractor
      why:
        ko: 1개 돌만 남아도 계속 루프를 실행하려고 하면, heappop을 2번 호출할 수 없습니다.
        en: Continuing with 1 stone would fail when trying to pop twice.
    - code: 'while stones:'
      type: distractor
      why:
        ko: 이것도 빈 배열까지 계속 실행하려고 하므로 잘못됩니다.
        en: This also runs until empty, causing a pop from an empty heap.
  - label:
      ko: 가장 무거운 돌 추출 (가장 음수)
      en: Extract the heaviest stone
    indent: 1
    options:
    - code: first = heapq.heappop(stones)
      type: good
      why:
        ko: heappop은 최소 힙에서 최소값(가장 음수)을 제거하고 반환하므로, 원래 배열에서 가장 무거운 돌입니다.
        en: heappop removes the minimum (most negative), which is the original maximum.
    - code: first = stones[0]
      type: distractor
      why:
        ko: 최상단 요소를 보기만 하고 제거하지 않으므로, 다음 반복에서 중복될 수 있습니다.
        en: Viewing the top element without removing it causes duplicates in next iteration.
    - code: first = max(stones) if stones else 0
      type: distractor
      why:
        ko: max()는 O(n)이고 힙의 이점을 잃습니다.
        en: Using max() is O(n) and defeats the purpose of using a heap.
  - label:
      ko: 두 번째로 무거운 돌 추출
      en: Extract the second heaviest stone
    indent: 1
    options:
    - code: second = heapq.heappop(stones)
      type: good
      why:
        ko: 다시 heappop으로 다음 최솟값(두 번째 가장 무거운 돌)을 추출합니다.
        en: Pop again to get the second heaviest stone from the remaining heap.
    - code: second = stones[0]
      type: distractor
      why:
        ko: 제거 없이 보기만 하므로 잘못된 상태입니다.
        en: Without removal, heap state becomes incorrect.
    - code: second = heapq.heappop(stones) or 0
      type: distractor
      why:
        ko: heappop은 0을 반환할 수 없으므로(우리는 음수를 저장), 이 or 0은 불필요합니다.
        en: heappop won't return 0 since we store negatives; the 'or 0' is unreachable.
  - label:
      ko: 다르면 차이를 힙에 삽입
      en: Push difference back if stones differ
    indent: 1
    options:
    - code: heapq.heappush(stones, first - second)
      type: good
      why:
        ko: 첫 번째에서 두 번째를 뺀 값이 남은 돌의 무게입니다. 음수 형태로 힙에 삽입하여 계속 비교할 수 있게 합니다.
        en: The difference (first - second) is the remaining stone's weight. Push it back into the heap for continued comparison.
    - code: heapq.heappush(stones, second - first)
      type: distractor
      why:
        ko: 뺄셈 순서가 반대입니다. first와 second는 모두 음수이므로 순서가 결과를 바꿉니다.
        en: Reversed subtraction gives the wrong weight difference.
    - code: heapq.heappush(stones, abs(first - second))
      type: distractor
      why:
        ko: abs()를 사용하면 양수가 되어 최소 힙 구조를 깨뜨립니다.
        en: Using abs() removes the negation and breaks the max-heap simulation.
  - label:
      ko: 마지막 돌의 무게 반환
      en: Return the weight of the last stone
    indent: 0
    options:
    - code: return abs(stones[0])
      type: good
      why:
        ko: append(0)은 빈 배열의 경우를 처리하고, abs()로 음수를 원래 값으로 변환합니다.
        en: append(0) handles the empty case; abs() converts the negated value back to the original weight.
    - code: return stones[0]
      type: distractor
      why:
        ko: 음수를 그대로 반환하고, 빈 배열일 때 에러가 발생합니다.
        en: Returns negative value and crashes if array is empty.
    - code: return stones[0] if stones else 0
      type: distractor
      why:
        ko: 음수 값을 반환하므로 잘못된 답입니다.
        en: Still returns a negative value, which is incorrect.
trace:
  code:
  - 'class Solution:'
  - '    def lastStoneWeight(self, stones: List[int]) -> int:'
  - '        stones = [-s for s in stones]'
  - '        heapq.heapify(stones)'
  - ''
  - '        while len(stones) > 1:'
  - '            first = heapq.heappop(stones)'
  - '            second = heapq.heappop(stones)'
  - '            if second > first:'
  - '                heapq.heappush(stones, first - second)'
  - ''
  - '        stones.append(0)'
  - '        return abs(stones[0])'
  - ''
  - '# There''s a private _heapify_max method.'
  - '# https://github.com/python/cpython/blob/1170d5a292b46f754cd29c245a040f1602f70301/Lib/heapq.py#L198'
  - 'class Solution(object):'
  - '    def lastStoneWeight(self, stones):'
  - '        heapq._heapify_max(stones)'
  - '        while len(stones) > 1:'
  - '            max_stone = heapq._heappop_max(stones)'
  - '            diff = max_stone - stones[0]'
  - '            if diff:'
  - '                heapq._heapreplace_max(stones, diff)'
  - '            else:'
  - '                heapq._heappop_max(stones)'
  - '        '
  - '        stones.append(0)'
  - '        return stones[0]'
  cases:
  - input: '[2,7,4,1,8,1]'
    expected: '1'
  - input: '[1]'
    expected: '1'
  worked_example:
    input: '[2,7,4,1,8,1]'
    steps:
    - ko: '돌을 음수로 변환: [-2, -7, -4, -1, -8, -1], 힙으로 구성'
      en: 'Convert to negatives: [-2, -7, -4, -1, -8, -1], build heap'
    - ko: '첫 반복: -8과 -7 추출 (원래 8과 7) → 차이 -1 삽입'
      en: 'Round 1: Pop -8, -7 (original 8, 7) → push -1 (difference)'
    - ko: '두 번째 반복: -4와 -2 추출 (원래 4와 2) → 차이 -2 삽입'
      en: 'Round 2: Pop -4, -2 (original 4, 2) → push -2 (difference)'
    - ko: '세 번째 반복: -2와 -1 추출 → 차이 -1 삽입, 계속해서 -1, -1, -1 중 두 개씩 제거'
      en: 'Round 3: Pop -2, -1 → push -1; continue with remaining -1 values'
    - ko: 마지막에 -1만 남고, abs(-1) = 1을 반환
      en: 'One stone remains: -1. Return abs(-1) = 1'
    answer: '1'
solution:
  code: "class Solution:\n    def lastStoneWeight(self, stones: List[int]) -> int:\n        stones = [-s for s in stones]\n        heapq.heapify(stones)\n\n        while len(stones) > 1:\n            first = heapq.heappop(stones)\n            second = heapq.heappop(stones)\n            if second > first:\n                heapq.heappush(stones, first - second)\n\n        stones.append(0)\n        return abs(stones[0])\n\n# There's a private _heapify_max method.\n# https://github.com/python/cpython/blob/1170d5a292b46f754cd29c245a040f1602f70301/Lib/heapq.py#L198\nclass Solution(object):\n    def lastStoneWeight(self, stones):\n        heapq._heapify_max(stones)\n        while len(stones) > 1:\n            max_stone = heapq._heappop_max(stones)\n            diff = max_stone - stones[0]\n            if diff:\n                heapq._heapreplace_max(stones, diff)\n            else:\n                heapq._heappop_max(stones)\n        \n        stones.append(0)\n        return stones[0]\n"
  complexity:
    time: O(n log n)
    space: O(n)
  followup:
  - ko: 돌의 무게가 음수일 수 있다면 어떻게 될까요? (코드 수정 필요)
    en: What if stone weights could be negative? How would the code change?
  - ko: 마지막 남은 돌의 원래 인덱스도 함께 반환해야 한다면? (id 추적 필요)
    en: How would you modify the solution to also return the index of the last remaining stone?
  - ko: 시뮬레이션 없이 최종 무게를 수학적으로 예측할 수 있을까요? (분할과 합의 원리)
    en: Can you predict the final stone's weight without simulation using a mathematical property?
```