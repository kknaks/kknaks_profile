---
created: '2026-05-16'
date: '2026-05-16'
day: Day 14
difficulty: hard
id: A-014
source:
  curated_in:
  - neetcode150
  number: 42
  platform: leetcode
  slug: trapping-rain-water
  url: https://leetcode.com/problems/trapping-rain-water/
status: draft
tags:
- array
- two-pointers
- dynamic-programming
- stack
- monotonic-stack
title:
  en: Trapping Rain Water
  ko: 빗물 정거량
today: true
type: algorithm
updated: '2026-05-16'
visible: true
---

# 빗물 정거량

## Data

```yaml
problem:
  title:
    ko: 빗물 정거량
    en: Trapping Rain Water
  statement:
    ko: n개의 음이 아닌 정수로 이루어진 배열이 주어지며, 이는 높이 맵을 나타냅니다. 여기서 각 막대의 너비는 1입니다. 비가 내린 후 얼마나 많은 물을 담을 수 있는지 계산하세요.
    en: Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
  constraints:
  - n == height.length
  - 1 ≤ n ≤ 2 × 10⁴
  - 0 ≤ height[i] ≤ 10⁵
  io:
  - input: '[0,1,0,2,1,0,1,3,2,1,2,1]'
    output: '6'
  - input: '[4,2,0,3,2,5]'
    output: '9'
clarifying:
  items:
  - q:
      ko: 각 위치에서 담을 수 있는 물의 양은 무엇에 의해 결정되나?
      en: What determines the amount of water trapped at each position?
    type: good
    why:
      ko: 물의 높이는 그 위치의 양쪽 최대 높이의 최솟값에 의해 결정됨. 이것이 핵심 인사이트
      en: Water level is determined by the minimum of the maximum heights on both sides—the core insight
  - q:
      ko: 왜 두 포인터 방식에서 leftMax < rightMax일 때 항상 왼쪽 포인터를 이동하나?
      en: Why move the left pointer when leftMax < rightMax?
    type: good
    why:
      ko: leftMax가 더 작으면, 현재 위치의 물의 높이가 rightMax와 무관하게 leftMax로 결정되므로 즉시 물의 양을 계산할 수 있음
      en: When leftMax is smaller, the water level at the left position is determined solely by leftMax, allowing immediate calculation
  - q:
      ko: 이 알고리즘의 시간과 공간 복잡도는?
      en: What are the time and space complexity?
    type: good
    why:
      ko: O(n) 시간에 배열을 한 번 순회하며 O(1) 추가 공간만 사용. 이는 DP 접근법의 O(n) 공간보다 최적
      en: Single pass is O(n) time with only O(1) extra space—better than DP's O(n) space
  - q:
      ko: 배열을 정렬해서 이 문제를 풀 수 있을까?
      en: Could you solve this by sorting the array?
    type: distractor
    why:
      ko: 정렬하면 원래 위치 정보가 손실되어 어느 위치에 물이 모이는지 알 수 없음
      en: Sorting loses position information; you cannot determine which locations trap water
  - q:
      ko: 각 위치의 물의 높이는 height[i]와 같은가?
      en: Is water level at position i equal to height[i]?
    type: distractor
    why:
      ko: 아니다. 물의 높이는 min(leftMax, rightMax)이고, 실제 물의 양은 이 높이에서 막대 높이를 뺀 값
      en: No. Water level is min(leftMax, rightMax); trapped water = level minus bar height
  - q:
      ko: 동적 계획법으로 모든 위치의 leftMax와 rightMax를 미리 계산해야 하나?
      en: Do you need to precompute leftMax and rightMax arrays?
    type: distractor
    why:
      ko: 필요 없다. 두 포인터는 필요한 것만 계산하므로 O(1) 공간으로 같은 결과를 얻을 수 있음
      en: No; two-pointer computes on-demand with O(1) space vs DP's O(n) precomputation
  - q:
      ko: 단조 스택으로도 이 문제를 풀 수 있을까?
      en: Can you solve this with a monotonic stack?
    type: good
    why:
      ko: 네, 스택을 유지하면서 더 큰 막대를 만날 때 물의 양을 계산할 수 있음. 하지만 두 포인터가 더 직관적
      en: Yes, by calculating water when encountering taller bars; but two-pointer is more intuitive
  - q:
      ko: 포인터가 만날 때까지 반복해야 하는 이유는?
      en: Why iterate until pointers meet?
    type: good
    why:
      ko: 포인터가 수렴하면 모든 위치의 물의 양이 정확히 한 번씩 계산됨. 이것이 O(n) 시간 복잡도를 보장
      en: Convergence ensures each position's water is calculated exactly once in linear time
approach:
  items:
  - name:
      ko: 완전 탐색 (Brute Force)
      en: Brute Force
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 각 위치마다 왼쪽과 오른쪽 모든 막대를 확인해 최댓값을 찾음. 이해하기 쉽지만 비효율적
      en: For each position, scan all elements left and right for max height. Simple but slow
  - name:
      ko: 동적 계획법 (사전 계산)
      en: Dynamic Programming (Precompute)
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: leftMax[i]와 rightMax[i]를 미리 계산한 후 각 위치에서 물의 양을 계산. O(n) 시간이지만 O(n) 공간 필요
      en: Precompute max arrays, then calculate water. Linear time but requires extra array space
  - name:
      ko: 두 포인터 (최적)
      en: Two Pointers (Optimal)
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 양쪽 끝에서 시작해 더 작은 최댓값을 가진 쪽을 이동. O(n) 시간과 O(1) 공간으로 최적 해결. 면접에 최고의 선택
      en: Start from both ends, move the smaller max side. Optimal space and time; best for interviews
  - name:
      ko: 단조 스택 (Monotonic Stack)
      en: Monotonic Stack
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 스택에 높이를 저장하면서 더 큰 막대를 만날 때 물의 양을 계산. O(n) 시간이지만 O(n) 공간 필요. 다른 스택 문제로의 응용성 있음
      en: Track bars in stack, calculate water when finding taller bars. Linear time/space; teaches stack patterns
  - name:
      ko: 스트리밍 (비현실적)
      en: Streaming (Impractical)
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 배열을 한 번만 스캔하려는 시도는 실제로는 추가 자료구조를 요구하게 되어 공간을 낭비
      en: Streaming attempts require auxiliary data structures, negating space savings
logic:
  format: slot
  slots:
  - label:
      ko: 빈 배열 확인
      en: Handle empty input
    indent: 0
    options:
    - code: 'if not height:'
      type: good
      why:
        ko: 비어있는 배열이면 물을 담을 수 없으므로 0을 반환해야 함
        en: Empty array cannot trap any water, so return 0 immediately
    - code: 'if len(height) == 0:'
      type: distractor
      why:
        ko: 같은 의미지만 `not height`가 더 pythonic하고 간결
        en: Same logic but `not height` is more Pythonic and concise
    - code: 'if height is None:'
      type: distractor
      why:
        ko: None과 빈 배열은 다름. 입력이 배열이므로 None 체크는 불필요
        en: Confuses None with empty list; input is guaranteed to be a list
  - label:
      ko: 양쪽 포인터 초기화
      en: Initialize two pointers
    indent: 0
    options:
    - code: l, r = 0, len(height) - 1
      type: good
      why:
        ko: 배열의 양 끝에서 시작하여 중심으로 수렴하는 두 포인터 방식의 기초
        en: Start from both ends and converge inward; foundational two-pointer setup
    - code: l, r = 0, len(height)
      type: distractor
      why:
        ko: 배열 인덱스는 len(height)-1까지이므로 off-by-one error 발생
        en: Array index goes to len(height)-1, not len(height) (off-by-one error)
    - code: l, r = 1, len(height) - 2
      type: distractor
      why:
        ko: 양 끝의 높이도 계산에 포함되어야 하므로 0과 len(height)-1부터 시작
        en: Boundary elements must be included; start at 0 and len(height)-1
  - label:
      ko: 양쪽 경계의 최대 높이 초기화
      en: Initialize max heights from boundaries
    indent: 0
    options:
    - code: leftMax, rightMax = height[l], height[r]
      type: good
      why:
        ko: 양 끝의 높이는 그 방향의 최대 높이. 이 값들이 물의 수위 상한이 됨
        en: Boundary heights become the initial water level ceilings for each direction
    - code: leftMax, rightMax = 0, 0
      type: distractor
      why:
        ko: 0으로 시작하면 첫 번째 움직임 이후 잘못된 계산이 발생
        en: Starting with 0 would miscalculate water at first position after pointer move
    - code: leftMax, rightMax = height[0], height[len(height)-1]
      type: distractor
      why:
        ko: 같은 결과이지만 변수 l, r을 사용하는 것이 포인터 기반 접근과 일관성 있음
        en: Same result but using l and r is more consistent with pointer-based approach
  - label:
      ko: 주 순회 루프
      en: 'Main loop: two-pointer iteration'
    indent: 0
    options:
    - code: 'while l < r:'
      type: good
      why:
        ko: l과 r이 만날 때까지 계속 반복. 포인터가 수렴할 때 모든 위치의 물의 양이 정확히 한 번씩 계산됨
        en: Continue until pointers converge; all water is calculated exactly once as they move inward
    - code: 'while l <= r:'
      type: distractor
      why:
        ko: l == r인 위치는 이미 처리되었으므로 l < r이어야 함
        en: When l == r, that position should not be processed again
    - code: 'for i in range(len(height)):'
      type: distractor
      why:
        ko: 고정 반복은 두 포인터의 동적 수렴 전략과 맞지 않음
        en: Fixed iteration doesn't match dynamic two-pointer convergence
  - label:
      ko: 좌측 경계 처리 (최대값 업데이트)
      en: 'Process left side: update left max'
    indent: 1
    options:
    - code: leftMax = max(leftMax, height[l])
      type: good
      why:
        ko: leftMax < rightMax이면 왼쪽 위치의 물의 높이는 leftMax에 의해 결정됨. leftMax를 현재 높이와의 최댓값으로 업데이트
        en: When leftMax is smaller, water level is determined by leftMax; update with current bar height
    - code: leftMax = height[l]
      type: distractor
      why:
        ko: 단순 할당은 이전의 최댓값을 버리므로 물의 높이 계산이 틀림
        en: Direct assignment loses previous maximum; need running max instead
    - code: leftMax = leftMax + height[l]
      type: distractor
      why:
        ko: 합산은 최댓값 추적이 아니므로 물의 높이 계산이 완전히 잘못됨
        en: Summing instead of max gives incorrect water level calculation
  - label:
      ko: 좌측에서 물의 양 누적
      en: Accumulate water on left side
    indent: 2
    options:
    - code: res += leftMax - height[l]
      type: good
      why:
        ko: 현재 위치에서 담을 수 있는 물의 양은 leftMax - height[l]. 이를 결과에 더함
        en: Water trapped at current position = leftMax - height[l]; add to result
    - code: res += height[l] - leftMax
      type: distractor
      why:
        ko: 뺄셈 순서가 반대면 음수가 되어 물의 양이 감소함
        en: Reversed subtraction gives negative water amount
    - code: res = leftMax - height[l]
      type: distractor
      why:
        ko: 누적이 아니라 덮어쓰기이므로 이전 계산값이 손실됨
        en: Assignment overwrites previous total; should accumulate with +=
  - label:
      ko: 우측 경계 처리 (최대값 업데이트)
      en: 'Process right side: update right max'
    indent: 1
    options:
    - code: rightMax = max(rightMax, height[r])
      type: good
      why:
        ko: rightMax < leftMax이면 오른쪽 위치의 물의 높이는 rightMax에 의해 결정됨. rightMax를 현재 높이와의 최댓값으로 업데이트
        en: When rightMax is smaller, water level is determined by rightMax; update with current bar height
    - code: rightMax = height[r]
      type: distractor
      why:
        ko: 단순 할당은 이전의 최댓값을 버리므로 물의 높이 계산이 틀림
        en: Direct assignment loses previous maximum; need running max
    - code: rightMax = rightMax + height[r]
      type: distractor
      why:
        ko: 합산은 최댓값 추적이 아니므로 물의 높이 계산이 완전히 잘못됨
        en: Summing instead of max gives incorrect water level
trace:
  code:
  - 'class Solution:'
  - '    def trap(self, height: List[int]) -> int:'
  - '        if not height:'
  - '            return 0'
  - ''
  - '        l, r = 0, len(height) - 1'
  - '        leftMax, rightMax = height[l], height[r]'
  - '        res = 0'
  - '        while l < r:'
  - '            if leftMax < rightMax:'
  - '                l += 1'
  - '                leftMax = max(leftMax, height[l])'
  - '                res += leftMax - height[l]'
  - '            else:'
  - '                r -= 1'
  - '                rightMax = max(rightMax, height[r])'
  - '                res += rightMax - height[r]'
  - '        return res'
  cases:
  - input: '[0,1,0,2,1,0,1,3,2,1,2,1]'
    expected: '6'
  - input: '[4,2,0,3,2,5]'
    expected: '9'
  worked_example:
    input: '[0,1,0,2,1,0,1,3,2,1,2,1]'
    steps:
    - ko: '초기값: l=0, r=11, leftMax=height[0]=0, rightMax=height[11]=1, res=0'
      en: 'Init: l=0, r=11, leftMax=0, rightMax=1, res=0'
    - ko: '반복 1~3: leftMax < rightMax이므로 왼쪽을 이동하며 처리. l=1: leftMax=max(0,1)=1, res+=0. l=2: leftMax=1, res+=1. l=3: leftMax=2, res+=0.'
      en: 'Iterations 1-3: leftMax < rightMax, process left. l=1→l=2→l=3: accumulate water at l=2 (value 1)'
    - ko: '반복 4~7: rightMax 업데이트하면서 오른쪽 처리. r=10: rightMax=2, res+=0. r=9: rightMax=2, res+=1. r=8: rightMax=2, res+=0. r=7: rightMax=3, res+=0.'
      en: 'Iterations 4-7: Update rightMax and process right. r=10→r=9→r=8→r=7: accumulate 1 unit at r=9'
    - ko: '반복 8~11: leftMax 계속 업데이트. l=4: leftMax=2, res+=1. l=5: leftMax=2, res+=2. l=6: leftMax=2, res+=1. l=7: l==r이므로 종료. 최종 res=6'
      en: 'Iterations 8-11: Continue left side. l=4→l=5→l=6→l=7: accumulate 1+2+1=4 more units. Final res=6'
    answer: '6'
solution:
  code: "class Solution:\n    def trap(self, height: List[int]) -> int:\n        if not height:\n            return 0\n\n        l, r = 0, len(height) - 1\n        leftMax, rightMax = height[l], height[r]\n        res = 0\n        while l < r:\n            if leftMax < rightMax:\n                l += 1\n                leftMax = max(leftMax, height[l])\n                res += leftMax - height[l]\n            else:\n                r -= 1\n                rightMax = max(rightMax, height[r])\n                res += rightMax - height[r]\n        return res\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 높이 배열이 매우 크거나 스트리밍 방식으로 들어온다면 어떻게 해야 할까?
    en: How would you solve this if the array were very large or provided as a stream?
  - ko: 2D 격자에서 빗물이 고이는 양을 계산할 수 있을까? (2D Rain Water Trapping)
    en: Can you extend this to a 2D elevation map to calculate trapped water volume?
  - ko: 입력 배열에 음수 높이가 포함된다면 어떻게 처리할까?
    en: How would you handle negative heights in the input array?
```