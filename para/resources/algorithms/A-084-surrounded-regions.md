---
created: '2026-08-11'
date: '2026-08-11'
day: Day 84
difficulty: medium
id: A-084
source:
  curated_in:
  - neetcode150
  number: 130
  platform: leetcode
  slug: surrounded-regions
  url: https://leetcode.com/problems/surrounded-regions/
tags:
- array
- depth-first-search
- breadth-first-search
- union-find
- matrix
title:
  en: Surrounded Regions
  ko: 둘러싸인 영역
today: false
type: algorithm
updated: '2026-08-11'
visible: true
---

# 둘러싸인 영역

## Data

```yaml
problem:
  title:
    ko: 둘러싸인 영역
    en: Surrounded Regions
  statement:
    ko: 'm x n 행렬 board가 주어지며, 이 행렬은 ''X''와 ''O'' 문자를 포함합니다. 다음과 같이 정의되는 둘러싸인 영역을 포획하세요:


      연결(Connect): 셀은 수평 또는 수직으로 인접한 셀과 연결됩니다.


      영역(Region): 영역을 형성하려면 모든 ''O'' 셀을 연결해야 합니다.


      포위(Surround): 영역이 포위되면 그 영역의 어떤 ''O'' 셀도 보드의 경계에 있지 않습니다. 이러한 영역은 ''X'' 셀로 완전히 둘러싸여 있습니다.


      둘러싸인 영역을 포획하려면 원래 보드에서 모든 ''O''를 ''X''로 바꾸세요. 함수는 아무것도 반환할 필요가 없습니다.'
    en: 'You are given an m x n matrix board containing letters ''X'' and ''O'', capture regions that are surrounded:


      Connect: A cell is connected to adjacent cells horizontally or vertically.


      Region: To form a region connect every ''O'' cell.


      Surround: A region is surrounded if none of the ''O'' cells in that region are on the edge of the board. Such regions are completely enclosed by ''X'' cells.


      To capture a surrounded region, replace all ''O''s with ''X''s in-place within the original board. You do not need to return anything.'
  constraints:
  - 1 ≤ m, n ≤ 200
  - board[i][j] is 'X' or 'O'
  - Modification must be in-place
  io:
  - input: '[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]'
    output: '[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]'
  - input: '[["X"]]'
    output: '[["X"]]'
clarifying:
  items:
  - q:
      ko: 어떤 조건이 영역을 '포위'되었다고 판단하나요?
      en: What condition makes a region 'surrounded'?
    type: good
    why:
      ko: 영역이 포위되려면 그 영역의 모든 'O' 셀이 보드 경계와 접하지 않아야 합니다.
      en: Core understanding—a region is surrounded only if NONE of its 'O' cells touch the board boundary.
  - q:
      ko: 대각선 연결이 'O' 영역 형성에 포함되나요?
      en: Do diagonal connections count when forming an 'O' region?
    type: good
    why:
      ko: 문제에서 명시적으로 '수평 또는 수직'만 언급하므로 대각선은 포함되지 않습니다.
      en: The problem explicitly states 'horizontally or vertically', so diagonals are excluded.
  - q:
      ko: '''O'' 셀이 보드 경계에 닿으면 그 영역을 포획할 수 있나요?'
      en: If an 'O' cell touches the board edge, can that region ever be captured?
    type: good
    why:
      ko: 아니요—영역의 어떤 'O'라도 경계에 닿으면 전체 영역이 포위되지 않으므로 포획되지 않습니다.
      en: No—if any 'O' in a region touches an edge, the entire region is unsurrounded and cannot be captured.
  - q:
      ko: 원본 board를 수정하지 않고 새로운 board를 반환해야 하나요?
      en: Should we return a modified copy or modify in-place?
    type: good
    why:
      ko: 문제에서 '아무것도 반환할 필요가 없습니다'라고 명시하므로 원본을 제자리에서 수정합니다.
      en: The problem states 'You do not need to return anything'—modify the board in-place.
  - q:
      ko: 전체 board가 'O'로만 이루어지면 어떻게 되나요?
      en: What if the entire board contains only 'O's?
    type: good
    why:
      ko: 모든 'O' 셀이 경계에 닿으므로 아무것도 포획되지 않습니다. 경계 조건 이해가 중요합니다.
      en: All 'O' cells touch edges, so nothing is captured. Tests boundary condition understanding.
  - q:
      ko: 영역의 모든 셀을 한 번에 방문하지 않고 개별적으로 검사하면 어떻게 되나요?
      en: Should we check each 'O' cell individually for boundary reachability?
    type: distractor
    why:
      ko: 각 셀마다 경계 도달 가능성을 확인하면 중복 작업이 많아져 O((m*n)²) 시간 복잡도가 됩니다.
      en: Checking each cell independently causes redundant work; boundary-first approach is more efficient.
  - q:
      ko: DFS와 BFS 중 어느 것이 이 문제에 더 적합한가요?
      en: Is DFS or BFS better for this problem?
    type: distractor
    why:
      ko: 둘 다 유효하고 시간/공간 복잡도가 동일합니다. BFS는 매우 깊은 보드에서 스택 오버플로우를 피할 수 있습니다.
      en: Both are valid with same complexity. BFS may be safer for very large boards to avoid stack overflow.
approach:
  items:
  - name:
      ko: 경계에서 시작하는 깊이 우선 탐색
      en: DFS from boundary
    complexity: O(m*n) time / O(m*n) space
    type: good
    why:
      ko: 경계의 'O'에서 DFS로 연결된 모든 'O'를 표시하고, 표시되지 않은 'O'만 'X'로 변환합니다. 직관적이고 효율적입니다.
      en: Mark all 'O's connected to edges via DFS starting from boundary cells, then flip unmarked 'O's. Efficient and intuitive.
  - name:
      ko: 경계에서 시작하는 너비 우선 탐색
      en: BFS from boundary
    complexity: O(m*n) time / O(m*n) space
    type: good
    why:
      ko: DFS와 동일한 논리이지만 큐를 사용해 반복적으로 처리합니다. 매우 깊은 보드에서 스택 오버플로우를 피할 수 있습니다.
      en: Same logic as DFS but uses queue for iterative processing. Avoids potential stack overflow on very large boards.
  - name:
      ko: 각 'O' 셀에서 경계 도달 가능성 개별 확인
      en: Individual boundary reachability check
    complexity: O((m*n)²) time / O(m*n) space
    type: distractor
    why:
      ko: 각 'O' 셀마다 별도로 경계 도달 여부를 확인하므로 중복 계산이 많고 비효율적입니다.
      en: For each 'O', check if it reaches boundary independently—massive redundant work compared to boundary-first approach.
  - name:
      ko: Union-Find (분리 집합)
      en: Union-Find
    complexity: O(m*n·α(m*n)) time / O(m*n) space
    type: distractor
    why:
      ko: 이론적으로 가능하지만 이 문제에서는 DFS/BFS보다 복잡하고 구현 난도가 높으며 이득이 없습니다.
      en: Possible but overkill; DFS/BFS is more straightforward and equally efficient for this problem.
logic:
  format: slot
  slots:
  - label:
      ko: 방문 추적 집합 초기화
      en: Initialize visited set
    indent: 0
    options:
    - code: flag = set()
      type: good
      why:
        ko: 방문한 셀을 추적하여 중복 방문과 무한 루프를 방지합니다.
        en: Tracks visited cells to prevent revisiting and infinite loops in recursion.
    - code: flag = []
      type: distractor
      why:
        ko: 리스트는 (r,c) 튜플 조회가 O(n)이므로 집합보다 느립니다.
        en: List membership test is O(n); set is O(1) for coordinate tuples.
    - code: flag = [[False] * cols for _ in range(rows)]
      type: distractor
      why:
        ko: 2D 배열은 메모리가 더 필요하고 tuple 저장에 부적합합니다.
        en: 2D array wastes space and doesn't naturally store coordinate tuples.
  - label:
      ko: 재귀 함수의 경계 조건 확인
      en: Check boundary and conditions in DFS
    indent: 1
    options:
    - code: 'if not(r in range(rows) and c in range(cols)) or board[r][c] != ''O'' or (r, c) in flag:'
      type: good
      why:
        ko: 범위, 셀 값, 방문 여부를 모두 확인하여 안전한 재귀를 보장합니다.
        en: Checks bounds, cell value, and visited status to safely guard recursion base case.
    - code: 'if board[r][c] != ''O'' or (r, c) in flag:'
      type: distractor
      why:
        ko: 범위 검사가 없어 음수나 범위 초과 인덱스로 IndexError가 발생합니다.
        en: Missing bounds check causes IndexError on negative or out-of-bounds indices.
    - code: 'if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] == ''X'':'
      type: distractor
      why:
        ko: 방문 여부 확인이 없어 같은 셀을 여러 번 처리할 수 있습니다.
        en: Missing visited check allows processing same cell multiple times.
  - label:
      ko: 현재 셀을 방문 집합에 추가
      en: Mark cell as visited
    indent: 2
    options:
    - code: flag.add((r, c))
      type: good
      why:
        ko: 재귀 전에 마크하여 사이클 없이 각 셀을 정확히 한 번 처리합니다.
        en: Mark BEFORE recursion to prevent processing the same cell multiple times.
    - code: board[r][c] = '#'
      type: distractor
      why:
        ko: board를 직접 수정하면 나중에 'O' 여부를 판단할 수 없습니다.
        en: Modifying board directly loses information needed for later checks.
    - code: visited[r * cols + c] = True
      type: distractor
      why:
        ko: 1D 배열로 변환하는 것은 가능하지만 tuple 집합보다 덜 명확합니다.
        en: Converting to 1D index is possible but less readable than tuple-based set.
  - label:
      ko: 경계에서 경계 'O' 찾기
      en: Detect boundary cells
    indent: 1
    options:
    - code: 'if( (r == 0 or c == 0 or r == rows - 1 or c == cols - 1) and board[r][c] == ''O''):'
      type: good
      why:
        ko: 모든 네 경계(top, bottom, left, right)를 확인하여 경계에 있는 'O' 셀부터 탐색을 시작합니다.
        en: Checks all four edges to identify boundary 'O' cells as starting points for unsurrounded regions.
    - code: 'if (r == 0 or r == rows - 1) and board[r][c] == ''O'':'
      type: distractor
      why:
        ko: 상하단 경계만 확인하고 좌우 경계를 놓칩니다.
        en: Only checks top/bottom edges; misses left/right boundary 'O's.
    - code: 'if (r == 0 and c == 0) and board[r][c] == ''O'':'
      type: distractor
      why:
        ko: 한 모서리만 확인하므로 다른 경계의 'O' 영역들을 포획하지 못합니다.
        en: Only checks one corner; misses unsurrounded regions on other edges.
  - label:
      ko: 포위된 'O' 셀 식별 및 변환
      en: Identify and capture surrounded regions
    indent: 2
    options:
    - code: 'if board[r][c] == ''O'' and (r, c) not in flag:'
      type: good
      why:
        ko: 경계 탐색에서 표시되지 않은 'O'는 경계와 연결되지 않은 포위된 영역입니다.
        en: Any 'O' not visited in boundary DFS is surrounded (not connected to any edge).
    - code: 'if board[r][c] == ''O'':'
      type: distractor
      why:
        ko: 경계에 연결된 'O'도 변환하여 잘못된 결과가 됩니다.
        en: Would flip ALL 'O's including unsurrounded ones on the boundary.
    - code: 'if (r, c) not in flag:'
      type: distractor
      why:
        ko: '''X'' 셀도 변환하여 보드가 손상됩니다.'
        en: Would flip all cells including 'X's that were never visited.
trace:
  code:
  - 'class Solution:'
  - '    def solve(self, board: List[List[str]]) -> None:'
  - '        rows, cols = len(board), len(board[0])'
  - '        flag = set()'
  - ''
  - '        def dfs(r, c):'
  - '            if not(r in range(rows) and c in range(cols)) or board[r][c] != ''O'' or (r, c) in flag:'
  - '                return'
  - '            flag.add((r, c))'
  - '            return (dfs(r + 1, c), dfs(r - 1, c), dfs(r, c + 1), dfs(r, c - 1))'
  - ''
  - '        # traverse through the board'
  - '        for r in range(rows):'
  - '            for c in range(cols):'
  - '                if( (r == 0 or c == 0 or r == rows - 1 or c == cols - 1) and board[r][c] == ''O''):'
  - '                    dfs(r, c)'
  - ''
  - '        # set all of the ''X''s to ''O''s'
  - '        for r in range(rows):'
  - '            for c in range(cols):'
  - '                if board[r][c] == ''O'' and (r, c) not in flag:'
  - '                    board[r][c] = ''X'''
  - ''
  - '    '''''''
  - '    def solve(self, board: List[List[str]]) -> None:'
  - '        ROWS, COLS = len(board), len(board[0])'
  - ''
  - '        def capture(r, c):'
  - '            if r < 0 or c < 0 or r == ROWS or c == COLS or board[r][c] != "O":'
  - '                return'
  - '            board[r][c] = "T"'
  - '            capture(r + 1, c)'
  - '            capture(r - 1, c)'
  - '            capture(r, c + 1)'
  - '            capture(r, c - 1)'
  - ''
  - '        # 1. (DFS) Capture unsurrounded regions (O -> T)'
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                if board[r][c] == "O" and (r in [0, ROWS - 1] or c in [0, COLS - 1]):'
  - '                    capture(r, c)'
  - ''
  - '        # 2. Capture surrounded regions (O -> X)'
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                if board[r][c] == "O":'
  - '                    board[r][c] = "X"'
  - ''
  - '        # 3. Uncapture unsurrounded regions (T -> O)'
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                if board[r][c] == "T":'
  - '                    board[r][c] = "O"'
  - '    '''''''
  cases:
  - input: '[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]'
    expected: '[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]'
  - input: '[["X"]]'
    expected: '[["X"]]'
  worked_example:
    input: '[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]'
    steps:
    - ko: '초기 설정: rows=4, cols=4, flag={} (공집합). 보드 순회를 준비합니다.'
      en: 'Setup: rows=4, cols=4, initialize flag={}. Prepare board traversal.'
    - ko: '경계 순회: 경계의 ''O'' 셀 (3,1)을 찾고, DFS(3,1) 호출. (3,1)은 상하좌우가 모두 ''X''이므로 flag={(3,1)}로 표시만 하고 재귀 종료.'
      en: 'Boundary DFS: Found boundary ''O'' at (3,1). DFS marks (3,1) in flag. Neighbors are all ''X'', so recursion stops. flag={(3,1)}'
    - ko: '내부 ''O'' 확인: 보드의 모든 ''O''를 순회: (1,1), (1,2), (2,2)는 flag에 없으므로 포위됨. (3,1)은 flag에 있으므로 유지.'
      en: 'Interior check: Traverse all cells. (1,1), (1,2), (2,2) are not in flag→surrounded. (3,1) is in flag→keep as ''O''.'
    - ko: '변환: (1,1)→''X'', (1,2)→''X'', (2,2)→''X''. 최종 결과: [[X,X,X,X],[X,X,X,X],[X,X,X,X],[X,O,X,X]]'
      en: 'Flip: Convert (1,1), (1,2), (2,2) to ''X''. Result: [[X,X,X,X],[X,X,X,X],[X,X,X,X],[X,O,X,X]]'
    answer: '[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]'
solution:
  code: "class Solution:\n    def solve(self, board: List[List[str]]) -> None:\n        rows, cols = len(board), len(board[0])\n        flag = set()\n\n        def dfs(r, c):\n            if not(r in range(rows) and c in range(cols)) or board[r][c] != 'O' or (r, c) in flag:\n                return\n            flag.add((r, c))\n            return (dfs(r + 1, c), dfs(r - 1, c), dfs(r, c + 1), dfs(r, c - 1))\n\n        # traverse through the board\n        for r in range(rows):\n            for c in range(cols):\n                if( (r == 0 or c == 0 or r == rows - 1 or c == cols - 1) and board[r][c] == 'O'):\n                    dfs(r, c)\n\n        # set all of the 'X's to 'O's\n        for r in range(rows):\n            for c in range(cols):\n                if board[r][c] == 'O' and (r, c) not in flag:\n                    board[r][c] = 'X'\n\n    '''\n    def solve(self, board: List[List[str]]) -> None:\n        ROWS, COLS = len(board), len(board[0])\n\n        def capture(r, c):\n  \
    \          if r < 0 or c < 0 or r == ROWS or c == COLS or board[r][c] != \"O\":\n                return\n            board[r][c] = \"T\"\n            capture(r + 1, c)\n            capture(r - 1, c)\n            capture(r, c + 1)\n            capture(r, c - 1)\n\n        # 1. (DFS) Capture unsurrounded regions (O -> T)\n        for r in range(ROWS):\n            for c in range(COLS):\n                if board[r][c] == \"O\" and (r in [0, ROWS - 1] or c in [0, COLS - 1]):\n                    capture(r, c)\n\n        # 2. Capture surrounded regions (O -> X)\n        for r in range(ROWS):\n            for c in range(COLS):\n                if board[r][c] == \"O\":\n                    board[r][c] = \"X\"\n\n        # 3. Uncapture unsurrounded regions (T -> O)\n        for r in range(ROWS):\n            for c in range(COLS):\n                if board[r][c] == \"T\":\n                    board[r][c] = \"O\"\n    '''\n"
  complexity:
    time: O(m·n)
    space: O(m·n)
  followup:
  - ko: 대각선 연결도 포함된다면 알고리즘을 어떻게 수정하겠습니까?
    en: How would you modify the solution if diagonal connections also counted?
  - ko: BFS(너비 우선 탐색)를 사용하여 구현하면 어떤 장점이 있습니까?
    en: What are the advantages of implementing this using BFS instead of DFS?
  - ko: Union-Find 자료 구조를 사용하여 이 문제를 해결할 수 있겠습니까?
    en: How would you solve this using a Union-Find (Disjoint Set Union) data structure?
```