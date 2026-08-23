---
created: '2026-05-07'
date: '2026-05-07'
day: Day 05
difficulty: medium
id: A-005
source:
  curated_in:
  - neetcode150
  number: 347
  platform: leetcode
  slug: top-k-frequent-elements
  url: https://leetcode.com/problems/top-k-frequent-elements/
status: draft
tags:
- array
- hash-table
- divide-and-conquer
- sorting
- heap-priority-queue
- bucket-sort
- counting
- quickselect
title:
  en: Top K Frequent Elements
  ko: 상위 K개 빈도 요소
today: false
type: algorithm
updated: '2026-05-07'
visible: true
---

# 상위 K개 빈도 요소

## Data

```yaml
problem:
  title:
    ko: 상위 K개 빈도 요소
    en: Top K Frequent Elements
  statement:
    ko: '정수 배열 nums와 정수 k가 주어졌을 때, 가장 자주 나타나는 k개의 요소를 반환하세요. 답은 어떤 순서로든 반환할 수 있습니다.


      팔로우업: 알고리즘의 시간 복잡도는 O(n log n)보다 나아야 합니다. 여기서 n은 배열의 크기입니다.'
    en: 'Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.


      Follow up: Your algorithm''s time complexity must be better than O(n log n), where n is the array''s size.'
  constraints:
  - 1 ≤ nums.length ≤ 10^5
  - -10^4 ≤ nums[i] ≤ 10^4
  - k is in the range [1, the number of unique elements in the array]
  - The answer is guaranteed to be unique
  io:
  - input: '[1,1,1,2,2,3]

      2'
    output: '[1,2]'
  - input: '[1]

      1'
    output: '[1]'
  - input: '[1,2,1,2,1,2,3,1,3,2]

      2'
    output: '[1,2]'
clarifying:
  items:
  - q:
      ko: 반환된 요소들의 순서가 중요한가요?
      en: Does the order of returned elements matter?
    type: good
    why:
      ko: 문제에서 '어떤 순서로든 반환할 수 있습니다'라고 명시되어 있으므로, 반환 순서는 상관없습니다.
      en: The problem explicitly states you may return the answer in any order, so sequence doesn't matter.
  - q:
      ko: 배열에 음수가 포함될 수 있나요?
      en: Can the array contain negative numbers?
    type: good
    why:
      ko: 제약 조건에서 -10^4 ≤ nums[i] ≤ 10^4이므로, 음수도 포함될 수 있습니다.
      en: The constraints show -10^4 ≤ nums[i] ≤ 10^4, so negative numbers are allowed.
  - q:
      ko: k가 항상 고유 요소의 개수 이하인가요?
      en: Is k always less than or equal to the number of unique elements?
    type: good
    why:
      ko: 제약 조건에서 k의 범위가 [1, 고유 요소의 개수]라고 명시되어 있습니다.
      en: The constraints explicitly state k is in the range [1, the number of unique elements].
  - q:
      ko: 가장 적게 나타나는 k개의 요소를 반환해야 하나요?
      en: Should we return the k least frequent elements?
    type: distractor
    why:
      ko: 아니요. 문제는 '가장 자주 나타나는' k개의 요소를 요청합니다.
      en: No. The problem asks for the k most frequent elements, not the least frequent.
  - q:
      ko: 값이 같은 요소들을 구분해야 하나요?
      en: Do we need to distinguish duplicate values as separate elements?
    type: distractor
    why:
      ko: 아니요. 배열에서 중복된 값은 같은 요소입니다. 우리는 고유한 값의 빈도를 세어야 합니다.
      en: No. Duplicate values in the array are the same element. We count frequency of unique values.
approach:
  items:
  - name:
      ko: 버킷 정렬 (빈도 기반)
      en: Bucket Sort (Frequency-based)
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 요소의 빈도를 세고, 빈도를 인덱스로 하는 버킷 배열을 만들어 높은 빈도부터 수집합니다. 팔로우업 제약을 만족하며 최적입니다.
      en: Count frequencies, create buckets indexed by frequency, then collect from highest to lowest. Achieves O(n) and satisfies the follow-up constraint.
  - name:
      ko: 최소 힙 (Min Heap)
      en: Min Heap
    complexity: O(n log k) time / O(n) space
    type: good
    why:
      ko: 모든 요소의 빈도를 센 후 최소 힙으로 상위 k개를 유지합니다. k가 작을 때 효율적입니다.
      en: Count frequencies and maintain a min-heap of top k elements. Efficient when k is small.
  - name:
      ko: 빈도순 정렬
      en: Sort by Frequency
    complexity: O(n log n) time / O(n) space
    type: distractor
    why:
      ko: 모든 요소를 빈도순으로 정렬한 후 상위 k개를 선택합니다. 간단하지만 O(n log n)이므로 팔로우업을 위반합니다.
      en: Sort all elements by frequency and pick the top k. Simple but O(n log n) violates the follow-up.
  - name:
      ko: 퀵셀렉트
      en: Quick Select
    complexity: O(n) avg / O(n²) worst / O(n) space
    type: distractor
    why:
      ko: 평균 O(n)이지만 최악의 경우 O(n²)이고, 구현이 복잡하므로 버킷 정렬이 선호됩니다.
      en: O(n) average but O(n²) worst case, with more complex implementation than bucket sort.
logic:
  format: slot
  slots:
  - label:
      ko: 빈도 카운터 초기화
      en: Initialize frequency counter
    indent: 0
    options:
    - code: count = {}
      type: good
      why:
        ko: 빈 딕셔너리를 만들어 각 요소의 등장 횟수를 저장합니다.
        en: Create an empty dictionary to store how many times each element appears.
    - code: count = []
      type: distractor
      why:
        ko: 리스트는 음수 인덱스를 사용할 수 없어 음수 요소를 저장하기 어렵습니다.
        en: Lists don't handle negative indices well for storing negative numbers as keys.
    - code: count = set()
      type: distractor
      why:
        ko: 집합은 요소만 저장하고 빈도 값을 저장할 수 없습니다.
        en: Sets only store unique elements, not frequency counts.
  - label:
      ko: 빈도 버킷 배열 초기화
      en: Initialize frequency bucket array
    indent: 0
    options:
    - code: freq = [[] for i in range(len(nums) + 1)]
      type: good
      why:
        ko: 빈도(0부터 n까지)를 인덱스로 하는 버킷 배열을 만듭니다. 각 버킷은 그 빈도를 가진 요소들을 저장합니다.
        en: Create buckets indexed by frequency. Size is len(nums) + 1 to accommodate frequencies 0 to n.
    - code: freq = [[] for i in range(len(nums))]
      type: distractor
      why:
        ko: 크기가 len(nums)이면, 최대 빈도 n을 저장할 수 없어 인덱스 오류가 발생합니다.
        en: Size of len(nums) would cause index out of bounds when storing frequency n.
    - code: freq = {}
      type: distractor
      why:
        ko: 딕셔너리는 빈도를 직접 인덱싱하기 어렵고, 느린 룩업이 필요합니다.
        en: Dictionaries don't provide the efficient O(1) indexed access that arrays do.
  - label:
      ko: 배열을 순회하며 빈도 계산
      en: Count frequencies by iterating array
    indent: 1
    options:
    - code: count[n] = 1 + count.get(n, 0)
      type: good
      why:
        ko: 각 요소 n의 빈도를 증가시킵니다. get(n, 0)으로 첫 등장 시 0에서 시작하여 1이 됩니다.
        en: Increment the count for each element. Using get(n, 0) ensures first occurrence starts at 1.
    - code: count[n] = count.get(n, 1) + 1
      type: distractor
      why:
        ko: 기본값이 1이면, 첫 등장이 2로 카운트되어 모든 빈도가 1 증가합니다.
        en: Starting with default 1 causes first occurrences to be counted as 2.
    - code: count[n] += 1
      type: distractor
      why:
        ko: 첫 등장하는 요소는 키가 존재하지 않아 KeyError가 발생합니다.
        en: Fails on first occurrence because the key doesn't exist yet.
  - label:
      ko: 빈도별로 요소를 버킷에 추가
      en: Add elements to frequency buckets
    indent: 1
    options:
    - code: freq[c].append(n)
      type: good
      why:
        ko: 각 요소를 그 빈도에 해당하는 버킷에 추가합니다. 같은 빈도의 요소들이 같은 버킷에 모입니다.
        en: Append each element to the bucket at index equal to its frequency. Groups elements by frequency.
    - code: freq[n].append(c)
      type: distractor
      why:
        ko: 요소와 빈도가 바뀌어서, 요소 값을 인덱스로 사용하면 음수나 큰 값에서 오류가 발생합니다.
        en: Swapping element and frequency causes index errors for negative or large values.
    - code: freq[c] = n
      type: distractor
      why:
        ko: 할당 대신 append를 사용해야 같은 빈도의 여러 요소를 모두 저장할 수 있습니다.
        en: Assignment overwrites previous elements; we need append to store multiple elements per bucket.
  - label:
      ko: 높은 빈도부터 역순으로 순회 및 수집
      en: Iterate from highest to lowest frequency and collect
    indent: 0
    options:
    - code: 'for i in range(len(freq) - 1, 0, -1):'
      type: good
      why:
        ko: 가장 높은 빈도(len(freq)-1)부터 빈도 1까지 역순으로 순회하여 상위 k개의 요소를 수집합니다.
        en: Loop from highest frequency down to 1, collecting elements until we have k of them.
    - code: 'for i in range(len(freq)):'
      type: distractor
      why:
        ko: 0부터 시작하면 가장 적은 빈도의 요소부터 수집하게 되어 결과가 틀립니다.
        en: Starting from 0 collects least frequent elements first, giving wrong results.
    - code: 'for i in range(len(freq) - 1, -1, -1):'
      type: distractor
      why:
        ko: -1까지 포함하면 빈도 0의 빈 버킷도 순회하여 불필요합니다.
        en: Including -1 iterates over empty buckets and is inefficient.
trace:
  code:
  - 'class Solution:'
  - '    def topKFrequent(self, nums: List[int], k: int) -> List[int]:'
  - '        count = {}'
  - '        freq = [[] for i in range(len(nums) + 1)]'
  - ''
  - '        for n in nums:'
  - '            count[n] = 1 + count.get(n, 0)'
  - '        for n, c in count.items():'
  - '            freq[c].append(n)'
  - ''
  - '        res = []'
  - '        for i in range(len(freq) - 1, 0, -1):'
  - '            res += freq[i]'
  - '            if len(res) == k:'
  - '                return res'
  - '                '
  - ''
  - '        # O(n)'
  cases:
  - input: '[1,1,1,2,2,3]

      2'
    expected: '[1,2]'
  - input: '[1]

      1'
    expected: '[1]'
  - input: '[1,2,1,2,1,2,3,1,3,2]

      2'
    expected: '[1,2]'
  worked_example:
    input: '[1,1,1,2,2,3]

      2'
    steps:
    - ko: '빈도 계산: count = {1: 3, 2: 2, 3: 1} (1은 3번, 2는 2번, 3은 1번 등장)'
      en: 'Count frequencies: count = {1: 3, 2: 2, 3: 1} (1 appears 3 times, 2 twice, 3 once)'
    - ko: '빈도 버킷 채우기: freq[3] = [1], freq[2] = [2], freq[1] = [3]'
      en: 'Populate buckets: freq[3] = [1], freq[2] = [2], freq[1] = [3]'
    - ko: 'i=5부터 i=1까지 순회: freq[5]~freq[4]는 비어있고, freq[3] = [1]을 추가 → res = [1]'
      en: 'Iterate from i=5 down: freq[5-4] empty, add freq[3] = [1] → res = [1]'
    - ko: freq[2] = [2]를 추가 → res = [1, 2], len(res) = 2 = k이므로 [1, 2] 반환
      en: Add freq[2] = [2] → res = [1, 2], len(res) = k, so return [1, 2]
    answer: '[1,2]'
solution:
  code: "class Solution:\n    def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n        count = {}\n        freq = [[] for i in range(len(nums) + 1)]\n\n        for n in nums:\n            count[n] = 1 + count.get(n, 0)\n        for n, c in count.items():\n            freq[c].append(n)\n\n        res = []\n        for i in range(len(freq) - 1, 0, -1):\n            res += freq[i]\n            if len(res) == k:\n                return res\n                \n\n        # O(n)\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 최소 힙을 사용하여 이 문제를 풀 수 있을까요? 시간 복잡도는 얼마일까요?
    en: Can you solve this with a min-heap? What's the time complexity?
  - ko: 'k가 매우 작을 때 (예: k=2, 고유 요소 100개) 어떤 접근이 더 효율적할까요?'
    en: If k is very small compared to unique elements, which approach is more efficient?
  - ko: 이 알고리즘을 수정하여 k개의 가장 적게 나타나는 요소를 찾을 수 있을까요?
    en: How would you modify this to find the k least frequent elements?
```