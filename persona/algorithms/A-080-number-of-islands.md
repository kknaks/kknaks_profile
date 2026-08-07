---
created: '2026-08-07'
date: '2026-08-07'
day: Day 80
difficulty: medium
id: A-080
source:
  curated_in:
  - neetcode150
  number: 200
  platform: leetcode
  slug: number-of-islands
  url: https://leetcode.com/problems/number-of-islands/
status: draft
tags:
- array
- depth-first-search
- breadth-first-search
- union-find
- matrix
title:
  en: Number of Islands
  ko: 섬의 개수
today: true
type: algorithm
updated: '2026-08-07'
visible: true
---

# 섬의 개수

## Data

```yaml
problem:
  title:
    ko: 섬의 개수
    en: Number of Islands
  statement:
    ko: 'm × n 크기의 2D 이진 그리드가 주어집니다. 이 그리드에서 ''1''은 땅, ''0''은 물을 나타냅니다. 섬의 개수를 반환하세요.


      섬은 물로 둘러싸여 있으며 인접한 땅들이 수평 또는 수직으로 연결되어 있습니다. 그리드의 모든 네 모서리는 물로 둘러싸여 있다고 가정할 수 있습니다.'
    en: 'Given an m x n 2D binary grid which represents a map of ''1''s (land) and ''0''s (water), return the number of islands.


      An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.'
  constraints:
  - 1 ≤ m, n ≤ 300
  - grid[i][j] ∈ {'0', '1'}
  - m == grid.length, n == grid[i].length
  io:
  - input: '[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]'
    output: '1'
  - input: '[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]'
    output: '3'
clarifying:
  items:
  - q:
      ko: 인접한 셀은 무엇을 포함하나요?
      en: What counts as adjacent cells?
    type: good
    why:
      ko: 섬의 정의가 '수평 또는 수직으로 연결'이므로, 대각선 연결은 포함되지 않으며 4방향(위, 아래, 좌, 우) 인접만 고려합니다.
      en: The problem states islands are formed by 'horizontal or vertical' connections, so only 4-directional adjacency (up, down, left, right) counts—diagonals do not.
  - q:
      ko: 입력 그리드를 수정할 수 있나요?
      en: Can I modify the input grid to mark visited cells?
    type: good
    why:
      ko: 네, 방문한 셀을 '0'으로 변경하여 별도 방문 집합을 사용하지 않을 수 있습니다. 또는 별도의 visited 세트를 사용해도 됩니다.
      en: Yes, you can modify the grid in-place to save space, or use a separate visited set for clarity. Both approaches are valid.
  - q:
      ko: null이거나 빈 그리드를 어떻게 처리하나요?
      en: How should I handle null or empty grid?
    type: good
    why:
      ko: 제약 조건에서 1 ≤ m, n이므로 공식적으로 빈 그리드는 없지만, 엣지 케이스로 0을 반환해야 합니다.
      en: While the constraints guarantee m, n ≥ 1, it's good practice to handle null/empty cases early and return 0.
  - q:
      ko: 대각선으로 연결된 땅도 같은 섬으로 계산하나요?
      en: Do diagonally adjacent land cells belong to the same island?
    type: distractor
    why:
      ko: 아니요, 문제에서 '수평 또는 수직으로 연결'이라고 명시되어 있으므로 대각선 연결은 무시합니다.
      en: No, the problem explicitly states 'horizontally or vertically', so diagonal connections are not considered.
  - q:
      ko: 물(0)의 개수를 세어야 하나요?
      en: Should I count water ('0') regions as islands?
    type: distractor
    why:
      ko: 아니요, 섬은 '1'(땅)의 연결된 영역입니다. 물은 섬이 아닙니다.
      en: No, islands are formed only by connected land cells ('1'). Water regions are not islands.
approach:
  items:
  - name:
      ko: 깊이 우선 탐색 (DFS + 방문 집합)
      en: Depth-First Search (DFS with visited set)
    complexity: O(m × n) time / O(m × n) space
    type: good
    why:
      ko: 각 셀을 한 번씩 방문하고, 방문한 셀을 집합에 기록합니다. 재귀 구조가 직관적이고 구현이 간단합니다.
      en: Visit each cell once and track visited cells in a set. Intuitive recursive structure with straightforward implementation.
  - name:
      ko: 너비 우선 탐색 (BFS + 큐)
      en: Breadth-First Search (BFS with queue)
    complexity: O(m × n) time / O(m × n) space
    type: good
    why:
      ko: DFS 대신 큐를 사용하여 반복적으로 섬을 탐색합니다. 재귀 깊이 제한 문제를 피할 수 있고, 같은 시간/공간 복잡도를 가집니다.
      en: Use a queue for iterative traversal. Avoids potential stack overflow with very large grids, with identical time/space complexity.
  - name:
      ko: 나이브한 카운팅 (모든 '1' 개수 세기)
      en: Naive cell counting (count all '1's)
    complexity: O(m × n) time / O(1) space
    type: distractor
    why:
      ko: 모든 '1' 셀의 개수를 단순히 센다면, 연결된 섬의 개념을 무시하게 됩니다. 예를 들어 5개의 연결된 '1' 셀은 1개의 섬입니다.
      en: Simply counting all '1' cells ignores connectivity—5 connected land cells form 1 island, not 5. This is incorrect.
  - name:
      ko: Union-Find (Disjoint Set Union)
      en: Union-Find (Disjoint Set Union)
    complexity: O(m × n × α(m × n)) time / O(m × n) space
    type: distractor
    why:
      ko: 이론적으로 유효하지만, 이 문제에는 DFS/BFS보다 복잡하고 구현 난이도가 높습니다. 동적 연결성 갱신이 필요한 문제에 더 적합합니다.
      en: Valid but overly complex for this static problem; DFS/BFS are simpler and more intuitive. Union-Find is better for dynamic connectivity.
logic:
  format: slot
  slots:
  - label:
      ko: 엣지 케이스 확인
      en: Check edge cases
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 그리드가 null이거나 비어있으면 즉시 0을 반환합니다.
        en: If grid is null or empty, return 0 immediately to avoid index errors.
    - code: 'if len(grid) == 0: return 0'
      type: distractor
      why:
        ko: grid[0]의 존재 여부를 확인하지 않아서 grid가 [[]]인 경우 인덱스 에러가 발생합니다.
        en: Doesn't check grid[0], so empty rows could cause IndexError.
    - code: 'if grid is None: return -1'
      type: distractor
      why:
        ko: null 체크는 하지만 반환값이 -1이므로 예상 출력 0과 맞지 않습니다.
        en: Returns -1 instead of 0, contradicting expected output format.
  - label:
      ko: 자료 구조 초기화
      en: Initialize data structures
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 섬 개수, 방문 집합, 행/열 개수를 초기화합니다.
        en: Initialize island counter, visited set, and grid dimensions for efficient access.
    - code: islands = 1
      type: distractor
      why:
        ko: 초기값을 1로 설정하면 빈 그리드나 물만 있는 경우 잘못된 결과(1)를 반환합니다.
        en: Starting with islands=1 gives wrong results for grids with zero islands.
    - code: visit = []
      type: distractor
      why:
        ko: 리스트는 O(n) 조회 시간이 필요하여 전체 성능이 O(n^2)으로 저하됩니다.
        en: Using a list makes membership checks O(n), degrading performance to O(n²).
  - label:
      ko: DFS 경계 및 상태 검사
      en: DFS boundary and state checks
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 범위 초과, 물('0'), 또는 이미 방문한 셀이면 재귀를 종료합니다.
        en: Return early if out of bounds, water, or already visited to prevent infinite recursion and redundant work.
    - code: 'if r < 0 or r >= rows or c < 0 or c >= cols: return'
      type: distractor
      why:
        ko: 경계 확인만 있고 물과 방문 체크가 없어서 중복 탐색과 물 셀 처리 오류가 발생합니다.
        en: Missing water and visited checks causes redundant traversals and incorrect water handling.
    - code: 'if grid[r][c] != ''1'': return'
      type: distractor
      why:
        ko: 경계 체크 없이 grid 접근 시 범위 밖 인덱스에서 IndexError가 발생합니다.
        en: Missing boundary check causes IndexError on out-of-bounds access.
  - label:
      ko: 방문 표시 및 4방향 탐색
      en: Mark visited and explore 4 neighbors
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 현재 셀을 방문한 것으로 표시하고, 4방향(상, 하, 좌, 우)에 대해 재귀적으로 DFS를 호출합니다.
        en: Mark current cell as visited, then recursively explore all 4 adjacent neighbors.
    - code: visit.add((r, c)); dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1)
      type: distractor
      why:
        ko: 4방향 중 3개만 탐색하므로 마지막 방향(아래)을 놓쳐서 섬을 완전히 탐색하지 못합니다.
        en: Only explores 3 directions, missing one neighbor entirely.
    - code: dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1); visit.add((r, c))
      type: distractor
      why:
        ko: 재귀 후에 방문 표시를 하면, 같은 셀이 여러 번 탐색되고 무한 재귀 위험이 있습니다.
        en: Adding to visited after recursion risks infinite loops and duplicate visits.
  - label:
      ko: '주 반복문: 미방문 땅 셀 찾기'
      en: 'Main loop: find unvisited land cells'
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 그리드를 순회하면서 '1'이면서 아직 방문하지 않은 셀을 찾습니다.
        en: Iterate through all cells and identify unvisited land ('1').
    - code: 'if grid[r][c] == ''1'':'
      type: distractor
      why:
        ko: 방문 체크를 하지 않아서 이미 탐색한 섬의 셀에 대해 다시 섬 카운트를 증가시킵니다.
        en: Missing visited check causes same island to be counted multiple times.
    - code: 'if (r, c) not in visit:'
      type: distractor
      why:
        ko: 물인지 확인하지 않아서 모든 미방문 셀(물 포함)에 대해 섬을 카운트합니다.
        en: Missing land check counts water regions as islands too.
  - label:
      ko: 섬 카운터 증가 및 DFS 호출
      en: Increment counter and start DFS
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 새로운 섬을 발견했으므로 카운터를 1 증가시키고, DFS를 호출하여 이 섬의 모든 셀을 표시합니다.
        en: Found a new island; increment counter and call DFS to mark all connected cells.
    - code: dfs(r, c); islands += 1
      type: distractor
      why:
        ko: DFS 후에 카운트하면 코드 의도가 덜 명확하며, 조건부 로직이 복잡해집니다.
        en: Incrementing after DFS is less clear semantically; increment before to show 'found island, now explore it'.
    - code: islands = islands + 1 + count_connected_cells(r, c)
      type: distractor
      why:
        ko: 섬의 셀 개수만큼 더하면 최종 섬 개수가 아닌 총 셀 개수가 됩니다.
        en: Adding cell count gives wrong total; we count islands, not cells.
  - label:
      ko: 결과 반환
      en: Return result
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 모든 셀을 탐색 완료한 후 찾은 섬의 총 개수를 반환합니다.
        en: After traversing entire grid, return the total island count.
    - code: return len(visit)
      type: distractor
      why:
        ko: 방문한 셀의 개수를 반환하므로, 섬의 개수와 일치하지 않습니다.
        en: Returns count of visited cells, not island count—completely different answer.
    - code: return islands + 1
      type: distractor
      why:
        ko: 오프셋 에러로 실제보다 1 많은 섬 개수를 반환합니다.
        en: Off-by-one error returns more islands than actual count.
trace:
  code:
  - 'class Solution:'
  - '    def numIslands(self, grid: List[List[str]]) -> int:'
  - '        if not grid or not grid[0]:'
  - '            return 0'
  - ''
  - '        islands = 0'
  - '        visit = set()'
  - '        rows, cols = len(grid), len(grid[0])'
  - ''
  - '        def dfs(r, c):'
  - '            if ('
  - '                r not in range(rows)'
  - '                or c not in range(cols)'
  - '                or grid[r][c] == "0"'
  - '                or (r, c) in visit'
  - '            ):'
  - '                return'
  - ''
  - '            visit.add((r, c))'
  - '            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]'
  - '            for dr, dc in directions:'
  - '                dfs(r + dr, c + dc)'
  - ''
  - '        for r in range(rows):'
  - '            for c in range(cols):'
  - '                if grid[r][c] == "1" and (r, c) not in visit:'
  - '                    islands += 1'
  - '                    dfs(r, c)'
  - '        return islands'
  - ''
  - '# DFS O(1) Space and much less code'
  - 'class Solution:'
  - '    def numIslands(self, grid: List[List[str]]) -> int:'
  - '        rows, cols = len(grid), len(grid[0])'
  - '        def dfs(r, c):'
  - '            if not 0 <= r < len(grid) or not 0 <= c < len(grid[0]) or grid[r][c] == ''0'':'
  - '                return 0'
  - '            grid[r][c] = ''0'''
  - '            dfs(r + 1, c)'
  - '            dfs(r - 1, c)'
  - '            dfs(r, c + 1)'
  - '            dfs(r, c - 1)'
  - '            return 1'
  - '        count = 0'
  - '        for r in range(rows):'
  - '            for c in range(cols):'
  - '                count += dfs(r, c)'
  - '        return count'
  - ''
  - '# BFS Version From Video'
  - 'class SolutionBFS:'
  - '    def numIslands(self, grid: List[List[str]]) -> int:'
  - '        if not grid:'
  - '            return 0'
  - ''
  - '        rows, cols = len(grid), len(grid[0])'
  - '        visited = set()'
  - '        islands = 0'
  - ''
  - '         def bfs(r, c):'
  - '             q = deque()'
  - '             visited.add((r, c))'
  - '             q.append((r, c))'
  - '           '
  - '             while q:'
  - '                 row, col = q.popleft()'
  - '                 directions = [[1, 0],[-1, 0],[0, 1],[0, -1]]'
  - '               '
  - '                 for dr, dc in directions:'
  - '                     r, c = row + dr, col + dc'
  - '                     if (r) in range(rows) and (c) in range(cols) and grid[r][c] == ''1'' and (r, c) not in visited:'
  - '                       '
  - '                         q.append((r, c ))'
  - '                         visited.add((r, c ))'
  - ''
  - '         for r in range(rows):'
  - '             for c in range(cols):'
  - '               '
  - '                 if grid[r][c] == "1" and (r, c) not in visited:'
  - '                     bfs(r, c)'
  - '                     islands += 1 '
  - ''
  - '         return islands'
  - ''
  cases:
  - input: '[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]'
    expected: '1'
  - input: '[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]'
    expected: '3'
  worked_example:
    input: '[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]'
    steps:
    - ko: '초기화: islands=0, visit={}, rows=4, cols=5. 그리드는 5×4 크기의 첫 번째 테스트 케이스.'
      en: 'Initialize: islands=0, visit={}, rows=4, cols=5. Grid is the first example.'
    - ko: '(0,0) 확인: grid[0][0]=''1''이고 방문하지 않았으므로, islands=1 증가 후 DFS(0,0) 호출.'
      en: 'Check (0,0): grid[0][0]=''1'' and unvisited → increment islands to 1, call DFS(0,0).'
    - ko: 'DFS 탐색: (0,0)에서 시작하여 인접한 모든 ''1'' 셀을 방문. (0,1)→(0,2)→(0,3)→(1,0)→(1,1)→(1,3)→(2,0)→(2,1)을 visit에 추가.'
      en: 'DFS traversal: from (0,0) mark all connected ''1'' cells—(0,1), (0,2), (0,3), (1,0), (1,1), (1,3), (2,0), (2,1).'
    - ko: '나머지 셀 탐색: 남은 모든 셀은 물(''0'')이거나 이미 방문했으므로 섬 카운트 증가 없음. 최종 islands=1.'
      en: 'Remaining cells: all are water (''0'') or visited, so islands count stays 1.'
    answer: '1'
solution:
  code: "class Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:\n        if not grid or not grid[0]:\n            return 0\n\n        islands = 0\n        visit = set()\n        rows, cols = len(grid), len(grid[0])\n\n        def dfs(r, c):\n            if (\n                r not in range(rows)\n                or c not in range(cols)\n                or grid[r][c] == \"0\"\n                or (r, c) in visit\n            ):\n                return\n\n            visit.add((r, c))\n            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]\n            for dr, dc in directions:\n                dfs(r + dr, c + dc)\n\n        for r in range(rows):\n            for c in range(cols):\n                if grid[r][c] == \"1\" and (r, c) not in visit:\n                    islands += 1\n                    dfs(r, c)\n        return islands\n\n# DFS O(1) Space and much less code\nclass Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:\n        rows, cols = len(grid),\
    \ len(grid[0])\n        def dfs(r, c):\n            if not 0 <= r < len(grid) or not 0 <= c < len(grid[0]) or grid[r][c] == '0':\n                return 0\n            grid[r][c] = '0'\n            dfs(r + 1, c)\n            dfs(r - 1, c)\n            dfs(r, c + 1)\n            dfs(r, c - 1)\n            return 1\n        count = 0\n        for r in range(rows):\n            for c in range(cols):\n                count += dfs(r, c)\n        return count\n\n# BFS Version From Video\nclass SolutionBFS:\n    def numIslands(self, grid: List[List[str]]) -> int:\n        if not grid:\n            return 0\n\n        rows, cols = len(grid), len(grid[0])\n        visited = set()\n        islands = 0\n\n         def bfs(r, c):\n             q = deque()\n             visited.add((r, c))\n             q.append((r, c))\n           \n             while q:\n                 row, col = q.popleft()\n                 directions = [[1, 0],[-1, 0],[0, 1],[0, -1]]\n               \n                 for\
    \ dr, dc in directions:\n                     r, c = row + dr, col + dc\n                     if (r) in range(rows) and (c) in range(cols) and grid[r][c] == '1' and (r, c) not in visited:\n                       \n                         q.append((r, c ))\n                         visited.add((r, c ))\n\n         for r in range(rows):\n             for c in range(cols):\n               \n                 if grid[r][c] == \"1\" and (r, c) not in visited:\n                     bfs(r, c)\n                     islands += 1 \n\n         return islands\n\n"
  complexity:
    time: O(m × n)
    space: O(m × n)
  followup:
  - ko: 가장 큰 섬의 크기를 구하려면?
    en: How would you find the size of the largest island?
  - ko: 각 DFS 호출 중 방문한 셀 개수를 센 후 최댓값을 추적합니다. DFS 함수에서 반환값을 크기로 사용하고 max()로 비교하면 됩니다.
    en: Track the count of cells visited during each DFS and return the maximum. Modify DFS to return the size of the island it explores.
```