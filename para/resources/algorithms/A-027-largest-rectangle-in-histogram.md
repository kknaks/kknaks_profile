---
created: '2026-06-02'
date: '2026-06-02'
day: Day 27
difficulty: hard
id: A-027
source:
  curated_in:
  - neetcode150
  number: 84
  platform: leetcode
  slug: largest-rectangle-in-histogram
  url: https://leetcode.com/problems/largest-rectangle-in-histogram/
tags:
- array
- stack
- monotonic-stack
title:
  en: Largest Rectangle in Histogram
  ko: 히스토그램에서 가장 큰 직사각형
today: false
type: algorithm
updated: '2026-06-02'
visible: true
---

# 히스토그램에서 가장 큰 직사각형

## Data

```yaml
problem:
  title:
    ko: 히스토그램에서 가장 큰 직사각형
    en: Largest Rectangle in Histogram
  statement:
    ko: 정수 배열 heights가 주어지며, 각 원소는 너비가 1인 히스토그램의 막대 높이를 나타냅니다. 히스토그램에서 만들 수 있는 가장 큰 직사각형의 넓이를 반환하세요.
    en: Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
  constraints:
  - 1 ≤ heights.length ≤ 10^5
  - 0 ≤ heights[i] ≤ 10^4
  io:
  - input: '[2,1,5,6,2,3]'
    output: '10'
  - input: '[2,4]'
    output: '4'
clarifying:
  items:
  - q:
      ko: 히스토그램에서 각 막대의 너비는 얼마입니까?
      en: What is the width of each bar in the histogram?
    type: good
    why:
      ko: 문제의 기본이 되는 조건입니다. 각 막대의 너비는 정확히 1이므로, 직사각형의 넓이 = 높이 × (포함된 막대의 개수)입니다.
      en: This is fundamental to the problem. Each bar has width exactly 1, so the area of a rectangle = height × (number of bars it spans).
  - q:
      ko: 직사각형이 연속되지 않은 막대들을 건너뛰고 포함할 수 있습니까?
      en: Can a rectangle span non-consecutive bars (skipping shorter bars)?
    type: good
    why:
      ko: 아니요, 직사각형은 반드시 연속된 막대들을 포함해야 합니다. 더 짧은 막대를 건너뛸 수 없습니다.
      en: No, rectangles must span consecutive bars. A shorter bar in between breaks the continuity.
  - q:
      ko: 직사각형의 높이는 어떻게 결정됩니까?
      en: What determines the height of a rectangle?
    type: good
    why:
      ko: 직사각형의 높이는 그 범위 내의 가장 짧은 막대의 높이입니다. 모든 막대가 최소한 그 높이 이상이어야 합니다.
      en: The height of a rectangle is limited by the shortest bar within its range. All bars must be at least that tall.
  - q:
      ko: 예제 [2,1,5,6,2,3]에서 최대 넓이가 12가 아니라 10인 이유는?
      en: In example [2,1,5,6,2,3], why is the maximum area 10, not 12?
    type: distractor
    why:
      ko: 인덱스 2-3 (높이 5,6)의 범위에서 최소 높이는 5이므로 넓이는 2×5=10입니다. 높이 6으로 계산하려면 인덱스 2의 높이도 6 이상이어야 하는데 5이므로 불가능합니다.
      en: Bars at indices 2-3 have min height 5, so area = 2×5=10. Using height 6 would require bar at index 2 to also be ≥6, but it's 5.
  - q:
      ko: 모든 막대의 높이가 0이면 최대 넓이는?
      en: If all bars have height 0, what is the maximum area?
    type: good
    why:
      ko: 0입니다. 넓이 = 높이 × 너비 = 0 × n = 0이므로 모든 직사각형의 넓이는 0입니다.
      en: 0. Area = height × width = 0 × n = 0 for any rectangle, since all heights are 0.
  - q:
      ko: 최적의 직사각형은 단 하나의 막대로만 구성될 수 있습니까?
      en: Can the optimal rectangle consist of just a single bar?
    type: good
    why:
      ko: '네, 그 막대가 주변 어떤 연속된 그룹보다 크면 가능합니다. 예: [1,1,5,1,1]에서 인덱스 2의 막대 하나가 최적입니다.'
      en: Yes, if that bar is taller than any contiguous group around it. For example, in [1,1,5,1,1], the single bar at index 2 is optimal.
  - q:
      ko: 정렬된 배열이 입력될까요?
      en: Is the input array always sorted?
    type: distractor
    why:
      ko: 아니요, 배열의 순서는 임의적입니다. 이 임의성 때문에 이 문제가 도전적입니다.
      en: No, heights appear in arbitrary order. This arbitrary ordering is what makes the problem challenging.
approach:
  items:
  - name:
      ko: Monotonic Stack (단조 스택)
      en: Monotonic Stack
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 스택을 사용하여 막대들을 증가 순서로 유지합니다. 더 짧은 막대를 만나면 스택의 더 긴 막대들을 꺼내며 그들의 최대 너비를 계산합니다. 각 원소는 정확히 한 번씩 push되고 pop되므로 O(n)입니다.
      en: Maintain a stack of bars in increasing height order. When a shorter bar is encountered, pop taller bars and calculate their maximum widths. Each bar is pushed and popped exactly once, giving O(n) time.
  - name:
      ko: Brute Force (모든 구간 확인)
      en: 'Brute Force: Check all subarrays'
    complexity: O(n^3) time / O(1) space
    type: distractor
    why:
      ko: 모든 (좌, 우) 쌍에 대해 그 범위 내의 최소 높이를 찾아 넓이를 계산합니다. 이해하기 쉽지만 입력이 크면 매우 느립니다.
      en: For each pair of left and right boundaries, scan to find minimum height. Simple to understand but extremely slow for large inputs.
  - name:
      ko: 분할과 정복 (Divide and Conquer)
      en: Divide and Conquer
    complexity: O(n log n) time / O(log n) space
    type: distractor
    why:
      ko: 배열을 재귀적으로 분할하여 최소 높이 위치를 찾고 결과를 합칩니다. 우아하지만 monotonic stack보다 느립니다.
      en: Recursively split the array, find minimum height divider, and combine. Elegant but slower than the monotonic stack approach.
  - name:
      ko: 각 막대의 경계 찾기
      en: 'Optimized Brute Force: Find bar boundaries'
    complexity: O(n^2) time / O(n) space
    type: distractor
    why:
      ko: 각 막대에 대해 그 높이 이상인 왼쪽 경계와 오른쪽 경계를 찾아 최대 너비를 계산합니다. 여전히 O(n^2)이며 스택의 깊은 통찰을 활용하지 못합니다.
      en: For each bar, find leftmost and rightmost positions where heights are >= current height. Still O(n^2) and doesn't use the stack insight.
logic:
  format: slot
  slots:
  - label:
      ko: 스택 초기화
      en: Initialize stack
    indent: 0
    options:
    - code: 'stack = []  # pair: (index, height)'
      type: good
      why:
        ko: 비어있는 스택을 만들어서 (인덱스, 높이) 쌍들을 저장할 준비를 합니다.
        en: Create an empty stack to store (index, height) pairs.
    - code: stack = None
      type: distractor
      why:
        ko: None으로 초기화하면 append() 메서드를 호출할 수 없습니다.
        en: Can't call append() on None; this would crash.
    - code: stack = [heights[0]]
      type: distractor
      why:
        ko: 첫 번째 높이를 미리 넣으면 이후의 로직이 복잡해지고 틀리게 됩니다.
        en: Prepopulating with the first bar complicates the logic and introduces errors.
  - label:
      ko: 모든 막대를 순회
      en: Iterate through each bar
    indent: 0
    options:
    - code: 'for i, h in enumerate(heights):'
      type: good
      why:
        ko: 각 막대의 인덱스 i와 높이 h를 모두 추적하며 왼쪽에서 오른쪽으로 진행합니다.
        en: Loop through each bar from left to right, tracking both index and height.
    - code: 'for h in heights:'
      type: distractor
      why:
        ko: 인덱스를 놓치게 되면 막대의 위치 정보가 없어서 직사각형의 너비를 계산할 수 없습니다.
        en: Without the index, you can't determine the width of the rectangle.
    - code: 'for i in range(len(heights)):'
      type: distractor
      why:
        ko: 이렇게 하면 높이를 직접 가져오지 못해 매번 heights[i]를 조회해야 합니다.
        en: This requires manually looking up heights[i] each iteration.
  - label:
      ko: 스택의 상단이 현재 막대보다 높은지 확인
      en: 'Pop condition: while top is taller'
    indent: 1
    options:
    - code: 'while stack and stack[-1][1] > h:'
      type: good
      why:
        ko: 스택의 맨 위 막대가 현재 막대보다 크면, 스택의 막대를 꺼내서 그것의 최대 범위를 계산할 수 있습니다.
        en: If the top bar is taller than the current bar, it's time to calculate the maximum width for that taller bar.
    - code: 'if stack and stack[-1][1] > h:'
      type: distractor
      why:
        ko: if를 사용하면 한 번만 확인하므로, 더 많은 막대들이 pop될 수 있는 경우를 놓칩니다.
        en: Using if instead of while misses cases where multiple bars need to be popped.
    - code: 'while stack and stack[-1][1] >= h:'
      type: distractor
      why:
        ko: '''>='' 조건은 같은 높이의 막대들을 잘못 처리합니다. 같은 높이면 유지해야 합니다.'
        en: '>= would cause equal-height bars to be popped, leading to incorrect calculations.'
  - label:
      ko: 꺼낸 막대의 넓이 계산
      en: Calculate area for popped bar
    indent: 2
    options:
    - code: maxArea = max(maxArea, height * (i - index))
      type: good
      why:
        ko: 꺼낸 막대의 높이로 만들 수 있는 직사각형의 너비는 (현재 위치 i - 꺼낸 막대의 위치)이므로, 넓이 = 높이 × (i - index)입니다.
        en: The width extends from the popped bar's original position (index) to just before the current bar (i), giving width = i - index.
    - code: maxArea = max(maxArea, height * (i - index - 1))
      type: distractor
      why:
        ko: i - index - 1은 off-by-one 오류입니다. 너비는 정확히 i - index입니다.
        en: Subtracting 1 is an off-by-one error; the width is exactly i - index.
    - code: maxArea = max(maxArea, height * i)
      type: distractor
      why:
        ko: index를 빼지 않으면 왼쪽 경계를 무시하게 되어 잘못된 계산입니다.
        en: Without subtracting the index, you ignore the left boundary of the rectangle.
  - label:
      ko: 시작 위치 갱신
      en: Update start position
    indent: 2
    options:
    - code: start = index
      type: good
      why:
        ko: 꺼낸 막대의 위치를 start로 기록하면, 현재 막대가 그 위치까지 왼쪽으로 확장될 수 있음을 나타냅니다.
        en: Recording the popped bar's index as the new start allows the current bar to extend leftward to fill that gap.
    - code: start = i - 1
      type: distractor
      why:
        ko: start를 i-1로 설정하면 스택에서 꺼낸 막대들의 왼쪽 위치 정보를 잃게 됩니다.
        en: Setting start to i-1 loses information about how far left the current bar can extend.
    - code: start = 0
      type: distractor
      why:
        ko: 항상 0으로 리셋하면 이전에 꺼낸 막대의 위치가 무시되어 확장 범위가 잘못 계산됩니다.
        en: Always resetting to 0 ignores previously popped bars' positions, causing incorrect range calculations.
  - label:
      ko: 현재 막대를 스택에 추가
      en: Push current bar
    indent: 1
    options:
    - code: stack.append((start, h))
      type: good
      why:
        ko: 확장된 시작 위치(start)와 함께 현재 막대를 스택에 넣어서, 나중에 이 막대의 왼쪽 경계를 알 수 있게 합니다.
        en: Push the bar with its extended start position so we can later determine its left boundary.
    - code: stack.append((i, h))
      type: distractor
      why:
        ko: start를 무시하고 i만 사용하면 왼쪽 확장 정보를 잃게 되어 계산이 틀립니다.
        en: Using i instead of start loses information about leftward extension from popping.
    - code: stack.insert(0, (start, h))
      type: distractor
      why:
        ko: 맨 앞에 삽입하면 O(n)의 시간이 걸리므로 전체 시간복잡도가 O(n²)이 됩니다.
        en: Inserting at the front is O(n), making overall time complexity O(n²).
  - label:
      ko: 남은 막대들 처리
      en: Process remaining bars in stack
    indent: 0
    options:
    - code: 'for i, h in stack:'
      type: good
      why:
        ko: 메인 루프가 끝난 후 스택에 남은 막대들은 오른쪽 끝까지 확장될 수 있으므로, 각각의 최대 범위를 계산합니다.
        en: After the main loop, remaining bars in the stack can extend all the way to the end, so calculate their maximum widths.
    - code: 'for _ in stack:'
      type: distractor
      why:
        ko: 변수를 바인딩하지 않으면 i와 h를 사용할 수 없어서 계산을 할 수 없습니다.
        en: Without binding variables, you can't access the index and height needed for the calculation.
    - code: 'for h, i in stack:'
      type: distractor
      why:
        ko: i와 h의 순서가 바뀌면, 계산에서 인덱스와 높이를 헷갈려서 틀린 결과를 얻습니다.
        en: Swapping the order causes index and height to be confused, producing wrong calculations.
trace:
  code:
  - 'class Solution:'
  - '    def largestRectangleArea(self, heights: List[int]) -> int:'
  - '        maxArea = 0'
  - '        stack = []  # pair: (index, height)'
  - ''
  - '        for i, h in enumerate(heights):'
  - '            start = i'
  - '            while stack and stack[-1][1] > h:'
  - '                index, height = stack.pop()'
  - '                maxArea = max(maxArea, height * (i - index))'
  - '                start = index'
  - '            stack.append((start, h))'
  - ''
  - '        for i, h in stack:'
  - '            maxArea = max(maxArea, h * (len(heights) - i))'
  - '        return maxArea'
  cases:
  - input: '[2,1,5,6,2,3]'
    expected: '10'
  - input: '[2,4]'
    expected: '4'
  worked_example:
    input: '[2,1,5,6,2,3]'
    steps:
    - ko: '초기: maxArea=0, stack=[]'
      en: 'Start: maxArea=0, stack=[]'
    - ko: 'i=0,1,2,3: 스택에 (0,2)→(0,1)→(2,5)→(3,6) 순서로 추가됩니다.'
      en: 'i=0,1,2,3: Add to stack in increasing height order: (0,2), (0,1), (2,5), (3,6)'
    - ko: 'i=4 (h=2): 6과 5를 pop합니다. 5 pop 시 5×(4-2)=10을 계산하고 maxArea=10으로 갱신합니다.'
      en: 'i=4 (h=2): Pop 6, then 5. When popping 5, area=5×(4-2)=10, update maxArea=10'
    - ko: 'i=5 이후: 스택 처리에서 남은 (0,1), (2,2), (5,3)을 확인하지만 10을 초과하는 넓이는 없습니다.'
      en: 'i=5 and finalization: Process remaining bars, but no area exceeds 10'
    answer: '10'
solution:
  code: "class Solution:\n    def largestRectangleArea(self, heights: List[int]) -> int:\n        maxArea = 0\n        stack = []  # pair: (index, height)\n\n        for i, h in enumerate(heights):\n            start = i\n            while stack and stack[-1][1] > h:\n                index, height = stack.pop()\n                maxArea = max(maxArea, height * (i - index))\n                start = index\n            stack.append((start, h))\n\n        for i, h in stack:\n            maxArea = max(maxArea, h * (len(heights) - i))\n        return maxArea\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 막대의 너비가 모두 1이 아니라면 어떻게 수정할까요?
    en: How would the solution change if bar widths are not all 1?
  - ko: 최대 넓이를 만드는 직사각형의 좌우 경계 인덱스를 함께 반환할 수 있을까요?
    en: Can you modify the solution to also return the left and right boundary indices of the optimal rectangle?
  - ko: 음수 높이가 허용된다면 알고리즘은 어떻게 변할까요?
    en: How would the algorithm change if negative heights were allowed?
```