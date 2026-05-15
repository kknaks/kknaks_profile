---
created: '2026-05-15'
date: '2026-05-15'
day: Day 13
difficulty: medium
id: A-013
source:
  curated_in:
  - neetcode150
  number: 11
  platform: leetcode
  slug: container-with-most-water
  url: https://leetcode.com/problems/container-with-most-water/
status: draft
tags:
- array
- two-pointers
- greedy
title:
  en: Container With Most Water
  ko: 물이 가장 많은 용기
today: true
type: algorithm
updated: '2026-05-15'
visible: true
---

# 물이 가장 많은 용기

## Data

```yaml
problem:
  title:
    ko: 물이 가장 많은 용기
    en: Container With Most Water
  statement:
    en: 'You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).


      Find two lines that together with the x-axis form a container, such that the container contains the most water.


      Return the maximum amount of water a container can store.


      Notice that you may not slant the container.'
    ko: '길이가 n인 정수 배열 height가 주어집니다. n개의 수직선이 있고, i번째 선의 끝점은 (i, 0)과 (i, height[i])입니다.


      두 선이 x축과 함께 만드는 용기가 가장 많은 물을 담을 수 있도록 두 선을 찾으세요.


      용기가 담을 수 있는 물의 최대량을 반환하세요.


      용기를 기울일 수 없다는 점에 유의하세요.'
  constraints:
  - n == height.length
  - 2 ≤ n ≤ 10^5
  - 0 ≤ height[i] ≤ 10^4
  io:
  - input: '[1,8,6,2,5,4,8,3,7]'
    output: '49'
  - input: '[1,1]'
    output: '1'
clarifying:
  items:
  - q:
      en: How is the area of water calculated between two lines?
      ko: 두 선 사이의 물의 넓이는 어떻게 계산되나요?
    type: good
    why:
      en: Understanding the area formula (width × min height) is essential to solve this problem correctly.
      ko: 넓이 공식(너비 × 최소 높이)을 이해하는 것이 문제를 올바르게 풀기 위해 필수적입니다.
  - q:
      en: Can we use any two lines with different indices?
      ko: 다른 인덱스의 임의의 두 선을 사용할 수 있나요?
    type: good
    why:
      en: Clarifying that we must choose exactly two distinct indices is crucial for understanding the problem scope.
      ko: 정확히 두 개의 서로 다른 인덱스를 선택해야 한다는 것을 명확히 하는 것이 문제의 범위를 이해하는 데 중요합니다.
  - q:
      en: Why should we move the pointer pointing to the smaller height?
      ko: 더 작은 높이를 가진 포인터를 왜 움직여야 하나요?
    type: good
    why:
      en: Understanding the greedy insight—that moving the taller line can only decrease area—is key to the two-pointer algorithm.
      ko: 더 큰 높이의 선을 움직이면 항상 넓이가 감소한다는 탐욕 알고리즘의 핵심을 이해하는 것이 중요합니다.
  - q:
      en: What if two adjacent lines have the same height?
      ko: 인접한 두 선의 높이가 같으면 어떻게 하나요?
    type: good
    why:
      en: This edge case helps verify understanding of the algorithm's handling of equal heights and the elif condition.
      ko: 이 경계 경우는 동일한 높이와 elif 조건을 처리하는 알고리즘의 이해를 검증하는 데 도움이 됩니다.
  - q:
      en: Must we check all possible pairs of lines?
      ko: 모든 가능한 선의 쌍을 확인해야 하나요?
    type: distractor
    why:
      en: The two-pointer approach doesn't check all pairs; it strategically prunes the search space, which is why it's O(n) not O(n²).
      ko: 두 포인터 접근법은 모든 쌍을 확인하지 않으며, 전략적으로 탐색 공간을 줄이기 때문에 O(n²)이 아니라 O(n)입니다.
  - q:
      en: Can the container be oriented vertically instead of horizontally?
      ko: 용기를 수평이 아닌 수직으로 배치할 수 있나요?
    type: distractor
    why:
      en: The problem explicitly states 'you may not slant the container,' meaning it must remain horizontal with vertical walls.
      ko: 문제에서 명시적으로 '용기를 기울일 수 없다'고 했으므로 수평을 유지하고 수직 벽이 있어야 합니다.
  - q:
      en: Do we need to modify the original height array?
      ko: 원본 높이 배열을 수정해야 하나요?
    type: distractor
    why:
      en: The solution only reads the array and tracks indices; modifying the array is unnecessary and inefficient.
      ko: 솔루션은 배열을 읽고 인덱스를 추적할 뿐이며, 배열을 수정하는 것은 불필요하고 비효율적입니다.
approach:
  items:
  - name:
      en: Two Pointers
      ko: 두 포인터
    complexity: O(n) time / O(1) space
    type: good
    why:
      en: Start from both ends and move the pointer at the shorter line inward. This greedy approach guarantees finding the maximum in a single pass.
      ko: 양쪽 끝에서 시작하여 더 짧은 선의 포인터를 안쪽으로 이동합니다. 이 탐욕 알고리즘은 한 번의 반복으로 최댓값을 찾는 것을 보장합니다.
  - name:
      en: Brute Force (All Pairs)
      ko: 완전 탐색 (모든 쌍)
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      en: Try every possible pair of indices and track the maximum area. Simple but inefficient for large inputs.
      ko: 모든 가능한 인덱스 쌍을 시도하고 최대 넓이를 추적합니다. 간단하지만 큰 입력에는 비효율적입니다.
  - name:
      en: Sorting + Two Pointers
      ko: 정렬 + 두 포인터
    complexity: O(n log n) time / O(1) space
    type: distractor
    why:
      en: Sort by height first, then apply two pointers. The sorting overhead makes this slower than the direct two-pointer approach.
      ko: 먼저 높이로 정렬한 다음 두 포인터를 적용합니다. 정렬 오버헤드로 인해 직접 두 포인터 접근법보다 느립니다.
  - name:
      en: Hash Map Storage
      ko: 해시맵 저장
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      en: Store heights in a hash map and iterate through pairs. Adds unnecessary space complexity without performance benefit.
      ko: 높이를 해시맵에 저장하고 쌍을 반복합니다. 성능 이점 없이 불필요한 공간 복잡도를 추가합니다.
logic:
  format: slot
  slots:
  - label:
      en: Initialize pointers at opposite ends
      ko: 양쪽 끝에 포인터 초기화
    indent: 0
    options:
    - code: l, r = 0, len(height) - 1
      type: good
      why:
        en: Setting up left pointer at index 0 and right pointer at len(height)-1 gives the maximum initial width.
        ko: 왼쪽 포인터를 인덱스 0에, 오른쪽 포인터를 len(height)-1에 설정하면 최대 초기 너비를 얻습니다.
    - code: l, r = 0, len(height) // 2
      type: distractor
      why:
        en: Starting from the middle limits the initial width and wastes potential container area.
        ko: 중간에서 시작하면 초기 너비가 제한되고 잠재적 용기 넓이가 낭비됩니다.
    - code: l, r = 1, len(height) - 2
      type: distractor
      why:
        en: Excluding the boundary indices skips valid containers that might be optimal.
        ko: 경계 인덱스를 제외하면 최적일 수 있는 유효한 용기를 건너뜁니다.
  - label:
      en: Initialize maximum area tracker
      ko: 최대 넓이 추적기 초기화
    indent: 0
    options:
    - code: res = 0
      type: good
      why:
        en: Starting res at 0 ensures any valid container area will be considered as a potential maximum.
        ko: res를 0에서 시작하면 유효한 모든 용기 넓이가 최댓값의 후보로 고려됩니다.
    - code: res = float('-inf')
      type: distractor
      why:
        en: Using negative infinity is unnecessary when all valid areas are non-negative.
        ko: 모든 유효한 넓이가 음이 아닐 때 음의 무한대를 사용하는 것은 불필요합니다.
    - code: res = height[0] * (len(height) - 1)
      type: distractor
      why:
        en: Pre-computing with the first element doesn't initialize properly and conflicts with the main loop logic.
        ko: 첫 번째 요소로 사전 계산하면 제대로 초기화되지 않고 메인 루프 로직과 충돌합니다.
  - label:
      en: Loop while pointers haven't crossed
      ko: 포인터가 교차할 때까지 반복
    indent: 0
    options:
    - code: 'while l < r:'
      type: good
      why:
        en: The condition l < r ensures we only evaluate valid pairs of distinct indices and stop when they meet.
        ko: l < r 조건은 서로 다른 인덱스의 유효한 쌍만 평가하고 포인터가 만날 때 멈춥니다.
    - code: 'while l <= r:'
      type: distractor
      why:
        en: Using <= includes the case where l == r, which compares a line with itself—invalid.
        ko: <= 를 사용하면 l == r인 경우가 포함되는데, 이는 한 선을 자신과 비교하는 것으로 유효하지 않습니다.
    - code: 'while r - l > 1:'
      type: distractor
      why:
        en: This skips the case where we have exactly two adjacent lines, which may contain valid solutions.
        ko: 이것은 정확히 두 개의 인접한 선이 있는 경우를 건너뛰는데, 이는 유효한 솔루션을 포함할 수 있습니다.
  - label:
      en: Calculate area and track maximum
      ko: 넓이 계산 및 최댓값 추적
    indent: 1
    options:
    - code: res = max(res, min(height[l], height[r]) * (r - l))
      type: good
      why:
        en: Area = min(height[l], height[r]) × (r - l). The minimum height limits capacity, and (r - l) is the width. Update res with the maximum found so far.
        ko: 넓이 = min(height[l], height[r]) × (r - l). 최소 높이가 용량을 제한하고 (r - l)이 너비입니다. res를 지금까지 찾은 최댓값으로 업데이트합니다.
    - code: res = max(res, height[l] * height[r] * (r - l))
      type: distractor
      why:
        en: Multiplying both heights instead of taking the minimum incorrectly calculates the area.
        ko: 최솟값을 구하지 않고 두 높이를 모두 곱하면 넓이가 잘못 계산됩니다.
    - code: res = max(res, (height[l] + height[r]) * (r - l))
      type: distractor
      why:
        en: Adding heights instead of taking the minimum gives an invalid area calculation.
        ko: 최솟값을 구하지 않고 높이를 더하면 유효하지 않은 넓이 계산이 됩니다.
  - label:
      en: Move pointer at smaller height
      ko: 더 작은 높이의 포인터 이동
    indent: 1
    options:
    - code: 'if height[l] < height[r]:'
      type: good
      why:
        en: If left height is smaller, moving left inward might find a taller line and increase area. Moving right would only decrease width while capacity is already limited by the smaller left height.
        ko: 왼쪽 높이가 더 작으면 왼쪽을 안쪽으로 이동하면 더 큰 선을 찾을 수 있고 넓이가 증가할 수 있습니다. 오른쪽을 이동하면 용량이 이미 더 작은 왼쪽 높이로 제한되어 너비만 감소합니다.
    - code: 'if height[l] > height[r]:'
      type: distractor
      why:
        en: Reversing the condition moves the taller line, which can only decrease potential area without benefit.
        ko: 조건을 반대로 하면 더 큰 선을 이동하는데, 이는 잇점 없이 잠재적 넓이만 감소시킵니다.
    - code: 'if l < r // 2:'
      type: distractor
      why:
        en: Using a position-based condition ignores the actual heights, losing the greedy optimization.
        ko: 위치 기반 조건을 사용하면 실제 높이를 무시하여 탐욕 최적화를 잃습니다.
  - label:
      en: Move left pointer inward
      ko: 왼쪽 포인터를 안쪽으로 이동
    indent: 2
    options:
    - code: l += 1
      type: good
      why:
        en: Increment l to move toward the right, exploring taller lines on the left side that might improve the result.
        ko: l을 증가시켜 오른쪽으로 이동하면서 결과를 개선할 수 있는 왼쪽의 더 큰 선을 탐색합니다.
    - code: l -= 1
      type: distractor
      why:
        en: Decrementing l moves away from center, contradicting the inward-movement strategy.
        ko: l을 감소시키면 중심에서 멀어지는데, 이는 안쪽 이동 전략에 모순됩니다.
    - code: l += 2
      type: distractor
      why:
        en: Skipping lines by incrementing by 2 might miss the optimal container location.
        ko: 2씩 증가시키면 선을 건너뛰어 최적의 용기 위치를 놓칠 수 있습니다.
  - label:
      en: Move right pointer inward (when applicable)
      ko: 오른쪽 포인터를 안쪽으로 이동 (해당하는 경우)
    indent: 2
    options:
    - code: r -= 1
      type: good
      why:
        en: When left height is greater than or equal to right height, moving right inward explores taller lines on the right side.
        ko: 왼쪽 높이가 오른쪽 높이보다 크거나 같을 때, 오른쪽을 안쪽으로 이동하면서 오른쪽 더 큰 선을 탐색합니다.
    - code: r += 1
      type: distractor
      why:
        en: Incrementing r moves away from center, opposite to the intended inward movement.
        ko: r을 증가시키면 중심에서 멀어지는데, 이는 의도한 안쪽 이동과 반대입니다.
    - code: r -= 2
      type: distractor
      why:
        en: Skipping every other line may miss potentially optimal containers.
        ko: 매 다른 선을 건너뛰면 잠재적으로 최적의 용기를 놓칠 수 있습니다.
trace:
  code:
  - 'class Solution:'
  - '    def maxArea(self, height: List[int]) -> int:'
  - '        l, r = 0, len(height) - 1'
  - '        res = 0'
  - ''
  - '        while l < r:'
  - '            res = max(res, min(height[l], height[r]) * (r - l))'
  - '            if height[l] < height[r]:'
  - '                l += 1'
  - '            elif height[r] <= height[l]:'
  - '                r -= 1'
  - '            '
  - '        return res'
  cases:
  - input: '[1,8,6,2,5,4,8,3,7]'
    expected: '49'
  - input: '[1,1]'
    expected: '1'
  worked_example:
    input: '[1,8,6,2,5,4,8,3,7]'
    steps:
    - en: Start with l=0 (height 1), r=8 (height 7). Area = min(1,7) × 8 = 8. Since height[0] < height[8], move left pointer right.
      ko: l=0 (높이 1), r=8 (높이 7)로 시작합니다. 넓이 = min(1,7) × 8 = 8. height[0] < height[8]이므로 왼쪽 포인터를 오른쪽으로 이동합니다.
    - en: Now l=1 (height 8), r=8 (height 7). Area = min(8,7) × 7 = 49. Update max to 49. Since height[1] > height[8], move right pointer left.
      ko: 이제 l=1 (높이 8), r=8 (높이 7). 넓이 = min(8,7) × 7 = 49. 최댓값을 49로 업데이트합니다. height[1] > height[8]이므로 오른쪽 포인터를 왼쪽으로 이동합니다.
    - en: 'Continue iterations: l=1, r=7 (height 3) gives 3×6=18; l=1, r=6 (height 8) gives 8×5=40; keep moving right pointer. Maximum remains 49.'
      ko: '계속 반복: l=1, r=7 (높이 3)는 3×6=18을 제공; l=1, r=6 (높이 8)은 8×5=40을 제공; 오른쪽 포인터를 계속 이동합니다. 최댓값은 여전히 49입니다.'
    - en: 'Eventually pointers cross (l ≥ r). The algorithm terminates and returns the maximum area found: 49.'
      ko: 결국 포인터가 교차합니다 (l ≥ r). 알고리즘이 종료되고 찾은 최대 넓이인 49를 반환합니다.
    answer: '49'
solution:
  code: "class Solution:\n    def maxArea(self, height: List[int]) -> int:\n        l, r = 0, len(height) - 1\n        res = 0\n\n        while l < r:\n            res = max(res, min(height[l], height[r]) * (r - l))\n            if height[l] < height[r]:\n                l += 1\n            elif height[r] <= height[l]:\n                r -= 1\n            \n        return res\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - en: What if we need to find k containers (pairs of lines) instead of just the maximum one? How would the approach change?
    ko: 최댓값 하나만 찾는 대신 k개의 용기(선의 쌍)를 찾아야 한다면 어떻게 접근을 바꿀까요?
  - en: What if the lines can have different widths (not just single points)? How would area calculation change?
    ko: 선이 너비가 다를 수 있다면(단일 점이 아닌) 넓이 계산은 어떻게 변할까요?
  - en: Can we optimize further if the heights follow a specific pattern (e.g., sorted, or with duplicates)?
    ko: '높이가 특정 패턴(예: 정렬됨 또는 중복)을 따르면 더 최적화할 수 있을까요?'
```