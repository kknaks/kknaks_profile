---
created: '2026-08-24'
date: '2026-08-24'
day: Day 96
difficulty: hard
id: A-096
source:
  curated_in:
  - neetcode150
  number: 778
  platform: leetcode
  slug: swim-in-rising-water
  url: https://leetcode.com/problems/swim-in-rising-water/
status: draft
tags:
- array
- binary-search
- depth-first-search
- breadth-first-search
- union-find
- minimax-algorithm
- heap-priority-queue
- matrix
- dijkstra
title:
  en: Swim in Rising Water
  ko: 상승하는 물에서 수영하기
today: false
type: algorithm
updated: '2026-08-24'
visible: true
---

# 상승하는 물에서 수영하기

## Data

```yaml
problem:
  title:
    ko: 상승하는 물에서 수영하기
    en: Swim in Rising Water
  statement:
    ko: 'n × n 정수 행렬 grid가 주어지며, 각 값 grid[i][j]는 위치 (i, j)의 높이를 나타냅니다.


      비가 내리기 시작하고 시간이 지남에 따라 물이 천천히 상승합니다. 시간 t일 때 수위는 t이므로, 높이가 t 이하인 모든 셀이 잠긴 상태(또는 도달 가능한 상태)가 됩니다.


      한 셀에서 인접한 4방향(상하좌우) 셀로 이동할 수 있습니다. 이동하려면 두 셀의 높이가 모두 t 이하여야 합니다. 무제한으로 멀리 헤엄칠 수 있지만 시간은 걸리지 않습니다. 물론 격자판의 경계 내에 머물러야 합니다.


      왼쪽 위 셀 (0, 0)에서 시작하여 오른쪽 아래 셀 (n - 1, n - 1)에 도달하는 데 필요한 최소 시간을 반환하세요.'
    en: 'You are given an n x n integer matrix grid where each value grid[i][j] represents the elevation at that point (i, j).


      It starts raining, and water gradually rises over time. At time t, the water level is t, meaning any cell with elevation less than equal to t is submerged or reachable.


      You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most t. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.


      Return the minimum time until you can reach the bottom right square (n - 1, n - 1) if you start at the top left square (0, 0).'
  constraints:
  - n == grid.length == grid[i].length
  - 1 ≤ n ≤ 50
  - 0 ≤ grid[i][j] < n²
  - Each value grid[i][j] is unique
  io:
  - input: '[[0,2],[1,3]]'
    output: '3'
  - input: '[[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]'
    output: '16'
clarifying:
  items:
  - q:
      ko: 시간 t에 높이가 t 이하인 셀에만 이동할 수 있다는 의미는?
      en: Does 'elevation at most t' mean both source and destination must be ≤ t to swim?
    type: good
    why:
      ko: '문제에서 명시: ''두 셀의 높이가 모두 t 이하일 때만 이동 가능''. 이는 Dijkstra에서 경로상 최대 높이를 추적하는 이유입니다.'
      en: The problem explicitly states both squares must have elevation ≤ t. This is why we track the maximum elevation on the path, not just individual step heights.
  - q:
      ko: 왜 '최소 시간'은 경로상 최대 높이와 같은가?
      en: Why does the minimum time equal the maximum elevation encountered on the path?
    type: good
    why:
      ko: 물이 계속 상승하므로, 어떤 경로든 그 경로상 가장 높은 셀에 도달해야만 전체 경로가 접근 가능해집니다.
      en: Water continuously rises; a path becomes accessible only when the water level reaches the highest cell on that path. Thus, minimum time = maximum elevation on the optimal path.
  - q:
      ko: 시작 셀 (0,0)의 높이가 매우 높다면 어떻게 되나요?
      en: What is the minimum possible answer if grid[0][0] has elevation 10?
    type: good
    why:
      ko: 최소 시간은 최소한 시작 셀의 높이 이상이어야 합니다. 답은 ≥ grid[0][0] 입니다.
      en: The minimum answer is at least grid[0][0], since we must wait for water to reach the starting cell before we can begin.
  - q:
      ko: 같은 셀을 여러 번 방문할 수 있나요?
      en: Can we revisit the same cell multiple times during the algorithm?
    type: good
    why:
      ko: 아니오. Dijkstra 알고리즘의 특성상 한 셀이 한 번 처리되면 그것이 최소 시간이므로 재방문은 불필요합니다.
      en: No. Once a cell is popped from the heap (minimum time reached), no other path can improve it. The visited set prevents redundant processing.
  - q:
      ko: 대각선 방향(대각선)으로도 이동할 수 있나요?
      en: Can we move diagonally (e.g., from (0,0) to (1,1))?
    type: distractor
    why:
      ko: 아니오. 문제에서 '4방향 인접'이라고 명시했습니다. 대각선은 허용되지 않습니다.
      en: No. The problem specifies '4-directionally adjacent', meaning only up, down, left, right. Diagonals are not allowed.
  - q:
      ko: 단순 BFS(너비 우선 탐색)로 충분하지 않을까요?
      en: Why can't we use simple BFS (each step costs 1 unit)?
    type: distractor
    why:
      ko: BFS는 모든 간선 가중치가 1일 때만 작동합니다. 여기서는 각 경로의 '비용'이 경로상 최대 높이로 불균등합니다. Dijkstra가 필요합니다.
      en: BFS works only when all edge weights are equal. Here, the 'cost' of a path depends on its maximum elevation, which varies. Dijkstra handles weighted edges correctly.
  - q:
      ko: 항상 오른쪽 또는 아래로만 이동해야 하나요?
      en: Must we always move rightward or downward (like a DP grid problem)?
    type: distractor
    why:
      ko: 아니오. 4방향 모두 이동 가능하며, 위나 왼쪽으로도 이동할 수 있습니다. 이것이 그래프 문제로 만드는 이유입니다.
      en: No. We can move in any of the 4 directions, including backward. This is why Dijkstra (a full graph algorithm) is appropriate, not dynamic programming.
approach:
  items:
  - name:
      ko: 다익스트라 알고리즘 (우선순위 큐)
      en: Dijkstra's Algorithm with Min-Heap
    complexity: O(n² log n) time / O(n²) space
    type: good
    why:
      ko: 각 셀을 최소 시간 순서로 처리합니다. 경로의 '거리'는 경로상 최대 높이이며, 힙을 사용하여 효율적으로 처리합니다.
      en: Process cells in order of minimum time using a min-heap. The 'distance' is the maximum elevation on the path. Guarantees optimal solution in one pass.
  - name:
      ko: 이진 탐색 + DFS/BFS
      en: Binary Search + DFS/BFS
    complexity: O(n² log n²) time / O(n²) space
    type: good
    why:
      ko: 답(시간 T)을 이진 탐색합니다. 각 T에 대해, 높이 ≤ T인 셀들로만 이동 가능한지 DFS/BFS로 확인합니다.
      en: Binary search on the answer (time T). For each T, check if we can reach the destination using only cells with elevation ≤ T via DFS/BFS.
  - name:
      ko: '그리디: 항상 가장 낮은 높이의 인접 셀로 이동'
      en: 'Greedy: Always Move to Lowest Adjacent Cell'
    complexity: O(n²) time / O(n²) space
    type: distractor
    why:
      ko: 국소 최소값에 갇힐 수 있습니다. 예제 2에서 중앙의 높은 영역으로 우회해야 하는데, 그리디는 이를 놓칩니다.
      en: Can get stuck in local minima. Example 2 requires taking a detour; greedy won't find this alternative path.
  - name:
      ko: '동적 프로그래밍: 하단-우측만 이동 가능'
      en: Dynamic Programming (Right/Down Only)
    complexity: O(n²) time / O(n²) space
    type: distractor
    why:
      ko: 이 문제는 상하좌우 모든 방향 이동을 허용하므로 DP 상태 정의가 불가능합니다. 최단 경로 문제는 그래프 알고리즘이 필요합니다.
      en: DP works only for restricted paths (e.g., down-right only). This problem allows all 4 directions, breaking the DP prerequisite of optimal substructure.
logic:
  format: slot
  slots:
  - label:
      ko: 시작 셀로 최소 힙 초기화
      en: Initialize min-heap with starting cell
    indent: 0
    options:
    - code: 'minH = [[grid[0][0], 0, 0]]  # (time/max-height, r, c)'
      type: good
      why:
        ko: 시작 시간은 시작 셀의 높이입니다. (0,0)에서 물의 수위가 그 높이에 도달할 때까지 기다려야 합니다.
        en: The initial time equals grid[0][0], the elevation we must wait for before swimming begins. Store as (time, row, col) tuple.
    - code: minH = [[0, 0, 0]]
      type: distractor
      why:
        ko: 시간 0에서는 (0,0)에 접근할 수 없습니다. 시작 높이까지 기다려야 합니다.
        en: Time 0 is incorrect; we must wait until water reaches grid[0][0].
    - code: minH = [grid[0][0], 0, 0]
      type: distractor
      why:
        ko: 힙은 리스트의 리스트여야 합니다. heapq 연산이 제대로 작동하려면 각 항목이 리스트/튜플이어야 합니다.
        en: Heap requires a list of lists, not a flat tuple, for heapq operations to work correctly.
    - code: minH = [[grid[N-1][N-1], N-1, N-1]]
      type: distractor
      why:
        ko: 목표부터 시작하는 것은 잘못된 방향입니다. (0,0)에서 시작해야 합니다.
        en: Start from the destination backwards? No—must begin from top-left (0, 0).
  - label:
      ko: 시작점을 방문 표시
      en: Mark starting cell as visited
    indent: 0
    options:
    - code: visit.add((0, 0))
      type: good
      why:
        ko: 방문 집합에 시작 위치를 추가하여 이후 반복에서 재방문을 방지합니다.
        en: Add starting position to visited set to prevent reprocessing it when encountering it as a neighbor later.
    - code: visit = {(0, 0)}
      type: distractor
      why:
        ko: 이것은 초기화입니다. 1번 줄에서 이미 visit = set()로 선언했으므로 add를 사용해야 합니다.
        en: This initializes the set, but visit was already initialized on line 1. Should use .add() to append.
    - code: 'if (0, 0) not in visit: visit.add((0, 0))'
      type: distractor
      why:
        ko: 불필요한 체크입니다. 빈 집합이므로 (0,0)은 확실히 없습니다.
        en: Redundant check; the set is empty, so this is always true. Just add directly.
  - label:
      ko: 최소 시간의 셀을 힙에서 추출
      en: Pop cell with minimum time from heap
    indent: 1
    options:
    - code: t, r, c = heapq.heappop(minH)
      type: good
      why:
        ko: '다익스트라의 핵심: 항상 최소 시간을 가진 셀을 먼저 처리합니다. t는 해당 셀에 도달하는 최소 시간(경로상 최대 높이)입니다.'
        en: 'Dijkstra core: always process the cell with minimum time first. t represents the maximum elevation encountered on the path to this cell.'
    - code: t, r, c = heapq.heappushpop(minH, new_item)
      type: distractor
      why:
        ko: heappushpop은 새 항목을 동시에 추가하며, 이는 로직을 바꿉니다. 단순히 팝만 해야 합니다.
        en: heappushpop adds a new item at the same time. We only want to extract, not insert.
    - code: r, c, t = heapq.heappop(minH)
      type: distractor
      why:
        ko: 순서가 틀렸습니다. 힙은 (time, row, col) 순서로 저장되어 있습니다.
        en: Wrong unpacking order. Heap stores (time, row, col), not (row, col, time).
    - code: t = min(minH)
      type: distractor
      why:
        ko: 세 값(시간, 행, 열)을 모두 추출해야 합니다. min()은 최솟값만 반환합니다.
        en: min() returns only the smallest value. We need to unpack all three components (time, row, col).
  - label:
      ko: 목표 도달 확인
      en: Check if destination is reached
    indent: 2
    options:
    - code: 'if r == N - 1 and c == N - 1:'
      type: good
      why:
        ko: '다익스트라의 종료 조건: (N-1, N-1)을 팝할 때, 그것이 최소 시간입니다. 이 시점에서 t를 반환합니다.'
        en: 'Dijkstra''s termination: once we pop the destination, we''ve found its minimum time. Early return avoids unnecessary further processing.'
    - code: 'if r == N or c == N:'
      type: distractor
      why:
        ko: 오프 바이 원 에러입니다. 배열은 0부터 N-1까지 인덱싱되므로 N-1을 확인해야 합니다.
        en: Off-by-one error. Array indices go from 0 to N-1, not 0 to N.
    - code: 'if r == N - 1 or c == N - 1:'
      type: distractor
      why:
        ko: 둘 다 확인해야 합니다. or는 하나만 만족하면 true가 되어 잘못된 조기 종료를 초래합니다.
        en: Must check both coordinates. Using 'or' stops too early (e.g., at (N-1, 0)).
    - code: 'if grid[r][c] == grid[N-1][N-1]:'
      type: distractor
      why:
        ko: 각 값이 고유하므로 이 비교는 작동하지만, 좌표를 확인하는 것이 더 명확하고 효율적입니다.
        en: While values are unique, comparing values is indirect and fragile. Compare coordinates directly.
  - label:
      ko: 4방향 인접 셀 탐색
      en: Iterate through 4 directions
    indent: 2
    options:
    - code: 'for dr, dc in directions:'
      type: good
      why:
        ko: 현재 셀의 모든 4방향 이웃을 체크합니다. directions 배열은 이미 3번 줄에서 초기화되었습니다.
        en: Check all 4-directional neighbors (up, down, left, right). The directions list was precomputed to avoid hardcoding.
    - code: 'for dr, dc in [(0,1), (1,0), (-1,0), (0,-1)]:'
      type: distractor
      why:
        ko: 하드코딩되어 있습니다. directions 변수를 사용하는 것이 더 유지보수하기 쉽고, 변경이 한 곳에서만 필요합니다.
        en: Hardcoding; harder to modify if needed. Using the directions variable is more maintainable.
    - code: 'for i in range(4): neiR, neiC = r + directions[i][0], c + directions[i][1]'
      type: distractor
      why:
        ko: 인덱스를 통한 순회는 불필요하게 복잡합니다. 직접 언팩하는 것이 더 우아합니다.
        en: Iterating by index is unnecessarily verbose. Direct unpacking (as in the good answer) is more Pythonic.
  - label:
      ko: 경로상 최대 높이로 이웃을 힙에 추가
      en: Push neighbor with max elevation on path
    indent: 3
    options:
    - code: heapq.heappush(minH, [max(t, grid[neiR][neiC]), neiR, neiC])
      type: good
      why:
        ko: '핵심 통찰: 이웃에 도달하는 시간은 max(현재시간, 이웃높이)입니다. 경로상 가장 높은 셀까지 기다려야 합니다.'
        en: 'Key insight: time to reach neighbor = max(current_time, neighbor_elevation). We wait for the highest cell on the path.'
    - code: heapq.heappush(minH, [grid[neiR][neiC], neiR, neiC])
      type: distractor
      why:
        ko: 이웃의 높이만 사용하면, 이전 경로상 높은 셀을 무시하게 됩니다. 경로상 최대값을 추적해야 합니다.
        en: Ignores the maximum on the current path. We must track the highest cell encountered so far.
    - code: heapq.heappush(minH, [min(t, grid[neiR][neiC]), neiR, neiC])
      type: distractor
      why:
        ko: 최소값을 사용하는 것은 반대입니다. 물은 상승하므로 최대값까지 기다려야 합니다.
        en: Using min is backwards. Water level rises, so we wait until it reaches the maximum, not minimum.
    - code: heapq.heappush(minH, [t + grid[neiR][neiC], neiR, neiC])
      type: distractor
      why:
        ko: 합계는 의미가 없습니다. 시간은 수위(높이)이며, 누적되지 않습니다.
        en: Adding times doesn't make sense. Time is determined by water level (height), not cumulative steps.
trace:
  code:
  - 'class Solution:'
  - '    def swimInWater(self, grid: List[List[int]]) -> int:'
  - '        N = len(grid)'
  - '        visit = set()'
  - '        minH = [[grid[0][0], 0, 0]]  # (time/max-height, r, c)'
  - '        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]'
  - ''
  - '        visit.add((0, 0))'
  - '        while minH:'
  - '            t, r, c = heapq.heappop(minH)'
  - '            if r == N - 1 and c == N - 1:'
  - '                return t'
  - '            for dr, dc in directions:'
  - '                neiR, neiC = r + dr, c + dc'
  - '                if ('
  - '                    neiR < 0'
  - '                    or neiC < 0'
  - '                    or neiR == N'
  - '                    or neiC == N'
  - '                    or (neiR, neiC) in visit'
  - '                ):'
  - '                    continue'
  - '                visit.add((neiR, neiC))'
  - '                heapq.heappush(minH, [max(t, grid[neiR][neiC]), neiR, neiC])'
  cases:
  - input: '[[0,2],[1,3]]'
    expected: '3'
  - input: '[[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]'
    expected: '16'
  worked_example:
    input: '[[0,2],[1,3]]'
    steps:
    - ko: '시작: (0,0) 팝, 높이 0. 이웃 (0,1) 높이 2 → 시간 max(0,2)=2, (1,0) 높이 1 → 시간 max(0,1)=1로 힙에 추가.'
      en: 'Pop (0,0) with time 0. Neighbors: (0,1) height 2 → push time max(0,2)=2; (1,0) height 1 → push time max(0,1)=1.'
    - ko: (1,0) 팝, 높이 1, 시간 1. 이웃 (1,1) 높이 3 → 시간 max(1,3)=3으로 힙에 추가.
      en: Pop (1,0) with time 1. Neighbor (1,1) height 3 → push time max(1,3)=3.
    - ko: (0,1) 팝, 높이 2, 시간 2. 이웃 (1,1) 높이 3은 이미 시간 3으로 처리됨.
      en: Pop (0,1) with time 2. Neighbor (1,1) already in heap at time 3.
    - ko: (1,1) 팝, 시간 3 → 목표 도달, 답 3 반환.
      en: Pop (1,1) with time 3 → destination reached, return 3.
    answer: '3'
solution:
  code: "class Solution:\n    def swimInWater(self, grid: List[List[int]]) -> int:\n        N = len(grid)\n        visit = set()\n        minH = [[grid[0][0], 0, 0]]  # (time/max-height, r, c)\n        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]\n\n        visit.add((0, 0))\n        while minH:\n            t, r, c = heapq.heappop(minH)\n            if r == N - 1 and c == N - 1:\n                return t\n            for dr, dc in directions:\n                neiR, neiC = r + dr, c + dc\n                if (\n                    neiR < 0\n                    or neiC < 0\n                    or neiR == N\n                    or neiC == N\n                    or (neiR, neiC) in visit\n                ):\n                    continue\n                visit.add((neiR, neiC))\n                heapq.heappush(minH, [max(t, grid[neiR][neiC]), neiR, neiC])\n"
  complexity:
    time: O(n² log n)
    space: O(n²)
  followup:
  - ko: 이진 탐색으로 같은 문제를 풀 수 있을까요? 시간 T에 대해, 높이 ≤ T인 셀들로만 도달 가능한지 BFS/DFS로 확인하면서 T를 이진 탐색합니다.
    en: Can you solve this with binary search? Binary search on time T, then use BFS/DFS to check if destination is reachable using only cells with height ≤ T.
  - ko: 실제 경로를 구성하려면 어떻게 할까요? 다익스트라에서 부모 포인터를 추적한 다음, 목표에서 시작점까지 역추적합니다.
    en: How would you reconstruct the actual path? Track parent pointers during Dijkstra, then backtrack from destination to source.
  - ko: Union-Find를 사용하는 접근 방식은 어떨까요? 높이 순서로 셀을 정렬한 후, 시작점과 목표점이 연결될 때까지 Union-Find로 합집합을 만듭니다.
    en: How would Union-Find work here? Sort cells by elevation, then use Union-Find to connect components until start and destination are in the same set.
```