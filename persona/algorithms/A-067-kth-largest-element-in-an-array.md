---
created: '2026-07-19'
date: '2026-07-19'
day: Day 67
difficulty: medium
id: A-067
source:
  curated_in:
  - neetcode150
  number: 215
  platform: leetcode
  slug: kth-largest-element-in-an-array
  url: https://leetcode.com/problems/kth-largest-element-in-an-array/
status: draft
tags:
- array
- divide-and-conquer
- sorting
- heap-priority-queue
- quickselect
title:
  en: Kth Largest Element in an Array
  ko: 배열에서 K번째 큰 원소
today: true
type: algorithm
updated: '2026-07-19'
visible: true
---

# 배열에서 K번째 큰 원소

## Data

```yaml
problem:
  title:
    ko: 배열에서 K번째 큰 원소
    en: Kth Largest Element in an Array
  statement:
    ko: '정수 배열 nums와 정수 k가 주어질 때, 배열에서 k번째 큰 원소를 반환하세요.


      정렬된 순서에서 k번째 큰 원소를 구하며, 서로 다른 k번째 원소가 아님을 주의하세요.


      정렬 없이 풀 수 있을까요?'
    en: 'Given an integer array nums and an integer k, return the kth largest element in the array.


      Note that it is the kth largest element in the sorted order, not the kth distinct element.


      Can you solve it without sorting?'
  constraints:
  - 1 ≤ k ≤ nums.length ≤ 10^5
  - -10^4 ≤ nums[i] ≤ 10^4
  io:
  - input: '[3,2,1,5,6,4]

      2'
    output: '5'
  - input: '[3,2,3,1,2,4,5,5,6]

      4'
    output: '4'
clarifying:
  items:
  - q:
      ko: k번째 큰 원소는 중복을 포함해서 세나요?
      en: Does 'kth largest' count duplicates or only distinct elements?
    type: good
    why:
      ko: 문제에서 명시했지만, 면접에서는 요구사항을 명확히 확인하는 것이 중요합니다.
      en: The problem states this, but confirming ambiguous requirements with the interviewer prevents building the wrong solution.
  - q:
      ko: 입력 배열을 수정해도 되나요?
      en: Can I modify the input array in place?
    type: good
    why:
      ko: 배열을 수정하면 공간 효율성을 높일 수 있으므로, 면접관의 허락을 먼저 얻는 것이 좋습니다.
      en: In-place modifications can save space; check with the interviewer before making this assumption.
  - q:
      ko: 배열에 음수가 포함될 수 있나요?
      en: Can the array contain negative numbers?
    type: good
    why:
      ko: '음수 범위를 알면 특정 알고리즘(예: 계수 정렬)의 적용 가능성을 판단할 수 있습니다.'
      en: Knowing the sign range helps determine if certain algorithms like counting sort are viable.
  - q:
      ko: 배열이 스트림처럼 계속 들어오는 경우도 고려해야 하나요?
      en: What if the array is too large to fit in memory or arrives as a data stream?
    type: good
    why:
      ko: '이는 흔한 follow-up이며, 해결책이 크게 달라집니다 (min-heap 유지).  '
      en: Common follow-up that requires a different approach; you'd maintain a rolling k-sized heap instead.
  - q:
      ko: 정렬을 사용하면 가장 간단하지 않을까요?
      en: Wouldn't just sorting the array be the simplest solution?
    type: distractor
    why:
      ko: 정렬은 작동하지만, 문제에서 '정렬 없이 풀 수 있을까요?'라고 명시했으므로, O(n log n)보다 나은 O(n log k) 방법을 찾아야 합니다.
      en: While sorting works correctly, the problem explicitly asks 'without sorting', and O(n log k) beats O(n log n) when k << n.
  - q:
      ko: 최대 힙을 사용하는 것이 더 직관적이지 않을까요?
      en: Wouldn't a max heap be more intuitive for finding 'largest' elements?
    type: distractor
    why:
      ko: 최대 힙은 직관적이지만, 전체 배열을 힙으로 만들고 k-1번 팝해야 하므로 (O(n + k log n)), 최소 힙으로 k개만 유지하는 것 (O(n log k))보다 비효율적입니다.
      en: Max heap is intuitive but requires popping k-1 times from a heap of size n. Min heap of size k is more efficient.
approach:
  items:
  - name:
      ko: 최소 힙 전략 (K개 원소 유지)
      en: Min-Heap Strategy (Maintain k Elements)
    complexity: O(n log k) time / O(k) space
    type: good
    why:
      ko: 배열을 순회하면서 가장 큰 k개 원소만 최소 힙으로 유지합니다. 힙의 루트(최솟값)는 항상 k번째로 큰 원소입니다. 크기가 작은 k에 대해 매우 효율적입니다.
      en: Maintain only the k largest elements in a min-heap. The root is always the kth largest. Efficient when k << n.
  - name:
      ko: QuickSelect 알고리즘
      en: QuickSelect (Partition-based Selection)
    complexity: O(n) average time / O(log n) space
    type: good
    why:
      ko: QuickSort의 분할 논리를 사용하여 k번째 원소를 평균 O(n) 시간에 찾습니다. 불필요한 정렬을 피하고 공간도 적게 사용합니다.
      en: Uses QuickSort's partition logic to find the kth largest in O(n) average time without full sort. Space for recursion stack only.
  - name:
      ko: 전체 배열 정렬 후 인덱싱
      en: Sort Entire Array and Index
    complexity: O(n log n) time / O(1) space
    type: distractor
    why:
      ko: 작동하며 구현이 간단하지만, 문제에서 '정렬 없이' 풀 것을 명시했고 O(n log n)은 O(n log k)보다 느립니다.
      en: Works and is simple, but violates the 'without sorting' hint and is suboptimal compared to heap/quickselect.
  - name:
      ko: 최대 힙 (전체 배열)
      en: Max-Heap (Entire Array)
    complexity: O(n + k log n) time / O(n) space
    type: distractor
    why:
      ko: 전체 배열을 최대 힙으로 만든 후 k-1번을 팝합니다. 최소 힙 전략보다 느리며 더 많은 메모리를 사용합니다.
      en: Heapify entire array, then pop k-1 times. Slower and more memory-hungry than min-heap strategy.
  - name:
      ko: 계수 정렬 (범위 기반)
      en: Counting Sort (Range-based)
    complexity: O(n + range) time / O(range) space
    type: distractor
    why:
      ko: 이 문제에서 범위는 20,000이지만, 일반적인 해결책이 아니며 특정 상황에서만 유리합니다.
      en: Range of 20,000 is not negligible; counting sort is only better when range is tiny, which is not general here.
logic:
  format: slot
  slots:
  - label:
      ko: 배열을 최소 힙으로 변환
      en: Convert array to min-heap
    indent: 0
    options:
    - code: heapify(nums)
      type: good
      why:
        ko: 배열을 in-place로 최소 힙 구조로 변환합니다. heapify()는 O(n) 시간에 모든 원소에 대해 힙 속성을 만족하도록 정렬합니다.
        en: Transforms the array in-place into a min-heap structure in O(n) time, satisfying the heap property for all elements.
    - code: nums = heapq.heapify(nums)
      type: distractor
      why:
        ko: heapify()는 None을 반환하므로 nums에 None이 할당됩니다. In-place 함수이므로 결과를 재할당하면 안 됩니다.
        en: heapify() returns None, so this assigns None to nums. heapify() modifies in-place; don't reassign the return value.
    - code: "heap = PriorityQueue()\nfor num in nums:\n    heap.put(num)"
      type: distractor
      why:
        ko: 작동하지만 추가 O(n) 공간을 사용하고, heapify()의 O(n) 시간 초기화 방법보다 느립니다.
        en: Works but uses O(n) extra space and O(n log n) time. heapify() is more efficient for initial setup.
  - label:
      ko: '반복: k개만 남을 때까지'
      en: Loop while more than k elements exist
    indent: 1
    options:
    - code: 'while len(nums) > k:'
      type: good
      why:
        ko: 힙의 크기가 정확히 k가 될 때까지 반복하면, 남은 k개 원소 중 가장 작은 것(힙의 루트)이 전체 배열에서 k번째로 큰 원소입니다.
        en: Loop until exactly k elements remain. The minimum of those k largest elements is the kth largest overall.
    - code: 'while len(nums) >= k:'
      type: distractor
      why:
        ko: 이 조건은 한 번 더 반복하여 최종적으로 k-1개만 남깁니다.
        en: This condition iterates one extra time, leaving only k-1 elements instead of k.
    - code: 'for _ in range(len(nums) - k):'
      type: distractor
      why:
        ko: 배열 크기가 변하면 루프 범위도 변하므로 예상과 다르게 작동할 수 있습니다.
        en: Works but can be fragile; the loop range was fixed at entry time, whereas the while condition adapts dynamically.
  - label:
      ko: 최소 원소 제거
      en: Pop the minimum element
    indent: 2
    options:
    - code: heappop(nums)
      type: good
      why:
        ko: heappop()은 최소 힙의 루트(가장 작은 원소)를 제거하고 O(log n) 시간에 힙 구조를 재정렬합니다.
        en: heappop() removes the minimum from the heap and re-balances in O(log n) time, maintaining the heap property.
    - code: nums.pop(0)
      type: distractor
      why:
        ko: 배열의 첫 번째 원소를 제거하지만, 힙 구조를 유지하지 않습니다. 이후 nums[0]은 최소값이 아닙니다.
        en: Removes the first array element but breaks the heap property. nums[0] is no longer the minimum.
    - code: 'min_val = min(nums)

        nums.remove(min_val)'
      type: distractor
      why:
        ko: 최소값을 제거하지만, min()은 O(n), remove()도 O(n)이므로 각 루프당 O(n)입니다. heappop()의 O(log n)보다 훨씬 느립니다.
        en: Removes the minimum but costs O(n) per iteration. heappop() is O(log n), much faster.
  - label:
      ko: k번째 큰 원소 반환
      en: Return the kth largest element
    indent: 1
    options:
    - code: return nums[0]
      type: good
      why:
        ko: 반복 후, 남은 k개 원소의 최솟값(nums[0])이 원래 배열에서 k번째로 큰 원소입니다.
        en: After the loop, nums[0] is the minimum of the k largest elements, which is the kth largest in the original array.
    - code: return nums[-1]
      type: distractor
      why:
        ko: 힙의 마지막 원소는 특정 순서를 보장하지 않습니다. k번째 큰 원소와 무관한 임의의 값입니다.
        en: The last position in a heap is arbitrary and has no guaranteed relationship to the kth largest.
    - code: return max(nums)
      type: distractor
      why:
        ko: 남은 k개 원소의 최댓값은 가장 큰 원소이지, k번째로 큰 원소가 아닙니다.
        en: The maximum of the k elements is the largest, not the kth largest.
trace:
  code:
  - '# Solution: Sorting'
  - '# Time Complexity:'
  - '#   - Best Case: O(n*log(k))'
  - '#   - Average Case: O(n*log(k))'
  - '#   - Worst Case:O(n*log(k))'
  - '# Extra Space Complexity: O(k)'
  - 'class Solution:'
  - '    def findKthLargest(self, nums: List[int], k: int) -> int:'
  - '        heapify(nums)'
  - '        while len(nums) > k:'
  - '            heappop(nums)'
  - '        return nums[0]'
  - ''
  - '# Solution: Sorting'
  - '# Time Complexity:'
  - '#   - Best Case: O(n)'
  - '#   - Average Case: O(n*log(n))'
  - '#   - Worst Case:O(n*log(n))'
  - '# Extra Space Complexity: O(n)'
  - 'class Solution1:'
  - '    def findKthLargest(self, nums: List[int], k: int) -> int:'
  - '        nums.sort()'
  - '        return nums[len(nums) - k]'
  - ''
  - ''
  - '# Solution: QuickSelect'
  - '# Time Complexity: O(n)'
  - '# Extra Space Complexity: O(n)'
  - 'class Solution2:'
  - '    def findKthLargest(self, nums: List[int], k: int) -> int:'
  - '        pivot = random.choice(nums)'
  - '        left = [num for num in nums if num > pivot]'
  - '        mid = [num for num in nums if num == pivot]'
  - '        right = [num for num in nums if num < pivot]'
  - ''
  - '        length_left = len(left)'
  - '        length_right = len(right)'
  - '        length_mid = len(mid)'
  - '        if k <= length_left:'
  - '            return self.findKthLargest(left, k)'
  - '        elif k > length_left + length_mid:'
  - '            return self.findKthLargest(right, k - length_mid - length_left)'
  - '        else:'
  - '            return mid[0]'
  cases:
  - input: '[3,2,1,5,6,4]

      2'
    expected: '5'
  - input: '[3,2,3,1,2,4,5,5,6]

      4'
    expected: '4'
  worked_example:
    input: '[3,2,1,5,6,4]

      2'
    steps:
    - ko: '배열 [3,2,1,5,6,4]를 최소 힙으로 변환 → 힙 구조: [1,2,3,5,6,4]'
      en: Transform [3,2,1,5,6,4] into min-heap → heap becomes [1,2,3,5,6,4]
    - ko: 'k=2이므로 len(nums) > 2인 동안 반복: 1, 2, 3, 4를 순차적으로 팝'
      en: 'k=2, so pop while len > 2: remove 1, then 2, then 3, then 4'
    - ko: 4번의 팝 후, 힙에 [5, 6]만 남음 (len=2), 반복 종료
      en: After 4 pops, heap contains [5, 6] with len=2, loop condition fails, exit
    - ko: nums[0] = 5 반환 → [6, 5, 4, 3, 2, 1] 정렬 순서에서 2번째가 맞음
      en: Return nums[0] = 5 → correctly the 2nd largest in [6, 5, 4, 3, 2, 1]
    answer: '5'
solution:
  code: "# Solution: Sorting\n# Time Complexity:\n#   - Best Case: O(n*log(k))\n#   - Average Case: O(n*log(k))\n#   - Worst Case:O(n*log(k))\n# Extra Space Complexity: O(k)\nclass Solution:\n    def findKthLargest(self, nums: List[int], k: int) -> int:\n        heapify(nums)\n        while len(nums) > k:\n            heappop(nums)\n        return nums[0]\n\n# Solution: Sorting\n# Time Complexity:\n#   - Best Case: O(n)\n#   - Average Case: O(n*log(n))\n#   - Worst Case:O(n*log(n))\n# Extra Space Complexity: O(n)\nclass Solution1:\n    def findKthLargest(self, nums: List[int], k: int) -> int:\n        nums.sort()\n        return nums[len(nums) - k]\n\n\n# Solution: QuickSelect\n# Time Complexity: O(n)\n# Extra Space Complexity: O(n)\nclass Solution2:\n    def findKthLargest(self, nums: List[int], k: int) -> int:\n        pivot = random.choice(nums)\n        left = [num for num in nums if num > pivot]\n        mid = [num for num in nums if num == pivot]\n        right = [num for num in nums\
    \ if num < pivot]\n\n        length_left = len(left)\n        length_right = len(right)\n        length_mid = len(mid)\n        if k <= length_left:\n            return self.findKthLargest(left, k)\n        elif k > length_left + length_mid:\n            return self.findKthLargest(right, k - length_mid - length_left)\n        else:\n            return mid[0]\n"
  complexity:
    time: O(n log k) — heapify O(n) + pop operations O((n−k) log k)
    space: O(k) — min-heap stores at most k elements (or O(1) extra if using input array)
  followup:
  - ko: 만약 배열이 매우 크거나 스트림처럼 계속 데이터가 들어온다면?
    en: How would you adapt this if the array is too large for memory or arrives as an unbounded stream?
  - ko: 상위 k개 원소 전체를 반환해야 한다면?
    en: How would you return all top k elements, not just the kth?
  - ko: QuickSelect는 평균 O(n)인데, 실제로 min-heap을 더 자주 쓰는 이유는?
    en: QuickSelect averages O(n) time, so why might a heap-based solution be preferred in production code?
```