---
created: '2026-08-22'
date: '2026-08-22'
day: Day 94
difficulty: medium
id: A-094
source:
  curated_in:
  - neetcode150
  number: 1584
  platform: leetcode
  slug: min-cost-to-connect-all-points
  url: https://leetcode.com/problems/min-cost-to-connect-all-points/
tags:
- array
- union-find
- graph
- minimum-spanning-tree
- prims-algorithm
- kruskals-algorithm
- boruvkas-algorithm
title:
  en: Min Cost to Connect All Points
  ko: 모든 점을 연결하는 최소 비용
today: false
type: algorithm
updated: '2026-08-22'
visible: true
---

# 모든 점을 연결하는 최소 비용

## Data

```yaml
problem:
  title:
    ko: 모든 점을 연결하는 최소 비용
    en: Min Cost to Connect All Points
  statement:
    ko: '2D 평면 위의 정수 좌표를 나타내는 배열 points가 주어집니다. 여기서 points[i] = [xi, yi]입니다.


      두 점 [xi, yi]와 [xj, yj]를 연결하는 비용은 맨해튼 거리입니다: |xi - xj| + |yi - yj|. 여기서 |val|은 val의 절댓값입니다.


      모든 점을 연결하는 최소 비용을 반환하세요. 모든 점이 연결되어 있다는 것은 임의의 두 점 사이에 정확히 하나의 단순 경로가 존재한다는 의미입니다.'
    en: 'You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].


      The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.


      Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.'
  constraints:
  - 1 ≤ points.length ≤ 1000
  - -1e6 ≤ xi, yi ≤ 1e6
  - All pairs (xi, yi) are distinct
  io:
  - input: '[[0,0],[2,2],[3,10],[5,2],[7,0]]'
    output: '20'
  - input: '[[3,12],[-2,5],[-4,1]]'
    output: '18'
clarifying:
  items:
  - q:
      ko: 모든 점이 '연결되어 있다'는 것은 정확히 무엇을 의미하나요?
      en: What exactly does it mean for all points to be 'connected'?
    type: good
    why:
      ko: 정확히 하나의 단순 경로가 존재한다는 것은 트리 구조를 의미합니다 — N개의 노드, 정확히 N-1개의 간선, 사이클 없음.
      en: Exactly one path between any two points means a tree structure — N nodes with exactly N-1 edges and no cycles.
  - q:
      ko: N개의 점을 연결하려면 정확히 몇 개의 간선이 필요한가요?
      en: How many edges are needed to connect N points?
    type: good
    why:
      ko: 사이클을 만들지 않으면서 모든 노드를 연결하려면 정확히 N-1개의 간선이 필요합니다.
      en: Exactly N-1 edges connect all N nodes without creating cycles — this is the tree property.
  - q:
      ko: '맨해튼 거리가 아닌 다른 거리 메트릭(예: 유클리드)을 사용할 수 있나요?'
      en: Can we use a different distance metric, like Euclidean distance?
    type: distractor
    why:
      ko: 문제에서 명시적으로 맨해튼 거리만 사용하도록 지정되어 있습니다.
      en: The problem explicitly specifies only Manhattan distance; using a different metric violates the problem constraints.
  - q:
      ko: 가장 가까운 두 점을 항상 먼저 연결하면 최소 비용을 보장할까요?
      en: Does always connecting the two closest points guarantee minimum cost?
    type: distractor
    why:
      ko: 탐욕 알고리즘은 MST 문제에서 최적해를 보장하지 않습니다. Prim이나 Kruskal 같은 MST 알고리즘이 필요합니다.
      en: Greedy nearest-neighbor doesn't guarantee optimal MST; dedicated MST algorithms (Prim/Kruskal) are required.
  - q:
      ko: 이 문제가 최소 신장 트리(MST) 문제인 이유가 뭐예요?
      en: Why is this a Minimum Spanning Tree problem?
    type: good
    why:
      ko: 모든 노드를 연결하면서 총 비용을 최소화하는 것이 MST의 정의입니다.
      en: MST is defined as connecting all nodes with minimum total edge cost — exactly what this problem asks.
  - q:
      ko: 이 구현의 시간 복잡도가 O(n² log n)인 이유는 뭐예요?
      en: Why is the time complexity O(n² log n)?
    type: good
    why:
      ko: 모든 점 쌍 사이 간선을 만드는 데 O(n²), 각 간선을 힙에 넣고 빼는 데 O(log n)이므로 총 O(n² log n)입니다.
      en: O(n²) to build all edges + O(n² log n) heap operations (each of O(n²) edges pushed/popped with O(log n) cost).
  - q:
      ko: Union-Find를 사용하는 Kruskal 알고리즘이 더 효율적일까요?
      en: Would Kruskal's algorithm with Union-Find be faster?
    type: distractor
    why:
      ko: 두 알고리즘 모두 O(n² log n)입니다. O(n²)개 간선의 정렬이 병목이므로 Union-Find는 큰 개선을 주지 못합니다.
      en: Both are O(n² log n). Sorting O(n²) edges is the bottleneck, so Union-Find doesn't provide major speedup.
approach:
  items:
  - name:
      ko: Prim 알고리즘 (최소 힙 사용)
      en: Prim's Algorithm (with min-heap)
    complexity: O(n² log n) time / O(n²) space
    type: good
    why:
      ko: 한 노드에서 시작하여 방문하지 않은 노드 중 최소 비용 간선을 매번 선택하여 트리를 확장합니다.
      en: Starts from one node and greedily adds minimum-cost edge to unvisited node at each step. Heap enables efficient selection.
  - name:
      ko: Kruskal 알고리즘 (Union-Find 사용)
      en: Kruskal's Algorithm (with Union-Find)
    complexity: O(n² log n) time / O(n²) space
    type: good
    why:
      ko: 모든 간선을 비용순으로 정렬한 후, 사이클을 만들지 않는 간선들을 순서대로 선택합니다.
      en: Sort all edges by cost, then greedily add edges that don't create cycles using Union-Find.
  - name:
      ko: 완전 탐색 (모든 가능한 연결 시도)
      en: Brute Force Enumeration
    complexity: O(n!) time / O(n) space
    type: distractor
    why:
      ko: 모든 가능한 트리 구조를 시도하는 것은 지수 시간이 걸려 n=1000에서 현실적으로 불가능합니다.
      en: Enumerating all tree structures takes factorial time — completely infeasible for n=1000.
  - name:
      ko: 탐욕 최근린 (가장 가까운 점 반복 선택)
      en: Greedy Nearest Neighbor
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 항상 가장 가까운 미방문 점을 선택하는 것은 O(n²)이지만, 최적해를 보장하지 못합니다.
      en: Selecting nearest unvisited node is O(n²) but doesn't guarantee optimal spanning tree.
  - name:
      ko: 다익스트라 알고리즘
      en: Dijkstra's Algorithm
    complexity: O(n² log n) time / O(n²) space
    type: distractor
    why:
      ko: 다익스트라는 단일 출발점의 최단 경로를 찾는 알고리즘이며, MST 문제와는 다릅니다.
      en: Dijkstra solves single-source shortest paths, not minimum spanning trees — different problems.
logic:
  format: slot
  slots:
  - label:
      ko: 그래프 크기 N 결정
      en: Determine graph size N
    indent: 0
    options:
    - code: N = len(points)
      type: good
      why:
        ko: 점의 개수가 곧 그래프의 노드 개수입니다.
        en: Number of points equals number of nodes in the graph.
    - code: N = len(points) - 1
      type: distractor
      why:
        ko: '오류: 0부터 N-1까지 N개의 노드가 있으므로 len(points)를 그대로 사용합니다.'
        en: 'Off-by-one error: we have exactly len(points) nodes indexed 0 to N-1.'
    - code: N = len(points) * (len(points) - 1) // 2
      type: distractor
      why:
        ko: 이것은 간선의 개수(조합)입니다. 노드의 개수가 아닙니다.
        en: This counts edges (combinations), not nodes.
  - label:
      ko: 모든 점 쌍의 맨해튼 거리 계산 및 간선 추가
      en: Calculate Manhattan distance for all pairs and add edges
    indent: 0
    options:
    - code: dist = abs(x1 - x2) + abs(y1 - y2)
      type: good
      why:
        ko: '맨해튼 거리 공식: |x1 - x2| + |y1 - y2|. 무방향 그래프이므로 양방향 간선을 모두 추가합니다.'
        en: Manhattan distance = |x1-x2| + |y1-y2|. Add edges in both directions for undirected graph.
    - code: dist = abs(x1 - x2) * abs(y1 - y2)
      type: distractor
      why:
        ko: '오류: 덧셈이어야 합니다. 곱셈은 맨해튼 거리가 아닙니다.'
        en: 'Wrong: should add, not multiply. Multiplication is not Manhattan distance.'
    - code: dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
      type: distractor
      why:
        ko: 이것은 유클리드 거리의 제곱입니다. 문제는 맨해튼 거리를 명시합니다.
        en: This is squared Euclidean distance. Problem requires Manhattan distance.
  - label:
      ko: 'Prim 알고리즘 초기화: 결과값, 방문 집합, 최소 힙'
      en: 'Initialize Prim: result, visited set, min heap'
    indent: 0
    options:
    - code: 'minH = [[0, 0]]  # [cost, point]'
      type: good
      why:
        ko: 노드 0부터 시작 (비용 0). 최소 힙은 항상 가장 작은 비용 간선을 먼저 처리합니다.
        en: Start from node 0 with cost 0. Min heap ensures minimum-cost edges are always processed first.
    - code: minH = [[0, i] for i in range(N)]
      type: distractor
      why:
        ko: 모든 노드를 초기화하면 불필요한 중복 처리가 발생합니다.
        en: Initializing all nodes causes redundant duplicate processing in the main loop.
    - code: minH = []
      type: distractor
      why:
        ko: 빈 힙은 처리할 간선이 없습니다. 최소한 시작 노드는 있어야 합니다.
        en: Empty heap has nothing to process. Must start with at least one node.
  - label:
      ko: 최소 비용 간선 추출 및 중복 확인
      en: Pop minimum edge and skip if node already visited
    indent: 1
    options:
    - code: 'if i in visit:'
      type: good
      why:
        ko: 같은 노드가 여러 번 힙에 들어갈 수 있으므로, 이미 방문한 노드는 건너뜁니다.
        en: A node can be added to heap multiple times with different edges. Skip if already processed.
    - code: 'if cost == 0: continue'
      type: distractor
      why:
        ko: 비용이 0이 아닌 것만 처리한다는 조건은 틀렸습니다. 모든 중복을 확인해야 합니다.
        en: Checking cost value is incorrect. Must check if node is visited, not cost value.
    - code: '# 확인 생략'
      type: distractor
      why:
        ko: 중복 확인이 없으면 같은 노드를 여러 번 처리하여 비효율적입니다.
        en: Without duplicate check, same node processed multiple times, causing inefficiency.
  - label:
      ko: 현재 간선 비용을 결과에 더하고 노드를 방문 처리
      en: Add edge cost to result and mark node as visited
    indent: 1
    options:
    - code: res += cost
      type: good
      why:
        ko: 선택된 간선의 비용을 누적하고, 해당 노드를 방문 완료합니다. 각 노드는 정확히 한 번만 처리됩니다.
        en: Accumulate the selected edge cost and mark node as processed. Each node contributes to result exactly once.
    - code: res += cost * 2
      type: distractor
      why:
        ko: 간선의 비용을 두 배로 세면 잘못된 결과입니다.
        en: Doubling the cost gives wrong answer. Each edge counted once.
    - code: res = cost + res
      type: distractor
      why:
        ko: 같은 의미지만 반대 순서입니다. += 연산자가 더 명확합니다.
        en: Same result but += is clearer. Minor style difference.
  - label:
      ko: 현재 노드의 미방문 이웃들을 힙에 추가
      en: Add unvisited neighbors to heap for future processing
    indent: 1
    options:
    - code: 'if nei not in visit:'
      type: good
      why:
        ko: 현재 노드에서 미방문 노드로 가는 모든 간선을 힙에 추가합니다. 힙이 비용순으로 정렬되어 다음 최소값을 빠르게 찾습니다.
        en: Add all edges from current node to unvisited nodes. Heap ordering ensures next minimum is found in O(log n).
    - code: 'for neiCost, nei in adj[i]: heapq.heappush(minH, [neiCost, nei])'
      type: distractor
      why:
        ko: 방문 체크 없이 모든 이웃을 추가하면 이미 방문한 노드도 힙에 들어갑니다.
        en: Without visited check, adds already-processed nodes, wasting heap space.
    - code: 'for neiCost, nei in adj[i]: heapq.heappush(minH, [neiCost, nei]) if nei not in minH'
      type: distractor
      why:
        ko: 힙에서 존재 여부를 확인하려면 O(n) 시간이 필요합니다. 방문 집합 체크가 정확합니다.
        en: Checking if in heap is O(n). Visited set check is O(1) and correct.
trace:
  code:
  - 'class Solution:'
  - '    def minCostConnectPoints(self, points: List[List[int]]) -> int:'
  - '        N = len(points)'
  - '        adj = {i: [] for i in range(N)}  # i : list of [cost, node]'
  - '        for i in range(N):'
  - '            x1, y1 = points[i]'
  - '            for j in range(i + 1, N):'
  - '                x2, y2 = points[j]'
  - '                dist = abs(x1 - x2) + abs(y1 - y2)'
  - '                adj[i].append([dist, j])'
  - '                adj[j].append([dist, i])'
  - ''
  - '        # Prim''s'
  - '        res = 0'
  - '        visit = set()'
  - '        minH = [[0, 0]]  # [cost, point]'
  - '        while len(visit) < N:'
  - '            cost, i = heapq.heappop(minH)'
  - '            if i in visit:'
  - '                continue'
  - '            res += cost'
  - '            visit.add(i)'
  - '            for neiCost, nei in adj[i]:'
  - '                if nei not in visit:'
  - '                    heapq.heappush(minH, [neiCost, nei])'
  - '        return res'
  cases:
  - input: '[[0,0],[2,2],[3,10],[5,2],[7,0]]'
    expected: '20'
  - input: '[[3,12],[-2,5],[-4,1]]'
    expected: '18'
  worked_example:
    input: '[[0,0],[2,2],[3,10],[5,2],[7,0]]'
    steps:
    - ko: '점들: P0(0,0), P1(2,2), P2(3,10), P3(5,2), P4(7,0). 핵심 거리: P0-P1=4, P1-P3=3, P3-P4=4, P1-P2=9.'
      en: 'Points: P0(0,0), P1(2,2), P2(3,10), P3(5,2), P4(7,0). Key distances: P0-P1=4, P1-P3=3, P3-P4=4, P1-P2=9.'
    - ko: 'Prim 시작: 힙=[[0,0]], 결과=0, 방문={}. 노드0 추출, 비용 0 추가, 이웃 P1,P2,P3,P4를 힙에 추가.'
      en: 'Start Prim: heap=[[0,0]], result=0, visited={}. Extract node 0 (cost 0), add neighbors P1,P2,P3,P4 to heap.'
    - ko: '반복 1: [4,1] 추출, 노드1 방문, 결과 += 4 = 4. 노드1의 미방문 이웃 P3(비용3), P2(비용9), P4(비용7) 추가.'
      en: 'Iteration 1: Pop [4,1], visit node 1, result=4. Add neighbors P3(3), P2(9), P4(7) to heap.'
    - ko: '반복 2: [3,3] 추출, 노드3 방문, 결과 += 3 = 7. 노드3의 미방문 이웃 P2, P4 추가.'
      en: 'Iteration 2: Pop [3,3], visit node 3, result=7. Add unvisited neighbors to heap.'
    - ko: '반복 3: [4,4] 추출, 노드4 방문, 결과 += 4 = 11. 노드4의 미방문 이웃 P2 추가.'
      en: 'Iteration 3: Pop [4,4], visit node 4, result=11. Add neighbor P2 to heap.'
    - ko: '반복 4: [9,2] 추출, 노드2 방문, 결과 += 9 = 20. 모든 5개 노드 방문 완료, 반환값=20.'
      en: 'Iteration 4: Pop [9,2], visit node 2, result=20. All 5 nodes visited. Return 20.'
    answer: '20'
solution:
  code: "class Solution:\n    def minCostConnectPoints(self, points: List[List[int]]) -> int:\n        N = len(points)\n        adj = {i: [] for i in range(N)}  # i : list of [cost, node]\n        for i in range(N):\n            x1, y1 = points[i]\n            for j in range(i + 1, N):\n                x2, y2 = points[j]\n                dist = abs(x1 - x2) + abs(y1 - y2)\n                adj[i].append([dist, j])\n                adj[j].append([dist, i])\n\n        # Prim's\n        res = 0\n        visit = set()\n        minH = [[0, 0]]  # [cost, point]\n        while len(visit) < N:\n            cost, i = heapq.heappop(minH)\n            if i in visit:\n                continue\n            res += cost\n            visit.add(i)\n            for neiCost, nei in adj[i]:\n                if nei not in visit:\n                    heapq.heappush(minH, [neiCost, nei])\n        return res\n"
  complexity:
    time: O(n² log n)
    space: O(n²)
  followup:
  - ko: Kruskal 알고리즘으로 어떻게 구현할까요? 두 알고리즘의 시간 복잡도를 비교하면?
    en: How would you implement Kruskal's algorithm? How do the time complexities compare?
  - ko: n=1,000,000일 때 O(n²) 공간을 사용할 수 없다면 어떻게 할까요?
    en: If n=1,000,000 and you can't use O(n²) space, what would you do?
  - ko: 이 문제를 완전 그래프가 아닌 희소 그래프에 적용하면 어떻게 달라질까요?
    en: How would the approach change if the input were a sparse graph instead of a complete graph?
```