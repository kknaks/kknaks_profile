---
created: '2026-08-06'
date: '2026-08-06'
day: Day 79
difficulty: hard
id: A-079
source:
  curated_in:
  - neetcode150
  number: 51
  platform: leetcode
  slug: n-queens
  url: https://leetcode.com/problems/n-queens/
status: draft
tags:
- array
- backtracking
- algorithm-x
title:
  en: N-Queens
  ko: N-퀸 문제
today: false
type: algorithm
updated: '2026-08-06'
visible: true
---

# N-퀸 문제

## Data

```yaml
problem:
  title:
    ko: N-퀸 문제
    en: N-Queens
  statement:
    ko: 'n×n 체스판에 n개의 퀸을 서로 공격할 수 없도록 배치하는 문제입니다. 퀸은 같은 행, 열, 대각선 위치에 있는 다른 기물을 공격할 수 있습니다.


      정수 n이 주어졌을 때, n-퀸 문제의 모든 서로 다른 해결책을 반환하세요. 답은 어떤 순서로든 반환할 수 있습니다.


      각 해결책은 퀸을 배치한 보드 설정을 나타내며, ''Q''는 퀸을, ''.''는 빈 칸을 나타냅니다.'
    en: 'The n-queens puzzle is the problem of placing n queens on an n×n chessboard such that no two queens attack each other.


      Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.


      Each solution contains a distinct board configuration of the n-queens'' placement, where ''Q'' and ''.'' both indicate a queen and an empty space, respectively.'
  constraints:
  - 1 ≤ n ≤ 9
  - Queens attack horizontally, vertically, and diagonally
  - Each row and column can contain at most one queen
  io:
  - input: '4'
    output: '[["..Q.","Q...","...Q",".Q.."],["Q...","...Q",".Q..","..Q."]]'
  - input: '1'
    output: '[["Q"]]'
clarifying:
  items:
  - q:
      ko: 체스판에서 퀸이 다른 퀸을 '공격'한다는 것은 무엇을 의미하나요?
      en: What does it mean for a queen to 'attack' another queen on a chessboard?
    type: good
    why:
      ko: 퀸의 공격 범위(수평, 수직, 대각선)를 정확히 이해하는 것이 문제 해결의 첫 단계입니다.
      en: Understanding the attack range (horizontal, vertical, and diagonal) is fundamental to solving this problem correctly.
  - q:
      ko: 같은 행에 여러 개의 퀸을 배치할 수 있나요?
      en: Can we place multiple queens in the same row?
    type: distractor
    why:
      ko: 이 질문은 학생이 같은 행의 퀸들도 서로 공격할 수 있다는 것을 이해하는지 테스트합니다.
      en: This tests whether the student understands that queens in the same row can attack each other.
  - q:
      ko: 왜 충돌 추적을 위해 집합(set)을 사용하나요?
      en: Why do we use sets to track conflicts instead of checking the entire board each time?
    type: good
    why:
      ko: 집합을 사용하면 충돌 검사를 O(1) 시간에 수행할 수 있어 효율성이 크게 향상됩니다.
      en: Sets allow us to check for conflicts in O(1) time instead of scanning the entire board, significantly improving efficiency.
  - q:
      ko: 대각선 충돌을 어떻게 표현하나요?
      en: How do we represent diagonal conflicts mathematically?
    type: good
    why:
      ko: 정 대각선은 r+c로, 역 대각선은 r-c로 표현하면 충돌을 효율적으로 감지할 수 있습니다.
      en: Positive diagonals can be represented by r+c and negative diagonals by r-c, allowing efficient conflict detection.
  - q:
      ko: 해의 순서가 정렬되어야 하나요?
      en: Do the solutions need to be in a specific order?
    type: distractor
    why:
      ko: 문제에서 '어떤 순서로든 반환할 수 있습니다'라고 명시하므로 정렬은 필요하지 않습니다.
      en: The problem explicitly states that we can return the answer in any order, so sorting is not required.
  - q:
      ko: 백트래킹에서 상태를 복원하는 이유는?
      en: Why do we need to restore the state (backtrack) after exploring a placement?
    type: good
    why:
      ko: 다른 가능한 배치를 탐색하기 위해 퀸을 제거하고 추적 상태를 되돌려야 합니다.
      en: We need to undo the placement and restore the tracking state to explore other possible configurations.
  - q:
      ko: 동적 계획법으로 이 문제를 해결할 수 있나요?
      en: Can we use dynamic programming to solve this problem?
    type: distractor
    why:
      ko: 이 문제는 모든 해결책을 찾아야 하므로 백트래킹이 더 적합합니다. DP는 최적 해를 찾는 데 더 유용합니다.
      en: This problem requires finding all solutions rather than an optimal solution, making backtracking more suitable than DP.
approach:
  items:
  - name:
      ko: 백트래킹 (대각선 추적)
      en: Backtracking with diagonal tracking
    complexity: O(N!) time / O(N) space
    type: good
    why:
      ko: 행별로 퀸을 배치하면서 열과 대각선 충돌을 효율적으로 추적합니다. 각 행에서 한 번의 퀸만 배치하므로 최적의 솔루션입니다.
      en: Places queens row by row while efficiently tracking column and diagonal conflicts using sets. Placing exactly one queen per row ensures optimality.
  - name:
      ko: 전체 순열 탐색 (브루트 포스)
      en: Brute force - check all permutations
    complexity: O(N^N) time / O(N) space
    type: distractor
    why:
      ko: 모든 가능한 배치(N^N개)를 확인해야 하므로 매우 비효율적입니다.
      en: Requires checking all N^N possible placements, making it extremely inefficient.
  - name:
      ko: 제약 만족 (CSP) 알고리즘
      en: Constraint satisfaction programming
    complexity: O(N!) time / O(N) space
    type: good
    why:
      ko: 백트래킹과 유사하게, 제약 조건을 활용하여 탐색 공간을 줄입니다.
      en: Similar to backtracking, it uses constraint propagation to reduce the search space.
  - name:
      ko: 그리디 배치
      en: Greedy placement
    complexity: O(N) time / O(N) space
    type: distractor
    why:
      ko: 각 행에서 단순히 첫 번째 가능한 위치에 퀸을 배치하면 모든 해결책을 찾을 수 없습니다.
      en: Simply placing queens at the first available position in each row will not find all solutions or may find none.
logic:
  format: slot
  slots:
  - label:
      ko: '초기화: 열 충돌 추적'
      en: Initialize column tracking
    indent: 0
    options:
    - code: col = set()
      type: good
      why:
        ko: 같은 열에 두 퀸이 없도록 하기 위해 점유된 열을 추적합니다.
        en: Track which columns already have queens to prevent multiple queens in the same column.
    - code: col = []
      type: distractor
      why:
        ko: 리스트는 멤버십 검사가 O(n)이므로 비효율적입니다.
        en: Lists require O(n) lookup time, making membership checking inefficient.
    - code: col = {}
      type: distractor
      why:
        ko: 딕셔너리는 불필요하며, 집합이 더 간결하고 의도를 명확히 합니다.
        en: A dictionary is unnecessary here; a set is cleaner and clearly expresses intent.
  - label:
      ko: '초기화: 정 대각선 충돌 추적 (r+c)'
      en: Initialize positive diagonal tracking (r+c)
    indent: 0
    options:
    - code: 'posDiag = set()  # (r + c)'
      type: good
      why:
        ko: 우하향 대각선(↘)은 r+c 값이 동일하므로, 이를 통해 대각선 충돌을 추적합니다.
        en: Cells on the same positive diagonal all have the same r+c value, enabling efficient tracking.
    - code: posDiag = {}
      type: distractor
      why:
        ko: 존재 여부만 필요하므로 집합이 더 적절합니다.
        en: We only need to track presence, not values, so a set is more appropriate.
    - code: 'posDiag = set()  # (r * c)'
      type: distractor
      why:
        ko: r*c는 서로 다른 위치에서 같은 값이 나올 수 있어 대각선을 정확히 추적하지 못합니다.
        en: r*c doesn't uniquely identify diagonals; different positions can have the same product.
  - label:
      ko: '초기화: 역 대각선 충돌 추적 (r-c)'
      en: Initialize negative diagonal tracking (r-c)
    indent: 0
    options:
    - code: 'negDiag = set()  # (r - c)'
      type: good
      why:
        ko: 우상향 대각선(↙)은 r-c 값이 동일하므로, 이를 통해 대각선 충돌을 추적합니다.
        en: Cells on the same negative diagonal all have the same r-c value, enabling efficient tracking.
    - code: 'negDiag = set()  # (c - r)'
      type: distractor
      why:
        ko: c-r은 r-c의 음수일 뿐이므로 정보는 동일하지만, r-c가 표준 관례입니다.
        en: While c-r is mathematically equivalent, r-c is the standard convention.
    - code: 'negDiag = set()  # (r - c) % n'
      type: distractor
      why:
        ko: 모듈로 연산은 불필요하며 음수 처리 문제를 야기합니다.
        en: Modulo operation is unnecessary and complicates handling of negative values.
  - label:
      ko: '기저 사례: 모든 퀸 배치 완료'
      en: 'Base case: all queens placed successfully'
    indent: 1
    options:
    - code: 'if r == n:'
      type: good
      why:
        ko: 행 인덱스 r이 n에 도달했다면 모든 행에 퀸이 배치되었으므로 해결책을 저장합니다.
        en: When r equals n, we've successfully placed queens in all rows, so we record this solution.
    - code: 'if r == n - 1:'
      type: distractor
      why:
        ko: n-1은 마지막 행의 인덱스이며, 아직 마지막 퀸을 배치하지 않았습니다.
        en: At r == n-1, we haven't placed the last queen yet, resulting in an off-by-one error.
    - code: 'if len(col) == n:'
      type: distractor
      why:
        ko: col의 크기가 n이어도 모든 행을 순서대로 처리했는지 보장하지 못합니다.
        en: Checking col size doesn't guarantee we've processed all rows in order.
  - label:
      ko: '충돌 검사: 열과 대각선 확인'
      en: Check for conflicts in column and diagonals
    indent: 2
    options:
    - code: 'if c in col or (r + c) in posDiag or (r - c) in negDiag:'
      type: good
      why:
        ko: 현재 위치에 퀸을 배치하기 전에, 같은 열 또는 대각선에 이미 퀸이 있는지 확인합니다.
        en: Before placing a queen, verify it doesn't share a column or diagonal with existing queens.
    - code: 'if c not in col and (r + c) not in posDiag and (r - c) not in negDiag:'
      type: distractor
      why:
        ko: 이 조건은 반대이며, 계속문(continue) 대신 배치 로직이 필요합니다.
        en: This inverts the condition; would require restructuring the placement logic.
    - code: 'if c in col or (r + c) in posDiag:'
      type: distractor
      why:
        ko: 역 대각선 확인이 빠져있어 불완전한 충돌 검사입니다.
        en: Missing the negative diagonal check, leaving the conflict detection incomplete.
  - label:
      ko: 퀸 배치 및 상태 업데이트
      en: Place queen and update tracking state
    indent: 2
    options:
    - code: col.add(c)
      type: good
      why:
        ko: 추적 집합에 현재 위치를 기록하고, 보드에 퀸을 표시한 후 다음 행을 재귀적으로 탐색합니다.
        en: Add the current position to all tracking sets, mark it on the board, then proceed to the next row.
    - code: col.add(c); posDiag.add(r + c); negDiag.add(r - c)
      type: distractor
      why:
        ko: 보드 배열을 업데이트하지 않으면 최종 해결책 생성 시 정보가 손실됩니다.
        en: Without updating the board, the final solution strings cannot be constructed correctly.
    - code: board[r][c] = "Q"
      type: distractor
      why:
        ko: 추적 집합에 위치를 기록하지 않으면 충돌 검사가 작동하지 않습니다.
        en: Without updating tracking sets, conflict detection in subsequent rows fails.
  - label:
      ko: '재귀 호출: 다음 행으로 진행'
      en: Recursively place queens in the next row
    indent: 2
    options:
    - code: backtrack(r + 1)
      type: good
      why:
        ko: 현재 행의 배치를 완료했으므로 다음 행(r+1)에서 퀸 배치를 시도합니다.
        en: After placing a queen in the current row, recursively attempt to place queens in row r+1.
    - code: backtrack(r)
      type: distractor
      why:
        ko: 같은 행을 다시 호출하면 무한 재귀에 빠집니다.
        en: Recursing on the same row creates an infinite loop.
    - code: backtrack(r + 2)
      type: distractor
      why:
        ko: 행을 건너뛰면 일부 행에는 퀸이 배치되지 않습니다.
        en: Skipping rows means some rows will never have queens, producing invalid solutions.
  - label:
      ko: '백트래킹: 상태 복원'
      en: 'Backtrack: restore state for next attempt'
    indent: 2
    options:
    - code: col.remove(c)
      type: good
      why:
        ko: 배치를 취소하고 추적 상태를 원래로 되돌려 같은 행의 다른 열 위치를 탐색합니다.
        en: Undo the placement by removing the queen from tracking sets and board, allowing other column positions to be tried.
    - code: '# 백트래킹 코드 생략'
      type: distractor
      why:
        ko: 상태를 복원하지 않으면 다음 시도가 잘못된 제약 조건을 상속합니다.
        en: Without restoring state, subsequent placements inherit incorrect conflict tracking.
    - code: col.clear(); posDiag.clear(); negDiag.clear()
      type: distractor
      why:
        ko: 모든 추적을 초기화하면 이전 행의 퀸 정보가 손실되어 유효하지 않은 해가 생성됩니다.
        en: Clearing all tracking loses information about queens in previous rows, producing invalid solutions.
trace:
  code:
  - 'class Solution:'
  - '    def solveNQueens(self, n: int) -> List[List[str]]:'
  - '        col = set()'
  - '        posDiag = set()  # (r + c)'
  - '        negDiag = set()  # (r - c)'
  - ''
  - '        res = []'
  - '        board = [["."] * n for i in range(n)]'
  - ''
  - '        def backtrack(r):'
  - '            if r == n:'
  - '                copy = ["".join(row) for row in board]'
  - '                res.append(copy)'
  - '                return'
  - ''
  - '            for c in range(n):'
  - '                if c in col or (r + c) in posDiag or (r - c) in negDiag:'
  - '                    continue'
  - ''
  - '                col.add(c)'
  - '                posDiag.add(r + c)'
  - '                negDiag.add(r - c)'
  - '                board[r][c] = "Q"'
  - ''
  - '                backtrack(r + 1)'
  - ''
  - '                col.remove(c)'
  - '                posDiag.remove(r + c)'
  - '                negDiag.remove(r - c)'
  - '                board[r][c] = "."'
  - ''
  - '        backtrack(0)'
  - '        return res'
  cases:
  - input: '4'
    expected: '[["..Q.","Q...","...Q",".Q.."],["Q...","...Q",".Q..","..Q."]]'
  - input: '1'
    expected: '[["Q"]]'
  worked_example:
    input: '4'
    steps:
    - ko: 'Row 0 시작: 각 열을 시도. Col 0에 퀸 배치. col={0}, posDiag={0}, negDiag={0}'
      en: 'Row 0: Try each column position. Place queen at column 0. col={0}, posDiag={0}, negDiag={0}'
    - ko: 'Row 1: Col 0-2 모두 충돌. Col 2에 퀸 배치. col={0,2}, posDiag={0,3}, negDiag={0,-1}'
      en: 'Row 1: Columns 0-2 conflict. Place at column 2. col={0,2}, posDiag={0,3}, negDiag={0,-1}'
    - ko: 'Row 2-3: 계속 탐색. 배치 실패 시 백트래킹. 다른 분기 시도.'
      en: 'Row 2-3: Continue exploring. Backtrack on conflicts. Try alternative branches.'
    - ko: 모든 탐색 경로 완료. 총 2개의 유효한 해 발견 및 반환.
      en: All search paths explored. Find 2 valid solutions and return them.
    answer: '[["..Q.","Q...","...Q",".Q.."],["Q...","...Q",".Q..","..Q."]]'
solution:
  code: "class Solution:\n    def solveNQueens(self, n: int) -> List[List[str]]:\n        col = set()\n        posDiag = set()  # (r + c)\n        negDiag = set()  # (r - c)\n\n        res = []\n        board = [[\".\"] * n for i in range(n)]\n\n        def backtrack(r):\n            if r == n:\n                copy = [\"\".join(row) for row in board]\n                res.append(copy)\n                return\n\n            for c in range(n):\n                if c in col or (r + c) in posDiag or (r - c) in negDiag:\n                    continue\n\n                col.add(c)\n                posDiag.add(r + c)\n                negDiag.add(r - c)\n                board[r][c] = \"Q\"\n\n                backtrack(r + 1)\n\n                col.remove(c)\n                posDiag.remove(r + c)\n                negDiag.remove(r - c)\n                board[r][c] = \".\"\n\n        backtrack(0)\n        return res\n"
  complexity:
    time: O(N!) — 백트래킹으로 N!에 비례하는 유효한 배치 탐색 / Explores valid placements bounded by N! through backtracking pruning
    space: O(N) — 재귀 스택 깊이 O(N) + 추적 집합 O(N) / Recursion stack depth O(N) plus tracking sets O(N)
  followup:
  - ko: 'N이 매우 클 때(예: n=20) 성능을 개선할 방법은?'
    en: How would you optimize this for very large N (e.g., n=20)?
  - ko: 보드 배치가 아닌 해의 개수만 필요하다면 어떻게 수정하시겠습니까?
    en: If you only need the count of solutions (not the board configurations), how would you modify the algorithm?
  - ko: '다른 제약 조건이 있는 변형 문제(예: K-Queens, 일부 셀이 점유됨)를 어떻게 해결하시겠습니까?'
    en: How would you adapt this solution for variants with different constraints (e.g., K-Queens or pre-occupied cells)?
```