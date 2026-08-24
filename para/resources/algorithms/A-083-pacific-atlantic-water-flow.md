---
created: '2026-08-10'
date: '2026-08-10'
day: Day 83
difficulty: medium
id: A-083
source:
  curated_in:
  - neetcode150
  number: 417
  platform: leetcode
  slug: pacific-atlantic-water-flow
  url: https://leetcode.com/problems/pacific-atlantic-water-flow/
tags:
- array
- depth-first-search
- breadth-first-search
- matrix
title:
  en: Pacific Atlantic Water Flow
  ko: 태평양과 대서양으로의 물의 흐름
today: false
type: algorithm
updated: '2026-08-10'
visible: true
---

# 태평양과 대서양으로의 물의 흐름

## Data

```yaml
problem:
  title:
    ko: 태평양과 대서양으로의 물의 흐름
    en: Pacific Atlantic Water Flow
  statement:
    ko: '태평양과 대서양에 인접한 m x n 크기의 직사각형 섬이 있습니다. 태평양은 섬의 왼쪽과 위쪽 경계에 접하고, 대서양은 섬의 오른쪽과 아래쪽 경계에 접합니다.


      섬은 정사각형 셀로 분할된 격자로 구성되어 있습니다. m x n 정수 행렬 heights가 주어지며, heights[r][c]는 좌표 (r, c)에 있는 셀의 해수면 위의 높이를 나타냅니다.


      섬은 많은 비를 받으며, 빗물은 현재 셀의 높이가 인접한 셀의 높이보다 크거나 같으면 북쪽, 남쪽, 동쪽, 서쪽의 인접한 셀로 흐를 수 있습니다. 물은 바다에 인접한 모든 셀에서 바다로 흘러갈 수 있습니다.


      강우수가 태평양과 대서양 모두로 흐를 수 있는 격자 좌표의 2D 리스트 result를 반환합니다. 여기서 result[i] = [r_i, c_i]는 셀 (r_i, c_i)에서 강우수가 태평양과 대서양 모두로 흐를 수 있음을 나타냅니다.'
    en: 'There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island''s left and top edges, and the Atlantic Ocean touches the island''s right and bottom edges.


      The island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).


      The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell''s height is less than or equal to the current cell''s height. Water can flow from any cell adjacent to an ocean into the ocean.


      Return a 2D list of grid coordinates result where result[i] = [r_i, c_i] denotes that rain water can flow from cell (r_i, c_i) to both the Pacific and Atlantic oceans.'
  constraints:
  - m == heights.length
  - n == heights[r].length
  - 1 ≤ m, n ≤ 200
  - 0 ≤ heights[r][c] ≤ 10^5
  io:
  - input: '[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]'
    output: '[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]'
  - input: '[[1]]'
    output: '[[0,0]]'
clarifying:
  items:
  - q:
      ko: 물은 현재 셀과 같은 높이의 인접 셀로 흐를 수 있나요?
      en: Can water flow to a neighboring cell with the same height as the current cell?
    type: good
    why:
      ko: 문제에서 '높이가 작거나 같다면'이라고 명시했으므로, 같은 높이의 셀로도 흐를 수 있습니다.
      en: The problem explicitly states 'if the neighboring cell's height is less than or equal to', so water can flow to equal-height neighbors.
  - q:
      ko: 바다에 인접한 셀이 자동으로 그 바다에 도달하나요?
      en: Does a cell adjacent to an ocean automatically reach that ocean?
    type: good
    why:
      ko: 문제에서 '바다에 인접한 셀에서 바다로 흐를 수 있다'고 했으므로, 경계 셀은 자동으로 인접 바다에 도달합니다.
      en: The problem states that water can flow from cells adjacent to an ocean into that ocean, so border cells automatically reach their adjacent ocean.
  - q:
      ko: 한 셀이 태평양과 대서양 모두에 도달할 수 있나요?
      en: Can a single cell reach both the Pacific and Atlantic oceans?
    type: good
    why:
      ko: 문제의 목표가 바로 이것입니다. 높은 중앙 지역의 셀들은 여러 방향으로 흘러 양쪽 바다에 도달할 수 있습니다.
      en: This is exactly what the problem asks us to find. High cells in the middle can flow in multiple directions to reach both oceans.
  - q:
      ko: 물은 대각선 방향(4개 방향 제외)으로 흐를 수 있나요?
      en: Can water flow diagonally (other than the 4 cardinal directions)?
    type: distractor
    why:
      ko: 문제에서 '북쪽, 남쪽, 동쪽, 서쪽'만 언급했으므로 대각선 흐름은 불가능합니다.
      en: The problem explicitly specifies only north, south, east, and west directions, not diagonals.
  - q:
      ko: 알고리즘이 바다 경계에서 시작하는 이유는 무엇인가요?
      en: Why does the algorithm start searches from the ocean borders?
    type: good
    why:
      ko: 역방향 탐색을 통해 각 바다에서 어떤 셀까지 도달할 수 있는지 찾는 것입니다. 경계에서 시작하여 올라가면서 모든 도달 가능한 셀을 표시합니다.
      en: 'We use reverse-flow search: starting from ocean borders, we explore backward (uphill) to find all cells that could flow to that ocean. This avoids checking every cell individually.'
  - q:
      ko: 물은 '낮은 셀에서 높은 셀로' 흐를 수 있나요?
      en: Can water flow from a lower cell to a higher cell (uphill)?
    type: distractor
    why:
      ko: 아니요, 물은 높이가 작거나 같은 곳으로만 흐릅니다. 알고리즘의 역방향 탐색은 이를 반영합니다.
      en: No, water flows only to cells with height ≤ current height. The reverse-flow search in the algorithm accounts for this.
  - q:
      ko: 같은 셀을 여러 번 방문할 수 있나요?
      en: Can we visit the same cell multiple times during the search?
    type: good
    why:
      ko: 아니요, visited 집합을 사용하여 각 셀을 최대 한 번만 방문하여 무한 루프를 방지합니다.
      en: No, we use a visited set to ensure each cell is processed at most once, preventing infinite loops.
approach:
  items:
  - name:
      ko: 바다 경계에서의 역방향 DFS
      en: Reverse-flow DFS from ocean borders
    complexity: O(m × n) time / O(m × n) space
    type: good
    why:
      ko: 각 바다의 경계에서 시작하여 도달 가능한 모든 셀을 표시합니다. 각 셀은 최대 한 번씩 방문되므로 효율적입니다. 두 집합의 교집합을 찾으면 답이 됩니다.
      en: Start DFS from each ocean's borders, marking all reachable cells by exploring uphill (in reverse flow direction). Each cell is visited at most once. The intersection of both reachable sets gives the answer.
  - name:
      ko: 바다 경계에서의 BFS
      en: BFS from ocean borders
    complexity: O(m × n) time / O(m × n) space
    type: good
    why:
      ko: DFS 대신 큐를 사용한 BFS로 동일한 역방향 탐색을 수행합니다. 반복적 접근으로 스택 오버플로우를 피할 수 있습니다.
      en: Same reverse-flow approach but using a queue instead of recursion. Avoids potential stack overflow on large grids.
  - name:
      ko: 각 셀에서의 순방향 DFS
      en: Forward DFS from each cell
    complexity: O(m² × n²) time / O(m × n) space
    type: distractor
    why:
      ko: 모든 셀에서 순방향으로 탐색하여 각각이 두 바다에 도달하는지 확인하는 방식입니다. 각 셀마다 전체 그리드를 탐색하므로 비효율적입니다.
      en: Check each cell by doing a forward flow search to see if it reaches both oceans. Inefficient because it requires exploring from every cell independently.
  - name:
      ko: 동적 프로그래밍 (모서리에서 중심으로)
      en: Dynamic programming (corners to center)
    complexity: O(m × n) time / O(m × n) space
    type: distractor
    why:
      ko: 모서리부터 시작하여 각 셀이 도달 가능한 바다를 저장하는 방식입니다. 올바르지만 구현이 복잡하고 직관적이지 않습니다.
      en: Build up from borders, storing which oceans each cell can reach. Correct but more complex to implement and less intuitive than the reverse-DFS approach.
logic:
  format: slot
  slots:
  - label:
      ko: 그리드 크기와 바다 도달 집합 초기화
      en: Initialize grid dimensions and ocean reachability sets
    indent: 0
    options:
    - code: ROWS, COLS = len(heights), len(heights[0])
      type: good
      why:
        ko: 그리드의 행과 열 수를 저장하고, 각 바다에 도달 가능한 셀을 추적할 두 집합을 생성합니다.
        en: Store grid bounds and create sets to track cells reachable to each ocean. Sets provide O(1) lookup and prevent duplicates.
    - code: ROWS, COLS = len(heights[0]), len(heights)
      type: distractor
      why:
        ko: 행과 열을 뒤바꾼 것입니다. 올바른 순서는 ROWS (높이의 길이)와 COLS (높이[0]의 길이)입니다.
        en: Dimensions are swapped. Correct order is ROWS (length of heights) and COLS (length of heights[0]).
    - code: pac, atl = list(), list()
      type: distractor
      why:
        ko: 리스트를 사용하면 O(n) 시간의 멤버십 테스트가 필요합니다. 집합은 O(1) 조회를 제공합니다.
        en: Lists require O(n) membership testing. Sets provide O(1) lookup for checking if a cell is already visited.
    - code: pac, atl = dict(), dict()
      type: distractor
      why:
        ko: 딕셔너리는 다른 자료구조이며, 여기서는 필요한 key-value 매핑이 없습니다.
        en: Dict requires key-value pairs which are unnecessary. We only need to track presence/absence of cells.
  - label:
      ko: 역방향 흐름 DFS 함수 정의
      en: Define reverse-flow DFS function
    indent: 0
    options:
    - code: 'def dfs(r, c, visit, prevHeight):'
      type: good
      why:
        ko: DFS는 현재 위치(r, c), 방문 집합, 그리고 이전 높이를 매개변수로 받습니다. 이전 높이는 흐름 가능 조건을 확인하기 위해 필요합니다.
        en: The DFS needs position (r,c), visited set to track explored cells, and prevHeight to check if flow to this cell is possible in reverse.
    - code: 'def dfs(r, c, visit):'
      type: distractor
      why:
        ko: prevHeight 매개변수가 없으면 흐름 가능 조건을 확인할 수 없습니다.
        en: Missing prevHeight parameter makes it impossible to check the height constraint for valid flow.
    - code: 'def dfs(r, c, prevHeight):'
      type: distractor
      why:
        ko: visit 집합이 없으면 이미 방문한 셀을 추적할 수 없어 무한 루프에 빠집니다.
        en: Without the visited set, we can't track explored cells and will loop infinitely.
    - code: 'def dfs(r, c, visit, currHeight):'
      type: distractor
      why:
        ko: 매개변수 이름을 currHeight로 하면 혼동을 초래합니다. prevHeight는 이전 셀의 높이를 의미합니다.
        en: Naming it currHeight is confusing. prevHeight represents the previous cell's height to compare against.
  - label:
      ko: 경계, 방문, 높이 조건 검증
      en: Validate cell position, visit status, and height constraint
    indent: 1
    options:
    - code: if (
      type: good
      why:
        ko: '기저 사례를 확인합니다: 그리드 밖, 이미 방문함, 또는 높이가 너무 낮음(역방향에서 ''낮다''는 것은 흐름이 불가능함을 의미).'
        en: 'Base case checks: out of bounds, already visited, or height is too low for reverse flow. If any condition is true, backtrack.'
    - code: 'if (r, c) in visit or r < 0 or c < 0 or heights[r][c] > prevHeight:'
      type: distractor
      why:
        ko: 높이 비교를 '>'로 하면 거꾸로 됩니다. 역방향에서는 높이가 같거나 크면 진행해야 합니다.
        en: Using > instead of < inverts the logic. In reverse flow, we continue if height >= prevHeight.
    - code: 'if ((r, c) in visit) and (r < 0) and (c < 0) and heights[r][c] < prevHeight:'
      type: distractor
      why:
        ko: 모든 조건을 AND로 연결하면 매우 드문 경우에만 종료됩니다. 하나라도 참이면 종료해야 합니다.
        en: Using AND requires all conditions to be true, but we should stop if ANY condition is true (OR logic).
    - code: 'if r == ROWS or c == COLS or r < 0 or c < 0:'
      type: distractor
      why:
        ko: 경계 확인만 하고 방문 및 높이 조건을 놓쳤습니다. 모든 세 조건이 필요합니다.
        en: Only checks bounds but misses visited set and height constraint. All three conditions are necessary.
  - label:
      ko: 셀을 방문으로 표시하고 4개 인접 셀 탐색
      en: Mark cell visited and recursively explore 4 neighbors
    indent: 1
    options:
    - code: visit.add((r, c))
      type: good
      why:
        ko: 현재 셀을 방문 집합에 추가한 후, 4개 방향(위, 아래, 좌, 우)의 인접 셀을 재귀적으로 탐색합니다.
        en: Add current cell to visited set, then recursively explore all 4 adjacent cells. Each recursive call passes the current cell's height as prevHeight.
    - code: visit.append((r, c))
      type: distractor
      why:
        ko: 집합의 .append() 메서드는 없습니다. set은 .add()를 사용합니다.
        en: Sets don't have .append() method. Use .add() for sets (lists use .append()).
    - code: 'if (r, c) not in visit: visit.add((r, c))'
      type: distractor
      why:
        ko: 이미 기저 사례에서 방문을 확인했으므로 추가 확인은 불필요합니다.
        en: Already checked in base case, so this redundant check wastes time.
    - code: visit.add((r, c)); return
      type: distractor
      why:
        ko: 마킹 후 재귀 호출을 하지 않으면, 이웃 셀들을 탐색하지 못합니다.
        en: Without the recursive calls to neighbors, we won't explore the full reachable set.
  - label:
      ko: 태평양 경계에서 DFS 시작 (위쪽 및 왼쪽 모서리)
      en: Start DFS from Pacific borders (top and left edges)
    indent: 0
    options:
    - code: 'for c in range(COLS):'
      type: good
      why:
        ko: 위쪽 행(row 0)의 모든 셀과 왼쪽 열(col 0)의 모든 셀에서 시작하여, 태평양에 도달 가능한 모든 셀을 표시합니다.
        en: Iterate through top row (row 0) and left column (col 0), starting DFS from each border cell to mark all Pacific-reachable cells.
    - code: dfs(ROWS - 1, c, pac, heights[ROWS - 1][c])
      type: distractor
      why:
        ko: ROWS - 1은 아래쪽 모서리입니다. 태평양은 위쪽과 왼쪽입니다.
        en: ROWS - 1 is the bottom edge (Atlantic). Pacific is at top (row 0) and left (col 0).
    - code: dfs(0, c, atl, heights[0][c])
      type: distractor
      why:
        ko: atl 집합을 사용하고 있습니다. 태평양은 pac 집합에 저장해야 합니다.
        en: Using atl set instead of pac. This would store in the wrong ocean's set.
    - code: 'for c in range(COLS): dfs(0, c, pac, heights[0][c])'
      type: distractor
      why:
        ko: 왼쪽 열 탐색이 빠졌습니다. 완전한 태평양 경계를 커버해야 합니다.
        en: Only covers top row, missing left column. Need both for complete Pacific border.
  - label:
      ko: 대서양 경계에서 DFS 시작 (아래쪽 및 오른쪽 모서리)
      en: Start DFS from Atlantic borders (bottom and right edges)
    indent: 0
    options:
    - code: dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])
      type: good
      why:
        ko: 아래쪽 행(row ROWS-1)의 모든 셀과 오른쪽 열(col COLS-1)의 모든 셀에서 시작하여, 대서양에 도달 가능한 모든 셀을 표시합니다.
        en: Iterate through bottom row (row ROWS-1) and right column (col COLS-1), starting DFS from each border cell to mark all Atlantic-reachable cells.
    - code: dfs(0, c, atl, heights[0][c])
      type: distractor
      why:
        ko: row 0은 태평양 경계입니다. 대서양은 아래쪽(ROWS-1)과 오른쪽(COLS-1)입니다.
        en: Row 0 is Pacific. Atlantic is at bottom (ROWS-1) and right (COLS-1).
    - code: dfs(r, 0, atl, heights[r][0])
      type: distractor
      why:
        ko: col 0은 태평양 경계입니다. 대서양 경계는 col COLS-1입니다.
        en: Col 0 is Pacific border. Atlantic is at col COLS-1.
    - code: dfs(ROWS - 1, c, pac, heights[ROWS - 1][c])
      type: distractor
      why:
        ko: pac 집합을 사용하고 있습니다. 이 경계는 atl 집합에 저장해야 합니다.
        en: Using pac set for Atlantic. Should use atl for Atlantic borders.
  - label:
      ko: 양쪽 바다에 모두 도달 가능한 셀 수집
      en: Collect cells that reach both oceans
    indent: 0
    options:
    - code: 'if (r, c) in pac and (r, c) in atl:'
      type: good
      why:
        ko: 모든 셀을 순회하며, 태평양 집합과 대서양 집합 모두에 속한 셀을 결과에 추가합니다. 이 셀들이 답입니다.
        en: Iterate all cells and add to result if present in both pac and atl sets. These cells can flow to both oceans.
    - code: 'if (r, c) in pac or (r, c) in atl:'
      type: distractor
      why:
        ko: OR 연산자를 사용하면 한쪽 바다에만 도달하는 셀도 포함됩니다. 양쪽 모두에 도달해야 합니다.
        en: Using OR would include cells reachable to only one ocean. We need cells reachable to BOTH.
    - code: 'if (r, c) in pac and (r, c) not in atl:'
      type: distractor
      why:
        ko: 이것은 태평양에만 도달하는 셀을 선택합니다. 양쪽 모두에 도달해야 합니다.
        en: This selects only Pacific-reachable cells. We need cells in both sets.
    - code: 'if pac.intersection(atl):'
      type: distractor
      why:
        ko: 이것은 전체 교집합을 확인하는 것입니다. 각 셀 개별적으로 확인해야 합니다.
        en: This checks the entire intersection once. We need to check each cell individually.
trace:
  code:
  - 'class Solution:'
  - '    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:'
  - '        ROWS, COLS = len(heights), len(heights[0])'
  - '        pac, atl = set(), set()'
  - ''
  - '        def dfs(r, c, visit, prevHeight):'
  - '            if ('
  - '                (r, c) in visit'
  - '                or r < 0'
  - '                or c < 0'
  - '                or r == ROWS'
  - '                or c == COLS'
  - '                or heights[r][c] < prevHeight'
  - '            ):'
  - '                return'
  - '            visit.add((r, c))'
  - '            dfs(r + 1, c, visit, heights[r][c])'
  - '            dfs(r - 1, c, visit, heights[r][c])'
  - '            dfs(r, c + 1, visit, heights[r][c])'
  - '            dfs(r, c - 1, visit, heights[r][c])'
  - ''
  - '        for c in range(COLS):'
  - '            dfs(0, c, pac, heights[0][c])'
  - '            dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])'
  - ''
  - '        for r in range(ROWS):'
  - '            dfs(r, 0, pac, heights[r][0])'
  - '            dfs(r, COLS - 1, atl, heights[r][COLS - 1])'
  - ''
  - '        res = []'
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                if (r, c) in pac and (r, c) in atl:'
  - '                    res.append([r, c])'
  - '        return res'
  cases:
  - input: '[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]'
    expected: '[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]'
  - input: '[[1]]'
    expected: '[[0,0]]'
  worked_example:
    input: '[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]'
    steps:
    - ko: '초기화: ROWS=5, COLS=5, pac={}, atl={}'
      en: 'Initialize: ROWS=5, COLS=5, pac={}, atl={}'
    - ko: 태평양 경계(위쪽 행과 왼쪽 열)에서 시작하는 DFS로 각 높이로부터 도달 가능한 더 높은 또는 같은 높이의 셀을 탐색하고 pac에 표시합니다.
      en: Run DFS from Pacific borders (top row and left column), exploring backward to higher-or-equal cells, marking all reachable cells in pac set.
    - ko: 대서양 경계(아래쪽 행과 오른쪽 열)에서 시작하는 DFS로 각 높이로부터 도달 가능한 더 높은 또는 같은 높이의 셀을 탐색하고 atl에 표시합니다.
      en: Run DFS from Atlantic borders (bottom row and right column), exploring backward to higher-or-equal cells, marking all reachable cells in atl set.
    - ko: pac과 atl의 교집합에 속한 셀들 [0,4], [1,3], [1,4], [2,2], [3,0], [3,1], [4,0]을 결과에 추가합니다.
      en: Collect cells present in both pac and atl sets and return as result.
    answer: '[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]'
solution:
  code: "class Solution:\n    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:\n        ROWS, COLS = len(heights), len(heights[0])\n        pac, atl = set(), set()\n\n        def dfs(r, c, visit, prevHeight):\n            if (\n                (r, c) in visit\n                or r < 0\n                or c < 0\n                or r == ROWS\n                or c == COLS\n                or heights[r][c] < prevHeight\n            ):\n                return\n            visit.add((r, c))\n            dfs(r + 1, c, visit, heights[r][c])\n            dfs(r - 1, c, visit, heights[r][c])\n            dfs(r, c + 1, visit, heights[r][c])\n            dfs(r, c - 1, visit, heights[r][c])\n\n        for c in range(COLS):\n            dfs(0, c, pac, heights[0][c])\n            dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])\n\n        for r in range(ROWS):\n            dfs(r, 0, pac, heights[r][0])\n            dfs(r, COLS - 1, atl, heights[r][COLS - 1])\n\n        res = []\n     \
    \   for r in range(ROWS):\n            for c in range(COLS):\n                if (r, c) in pac and (r, c) in atl:\n                    res.append([r, c])\n        return res\n"
  complexity:
    time: O(m × n)
    space: O(m × n)
  followup:
  - ko: 이 알고리즘을 BFS로 구현할 수 있나요? 시간 복잡도는 같을까요?
    en: Can you implement this algorithm using BFS instead of DFS? Would the time complexity be the same?
  - ko: 물이 대각선으로도 흐를 수 있다면 어떻게 변경되나요?
    en: How would the solution change if water could flow diagonally (8 directions instead of 4)?
  - ko: 결과 좌표만 필요하지 않고 개수만 필요하다면 어떻게 최적화할 수 있나요?
    en: How would you optimize the solution if you only need the count of cells, not their coordinates?
```