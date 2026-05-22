---
created: '2026-05-22'
date: '2026-05-22'
day: Day 20
difficulty: hard
id: A-020
source:
  curated_in:
  - neetcode150
  number: 239
  platform: leetcode
  slug: sliding-window-maximum
  url: https://leetcode.com/problems/sliding-window-maximum/
status: draft
tags:
- array
- queue
- sliding-window
- heap-priority-queue
- monotonic-queue
title:
  en: Sliding Window Maximum
  ko: 슬라이딩 윈도우 최댓값
today: true
type: algorithm
updated: '2026-05-22'
visible: true
---

# 슬라이딩 윈도우 최댓값

## Data

```yaml
problem:
  title:
    ko: 슬라이딩 윈도우 최댓값
    en: Sliding Window Maximum
  statement:
    ko: '정수 배열 nums와 윈도우 크기 k가 주어집니다. 크기 k인 슬라이딩 윈도우가 배열의 맨 왼쪽에서 맨 오른쪽으로 이동합니다. 각 이동마다 윈도우 내의 최댓값을 구해야 합니다.


      매번 윈도우가 한 칸씩 오른쪽으로 이동할 때, 각 윈도우의 최댓값들을 반환하세요.'
    en: 'You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.


      Return the max sliding window.'
  constraints:
  - 1 ≤ nums.length ≤ 10⁵
  - -10⁴ ≤ nums[i] ≤ 10⁴
  - 1 ≤ k ≤ nums.length
  io:
  - input: '[1,3,-1,-3,5,3,6,7]

      3'
    output: '[3,3,5,5,6,7]'
  - input: '[1]

      1'
    output: '[1]'
clarifying:
  items:
  - q:
      ko: 윈도우에 정확히 k개의 원소가 있을 때부터 최댓값을 출력해야 하나요?
      en: Should we start outputting the maximum only when the window has exactly k elements?
    type: good
    why:
      ko: 이는 문제의 핵심 조건입니다. 처음 k-1개 원소는 윈도우가 완성되지 않았으므로 출력하지 않습니다.
      en: This is a critical boundary condition. The first k-1 elements don't form a complete window, so no output yet.
  - q:
      ko: 어떤 데이터 구조를 사용하면 최댓값을 효율적으로 추적할 수 있을까요?
      en: What data structure can efficiently maintain the maximum across multiple windows?
    type: good
    why:
      ko: 데큐와 단조성을 활용하면 각 원소가 정확히 한 번 삽입되고 삭제되어 O(n) 시간이 가능합니다.
      en: A monotonic deque allows each element to be processed exactly once, achieving O(n) time overall.
  - q:
      ko: 윈도우를 벗어난 원소를 데큐에서 제거해야 하는 이유는 무엇인가요?
      en: Why must we remove elements that fall outside the current window?
    type: good
    why:
      ko: 데큐의 맨 앞이 항상 현재 윈도우 내의 최댓값을 나타내야 합니다. 윈도우 밖의 원소는 제거되어야만 이를 보장할 수 있습니다.
      en: The front of the deque must always represent the maximum within the current window. Old elements outside the window would give incorrect results.
  - q:
      ko: 배열 값 대신 인덱스를 데큐에 저장하는 이유는 무엇인가요?
      en: Why store indices instead of values in the deque?
    type: good
    why:
      ko: 인덱스를 저장해야 어떤 원소가 현재 윈도우 범위 [l, r] 내에 있는지 확인할 수 있습니다.
      en: Indices let us determine which elements are within the window boundaries. Values alone don't tell us position.
  - q:
      ko: 모든 원소가 같은 경우에는 어떻게 되나요?
      en: What happens if all elements in the array are identical?
    type: good
    why:
      ko: 모든 윈도우의 최댓값이 그 값이 되고, 데큐에는 한 원소만 남게 됩니다. 알고리즘은 여전히 정상 작동합니다.
      en: The output would be that value repeated n-k+1 times, and the deque would only hold one index at a time.
  - q:
      ko: 배열을 정렬한 후에 슬라이딩 윈도우를 적용할 수 있을까요?
      en: Could we sort the array first and then apply sliding window?
    type: distractor
    why:
      ko: 정렬하면 원래 순서가 손실되어 윈도우의 연속성이 깨집니다. 문제는 원래 배열의 연속된 부분 배열의 최댓값을 요구합니다.
      en: Sorting loses the original order. We need maxima of consecutive subarrays in the original array.
  - q:
      ko: 슬라이딩 윈도우 접근법이 항상 무차별 대입보다 빠를까요?
      en: Is sliding window always faster than brute force for this problem?
    type: distractor
    why:
      ko: 이론적으로는 O(n)이 O(nk)보다 빠르지만, k가 매우 작을 때는 실제 성능이 비슷할 수 있습니다. 하지만 k가 클 때는 훨씬 빠릅니다.
      en: Theoretically yes (O(n) vs O(nk)), but for very small k the constants matter. The deque approach is asymptotically superior.
approach:
  items:
  - name:
      ko: 단조성 데큐
      en: Monotonic Deque
    complexity: O(n) time / O(k) space
    type: good
    why:
      ko: 각 원소가 정확히 한 번 삽입되고 한 번 삭제되므로 선형 시간입니다. 단조 감소하는 데큐의 맨 앞이 항상 현재 윈도우의 최댓값입니다.
      en: Each element enters and exits the deque exactly once, so linear time. The deque's front always holds the window's maximum due to the monotonic property.
  - name:
      ko: 우선순위 큐 (지연 삭제)
      en: Priority Queue with Lazy Deletion
    complexity: O(n log n) time / O(n) space
    type: good
    why:
      ko: 최대 힙을 사용하되, 윈도우 범위를 벗어난 원소는 나중에 삭제합니다. 구현은 단순하지만 O(n log n)으로 더 느립니다.
      en: Use a max heap and lazily remove out-of-window elements. Simpler conceptually but slower than monotonic deque.
  - name:
      ko: 무차별 대입
      en: Brute Force
    complexity: O(nk) time / O(n) space
    type: distractor
    why:
      ko: 각 윈도우마다 k개 원소를 순회하며 최댓값을 계산합니다. k가 크면 매우 비효율적입니다.
      en: For each window, scan all k elements to find the max. Becomes very slow when k is large.
  - name:
      ko: 균형 이진 탐색 트리 (TreeMap)
      en: Balanced BST (TreeMap)
    complexity: O(n log k) time / O(k) space
    type: distractor
    why:
      ko: 자가 균형 트리에 윈도우 내 원소를 저장하여 최댓값을 O(log k)에 조회합니다. 작동하지만 복잡하고 필요 이상으로 정교합니다.
      en: Store window elements in a balanced tree for O(log k) max queries. Works but unnecessarily complex.
logic:
  format: slot
  slots:
  - label:
      ko: '초기화: 결과 배열과 데큐 준비'
      en: Initialize output and monotonic deque
    indent: 0
    options:
    - code: 'q = collections.deque()  # index'
      type: good
      why:
        ko: 데큐는 인덱스를 저장하여 윈도우 범위를 추적합니다. 두 포인터 l, r도 함께 초기화됩니다.
        en: Initialize the deque to store indices for tracking window boundaries, plus left and right pointers.
    - code: 'q = []  # list'
      type: distractor
      why:
        ko: 일반 리스트로는 앞에서 제거(popleft)가 O(n)이 되어 전체 복잡도가 증가합니다.
        en: List's popleft is O(n); use deque for O(1) operations at both ends.
    - code: 'q = collections.deque()  # value'
      type: distractor
      why:
        ko: 값을 저장하면 어떤 원소가 현재 윈도우에 속해 있는지 알 수 없습니다.
        en: Storing values instead of indices prevents us from checking window membership.
  - label:
      ko: '메인 루프: 배열 순회'
      en: Main loop to traverse array
    indent: 0
    options:
    - code: 'while r < len(nums):'
      type: good
      why:
        ko: 오른쪽 포인터 r을 배열 끝까지 이동시키며 각 위치에서 윈도우를 처리합니다.
        en: Iterate through the array with the right pointer to process each potential window position.
    - code: 'while r < len(nums) - k:'
      type: distractor
      why:
        ko: 마지막 윈도우를 처리하지 못합니다.
        en: Stops before the last window, missing the final output.
    - code: 'while r < len(nums) - 1:'
      type: distractor
      why:
        ko: 마지막 원소를 포함하는 윈도우를 놓칩니다.
        en: Misses processing the window containing the last element.
  - label:
      ko: '데큐 유지: 더 작은 값 제거'
      en: Maintain monotonic property by removing smaller values
    indent: 1
    options:
    - code: 'while q and nums[q[-1]] < nums[r]:'
      type: good
      why:
        ko: 현재 원소보다 작은 기존 원소들은 절대 최댓값이 될 수 없으므로 제거합니다. 이렇게 하면 데큐는 항상 감소 순서를 유지합니다.
        en: Any element smaller than the current one can never be the max, so remove it. This maintains descending order in the deque.
    - code: 'while q and nums[q[-1]] <= nums[r]:'
      type: distractor
      why:
        ko: 같은 값도 제거하여 중복된 최댓값을 놓칠 수 있습니다.
        en: Removes equal elements unnecessarily, potentially losing duplicate maxima.
    - code: 'while q and nums[q[-1]] > nums[r]:'
      type: distractor
      why:
        ko: 더 큰 값을 제거하므로 단조성이 깨지고 최댓값을 잃게 됩니다.
        en: Removes larger elements, destroying the monotonic property and losing the maximum.
    - code: 'while q and nums[q[0]] < nums[r]:'
      type: distractor
      why:
        ko: 데큐의 앞(오래된 데이터)을 확인하면 데큐 구조가 망가집니다.
        en: Checking the front instead of back disrupts the deque structure and invariant.
  - label:
      ko: 현재 원소 추가
      en: Append current index to deque
    indent: 1
    options:
    - code: q.append(r)
      type: good
      why:
        ko: 더 작은 값들을 제거한 후, 현재 원소의 인덱스를 데큐의 맨 뒤에 추가합니다.
        en: After removing smaller elements, add the current index to the back of the deque.
    - code: q.appendleft(r)
      type: distractor
      why:
        ko: 앞에 추가하면 최신 원소가 잘못된 위치에 들어가 모든 논리가 깨집니다.
        en: Appending to the front puts the newest element in the wrong position.
    - code: q.append(nums[r])
      type: distractor
      why:
        ko: 값을 저장하면 나중에 윈도우 범위를 확인할 수 없습니다.
        en: Storing the value instead of index prevents window boundary checks later.
  - label:
      ko: '윈도우 경계 유지: 범위 밖 원소 제거'
      en: Remove out-of-window elements from front
    indent: 1
    options:
    - code: 'if l > q[0]:'
      type: good
      why:
        ko: 왼쪽 포인터 l이 데큐의 맨 앞(최댓값) 인덱스를 넘으면, 그 원소는 현재 윈도우 범위를 벗어났으므로 제거합니다.
        en: If the left pointer passes the front element's index, that element is outside the current window and must be removed.
    - code: 'if l >= q[0]:'
      type: distractor
      why:
        ko: 오프셋 에러로 아직 윈도우 내에 있는 원소도 제거됩니다.
        en: 'Off-by-one error: removes elements that are still in the window.'
    - code: 'if r - l >= k:'
      type: distractor
      why:
        ko: 잘못된 윈도우 경계 체크로 실제 데큐의 상태와 맞지 않을 수 있습니다.
        en: Incorrect window boundary check; should verify against the actual front of the deque.
  - label:
      ko: '결과 기록: 윈도우가 완성되면 최댓값 출력'
      en: Record maximum when window is complete
    indent: 1
    options:
    - code: output.append(nums[q[0]])
      type: good
      why:
        ko: 윈도우 크기가 k에 도달하면 (r+1 >= k), 데큐의 맨 앞 원소가 현재 윈도우의 최댓값입니다.
        en: Once the window reaches size k, the front of the deque holds the maximum of the current window.
    - code: output.append(nums[q[-1]])
      type: distractor
      why:
        ko: 데큐의 뒤는 최솟값 쪽이므로 잘못된 결과를 출력합니다.
        en: The back of the deque holds the smallest value, not the maximum.
    - code: output.append(q[0])
      type: distractor
      why:
        ko: 값이 아닌 인덱스를 저장하므로 잘못된 출력입니다.
        en: Appends the index instead of the value from nums.
    - code: output.append(max(nums[l:r+1]))
      type: distractor
      why:
        ko: 매번 전체 윈도우를 다시 계산하므로 O(nk) 복잡도로 최적화의 이점을 잃습니다.
        en: Recalculates the max for each window, negating the O(n) optimization.
trace:
  code:
  - 'class Solution:'
  - '    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:'
  - '        output = []'
  - '        q = collections.deque()  # index'
  - '        l = r = 0'
  - '        # O(n) O(n)'
  - '        while r < len(nums):'
  - '            # pop smaller values from q'
  - '            while q and nums[q[-1]] < nums[r]:'
  - '                q.pop()'
  - '            q.append(r)'
  - ''
  - '            # remove left val from window'
  - '            if l > q[0]:'
  - '                q.popleft()'
  - ''
  - '            if (r + 1) >= k:'
  - '                output.append(nums[q[0]])'
  - '                l += 1'
  - '            r += 1'
  - ''
  - '        return output'
  cases:
  - input: '[1,3,-1,-3,5,3,6,7]

      3'
    expected: '[3,3,5,5,6,7]'
  - input: '[1]

      1'
    expected: '[1]'
  worked_example:
    input: '[1,3,-1,-3,5,3,6,7]

      3'
    steps:
    - ko: 'r=0,1: 윈도우가 아직 크기 3에 미달. 데큐 = [1] (3의 인덱스)'
      en: 'r=0,1: Window not yet size 3. Deque = [1] after processing 3.'
    - ko: 'r=2 (첫 출력): 윈도우 [1,3,-1] 완성. 데큐 앞 = nums[1] = 3. output=[3]'
      en: 'r=2 (first output): Window [1,3,-1] complete. Front of deque = nums[1] = 3. output=[3]'
    - ko: 'r=3,4: 더 큰 값 5가 들어오므로 3의 인덱스도 제거. 데큐 = [4] (5의 인덱스). output=[3,3,5,...]'
      en: 'r=4: Larger value 5 arrives, smaller elements removed. Deque = [4]. Next outputs: [3,3,5,...]'
    - ko: 'r=5,6,7: 유사하게 각 윈도우의 최댓값을 데큐 앞에서 추출. 최종 output=[3,3,5,5,6,7]'
      en: 'r=5-7: Continue tracking maxima. Final output = [3,3,5,5,6,7]'
    answer: '[3,3,5,5,6,7]'
solution:
  code: "class Solution:\n    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:\n        output = []\n        q = collections.deque()  # index\n        l = r = 0\n        # O(n) O(n)\n        while r < len(nums):\n            # pop smaller values from q\n            while q and nums[q[-1]] < nums[r]:\n                q.pop()\n            q.append(r)\n\n            # remove left val from window\n            if l > q[0]:\n                q.popleft()\n\n            if (r + 1) >= k:\n                output.append(nums[q[0]])\n                l += 1\n            r += 1\n\n        return output\n"
  complexity:
    time: O(n)
    space: O(k)
  followup:
  - ko: '만약 여러 슬라이딩 윈도우 쿼리가 주어진다면? (예: 같은 배열에 대해 k=2, k=3, k=5로 각각 최댓값 구하기)'
    en: If multiple queries were given (e.g., find max for k=2, k=3, k=5 on the same array), how would you optimize?
  - ko: 음수와 양수가 섞여 있거나 모두 음수인 경우, 알고리즘이 여전히 정확한가?
    en: Does the algorithm handle negative numbers correctly? Can all elements be negative?
  - ko: k=1인 경우는 어떻게 처리되나? 이 경우 최적화는 가능한가?
    en: What is the edge case when k=1? Can this be optimized further?
```