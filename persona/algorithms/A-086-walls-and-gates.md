---
created: '2026-08-13'
date: '2026-08-13'
day: Day 86
difficulty: medium
id: A-086
source:
  curated_in:
  - neetcode150
  number: 286
  platform: leetcode
  slug: walls-and-gates
  url: https://leetcode.com/problems/walls-and-gates/
status: draft
tags:
- array
- breadth-first-search
- matrix
title:
  en: Walls and Gates
  ko: 벽과 문
today: true
type: algorithm
updated: '2026-08-13'
visible: true
---

# 벽과 문

## Data

```yaml
problem:
  title:
    ko: 벽과 문
    en: Walls and Gates
  statement:
    ko: 'm×n 2D 격자가 주어집니다. 각 셀은 다음 중 하나입니다:

      - 0: 문(gate)

      - -1: 벽(wall)

      - 2147483647: 빈 방(empty room)


      각 빈 방을 가장 가까운 문까지의 거리로 업데이트하세요. 문에 도달할 수 없는 셀은 그대로 2147483647로 유지됩니다. 격자를 제자리에서(in-place) 수정하세요.'
    en: 'You are given an m×n 2D grid rooms where each cell is one of the following:

      - 0: A gate

      - -1: A wall

      - 2147483647: An empty room


      Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should remain as 2147483647. Modify the grid in-place.'
  constraints:
  - m and n are in range [1, 100]
  - rooms[i][j] is one of {-1, 0, 2147483647}
  - There is at least one gate in rooms
  io:
  - input: '[[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]'
    output: '[[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,2]]'
  - input: '[[-1]]'
    output: '[[-1]]'
clarifying:
  items:
  - q:
      ko: 0은 문(gate)을 나타내나요?
      en: Does 0 represent a gate?
    type: good
    why:
      ko: 0이 문이며, 이들이 BFS의 출발점입니다.
      en: 0 represents gates, which are the starting points for multi-source BFS.
  - q:
      ko: -1은 벽으로, 통과할 수 없나요?
      en: Does -1 represent a wall that cannot be traversed?
    type: good
    why:
      ko: 벽은 BFS 중에 방문할 수 없는 장애물입니다.
      en: Walls are obstacles that should never be visited or updated during BFS.
  - q:
      ko: 원본 배열을 수정해야 하나요?
      en: Should we modify the input array in-place?
    type: good
    why:
      ko: 이 문제는 새로운 배열을 반환하지 않고 주어진 배열을 직접 수정합니다.
      en: The problem requires modifying the grid in-place rather than creating a new one.
  - q:
      ko: 각 방에 대해 개별적으로 BFS를 실행해야 하나요?
      en: Should we run BFS separately from each empty room?
    type: distractor
    why:
      ko: 비효율적입니다. 모든 문에서 동시에 시작하는 다중 출발점 BFS가 최적입니다.
      en: That would be inefficient. Multi-source BFS starting from all gates simultaneously is optimal.
  - q:
      ko: 문에 도달할 수 없는 방은 어떻게 처리하나요?
      en: What happens to rooms that cannot reach any gate?
    type: distractor
    why:
      ko: 그들은 2147483647로 유지됩니다. BFS는 이들에 절대 도달하지 않으므로 자동으로 처리됩니다.
      en: They remain 2147483647 since BFS will never reach them from any gate source.
  - q:
      ko: 벽을 먼저 처리한 후 방을 처리해야 하나요?
      en: Should we pre-process walls before starting BFS?
    type: distractor
    why:
      ko: 아니요. addRooms 헬퍼 함수에서 벽을 체크하므로 자동으로 건너뜁니다.
      en: No, the addRooms validation function automatically skips walls during BFS.
approach:
  items:
  - name:
      ko: 다중 출발점 BFS
      en: Multi-source BFS
    complexity: O(m*n) time / O(m*n) space
    type: good
    why:
      ko: 모든 문을 동시에 큐에 넣어 한 번의 BFS로 각 셀까지의 최단 거리를 계산합니다.
      en: Start BFS from all gates simultaneously. Each cell is visited exactly once, computing shortest distance in a single pass.
  - name:
      ko: 각 문마다 개별 BFS
      en: Individual BFS from each gate
    complexity: O(g*m*n) time / O(m*n) space
    type: distractor
    why:
      ko: 각 문에서 별도 BFS를 실행하면 중복 계산이 발생하고, g(문의 개수)배 느립니다.
      en: Running separate BFS from each gate causes redundant computation and is g times slower.
  - name:
      ko: 동적 계획법 (DP)
      en: Dynamic Programming
    complexity: O(m*n) time / O(m*n) space
    type: distractor
    why:
      ko: DP는 이 문제에 적합하지 않습니다. 우리는 그래프의 최단 경로를 찾아야 하므로 그래프 탐색이 필요합니다.
      en: DP is unsuitable for finding shortest paths. This is inherently a graph traversal problem.
  - name:
      ko: Dijkstra's 알고리즘
      en: Dijkstra's Algorithm
    complexity: O(m*n*log(m*n)) time / O(m*n) space
    type: distractor
    why:
      ko: 모든 엣지 가중치가 1이므로 Dijkstra는 BFS보다 복잡하고 느립니다.
      en: With uniform edge weights (all 1), Dijkstra is unnecessarily complex compared to simple BFS.
logic:
  format: slot
  slots:
  - label:
      ko: 격자 크기 초기화
      en: Initialize grid dimensions
    indent: 0
    options:
    - code: ROWS, COLS = len(rooms), len(rooms[0])
      type: good
      why:
        ko: ROWS와 COLS을 저장하여 이후 경계 체크에서 사용합니다.
        en: Store dimensions for boundary validation during BFS traversal.
    - code: ROWS, COLS = len(rooms), len(rooms)
      type: distractor
      why:
        ko: COLS 계산이 잘못되었습니다. len(rooms)는 행의 개수이지, 열의 개수가 아닙니다.
        en: Incorrect column count. Should use len(rooms[0]) not len(rooms).
    - code: 'ROWS = len(rooms) + 1

        COLS = len(rooms[0]) + 1'
      type: distractor
      why:
        ko: 크기를 초과합니다. 경계 체크가 잘못된 결과를 냅니다.
        en: Off-by-one errors break boundary validation.
  - label:
      ko: 방문 추적 및 큐 초기화
      en: Initialize visit set and queue
    indent: 0
    options:
    - code: visit = set()
      type: good
      why:
        ko: visit 세트로 중복 방문을 방지하고, deque q로 BFS를 수행합니다.
        en: The visit set prevents reprocessing cells; deque q stores the BFS frontier.
    - code: 'visit = []

        q = []'
      type: distractor
      why:
        ko: 리스트는 O(n) 조회를 가지므로 O(1)인 set보다 느립니다. 또한 append/popleft 시 성능 문제가 있습니다.
        en: Lists have O(n) lookup vs O(1) for sets; also inefficient popleft performance.
    - code: 'visited = set()

        queue = deque()'
      type: distractor
      why:
        ko: 변수명이 코드의 나머지 부분과 일치하지 않아 참조 오류가 발생합니다.
        en: Variable name mismatch causes undefined reference errors in subsequent code.
  - label:
      ko: 경계 및 벽 검증 헬퍼 함수
      en: 'Helper function: boundary and wall validation'
    indent: 0
    options:
    - code: 'def addRooms(r, c):'
      type: good
      why:
        ko: addRooms는 경계, 벽, 방문 여부를 체크한 후 유효한 셀만 큐에 추가합니다.
        en: The addRooms function validates cells comprehensively before queueing them.
    - code: "def addRooms(r, c):\n    if r < 0 or c < 0 or r >= ROWS or c >= COLS:\n        return\n    visit.add((r, c))\n    q.append([r, c])"
      type: distractor
      why:
        ko: 벽 (-1)과 방문 여부 체크가 없어서 벽이나 이미 방문한 셀을 중복 처리합니다.
        en: Missing wall and visited checks causes walls and duplicate cells to be processed.
    - code: "def addRooms(r, c):\n    if (r, c) in visit or rooms[r][c] == -1:\n        return\n    visit.add((r, c))\n    q.append([r, c])"
      type: distractor
      why:
        ko: 경계 체크가 없어서 범위를 벗어난 인덱스로 접근할 수 있습니다.
        en: Missing boundary checks can cause IndexError on out-of-bounds access.
  - label:
      ko: 모든 문으로 BFS 초기화
      en: Initialize BFS queue with all gates
    indent: 0
    options:
    - code: 'for r in range(ROWS):'
      type: good
      why:
        ko: '다중 출발점 BFS의 핵심: 모든 문(0)을 동시에 출발점으로 설정하여 각 셀까지의 최단 거리를 한 번에 계산합니다.'
        en: 'Critical for multi-source BFS: all gates are sources simultaneously, enabling single-pass distance computation.'
    - code: "if rooms[r][c] != 0:\n    q.append([r, c])\n    visit.add((r, c))"
      type: distractor
      why:
        ko: 조건이 반대입니다. 0이 아닌 셀을 추가하므로 문을 제외하고 모든 셀을 시작점으로 만듭니다.
        en: 'Inverted condition: adds non-gates instead of gates, breaking the algorithm.'
    - code: "if rooms[r][c] == 0:\n    q.append([r, c])\n    # 방문 여부 업데이트 없음"
      type: distractor
      why:
        ko: 문을 큐에 추가하지만 visit에 표시하지 않아 중복 처리될 수 있습니다.
        en: Adds gates to queue without marking as visited, causing potential duplicates.
  - label:
      ko: 거리별 층별 BFS 처리
      en: Level-by-level BFS traversal
    indent: 0
    options:
    - code: 'while q:'
      type: good
      why:
        ko: 외부 while은 각 거리 레벨을 처리합니다. len(q)를 고정하여 현재 거리의 모든 셀을 처리한 후 거리를 증가시킵니다.
        en: Outer loop processes one distance level at a time. Fixed queue size ensures all cells at current distance are processed before incrementing distance.
    - code: "while q:\n    r, c = q.popleft()\n    rooms[r][c] = dist\n    dist += 1"
      type: distractor
      why:
        ko: 각 셀마다 거리를 증가시켜서 인접 셀의 거리 계산이 잘못됩니다.
        en: Incrementing distance per cell instead of per level produces incorrect distances.
    - code: "while q:\n    r, c = q.popleft()\n    rooms[r][c] = dist\n    addRooms(r + 1, c)\n    addRooms(r - 1, c)\n    addRooms(r, c + 1)\n    addRooms(r, c - 1)"
      type: distractor
      why:
        ko: 거리 업데이트가 루프 외부에 없어서 모든 셀이 같은 거리를 받습니다.
        en: Missing distance increment causes all cells to have the same distance value.
  - label:
      ko: 4방향 인접 셀 탐색
      en: Explore 4 adjacent directions
    indent: 1
    options:
    - code: addRooms(r + 1, c)
      type: good
      why:
        ko: 상, 하, 좌, 우 4방향을 모두 탐색하여 모든 가능한 최단 경로를 고려합니다.
        en: Systematically explores all 4 neighbors (up, down, left, right) to find shortest distances in grid.
    - code: 'addRooms(r + 1, c)

        addRooms(r, c + 1)'
      type: distractor
      why:
        ko: 2방향만 탐색하므로 모든 경로를 찾지 못합니다.
        en: Only explores 2 directions; misses valid shortest paths.
    - code: "for dr, dc in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1)]:\n    addRooms(r + dr, c + dc)"
      type: distractor
      why:
        ko: 대각선(1,1), (-1,-1)을 포함하면 격자 거리 규칙을 위반합니다.
        en: Including diagonals violates standard grid distance rules.
trace:
  code:
  - 'class Solution:'
  - '    """'
  - '    @param rooms: m x n 2D grid'
  - '    @return: nothing'
  - '    """'
  - ''
  - '    def walls_and_gates(self, rooms: List[List[int]]):'
  - '        ROWS, COLS = len(rooms), len(rooms[0])'
  - '        visit = set()'
  - '        q = deque()'
  - ''
  - '        def addRooms(r, c):'
  - '            if ('
  - '                min(r, c) < 0'
  - '                or r == ROWS'
  - '                or c == COLS'
  - '                or (r, c) in visit'
  - '                or rooms[r][c] == -1'
  - '            ):'
  - '                return'
  - '            visit.add((r, c))'
  - '            q.append([r, c])'
  - ''
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                if rooms[r][c] == 0:'
  - '                    q.append([r, c])'
  - '                    visit.add((r, c))'
  - ''
  - '        dist = 0'
  - '        while q:'
  - '            for i in range(len(q)):'
  - '                r, c = q.popleft()'
  - '                rooms[r][c] = dist'
  - '                addRooms(r + 1, c)'
  - '                addRooms(r - 1, c)'
  - '                addRooms(r, c + 1)'
  - '                addRooms(r, c - 1)'
  - '            dist += 1'
  cases:
  - input: '[[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]'
    expected: '[[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,2]]'
  - input: '[[-1]]'
    expected: '[[-1]]'
  worked_example:
    input: '[[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]'
    steps:
    - ko: '격자에서 모든 문(0)을 찾습니다: (0,2)와 (3,0). 이들을 큐에 넣고 visit에 표시하며, dist=0입니다.'
      en: 'Find all gates (0): (0,2) and (3,0). Add both to queue and visit set with dist=0.'
    - ko: 'dist=1: 첫 번째 레벨 처리. (0,2)의 이웃 (0,3), (1,2)와 (3,0)의 이웃 (2,0)을 큐에 추가합니다. dist를 1로 증가시킵니다.'
      en: 'dist=1: Process level 1. Neighbors of gates like (0,3), (1,2), (2,0) are added with distance 1.'
    - ko: 'dist=2, 3, ...: 계속해서 외부로 확산합니다. 각 새 레벨의 모든 셀을 처리한 후 거리를 증가시킵니다.'
      en: 'dist=2, 3, ...: Continue expanding outward. Each level completes before distance increments.'
    - ko: 벽(-1)은 addRooms에서 필터링되고, 도달 불가능한 셀은 초기값 2147483647을 유지합니다.
      en: Walls (-1) are filtered by addRooms validation. Unreachable cells retain initial 2147483647.
    answer: '[[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,2]]'
solution:
  code: "class Solution:\n    \"\"\"\n    @param rooms: m x n 2D grid\n    @return: nothing\n    \"\"\"\n\n    def walls_and_gates(self, rooms: List[List[int]]):\n        ROWS, COLS = len(rooms), len(rooms[0])\n        visit = set()\n        q = deque()\n\n        def addRooms(r, c):\n            if (\n                min(r, c) < 0\n                or r == ROWS\n                or c == COLS\n                or (r, c) in visit\n                or rooms[r][c] == -1\n            ):\n                return\n            visit.add((r, c))\n            q.append([r, c])\n\n        for r in range(ROWS):\n            for c in range(COLS):\n                if rooms[r][c] == 0:\n                    q.append([r, c])\n                    visit.add((r, c))\n\n        dist = 0\n        while q:\n            for i in range(len(q)):\n                r, c = q.popleft()\n                rooms[r][c] = dist\n                addRooms(r + 1, c)\n                addRooms(r - 1, c)\n                addRooms(r, c\
    \ + 1)\n                addRooms(r, c - 1)\n            dist += 1\n"
  complexity:
    time: O(m*n)
    space: O(m*n)
  followup:
  - ko: 최대 거리가 매우 크거나 제한이 있다면 어떻게 처리할까요? 예를 들어 200 이상인 거리를 모두 200으로 표시해야 한다면?
    en: What if there's a maximum distance cap? For example, if you need to mark all unreachable cells only if distance > some threshold?
  - ko: 3D 격자나 N-dimensional 격자에서 이를 일반화할 수 있을까요?
    en: How would you generalize this solution to 3D grids or N-dimensional grids?
  - ko: '여러 종류의 출발점(예: 서로 다른 값 0, 1, 2)이 있다면 우선순위를 어떻게 설정할까요?'
    en: If there are multiple types of sources with different priorities, how would the algorithm need to change?
```