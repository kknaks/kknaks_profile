---
created: '2026-06-05'
date: '2026-06-05'
day: Day 30
difficulty: medium
id: A-030
source:
  curated_in:
  - neetcode150
  number: 875
  platform: leetcode
  slug: koko-eating-bananas
  url: https://leetcode.com/problems/koko-eating-bananas/
tags:
- array
- binary-search
title:
  en: Koko Eating Bananas
  ko: 코코의 바나나 먹기
today: false
type: algorithm
updated: '2026-06-05'
visible: true
---

# 코코의 바나나 먹기

## Data

```yaml
problem:
  title:
    ko: 코코의 바나나 먹기
    en: Koko Eating Bananas
  statement:
    ko: '코코는 바나나를 먹는 것을 좋아합니다. n개의 바나나 더미가 있으며, i번째 더미에는 piles[i]개의 바나나가 있습니다. 경비원들이 가서 h시간 후에 돌아올 예정입니다.


      코코는 시간당 바나나 먹는 속도 k를 정할 수 있습니다. 매 시간마다, 그녀는 어떤 바나나 더미를 선택하고 그 더미에서 k개의 바나나를 먹습니다. 만약 더미에 k개보다 적은 바나나가 있다면, 모두 먹고 그 시간 동안 더 이상의 바나나를 먹지 않습니다.


      코코는 천천히 먹고 싶지만, 경비원이 돌아오기 전에 모든 바나나를 먹어야 합니다.


      코코가 h시간 내에 모든 바나나를 먹을 수 있는 최소 정수 k를 반환하세요.'
    en: 'Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.


      Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.


      Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.


      Return the minimum integer k such that she can eat all the bananas within h hours.'
  constraints:
  - 1 ≤ piles.length ≤ 10⁴
  - piles.length ≤ h ≤ 10⁹
  - 1 ≤ piles[i] ≤ 10⁹
  io:
  - input: '[3,6,7,11]

      8'
    output: '4'
  - input: '[30,11,23,4,20]

      5'
    output: '30'
  - input: '[30,11,23,4,20]

      6'
    output: '23'
clarifying:
  items:
  - q:
      ko: 코코는 한 시간에 여러 더미에서 먹을 수 있나요?
      en: Can Koko eat from multiple piles in a single hour?
    type: good
    why:
      ko: 문제에서 '그 더미에서'라고 하여 한 시간에 한 더미만 선택하는 것을 명확히 합니다.
      en: The problem states 'she chooses some pile' (singular) each hour, clarifying she can only eat from one pile per hour.
  - q:
      ko: 코코의 먹는 속도 k는 시간에 따라 변할 수 있나요?
      en: Can Koko's eating speed k change over time?
    type: good
    why:
      ko: 문제에서 '먹는 속도 k를 정할 수 있다'고 하여 k는 고정된 하나의 값임을 나타냅니다.
      en: The problem states she 'decides her eating speed of k', indicating k is a single fixed value for all hours.
  - q:
      ko: k는 정수여야 하나요?
      en: Must the eating speed k be an integer?
    type: good
    why:
      ko: 문제에서 '최소 정수 k'를 구하라고 명시하므로 k는 정수입니다.
      en: The problem explicitly asks for 'the minimum integer k', so k must be a whole number.
  - q:
      ko: 어떤 더미에서 시작하든 모두 시간이 같나요?
      en: Does the order of eating piles matter?
    type: distractor
    why:
      ko: 먹는 순서는 중요하지 않습니다. k로 정해지면 모든 더미를 처리하는 데 필요한 총 시간은 동일합니다.
      en: The order doesn't matter; once k is fixed, the total time to process all piles is the same regardless of order.
  - q:
      ko: k가 max(piles)보다 작으면 반드시 모든 바나나를 먹을 수 없나요?
      en: If k < max(piles), is it impossible to finish all bananas?
    type: distractor
    why:
      ko: k는 max(piles)보다 작을 수 있습니다. 예를 들어 piles = [1, 1, 1, 1], h = 4일 때 k = 1이면 충분합니다.
      en: No; k can be less than max(piles). For example, if piles = [1,1,1,1] and h = 4, then k = 1 works.
approach:
  items:
  - name:
      ko: 이진 탐색 (답에 대한 이진 탐색)
      en: Binary search on the answer
    complexity: O(n * log(max(piles))) time / O(1) space
    type: good
    why:
      ko: k의 범위는 [1, max(piles)]이고, 각 후보 k에 대해 O(n) 시간에 실행 가능성을 확인합니다. 이진 탐색으로 최소 k를 효율적으로 찾을 수 있습니다.
      en: k ranges from 1 to max(piles). For each candidate k, we check feasibility in O(n) time. Binary search efficiently finds the minimum feasible k.
  - name:
      ko: 선형 탐색 (모든 k를 순차적으로 확인)
      en: Linear search (try each k sequentially)
    complexity: O(max(piles) * n) time / O(1) space
    type: good
    why:
      ko: k = 1부터 max(piles)까지 순차적으로 확인할 수 있지만, max(piles)가 최대 10^9일 수 있으므로 이진 탐색보다 훨씬 느립니다.
      en: We could check k from 1 to max(piles) sequentially, but max(piles) can be up to 10^9, making this much slower than binary search.
  - name:
      ko: 탐욕법 (가장 큰 더미부터 먹음)
      en: Greedy approach (eat largest pile first)
    complexity: O(n log n + h) time / O(n) space
    type: distractor
    why:
      ko: k는 시간에 따라 고정되므로, 더미의 순서를 바꾸는 것은 총 시간에 영향을 주지 않습니다. 이 접근은 작동하지 않습니다.
      en: k is fixed for all hours, so pile order doesn't affect total time. Greedy strategy doesn't solve this problem.
  - name:
      ko: 동적 프로그래밍
      en: Dynamic programming
    complexity: O(n * max(piles)) time / O(max(piles)) space
    type: distractor
    why:
      ko: 이 문제는 최적화 선택의 수열이 아니라, 고정된 값 k의 임계값을 찾는 문제입니다. DP는 적용되지 않습니다.
      en: We're finding a threshold value k, not optimizing a sequence of choices. DP does not apply here.
logic:
  format: slot
  slots:
  - label:
      ko: 이진 탐색 범위 초기화
      en: Initialize binary search bounds
    indent: 0
    options:
    - code: l, r = 1, max(piles)
      type: good
      why:
        ko: k의 최소값은 1 (천천히 먹기)이고, 최대값은 max(piles) (한 시간에 가장 큰 더미를 모두 먹기)입니다.
        en: Eating speed k ranges from 1 (minimum) to max(piles) (maximum needed to finish largest pile in one hour).
    - code: l, r = 0, sum(piles)
      type: distractor
      why:
        ko: k는 최소 1이어야 하고, 상한은 모든 더미의 합이 아니라 가장 큰 더미입니다.
        en: k must be at least 1, and upper bound is the largest pile, not the total sum.
    - code: l, r = 1, len(piles)
      type: distractor
      why:
        ko: 상한은 더미의 개수가 아니라 가장 큰 더미의 크기여야 합니다.
        en: Upper bound should be the max pile size, not the number of piles.
  - label:
      ko: 최대 속도로 초기 결과 설정
      en: Initialize result with maximum speed
    indent: 0
    options:
    - code: res = r
      type: good
      why:
        ko: res = r은 항상 유효한 답을 보장합니다 (최대 속도로 모두 먹을 수 있음). 그 후 더 느린 속도를 찾아 업데이트합니다.
        en: res = r ensures we always have a valid answer (max speed always works). We refine downward to find the minimum.
    - code: res = l
      type: distractor
      why:
        ko: l = 1은 항상 실행 가능하지 않을 수 있습니다. r로 시작하면 안전합니다.
        en: l = 1 may not be feasible; starting with r is safer.
    - code: res = -1
      type: distractor
      why:
        ko: -1은 '찾지 못함'을 의미하지만, 해는 항상 존재합니다.
        en: -1 signals 'not found', but a solution always exists.
  - label:
      ko: 탐색 범위가 존재하는 동안 반복
      en: Continue while search space exists
    indent: 0
    options:
    - code: 'while l <= r:'
      type: good
      why:
        ko: while l <= r은 범위가 수렴할 때까지 진행합니다. <=는 마지막 후보 (l == r)도 확인하도록 보장합니다.
        en: while l <= r continues until the range converges. <= ensures we evaluate the final candidate.
    - code: 'while l < r:'
      type: distractor
      why:
        ko: l == r일 때의 경계 사례를 놓칩니다. 그 중간값도 확인해야 합니다.
        en: Misses the boundary case where l == r; that value must be checked.
    - code: 'while l <= r - 1:'
      type: distractor
      why:
        ko: l < r과 동일하며, 마지막 비교를 건너뜁니다.
        en: Equivalent to l < r; skips the final comparison needed.
  - label:
      ko: 중간 후보 속도 계산
      en: Calculate candidate eating speed
    indent: 1
    options:
    - code: k = (l + r) // 2
      type: good
      why:
        ko: k = (l + r) // 2는 중간값을 구합니다. 정수 나눗셈이므로 k는 항상 정수입니다.
        en: k = (l + r) // 2 finds the midpoint. Integer division ensures k is a whole number.
    - code: k = (l + r) / 2
      type: distractor
      why:
        ko: 실수 나눗셈이므로 k가 소수가 됩니다. 시간당 바나나 수는 정수여야 합니다.
        en: Float division produces a decimal; eating speed must be a whole number.
    - code: k = r - (r - l) // 2
      type: distractor
      why:
        ko: 불필요하게 복잡합니다. (l + r) // 2가 더 간단합니다.
        en: Unnecessarily complex; (l + r) // 2 is simpler.
  - label:
      ko: 속도 k로 필요한 총 시간 계산
      en: Calculate total hours needed for speed k
    indent: 2
    options:
    - code: totalTime += math.ceil(float(p) / k)
      type: good
      why:
        ko: 각 더미에 대해 천장 함수로 시간을 계산하고 (부분 시간을 올림), 합계를 누적합니다.
        en: For each pile, use ceiling division to calculate hours (rounding up partial hours); accumulate the total.
    - code: totalTime += p // k
      type: distractor
      why:
        ko: 바닥 함수는 부분 시간을 버립니다. 5개 바나나를 속도 2로 먹으면 3시간 필요하지만, 바닥은 2시간이 됩니다.
        en: Floor division loses fractional hours; 5 bananas at speed 2 takes 3 hours (not 2).
    - code: totalTime += p / k
      type: distractor
      why:
        ko: 실수 나눗셈이므로 소수 시간이 됩니다. 천장 함수로 올림해야 합니다.
        en: Float division; need math.ceil to round up to whole hours.
  - label:
      ko: 속도가 실행 가능할 때 우측 범위 업데이트
      en: Update right bound when feasible
    indent: 2
    options:
    - code: r = k - 1
      type: good
      why:
        ko: totalTime <= h이면 k는 작동합니다. 그것을 저장하고 더 느린 속도를 찾기 위해 우측 범위를 좁힙니다 (r = k - 1).
        en: If totalTime ≤ h, k works. Save it and search for slower speeds by moving right boundary left (r = k - 1).
    - code: l = k + 1
      type: distractor
      why:
        ko: 좌측 범위를 움직입니다. k가 작동하면 좌측을 움직여선 안 됩니다.
        en: Moves left boundary; wrong direction when k is feasible.
    - code: r = k
      type: distractor
      why:
        ko: 범위를 좁히지 못합니다. 무한 루프가 되거나 최적값을 놓칩니다.
        en: Doesn't narrow search; infinite loop or missed optimal value.
  - label:
      ko: 속도가 불충분할 때 좌측 범위 업데이트
      en: Update left bound when infeasible
    indent: 2
    options:
    - code: l = k + 1
      type: good
      why:
        ko: totalTime > h이면 k는 너무 느립니다. 더 빠른 속도를 찾기 위해 좌측 범위를 오른쪽으로 움직입니다 (l = k + 1).
        en: If totalTime > h, k is too slow. Search for faster speeds by moving left boundary right (l = k + 1).
    - code: r = k - 1
      type: distractor
      why:
        ko: 우측 범위를 움직입니다. k가 작동하지 않으면 우측을 움직여선 안 됩니다.
        en: Moves right boundary; wrong direction when k is infeasible.
    - code: l = k
      type: distractor
      why:
        ko: k를 제외하지 않으므로 진전이 없습니다. l = k + 1이어야 우측으로 이동합니다.
        en: Doesn't exclude k; need l = k + 1 to move right.
trace:
  code:
  - 'class Solution:'
  - '    def minEatingSpeed(self, piles: List[int], h: int) -> int:'
  - '        l, r = 1, max(piles)'
  - '        res = r'
  - ''
  - '        while l <= r:'
  - '            k = (l + r) // 2'
  - ''
  - '            totalTime = 0'
  - '            for p in piles:'
  - '                totalTime += math.ceil(float(p) / k)'
  - '            if totalTime <= h:'
  - '                res = k'
  - '                r = k - 1'
  - '            else:'
  - '                l = k + 1'
  - '        return res'
  cases:
  - input: '[3,6,7,11]

      8'
    expected: '4'
  - input: '[30,11,23,4,20]

      5'
    expected: '30'
  - input: '[30,11,23,4,20]

      6'
    expected: '23'
  worked_example:
    input: '[3,6,7,11]

      8'
    steps:
    - ko: '범위 [1, 11]에서 시작. k = 6 시도: ceil(3/6) + ceil(6/6) + ceil(7/6) + ceil(11/6) = 1+1+2+2 = 6시간 ≤ 8 ✓'
      en: 'Start with range [1, 11]. Try k=6: ceil(3/6) + ceil(6/6) + ceil(7/6) + ceil(11/6) = 1+1+2+2 = 6 hours ≤ 8 ✓'
    - ko: 'k=6 작동하므로 답 저장, 범위를 [1, 5]로 좁힘. k = 3 시도: 1+2+3+4 = 10시간 > 8 ✗'
      en: 'k=6 works, save answer, narrow to [1, 5]. Try k=3: 1+2+3+4 = 10 hours > 8 ✗'
    - ko: 'k=3 너무 느림, 범위를 [4, 5]로 좁힘. k = 4 시도: 1+2+2+3 = 8시간 ≤ 8 ✓'
      en: 'k=3 too slow, narrow to [4, 5]. Try k=4: 1+2+2+3 = 8 hours ≤ 8 ✓'
    - ko: 'l = 4, r = 3이므로 l > r. 탐색 종료, 답: 4'
      en: 'l = 4, r = 3, so l > r. Loop ends. Answer: 4'
    answer: '4'
solution:
  code: "class Solution:\n    def minEatingSpeed(self, piles: List[int], h: int) -> int:\n        l, r = 1, max(piles)\n        res = r\n\n        while l <= r:\n            k = (l + r) // 2\n\n            totalTime = 0\n            for p in piles:\n                totalTime += math.ceil(float(p) / k)\n            if totalTime <= h:\n                res = k\n                r = k - 1\n            else:\n                l = k + 1\n        return res\n"
  complexity:
    time: O(n * log(max(piles)))
    space: O(1)
  followup:
  - ko: 여러 개의 h값에 대한 쿼리가 있다면 어떻게 할까요?
    en: What if there are multiple queries with different h values for the same piles?
  - ko: '다른 이진 탐색 패턴 (예: while l < r 사용)으로 구현할 수 있을까요?'
    en: Can you implement this with a different binary search pattern (e.g., while l < r)?
  - ko: '먹는 속도 k가 소수 (예: 3.5개/시간)일 수 있다면?'
    en: What if eating speed k could be fractional (e.g., 3.5 bananas/hour)?
```