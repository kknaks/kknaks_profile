---
created: '2026-07-16'
date: '2026-07-16'
day: Day 64
difficulty: easy
id: A-064
source:
  curated_in:
  - neetcode150
  number: 703
  platform: leetcode
  slug: kth-largest-element-in-a-stream
  url: https://leetcode.com/problems/kth-largest-element-in-a-stream/
status: draft
tags:
- tree
- design
- binary-search-tree
- heap-priority-queue
- binary-tree
- data-stream
title:
  en: Kth Largest Element in a Stream
  ko: 스트림에서 k번째 최대 요소
today: true
type: algorithm
updated: '2026-07-16'
visible: true
---

# 스트림에서 k번째 최대 요소

## Data

```yaml
problem:
  title:
    ko: 스트림에서 k번째 최대 요소
    en: Kth Largest Element in a Stream
  statement:
    ko: '대학 입시 사무실의 일원으로서, 지원자의 시험 성적 중 k번째 최고 성적을 실시간으로 추적해야 합니다. 이는 면접 및 입시의 커트라인을 동적으로 결정하는 데 도움이 됩니다.


      새로운 성적이 제출될 때마다 주어진 정수 k에 대해 스트림의 k번째 최고 성적을 유지하고 지속적으로 반환하는 클래스를 구현해야 합니다. 더 구체적으로, 우리는 모든 성적의 정렬된 목록에서 k번째 최고 성적을 찾고 있습니다.


      KthLargest 클래스를 구현하십시오:


      KthLargest(int k, int[] nums): 정수 k와 시험 성적의 스트림 nums로 객체를 초기화합니다.


      int add(int val): 새로운 시험 성적 val을 스트림에 추가하고 지금까지의 성적 풀에서 k번째 최대 요소를 나타내는 요소를 반환합니다.'
    en: 'You are part of a university admissions office and need to keep track of the kth highest test score from applicants in real-time. This helps to determine cut-off marks for interviews and admissions dynamically as new applicants submit their scores.


      You are tasked to implement a class which, for a given integer k, maintains a stream of test scores and continuously returns the kth highest test score after a new score has been submitted. More specifically, we are looking for the kth highest score in the sorted list of all scores.


      Implement the KthLargest class:


      KthLargest(int k, int[] nums) Initializes the object with the integer k and the stream of test scores nums.


      int add(int val) Adds a new test score val to the stream and returns the element representing the kth largest element in the pool of test scores so far.'
  constraints:
  - 0 ≤ nums.length ≤ 10^4
  - 1 ≤ k ≤ nums.length + 1
  - -10^4 ≤ nums[i] ≤ 10^4
  - -10^4 ≤ val ≤ 10^4
  - At most 10^4 calls will be made to add()
  io:
  - input: '["KthLargest","add","add","add","add","add"]

      [[3,[4,5,8,2]],[3],[5],[10],[9],[4]]'
    output: '[null, 4, 5, 5, 8, 8]'
  - input: '["KthLargest","add","add","add","add"]

      [[4,[7,7,7,7,8,3]],[2],[10],[9],[9]]'
    output: '[null, 7, 7, 7, 8]'
clarifying:
  items:
  - q:
      ko: k번째 최대값은 중복을 포함하는 순위로 계산되는가?
      en: Does 'kth largest' count duplicates as separate rankings?
    type: good
    why:
      ko: 네, 중복값도 각각 하나의 요소로 계산됩니다. [8, 8, 7]에서 2번째 최대는 8입니다.
      en: Yes, duplicates count separately. In sorted [8, 8, 7], the 2nd largest is 8, not 7.
  - q:
      ko: 최소 힙의 루트가 항상 k번째 최대값인 이유는?
      en: Why does the min-heap root always give the kth largest element?
    type: good
    why:
      ko: 크기 k인 최소 힙에는 k개의 최대 요소만 보관됩니다. 최소 힙의 루트는 이 k개 중 가장 작은 요소이므로 k번째 최대값입니다.
      en: By keeping only the k largest elements in a min-heap, the root (smallest of k largest) is exactly the kth largest.
  - q:
      ko: 입력 배열을 직접 수정하는 것이 안전한가?
      en: Is it safe to modify the input array nums directly?
    type: good
    why:
      ko: 네, nums를 힙 구조로 변환하여 추가 배열 할당을 줄입니다. 문제에서 이를 금지하지 않습니다.
      en: Yes, using nums as the heap directly saves space and the problem doesn't forbid it.
  - q:
      ko: 최대 힙으로 모든 요소를 추적하면 더 효율적이지 않을까?
      en: Why not use a max-heap to track all elements instead?
    type: distractor
    why:
      ko: 최대 힙은 모든 n개 요소를 보관해야 하므로 O(n) 공간이 필요합니다. 최소 힙은 k개만 보관하므로 O(k) 공간입니다.
      en: A max-heap would require O(n) space for all elements. Min-heap uses only O(k) space by keeping just the k largest.
  - q:
      ko: 매번 전체 배열을 정렬하면 안 되는 이유는?
      en: Why not just sort the array after each add()?
    type: distractor
    why:
      ko: 정렬은 각 add()에서 O(n log n) 시간이 필요하여, O(log k) 힙 연산보다 훨씬 느립니다.
      en: Sorting takes O(n log n) per add(), much slower than the O(log k) heap operations.
  - q:
      ko: 초기화 후 요소가 k개 미만이면 add()는 어떻게 작동하는가?
      en: What happens if we have fewer than k elements after initialization?
    type: good
    why:
      ko: 문제 조건 1 ≤ k ≤ nums.length + 1이 보장하므로, 첫 add() 후에는 항상 k개 이상의 요소가 있습니다.
      en: The constraint guarantees that after at most one add(), we have at least k elements to track.
  - q:
      ko: heapify()가 O(n) 시간에 작동하는가?
      en: Is heapify() really O(n) instead of O(n log n)?
    type: good
    why:
      ko: 네, heapify()는 하향식 접근으로 O(n) 시간에 배열을 힙 구조로 변환합니다. 정렬보다 훨씬 빠릅니다.
      en: Yes, heapify uses a bottom-up approach in O(n) time, not O(n log n). Much faster than sorting.
  - q:
      ko: add() 후 len > k 체크에서 while이 아닌 if를 쓰는 이유는?
      en: Why use if instead of while when trimming after add()?
    type: good
    why:
      ko: 각 add()는 최대 1개 요소만 추가하므로, 크기가 최대 k+1이 됩니다. if 한 번으로 충분합니다.
      en: We only push one element per add(), so size is at most k+1. A single if/pop is sufficient.
approach:
  items:
  - name:
      ko: 최소 힙 (k개 최대 유지)
      en: Min-Heap (maintain k largest)
    complexity: O(n log k) initialization, O(log k) per add; O(k) space
    type: good
    why:
      ko: 크기 k인 최소 힙을 유지하여 O(log k) 시간에 k번째 최대값을 얻습니다. 초기화는 O(n) heapify + O(k log k) pop입니다.
      en: 'Optimal: maintain only k elements, achieving O(log k) per add() and O(k) space. Initialization uses O(n) heapify plus O(k log k) for trimming.'
  - name:
      ko: 정렬된 리스트 유지
      en: Sorted List
    complexity: O(n log n) init, O(n) per add; O(n) space
    type: distractor
    why:
      ko: 매 add()마다 정렬된 위치에 삽입해야 하므로 O(n)이 필요하고, O(n) 공간을 낭비합니다.
      en: Each add() requires O(n) insertion into a sorted position and we store all O(n) elements. Slower and uses more space than heap.
  - name:
      ko: 최대 힙 (모든 요소)
      en: Max-Heap (store all elements)
    complexity: O(n log n) init, O(log n) per add; O(n) space
    type: distractor
    why:
      ko: 모든 요소를 최대 힙에 보관하고 k번 pop하여 k번째를 찾아야 하므로 불필요하게 복잡합니다.
      en: Stores all O(n) elements and requires k pops to find the kth largest. Min-heap of size k is simpler and more efficient.
  - name:
      ko: 이진 탐색 트리 (BST)
      en: Binary Search Tree (BST)
    complexity: O(n log n) build, O(log n) per add; O(n) space
    type: distractor
    why:
      ko: BST도 작동하지만 구현이 복잡하고, 불균형 트리는 O(n) 악화 위험이 있습니다. 힙이 더 간단합니다.
      en: BST could work but requires complex balancing logic and risks O(n) worst-case. Heap is simpler with guaranteed O(log k).
  - name:
      ko: 무차별 탐색 (매번 정렬)
      en: Brute Force (sort each add)
    complexity: O(1) init, O(n log n) per add; O(n) space
    type: distractor
    why:
      ko: 매 add()마다 전체 배열을 정렬하면 O(n log n)이 되어 스트리밍 환경에서 매우 비효율적입니다.
      en: Sorting all elements after each add() is O(n log n) per operation—impractical for streaming scenarios.
logic:
  format: slot
  slots:
  - label:
      ko: 힙 변수와 k 초기화
      en: Initialize heap variable and k
    indent: 0
    options:
    - code: self.minHeap, self.k = nums, k
      type: good
      why:
        ko: 입력 배열 nums를 그대로 힙으로 사용할 변수에 저장하고 k를 저장합니다. 추가 배열 할당을 줄입니다.
        en: Store the input array and k value. We'll use nums as the heap structure directly, avoiding extra allocations.
    - code: self.minHeap = heapq.heappush(nums, k)
      type: distractor
      why:
        ko: heappush는 기존 힙에 하나의 요소를 추가하는 것이지, 배열을 힙으로 초기화하는 게 아닙니다.
        en: heappush adds a single element to an existing heap; it doesn't initialize a heap from a list.
    - code: self.minHeap = nums[:k]
      type: distractor
      why:
        ko: 처음 k개만 가져가면 나머지 배열의 더 큰 값들을 놓칠 수 있습니다.
        en: Taking only the first k elements discards larger values from later in the array.
  - label:
      ko: 배열을 힙 구조로 변환
      en: Convert list into heap structure
    indent: 0
    options:
    - code: heapq.heapify(self.minHeap)
      type: good
      why:
        ko: heapify()는 배열을 O(n) 시간에 제자리에서 유효한 최소 힙 구조로 변환합니다. 정렬보다 훨씬 빠릅니다.
        en: heapify() restructures the array in-place into a valid min-heap in O(n) time—much faster than sorting O(n log n).
    - code: heapq.heappop(self.minHeap)
      type: distractor
      why:
        ko: pop()은 요소를 제거하는 연산이므로 힙 구조를 만들지 못합니다.
        en: heappop() removes an element; it doesn't structure the heap.
    - code: self.minHeap = sorted(self.minHeap)
      type: distractor
      why:
        ko: 정렬은 O(n log n) 시간이 필요하므로 O(n) heapify보다 느립니다.
        en: Sorting takes O(n log n), whereas heapify is O(n).
  - label:
      ko: 초기화 중 초과 요소 제거
      en: Remove excess elements during init
    indent: 0
    options:
    - code: 'while len(self.minHeap) > k:'
      type: good
      why:
        ko: heapify 후, 힙 크기가 k를 초과하면 반복해서 최소 요소를 제거하여 정확히 k개의 최대 요소만 남깁니다.
        en: After heapify, repeatedly pop the minimum to keep exactly the k largest elements.
    - code: 'if len(self.minHeap) > self.k:'
      type: distractor
      why:
        ko: if 문은 한 번만 체크하므로, 제거가 필요한 여러 요소를 놓칠 수 있습니다.
        en: Using if only removes one element. We might need to remove several elements to reach size k.
    - code: 'while len(self.minHeap) > self.k: heapq.heappush(self.minHeap, self.minHeap[0])'
      type: distractor
      why:
        ko: heappush는 추가하는 연산이므로 크기를 줄이지 못합니다. heappop을 사용해야 합니다.
        en: heappush adds elements; we need heappop to remove.
  - label:
      ko: 새 값을 힙에 추가
      en: Push new value to heap
    indent: 1
    options:
    - code: heapq.heappush(self.minHeap, val)
      type: good
      why:
        ko: heappush(val)은 새로운 요소를 O(log k) 시간에 힙에 추가하고 최소 힙 성질을 유지합니다.
        en: heappush() adds the new value in O(log k) time while maintaining the min-heap property.
    - code: heapq.heappop(self.minHeap, val)
      type: distractor
      why:
        ko: heappop은 인자를 받지 않으며 요소를 추가하지 않고 제거합니다.
        en: heappop() doesn't take arguments and removes elements instead of adding.
    - code: self.minHeap.append(val)
      type: distractor
      why:
        ko: append는 힙 구조를 유지하지 않아 이후 힙 연산에서 오류가 발생합니다.
        en: append() doesn't maintain the heap property; subsequent operations will be incorrect.
  - label:
      ko: 추가 후 크기 초과 시 최소값 제거
      en: Pop if heap exceeds size k
    indent: 1
    options:
    - code: 'if len(self.minHeap) > self.k:'
      type: good
      why:
        ko: 새로운 값 추가 후, 힙 크기가 k를 초과하면 최소값 (루트)을 제거하여 항상 정확히 k개의 최대 요소만 유지합니다.
        en: After pushing, if size exceeds k, pop the root (smallest of k largest) to maintain exactly k elements.
    - code: 'if len(self.minHeap) >= self.k:'
      type: distractor
      why:
        ko: ≥ 연산자는 크기가 정확히 k일 때도 제거하므로, k개보다 적은 요소가 남게 됩니다.
        en: Using >= would pop when size equals k, leaving fewer than k elements.
    - code: 'while len(self.minHeap) > self.k: heapq.heappop(self.minHeap)'
      type: distractor
      why:
        ko: 한 번에 하나의 요소만 추가하므로 루프가 불필요합니다. if 한 번이 충분합니다.
        en: We only push one element, so the heap size is at most k+1. A single if/pop suffices.
  - label:
      ko: k번째 최대값 반환
      en: Return kth largest element
    indent: 1
    options:
    - code: return self.minHeap[0]
      type: good
      why:
        ko: 크기 k인 최소 힙의 루트(heap[0])는 k개의 최대 요소 중 최소이므로 정확히 k번째 최대값입니다.
        en: The root of a min-heap of size k is the smallest of the k largest elements, which is the kth largest overall.
    - code: return self.minHeap[-1]
      type: distractor
      why:
        ko: 최소 힙에서 마지막 요소는 무작위 위치이므로 k번째 최대값이 아닙니다.
        en: In a min-heap, the last element's position is arbitrary; it's not the kth largest.
    - code: return self.minHeap.pop()
      type: distractor
      why:
        ko: pop()은 힙의 구조를 변경하므로 다음 add() 호출에서 정확한 결과를 얻을 수 없습니다.
        en: pop() modifies the heap, breaking the invariant for the next add().
    - code: return sorted(self.minHeap)[0]
      type: distractor
      why:
        ko: 정렬은 불필요하며 O(k log k) 시간이 낭비됩니다. 루트가 이미 최솟값입니다.
        en: Sorting wastes O(k log k) time; the root is already the minimum.
trace:
  code:
  - 'class KthLargest:'
  - '    def __init__(self, k: int, nums: List[int]):'
  - '        # minHeap w/ K largest integers'
  - '        self.minHeap, self.k = nums, k'
  - '        heapq.heapify(self.minHeap)'
  - '        while len(self.minHeap) > k:'
  - '            heapq.heappop(self.minHeap)'
  - ''
  - '    def add(self, val: int) -> int:'
  - '        heapq.heappush(self.minHeap, val)'
  - '        if len(self.minHeap) > self.k:'
  - '            heapq.heappop(self.minHeap)'
  - '        return self.minHeap[0]'
  cases:
  - input: '["KthLargest","add","add","add","add","add"]

      [[3,[4,5,8,2]],[3],[5],[10],[9],[4]]'
    expected: '[null, 4, 5, 5, 8, 8]'
  - input: '["KthLargest","add","add","add","add"]

      [[4,[7,7,7,7,8,3]],[2],[10],[9],[9]]'
    expected: '[null, 7, 7, 7, 8]'
  worked_example:
    input: '["KthLargest","add","add","add","add","add"]

      [[3,[4,5,8,2]],[3],[5],[10],[9],[4]]'
    steps:
    - ko: '초기화: nums=[4,5,8,2], k=3 → heapify()로 최소 힙 구조 생성 → 크기 4 > k이므로 최소값(2) 제거 → 결과: [4,5,8]'
      en: 'Initialize: heapify [4,5,8,2] → min-heap structure [2,4,8,5] → size 4 > k, remove min(2) → heap=[4,5,8]'
    - ko: 'add(3), add(5), add(10): 각각 추가하고 크기가 4가 되면 최소값 제거 → 루트 반환 4, 5, 5'
      en: 'add(3), add(5), add(10): push each, trim to size k → return roots 4, 5, 5'
    - ko: 'add(9), add(4): 9 추가 후 최소(5) 제거하여 [8,9,10] 반환 8; 4 추가 후 최소(4) 제거하여 [8,9,10] 반환 8'
      en: 'add(9), add(4): push 9 → pop min(5) → return 8; push 4 → pop min(4) → return 8'
    answer: '[null, 4, 5, 5, 8, 8]'
solution:
  code: "class KthLargest:\n    def __init__(self, k: int, nums: List[int]):\n        # minHeap w/ K largest integers\n        self.minHeap, self.k = nums, k\n        heapq.heapify(self.minHeap)\n        while len(self.minHeap) > k:\n            heapq.heappop(self.minHeap)\n\n    def add(self, val: int) -> int:\n        heapq.heappush(self.minHeap, val)\n        if len(self.minHeap) > self.k:\n            heapq.heappop(self.minHeap)\n        return self.minHeap[0]\n"
  complexity:
    time: O(n log k) initialization (O(n) heapify + O(k log k) removals), O(log k) per add()
    space: O(k) for heap of k largest elements
  followup:
  - ko: k가 매우 크거나 스트림이 매우 길다면? 메모리를 절약하는 방법은?
    en: How would you optimize if k is very large or the stream is infinite? Could you use approximation or external storage?
  - ko: '요소 업데이트/삭제를 지원해야 한다면? (예: 특정 점수를 수정하거나 제거)'
    en: What if you needed to support updates or removals of specific scores after they've been added?
  - ko: '동시에 여러 k값에 대한 답을 유지해야 한다면? (예: 1번째, 3번째, 5번째 최대)'
    en: If you needed to simultaneously track the 1st, 3rd, and 5th largest elements, how would you optimize?
```