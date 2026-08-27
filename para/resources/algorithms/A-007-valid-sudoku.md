---
created: '2026-05-09'
date: '2026-05-09'
day: Day 07
difficulty: medium
id: A-007
source:
  curated_in:
  - neetcode150
  number: 36
  platform: leetcode
  slug: valid-sudoku
  url: https://leetcode.com/problems/valid-sudoku/
tags:
- array
- hash-table
- matrix
title:
  en: Valid Sudoku
  ko: 유효한 스도쿠
today: false
type: algorithm
updated: '2026-05-09'
visible: true
---

# 유효한 스도쿠

## Data

```yaml
problem:
  title:
    ko: 유효한 스도쿠
    en: Valid Sudoku
  statement:
    en: 'Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:


      Each row must contain the digits 1-9 without repetition.


      Each column must contain the digits 1-9 without repetition.


      Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.


      Note: A Sudoku board (partially filled) could be valid but is not necessarily solvable. Only the filled cells need to be validated according to the mentioned rules.'
    ko: '9 x 9 스도쿠 보드가 유효한지 판단하시오. 채워진 셀만 다음 규칙에 따라 유효성을 검사하면 됩니다:


      각 행은 1-9의 숫자를 중복 없이 포함해야 합니다.


      각 열은 1-9의 숫자를 중복 없이 포함해야 합니다.


      9개의 3 x 3 부분 박스 각각은 1-9의 숫자를 중복 없이 포함해야 합니다.


      참고: 스도쿠 보드는 부분적으로 채워질 수 있으며 유효하지만 해결 불가능할 수 있습니다. 채워진 셀만 위의 규칙에 따라 검사하면 됩니다.'
  constraints:
  - board.length == 9
  - board[i].length == 9
  - board[i][j] is a digit 1-9 or '.'
  io:
  - input: '[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]'
    output: 'true'
  - input: '[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]'
    output: 'false'
clarifying:
  items:
  - q:
      en: Do we need to validate all three rules (rows, columns, and 3x3 boxes) simultaneously?
      ko: 세 가지 규칙(행, 열, 3x3 박스)을 모두 동시에 검사해야 합니까?
    type: good
    why:
      en: The problem explicitly requires checking all three constraints together—a digit is invalid if it violates any of them.
      ko: 문제에서 명시적으로 세 제약 조건을 모두 검사해야 하며, 숫자는 이 중 어느 것도 위반하면 유효하지 않습니다.
  - q:
      en: What does 'only the filled cells need to be validated' mean?
      ko: '''채워진 셀만 검사''라는 것은 정확히 무엇을 의미합니까?'
    type: good
    why:
      en: Empty cells marked with '.' should be completely ignored—they don't contribute to conflict checking.
      ko: '''.''로 표시된 빈 셀은 완전히 무시해야 하며, 충돌 확인에 기여하지 않습니다.'
  - q:
      en: If a digit appears twice in the same row, is the board automatically invalid?
      ko: 숫자가 같은 행에 두 번 나타나면 보드는 자동으로 유효하지 않습니까?
    type: good
    why:
      en: Yes, any violation of the row, column, or box rule immediately makes the board invalid.
      ko: 네, 행, 열 또는 박스 규칙의 어떤 위반이라도 보드를 즉시 유효하지 않게 합니다.
  - q:
      en: Can we assume the input board is always exactly 9x9?
      ko: 입력 보드가 항상 정확히 9x9라고 가정할 수 있습니까?
    type: good
    why:
      en: Yes, the constraints guarantee this, so no need to validate dimensions.
      ko: 네, 제약 조건에서 이를 보장하므로 차원을 검사할 필요가 없습니다.
  - q:
      en: Should we return which cell has the conflict?
      ko: 충돌이 발생한 셀을 반환해야 합니까?
    type: distractor
    why:
      en: 'No, the problem only asks for a boolean: true if valid, false otherwise.'
      ko: '아니요, 문제는 boolean만 요구합니다: 유효하면 true, 유효하지 않으면 false.'
  - q:
      en: Do we need to check if the Sudoku board is solvable?
      ko: 스도쿠 보드가 풀 수 있는지 확인해야 합니까?
    type: distractor
    why:
      en: No, the problem notes that a valid board is not necessarily solvable. We only validate existing filled cells.
      ko: 아니요, 문제에서 유효한 보드가 반드시 풀 수 있는 것은 아니라고 명시합니다. 우리는 채워진 셀만 검사합니다.
approach:
  items:
  - name:
      en: Hash sets (single pass)
      ko: 해시 집합 (한 번의 통과)
    complexity: O(1) time / O(1) space
    type: good
    why:
      en: Use three dictionaries of sets to track digits in rows, columns, and 3x3 boxes. One pass through all 81 cells checks for conflicts as you go. Optimal and clean.
      ko: 행, 열, 3x3 박스에서 숫자를 추적하기 위해 3개의 집합 딕셔너리를 사용합니다. 81개 셀을 한 번에 통과하면서 충돌을 확인합니다. 최적이고 깔끔합니다.
  - name:
      en: Tuple hashing
      ko: 튜플 해싱
    complexity: O(1) time / O(1) space
    type: good
    why:
      en: Store tuples like (row_idx, digit), (col_idx, digit), (box_idx, digit) in a single set. When you encounter a cell, check if its three tuples already exist.
      ko: (행_인덱스, 숫자), (열_인덱스, 숫자), (박스_인덱스, 숫자) 같은 튜플을 하나의 집합에 저장합니다. 셀을 만날 때 세 튜플이 이미 존재하는지 확인합니다.
  - name:
      en: Brute force (per-cell scanning)
      ko: 무차별 대입 (셀 단위 스캔)
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      en: For each filled cell, scan its entire row, column, and box to check for duplicates. Works but much slower due to repeated scans.
      ko: 채워진 각 셀에 대해 전체 행, 열, 박스를 스캔하여 중복을 확인합니다. 작동하지만 반복 스캔으로 인해 훨씬 느립니다.
  - name:
      en: Multiple passes
      ko: 여러 번의 통과
    complexity: O(1) time / O(1) space
    type: distractor
    why:
      en: Validate rows in one pass, columns in another, boxes in a third. Unnecessarily repetitive—you visit each cell three times.
      ko: 행을 한 번에 검증하고, 열을 다시, 박스를 또 다시 검증합니다. 불필요하게 반복되며 각 셀을 세 번 방문합니다.
logic:
  format: slot
  slots:
  - label:
      en: Initialize tracking structures
      ko: 추적 구조 초기화
    indent: 0
    options:
    - code: cols = collections.defaultdict(set)
      type: good
      why:
        en: Create three dictionaries to track which digits have been seen in each row, column, and 3x3 box. defaultdict(set) avoids KeyError when accessing new keys.
        ko: 각 행, 열, 3x3 박스에서 본 숫자를 추적하기 위해 3개의 딕셔너리를 만듭니다. defaultdict(set)은 새로운 키 접근 시 KeyError를 피합니다.
    - code: cols = {}
      type: distractor
      why:
        en: Regular dict requires checking if key exists before accessing—defaultdict is more elegant and error-safe.
        ko: 일반 딕셔너리는 접근 전에 키 존재 여부를 확인해야 하므로 defaultdict이 더 우아하고 안전합니다.
    - code: cols = set()
      type: distractor
      why:
        en: A single set cannot organize digits by row/column/box—you need a mapping structure.
        ko: 단일 집합은 숫자를 행/열/박스별로 구분할 수 없으므로 매핑 구조가 필요합니다.
  - label:
      en: Iterate through all cells
      ko: 모든 셀을 반복
    indent: 0
    options:
    - code: 'for r in range(9):'
      type: good
      why:
        en: Nested loops check all 9 rows and 9 columns. range(9) is cleaner than iterating directly over the board.
        ko: 중첩 루프는 모든 9개 행과 9개 열을 확인합니다. range(9)는 보드를 직접 반복하는 것보다 깔끔합니다.
    - code: 'for r in range(8):'
      type: distractor
      why:
        en: range(8) only covers 0-7, missing the last row (index 8).
        ko: range(8)은 0-7만 포함하여 마지막 행(인덱스 8)을 놓칩니다.
    - code: 'for row in board:'
      type: distractor
      why:
        en: This loses the row index needed for rows[r].
        ko: 이렇게 하면 rows[r]에 필요한 행 인덱스를 잃습니다.
  - label:
      en: Skip empty cells
      ko: 빈 셀 건너뛰기
    indent: 2
    options:
    - code: 'if board[r][c] == ".":'
      type: good
      why:
        en: The '.' character marks empty cells. Skip them because only filled cells need validation.
        ko: '''.'' 문자는 빈 셀을 표시합니다. 채워진 셀만 검증이 필요하므로 건너뜁니다.'
    - code: 'if board[r][c] == 0:'
      type: distractor
      why:
        en: The problem uses '.' strings, not 0. This condition will never be true.
        ko: 문제는 0이 아닌 '.' 문자열을 사용합니다. 이 조건은 절대 참이 아닙니다.
    - code: 'if not board[r][c]:'
      type: distractor
      why:
        en: In Python, '.' is truthy, so this won't skip empty cells.
        ko: Python에서 '.'는 참이므로 빈 셀을 건너뛰지 않습니다.
  - label:
      en: Check for conflicts
      ko: 충돌 확인
    indent: 2
    options:
    - code: board[r][c] in rows[r]
      type: good
      why:
        en: Use 'in' to check set membership. If the digit is already in the row's set, it's a duplicate. Apply the same check to columns and boxes.
        ko: '''in''을 사용하여 집합 멤버십을 확인합니다. 숫자가 이미 행의 집합에 있으면 중복입니다. 열과 박스도 같은 방식으로 확인합니다.'
    - code: board[r][c] == rows[r]
      type: distractor
      why:
        en: This compares a digit string to a set object—always false. Use 'in' for membership.
        ko: 이것은 숫자 문자열을 집합 객체와 비교하므로 항상 거짓입니다. 멤버십에는 'in'을 사용하세요.
    - code: rows[r].get(board[r][c])
      type: distractor
      why:
        en: Sets don't have a .get() method—that's for dicts. Use 'in' for sets.
        ko: 집합에는 .get() 메서드가 없습니다. 집합에는 'in'을 사용하세요.
  - label:
      en: Map cell to 3x3 box
      ko: 셀을 3x3 박스로 매핑
    indent: 2
    options:
    - code: or board[r][c] in squares[(r // 3, c // 3)]
      type: good
      why:
        en: Integer division by 3 maps row/column indices to their 3x3 box. Rows 0-2 map to 0, 3-5 to 1, 6-8 to 2. Tuple (r//3, c//3) uniquely identifies each box.
        ko: 3으로의 정수 나눗셈은 행/열 인덱스를 3x3 박스로 매핑합니다. 행 0-2는 0으로, 3-5는 1로, 6-8은 2로 매핑됩니다. 튜플 (r//3, c//3)은 각 박스를 고유하게 식별합니다.
    - code: squares[(r // 2, c // 2)]
      type: distractor
      why:
        en: Division by 2 creates 2x2 or 2.25x2.25 boxes, not 3x3. Box mapping would be incorrect.
        ko: 2로 나누면 2x2 또는 2.25x2.25 박스가 생성되어 3x3이 아닙니다. 박스 매핑이 잘못됩니다.
    - code: squares[(r % 3, c % 3)]
      type: distractor
      why:
        en: Modulo gives position within the box (0-2), not the box index. Multiple boxes would map to the same key.
        ko: 모듈로는 박스 내의 위치(0-2)를 제공하지만 박스 인덱스를 제공하지 않습니다. 여러 박스가 같은 키로 매핑됩니다.
  - label:
      en: Track seen values
      ko: 본 값 추적
    indent: 2
    options:
    - code: cols[c].add(board[r][c])
      type: good
      why:
        en: Add the digit to the column's set so future cells in the same column can detect duplicates. Do the same for rows and boxes.
        ko: 같은 열의 향후 셀이 중복을 감지할 수 있도록 열의 집합에 숫자를 추가합니다. 행과 박스도 같은 방식으로 수행합니다.
    - code: cols[c].append(board[r][c])
      type: distractor
      why:
        en: Sets don't have .append()—that's for lists. Use .add() for sets.
        ko: 집합에는 .append()가 없습니다—그것은 리스트용입니다. 집합에는 .add()를 사용하세요.
    - code: cols[c] = {board[r][c]}
      type: distractor
      why:
        en: This overwrites the entire set, losing all previous values. Use .add() to insert while preserving.
        ko: 이것은 전체 집합을 덮어써 모든 이전 값을 잃습니다. 보존하면서 삽입하려면 .add()를 사용하세요.
trace:
  code:
  - 'class Solution:'
  - '    def isValidSudoku(self, board: List[List[str]]) -> bool:'
  - '        cols = collections.defaultdict(set)'
  - '        rows = collections.defaultdict(set)'
  - '        squares = collections.defaultdict(set)  # key = (r /3, c /3)'
  - ''
  - '        for r in range(9):'
  - '            for c in range(9):'
  - '                if board[r][c] == ".":'
  - '                    continue'
  - '                if ('
  - '                    board[r][c] in rows[r]'
  - '                    or board[r][c] in cols[c]'
  - '                    or board[r][c] in squares[(r // 3, c // 3)]'
  - '                ):'
  - '                    return False'
  - '                cols[c].add(board[r][c])'
  - '                rows[r].add(board[r][c])'
  - '                squares[(r // 3, c // 3)].add(board[r][c])'
  - ''
  - '        return True'
  cases:
  - input: '[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]'
    expected: 'true'
  - input: '[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]'
    expected: 'false'
  worked_example:
    input: '[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]'
    steps:
    - en: Initialize three empty defaultdict(set) for rows, cols, and squares.
      ko: 행, 열, 박스에 대해 3개의 빈 defaultdict(set)을 초기화합니다.
    - en: 'At (0,0): digit ''5''. Check—not in rows[0], cols[0], or squares[(0,0)]. Add ''5'' to all three sets. Continue through filled cells.'
      ko: (0,0)에서 숫자 '5'. 확인—rows[0], cols[0], squares[(0,0)]에 없습니다. 세 집합 모두에 '5'를 추가합니다. 채워진 셀을 계속 처리합니다.
    - en: Skip all '.' cells. For each filled cell, verify no conflicts in row, column, or box. If any conflict found, return False immediately.
      ko: 모든 '.' 셀을 건너뜁니다. 채워진 각 셀에 대해 행, 열, 박스에서 충돌이 없는지 확인합니다. 충돌이 발견되면 즉시 False를 반환합니다.
    - en: Process all 81 cells without finding any duplicates. Return True at the end.
      ko: 중복 없이 모든 81개 셀을 처리합니다. 끝에서 True를 반환합니다.
    answer: 'true'
solution:
  code: "class Solution:\n    def isValidSudoku(self, board: List[List[str]]) -> bool:\n        cols = collections.defaultdict(set)\n        rows = collections.defaultdict(set)\n        squares = collections.defaultdict(set)  # key = (r /3, c /3)\n\n        for r in range(9):\n            for c in range(9):\n                if board[r][c] == \".\":\n                    continue\n                if (\n                    board[r][c] in rows[r]\n                    or board[r][c] in cols[c]\n                    or board[r][c] in squares[(r // 3, c // 3)]\n                ):\n                    return False\n                cols[c].add(board[r][c])\n                rows[r].add(board[r][c])\n                squares[(r // 3, c // 3)].add(board[r][c])\n\n        return True\n"
  complexity:
    time: O(1)
    space: O(1)
  followup:
  - en: How would you modify the solution to find and return all cells that violate Sudoku rules, rather than just detecting invalidity?
    ko: 유효하지 않음을 감지하는 것이 아니라 스도쿠 규칙을 위반하는 모든 셀을 찾아서 반환하도록 솔루션을 수정하시겠습니까?
  - en: How would the solution scale if the grid was N×N instead of 9×9, where each sub-box is √N × √N?
    ko: 각 부분 박스가 √N × √N인 9×9 대신 N×N 그리드인 경우 솔루션은 어떻게 확장됩니까?
  - en: Could you validate a Sudoku board if cells are given to you one at a time as a stream, without storing the entire board?
    ko: 전체 보드를 저장하지 않고 셀이 스트림으로 한 번에 하나씩 주어지는 경우 스도쿠 보드를 검증할 수 있습니까?
```