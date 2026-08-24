---
created: '2026-06-04'
date: '2026-06-04'
day: Day 29
difficulty: medium
id: A-029
source:
  curated_in:
  - neetcode150
  number: 74
  platform: leetcode
  slug: search-a-2d-matrix
  url: https://leetcode.com/problems/search-a-2d-matrix/
tags:
- array
- binary-search
- matrix
title:
  en: Search a 2D Matrix
  ko: 2D 행렬 검색
today: false
type: algorithm
updated: '2026-06-04'
visible: true
---

# 2D 행렬 검색

## Data

```yaml
problem:
  title:
    ko: 2D 행렬 검색
    en: Search a 2D Matrix
  statement:
    ko: 'm × n 크기의 정수 행렬이 주어지며, 다음 두 가지 성질을 만족합니다:


      각 행은 오름차순으로 정렬되어 있습니다.

      각 행의 첫 번째 원소는 이전 행의 마지막 원소보다 큽니다.


      정수 target이 주어질 때, target이 행렬에 존재하면 true를, 없으면 false를 반환하세요.


      O(log(m * n)) 시간 복잡도의 해결책을 작성해야 합니다.'
    en: 'You are given an m x n integer matrix with the following two properties:


      Each row is sorted in non-decreasing order.

      The first integer of each row is greater than the last integer of the previous row.


      Given an integer target, return true if target is in matrix or false otherwise.


      You must write a solution in O(log(m * n)) time complexity.'
  constraints:
  - 1 ≤ m, n ≤ 100
  - Each row sorted in non-decreasing order
  - First element of each row > last element of previous row
  - -10⁴ ≤ matrix values, target ≤ 10⁴
  io:
  - input: '[[1,3,5,7],[10,11,16,20],[23,30,34,60]]

      3'
    output: 'true'
  - input: '[[1,3,5,7],[10,11,16,20],[23,30,34,60]]

      13'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 이 행렬을 전체적으로 정렬된 1D 배열로 볼 수 있나요?
      en: Can we treat the entire matrix as a single globally sorted 1D array?
    type: good
    why:
      ko: 네, 행렬의 성질상 모든 원소가 전역적으로 정렬되어 있습니다. 이는 O(log(m*n)) 복잡도를 가능하게 합니다.
      en: Yes, by the matrix properties, all elements follow a global ordering. This makes O(log(m*n)) achievable.
  - q:
      ko: 왜 O(log(m*n)) 복잡도가 요구되나요?
      en: What does the O(log(m*n)) time requirement suggest about the solution?
    type: good
    why:
      ko: 이진 탐색을 사용해야 합니다. 두 개의 연속적인 이진 탐색(O(log m) + O(log n))으로 이를 달성할 수 있습니다.
      en: It indicates binary search. Two consecutive binary searches O(log m + log n) = O(log(m*n)) achieve this.
  - q:
      ko: 왜 matrix[row][0]과 matrix[row][-1]을 비교하는 것이 올바른 행을 찾는 데 도움이 되나요?
      en: Why can comparing target with matrix[row][0] and matrix[row][-1] identify the correct row?
    type: good
    why:
      ko: 연속된 행들은 겹치지 않으므로(행 i의 첫 원소 > 행 i-1의 마지막 원소), target은 최대 한 행에만 속할 수 있습니다.
      en: Consecutive rows don't overlap (first of row i > last of row i-1). Target can only belong to at most one row.
  - q:
      ko: 올바른 행을 찾은 후에는 어떻게 하나요?
      en: Once we identify the correct row, what is the next step?
    type: good
    why:
      ko: 그 행에서 표준 이진 탐색을 수행하여 O(log n) 시간에 target을 찾습니다.
      en: Perform a standard binary search within that row to find target in O(log n) time.
  - q:
      ko: 확실하게 하려면 모든 행을 확인해야 하나요?
      en: Do we need to search every row to ensure correctness?
    type: distractor
    why:
      ko: 아니요. 행렬의 순서 성질로 인해 target을 포함한 행은 최대 하나입니다.
      en: No, the ordering property guarantees target appears in at most one row. We can identify and search only that row.
  - q:
      ko: O(m + n) 시간 복잡도로 간단하게 구현할 수 있으면 괜찮나요?
      en: Is an O(m + n) solution acceptable if it is simpler to implement?
    type: distractor
    why:
      ko: 아니요. 문제에서 명시적으로 O(log(m*n))을 요구하므로 더 고급 접근이 필요합니다.
      en: No, the problem explicitly requires O(log(m*n)) complexity. A more sophisticated approach is necessary.
  - q:
      ko: 각 행을 선형 탐색하는 것이 해결책의 핵심인가요?
      en: Is linear scanning each row essential to the solution?
    type: distractor
    why:
      ko: 아니요. 올바른 행을 찾은 후 그 행 내에서도 이진 탐색을 사용합니다.
      en: No, after identifying the correct row, we use binary search within it to achieve O(log n).
approach:
  items:
  - name:
      ko: 두 번의 이진 탐색 (행 탐색 후 열 탐색)
      en: Two binary searches (row then column)
    complexity: O(log m + log n) = O(log(m*n)) time, O(1) space
    type: good
    why:
      ko: 첫 번째 이진 탐색으로 target을 포함한 행을 찾고, 두 번째 이진 탐색으로 그 행 내에서 target을 찾습니다. 요구되는 복잡도를 정확히 만족합니다.
      en: First binary search identifies the correct row, second finds target within that row. Exactly matches O(log(m*n)) requirement.
  - name:
      ko: 단일 이진 탐색 (2D를 1D로 변환)
      en: Single binary search (treat matrix as 1D)
    complexity: O(log(m*n)) time, O(1) space
    type: good
    why:
      ko: 2D 인덱스를 1D로 변환(mid // cols, mid % cols)하여 단 한 번의 이진 탐색으로 처리합니다. 동일한 복잡도로 더 우아합니다.
      en: Convert 2D indices to 1D (mid // cols, mid % cols) and perform single binary search. Same complexity but more elegant.
  - name:
      ko: 선형 탐색 (모든 원소 순회)
      en: Linear scan (check every element)
    complexity: O(m*n) time, O(1) space
    type: distractor
    why:
      ko: 정렬 성질을 무시하고 모든 원소를 확인합니다. 큰 행렬에서는 너무 느리고 O(log(m*n)) 요구사항을 만족하지 못합니다.
      en: Ignores the sorting property and checks every cell. Far too slow and violates O(log(m*n)) requirement.
  - name:
      ko: 첫 번째 열 이진 탐색 후 행 선형 탐색
      en: Binary search first column, then linear scan row
    complexity: O(log m + n) time, O(1) space
    type: distractor
    why:
      ko: 행을 찾는 데 O(log m)이 걸리지만, 그 행의 원소를 확인하는 O(n) 때문에 O(log(m*n))을 달성하지 못합니다.
      en: Finding the row takes O(log m), but linear scanning the row requires O(n), failing to meet O(log(m*n)).
  - name:
      ko: 경계 확인 (휴리스틱)
      en: Check boundaries only (heuristic)
    complexity: O(1) or O(m+n) time, O(1) space
    type: distractor
    why:
      ko: 모서리 원소만 확인하는 방식으로는 대부분의 원소를 놓칠 것입니다. 체계적인 탐색 전략이 없어 신뢰할 수 없습니다.
      en: Checking only corners misses most elements. No systematic search strategy, unreliable for correctness.
logic:
  format: slot
  slots:
  - label:
      ko: 행렬 크기 초기화
      en: Initialize matrix dimensions
    indent: 0
    options:
    - code: ROWS, COLS = len(matrix), len(matrix[0])
      type: good
      why:
        ko: 행과 열의 개수를 미리 저장하여 이진 탐색의 경계값으로 사용합니다.
        en: Store row and column counts for use as binary search boundaries.
    - code: ROWS, COLS = len(matrix[0]), len(matrix)
      type: distractor
      why:
        ko: 행과 열이 바뀌면 탐색 범위가 잘못 설정됩니다.
        en: Swapped indices cause incorrect search boundaries.
    - code: ROWS, COLS = len(matrix), len(matrix)
      type: distractor
      why:
        ko: COLS가 잘못 계산되어 열 탐색 범위가 오류가 됩니다.
        en: COLS is calculated incorrectly, breaking column search bounds.
  - label:
      ko: 행 탐색 범위 설정
      en: Set row search bounds
    indent: 0
    options:
    - code: top, bot = 0, ROWS - 1
      type: good
      why:
        ko: 행 이진 탐색을 위해 첫 행부터 마지막 행까지의 범위를 초기화합니다.
        en: Initialize search window for row binary search from first to last row.
    - code: top, bot = 1, ROWS - 1
      type: distractor
      why:
        ko: top이 1로 시작하면 첫 번째 행(인덱스 0)을 놓칠 수 있습니다.
        en: Starting top at 1 misses the first row (index 0).
    - code: top, bot = 0, ROWS
      type: distractor
      why:
        ko: bot이 ROWS이면 범위를 초과하여 인덱스 오류가 발생합니다.
        en: Setting bot to ROWS exceeds valid indices (should be ROWS-1).
  - label:
      ko: target과 행 경계 비교
      en: Compare target with row boundaries
    indent: 1
    options:
    - code: 'if target > matrix[row][-1]:'
      type: good
      why:
        ko: target이 현재 행의 마지막 원소보다 크면 target은 아래쪽 행에 있어야 합니다.
        en: If target exceeds the last element of current row, target must be in lower rows.
    - code: 'if target > matrix[row][0]:'
      type: distractor
      why:
        ko: 첫 원소와 비교하면 행을 잘못 선택할 수 있습니다.
        en: Comparing with first element leads to incorrect row selection.
    - code: 'if target >= matrix[row][-1]:'
      type: distractor
      why:
        ko: '>=를 사용하면 target이 마지막 원소일 때 오류가 발생합니다.'
        en: Using >= causes incorrect behavior when target equals the last element.
  - label:
      ko: 행 발견 여부 확인
      en: Verify row was found
    indent: 0
    options:
    - code: 'if not (top <= bot):'
      type: good
      why:
        ko: 이진 탐색 후 top > bot이면 target을 포함한 행이 없는 것입니다.
        en: After binary search, if top > bot, no valid row exists containing target.
    - code: 'if top == bot:'
      type: distractor
      why:
        ko: 이 조건은 모든 실패 경우를 감지하지 못합니다.
        en: This condition doesn't catch all failure cases.
    - code: 'if top > bot:'
      type: distractor
      why:
        ko: not을 빼면 반대의 경우를 처리하게 됩니다.
        en: Removing 'not' reverses the logic.
  - label:
      ko: 행 내 target 검색
      en: Binary search within row
    indent: 1
    options:
    - code: 'if target > matrix[row][m]:'
      type: good
      why:
        ko: target이 중간값보다 크면 우측 절반을 탐색하는 표준 이진 탐색입니다.
        en: 'Standard binary search: if target exceeds mid element, search the right half.'
    - code: 'if target > matrix[row][l]:'
      type: distractor
      why:
        ko: 잘못된 포인터(l)를 사용하면 이진 탐색의 진행이 오류가 됩니다.
        en: Using wrong pointer variable breaks binary search progression.
    - code: 'if target >= matrix[row][m]:'
      type: distractor
      why:
        ko: '>=를 사용하면 정확한 일치 조건과 충돌합니다.'
        en: Using >= conflicts with the exact match condition.
trace:
  code:
  - 'class Solution:'
  - '    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:'
  - '        ROWS, COLS = len(matrix), len(matrix[0])'
  - ''
  - '        top, bot = 0, ROWS - 1'
  - '        while top <= bot:'
  - '            row = (top + bot) // 2'
  - '            if target > matrix[row][-1]:'
  - '                top = row + 1'
  - '            elif target < matrix[row][0]:'
  - '                bot = row - 1'
  - '            else:'
  - '                break'
  - ''
  - '        if not (top <= bot):'
  - '            return False'
  - '        row = (top + bot) // 2'
  - '        l, r = 0, COLS - 1'
  - '        while l <= r:'
  - '            m = (l + r) // 2'
  - '            if target > matrix[row][m]:'
  - '                l = m + 1'
  - '            elif target < matrix[row][m]:'
  - '                r = m - 1'
  - '            else:'
  - '                return True'
  - '        return False'
  cases:
  - input: '[[1,3,5,7],[10,11,16,20],[23,30,34,60]]

      3'
    expected: 'true'
  - input: '[[1,3,5,7],[10,11,16,20],[23,30,34,60]]

      13'
    expected: 'false'
  worked_example:
    input: '[[1,3,5,7],[10,11,16,20],[23,30,34,60]]

      3'
    steps:
    - ko: 'ROWS=3, COLS=4 초기화. 행 탐색: top=0, bot=2.'
      en: 'Initialize ROWS=3, COLS=4. Row search: top=0, bot=2.'
    - ko: '행 mid=1: [10,11,16,20]. target 3 < 10이므로 bot=0으로 업데이트.'
      en: 'Row mid=1: [10,11,16,20]. Since target 3 < 10, update bot=0.'
    - ko: '행 mid=0: [1,3,5,7]. target 3은 범위 내, 행 결정. 열 탐색 시작.'
      en: 'Row mid=0: [1,3,5,7]. Target 3 is in range, row found. Start column search.'
    - ko: '열 mid=1: matrix[0][1]=3. target과 일치, True 반환.'
      en: 'Column mid=1: matrix[0][1]=3 matches target. Return True.'
    answer: 'true'
solution:
  code: "class Solution:\n    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:\n        ROWS, COLS = len(matrix), len(matrix[0])\n\n        top, bot = 0, ROWS - 1\n        while top <= bot:\n            row = (top + bot) // 2\n            if target > matrix[row][-1]:\n                top = row + 1\n            elif target < matrix[row][0]:\n                bot = row - 1\n            else:\n                break\n\n        if not (top <= bot):\n            return False\n        row = (top + bot) // 2\n        l, r = 0, COLS - 1\n        while l <= r:\n            m = (l + r) // 2\n            if target > matrix[row][m]:\n                l = m + 1\n            elif target < matrix[row][m]:\n                r = m - 1\n            else:\n                return True\n        return False\n"
  complexity:
    time: O(log m + log n) = O(log(m*n))
    space: O(1)
  followup:
  - ko: 2D 좌표를 1D 인덱스로 변환하여 단 한 번의 이진 탐색으로 O(log(m*n))을 달성할 수 있나요?
    en: Can you achieve O(log(m*n)) with a single binary search by converting 2D coordinates to 1D?
  - ko: 행렬이 반대 순서(오른쪽에서 왼쪽, 아래에서 위로)로 정렬되어 있다면 알고리즘이 어떻게 바뀔까요?
    en: How would the algorithm change if the matrix was sorted in reverse order?
  - ko: m이 n보다 훨씬 크다면 어느 차원을 먼저 탐색하는 것이 더 효율적일까요?
    en: If m >> n, would it be more efficient to search rows or columns first, and why?
```