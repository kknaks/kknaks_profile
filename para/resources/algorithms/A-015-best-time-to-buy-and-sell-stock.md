---
created: '2026-05-17'
date: '2026-05-17'
day: Day 15
difficulty: easy
id: A-015
source:
  curated_in:
  - neetcode150
  number: 121
  platform: leetcode
  slug: best-time-to-buy-and-sell-stock
  url: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
tags:
- array
- dynamic-programming
title:
  en: Best Time to Buy and Sell Stock
  ko: 주식을 사고팔기 가장 좋은 시점
today: false
type: algorithm
updated: '2026-05-17'
visible: true
---

# 주식을 사고팔기 가장 좋은 시점

## Data

```yaml
problem:
  title:
    ko: 주식을 사고팔기 가장 좋은 시점
    en: Best Time to Buy and Sell Stock
  statement:
    en: 'You are given an array prices where prices[i] is the price of a given stock on the ith day.


      You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.


      Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.'
    ko: '정수 배열 prices가 주어지며, prices[i]는 i번째 날의 주식 가격입니다.


      한 주의 주식을 사는 하나의 날과 그 이후의 다른 날에 파는 날을 선택하여 이득을 최대화하려고 합니다.


      이 거래에서 얻을 수 있는 최대 이득을 반환하세요. 이득을 얻을 수 없다면 0을 반환하세요.'
  constraints:
  - 1 ≤ prices.length ≤ 10⁵
  - 0 ≤ prices[i] ≤ 10⁴
  io:
  - input: '[7,1,5,3,6,4]'
    output: '5'
  - input: '[7,6,4,3,1]'
    output: '0'
clarifying:
  items:
  - q:
      ko: 같은 날에 사서 팔 수 있나요?
      en: Can we buy and sell on the same day?
    type: good
    why:
      ko: 문제에서 '다른 날'이라고 명시했으므로 불가능합니다. 최소 1일 이상의 보유 기간이 필요합니다.
      en: The problem explicitly states 'a different day in the future', so this is not allowed. You must hold the stock for at least one day.
  - q:
      ko: 반드시 거래를 완료해야 하나요?
      en: Must we complete a transaction?
    type: good
    why:
      ko: 아니오. 이득을 얻을 수 없으면 0을 반환합니다. 예시 2에서 모든 가격이 내려가므로 거래하지 않습니다.
      en: No. If no profit is possible, we return 0. Example 2 shows that when prices only decrease, we don't make any transaction.
  - q:
      ko: 여러 번 사고팔 수 있나요?
      en: Can we complete multiple buy-sell transactions?
    type: good
    why:
      ko: '''단일 날을 선택하여 사고 다른 날에 판다''고 명시했으므로 하나의 거래만 가능합니다.'
      en: The problem specifies 'a single day to buy' and 'a different day to sell', indicating only one transaction is allowed.
  - q:
      ko: 가격이 계속 내려가면 무엇을 반환하나요?
      en: If all prices are strictly decreasing, what should we return?
    type: good
    why:
      ko: 0을 반환합니다. 어느 시점에서든 판매하면 손해이므로 거래하지 않는 것이 최선입니다.
      en: Return 0, since no profit is possible. At every point, selling would result in a loss.
  - q:
      ko: 미래의 가격을 미리 알고 의사결정하나요?
      en: Can we use future prices to decide whether to buy?
    type: distractor
    why:
      ko: 아니오. 알고리즘은 앞으로만 진행하며 각 시점에서 지금까지의 최저가와 현재 가격만 고려합니다.
      en: No. The algorithm moves forward only, considering only past minimum price and current price at each step.
  - q:
      ko: 배열의 길이가 1이면 어떻게 하나요?
      en: What if the array has only one element?
    type: distractor
    why:
      ko: 다른 날에 팔 수 없으므로 이득이 0입니다. 초기값 res=0이 반환됩니다.
      en: We cannot sell on a different day, so profit is 0. The initial value res=0 is returned.
approach:
  items:
  - name:
      ko: 한 번의 순회로 최소값 추적
      en: One-pass tracking minimum price
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 지금까지의 최저가를 계속 업데이트하면서 현재 가격과의 차이로 이득을 계산합니다. 가장 효율적입니다.
      en: Track the minimum price seen so far and calculate profit against current price at each step. Most efficient.
  - name:
      ko: 동적 프로그래밍 (최소값 추적)
      en: Dynamic programming with min tracking
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 각 위치에서의 최대 이득을 구하는데, 이전의 최소값 정보를 활용합니다. 본 솔루션과 동일한 효율성을 가집니다.
      en: Calculate max profit at each position using prior minimum. Achieves same complexity as one-pass approach.
  - name:
      ko: 완전 탐색 (모든 쌍 확인)
      en: Brute force (check all pairs)
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 모든 (i,j) 쌍에서 i < j일 때 이득을 계산합니다. 정확하지만 비효율적입니다.
      en: Check all pairs (i,j) where i < j. Correct but inefficient for large inputs.
  - name:
      ko: 정렬 후 매칭
      en: Sort and match prices
    complexity: O(n log n) time / O(n) space
    type: distractor
    why:
      ko: 정렬하면 배열의 순서 정보가 손실되어 '구매일이 판매일보다 먼저'라는 제약을 만족할 수 없습니다.
      en: Sorting loses the temporal order needed to ensure buying happens before selling.
  - name:
      ko: 슬라이딩 윈도우
      en: Sliding window
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 이 문제는 연속된 부분배열을 찾는 것이 아니라 임의의 두 인덱스를 찾는 것이므로 슬라이딩 윈도우가 부적절합니다.
      en: This problem seeks two arbitrary indices, not a contiguous subarray, so sliding window doesn't apply.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 변수 초기화
      en: Initialize result variable
    indent: 0
    options:
    - code: res = 0
      type: good
      why:
        ko: 이득이 없을 때 기본값 0을 반환하기 위해 res를 0으로 초기화합니다.
        en: Initialize res to 0 as the default return value when no profit is possible.
    - code: res = float('-inf')
      type: distractor
      why:
        ko: 음수 이득을 허용하지 않으므로 음의 무한대로 초기화할 필요가 없습니다.
        en: We cannot have negative profit since we can choose not to trade, so -inf is unnecessary.
    - code: res = prices[0]
      type: distractor
      why:
        ko: res는 이득(가격 차이)을 저장해야 하는데, 가격값으로 초기화하면 의미가 맞지 않습니다.
        en: res should store profit (a difference), not a price value.
  - label:
      ko: 최소 가격 초기화
      en: Initialize minimum price
    indent: 0
    options:
    - code: lowest = prices[0]
      type: good
      why:
        ko: 첫 번째 가격을 초기 최솟값으로 설정합니다. 이후 더 낮은 가격이 나타나면 업데이트됩니다.
        en: Set the first price as the initial minimum. It will be updated if a lower price is encountered.
    - code: lowest = float('inf')
      type: distractor
      why:
        ko: 무한대로 초기화하면 첫 번째 가격도 올바르게 인식되지만, prices[0]으로 직접 초기화하는 것이 더 효율적입니다.
        en: While inf works, initializing with prices[0] is more direct and efficient.
    - code: lowest = 0
      type: distractor
      why:
        ko: 0으로 초기화하면 모든 실제 가격이 0 이상이므로 항상 잘못된 결과를 줍니다.
        en: Initializing to 0 fails since all prices are at least 0 per constraints.
  - label:
      ko: 배열 순회
      en: Iterate through array
    indent: 0
    options:
    - code: 'for price in prices:'
      type: good
      why:
        ko: 모든 가격을 순회하면서 각 시점에서의 이득을 계산합니다. 한 번의 순회로 충분합니다.
        en: Iterate through all prices once, calculating potential profit at each point.
    - code: 'for i in range(1, len(prices)):'
      type: distractor
      why:
        ko: 첫 번째 가격을 건너뛰면 그것을 판매 가격으로 사용하는 경우를 놓칩니다.
        en: Skipping the first price means we miss using it as a potential selling price.
    - code: 'for price in prices[1:]:'
      type: distractor
      why:
        ko: 마찬가지로 첫 번째 가격을 건너뜁니다. 완전한 순회가 필요합니다.
        en: Also skips the first price. A complete pass through all prices is needed.
  - label:
      ko: 새로운 최솟값 확인
      en: Check for new minimum
    indent: 1
    options:
    - code: 'if price < lowest:'
      type: good
      why:
        ko: 현재 가격이 지금까지의 최저가보다 낮으면, 이 새 가격을 구매 기회로 업데이트합니다.
        en: If current price is lower than the minimum seen, it becomes the new buying opportunity.
    - code: 'if price <= lowest:'
      type: distractor
      why:
        ko: 같을 때는 업데이트할 필요가 없으므로 '<'가 정확합니다. '≤'는 불필요한 연산을 추가합니다.
        en: Using '<=' instead of '<' is correct but performs unnecessary updates when prices are equal.
    - code: 'if price > lowest:'
      type: distractor
      why:
        ko: 조건이 반대입니다. 낮은 가격을 구매가로 하려면 '<'이어야 합니다.
        en: The condition is reversed; we want lower prices as buying opportunities.
  - label:
      ko: 최솟값 업데이트
      en: Update minimum price
    indent: 2
    options:
    - code: lowest = price
      type: good
      why:
        ko: 새 최솟값을 기록합니다. 이후 가격들과의 차이를 계산할 때 사용됩니다.
        en: Record the new minimum. This will be used to calculate profit against future prices.
    - code: min_price = price
      type: distractor
      why:
        ko: 변수명이 다르면 'lowest'와 불일치하여 이후에 정의되지 않은 변수 오류가 발생합니다.
        en: Using a different variable name breaks the algorithm since 'lowest' is used later.
    - code: lowest = price - res
      type: distractor
      why:
        ko: 가격에서 이득을 뺄 이유가 없습니다. 단순히 현재 가격을 저장해야 합니다.
        en: Subtracting profit from price makes no sense; just store the current price.
  - label:
      ko: 최대 이득 계산 및 업데이트
      en: Calculate and update maximum profit
    indent: 1
    options:
    - code: res = max(res, price - lowest)
      type: good
      why:
        ko: 현재 가격에서 최저가를 뺀 값이 이전 최대 이득보다 크면 업데이트합니다. 한 번의 순회로 최댓값을 추적합니다.
        en: If profit from selling at current price exceeds prior maximum, update it. Tracks the global maximum in one pass.
    - code: res = price - lowest
      type: distractor
      why:
        ko: max()를 사용하지 않으면 현재 이득이 음수일 때 res가 음수가 되어 거래하지 않는 경우를 놓칩니다.
        en: Without max(), res becomes negative when current profit is negative, losing the benefit of not trading.
    - code: res = max(res, lowest - price)
      type: distractor
      why:
        ko: 차이의 순서가 반대입니다. 판매가 - 구매가가 이득이므로 'price - lowest'여야 합니다.
        en: Profit is selling price minus buying price, not the reverse.
  - label:
      ko: 결과 반환
      en: Return result
    indent: 0
    options:
    - code: return res
      type: good
      why:
        ko: 최대 이득을 반환합니다. 이득이 없으면 0(초기값)을 반환합니다.
        en: Return the maximum profit found. If no profit exists, returns 0 (the initial value).
    - code: return lowest
      type: distractor
      why:
        ko: lowest는 최저 가격이지 이득이 아닙니다. 문제에서 요구하는 것은 이득입니다.
        en: lowest is a price, not profit. The problem asks for maximum profit.
    - code: return max(res, lowest)
      type: distractor
      why:
        ko: res는 이미 최댓값이므로 다시 max()를 할 필요가 없습니다. 잘못된 값을 반환할 수 있습니다.
        en: res is already the maximum; comparing with lowest again produces incorrect results.
trace:
  code:
  - 'class Solution:'
  - '    def maxProfit(self, prices: List[int]) -> int:'
  - '        res = 0'
  - '        '
  - '        lowest = prices[0]'
  - '        for price in prices:'
  - '            if price < lowest:'
  - '                lowest = price'
  - '            res = max(res, price - lowest)'
  - '        return res'
  cases:
  - input: '[7,1,5,3,6,4]'
    expected: '5'
  - input: '[7,6,4,3,1]'
    expected: '0'
  worked_example:
    input: '[7,1,5,3,6,4]'
    steps:
    - ko: 'res=0, lowest=7 초기화. 가격 7 처리: 새 최솟값 아님, 이득=7-7=0, res=0'
      en: 'Initialize res=0, lowest=7. Process price 7: not new min, profit=7-7=0, res=0'
    - ko: '가격 1 처리: 1 < 7이므로 lowest=1. 이득=1-1=0, res=0'
      en: 'Process price 1: 1 < 7 so lowest=1. profit=1-1=0, res=0'
    - ko: '가격 5 처리: 새 최솟값 아님, 이득=5-1=4, res=4 업데이트'
      en: 'Process price 5: not new min, profit=5-1=4, update res=4'
    - ko: '가격 3 처리: 새 최솟값 아님, 이득=3-1=2, res=4 (유지)'
      en: 'Process price 3: not new min, profit=3-1=2, res=4 (unchanged)'
    - ko: '가격 6 처리: 새 최솟값 아님, 이득=6-1=5, res=5 업데이트'
      en: 'Process price 6: not new min, profit=6-1=5, update res=5'
    - ko: '가격 4 처리: 새 최솟값 아님, 이득=4-1=3, res=5 (유지). 반환: 5'
      en: 'Process price 4: not new min, profit=4-1=3, res=5 (unchanged). Return 5'
    answer: '5'
solution:
  code: "class Solution:\n    def maxProfit(self, prices: List[int]) -> int:\n        res = 0\n        \n        lowest = prices[0]\n        for price in prices:\n            if price < lowest:\n                lowest = price\n            res = max(res, price - lowest)\n        return res\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 최대 2번의 거래가 가능하다면? (Best Time to Buy and Sell Stock III)
    en: What if we can complete at most 2 transactions? (Best Time to Buy and Sell Stock III)
  - ko: 무제한 거래가 가능하다면? (가격이 오를 때마다 사고팔기)
    en: What if we can complete unlimited transactions? (Buy-sell whenever price increases)
  - ko: 각 거래마다 수수료가 있다면? (이득에서 수수료를 빼기)
    en: What if there's a transaction fee? (Subtract fee from profit)
```