---
created: '2026-08-09'
date: '2026-08-09'
day: Day 82
difficulty: medium
id: A-082
source:
  curated_in:
  - neetcode150
  number: 695
  platform: leetcode
  slug: max-area-of-island
  url: https://leetcode.com/problems/max-area-of-island/
status: draft
tags:
- array
- depth-first-search
- breadth-first-search
- union-find
- matrix
title:
  en: Max Area of Island
  ko: 섬의 최대 넓이
today: true
type: algorithm
updated: '2026-08-09'
visible: true
---

# 섬의 최대 넓이

## Data

```yaml
problem:
  title:
    ko: 섬의 최대 넓이
    en: Max Area of Island
  statement:
    ko: 'm x n 크기의 이진 행렬 grid가 주어집니다. 섬은 1(육지)들로 이루어진 그룹으로, 4방향(상하좌우)으로 연결되어 있습니다. 모든 모서리는 물로 둘러싸여 있다고 가정할 수 있습니다.


      섬의 넓이는 섬에 속한 값 1인 셀의 개수입니다.


      grid에서 섬의 최대 넓이를 반환합니다. 섬이 없으면 0을 반환합니다.'
    en: 'You are given an m x n binary matrix grid. An island is a group of 1''s (representing land) connected 4-directionally (horizontal or vertical). You may assume all four edges of the grid are surrounded by water.


      The area of an island is the number of cells with a value 1 in the island.


      Return the maximum area of an island in grid. If there is no island, return 0.'
  constraints:
  - m == grid.length
  - n == grid[i].length
  - 1 ≤ m, n ≤ 50
  - grid[i][j] is either 0 or 1
  io:
  - input: '[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]'
    output: '6'
  - input: '[[0,0,0,0,0,0,0,0]]'
    output: '0'
clarifying:
  items:
  - q:
      ko: '"4방향 연결"은 정확히 무엇을 의미하나요?'
      en: What does "4-directional connection" mean exactly?
    type: good
    why:
      ko: 상하좌우 이웃만 연결된 것으로 간주하고, 대각선 연결은 포함하지 않습니다.
      en: Only up, down, left, right neighbors count as connected. Diagonal connections are not allowed.
  - q:
      ko: 여러 섬이 있을 때는 어떻게 하나요?
      en: What if there are multiple islands in the grid?
    type: good
    why:
      ko: 각 섬의 넓이를 계산하고 그 중 최댓값만 반환합니다.
      en: Calculate the area of each island independently and return only the maximum.
  - q:
      ko: 방문한 셀을 추적해야 하는 이유는 무엇인가요?
      en: Why do we need to track visited cells?
    type: good
    why:
      ko: 같은 셀을 여러 번 방문하면 넓이가 중복되어 계산되므로, 방문 표시로 각 셀을 한 번만 센다.
      en: Without tracking, the same cell would be counted multiple times from different recursion paths.
  - q:
      ko: 그리드를 직접 수정할 수 있나요?
      en: Can we modify the grid in-place instead of using a separate visited set?
    type: distractor
    why:
      ko: 기술적으로 가능하지만, 인터뷰에서 명시적으로 허용되지 않으면 입력을 수정하지 않는 것이 관례입니다.
      en: Technically possible, but modifying input is considered poor practice unless explicitly allowed.
  - q:
      ko: 빈 그리드(크기 0)을 처리해야 하나요?
      en: Do we need to handle edge cases like empty grids or single-cell grids?
    type: distractor
    why:
      ko: 제약 조건에서 1 ≤ m, n ≤ 50이므로 빈 그리드는 불가능합니다. 싱글 셀은 자동으로 처리됩니다.
      en: Constraints guarantee m, n ≥ 1, so empty grids are impossible. Single-cell cases work naturally.
  - q:
      ko: 대각선(8방향)도 연결로 간주해야 하나요?
      en: Should diagonal connections count as part of the same island?
    type: distractor
    why:
      ko: 문제에서 명확히 4방향만 연결된다고 명시했으므로, 대각선은 무시합니다.
      en: The problem explicitly states 4-directional connectivity; diagonals are not neighbors.
approach:
  items:
  - name:
      ko: 깊이 우선 탐색(DFS) + 방문 집합
      en: Depth-First Search (DFS) with Visited Set
    complexity: O(m*n) time / O(m*n) space
    type: good
    why:
      ko: 각 셀을 정확히 한 번 방문합니다. 방문 집합과 재귀 스택이 O(m*n) 공간을 사용합니다. 직관적이고 구현이 간단합니다.
      en: Each cell visited exactly once. Space for visited set and recursion stack. Intuitive and straightforward.
  - name:
      ko: 너비 우선 탐색(BFS) + 방문 집합
      en: Breadth-First Search (BFS) with Visited Set
    complexity: O(m*n) time / O(m*n) space
    type: good
    why:
      ko: DFS와 같은 복잡도이지만, 큐를 사용하여 반복적으로 구현합니다. 깊은 재귀로 인한 스택 오버플로우를 피할 수 있습니다.
      en: Same complexity as DFS but iterative using a queue. Avoids potential stack overflow on large islands.
  - name:
      ko: Union-Find (Disjoint Set Union)
      en: Union-Find (Disjoint Set Union)
    complexity: O(m*n*α(m*n)) time / O(m*n) space
    type: distractor
    why:
      ko: 이 문제에는 필요 이상으로 복잡합니다. 연결 성분 찾은 후 별도로 넓이를 계산해야 하므로 비효율적입니다.
      en: Overkill for this problem. Requires an additional pass to compute areas, making it unnecessarily complex.
  - name:
      ko: 모든 가능한 직사각형 검사
      en: 'Brute Force: Check All Possible Rectangles'
    complexity: O((m*n)²) or worse time / O(1) space
    type: distractor
    why:
      ko: 모든 직사각형 쌍을 확인하는 것은 극도로 비효율적이고, 불규칙한 섬 모양을 올바르게 처리할 수 없습니다.
      en: Extremely inefficient and cannot handle irregular island shapes that don't form rectangles.
  - name:
      ko: 방문 추적 없는 단일 패스
      en: Single Pass Without Visited Tracking
    complexity: O(m*n) time / O(1) space
    type: distractor
    why:
      ko: 방문 추적이 없으면 같은 셀을 다른 경로에서 여러 번 세게 되어 잘못된 결과가 나옵니다.
      en: Without visited tracking, cells get counted multiple times from different paths, producing wrong results.
logic:
  format: slot
  slots:
  - label:
      ko: 그리드 크기 초기화
      en: Initialize Grid Dimensions
    indent: 0
    options:
    - code: ROWS, COLS = len(grid), len(grid[0])
      type: good
      why:
        ko: 행과 열의 개수를 미리 저장하면 DFS에서 경계 확인을 효율적으로 할 수 있습니다.
        en: Pre-computing dimensions enables constant-time boundary checking throughout the DFS traversal.
    - code: ROWS = len(grid[0])
      type: distractor
      why:
        ko: grid[0]의 길이는 첫 번째 행의 크기로 열의 개수이지, 행의 개수가 아닙니다.
        en: grid[0] gives the number of columns in the first row, not the number of rows.
    - code: ROWS, COLS = len(grid), len(grid)
      type: distractor
      why:
        ko: 두 번째 len(grid)는 행의 개수를 다시 반환합니다. COLS는 grid[0]의 길이여야 합니다.
        en: The second len(grid) returns rows again. COLS should be len(grid[0]) for the column count.
  - label:
      ko: 방문 셀 추적용 집합 초기화
      en: Initialize Visited Set
    indent: 0
    options:
    - code: visit = set()
      type: good
      why:
        ko: 빠른 O(1) 조회로 방문 여부를 확인하고, 중복 방문을 방지합니다.
        en: A set provides O(1) membership checking, preventing cells from being counted multiple times.
    - code: visit = []
      type: distractor
      why:
        ko: 리스트는 in 연산이 O(n)이므로 성능이 떨어집니다. 집합을 사용하면 O(1)입니다.
        en: List membership checking is O(n). Set lookup is O(1), which is necessary for efficiency.
    - code: visit = {}
      type: distractor
      why:
        ko: 딕셔너리를 사용할 필요가 없습니다. 단순히 방문 여부만 기록하면 되므로 집합이 충분합니다.
        en: A dictionary is unnecessary—we only need to track whether a cell is visited, not associated values.
  - label:
      ko: 'DFS 함수: 경계 및 유효성 확인'
      en: 'DFS Function: Boundary and Validity Checks'
    indent: 1
    options:
    - code: if (
      type: good
      why:
        ko: 경계 밖, 물(0), 또는 이미 방문한 셀은 탐색할 수 없으므로 0을 반환합니다. 이를 통해 무한 재귀를 방지합니다.
        en: Out-of-bounds, water (0), and visited cells contribute 0 and stop recursion. Prevents infinite loops.
    - code: 'if r < 0 or r <= ROWS or c < 0 or c <= COLS:'
      type: distractor
      why:
        ko: r <= ROWS는 잘못되었습니다. 유효한 행 인덱스는 0부터 ROWS-1까지이므로 r == ROWS이거나 r >= ROWS일 때 경계를 벗어난 것입니다.
        en: Using r <= ROWS is wrong. Valid indices are 0 to ROWS-1, so check r == ROWS or r >= ROWS.
    - code: 'if r < 0 or r == ROWS or c < 0 or c == COLS:'
      type: distractor
      why:
        ko: grid[r][c] == 0 조건이 없으면 물(0)을 육지(1)처럼 처리하여 잘못된 섬 경계를 탐색합니다.
        en: Missing the grid[r][c] == 0 check means water cells are incorrectly treated as land.
  - label:
      ko: 현재 셀을 방문 집합에 추가
      en: Mark Current Cell as Visited
    indent: 1
    options:
    - code: visit.add((r, c))
      type: good
      why:
        ko: 셀을 방문 집합에 추가하면 다른 경로에서 재귀적으로 접근할 때 중복 방문을 막습니다.
        en: Adding to the visited set ensures the cell won't be reprocessed from other recursive paths.
    - code: visit.remove((r, c))
      type: distractor
      why:
        ko: 집합에서 제거하면 중복 계산이 발생합니다. 추가해야 합니다.
        en: Removing instead of adding would allow cells to be counted multiple times.
    - code: 'if (r, c) not in visit: visit.add((r, c))'
      type: distractor
      why:
        ko: 경계 검사에서 이미 (r, c) in visit을 확인했으므로 여기서 다시 조건 검사는 중복입니다.
        en: Redundant—the boundary check already filters out visited cells, so the if is unnecessary.
  - label:
      ko: 4방향 재귀 탐색 및 넓이 누적
      en: Recursively Explore 4 Neighbors and Accumulate Area
    indent: 1
    options:
    - code: return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
      type: good
      why:
        ko: 현재 셀(1)에 4방향 이웃 탐색의 합을 더하여 연결된 섬의 총 넓이를 계산합니다.
        en: Returns 1 for the current cell plus the sum of areas from all four neighbors' DFS calls.
    - code: return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1)
      type: distractor
      why:
        ko: 오른쪽(r, c + 1)은 있지만 왼쪽(r, c - 1)이 없습니다. 4방향을 모두 확인해야 합니다.
        en: 'Missing one direction. Must check all four neighbors: up, down, left, right.'
    - code: return max(1, dfs(r + 1, c), dfs(r - 1, c), dfs(r, c + 1), dfs(r, c - 1))
      type: distractor
      why:
        ko: 최댓값을 구하면 넓이를 잘못 계산합니다. 연결된 모든 셀을 합산해야 합니다.
        en: Taking max instead of sum would return the largest single neighbor, not the total area.
  - label:
      ko: 모든 셀을 시작점으로 DFS 시도
      en: Iterate Through All Cells as Potential Starting Points
    indent: 0
    options:
    - code: 'for r in range(ROWS):'
      type: good
      why:
        ko: 모든 셀을 시작점으로 DFS를 호출하면, 모든 섬을 탐색할 수 있습니다. 이미 방문한 셀은 자동으로 0을 반환합니다.
        en: Iterating from every cell ensures all islands are explored. Already-visited cells return 0 automatically.
    - code: "for r in range(1, ROWS):\n    for c in range(1, COLS):"
      type: distractor
      why:
        ko: range(1, ROWS)는 첫 번째 행을 건너뜁니다. range(ROWS)로 모든 행을 포함해야 합니다.
        en: Starting from 1 skips the first row and column, potentially missing island cells at the edges.
    - code: "for r in ROWS:\n    for c in COLS:"
      type: distractor
      why:
        ko: ROWS와 COLS는 정수이므로 직접 반복할 수 없습니다. range(ROWS)와 range(COLS)를 사용해야 합니다.
        en: ROWS and COLS are integers, not iterables. Must use range(ROWS) and range(COLS).
  - label:
      ko: 최댓값 추적 및 반환
      en: Track Maximum Area and Return Result
    indent: 2
    options:
    - code: area = max(area, dfs(r, c))
      type: good
      why:
        ko: 각 DFS 호출에서 반환된 넓이와 현재까지의 최댓값을 비교하여 유지합니다. 루프 후 최댓값을 반환합니다.
        en: The max() function updates the running maximum. After all iterations, return the largest area found.
    - code: area = dfs(r, c)
      type: distractor
      why:
        ko: 이렇게 하면 마지막 셀의 넓이만 반환합니다. 모든 셀을 확인한 후 최댓값을 유지해야 합니다.
        en: This overwrites area every iteration, so only the last cell's area is returned.
    - code: area += dfs(r, c)
      type: distractor
      why:
        ko: 모든 섬의 넓이를 합산하면 중복 계산되어 전체 합이 나옵니다. 최댓값만 필요합니다.
        en: Summing all areas gives the total land count, not the maximum island area.
trace:
  code:
  - 'class Solution:'
  - '    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:'
  - '        ROWS, COLS = len(grid), len(grid[0])'
  - '        visit = set()'
  - ''
  - '        def dfs(r, c):'
  - '            if ('
  - '                r < 0'
  - '                or r == ROWS'
  - '                or c < 0'
  - '                or c == COLS'
  - '                or grid[r][c] == 0'
  - '                or (r, c) in visit'
  - '            ):'
  - '                return 0'
  - '            visit.add((r, c))'
  - '            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)'
  - ''
  - '        area = 0'
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                area = max(area, dfs(r, c))'
  - '        return area'
  cases:
  - input: '[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]'
    expected: '6'
  - input: '[[0,0,0,0,0,0,0,0]]'
    expected: '0'
  worked_example:
    input: '[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]'
    steps:
    - ko: '초기화: ROWS=8, COLS=13, visit=공집합. 모든 (r,c)에 대해 dfs(r,c) 호출을 시작합니다.'
      en: 'Initialize: ROWS=8, COLS=13, visit={}. Begin calling dfs(r,c) for each cell.'
    - ko: 0인 셀들은 즉시 0을 반환하고, 1인 셀에 처음 도달하면 DFS로 연결된 섬 전체를 탐색합니다.
      en: Water cells (0) return 0 immediately. When landing on an unvisited 1, DFS explores the entire connected island.
    - ko: '행 3-5, 열 8-10 근처의 섬을 탐색할 때: (3,8) → (4,8) → (4,9) → (4,10) → (5,10), 그리고 (3,10)을 방문하여 총 6개 셀을 세고 넓이=6을 반환합니다.'
      en: The largest island connects (3,8)→(4,8)→(4,9)→(4,10)→(5,10)→(3,10), yielding area=6.
    - ko: 다른 모든 섬들(왼쪽의 5개 셀, 아래의 5개 셀 등)은 각각 최대 5개 이하의 셀을 가집니다. 따라서 최댓값은 6입니다.
      en: All other islands have at most 5 cells, so the maximum area is 6.
    answer: '6'
solution:
  code: "class Solution:\n    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:\n        ROWS, COLS = len(grid), len(grid[0])\n        visit = set()\n\n        def dfs(r, c):\n            if (\n                r < 0\n                or r == ROWS\n                or c < 0\n                or c == COLS\n                or grid[r][c] == 0\n                or (r, c) in visit\n            ):\n                return 0\n            visit.add((r, c))\n            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)\n\n        area = 0\n        for r in range(ROWS):\n            for c in range(COLS):\n                area = max(area, dfs(r, c))\n        return area\n"
  complexity:
    time: O(m*n)
    space: O(m*n)
  followup:
  - ko: 추가 메모리 없이 풀 수 있을까요? (그리드를 직접 수정하여 방문한 셀을 표시)
    en: How would you solve this using O(1) extra space by modifying the grid in-place?
  - ko: BFS를 사용하여 어떻게 풀 수 있을까요?
    en: How would you implement this using BFS instead of DFS?
  - ko: 그리드가 매우 크면, Union-Find를 사용하는 것이 더 효율적일까요?
    en: When would Union-Find be preferable over DFS/BFS for this problem?
```