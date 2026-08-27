---
created: '2026-08-23'
date: '2026-08-23'
day: Day 95
difficulty: medium
id: A-095
source:
  curated_in:
  - neetcode150
  number: 743
  platform: leetcode
  slug: network-delay-time
  url: https://leetcode.com/problems/network-delay-time/
status: draft
tags:
- depth-first-search
- breadth-first-search
- graph
- heap-priority-queue
- shortest-path
- dijkstra
title:
  en: Network Delay Time
  ko: 네트워크 지연 시간
today: false
type: algorithm
updated: '2026-08-23'
visible: true
---

# 네트워크 지연 시간

## Data

```yaml
problem:
  title:
    ko: 네트워크 지연 시간
    en: Network Delay Time
  statement:
    en: 'You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (u_i, v_i, w_i), where u_i is the source node, v_i is the target node, and w_i is the time it takes for a signal to travel from source to target.


      We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.'
    ko: 'n개의 노드(1부터 n까지 레이블)로 구성된 네트워크가 주어집니다. 또한 times 리스트가 주어지는데, times[i] = (u_i, v_i, w_i)는 방향 간선을 나타내며, u_i는 출발 노드, v_i는 도착 노드, w_i는 출발에서 도착까지 신호가 이동하는 데 걸리는 시간입니다.


      노드 k에서 신호를 보냅니다. 모든 n개의 노드가 신호를 받는 데 걸리는 최소 시간을 반환하세요. 모든 노드가 신호를 받을 수 없으면 -1을 반환하세요.'
  constraints:
  - 1 ≤ k ≤ n ≤ 100
  - 1 ≤ times.length ≤ 6000
  - 1 ≤ u_i, v_i ≤ n; 0 ≤ w_i ≤ 100
  - All pairs (u_i, v_i) are unique
  io:
  - input: '[[2,1,1],[2,3,1],[3,4,1]]

      4

      2'
    output: '2'
  - input: '[[1,2,1]]

      2

      1'
    output: '1'
  - input: '[[1,2,1]]

      2

      2'
    output: '-1'
clarifying:
  items:
  - q:
      ko: 출발 노드 k도 '신호를 받은' 노드로 카운트되나요?
      en: Does the source node k count as receiving the signal?
    type: good
    why:
      ko: 네. 신호는 시간 0에 노드 k에서 시작하므로, k는 항상 신호를 받습니다.
      en: Yes. The signal originates at k at time 0, so k always receives it immediately.
  - q:
      ko: 그래프가 항상 모든 노드를 연결하고 있나요?
      en: Is the graph always fully connected?
    type: good
    why:
      ko: 아니요. 일부 노드에 도달할 수 없으면 -1을 반환해야 합니다.
      en: No. Some nodes may be unreachable from k, in which case we return -1.
  - q:
      ko: 간선의 가중치가 음수일 수 있나요?
      en: Can edge weights be negative?
    type: good
    why:
      ko: 아니요. 제약 조건에서 0 ≤ w_i ≤ 100입니다.
      en: No. Constraints specify 0 ≤ w_i ≤ 100, so all weights are non-negative.
  - q:
      ko: 같은 두 노드 사이에 여러 간선이 있을 수 있나요?
      en: Can there be multiple edges between the same pair of nodes?
    type: good
    why:
      ko: 아니요. 제약 조건에서 '모든 쌍 (u_i, v_i)는 고유하다'고 명시됩니다.
      en: No. The constraint states all pairs (u_i, v_i) are unique.
  - q:
      ko: 신호를 받는 노드의 순서가 중요한가요?
      en: Does the order in which nodes receive the signal matter?
    type: distractor
    why:
      ko: 아니요. 우리는 모든 노드가 신호를 받는 데 걸리는 최대 시간만 반환하면 됩니다.
      en: No. We only need the maximum arrival time across all nodes.
  - q:
      ko: 같은 시간에 여러 노드가 신호를 받을 수 있나요?
      en: Can multiple nodes receive the signal simultaneously?
    type: distractor
    why:
      ko: 네, 가능합니다. 예를 들어, 두 이웃 노드까지의 거리가 같으면 동시에 신호를 받습니다.
      en: Yes. For instance, if two neighbors are both distance 1 from the source, they both receive at time 1.
approach:
  items:
  - name:
      ko: 다익스트라 알고리즘 (최소 힙)
      en: Dijkstra's Algorithm with Min-Heap
    complexity: O(E log V) time / O(V + E) space
    type: good
    why:
      ko: 최소 힙으로 항상 가장 짧은 거리의 미방문 노드를 처리하므로 최적입니다. 비음수 가중치에 완벽합니다.
      en: Always processes the unvisited node with minimum distance first. Optimal for non-negative weights; each node is finalized only once.
  - name:
      ko: BFS 및 거리 업데이트
      en: BFS with Distance Update
    complexity: O(V × E) time / O(V) space
    type: distractor
    why:
      ko: BFS는 단위 가중치 그래프에 최적이지만, 이 문제에서는 매우 비효율적입니다. 노드를 여러 번 처리할 수 있습니다.
      en: BFS works only for uniform weights. For varied weights, nodes may be processed multiple times, making it much slower than Dijkstra's.
  - name:
      ko: 깊이 우선 탐색 (DFS)
      en: Depth-First Search (DFS)
    complexity: O(V + E) time / O(V + E) space
    type: distractor
    why:
      ko: 가중치 그래프에서 최단 경로를 찾을 수 없습니다. 모든 경로를 탐색해야 하므로 부정확합니다.
      en: Cannot find shortest paths in weighted graphs. DFS doesn't consider weights properly and would give incorrect results.
  - name:
      ko: 벨만-포드 알고리즘
      en: Bellman-Ford Algorithm
    complexity: O(V × E) time / O(V) space
    type: distractor
    why:
      ko: 음수 가중치를 처리할 수 있지만, 이 문제에서는 불필요합니다. 다익스트라보다 훨씬 느립니다.
      en: Handles negative weights but unnecessary here. Much slower than Dijkstra's for non-negative weights.
logic:
  format: slot
  slots:
  - label:
      ko: 그래프를 인접 리스트로 표현
      en: Build graph as adjacency list
    indent: 0
    options:
    - code: edges = collections.defaultdict(list)
      type: good
      why:
        ko: defaultdict(list)를 사용하면 존재하지 않는 노드를 자동으로 빈 리스트로 초기화합니다. 간선을 u → v로 저장합니다.
        en: defaultdict auto-initializes missing nodes as empty lists. Stores edges as u → (v, weight) pairs for efficient lookup.
    - code: edges = {}
      type: distractor
      why:
        ko: 빈 딕셔너리는 존재하지 않는 키 접근 시 KeyError를 발생시킵니다.
        en: Plain dict raises KeyError on missing keys; would require extra checks.
    - code: edges = [[] for _ in range(n + 1)]
      type: distractor
      why:
        ko: 배열도 작동하지만, defaultdict가 더 간결합니다. 배열은 메모리를 더 낭비합니다.
        en: Works but less elegant; wastes space for nodes with no outgoing edges.
  - label:
      ko: 최소 힙과 방문 추적 초기화
      en: Initialize min-heap and visited set
    indent: 0
    options:
    - code: minHeap = [(0, k)]
      type: good
      why:
        ko: 최소 힙에 (거리, 노드) 튜플을 저장합니다. 거리를 먼저 저장하므로 최소값이 항상 먼저 추출됩니다.
        en: Heap stores (distance, node). Distance comes first, so Python's heapq always pops the nearest unvisited node.
    - code: minHeap = [(k, 0)]
      type: distractor
      why:
        ko: 튜플 순서를 반대로 하면 노드가 먼저 정렬되므로 다익스트라가 깨집니다.
        en: 'Reversing tuple order breaks Dijkstra''s: heap sorts by node ID first, not distance.'
    - code: 'minHeap = [(0, k)]

        visit = {k}'
      type: distractor
      why:
        ko: 시작 노드를 미리 방문으로 표시하면 첫 반복에서 건너뛰어 시간을 업데이트하지 못합니다.
        en: Pre-marking source as visited causes the first iteration to skip it, never updating the time.
  - label:
      ko: 최소 거리 노드 추출
      en: Extract node with minimum distance from heap
    indent: 1
    options:
    - code: w1, n1 = heapq.heappop(minHeap)
      type: good
      why:
        ko: heappop은 최소 거리를 가진 노드를 꺼냅니다. 이것이 다익스트라 정확성의 핵심입니다.
        en: heappop extracts the node with minimum known distance. Key to Dijkstra's correctness and optimality.
    - code: w1, n1 = min(minHeap)
      type: distractor
      why:
        ko: min()은 요소를 제거하지 않고, 비효율적입니다.
        en: min() doesn't remove the element and is O(n), not O(log n).
    - code: n1, w1 = heapq.heappop(minHeap)
      type: distractor
      why:
        ko: 튜플 순서를 바꾸면 노드와 거리를 혼동합니다.
        en: Swapping tuple order confuses distance with node ID.
  - label:
      ko: 이미 방문한 노드 건너뛰기
      en: Skip if node already visited
    indent: 1
    options:
    - code: 'if n1 in visit:'
      type: good
      why:
        ko: 같은 노드가 여러 번 힙에 들어갈 수 있으므로, 이미 최적해를 찾은 노드는 건너뜁니다.
        en: Same node may be pushed multiple times with different distances. Once visited with optimal distance, skip future entries.
    - code: 'if n1 in visit: break'
      type: distractor
      why:
        ko: break를 사용하면 전체 루프를 종료하여 다른 노드들을 처리하지 못합니다.
        en: break exits the entire while loop, missing reachable nodes.
    - code: 'if n1 not in visit: continue'
      type: distractor
      why:
        ko: 조건을 반대로 하면 미방문 노드를 건너뛰고 방문한 노드만 처리합니다.
        en: Inverting the condition skips unvisited nodes and processes visited ones—backwards.
  - label:
      ko: 노드 방문 처리 및 시간 기록
      en: Mark as visited and record arrival time
    indent: 1
    options:
    - code: visit.add(n1)
      type: good
      why:
        ko: 방문 집합에 추가하여 중복 처리를 방지합니다. 현재 거리(w1)를 기록합니다—마지막 방문 노드의 시간이 답입니다.
        en: Add to visited to prevent reprocessing. Record the current distance—the last node visited has the maximum time.
    - code: 'visit.add(n1)

        t = min(t, w1)'
      type: distractor
      why:
        ko: 최소값을 취하면 안 됩니다. 우리는 최대 도착 시간(가장 마지막 노드)이 필요합니다.
        en: min() is wrong; we need the maximum arrival time (the bottleneck node).
    - code: 't = w1

        if n1 not in visit: visit.add(n1)'
      type: distractor
      why:
        ko: 이미 if 조건으로 방문 여부를 확인했으므로, 추가 확인은 불필요합니다.
        en: Redundant check; we've already skipped visited nodes above.
  - label:
      ko: 미방문 이웃을 힙에 추가
      en: Add unvisited neighbors to heap
    indent: 2
    options:
    - code: heapq.heappush(minHeap, (w1 + w2, n2))
      type: good
      why:
        ko: 각 미방문 이웃에 대해, 출발지에서의 누적 거리(w1 + w2)를 계산하고 힙에 추가합니다. 나중에 더 먼 거리는 자동으로 건너뜁니다.
        en: For each unvisited neighbor, compute cumulative distance from source. Push to heap. Later redundant entries are skipped via visited check.
    - code: "for n2, w2 in edges[n1]:\n    heapq.heappush(minHeap, (w1 + w2, n2))"
      type: distractor
      why:
        ko: 미방문 여부를 확인하지 않으면 불필요한 항목이 힙에 들어갑니다. 다익스트라는 여전히 작동하지만 비효율적입니다.
        en: Without the visited check, waste heap space. Dijkstra still works but is less efficient.
    - code: "for n2, w2 in edges[n1]:\n    heapq.heappush(minHeap, (w2, n2))"
      type: distractor
      why:
        ko: w1을 더하지 않으면 직접 간선 가중치만 사용되고, 출발지에서의 실제 거리를 무시합니다.
        en: Forgetting w1 means only the direct edge weight is used, not the cumulative distance from source.
  - label:
      ko: 결과 반환
      en: Return result based on connectivity
    indent: 0
    options:
    - code: return t if len(visit) == n else -1
      type: good
      why:
        ko: 모든 n개 노드를 방문했으면 최대 도착 시간 t를 반환합니다. 그렇지 않으면 일부 노드에 도달할 수 없으므로 -1을 반환합니다.
        en: If all n nodes are visited, all are reachable; return the last arrival time. Otherwise, return -1.
    - code: return t if len(visit) > 0 else -1
      type: distractor
      why:
        ko: 출발 노드는 항상 방문되므로 이 조건은 거의 항상 참입니다. 도달 불가능한 경우를 제대로 감지하지 못합니다.
        en: Source is always visited, so this nearly always returns t. Fails to detect unreachable nodes.
    - code: return t if len(visit) == n else 0
      type: distractor
      why:
        ko: 도달 불가능할 때 0을 반환하면 정답(0 또는 양수)과 구별할 수 없습니다. -1을 반환해야 합니다.
        en: Returning 0 for unreachable cases conflicts with possible actual answer 0. Must return -1.
trace:
  code:
  - 'class Solution:'
  - '    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:'
  - '        edges = collections.defaultdict(list)'
  - '        for u, v, w in times:'
  - '            edges[u].append((v, w))'
  - ''
  - '        minHeap = [(0, k)]'
  - '        visit = set()'
  - '        t = 0'
  - '        while minHeap:'
  - '            w1, n1 = heapq.heappop(minHeap)'
  - '            if n1 in visit:'
  - '                continue'
  - '            visit.add(n1)'
  - '            t = w1'
  - ''
  - '            for n2, w2 in edges[n1]:'
  - '                if n2 not in visit:'
  - '                    heapq.heappush(minHeap, (w1 + w2, n2))'
  - '        return t if len(visit) == n else -1'
  - ''
  - '        # O(E * logV)'
  cases:
  - input: '[[2,1,1],[2,3,1],[3,4,1]]

      4

      2'
    expected: '2'
  - input: '[[1,2,1]]

      2

      1'
    expected: '1'
  - input: '[[1,2,1]]

      2

      2'
    expected: '-1'
  worked_example:
    input: '[[2,1,1],[2,3,1],[3,4,1]]

      4

      2'
    steps:
    - ko: '초기: times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2. 그래프: 2→1(1), 2→3(1), 3→4(1). 힙=[(0,2)], 방문={}, t=0'
      en: 'Start: Graph is 2→1(1), 2→3(1), 3→4(1). heap=[(0,2)], visited={}, t=0'
    - ko: '노드 2 처리 (거리 0): 방문={2}, t=0. 이웃 1(거리1), 3(거리1) 추가. 힙=[(1,1),(1,3)]'
      en: 'Pop (0,2): visit node 2. Add neighbors 1 and 3 at distance 1. heap=[(1,1),(1,3)]'
    - ko: '노드 1 처리 (거리 1): 방문={2,1}, t=1. 노드 1은 이웃 없음. 힙=[(1,3)]'
      en: 'Pop (1,1): visit node 1. No neighbors. heap=[(1,3)]'
    - ko: '노드 3 처리 (거리 1): 방문={2,1,3}, t=1. 이웃 4(거리2) 추가. 힙=[(2,4)]'
      en: 'Pop (1,3): visit node 3. Add neighbor 4 at distance 2. heap=[(2,4)]'
    - ko: '노드 4 처리 (거리 2): 방문={2,1,3,4}, t=2. 노드 4는 이웃 없음. 힙 비어있음.'
      en: 'Pop (2,4): visit node 4. No neighbors. heap empty.'
    - ko: 모든 4개 노드 방문됨. len(visit)=4=n이므로 답=t=2
      en: All 4 nodes visited. len(visit)==n, so return t=2
    answer: '2'
solution:
  code: "class Solution:\n    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:\n        edges = collections.defaultdict(list)\n        for u, v, w in times:\n            edges[u].append((v, w))\n\n        minHeap = [(0, k)]\n        visit = set()\n        t = 0\n        while minHeap:\n            w1, n1 = heapq.heappop(minHeap)\n            if n1 in visit:\n                continue\n            visit.add(n1)\n            t = w1\n\n            for n2, w2 in edges[n1]:\n                if n2 not in visit:\n                    heapq.heappush(minHeap, (w1 + w2, n2))\n        return t if len(visit) == n else -1\n\n        # O(E * logV)\n"
  complexity:
    time: O(E log V)
    space: O(V + E)
  followup:
  - ko: 여러 출발점이 있다면? 모든 출발 노드를 최초에 거리 0으로 힙에 추가하세요.
    en: Multiple sources? Initialize the heap with all source nodes at distance 0.
  - ko: 음수 가중치를 허용한다면? 벨만-포드 알고리즘을 사용하세요 (O(VE)).
    en: Negative weights? Use Bellman-Ford algorithm instead (O(VE)).
  - ko: 신호를 마지막으로 받는 노드의 번호를 반환하려면? t를 업데이트할 때 현재 노드도 함께 기록하세요.
    en: Return which node receives the signal last? Track the node ID along with the maximum time.
```