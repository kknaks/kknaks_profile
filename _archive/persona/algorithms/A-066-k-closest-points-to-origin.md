---
created: '2026-07-18'
date: '2026-07-18'
day: Day 66
difficulty: medium
id: A-066
source:
  curated_in:
  - neetcode150
  number: 973
  platform: leetcode
  slug: k-closest-points-to-origin
  url: https://leetcode.com/problems/k-closest-points-to-origin/
status: draft
tags:
- array
- math
- divide-and-conquer
- geometry
- sorting
- heap-priority-queue
- quickselect
title:
  en: K Closest Points to Origin
  ko: 원점에서 가장 가까운 K개의 점
today: false
type: algorithm
updated: '2026-07-18'
visible: true
---

# 원점에서 가장 가까운 K개의 점

## Data

```yaml
problem:
  title:
    ko: 원점에서 가장 가까운 K개의 점
    en: K Closest Points to Origin
  statement:
    ko: 'X-Y 평면 위의 점들을 나타내는 배열 points가 주어졌을 때, points[i] = [xi, yi]이고 정수 k가 주어진다. 원점 (0, 0)에서 가장 가까운 k개의 점을 반환하시오.


      X-Y 평면 위의 두 점 사이의 거리는 유클리드 거리(√((x1 - x2)² + (y1 - y2)²))이다.


      답은 어떤 순서로든 반환할 수 있다. 답은 순서를 제외하고는 유일하다고 보장된다.'
    en: 'Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).


      The distance between two points on the X-Y plane is the Euclidean distance (i.e., √((x1 - x2)² + (y1 - y2)²)).


      You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).'
  constraints:
  - 1 ≤ k ≤ points.length ≤ 10^4
  - -10^4 ≤ xi, yi ≤ 10^4
  io:
  - input: '[[1,3],[-2,2]]

      1'
    output: '[[-2,2]]'
  - input: '[[3,3],[5,-1],[-2,4]]

      2'
    output: '[[3,3],[-2,4]]'
clarifying:
  items:
  - q:
      ko: 반환된 점들의 순서가 중요한가?
      en: Does the order of returned points matter?
    type: good
    why:
      ko: 문제에서 '어떤 순서로든 반환할 수 있다'고 명시되어 있으므로 정렬 불필요.
      en: The problem explicitly states 'You may return the answer in any order', so sorting is not required.
  - q:
      ko: 거리 계산 시 제곱근을 구해야 하는가?
      en: Do we need to calculate the square root when computing distance?
    type: good
    why:
      ko: 제곱근은 단조증가 함수이므로 √(x² + y²)와 x² + y²는 같은 순서를 유지한다.
      en: Square root is monotonically increasing, so √(x² + y²) and x² + y² maintain identical ordering.
  - q:
      ko: 여러 점이 동일한 거리에 있을 수 있는가?
      en: Can multiple points have the same distance?
    type: good
    why:
      ko: 문제에서 답이 유일하다고 보장하므로 같은 거리로 인한 tie-breaking 불필요.
      en: The problem guarantees the answer is unique, so tie-breaking between equal distances is unnecessary.
  - q:
      ko: k가 배열 길이와 같으면 모든 점을 반환해야 하는가?
      en: If k equals points.length, should we return all points?
    type: good
    why:
      ko: 제약조건에서 k ≤ points.length이므로 k = n인 경우 모든 점을 반환하면 된다.
      en: The constraint ensures k ≤ points.length, so returning all points when k equals array length is correct.
  - q:
      ko: 음수 좌표도 거리 계산에 올바르게 처리되는가?
      en: Are negative coordinates correctly handled?
    type: good
    why:
      ko: 거리 계산에서 제곱을 사용하므로 x² + y²는 음수 부호를 자동으로 처리한다.
      en: Squaring in distance calculation naturally handles negative values since negative² = positive.
  - q:
      ko: 원본 배열을 수정할 수 있는가?
      en: Can we modify the original points array?
    type: distractor
    why:
      ko: 문제에서 명시하지 않았지만, 인터뷰에서는 보통 원본 수정 불가를 선호한다.
      en: Not explicitly stated; interviews typically prefer non-destructive solutions.
  - q:
      ko: k = 0인 경우도 처리해야 하는가?
      en: Do we need to handle the case where k = 0?
    type: distractor
    why:
      ko: 제약조건에서 k ≥ 1이므로 k = 0은 입력되지 않는다.
      en: The constraint specifies k ≥ 1, so k = 0 is never provided as input.
approach:
  items:
  - name:
      ko: 최소 힙 (Min Heap)
      en: Min Heap
    complexity: O(n log n) time / O(n) space
    type: good
    why:
      ko: 모든 점의 거리를 힙에 저장하고 k번 추출한다. 구현이 간단하고 직관적이다.
      en: Build a heap with all distances, then pop k times. Simple, intuitive, and reliable for general k values.
  - name:
      ko: 정렬 (Sorting)
      en: Sorting
    complexity: O(n log n) time / O(1) space
    type: good
    why:
      ko: 모든 점의 거리를 계산하여 정렬한 후 처음 k개를 반환한다. 같은 시간복잡도이면서 공간 효율이 좋다.
      en: Calculate distances, sort, return first k. Same time complexity but better space efficiency excluding output.
  - name:
      ko: 최대 힙 (크기 K)
      en: Max Heap (Size K)
    complexity: O(n log k) time / O(k) space
    type: good
    why:
      ko: k개의 점만 힙에 유지하므로 k가 작을 때 가장 효율적이다.
      en: Maintain only k elements in a max-heap. Most efficient when k is significantly smaller than n.
  - name:
      ko: 퀵셀렉트 (QuickSelect)
      en: QuickSelect
    complexity: O(n) average / O(n²) worst-case time
    type: distractor
    why:
      ko: k번째 거리를 찾아 분할한다. 평균은 좋지만 최악의 경우가 있고 구현이 복잡하다.
      en: Find kth smallest distance via partitioning. Best average-case but complex implementation and poor worst-case.
  - name:
      ko: 브루트 포스 (모든 점 순회)
      en: Brute Force (Full Scan)
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 모든 점을 반복 비교하여 최소값을 찾는다. 매우 비효율적이고 실무에서 사용하지 않는다.
      en: Compare all pairs repeatedly to find minimums. Extremely inefficient and impractical.
logic:
  format: slot
  slots:
  - label:
      ko: 힙 초기화
      en: Initialize heap
    indent: 0
    options:
    - code: minHeap = []
      type: good
      why:
        ko: 거리와 좌표 정보를 저장할 빈 리스트를 생성한다.
        en: Create empty list to store (distance, x, y) tuples.
    - code: minHeap = ()
      type: distractor
      why:
        ko: 튜플은 append 메서드가 없어서 요소를 추가할 수 없다.
        en: Tuples lack append method; dynamic growth is impossible.
    - code: 'minHeap = {x: y for x, y in points}'
      type: distractor
      why:
        ko: 딕셔너리는 거리 값을 우선순위로 유지하지 못한다.
        en: Dictionaries cannot prioritize by distance value.
  - label:
      ko: 각 점의 거리 계산
      en: Calculate squared distance
    indent: 1
    options:
    - code: dist = (x ** 2) + (y ** 2)
      type: good
      why:
        ko: 원점 (0, 0)으로부터의 거리를 제곱 형태로 계산한다. 제곱근은 순서 보존에 불필요하다.
        en: Compute x² + y² for each point. Square root omitted since ordering is preserved.
    - code: dist = (x ** 2 + y ** 2) ** 0.5
      type: distractor
      why:
        ko: 제곱근 계산은 불필요하고 느리다. 이미 순서는 같으므로 낭비다.
        en: Square root is unnecessary and slower; ordering already matches.
    - code: dist = abs(x) + abs(y)
      type: distractor
      why:
        ko: 이것은 맨해튼 거리이며 유클리드 거리와 다르다.
        en: This is Manhattan distance, not Euclidean distance.
  - label:
      ko: 거리-좌표 튜플을 힙에 추가
      en: Append tuple to heap
    indent: 1
    options:
    - code: minHeap.append((dist, x, y))
      type: good
      why:
        ko: 거리를 첫 요소로 하는 튜플을 추가하면 파이썬 힙이 거리 기준으로 자동 정렬된다.
        en: Placing distance first makes Python's heap sort by distance when heapified.
    - code: minHeap.append((x, y, dist))
      type: distractor
      why:
        ko: 거리가 마지막 원소면 힙이 x 좌표 기준으로 정렬되어 원하는 동작이 아니다.
        en: Distance last causes heap to sort by x-coordinate first.
    - code: minHeap.append([dist, x, y])
      type: distractor
      why:
        ko: 힙 요소는 튜플을 권장한다. 리스트는 뮤터블이고 비교 시 예기치 않은 동작이 생길 수 있다.
        en: Tuples are preferred for heap elements; lists are mutable and may cause comparison issues.
  - label:
      ko: 힙 구조 구성
      en: Build heap structure
    indent: 0
    options:
    - code: heapq.heapify(minHeap)
      type: good
      why:
        ko: heapq.heapify()는 리스트를 제자리에서 최소 힙으로 변환한다. O(n) 시간에 완료.
        en: heapq.heapify() transforms list into min-heap in-place in O(n) time.
    - code: minHeap = heapq.nsmallest(k, minHeap)
      type: distractor
      why:
        ko: heapify 대신 nsmallest로 직접 선택하면 알고리즘이 달라진다. 효율성도 떨어진다.
        en: nsmallest directly selects rather than building heap; less efficient overall.
    - code: heapq.heappop(minHeap)
      type: distractor
      why:
        ko: heapify 없이 heappop을 호출하면 힙 불변성이 보장되지 않는다.
        en: Calling heappop without heapify violates heap invariant.
  - label:
      ko: 결과 리스트 초기화
      en: Initialize result list
    indent: 0
    options:
    - code: res = []
      type: good
      why:
        ko: 최종 k개 좌표를 저장할 빈 리스트를 생성한다.
        en: Create empty list to collect k closest (x, y) points.
    - code: res = [None] * k
      type: distractor
      why:
        ko: 미리 크기를 할당하는 것은 불필요하고 코드를 복잡하게 한다.
        en: Pre-allocating with None is unnecessary and complicates indexing.
    - code: res = minHeap[:k]
      type: distractor
      why:
        ko: 이것은 (dist, x, y) 튜플을 포함하지만, 우리는 (x, y)만 필요하다.
        en: This includes distance tuples; we need only (x, y) coordinates.
  - label:
      ko: K번 최소 요소 추출
      en: Extract k smallest elements
    indent: 1
    options:
    - code: _, x, y = heapq.heappop(minHeap)
      type: good
      why:
        ko: 최소 힙에서 k번 가장 작은 요소를 꺼낸다. 거리는 불필요하므로 언더스코어로 버린다.
        en: Pop k times from min-heap. Discard distance with underscore; keep only coordinates.
    - code: dist, x, y = heapq.heappop(minHeap)
      type: distractor
      why:
        ko: dist 변수를 명시하면 사용하지 않는 값을 저장해서 혼란스럽다.
        en: Storing unused dist variable is confusing; underscore is clearer intent.
    - code: res.append(heapq.heappop(minHeap))
      type: distractor
      why:
        ko: 전체 (dist, x, y) 튜플이 추가되지만, (x, y)만 필요하다.
        en: This appends entire tuple including distance; only (x, y) should be added.
  - label:
      ko: 결과 반환
      en: Return result
    indent: 0
    options:
    - code: return res
      type: good
      why:
        ko: k개의 가장 가까운 점을 포함하는 리스트를 반환한다.
        en: Return list containing k closest points.
    - code: return res[:k]
      type: distractor
      why:
        ko: 루프가 정확히 k번 실행되므로 슬라이싱은 불필요하고 혼동을 줄 수 있다.
        en: Loop already runs exactly k times; slicing is redundant and confusing.
    - code: return sorted(res)
      type: distractor
      why:
        ko: 문제에서 '어떤 순서로든 반환 가능'하므로 정렬은 불필요하다.
        en: Problem allows any order; sorting is unnecessary and wastes time.
trace:
  code:
  - 'class Solution:'
  - '    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:'
  - '        minHeap = []'
  - '        for x, y in points:'
  - '            dist = (x ** 2) + (y ** 2)'
  - '            minHeap.append((dist, x, y))'
  - '        '
  - '        heapq.heapify(minHeap)'
  - '        res = []'
  - '        for _ in range(k):'
  - '            _, x, y = heapq.heappop(minHeap)'
  - '            res.append((x, y))'
  - '        return res'
  cases:
  - input: '[[1,3],[-2,2]]

      1'
    expected: '[[-2,2]]'
  - input: '[[3,3],[5,-1],[-2,4]]

      2'
    expected: '[[3,3],[-2,4]]'
  worked_example:
    input: '[[1,3],[-2,2]]

      1'
    steps:
    - ko: 점 [1,3] → 거리 = 1² + 3² = 10 / 점 [-2,2] → 거리 = 4 + 4 = 8
      en: Point [1,3] → distance = 1² + 3² = 10 / Point [-2,2] → distance = 4 + 4 = 8
    - ko: minHeap = [(8, -2, 2), (10, 1, 3)] → heapify 적용, 최소 힙 구조 완성
      en: minHeap = [(8, -2, 2), (10, 1, 3)] → heapify applied, min-heap ready
    - ko: 'k = 1이므로 루프 1회: heappop() → (8, -2, 2) 추출 → res = [(-2, 2)]'
      en: 'Loop runs once (k=1): heappop() → extract (8, -2, 2) → res = [(-2, 2)]'
    answer: '[[-2,2]]'
solution:
  code: "class Solution:\n    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:\n        minHeap = []\n        for x, y in points:\n            dist = (x ** 2) + (y ** 2)\n            minHeap.append((dist, x, y))\n        \n        heapq.heapify(minHeap)\n        res = []\n        for _ in range(k):\n            _, x, y = heapq.heappop(minHeap)\n            res.append((x, y))\n        return res"
  complexity:
    time: O(n log n)
    space: O(n)
  followup:
  - ko: k가 n에 비해 매우 작다면 최대 힙을 사용하여 O(n log k)로 최적화할 수 있는가?
    en: If k is much smaller than n, can we optimize to O(n log k) using a max-heap of size k?
  - ko: 평균 시간복잡도 O(n)을 달성하려면 퀵셀렉트 알고리즘을 어떻게 적용하겠는가?
    en: How would you apply QuickSelect to achieve average O(n) time complexity?
  - ko: 입력 점들이 이미 거리 순서로 정렬되어 있다면 알고리즘을 어떻게 수정할 수 있는가?
    en: If points were pre-sorted by distance, how would the solution change?
```