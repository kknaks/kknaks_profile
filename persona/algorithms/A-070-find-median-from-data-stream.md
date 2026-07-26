---
created: '2026-07-26'
date: '2026-07-26'
day: Day 70
difficulty: hard
id: A-070
source:
  curated_in:
  - neetcode150
  number: 295
  platform: leetcode
  slug: find-median-from-data-stream
  url: https://leetcode.com/problems/find-median-from-data-stream/
status: draft
tags:
- two-pointers
- design
- sorting
- heap-priority-queue
- data-stream
title:
  en: Find Median from Data Stream
  ko: 데이터 스트림에서 중앙값 구하기
today: true
type: algorithm
updated: '2026-07-26'
visible: true
---

# 데이터 스트림에서 중앙값 구하기

## Data

```yaml
problem:
  title:
    ko: 데이터 스트림에서 중앙값 구하기
    en: Find Median from Data Stream
  statement:
    ko: '중앙값(median)은 정렬된 정수 리스트의 중간 값입니다. 리스트의 크기가 짝수인 경우 중간 값이 없으므로, 중앙값은 두 중간 값의 평균입니다.


      MedianFinder 클래스를 구현하세요:


      - MedianFinder()는 MedianFinder 객체를 초기화합니다.

      - void addNum(int num)은 데이터 스트림에서 정수 num을 데이터 구조에 추가합니다.

      - double findMedian()은 지금까지의 모든 원소의 중앙값을 반환합니다. 실제 답의 10^-5 이내의 오차가 허용됩니다.'
    en: 'The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.


      Implement the MedianFinder class:


      - MedianFinder() initializes the MedianFinder object.

      - void addNum(int num) adds the integer num from the data stream to the data structure.

      - double findMedian() returns the median of all elements so far. Answers within 10^-5 of the actual answer will be accepted.'
  constraints:
  - -10^5 ≤ num ≤ 10^5
  - There will be at least one element in the data structure before calling findMedian
  - At most 5 × 10^4 calls will be made to addNum and findMedian
  io:
  - input: '["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]

      [[],[1],[2],[],[3],[]]'
    output: '[null, null, null, 1.5, null, 2.0]'
clarifying:
  items:
  - q:
      ko: 두 힙을 '균형 잡혀있다'는 것은 정확히 무엇을 의미하나요?
      en: What does it mean for the two heaps to be 'balanced'?
    type: good
    why:
      ko: 두 힙의 크기 차이가 최대 1이어야 합니다. 이렇게 하면 중앙값에 상수 시간에 접근할 수 있습니다.
      en: The size difference should be at most 1. This ensures the median is always at the heap roots.
  - q:
      ko: 왜 작은 수들을 담는 힙에 음수를 저장하나요?
      en: Why do we negate numbers when storing them in the small heap?
    type: good
    why:
      ko: Python의 heapq는 최소 힙만 지원하므로, 음수를 사용하여 최대 힙을 구현합니다.
      en: Python's heapq only provides min heaps. Negating values simulates a max heap by flipping the comparison.
  - q:
      ko: 총 원소 개수가 홀수일 때와 짝수일 때 중앙값을 어떻게 다르게 반환하나요?
      en: How does the median calculation differ for odd vs even total counts?
    type: good
    why:
      ko: 홀수 개면 크기가 큰 힙의 최상단을 반환합니다. 짝수 개면 두 힙의 최상단 평균을 반환합니다.
      en: 'Odd: return the root of the larger heap. Even: return the average of both roots.'
  - q:
      ko: 새로운 수를 어느 힙에 먼저 추가할지 어떻게 결정하나요?
      en: How do we decide which heap to add a new number to?
    type: good
    why:
      ko: 큰 힙의 최솟값과 비교하여, 크면 큰 힙에, 아니면 작은 힙에 추가합니다.
      en: 'Compare with large''s minimum: if greater, add to large; otherwise add to small.'
  - q:
      ko: 정렬된 배열 대신 두 힙을 사용하는 이유는 무엇인가요?
      en: Why use two heaps instead of a sorted array?
    type: good
    why:
      ko: 정렬된 배열은 새 원소 삽입에 O(n) 시간이 필요하지만, 힙은 O(log n)입니다. 50k 작업에서는 큰 차이입니다.
      en: Sorted arrays require O(n) insertion time; heaps require only O(log n). With 50k operations, this is significant.
  - q:
      ko: 모든 작은 수를 최소 힙에, 큰 수를 최대 힙에 저장해야 하나요?
      en: Should small numbers go in a min heap and large numbers in a max heap?
    type: distractor
    why:
      ko: 반대입니다. 작은 수는 최대 힙에, 큰 수는 최소 힙에 저장하여 각각의 최상단에 빠르게 접근합니다.
      en: This is backwards. Small numbers go to a max heap (to quickly access the largest small number); large numbers go to a min heap (to quickly access the smallest large number).
  - q:
      ko: findMedian()의 시간 복잡도가 O(1)인 이유는 무엇인가요?
      en: Why is findMedian() O(1) time?
    type: distractor
    why:
      ko: 중앙값은 항상 두 힙의 최상단(root)에만 있으므로 검색이나 정렬 없이 상수 시간에 반환할 수 있습니다.
      en: The median is always at the heap roots; no traversal or reordering is needed.
  - q:
      ko: 힙 재조정 후 total count가 변하나요?
      en: Does rebalancing change the total number of elements?
    type: good
    why:
      ko: 아니요, 재조정은 한 힙에서 다른 힙으로 원소를 이동시킬 뿐, 총 개수는 변하지 않습니다.
      en: No, rebalancing just redistributes elements between heaps; total count remains unchanged.
approach:
  items:
  - name:
      ko: 두 힙 (최대 힙 + 최소 힙)
      en: Two Heaps (Max Heap + Min Heap)
    complexity: O(log n) addNum / O(1) findMedian
    type: good
    why:
      ko: 최소 힙은 큰 수들의 최솟값, 최대 힙은 작은 수들의 최댓값을 저장합니다. 균형을 유지하면 중앙값에 O(1)에 접근할 수 있습니다.
      en: The min heap stores the upper half's minimum; the max heap stores the lower half's maximum. Balanced heaps allow O(1) median lookup with O(log n) insertion.
  - name:
      ko: 정렬된 배열
      en: Sorted Array
    complexity: O(n) addNum / O(1) findMedian
    type: distractor
    why:
      ko: 배열에 새 원소를 정렬 순서대로 삽입하려면 O(n) 시간이 필요하므로 큰 데이터 스트림에는 비효율적입니다.
      en: Inserting into a sorted array requires finding the position and shifting elements, both O(n). Inefficient for large streams.
  - name:
      ko: 이진 검색 + 배열
      en: Binary Search + Array
    complexity: O(n) addNum / O(log n) findMedian
    type: distractor
    why:
      ko: 이진 검색으로 위치를 O(log n)에 찾을 수 있지만, 배열의 실제 삽입은 여전히 O(n) 시간이 필요합니다.
      en: Binary search finds position in O(log n), but array insertion still requires O(n) element shifts.
  - name:
      ko: 멀티셋 (트리 기반 정렬 집합)
      en: Multiset (Tree-based Sorted Set)
    complexity: O(log n) addNum / O(log n) findMedian
    type: distractor
    why:
      ko: 삽입은 O(log n)이지만, 중앙값을 찾기 위해 중간 원소에 접근해야 하므로 findMedian도 O(log n)입니다.
      en: While insertion is O(log n), accessing the median element requires traversing to the middle, making findMedian O(log n).
  - name:
      ko: 카운팅 정렬 / 버킷
      en: Counting Sort / Bucket
    complexity: O(1) addNum / O(k) findMedian (k=range)
    type: distractor
    why:
      ko: '범위가 제한되면 (예: 0-100) 각 값의 빈도를 저장할 수 있습니다. 하지만 범위가 넓으면 (−10^5 ~ 10^5) 메모리가 낭비됩니다.'
      en: Works for constrained ranges (see follow-up), but the full range [−10^5, 10^5] makes the bucket array impractically large.
logic:
  format: slot
  slots:
  - label:
      ko: 두 힙 초기화
      en: Initialize two heaps
    indent: 0
    options:
    - code: 'self.small, self.large = [], []  # maxHeap, minHeap (python default)'
      type: good
      why:
        ko: 비어있는 리스트로 작은 수 힙(small)과 큰 수 힙(large)을 초기화합니다.
        en: Initialize small and large as empty lists to represent the lower and upper halves.
    - code: self.small, self.large = set(), set()
      type: distractor
      why:
        ko: 집합으로는 heappush/heappop 연산을 수행할 수 없습니다.
        en: Sets don't support heappush/heappop; heaps must be lists.
    - code: self.heap = []
      type: distractor
      why:
        ko: 단일 힙으로는 중앙값을 효율적으로 구할 수 없습니다.
        en: A single heap cannot efficiently maintain both halves separately.
  - label:
      ko: 수를 적절한 힙에 추가
      en: Add number to appropriate heap
    indent: 1
    options:
    - code: 'if self.large and num > self.large[0]:'
      type: good
      why:
        ko: 큰 힙이 비어있지 않고 새 수가 큰 힙의 최솟값보다 크면 큰 힙에, 그렇지 않으면 작은 힙에 추가합니다.
        en: If large is non-empty and num > large's minimum, add to large (upper half); else add to small (lower half).
    - code: heapq.heappush(self.small, num); heapq.heappush(self.large, num)
      type: distractor
      why:
        ko: 모든 수를 두 힙에 모두 저장하는 것은 중복이며 공간 낭비입니다.
        en: Storing every number in both heaps wastes space and breaks the size invariant.
    - code: 'if num > 0: heapq.heappush(self.large, num) else: heapq.heappush(self.small, num)'
      type: distractor
      why:
        ko: 수의 부호가 아니라 현재 힙의 상태와 비교해야 합니다.
        en: Should compare with heap contents, not the number's sign.
  - label:
      ko: 작은 힙 크기 초과 시 재조정
      en: Rebalance small heap if oversized
    indent: 1
    options:
    - code: 'if len(self.small) > len(self.large) + 1:'
      type: good
      why:
        ko: 작은 힙이 큰 힙보다 2개 이상 크면, 작은 힙의 최댓값을 꺼내 큰 힙으로 옮깁니다.
        en: If small exceeds large's size by more than 1, move small's maximum to large.
    - code: 'if len(self.small) > len(self.large): val = -1 * heapq.heappop(self.small); heapq.heappush(self.large, val)'
      type: distractor
      why:
        ko: 조건이 느슨합니다. 크기 차이가 1일 때도 재조정하면 균형이 깨집니다.
        en: Condition is too loose; > 1 is required to maintain the invariant.
    - code: 'if len(self.small) > len(self.large): val = heapq.heappop(self.small); heapq.heappush(self.large, -1 * val)'
      type: distractor
      why:
        ko: heappop()으로 꺼낸 값은 이미 음수이므로, 다시 음수로 변환하면 안 됩니다.
        en: Values popped from small are already negated; don't negate them again.
  - label:
      ko: 큰 힙 크기 초과 시 재조정
      en: Rebalance large heap if oversized
    indent: 1
    options:
    - code: 'if len(self.large) > len(self.small) + 1:'
      type: good
      why:
        ko: 큰 힙이 작은 힙보다 2개 이상 크면, 큰 힙의 최솟값을 꺼내 작은 힙으로 옮깁니다.
        en: If large exceeds small's size by more than 1, move large's minimum to small.
    - code: 'if len(self.large) > len(self.small) + 1: val = heapq.heappop(self.large); heapq.heappush(self.small, val)'
      type: distractor
      why:
        ko: 큰 힙에서 꺼낸 양수 값을 음수로 변환하지 않으면 작은 힙의 부호 불일치가 발생합니다.
        en: Must negate the value before pushing to small to maintain the negation convention.
    - code: 'if len(self.large) >= len(self.small): val = heapq.heappop(self.large); heapq.heappush(self.small, -1 * val)'
      type: distractor
      why:
        ko: 조건이 느슨합니다. 크기 차이가 1일 때는 재조정할 필요가 없습니다.
        en: Condition should be >, not >=; difference of 1 is acceptable.
  - label:
      ko: 작은 힙이 크면 그 최댓값 반환
      en: Return small's max if it's larger
    indent: 1
    options:
    - code: 'if len(self.small) > len(self.large):'
      type: good
      why:
        ko: 작은 힙의 크기가 크면, 홀수 개이므로 중앙값은 작은 힙의 최댓값입니다.
        en: When small has one more element (odd total), the median is its maximum (at index 0 after negation).
    - code: 'if len(self.small) > len(self.large): return self.small[0]'
      type: distractor
      why:
        ko: self.small[0]은 음수이므로 반드시 -1을 곱해야 실제 값이 됩니다.
        en: self.small[0] is negative; must negate to get the actual value.
    - code: 'if len(self.small) >= len(self.large): return -1 * self.small[0]'
      type: distractor
      why:
        ko: 조건이 잘못되었습니다. 크기가 같을 때는 평균을 반환해야 합니다.
        en: Wrong condition; when equal, you should return the average, not small's max alone.
  - label:
      ko: 큰 힙이 크면 그 최솟값 반환
      en: Return large's min if it's larger
    indent: 1
    options:
    - code: 'elif len(self.large) > len(self.small):'
      type: good
      why:
        ko: 큰 힙의 크기가 크면, 홀수 개이므로 중앙값은 큰 힙의 최솟값입니다.
        en: When large has one more element (odd total), the median is its minimum (at index 0).
    - code: 'elif len(self.large) > len(self.small): return -1 * self.large[0]'
      type: distractor
      why:
        ko: 큰 힙의 값은 이미 양수이므로 음수로 변환하면 안 됩니다.
        en: Large heap values are positive; negating gives the wrong result.
    - code: 'elif len(self.large) >= len(self.small): return self.large[-1]'
      type: distractor
      why:
        ko: 힙의 마지막 요소는 임의의 위치이며 최솟값이 아닙니다. 최솟값은 index 0입니다.
        en: The last element in a heap is arbitrary; the minimum is always at index 0.
  - label:
      ko: 크기가 같으면 두 최상단의 평균 반환
      en: Return average of both roots if equal size
    indent: 1
    options:
    - code: return (-1 * self.small[0] + self.large[0]) / 2.0
      type: good
      why:
        ko: 두 힙의 크기가 같으면, 짝수 개이므로 중앙값은 작은 힙의 최댓값과 큰 힙의 최솟값의 평균입니다.
        en: When both heaps have equal size (even total count), the median is the average of their roots.
    - code: return (self.small[0] + self.large[0]) / 2.0
      type: distractor
      why:
        ko: self.small[0]은 음수이므로, -1을 곱해야 실제 최댓값이 됩니다.
        en: Must negate small[0] since it stores negative values.
    - code: return (-1 * self.small[0] + self.large[0]) / 2
      type: distractor
      why:
        ko: 정수 2로 나누면 정수 나눗셈이 되어 소수 부분이 손실됩니다. 2.0을 사용해야 합니다.
        en: Integer division with 2 loses precision; use 2.0 for float division.
trace:
  code:
  - 'class MedianFinder:'
  - '    def __init__(self):'
  - '        """'
  - '        initialize your data structure here.'
  - '        """'
  - '        # two heaps, large, small, minheap, maxheap'
  - '        # heaps should be equal size'
  - '        self.small, self.large = [], []  # maxHeap, minHeap (python default)'
  - ''
  - '    def addNum(self, num: int) -> None:'
  - '        if self.large and num > self.large[0]:'
  - '            heapq.heappush(self.large, num)'
  - '        else:'
  - '            heapq.heappush(self.small, -1 * num)'
  - ''
  - '        if len(self.small) > len(self.large) + 1:'
  - '            val = -1 * heapq.heappop(self.small)'
  - '            heapq.heappush(self.large, val)'
  - '        if len(self.large) > len(self.small) + 1:'
  - '            val = heapq.heappop(self.large)'
  - '            heapq.heappush(self.small, -1 * val)'
  - ''
  - '    def findMedian(self) -> float:'
  - '        if len(self.small) > len(self.large):'
  - '            return -1 * self.small[0]'
  - '        elif len(self.large) > len(self.small):'
  - '            return self.large[0]'
  - '        return (-1 * self.small[0] + self.large[0]) / 2.0'
  cases:
  - input: '["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]

      [[],[1],[2],[],[3],[]]'
    expected: '[null, null, null, 1.5, null, 2.0]'
  worked_example:
    input: '["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]

      [[],[1],[2],[],[3],[]]'
    steps:
    - ko: 'MedianFinder() 호출: small = [], large = [] 초기화'
      en: 'Constructor: initialize small = [], large = []'
    - ko: 'addNum(1): large가 비어있으므로 1을 small에 추가 → small = [-1], large = []'
      en: 'addNum(1): large is empty, add 1 to small → small = [-1], large = []'
    - ko: 'addNum(2): large가 비어있으므로 2를 small에 추가 → small = [-2, -1]. 재조정: len(small)=2 > len(large)+1=1이므로 max(small)=2를 꺼내 large로 이동 → small = [-1], large = [2]'
      en: 'addNum(2): large is empty, add 2 to small → small = [-2, -1]. Rebalance: move max of small (2) to large → small = [-1], large = [2]'
    - ko: 'findMedian(): len(small)=1, len(large)=1 → 평균 반환 = (-(-1) + 2) / 2 = 1.5'
      en: 'findMedian(): both heaps size 1 → return (1 + 2) / 2 = 1.5'
    - ko: 'addNum(3): large[0]=2, 3>2이므로 large에 추가 → large = [2, 3], small = [-1]. 재조정 불필요 (균형 유지)'
      en: 'addNum(3): 3 > large[0]=2, add to large → large = [2, 3], small = [-1]. Balanced.'
    - ko: 'findMedian(): len(large)=2 > len(small)=1 → large[0]=2 반환'
      en: 'findMedian(): large has more → return large[0] = 2.0'
    answer: '[null, null, null, 1.5, null, 2.0]'
solution:
  code: "class MedianFinder:\n    def __init__(self):\n        \"\"\"\n        initialize your data structure here.\n        \"\"\"\n        # two heaps, large, small, minheap, maxheap\n        # heaps should be equal size\n        self.small, self.large = [], []  # maxHeap, minHeap (python default)\n\n    def addNum(self, num: int) -> None:\n        if self.large and num > self.large[0]:\n            heapq.heappush(self.large, num)\n        else:\n            heapq.heappush(self.small, -1 * num)\n\n        if len(self.small) > len(self.large) + 1:\n            val = -1 * heapq.heappop(self.small)\n            heapq.heappush(self.large, val)\n        if len(self.large) > len(self.small) + 1:\n            val = heapq.heappop(self.large)\n            heapq.heappush(self.small, -1 * val)\n\n    def findMedian(self) -> float:\n        if len(self.small) > len(self.large):\n            return -1 * self.small[0]\n        elif len(self.large) > len(self.small):\n            return self.large[0]\n\
    \        return (-1 * self.small[0] + self.large[0]) / 2.0\n"
  complexity:
    time: O(log n) per addNum; O(1) per findMedian
    space: O(n) to store all elements
  followup:
  - ko: '모든 수가 [0, 100] 범위에 있다면? → 카운팅 배열 사용: addNum O(1), findMedian O(k) (k=범위)'
    en: 'If all numbers are in [0, 100]? → Use a count array: addNum becomes O(1), findMedian becomes O(range).'
  - ko: '99%의 수가 [0, 100] 범위에 있다면? → 하이브리드: [0, 100]은 카운팅, 범위 밖은 두 힙으로 처리'
    en: 'If 99% of numbers are in [0, 100]? → Hybrid approach: count array for [0, 100], two heaps for outliers.'
  - ko: 지속적으로 다양한 백분위수를 구해야 한다면? → 균형잡힌 이진 탐색 트리나 Skip List 고려
    en: If you need arbitrary percentiles efficiently? → Consider a balanced BST or skip list for O(log n) access to any rank.
```