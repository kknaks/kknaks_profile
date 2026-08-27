---
created: '2026-05-08'
date: '2026-05-08'
day: Day 06
difficulty: medium
id: A-006
source:
  curated_in:
  - neetcode150
  number: 238
  platform: leetcode
  slug: product-of-array-except-self
  url: https://leetcode.com/problems/product-of-array-except-self/
tags:
- array
- prefix-sum
title:
  en: Product of Array Except Self
  ko: 자신을 제외한 배열의 곱
today: false
type: algorithm
updated: '2026-05-08'
visible: true
---

# 자신을 제외한 배열의 곱

## Data

```yaml
problem:
  title:
    ko: 자신을 제외한 배열의 곱
    en: Product of Array Except Self
  statement:
    ko: '정수 배열 nums가 주어졌을 때, answer[i]가 nums[i]를 제외한 nums의 모든 원소의 곱이 되도록 하는 배열 answer를 반환하세요.


      nums의 어떤 prefix 또는 suffix의 곱도 32비트 정수에 맞다고 보장됩니다.


      O(n) 시간에 작동하는 알고리즘을 작성해야 하며, 나눗셈 연산을 사용할 수 없습니다.'
    en: 'Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].


      The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.


      You must write an algorithm that runs in O(n) time and without using the division operation.'
  constraints:
  - 2 ≤ nums.length ≤ 10⁵
  - −30 ≤ nums[i] ≤ 30
  - Division operation is forbidden
  - answer[i] guaranteed to fit in 32-bit integer
  io:
  - input: '[1,2,3,4]'
    output: '[24,12,8,6]'
  - input: '[-1,1,0,-3,3]'
    output: '[0,0,9,0,0]'
clarifying:
  items:
  - q:
      ko: 배열에 0이 포함되어 있으면 어떻게 해야 하나요?
      en: What happens if the array contains zeros?
    type: good
    why:
      ko: 0은 모든 곱을 0으로 만든다는 특수한 경우입니다. prefix-suffix 접근법은 자연스럽게 이를 처리합니다.
      en: Zero makes any product zero, and the prefix-suffix approach naturally handles this edge case.
  - q:
      ko: 입력 배열을 수정해도 괜찮나요?
      en: Can I modify the input array?
    type: good
    why:
      ko: 문제에서 입력 배열 수정을 금지하지 않으므로, 최적 공간 복잡도 달성에 도움이 됩니다.
      en: The problem does not forbid modifying the input, which helps achieve O(1) extra space.
  - q:
      ko: 나눗셈을 사용하면 안 되는 이유가 뭘까요?
      en: Why can't we use division?
    type: good
    why:
      ko: 전체 곱에서 각 원소로 나누면 0이 있을 때 정의되지 않으며, 알고리즘 설계 능력을 테스트하기 위한 제약입니다.
      en: Division by zero is undefined when the array contains 0, and the constraint tests your algorithmic thinking.
  - q:
      ko: 전체 곱을 먼저 계산한 후, 각 원소로 나누는 방법은 어떤가요?
      en: Why not compute the total product first and then divide?
    type: distractor
    why:
      ko: 나눗셈 사용이 명시적으로 금지되어 있으며, 0을 다루기 위해 특수 경우 처리가 필요합니다.
      en: Division is explicitly forbidden, and zero requires special handling.
  - q:
      ko: 해시맵을 사용해서 이전 곱들을 저장하면 더 명확할까요?
      en: Would using a hash map to store intermediate products be clearer?
    type: distractor
    why:
      ko: 해시맵은 불필요한 공간을 사용하며, prefix-suffix 접근법으로 O(1) 공간을 달성할 수 있습니다.
      en: Hash map adds unnecessary space; prefix-suffix achieves O(1) extra space.
  - q:
      ko: 음수가 포함된 경우 특별히 처리해야 하나요?
      en: Do negative numbers require special handling?
    type: good
    why:
      ko: 곱셈은 음수와도 동일하게 작동하므로, 추가 처리 없이 자연스럽게 작동합니다.
      en: Multiplication works identically with negatives; no special handling needed.
  - q:
      ko: prefix와 suffix를 계산할 때, 별도의 배열이 필요한가요?
      en: Do we need separate arrays for prefix and suffix products?
    type: good
    why:
      ko: 아니요. suffix는 우측에서 좌측으로 순회하면서 계산할 수 있어, O(1) 공간만 필요합니다.
      en: No. We can compute suffix on-the-fly while iterating right-to-left, using O(1) space.
approach:
  items:
  - name:
      ko: Prefix-Suffix 곱 (공간 최적화)
      en: Prefix-Suffix Products (Space Optimized)
    complexity: O(n) time / O(1) extra space
    type: good
    why:
      ko: 좌측에서 우측으로 prefix 곱을 계산하고, 우측에서 좌측으로 suffix 곱을 곱한다. 출력 배열만 사용하므로 추가 공간이 없습니다.
      en: Compute prefix products left-to-right, then multiply by suffix products right-to-left. Uses only the output array.
  - name:
      ko: 별도 배열을 사용한 Prefix-Suffix
      en: Prefix-Suffix with Separate Arrays
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: prefix와 suffix 배열을 별도로 만들어 더 명확하게 이해할 수 있지만, 추가 공간을 사용합니다.
      en: Creates separate prefix and suffix arrays for clarity, but uses extra space. Good for learning.
  - name:
      ko: 완전 탐색 (각 인덱스마다 곱 계산)
      en: Brute Force (Per-Index Multiplication)
    complexity: O(n²) time / O(1) extra space
    type: distractor
    why:
      ko: 각 인덱스에 대해 다른 모든 원소를 곱하면 O(n²)이 되어 시간 제약을 만족하지 못합니다.
      en: For each index, multiply all other elements. This is O(n²) and violates the O(n) requirement.
  - name:
      ko: 전체 곱을 이용한 나눗셈
      en: Total Product with Division
    complexity: O(n) time / O(1) extra space
    type: distractor
    why:
      ko: 전체 곱을 계산한 후 각 원소로 나누는 것이 가장 직관적이지만, 나눗셈이 금지되어 있고 0 처리가 복잡합니다.
      en: Compute total product, then divide. Simple idea, but division is forbidden and zero-handling is messy.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 배열을 1로 초기화
      en: Initialize result array with 1s
    indent: 0
    options:
    - code: res = [1] * (len(nums))
      type: good
      why:
        ko: 모든 원소가 1로 시작하여, 이후 곱셈 연산에서 항등원 역할을 합니다.
        en: All elements start as 1 (multiplicative identity) for subsequent multiplications.
    - code: res = [0] * (len(nums))
      type: distractor
      why:
        ko: 0으로 초기화하면 모든 곱셈 결과가 0이 됩니다.
        en: Initializing with 0 makes all products 0.
    - code: res = nums[:]
      type: distractor
      why:
        ko: 입력 배열을 복사하면, 다른 원소들의 곱을 반영하지 못합니다.
        en: Copying the input leaves original values, not products of others.
  - label:
      ko: 좌측 Prefix 루프
      en: Left-to-right prefix loop
    indent: 1
    options:
    - code: 'for i in range(1, len(nums)):'
      type: good
      why:
        ko: 인덱스 1부터 시작하여 좌측의 모든 원소를 누적 곱합니다. res[i-1]은 i 좌측의 곱입니다.
        en: Starting from index 1, accumulate the product of all elements to the left. res[i-1] holds the product left of i.
    - code: 'for i in range(len(nums)):'
      type: distractor
      why:
        ko: 인덱스 0부터 시작하면, res[0]에 nums[-1]을 곱하게 되어 잘못된 결과입니다.
        en: Starting at 0 would incorrectly multiply res[0] by nums[-1].
    - code: 'for i in range(len(nums) - 1):'
      type: distractor
      why:
        ko: 마지막 원소를 건너뛰므로, 불완전한 prefix 계산입니다.
        en: Skipping the last element leaves the prefix incomplete.
  - label:
      ko: Prefix 누적 계산
      en: Accumulate prefix product
    indent: 2
    options:
    - code: res[i] = res[i-1] * nums[i-1]
      type: good
      why:
        ko: res[i]에 res[i-1] (i 좌측의 곱) 곱하기 nums[i-1] (i 직전의 값)을 저장합니다.
        en: 'Store res[i-1] * nums[i-1] in res[i]: the product of everything left of i.'
    - code: res[i] = res[i-1] * nums[i]
      type: distractor
      why:
        ko: nums[i]를 곱하면, 자신까지 포함하는 곱이 되어 자신을 제외한 곱이 아닙니다.
        en: Multiplying nums[i] includes the element itself, not except-self.
    - code: res[i] += res[i-1] * nums[i-1]
      type: distractor
      why:
        ko: 덧셈(+=)을 사용하면, 이미 1로 초기화된 값이 포함되어 잘못된 곱이 됩니다.
        en: Using += includes the initial 1, corrupting the product.
  - label:
      ko: Suffix 변수 초기화
      en: Initialize postfix variable
    indent: 0
    options:
    - code: postfix = 1
      type: good
      why:
        ko: 우측에서 좌측으로 순회하면서 suffix 곱을 누적할 변수를 1로 초기화합니다.
        en: Initialize the postfix accumulator to 1 before right-to-left traversal.
    - code: postfix = 0
      type: distractor
      why:
        ko: 0으로 초기화하면 모든 곱이 0이 됩니다.
        en: Starting with 0 makes all products 0.
    - code: postfix = nums[-1]
      type: distractor
      why:
        ko: 마지막 원소로 초기화하면, suffix 계산이 잘못됩니다.
        en: Seeding with nums[-1] skews the suffix calculation.
  - label:
      ko: 우측 Suffix 루프
      en: Right-to-left suffix loop
    indent: 1
    options:
    - code: 'for i in range(len(nums) - 1, -1, -1):'
      type: good
      why:
        ko: 배열의 오른쪽 끝에서 왼쪽 끝으로 순회하면서, 각 위치의 suffix 곱을 누적합니다.
        en: Traverse from right to left, accumulating the suffix product for each position.
    - code: 'for i in range(len(nums)):'
      type: distractor
      why:
        ko: 좌측에서 우측으로 순회하면, suffix 개념이 맞지 않습니다.
        en: Left-to-right traversal contradicts the suffix concept.
    - code: 'for i in range(len(nums) - 1, 0, -1):'
      type: distractor
      why:
        ko: 인덱스 0을 포함하지 않아, 첫 번째 원소를 건너뜁니다.
        en: Excluding index 0 leaves the first element unprocessed.
  - label:
      ko: Suffix로 결과 업데이트
      en: Multiply result by postfix
    indent: 2
    options:
    - code: res[i] *= postfix
      type: good
      why:
        ko: res[i]에 현재 postfix (i 우측의 곱)를 곱합니다. res[i]는 이제 모든 다른 원소의 곱입니다.
        en: Multiply res[i] by postfix (product of everything right of i). res[i] now contains product-except-self.
    - code: res[i] = postfix
      type: distractor
      why:
        ko: 할당(=)을 사용하면, 이미 계산한 prefix 곱이 사라집니다.
        en: Assignment (=) discards the prefix product we computed earlier.
    - code: res[i] += postfix
      type: distractor
      why:
        ko: 덧셈은 prefix와 suffix를 더하므로, 곱이 아닌 합이 됩니다.
        en: Addition sums prefix and suffix instead of multiplying them.
  - label:
      ko: Suffix 누적 업데이트
      en: Accumulate postfix for next iteration
    indent: 2
    options:
    - code: postfix *= nums[i]
      type: good
      why:
        ko: postfix에 nums[i]를 곱하여, 다음 반복에서 사용할 우측의 곱을 준비합니다.
        en: Multiply postfix by nums[i] to prepare the suffix product for the previous index.
    - code: postfix += nums[i]
      type: distractor
      why:
        ko: 덧셈(+=)을 사용하면, 곱이 아닌 합이 되어 알고리즘이 깨집니다.
        en: Using += accumulates a sum instead of a product.
    - code: postfix = nums[i]
      type: distractor
      why:
        ko: 할당(=)을 사용하면, 이전의 postfix가 날아가 계산이 잘못됩니다.
        en: Assignment loses the accumulated postfix from previous iterations.
trace:
  code:
  - 'class Solution:'
  - '    def productExceptSelf(self, nums: List[int]) -> List[int]:'
  - '        res = [1] * (len(nums))'
  - ''
  - '        for i in range(1, len(nums)):'
  - '            res[i] = res[i-1] * nums[i-1]'
  - '        postfix = 1'
  - '        for i in range(len(nums) - 1, -1, -1):'
  - '            res[i] *= postfix'
  - '            postfix *= nums[i]'
  - '        return res'
  cases:
  - input: '[1,2,3,4]'
    expected: '[24,12,8,6]'
  - input: '[-1,1,0,-3,3]'
    expected: '[0,0,9,0,0]'
  worked_example:
    input: '[1,2,3,4]'
    steps:
    - ko: res를 [1, 1, 1, 1]로 초기화합니다.
      en: Initialize res = [1, 1, 1, 1].
    - ko: '좌측 루프: i=1에서 i=3까지, prefix 곱을 누적. res = [1, 1, 2, 6]. (res[1]=1*1, res[2]=1*2, res[3]=2*3)'
      en: 'Left-to-right prefix: res[1]=1*1=1, res[2]=1*2=2, res[3]=2*3=6. Result: [1, 1, 2, 6].'
    - ko: '우측 루프: postfix로 suffix 곱을 누적하며 곱함. i=3부터 i=0까지, postfix는 [1→4→12→24]. res[3]=6*1=6, res[2]=2*4=8, res[1]=1*12=12, res[0]=1*24=24.'
      en: 'Right-to-left suffix: postfix grows 1→4→12→24. res[3]=6*1=6, res[2]=2*4=8, res[1]=1*12=12, res[0]=1*24=24. Final: [24, 12, 8, 6].'
    answer: '[24,12,8,6]'
solution:
  code: "class Solution:\n    def productExceptSelf(self, nums: List[int]) -> List[int]:\n        res = [1] * (len(nums))\n\n        for i in range(1, len(nums)):\n            res[i] = res[i-1] * nums[i-1]\n        postfix = 1\n        for i in range(len(nums) - 1, -1, -1):\n            res[i] *= postfix\n            postfix *= nums[i]\n        return res\n"
  complexity:
    time: O(n)
    space: O(1) extra space (output array not counted)
  followup:
  - ko: 나눗셈을 사용했다면, 0을 어떻게 처리하겠습니까?
    en: If division were allowed, how would you handle the zero case?
  - ko: 배열에 정확히 하나의 0이 있다면, 더 효율적인 방법이 있을까요?
    en: If the array contains exactly one zero, is there a more efficient approach?
  - ko: 배열의 크기가 매우 크면 (10억 개 원소), 메모리나 처리 시간에서 문제가 될까요?
    en: If the array is extremely large (1 billion elements), would memory or time become a concern?
```